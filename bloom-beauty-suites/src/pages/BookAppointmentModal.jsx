// Reusable "book an appointment" sheet. Used from the Schedule page, a client's
// profile, and the empty-day prompt.
import { useState, useEffect } from "react";
import { useBloom } from "../store";
import { todayISO } from "../format";
import { C } from "../theme";
import { Modal, Field, Select, Input, Textarea, PrimaryButton } from "../ui";

// Working-day start slots (09:00–17:30, 30-min steps). The actual options are
// filtered per service so the visit ends by the 18:00 close.
const TIMES = [];
for (let h = 9; h < 18; h++) {
  for (const m of ["00", "30"]) TIMES.push(`${String(h).padStart(2, "0")}:${m}`);
}

export default function BookAppointmentModal({ open, onClose, presetClientId, presetDate }) {
  const { data, actions } = useBloom();
  const [form, setForm] = useState({
    clientId: "",
    serviceId: data.services[0]?.id || "",
    date: presetDate || todayISO(),
    time: "10:00",
    notes: "",
  });

  useEffect(() => {
    if (open) {
      setForm((f) => ({
        ...f,
        clientId: presetClientId ? String(presetClientId) : "",
        // Default to a service that's actually on the current menu.
        serviceId: data.services.some((s) => s.id === f.serviceId) ? f.serviceId : data.services[0]?.id || "",
        date: presetDate || todayISO(),
        // Don't carry last booking's notes into the next appointment.
        notes: "",
      }));
    }
  }, [open, presetClientId, presetDate, data.services]);

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  // Detect a time clash with an existing appointment on that day (overlap by
  // service duration), so the solo owner doesn't accidentally double-book a slot.
  const toMin = (t) => { const [h, m] = t.split(":").map(Number); return h * 60 + m; };
  const dur = data.services.find((s) => s.id === form.serviceId)?.duration || 60;
  // Only offer start times where the whole service fits before the 18:00 close.
  const timeOptions = TIMES.filter((t) => toMin(t) + dur <= 18 * 60);
  const canBook = form.clientId && form.serviceId && form.date && timeOptions.includes(form.time);
  const start = toMin(form.time);

  // If switching to a longer service makes the chosen time run past close, snap
  // to the latest slot that still fits.
  useEffect(() => {
    if (open && timeOptions.length && !timeOptions.includes(form.time)) {
      setForm((f) => ({ ...f, time: timeOptions[timeOptions.length - 1] }));
    }
  }, [open, form.serviceId, form.time, dur]);
  const conflict = data.appointments.find(
    (a) =>
      a.date === form.date &&
      (a.status === "scheduled" || a.status === "completed") &&
      start < toMin(a.time) + a.duration &&
      toMin(a.time) < start + dur
  );

  return (
    <Modal open={open} onClose={onClose} title="Book Appointment">
      <Field label="Client">
        <Select value={form.clientId} onChange={set("clientId")}>
          <option value="">Select a client…</option>
          {[...data.clients]
            .sort((a, b) => a.name.localeCompare(b.name))
            .map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
        </Select>
      </Field>
      <Field label="Service">
        <Select value={form.serviceId} onChange={set("serviceId")}>
          {data.services.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} — ${s.price}
            </option>
          ))}
        </Select>
      </Field>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <Field label="Date">
          <Input type="date" value={form.date} onChange={set("date")} />
        </Field>
        <Field label="Time">
          <Select value={form.time} onChange={set("time")}>
            {timeOptions.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </Select>
        </Field>
      </div>
      <Field label="Notes (optional)">
        <Textarea rows={2} value={form.notes} onChange={set("notes")} placeholder="Anything to remember for this visit…" />
      </Field>
      {conflict && (
        <div style={{ background: C.amberLight, border: `1px solid ${C.amber}`, borderRadius: 10, padding: "8px 12px", marginBottom: 12, fontSize: 12, color: C.charcoal }}>
          ⚠ This overlaps <strong>{conflict.clientName}</strong> at {conflict.time}. Pick a different time.
        </div>
      )}
      <PrimaryButton
        disabled={!canBook || !!conflict}
        onClick={() => {
          const created = actions.bookAppointment({ ...form, clientId: Number(form.clientId) });
          if (created) onClose();
        }}
      >
        Book Appointment
      </PrimaryButton>
    </Modal>
  );
}
