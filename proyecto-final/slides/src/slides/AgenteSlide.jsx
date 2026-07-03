import { motion } from 'framer-motion'

export default function AgenteSlide() {
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
        Motor de Diálogo
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
        Clasificador híbrido en 2 etapas + consultas estructuradas vía MCP
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        {/* Hybrid Classifier */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          style={{
            padding: 28,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}
        >
          <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--blue)', marginBottom: 16, fontWeight: 600 }}>
            Clasificador Híbrido
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, position: 'relative' }}>
            {/* Stage 1 */}
            <div style={{
              padding: 14,
              border: '1px solid var(--border)',
              borderRadius: 8,
              background: 'var(--bg)',
            }}>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing: '0.05em' }}>
                ETAPA 1 — HEURÍSTICO
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-dim)' }}>
                Regex (YAML) para comandos directos y destinos conocidos
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--blue)', marginTop: 4 }}>
                ↓ Enruta directo a hardware si hay match
              </div>
            </div>

            {/* Stage 2 */}
            <div style={{
              padding: 14,
              border: '1px solid var(--border)',
              borderRadius: 8,
              background: 'var(--bg)',
            }}>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing: '0.05em' }}>
                ETAPA 2 — LLM INFERENCE
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-dim)' }}>
                Groq Llama 4 Scout — tool calling para navegación
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--blue)', marginTop: 4 }}>
                ↓ Memoria de 20 turnos + contexto dinámico
              </div>
            </div>
          </div>
        </motion.div>

        {/* MCP */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          style={{
            padding: 28,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}
        >
          <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--blue)', marginBottom: 16, fontWeight: 600 }}>
            MCP — Model Context Protocol
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {[
              { tool: 'get_place_info', desc: 'Información de ubicaciones' },
              { tool: 'search_food', desc: 'Opciones de cafetería' },
              { tool: 'search_store', desc: 'Inventario de tiendas' },
              { tool: 'get_service_directory', desc: 'Directorio de servicios' },
              { tool: 'get_campus_context', desc: 'Contexto general del campus' },
            ].map((t, i) => (
              <div key={i} style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: 8,
                padding: '8px 12px',
                background: 'var(--bg)',
                borderRadius: 6,
                fontSize: '0.78rem',
              }}>
                <span style={{ color: 'var(--blue)', fontWeight: 500, fontFamily: 'monospace' }}>
                  {t.tool}
                </span>
                <span style={{ color: 'var(--text-dim)' }}>
                  {t.desc}
                </span>
              </div>
            ))}
          </div>

          <div style={{
            marginTop: 12,
            padding: '8px 12px',
            background: 'var(--bg)',
            borderRadius: 6,
            fontSize: '0.75rem',
            color: 'var(--text-muted)',
            borderLeft: '2px solid var(--blue)',
          }}>
            SQL parametrizado + solo-lectura — sin inyección
          </div>
        </motion.div>
      </div>

      {/* Bottom: context injection */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        style={{
          marginTop: 20,
          padding: '12px 20px',
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 8,
          display: 'flex',
          gap: 20,
          alignItems: 'center',
          flexWrap: 'wrap',
        }}
      >
        <span style={{ fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', fontWeight: 600 }}>
          System Prompt Dinámico:
        </span>
        {['Telemetría del robot', 'Entidades de sesión', 'Grafo navegable', 'Confirmación obligatoria'].map((item, i) => (
          <span key={i} style={{
            fontSize: '0.75rem',
            color: 'var(--text-dim)',
            background: 'var(--bg)',
            padding: '4px 10px',
            borderRadius: 4,
          }}>
            {item}
          </span>
        ))}
      </motion.div>
    </div>
  )
}
