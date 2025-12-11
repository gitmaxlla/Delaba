export interface Task {
    channel: string,
    createdAt: string,
    deadline: string,
    fileHash: string | null,
    id: number,
    modifiedAt: string,
    subject: string,
    title: string,
    type: string,
    subtasks: string[]
}

export interface News {
    bound_task_id: number | null,
    by: string,
    channel: string,
    id: number,
    message: string,
    modifiedAt: string,
    postedAt: string,
    section: string,
    title: string
}