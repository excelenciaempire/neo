
# Enumeración

La enumeración o `footprinting` es una parte crítica en cualquier ejercicio de hacking ético. El arte, la dificultad y el objetivo no son acceder a nuestro ordenador objetivo. Más bien, se trata de <mark style="color:purple;">identificar todas las formas</mark> en que podríamos atacar un objetivo.

Es fundamental comprender cómo funcionan estos servicios y qué sintaxis utilizan para una comunicación e interacción efectiva con los diferentes servicios.

## <mark style="color:purple;">Objetivo</mark>

Esta fase tiene como objetivo mejorar nuestro conocimiento y comprensión de las tecnologías, protocolos y cómo funcionan y aprender a manejar nueva información y adaptarse a nuestros conocimientos ya adquiridos. La enumeración consiste en recopilar la mayor cantidad de información posible. Cuanta más información tengamos, más fácil nos resultará encontrar vectores de ataque.

Imagina la siguiente situación:

> Nuestro socio no está en casa y ha perdido las llaves del coche. Llamamos a nuestro socio y le preguntamos dónde están las llaves. Si recibimos una respuesta como "en la sala de estar", no está del todo claro y puede llevar mucho tiempo encontrarlos allí. Sin embargo, ¿y si nuestra pareja nos dice algo así como “en el salón en la estantería blanca, al lado del televisor, en el tercer cajón”? Como resultado, será mucho más fácil encontrarlos.

No es difícil acceder al sistema de destino una vez que sabemos cómo hacerlo. La mayoría de las formas en que podemos obtener acceso podemos limitarlas a los dos puntos siguientes:

* Funciones y/o recursos que nos permiten interactuar con el objetivo y/o proporcionar información adicional.
* Información que nos proporciona información aún más importante para acceder a nuestro target.

Al escanear e inspeccionar, buscamos exactamente estas dos posibilidades. La mayor parte de la información que recibimos proviene de configuraciones erróneas o negligencia en la seguridad de los respectivos servicios. Las configuraciones incorrectas son el resultado de la ignorancia o de una mentalidad de seguridad incorrecta. Por ejemplo, si el administrador sólo confía en el firewall, los objetos de política de grupo (GPO) y las actualizaciones continuas, a menudo esto no es suficiente para proteger la red.

## <mark style="color:purple;">La enumeración es la clave</mark>

Eso es lo que dice la mayoría de la gente y tienen razón. Sin embargo, con demasiada frecuencia se malinterpreta. La mayoría de las personas comprenden que no han probado todas las herramientas para obtener la información que necesitan. La mayoría de las veces, sin embargo, no son las herramientas que no hemos probado, sino el hecho de que no sabemos cómo interactuar con el servicio y qué es relevante.

Ésa es precisamente la razón por la que tanta gente se queda estancada en un lugar y no sale adelante. Si estas personas hubieran invertido un par de horas en aprender más sobre el servicio, cómo funciona y para qué sirve, se ahorrarían algunas horas o incluso días en alcanzar su objetivo y obtener acceso al sistema.

## <mark style="color:purple;">Enumeración manual</mark>

La enumeración manual es un componente crítico. Muchas herramientas de escaneo simplifican y aceleran el proceso. Sin embargo, estas no siempre pueden eludir las medidas de seguridad de los servicios. La forma más sencilla de ilustrar esto es utilizar el siguiente ejemplo:

> La mayoría de las herramientas de escaneo tienen un tiempo de espera establecido hasta que reciben una respuesta del servicio. Si esta herramienta no responde dentro de un tiempo específico, este servicio/puerto se marcará como cerrado, filtrado o desconocido. En los dos últimos casos, aún podremos trabajar con él. Sin embargo, si un puerto está marcado como cerrado y Nmap no nos lo muestra, estaremos en una mala situación. Este servicio/puerto puede brindarnos la oportunidad de encontrar una manera de acceder al sistema. Por lo tanto, este resultado puede llevar mucho tiempo innecesario hasta encontrarlo.
