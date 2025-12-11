import GradientBackground from "~/components/GradientBackground";
import OnboardingPager from "~/components/OnboardingPager"
import type { Route } from "./+types/index";

import Switch from "~/components/Switch"
import styles from "app/app.module.scss";
import colors from "app/colors.module.scss";
import ListItem from "~/components/ListItem";
import { ItemIconType } from "~/components/ItemIcon"
import ListSeparator from "~/components/ListSeparator";
import { useGlobalStore } from "~/store";

import { redirect, useNavigate } from "react-router";
import { authClient } from "~/store";
import { useEffect, useState } from "react";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Delaba" },
    { name: "description", content: "Application settings." },
  ];
}

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  if (!useGlobalStore.getState().authorized) {
    return redirect("/")
  }
}

export default function Index() {
  const navigate = useNavigate()
  const { unauthorize, moderator } = useGlobalStore()
  const [usingSection, setUsingSection] = useState("Основные")

  const [enableEdit, setEnableEdit] = useState(false)

  useEffect(() => {
    const enableEditSet = localStorage.getItem("enable_edit")
    if (enableEditSet != null && enableEditSet == "true") {
      setEnableEdit(true)
    }
  }, [])

  useEffect(() => {
    localStorage.setItem("enable_edit", ""+enableEdit)
  }, [enableEdit])

  return (
    <GradientBackground color={colors.primary}>
      <div style={{position: "absolute", width: "100%", height: "100%", display: "flex", alignItems: "center", justifyContent: "center"}}>
        <div style={{border: `5px solid ${colors.primary}`, borderRadius: "30px", width: "90%", height: "90%"}}>    
            <div style={{
                width: "100%",
                height: "100%",
                borderRadius: "25px",
                padding: "20px 0px 0px 320px",
            }}>
              <div style={{display: "flex", flexDirection: "column", justifyContent: "space-between", height: "100%", padding: "20px 30px 20px 0px"}}>
                <div style={{display: "flex", flexDirection: "column", gap: "15px"}}>
                  <p onClick={() => {
                    localStorage.clear()
                    authClient.put("/users/data/", {})
                  }} className={styles['settings-button']}>Удалить данные использования</p>
                  {moderator ? 
                  <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
                    <p style={{color: colors.primary, fontSize: "30px", fontWeight: "bold"}}>Включить редактирование</p>
                    <Switch checked={enableEdit} onChange={(value) => {setEnableEdit(value)}} />
                  </div>
                  : <></>}
                </div>

                <h1 style={{lineHeight: "60px", textAlign: "end"}}>{usingSection}</h1>
              </div>
                
            </div>
        </div></div>

        <div style={{
            width: "300px",
            position: "absolute",
            bottom: "30px",
            left: "30px",
            height: "87%",
            padding: "20px",
            background: colors.primary,
            borderRadius: "25px"}}>

            <div style={{display: "flex", flexDirection: "column", height: "100%", justifyContent: "space-between"}}>
              <div style={{display: "flex", height: "100%", justifyContent: "start", gap: "15px", flexDirection: "column"}}>
                  <ListItem title="Основные" highlight={false} icon={ItemIconType.None} />
                  <ListSeparator />
                  <div onClick={() => {
                    authClient.post("/auth/logout")
                    unauthorize()
                    navigate("/")
                  }}>
                    <ListItem title="Выйти" highlight={true} icon={ItemIconType.None} />
                  </div>
              </div>

              <img src="exit.svg" onClick={() => {navigate(-1)}} style={{width: "30px", margin: "7px"}} />
            </div>
        </div>
    </GradientBackground>
  );
}
