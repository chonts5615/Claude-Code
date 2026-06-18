// Clients: searchable/filterable list, full profile with computed health and
// rebooking shortcuts, plus add/edit intake forms.
import { useMemo, useState } from "react";
import { useBloom } from "../store";
import { clientStatus, daysUntilDue, rebookMessage } from "../automation";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { fmt, daysAgo } from "../format";
import {
  Card, SectionHeader, SearchBar, StatusBadge, Avatar, BackButton, PageTitle,
  Field, Input, Select, Textarea, PrimaryButton, GhostButton, copyText, smsHref,
} from "../ui";
import BookAppointmentModal from "./BookAppointmentModal";

const CURLS = ["J", "B", "C", "D", "L"];
const STYLES = ["Natural", "Cat Eye", "Doll Eye", "Wispy", "Hybrid", "Volume", "Mega Volume"];
const EMPTY = { name: "", phone: "", email: "", curl: "C", style: "Natural", length: "", diameter: "", allergies: "None", notes: "" };

function ClientForm({ initial, title, submitLabel, onCancel, onSubmit }) {
  const [form, setForm] = useState(initial);
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));
  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onCancel} label="Cancel" />
      <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: "0 0 16px" }}>{title}</h2>
      <Card style={{ padding: 20 }}>
        <Field label="Full Name"><Input value={form.name} onChange={set("name")} /></Field>
        <Field label="Phone"><Input type="tel" value={form.phone} onChange={set("phone")} /></Field>
        <Field label="Email"><Input type="email" value={form.email} onChange={set("email")} /></Field>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <Field label="Curl Preference">
            <Select value={form.curl} onChange={set("curl")}>
              {CURLS.map((c) => <option key={c} value={c}>{c} Curl</option>)}
            </Select>
          </Field>
          <Field label="Style">
            <Select value={form.style} onChange={set("style")}>
              {STYLES.map((s) => <option key={s} value={s}>{s}</option>)}
            </Select>
          </Field>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <Field label="Length"><Input value={form.length} onChange={set("length")} placeholder="e.g. 11-13mm" /></Field>
          <Field label="Diameter"><Input value={form.diameter} onChange={set("diameter")} placeholder="e.g. 0.07mm" /></Field>
        </div>
        <Field label="Allergies / Sensitivities">
          <Input value={form.allergies} onChange={set("allergies")} placeholder="None, or describe…" />
        </Field>
        <Field label="Notes">
          <Textarea rows={3} value={form.notes} onChange={set("notes")} placeholder="Contact lenses, eye conditions, preferences…" />
        </Field>
        <div style={{ background: C.roseLight, borderRadius: 12, padding: 14, marginBottom: 16 }}>
          <p style={{ fontSize: 12, color: C.charcoal, margin: 0 }}>
            <strong>Consent:</strong> By proceeding, client acknowledges they have been informed of lash extension risks including potential allergic reaction, irritation, and the importance of following aftercare instructions. Client confirms no recent eye surgery, active eye infections, or contraindicated medications.
          </p>
        </div>
        <PrimaryButton disabled={!form.name || !form.phone} onClick={() => onSubmit(form)}>
          {submitLabel}
        </PrimaryButton>
      </Card>
    </div>
  );
}

