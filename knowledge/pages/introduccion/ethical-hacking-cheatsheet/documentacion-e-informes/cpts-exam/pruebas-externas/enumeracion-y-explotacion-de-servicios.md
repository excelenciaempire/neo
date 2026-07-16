
# Enumeración y explotación de servicios

Tenemos los siguientes servicios expuestos, que procederemos a enumerar e intentar explotar:

```bash
afsh4ck@kali$ sudo nmap --open -oA trilocor_scan trilocor.local

Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-14 16:27 CST
Nmap scan report for trilocor.local (10.129.151.166)
Host is up (0.051s latency).
Not shown: 990 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit

PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
25/tcp  open  smtp
53/tcp  open  domain
80/tcp  open  http
110/tcp open  pop3
111/tcp open  rpcbind
143/tcp open  imap
993/tcp open  imaps
995/tcp open  pop3s

Nmap done: 1 IP address (1 host up) scanned in 4.94 seconds
```

Ya realizamos una transferencia de zona DNS durante nuestra recopilación inicial de información, lo que generó varios subdominios que analizaremos más a fondo más adelante. No vale la pena intentar otros ataques DNS en nuestro entorno actual.

***

## <mark style="color:purple;">FTP (21/tcp)</mark>

El objetivo es vulnerable a login ftp anónimo, permitiéndonos acceder cómo el usuario `anonymous` sin contraseña y descargar archivos de su interior.

```bash
afsh4ck@kali$ ftp trilocor.local     
                                    
Connected to trilocor.local.
220 (vsFTPd 3.0.3)
Name (tricolor.local:kali): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||47300|)
ftp: Can't connect to `10.129.151.166:47300': Expiró el tiempo de conexión
200 EPRT command successful. Consider using EPSV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0               1 Oct 13  2022 Uninstaller.lnk
226 Directory send OK.
ftp> get Uninstaller.lnk
local: Uninstaller.lnk remote: Uninstaller.lnk
200 EPRT command successful. Consider using EPSV.
150 Opening BINARY mode data connection for Uninstaller.lnk (1 bytes).
100% |********************************|     1        4.30 KiB/s    00:00 ETA
226 Transfer complete.
1 byte received in 00:00 (0.02 KiB/s)
ftp> 
```

Solamente encontramos el archivo `Uninstaller.lnk` que no contiene ningún dato relevante y tampoco podemos subir archivos:

```bash
ftp> put test.txt 
local: test.txt remote: test.txt
229 Entering Extended Passive Mode (|||41423|)
200 EPRT command successful. Consider using EPSV.
550 Permission denied.
```

Añadiremos el hallazgo `Anonymous FTP Login Enabled` al informe.

***

## <mark style="color:purple;">SSH (22/tcp)</mark>

Probamos fuerza bruta contra el usuario root, pero no conseguimos acceder. Por el momento lo dejaremos hasta conseguir algún usuario o contraseña que nos permita el acceso.

```bash
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://10.129.151.166

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-12-14 17:13:29
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ssh://10.129.151.166:22/
```

***

## <mark style="color:purple;">SMTP (25/tcp)</mark>

Al conectarnos con netcat vemos que nos dice que está abierto:

```bash
nc -nv 10.129.151.166 25

(UNKNOWN) [10.129.151.166] 25 (smtp) open
220 WEB-DMZ01 ESMTP Postfix (Ubuntu)
```

Probamos que VRFY funciona:

```bash
telnet 10.129.151.166 25
Trying 10.129.151.166...
Connected to 10.129.151.166.
Escape character is '^]'.
220 WEB-DMZ01 ESMTP Postfix (Ubuntu)
VRFY root
252 2.0.0 root
```

Con swaks comprobamos que no tiene relé abierto:

```bash
swaks --to test@tricolor.local --from spoof@external.com --server 10.129.151.166

=== Trying 10.129.151.166:25...
=== Connected to 10.129.151.166.
<-  220 WEB-DMZ01 ESMTP Postfix (Ubuntu)
 -> EHLO kali
<-  250-WEB-DMZ01
<-  250-PIPELINING
<-  250-SIZE 10240000
<-  250-VRFY
<-  250-ETRN
<-  250-STARTTLS
<-  250-ENHANCEDSTATUSCODES
<-  250-8BITMIME
<-  250-DSN
<-  250-SMTPUTF8
<-  250 CHUNKING
 -> MAIL FROM:<spoof@external.com>
