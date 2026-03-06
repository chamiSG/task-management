import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'
import { ROUTES } from '@/lib/constants'
import { AppLayout } from '@/components/layout/AppLayout'
import { HomePage } from '@/features/home/HomePage'
import { LoginPage } from '@/app/auth/LoginPage'
import { TasksPage } from '@/features/tasks/TasksPage'
import { AuthGuard } from '@/app/auth/AuthGuard'

const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <AppLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'login', element: <LoginPage /> },
      {
        element: <AuthGuard />,
        children: [{ path: 'tasks', element: <TasksPage /> }],
      },
    ],
  },
  { path: '*', element: <Navigate to={ROUTES.HOME} replace /> },
])

export function AppRouter() {
  return <RouterProvider router={router} />
}
