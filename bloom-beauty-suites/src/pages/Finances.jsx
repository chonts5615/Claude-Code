// Finances: a plain-language monthly snapshot driven off real logged revenue,
// plus a tax set-aside helper and per-service performance.
import { useMemo } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useBloom } from "../store";
import { completedAppointments, revenueOf } from "../automation";
import { C } from "../theme";
import { fmt, todayISO, addDays, monthName } from "../format";
import { Card, KPI, SectionHeader } from "../ui";

export default function Finances() {
  const { data } = useBloom();
  const { settings } = data;

  const f = useMemo(() => {
    const completed = completedAppointments(data);
    const today = todayISO();
    const weekRev = revenueOf(completed.filter((a) => a.date >= addDays(today, -6) && a.date <= today));

    const exp = settings.monthlyExpenses;
    const totalExp = Object.values(exp).reduce((s, v) => s + v, 0);
    const estRev = Math.round(weekRev * 4.3);
    const estCogs = Math.round(estRev * settings.cogsRate);
    const estProfit = estRev - estCogs - totalExp;
    const margin = estRev > 0 ? ((estProfit / estRev) * 100).toFixed(1) : "0";

    const months = {};
    completed.forEach((a) => {
      const key = a.date.substring(0, 7);
      months[key] = (months[key] || 0) + a.price;
    });
    const trend = Object.entries(months)
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([k, v]) => ({ month: monthName(parseInt(k.split("-")[1], 10) - 1), revenue: v }));

    // Build from completed appointments (not just the current menu) so a service
    // the owner later removed still shows the revenue it earned. Rows whose
    // current service is an add-on ("Other") are hidden, matching the prior view.
    const perfMap = {};
    completed.forEach((a) => {
      if (!perfMap[a.serviceId]) {
        const svc = data.services.find((s) => s.id === a.serviceId);
        if (svc && svc.category === "Other") return; // skip add-ons still on the menu
        perfMap[a.serviceId] = { id: a.serviceId, name: svc ? svc.name : a.serviceName, listPrice: svc ? svc.price : null, removed: !svc, count: 0, rev: 0 };
      }
      const row = perfMap[a.serviceId];
      if (row) { row.count += 1; row.rev += a.price; }
    });
    const perService = Object.values(perfMap).sort((a, b) => b.rev - a.rev);

    return { weekRev, estRev, estCogs, estProfit, margin, totalExp, exp, trend, perService };
  }, [data, settings]);

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: "0 0 16px" }}>Finances</h2>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Monthly Estimate (from this week)" />
        <div style={{ display: "flex", gap: 10, marginBottom: 12 }}>
          <KPI label="Est. Revenue" value={fmt(f.estRev)} />
          <KPI label="Est. Profit" value={fmt(f.estProfit)} sub={`${f.margin}% margin`} trend={Number(f.margin) > 60 ? "up" : "down"} />
        </div>
        <div style={{ background: C.blush, borderRadius: 12, padding: 14 }}>
          <div style={{ fontSize: 12, color: C.charcoal, marginBottom: 8 }}><strong>Monthly Breakdown</strong></div>
          {[
            ["Gross Revenue", f.estRev],
            ["Product (COGS)", -f.estCogs],
            ["Rent", -f.exp.rent],
            ["Supplies", -f.exp.supplies],
            ["Tech/Phone/Internet", -f.exp.tech],
            ["Insurance", -f.exp.insurance],
            ["Banking/Other", -(f.exp.banking + f.exp.other)],
          ].map(([label, val]) => (
            <div key={label} style={{ display: "flex", justifyContent: "space-between", padding: "4px 0", fontSize: 13 }}>
              <span style={{ color: C.gray }}>{label}</span>
              <span style={{ color: val < 0 ? C.red : C.charcoal, fontWeight: 600 }}>
                {val < 0 ? `(${fmt(-val)})` : fmt(val)}
              </span>
            </div>
          ))}
          <div style={{ borderTop: `2px solid ${C.rose}`, marginTop: 8, paddingTop: 8, display: "flex", justifyContent: "space-between", fontSize: 14, fontWeight: 700 }}>
            <span>Net Profit</span>
            <span style={{ color: f.estProfit > 0 ? C.green : C.red }}>{fmt(f.estProfit)}</span>
          </div>
        </div>
        <p style={{ fontSize: 11, color: C.grayLight, marginTop: 8 }}>
          Estimated by projecting this week's logged revenue across the month. Adjust expenses in Settings.
        </p>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Revenue Trend" />
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={f.trend} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke={C.grayBorder} />
            <XAxis dataKey="month" fontSize={11} stroke={C.grayLight} />
            <YAxis fontSize={11} stroke={C.grayLight} tickFormatter={(v) => `$${Math.round(v / 1000)}k`} />
            <Tooltip formatter={(v) => [fmt(v), "Revenue"]} contentStyle={{ borderRadius: 8, border: "none", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }} />
            <Bar dataKey="revenue" fill={C.rose} radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Tax Reserve" />
        <div style={{ display: "flex", gap: 10 }}>
          <div style={{ flex: 1, background: C.amberLight, borderRadius: 10, padding: 12, textAlign: "center" }}>
            <div style={{ fontSize: 18, fontWeight: 700, color: C.amber }}>{fmt(Math.round(Math.max(0, f.estProfit) * 0.141))}</div>
            <div style={{ fontSize: 11, color: C.amber }}>SE Tax (14.1%)</div>
          </div>
          <div style={{ flex: 1, background: C.roseLight, borderRadius: 10, padding: 12, textAlign: "center" }}>
            <div style={{ fontSize: 18, fontWeight: 700, color: C.rose }}>{fmt(Math.round(Math.max(0, f.estProfit) * settings.taxReserveRate))}</div>
            <div style={{ fontSize: 11, color: C.rose }}>Total to Set Aside</div>
          </div>
        </div>
        <p style={{ fontSize: 11, color: C.grayLight, marginTop: 8 }}>
          Set aside {Math.round(settings.taxReserveRate * 100)}% of net profit for combined SE tax + federal + state.
        </p>
      </Card>

      <Card>
        <SectionHeader title="Service Performance" />
        {f.perService.length === 0 ? (
          <p style={{ fontSize: 13, color: C.grayLight, textAlign: "center", padding: 12 }}>No completed services yet</p>
        ) : (
          f.perService.map((s) => (
            <div key={s.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "8px 0", borderBottom: `1px solid ${C.grayBorder}` }}>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600, color: C.charcoal }}>{s.name}{s.removed ? " (removed)" : ""}</div>
                <div style={{ fontSize: 11, color: C.gray }}>{s.count} bookings{s.listPrice != null ? ` · ${fmt(s.listPrice)} list` : ""}</div>
              </div>
              <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{fmt(s.rev)}</div>
            </div>
          ))
        )}
      </Card>
    </div>
  );
}
