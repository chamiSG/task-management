import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'
import { ROUTES } from '@/lib/constants'
import { AppLayout } from '@/components/layout'
import { HomePage } from '@/features/home'
import { LoginPage } from '@/features/auth'
import { TasksPage } from '@/features/tasks/TasksPage'

const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <AppLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'login', element: <LoginPage /> },
      { path: 'tasks', element: <TasksPage /> },
    ],
  },
  { path: '*', element: <Navigate to={ROUTES.HOME} replace /> },
])

export function AppRouter() {
  return <RouterProvider router={router} />
}
