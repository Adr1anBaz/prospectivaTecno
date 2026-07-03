import { motion } from 'framer-motion'

const goals = [
  { icon: '🎙️', label: 'Comprensión de voz', desc: 'Transcripción mediante Whisper (Groq) y detección de activación con Vosk offline' },
  { icon: '🧠', label: 'Clasificación híbrida', desc: 'Intenciones de navegación por regex (YAML) + razonamiento semántico con LLM (Llama 4 Scout)' },
  { icon: '🗺️', label: 'Consulta estructurada', desc: 'Datos del campus vía MCP — lugares, servicios, horarios, inventario' },
  { icon: '🤖', label: 'Control robótico', desc: 'Órdenes al Unitree Go2 mediante ROS2 Humble + WebRTC con archivos JSON compartidos' },
]

export default function ObjetivoSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1100 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 12,
        }}
      >
        Objetivo
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '1rem',
          marginBottom: 40,
          fontWeight: 300,
          maxWidth: 700,
          lineHeight: 1.6,
        }}
      >
        Traducir instrucciones en lenguaje natural a comandos de navegación física
        sobre un robot cuadrúpedo, integrando procesamiento de voz, razonamiento
        con LLM y control motor en una arquitectura de procesos desacoplados.
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {goals.map((g, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 + i * 0.1 }}
            style={{
              padding: '20px 24px',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 12,
            }}
          >
            <div style={{ fontSize: 24, marginBottom: 8 }}>{g.icon}</div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 6, color: 'var(--blue)' }}>{g.label}</h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>{g.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
