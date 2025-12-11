import styles from "../app.module.scss"
import type { Task } from '../types'
import { authClient, useGlobalStore } from "~/store"

import type { AxiosProgressEvent } from "axios"
import { useState, useEffect, useRef } from "react"
import { formatDate, inflectDayWord } from "~/util"

import { daysUntilDeadline } from "~/util"

export default function TaskCard({task, num, toFocusId, editMode}: {task: Task, num: number, toFocusId: string | undefined, editMode: boolean}) {
    const { subjectColors, completed, pushCompleted, removeTask, popCompleted } = useGlobalStore() 
    const [ downloadProgress, setDownloadProgress ] = useState("0%")
    const ref = useRef(null)
    const [color, setColor] = useState(subjectColors.get(task.subject))    
    const [now, subject_tasks] = useState(new Date())
    const [deadline, setDeadline] = useState(new Date(task.deadline))
    const [untilDeadline, setUntilDeadline] = useState(0)
    const [deadlinePassed, setDeadlinePassed] = useState(false)

    useEffect(() => {
        const daysToDeadline = daysUntilDeadline(task.deadline) 
        setUntilDeadline(daysToDeadline)
        setDeadlinePassed(daysToDeadline <= 0)
        let progress = localStorage.getItem(""+task.id)
        if (progress != null) {
            setDownloadProgress("100%")
        }
    }, [])
    
    useEffect(() => {
        let shouldFocus = false
        if (toFocusId != undefined && task.id+"" == toFocusId) {
            shouldFocus = true
        }

        if (shouldFocus) {
            ref.current?.focus()
        }
    }, [toFocusId])

    return (
        <div onClick={()=> {
            if (completed.has(task.id)) {
                popCompleted(task.id)
            } else {
                pushCompleted(task.id)
            }
        }}tabIndex={0} ref={ref} className={styles["card-subject-compact"]} style={{backgroundColor: color, minWidth: completed.has(task.id) ? "87px" : "300px", opacity: deadlinePassed ? 0.2 : 1.0}}>
            <div style={{display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "space-between"}}>
                <div style={{display: "flex", flexDirection: "column"}}>
                    <h3 style={{fontWeight: "bolder", display: completed.has(task.id) ? "none" : "block"}}>{task.title}</h3>
                    <h3 style={{display: completed.has(task.id) ? "none" : "block"}}>(до {formatDate(task.deadline)} - {deadlinePassed ? "прошёл" : `ещё ${untilDeadline} ${inflectDayWord(untilDeadline)}`})</h3>
                </div>
                <h2>{num}</h2>
            </div>
            <div className={styles["card-page"]} style={{position: "relative", display: completed.has(task.id) ? "none" : "flex"}}>
                {task.type == "document" ?
                <div>
                    <p style={{userSelect: "none", cursor: "pointer"}} onClick={(event) => {
                        event.stopPropagation()
                        localStorage.removeItem(""+task.id)
                        setDownloadProgress("0%")
                        authClient("/tasks/" + task.id + "/file",
                            {responseType: 'blob', onDownloadProgress: (progressEvent: AxiosProgressEvent) => {
                                if (progressEvent.lengthComputable) {
                                    setDownloadProgress(`${Math.trunc((100*progressEvent.loaded) / progressEvent.total)}%`)
                                }
                            }}).then((response) => {
                            const blob = new Blob([response.data], {type: response.headers['content-type']})
                            const url = window.URL.createObjectURL(blob);
                            const link = document.createElement("a")
                            link.href = url
                            link.setAttribute('download', task.subject + "_" + task.title + "_" + task.id + ".pdf")
                            link.click()
                            link.remove()
                            window.URL.revokeObjectURL(url)
                            localStorage.setItem(""+task.id, "")
                            setDownloadProgress("100%")
                        })
                    }}>Нажмите сюда, чтобы скачать документ</p>


                    <div style={{position: "relative"}}>
                        <div style={{position: "absolute", width: downloadProgress, height: "7px", zIndex: 10, transition: "width 0.2s", borderRadius: "10px", marginTop: "10px", backgroundColor: color}} />
                        <div style={{position: "absolute", width: "100%", height: "7px", borderRadius: "10px", marginTop: "10px", backgroundColor: "gray"}} />
                    </div>
                </div>:
                <ul style={{listStyle: "initial"}}>{task.subtasks.map((subtask) => (
                    <li key={subtask}>{subtask}</li>
                ))}</ul>}

                {editMode?
                <button onClick={(event) => {
                    event.stopPropagation()
                    authClient.delete("/tasks/" + (""+task.id)).then(() => {
                        removeTask(task.id)
                    })    
                }} style={{position: "absolute", top: 0, width: "100%", backgroundColor: "black", color: "white", cursor: "crosshair", padding: "20px"}}>
                    Удалить
                </button> 
                :<></>}
            </div>
        </div>
    )
}
