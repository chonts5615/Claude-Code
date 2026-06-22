// Home screen: the day at a glance. Leads with the automated Action Center so
// the owner immediately sees what to do, then the key numbers and charts.
import { useMemo } from "react";
import {
  AreaChart, Area, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import { useBloom } from "../store";
import { clientStatus, completedAppointments, revenueOf } from "../automation";
import { C, PIE_COLORS } from "../theme";
import { fmt, todayISO, addDays, dayName, longDate } from "../format";
import { Card, KPI, SectionHeader, StatusBadge } from "../ui";
import ActionCenter from "./ActionCenter";
import { Banners } from "./Banners";

export default function Dashboard({ onOpenClient, goTo }) {
  const { data } = useBloom();
  const { clients, appointments, settings } = data;

  const m = useMemo(() => {
    const completed = completedAppointments(data);
    const today = todayISO();
    const weekStart = addDays(today, -6);
    const prevStart = addDays(today, -13);
    const prevEnd = addDays(today, -7);

    const inRange = (a, s, e) => a.date >= s && a.date <= e;
    const thisWeek = completed.filter((a) => inRange(a, weekStart, today));
    const lastWeek = completed.filter((a) => inRange(a, prevStart, prevEnd));
    const thisRev = revenueOf(thisWeek);
    const lastRev = revenueOf(lastWeek);

    const dailyRev = [];
    for (let i = 6; i >= 0; i--) {
      const d = addDays(today, -i);
      dailyRev.push({ day: dayName(d), revenue: revenueOf(completed.filter((a) => a.date === d)) });
    }

    const mix = {};
    completed.forEach((a) => {
      const svc = data.services.find((s) => s.id === a.serviceId);
      const cat = svc ? svc.category : "Other";
      mix[cat] = (mix[cat] || 0) + a.price;
    });

    const health = { active: 0, lapsing: 0, lost: 0 };
    clients.forEach((c) => health[clientStatus(c)]++);

    const rebookRate = completed.length
      ? Math.round((completed.filter((a) => a.rebooked).length / completed.length) * 100)
      : 0;

    return {
      thisRev,
      weekChange: lastRev > 0 ? Math.round(((thisRev - lastRev) / lastRev) * 100) : 0,
      avgTicket: thisWeek.length ? Math.round(thisRev / thisWeek.length) : 0,
      apptCount: thisWeek.length,
      todayAll: appointments.filter((a) => a.date === today),
      todayScheduled: appointments.filter((a) => a.date === today && a.status === "scheduled"),
      dailyRev,
      mix: Object.entries(mix).map(([name, value]) => ({ name, value })),
      health,
      rebookRate,
    };
  }, [data, clients, appointments]);

  const todayList = appointments
    .filter((a) => a.date === todayISO())
    .sort((a, b) => a.time.localeCompare(b.time));

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <div style={{ marginBottom: 16 }}>
        <h2 style={{ fontSize: 22, fontWeight: 700, color: C.charcoal, margin: "0 0 2px" }}>
          Good {new Date().getHours() < 12 ? "morning" : new Date().getHours() < 18 ? "afternoon" : "evening"}, {settings.ownerName}
        </h2>
        <p style={{ fontSize: 13, color: C.grayLight, margin: 0 }}>{longDate()}</p>
      </div>

      <Banners goTo={goTo} />

      {/* Automated daily task list */}
      <ActionCenter onOpenClient={onOpenClient} />

      {/* KPIs */}
      <div style={{ display: "flex", gap: 10, marginBottom: 10 }}>
        <KPI label="This Week" value={fmt(m.thisRev)} sub={`${m.weekChange > 0 ? "+" : ""}${m.weekChange}% vs last week`} trend={m.weekChange >= 0 ? "up" : "down"} />
        <KPI label="Avg Ticket" value={fmt(m.avgTicket)} sub="per appointment" />
      </div>
      <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
        <KPI label="Appointments" value={m.apptCount} sub={`${m.todayAll.length} today`} />
        <KPI label="Rebook Rate" value={`${m.rebookRate}%`} sub={`${m.health.active} active clients`} trend={m.rebookRate >= 70 ? "up" : "down"} />
      </div>

      {/* Weekly revenue */}
      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="This Week's Revenue" />
        <ResponsiveContainer width="100%" height={160}>
          <AreaChart data={m.dailyRev} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="roseGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={C.rose} stopOpacity={0.3} />
                <stop offset="95%" stopColor={C.rose} stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke={C.grayBorder} />
            <XAxis dataKey="day" fontSize={11} stroke={C.grayLight} />
            <YAxis fontSize={11} stroke={C.grayLight} tickFormatter={(v) => `$${v}`} />
            <Tooltip formatter={(v) => [fmt(v), "Revenue"]} contentStyle={{ borderRadius: 8, border: "none", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }} />
            <Area type="monotone" dataKey="revenue" stroke={C.rose} fill="url(#roseGrad)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </Card>

      {/* Today's schedule preview */}
      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Today's Schedule" action="View All" onAction={() => goTo("schedule")} />
        {todayList.length === 0 ? (
          <p style={{ fontSize: 13, color: C.grayLight, textAlign: "center", padding: 20 }}>No appointments today</p>
        ) : (
          todayList.slice(0, 4).map((a) => (
            <div key={a.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 0", borderBottom: `1px solid ${C.grayBorder}` }}>
              <div style={{ width: 48, textAlign: "center", fontSize: 14, fontWeight: 700, color: C.charcoal }}>{a.time}</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{a.clientName}</div>
                <div style={{ fontSize: 12, color: C.gray }}>{a.serviceName}</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{fmt(a.price)}</div>
                <StatusBadge status={a.status} />
              </div>
            </div>
          ))
        )}
      </Card>

      {/* Client health */}
      <Card style={{ marginBottom: 16 }}>
        <SectionHeader title="Client Health" action="View" onAction={() => goTo("clients")} />
        <div style={{ display: "flex", gap: 10 }}>
          {[
            ["Active", m.health.active, C.green, C.greenLight],
            ["Lapsing", m.health.lapsing, C.amber, C.amberLight],
            ["Lost", m.health.lost, C.red, C.redLight],
          ].map(([label, val, color, bg]) => (
            <div key={label} style={{ flex: 1, textAlign: "center", padding: 12, background: bg, borderRadius: 12 }}>
              <div style={{ fontSize: 22, fontWeight: 700, color }}>{val}</div>
              <div style={{ fontSize: 11, color }}>{label}</div>
            </div>
          ))}
        </div>
      </Card>

      {/* Service mix */}
      <Card>
        <SectionHeader title="Revenue by Service Type" />
        <div style={{ display: "flex", alignItems: "center" }}>
          <ResponsiveContainer width="50%" height={140}>
            <PieChart>
              <Pie data={m.mix} dataKey="value" cx="50%" cy="50%" outerRadius={55} innerRadius={30}>
                {m.mix.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          <div style={{ flex: 1, paddingLeft: 10 }}>
            {m.mix.map((s, i) => (
              <div key={s.name} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                <div style={{ width: 10, height: 10, borderRadius: 3, background: PIE_COLORS[i % PIE_COLORS.length] }} />
                <span style={{ fontSize: 12, color: C.charcoal }}>{s.name}</span>
                <span style={{ fontSize: 12, color: C.grayLight, marginLeft: "auto" }}>{fmt(s.value)}</span>
              </div>
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
}
