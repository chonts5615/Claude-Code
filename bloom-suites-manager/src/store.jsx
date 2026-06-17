// Central data store: loads/saves to localStorage automatically and exposes
// every mutation as a named action. Components never touch storage directly.
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import { buildSeedData } from "./seed";
import { todayISO, monthKey, addDays } from "./format";

const STORAGE_KEY = "bloom-suites.v1";
const BloomContext = createContext(null);

const nextId = (list) => (list.length ? Math.max(...list.map((x) => x.id)) + 1 : 1);

function loadData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && Array.isArray(parsed.suites) && Array.isArray(parsed.tenants)) return parsed;
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

export function BloomProvider({ children }) {
  const [data, setData] = useState(loadData);
  const [toast, setToast] = useState(null);
  const toastTimer = useRef(null);

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
      // --- Rent ---
      markRentPaid(rowId) {
        update((d) => ({ ledger: d.ledger.map((r) => (r.id === rowId ? { ...r, paidDate: todayISO() } : r)) }));
        notify("Rent recorded");
      },
      markRentUnpaid(rowId) {
        update((d) => ({ ledger: d.ledger.map((r) => (r.id === rowId ? { ...r, paidDate: null } : r)) }));
      },
      // Create rent rows for any active/notice tenant not yet billed for a month.
      generateRentForMonth(mk = monthKey()) {
        let added = 0;
        setData((d) => {
          const existing = new Set(d.ledger.filter((r) => r.month === mk).map((r) => r.tenantId));
          const newRows = d.tenants
            .filter((t) => t.status !== "past" && !existing.has(t.id))
            .map((t, i) => ({ id: nextId(d.ledger) + i, tenantId: t.id, month: mk, amount: t.rent, dueDate: `${mk}-01`, paidDate: null }));
          added = newRows.length;
          return { ...d, ledger: [...d.ledger, ...newRows] };
        });
        notify(added ? `Billed ${added} tenant${added === 1 ? "" : "s"}` : "Already billed");
      },

      // --- Tenants ---
      addTenant(form) {
        const suite = data.suites.find((s) => s.id === Number(form.suiteId));
        const created = {
          id: nextId(data.tenants),
          name: form.name.trim(),
          business: form.business || "",
          profession: form.profession || "Lash Artist",
          phone: form.phone.trim(),
          email: (form.email || "").trim(),
          suite: suite ? suite.name : "",
          rent: suite ? suite.rent : Number(form.rent) || 0,
          deposit: suite ? suite.rent : Number(form.rent) || 0,
          status: "active",
          leaseStart: todayISO(),
          leaseEnd: addDays(todayISO(), 365),
          moveIn: todayISO(),
          notes: form.notes || "",
        };
        setData((d) => ({
          ...d,
          tenants: [...d.tenants, created],
          suites: d.suites.map((s) => (s.id === Number(form.suiteId) ? { ...s, tenantId: created.id } : s)),
          // Bill the current month right away so rent shows as due.
          ledger: [...d.ledger, { id: nextId(d.ledger), tenantId: created.id, month: monthKey(), amount: created.rent, dueDate: `${monthKey()}-01`, paidDate: null }],
        }));
        notify(`${created.name.split(" ")[0]} added`);
        return created;
      },
      updateTenant(id, patch) {
        update((d) => ({ tenants: d.tenants.map((t) => (t.id === id ? { ...t, ...patch } : t)) }));
      },
      giveNotice(id) {
        update((d) => ({ tenants: d.tenants.map((t) => (t.id === id ? { ...t, status: "notice" } : t)) }));
        notify("Marked as moving out");
      },
      renewLease(id, days = 365) {
        update((d) => ({
          tenants: d.tenants.map((t) => (t.id === id ? { ...t, status: "active", leaseEnd: addDays(t.leaseEnd >= todayISO() ? t.leaseEnd : todayISO(), days) } : t)),
        }));
        notify("Lease renewed");
      },
      endTenancy(id) {
        update((d) => ({
          tenants: d.tenants.map((t) => (t.id === id ? { ...t, status: "past" } : t)),
          suites: d.suites.map((s) => (s.tenantId === id ? { ...s, tenantId: null } : s)),
        }));
        notify("Suite is now vacant");
      },

      // --- Suites ---
      updateSuite(id, patch) {
        update((d) => ({ suites: d.suites.map((s) => (s.id === id ? { ...s, ...patch } : s)) }));
      },

      // --- Maintenance ---
      addMaintenance(form) {
        update((d) => ({
          maintenance: [
            ...d.maintenance,
            {
              id: nextId(d.maintenance),
              suiteId: Number(form.suiteId) || null,
              tenantId: null,
              title: form.title.trim(),
              priority: form.priority || "normal",
              status: "open",
              created: todayISO(),
            },
          ],
        }));
        notify("Request logged");
      },
      setMaintenanceStatus(id, status) {
        update((d) => ({ maintenance: d.maintenance.map((m) => (m.id === id ? { ...m, status } : m)) }));
      },

      // --- Applicants ---
      addApplicant(form) {
        update((d) => ({
          applicants: [
            ...d.applicants,
            {
              id: nextId(d.applicants),
              name: form.name.trim(),
              profession: form.profession || "Lash Artist",
              phone: form.phone.trim(),
              email: (form.email || "").trim(),
              interest: form.interest || "Any suite",
              status: "new",
              added: todayISO(),
              notes: form.notes || "",
            },
          ],
        }));
        notify("Applicant added");
      },
      setApplicantStatus(id, status) {
        update((d) => ({ applicants: d.applicants.map((a) => (a.id === id ? { ...a, status } : a)) }));
      },
      removeApplicant(id) {
        update((d) => ({ applicants: d.applicants.filter((a) => a.id !== id) }));
      },

      // --- Settings ---
      updateSettings(patch) {
        update((d) => ({ settings: { ...d.settings, ...patch } }));
      },

      // --- Data safety ---
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
          a.download = `bloom-suites-backup-${todayISO()}.json`;
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
        if (!parsed || !Array.isArray(parsed.suites) || !Array.isArray(parsed.tenants)) {
          throw new Error("That file doesn't look like a Bloom Suites backup.");
        }
        setData(parsed);
        notify("Backup restored");
      },
      resetToSample() {
        setData(buildSeedData());
        notify("Reset to sample data");
      },
      // Keep the owner's own suites (rents/names/notes) and settings; just empty
      // the demo tenants/rent/applicants/maintenance and free every suite.
      clearAll() {
        setData((d) => ({
          ...d,
          suites: d.suites.map((s) => ({ ...s, tenantId: null })),
          tenants: [],
          ledger: [],
          applicants: [],
          maintenance: [],
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
