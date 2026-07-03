import { motion } from 'framer-motion'

export default function MetricasSlide() {
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
        Resultados — Fase 1 y 2
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
        Guardrails (OWASP ASVS) + Clasificación de intenciones (ISO 25023)
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        {/* Guardrails */}
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
            Phase 1 — ToolValidator
          </h4>

          <div style={{ display: 'flex', gap: 16, marginBottom: 20 }}>
            <div style={{ textAlign: 'center', flex: 1 }}>
              <div style={{ fontSize: '2rem', fontWeight: 600, color: 'var(--blue)' }}>49</div>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Prompts</div>
            </div>
            <div style={{ textAlign: 'center', flex: 1 }}>
              <div style={{ fontSize: '2rem', fontWeight: 600, color: '#6BCB8A' }}>100%</div>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Validez</div>
            </div>
            <div style={{ textAlign: 'center', flex: 1 }}>
              <div style={{ fontSize: '2rem', fontWeight: 600, color: 'var(--text-dim)' }}>0</div>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Errores</div>
            </div>
          </div>

          <div style={{
            padding: 10,
            background: 'var(--bg)',
            borderRadius: 6,
            fontSize: '0.78rem',
            color: 'var(--text-dim)',
            lineHeight: 1.5,
          }}>
            10/10 navegación → tool calls válidos. Ruido y conversación → texto limpio sin sintaxis residual.
          </div>

          <div style={{
            marginTop: 12,
            padding: '8px 12px',
            background: 'var(--bg)',
            borderRadius: 6,
            fontSize: '0.72rem',
            color: 'var(--text-muted)',
          }}>
            Validación: existencia de tool, campos requeridos, tipos correctos — correcciones conservadoras
          </div>
        </motion.div>

        {/* Classification */}
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
            Phase 2 — Clasificación (40 frases)
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {[
              { cls: 'Navegación', p: '0.77', r: '1.00', f1: '0.87' },
              { cls: 'Comando', p: '0.89', r: '0.80', f1: '0.84' },
              { cls: 'Conversación', p: '0.56', r: '0.77', f1: '0.65' },
              { cls: 'Ruido', p: '0.00', r: '0.00', f1: '0.00' },
            ].map((row, i) => (
              <div key={i} style={{
                display: 'grid',
                gridTemplateColumns: '100px 1fr 1fr 1fr',
                gap: 8,
                padding: '8px 12px',
                background: 'var(--bg)',
                borderRadius: 6,
                fontSize: '0.78rem',
                alignItems: 'center',
              }}>
                <span style={{ color: 'var(--text)', fontWeight: 500 }}>{row.cls}</span>
                <span style={{ color: 'var(--text-dim)' }}>P={row.p}</span>
                <span style={{ color: 'var(--text-dim)' }}>R={row.r}</span>
                <span style={{ color: 'var(--blue)', fontWeight: 600 }}>F1={row.f1}</span>
              </div>
            ))}
          </div>

          <div style={{
            marginTop: 12,
            padding: '8px 12px',
            background: 'var(--bg)',
            borderRadius: 6,
            fontSize: '0.72rem',
            color: 'var(--text-muted)',
            lineHeight: 1.5,
          }}>
            Recall 1.0 en navegación. Ruido al 0%: el sistema no implementa clase de rechazo explícito.
          </div>
        </motion.div>
      </div>
    </div>
  )
}
