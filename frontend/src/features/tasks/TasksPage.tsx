import { useState } from 'react'
import { Button, Card, message, Select, Space, Table, Tag, Typography } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useTasks, useCreateTask, useUpdateTask } from './hooks'
import { TaskFormModal, getCreatePayload } from './components'
import type { Task, TaskStatus } from '@/types'
import type { TaskFormValues } from './components/TaskFormModal'

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

function getColumns(openEdit: (record: Task) => void): ColumnsType<Task> {
  return [
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
    {
      title: 'Actions',
      key: 'actions',
      width: 100,
      render: (_: unknown, record: Task) => (
        <Button type="link" size="small" onClick={() => openEdit(record)}>
          Edit
        </Button>
      ),
    },
  ]
}

export function TasksPage() {
  const [page, setPage] = useState(1)
  const [statusFilter, setStatusFilter] = useState<TaskStatus | ''>('')
  const [modalOpen, setModalOpen] = useState(false)
  const [modalMode, setModalMode] = useState<'create' | 'edit'>('create')
  const [editingTask, setEditingTask] = useState<Task | null>(null)

  const { data, isLoading, isError, error } = useTasks({
    limit: PAGE_SIZE,
    skip: (page - 1) * PAGE_SIZE,
    ...(statusFilter ? { status: statusFilter } : {}),
  })
  const createMutation = useCreateTask()
  const updateMutation = useUpdateTask()

  const items = data?.items ?? []
  const total = data?.total ?? 0

  const openCreate = () => {
    setModalMode('create')
    setEditingTask(null)
    setModalOpen(true)
  }
  const openEdit = (record: Task) => {
    setModalMode('edit')
    setEditingTask(record)
    setModalOpen(true)
  }
  const handleModalSubmit = (values: TaskFormValues) => {
    if (modalMode === 'create') {
      createMutation.mutate(getCreatePayload(values), {
        onSuccess: () => {
          message.success('Task created')
          setModalOpen(false)
        },
        onError: (e) => message.error(e instanceof Error ? e.message : 'Failed to create task'),
      })
    } else if (editingTask) {
      updateMutation.mutate(
        {
          id: editingTask.id,
          payload: {
            title: values.title.trim(),
            description: values.description?.trim() || null,
            status: values.status,
          },
        },
        {
          onSuccess: () => {
            message.success('Task updated')
            setModalOpen(false)
          },
          onError: (e) => message.error(e instanceof Error ? e.message : 'Failed to update task'),
        }
      )
    }
  }

  const columns = getColumns(openEdit)

  return (
    <>
      <Card
        title="Task list"
        extra={
          <Space>
            <Button type="primary" onClick={openCreate}>
              Create task
            </Button>
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
      <TaskFormModal
        open={modalOpen}
        mode={modalMode}
        task={editingTask}
        onClose={() => setModalOpen(false)}
        onSubmit={handleModalSubmit}
        isLoading={createMutation.isPending || updateMutation.isPending}
      />
    </>
  )
}
