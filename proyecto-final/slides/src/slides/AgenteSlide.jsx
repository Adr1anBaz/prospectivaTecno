import { motion } from 'framer-motion'

export default function AgenteSlide() {
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
        Diseño del Agente Conversacional
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
        Un motor de diálogo que combina rapidez determinista con flexibilidad semántica
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        {/* Classifier */}
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
            Clasificador Híbrido
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            <div style={{
              padding: 14,
              border: '1px solid var(--border)',
              borderRadius: 8,
              background: 'var(--bg)',
            }}>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing: '0.05em' }}>
                ETAPA 1 — HEURÍSTICO
              </div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-dim)' }}>
                Patrones de expresión regular (YAML) para comandos directos y destinos conocidos. Sin latencia de red.
              </div>
            </div>

            <div style={{
              padding: 14,
              border: '1px solid var(--border)',
              borderRadius: 8,
              background: 'var(--bg)',
            }}>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing: '0.05em' }}>
                ETAPA 2 — LLM
              </div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-dim)' }}>
                Modelo de Lenguaje para consultas semánticas, razonamiento contextual y generación de diálogo.
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
            padding: 24,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}
        >
          <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--blue)', marginBottom: 16, fontWeight: 600 }}>
            Acceso a Datos — MCP
          </h4>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', marginBottom: 16, lineHeight: 1.5 }}>
            El Model Context Protocol permite al LLM consultar información estructurada del campus mediante herramientas parametrizadas.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {[
              'Información de ubicaciones y edificios',
              'Opciones de cafetería y horarios',
              'Directorio de servicios y oficinas',
              'Inventario de tiendas del campus',
            ].map((item, i) => (
              <div key={i} style={{
                fontSize: '0.78rem',
                color: 'var(--text-dim)',
                padding: '6px 12px',
                background: 'var(--bg)',
                borderRadius: 4,
                borderLeft: '2px solid var(--blue)',
              }}>
                {item}
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Context management */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        style={{
          marginTop: 20,
          padding: '14px 20px',
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 8,
          display: 'flex',
          gap: 16,
          alignItems: 'center',
          flexWrap: 'wrap',
        }}
      >
        <span style={{ fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', fontWeight: 600 }}>
          Memoria de Conversación:
        </span>
        {['Ventana de 20 turnos', 'Entidades persistentes', 'Contexto dinámico inyectado', 'Confirmación obligatoria'].map((item, i) => (
          <span key={i} style={{
            fontSize: '0.72rem',
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
