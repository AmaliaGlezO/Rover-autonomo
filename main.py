from entorno_gen import GeneradorEntornoRover
from modulo_busqueda import BusquedaRover

if __name__ == "__main__":
    # 1. Generamos el entorno utilizando el código anterior
    generador = GeneradorEntornoRover(ancho=8, alto=8, semilla=123)
    instancia = generador.generar_mapa(probabilidad_obstaculos=0.1, num_pois=2)
    
    # 2. Inicializamos el módulo de búsqueda pasándole la instancia del mapa
    buscador = BusquedaRover(instancia)
    
    # 3. Definimos punto de inicio y buscamos el camino hacia el primer POI o la Zona de Comunicación
    inicio = instancia['inicio']
    objetivo = instancia['pois'][0] # Primer Punto de Interés
    
    print(f"Calculando ruta óptima para el Rover desde {inicio} hasta el POI en {objetivo}...")
    
    camino, costo_total_bateria = buscador.buscar_camino_a_estrella(inicio, objetivo)
    
    if camino:
        print(f"¡Ruta encontrada con éxito!")
        print(f"Camino a seguir (coordenadas): {camino}")
        print(f"Costo total de batería consumido: {costo_total_bateria} unidades\n")
    else:
        print("Lo siento, el rover está atrapado y no hay ruta posible hacia el objetivo.")