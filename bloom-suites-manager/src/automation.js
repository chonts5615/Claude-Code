// Automation engine — pure functions that turn raw data into the derived
// signals and daily task list that make the app save the owner time.
import { daysAgo, todayISO, monthKey, monthLabel } from "./format.js";

const APPLICANT_FOLLOWUP_DAYS = 3;

export const firstName = (name) => name.split(" ")[0];
export const tenantById = (tenants, id) => tenants.find((t) => t.id === id) || null;
export const suiteById = (suites, id) => suites.find((s) => s.id === id) || null;

// Days from today until `iso` (negative = in the past).
export const daysUntil = (iso, base = todayISO()) => daysAgo(base, iso);

// --- Rent status (computed per ledger row) ---
export function rentStatus(row, settings, base = todayISO()) {
  if (row.paidDate) return "paid";
  const grace = settings?.lateGraceDays ?? 5;
  const dueDays = daysAgo(row.dueDate, base); // days since due (positive = past due)
  if (dueDays > grace) return "late";
  if (dueDays >= 0) return "due";
  return "upcoming";
}

// --- Suite status (vacant / occupied / notice) ---
export function suiteStatus(suite, tenants) {
  if (!suite.tenantId) return "vacant";
  const t = tenantById(tenants, suite.tenantId);
  if (!t || t.status === "past") return "vacant";
  if (t.status === "notice") return "notice";
  return "occupied";
}

export function occupancy(state) {
  const counts = { occupied: 0, vacant: 0, notice: 0 };
  state.suites.forEach((s) => counts[suiteStatus(s, state.tenants)]++);
  const total = state.suites.length;
  // "Notice" suites still occupied/paying this month, so count them as filled.
  const filled = counts.occupied + counts.notice;
  return { ...counts, total, rate: total ? Math.round((filled / total) * 100) : 0 };
}

// Potential monthly rent from all active/notice tenants.
export const rentRoll = (state) =>
  state.tenants.filter((t) => t.status !== "past").reduce((s, t) => s + t.rent, 0);

export function monthTotals(state, mk = monthKey()) {
  const rows = state.ledger.filter((r) => r.month === mk);
  const collected = rows.filter((r) => r.paidDate).reduce((s, r) => s + r.amount, 0);
  const outstanding = rows.filter((r) => !r.paidDate).reduce((s, r) => s + r.amount, 0);
  return { collected, outstanding, billed: collected + outstanding, rows };
}

// Whether a tenant should be billed for month `mk`. Single source of truth used
// by the Rent page, the store's billing action, and the Action Center, so they
// never disagree about who's billable.
export function eligibleToBill(tenant, mk) {
  if (tenant.status === "past") return false;
  if ((tenant.moveIn || tenant.leaseStart || "").substring(0, 7) > mk) return false; // before move-in
  if (tenant.status === "notice" && (tenant.leaseEnd || "9999-12").substring(0, 7) < mk) return false; // after move-out
  return true;
}

// Eligible tenants for `mk` who don't yet have a ledger row.
export function unbilledTenants(state, mk = monthKey()) {
  const billed = new Set(state.ledger.filter((r) => r.month === mk).map((r) => r.tenantId));
  return state.tenants.filter((t) => eligibleToBill(t, mk) && !billed.has(t.id));
}

