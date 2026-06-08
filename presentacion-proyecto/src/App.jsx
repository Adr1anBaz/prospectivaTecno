import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'
import IntroSlide from './slides/IntroSlide'
import VoiceControlSlide from './slides/VoiceControlSlide'
import ArchitectureSlide from './slides/ArchitectureSlide'
import TelemetrySlide from './slides/TelemetrySlide'
import ROS2SLAMSlide from './slides/ROS2SLAMSlide'
import ChallengesSlide from './slides/ChallengesSlide'
import DemoSlide from './slides/DemoSlide'
import FutureSlide from './slides/FutureSlide'

const slides = [
  { id: 0, component: IntroSlide, title: 'Introducción' },
  { id: 1, component: VoiceControlSlide, title: 'Control por Voz' },
  { id: 2, component: ArchitectureSlide, title: 'Arquitectura' },
  { id: 3, component: TelemetrySlide, title: 'Telemetría' },
  { id: 4, component: ROS2SLAMSlide, title: 'ROS2 & SLAM' },
  { id: 5, component: ChallengesSlide, title: 'Desafíos' },
  { id: 6, component: DemoSlide, title: 'Demo' },
  { id: 7, component: FutureSlide, title: 'Próximos Pasos' },
]

function App() {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [direction, setDirection] = useState(1)

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        nextSlide()
      } else if (e.key === 'ArrowLeft') {
        prevSlide()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [currentSlide])

  const nextSlide = () => {
    if (currentSlide < slides.length - 1) {
      setDirection(1)
      setCurrentSlide(currentSlide + 1)
    }
  }

  const prevSlide = () => {
    if (currentSlide > 0) {
      setDirection(-1)
      setCurrentSlide(currentSlide - 1)
    }
  }

  const goToSlide = (index) => {
    setDirection(index > currentSlide ? 1 : -1)
    setCurrentSlide(index)
  }

  const CurrentSlideComponent = slides[currentSlide].component

  const slideVariants = {
    enter: (direction) => ({
      x: direction > 0 ? 1000 : -1000,
      opacity: 0
    }),
    center: {
      x: 0,
      opacity: 1
    },
    exit: (direction) => ({
      x: direction < 0 ? 1000 : -1000,
      opacity: 0
    })
  }

  return (
    <div className="app">
      <AnimatePresence mode="wait" custom={direction}>
        <motion.div
          key={currentSlide}
          custom={direction}
          variants={slideVariants}
          initial="enter"
          animate="center"
          exit="exit"
          transition={{
            x: { type: "spring", stiffness: 300, damping: 30 },
            opacity: { duration: 0.2 }
          }}
          className="slide-container"
        >
          <CurrentSlideComponent />
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div className="navigation">
        <button
          onClick={prevSlide}
          disabled={currentSlide === 0}
          className="nav-button"
        >
          ← Anterior
        </button>

        <div className="slide-indicators">
          {slides.map((slide, index) => (
            <button
              key={slide.id}
              onClick={() => goToSlide(index)}
              className={`indicator ${index === currentSlide ? 'active' : ''}`}
              title={slide.title}
            />
          ))}
        </div>

        <button
          onClick={nextSlide}
          disabled={currentSlide === slides.length - 1}
          className="nav-button"
        >
          Siguiente →
        </button>
      </div>

      {/* Slide Counter */}
      <div className="slide-counter">
        {currentSlide + 1} / {slides.length}
      </div>

      {/* Instructions */}
      {currentSlide === 0 && (
        <motion.div
          className="instructions"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
        >
          Usa las flechas del teclado o haz clic para navegar
        </motion.div>
      )}
    </div>
  )
}

export default App
