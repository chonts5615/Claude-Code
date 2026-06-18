// Sample data used to seed a brand-new install so the owner can explore a
// populated app before entering real data. All dates are generated RELATIVE to
// today, so the demo always shows a current, realistic week.
import { todayISO, addDays, toISO } from "./format.js";

export const SERVICES = [
  { id: "classic-full", name: "Classic Full Set", price: 165, duration: 120, category: "Full Set" },
  { id: "hybrid-full", name: "Hybrid Full Set", price: 195, duration: 135, category: "Full Set" },
  { id: "volume-full", name: "Volume Full Set", price: 225, duration: 150, category: "Full Set" },
  { id: "classic-fill", name: "Classic Fill (2wk)", price: 75, duration: 60, category: "Fill" },
  { id: "classic-fill-3", name: "Classic Fill (3wk)", price: 90, duration: 75, category: "Fill" },
  { id: "hybrid-fill", name: "Hybrid Fill (2wk)", price: 95, duration: 75, category: "Fill" },
  { id: "volume-fill", name: "Volume Fill (2wk)", price: 110, duration: 90, category: "Fill" },
  { id: "volume-fill-3", name: "Volume Fill (3wk)", price: 125, duration: 90, category: "Fill" },
  { id: "removal", name: "Lash Removal", price: 35, duration: 30, category: "Other" },
  { id: "lash-lift", name: "Lash Lift & Tint", price: 85, duration: 60, category: "Other" },
  { id: "brow-lam", name: "Brow Lamination", price: 75, duration: 45, category: "Other" },
];

