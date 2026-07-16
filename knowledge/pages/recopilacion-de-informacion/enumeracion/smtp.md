
# SMTP

## <mark style="color:purple;">¿Cómo funciona SMTP?</mark>

Se puede utilizar entre un cliente de correo electrónico y un servidor de correo saliente o entre dos servidores SMTP. SMTP a menudo se combina con los protocolos IMAP o POP3, que pueden recuperar y enviar correos electrónicos. En principio es un protocolo basado en cliente-servidor, aunque se puede utilizar SMTP entre un cliente y un servidor y entre dos servidores SMTP. En este caso, un servidor actúa efectivamente como cliente.

De forma predeterminada, los servidores SMTP aceptan solicitudes de conexión en el puerto `25`. Sin embargo, los servidores SMTP más nuevos también utilizan otros puertos como el puerto TCP `587`. Este puerto se utiliza para recibir correo de usuarios/servidores autenticados, normalmente utilizando el comando STARTTLS para cambiar la conexión de texto sin formato existente a una conexión cifrada. Los datos de autenticación están protegidos y ya no son visibles en texto sin formato en la red.&#x20;

Al inicio de la conexión, la autenticación ocurre cuando el cliente confirma su identidad con un nombre de usuario y contraseña. Luego se pueden transmitir los correos electrónicos. Para ello, el cliente envía al servidor las direcciones del remitente y del destinatario, el contenido del correo electrónico y otra información y parámetros. Una vez transmitido el correo electrónico, la conexión se vuelve a finalizar. Luego, el servidor de correo electrónico comienza a enviar el correo electrónico a otro servidor SMTP.

SMTP funciona sin cifrar, sin medidas adicionales y transmite todos los comandos, datos o información de autenticación en texto sin formato. Para evitar la lectura no autorizada de datos, el SMTP se utiliza junto con el cifrado SSL/TLS. En determinadas circunstancias, un servidor utiliza un puerto distinto del puerto TCP estándar `25`para la conexión cifrada, por ejemplo, el puerto TCP `465`.

Una función esencial de un servidor SMTP es prevenir el spam mediante mecanismos de autenticación que permiten que sólo los usuarios autorizados envíen correos electrónicos. Para ello, la mayoría de los servidores SMTP modernos admiten la extensión del protocolo ESMTP con SMTP-Auth. Después de enviar su correo electrónico, el cliente SMTP, también conocido como `Mail User Agent`( `MUA`), lo convierte en un encabezado y un cuerpo y los carga en el servidor SMTP. Éste tiene la denominada `Mail Transfer Agent`( `MTA`), la base del software para enviar y recibir correos electrónicos. El MTA comprueba el tamaño del correo electrónico y el spam y luego lo almacena.&#x20;

Para aliviar el MTA, en ocasiones va precedido de un `Mail Submission Agent`( `MSA`), que comprueba la validez, es decir, el origen del correo electrónico. Este `MSA` también se llama servidor. `Relay` . Estos son muy importantes más adelante, ya que en muchos servidores SMTP pueden realizarse `Open Relay Attacks` debido a una configuración incorrecta. Discutiremos este ataque y cómo identificar su punto débil un poco más adelante. Luego, el MTA busca en el DNS la dirección IP del servidor de correo del destinatario.

Al llegar al servidor SMTP de destino, los paquetes de datos se vuelven a ensamblar para formar un correo electrónico completo. Desde allí, `Mail delivery agent`( `MDA`) lo transfiere al buzón del destinatario.

<table data-header-hidden><thead><tr><th></th><th width="52"></th><th></th><th width="51"></th><th></th><th width="51"></th><th></th><th width="47"></th><th></th></tr></thead><tbody><tr><td>Cliente ( <code>MUA</code>)</td><td><code>➞</code></td><td>Agente de envío ( <code>MSA</code>)</td><td><code>➞</code></td><td>Open Relay ( <code>MTA</code>)</td><td><code>➞</code></td><td>Agente de entrega de correo ( <code>MDA</code>)</td><td><code>➞</code></td><td>Buzón ( <code>POP3</code>/ <code>IMAP</code>)</td></tr></tbody></table>

Pero SMTP tiene dos desventajas inherentes al protocolo de red.

