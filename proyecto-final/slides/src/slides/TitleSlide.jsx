import { motion } from 'framer-motion'

export default function TitleSlide() {
  return (
    <div style={{ textAlign: 'center', padding: '0 60px' }}>
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(5rem, 12vw, 9rem)',
          fontWeight: 400,
          color: 'var(--blue)',
          letterSpacing: '-0.02em',
          lineHeight: 1,
        }}
      >
        Blu
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        style={{
          marginTop: 32,
          fontSize: 'clamp(1.1rem, 2vw, 1.4rem)',
          color: 'var(--text-dim)',
          fontWeight: 300,
          maxWidth: 500,
          marginInline: 'auto',
          lineHeight: 1.6,
        }}
      >
        Agente de navegación inteligente
        <br />
        para el campus Ibero
      </motion.p>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7, duration: 0.6 }}
        style={{
          marginTop: 64,
          fontSize: 14,
          color: 'var(--text-muted)',
          letterSpacing: '0.1em',
          textTransform: 'uppercase',
        }}
      >
        Unitree Go2 Air + IA
      </motion.div>
    </div>
  )
}
