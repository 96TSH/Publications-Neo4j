import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";

import Homepage from "./pages/homepage.jsx";
import Dashboard from "./pages/dashboard.jsx";
import Navbar from "./components/Navbar.jsx";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navbar />}>
            <Route index element={<Homepage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
