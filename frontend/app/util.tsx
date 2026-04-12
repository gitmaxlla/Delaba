import type { Task } from "./types"

export function formatDate(date: string) {
    const dateObj = new Date(date)
    return dateObj.getDate() + "." + dateObj.getMonth() + "." + dateObj.getFullYear()
}

export function daysUntilDeadline(deadline: string) {
    const now = new Date()
    now.setUTCHours(0, 0, 0, 0)

    const deadlineDate = new Date(deadline)
    deadlineDate.setUTCHours(0, 0, 0, 0)
    
    const daysUntilDeadline = Math.trunc((deadlineDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
    return daysUntilDeadline
}

export function inflectDayWord(days: number) {
    if (days % 10 >= 2 && days % 10 <= 4) {
        return "дня"
    }
    return "дней"
}

export function dateToUTC(date: string) {
    const d_m_y = date.split('.').map((num) => Number(num))
    return new Date(Date.UTC(d_m_y[2], d_m_y[1], d_m_y[0])).toISOString()
}

export function sortByDeadline(tasks: Task[]) {
    tasks.sort((a,b) => (Number(new Date(a.deadline)) - Number(new Date(b.deadline))))
}
