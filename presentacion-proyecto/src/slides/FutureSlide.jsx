import { motion } from 'framer-motion'

const FutureSlide = () => {
  const roadmap = [
    {
      phase: 'CORTO PLAZO',
      icon: '▸',
      color: 'var(--primary)',
      items: [
        'Solucionar deriva en navegación',
        'Optimizar corrección de posición RT',
        'Mejorar calidad de mapeo SLAM',
        'Reducir latencia pipeline de voz'
      ],
    },
    {
      phase: 'MEDIANO PLAZO',
      icon: '▸▸',
      color: 'var(--accent)',
      items: [
        'Fusión sensorial (IMU + LiDAR + Visual)',
        'Dashboard web para telemetría',
        'Sistema de logging y análisis',
        'Integración de cámara para detección'
      ],
    },
    {
      phase: 'LARGO PLAZO',
      icon: '▸▸▸',
      color: 'var(--secondary)',
      items: [
        'Navegación colaborativa multi-robot',
        'Aprendizaje por refuerzo',
        'Reconocimiento de objetos con IA',
        'Autonomía completa en entornos complejos'
      ],
    },
  ]

  return (
    <div className="slide">
      <motion.h2
        initial={{ opacity: 0, scale: 0.9, filter: 'blur(10px)' }}
        animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
        transition={{ duration: 0.5 }}
        style={{ textAlign: 'center', marginBottom: '25px' }}
      >
        PRÓXIMOS PASOS
      </motion.h2>

      <div className="grid-2" style={{ gap: '15px' }}>
        {/* Left column - Roadmap */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {roadmap.map((phase, index) => (
            <motion.div
              key={phase.phase}
              className="card"
              style={{
                background: 'var(--steel)',
                border: `2px solid ${phase.color}`,
                borderLeftWidth: '4px',
                padding: '15px'
              }}
              initial={{ x: -50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.2 + index * 0.15, duration: 0.5 }}
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                marginBottom: '10px'
              }}>
                <span style={{
                  fontSize: '1.2rem',
                  color: phase.color,
                  fontFamily: 'IBM Plex Mono',
                  fontWeight: '700'
                }}>
                  {phase.icon}
                </span>
                <h3 style={{
                  margin: 0,
                  color: phase.color,
                  fontSize: '1.1rem',
                  fontFamily: 'IBM Plex Mono',
                  letterSpacing: '1px'
                }}>
                  {phase.phase}
                </h3>
              </div>
              <ul style={{ fontSize: '0.85rem', lineHeight: '1.5', margin: 0 }}>
                {phase.items.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Right column - Research areas */}
        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <div className="card" style={{ marginBottom: '12px' }}>
            <h3 style={{
              textAlign: 'center',
              marginBottom: '15px',
              color: 'var(--primary)',
              fontSize: '1.1rem',
              fontFamily: 'IBM Plex Mono',
              letterSpacing: '1px'
            }}>
              ÁREAS DE INVESTIGACIÓN
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {[
                { title: 'NAVEGACIÓN', icon: '🧭', color: 'var(--primary)', desc: 'Corrección de deriva, fusión sensorial' },
                { title: 'IA LOCAL', icon: '🤖', color: 'var(--accent)', desc: 'Optimización, fine-tuning, razonamiento' },
                { title: 'VISIÓN', icon: '👁️', color: 'var(--secondary)', desc: 'Detección objetos, control por gestos' },
                { title: 'COLABORACIÓN', icon: '🌐', color: 'var(--accent)', desc: 'Multi-robot, mapeo colaborativo' }
              ].map((area, i) => (
                <div
                  key={i}
                  style={{
                    padding: '12px',
                    background: 'rgba(0, 0, 0, 0.4)',
                    border: `2px solid ${area.color}`,
                    clipPath: 'polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px)'
                  }}
                >
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    marginBottom: '6px'
                  }}>
                    <span style={{ fontSize: '1rem' }}>{area.icon}</span>
                    <h4 style={{
                      color: area.color,
                      margin: 0,
                      fontSize: '0.9rem',
                      fontFamily: 'IBM Plex Mono',
                      letterSpacing: '1px'
                    }}>
                      {area.title}
                    </h4>
                  </div>
                  <p style={{
                    fontSize: '0.8rem',
                    lineHeight: '1.4',
                    opacity: 0.8,
                    margin: 0
                  }}>
                    {area.desc}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Final summary card */}
          <motion.div
            className="card"
            style={{
              background: 'rgba(255, 85, 0, 0.05)',
              border: '2px solid var(--primary)',
              textAlign: 'center',
              padding: '15px'
            }}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.8 }}
          >
            <motion.h3
              style={{
                marginBottom: '10px',
                fontSize: '1.3rem',
                color: 'var(--primary)',
                fontFamily: 'IBM Plex Mono',
                letterSpacing: '1px'
              }}
              animate={{ opacity: [1, 0.7, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              UNITREE GO2 + IA LOCAL
            </motion.h3>
            <p style={{
              fontSize: '0.85rem',
              lineHeight: '1.5',
              marginBottom: '12px'
            }}>
              <strong>Control Inteligente</strong> • <strong>Navegación Autónoma</strong> • <strong>100% Local</strong>
            </p>
            <div style={{
              display: 'flex',
              gap: '8px',
              justifyContent: 'center',
              flexWrap: 'wrap'
            }}>
              {['Control Voz', 'Telemetría', 'SLAM+Nav2', 'Validado'].map((item, i) => (
                <span
                  key={i}
                  className="badge"
                  style={{ fontSize: '0.75rem', padding: '6px 12px' }}
                >
                  {item}
                </span>
              ))}
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}

export default FutureSlide
