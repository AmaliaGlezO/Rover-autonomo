# Proyecto 1 — Rover autónomo

Este repositorio implementa una simulación de misión autónoma para un rover que explora un entorno discreto, recolecta datos, analiza resultados y transmite información en zonas de comunicación.

El proyecto incluye:

- generación parametrizable del entorno
- búsqueda con A*
- modelado operativo del rover con batería y memoria
- planificación de alto nivel
- optimización por metaheurísticas
- comparación experimental con varias semillas

## Requisitos

- Python 3.11+
- pip

## Instalación desde cero

1. Clona o descarga el repositorio.
2. Entra en la carpeta del proyecto.
3. Crea un entorno virtual:

   python -m venv .venv

4. Activa el entorno:

   En Windows PowerShell:
   .\.venv\Scripts\Activate.ps1

5. Instala las dependencias:

   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt

## Estructura del proyecto

- `entorno_gen.py`: generador del mapa y la instancia del problema.
- `modulo_busqueda.py`: implementación del algoritmo A* con costes por terreno.
- `modelo_rover.py`: modelo del rover con batería, memoria, POIs y comunicación.
- `planificador_rover.py`: planificador de alto nivel.
- `metaheuristicas_rover.py`: optimización del orden de visita de POIs.
- `experimentacion_rover.py`: protocolo experimental con varias semillas.
- `simulador.py`: demo funcional del sistema completo.
- `main.py`: entrada principal para ejecutar los módulos.
- `rover-dominio.pddl`: dominio PDDL base.
- `rover-problema.pddl`: problema PDDL base.

## Ejecución de cada parte

### 1. Generar un entorno

python entorno_gen.py

Esto genera una instancia con mapa, obstáculos, POIs y recursos.

### 2. Ejecutar la búsqueda A*

python main.py --demo busqueda

### 3. Ejecutar el rover con misión básica

python main.py --demo rover

### 4. Ejecutar el planificador de alto nivel

python main.py --demo planificador

### 5. Ejecutar la optimización por metaheurísticas

python main.py --demo metaheuristica

### 6. Ejecutar la comparación experimental

python main.py --demo experimentacion

### 7. Ejecutar la demo completa

python main.py --demo todo

También puedes ejecutar:

python simulador.py

## Flujo recomendado del proyecto

1. Generar la instancia del entorno.
2. Resolver rutas con A*.
3. Ejecutar la misión del rover con el planificador.
4. Optimizar el orden de visita con metaheurísticas.
5. Comparar varias semillas con experimentación.
6. Analizar coste, puntuación, tiempos y robustez.

## Dependencias declaradas

El proyecto usa principalmente:

- numpy

La lista exacta está en `requirements.txt`.

## Notas de reproducibilidad

- Las instancias se generan por semilla.
- Las comparaciones se hacen sobre varias semillas para evitar conclusiones basadas en un único caso.
- Los resultados deben reportarse como media y dispersión, no solo como una mejor ejecución.
- La ejecución del proyecto es reproducible usando el mismo entorno virtual y la misma lista de dependencias.