import GradientBackground from "~/components/GradientBackground";
import OnboardingPager from "~/components/OnboardingPager"
import { baseClient } from "app/store"

import type { Route } from "./+types/index";

import styles from "app/app.module.scss";
import colors from "app/colors.module.scss";
import { useNavigate } from "react-router";
import { useState } from "react"; 
import { useGlobalStore } from "app/store";
import { redirect } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Delaba" },
    { name: "description", content: "The screen to use to log into Delaba." },
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
  const [initToken, setInitToken] = useState("")

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

  const initTokenChanged = (event: any) => {
    setInitToken(event.target.value) 
  }

  function logIn() {
    setErrorMsg("")
    baseClient.post("/auth/login", {
      login: login,
      password: password
    }).then((response) => {
      if (response.status == 200) {
        authorize()
        navigate("/home", {replace: true})
      }
    }).catch((error) => {
      const status = error.response.status
      if (status == 403) {
        setInitMode(true)
      } else if (status == 404) {
        setErrorMsg("Пользователь не найден")
      } else if (status == 401) {
        setErrorMsg("Неверный пароль")
      }
    })

  }

  function initUser() {
    setErrorMsg("")
    if (newPassword == newPasswordCheck) {
      baseClient.post("/auth/init", {
        login: login,
        new_password: newPassword,
        init_token: initToken
      }).then((response) => {
        if (response.status == 200) {
          authorize()
          navigate("/home", {replace: true})
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

  return (
      <GradientBackground color={colors.primary}>
        <div style={{height: "100%", width: "100%", display: "flex", flexWrap: "wrap", justifyContent: "space-around", alignItems: "center", gap: "50px"}}>
          <div style={{display: "flex", flexDirection: "column", justifyContent: "space-around", alignItems: "center"}}>
            <div style={{display: "flex", flexDirection: "row", gap: "20px"}}>
              {initMode ? <img style={{width: "60px", transform: "rotate(-90deg)"}} onClick={() => {
                setErrorMsg("")
                setInitMode(false)
              }} src="/back.svg" />:<></>}
              <h1 className={styles.h1} style={{color: colors.primary}}>Делаба ☺</h1>
            </div>
            <div style={{display: "flex", flexDirection: "column", gap: "20px"}}>
              <h2 style={{color: colors.secondary, textAlign: "center", fontSize: "2em"}}>{errorMsg}</h2>
              {initMode ?
              <>
                <input onChange={initTokenChanged} value={initToken} placeholder="Код создания" type="password" className={styles.textbox} />
                <input onChange={newPasswordChanged} value={newPassword} placeholder="Новый пароль" type="password" className={styles.textbox} />
                <input onChange={newPasswordCheckChanged} value={newPasswordCheck} placeholder="Повторите пароль" type="password" className={styles.textbox} />
              </>:
              <>
                <input onChange={loginChanged} value={login} placeholder="Логин" type="text" className={styles.textbox} />
                <input onChange={passwordChanged} value={password} placeholder="Пароль" type="password" className={styles.textbox} />
              </>
              }
            </div>

              <div 
                style={{position: "relative", width: "300px", height: "300px"}} title="Войти"
                onClick={() => {
                  setErrorMsg("")
                  if(initMode) {
                    initUser()
                  } else {
                    logIn()
                  }
                }}
              >
                <img className={styles['logo-main']} src="./logo.svg" />
                <img className={styles['logo-hover']} src="./logo_filled.svg" />
              </div>
          </div>

          <OnboardingPager />
        </div>
      </GradientBackground>
  );
}
