# Práctica 2 — Selección de plataforma y benchmark de LLMs

Práctica de análisis (sin servicio ejecutable). Compara alternativas de plataforma
para el despliegue del proyecto final mediante una matriz de decisión y documenta un
benchmark de modelos locales en Ollama con datos reales de terminal.

## Contenido

Dos partes:

1. **Matriz de decisión**: evaluación de plataformas (PC local CPU/GPU, API en la nube,
   servidor GPU en la nube, Jetson embebido, microcontrolador + API) según costo,
   latencia, privacidad, implementación y escalabilidad.
2. **Benchmark de modelos**: 100 ciclos por modelo con un prompt fijo y `num_predict=50`,
   midiendo tiempo promedio, mínimo, máximo, tokens de entrada/salida y tokens/s.

## Estructura

```
practica-2/
├── practica_2.md   # Reporte: matriz de decisión + benchmark y análisis
└── anexos/         # Evidencia y datos que respaldan el reporte
    ├── benchmark_modelos_detallado.csv
    ├── variacion_parametros_qwen.csv
    ├── comparacion_modelos.png
    ├── comparativa_latencia_modelos.png
    ├── variacion_modelos.png
    └── graficas_variacion_parametros_limpias.png
```

## Modelos evaluados

| Modelo | Tiempo promedio (s) | Tokens/s |
|--------|--------------------:|---------:|
| `tinyllama:1.1b-chat-v1-q8_0` | 2.618 | 129.40 |
| `llama3.2:3b` | 4.437 | 28.45 |
| `qwen2.5:7b` | 6.492 | 13.24 |

Valores reales de terminal (promedio de 100 ciclos por modelo). El detalle y las
gráficas están en `anexos/`.

## Reporte

El reporte completo es `practica_2.md`, publicado también en el sitio del proyecto
(GitHub Pages) como la página "Práctica 2".