<-  250 2.1.0 Ok
 -> RCPT TO:<test@tricolor.local>
<** 454 4.7.1 <test@tricolor.local>: Relay access denied
 -> QUIT
<-  221 2.0.0 Bye
=== Connection closed with remote host.
```

### Enumeración de usuarios SMTP

Podemos usar un módulo de Metasploit para enumerar usuarios SMTP:

```bash
msf6 auxiliary(scanner/smtp/smtp_enum) > run
[*] 10.129.114.240:25     - 10.129.114.240:25 Banner: 220 WEB-DMZ01 ESMTP Postfix (Ubuntu)
[+] 10.129.114.240:25     - 10.129.114.240:25 Users found: , _apt, backup, bin, daemon, dnsmasq, ftp, games, gnats, irc, landscape, list, lp, lxd, mail, man, messagebus, news, nobody, pollinate, postfix, postmaster, proxy, sshd, sync, sys, syslog, systemd-coredump, systemd-network, systemd-resolve, systemd-timesync, tcpdump, tss, usbmux, uucp, uuidd, www-data
[*] 10.129.114.240:25     - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

El servidor SMTP **NO acepta RCPT TO** para esos usuarios (lo cual es bueno para seguridad)  y **NO tiene autenticación habilitada** (Error 503: "authentication not enabled"):

```bash
(
echo "EHLO test.com"
sleep 1
echo "AUTH LOGIN"
sleep 1
echo "QUIT"
) | nc 10.129.151.166 25

220 WEB-DMZ01 ESMTP Postfix (Ubuntu)
250-WEB-DMZ01
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-STARTTLS
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING
503 5.5.1 Error: authentication not enabled
221 2.0.0 Bye
```

Esto significa que:

1. **No podemos enviar correos** a esos usuarios vía SMTP
2. **No podemos hacer fuerza bruta** de autenticación SMTP
3. Pero **VRFY confirma que los usuarios existen** en el sistema

En este caso, un callejón sin salida. Sigamos.

***

## <mark style="color:purple;">POP3 / IMAP / POP3S / IMAPS (110,143,993,995)</mark>

{% content-ref url="/pages/FFaP3OeX4RJRMgzEU9cv" %}
[IMAP/POP3](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion/imap-pop3.md)
{% endcontent-ref %}

```bash
# POP3 banner grab
nc 10.129.151.166 110
+OK Dovecot (Ubuntu) ready.

# IMAP banner grab
nc 10.129.151.166 143
* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ STARTTLS LOGINDISABLED] Dovecot (Ubuntu) ready.

# Enumeración con nmap
nmap --script pop3-capabilities,imap-capabilities -p 110,143,993,995 10.129.151.166
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-14 17:44 CST
Nmap scan report for tricolor.local (10.129.151.166)
Host is up (0.044s latency).

PORT    STATE SERVICE
110/tcp open  pop3
|_pop3-capabilities: TOP RESP-CODES UIDL CAPA SASL STLS PIPELINING AUTH-RESP-CODE
143/tcp open  imap
|_imap-capabilities: more capabilities IDLE LOGIN-REFERRALS ENABLE LOGINDISABLEDA0001 listed OK have ID SASL-IR STARTTLS Pre-login IMAP4rev1 post-login LITERAL+
993/tcp open  imaps
|_imap-capabilities: more IDLE LOGIN-REFERRALS capabilities ENABLE listed AUTH=PLAINA0001 have ID SASL-IR OK Pre-login IMAP4rev1 post-login LITERAL+
995/tcp open  pop3s
|_pop3-capabilities: TOP RESP-CODES UIDL CAPA SASL(PLAIN) USER PIPELINING AUTH-RESP-CODE

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds
```

Comprobamos que podemos conectarnos, pero no tenemos usuario ni contraseña, por lo que no podríamos acceder a correos corporativos:

