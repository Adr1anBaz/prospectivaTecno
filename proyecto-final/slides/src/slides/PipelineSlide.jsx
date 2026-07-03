import { motion } from 'framer-motion'

const stages = [
  { label: 'Captura', desc: 'Micrófono 16 kHz', icon: '🎤' },
  { label: 'Wake Word', desc: 'Activación por voz local', icon: '🔊' },
  { label: 'VAD', desc: 'Segmentación de voz', icon: '📡' },
  { label: 'STT', desc: 'Transcripción a texto', icon: '📝' },
  { label: 'LLM', desc: 'Razonamiento semántico', icon: '🧠' },
  { label: 'TTS', desc: 'Síntesis de respuesta', icon: '🔈' },
]

export default function PipelineSlide() {
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
        Pipeline de Interacción por Voz
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '0.9rem',
          marginBottom: 48,
          fontWeight: 300,
        }}
      >
        El usuario habla — el sistema procesa, entiende y responde
      </motion.p>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0, marginBottom: 48, flexWrap: 'wrap' }}>
        {stages.map((s, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center' }}>
            <motion.div
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 + i * 0.1, type: 'spring' }}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: 8,
                minWidth: 80,
              }}
            >
              <div style={{
                width: 52,
                height: 52,
                borderRadius: '50%',
                background: 'var(--surface)',
                border: '2px solid var(--blue)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 18,
              }}>
                {s.icon}
              </div>
              <div style={{ fontSize: '0.65rem', fontWeight: 600, color: 'var(--text)', textAlign: 'center' }}>
                {s.label}
              </div>
              <div style={{ fontSize: '0.6rem', color: 'var(--text-muted)', textAlign: 'center', maxWidth: 70 }}>
                {s.desc}
              </div>
            </motion.div>
            {i < stages.length - 1 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 + i * 0.1 }}
                style={{
                  width: 24,
                  height: 2,
                  background: 'var(--blue)',
                  opacity: 0.3,
                  margin: '0 4px',
                  position: 'relative',
                  top: -14,
                }}
              />
            )}
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16 }}>
        {[
          {
            title: 'Procesamiento de Audio',
            items: ['Detección de activación por palabra clave (offline)', 'Segmentación por actividad vocal (VAD)', 'Buffer circular para preservar inicio del comando'],
          },
          {
            title: 'Reconocimiento y Síntesis',
            items: ['STT: conversión voz → texto vía API externa', 'TTS: conversión texto → voz vía API externa', 'Arquitectura agnóstica al proveedor'],
          },
          {
            title: 'Supresión de Retroalimentación',
            items: ['Silenciar micrófono durante reproducción TTS', 'Limpiar buffer antes de cada reproducción', 'Tiempo de espera post-respuesta para disipación de eco'],
          },
        ].map((col, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 + i * 0.1 }}
            style={{
              padding: 20,
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 10,
            }}
          >
            <h4 style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--blue)', marginBottom: 12, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              {col.title}
            </h4>
            <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 8 }}>
              {col.items.map((item, j) => (
                <li key={j} style={{ fontSize: '0.78rem', color: 'var(--text-dim)', lineHeight: 1.5, paddingLeft: 10, borderLeft: '1px solid var(--border)' }}>
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
