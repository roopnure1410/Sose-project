import { useEffect, useState } from 'react'

export default function ThemeToggle() {
  const [dark, setDark] = useState(true)
  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])
  return (
    <button
      aria-label="Toggle theme"
      onClick={() => setDark(!dark)}
      className="ml-3 px-3 py-2 rounded-2xl glass hover-glow-cyan text-sm"
    >
      {dark ? '🌙 Dark' : '☀️ Light'}
    </button>
  )
}