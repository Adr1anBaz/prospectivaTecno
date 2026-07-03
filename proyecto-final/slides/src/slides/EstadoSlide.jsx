import { motion } from 'framer-motion'

const done = [
  'Control del robot vía Python/WebRTC',
  'Pipeline de voz: Whisper → LLM → TTS',
]

const working = [
  'Base de datos vectorizada con MCP',
  'Estructura de grafo para navegación',
  'Rutas pregrabadas por tramos modulares',
]

const pending = [
  'Resolver conectividad WiFi',
  'Raspberry Pi 5 como dispositivo portable',
  'Navegación autónoma con ROS2/SLAM',
]

export default function EstadoSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1100 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 48,
        }}
      >
        Estado Actual
      </motion.h2>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 40 }}>
        {/* Done */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h4 style={{
            fontSize: '0.75rem',
            textTransform: 'uppercase',
            letterSpacing: '0.1em',
            color: 'var(--blue)',
            marginBottom: 20,
            fontWeight: 600,
          }}>
            Logrado
          </h4>
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 14 }}>
            {done.map((item, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + i * 0.08 }}
                style={{
                  color: 'var(--text-dim)',
                  fontSize: '0.95rem',
                  paddingLeft: 16,
                  borderLeft: '2px solid var(--blue)',
                  lineHeight: 1.5,
                }}
              >
                {item}
              </motion.li>
            ))}
          </ul>
        </motion.div>

        {/* Working */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <h4 style={{
            fontSize: '0.75rem',
            textTransform: 'uppercase',
            letterSpacing: '0.1em',
            color: '#E6A85B',
            marginBottom: 20,
            fontWeight: 600,
          }}>
            En progreso
          </h4>
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 14 }}>
            {working.map((item, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.08 }}
                style={{
                  color: 'var(--text-dim)',
                  fontSize: '0.95rem',
                  paddingLeft: 16,
                  borderLeft: '2px solid #E6A85B',
                  lineHeight: 1.5,
                }}
              >
                {item}
              </motion.li>
            ))}
          </ul>
        </motion.div>

        {/* Pending */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h4 style={{
            fontSize: '0.75rem',
            textTransform: 'uppercase',
            letterSpacing: '0.1em',
            color: 'var(--text-muted)',
            marginBottom: 20,
            fontWeight: 600,
          }}>
            Pendiente
          </h4>
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 14 }}>
            {pending.map((item, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + i * 0.08 }}
                style={{
                  color: 'var(--text-muted)',
                  fontSize: '0.95rem',
                  paddingLeft: 16,
                  borderLeft: '2px solid var(--border)',
                  lineHeight: 1.5,
                }}
              >
                {item}
              </motion.li>
            ))}
          </ul>
        </motion.div>
      </div>
    </div>
  )
}
