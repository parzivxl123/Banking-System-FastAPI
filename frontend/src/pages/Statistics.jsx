import { useEffect, useState } from "react"
import api from "../services/api"

function Statistics() {
    const [summary, setSummary] = useState(null)

    async function loadSummary() {
        try {
            const response = await api.get(
                "/analytics/summary"
            )

            setSummary(response.data)
        }
        catch(error) {
            console.log(error)
        }
    }

    useEffect(() => {
        loadSummary()
    }, [])

    if (!summary) {
        return <h2>Loading...</h2>
    }

    return (
        <div style={{ padding: "30px" }}>
            <h1>Statistics</h1>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit, minmax(250px, 1fr))",
                    gap: "20px",
                    marginTop: "20px"
                }}
            >
                <div className="stat-card">
                    <h3>Current Balance</h3>
                    <h2>
                        ₹{Number(summary.balance)
                        .toLocaleString()}
                    </h2>
                </div>

                <div className="stat-card">
                    <h3>Money Sent</h3>
                    <h2>
                        ₹{Number(summary.money_sent)
                        .toLocaleString()}
                    </h2>
                </div>

                <div className="stat-card">
                    <h3>Money Received</h3>
                    <h2>
                        ₹{Number(summary.money_received)
                        .toLocaleString()}
                    </h2>
                </div>

                <div className="stat-card">
                    <h3>Total Transactions</h3>
                    <h2>
                        {summary.total_transactions}
                    </h2>
                </div>
            </div>
        </div>
    )
}

export default Statistics