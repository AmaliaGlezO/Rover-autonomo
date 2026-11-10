from modelo_rover import RoverAutonomo


class PlanificadorRover:
    """Genera un plan de alto nivel para una misión del rover."""

    def __init__(self, instancia):
        self.instancia = instancia
        self.orden_pois = sorted(
            instancia.get("pois_info", []),
            key=lambda poi: (-poi.get("prioridad", 1.0), -poi.get("valor", 0))
        )

    def _estacion_mas_cercana(self, rover):
        estaciones = rover.instancia.get("estaciones_recarga", [rover.base])
        mejor_estacion = None
        mejor_coste = float("inf")

        for estacion in estaciones:
            camino, coste = rover.buscador.buscar_camino_a_estrella(rover.posicion, tuple(estacion))
            if camino is not None and coste < mejor_coste:
                mejor_coste = coste
                mejor_estacion = tuple(estacion)

        return mejor_estacion

    def generar_plan_alto_nivel(self):
        """Crea una secuencia de acciones de alto nivel para visitar los POIs y transmitir."""
        plan = []

        for poi in self.orden_pois:
            plan.append({"accion": "mover", "destino": tuple(poi["pos"])})
            plan.append({"accion": "recoger", "poi_id": poi["id"]})
            plan.append({"accion": "analizar", "poi_id": poi["id"]})

        plan.append({"accion": "mover", "destino": tuple(self.instancia["zona_comunicacion"])})
        plan.append({"accion": "transmitir"})
        return plan

    def ejecutar_plan(self, rover):
        """Ejecuta el plan alto nivel sobre un rover concreto usando las acciones del modelo."""
        for paso in self.generar_plan_alto_nivel():
            accion = paso["accion"]

            if rover.bateria < 8:
                estacion = self._estacion_mas_cercana(rover)
                if estacion is not None and estacion != rover.posicion:
                    rover.mover_a(estacion)
                rover.recargar()

            if accion == "mover":
                destino = paso["destino"]
                try:
                    rover.mover_a(destino)
                except ValueError:
                    estacion = self._estacion_mas_cercana(rover)
                    if estacion is not None and estacion != rover.posicion:
                        rover.mover_a(estacion)
                    rover.recargar()
                    rover.mover_a(destino)
            elif accion == "recoger":
                rover.recoger_datos(paso["poi_id"])
            elif accion == "analizar":
                rover.analizar(paso["poi_id"])
            elif accion == "transmitir":
                rover.transmitir()

        return rover.resumen()


if __name__ == "__main__":
    from entorno_gen import GeneradorEntornoRover

    instancia = GeneradorEntornoRover(ancho=8, alto=8, semilla=42).generar_mapa(probabilidad_obstaculos=0.12, num_pois=3)
    rover = RoverAutonomo(instancia)
    planificador = PlanificadorRover(instancia)
    plan = planificador.generar_plan_alto_nivel()
    print("Plan de alto nivel:")
    for i, paso in enumerate(plan, 1):
        print(i, paso)
    print("\nEjecución:")
    print(planificador.ejecutar_plan(rover))
