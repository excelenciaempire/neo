
# Prevención de Command Injection

Ahora deberíamos tener una comprensión sólida de cómo se producen las vulnerabilidades de inyección de comandos y cómo se pueden eludir ciertas mitigaciones, como los filtros de caracteres y comandos. En esta sección, analizaremos los métodos que podemos utilizar para evitar las vulnerabilidades de inyección de comandos en nuestras aplicaciones web y configurar correctamente el servidor web para evitarlas.

***

## <mark style="color:purple;">Comandos del sistema</mark>

Siempre debemos evitar el uso de funciones que ejecuten comandos del sistema, especialmente si utilizamos la entrada del usuario con ellas. Incluso cuando no introducimos directamente la entrada del usuario en estas funciones, un usuario puede influir indirectamente en ellas, lo que puede acabar provocando una vulnerabilidad de inyección de comandos.

En lugar de utilizar funciones de ejecución de comandos del sistema, deberíamos utilizar funciones integradas que realicen la funcionalidad necesaria, ya que los lenguajes de back-end suelen tener implementaciones seguras de este tipo de funcionalidades. Por ejemplo, supongamos que queremos probar si un host en particular está activo con `PHP`. En ese caso, podemos utilizar la función `fsockopen` en su lugar, que no debería ser explotable para ejecutar comandos arbitrarios del sistema.

Si necesitamos ejecutar un comando del sistema y no encontramos ninguna función incorporada que realice la misma función, nunca deberíamos usar directamente la entrada del usuario con estas funciones, sino que siempre deberíamos validar y depurar la entrada del usuario en el back-end. Además, deberíamos intentar limitar el uso de este tipo de funciones tanto como sea posible y solo usarlas cuando no haya una alternativa incorporada a la funcionalidad que necesitamos.

***

## <mark style="color:purple;">Validación de inputs</mark>

Ya sea que utilicemos funciones integradas o funciones de ejecución de comandos del sistema, siempre debemos validar y luego sanitizar los inputs o entradas del usuario. La validación de la entrada se realiza para garantizar que coincida con el formato esperado para la entrada, de modo que la solicitud se rechace si no coincide. En nuestra aplicación web de ejemplo, vimos que hubo un intento de validación de entrada en el front-end, pero la validación de entrada debe realizarse tanto en el front-end como en el back-end.

En `PHP`, como muchos otros lenguajes de desarrollo web, hay filtros integrados para una variedad de formatos estándar, como correos electrónicos, URL e incluso IP, que se pueden usar con la función `filter_var`, de la siguiente manera:

```php
if (filter_var($_GET['ip'], FILTER_VALIDATE_IP)) {
    // call function
} else {
    // deny request
}
```

Si quisiéramos validar un formato diferente que no sea el estándar, entonces podemos usar una expresión regular `regex` con la función `preg_match`. Lo mismo se puede lograr con `JavaScript` tanto para el front-end como para el back-end (es decir, `NodeJS`), de la siguiente manera:

```javascript
if(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ip)){
    // call function
}
else{
    // deny request
}
```

