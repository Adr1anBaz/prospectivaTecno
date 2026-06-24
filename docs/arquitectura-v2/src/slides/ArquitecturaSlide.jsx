import { motion } from 'framer-motion'

export default function ArquitecturaSlide() {
  return (
    <div style={{ padding: '0 60px', maxWidth: 1100 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 40,
        }}
      >
        Arquitectura
      </motion.h2>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 16,
          padding: 32,
        }}
      >
        {/* Architecture Diagram SVG */}
        <svg viewBox="0 0 900 420" style={{ width: '100%', maxHeight: 420 }}>
          {/* Background grid */}
          <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.02)" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="900" height="420" fill="url(#grid)" />

          {/* EventBus — Center */}
          <rect x="350" y="160" width="200" height="80" rx="12" fill="rgba(91,164,230,0.08)" stroke="var(--blue)" strokeWidth="2" />
          <text x="450" y="190" textAnchor="middle" fontSize="14" fontWeight="600" fill="var(--blue)" letterSpacing="1">EVENT BUS</text>
          <text x="450" y="210" textAnchor="middle" fontSize="10" fill="rgba(228,228,232,0.4)" letterSpacing="0.5">mp.Queue broadcast</text>
          <text x="450" y="225" textAnchor="middle" fontSize="10" fill="rgba(228,228,232,0.4)" letterSpacing="0.5">per-process private queues</text>

          {/* AudioProcess — Top Left */}
          <rect x="60" y="40" width="180" height="70" rx="10" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="150" y="62" textAnchor="middle" fontSize="12" fontWeight="600" fill="var(--text)">AudioProcess</text>
          <text x="150" y="78" textAnchor="middle" fontSize="9" fill="var(--text-dim)">Mic · VAD · Vosk Wake</text>
          <text x="150" y="92" textAnchor="middle" fontSize="9" fill="var(--text-muted)">WAKE_WORD → LISTENING</text>

          {/* Arrow: AudioProcess → EventBus */}
          <line x1="240" y1="90" x2="350" y2="170" stroke="rgba(91,164,230,0.3)" strokeWidth="1.5" />
          <text x="285" y="120" textAnchor="middle" fontSize="8" fill="var(--text-muted)">SPEECH_COMPLETED</text>

          {/* Orquestador — Top Right */}
          <rect x="660" y="40" width="180" height="70" rx="10" fill="var(--surface)" stroke="var(--blue)" strokeWidth="1.5" />
          <text x="750" y="62" textAnchor="middle" fontSize="12" fontWeight="600" fill="var(--blue)">Orquestador</text>
          <text x="750" y="78" textAnchor="middle" fontSize="9" fill="var(--text-dim)">Classifier · LLM · Tools</text>
          <text x="750" y="92" textAnchor="middle" fontSize="9" fill="var(--text-muted)">AUDIO_SYNTHESIZED</text>

          {/* Arrow: EventBus → Orquestador */}
          <line x1="550" y1="170" x2="660" y2="90" stroke="rgba(91,164,230,0.3)" strokeWidth="1.5" />
          <text x="610" y="120" textAnchor="middle" fontSize="8" fill="var(--text-muted)">TEXT_TRANSCRIBED</text>

          {/* AudioPlayback — Bottom Left */}
          <rect x="60" y="310" width="180" height="70" rx="10" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="150" y="332" textAnchor="middle" fontSize="12" fontWeight="600" fill="var(--text)">AudioPlayback</text>
          <text x="150" y="348" textAnchor="middle" fontSize="9" fill="var(--text-dim)">sounddevice speaker</text>
          <text x="150" y="362" textAnchor="middle" fontSize="9" fill="var(--text-muted)">plays WAV chunks</text>

          {/* Arrow: EventBus → AudioPlayback */}
          <line x1="380" y1="240" x2="150" y2="310" stroke="rgba(91,164,230,0.3)" strokeWidth="1.5" />
          <text x="250" y="285" textAnchor="middle" fontSize="8" fill="var(--text-muted)">AUDIO_SYNTHESIZED</text>

          {/* MovementProcess — Bottom Right */}
          <rect x="660" y="310" width="180" height="70" rx="10" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="750" y="332" textAnchor="middle" fontSize="12" fontWeight="600" fill="var(--text)">MovementProcess</text>
          <text x="750" y="348" textAnchor="middle" fontSize="9" fill="var(--text-dim)">CSV route executor</text>
          <text x="750" y="362" textAnchor="middle" fontSize="9" fill="var(--text-muted)">placeholder for Go2</text>

          {/* Arrow: EventBus → MovementProcess */}
          <line x1="520" y1="240" x2="750" y2="310" stroke="rgba(91,164,230,0.3)" strokeWidth="1.5" />
          <text x="640" y="285" textAnchor="middle" fontSize="8" fill="var(--text-muted)">MOVEMENT_SEQUENCE</text>

          {/* External Services — Right side */}
          <rect x="660" y="170" width="180" height="80" rx="10" fill="rgba(91,164,230,0.03)" stroke="rgba(91,164,230,0.2)" strokeWidth="1" strokeDasharray="4 4" />
          <text x="750" y="192" textAnchor="middle" fontSize="11" fontWeight="600" fill="rgba(91,164,230,0.7)">Servicios Externos</text>
          <text x="750" y="210" textAnchor="middle" fontSize="9" fill="var(--text-dim)">Groq API · Deepgram API</text>
          <text x="750" y="225" textAnchor="middle" fontSize="9" fill="var(--text-dim)">MCP Server · Route API</text>
          <text x="750" y="240" textAnchor="middle" fontSize="9" fill="var(--text-muted)">PostgreSQL campus DB</text>

          {/* Dotted line: Orquestador → External */}
          <line x1="800" y1="110" x2="800" y2="170" stroke="rgba(91,164,230,0.2)" strokeWidth="1" strokeDasharray="4 4" />
          <text x="830" y="145" textAnchor="start" fontSize="8" fill="var(--text-muted)">HTTP / JSON-RPC</text>

          {/* Legend */}
          <g transform="translate(60, 170)">
            <rect x="0" y="0" width="12" height="12" rx="3" fill="var(--surface)" stroke="var(--border)" />
            <text x="18" y="10" fontSize="9" fill="var(--text-dim)">Proceso</text>
            <rect x="0" y="20" width="12" height="12" rx="3" fill="rgba(91,164,230,0.08)" stroke="var(--blue)" strokeWidth="1.5" />
            <text x="18" y="30" fontSize="9" fill="var(--text-dim)">EventBus</text>
            <rect x="0" y="40" width="12" height="12" rx="3" fill="rgba(91,164,230,0.03)" stroke="rgba(91,164,230,0.3)" strokeWidth="1" strokeDasharray="3 3" />
            <text x="18" y="50" fontSize="9" fill="var(--text-dim)">Externo</text>
          </g>
        </svg>
      </motion.div>

      {/* Process descriptions */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: 16,
        marginTop: 24,
      }}>
        {[
          { name: 'AudioProcess', desc: 'Captura micrófono, VAD, wake word "blu", STT streaming' },
          { name: 'Orquestador', desc: 'Recibe eventos, clasifica intención, LLM con tool calling, síntesis TTS' },
          { name: 'AudioPlayback', desc: 'Reproduce audio WAV generado por Deepgram TTS' },
          { name: 'MovementProcess', desc: 'Placeholder para ejecutar secuencias de movimiento CSV' },
        ].map((p, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 + i * 0.1 }}
            style={{
              padding: '16px',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 10,
            }}
          >
            <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--blue)', marginBottom: 6 }}>{p.name}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>{p.desc}</div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
