(define (domain rover-dominio)
  (:requirements :strips :typing)
  
  (:types 
    lugar 
    muestra
  )
  
  (:predicates 
    (en ?l - lugar)
    (conectado ?l1 - lugar ?l2 - lugar)
    (muestra-en ?m - muestra ?l - lugar)
    (tiene ?m - muestra)
    (analizada ?m - muestra)
    (transmitida ?m - muestra)
    (zona-com ?l - lugar)
  )

  ;; Acción 1: Mover el rover de un lugar a otro conectado
  (:action mover
    :parameters (?desde - lugar ?hacia - lugar)
    :precondition (and 
      (en ?desde) 
      (conectado ?desde ?hacia)
    )
    :effect (and 
      (not (en ?desde)) 
      (en ?hacia)
    )
  )

  ;; Acción 2: Tomar una muestra que se encuentra en el lugar actual
  (:action tomar
    :parameters (?m - muestra ?l - lugar)
    :precondition (and 
      (en ?l) 
      (muestra-en ?m ?l)
    )
    :effect (and 
      (not (muestra-en ?m ?l)) 
      (tiene ?m)
    )
  )

  ;; Acción 3: Analizar una muestra que el rover tiene en su poder
  (:action analizar
    :parameters (?m - muestra)
    :precondition (and 
      (tiene ?m)
    )
    :effect (and 
      (analizada ?m)
    )
  )

  ;; Acción 4: Transmitir los datos de una muestra analizada desde una zona de comunicación
  (:action transmitir
    :parameters (?m - muestra ?l - lugar)
    :precondition (and 
      (en ?l) 
      (zona-com ?l) 
      (tiene ?m) 
      (analizada ?m)
    )
    :effect (and 
      (transmitida ?m)
    )
  )
)