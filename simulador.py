from entorno_gen import GeneradorEntornoRover
from modelo_rover import RoverAutonomo
from planificador_rover import PlanificadorRover

if __name__ == "__main__":
    instancia = GeneradorEntornoRover(ancho=8, alto=8, semilla=42).generar_mapa(
        probabilidad_obstaculos=0.12,
        num_pois=3,
    )

    rover = RoverAutonomo(instancia)
    planificador = PlanificadorRover(instancia)

    plan = planificador.generar_plan_alto_nivel()
    resultado = planificador.ejecutar_plan(rover)

    print("Plan de alto nivel:")
    for i, paso in enumerate(plan, 1):
        print(f"{i}. {paso}")

    print("\nResultado de la ejecución:")
    print(resultado)