import { motion } from 'framer-motion'

const FutureSlide = () => {
  const roadmap = [
    {
      phase: 'Corto Plazo',
      icon: '🎯',
      color: 'var(--primary)',
      items: [
        'Solucionar problema de deriva en navegación',
        'Optimizar corrección de posición en tiempo real',
        'Mejorar calidad de mapeo SLAM',
        'Reducir latencia del pipeline de voz',
        'Calibración fina de parámetros Nav2',
      ],
    },
    {
      phase: 'Mediano Plazo',
      icon: '🚀',
      color: 'var(--accent)',
      items: [
        'Fusión sensorial (IMU + LiDAR + Visual)',
        'Dashboard web para telemetría (React + WebSockets)',
        'Sistema de logging y análisis de datos',
        'Integración de cámara para detección visual',
        'Control por gestos usando cámara',
      ],
    },
    {
      phase: 'Largo Plazo',
      icon: '🌟',
      color: 'var(--secondary)',
      items: [
        'Navegación colaborativa multi-robot',
        'Aprendizaje por refuerzo para optimizar trayectorias',
        'Reconocimiento de objetos con IA',
        'Interacción natural conversacional (diálogo)',
        'Autonomía completa en entornos complejos',
      ],
    },
  ]

  return (
    <div className="slide">
      <motion.h2
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        style={{ textAlign: 'center', marginBottom: '40px' }}
      >
        🔮 Próximos Pasos y Visión Futura
      </motion.h2>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
        {roadmap.map((phase, index) => (
          <motion.div
            key={phase.phase}
            className="card"
            style={{
              background: `linear-gradient(135deg, ${phase.color}15, rgba(0, 0, 0, 0.3))`,
              border: `2px solid ${phase.color}`,
            }}
            initial={{ x: index % 2 === 0 ? -100 : 100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.2 + index * 0.2, duration: 0.6 }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
              <span style={{ fontSize: '2.5rem' }}>{phase.icon}</span>
              <h3 style={{ margin: 0, color: phase.color }}>{phase.phase}</h3>
            </div>
            <ul style={{ fontSize: '1rem', lineHeight: '1.9' }}>
              {phase.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </motion.div>
        ))}
      </div>

      <motion.div
        style={{ marginTop: '40px' }}
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
      >
        <div className="card" style={{ background: 'rgba(255, 255, 255, 0.05)' }}>
          <h3 style={{ textAlign: 'center', marginBottom: '25px', color: 'var(--primary)' }}>
            🎓 Áreas de Investigación Activa
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
            <div style={{ padding: '20px', background: 'rgba(0, 212, 255, 0.1)', borderRadius: '12px' }}>
              <h4 style={{ color: 'var(--primary)', marginBottom: '12px' }}>🧭 Navegación</h4>
              <p style={{ fontSize: '0.9rem', lineHeight: '1.7', opacity: 0.9 }}>
                Algoritmos avanzados de corrección de deriva, control predictivo de trayectorias,
                y fusión sensorial para mejorar precisión.
              </p>
            </div>
            <div style={{ padding: '20px', background: 'rgba(0, 255, 136, 0.1)', borderRadius: '12px' }}>
              <h4 style={{ color: 'var(--accent)', marginBottom: '12px' }}>🤖 IA Local</h4>
              <p style={{ fontSize: '0.9rem', lineHeight: '1.7', opacity: 0.9 }}>
                Optimización de modelos para reducir latencia, fine-tuning para comandos específicos,
                y razonamiento contextual.
              </p>
            </div>
            <div style={{ padding: '20px', background: 'rgba(255, 0, 234, 0.1)', borderRadius: '12px' }}>
              <h4 style={{ color: 'var(--secondary)', marginBottom: '12px' }}>👁️ Visión</h4>
              <p style={{ fontSize: '0.9rem', lineHeight: '1.7', opacity: 0.9 }}>
                Detección de objetos, reconocimiento facial, seguimiento de personas,
                y control por gestos usando cámaras.
              </p>
            </div>
            <div style={{ padding: '20px', background: 'rgba(255, 200, 0, 0.1)', borderRadius: '12px' }}>
              <h4 style={{ color: '#ffc107', marginBottom: '12px' }}>🌐 Colaboración</h4>
              <p style={{ fontSize: '0.9rem', lineHeight: '1.7', opacity: 0.9 }}>
                Comunicación multi-robot, coordinación de tareas,
                y mapeo colaborativo en tiempo real.
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      <motion.div
        style={{
          marginTop: '35px',
          textAlign: 'center',
          padding: '30px',
          background: 'linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(255, 0, 234, 0.2))',
          borderRadius: '20px',
          border: '2px solid rgba(255, 255, 255, 0.2)',
        }}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 1.2 }}
      >
        <motion.h2
          style={{ marginBottom: '15px', fontSize: '2.5rem' }}
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          🤖 Unitree Go2 + IA Local
        </motion.h2>
        <p style={{ fontSize: '1.3rem', lineHeight: '1.8' }}>
          <strong>Control Inteligente</strong> | <strong>Navegación Autónoma</strong> | <strong>100% Local</strong>
        </p>
        <div style={{ marginTop: '25px', display: 'flex', gap: '15px', justifyContent: 'center', flexWrap: 'wrap' }}>
          <span className="badge" style={{ fontSize: '1rem' }}>🎤 Control por Voz</span>
          <span className="badge" style={{ fontSize: '1rem' }}>📡 Telemetría Completa</span>
          <span className="badge" style={{ fontSize: '1rem' }}>🗺️ SLAM + Nav2</span>
          <span className="badge" style={{ fontSize: '1rem' }}>🛡️ Seguro & Validado</span>
        </div>
        <p style={{ marginTop: '30px', fontSize: '1.1rem', opacity: 0.8, fontStyle: 'italic' }}>
          Un sistema robótico completo con procesamiento local de IA<br />
          y capacidades de navegación autónoma
        </p>
      </motion.div>
    </div>
  )
}

export default FutureSlide
