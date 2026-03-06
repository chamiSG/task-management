import { useState } from 'react'
import { Button, Card, Form, Input, message } from 'antd'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/app/auth'
import { login } from './api'
import { ROUTES } from '@/lib/constants'

export function LoginPage() {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login: setAuth } = useAuth()

  const onFinish = async (values: { username: string; password: string }) => {
    setLoading(true)
    try {
      const res = await login({ username: values.username, password: values.password })
      setAuth(res.access_token, values.username)
      message.success('Logged in')
      navigate(ROUTES.TASKS, { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card title="Log in" style={{ maxWidth: 400, margin: 'auto' }}>
      <Form
        name="login"
        layout="vertical"
        onFinish={onFinish}
        autoComplete="on"
      >
        <Form.Item
          name="username"
          label="Username"
          rules={[{ required: true, message: 'Please enter your username' }]}
        >
          <Input placeholder="Username" />
        </Form.Item>
        <Form.Item
          name="password"
          label="Password"
          rules={[{ required: true, message: 'Please enter your password' }]}
        >
          <Input.Password placeholder="Password" autoComplete="current-password" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>
            Sign in
          </Button>
        </Form.Item>
      </Form>
    </Card>
  )
}
