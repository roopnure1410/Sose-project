import { useEffect, useRef } from 'react'

export default function useAudioVisualizer(audioRef) {
  const canvasRef = useRef(null)
  useEffect(() => {
    if (!audioRef.current) return
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)()
    const source = audioCtx.createMediaElementSource(audioRef.current)
    const analyser = audioCtx.createAnalyser()
    analyser.fftSize = 256
    source.connect(analyser)
    analyser.connect(audioCtx.destination)
    const bufferLength = analyser.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')

    function draw() {
      requestAnimationFrame(draw)
      analyser.getByteFrequencyData(dataArray)
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      const barWidth = (canvas.width / bufferLength) * 1.5
      let x = 0
      for (let i = 0; i < bufferLength; i++) {
        const barHeight = dataArray[i]
        ctx.fillStyle = `rgba(159,122,234,${0.2 + barHeight/512})`
        ctx.fillRect(x, canvas.height - barHeight/2, barWidth, barHeight/2)
        x += barWidth + 2
      }
    }
    draw()
    return () => audioCtx.close()
  }, [audioRef])
  return canvasRef
}