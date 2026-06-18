// "More" hub plus its sub-pages: Inventory, Waitlist, Service Menu, and
// Settings (business info, expenses, and data backup/restore).
import { useRef, useState } from "react";
import { useBloom } from "../store";
import { lowStockItems, expiringItems, waitlistMessage } from "../automation";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { fmt, fmtD } from "../format";
import {
  Card, SectionHeader, StatusBadge, BackButton, PageTitle, EmptyState,
  Field, Input, Select, PrimaryButton, GhostButton, Modal, copyText,
} from "../ui";

// ---------- Inventory ----------
const INV_CATS = ["Adhesive", "Lash Trays", "Consumables", "Solutions", "Tools"];
const EMPTY_INV = { name: "", category: "Consumables", qty: "", reorder: "", cost: "", supplier: "", expires: "" };

function Inventory({ onBack }) {
  const { data, actions } = useBloom();
  const low = lowStockItems(data.inventory);
  const expiring = expiringItems(data.inventory);
  const [adding, setAdding] = useState(false);
  const [form, setForm] = useState(EMPTY_INV);
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onBack} />
      <PageTitle right={<button onClick={() => { setForm(EMPTY_INV); setAdding(true); }} style={addBtn}><Icon d={Icons.plus} size={16} color={C.white} /> Add</button>}>Inventory</PageTitle>

      {(low.length > 0 || expiring.length > 0) && (
        <div style={{ marginBottom: 16 }}>
          {low.map((i) => (
            <div key={`low-${i.id}`} style={{ background: C.amberLight, border: `1px solid ${C.amber}`, borderRadius: 10, padding: "8px 12px", marginBottom: 6, fontSize: 13, color: C.charcoal }}>
              ⚠ <strong>{i.name}</strong> — {i.qty} left (reorder at {i.reorder})
            </div>
          ))}
          {expiring.map((i) => (
            <div key={`exp-${i.id}`} style={{ background: C.redLight, border: `1px solid ${C.red}`, borderRadius: 10, padding: "8px 12px", marginBottom: 6, fontSize: 13, color: C.charcoal }}>
              🕐 <strong>{i.name}</strong> — expires {i.expires}
            </div>
          ))}
        </div>
      )}

      {data.inventory.length === 0 && <EmptyState icon={Icons.box} text="No inventory yet — tap Add to track your first supply" />}

      {INV_CATS.map((cat) => {
        const items = data.inventory.filter((i) => i.category === cat);
        if (!items.length) return null;
        return (
          <div key={cat} style={{ marginBottom: 16 }}>
            <h3 style={{ fontSize: 12, fontWeight: 700, color: C.rose, margin: "0 0 8px", textTransform: "uppercase", letterSpacing: 0.5 }}>{cat}</h3>
            {items.map((i) => (
              <div key={i.id} style={{ background: C.white, borderRadius: 12, padding: "12px 14px", marginBottom: 6, boxShadow: "0 1px 3px rgba(0,0,0,0.04)" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 13, fontWeight: 600, color: C.charcoal }}>{i.name}</div>
                    <div style={{ fontSize: 11, color: C.gray }}>
                      {fmtD(i.cost)} · {i.supplier}{i.expires ? ` · Exp ${i.expires}` : ""}
                    </div>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                    <button onClick={() => actions.adjustInventory(i.id, -1)} style={qtyBtn}>−</button>
                    <span style={{ fontSize: 16, fontWeight: 700, color: i.qty <= i.reorder ? C.amber : C.charcoal, minWidth: 24, textAlign: "center" }}>{i.qty}</span>
                    <button onClick={() => actions.adjustInventory(i.id, 1)} style={qtyBtn}>+</button>
                  </div>
                </div>
                {i.qty <= i.reorder && (
                  <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
                    {i.onOrder ? (
                      <button onClick={() => actions.receiveStock(i.id, i.reorder * 2)} style={{ flex: 1, padding: 8, borderRadius: 8, border: "none", background: C.green, color: C.white, fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
                        ✓ Received — add stock
                      </button>
                    ) : (
                      <button onClick={() => actions.markOrdered(i.id)} style={{ flex: 1, padding: 8, borderRadius: 8, border: `1px solid ${C.amber}`, background: C.amberLight, color: C.amber, fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
                        Mark ordered
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        );
      })}

      <Modal open={adding} onClose={() => setAdding(false)} title="Add Inventory Item">
        <Field label="Name"><Input value={form.name} onChange={set("name")} placeholder="e.g. Classic Lash Tray — C 0.15" /></Field>
        <Field label="Category">
          <Select value={form.category} onChange={set("category")}>{INV_CATS.map((c) => <option key={c} value={c}>{c}</option>)}</Select>
        </Field>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <Field label="Quantity on hand"><Input type="number" inputMode="numeric" min={0} value={form.qty} onChange={set("qty")} /></Field>
          <Field label="Reorder at"><Input type="number" inputMode="numeric" min={0} value={form.reorder} onChange={set("reorder")} /></Field>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <Field label="Cost ($)"><Input type="number" inputMode="decimal" min={0} value={form.cost} onChange={set("cost")} /></Field>
          <Field label="Supplier"><Input value={form.supplier} onChange={set("supplier")} /></Field>
        </div>
        <Field label="Expiry date (optional)"><Input type="date" value={form.expires} onChange={set("expires")} /></Field>
        <PrimaryButton disabled={!form.name} onClick={() => { actions.addInventoryItem(form); setAdding(false); }}>Add Item</PrimaryButton>
      </Modal>
    </div>
  );
}
const qtyBtn = { width: 28, height: 28, borderRadius: 8, border: `1px solid ${C.grayBorder}`, background: C.white, cursor: "pointer", fontSize: 16, fontWeight: 700, color: C.charcoal };

// ---------- Waitlist ----------
function Waitlist({ onBack }) {
  const { data, actions, notify } = useBloom();
  const [adding, setAdding] = useState(false);
  const blankWaitlist = () => ({ name: "", phone: "", service: data.services[0]?.name || "", preferred: "" });
  const [form, setForm] = useState(blankWaitlist);
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));
  const openAdd = () => { setForm(blankWaitlist()); setAdding(true); };

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onBack} />
      <PageTitle
        right={
          <button onClick={openAdd} style={{ display: "flex", alignItems: "center", gap: 4, background: C.rose, color: C.white, border: "none", borderRadius: 10, padding: "8px 14px", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
            <Icon d={Icons.plus} size={16} color={C.white} /> Add
          </button>
        }
      >
        Waitlist
      </PageTitle>

      {data.waitlist.length === 0 && <EmptyState icon={Icons.list} text="No one on the waitlist right now" />}

      {data.waitlist.map((w) => (
        <Card key={w.id} style={{ padding: "14px 16px", marginBottom: 8 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <div>
              <div style={{ fontSize: 15, fontWeight: 600, color: C.charcoal }}>{w.name}</div>
              <div style={{ fontSize: 12, color: C.gray }}>{w.service} · {w.preferred}</div>
              <div style={{ fontSize: 11, color: C.grayLight, marginTop: 2 }}>{w.phone} · Added {w.added}</div>
            </div>
            <StatusBadge status={w.status} />
          </div>
          <div style={{ display: "flex", gap: 8, marginTop: 10, flexWrap: "wrap" }}>
            <button
              onClick={async () => {
                const ok = await copyText(waitlistMessage(w, data.settings));
                notify(ok ? "Message copied" : "Couldn't copy");
              }}
              style={btn(false)}
            >
              Copy text
            </button>
            {w.status === "waiting" && (
              <button onClick={() => actions.setWaitlistStatus(w.id, "contacted")} style={btn(false)}>Mark contacted</button>
            )}
            <button onClick={() => actions.setWaitlistStatus(w.id, "booked")} style={btn(true)}>Booked</button>
            <button onClick={() => actions.removeWaitlist(w.id)} style={{ ...btn(false), borderColor: C.grayBorder, color: C.gray }}>Remove</button>
          </div>
        </Card>
      ))}

      <Modal open={adding} onClose={() => setAdding(false)} title="Add to Waitlist">
        <Field label="Name"><Input value={form.name} onChange={set("name")} /></Field>
        <Field label="Phone"><Input type="tel" value={form.phone} onChange={set("phone")} /></Field>
        <Field label="Service">
          <Select value={form.service} onChange={set("service")}>
            {data.services.map((s) => <option key={s.id} value={s.name}>{s.name}</option>)}
          </Select>
        </Field>
        <Field label="Preferred Times"><Input value={form.preferred} onChange={set("preferred")} placeholder="e.g. Weekday mornings" /></Field>
        <PrimaryButton
          disabled={!form.name || !form.phone}
          onClick={() => {
            actions.addWaitlist(form);
            setForm(blankWaitlist());
            setAdding(false);
          }}
        >
          Add to Waitlist
        </PrimaryButton>
      </Modal>
    </div>
  );
}
const btn = (solid) => ({ padding: "8px 12px", borderRadius: 8, border: solid ? "none" : `1px solid ${C.rose}`, background: solid ? C.rose : C.roseLight, color: solid ? C.white : C.rose, fontSize: 12, fontWeight: 600, cursor: "pointer" });

// ---------- Services (editable: owners change prices and offerings) ----------
const SVC_CATS = ["Full Set", "Fill", "Other"];
const EMPTY_SVC = { name: "", category: "Full Set", price: "", duration: "" };

function Services({ onBack }) {
  const { data, actions } = useBloom();
  const [editing, setEditing] = useState(null); // service object, or "new", or null
  const [form, setForm] = useState(EMPTY_SVC);
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const openNew = () => { setForm(EMPTY_SVC); setEditing("new"); };
  const openEdit = (s) => { setForm({ name: s.name, category: s.category, price: s.price, duration: s.duration }); setEditing(s); };
  const save = () => {
    if (editing === "new") actions.addService(form);
    else actions.updateService(editing.id, { name: form.name.trim(), category: form.category, price: Math.max(0, Number(form.price) || 0), duration: Number(form.duration) > 0 ? Number(form.duration) : 60 });
    setEditing(null);
  };

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onBack} />
      <PageTitle right={<button onClick={openNew} style={addBtn}><Icon d={Icons.plus} size={16} color={C.white} /> Add</button>}>Service Menu</PageTitle>
      {SVC_CATS.map((cat) => {
        const items = data.services.filter((s) => s.category === cat);
        if (!items.length) return null;
        return (
          <div key={cat} style={{ marginBottom: 20 }}>
            <h3 style={{ fontSize: 12, fontWeight: 700, color: C.rose, margin: "0 0 8px", textTransform: "uppercase", letterSpacing: 0.5 }}>{cat}s</h3>
            {items.map((s) => (
              <button key={s.id} onClick={() => openEdit(s)} style={{ width: "100%", textAlign: "left", background: C.white, borderRadius: 12, padding: "12px 16px", marginBottom: 6, boxShadow: "0 1px 3px rgba(0,0,0,0.04)", border: "none", cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{s.name}</div>
                  <div style={{ fontSize: 12, color: C.gray }}>{s.duration} min · tap to edit</div>
                </div>
                <div style={{ fontSize: 18, fontWeight: 700, color: C.gold }}>{fmt(s.price)}</div>
              </button>
            ))}
          </div>
        );
      })}

      <Modal open={!!editing} onClose={() => setEditing(null)} title={editing === "new" ? "Add Service" : "Edit Service"}>
        <Field label="Name"><Input value={form.name} onChange={set("name")} placeholder="e.g. Volume Full Set" /></Field>
        <Field label="Category">
          <Select value={form.category} onChange={set("category")}>{SVC_CATS.map((c) => <option key={c} value={c}>{c}</option>)}</Select>
        </Field>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <Field label="Price ($)"><Input type="number" inputMode="decimal" min={0} value={form.price} onChange={set("price")} /></Field>
          <Field label="Duration (min)"><Input type="number" inputMode="numeric" min={0} value={form.duration} onChange={set("duration")} /></Field>
        </div>
        <PrimaryButton disabled={!form.name} onClick={save}>{editing === "new" ? "Add Service" : "Save Changes"}</PrimaryButton>
        {editing && editing !== "new" && (
          <button onClick={() => { if (confirm(`Remove "${editing.name}" from your menu?`)) { actions.deleteService(editing.id); setEditing(null); } }} style={{ width: "100%", marginTop: 10, padding: 12, borderRadius: 10, border: `1px solid ${C.red}`, background: C.redLight, color: C.red, fontSize: 14, fontWeight: 600, cursor: "pointer" }}>Remove Service</button>
        )}
      </Modal>
    </div>
  );
}
const addBtn = { display: "flex", alignItems: "center", gap: 4, background: C.rose, color: C.white, border: "none", borderRadius: 10, padding: "8px 14px", fontSize: 13, fontWeight: 600, cursor: "pointer" };

// ---------- Settings ----------
function Settings({ onBack }) {
  const { data, actions } = useBloom();
  const { settings } = data;
  const fileRef = useRef(null);

  const setField = (k) => (e) => actions.updateSettings({ [k]: e.target.value });
  const setExpense = (k) => (e) =>
    actions.updateSettings({ monthlyExpenses: { ...settings.monthlyExpenses, [k]: Math.max(0, Number(e.target.value) || 0) } });

  const backup = () => actions.backupData();
  const restore = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        actions.importData(String(reader.result));
      } catch (err) {
        alert(err.message || "Couldn't read that file.");
      }
    };
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
        <SectionHeader title="Monthly Expenses" />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          {[
            ["Rent", "rent"], ["Supplies", "supplies"], ["Tech/Phone", "tech"],
            ["Insurance", "insurance"], ["Banking", "banking"], ["Other", "other"],
          ].map(([label, key]) => (
            <Field key={key} label={label}>
              <Input type="number" inputMode="decimal" min={0} value={settings.monthlyExpenses[key]} onChange={setExpense(key)} />
            </Field>
          ))}
        </div>
        <p style={{ fontSize: 11, color: C.grayLight, margin: 0 }}>Used to estimate monthly profit on the Finances tab.</p>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Your Data" />
        <p style={{ fontSize: 12, color: C.gray, marginTop: 0 }}>
          Everything is stored privately on this device. Back up regularly so you never lose your records — and use the same file to move to a new phone.
        </p>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <PrimaryButton onClick={backup} style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
            <Icon d={Icons.download} size={18} color={C.white} /> Back Up My Data
          </PrimaryButton>
          <GhostButton style={{ textAlign: "center", display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }} onClick={() => fileRef.current?.click()}>
            <Icon d={Icons.upload} size={18} color={C.rose} /> Restore from Backup
          </GhostButton>
          <input ref={fileRef} type="file" accept="application/json,.json" onChange={restore} style={{ display: "none" }} />
        </div>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Start Over" />
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <button
            onClick={() => { if (confirm("Replace everything with the sample demo data?")) actions.resetToSample(); }}
            style={{ padding: 12, borderRadius: 10, border: `1px solid ${C.grayBorder}`, background: C.white, color: C.charcoal, fontSize: 14, fontWeight: 600, cursor: "pointer" }}
          >
            Load Sample Data
          </button>
          <button
            onClick={() => { if (confirm("Erase all clients, appointments, waitlist, and inventory so you can enter your own? Your service menu and settings are kept. This cannot be undone — back up first!")) actions.clearAll(); }}
            style={{ padding: 12, borderRadius: 10, border: `1px solid ${C.red}`, background: C.redLight, color: C.red, fontSize: 14, fontWeight: 600, cursor: "pointer" }}
          >
            Clear &amp; Start Fresh
          </button>
        </div>
      </Card>

      <p style={{ fontSize: 11, color: C.grayLight, textAlign: "center" }}>Bloom Beauty Suites · Beta</p>
    </div>
  );
}

// ---------- Hub ----------
export default function More() {
  const { data } = useBloom();
  const [page, setPage] = useState(null);
  const low = lowStockItems(data.inventory);

  if (page === "inventory") return <Inventory onBack={() => setPage(null)} />;
  if (page === "waitlist") return <Waitlist onBack={() => setPage(null)} />;
  if (page === "services") return <Services onBack={() => setPage(null)} />;
  if (page === "settings") return <Settings onBack={() => setPage(null)} />;

  const items = [
    { id: "inventory", icon: Icons.box, label: "Inventory", sub: `${low.length} low stock`, badge: low.length || null },
    { id: "waitlist", icon: Icons.list, label: "Waitlist", sub: `${data.waitlist.filter((w) => w.status !== "booked").length} waiting` },
    { id: "services", icon: Icons.star, label: "Service Menu", sub: `${data.services.length} services` },
    { id: "settings", icon: Icons.settings, label: "Settings & Backup", sub: "Business info, expenses, data" },
  ];

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
          ["Active Clients", `${data.clients.length}`],
          ["Services Offered", `${data.services.length}`],
          ["Monthly Rent", fmt(data.settings.monthlyExpenses.rent)],
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
