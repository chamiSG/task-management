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

export interface TaskCreatePayload {
  title: string
  description?: string | null
  status?: TaskStatus
  owner_id: string
}

export interface TaskUpdatePayload {
  title?: string
  description?: string | null
  status?: TaskStatus
}

export interface TaskListResponse {
  items: Task[]
  total: number
  limit: number
  skip: number
}
