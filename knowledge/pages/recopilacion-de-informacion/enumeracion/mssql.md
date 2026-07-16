
# MSSQL

## <mark style="color:purple;">Cómo funciona</mark>

A diferencia de MySQL, que analizamos en la última sección, MSSQL es de código cerrado y fue escrito inicialmente para ejecutarse en sistemas operativos Windows. Es popular entre los administradores y desarrolladores de bases de datos cuando crean aplicaciones que se ejecutan en el marco .NET de Microsoft debido a su sólido soporte nativo para .NET. Hay versiones de MSSQL que se ejecutan en Linux y MacOS, pero es más probable que nos encontremos con instancias de MSSQL en objetivos que ejecutan Windows.

### **Clientes MSSQL**

[SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15) ( `SSMS`) viene como una característica que se puede instalar con el paquete de instalación de MSSQL o se puede descargar e instalar por separado. Normalmente se instala en el servidor para la configuración inicial y la gestión a largo plazo de las bases de datos por parte de los administradores.&#x20;

Ten en cuenta que, dado que SSMS es una aplicación del lado del cliente, se puede instalar y utilizar en cualquier sistema desde el que un administrador o desarrollador planee administrar la base de datos. No sólo existe en el servidor que aloja la base de datos. Esto quiere decir que podríamos encontrarnos con un sistema vulnerable con SSMS con credenciales guardadas que nos permitan conectarnos a la base de datos. La siguiente imagen muestra SSMS en acción.

