// "More" hub plus its sub-pages: Applicants, Maintenance, and Settings
// (business info, expenses, rules, and data backup/restore).
import { useEffect, useRef, useState } from "react";
import { useBloom } from "../store";
import { applicantMessage, tenantById, suiteById } from "../automation";
import { PROFESSIONS } from "../seed";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { fmt, daysAgo } from "../format";
import {
  Card, SectionHeader, StatusBadge, BackButton, PageTitle, EmptyState,
  Field, Input, Select, Textarea, PrimaryButton, GhostButton, Modal, copyText,
} from "../ui";

const APPLICANT_NEXT = { new: "toured", toured: "applied", applied: "approved" };

// ---------- Applicants ----------
function Applicants({ onBack }) {
  const { data, actions, notify } = useBloom();
  const [adding, setAdding] = useState(false);
  const [form, setForm] = useState({ name: "", profession: "Lash Artist", phone: "", email: "", interest: "", notes: "" });
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onBack} />
      <PageTitle right={
        <button onClick={() => setAdding(true)} style={addBtn}><Icon d={Icons.plus} size={16} color={C.white} /> Add</button>
      }>Applicants</PageTitle>

      {data.applicants.length === 0 && <EmptyState icon={Icons.users} text="No applicants yet" />}

      {data.applicants.map((a) => (
        <Card key={a.id} style={{ padding: "14px 16px", marginBottom: 8 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <div>
              <div style={{ fontSize: 15, fontWeight: 600, color: C.charcoal }}>{a.name}</div>
              <div style={{ fontSize: 12, color: C.gray }}>{a.profession} · interested in {a.interest}</div>
              <div style={{ fontSize: 11, color: C.grayLight, marginTop: 2 }}>{a.phone} · {daysAgo(a.added)}d ago</div>
              {a.notes && <div style={{ fontSize: 12, color: C.gray, marginTop: 4 }}>{a.notes}</div>}
            </div>
            <StatusBadge status={a.status} />
          </div>
          <div style={{ display: "flex", gap: 8, marginTop: 10, flexWrap: "wrap" }}>
            {APPLICANT_NEXT[a.status] && (
              <button onClick={() => actions.setApplicantStatus(a.id, APPLICANT_NEXT[a.status])} style={miniBtn(true)}>
                Mark {APPLICANT_NEXT[a.status]}
              </button>
            )}
            <button onClick={async () => { const ok = await copyText(applicantMessage(a, data.settings)); notify(ok ? "Message copied" : "Couldn't copy"); }} style={miniBtn(false)}>Copy text</button>
            <button onClick={() => actions.removeApplicant(a.id)} style={{ ...miniBtn(false), borderColor: C.grayBorder, color: C.gray }}>Remove</button>
          </div>
        </Card>
      ))}

      <Modal open={adding} onClose={() => setAdding(false)} title="Add Applicant">
        <Field label="Name"><Input value={form.name} onChange={set("name")} /></Field>
        <Field label="Profession">
          <Select value={form.profession} onChange={set("profession")}>{PROFESSIONS.map((p) => <option key={p}>{p}</option>)}</Select>
        </Field>
        <Field label="Phone"><Input type="tel" value={form.phone} onChange={set("phone")} /></Field>
        <Field label="Email"><Input type="email" value={form.email} onChange={set("email")} /></Field>
        <Field label="Interested In"><Input value={form.interest} onChange={set("interest")} placeholder="e.g. Suite 4, or any medium suite" /></Field>
        <Field label="Notes"><Textarea rows={2} value={form.notes} onChange={set("notes")} /></Field>
        <PrimaryButton disabled={!form.name || !form.phone} onClick={() => { actions.addApplicant(form); setForm({ name: "", profession: "Lash Artist", phone: "", email: "", interest: "", notes: "" }); setAdding(false); }}>Add Applicant</PrimaryButton>
      </Modal>
    </div>
  );
}

