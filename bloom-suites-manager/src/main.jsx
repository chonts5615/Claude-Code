import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BloomProvider } from "./store";
import App from "./App";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BloomProvider>
      <App />
    </BloomProvider>
  </StrictMode>
);
