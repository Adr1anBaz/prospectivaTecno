import { motion } from 'framer-motion'

const achievements = [
  '100% validez en tool calling (49 prompts)',
  'Recall 1.0 en intenciones de navegación',
  'Pipeline ~1.6 s de latencia total estimada',
  'EventBus: 1300 eventos/s sin pérdidas',
  'Pico de 85.7 MB RAM del proceso conversacional',
  'Validación física: 30 comandos + rutas navegables',
]

const future = [
  'Integración SLAM sobre ROS2 para navegación autónoma',
  'Estabilizar odometría tras rutinas de alta dinámica',
  'Completar control por velocidad',
  'Clase de rechazo explícito para ruido',
  'Evaluar modelos locales (híbrido) para operación sin internet',
]

export default function ConclusionesSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1100 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 8,
        }}
      >
        Conclusiones
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '0.85rem',
          marginBottom: 36,
          fontWeight: 300,
          maxWidth: 700,
          lineHeight: 1.6,
        }}
      >
        La arquitectura separa el control físico local del procesamiento lingüístico remoto.
        El uso de STT, LLM y TTS externos, junto con MCP para consultas estructuradas,
        traslada la carga computacional cara fuera del dispositivo local.
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
        {/* Achievements */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h4 style={{
            fontSize: '0.75rem',
            textTransform: 'uppercase',
            letterSpacing: '0.1em',
            color: '#6BCB8A',
            marginBottom: 16,
            fontWeight: 600,
          }}>
            Logros
          </h4>
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 10 }}>
            {achievements.map((item, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + i * 0.06 }}
                style={{
                  color: 'var(--text-dim)',
                  fontSize: '0.85rem',
                  paddingLeft: 14,
                  borderLeft: '2px solid #6BCB8A',
                  lineHeight: 1.4,
                }}
              >
                {item}
              </motion.li>
            ))}
          </ul>
        </motion.div>

        {/* Future */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h4 style={{
            fontSize: '0.75rem',
            textTransform: 'uppercase',
            letterSpacing: '0.1em',
            color: 'var(--text-muted)',
            marginBottom: 16,
            fontWeight: 600,
          }}>
            Trabajo Futuro
          </h4>
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 10 }}>
            {future.map((item, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.06 }}
                style={{
                  color: 'var(--text-muted)',
                  fontSize: '0.85rem',
                  paddingLeft: 14,
                  borderLeft: '2px solid var(--border)',
                  lineHeight: 1.4,
                }}
              >
                {item}
              </motion.li>
            ))}
          </ul>
        </motion.div>
      </div>

      {/* Key insight */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7 }}
        style={{
          marginTop: 32,
          padding: '14px 20px',
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 10,
          textAlign: 'center',
          fontSize: '0.8rem',
          color: 'var(--text-dim)',
          lineHeight: 1.6,
        }}
      >
        La reducción de requerimientos locales de hardware tiene como contrapartida
        una dependencia explícita de conectividad. En aplicaciones de guía en campus,
        este balance es aceptable cuando existe cobertura de red estable.
      </motion.div>
    </div>
  )
}