// ---------- Maintenance ----------
function Maintenance({ onBack }) {
  const { data, actions } = useBloom();
  const [adding, setAdding] = useState(false);
  const [form, setForm] = useState({ suiteId: data.suites[0]?.id || "", title: "", priority: "normal" });
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));
  const open = data.maintenance.filter((m) => m.status !== "done");
  const done = data.maintenance.filter((m) => m.status === "done");

  const TicketCard = ({ m }) => (
    <Card style={{ padding: "12px 14px", marginBottom: 8 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{m.title}</div>
          <div style={{ fontSize: 12, color: C.gray }}>{suiteById(data.suites, m.suiteId)?.name || "Common area"}{m.tenantId ? ` · ${tenantById(data.tenants, m.tenantId)?.name || ""}` : ""} · {m.priority} priority</div>
          <div style={{ fontSize: 11, color: C.grayLight, marginTop: 2 }}>Logged {m.created}</div>
        </div>
        <StatusBadge status={m.status} />
      </div>
      {m.status !== "done" && (
        <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
          {m.status === "open" && <button onClick={() => actions.setMaintenanceStatus(m.id, "in-progress")} style={miniBtn(false)}>Start</button>}
          <button onClick={() => actions.setMaintenanceStatus(m.id, "done")} style={miniBtn(true)}>Mark done</button>
        </div>
      )}
    </Card>
  );

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onBack} />
      <PageTitle right={<button onClick={() => setAdding(true)} style={addBtn}><Icon d={Icons.plus} size={16} color={C.white} /> Log</button>}>Maintenance</PageTitle>

      {open.length === 0 ? <EmptyState icon={Icons.wrench} text="No open requests" /> : open.map((m) => <TicketCard key={m.id} m={m} />)}

      {done.length > 0 && (
        <>
          <h3 style={{ fontSize: 12, fontWeight: 700, color: C.grayLight, textTransform: "uppercase", letterSpacing: 0.5, margin: "16px 0 8px" }}>Completed</h3>
          {done.map((m) => <TicketCard key={m.id} m={m} />)}
        </>
      )}

      <Modal open={adding} onClose={() => setAdding(false)} title="Log Maintenance Request">
        <Field label="Suite">
          <Select value={form.suiteId} onChange={set("suiteId")}>{data.suites.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}</Select>
        </Field>
        <Field label="Issue"><Input value={form.title} onChange={set("title")} placeholder="e.g. Leaky faucet" /></Field>
        <Field label="Priority">
          <Select value={form.priority} onChange={set("priority")}><option value="low">Low</option><option value="normal">Normal</option><option value="high">High</option></Select>
        </Field>
        <PrimaryButton disabled={!form.title} onClick={() => { actions.addMaintenance(form); setForm({ suiteId: data.suites[0]?.id || "", title: "", priority: "normal" }); setAdding(false); }}>Log Request</PrimaryButton>
      </Modal>
    </div>
  );
}

// ---------- Settings ----------
function Settings({ onBack }) {
  const { data, actions } = useBloom();
  const { settings } = data;
  const fileRef = useRef(null);
  const setField = (k) => (e) => actions.updateSettings({ [k]: e.target.value });
  const setNum = (k) => (e) => actions.updateSettings({ [k]: Math.max(0, Number(e.target.value) || 0) });
  const setExpense = (k) => (e) => actions.updateSettings({ monthlyExpenses: { ...settings.monthlyExpenses, [k]: Math.max(0, Number(e.target.value) || 0) } });

  const backup = () => actions.backupData();
  const restore = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => { try { actions.importData(String(reader.result)); } catch (err) { alert(err.message || "Couldn't read that file."); } };
    reader.readAsText(file);
    e.target.value = "";
  };

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onBack} />
      <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: "0 0 16px" }}>Settings</h2>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Business Info" />
        <Field label="Your Name"><Input value={settings.ownerName} onChange={setField("ownerName")} /></Field>
        <Field label="Business Name"><Input value={settings.businessName} onChange={setField("businessName")} /></Field>
        <Field label="Location"><Input value={settings.location} onChange={setField("location")} /></Field>
        <Field label="Address"><Input value={settings.address} onChange={setField("address")} /></Field>
        <p style={{ fontSize: 11, color: C.grayLight, margin: 0 }}>Changes save automatically.</p>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Rules" />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <Field label="Rent late after (days)"><Input type="number" inputMode="numeric" min={0} value={settings.lateGraceDays} onChange={setNum("lateGraceDays")} /></Field>
          <Field label="Renewal window (days)"><Input type="number" inputMode="numeric" min={0} value={settings.leaseRenewalWindowDays} onChange={setNum("leaseRenewalWindowDays")} /></Field>
        </div>
        <p style={{ fontSize: 11, color: C.grayLight, margin: 0 }}>Controls when rent is flagged late and when lease renewals appear in your to-dos.</p>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Monthly Expenses" />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          {[["Mortgage/Lease", "mortgage"], ["Utilities", "utilities"], ["Insurance", "insurance"], ["Cleaning", "cleaning"], ["Internet", "internet"], ["Other", "other"]].map(([label, key]) => (
            <Field key={key} label={label}><Input type="number" inputMode="decimal" min={0} value={settings.monthlyExpenses[key]} onChange={setExpense(key)} /></Field>
          ))}
        </div>
        <p style={{ fontSize: 11, color: C.grayLight, margin: 0 }}>Tracked so you can compare rent collected against your costs.</p>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Your Data" />
        <p style={{ fontSize: 12, color: C.gray, marginTop: 0 }}>Everything is stored privately on this device. Back up regularly so you never lose your records — and use the same file to move to a new phone or computer.</p>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <PrimaryButton onClick={backup} style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}><Icon d={Icons.download} size={18} color={C.white} /> Back Up My Data</PrimaryButton>
          <GhostButton style={{ textAlign: "center", display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }} onClick={() => fileRef.current?.click()}><Icon d={Icons.upload} size={18} color={C.rose} /> Restore from Backup</GhostButton>
          <input ref={fileRef} type="file" accept="application/json,.json" onChange={restore} style={{ display: "none" }} />
        </div>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Start Over" />
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <button onClick={() => { if (confirm("Replace everything with the sample demo data?")) actions.resetToSample(); }} style={{ padding: 12, borderRadius: 10, border: `1px solid ${C.grayBorder}`, background: C.white, color: C.charcoal, fontSize: 14, fontWeight: 600, cursor: "pointer" }}>Load Sample Data</button>
          <button onClick={() => { if (confirm("Erase all tenants, rent records, applicants, and maintenance (suites are kept, set to vacant)? Back up first!")) actions.clearAll(); }} style={{ padding: 12, borderRadius: 10, border: `1px solid ${C.red}`, background: C.redLight, color: C.red, fontSize: 14, fontWeight: 600, cursor: "pointer" }}>Clear &amp; Start Fresh</button>
        </div>
      </Card>

      <p style={{ fontSize: 11, color: C.grayLight, textAlign: "center" }}>Bloom Suites Manager · Beta</p>
    </div>
  );
}
const addBtn = { display: "flex", alignItems: "center", gap: 4, background: C.rose, color: C.white, border: "none", borderRadius: 10, padding: "8px 14px", fontSize: 13, fontWeight: 600, cursor: "pointer" };
const miniBtn = (solid) => ({ padding: "8px 12px", borderRadius: 8, border: solid ? "none" : `1px solid ${C.rose}`, background: solid ? C.rose : C.roseLight, color: solid ? C.white : C.rose, fontSize: 12, fontWeight: 600, cursor: "pointer" });

