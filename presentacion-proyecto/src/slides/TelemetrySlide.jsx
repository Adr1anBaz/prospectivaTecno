import { motion } from 'framer-motion'

const TelemetrySlide = () => {
  const telemetryData = [
    {
      category: '🧭 IMU & Orientación',
      items: ['Cuaternión [W,X,Y,Z]', 'Roll, Pitch, Yaw', 'Giroscopio', 'Acelerómetro', 'Temperatura'],
    },
    {
      category: '📍 Posición & Velocidad',
      items: ['Posición [X,Y,Z]', 'Velocidad lineal', 'Velocidad angular', 'Altura corporal'],
    },
    {
      category: '🦿 Estado de Patas',
      items: ['Fuerza en cada pata (N)', 'Posición relativa', 'Velocidad relativa', '4 patas monitoreadas'],
    },
    {
      category: '⚙️ Motores (20 total)',
      items: ['Posición angular', 'Velocidad', 'Torque estimado', 'Temperatura', 'Estado de com'],
    },
  ]

  return (
    <div className="slide">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        📡 Sistema de Telemetría en Tiempo Real
      </motion.h2>

      <div className="grid-2">
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h3>Datos Monitoreados</h3>

          {telemetryData.map((section, index) => (
            <motion.div
              key={section.category}
              className="card"
              style={{ marginBottom: '15px' }}
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3 + index * 0.15 }}
            >
              <h4 style={{ color: 'var(--primary)', marginBottom: '12px' }}>{section.category}</h4>
              <ul style={{ fontSize: '0.95rem', opacity: 0.9 }}>
                {section.items.map((item) => (
                  <li key={item} style={{ padding: '5px 0' }}>{item}</li>
                ))}
              </ul>
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h3>Monitoreo Adicional</h3>

          <motion.div
            className="card"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            <h4 style={{ color: 'var(--accent)' }}>🔋 Batería (BMS)</h4>
            <ul style={{ fontSize: '0.95rem', marginTop: '10px' }}>
              <li>Nivel de carga (SOC %)</li>
              <li>Voltaje y corriente</li>
              <li>Potencia instantánea (W)</li>
              <li>Ciclos de carga</li>
              <li>Temperatura de celdas</li>
            </ul>
            <div style={{ marginTop: '15px', padding: '10px', background: 'rgba(0, 255, 136, 0.1)', borderRadius: '8px' }}>
              <p style={{ fontSize: '0.85rem' }}>
                🟢 {'>'}60% | 🟡 30-60% | 🔴 {'<'}30%
              </p>
            </div>
          </motion.div>

          <motion.div
            className="card"
            style={{ marginTop: '20px' }}
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            <h4 style={{ color: 'var(--secondary)' }}>🚧 Detección de Obstáculos</h4>
            <ul style={{ fontSize: '0.95rem', marginTop: '10px' }}>
              <li>Frente, Atrás, Izquierda, Derecha</li>
              <li>Distancias en metros</li>
            </ul>
            <div style={{ marginTop: '15px', padding: '10px', background: 'rgba(255, 0, 234, 0.1)', borderRadius: '8px' }}>
              <p style={{ fontSize: '0.85rem' }}>
                🟢 {'>'}0.5m | 🟡 0.3-0.5m | 🔴 {'<'}0.3m ALERTA
              </p>
            </div>
          </motion.div>

          <motion.div
            className="card"
            style={{ marginTop: '20px' }}
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 1.0 }}
          >
            <h4 style={{ color: 'var(--primary)' }}>💻 Sistema</h4>
            <ul style={{ fontSize: '0.95rem', marginTop: '10px' }}>
              <li>Modo actual del robot (0-11)</li>
              <li>Tipo de marcha (Idle/Trot/Run)</li>
              <li>Progreso de acción (0-100%)</li>
              <li>Temperaturas NTC1/NTC2</li>
              <li>Ventiladores (frecuencia Hz)</li>
              <li>Firmware y número de serie</li>
            </ul>
          </motion.div>

          <motion.div
            className="card"
            style={{ marginTop: '20px', background: 'rgba(0, 212, 255, 0.1)' }}
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 1.2 }}
          >
            <h4 style={{ color: 'var(--primary)' }}>📊 Dashboard</h4>
            <p style={{ fontSize: '0.95rem', marginTop: '8px' }}>
              ✅ Actualización cada 0.5 segundos (2 Hz)<br />
              ✅ Modo demo sin robot disponible<br />
              ✅ Visualización en consola en tiempo real
            </p>
          </motion.div>
        </motion.div>
      </div>

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
        transition={{ delay: 1.4 }}
      >
        <p style={{ fontSize: '1.1rem' }}>
          <strong>Tópicos ROS2:</strong> SportModeState | LowState | WirelessController
        </p>
      </motion.div>
    </div>
  )
}

export default TelemetrySlide
