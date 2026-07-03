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
      {/* Image */}
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

      {/* Info */}
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
          Control Robótico
        </h2>
        <p style={{
          color: 'var(--blue)',
          fontSize: '0.9rem',
          marginBottom: 32,
          fontWeight: 500,
        }}>
          Unitree Go2 Air — 3 nodos ROS2 + WebRTC
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {/* Controller */}
          <div style={{
            padding: 14,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            borderLeft: '3px solid var(--blue)',
          }}>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--blue)', marginBottom: 4 }}>
              Controller Node
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              WebRTC activo, reenvío de comandos, publicación de telemetría (odometría + IMU)
            </p>
          </div>

          {/* Actions */}
          <div style={{
            padding: 14,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            borderLeft: '3px solid #E6A85B',
          }}>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#E6A85B', marginBottom: 4 }}>
              Actions Node
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              Rutinas discretas preprogramadas: sentarse, pararse, detenerse, saludo, baile
            </p>
          </div>

          {/* Navigation */}
          <div style={{
            padding: 14,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            borderLeft: '3px solid #6BCB8A',
          }}>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#6BCB8A', marginBottom: 4 }}>
              Navigation Node
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-dim)', lineHeight: 1.5 }}>
              Secuencias espaciales → velocidades lineales/angulares. Ejecución temporal si no hay odometría.
            </p>
          </div>

          {/* Shared files */}
          <div style={{
            padding: 10,
            background: 'var(--bg)',
            border: '1px dashed var(--border)',
            borderRadius: 6,
            fontSize: '0.78rem',
            color: 'var(--text-muted)',
            textAlign: 'center',
          }}>
            JSON compartido: agente escribe → ROS2 lee → feedback de vuelta
          </div>
        </div>
      </motion.div>
    </div>
  )
}
