import { useState, useEffect } from "react";
import Search from "antd/es/input/Search";

export function DebouncedSearch(
  { onDebounce, loading }: {
    onDebounce: (query: string) => void,
    loading: boolean
  }) {
  const [query, setQuery] = useState("")

  useEffect(() => {
    const timer = setTimeout(() => {
      onDebounce(query)
    }, 200)

    return () => {
      clearTimeout(timer)
    }

  }, [query])

  return (
    <Search enterButton={false} loading={loading} placeholder="Поиск"
      onChange={(e) => {
        setQuery(e.target.value)
      }} />
  )
}
