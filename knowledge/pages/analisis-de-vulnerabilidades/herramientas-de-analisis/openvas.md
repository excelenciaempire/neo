
# OpenVAS

OpenVAS (Open Vulnerability Assessment System) es una poderosa herramienta de análisis de vulnerabilidades que forma parte de **Greenbone Vulnerability Manager (GVM)**. Permite escanear redes, servidores y dispositivos en busca de vulnerabilidades conocidas. OpenVAS es ampliamente utilizado por profesionales de la ciberseguridad para realizar auditorías y análisis de seguridad.

OpenVAS tiene la capacidad de realizar escaneos de red, incluidas pruebas autenticadas y no autenticadas.

{% embed url="<https://openvas.org/>" %}

<figure><img src="/files/YIpv8Mwyacjb0IyKGOSn" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Es totalmente gratuito y se puede instalar con apt en Kali Linux
{% endhint %}

## <mark style="color:purple;">Instalación</mark>

### Instalar requisitos

```bash
# Actualizar paquetes y instalar gvm
sudo apt update
sudo apt install gvm
sudo gvm-setup

# Instalar UFW (opcional)
sudo apt install ufw

# Habilita UFW y permite el acceso al servidor de OpenVAS por los puertos 80 y 9392
sudo ufw enable
sudo ufw allow 80
sudo ufw allow 9392
```

Si al ejecutar el `gvm-setup` nos da el siguiente error deberemos cambiar del clúster 16 al 17 de PostgreSQL:

```bash
sudo gvm-setup

[>] Starting PostgreSQL service
[-] ERROR: The default PostgreSQL version (16) is not 17 that is required by libgvmd
[-] ERROR: libgvmd needs PostgreSQL 17 to use the port 5432
[-] ERROR: Use pg_upgradecluster to update your PostgreSQL cluster
```

### Instalar asistente de Greenbone

```bash
# Instala el asistente de greenbone
sudo gvm-check-setup
sudo gvm-start

# Abre un navegador en localhost por el puerto 9392
https://localhost:9392/
```

### **Reiniciar OpenVAS**

```bash
sudo gvm-stop
sudo gvm-start
```

```sql
REINDEX DATABASE template1;
ALTER DATABASE template1 REFRESH COLLATION VERSION;
```

### Crear base de datos

```bash
sudo runuser -u postgres -- /usr/share/gvm/create-postgresql-database

[i] User _gvm already exists in PostgreSQL

[*] Creating database

[*] Creating permissions
CREATE ROLE

[*] Applying permissions
GRANT ROLE

[*] Creating extension uuid-ossp
CREATE EXTENSION

[*] Creating extension pgcrypto
CREATE EXTENSION

[*] Creating extension pg-gvm
CREATE EXTENSION
```

### Crear un nuevo usuario para OpenVAS

```bash
sudo runuser -u _gvm -- gvmd --create-user=kali --password=kali
User created.
```

### Actualizar feeds de vulnerabilidades

```bash
sudo greenbone-feed-sync
```

### Iniciar OpenVAS

```bash
sudo gvm-check-setup
sudo gvm-start

# Abre un navegador en localhost por el puerto 9392
https://localhost:9392/
```

<figure><img src="/files/AXGFWDHP7y2eKxTXNQiD" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Errores comunes de instalación</mark>

### Error de versión de PostgreSQL

```bash
sudo gvm-setup

[>] Starting PostgreSQL service
[-] ERROR: The default PostgreSQL version (16) is not 17 that is required by libgvmd
[-] ERROR: libgvmd needs PostgreSQL 17 to use the port 5432
[-] ERROR: Use pg_upgradecluster to update your PostgreSQL cluster
```

#### Configurar PostgreSQL

OpenVAS necesita tener habilitado el clúster de PostgreSQL 17. Si tenemos una versión anterior podemos deshabilitarla de la siguiente manera:

```bash
# Combrobar clusters de PostgreSQL
pg_lsclusters

Ver Cluster Port Status Owner    Data directory              Log file
16  main    5432 online postgres /var/lib/postgresql/16/main /var/log/postgresql/postgresql-16-main.log
17  main    5433 online postgres /var/lib/postgresql/17/main /var/log/postgresql/postgresql-17-main.log

# Detener cluster de PostgreSQL
sudo pg_ctlcluster 16 main stop
```

#### **Cambiar PostgreSQL 17 al puerto 5432**

