import colors from "app/colors.module.scss"
import SubjectBadge from "./SubjectBadge"
import { useNavigate } from "react-router"
import { useGlobalStore } from "~/store"
import styles from "app/app.module.scss"
import React from "react"
import { daysUntilDeadline } from "~/util"

export default function ActionBar({ children, showReturn, routeTo }: 
    { children?: React.ReactNode, showReturn: boolean, routeTo: string } ) {
    const navigate = useNavigate()
    const { tasks, subjectColors, completed } = useGlobalStore()

    return (
        <div style={{display: "flex", height: "100%", flexDirection: "column", justifyContent: "center"}}>
            <div style={{
                width: "70px",
                height: "95%",
                display: "flex",
                flexDirection: "column",
                gap: "25px",
                backgroundImage: "linear-gradient(to bottom, #e6d1fc, #b992ff)",
                borderRadius: "25px",
                justifyContent: "space-between",
                alignItems: "center",
                paddingTop: "20px",
                paddingBottom: "20px"
            }}>


                <img src="/back.svg" onClick={() => {navigate(routeTo)}} style={{width: "35px", userSelect: "none", cursor: "pointer", visibility: showReturn ? "visible" : "hidden"}} />
                
                <div className={styles["action-bar-container"]}>
                    {[...tasks.entries()].map((subjectTasks) => (
                        <React.Fragment key={subjectTasks[0]}>
                        {[...subjectTasks[1].entries()].map((indexedTask) => {
                            if (completed.has(indexedTask[1].id)) {
                                return <React.Fragment key={indexedTask[1].id} />
                            }
                            return <SubjectBadge key={indexedTask[1].id} num={indexedTask[0]+1} task={indexedTask[1]} color={subjectColors.get(indexedTask[1].subject)} />
                        })}
                        <div style={{background: "transparent", minWidth: "10px", minHeight: "10px", maxWidth: "10px", maxHeight: "10px", borderRadius: "50%", marginTop: "10px", marginBottom: "10px"}} />
                        </React.Fragment>
                    ))}

                </div>

                <img src="/settings.svg" onClick={() => {navigate("/settings")}} style={{width: "55px", userSelect: "none", cursor: "pointer"}} />

                {children}
            </div>
        </div>
    )
}