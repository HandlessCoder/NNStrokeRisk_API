# Página principal

## Objetivo

El objetivo es de la tarea es habilitar la sección `A jugar` para que tengamos un panel como el siguiente:

![Canvas de imagen](/usr/app/src/img/canvas.png)

en el cuál podamos ejecutar una operación matemática sencilla.

Tenemos entonces tres tipos de input en nuestro canvas:

![Canvas de imagen](usr/app/src/img/canvas2.png)

1. Exponentes: 3 posibles referentes a los cuadrados morados. Deben ser números del 0 al 9.
2. Operadores: 2 posibles referentes a los cuadrados azules. Explicados en la siguiente sección.
3. Números: 3 posibles referentes a los cuadrados rojos. Deben ser números del 0 al 9.

## Operadores

Solo vamos a usar las 4 operaciones fundamentales: suma, resta, multiplicación y división. 

En el caso de suma y resta las únicas opciones posibles son: + (ASCII Code 43) y - (ASCII Code 45), respectivamente.

En el caso de multiplicación y división tendremos 2 opciones como sigue:

### Multiplicación

Una × (ASCII Code 215) o un asterísco * (ASCII Code 42)

![Multiplicación 1](img/mult1.png) ![Multiplicación 2](src/img/mult2.png)


### División

Un slash / (ASCII code 47) o el operando convencional ÷ (ASCII code 247)

![Multiplicación 1](/img/div2.png) ![Multiplicación 2](src/img/div1.png)


## Comentarios

### Sobre las operaciones

1. Asumimos que la aplicación siempre será usada por un agente honesto. No se debe validar para datos que no sean los referentes al modelo (aunque es un problema interesante de resolver)
2. Somos consistentes en la entrada de cada canvas así como en el orden de las operaciones: de izquierda a derecha y con prioridad de operadores: ^, ( *, /), (+, -).

### Sobre la parte visual

Escoger las secciones útiles de `02_Canvas.py` y crear la vista referente a cada uno de los elementos de entrada:

1. 3 Coeficientes
2. 3 exponentes
3. 2 operadores

Para luego llamar a los modelos y evaluar la función.

