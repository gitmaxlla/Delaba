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

import TaskCreationDialog from "~/components/TaskCreationDialog";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Delaba" },
    { name: "description", content: "Tasks assigned to the provided subject." },
  ];
}

interface SubjectParams {
  name: string,
  focusId: string,
}

export async function clientLoader({
  params,
}: { params: SubjectParams }) {
  if (!useGlobalStore.getState().authorized) {
    return redirect("/")
  }
}

export default function Subject() {
  const navigate = useNavigate()
  const { name, focusId } = useParams()
  const { tasks: allTasks, subjectColors, authorized, moderator, addTask } = useGlobalStore()
  const [editMode, setEditMode] = useState(false)
  const [showCreationDialog, setShowCreationDialog] = useState(false)

  const [minID, setMinID] = useState(-1)
  const [tasks, setTasks] = useState<Task[]>([])


  useEffect(() => {
    const availableTasks = allTasks.get(name!)

    if (availableTasks !== undefined) {
      setTasks(availableTasks)
    } else {
      setTasks([])
    }

    setMinID(-1)
    for (let i = 0; i < tasks.length; i++) {
      if (tasks[i].id > minID) {
        setMinID(tasks[i].id)
      }
    }
  }, [allTasks, name])

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

  return (
    <GradientBackground color={colors.primary}>
      <TaskCreationDialog subject={name!} hidden={!showCreationDialog} setHidden={setShowCreationDialog} />

      <div style={{ display: "flex", width: "100%", height: "100%", gap: "25px", justifyContent: "space-between", flexDirection: "row", alignItems: "center" }}>
        <ActionBar showReturn={true} routeTo="/home" />
        <div style={{ display: "flex", width: "100%", overflow: "hidden", height: "100%", justifyContent: "space-between", alignItems: "center", flexDirection: "column" }}>
          <div style={{ display: "flex", flexWrap: "wrap", width: "100%", justifyContent: "space-between", padding: "0px 25px", alignItems: "center" }}>
            <h2 style={{ color: "black" }}>{name}</h2>
            <h2 style={{ fontSize: "1.5em", transform: "translateY(-0.3em)", color: subjectColors.get(name!) }}>Всего работ: {tasks.length}</h2>
          </div>
          <div className={styles.tasks}>
            <div onClick={() => { setShowCreationDialog(true) }} className={styles["card-subject-compact"]} style={{ display: editMode ? "flex" : "none", backgroundColor: "transparent", border: "5px dashed black" }}>
              <div style={{ width: "100%", height: "100%", display: "flex", justifyContent: "center", alignItems: "center" }}>
                <div style={{ color: "black", fontSize: "5em", transform: "translateY(-0.1em)", userSelect: "none" }}>+</div>
              </div>
            </div>

            {Object.entries(tasks).map(([num, task]) => (
              <TaskCard key={task.id} editMode={editMode} toFocusId={focusId} task={task} num={tasks.length - (parseInt(num))} /> // TODO: why's num string?
            ))}
          </div>
        </div>
      </div>

    </GradientBackground>
  )
}
