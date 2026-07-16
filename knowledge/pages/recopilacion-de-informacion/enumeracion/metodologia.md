
# Metodología

## <mark style="color:purple;">Introducción</mark>

Con la variedad de casos que nos pueden ofrecer los sistemas de destino, es casi impredecible cómo debería diseñarse este enfoque. Por lo tanto, la mayoría de los Pentesters siguen sus hábitos y los pasos con los que se sienten más cómodos y familiarizados. Sin embargo, esta no es una metodología estandarizada sino más bien un enfoque basado en la experiencia.

Sabemos que las pruebas de penetración y, por tanto, la enumeración, son un proceso dinámico. En consecuencia, he desarrollado una metodología de enumeración estática para pruebas de penetración externas e internas que incluye dinámica libre y permite una amplia gama de cambios y adaptaciones al entorno dado.&#x20;

## <mark style="color:purple;">Capas</mark>

Esta metodología está anidada en <mark style="color:purple;">6 capas</mark> y representa, metafóricamente hablando, límites que intentamos traspasar con el proceso de enumeración. Todo el proceso de enumeración se divide en tres niveles diferentes:

| `Enumeración basada en Infraestructura` | `Enumeración basada en Hosts` | `Enumeración basada en Sistemas Operativos` |
| --------------------------------------- | ----------------------------- | ------------------------------------------- |

