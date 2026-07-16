
# IDOR en APIs Inseguras

Hasta ahora, solo hemos utilizado vulnerabilidades de IDOR para acceder a archivos y recursos que están fuera del alcance de nuestros usuarios. Sin embargo, las vulnerabilidades de IDOR también pueden existir en llamadas de funciones y API, y explotarlas nos permitiría realizar diversas acciones como otros usuarios.

Si bien las `IDOR Information Disclosure Vulnerabilities` nos permiten leer varios tipos de recursos, `IDOR Insecure Function Calls` nos permiten llamar a API o ejecutar funciones como otro usuario. Dichas funciones y API se pueden utilizar para cambiar la información privada de otro usuario, restablecer la contraseña de otro usuario o incluso comprar artículos utilizando la información de pago de otro usuario. En muchos casos, podemos estar obteniendo cierta información a través de una vulnerabilidad de divulgación de información de IDOR y luego usar esta información con vulnerabilidades de llamada de función insegura de IDOR, como veremos más adelante en el módulo.

***

## <mark style="color:purple;">Identificación de API inseguras</mark>

Volviendo a nuestra aplicación `Employee Manager`, podemos comenzar a probar la página `Edit Profile` en busca de vulnerabilidades de IDOR:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_employee_manager.jpg" alt=""><figcaption></figcaption></figure>

Al hacer clic en el botón `Edit Profile`, se nos lleva a una página para editar información de nuestro perfil de usuario, es decir `Full Name`, `Email`, y `About Me`, que es una característica común en muchas aplicaciones web:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_edit_profile.jpg" alt=""><figcaption></figcaption></figure>

Podemos cambiar cualquiera de los detalles de nuestro perfil y hacer clic en `Update profile`, y veremos que se actualizan y persisten a través de las actualizaciones, lo que significa que se actualizan en una base de datos en algún lugar. Interceptemos la solicitud `Update` en Burp y veámosla:

![solicitud de actualización](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_update_request.jpg)

Vemos que la página está enviando una solicitud `PUT` al punto final de la API `/profile/api.php/profile/1`. Las solicitudes `PUT` se utilizan normalmente en las API para actualizar los detalles de los elementos, mientras que `POST` se utilizan para crear nuevos elementos, `DELETE` eliminar elementos y `GET` recuperar detalles de los elementos. Por lo tanto, se espera una solicitud `PUT` para la función `Update profile`. La parte interesante son los parámetros JSON que está enviando:

```json
{
    "uid": 1,
    "uuid": "40f5888b67c748df7efba008e7c2f9d2",
    "role": "employee",
    "full_name": "Amy Lindon",
    "email": "a_lindon@employees.htb",
    "about": "A Release is like a boat. 80% of the holes plugged is not good enough."
}
```

Vemos que la solicitud `PUT` incluye algunos parámetros ocultos, como `uid`, `uuid`y lo más interesante `role`, que está configurado en `employee`. La aplicación web también parece estar configurando los privilegios de acceso del usuario (por ejemplo, `role`) en el lado del cliente, en forma de nuestra `Cookie: role=employee`, que parece reflejar lo especificado para nuestro `role` de usuario. Este es un problema de seguridad común. Los privilegios de control de acceso se envían como parte de la solicitud HTTP del cliente, ya sea como una cookie o como parte de la solicitud JSON, dejándola bajo el control del cliente, que podría manipularse para obtener más privilegios.

Entonces, a menos que la aplicación web tenga un sistema de control de acceso sólido en el back-end, deberíamos poder establecer un rol arbitrario para nuestro usuario, lo que puede otorgarnos más privilegios. Sin embargo, ¿cómo sabríamos qué otros roles existen?

***

## <mark style="color:purple;">Explotación de API inseguras</mark>

Sabemos que podemos cambiar los parámetros `full_name`, `email` y `about`, ya que son los que están bajo nuestro control en el formulario HTML de la página `/profile`. Por lo tanto, intentemos manipular los demás parámetros.

Hay algunas cosas que podríamos intentar en este caso:

1. Cambiar nuestra cuenta `uid` por la de otro usuario `uid`, de modo que podamos hacernos cargo de sus cuentas.
2. Cambiar los datos de otro usuario, lo que nos puede permitir realizar varios ataques web
3. Crear nuevos usuarios con detalles arbitrarios o eliminar usuarios existentes
4. Cambiar nuestro rol a un rol más privilegiado (por ejemplo `admin`) para poder realizar más acciones

