import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer,
    Legend
} from "recharts"

function MoneyFlowChart({ summary }) {

    const data = [
        {
            name: "Money Sent",
            value: Number(summary.money_sent)
        },
        {
            name: "Money Received",
            value: Number(summary.money_received)
        }
    ]

    const COLORS = [
        "#ef4444",
        "#10b981"
    ]

    return (
        <div
            style={{
                backgroundColor: "#160e26",
                border: "1px solid #2a164d",
                borderRadius: "16px",
                padding: "25px",
                marginTop: "35px",
                boxShadow:
                    "0 8px 32px rgba(0,0,0,.3)"
            }}
        >
            <h2
                style={{
                    color: "white",
                    marginTop: 0
                }}
            >
                Money Flow Analysis
            </h2>

            <div
                style={{
                    height: "450px"
                }}
            >
                <ResponsiveContainer
                    width="100%"
                    height="100%"
                >
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            innerRadius={90}
                            outerRadius={150}
                            paddingAngle={5}
                            dataKey="value"
                        >
                            {
                                data.map(
                                    (_, index) => (
                                        <Cell
                                            key={index}
                                            fill={
                                                COLORS[index]
                                            }
                                        />
                                    )
                                )
                            }
                        </Pie>

                        <Tooltip
                            formatter={(value) =>
                                `₹${Number(value).toLocaleString()}`
                            }
                        />

                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

export default MoneyFlowChart