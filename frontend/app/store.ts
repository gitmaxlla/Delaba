import { create } from 'zustand'
import axios from 'axios'
import axiosRetry from 'axios-retry'

import type { Task, News } from './types'
import colors from "app/colors.module.scss"
import { sortByDeadline } from './util'

const server: string = "http://localhost:8000/v1"

export const baseClient = axios.create({
    baseURL: server,
    withCredentials: true
})

export const authClient = axios.create({
    baseURL: server,
    withCredentials: true
})

axiosRetry(authClient, {
    retries: 2,
    retryDelay: axiosRetry.exponentialDelay,
    retryCondition: (error) => {
        return error.response?.status === 401;
    },
    onRetry: (retryCount, error, requestConfig) => {
        console.log("Trying to refresh the access token.")
        baseClient.post("/auth/refresh")
    },
    onMaxRetryTimesExceeded: (error, retryCount) => {}
})

interface GlobalStore {
    authorized: boolean,
    authorize: () => void,
    unauthorize: () => void,
    tasks: Map<string, Task[]>,
    news: News[],
    subjectColors: Map<string, string>,
    updateTasks: (newTasks: Task[]) => void,
    updateNews: (newNews: News[]) => void,
    setColors: (newColors: Map<string, string>) => void,
    completed: Map<number, null>,
    addCompletedLocal: (taskId: number) => void,
    addTask: (task: Task) => void,
    removeTask: (taskId: number) => void,
    removeCompletedLocal: (taskId: number) => void,
    pushCompleted: (taskId: number) => void,
    popCompleted: (taskId: number) => void,
    moderator: boolean,
    enableModeratorOptions: () => void
}

export const useGlobalStore = create<GlobalStore>((set) => ({
    authorized: true,
    news: [],
    enableModeratorOptions: () => set((state) => ({moderator: true})),
    authorize: () => set((state) => ({authorized: true})),
    unauthorize: () => set((state) => ({authorized: false})),
    tasks: new Map<string, Task[]>(),
    subjectColors: new Map<string, string>(),
    setColors: (newColors: Map<string, string>) => set(() => ({subjectColors: newColors})),
    updateTasks: (newTasks: Task[]) => set(() => ({tasks: arrangeTasks(newTasks)})),
    updateNews: (newNews: News[]) => set(() => ({news: newNews})),
    completed: new Map<number, null>(),
    removeTask: (taskId: number) => set((state) => {
        const newTasks = new Map(state.tasks)
        for(const subject of newTasks) {
            newTasks.set(subject[0], newTasks.get(subject[0]).filter((task) => task.id != taskId))
        }   
        return {tasks: newTasks}
    }),
    addTask: (task: Task) => set((state) => {
        const newTasks = new Map(state.tasks)
        const taskSubjectTasks = newTasks.get(task.subject)
        const newSubjectTasks = [...taskSubjectTasks, task]

        sortByDeadline(newSubjectTasks)
        newTasks.set(task.subject, newSubjectTasks)
        return {tasks: newTasks}
    }),
    moderator: false,
    addCompletedLocal: (taskId: number) => set((state) => {
        const newMap = new Map(state.completed)
        newMap.set(taskId, null)        
        return {completed: newMap}
    }),
    removeCompletedLocal: (taskId: number) => set((state) => {
        const newMap = new Map(state.completed)
        newMap.delete(taskId)
        return {completed: newMap}
    }),
    pushCompleted: (taskId: number) => set((state) => {
        const newMap = new Map(state.completed)
        newMap.set(taskId, null)
        authClient.put("/users/data", {"completed": [...newMap.keys()]}).catch((error) => {
            console.log(error)
            useGlobalStore.getState().removeCompletedLocal(taskId)
        })
        
        return {completed: newMap}
    }),
    popCompleted: (taskId: number) => set((state) => {
        const newMap = new Map(state.completed)
        newMap.delete(taskId)
        authClient.put("/users/data", {"completed": [...newMap.keys()]}).catch((error) => {
            console.log(error)
            useGlobalStore.getState().addCompletedLocal(taskId)
        })

        return {completed: newMap}
    }),
}))

function arrangeTasks(tasks: Task[]): Map<string, Task[]> {
    let result = new Map<string, Task[]>()

    const subjects = [...new Set(tasks.map((task) => task.subject))].sort(
        (a, b) => a.localeCompare(b)
    )

    let subject_colors = new Map<string, string>()
    const available_colors = [colors.primary, colors.secondary, colors.tertiary]

    for (const [index, subject] of subjects.entries()) {
        const this_tasks = tasks.filter((task) => task.subject === subject)
        subject_colors.set(subject, available_colors[index % 3])
        sortByDeadline(this_tasks)
        result.set(subject, this_tasks)
    }

    useGlobalStore.getState().setColors(subject_colors)

    return result
}