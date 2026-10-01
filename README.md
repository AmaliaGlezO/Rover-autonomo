# Proyecto 1 de Elementos de Inteligencia Artificial — Rover autónomo

El proyecto consiste en simular un rover autónomo que explora un entorno desconocido. El rover se mueve por una rejilla o un grafo donde hay obstáculos, distintos tipos de terreno, puntos de interés científico y zonas de comunicación. Durante la misión tiene que moverse, recolectar datos, analizarlos, transmitirlos y recargar energía, todo con recursos limitados (batería y memoria).

El objetivo es modelar bien el problema y aplicar técnicas de inteligencia artificial para que el rover tome buenas decisiones.

## Se va a implementará
El proyecto tiene tres módulos obligatorios y uno opcional:  
  
- Búsqueda: algoritmos para encontrar rutas entre objetivos, considerando que cada tipo de terreno tiene un costo distinto.  
  
- Planificación o CSP: se elige uno de los dos. El planificador genera la secuencia de alto nivel de acciones del rover (moverse, recolectar, analizar, transmitir, recargar). El CSP formula la misión como un problema de restricciones (batería, memoria, ventanas de comunicación, precedencias, tiempo).  
  
- Metaheurísticas: para ordenar los puntos de interés a visitar, ajustar parámetros como el umbral de recarga, o maximizar la puntuación de la misión.  
  
- Sistemas basados en reglas (opcional, bonificable): reglas para decisiones como la política de recarga o la priorización de objetivos.