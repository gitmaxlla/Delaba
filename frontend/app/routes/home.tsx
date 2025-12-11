import type { Route } from "./+types/home";
import ActionBar from "~/components/ActionBar"
import colors from "app/colors.module.scss"
import styles from "app/app.module.scss"
import Carousel from "~/components/Carousel";
import GradientBackground from "~/components/GradientBackground";
import { useEffect, useState } from "react";
import { useGlobalStore } from "~/store";
import { useNavigate } from "react-router";
import { formatDate } from "~/util";
import { redirect } from "react-router";
import { daysUntilDeadline, inflectDayWord } from "~/util";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Delaba" },
    { name: "description", content: "Tasks grouped by the subject they are assigned to." },
  ];
}

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  if (!useGlobalStore.getState().authorized) {
    return redirect("/")
  }
}

export default function Home() {
  const { authorized, news, tasks, subjectColors } = useGlobalStore()
  const navigate = useNavigate()

  const [hovering, setHovering] = useState("Не выбрано")
  const [info, setInfo] = useState<string[]>([])

  useEffect(() => {
    if (!authorized) {
      navigate("/")
    }
  }, [authorized])
  
  useEffect(() => {
    if (hovering != "Не выбрано") {
      const subject_tasks = tasks.get(hovering)

      if (subject_tasks !== undefined) {
        const numTasks = subject_tasks.length
        let deadlineClosestDate = new Date(0, 0, 0, 0)
        let deadlineClosest = Number.MAX_VALUE

        const now = new Date()
        now.setUTCHours(0, 0, 0, 0)

        for (let i = 0; i < subject_tasks.length; i++) {
          const untilDeadline = daysUntilDeadline(subject_tasks[i].deadline)
            deadlineClosestDate = new Date(subject_tasks[i].deadline)
            deadlineClosest = untilDeadline
            if (untilDeadline > 0) {
              break
            }
        }

        setInfo([`Опубликовано заданий: ${numTasks}`, `Ближайший дедлайн: ${deadlineClosestDate.getDate() + "." + deadlineClosestDate.getMonth() + "." + deadlineClosestDate.getFullYear()}`, `${deadlineClosest > 0? `(осталось ${deadlineClosest} ${inflectDayWord(deadlineClosest)})` : "(прошёл)"}`])
      }
    }
  }, [hovering])

  return <GradientBackground color={colors.primary}>
    <div style={{width: "100%", height: "100%", display: "flex", justifyContent: "space-between", alignItems: "center"}}>
      <ActionBar showReturn={false} routeTo="/" />
      
      <Carousel subjects={Array.from(tasks.keys())}
        onHover={(subject) => {setHovering(subject)}} 
        onHoverEnd={(subject) => {setHovering("Не выбрано")}}
        onSelected={(subject) => {navigate("/subject/" + subject)}} />

      <div className={styles["vertical-apart"]}>
        <div className={styles["news-container"]}>
          <div>
            <h3>Новости</h3>
            <hr/>
          </div>
          <div style={{overflowY: "scroll", height: "100%", padding: "10px 0px"}}>
              {news.map((news) => (
                <div key={news.id} style={{marginBottom: "20px", marginRight: "10px", marginLeft: "10px"}}>
                  <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", fontSize: "0.8em", alignItems: "center"}}>
                    <div>{news.by}</div>
                    <div>{formatDate(news.postedAt)}</div>
                  </div>
                  <div style={{fontWeight: "bolder"}}>{news.section}: {news.title}</div>
                  <p style={{padding: "0px 15px", fontSize: "0.8em"}}>{news.message}</p>
                </div>
              ))}
          </div>
        </div>

        <div style={{backgroundColor: subjectColors.get(hovering), opacity: hovering == "Не выбрано" ? 0.0: 1.0}} className={styles["subject-hovered-container"]}>
          <div>
            <h3>{hovering}</h3>
            <hr/>
          </div>
            {info.map((line) => (
              <p className={styles['hover-info']} style={{opacity: hovering == "Не выбрано" ? 0.0 : 1.0}} key={line}>{line}</p>
            ))}
        </div>
      </div>
    </div>
  </GradientBackground>;
}
