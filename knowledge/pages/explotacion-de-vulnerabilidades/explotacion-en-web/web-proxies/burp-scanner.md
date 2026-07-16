
# Burp Scanner

Una característica esencial de las herramientas de proxy web son sus escáneres web. Burp Suite incluye `Burp Scanner` un potente escáner para varios tipos de vulnerabilidades web, que utiliza `Crawler` para crear la estructura del sitio web y `Scanner` para el escaneo pasivo y activo.

Burp Scanner es una función exclusiva de la `versión Pro` y no está disponible en la versión gratuita Community de Burp Suite. Sin embargo, dado el amplio alcance que cubre Burp Scanner y las funciones avanzadas que incluye, se trata de una herramienta de nivel empresarial y, como tal, se espera que sea una función de pago.

***

## <mark style="color:purple;">Alcance del objetivo</mark>

Para iniciar un escaneo en Burp Suite, tenemos las siguientes opciones:

1. `Iniciar escaneo en una solicitud específica desde el historial de proxy`
2. `Iniciar un nuevo escaneo en un conjunto de objetivos`
3. `Iniciar un escaneo de los elementos dentro del alcance`

Para iniciar un escaneo sobre una solicitud específica del Historial de Proxy, podemos hacer click derecho sobre ella una vez que la ubiquemos en el historial, y luego seleccionar `Scan` para poder configurar el escaneo antes de ejecutarlo, o seleccionar `Passive/Active Scan` para iniciar rápidamente un escaneo con las configuraciones predeterminadas:

