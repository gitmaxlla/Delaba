import type { Route } from "./+types/home";
import ActionBar from "~/components/ActionBar";
import colors from "app/colors.module.scss";
import styles from "app/app.module.scss";
import Carousel from "~/components/Carousel";
import GradientBackground from "~/components/GradientBackground";
import { useEffect, useRef, useState } from "react";
import { authClient, useGlobalStore } from "~/store";
import { useNavigate } from "react-router";
import { formatDate } from "~/util";
import { redirect } from "react-router";
import { daysUntilDeadline, inflectDayWord } from "~/util";
import { Suspense } from "react";
import { lazy } from "react";

const TaskCreationDialog = lazy(
  () => import("~/components/TaskCreationDialog"),
);

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Главная / Delaba" },
    {
      name: "description",
      content:
        "Новости и меню выбора предмета для перехода к учебным заданиям.",
    },
  ];
}

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
  if (!useGlobalStore.getState().authorized) {
    return redirect("/");
  }
}

clientLoader.hydrate = true;

export default function Home() {
  const { moderator, authorized, news, tasks, subjectColors } =
    useGlobalStore();
  const navigate = useNavigate();

  const [hovering, setHovering] = useState("Delaba AI");
  const [info, setInfo] = useState<string[]>([]);
  const [showCreationDialog, setShowCreationDialog] = useState(false);

  const [externalApiHealthy, setExternalApiHealthy] = useState(true);
  const [userPrompt, setUserPrompt] = useState("");

  const [AIResponse, setAIResponse] = useState("");

  const abortController = useRef<AbortController>(null);
  const [subjects, setSubjects] = useState<string[]>([]);
  useEffect(() => {
    setSubjects(Array.from(tasks.keys()));
  }, [tasks]);

  useEffect(() => {
    if (hovering == "Delaba AI" && externalApiHealthy == false) {
      setAIResponse("Сервис нейросети временно недоступен. Попробуйте позже.");
    }
  }, [externalApiHealthy, hovering]);

  useEffect(() => {
    if (!authorized) {
      navigate("/");
    }
  }, [authorized]);

  useEffect(() => {
    authClient.get("/external/ai/health").catch((response) => {
      if (response.status != 200 || !response.data) {
        setExternalApiHealthy(false);
      }
    });

    return () => {
      if (abortController.current) {
        abortController.current.abort();
      }
    };
  }, []);

  useEffect(() => {
    if (hovering != "Delaba AI") {
      const subject_tasks = tasks.get(hovering);

      if (subject_tasks !== undefined) {
        const numTasks = subject_tasks.length;
        let deadlineClosestDate = new Date(0, 0, 0, 0);
        let deadlineClosest = Number.MAX_VALUE;

        const now = new Date();
        now.setUTCHours(0, 0, 0, 0);

        for (let i = 0; i < subject_tasks.length; i++) {
          const untilDeadline = daysUntilDeadline(subject_tasks[i].deadline);
          deadlineClosestDate = new Date(subject_tasks[i].deadline);
          deadlineClosest = untilDeadline;
          if (untilDeadline > 0) {
            break;
          }
        }

        setInfo([
          `Опубликовано заданий: ${numTasks}`,
          `Ближайший дедлайн: ${deadlineClosestDate.getDate() + "." + deadlineClosestDate.getMonth() + "." + deadlineClosestDate.getFullYear()}`,
          `${deadlineClosest > 0 ? `(осталось ${deadlineClosest} ${inflectDayWord(deadlineClosest)})` : "(прошёл)"}`,
        ]);
      }
    } else {
      setInfo([]);
    }
  }, [hovering]);

  return (
    <GradientBackground color={colors.primary}>
      {moderator ? (
        <Suspense>
          <TaskCreationDialog
            subject=""
            hidden={!showCreationDialog}
            setHidden={setShowCreationDialog}
          />
        </Suspense>
      ) : (
        <></>
      )}

      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <ActionBar showReturn={false} routeTo="/" />

        <Carousel
          subjects={subjects}
          onHover={(subject) => {
            setHovering(subject);
          }}
          onHoverEnd={(subject) => {
            setHovering("Delaba AI");
          }}
          onSelected={(subject) => {
            navigate("/subject/" + subject);
          }}
          onCreate={() => {
            setShowCreationDialog(true);
          }}
        />

        <div className={styles["vertical-apart"]}>
          <div className={styles["news-container"]}>
            <div>
              <h3>Новости</h3>
              <hr />
            </div>
            <div
              style={{
                overflowY: "scroll",
                height: "100%",
                padding: "10px 0px",
              }}
            >
              {news.map((news) => (
                <div
                  key={news.id}
                  style={{
                    marginBottom: "20px",
                    marginRight: "10px",
                    marginLeft: "10px",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "row",
                      justifyContent: "space-between",
                      fontSize: "0.8em",
                      alignItems: "center",
                    }}
                  >
                    <div>{news.by}</div>
                    <div>{formatDate(news.postedAt)}</div>
                  </div>
                  <div style={{ fontWeight: "bolder" }}>
                    {news.section}: {news.title}
                  </div>
                  <p style={{ padding: "0px 15px", fontSize: "0.8em" }}>
                    {news.message}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div
            style={{
              color: "black",
              backgroundColor:
                hovering == "Delaba AI"
                  ? "transparent"
                  : subjectColors.get(hovering),
            }}
            className={styles["subject-hovered-container"]}
          >
            <div>
              <div
                style={{
                  display: "flex",
                  flexDirection: "row",
                  justifyContent: "space-between",
                }}
              >
                <h3>{hovering}</h3>
                {hovering == "Delaba AI" ? (
                  <button
                    aria-label="Generate AI Answer"
                    style={{
                      outline: "1px solid black",
                      padding: "5px",
                      borderRadius: "6px",
                    }}
                    onClick={() => {
                      if (abortController.current) {
                        abortController.current.abort();
                      }

                      setAIResponse("");

                      abortController.current = new AbortController();
                      authClient
                        .post(
                          "/external/ai",
                          {
                            content: userPrompt,
                          },
                          {
                            signal: abortController.current!.signal,
                            timeout: 30000,
                          },
                        )
                        .then((response) => {
                          setAIResponse(response.data.content);
                        })
                        .catch((error) => {
                          if (error.response.status == 500) {
                            setExternalApiHealthy(false);
                          }
                        });
                    }}
                  >
                    {externalApiHealthy ? "Отправить" : "Переподключиться"}
                  </button>
                ) : (
                  <></>
                )}
              </div>
              <hr />
            </div>
            {hovering == "Delaba AI" ? (
              <p>{AIResponse}</p>
            ) : (
              info.map((line) => <span key={line}>{line}</span>)
            )}
            {hovering == "Delaba AI" && externalApiHealthy ? (
              <input
                value={userPrompt}
                onChange={(e) => {
                  setUserPrompt(e.target.value);
                }}
                type="text"
                placeholder="Задайте вопрос по недавним задачам"
              />
            ) : (
              <></>
            )}
          </div>
        </div>
      </div>
    </GradientBackground>
  );
}
