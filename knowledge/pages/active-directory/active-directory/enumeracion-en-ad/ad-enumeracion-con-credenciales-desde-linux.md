
# AD: Enumeración con credenciales: desde Linux

Ahora que hemos adquirido un punto de apoyo en el dominio, es hora de profundizar más utilizando nuestras credenciales de usuario de dominio con privilegios bajos. Dado que tenemos una idea general sobre la base de usuarios y las máquinas del dominio, es hora de enumerar el dominio en profundidad.&#x20;

Estamos interesados ​​en información sobre:

* `Atributos de computadora`
* `Usuarios del dominio`
* `Membresía de grupos`
* `Objetos de política de grupo`
* `Permisos`
* `ACL`
* `Confianzas` y más.&#x20;

Tenemos varias opciones disponibles, pero lo más importante que debemos recordar es que la mayoría de estas herramientas no funcionarán sin credenciales de usuario de dominio válidas en cualquier nivel de permiso. Entonces, como mínimo, tendremos que haber adquirido una contraseña de texto sin cifrar de usuario, un hash de contraseña NTLM o acceso `SYSTEM` en un host unido a un dominio.

***

## <mark style="color:purple;">CrackMapExec</mark>

[CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) (CME) es un potente conjunto de herramientas que ayuda a evaluar los entornos de AD. Utiliza paquetes de los kits de herramientas `Impacket` y `PowerSploit` para realizar sus funciones. Para obtener explicaciones detalladas sobre el uso de la herramienta y los módulos que la acompañan, consulte la [wiki](https://github.com/byt3bl33d3r/CrackMapExec/wiki) . Podemos usar la flag `-h` para revisar las opciones y la sintaxis disponibles.

**Menú de ayuda de CME**

```shell-session
afsh4ck@kali$ crackmapexec -h

usage: crackmapexec [-h] [-t THREADS] [--timeout TIMEOUT] [--jitter INTERVAL] [--darrell]
                    [--verbose]
                    {mssql,smb,ssh,winrm} ...

      ______ .______           ___        ______  __  ___ .___  ___.      ___      .______    _______ ___   ___  _______   ______
     /      ||   _  \         /   \      /      ||  |/  / |   \/   |     /   \     |   _  \  |   ____|\  \ /  / |   ____| /      |
    |  ,----'|  |_)  |       /  ^  \    |  ,----'|  '  /  |  \  /  |    /  ^  \    |  |_)  | |  |__    \  V  /  |  |__   |  ,----'
    |  |     |      /       /  /_\  \   |  |     |    <   |  |\/|  |   /  /_\  \   |   ___/  |   __|    >   <   |   __|  |  |
    |  `----.|  |\  \----. /  _____  \  |  `----.|  .  \  |  |  |  |  /  _____  \  |  |      |  |____  /  .  \  |  |____ |  `----.
     \______|| _| `._____|/__/     \__\  \______||__|\__\ |__|  |__| /__/     \__\ | _|      |_______|/__/ \__\ |_______| \______|

                                         A swiss army knife for pentesting networks
                                    Forged by @byt3bl33d3r using the powah of dank memes

                                                      Version: 5.0.2dev
                                                     Codename: P3l1as
optional arguments:
  -h, --help            show this help message and exit
  -t THREADS            set how many concurrent threads to use (default: 100)
  --timeout TIMEOUT     max timeout in seconds of each thread (default: None)
  --jitter INTERVAL     sets a random delay between each connection (default: None)
  --darrell             give Darrell a hand
  --verbose             enable verbose output

protocols:
  available protocols

  {mssql,smb,ssh,winrm}
    mssql               own stuff using MSSQL
    smb                 own stuff using SMB
    ssh                 own stuff using SSH
    winrm               own stuff using WINRM

Ya feelin' a bit buggy all of a sudden?
```

Podemos ver que podemos usar la herramienta con credenciales MSSQL, SMB, SSH y WinRM. Veamos nuestras opciones para CME con el protocolo SMB:

**Opciones CME (SMB)**

```shell-session
afsh4ck@kali$ crackmapexec smb -h

usage: crackmapexec smb [-h] [-id CRED_ID [CRED_ID ...]] [-u USERNAME [USERNAME ...]] [-p PASSWORD [PASSWORD ...]] [-k]
                        [--aesKey AESKEY [AESKEY ...]] [--kdcHost KDCHOST]
                        [--gfail-limit LIMIT | --ufail-limit LIMIT | --fail-limit LIMIT] [-M MODULE]
                        [-o MODULE_OPTION [MODULE_OPTION ...]] [-L] [--options] [--server {https,http}] [--server-host HOST]
                        [--server-port PORT] [-H HASH [HASH ...]] [--no-bruteforce] [-d DOMAIN | --local-auth] [--port {139,445}]
                        [--share SHARE] [--smb-server-port SMB_SERVER_PORT] [--gen-relay-list OUTPUT_FILE] [--continue-on-success]
                        [--sam | --lsa | --ntds [{drsuapi,vss}]] [--shares] [--sessions] [--disks] [--loggedon-users] [--users [USER]]
                        [--groups [GROUP]] [--local-groups [GROUP]] [--pass-pol] [--rid-brute [MAX_RID]] [--wmi QUERY]
                        [--wmi-namespace NAMESPACE] [--spider SHARE] [--spider-folder FOLDER] [--content] [--exclude-dirs DIR_LIST]
                        [--pattern PATTERN [PATTERN ...] | --regex REGEX [REGEX ...]] [--depth DEPTH] [--only-files]
                        [--put-file FILE FILE] [--get-file FILE FILE] [--exec-method {atexec,smbexec,wmiexec,mmcexec}] [--force-ps32]
                        [--no-output] [-x COMMAND | -X PS_COMMAND] [--obfs] [--amsi-bypass FILE] [--clear-obfscripts]
                        [target ...]

positional arguments:
  target                the target IP(s), range(s), CIDR(s), hostname(s), FQDN(s), file(s) containing a list of targets, NMap XML or
                        .Nessus file(s)

optional arguments:
  -h, --help            show this help message and exit
  -id CRED_ID [CRED_ID ...]
                        database credential ID(s) to use for authentication
  -u USERNAME [USERNAME ...]
                        username(s) or file(s) containing usernames
  -p PASSWORD [PASSWORD ...]
                        password(s) or file(s) containing passwords
  -k, --kerberos        Use Kerberos authentication from ccache file (KRB5CCNAME)
  
<SNIP>  
```

CME ofrece un menú de ayuda para cada protocolo (es decir `crackmapexec winrm -h`, etc.). Asegúrese de revisar todo el menú de ayuda y todas las opciones posibles. Por ahora, las flags que nos interesan son:

<table><thead><tr><th width="233">Opción</th><th>Descripción</th></tr></thead><tbody><tr><td><code>-u</code></td><td>Nombre de usuario cuyas credenciales usaremos para autenticar</td></tr><tr><td><code>-p</code></td><td>Contraseña del usuario</td></tr><tr><td><code>Target (IP o FQDN)</code></td><td>Host de destino a enumerar (en nuestro caso, el Controlador de Dominio)</td></tr><tr><td><code>--users</code></td><td>Especifica enumerar usuarios del dominio</td></tr><tr><td><code>--groups</code></td><td>Especifica enumerar grupos del dominio</td></tr><tr><td><code>--loggedon-users</code></td><td>Intenta enumerar qué usuarios están conectados a un destino, si los hay</td></tr></tbody></table>

Comenzaremos usando el protocolo SMB para enumerar usuarios y grupos. Nos centraremos en el controlador de dominio (cuya dirección descubrimos anteriormente) porque contiene todos los datos de la base de datos del dominio que nos interesan. Asegúrese de anteponer todos los comandos con `sudo`.

### **CME - Enumeración de Usuarios del Dominio**

Comenzamos apuntando CME al controlador de dominio y usando las credenciales del usuario `forend` para recuperar una lista de todos los usuarios del dominio. Observe que cuando nos proporciona la información del usuario, incluye puntos de datos como el atributo [badPwdCount](https://docs.microsoft.com/en-us/windows/win32/adschema/a-badpwdcount) . Esto resulta útil al realizar acciones como la pulverización selectiva de contraseñas. Podríamos crear una lista de usuarios objetivo filtrando a los usuarios con su atributo `badPwdCount` superior a 0 para tener mucho cuidado de no bloquear ninguna cuenta.

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 --users

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\forend:Klmcargo2 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] Enumerated domain user(s)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\administrator                  badpwdcount: 0 baddpwdtime: 2022-03-29 12:29:14.476567
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\guest                          badpwdcount: 0 baddpwdtime: 1600-12-31 19:03:58
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\lab_adm                        badpwdcount: 0 baddpwdtime: 2022-04-09 23:04:58.611828
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\krbtgt                         badpwdcount: 0 baddpwdtime: 1600-12-31 19:03:58
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\htb-student                    badpwdcount: 0 baddpwdtime: 2022-03-30 16:27:41.960920
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\avazquez                       badpwdcount: 3 baddpwdtime: 2022-02-24 18:10:01.903395

<SNIP>
```

También podemos obtener una lista completa de los grupos de dominios. Debemos guardar todos los resultados en archivos para poder acceder a ellos fácilmente más tarde para generar informes o utilizarlos con otras herramientas.

### **CME - Enumeración de Grupos del Dominio**

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 --groups
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\forend:Klmcargo2 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] Enumerated domain group(s)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Administrators                           membercount: 3
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Users                                    membercount: 4
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Guests                                   membercount: 2
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Print Operators                          membercount: 0
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Backup Operators                         membercount: 1
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Replicator                               membercount: 0

<SNIP>

SMB         172.16.5.5      445    ACADEMY-EA-DC01  Domain Admins                            membercount: 19
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Domain Users                             membercount: 0

<SNIP>

SMB         172.16.5.5      445    ACADEMY-EA-DC01  Contractors                              membercount: 138
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Accounting                               membercount: 15
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Engineering                              membercount: 19
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Executives                               membercount: 10
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Human Resources                          membercount: 36

<SNIP>
```

El fragmento anterior enumera los grupos dentro del dominio y la cantidad de usuarios en cada uno. El resultado también muestra los grupos integrados en el controlador de dominio, como `Backup Operators`. Podemos comenzar a anotar los grupos de interés. Tome nota de los grupos clave como `Administrators`, `Domain Admins`, `Executives`, cualquier grupo que pueda contener administradores de TI privilegiados, etc. Estos grupos probablemente contendrán usuarios con privilegios elevados que valga la pena analizar durante nuestra evaluación.

### **CME - Logged On Users**

También podemos usar CME para apuntar a otros hosts. Echemos un vistazo a lo que parece ser un servidor de archivos para ver qué usuarios están conectados actualmente.

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 172.16.5.130 -u forend -p Klmcargo2 --loggedon-users

SMB         172.16.5.130    445    ACADEMY-EA-FILE  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-FILE) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
SMB         172.16.5.130    445    ACADEMY-EA-FILE  [+] INLANEFREIGHT.LOCAL\forend:Klmcargo2 (Pwn3d!)
SMB         172.16.5.130    445    ACADEMY-EA-FILE  [+] Enumerated loggedon users
SMB         172.16.5.130    445    ACADEMY-EA-FILE  INLANEFREIGHT\clusteragent              logon_server: ACADEMY-EA-DC01
SMB         172.16.5.130    445    ACADEMY-EA-FILE  INLANEFREIGHT\lab_adm                   logon_server: ACADEMY-EA-DC01
SMB         172.16.5.130    445    ACADEMY-EA-FILE  INLANEFREIGHT\svc_qualys                logon_server: ACADEMY-EA-DC01
SMB         172.16.5.130    445    ACADEMY-EA-FILE  INLANEFREIGHT\wley                      logon_server: ACADEMY-EA-DC01