1. La primera es que enviar un correo electrónico mediante SMTP no devuelve una confirmación de entrega utilizable. Aunque las especificaciones del protocolo prevén este tipo de notificación, su formato no se especifica de forma predeterminada, por lo que normalmente sólo se devuelve un mensaje de error en inglés, incluido el encabezado del mensaje no entregado.
2. Los usuarios no se autentican cuando se establece una conexión y, por tanto, el remitente de un correo electrónico no es fiable. Como resultado, los repetidores SMTP abiertos a menudo se utilizan indebidamente para enviar spam en masa. Para no ser rastreados, los autores utilizan direcciones de remitentes falsas y arbitrarias (mail spoofing). Hoy en día, se utilizan muchas técnicas de seguridad diferentes para evitar el uso indebido de servidores SMTP. Por ejemplo, los correos electrónicos sospechosos se rechazan o se ponen en cuarentena (carpeta de correo no deseado). Por ejemplo, los responsables de esto son el protocolo de identificación [DomainKeys](http://dkim.org/) ( `DKIM`), el [Sender Policy Framework](https://dmarcian.com/what-is-spf/) ( `SPF`).

Para ello se ha desarrollado una extensión para SMTP llamada `Extended SMTP`( `ESMTP`). Cuando la gente habla de SMTP en general, normalmente se refiere a ESMTP. ESMTP usa TLS, que se realiza después del `EHLO`comando enviando `STARTTLS`. Esto inicializa la conexión SMTP protegida por SSL y, a partir de este momento, toda la conexión queda cifrada y, por tanto, más o menos segura. Ahora la extensión [AUTH PLAIN](https://www.samlogic.net/articles/smtp-commands-reference-auth.htm) para autenticación también se puede utilizar de forma segura.

***

## <mark style="color:purple;">Configuración predeterminada</mark>

Cada servidor SMTP se puede configurar de muchas maneras, al igual que todos los demás servicios. Sin embargo, existen diferencias porque el servidor SMTP solo es responsable de enviar y reenviar correos electrónicos.

```bash
afsh4ck$ cat /etc/postfix/main.cf | grep -v "#" | sed -r "/^\s*$/d"

smtpd_banner = ESMTP Server 
biff = no
append_dot_mydomain = no
readme_directory = no
compatibility_level = 2
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
myhostname = mail1.inlanefreight.htb
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
smtp_generic_maps = hash:/etc/postfix/generic
mydestination = $myhostname, localhost 
masquerade_domains = $myhostname
mynetworks = 127.0.0.0/8 10.129.0.0/16
mailbox_size_limit = 0
recipient_delimiter = +
smtp_bind_address = 0.0.0.0
inet_protocols = ipv4
smtpd_helo_restrictions = reject_invalid_hostname
home_mailbox = /home/postfix
```

El envío y la comunicación también se realizan mediante comandos especiales que hacen que el servidor SMTP haga lo que el usuario requiere.

<table data-header-hidden><thead><tr><th width="159"></th><th></th></tr></thead><tbody><tr><td><strong>Dominio</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>AUTH PLAIN</code></td><td>AUTH es una extensión de servicio utilizada para autenticar al cliente.</td></tr><tr><td><code>HELO</code></td><td>El cliente inicia sesión con el nombre de su computadora y así inicia la sesión.</td></tr><tr><td><code>MAIL FROM</code></td><td>El cliente nombra el remitente del correo electrónico.</td></tr><tr><td><code>RCPT TO</code></td><td>El cliente nombra el destinatario del correo electrónico.</td></tr><tr><td><code>DATA</code></td><td>El cliente inicia la transmisión del correo electrónico.</td></tr><tr><td><code>RSET</code></td><td>El cliente aborta la transmisión iniciada pero mantiene la conexión entre el cliente y el servidor.</td></tr><tr><td><code>VRFY</code></td><td>El cliente comprueba si hay un buzón disponible para la transferencia de mensajes.</td></tr><tr><td><code>EXPN</code></td><td>El cliente también verifica si hay un buzón disponible para enviar mensajes con este comando.</td></tr><tr><td><code>NOOP</code></td><td>El cliente solicita una respuesta del servidor para evitar la desconexión por tiempo de espera.</td></tr><tr><td><code>QUIT</code></td><td>El cliente finaliza la sesión.</td></tr></tbody></table>

Para interactuar con el servidor SMTP, podemos usar la `telnet`herramienta para inicializar una conexión TCP con el servidor SMTP. La inicialización real de la sesión se realiza con el comando mencionado anteriormente, `HELO`o `EHLO`.

### **Telnet-HELO/EHLO**

```shell-session
afsh4ck$ telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server 

HELO mail1.inlanefreight.htb

250 mail1.inlanefreight.htb

EHLO mail1

250-mail1.inlanefreight.htb
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING
```

El comando `VRFY` se puede utilizar para enumerar los usuarios existentes en el sistema. Sin embargo, esto no siempre funciona. Dependiendo de cómo esté configurado el servidor SMTP, el servidor SMTP puede emitir `code 252` y confirmar la existencia de un usuario que no existe en el sistema. Puede encontrar una lista de todos los códigos de respuesta SMTP [aquí](https://serversmtp.com/smtp-error/) .

### **Telnet-VRFY**

```shell-session
afsh4ck$ telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server 

VRFY root
252 2.0.0 root

VRFY cry0l1t3
252 2.0.0 cry0l1t3

VRFY testuser
252 2.0.0 testuser

VRFY aaaaaaaaaaaaaaaaaaaaaaaaaaaa
252 2.0.0 aaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Por lo tanto, nunca se debe confiar enteramente en los resultados de las herramientas automáticas. Después de todo, ejecutan comandos preconfigurados, pero ninguna de las funciones indica explícitamente cómo el administrador configura el servidor probado.

En ocasiones es posible que tengamos que trabajar a través de un proxy web. También podemos hacer que este proxy web se conecte al servidor SMTP. El comando que enviaríamos entonces se vería así: `CONNECT 10.129.14.128:25 HTTP/1.0`

Todos los comandos que ingresamos en la línea de comando para enviar un correo electrónico los conocemos de todos los programas cliente de correo electrónico como Thunderbird, Gmail, Outlook y muchos otros. Especificamos el destinatario `subject` del correo electrónico, CC, BCC y la información que queremos compartir con otros. Por supuesto, lo mismo funciona desde la línea de comando.

### **Enviar un correo electrónico**

```shell-session
afsh4ck$ telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server


EHLO inlanefreight.htb

250-mail1.inlanefreight.htb
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING


MAIL FROM: <cry0l1t3@inlanefreight.htb>

250 2.1.0 Ok


RCPT TO: <mrb3n@inlanefreight.htb> NOTIFY=success,failure

250 2.1.5 Ok


DATA

354 End data with <CR><LF>.<CR><LF>

From: <cry0l1t3@inlanefreight.htb>
To: <mrb3n@inlanefreight.htb>
Subject: DB
Date: Tue, 28 Sept 2021 16:32:51 +0200
Hey man, I am trying to access our XY-DB but the creds don't work. 
Did you make any changes there?
.

250 2.0.0 Ok: queued as 6E1CF1681AB


QUIT

221 2.0.0 Bye
Connection closed by foreign host.
```

El encabezado del correo es el portador de una gran cantidad de información interesante en un correo electrónico. Entre otras cosas, proporciona información sobre el remitente y el destinatario, la hora de envío y llegada, las estaciones por las que pasó el correo electrónico en su camino, el contenido y formato del mensaje, y el remitente y el destinatario.

Parte de esta información es obligatoria, como la información del remitente y cuándo se creó el correo electrónico. Otra información es opcional. Sin embargo, el encabezado del correo electrónico no contiene ninguna información necesaria para la entrega técnica. Se transmite como parte del protocolo de transmisión. Tanto el remitente como el destinatario pueden acceder al encabezado de un correo electrónico, aunque no sea visible a primera vista. La estructura de un encabezado de correo electrónico está definida por [RFC5322](https://datatracker.ietf.org/doc/html/rfc5322) .

***

## <mark style="color:purple;">Configuraciones peligrosas</mark>

Para evitar que los correos electrónicos enviados sean filtrados por filtros de spam y no lleguen al destinatario, el remitente puede utilizar un servidor de retransmisión en el que el destinatario confíe. Es un servidor SMTP conocido y verificado por todos los demás. Como regla general, el remitente debe autenticarse en el servidor de retransmisión antes de utilizarlo.

A menudo, los administradores no tienen una visión general de qué rangos de IP deben permitir. Esto da como resultado una mala configuración del servidor SMTP que todavía encontraremos a menudo en las pruebas de penetración externas e internas. Por tanto, permiten que todas las direcciones IP no provoquen errores en el tráfico de correo electrónico y así no perturben o interrumpan involuntariamente la comunicación con los clientes actuales y potenciales.

### **Configuración de Open Relay**

```shell-session
mynetworks = 0.0.0.0/0
```

Con esta configuración, este servidor SMTP puede enviar correos electrónicos falsos y así inicializar la comunicación entre varias partes. Otra posibilidad de ataque sería falsificar el correo electrónico y leerlo.

***

## <mark style="color:purple;">Enumerando el servicio</mark>

Los scripts predeterminados de Nmap incluyen `smtp-commands`, que utiliza el comando `EHLO` para enumerar todos los comandos posibles que se pueden ejecutar en el servidor SMTP de destino.

### **Nmap**

```bash
afsh4ck$ sudo nmap 10.129.14.128 -sC -sV -p25

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-27 17:56 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00025s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
|_smtp-commands: mail1.inlanefreight.htb, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING, 
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.09 seconds
```

Sin embargo, también podemos utilizar el script NSE [smtp-open-relay](https://nmap.org/nsedoc/scripts/smtp-open-relay.html) para identificar el servidor SMTP de destino como un Open Relay mediante 16 pruebas diferentes. Si también imprimimos el resultado del escaneo en detalle, también podremos ver qué pruebas está ejecutando el script.

### Scripts NSE disponibles

```bash
ls -al /usr/share/nmap/scripts/ | grep -e "smtp"
.rw-r--r-- root root 4.2 KB Thu Nov  2 03:10:47 2023 smtp-brute.nse
.rw-r--r-- root root 4.8 KB Thu Nov  2 03:10:47 2023 smtp-commands.nse
.rw-r--r-- root root  12 KB Thu Nov  2 03:10:47 2023 smtp-enum-users.nse
.rw-r--r-- root root 5.7 KB Thu Nov  2 03:10:47 2023 smtp-ntlm-info.nse
.rw-r--r-- root root 9.9 KB Thu Nov  2 03:10:47 2023 smtp-open-relay.nse
.rw-r--r-- root root 716 B  Thu Nov  2 03:10:47 2023 smtp-strangeport.nse
.rw-r--r-- root root  14 KB Thu Nov  2 03:10:47 2023 smtp-vuln-cve2010-4344.nse
.rw-r--r-- root root 7.5 KB Thu Nov  2 03:10:47 2023 smtp-vuln-cve2011-1720.nse
.rw-r--r-- root root 7.4 KB Thu Nov  2 03:10:47 2023 smtp-vuln-cve2011-1764.nse
```

### **Nmap - Open Relay**

```bash
afsh4ck$ sudo nmap -v 10.129.14.128 -p25 --script smtp-open-relay

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-30 02:29 CEST
NSE: Loaded 1 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.00s elapsed
Initiating ARP Ping Scan at 02:29
Scanning 10.129.14.128 [1 port]
Completed ARP Ping Scan at 02:29, 0.06s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 02:29
Completed Parallel DNS resolution of 1 host. at 02:29, 0.03s elapsed
Initiating SYN Stealth Scan at 02:29
Scanning 10.129.14.128 [1 port]
Discovered open port 25/tcp on 10.129.14.128
Completed SYN Stealth Scan at 02:29, 0.06s elapsed (1 total ports)
NSE: Script scanning 10.129.14.128.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.07s elapsed
Nmap scan report for 10.129.14.128
Host is up (0.00020s latency).

PORT   STATE SERVICE
25/tcp open  smtp
| smtp-open-relay: Server is an open relay (16/16 tests)
|  MAIL FROM:<> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@nmap.scanme.org> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@ESMTP> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest%nmap.scanme.org@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest%nmap.scanme.org@ESMTP>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest@nmap.scanme.org">
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest%nmap.scanme.org">
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest@nmap.scanme.org"@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org@ESMTP>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<@[10.129.14.128]:relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<@ESMTP:relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest@[10.129.14.128]>
|_ MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest@ESMTP>
MAC Address: 00:00:00:00:00:00 (VMware)

NSE: Script Post-scanning.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.48 seconds
           Raw packets sent: 2 (72B) | Rcvd: 2 (72B)
```

### Enumeración de usuarios SMTP

{% embed url="<https://github.com/pentestmonkey/smtp-user-enum>" %}

Lo podemos instalar de la siguiente manera:

```bash
sudo apt install smtp-user-enum
```

```perl
perl smtp-user-enum.pl 
smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

Usage: smtp-user-enum.pl [options] ( -u username | -U file-of-usernames ) ( -t host | -T file-of-targets )

options are:
        -m n     Maximum number of processes (default: 5)
	-M mode  Method to use for username guessing EXPN, VRFY or RCPT (default: VRFY)
	-u user  Check if user exists on remote system
	-f addr  MAIL FROM email address.  Used only in "RCPT TO" mode (default: user@example.com)
        -D dom   Domain to append to supplied user list to make email addresses (Default: none)
                 Use this option when you want to guess valid email addresses instead of just usernames
                 e.g. "-D example.com" would guess foo@example.com, bar@example.com, etc.  Instead of 
                      simply the usernames foo and bar.
	-U file  File of usernames to check via smtp service
	-t host  Server host running smtp service
	-T file  File of hostnames running the smtp service
	-p port  TCP port on which smtp service runs (default: 25)
	-d       Debugging output
	-t n     Wait a maximum of n seconds for reply (default: 5)
	-v       Verbose
	-h       This help message

Also see smtp-user-enum-user-docs.pdf from the smtp-user-enum tar ball.

Examples:

$ smtp-user-enum.pl -M VRFY -U users.txt -t 10.0.0.1
$ smtp-user-enum.pl -M EXPN -u admin1 -t 10.0.0.1
$ smtp-user-enum.pl -M RCPT -U users.txt -T mail-server-ips.txt
$ smtp-user-enum.pl -M EXPN -D example.com -U users.txt -t 10.0.0.1
```
