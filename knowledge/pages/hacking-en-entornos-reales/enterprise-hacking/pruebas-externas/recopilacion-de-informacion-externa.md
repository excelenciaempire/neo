
# Recopilación de Información Externa

## <mark style="color:purple;">Escaneo de puertos</mark>

Comenzamos con un escaneo inicial rápido de Nmap contra nuestro objetivo para familiarizarnos con el entorno y ver con qué nos enfrentamos. Nos aseguramos de guardar todos los resultados del escaneo en el subdirectorio correspondiente del directorio de nuestro proyecto.

```shell-session
afsh4ck@kali$ sudo nmap --open -oA inlanefreight_ept_tcp_1k -iL scope 

Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-20 14:56 EDT
Nmap scan report for 10.129.203.101
Host is up (0.12s latency).
Not shown: 989 closed tcp ports (reset)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
25/tcp   open  smtp
53/tcp   open  domain
80/tcp   open  http
110/tcp  open  pop3
111/tcp  open  rpcbind
143/tcp  open  imap
993/tcp  open  imaps
995/tcp  open  pop3s
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 2.25 seconds
```

Observamos 11 puertos abiertos en nuestro análisis rápido de los 1000 puertos TCP principales. Parece que se trata de un servidor web que también ejecuta servicios adicionales como FTP, SSH, correo electrónico (SMTP, POP3 e IMAP), DNS y al menos dos puertos relacionados con aplicaciones web.

## <mark style="color:purple;">Escaneo completo</mark>

Mientras tanto, hemos estado ejecutando un escaneo completo de puertos con la opción  `-A`"[escaneo agresivo](https://nmap.org/book/man-misc-options.html) " para realizar enumeraciones adicionales, incluyendo la detección del sistema operativo, el escaneo de versiones y el escaneo de scripts. Ten en cuenta que este escaneo es más intrusivo que ejecutarlo con la opción `-sV` "Escaneo de versiones", y debemos asegurarnos de que los scripts que se ejecuten con el escaneo de scripts no causen problemas.

