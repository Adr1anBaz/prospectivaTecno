import { motion } from 'framer-motion'

const ChallengesSlide = () => {
  const challenges = [
    {
      title: '🗺️ Navegación Autónoma',
      status: '⚠️',
      description: 'El robot se desvía durante la navegación',
      details: [
        'Robot va chueco al seguir rutas',
        'Da vueltas innecesarias',
        'Pierde precisión en trayectorias largas',
      ],
      solutions: [
        'Remapear con mejor calidad',
        'Implementar corrección de posición en tiempo real',
        'Ajustar parámetros de Nav2',
        'Calibrar odometría del robot',
      ],
    },
    {
      title: '🎤 Latencia del Pipeline de Voz',
      status: '🟡',
      description: 'Procesamiento toma 6-15 segundos',
      details: [
        'Whisper: 2-3s de transcripción',
        'Ollama: 1-2s de generación',
        'Ejecución: 2-3s',
      ],
      solutions: [
        'Usar modelo Whisper tiny (más rápido)',
        'Optimizar prompt del LLM',
        'Pipeline asíncrono para múltiples comandos',
      ],
    },
  ]

  return (
    <div className="slide">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        🚧 Desafíos y Soluciones Propuestas
      </motion.h2>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '30px', marginTop: '30px' }}>
        {challenges.map((challenge, index) => (
          <motion.div
            key={challenge.title}
            initial={{ x: index % 2 === 0 ? -100 : 100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.2 + index * 0.3, duration: 0.5 }}
          >
            <div className="card" style={{ background: 'rgba(255, 100, 100, 0.1)', border: '2px solid rgba(255, 100, 100, 0.5)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
                <span style={{ fontSize: '2.5rem' }}>{challenge.status}</span>
                <div>
                  <h3 style={{ margin: 0, color: '#ff6b6b' }}>{challenge.title}</h3>
                  <p style={{ margin: '5px 0 0 0', fontSize: '1rem', opacity: 0.9 }}>
                    {challenge.description}
                  </p>
                </div>
              </div>

              <div className="grid-2" style={{ gap: '25px' }}>
                <div>
                  <h4 style={{ color: 'var(--accent)', marginBottom: '12px' }}>📋 Detalles del Problema</h4>
                  <ul style={{ fontSize: '0.95rem', lineHeight: '1.8' }}>
                    {challenge.details.map((detail) => (
                      <li key={detail}>{detail}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 style={{ color: 'var(--primary)', marginBottom: '12px' }}>✅ Soluciones Propuestas</h4>
                  <ul style={{ fontSize: '0.95rem', lineHeight: '1.8' }}>
                    {challenge.solutions.map((solution) => (
                      <li key={solution}>{solution}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <motion.div
        className="grid-2"
        style={{ marginTop: '30px', gap: '20px' }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9 }}
      >
        <div className="card" style={{ background: 'rgba(0, 255, 136, 0.1)' }}>
          <h4 style={{ color: 'var(--accent)', marginBottom: '12px' }}>✅ Logros Exitosos</h4>
          <ul style={{ fontSize: '0.95rem', lineHeight: '1.7' }}>
            <li>Control por voz 100% local funcionando</li>
            <li>Sistema de telemetría completo</li>
            <li>Guardrails de seguridad robustos</li>
            <li>Mapeo SLAM exitoso</li>
            <li>Integración ROS2 funcional</li>
          </ul>
        </div>

        <div className="card" style={{ background: 'rgba(0, 212, 255, 0.1)' }}>
          <h4 style={{ color: 'var(--primary)', marginBottom: '12px' }}>🔬 En Investigación</h4>
          <ul style={{ fontSize: '0.95rem', lineHeight: '1.7' }}>
            <li>Fusión sensorial (IMU + LiDAR + Visual)</li>
            <li>Algoritmos de corrección de deriva</li>
            <li>Optimización de parámetros Nav2</li>
            <li>Control predictivo de trayectoria</li>
          </ul>
        </div>
      </motion.div>

      <motion.div
        style={{
          marginTop: '30px',
          textAlign: 'center',
          padding: '20px',
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '15px',
        }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2 }}
      >
        <p style={{ fontSize: '1.1rem', fontStyle: 'italic' }}>
          "La mayoría de funcionalidades están operativas. El foco actual es mejorar la precisión de navegación autónoma."
        </p>
      </motion.div>
    </div>
  )
}

export default ChallengesSlide
