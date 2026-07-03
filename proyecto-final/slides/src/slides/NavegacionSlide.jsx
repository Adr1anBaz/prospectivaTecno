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

export default function NavegacionSlide() {
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
        Sistema de Navegación
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
        Del lenguaje natural a una ruta física en el campus
      </motion.p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 60, alignItems: 'center' }}>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <svg viewBox="0 0 480 220" style={{ width: '100%' }}>
            {edges.map(([a, b], i) => (
              <line
                key={i}
                x1={nodes[a].x} y1={nodes[a].y}
                x2={nodes[b].x} y2={nodes[b].y}
                stroke="rgba(255,255,255,0.1)"
                strokeWidth={1.2}
              />
            ))}
            {nodes.map((n, i) => (
              <g key={i}>
                <circle
                  cx={n.x} cy={n.y} r={8}
                  fill="var(--surface)"
                  stroke="rgba(91, 164, 230, 0.5)"
                  strokeWidth={1.5}
                />
                <text
                  x={n.x} y={n.y + 4}
                  textAnchor="middle"
                  fontSize="10"
                  fill="rgba(91, 164, 230, 0.7)"
                  fontWeight="600"
                >
                  {n.id}
                </text>
              </g>
            ))}
          </svg>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          style={{ display: 'flex', flexDirection: 'column', gap: 20 }}
        >
          <div>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 6 }}>
              Modelado del Entorno
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', lineHeight: 1.6 }}>
              Grafo no dirigido donde cada nodo representa una ubicación
              alcanzable (edificios, entradas, intersecciones) y cada arista
              una ruta posible entre ellos.
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 6 }}>
              Algoritmo de Ruteo
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', lineHeight: 1.6 }}>
              Dijkstra para trayectorias óptimas. El LLM traduce la intención
              del usuario a un destino y el sistema calcula la ruta más corta
              desde la ubicación actual.
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-muted)', marginBottom: 6 }}>
              Ejecución de Rutas
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', lineHeight: 1.6 }}>
              Las rutas se dividen en tramos modulares. El robot ejecuta cada
              segmento secuencialmente, con capacidad de pausa y retorno en
              cada punto de control.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
