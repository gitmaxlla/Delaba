import styles from "../app.module.scss"
import type { Task } from '../types'
import { authClient, useGlobalStore } from "~/store"

import type { AxiosProgressEvent } from "axios"
import { useState, useEffect, useRef } from "react"
import { formatDate, inflectDayWord } from "~/util"

import { daysUntilDeadline } from "~/util"

export default function TaskCard({ task, num, toFocusId, editMode }: { task: Task, num: number, toFocusId: string | undefined, editMode: boolean }) {
  const { subjectColors, completed, pushCompleted, removeTask, addTask, updateTask, popCompleted } = useGlobalStore()
  const [downloadProgress, setDownloadProgress] = useState("0%")
  const ref = useRef<HTMLDivElement>(null)
  const [color, setColor] = useState(subjectColors.get(task.subject))
  const [now, subject_tasks] = useState(new Date())
  const [untilDeadline, setUntilDeadline] = useState(0)
  const [deadlinePassed, setDeadlinePassed] = useState(false)

  const [inlineUpdateMode, setInlineUpdateMode] = useState(false)
  const [updatedDeadline, setUpdatedDeadline] = useState(task.deadline)
  const [updatedTitle, setUpdatedTitle] = useState(task.title)

  useEffect(() => {
    const daysToDeadline = daysUntilDeadline(task.deadline)
    setUntilDeadline(daysToDeadline)
    setDeadlinePassed(daysToDeadline <= 0)
    let progress = localStorage.getItem("" + task.id)
    if (progress != null) {
      setDownloadProgress("100%")
    }
  }, [task.deadline])

  useEffect(() => {
    let shouldFocus = false
    if (toFocusId != undefined && task.id + "" == toFocusId) {
      shouldFocus = true
    }

    if (shouldFocus) {
      ref.current?.focus()
    }
  }, [toFocusId])

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "37px" }}>
      {(editMode && !completed.has(task.id)) ? <button onClick={() => {
        setInlineUpdateMode(true)
        setUpdatedDeadline(task.deadline)
        setUpdatedTitle(task.title)
      }} className={styles["edit-button"]} style={{ fontSize: "16px" }}>Редактировать метаданные</button> : <></>}

      {inlineUpdateMode ?
        <div tabIndex={0} ref={ref} className={styles["card-subject-compact"]} style={{ backgroundColor: color, minWidth: completed.has(task.id) ? "87px" : "300px", opacity: (deadlinePassed && !editMode) ? 0.2 : 1.0 }}>
          <div style={{ display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "space-between" }}>
            <div style={{ display: "flex", gap: "10px", position: "relative", flexDirection: "column" }}>
              <input className={styles["card-update-input"]} value={updatedTitle}
                onChange={(e) => {
                  setUpdatedTitle(e.target.value)
                }} />
              <input className={styles["card-update-input"]} value={updatedDeadline}
                onChange={(e) => {
                  setUpdatedDeadline(e.target.value)
                }} />
            </div>
            <h2>{num}</h2>
          </div>
          <div className={styles["card-page"]} style={{ display: "flex", flexDirection: "column", bottom: 0, gap: "20px" }}>
            <button onClick={(event) => {
              event.stopPropagation()

              authClient.patch("/tasks/" + ("" + task.id), {
                title: updatedTitle,
                deadline: updatedDeadline
              }).then((response) => {
                if (response.status === 200) {
                  updateTask(task.id, updatedTitle, updatedDeadline)
                  setInlineUpdateMode(false)
                }
              })
            }} style={{ width: "100%", backgroundColor: color, color: "white", cursor: "crosshair", padding: "20px" }}>
              Готово
            </button>

            <button onClick={(event) => {
              event.stopPropagation()
              setInlineUpdateMode(false)
            }} style={{ width: "100%", backgroundColor: color, color: "white", cursor: "crosshair", padding: "20px" }}>
              Отменить
            </button>
          </div>
        </div>
        :
        <div onClick={() => {
          if (completed.has(task.id)) {
            popCompleted(task.id)
          } else {
            pushCompleted(task.id)
          }
        }} tabIndex={0} ref={ref} className={styles["card-subject-compact"]} style={{ backgroundColor: color, minWidth: completed.has(task.id) ? "87px" : "300px", opacity: (deadlinePassed && !editMode) ? 0.2 : 1.0 }}>
          <div style={{ display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "space-between" }}>
            <div style={{ display: "flex", position: "relative", flexDirection: "column" }}>
              <h3 style={{ fontWeight: "bolder", display: completed.has(task.id) ? "none" : "block" }}>{task.title}</h3>
              <h3 style={{ display: completed.has(task.id) ? "none" : "block" }}>(до {formatDate(task.deadline)} - {deadlinePassed ? "прошёл" : `ещё ${untilDeadline} ${inflectDayWord(untilDeadline)}`})</h3>
            </div>
            <h2>{num}</h2>
          </div>
          <div className={styles["card-page"]} style={{ position: "relative", display: completed.has(task.id) ? "none" : "flex" }}>
            {task.type == "document" ?
              <div onClick={(event) => {
                event.stopPropagation()
                localStorage.removeItem("" + task.id)
                setDownloadProgress("0%")
                authClient("/tasks/" + task.id + "/file",
                  {
                    responseType: 'blob', onDownloadProgress: (progressEvent: AxiosProgressEvent) => {
                      if (progressEvent.lengthComputable) {
                        setDownloadProgress(`${Math.trunc((100 * progressEvent.loaded) / progressEvent.total!)}%`)
                      }
                    }
                  }).then((response) => {
                    const blob = new Blob([response.data], { type: response.headers['content-type'] })
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement("a")
                    link.href = url
                    link.setAttribute('download', task.subject + "_" + task.title + "_" + task.id + ".pdf")
                    link.click()
                    link.remove()
                    window.URL.revokeObjectURL(url)
                    localStorage.setItem("" + task.id, "")
                    setDownloadProgress("100%")
                  })
              }}>
                <p style={{ userSelect: "none", cursor: "pointer" }}>Нажмите сюда, чтобы скачать документ</p>

                <div style={{ position: "relative" }}>
                  <div style={{ position: "absolute", width: downloadProgress, height: "7px", zIndex: 10, transition: "width 0.2s", borderRadius: "10px", marginTop: "10px", backgroundColor: color }} />
                  <div style={{ position: "absolute", width: "100%", height: "7px", borderRadius: "10px", marginTop: "10px", backgroundColor: "gray" }} />
                </div>
              </div> :
              <ul style={{ listStyle: "initial" }}>{task.subtasks.map((subtask) => (
                <li key={subtask}>{subtask}</li>
              ))}</ul>}

            {editMode ?
              <button onClick={(event) => {
                event.stopPropagation()
                authClient.delete("/tasks/" + ("" + task.id)).then(() => {
                  updateTask(task.id, updatedTitle, updatedDeadline)
                })
              }} style={{ position: "absolute", top: 0, width: "100%", backgroundColor: "black", color: "white", cursor: "crosshair", padding: "20px" }}>
                Удалить
              </button>
              : <></>}
          </div>
        </div>
      }
    </div >
  )
}
