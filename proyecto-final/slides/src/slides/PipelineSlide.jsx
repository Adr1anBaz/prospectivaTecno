import { motion } from 'framer-motion'

const stages = [
  { label: 'Captura', freq: '16 kHz / 32 ms', icon: '🎤' },
  { label: 'Wake Word', freq: 'Vosk 42 MB offline', icon: '🔊' },
  { label: 'VAD', freq: 'Silero · umbral 0.4', icon: '📡' },
  { label: 'STT', freq: 'Groq Whisper', icon: '📝' },
  { label: 'Clasif.', freq: 'YAML + LLM', icon: '🧠' },
  { label: 'TTS', freq: 'Edge / Deepgram', icon: '🔈' },
]

export default function PipelineSlide() {
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
        Pipeline de Voz
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
        Procesamiento secuencial de 5 etapas — latencia total estimada ~1.6 s
      </motion.p>

      {/* Pipeline flow - horizontal circles with arrows */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0, marginBottom: 48 }}>
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
                minWidth: 90,
              }}
            >
              <div style={{
                width: 56,
                height: 56,
                borderRadius: '50%',
                background: 'var(--surface)',
                border: '2px solid var(--blue)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 20,
              }}>
                {s.icon}
              </div>
              <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text)' }}>
                {s.label}
              </div>
              <div style={{ fontSize: '0.6rem', color: 'var(--text-muted)', textAlign: 'center', maxWidth: 80 }}>
                {s.freq}
              </div>
            </motion.div>
            {i < stages.length - 1 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 + i * 0.1 }}
                style={{
                  width: 32,
                  height: 2,
                  background: 'var(--blue)',
                  opacity: 0.3,
                  margin: '0 4px',
                  position: 'relative',
                  top: -16,
                }}
              />
            )}
          </div>
        ))}
      </div>

      {/* Detail boxes */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          style={{
            padding: 20,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}
        >
          <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--blue)', marginBottom: 12, fontWeight: 600 }}>
            Captura y Activación
          </h4>
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 8 }}>
            <li style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              Buffer circular de 0.5 s para preservar inicio del comando
            </li>
            <li style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              Silencio continuo de 1.0 s → fin de instrucción
            </li>
            <li style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              Wake word offline con latencia &lt; 200 ms
            </li>
          </ul>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          style={{
            padding: 20,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}
        >
          <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--blue)', marginBottom: 12, fontWeight: 600 }}>
            STT y TTS — Proveedores
          </h4>
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 8 }}>
            <li style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              <span style={{ color: 'var(--blue)' }}>STT:</span> Groq Whisper-large-v3-turbo (default), Deepgram Nova-3, Google STT, Parakeet ONNX
            </li>
            <li style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              <span style={{ color: 'var(--blue)' }}>TTS:</span> Edge TTS (default), Deepgram Aura-2
            </li>
            <li style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              Arquitectura agnóstica al proveedor — intercambiable por configuración
            </li>
          </ul>
        </motion.div>
      </div>
    </div>
  )
}
