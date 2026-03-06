import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

const TOKEN_KEY = 'token'
const USERNAME_KEY = 'username'

interface AuthState {
  token: string | null
  username: string | null
  isAuthenticated: boolean
}

interface AuthContextValue extends AuthState {
  login: (token: string, username: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

function readStored(): AuthState {
  if (typeof window === 'undefined') {
    return { token: null, username: null, isAuthenticated: false }
  }
  const token = localStorage.getItem(TOKEN_KEY)
  const username = localStorage.getItem(USERNAME_KEY)
  return {
    token,
    username,
    isAuthenticated: Boolean(token),
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>(readStored)

  useEffect(() => {
    const onStorage = () => setState(readStored())
    window.addEventListener('storage', onStorage)
    return () => window.removeEventListener('storage', onStorage)
  }, [])

  const login = useCallback((token: string, username: string) => {
    localStorage.setItem(TOKEN_KEY, token)
    localStorage.setItem(USERNAME_KEY, username)
    setState({ token, username, isAuthenticated: true })
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USERNAME_KEY)
    setState({ token: null, username: null, isAuthenticated: false })
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      ...state,
      login,
      logout,
    }),
    [state.token, state.username, state.isAuthenticated, login, logout]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return ctx
}
