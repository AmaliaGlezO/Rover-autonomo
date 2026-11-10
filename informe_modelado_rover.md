# Informe del modelado completo del problema Rover autónomo

## 1. Objetivo del trabajo

El proyecto original partía de una base válida, pero demasiado simple para el enunciado del curso: solo existía un mapa con costes de terreno y un algoritmo A* para encontrar rutas. Eso permite resolver un problema de navegación, pero no un problema de misión autónoma real para un rover.

La carencia principal estaba en la falta de modelado operativo del rover como agente con recursos y restricciones. Por eso se ha ampliado el problema para que incluya:

- consumo real de batería
- memoria limitada
- puntos de interés (POIs) con valor, tamaño de datos y prioridad
- recorrido por el mapa con coste asociado a cada tipo de terreno
- recarga desde estaciones o base
- recogida de datos
- análisis de muestras
- transmisión en zonas de comunicación
- integración entre la búsqueda y la ejecución de la misión

Con esto, el entorno deja de ser solo un mapa y pasa a ser una instancia del problema de exploración del rover.

## 2. Qué faltaba antes

Antes del ajuste, el proyecto tenía:

- un generador de mapas con obstáculos y terrenos
- un módulo de búsqueda con A*
- una base de planificación en PDDL

Pero no tenía una representación completa del rover como entidad activa. En particular faltaban estos elementos:

- batería real con consumo por movimiento
- memoria como recurso limitante
- estaciones de recarga
- zonas de comunicación
- POIs con prioridad y carga de datos
- acciones de: recoger, analizar, transmitir
- concepto de misión completa y puntuación

En otras palabras, solo se estaba resolviendo el problema de “ir de un punto a otro”, no el problema de “planificar una misión robótica”.

## 3. Nuevo modelado del problema

### 3.1 Entorno de misión

Se ha ampliado el generador del entorno para que cada instancia incluya no solo el mapa, sino también:

- `inicio`: posición inicial del rover
- `zonas_comunicacion`: lugares útiles para enviar información
- `estaciones_recarga`: puntos donde puede recargar batería
- `pois_info`: lista con cada POI, incluyendo posición, valor, datos, prioridad y estado
- `bateria_inicial`, `bateria_max`, `memoria_inicial`, `memoria_max`
- `tiempo_maximo`, `ventanas_comunicacion`, `recarga_por_ciclo`, etc.

Esto convierte la instancia en un problema completo de exploración, no solo en un mapa estático.

### 3.2 Rover autónomo

Se ha creado la clase `RoverAutonomo`, que encapsula el estado del rover:

- `posicion`
- `bateria`
- `memoria`
- `tiempo`
- `puntuacion`
- `transmitidos`
- `pois`

El rover tiene acceso al buscador A* para calcular rutas entre posiciones y puede realizar acciones concretas del problema.

## 4. Acciones reales integradas en la simulación

Se han añadido operaciones que corresponden al comportamiento de misión del rover:

### 4.1 Movimiento

La acción `mover_a(destino)`:

- calcula la ruta con A*
- valida si hay camino
- comprueba que la batería sea suficiente
- actualiza la posición y el coste de energía

Esto conecta la búsqueda con la misión, que es una parte fundamental del enunciado.

### 4.2 Recogida de datos

La acción `recoger_datos(poi_id)`:

- solo puede ejecutarse si el rover está en el POI
- solo si el POI está pendiente
- exige que la memoria sea suficiente para almacenar los datos del punto

Cuando se recoge, el valor del objetivo se acumula a la puntuación y el estado del POI pasa a `recogido`.

### 4.3 Análisis

La acción `analizar(poi_id)`:

- requiere que el POI haya sido recogido
- consume batería y memoria
- cambia el estado a `analizado`
- añade puntuación adicional

Esto refleja que la misión no termina en la recolección; también debe procesar la información.

### 4.4 Recarga

La acción `recargar()`:

- solo está permitida si el rover está en una estación de recarga
- incrementa la batería hasta su máximo

Esto soluciona la necesidad de gestionar energía como un recurso crítico.

### 4.5 Transmisión

La acción `transmitir()`:

- sólo funciona si el rover está en la zona de comunicación
- transmite solo los POIs ya analizados
- consume memoria en la transmisión
- aumenta la puntuación total

Esto modela la fase final de la misión de exploración.

## 5. Integración de la Búsqueda con la misión

Una parte importante del trabajo es precisamente esta conexión:

- El entorno genera un mapa con costes por tipo de terreno.
- El módulo de búsqueda A* calcula rutas con coste real.
- El rover usa esas rutas para desplazarse desde su posición a un POI, a una estación de recarga o a la zona de comunicación.

Así, la búsqueda deja de ser una prueba aislada y pasa a ser un componente funcional del sistema de decisión del rover.

## 6. Qué incorpora el nuevo entorno

En `entorno_gen.py` se han añadido varios elementos que antes faltaban:

- zonas de comunicación
- estaciones de recarga
- POIs con valor, datos y prioridad
- recursos de batería y memoria
- información útil para simular la misión completa

Esto hace que cada instancia del problema sea mucho más realista y más alineada con el enunciado del proyecto.

## 7. Ejemplo de ejecución del modelo

La clase `RoverAutonomo` ya permite ejecutar una misión básica con una estrategia simple:

- ordenar los POIs por prioridad
- moverse hasta cada POI
- recoger sus datos
- analizar la información
- regresar a una zona de comunicación
- transmitir

La operación `ejecutar_mision_basica()` encapsula ese flujo. Aunque todavía es una estrategia simple, ya refleja el comportamiento completo del rover y deja la base para:

- metaheurísticas
- planificación o CSP
- comparación experimental entre estrategias

## 8. Por qué esto resuelve la parte que faltaba

Con este modelado, el proyecto ya no es solo un “mapa con A*”, sino un problema de misión robótica con restricciones reales. Se cumplen estos aspectos que el enunciado exige:

- batería como recurso limitado
- memoria como recurso limitado
- objetivos con prioridad y valor
- comunicación como parte de la misión
- acciones de recogida, análisis y transmisión
- integración entre los módulos de entorno y búsqueda

Esto es la base sólida para continuar con la siguiente fase del proyecto: planificación o CSP, metaheurísticas y experimentación con varias instancias generadas por semilla.

## 9. Conclusión

El trabajo realizado ha sido clave para pasar de un prototipo conceptual a un modelo de misión más realista y apropiado para la asignatura. El proyecto ya incluye la parte central que faltaba: el rover deja de ser un punto móvil y se convierte en un agente que toma decisiones bajo restricciones de energía, memoria y comunicación.

Este modelado es la base necesaria para implementar la siguiente capa del proyecto: optimización mediante metaheurísticas y procedimientos de planificación o CSP.
