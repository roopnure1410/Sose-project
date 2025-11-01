import { motion } from 'framer-motion'

export default function Header() {
  return (
    <header className="pt-8">
      <motion.div initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} className="text-center">
        <div className="inline-flex items-center gap-3 px-5 py-4 rounded-2xl glass">
          <span className="text-2xl text-neonPurple">🎵</span>
          <div>
            <h1 className="text-2xl font-semibold">OpenMusic AI</h1>
            <p className="text-sm text-white/60">Create music from your imagination with AI</p>
          </div>
        </div>
      </motion.div>
      <div className="container mx-auto px-6 max-w-5xl">
        <div className="accent-underline" />
        <div className="flex justify-end mt-2">
          <a href="#" className="px-3 py-2 rounded-xl glass hover-glow text-white/80">Docs</a>
        </div>
      </div>
    </header>
  )
}