Al igual que `PHP` con `NodeJS` también podemos utilizar bibliotecas para validar varios formatos estándar, como [is-ip](https://www.npmjs.com/package/is-ip) por ejemplo, que podemos instalar con `npm`, y luego utilizar la función `isIp(ip)` en nuestro código. Puedes leer los manuales de otros lenguajes, como [.NET](https://learn.microsoft.com/en-us/aspnet/web-pages/overview/ui-layouts-and-themes/validating-user-input-in-aspnet-web-pages-sites) o [Java](https://docs.oracle.com/cd/E13226_01/workshop/docs81/doc/en/workshop/guide/netui/guide/conValidatingUserInput.html?skipReload=true) , para saber cómo validar la entrada del usuario en cada lenguaje respectivo.

***

## <mark style="color:purple;">Sanitización de inputs</mark>

La parte más importante para prevenir cualquier vulnerabilidad de inyección es la sanitización de inputs, lo que significa eliminar cualquier carácter especial innecesario de la entrada del usuario. La limpieza de la entrada siempre se realiza después de la validación de la entrada. Incluso después de que hayamos validado que la entrada del usuario proporcionada está en el formato correcto, aún debemos realizar la limpieza y eliminar cualquier carácter especial que no sea necesario para el formato específico, ya que hay casos en los que la validación de la entrada puede fallar (por ejemplo, una expresión regular incorrecta).

En nuestro código de ejemplo, vimos que cuando estábamos trabajando con filtros de caracteres y comandos, se ponía en la lista negra ciertas palabras y se buscaban en la entrada del usuario. Generalmente, este no es un enfoque lo suficientemente bueno para evitar las inyecciones, y deberíamos usar funciones integradas para eliminar cualquier carácter especial. Podemos usar `preg_replace` para eliminar cualquier carácter especial de la entrada del usuario, de la siguiente manera:

```php
$ip = preg_replace('/[^A-Za-z0-9.]/', '', $_GET['ip']);
```

Como podemos ver, la expresión regular anterior solo permite caracteres alfanuméricos (`A-Za-z0-9`) y permite un carácter de punto (`.`) según sea necesario para las direcciones IP. Cualquier otro carácter se eliminará de la cadena. Se puede hacer lo mismo con `JavaScript`, de la siguiente manera:

```javascript
var ip = ip.replace(/[^A-Za-z0-9.]/g, '');
```

También podemos utilizar la biblioteca DOMPurify para un back-end `NodeJS`, de la siguiente manera:

```javascript
import DOMPurify from 'dompurify';
var ip = DOMPurify.sanitize(ip);
```

En ciertos casos, es posible que queramos permitir todos los caracteres especiales (por ejemplo, comentarios de usuarios), entonces podemos usar la misma función `filter_var` que usamos con la validación de entrada y usar el filtro `escapeshellcmd` para escapar cualquier carácter especial, de modo que no pueda causar ninguna inyección. Para `NodeJS`, simplemente podemos usar la función `escape(ip)`. Sin embargo, como hemos visto en este módulo, escapar de caracteres especiales generalmente no se considera una práctica segura, ya que a menudo se puede evitar mediante diversas técnicas.

***

## <mark style="color:purple;">Configuración del servidor</mark>

Por último, debemos asegurarnos de que nuestro servidor back-end esté configurado de forma segura para reducir el impacto en caso de que el servidor web se vea comprometido. Algunas de las configuraciones que podemos implementar son:

* Utilice el firewall de aplicaciones web integrado del servidor web (por ejemplo, en Apache `mod_security`), además de un WAF externo (por ejemplo `Cloudflare` , `Fortinet`, `Imperva`...)
* Cumplir con el [principio de mínimo privilegio (PoLP)](https://en.wikipedia.org/wiki/Principle_of_least_privilege) ejecutando el servidor web como un usuario con pocos privilegios (por ejemplo, `www-data`)
* Impedir que el servidor web ejecute determinadas funciones (por ejemplo, en PHP `disable_functions=system,...`)
* Limitar el alcance accesible por la aplicación web a su carpeta (por ejemplo en PHP `open_basedir = '/var/www/html'`)
* Rechazar solicitudes con doble codificación y caracteres no ASCII en las URL
* Evite el uso de bibliotecas y módulos confidenciales/obsoletos (por ejemplo, [PHP CGI](https://www.php.net/manual/en/install.unix.commandline.php) )

Al final, incluso después de todas estas configuraciones y mitigaciones de seguridad, tenemos que realizar las técnicas de pruebas de penetración que aprendimos en este módulo para ver si alguna funcionalidad de la aplicación web aún puede ser vulnerable a la inyección de comandos. Como algunas aplicaciones web tienen millones de líneas de código, cualquier error en cualquier línea de código puede ser suficiente para introducir una vulnerabilidad. Por lo tanto, debemos intentar proteger la aplicación web complementando las mejores prácticas de codificación segura con pruebas de penetración exhaustivas.
