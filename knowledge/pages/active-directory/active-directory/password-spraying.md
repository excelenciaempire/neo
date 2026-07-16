
# Password Spraying

## <mark style="color:purple;">Introducción</mark>

La pulverización de contraseñas puede dar lugar a la obtención de acceso a los sistemas y, potencialmente, a establecerse en una red de destino. El ataque implica intentar iniciar sesión en un servicio expuesto utilizando una contraseña común y una lista más larga de nombres de usuario o direcciones de correo electrónico.&#x20;

Es posible que los nombres de usuario y los correos electrónicos se hayan recopilado durante la fase OSINT de la prueba de penetración o durante nuestros intentos iniciales de enumeración. Recuerde que una prueba de penetración no es estática, sino que iteramos constantemente a través de varias técnicas y repetimos procesos a medida que descubrimos nuevos datos. A menudo trabajaremos en equipo o ejecutaremos varios TTP a la vez para utilizar nuestro tiempo de manera efectiva.&#x20;

A medida que avanzamos en nuestra carrera, encontraremos que muchas de nuestras tareas, como escanear, intentar descifrar hashes y otras, toman bastante tiempo. Necesitamos asegurarnos de que estamos usando nuestro tiempo de manera efectiva y creativa porque la mayoría de las evaluaciones tienen un límite de tiempo. Entonces, mientras tenemos nuestros intentos de envenenamiento en ejecución, también podemos utilizar la información que tenemos para intentar obtener acceso a través de la pulverización de contraseñas. Ahora cubramos algunas de las consideraciones para la pulverización de contraseñas y cómo hacer nuestra lista de objetivos a partir de la información que tenemos.

***

## <mark style="color:purple;">Escenarios de ejemplo</mark>

La pulverización de contraseñas puede ser una forma muy eficaz de afianzarse internamente. Son muchas las veces que esta técnica me ha ayudado a afianzarme durante mis evaluaciones. Tenga en cuenta que estos ejemplos provienen de evaluaciones no evasivas de "caja gris" en las que tenía acceso a la red interna con una máquina virtual Linux y una lista de rangos de IP dentro del alcance y nada más.

### Escenario 1

En este primer ejemplo, realicé todas mis comprobaciones estándar y no pude encontrar nada útil como una sesión SMB NULL o un enlace anónimo LDAP que pudiera permitirme recuperar una lista de usuarios válidos. Entonces decidí usar la herramienta `Kerbrute` para crear una lista de nombres de usuario de destino enumerando los usuarios de dominio válidos (una técnica que cubriremos más adelante en esta sección).&#x20;

