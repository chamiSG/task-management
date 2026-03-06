import { QueryClientProvider } from '@tanstack/react-query'
import type { ReactNode } from 'react'
import { queryClient } from './query-client'
import { AntdProvider } from './antd-provider'

export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AntdProvider>{children}</AntdProvider>
    </QueryClientProvider>
  )
}
