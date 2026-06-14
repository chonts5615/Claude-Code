// Home screen: the rental business at a glance, led by the automated Action
// Center, then occupancy and rent numbers.
import { useMemo } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useBloom } from "../store";
import { occupancy, rentRoll, monthTotals } from "../automation";
import { C } from "../theme";
import { fmt, longDate, monthKey, monthLabel, monthShortLabel, addMonths } from "../format";
import { Card, KPI, SectionHeader } from "../ui";
import ActionCenter from "./ActionCenter";

export default function Dashboard({ onOpenTenant, goTo }) {
  const { data } = useBloom();
  const { settings } = data;

  const m = useMemo(() => {
    const occ = occupancy(data);
    const cur = monthKey();
    const totals = monthTotals(data, cur);
    const roll = rentRoll(data);

    const trend = [];
    for (let i = 4; i >= 0; i--) {
      const mk = addMonths(cur, -i);
      trend.push({ month: monthShortLabel(mk), collected: monthTotals(data, mk).collected });
    }
    const collectRate = totals.billed ? Math.round((totals.collected / totals.billed) * 100) : 0;
    return { occ, totals, roll, trend, cur, collectRate };
  }, [data]);

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 22, fontWeight: 700, color: C.charcoal, margin: "0 0 2px" }}>
          Good {new Date().getHours() < 12 ? "morning" : new Date().getHours() < 18 ? "afternoon" : "evening"}, {settings.ownerName}
        </h2>
        <p style={{ fontSize: 13, color: C.grayLight, margin: 0 }}>{longDate()}</p>
      </div>

      <ActionCenter onOpenTenant={onOpenTenant} goTo={goTo} />

      <div style={{ display: "flex", gap: 10, marginBottom: 10 }}>
        <KPI label="Occupancy" value={`${m.occ.rate}%`} sub={`${m.occ.occupied + m.occ.notice} of ${m.occ.total} suites filled`} trend={m.occ.rate >= 80 ? "up" : "down"} />
        <KPI label="Rent Roll" value={fmt(m.roll)} sub="potential / month" />
      </div>
      <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
        <KPI label={`Collected (${monthLabel(m.cur).split(" ")[0]})`} value={fmt(m.totals.collected)} sub={`${m.collectRate}% of billed`} trend={m.collectRate >= 80 ? "up" : "down"} />
        <KPI label="Outstanding" value={fmt(m.totals.outstanding)} sub="still owed" trend={m.totals.outstanding > 0 ? "down" : "up"} />
      </div>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Rent Collected by Month" />
        <ResponsiveContainer width="100%" height={170}>
          <BarChart data={m.trend} margin={{ top: 5, right: 5, left: -18, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke={C.grayBorder} />
            <XAxis dataKey="month" fontSize={11} stroke={C.grayLight} />
            <YAxis fontSize={11} stroke={C.grayLight} tickFormatter={(v) => `$${Math.round(v / 1000)}k`} />
            <Tooltip formatter={(v) => [fmt(v), "Collected"]} contentStyle={{ borderRadius: 8, border: "none", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }} />
            <Bar dataKey="collected" fill={C.gold} radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Suites" action="View" onAction={() => goTo("suites")} />
        <div style={{ display: "flex", gap: 10 }}>
          {[
            ["Occupied", m.occ.occupied, C.green, C.greenLight],
            ["Notice", m.occ.notice, C.amber, C.amberLight],
            ["Vacant", m.occ.vacant, C.red, C.redLight],
          ].map(([label, val, color, bg]) => (
            <div key={label} style={{ flex: 1, textAlign: "center", padding: 12, background: bg, borderRadius: 12 }}>
              <div style={{ fontSize: 22, fontWeight: 700, color }}>{val}</div>
              <div style={{ fontSize: 11, color }}>{label}</div>
            </div>
          ))}
        </div>
      </Card>

      <Card>
        <SectionHeader title="This Month" action="Rent" onAction={() => goTo("rent")} />
        <div style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", fontSize: 13 }}>
          <span style={{ color: C.gray }}>Billed ({monthLabel(m.cur)})</span>
          <span style={{ fontWeight: 600, color: C.charcoal }}>{fmt(m.totals.billed)}</span>
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", fontSize: 13 }}>
          <span style={{ color: C.gray }}>Collected</span>
          <span style={{ fontWeight: 600, color: C.green }}>{fmt(m.totals.collected)}</span>
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", fontSize: 13, borderTop: `2px solid ${C.rose}`, marginTop: 4, paddingTop: 8 }}>
          <span style={{ fontWeight: 700, color: C.charcoal }}>Outstanding</span>
          <span style={{ fontWeight: 700, color: m.totals.outstanding > 0 ? C.red : C.green }}>{fmt(m.totals.outstanding)}</span>
        </div>
      </Card>
    </div>
  );
}
