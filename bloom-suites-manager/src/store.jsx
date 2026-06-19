// Central data store: loads/saves to localStorage automatically and exposes
// every mutation as a named action. Components never touch storage directly.
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import { buildSeedData, DEFAULT_SETTINGS } from "./seed";
import { eligibleToBill } from "./automation";
import { todayISO, monthKey, addDays } from "./format";

const STORAGE_KEY = "bloom-suites.v1";
const BloomContext = createContext(null);

const nextId = (list) => (list.length ? Math.max(...list.map((x) => x.id)) + 1 : 1);

function loadData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && Array.isArray(parsed.suites) && Array.isArray(parsed.tenants)) return normalize(parsed);
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

// Fill any missing arrays/settings so older or partial saved data can't crash
// the app on first render. Same shape that a restore produces.
function normalize(parsed) {
  const s = parsed.settings && typeof parsed.settings === "object" ? parsed.settings : {};
  return {
    version: parsed.version ?? 1,
    suites: Array.isArray(parsed.suites) ? parsed.suites : [],
    tenants: Array.isArray(parsed.tenants) ? parsed.tenants : [],
    ledger: Array.isArray(parsed.ledger) ? parsed.ledger : [],
    applicants: Array.isArray(parsed.applicants) ? parsed.applicants : [],
    maintenance: Array.isArray(parsed.maintenance) ? parsed.maintenance : [],
    settings: { ...DEFAULT_SETTINGS, ...s, monthlyExpenses: { ...DEFAULT_SETTINGS.monthlyExpenses, ...(s.monthlyExpenses || {}) } },
  };
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
      // Add a one-time late fee to an unpaid row (idempotent).
      applyLateFee(rowId) {
        update((d) => ({
          ledger: d.ledger.map((r) =>
            r.id === rowId && !r.paidDate && !r.lateFeeApplied
              ? { ...r, amount: r.amount + (d.settings.lateFeeAmount || 0), lateFee: d.settings.lateFeeAmount || 0, lateFeeApplied: true }
              : r
          ),
        }));
        notify("Late fee added");
      },
      // Create rent rows for any active/notice tenant not yet billed for a month.
      generateRentForMonth(mk = monthKey()) {
        let added = 0;
        setData((d) => {
          const existing = new Set(d.ledger.filter((r) => r.month === mk).map((r) => r.tenantId));
          const newRows = d.tenants
            .filter((t) => eligibleToBill(t, mk) && !existing.has(t.id))
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
        setData((d) => {
          // Re-id against the latest state so a double-tap can't create two
          // tenants (and their ledger rows) sharing one id.
          const id = nextId(d.tenants);
          const tenant = { ...created, id };
          return {
            ...d,
            tenants: [...d.tenants, tenant],
            suites: d.suites.map((s) => (s.id === Number(form.suiteId) ? { ...s, tenantId: id } : s)),
            // Bill the current month, due on the move-in date so a mid-month new
            // tenant isn't flagged late/overdue on day one.
            ledger: [...d.ledger, { id: nextId(d.ledger), tenantId: id, month: monthKey(), amount: created.rent, dueDate: todayISO(), paidDate: null }],
          };
        });
        notify(`${created.name.split(" ")[0]} added`);
        return created;
      },
      updateTenant(id, patch) {
        update((d) => ({ tenants: d.tenants.map((t) => (t.id === id ? { ...t, ...patch } : t)) }));
      },
      giveNotice(id) {
        // Giving notice means moving out at the end of the current month — set
        // that as the move-out date so billing stops and the suite frees up then,
        // regardless of any later original lease-end date.
        const cur = monthKey();
        const lastDay = new Date(Number(cur.slice(0, 4)), Number(cur.slice(5, 7)), 0).getDate();
        const moveOut = `${cur}-${String(lastDay).padStart(2, "0")}`;
        update((d) => ({
          tenants: d.tenants.map((t) =>
            t.id === id ? { ...t, status: "notice", leaseEnd: moveOut } : t
          ),
        }));
        notify("Marked as moving out");
      },
      renewLease(id, days = 365) {
        update((d) => {
          const window = d.settings.leaseRenewalWindowDays ?? 60;
          return {
            tenants: d.tenants.map((t) => {
              if (t.id !== id) return t;
              // Idempotent: only renew a lease that's actually up for renewal, so a
              // double-tap can't stack into a multi-year extension.
              if (t.status === "active" && t.leaseEnd > addDays(todayISO(), window)) return t;
              return { ...t, status: "active", leaseEnd: addDays(t.leaseEnd >= todayISO() ? t.leaseEnd : todayISO(), days) };
            }),
          };
        });
        notify("Lease renewed");
      },
      endTenancy(id) {
        update((d) => ({
          tenants: d.tenants.map((t) => (t.id === id ? { ...t, status: "past" } : t)),
          suites: d.suites.map((s) => (s.tenantId === id ? { ...s, tenantId: null } : s)),
          // Drop any unpaid rent dated after move-out so the app never asks the
          // owner to collect future rent from someone who has left.
          ledger: d.ledger.filter((r) => !(r.tenantId === id && !r.paidDate && r.dueDate > todayISO())),
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
      // Approve an applicant into a tenant: create the tenancy, assign the suite,
      // bill the current month, and remove them from the pipeline (all re-id'd
      // inside the updater so a double-tap can't duplicate).
      convertApplicantToTenant(applicantId, suiteId) {
        let created = null;
        setData((d) => {
          const applicant = d.applicants.find((a) => a.id === applicantId);
          const suite = d.suites.find((s) => s.id === Number(suiteId));
          if (!applicant || !suite || suite.tenantId) return d;
          const id = nextId(d.tenants);
          created = {
            id,
            name: applicant.name,
            business: "",
            profession: applicant.profession,
            phone: applicant.phone,
            email: applicant.email,
            suite: suite.name,
            rent: suite.rent,
            deposit: suite.rent,
            status: "active",
            leaseStart: todayISO(),
            leaseEnd: addDays(todayISO(), 365),
            moveIn: todayISO(),
            notes: applicant.notes || "",
          };
          return {
            ...d,
            tenants: [...d.tenants, created],
            suites: d.suites.map((s) => (s.id === Number(suiteId) ? { ...s, tenantId: id } : s)),
            ledger: [...d.ledger, { id: nextId(d.ledger), tenantId: id, month: monthKey(), amount: suite.rent, dueDate: todayISO(), paidDate: null }],
            applicants: d.applicants.filter((a) => a.id !== applicantId),
          };
        });
        if (created) notify(`${created.name.split(" ")[0]} is now a tenant`);
        return created;
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
        const ok = parsed && ["suites", "tenants", "ledger", "applicants", "maintenance"].every((k) => Array.isArray(parsed[k]));
        if (!ok) throw new Error("That file doesn't look like a complete Bloom Suites backup.");
        setData(normalize(parsed));
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
