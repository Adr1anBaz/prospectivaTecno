import { motion } from 'framer-motion'

const ROS2SLAMSlide = () => {
  return (
    <div className="slide">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        🗺️ Sistema ROS2 + SLAM + Navegación Autónoma
      </motion.h2>

      <div className="grid-2">
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h3>Implementación</h3>

          <motion.div
            className="card"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <h4 style={{ color: 'var(--primary)' }}>📦 SDK y Herramientas</h4>
            <ul style={{ fontSize: '0.95rem', marginTop: '10px' }}>
              <li><strong>Unitree SDK</strong> - Repositorio oficial</li>
              <li><strong>SLAM Toolbox</strong> - Mapeo y localización</li>
              <li><strong>RViz2</strong> - Visualización 3D</li>
              <li><strong>Nav2</strong> - Stack de navegación</li>
            </ul>
          </motion.div>

          <motion.div
            className="card"
            style={{ marginTop: '20px' }}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            <h4 style={{ color: 'var(--accent)' }}>🗂️ Scripts Bash</h4>
            <div className="code-block" style={{ marginTop: '15px', fontSize: '0.85rem' }}>
              <div># Script 1: Mapeo</div>
              <div style={{ opacity: 0.7, marginLeft: '15px' }}>- Activa odometría</div>
              <div style={{ opacity: 0.7, marginLeft: '15px' }}>- Genera mapa de puntos</div>
              <div style={{ opacity: 0.7, marginLeft: '15px' }}>- SLAM Toolbox con modelo</div>
              <div style={{ opacity: 0.7, marginLeft: '15px' }}>- Visualiza en RViz2</div>
              <div style={{ opacity: 0.7, marginLeft: '15px' }}>- Serializa: .pgm + .yaml</div>
              <div style={{ marginTop: '10px' }}># Script 2: Navegación</div>
              <div style={{ opacity: 0.7, marginLeft: '15px' }}>- Carga mapa serializado</div>
              <div style={{ opacity: 0.7, marginLeft: '15px' }}>- Activa Nav2</div>
              <div style={{ opacity: 0.7, marginLeft: '15px' }}>- Navegación autónoma</div>
              <div style={{ opacity: 0.7, marginLeft: '15px' }}>- Establecer goal points</div>
            </div>
          </motion.div>

          <motion.div
            className="card"
            style={{ marginTop: '20px', background: 'rgba(0, 212, 255, 0.1)' }}
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            <h4 style={{ color: 'var(--primary)' }}>✅ Funcionalidades</h4>
            <ul style={{ fontSize: '0.95rem', marginTop: '10px' }}>
              <li>Mapeo en tiempo real con SLAM</li>
              <li>Navegación punto a punto</li>
              <li>Funciona en simulación Y físicamente</li>
              <li>Evitación de obstáculos</li>
            </ul>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <h3>Flujo de Trabajo</h3>

          <div style={{ background: 'rgba(0, 0, 0, 0.3)', padding: '25px', borderRadius: '15px' }}>
            <motion.div
              style={{
                background: 'rgba(0, 212, 255, 0.15)',
                border: '2px solid var(--primary)',
                borderRadius: '12px',
                padding: '20px',
                marginBottom: '15px',
              }}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <strong style={{ fontSize: '1.1rem' }}>Fase 1: Mapeo</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '10px', opacity: 0.9 }}>
                1. Ejecutar script de mapeo<br />
                2. Robot recorre el área<br />
                3. SLAM genera mapa 3D<br />
                4. Visualización en RViz2<br />
                5. Guardar mapa (.pgm + .yaml)
              </p>
            </motion.div>

            <div style={{ textAlign: 'center', fontSize: '2rem', margin: '10px 0', color: 'var(--accent)' }}>
              ↓
            </div>

            <motion.div
              style={{
                background: 'rgba(0, 255, 136, 0.15)',
                border: '2px solid var(--accent)',
                borderRadius: '12px',
                padding: '20px',
              }}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              <strong style={{ fontSize: '1.1rem' }}>Fase 2: Navegación</strong>
              <p style={{ fontSize: '0.9rem', marginTop: '10px', opacity: 0.9 }}>
                1. Cargar mapa guardado<br />
                2. Ejecutar script de navegación<br />
                3. Establecer goal point en RViz2<br />
                4. Nav2 calcula ruta<br />
                5. Robot navega autónomamente
              </p>
            </motion.div>
          </div>

          <motion.div
            className="card"
            style={{ marginTop: '25px', background: 'rgba(255, 200, 0, 0.1)', border: '2px solid #ffc107' }}
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 1.1 }}
          >
            <h4 style={{ color: '#ffc107' }}>⚠️ Problema Detectado</h4>
            <p style={{ fontSize: '0.95rem', marginTop: '12px', lineHeight: '1.7' }}>
              <strong>Síntoma:</strong> El robot se desvía durante la navegación autónoma
              (va chueco y da vueltas innecesarias)
            </p>
            <div style={{ marginTop: '15px', padding: '15px', background: 'rgba(0, 0, 0, 0.3)', borderRadius: '8px' }}>
              <p style={{ fontSize: '0.9rem', marginBottom: '8px' }}><strong>Hipótesis:</strong></p>
              <ul style={{ fontSize: '0.85rem', lineHeight: '1.7' }}>
                <li>Mapa de baja calidad (necesita remapeo)</li>
                <li>Falta de corrección de posición en tiempo real</li>
                <li>Deriva en la odometría</li>
              </ul>
            </div>
          </motion.div>
        </motion.div>
      </div>

      <motion.div
        style={{
          marginTop: '25px',
          textAlign: 'center',
          padding: '20px',
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '15px',
        }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.3 }}
      >
        <p style={{ fontSize: '1.05rem' }}>
          <strong>Outputs:</strong> Odometría | Mapa de puntos | Diagrama SLAM | Archivos .pgm/.yaml
        </p>
      </motion.div>
    </div>
  )
}

export default ROS2SLAMSlide
