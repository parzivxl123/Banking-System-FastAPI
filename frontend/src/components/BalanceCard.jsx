function BalanceCard({ balance }) {
    return (
        <div
            style={{
                backgroundImage: 'linear-gradient(135deg, #44226E 0%, #8342D4 100%)',
                padding: "30px",
                borderRadius: "16px",
                color: "white",
                boxShadow: "0 8px 24px rgba(68, 34, 110, 0.4)",
                border: "1px solid #5a2d91"
            }}
        >
            <h2 style={{ margin: "0 0 10px 0", fontSize: "16px", fontWeight: "400", opacity: 0.9 }}>
                Current Balance
            </h2>

            <h1 style={{ margin: 0, fontSize: "42px", fontWeight: "bold" }}>
                ₹ {balance}
            </h1>
        </div>
    )
}

export default BalanceCard