![](https://academy.hackthebox.com/storage/modules/110/burp_scan_request.jpg)

También podemos hacer clic en el botón `New Scan` de la pestaña `Dashboard`, que abrirá la ventana de configuración `New Scan` para configurar un análisis en un conjunto de objetivos personalizados. En lugar de crear un análisis personalizado desde cero, veamos cómo podemos utilizar el ámbito para definir correctamente qué se incluye o excluye de nuestros análisis mediante el `Target Scope`. El `Target Scope` se puede utilizar con todas las funciones de Burp para definir un conjunto personalizado de objetivos que se procesarán. Burp también nos permite limitar Burp a elementos dentro del ámbito para ahorrar recursos al ignorar cualquier URL fuera del ámbito.

Si vamos a ( `Target>Site map`), se mostrará un listado de todos los directorios y archivos que burp ha detectado en varias solicitudes que pasaron por su proxy:

![Mapa del sitio](https://academy.hackthebox.com/storage/modules/110/burp_site_map_before.jpg)

Para agregar un elemento a nuestro alcance, podemos hacer clic derecho sobre él y seleccionar `Add to scope`:

![Añadir al alcance](https://academy.hackthebox.com/storage/modules/110/burp_add_to_scope.jpg)

{% hint style="info" %}
**Nota**: Cuando agrega el primer elemento a su alcance, Burp le dará la opción de restringir sus funciones solo a los elementos dentro del alcance e ignorar cualquier elemento fuera del alcance.
{% endhint %}

También es posible que necesitemos excluir algunos elementos del ámbito si escanearlos puede ser peligroso o puede terminar nuestra sesión "como una función de cierre de sesión". Para excluir un elemento de nuestro ámbito, podemos hacer click derecho en cualquier elemento dentro del ámbito y seleccionar `Remove from scope`. Finalmente, podemos ir a ( `Target>Scope`) para ver los detalles de nuestro ámbito. Aquí, también podemos agregar/eliminar otros elementos y usar el control avanzado del ámbito para especificar patrones de expresiones regulares que se incluirán/excluirán.

![](https://academy.hackthebox.com/storage/modules/110/burp_target_scope.jpg)

***

## <mark style="color:purple;">Crawler</mark>

Una vez que tengamos nuestro scope listo, podemos ir a la pestaña `Dashboard` y hacer click en `New Scan` para configurar nuestro escaneo, que se completará automáticamente con nuestros elementos dentro del scope:

![Nuevo scan](https://academy.hackthebox.com/storage/modules/110/burp_new_scan.jpg)

Vemos que Burp nos da dos opciones de escaneo: `Crawl and Audit`y `Crawl`. Un Web Crawler navega por un sitio web accediendo a los enlaces que se encuentran en sus páginas, accediendo a los formularios y examinando las solicitudes que realiza para construir un mapa completo del sitio web. Al final, Burp Scanner nos presenta un mapa del objetivo, mostrando todos los datos de acceso público en un solo lugar. Si seleccionamos `Crawl and Audit`, Burp ejecutará su escáner después de su Crawler (como veremos más adelante).

{% hint style="info" %}
**Nota**: un análisis de rastreo solo sigue y mapea los enlaces que se encuentran en la página que especificamos y las páginas que se encuentran en ella. No realiza un análisis de fuzzing para identificar páginas a las que nunca se hace referencia, como lo harían dirbuster o ffuf. Esto se puede hacer con Burp Intruder o Content Discovery y luego agregarlo al alcance, si es necesario.
{% endhint %}

Seleccionemos `Crawl` como inicio y vayamos a la pestaña `Scan configuration` para configurar nuestro escaneo. Desde aquí, podemos elegir hacer clic en `New` para crear una configuración personalizada, que nos permitirá establecer configuraciones como la velocidad o el límite de rastreo, si Burp intentará iniciar sesión en algún formulario de inicio de sesión y algunas otras configuraciones. Para simplificar, haremos clic en el botón `Select from library`, que nos brinda algunas configuraciones preestablecidas entre las que podemos elegir (o configuraciones personalizadas que definimos previamente):

![](https://academy.hackthebox.com/storage/modules/110/burp_crawl_config.jpg)

Seleccionaremos la opción `Crawl strategy - fastest` y continuaremos hasta la pestaña `Application login`. En esta pestaña, podemos agregar un conjunto de credenciales para que Burp intente iniciar sesión en cualquier formulario o campo de inicio de sesión que encuentre. También podemos registrar un conjunto de pasos realizando un inicio de sesión manual en el navegador preconfigurado, de modo que Burp sepa qué pasos seguir para obtener una sesión de inicio de sesión. Esto puede ser esencial si estuviéramos ejecutando nuestro escaneo utilizando un usuario autenticado, lo que nos permitiría cubrir partes de la aplicación web a las que Burp no podría tener acceso de otra manera. Como no tenemos credenciales, lo dejaremos vacío.

Con eso, podemos hacer click en el botón `Ok` para iniciar nuestro análisis de rastreo. Una vez que comience nuestro análisis, podemos ver su progreso en la pestaña `Dashboard` que se encuentra debajo de `Tasks`:

![Configuración de rastreo](https://academy.hackthebox.com/storage/modules/110/burp_crawl_progress.jpg)

También podemos hacer clic en el botón `View details` de las tareas para ver más detalles sobre el análisis en ejecución o hacer clic en el icono de engranaje para personalizar aún más nuestras configuraciones de análisis. Finalmente, una vez que nuestro análisis esté completo, veremos `Crawl Finished` con la información de la tarea y luego podemos volver a ( `Target>Site map`) para ver el mapa del sitio actualizado:

![Mapa del sitio](https://academy.hackthebox.com/storage/modules/110/burp_site_map_after.jpg)

***

## <mark style="color:purple;">Escáner pasivo</mark>

Ahora que el mapa del sitio está completamente creado, podemos seleccionar escanear este objetivo en busca de posibles vulnerabilidades. Cuando elegimos la opción `Crawl and Audit` en el cuadro de diálogo `New Scan`, Burp realizará dos tipos de escaneos: `Passive Vulnerability Scan` y `Active Vulnerability Scan`.

A diferencia de un análisis activo, un análisis pasivo no envía ninguna solicitud nueva, sino que analiza el origen de las páginas ya visitadas en el objetivo/ámbito y luego intenta identificar `potenciales` vulnerabilidades. Esto es muy útil para un análisis rápido de un objetivo específico, como etiquetas HTML faltantes o posibles vulnerabilidades XSS basadas en DOM. Sin embargo, sin enviar ninguna solicitud para probar y verificar estas vulnerabilidades, un análisis pasivo solo puede sugerir una lista de vulnerabilidades potenciales. Aun así, Burp Passive Scanner proporciona un nivel de vulnerabilidad `Confidence` para cada vulnerabilidad identificada, lo que también es útil para priorizar las vulnerabilidades potenciales.

Empecemos por intentar realizar un escaneo pasivo únicamente. Para ello, podemos seleccionar nuevamente el objetivo en ( `Target>Site map`) o una solicitud en Burp Proxy History, luego hacer click derecho sobre él y seleccionar `Do passive scan` o `Passively scan this target`. El escaneo pasivo comenzará a ejecutarse y su tarea también se puede ver en la pestaña `Dashboard`. Una vez que finalice el escaneo, podemos hacer clic en `View Details` para revisar las vulnerabilidades identificadas y luego seleccionar la pestaña `Issue activity`:

![](https://academy.hackthebox.com/storage/modules/110/burp_passive_scan.jpg)

Alternativamente, podemos ver todos los problemas identificados en el panel `Issue activity` de la pestaña `Dashboard`. Como podemos ver, se muestra la lista de vulnerabilidades potenciales, su gravedad y su nivel de confianza. Por lo general, queremos buscar vulnerabilidades con nivel de gravedad `High` y nivel de confianza `Certain`. Sin embargo, deberíamos incluir todos los niveles de gravedad y nivel de confianza para aplicaciones web muy sensibles, con especial atención a la gravedad `High`  y el nivel de confianza `Confident/Firm`.

***

## <mark style="color:purple;">Escáner activo</mark>

Finalmente llegamos a la parte más potente de Burp Scanner, que es su escáner de vulnerabilidades activo. Un análisis activo ejecuta un análisis más completo que un análisis pasivo, de la siguiente manera:

1. Comienza ejecutando un rastreo y un analizador de vulnerabilidades web (como dirbuster/ffuf) para identificar todas las páginas posibles.
2. Ejecuta un escaneo pasivo en todas las páginas identificadas.
3. Comprueba cada una de las vulnerabilidades identificadas en el escaneo pasivo y envía solicitudes para verificarlas.
4. Realiza un análisis de JavaScript para identificar otras vulnerabilidades potenciales.
5. Analiza varios puntos de inserción y parámetros identificados para buscar vulnerabilidades comunes como XSS, inyección de comandos, inyección SQL y otras vulnerabilidades web comunes.

El escáner Burp Active se considera una de las mejores herramientas en ese campo y el equipo de investigación de Burp lo actualiza con frecuencia para buscar vulnerabilidades web recientemente identificadas.

Podemos iniciar un escaneo activo de manera similar a cómo iniciamos un escaneo pasivo, seleccionando el botón derecho del menú `Do active scan` en una solicitud en Burp Proxy History. Alternativamente, podemos ejecutar un escaneo en nuestro scope con el botón `New Scan` en la pestaña `Dashboard`, lo que nos permitirá configurar nuestro escaneo activo. Esta vez, seleccionaremos la opción `Crawl and Audit`, que realizará todos los puntos anteriores y todo lo que hemos discutido hasta ahora.

También podemos configurar las configuraciones de Crawl (como comentamos anteriormente) y las configuraciones de Audit (auditoría). Las configuraciones de Audit (auditoría) nos permiten seleccionar qué tipo de vulnerabilidades queremos escanear (por defecto todas), dónde el escáner intentará insertar sus payloads, además de muchas otras configuraciones útiles. Una vez más, podemos seleccionar una configuración preestablecida con el botón `Select from library`. Para nuestra prueba, como nos interesan las vulnerabilidades `High` que nos permitan obtener el control sobre el servidor backend, seleccionaremos la opción `Audit checks - critical issues only`. Por último, podemos añadir los datos de acceso, como vimos anteriormente con las configuraciones de Crawl (rastreo).

Una vez que seleccionamos nuestras configuraciones, podemos hacer clic en el botón `Ok` para iniciar el escaneo, y la tarea de escaneo activa debe agregarse en el panel `Tasks` en la pestaña `Dashboard`:

![Escaneo activo](https://academy.hackthebox.com/storage/modules/110/burp_active_scan.jpg)

El análisis ejecutará todos los pasos mencionados anteriormente, por lo que tardará mucho más en finalizar que nuestros análisis anteriores, según las configuraciones que hayamos seleccionado. Mientras se ejecuta el análisis, podemos ver las distintas solicitudes que realiza haciendo clic en el botón `View details` y seleccionando la pestaña `Logger`, o yendo a la pestaña `Logger` en Burp, que muestra todas las solicitudes que se realizaron o que Burp realizó:

![Registrador](https://academy.hackthebox.com/storage/modules/110/burp_logger.jpg)

Una vez finalizado el análisis, podemos consultar el panel `Issue activity` de la pestaña `Dashboard` para ver y filtrar todos los problemas identificados hasta el momento. En el filtro que se encuentra sobre los resultados, seleccionemos `High` y veamos nuestros resultados filtrados `Certain`:

![Altas vulnerabilidades](https://academy.hackthebox.com/storage/modules/110/burp_high_vulnerabilities.jpg)

Vemos que Burp ha identificado una vulnerabilidad `OS command injection`, a la que se le asigna un nivel de gravedad `High` y `Firm` de confianza. Como Burp está totalmente seguro de que esta vulnerabilidad grave existe, podemos leer sobre ella haciendo clic en ella y leyendo el aviso que se muestra y ver la solicitud enviada y la respuesta recibida, para poder saber si la vulnerabilidad puede ser explotada o si representa una amenaza para el servidor web:

![Detalles vulnerables](https://academy.hackthebox.com/storage/modules/110/burp_vuln_details.jpg)

***

## <mark style="color:purple;">Informes</mark>

Finalmente, una vez que se hayan completado todos los análisis y se hayan identificado todos los problemas potenciales, podemos ir a ( `Target > Site map`), hacer clic derecho en nuestro objetivo y seleccionar ( `Issue > Report issues for this host`). Se nos solicitará que seleccionemos el tipo de exportación para el informe y qué información nos gustaría incluir en el informe. Una vez que exportemos el informe, podemos abrirlo en cualquier navegador web para ver sus detalles:

![Informe de escaneo](https://academy.hackthebox.com/storage/modules/110/burp_scan_report.jpg)

Como podemos ver, el informe de Burp está muy organizado y se puede personalizar para incluir solo problemas seleccionados por gravedad/confianza. También muestra detalles de prueba de concepto sobre cómo explotar la vulnerabilidad e información sobre cómo remediarla. Estos informes se pueden utilizar como datos complementarios para los informes detallados que preparamos para nuestros clientes o los desarrolladores de aplicaciones web cuando realizamos una prueba de penetración web o se pueden almacenar para nuestra referencia futura.&#x20;

Nunca debemos simplemente exportar un informe de cualquier herramienta de penetración y enviarlo a un cliente como el producto final. En cambio, los informes y los datos generados por las herramientas pueden ser útiles como datos de apéndice para los clientes que pueden necesitar los datos de escaneo sin procesar para los esfuerzos de remediación o para importarlos a un panel de seguimiento.
