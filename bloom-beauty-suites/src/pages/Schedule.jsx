// Schedule: pick a day, see the timeline, and manage each appointment. Marking
// a visit complete here is what automatically updates the client's stats.
import { useState } from "react";
import { useBloom } from "../store";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { fmt, todayISO, addDays, dayName } from "../format";
import { StatusBadge, EmptyState } from "../ui";
import BookAppointmentModal from "./BookAppointmentModal";

const dotColor = (status) =>
  status === "completed" ? C.green : status === "no-show" ? C.red : status === "late-cancel" ? C.amber : C.rose;

const MiniBtn = ({ children, onClick, color = C.rose, solid }) => (
  <button
    onClick={onClick}
    style={{ padding: "6px 10px", borderRadius: 8, border: solid ? "none" : `1px solid ${color}`, background: solid ? color : C.white, color: solid ? C.white : color, fontSize: 12, fontWeight: 600, cursor: "pointer" }}
  >
    {children}
  </button>
);

export default function Schedule() {
  const { data, actions } = useBloom();
  const [scheduleDate, setScheduleDate] = useState(todayISO());
  const [booking, setBooking] = useState(false);

  // Strip follows the selected day so any future date (e.g. a cadence-based
  // rebook weeks out) is reachable by stepping or via the date picker.
  const dates = [];
  for (let i = -3; i <= 10; i++) dates.push(addDays(scheduleDate, i));

  const dayAppts = data.appointments
    .filter((a) => a.date === scheduleDate)
    .sort((a, b) => a.time.localeCompare(b.time));

  return (
    <div style={{ padding: "16px 16px 100px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: 0 }}>Schedule</h2>
        <button onClick={() => setBooking(true)} style={{ display: "flex", alignItems: "center", gap: 4, background: C.rose, color: C.white, border: "none", borderRadius: 10, padding: "8px 14px", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
          <Icon d={Icons.plus} size={16} color={C.white} /> Book
        </button>
      </div>

      {/* Jump to any date (rebooks can land weeks out) */}
      <div style={{ display: "flex", gap: 8, marginBottom: 12, alignItems: "center" }}>
        <input type="date" value={scheduleDate} onChange={(e) => e.target.value && setScheduleDate(e.target.value)} style={{ flex: 1, padding: "9px 12px", borderRadius: 10, border: `1px solid ${C.grayBorder}`, fontSize: 14, background: C.white, color: C.charcoal, outline: "none" }} />
        <button onClick={() => setScheduleDate(todayISO())} style={{ padding: "9px 14px", borderRadius: 10, border: `1px solid ${C.rose}`, background: C.roseLight, color: C.rose, fontSize: 13, fontWeight: 600, cursor: "pointer", whiteSpace: "nowrap" }}>Today</button>
      </div>

      <div style={{ display: "flex", gap: 6, overflowX: "auto", marginBottom: 16, paddingBottom: 4 }}>
        {dates.map((d) => {
          const active = d === scheduleDate;
          const isToday = d === todayISO();
          const dt = new Date(d + "T12:00:00");
          const count = data.appointments.filter((a) => a.date === d).length;
          return (
            <button
              key={d}
              onClick={() => setScheduleDate(d)}
              style={{ minWidth: 52, padding: "8px 6px", borderRadius: 12, border: active ? `2px solid ${C.rose}` : `1px solid ${isToday ? C.gold : C.grayBorder}`, background: active ? C.roseLight : C.white, cursor: "pointer", textAlign: "center", flexShrink: 0 }}
            >
              <div style={{ fontSize: 10, color: C.grayLight }}>{dayName(d)}</div>
              <div style={{ fontSize: 18, fontWeight: 700, color: active ? C.rose : C.charcoal }}>{dt.getDate()}</div>
              <div style={{ fontSize: 10, color: active ? C.rose : C.gray, minHeight: 13 }}>{count > 0 ? count : ""}</div>
            </button>
          );
        })}
      </div>

      <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
        {[
          [dayAppts.length, "Appointments"],
          // Revenue excludes no-shows / late-cancels (matches Finances, which
          // only counts completed/expected visits as earned).
          [fmt(dayAppts.filter((a) => a.status !== "no-show" && a.status !== "late-cancel").reduce((s, a) => s + a.price, 0)), "Revenue"],
          [`${dayAppts.reduce((s, a) => s + a.duration, 0)}m`, "Booked Time"],
        ].map(([v, l]) => (
          <div key={l} style={{ flex: 1, background: C.white, borderRadius: 12, padding: 12, textAlign: "center", boxShadow: "0 1px 3px rgba(0,0,0,0.04)" }}>
            <div style={{ fontSize: 20, fontWeight: 700, color: C.charcoal }}>{v}</div>
            <div style={{ fontSize: 11, color: C.grayLight }}>{l}</div>
          </div>
        ))}
      </div>

      {dayAppts.length === 0 ? (
        <EmptyState text="No appointments on this day" />
      ) : (
        dayAppts.map((a, i) => (
          <div key={a.id} style={{ display: "flex", gap: 14, marginBottom: 4 }}>
            <div style={{ width: 50, textAlign: "right", paddingTop: 14 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: C.charcoal }}>{a.time}</div>
              <div style={{ fontSize: 11, color: C.grayLight }}>{a.duration}m</div>
            </div>
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
              <div style={{ width: 12, height: 12, borderRadius: 6, background: dotColor(a.status), border: `2px solid ${C.white}`, boxShadow: `0 0 0 2px ${dotColor(a.status)}`, marginTop: 16 }} />
              {i < dayAppts.length - 1 && <div style={{ width: 2, flex: 1, background: C.grayBorder, minHeight: 40 }} />}
            </div>
            <div style={{ flex: 1, background: C.white, borderRadius: 14, padding: "12px 14px", boxShadow: "0 1px 3px rgba(0,0,0,0.04)", marginBottom: 8 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{a.clientName}</div>
                  <div style={{ fontSize: 12, color: C.gray }}>{a.serviceName}</div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontSize: 14, fontWeight: 600, color: C.charcoal }}>{fmt(a.price)}</div>
                  <StatusBadge status={a.status} />
                </div>
              </div>

              {a.status === "scheduled" && (
                <div style={{ display: "flex", gap: 8, marginTop: 10, flexWrap: "wrap" }}>
                  <MiniBtn solid onClick={() => actions.completeAppointment(a.id)}>✓ Complete</MiniBtn>
                  <MiniBtn color={C.amber} onClick={() => actions.setAppointmentStatus(a.id, "no-show")}>No-show</MiniBtn>
                  <MiniBtn color={C.gray} onClick={() => actions.deleteAppointment(a.id)}>Cancel</MiniBtn>
                </div>
              )}

              {a.status === "completed" && (
                <div style={{ marginTop: 8, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ fontSize: 12, color: a.rebooked ? C.green : C.amber }}>
                    {a.rebooked ? "✓ Rebooked" : "○ Not yet rebooked"}
                  </span>
                  {!a.rebooked && (
                    <MiniBtn onClick={() => actions.rebookClient(a.clientId, { serviceId: a.serviceId, fromApptId: a.id })}>
                      Rebook
                    </MiniBtn>
                  )}
                </div>
              )}
            </div>
          </div>
        ))
      )}

      <BookAppointmentModal open={booking} onClose={() => setBooking(false)} presetDate={scheduleDate} />
    </div>
  );
}
