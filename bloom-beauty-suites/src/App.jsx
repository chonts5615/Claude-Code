// App shell: header, the active page, the bottom tab bar, and the toast.
import { useState } from "react";
import { useBloom } from "./store";
import { C } from "./theme";
import { Icon, Icons } from "./icons";
import { Toast } from "./ui";
import Dashboard from "./pages/Dashboard";
import Clients from "./pages/Clients";
import Schedule from "./pages/Schedule";
import Finances from "./pages/Finances";
import More from "./pages/More";

const NavTab = ({ label, icon, active, onClick }) => (
  <button onClick={onClick} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 2, padding: "8px 0 6px", background: "none", border: "none", cursor: "pointer", color: active ? C.rose : C.grayLight, fontSize: 10, fontWeight: active ? 700 : 400, position: "relative" }}>
    <Icon d={icon} size={22} color={active ? C.rose : C.grayLight} />
    {label}
    {active && <div style={{ position: "absolute", top: 0, left: "25%", right: "25%", height: 2, background: C.rose, borderRadius: 1 }} />}
  </button>
);

export default function App() {
  const { data, toast } = useBloom();
  const [tab, setTab] = useState("dashboard");
  const [selectedClientId, setSelectedClientId] = useState(null);

  const openClient = (client) => {
    setSelectedClientId(client.id);
    setTab("clients");
  };
  const goTo = (t) => {
    if (t === "clients") setSelectedClientId(null);
    setTab(t);
  };

  return (
    <div style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", background: C.bg, minHeight: "100vh", maxWidth: 480, margin: "0 auto", position: "relative" }}>
      <div style={{ background: `linear-gradient(135deg, ${C.rose} 0%, #d4849c 100%)`, padding: "14px 18px 12px", display: "flex", justifyContent: "space-between", alignItems: "center", paddingTop: "max(14px, env(safe-area-inset-top))" }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
          <div style={{ fontSize: 20, fontWeight: 800, color: C.white, letterSpacing: -0.5 }}>bloom</div>
          <div style={{ fontSize: 11, color: "rgba(255,255,255,0.85)", fontWeight: 400 }}>beauty suites</div>
        </div>
        <div style={{ fontSize: 11, color: "rgba(255,255,255,0.85)" }}>{data.settings.location}</div>
      </div>

      <div style={{ paddingBottom: 70 }}>
        {tab === "dashboard" && <Dashboard onOpenClient={openClient} goTo={goTo} />}
        {tab === "clients" && <Clients selectedClientId={selectedClientId} setSelectedClientId={setSelectedClientId} />}
        {tab === "schedule" && <Schedule />}
        {tab === "finances" && <Finances />}
        {tab === "more" && <More />}
      </div>

      <Toast toast={toast} />

      <div style={{ position: "fixed", bottom: 0, left: "50%", transform: "translateX(-50%)", width: "100%", maxWidth: 480, background: C.white, borderTop: `1px solid ${C.grayBorder}`, display: "flex", paddingBottom: "env(safe-area-inset-bottom, 8px)", boxShadow: "0 -2px 10px rgba(0,0,0,0.05)", zIndex: 100 }}>
        <NavTab label="Home" icon={Icons.home} active={tab === "dashboard"} onClick={() => goTo("dashboard")} />
        <NavTab label="Clients" icon={Icons.users} active={tab === "clients"} onClick={() => goTo("clients")} />
        <NavTab label="Schedule" icon={Icons.calendar} active={tab === "schedule"} onClick={() => goTo("schedule")} />
        <NavTab label="Finances" icon={Icons.dollar} active={tab === "finances"} onClick={() => goTo("finances")} />
        <NavTab label="More" icon={Icons.menu} active={tab === "more"} onClick={() => goTo("more")} />
      </div>
    </div>
  );
}
