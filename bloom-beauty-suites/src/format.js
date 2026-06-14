// Formatting + date helpers. All "today" logic flows through todayISO() so the
// whole app shares one notion of the current day (and tests/demos stay stable).

export const fmt = (n) =>
  "$" + Math.round(Number(n) || 0).toLocaleString("en-US");

export const fmtD = (n) =>
  "$" +
  (Number(n) || 0).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

// Local-time ISO date (YYYY-MM-DD) — avoids the UTC off-by-one that
// toISOString() causes for users in negative time zones.
export const toISO = (d) => {
  const x = new Date(d);
  return `${x.getFullYear()}-${String(x.getMonth() + 1).padStart(2, "0")}-${String(
    x.getDate()
  ).padStart(2, "0")}`;
};

export const todayISO = () => toISO(new Date());

export const dayName = (iso) => DAYS[new Date(iso + "T12:00:00").getDay()];
export const monthName = (m) => MONTHS[m];

export const addDays = (iso, n) => {
  const d = new Date(iso + "T12:00:00");
  d.setDate(d.getDate() + n);
  return toISO(d);
};

// Whole days from `iso` until today (positive = in the past).
export const daysAgo = (iso, base = todayISO()) =>
  Math.round((new Date(base + "T12:00:00") - new Date(iso + "T12:00:00")) / 86400000);

// Friendly long date, e.g. "Friday, June 13, 2026".
export const longDate = (iso = todayISO()) =>
  new Date(iso + "T12:00:00").toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });

export const initials = (name) =>
  name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
