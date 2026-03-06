import { useMutation, useQueryClient } from '@tanstack/react-query'
import type { TaskCreatePayload, TaskUpdatePayload } from '@/types'
import { createTask, updateTask } from '../api'

export function useCreateTask() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: TaskCreatePayload) => createTask(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}

export function useUpdateTask() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: TaskUpdatePayload }) => updateTask(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })
}
