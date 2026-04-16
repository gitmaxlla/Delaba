import { DebouncedSearch } from "~/components/DebouncedSeach"
import Layout, { Content, Header } from "antd/es/layout/layout"
import Sider from "antd/es/layout/Sider"
import { authClient } from "~/store"
import type { Route } from "./+types/home"

import { DownOutlined, NotificationOutlined, NumberOutlined, UserOutlined } from "@ant-design/icons"
import type { SelectProps, TablePaginationConfig } from "antd"
import { ConfigProvider, Dropdown, Flex, Menu, notification, Select, Space, Table, type MenuProps } from "antd"
import Search from "antd/es/input/Search"
import colors from "app/colors.module.scss"
import { useEffect, useRef, useState } from "react"
import type { User } from "~/types"


export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Management Panel" },
    { name: "description", content: "App Management Panel" },
  ]
}

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  try {
    const response = await authClient.get("/users/permissions")
    if (Number(response.data) < 6) {
      throw new Response("", { status: 404 })
    }
  } catch (e: any) {
    if (e.status === 401) {
      throw new Response("", { status: 404 })
    }
  }
}

type MenuItem = Required<MenuProps>['items'][number]

const items: MenuItem[] = [
  { key: '1', icon: <UserOutlined />, label: 'Пользователи' },
  { key: '2', icon: <NotificationOutlined />, label: 'Новости' },
  { key: '3', icon: <NumberOutlined />, label: 'Каналы' },
]

const columns = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
    sorter: true,
    sortDirections: ['ascend', 'descend', 'ascend'],
    defaultSortOrder: 'ascend'
  },

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

export default function Home() {
  const [api, contextHolder] = notification.useNotification()
  const [channels, setChannels] = useState<string[]>([])

  const [selectedChannel, setSelectedChannelIdx] = useState("")
  const [channelUsers, setChannelUsers] = useState<User[]>([])

  const [searching, setSearching] = useState(false)
  const [tableParams, setTableParams] = useState({
    pagination: {
      current: 1,
      pageSize: 10,
      total: 0
    } as TablePaginationConfig
  })

  const [filter, setFilter] = useState({
    newestFirst: true,
    role: [] as string[],
    permissions: [] as number[],
    q: ""
  })

  const permisionFilters: SelectProps['options'] = [
    {
      label: 'Администратор',
      value: 14
    },

    {
      label: 'Модератор',
      value: 6
    },

    {
      label: 'Пользователь',
      value: 2
    },
  ]

  const openNotification = (title: string, description: string) => {
    api.info({
      title: title,
      description: description,
      placement: 'bottomRight'
    })
  }

  useEffect(() => {
    authClient.get("/channels/").then((response) => {
      if (response.status === 200) {
        const channels = response.data
        setChannels(channels)
      }
    })
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => {
      authClient
        .get('/users', {
          params: {
            "page_size": tableParams.pagination.pageSize,
            "page": tableParams.pagination.current - 1,
            "channel": selectedChannel,
            "newest_first": filter.newestFirst,
            "q": filter.q,
            "permissions": filter.permissions,
            "role": filter.role
          }
        })
        .then((response) => {
          setChannelUsers(response.data.values)
          setTableParams({
            ...tableParams, pagination: {
              ...tableParams.pagination,
              total: response.data.total
            }
          })
          setSearching(false)
        })
    }, 1000)


    return () => {
      clearTimeout(timer)
      setSearching(true)
    }

  }, [selectedChannel, tableParams.pagination.current, filter])

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: colors.primary
        }
      }}
    >
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
            <Flex vertical align="stretch" gap="middle">
              <label>Пригласить нового пользователя</label>
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

              <label>Пользователи</label>

              <DebouncedSearch onDebounce={(query) => {
                setFilter({ ...filter, q: query })
              }} loading={searching} />

              <Select placeholder="Роли" onChange={(value: string[]) => {
                setFilter({ ...filter, role: value })
              }} mode="tags" />
              <Select onChange={(value: number[]) => {
                setFilter({ ...filter, permissions: value })
              }} placeholder="Уровень доступа" mode="multiple" options={permisionFilters} />

              <Table
                pagination={tableParams.pagination}
                dataSource={channelUsers}
                columns={columns}
                onChange={(pagination, filters, sorter) => {
                  setFilter({ ...filter, newestFirst: sorter.order == 'ascend' })
                  setTableParams({ pagination })
                }}
              ></Table>
            </Flex>
          </Content>
        </Layout>
      </Layout>
    </ConfigProvider>
  )
}
