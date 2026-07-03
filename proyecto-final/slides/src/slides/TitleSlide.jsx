import { motion } from 'framer-motion'

export default function TitleSlide() {
  return (
    <div style={{ textAlign: 'center', padding: '0 80px', maxWidth: 1000 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        style={{
          fontSize: 'clamp(0.7rem, 1vw, 0.85rem)',
          color: 'var(--blue)',
          letterSpacing: '0.15em',
          textTransform: 'uppercase',
          marginBottom: 24,
          fontWeight: 500,
        }}
      >
        IEEE Conference Paper
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.8rem, 6vw, 4.5rem)',
          fontWeight: 400,
          color: 'var(--blue)',
          letterSpacing: '-0.02em',
          lineHeight: 1.15,
        }}
      >
        Walking the Talk
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        style={{
          marginTop: 16,
          fontSize: 'clamp(1rem, 1.8vw, 1.3rem)',
          color: 'var(--text-dim)',
          fontWeight: 300,
          maxWidth: 700,
          marginInline: 'auto',
          lineHeight: 1.5,
        }}
      >
        Robot-Guided Navigation Through Conversational AI on University Campuses
      </motion.p>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6, duration: 0.6 }}
        style={{
          marginTop: 48,
          fontSize: 'clamp(0.75rem, 1vw, 0.85rem)',
          color: 'var(--text-muted)',
          lineHeight: 1.7,
        }}
      >
        <div>Adrián Bazaldua, Sebastián Enguilo, Fernando Pérez</div>
        <div>Joel Arango, Huber Girón</div>
        <div style={{ marginTop: 8, color: 'var(--text-dim)' }}>
          Universidad Iberoamericana — Depto. de Ingeniería
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.9, duration: 0.6 }}
        style={{
          marginTop: 48,
          fontSize: 13,
          color: 'var(--text-muted)',
          letterSpacing: '0.1em',
          textTransform: 'uppercase',
        }}
      >
        Unitree Go2 + Groq LLM + ROS2
      </motion.div>
    </div>
  )
}
