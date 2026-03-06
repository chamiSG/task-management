const API_BASE = import.meta.env.VITE_API_BASE_URL ?? ''

export function getApiUrl(path: string): string {
  const p = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE}${p}`
}

function getAuthHeaders(): Record<string, string> {
  const token = localStorage.getItem('token')
  if (!token) return {}
  return { Authorization: `Bearer ${token}` }
}

export async function apiRequest<T>(
  path: string,
  options?: RequestInit & { params?: Record<string, string> }
): Promise<T> {
  const { params, ...init } = options ?? {}
  let url = getApiUrl(path)
  if (params && Object.keys(params).length > 0) {
    const search = new URLSearchParams(params).toString()
    url += (url.includes('?') ? '&' : '?') + search
  }
  const res = await fetch(url, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
      ...init.headers,
    },
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error((body as { detail?: string })?.detail ?? res.statusText)
  }
  return res.json() as Promise<T>
}
