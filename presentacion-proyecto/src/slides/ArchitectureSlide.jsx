import { motion } from 'framer-motion'

const ArchitectureSlide = () => {
  const techStack = [
    {
      title: 'AUDIO & IA',
      color: 'var(--primary)',
      items: [
        { name: 'Whisper (base)', desc: 'Transcripción ~1GB' },
        { name: 'Ollama (Qwen2.5:3b)', desc: 'LLM local ~1.9GB' },
        { name: 'SoundDevice', desc: 'Captura de audio' },
        { name: 'PyTorch', desc: 'Inferencia de modelos' }
      ]
    },
    {
      title: 'COMUNICACIÓN',
      color: 'var(--accent)',
      items: [
        { name: 'WebRTC', desc: 'Conexión en tiempo real' },
        { name: 'unitree-webrtc-connect', desc: 'SDK oficial' },
        { name: 'LocalAP', desc: 'Red 192.168.12.x' }
      ]
    },
    {
      title: 'NAVEGACIÓN',
      color: 'var(--secondary)',
      items: [
        { name: 'ROS2', desc: 'Framework robótico' },
        { name: 'SLAM Toolbox', desc: 'Mapeo y localización' },
        { name: 'Nav2', desc: 'Navegación autónoma' },
        { name: 'RViz2', desc: 'Visualización' }
      ]
    }
  ]

  return (
    <div className="slide">
      <motion.h2
        initial={{ opacity: 0, y: -20, filter: 'blur(10px)' }}
        animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
        transition={{ duration: 0.6 }}
      >
        ARQUITECTURA DEL SISTEMA
      </motion.h2>

      <div className="grid-2" style={{ gap: '25px' }}>
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h3>STACK TECNOLÓGICO</h3>

          {techStack.map((stack, index) => (
            <motion.div
              key={stack.title}
              className="card"
              style={{
                marginTop: index === 0 ? '20px' : '15px',
                borderLeftColor: stack.color,
                borderLeftWidth: '4px'
              }}
              initial={{ x: -30, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.3 + index * 0.15 }}
            >
              <h4 style={{
                color: stack.color,
                marginBottom: '15px',
                fontFamily: 'IBM Plex Mono',
                fontSize: '0.95rem',
                letterSpacing: '1px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span style={{ fontSize: '1.2rem' }}>▸</span>
                {stack.title}
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {stack.items.map((item, i) => (
                  <div
                    key={i}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '8px 0',
                      borderBottom: i < stack.items.length - 1 ? '1px solid var(--border)' : 'none'
                    }}
                  >
                    <span style={{
                      fontFamily: 'IBM Plex Mono',
                      fontWeight: '600',
                      fontSize: '0.9rem',
                      color: '#e0e0e0'
                    }}>
                      {item.name}
                    </span>
                    <span style={{
                      fontFamily: 'Space Mono',
                      fontSize: '0.75rem',
                      opacity: 0.6,
                      color: stack.color
                    }}>
                      {item.desc}
                    </span>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h3>FLUJO DE DATOS</h3>

          <div style={{
            background: 'rgba(0, 0, 0, 0.5)',
            padding: '25px',
            marginTop: '20px',
            border: '2px solid var(--border)',
            clipPath: 'polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px)',
            position: 'relative'
          }}>
            <motion.div
              style={{
                background: 'var(--steel)',
                border: '2px solid var(--primary)',
                padding: '18px',
                marginBottom: '12px',
                clipPath: 'polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px)',
              }}
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              <div style={{
                fontFamily: 'IBM Plex Mono',
                fontWeight: '700',
                color: 'var(--primary)',
                fontSize: '0.95rem',
                letterSpacing: '1px'
              }}>
                [01] USUARIO
              </div>
              <p style={{
                fontSize: '0.85rem',
                marginTop: '8px',
                opacity: 0.7,
                fontFamily: 'Space Mono'
              }}>
                Comando de voz capturado
              </p>
            </motion.div>

            <div style={{
              textAlign: 'center',
              fontSize: '1.5rem',
              margin: '8px 0',
              color: 'var(--secondary)',
              fontWeight: '700'
            }}>
              ↓
            </div>

            <motion.div
              style={{
                background: 'var(--steel)',
                border: '2px solid var(--accent)',
                padding: '18px',
                marginBottom: '12px',
                clipPath: 'polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px)',
              }}
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              <div style={{
                fontFamily: 'IBM Plex Mono',
                fontWeight: '700',
                color: 'var(--accent)',
                fontSize: '0.95rem',
                letterSpacing: '1px'
              }}>
                [02] PROCESAMIENTO LOCAL
              </div>
              <p style={{
                fontSize: '0.85rem',
                marginTop: '8px',
                opacity: 0.7,
                fontFamily: 'Space Mono'
              }}>
                Whisper → Ollama → Validación
              </p>
            </motion.div>

            <div style={{
              textAlign: 'center',
              fontSize: '1.5rem',
              margin: '8px 0',
              color: 'var(--secondary)',
              fontWeight: '700'
            }}>
              ↓
            </div>

            <motion.div
              style={{
                background: 'var(--steel)',
                border: '2px solid var(--secondary)',
                padding: '18px',
                clipPath: 'polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px)',
              }}
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 1 }}
            >
              <div style={{
                fontFamily: 'IBM Plex Mono',
                fontWeight: '700',
                color: 'var(--secondary)',
                fontSize: '0.95rem',
                letterSpacing: '1px'
              }}>
                [03] ROBOT UNITREE GO2
              </div>
              <p style={{
                fontSize: '0.85rem',
                marginTop: '8px',
                opacity: 0.7,
                fontFamily: 'Space Mono'
              }}>
                Ejecución del comando vía WebRTC
              </p>
            </motion.div>
          </div>

          <motion.div
            className="card"
            style={{
              marginTop: '20px',
              background: 'rgba(255, 85, 0, 0.05)',
              borderColor: '#ff3333',
              borderWidth: '2px'
            }}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 1.2 }}
          >
            <h4 style={{
              color: '#ff6666',
              fontFamily: 'IBM Plex Mono',
              letterSpacing: '1px',
              fontSize: '0.95rem',
              marginBottom: '12px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <span style={{ fontSize: '1.2rem' }}>🛡️</span>
              SISTEMA DE GUARDRAILS
            </h4>
            <ul style={{ fontSize: '0.85rem', marginTop: '10px', opacity: 0.85 }}>
              <li>Validación de rangos de movimiento</li>
              <li>Whitelist de acciones permitidas</li>
              <li>Prevención de comandos peligrosos</li>
              <li>Bloqueo durante ejecución</li>
            </ul>
          </motion.div>
        </motion.div>
      </div>

      <motion.div
        style={{
          marginTop: '30px',
          textAlign: 'center',
          padding: '18px 30px',
          background: 'var(--steel)',
          border: '2px solid var(--accent)',
          clipPath: 'polygon(12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%, 0 12px)',
        }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.4 }}
      >
        <p style={{
          fontSize: '1rem',
          fontFamily: 'IBM Plex Mono',
          color: 'var(--accent)'
        }}>
          <span style={{ color: 'var(--primary)' }}>⏱️</span>{' '}
          <strong>LATENCIA:</strong> 6-15 seg/comando
          <span style={{ opacity: 0.6, marginLeft: '15px' }}>[Procesamiento + Ejecución]</span>
        </p>
      </motion.div>
    </div>
  )
}

export default ArchitectureSlide
