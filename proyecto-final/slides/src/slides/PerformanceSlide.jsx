import { motion } from 'framer-motion'

const phases = [
  {
    title: 'Fase 1 — Fundación',
    items: [
      'Pipeline de voz funcional (STT → LLM → TTS)',
      'Clasificador híbrido operativo',
      'Integración con datos del campus vía MCP',
    ],
    color: 'var(--blue)',
    status: 'base',
  },
  {
    title: 'Fase 2 — Control Robótico',
    items: [
      'Comunicación WebRTC con robot',
      'Comandos básicos de presencia (sentarse, pararse, saludar)',
      'Arquitectura ROS2 implementada',
    ],
    color: '#E6A85B',
    status: 'next',
  },
  {
    title: 'Fase 3 — Navegación',
    items: [
      'Modelado del grafo del campus',
      'Algoritmo de ruteo (Dijkstra)',
      'Ejecución de rutas pregrabadas',
    ],
    color: '#6BCB8A',
    status: 'future',
  },
  {
    title: 'Fase 4 — Autonomía',
    items: [
      'Navegación autónoma con SLAM',
      'Detección de obstáculos en tiempo real',
      'Modelos locales para operación sin internet',
    ],
    color: 'var(--text-muted)',
    status: 'future',
  },
]

export default function PerformanceSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1000 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.2rem)',
          fontWeight: 400,
          marginBottom: 8,
        }}
      >
        Hoja de Ruta
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '0.9rem',
          marginBottom: 40,
          fontWeight: 300,
        }}
      >
        Del prototipo funcional a la autonomía completa
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {phases.map((p, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + i * 0.1 }}
            style={{
              padding: 24,
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 12,
              borderTop: `3px solid ${p.color}`,
              opacity: p.status === 'future' ? 0.6 : 1,
            }}
          >
            <div style={{
              fontSize: '0.65rem',
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              color: p.color,
              fontWeight: 600,
              marginBottom: 12,
            }}>
              {p.title}
            </div>
            <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 8 }}>
              {p.items.map((item, j) => (
                <li key={j} style={{
                  fontSize: '0.82rem',
                  color: 'var(--text-dim)',
                  paddingLeft: 12,
                  borderLeft: `2px solid ${p.color}`,
                  lineHeight: 1.4,
                }}>
                  {item}
                </li>
              ))}
            </ul>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
