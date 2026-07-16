
# Medusa

Medusa, una herramienta destacada en el arsenal de ciberseguridad, está diseñada para ser un sistema de fuerza bruta de inicio de sesión rápido, masivamente paralelo y modular. Su objetivo principal es ofrecer soporte para una amplia gama de servicios que permiten la autenticación remota, lo que permite a los testers de penetración y a los profesionales de la seguridad evaluar la resiliencia de los sistemas de inicio de sesión ante ataques de fuerza bruta.

## <mark style="color:purple;">Instalación</mark>

Medusa suele venir preinstalado en distribuciones populares de pruebas de penetración como Kali Linux o ParrotOS. Puedes comprobar su presencia ejecutando:

```shell-session
afsh4ck@kali$ medusa -h
```

Instalar Medusa en un sistema Linux es sencillo.

```shell-session
afsh4ck@kali$ sudo apt-get -y update
afsh4ck@kali$ sudo apt-get -y install medusa
```

## <mark style="color:purple;">Sintaxis de comandos y tabla de parámetros</mark>

La interfaz de línea de comandos de Medusa es sencilla. Permite a los usuarios especificar hosts, usuarios, contraseñas y módulos con diversas opciones para optimizar el proceso de ataque.

```shell-session
afsh4ck@kali$ medusa [target_options] [credential_options] -M module [module_options]
```

<table data-header-hidden><thead><tr><th width="168.296875"></th><th width="329.33984375"></th><th></th></tr></thead><tbody><tr><td>Parámetro</td><td>Explicación</td><td>Ejemplo de uso</td></tr><tr><td><p><code>-h HOST</code> o</p><p><code>-H ARCHIVO</code></p></td><td>Opciones de destino: especifique un único nombre de host o dirección IP de destino (<code>-h</code>) o un archivo que contenga una lista de objetivos (<code>-H</code>)</td><td><code>medusa -h 192.168.1.10 ...</code> o <code>medusa -H targets.txt ...</code></td></tr><tr><td><code>-u USERNAME</code> o   <code>-U ARCHIVO</code></td><td>Opciones de nombre de usuario: proporcione un único nombre de usuario ( <code>-u</code>) o un archivo que contenga una lista de nombres de usuario ( <code>-U</code>).</td><td><code>medusa -u admin ...</code> o <code>medusa -U usernames.txt ...</code></td></tr><tr><td><code>-p PASSWORD</code> o   <code>-P ARCHIVO</code></td><td>Opciones de contraseña: especifique una única contraseña ( <code>-p</code>) o un archivo que contenga una lista de contraseñas ( <code>-P</code>).</td><td><code>medusa -p password123 ...</code> o <code>medusa -P passwords.txt ...</code></td></tr><tr><td><code>-M MODULE</code></td><td>Módulo: define el módulo específico que se utilizará para el ataque (por ejemplo, <code>ssh</code>, <code>ftp</code>, <code>http</code>).</td><td><code>medusa -M ssh ...</code></td></tr><tr><td><code>-m "MODULE_OPTION"</code></td><td>Opciones del módulo: proporcione parámetros adicionales requeridos por el módulo elegido, entre comillas.</td><td><code>medusa -M http -m "POST /login.php HTTP/1.1\r\nContent-Length: 30\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nusername=^USER^&#x26;password=^PASS^" ...</code></td></tr><tr><td><code>-t TASKS</code></td><td>Tareas: Definir la cantidad de intentos de inicio de sesión paralelos que se ejecutarán, lo que potencialmente acelerará el ataque.</td><td><code>medusa -t 4 ...</code></td></tr><tr><td><p><code>-f</code> o</p><p><code>-F</code></p></td><td>Modo rápido: detiene el ataque después de encontrar el primer inicio de sesión exitoso, ya sea en el host actual ( <code>-f</code>) o en cualquier host ( <code>-F</code>).</td><td><code>medusa -f ...</code>o<code>medusa -F ...</code></td></tr><tr><td><code>-n PORT</code></td><td>Puerto: especifique un puerto no predeterminado para el servicio de destino.</td><td><code>medusa -n 2222 ...</code></td></tr><tr><td><code>-v LEVEL</code></td><td>Salida detallada: Muestra información detallada sobre el progreso del ataque. Cuanto mayor sea el valor <code>LEVEL</code>(hasta 6), más detallada será la salida.</td><td><code>medusa -v 4 ...</code></td></tr></tbody></table>

### Módulos Medusa

Cada módulo de Medusa está diseñado para interactuar con mecanismos de autenticación específicos, lo que le permite enviar las solicitudes adecuadas e interpretar las respuestas para ataques exitosos. A continuación, se muestra una tabla de módulos de uso común:

