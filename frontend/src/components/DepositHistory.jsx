import { useEffect, useState } from "react"
import api from "../services/api"

function DepositHistory() {

    const [deposits, setDeposits] = useState([])
    const [page, setPage] = useState(1)
    const [totalDeposits, setTotalDeposits] =
        useState(0)

    const totalPages = Math.ceil(
        totalDeposits / 5
    )
    async function loadDeposits() {
        try {
            const response =
                await api.get(`/deposits/?page=${page}`)

            setDeposits(
                response.data.deposits
            )

            setTotalDeposits(
                response.data.total_deposits
            )
        }
        catch(error) {
            console.log(error)
        }
    }

    useEffect(() => {
        loadDeposits()
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
                Deposit History
            </h2>

            {
                deposits.map((deposit) => (
                    <div
                        key={deposit.DepositID}
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
                                Deposit #{deposit.DepositID}
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
                                        deposit.DepositDate
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
                                color: "#10b981",
                                fontWeight: "bold",
                                fontSize: "18px"
                            }}
                        >
                +₹
                            {Number(
                                deposit.Amount
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

export default DepositHistory