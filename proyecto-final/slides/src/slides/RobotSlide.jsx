import { motion } from 'framer-motion'

export default function RobotSlide() {
  return (
    <div style={{
      padding: '0 80px',
      maxWidth: 1100,
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 48,
      alignItems: 'center',
    }}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        style={{
          borderRadius: 16,
          overflow: 'hidden',
          border: '1px solid var(--border)',
          background: 'var(--surface)',
        }}
      >
        <img
          src={`${import.meta.env.BASE_URL}images/22.webp`}
          alt="Unitree Go2 Air"
          style={{
            width: '100%',
            height: 'auto',
            display: 'block',
            objectFit: 'cover',
          }}
        />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
      >
        <h2 style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: '2.4rem',
          fontWeight: 400,
          marginBottom: 8,
        }}>
          Plataforma Robótica
        </h2>
        <p style={{
          color: 'var(--blue)',
          fontSize: '0.9rem',
          marginBottom: 28,
          fontWeight: 500,
        }}>
          Robot cuadrúpedo como guía físico
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div style={{
            padding: 14,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            borderLeft: '3px solid var(--blue)',
          }}>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--blue)', marginBottom: 4 }}>
              ¿Por qué un robot?
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              Un agente físico genera confianza, atrae atención y puede guiar activamente
              a una persona, no solo indicar una ruta en un mapa.
            </p>
          </div>

          <div style={{
            padding: 14,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            borderLeft: '3px solid #E6A85B',
          }}>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#E6A85B', marginBottom: 4 }}>
              Control Propuesto
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              Comunicación vía WebRTC para comandos en tiempo real.
              ROS2 como middleware para orquestación de movimientos y sensores.
            </p>
          </div>

          <div style={{
            padding: 14,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            borderLeft: '3px solid #6BCB8A',
          }}>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#6BCB8A', marginBottom: 4 }}>
              Capacidades Deseadas
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              Desplazamiento autónomo entre puntos del campus, ejecución de rutas
              pregrabadas, y comandos de presencia (sentarse, saludar, guiar).
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
