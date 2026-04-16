import { useState, useEffect } from "react";
import Search from "antd/es/input/Search";

export function DebouncedSearch(
  { onDebounce, loading, initial }: {
    onDebounce: (query: string) => void,
    loading: boolean,
    initial: string
  }) {
  const [query, setQuery] = useState(initial)

  useEffect(() => {
    const timer = setTimeout(() => {
      onDebounce(query)
    }, 200)

    return () => {
      clearTimeout(timer)
    }

  }, [query])

  return (
    <Search enterButton={false} value={query} loading={loading} placeholder="Поиск"
      onChange={(e) => {
        setQuery(e.target.value)
      }} />
  )
}
