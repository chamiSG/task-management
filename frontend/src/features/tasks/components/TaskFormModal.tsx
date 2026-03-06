import { useEffect } from 'react'
import { Form, Input, Modal, Select } from 'antd'
import type { Task, TaskStatus } from '@/types'
import { getCurrentOwnerId } from '@/lib/constants'

const STATUS_OPTIONS: { value: TaskStatus; label: string }[] = [
  { value: 'todo', label: 'Todo' },
  { value: 'in_progress', label: 'In progress' },
  { value: 'done', label: 'Done' },
]

export interface TaskFormValues {
  title: string
  description?: string | null
  status: TaskStatus
}

interface TaskFormModalProps {
  open: boolean
  mode: 'create' | 'edit'
  task?: Task | null
  onClose: () => void
  onSubmit: (values: TaskFormValues) => void
  isLoading?: boolean
}

export function TaskFormModal({
  open,
  mode,
  task,
  onClose,
  onSubmit,
  isLoading = false,
}: TaskFormModalProps) {
  const [form] = Form.useForm<TaskFormValues>()

  useEffect(() => {
    if (open) {
      if (mode === 'edit' && task) {
        form.setFieldsValue({
          title: task.title,
          description: task.description ?? undefined,
          status: task.status,
        })
      } else {
        form.resetFields()
        form.setFieldsValue({ status: 'todo' })
      }
    }
  }, [open, mode, task, form])

  const handleOk = () => {
    form.validateFields().then((values) => {
      onSubmit(values)
    })
  }

  const handleClose = () => {
    form.resetFields()
    onClose()
  }

  return (
    <Modal
      title={mode === 'create' ? 'Create task' : 'Edit task'}
      open={open}
      onOk={handleOk}
      onCancel={handleClose}
      confirmLoading={isLoading}
      destroyOnClose
      okText={mode === 'create' ? 'Create' : 'Save'}
      afterClose={() => form.resetFields()}
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{ status: 'todo' }}
      >
        <Form.Item
          name="title"
          label="Title"
          rules={[
            { required: true, message: 'Please enter a title' },
            { min: 1, message: 'Title is required' },
            { max: 200, message: 'Title must be at most 200 characters' },
          ]}
        >
          <Input placeholder="Task title" maxLength={200} showCount />
        </Form.Item>
        <Form.Item
          name="description"
          label="Description"
          rules={[{ max: 2000, message: 'Description must be at most 2000 characters' }]}
        >
          <Input.TextArea placeholder="Optional description" rows={3} maxLength={2000} showCount />
        </Form.Item>
        <Form.Item name="status" label="Status" rules={[{ required: true }]}>
          <Select options={STATUS_OPTIONS} placeholder="Status" />
        </Form.Item>
      </Form>
    </Modal>
  )
}

export function getCreatePayload(values: TaskFormValues): { title: string; description?: string | null; status: TaskStatus; owner_id: string } {
  return {
    title: values.title.trim(),
    description: values.description?.trim() || null,
    status: values.status,
    owner_id: getCurrentOwnerId(),
  }
}
