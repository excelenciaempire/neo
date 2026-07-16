
# Consejos y trucos en la realización de informes

La elaboración de informes es una parte esencial del proceso de pruebas de penetración, pero si se gestiona mal, puede volverse muy tediosa y propensa a errores. Un aspecto clave de los informes es que debemos trabajar en su elaboración desde el principio. Esto comienza con nuestra estructura organizativa y la configuración de la toma de notas, pero en ocasiones podemos realizar un análisis de descubrimiento extenso donde podríamos completar partes predefinidas del informe, como la información de contacto, el nombre del cliente, el alcance, etc.&#x20;

Durante las pruebas, podemos redactar nuestra cadena de ataque y cada hallazgo con toda la evidencia necesaria para no tener que apresurarnos a recuperarla una vez finalizada la evaluación. Trabajar sobre la marcha garantizará que nuestro informe no se realice con prisas y que el control de calidad lo devuelva con numerosos cambios en rojo.

***

## <mark style="color:purple;">Plantillas</mark>

Esto debería ser obvio, pero no deberíamos empezar de cero con cada informe que redactamos. Es mejor tener una plantilla de informe en blanco para cada tipo de evaluación que realizamos (incluso las más complejas). Si no usamos una herramienta de informes y trabajamos con el clásico MS Word, siempre podemos crear una plantilla de informe con macros y marcadores de posición para completar algunos de los datos que rellenamos en cada evaluación.&#x20;

Deberíamos trabajar siempre con plantillas en blanco y no simplemente modificar el informe de un cliente anterior, ya que podríamos correr el riesgo de dejar el nombre de otro cliente en el informe u otros datos que no se ajusten a nuestro entorno actual. Este tipo de error nos hace parecer aficionados y es fácilmente evitable.

***

## <mark style="color:purple;">Consejos y trucos de MS Word</mark>

Trabajar con Microsoft Word puede ser un fastidio, pero hay varias maneras de simplificarnos la vida. En nuestra experiencia, es sin duda el menor de los males. Aquí tienes algunos consejos y trucos que hemos recopilado a lo largo de los años, en mi camino hacia convertirme en un experto en MS Word. Primero, algunos comentarios:

* Los consejos y trucos que se describen aquí son para Microsoft Word. Es posible que algunas de las mismas funciones también existan en LibreOffice, pero tendrás que `[preferred search engine]`explorarlas para comprobar si es posible.
* Hazte un favor: usa Word para Windows y evita explícitamente usar Word para Mac. Si quieres usar una Mac como plataforma de pruebas, consigue una máquina virtual Windows para crear tus informes. Word para Mac carece de algunas funciones básicas que Word para Windows sí tiene, no tiene editor de VB (por si necesitas usar macros) y no puede generar archivos PDF de forma nativa que se vean y funcionen correctamente (recorta los márgenes y elimina todos los hipervínculos en la tabla de contenido), por nombrar solo algunas.
* Hay muchas más funciones avanzadas como el interletraje de fuentes que puedes usar para llevar tu estilo al siguiente nivel si lo deseas, pero vamos a tratar de concentrarnos en las cosas que mejoran la eficiencia y dejaremos que el lector (o su departamento de marketing) determine las preferencias cosméticas específicas.

Vamos a cubrir los conceptos básicos:

* `Estilos de fuentes`
  * Deberías aproximarte lo más posible a un documento sin "formato directo". Con "formato directo" me refiero a resaltar el texto y hacer clic en el botón para ponerlo en negrita, cursiva, subrayado, coloreado, resaltado, etc. "Pero pensé que acababas de decir que solo nos centraríamos en lo que mejora la eficiencia". Y así es. Si usas estilos de fuente y descubres que has pasado por alto una configuración en uno de tus encabezados que afecta la ubicación o su aspecto, al actualizar el estilo, se actualizan "todas" las instancias de ese estilo utilizadas en todo el documento en lugar de tener que actualizar manualmente las 45 veces que usaste un encabezado aleatorio (e incluso así, podrías pasar por alto alguno).
* `Estilos de tablas`
  * Aplica a las tablas todo lo que acabo de mencionar sobre los estilos de fuente. El mismo concepto. Facilita mucho los cambios globales y promueve la coherencia en todo el informe. Además, en general, facilita la experiencia de todos los usuarios del documento, tanto autores como personal de control de calidad.
