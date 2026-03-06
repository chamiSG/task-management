import { QueryClientProvider } from '@tanstack/react-query'
import type { ReactNode } from 'react'
import { queryClient } from './query-client'
import { AntdProvider } from './antd-provider'
import { AuthProvider } from '@/app/auth/AuthContext'

export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AntdProvider>
        <AuthProvider>{children}</AuthProvider>
      </AntdProvider>
    </QueryClientProvider>
  )
}
