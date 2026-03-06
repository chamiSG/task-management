/** Task status values matching backend enum. */
export type TaskStatus = 'todo' | 'in_progress' | 'done'

export interface Task {
  id: string
  title: string
  description: string | null
  status: TaskStatus
  owner_id: string
  created_at: string
  updated_at: string
}

export interface TaskListResponse {
  items: Task[]
  total: number
  limit: number
  skip: number
}
