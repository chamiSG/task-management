import { useState } from 'react'
import { Card, Select, Space, Table, Tag, Typography } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useTasks } from './hooks'
import type { Task, TaskStatus } from '@/types'

const PAGE_SIZE = 10
const STATUS_OPTIONS: { value: TaskStatus | ''; label: string }[] = [
  { value: '', label: 'All' },
  { value: 'todo', label: 'Todo' },
  { value: 'in_progress', label: 'In progress' },
  { value: 'done', label: 'Done' },
]

const statusColors: Record<TaskStatus, string> = {
  todo: 'default',
  in_progress: 'processing',
  done: 'success',
}

const columns: ColumnsType<Task> = [
  { title: 'Title', dataIndex: 'title', key: 'title', ellipsis: true },
  {
    title: 'Description',
    dataIndex: 'description',
    key: 'description',
    ellipsis: true,
    render: (val: string | null) => val ?? '—',
  },
  {
    title: 'Status',
    dataIndex: 'status',
    key: 'status',
    width: 120,
    render: (status: TaskStatus) => <Tag color={statusColors[status]}>{status}</Tag>,
  },
  {
    title: 'Created',
    dataIndex: 'created_at',
    key: 'created_at',
    width: 180,
    render: (val: string) => (val ? new Date(val).toLocaleString() : '—'),
  },
]

export function TasksPage() {
  const [page, setPage] = useState(1)
  const [statusFilter, setStatusFilter] = useState<TaskStatus | ''>('')

  const { data, isLoading, isError, error } = useTasks({
    limit: PAGE_SIZE,
    skip: (page - 1) * PAGE_SIZE,
    ...(statusFilter ? { status: statusFilter } : {}),
  })

  const items = data?.items ?? []
  const total = data?.total ?? 0

  return (
    <Card
      title="Task list"
      extra={
        <Space>
          <Typography.Text type="secondary">Status</Typography.Text>
          <Select
            value={statusFilter || undefined}
            onChange={(v) => {
              setStatusFilter((v as TaskStatus | '') ?? '')
              setPage(1)
            }}
            options={STATUS_OPTIONS}
            style={{ width: 140 }}
            allowClear
            placeholder="All"
          />
        </Space>
      }
    >
      <Table<Task>
        rowKey="id"
        columns={columns}
        dataSource={items}
        loading={isLoading}
        pagination={{
          current: page,
          pageSize: PAGE_SIZE,
          total,
          showSizeChanger: false,
          showTotal: (t) => `Total ${t} task${t !== 1 ? 's' : ''}`,
          onChange: (p) => setPage(p),
        }}
        locale={{
          emptyText: isError
            ? `Error: ${error instanceof Error ? error.message : 'Failed to load tasks'}`
            : 'No tasks yet',
        }}
      />
    </Card>
  )
}
