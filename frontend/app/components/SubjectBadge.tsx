import Centerer from "./Centerer";
import fonts from "app/fonts.module.scss"
import { replace, useNavigate } from "react-router";
import type { Task } from "~/types";
import { formatDate } from "~/util";

export default function SubjectBadge({ task, num, color  }: {task: Task, num: number, color: string} ) {
    const navigate = useNavigate()
    
    return (
        <div style={{
            userSelect: "none",
            minWidth: "45px",
            minHeight: "45px",
            borderRadius: "50%",
            clipPath: "circle(50% at 50% 50%)",
            background: color
        }} draggable={true} onDragStart={(event) => {
            event.dataTransfer.setData("text/plain", `${task.subject}: "${task.title}" - до ${formatDate(task.deadline)}\n${task.subtasks != null ? task.subtasks.map((subtask) => " - " + subtask).join('\n') : "- (Прикреплённый файл)"}`)
            event.dataTransfer.setData("application/delaba-task", JSON.stringify(task))
        }} onClick={() => {
                navigate(`/subject/${task.subject}/${task.id}`, {replace: true})
        }}>
            <Centerer><span style={{color: "white", fontFamily: fonts.dela, fontSize: "18px", transform: "translate(0px, -2px)"}}>{task.subject[0]+num}</span></Centerer>
        </div>
    )
}