
# Report Template - Windows

<figure><img src="/files/hZMiyVkDAuu0CnV3Yxuj" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Despliegue de la máquina</mark>

```bash
sudo bash auto_deploy.sh library.tar

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2
```

## <mark style="color:purple;">Información General</mark>

* **IP:** `172.17.0.2`
* **Sistema operativo:** Linux
* **Dificultad:** 🟢 Fácil | 🟡 Media | 🔴 Difícil (seleccionar)
* **Fecha:** DD-MM-AAAA

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "172.17.0.2" | sudo tee -a /etc/hosts
```

### Acceso Web

Accedemos a `http://planning.htb` y observamos que parece ser una plataforma de cursos en línea.

<figure><img src="/files/i7yQwHwiDrUCEZlLguIu" alt=""><figcaption></figcaption></figure>

Comandos adicionales útiles:

```bash
host 172.17.0.2
dig 172.17.0.2
curl -I 172.17.0.2
whatweb h172.17.0.2
netcat -vz 172.17.0.2 1-1000
```

***

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -T5 10.10.11.70
```

```bash
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-05-21 19:47:38Z)
111/tcp  open  rpcbind       2-4 (RPC #100000)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: PUPPY.HTB0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
2049/tcp open  nlockmgr      1-4 (RPC #100021)
3260/tcp open  iscsi?
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: PUPPY.HTB0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Encontramos multitud de puertos abiertos, lo normal en máquinas Windows. Ademas nos encontramos con que la máquina objetivo es un Domain Controller, por la presencia de los puertos 3268 o 389, reservados para DCs.

Destacan los puertos:

* `111 (RPC)` - Puede contener recursos compartidos o enumerar usuarios
* `445 (SMB)` - Recursos compartidos y enumeración
* `5985 (WinRM)` - Acceso con EvilWinRM con contraseña
* `88 (Kerberos)` - Posible Kerberoasting o AS-REP Roasting

***

## <mark style="color:purple;">Acceso web (si hay servicio web)</mark>

Mostrar lo que hay

***

## <mark style="color:purple;">Enumeración web (si hay servicio web)</mark>

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

## <mark style="color:purple;">Enumeración inicial</mark>

```
enum4linux-ng puppy.htb
```

***

## <mark style="color:purple;">Enumeración de Active Directory (si es AD)</mark>

### Extracción de información LDAP

```bash
ldapsearch -x -H ldap://puppy.htb -D "levi.james@PUPPY.HTB" -w 'KingofAkron2025!' -b "dc=puppy,dc=htb" > ldapsearch.txt

cat ldapsearch.txt
```

### Enumeración de usuarios/grupos

```bash
crackmapexec smb puppy.htb -u levi.james -p 'KingofAkron2025!' --users

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
crackmapexec smb puppy.htb -u levi.james -p 'KingofAkron2025!' --shares

SMB         puppy.htb       445    DC               [*] Windows Server 2022 Build 20348 x64 (name:DC) (domain:PUPPY.HTB) (signing:True) (SMBv1:False)
SMB         puppy.htb       445    DC               [+] PUPPY.HTB\levi.james:KingofAkron2025! 
SMB         puppy.htb       445    DC               [+] Enumerated shares
SMB         puppy.htb       445    DC               Share           Permissions     Remark
SMB         puppy.htb       445    DC               -----           -----------     ------
SMB         puppy.htb       445    DC               ADMIN$                          Remote Admin
SMB         puppy.htb       445    DC               C$                              Default share
SMB         puppy.htb       445    DC               DEV                             DEV-SHARE for PUPPY-DEVS
SMB         puppy.htb       445    DC               IPC$            READ            Remote IPC
SMB         puppy.htb       445    DC               NETLOGON        READ            Logon server share 
SMB         puppy.htb       445    DC               SYSVOL          READ            Logon server share 
```

Encontramos un Share DEV interesante, pero no tenemos permisos de lectura, y analizando el resto de Shares no encontramos nada relevante. Seguramente si conseguimos un usuario del grupo DEVELOPERS podríamos acceder.

***

## <mark style="color:purple;">Enumeración con Bloodhound (Si es AD)</mark>

### Editar resolv.conf

<pre class="language-bash"><code class="lang-bash">sudo gedit /etc/resolv.conf
<strong>
</strong><strong>domain puppy.htb
</strong>nameserver 10.10.11.70
search puppy.htb
</code></pre>

### Bloodhound Python

```bash
bloodhound-python -u levi.james -p 'KingofAkron2025!' -d puppy.htb -c all --zip

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
