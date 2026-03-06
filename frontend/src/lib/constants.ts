/** App route paths - single source of truth for URLs. */
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  TASKS: '/tasks',
} as const

/** Default owner_id when not provided by auth (e.g. demo). Replace with value from login when available. */
export const DEMO_OWNER_ID = '00000000-0000-0000-0000-000000000001'

export function getCurrentOwnerId(): string {
  return typeof localStorage !== 'undefined' ? localStorage.getItem('owner_id') ?? DEMO_OWNER_ID : DEMO_OWNER_ID
}