* `Captions`
  * Utilice la función de subtítulos integrada (haga clic con el botón derecho en una imagen o tabla resaltada y seleccione "Insertar subtítulo...") si va a añadir subtítulos. Esta función hará que los subtítulos se renumeren automáticamente si tiene que añadir o eliminar algo del informe, lo cual es un verdadero dolor de cabeza. Normalmente, esta función incluye un estilo de fuente que le permite controlar el aspecto de los subtítulos.
* `Número de página`
  * La numeración de páginas facilita la referencia a áreas específicas del documento al colaborar con el cliente para responder preguntas o aclarar el contenido del informe (p. ej., "¿Qué significa el segundo párrafo de la página 12?"). Lo mismo ocurre con los clientes que trabajan internamente con sus equipos para abordar los hallazgos.
* `Tabla de contenidos`
  * Una tabla de contenido es un componente estándar de un informe profesional. La tabla de contenido predeterminada probablemente sea suficiente, pero si desea personalizarla, como ocultar los números de página o cambiar el encabezado de pestaña, puede seleccionar una tabla de contenido personalizada y modificar la configuración.
* `Lista de imágenes / tablas`
  * Es discutible si el informe debería incluir una Lista de Figuras o Tablas. Es el mismo concepto que una Tabla de Contenidos, pero solo enumera las figuras o tablas del informe. Estas activan los títulos, así que si no se usan títulos en una, en la otra o en ambas, no funcionará.
* `Marcadores`
  * Los marcadores se usan comúnmente para identificar lugares del documento a los que se pueden crear hipervínculos (como un apéndice con un encabezado personalizado). Si planea usar macros para combinar plantillas, también puede usar marcadores para identificar secciones enteras que se pueden eliminar automáticamente del informe.
* `Diccionarios Custom`
  * Puedes considerar un diccionario personalizado como una extensión de la función de Autocorrección integrada de Word. Si escribes mal las mismas palabras cada vez que escribes un informe o quieres evitar errores tipográficos embarazosos, como escribir "público" en lugar de "público", puedes agregar estas palabras a un diccionario personalizado y Word las reemplazará automáticamente. Lamentablemente, esta función no sigue la plantilla, así que tendrás que configurar la tuya.
* `Ajustes de idioma`
  * Lo más probable es que la configuración de idioma personalizada se aplique principalmente al estilo de fuente que creaste para tu código, terminal o evidencia textual (¿creaste uno, verdad?). Puedes seleccionar la opción de ignorar la corrección ortográfica y gramatical en la configuración de idioma para este (o cualquier) estilo de fuente. Esto es útil porque, después de crear un informe con varias cifras y querer ejecutar el corrector ortográfico, no tienes que hacer clic en "ignorar" un montón de veces para omitir todo el contenido de las cifras.
* `Bullets y numeración personalizada`
  * Puede configurar una numeración personalizada para numerar automáticamente elementos como sus hallazgos, apéndices y cualquier otra cosa que pueda beneficiarse de la numeración automática.
* `Setup de la Toolbar de Acceso Rápido`
  * Hay muchas opciones y funciones que puedes agregar a tu Barra de Herramientas de Acceso Rápido, que puedes revisar con calma para determinar su utilidad en tu flujo de trabajo. Aquí enumeraremos algunas prácticas. Selecciona `File > Options > Quick Access Toolbar` para acceder a la configuración.
  * Atrás: Siempre es recomendable hacer clic en los hipervínculos que creas para asegurarte de que te dirijan al lugar correcto del documento. Lo molesto es volver al punto donde estabas al hacer clic para poder seguir trabajando. Este botón se encarga de eso.
  * Deshacer/Rehacer: esto solo es útil si no utiliza los atajos de teclado.
  * Guardar: nuevamente, resulta útil si no utilizas el atajo de teclado.
  * Además de esto, puede configurar el menú desplegable "Elegir comandos de:" en "Comandos que no están en la cinta" para explorar las funciones que son más difíciles de realizar.
