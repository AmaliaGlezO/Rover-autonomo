import heapq
import time
from collections import deque


class BusquedaRover:
    def __init__(self, instancia_mapa):
        """
        Recibe el diccionario de la instancia generada por el entorno anterior.
        """
        self.mapa = instancia_mapa["mapa"]
        self.costos = instancia_mapa["costos"]
        self.alto = instancia_mapa["alto"]
        self.ancho = instancia_mapa["ancho"]

    def _obtener_vecinos(self, pos):
        """
        Función de ACCIONES y MODELO DE TRANSICIÓN:
        Devuelve las casillas vecinas válidas (Arriba, Abajo, Izquierda, Derecha)
        y el costo de moverse hacia ellas según el tipo de terreno.
        """
        y, x = pos
        movimientos = [
            (-1, 0, "Arriba"),
            (1, 0, "Abajo"),
            (0, -1, "Izquierda"),
            (0, 1, "Derecha"),
        ]

        vecinos = []
        for dy, dx, accion in movimientos:
            ny, nx = y + dy, x + dx

            if 0 <= ny < self.alto and 0 <= nx < self.ancho:
                tipo_terreno = self.mapa[ny, nx]
                costo_movimiento = self.costos[tipo_terreno]

                if costo_movimiento != float('inf'):
                    vecinos.append(((ny, nx), costo_movimiento, accion))

        return vecinos

    def _heuristica_manhattan(self, pos_actual, pos_meta):
        """
        Distancia Manhattan para una cuadrícula 4-direccional.
        """
        y1, x1 = pos_actual
        y2, x2 = pos_meta
        return abs(y1 - y2) + abs(x1 - x2)

    def _reconstruir_camino(self, padres, nodo_final):
        camino = []
        actual = nodo_final
        while actual is not None:
            camino.append(actual)
            actual = padres.get(actual)
        return list(reversed(camino))

    def _coste_camino(self, camino):
        if camino is None or len(camino) < 2:
            return 0.0

        total = 0.0
        for (y1, x1), (y2, x2) in zip(camino[:-1], camino[1:]):
            tipo_terreno = self.mapa[y2][x2]
            total += self.costos[tipo_terreno]
        return total

    def _buscar_bfs_detallado(self, inicio, meta):
        """
        BFS con coste unitario: explora por niveles y cuenta los nodos expandidos.
        """
        if inicio == meta:
            return [inicio], 0.0, 1

        cola = deque([inicio])
        padres = {inicio: None}
        visitados = {inicio}
        nodos_expandidos = 0

        while cola:
            nodo_actual = cola.popleft()
            nodos_expandidos += 1

            for vecino, _, _ in self._obtener_vecinos(nodo_actual):
                if vecino in visitados:
                    continue
                visitados.add(vecino)
                padres[vecino] = nodo_actual

                if vecino == meta:
                    camino = self._reconstruir_camino(padres, vecino)
                    return camino, self._coste_camino(camino), nodos_expandidos

                cola.append(vecino)

        return None, float('inf'), nodos_expandidos

    def buscar_camino_bfs(self, inicio, meta):
        """
        Version pública de BFS compatible con la API existente.
        """
        camino, costo, _ = self._buscar_bfs_detallado(inicio, meta)
        return camino, costo

    def _buscar_dijkstra_detallado(self, inicio, meta):
        """
        Dijkstra: algoritmo de coste uniforme, óptimo para costes no negativos.
        Devuelve camino, costo total y nodos expandidos.
        """
        if inicio == meta:
            return [inicio], 0.0, 1

        frontera = []
        heapq.heappush(frontera, (0.0, inicio))
        distancia = {inicio: 0.0}
        padres = {inicio: None}
        nodos_expandidos = 0

        while frontera:
            costo_actual, nodo_actual = heapq.heappop(frontera)
            nodos_expandidos += 1

            if costo_actual > distancia.get(nodo_actual, float('inf')):
                continue

            if nodo_actual == meta:
                camino = self._reconstruir_camino(padres, meta)
                return camino, distancia[meta], nodos_expandidos

            for vecino, costo_accion, _ in self._obtener_vecinos(nodo_actual):
                nuevo_coste = costo_actual + costo_accion
                if nuevo_coste < distancia.get(vecino, float('inf')):
                    distancia[vecino] = nuevo_coste
                    padres[vecino] = nodo_actual
                    heapq.heappush(frontera, (nuevo_coste, vecino))

        return None, float('inf'), nodos_expandidos

    def buscar_camino_dijkstra(self, inicio, meta):
        """
        Versión pública de Dijkstra compatible con la API antigua.
        """
        camino, costo, _ = self._buscar_dijkstra_detallado(inicio, meta)
        return camino, costo

    def _buscar_astar_detallado(self, inicio, meta):
        """
        Implementa A* con la heurística Manhattan y contabiliza nodos expandidos.
        """
        if inicio == meta:
            return [inicio], 0.0, 1

        frontera = []
        g_inicial = 0.0
        h_inicial = self._heuristica_manhattan(inicio, meta)
        f_inicial = g_inicial + h_inicial
        heapq.heappush(frontera, (f_inicial, g_inicial, inicio, [inicio]))

        costos_g_conocidos = {inicio: 0.0}
        nodos_expandidos = 0

        while frontera:
            f_n, g_n, nodo_actual, camino = heapq.heappop(frontera)
            nodos_expandidos += 1

            if nodo_actual == meta:
                return camino, g_n, nodos_expandidos

            if g_n > costos_g_conocidos.get(nodo_actual, float('inf')):
                continue

            for sucesor, costo_accion, accion in self._obtener_vecinos(nodo_actual):
                nuevo_g = g_n + costo_accion

                if sucesor not in costos_g_conocidos or nuevo_g < costos_g_conocidos[sucesor]:
                    costos_g_conocidos[sucesor] = nuevo_g
                    h_sucesor = self._heuristica_manhattan(sucesor, meta)
                    nuevo_f = nuevo_g + h_sucesor

                    nuevo_camino = camino + [sucesor]
                    heapq.heappush(frontera, (nuevo_f, nuevo_g, sucesor, nuevo_camino))

        return None, float('inf'), nodos_expandidos

    def buscar_camino_a_estrella(self, inicio, meta):
        """
        Implementación pública de A* compatible con la API anterior.
        """
        camino, costo, _ = self._buscar_astar_detallado(inicio, meta)
        return camino, costo

    def comparar_algoritmos(self, inicio, meta):
        """
        Ejecuta BFS, Dijkstra y A* sobre la misma instancia y devuelve una tabla
        con coste, nodos expandidos y tiempo de ejecución.
        """
        resultados = {}

        for nombre, funcion_detallado in [
            ("bfs", self._buscar_bfs_detallado),
            ("dijkstra", self._buscar_dijkstra_detallado),
            ("astar", self._buscar_astar_detallado),
        ]:
            inicio_tiempo = time.perf_counter()
            camino, costo, nodos_expandidos = funcion_detallado(inicio, meta)
            fin_tiempo = time.perf_counter()

            resultados[nombre] = {
                "camino": camino,
                "coste_total": costo,
                "nodos_expandidos": nodos_expandidos,
                "tiempo_seg": fin_tiempo - inicio_tiempo,
                "longitud": None if camino is None else len(camino) - 1,
            }

        return resultados