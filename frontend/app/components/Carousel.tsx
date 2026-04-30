import styles from "app/app.module.scss";
import { useEffect, useState } from "react";

export default function Carousel({
  subjects,
  onHover,
  onHoverEnd,
  onSelected,
  onCreate,
}: {
  subjects: string[];
  onHover: (subject: string) => void;
  onHoverEnd: (subject: string) => void;
  onSelected: (subject: string) => void;
  onCreate: () => void;
}) {
  const [editMode, setEditMode] = useState(false);
  useEffect(() => {
    if (localStorage.getItem("enable_edit") == "true") {
      setEditMode(true);
    }
  }, []);

  return (
    <div className={styles.carousel}>
      {subjects.map((subject) => (
        <div
          key={subject}
          onMouseLeave={() => onHoverEnd(subject)}
          onMouseEnter={() => {
            onHover(subject);
          }}
          onClick={() => {
            onSelected(subject);
          }}
          className={styles["carousel-item"]}
        >
          <p>{subject}</p>
        </div>
      ))}

      {editMode ? (
        <div
          onClick={onCreate}
          aria-label="Add Task"
          className={styles["carousel-item"]}
          style={{
            background: "transparent",
            border: "3px dashed black",
            margin: "0px 15px",
          }}
        >
          <p>Добавить предмет</p>
        </div>
      ) : (
        <></>
      )}
    </div>
  );
}

