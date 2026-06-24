import { motion } from 'framer-motion'

const tools = [
  {
    category: 'Información General',
    items: [
      { name: 'health_check', desc: 'Estado del servidor MCP' },
      { name: 'database_summary', desc: 'Resumen de la BD del campus' },
      { name: 'list_places', desc: 'Lista todas las ubicaciones' },
    ],
  },
  {
    category: 'Lugares',
    items: [
      { name: 'search_places', desc: 'Búsqueda semántica de lugares' },
      { name: 'get_place_detail', desc: 'Detalle por ID' },
      { name: 'get_place_detail_by_name', desc: 'Detalle por nombre' },
    ],
  },
  {
    category: 'Comida',
    items: [
      { name: 'search_food', desc: 'Buscar restaurantes/cafés' },
      { name: 'get_restaurant_menu', desc: 'Menú por ID' },
      { name: 'get_restaurant_menu_by_name', desc: 'Menú por nombre' },
    ],
  },
  {
    category: 'Tiendas',
    items: [
      { name: 'search_products', desc: 'Buscar productos en tiendas' },
      { name: 'get_store_products', desc: 'Productos por tienda' },
    ],
  },
  {
    category: 'Servicios',
    items: [
      { name: 'find_office_by_need', desc: 'Oficina según necesidad' },
      { name: 'get_gates', desc: 'Información de entradas' },
    ],
  },
  {
    category: 'Contexto',
    items: [
      { name: 'search_semantic_documents', desc: 'Búsqueda semántica en docs' },
      { name: 'get_current_crowd_levels', desc: 'Nivel de afluencia actual' },
    ],
  },
]

export default function MCPClientSlide() {
  return (
    <div style={{ padding: '0 60px', maxWidth: 1100 }}>
      <motion.h2
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        style={{
          fontFamily: "'Instrument Serif', serif",
          fontSize: 'clamp(2.4rem, 5vw, 3.5rem)',
          fontWeight: 400,
          marginBottom: 12,
        }}
      >
        MCP Client
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          color: 'var(--text-dim)',
          fontSize: '1.05rem',
          marginBottom: 32,
          fontWeight: 300,
        }}
      >
        15 herramientas disponibles para el LLM vía JSON-RPC 2.0
      </motion.p>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 16,
      }}>
        {tools.map((group, gi) => (
          <motion.div
            key={gi}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 + gi * 0.1 }}
            style={{
              padding: '20px',
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: 12,
            }}
          >
            <div style={{
              fontSize: '0.7rem',
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              color: 'var(--blue)',
              marginBottom: 14,
              fontWeight: 600,
            }}>
              {group.category}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {group.items.map((tool, ti) => (
                <div key={ti} style={{
                  padding: '10px 12px',
                  background: 'rgba(255,255,255,0.02)',
                  borderRadius: 8,
                  borderLeft: '2px solid var(--blue)',
                }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text)', marginBottom: 2 }}>{tool.name}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>{tool.desc}</div>
                </div>
              ))}
            </div>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.9 }}
        style={{
          marginTop: 24,
          padding: '16px 20px',
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 10,
          display: 'flex',
          alignItems: 'center',
          gap: 16,
        }}
      >
        <div style={{
          width: 40,
          height: 40,
          borderRadius: '50%',
          background: 'rgba(91,164,230,0.1)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.2rem',
        }}>🔐</div>
        <div>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text)', marginBottom: 2 }}>Autenticación Bearer</div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>MCP_BEARER_TOKEN en .env — JSON-RPC 2.0 sobre HTTP</div>
        </div>
      </motion.div>
    </div>
  )
}
