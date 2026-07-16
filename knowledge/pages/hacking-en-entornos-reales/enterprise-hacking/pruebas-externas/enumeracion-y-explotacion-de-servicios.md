
# Enumeración y explotación de servicios

## <mark style="color:purple;">Servicios de escucha</mark>

Nuestros escaneos de Nmap descubrieron algunos servicios interesantes:

* Puerto 21: FTP
* Puerto 22: SSH
* Puerto 25: SMTP
* Puerto 53: DNS
* Puerto 80: HTTP
* Puertos 110/143/993/995: imap y pop3
* Puerto 111: rpcbind

Ya realizamos una transferencia de zona DNS durante nuestra recopilación inicial de información, lo que generó varios subdominios que analizaremos más a fondo más adelante. No vale la pena intentar otros ataques DNS en nuestro entorno actual.

***

## <mark style="color:purple;">FTP</mark>

Comencemos con FTP en el puerto 21. El análisis agresivo de Nmap detectó que era posible iniciar sesión anónimamente por FTP. Confirmémoslo manualmente.

```shell-session
afsh4ck@kali$ ftp 10.129.203.101

Connected to 10.129.203.101.
220 (vsFTPd 3.0.3)
Name (10.129.203.101:tester): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0              38 May 30 17:16 flag.txt
226 Directory send OK.
ftp>
```

La conexión con el usuario `anonymous` y una contraseña en blanco funciona. Parece que no podemos acceder a ningún archivo interesante, salvo a uno, y tampoco podemos cambiar de directorio.

```bash
ftp> put test.txt 

local: test.txt remote: test.txt
200 PORT command successful. Consider using PASV.
550 Permission denied.
```

Tampoco podemos cargar ningún archivo.

