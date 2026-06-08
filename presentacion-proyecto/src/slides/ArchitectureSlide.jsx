import { motion } from 'framer-motion'

const ArchitectureSlide = () => {
  return (
    <div className="slide">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        🏗️ Arquitectura del Sistema
      </motion.h2>

      <div className="grid-2">
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h3>Stack Tecnológico</h3>

          <div className="card">
            <h4 style={{ color: 'var(--primary)', marginBottom: '15px' }}>🎤 Audio & IA</h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><strong>Whisper (base)</strong> - Transcripción ~1GB</li>
              <li><strong>Ollama (Qwen2.5:3b)</strong> - LLM local ~1.9GB</li>
              <li><strong>SoundDevice</strong> - Captura de audio</li>
              <li><strong>PyTorch</strong> - Inferencia de modelos</li>
            </ul>
          </div>

          <div className="card" style={{ marginTop: '20px' }}>
            <h4 style={{ color: 'var(--accent)', marginBottom: '15px' }}>📡 Comunicación</h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><strong>WebRTC</strong> - Conexión en tiempo real</li>
              <li><strong>unitree-webrtc-connect</strong> - SDK oficial</li>
              <li><strong>LocalAP</strong> - Red 192.168.12.x</li>
            </ul>
          </div>

          <div className="card" style={{ marginTop: '20px' }}>
            <h4 style={{ color: 'var(--secondary)', marginBottom: '15px' }}>🗺️ Navegación</h4>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><strong>ROS2</strong> - Framework robótico</li>
              <li><strong>SLAM Toolbox</strong> - Mapeo y localización</li>
              <li><strong>Nav2</strong> - Navegación autónoma</li>
              <li><strong>RViz2</strong> - Visualización</li>
            </ul>
          </div>
        </motion.div>

        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h3>Flujo de Datos</h3>

          <div style={{ background: 'rgba(0, 0, 0, 0.3)', padding: '30px', borderRadius: '15px' }}>
            <motion.div
              style={{
                background: 'rgba(0, 212, 255, 0.1)',
                border: '2px solid var(--primary)',
                borderRadius: '10px',
                padding: '15px',
                marginBottom: '15px',
              }}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              <strong>Usuario</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '5px', opacity: 0.8 }}>
                Comando de voz
              </p>
            </motion.div>

            <div style={{ textAlign: 'center', fontSize: '2rem', margin: '10px 0' }}>↓</div>

            <motion.div
              style={{
                background: 'rgba(0, 255, 136, 0.1)',
                border: '2px solid var(--accent)',
                borderRadius: '10px',
                padding: '15px',
                marginBottom: '15px',
              }}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              <strong>Procesamiento Local</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '5px', opacity: 0.8 }}>
                Whisper → Ollama → Validación
              </p>
            </motion.div>

            <div style={{ textAlign: 'center', fontSize: '2rem', margin: '10px 0' }}>↓</div>

            <motion.div
              style={{
                background: 'rgba(255, 0, 234, 0.1)',
                border: '2px solid var(--secondary)',
                borderRadius: '10px',
                padding: '15px',
              }}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 1 }}
            >
              <strong>Robot Unitree Go2</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '5px', opacity: 0.8 }}>
                Ejecución del comando
              </p>
            </motion.div>
          </div>

          <motion.div
            className="card"
            style={{ marginTop: '30px', background: 'rgba(255, 0, 0, 0.1)' }}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 1.2 }}
          >
            <h4 style={{ color: '#ff6b6b' }}>🛡️ Sistema de Guardrails</h4>
            <ul style={{ fontSize: '0.95rem', marginTop: '10px' }}>
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
          padding: '20px',
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '15px',
        }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4 }}
      >
        <p style={{ fontSize: '1.1rem' }}>
          ⏱️ <strong>Tiempo de respuesta:</strong> 6-15 segundos por comando (incluyendo ejecución)
        </p>
      </motion.div>
    </div>
  )
}

export default ArchitectureSlide
