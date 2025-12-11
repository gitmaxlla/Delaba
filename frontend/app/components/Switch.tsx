import styles from "app/app.module.scss"

export default function Switch({ checked, onChange = (checked) => {} }: {checked: boolean, onChange: (arg0: boolean) => void} ) {
    return (
        <label className={styles.switch}>
            <input type="checkbox" checked={checked} onChange={(e) => {onChange(e.target.checked)}} />
            <span className={styles.slider} />
        </label>
    )
}