// Rent: the monthly rent roll. See who has paid, mark payments, and bill a new
// month in one tap.
import { useMemo, useState } from "react";
import { useBloom } from "../store";
import { rentStatus, tenantById, monthTotals } from "../automation";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { fmt, monthKey, monthLabel, addMonths } from "../format";
import { Card, SectionHeader, StatusBadge } from "../ui";

export default function Rent() {
  const { data, actions } = useBloom();
  const [mk, setMk] = useState(monthKey());

  const view = useMemo(() => {
    const totals = monthTotals(data, mk);
    const rows = totals.rows
      .map((r) => ({ ...r, tenant: tenantById(data.tenants, r.tenantId), status: rentStatus(r, data.settings) }))
      .filter((r) => r.tenant)
      .sort((a, b) => (a.paidDate ? 1 : 0) - (b.paidDate ? 1 : 0) || a.tenant.name.localeCompare(b.tenant.name));
    const activeUnbilled = data.tenants.filter((t) => t.status !== "past" && !totals.rows.some((r) => r.tenantId === t.id));
    return { totals, rows, activeUnbilled };
  }, [data, mk]);

  const isCurrent = mk === monthKey();

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: "0 0 16px" }}>Rent</h2>

      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
        <button onClick={() => setMk(addMonths(mk, -1))} style={navBtn}><Icon d={Icons.back} size={18} color={C.rose} /></button>
        <div style={{ fontSize: 16, fontWeight: 700, color: C.charcoal }}>{monthLabel(mk)}</div>
        <button onClick={() => setMk(addMonths(mk, 1))} style={{ ...navBtn, transform: "rotate(180deg)" }}><Icon d={Icons.back} size={18} color={C.rose} /></button>
      </div>

      <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
        {[
          ["Collected", view.totals.collected, C.green, C.greenLight],
          ["Outstanding", view.totals.outstanding, view.totals.outstanding > 0 ? C.red : C.green, view.totals.outstanding > 0 ? C.redLight : C.greenLight],
          ["Billed", view.totals.billed, C.charcoal, C.blush],
        ].map(([label, val, color, bg]) => (
          <div key={label} style={{ flex: 1, textAlign: "center", padding: 12, background: bg, borderRadius: 12 }}>
            <div style={{ fontSize: 17, fontWeight: 700, color }}>{fmt(val)}</div>
            <div style={{ fontSize: 11, color }}>{label}</div>
          </div>
        ))}
      </div>

      {view.activeUnbilled.length > 0 && (
        <button onClick={() => actions.generateRentForMonth(mk)} style={{ width: "100%", padding: 12, marginBottom: 16, borderRadius: 12, border: `1px dashed ${C.rose}`, background: C.roseLight, color: C.rose, fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
          + Bill {view.activeUnbilled.length} tenant{view.activeUnbilled.length === 1 ? "" : "s"} for {monthLabel(mk).split(" ")[0]}
        </button>
      )}

      <Card>
        <SectionHeader title={isCurrent ? "This Month" : "Rent Roll"} />
        {view.rows.length === 0 ? (
          <p style={{ fontSize: 13, color: C.grayLight, textAlign: "center", padding: 16 }}>No rent billed for this month yet</p>
        ) : (
          view.rows.map((r) => (
            <div key={r.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 0", borderBottom: `1px solid ${C.grayBorder}` }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{r.tenant.name}</div>
                <div style={{ fontSize: 12, color: C.gray }}>{r.tenant.suite} · {fmt(r.amount)}</div>
              </div>
              {r.paidDate ? (
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <StatusBadge status="paid" />
                  <button onClick={() => actions.markRentUnpaid(r.id)} style={{ background: "none", border: "none", color: C.grayLight, fontSize: 11, cursor: "pointer", textDecoration: "underline" }}>undo</button>
                </div>
              ) : (
                <button onClick={() => actions.markRentPaid(r.id)} style={{ padding: "8px 14px", borderRadius: 9, border: "none", background: r.status === "late" ? C.red : C.rose, color: C.white, fontSize: 12, fontWeight: 700, cursor: "pointer" }}>
                  {r.status === "late" ? "Late · Mark Paid" : "Mark Paid"}
                </button>
              )}
            </div>
          ))
        )}
      </Card>
    </div>
  );
}
const navBtn = { width: 40, height: 40, borderRadius: 20, border: `1px solid ${C.grayBorder}`, background: C.white, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" };
