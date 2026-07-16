
# Web App Scanning con OWASP ZAP

{% content-ref url="/pages/gs0z5fcuKuAB9oCBSu6W" %}
[Zap Scanner](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/web-proxies/zap-scanner.md)
{% endcontent-ref %}

## <mark style="color:$primary;">Lab</mark>

Las herramientas de pentesting de aplicaciones web pueden resultar muy útiles al realizar pruebas de penetración.&#x20;

En este ejercicio de laboratorio, veremos cómo usar [ZAProxy](https://www.zaproxy.org/) para escanear aplicaciones web e identificar diversas vulnerabilidades. &#x20;

Objetivo: Analizar la aplicación web con ZAProxy e identificar las posibles vulnerabilidades.&#x20;

### Hosts

Tenemos 10 objetivos para escanear:

<figure><img src="/files/jR8jPF9NSbgIKgo9ypk3" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Target 1 (bWAPP)</mark>

<figure><img src="/files/fDVqOJLgiVEdCkLc0cbu" alt=""><figcaption></figcaption></figure>

#### Abrimos la web en el navegador de ZAP

<figure><img src="/files/h1zhpmSeY8qqAutLRyLa" alt=""><figcaption></figcaption></figure>

Y nos logueamos con las credenciales bee:bug, automáticamente hace un reconocimiento pasivo de la web y nos lo incluye en la lista de sites:

<figure><img src="/files/UibCzIiEZX44GYEuoH2X" alt=""><figcaption></figcaption></figure>

### Login POST Request

Por ejemplo podemos hacer click derecho sobre un request y añadirlo al contexto:

<figure><img src="/files/ypy7wWqFLMDSPw2j9LMu" alt=""><figcaption></figcaption></figure>

En la nueva pestaña podemos seleccionar por ejemplo Authentication > Form-based:

<figure><img src="/files/HSNPNIG8eOxnb2KshlMa" alt=""><figcaption></figcaption></figure>

Seleccionamos el target y los datos POST:

<figure><img src="/files/ukwfeHXBrJI4Ajo4gWTX" alt=""><figcaption></figcaption></figure>

Y en users añadimos un nuevo usuario:

<figure><img src="/files/x2gsIMFAdC6YNPTc4zBe" alt=""><figcaption></figcaption></figure>

Añadimos la URL al Default Context:

<figure><img src="/files/3ObsWdDp0NmPZ4JvsEKL" alt=""><figcaption></figcaption></figure>

### Spidering

Una vez tenemos un usuario con el que podemos autenticarnos realizaremos un spidering completo del site con Click derecho > Attack > Spider:

<figure><img src="/files/1iTxfRQFeloUKxsfb5VE" alt=""><figcaption></figcaption></figure>

Seleccionamos el contexto y el usuario con el que podemos loguearnos e iniciamos el escaneo:

<figure><img src="/files/uUANGGVJp9xE8N0IWTph" alt=""><figcaption></figcaption></figure>

Eso automáticamente nos mapea completamente el sitio web con todos los directorios, a los cuales no podríamos acceder sin estar logueados:

<figure><img src="/files/N81twYja9PrNOcHWRPmb" alt=""><figcaption></figcaption></figure>

Por ejemplo a archivos que contengan contraseñas:

<figure><img src="/files/hxjwd1obqOhIVRhAFHQW" alt=""><figcaption></figcaption></figure>

### Escaneo activo

Click derecho sobre la URL > Attack > Active Scan:

<figure><img src="/files/x5xTv6Zm5afD9Nz0HyB6" alt=""><figcaption></figcaption></figure>

Incluimos el contexto y el usuario con el que podemos loguearnos:

<figure><img src="/files/u4ZtrPWli4yYRb5JH8GO" alt=""><figcaption></figcaption></figure>

#### Configuración de escaneos

Podemos configurar escaneos más o menos agresivos:

<figure><img src="/files/v1MbSyWy8UYsW6gENbHs" alt=""><figcaption></figcaption></figure>

Con eso directamente nos saca todas las posibles vulnerabilidades del site como SQL Injection o XSS entre otras:

<figure><img src="/files/eqfjqYl1dolq3Ub9mpWX" alt=""><figcaption></figcaption></figure>

### Escaneo masivo

Podemos navegar con ZAP y su navegador integrado a todas las URLs que queramos incluir en nuestro escaneo y añadirlas al contexto:

<figure><img src="/files/nf0RoJCn8FL2uCciOiT4" alt=""><figcaption></figcaption></figure>

Y hacer un active scan de todas a la vez:

<figure><img src="/files/58Uc6TdNWtJhzr5Zby8x" alt=""><figcaption></figcaption></figure>
