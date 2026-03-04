"""
analysis.py  –  Ejecuta todos los escenarios pedidos en la guía
"""
from simulation import correr_simulacion

PROCESOS   = [25, 50, 100, 150, 200]
INTERVALOS = [10, 5, 1]

def encabezado(titulo):
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")
    print(f"{'Procesos':>10} {'Intervalo':>10} {'Promedio':>12} {'Std Dev':>12}")
    print(f"{'-'*46}")

def tabla(resultados):
    for n, iv, prom, std in resultados:
        print(f"{n:>10} {iv:>10} {prom:>12.2f} {std:>12.2f}")

# ── TAREA 1 & 2: baseline con intervalos 10, 5, 1 ──────────────────────────
encabezado("BASELINE  (RAM=100, 1 CPU, 3 inst/ciclo)")
baseline = []
for iv in INTERVALOS:
    for n in PROCESOS:
        prom, std = correr_simulacion(n, intervalo=iv)
        baseline.append((n, iv, prom, std))
        print(f"{n:>10} {iv:>10} {prom:>12.2f} {std:>12.2f}")

# ── TAREA 3a: más RAM ───────────────────────────────────────────────────────
encabezado("3a: RAM=200, 1 CPU, 3 inst/ciclo")
ram200 = []
for iv in INTERVALOS:
    for n in PROCESOS:
        prom, std = correr_simulacion(n, intervalo=iv, ram=200)
        ram200.append((n, iv, prom, std))
        print(f"{n:>10} {iv:>10} {prom:>12.2f} {std:>12.2f}")

# ── TAREA 3b: CPU más rápido ────────────────────────────────────────────────
encabezado("3b: RAM=100, 1 CPU rápido (6 inst/ciclo)")
cpu_rapido = []
for iv in INTERVALOS:
    for n in PROCESOS:
        prom, std = correr_simulacion(n, intervalo=iv, inst_ciclo=6)
        cpu_rapido.append((n, iv, prom, std))
        print(f"{n:>10} {iv:>10} {prom:>12.2f} {std:>12.2f}")

# ── TAREA 3c: 2 CPUs ────────────────────────────────────────────────────────
encabezado("3c: RAM=100, 2 CPUs, 3 inst/ciclo")
dos_cpus = []
for iv in INTERVALOS:
    for n in PROCESOS:
        prom, std = correr_simulacion(n, intervalo=iv, cpus=2)
        dos_cpus.append((n, iv, prom, std))
        print(f"{n:>10} {iv:>10} {prom:>12.2f} {std:>12.2f}")

# Exportar para plots.py
data = {
    "baseline":   baseline,
    "ram200":     ram200,
    "cpu_rapido": cpu_rapido,
    "dos_cpus":   dos_cpus,
}

import json, pathlib
pathlib.Path("resultados.json").write_text(json.dumps(data))
print("\n Resultados guardados en resultados.json")