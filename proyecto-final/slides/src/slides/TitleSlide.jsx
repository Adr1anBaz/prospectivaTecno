import { motion } from 'framer-motion'

export default function TitleSlide() {
  return (
    <div style={{ textAlign: 'center', padding: '0 80px', maxWidth: 1000 }}>
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        style={{
          fontSize: 'clamp(0.65rem, 0.9vw, 0.8rem)',
          color: 'var(--blue)',
          letterSpacing: '0.2em',
          textTransform: 'uppercase',
          marginBottom: 32,
          fontWeight: 500,
        }}
      >
        Proyecto de Investigación
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(3rem, 7vw, 5.5rem)',
          fontWeight: 400,
          color: 'var(--blue)',
          letterSpacing: '-0.02em',
          lineHeight: 1.1,
        }}
      >
          Guía Autónoma
        <br />
        <span style={{ color: 'var(--text)', fontSize: '0.7em' }}>
          con Agentes Conversacionales
        </span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        style={{
          marginTop: 28,
          fontSize: 'clamp(0.95rem, 1.5vw, 1.15rem)',
          color: 'var(--text-dim)',
          fontWeight: 300,
          maxWidth: 600,
          marginInline: 'auto',
          lineHeight: 1.6,
        }}
      >
        Navegación inteligente en campus universitarios mediante
        interacción por voz, modelos de lenguaje y robótica móvil
      </motion.p>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6, duration: 0.6 }}
        style={{
          marginTop: 56,
          fontSize: 'clamp(0.7rem, 0.9vw, 0.8rem)',
          color: 'var(--text-muted)',
          lineHeight: 1.8,
        }}
      >
        <div>Adrián Bazaldua · Sebastián Enguilo · Fernando Pérez</div>
        <div style={{ color: 'var(--text-dim)' }}>
          Universidad Iberoamericana — Departamento de Ingeniería
        </div>
      </motion.div>
    </div>
  )
}
