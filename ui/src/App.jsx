import { useState } from 'react'
import { motion } from 'framer-motion'
import Header from './components/Header'
import ThemeToggle from './components/ThemeToggle'
import GenerateCard from './components/GenerateCard'
import OutputCard from './components/OutputCard'
import ExamplePrompts from './components/ExamplePrompts'
import Footer from './components/Footer'

export default function App() {
  const [track, setTrack] = useState(null)
  const [prefill, setPrefill] = useState(null)
  const handlePick = (e) => {
    setPrefill(e)
  }
  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'radial-gradient(1200px 600px at 20% 0%, rgba(159,122,234,0.15), transparent), radial-gradient(1200px 600px at 80% 0%, rgba(6,182,212,0.15), transparent)' }}>
      <Header />
      <main className="flex-1 container mx-auto px-6 py-8 max-w-5xl">
        <motion.section initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.4 }}>
          <div className="flex items-center justify-between mb-5">
            <div>
              <h2 className="text-2xl font-semibold">Studio</h2>
              <p className="text-white/60 text-sm">Describe your music, set duration, pick a style, and generate.</p>
            </div>
            <ThemeToggle />
          </div>
          <GenerateCard onGenerated={setTrack} prefill={prefill} />
        </motion.section>

        <motion.section className="mt-6" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
          <OutputCard track={track} />
        </motion.section>

        <motion.section className="mt-8" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
          <ExamplePrompts onPick={handlePick} />
        </motion.section>
      </main>
      <div className="container mx-auto px-6 max-w-5xl w-full">
        <Footer />
      </div>
    </div>
  )
}