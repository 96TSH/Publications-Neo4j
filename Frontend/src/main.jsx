import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { FetchContextProvider } from "./stores/fetchContext.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <FetchContextProvider>
      <App />
    </FetchContextProvider>
  </React.StrictMode>
);
