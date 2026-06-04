import { useEffect, useState } from "react"
import api from "../services/api"

function TransactionHistory() {
  const [transactions, setTransactions] = useState([])

  async function loadTransactions() {
    try {
      const response = await api.get("/transactions/")
      setTransactions(response.data.transactions)
    }
    catch(error) {
      console.log(error)
    }
  }

  useEffect(() => {
    loadTransactions()
  }, [])

  return (
    <div
      style={{
        backgroundColor: "#160e26",
        padding: "30px",
        borderRadius: "16px",
        marginTop: "30px",
        boxShadow: "0 8px 32px rgba(0,0,0,0.3)",
        border: "1px solid #2a164d"
      }}
    >
      <h2 style={{ marginTop: 0, marginBottom: "20px", color: "#ffffff", fontSize: "20px", fontWeight: "600" }}>
        Recent Transactions
      </h2>

      {
        transactions.length === 0
        ?
        <p style={{ color: "#a89ec4" }}>No Transactions found.</p>
        :
        transactions.map((transaction) => (
          <div
            key={transaction.TransactionID}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              borderBottom: "1px solid #2a164d",
              padding: "15px 0"
            }}
          >
            <div>
               <p style={{ margin: "0 0 6px 0", fontWeight: "600", color: "#ffffff" }}>
                 Transaction #{transaction.TransactionID || "..."}
               </p>
               <p style={{ margin: 0, fontSize: "13px", color: "#a89ec4" }}>
                 Sender: {transaction.SenderID} | Receiver: {transaction.RecieverID}
               </p>
            </div>

            <div>
               <p style={{ margin: 0, fontWeight: "bold", fontSize: "18px", color: "#10b981" }}>
                 ₹{transaction.TransactionAmount}
               </p>
            </div>
          </div>
        ))
      }
    </div>
  )
}

export default TransactionHistory