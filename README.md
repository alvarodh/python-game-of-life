# Game of Life

Utiliza la versión 3.6.6 de Python.

Se necesita de los módulos Pygame y Numpy, en caso de no tenerlos instalados habría que acceder a las páginas oficiales para realizar su descarga:

- **Pygame**: https://www.pygame.org/news
- **Numpy**: https://numpy.org/

Una vez estén ya instalados bastaría con ir a un terminal, entrar en la carpeta del proyecto y escribir la orden para lanzarlo: **python3 game_of_life.py**

**The Game of Life** o **El Juego de la Vida** es un juego autómata, es decir, la evolución del juego está determinada por el estado inicial y no necesita de ninguna entrada de datos posterior, el creador fue el matemático británico *John Horton Conway* en 1970.

El tablero es una malla formada, en este caso, por 50 filas y 50 columnas de cuadrados, que llamaremos células, todas las células tienen 8 vecinos, el tablero tendrá forma cuadrada, no obstante podemos observar que las células pueden pasar de la zona derecha a la zona izquierda y viceversa, así como de arriba a abajo y viceversa, esto se debe a que el tablero no acaba en los bordes, sino que los bordes están unidos entre sí, como si hubiésemos creado un "donut".

Todas las células tienen únicamente dos estados, que van cambiando a cada turno, las reglas que rigen el estado de una célula son:

- Una célula muerta con 3 células vecinas vivas estará viva en el próximo turno.
- Una célula viva con 2 o 3 células vecinas vivas sigue viva, en cualquier otro caso muere.

En esta variante podemos incluir diversos patrones ya conocidos, así como crear nuestros propios patrones para ver cómo se desarrollan. Los patrones conocidos que se permiten son:

- **Osciladores**: Patrones que tras un número limitado de turnos, vuelven a su estado original.
- **Autómatas** o **Naves espaciales**: Patrones que tras un número finito de turnos vuelven a su estado original, pero en otro lugar.
- **Pistolas de planeadores**: Son estructuras fijas que generan autómatas.
- **Matusalenes**: Son patrones que pueden evolucionar a lo largo de muchos tunos antes de estabilizarse.

Para crear un patrón tendremos que pulsar algunas de las teclas del teclado, qué tecla crea cada uno de los patrones está definido en las instrucciones de uso, que se encuentran en la zona derecha de la pantalla emergente, a su vez, podemos cambiar el idioma de las mismas, con los botones de la parte inferior derecha de la pantalla.
