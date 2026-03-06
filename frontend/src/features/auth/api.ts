import { apiRequest } from '@/lib/api'

const AUTH_BASE = '/api/v1/auth'

export interface LoginCredentials {
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export async function login(credentials: LoginCredentials): Promise<TokenResponse> {
  return apiRequest<TokenResponse>(`${AUTH_BASE}/login`, {
    method: 'POST',
    body: JSON.stringify(credentials),
  })
}
