import statistics
from time import perf_counter

from entorno_gen import GeneradorEntornoRover
from metaheuristicas_rover import MetaheuristicasRover

ESTRATEGIAS = ["greedy", "hill_climbing", "annealing"]


def ejecutar_una_instancia(seed, ancho=8, alto=8, num_pois=5, probabilidad_obstaculos=0.12):
    """Evalúa todas las estrategias sobre una instancia concreta."""
    instancia = GeneradorEntornoRover(
        ancho=ancho,
        alto=alto,
        semilla=seed,
    ).generar_mapa(
        probabilidad_obstaculos=probabilidad_obstaculos,
        num_pois=num_pois,
    )

    resultados = {}
    for estrategia in ESTRATEGIAS:
        t0 = perf_counter()
        optimizador = MetaheuristicasRover(instancia, semilla=seed)
        salida = optimizador.resolver(estrategia)
        tiempo = perf_counter() - t0
        resultados[estrategia] = {
            "orden": salida["orden"],
            "costo": salida["evaluacion"]["costo"],
            "puntuacion": salida["evaluacion"]["puntuacion"],
            "exito": salida["evaluacion"]["exito"],
            "tiempo": tiempo,
        }

    return instancia, resultados


def comparar_experimento(seeds=None, ancho=8, alto=8, num_pois=5, probabilidad_obstaculos=0.12):
    """Compara las estrategias sobre varias semillas y devuelve media y dispersión."""
    if seeds is None:
        seeds = list(range(10, 41))

    resumen = {estrategia: {"coste": [], "puntuacion": [], "tiempo": []} for estrategia in ESTRATEGIAS}
    detalle_por_semilla = []

    for seed in seeds:
        _, resultados = ejecutar_una_instancia(
            seed=seed,
            ancho=ancho,
            alto=alto,
            num_pois=num_pois,
            probabilidad_obstaculos=probabilidad_obstaculos,
        )

        fila = {"semilla": seed}
        for estrategia in ESTRATEGIAS:
            fila[f"{estrategia}_costo"] = resultados[estrategia]["costo"]
            fila[f"{estrategia}_puntuacion"] = resultados[estrategia]["puntuacion"]
            fila[f"{estrategia}_tiempo"] = resultados[estrategia]["tiempo"]
            fila[f"{estrategia}_exito"] = resultados[estrategia]["exito"]

            resumen[estrategia]["coste"].append(resultados[estrategia]["costo"])
            resumen[estrategia]["puntuacion"].append(resultados[estrategia]["puntuacion"])
            resumen[estrategia]["tiempo"].append(resultados[estrategia]["tiempo"])

        detalle_por_semilla.append(fila)

    resumen_final = {}
    for estrategia in ESTRATEGIAS:
        resumen_final[estrategia] = {
            "media_coste": statistics.mean(resumen[estrategia]["coste"]),
            "std_coste": statistics.pstdev(resumen[estrategia]["coste"]),
            "media_puntuacion": statistics.mean(resumen[estrategia]["puntuacion"]),
            "std_puntuacion": statistics.pstdev(resumen[estrategia]["puntuacion"]),
            "media_tiempo": statistics.mean(resumen[estrategia]["tiempo"]),
            "std_tiempo": statistics.pstdev(resumen[estrategia]["tiempo"]),
        }

    return {
        "seeds": seeds,
        "detalle": detalle_por_semilla,
        "resumen": resumen_final,
    }


def imprimir_resumen(experimento):
    print("=== RESUMEN EXPERIMENTAL ===")
    print(f"Semillas evaluadas: {experimento['seeds']}")
    print()
    for estrategia in ESTRATEGIAS:
        datos = experimento["resumen"][estrategia]
        print(f"Estrategia: {estrategia}")
        print(f"  costo medio: {datos['media_coste']:.3f} ± {datos['std_coste']:.3f}")
        print(f"  puntuación media: {datos['media_puntuacion']:.3f} ± {datos['std_puntuacion']:.3f}")
        print(f"  tiempo medio: {datos['media_tiempo']:.6f} s ± {datos['std_tiempo']:.6f} s")
        print()


if __name__ == "__main__":
    experimento = comparar_experimento(
        seeds=list(range(10, 31)),
        ancho=8,
        alto=8,
        num_pois=5,
        probabilidad_obstaculos=0.12,
    )
    imprimir_resumen(experimento)
    print("Detalle por semilla:")
    for fila in experimento["detalle"]:
        print(fila)
