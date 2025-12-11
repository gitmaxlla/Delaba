import {
  isRouteErrorResponse,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useNavigate,
} from "react-router";

import type { Route } from "./+types/root";

import styles from "./app.module.scss";
import colors from "app/colors.module.scss";
import GradientBackground from "./components/GradientBackground";

import { useEffect } from "react";
import { authClient, baseClient } from "./store";
import { useGlobalStore } from "./store";

export const links: Route.LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
];

export function Layout({ children }: { children: React.ReactNode }) {
  const { authorized, unauthorize, updateNews, addCompletedLocal, updateTasks, enableModeratorOptions } = useGlobalStore()
 
  useEffect(() => {
    baseClient.post("/auth/refresh").then(() => {
      authClient.get("/tasks/").then((response) => {
        updateTasks(response.data)
      })

      authClient.get("/users/permissions").then((response) => {
        if(Number(response.data) >= 6) {
          enableModeratorOptions()
        }
      })

      authClient.get("/users/data/").then((response) => {
        if ("completed" in response.data) {
          for (const completedId in response.data["completed"]) {
            addCompletedLocal(Number(response.data["completed"][completedId]))
          }
        }
      })

      authClient.get("/news/").then((response) => {
        updateNews(response.data.toReversed())
      })
    }).catch(error => { unauthorize() })
  }, [authorized])

  return (
    <html lang="ru">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" type="image/x-icon" />
        <Meta />
        <Links />
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}

export function HydrateFallback() {
  return <GradientBackground color={colors.primary}>
    <div style={{width: "100%", height: "100%", display: "flex", justifyContent: "center", alignItems: "center"}}>
      <h1 className={styles['loading-message']}>Загрузка</h1>
    </div>
  </GradientBackground>
}

export function ErrorBoundary({ error }: Route.ErrorBoundaryProps) {
  let message = "Ой!";
  let details = "Возникла непредвиденная ошибка.";
  let stack: string | undefined;

  if (isRouteErrorResponse(error)) {
    message = error.status === 404 ? "404" : "Ошибка";
    details =
      error.status === 404
        ? "Запрашиваемая страница не найдена."
        : error.statusText || details;
  } else if (import.meta.env.DEV && error && error instanceof Error) {
    details = error.message;
    stack = error.stack;
  }

  return (
    <GradientBackground color={colors.primary}>
    <main style={{display: "flex", flexDirection: "column", justifyContent: "center", gap: "50px", alignItems: "center", height: "100%", width: "100%"}}>
      <div style={{display: "flex", gap: "100px", alignItems: "center"}}>
        <img style={{width: "300px"}} src="/logo_filled.svg"></img>
        <div style={{width: "7px", borderRadius: "15px", height: "100%", backgroundColor: colors.primary}} />
        <h1 style={{fontSize: "120px", transform: "translateY(-20px)"}}>{message}</h1>
      </div>
      <p style={{color: colors.primary, fontSize: "32px"}}>{details}</p>
      {stack && (
        <pre className="w-full p-4 overflow-x-auto">
          <code>{stack}</code>
        </pre>
      )}
    </main>
    </GradientBackground>
  );
}
