import { motion } from 'framer-motion'

const EXAMPLES = [
  { t: 'Epic orchestral battle theme with choir and taiko', d: 8, s: 'Classical' },
  { t: 'Lo-fi chillhop with dusty vinyl crackle and jazz chords', d: 7, s: 'Jazz' },
  { t: 'Driving synthwave pulse with retro arps and gated reverb', d: 6, s: 'Electronic' },
  { t: 'Atmospheric ambient pads with distant piano echoes', d: 8, s: 'Ambient' },
  { t: 'World fusion with handpan, tabla, and subtle strings', d: 7, s: 'World' },
  { t: 'Experimental glitch textures with granular drones', d: 6, s: 'Experimental' },
]

export default function ExamplePrompts({ onPick }) {
  return (
    <motion.section initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <h2 className="text-xl font-semibold mb-3">💡 Try these examples</h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {EXAMPLES.map((e, i) => (
          <motion.button
            key={i}
            onClick={() => onPick(e)}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="text-left glass rounded-2xl p-4 hover-glow transition"
          >
            <div className="flex items-center justify-between">
              <div className="font-medium line-clamp-2 pr-3">{e.t}</div>
              <span className="text-xs px-2 py-1 rounded-full bg-neonPurple/20 text-neonPurple whitespace-nowrap">{e.s}</span>
            </div>
            <div className="text-sm text-white/60 mt-2">Duration: {e.d}s</div>
          </motion.button>
        ))}
      </div>
    </motion.section>
  )
}