```shell-session
afsh4ck@kali$ sudo nmap --open -p- -A -oA inlanefreight_ept_tcp_all_svc -iL scope

Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-20 15:27 EDT
Nmap scan report for 10.129.203.101
Host is up (0.12s latency).
Not shown: 65524 closed tcp ports (reset)
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              38 May 30 17:16 flag.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.14.15
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 71:08:b0:c4:f3:ca:97:57:64:97:70:f9:fe:c5:0c:7b (RSA)
|   256 45:c3:b5:14:63:99:3d:9e:b3:22:51:e5:97:76:e1:50 (ECDSA)
|_  256 2e:c2:41:66:46:ef:b6:81:95:d5:aa:35:23:94:55:38 (ED25519)
25/tcp   open  smtp     Postfix smtpd
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Not valid before: 2022-05-30T17:15:40
|_Not valid after:  2032-05-27T17:15:40
|_smtp-commands: ubuntu, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING
53/tcp   open  domain   
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|     bind
| dns-nsid: 
|_  bind.version: 
80/tcp   open  http     Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Inlanefreight
110/tcp  open  pop3     Dovecot pop3d
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Not valid before: 2022-05-30T17:15:40
|_Not valid after:  2032-05-27T17:15:40
|_pop3-capabilities: SASL TOP PIPELINING STLS RESP-CODES AUTH-RESP-CODE CAPA UIDL
111/tcp  open  rpcbind  2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|_  100000  3,4          111/udp6  rpcbind
143/tcp  open  imap     Dovecot imapd (Ubuntu)
|_imap-capabilities: LITERAL+ LOGIN-REFERRALS more Pre-login post-login ID capabilities listed have LOGINDISABLEDA0001 OK ENABLE IDLE STARTTLS SASL-IR IMAP4rev1
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Not valid before: 2022-05-30T17:15:40
|_Not valid after:  2032-05-27T17:15:40
993/tcp  open  ssl/imap Dovecot imapd (Ubuntu)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Not valid before: 2022-05-30T17:15:40
|_Not valid after:  2032-05-27T17:15:40
|_imap-capabilities: LITERAL+ LOGIN-REFERRALS AUTH=PLAINA0001 post-login ID capabilities more have listed OK ENABLE IDLE Pre-login SASL-IR IMAP4rev1
995/tcp  open  ssl/pop3 Dovecot pop3d
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Not valid before: 2022-05-30T17:15:40
|_Not valid after:  2032-05-27T17:15:40
|_ssl-date: TLS randomness does not represent time
|_pop3-capabilities: SASL(PLAIN) TOP PIPELINING CAPA RESP-CODES AUTH-RESP-CODE USER UIDL
8080/tcp open  http     Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported:CONNECTION
|_http-title: Support Center
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.92%I=7%D=6/20%Time=62B0CA68%P=x86_64-pc-linux-gnu%r(DNSV
SF:ersionBindReqTCP,39,"\x007\0\x06\x85\0\0\x01\0\x01\0\0\0\0\x07version\x
SF:04bind\0\0\x10\0\x03\xc0\x0c\0\x10\0\x03\0\0\0\0\0\r\x0c");
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.92%E=4%D=6/20%OT=21%CT=1%CU=36505%PV=Y%DS=2%DC=T%G=Y%TM=62B0CA8
OS:8%P=x86_64-pc-linux-gnu)SEQ(SP=104%GCD=1%ISR=10B%TI=Z%CI=Z%II=I%TS=A)OPS
OS:(O1=M505ST11NW7%O2=M505ST11NW7%O3=M505NNT11NW7%O4=M505ST11NW7%O5=M505ST1
OS:1NW7%O6=M505ST11)WIN(W1=FE88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W6=FE88)ECN
OS:(R=Y%DF=Y%T=40%W=FAF0%O=M505NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=A
OS:S%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R
OS:=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F
OS:=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%
OS:T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD
OS:=S)

Network Distance: 2 hops
Service Info: Host:  ubuntu; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 443/tcp)
HOP RTT       ADDRESS
1   116.63 ms 10.10.14.1
2   117.72 ms 10.129.203.101

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 84.91 seconds
```

