import type { Route } from "./+types/home"
import Layout from "antd/es/layout/layout"
import Sider from "antd/es/layout/Sider"
import GradientBackground from "~/components/GradientBackground"
import { useGlobalStore } from "~/store"
import { authClient } from "~/store"

import colors from "app/colors.module.scss"

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

export default function Home() {
  return (
    <Layout>
      <Sider>

      </Sider>
    </Layout>
  )
}