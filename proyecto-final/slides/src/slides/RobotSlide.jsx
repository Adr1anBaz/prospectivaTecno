import { motion } from 'framer-motion'

export default function RobotSlide() {
  return (
    <div style={{
      padding: '0 80px',
      maxWidth: 1100,
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 60,
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
          fontSize: '2.8rem',
          fontWeight: 400,
          marginBottom: 12,
        }}>
          El Robot
        </h2>
        <p style={{
          color: 'var(--blue)',
          fontSize: '1rem',
          marginBottom: 36,
          fontWeight: 500,
        }}>
          Unitree Go2 Pro
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div>
            <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 8 }}>
              Por qué este robot
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem', lineHeight: 1.6 }}>
              Atrae al público — lo graban, preguntan, se acercan
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 8 }}>
              Control
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem', lineHeight: 1.6 }}>
              Vía Python usando la biblioteca WebRTC del robot
              <br />
              <span style={{ color: 'var(--text-muted)' }}>No open-source, pero controlable programáticamente</span>
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 8 }}>
              Navegación
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem', lineHeight: 1.6 }}>
              ROS2/SLAM no viable en el tiempo disponible
              <br />
              <span style={{ color: 'var(--blue)' }}>Solución → rutas pregrabadas modulares</span>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
