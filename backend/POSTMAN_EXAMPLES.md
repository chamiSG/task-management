# Postman – API Testing Guide

Base URL: **http://127.0.0.1:8000**  
API prefix: **/api/v1**

---

## 1. Health check (no auth)

**GET** `http://127.0.0.1:8000/api/v1/health`

- **Headers:** none  
- **Body:** none  

**Example response (200):**
```json
{
  "status": "ok",
  "service": "Tasks Management API",
  "environment": "development"
}
```

---

## 2. Login (get JWT token)

**POST** `http://127.0.0.1:8000/api/v1/auth/login`

- **Headers:** `Content-Type: application/json`  
- **Body (raw JSON):**

```json
{
  "username": "admin",
  "password": "admin"
}
```

**Example response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Example response (401 – wrong credentials):**
```json
{
  "detail": "Incorrect username or password"
}
```

Use the `access_token` value in the **Authorization** header for protected endpoints (see below).

---

## 3. List tasks (no auth)

**GET** `http://127.0.0.1:8000/api/v1/tasks`

- **Headers:** none  
- **Query params (all optional):**

| Parameter  | Type   | Example                                  | Description        |
|-----------|--------|------------------------------------------|--------------------|
| owner_id  | UUID   | `11111111-1111-1111-1111-111111111111`   | Filter by owner    |
| status    | string | `todo`, `in_progress`, or `done`         | Filter by status   |
| limit     | int    | `10`                                     | Page size (default 50) |
| skip      | int    | `0`                                      | Offset for pagination  |

**Example URLs:**
- All tasks: `http://127.0.0.1:8000/api/v1/tasks`
- With filters: `http://127.0.0.1:8000/api/v1/tasks?status=todo&owner_id=11111111-1111-1111-1111-111111111111&limit=10&skip=0`

**Example response (200):**
```json
{
  "items": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "title": "Finish API docs",
      "description": "Write Postman examples",
      "status": "todo",
      "owner_id": "11111111-1111-1111-1111-111111111111",
      "created_at": "2026-03-06T12:00:00.000000+00:00",
      "updated_at": "2026-03-06T12:00:00.000000+00:00"
    }
  ],
  "total": 1,
  "limit": 10,
  "skip": 0
}
```

---

## 4. Get one task (no auth)

**GET** `http://127.0.0.1:8000/api/v1/tasks/{task_id}`

- **Headers:** none  
- **Path:** replace `{task_id}` with a valid task UUID (e.g. from a previous create or list response).

**Example:** `http://127.0.0.1:8000/api/v1/tasks/a1b2c3d4-e5f6-7890-abcd-ef1234567890`

**Example response (200):**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Finish API docs",
  "description": "Write Postman examples",
  "status": "todo",
  "owner_id": "11111111-1111-1111-1111-111111111111",
  "created_at": "2026-03-06T12:00:00.000000+00:00",
  "updated_at": "2026-03-06T12:00:00.000000+00:00"
}
```

**Example response (404):**
```json
{
  "detail": "Task with id a1b2c3d4-e5f6-7890-abcd-ef1234567890 not found."
}
```

---

## 5. Create task (auth required)

**POST** `http://127.0.0.1:8000/api/v1/tasks`

- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <access_token>` (use token from login)
- **Body (raw JSON):**

```json
{
  "title": "Finish API docs",
  "description": "Write Postman examples for all endpoints",
  "status": "todo",
  "owner_id": "11111111-1111-1111-1111-111111111111"
}
```

**Field rules:**
- `title`: required, 1–200 chars  
- `description`: optional, max 2000 chars  
- `status`: optional, one of `todo`, `in_progress`, `done` (default `todo`)  
- `owner_id`: required, valid UUID  

**Example response (201):**
```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "title": "Finish API docs",
  "description": "Write Postman examples for all endpoints",
  "status": "todo",
  "owner_id": "11111111-1111-1111-1111-111111111111",
  "created_at": "2026-03-06T12:05:00.000000+00:00",
  "updated_at": "2026-03-06T12:05:00.000000+00:00"
}
```

**Example response (401 – no/invalid token):**
```json
{
  "detail": "Could not validate credentials"
}
```

---

## 6. Update task (auth required)

**PUT** `http://127.0.0.1:8000/api/v1/tasks/{task_id}`

- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <access_token>`
- **Path:** replace `{task_id}` with the task UUID to update.
- **Body (raw JSON, all fields optional):**

```json
{
  "title": "Finish API docs (updated)",
  "description": "Include auth and error examples",
  "status": "in_progress"
}
```

**Valid status transitions:**
- `todo` → `in_progress`
- `in_progress` → `done`  
Any other change returns **400**.

**Example response (200):**
```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "title": "Finish API docs (updated)",
  "description": "Include auth and error examples",
  "status": "in_progress",
  "owner_id": "11111111-1111-1111-1111-111111111111",
  "created_at": "2026-03-06T12:05:00.000000+00:00",
  "updated_at": "2026-03-06T12:10:00.000000+00:00"
}
```

**Example response (400 – invalid status transition):**
```json
{
  "detail": "Cannot change status from 'done' to 'todo'."
}
```

**Example response (404):** same shape as Get one task.

---

## 7. Delete task (auth required)

**DELETE** `http://127.0.0.1:8000/api/v1/tasks/{task_id}`

- **Headers:** `Authorization: Bearer <access_token>`  
- **Path:** replace `{task_id}` with the task UUID to delete.  
- **Body:** none  

**Example:** `http://127.0.0.1:8000/api/v1/tasks/b2c3d4e5-f6a7-8901-bcde-f12345678901`

**Example response (204):** empty body.

**Example response (404):**
```json
{
  "detail": "Task with id b2c3d4e5-f6a7-8901-bcde-f12345678901 not found."
}
```

---

## Quick reference

| Method | Endpoint              | Auth  | Purpose        |
|--------|-----------------------|-------|----------------|
| GET    | /api/v1/health        | No    | Health check   |
| POST   | /api/v1/auth/login    | No    | Get JWT        |
| GET    | /api/v1/tasks         | No    | List tasks     |
| GET    | /api/v1/tasks/{id}    | No    | Get one task   |
| POST   | /api/v1/tasks         | Bearer| Create task    |
| PUT    | /api/v1/tasks/{id}    | Bearer| Update task    |
| DELETE | /api/v1/tasks/{id}    | Bearer| Delete task    |

**Suggested test order:**  
1) Health → 2) Login → 3) Create task (copy `id`) → 4) List tasks → 5) Get task by id → 6) Update task → 7) Delete task.

**Postman tip:** In the collection, set a collection variable `base_url` = `http://127.0.0.1:8000` and `token` from the login response; use `{{base_url}}/api/v1/...` and `Authorization: Bearer {{token}}` for protected routes.
