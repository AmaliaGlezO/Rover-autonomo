import random
import numpy as np

# ==========================================
# 1. DEFINICIÓN DE CONSTANTES Y COSTOS
# ==========================================
TERRENO_LISO = 0
TERRENO_RUGOSO = 1
ARENA_FINA = 2
BARRO = 3
OBSTACULO = -1

COSTOS_BATERIA = {
    TERRENO_LISO: 1,
    TERRENO_RUGOSO: 3,
    ARENA_FINA: 5,
    BARRO: 8,
    OBSTACULO: float('inf')
}


class GeneradorEntornoRover:
    def __init__(self, ancho=8, alto=8, semilla=42):
        self.ancho = ancho
        self.alto = alto
        self.semilla = semilla
        random.seed(self.semilla)
        np.random.seed(self.semilla)

    def _ruta_existe(self, mapa, inicio, objetivo):
        """Comprueba conectividad con BFS, evitando obstáculos y considerando coste por terreno."""
        if inicio == objetivo:
            return True

        cola = [inicio]
        visitados = {inicio}
        while cola:
            y, x = cola.pop(0)
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.alto and 0 <= nx < self.ancho and (ny, nx) not in visitados:
                    if mapa[ny, nx] != OBSTACULO:
                        if (ny, nx) == objetivo:
                            return True
                        cola.append((ny, nx))
                        visitados.add((ny, nx))
        return False

    def _generar_pois(self, mapa, inicio, zona_comunicacion, num_pois):
        pois = []
        usados = {inicio, zona_comunicacion}
        intentos = 0

        while len(pois) < num_pois and intentos < 500:
            py = random.randint(0, self.alto - 1)
            px = random.randint(0, self.ancho - 1)
            pos = (py, px)

            if pos in usados:
                intentos += 1
                continue
            if mapa[py, px] == OBSTACULO:
                intentos += 1
                continue
            if not self._ruta_existe(mapa, inicio, pos):
                intentos += 1
                continue

            pois.append({
                "id": f"POI_{len(pois) + 1}",
                "pos": pos,
                "valor": random.randint(25, 60),
                "datos": random.randint(3, 8),
                "prioridad": round(random.uniform(0.7, 1.8), 2),
                "estado": "pendiente",
            })
            usados.add(pos)

        if len(pois) < num_pois:
            raise RuntimeError("No se pudo generar un conjunto válido de POIs.")
        return pois

    def generar_mapa(self, probabilidad_obstaculos=0.12, num_pois=3, max_intentos=200):
        """Genera una instancia con recursos del rover: batería, memoria, zonas de comunicación y POIs."""
        intentos = 0
        while intentos < max_intentos:
            tipos_terreno = [TERRENO_LISO, TERRENO_RUGOSO, ARENA_FINA, BARRO]
            pesos = [0.50, 0.25, 0.15, 0.10]

            mapa = np.random.choice(tipos_terreno, size=(self.alto, self.ancho), p=pesos)

            for y in range(self.alto):
                for x in range(self.ancho):
                    if random.random() < probabilidad_obstaculos:
                        mapa[y, x] = OBSTACULO

            inicio = (0, 0)
            mapa[inicio] = TERRENO_LISO

            zona = (self.alto - 1, self.ancho - 1)
            mapa[zona] = TERRENO_LISO

            # Estaciones de recarga en base y en zona de comunicación.
            estaciones = [inicio, zona]
            pois = self._generar_pois(mapa, inicio, zona, num_pois)

            objetivos = [p["pos"] for p in pois] + [zona]
            if all(self._ruta_existe(mapa, inicio, obj) for obj in objetivos):
                instancia = {
                    "ancho": self.ancho,
                    "alto": self.alto,
                    "semilla": self.semilla,
                    "mapa": mapa,
                    "costos": COSTOS_BATERIA,
                    "inicio": inicio,
                    "zona_comunicacion": zona,
                    "zonas_comunicacion": [zona],
                    "estaciones_recarga": estaciones,
                    "ventanas_comunicacion": [
                        {"inicio": 0, "fin": 12, "lugar": zona},
                        {"inicio": 16, "fin": 30, "lugar": zona},
                    ],
                    "pois": [p["pos"] for p in pois],
                    "pois_info": pois,
                    "bateria_inicial": 40,
                    "bateria_max": 60,
                    "memoria_inicial": 18,
                    "memoria_max": 24,
                    "coste_recoleccion": 2,
                    "coste_analisis": 5,
                    "memoria_analisis": 2,
                    "memoria_transmision": 1,
                    "recarga_por_ciclo": 22,
                    "tiempo_maximo": 80,
                }
                return instancia

            intentos += 1

        raise RuntimeError("No se pudo generar un mapa soluble tras varios intentos.")

# ==========================================
# PRUEBA RÁPIDA
# ==========================================
if __name__ == "__main__":
    generador = GeneradorEntornoRover(ancho=8, alto=8, semilla=42)
    instancia = generador.generar_mapa(probabilidad_obstaculos=0.12, num_pois=3)
    print("Inicio:", instancia["inicio"])
    print("Zonas de comunicación:", instancia["zonas_comunicacion"])
    print("POIs:", instancia["pois"])
    print(instancia["mapa"])
