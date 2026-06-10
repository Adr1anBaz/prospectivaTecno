import { motion } from 'framer-motion'

const IntroSlide = () => {
  return (
    <div className="slide" style={{ textAlign: 'center', position: 'relative' }}>
      {/* Decorative corner elements */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.3 }}
        transition={{ delay: 0.5 }}
        style={{
          position: 'absolute',
          top: '40px',
          left: '40px',
          width: '80px',
          height: '80px',
          borderTop: '3px solid var(--primary)',
          borderLeft: '3px solid var(--primary)',
          clipPath: 'polygon(0 0, 100% 0, 100% 3px, 3px 3px, 3px 100%, 0 100%)'
        }}
      />
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.3 }}
        transition={{ delay: 0.7 }}
        style={{
          position: 'absolute',
          bottom: '40px',
          right: '40px',
          width: '80px',
          height: '80px',
          borderBottom: '3px solid var(--secondary)',
          borderRight: '3px solid var(--secondary)',
          clipPath: 'polygon(0 calc(100% - 3px), 0 100%, 100% 100%, 100% 0, calc(100% - 3px) 0, calc(100% - 3px) calc(100% - 3px), 0 calc(100% - 3px))'
        }}
      />

      <motion.div
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <motion.div
          style={{
            display: 'inline-block',
            padding: '8px 20px',
            border: '2px solid var(--secondary)',
            marginBottom: '30px',
            clipPath: 'polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px)',
            background: 'rgba(180, 255, 0, 0.05)'
          }}
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          <span style={{
            fontFamily: 'IBM Plex Mono',
            fontSize: '0.85rem',
            color: 'var(--secondary)',
            letterSpacing: '3px',
            textTransform: 'uppercase'
          }}>
            Sistema de Control Inteligente
          </span>
        </motion.div>

        <motion.h1
          initial={{ y: -50, opacity: 0, filter: 'blur(10px)' }}
          animate={{ y: 0, opacity: 1, filter: 'blur(0px)' }}
          transition={{ delay: 0.5, duration: 0.8 }}
          style={{
            fontSize: '4rem',
            letterSpacing: '-3px',
            marginBottom: '8px',
            lineHeight: '1'
          }}
        >
          UNITREE
        </motion.h1>
        <motion.h1
          initial={{ y: -50, opacity: 0, filter: 'blur(10px)' }}
          animate={{ y: 0, opacity: 1, filter: 'blur(0px)' }}
          transition={{ delay: 0.7, duration: 0.8 }}
          style={{
            fontSize: '3rem',
            letterSpacing: '-2px',
            color: 'var(--secondary)',
            textShadow: '0 0 30px rgba(180, 255, 0, 0.5)'
          }}
        >
          GO2 AIR
        </motion.h1>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9, duration: 0.6 }}
        style={{ marginTop: '30px' }}
      >
        <div style={{
          display: 'inline-block',
          padding: '20px 40px',
          border: '2px solid var(--border)',
          borderLeft: '4px solid var(--primary)',
          background: 'rgba(26, 26, 26, 0.8)',
          clipPath: 'polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px)',
          position: 'relative'
        }}>
          <p style={{
            fontSize: '1.15rem',
            opacity: 0.9,
            fontFamily: 'Space Mono',
            lineHeight: '1.8'
          }}>
            <span style={{ color: 'var(--primary)' }}>{'>'}</span> Control por Voz
            <span style={{ margin: '0 15px', color: 'var(--border)' }}>|</span>
            <span style={{ color: 'var(--primary)' }}>{'>'}</span> Telemetría RT
            <span style={{ margin: '0 15px', color: 'var(--border)' }}>|</span>
            <span style={{ color: 'var(--primary)' }}>{'>'}</span> Navegación Autónoma
          </p>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.1, duration: 0.6 }}
        style={{ marginTop: '30px' }}
      >
        <div style={{
          display: 'flex',
          gap: '15px',
          justifyContent: 'center',
          flexWrap: 'wrap',
          maxWidth: '900px',
          margin: '0 auto'
        }}>
          {[
            { icon: '[WHISPER]', label: 'OpenAI Whisper', delay: 0 },
            { icon: '[OLLAMA]', label: 'Qwen2.5', delay: 0.1 },
            { icon: '[WebRTC]', label: 'Real-Time Comm', delay: 0.2 },
            { icon: '[ROS2]', label: 'Robot OS 2', delay: 0.3 },
            { icon: '[SLAM]', label: 'Mapping', delay: 0.4 },
            { icon: '[NAV2]', label: 'Navigation', delay: 0.5 }
          ].map((tech, i) => (
            <motion.span
              key={i}
              className="badge"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.3 + tech.delay }}
            >
              <span style={{ opacity: 0.5, marginRight: '8px' }}>{tech.icon}</span>
              {tech.label}
            </motion.span>
          ))}
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2, duration: 0.8 }}
        style={{ marginTop: '30px' }}
      >
        <div style={{
          display: 'inline-block',
          padding: '15px 30px',
          border: '2px solid var(--accent)',
          background: 'rgba(255, 170, 0, 0.05)',
          clipPath: 'polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px)'
        }}>
          <h3 style={{
            color: 'var(--accent)',
            fontSize: '1.1rem',
            marginBottom: '8px',
            fontFamily: 'IBM Plex Mono'
          }}>
            [R&D PROJECT]
          </h3>
          <p style={{
            fontSize: '0.95rem',
            opacity: 0.8,
            fontFamily: 'Space Mono',
            maxWidth: '600px'
          }}>
            Control robótico mediante procesamiento local de voz + navegación autónoma con SLAM
          </p>
        </div>
      </motion.div>

      {/* Animated scan lines */}
      <motion.div
        animate={{
          y: ['-100%', '200%']
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: 'linear'
        }}
        style={{
          position: 'absolute',
          left: 0,
          width: '100%',
          height: '2px',
          background: 'linear-gradient(to right, transparent, var(--primary), transparent)',
          opacity: 0.3,
          pointerEvents: 'none'
        }}
      />
    </div>
  )
}

export default IntroSlide