```bash
openssl s_client -connect 10.129.151.166:imaps

Connecting to 10.129.151.166
CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 CN=ubuntu
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN=ubuntu
verify return:1
---
Certificate chain
 0 s:CN=ubuntu
   i:CN=ubuntu
   a:PKEY: RSA, 2048 (bit); sigalg: sha256WithRSAEncryption
   v:NotBefore: Oct 13 17:49:27 2022 GMT; NotAfter: Oct 10 17:49:27 2032 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIC0DCCAbigAwIBAgIUHxWTyQw4+99AJLbtv4kAioCf/S4wDQYJKoZIhvcNAQEL
BQAwETEPMA0GA1UEAwwGdWJ1bnR1MB4XDTIyMTAxMzE3NDkyN1oXDTMyMTAxMDE3
NDkyN1owETEPMA0GA1UEAwwGdWJ1bnR1MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
MIIBCgKCAQEA00Hy0hXS+OiplScXZrhOJU6Z07WtJ5RuzNVau02ZAoFiOEnQWClP
MOpARDDb48dL6Pimo8cmSODGwMW9Se9rOzyTQMHUP9zqjM5UvHcr/Gty0bdJGtiF
nq9/VTi3zh0Uiy0OQCEduNbysJLkZ+XlltfsgGmvQk2PF+/tCuFwb92j4KX0INrC
+hg4C1gdN0480Rcv1UDW+no8EZZXKWqdEL8E8+5U3moHqhcB3pfLr3ossNx+8uuB
Fx7OXHeGYIxnmq0CqyfNGUTeB6pbRLvuK4tzrYd/Pkj5j90JEWmy9jL7kgd6fbFf
9UlIQryYaHyH+9zEX+T85qr5TPU+0aefZQIDAQABoyAwHjAJBgNVHRMEAjAAMBEG
A1UdEQQKMAiCBnVidW50dTANBgkqhkiG9w0BAQsFAAOCAQEAcSL0WE+kK0pe7IxF
lzMtETDsDTVkJUHa7jI9twevy7YLe3J4ZrLnAVmyRsRDtRZ0kwZc+UCSeKB8GTrV
O0Zf85b0+QQ534H1SgxaijJQZNe8eRF5Pj0lrwodQbNa7cMqSoLIeyU9JTTZJZja
3ZL6YLfDg32xQkiBEpTd1XkZKyiFGf6VaGvhq9PDOqMx6v7ieLe26dq8j/pKH+NS
VDi4BF401Nd2K6/MaAB2jnBcAHbSGWjhx1aGjqitUWcHDrVhY8Cy/Yq5Bgdl8DY6
7hwsmuSY6LLNwJHu+91bunnsw2qOPYdCVjgirxNK6pwUUDMQU4bmdoqlUryH654Q
Nwxv3w==
-----END CERTIFICATE-----
subject=CN=ubuntu
issuer=CN=ubuntu
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: rsa_pss_rsae_sha256
Peer Temp Key: X25519, 253 bits
---
SSL handshake has read 1280 bytes and written 1740 bytes
Verification error: self-signed certificate
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Protocol: TLSv1.3
Server public key is 2048 bit
This TLS version forbids renegotiation.
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 18 (self-signed certificate)
---
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 4CB860ACC10FE83C5B3DC4F606E299E1B3EDF5ED44F16FCE158FEB16AF94CC8E
    Session-ID-ctx: 
    Resumption PSK: 79061EFA0E7DC5741FAEBFC8BC2CAB05C146FB91711A5EEAC1480F6B15AC22F912ED55F6E4BF24FD5DA3CEC8F7335A21
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 67 56 3d aa 1d 52 2c bf-03 7e 4a 85 28 0f f7 b1   gV=..R,..~J.(...
    0010 - 0a 8f 1e 8a bd a4 23 c1-56 ef e9 24 81 da b8 f8   ......#.V..$....
    0020 - f9 86 85 4d 99 d8 ff 35-e0 58 c4 7f 4b 52 ff eb   ...M...5.X..KR..
    0030 - 1b 6d 9f 88 4b 9a 8f 93-1a 49 5f 31 04 d8 c6 0e   .m..K....I_1....
    0040 - c0 01 ae 2e 11 74 73 be-e9 5f dc e9 6f e6 f2 7c   .....ts.._..o..|
    0050 - c0 63 6c c4 87 56 c4 42-3f 16 e6 15 49 d9 fe 28   .cl..V.B?...I..(
    0060 - 5e 1b d0 81 d0 42 d8 48-f8 85 03 0e e9 10 5c a4   ^....B.H......\.
    0070 - 46 b3 05 a2 cb 01 a0 a0-91 99 e0 9a 0c 57 b7 91   F............W..
    0080 - a6 f0 92 d6 4c 8b c2 7c-30 50 1b c9 36 49 59 28   ....L..|0P..6IY(
    0090 - cb c7 de 4e 45 cb 40 5e-11 bd b0 bc ac 8c 50 ca   ...NE.@^......P.
    00a0 - e1 10 ba ff 46 0f 95 ae-6a de 35 93 8f d8 46 bb   ....F...j.5...F.
    00b0 - 95 c4 8b 9b c8 73 70 dd-15 fe dd c1 38 a8 eb f6   .....sp.....8...

    Start Time: 1765705562
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 1A9B4EA58A7332A0BCA6128A12FB565B33C4DC0CF2C8037223113AD73ADE30F6
    Session-ID-ctx: 
    Resumption PSK: 4688FB60034EAF5845EEB4C27FA7B8250435D6967F0D6EF0ADFC6FBA4A5467BDB006713E10F13E1FF567ABA96CF818B7
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 67 56 3d aa 1d 52 2c bf-03 7e 4a 85 28 0f f7 b1   gV=..R,..~J.(...
    0010 - c1 10 bc a8 3a 32 6c 47-0b 69 54 66 90 d2 c8 97   ....:2lG.iTf....
    0020 - 1e bf c9 fc 08 98 91 0d-4e 2d 07 6e c7 0a f9 17   ........N-.n....
    0030 - 7d 57 3a eb 28 d8 25 76-c5 62 8b bf d0 5c 22 21   }W:.(.%v.b...\"!
    0040 - 4c 52 83 2c ff 86 97 59-b5 3e 26 a4 b9 9d 43 e1   LR.,...Y.>&...C.
    0050 - 5e 72 e4 67 9e fd a1 c1-7f 1f b0 48 80 a0 d4 41   ^r.g.......H...A
    0060 - a5 1c c9 12 4d a0 b1 22-7b ff 71 e9 2a b5 0e f0   ....M.."{.q.*...
    0070 - 40 50 ee 11 8f 09 e4 be-97 6f a4 c3 1e a5 ec d8   @P.......o......
    0080 - 06 87 16 d4 ac 3b 86 6a-54 63 6d f8 08 0e 9c 3e   .....;.jTcm....>
    0090 - 67 28 b5 37 7a 73 f9 61-d7 94 19 ba c4 4d 76 f1   g(.7zs.a.....Mv.
    00a0 - 08 68 d7 96 e3 a4 ac b4-2d 34 3b de 4b d8 46 03   .h......-4;.K.F.
    00b0 - 0f 08 b6 9e 54 c9 5c 6b-9e 02 2c 3e 26 6e 58 72   ....T.\k..,>&nXr

    Start Time: 1765705562
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ AUTH=PLAIN] Dovecot (Ubuntu) ready.
```

