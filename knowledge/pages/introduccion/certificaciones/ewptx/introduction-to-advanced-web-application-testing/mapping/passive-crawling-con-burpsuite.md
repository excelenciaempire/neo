
# Passive Crawling con BurpSuite

Mientras que HTTrack permite clonar un sitio para un análisis offline, el rastreo pasivo con Burp Suite adopta un enfoque diferente: construye el mapa del sitio **mientras navegas normalmente**, sin enviar peticiones adicionales al servidor. Esto lo convierte en la técnica más sigilosa y eficiente para las fases iniciales de reconocimiento.

***

## <mark style="color:$primary;">¿Qué es el rastreo pasivo?</mark>

El rastreo pasivo es una técnica en la que Burp Suite monitorea y analiza el tráfico que pasa a través de él (principalmente desde tu navegador), extrayendo automáticamente enlaces, rutas de API y otros endpoints **sin generar peticiones propias**.

A medida que navegas manualmente por una aplicación, Burp analiza el contenido de las respuestas, descubre nuevos endpoints a partir de hipervínculos, archivos JavaScript, formularios y respuestas JSON, y los añade a su mapa del sitio (Site Map). De esta forma, con cada clic que das, el mapa de la superficie de ataque se engrosa automáticamente.

La característica clave es la **no-intrusividad**: no envías ni una sola petición extra, solo observas, lo que minimiza el ruido en los logs del servidor y no activa alertas de seguridad prematuras.

***

## <mark style="color:$primary;">Configuración inicial</mark>

#### **Configuración básica del proxy**

Burp Suite Professional incluye un proxy HTTP/HTTPS que debe configurarse en tu navegador (normalmente en `127.0.0.1:8080`) para que todo el tráfico pase por él.

1. Abre Burp Suite Professional.
2. Ve a **Proxy > Options** y verifica que el listener esté activo.
3. Configura tu navegador para usar `127.0.0.1:8080` como proxy HTTP y HTTPS.

#### **Definición del alcance (Scope)**

Cuando añades los primeros elementos a tu alcance, Burp te ofrece la opción de restringir sus funciones solo a los elementos dentro de ese alcance, ignorando cualquier otro. Configurar el scope correctamente es el paso más importante para evitar ruido innecesario.

Puedes añadir elementos al scope de dos formas:

<table data-header-hidden><thead><tr><th width="246.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Método</td><td>Descripción</td></tr><tr><td><strong>Manual (Target > Scope)</strong></td><td>Introduce manualmente el dominio o la URL en la pestaña <strong>Include in Scope</strong>. Por ejemplo, añadir <code>example.org</code> implica que Burp solo considerará los recursos de <code>example.org</code> y los tratará como objetivo de la prueba.</td></tr><tr><td><strong>Contextual (desde Site Map o Proxy History)</strong></td><td>Haz clic derecho sobre el host o la petición que te interese y selecciona <strong>Add to scope</strong>.</td></tr></tbody></table>

Una buena práctica es activar la casilla **"Advanced Scope Control"** cuando necesites mayor precisión. Esto te permite definir reglas basadas en el protocolo, el host, el puerto o la ruta mediante expresiones regulares.

#### **Configuración del spider pasivo**

1. Ve al **Dashboard** (Panel de control).
2. Haz clic en **New live task...** (Nueva tarea en vivo).
3. Aparecerá un cuadro de diálogo donde deberás especificar el **tipo de tarea**: `Live Passive Crawl` (Rastreo Pasivo en Vivo).

   Esta tarea se ejecutará en segundo plano mientras navegas y se encargará de poblar el `Target > Site map` con los elementos derivados de las peticiones a la aplicación.

<figure><img src="/files/ZkyCrGsG0bSmQ98zDcxa" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Interpretación del Site Map</mark>

Una vez que el `Live Passive Crawl` está en marcha, cada interacción que tengas con la aplicación se traduce en nuevos nodos en el árbol del `Site Map`.

#### **Estructura del Site Map**

El `Target > Site map` es mucho más que un registro de URLs visitadas. Es una representación jerárquica de todos los recursos descubiertos.

* **Árbol de dominios**: Muestra la estructura de URLs exploradas de cada host.
* **Tabla de detalles**: Para cada nodo del árbol, la tabla muestra el método HTTP usado, la URL completa, el status code y la longitud de la respuesta.
* **Pestañas de Request/Response**: Al seleccionar un ítem, puedes inspeccionar las peticiones y respuestas completas, con funcionalidades como el `Pretty` (formateado) o el `Hex`.

#### **Ítems no solicitados (Unrequested items) en gris**