Para crear esta lista, tomé la lista `jsmith.txt` de nombres de usuario del repositorio de GitHub [statistically-likely-usernames](https://github.com/insidetrust/statistically-likely-usernames) y la combiné con los resultados que obtuve al hacer Scraping en LinkedIn. Con esta lista combinada, enumeré los usuarios válidos con `Kerbrute` y luego utilicé la misma herramienta para pulverizar contraseñas con la contraseña común `Welcome1`. Obtuve dos accesos con esta contraseña para usuarios con privilegios muy bajos, pero esto me dio suficiente acceso dentro del dominio para ejecutar `BloodHound` y, finalmente, identificar rutas de ataque que condujeron al compromiso del dominio.

### Escenario 2

En la segunda evaluación, me enfrenté a una configuración similar, pero enumerar usuarios de dominio válidos con listas de nombres de usuarios comunes y los resultados de LinkedIn no arrojaron ningún resultado. Busqué en Google y busqué archivos PDF publicados por la organización. Mi búsqueda generó muchos resultados y confirmé en las propiedades del documento de 4 de ellos que la estructura interna del nombre de usuario tenía el formato `F9L8` , generando aleatoriamente GUIDs usando solo letras mayúsculas y números ( `A-Z and 0-9`). Esta información se publicó con el documento en el campo `Author` y muestra la importancia de eliminar los metadatos del documento antes de publicar algo en línea. A partir de aquí, se podría utilizar un breve script Bash para generar `16.679.616` posibles combinaciones de nombres de usuarios.

```bash

#!/bin/bash

for x in {{A..Z},{0..9}}{{A..Z},{0..9}}{{A..Z},{0..9}}{{A..Z},{0..9}}
    do echo $x;
done
```

Luego utilicé la lista de nombres de usuarios generada para enumerar con `Kerbrute` cada cuenta de usuario en el dominio. Este intento de hacer más difícil enumerar los nombres de usuario terminó en poder enumerar cada cuenta en el dominio debido al GUID predecible en uso combinado con los metadatos del PDF que pude localizar y facilitó enormemente el ataque. Normalmente, sólo puedo identificar entre el 40 y el 60 % de las cuentas válidas utilizando una lista como `jsmith.txt`.&#x20;

En este ejemplo, incrementé significativamente mis posibilidades de tener un ataque exitoso de pulverización de contraseñas al iniciar el ataque con TODAS las cuentas de dominio en mi lista de objetivos. Desde aquí obtuve contraseñas válidas para algunas cuentas. Finalmente, pude seguir una cadena de ataque complicada que involucraba [la delegación restringida basada en recursos (RBCD)](https://posts.specterops.io/another-word-on-delegation-10bdbe3cd94a) y el ataque [de credenciales en la sombra](https://www.fortalicesolutions.com/posts/shadow-credentials-workstation-takeover-edition) para finalmente obtener el control sobre el dominio.

***

## <mark style="color:purple;">Consideraciones sobre el Password Spraying</mark>

Si bien la pulverización de contraseñas es útil para un Pentester o un miembro del Red Team, el uso descuidado puede causar daños considerables, como bloquear cientos de cuentas de producción. Un ejemplo son los intentos de fuerza bruta para identificar la contraseña de una cuenta utilizando una larga lista de contraseñas. Por el contrario, la pulverización de contraseñas es un ataque más mesurado, que utiliza contraseñas muy comunes en múltiples industrias. La siguiente tabla visualiza un Password Spraying:

<table data-header-hidden><thead><tr><th width="136"></th><th></th><th></th></tr></thead><tbody><tr><td><strong>Ataque</strong></td><td><strong>Nombre de usuario</strong></td><td><strong>Contraseña</strong></td></tr><tr><td>1</td><td>bob.smith@inlanefreight.local</td><td>Bienvenido1</td></tr><tr><td>1</td><td>john.doe@inlanefreight.local</td><td>Bienvenido1</td></tr><tr><td>1</td><td>jane.doe@inlanefreight.local</td><td>Bienvenido1</td></tr><tr><td>DEMORA</td><td></td><td></td></tr><tr><td>2</td><td>bob.smith@inlanefreight.local</td><td>Contraseña</td></tr><tr><td>2</td><td>john.doe@inlanefreight.local</td><td>Contraseña</td></tr><tr><td>2</td><td>jane.doe@inlanefreight.local</td><td>Contraseña</td></tr><tr><td>DEMORA</td><td></td><td></td></tr><tr><td>3</td><td>bob.smith@inlanefreight.local</td><td>Invierno2022</td></tr><tr><td>3</td><td>john.doe@inlanefreight.local</td><td>Invierno2022</td></tr><tr><td>3</td><td>jane.doe@inlanefreight.local</td><td>Invierno2022</td></tr></tbody></table>

Implica enviar menos solicitudes de inicio de sesión por nombre de usuario y es menos probable que bloquee cuentas que un ataque de fuerza bruta. Sin embargo, la difusión de contraseñas todavía presenta un riesgo de bloqueos, por lo que es esencial introducir un retraso entre los intentos de inicio de sesión. La pulverización de contraseñas internas se puede utilizar para moverse lateralmente dentro de una red, y se aplican las mismas consideraciones con respecto al bloqueo de cuentas. Sin embargo, es posible obtener la política de contraseña del dominio con acceso interno, lo que reduce significativamente este riesgo.

Es común encontrar una política de contraseñas que permita cinco intentos fallidos antes de bloquear la cuenta, con un umbral de desbloqueo automático de 30 minutos. Algunas organizaciones configuran umbrales de bloqueo de cuentas más extendidos, e incluso requieren que un administrador desbloquee las cuentas manualmente. Si no conoce la política de contraseñas, una buena regla general es esperar unas horas entre intentos, lo que debería ser suficiente para que se restablezca el umbral de bloqueo de la cuenta.

Es mejor obtener la política de contraseñas antes de intentar el ataque durante una evaluación interna, pero esto no siempre es posible. Podemos pecar de cautelosos y optar por realizar solo un intento de pulverización de contraseñas dirigida utilizando una contraseña débil/común como un "Ave María" si se han agotado todas las demás opciones para afianzarse o ampliar el acceso. Dependiendo del tipo de valoración, siempre podremos pedir al cliente que aclare la política de contraseñas. Si ya tenemos un punto de apoyo o se nos proporcionó una cuenta de usuario como parte de la prueba, podemos enumerar la política de contraseñas de varias maneras. Practiquemos esto en la siguiente sección.
