import styles from "app/app.module.scss"

type SubjectHandle = {
    id: number;
    num: number;
    color: string;
}

export default function Checkbox() {
    return (
        <label className={styles['checkbox-container']}>
            <input type="checkbox" />
            <span className={styles.checkbox} />
        </label>
    )
}