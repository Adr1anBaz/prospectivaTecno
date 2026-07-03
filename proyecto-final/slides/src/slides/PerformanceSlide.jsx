import { motion } from 'framer-motion'

export default function PerformanceSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1000 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 8,
        }}
      >
        Resultados — Fase 3 y 4
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '0.85rem',
          marginBottom: 32,
          fontWeight: 300,
        }}
      >
        Latencia del pipeline (ISO 25022) + Consumo de recursos (ISO 25023)
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* Latency breakdown */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          style={{
            padding: 24,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}
        >
          <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--blue)', marginBottom: 16, fontWeight: 600 }}>
            Latencia del Pipeline
          </h4>

          {[
            { stage: 'STT (Groq Whisper)', time: '750 ms', bar: 75 },
            { stage: 'LLM (Llama 4 Scout)', time: '350 ms', bar: 35 },
            { stage: 'ToolValidator', time: '&lt; 0.01 ms', bar: 0.5 },
            { stage: 'TTS (Edge, estimado)', time: '500 ms', bar: 50 },
          ].map((row, i) => (
            <div key={i} style={{ marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: 4 }}>
                <span style={{ color: 'var(--text-dim)' }}>{row.stage}</span>
                <span style={{ color: 'var(--blue)', fontWeight: 500 }}>{row.time}</span>
              </div>
              <div style={{ height: 4, background: 'var(--bg)', borderRadius: 2, overflow: 'hidden' }}>
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${row.bar}%` }}
                  transition={{ delay: 0.4 + i * 0.1, duration: 0.6 }}
                  style={{ height: '100%', background: 'var(--blue)', borderRadius: 2 }}
                />
              </div>
            </div>
          ))}

          <div style={{
            marginTop: 8,
            padding: '10px 14px',
            background: 'var(--bg)',
            borderRadius: 6,
            display: 'flex',
            justifyContent: 'space-between',
            fontSize: '0.82rem',
          }}>
            <span style={{ color: 'var(--text-dim)' }}>Total estimado</span>
            <span style={{ color: 'var(--blue)', fontWeight: 700 }}>~1.6 s</span>
          </div>
        </motion.div>

        {/* EventBus + Resources */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          style={{
            padding: 24,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}
        >
          <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--blue)', marginBottom: 16, fontWeight: 600 }}>
            Event Bus + Recursos
          </h4>

          {/* EventBus */}
          <div style={{
            padding: 12,
            background: 'var(--bg)',
            borderRadius: 8,
            marginBottom: 16,
          }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 8, letterSpacing: '0.05em', textTransform: 'uppercase' }}>
              Stress Test — 100 eventos
            </div>
            <div style={{ display: 'flex', gap: 20 }}>
              {[
                { label: 'Entregados', value: '100%', color: '#6BCB8A' },
                { label: 'Pérdidas', value: '0', color: 'var(--text-dim)' },
                { label: 'Throughput', value: '1300/s', color: 'var(--blue)' },
              ].map((s, i) => (
                <div key={i} style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '1.2rem', fontWeight: 600, color: s.color }}>{s.value}</div>
                  <div style={{ fontSize: '0.6rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{s.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* RAM consumption */}
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 8, letterSpacing: '0.05em', textTransform: 'uppercase' }}>
              Consumo del proceso conversacional
            </div>
            {[
              { state: 'Idle', ram: '23.5 MB', cpu: '0.7%' },
              { state: 'Procesando', ram: '45.7 MB', cpu: '0.2%' },
              { state: 'Playback', ram: '85.7 MB', cpu: '0.0%' },
            ].map((row, i) => (
              <div key={i} style={{
                display: 'grid',
                gridTemplateColumns: '80px 1fr 1fr',
                gap: 8,
                padding: '6px 10px',
                background: i % 2 === 0 ? 'var(--bg)' : 'transparent',
                borderRadius: 4,
                fontSize: '0.75rem',
                alignItems: 'center',
              }}>
                <span style={{ color: 'var(--text)', fontWeight: 500 }}>{row.state}</span>
                <span style={{ color: 'var(--text-dim)' }}>RAM {row.ram}</span>
                <span style={{ color: 'var(--text-dim)' }}>CPU {row.cpu}</span>
              </div>
            ))}
            <div style={{
              marginTop: 8,
              fontSize: '0.7rem',
              color: 'var(--text-muted)',
              padding: '6px 10px',
              background: 'var(--bg)',
              borderRadius: 4,
              borderLeft: '2px solid var(--blue)',
            }}>
              Pico 85.7 MB ≈ 1% de RAM de una Raspberry Pi 5
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