Tampoco encontramos ninguna community string:

```bash
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt 10.129.151.166
Scanning 1 hosts, 3219 communities
```

Y al intentar hacer alguna fuerza bruta para conseguir usuarios no conseguimos nada relevante:

```bash
nmap -p 143 --script imap-brute tricolor.local

Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-14 17:47 CST
Nmap scan report for tricolor.local (10.129.151.166)
Host is up (0.044s latency).

PORT    STATE SERVICE
143/tcp open  imap
| imap-brute: 
|   Accounts: No valid accounts found
|_  Statistics: Performed 50009 guesses in 129 seconds, average tps: 387.9

Nmap done: 1 IP address (1 host up) scanned in 129.46 seconds
```

Es un callejón sin salida. Continuemos.

***

## <mark style="color:purple;">RPCBind (111/tcp)</mark>

Tampoco tenemos NFS ni ningún servicio RPC interesante:

```bash
# Enumerar servicios RPC
rpcinfo -p 10.129.151.166
   program vers proto   port  service
    100000    4   tcp    111  portmapper
    100000    3   tcp    111  portmapper
    100000    2   tcp    111  portmapper
    100000    4   udp    111  portmapper
    100000    3   udp    111  portmapper
    100000    2   udp    111  portmapper

# Usar showmount si hay NFS
showmount -e 10.129.151.166
clnt_create: RPC: Program not registered
```

El servicio `rpcbind` no debería exponerse externamente, por lo que podríamos generar un hallazgo `Low`, `Unnecessary Exposed Services` o algo similar.

***

## <mark style="color:purple;">HTTP (80/tcp)</mark>

Entramos al servicio web para ver su contenido. A simple vista parece una empresa de robótica.

