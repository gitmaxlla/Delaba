import type { Route } from "./+types/home";
import styles from "app/app.module.scss"
import colors from "app/colors.module.scss"
import { useParams } from "react-router";
import ActionBar from "~/components/ActionBar";
import GradientBackground from "~/components/GradientBackground";
import TaskCard from "~/components/TaskCard";
import { authClient, useGlobalStore } from "~/store";
import { useNavigate } from "react-router";
import type { Task } from "~/types";
import { useEffect, useState, useRef } from "react";
import { redirect } from "react-router";

import { dateToUTC } from "~/util";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Delaba" },
    { name: "description", content: "Tasks assigned to the provided subject." },
  ];
}

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  if (!useGlobalStore.getState().authorized) {
    return redirect("/")
  }
}

export default function Subject() {
    const navigate = useNavigate()
    const { name, focusId } = useParams()
    const { tasks, subjectColors, authorized, moderator, addTask } = useGlobalStore()
    let subject_tasks: Task[] = []

    const [creationMode, setCreationMode] = useState(false)
    const [editMode, setEditMode] = useState(false)

    const [creationTitle, setCreationTitle] = useState("")
    const [creationDeadline, setCreationDeadline] = useState("") 
    const [creationSubtasks, setCreationSubtasks] = useState("")

    const [uploadTodo, setUploadTodo] = useState(true)
    const [file, setFile] = useState<File | null>(null)
    const filePicker = useRef(null)

    const resetCreationData = () => {
      setCreationMode(false)
      setCreationTitle("")
      setCreationDeadline("")
      setCreationSubtasks("")
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

    useEffect(() => {
      if (localStorage.getItem("enable_edit") == "true") {
        setEditMode(true)
      }
    })

    useEffect(() => {
      if (!authorized) {
        navigate("/")
      }
    }, [authorized])


    if (name !== undefined) {
      const available_tasks = tasks.get(name)
      if (available_tasks !== undefined) {
        subject_tasks = available_tasks
      }
    }

    if (subject_tasks === undefined || name === undefined) {
      navigate("/home")
    }

    let min_id = subject_tasks[0].id
    for (let i = 1; i < subject_tasks.length; i++) {
      if (subject_tasks[i].id < min_id) {
        min_id = subject_tasks[i].id
      }
    }

    return(
    <GradientBackground color={colors.primary}>
      <div className={creationMode ? styles["dialog-wrapper"] : styles.hidden}>
        <div className={styles.dialog}>
            <h2>Конструктор задания</h2>

            <div style={{display: "flex", width: "100%", height: "100%", gap: "50px", flexDirection: "row", justifyContent: "space-between"}}>
              <div style={{display: "flex", flexDirection: "column", justifyContent: "start", gap: "20px"}}>
                <input onChange={onTitleChanged} placeholder="Заголовок" value={creationTitle} type="text" className={styles.textbox} />
                <input onChange={onDeadlineChanged} placeholder="Дата сдачи (дд.мм.гггг)" value={creationDeadline} type="text" className={styles.textbox} />
                <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between"}}>
                  <h2 onClick={() => {setUploadTodo(true)}} style={{userSelect: "none", color: colors.primary, opacity: uploadTodo ? 1 : 0.5}}>Задачи</h2>
                  <h2 onClick={() => {setUploadTodo(false)}} style={{userSelect: "none", color: colors.primary, opacity: !uploadTodo ? 1 : 0.5}}>Документ</h2>
                </div>

              </div>

              <div style={{display: "flex", justifyContent: "center", width: "100%", height: "100%"}}>
                {uploadTodo ? 
                <div style={{width: "100%", height: "100%"}}>
                  <textarea style={{border: "3px solid", borderRadius: "15px", width: "100%", height: "100%", resize: "none"}} onChange={onSubtasksChanged} placeholder="Подзадачи (с новой строки)" value={creationSubtasks} className={styles.textbox} />
                </div>:
                
                <div>
                  <button className={styles.button} style={{height: "100%"}} onClick={() => {
                    filePicker.current.click()
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
                    const formData = new FormData()
                    formData.append("file", file as File)
                    formData.append("subject", ""+name)
                    formData.append("title", creationTitle)
                    formData.append("channel", channel)
                    formData.append("deadline", dateToUTC(creationDeadline))

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

      <div style={{display: "flex", width: "100%", height: "100%", gap: "25px", justifyContent: "space-between", flexDirection: "row", alignItems: "center"}}>
          <ActionBar showReturn={true} routeTo="/home" />
          <div style={{display: "flex", width: "100%", overflow: "hidden", height: "100%", justifyContent: "space-between", alignItems: "center", flexDirection: "column"}}>
            <div style={{display: "flex", flexWrap: "wrap", width: "100%", justifyContent: "space-between", padding: "0px 25px", alignItems: "center"}}>
              <h2 style={{color: "black"}}>{name}</h2>
              <h2 style={{fontSize: "1.5em", transform: "translateY(-0.3em)", color: subjectColors.get(name)}}>Всего работ: {subject_tasks.length}</h2>
            </div>
            <div className={styles.tasks}>
              {[...subject_tasks.entries()].map((taskEntry) => (
                  <TaskCard key={taskEntry[1].id} editMode={editMode} toFocusId={focusId} task={taskEntry[1]} num={taskEntry[0]+1}/>
              ))}
              
              <div onClick={() => {setCreationMode(true)}} className={styles["card-subject-compact"]} style={{display: editMode ? "flex" : "none", backgroundColor: "transparent", border: "5px dashed black"}}>
                <div style={{width: "100%", height: "100%", display: "flex", justifyContent: "center", alignItems: "center"}}>
                  <div style={{color: "black", fontSize: "5em", transform: "translateY(-0.1em)", userSelect: "none"}}>+</div>
                </div>
              </div>
            </div>
        </div>
      </div>

    </GradientBackground>);
}