Edita la configuración del clúster de PostgreSQL 17 para que use el puerto 5432. Modifica el archivo `postgresql.conf` de la versión 17:

```bash
sudo nano /etc/postgresql/17/main/postgresql.conf
```

Busca la línea donde se especifica el puerto y cambia `5433` por `5432`:

```plaintext
port = 5432
```

#### Iniciar clúster PostgreSQL17

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ sudo pg_ctlcluster 17 main start
</strong>
afsh4ck@kali$ sudo gvm-setup
</code></pre>

Este comando hará lo siguiente:

* Configura los servicios necesarios (PostgreSQL, Redis, etc.).
* Descarga el feed de vulnerabilidades de Greenbone actualizado.
* Configura las bases de datos y los servicios de OpenVAS.

Anota las credenciales generadas. Al final del proceso, verás algo como:

```plaintext
User created: admin
Password: some-random-password
```

Si lo necesitas, puedes cambiar la contraseña usando:

```bash
sudo gvmd --user=admin --new-password=admin
```

#### **Eliminar el clúster antiguo (opcional)**

Si confirmas que PostgreSQL 17 está funcionando correctamente, puedes eliminar el clúster antiguo (versión 16):

```bash
sudo pg_dropcluster 16 main --stop
```

### Error de collation

```
[*] Creating database
createdb: error: falló la creación de la base de datos: ERROR:  discordancia en la versión de «collation» de la base de datos patrón «template1»
DETALLE:  La base de datos patrón fue creada usando la versión 2.38, pero el sistema operativo provee la versión 2.40.
SUGERENCIA:  Reconstruya todos los objetos de la base de datos patrón afectados por este ordenamiento y ejecute ALTER DATABASE template1 REFRESH COLLATION VERSION, o construya PostgreSQL con la versión correcta de la biblioteca.
```

El mensaje indica que la base de datos PostgreSQL tiene una discordancia de versión de **collation** entre lo que fue usado al crearla y lo que ofrece nuestro sistema actual.

Sigue los pasos sugeridos para corregir el problema de collation en la base de datos:

**1. Accede a PostgreSQL como usuario `postgres`:**

```bash
sudo -u postgres psql
```

**2. Permitir cambios en `template1`:**

```sql
UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';
```

**3. Reconstruir índices y actualizar la collation en `template1`:**

```sql
REINDEX DATABASE template1;
ALTER DATABASE template1 REFRESH COLLATION VERSION;
```

**4. Marcar `template1` como plantilla nuevamente:**

```sql
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';
```

**5. Hacer lo mismo con `template0`:**

```sql
UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template0';
REINDEX DATABASE template0;
ALTER DATABASE template0 REFRESH COLLATION VERSION;
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template0';
```

**6. Salir del cliente de PostgreSQL:**

```sql
\q
```

### Error al arrancar PostgreSQL

```bash
sudo -u postgres psql

psql: error: falló la conexión al servidor en el socket «/var/run/postgresql/.s.PGSQL.5432»: No existe el fichero o el directorio
	¿Está el servidor en ejecución localmente y aceptando conexiones en ese socket?
```

Reiniciar servicio::

```bash
sudo systemctl restart postgresql
```

***

## <mark style="color:purple;">Escaneo con OpenVAS</mark>

Una vez logueados debemos esperar hasta que se sincronicen los feeds en `Administration/Feed Status`. Deben quedar en Status `Current`.

{% hint style="warning" %}
Esto es importante, ya que sino los escaneos pueden arrojar errores o no funcionar.
{% endhint %}

<figure><img src="/files/8DlnKLTKj2Idw1qUgQX1" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/FdxacEIxIaDKjngmuxQy" alt=""><figcaption></figcaption></figure>

### 1. Añadir nuevo target

En `Configuration/Targets` hacemos clic en el botón de la esquina superior izquierda:

<figure><img src="/files/55J6lumkn9pZCXNOn6Ve" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/7KCDkbXa03MO0CbFLJ7f" alt=""><figcaption></figcaption></figure>

Aquí añadimos el nombre del host, descripción y puertos a escanear. Para escanear todos los puertos disponibles podemos usar:

```
T:1-65535,U:1-65535
```

### 2. Crear Task de escaneo

En `Scan/Tasks` añadimos una nueva tarea:

<figure><img src="/files/uHbf0CHbsaEMd62EBtOY" alt=""><figcaption></figcaption></figure>
