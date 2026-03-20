import type { Route } from "./+types/home"
import Layout, { Content, Footer, Header } from "antd/es/layout/layout"
import Sider from "antd/es/layout/Sider"
import GradientBackground from "~/components/GradientBackground"
import { useGlobalStore } from "~/store"
import { authClient } from "~/store"

import colors from "app/colors.module.scss"
import { Breadcrumb, Button, Dropdown, Input, Menu, notification, Space, type MenuProps, type NotificationArgsProps } from "antd"
import Search from "antd/es/input/Search"
import { UserOutlined } from "@ant-design/icons"
import { NotificationPlacements } from "antd/es/notification/interface"
import { useEffect } from "react"
import { useState } from "react"

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Management Panel" },
    { name: "description", content: "App Management Panel" },
  ]
}

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  const response = await authClient.get("/users/permissions")
  if(Number(response.data) < 6) {
    throw new Response("", {status: 404})
  }
}

type MenuItem = Required<MenuProps>['items'][number]

export default function Home() {
  const items: MenuItem[] = [
    { key: '1', icon: <UserOutlined/>, label: 'Пользователи' }
  ]

  const [api, contextHolder] = notification.useNotification()
  const [channels, setChannels] = useState<MenuProps['items']>([])
  const [selectedChannelIdx, setSelectedChannelIdx] = useState(0)

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
        const result = []
        channels.forEach((channel, index) => {
          result.push({key: index, label: channel})
        })

        setChannels(result)
      }
    })
  }, [])

  return (
    <>
      {contextHolder}
      <Layout style={{minHeight: '100vh'}}>
        <Sider style={{padding: '10px'}}>
          <Menu selectedKeys={['1']} theme="dark" mode="inline" items={items}></Menu>
        </Sider>
        
        <Layout>
          <Header style={{background: 'white', fontSize: "30px"}}>
            <Space orientation="horizontal">
              Delaba Panel
              <Dropdown menu={channels}>
              </Dropdown>
            </Space>
          </Header>

          <Content style={{margin: "30px"}}>
            <Space orientation="vertical" size={10}>
              Пригласить нового пользователя
              <Search placeholder="Электронная почта" enterButton="Пригласить"
                onSearch={(value) => {
                  authClient.post("/users/", {
                    login: value,
                    role: "Пользователь",
                    channel: ""
                  }).then((response) => {
                    if (response.status === 200) {
                      openNotification("Приглашение отправлено", "Данные для входа пользователя отправлены на указанный почтовый адрес.")
                    }
                  })
                }}/>
            </Space>
          </Content>

          <Footer>

          </Footer>
        </Layout>
      </Layout>
    </>
  )
}