// Client profiles. `lastVisitDaysAgo` is converted to a real date at seed time
// so the computed health status (active / lapsing / lost) stays realistic.
const CLIENT_SEED = [
  { name: "Sarah Mitchell", phone: "612-555-0101", email: "sarah.m@email.com", firstVisit: "2024-03-15", curl: "C", length: "11-13mm", diameter: "0.07mm", style: "Cat Eye", allergies: "None", notes: "Prefers dramatic outer corners. Contact lens wearer.", visits: 28, ltv: 2380, avgInterval: 17, lastVisitDaysAgo: 4 },
  { name: "Jessica Park", phone: "763-555-0202", email: "jpark@email.com", firstVisit: "2024-06-01", curl: "D", length: "12-14mm", diameter: "0.05mm", style: "Volume", allergies: "Sensitive to latex tape", notes: "Use micropore tape only. Gets volume fills every 2 weeks religiously.", visits: 42, ltv: 4620, avgInterval: 14, lastVisitDaysAgo: 6 },
  { name: "Amanda Chen", phone: "952-555-0303", email: "achen@email.com", firstVisit: "2025-01-10", curl: "C", length: "10-12mm", diameter: "0.07mm", style: "Natural", allergies: "None", notes: "Conservative style. First-time lash client, now a regular.", visits: 22, ltv: 1760, avgInterval: 18, lastVisitDaysAgo: 9 },
  { name: "Rachel Torres", phone: "612-555-0404", email: "rtorres@email.com", firstVisit: "2024-09-20", curl: "B", length: "9-11mm", diameter: "0.10mm", style: "Natural", allergies: "None", notes: "Prefers very subtle look. Works in corporate finance.", visits: 18, ltv: 1440, avgInterval: 21, lastVisitDaysAgo: 2 },
  { name: "Emily Larson", phone: "763-555-0505", email: "elarson@email.com", firstVisit: "2023-11-01", curl: "D", length: "13-15mm", diameter: "0.05mm", style: "Wispy", allergies: "Sensitive to cyanoacrylate fumes", notes: "Use low-fume adhesive ONLY. Nano mister after application. Longest-standing client.", visits: 52, ltv: 5460, avgInterval: 15, lastVisitDaysAgo: 7 },
  { name: "Megan O'Brien", phone: "612-555-0606", email: "mobrien@email.com", firstVisit: "2025-03-01", curl: "C", length: "11-13mm", diameter: "0.07mm", style: "Hybrid", allergies: "None", notes: "Bridal party in September. Wants trial run in August.", visits: 16, ltv: 1520, avgInterval: 19, lastVisitDaysAgo: 13 },
  { name: "Taylor Nguyen", phone: "952-555-0707", email: "tnguyen@email.com", firstVisit: "2024-12-15", curl: "L", length: "10-12mm", diameter: "0.07mm", style: "Doll Eye", allergies: "None", notes: "Hooded lids — use L curl for lift. Great retention.", visits: 20, ltv: 1900, avgInterval: 18, lastVisitDaysAgo: 15 },
  { name: "Brittany Kowalski", phone: "763-555-0808", email: "bkow@email.com", firstVisit: "2025-06-15", curl: "C", length: "12-14mm", diameter: "0.05mm", style: "Volume", allergies: "None", notes: "Instagram referral. Always posts her lashes — great for social proof.", visits: 14, ltv: 1540, avgInterval: 16, lastVisitDaysAgo: 3 },
  { name: "Lauren Schmidt", phone: "612-555-0909", email: "lschmidt@email.com", firstVisit: "2024-07-01", curl: "C", length: "11-13mm", diameter: "0.07mm", style: "Cat Eye", allergies: "Eye drops for glaucoma", notes: "Check medication list each visit. Very loyal.", visits: 25, ltv: 2125, avgInterval: 20, lastVisitDaysAgo: 17 },
  { name: "Hannah Patel", phone: "952-555-1010", email: "hpatel@email.com", firstVisit: "2025-08-01", curl: "D", length: "12-14mm", diameter: "0.05mm", style: "Wispy Volume", allergies: "None", notes: "Referred by Jessica Park. Wants same dramatic look.", visits: 10, ltv: 1100, avgInterval: 15, lastVisitDaysAgo: 5 },
  { name: "Danielle Olson", phone: "763-555-1111", email: "dolson@email.com", firstVisit: "2025-02-14", curl: "C", length: "10-12mm", diameter: "0.10mm", style: "Natural", allergies: "None", notes: "Valentine's Day gift from husband. Has become a regular.", visits: 15, ltv: 1200, avgInterval: 22, lastVisitDaysAgo: 20 },
  { name: "Kendra Williams", phone: "612-555-1212", email: "kwill@email.com", firstVisit: "2024-04-01", curl: "C", length: "11-13mm", diameter: "0.07mm", style: "Hybrid", allergies: "None", notes: "Teacher — seasonal client. Heavy summer, light during school year.", visits: 12, ltv: 1140, avgInterval: 35, lastVisitDaysAgo: 48 },
  { name: "Courtney Johansson", phone: "763-555-1313", email: "cjoh@email.com", firstVisit: "2025-09-01", curl: "B", length: "9-11mm", diameter: "0.10mm", style: "Natural", allergies: "Sensitivity to black adhesive", notes: "Use clear adhesive. Very sensitive eyes — go slow.", visits: 6, ltv: 510, avgInterval: 40, lastVisitDaysAgo: 70 },
  { name: "Michelle Park-Davis", phone: "952-555-1414", email: "mpd@email.com", firstVisit: "2024-11-01", curl: "D", length: "13-15mm", diameter: "0.05mm", style: "Mega Volume", allergies: "None", notes: "Influencer — posts tagged content. Comp'd services quarterly for content.", visits: 19, ltv: 1425, avgInterval: 18, lastVisitDaysAgo: 11 },
  { name: "Alexis Rivera", phone: "612-555-1515", email: "arivera@email.com", firstVisit: "2025-11-15", curl: "C", length: "10-12mm", diameter: "0.07mm", style: "Cat Eye", allergies: "None", notes: "New client. Moved from Chicago — was paying $200/fill there.", visits: 8, ltv: 720, avgInterval: 16, lastVisitDaysAgo: 8 },
  { name: "Nicole Bergstrom", phone: "763-555-1616", email: "nberg@email.com", firstVisit: "2024-08-01", curl: "C", length: "11-13mm", diameter: "0.07mm", style: "Wispy", allergies: "None", notes: "Comes with her daughter sometimes. Potential family package.", visits: 9, ltv: 765, avgInterval: 45, lastVisitDaysAgo: 165 },
];

