import { motion } from 'framer-motion'

const DemoSlide = () => {
  const demoCategories = [
    {
      title: 'CONTROL POR VOZ',
      icon: '🎤',
      color: 'var(--primary)',
      desc: 'Demostración de comandos de movimiento y gestos'
    },
    {
      title: 'MAPEO SLAM',
      icon: '🗺️',
      color: 'var(--secondary)',
      desc: 'Proceso de generación de mapa en RViz2'
    },
    {
      title: 'NAVEGACIÓN',
      icon: '🧭',
      color: 'var(--accent)',
      desc: 'Robot navegando hacia goal points'
    }
  ]

  return (
    <div className="slide">
      <motion.h2
        initial={{ opacity: 0, scale: 0.9, filter: 'blur(10px)' }}
        animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
        transition={{ duration: 0.6 }}
        style={{ textAlign: 'center', marginBottom: '40px' }}
      >
        DEMOS Y CASOS DE USO
      </motion.h2>

      <div className="grid-2" style={{ gap: '25px' }}>
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h3>DEMO: CONTROL POR VOZ</h3>

          <div className="card" style={{
            background: 'rgba(255, 85, 0, 0.05)',
            marginTop: '20px',
            borderLeft: '4px solid var(--primary)'
          }}>
            <h4 style={{
              color: 'var(--primary)',
              marginBottom: '15px',
              fontFamily: 'IBM Plex Mono',
              fontSize: '0.95rem',
              letterSpacing: '1px'
            }}>
              EJEMPLO DE INTERACCIÓN
            </h4>
            <div className="code-block" style={{ fontSize: '0.85rem', lineHeight: '1.6' }}>
              <div style={{ color: 'var(--secondary)' }}>$ uv run python robot_voice_controller.py</div>
              <div style={{ marginTop: '8px', opacity: 0.6 }}>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
              <div style={{ color: 'var(--secondary)' }}>✅ Conexión establecida</div>
              <div style={{ color: 'var(--secondary)' }}>✅ Modelos cargados</div>
              <div style={{ marginTop: '8px' }}>⏺️  🔴 GRABANDO...</div>
              <div style={{ marginTop: '8px', color: '#999' }}>[Usuario]: "Camina hacia adelante"</div>
              <div style={{ marginTop: '8px', opacity: 0.8 }}>📝 Transcribiendo...</div>
              <div style={{ opacity: 0.8 }}>💬 Comando: "camina hacia adelante"</div>
              <div style={{ opacity: 0.8 }}>🤖 Generando comando...</div>
              <div style={{ opacity: 0.8 }}>🛡️  Validando seguridad...</div>
              <div style={{ marginTop: '8px', color: 'var(--secondary)' }}>
                🤖 EJECUTANDO: move_robot
              </div>
              <div style={{ opacity: 0.7 }}>📊 Parámetros: {`{"x": 0.3, "y": 0, "z": 0}`}</div>
              <div style={{ marginTop: '8px', color: 'var(--secondary)' }}>✅ Comando completado</div>
              <div style={{ marginTop: '8px', opacity: 0.6 }}>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
            </div>
          </div>

          <div className="card" style={{ marginTop: '15px' }}>
            <h4 style={{
              color: 'var(--accent)',
              fontFamily: 'IBM Plex Mono',
              fontSize: '0.95rem',
              letterSpacing: '1px',
              marginBottom: '12px'
            }}>
              COMANDOS DE PRUEBA
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.9rem' }}>
              {[
                { cmd: 'Saluda', action: 'Animación de saludo' },
                { cmd: 'Gira a la derecha', action: 'Rotación en eje Z' },
                { cmd: 'Siéntate', action: 'Cambio de postura' },
                { cmd: 'Modo normal', action: 'Cambio de modo locomotion' }
              ].map((item, i) => (
                <div
                  key={i}
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '8px 0',
                    borderBottom: i < 3 ? '1px solid var(--border)' : 'none'
                  }}
                >
                  <span style={{ fontFamily: 'Space Mono', color: 'var(--primary)' }}>
                    "{item.cmd}"
                  </span>
                  <span style={{ fontSize: '0.8rem', opacity: 0.6 }}>
                    → {item.action}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h3>DEMO: NAVEGACIÓN AUTÓNOMA</h3>

          <div className="card" style={{
            background: 'rgba(180, 255, 0, 0.05)',
            marginTop: '20px',
            borderLeft: '4px solid var(--secondary)'
          }}>
            <h4 style={{
              color: 'var(--secondary)',
              marginBottom: '15px',
              fontFamily: 'IBM Plex Mono',
              fontSize: '0.95rem',
              letterSpacing: '1px'
            }}>
              FLUJO DE NAVEGACIÓN
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {[
                { num: '01', text: 'Ejecutar script de mapeo', icon: '▸' },
                { num: '02', text: 'Robot genera mapa en RViz2', icon: '▸' },
                { num: '03', text: 'Guardar mapa (.pgm + .yaml)', icon: '▸' },
                { num: '04', text: 'Ejecutar script de navegación', icon: '▸' },
                { num: '05', text: 'Establecer goal point', icon: '▸' },
                { num: '06', text: 'Robot navega autónomamente', icon: '✓' }
              ].map((step, i) => (
                <motion.div
                  key={i}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '10px',
                    background: i === 5 ? 'rgba(180, 255, 0, 0.1)' : 'rgba(0, 0, 0, 0.3)',
                    border: i === 5 ? '1px solid var(--secondary)' : '1px solid var(--border)',
                    clipPath: 'polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px)'
                  }}
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.6 + i * 0.1 }}
                >
                  <span style={{
                    fontFamily: 'IBM Plex Mono',
                    fontWeight: '700',
                    color: i === 5 ? 'var(--secondary)' : 'var(--primary)',
                    fontSize: '0.95rem',
                    minWidth: '30px'
                  }}>
                    {step.num}
                  </span>
                  <span style={{
                    fontSize: '1rem',
                    color: i === 5 ? 'var(--secondary)' : 'var(--primary)',
                    marginRight: '8px'
                  }}>
                    {step.icon}
                  </span>
                  <span style={{ fontSize: '0.9rem', fontFamily: 'Space Mono' }}>
                    {step.text}
                  </span>
                </motion.div>
              ))}
            </div>
          </div>

          <div className="card" style={{ marginTop: '15px' }}>
            <h4 style={{
              color: 'var(--primary)',
              fontFamily: 'IBM Plex Mono',
              fontSize: '0.95rem',
              letterSpacing: '1px',
              marginBottom: '10px'
            }}>
              DEMO: TELEMETRÍA RT
            </h4>
            <div className="code-block" style={{ fontSize: '0.8rem', lineHeight: '1.6' }}>
              <div style={{ color: 'var(--secondary)' }}>$ uv run python telemetry_demo.py</div>
              <div style={{ marginTop: '8px', opacity: 0.6 }}>
                📡 Dashboard en Tiempo Real
              </div>
              <div style={{ opacity: 0.5, marginTop: '5px' }}>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
              <div>🧭 IMU: Roll=0.5° Pitch=1.2° Yaw=45°</div>
              <div>📍 Pos: X=1.2m Y=0.3m Z=0.2m</div>
              <div>🔋 Batería: 85% | 24.5V | 2.3A</div>
              <div>🦿 Patas: FL=15N FR=16N RL=14N RR=15N</div>
              <div>⚙️  Modo: Walk (4) | Marcha: Trot</div>
              <div style={{ opacity: 0.5, marginTop: '5px' }}>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
            </div>
          </div>
        </motion.div>
      </div>

      <motion.div
        style={{ marginTop: '35px' }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
      >
        <div className="card" style={{
          background: 'var(--steel)',
          borderWidth: '2px'
        }}>
          <h3 style={{
            color: 'var(--primary)',
            marginBottom: '25px',
            textAlign: 'center',
            fontFamily: 'IBM Plex Mono',
            fontSize: '1.2rem',
            letterSpacing: '2px'
          }}>
            VIDEOS DE DEMO DISPONIBLES
          </h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '15px'
          }}>
            {demoCategories.map((cat, i) => (
              <motion.div
                key={i}
                style={{
                  textAlign: 'center',
                  padding: '20px',
                  background: 'rgba(0, 0, 0, 0.4)',
                  border: `2px solid ${cat.color}`,
                  clipPath: 'polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px)',
                  transition: 'all 0.3s'
                }}
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 1 + i * 0.15 }}
                whileHover={{
                  scale: 1.05,
                  boxShadow: `0 0 25px ${cat.color}40`
                }}
              >
                <div style={{ fontSize: '2.5rem', marginBottom: '12px' }}>{cat.icon}</div>
                <div style={{
                  fontFamily: 'IBM Plex Mono',
                  fontWeight: '700',
                  fontSize: '0.9rem',
                  color: cat.color,
                  letterSpacing: '1px',
                  marginBottom: '8px'
                }}>
                  {cat.title}
                </div>
                <p style={{
                  fontSize: '0.8rem',
                  opacity: 0.7,
                  fontFamily: 'Space Mono',
                  lineHeight: '1.5'
                }}>
                  {cat.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>

      <motion.div
        style={{
          marginTop: '25px',
          textAlign: 'center',
          padding: '15px 30px',
          background: 'rgba(255, 170, 0, 0.1)',
          border: '2px solid var(--accent)',
          clipPath: 'polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px)',
        }}
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 1.5 }}
      >
        <p style={{
          fontSize: '1rem',
          fontFamily: 'IBM Plex Mono',
          color: 'var(--accent)'
        }}>
          💡 Todos los demos disponibles en modo simulación (sin robot físico)
        </p>
      </motion.div>
    </div>
  )
}

export default DemoSlide
