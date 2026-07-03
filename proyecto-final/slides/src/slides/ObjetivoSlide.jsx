import { motion } from 'framer-motion'

const problems = [
  {
    title: 'Orientación en campus',
    desc: 'Visitantes, estudiantes de nuevo ingreso y personal externo enfrentan dificultades para ubicar edificios, laboratorios, cafeterías y oficinas administrativas.',
  },
  {
    title: 'Señalética estática',
    desc: 'Los mapas y letreros fijos no se actualizan en tiempo real ni contemplan cierres temporales, horarios o disponibilidad de servicios.',
  },
  {
    title: 'Recurso humano limitado',
    desc: 'El personal de recepción y orientación tiene capacidad restringida, especialmente en horas piso o en eventos masivos.',
  },
  {
    title: 'Sin canal conversacional',
    desc: 'No existe un medio natural (voz, lenguaje cotidiano) para solicitar indicaciones, hacer preguntas de contexto o recibir asistencia paso a paso.',
  },
]

export default function ObjetivoSlide() {
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
        El Problema
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '0.9rem',
          marginBottom: 40,
          fontWeight: 300,
        }}
      >
        ¿Cómo ayudar a una persona a encontrar su destino en un campus universitario
        sin depender de mapas físicos o personal de recepción?
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {problems.map((p, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + i * 0.1 }}
            style={{
              padding: '20px 24px',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 12,
              borderLeft: '3px solid var(--blue)',
            }}
          >
            <h4 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: 8, color: 'var(--blue)' }}>
              {p.title}
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.6 }}>
              {p.desc}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
