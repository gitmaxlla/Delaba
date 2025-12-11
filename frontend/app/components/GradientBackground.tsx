import styles from "app/app.module.scss"

export default function GradientBackground({ color, children }: {color: string, children: React.ReactNode} ) {
    return (
        <div style={{
            width: "100vw",
            height: "100vh",
            padding: "25px",
            background: `linear-gradient(to bottom, white, ${color + "55"})`
        }}>
            <div className={styles['page']}>
                {children}
            </div>
        </div>
    )
}