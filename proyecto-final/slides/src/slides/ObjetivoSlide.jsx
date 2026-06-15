import { motion } from 'framer-motion'

const queries = [
  '"Llévame a la cafetería con el desayuno más barato"',
  '"Llévame a donde haya buena señal de internet"',
  '"Llévame a la cafetería que no tenga tantas personas ahorita"',
]

export default function ObjetivoSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1000 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 16,
        }}
      >
        Objetivo
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '1.1rem',
          marginBottom: 48,
          fontWeight: 300,
        }}
      >
        Un agente capaz de guiar usuarios por la universidad
        respondiendo peticiones en lenguaje natural
      </motion.p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {queries.map((q, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 + i * 0.15 }}
            style={{
              padding: '20px 28px',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 12,
              fontSize: '1.05rem',
              fontStyle: 'italic',
              color: 'var(--text-dim)',
              borderLeft: '3px solid var(--blue)',
            }}
          >
            {q}
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.85 }}
        style={{ marginTop: 48 }}
      >
        <img
          src={`${import.meta.env.BASE_URL}images/muestra.png`}
          alt="Muestra del agente"
          style={{
            width: '100%',
            height: 'auto',
            display: 'block',
            borderRadius: 12,
          }}
        />
      </motion.div>
    </div>
  )
}
