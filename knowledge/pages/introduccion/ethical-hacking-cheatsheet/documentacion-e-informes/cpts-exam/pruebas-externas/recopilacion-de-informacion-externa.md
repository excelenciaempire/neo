
# Recopilación de información externa

## <mark style="color:purple;">Enumeración externa</mark>

Comenzamos con un escaneo inicial rápido de Nmap contra nuestro objetivo para familiarizarnos con el entorno y ver con qué nos enfrentamos. Nos aseguramos de guardar todos los resultados del escaneo en el subdirectorio correspondiente del directorio de nuestro proyecto.

<table data-full-width="false"><thead><tr><th>Pruebas externas</th></tr></thead><tbody><tr><td><code>10.129.101.0/24</code> - Red externa</td></tr><tr><td><code>*.trilocor.local</code> - Todos los subdominios</td></tr></tbody></table>

#### etc/hosts

```bash
sudo echo "10.129.101.37 trilocor.local" | sudo tee -a /etc/hosts
```

## <mark style="color:purple;">Escaneo de puertos y servicios</mark>

#### Escaneo simple de servicios

<pre class="language-bash"><code class="lang-bash"><strong>afsh4ck@kali$ sudo nmap --open -oA trilocor_scan trilocor.local
</strong>
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-14 16:27 CST
Nmap scan report for tricolor.local (10.129.151.166)
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
</code></pre>

#### Escaneo completo

```bash
sudo nmap -v -p- --open -A -oA trilocor_svc trilocor.local

Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-14 16:28 CST
NSE: Loaded 157 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 16:28
<SNIP>
PORT    STATE SERVICE  VERSION
21/tcp  open  ftp      vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.14.17
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 71:08:b0:c4:f3:ca:97:57:64:97:70:f9:fe:c5:0c:7b (RSA)
|   256 45:c3:b5:14:63:99:3d:9e:b3:22:51:e5:97:76:e1:50 (ECDSA)
|_  256 2e:c2:41:66:46:ef:b6:81:95:d5:aa:35:23:94:55:38 (ED25519)
25/tcp  open  smtp     Postfix smtpd
|_smtp-commands: WEB-DMZ01, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING
53/tcp  open  domain   (unknown banner: BIND 9)
| dns-nsid: 
|_  bind.version: BIND 9
| fingerprint-strings: 
|   DNSVersionBindReqTCP: 
|     version
|     bind
|_    BIND 9
80/tcp  open  http     Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-generator: WordPress 5.8.3
|_http-title: Trilocor &#8211; A cutting edge robotics company!
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
110/tcp open  pop3     Dovecot pop3d
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Issuer: commonName=ubuntu
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2022-10-13T17:49:27
| Not valid after:  2032-10-10T17:49:27
| MD5:   aad6:9528:3d9a:18ea:8dd5:8de2:c927:6b66
|_SHA-1: 7765:8cb3:93f3:9ca1:1efe:a8cf:63a7:b450:1d43:6a7a
|_ssl-date: TLS randomness does not represent time
|_pop3-capabilities: TOP SASL AUTH-RESP-CODE CAPA RESP-CODES STLS UIDL PIPELINING
111/tcp open  rpcbind  2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|_  100000  3,4          111/udp6  rpcbind
143/tcp open  imap     Dovecot imapd (Ubuntu)
|_imap-capabilities: have SASL-IR LITERAL+ Pre-login more IMAP4rev1 listed OK ID STARTTLS post-login IDLE ENABLE capabilities LOGINDISABLEDA0001 LOGIN-REFERRALS
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Issuer: commonName=ubuntu
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2022-10-13T17:49:27
| Not valid after:  2032-10-10T17:49:27
| MD5:   aad6:9528:3d9a:18ea:8dd5:8de2:c927:6b66
|_SHA-1: 7765:8cb3:93f3:9ca1:1efe:a8cf:63a7:b450:1d43:6a7a
|_ssl-date: TLS randomness does not represent time
993/tcp open  ssl/imap Dovecot imapd (Ubuntu)
|_imap-capabilities: have SASL-IR LITERAL+ more IMAP4rev1 listed OK ID Pre-login post-login IDLE ENABLE capabilities AUTH=PLAINA0001 LOGIN-REFERRALS
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Issuer: commonName=ubuntu
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2022-10-13T17:49:27
| Not valid after:  2032-10-10T17:49:27
| MD5:   aad6:9528:3d9a:18ea:8dd5:8de2:c927:6b66
|_SHA-1: 7765:8cb3:93f3:9ca1:1efe:a8cf:63a7:b450:1d43:6a7a
995/tcp open  ssl/pop3 Dovecot pop3d
|_ssl-date: TLS randomness does not represent time
|_pop3-capabilities: TOP USER AUTH-RESP-CODE CAPA RESP-CODES SASL(PLAIN) UIDL PIPELINING
| ssl-cert: Subject: commonName=ubuntu
| Subject Alternative Name: DNS:ubuntu
| Issuer: commonName=ubuntu
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2022-10-13T17:49:27
| Not valid after:  2032-10-10T17:49:27
| MD5:   aad6:9528:3d9a:18ea:8dd5:8de2:c927:6b66
|_SHA-1: 7765:8cb3:93f3:9ca1:1efe:a8cf:63a7:b450:1d43:6a7a
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.95%I=7%D=12/14%Time=693E75F7%P=x86_64-pc-linux-gnu%r(DNS
SF:VersionBindReqTCP,33,"\x001\0\x06\x85\0\0\x01\0\x01\0\0\0\0\x07version\
SF:x04bind\0\0\x10\0\x03\xc0\x0c\0\x10\0\x03\0\0\0\0\0\x07\x06BIND\x209");
```

