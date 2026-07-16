
# IDOR

## <mark style="color:purple;">Introducción a IDOR</mark>

Las vulnerabilidades `Insecure Direct Object References (IDOR)` se encuentran entre las vulnerabilidades web más comunes y pueden afectar significativamente a la aplicación web vulnerable. Las vulnerabilidades IDOR ocurren cuando una aplicación web expone una referencia directa a un objeto, como un archivo o un recurso de base de datos, que el usuario final puede controlar directamente para obtener acceso a otros objetos similares. Si cualquier usuario puede acceder a cualquier recurso debido a la falta de un sistema de control de acceso sólido, el sistema se considera vulnerable.

La creación de un sistema de control de acceso sólido es un gran desafío, por lo que las vulnerabilidades de IDOR son omnipresentes. Además, automatizar el proceso de identificación de debilidades en los sistemas de control de acceso también es bastante difícil, lo que puede provocar que estas vulnerabilidades pasen desapercibidas hasta que lleguen a producción.

Por ejemplo, si los usuarios solicitan acceso a un archivo que han subido recientemente, pueden obtener un enlace al mismo como (`download.php?file_id=123`). Entonces, como el enlace hace referencia directa al archivo con (`file_id=123`), ¿qué sucedería si intentáramos acceder a otro archivo (que puede no pertenecernos) con ( `download.php?file_id=124`)? Si la aplicación web no tiene un sistema de control de acceso adecuado en el back-end, es posible que podamos acceder a cualquier archivo enviando una solicitud con su `file_id`. En muchos casos, podemos encontrar que el `id` es fácilmente adivinable, lo que hace posible recuperar muchos archivos o recursos a los que no deberíamos tener acceso en función de nuestros permisos.

***

## <mark style="color:purple;">¿Qué hace que una IDOR sea vulnerable?</mark>

El simple hecho de exponer una referencia directa a un objeto o recurso interno no constituye una vulnerabilidad en sí misma. Sin embargo, esto puede permitir explotar otra vulnerabilidad: `un sistema de control de acceso débil`. Muchas aplicaciones web restringen el acceso de los usuarios a los recursos al restringirles el acceso a las páginas, funciones y API que pueden recuperar estos recursos.&#x20;

Sin embargo, ¿qué sucedería si un usuario obtuviera acceso a estas páginas de alguna manera (por ejemplo, a través de un enlace compartido/adivinado)? ¿Podrían seguir accediendo a los mismos recursos simplemente teniendo el enlace para acceder a ellos? Si la aplicación web no tuviera un sistema de control de acceso en el back-end que compare la autenticación del usuario con la lista de acceso del recurso, podrían hacerlo.

Existen muchas formas de implementar un sistema de control de acceso sólido para aplicaciones web, como por ejemplo un sistema de control de acceso basado en roles ( [RBAC](https://en.wikipedia.org/wiki/Role-based_access_control) una vulnerabilidad IDOR que existe principalmente debido a la falta de un control de acceso en el back-end ). La principal conclusión es que si un usuario tuviera referencias directas a objetos en una aplicación web que carece de control de acceso, sería posible que los atacantes vieran o modificaran los datos de otros usuarios.

Muchos desarrolladores ignoran la creación de un sistema de control de acceso; por lo tanto, la mayoría de las aplicaciones web y móviles quedan desprotegidas en el back-end. En dichas aplicaciones, todos los usuarios pueden tener acceso arbitrario a los datos de todos los demás usuarios en el back-end. Lo único que impediría a los usuarios acceder a los datos de otros usuarios sería la implementación del front-end de la aplicación, que está diseñada para mostrar solo los datos del usuario. En tales casos, la manipulación manual de las solicitudes HTTP puede revelar que todos los usuarios tienen acceso completo a todos los datos, lo que lleva a un ataque exitoso.

Todo esto hace que las vulnerabilidades de IDOR se encuentren entre las vulnerabilidades más críticas para cualquier aplicación web o móvil, no solo por exponer referencias directas a objetos, sino principalmente por la falta de un sistema de control de acceso sólido. Incluso un sistema de control de acceso básico puede resultar complicado de desarrollar. Un sistema de control de acceso integral que cubra toda la aplicación web sin interferir con sus funciones puede ser una tarea aún más difícil. Es por eso que las vulnerabilidades de IDOR/Control de acceso se encuentran incluso en aplicaciones web muy grandes, como [Facebook](https://infosecwriteups.com/disclose-private-attachments-in-facebook-messenger-infrastructure-15-000-ae13602aa486) , [Instagram](https://infosecwriteups.com/add-description-to-instagram-posts-on-behalf-of-other-users-6500-7d55b4a24c5a) y [Twitter](https://medium.com/@kedrisec/publish-tweets-by-any-other-user-6c9d892708e3) .

***

## <mark style="color:purple;">Impacto de las vulnerabilidades de IDOR</mark>

Como se mencionó anteriormente, las vulnerabilidades de IDOR pueden tener un impacto significativo en las aplicaciones web. El ejemplo más básico de una vulnerabilidad de IDOR es el acceso a archivos y recursos privados de otros usuarios a los que no deberíamos tener acceso, como archivos personales o datos de tarjetas de crédito, lo que se conoce como `IDOR Information Disclosure Vulnerabilities`. Dependiendo de la naturaleza de la referencia directa expuesta, la vulnerabilidad puede incluso permitir la modificación o eliminación de los datos de otros usuarios, lo que puede llevar a una apropiación total de la cuenta.

Una vez que un atacante identifica las referencias directas, que pueden ser identificaciones de bases de datos o parámetros de URL, puede comenzar a probar patrones específicos para ver si puede obtener acceso a algún dato y eventualmente entender cómo extraer o modificar datos para cualquier usuario arbitrario.

Las vulnerabilidades de IDOR también pueden llevar a la elevación de los privilegios de usuario de un usuario estándar a un usuario administrador, con `IDOR Insecure Function Calls`. Por ejemplo, muchas aplicaciones web exponen parámetros de URL o API para funciones solo de administrador en el código de front-end de la aplicación web y deshabilitan estas funciones para usuarios que no son administradores. Sin embargo, si tuviéramos acceso a dichos parámetros o API, podríamos llamarlos con nuestros privilegios de usuario estándar.&#x20;

Supongamos que el back-end no denegó explícitamente a los usuarios que no son administradores la posibilidad de llamar a estas funciones. En ese caso, podríamos realizar operaciones administrativas no autorizadas, como cambiar las contraseñas de los usuarios o concederles ciertos roles, lo que eventualmente podría llevar a una toma de control total de toda la aplicación web.