<table data-header-hidden><thead><tr><th width="114.3671875"></th><th width="165.046875"></th><th width="247.33984375"></th><th></th></tr></thead><tbody><tr><td>Módulo</td><td>Servicio/Protocolo</td><td>Descripción</td><td>Ejemplo de uso</td></tr><tr><td>FTP</td><td>Protocolo de transferencia de archivos</td><td>Credenciales de inicio de sesión FTP mediante fuerza bruta, utilizadas para transferencias de archivos a través de una red.</td><td><code>medusa -M ftp -h 192.168.1.100 -u admin -P passwords.txt</code></td></tr><tr><td>HTTP</td><td>Protocolo de transferencia de hipertexto</td><td>Forzar brutamente los formularios de inicio de sesión en aplicaciones web a través de HTTP (GET/POST).</td><td><code>medusa -M http -h www.example.com -U users.txt -P passwords.txt -m DIR:/login.php -m FORM:username=^USER^&#x26;password=^PASS^</code></td></tr><tr><td>IMAP</td><td>Protocolo de acceso a mensajes de Internet</td><td>Inicios de sesión IMAP mediante fuerza bruta, a menudo utilizados para acceder a servidores de correo electrónico.</td><td><code>medusa -M imap -h mail.example.com -U users.txt -P passwords.txt</code></td></tr><tr><td>MySQL</td><td>Base de datos MySQL</td><td>Fuerza bruta de las credenciales de la base de datos MySQL, comúnmente utilizada para aplicaciones web y bases de datos.</td><td><code>medusa -M mysql -h 192.168.1.100 -u root -P passwords.txt</code></td></tr><tr><td>POP3</td><td>Protocolo de Correos 3</td><td>Inicios de sesión POP3 mediante fuerza bruta, normalmente utilizados para recuperar correos electrónicos de un servidor de correo.</td><td><code>medusa -M pop3 -h mail.example.com -U users.txt -P passwords.txt</code></td></tr><tr><td>RDP</td><td>Protocolo de escritorio remoto</td><td>Inicios de sesión RDP mediante fuerza bruta, comúnmente utilizados para acceso de escritorio remoto a sistemas Windows.</td><td><code>medusa -M rdp -h 192.168.1.100 -u admin -P passwords.txt</code></td></tr><tr><td>SSHv2</td><td>Shell seguro (SSH)</td><td>Inicios de sesión SSH mediante fuerza bruta, comúnmente utilizados para acceso remoto seguro.</td><td><code>medusa -M ssh -h 192.168.1.100 -u root -P passwords.txt</code></td></tr><tr><td>Subversión (SVN)</td><td>Sistema de control de versiones</td><td>Forzar brutamente los repositorios de Subversion (SVN) para el control de versiones.</td><td><code>medusa -M svn -h 192.168.1.100 -u admin -P passwords.txt</code></td></tr><tr><td>Telnet</td><td>Protocolo Telnet</td><td>Servicios Telnet de fuerza bruta para ejecución remota de comandos en sistemas más antiguos.</td><td><code>medusa -M telnet -h 192.168.1.100 -u admin -P passwords.txt</code></td></tr><tr><td>VNC</td><td>Computación en red virtual</td><td>Forzar brutamente las credenciales de inicio de sesión de VNC para acceder al escritorio remoto.</td><td><code>medusa -M vnc -h 192.168.1.100 -P passwords.txt</code></td></tr><tr><td>Formulario web</td><td>Formularios de inicio de sesión web mediante fuerza bruta</td><td>Forzar brutamente los formularios de inicio de sesión en sitios web mediante solicitudes HTTP POST.</td><td><code>medusa -M web-form -h www.example.com -U users.txt -P passwords.txt -m FORM:"username=^USER^&#x26;password=^PASS^:F=Invalid"</code></td></tr></tbody></table>

### Bruteforce a un servidor SSH

Imagina un escenario en el que necesitas probar la seguridad de un servidor SSH en la IP `192.168.0.100`. Tienes una lista de posibles nombres de usuario en `usernames.txt`y contraseñas comunes en `passwords.txt`. Para lanzar un ataque de fuerza bruta contra el servicio SSH en este servidor, podemos usar el siguiente comando de Medusa:

```shell-session
afsh4ck@kali$ medusa -h 192.168.0.100 -U usernames.txt -P passwords.txt -M ssh 
```

Este comando le ordena a Medusa que:

* Apunta al host en `192.168.0.100`.
* Utilice los nombres de usuario del archivo `usernames.txt`.
* Pruebe las contraseñas que aparecen en el archivo `passwords.txt`.
* Utilice el módulo `ssh` para el ataque.

Medusa probará sistemáticamente cada combinación de nombre de usuario y contraseña contra el servicio SSH para intentar obtener acceso no autorizado.

### Bruteforce a varios servidores web con autenticación HTTP básica

Supongamos que tiene una lista de servidores web que utilizan autenticación HTTP básica. Las direcciones de estos servidores se almacenan en `web_servers.txt` y también tiene listas de nombres de usuario y contraseñas comunes en `usernames.txt` y `passwords.txt`, respectivamente. Para probar estos servidores simultáneamente, ejecute:

```shell-session
afsh4ck@kali$ medusa -H web_servers.txt -U usernames.txt -P passwords.txt -M http -m GET 
```

En este caso, Medusa:

* Itera a través de la lista de servidores web en `web_servers.txt`.
* Utiliza los nombres de usuario y contraseñas proporcionados.
* Utiliza el módulo `http` con el `GET`método para intentar iniciar sesión.

Al ejecutar varios subprocesos, Medusa verifica eficientemente cada servidor en busca de credenciales débiles.

### Prueba de contraseñas vacías o predeterminadas

Si desea evaluar si alguna cuenta en un host específico (`10.0.0.5`) tiene contraseñas vacías o predeterminadas (donde la contraseña coincide con el nombre de usuario), puede usar:

```shell-session
afsh4ck@kali$ medusa -h 10.0.0.5 -U usernames.txt -e ns -M service_name
```

Este comando le ordena a Medusa que:

* Apunte al host en `10.0.0.5`.
* Utilice los nombres de usuario de `usernames.txt`.
* Realice comprobaciones adicionales de contraseñas vacías (`-e n`) y contraseñas que coincidan con el nombre de usuario (`-e s`).
* Utilice el módulo de servicio apropiado (reemplácelo `service_name` con el nombre del módulo correcto).

Medusa probará cada nombre de usuario con una contraseña vacía y luego con la contraseña que coincida con el nombre de usuario, revelando potencialmente cuentas con configuraciones débiles o predeterminadas.
