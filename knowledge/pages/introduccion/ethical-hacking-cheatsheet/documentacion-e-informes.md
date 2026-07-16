
# Documentación e informes

## <mark style="color:purple;">Introducción a la documentación y los informes</mark>

***

Unas sólidas habilidades de documentación y generación de informes son increíblemente beneficiosas en cualquier área de las tecnologías de la información o la seguridad de la información, y dominarlas puede ayudarnos a progresar rápidamente en nuestras carreras. Un alto nivel técnico es fundamental, pero sin soft skills que respalden nuestras habilidades de dominio técnico, no seremos tan eficaces al redactar políticas y procedimientos internos, documentación técnica, informes de pruebas de penetración u otros tipos de entregables para clientes.

No existe una solución universal para la toma de notas y la preparación de informes, pero sí existen principios fundamentales que deben seguirse para tener éxito. Este módulo explorará diferentes estilos de herramientas para la toma de notas, la organización de la evidencia en nuestra máquina virtual de pruebas, la redacción de resúmenes ejecutivos para públicos sin conocimientos técnicos y la documentación de cadenas de ataque y hallazgos técnicos. Intentamos ofrecer una fórmula genérica que cualquiera pueda usar para alcanzar el éxito, incluyendo consejos, trucos y buenas prácticas que hemos aprendido durante aproximadamente 25 años en conjunto en diversos puestos de consultoría técnica y gestión de cara al cliente.

Una consideración crucial para nosotros como evaluadores es que una prueba de penetración es una instantánea del estado de seguridad de la red objetivo. Deberíamos incluir una sección de resumen en nuestro informe que detalle el tipo de trabajo realizado, quién lo realizó, las direcciones IP de origen utilizadas en las pruebas y cualquier consideración especial (por ejemplo, pruebas realizadas remotamente a través de una VPN o desde un host dentro de la red del cliente). Este resumen también debería indicar que nuestras pruebas se realizaron durante un período específico y que los cambios en los sistemas incluidos en el alcance y las vulnerabilidades resultantes no se incluirán en este informe. Podríamos indicar: "Todas las actividades de prueba se realizaron entre el 7 y el 19 de enero de 2022". También podríamos añadir una cláusula de exención de responsabilidad, como: "Este informe representa una instantánea del período de prueba mencionado, y Acme Consulting, LLC no puede garantizar el estado de los activos de información propiedad del cliente fuera de este período de prueba".

***

## <mark style="color:purple;">Documentación e informes en la práctica</mark>

Podrías estar pensando: "`Este será un módulo aburrido`" o "`¿Cómo podríamos hacer un curso completo sobre este tema?`". Si bien la documentación y la generación de informes no son temas emocionantes ni tan satisfactorios como dominar una máquina o adquirir Domain Admin en un laboratorio o una red real, son habilidades cruciales para cualquier consultor. A continuación, se presentan algunos ejemplos de momentos en nuestras carreras en los que una documentación ordenada y minuciosa, así como informes detallados, nos salvaron de lo que podría haber derivado en una situación bastante desagradable.

### **Escenario 1: El caso de una máquina virtual en explosión**

Durante una prueba de penetración externa de casi un mes, me conecté un día y mi máquina virtual no cargaba correctamente. Estuve un rato intentando recuperar el sistema de archivos, pero había desaparecido por completo. Por suerte, había estado tomando notas excelentes y detalladas del proyecto con una copia local de OneNote en mi estación de trabajo. Mi equipo en aquel momento usaba una solución de almacenamiento compartido para todos los proyectos y teníamos un script automatizado para sincronizar nuestros datos y compartirlos al final de las pruebas, tanto para control de calidad como para fines de archivo. Siguiendo el consejo de un compañero de equipo con más experiencia, había estado haciendo copias de seguridad de mis pruebas en este recurso compartido al final de cada jornada laboral. Por lo tanto, una vez que creé una nueva máquina virtual (a partir de una plantilla que conservé), solo tuve que sincronizar los datos de mi proyecto y volví a las pruebas sin interrupciones. Si no hubiera seguido un proceso definido, el resultado podría haber sido catastrófico: perder semanas de trabajo y, potencialmente, un cliente para la empresa o incluso mi puesto.

### **Escenario 2 - Ping de la muerte**