// ---------- Hub ----------
export default function More({ sub, clearSub }) {
  const { data } = useBloom();
  const [page, setPage] = useState(sub || null);

  useEffect(() => {
    if (sub) { setPage(sub); clearSub(); }
  }, [sub, clearSub]);

  if (page === "applicants") return <Applicants onBack={() => setPage(null)} />;
  if (page === "maintenance") return <Maintenance onBack={() => setPage(null)} />;
  if (page === "settings") return <Settings onBack={() => setPage(null)} />;

  const openMaint = data.maintenance.filter((m) => m.status !== "done").length;
  const activeLeads = data.applicants.filter((a) => a.status !== "approved").length;
  const items = [
    { id: "applicants", icon: Icons.users, label: "Applicants", sub: `${activeLeads} in pipeline` },
    { id: "maintenance", icon: Icons.wrench, label: "Maintenance", sub: `${openMaint} open`, badge: openMaint || null },
    { id: "settings", icon: Icons.settings, label: "Settings & Backup", sub: "Business info, expenses, data" },
  ];

  const totalExp = Object.values(data.settings.monthlyExpenses).reduce((s, v) => s + v, 0);

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: "0 0 16px" }}>More</h2>
      {items.map((item) => (
        <button key={item.id} onClick={() => setPage(item.id)} style={{ display: "flex", alignItems: "center", gap: 14, width: "100%", padding: "16px 14px", background: C.white, borderRadius: 14, border: "none", marginBottom: 8, boxShadow: "0 1px 3px rgba(0,0,0,0.04)", cursor: "pointer", textAlign: "left" }}>
          <div style={{ width: 40, height: 40, borderRadius: 12, background: C.roseLight, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Icon d={item.icon} size={20} color={C.rose} />
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 15, fontWeight: 600, color: C.charcoal }}>{item.label}</div>
            <div style={{ fontSize: 12, color: C.gray }}>{item.sub}</div>
          </div>
          {item.badge && <span style={{ background: C.amber, color: C.white, fontSize: 11, fontWeight: 700, borderRadius: 10, padding: "2px 8px" }}>{item.badge}</span>}
          <Icon d={Icons.chevRight} size={18} color={C.grayLight} />
        </button>
      ))}

      <Card style={{ marginTop: 16 }}>
        <SectionHeader title="Business Snapshot" />
        {[
          ["Suites", `${data.suites.length}`],
          ["Tenants", `${data.tenants.filter((t) => t.status !== "past").length}`],
          ["Monthly Expenses", fmt(totalExp)],
          ["Location", data.settings.location],
          ["Address", data.settings.address],
        ].map(([label, val]) => (
          <div key={label} style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", borderBottom: `1px solid ${C.grayBorder}`, gap: 12 }}>
            <span style={{ fontSize: 13, color: C.gray }}>{label}</span>
            <span style={{ fontSize: 13, fontWeight: 600, color: C.charcoal, textAlign: "right" }}>{val}</span>
          </div>
        ))}
      </Card>
    </div>
  );
}
