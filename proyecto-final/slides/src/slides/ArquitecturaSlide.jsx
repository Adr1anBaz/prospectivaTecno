import { motion } from 'framer-motion'

const pillars = [
  {
    title: 'Interacción por Voz',
    items: ['Captura de audio y detección de activación', 'Reconocimiento de voz (STT)', 'Síntesis de voz (TTS)'],
    icon: '🎤',
  },
  {
    title: 'Razonamiento con IA',
    items: ['Clasificador híbrido (reglas + LLM)', 'Modelo de Lenguaje (LLM) conversacional', 'Conexión a datos estructurados vía MCP'],
    icon: '🧠',
  },
  {
    title: 'Robótica Móvil',
    items: ['Robot cuadrúpedo como plataforma de guía', 'Control por ROS2 + WebRTC', 'Ejecución de rutas de navegación'],
    icon: '🤖',
  },
  {
    title: 'Arquitectura Desacoplada',
    items: ['Procesos independientes comunicados por bus', 'Separación de capas (lenguaje, orquestación, control)', 'Componentes intercambiables'],
    icon: '🔗',
  },
]

export default function ArquitecturaSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1100 }}>
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
        Visión del Sistema
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
          maxWidth: 650,
          lineHeight: 1.6,
        }}
      >
        Un sistema capaz de guiar personas dentro de un campus universitario
        mediante conversación natural, combinando cuatro pilares tecnológicos.
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {pillars.map((p, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + i * 0.12 }}
            style={{
              padding: 24,
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 12,
            }}
          >
            <div style={{ fontSize: 28, marginBottom: 12 }}>{p.icon}</div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 12, color: 'var(--blue)' }}>
              {p.title}
            </h4>
            <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 6 }}>
              {p.items.map((item, j) => (
                <li key={j} style={{
                  fontSize: '0.8rem',
                  color: 'var(--text-dim)',
                  paddingLeft: 12,
                  borderLeft: '1px solid var(--border)',
                  lineHeight: 1.5,
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
