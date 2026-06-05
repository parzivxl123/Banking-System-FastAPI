function ActionButtons({setHistoryType}) {
  const btnStyle = {
    padding: "14px 24px",
    backgroundColor: "#160e26",
    color: "#ffffff",
    border: "1px solid #44226E",
    borderRadius: "12px",
    fontSize: "15px",
    fontWeight: "bold",
    cursor: "pointer",
    flex: 1,
    boxShadow: "0 4px 12px rgba(0,0,0,0.2)"
  };

  return (
<div
  style={{
    display: "flex",
        gap: "15px",
        marginTop: "30px"
  }}
>
  <button
    style={btnStyle}
    onClick={() =>
      setHistoryType("deposits")
    }
  >
    Deposit
  </button>

  <button
    style={btnStyle}
    onClick={() =>
      setHistoryType("withdrawals")
    }
  >
    Withdraw
  </button>

  <button
    style={btnStyle}
    onClick={() =>
      setHistoryType("transactions")
    }
  >
    Transfer
  </button>
</div>
  )
}





export default ActionButtons