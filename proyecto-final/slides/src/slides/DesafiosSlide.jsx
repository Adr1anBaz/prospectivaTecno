import { motion } from 'framer-motion'

export default function DesafiosSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1000 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 48,
        }}
      >
        Desafíos
      </motion.h2>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
        {/* Bottleneck 1 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          style={{
            padding: 32,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 16,
          }}
        >
          <span style={{
            display: 'inline-block',
            fontSize: '0.7rem',
            textTransform: 'uppercase',
            letterSpacing: '0.1em',
            color: 'var(--blue)',
            marginBottom: 16,
            fontWeight: 600,
          }}>
            Local vs Nube
          </span>
          <h3 style={{ fontSize: '1.2rem', marginBottom: 16, fontWeight: 500 }}>
            Raspberry Pi 5
          </h3>
          <ul style={{
            listStyle: 'none',
            padding: 0,
            display: 'flex',
            flexDirection: 'column',
            gap: 10,
          }}>
            <li style={{ color: 'var(--text-dim)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Error al cargar SO desde SD card
            </li>
            <li style={{ color: 'var(--text-dim)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              No se pueden probar modelos localmente en dispositivo portable
            </li>
            <li style={{ color: 'var(--text-muted)', fontSize: '0.85rem', lineHeight: 1.6 }}>
              Impacto potencial a futuro si se requiere procesamiento local
            </li>
          </ul>
        </motion.div>

        {/* Bottleneck 2 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35 }}
          style={{
            padding: 32,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 16,
          }}
        >
          <span style={{
            display: 'inline-block',
            fontSize: '0.7rem',
            textTransform: 'uppercase',
            letterSpacing: '0.1em',
            color: 'var(--blue)',
            marginBottom: 16,
            fontWeight: 600,
          }}>
            Conectividad
          </span>
          <h3 style={{ fontSize: '1.2rem', marginBottom: 16, fontWeight: 500 }}>
            WiFi del Robot
          </h3>
          <ul style={{
            listStyle: 'none',
            padding: 0,
            display: 'flex',
            flexDirection: 'column',
            gap: 10,
          }}>
            <li style={{ color: 'var(--text-dim)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Se requiere conexión al access point del robot
            </li>
            <li style={{ color: 'var(--text-dim)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              No se logró conectar a red de la escuela ni red generada
            </li>
            <li style={{ color: 'var(--text-muted)', fontSize: '0.85rem', lineHeight: 1.6 }}>
              Problemas para peticiones a internet si servidores no están en la red del robot
            </li>
          </ul>
        </motion.div>
      </div>
    </div>
  )
}
