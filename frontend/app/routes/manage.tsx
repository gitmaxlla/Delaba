import type { Route } from "./+types/home"
import Layout, { Content, Footer, Header } from "antd/es/layout/layout"
import Sider from "antd/es/layout/Sider"
import GradientBackground from "~/components/GradientBackground"
import { useGlobalStore } from "~/store"
import { authClient } from "~/store"

import colors from "app/colors.module.scss"
import { Breadcrumb, Button, Dropdown, Flex, Input, Menu, notification, Space, Table, type MenuProps, type NotificationArgsProps } from "antd"
import Search from "antd/es/input/Search"
import { DownOutlined, NotificationOutlined, NumberOutlined, TeamOutlined, UserOutlined } from "@ant-design/icons"
import { NotificationPlacements } from "antd/es/notification/interface"
import { useEffect } from "react"
import { useState } from "react"


export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Management Panel" },
    { name: "description", content: "App Management Panel" },
  ]
}

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  const response = await authClient.get("/users/permissions")
  if (Number(response.data) < 6) {
    throw new Response("", { status: 404 })
  }
}

type MenuItem = Required<MenuProps>['items'][number]

export default function Home() {
  const items: MenuItem[] = [
    { key: '1', icon: <UserOutlined />, label: 'Пользователи' },
    { key: '2', icon: <NotificationOutlined />, label: 'Новости' },
    { key: '3', icon: <NumberOutlined />, label: 'Каналы' },
  ]

  const columns = [
    {
      title: 'Email',
      dataIndex: 'login',
      key: 'email'
    },

    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role'
    },

    {
      title: 'Permissions',
      dataIndex: 'permissions',
      key: 'permissions'
    },
  ]

  const [api, contextHolder] = notification.useNotification()
  const [channels, setChannels] = useState<string[]>([])

  const [selectedChannel, setSelectedChannelIdx] = useState("")
  const [channelUsers, setChannelUsers] = useState("")

  const openNotification = (title: string, description: string) => {
    api.info({
      title: title,
      description: description,
      placement: 'bottomRight'
    })
  }

  useEffect(() => {
    const channels = authClient.get("/channels/").then((response) => {
      if (response.status === 200) {
        const channels = response.data
        setChannels(channels)
      }
    })
  }, [])

  return (
    <>
      {contextHolder}
      <Layout style={{ minHeight: '100vh' }}>
        <Sider style={{ padding: '10px' }}>
          <Menu selectedKeys={['1']} theme="dark" mode="inline" items={items}></Menu>
        </Sider>

        <Layout>
          <Header style={{ background: 'white', fontSize: "30px" }}>
            <Flex justify="space-between">
              <p>Delaba Panel</p>
              <Dropdown destroyOnHidden={false} trigger={['click']} menu={{
                items: channels.map((channel) => {
                  return {
                    key: channel,
                    label: (
                      <a onClick={() => {
                        setSelectedChannelIdx(channel)
                        authClient
                          .get('channels/users', { params: { "channel": selectedChannel } })
                          .then((response) => {
                            setChannelUsers(response.data)
                          })
                      }}>{channel}</a>
                    )
                  }
                })
              }}>
                <Space>
                  <p>{channels?.length == 0 ? "" : selectedChannel}</p>
                  <DownOutlined />
                </Space>
              </Dropdown>
            </Flex>
          </Header>

          <Content style={{ margin: "30px" }}>
            <Space orientation="vertical" size={10}>
              Пригласить нового пользователя
              <Search placeholder="Электронная почта" enterButton="Пригласить"
                onSearch={(value) => {
                  authClient.post("/users/", {
                    login: value,
                    role: "Пользователь",
                    channel: selectedChannel
                  }).then((response) => {
                    if (response.status === 200) {
                      openNotification("Приглашение отправлено", "Данные для входа пользователя отправлены на указанный почтовый адрес.")
                    }
                  })
                }} />
            </Space>

            <Table dataSource={channelUsers} columns={columns}></Table>
          </Content>

          <Footer>

          </Footer>
        </Layout>
      </Layout >
    </>
  )
}
