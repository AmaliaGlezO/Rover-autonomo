from modulo_busqueda import BusquedaRover


class RoverAutonomo:
    """Modelo operativo del rover con recursos, objetivos y comunicación."""

    def __init__(self, instancia):
        self.instancia = instancia
        self.posicion = instancia["inicio"]
        self.base = instancia["inicio"]
        self.bateria = instancia.get("bateria_inicial", 50)
        self.bateria_maxima = instancia.get("bateria_max", self.bateria)
        self.memoria = instancia.get("memoria_inicial", 20)
        self.memoria_maxima = instancia.get("memoria_max", self.memoria)
        self.tiempo = 0
        self.puntuacion = 0
        self.transmitidos = set()
        self.buscador = BusquedaRover(instancia)

        self.pois = {}
        for poi in instancia.get("pois_info", []):
            self.pois[poi["id"]] = {
                "id": poi["id"],
                "pos": poi["pos"],
                "valor": poi.get("valor", 20),
                "datos": poi.get("datos", 5),
                "prioridad": poi.get("prioridad", 1.0),
                "estado": "pendiente",
            }

    def _coste_movimiento(self, destino):
        camino, coste = self.buscador.buscar_camino_a_estrella(self.posicion, destino)
        if camino is None:
            return None, float("inf")
        return camino, coste

    def mover_a(self, destino):
        """Mueve el rover por el mapa siguiendo una ruta costada."""
        camino, coste = self._coste_movimiento(destino)
        if camino is None:
            raise ValueError(f"No existe ruta desde {self.posicion} hasta {destino}.")

        if costes := self.bateria - coste:
            pass

        self.bateria = max(0, self.bateria - coste)
        self.tiempo += 1 + len(camino)
        self.posicion = destino
        return camino, coste

    def recoger_datos(self, poi_id):
        """Recoge una muestra en el POI actual."""
        poi = self.pois.get(poi_id)
        if poi is None:
            return False
        if poi["estado"] != "pendiente":
            return False
        if self.posicion != poi["pos"]:
            return False
        if self.memoria < poi["datos"]:
            return False

        self.memoria -= poi["datos"]
        self.puntuacion += poi["valor"]
        poi["estado"] = "recogido"
        self.tiempo += 2
        return True

    def analizar(self, poi_id):
        """Analiza un POI ya recogido usando batería y memoria."""
        poi = self.pois.get(poi_id)
        if poi is None:
            return False
        if poi["estado"] != "recogido":
            return False

        coste_analisis = self.instancia.get("coste_analisis", 4)
        memoria_analisis = self.instancia.get("memoria_analisis", 2)

        if self.bateria < coste_analisis or self.memoria < memoria_analisis:
            return False

        self.bateria -= coste_analisis
        self.memoria -= memoria_analisis
        poi["estado"] = "analizado"
        self.puntuacion += int(poi["valor"] * 0.5)
        self.tiempo += 3
        return True

    def recargar(self):
        """Recarga batería desde la base o desde una estación de recarga."""
        if self.posicion not in self.instancia.get("estaciones_recarga", [self.base]):
            return False

        recarga = self.instancia.get("recarga_por_ciclo", 25)
        self.bateria = min(self.bateria_maxima, self.bateria + recarga)
        self.tiempo += 2
        return True

    def transmitir(self):
        """Transmite todos los POIs analizados que estén en una zona de comunicación."""
        if self.posicion not in self.instancia.get("zonas_comunicacion", []):
            return 0

        transmitidos_hoy = 0
        memoria_tx = self.instancia.get("memoria_transmision", 1)

        for poi_id, poi in self.pois.items():
            if poi["estado"] != "analizado" or poi_id in self.transmitidos:
                continue
            if self.memoria < memoria_tx:
                continue

            self.memoria -= memoria_tx
            self.puntuacion += int(poi["valor"] * 0.75)
            self.transmitidos.add(poi_id)
            transmitidos_hoy += 1
            self.tiempo += 2

        return transmitidos_hoy

    def ir_a_zona_comunicacion_mas_cercana(self):
        """Mueve al rover a la zona de comunicación más cercana."""
        mejor_zona = None
        mejor_coste = float("inf")
        mejor_camino = None

        for zona in self.instancia.get("zonas_comunicacion", []):
            camino, coste = self._coste_movimiento(zona)
            if camino is not None and coste < mejor_coste:
                mejor_coste = coste
                mejor_zona = zona
                mejor_camino = camino

        if mejor_zona is None:
            return None, float("inf")

        if mejor_zona != self.posicion:
            self.mover_a(mejor_zona)
        return mejor_camino, mejor_coste

    def mision_completada(self):
        if not self.pois:
            return False
        return all(poi["estado"] == "analizado" for poi in self.pois.values()) and len(self.transmitidos) == len(self.pois)

    def resumen(self):
        return {
            "posicion": self.posicion,
            "bateria": self.bateria,
            "memoria": self.memoria,
            "tiempo": self.tiempo,
            "puntuacion": self.puntuacion,
            "misiones": {poi_id: info["estado"] for poi_id, info in self.pois.items()},
            "transmitidos": sorted(self.transmitidos),
            "completada": self.mision_completada(),
        }
