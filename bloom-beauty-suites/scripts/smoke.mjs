// Smoke test for the pure logic (run via esbuild bundling, see package note).
import { buildSeedData } from "../src/seed.js";
import {
  clientStatus, daysUntilDue, buildActionCenter, completedAppointments,
  rebookMessage, lowStockItems, expiringItems, noShowCount, depositRecommended,
} from "../src/automation.js";
import { todayISO } from "../src/format.js";

const data = buildSeedData();
const assert = (cond, msg) => {
  if (!cond) {
    console.error("FAIL:", msg);
    process.exitCode = 1;
  } else {
    console.log("ok  :", msg);
  }
};

// Seed sanity
assert(data.clients.length === 16, `16 clients seeded (got ${data.clients.length})`);
assert(data.appointments.length > 50, `appointments generated (${data.appointments.length})`);

// Status spread should be roughly 13 / 2 / 1
const counts = { active: 0, lapsing: 0, lost: 0 };
data.clients.forEach((c) => counts[clientStatus(c)]++);
console.log("    status spread:", counts);
assert(counts.active >= 10, "most clients active");
assert(counts.lost >= 1, "at least one lost client");
assert(counts.lapsing >= 1, "at least one lapsing client");

// Appointments are anchored around today
const today = todayISO();
const future = data.appointments.filter((a) => a.date >= today && a.status === "scheduled");
assert(future.length > 0, `upcoming scheduled appts exist (${future.length})`);

// Action center produces tasks
const ac = buildActionCenter(data);
console.log("    action center:", {
  total: ac.total,
  rebook: ac.groups.rebook.length,
  winback: ac.groups.winback.length,
  reorder: ac.groups.reorder.length,
  expiring: ac.groups.expiring.length,
  waitlist: ac.groups.waitlist.length,
});
assert(ac.total > 0, "action center surfaces tasks");
assert(ac.groups.reorder.length === lowStockItems(data.inventory).length, "reorder matches low stock");

// Expiry days should be positive for future-dated items
const exp = expiringItems(data.inventory);
assert(exp.length > 0, `expiring items detected (${exp.length})`);
assert(ac.groups.expiring.every((t) => t.daysLeft >= 0), "expiry daysLeft is non-negative");

// Win-back clients are the lost ones, and never appear in rebook
assert(ac.groups.winback.every((t) => clientStatus(t.client) === "lost"), "winback only lost clients");
assert(ac.groups.rebook.every((t) => clientStatus(t.client) !== "lost"), "rebook excludes lost clients");

// Due math: a clearly overdue client
const overdue = data.clients.find((c) => daysUntilDue(c, data.settings) < -5);
assert(!!overdue, "found an overdue client");

// Message template includes the owner + client first name
const msg = rebookMessage(data.clients[0], data.settings);
assert(msg.includes(data.settings.ownerName) && msg.includes(data.clients[0].name.split(" ")[0]), "rebook message personalized");

// New effectiveness features: groups exist; no-show/deposit logic behaves
["confirm", "deposit", "reviews", "loyalty"].forEach((g) =>
  assert(Array.isArray(ac.groups[g]), `action center has ${g} group`));
const someClient = data.clients[0];
assert(typeof noShowCount(someClient.id, data.appointments) === "number", "noShowCount returns a number");
assert(depositRecommended({ ...someClient, requireDeposit: true }, data.appointments, data.settings) === true, "requireDeposit flag forces a deposit");

console.log("\nCompleted visits:", completedAppointments(data).length);
console.log(process.exitCode ? "\nSMOKE TEST FAILED" : "\nSMOKE TEST PASSED");