* `Atájos rápidos`
  * F4 aplicará la última acción realizada. Por ejemplo, si seleccionas un texto y le aplicas un estilo de fuente, puedes seleccionar otra cosa a la que quieras aplicar el mismo estilo y simplemente pulsar F4, lo cual hará lo mismo.
  * Si usa una tabla de contenidos y listas de figuras y tablas, puede presionar Ctrl+A para seleccionarlas todas y F9 para actualizarlas todas simultáneamente. Esto también actualizará cualquier otro campo del documento y, en ocasiones, no funciona según lo previsto, así que úselo bajo su propia responsabilidad.
  * Una opción más común es Ctrl+S para guardar. La menciono aquí porque deberías usarla con frecuencia por si Word se bloquea y así evitar perder datos.
  * Si necesita ver dos áreas diferentes del informe simultáneamente y no desea desplazarse hacia adelante y hacia atrás, puede usar Ctrl+Alt+S para dividir la ventana en dos paneles.
  * Puede que esto parezca una tontería, pero si accidentalmente presionas tu teclado y no tienes idea de dónde está el cursor (o dónde insertaste algún carácter extraño o escribiste accidentalmente algo poco profesional en tu informe en lugar de en Discord), puedes presionar Shift+F5 para mover el cursor a donde se realizó la última revisión.
  * Hay muchos más enumerados [aquí](https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2) , pero estos son los que he encontrado más útiles y que tampoco son obvios.

***

## <mark style="color:purple;">Automatización</mark>

Al desarrollar plantillas de informes, puede llegar a un punto en el que tenga un documento bastante desarrollado, pero no disponga del tiempo ni el presupuesto suficientes para adquirir una plataforma de informes automatizada. Se puede lograr una gran automatización mediante macros en documentos de MS Word. Deberá guardar sus plantillas como archivos .dotm y usar un entorno Windows para sacarle el máximo provecho (el editor de VB de Word para Mac podría no existir). Algunas de las funciones más comunes que puede realizar con macros son:

* Cree una macro que mostrará una ventana emergente para que ingrese información clave que luego se insertará automáticamente en la plantilla de informe donde se encuentran las variables de marcador de posición designadas:
  * Nombre del cliente
  * Fechas
  * Detalles del alcance
  * Tipo de prueba
  * Nombres de entornos o aplicaciones
* Puede combinar diferentes plantillas de informes en un solo documento y hacer que una macro recorra y elimine secciones enteras (que usted designe mediante marcadores) que no pertenecen a un tipo de evaluación en particular.
  * Esto facilita la tarea de mantener sus plantillas, ya que solo tiene que mantener una en lugar de muchas.
* También puede automatizar las tareas de control de calidad corrigiendo errores frecuentes. Dado que escribir macros en Word es básicamente un lenguaje de programación en sí mismo (y podría ser un curso en sí mismo), dejamos al lector la opción de usar recursos en línea para aprender a realizar estas tareas.

***

## <mark style="color:purple;">Herramientas de informes</mark>

Una vez que realice varias evaluaciones, comenzará a notar que muchos de los entornos a los que se dirige presentan los mismos problemas. Si no cuenta con una base de datos de hallazgos, perderá mucho tiempo reescribiendo el mismo contenido repetidamente y se arriesga a introducir inconsistencias en sus recomendaciones y en la precisión con la que describe el hallazgo. Si multiplica estos problemas por todo un equipo, la calidad de sus informes variará enormemente de un consultor a otro. Como mínimo, debe mantener un documento específico con versiones depuradas de sus hallazgos que pueda copiar y pegar en sus informes. Como se mencionó anteriormente, debemos esforzarnos constantemente por adaptar los hallazgos al entorno del cliente siempre que sea necesario, pero tener hallazgos en plantillas ahorra mucho tiempo.

Sin embargo, vale la pena invertir tiempo en investigar y configurar una de las plataformas disponibles diseñadas para este propósito. Algunas son gratuitas y otras de pago, pero lo más probable es que se amorticen rápidamente con el tiempo y los dolores de cabeza que se ahorran si se puede afrontar la inversión inicial.

