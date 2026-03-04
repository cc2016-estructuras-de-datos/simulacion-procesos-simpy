"""
simulation.py  –  Núcleo DES del sistema operativo con SimPy
"""
import simpy, random, statistics

RANDOM_SEED           = 42
RAM_CAPACITY          = 100
CPU_CAPACITY          = 1
INSTRUCTIONS_PER_UNIT = 3
IO_WAIT_MAX           = 5
INTERVAL              = 10


def proceso(env, pid, RAM, CPU, inst_por_ciclo, resultados):
    llegada = env.now

    # NEW: pedir memoria
    memoria = random.randint(1, 10)
    yield RAM.get(memoria)

    # READY → RUNNING loop
    instrucciones = random.randint(1, 10)

    while instrucciones > 0:
        with CPU.request() as req:
            yield req                                    # esperar CPU
            ejecutadas = min(inst_por_ciclo, instrucciones)
            yield env.timeout(ejecutadas / inst_por_ciclo)  # libera CPU anticipadamente si ejecutadas < inst_por_ciclo
            instrucciones -= ejecutadas

        if instrucciones == 0:
            break                                        # → TERMINATED

        evento = random.randint(1, 21)
        if evento == 1:                                  # → WAITING
            yield env.timeout(random.randint(1, IO_WAIT_MAX))
        # evento 2-21 → READY directamente (continúa while)

    # TERMINATED: liberar memoria
    yield RAM.put(memoria)
    resultados.append(env.now - llegada)


def generador_procesos(env, n, RAM, CPU, inst_por_ciclo, intervalo, resultados):
    for pid in range(n):
        env.process(proceso(env, pid, RAM, CPU, inst_por_ciclo, resultados))
        yield env.timeout(random.expovariate(1.0 / intervalo))


def correr_simulacion(n_procesos, intervalo=INTERVAL, ram=RAM_CAPACITY,
                      cpus=CPU_CAPACITY, inst_ciclo=INSTRUCTIONS_PER_UNIT,
                      seed=RANDOM_SEED):
    random.seed(seed)
    env = simpy.Environment()
    RAM = simpy.Container(env, init=ram, capacity=ram)
    CPU = simpy.Resource(env, capacity=cpus)
    resultados = []
    env.process(generador_procesos(env, n_procesos, RAM, CPU,
                                   inst_ciclo, intervalo, resultados))
    env.run()
    prom = statistics.mean(resultados)
    std  = statistics.stdev(resultados) if len(resultados) > 1 else 0.0
    return prom, std