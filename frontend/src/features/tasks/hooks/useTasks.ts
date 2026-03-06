import { useQuery } from '@tanstack/react-query'
import type { FetchTasksParams } from '../api'
import { fetchTasks } from '../api'

export function useTasks(params?: FetchTasksParams) {
  return useQuery({
    queryKey: ['tasks', params],
    queryFn: () => fetchTasks(params),
  })
}
