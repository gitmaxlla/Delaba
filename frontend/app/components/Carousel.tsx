import styles from "app/app.module.scss";

export default function Carousel({subjects, onHover, onHoverEnd, onSelected}: 
    {subjects: string[], onHover: (subject: string) => void, onHoverEnd: (subject: string) => void, onSelected: (subject: string) => void}) {
    const subjectItems = subjects.map(subject =>
        <div key={subject} onMouseLeave={() => onHoverEnd(subject)} onMouseEnter={() => {onHover(subject)}} 
             onClick={() => {onSelected(subject)}} className={styles['carousel-item']}>
            <p>{subject}</p>
        </div>
    )

    return (
        <div className={styles.carousel}>
            {subjectItems}
        </div>
    )
}