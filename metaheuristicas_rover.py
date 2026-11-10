import random
from modulo_busqueda import BusquedaRover


class MetaheuristicasRover:
    """Optimiza el orden de visita de POIs y el umbral de recarga usando metaheurísticas."""

    def __init__(self, instancia, semilla=42):
        self.instancia = instancia
        self.semilla = semilla
        self.rng = random.Random(semilla)
        self.buscador = BusquedaRover(instancia)
        self.pois = instancia.get("pois_info", [])
        self.pos_poi = {poi["id"]: tuple(poi["pos"]) for poi in self.pois}
        self.zona = tuple(instancia["zona_comunicacion"])

    def _distancia(self, a, b):
        a = tuple(a)
        b = tuple(b)
        camino, costo = self.buscador.buscar_camino_a_estrella(a, b)
        if camino is None:
            return float("inf")
        return costo

    def _valor_poi(self, poi):
        return poi.get("valor", 0) * poi.get("prioridad", 1.0)

    def _score_orden(self, orden):
        """Evalúa un orden de visita: recompensa valor y penaliza distancia y recarga."""
        if not orden:
            return {"costo": 0.0, "puntuacion": 0.0, "exito": False}

        total_coste = 0.0
        puntuacion = 0.0
        pos_actual = tuple(self.instancia["inicio"])

        for poi_id in orden:
            poi = next(p for p in self.pois if p["id"] == poi_id)
            pos_destino = tuple(poi["pos"])
            costo = self._distancia(pos_actual, pos_destino)
            if costo == float("inf"):
                return {"costo": float("inf"), "puntuacion": -1e9, "exito": False}
            total_coste += costo
            puntuacion += self._valor_poi(poi)
            pos_actual = pos_destino

        costo_final = self._distancia(pos_actual, self.zona)
        if costo_final == float("inf"):
            return {"costo": float("inf"), "puntuacion": -1e9, "exito": False}

        total_coste += costo_final
        puntuacion -= 0.5 * total_coste
        return {"costo": total_coste, "puntuacion": puntuacion, "exito": True}

    def _orden_inicial_greedy(self):
        """Construye una solución inicial escogiendo el siguiente POI con mejor relación valor/distancia."""
        orden = []
        pos_actual = tuple(self.instancia["inicio"])
        restantes = [p["id"] for p in self.pois]

        while restantes:
            mejor_poi = None
            mejor_ratio = -float("inf")
            for poi_id in restantes:
                poi = next(p for p in self.pois if p["id"] == poi_id)
                dist = self._distancia(pos_actual, poi["pos"])
                ratio = self._valor_poi(poi) / (dist + 1.0)
                if ratio > mejor_ratio:
                    mejor_ratio = ratio
                    mejor_poi = poi_id

            orden.append(mejor_poi)
            pos_actual = self.pos_poi[mejor_poi]
            restantes.remove(mejor_poi)

        return orden

    def _swap_orden(self, orden):
        """Perfecciona la solución por intercambio local."""
        mejor_orden = list(orden)
        mejor_eval = self._score_orden(mejor_orden)
        mejora = True

        while mejora:
            mejora = False
            for i in range(len(mejor_orden)):
                for j in range(i + 1, len(mejor_orden)):
                    candidato = mejor_orden[:]
                    candidato[i], candidato[j] = candidato[j], candidato[i]
                    eval_cand = self._score_orden(candidato)
                    if eval_cand["puntuacion"] > mejor_eval["puntuacion"]:
                        mejor_orden = candidato
                        mejor_eval = eval_cand
                        mejora = True

        return mejor_orden, mejor_eval

    def _annealing(self, orden, temperatura_inicial=25.0, pasos=200):
        """Simulated annealing para escapar de óptimos locales."""
        mejor_orden = list(orden)
        mejor_eval = self._score_orden(mejor_orden)
        actual = list(orden)
        actual_eval = mejor_eval
        temperatura = temperatura_inicial

        for _ in range(pasos):
            candidato = actual[:]
            i, j = self.rng.sample(range(len(candidato)), 2)
            candidato[i], candidato[j] = candidato[j], candidato[i]
            cand_eval = self._score_orden(candidato)

            delta = cand_eval["puntuacion"] - actual_eval["puntuacion"]
            if delta > 0 or self.rng.random() < min(1.0, __import__('math').exp(delta / temperatura)):
                actual = candidato
                actual_eval = cand_eval

            if actual_eval["puntuacion"] > mejor_eval["puntuacion"]:
                mejor_orden = actual[:]
                mejor_eval = actual_eval

            temperatura *= 0.95

        return mejor_orden, mejor_eval

    def resolver(self, estrategia="annealing"):
        """Resuelve el problema de ordenación de POIs con una estrategia metaheurística."""
        inicial = self._orden_inicial_greedy()

        if estrategia == "greedy":
            orden, eval_ = inicial, self._score_orden(inicial)
        elif estrategia == "hill_climbing":
            orden, eval_ = self._swap_orden(inicial)
        elif estrategia == "annealing":
            orden, eval_ = self._annealing(inicial)
            orden, eval_ = self._swap_orden(orden)
        else:
            raise ValueError(f"Estrategia no soportada: {estrategia}")

        return {"orden": orden, "evaluacion": eval_}

    def comparar_algoritmos(self, estrategias=None):
        """Compara varias metaheurísticas sobre la misma instancia con semilla fija."""
        if estrategias is None:
            estrategias = ["greedy", "hill_climbing", "annealing"]

        resultados = []
        for estrategia in estrategias:
            salida = self.resolver(estrategia)
            resultados.append({
                "estrategia": estrategia,
                "orden": salida["orden"],
                "costo": salida["evaluacion"]["costo"],
                "puntuacion": salida["evaluacion"]["puntuacion"],
                "exito": salida["evaluacion"]["exito"],
            })

        return sorted(resultados, key=lambda x: x["puntuacion"], reverse=True)


if __name__ == "__main__":
    from entorno_gen import GeneradorEntornoRover

    instancia = GeneradorEntornoRover(ancho=8, alto=8, semilla=42).generar_mapa(probabilidad_obstaculos=0.12, num_pois=5)
    optimizador = MetaheuristicasRover(instancia, semilla=42)
    print(optimizador.comparar_algoritmos())
