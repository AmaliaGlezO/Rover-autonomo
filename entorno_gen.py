import random
import numpy as np

# ==========================================
# 1. DEFINICIÓN DE CONSTANTES Y COSTOS
# ==========================================
# Aquí definimos los tipos de terreno y su costo en batería.
# Usamos números enteros para representar cada tipo en la matriz.
TERRENO_LISO = 0      # Costo bajo de batería
TERRENO_RUGOSO = 1    # Costo moderado
ARENA_FINA = 2        # Costo alto
BARRO = 3             # Costo muy alto
OBSTACULO = -1        # Impasable (paredes/rocas gigantes)

COSTOS_BATERIA = {
    TERRENO_LISO: 1,
    TERRENO_RUGOSO: 3,
    ARENA_FINA: 5,
    BARRO: 8,
    OBSTACULO: float('inf') # Infinito, no se puede pasar
}

class GeneradorEntornoRover:
    def __init__(self, ancho=10, alto=10, semilla=42):
        """
        Inicializa el generador del entorno.
        - ancho y alto: Dimensiones de la cuadrícula.
        - semilla: El número clave para que el mapa sea reproducible.
        """
        self.ancho = ancho
        self.alto = alto
        self.semilla = semilla
        
        # Fijamos la semilla en Python y NumPy para garantizar reproducibilidad exacta
        random.seed(self.semilla)
        np.random.seed(self.semilla)

    def generar_mapa(self, probabilidad_obstaculos=0.15, num_pois=3):
        """
        Genera una instancia del mapa de manera aleatoria pero controlada por la semilla.
        """
        # Creamos una cuadrícula base utilizando probabilidades para los tipos de terreno:
        # 50% Liso, 25% Rugoso, 15% Arena, 10% Barro
        tipos_terreno = [TERRENO_LISO, TERRENO_RUGOSO, ARENA_FINA, BARRO]
        pesos_probabilidad = [0.50, 0.25, 0.15, 0.10]
        
        # Matriz numérica del mapa de terrenos
        mapa_terrenos = np.random.choice(
            tipos_terreno, 
            size=(self.alto, self.ancho), 
            p=pesos_probabilidad
        )
        
        # Colocamos obstáculos de manera aleatoria según la probabilidad
        for y in range(self.alto):
            for x in range(self.ancho):
                if random.random() < probabilidad_obstaculos:
                    mapa_terrenos[y, x] = OBSTACULO

        # Definimos posiciones especiales de forma segura (ej. Inicio y Zonas de Coms)
        punto_inicio = (0, 0)
        mapa_terrenos[punto_inicio] = TERRENO_LISO # Garantizamos que la salida esté libre
        
        zona_comunicacion = (self.alto - 1, self.ancho - 1)
        mapa_terrenos[zona_comunicacion] = TERRENO_LISO # Garantizamos que la base esté libre

        # Colocamos los Puntos de Interés (POI) aleatoriamente en casillas que no sean obstáculos
        pois = []
        while len(pois) < num_pois:
            px = random.randint(0, self.ancho - 1)
            py = random.randint(0, self.alto - 1)
            
            # Evitamos poner un POI justo en el inicio, en la base o sobre un obstáculo
            if (py, px) != punto_inicio and (py, px) != zona_comunicacion and mapa_terrenos[py, px] != OBSTACULO:
                if (py, px) not in pois:
                    pois.append((py, px))

        # Empaquetamos todo en un diccionario que representa nuestra "Instancia del Problema"
        instancia_problema = {
            "ancho": self.ancho,
            "alto": self.alto,
            "semilla": self.semilla,
            "mapa": mapa_terrenos,
            "costos": COSTOS_BATERIA,
            "inicio": punto_inicio,
            "zona_comunicacion": zona_comunicacion,
            "pois": pois
        }
        
        return instancia_problema

# ==========================================
# EJEMPLO DE USO (Para probar que funcione)
# ==========================================
if __name__ == "__main__":
    # Creamos un generador con un mapa de 8x8 y semilla 123
    mi_generador = GeneradorEntornoRover(ancho=8, alto=8, semilla=123)
    mapa_prueba = mi_generador.generar_mapa(probabilidad_obstaculos=0.1, num_pois=3)

    print(f"--- MAPA GENERADO (Semilla: {mapa_prueba['semilla']}) ---")
    print(f"Posición de Inicio (Rover): {mapa_prueba['inicio']}")
    print(f"Zona de Comunicación: {mapa_prueba['zona_comunicacion']}")
    print(f"Puntos de Interés (POI): {mapa_prueba['pois']}\n")
    print("Matriz del Terreno (Leyes: -1=Obstáculo, 0=Liso, 1=Rugoso, 2=Arena, 3=Barro):")
    print(mapa_prueba['mapa'])