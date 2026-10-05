(define (problem mision-rover-1)
  (:domain rover-dominio)
  
  (:objects 
    base r1 r2 ant - lugar
    m1 m2 - muestra
  )
  
  (:init 
    ;; Ubicación inicial del rover
    (en base)
    
    ;; Conexiones bidireccionales entre los lugares de la misión
    (conectado base r1)
    (conectado r1 base)
    
    (conectado r1 r2)
    (conectado r2 r1)
    
    (conectado r2 ant)
    (conectado ant r2)
    
    ;; Localización de las muestras científicas
    (muestra-en m1 r1)
    (muestra-en m2 r2)
    
    ;; Definición de la zona con antena de comunicación
    (zona-com ant)
  )
  
  (:goal 
    (and 
      (transmitida m1)
      (transmitida m2)
    )
  )
)