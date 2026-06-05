import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
    Legend
} from "recharts"

function MonthlyActivityChart({ data }) {

    return (
        <div
            style={{
                backgroundColor: "#160e26",
                border: "1px solid #2a164d",
                borderRadius: "16px",
                padding: "25px",
                marginTop: "30px",
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
                Monthly Activity
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
                    <LineChart
                        data={data}
                    >
                        <CartesianGrid
                            stroke="#2a164d"
                        />

                        <XAxis
                            dataKey="month"
                            stroke="#a89ec4"
                        />

                        <YAxis
                            stroke="#a89ec4"
                        />

                        <Tooltip
                            formatter={(value) =>
                                `₹${Number(value)
                                    .toLocaleString()}`
                            }
                        />

                        <Legend />

                        <Line
                            type="monotone"
                            dataKey="sent"
                            stroke="#ef4444"
                            strokeWidth={3}
                            dot={{ r: 5 }}
                        />

                        <Line
                            type="monotone"
                            dataKey="received"
                            stroke="#10b981"
                            strokeWidth={3}
                            dot={{ r: 5 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

export default MonthlyActivityChart