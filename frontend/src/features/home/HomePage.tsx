import { Typography } from 'antd'

const { Title, Paragraph } = Typography

export function HomePage() {
  return (
    <>
      <Title level={2}>Welcome</Title>
      <Paragraph>
        React + TypeScript frontend with Vite, Ant Design, React Query, and React Router.
        Use the scalable folder structure under <code>src/</code> to add features.
      </Paragraph>
    </>
  )
}
