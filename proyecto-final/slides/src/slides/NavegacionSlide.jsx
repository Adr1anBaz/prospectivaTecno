import { motion } from 'framer-motion'

const nodes = [
  { id: 'A', x: 80, y: 60 },
  { id: 'B', x: 200, y: 40 },
  { id: 'C', x: 160, y: 140 },
  { id: 'D', x: 300, y: 100 },
  { id: 'E', x: 280, y: 180 },
  { id: 'F', x: 400, y: 60 },
  { id: 'G', x: 380, y: 160 },
]

const edges = [
  [0, 1], [0, 2], [1, 2], [1, 3], [2, 4], [3, 4], [3, 5], [4, 6], [5, 6],
]

const path = [0, 1, 3, 5]

export default function NavegacionSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1000 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 48,
        }}
      >
        Navegación
      </motion.h2>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 60, alignItems: 'center' }}>
        {/* Graph visualization */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <svg viewBox="0 0 480 220" style={{ width: '100%' }}>
            {/* Edges */}
            {edges.map(([a, b], i) => {
              const isPath = path.includes(a) && path.includes(b) &&
                Math.abs(path.indexOf(a) - path.indexOf(b)) === 1
              return (
                <line
                  key={i}
                  x1={nodes[a].x} y1={nodes[a].y}
                  x2={nodes[b].x} y2={nodes[b].y}
                  stroke={isPath ? '#5BA4E6' : 'rgba(255,255,255,0.08)'}
                  strokeWidth={isPath ? 2.5 : 1}
                />
              )
            })}
            {/* Nodes */}
            {nodes.map((n, i) => (
              <g key={i}>
                <circle
                  cx={n.x} cy={n.y} r={path.includes(i) ? 10 : 6}
                  fill={path.includes(i) ? '#5BA4E6' : 'var(--surface)'}
                  stroke={path.includes(i) ? '#5BA4E6' : 'rgba(255,255,255,0.15)'}
                  strokeWidth={1.5}
                />
                <text
                  x={n.x} y={n.y + 4}
                  textAnchor="middle"
                  fontSize="9"
                  fill={path.includes(i) ? '#0A0A0F' : 'rgba(255,255,255,0.4)'}
                  fontWeight="600"
                >
                  {n.id}
                </text>
              </g>
            ))}
          </svg>
        </motion.div>

        {/* Description */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          style={{ display: 'flex', flexDirection: 'column', gap: 24 }}
        >
          <div>
            <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 8 }}>
              Estructura
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem', lineHeight: 1.7 }}>
              Grafo donde cada nodo = ubicación alcanzable
              <br />
              Rutas divididas en tramos modulares
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 8 }}>
              Algoritmo
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem', lineHeight: 1.7 }}>
              Dijkstra para trayectorias óptimas
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 8 }}>
              Almacenamiento
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.95rem', lineHeight: 1.7 }}>
              Base de datos en servidor privado
              <br />
              <span style={{ color: 'var(--text-muted)' }}>El robot no aloja información del grafo</span>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
