import { motion } from 'framer-motion'

const DemoSlide = () => {
  return (
    <div className="slide">
      <motion.h2
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        style={{ textAlign: 'center', marginBottom: '50px' }}
      >
        🎬 Demo y Casos de Uso
      </motion.h2>

      <div className="grid-2" style={{ gap: '30px' }}>
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h3>🎤 Demo de Control por Voz</h3>

          <div className="card" style={{ background: 'rgba(0, 212, 255, 0.1)', marginBottom: '20px' }}>
            <h4 style={{ color: 'var(--primary)', marginBottom: '15px' }}>Ejemplo de Interacción</h4>
            <div className="code-block" style={{ fontSize: '0.9rem' }}>
              <div style={{ color: 'var(--accent)' }}>$ uv run python robot_voice_controller.py</div>
              <div style={{ marginTop: '10px', opacity: 0.7 }}>✅ Conexión establecida</div>
              <div style={{ opacity: 0.7 }}>✅ Modelos cargados</div>
              <div style={{ marginTop: '10px' }}>⏺️ 🔴 GRABANDO...</div>
              <div style={{ marginTop: '10px', color: '#aaa' }}>[Usuario]: "Camina hacia adelante"</div>
              <div style={{ marginTop: '10px', opacity: 0.8 }}>📝 Transcribiendo...</div>
              <div style={{ opacity: 0.8 }}>💬 Comando: "camina hacia adelante"</div>
              <div style={{ opacity: 0.8 }}>🤖 Generando comando...</div>
              <div style={{ opacity: 0.8 }}>🛡️ Validando seguridad...</div>
              <div style={{ marginTop: '5px', color: 'var(--accent)' }}>
                🤖 EJECUTANDO: move_robot
              </div>
              <div style={{ opacity: 0.7 }}>📊 Parámetros: {`{"x": 0.3, "y": 0, "z": 0}`}</div>
              <div style={{ marginTop: '5px', color: 'var(--accent)' }}>✅ Comando completado</div>
            </div>
          </div>

          <div className="card">
            <h4 style={{ color: 'var(--secondary)' }}>🎯 Comandos de Prueba</h4>
            <ul style={{ fontSize: '0.95rem', marginTop: '10px' }}>
              <li>"Saluda" → Animación de saludo</li>
              <li>"Gira a la derecha" → Rotación</li>
              <li>"Siéntate" → Cambio de postura</li>
              <li>"Modo normal" → Cambio de modo</li>
            </ul>
          </div>
        </motion.div>

        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h3>🗺️ Demo de Navegación</h3>

          <div className="card" style={{ background: 'rgba(0, 255, 136, 0.1)', marginBottom: '20px' }}>
            <h4 style={{ color: 'var(--accent)', marginBottom: '15px' }}>Flujo de Navegación</h4>
            <div style={{ fontSize: '0.95rem', lineHeight: '2' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ fontSize: '1.5rem' }}>1️⃣</span>
                <span>Ejecutar script de mapeo</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ fontSize: '1.5rem' }}>2️⃣</span>
                <span>Robot genera mapa en RViz2</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ fontSize: '1.5rem' }}>3️⃣</span>
                <span>Guardar mapa (.pgm + .yaml)</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ fontSize: '1.5rem' }}>4️⃣</span>
                <span>Ejecutar script de navegación</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ fontSize: '1.5rem' }}>5️⃣</span>
                <span>Establecer goal point</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ fontSize: '1.5rem' }}>6️⃣</span>
                <span>Robot navega autónomamente</span>
              </div>
            </div>
          </div>

          <div className="card">
            <h4 style={{ color: 'var(--primary)' }}>📊 Demo de Telemetría</h4>
            <div className="code-block" style={{ fontSize: '0.85rem', marginTop: '10px' }}>
              <div style={{ color: 'var(--accent)' }}>$ uv run python telemetry_demo.py</div>
              <div style={{ marginTop: '10px', opacity: 0.7 }}>
                📡 Dashboard en Tiempo Real
              </div>
              <div style={{ opacity: 0.6, marginTop: '5px' }}>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
              <div>🧭 IMU: Roll=0.5° Pitch=1.2° Yaw=45°</div>
              <div>📍 Pos: X=1.2m Y=0.3m Z=0.2m</div>
              <div>🔋 Batería: 85% | 24.5V | 2.3A</div>
              <div>🦿 Patas: FL=15N FR=16N RL=14N RR=15N</div>
              <div>⚙️ Modo: Walk (4) | Marcha: Trot</div>
              <div style={{ opacity: 0.6, marginTop: '5px' }}>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</div>
            </div>
          </div>
        </motion.div>
      </div>

      <motion.div
        style={{ marginTop: '40px' }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
      >
        <div className="card" style={{ background: 'rgba(255, 255, 255, 0.05)' }}>
          <h3 style={{ color: 'var(--primary)', marginBottom: '20px', textAlign: 'center' }}>
            🎥 Videos de Demo Disponibles
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', fontSize: '0.95rem' }}>
            <div style={{ textAlign: 'center', padding: '15px', background: 'rgba(0, 212, 255, 0.1)', borderRadius: '10px' }}>
              <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🎤</div>
              <strong>Control por Voz</strong>
              <p style={{ fontSize: '0.85rem', marginTop: '8px', opacity: 0.8 }}>
                Demostración de comandos de movimiento y gestos
              </p>
            </div>
            <div style={{ textAlign: 'center', padding: '15px', background: 'rgba(0, 255, 136, 0.1)', borderRadius: '10px' }}>
              <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🗺️</div>
              <strong>Mapeo SLAM</strong>
              <p style={{ fontSize: '0.85rem', marginTop: '8px', opacity: 0.8 }}>
                Proceso de generación de mapa en RViz2
              </p>
            </div>
            <div style={{ textAlign: 'center', padding: '15px', background: 'rgba(255, 0, 234, 0.1)', borderRadius: '10px' }}>
              <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🧭</div>
              <strong>Navegación</strong>
              <p style={{ fontSize: '0.85rem', marginTop: '8px', opacity: 0.8 }}>
                Robot navegando hacia goal points
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      <motion.div
        style={{
          marginTop: '30px',
          textAlign: 'center',
          padding: '20px',
          background: 'linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(255, 0, 234, 0.1))',
          borderRadius: '15px',
          border: '2px solid rgba(255, 255, 255, 0.1)',
        }}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 1.2 }}
      >
        <p style={{ fontSize: '1.2rem', fontWeight: '600' }}>
          💡 Todos los demos disponibles en modo simulación (sin robot físico)
        </p>
      </motion.div>
    </div>
  )
}

export default DemoSlide
