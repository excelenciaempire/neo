
# Prevención en carga de archivos

A lo largo de este módulo, hemos analizado varios métodos para explotar diferentes vulnerabilidades en la carga de archivos. En cualquier prueba de penetración o ejercicio de Bug Bounty en el que participemos, debemos poder informar sobre las medidas que se deben tomar para rectificar las vulnerabilidades identificadas.

En esta sección se analizará lo que podemos hacer para garantizar que nuestras funciones de carga de archivos estén codificadas de forma segura y protegidas contra la explotación y qué puntos de acción podemos recomendar para cada tipo de vulnerabilidad de carga de archivos.

***

## <mark style="color:purple;">Validación de extensión</mark>

El primer tipo de vulnerabilidad de carga, y el más común, que analizamos en este módulo fue la validación de extensiones de archivos. Las extensiones de archivos desempeñan un papel importante en la ejecución de archivos y scripts, ya que la mayoría de los servidores y aplicaciones web tienden a utilizar extensiones de archivos para establecer sus propiedades de ejecución. Por este motivo, debemos asegurarnos de que nuestras funciones de carga de archivos puedan gestionar de forma segura la validación de extensiones.

Si bien incluir extensiones en la lista blanca siempre es más seguro, como hemos visto anteriormente, se recomienda usar ambas opciones, incluyendo las extensiones permitidas en la lista blanca y las extensiones peligrosas en la lista negra. De esta manera, la lista negra evitará la carga de scripts maliciosos si alguna vez se pasa por alto la lista blanca (por ejemplo, `shell.php.jpg`). El siguiente ejemplo muestra cómo se puede hacer esto con una aplicación web PHP, pero el mismo concepto se puede aplicar a otros frameworks:

```php
$fileName = basename($_FILES["uploadFile"]["name"]);

// blacklist test
if (preg_match('/^.+\.ph(p|ps|ar|tml)/', $fileName)) {
    echo "Only images are allowed";
    die();
}

// whitelist test
if (!preg_match('/^.*\.(jpg|jpeg|png|gif)$/', $fileName)) {
    echo "Only images are allowed";
    die();
}
```

Vemos que con las extensiones incluidas en la lista negra, la aplicación web comprueba `si la extensión existe en algún lugar dentro del nombre del archivo`, mientras que con las listas blancas, la aplicación web comprueba `si el nombre del archivo termina con la extensión`. Además, también deberíamos aplicar la validación de archivos tanto en el back-end como en el front-end. Incluso si la validación en el front-end se puede omitir fácilmente, reduce las posibilidades de que los usuarios carguen archivos no deseados, lo que podría activar un mecanismo de defensa y enviarnos una alerta falsa.

***

## <mark style="color:purple;">Validación de contenido</mark>

Como también hemos aprendido en este módulo, la validación de la extensión no es suficiente, ya que también debemos validar el contenido del archivo. No podemos validar una sin la otra y siempre debemos validar tanto la extensión del archivo como su contenido. Además, siempre debemos asegurarnos de que la extensión del archivo coincida con el contenido del archivo.

El siguiente ejemplo nos muestra cómo podemos validar la extensión del archivo a través de la lista blanca y validar tanto la firma del archivo como el encabezado HTTP Content-Type, al tiempo que garantizamos que ambos coincidan con nuestro tipo de archivo esperado:

```php
$fileName = basename($_FILES["uploadFile"]["name"]);
$contentType = $_FILES['uploadFile']['type'];
$MIMEtype = mime_content_type($_FILES['uploadFile']['tmp_name']);

// whitelist test
if (!preg_match('/^.*\.png$/', $fileName)) {
    echo "Only PNG images are allowed";
    die();
}

// content test
foreach (array($contentType, $MIMEtype) as $type) {
    if (!in_array($type, array('image/png'))) {
        echo "Only PNG images are allowed";
        die();
    }
}
```

***

## <mark style="color:purple;">Divulgación de directorio de carga</mark>

Otra cosa que debemos evitar es revelar el directorio de subidas o proporcionar acceso directo al archivo subido. Siempre se recomienda ocultar el directorio de subidas a los usuarios finales y solo permitirles descargar los archivos subidos a través de una página de descarga.

Podemos escribir un script `download.php` para obtener el archivo solicitado del directorio de carga y luego descargarlo para el usuario final. De esta manera, la aplicación web oculta el directorio de carga y evita que el usuario acceda directamente al archivo cargado. Esto puede reducir significativamente las posibilidades de acceder a un script cargado de forma malintencionada para ejecutar código.

Si utilizamos una página de descarga, debemos asegurarnos de que el script `download.php` solo otorgue acceso a los archivos que son propiedad de los usuarios (es decir, evitar vulnerabilidades `IDOR/LFI`) y que los usuarios no tengan acceso directo al directorio de carga (es decir, `error 403`). Esto se puede lograr utilizando los encabezados `Content-Disposition` y `nosniff` y utilizando un encabezado preciso `Content-Type`

Además de restringir el directorio de subidas, también deberíamos aleatorizar los nombres de los archivos subidos en el almacenamiento y almacenar sus nombres originales "saneados" en una base de datos. Cuando el script `download.php` necesita descargar un archivo, obtiene su nombre original de la base de datos y se lo proporciona al usuario en el momento de la descarga. De esta manera, los usuarios no conocerán el directorio de subidas ni el nombre del archivo subido. También podemos evitar vulnerabilidades causadas por inyecciones en los nombres de los archivos, como vimos en la sección anterior.

Otra cosa que podemos hacer es almacenar los archivos subidos en un servidor o contenedor independiente. Si un atacante puede obtener la ejecución remota de código, solo comprometería el servidor de subidas, no todo el servidor back-end. Además, los servidores web se pueden configurar para evitar que las aplicaciones web accedan a archivos fuera de sus directorios restringidos mediante configuraciones como (`open_basedir`) en PHP.

***

## <mark style="color:purple;">Más seguridad</mark>

Los consejos anteriores deberían reducir significativamente las posibilidades de cargar y acceder a un archivo malicioso. Podemos tomar algunas otras medidas para garantizar que el servidor back-end no se vea comprometido si se ignora alguna de las medidas anteriores.

Una configuración crítica que podemos agregar es deshabilitar funciones específicas que se pueden usar para ejecutar comandos del sistema a través de la aplicación web. Por ejemplo, para hacerlo en PHP, podemos usar la `disable_functions`configuración en `php.ini`y agregar funciones peligrosas como `exec`, `shell_exec`, `system`, `passthru`, y algunas otras.

Otra cosa que deberíamos hacer es desactivar la visualización de errores del sistema o del servidor para evitar la divulgación de información confidencial. Siempre deberíamos gestionar los errores a nivel de la aplicación web e imprimir errores simples que expliquen el error sin revelar ningún detalle confidencial o específico, como el nombre del archivo, el directorio de carga o los errores sin procesar.

Por último, a continuación se presentan algunos otros consejos que debemos tener en cuenta para nuestras aplicaciones web:

* Limitar el tamaño del archivo
* Actualice todas las bibliotecas utilizadas
* Analizar los archivos cargados en busca de malware o cadenas maliciosas
* Utilice un firewall de aplicaciones web (WAF) como capa secundaria de protección

Una vez que implementemos todas las medidas de seguridad que se describen en esta sección, la aplicación web debería ser relativamente segura y no vulnerable a las amenazas comunes de carga de archivos. Al realizar una prueba de penetración web, podemos usar estos puntos como una lista de verificación y proporcionar los que falten a los desarrolladores para que completen los espacios vacíos.
