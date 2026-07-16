
# Prevención de HTML Verb Tampering

Después de ver algunas formas de explotar vulnerabilidades de HTTP Verb Tampering, veamos cómo podemos protegernos contra este tipo de ataques. Las configuraciones y la codificación inseguras son las que suelen introducir vulnerabilidades de manipulación de verbos. En esta sección, veremos ejemplos de código y configuraciones vulnerables y analizaremos cómo podemos aplicarles parches.

***

## <mark style="color:purple;">Configuración insegura</mark>

Las vulnerabilidades HTTP Verb Tampering pueden ocurrir en la mayoría de los servidores web modernos, incluidos `Apache`, `Tomcat` y `ASP.NET`. La vulnerabilidad suele ocurrir cuando limitamos la autorización de una página a un conjunto particular de verbos/métodos HTTP, lo que deja desprotegidos a los demás métodos restantes.

El siguiente es un ejemplo de una configuración vulnerable para un servidor web Apache, que se encuentra en el archivo de configuración del sitio (por ejemplo `000-default.conf`), o en un archivo de configuración `.htaccess` de una página web:

```xml
<Directory "/var/www/html/admin">
    AuthType Basic
    AuthName "Admin Panel"
    AuthUserFile /etc/apache2/.htpasswd
    <Limit GET>
        Require valid-user
    </Limit>
</Directory>
```

Como podemos ver, esta configuración establece las configuraciones de autorización para el directorio web `admin`. Sin embargo, como se utiliza la palabra clave `<Limit GET>`, la configuración `Require valid-user` solo se aplicará a las solicitudes `GET`, lo que dejará la página accesible a través de `POST`. Incluso si se especificaran `GET` y `POST`, la página quedaría accesible a través de otros métodos, como `HEAD` o `OPTIONS`.

El siguiente ejemplo muestra la misma vulnerabilidad para una configuración de servidor `Tomcat`, que se puede encontrar en el archivo `web.xml` de una determinada aplicación web Java:

```xml
<security-constraint>
    <web-resource-collection>
        <url-pattern>/admin/*</url-pattern>
        <http-method>GET</http-method>
    </web-resource-collection>
    <auth-constraint>
        <role-name>admin</role-name>
    </auth-constraint>
</security-constraint>
```

Podemos ver que la autorización se limita únicamente al método `GET` con `http-method`, lo que deja la página accesible a través de otros métodos HTTP.

Finalmente, el siguiente es un ejemplo de una configuración `ASP.NET` que se encuentra en el archivo `web.config` de una aplicación web:

```xml
<system.web>
    <authorization>
        <allow verbs="GET" roles="admin">
            <deny verbs="GET" users="*">
        </deny>
        </allow>
    </authorization>
</system.web>
```

Una vez más, el alcance de permitir y denegar se limita al método GET, lo que deja la aplicación web accesible a través de otros métodos HTTP.

Los ejemplos anteriores muestran que no es seguro limitar la configuración de autorización a un verbo HTTP específico. Es por eso que siempre debemos evitar restringir la autorización a un método HTTP en particular y siempre permitir/denegar todos los verbos y métodos HTTP.

Si queremos especificar un solo método, podemos usar palabras clave seguras, como `LimitExcept` en Apache, `http-method-omission` en Tomcat y `add/remove` en ASP.NET, que cubren todos los verbos excepto los especificados.

Finalmente, para evitar ataques similares, generalmente deberíamos considerar deshabilitar/denegar todas las solicitudes HEAD a menos que la aplicación web lo requiera específicamente.

***

## <mark style="color:purple;">Codificación insegura</mark>

Si bien identificar y aplicar parches a configuraciones de servidores web inseguros es relativamente fácil, hacer lo mismo con códigos inseguros es mucho más complicado. Esto se debe a que, para identificar esta vulnerabilidad en el código, debemos encontrar inconsistencias en el uso de parámetros HTTP en las distintas funciones, ya que, en algunos casos, esto puede generar funcionalidades y filtros desprotegidos.

Consideremos el siguiente código `PHP` de nuestro ejercicio `File Manager`:

```php
if (isset($_REQUEST['filename'])) {
    if (!preg_match('/[^A-Za-z0-9. _-]/', $_POST['filename'])) {
        system("touch " . $_REQUEST['filename']);
    } else {
        echo "Malicious Request Denied!";
    }
}
```

Si solo estuviéramos considerando vulnerabilidades de inyección de comandos, diríamos que esto está codificado de forma segura. La función `preg_match` busca correctamente caracteres especiales no deseados y no permite que la entrada se introduzca en el comando si se encuentran caracteres especiales. Sin embargo, el error fatal que se comete en este caso no se debe a inyecciones de comandos, sino al `uso inconsistente de métodos HTTP`.

Vemos que el filtro `preg_match` solo busca caracteres especiales en los parámetros `POST` con `$_POST['filename']`. Sin embargo, el comando `system` final utiliza la variable `$_REQUEST['filename']` , que cubre tanto los parámetros `GET` como `POST`. Por lo tanto, en la sección anterior, cuando estábamos enviando nuestra entrada maliciosa a través de una solicitud `GET`, la función no la detuvo `preg_match`, ya que los parámetros `POST` estaban vacíos y, por lo tanto, no contenían ningún carácter especial. Sin embargo, una vez que llegamos a la función `system`, utilizó todos los parámetros que se encontraron en la solicitud y nuestros parámetros `GET` se utilizaron en el comando, lo que finalmente provocó una inyección de comando.

Este ejemplo básico nos muestra cómo pequeñas inconsistencias en el uso de métodos HTTP pueden llevar a vulnerabilidades críticas. En una aplicación web de producción, este tipo de vulnerabilidades no serán tan obvias. Probablemente se distribuirán por toda la aplicación web y no estarán en dos líneas consecutivas como las que tenemos aquí. En cambio, la aplicación web probablemente tendrá una función especial para verificar las inyecciones y una función diferente para crear archivos. Esta separación del código dificulta la detección de este tipo de inconsistencias y, por lo tanto, pueden sobrevivir a la producción.

Para evitar vulnerabilidades HTTP Verb Tampering en nuestro código, debemos ser coherentes con el uso de métodos HTTP y asegurarnos de que siempre se utilice el mismo método para cualquier funcionalidad específica en toda la aplicación web. Siempre se recomienda ampliar el alcance de las pruebas en los filtros de seguridad probando todos los parámetros de la solicitud. Esto se puede hacer con las siguientes funciones y variables:

<table data-header-hidden><thead><tr><th width="185"></th><th></th></tr></thead><tbody><tr><td>Idioma</td><td>Función</td></tr><tr><td>PHP</td><td><code>$_REQUEST['param']</code></td></tr><tr><td>Java</td><td><code>request.getParameter('param')</code></td></tr><tr><td>DO#</td><td><code>Request['param']</code></td></tr></tbody></table>

Si nuestro alcance en funciones relacionadas con la seguridad cubre todos los métodos, deberíamos evitar dichas vulnerabilidades o eludir filtros.
