// Sample data for a fresh install so the owner can explore a populated app.
// Dates (leases, rent ledger, applicants, tickets) are generated RELATIVE to
// today so the demo always looks current.
import { todayISO, addDays, monthKey, addMonths } from "./format";

export const PROFESSIONS = [
  "Lash Artist", "Nail Tech", "Hair Stylist", "Esthetician",
  "Brow & Makeup", "Microblading", "Massage Therapist", "Spray Tan",
];

// 12 suites across three sizes. tenantSeed index links a tenant in at seed time.
const SUITE_SEED = [
  { name: "Suite 1", size: "100 sqft", rent: 550, tenant: "Bianca Flores" },
  { name: "Suite 2", size: "100 sqft", rent: 550, tenant: "Sophie Albers" },
  { name: "Suite 3", size: "100 sqft", rent: 550, tenant: "Chloe Bennett" },
  { name: "Suite 4", size: "100 sqft", rent: 550, tenant: null },
  { name: "Suite 5", size: "140 sqft", rent: 650, tenant: "Maya Johnson" },
  { name: "Suite 6", size: "140 sqft", rent: 650, tenant: "Kristen Mitchell" },
  { name: "Suite 7", size: "140 sqft", rent: 650, tenant: "Priya Patel" },
  { name: "Suite 8", size: "140 sqft", rent: 650, tenant: null },
  { name: "Suite 9", size: "180 sqft", rent: 750, tenant: "Tara Nguyen" },
  { name: "Suite 10", size: "180 sqft", rent: 750, tenant: "Gabriela Santos" },
  { name: "Suite 11", size: "180 sqft", rent: 750, tenant: "Hailey Brooks" },
  { name: "Suite 12", size: "180 sqft", rent: 750, tenant: null },
];

// leaseEndInDays drives the renewal automation; status 'notice' = moving out.
const TENANT_SEED = [
  { name: "Bianca Flores", profession: "Nail Tech", business: "Polished by Bianca", phone: "612-555-3001", email: "bianca@email.com", suite: "Suite 1", rent: 550, status: "active", leaseStartDaysAgo: 325, leaseEndInDays: 40, notes: "Often pays a few days late — a reminder usually does it." },
  { name: "Sophie Albers", profession: "Esthetician", business: "Glow Skin Studio", phone: "763-555-3002", email: "sophie@email.com", suite: "Suite 2", rent: 550, status: "active", leaseStartDaysAgo: 245, leaseEndInDays: 120, notes: "Quiet, reliable. Interested in a larger suite when one opens." },
  { name: "Chloe Bennett", profession: "Spray Tan", business: "Sunlit Glow", phone: "952-555-3003", email: "chloe@email.com", suite: "Suite 3", rent: 550, status: "active", leaseStartDaysAgo: 180, leaseEndInDays: 185, notes: "" },
  { name: "Maya Johnson", profession: "Brow & Makeup", business: "Maya Beauty", phone: "612-555-3004", email: "maya@email.com", suite: "Suite 5", rent: 650, status: "notice", leaseStartDaysAgo: 335, leaseEndInDays: 30, notes: "Gave notice — relocating out of state. Suite 5 free at month end." },
  { name: "Kristen Mitchell", profession: "Lash Artist", business: "Lashes by Kristen", phone: "763-555-3005", email: "kristen@email.com", suite: "Suite 6", rent: 650, status: "active", leaseStartDaysAgo: 400, leaseEndInDays: 250, notes: "Longtime tenant, fully booked. Great referral source." },
  { name: "Priya Patel", profession: "Microblading", business: "Brow Artistry", phone: "952-555-3006", email: "priya@email.com", suite: "Suite 7", rent: 650, status: "active", leaseStartDaysAgo: 150, leaseEndInDays: 205, notes: "" },
  { name: "Tara Nguyen", profession: "Hair Stylist", business: "Tara Hair Co.", phone: "612-555-3007", email: "tara@email.com", suite: "Suite 9", rent: 750, status: "active", leaseStartDaysAgo: 290, leaseEndInDays: 300, notes: "Has the corner suite — uses the extra space for color." },
  { name: "Gabriela Santos", profession: "Massage Therapist", business: "Restore Massage", phone: "763-555-3008", email: "gaby@email.com", suite: "Suite 10", rent: 750, status: "active", leaseStartDaysAgo: 310, leaseEndInDays: 55, notes: "Wants to discuss adding a second treatment room." },
  { name: "Hailey Brooks", profession: "Hair Stylist", business: "Brooks Blowouts", phone: "952-555-3009", email: "hailey@email.com", suite: "Suite 11", rent: 750, status: "active", leaseStartDaysAgo: 95, leaseEndInDays: 270, notes: "Newer tenant, building her book." },
];