<figure><img src="/files/yyPEvAY215AwflYUQ2Ax" alt=""><figcaption></figcaption></figure>

No tenemos ninguna funcionalidad destacable, excepto en la página testimonials que hay un formulario:

<figure><img src="/files/5cQXu4Jutv3m0cye98Yg" alt=""><figcaption></figcaption></figure>

### Tecnología web

Con Whatweb descubrimos que es un Wordpress:

```bash
whatweb -v http://10.129.151.166

WhatWeb report for http://10.129.151.166
Status    : 200 OK
Title     : Trilocor &#8211; A cutting edge robotics company!
IP        : 10.129.151.166
Country   : RESERVED, ZZ

Summary   : Apache[2.4.41], Email[contact@info.com], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], JQuery[3.6.0], MetaGenerator[WordPress 5.8.3], PoweredBy[Trilocor], Script, WordPress[5.8.3]

Detected Plugins:
[ Apache ]
	The Apache HTTP Server Project is an effort to develop and 
	maintain an open-source HTTP server for modern operating 
	systems including UNIX and Windows NT. The goal of this 
	project is to provide a secure, efficient and extensible 
	server that provides HTTP services in sync with the current 
	HTTP standards. 

	Version      : 2.4.41 (from HTTP Server Header)
	Google Dorks: (3)
	Website     : http://httpd.apache.org/

[ Email ]
	Extract email addresses. Find valid email address and 
	syntactically invalid email addresses from mailto: link 
	tags. We match syntactically invalid links containing 
	mailto: to catch anti-spam email addresses, eg. bob at 
	gmail.com. This uses the simplified email regular 
	expression from 
	http://www.regular-expressions.info/email.html for valid 
	email address matching. 
	String       : contact@info.com

[ HTML5 ]
	HTML version 5, detected by the doctype declaration 

[ HTTPServer ]
	HTTP server header string. This plugin also attempts to 
	identify the operating system from the server header. 
	OS           : Ubuntu Linux
	String       : Apache/2.4.41 (Ubuntu) (from server string)

[ JQuery ]
	A fast, concise, JavaScript that simplifies how to traverse 
	HTML documents, handle events, perform animations, and add 
	AJAX. 
	Version      : 3.6.0
	Website     : http://jquery.com/

[ MetaGenerator ]
	This plugin identifies meta generator tags and extracts its 
	value. 
	String       : WordPress 5.8.3

[ PoweredBy ]
	This plugin identifies instances of 'Powered by x' text and 
	attempts to extract the value for x. 
	String       : Trilocor

[ Script ]
	This plugin detects instances of script HTML elements and 
	returns the script language/type. 

[ WordPress ]
	WordPress is an opensource blogging system commonly used as 
	a CMS. 
	Version      : 5.8.3
	Aggressive function available (check plugin file or details).
	Google Dorks: (1)
	Website     : http://www.wordpress.org/

HTTP Headers:
	HTTP/1.1 200 OK
	Date: Sun, 14 Dec 2025 09:26:05 GMT
	Server: Apache/2.4.41 (Ubuntu)
	Vary: Accept-Encoding
	Content-Encoding: gzip
	Content-Length: 23972
	Connection: close
	Content-Type: text/html; charset=UTF-8
```

Encontramos la versión `5.8.3`, que nos permitiría buscar algún exploit público. También encontramos el plugin de MetaGenerator en la misma versión.

Intentaremos explotar esto en la siguiente sección.

### Análisis de vulnerabilidades

```bash
nuclei -u http://tricolor.local
```

<figure><img src="/files/qbYnORvf3hK3TOcuaDHY" alt=""><figcaption></figcaption></figure>

Encontramos solo dos vulnerabilidades marcadas como "medium" por Nuclei:

```bash
[CVE-2023-48795] [javascript] [medium] tricolor.local:22 ["Vulnerable to Terrapin"]
[ftp-anonymous-login] [tcp] [medium] tricolor.local:21
```

Ya explotamos el FTP Login Anonymous. El CVE-2023-48795 permite a un atacante (en posición MitM) eliminar o modificar mensajes al inicio de la conexión SSH, por lo que en principio no nos interesa ya que no es una vulnerabilidad para ganar acceso.

***

## <mark style="color:purple;">Análisis post-enumeración</mark>

En este punto, analizaremos todos los subdominios descubiertos y la web principal para acceder a la `DMZ01`
