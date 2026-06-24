import { motion } from 'framer-motion'

export default function AudioPipelineSlide() {
  return (
    <div style={{ padding: '0 60px', maxWidth: 1100 }}>
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
        Pipeline de Audio
      </motion.h2>

      {/* State Machine Diagram */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 16,
          padding: 28,
          marginBottom: 24,
        }}
      >
        <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--text-muted)', marginBottom: 20 }}>
          State Machine — AudioProcess
        </div>
        <svg viewBox="0 0 800 160" style={{ width: '100%', maxHeight: 160 }}>
          {/* WAKE_WORD state */}
          <rect x="40" y="50" width="140" height="60" rx="10" fill="var(--surface)" stroke="var(--blue)" strokeWidth="2" />
          <text x="110" y="75" textAnchor="middle" fontSize="12" fontWeight="600" fill="var(--blue)">WAKE_WORD</text>
          <text x="110" y="92" textAnchor="middle" fontSize="9" fill="var(--text-dim)">Escucha "blu"</text>
          <text x="110" y="105" textAnchor="middle" fontSize="8" fill="var(--text-muted)">Vosk offline</text>

          {/* Arrow to LISTENING */}
          <line x1="180" y1="80" x2="280" y2="80" stroke="var(--blue)" strokeWidth="1.5" />

          <text x="230" y="72" textAnchor="middle" fontSize="8" fill="var(--text-muted)">Wake detected</text>

          {/* LISTENING state */}
          <rect x="280" y="50" width="140" height="60" rx="10" fill="rgba(91,164,230,0.08)" stroke="var(--blue)" strokeWidth="2" />
          <text x="350" y="75" textAnchor="middle" fontSize="12" fontWeight="600" fill="var(--blue)">LISTENING</text>
          <text x="350" y="92" textAnchor="middle" fontSize="9" fill="var(--text-dim)">Silero VAD (thr=0.3)</text>
          <text x="350" y="105" textAnchor="middle" fontSize="8" fill="var(--text-muted)">Deepgram Nova-3 streaming</text>

          {/* Arrow to COOLDOWN */}
          <line x1="420" y1="80" x2="520" y2="80" stroke="var(--blue)" strokeWidth="1.5" />

          <text x="470" y="72" textAnchor="middle" fontSize="8" fill="var(--text-muted)">VAD silent</text>

          {/* COOLDOWN state */}
          <rect x="520" y="50" width="140" height="60" rx="10" fill="var(--surface)" stroke="var(--border)" strokeWidth="1.5" />
          <text x="590" y="75" textAnchor="middle" fontSize="12" fontWeight="600" fill="var(--text)">COOLDOWN</text>
          <text x="590" y="92" textAnchor="middle" fontSize="9" fill="var(--text-dim)">1s cooldown</text>
          <text x="590" y="105" textAnchor="middle" fontSize="8" fill="var(--text-muted)">~31 audio chunks</text>

          {/* Arrow back to WAKE_WORD */}
          <path d="M 590 50 Q 590 20 350 20 Q 110 20 110 50" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1.5" strokeDasharray="4 4" />

          <text x="350" y="32" textAnchor="middle" fontSize="8" fill="var(--text-muted)">Cooldown ended</text>

          {/* Arrow: LISTENING → WAKE_WORD (timeout) */}
          <path d="M 350 110 Q 350 140 230 140 Q 110 140 110 110" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="1" strokeDasharray="3 3" />

          <text x="230" y="132" textAnchor="middle" fontSize="7" fill="var(--text-muted)">15s timeout</text>

          {/* CONVERSATION_CONTINUING event */}
          <line x1="350" y1="110" x2="350" y2="130" stroke="#E6A85B" strokeWidth="1.5" strokeDasharray="3 3" />
          <text x="355" y="128" textAnchor="start" fontSize="7" fill="#E6A85B">CONVERSATION_CONTINUING</text>
        </svg>
      </motion.div>

      {/* Audio flow */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 12, alignItems: 'center' }}>
        {[
          { label: 'Mic', desc: 'sounddevice', icon: '🎤' },
          { label: 'VAD', desc: 'Silero (thr=0.3)', icon: '🔊' },
          { label: 'Wake', desc: 'Vosk "blu"', icon: '👂' },
          { label: 'STT', desc: 'Groq / Deepgram', icon: '📝' },
          { label: 'Orquestador', desc: 'Classifier + LLM', icon: '🧠' },
          { label: 'Speaker', desc: 'Deepgram TTS', icon: '🔈' },
        ].map((step, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + i * 0.1 }}
            style={{
              padding: '16px 12px',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 10,
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: '1.5rem', marginBottom: 6 }}>{step.icon}</div>
            <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text)', marginBottom: 4 }}>{step.label}</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>{step.desc}</div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
