import { useEffect, useState } from "react"
import api from "../services/api"

function TransactionHistory({ user }) {
    const [transactions, setTransactions] = useState([])
    const [page, setPage] = useState(1)
    const [totalTransactions, setTotalTransactions] = useState(0)



    async function loadTransactions() {
        try {
            const response = await api.get(
                `/transactions/?page=${page}`
            )

            setTransactions(
                response.data.transactions
            )

            setTotalTransactions(
                response.data.total_transactions
            )
        }
        catch (error) {
            console.log(error)
        }
    }
    const totalPages = Math.ceil(totalTransactions / 5)
    useEffect(() => {
        loadTransactions()
    }, [page])

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
            <h2
                style={{
                    marginTop: 0,
                    marginBottom: "20px",
                    color: "#ffffff",
                    fontSize: "20px",
                    fontWeight: "600"
                }}
            >
                Recent Transactions
            </h2>

            {
                transactions.length === 0
                    ?
                    <p
                        style={{
                            color: "#a89ec4"
                        }}
                    >
                        No Transactions Found
                    </p>
                    :
                    transactions.map((transaction) => {

                        const outgoing =
                            transaction.SenderID === user?.UserID

                        return (
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
                                    <p
                                        style={{
                                            margin: "0 0 6px 0",
                                            fontWeight: "600",
                                            color: "#ffffff"
                                        }}
                                    >
                                        {
                                            outgoing
                                                ? "Transfer Sent"
                                                : "Transfer Received"
                                        }
                                    </p>

                                    <p
                                        style={{
                                            margin: 0,
                                            fontSize: "13px",
                                            color: "#a89ec4"
                                        }}
                                    >
                                        {
                                            outgoing
                                                ? `To User ${transaction.RecieverID}`
                                                : `From User ${transaction.SenderID}`
                                        }
                                    </p>

                                    <p
                                        style={{
                                            margin: "4px 0 0 0",
                                            fontSize: "12px",
                                            color: "#7c72a1"
                                        }}
                                    >
                                        Transaction ID: {transaction.TransactionID}
                                    </p>
                                </div>

                                <div>
                                    <p
                                        style={{
                                            margin: 0,
                                            fontWeight: "bold",
                                            fontSize: "18px",
                                            color: outgoing
                                                ? "#ef4444"
                                                : "#10b981"
                                        }}
                                    >
                                        {
                                            outgoing
                                                ? "-"
                                                : "+"
                                        }
                                        ₹
                                        {Number(
                                            transaction.TransactionAmount
                                        ).toLocaleString()}
                                    </p>

                                    <p
                                        style={{
                                            margin: "4px 0 0 0",
                                            fontSize: "12px",
                                            textAlign: "right",
                                            color: "#a89ec4"
                                        }}
                                    >
                                        {transaction.TransactionStatus}
                                    </p>
                                </div>
                            </div>
                        )
                    })
            }

            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginTop: "20px"
                }}
            >
                <button
                    onClick={() => setPage(page - 1)}
                    disabled={page === 1}
                >
                    ← Previous
                </button>

                <span
                    style={{
                        color: "#ffffff"
                    }}
                >
                    Page {page} of {totalPages}
                </span>

                <button
                    onClick={() => setPage(page + 1)}
                    disabled={page >= totalPages}
                >
                    Next →
                </button>
            </div>
        </div>
    )
}

export default TransactionHistory