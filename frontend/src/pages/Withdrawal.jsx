import { useState } from "react"
import api from "../services/api"
import { useNavigate } from "react-router-dom"

function Withdrawal() {
    const [amount, setAmount] = useState("")
    const navigate = useNavigate()
    const [loading, setLoading] = useState(false)

    async function handleWithdrawal() {
        setLoading(true)
        try {
            const response = await api.post(
                "/withdrawal/",
                {
                    Amount: Number(amount)
                }
            )

            console.log(response.data)

            alert("Withdrawal Successful")
            navigate("/dashboard")
            setLoading(false)
            setAmount("")
        }
        catch (error) {
            console.log(error)
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
            }}>

            <div style={{
                backgroundColor: "#160e26",
                padding: "40px",
                borderRadius: "16px",
                boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
                border: "1px solid #2a164d",
                width: "100%",
                maxWidth: "400px"
            }}>
                <h1 style={{ textAlign: "center", marginBottom: "30px" }}>Withdraw Funds</h1>

                <input
                    type="number"
                    placeholder="Enter amount"
                    value={amount}
                    onChange={(event) => setAmount(event.target.value)}
                    style={{
                        width: "100%",
                        padding: "14px",
                        marginBottom: "20px",
                        borderRadius: "8px",
                        border: "1px solid #44226E",
                        backgroundColor: "#0b0614",
                        color: "#ffffff",
                        boxSizing: "border-box",
                        outline: "none"
                    }}
                />

                <button
                    onClick={handleWithdrawal}
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
                    {loading ? "Withdrawing..." : "Withdraw"}
                </button>
            </div>
        </div>
    )
}

export default Withdrawal