#### Extraer servicios en ejecución

```bash
egrep -v "^#|Status: Up" tricolor_svc.gnmap | cut -d ' ' -f4- | tr ',' '\n' | \
sed -e 's/^[ \t]*//' | awk -F '/' '{print $7}' | grep -v "^$" | sort | uniq -c | sort -k 1 -nr
      
      2 Dovecot pop3d
      2 Dovecot imapd (Ubuntu)
      1 vsftpd 3.0.3
      1 (unknown banner: BIND 9)
      1 Postfix smtpd
      1 OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
      1 Apache httpd 2.4.41 ((Ubuntu))
      1 2-4 (RPC #100000)
```

#### Escaneo SYN de red externa

Esto nos saca todos los hosts "vivos" en la red con su dirección IP:

```bash
fping -a -g 10.129.151.1 10.129.151.244
                    
10.129.151.166
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.26
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.26
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.59
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.59
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.59
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.26
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.95
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.165
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.215
ICMP Host Unreachable from 10.10.14.1 for ICMP Echo sent to 10.129.151.124
```

Solamente tenemos el host `DMZ01` activo en la red

## <mark style="color:purple;">Enumeración de subdominios</mark>

#### Con DIG

Probamos una transferencia de zona y obtenemos algunos subdominios:

{% hint style="success" %}
Añadir `DNS Zone Transfer Enabled` al informe
{% endhint %}

```bash
dig axfr trilocor.local @10.129.101.37 

; <<>> DiG 9.20.9-1-Debian <<>> axfr trilocor.local @10.129.101.37
;; global options: +cmd
trilocor.local.		86400	IN	SOA	ns1.trilocor.local. dnsadmin.trilocor.local. 21 604800 86400 2419200 86400
trilocor.local.		86400	IN	NS	trilocor.local.
trilocor.local.		86400	IN	A	127.0.0.1
blog.trilocor.local.	86400	IN	A	127.0.0.1
dev.trilocor.local.	86400	IN	A	127.0.0.1
jobs.trilocor.local.	86400	IN	A	127.0.0.1
news.trilocor.local.	86400	IN	A	127.0.0.1
nms.trilocor.local.	86400	IN	A	127.0.0.1
selfservicestg.trilocor.local. 86400 IN	A	127.0.0.1
shop.trilocor.local.	86400	IN	A	127.0.0.1
trilocor.local.		86400	IN	SOA	ns1.trilocor.local. dnsadmin.trilocor.local. 21 604800 86400 2419200 86400
;; Query time: 36 msec
;; SERVER: 10.129.101.37#53(10.129.101.37) (TCP)
;; WHEN: Mon Dec 15 19:53:49 CST 2025
;; XFR size: 11 records (messages 1, bytes 341)
```

Hemos descubierto:

1. **blog.trilocor.local** - Blog corporativo
2. **dev.trilocor.local** - Desarrollo/Testing
3. **jobs.trilocor.local** - Portal de empleo
4. **news.trilocor.local** - Noticias corporativas
5. **nms.trilocor.local** - Network Management System (¡Interesante!)
6. **selfservicestg.trilocor.local** - Self-service staging
7. **shop.trilocor.local** - Tienda online

## <mark style="color:purple;">Enumeración de Vhosts</mark>

Al enumerar vhosts con ffuf encontramos alguno extra que no habíamos descubierto, como `hrportal.trilocor.local`, lo que lo convierte en un objetivo valioso o mejor securizado, y posiblemente la vía de acceso a la DMZ:

```bash
ffuf -u "http://trilocor.local/" -H "Host: FUZZ.trilocor.local" -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -fs 251273

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://trilocor.local/
 :: Wordlist         : FUZZ: /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt
 :: Header           : Host: FUZZ.trilocor.local
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 251273
________________________________________________

news                    [Status: 200, Size: 21033, Words: 11361, Lines: 300, Duration: 136ms]
jobs                    [Status: 200, Size: 3661, Words: 1025, Lines: 82, Duration: 154ms]
blog                    [Status: 302, Size: 314, Words: 60, Lines: 12, Duration: 2607ms]
nms                     [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 968ms]
shop                    [Status: 200, Size: 13057, Words: 5397, Lines: 301, Duration: 4582ms]
dev                     [Status: 200, Size: 10918, Words: 3499, Lines: 376, Duration: 4589ms]
hrportal                [Status: 200, Size: 2423, Words: 873, Lines: 59, Duration: 347ms]
:: Progress: [114442/114442] :: Job [1/1] :: 113 req/sec :: Duration: [0:14:09] :: Errors: 0 ::
```

Crearemos una lista de `valid_subdomains.txt` y los añadiremos al `/etc/hosts` para analizarlos:

```
blog.trilocor.local
dev.trilocor.local
jobs.trilocor.local
news.trilocor.local
nms.trilocor.local
selfservicestg.trilocor.local
shop.trilocor.local
hrportal.trilocor.local
```

## <mark style="color:purple;">Hacia delante</mark>

Ahora que tenemos esta información, procederemos con la explotación de servicios.