// --- The Action Center: the automated daily to-do list ---
export function buildActionCenter(state, base = todayISO()) {
  const { tenants, suites, ledger, applicants, maintenance, settings } = state;
  const renewWindow = settings?.leaseRenewalWindowDays ?? 60;

  // 1. Rent to collect (any unpaid row already due).
  const rent = ledger
    .filter((r) => !r.paidDate && daysAgo(r.dueDate, base) >= 0)
    .map((r) => {
      const tenant = tenantById(tenants, r.tenantId);
      const status = rentStatus(r, settings, base);
      const overdue = daysAgo(r.dueDate, base);
      return { id: `rent-${r.id}`, kind: "rent", row: r, tenant, status, overdue, priority: 100 + (status === "late" ? overdue : 0) };
    })
    .filter((t) => t.tenant)
    .sort((a, b) => b.priority - a.priority);

  // 2. Leases coming up for renewal (active tenants only — not those on notice).
  // No lower bound: an active lease that's already lapsed keeps prompting until
  // the owner renews or gives notice, so an occupied suite is never left adrift.
  const renewals = tenants
    .filter((t) => t.status === "active")
    .map((t) => ({ tenant: t, daysLeft: daysUntil(t.leaseEnd, base) }))
    .filter((x) => x.daysLeft <= renewWindow)
    .map((x) => ({ id: `renew-${x.tenant.id}`, kind: "renewal", tenant: x.tenant, daysLeft: x.daysLeft, priority: 80 + (x.daysLeft < 0 ? 20 : 0) }))
    .sort((a, b) => a.daysLeft - b.daysLeft);

  // 3. Vacancies to fill (empty suites + suites with notice given).
  const vacancies = suites
    .map((s) => ({ suite: s, status: suiteStatus(s, tenants) }))
    .filter((x) => x.status !== "occupied")
    .map((x) => ({
      id: `vac-${x.suite.id}`,
      kind: "vacancy",
      suite: x.suite,
      upcoming: x.status === "notice",
      tenant: x.status === "notice" ? tenantById(tenants, x.suite.tenantId) : null,
      priority: x.status === "vacant" ? 75 : 55,
    }))
    .sort((a, b) => b.priority - a.priority);

  // 4. Open maintenance tickets.
  const maint = maintenance
    .filter((m) => m.status !== "done")
    .map((m) => ({ id: `maint-${m.id}`, kind: "maintenance", ticket: m, suite: suiteById(suites, m.suiteId), priority: 60 + (m.priority === "high" ? 30 : m.priority === "normal" ? 10 : 0) }))
    .sort((a, b) => b.priority - a.priority);

  // 5. Applicant follow-ups (still "new" — touring/applying clears the task so
  // recording progress removes it instead of re-surfacing it).
  const leads = applicants
    .filter((a) => a.status === "new" && daysAgo(a.added, base) >= APPLICANT_FOLLOWUP_DAYS)
    .map((a) => ({ id: `lead-${a.id}`, kind: "applicant", applicant: a, waitingDays: daysAgo(a.added, base), priority: 50 }));

  // 6. Rent not yet billed for the current month (so a new month doesn't slip
  // by unbilled just because the owner hasn't opened the Rent page).
  const curMonth = monthKey(base);
  const toBill = unbilledTenants(state, curMonth);
  const billing = toBill.length
    ? [{ id: `bill-${curMonth}`, kind: "billing", month: curMonth, count: toBill.length, priority: 95 }]
    : [];

  const groups = { billing, rent, renewals, vacancies, maintenance: maint, leads };
  const total =
    billing.length + rent.length + renewals.length + vacancies.length + maint.length + leads.length;
  return { groups, total };
}

// --- Ready-to-send message templates (copy-to-clipboard; no SMS backend in beta) ---
export function rentReminder(tenant, row, settings) {
  const owner = settings?.ownerName || "your suite manager";
  const biz = settings?.businessName || "the studio";
  return `Hi ${firstName(tenant.name)}, it's ${owner} at ${biz}. Friendly reminder that ${monthLabel(row.month)} rent ($${row.amount}) for ${tenant.suite} is due. Let me know if you have any questions — thank you!`;
}

export function renewalMessage(tenant, settings) {
  const owner = settings?.ownerName || "your suite manager";
  const biz = settings?.businessName || "the studio";
  return `Hi ${firstName(tenant.name)}! It's ${owner} at ${biz}. Your lease for ${tenant.suite} is coming up on ${tenant.leaseEnd}. I'd love to have you stay — want to set up a quick time to renew?`;
}

export function applicantMessage(applicant, settings) {
  const owner = settings?.ownerName || "the team";
  const biz = settings?.businessName || "our suites";
  return `Hi ${firstName(applicant.name)}! Thanks for your interest in a suite at ${biz}. This is ${owner} — are you free this week to come tour? Happy to answer any questions.`;
}
