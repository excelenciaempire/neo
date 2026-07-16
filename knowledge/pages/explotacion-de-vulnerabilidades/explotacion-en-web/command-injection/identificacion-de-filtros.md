
# Identificación de filtros

Como hemos visto en la sección anterior, incluso si los desarrolladores intentan proteger la aplicación web contra las inyecciones, aún puede ser explotable si no se codificó de forma segura. Otro tipo de mitigación de la inyección es utilizar caracteres y palabras incluidos en la lista negra en el back-end para detectar intentos de inyección y denegar la solicitud si alguna de ellas los contenía.&#x20;

Otra capa adicional es utilizar firewalls de aplicaciones web (WAF), que pueden tener un alcance más amplio y varios métodos de detección de inyecciones y prevenir otros ataques como inyecciones SQL o ataques XSS.

En esta sección veremos algunos ejemplos de cómo se pueden detectar y bloquear las inyecciones de comandos y cómo podemos identificar qué se está bloqueando.

***

## <mark style="color:purple;">Detección de filtro/WAF</mark>

Comencemos visitando la aplicación web del ejercicio que se encuentra al final de esta sección. Vemos la misma aplicación web `Host Checker` que hemos estado explotando, pero ahora tiene algunas mitigaciones bajo la manga. Podemos ver que si probamos los operadores anteriores que probamos, como ( `;`, `&&`, `||`), obtenemos el mensaje de error `invalid input`:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_1.jpg" alt=""><figcaption></figcaption></figure>

Esto indica que algo que enviamos activó un mecanismo de seguridad que rechazó nuestra solicitud. Este mensaje de error se puede mostrar de varias maneras. En este caso, lo vemos en el campo donde se muestra el resultado, lo que significa que fue detectado y prevenido por la propia aplicación web PHP. Si el mensaje de error mostraba una página diferente, con información como nuestra IP y nuestra solicitud, esto puede indicar que fue rechazada por un WAF.

Revisemos la carga útil que enviamos:

```bash
127.0.0.1; whoami
```

Además de la IP (que sabemos que no está en la lista negra), enviamos:

1. Un carácter de punto y coma `;`
2. Un carácter espacial
3. Una orden `whoami`

Entonces, la aplicación web detectó un carácter o un comando en la lista negra, o ambos. Entonces, veamos cómo evitar cada uno de ellos.

***

## <mark style="color:purple;">Caracteres incluidos en la lista negra</mark>

Una aplicación web puede tener una lista de caracteres prohibidos y, si el comando los contiene, rechazará la solicitud. El código `PHP` puede ser similar al siguiente:

```php
$blacklist = ['&', '|', ';', ...SNIP...];
foreach ($blacklist as $character) {
    if (strpos($_POST['ip'], $character) !== false) {
        echo "Invalid input";
    }
}
```

Si algún carácter de la cadena que enviamos coincide con un carácter de la lista negra, nuestra solicitud será rechazada. Antes de comenzar a intentar eludir el filtro, debemos intentar identificar qué carácter provocó la solicitud rechazada.

### Cómo identificar carácteres incluidos en la lista negra

Reduzcamos nuestra solicitud a un carácter a la vez y veamos cuándo se bloquea. Sabemos que la carga útil (`127.0.0.1`) funciona, así que comencemos agregando el punto y coma (`127.0.0.1;`):&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_2.jpg" alt=""><figcaption></figcaption></figure>

Aún recibimos un error `invalid input` , que significa que un punto y coma está en la lista negra. Por lo tanto, veamos si todos los operadores de inyección que analizamos anteriormente están en la lista negra.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 83.136.250.196:33250
```

Pruebe todos los demás operadores de inyección para ver si alguno de ellos no está en la lista negra. ¿Cuál de los siguientes (nueva línea, &, |) no está en la lista negra de la aplicación web?

<figure><img src="/files/v65GjTL5NfxSLPsZW8dp" alt=""><figcaption></figcaption></figure>

Probando todos los caracteres el único que no nos da error es el de nueva línea `%0a`
