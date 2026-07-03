import { motion } from 'framer-motion'

export default function ConclusionesSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 900, textAlign: 'center' }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 24,
        }}
      >
          Guía Autónoma
        <br />
        <span style={{ color: 'var(--blue)', fontSize: '0.7em' }}>
          con Agentes Conversacionales
        </span>
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '1rem',
          lineHeight: 1.7,
          marginBottom: 48,
          maxWidth: 650,
          marginInline: 'auto',
        }}
      >
        Un sistema que integra procesamiento de voz, modelos de lenguaje y robótica móvil
        para ofrecer navegación asistida en entornos universitarios de forma natural,
        sin necesidad de aplicaciones ni infraestructura adicional.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        style={{
          display: 'flex',
          gap: 32,
          justifyContent: 'center',
          marginBottom: 48,
        }}
      >
        {[
          { icon: '🎤', label: 'Voz' },
          { icon: '🧠', label: 'IA' },
          { icon: '🤖', label: 'Robot' },
          { icon: '🗺️', label: 'Ruta' },
        ].map((item, i) => (
          <div key={i} style={{ textAlign: 'center' }}>
            <div style={{
              width: 56,
              height: 56,
              borderRadius: '50%',
              background: 'var(--surface)',
              border: '2px solid var(--blue)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 22,
              margin: '0 auto 8px',
            }}>
              {item.icon}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', fontWeight: 500 }}>
              {item.label}
            </div>
          </div>
        ))}
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        style={{
          fontSize: '0.75rem',
          color: 'var(--text-muted)',
          lineHeight: 1.6,
        }}
      >
        <div>Adrián Bazaldua · Sebastián Enguilo · Fernando Pérez</div>
        <div>Universidad Iberoamericana — Departamento de Ingeniería</div>
      </motion.div>
    </div>
  )
}
