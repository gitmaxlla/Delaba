import styles from "app/app.module.scss";

export enum ItemIconType {
    Circle,
    Square,
    None
}

export default function ItemIcon({ type }: { type: ItemIconType } ) {
    if (type == ItemIconType.None) {
        return <></>
    } else if (type == ItemIconType.Circle) {
        return <div style={{background: "white", width: "20px", marginRight: "15px", height: "20px", borderRadius: "10px"}}></div>
    } else if (type == ItemIconType.Square) {
        return <div style={{background: "white", width: "20px", marginRight: "15px", height: "20px", borderRadius: "5px"}}></div>
    }
}