const APPLICANT_SEED = [
  { name: "Jasmine Lee", profession: "Nail Tech", phone: "612-555-4001", email: "jasmine@email.com", interest: "Suite 4", status: "new", addedDaysAgo: 2, notes: "Found us on Instagram. Wants a small suite." },
  { name: "Olivia Park", profession: "Esthetician", phone: "763-555-4002", email: "olivia@email.com", interest: "Suite 8", status: "toured", addedDaysAgo: 8, notes: "Toured last week — liked Suite 8. Following up on price." },
  { name: "Mia Carter", profession: "Lash Artist", phone: "952-555-4003", email: "mia@email.com", interest: "Any medium suite", status: "applied", addedDaysAgo: 12, notes: "Application in. Needs space by next month." },
  { name: "Brooke Daniels", profession: "Hair Stylist", phone: "612-555-4004", email: "brooke@email.com", interest: "Suite 12", status: "new", addedDaysAgo: 1, notes: "Referred by Tara." },
];

const MAINT_SEED = [
  { suite: "Suite 9", title: "Leaky sink faucet", reportedBy: "Tara Nguyen", priority: "high", status: "open", createdDaysAgo: 2 },
  { suite: "Suite 6", title: "Flickering outlet by ring light", reportedBy: "Kristen Mitchell", priority: "normal", status: "in-progress", createdDaysAgo: 5 },
  { suite: "Suite 2", title: "AC vent rattling", reportedBy: "Sophie Albers", priority: "low", status: "open", createdDaysAgo: 9 },
  { suite: "Suite 11", title: "Sticky door lock", reportedBy: "Hailey Brooks", priority: "normal", status: "done", createdDaysAgo: 20 },
];

export const DEFAULT_SETTINGS = {
  ownerName: "Renee",
  businessName: "Bloom Beauty Suites",
  location: "Maple Grove, MN",
  address: "9325 Upland Ln N, Maple Grove",
  rentDueDay: 1, // rent is due on the 1st of each month
  lateGraceDays: 5, // days after due date before rent is "late"
  leaseRenewalWindowDays: 60, // start renewal outreach this far ahead
  monthlyExpenses: { mortgage: 4200, utilities: 680, insurance: 240, cleaning: 320, internet: 140, other: 200 },
};

function buildTenants() {
  return TENANT_SEED.map((t, i) => {
    const { leaseStartDaysAgo, leaseEndInDays, ...rest } = t;
    return {
      ...rest,
      id: i + 1,
      deposit: t.rent,
      leaseStart: addDays(todayISO(), -leaseStartDaysAgo),
      leaseEnd: addDays(todayISO(), leaseEndInDays),
      moveIn: addDays(todayISO(), -leaseStartDaysAgo),
    };
  });
}

function buildSuites(tenants) {
  return SUITE_SEED.map((s, i) => {
    const tenant = s.tenant ? tenants.find((t) => t.name === s.tenant) : null;
    return {
      id: i + 1,
      name: s.name,
      size: s.size,
      rent: s.rent,
      tenantId: tenant ? tenant.id : null,
      notes: "",
    };
  });
}

// Rent ledger: one row per active/notice tenant per month for the last 3 months
// plus the current month. Past months are paid; the current month has a few
// unpaid so the demo shows overdue rent to collect.
function buildLedger(tenants) {
  const rows = [];
  const cur = monthKey();
  const months = [addMonths(cur, -3), addMonths(cur, -2), addMonths(cur, -1), cur];
  const unpaidThisMonth = new Set(["Bianca Flores", "Sophie Albers", "Hailey Brooks"]);
  let id = 1;
  tenants
    .filter((t) => t.status !== "past")
    .forEach((t) => {
      months.forEach((mk) => {
        const isCurrent = mk === cur;
        const unpaid = isCurrent && unpaidThisMonth.has(t.name);
        rows.push({
          id: id++,
          tenantId: t.id,
          month: mk,
          amount: t.rent,
          dueDate: `${mk}-01`,
          paidDate: unpaid ? null : isCurrent ? `${mk}-03` : `${mk}-02`,
        });
      });
    });
  return rows;
}

function buildApplicants() {
  return APPLICANT_SEED.map((a, i) => {
    const { addedDaysAgo, ...rest } = a;
    return { ...rest, id: i + 1, added: addDays(todayISO(), -addedDaysAgo) };
  });
}

function buildMaintenance(tenants, suites) {
  return MAINT_SEED.map((m, i) => {
    const { createdDaysAgo, suite, reportedBy, ...rest } = m;
    const su = suites.find((s) => s.name === suite);
    const te = tenants.find((t) => t.name === reportedBy);
    return {
      ...rest,
      id: i + 1,
      suiteId: su ? su.id : null,
      tenantId: te ? te.id : null,
      created: addDays(todayISO(), -createdDaysAgo),
    };
  });
}

export function buildSeedData() {
  const tenants = buildTenants();
  const suites = buildSuites(tenants);
  return {
    version: 1,
    seededAt: todayISO(),
    suites,
    tenants,
    ledger: buildLedger(tenants),
    applicants: buildApplicants(),
    maintenance: buildMaintenance(tenants, suites),
    settings: DEFAULT_SETTINGS,
  };
}
