// Central data store: loads/saves to localStorage automatically and exposes
// every mutation as a named action. Components never touch storage directly.
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import { buildSeedData, DEFAULT_SETTINGS } from "./seed";
import { todayISO, addDays } from "./format";

const STORAGE_KEY = "bloom.v1";
const BloomContext = createContext(null);

const nextId = (list) => (list.length ? Math.max(...list.map((x) => x.id)) + 1 : 1);

// First start time (09:00–18:00, 30-min steps) on `date` that doesn't overlap an
// existing scheduled/completed appointment for the given duration. Returns null
// if the whole day is booked, so callers can pick another day instead of
// silently double-booking.
const toMin = (t) => {
  const [h, m] = t.split(":").map(Number);
  return h * 60 + m;
};
function firstFreeTime(appointments, date, duration) {
  const sameDay = appointments.filter((a) => a.date === date && (a.status === "scheduled" || a.status === "completed"));
  const overlaps = (start) => sameDay.some((a) => start < toMin(a.time) + a.duration && toMin(a.time) < start + duration);
  for (let mins = 9 * 60; mins <= 18 * 60; mins += 30) {
    if (!overlaps(mins)) return `${String(Math.floor(mins / 60)).padStart(2, "0")}:${mins % 60 === 0 ? "00" : "30"}`;
  }
  return null;
}

function loadData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && Array.isArray(parsed.clients) && Array.isArray(parsed.appointments)) {
        return parsed;
      }
    }
  } catch {
    /* fall through to seed */
  }
  const seed = buildSeedData();
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(seed));
  } catch {
    /* storage may be unavailable; app still works in-memory */
  }
  return seed;
}

// Average gap (days) between a client's completed visits — used to keep each
// client's cadence current as new visits are logged.
function recomputeInterval(clientId, appointments, fallback) {
  const dates = appointments
    .filter((a) => a.clientId === clientId && a.status === "completed")
    .map((a) => a.date)
    .sort();
  if (dates.length < 2) return fallback;
  let total = 0;
  for (let i = 1; i < dates.length; i++) {
    total += (new Date(dates[i]) - new Date(dates[i - 1])) / 86400000;
  }
  return Math.max(7, Math.round(total / (dates.length - 1)));
}

