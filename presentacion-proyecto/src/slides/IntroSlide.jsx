import { motion } from 'framer-motion'

const IntroSlide = () => {
  return (
    <div className="slide" style={{ textAlign: 'center' }}>
      <motion.div
        initial={{ scale: 0.5, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.h1
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          🤖 Sistema de Control Inteligente
        </motion.h1>
        <motion.h1
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          style={{ fontSize: '3rem', marginTop: '20px' }}
        >
          Unitree Go2 Air
        </motion.h1>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.6 }}
        style={{ marginTop: '60px' }}
      >
        <p style={{ fontSize: '1.5rem', opacity: 0.8, marginBottom: '40px' }}>
          Control por Voz + Telemetría en Tiempo Real + Navegación Autónoma
        </p>

        <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', flexWrap: 'wrap' }}>
          <span className="badge">🎤 OpenAI Whisper</span>
          <span className="badge">🤖 Ollama (Qwen2.5)</span>
          <span className="badge">📡 WebRTC</span>
          <span className="badge">🗺️ ROS2 + SLAM</span>
          <span className="badge">🧭 Nav2</span>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.8 }}
        style={{ marginTop: '60px' }}
      >
        <h3 style={{ color: 'var(--accent)', fontSize: '1.3rem' }}>
          Proyecto de Investigación y Desarrollo
        </h3>
        <p style={{ fontSize: '1.1rem', opacity: 0.7 }}>
          Control robótico mediante procesamiento local de voz + navegación autónoma con SLAM
        </p>
      </motion.div>
    </div>
  )
}

export default IntroSlide
