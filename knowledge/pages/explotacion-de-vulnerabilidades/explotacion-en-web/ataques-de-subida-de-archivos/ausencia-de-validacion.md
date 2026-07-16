
# Ausencia de validación

El tipo más básico de vulnerabilidad de carga de archivos ocurre cuando la aplicación web `no tiene ninguna forma de validación ni filtros` en los archivos cargados, lo que permite la carga de cualquier tipo de archivo de forma predeterminada.

Con este tipo de aplicaciones web vulnerables, podemos cargar directamente nuestro shell web o script de shell inverso a la aplicación web y luego, con solo visitar el script cargado, podemos interactuar con nuestro shell web o enviar el shell inverso.

***

## <mark style="color:purple;">Carga de archivos arbitrarios</mark>

En este ejemplo de [Hack the Box Academy](https://academy.hackthebox.com/module/136/section/1260), veremos una aplicación web `Employee File Manager`, que nos permite subir archivos personales a la aplicación web:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_file_manager.jpg" alt=""><figcaption></figcaption></figure>

La aplicación web no menciona nada sobre qué tipos de archivos están permitidos, y podemos arrastrar y soltar cualquier archivo que queramos, y su nombre aparecerá en el formulario de carga, incluidos los archivos `.php`:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_file_selected_php_file.jpg" alt=""><figcaption></figcaption></figure>

Además, si hacemos clic en el formulario para seleccionar un archivo, el cuadro de diálogo del selector de archivos no especifica ningún tipo de archivo, dice `All Files` para el tipo de archivo, lo que también puede sugerir que no se especifica ningún tipo de restricciones o limitaciones para la aplicación web:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_file_selection_dialog.jpg" alt=""><figcaption></figcaption></figure>

Todo esto nos dice que el programa parece no tener restricciones de tipo de archivo en el front-end, y si no se especificaron restricciones en el back-end, podríamos cargar tipos de archivos arbitrarios al servidor back-end para obtener control total sobre él.

***

## <mark style="color:purple;">Identificación de la tecnología</mark>

Necesitamos cargar un script malicioso para probar si podemos cargar cualquier tipo de archivo al servidor back-end y probar si podemos usarlo para explotar el servidor back-end. Muchos tipos de scripts pueden ayudarnos a explotar aplicaciones web mediante la carga de archivos arbitrarios, los más comunes son un [`Web Shell`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/webshells.md) o un [`Reverse Shell`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/reverse-shells.md).

Un Web Shell nos proporciona un método sencillo para interactuar con el servidor back-end al aceptar comandos de shell e imprimir su salida en el navegador web. Un Web Shell debe estar escrito en el mismo lenguaje de programación que ejecuta el servidor web, ya que ejecuta funciones y comandos específicos de la plataforma para ejecutar comandos del sistema en el servidor back-end, lo que hace que los Web Shell no sean scripts multiplataforma. Por lo tanto, el primer paso sería identificar qué lenguaje ejecuta la aplicación web.

Esto suele ser relativamente sencillo, ya que a menudo podemos ver la extensión de la página web en las URL, lo que puede revelar el lenguaje de programación que ejecuta la aplicación web. Sin embargo, en ciertos frameworks y lenguajes web, se utilizan `Web Routes` para mapear las URL a las páginas web, en cuyo caso la extensión de la página web puede no mostrarse. Además, la explotación de la carga de archivos también sería diferente, ya que nuestros archivos cargados pueden no ser directamente enrutables o accesibles.

Un método sencillo para determinar en qué lenguaje se ejecuta la aplicación web es visitar la página `/index.ext`, donde podríamos ir intercambiando `ext` con varias extensiones web comunes, como `php`, `asp`, `aspx`, entre otras, para ver si existe alguna de ellas.

Por ejemplo, cuando visitamos nuestro ejercicio a continuación, vemos su URL como `http://SERVER_IP:PORT/`, ya que la página `index` suele estar oculta de forma predeterminada. Pero, si intentamos visitar `http://SERVER_IP:PORT/index.php`, obtendremos la misma página, lo que significa que se trata de una aplicación web `PHP`. No necesitamos hacer esto manualmente, por supuesto, ya que podemos usar una herramienta como [Burp Intruder](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/web-proxies/burp-intruder.md) para realizar un fuzzing de la extensión del archivo utilizando una lista de palabras [de extensiones web](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-extensions.txt) , como veremos en las próximas secciones. Sin embargo, este método puede no ser siempre preciso, ya que la aplicación web puede no utilizar páginas de índice o puede utilizar más de una extensión web.

Existen otras técnicas que pueden ayudar a identificar las tecnologías que ejecutan la aplicación web, como el uso de la extensión [Wappalyzer](https://www.wappalyzer.com/) , que está disponible para todos los navegadores principales. Una vez agregada a nuestro navegador, podemos hacer clic en su icono para ver todas las tecnologías que ejecutan la aplicación web:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_wappalyzer.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, la extensión no solo nos indicó que la aplicación web se ejecuta en `PHP`, sino que también identificó el tipo y la versión del servidor web, el sistema operativo back-end y otras tecnologías en uso. Estas extensiones son esenciales en el arsenal de un evaluador de penetración web, aunque siempre es mejor conocer métodos manuales alternativos para identificar el marco web, como el método que analizamos anteriormente.

También podemos ejecutar escáneres web para identificar el marco web, como los escáneres Burp/ZAP u otras herramientas de evaluación de vulnerabilidades web. Al final, una vez que identificamos el lenguaje que ejecuta la aplicación web, podemos cargar un script malicioso escrito en el mismo lenguaje para explotar la aplicación web y obtener control remoto sobre el servidor back-end.

***

## <mark style="color:purple;">Identificación de vulnerabilidades</mark>

Ahora que hemos identificado la tecnología que ejecuta la aplicación web y su lenguaje de programación, podemos probar si podemos cargar un archivo con la misma extensión. Como prueba inicial para identificar si podemos cargar archivos arbitrarios `PHP`, creemos un script básico `Hello World` para probar si podemos ejecutar código `PHP` con nuestro archivo cargado.

Para ello, escribiremos `<?php echo "Hello HTB";?>` en `test.php`, e intentaremos subirlo a la aplicación web:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_upload_php.jpg" alt=""><figcaption></figcaption></figure>

Parece que el archivo se ha cargado correctamente, ya que aparece un mensaje que dice `File successfully uploaded`, lo que significa que la aplicación web `no tiene ningún tipo de validación de archivos en el back-end`. Ahora, podemos hacer clic en el botón `Download` y la aplicación web nos llevará al archivo cargado:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_hello_htb.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, la página imprime nuestro mensaje `Hello HTB`, lo que significa que se ejecutó la función `echo` para imprimir nuestra cadena y que ejecutamos el código `PHP` correctamente en el servidor back-end. Si la página no pudiera ejecutar el código PHP, veríamos nuestro código fuente impreso en la página.

En la siguiente sección, veremos cómo explotar esta vulnerabilidad para ejecutar código en el servidor back-end y tomar control sobre él.

***

## Caso práctico

Intente cargar un script PHP que ejecute el comando (`hostname`) en el servidor back-end y envíe la primera palabra como respuesta.

```
Objetivo: 94.237.59.63:38185
```

Vamos a crear un archivo `shell.php` con el siguiente código:

```php
<?php system('hostname'); ?>
```

Lo subimos correctamente, y si accedemos a `/uploads/shell.php` ejecuta el comando y nos devuelve el hostname:

<figure><img src="/files/psLw6g0AnIu58kCysaXL" alt=""><figcaption></figcaption></figure>
