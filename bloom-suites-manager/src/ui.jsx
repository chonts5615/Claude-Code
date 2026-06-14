// Shared presentational building blocks used across pages.
import { useEffect } from "react";
import { C } from "./theme";
import { Icon, Icons } from "./icons";

export const card = {
  background: C.white,
  borderRadius: 16,
  padding: 16,
  boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
};

export const Card = ({ children, style }) => <div style={{ ...card, ...style }}>{children}</div>;

export const KPI = ({ label, value, sub, trend }) => (
  <div style={{ ...card, padding: "16px 18px", flex: "1 1 45%", minWidth: 140 }}>
    <div style={{ fontSize: 11, color: C.grayLight, textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 4 }}>
      {label}
    </div>
    <div style={{ fontSize: 26, fontWeight: 700, color: C.charcoal }}>{value}</div>
    {sub && (
      <div style={{ fontSize: 12, marginTop: 2, color: trend === "up" ? C.green : trend === "down" ? C.red : C.gray }}>
        {sub}
      </div>
    )}
  </div>
);

export const Badge = ({ text, color, bg }) => (
  <span style={{ display: "inline-block", fontSize: 10, fontWeight: 600, color, background: bg, padding: "2px 8px", borderRadius: 10, textTransform: "uppercase", letterSpacing: 0.5 }}>
    {text}
  </span>
);

// Status → colors, defined once so badges stay consistent everywhere.
const STATUS_STYLE = {
  // Suites / tenants
  occupied: [C.green, C.greenLight],
  notice: [C.amber, C.amberLight],
  vacant: [C.red, C.redLight],
  // Rent
  paid: [C.green, C.greenLight],
  due: [C.gold, C.goldLight],
  late: [C.red, C.redLight],
  upcoming: [C.gray, C.grayBorder],
  // Maintenance
  open: [C.amber, C.amberLight],
  "in-progress": [C.rose, C.roseLight],
  done: [C.green, C.greenLight],
  // Applicants
  new: [C.gold, C.goldLight],
  toured: [C.rose, C.roseLight],
  applied: [C.rose, C.roseLight],
  approved: [C.green, C.greenLight],
};
export const StatusBadge = ({ status }) => {
  const [color, bg] = STATUS_STYLE[status] || [C.gray, C.grayBorder];
  return <Badge text={status} color={color} bg={bg} />;
};

export const SectionHeader = ({ title, action, onAction }) => (
  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
    <h3 style={{ fontSize: 16, fontWeight: 700, color: C.charcoal, margin: 0 }}>{title}</h3>
    {action && (
      <button onClick={onAction} style={{ fontSize: 12, color: C.rose, background: "none", border: "none", cursor: "pointer", fontWeight: 600 }}>
        {action}
      </button>
    )}
  </div>
);

export const SearchBar = ({ value, onChange, placeholder }) => (
  <div style={{ position: "relative", marginBottom: 12 }}>
    <div style={{ position: "absolute", left: 12, top: 10 }}>
      <Icon d={Icons.search} size={16} color={C.grayLight} />
    </div>
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      style={{ width: "100%", padding: "10px 12px 10px 36px", borderRadius: 12, border: `1px solid ${C.grayBorder}`, fontSize: 14, background: C.white, outline: "none", color: C.charcoal, boxSizing: "border-box" }}
    />
  </div>
);

export const Avatar = ({ name, size = 40 }) => (
  <div style={{ width: size, height: size, borderRadius: size / 2, background: C.roseLight, display: "flex", alignItems: "center", justifyContent: "center", fontSize: size * 0.4, fontWeight: 700, color: C.rose, flexShrink: 0 }}>
    {name.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase()}
  </div>
);

export const PrimaryButton = ({ children, onClick, style, type = "button", disabled }) => (
  <button
    type={type}
    onClick={onClick}
    disabled={disabled}
    style={{ width: "100%", padding: 14, background: disabled ? C.grayLight : C.rose, color: C.white, border: "none", borderRadius: 12, fontSize: 16, fontWeight: 700, cursor: disabled ? "default" : "pointer", ...style }}
  >
    {children}
  </button>
);

