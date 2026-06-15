import { motion } from 'framer-motion'

const techs = [
  { label: 'Whisper', desc: 'Comandos de voz', position: 'Entrada' },
  { label: 'LLMs', desc: 'Decidir acción: comandos, guía o charla', position: 'Procesamiento' },
  { label: 'MCP', desc: 'Consultas semánticas a BD vectorizada', position: 'Contexto' },
  { label: 'Grafo', desc: 'Nodos = ubicaciones, Dijkstra para rutas', position: 'Navegación' },
  { label: 'TTS', desc: 'Respuestas de voz en tiempo real', position: 'Salida' },
]

function JarvisHUD() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, ease: [0.4, 0, 0.2, 1] }}
      style={{ position: 'relative', width: 260, height: 260, flexShrink: 0 }}
    >
      <svg viewBox="0 0 300 300" style={{ width: '100%', height: '100%' }}>
        {/* Outer ring */}
        <motion.circle
          cx="150" cy="150" r="140"
          fill="none"
          stroke="rgba(91, 164, 230, 0.15)"
          strokeWidth="1"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 1.2, delay: 0.2 }}
        />
        {/* Outer dashed ring */}
        <circle
          cx="150" cy="150" r="130"
          fill="none"
          stroke="rgba(91, 164, 230, 0.25)"
          strokeWidth="0.5"
          strokeDasharray="4 6"
        />
        {/* Main ring */}
        <motion.circle
          cx="150" cy="150" r="110"
          fill="none"
          stroke="rgba(91, 164, 230, 0.4)"
          strokeWidth="2"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 1, delay: 0.4 }}
        />
        {/* Inner ring */}
        <motion.circle
          cx="150" cy="150" r="85"
          fill="none"
          stroke="rgba(91, 164, 230, 0.2)"
          strokeWidth="1.5"
          strokeDasharray="8 4 2 4"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        />
        {/* Core ring */}
        <motion.circle
          cx="150" cy="150" r="55"
          fill="rgba(91, 164, 230, 0.03)"
          stroke="rgba(91, 164, 230, 0.5)"
          strokeWidth="1.5"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        />
        {/* Innermost glow */}
        <circle
          cx="150" cy="150" r="30"
          fill="rgba(91, 164, 230, 0.06)"
          stroke="rgba(91, 164, 230, 0.3)"
          strokeWidth="1"
        />

        {/* Tick marks on outer ring */}
        {Array.from({ length: 36 }).map((_, i) => {
          const angle = (i * 10) * Math.PI / 180
          const len = i % 3 === 0 ? 8 : 4
          const x1 = 150 + Math.cos(angle) * 130
          const y1 = 150 + Math.sin(angle) * 130
          const x2 = 150 + Math.cos(angle) * (130 - len)
          const y2 = 150 + Math.sin(angle) * (130 - len)
          return (
            <line
              key={i}
              x1={x1} y1={y1} x2={x2} y2={y2}
              stroke={i % 3 === 0 ? 'rgba(91, 164, 230, 0.5)' : 'rgba(91, 164, 230, 0.2)'}
              strokeWidth={i % 3 === 0 ? 1.5 : 0.7}
            />
          )
        })}

        {/* Arc segments */}
        <motion.path
          d="M 150 40 A 110 110 0 0 1 250 100"
          fill="none"
          stroke="rgba(91, 164, 230, 0.6)"
          strokeWidth="3"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.7, delay: 1 }}
        />
        <motion.path
          d="M 60 200 A 110 110 0 0 1 50 100"
          fill="none"
          stroke="rgba(91, 164, 230, 0.4)"
          strokeWidth="2"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.7, delay: 1.1 }}
        />
        <motion.path
          d="M 200 245 A 110 110 0 0 1 100 255"
          fill="none"
          stroke="rgba(91, 164, 230, 0.3)"
          strokeWidth="2"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.5, delay: 1.2 }}
        />

        {/* Node dots */}
        {[45, 120, 200, 280, 340].map((deg, i) => {
          const angle = deg * Math.PI / 180
          const x = 150 + Math.cos(angle) * 85
          const y = 150 + Math.sin(angle) * 85
          return (
            <motion.circle
              key={i}
              cx={x} cy={y} r="4"
              fill="#5BA4E6"
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 1.2 + i * 0.1 }}
            />
          )
        })}

        {/* Center text */}
        <motion.text
          x="150" y="147"
          textAnchor="middle"
          fontSize="16"
          fontWeight="600"
          fill="#5BA4E6"
          letterSpacing="3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.4 }}
        >
          BLU
        </motion.text>
        <motion.text
          x="150" y="165"
          textAnchor="middle"
          fontSize="7"
          fill="rgba(91, 164, 230, 0.5)"
          letterSpacing="1.5"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
        >
          AGENT CORE
        </motion.text>

        {/* Decorative crosshairs */}
        <line x1="150" y1="15" x2="150" y2="25" stroke="rgba(91, 164, 230, 0.3)" strokeWidth="1" />
        <line x1="150" y1="275" x2="150" y2="285" stroke="rgba(91, 164, 230, 0.3)" strokeWidth="1" />
        <line x1="15" y1="150" x2="25" y2="150" stroke="rgba(91, 164, 230, 0.3)" strokeWidth="1" />
        <line x1="275" y1="150" x2="285" y2="150" stroke="rgba(91, 164, 230, 0.3)" strokeWidth="1" />
      </svg>

      {/* Ambient glow */}
      <div style={{
        position: 'absolute',
        inset: '20%',
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(91, 164, 230, 0.08) 0%, transparent 70%)',
        pointerEvents: 'none',
      }} />
    </motion.div>
  )
}

export default function AgenteSlide() {
  return (
    <div style={{
      padding: '0 80px',
      maxWidth: 1100,
      display: 'grid',
      gridTemplateColumns: '260px 1fr',
      gap: 60,
      alignItems: 'center',
    }}>
      {/* Jarvis HUD */}
      <JarvisHUD />

      {/* Content */}
      <div>
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
          El Agente
        </motion.h2>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.15 }}
          style={{
            color: 'var(--text-dim)',
            fontSize: '1.05rem',
            marginBottom: 36,
            fontWeight: 300,
          }}
        >
          "Blu" — hace al robot inteligente mediante IA
        </motion.p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {techs.map((t, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + i * 0.1 }}
              style={{
                display: 'grid',
                gridTemplateColumns: '90px 90px 1fr',
                alignItems: 'center',
                gap: 16,
                padding: '14px 20px',
                background: 'var(--surface)',
                border: '1px solid var(--border)',
                borderRadius: 10,
              }}
            >
              <span style={{
                fontSize: '0.7rem',
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
                color: 'var(--text-muted)',
              }}>
                {t.position}
              </span>
              <span style={{
                fontSize: '0.95rem',
                fontWeight: 600,
                color: 'var(--blue)',
              }}>
                {t.label}
              </span>
              <span style={{
                fontSize: '0.9rem',
                color: 'var(--text-dim)',
              }}>
                {t.desc}
              </span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}
