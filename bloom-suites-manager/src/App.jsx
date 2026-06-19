// App shell: header, the active page, the bottom tab bar, and the toast.
import { useCallback, useState } from "react";
import { useBloom } from "./store";
import { C } from "./theme";
import { Icon, Icons } from "./icons";
import { Toast } from "./ui";
import Dashboard from "./pages/Dashboard";
import Suites from "./pages/Suites";
import Tenants from "./pages/Tenants";
import Rent from "./pages/Rent";
import More from "./pages/More";

const NavTab = ({ label, icon, active, onClick }) => (
  <button onClick={onClick} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 2, padding: "8px 0 6px", background: "none", border: "none", cursor: "pointer", color: active ? C.gold : C.grayLight, fontSize: 10, fontWeight: active ? 700 : 400, position: "relative" }}>
    <Icon d={icon} size={22} color={active ? C.gold : C.grayLight} />
    {label}
    {active && <div style={{ position: "absolute", top: 0, left: "25%", right: "25%", height: 2, background: C.gold, borderRadius: 1 }} />}
  </button>
);

export default function App() {
  const { data, toast } = useBloom();
  const [tab, setTab] = useState("dashboard");
  const [selectedTenantId, setSelectedTenantId] = useState(null);
  const [moreSub, setMoreSub] = useState(null);

  const openTenant = (tenant) => {
    setSelectedTenantId(tenant.id);
    setTab("tenants");
  };
  const goTo = (t, sub = null) => {
    if (t === "tenants") setSelectedTenantId(null);
    if (t === "more") setMoreSub(sub);
    setTab(t);
  };
  const clearSub = useCallback(() => setMoreSub(null), []);

  return (
    <div style={{ fontFamily: "'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", background: C.bg, minHeight: "100vh", maxWidth: 480, margin: "0 auto", position: "relative" }}>
      {/* Editorial wordmark header, matched to the brand site (operator app) */}
      <div style={{ background: C.white, borderBottom: `1px solid ${C.grayBorder}`, padding: "16px 18px 13px", paddingTop: "max(16px, env(safe-area-inset-top))", textAlign: "center", position: "relative" }}>
        <div style={{ fontFamily: C.serif, fontSize: 23, fontWeight: 600, color: C.charcoal, letterSpacing: 5, lineHeight: 1 }}>BLOOM</div>
        <div style={{ fontSize: 9, color: C.gold, letterSpacing: 4, marginTop: 3, fontWeight: 600 }}>SUITES&nbsp;&nbsp;MANAGER</div>
        <div style={{ position: "absolute", right: 16, bottom: 13, fontSize: 10, color: C.grayLight, letterSpacing: 0.3 }}>{data.settings.location}</div>
      </div>

      <div style={{ paddingBottom: 70 }}>
        {tab === "dashboard" && <Dashboard onOpenTenant={openTenant} goTo={goTo} />}
        {tab === "suites" && <Suites onOpenTenant={openTenant} />}
        {tab === "tenants" && <Tenants selectedTenantId={selectedTenantId} setSelectedTenantId={setSelectedTenantId} />}
        {tab === "rent" && <Rent />}
        {tab === "more" && <More sub={moreSub} clearSub={clearSub} />}
      </div>

      <Toast toast={toast} />

      <div style={{ position: "fixed", bottom: 0, left: "50%", transform: "translateX(-50%)", width: "100%", maxWidth: 480, background: C.white, borderTop: `1px solid ${C.grayBorder}`, display: "flex", paddingBottom: "env(safe-area-inset-bottom, 8px)", boxShadow: "0 -2px 10px rgba(0,0,0,0.05)", zIndex: 100 }}>
        <NavTab label="Home" icon={Icons.home} active={tab === "dashboard"} onClick={() => goTo("dashboard")} />
        <NavTab label="Suites" icon={Icons.building} active={tab === "suites"} onClick={() => goTo("suites")} />
        <NavTab label="Tenants" icon={Icons.users} active={tab === "tenants"} onClick={() => goTo("tenants")} />
        <NavTab label="Rent" icon={Icons.dollar} active={tab === "rent"} onClick={() => goTo("rent")} />
        <NavTab label="More" icon={Icons.menu} active={tab === "more"} onClick={() => goTo("more")} />
      </div>
    </div>
  );
}
