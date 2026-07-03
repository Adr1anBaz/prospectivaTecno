import { motion } from 'framer-motion'

const layers = [
  {
    title: 'Procesamiento de Lenguaje',
    items: ['Captura y reproducción de audio', 'Reconocimiento de voz (STT)', 'Síntesis de voz (TTS)', 'Orquestación del diálogo (LLM)'],
    color: 'var(--blue)',
  },
  {
    title: 'Orquestación y Datos',
    items: ['Clasificador de intenciones', 'Conexión a base de datos vía MCP', 'Generación de instrucciones JSON', 'Memoria de conversación'],
    color: '#E6A85B',
  },
  {
    title: 'Control Robótico',
    items: ['Recepción de comandos JSON', 'Traducción a movimientos ROS2', 'Comunicación WebRTC con robot', 'Retroalimentación de estado'],
    color: '#6BCB8A',
  },
]

export default function AntiFeedbackSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1000 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.2rem)',
          fontWeight: 400,
          marginBottom: 8,
        }}
      >
        Arquitectura de Comunicación
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '0.9rem',
          marginBottom: 40,
          fontWeight: 300,
        }}
      >
        Procesos independientes que se comunican a través de un bus de eventos compartido
      </motion.p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 0, position: 'relative' }}>
        {layers.map((layer, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 + i * 0.15 }}
            style={{
              display: 'grid',
              gridTemplateColumns: '160px 1fr',
              gap: 16,
              padding: '16px 20px',
              background: 'var(--surface)',
              border: `1px solid ${layer.color}22`,
              borderLeft: `3px solid ${layer.color}`,
              borderRadius: i === 0 ? '12px 12px 0 0' : i === layers.length - 1 ? '0 0 12px 12px' : 0,
              marginTop: i > 0 ? -1 : 0,
            }}
          >
            <div>
              <div style={{
                fontSize: '0.6rem',
                textTransform: 'uppercase',
                letterSpacing: '0.1em',
                color: layer.color,
                fontWeight: 600,
                marginBottom: 2,
              }}>
                Capa {i + 1}
              </div>
              <div style={{ fontSize: '0.8rem', fontWeight: 500, color: 'var(--text)' }}>
                {layer.title}
              </div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {layer.items.map((item, j) => (
                <div key={j} style={{
                  fontSize: '0.78rem',
                  color: 'var(--text-dim)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                }}>
                  <span style={{ color: layer.color, fontSize: '0.45rem' }}>◆</span>
                  {item}
                </div>
              ))}
            </div>
          </motion.div>
        ))}

        <motion.div
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8, type: 'spring' }}
          style={{
            position: 'absolute',
            right: -20,
            top: '50%',
            transform: 'translateY(-50%)',
            background: 'var(--bg)',
            border: '1px solid var(--blue)',
            borderRadius: 20,
            padding: '8px 16px',
            fontSize: '0.65rem',
            color: 'var(--blue)',
            fontWeight: 600,
            letterSpacing: '0.05em',
            whiteSpace: 'nowrap',
          }}
        >
          EVENT BUS — Colas de mensajes
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.9 }}
        style={{
          marginTop: 20,
          padding: '10px 16px',
          background: 'var(--surface)',
          border: '1px dashed var(--border)',
          borderRadius: 6,
          fontSize: '0.78rem',
          color: 'var(--text-muted)',
          textAlign: 'center',
        }}
      >
        Capa de control robótico: archivos JSON compartidos entre el agente (Python) y ROS2 —
        escritura de comandos, ejecución, y retroalimentación de estado
      </motion.div>
    </div>
  )
}
