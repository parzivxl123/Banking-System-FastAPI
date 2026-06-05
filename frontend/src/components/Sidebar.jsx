import { useNavigate } from "react-router-dom"

function Sidebar() {
    function handleLogout() {
        localStorage.removeItem("token")
        window.location.href = "/"
    }
    const navigate = useNavigate()

    const navButtonStyle = {
        padding: "12px 16px",
        backgroundColor: "transparent",
        color: "#a89ec4",
        border: "none",
        textAlign: "left",
        fontSize: "16px",
        cursor: "pointer",
        borderRadius: "8px",
        marginBottom: "8px",
        fontWeight: "500",
        transition: "color 0.2s"
    }

    return (
        <div
            style={{
                width: "250px",
                backgroundColor: "#08040f",
                borderRight: "1px solid #2a164d",
                color: "white",
                padding: "30px 20px",
                minHeight: "100vh",
                display: "flex",
                flexDirection: "column",
                boxSizing: "border-box"
            }}
        >
            <h2 style={{ margin: "0 0 40px 0", color: "#ffffff", textAlign: "center", fontWeight: "600" }}>
                BankingSys
            </h2>

            <p style={{ color: "#5a4b81", fontSize: "12px", textTransform: "uppercase", letterSpacing: "1px", marginBottom: "15px", paddingLeft: "16px", fontWeight: "bold" }}>
                Main Menu
            </p>

            <button style={navButtonStyle} onClick={() => navigate("/deposit")}>
                Deposit
            </button>
            <button style={navButtonStyle} onClick={() => navigate("/withdrawal")}>
                Withdrawal
            </button>
            <button style={navButtonStyle} onClick={() => navigate("/transfer")}>
                Transfer
            </button>
            <button style={navButtonStyle} onClick={() => navigate("/analytics")}>
                Statistics
            </button>

            <div style={{ marginTop: "auto" }}>
                <button
                    onClick={handleLogout}
                    style={{
                        ...navButtonStyle,
                        width: "100%",
                        color: "#ef4444",
                        marginBottom: "0"
                    }}
                >
                    Logout
                </button>
            </div>
        </div>
    )
}

export default Sidebar