export const GhostButton = ({ children, onClick, style }) => (
  <button
    onClick={onClick}
    style={{ padding: "10px 14px", background: C.roseLight, color: C.rose, border: `1px solid ${C.rose}`, borderRadius: 10, fontSize: 13, fontWeight: 600, cursor: "pointer", ...style }}
  >
    {children}
  </button>
);

export const BackButton = ({ onClick, label = "Back" }) => (
  <button
    onClick={onClick}
    style={{ display: "flex", alignItems: "center", gap: 6, background: "none", border: "none", cursor: "pointer", color: C.rose, fontSize: 14, fontWeight: 600, marginBottom: 16, padding: 0 }}
  >
    <Icon d={Icons.back} size={18} color={C.rose} /> {label}
  </button>
);

export const PageTitle = ({ children, right }) => (
  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
    <h2 style={{ fontSize: 20, fontWeight: 700, color: C.charcoal, margin: 0 }}>{children}</h2>
    {right}
  </div>
);

export const Field = ({ label, children }) => (
  <div style={{ marginBottom: 14 }}>
    <label style={{ fontSize: 12, color: C.gray, fontWeight: 600, display: "block", marginBottom: 4 }}>{label}</label>
    {children}
  </div>
);

const inputStyle = {
  width: "100%",
  padding: "10px 12px",
  borderRadius: 10,
  border: `1px solid ${C.grayBorder}`,
  fontSize: 14,
  boxSizing: "border-box",
  outline: "none",
  background: C.white,
  color: C.charcoal,
};
export const Input = (props) => <input {...props} style={{ ...inputStyle, ...props.style }} />;
export const Textarea = (props) => (
  <textarea {...props} style={{ ...inputStyle, resize: "vertical", ...props.style }} />
);
export const Select = ({ children, ...props }) => (
  <select {...props} style={{ ...inputStyle, ...props.style }}>
    {children}
  </select>
);

export const EmptyState = ({ icon = Icons.calendar, text }) => (
  <div style={{ textAlign: "center", padding: 40, color: C.grayLight }}>
    <Icon d={icon} size={40} color={C.grayBorder} />
    <p style={{ fontSize: 14, marginTop: 10 }}>{text}</p>
  </div>
);

// Bottom-sheet modal — large tap targets, easy to dismiss.
export const Modal = ({ open, onClose, title, children }) => {
  useEffect(() => {
    if (!open) return;
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);
  if (!open) return null;
  return (
    <div
      onClick={onClose}
      style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.4)", zIndex: 200, display: "flex", alignItems: "flex-end", justifyContent: "center" }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{ width: "100%", maxWidth: 480, background: C.bg, borderRadius: "20px 20px 0 0", padding: "8px 16px 24px", maxHeight: "90vh", overflowY: "auto", boxShadow: "0 -4px 20px rgba(0,0,0,0.15)" }}
      >
        <div style={{ width: 40, height: 4, borderRadius: 2, background: C.grayBorder, margin: "8px auto 12px" }} />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
          <h3 style={{ fontSize: 18, fontWeight: 700, color: C.charcoal, margin: 0 }}>{title}</h3>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", padding: 4 }}>
            <Icon d={Icons.x} size={22} color={C.grayLight} />
          </button>
        </div>
        {children}
      </div>
    </div>
  );
};

export const Toast = ({ toast }) => {
  if (!toast) return null;
  return (
    <div style={{ position: "fixed", bottom: 86, left: "50%", transform: "translateX(-50%)", background: C.charcoal, color: C.white, padding: "10px 18px", borderRadius: 24, fontSize: 13, fontWeight: 600, zIndex: 300, boxShadow: "0 4px 16px rgba(0,0,0,0.25)", display: "flex", alignItems: "center", gap: 8, maxWidth: "90%" }}>
      <Icon d={Icons.check} size={16} color={C.rose} /> {toast.message}
    </div>
  );
};

// Copy text to the clipboard with a graceful fallback for older mobile browsers.
export async function copyText(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch {
    /* fall through */
  }
  try {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    return true;
  } catch {
    return false;
  }
}
