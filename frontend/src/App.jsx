import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import Deposit from "./pages/Deposit"
import Withdrawal from "./pages/Withdrawal"
import Transfer from "./pages/Transfer";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
function App() {

  return (
      <BrowserRouter>
        <Routes>
          <Route
              path="/"
              element={<Login />}
          />

          <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
          />

          <Route
              path="/deposit"
              element={
                <ProtectedRoute>
                  <Deposit />
                </ProtectedRoute>
              }
          />
          <Route
              path="/withdrawal"
              element={
                <ProtectedRoute>
                  <Withdrawal />
                </ProtectedRoute>}
          />
          <Route
              path="/transfer"
              element={
                <ProtectedRoute>
                  <Transfer />
                </ProtectedRoute>
              }
          />
        </Routes>

      </BrowserRouter>
  )
}

export default App