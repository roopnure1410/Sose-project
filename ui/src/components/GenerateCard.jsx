import { useState } from 'react'
import { motion } from 'framer-motion'
import { generateMusic } from '../api/gradio'

const STYLES = ['Balanced','Classical','Jazz','Electronic','Ambient','Rock','Folk','World']

export default function GenerateCard({ onGenerated, prefill }) {
  const [description, setDescription] = useState('Cinematic ambient pads with gentle piano and evolving textures')
  const [duration, setDuration] = useState(8)
  const [style, setStyle] = useState('Ambient')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('Ready')

  // Apply prefill from ExamplePrompts when provided
  // Expected shape: { t, d, s }
  // Keep existing local control intact
  if (prefill && typeof prefill === 'object') {
    const { t, d, s } = prefill
    if (t && description !== t) setDescription(t)
    if (d && duration !== d) setDuration(d)
    if (s && style !== s) setStyle(s)
  }

  const handleGenerate = async () => {
    setLoading(true)
    setStatus('Generating...')
    try {
      const res = await generateMusic({ description, duration, style })
      onGenerated({ url: res.url, title: description, style, duration })
      setStatus('Done')
    } catch (e) {
      console.error(e)
      setStatus('Failed: ' + e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-3xl p-6 shadow-card">
      <div className="grid gap-4">
        <label className="text-sm text-white/70">Music Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Describe the music you want..."
          className="w-full min-h-[120px] rounded-2xl bg-black/30 border border-white/10 px-4 py-3 outline-none focus:border-neonPurple focus:ring-2 focus:ring-neonPurple/40 transition"
        />

        <div className="grid md:grid-cols-3 gap-4 items-center">
          <div className="md:col-span-2">
            <label className="text-sm text-white/70">Duration: <span className="text-white font-medium">{duration}s</span></label>
            <input type="range" min="3" max="15" step="1" value={duration}
              onChange={(e)=>setDuration(parseInt(e.target.value))}
              className="w-full accent-neonPurple" />
          </div>
          <div>
            <label className="text-sm text-white/70">Style</label>
            <select value={style} onChange={(e)=>setStyle(e.target.value)}
              className="w-full rounded-2xl bg-black/30 border border-white/10 px-3 py-2 outline-none focus:border-neonCyan">
              {STYLES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
            <div className="flex flex-wrap gap-2 mt-2">
              {STYLES.map(s => (
                <button key={s} type="button"
                  onClick={()=>setStyle(s)}
                  className={`px-3 py-1.5 rounded-xl text-sm border ${style===s?'border-neonPurple bg-black/40':'border-white/10 bg-black/20'} hover:border-neonCyan transition`}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-2 text-center">
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="px-7 py-3 rounded-2xl text-black font-semibold bg-gradient-to-r from-neonPurple to-neonCyan hover:opacity-90 hover-glow transition disabled:opacity-50"
          >
            🎶 Generate Music
          </button>
          <div className="text-sm text-white/60 mt-2">
            {loading ? <span className="animate-pulse">♪ Generating...</span> : status}
          </div>
        </div>
      </div>
    </motion.div>
  )
}