![Las 6 capas en la enumeración](https://academy.hackthebox.com/storage/modules/112/enum-method3.png)

{% hint style="info" %}
**Nota:** Los componentes de cada capa que se muestran representan las categorías principales y no una lista completa de todos los componentes que se deben buscar. Además, debe mencionarse aquí que la primera y segunda capa (presencia en Internet, puerta de enlace) no se aplican del todo a la intranet, como una infraestructura de Active Directory. Las capas de infraestructura interna se cubrirán en otros módulos.
{% endhint %}

Considere estas líneas como una especie de obstáculo, como una pared, por ejemplo. Lo que hacemos aquí es mirar a nuestro alrededor para saber dónde está la entrada, o el hueco por el que podemos pasar, o trepar para acercarnos a nuestro objetivo. Teóricamente también es posible atravesar la pared de cabeza, pero muchas veces sucede que el punto en el que hemos roto el hueco con mucho esfuerzo y tiempo con fuerza no nos aporta mucho porque no hay entrada por este punto. la pared para pasar a la siguiente pared.

Estas capas están diseñadas de la siguiente manera:

<table data-header-hidden><thead><tr><th width="171.33333333333331"></th><th></th><th></th></tr></thead><tbody><tr><td><strong>Capa</strong></td><td><strong>Descripción</strong></td><td><strong>Categorías de información</strong></td></tr><tr><td><code>1. Presencia en Internet</code></td><td>Identificación de presencia en Internet e infraestructura accesible externamente.</td><td>Dominios, Subdominios, vHosts, ASN, Netblocks, Direcciones IP, Instancias en la Nube, Medidas de Seguridad</td></tr><tr><td><code>2. Puerta de enlace</code></td><td>Identificar las posibles medidas de seguridad para proteger la infraestructura externa e interna de la empresa.</td><td>Firewalls, DMZ, IPS/IDS, EDR, Proxies, NAC, Segmentación de red, VPN, Cloudflare</td></tr><tr><td><code>3. Servicios Accesibles</code></td><td>Identifique interfaces y servicios accesibles que estén alojados externa o internamente.</td><td>Tipo de servicio, funcionalidad, configuración, puerto, versión, interfaz</td></tr><tr><td><code>4. Procesos</code></td><td>Identificar los procesos internos, fuentes y destinos asociados a los servicios.</td><td>PID, Datos Procesados, Tareas, Origen, Destino</td></tr><tr><td><code>5. Privilegios</code></td><td>Identificación de los permisos y privilegios internos a los servicios accesibles.</td><td>Grupos, Usuarios, Permisos, Restricciones, Entorno</td></tr><tr><td><code>6. OS Setup</code></td><td>Identificación de los componentes internos y configuración de los sistemas.</td><td>Tipo de sistema operativo, nivel de parche, configuración de red, entorno del sistema operativo, archivos de configuración, archivos privados confidenciales</td></tr></tbody></table>

{% hint style="info" %}
**Nota importante:** El aspecto humano y la información que pueden obtener los empleados usando OSINT se han eliminado de la capa "Presencia en Internet" por simplicidad.
{% endhint %}

Por fin podemos imaginar toda la prueba de penetración en forma de laberinto donde tenemos que identificar los huecos y encontrar la manera de entrar en él de la forma más rápida y eficaz posible. Este tipo de laberinto puede verse así:

![imagen](https://academy.hackthebox.com/storage/modules/112/pentest-labyrinth.png)

Los cuadrados representan las brechas/vulnerabilidades. Como probablemente ya hemos notado, podemos ver que encontraremos una brecha y muy probablemente varias. El hecho interesante y muy común es que no todos los huecos que encontramos pueden llevarnos al interior.&#x20;

Todas las pruebas de penetración están limitadas en el tiempo, pero siempre debemos tener en cuenta la creencia de que casi siempre hay una manera de entrar. Incluso después de una prueba de penetración de cuatro semanas, no podemos decir al 100% que no hay más vulnerabilidades.&#x20;

Alguien que haya estado estudiando la empresa durante meses y analizándola probablemente tendrá una comprensión mucho mayor de las aplicaciones y la estructura de la que pudimos obtener en las pocas semanas que dedicamos a la evaluación. Un excelente y reciente ejemplo de ello es el [ciberataque a SolarWinds](https://www.rpc.senate.gov/policy-papers/the-solarwinds-cyberattack) , ocurrido no hace mucho. Esta es otra excelente razón para una metodología que debe excluir tales casos.

Supongamos que se nos ha pedido que realicemos una prueba de penetración externa de "caja negra". Una vez que se hayan cumplido por completo todos los elementos necesarios del contrato, nuestra prueba de penetración comenzará a la hora especificada.

***

### <mark style="color:purple;">Capa 1: Presencia en Internet</mark>

La primera capa que tenemos que pasar es la capa de "Presencia en Internet", donde nos centramos en encontrar los objetivos que podemos investigar. Si el alcance del contrato nos permite buscar hosts adicionales, esta capa es incluso más crítica que solo para objetivos fijos. En esta capa utilizamos diferentes técnicas para encontrar dominios, subdominios, netblocks y muchos otros componentes e información que presentan la presencia de la empresa y su infraestructura en Internet.

> El objetivo de esta capa es identificar todos los posibles sistemas de destino e interfaces que se pueden probar.

***

### <mark style="color:purple;">Capa 2: Puerta de enlace</mark>

Aquí intentamos comprender la interfaz del objetivo alcanzable, cómo está protegido y dónde se encuentra en la red. Debido a la diversidad, diferentes funcionalidades y algunos procedimientos particulares, entraremos en más detalles sobre esta capa en otros módulos.

> El objetivo es comprender a qué nos enfrentamos y a qué debemos prestar atención.

***

### <mark style="color:purple;">Capa 3: Servicios Accesibles</mark>

En el caso de servicios accesibles, examinamos cada destino por todos los servicios que ofrece. Cada uno de estos servicios tiene un propósito específico que ha sido instalado por un motivo particular por parte del administrador. Cada servicio tiene determinadas funciones que, por tanto, también conducen a resultados específicos. Para trabajar eficazmente con ellos, necesitamos saber cómo funcionan. De lo contrario, debemos aprender a comprenderlos.

> Esta capa tiene como objetivo comprender el motivo y la funcionalidad del sistema de destino y obtener el conocimiento necesario para comunicarnos con él y explotarlo para nuestros propósitos de manera efectiva.

Esta es la parte de la enumeración que trataremos principalmente en este módulo.

***

### <mark style="color:purple;">Capa 4: Procesos</mark>

Cada vez que se ejecuta un comando o función, se procesan datos, ya sean ingresados ​​por el usuario o generados por el sistema. Esto inicia un proceso que tiene que realizar tareas específicas, y dichas tareas tienen al menos un origen y un destino.

> El objetivo aquí es comprender estos factores e identificar las dependencias entre ellos.

***

### <mark style="color:purple;">Capa 5: Privilegios</mark>

Cada servicio se ejecuta a través de un usuario específico en un grupo particular con permisos y privilegios definidos por el administrador o el sistema. Estos privilegios muchas veces nos proporcionan funciones que los administradores pasan por alto. Esto sucede a menudo en infraestructuras de Active Directory y muchos otros entornos y servidores de administración de casos específicos donde los usuarios son responsables de múltiples áreas de administración.

> Es crucial identificarlos y comprender qué es y qué no es posible con estos privilegios.

***

### <mark style="color:purple;">Capa 6: Configuración del Sistema Operativo</mark>

Aquí recopilamos información sobre el sistema operativo real y su configuración mediante acceso interno. Esto nos brinda una buena visión general de la seguridad interna de los sistemas y refleja las habilidades y capacidades de los equipos administrativos de la empresa.

> El objetivo aquí es ver cómo los administradores gestionan los sistemas y qué información interna sensible podemos obtener de ellos.

***

### <mark style="color:purple;">Metodología de enumeración en la práctica</mark>

Una metodología resume todos los procedimientos sistemáticos para obtener conocimiento dentro de los límites de un objetivo determinado. Es importante señalar que una metodología no es una guía paso a paso sino, como implica la definición, un resumen de procedimientos sistemáticos. En nuestro caso, la metodología de enumeración es el enfoque sistemático para explorar un objetivo determinado.

La forma en que se identifican los componentes individuales y se obtiene la información en esta metodología es un aspecto dinámico y en crecimiento que cambia constantemente y, por lo tanto, puede diferir. Un excelente ejemplo de esto es el uso de herramientas de recopilación de información de servidores web. Existen innumerables herramientas diferentes para esto y cada una de ellas tiene un enfoque específico y, por lo tanto, ofrece resultados individuales que se diferencian de otras aplicaciones. El objetivo, sin embargo, es el mismo. Por lo tanto, la colección de herramientas y comandos no es parte de la metodología real, sino más bien un Cheatsheet al que podemos referirnos usando los comandos y herramientas enumerados en casos determinados.
