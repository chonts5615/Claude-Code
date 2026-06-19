// Automation engine — pure functions that turn raw data into the derived
// signals and daily task list that make the app save the owner time.
// Nothing here mutates state; the store calls these to decide what to show.
import { daysAgo, todayISO, addDays } from "./format.js";

const EXPIRY_WINDOW_DAYS = 30; // flag products expiring within a month
const WAITLIST_FOLLOWUP_DAYS = 5; // nudge to follow up on stale waitlist entries

export const firstName = (name) => name.split(" ")[0];

// --- Client health (computed, never hand-maintained) ---------------------
// Based on how long it's been since the last visit vs. the client's own cadence.
export function clientStatus(client, base = todayISO()) {
  const expected = client.avgInterval || 21;
  const since = daysAgo(client.lastVisit, base);
  if (since > 75 && since > expected * 2) return "lost";
  if (since > expected + 10) return "lapsing";
  return "active";
}

// Days until the client is "due" for a rebook (negative = overdue).
export function daysUntilDue(client, _settings, base = todayISO()) {
  const expected = client.avgInterval || 21;
  return expected - daysAgo(client.lastVisit, base);
}

export function hasUpcomingAppointment(clientId, appointments, base = todayISO()) {
  return appointments.some(
    (a) => a.clientId === clientId && a.status === "scheduled" && a.date >= base
  );
}

export const completedAppointments = (state) =>
  state.appointments.filter((a) => a.status === "completed");

export const revenueOf = (appts) => appts.reduce((s, a) => s + a.price, 0);

// --- No-show / deposit policy ---------------------------------------------
export const noShowCount = (clientId, appointments) =>
  appointments.filter((a) => a.clientId === clientId && a.status === "no-show").length;

// A client earns a "ask for a deposit" prompt once they've no-showed enough
// (or the owner flips the per-client requireDeposit switch).
export function depositRecommended(client, appointments, settings) {
  if (client.requireDeposit) return true;
  return noShowCount(client.id, appointments) >= (settings?.noShowThreshold ?? 2);
}

// --- Inventory signals -----------------------------------------------------
export const lowStockItems = (inventory) =>
  inventory.filter((i) => i.qty <= i.reorder && !i.onOrder);

export const expiringItems = (inventory, base = todayISO()) =>
  inventory.filter((i) => i.expires && i.expires <= addDays(base, EXPIRY_WINDOW_DAYS) && !i.onOrder);

// --- The Action Center: the automated daily to-do list ---------------------
// Returns grouped tasks plus a total count. The UI renders each group and wires
// the one-tap actions; this function only decides WHAT needs attention.
export function buildActionCenter(state, base = todayISO()) {
  const { clients, appointments, inventory, waitlist, settings } = state;

  // 1. Clients due / overdue for a rebook with nothing already on the books.
  const rebook = clients
    .map((c) => ({ client: c, status: clientStatus(c, base), due: daysUntilDue(c, settings, base) }))
    .filter(
      (x) =>
        x.status !== "lost" &&
        x.due <= 0 &&
        !hasUpcomingAppointment(x.client.id, appointments, base)
    )
    .map((x) => ({
      id: `rebook-${x.client.id}`,
      kind: "rebook",
      client: x.client,
      overdueDays: -x.due,
      status: x.status,
      priority: 100 + -x.due + (x.status === "lapsing" ? 30 : 0),
    }))
    .sort((a, b) => b.priority - a.priority);

  // 2. Win-back: clients who have fully lapsed into "lost" with nothing booked.
  const winback = clients
    .filter((c) => clientStatus(c, base) === "lost" && !hasUpcomingAppointment(c.id, appointments, base))
    .map((c) => ({
      id: `winback-${c.id}`,
      kind: "winback",
      client: c,
      daysSince: daysAgo(c.lastVisit, base),
      priority: 20,
    }))
    .sort((a, b) => a.daysSince - b.daysSince);

  // 3. Inventory to reorder.
  const reorder = lowStockItems(inventory).map((i) => ({
    id: `reorder-${i.id}`,
    kind: "reorder",
    item: i,
    priority: 70 + (i.qty === 0 ? 40 : 0),
  }));

  // 4. Products expiring soon.
  const expiring = expiringItems(inventory, base).map((i) => ({
    id: `expiring-${i.id}`,
    kind: "expiring",
    item: i,
    daysLeft: daysAgo(base, i.expires), // days from today until expiry
    priority: 60,
  }));

  // 5. Waitlist follow-ups (still waiting — not yet contacted or booked).
  const waitlistFollowups = waitlist
    .filter((w) => w.status === "waiting" && daysAgo(w.added, base) >= WAITLIST_FOLLOWUP_DAYS)
    .map((w) => ({
      id: `waitlist-${w.id}`,
      kind: "waitlist",
      entry: w,
      waitingDays: daysAgo(w.added, base),
      priority: 50,
    }));

  const byClient = (id) => clients.find((c) => c.id === id);

  // 6. Confirm tomorrow's appointments (cuts no-shows).
  const tomorrow = addDays(base, 1);
  const confirm = appointments
    .filter((a) => a.status === "scheduled" && a.date === tomorrow && !a.confirmed)
    .map((a) => ({ id: `confirm-${a.id}`, kind: "confirm", appt: a, client: byClient(a.clientId), priority: 92 }))
    .filter((t) => t.client);

  // 7. Deposit reminders — upcoming visit for a client who's earned a deposit ask.
  const deposit = appointments
    .filter((a) => a.status === "scheduled" && a.date >= base && !a.depositCollected)
    .map((a) => ({ appt: a, client: byClient(a.clientId) }))
    .filter((x) => x.client && depositRecommended(x.client, appointments, settings))
    .map((x) => ({ id: `deposit-${x.appt.id}`, kind: "deposit", appt: x.appt, client: x.client, noShows: noShowCount(x.client.id, appointments), priority: 84 }));

  // 8. Ask recent visitors for a review (last 2 days, once).
  const reviews = appointments
    .filter((a) => a.status === "completed" && a.date >= addDays(base, -2) && a.date <= base && !a.reviewRequested)
    .map((a) => ({ id: `review-${a.id}`, kind: "review", appt: a, client: byClient(a.clientId), priority: 38 }))
    .filter((t) => t.client);

  // 9. Loyalty milestones — reward every Nth visit, once per milestone.
  const every = settings?.loyaltyEvery ?? 0;
  const loyalty = every > 0
    ? clients
        .filter((c) => c.visits > 0 && c.visits % every === 0 && (c.loyaltyRewardedAt || 0) < c.visits)
        .map((c) => ({ id: `loyalty-${c.id}`, kind: "loyalty", client: c, milestone: c.visits, priority: 44 }))
    : [];

  const groups = { confirm, deposit, rebook, winback, reorder, expiring, waitlist: waitlistFollowups, reviews, loyalty };
  const total =
    confirm.length + deposit.length + rebook.length + winback.length + reorder.length +
    expiring.length + waitlistFollowups.length + reviews.length + loyalty.length;
  return { groups, total };
}

