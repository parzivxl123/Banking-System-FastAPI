import { useEffect, useState } from "react"
import api from "../services/api"
import TiltCard from "../components/TiltCard"
import MoneyFlowChart from "../components/MoneyFlowCharts.jsx";
import MonthlyActivityChart from "../components/MonthlyActivityChart.jsx";
function Statistics() {
    const [summary, setSummary] = useState(null)
    const [monthlyData, setMonthlyData] =
        useState([])
    async function loadMonthlyData() {
        try {
            const response =
                await api.get(
                    "/analytics/monthly"
                )

            setMonthlyData(
                response.data
            )
        }
        catch(error) {
            console.log(error)
        }
    }
    async function loadSummary() {
        try {
            const response = await api.get(
                "/analytics/summary"
            )

            setSummary(response.data)
        }
        catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        loadSummary()
        loadMonthlyData()
    }, [])

    if (!summary) {
        return (
            <div
                style={{
                    minHeight: "100vh",
                    background: "#0d0818",
                    color: "white",
                    padding: "40px"
                }}
            >
                Loading...
            </div>
        )
    }

    return (
        <div
            style={{
                minHeight: "100vh",
                background:
                    "linear-gradient(135deg, #0d0818 0%, #160e26 100%)",
                padding: "40px"
            }}
        >
            <h1
                style={{
                    color: "white",
                    marginBottom: "30px",
                    fontSize: "36px"
                }}
            >
                Analytics Dashboard
            </h1>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit, minmax(280px, 1fr))",
                    gap: "25px"
                }}
            >
                <TiltCard>
                    <div
                        style={{
                            padding: "25px"
                        }}
                    >
                        <h3
                            style={{
                                color: "#a89ec4",
                                marginTop: 0
                            }}
                        >
                            Current Balance
                        </h3>

                        <h2
                            style={{
                                color: "#ffffff",
                                marginBottom: 0,
                                fontSize: "32px"
                            }}
                        >
                            ₹
                            {Number(
                                summary.balance
                            ).toLocaleString()}
                        </h2>
                    </div>
                </TiltCard>

                <TiltCard>
                    <div
                        style={{
                            padding: "25px"
                        }}
                    >
                        <h3
                            style={{
                                color: "#a89ec4",
                                marginTop: 0
                            }}
                        >
                            Money Sent
                        </h3>

                        <h2
                            style={{
                                color: "#ef4444",
                                marginBottom: 0,
                                fontSize: "32px"
                            }}
                        >
                            ₹
                            {Number(
                                summary.money_sent
                            ).toLocaleString()}
                        </h2>
                    </div>
                </TiltCard>

                <TiltCard>
                    <div
                        style={{
                            padding: "25px"
                        }}
                    >
                        <h3
                            style={{
                                color: "#a89ec4",
                                marginTop: 0
                            }}
                        >
                            Money Received
                        </h3>

                        <h2
                            style={{
                                color: "#10b981",
                                marginBottom: 0,
                                fontSize: "32px"
                            }}
                        >
                            ₹
                            {Number(
                                summary.money_received
                            ).toLocaleString()}
                        </h2>
                    </div>
                </TiltCard>

                <TiltCard>
                    <div
                        style={{
                            padding: "25px"
                        }}
                    >
                        <h3
                            style={{
                                color: "#a89ec4",
                                marginTop: 0
                            }}
                        >
                            Total Deposits
                        </h3>

                        <h2
                            style={{
                                color: "#22c55e",
                                marginBottom: 0,
                                fontSize: "32px"
                            }}
                        >

                            {Number(
                                summary.total_deposits
                            ).toLocaleString()}
                        </h2>
                    </div>
                </TiltCard>

                <TiltCard>
                    <div
                        style={{
                            padding: "25px"
                        }}
                    >
                        <h3
                            style={{
                                color: "#a89ec4",
                                marginTop: 0
                            }}
                        >
                            Total Withdrawals
                        </h3>

                        <h2
                            style={{
                                color: "#f97316",
                                marginBottom: 0,
                                fontSize: "32px"
                            }}
                        >

                            {Number(
                                summary.total_withdrawals
                            ).toLocaleString()}
                        </h2>
                    </div>
                </TiltCard>

                <TiltCard>
                    <div
                        style={{
                            padding: "25px"
                        }}
                    >
                        <h3
                            style={{
                                color: "#a89ec4",
                                marginTop: 0
                            }}
                        >
                            Total Transactions
                        </h3>

                        <h2
                            style={{
                                color: "#ffffff",
                                marginBottom: 0,
                                fontSize: "32px"
                            }}
                        >
                            {summary.total_transactions}
                        </h2>
                    </div>
                </TiltCard>
            </div>
            <MoneyFlowChart
                summary={summary}
            />
            <MonthlyActivityChart
                data={monthlyData}
            />
        </div>
    )
}

export default Statistics