Es improbable que se produzcan otros ataques, como un ataque de rebote FTP, y aún no disponemos de información sobre la red interna. La búsqueda de exploits públicos para vsFTPd 3.0.3 solo muestra [esta](https://www.exploit-db.com/exploits/49719) PoC para `Remote Denial of Service`, lo cual queda fuera del alcance de nuestras pruebas. La fuerza bruta tampoco nos servirá en este caso, ya que desconocemos los nombres de usuario.

Esto parece un callejón sin salida. Sigamos adelante.

***

## <mark style="color:purple;">SSH</mark>

A continuación, SSH. Empezaremos con una captura de banner:

```shell-session
afsh4ck@kali$ nc -nv 10.129.203.101 22

(UNKNOWN) [10.129.203.101] 22 (ssh) open
SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
```

Esto nos indica que el host ejecuta OpenSSH versión 8.2, que no presenta vulnerabilidades conocidas al momento de escribir este artículo. Podríamos intentar forzar la contraseña, pero no tenemos una lista de nombres de usuario válidos, así que sería arriesgado. También es dudoso que podamos forzar la contraseña de root. Podemos probar algunas combinaciones como `admin:admin`, `root:toor`, `admin:Welcome`, `admin:Pass123` pero sin éxito.

```shell-session
afsh4ck@kali$ ssh admin@10.129.203.101

The authenticity of host '10.129.203.101 (10.129.203.101)' can't be established.
ECDSA key fingerprint is SHA256:3I77Le3AqCEUd+1LBAraYTRTF74wwJZJiYcnwfF5yAs.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.203.101' (ECDSA) to the list of known hosts.
admin@10.129.203.101's password: 
Permission denied, please try again.
```

SSH también parece un callejón sin salida. Veamos qué más tenemos.

***

## <mark style="color:purple;">Servicios de correo electrónico</mark>

El protocolo SMTP es interesante. Podemos consultar la sección [`Ataques a Emails`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/atacando-servicios-comunes/ataques-a-emails.md) para obtener ayuda. En una evaluación práctica, podríamos usar un sitio web como [MXToolbox](https://mxtoolbox.com/) o la herramienta `dig` para enumerar registros MX.

Hagamos otro escaneo contra el puerto 25 para buscar configuraciones incorrectas.

```shell-session
afsh4ck@kali$ sudo nmap -sV -sC -p25 10.129.203.101

Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-20 18:55 EDT
Nmap scan report for inlanefreight.local (10.129.203.101)
Host is up (0.11s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Not valid before: 2022-05-30T17:15:40
|_Not valid after:  2032-05-27T17:15:40
|_smtp-commands: ubuntu, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING
|_ssl-date: TLS randomness does not represent time
Service Info: Host:  ubuntu

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 5.37 second
```

A continuación, comprobaremos si hay alguna configuración incorrecta relacionada con la autenticación. Podemos intentar usar el comando `VRFY` para enumerar los usuarios del sistema.

```shell-session
afsh4ck@kali$ telnet 10.129.203.101 25

Trying 10.129.203.101...
Connected to 10.129.203.101.
Escape character is '^]'.
220 ubuntu ESMTP Postfix (Ubuntu)
VRFY root
252 2.0.0 root
VRFY www-data
252 2.0.0 www-data
VRFY randomuser
550 5.1.1 <randomuser>: Recipient address rejected: User unknown in local recipient table
```

Podemos ver que el comando `VRFY` no está deshabilitado y podemos usarlo para enumerar usuarios válidos. Esto podría aprovecharse para recopilar una lista de usuarios que podríamos usar para lanzar un ataque de fuerza bruta de contraseñas contra los servicios FTP y SSH, y quizás otros. Si bien esto es de bajo riesgo, vale la pena anotarlo como hallazgo de criticidad `Low` para nuestro informe, ya que nuestros clientes deberían reducir su superficie de ataque externa tanto como sea posible. Si esta no es una razón comercial válida para habilitar este comando, deberíamos recomendarles que lo deshabiliten.

Podríamos intentar enumerar más usuarios con una herramienta como [smtp-user-enum](https://github.com/pentestmonkey/smtp-user-enum) para aclarar el asunto y potencialmente encontrar más usuarios. Normalmente no vale la pena dedicar mucho tiempo a forzar la autenticación para servicios externos. Esto podría causar una interrupción del servicio, así que incluso si logramos crear una lista de usuarios, podemos probar algunas contraseñas débiles y seguir adelante.

Podríamos repetir este proceso con los comandos `EXPN` y `RCPT TO`, pero no obtendríamos nada adicional.

El protocolo `POP3` también se puede usar para enumerar usuarios, dependiendo de su configuración. Podemos intentar enumerar los usuarios del sistema con el comando `USER` de nuevo, y si el servidor responde con `+OK`, el usuario existe en el sistema. Esto no funciona. Al escanear el puerto 995, el puerto SSL/TLS para POP3, tampoco se obtiene ningún resultado.

```shell-session
afsh4ck@kali$ telnet 10.129.203.101 110

Trying 10.129.203.101...
Connected to 10.129.203.101.
Escape character is '^]'.
+OK Dovecot (Ubuntu) ready.
user www-data
-ERR [AUTH] Plaintext authentication disallowed on non-secure (SSL/TLS) connections.
```

El módulo [`Enumeración`](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion.md) contiene más información sobre servicios comunes y principios de enumeración y vale la pena revisarlo nuevamente después de trabajar en esta sección.

Nos gustaría analizar más a fondo la implementación de correo electrónico del cliente en una evaluación real. Si utilizan Office 365 o Exchange local, podríamos lanzar un ataque de Password Spraying que permitiría el acceso a las bandejas de entrada o, potencialmente, a la red interna si conseguimos usar una contraseña válida para conectarnos a través de una VPN. También podríamos encontrarnos con un Open Relay, que podríamos usar para phishing enviando correos electrónicos con usuarios ficticios o suplantando una cuenta de correo electrónico para que parezca oficial e intentando engañar a los empleados para que introduzcan sus credenciales o ejecuten un payload.

El phishing queda fuera del alcance de esta evaluación en particular y probablemente lo estará en la mayoría de las pruebas de penetración externas, por lo que sería conveniente confirmar e informar este tipo de vulnerabilidad si la detectamos. Sin embargo, no deberíamos ir más allá de una simple validación sin consultar primero con el cliente. Sin embargo, esto podría ser extremadamente útil en una evaluación completa de Red Team.

Podemos comprobarlo de todos modos, pero no encontramos un open relay, lo cual es bueno para nuestro cliente.

```shell-session
afsh4ck@kali$ nmap -p25 -Pn --script smtp-open-relay  10.129.203.101

Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-20 19:14 EDT
Nmap scan report for inlanefreight.local (10.129.203.101)
Host is up (0.12s latency).

PORT   STATE SERVICE
25/tcp open  smtp
|_smtp-open-relay: Server doesn't seem to be an open relay, all tests failed

Nmap done: 1 IP address (1 host up) scanned in 24.30 seconds
```

***

## <mark style="color:purple;">Hacia delante</mark>

El puerto 111 es el servicio `rpcbind` que no debe exponerse externamente, por lo que podríamos generar un hallazgo `Low`, `Unnecessary Exposed Services` o algo similar. Este puerto se puede sondear para identificar el sistema operativo o recopilar información sobre los servicios disponibles. Podemos intentar escanearlo con el comando [rpcinfo](https://linux.die.net/man/8/rpcinfo) o Nmap. Funciona, pero no obtenemos nada útil. Nuevamente, conviene anotarlo para que el cliente sepa qué está exponiendo, pero no podemos hacer nada más con ello.

```shell-session
afsh4ck@kali$ rpcinfo 10.129.203.101

   program version netid     address                service    owner
    100000    4    tcp6      ::.0.111               portmapper superuser
    100000    3    tcp6      ::.0.111               portmapper superuser
    100000    4    udp6      ::.0.111               portmapper superuser
    100000    3    udp6      ::.0.111               portmapper superuser
    100000    4    tcp       0.0.0.0.0.111          portmapper superuser
    100000    3    tcp       0.0.0.0.0.111          portmapper superuser
    100000    2    tcp       0.0.0.0.0.111          portmapper superuser
    100000    4    udp       0.0.0.0.0.111          portmapper superuser
    100000    3    udp       0.0.0.0.0.111          portmapper superuser
    100000    2    udp       0.0.0.0.0.111          portmapper superuser
    100000    4    local     /run/rpcbind.sock      portmapper superuser
    100000    3    local     /run/rpcbind.sock      portmapper superuser
```

Vale la pena consultar esta guía de HackTricks sobre [Pentesting rpcbind](https://book.hacktricks.xyz/network-services-pentesting/pentesting-rpcbind) para obtener información futura sobre este servicio.

El último puerto es el puerto `80`, que, como sabemos, corresponde al servicio HTTP. Sabemos que probablemente existan múltiples aplicaciones web basadas en la enumeración de subdominios y vhosts que realizamos anteriormente. Así que, pasemos a la web.&#x20;

Aún no tenemos una base sólida ni mucho más allá de algunos hallazgos de riesgo medio y bajo. En entornos modernos, rara vez vemos servicios explotables externamente, como un servidor FTP vulnerable o similar, que conduzca a la ejecución remota de código (RCE). Sin embargo, nunca digas nunca. Hemos visto cosas más locas, por lo que siempre vale la pena explorar todas las posibilidades.&#x20;

La mayoría de las organizaciones a las que nos enfrentamos serán más susceptibles a ataques a través de sus aplicaciones web, ya que estas suelen presentar una amplia superficie de ataque, por lo que normalmente dedicaremos la mayor parte de nuestro tiempo durante una prueba de penetración externa a enumerar y atacar aplicaciones web.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.48.123

vHosts necesarios para estas preguntas:
inlanefreight.local
```

### Pregunta 1

> Enumera los servicios accesibles y encuentra una flag. Envíe el valor de la flag como respuesta

#### FTP Login Anonymous

```shell-session
afsh4ck@kali$ ftp anonymous@10.129.48.123     
                                                                                             
Connected to 10.129.48.123.
220 (vsFTPd 3.0.3)
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||40341|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0              38 May 30  2022 flag.txt
226 Directory send OK.
ftp> get flag.txt
local: flag.txt remote: flag.txt
229 Entering Extended Passive Mode (|||41130|)
150 Opening BINARY mode data connection for flag.txt (38 bytes).
100% |**************************************************************************************************************************|    38      281.13 KiB/s    00:00 ETA
226 Transfer complete.
38 bytes received in 00:00 (1.11 KiB/s)
ftp> ^D
221 Goodbye.
```

```shell-session
afsh4ck@kali$ cat flag.txt                                          
HTB{0eb0ab788df18c3115ac43b1c06ae6c4}
```