| **Gratis**                                                                    | **De pago**                                                     |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [Ghostwriter](https://github.com/GhostManager/Ghostwriter)                    | [AttackForge](https://attackforge.com/)                         |
| [Dradis](https://dradisframework.com/ce/)                                     | [PlexTrac](https://plextrac.com/)                               |
| [Security Risk Advisors VECTR](https://github.com/SecurityRiskAdvisors/VECTR) | [Rootshell Prism](https://www.rootshellsecurity.net/why-prism/) |
| [WriteHat](https://github.com/blacklanternsecurity/writehat)                  |                                                                 |

***

## <mark style="color:purple;">Consejos y trucos varios</mark>

Aunque hemos cubierto algunos de estos temas en otras secciones del módulo, aquí hay una lista de consejos y trucos que debes tener a mano:

* Intenta contar una historia con tu informe. ¿Por qué es importante poder ejecutar Kerberoasting y descifrar un hash? ¿Cuál fue el impacto de las credenciales predeterminadas en la aplicación X?
* Escribe sobre la marcha. No dejes el informe para el final. No es necesario que tu informe sea perfecto durante las pruebas, pero documentar todo lo posible con la mayor claridad posible durante las pruebas te ayudará a ser lo más exhaustivo posible y a no pasar por alto nada ni tomar atajos por las prisas el último día del periodo de pruebas.
* Mantén el orden. Mantén las cosas en orden cronológico para que trabajar con tus notas sea más fácil. Haz que tus notas sean claras y fáciles de navegar, para que sean valiosas y no te ocasionen trabajo extra.
* Muestre la mayor cantidad de evidencia posible sin ser demasiado detallado. Incluya suficientes capturas de pantalla y comandos para demostrar y reproducir claramente los problemas, pero no agregue demasiadas capturas de pantalla adicionales ni comandos innecesarios que saturarán el informe.
* Muestra claramente lo que se presenta en las capturas de pantalla. Usa una herramienta como [Greenshot](https://getgreenshot.org/) o [Flameshot](https://flameshot.org/) para añadir flechas o cuadros de colores a las capturas de pantalla y, si es necesario, añade explicaciones debajo. Una captura de pantalla es inútil si tu público tiene que adivinar qué intentas mostrar.
* Oculte los datos confidenciales siempre que sea posible. Esto incluye contraseñas en texto plano, hashes de contraseñas, otros secretos y cualquier dato que pueda considerarse confidencial para nuestros clientes. Los informes pueden enviarse a otras empresas e incluso a terceros, por lo que queremos asegurarnos de haber realizado la debida diligencia para no incluir en el informe ningún dato que pueda utilizarse indebidamente. Se puede usar una herramienta como [Flameshot](https://flameshot.org/) para ofuscar partes de una captura de pantalla (usando formas sólidas, no borrosas).
* Redacte la salida de la herramienta siempre que sea posible para eliminar elementos que personas no expertas en hacking puedan interpretar como poco profesionales (por ejemplo, `(Pwn3d!)`de la salida de CrackMapExec). En el caso de CME, puede cambiar ese valor en su archivo de configuración para mostrar otro valor en pantalla, de modo que no tenga que cambiarlo en su informe cada vez. Otras herramientas pueden tener una personalización similar.
* Revisa la salida de tu Hashcat para asegurarte de que ninguna de las contraseñas candidatas sea vulgar. Muchas listas de palabras contienen palabras que pueden considerarse vulgares u ofensivas, y si alguna de ellas aparece en la salida de Hashcat, cámbiala por algo inocuo. Quizás pienses: "Dijeron que nunca se debe alterar la salida del comando". Los dos ejemplos anteriores son algunos de los pocos casos en los que es aceptable. Generalmente, si modificamos algo que puede interpretarse como ofensivo o poco profesional, pero no cambiamos la representación general de la evidencia del hallazgo, no hay problema, pero analízalo caso por caso y, en caso de duda, plantéalo a un gerente o líder de equipo.
* Verifique la gramática, la ortografía y el formato, asegúrese de que la fuente y el tamaño de fuente sean consistentes y deletree las siglas la primera vez que las utilice en un informe.
* Asegúrese de que las capturas de pantalla sean nítidas y no capturen partes adicionales de la pantalla que aumenten su tamaño. Si su informe es difícil de interpretar debido a un formato deficiente o a errores gramaticales y ortográficos, esto afectará negativamente los resultados técnicos de la evaluación. Considere una herramienta como Grammarly o LanguageTool (pero tenga en cuenta que estas herramientas pueden enviar algunos de sus datos a la nube para su "aprendizaje"), que es mucho más potente que el corrector ortográfico y gramatical integrado de Microsoft Word.
* Usa la salida de comandos sin procesar siempre que sea posible, pero cuando necesites capturar una consola, asegúrate de que no sea transparente y que no muestre el fondo ni otras herramientas (esto se ve fatal). La consola debe ser completamente negra con un tema adecuado (fondo negro, texto blanco o verde, no un tema multicolor extravagante que le dé problemas al lector). Tu cliente podría imprimir el informe, así que considera un fondo claro con texto oscuro para no dañar el cartucho de la impresora.
* Mantén tu nombre de host y nombre de usuario profesionales. No muestres capturas de pantalla con un mensaje como " `azzkicker@clientsmasher`.
* Establece un proceso de control de calidad. Tu informe debe pasar por al menos una, o preferiblemente dos, rondas de control de calidad (dos revisores además de ti). Nunca debemos revisar nuestro propio trabajo (siempre que sea posible) y queremos obtener el mejor resultado posible, así que presta atención al proceso de control de calidad. Como mínimo, si eres independiente, deberías pensarlo una noche y volver a revisarlo. Dejar el informe un rato puede ayudarte a ver cosas que pasaste por alto después de examinarlo durante mucho tiempo.
* Establezca una guía de estilo y cúmplala para que todos en su equipo sigan un formato similar y los informes se vean consistentes en todas las evaluaciones.
* Usa el autoguardado con tu herramienta de notas y MS Word. No querrás perder horas de trabajo porque un programa se bloquee. Además, haz copias de seguridad de tus notas y otros datos sobre la marcha, y no guardes todo en una sola máquina virtual. Las máquinas virtuales pueden fallar, así que deberías mover la evidencia a una ubicación secundaria sobre la marcha. Esta es una tarea que puede y debe automatizarse.
* Programe y automatice siempre que sea posible. Esto garantizará la coherencia de su trabajo en todas las evaluaciones que realice y evitará perder tiempo en tareas repetidas en cada evaluación.

***

## <mark style="color:purple;">Comunicación con el cliente</mark>

Unas sólidas habilidades de comunicación escrita y verbal son fundamentales para cualquier persona que desempeñe un puesto en pruebas de penetración. Durante nuestras intervenciones (desde la definición del alcance hasta la entrega y revisión del informe final), debemos mantener un contacto constante con nuestros clientes y desempeñar adecuadamente nuestro papel de asesores de confianza. Nos contratan y nos pagan una cantidad considerable para identificar problemas en sus redes, brindarles asesoramiento sobre soluciones y capacitar a su personal sobre los problemas que detectamos en nuestro informe. Al inicio de cada intervención, debemos enviar un correo electrónico con información como:

* Nombre del probador
* Descripción del tipo/alcance del compromiso
* Dirección IP de origen para la prueba (IP pública para un host de ataque externo o la IP interna de nuestro host de ataque si estamos realizando una prueba de penetración interna)
* Fechas previstas para las pruebas
* Información de contacto principal y secundaria (correo electrónico y teléfono)

Al final de cada día, debemos enviar una notificación de parada para indicar el final de las pruebas. Este puede ser un buen momento para ofrecer un resumen general de los hallazgos (especialmente si el informe incluirá más de 20 hallazgos de alto riesgo) para que el informe no sorprenda por completo al cliente. También podemos reiterar las expectativas para la entrega del informe en este momento. Por supuesto, debemos trabajar en el informe sobre la marcha y no dejarlo completamente para el último minuto, pero puede llevar varios días redactar toda la cadena de ataque, el resumen ejecutivo, los hallazgos, las recomendaciones y realizar las autoverificaciones de calidad. Después, el informe debe pasar al menos una ronda de control de calidad interno (y los responsables de control de calidad probablemente tengan muchas otras tareas pendientes), lo que puede llevar tiempo.

Las notificaciones de inicio y detención también le brindan al cliente una ventana para saber cuándo se llevaron a cabo sus exploraciones y actividades de prueba en caso de que necesite ejecutar alguna alerta.

Además de estas comunicaciones formales, es recomendable mantener un diálogo abierto con nuestros clientes y fortalecer la relación de confianza con nuestro asesor. ¿Descubrió una subred o subdominio externo adicional? Consulte con el cliente si desea añadirlo al alcance (dentro de lo razonable y siempre que no exceda el tiempo asignado para las pruebas). ¿Descubrió una falla de inyección SQL o ejecución remota de código de alto riesgo en un sitio web externo? Interrumpa las pruebas, notifique formalmente al cliente y vea cómo desea proceder. ¿Parece que un host está inactivo tras el escaneo? Sucede, y es mejor ser sincero que intentar ocultarlo. ¿Tiene un administrador de dominio o de empresa? Avise al cliente por si ve alertas y se pone nervioso, o para que pueda preparar a su equipo de gestión para el informe pendiente. Además, en este punto, infórmele que seguirá probando y buscando otras opciones, pero pregúntele si hay algo más en lo que le gustaría que se centrara o si hay servidores o bases de datos que deban seguir limitados, incluso con privilegios de DA, a los que pueda acceder.

También deberíamos hablar sobre la importancia de las notas detalladas y el registro/resultado de la herramienta del escáner. Si su cliente pregunta si se detectó un host específico el día X, debería poder proporcionar, sin lugar a dudas, evidencia documentada de sus actividades exactas. Es una lástima que lo culpen por una interrupción, pero es aún peor si lo culpan y no tienen ninguna prueba concreta que demuestre que no fue resultado de sus pruebas.

Tener en cuenta estos consejos de comunicación te ayudará mucho a generar confianza con tu cliente y a conseguir clientes recurrentes e incluso recomendaciones. A la gente le gusta trabajar con personas que la traten bien y trabajen con diligencia y profesionalismo, así que este es tu momento de brillar. Con excelentes habilidades técnicas y de comunicación, ¡serás imparable!

***

## <mark style="color:purple;">Presentando el informe final</mark>

Una vez listo el informe, debe revisarse antes de su entrega. Una vez entregado, es habitual convocar al cliente a una reunión de revisión para revisarlo en su totalidad, solo los hallazgos, o responder a sus preguntas.

#### **Proceso de control de calidad**

Un informe descuidado cuestionará todos los aspectos de nuestra evaluación. Si nuestro informe es un desastre, ¿es posible que hayamos realizado una evaluación exhaustiva? ¿Fuimos descuidados y dejamos un rastro de destrucción que el cliente tendrá que dedicar tiempo innecesario a limpiar? Asegurémonos de que nuestro informe sea un testimonio de nuestro conocimiento y trabajo duro en la evaluación, y que refleje ambos adecuadamente. El cliente no verá la mayor parte de lo que usted hizo durante la evaluación.

`El informe es lo más destacado y es por lo que el cliente está pagando!`

Podrías haber ejecutado la cadena de ataque más compleja y asombrosa de la historia de las cadenas de ataque, pero si no puedes plasmarla en el papel de forma que otra persona pueda entenderla, es como si nunca hubiera sucedido.

Si es posible, cada informe debería someterse al menos a una ronda de control de calidad por parte de alguien que no sea el autor. Algunos equipos también pueden optar por dividir el proceso de control de calidad en varios pasos (por ejemplo, control de calidad para la precisión técnica y luego control de calidad para el estilo y la estética adecuados). Dependerá de usted, su equipo o su organización elegir el enfoque adecuado para el tamaño de su equipo. Si está empezando por su cuenta y no puede permitirse el lujo de que otra persona revise su informe, le recomiendo encarecidamente que lo deje por un tiempo o que lo contemple con la almohada y lo revise de nuevo como mínimo. Después de leer un documento 45 veces, empieza a pasar por alto cosas. Este pequeño repaso puede ayudarle a detectar cosas que no vio después de haberlo examinado durante días.

Es recomendable incluir una lista de verificación de control de calidad como parte de la plantilla de su informe (elimínela una vez que el informe esté finalizado). Esta debe incluir todas las comprobaciones que el autor debe realizar respecto al contenido, el formato y cualquier otro aspecto que pueda incluir en su guía de estilo. Es probable que esta lista crezca con el tiempo a medida que usted y su equipo perfeccionen los procesos y descubran qué errores son más comunes. ¡Asegúrese de revisar la gramática, la ortografía y el formato! Una herramienta como Grammarly o LanguageTool es excelente (pero asegúrese de obtener la aprobación). No envíe un informe descuidado a control de calidad, ya que podrían devolvérselo para que lo corrijan antes de que el revisor lo revise, y puede ser una costosa pérdida de tiempo para usted y para los demás.

Una nota rápida sobre las herramientas de corrección gramatical en línea: Para aprender más y mejorar la precisión de la herramienta, estas suelen enviar fragmentos de los datos que lee de vuelta a casa. Esto significa que, si escribe un informe con información confidencial sobre vulnerabilidades de clientes, podría estar infringiendo algún tipo de MSA o algo similar sin darse cuenta. Antes de usar herramientas como esta, es importante analizar su funcionalidad y si este tipo de comportamiento se puede desactivar.

Si tienes acceso a alguien que pueda realizar control de calidad y empiezas a intentar implementar un proceso, pronto descubrirás que, a medida que el equipo crece y aumenta el número de informes generados, el seguimiento puede volverse difícil. En un nivel básico, se podría usar una hoja de cálculo de Google o algo equivalente para asegurar que no se pierda información, pero si tienes mucho más personal (como consultores y gestores de proyectos) y tienes acceso a una herramienta como Jira, esta podría ser una solución mucho más escalable. Probablemente necesites un lugar central para almacenar tus informes, de modo que otras personas puedan acceder a ellos para realizar el proceso de control de calidad. Hay muchas opciones que podrían funcionar, pero elegir la mejor queda fuera del alcance de este curso.

Idealmente, la persona que realiza el control de calidad no debería ser responsable de realizar modificaciones significativas al informe. Si existen errores tipográficos, de redacción o de formato menores que deban corregirse con mayor rapidez que devolver el informe al autor para que lo modifique, probablemente no habrá problema. En el caso de evidencia faltante o mal ilustrada, hallazgos incompletos, contenido inutilizable del resumen ejecutivo, etc., el autor debería ser responsable de que el documento esté en condiciones presentables.

Obviamente, querrás revisar con diligencia los cambios realizados en tu informe (¡activa el Control de Cambios!) para evitar cometer los mismos errores en informes posteriores. Es una oportunidad de aprendizaje, así que no la desaproveches. Si es algo que ocurre con varias personas, podrías considerar añadirlo a tu lista de verificación de control de calidad para recordarles que deben solucionar esos problemas antes de enviar los informes a control de calidad. Pocas sensaciones son mejores en esta profesión que cuando un informe que escribiste pasa el control de calidad sin cambios.

Aunque parezca una mera formalidad, es bastante común emitir inicialmente un borrador del informe al cliente una vez finalizado el proceso de control de calidad. Una vez que el cliente reciba el borrador, deberá revisarlo y le informará si desea tener la oportunidad de revisarlo con usted para discutir las modificaciones y hacer preguntas. Si es necesario realizar cambios o actualizaciones al informe después de esta conversación, se pueden realizar y emitir una versión final. El informe final suele ser idéntico al borrador (si el cliente no necesita realizar cambios), pero solo indicará "Final" en lugar de "Borrador". Puede parecer frívolo, pero algunos auditores solo aceptan un informe final como un artefacto, por lo que podría ser muy importante para algunos clientes.

***

## <mark style="color:purple;">Reunión de revisión de informes</mark>

Una vez entregado el informe, es habitual darle al cliente aproximadamente una semana para revisarlo, reflexionar sobre sus ideas y ofrecerle una llamada para revisarlo y recopilar sus comentarios sobre el trabajo. Normalmente, esta llamada cubre los detalles técnicos de los hallazgos uno por uno y permite al cliente hacer preguntas sobre lo que se encontró y cómo se hizo. Estas llamadas pueden ser de gran ayuda para mejorar la presentación de este tipo de datos, así que preste mucha atención a la conversación. Si siempre responde las mismas preguntas, podría indicar que necesita ajustar su flujo de trabajo o la información que proporciona para responderlas antes de que el cliente las formule.

Una vez revisado y aceptado el informe por ambas partes, es habitual cambiar la designación `DRAFT` a `FINAL` y entregar la copia final al cliente. A partir de este momento, debemos archivar todos nuestros datos de prueba según las políticas de retención de nuestra empresa hasta que, como mínimo, se realice una nueva prueba de los hallazgos corregidos.

***

## <mark style="color:purple;">Para terminar</mark>

Estos son solo algunos consejos y trucos que hemos recopilado a lo largo de los años. Muchos de ellos son de sentido común. Vale la pena leer esta [publicación](https://blackhillsinfosec.com/how-to-not-suck-at-reporting-or-how-to-write-great-pentesting-reports/) del excelente equipo de Black Hills Information Security. El objetivo es presentar el resultado más profesional posible, contando una historia clara basada en nuestro arduo trabajo durante una evaluación técnica. Da lo mejor de ti y crea un resultado del que puedas estar orgulloso. Has dedicado muchas horas incansablemente a la administración de dominios. Aplica ese mismo celo a tus informes y serás un crack. En las últimas secciones de este módulo, analizaremos oportunidades para practicar nuestras habilidades de documentación e informes.
