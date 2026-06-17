// First-run welcome + data-backup reminder shown atop the dashboard. These keep
// a non-technical owner oriented (the demo data is sample) and safe (back up).
import { useBloom } from "../store";
import { C } from "../theme";
import { Icon, Icons } from "../icons";
import { daysAgo } from "../format";

export function Banners({ goTo }) {
  const { data, actions } = useBloom();
  const { settings } = data;
  const hasData = (data.clients?.length || 0) > 0;

  if (!settings.welcomeDismissed) {
    return (
      <div style={{ background: C.roseLight, border: `1px solid ${C.rose}`, borderRadius: 14, padding: "14px 16px", marginBottom: 16 }}>
        <div style={{ fontSize: 14, fontWeight: 700, color: C.charcoal, marginBottom: 4 }}>👋 Welcome to Bloom</div>
        <div style={{ fontSize: 13, color: C.charcoal, lineHeight: 1.5, marginBottom: 10 }}>
          This is <strong>sample data</strong> so you can explore. When you're ready for your real clients, go to{" "}
          <strong>More → Settings → Clear &amp; Start Fresh</strong>. Everything stays private on this device — just remember to <strong>back up</strong> now and then.
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={() => actions.updateSettings({ welcomeDismissed: true })} style={{ background: C.rose, color: C.white, border: "none", borderRadius: 9, padding: "8px 14px", fontSize: 13, fontWeight: 700, cursor: "pointer" }}>Got it</button>
          <button onClick={() => goTo("more")} style={{ background: C.white, color: C.rose, border: `1px solid ${C.rose}`, borderRadius: 9, padding: "8px 14px", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>Open Settings</button>
        </div>
      </div>
    );
  }

  const lb = settings.lastBackup;
  const stale = hasData && (!lb || daysAgo(lb) >= 7);
  if (stale) {
    return (
      <div style={{ background: C.amberLight, border: `1px solid ${C.amber}`, borderRadius: 14, padding: "12px 14px", marginBottom: 16, display: "flex", alignItems: "center", gap: 10 }}>
        <Icon d={Icons.download} size={20} color={C.amber} />
        <div style={{ flex: 1, fontSize: 13, color: C.charcoal }}>
          {lb ? `It's been ${daysAgo(lb)} days since your last backup.` : "You haven't backed up your data yet."} Keep it safe.
        </div>
        <button onClick={() => actions.backupData()} style={{ background: C.amber, color: C.white, border: "none", borderRadius: 9, padding: "8px 12px", fontSize: 12, fontWeight: 700, cursor: "pointer", whiteSpace: "nowrap" }}>Back up</button>
      </div>
    );
  }

  return null;
}
