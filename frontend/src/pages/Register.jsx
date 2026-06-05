import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../services/api"

function Register() {

    const navigate = useNavigate()

    const [username, setUsername] =
        useState("")

    const [email, setEmail] =
        useState("")

    const [password, setPassword] =
        useState("")

    async function handleRegister(e) {

        e.preventDefault()

        try {

            await api.post(
                "/users/register",
                {
                    UserName: username,
                    UserEmail: email,
                    UserPassword: password
                }
            )

            alert(
                "Account created successfully, Please Check your Mail and verify your account to log in"
            )

            navigate("/")

        }
        catch(error) {

            console.log(error)

            alert(
                "Registration failed"
            )
        }
    }

    return (
        <div
            style={{
                padding: "40px"
            }}
        >
            <h1>Create Account</h1>

            <form
                onSubmit={handleRegister}
            >
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) =>
                        setUsername(
                            e.target.value
                        )
                    }
                />

                <br /><br />

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) =>
                        setEmail(
                            e.target.value
                        )
                    }
                />

                <br /><br />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) =>
                        setPassword(
                            e.target.value
                        )
                    }
                />

                <br /><br />

                <button
                    type="submit"
                >
                    Create Account
                </button>
            </form>
        </div>
    )
}

export default Register