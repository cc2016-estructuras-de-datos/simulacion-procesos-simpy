# Hoja de Trabajo 5 — Simulación de Procesos con SimPy

Simulación DES (Discrete Event Simulation) de un sistema operativo de tiempo compartido, implementada con el módulo **SimPy** de Python. Modela el ciclo de vida completo de procesos: `new → ready → running → waiting/terminated`.

## Estructura del proyecto

```
├── simulation.py      # Núcleo de la simulación (lógica DES)
├── analysis.py        # Ejecuta todos los escenarios y exporta resultados
├── plots.py           # Genera las gráficas a partir de resultados.json
├── resultados.json    # Datos generados por analysis.py
├── t1_baseline.png         # Gráfica tarea 1 & 2: baseline (intervalos 10, 5, 1)
├── t3a_ram200.png          # Gráfica tarea 3a: RAM=200
├── t3b_cpu_rapido.png      # Gráfica tarea 3b: CPU 6 inst/ciclo
├── t3c_dos_cpus.png        # Gráfica tarea 3c: 2 CPUs
├── comparativa_iv10.png    # Gráfica tarea 4: comparación estrategias (intervalo 10)
├── comparativa_iv5.png     # Gráfica tarea 4: comparación estrategias (intervalo 5)
└── comparativa_iv1.png     # Gráfica tarea 4: comparación estrategias (intervalo 1)
```

## Modelo de simulación

### Ciclo de vida del proceso

```
new ──► ready ──► running ──► terminated
                    │   ▲         (instrucciones = 0)
                    │   │
                    ▼   │  (evento = 2–21)
                  waiting
                 (evento = 1, I/O)
```

| Estado | Descripción |
|--------|-------------|
| **new** | El proceso llega y solicita memoria RAM (entero aleatorio 1–10). Hace cola si no hay disponible. |
| **ready** | Espera turno de CPU. Tiene un contador de instrucciones totales (entero aleatorio 1–10). |
| **running** | El CPU atiende al proceso. Ejecuta hasta 3 instrucciones por unidad de tiempo. Si quedan menos de 3, libera el CPU anticipadamente. |
| **waiting** | Ocurre cuando el evento post-CPU es 1 (de 1–21). El proceso espera operaciones de I/O antes de volver a ready. |
| **terminated** | El proceso termina cuando llega a 0 instrucciones. Libera su memoria RAM. |

### Parámetros configurables

| Constante | Valor por defecto | Descripción |
|-----------|:-----------------:|-------------|
| `RANDOM_SEED` | `42` | Semilla para reproducibilidad |
| `RAM_CAPACITY` | `100` | Memoria RAM total disponible |
| `CPU_CAPACITY` | `1` | Número de CPUs |
| `INSTRUCTIONS_PER_UNIT` | `3` | Instrucciones ejecutadas por unidad de tiempo |
| `IO_WAIT_MAX` | `5` | Tiempo máximo de espera en I/O (uniforme 1–5) |
| `INTERVAL` | `10` | Intervalo medio de llegada de procesos (distribución exponencial) |

## Requisitos

```
simpy
matplotlib
```

Instalar con:

```bash
pip install simpy matplotlib
```

## Cómo ejecutar

**1. Correr todos los escenarios y guardar resultados:**

```bash
python analysis.py
```

Imprime tablas con promedio y desviación estándar para cada combinación de (n_procesos, intervalo, escenario) y genera `resultados.json`.

**2. Generar las gráficas:**

```bash
python plots.py
```

Requiere que `resultados.json` exista (generado en el paso anterior).

## Escenarios evaluados

| Tarea | Escenario | RAM | CPUs | Inst/ciclo |
|-------|-----------|:---:|:----:|:----------:|
| 1 & 2 | Baseline | 100 | 1 | 3 |
| 3a | Más memoria | 200 | 1 | 3 |
| 3b | CPU más rápido | 100 | 1 | 6 |
| 3c | Dos procesadores | 100 | 2 | 3 |

Todos los escenarios se prueban con **25, 50, 100, 150 y 200 procesos** y con intervalos de llegada de **10, 5 y 1**.

## Uso de la API de simulación

La función `correr_simulacion` puede invocarse de forma independiente:

```python
from simulation import correr_simulacion

promedio, std_dev = correr_simulacion(
    n_procesos=100,
    intervalo=10,   # intervalo medio de llegada
    ram=100,        # capacidad RAM
    cpus=1,         # número de CPUs
    inst_ciclo=3,   # instrucciones por unidad de tiempo
    seed=42
)
print(f"Promedio: {promedio:.2f}  |  Desviación estándar: {std_dev:.2f}")
```

---

Universidad del Valle de Guatemala — Estructuras de Datos — 2025
