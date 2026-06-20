// The Action Center turns the automation engine's output into a one-tap daily
// to-do list for the suite owner.
import { useState } from "react";
import { useBloom } from "../store";
import { buildActionCenter, rentReminder, renewalMessage, applicantMessage } from "../automation";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { Card, copyText, smsHref } from "../ui";
import { fmt, monthLabel } from "../format";

const META = {
  billing: { icon: Icons.card, color: C.gold, bg: C.goldLight },
  rent: { icon: Icons.dollar, color: C.green, bg: C.greenLight },
  renewal: { icon: Icons.refresh, color: C.gold, bg: C.goldLight },
  vacancy: { icon: Icons.door, color: C.rose, bg: C.roseLight },
  maintenance: { icon: Icons.wrench, color: C.amber, bg: C.amberLight },
  applicant: { icon: Icons.users, color: C.rose, bg: C.roseLight },
};

const ActionBtn = ({ children, onClick, primary }) => (
  <button onClick={onClick} style={{ padding: "7px 12px", borderRadius: 9, border: primary ? "none" : `1px solid ${C.grayBorder}`, background: primary ? C.rose : C.white, color: primary ? C.white : C.charcoal, fontSize: 12, fontWeight: 600, cursor: "pointer", whiteSpace: "nowrap" }}>
    {children}
  </button>
);

// An <a> styled like ActionBtn that opens the phone's Messages app (sms:).
const TextBtn = ({ phone, body }) => (
  <a href={smsHref(phone, body)} style={{ padding: "7px 12px", borderRadius: 9, border: "none", background: C.rose, color: C.white, fontSize: 12, fontWeight: 600, textDecoration: "none", whiteSpace: "nowrap", display: "inline-flex", alignItems: "center", gap: 5 }}>
    <Icon d={Icons.phone} size={13} color={C.white} /> Text
  </a>
);

