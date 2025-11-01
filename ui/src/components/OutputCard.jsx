import { useRef, useState } from 'react'
import { motion } from 'framer-motion'
import useAudioVisualizer from '../hooks/useAudioVisualizer'

export default function OutputCard({ track, onRegenerate }) {
  const audioRef = useRef(null)
  const canvasRef = useAudioVisualizer(audioRef)
  const [downloading, setDownloading] = useState(false)
  if (!track) return null

  const handleDownload = async () => {
    setDownloading(true)
    try {
      const a = document.createElement('a')
      a.href = track.url
      a.download = (track.title || 'openmusic') + '.wav'
      a.click()
    } finally {
      setDownloading(false)
    }
  }

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-3xl p-6 shadow-card">
      <div className="flex flex-col md:flex-row gap-4 items-center">
        <div className="flex-1">
          <h3 className="text-lg font-semibold">{track.title}</h3>
          <p className="text-white/60 text-sm">{track.style} • {track.duration}s</p>
          <audio ref={audioRef} src={track.url} controls className="w-full mt-3" />
          <canvas ref={canvasRef} width={600} height={80} className="w-full mt-3 rounded-xl bg-black/30" />
        </div>
        <div className="flex md:flex-col gap-3">
          <button onClick={()=>audioRef.current?.play()} className="px-4 py-2 rounded-2xl glass hover-glow">▶ Play</button>
          <button onClick={()=>audioRef.current?.pause()} className="px-4 py-2 rounded-2xl glass hover-glow">⏸ Pause</button>
          <button onClick={handleDownload} disabled={downloading} className="px-4 py-2 rounded-2xl glass hover-glow-cyan disabled:opacity-50">⬇ Download</button>
          {onRegenerate && (
            <button onClick={()=>onRegenerate(track)} className="px-4 py-2 rounded-2xl glass hover-glow">🔁 Regenerate</button>
          )}
        </div>
      </div>
    </motion.div>
  )
}