export function BloomProvider({ children }) {
  const [data, setData] = useState(loadData);
  const [toast, setToast] = useState(null);
  const toastTimer = useRef(null);

  // Auto-save on every change. This is what removes "remembering to save".
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch {
      /* ignore quota/availability errors */
    }
  }, [data]);

  const notify = useCallback((message) => {
    setToast({ message, id: Date.now() });
    clearTimeout(toastTimer.current);
    toastTimer.current = setTimeout(() => setToast(null), 2600);
  }, []);

  const actions = useMemo(() => {
    const update = (fn) => setData((d) => ({ ...d, ...fn(d) }));

    return {
      // --- Clients ---
      addClient(form) {
        const created = {
          id: nextId(data.clients),
          name: form.name.trim(),
          phone: form.phone.trim(),
          email: (form.email || "").trim(),
          curl: form.curl || "C",
          style: form.style || "Natural",
          length: form.length || "TBD",
          diameter: form.diameter || "TBD",
          allergies: form.allergies || "None",
          notes: form.notes || "",
          firstVisit: todayISO(),
          lastVisit: todayISO(),
          visits: 0,
          ltv: 0,
          avgInterval: 21,
        };
        setData((d) => ({ ...d, clients: [...d.clients, created] }));
        notify(`${created.name.split(" ")[0]} added`);
        return created;
      },
      updateClient(id, patch) {
        update((d) => ({ clients: d.clients.map((c) => (c.id === id ? { ...c, ...patch } : c)) }));
      },

      // --- Appointments ---
      bookAppointment({ clientId, date, time, serviceId, notes = "" }) {
        const client = data.clients.find((c) => c.id === clientId);
        // Only book a service that's actually on the current menu.
        const svc = data.services.find((s) => s.id === serviceId);
        if (!svc) {
          notify("Pick a service first");
          return null;
        }
        const created = {
          id: nextId(data.appointments),
          clientId,
          clientName: client ? client.name : "Walk-in",
          date,
          time,
          serviceId,
          serviceName: svc.name,
          price: svc.price,
          duration: svc.duration,
          status: "scheduled",
          notes,
          rebooked: false,
        };
        setData((d) => ({ ...d, appointments: [...d.appointments, created] }));
        notify("Appointment booked");
        return created;
      },

      // Logging a visit complete also updates the client's stats automatically.
      completeAppointment(id) {
        update((d) => {
          const appt = d.appointments.find((a) => a.id === id);
          if (!appt || appt.status === "completed") return {};
          // Don't log a visit that hasn't happened yet (guards stray calls).
          if (appt.date > todayISO()) return {};
          const appointments = d.appointments.map((a) =>
            a.id === id ? { ...a, status: "completed" } : a
          );
          const clients = d.clients.map((c) => {
            if (c.id !== appt.clientId) return c;
            return {
              ...c,
              visits: (c.visits || 0) + 1,
              ltv: (c.ltv || 0) + appt.price,
              lastVisit: appt.date > c.lastVisit ? appt.date : c.lastVisit,
              avgInterval: recomputeInterval(c.id, appointments, c.avgInterval),
            };
          });
          return { appointments, clients };
        });
        notify("Visit logged");
      },

      setAppointmentStatus(id, status) {
        update((d) => ({
          appointments: d.appointments.map((a) => (a.id === id ? { ...a, status } : a)),
        }));
      },

      deleteAppointment(id) {
        update((d) => ({ appointments: d.appointments.filter((a) => a.id !== id) }));
        notify("Appointment removed");
      },

      // Rebook a client at their usual cadence. The source completed appointment
      // (passed in, or the client's most recent visit) is marked rebooked so the
      // rebook-rate metric updates, and its service is used by default.
      rebookClient(clientId, { serviceId, fromApptId } = {}) {
        const client = data.clients.find((c) => c.id === clientId);
        if (!client) return null;
        const interval = client.avgInterval || 21;
        // Next visit lands one cadence after the last one — but if that date has
        // already passed (client is due/overdue), book them in the next few days.
        const fromLast = addDays(client.lastVisit, interval);
        const date = fromLast > todayISO() ? fromLast : addDays(todayISO(), 3);
        // Most recent completed visit drives the default service and rebook flag.
        const history = data.appointments
          .filter((a) => a.clientId === clientId)
          .sort((a, b) => `${b.date} ${b.time}`.localeCompare(`${a.date} ${a.time}`));
        const lastVisit = history.find((a) => a.status === "completed");
        const sourceId = fromApptId ?? lastVisit?.id;
        // Default to the client's latest service; if that one's been removed from
        // the menu, fall back to a current service.
        let svcId = serviceId || lastVisit?.serviceId || history[0]?.serviceId;
        if (!data.services.some((s) => s.id === svcId)) svcId = data.services[0]?.id;
        const svc = data.services.find((s) => s.id === svcId);
        if (!svc) {
          notify("Add a service first");
          return null;
        }
        // Find the first day from the target date with an open slot (don't
        // silently double-book a fully booked day).
        let bookDate = date;
        let time = null;
        for (let i = 0; i < 30 && !time; i++) {
          time = firstFreeTime(data.appointments, bookDate, svc.duration);
          if (!time) bookDate = addDays(bookDate, 1);
        }
        if (!time) {
          bookDate = date;
          time = "10:00";
        }
        const created = {
          id: nextId(data.appointments),
          clientId,
          clientName: client.name,
          date: bookDate,
          time,
          serviceId: svc.id,
          serviceName: svc.name,
          price: svc.price,
          duration: svc.duration,
          status: "scheduled",
          notes: "",
          rebooked: false,
        };
        setData((d) => ({
          ...d,
          appointments: [
            ...d.appointments.map((a) => (a.id === sourceId ? { ...a, rebooked: true } : a)),
            created,
          ],
        }));
        notify(`Rebooked for ${created.date}`);
        return created;
      },

      // --- Inventory ---
      addInventoryItem(form) {
        update((d) => ({
          inventory: [
            ...d.inventory,
            {
              id: nextId(d.inventory),
              name: form.name.trim(),
              category: form.category || "Consumables",
              qty: Number(form.qty) || 0,
              reorder: Number(form.reorder) || 1,
              cost: Number(form.cost) || 0,
              supplier: form.supplier || "",
              expires: form.expires || null,
              lastOrdered: todayISO(),
              onOrder: false,
            },
          ],
        }));
        notify("Item added");
      },
      adjustInventory(id, delta) {
        update((d) => ({
          inventory: d.inventory.map((i) => {
            if (i.id !== id) return i;
            const qty = Math.max(0, i.qty + delta);
            // Restocking back above the reorder level clears the "on order" flag.
            return { ...i, qty, onOrder: qty > i.reorder ? false : i.onOrder };
          }),
        }));
      },
      markOrdered(id) {
        update((d) => ({
          inventory: d.inventory.map((i) =>
            i.id === id ? { ...i, onOrder: true, lastOrdered: todayISO() } : i
          ),
        }));
        notify("Marked as ordered");
      },
      receiveStock(id, qty) {
        update((d) => ({
          inventory: d.inventory.map((i) =>
            i.id === id ? { ...i, qty: i.qty + qty, onOrder: false, lastOrdered: todayISO() } : i
          ),
        }));
        notify("Stock received");
      },

      // --- Waitlist ---
      addWaitlist(form) {
        update((d) => ({
          waitlist: [
            ...d.waitlist,
            {
              id: nextId(d.waitlist),
              name: form.name.trim(),
              phone: form.phone.trim(),
              service: form.service,
              preferred: form.preferred || "Any time",
              added: todayISO(),
              status: "waiting",
            },
          ],
        }));
        notify("Added to waitlist");
      },
      setWaitlistStatus(id, status) {
        update((d) => ({
          waitlist: d.waitlist.map((w) => (w.id === id ? { ...w, status } : w)),
        }));
      },
      removeWaitlist(id) {
        update((d) => ({ waitlist: d.waitlist.filter((w) => w.id !== id) }));
      },

      // --- Services (the menu the owner prices and offers) ---
      addService(form) {
        const base = (form.name || "service").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "service";
        update((d) => {
          let id = base;
          let n = 2;
          while (d.services.some((s) => s.id === id)) id = `${base}-${n++}`;
          return {
            services: [
              ...d.services,
              { id, name: form.name.trim(), category: form.category || "Other", price: Number(form.price) || 0, duration: Number(form.duration) || 60 },
            ],
          };
        });
        notify("Service added");
      },
      updateService(id, patch) {
        update((d) => ({ services: d.services.map((s) => (s.id === id ? { ...s, ...patch } : s)) }));
      },
      deleteService(id) {
        update((d) => ({ services: d.services.filter((s) => s.id !== id) }));
        notify("Service removed");
      },

      // --- Settings ---
      updateSettings(patch) {
        update((d) => ({ settings: { ...d.settings, ...patch } }));
      },

      // --- Data safety: backup / restore / reset ---
      exportData() {
        return JSON.stringify(data, null, 2);
      },
      // Download a backup file and record the date (powers the backup reminder).
      backupData() {
        try {
          const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = `bloom-backup-${todayISO()}.json`;
          a.click();
          URL.revokeObjectURL(url);
        } catch {
          /* download may be blocked; still record the attempt below */
        }
        update((d) => ({ settings: { ...d.settings, lastBackup: todayISO() } }));
        notify("Backup downloaded");
      },
      importData(json) {
        const parsed = JSON.parse(json);
        const ok = parsed && ["clients", "appointments", "services", "inventory", "waitlist"].every((k) => Array.isArray(parsed[k]));
        if (!ok) throw new Error("That file doesn't look like a complete Bloom backup.");
        // Merge defaults so an older/partial backup (e.g. empty settings) can't
        // leave required fields undefined and crash the app on render.
        const src = parsed.settings && typeof parsed.settings === "object" ? parsed.settings : {};
        const settings = { ...DEFAULT_SETTINGS, ...src, monthlyExpenses: { ...DEFAULT_SETTINGS.monthlyExpenses, ...(src.monthlyExpenses || {}) } };
        setData({ ...parsed, settings });
        notify("Backup restored");
      },
      resetToSample() {
        setData(buildSeedData());
        notify("Reset to sample data");
      },
      // Keep the owner's own services + settings; clear the demo records and
      // sample inventory so the fresh state has nothing they didn't enter.
      clearAll() {
        setData((d) => ({
          ...d,
          clients: [],
          appointments: [],
          waitlist: [],
          inventory: [],
        }));
        notify("Started fresh");
      },
    };
  }, [data, notify]);

  const value = useMemo(() => ({ data, actions, toast, notify }), [data, actions, toast, notify]);
  return <BloomContext.Provider value={value}>{children}</BloomContext.Provider>;
}

export function useBloom() {
  const ctx = useContext(BloomContext);
  if (!ctx) throw new Error("useBloom must be used inside <BloomProvider>");
  return ctx;
}
