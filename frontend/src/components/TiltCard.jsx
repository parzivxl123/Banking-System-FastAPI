import { useRef } from "react"

function TiltCard({ children }) {
    const cardRef = useRef(null)

    function handleMouseMove(e) {
        const card = cardRef.current

        const rect = card.getBoundingClientRect()

        const x = e.clientX - rect.left
        const y = e.clientY - rect.top

        const middleX = rect.width / 2
        const middleY = rect.height / 2

        const deltaX = x - middleX
        const deltaY = y - middleY

        const rotationY = (deltaX / middleX) * 12
        const rotationX = -(deltaY / middleY) * 12

        card.style.transform =
            `
            translateY(-10px)
            rotateX(${rotationX}deg)
            rotateY(${rotationY}deg)
            `
    }

    function handleMouseLeave() {
        const card = cardRef.current

        card.style.transform =
            "translateY(0) rotateX(0deg) rotateY(0deg)"
    }

    return (
        <div
            style={{
                perspective: "1000px"
            }}
        >
            <div
                ref={cardRef}
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
                style={{
                    transition:
                        "transform 0.15s ease-out, box-shadow 0.3s ease",

                    transformStyle:
                        "preserve-3d",

                    borderRadius: "16px",

                    background: "#160e26",

                    border:
                        "1px solid #2a164d",

                    boxShadow:
                        "0 8px 32px rgba(0,0,0,.3)"
                }}
            >
                {children}
            </div>
        </div>
    )
}

export default TiltCard