
# PostgreSQL

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que vamos a comprometer la base de datos del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">**Conexión a PostgreSQL por terminal**</mark>

```bash
psql -U nombre_usuario -d nombre_base_datos -h localhost -p puerto
```

* `-U nombre_usuario`: Especifica el nombre de usuario de PostgreSQL.
* `-d nombre_base_datos`: Especifica el nombre de la base de datos a la que deseas conectarte.
* `-h localhost`: Especifica la dirección del host de PostgreSQL (en este caso, localhost).
* `-p puerto`: Especifica el puerto en el que PostgreSQL está escuchando (por defecto, el puerto es 5432).

Después de ejecutar este comando, se te pedirá que ingreses la contraseña del usuario.

## <mark style="color:purple;">**Comandos para extraer información**</mark>

### Mostrar todas las bases de datos

```sql
\l
```

### Conectarse a una base de datos específica

```sql
\c nombre_base_datos
```

### Listar todas las tablas en la base de datos seleccionada

```sql
\dt
```

### Mostrar la estructura de una tabla específica

```sql
\d nombre_tabla
```

### Extraer todos los datos de una tabla

```sql
SELECT * FROM nombre_tabla;
```

### Filtrar datos con una consulta SELECT

```sql
SELECT columna1, columna2 FROM nombre_tabla WHERE condición;
```

### Exportar resultados de una consulta SELECT a un archivo CSV

```sql
COPY (SELECT columna1, columna2 FROM nombre_tabla) TO '/ruta/al/archivo.csv' WITH CSV HEADER;
```

### Salir de `psql`

```sql
\q
```

## <mark style="color:purple;">**Consultas SELECT avanzadas**</mark>

### Ordenar los resultados en orden ascendente:

```sql
SELECT * FROM nombre_tabla ORDER BY columna ASC;
```

### Ordenar los resultados en orden descendente:

```sql
SELECT * FROM nombre_tabla ORDER BY columna DESC;
```

### Limitar la cantidad de resultados:

```sql
SELECT * FROM nombre_tabla LIMIT cantidad;
```

### Saltar una cantidad específica de resultados antes de devolverlos:

```sql
SELECT * FROM nombre_tabla OFFSET cantidad;
```

### Combinar varias condiciones en una consulta SELECT utilizando operadores lógicos (AND, OR, NOT):

```sql
SELECT * FROM nombre_tabla WHERE condición1 AND condición2;
```

### Utilizar funciones de agregación como SUM, COUNT, AVG, MAX, MIN, etc., para realizar cálculos en los datos:

```sql
SELECT COUNT(*) FROM nombre_tabla;
```

## <mark style="color:purple;">**Consultas con UNION**</mark>

### Combinar resultados de múltiples consultas SELECT utilizando UNION&#x20;

* Para eliminar duplicados

```sql
SELECT columna FROM tabla1
UNION
SELECT columna FROM tabla2;
```

## <mark style="color:purple;">**Consultas con JOINS**</mark>

### Realizar una consulta que combina datos de múltiples tablas utilizando INNER JOIN:

```sql
SELECT t1.columna1, t2.columna2
FROM tabla1 t1
INNER JOIN tabla2 t2 ON t1.clave = t2.clave;
```

### Utilizar LEFT JOIN para obtener todos los registros de la tabla de la izquierda y los registros coincidentes de la tabla de la derecha:

```sql
SELECT t1.columna1, t2.columna2
FROM tabla1 t1
LEFT JOIN tabla2 t2 ON t1.clave = t2.clave;
```

### Realizar una consulta que combine datos de múltiples tablas utilizando FULL OUTER JOIN:

```sql
SELECT t1.columna1, t2.columna2
FROM tabla1 t1
FULL OUTER JOIN tabla2 t2 ON t1.clave = t2.clave;
```

## <mark style="color:purple;">**Consultas con GROUP BY y HAVING**</mark>

### Agrupar registros basados en una columna específica y realizar cálculos en grupos de datos:

```sql
SELECT columna1, COUNT(*) as cantidad
FROM nombre_tabla
GROUP BY columna1
HAVING COUNT(*) > 1;
```