function Row({ meta, title, subtitle, onOpen, children }) {
  return (
    <div style={{ display: "flex", gap: 12, padding: "12px 0", borderBottom: `1px solid ${C.grayBorder}` }}>
      <div style={{ width: 34, height: 34, borderRadius: 10, background: meta.bg, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
        <Icon d={meta.icon} size={18} color={meta.color} />
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div onClick={onOpen} style={{ fontSize: 14, fontWeight: 600, color: C.charcoal, cursor: onOpen ? "pointer" : "default" }}>{title}</div>
        <div style={{ fontSize: 12, color: C.gray, marginBottom: 8 }}>{subtitle}</div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>{children}</div>
      </div>
    </div>
  );
}

export default function ActionCenter({ onOpenTenant, goTo }) {
  const { data, actions, notify } = useBloom();
  const { groups, total } = buildActionCenter(data);
  const [collapsed, setCollapsed] = useState(false);

  const copy = async (text) => {
    const ok = await copyText(text);
    notify(ok ? "Message copied" : "Couldn't copy");
  };

  if (total === 0) {
    return (
      <Card style={{ marginBottom: 16, textAlign: "center", padding: "26px 16px" }}>
        <div style={{ fontSize: 30, marginBottom: 6 }}>🌸</div>
        <div style={{ fontSize: 15, fontWeight: 700, color: C.charcoal }}>You're all caught up</div>
        <div style={{ fontSize: 13, color: C.gray, marginTop: 2 }}>No tasks need your attention right now.</div>
      </Card>
    );
  }

  return (
    <Card style={{ marginBottom: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: collapsed ? 0 : 6 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <h3 style={{ fontSize: 16, fontWeight: 700, color: C.charcoal, margin: 0 }}>Today's To-Dos</h3>
          <span style={{ background: C.rose, color: C.white, fontSize: 12, fontWeight: 700, borderRadius: 12, padding: "1px 8px" }}>{total}</span>
        </div>
        <button onClick={() => setCollapsed((v) => !v)} style={{ background: "none", border: "none", cursor: "pointer", color: C.rose, fontSize: 12, fontWeight: 600 }}>
          {collapsed ? "Show" : "Hide"}
        </button>
      </div>

      {!collapsed && (
        <div>
          {groups.billing.map((t) => (
            <Row key={t.id} meta={META.billing}
              title={`Bill rent for ${monthLabel(t.month)}`}
              subtitle={`${t.count} tenant${t.count === 1 ? "" : "s"} not yet billed this month`}>
              <ActionBtn primary onClick={() => actions.generateRentForMonth(t.month)}>Bill now</ActionBtn>
            </Row>
          ))}

          {groups.rent.map((t) => (
            <Row key={t.id} meta={META.rent} onOpen={() => onOpenTenant(t.tenant)}
              title={`Collect rent — ${t.tenant.name}`}
              subtitle={`${monthLabel(t.row.month)} · ${fmt(t.row.amount)}${t.lateFeeAmount > 0 ? ` + ${fmt(t.lateFeeAmount)} late fee` : ""} · ${t.status === "late" ? `${t.overdue} days overdue` : "due now"} · ${t.tenant.suite}`}>
              <ActionBtn primary onClick={() => actions.markRentPaid(t.row.id)}>Mark paid</ActionBtn>
              <TextBtn phone={t.tenant.phone} body={rentReminder(t.tenant, t.row, data.settings)} />
              <ActionBtn onClick={() => copy(rentReminder(t.tenant, t.row, data.settings))}>Copy</ActionBtn>
            </Row>
          ))}

          {groups.renewals.map((t) => (
            <Row key={t.id} meta={META.renewal} onOpen={() => onOpenTenant(t.tenant)}
              title={`Renew lease — ${t.tenant.name}`}
              subtitle={t.daysLeft < 0 ? `Lease expired ${-t.daysLeft} days ago · ${t.tenant.suite}` : `${t.daysLeft} days left · ${t.tenant.suite}`}>
              <ActionBtn primary onClick={() => actions.renewLease(t.tenant.id)}>Renew 1 yr</ActionBtn>
              <TextBtn phone={t.tenant.phone} body={renewalMessage(t.tenant, data.settings)} />
              <ActionBtn onClick={() => copy(renewalMessage(t.tenant, data.settings))}>Copy</ActionBtn>
            </Row>
          ))}

          {groups.vacancies.map((t) => (
            <Row key={t.id} meta={META.vacancy}
              title={t.upcoming ? `Upcoming vacancy — ${t.suite.name}` : `Fill vacancy — ${t.suite.name}`}
              subtitle={t.upcoming ? `${t.tenant?.name} moving out · ${fmt(t.suite.rent)}/mo` : `Empty · ${fmt(t.suite.rent)}/mo`}>
              <ActionBtn primary onClick={() => goTo("more", "applicants")}>View applicants</ActionBtn>
            </Row>
          ))}

          {groups.maintenance.map((t) => (
            <Row key={t.id} meta={META.maintenance}
              title={`${t.ticket.title} — ${t.suite?.name || "Common area"}`}
              subtitle={`${t.ticket.priority} priority · ${t.ticket.status}`}>
              <ActionBtn primary onClick={() => actions.setMaintenanceStatus(t.ticket.id, "done")}>Mark done</ActionBtn>
              {t.ticket.status === "open" && <ActionBtn onClick={() => actions.setMaintenanceStatus(t.ticket.id, "in-progress")}>Start</ActionBtn>}
            </Row>
          ))}

          {groups.leads.map((t) => (
            <Row key={t.id} meta={META.applicant}
              title={`Follow up — ${t.applicant.name}`}
              subtitle={`Waiting ${t.waitingDays} days · ${t.applicant.profession} · ${t.applicant.interest}`}>
              <ActionBtn primary onClick={() => actions.setApplicantStatus(t.applicant.id, t.applicant.status === "new" ? "toured" : "applied")}>
                {t.applicant.status === "new" ? "Mark toured" : "Mark applied"}
              </ActionBtn>
              <TextBtn phone={t.applicant.phone} body={applicantMessage(t.applicant, data.settings)} />
              <ActionBtn onClick={() => copy(applicantMessage(t.applicant, data.settings))}>Copy</ActionBtn>
            </Row>
          ))}
        </div>
      )}
    </Card>
  );
}
