import { useLoaderData } from "react-router"
import { useSearchParams } from "react-router"
import { DebouncedSearch } from "~/components/DebouncedSearch"
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
    { title: "Панель управления / Delaba" },
    { name: "description", content: "Графическая панель управления данными сервиса Delaba." },
  ]
}

export async function clientLoader({
  request,
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

  const url = new URL(request.url)
  return {
    filter: {
      newestFirst: url.searchParams.get("newest_first") || true,
      role: url.searchParams.get("role") || [] as string[],
      channel: url.searchParams.get("channel") || "" as string,
      permissions: url.searchParams.get("permissions") || [] as number[],
      q: url.searchParams.get("q") || ""
    },

    pagination: {
      current: url.searchParams.get("page") || 1,
      pageSize: url.searchParams.get("page_size") || 10,
      total: url.searchParams.get("total") || 0
    } as TablePaginationConfig
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
  const loader = useLoaderData()
  const [channels, setChannels] = useState<string[]>([])

  const [selectedChannel, setSelectedChannelIdx] = useState(loader.filter.channel)
  const [channelUsers, setChannelUsers] = useState<User[]>([])

  const [filter, setFilter] = useState(loader.filter)

  const [searching, setSearching] = useState(false)
  const [tableParams, setTableParams] = useState({ pagination: loader.pagination })
  const [searchParams, setSearchParams] = useSearchParams()

  console.log(loader)

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
      const resultingQuery = {
        "page_size": tableParams.pagination.pageSize,
        "page": tableParams.pagination.current,
        "channel": selectedChannel,
        "newest_first": filter.newestFirst,
        "q": filter.q,
        "permissions": filter.permissions,
        "role": filter.role
      }

      setSearchParams({ ...resultingQuery }, { replace: true })

      authClient
        .get('/users', {
          params: { ...resultingQuery, "page": resultingQuery.page - 1 }
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

              <DebouncedSearch initial={filter.q} onDebounce={(query) => {
                setFilter({ ...filter, q: query })
              }} loading={searching} />

              <Select placeholder="Роли" value={filter.role} onChange={(value: string[]) => {
                setFilter({ ...filter, role: value })
              }} mode="tags" />
              <Select value={filter.permissions} onChange={(value: number[]) => {
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
