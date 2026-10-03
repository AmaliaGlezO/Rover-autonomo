import heapq

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
            (0, 1, "Derecha")
        ]
        
        vecinos = []
        for dy, dx, accion in movimientos:
            ny, nx = y + dy, x + dx
            
            # Verificar que el vecino esté dentro de los límites del mapa
            if 0 <= ny < self.alto and 0 <= nx < self.ancho:
                tipo_terreno = self.mapa[ny, nx]
                costo_movimiento = self.costos[tipo_terreno]
                
                # Si el costo no es infinito, es una celda transitable (no es obstáculo)
                if costo_movimiento != float('inf'):
                    vecinos.append(((ny, nx), costo_movimiento, accion))
                    
        return vecinos

    def _heuristica_manhattan(self, pos_actual, pos_meta):
        """
        Función Heurística h(n): Distancia en línea recta adaptada a rejillas (Manhattan).
        Estima el costo mínimo ignorando temporalmente los terrenos difíciles u obstáculos.
        """
        y1, x1 = pos_actual
        y2, x2 = pos_meta
        return abs(y1 - y2) + abs(x1 - x2)

    def buscar_camino_a_estrella(self, inicio, meta):
        """
        Implementa el algoritmo de búsqueda A* con una cola con prioridad.
        Encuentra la ruta óptima minimizando el costo total de batería.
        """
        # La frontera es una cola con prioridad que almacena tuplas: (f(n), g(n), posicion_actual, camino_recorrido)
        frontera = []
        g_inicial = 0
        h_inicial = self._heuristica_manhattan(inicio, meta)
        f_inicial = g_inicial + h_inicial
        
        heapq.heappush(frontera, (f_inicial, g_inicial, inicio, [inicio]))
        
        # Diccionario para registrar el menor costo g(n) encontrado para cada estado visitado
        costos_g_conocidos = {inicio: 0}
        
        while frontera:
            f_n, g_n, nodo_actual, camino = heapq.heappop(frontera)
            
            # PRUEBA DE META: Se comprueba al expandir el nodo (regla de oro de A*)[cite: 17]
            if nodo_actual == meta:
                return camino, g_n
                
            # Si ya encontramos un camino mejor hacia este nodo, lo ignoramos
            if g_n > costos_g_conocidos.get(nodo_actual, float('inf')):
                continue
                
            # EXPANDIR NODO: Generar los sucesores
            for sucesor, costo_accion, accion in self._obtener_vecinos(nodo_actual):
                nuevo_g = g_n + costo_accion
                
                # Si el sucesor no ha sido visitado o encontramos un camino con menor costo de batería
                if sucesor not in costos_g_conocidos or nuevo_g < costos_g_conocidos[sucesor]:
                    costos_g_conocidos[sucesor] = nuevo_g
                    h_sucesor = self._heuristica_manhattan(sucesor, meta)
                    nuevo_f = nuevo_g + h_sucesor
                    
                    nuevo_camino = camino + [sucesor]
                    heapq.heappush(frontera, (nuevo_f, nuevo_g, sucesor, nuevo_camino))
                    
        # Si la frontera se vacía y no llegamos a la meta, devuelve None
        return None, float('inf')