Un estado avanzado del rastreo pasivo se materializa cuando Burp descubre un endpoint pero aún no ha tenido oportunidad de enviar una petición para validarlo. Los elementos que el rastreo pasivo ha detectado pero que aún no has solicitado se muestran en color gris.

Estos ítems grises representan oportunidades potenciales. Puedes hacer clic derecho sobre ellos y seleccionar **Request in browser** o copiar la URL para abrirla manualmente en tu navegador y ver qué contiene el endpoint.

***

## <mark style="color:$primary;">Técnicas avanzadas y casos de uso</mark>

#### **1. Filtrado y búsqueda de endpoints específicos**

El campo de búsqueda en el `Site map` permite filtrar por extensiones de archivo, rutas críticas o términos de interés. La búsqueda de `openapi.json`, `swagger.json` o `api-docs` en el Site Map es una táctica fundamental para descubrir documentación de API.

#### **2. JavaScript Link Finder (extensión)**

`BurpJSLinkFinder` analiza automáticamente los archivos JavaScript que pasan por el proxy y extrae los endpoints vinculados, como rutas de API. Instálalo desde el BApp Store (es una extensión Java). Su principal campo de aplicación es el análisis de `Single Page Applications` (SPA), donde los endpoints suelen estar dinámicamente definidos en el código.

#### **3. Jsluice++**

Esta extensión extrae URLs, rutas y secretos de archivos JavaScript y los integra con Burp Suite.

* **Escaneo Activo**: Clasifica elementos, los añade al árbol de Hosts y permite reenviarlos directamente a Repeater/Intruder.
* **Escaneo Pasivo**: Analiza tráfico del proxy en tiempo real.

#### **4. Asset Discover**

`Asset Discover` es una extensión que utiliza técnicas de escaneo pasivo para descubrir nuevos activos (como subdominios) basándose en las respuestas HTTP.

#### **5. Análisis de APIs GraphQL**

La extensión `Grapher` extrae automáticamente todas las operaciones GraphQL (consultas, mutaciones, suscripciones) del tráfico proxy sin necesidad de habilitar la introspección. Es especialmente útil cuando la introspección está desactivada en producción.

Burp Suite también facilita el trabajo con GraphQL mediante el **GraphQL Editor Tab**, que separa la consulta de la solicitud y las variables, y el **Introspección Query Generator** para obtener el esquema completo de la API.

***

## <mark style="color:$primary;">Consejos de uso profesional</mark>

* **Define el alcance antes de empezar** – Ajusta el `Target Scope` al inicio de tu prueba y, en cuanto aparezca el primer nodo en el `Site Map`, selecciona **Add to Scope**. Burp ignorará automáticamente las peticiones fuera del dominio de la aplicación.
* **Combina el rastreo pasivo con el activo** – Puebla el mapa con el rastreo pasivo, espera a visualizar los 'ítems grises' y, una vez analizados, lanza un rastreo activo sobre los mismos con un tiempo limitado (`recurse depth = 2`) y una pausa de 300 ms entre peticiones para no saturar al servidor.
* **Revisa los ítems grises rápidamente** – Los 'unrequested items' aparecen como **sombreados en gris** en el Site Map. Ordénalos por la columna `Status Code` para ver rápidamente los que no se han solicitado. Haz clic derecho y selecciona **Request in browser** para abrirlos como si fueras un usuario normal.
* **Inspecciona todas las extensiones** – Haz clic derecho sobre el nodo raíz del sitio y selecciona **Show all files with extensions** para identificar todos los tipos de archivos presentes en el dominio: imágenes, código, scripts o archivos de backup.
* **Utiliza el Content Discovery adecuadamente** – Muchos pentesters lanzan el `Content Discovery` prematuramente. Si has definido bien el scope, puedes lanzarlo desde el `Site Map` con "Case sensitivity" activado y "Discovery engine" en modo **"Quiet"** para no realizar demasiadas peticiones por segundo.
* **Nunca clones un sitio sin permiso** – El uso de estas técnicas debe contar con la autorización explícita del propietario del sistema. Este es un requisito legal y ético fundamental.

***

## Referencias y recursos oficiales

* [Creación de tareas en vivo (Live Tasks) – PortSwigger](https://portswigger.net/burp/documentation/desktop/running-scans/live-tasks)
* [Revisión de ítems no solicitados – PortSwigger](https://portswigger.net/burp/documentation/desktop/tools/target/unrequested-items)
* [BApp Store (extensiones oficiales) – PortSwigger](https://portswigger.net/bappstore)
* [Guía de pruebas de seguridad web de OWASP (WSTG)](https://owasp.org/www-project-web-security-testing-guide/)
