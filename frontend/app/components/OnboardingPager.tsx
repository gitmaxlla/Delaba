import Centerer from "./Centerer";
import styles from "../app.module.scss"
import colors from "app/colors.module.scss";
import { useState } from "react";

export default function OnboardingPager() {
    const [page, setPage] = useState(0)
    const pages: {[key: number]: React.ReactElement} = {
        0: <>Где лаба?<br />- Делаба</>,
        1: <>Все учебные задания в одном месте</>,
        2: <>Планируй учёбу эффективно!</>
    }

    return (
        <div style={{display: "flex", alignItems: "end", flexDirection: "column", gap: "20px"}}>
            <div style={{
                width: "550px",
                height: "400px",
                background: colors.primary,
                borderRadius: "30px",
                boxShadow: `0px 5px 5px ${colors.primary + "55"}`,
                display: "flex",
                justifyContent: "center",
                alignItems: "end"
            }}>
                <div style={{
                    width: "450px",
                    height: "350px",
                    background: "white",
                    borderRadius: "30px 30px 0px 0px",
                }}>
                    <Centerer>
                        <h2 className={styles.h2} style={{padding: "20px", textWrap: "wrap"}}>
                            {pages[page]}
                        </h2>
                    </Centerer>
                </div>
            </div>
            
            <div style={{paddingRight: "50px", display: "flex", gap: "20px"}}>
                <div onClick={() => {setPage(0)}} style={{borderRadius: "50%", width: "15px", height: "15px", background: (page != 0) ? `${colors.primary + "55"}` : colors.primary}} />
                <div onClick={() => {setPage(1)}} style={{borderRadius: "50%", width: "15px", height: "15px", background: (page != 1) ? `${colors.primary + "55"}` : colors.primary}} />
                <div onClick={() => {setPage(2)}} style={{borderRadius: "50%", width: "15px", height: "15px", background: (page != 2) ? `${colors.primary + "55"}` : colors.primary}} />
            </div>
        </div>
    )
}