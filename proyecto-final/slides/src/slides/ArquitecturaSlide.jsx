import { motion } from 'framer-motion'

export default function ArquitecturaSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1000 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 56,
        }}
      >
        Arquitectura
      </motion.h2>

      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr auto 1fr',
        alignItems: 'center',
        gap: 40,
      }}>
        {/* Robot */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          style={{
            padding: 40,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 16,
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: 40, marginBottom: 16 }}>Periférico</div>
          <h3 style={{ fontSize: '1.3rem', marginBottom: 8 }}>Robot</h3>
          <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem' }}>
            Unitree Go2 Air
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: 8 }}>
            Ejecución física, sensores, movimiento
          </p>
        </motion.div>

        {/* Connection */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 8,
          }}
        >
          <div style={{
            width: 80,
            height: 2,
            background: 'var(--blue)',
            opacity: 0.5,
          }} />
          <span style={{ fontSize: 12, color: 'var(--text-muted)', letterSpacing: '0.05em' }}>
            WebRTC
          </span>
        </motion.div>

        {/* Agent */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          style={{
            padding: 40,
            background: 'var(--surface)',
            border: '1px solid var(--blue)',
            borderRadius: 16,
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: 40, marginBottom: 16 }}>Cerebro</div>
          <h3 style={{ fontSize: '1.3rem', marginBottom: 8, color: 'var(--blue)' }}>Agente</h3>
          <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem' }}>
            "Blu"
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: 8 }}>
            Decisiones, NLP, navegación, contexto
          </p>
        </motion.div>
      </div>
    </div>
  )
}
