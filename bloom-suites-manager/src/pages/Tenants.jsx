// Tenants: searchable list, full profile with lease + payment history and the
// rent/renewal shortcuts, plus a new-tenant intake form.
import { useMemo, useState } from "react";
import { useBloom } from "../store";
import {
  rentStatus, rentReminder, renewalMessage, daysUntil, suiteStatus,
} from "../automation";
import { PROFESSIONS } from "../seed";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { fmt, monthLabel, monthKey } from "../format";
import {
  Card, SectionHeader, SearchBar, StatusBadge, Avatar, BackButton, PageTitle,
  Field, Input, Select, Textarea, PrimaryButton, GhostButton, copyText,
} from "../ui";

function TenantForm({ onCancel, onSubmit, vacantSuites }) {
  const [form, setForm] = useState({ name: "", business: "", profession: "Lash Artist", phone: "", email: "", suiteId: vacantSuites[0]?.id || "", notes: "" });
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));
  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onCancel} label="Cancel" />
      <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: "0 0 16px" }}>New Tenant</h2>
      <Card style={{ padding: 20 }}>
        <Field label="Name"><Input value={form.name} onChange={set("name")} /></Field>
        <Field label="Business Name"><Input value={form.business} onChange={set("business")} placeholder="e.g. Lashes by Kristen" /></Field>
        <Field label="Profession">
          <Select value={form.profession} onChange={set("profession")}>
            {PROFESSIONS.map((p) => <option key={p} value={p}>{p}</option>)}
          </Select>
        </Field>
        <Field label="Phone"><Input type="tel" value={form.phone} onChange={set("phone")} /></Field>
        <Field label="Email"><Input type="email" value={form.email} onChange={set("email")} /></Field>
        <Field label="Suite">
          {vacantSuites.length === 0 ? (
            <div style={{ fontSize: 13, color: C.red, padding: "8px 0" }}>No vacant suites available right now.</div>
          ) : (
            <Select value={form.suiteId} onChange={set("suiteId")}>
              {vacantSuites.map((s) => <option key={s.id} value={s.id}>{s.name} — {fmt(s.rent)}/mo</option>)}
            </Select>
          )}
        </Field>
        <Field label="Notes"><Textarea rows={2} value={form.notes} onChange={set("notes")} /></Field>
        <p style={{ fontSize: 11, color: C.grayLight, marginTop: -4, marginBottom: 14 }}>A 1-year lease starts today and this month's rent is billed automatically.</p>
        <PrimaryButton disabled={!form.name || !form.phone || !form.suiteId} onClick={() => onSubmit(form)}>Add Tenant</PrimaryButton>
      </Card>
    </div>
  );
}

function TenantDetail({ tenant, onBack }) {
  const { data, actions, notify } = useBloom();
  const rows = data.ledger.filter((r) => r.tenantId === tenant.id).sort((a, b) => b.month.localeCompare(a.month));
  const currentDue = rows.find((r) => r.month === monthKey() && !r.paidDate);
  const leaseLeft = daysUntil(tenant.leaseEnd);

  const copy = async (text) => {
    const ok = await copyText(text);
    notify(ok ? "Message copied" : "Couldn't copy");
  };

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onBack} />
      <Card style={{ padding: 20, marginBottom: 16 }}>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <Avatar name={tenant.name} size={48} />
          <div style={{ flex: 1 }}>
            <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: "0 0 2px" }}>{tenant.name}</h2>
            <div style={{ fontSize: 13, color: C.gray }}>{tenant.profession} · {tenant.business}</div>
            <div style={{ marginTop: 4 }}><StatusBadge status={tenant.status === "active" ? "occupied" : tenant.status === "notice" ? "notice" : "vacant"} /></div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 18, fontWeight: 700, color: C.gold }}>{fmt(tenant.rent)}</div>
            <div style={{ fontSize: 11, color: C.grayLight }}>{tenant.suite}</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 8, marginTop: 16, flexWrap: "wrap" }}>
          <a href={`tel:${tenant.phone}`} style={{ flex: "1 1 100px", textAlign: "center", padding: 10, borderRadius: 10, background: C.roseLight, color: C.rose, fontSize: 13, fontWeight: 600, textDecoration: "none" }}>Call</a>
          {currentDue && <GhostButton style={{ flex: "1 1 100px", textAlign: "center" }} onClick={() => copy(rentReminder(tenant, currentDue, data.settings))}>Rent reminder</GhostButton>}
        </div>
      </Card>

      <Card style={{ marginBottom: 12 }}>
        <SectionHeader title="Lease" />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
          {[["Suite", tenant.suite], ["Rent", `${fmt(tenant.rent)}/mo`], ["Lease Start", tenant.leaseStart], ["Lease End", tenant.leaseEnd], ["Deposit", fmt(tenant.deposit)], ["Days Left", `${leaseLeft}d`]].map(([l, v]) => (
            <div key={l} style={{ background: C.roseLight, borderRadius: 10, padding: "8px 12px" }}>
              <div style={{ fontSize: 10, color: C.grayLight, textTransform: "uppercase", letterSpacing: 0.5 }}>{l}</div>
              <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{v}</div>
            </div>
          ))}
        </div>
        {leaseLeft <= (data.settings.leaseRenewalWindowDays ?? 60) && tenant.status === "active" && (
          <div style={{ marginTop: 10, display: "flex", gap: 8 }}>
            <PrimaryButton style={{ padding: 10, fontSize: 13 }} onClick={() => actions.renewLease(tenant.id)}>Renew 1 Year</PrimaryButton>
            <GhostButton style={{ flex: 1, textAlign: "center" }} onClick={() => copy(renewalMessage(tenant, data.settings))}>Copy renewal</GhostButton>
          </div>
        )}
      </Card>

      {tenant.notes && (
        <Card style={{ marginBottom: 12 }}>
          <SectionHeader title="Notes" />
          <p style={{ fontSize: 13, color: C.charcoal, margin: 0 }}>{tenant.notes}</p>
        </Card>
      )}

      <Card style={{ marginBottom: 12 }}>
        <SectionHeader title="Payment History" />
        {rows.length === 0 ? (
          <p style={{ fontSize: 13, color: C.grayLight, textAlign: "center", padding: 12 }}>No rent billed yet</p>
        ) : (
          rows.slice(0, 8).map((r) => {
            const st = rentStatus(r, data.settings);
            return (
              <div key={r.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 0", borderBottom: `1px solid ${C.grayBorder}` }}>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: C.charcoal }}>{monthLabel(r.month)}</div>
                  <div style={{ fontSize: 11, color: C.gray }}>{r.paidDate ? `Paid ${r.paidDate}` : `Due ${r.dueDate}`}</div>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{ fontSize: 13, fontWeight: 600 }}>{fmt(r.amount)}</span>
                  {r.paidDate ? (
                    <button onClick={() => actions.markRentUnpaid(r.id)} style={pill(C.green, C.greenLight)}>paid</button>
                  ) : (
                    <button onClick={() => actions.markRentPaid(r.id)} style={pill(st === "late" ? C.red : C.gold, st === "late" ? C.redLight : C.goldLight)}>{st === "late" ? "late — mark paid" : "mark paid"}</button>
                  )}
                </div>
              </div>
            );
          })
        )}
      </Card>

      <Card>
        <SectionHeader title="Manage" />
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {tenant.status === "active" && (
            <button onClick={() => { if (confirm(`Mark ${tenant.name} as moving out (giving notice)?`)) actions.giveNotice(tenant.id); }} style={{ padding: 12, borderRadius: 10, border: `1px solid ${C.amber}`, background: C.amberLight, color: C.amber, fontSize: 14, fontWeight: 600, cursor: "pointer" }}>Give Notice (moving out)</button>
          )}
          <button onClick={() => { if (confirm(`End ${tenant.name}'s tenancy and free up ${tenant.suite}? They'll move to past tenants.`)) { actions.endTenancy(tenant.id); onBack(); } }} style={{ padding: 12, borderRadius: 10, border: `1px solid ${C.red}`, background: C.redLight, color: C.red, fontSize: 14, fontWeight: 600, cursor: "pointer" }}>End Tenancy</button>
        </div>
      </Card>
    </div>
  );
}
const pill = (color, bg) => ({ fontSize: 10, fontWeight: 700, color, background: bg, padding: "4px 8px", borderRadius: 10, textTransform: "uppercase", letterSpacing: 0.3, border: "none", cursor: "pointer" });