Lo primero que podemos ver es que se trata de un host Ubuntu que ejecuta algún tipo de proxy HTTP. Podemos usar esta práctica [hoja de trucos](https://github.com/leonjza/awesome-nmap-grep) de Nmap grep para simplificar el análisis y extraer la información más útil. Extraigamos los servicios en ejecución y sus números para tenerlos a mano para una investigación más profunda.

```shell-session
afsh4ck@kali$ egrep -v "^#|Status: Up" inlanefreight_ept_tcp_all_svc.gnmap | cut -d ' ' -f4- | tr ',' '\n' | \                                                               
sed -e 's/^[ \t]*//' | awk -F '/' '{print $7}' | grep -v "^$" | sort | uniq -c \
| sort -k 1 -nr

      2 Dovecot pop3d
      2 Dovecot imapd (Ubuntu)
      2 Apache httpd 2.4.41 ((Ubuntu))
      1 vsftpd 3.0.3
      1 Postfix smtpd
      1 OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
      1 2-4 (RPC #100000)
```

## <mark style="color:purple;">Transferencia de zona</mark>

Desde estos servicios de escucha, podemos probar varias cosas de inmediato, pero como vemos que el DNS está presente, probaremos una transferencia de zona DNS para ver si podemos enumerar subdominios válidos para una mayor exploración y ampliar el alcance de nuestras pruebas. Sabemos, por la hoja de alcance, que el dominio principal es \[nombre del dominio] `INLANEFREIGHT.LOCAL`, así que veamos qué podemos encontrar.

```shell-session
afsh4ck@kali$ dig axfr inlanefreight.local @10.129.203.101

; <<>> DiG 9.16.27-Debian <<>> axfr inlanefreight.local @10.129.203.101
;; global options: +cmd
inlanefreight.local.	86400	IN	SOA	ns1.inlanfreight.local. dnsadmin.inlanefreight.local. 21 604800 86400 2419200 86400
inlanefreight.local.	86400	IN	NS	inlanefreight.local.
inlanefreight.local.	86400	IN	A	127.0.0.1
blog.inlanefreight.local. 86400	IN	A	127.0.0.1
careers.inlanefreight.local. 86400 IN	A	127.0.0.1
dev.inlanefreight.local. 86400	IN	A	127.0.0.1
gitlab.inlanefreight.local. 86400 IN	A	127.0.0.1
ir.inlanefreight.local.	86400	IN	A	127.0.0.1
status.inlanefreight.local. 86400 IN	A	127.0.0.1
support.inlanefreight.local. 86400 IN	A	127.0.0.1
tracking.inlanefreight.local. 86400 IN	A	127.0.0.1
vpn.inlanefreight.local. 86400	IN	A	127.0.0.1
inlanefreight.local.	86400	IN	SOA	ns1.inlanfreight.local. dnsadmin.inlanefreight.local. 21 604800 86400 2419200 86400
;; Query time: 116 msec
;; SERVER: 10.129.203.101#53(10.129.203.101)
;; WHEN: Mon Jun 20 16:28:20 EDT 2022
;; XFR size: 14 records (messages 1, bytes 448)
```

La transferencia de zona funciona y encontramos 9 subdominios adicionales. En una situación real, si no es posible realizar una transferencia de zona DNS, podríamos enumerar los subdominios de diversas maneras. El sitio web [DNSDumpster.com](https://dnsdumpster.com/) es una buena opción. El módulo [`Recopilación de Información`](/ethical-hacking-cheatsheet/recopilacion-de-informacion/google-hacking.md) enumera varios métodos para la enumeración[ pasiva](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-pasiva/subdominios-pasiva.md) y [activa de subdominios](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-activa/subdominios-activa.md) .

## <mark style="color:purple;">Enumeración de vhosts</mark>

Si el DNS no estuviera en juego, también podríamos realizar una enumeración de vhost con una herramienta como `ffuf`. Probémosla aquí para ver si encontramos algo más que la transferencia de zona no haya detectado. Usaremos [esta](https://github.com/danielmiessler/SecLists/blob/master/Discovery/DNS/namelist.txt) wordlist para la enumeración, que se encuentra en la ruta `/usr/share/Seclists/Discovery/DNS/namelist.txt` en Kali Linux.

Para fuzzear vhosts, primero debemos determinar cómo se ve la respuesta para un vhost inexistente. Podemos elegir lo que queramos; solo queremos provocar una respuesta, así que deberíamos elegir algo que muy probablemente no exista.

```shell-session
afsh4ck@kali$ curl -s -I http://10.129.203.101 -H "HOST: defnotvalid.inlanefreight.local" | grep "Content-Length:"

Content-Length: 15157
```

Al intentar especificar `defnotvalid` en el encabezado del host, obtenemos un tamaño de respuesta de `15157`. Podemos inferir que este será el mismo para cualquier vhost no válido, así que trabajaremos con `ffuf`, usando el indicador  `-fs` para filtrar las respuestas con tamaño, `15157`ya que sabemos que no son válidas.

```shell-session
afsh4ck@kali$ ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt -u http://10.129.48.123/ -H "Host: FUZZ.inlanefreight.local" -fs 15157


        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.48.123/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.inlanefreight.local
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 15157
________________________________________________

blog                    [Status: 200, Size: 8708, Words: 1509, Lines: 232, Duration: 416ms]
careers                 [Status: 200, Size: 51806, Words: 22041, Lines: 732, Duration: 114ms]
dev                     [Status: 200, Size: 2048, Words: 643, Lines: 74, Duration: 68ms]
gitlab                  [Status: 302, Size: 113, Words: 5, Lines: 1, Duration: 84ms]
ir                      [Status: 200, Size: 28548, Words: 2885, Lines: 210, Duration: 1460ms]
monitoring              [Status: 200, Size: 56, Words: 3, Lines: 4, Duration: 51ms]
status                  [Status: 200, Size: 878, Words: 105, Lines: 43, Duration: 48ms]
support                 [Status: 200, Size: 26635, Words: 11730, Lines: 523, Duration: 53ms]
tracking                [Status: 200, Size: 35211, Words: 10413, Lines: 791, Duration: 61ms]
vpn                     [Status: 200, Size: 1578, Words: 414, Lines: 35, Duration: 42ms]
```

Al comparar los resultados, vemos un vhost `monitoring` que no fue parte de los resultados de la transferencia de zona DNS que realizamos.

***

## <mark style="color:purple;">Resultados de la enumeración</mark>

En nuestra enumeración inicial, detectamos varios puertos interesantes abiertos que analizaremos con más detalle en la siguiente sección. También recopilamos varios subdominios/vhosts. Los añadiremos a nuestro archivo `/etc/hosts` para investigarlos en profundidad.

```shell-session
afsh4ck@kali$ sudo tee -a /etc/hosts > /dev/null <<EOT

## inlanefreight hosts 
10.129.203.101 inlanefreight.local blog.inlanefreight.local careers.inlanefreight.local dev.inlanefreight.local gitlab.inlanefreight.local ir.inlanefreight.local status.inlanefreight.local support.inlanefreight.local tracking.inlanefreight.local vpn.inlanefreight.local
EOT
```

En la siguiente sección, analizaremos más a fondo los resultados del análisis de Nmap y veremos si podemos encontrar algún servicio directamente explotable o mal configurado.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.48.123

vHosts necesarios para estas preguntas:
inlanefreight.local
```

### Pregunta 1

> Realiza una captura de banner de los servicios que escuchan en el host de destino y encuentre un banner de servicio no estándar. Envíe el nombre como respuesta (formato: palabra\_palabra\_palabra)

Añadimos `inlanefreight.local` a nuestro archivo `/etc/hosts`

#### Escaneo de puertos

```shell-session
afsh4ck@kali$ sudo nmap -v -sS -T5 -Pn 10.129.48.123
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times may be slower.
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-04 17:44 CEST
Nmap scan report for 10.129.48.123
Host is up (0.037s latency).
Not shown: 989 closed tcp ports (reset)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
25/tcp   open  smtp
53/tcp   open  domain
80/tcp   open  http
110/tcp  open  pop3
111/tcp  open  rpcbind
143/tcp  open  imap
993/tcp  open  imaps
995/tcp  open  pop3s
8080/tcp open  http-proxy
```

Tenemos 11 puertos abiertos. Vamos a enumerar los servicios.

#### Enumeración de servicios

```shell-session
afsh4ck@kali$ sudo nmap -sV -Pn 10.129.48.123

Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-04 17:48 CEST
Nmap scan report for inlanefreight.local (10.129.48.123)
Host is up (0.043s latency).
Not shown: 989 closed tcp ports (reset)
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 3.0.3
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
25/tcp   open  smtp     Postfix smtpd
53/tcp   open  domain   (unknown banner: 1337_HTB_DNS)
80/tcp   open  http     Apache httpd 2.4.41 ((Ubuntu))
110/tcp  open  pop3     Dovecot pop3d
111/tcp  open  rpcbind  2-4 (RPC #100000)
143/tcp  open  imap     Dovecot imapd (Ubuntu)
993/tcp  open  ssl/imap Dovecot imapd (Ubuntu)
995/tcp  open  ssl/pop3 Dovecot pop3d
8080/tcp open  http     Apache httpd 2.4.41 ((Ubuntu))
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.95%I=7%D=4/4%Time=67EFFF5A%P=x86_64-pc-linux-gnu%r(DNSVe
SF:rsionBindReqTCP,39,"\x007\0\x06\x85\0\0\x01\0\x01\0\0\0\0\x07version\x0
SF:4bind\0\0\x10\0\x03\xc0\x0c\0\x10\0\x03\0\0\0\0\0\r\x0c1337_HTB_DNS");
Service Info: Host:  ubuntu; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

#### **Banner no estándar detectado**

```txt
53/tcp   open  domain   (unknown banner: 1337_HTB_DNS)
```

Esto destaca **claramente** del resto de servicios. Es un banner **no estándar** en el servicio de DNS (puerto 53.

### Pregunta 2

> Realiza una transferencia de zona DNS contra el objetivo y encuentre una flag. Envíe el valor de la flag como respuesta.

```shell-session
afsh4ck@kali$ dig axfr inlanefreight.local @10.129.48.123

; <<>> DiG 9.20.4-4-Debian <<>> axfr inlanefreight.local @10.129.48.123
;; global options: +cmd
inlanefreight.local.	86400	IN	SOA	ns1.inlanfreight.local. dnsadmin.inlanefreight.local. 21 604800 86400 2419200 86400
inlanefreight.local.	86400	IN	NS	inlanefreight.local.
inlanefreight.local.	86400	IN	A	127.0.0.1
blog.inlanefreight.local. 86400	IN	A	127.0.0.1
careers.inlanefreight.local. 86400 IN	A	127.0.0.1
dev.inlanefreight.local. 86400	IN	A	127.0.0.1
flag.inlanefreight.local. 86400	IN	TXT	"HTB{DNs_ZOn3_Tr@nsf3r}"
gitlab.inlanefreight.local. 86400 IN	A	127.0.0.1
ir.inlanefreight.local.	86400	IN	A	127.0.0.1
status.inlanefreight.local. 86400 IN	A	127.0.0.1
support.inlanefreight.local. 86400 IN	A	127.0.0.1
tracking.inlanefreight.local. 86400 IN	A	127.0.0.1
vpn.inlanefreight.local. 86400	IN	A	127.0.0.1
inlanefreight.local.	86400	IN	SOA	ns1.inlanfreight.local. dnsadmin.inlanefreight.local. 21 604800 86400 2419200 86400
;; Query time: 31 msec
;; SERVER: 10.129.48.123#53(10.129.48.123) (TCP)
;; WHEN: Fri Apr 04 17:51:39 CEST 2025
;; XFR size: 14 records (messages 1, bytes 448)
```

Obtenemos la flag y el FQDN del servicio asociado:

```
flag.inlanefreight.local. 86400	IN	TXT	"HTB{DNs_ZOn3_Tr@nsf3r}"
```

### Pregunta 3

> Realiza la detección de vhost. ¿Qué vhost adicional existe? (una palabra)

Al realizar fuzzing de vhosts con fuff filtramos por la longitud 15157, ya que de otra manera obtenemos multitud de falsos positivos:

```shell-session
afsh4ck@kali$ ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt -u http://10.129.48.123/ -H "Host: FUZZ.inlanefreight.local" -fs 15157


        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.48.123/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.inlanefreight.local
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 15157
________________________________________________

blog                    [Status: 200, Size: 8708, Words: 1509, Lines: 232, Duration: 416ms]
careers                 [Status: 200, Size: 51806, Words: 22041, Lines: 732, Duration: 114ms]
dev                     [Status: 200, Size: 2048, Words: 643, Lines: 74, Duration: 68ms]
gitlab                  [Status: 302, Size: 113, Words: 5, Lines: 1, Duration: 84ms]
ir                      [Status: 200, Size: 28548, Words: 2885, Lines: 210, Duration: 1460ms]
monitoring              [Status: 200, Size: 56, Words: 3, Lines: 4, Duration: 51ms]
status                  [Status: 200, Size: 878, Words: 105, Lines: 43, Duration: 48ms]
support                 [Status: 200, Size: 26635, Words: 11730, Lines: 523, Duration: 53ms]
tracking                [Status: 200, Size: 35211, Words: 10413, Lines: 791, Duration: 61ms]
vpn                     [Status: 200, Size: 1578, Words: 414, Lines: 35, Duration: 42ms]
```

Encontramos varios vhosts, destacando un vhost que no  nos mostraba en la transferencia de zona:

* monitoring
