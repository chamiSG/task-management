# Tasks Management – Frontend

React + TypeScript app with Vite, Ant Design, React Query, and React Router.

## Setup

```bash
cd frontend
npm install
```

## Scripts

- `npm run dev` – start dev server (port 3000, proxies `/api` to backend)
- `npm run build` – production build
- `npm run preview` – preview production build
- `npm run lint` – run ESLint

## Folder structure (scalable)

```
src/
  app/              # App shell: router, providers
  components/       # Shared UI (layout, common components)
  features/         # Feature modules (e.g. home, auth, tasks)
  lib/              # Utilities, constants, API client
  types/            # Shared TypeScript types
  styles/           # Global styles
```

Add new features under `features/<name>/` with their own components, hooks, and API calls. Use `lib/` for shared code and `@/` path alias in imports.
