import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '@/app/auth/AuthContext'
import { ROUTES } from '@/lib/constants'

/**
 * Renders child routes only when the user is authenticated.
 * Otherwise redirects to the login page, storing the current location
 * so the user can be sent back after logging in.
 */
export function AuthGuard() {
  const { isAuthenticated } = useAuth()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />
  }

  return <Outlet />
}
