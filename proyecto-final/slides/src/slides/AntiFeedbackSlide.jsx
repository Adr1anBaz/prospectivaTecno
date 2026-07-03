import { motion } from 'framer-motion'

const blocks = [
  {
    title: 'Silenciamiento Activo',
    desc: 'Ignorar tramos de micrófono durante reproducción TTS',
    icon: '🔇',
    detail: 'El AudioProcess descarta frames mientras el PlaybackProcess está activo',
  },
  {
    title: 'Flush de Buffer',
    desc: 'Eliminar señal residual acústica antes de reproducir',
    icon: '🔄',
    detail: 'Limpia el buffer circular de 0.5 s inmediatamente antes del TTS',
  },
  {
    title: 'Cooldown Temporal',
    desc: 'Tiempo muerto post-TTS para disipación de eco',
    icon: '⏳',
    detail: '3.0 s por defecto antes de reanudar captura — configurable',
  },
]

export default function AntiFeedbackSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1000 }}>
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
        Supresión de Retroalimentación
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
          maxWidth: 600,
        }}
      >
        El sistema no debe procesar su propia voz como una instrucción de usuario.
        Tres mecanismos software en la capa de captura de audio.
      </motion.p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {blocks.map((b, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 + i * 0.12 }}
            style={{
              display: 'grid',
              gridTemplateColumns: '48px 1fr',
              gap: 20,
              padding: '20px 24px',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 12,
              alignItems: 'center',
            }}
          >
            <div style={{
              width: 48,
              height: 48,
              borderRadius: '50%',
              background: 'var(--bg)',
              border: '1px solid var(--border)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 20,
            }}>
              {b.icon}
            </div>
            <div>
              <div style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--blue)', marginBottom: 4 }}>
                {b.title}
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-dim)', marginBottom: 4 }}>
                {b.desc}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                {b.detail}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
