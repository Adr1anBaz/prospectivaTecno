import { motion } from 'framer-motion'
// 1. Importas la imagen desde la ruta relativa donde la tengas guardada en src
import miImagenWebp from '../assets/images/muestra.webp' 

const queries = [
  '"Llévame a la cafetería con el desayuno más barato"',
  '"Llévame a donde haya buena señal de internet"',
  '"Llévame a la cafetería que no tenga tantas personas ahorita"',
]

export default function ObjetivoSlide() {
  return (
    <div style={{ padding: '0 80px', maxWidth: 1100 }}>
      {/* ... todo el resto de tu código queda igual ... */}

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.85, duration: 0.5 }}
        style={{
          marginTop: 48,
          borderRadius: 16,
          overflow: 'hidden',
          border: '1px solid var(--border)',
          background: 'var(--surface)',
          minHeight: 400,
        }}
      >
        {/* 2. Usas la variable directamente en el src */}
        <img
          src={miImagenWebp} 
          alt="Muestra del agente"
          style={{
            width: '100%',
            height: 'auto',
            display: 'block',
            objectFit: 'cover',
          }}
        />
      </motion.div>
    </div>
  )
}