Sabía que esta prueba de penetración interna sería difícil desde la llamada inicial de alcance. Un miembro del equipo de IT interno del cliente se mostró muy hostil y lo cuestionó todo, desconfiando de las habilidades del equipo y protegiendo con vehemencia un conjunto de servidores críticos (cuyas direcciones IP no estaban dentro del alcance de la prueba). Durante la fase de enumeración de las pruebas, recibí un correo electrónico y una llamada del cliente solicitando que detuviéramos todas las pruebas, ya que habíamos desactivado varios servidores críticos sensibles a cualquier tipo de análisis. Presenté todos los datos de registro, los archivos de alcance y los datos de escaneo sin procesar con marca de tiempo. Las direcciones IP de los hosts afectados estaban en mis análisis, pero también estaban incluidas en el archivo de alcance, que el cliente había confirmado. En este caso, no hice nada malo, ya que estaba probando el alcance que me asignaron (y que confirmé) y no realicé ninguna actividad imprudente. Sin embargo, aprendí una lección que añadí a mis procesos. Después de esto, me aseguré de solicitar a los clientes una lista específica de las direcciones IP y los nombres de host individuales que debían excluirse explícitamente de cualquier análisis u otra actividad de prueba. En esta situación, contaba con documentación sólida que respaldaba las actividades realizadas y una confirmación por escrito del cliente de los rangos de direcciones IP incluidos en el alcance. Sin embargo, encontré una oportunidad para perfeccionar mis procesos y crecer como consultor.

### **Escenario 3 - Lento como la melaza**

En este último ejemplo, estaba realizando una prueba de penetración interna en la sede de un cliente, sentado en una zona de la oficina donde se encontraba el personal de IT. Detrás de mí se encontraba un administrador de red particularmente hostil, quien se había mostrado escéptico sobre nuestras capacidades y herramientas desde la llamada inicial, afirmando que las pruebas de penetración anteriores de otras empresas habían ralentizado enormemente la red debido a la inexperiencia y la imprudencia de los pentesters. Menos de 20 minutos después de iniciar la prueba, este administrador de red envió correos electrónicos a toda la lista de distribución y se acercó a mi escritorio para informarme que nuestros análisis habían ralentizado la red por completo y que había bloqueado nuestras direcciones IP de origen. Luego, compartimos los resultados de nuestro análisis, demostrando que habíamos seguido las mejores prácticas y que nada de lo que habíamos hecho explicaba la ralentización de la red. Mientras tanto, otro administrador determinó que se había habilitado el modo de depuración en todos los dispositivos de red, lo cual, combinado con los análisis normales de Nmap, fue suficiente para saturar los dispositivos y causar ralentizaciones. Una vez desactivado, las pruebas continuaron sin problemas. En este caso, nuestra documentación respaldó nuestras acciones y obligó al cliente a investigar más a fondo. Si no hubiéramos tenido documentación (o si hubiera sido deficiente), fácilmente podríamos habernos culpado, lo que podría haber afectado gravemente la relación con el cliente y nuestra reputación.

Estas historias ilustran la importancia de una documentación sólida. Necesitamos justificar nuestras acciones y, si se nos solicita, presentar pruebas para que el cliente intente solucionar un problema. No es raro que cualquier problema de red durante una prueba de penetración se atribuya al pentester, independientemente de si es resultado de sus actividades. Queremos estar en una posición sólida para protegernos y ayudar a nuestros clientes. Además, nunca queremos apresurarnos a rehacer las pruebas tras perder pruebas ni pedirle a un cliente más tiempo por no haber sido diligentes en la toma de notas y la organización.

***

## <mark style="color:purple;">Sobre este módulo</mark>

Puedes descargar recursos de documentación en el siguiente enlace, que incluyen:&#x20;

* Una plantilla de reporte de ejemplo contra el cliente Inlanefreight&#x20;
* Una carpeta de organización de proyectos:

{% embed url="<https://drive.proton.me/urls/P6P3MFRJC4#pychIelN2pF6>" %}

Para sacarle el máximo provecho, recomendamos (obviamente) tomar notas detalladas y usar los consejos y trucos para identificar posibles deficiencias o ineficiencias en sus procesos. Una vez que lo haya resuelto, esperamos que encuentre maneras de ser más productivo y reducir la carga de informes, porque, siendo honestos, a nadie le gusta crear informes; lo toleramos como un mal necesario. Una vez que haya terminado este módulo, vale la pena practicar estos consejos en situaciones reales o, si aún no trabaja en consultoría, practicar sus habilidades de documentación e informes con distintas máquinas vulnerables.

Incluimos un host de ataque preconfigurado y un pequeño laboratorio con este módulo que puedes usar para simular una prueba de penetración interna. Aprovecha esto y úsalo para practicar todo lo que quieras hasta que te sientas cómodo identificando todos los hallazgos y desarrollando un estilo de documentación que se adapte a tu flujo de trabajo.

A lo largo del módulo, es posible que usemos términos como "interno" o "externo". En estos casos, nos referimos a una prueba de penetración interna o externa, respectivamente.

He tratado de hacer que este tema típicamente aburrido sea más interesante de lo habitual, así que vamos a verlo más en detalle.