![SSMS](https://academy.hackthebox.com/storage/modules/112/ssms.png)

Se pueden utilizar muchos otros clientes para acceder a una base de datos que se ejecuta en MSSQL. Incluyendo pero no limitado a:

|                                                                                         |                                                                                                                            |                                       |                                         |                                                                                                              |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [mssql-cli](https://docs.microsoft.com/en-us/sql/tools/mssql-cli?view=sql-server-ver15) | [PowerShell del servidor SQL](https://docs.microsoft.com/en-us/sql/powershell/sql-server-powershell?view=sql-server-ver15) | [heidisql](https://www.heidisql.com/) | [SQLPro](https://www.macsqlclient.com/) | [mssqlclient.py de Impacket](https://github.com/SecureAuthCorp/impacket/blob/master/examples/mssqlclient.py) |

De los clientes MSSQL enumerados anteriormente, los pentesters pueden encontrar `mssqlclient.py` de Impacket como el más útil debido a que el proyecto Impacket de SecureAuthCorp está presente en muchas distribuciones de pentesting durante la instalación. Para saber si el cliente está ubicado en nuestro host y dónde, podemos usar el siguiente comando:

```bash
afsh4ck$ locate mssqlclient

/usr/bin/impacket-mssqlclient
/usr/share/doc/python3-impacket/examples/mssqlclient.py
```

### **Bases de datos MSSQL**

MSSQL tiene bases de datos del sistema predeterminadas que pueden ayudarnos a comprender la estructura de todas las bases de datos que pueden estar alojadas en un servidor de destino. Aquí están las bases de datos predeterminadas y una breve descripción de cada una:

<table data-header-hidden><thead><tr><th width="234"></th><th></th></tr></thead><tbody><tr><td>Base de datos del sistema predeterminada</td><td>Descripción</td></tr><tr><td><code>master</code></td><td>Realiza un seguimiento de toda la información del sistema para una instancia de servidor SQL</td></tr><tr><td><code>model</code></td><td>Base de datos de plantilla que actúa como estructura para cada nueva base de datos creada. Cualquier configuración modificada en la base de datos del modelo se reflejará en cualquier base de datos nueva creada después de los cambios en la base de datos del modelo.</td></tr><tr><td><code>msdb</code></td><td>El Agente SQL Server utiliza esta base de datos para programar trabajos y alertas</td></tr><tr><td><code>tempdb</code></td><td>Almacena objetos temporales</td></tr><tr><td><code>resource</code></td><td>Base de datos de solo lectura que contiene objetos del sistema incluidos con el servidor SQL</td></tr></tbody></table>

Fuente de la tabla: [Bases de datos del sistema Microsoft Doc](https://docs.microsoft.com/en-us/sql/relational-databases/databases/system-databases?view=sql-server-ver15)

***

### Configuración predeterminada

Cuando un administrador instala y configura inicialmente MSSQL para que sea accesible desde la red, es probable que el servicio SQL se ejecute como archivo `NT SERVICE\MSSQLSERVER`. Es posible conectarse desde el lado del cliente a través de la autenticación de Windows y, de forma predeterminada, no se aplica el cifrado al intentar conectarse.

![SSMS](https://academy.hackthebox.com/storage/modules/112/auth.png)

La autenticación configurada en `Windows Authentication`significa que el sistema operativo Windows subyacente procesará la solicitud de inicio de sesión y utilizará la base de datos SAM local o el controlador de dominio (que aloja Active Directory) antes de permitir la conectividad con el sistema de administración de la base de datos. El uso de Active Directory puede ser ideal para auditar la actividad y controlar el acceso en un entorno Windows, pero si una cuenta se ve comprometida, podría provocar una escalada de privilegios y un movimiento lateral en un entorno de dominio Windows. Al igual que con cualquier sistema operativo, servicio, función de servidor o aplicación, puede resultar beneficioso configurarlo en una máquina virtual desde la instalación hasta la configuración para comprender todas las configuraciones predeterminadas y los posibles errores que podría cometer el administrador.

***

## <mark style="color:purple;">Configuraciones peligrosas</mark>

Puede resultar beneficioso colocarnos en la perspectiva de un administrador de TI cuando tenemos un contrato. Esta mentalidad puede ayudarnos a recordar buscar varias configuraciones que un administrador pueda haber configurado mal o de manera peligrosa. Un día de trabajo en TI puede ser bastante ajetreado, con muchos proyectos diferentes sucediendo simultáneamente y la presión de desempeñarse con velocidad y precisión siendo una realidad en muchas organizaciones, se pueden cometer errores fácilmente. Sólo hace falta un pequeño error de configuración que podría comprometer un servidor o servicio crítico en la red. Esto se aplica a casi todos los servicios de red y funciones de servidor que se pueden configurar, incluido MSSQL.

Esta no es una lista extensa porque hay innumerables formas en que los administradores pueden configurar las bases de datos MSSQL según las necesidades de sus respectivas organizaciones. Podríamos beneficiarnos al investigar lo siguiente:

* Los clientes MSSQL no utilizan cifrado para conectarse al servidor MSSQL
* El uso de certificados autofirmados cuando se utiliza cifrado. Es posible falsificar certificados autofirmados
* El uso de [tuberías con nombre.](https://docs.microsoft.com/en-us/sql/tools/configuration-manager/named-pipes-properties?view=sql-server-ver15)
* Credenciales `sa` débiles y predeterminadas . Los administradores pueden olvidarse de desactivar esta cuenta.

***

## <mark style="color:purple;">Enumeración del servicio</mark>

Hay muchas maneras en que podemos abordar el seguimiento del servicio MSSQL; cuanto más específicos seamos con nuestros escaneos, más información útil podremos recopilar. NMAP tiene scripts mssql predeterminados que se pueden usar para apuntar al puerto tcp predeterminado `1433` en el que escucha MSSQL.

El escaneo NMAP programado a continuación nos proporciona información útil. Podemos ver `hostname`, `database instance name`, `software version of MSSQL`y `named pipes are enabled`. Nos beneficiaremos añadiendo estos descubrimientos a nuestras notas.

### **Nmap - Secuencias de comandos NMAP MSSQL**

```bash
afsh4ck$ sudo nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 10.129.201.248

Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-08 09:40 EST
Nmap scan report for 10.129.201.248
Host is up (0.15s latency).

PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-ntlm-info: 
|   Target_Name: SQL-01
|   NetBIOS_Domain_Name: SQL-01
|   NetBIOS_Computer_Name: SQL-01
|   DNS_Domain_Name: SQL-01
|   DNS_Computer_Name: SQL-01
|_  Product_Version: 10.0.17763

Host script results:
| ms-sql-dac: 
|_  Instance: MSSQLSERVER; DAC port: 1434 (connection failed)
| ms-sql-info: 
|   Windows server name: SQL-01
|   10.129.201.248\MSSQLSERVER: 
|     Instance name: MSSQLSERVER
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|     TCP port: 1433
|     Named pipe: \\10.129.201.248\pipe\sql\query
|_    Clustered: false

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.52 seconds
```

También podemos usar Metasploit para ejecutar un escáner auxiliar llamado `mssql_ping`que escaneará el servicio MSSQL y proporcionará información útil en nuestro proceso de huella.

### **Ping de MSSQL en Metasploit**

```bash
msf6 auxiliary(scanner/mssql/mssql_ping) > set rhosts 10.129.201.248

rhosts => 10.129.201.248


msf6 auxiliary(scanner/mssql/mssql_ping) > run

[*] 10.129.201.248:       - SQL Server information for 10.129.201.248:
[+] 10.129.201.248:       -    ServerName      = SQL-01
[+] 10.129.201.248:       -    InstanceName    = MSSQLSERVER
[+] 10.129.201.248:       -    IsClustered     = No
[+] 10.129.201.248:       -    Version         = 15.0.2000.5
[+] 10.129.201.248:       -    tcp             = 1433
[+] 10.129.201.248:       -    np              = \\SQL-01\pipe\sql\query
[*] 10.129.201.248:       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

### **Conexión con Mssqlclient.py**

Si podemos adivinar u obtener acceso a las credenciales, esto nos permite conectarnos de forma remota al servidor MSSQL y comenzar a interactuar con bases de datos usando T-SQL ( `Transact-SQL`). La autenticación con MSSQL nos permitirá interactuar directamente con las bases de datos a través del SQL Database Engine. Desde un equipo de atacante, podemos usar `mssqlclient.py` de `Impacket` para conectarnos como se ve en el siguiente resultado. Una vez conectado al servidor, puede ser bueno tener una idea del terreno y enumerar las bases de datos presentes en el sistema.

<table data-header-hidden><thead><tr><th width="360"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td>impacket-mssqlclient <code>&#x3C;user>@&#x3C;FQDN/IP> -windows-auth</code></td><td>Inicia sesión en el servidor MSSQL utilizando la autenticación de Windows.</td></tr></tbody></table>

```shell-session
afsh4ck@kali$ impacket-mssqlclient Administrator@10.129.201.248 -windows-auth

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(SQL-01): Line 1: Changed database context to 'master'.
[*] INFO(SQL-01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands

SQL> select name from sys.databases

name                                                                                                                               

--------------------------------------------------------------------------------

master                                  
tempdb                                 
model                                                                                                                              
Transactions    
```
