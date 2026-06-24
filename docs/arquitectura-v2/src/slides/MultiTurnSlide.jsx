import { motion } from 'framer-motion'

export default function MultiTurnSlide() {
  return (
    <div style={{ padding: '0 60px', maxWidth: 1000 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 32,
        }}
      >
        Modo Conversación
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '1.05rem',
          marginBottom: 32,
          fontWeight: 300,
          maxWidth: 700,
        }}
      >
        Después de una respuesta conversacional, el sistema permanece en modo LISTENING
        sin requerir el wake word. Timeout de 15 segundos de silencio.
      </motion.p>

      {/* Conversation Flow Diagram */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 16,
          padding: 28,
          marginBottom: 24,
        }}
      >
        <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--text-muted)', marginBottom: 20 }}>
          Flujo Multi-Turn
        </div>
        <svg viewBox="0 0 800 200" style={{ width: '100%', maxHeight: 200 }}>
          {/* Turn 1: User */}
          <rect x="20" y="20" width="140" height="50" rx="8" fill="rgba(91,164,230,0.08)" stroke="var(--blue)" strokeWidth="1.5" />
          <text x="90" y="40" textAnchor="middle" fontSize="10" fontWeight="600" fill="var(--blue)">Usuario</text>
          <text x="90" y="55" textAnchor="middle" fontSize="8" fill="var(--text-dim)">"Blu, tengo hambre"</text>

          {/* Arrow */}
          <line x1="160" y1="45" x2="210" y2="45" stroke="var(--blue)" strokeWidth="1.5" />


          {/* System Response */}
          <rect x="210" y="20" width="160" height="50" rx="8" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="290" y="40" textAnchor="middle" fontSize="10" fontWeight="600" fill="var(--text)">Sistema</text>
          <text x="290" y="55" textAnchor="middle" fontSize="8" fill="var(--text-dim)">"¿Quieres restaurante o tienda?"</text>

          {/* Event: CONVERSATION_CONTINUING */}
          <line x1="290" y1="70" x2="290" y2="95" stroke="#E6A85B" strokeWidth="1.5" strokeDasharray="3 3" />

          <rect x="210" y="95" width="160" height="28" rx="6" fill="rgba(230,168,91,0.05)" stroke="#E6A85B" strokeWidth="1" strokeDasharray="3 3" />
          <text x="290" y="113" textAnchor="middle" fontSize="8" fill="#E6A85B" fontWeight="500">CONVERSATION_CONTINUING</text>

          {/* Arrow down to AudioProcess */}
          <line x1="290" y1="123" x2="290" y2="140" stroke="#E6A85B" strokeWidth="1.5" strokeDasharray="3 3" />


          {/* AudioProcess stays LISTENING */}
          <rect x="210" y="140" width="160" height="40" rx="8" fill="rgba(91,164,230,0.05)" stroke="var(--blue)" strokeWidth="1" />
          <text x="290" y="158" textAnchor="middle" fontSize="9" fontWeight="600" fill="var(--blue)">AudioProcess</text>
          <text x="290" y="172" textAnchor="middle" fontSize="8" fill="var(--text-dim)">LISTENING (no wake needed)</text>

          {/* Turn 2: User (no wake word) */}
          <rect x="420" y="140" width="140" height="40" rx="8" fill="rgba(91,164,230,0.08)" stroke="var(--blue)" strokeWidth="1.5" />
          <text x="490" y="158" textAnchor="middle" fontSize="10" fontWeight="600" fill="var(--blue)">Usuario</text>
          <text x="490" y="172" textAnchor="middle" fontSize="8" fill="var(--text-dim)">"Un restaurante"</text>

          {/* Arrow */}
          <line x1="370" y1="160" x2="420" y2="160" stroke="var(--blue)" strokeWidth="1.5" />


          {/* Final Response */}
          <rect x="590" y="140" width="180" height="40" rx="8" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="680" y="158" textAnchor="middle" fontSize="10" fontWeight="600" fill="var(--text)">Sistema</text>
          <text x="680" y="172" textAnchor="middle" fontSize="8" fill="var(--text-dim)">"Te recomiendo el Giornale..."</text>

          {/* Arrow */}
          <line x1="560" y1="160" x2="590" y2="160" stroke="var(--blue)" strokeWidth="1.5" />

        </svg>
      </motion.div>

      {/* Features */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
        {[
          {
            label: 'Evento',
            value: 'CONVERSATION_CONTINUING',
            desc: 'Publicado por Orquestador después de respuesta conversacional',
          },
          {
            label: 'Transición',
            value: 'WAKE_WORD → LISTENING',
            desc: 'AudioProcess recibe evento y salta directo a escucha',
          },
          {
            label: 'Timeout',
            value: '15 segundos',
            desc: 'De silencio vuelve a WAKE_WORD automáticamente',
          },
        ].map((f, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 + i * 0.1 }}
            style={{
              padding: '20px',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 10,
            }}
          >
            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 8 }}>{f.label}</div>
            <div style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--blue)', marginBottom: 6 }}>{f.value}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>{f.desc}</div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
