import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../services/api"

function Transfer() {
    const [receiverId, setReceiverId] = useState("")
    const [amount, setAmount] = useState("")
    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()

    async function handleTransfer() {
        try {
            setLoading(true)

            await api.post("/transactions/", {
                TransactionAmount: Number(amount),
                RecieverID: Number(receiverId)
            })

            alert("Transfer Successful")

            navigate("/dashboard")
        }
        catch (error) {
            console.log(error)

            if (error.response?.data?.detail) {
                alert(error.response.data.detail)
            }
        }
        finally {
            setLoading(false)
        }
    }

    return (
        <div
            style={{
                minHeight: "100vh",
                backgroundColor: "#0b0614",
                color: "#ffffff",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                fontFamily: "system-ui, sans-serif",
                padding: "30px"
            }}
        >
            <div style={{
                backgroundColor: "#160e26",
                padding: "40px",
                borderRadius: "16px",
                boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
                border: "1px solid #2a164d",
                width: "100%",
                maxWidth: "400px"
            }}>
                <h1 style={{ textAlign: "center", marginBottom: "30px" }}>Transfer Funds</h1>

                <div style={{ marginBottom: "15px" }}>
                    <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#a89ec4" }}>Receiver ID</p>
                    <input
                        type="number"
                        placeholder="Enter ID"
                        value={receiverId}
                        onChange={(e) => setReceiverId(e.target.value)}
                        style={{
                            width: "100%",
                            padding: "14px",
                            borderRadius: "8px",
                            border: "1px solid #44226E",
                            backgroundColor: "#0b0614",
                            color: "#ffffff",
                            boxSizing: "border-box",
                            outline: "none"
                        }}
                    />
                </div>

                <div style={{ marginBottom: "25px" }}>
                    <p style={{ margin: "0 0 8px 0", fontSize: "14px", color: "#a89ec4" }}>Amount</p>
                    <input
                        type="number"
                        placeholder="Enter amount"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        style={{
                            width: "100%",
                            padding: "14px",
                            borderRadius: "8px",
                            border: "1px solid #44226E",
                            backgroundColor: "#0b0614",
                            color: "#ffffff",
                            boxSizing: "border-box",
                            outline: "none"
                        }}
                    />
                </div>

                <button
                    onClick={handleTransfer}
                    disabled={loading}
                    style={{
                        width: "100%",
                        padding: "14px",
                        borderRadius: "8px",
                        border: "none",
                        background: "linear-gradient(to right, #44226E, #8342D4)",
                        color: "white",
                        fontWeight: "bold",
                        fontSize: "16px",
                        cursor: loading ? "not-allowed" : "pointer",
                        opacity: loading ? 0.7 : 1
                    }}
                >
                    {loading ? "Transferring..." : "Transfer"}
                </button>
            </div>
        </div>
    )
}

export default Transfer