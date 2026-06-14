// Suites: a status board of every suite, with a detail view showing the current
// tenant, rent, and any open maintenance.
import { useState } from "react";
import { useBloom } from "../store";
import { suiteStatus, tenantById, daysUntil } from "../automation";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { fmt } from "../format";
import { Card, StatusBadge, BackButton, SectionHeader, Avatar, Field, Input } from "../ui";

const STATUS_COLOR = { occupied: C.green, notice: C.amber, vacant: C.red };

function SuiteDetail({ suite, onBack, onOpenTenant }) {
  const { data, actions } = useBloom();
  const status = suiteStatus(suite, data.tenants);
  const tenant = tenantById(data.tenants, suite.tenantId);
  const tickets = data.maintenance.filter((m) => m.suiteId === suite.id && m.status !== "done");

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <BackButton onClick={onBack} />
      <Card style={{ padding: 20, marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <h2 style={{ fontSize: 22, fontWeight: 700, color: C.charcoal, margin: "0 0 4px" }}>{suite.name}</h2>
            <div style={{ fontSize: 13, color: C.gray }}>{suite.size}</div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 20, fontWeight: 700, color: C.gold }}>{fmt(suite.rent)}</div>
            <div style={{ fontSize: 11, color: C.grayLight }}>per month</div>
            <div style={{ marginTop: 6 }}><StatusBadge status={status} /></div>
          </div>
        </div>
      </Card>

      {tenant ? (
        <Card style={{ marginBottom: 16 }}>
          <SectionHeader title="Current Tenant" />
          <div onClick={() => onOpenTenant(tenant)} style={{ display: "flex", alignItems: "center", gap: 12, cursor: "pointer" }}>
            <Avatar name={tenant.name} />
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 15, fontWeight: 600, color: C.charcoal }}>{tenant.name}</div>
              <div style={{ fontSize: 12, color: C.gray }}>{tenant.profession} · {tenant.business}</div>
              <div style={{ fontSize: 11, color: C.grayLight, marginTop: 2 }}>Lease ends {tenant.leaseEnd} ({daysUntil(tenant.leaseEnd)} days)</div>
            </div>
            <Icon d={Icons.chevRight} size={18} color={C.grayLight} />
          </div>
        </Card>
      ) : (
        <Card style={{ marginBottom: 16, background: C.redLight, border: `1px solid ${C.red}` }}>
          <div style={{ fontSize: 14, fontWeight: 600, color: C.red }}>Vacant — {fmt(suite.rent)}/mo of potential rent unfilled</div>
          <div style={{ fontSize: 12, color: C.charcoal, marginTop: 4 }}>Check the Applicants list under More to fill this suite.</div>
        </Card>
      )}

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Monthly Rent" />
        <Field label="Rent amount ($/month)">
          <Input type="number" inputMode="decimal" value={suite.rent} onChange={(e) => actions.updateSuite(suite.id, { rent: Number(e.target.value) || 0 })} />
        </Field>
        <p style={{ fontSize: 11, color: C.grayLight, margin: 0 }}>Changes save automatically. Existing tenant rent is unchanged.</p>
      </Card>

      <Card>
        <SectionHeader title="Open Maintenance" />
        {tickets.length === 0 ? (
          <p style={{ fontSize: 13, color: C.grayLight, textAlign: "center", padding: 12 }}>No open requests</p>
        ) : (
          tickets.map((m) => (
            <div key={m.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 0", borderBottom: `1px solid ${C.grayBorder}` }}>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600, color: C.charcoal }}>{m.title}</div>
                <div style={{ fontSize: 11, color: C.gray }}>{m.priority} priority · {m.status}</div>
              </div>
              <button onClick={() => actions.setMaintenanceStatus(m.id, "done")} style={{ padding: "6px 10px", borderRadius: 8, border: "none", background: C.green, color: C.white, fontSize: 12, fontWeight: 600, cursor: "pointer" }}>Done</button>
            </div>
          ))
        )}
      </Card>
    </div>
  );
}

export default function Suites({ onOpenTenant }) {
  const { data } = useBloom();
  const [selectedId, setSelectedId] = useState(null);
  const selected = selectedId ? data.suites.find((s) => s.id === selectedId) : null;

  if (selected) return <SuiteDetail suite={selected} onBack={() => setSelectedId(null)} onOpenTenant={onOpenTenant} />;

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: "0 0 16px" }}>Suites</h2>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        {data.suites.map((s) => {
          const status = suiteStatus(s, data.tenants);
          const tenant = tenantById(data.tenants, s.tenantId);
          return (
            <button key={s.id} onClick={() => setSelectedId(s.id)} style={{ textAlign: "left", background: C.white, border: `1px solid ${C.grayBorder}`, borderLeft: `4px solid ${STATUS_COLOR[status]}`, borderRadius: 14, padding: 14, cursor: "pointer", boxShadow: "0 1px 3px rgba(0,0,0,0.04)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                <span style={{ fontSize: 15, fontWeight: 700, color: C.charcoal }}>{s.name}</span>
                <StatusBadge status={status} />
              </div>
              <div style={{ fontSize: 12, color: C.gray, minHeight: 16 }}>{tenant ? tenant.name : "Available"}</div>
              <div style={{ fontSize: 13, fontWeight: 600, color: C.gold, marginTop: 4 }}>{fmt(s.rent)}/mo</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
