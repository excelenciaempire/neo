
# GitLab - Enumeración

[GitLab](https://about.gitlab.com/) es una herramienta de alojamiento de repositorios Git basada en la web que ofrece capacidades de wiki, seguimiento de problemas y funcionalidad de canalización de implementación e integración continua. Es de código abierto y originalmente estaba escrita en Ruby, pero el stack tecnologico actual incluye Go, Ruby on Rails y Vue.js. GitLab se lanzó por primera vez en 2014 y, con el paso de los años, se ha convertido en una empresa de 1400 personas con ingresos de 150 millones de dólares en 2020. Aunque la aplicación es gratuita y de código abierto, también ofrecen una versión empresarial paga. A continuación, se muestran algunas [estadísticas](https://about.gitlab.com/company/) rápidas sobre GitLab:

* En el momento de redactar este artículo, la empresa cuenta con 1.466 empleados.
* Gitlab tiene más de 30 millones de usuarios registrados ubicados en 66 países.
* La empresa publica la mayoría de sus procedimientos internos y OKR públicamente en su sitio web.
* Algunas empresas que utilizan GitLab incluyen Drupal, Goldman Sachs, Hackerone, Ticketmaster, Nvidia, Siemens y [más.](https://about.gitlab.com/customers/)

GitLab es similar a GitHub y BitBucket, que también son herramientas de repositorio Git basadas en la web. Puedes ver una comparación entre los tres [aquí](https://stackshare.io/stackups/bitbucket-vs-github-vs-gitlab) .

Durante las pruebas de penetración internas y externas, es común encontrar datos interesantes en el repositorio de GitHub de una empresa o en una instancia de GitLab o BitBucket alojada por uno mismo. Estos repositorios de Git pueden contener código disponible públicamente, como scripts para interactuar con una API. Sin embargo, también podemos encontrar scripts o archivos de configuración que se enviaron accidentalmente y que contienen secretos en texto claro, como contraseñas, que podemos usar en nuestro beneficio.&#x20;

También podemos encontrarnos con claves privadas SSH. Podemos intentar usar la función de búsqueda para buscar usuarios, contraseñas, etc. Las aplicaciones como GitLab permiten repositorios públicos (que no requieren autenticación), repositorios internos (disponibles para usuarios autenticados) y repositorios privados (restringidos a usuarios específicos).&#x20;

También vale la pena examinar los repositorios públicos en busca de datos confidenciales y, si la aplicación lo permite, registrar una cuenta y ver si hay repositorios internos interesantes a los que se pueda acceder. La mayoría de las empresas solo permitirán que un usuario con una dirección de correo electrónico de la empresa se registre y requerirán que un administrador autorice la cuenta, pero como veremos más adelante, se puede configurar una instancia de GitLab para permitir que cualquier persona se registre y luego inicie sesión.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/gitlab_signup_res.png" alt=""><figcaption></figcaption></figure>

Si podemos obtener las credenciales de usuario de nuestra OSINT, podremos iniciar sesión en una instancia de GitLab. La autenticación de dos factores está deshabilitada de forma predeterminada.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/gitlab_2fa.png" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Discovery / Footprinting</mark>

Podemos determinar rápidamente que GitLab está en uso en un entorno simplemente navegando a la URL de GitLab, y seremos dirigidos a la página de inicio de sesión, que muestra el logotipo de GitLab.  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/gitlab_login.png" alt=""><figcaption></figcaption></figure>

La única forma de rastrear el número de versión de GitLab en uso es navegando a la página  `/help` cuando haya iniciado sesión. Si la instancia de GitLab nos permite registrar una cuenta, podemos iniciar sesión y navegar a esta página para confirmar la versión. Si no podemos registrar una cuenta, es posible que tengamos que probar un exploit de bajo riesgo como [este](https://www.exploit-db.com/exploits/49821) . No recomendamos lanzar varios exploits en una aplicación, por lo que si no tenemos forma de enumerar el número de versión (como una fecha en la página, la primera confirmación pública o registrando un usuario), entonces deberíamos limitarnos a buscar secretos y no intentar múltiples exploits contra él a ciegas. Ha habido algunos exploits graves contra GitLab [12.9.0](https://www.exploit-db.com/exploits/48431) y GitLab [11.4.7](https://www.exploit-db.com/exploits/49257) en los últimos años, así como también contra GitLab Community Edition [13.10.3](https://www.exploit-db.com/exploits/49821) , [13.9.3](https://www.exploit-db.com/exploits/49944) y [13.10.2](https://www.exploit-db.com/exploits/49951) .

***

## <mark style="color:purple;">Enumeración</mark>

No hay mucho que podamos hacer contra GitLab sin saber el número de versión o estar conectado. Lo primero que deberíamos intentar es navegar a `/explore` y ver si hay algún proyecto público que pueda contener algo interesante. Navegando a esta página, vemos un proyecto llamado `Inlanefreight dev`. Los proyectos públicos pueden ser interesantes porque podemos usarlos para obtener más información sobre la infraestructura de la empresa, encontrar código de producción en el que podamos encontrar un error después de una revisión de código, credenciales codificadas, un script o archivo de configuración que contenga credenciales u otros secretos como una clave privada SSH o una clave API.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/gitlab_explore.png" alt=""><figcaption></figcaption></figure>

Al explorar el proyecto, parece un proyecto de ejemplo y puede que no contenga nada útil, aunque siempre vale la pena investigar un poco.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/gitlab_example.png" alt=""><figcaption></figcaption></figure>

Desde aquí, podemos explorar cada una de las páginas vinculadas en la parte superior izquierda `groups`, `snippets` y `help`. También podemos usar la función de búsqueda y ver si podemos descubrir otros proyectos. Una vez que hayamos terminado de buscar en lo que está disponible externamente, debemos verificar si podemos registrar una cuenta y acceder a proyectos adicionales. Supongamos que la organización no configuró GitLab solo para permitir que se registren correos electrónicos de la empresa o para requerir que un administrador apruebe una nueva cuenta. En ese caso, es posible que podamos acceder a datos adicionales.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/gitlab_signup.png" alt=""><figcaption></figcaption></figure>

También podemos usar el formulario de registro para enumerar usuarios válidos (más sobre esto en la siguiente sección). Si podemos hacer una lista de usuarios válidos, podríamos intentar adivinar contraseñas débiles o posiblemente reutilizar credenciales que encontremos de un volcado de contraseñas usando una herramienta como la de `Dehashed` que se ve en la sección [osTicket](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/ataques-a-aplicaciones-varias/osticket.md).&#x20;

Aquí podemos ver que el usuario `root` está tomado. Veremos otro ejemplo de enumeración de nombres de usuario en la siguiente sección. En esta instancia particular de GitLab (y probablemente en otras), también podemos enumerar correos electrónicos. Si intentamos registrarnos con un correo electrónico que ya ha sido tomado, obtendremos el error `1 error prohibited this user from being saved: Email has already been taken`. Al momento de escribir esto, esta técnica de enumeración de nombres de usuario funciona con la última versión de GitLab. Incluso si la casilla de verificación `Sign-up enabled` está desmarcada dentro de la página de configuración en `Sign-up restrictions`, aún podemos navegar a la página `/users/sign_up` y enumerar usuarios, pero no podremos registrar un usuario.

Se pueden implementar algunas mitigaciones para esto, como aplicar 2FA en todas las cuentas de usuario, usar Fail2Ban para bloquear intentos fallidos de inicio de sesión que son indicativos de ataques de fuerza bruta e incluso restringir qué direcciones IP pueden acceder a una instancia de GitLab si es necesario. accesible fuera de la red corporativa interna.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/gitlab_taken2.png" alt=""><figcaption></figcaption></figure>

Vamos a registrarnos con las credenciales `hacker:Welcome`, iniciar sesión y echar un vistazo. Tan pronto como completemos el registro, iniciaremos sesión y nos dirigiremos a la página del panel de proyectos. Si vamos a la página `/explore` ahora, notamos que ahora hay un proyecto interno `Inlanefreight website` disponible para nosotros. Investigando un poco, parece ser solo un sitio web estático para la empresa. Supongamos que se trata de otro tipo de aplicación (como PHP). En ese caso, podríamos descargar el código fuente y revisarlo en busca de vulnerabilidades o funcionalidades ocultas o encontrar credenciales u otros datos confidenciales.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/gitlab_internal.png" alt=""><figcaption></figcaption></figure>

En un escenario del mundo real, podríamos encontrar una cantidad considerable de datos confidenciales si nos registramos y obtenemos acceso a cualquiera de sus repositorios. Como explica esta [publicación del blog](https://tillsongalloway.com/finding-sensitive-information-on-github/index.html) , existe una cantidad considerable de datos que podríamos descubrir en GitLab, GitHub, etc.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.21.88 (ACADEMY-ATCKAPPS-APP04) 

vHosts necesarios:
gitlab.inlanefreight.local
```

### Pregunta 1

> Enumera la instancia de GitLab en <http://gitlab.inlanefreight.local>. ¿Cuál es el número de versión?

Vamos a usar un módulo de Metasploit para encontrar la versión de GitLab:

```bash
msf6 auxiliary(scanner/http/gitlab_version) > setg vhost gitlab.inlanefreight.local
vhost => gitlab.inlanefreight.local
msf6 auxiliary(scanner/http/gitlab_version) > setg rhosts 10.129.201.88
rhosts => 10.129.201.88
msf6 auxiliary(scanner/http/gitlab_version) > set rport 8081
rport => 8081
msf6 auxiliary(scanner/http/gitlab_version) > run

[+] Gitlab version range for 10.129.201.88:8081: [#<Rex::Version "13.10.0">, #<Rex::Version "13.10.5">]
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Vemos que usa una versión entre la `13.10.0` y la `13.10.5`. Haciendo un poco de research encontramos la versión `13.0.2`

### Pregunta 2

> Busca la contraseña de la base de datos PostgreSQL en el proyecto de ejemplo.

Accedemos a `gitlab.inlanefreight.local`:

<figure><img src="/files/oAVo9W0qLvHUT5Du61hN" alt=""><figcaption></figcaption></figure>

En el footer encontramos una pestaña Explore, accedemos y encontramos un repositorio interesante de un administrador:

<figure><img src="/files/4rSKsRr3lRuP0JCgZSMQ" alt=""><figcaption></figcaption></figure>

Encontramos 2 archivos xml de bases de datos que contienen las contraseñas para MySQL y para PostgreSQL:

<figure><img src="/files/7UKOz5TGapdz9wUbqdic" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/2YcaohBaqzPDsVveVE5A" alt=""><figcaption></figcaption></figure>
