import BalanceCard from "../components/BalanceCard"
import ActionButtons from "../components/ActionButtons"
import { useEffect, useState } from "react"
import api from "../services/api"
import Sidebar from "../components/Sidebar"
import TransactionHistory from "../components/TransactionHistory.jsx";
import DepositHistory from "../components/DepositHistory.jsx";
import WithdrawalHistory from "../components/WithdrawalHistory.jsx";

function Dashboard() {
    const [user, setUser] = useState(null)
    const [historyType, setHistoryType] =
        useState("transactions")
  async function loadUser() {
    try {
      const token = localStorage.getItem("token")

      const response = await api.get(
        "/users/user"
      )

      setUser(response.data)

      console.log(response.data)
    }
    catch (error) {
      console.log(error)
    }
  }

  useEffect(() => {
    loadUser()
  }, [])

  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        backgroundColor: "#0b0614",
        color: "#ffffff",
        fontFamily: "system-ui, sans-serif"
      }}
    >
      <Sidebar />

      <div
        style={{
          flex: 1,
          padding: "40px",
          maxWidth: "1200px",
          margin: "0 auto"
        }}
      >
        <h1 style={{ fontWeight: "600", marginBottom: "30px" }}>
          Welcome {user?.UserName}
        </h1>

          <BalanceCard
              balance={user?.UserBalance || 0}
          />

          <ActionButtons
              setHistoryType={setHistoryType}
          />

          {
              historyType === "transactions" &&
              <TransactionHistory user={user}/>
          }

          {
              historyType === "deposits" &&
              <DepositHistory />
          }

          {
              historyType === "withdrawals" &&
              <WithdrawalHistory />
          }
      </div>
    </div>
  )
}

export default Dashboard