export default function Tenants({ selectedTenantId, setSelectedTenantId }) {
  const { data, actions } = useBloom();
  const [search, setSearch] = useState("");
  const [adding, setAdding] = useState(false);

  const vacantSuites = useMemo(
    () => data.suites.filter((s) => suiteStatus(s, data.tenants) === "vacant"),
    [data.suites, data.tenants]
  );
  const selected = selectedTenantId ? data.tenants.find((t) => t.id === selectedTenantId) : null;

  const list = useMemo(() => {
    const q = search.trim().toLowerCase();
    const order = { active: 0, notice: 1, past: 2 };
    return data.tenants
      .filter((t) => (q ? t.name.toLowerCase().includes(q) || t.business.toLowerCase().includes(q) || t.suite.toLowerCase().includes(q) || t.profession.toLowerCase().includes(q) : true))
      .sort((a, b) => (order[a.status] - order[b.status]) || a.name.localeCompare(b.name));
  }, [data.tenants, search]);

  if (adding) {
    return (
      <TenantForm
        vacantSuites={vacantSuites}
        onCancel={() => setAdding(false)}
        onSubmit={(form) => { const t = actions.addTenant(form); setAdding(false); setSelectedTenantId(t.id); }}
      />
    );
  }
  if (selected) return <TenantDetail tenant={selected} onBack={() => setSelectedTenantId(null)} />;

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <PageTitle right={
        <button onClick={() => setAdding(true)} style={{ display: "flex", alignItems: "center", gap: 4, background: C.rose, color: C.white, border: "none", borderRadius: 10, padding: "8px 14px", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
          <Icon d={Icons.plus} size={16} color={C.white} /> New
        </button>
      }>Tenants</PageTitle>
      <SearchBar value={search} onChange={setSearch} placeholder="Search by name, business, suite…" />
      {list.map((t) => {
        const badge = t.status === "active" ? "occupied" : t.status === "notice" ? "notice" : "vacant";
        return (
          <div key={t.id} onClick={() => setSelectedTenantId(t.id)} style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 14px", background: C.white, borderRadius: 14, marginBottom: 8, boxShadow: "0 1px 3px rgba(0,0,0,0.04)", cursor: "pointer", opacity: t.status === "past" ? 0.6 : 1 }}>
            <Avatar name={t.name} />
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{t.name}</div>
              <div style={{ fontSize: 12, color: C.gray }}>{t.profession} · {t.suite || "—"}</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: C.gold }}>{fmt(t.rent)}</div>
              <div style={{ marginTop: 2 }}><StatusBadge status={badge} /></div>
            </div>
          </div>
        );
      })}
      {list.length === 0 && <p style={{ textAlign: "center", color: C.grayLight, padding: 30 }}>No tenants found</p>}
    </div>
  );
}
