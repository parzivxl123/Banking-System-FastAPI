import { useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()

  async function handleLogin() {
    try {
      const formData = new URLSearchParams()

      formData.append("username", email)
      formData.append("password", password)

      const response = await axios.post(
        "http://localhost:8001/login",
        formData
      )

      localStorage.setItem(
        "token",
        response.data.access_token
      )
      navigate("/dashboard")

      console.log(response.data)
    }
    catch(error) {
      console.log(error)
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      backgroundColor: "#0b0614",
      color: "#ffffff",
      fontFamily: "system-ui, sans-serif"
    }}>
      <div style={{
        backgroundColor: "#160e26",
        padding: "40px",
        borderRadius: "16px",
        boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
        border: "1px solid #2a164d",
        width: "100%",
        maxWidth: "400px",
        textAlign: "center"
      }}>
        <h1 style={{ marginBottom: "30px", fontWeight: "600" }}>Banking System</h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          style={{
            width: "100%",
            padding: "14px",
            marginBottom: "15px",
            borderRadius: "8px",
            border: "1px solid #44226E",
            backgroundColor: "#0b0614",
            color: "#ffffff",
            boxSizing: "border-box",
            outline: "none"
          }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          style={{
            width: "100%",
            padding: "14px",
            marginBottom: "25px",
            borderRadius: "8px",
            border: "1px solid #44226E",
            backgroundColor: "#0b0614",
            color: "#ffffff",
            boxSizing: "border-box",
            outline: "none"
          }}
        />

        <button
          onClick={handleLogin}
          style={{
            width: "100%",
            padding: "14px",
            borderRadius: "8px",
            border: "none",
            background: "linear-gradient(to right, #44226E, #8342D4)",
            color: "white",
            fontWeight: "bold",
            fontSize: "16px",
            cursor: "pointer",
            transition: "opacity 0.2s"
          }}
        >
          Login
        </button>
      </div>
    </div>
  )
}

export default Login