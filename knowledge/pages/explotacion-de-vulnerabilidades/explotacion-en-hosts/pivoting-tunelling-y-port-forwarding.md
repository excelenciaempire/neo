
# Pivoting, Tunelling y Port Forwarding

## <mark style="color:purple;">Introducción a la sección</mark>

<figure><img src="/files/6rgkWMViZjo4nmoqDinK" alt=""><figcaption></figcaption></figure>

Durante un ejercicio de `red team`, una `prueba de penetración` o una `evaluación de Active Directory`, a menudo nos encontraremos en una situación en la que es posible que ya hayamos comprometido las credenciales, claves ssh, hashes o tokens de acceso necesarios para pasar a otro host, pero es posible que haya `otro host al que no se se pueda acceder directamente` desde nuestro host de ataque.&#x20;

En tales casos, es posible que necesitemos utilizar un host de pivote que ya hayamos comprometido para encontrar un camino hacia nuestro próximo objetivo. Una de las cosas más importantes que debemos hacer al acceder a un host por primera vez es verificar nuestro nivel de privilegios, conexiones de red y posibles VPN u otro software de acceso remoto. Si un host tiene más de un adaptador de red, probablemente podamos usarlo para movernos a un segmento de red diferente. Pivotar es esencialmente la idea de moverse a otras redes a través de un host comprometido para encontrar más objetivos en diferentes segmentos de la red.

Hay muchos términos diferentes que se utilizan para describir un host comprometido que podemos utilizar para pasar a un segmento de red previamente inalcanzable. Algunos de los más comunes son:

* `Pivot Host`
* `Proxy`
* `Foothold`
* `Beach Head system`
* `Jump Host`

El uso principal de Pivoting es vencer la segmentación (tanto física como virtualmente) para acceder a una red aislada. La construcción de túneles, por otro lado, es un subconjunto de la pivotación. El túnel encapsula el tráfico de la red en otro protocolo y lo dirige a través de él. Piensa en esto, de esta manera:

Tenemos una clave que debemos enviar a un socio, pero no queremos que nadie que vea nuestro paquete sepa que es una clave. Entonces conseguimos un animal de peluche y escondemos la llave dentro con instrucciones sobre lo que hace. Luego empaquetamos el juguete y se lo enviamos a nuestro socio. Cualquiera que inspeccione la caja verá un simple peluche, sin darse cuenta de que contiene algo más. Sólo nuestro socio sabrá que la llave está escondida en su interior y aprenderá cómo acceder a ella y utilizarla una vez entregada.

Las aplicaciones típicas como VPN o navegadores especializados son simplemente otra forma de tunelización del tráfico de red.

Inevitablemente nos encontraremos con varios términos diferentes utilizados para describir lo mismo en TI y en la industria de Infosec. Al pivotar, notaremos que esto a menudo se denomina [`movimiento lateral`](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/movimientos-laterales.md).

***¿No es lo mismo que pivotar?***

La respuesta a eso no es exactamente. Tomémonos un segundo para comparar y contrastar el movimiento lateral con el pivote y el túnel, ya que puede haber cierta confusión sobre por qué algunos los consideran conceptos diferentes.

***

## <mark style="color:purple;">Comparación de Movimiento Lateral, Pivoting y Tunelización</mark>

### **Movimiento lateral**

El movimiento lateral puede describirse como una técnica utilizada para promover nuestro acceso a entornos adicionales `hosts`, `aplicaciones` y `servicios` dentro de un entorno de red. El movimiento lateral también puede ayudarnos a obtener acceso a recursos de dominio específicos que podamos necesitar para elevar nuestros privilegios. El movimiento lateral a menudo permite la escalada de privilegios entre hosts. Además de la explicación que hemos brindado para este concepto, también podemos estudiar cómo otras organizaciones respetadas explican el Movimiento Lateral. Consulte estas dos explicaciones cuando el tiempo lo permita:

[Explicación de Palo Alto Network](https://www.paloaltonetworks.com/cyberpedia/what-is-lateral-movement)

[Explicación de MITRE](https://attack.mitre.org/tactics/TA0008/)

Un ejemplo práctico de `Movimiento Lateral` sería:

Durante una evaluación, obtuvimos acceso inicial al entorno de destino y pudimos obtener el control de la cuenta de administrador local. Realizamos un escaneo de la red y encontramos tres hosts de Windows más en la red. Intentamos utilizar las mismas credenciales de administrador local y uno de esos dispositivos compartió la misma cuenta de administrador. Usamos las credenciales para movernos lateralmente a ese otro dispositivo, lo que nos permitió comprometer aún más el dominio.

### **Pivoting**

Utilizar múltiples hosts para `cruzar fronteras de red` a las que normalmente no tendría acceso. Este es más bien un objetivo específico. El objetivo aquí es permitirnos avanzar más profundamente en una red comprometiendo los hosts o la infraestructura específicos.

Un ejemplo práctico de `Pivoting` sería:

Durante un pentesting, la red del objetivo se separó física y lógicamente. Esta separación nos dificultaba movernos y completar nuestros objetivos. Tuvimos que buscar en la red y comprometer un host que resultó ser la estación de trabajo de ingeniería utilizada para mantener y monitorear equipos en el entorno operativo, enviar informes y realizar otras tareas administrativas en el entorno empresarial. Ese host resultó tener doble hogar (tener más de una NIC física conectada a diferentes redes). Sin tener acceso a redes empresariales y operativas, no habríamos podido girar como necesitábamos para completar nuestra evaluación.

### **Tunelling**

A menudo nos encontramos utilizando varios protocolos para trasladar el tráfico dentro y fuera de una red donde existe la posibilidad de que nuestro tráfico sea detectado. Por ejemplo, usar HTTP para enmascarar nuestro tráfico de Comando y Control desde un servidor de nuestra propiedad al host de la víctima. La clave aquí es ofuscar nuestras acciones para evitar ser detectados durante el mayor tiempo posible. Utilizamos protocolos con medidas de seguridad mejoradas, como HTTPS sobre TLS o SSH sobre otros protocolos de transporte. Este tipo de acciones también permiten tácticas como la filtración de datos fuera de una red objetivo o la entrega de más cargas útiles e instrucciones a la red.

Un ejemplo práctico de `Tunneling` sería:

Una forma en que utilizamos Tunneling fue diseñar nuestro tráfico para que se oculte en HTTP y HTTPS. Esta es una forma común en la que mantenemos el Comando y Control (C2) de los hosts que habíamos comprometido dentro de una red. Enmascaramos nuestras instrucciones dentro de solicitudes GET y POST que aparecían como tráfico normal y, para el ojo inexperto, parecerían una solicitud web o una respuesta a cualquier sitio web antiguo. Si el paquete se formó correctamente, se reenviará a nuestro servidor de Control. Si no lo fuera, sería redirigido a otro sitio web, lo que podría despistar al defensor que lo revisa.

En resumen, deberíamos considerar estas tácticas como cosas separadas. El movimiento lateral nos ayuda a expandirnos dentro de una red, elevando nuestros privilegios, mientras que el movimiento pivotante nos permite profundizar en las redes accediendo a entornos que antes eran inalcanzables. Tenga en cuenta esta comparación mientras avanza por este módulo.

***

Ahora que hemos conocido el módulo y hemos definido y comparado el movimiento lateral, el pivote y el túnel, profundicemos en algunos de los conceptos de red que nos permiten realizar estas tácticas.
