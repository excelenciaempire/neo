
# Bruteforce con Hydra

{% embed url="<https://github.com/vanhauser-thc/thc-hydra>" %}

Puedes consultar una sección del GitBook dedicada a esta herramienta:

{% content-ref url="/pages/OjTADQBHgnrkHq7LDMHB" %}
[Hydra](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/hydra.md)
{% endcontent-ref %}

## Uso básico

La sintaxis básica de Hydra es:

```shell-session
afsh4ck@kali$ hydra [login_options] [password_options] [attack_options] [service_options]
```

<table data-header-hidden><thead><tr><th width="207.33984375"></th><th width="319.21484375"></th><th></th></tr></thead><tbody><tr><td>Parámetro</td><td>Explicación</td><td>Ejemplo de uso</td></tr><tr><td><code>-l USUARIO</code> o <code>-L ARCHIVO</code></td><td>Opciones de inicio de sesión: especifique un solo nombre de usuario ( <code>-l</code>) o un archivo que contenga una lista de nombres de usuario ( <code>-L</code>).</td><td><code>hydra -l admin ...</code> o <code>hydra -L usernames.txt ...</code></td></tr><tr><td><code>-p PASS</code> o <code>-P ARCHIVO</code></td><td>Opciones de contraseña: proporcione una única contraseña ( <code>-p</code>) o un archivo que contenga una lista de contraseñas ( <code>-P</code>).</td><td><code>hydra -p password123 ...</code> o<code>hydra -P passwords.txt ...</code></td></tr><tr><td><code>-t TASKS</code></td><td>Tareas: define la cantidad de tareas paralelas (subprocesos) a ejecutar, lo que potencialmente acelerará el ataque.</td><td><code>hydra -t 4 ...</code></td></tr><tr><td><code>-f</code></td><td>Modo rápido: detiene el ataque después de encontrar el primer inicio de sesión exitoso.</td><td><code>hydra -f ...</code></td></tr><tr><td><code>-s PUERTO</code></td><td>Puerto: especifique un puerto no predeterminado para el servicio de destino.</td><td><code>hydra -s 2222 ...</code></td></tr><tr><td><code>-v</code> o <code>-V</code></td><td>Salida detallada: muestra información detallada sobre el progreso del ataque, incluidos los intentos y los resultados.</td><td><code>hydra -v ...</code> o <code>hydra -V ...</code>(para mayor verbosidad)</td></tr><tr><td><code>service://server</code></td><td>Objetivo: especifique el servicio (por ejemplo, <code>ssh</code>, <code>http</code>, <code>ftp</code>) y la dirección o el nombre de host del servidor de destino.</td><td><code>hydra ssh://192.168.1.100</code></td></tr><tr><td><code>/OPT</code></td><td>Opciones específicas del servicio: proporcione cualquier opción adicional requerida por el servicio de destino.</td><td><code>hydra http-get://example.com/login.php -m "POST:user=^USER^&#x26;pass=^PASS^"</code>(para autenticación basada en formulario HTTP)</td></tr></tbody></table>

## <mark style="color:purple;">Servicios Hydra</mark>

Los servicios de Hydra definen esencialmente los protocolos o servicios específicos a los que Hydra puede acceder. Permiten que Hydra interactúe con diferentes mecanismos de autenticación utilizados por diversos sistemas, aplicaciones y servicios de red. Cada módulo está diseñado para comprender los patrones de comunicación y los requisitos de autenticación de un protocolo específico, lo que permite a Hydra enviar solicitudes de inicio de sesión adecuadas e interpretar las respuestas. A continuación, se muestra una tabla de servicios de uso común:

<table data-header-hidden><thead><tr><th width="132"></th><th width="154.8671875"></th><th></th><th></th></tr></thead><tbody><tr><td>Servicio</td><td>Servicio/Protocolo</td><td>Descripción</td><td>Comando de ejemplo</td></tr><tr><td>FTP</td><td>Protocolo de transferencia de archivos (FTP)</td><td>Se utiliza para forzar las credenciales de inicio de sesión para servicios FTP, comúnmente utilizados para transferir archivos a través de una red.</td><td><code>hydra -l admin -P /path/to/password_list.txt ftp://192.168.1.100</code></td></tr><tr><td>ssh</td><td>Shell seguro (SSH)</td><td>Dirige los servicios SSH a credenciales de fuerza bruta, comúnmente utilizadas para el inicio de sesión remoto seguro en los sistemas.</td><td><code>hydra -l root -P /path/to/password_list.txt ssh://192.168.1.100</code></td></tr><tr><td>http-get/post</td><td>Servicios web HTTP</td><td>Se utiliza para forzar las credenciales de inicio de sesión para formularios de inicio de sesión web HTTP mediante solicitudes GET o POST.</td><td><code>hydra -l admin -P /path/to/password_list.txt http-post-form "/login.php:user=^USER^&#x26;pass=^PASS^:F=incorrect"</code></td></tr><tr><td>SMTP</td><td>Protocolo simple de transferencia de correo</td><td>Ataca servidores de correo electrónico mediante la fuerza bruta de las credenciales de inicio de sesión para SMTP, comúnmente utilizadas para enviar correos electrónicos.</td><td><code>hydra -l admin -P /path/to/password_list.txt smtp://mail.server.com</code></td></tr><tr><td>pop3</td><td>Protocolo de oficina postal (POP3)</td><td>Dirige los servicios de recuperación de correo electrónico para forzar la obtención de credenciales para el inicio de sesión POP3.</td><td><code>hydra -l user@example.com -P /path/to/password_list.txt pop3://mail.server.com</code></td></tr><tr><td>IMAP</td><td>Protocolo de acceso a mensajes de Internet</td><td>Se utiliza para forzar las credenciales de los servicios IMAP, que permiten a los usuarios acceder a su correo electrónico de forma remota.</td><td><code>hydra -l user@example.com -P /path/to/password_list.txt imap://mail.server.com</code></td></tr><tr><td>MySQL</td><td>Base de datos MySQL</td><td>Intentos de forzar la obtención de credenciales de inicio de sesión para bases de datos MySQL.</td><td><code>hydra -l root -P /path/to/password_list.txt mysql://192.168.1.100</code></td></tr><tr><td>mssql</td><td>Microsoft SQL Server</td><td>Dirige a servidores Microsoft SQL para forzar la obtención de credenciales de inicio de sesión de la base de datos.</td><td><code>hydra -l sa -P /path/to/password_list.txt mssql://192.168.1.100</code></td></tr><tr><td>VNC</td><td>Computación en red virtual (VNC)</td><td>Servicios VNC de fuerza bruta, utilizados para acceso a escritorio remoto.</td><td><code>hydra -P /path/to/password_list.txt vnc://192.168.1.100</code></td></tr><tr><td>RDP</td><td>Protocolo de escritorio remoto (RDP)</td><td>Tiene como objetivo los servicios RDP de Microsoft para realizar ataques de fuerza bruta al inicio de sesión remoto.</td><td><code>hydra -l admin -P /path/to/password_list.txt rdp://192.168.1.100</code></td></tr></tbody></table>

## <mark style="color:purple;">Autenticación HTTP por fuerza bruta</mark>

Imagina que te encargan probar la seguridad de un sitio web mediante autenticación HTTP básica en `www.example.com`. Tienes una lista de posibles nombres de usuario almacenados en `usernames.txt`y sus correspondientes contraseñas en `passwords.txt`. Para lanzar un ataque de fuerza bruta contra este servicio HTTP, usa el siguiente comando de Hydra:

```shell-session
afsh4ck@kali$ hydra -L usernames.txt -P passwords.txt www.example.com http-get
```

Este comando le indica a Hydra que:

* Utilice la lista de nombres de usuario del archivo `usernames.txt`.
* Utilice la lista de contraseñas del archivo `passwords.txt`.
* Apunte al sitio web `www.example.com`.
* Utilice el módulo `http-get` para probar la autenticación HTTP.

Hydra probará sistemáticamente cada combinación de nombre de usuario y contraseña en el sitio web de destino para descubrir un inicio de sesión válido.

