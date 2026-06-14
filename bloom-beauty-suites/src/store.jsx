// Central data store: loads/saves to localStorage automatically and exposes
// every mutation as a named action. Components never touch storage directly.
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import { buildSeedData, SERVICES } from "./seed";
import { todayISO, addDays } from "./format";

const STORAGE_KEY = "bloom.v1";
const BloomContext = createContext(null);

const nextId = (list) => (list.length ? Math.max(...list.map((x) => x.id)) + 1 : 1);

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
        const svc = data.services.find((s) => s.id === serviceId) || SERVICES.find((s) => s.id === serviceId);
        const created = {
          id: nextId(data.appointments),
          clientId,
          clientName: client ? client.name : "Walk-in",
          date,
          time,
          serviceId,
          serviceName: svc ? svc.name : serviceId,
          price: svc ? svc.price : 0,
          duration: svc ? svc.duration : 60,
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

      // Rebook a client at their usual cadence. `fromApptId` marks the source
      // completed appointment as rebooked so the rebook-rate metric updates.
      rebookClient(clientId, { serviceId, fromApptId } = {}) {
        const client = data.clients.find((c) => c.id === clientId);
        if (!client) return null;
        const interval = client.avgInterval || 21;
        // Schedule from whichever is later: their cadence from last visit, or today.
        const fromLast = addDays(client.lastVisit, interval);
        const date = fromLast > todayISO() ? fromLast : addDays(todayISO(), interval);
        const svcId =
          serviceId || data.appointments.find((a) => a.clientId === clientId)?.serviceId || "classic-fill";
        const svc = data.services.find((s) => s.id === svcId) || SERVICES.find((s) => s.id === svcId);
        const created = {
          id: nextId(data.appointments),
          clientId,
          clientName: client.name,
          date,
          time: "10:00",
          serviceId: svcId,
          serviceName: svc ? svc.name : svcId,
          price: svc ? svc.price : 0,
          duration: svc ? svc.duration : 60,
          status: "scheduled",
          notes: "",
          rebooked: false,
        };
        setData((d) => ({
          ...d,
          appointments: [
            ...d.appointments.map((a) => (a.id === fromApptId ? { ...a, rebooked: true } : a)),
            created,
          ],
        }));
        notify(`Rebooked for ${created.date}`);
        return created;
      },

      // --- Inventory ---
      adjustInventory(id, delta) {
        update((d) => ({
          inventory: d.inventory.map((i) =>
            i.id === id ? { ...i, qty: Math.max(0, i.qty + delta) } : i
          ),
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

      // --- Settings ---
      updateSettings(patch) {
        update((d) => ({ settings: { ...d.settings, ...patch } }));
      },

      // --- Data safety: backup / restore / reset ---
      exportData() {
        return JSON.stringify(data, null, 2);
      },
      importData(json) {
        const parsed = JSON.parse(json);
        if (!parsed || !Array.isArray(parsed.clients) || !Array.isArray(parsed.appointments)) {
          throw new Error("That file doesn't look like a Bloom backup.");
        }
        setData(parsed);
        notify("Backup restored");
      },
      resetToSample() {
        setData(buildSeedData());
        notify("Reset to sample data");
      },
      clearAll() {
        const seed = buildSeedData();
        setData({
          ...seed,
          clients: [],
          appointments: [],
          waitlist: [],
        });
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
