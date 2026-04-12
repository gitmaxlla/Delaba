import styles from "app/app.module.scss";
import colors from "app/colors.module.scss"

import ItemIcon from "./ItemIcon";
import { ItemIconType } from "./ItemIcon"

export default function ListItem({ title, icon, highlight }: { title: string, icon: ItemIconType, highlight: boolean } ) {
    return (
        <div style={{color: highlight? colors.primary : "white", backgroundColor: highlight? "white": ""}} className={styles['list-item']}>
            <ItemIcon type={icon} />
            {title}
        </div>
    )
}