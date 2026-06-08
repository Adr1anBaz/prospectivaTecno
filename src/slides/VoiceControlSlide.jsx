import { motion } from 'framer-motion'

const VoiceControlSlide = () => {
  const commands = [
    { category: '🏃 Movimiento', examples: ['Camina adelante', 'Muévete a la izquierda', 'Retrocede'] },
    { category: '🔄 Giros', examples: ['Gira a la derecha', 'Da la vuelta'] },
    { category: '🎭 Gestos', examples: ['Siéntate', 'Ponte de pie', 'Saluda', 'Baila'] },
    { category: '⚙️ Modos', examples: ['Modo normal', 'Apaga los motores'] },
  ]

  return (
    <div className="slide">
      <motion.h2
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        🎤 Sistema de Control por Voz
      </motion.h2>

      <div className="grid-2">
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          <h3>Pipeline de Procesamiento</h3>
          <div className="flow-diagram" style={{ flexDirection: 'column', gap: '20px' }}>
            <div className="flow-step">
              <strong>1. Captura de Audio</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '10px', opacity: 0.8 }}>
                Usuario habla comando
              </p>
            </div>
            <div className="flow-arrow">↓</div>
            <div className="flow-step">
              <strong>2. Whisper (base)</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '10px', opacity: 0.8 }}>
                Transcripción voz → texto
              </p>
            </div>
            <div className="flow-arrow">↓</div>
            <div className="flow-step">
              <strong>3. Ollama (Qwen2.5:3b)</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '10px', opacity: 0.8 }}>
                Generación de comando JSON
              </p>
            </div>
            <div className="flow-arrow">↓</div>
            <div className="flow-step">
              <strong>4. Guardrails</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '10px', opacity: 0.8 }}>
                Validación de seguridad
              </p>
            </div>
            <div className="flow-arrow">↓</div>
            <div className="flow-step" style={{ borderColor: 'var(--accent)' }}>
              <strong>5. Robot Ejecuta</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '10px', opacity: 0.8 }}>
                Vía WebRTC
              </p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          <h3>Comandos Disponibles</h3>
          {commands.map((cmd, index) => (
            <motion.div
              key={cmd.category}
              className="card"
              style={{ marginBottom: '15px' }}
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.5 + index * 0.1 }}
            >
              <h4 style={{ color: 'var(--accent)', marginBottom: '10px' }}>{cmd.category}</h4>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                {cmd.examples.map((ex) => (
                  <span
                    key={ex}
                    style={{
                      background: 'rgba(0, 255, 136, 0.1)',
                      padding: '5px 12px',
                      borderRadius: '10px',
                      fontSize: '0.85rem',
                      border: '1px solid rgba(0, 255, 136, 0.3)',
                    }}
                  >
                    "{ex}"
                  </span>
                ))}
              </div>
            </motion.div>
          ))}

          <motion.div
            className="card"
            style={{ marginTop: '20px', background: 'rgba(0, 212, 255, 0.1)' }}
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 1 }}
          >
            <h4 style={{ color: 'var(--primary)' }}>✅ 100% Local</h4>
            <p style={{ fontSize: '0.95rem', marginTop: '8px' }}>
              Sin APIs externas ni conexión a internet requerida
            </p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}

export default VoiceControlSlide
