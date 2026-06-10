import { motion } from 'framer-motion'

const VoiceControlSlide = () => {
  const commands = [
    { category: 'MOVIMIENTO', icon: '▸', examples: ['Camina adelante', 'Muévete izquierda', 'Retrocede'], color: 'var(--primary)' },
    { category: 'GIROS', icon: '↻', examples: ['Gira derecha', 'Da la vuelta'], color: 'var(--accent)' },
    { category: 'GESTOS', icon: '⚡', examples: ['Siéntate', 'Ponte de pie', 'Saluda', 'Baila'], color: 'var(--secondary)' },
    { category: 'MODOS', icon: '⚙', examples: ['Modo normal', 'Apaga motores'], color: 'var(--primary)' },
  ]

  const pipeline = [
    { step: '01', label: 'AUDIO IN', desc: 'Captura de comando de voz' },
    { step: '02', label: 'WHISPER', desc: 'Speech-to-text [base model]' },
    { step: '03', label: 'QWEN2.5', desc: 'NLP → JSON generation [3b]' },
    { step: '04', label: 'GUARD', desc: 'Safety validation layer' },
    { step: '05', label: 'EXECUTE', desc: 'Robot action via WebRTC' }
  ]

  return (
    <div className="slide">
      <motion.h2
        initial={{ x: -100, opacity: 0, filter: 'blur(10px)' }}
        animate={{ x: 0, opacity: 1, filter: 'blur(0px)' }}
        transition={{ duration: 0.6 }}
      >
        CONTROL POR VOZ
      </motion.h2>

      <div className="grid-2">
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          <h3>PIPELINE DE PROCESAMIENTO</h3>
          <div style={{ marginTop: '25px' }}>
            {pipeline.map((item, index) => (
              <motion.div
                key={item.step}
                initial={{ x: -30, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.3 + index * 0.15 }}
                style={{ marginBottom: '15px', position: 'relative' }}
              >
                <div className="card" style={{
                  padding: '20px',
                  borderLeft: index === pipeline.length - 1 ? '4px solid var(--secondary)' : '4px solid var(--border)',
                  transition: 'all 0.3s'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <div style={{
                      width: '45px',
                      height: '45px',
                      border: '2px solid var(--primary)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontFamily: 'IBM Plex Mono',
                      fontWeight: '700',
                      color: 'var(--primary)',
                      fontSize: '1rem',
                      clipPath: 'polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px)',
                      background: 'rgba(255, 85, 0, 0.1)'
                    }}>
                      {item.step}
                    </div>
                    <div style={{ flex: 1 }}>
                      <div style={{
                        fontFamily: 'IBM Plex Mono',
                        fontWeight: '700',
                        fontSize: '1rem',
                        color: 'var(--primary)',
                        letterSpacing: '1px',
                        marginBottom: '4px'
                      }}>
                        {item.label}
                      </div>
                      <div style={{
                        fontFamily: 'Space Mono',
                        fontSize: '0.85rem',
                        opacity: 0.7
                      }}>
                        {item.desc}
                      </div>
                    </div>
                  </div>
                </div>
                {index < pipeline.length - 1 && (
                  <motion.div
                    animate={{ opacity: [0.3, 0.8, 0.3] }}
                    transition={{ duration: 2, repeat: Infinity, delay: index * 0.3 }}
                    style={{
                      position: 'absolute',
                      left: '22px',
                      bottom: '-15px',
                      color: 'var(--secondary)',
                      fontSize: '1.5rem',
                      fontWeight: '700'
                    }}
                  >
                    ↓
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          <h3>COMANDOS DISPONIBLES</h3>
          <div style={{ marginTop: '25px' }}>
            {commands.map((cmd, index) => (
              <motion.div
                key={cmd.category}
                className="card"
                style={{ marginBottom: '15px', borderLeftColor: cmd.color, borderLeftWidth: '4px' }}
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 + index * 0.1 }}
              >
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  marginBottom: '12px'
                }}>
                  <span style={{
                    fontSize: '1.2rem',
                    color: cmd.color
                  }}>
                    {cmd.icon}
                  </span>
                  <h4 style={{
                    color: cmd.color,
                    fontFamily: 'IBM Plex Mono',
                    letterSpacing: '1px',
                    fontSize: '0.95rem'
                  }}>
                    {cmd.category}
                  </h4>
                </div>
                <div style={{
                  display: 'flex',
                  gap: '8px',
                  flexWrap: 'wrap'
                }}>
                  {cmd.examples.map((ex) => (
                    <span
                      key={ex}
                      style={{
                        background: 'rgba(0, 0, 0, 0.4)',
                        border: '1px solid var(--border)',
                        padding: '6px 12px',
                        fontSize: '0.8rem',
                        fontFamily: 'Space Mono',
                        color: '#e0e0e0',
                        clipPath: 'polygon(5px 0, 100% 0, 100% calc(100% - 5px), calc(100% - 5px) 100%, 0 100%, 0 5px)',
                        transition: 'all 0.2s',
                        cursor: 'default'
                      }}
                    >
                      {ex}
                    </span>
                  ))}
                </div>
              </motion.div>
            ))}

            <motion.div
              className="card"
              style={{
                marginTop: '20px',
                background: 'rgba(180, 255, 0, 0.05)',
                borderColor: 'var(--secondary)',
                borderWidth: '2px'
              }}
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 1.1 }}
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px'
              }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  border: '2px solid var(--secondary)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '1.2rem',
                  clipPath: 'polygon(6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%, 0 6px)',
                  background: 'rgba(180, 255, 0, 0.1)'
                }}>
                  ✓
                </div>
                <div>
                  <h4 style={{
                    color: 'var(--secondary)',
                    fontFamily: 'IBM Plex Mono',
                    fontSize: '1rem',
                    letterSpacing: '1px',
                    marginBottom: '4px'
                  }}>
                    100% LOCAL
                  </h4>
                  <p style={{
                    fontSize: '0.85rem',
                    marginTop: '4px',
                    opacity: 0.8,
                    fontFamily: 'Space Mono'
                  }}>
                    Sin APIs externas • Sin internet • Procesamiento on-device
                  </p>
                </div>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>

      {/* Data stream animation */}
      <motion.div
        animate={{
          x: ['-100%', '200%']
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: 'linear'
        }}
        style={{
          position: 'absolute',
          bottom: '30px',
          left: 0,
          fontSize: '0.7rem',
          fontFamily: 'Space Mono',
          color: 'var(--secondary)',
          opacity: 0.2,
          whiteSpace: 'nowrap'
        }}
      >
        {'[AUDIO] → [STT] → [NLP] → [VALIDATE] → [EXECUTE] '.repeat(10)}
      </motion.div>
    </div>
  )
}

export default VoiceControlSlide
