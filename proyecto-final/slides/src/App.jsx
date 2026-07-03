import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import TitleSlide from './slides/TitleSlide'
import ObjetivoSlide from './slides/ObjetivoSlide'
import ArquitecturaSlide from './slides/ArquitecturaSlide'
import PipelineSlide from './slides/PipelineSlide'
import AgenteSlide from './slides/AgenteSlide'
import RobotSlide from './slides/RobotSlide'
import AntiFeedbackSlide from './slides/AntiFeedbackSlide'
import MetricasSlide from './slides/MetricasSlide'
import PerformanceSlide from './slides/PerformanceSlide'
import NavegacionSlide from './slides/NavegacionSlide'
import DesafiosSlide from './slides/DesafiosSlide'
import ConclusionesSlide from './slides/ConclusionesSlide'

const slides = [
  TitleSlide,
  ObjetivoSlide,
  ArquitecturaSlide,
  PipelineSlide,
  AgenteSlide,
  RobotSlide,
  AntiFeedbackSlide,
  MetricasSlide,
  PerformanceSlide,
  NavegacionSlide,
  DesafiosSlide,
  ConclusionesSlide,
]

export default function App() {
  const [current, setCurrent] = useState(0)
  const [dir, setDir] = useState(1)

  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault()
        go(1)
      }
      if (e.key === 'ArrowLeft') go(-1)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  })

  const go = (d) => {
    const next = current + d
    if (next < 0 || next >= slides.length) return
    setDir(d)
    setCurrent(next)
  }

  const Slide = slides[current]

  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
      <AnimatePresence mode="wait" custom={dir}>
        <motion.div
          key={current}
          custom={dir}
          initial={{ opacity: 0, x: dir * 60 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: dir * -60 }}
          transition={{ duration: 0.35, ease: [0.4, 0, 0.2, 1] }}
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Slide />
        </motion.div>
      </AnimatePresence>

      {/* Dots */}
      <div style={{
        position: 'fixed',
        bottom: 32,
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: 8,
        zIndex: 100,
      }}>
        {slides.map((_, i) => (
          <button
            key={i}
            onClick={() => { setDir(i > current ? 1 : -1); setCurrent(i) }}
            style={{
              width: i === current ? 24 : 8,
              height: 8,
              borderRadius: 4,
              border: 'none',
              background: i === current ? 'var(--blue)' : 'var(--text-muted)',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
            }}
          />
        ))}
      </div>

      {/* Counter */}
      <div style={{
        position: 'fixed',
        bottom: 32,
        right: 40,
        fontSize: 13,
        color: 'var(--text-muted)',
        fontWeight: 500,
        letterSpacing: '0.05em',
      }}>
        {current + 1}/{slides.length}
      </div>
    </div>
  )
}
