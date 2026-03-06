import { Typography } from 'antd'

const { Title, Paragraph } = Typography

export function HomePage() {
  return (
    <>
      <Title level={2}>Welcome</Title>
      <Paragraph>
        Manage your tasks in one place. Create, update, and track progress from the Tasks page.
      </Paragraph>
    </>
  )
}
