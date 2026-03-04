"""
plots.py  –  Genera las gráficas pedidas en la guía
"""
import json, matplotlib.pyplot as plt, matplotlib.ticker as ticker

data       = json.load(open("resultados.json"))
PROCESOS   = [25, 50, 100, 150, 200]
INTERVALOS = [10, 5, 1]
COLORES    = {10: "#2196F3", 5: "#FF9800", 1: "#F44336"}
LABELS_IV  = {10: "Intervalo 10 (normal)", 5: "Intervalo 5 (rápido)", 1: "Intervalo 1 (alta carga)"}


def extraer(dataset, intervalo):
    """Filtra un dataset por intervalo y devuelve (promedios, stds)."""
    filas = [(n, p, s) for n, iv, p, s in dataset if iv == intervalo]
    filas.sort()
    promedios = [p for _, p, _ in filas]
    stds      = [s for _, _, s in filas]
    return promedios, stds


def grafica_escenario(dataset, titulo, filename):
    """Una figura con 3 líneas (una por intervalo) + barras de error."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for iv in INTERVALOS:
        proms, stds = extraer(dataset, iv)
        ax.errorbar(PROCESOS, proms, yerr=stds,
                    label=LABELS_IV[iv], color=COLORES[iv],
                    marker="o", linewidth=2, capsize=4)
    ax.set_title(titulo, fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de procesos")
    ax.set_ylabel("Tiempo promedio en sistema")
    ax.legend()
    ax.xaxis.set_major_locator(ticker.FixedLocator(PROCESOS))
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)
    print(f" {filename}")


def grafica_comparativa(intervalo):
    """Compara las 4 estrategias para un intervalo dado."""
    fig, ax = plt.subplots(figsize=(9, 5))
    escenarios = [
        ("baseline",   "#607D8B", "Baseline (RAM=100, 1CPU, 3inst)"),
        ("ram200",     "#4CAF50", "RAM=200"),
        ("cpu_rapido", "#9C27B0", "CPU rápido (6 inst/ciclo)"),
        ("dos_cpus",   "#FF5722", "2 CPUs"),
    ]
    for key, color, label in escenarios:
        proms, stds = extraer(data[key], intervalo)
        ax.plot(PROCESOS, proms, label=label, color=color, marker="o", linewidth=2)

    ax.set_title(f"Comparación de estrategias — Intervalo {intervalo}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Número de procesos")
    ax.set_ylabel("Tiempo promedio en sistema")
    ax.legend()
    ax.xaxis.set_major_locator(ticker.FixedLocator(PROCESOS))
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    fname = f"comparativa_iv{intervalo}.png"
    fig.savefig(fname, dpi=150)
    plt.close(fig)
    print(f" {fname}")


print("\n Generando gráficas...")

# Tarea 1 & 2: baseline por intervalo
grafica_escenario(data["baseline"],   "Baseline – Tiempo promedio por nº de procesos",  "t1_baseline.png")

# Tarea 3: una por escenario
grafica_escenario(data["ram200"],     "3a: RAM=200 – Tiempo promedio",                   "t3a_ram200.png")
grafica_escenario(data["cpu_rapido"], "3b: CPU rápido (6 inst) – Tiempo promedio",       "t3b_cpu_rapido.png")
grafica_escenario(data["dos_cpus"],   "3c: 2 CPUs – Tiempo promedio",                    "t3c_dos_cpus.png")

# Tarea 4: comparativa por intervalo
for iv in INTERVALOS:
    grafica_comparativa(iv)

print("\n Todas las gráficas generadas.")