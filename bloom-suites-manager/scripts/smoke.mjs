// Smoke test for the pure logic (run via esbuild bundling).
import { buildSeedData } from "../src/seed.js";
import {
  occupancy, rentRoll, monthTotals, buildActionCenter, rentStatus,
  suiteStatus, rentReminder, renewalMessage,
} from "../src/automation.js";
import { monthKey } from "../src/format.js";

const data = buildSeedData();
const assert = (cond, msg) => {
  if (!cond) { console.error("FAIL:", msg); process.exitCode = 1; }
  else console.log("ok  :", msg);
};

assert(data.suites.length === 12, `12 suites seeded (got ${data.suites.length})`);
assert(data.tenants.length === 9, `9 tenants seeded (got ${data.tenants.length})`);
assert(data.ledger.length > 20, `rent ledger generated (${data.ledger.length} rows)`);

const occ = occupancy(data);
console.log("    occupancy:", occ);
assert(occ.total === 12, "12 suites total");
assert(occ.vacant === 3, `3 vacant suites (got ${occ.vacant})`);
assert(occ.notice === 1, `1 suite on notice (got ${occ.notice})`);
assert(occ.rate >= 60 && occ.rate <= 100, `occupancy rate sane (${occ.rate}%)`);

const totals = monthTotals(data, monthKey());
console.log("    this month:", { roll: rentRoll(data), collected: totals.collected, outstanding: totals.outstanding });
assert(totals.outstanding > 0, "some rent outstanding this month");
assert(totals.billed === totals.collected + totals.outstanding, "billed = collected + outstanding");

const ac = buildActionCenter(data);
console.log("    action center:", {
  total: ac.total, rent: ac.groups.rent.length, renewals: ac.groups.renewals.length,
  vacancies: ac.groups.vacancies.length, maintenance: ac.groups.maintenance.length, leads: ac.groups.leads.length,
});
assert(ac.total > 0, "action center surfaces tasks");
assert(ac.groups.rent.length === 3, `3 rent-collection tasks (got ${ac.groups.rent.length})`);
assert(ac.groups.rent.every((t) => t.status === "late" || t.status === "due"), "rent tasks are due/late");
assert(ac.groups.renewals.length >= 1, "lease renewal task present");
assert(ac.groups.renewals.every((t) => t.tenant.status === "active"), "renewals exclude tenants on notice");
assert(ac.groups.vacancies.length === 4, `4 vacancy tasks: 3 vacant + 1 notice (got ${ac.groups.vacancies.length})`);
assert(ac.groups.maintenance.length === 3, `3 open maintenance tickets (got ${ac.groups.maintenance.length})`);

// A notice suite is not counted "occupied"
const noticeSuite = data.suites.find((s) => suiteStatus(s, data.tenants) === "notice");
assert(!!noticeSuite, "found the suite on notice");

// Rent status: an unpaid current-month row is collectible (due early in the
// month, late once past the grace period — both are "to collect").
const unpaid = data.ledger.find((r) => r.month === monthKey() && !r.paidDate);
assert(["due", "late"].includes(rentStatus(unpaid, data.settings)), "unpaid current-month rent is due or late");

// Messages personalized
const t = data.tenants[0];
const row = data.ledger.find((r) => r.tenantId === t.id && !r.paidDate) || data.ledger.find((r) => r.tenantId === t.id);
assert(rentReminder(t, row, data.settings).includes(t.name.split(" ")[0]), "rent reminder personalized");
assert(renewalMessage(t, data.settings).includes(data.settings.businessName), "renewal message includes business name");

console.log(process.exitCode ? "\nSMOKE TEST FAILED" : "\nSMOKE TEST PASSED");
