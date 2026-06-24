import { motion } from 'framer-motion'

const nodes = [
  { id: 'ENTRADA', x: 80, y: 180, label: 'Entrada' },
  { id: 'PASILLO_A', x: 200, y: 180, label: 'Pasillo A' },
  { id: 'PASILLO_B', x: 320, y: 120, label: 'Pasillo B' },
  { id: 'PASILLO_C', x: 320, y: 240, label: 'Pasillo C' },
  { id: 'BIOMEDICA', x: 440, y: 80, label: 'Biomédica' },
  { id: 'BIBLIOTECA', x: 440, y: 160, label: 'Biblioteca' },
  { id: 'GIORNALE', x: 440, y: 240, label: 'Giornale' },
  { id: 'CAFETERIA', x: 440, y: 320, label: 'Cafetería' },
]

const edges = [
  [0, 1], [1, 2], [1, 3], [2, 4], [2, 5], [3, 6], [3, 7],
]

const path = [0, 1, 3, 6]

export default function NavegacionSlide() {
  return (
    <div style={{ padding: '0 60px', maxWidth: 1000 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 32,
        }}
      >
        Navegación
      </motion.h2>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 40, alignItems: 'start' }}>
        {/* Graph visualization */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          style={{
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 16,
            padding: 24,
          }}
        >
          <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--text-muted)', marginBottom: 16 }}>
            Grafo del Campus — Nodos de Navegación
          </div>
          <svg viewBox="0 0 520 360" style={{ width: '100%' }}>
            {/* Edges */}
            {edges.map(([a, b], i) => {
              const isPath = path.includes(a) && path.includes(b) &&
                Math.abs(path.indexOf(a) - path.indexOf(b)) === 1
              return (
                <line
                  key={i}
                  x1={nodes[a].x} y1={nodes[a].y}
                  x2={nodes[b].x} y2={nodes[b].y}
                  stroke={isPath ? 'var(--blue)' : 'rgba(255,255,255,0.08)'}
                  strokeWidth={isPath ? 2.5 : 1}
                />
              )
            })}
            {/* Nodes */}
            {nodes.map((n, i) => (
              <g key={i}>
                <circle
                  cx={n.x} cy={n.y} r={path.includes(i) ? 12 : 8}
                  fill={path.includes(i) ? 'var(--blue)' : 'var(--surface)'}
                  stroke={path.includes(i) ? 'var(--blue)' : 'rgba(255,255,255,0.15)'}
                  strokeWidth={1.5}
                />
                <text
                  x={n.x} y={n.y + 4}
                  textAnchor="middle"
                  fontSize="8"
                  fill={path.includes(i) ? '#0A0A0F' : 'rgba(255,255,255,0.4)'}
                  fontWeight="600"
                >
                  {n.id[0]}
                </text>
                <text
                  x={n.x} y={n.y + 26}
                  textAnchor="middle"
                  fontSize="9"
                  fill={path.includes(i) ? 'var(--blue)' : 'rgba(255,255,255,0.35)'}
                  fontWeight="500"
                >
                  {n.label}
                </text>
              </g>
            ))}

            {/* Path label */}
            <text x="260" y="340" textAnchor="middle" fontSize="10" fill="var(--blue)" fontWeight="500">
              Ruta: Entrada → Pasillo A → Pasillo C → Giornale
            </text>
          </svg>
        </motion.div>

        {/* Description */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          style={{ display: 'flex', flexDirection: 'column', gap: 20 }}
        >
          <div style={{
            padding: '24px',
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--blue)', marginBottom: 12, fontWeight: 600 }}>
              Route API
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Servicio externo que calcula rutas óptimas entre nodos del grafo del campus
            </p>
          </div>

          <div style={{
            padding: '24px',
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--blue)', marginBottom: 12, fontWeight: 600 }}>
              Movimiento
            </h4>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Rutas pregrabadas en CSV modulares por tramo. Cada nodo→nodo tiene su archivo de movimiento
            </p>
          </div>

          <div style={{
            padding: '24px',
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: 12,
          }}>
            <h4 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--blue)', marginBottom: 12, fontWeight: 600 }}>
              Destinos Conocidos
            </h4>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {['biomedica', 'biblioteca', 'giornale', 'cafeteria', 'entrada'].map((d, i) => (
                <span key={i} style={{
                  padding: '4px 10px',
                  background: 'rgba(91,164,230,0.08)',
                  borderRadius: 6,
                  fontSize: '0.8rem',
                  color: 'var(--blue)',
                }}>{d}</span>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
