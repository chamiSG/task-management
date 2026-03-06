import { Layout, Menu } from 'antd'
import { Link, Outlet, useLocation } from 'react-router-dom'
import { HomeOutlined, UnorderedListOutlined } from '@ant-design/icons'
import { ROUTES } from '@/lib/constants'

const { Header, Content } = Layout

const navItems = [
  { key: ROUTES.HOME, icon: <HomeOutlined />, label: <Link to={ROUTES.HOME}>Home</Link> },
  { key: ROUTES.TASKS, icon: <UnorderedListOutlined />, label: <Link to={ROUTES.TASKS}>Tasks</Link> },
]

export function AppLayout() {
  const { pathname } = useLocation()
  const selected = pathname === ROUTES.HOME ? ROUTES.HOME : pathname

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
        <span style={{ color: '#fff', fontWeight: 600 }}>Tasks Management</span>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[selected]}
          items={navItems}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Content style={{ padding: 24 }}>
        <Outlet />
      </Content>
    </Layout>
  )
}