function ClientDetail({ client, onBack, onEdit }) {
  const { data, actions, notify } = useBloom();
  const [booking, setBooking] = useState(false);
  const status = clientStatus(client);
  const since = daysAgo(client.lastVisit);
  const due = daysUntilDue(client, data.settings);
  const appts = data.appointments
    .filter((a) => a.clientId === client.id)
    .sort((a, b) => b.date.localeCompare(a.date));

  const copyReminder = async () => {
    const ok = await copyText(rebookMessage(client, data.settings));
    notify(ok ? "Reminder copied" : "Couldn't copy");
  };

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onBack} />
      <Card style={{ padding: 20, marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <Avatar name={client.name} size={48} />
            <div>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: "0 0 4px" }}>{client.name}</h2>
              <StatusBadge status={status} />
            </div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 20, fontWeight: 700, color: C.gold }}>{fmt(client.ltv)}</div>
            <div style={{ fontSize: 11, color: C.grayLight }}>Lifetime Value</div>
          </div>
        </div>
        <div style={{ display: "flex", gap: 8, marginTop: 16 }}>
          <PrimaryButton style={{ padding: 12, fontSize: 14 }} onClick={() => setBooking(true)}>Book</PrimaryButton>
          <GhostButton style={{ flex: 1, textAlign: "center" }} onClick={() => actions.rebookClient(client.id)}>Quick Rebook</GhostButton>
        </div>
      </Card>

      {due <= 7 && status !== "lost" && (
        <div style={{ background: C.amberLight, border: `1px solid ${C.amber}`, borderRadius: 12, padding: "10px 14px", marginBottom: 12, fontSize: 13, color: C.amber, fontWeight: 600, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
          <span>{due < 0 ? `⏰ Overdue by ${-due} days` : due === 0 ? "⏰ Due for rebooking today" : `⏰ Due in ${due} days`}</span>
          <div style={{ display: "flex", gap: 6 }}>
            <a href={smsHref(client.phone, rebookMessage(client, data.settings))} style={{ background: C.amber, color: C.white, borderRadius: 8, padding: "5px 10px", fontSize: 11, fontWeight: 700, textDecoration: "none", whiteSpace: "nowrap" }}>Text</a>
            <button onClick={copyReminder} style={{ background: C.white, color: C.amber, border: `1px solid ${C.amber}`, borderRadius: 8, padding: "5px 10px", fontSize: 11, fontWeight: 700, cursor: "pointer", whiteSpace: "nowrap" }}>Copy</button>
          </div>
        </div>
      )}

      <Card style={{ marginBottom: 12 }}>
        <SectionHeader title="Contact" action="Edit" onAction={onEdit} />
        <div style={{ fontSize: 13, color: C.charcoal, display: "flex", flexDirection: "column", gap: 6 }}>
          <a href={`tel:${client.phone}`} style={{ display: "flex", gap: 8, alignItems: "center", color: C.charcoal, textDecoration: "none" }}>
            <Icon d={Icons.phone} size={14} color={C.grayLight} /> {client.phone}
          </a>
          {client.email && <div style={{ display: "flex", gap: 8 }}><span style={{ fontSize: 14 }}>✉</span> {client.email}</div>}
          <div style={{ display: "flex", gap: 8 }}><Icon d={Icons.calendar} size={14} color={C.grayLight} /> Client since {client.firstVisit}</div>
        </div>
      </Card>

      <Card style={{ marginBottom: 12 }}>
        <SectionHeader title="Lash Profile" />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
          {[["Curl", client.curl], ["Length", client.length], ["Diameter", client.diameter], ["Style", client.style]].map(([label, val]) => (
            <div key={label} style={{ background: C.roseLight, borderRadius: 10, padding: "8px 12px" }}>
              <div style={{ fontSize: 10, color: C.grayLight, textTransform: "uppercase", letterSpacing: 0.5 }}>{label}</div>
              <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{val}</div>
            </div>
          ))}
        </div>
      </Card>

      {(client.allergies !== "None" || client.notes) && (
        <Card style={{ marginBottom: 12, background: client.allergies !== "None" ? C.redLight : C.white, border: client.allergies !== "None" ? `1px solid ${C.red}` : "none" }}>
          <SectionHeader title={client.allergies !== "None" ? "⚠ Allergies & Notes" : "Notes"} />
          {client.allergies !== "None" && <p style={{ fontSize: 13, color: C.red, fontWeight: 600, margin: "0 0 6px" }}>{client.allergies}</p>}
          {client.notes && <p style={{ fontSize: 13, color: C.charcoal, margin: 0 }}>{client.notes}</p>}
        </Card>
      )}

      <Card style={{ marginBottom: 12 }}>
        <SectionHeader title="Visit History" />
        <div style={{ display: "flex", gap: 10 }}>
          {[[client.visits, "Total Visits"], [`${client.avgInterval}d`, "Avg Interval"], [`${since}d`, "Since Last"]].map(([v, l]) => (
            <div key={l} style={{ flex: 1, textAlign: "center", padding: 10, background: C.blush, borderRadius: 10 }}>
              <div style={{ fontSize: 20, fontWeight: 700, color: C.charcoal }}>{v}</div>
              <div style={{ fontSize: 11, color: C.gray }}>{l}</div>
            </div>
          ))}
        </div>
      </Card>

      <Card>
        <SectionHeader title="Appointment History" />
        {appts.length === 0 ? (
          <p style={{ fontSize: 13, color: C.grayLight, textAlign: "center", padding: 16 }}>No appointments yet</p>
        ) : (
          appts.slice(0, 8).map((a) => (
            <div key={a.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 0", borderBottom: `1px solid ${C.grayBorder}` }}>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600, color: C.charcoal }}>{a.date}</div>
                <div style={{ fontSize: 12, color: C.gray }}>{a.serviceName}</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 13, fontWeight: 600 }}>{fmt(a.price)}</div>
                <StatusBadge status={a.status} />
              </div>
            </div>
          ))
        )}
      </Card>

      <BookAppointmentModal open={booking} onClose={() => setBooking(false)} presetClientId={client.id} />
    </div>
  );
}

