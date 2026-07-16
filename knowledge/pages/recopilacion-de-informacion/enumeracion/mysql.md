
# MySQL

## <mark style="color:purple;">Cómo funciona</mark>

Una base de datos es simplemente una colección estructurada de datos organizados para su fácil uso y recuperación. El sistema de base de datos puede procesar rápidamente grandes cantidades de datos con un alto rendimiento. Dentro de la base de datos, el almacenamiento de datos se realiza de manera que ocupe el menor espacio posible. La base de datos se controla utilizando el [lenguaje de base de datos SQL](https://www.w3schools.com/sql/sql_intro.asp) .&#x20;

MySQL funciona según el principio de `cliente-servidor` y consta de un servidor MySQL y uno o más clientes MySQL. El servidor MySQL es el sistema de gestión de bases de datos real. Se encarga del almacenamiento y distribución de datos. Los datos se almacenan en tablas con diferentes columnas, filas y tipos de datos. Estas bases de datos suelen almacenarse en un único archivo con la extensión `.sql`, por ejemplo, como `wordpress.sql`.

### **Clientes MySQL**

Los clientes MySQL pueden recuperar y editar los datos mediante consultas estructuradas al motor de base de datos. La inserción, eliminación, modificación y recuperación de datos se realiza utilizando el lenguaje de base de datos SQL. Por lo tanto, MySQL es adecuado para gestionar muchas bases de datos diferentes a las que los clientes pueden enviar múltiples consultas simultáneamente. Dependiendo del uso de la base de datos, el acceso es posible a través de una red interna o de la Internet pública.

Uno de los mejores ejemplos de uso de bases de datos es el CMS [WordPress](/ethical-hacking-cheatsheet/recopilacion-de-informacion/hacking-en-cms.md). WordPress almacena todas las publicaciones, nombres de usuario y contraseñas creados en su propia base de datos, a la que solo se puede acceder desde el host local. Sin embargo, como se explica con más detalle en el módulo [Introducción a las aplicaciones web](https://academy.hackthebox.com/course/preview/introduction-to-web-applications) , existen estructuras de bases de datos que también se distribuyen en varios servidores.

### **Bases de datos MySQL**

MySQL es ideal para aplicaciones como `webs dinámicas`, donde la sintaxis eficiente y la alta velocidad de respuesta son esenciales. A menudo se combina con un sistema operativo Linux, PHP y un servidor web Apache y también se conoce en esta combinación como [LAMP](https://en.wikipedia.org/wiki/LAMP_\(software_bundle\)) (Linux, Apache, MySQL, PHP), o cuando se usa Nginx, como [LEMP](https://lemp.io/) . En un alojamiento web con base de datos MySQL, esto sirve como una instancia central en la que se almacena el contenido requerido por los scripts PHP. Entre estos están:

|                           |                         |                        |             |
| ------------------------- | ----------------------- | ---------------------- | ----------- |
| Encabezados               | Textos                  | meta etiquetas         | Formularios |
| Clientes                  | Nombres de usuario      | Administradores        | Moderadores |
| Correos electrónicos      | Información del usuario | Permisos               | Contraseñas |
| Enlaces externos/internos | Enlaces a archivos      | Contenidos específicos | Valores     |

MySQL puede almacenar datos confidenciales, como contraseñas, en formato de texto sin formato; sin embargo, generalmente están cifrados de antemano mediante scripts PHP utilizando métodos seguros como [One-Way-Encryption](https://en.citizendium.org/wiki/One-way_encryption) .

### **Vulnerabilidades - SQL Injections**

{% content-ref url="/pages/lIoNr7ttmkn5RkFA9FXK" %}
[SQL Injection](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/sql-injection.md)
{% endcontent-ref %}

Una base de datos MySQL traduce los comandos internamente en código ejecutable y realiza las acciones solicitadas. La aplicación web informa al usuario si se produce algún error durante el procesamiento, que puede provocar diversas[ SQL Injections](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/sql-injection.md). A menudo, estas vulnerabilidades contienen información importante y confirman, entre otras cosas, que la aplicación web interactúa con la base de datos de una manera diferente a la prevista por los desarrolladores.

La aplicación web envía la información generada al cliente si los datos se procesan correctamente. Esta información pueden ser extractos de datos de una tabla o registros necesarios para su posterior procesamiento con inicios de sesión, funciones de búsqueda, etc. Los comandos SQL pueden mostrar, modificar, agregar o eliminar filas en las tablas. Además, SQL también puede cambiar la estructura de tablas, crear o eliminar relaciones e índices y administrar usuarios.

### MariaDB

MariaDB, que a menudo está relacionado con MySQL, es una bifurcación del código MySQL original. Esto se debe a que el desarrollador jefe de MySQL abandonó la empresa `MySQL AB` después de que ésta fue adquirida por `Oracle` y desarrolló otro sistema de gestión de bases de datos SQL de código abierto basado en el código fuente de MySQL y lo llamó MariaDB.

***

## <mark style="color:purple;">Configuración predeterminada</mark>

La gestión de bases de datos SQL y sus configuraciones es un tema amplio. Es tan grande que profesiones enteras, como por ejemplo el `Administrador de Bases de Datos`, se ocupan casi exclusivamente de bases de datos. Estas estructuras crecen rápidamente y su planificación puede resultar complicada.&#x20;

Entre otras cosas, la gestión de bases de datos es una competencia básica para `Desarrolladores de Software` pero también para `Cybersecurity Analysts`. Cubrir esta área completamente iría más allá del alcance de este módulo. Por lo tanto, recomiendo configurar una instancia de MySQL/MariaDB para experimentar con las distintas configuraciones y comprender mejor la funcionalidad disponible y las opciones de configuración. Echemos un vistazo a la configuración predeterminada de MySQL.

```bash
afsh4ck$ sudo apt install mysql-server -y
afsh4ck$ cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep -v "#" | sed -r '/^\s*$/d'

[client]
port		= 3306
socket		= /var/run/mysqld/mysqld.sock

[mysqld_safe]
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
nice		= 0

[mysqld]
skip-host-cache
skip-name-resolve
user		= mysql
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
port		= 3306
basedir		= /usr
datadir		= /var/lib/mysql
tmpdir		= /tmp
lc-messages-dir	= /usr/share/mysql
explicit_defaults_for_timestamp

symbolic-links=0

!includedir /etc/mysql/conf.d/
```

***

## <mark style="color:purple;">Configuraciones peligrosas</mark>

Muchas cosas se pueden configurar mal con MySQL. Podemos mirar con más detalle la [referencia de MySQL](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html) para determinar qué opciones se pueden realizar en la configuración del servidor. Las principales opciones relevantes para la seguridad son:

<table data-header-hidden><thead><tr><th width="224"></th><th></th></tr></thead><tbody><tr><td><strong>Ajustes</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>user</code></td><td>Establece con qué usuario se ejecutará el servicio MySQL.</td></tr><tr><td><code>password</code></td><td>Establece la contraseña para el usuario de MySQL.</td></tr><tr><td><code>admin_address</code></td><td>La dirección IP en la que escuchar las conexiones TCP/IP en la interfaz de red administrativa.</td></tr><tr><td><code>debug</code></td><td>Esta variable indica la configuración de depuración actual.</td></tr><tr><td><code>sql_warnings</code></td><td>Esta variable controla si las declaraciones INSERT de una sola fila producen una cadena de información si se producen advertencias.</td></tr><tr><td><code>secure_file_priv</code></td><td>Esta variable se utiliza para limitar el efecto de las operaciones de importación y exportación de datos.</td></tr></tbody></table>

Los ajustes `user`, `password`y `admin_address` son relevantes para la seguridad porque las entradas se realizan en texto plano. A menudo, los derechos para el archivo de configuración del servidor MySQL no están asignados correctamente. Si obtenemos otra forma de leer archivos o incluso un shell, podemos ver el archivo y el nombre de usuario y contraseña del servidor MySQL. Supongamos que no existen otras medidas de seguridad para evitar el acceso no autorizado. En ese caso, se puede ver e incluso editar toda la base de datos y toda la información, direcciones de correo electrónico, contraseñas y datos personales de los clientes existentes.

Las configuraciones `debug` y `sql_warnings` brindan información detallada en caso de errores, que son esenciales para el administrador pero que otros no deben ver. Esta información a menudo contiene contenido confidencial, que podría detectarse mediante prueba y error para identificar otras posibilidades de ataque. Estos mensajes de error suelen mostrarse directamente en las aplicaciones web. En consecuencia, las inyecciones de SQL podrían manipularse incluso para que el servidor MySQL ejecute comandos del sistema. Esto se analiza y muestra en el módulo de [SQL Injections](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/sql-injection.md).

***

## <mark style="color:purple;">Enumeración del servicio</mark>

Hay muchas razones por las que se puede acceder a un servidor MySQL desde una red externa. Sin embargo, está lejos de ser una de las mejores prácticas y siempre podemos encontrar bases de datos a las que podemos acceder. A menudo, estas configuraciones solo estaban destinadas a ser temporales, pero los administradores las olvidaban. Esta configuración del servidor también podría usarse como solución alternativa debido a un problema técnico. Por lo general, el servidor MySQL se ejecuta `TCP port 3306`y podemos escanear este puerto `Nmap`para obtener información más detallada.

### **Nmap - Escaneando MySQL**

```bash
afsh4ck$ sudo nmap 10.129.14.128 -sV -sC -p3306 --script mysql*

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-21 00:53 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00021s latency).

PORT     STATE SERVICE     VERSION
3306/tcp open  nagios-nsca Nagios NSCA
| mysql-brute: 
|   Accounts: 
|     root:<empty> - Valid credentials
|_  Statistics: Performed 45010 guesses in 5 seconds, average tps: 9002.0
|_mysql-databases: ERROR: Script execution failed (use -d to debug)
|_mysql-dump-hashes: ERROR: Script execution failed (use -d to debug)
| mysql-empty-password: 
|_  root account has empty password
| mysql-enum: 
|   Valid usernames: 
|     root:<empty> - Valid credentials
|     netadmin:<empty> - Valid credentials
|     guest:<empty> - Valid credentials
|     user:<empty> - Valid credentials
|     web:<empty> - Valid credentials
|     sysadmin:<empty> - Valid credentials
|     administrator:<empty> - Valid credentials
|     webadmin:<empty> - Valid credentials
|     admin:<empty> - Valid credentials
|     test:<empty> - Valid credentials
|_  Statistics: Performed 10 guesses in 1 seconds, average tps: 10.0
| mysql-info: 
|   Protocol: 10
|   Version: 8.0.26-0ubuntu0.20.04.1
|   Thread ID: 13
|   Capabilities flags: 65535
|   Some Capabilities: SupportsLoadDataLocal, SupportsTransactions, Speaks41ProtocolOld, LongPassword, DontAllowDatabaseTableColumn, Support41Auth, IgnoreSigpipes, SwitchToSSLAfterHandshake, FoundRows, InteractiveClient, Speaks41ProtocolNew, ConnectWithDatabase, IgnoreSpaceBeforeParenthesis, LongColumnFlag, SupportsCompression, ODBCClient, SupportsMultipleStatments, SupportsAuthPlugins, SupportsMultipleResults
|   Status: Autocommit
|   Salt: YTSgMfqvx\x0F\x7F\x16\&\x1EAeK>0
|_  Auth Plugin Name: caching_sha2_password
|_mysql-users: ERROR: Script execution failed (use -d to debug)
|_mysql-variables: ERROR: Script execution failed (use -d to debug)
|_mysql-vuln-cve2012-2122: ERROR: Script execution failed (use -d to debug)
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.21 seconds
```

Como ocurre con todos nuestros escaneos, debemos tener cuidado con los resultados y confirmar manualmente la información obtenida porque parte de la información podría resultar un falso positivo. Este escaneo anterior es un excelente ejemplo de esto, ya que sabemos con certeza que el servidor MySQL de destino no usa una contraseña vacía para el usuario `root`, sino una contraseña fija. Podemos probar esto con el siguiente comando:

### **Interacción con el servidor MySQL**

```bash
afsh4ck$ mysql -u root -h 10.129.14.132

ERROR 1045 (28000): Access denied for user 'root'@'10.129.14.1' (using password: NO)
```

Por ejemplo, si utilizamos una contraseña que hemos adivinado o encontrado durante nuestra investigación, podremos iniciar sesión en el servidor MySQL y ejecutar algunos comandos.

```bash
afsh4ck$ mysql -u root -pP4SSw0rd -h 10.129.14.128

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 150165
Server version: 8.0.27-0ubuntu0.20.04.1 (Ubuntu)                                                         
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.                                     
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.                           
      
MySQL [(none)]> show databases;                                                                          
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.006 sec)


MySQL [(none)]> select version();
+-------------------------+
| version()               |
+-------------------------+
| 8.0.27-0ubuntu0.20.04.1 |
+-------------------------+
1 row in set (0.001 sec)


MySQL [(none)]> use mysql;
MySQL [mysql]> show tables;
+------------------------------------------------------+
| Tables_in_mysql                                      |
+------------------------------------------------------+
| columns_priv                                         |
| component                                            |
| db                                                   |
| default_roles                                        |
| engine_cost                                          |
| func                                                 |
| general_log                                          |
| global_grants                                        |
| gtid_executed                                        |
| help_category                                        |
| help_keyword                                         |
| help_relation                                        |
| help_topic                                           |
| innodb_index_stats                                   |
| innodb_table_stats                                   |
| password_history                                     |
...SNIP...
| user                                                 |
+------------------------------------------------------+
37 rows in set (0.002 sec)
```

Si miramos las bases de datos existentes, veremos que ya existen varias. Las bases de datos más importantes para el servidor MySQL son `system schema`( `sys`) y `information schema`( `information_schema`). El esquema del sistema contiene tablas, información y metadatos necesarios para la gestión. Puede encontrar más información sobre esta base de datos en el [manual de referencia](https://dev.mysql.com/doc/refman/8.0/en/system-schema.html#:~:text=The%20mysql%20schema%20is%20the,used%20for%20other%20operational%20purposes) de MySQL.

```bash
mysql> use sys;
mysql> show tables;  

+-----------------------------------------------+
| Tables_in_sys                                 |
+-----------------------------------------------+
| host_summary                                  |
| host_summary_by_file_io                       |
| host_summary_by_file_io_type                  |
| host_summary_by_stages                        |
| host_summary_by_statement_latency             |
| host_summary_by_statement_type                |
| innodb_buffer_stats_by_schema                 |
| innodb_buffer_stats_by_table                  |
| innodb_lock_waits                             |
| io_by_thread_by_latency                       |
...SNIP...
| x$waits_global_by_latency                     |
+-----------------------------------------------+


mysql> select host, unique_users from host_summary;

+-------------+--------------+                   
| host        | unique_users |                   
+-------------+--------------+                   
| 10.129.14.1 |            1 |                   
| localhost   |            2 |                   
+-------------+--------------+                   
2 rows in set (0,01 sec)  
```

También es `information schema`una base de datos que contiene metadatos. Sin embargo, estos metadatos se recuperan principalmente de la `system schema`base de datos. La razón de la existencia de estos dos es el estándar ANSI/ISO que se ha establecido. `System schema`es un catálogo del sistema de Microsoft para servidores SQL y contiene mucha más información que el archivo `information schema`.

### Comandos MySQL

Algunos de los comandos que debemos recordar y anotar para trabajar con bases de datos MySQL se describen a continuación en la tabla.

<table data-header-hidden><thead><tr><th width="335"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>mysql -u &#x3C;user> -p&#x3C;password> -h &#x3C;IP address></code></td><td>Conéctese al servidor MySQL. <strong>No</strong> debe haber un espacio entre el indicador '-p' y la contraseña.</td></tr><tr><td><code>show databases;</code></td><td>Mostrar todas las bases de datos.</td></tr><tr><td><code>use &#x3C;database>;</code></td><td>Seleccione una de las bases de datos existentes.</td></tr><tr><td><code>show tables;</code></td><td>Mostrar todas las tablas disponibles en la base de datos seleccionada.</td></tr><tr><td><code>show columns from &#x3C;table>;</code></td><td>Mostrar todas las columnas de la base de datos seleccionada.</td></tr><tr><td><code>select * from &#x3C;table>;</code></td><td>Muestra todo en la tabla deseada.</td></tr><tr><td><code>select * from &#x3C;table> where &#x3C;column> = "&#x3C;string>";</code></td><td>Buscar un <code>string</code> en la tabla deseada.</td></tr></tbody></table>

Debemos saber interactuar con diferentes bases de datos. Por lo tanto, recomendamos instalar y configurar un servidor MySQL en una de nuestras máquinas virtuales para experimentar. También hay una sección [de problemas de seguridad](https://dev.mysql.com/doc/refman/8.0/en/general-security-issues.html) ampliamente cubierta en el manual de referencia que cubre las mejores prácticas para proteger los servidores MySQL. Deberíamos usar esto al configurar nuestro servidor MySQL para comprender mejor por qué algo podría no funcionar.
