
# Report Template

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.11` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.11 board.htb" | sudo tee -a /etc/hosts
```

<figure><img src="/files/GiV22TR8UH668FEdpz4I" alt=""><figcaption></figcaption></figure>

Parece una web de servicios de ciberseguridad.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -sCV -T5 10.10.11.11
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 06:2d:3b:85:10:59:ff:73:66:27:7f:0e:ae:03:ea:f4 (RSA)
|   256 59:03:dc:52:87:3a:35:99:34:44:74:33:78:31:35:fb (ECDSA)
|_  256 ab:13:38:e4:3e:e0:24:b4:69:38:a9:63:82:38:dd:f4 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos 2 puertos abiertos, el 22 y el 80, los típicos.

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch nos encontramos unos pocos directorios:

```bash
dirsearch -u http://permx.htb -x 300,301,302,400,403,404,503

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/freelancer/reports/http_permx.htb/_24-08-13_00-03-19.txt

Target: http://permx.htb/

[00:03:19] Starting: 
[00:03:25] 200 -    3KB - /404.html
[00:03:26] 200 -    4KB - /about.html
[00:03:38] 200 -    3KB - /contact.html
[00:03:47] 200 -  448B  - /js/
[00:03:48] 200 -  491B  - /lib/
[00:03:48] 200 -  649B  - /LICENSE.txt
```

Revisando los directorios no encontramos nada relevante.

## <mark style="color:purple;">Enumeración de Vhosts</mark>

En este momento puede parecer que no podemos hacer nada, pero vamos a usar ffuf para enumerar subdominios dentro de este host:

```bash
ffuf -u http://board.htb -H "Host:FUZZ.board.htb" -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt:FUZZ -fw 12

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://board.htb
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
 :: Header           : Host: FUZZ.board.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 12
________________________________________________

web                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 64ms]
m                       [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 65ms]
mail1                   [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 65ms]
gw                      [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 66ms]
dev                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 87ms]
secure                  [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 86ms]
mail2                   [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
ww1                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
ww42                    [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 87ms]
owa                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
server                  [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
webmail                 [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
crm                     [Status: 200, Size: 6360, Words: 397, Lines: 150, Duration: 98ms]
```

Observamos que hay un subdominio crm con un tamaño de respuesta diferente al resto, por lo que seguramente sea válido.&#x20;

## <mark style="color:purple;">Búsqueda de exploits</mark>

Haciendo un poco de research nos encontramos este exploit que nos podría servir:

## <mark style="color:purple;">Explotación</mark>

## <mark style="color:purple;">Conexión a base de datos</mark>

## <mark style="color:purple;">User flag</mark>

## <mark style="color:purple;">Escalada de privilegios</mark>
