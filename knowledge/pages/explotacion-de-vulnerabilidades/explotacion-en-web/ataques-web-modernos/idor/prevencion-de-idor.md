
# Prevención de IDOR

En esta sección hemos aprendido varias formas de identificar y explotar vulnerabilidades de IDOR en páginas web, funciones web y llamadas API. A esta altura, deberíamos haber entendido que las vulnerabilidades de IDOR son causadas principalmente por un control de acceso inadecuado en los servidores back-end. Para evitar dichas vulnerabilidades, primero tenemos que crear un sistema de control de acceso a nivel de objeto y luego usar referencias seguras para nuestros objetos al almacenarlos y llamarlos.

***

## <mark style="color:purple;">Control de acceso a nivel de objeto</mark>

Un sistema de Control de Acceso debe ser el núcleo de cualquier aplicación web, ya que puede afectar a todo su diseño y estructura. Para controlar adecuadamente cada área de la aplicación web, su diseño tiene que soportar la segmentación de roles y permisos de forma centralizada. Sin embargo, el Control de Acceso es un tema muy amplio, por lo que nos centraremos únicamente en su papel en las vulnerabilidades IDOR, representadas en los mecanismos de control de acceso `Object-Level`.

Los roles y permisos de los usuarios son una parte vital de cualquier sistema de control de acceso, lo que se materializa plenamente en un sistema de control de acceso basado en roles (RBAC). Para evitar explotar las vulnerabilidades de IDOR, debemos asignar el RBAC a todos los objetos y recursos. El servidor back-end puede permitir o rechazar cada solicitud, dependiendo de si el rol del solicitante tiene suficientes privilegios para acceder al objeto o al recurso.

Una vez que se haya implementado un RBAC, a cada usuario se le asignará un rol que tendrá ciertos privilegios. En cada solicitud que realice el usuario, se comprobarán sus roles y privilegios para ver si tiene acceso al objeto que solicita. Solo se le permitirá acceder a él si tiene derecho a hacerlo.

Existen muchas formas de implementar un sistema RBAC y asignarlo a los objetos y recursos de la aplicación web, y diseñarlo en el núcleo de la estructura de la aplicación web es un arte que hay que perfeccionar. El siguiente es un código de muestra de cómo una aplicación web puede comparar los roles de usuario con los objetos para permitir o denegar el control de acceso:

```javascript
match /api/profile/{userId} {
    allow read, write: if user.isAuth == true
    && (user.uid == userId || user.roles == 'admin');
}
```

El ejemplo anterior utiliza el token de usuario, que se puede asignar a partir de la solicitud HTTP realizada al RBAC para recuperar las diversas funciones y privilegios del usuario. Luego, solo permite el acceso de lectura/escritura si el uid del usuario en el sistema RBAC coincide con el uid en el punto final API que está solicitando. Además, si un usuario tiene la función de administrador en el RBAC de back-end, se le permite acceso de lectura/escritura.

En nuestros ataques anteriores, vimos ejemplos en los que la función del usuario se almacena en los detalles del usuario o en su cookie, los cuales están bajo el control del usuario y pueden manipularse para aumentar sus privilegios de acceso. El ejemplo anterior demuestra un enfoque más seguro para asignar roles de usuario, ya que los privilegios de usuario no se pasaban a través de la solicitud HTTP, sino que se asignaban directamente desde el RBAC en el back-end utilizando el token de sesión del usuario como mecanismo de autenticación.

Los sistemas de control de acceso y los RBAC son mucho más complejos, ya que pueden ser algunos de los sistemas más difíciles de diseñar. Sin embargo, esto debería darnos una idea de cómo deberíamos controlar el acceso de los usuarios a los objetos y recursos de las aplicaciones web.

***

## <mark style="color:purple;">Referencia de objetos</mark>

Si bien el problema principal de IDOR radica en el control de acceso defectuoso (`Inseguro`), tener acceso a referencias directas a objetos (`Direct Object Referencing`) permite enumerar y explotar estas vulnerabilidades de control de acceso. Todavía podemos usar referencias directas, pero solo si tenemos implementado un sistema de control de acceso sólido.

Incluso después de construir un sistema de control de acceso sólido, nunca deberíamos usar referencias a objetos en texto claro o patrones simples (por ejemplo, `uid=1`). Siempre deberíamos usar referencias fuertes y únicas, como hashes con sal o `UUIDs`. Por ejemplo, podemos usar `UUID V4` para generar un id fuertemente aleatorio para cualquier elemento, que se ve algo como ( `89c9b29b-d19f-4515-b2dd-abb6e693eb20`). Luego, podemos asignar esto al objeto `UUID` al que hace referencia en la base de datos de back-end, y cada vez que se llama al `UUID`, la base de datos de back-end sabrá qué objeto devolver. El siguiente código PHP de ejemplo nos muestra cómo puede funcionar esto:

```php
$uid = intval($_REQUEST['uid']);
$query = "SELECT url FROM documents where uid=" . $uid;
$result = mysqli_query($conn, $query);
$row = mysqli_fetch_array($result));
echo "<a href='" . $row['url'] . "' target='_blank'></a>";
```

Además, como hemos visto anteriormente en el módulo, nunca debemos calcular hashes en el front-end. Debemos generarlos cuando se crea un objeto y almacenarlos en la base de datos del back-end. Luego, debemos crear mapas de bases de datos para permitir una rápida referencia cruzada de objetos y referencias.

Por último, debemos tener en cuenta que el uso de `UUIDs` puede hacer que las vulnerabilidades de IDOR pasen desapercibidas, ya que dificulta la prueba de vulnerabilidades de IDOR. Es por ello que la referencia a objetos segura es siempre el segundo paso después de implementar un sistema de control de acceso seguro. Además, algunas de las técnicas que aprendimos en este módulo funcionarían incluso con referencias únicas si el sistema de control de acceso no funciona, como repetir la solicitud de un usuario con la sesión de otro usuario, como hemos visto anteriormente.

Si implementamos ambos mecanismos de seguridad, deberíamos estar relativamente seguros contra las vulnerabilidades de IDOR.