// --- Ready-to-send message templates --------------------------------------
// No SMS backend in beta — these produce copy-ready text the owner pastes into
// her phone's Messages app, so she never has to think about wording.
export function rebookMessage(client, settings) {
  const owner = settings?.ownerName || "your lash artist";
  const biz = settings?.businessName || "the studio";
  return `Hi ${firstName(client.name)}! It's ${owner} at ${biz}. You're about due for your next fill — want me to get you on the books this week? 💕`;
}

export function winbackMessage(client, settings) {
  const owner = settings?.ownerName || "your lash artist";
  return `Hi ${firstName(client.name)}! It's ${owner} — I've missed seeing you! I'd love to get your lashes refreshed. I have some openings coming up if you'd like to come back in. 🌸`;
}

export function waitlistMessage(entry, settings) {
  const owner = settings?.ownerName || "your lash artist";
  const biz = settings?.businessName || "the studio";
  return `Hi ${firstName(entry.name)}! ${owner} from ${biz} here — a ${entry.service} spot just opened up. Want me to grab it for you?`;
}

export function confirmMessage(client, appt, settings) {
  const owner = settings?.ownerName || "your lash artist";
  return `Hi ${firstName(client.name)}! Confirming your ${appt.serviceName} appointment tomorrow at ${appt.time} with ${owner}. Reply YES to confirm, or let me know if you need to reschedule — see you soon! 💕`;
}

export function depositMessage(client, settings) {
  const owner = settings?.ownerName || "your lash artist";
  const amt = settings?.depositAmount ?? 25;
  return `Hi ${firstName(client.name)}! To hold your spot, ${owner} now asks for a $${amt} deposit that goes toward your service. Just let me know and I'll send a quick payment link. Thank you!`;
}

export function reviewMessage(client, settings) {
  const owner = settings?.ownerName || "your lash artist";
  const biz = settings?.businessName || "the studio";
  const link = settings?.reviewLink ? ` ${settings.reviewLink}` : "";
  return `Hi ${firstName(client.name)}! Thank you for visiting ${biz} 💕 If you loved your lashes, a quick review would mean the world to ${owner}:${link}`.trim();
}

export function loyaltyMessage(client, settings) {
  const owner = settings?.ownerName || "your lash artist";
  return `Hi ${firstName(client.name)}! That was visit #${client.visits} with ${owner} 🎉 Thank you for your loyalty — enjoy a little reward on your next visit!`;
}
