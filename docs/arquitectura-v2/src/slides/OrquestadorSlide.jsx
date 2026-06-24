import { motion } from 'framer-motion'

export default function OrquestadorSlide() {
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
        Orquestador
      </motion.h2>

      {/* Tool Calling Flow Diagram */}
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
        <svg viewBox="0 0 840 320" style={{ width: '100%', maxHeight: 320 }}>
          {/* Input */}
          <rect x="20" y="20" width="120" height="50" rx="8" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="80" y="40" textAnchor="middle" fontSize="10" fontWeight="600" fill="var(--text)">TEXT_TRANSCRIBED</text>
          <text x="80" y="55" textAnchor="middle" fontSize="8" fill="var(--text-muted)">User query</text>

          {/* Arrow */}
          <line x1="140" y1="45" x2="180" y2="45" stroke="var(--blue)" strokeWidth="1.5" />


          {/* Classifier */}
          <rect x="180" y="20" width="120" height="50" rx="8" fill="rgba(91,164,230,0.05)" stroke="var(--blue)" strokeWidth="1" />
          <text x="240" y="40" textAnchor="middle" fontSize="10" fontWeight="600" fill="var(--blue)">Classifier</text>
          <text x="240" y="55" textAnchor="middle" fontSize="8" fill="var(--text-muted)">YAML patterns</text>

          {/* Branch: NAVEGAR */}
          <line x1="240" y1="70" x2="240" y2="100" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
          <line x1="240" y1="100" x2="120" y2="100" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
          <line x1="120" y1="100" x2="120" y2="120" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />

          <rect x="60" y="120" width="120" height="40" rx="8" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="120" y="138" textAnchor="middle" fontSize="9" fill="var(--text-dim)">NAVEGAR → Route API</text>
          <text x="120" y="150" textAnchor="middle" fontSize="7" fill="var(--text-muted)">Dijkstra + movement CSV</text>

          {/* Branch: COMANDO */}
          <line x1="240" y1="100" x2="360" y2="100" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
          <line x1="360" y1="100" x2="360" y2="120" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />

          <rect x="300" y="120" width="120" height="40" rx="8" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="360" y="138" textAnchor="middle" fontSize="9" fill="var(--text-dim)">COMANDO → Actions</text>
          <text x="360" y="150" textAnchor="middle" fontSize="7" fill="var(--text-muted)">sit, dance, wave, walk</text>

          {/* Branch: HABLAR → LLM */}
          <line x1="240" y1="100" x2="600" y2="100" stroke="var(--blue)" strokeWidth="1.5" />
          <line x1="600" y1="100" x2="600" y2="120" stroke="var(--blue)" strokeWidth="1.5" />


          {/* LLM */}
          <rect x="540" y="120" width="120" height="50" rx="8" fill="rgba(91,164,230,0.08)" stroke="var(--blue)" strokeWidth="2" />
          <text x="600" y="142" textAnchor="middle" fontSize="11" fontWeight="600" fill="var(--blue)">Groq LLM</text>
          <text x="600" y="158" textAnchor="middle" fontSize="8" fill="var(--text-muted)">llama-3.1-8b-instant</text>

          {/* Arrow: LLM → Tool Calls */}
          <line x1="600" y1="170" x2="600" y2="200" stroke="var(--blue)" strokeWidth="1.5" strokeDasharray="4 4" />

          <text x="620" y="188" textAnchor="start" fontSize="8" fill="var(--text-muted)">finish_reason=tool_calls</text>

          {/* Tools box */}
          <rect x="460" y="200" width="280" height="50" rx="8" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="600" y="220" textAnchor="middle" fontSize="10" fontWeight="600" fill="var(--text)">15 MCP Tools</text>
          <text x="600" y="235" textAnchor="middle" fontSize="8" fill="var(--text-dim)">search_places · get_menu · find_office · crowd_levels ...</text>

          {/* Arrow: Tools → LLM (results) */}
          <line x1="460" y1="225" x2="420" y2="225" stroke="var(--blue)" strokeWidth="1.5" />

          <text x="440" y="218" textAnchor="middle" fontSize="7" fill="var(--text-muted)">results</text>

          {/* Final Response */}
          <rect x="280" y="200" width="120" height="50" rx="8" fill="rgba(91,164,230,0.05)" stroke="var(--blue)" strokeWidth="1" />
          <text x="340" y="220" textAnchor="middle" fontSize="10" fontWeight="600" fill="var(--blue)">Respuesta Final</text>
          <text x="340" y="235" textAnchor="middle" fontSize="8" fill="var(--text-muted)">TTS synthesis</text>

          {/* Arrow to TTS */}
          <line x1="340" y1="250" x2="340" y2="280" stroke="var(--blue)" strokeWidth="1.5" />


          {/* TTS */}
          <rect x="280" y="280" width="120" height="30" rx="6" fill="var(--surface)" stroke="var(--border)" strokeWidth="1" />
          <text x="340" y="298" textAnchor="middle" fontSize="9" fill="var(--text-dim)">Deepgram Aura-2</text>

          {/* Conversation continuing */}
          <line x1="400" y1="295" x2="500" y2="295" stroke="#E6A85B" strokeWidth="1.5" strokeDasharray="3 3" />

          <text x="450" y="288" textAnchor="middle" fontSize="7" fill="#E6A85B">CONVERSATION_CONTINUING</text>
          <text x="530" y="298" textAnchor="start" fontSize="7" fill="#E6A85B">→ AudioProcess LISTENING</text>
        </svg>
      </motion.div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
        {[
          { label: 'LLM Model', value: 'llama-3.1-8b-instant', sub: 'Groq — 15 tools' },
          { label: 'Tool Calling', value: 'Nativo', sub: 'finish_reason=tool_calls' },
          { label: 'Context', value: 'Multi-turn', sub: 'ConversationMemory + current_node' },
        ].map((s, i) => (
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
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 8 }}>{s.label}</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--blue)', marginBottom: 4 }}>{s.value}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>{s.sub}</div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