Comencemos por cambiar nuestro `uid` por el de otro usuario (por ejemplo, `"uid": 2`). Sin embargo, cualquier número que establezcamos que no sea nuestro `uid` nos dará como respuesta `uid mismatch`:

![No coincide el uid](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_uid_mismatch.jpg)

La aplicación web parece comparar la solicitud `uid` con el punto final de la API ( `/1`). Esto significa que una forma de control de acceso en el back-end nos impide cambiar arbitrariamente algunos parámetros JSON, lo que podría ser necesario para evitar que la aplicación web se bloquee o devuelva errores.

Quizás podamos intentar cambiar los datos de otro usuario. Cambiaremos el punto final de la API a `/profile/api.php/profile/2` y cambiaremos `"uid": 2` para evitar el error anterior `uid mismatch`:

![uuid\_desajuste](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_uuid_mismatch.jpg)

Como podemos ver, esta vez recibimos un mensaje de error que dice `uuid mismatch`. La aplicación web parece estar verificando si el valor `uuid` que estamos enviando coincide con el del usuario `uuid`. Como estamos enviando nuestro propio `uuid`, nuestra solicitud está fallando. Esto parece ser otra forma de control de acceso para evitar que los usuarios cambien los detalles de otro usuario.

A continuación, veamos si podemos crear un nuevo usuario con una solicitud `POST` al punto final de la API. Podemos cambiar el método de solicitud a `POST`, cambiar el `uid` a uno nuevo y enviar la solicitud al punto final de la API del nuevo `uid`:

![crear\_nuevo\_usuario\_1](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_create_new_user_1.jpg)

Recibimos un mensaje de error que dice `Creating new employees is for admins only`. Lo mismo sucede cuando enviamos una solicitud `Delete`, ya que recibimos `Deleting employees is for admins only`. La aplicación web podría estar verificando nuestra autorización a través de la cookie `role=employee` porque esta parece ser la única forma de autorización en la solicitud HTTP.

Por último, intentemos cambiar nuestro `role` a `admin`/ `administrator` para obtener mayores privilegios. Desafortunadamente, sin conocer un `role` válido, obtenemos la respuesta `Invalid role` y nuestro `role` no se actualiza:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_invalid_role.jpg" alt=""><figcaption></figcaption></figure>

Por lo tanto todos nuestros intentos parecen haber fracasado, no podemos crear ni eliminar usuarios, ya que no podemos cambiar nuestro `role`. No podemos cambiar nuestros `uid`, ya que existen medidas preventivas en el back-end que no podemos controlar, ni tampoco podemos cambiar los datos de otro usuario por la misma razón. `Entonces, ¿la aplicación web es segura contra ataques IDOR?`.

Hasta ahora, solo hemos estado probando `IDOR Insecure Function Calls`. Sin embargo, no hemos probado la solicitud de la API `GET` para `IDOR Information Disclosure Vulnerabilities`. Si no hubiera un sistema de control de acceso sólido, podríamos leer los detalles de otros usuarios, lo que podría ayudarnos con los ataques anteriores que intentamos.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.62.166:58222
```

Intente leer los detalles del usuario con '`uid=5`'. ¿Cuál es su valor '`uuid`'?

<figure><img src="/files/gikyf9idBF0ATF81mmGQ" alt=""><figcaption></figcaption></figure>

Cuando editamos un perfil y capturamos la petición nos da muchos más detalles del uid y uuid del usuario:

<figure><img src="/files/DZHWlAYiZ3Aa0UmY8boB" alt=""><figcaption></figcaption></figure>

Al intentar cambiar el uid al 5 por ejemplo nos da el error `uuid mismatch`:

<figure><img src="/files/3Ipiij9QxUk5wNqronPh" alt=""><figcaption></figcaption></figure>

Cambiamos a POST y nos da otro error, que nos dice solo los admins pueden crear empleados:

<figure><img src="/files/BpczLqqewL9pYVtSL6UZ" alt=""><figcaption></figcaption></figure>

Sin embargo, en este punto si cambiamos a GET podemos extraer la información sin problema:

<figure><img src="/files/3LH9QJuQ6jmbb8MYOFOx" alt=""><figcaption></figcaption></figure>
