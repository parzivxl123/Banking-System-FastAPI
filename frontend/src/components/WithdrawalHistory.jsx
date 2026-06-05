import { useEffect, useState } from "react"
import api from "../services/api"

function WithdrawalHistory() {

    const [withdrawals, setWithdrawals] = useState([])
    const [page, setPage] = useState(1)
    const [totalWithdrawals, setTotalWithdrawals] =
        useState(0)

    const totalPages = Math.ceil(
        totalWithdrawals / 5
    )
    async function loadWithdrawals() {
        try {
            const response =
                await api.get(`/withdrawals/?page=${page}`)

            setWithdrawals(
                response.data.withdrawals
            )

            setTotalWithdrawals(
                response.data.total_withdrawals
            )
        }
        catch(error) {
            console.log(error)
        }
    }

    useEffect(() => {
        loadWithdrawals()
    }, [page])

    return (
        <div
            style={{
                backgroundColor: "#160e26",
                padding: "30px",
                borderRadius: "16px",
                marginTop: "30px",
                border: "1px solid #2a164d"
            }}
        >
            <h2 style={{color:"white"}}>
                Withdrawal History
            </h2>

            {
                withdrawals.map((withdrawal) => (
                    <div
                        key={withdrawal.WithdrawalID}
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            padding: "15px 0",
                            borderBottom: "1px solid #2a164d"
                        }}
                    >
                        <div>
                            <p
                                style={{
                                    margin: "0 0 5px 0",
                                    color: "#ffffff",
                                    fontWeight: "600"
                                }}
                            >
                                Withdrawal #{withdrawal.WithdrawalID}
                            </p>

                            <p
                                style={{
                                    margin: 0,
                                    color: "#a89ec4",
                                    fontSize: "13px"
                                }}
                            >
                                {
                                    new Date(
                                        withdrawal.WithdrawalDate
                                    ).toLocaleString(
                                        "en-IN",
                                        {
                                            dateStyle:"medium",
                                            timeStyle:"short"
                                        }
                                    )
                                }
                            </p>
                        </div>

                        <span
                            style={{
                                color: "red",
                                fontWeight: "bold",
                                fontSize: "18px"
                            }}
                        >
                -₹
                            {Number(
                                withdrawal.Amount
                            ).toLocaleString()}
            </span>
                    </div>
                ))
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
                    onClick={() =>
                        setPage(page - 1)
                    }
                    disabled={page === 1}
                >
                    ← Previous
                </button>

                <span
                    style={{
                        color: "white"
                    }}
                >
        Page {page} of {totalPages || 1}
    </span>

                <button
                    onClick={() =>
                        setPage(page + 1)
                    }
                    disabled={
                        page >= totalPages
                    }
                >
                    Next →
                </button>
            </div>
        </div>
    )
}

export default WithdrawalHistory