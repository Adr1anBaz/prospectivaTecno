import { motion } from 'framer-motion'

const scenarios = [
  {
    icon: '🗣️',
    title: 'Activación por Voz',
    desc: 'El usuario dice una palabra clave para activar el sistema. El robot responde con un saludo audible indicando que está listo para recibir instrucciones.',
  },
  {
    icon: '📍',
    title: 'Petición de Destino',
    desc: '"Llévame a la cafetería con el desayuno más barato" o "¿Dónde está el laboratorio de robótica?". El sistema interpreta la intención y consulta su base de datos.',
  },
  {
    icon: '🤔',
    title: 'Preguntas de Contexto',
    desc: '"¿A qué hora cierra la biblioteca?" o "¿Hay algún lugar cerca con buena señal de internet?". El LLM responde con información actualizada vía MCP.',
  },
  {
    icon: '🚶',
    title: 'Seguimiento Físico',
    desc: 'El robot confirma el destino, espera autorización del usuario, y comienza a desplazarse. Durante el trayecto, puede indicar puntos de referencia verbalmente.',
  },
]

export default function MetricasSlide() {
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
        Experiencia de Usuario
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
        Cómo imaginas la interacción con el sistema — del primer saludo al destino final
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {scenarios.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + i * 0.1 }}
            style={{
              padding: '20px 24px',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 12,
            }}
          >
            <div style={{ fontSize: 28, marginBottom: 8 }}>{s.icon}</div>
            <h4 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: 8, color: 'var(--blue)' }}>
              {s.title}
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.6 }}>
              {s.desc}
            </p>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        style={{
          marginTop: 24,
          padding: '14px 20px',
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 10,
          display: 'flex',
          gap: 20,
          justifyContent: 'center',
          flexWrap: 'wrap',
        }}
      >
        {['Sin entrenamiento ni app', 'Lenguaje natural', 'Confirmación antes de actuar', 'Respuesta visual + auditiva'].map((tag, i) => (
          <span key={i} style={{
            fontSize: '0.75rem',
            color: 'var(--text-dim)',
            padding: '4px 12px',
            background: 'var(--bg)',
            borderRadius: 20,
            border: '1px solid var(--border)',
          }}>
            {tag}
          </span>
        ))}
      </motion.div>
    </div>
  )
}