export default function Clients({ selectedClientId, setSelectedClientId }) {
  const { data, actions } = useBloom();
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState(null);
  const [mode, setMode] = useState(null); // null | 'new' | 'edit'

  const withStatus = useMemo(
    () => data.clients.map((c) => ({ ...c, _status: clientStatus(c) })),
    [data.clients]
  );
  const counts = useMemo(() => {
    const c = { active: 0, lapsing: 0, lost: 0 };
    withStatus.forEach((x) => c[x._status]++);
    return c;
  }, [withStatus]);

  const selected = selectedClientId ? data.clients.find((c) => c.id === selectedClientId) : null;

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    return withStatus
      .filter((c) => (filter ? c._status === filter : true))
      .filter((c) =>
        q ? c.name.toLowerCase().includes(q) || c.phone.includes(q) || c.email.toLowerCase().includes(q) : true
      )
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [withStatus, search, filter]);

  if (mode === "new") {
    return (
      <ClientForm
        initial={EMPTY}
        title="New Client Intake"
        submitLabel="Add Client"
        onCancel={() => setMode(null)}
        onSubmit={(form) => {
          const created = actions.addClient(form);
          setMode(null);
          setSelectedClientId(created.id);
        }}
      />
    );
  }
  if (mode === "edit" && selected) {
    return (
      <ClientForm
        initial={{ ...EMPTY, ...selected }}
        title="Edit Client"
        submitLabel="Save Changes"
        onCancel={() => setMode(null)}
        onSubmit={(form) => {
          actions.updateClient(selected.id, form);
          setMode(null);
        }}
      />
    );
  }
  if (selected) {
    return (
      <ClientDetail
        client={selected}
        onBack={() => setSelectedClientId(null)}
        onEdit={() => setMode("edit")}
      />
    );
  }

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <PageTitle
        right={
          <button onClick={() => setMode("new")} style={{ display: "flex", alignItems: "center", gap: 4, background: C.rose, color: C.white, border: "none", borderRadius: 10, padding: "8px 14px", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
            <Icon d={Icons.plus} size={16} color={C.white} /> New
          </button>
        }
      >
        Clients
      </PageTitle>
      <SearchBar value={search} onChange={setSearch} placeholder="Search by name, phone, or email…" />

      <div style={{ display: "flex", gap: 8, marginBottom: 14, flexWrap: "wrap" }}>
        {[
          [`All (${data.clients.length})`, null],
          [`Active (${counts.active})`, "active"],
          [`Lapsing (${counts.lapsing})`, "lapsing"],
          [`Lost (${counts.lost})`, "lost"],
        ].map(([label, f]) => (
          <button
            key={label}
            onClick={() => setFilter(f)}
            style={{ padding: "6px 12px", borderRadius: 20, border: `1px solid ${filter === f ? C.rose : C.grayBorder}`, background: filter === f ? C.roseLight : C.white, color: filter === f ? C.rose : C.charcoal, fontSize: 12, fontWeight: filter === f ? 600 : 400, cursor: "pointer" }}
          >
            {label}
          </button>
        ))}
      </div>

      {filtered.map((c) => (
        <div key={c.id} onClick={() => setSelectedClientId(c.id)} style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 14px", background: C.white, borderRadius: 14, marginBottom: 8, boxShadow: "0 1px 3px rgba(0,0,0,0.04)", cursor: "pointer" }}>
          <Avatar name={c.name} />
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{c.name}</div>
            <div style={{ fontSize: 12, color: C.gray }}>{c.visits} visits · {fmt(c.ltv)} LTV</div>
          </div>
          <div style={{ textAlign: "right" }}>
            <StatusBadge status={c._status} />
            <div style={{ fontSize: 11, color: C.grayLight, marginTop: 2 }}>{daysAgo(c.lastVisit)}d ago</div>
          </div>
        </div>
      ))}
      {filtered.length === 0 && <p style={{ textAlign: "center", color: C.grayLight, padding: 30 }}>No clients found</p>}
    </div>
  );
}