const INVENTORY_SEED = [
  { name: "Classic Lash Tray — C Curl 0.15", category: "Lash Trays", qty: 8, reorder: 3, cost: 12.99, supplier: "BL Lashes", expiresIn: 290, orderedDaysAgo: 44 },
  { name: "Classic Lash Tray — D Curl 0.15", category: "Lash Trays", qty: 6, reorder: 3, cost: 12.99, supplier: "BL Lashes", expiresIn: 290, orderedDaysAgo: 44 },
  { name: "Volume Lash Tray — C Curl 0.05", category: "Lash Trays", qty: 5, reorder: 3, cost: 14.99, supplier: "BL Lashes", expiresIn: 290, orderedDaysAgo: 44 },
  { name: "Volume Lash Tray — D Curl 0.05", category: "Lash Trays", qty: 4, reorder: 3, cost: 14.99, supplier: "BL Lashes", expiresIn: 290, orderedDaysAgo: 44 },
  { name: "Volume Lash Tray — L Curl 0.07", category: "Lash Trays", qty: 2, reorder: 2, cost: 15.99, supplier: "BL Lashes", expiresIn: 290, orderedDaysAgo: 60 },
  { name: "Stacy Lash Adhesive — Extra Strong", category: "Adhesive", qty: 3, reorder: 2, cost: 22.99, supplier: "Amazon", expiresIn: 31, orderedDaysAgo: 13 },
  { name: "Low-Fume Adhesive (sensitive clients)", category: "Adhesive", qty: 1, reorder: 2, cost: 24.99, supplier: "Amazon", expiresIn: 17, orderedDaysAgo: 25 },
  { name: "Clear Adhesive (allergy clients)", category: "Adhesive", qty: 1, reorder: 1, cost: 19.99, supplier: "BL Lashes", expiresIn: 48, orderedDaysAgo: 30 },
  { name: "Gel Eye Pads (box/50)", category: "Consumables", qty: 35, reorder: 20, cost: 8.99, supplier: "Amazon", expiresIn: null, orderedDaysAgo: 44 },
  { name: "Micro Brushes (bag/100)", category: "Consumables", qty: 180, reorder: 50, cost: 4.99, supplier: "Amazon", expiresIn: null, orderedDaysAgo: 74 },
  { name: "Lash Primer", category: "Solutions", qty: 2, reorder: 1, cost: 15.99, supplier: "BL Lashes", expiresIn: 170, orderedDaysAgo: 60 },
  { name: "Lash Sealant/Coating", category: "Solutions", qty: 2, reorder: 1, cost: 17.99, supplier: "BL Lashes", expiresIn: 170, orderedDaysAgo: 60 },
  { name: "Isolation Tweezers (pair)", category: "Tools", qty: 4, reorder: 2, cost: 18.99, supplier: "Lash Box LA", expiresIn: null, orderedDaysAgo: 150 },
  { name: "Volume Tweezers (pair)", category: "Tools", qty: 3, reorder: 2, cost: 24.99, supplier: "Lash Box LA", expiresIn: null, orderedDaysAgo: 150 },
  { name: "Adhesive Remover — Cream", category: "Solutions", qty: 2, reorder: 1, cost: 13.99, supplier: "BL Lashes", expiresIn: 200, orderedDaysAgo: 105 },
  { name: "Nano Mister", category: "Tools", qty: 1, reorder: 1, cost: 12.99, supplier: "Amazon", expiresIn: null, orderedDaysAgo: 225 },
];

const WAITLIST_SEED = [
  { name: "Christina Meyers", phone: "612-555-2001", service: "Volume Full Set", preferred: "Weekday mornings", addedDaysAgo: 4, status: "waiting" },
  { name: "Ashley Kim", phone: "763-555-2002", service: "Hybrid Full Set", preferred: "Sat or Fri afternoon", addedDaysAgo: 6, status: "waiting" },
  { name: "Jordan Blake", phone: "952-555-2003", service: "Classic Full Set", preferred: "Any weekday", addedDaysAgo: 9, status: "contacted" },
];

function buildClients() {
  return CLIENT_SEED.map((c, i) => {
    const { lastVisitDaysAgo, ...rest } = c;
    return { ...rest, id: i + 1, lastVisit: addDays(todayISO(), -lastVisitDaysAgo) };
  });
}

function buildInventory() {
  return INVENTORY_SEED.map((it, i) => {
    const { expiresIn, orderedDaysAgo, ...rest } = it;
    return {
      ...rest,
      id: i + 1,
      expires: expiresIn == null ? null : addDays(todayISO(), expiresIn),
      lastOrdered: addDays(todayISO(), -orderedDaysAgo),
      onOrder: false,
    };
  });
}

