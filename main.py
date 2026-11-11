import argparse

from entorno_gen import GeneradorEntornoRover
from modulo_busqueda import BusquedaRover
from modelo_rover import RoverAutonomo
from planificador_rover import PlanificadorRover
from metaheuristicas_rover import MetaheuristicasRover
from experimentacion_rover import comparar_experimento, imprimir_resumen


def demo_busqueda():
    generador = GeneradorEntornoRover(ancho=8, alto=8, semilla=123)
    instancia = generador.generar_mapa(probabilidad_obstaculos=0.1, num_pois=2)
    buscador = BusquedaRover(instancia)

    inicio = instancia['inicio']
    objetivo = instancia['pois'][0]
    camino, costo_total_bateria = buscador.buscar_camino_a_estrella(inicio, objetivo)

    print("--- DEMO BÚSQUEDA ---")
    print(f"Inicio: {inicio}")
    print(f"Objetivo: {objetivo}")
    print(f"Camino: {camino}")
    print(f"Costo: {costo_total_bateria}")


def demo_rover():
    instancia = GeneradorEntornoRover(ancho=8, alto=8, semilla=42).generar_mapa(
        probabilidad_obstaculos=0.12,
        num_pois=3,
    )
    rover = RoverAutonomo(instancia)
    print("--- DEMO ROVER ---")
    print(rover.resumen())


def demo_planificador():
    instancia = GeneradorEntornoRover(ancho=8, alto=8, semilla=42).generar_mapa(
        probabilidad_obstaculos=0.12,
        num_pois=3,
    )
    rover = RoverAutonomo(instancia)
    planificador = PlanificadorRover(instancia)
    resultado = planificador.ejecutar_plan(rover)
    print("--- DEMO PLANIFICADOR ---")
    print(resultado)


def demo_metaheuristica():
    instancia = GeneradorEntornoRover(ancho=8, alto=8, semilla=42).generar_mapa(
        probabilidad_obstaculos=0.12,
        num_pois=5,
    )
    optimizador = MetaheuristicasRover(instancia, semilla=42)
    print("--- DEMO METAHEURÍSTICA ---")
    print(optimizador.comparar_algoritmos())


def demo_experimentacion():
    print("--- DEMO EXPERIMENTACIÓN ---")
    experimento = comparar_experimento(
        seeds=list(range(10, 31)),
        ancho=8,
        alto=8,
        num_pois=5,
        probabilidad_obstaculos=0.12,
    )
    imprimir_resumen(experimento)


def demo_todo():
    demo_busqueda()
    demo_rover()
    demo_planificador()
    demo_metaheuristica()
    demo_experimentacion()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proyecto Rover autónomo")
    parser.add_argument("--demo", choices=["busqueda", "rover", "planificador", "metaheuristica", "experimentacion", "todo"], default="todo")
    args = parser.parse_args()

    if args.demo == "busqueda":
        demo_busqueda()
    elif args.demo == "rover":
        demo_rover()
    elif args.demo == "planificador":
        demo_planificador()
    elif args.demo == "metaheuristica":
        demo_metaheuristica()
    elif args.demo == "experimentacion":
        demo_experimentacion()
    else:
        demo_todo()