<SNIP>
```

Vemos que muchos usuarios han iniciado sesión en este servidor, lo cual es muy interesante. También podemos ver que nuestro usuario `forend`es un administrador local porque `(Pwn3d!)`aparece después de que la herramienta se autentica exitosamente en el host de destino. Los usuarios administrativos pueden utilizar un host como este como host de salto o similar. Podemos ver que el usuario `svc_qualys`que anteriormente identificamos como administrador del dominio ha iniciado sesión. Podría ser una victoria fácil si podemos robar las credenciales de este usuario de la memoria o suplantarlas.

Como veremos más adelante, `BloodHound`(y otras herramientas como `PowerView`) se pueden utilizar para buscar sesiones de usuario. BloodHound es particularmente potente, ya que podemos usarlo para ver sesiones de usuario de dominio de forma gráfica y rápida de muchas maneras. De todas formas, herramientas como CME son excelentes para una enumeración más específica y para la búsqueda de usuarios.

### **CME - Búsqueda de Recursos Compartidos**

Podemos utilizar la flag `--shares` para enumerar los recursos compartidos disponibles en el host remoto y el nivel de acceso que nuestra cuenta de usuario tiene a cada recurso compartido (acceso de LECTURA o ESCRITURA). Ejecutemos esto contra el controlador de dominio INLANEFREIGHT.LOCAL.

**Enumeración de acciones: controlador de dominio**

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 --shares

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\forend:Klmcargo2 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] Enumerated shares
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Share           Permissions     Remark
SMB         172.16.5.5      445    ACADEMY-EA-DC01  -----           -----------     ------
SMB         172.16.5.5      445    ACADEMY-EA-DC01  ADMIN$                          Remote Admin
SMB         172.16.5.5      445    ACADEMY-EA-DC01  C$                              Default share
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Department Shares READ            
SMB         172.16.5.5      445    ACADEMY-EA-DC01  IPC$            READ            Remote IPC
SMB         172.16.5.5      445    ACADEMY-EA-DC01  NETLOGON        READ            Logon server share 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  SYSVOL          READ            Logon server share 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  User Shares     READ            
SMB         172.16.5.5      445    ACADEMY-EA-DC01  ZZZ_archive     READ 
```