function buildWaitlist() {
  return WAITLIST_SEED.map((w, i) => {
    const { addedDaysAgo, ...rest } = w;
    return { ...rest, id: i + 1, added: addDays(todayISO(), -addedDaysAgo) };
  });
}

// Generate a believable appointment history (past 8 weeks) plus the coming
// week, anchored to today. `clients` is the already-built client list.
function buildAppointments(clients) {
  const appts = [];
  const outcomes = ["completed", "completed", "completed", "completed", "completed", "completed", "completed", "completed", "no-show", "late-cancel"];
  const serviceIds = ["classic-fill", "classic-fill", "classic-fill-3", "hybrid-fill", "volume-fill", "volume-fill", "volume-fill-3", "classic-full", "hybrid-full", "volume-full", "removal", "lash-lift"];
  const active = clients.filter((c) => c.lastVisit >= addDays(todayISO(), -120));
  const base = new Date(todayISO() + "T12:00:00");
  // Most recent past Saturday — used as the right edge of history.
  const lastSat = new Date(base);
  lastSat.setDate(base.getDate() - ((base.getDay() + 1) % 7));
  let id = 1;
  const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];

  for (let w = 7; w >= 0; w--) {
    const count = 15 + Math.floor(Math.random() * 6);
    for (let a = 0; a < count; a++) {
      const day = Math.floor(Math.random() * 5);
      const hour = 9 + Math.floor(Math.random() * 8);
      const d = new Date(lastSat);
      d.setDate(lastSat.getDate() - w * 7 - day);
      const client = pick(active);
      const sid = pick(serviceIds);
      const svc = SERVICES.find((s) => s.id === sid);
      const status = pick(outcomes);
      appts.push({
        id: id++,
        clientId: client.id,
        clientName: client.name,
        date: toISO(d),
        time: `${String(hour).padStart(2, "0")}:${Math.random() > 0.5 ? "00" : "30"}`,
        serviceId: svc.id,
        serviceName: svc.name,
        price: svc.price + (Math.random() > 0.7 ? Math.floor(Math.random() * 20) : 0),
        duration: svc.duration,
        status,
        notes: "",
        rebooked: status === "completed" ? Math.random() > 0.25 : false,
      });
    }
  }
  // Upcoming week (next 5 business days starting today).
  for (let d = 0; d < 7; d++) {
    const iso = addDays(todayISO(), d);
    const dow = new Date(iso + "T12:00:00").getDay();
    if (dow === 0 || dow === 6) continue;
    const count = 3 + Math.floor(Math.random() * 2);
    for (let a = 0; a < count; a++) {
      const hour = 9 + a * 2;
      const client = pick(active);
      const sid = pick(serviceIds);
      const svc = SERVICES.find((s) => s.id === sid);
      appts.push({
        id: id++,
        clientId: client.id,
        clientName: client.name,
        date: iso,
        time: `${String(hour).padStart(2, "0")}:00`,
        serviceId: svc.id,
        serviceName: svc.name,
        price: svc.price,
        duration: svc.duration,
        status: "scheduled",
        notes: "",
        rebooked: false,
      });
    }
  }
  return appts;
}

export const DEFAULT_SETTINGS = {
  ownerName: "Kristen",
  businessName: "Bloom Beauty Suites",
  location: "Maple Grove, MN",
  address: "9325 Upland Ln N, Maple Grove",
  monthlyExpenses: { rent: 600, supplies: 64, insurance: 14, tech: 199, banking: 16, other: 66 },
  cogsRate: 0.065, // share of revenue spent on product per service
  taxReserveRate: 0.37, // SE + federal + state set-aside
  lapseGraceDays: 10, // days past usual cadence before a client is "due"
  welcomeDismissed: false, // first-run welcome banner
  lastBackup: null, // ISO date of the last data backup (for the reminder)
};

// Build a complete fresh dataset for a new install.
export function buildSeedData() {
  const clients = buildClients();
  return {
    version: 1,
    seededAt: todayISO(),
    services: SERVICES,
    clients,
    appointments: buildAppointments(clients),
    inventory: buildInventory(),
    waitlist: buildWaitlist(),
    settings: DEFAULT_SETTINGS,
  };
}
