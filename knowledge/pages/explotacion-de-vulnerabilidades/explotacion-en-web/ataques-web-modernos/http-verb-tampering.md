
# HTTP Verb Tampering

## <mark style="color:purple;">Introducción a HTTP Verb Tampering</mark>

***

El protocolo `HTTP` funciona aceptando varios métodos HTTP `verbs` al comienzo de una solicitud HTTP. Según la configuración del servidor web, las aplicaciones web pueden programarse para aceptar determinados métodos HTTP para sus diversas funcionalidades y realizar una acción particular según el tipo de solicitud.

Si bien los programadores consideran principalmente los dos métodos HTTP más utilizados, `GET`y `POST`, cualquier cliente puede enviar cualquier otro método en sus solicitudes HTTP y luego ver cómo el servidor web maneja estos métodos. Supongamos que tanto la aplicación web como el servidor web back-end están configurados solo para aceptar solicitudes `GET` y `POST`. En ese caso, enviar una solicitud diferente hará que se muestre una página de error del servidor web, lo que no es una vulnerabilidad grave en sí misma (aparte de proporcionar una mala experiencia de usuario y potencialmente conducir a la divulgación de información). Por otro lado, si las configuraciones del servidor web no están restringidas para aceptar solo los métodos HTTP requeridos por el servidor web (por ejemplo, `GET`/ `POST`), y la aplicación web no está desarrollada para manejar otros tipos de solicitudes HTTP (por ejemplo `HEAD`, `PUT`), entonces podemos ser capaces de explotar esta configuración insegura para obtener acceso a funcionalidades a las que no tenemos acceso, o incluso eludir ciertos controles de seguridad.

***

## <mark style="color:purple;">HTTP Verb Tampering</mark>

Para comprender `HTTP Verb Tampering`, primero debemos conocer los diferentes métodos que acepta el protocolo HTTP. HTTP tiene [9 verbos diferentes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) que los servidores web pueden aceptar como métodos HTTP. Además de `GET` y `POST`, los siguientes son algunos de los verbos HTTP más utilizados:

<table data-header-hidden><thead><tr><th width="128"></th><th></th></tr></thead><tbody><tr><td>Verbo</td><td>Descripción</td></tr><tr><td><code>HEAD</code></td><td>Idéntico a una solicitud GET, pero su respuesta solo contiene el <code>headers</code>, sin el cuerpo de la respuesta</td></tr><tr><td><code>PUT</code></td><td>Escribe la carga útil de la solicitud en la ubicación especificada</td></tr><tr><td><code>DELETE</code></td><td>Elimina el recurso en la ubicación especificada</td></tr><tr><td><code>OPTIONS</code></td><td>Muestra diferentes opciones aceptadas por un servidor web, como verbos HTTP aceptados</td></tr><tr><td><code>PATCH</code></td><td>Aplicar modificaciones parciales al recurso en la ubicación especificada</td></tr></tbody></table>

Como puedes imaginar, algunos de los métodos anteriores pueden realizar funciones muy sensibles, como escribir (`PUT`) o eliminar (`DELETE`) archivos en el directorio raíz web en el servidor back-end. Como se explicó en el módulo [Solicitudes web](https://academy.hackthebox.com/course/preview/web-requests) , si un servidor web no está configurado de forma segura para administrar estos métodos, podemos usarlos para obtener el control sobre el servidor back-end. Sin embargo, lo que hace que los ataques de manipulación de verbos HTTP sean más comunes (y, por lo tanto, más críticos) es que son causados ​​por una configuración incorrecta en el servidor web back-end o en la aplicación web, cualquiera de los cuales puede causar la vulnerabilidad.

***

## <mark style="color:purple;">Configuraciones inseguras</mark>

Las configuraciones de servidores web inseguras provocan el primer tipo de vulnerabilidades de manipulación de verbos HTTP. La configuración de autenticación de un servidor web puede estar limitada a métodos HTTP específicos, lo que dejaría algunos métodos HTTP accesibles sin autenticación. Por ejemplo, un administrador de sistemas puede utilizar la siguiente configuración para exigir autenticación en una página web en particular:

```xml
<Limit GET POST>
    Require valid-user
</Limit>
```

Como podemos ver, aunque la configuración especifica tanto `GET` como `POST` solicita el método de autenticación, un atacante puede usar un método HTTP diferente (como `HEAD`) para eludir este mecanismo de autenticación por completo, como veremos en la siguiente sección. Esto finalmente conduce a una omisión de la autenticación y permite a los atacantes acceder a páginas web y dominios a los que no deberían tener acceso.

***

## <mark style="color:purple;">Codificación insegura</mark>

Las prácticas de codificación inseguras causan otro tipo de vulnerabilidades de manipulación de verbos HTTP (aunque algunas personas pueden no considerar esta manipulación de verbos). Esto puede ocurrir cuando un desarrollador web aplica filtros específicos para mitigar vulnerabilidades particulares sin cubrir todos los métodos HTTP con ese filtro. Por ejemplo, si se descubre que una página web es vulnerable a una vulnerabilidad de inyección SQL y el desarrollador de back-end mitiga la vulnerabilidad de inyección SQL aplicando los siguientes filtros de limpieza de entrada:

```php
$pattern = "/^[A-Za-z\s]+$/";

if(preg_match($pattern, $_GET["code"])) {
    $query = "Select * from ports where port_code like '%" . $_REQUEST["code"] . "%'";
    ...SNIP...
}
```

Podemos ver que el filtro de desinfección solo se está probando en el parámetro GET. Si las solicitudes GET no contienen caracteres incorrectos, entonces se ejecutará la consulta. Sin embargo, cuando se ejecuta la consulta, se utilizan los parámetros `$_REQUEST["code"]`, que también pueden contener parámetros POST, lo que genera una inconsistencia en el uso de los verbos HTTP. En este caso, un atacante puede utilizar una solicitud POST para realizar una inyección SQL, en cuyo caso los parámetros GET estarían vacíos (no incluirán ningún carácter incorrecto). La solicitud pasaría el filtro de seguridad, lo que haría que la función aún fuera vulnerable a la inyección SQL.

Si bien ambas vulnerabilidades mencionadas anteriormente se encuentran en el público, la segunda es mucho más común, ya que se debe a errores cometidos en la codificación, mientras que la primera suele evitarse mediante configuraciones seguras del servidor web, ya que la documentación suele advertir sobre su uso. En las siguientes secciones, veremos ejemplos de ambos tipos y cómo explotarlos.