Vemos varios recursos compartidos disponibles para nosotros con acceso `READ`. Vale la pena investigar más a fondo los recursos compartidos , y `Department Shares`, ya que pueden contener datos confidenciales, como contraseñas o información de identificación personal. A continuación, podemos investigar los recursos compartidos y rastrear cada directorio en busca de archivos. El módulo `spider_plus` buscará en cada recurso compartido legible en el host y enumerará todos los archivos legibles.

### **CME - Spider\_plus**

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 -M spider_plus --share 'Department Shares'

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\forend:Klmcargo2 
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*] Started spidering plus with option:
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*]        DIR: ['print$']
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*]        EXT: ['ico', 'lnk']
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*]       SIZE: 51200
SPIDER_P... 172.16.5.5      445    ACADEMY-EA-DC01  [*]     OUTPUT: /tmp/cme_spider_plus
```

En el comando anterior, ejecutamos la araña contra el `Department Shares`. Cuando se completa, CME escribe los resultados en un archivo JSON ubicado en `/tmp/cme_spider_plus/<ip-host>`.&#x20;

A continuación, podemos ver una parte de la salida JSON. Podríamos buscar archivos interesantes, como archivos `web.config` o scripts que puedan contener contraseñas. Si quisiéramos investigar más, podríamos extraer esos archivos para ver qué contienen y quizás encontrar algunas credenciales codificadas u otra información confidencial.

```shell-session
afsh4ck@kali$ head -n 10 /tmp/cme_spider_plus/172.16.5.5.json 

