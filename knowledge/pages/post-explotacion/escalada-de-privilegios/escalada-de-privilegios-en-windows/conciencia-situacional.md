
# Conciencia situacional

En cualquier situación, ya sea en nuestra vida diaria o durante un proyecto como una prueba de penetración de red, siempre es importante orientarnos en el espacio y el tiempo. No podemos funcionar y reaccionar de manera efectiva sin comprender nuestro entorno actual. Necesitamos esta información para tomar decisiones informadas sobre nuestros próximos pasos para operar de manera proactiva en lugar de reactiva. Cuando aterrizamos en un sistema Windows o Linux con la intención de escalar privilegios a continuación, hay varias cosas que siempre debemos buscar para planificar nuestros próximos movimientos. Es posible que encontremos otros hosts a los que podamos acceder directamente, protecciones implementadas que deban eludirse o descubramos que ciertas herramientas no funcionarán contra el sistema en cuestión.

***

## <mark style="color:purple;">Información de la red</mark>

La recopilación de información de red es una parte crucial de nuestra enumeración. Podemos descubrir que el host tiene una conexión dual y que comprometer el host puede permitirnos movernos lateralmente a otra parte de la red a la que no podíamos acceder anteriormente. La conexión dual significa que el host o servidor pertenece a dos o más redes diferentes y, en la mayoría de los casos, tiene varias interfaces de red físicas o virtuales. Siempre debemos consultar [las tablas de enrutamiento](https://en.wikipedia.org/wiki/Routing_table) para ver información sobre la red local y las redes que la rodean. También podemos recopilar información sobre el dominio local (si el host es parte de un entorno de Active Directory), incluidas las direcciones IP de los controladores de dominio. También es importante utilizar el comando [arp](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/arp) para ver el caché ARP de cada interfaz y ver otros hosts con los que el host se ha comunicado recientemente. Esto podría ayudarnos con el movimiento lateral después de obtener las credenciales. Podría ser un buen indicador de a qué hosts se están conectando los administradores a través de RDP o WinRM desde este host.

Esta información de red puede ayudarnos directa o indirectamente con la escalada de privilegios locales. Puede llevarnos por otro camino hacia un sistema al que podemos acceder o en el que podemos escalar privilegios o revelar información que podemos usar para el movimiento lateral para ampliar nuestro acceso después de escalar privilegios en el sistema actual.

### **Interfaz(es), dirección(es) IP, información DNS**

```cmd-session
C:\htb> ipconfig /all

Windows IP Configuration

   Host Name . . . . . . . . . . . . : WINLPE-SRV01
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No
   DNS Suffix Search List. . . . . . : .htb

Ethernet adapter Ethernet1:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter
   Physical Address. . . . . . . . . : 00-50-56-B9-C5-4B
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::f055:fefd:b1b:9919%9(Preferred)
   IPv4 Address. . . . . . . . . . . : 192.168.20.56(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.20.1
   DHCPv6 IAID . . . . . . . . . . . : 151015510
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-27-ED-DB-68-00-50-56-B9-90-94
   DNS Servers . . . . . . . . . . . : 8.8.8.8
   NetBIOS over Tcpip. . . . . . . . : Enabled

Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . : .htb
   Description . . . . . . . . . . . : Intel(R) 82574L Gigabit Network Connection
   Physical Address. . . . . . . . . : 00-50-56-B9-90-94
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes
   IPv6 Address. . . . . . . . . . . : dead:beef::e4db:5ea3:2775:8d4d(Preferred)
   Link-local IPv6 Address . . . . . : fe80::e4db:5ea3:2775:8d4d%4(Preferred)
   IPv4 Address. . . . . . . . . . . : 10.129.43.8(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Lease Obtained. . . . . . . . . . : Thursday, March 25, 2021 9:24:45 AM
   Lease Expires . . . . . . . . . . : Monday, March 29, 2021 1:28:44 PM
   Default Gateway . . . . . . . . . : fe80::250:56ff:feb9:4ddf%4
                                       10.129.0.1
   DHCP Server . . . . . . . . . . . : 10.129.0.1
   DHCPv6 IAID . . . . . . . . . . . : 50352214
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-27-ED-DB-68-00-50-56-B9-90-94
   DNS Servers . . . . . . . . . . . : 1.1.1.1
                                       8.8.8.8
   NetBIOS over Tcpip. . . . . . . . : Enabled

Tunnel adapter isatap..htb:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : .htb
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

Tunnel adapter Teredo Tunneling Pseudo-Interface:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Teredo Tunneling Pseudo-Interface
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

Tunnel adapter isatap.{02D6F04C-A625-49D1-A85D-4FB454FBB3DB}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter #2
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
```

### **Tabla ARP**

```cmd-session
C:\htb> arp -a

Interface: 10.129.43.8 --- 0x4
  Internet Address      Physical Address      Type
  10.129.0.1            00-50-56-b9-4d-df     dynamic
  10.129.43.12          00-50-56-b9-da-ad     dynamic
  10.129.43.13          00-50-56-b9-5b-9f     dynamic
  10.129.255.255        ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.252           01-00-5e-00-00-fc     static
  224.0.0.253           01-00-5e-00-00-fd     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static

Interface: 192.168.20.56 --- 0x9
  Internet Address      Physical Address      Type
  192.168.20.255        ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static
```

### **Tabla de enrutamiento**

```powershell
C:\htb> route print

===========================================================================
Interface List
  9...00 50 56 b9 c5 4b ......vmxnet3 Ethernet Adapter
  4...00 50 56 b9 90 94 ......Intel(R) 82574L Gigabit Network Connection
  1...........................Software Loopback Interface 1
  3...00 00 00 00 00 00 00 e0 Microsoft ISATAP Adapter
  5...00 00 00 00 00 00 00 e0 Teredo Tunneling Pseudo-Interface
 13...00 00 00 00 00 00 00 e0 Microsoft ISATAP Adapter #2
===========================================================================

IPv4 Route Table
===========================================================================
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0       10.129.0.1      10.129.43.8     25
          0.0.0.0          0.0.0.0     192.168.20.1    192.168.20.56    271
       10.129.0.0      255.255.0.0         On-link       10.129.43.8    281
      10.129.43.8  255.255.255.255         On-link       10.129.43.8    281
   10.129.255.255  255.255.255.255         On-link       10.129.43.8    281
        127.0.0.0        255.0.0.0         On-link         127.0.0.1    331
        127.0.0.1  255.255.255.255         On-link         127.0.0.1    331
  127.255.255.255  255.255.255.255         On-link         127.0.0.1    331
     192.168.20.0    255.255.255.0         On-link     192.168.20.56    271
    192.168.20.56  255.255.255.255         On-link     192.168.20.56    271
   192.168.20.255  255.255.255.255         On-link     192.168.20.56    271
        224.0.0.0        240.0.0.0         On-link         127.0.0.1    331
        224.0.0.0        240.0.0.0         On-link       10.129.43.8    281
        224.0.0.0        240.0.0.0         On-link     192.168.20.56    271
  255.255.255.255  255.255.255.255         On-link         127.0.0.1    331
  255.255.255.255  255.255.255.255         On-link       10.129.43.8    281
  255.255.255.255  255.255.255.255         On-link     192.168.20.56    271
===========================================================================
Persistent Routes:
  Network Address          Netmask  Gateway Address  Metric
          0.0.0.0          0.0.0.0     192.168.20.1  Default
===========================================================================

IPv6 Route Table
===========================================================================
Active Routes:
 If Metric Network Destination      Gateway
  4    281 ::/0                     fe80::250:56ff:feb9:4ddf
  1    331 ::1/128                  On-link
  4    281 dead:beef::/64           On-link
  4    281 dead:beef::e4db:5ea3:2775:8d4d/128
                                    On-link
  4    281 fe80::/64                On-link
  9    271 fe80::/64                On-link
  4    281 fe80::e4db:5ea3:2775:8d4d/128
                                    On-link
  9    271 fe80::f055:fefd:b1b:9919/128
                                    On-link
  1    331 ff00::/8                 On-link
  4    281 ff00::/8                 On-link
  9    271 ff00::/8                 On-link
===========================================================================
Persistent Routes:
  None
```

***

## <mark style="color:purple;">Enumeración de protecciones</mark>

La mayoría de los entornos modernos cuentan con algún tipo de antivirus o servicio de detección y respuesta de endpoints (EDR) en ejecución para supervisar, alertar y bloquear amenazas de forma proactiva. Estas herramientas pueden interferir con el proceso de enumeración. Es muy probable que presenten algún tipo de desafío durante el proceso de escalada de privilegios, especialmente si estamos utilizando algún tipo de herramienta o exploit PoC público. Enumerar las protecciones implementadas nos ayudará a asegurarnos de que estamos utilizando métodos que no se bloquean ni se detectan y nos ayudará si tenemos que crear cargas útiles personalizadas o modificar herramientas antes de compilarlas.

Muchas organizaciones utilizan algún tipo de solución de lista blanca de aplicaciones para controlar qué tipos de aplicaciones y archivos pueden ejecutar determinados usuarios. Esto se puede utilizar para intentar impedir que los usuarios que no sean administradores ejecuten archivos binarios cómo `cmd.exe`, `powershell.exe` o tipos de archivos que no necesiten para su trabajo diario. Una solución popular ofrecida por Microsoft es [AppLocker](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/applocker/applocker-overview) . Podemos utilizar el cmdlet [GetAppLockerPolicy](https://docs.microsoft.com/en-us/powershell/module/applocker/get-applockerpolicy?view=windowsserver2019-ps) para enumerar las políticas locales, efectivas (aplicadas) y de dominio de AppLocker. Esto nos ayudará a ver qué archivos binarios o tipos de archivos se pueden bloquear y si tendremos que realizar algún tipo de omisión de AppLocker durante nuestra enumeración o antes de ejecutar una herramienta o técnica para aumentar los privilegios.

En una interacción en el mundo real, es probable que el cliente tenga implementadas protecciones que detecten las herramientas y scripts más comunes (incluidos los presentados en la sección anterior). Existen formas de lidiar con estos problemas, y enumerar las protecciones en uso puede ayudarnos a modificar nuestras herramientas en un entorno de laboratorio y probarlas antes de usarlas contra un sistema cliente. Algunas herramientas EDR detectan o incluso bloquean el uso de binarios comunes como `net.exe`, `tasklist`, etc. Las organizaciones pueden restringir qué binarios puede ejecutar un usuario o marcar inmediatamente actividades sospechosas, como que la máquina de un contador muestre binarios específicos que se ejecutan a través de cmd.exe. La enumeración temprana y un conocimiento profundo del entorno del cliente y las soluciones alternativas contra soluciones EDR y AV comunes pueden ahorrarnos tiempo durante una interacción no evasiva y determinar el éxito o el fracaso de una interacción evasiva.

### **Comprobar el estado de Windows Defender**

```powershell
PS C:\htb> Get-MpComputerStatus

AMEngineVersion                 : 1.1.17900.7
AMProductVersion                : 4.10.14393.2248
AMServiceEnabled                : True
AMServiceVersion                : 4.10.14393.2248
AntispywareEnabled              : True
AntispywareSignatureAge         : 1
AntispywareSignatureLastUpdated : 3/28/2021 2:59:13 AM
AntispywareSignatureVersion     : 1.333.1470.0
AntivirusEnabled                : True
AntivirusSignatureAge           : 1
AntivirusSignatureLastUpdated   : 3/28/2021 2:59:12 AM
AntivirusSignatureVersion       : 1.333.1470.0
BehaviorMonitorEnabled          : False
ComputerID                      : 54AF7DE4-3C7E-4DA0-87AC-831B045B9063
ComputerState                   : 0
FullScanAge                     : 4294967295
FullScanEndTime                 :
FullScanStartTime               :
IoavProtectionEnabled           : False
LastFullScanSource              : 0
LastQuickScanSource             : 0
NISEnabled                      : False
NISEngineVersion                : 0.0.0.0
NISSignatureAge                 : 4294967295
NISSignatureLastUpdated         :
NISSignatureVersion             : 0.0.0.0
OnAccessProtectionEnabled       : False
QuickScanAge                    : 4294967295
QuickScanEndTime                :
QuickScanStartTime              :
RealTimeProtectionEnabled       : False
RealTimeScanDirection           : 0
PSComputerName                  :
```

### **Lista de reglas de AppLocker**

```powershell
PS C:\htb> Get-AppLockerPolicy -Effective | select -ExpandProperty RuleCollections

PublisherConditions : {*\*\*,0.0.0.0-*}
PublisherExceptions : {}
PathExceptions      : {}
HashExceptions      : {}
Id                  : a9e18c21-ff8f-43cf-b9fc-db40eed693ba
Name                : (Default Rule) All signed packaged apps
Description         : Allows members of the Everyone group to run packaged apps that are signed.
UserOrGroupSid      : S-1-1-0
Action              : Allow

PathConditions      : {%PROGRAMFILES%\*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : 921cc481-6e17-4653-8f75-050b80acca20
Name                : (Default Rule) All files located in the Program Files folder
Description         : Allows members of the Everyone group to run applications that are located in the Program Files
                      folder.
UserOrGroupSid      : S-1-1-0
Action              : Allow

PathConditions      : {%WINDIR%\*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : a61c8b2c-a319-4cd0-9690-d2177cad7b51
Name                : (Default Rule) All files located in the Windows folder
Description         : Allows members of the Everyone group to run applications that are located in the Windows folder.
UserOrGroupSid      : S-1-1-0
Action              : Allow

PathConditions      : {*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : fd686d83-a829-4351-8ff4-27c7de5755d2
Name                : (Default Rule) All files
Description         : Allows members of the local Administrators group to run all applications.
UserOrGroupSid      : S-1-5-32-544
Action              : Allow

PublisherConditions : {*\*\*,0.0.0.0-*}
PublisherExceptions : {}
PathExceptions      : {}
HashExceptions      : {}
Id                  : b7af7102-efde-4369-8a89-7a6a392d1473
Name                : (Default Rule) All digitally signed Windows Installer files
Description         : Allows members of the Everyone group to run digitally signed Windows Installer files.
UserOrGroupSid      : S-1-1-0
Action              : Allow

PathConditions      : {%WINDIR%\Installer\*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : 5b290184-345a-4453-b184-45305f6d9a54
Name                : (Default Rule) All Windows Installer files in %systemdrive%\Windows\Installer
Description         : Allows members of the Everyone group to run all Windows Installer files located in
                      %systemdrive%\Windows\Installer.
UserOrGroupSid      : S-1-1-0
Action              : Allow

PathConditions      : {*.*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : 64ad46ff-0d71-4fa0-a30b-3f3d30c5433d
Name                : (Default Rule) All Windows Installer files
Description         : Allows members of the local Administrators group to run all Windows Installer files.
UserOrGroupSid      : S-1-5-32-544
Action              : Allow

PathConditions      : {%PROGRAMFILES%\*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : 06dce67b-934c-454f-a263-2515c8796a5d
Name                : (Default Rule) All scripts located in the Program Files folder
Description         : Allows members of the Everyone group to run scripts that are located in the Program Files folder.
UserOrGroupSid      : S-1-1-0
Action              : Allow

PathConditions      : {%WINDIR%\*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : 9428c672-5fc3-47f4-808a-a0011f36dd2c
Name                : (Default Rule) All scripts located in the Windows folder
Description         : Allows members of the Everyone group to run scripts that are located in the Windows folder.
UserOrGroupSid      : S-1-1-0
Action              : Allow

PathConditions      : {*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : ed97d0cb-15ff-430f-b82c-8d7832957725
Name                : (Default Rule) All scripts
Description         : Allows members of the local Administrators group to run all scripts.
UserOrGroupSid      : S-1-5-32-544
Action              : Allow
```

### **Política de prueba de AppLocker**

```powershell
PS C:\htb> Get-AppLockerPolicy -Local | Test-AppLockerPolicy -path C:\Windows\System32\cmd.exe -User Everyone

FilePath                    PolicyDecision MatchingRule
--------                    -------------- ------------
C:\Windows\System32\cmd.exe         Denied c:\windows\system32\cmd.exe
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

RDP con usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

### Pregunta 1

> ¿Cuál es la dirección IP de la otra NIC conectada al host de destino?

```powershell
Windows IP Configuration

   Host Name . . . . . . . . . . . . : WINLPE-SRV01
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No
   DNS Suffix Search List. . . . . . : htb

Ethernet adapter Ethernet1:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter
   Physical Address. . . . . . . . . : 00-50-56-B0-4B-D5
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::2cc7:f144:ea6:937b%2(Preferred)
   IPv4 Address. . . . . . . . . . . : 172.16.20.45(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.254.0
   Default Gateway . . . . . . . . . : 172.16.20.1
   DHCPv6 IAID . . . . . . . . . . . : 151015510
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-2F-40-01-A3-00-50-56-B0-4B-D5
   DNS Servers . . . . . . . . . . . : 8.8.8.8
   NetBIOS over Tcpip. . . . . . . . : Enabled

Ethernet adapter Ethernet0 2:

   Connection-specific DNS Suffix  . : .htb
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter #2
   Physical Address. . . . . . . . . : 00-50-56-B0-E6-5D
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes
   IPv6 Address. . . . . . . . . . . : dead:beef::1d9(Preferred)
   Lease Obtained. . . . . . . . . . : Thursday, February 13, 2025 11:34:36 AM
   Lease Expires . . . . . . . . . . : Thursday, February 13, 2025 12:34:36 PM
   IPv6 Address. . . . . . . . . . . : dead:beef::4db1:a779:b462:3368(Preferred)
   Link-local IPv6 Address . . . . . : fe80::4db1:a779:b462:3368%4(Preferred)
   IPv4 Address. . . . . . . . . . . : 10.129.43.43(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Lease Obtained. . . . . . . . . . : Thursday, February 13, 2025 11:34:37 AM
   Lease Expires . . . . . . . . . . : Thursday, February 13, 2025 12:34:36 PM
   Default Gateway . . . . . . . . . : fe80::250:56ff:feb0:ef1%4
                                       10.129.0.1
   DHCP Server . . . . . . . . . . . : 10.129.0.1
   DHCPv6 IAID . . . . . . . . . . . : 436228182
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-2F-40-01-A3-00-50-56-B0-4B-D5
   DNS Servers . . . . . . . . . . . : 1.1.1.1
                                       8.8.8.8
   NetBIOS over Tcpip. . . . . . . . : Enabled
   Connection-specific DNS Suffix Search List :
                                       htb
```

El comando `ipconfig /all` muestra que el host tiene **dos interfaces activas** con direcciones IPv4 asignadas:

1️⃣ **Ethernet1**

* **IP:** `172.16.20.45`(IP interna)
* **Máscara:** `255.255.254.0`
* **Gateway:** `172.16.20.1`

2️⃣ **Ethernet0 2**

* **IP:** `10.129.43.43` (IP actual)
* **Máscara:** `255.255.0.0`
* **Gateway:** `10.129.0.1`

Ambas interfaces están activas, lo que indica que este host está conectado a **dos redes diferentes** simultáneamente.

***

### Pregunta 2

> ¿Qué otro ejecutable además de `cmd.exe` está bloqueado por `AppLocker`?

Para realizar un escaneo completo de los ejecutables bloqueados por AppLocker en el sistema, lo más sencillo es con este script de powershell:

```powershell
$allowedExtensions = @(".exe", ".dll", ".msi", ".ps1", ".vbs", ".bat", ".cmd", ".psm1", ".psd1")
$files = Get-ChildItem -Path "C:\Windows\System32" | Where-Object { $allowedExtensions -contains $_.Extension }

foreach ($file in $files) {
    $result = Get-AppLockerPolicy -Local | Test-AppLockerPolicy -path $file.FullName -User Everyone
    if ($result.PolicyDecision -eq "Denied") {
        $result
    }
}
```

Eso nos buscará todos los ejecutables bloqueados en la ruta `C:\Windows\System32`, aunque se puede ajustar para que analice todo el sistema con `C:\*\*\*\*\*\*`

```
FilePath                                                          PolicyDecision MatchingRule
--------                                                          -------------- ------------
C:\Windows\System32\cmd.exe                                       Denied c:\windows\system32\cmd.exe
C:\Windows\System32\WindowsPowerShell\v1.0\powershell_ise.exe     Denied Block PowerShell ISE
C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell_ise.exe     Denied Block PowerShell ISE
```

Encontramos el otro ejecutable bloqueado: `powershell_ise.exe`
