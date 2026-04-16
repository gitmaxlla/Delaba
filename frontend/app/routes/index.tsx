import GradientBackground from "~/components/GradientBackground";
import OnboardingPager from "~/components/OnboardingPager"
import { baseClient } from "~/store"

import type { Route } from "./+types/index";

import styles from "app/app.module.scss";
import colors from "app/colors.module.scss";
import { useNavigate } from "react-router";
import { useEffect, useState } from "react";
import { useGlobalStore } from "app/store";
import { redirect } from "react-router";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Вход / Delaba" },
    { name: "description", content: "Лендинг и страница авторизации в приложение Delaba." },
  ];
}

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  if (useGlobalStore.getState().authorized) {
    return redirect("/home")
  }
}

export default function Index() {
  const { authorized, authorize, unauthorize } = useGlobalStore()
  const navigate = useNavigate()

  const [login, setLogin] = useState("")
  const [password, setPassword] = useState("")

  const [newPassword, setNewPassword] = useState("")
  const [newPasswordCheck, setNewPasswordCheck] = useState("")

  const [initMode, setInitMode] = useState(false)

  const [errorMsg, setErrorMsg] = useState("")

  const loginChanged = (event: any) => {
    setLogin(event.target.value)
  }

  const passwordChanged = (event: any) => {
    setPassword(event.target.value)
  }

  const newPasswordChanged = (event: any) => {
    setNewPassword(event.target.value)
  }

  const newPasswordCheckChanged = (event: any) => {
    setNewPasswordCheck(event.target.value)
  }

  const authenticate = () => {
    setErrorMsg("")
    initMode ? initUser() : logIn()
  }

  function logIn() {
    baseClient.post("/auth/login", {
      login: login,
      password: password
    }).then((response) => {
      if (response.status == 200) {
        authorize()
        navigate("/home", { replace: true })
      }
    }).catch((error) => {
      const status = error.response.status
      const msg = error.response.data.detail as string
      // TODO: not very robust, but alright as a quick fix
      if (msg.includes("banned")) {
        setErrorMsg("Доступ заблокирован")
      } else if (status == 403) {
        setInitMode(true)
      } else if (status == 404) {
        setErrorMsg("Пользователь не найден")
      } else if (status == 401) {
        setErrorMsg("Неверный пароль")
      }
    })
  }

  function initUser() {
    if (newPassword == newPasswordCheck) {
      baseClient.post("/auth/init", {
        login: login,
        init_password: password,
        new_password: newPassword,
      }).then((response) => {
        if (response.status == 200) {
          authorize()
          navigate("/home", { replace: true })
        }
      }).catch((error) => {
        if (error.response.status == 401) {
          setErrorMsg("Неверный токен создания")
        }
      })
    } else {
      setErrorMsg("Пароли не совпадают")
    }
  }

  useEffect(() => {
    const authenticateOnEnter = (e: KeyboardEvent) => {
      if (e.key == 'Enter') authenticate()
    }

    document.addEventListener('keydown', authenticateOnEnter)
    return () => { document.removeEventListener('keydown', authenticateOnEnter) }
  }, [])

  return (
    <GradientBackground color={colors.primary}>
      <div style={{ height: "100%", width: "100%", display: "flex", flexWrap: "wrap", justifyContent: "space-around", alignItems: "center", gap: "50px" }}>
        <main style={{ display: "flex", flexDirection: "column", justifyContent: "space-around", alignItems: "center" }}>
          <div style={{ display: "flex", flexDirection: "row", gap: "20px" }}>
            {initMode ? <img alt="'Go back' arrow" style={{ width: "60px", transform: "rotate(-90deg)" }} onClick={() => {
              setErrorMsg("")
              setInitMode(false)
            }} src="/back.svg" /> : <></>}
            <h1 className={styles.h1} style={{ color: colors.primary }}>Делаба ☺</h1>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            {errorMsg !== "" ? <h2 style={{ color: colors.secondary, textAlign: "center", fontSize: "2em" }}>{errorMsg}</h2> : <></>}
            {initMode ?
              <>
                <input onChange={newPasswordChanged} value={newPassword} placeholder="Новый пароль" type="password" className={styles.textbox} />
                <input onChange={newPasswordCheckChanged} value={newPasswordCheck} placeholder="Повторите пароль" type="password" className={styles.textbox} />
              </> :
              <>
                <input onChange={loginChanged} value={login} placeholder="Логин" type="text" autoComplete="username" className={styles.textbox} />
                <input onChange={passwordChanged} value={password} placeholder="Пароль" type="password" autoComplete="password" className={styles.textbox} />
              </>
            }
          </div>

          <div
            role="banner"
            style={{ position: "relative", width: "300px", height: "300px" }} title="Войти"
            onClick={authenticate}
          >
            <input type="submit" hidden onSubmit={authenticate} />
            <img fetchPriority="high" alt="Delaba app logo with an arrow in a circular outline." className={styles['logo-main']} src="./logo.svg" />
            <img fetchPriority="high" alt="Delaba app logo win an arrow in a filled circle" className={styles['logo-hover']} src="./logo_filled.svg" />
          </div>
        </main>

        <aside>
          <OnboardingPager />
        </aside>
      </div>
    </GradientBackground>
  );
}
