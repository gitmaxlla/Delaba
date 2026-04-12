import { authClient } from "~/store"
import { dateToUTC } from "~/util"
import { useState, useRef } from "react"

import { useGlobalStore } from "~/store"

import styles from "app/app.module.scss"
import colors from "app/colors.module.scss"
import type { Task } from "~/types"

export default function TaskCreationDialog(
    {subject, hidden, setHidden}: {subject: string, hidden: boolean, setHidden: (arg0: boolean) => void}) {
    const [creationTitle, setCreationTitle] = useState("")
    const [creationDeadline, setCreationDeadline] = useState("") 
    const [creationSubtasks, setCreationSubtasks] = useState("")

    const [uploadTodo, setUploadTodo] = useState(true)
    const [file, setFile] = useState<File | null>(null)
    const filePicker = useRef<HTMLInputElement>(null)

    const [name, setName] = useState(subject)

    const resetCreationData = () => {
      setHidden(false)
      setCreationTitle("")
      setCreationDeadline("")
      setCreationSubtasks("")
      if (subject == "") setName("")
    }

    const onSubjectChanged = (event: any) => {
        setName(event.target.value)
    }

    const onTitleChanged = (event: any) => {
      setCreationTitle(event.target.value)
    }

    const onDeadlineChanged = (event: any) => {
      setCreationDeadline(event.target.value)
    }

    const onSubtasksChanged = (event: any) => {
      setCreationSubtasks(event.target.value)
    }

    const {addTask} = useGlobalStore()

    return (
        <div className={hidden ? styles.hidden : styles["dialog-wrapper"]}>
        <div className={styles.dialog}>
            <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", width: "100%"}}>
              <h2>Конструктор задания</h2>
              <div style={{display: "flex", gap: "30px", flexDirection: "row", justifyContent: "space-between"}}>
                <h2 onClick={() => {setUploadTodo(true)}} style={{userSelect: "none", color: colors.primary, opacity: uploadTodo ? 1 : 0.5}}>Задачи</h2>
                <h2 onClick={() => {setUploadTodo(false)}} style={{userSelect: "none", color: colors.primary, opacity: !uploadTodo ? 1 : 0.5}}>Документ</h2>
              </div>
            </div>

            <div style={{display: "flex", width: "100%", height: "100%", gap: "50px", flexDirection: "row", justifyContent: "space-between"}}>
              <div style={{display: "flex", flexDirection: "column", justifyContent: "start", gap: "20px"}}>
                {subject == "" ? <input onChange={onSubjectChanged} placeholder="Предмет" value={name} type="text" className={styles.textbox} /> : <></>}
                <input onChange={onTitleChanged} placeholder="Заголовок" value={creationTitle} type="text" className={styles.textbox} />
                <input onChange={onDeadlineChanged} placeholder="Дата сдачи (дд.мм.гггг)" value={creationDeadline} type="text" className={styles.textbox} />
              </div>

              <div style={{display: "flex", justifyContent: "center", width: "100%", height: "100%"}}>
                {uploadTodo ? 
                <div style={{width: "100%", height: "100%"}}>
                  <textarea style={{border: "3px solid", borderRadius: "15px", width: "100%", height: "100%", resize: "none"}} onChange={onSubtasksChanged} placeholder="Подзадачи (с новой строки)" value={creationSubtasks} className={styles.textbox} />
                </div>:
                
                <div>
                  <button className={styles.button} style={{height: "100%"}} onClick={() => {
                    filePicker.current?.click()
                  }}>
                    Нажмите, чтобы выбрать файл (.pdf)
                  </button>
                  <input ref={filePicker} onChange={(event) => {
                    if (event.target.files != undefined) {
                      setFile(event.target.files?.item(0) as File)
                    }
                  }} style={{display: "none"}} type="file" />
                </div>}
              </div>
            </div>

            <div style={{gap: "30px", display: "flex"}}>
              <input type="button" value="Закрыть" onClick={() => {
                resetCreationData()}} 
                className={styles.button} />
              <input onClick={() => {
                authClient.get('/channels/').then((response) => {
                  const channel = response.data[0]

                  if (uploadTodo) {
                    let newTodoTask = {
                      "subject": name,
                      "title": creationTitle,
                      "channel": channel,
                      "subtasks": creationSubtasks.split('\n'),
                      "deadline": dateToUTC(creationDeadline)
                    }

                    authClient.post("/tasks/todo", newTodoTask).then((response) => {
                      const newTaskId = response.data

                      authClient.get("/tasks/"+newTaskId).then((response) => {
                        addTask(response.data as Task)
                      })

                      resetCreationData()
                    })
                  } else if (file != null) {
                    console.log(""+name)

                    const formData = new FormData()
                    formData.append("file", file as File)
                    formData.append("title", creationTitle)
                    formData.append("subject", ""+name)
                    formData.append("deadline", dateToUTC(creationDeadline))
                    formData.append("channel", channel)

                    authClient.post("/tasks/document", formData).then((response) => {
                      const newTaskId = response.data

                      authClient.get("/tasks/"+newTaskId).then((response) => {
                        addTask(response.data as Task)
                      })

                      resetCreationData()
                    })
                  }
                })
              }} type="button" value="Создать" className={styles.button} />
            </div>
        </div>
      </div>
    )
}