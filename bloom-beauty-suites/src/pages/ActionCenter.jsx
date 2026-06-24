// The Action Center turns the automation engine's output into a one-tap daily
// to-do list. Open the app → see exactly what needs doing today.
import { useState } from "react";
import { useBloom } from "../store";
import {
  buildActionCenter,
  rebookMessage,
  winbackMessage,
  waitlistMessage,
} from "../automation";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { Card, SectionHeader, copyText, smsHref } from "../ui";
import { fmtD } from "../format";

const TASK_META = {
  rebook: { icon: Icons.bell, color: C.rose, bg: C.roseLight },
  winback: { icon: Icons.heart || Icons.bell, color: C.gold, bg: C.goldLight },
  reorder: { icon: Icons.box, color: C.amber, bg: C.amberLight },
  expiring: { icon: Icons.clock, color: C.red, bg: C.redLight },
  waitlist: { icon: Icons.list, color: C.rose, bg: C.roseLight },
};

const ActionBtn = ({ children, onClick, primary }) => (
  <button
    onClick={onClick}
    style={{
      padding: "7px 12px",
      borderRadius: 9,
      border: primary ? "none" : `1px solid ${C.grayBorder}`,
      background: primary ? C.rose : C.white,
      color: primary ? C.white : C.charcoal,
      fontSize: 12,
      fontWeight: 600,
      cursor: "pointer",
      whiteSpace: "nowrap",
    }}
  >
    {children}
  </button>
);

// Like ActionBtn, but an <a> so it can open the phone's Messages app (sms:).
const TextBtn = ({ phone, body }) => (
  <a
    href={smsHref(phone, body)}
    style={{ padding: "7px 12px", borderRadius: 9, border: "none", background: C.rose, color: C.white, fontSize: 12, fontWeight: 600, textDecoration: "none", whiteSpace: "nowrap", display: "inline-flex", alignItems: "center", gap: 5 }}
  >
    <Icon d={Icons.phone} size={13} color={C.white} /> Text
  </a>
);

function TaskRow({ meta, title, subtitle, children, onOpen }) {
  return (
    <div style={{ display: "flex", gap: 12, padding: "12px 0", borderBottom: `1px solid ${C.grayBorder}` }}>
      <div style={{ width: 34, height: 34, borderRadius: 10, background: meta.bg, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
        <Icon d={meta.icon} size={18} color={meta.color} />
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div
          onClick={onOpen}
          style={{ fontSize: 14, fontWeight: 600, color: C.charcoal, cursor: onOpen ? "pointer" : "default" }}
        >
          {title}
        </div>
        <div style={{ fontSize: 12, color: C.gray, marginBottom: 8 }}>{subtitle}</div>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>{children}</div>
      </div>
    </div>
  );
}

export default function ActionCenter({ onOpenClient }) {
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
          <span style={{ background: C.rose, color: C.white, fontSize: 12, fontWeight: 700, borderRadius: 12, padding: "1px 8px" }}>
            {total}
          </span>
        </div>
        <button onClick={() => setCollapsed((v) => !v)} style={{ background: "none", border: "none", cursor: "pointer", color: C.rose, fontSize: 12, fontWeight: 600 }}>
          {collapsed ? "Show" : "Hide"}
        </button>
      </div>

      {!collapsed && (
        <div>
          {groups.rebook.map((t) => (
            <TaskRow
              key={t.id}
              meta={TASK_META.rebook}
              onOpen={() => onOpenClient(t.client)}
              title={`Rebook ${t.client.name}`}
              subtitle={
                t.overdueDays > 0
                  ? `${t.overdueDays} day${t.overdueDays === 1 ? "" : "s"} past their usual ${t.client.avgInterval}-day cadence`
                  : "Due for their next appointment"
              }
            >
              <ActionBtn primary onClick={() => actions.rebookClient(t.client.id)}>
                Rebook
              </ActionBtn>
              <TextBtn phone={t.client.phone} body={rebookMessage(t.client, data.settings)} />
              <ActionBtn onClick={() => copy(rebookMessage(t.client, data.settings))}>
                Copy
              </ActionBtn>
            </TaskRow>
          ))}

          {groups.winback.map((t) => (
            <TaskRow
              key={t.id}
              meta={TASK_META.winback}
              onOpen={() => onOpenClient(t.client)}
              title={`Win back ${t.client.name}`}
              subtitle={`${t.daysSince} days since last visit`}
            >
              <TextBtn phone={t.client.phone} body={winbackMessage(t.client, data.settings)} />
              <ActionBtn onClick={() => copy(winbackMessage(t.client, data.settings))}>
                Copy win-back
              </ActionBtn>
            </TaskRow>
          ))}

          {groups.reorder.map((t) => (
            <TaskRow
              key={t.id}
              meta={TASK_META.reorder}
              title={`Reorder ${t.item.name}`}
              subtitle={`${t.item.qty} left · reorder at ${t.item.reorder} · ${fmtD(t.item.cost)} from ${t.item.supplier}`}
            >
              <ActionBtn primary onClick={() => actions.markOrdered(t.item.id)}>
                Mark ordered
              </ActionBtn>
            </TaskRow>
          ))}

          {groups.expiring.map((t) => (
            <TaskRow
              key={t.id}
              meta={TASK_META.expiring}
              title={`${t.item.name} expiring`}
              subtitle={`Expires ${t.item.expires}${t.daysLeft >= 0 ? ` · ${t.daysLeft} days left` : " · expired"}`}
            >
              <ActionBtn onClick={() => actions.markOrdered(t.item.id)}>Reorder</ActionBtn>
            </TaskRow>
          ))}

          {groups.waitlist.map((t) => (
            <TaskRow
              key={t.id}
              meta={TASK_META.waitlist}
              title={t.entry.status === "contacted" ? `Follow up again — ${t.entry.name}` : `Follow up with ${t.entry.name}`}
              subtitle={`${t.waitingDays} days on waitlist · ${t.entry.service}${t.entry.preferred ? ` · ${t.entry.preferred}` : ""}`}
            >
              <ActionBtn primary onClick={() => actions.setWaitlistStatus(t.entry.id, "booked")}>
                Mark booked
              </ActionBtn>
              <TextBtn phone={t.entry.phone} body={waitlistMessage(t.entry, data.settings)} />
              <ActionBtn onClick={() => copy(waitlistMessage(t.entry, data.settings))}>
                Copy
              </ActionBtn>
              {t.entry.status === "waiting" && (
                <ActionBtn onClick={() => actions.setWaitlistStatus(t.entry.id, "contacted")}>
                  Mark contacted
                </ActionBtn>
              )}
            </TaskRow>
          ))}
        </div>
      )}
    </Card>
  );
}
