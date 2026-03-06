import { apiRequest } from '@/lib/api'
import type { Task, TaskListResponse, TaskCreatePayload, TaskUpdatePayload } from '@/types'

const BASE = '/api/v1/tasks'

export interface FetchTasksParams {
  owner_id?: string
  status?: string
  limit?: number
  skip?: number
}

type RawTask = Task & { _id?: string }
type RawListResponse = { items: RawTask[]; total: number; limit: number; skip: number }

export async function fetchTasks(params?: FetchTasksParams): Promise<TaskListResponse> {
  const search: Record<string, string> = {}
  if (params?.limit != null) search.limit = String(params.limit)
  if (params?.skip != null) search.skip = String(params.skip)
  if (params?.owner_id) search.owner_id = params.owner_id
  if (params?.status) search.status = params.status
  const raw = await apiRequest<RawListResponse>(
    BASE,
    { params: Object.keys(search).length ? search : undefined }
  )
  return {
    ...raw,
    items: raw.items.map((item) => ({
      ...item,
      id: item.id ?? item._id ?? '',
    })),
  }
}

export async function fetchTask(id: string): Promise<Task> {
  const raw = await apiRequest<Task & { _id?: string }>(`${BASE}/${id}`)
  return {
    ...raw,
    id: raw.id ?? raw._id ?? id,
  }
}

export async function createTask(payload: TaskCreatePayload): Promise<Task> {
  const raw = await apiRequest<Task & { _id?: string }>(BASE, {
    method: 'POST',
    body: JSON.stringify({
      title: payload.title,
      description: payload.description ?? null,
      status: payload.status ?? 'todo',
      owner_id: payload.owner_id,
    }),
  })
  return {
    ...raw,
    id: raw.id ?? raw._id ?? '',
  }
}

export async function updateTask(id: string, payload: TaskUpdatePayload): Promise<Task> {
  const raw = await apiRequest<Task & { _id?: string }>(`${BASE}/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
  return {
    ...raw,
    id: raw.id ?? raw._id ?? id,
  }
}