{
    "Department Shares": {
        "Accounting/Private/AddSelect.bat": {
            "atime_epoch": "2022-03-31 14:44:42",
            "ctime_epoch": "2022-03-31 14:44:39",
            "mtime_epoch": "2022-03-31 15:14:46",
            "size": "278 Bytes"
        },
        "Accounting/Private/ApproveConnect.wmf": {
            "atime_epoch": "2022-03-31 14:45:14",
     
<SNIP>
```

CrackMapExec es poderoso y esto es sólo un pequeño vistazo a sus capacidades; Vale la pena experimentar más con él contra los objetivos de laboratorio. Utilizaremos CME de varias maneras a medida que avancemos en el resto de este módulo.

***

## <mark style="color:purple;">SMBMap</mark>

SMBMap es excelente para enumerar recursos compartidos SMB desde un host de ataque de Linux. Se puede utilizar para recopilar una lista de recursos compartidos, permisos y contenidos compartidos si están accesibles. Una vez que se obtiene el acceso, se puede utilizar para descargar y cargar archivos y ejecutar comandos remotos.

Al igual que CME, podemos usar SMBMap y un conjunto de credenciales de usuario de dominio para verificar si hay recursos compartidos accesibles en sistemas remotos. Al igual que con otras herramientas, podemos escribir el comando `smbmap -h` para ver el menú de uso de la herramienta. Además de enumerar recursos compartidos, podemos usar SMBMap para enumerar directorios de forma recursiva, enumerar el contenido de un directorio, buscar el contenido de archivos y más. Esto puede ser especialmente útil cuando se saquean recursos compartidos para obtener información útil.

### **SMBMap - Verificar el acceso**

```shell-session
afsh4ck@kali$ smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5

[+] IP: 172.16.5.5:445	Name: inlanefreight.local                               
        Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	ADMIN$                                            	NO ACCESS	Remote Admin
	C$                                                	NO ACCESS	Default share
	Department Shares                                 	READ ONLY	
	IPC$                                              	READ ONLY	Remote IPC
	NETLOGON                                          	READ ONLY	Logon server share 
	SYSVOL                                            	READ ONLY	Logon server share 
	User Shares                                       	READ ONLY	
	ZZZ_archive                                       	READ ONLY
```

Lo anterior nos dirá a qué puede acceder nuestro usuario y sus niveles de permiso. Al igual que nuestros resultados de CME, vemos que el usuario `forend` no tiene acceso al DC a través de `ADMIN$`o `C$`recursos compartidos (esto es lo esperado para una cuenta de usuario estándar), pero sí tiene acceso de lectura a través de `IPC$`, `NETLOGON` y `SYSVOL` que es el valor predeterminado en cualquier dominio. Los otros recursos compartidos no estándar, como `Department Shares` los recursos compartidos de usuario y de archivo, son los más interesantes. Hagamos una lista recursiva de los directorios del recurso compartido `Department Shares`. Podemos ver, como era de esperar, subdirectorios para cada departamento de la empresa.

### **SMBMap - Lista recursiva de todos los directorios**

```shell-session
afsh4ck@kali$ smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5 -R 'Department Shares' --dir-only

[+] IP: 172.16.5.5:445	Name: inlanefreight.local                               
        Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	Department Shares                                 	READ ONLY	
	.\Department Shares\*
	dr--r--r--                0 Thu Mar 31 15:34:29 2022	.
	dr--r--r--                0 Thu Mar 31 15:34:29 2022	..
	dr--r--r--                0 Thu Mar 31 15:14:48 2022	Accounting
	dr--r--r--                0 Thu Mar 31 15:14:39 2022	Executives
	dr--r--r--                0 Thu Mar 31 15:14:57 2022	Finance
	dr--r--r--                0 Thu Mar 31 15:15:04 2022	HR
	dr--r--r--                0 Thu Mar 31 15:15:21 2022	IT
	dr--r--r--                0 Thu Mar 31 15:15:29 2022	Legal
	dr--r--r--                0 Thu Mar 31 15:15:37 2022	Marketing
	dr--r--r--                0 Thu Mar 31 15:15:47 2022	Operations
	dr--r--r--                0 Thu Mar 31 15:15:58 2022	R&D
	dr--r--r--                0 Thu Mar 31 15:16:10 2022	Temp
	dr--r--r--                0 Thu Mar 31 15:16:18 2022	Warehouse

    <SNIP>
```

A medida que el listado recursivo se adentra más, le mostrará el resultado de todos los subdirectorios dentro de los directorios de nivel superior. El uso de la flag `--dir-only` proporcionó solo el resultado de todos los directorios y no incluyó todos los archivos. Pruebe esto con otros recursos compartidos en el controlador de dominio y vea qué puede encontrar.

***

## <mark style="color:purple;">rpcclient</mark>

[rpcclient](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html) es una herramienta muy útil creada para su uso con el protocolo Samba y para proporcionar funcionalidad adicional a través de MS-RPC. Puede enumerar, agregar, cambiar e incluso eliminar objetos de AD. Es muy versátil; solo tenemos que encontrar el comando correcto para ejecutar según lo que queremos lograr. La página del manual de rpcclient es muy útil para esto; solo escriba `man rpcclient` en el shell de su host de ataque y revise las opciones disponibles. Veamos algunas funciones de rpcclient que pueden ser útiles durante una prueba de penetración.

Debido a las sesiones `SMB NULL` (que se tratan en profundidad en las secciones sobre Password Spraying) en algunos de nuestros hosts, podemos realizar una enumeración autenticada o no autenticada utilizando rpcclient en el dominio INLANEFREIGHT.LOCAL. Un ejemplo de uso de rpcclient desde un punto de vista no autenticado (si esta configuración existe en nuestro dominio de destino) sería:

```bash
rpcclient -U "" -N 172.16.5.5
```

Lo anterior nos proporcionará una conexión enlazada y deberíamos ver un nuevo mensaje para comenzar a aprovechar el poder de rpcclient.

### **Sesión NULL de SMB con rpcclient**

![imagen](https://academy.hackthebox.com/storage/modules/143/rpcclient.png)

A partir de aquí, podemos empezar a enumerar cualquier cantidad de cosas diferentes. Comencemos con los usuarios del dominio.

### **Enumeración con rpcclient**

Mientras observa a los usuarios en rpcclient, es posible que observe un campo llamado `rid:` junto a cada usuario. Un [Relative Identifier (RID)](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/security-identifiers)  es un identificador único (representado en formato hexadecimal) utilizado por Windows para rastrear e identificar objetos. Para explicar cómo encaja esto, veamos los ejemplos siguientes:

* El [SID](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/security-identifiers) para el dominio INLANEFREIGHT.LOCAL es: `S-1-5-21-3842939050-3880317879-2865463114`.
* Cuando se crea un objeto dentro de un dominio, el número anterior (SID) se combinará con un RID para crear un valor único utilizado para representar el objeto.
* Entonces, el usuario de dominio `htb-student` con un RID:\[0x457] Hex 0x457 tendría = decimal `1111`, tendrá un SID de usuario completo de `S-1-5-21-3842939050-3880317879-2865463114-1111`:.
* Esto es exclusivo del objeto `htb-student` en el dominio INLANEFREIGHT.LOCAL y nunca verá este valor emparejado vinculado a otro objeto en este dominio o cualquier otro.

Sin embargo, notarás que hay cuentas que tienen el mismo RID independientemente del host en el que te encuentres. Las cuentas como el Administrador integrado para un dominio tendrán un RID \[administrador] rid:\[0x1f4], que, cuando se convierte a un valor decimal, es igual a `500`. La cuenta de administrador integrada siempre tendrá el valor RID `Hex 0x1f4`, o 500. Este siempre será el caso. Dado que este valor es exclusivo de un objeto, podemos usarlo para enumerar más información sobre él desde el dominio. Intentémoslo nuevamente con rpcclient. Profundizaremos un poco centrándonos en el usuario `htb-student`.

### **Enumeración de usuarios de RPCClient por RID**

```shell-session
rpcclient $> queryuser 0x457

        User Name   :   htb-student
        Full Name   :   Htb Student
        Home Drive  :
        Dir Drive   :
        Profile Path:
        Logon Script:
        Description :
        Workstations:
        Comment     :
        Remote Dial :
        Logon Time               :      Wed, 02 Mar 2022 15:34:32 EST
        Logoff Time              :      Wed, 31 Dec 1969 19:00:00 EST
        Kickoff Time             :      Wed, 13 Sep 30828 22:48:05 EDT
        Password last set Time   :      Wed, 27 Oct 2021 12:26:52 EDT
        Password can change Time :      Thu, 28 Oct 2021 12:26:52 EDT
        Password must change Time:      Wed, 13 Sep 30828 22:48:05 EDT
        unknown_2[0..31]...
        user_rid :      0x457
        group_rid:      0x201
        acb_info :      0x00000010
        fields_present: 0x00ffffff
        logon_divs:     168
        bad_password_count:     0x00000000
        logon_count:    0x0000001d
        padding1[0..7]...
        logon_hrs[0..21]...
```

Cuando buscamos información usando el comando `queryuser` contra RID `0x457`, RPC devolvió la información del usuario `htb-student` como se esperaba. Esto no fue difícil porque ya conocíamos el RID de `htb-student`. Si quisiéramos enumerar a todos los usuarios para recopilar los RID de más de uno, usaríamos el comando `enumdomusers`.

### **Enumdomusers**

```shell-session
rpcclient $> enumdomusers

user:[administrator] rid:[0x1f4]
user:[guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[lab_adm] rid:[0x3e9]
user:[htb-student] rid:[0x457]
user:[avazquez] rid:[0x458]
user:[pfalcon] rid:[0x459]
user:[fanthony] rid:[0x45a]
user:[wdillard] rid:[0x45b]
user:[lbradford] rid:[0x45c]
user:[sgage] rid:[0x45d]
user:[asanchez] rid:[0x45e]
user:[dbranch] rid:[0x45f]
user:[ccruz] rid:[0x460]
user:[njohnson] rid:[0x461]
user:[mholliday] rid:[0x462]

<SNIP>  
```

Si lo utiliza de esta manera, se imprimirán todos los usuarios del dominio por nombre y RID. Nuestra enumeración puede ser muy detallada utilizando rpcclient. Incluso podríamos comenzar a realizar acciones como editar usuarios y grupos o agregar los nuestros al dominio, pero esto está fuera del alcance de este módulo. Por ahora, solo queremos realizar la enumeración del dominio para validar nuestros hallazgos. Tómese un tiempo para jugar con las otras funciones de rpcclient y vea los resultados que producen.

***

## <mark style="color:purple;">Impacket Toolkit</mark>

Impacket es un conjunto de herramientas versátil que nos proporciona muchas formas diferentes de enumerar, interactuar y explotar los protocolos de Windows y encontrar la información que necesitamos usando Python. La herramienta se mantiene de forma activa y tiene muchos colaboradores, especialmente cuando surgen nuevas técnicas de ataque. Podríamos realizar muchas otras acciones con Impacket, pero solo destacaremos algunas en esta sección; [wmiexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/wmiexec.py) y [psexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/psexec.py) . Anteriormente, en la sección de [`Envenenamiento LLMNR`](/ethical-hacking-cheatsheet/active-directory/active-directory/sniffing-desde-el-foothold/llmnr-nbt-ns-poisoning-desde-linux.md), tomamos un hash para el usuario `wley` con `Responder` y lo desciframos para obtener la contraseña `transporter@4`. Veremos en la siguiente sección que este usuario es un administrador local en el host `ACADEMY-EA-FILE`. Utilizaremos las credenciales para las próximas acciones.

### **Psexec.py**

Una de las herramientas más útiles de la suite Impacket es `psexec.py`. Psexec.py es un clon del ejecutable psexec de Sysinternals, pero funciona de forma ligeramente diferente al original. La herramienta crea un servicio remoto cargando un ejecutable con un nombre aleatorio en el recurso compartido `ADMIN$` del host de destino. Luego, registra el servicio a través de `RPC`y `Windows Service Control Manager`. Una vez establecida, la comunicación se realiza a través de una tubería con nombre, lo que proporciona un shell remoto interactivo como `SYSTEM`en el host de la víctima.

**Usando psexec.py**

Para conectarnos a un host con `psexec.py`, necesitamos credenciales para un usuario con privilegios de administrador local.

```bash
psexec.py inlanefreight.local/wley:'transporter@4'@172.16.5.125  
```

![imagen](https://academy.hackthebox.com/storage/modules/143/psexec-action.png)

Una vez que ejecutamos el módulo psexec, nos lleva al directorio `system32` en el host de destino. Ejecutamos el comando `whoami` para verificar que llegamos al host como `SYSTEM`. Desde aquí, podemos realizar casi cualquier tarea en este host; desde enumeraciones adicionales hasta persistencia y movimiento lateral. Probemos otro módulo de Impacket: `wmiexec.py`.

### **wmiexec.py**

Wmiexec.py utiliza un shell semi interactivo donde los comandos se ejecutan a través [del Instrumental de administración de Windows](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-start-page) . No coloca ningún archivo ni ejecutable en el host de destino y genera menos registros que otros módulos. Después de conectarse, se ejecuta como el usuario administrador local con el que nos conectamos (esto puede ser menos obvio para alguien que busca una intrusión que ver al `SYSTEM` ejecutando muchos comandos). Este es un enfoque de ejecución más sigiloso en hosts que otras herramientas, pero aún así probablemente sería detectado por la mayoría de los sistemas antivirus y EDR modernos. Usaremos la misma cuenta que con psexec.py para acceder al host.

**Usando wmiexec.py**

```bash
wmiexec.py inlanefreight.local/wley:'transporter@4'@172.16.5.5  
```

![texto](https://academy.hackthebox.com/storage/modules/143/wmiexec-action.png)

Tenga en cuenta que este entorno de shell no es completamente interactivo, por lo que cada comando emitido ejecutará un nuevo `cmd.exe` desde WMI y ejecutará su comando. La desventaja de esto es que si un defensor vigilante verifica los registros de eventos y observa el ID de evento [4688: A new process has been created](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688) , verá un nuevo proceso creado para generar cmd.exe y emitir un comando. Esto no siempre es una actividad maliciosa ya que muchas organizaciones utilizan WMI para administrar computadoras, pero puede ser un indicio en una investigación.&#x20;

En la imagen de arriba, también es evidente que el proceso se está ejecutando bajo el contexto de usuario `wley` en el host, no como `SYSTEM`. Impacket es una herramienta inmensamente valiosa que tiene muchos casos de uso. Veremos muchas otras herramientas en el kit de herramientas de Impacket a lo largo del resto de este módulo. Como pentester que trabaja con hosts de Windows, esta herramienta siempre debe estar en nuestro arsenal.&#x20;

***

## <mark style="color:purple;">Windapsearch</mark>

[Windapsearch](https://github.com/ropnop/windapsearch) es otro script de Python útil que podemos usar para enumerar usuarios, grupos y computadoras de un dominio de Windows mediante consultas LDAP. En los ejemplos de esta sección está presente en el directorio `/opt/windapsearch/` del host de ataque.

**Windapsearch Ayuda**

```shell-session
afsh4ck@kali$ windapsearch.py -h

usage: windapsearch.py [-h] [-d DOMAIN] [--dc-ip DC_IP] [-u USER]
                       [-p PASSWORD] [--functionality] [-G] [-U] [-C]
                       [-m GROUP_NAME] [--da] [--admin-objects] [--user-spns]
                       [--unconstrained-users] [--unconstrained-computers]
                       [--gpos] [-s SEARCH_TERM] [-l DN]
                       [--custom CUSTOM_FILTER] [-r] [--attrs ATTRS] [--full]
                       [-o output_dir]

Script to perform Windows domain enumeration through LDAP queries to a Domain
Controller

optional arguments:
  -h, --help            show this help message and exit

Domain Options:
  -d DOMAIN, --domain DOMAIN
                        The FQDN of the domain (e.g. 'lab.example.com'). Only
                        needed if DC-IP not provided
  --dc-ip DC_IP         The IP address of a domain controller

Bind Options:
  Specify bind account. If not specified, anonymous bind will be attempted

  -u USER, --user USER  The full username with domain to bind with (e.g.
                        'ropnop@lab.example.com' or 'LAB\ropnop'
  -p PASSWORD, --password PASSWORD
                        Password to use. If not specified, will be prompted
                        for

Enumeration Options:
  Data to enumerate from LDAP

  --functionality       Enumerate Domain Functionality level. Possible through
                        anonymous bind
  -G, --groups          Enumerate all AD Groups
  -U, --users           Enumerate all AD Users
  -PU, --privileged-users
                        Enumerate All privileged AD Users. Performs recursive
                        lookups for nested members.
  -C, --computers       Enumerate all AD Computers

  <SNIP>
```

Tenemos varias opciones con Windapsearch para realizar una enumeración estándar (descargando usuarios, computadoras y grupos) y una enumeración más detallada. La flag `--da` (enumerar los miembros del grupo de administradores de dominio) y la flag `-PU` (buscar usuarios privilegiados). La flag `-PU` es interesante porque realizará una búsqueda recursiva de usuarios con membresía en grupos anidados.

### **Windapsearch - Administradores de dominio**

```shell-session
afsh4ck@kali$ python3 windapsearch.py --dc-ip 172.16.5.5 -u forend@inlanefreight.local -p Klmcargo2 --da

[+] Using Domain Controller at: 172.16.5.5
[+] Getting defaultNamingContext from Root DSE
[+]	Found: DC=INLANEFREIGHT,DC=LOCAL
[+] Attempting bind
[+]	...success! Binded as: 
[+]	 u:INLANEFREIGHT\forend
[+] Attempting to enumerate all Domain Admins
[+] Using DN: CN=Domain Admins,CN=Users.CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
[+]	Found 28 Domain Admins:

cn: Administrator
userPrincipalName: administrator@inlanefreight.local

cn: lab_adm

cn: Matthew Morgan
userPrincipalName: mmorgan@inlanefreight.local

<SNIP>
```

De los resultados del shell anterior, podemos ver que se enumeraron 28 usuarios del grupo `Administradores de dominio`. Tome nota de algunos usuarios que ya hemos visto antes y que pueden tener una contraseña hash o de texto sin formato como `wley`, `svc_qualys` y `lab_adm`.

Para identificar más usuarios potenciales, podemos ejecutar la herramienta con la flag `-PU` y verificar si hay usuarios con privilegios elevados que pueden haber pasado desapercibidos. Esta es una excelente verificación para generar informes, ya que es muy probable que informe al cliente sobre usuarios con privilegios excesivos debido a la membresía de un grupo anidado.

### **Windapsearch - Usuarios privilegiados**

```shell-session
afsh4ck@kali$ python3 windapsearch.py --dc-ip 172.16.5.5 -u forend@inlanefreight.local -p Klmcargo2 -PU

[+] Using Domain Controller at: 172.16.5.5
[+] Getting defaultNamingContext from Root DSE
[+]     Found: DC=INLANEFREIGHT,DC=LOCAL
[+] Attempting bind
[+]     ...success! Binded as:
[+]      u:INLANEFREIGHT\forend
[+] Attempting to enumerate all AD privileged users
[+] Using DN: CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
[+]     Found 28 nested users for group Domain Admins:

cn: Administrator
userPrincipalName: administrator@inlanefreight.local

cn: lab_adm

cn: Angela Dunn
userPrincipalName: adunn@inlanefreight.local

cn: Matthew Morgan
userPrincipalName: mmorgan@inlanefreight.local

cn: Dorothy Click
userPrincipalName: dclick@inlanefreight.local

<SNIP>

[+] Using DN: CN=Enterprise Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
[+]     Found 3 nested users for group Enterprise Admins:

cn: Administrator
userPrincipalName: administrator@inlanefreight.local

cn: lab_adm

cn: Sharepoint Admin
userPrincipalName: sp-admin@INLANEFREIGHT.LOCAL

<SNIP>
```

Notarás que realizó mutaciones contra nombres de grupos elevados comunes en diferentes idiomas. Este resultado ofrece un ejemplo de los peligros de la pertenencia a grupos anidados, y esto se volverá más evidente cuando trabajemos con gráficos de BloodHound para visualizar esto.

***

## <mark style="color:purple;">Bloodhound.py</mark>

Una vez que tenemos las credenciales de dominio, podemos ejecutar [BloodHound.py](https://github.com/fox-it/BloodHound.py) desde nuestro host de ataque Linux. BloodHound es una de las herramientas más impactantes, si no la más impactante, jamás lanzada para auditar la seguridad de Active Directory, y es enormemente beneficiosa para nosotros como Pentesters. Podemos tomar grandes cantidades de datos que llevarían mucho tiempo analizar y crear representaciones gráficas o "rutas de ataque" de adónde puede conducir el acceso con un usuario en particular.&#x20;

A menudo encontraremos fallas matizadas en un entorno de AD que se habrían pasado por alto sin la capacidad de ejecutar consultas con la herramienta GUI BloodHound y visualizar problemas. La herramienta usa [la teoría de grafos](https://en.wikipedia.org/wiki/Graph_theory) para representar visualmente las relaciones y descubrir rutas de ataque que habrían sido difíciles, o incluso imposibles, de detectar con otras herramientas. La herramienta consta de dos partes: el [SharpHound collector](https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors) escrito en C# para su uso en sistemas Windows, o para esta sección, el recopilador `BloodHound.py` (también conocido como `ingestor`) y la herramienta GUI [BloodHound](https://github.com/BloodHoundAD/BloodHound/releases) que nos permite cargar datos recopilados en forma de archivos JSON. Una vez cargados, podemos ejecutar varias consultas predefinidas o escribir consultas personalizadas utilizando [el lenguaje Cypher](https://blog.cptjesus.com/posts/introtocypher) . La herramienta recopila datos de AD, como usuarios, grupos, computadoras, membresía de grupos, GPO, ACL, confianzas de dominio, acceso de administrador local, sesiones de usuario, propiedades de computadora y usuario, acceso RDP, acceso WinRM, etc.

Inicialmente solo se lanzó con un recopilador de PowerShell, por lo que tuvo que ejecutarse desde un host de Windows. Finalmente, un miembro de la comunidad lanzó una adaptación de Python (que requiere Impacket, `ldap3` y `dnspython` ). Esto fue de gran ayuda durante las pruebas de penetración cuando tenemos credenciales de dominio válidas, pero no tenemos derechos para acceder a un host de Windows unido al dominio o no tenemos un host de ataque de Windows desde el cual ejecutar el recopilador SharpHound. Esto también nos ayuda a no tener que ejecutar el recopilador desde un host de dominio, lo que potencialmente podría bloquearse o activar alertas (aunque incluso ejecutarlo desde nuestro host de ataque probablemente activará alarmas en entornos bien protegidos).

Ejecutar `bloodhound-python -h` desde nuestro host de ataque Linux nos mostrará las opciones disponibles.

**Opciones de BloodHound.py**

```shell-session
afsh4ck@kali$ bloodhound-python -h

usage: bloodhound-python [-h] [-c COLLECTIONMETHOD] [-u USERNAME]
                         [-p PASSWORD] [-k] [--hashes HASHES] [-ns NAMESERVER]
                         [--dns-tcp] [--dns-timeout DNS_TIMEOUT] [-d DOMAIN]
                         [-dc HOST] [-gc HOST] [-w WORKERS] [-v]
                         [--disable-pooling] [--disable-autogc] [--zip]

Python based ingestor for BloodHound
For help or reporting issues, visit https://github.com/Fox-IT/BloodHound.py

optional arguments:
  -h, --help            show this help message and exit
  -c COLLECTIONMETHOD, --collectionmethod COLLECTIONMETHOD
                        Which information to collect. Supported: Group,
                        LocalAdmin, Session, Trusts, Default (all previous),
                        DCOnly (no computer connections), DCOM, RDP,PSRemote,
                        LoggedOn, ObjectProps, ACL, All (all except LoggedOn).
                        You can specify more than one by separating them with
                        a comma. (default: Default)
  -u USERNAME, --username USERNAME
                        Username. Format: username[@domain]; If the domain is
                        unspecified, the current domain is used.
  -p PASSWORD, --password PASSWORD
                        Password

  <SNIP>
```

Como podemos ver, la herramienta acepta varios métodos de recopilación con el indicador `-c` o `--collectionmethod`. Podemos recuperar datos específicos, como sesiones de usuario, usuarios y grupos, propiedades de objetos, ACLS o seleccionar `all` para recopilar la mayor cantidad de datos posible. Ejecutémosla de esta manera.

### **Ejecutar BloodHound.py**

```shell-session
afsh4ck@kali$ sudo bloodhound-python -u 'forend' -p 'Klmcargo2' -ns 172.16.5.5 -d inlanefreight.local -c all 

INFO: Found AD domain: inlanefreight.local
INFO: Connecting to LDAP server: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
INFO: Found 1 domains
INFO: Found 2 domains in the forest
INFO: Found 564 computers
INFO: Connecting to LDAP server: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
INFO: Found 2951 users
INFO: Connecting to GC LDAP server: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
INFO: Found 183 groups
INFO: Found 2 trusts
INFO: Starting computer enumeration with 10 workers

<SNIP>
```

El comando anterior ejecutó Bloodhound.py con el usuario `forend`. Especificamos nuestro servidor de nombres como el controlador de dominio con el `-ns`indicador y el dominio, INLANEFREIGHt.LOCAL con la flag `-d` . La flag `-c all` le indicó a la herramienta que ejecutara todas las comprobaciones. Una vez que finalice el script, veremos los archivos de salida en el directorio de trabajo actual en el formato `<date_object.json>`.

**Visualización de los resultados**

```shell-session
afsh4ck@kali$ ls

20220307163102_computers.json  20220307163102_domains.json  20220307163102_groups.json  20220307163102_users.json  
```

### **Subir el archivo Zip a la GUI de BloodHound**

Luego podríamos escribir `sudo neo4j start` para iniciar el servicio [neo4j](https://neo4j.com/) , activando la base de datos en la que cargaremos los datos y también ejecutaremos consultas Cypher.

A continuación, podemos escribir `bloodhound` desde nuestro host de ataque de Linux cuando iniciamos sesión usando `freerdp` para iniciar la aplicación GUI BloodHound y cargar los datos. Las credenciales se completan previamente en el host de ataque de Linux, pero si por alguna razón se muestra un mensaje de credencial, use:

* `user == neo4j`/ `pass == HTB_@cademy_stdnt!`

Una vez hecho todo lo anterior, deberíamos tener la herramienta GUI de BloodHound cargada con una pizarra en blanco. Ahora necesitamos cargar los datos. Podemos cargar cada archivo JSON uno por uno o comprimirlos primero con un comando como `zip -r domain.zip *.json` y cargar el archivo Zip. Esto lo hacemos haciendo clic en el botón `Upload Data` en el lado derecho de la ventana (flecha verde). Cuando aparezca la ventana del explorador de archivos para seleccionar un archivo, elija el archivo zip (o cada archivo JSON) (flecha roja) y presione `Open`.

**Subiendo el archivo zip**

![imagen](https://academy.hackthebox.com/storage/modules/143/bh-injest.png)

Ahora que los datos están cargados, podemos usar la pestaña Análisis para ejecutar consultas en la base de datos. Estas consultas pueden ser personalizadas y específicas para lo que usted decida mediante [consultas Cypher personalizadas](https://hausec.com/2019/09/09/bloodhound-cypher-cheatsheet/) . Hay muchas hojas de trucos excelentes que nos ayudarán aquí. Analizaremos más las consultas Cypher personalizadas en una sección posterior. Como se ve a continuación, podemos usar las consultas integradas de búsqueda de ruta en la pestaña `Analysis` en el lado izquierdo de la ventana.

**Buscando relaciones**

![imagen](https://academy.hackthebox.com/storage/modules/143/bh-analysis.png)

La consulta elegida para producir el mapa anterior fue `Find Shortest Paths To Domain Admins`. Nos dará cualquier ruta lógica que encuentre a través de usuarios/grupos/hosts/ACL/GPO, etc., relaciones que probablemente nos permitirán escalar a privilegios de Administrador de dominio o equivalentes. Esto será de gran ayuda a la hora de planificar nuestros próximos pasos para el movimiento lateral a través de la red.&#x20;

Tómate un tiempo para experimentar con las diversas funciones: mira la pestaña  `Database Info` después de cargar los datos, busque un nodo como `Domain Users` y, desplácese por todas las opciones debajo de la pestaña `Node Info`, consulta las consultas prediseñadas debajo de la pestaña `Analysis`, muchas de las cuales son potente y puede encontrar rápidamente varias formas de adquisición de dominio. Finalmente, experimente con algunas consultas Cypher personalizadas seleccionando algunas interesantes de la hoja de trucos Cypher vinculada arriba, pegándolas en el cuadro `Raw Query` en la parte inferior y presionando Enter. También puedes jugar con el menú `Settings` haciendo clic en el ícono de ajustes en el lado derecho de la pantalla y ajustando cómo se muestran los nodos y bordes, habilitando el modo de depuración de consultas y habilitando el modo oscuro. A lo largo del resto de este módulo, usaremos BloodHound de varias maneras, pero para un estudio específico sobre la herramienta BloodHound, consulte el módulo [BloodHound](/ethical-hacking-cheatsheet/active-directory/active-directory/bloodhound.md)

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.114.51 (ACADEMY-EA-ATTACK01)
Usuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
Domain Controller IP: 172.16.5.5
```

Para la enumeración del dominio INLANEFREIGHT.LOCAL utilizando las herramientas instaladas en el host Parrot Linux ATTACK01, utilizaremos las siguientes credenciales:&#x20;

```
User = forendy 
Pass = Klmcargo2
```

### Pregunta 1

¿Qué usuario de AD tiene un RID igual a Decimal 1170?

1. Vamos a crear una Session SMB Null con rpcclient

```
rpcclient -U "" -N 172.16.5.5
```

```
┌─[htb-student@ea-attack01]─[~]
└──╼ $rpcclient -U "" -N 172.16.5.5

rpcclient $> queryuser 1170
	User Name   :	mmorgan
	Full Name   :	Matthew Morgan
	Home Drive  :	
	Dir Drive   :	
	Profile Path:	
	Logon Script:	
	Description :	
	Workstations:	
	Comment     :	
	Remote Dial :
	Logon Time               :	Thu, 10 Mar 2022 14:48:06 EST
	Logoff Time              :	Wed, 31 Dec 1969 19:00:00 EST
	Kickoff Time             :	Wed, 31 Dec 1969 19:00:00 EST
	Password last set Time   :	Tue, 05 Apr 2022 15:34:55 EDT
	Password can change Time :	Wed, 06 Apr 2022 15:34:55 EDT
	Password must change Time:	Wed, 13 Sep 30828 22:48:05 EDT
	unknown_2[0..31]...
	user_rid :	0x492
	group_rid:	0x201
	acb_info :	0x00010210
	fields_present:	0x00ffffff
	logon_divs:	168
	bad_password_count:	0x00000000
	logon_count:	0x00000018
	padding1[0..7]...
	logon_hrs[0..21]...
```

### Pregunta 2

¿Cuál es el número de miembros del grupo "`Domain Admins`"?&#x20;

```
┌─[✗]─[htb-student@ea-attack01]─[~]
└──╼ $sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 --groups
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\forend:Klmcargo2 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] Enumerated domain group(s)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Administrators                           membercount: 3
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Users                                    membercount: 4
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Guests                                   membercount: 2
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Print Operators                          membercount: 0
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Backup Operators                         membercount: 1
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Replicator                               membercount: 0
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Remote Desktop Users                     membercount: 0
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Domain Admins                            membercount: 19
<------SNIP------>
```

Concretamente vemos que hay `19 usuarios` en el grupo Domain Admins.

***

Experimentamos con varias herramientas nuevas para la enumeración de dominios desde un host Linux. La siguiente sección cubrirá varias herramientas más que podemos usar desde un host Windows unido a un dominio. Como nota rápida, si aún no has revisado el [proyecto WADComs](https://wadcoms.github.io/) , definitivamente deberías hacerlo. Es una hoja de trucos interactiva para muchas de las herramientas que cubriremos (y más) en este módulo. Es de gran ayuda cuando no puedes recordar la sintaxis exacta de los comandos o estás probando una herramienta por primera vez. ¡Vale la pena agregarla a favoritos e incluso [contribuir](https://wadcoms.github.io/contribute/) a ella!

En la siguiente sección, cubriremos la ejecución del recopilador SharpHound desde un host de Windows unido a un dominio y analizaremos algunos ejemplos de trabajo con datos en la GUI de BloodHound.