## <mark style="color:purple;">Bruteforce de múltiples servidores SSH</mark>

Imagine una situación en la que ha identificado varios servidores que podrían ser vulnerables a ataques de fuerza bruta SSH. Compila sus direcciones IP en un archivo llamado `targets.txt` y sabe que estos servidores podrían usar el nombre de usuario predeterminado "`root`" y la contraseña "`toor`". Para probar eficazmente todos estos servidores simultáneamente, use el siguiente comando de Hydra:

```shell-session
afsh4ck@kali$ hydra -l root -p toor -M targets.txt ssh
```

Este comando le indica a Hydra que:

* Utilice el nombre de usuario "`root`".
* Utilice la contraseña "`toor`".
* Apunte a todas las direcciones IP enumeradas en el archivo `targets.txt`.
* Utilice el módulo `ssh` para el ataque.

Hydra ejecutará intentos de fuerza bruta paralelos en cada servidor, acelerando significativamente el proceso.

## <mark style="color:purple;">Bruteforce de FTP en un puerto no estándar</mark>

Imagina que necesitas evaluar la seguridad de un servidor FTP alojado en `ftp.example.com`, que opera en un puerto no estándar `2121`. Tienes listas de posibles nombres de usuario y contraseñas almacenadas en  `usernames.txt`y `passwords.txt`, respectivamente. Para probar estas credenciales con el servicio FTP, usa el siguiente comando de Hydra:

```shell-session
afsh4ck@kali$ hydra -L usernames.txt -P passwords.txt -s 2121 -V ftp.example.com ftp
```

Este comando le indica a Hydra que:

* Utilice la lista de nombres de usuario `usernames.txt`.
* Utilice la lista de contraseñas `passwords.txt`.
* Apunte al servicio FTP `ftp.example.com` a través del puerto `2121`.
* Utilice el módulo `ftp` y proporcione una salida detallada (`-V`) para un monitoreo detallado.

Hydra intentará hacer coincidir cada combinación de nombre de usuario y contraseña con el servidor FTP en el puerto especificado.

## <mark style="color:purple;">Bruteforce de formulario de inicio de sesión web</mark>

Supongamos que se le solicita que ataque por fuerza bruta un formulario de inicio de sesión en una aplicación web en `www.example.com`. Sabe que el nombre de usuario es "`admin`" y que los parámetros del formulario de inicio de sesión son `user=^USER^&pass=^PASS^`. Para realizar este ataque, use el siguiente comando de Hydra:

```shell-session
afsh4ck@kali$ hydra -l admin -P passwords.txt www.example.com http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
```

Este comando le indica a Hydra que:

* Utilice el nombre de usuario "`admin`".
* Utilice la lista de contraseñas `passwords.txt`.
* Apunte al formulario de inicio de sesión `/login` en `www.example.com`.
* Utilice el módulo `http-post-form` con los parámetros de formulario especificados.
* Busque un inicio de sesión exitoso indicado por el código de estado HTTP `302`.

Hydra intentará sistemáticamente cada contraseña para la cuenta "admin", verificando la condición de éxito especificada.

## <mark style="color:purple;">Bruteforce avanzado de RDP</mark>

Ahora, imagina que estás probando un servicio de Protocolo de Escritorio Remoto (RDP) en un servidor con IP `192.168.1.100`. Sospechas que el nombre de usuario es "`administrator`" y que la contraseña consta de 6 a 8 caracteres, incluyendo minúsculas, mayúsculas y números. Para ejecutar este ataque, usa el siguiente comando de Hydra:

```shell-session
afsh4ck@kali$ hydra -l administrator -x 6:8:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 192.168.1.100 rdp
```

Este comando le indica a Hydra que:

* Utilice el nombre de usuario "`administrator`".
* Genere y pruebe contraseñas de entre 6 y 8 caracteres, utilizando el conjunto de caracteres especificado.
* Apunte al servicio RDP en `192.168.1.100`.
* Utilice el módulo `rdp` para el ataque.

Hydra generará y probará todas las combinaciones de contraseñas posibles dentro de los parámetros especificados, intentando ingresar al servicio RDP.
