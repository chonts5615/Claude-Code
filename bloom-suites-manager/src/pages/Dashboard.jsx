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
import { Banners } from "./Banners";

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
    const expenses = Object.values(data.settings.monthlyExpenses).reduce((s, v) => s + v, 0);
    const net = totals.collected - expenses;
    const year = cur.slice(0, 4);
    const collectedYTD = data.ledger.filter((r) => r.paidDate && r.month.startsWith(year)).reduce((s, r) => s + r.amount, 0);
    const projectedAnnual = roll * 12;
    return { occ, totals, roll, trend, cur, collectRate, expenses, net, collectedYTD, projectedAnnual, year };
  }, [data]);

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 22, fontWeight: 700, color: C.charcoal, margin: "0 0 2px" }}>
          Good {new Date().getHours() < 12 ? "morning" : new Date().getHours() < 18 ? "afternoon" : "evening"}, {settings.ownerName}
        </h2>
        <p style={{ fontSize: 13, color: C.grayLight, margin: 0 }}>{longDate()}</p>
      </div>

      <Banners goTo={goTo} />

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
        <SectionHeader title={`This Month · ${monthLabel(m.cur).split(" ")[0]}`} action="Rent" onAction={() => goTo("rent")} />
        {[
          ["Rent collected", fmt(m.totals.collected), C.green],
          ["Still outstanding", fmt(m.totals.outstanding), m.totals.outstanding > 0 ? C.red : C.gray],
          ["Expenses", `(${fmt(m.expenses)})`, C.red],
        ].map(([label, val, color]) => (
          <div key={label} style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", fontSize: 13 }}>
            <span style={{ color: C.gray }}>{label}</span>
            <span style={{ fontWeight: 600, color }}>{val}</span>
          </div>
        ))}
        <div style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", fontSize: 14, borderTop: `2px solid ${C.gold}`, marginTop: 4, paddingTop: 8 }}>
          <span style={{ fontWeight: 700, color: C.charcoal }}>Net so far</span>
          <span style={{ fontWeight: 700, color: m.net >= 0 ? C.green : C.red }}>{fmt(m.net)}</span>
        </div>
        <p style={{ fontSize: 11, color: C.grayLight, margin: "6px 0 0" }}>Rent collected minus your monthly expenses (set in Settings).</p>
      </Card>

      <Card style={{ marginTop: 16 }}>
        <SectionHeader title={`This Year · ${m.year}`} />
        <div style={{ display: "flex", gap: 10 }}>
          <div style={{ flex: 1, textAlign: "center", padding: 12, background: C.greenLight, borderRadius: 12 }}>
            <div style={{ fontSize: 19, fontWeight: 700, color: C.green }}>{fmt(m.collectedYTD)}</div>
            <div style={{ fontSize: 11, color: C.green }}>Collected YTD</div>
          </div>
          <div style={{ flex: 1, textAlign: "center", padding: 12, background: C.goldLight, borderRadius: 12 }}>
            <div style={{ fontSize: 19, fontWeight: 700, color: C.gold }}>{fmt(m.projectedAnnual)}</div>
            <div style={{ fontSize: 11, color: C.gold }}>Projected annual</div>
          </div>
        </div>
        <p style={{ fontSize: 11, color: C.grayLight, margin: "8px 0 0" }}>Projected annual = current rent roll × 12 at full occupancy.</p>
      </Card>
    </div>
  );
}
