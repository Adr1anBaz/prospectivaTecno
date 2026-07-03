import { motion } from 'framer-motion'

const layers = [
  {
    title: 'Procesamiento de Lenguaje',
    items: ['AudioProcess (captura, VAD, wake word)', 'Orquestador (clasificador + LLM)', 'AudioPlayback (TTS streaming)'],
    color: 'var(--blue)',
  },
  {
    title: 'Orquestación Robótica',
    items: ['Event Bus (multiprocessing.Queue)', 'MCP Client (consultas a BD campus)', 'Generación de instrucciones JSON'],
    color: '#E6A85B',
  },
  {
    title: 'Comunicación Física',
    items: ['ROS2 Humble (controller + actions + nav)', 'WebRTC DataChannel', 'Ejecución en Unitree Go2 Air'],
    color: '#6BCB8A',
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
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 12,
        }}
      >
        Arquitectura
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '0.9rem',
          marginBottom: 36,
          fontWeight: 300,
        }}
      >
        Procesos desacoplados comunicados por Event Bus — 3 capas jerárquicas
      </motion.p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 0, position: 'relative' }}>
        {layers.map((layer, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 + i * 0.15 }}
            style={{
              display: 'grid',
              gridTemplateColumns: '180px 1fr',
              gap: 20,
              padding: '18px 24px',
              background: 'var(--surface)',
              border: `1px solid ${layer.color}33`,
              borderLeft: `3px solid ${layer.color}`,
              borderRadius: i === 0 ? '12px 12px 0 0' : i === layers.length - 1 ? '0 0 12px 12px' : 0,
              marginTop: i > 0 ? -1 : 0,
            }}
          >
            <div>
              <div style={{
                fontSize: '0.65rem',
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
                color: layer.color,
                fontWeight: 600,
                marginBottom: 4,
              }}>
                Capa {i + 1}
              </div>
              <div style={{ fontSize: '0.85rem', fontWeight: 500, color: 'var(--text)' }}>
                {layer.title}
              </div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {layer.items.map((item, j) => (
                <div key={j} style={{
                  fontSize: '0.82rem',
                  color: 'var(--text-dim)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                }}>
                  <span style={{ color: layer.color, fontSize: '0.5rem' }}>◆</span>
                  {item}
                </div>
              ))}
            </div>
          </motion.div>
        ))}

        {/* Event Bus badge */}
        <motion.div
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8, type: 'spring' }}
          style={{
            position: 'absolute',
            right: -20,
            top: '50%',
            transform: 'translateY(-50%)',
            background: 'var(--bg)',
            border: '1px solid var(--blue)',
            borderRadius: 20,
            padding: '8px 16px',
            fontSize: '0.7rem',
            color: 'var(--blue)',
            fontWeight: 600,
            letterSpacing: '0.05em',
          }}
        >
          EVENT BUS
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.9 }}
        style={{
          marginTop: 20,
          display: 'flex',
          gap: 16,
          justifyContent: 'center',
        }}
      >
        {[
          { label: 'STT remoto (Groq Whisper)', color: 'var(--blue)' },
          { label: 'LLM remoto (Groq Llama 4)', color: 'var(--blue)' },
          { label: 'TTS remoto (Edge / Deepgram)', color: 'var(--blue)' },
        ].map((s, i) => (
          <div key={i} style={{
            fontSize: '0.65rem',
            color: 'var(--text-muted)',
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 6,
            padding: '4px 10px',
            letterSpacing: '0.03em',
          }}>
            {s.label}
          </div>
        ))}
      </motion.div>
    </div>
  )
}
