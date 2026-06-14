// Reusable "book an appointment" sheet. Used from the Schedule page, a client's
// profile, and the empty-day prompt.
import { useState, useEffect } from "react";
import { useBloom } from "../store";
import { todayISO } from "../format";
import { Modal, Field, Select, Input, Textarea, PrimaryButton } from "../ui";

const TIMES = [];
for (let h = 8; h <= 19; h++) {
  for (const m of ["00", "30"]) TIMES.push(`${String(h).padStart(2, "0")}:${m}`);
}

export default function BookAppointmentModal({ open, onClose, presetClientId, presetDate }) {
  const { data, actions } = useBloom();
  const [form, setForm] = useState({
    clientId: "",
    serviceId: "classic-fill",
    date: presetDate || todayISO(),
    time: "10:00",
    notes: "",
  });

  useEffect(() => {
    if (open) {
      setForm((f) => ({
        ...f,
        clientId: presetClientId ? String(presetClientId) : "",
        date: presetDate || todayISO(),
      }));
    }
  }, [open, presetClientId, presetDate]);

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));
  const canBook = form.clientId && form.serviceId && form.date && form.time;

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
            {TIMES.map((t) => (
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
      <PrimaryButton
        disabled={!canBook}
        onClick={() => {
          actions.bookAppointment({ ...form, clientId: Number(form.clientId) });
          onClose();
        }}
      >
        Book Appointment
      </PrimaryButton>
    </Modal>
  );
}
