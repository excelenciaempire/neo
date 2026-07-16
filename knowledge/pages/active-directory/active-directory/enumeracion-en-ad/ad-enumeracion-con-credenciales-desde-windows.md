
# AD: Enumeración con credenciales: desde Windows

En la sección anterior, exploramos algunas herramientas que podemos usar desde nuestro host de ataque de Linux para la enumeración con credenciales de dominio válidas. En esta sección, experimentaremos con algunas herramientas para enumerar desde un host de ataque de Windows, como `SharpHound/BloodHound`, `PowerView/SharpView`, `Grouper2`, `Snaffler` y algunas herramientas integradas útiles para la enumeración de AD.&#x20;

Algunos de los datos que recopilamos en esta fase pueden proporcionar más información para generar informes, no solo conducir directamente a rutas de ataque. Dependiendo del tipo de evaluación, nuestro cliente puede estar interesado en todos los hallazgos posibles, por lo que incluso cuestiones como la capacidad de ejecutar BloodHound libremente o ciertos atributos de la cuenta de usuario pueden valer la pena incluirlos en nuestro informe como hallazgos de riesgo medio o en una sección de apéndice separada. No todos los problemas que descubrimos tienen que estar orientados a reenviar nuestros ataques. Algunos de los resultados pueden ser de naturaleza informativa pero útiles para el cliente para ayudar a mejorar su postura de seguridad.

En este punto, nos interesan otras configuraciones erróneas y problemas de permisos que podrían provocar movimientos laterales y verticales. También estamos interesados ​​en tener una idea más amplia de cómo está configurado el dominio, es decir, ¿existen fideicomisos con otros dominios tanto dentro como fuera del bosque actual? También estamos interesados ​​en saquear los archivos compartidos a los que nuestro usuario tiene acceso, ya que a menudo contienen datos confidenciales, como credenciales, que pueden usarse para mejorar nuestro acceso.

***

## <mark style="color:purple;">TTPs</mark>

La primera herramienta que exploraremos es el [módulo PowerShell de ActiveDirectory](https://docs.microsoft.com/en-us/powershell/module/activedirectory/?view=windowsserver2022-ps) . Al acceder a un host de Windows en el dominio, especialmente uno que utilice un administrador, es posible que encuentre herramientas y scripts valiosos en el host.

***

## <mark style="color:purple;">Módulo PowerShell de ActiveDirectory</mark>

El módulo ActiveDirectory PowerShell es un grupo de cmdlets de PowerShell para administrar un entorno de Active Directory desde la línea de comandos. Consta de 147 cmdlets diferentes en el momento de redactar este artículo. No podemos cubrirlos todos aquí, pero veremos algunos que son particularmente útiles para enumerar entornos de AD. No dude en explorar otros cmdlets incluidos en el módulo en el laboratorio creado para esta sección y vea qué combinaciones y resultados interesantes puede crear.

Antes de que podamos utilizar el módulo, primero debemos asegurarnos de que esté importado. El cmdlet [Get-Module](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-module?view=powershell-7.2) , que forma parte del [módulo Microsoft.PowerShell.Core](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/?view=powershell-7.2) , enumerará todos los módulos disponibles, su versión y los posibles comandos para su uso. Esta es una excelente manera de ver si hay instalado algo como Git o scripts de administrador personalizados. Si el módulo no está cargado, ejecútelo `Import-Module ActiveDirectory` para cargarlo y usarlo.

**Descubrir los módulos importados**

```powershell
PS C:\htb> Get-Module

ModuleType Version    Name                                ExportedCommands
---------- -------    ----                                ----------------
Manifest   3.1.0.0    Microsoft.PowerShell.Utility        {Add-Member, Add-Type, Clear-Variable, Compare-Object...}
Script     2.0.0      PSReadline                          {Get-PSReadLineKeyHandler, Get-PSReadLineOption, Remove-PS...
```

Vemos que el módulo ActiveDirectory aún no se ha importado. Vamos a importarlo.

### **Importar módulo ActiveDirectory**

```powershell
PS C:\htb> Import-Module ActiveDirectory
PS C:\htb> Get-Module

ModuleType Version    Name                                ExportedCommands
---------- -------    ----                                ----------------
Manifest   1.0.1.0    ActiveDirectory                     {Add-ADCentralAccessPolicyMember, Add-ADComputerServiceAcc...
Manifest   3.1.0.0    Microsoft.PowerShell.Utility        {Add-Member, Add-Type, Clear-Variable, Compare-Object...}
Script     2.0.0      PSReadline                          {Get-PSReadLineKeyHandler, Get-PSReadLineOption, Remove-PS...  
```

Ahora que nuestros módulos están cargados, comencemos. Primero, enumeraremos información básica sobre el dominio con el cmdlet [Get-ADDomain](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-addomain?view=windowsserver2022-ps) .

### Obtener información del dominio

```powershell
PS C:\htb> Get-ADDomain

AllowedDNSSuffixes                 : {}
ChildDomains                       : {LOGISTICS.INLANEFREIGHT.LOCAL}
ComputersContainer                 : CN=Computers,DC=INLANEFREIGHT,DC=LOCAL
DeletedObjectsContainer            : CN=Deleted Objects,DC=INLANEFREIGHT,DC=LOCAL
DistinguishedName                  : DC=INLANEFREIGHT,DC=LOCAL
DNSRoot                            : INLANEFREIGHT.LOCAL
DomainControllersContainer         : OU=Domain Controllers,DC=INLANEFREIGHT,DC=LOCAL
DomainMode                         : Windows2016Domain
DomainSID                          : S-1-5-21-3842939050-3880317879-2865463114
ForeignSecurityPrincipalsContainer : CN=ForeignSecurityPrincipals,DC=INLANEFREIGHT,DC=LOCAL
Forest                             : INLANEFREIGHT.LOCAL
InfrastructureMaster               : ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
LastLogonReplicationInterval       :
LinkedGroupPolicyObjects           : {cn={DDBB8574-E94E-4525-8C9D-ABABE31223D0},cn=policies,cn=system,DC=INLANEFREIGHT,
                                     DC=LOCAL, CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=INLAN
                                     EFREIGHT,DC=LOCAL}
LostAndFoundContainer              : CN=LostAndFound,DC=INLANEFREIGHT,DC=LOCAL
ManagedBy                          :
Name                               : INLANEFREIGHT
NetBIOSName                        : INLANEFREIGHT
ObjectClass                        : domainDNS
ObjectGUID                         : 71e4ecd1-a9f6-4f55-8a0b-e8c398fb547a
ParentDomain                       :
PDCEmulator                        : ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
PublicKeyRequiredPasswordRolling   : True
QuotasContainer                    : CN=NTDS Quotas,DC=INLANEFREIGHT,DC=LOCAL
ReadOnlyReplicaDirectoryServers    : {}
ReplicaDirectoryServers            : {ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL}
RIDMaster                          : ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
SubordinateReferences              : {DC=LOGISTICS,DC=INLANEFREIGHT,DC=LOCAL,
                                     DC=ForestDnsZones,DC=INLANEFREIGHT,DC=LOCAL,
                                     DC=DomainDnsZones,DC=INLANEFREIGHT,DC=LOCAL,
                                     CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL}
SystemsContainer                   : CN=System,DC=INLANEFREIGHT,DC=LOCAL
UsersContainer                     : CN=Users,DC=INLANEFREIGHT,DC=LOCAL
```

Esto imprimirá información útil como el SID del dominio, el nivel funcional del dominio, los dominios secundarios y más. A continuación, utilizaremos el cmdlet [Get-ADUser](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-aduser?view=windowsserver2022-ps) . Filtraremos las cuentas con la propiedad `ServicePrincipalName` completada. Esto nos dará una lista de cuentas que pueden ser susceptibles a un ataque Kerberoasting, que abordaremos en profundidad después de la siguiente sección.

### **Get-ADUser**

```powershell
PS C:\htb> Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName

DistinguishedName    : CN=adfs,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
Enabled              : True
GivenName            : Sharepoint
Name                 : adfs
ObjectClass          : user
ObjectGUID           : 49b53bea-4bc4-4a68-b694-b806d9809e95
SamAccountName       : adfs
ServicePrincipalName : {adfsconnect/azure01.inlanefreight.local}
SID                  : S-1-5-21-3842939050-3880317879-2865463114-5244
Surname              : Admin
UserPrincipalName    :

DistinguishedName    : CN=BACKUPAGENT,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
Enabled              : True
GivenName            : Jessica
Name                 : BACKUPAGENT
ObjectClass          : user
ObjectGUID           : 2ec53e98-3a64-4706-be23-1d824ff61bed
SamAccountName       : backupagent
ServicePrincipalName : {backupjob/veam001.inlanefreight.local}
SID                  : S-1-5-21-3842939050-3880317879-2865463114-5220
Surname              : Systemmailbox 8Cc370d3-822A-4Ab8-A926-Bb94bd0641a9
UserPrincipalName    :

<SNIP>
```

Otra comprobación interesante que podemos realizar utilizando el módulo ActiveDirectory sería verificar las relaciones de confianza del dominio utilizando el cmdlet [Get-ADTrust](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-adtrust?view=windowsserver2022-ps)

### **Comprobación de relaciones de confianza**

```powershell
PS C:\htb> Get-ADTrust -Filter *

Direction               : BiDirectional
DisallowTransivity      : False
DistinguishedName       : CN=LOGISTICS.INLANEFREIGHT.LOCAL,CN=System,DC=INLANEFREIGHT,DC=LOCAL
ForestTransitive        : False
IntraForest             : True
IsTreeParent            : False
IsTreeRoot              : False
Name                    : LOGISTICS.INLANEFREIGHT.LOCAL
ObjectClass             : trustedDomain
ObjectGUID              : f48a1169-2e58-42c1-ba32-a6ccb10057ec
SelectiveAuthentication : False
SIDFilteringForestAware : False
SIDFilteringQuarantined : False
Source                  : DC=INLANEFREIGHT,DC=LOCAL
Target                  : LOGISTICS.INLANEFREIGHT.LOCAL
TGTDelegation           : False
TrustAttributes         : 32
TrustedPolicy           :
TrustingPolicy          :
TrustType               : Uplevel
UplevelOnly             : False
UsesAESKeys             : False
UsesRC4Encryption       : False

Direction               : BiDirectional
DisallowTransivity      : False
DistinguishedName       : CN=FREIGHTLOGISTICS.LOCAL,CN=System,DC=INLANEFREIGHT,DC=LOCAL
ForestTransitive        : True
IntraForest             : False
IsTreeParent            : False
IsTreeRoot              : False
Name                    : FREIGHTLOGISTICS.LOCAL
ObjectClass             : trustedDomain
ObjectGUID              : 1597717f-89b7-49b8-9cd9-0801d52475ca
SelectiveAuthentication : False
SIDFilteringForestAware : False
SIDFilteringQuarantined : False
Source                  : DC=INLANEFREIGHT,DC=LOCAL
Target                  : FREIGHTLOGISTICS.LOCAL
TGTDelegation           : False
TrustAttributes         : 8
TrustedPolicy           :
TrustingPolicy          :
TrustType               : Uplevel
UplevelOnly             : False
UsesAESKeys             : False
UsesRC4Encryption       : False  
```

Este cmdlet imprimirá cualquier relación de confianza que tenga el dominio. Podemos determinar si son relaciones dentro de nuestro bosque o con dominios en otros bosques, el tipo de relaciones, la dirección de la relación y el nombre del dominio con el que es la relación. Esto será útil más adelante cuando se busque aprovechar las relaciones de confianza entre padres e hijos y atacar a través de fideicomisos de boque. A continuación, podemos recopilar información del grupo AD utilizando el cmdlet [Get-ADGroup](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-adgroup?view=windowsserver2022-ps) .

### **Enumeración de grupos**

```powershell
PS C:\htb> Get-ADGroup -Filter * | select name

name
----
Administrators
Users
Guests
Print Operators
Backup Operators
Replicator
Remote Desktop Users
Network Configuration Operators
Performance Monitor Users
Performance Log Users
Distributed COM Users
IIS_IUSRS
Cryptographic Operators
Event Log Readers
Certificate Service DCOM Access
RDS Remote Access Servers
RDS Endpoint Servers
RDS Management Servers
Hyper-V Administrators
Access Control Assistance Operators
Remote Management Users
Storage Replica Administrators
Domain Computers
Domain Controllers
Schema Admins
Enterprise Admins
Cert Publishers
Domain Admins

<SNIP>
```

Podemos tomar los resultados y volver a introducir nombres interesantes en el cmdlet para obtener información más detallada sobre un grupo en particular de la siguiente manera:

### **Información detallada del grupo**

```powershell
PS C:\htb> Get-ADGroup -Identity "Backup Operators"

DistinguishedName : CN=Backup Operators,CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL
GroupCategory     : Security
GroupScope        : DomainLocal
Name              : Backup Operators
ObjectClass       : group
ObjectGUID        : 6276d85d-9c39-4b7c-8449-cad37e8abc38
SamAccountName    : Backup Operators
SID               : S-1-5-32-551
```

Ahora que sabemos más sobre el grupo, obtengamos una lista de miembros usando el cmdlet [Get-ADGroupMember](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-adgroupmember?view=windowsserver2022-ps) .

#### Membresía de grupo

&#x20; Enumeración con credenciales: desde Windows

```powershell
PS C:\htb> Get-ADGroupMember -Identity "Backup Operators"

distinguishedName : CN=BACKUPAGENT,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
name              : BACKUPAGENT
objectClass       : user
objectGUID        : 2ec53e98-3a64-4706-be23-1d824ff61bed
SamAccountName    : backupagent
SID               : S-1-5-21-3842939050-3880317879-2865463114-5220
```

Podemos ver que una cuenta, `backupagent` pertenece a este grupo. Vale la pena anotar esto porque si podemos tomar el control de esta cuenta de servicio mediante algún ataque, podríamos usar su membresía en el grupo Operadores de respaldo para tomar el control del dominio. Podemos realizar este proceso para que los otros grupos comprendan completamente la configuración de membresía del dominio. Intente repetir el proceso con algunos grupos diferentes.&#x20;

Verá que este proceso puede resultar tedioso y nos quedará una enorme cantidad de datos que analizar. Debemos saber cómo hacer esto con herramientas integradas como el módulo ActiveDirectory PowerShell, pero veremos más adelante en esta sección hasta qué punto herramientas como BloodHound pueden acelerar este proceso y hacer que nuestros resultados sean mucho más precisos y organizados.

Utilizar el módulo ActiveDirectory en un host puede ser una forma más sigilosa de realizar acciones que colocar una herramienta en un host o cargarla en la memoria e intentar usarla. De esta manera, nuestras acciones podrían potencialmente mezclarse más. A continuación, analizaremos la herramienta PowerView, que tiene muchas funciones para simplificar la enumeración y profundizar en el dominio.

***

## <mark style="color:purple;">PowerView</mark>

[PowerView](https://github.com/PowerShellMafia/PowerSploit/tree/master/Recon) es una herramienta escrita en PowerShell que nos ayuda a obtener conocimiento de la situación dentro de un entorno de AD. Al igual que BloodHound, proporciona una forma de identificar dónde los usuarios han iniciado sesión en una red, enumerar información de dominio como usuarios, computadoras, grupos, ACLS, confianzas, buscar recursos compartidos de archivos y contraseñas, realizar Kerberoasting y más. Es una herramienta muy versátil que puede brindarnos una gran perspectiva sobre la postura de seguridad del dominio de nuestro cliente. Requiere más trabajo manual para determinar configuraciones incorrectas y relaciones dentro del dominio que BloodHound, pero, cuando se usa correctamente, puede ayudarnos a identificar configuraciones incorrectas sutiles.

Examinemos algunas de las capacidades de PowerView y veamos qué datos devuelve. La siguiente tabla describe algunas de las funciones más útiles que ofrece PowerView.

<table data-header-hidden><thead><tr><th width="305"></th><th></th></tr></thead><tbody><tr><td><strong>Dominio</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>Export-PowerViewCSV</code></td><td>Agregar resultados a un archivo CSV</td></tr><tr><td><code>ConvertTo-SID</code></td><td>Convertir un nombre de usuario o grupo a su valor SID</td></tr><tr><td><code>Get-DomainSPNTicket</code></td><td>Solicita el ticket de Kerberos para una cuenta de nombre principal de servicio (SPN) especificada</td></tr><tr><td><strong>Funciones de dominio/LDAP:</strong></td><td></td></tr><tr><td><code>Get-Domain</code></td><td>Devolverá el objeto AD para el dominio actual (o especificado)</td></tr><tr><td><code>Get-DomainController</code></td><td>Devuelve una lista de los controladores de dominio para el dominio especificado</td></tr><tr><td><code>Get-DomainUser</code></td><td>Devolverá todos los usuarios u objetos de usuario específicos en AD</td></tr><tr><td><code>Get-DomainComputer</code></td><td>Devolverá todas las computadoras u objetos de computadora específicos en AD</td></tr><tr><td><code>Get-DomainGroup</code></td><td>Devolverá todos los grupos u objetos de grupos específicos en AD</td></tr><tr><td><code>Get-DomainOU</code></td><td>Busque todos o objetos OU específicos en AD</td></tr><tr><td><code>Find-InterestingDomainAcl</code></td><td>Encuentra ACL de objetos en el dominio con derechos de modificación establecidos para objetos no integrados</td></tr><tr><td><code>Get-DomainGroupMember</code></td><td>Devolverá los miembros de un grupo de dominio específico</td></tr><tr><td><code>Get-DomainFileServer</code></td><td>Devuelve una lista de servidores que probablemente funcionen como servidores de archivos</td></tr><tr><td><code>Get-DomainDFSShare</code></td><td>Devuelve una lista de todos los sistemas de archivos distribuidos para el dominio actual (o especificado)</td></tr><tr><td><strong>Funciones de GPO:</strong></td><td></td></tr><tr><td><code>Get-DomainGPO</code></td><td>Devolverá todos los GPO u objetos GPO específicos en AD</td></tr><tr><td><code>Get-DomainPolicy</code></td><td>Devuelve la política de dominio predeterminada o la política de controlador de dominio para el dominio actual.</td></tr><tr><td><strong>Funciones de enumeración de computadora:</strong></td><td></td></tr><tr><td><code>Get-NetLocalGroup</code></td><td>Enumera grupos locales en la máquina local o remota</td></tr><tr><td><code>Get-NetLocalGroupMember</code></td><td>Enumera los miembros de un grupo local específico</td></tr><tr><td><code>Get-NetShare</code></td><td>Devuelve los recursos compartidos abiertos en la máquina local (o remota)</td></tr><tr><td><code>Get-NetSession</code></td><td>Devolverá información de sesión para la máquina local (o remota)</td></tr><tr><td><code>Test-AdminAccess</code></td><td>Comprueba si el usuario actual tiene acceso administrativo a la máquina local (o remota)</td></tr><tr><td><strong>Funciones 'meta' enhebradas:</strong></td><td></td></tr><tr><td><code>Find-DomainUserLocation</code></td><td>Encuentra máquinas donde usuarios específicos han iniciado sesión</td></tr><tr><td><code>Find-DomainShare</code></td><td>Encuentra recursos compartidos accesibles en máquinas de dominio</td></tr><tr><td><code>Find-InterestingDomainShareFile</code></td><td>Busca archivos que coincidan con criterios específicos en recursos compartidos legibles en el dominio.</td></tr><tr><td><code>Find-LocalAdminAccess</code></td><td>Encuentre máquinas en el dominio local donde el usuario actual tiene acceso de administrador local</td></tr><tr><td><strong>Funciones de confianza del dominio:</strong></td><td></td></tr><tr><td><code>Get-DomainTrust</code></td><td>Devuelve confianzas de dominio para el dominio actual o un dominio específico</td></tr><tr><td><code>Get-ForestTrust</code></td><td>Devuelve todos los fideicomisos de bosque para el bosque actual o un bosque especificado</td></tr><tr><td><code>Get-DomainForeignUser</code></td><td>Enumera los usuarios que están en grupos fuera del dominio del usuario.</td></tr><tr><td><code>Get-DomainForeignGroupMember</code></td><td>Enumera grupos con usuarios fuera del dominio del grupo y devuelve cada miembro externo</td></tr><tr><td><code>Get-DomainTrustMapping</code></td><td>Enumerará todas las confianzas para el dominio actual y cualquier otro visto.</td></tr></tbody></table>

Esta tabla no abarca todo lo que ofrece PowerView, pero incluye muchas de las funciones que utilizaremos repetidamente. Para obtener más información sobre PowerView, consulte el [módulo PowerView de Active Directory](https://academy.hackthebox.com/course/preview/active-directory-powerview) . A continuación, experimentaremos con algunos de ellos.

Primero está la función [Get-DomainUser](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainUser/) . Esto nos proporcionará información sobre todos los usuarios o usuarios específicos que especifiquemos. A continuación lo usaremos para obtener información sobre un usuario específico `mmorgan`.

### **Información del usuario del dominio**

```powershell
PS C:\htb> Get-DomainUser -Identity mmorgan -Domain inlanefreight.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,useraccountcontrol

name                 : Matthew Morgan
samaccountname       : mmorgan
description          :
memberof             : {CN=VPN Users,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Shared Calendar
                       Read,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Printer Access,OU=Security
                       Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=File Share H Drive,OU=Security
                       Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL...}
whencreated          : 10/27/2021 5:37:06 PM
pwdlastset           : 11/18/2021 10:02:57 AM
lastlogontimestamp   : 2/27/2022 6:34:25 PM
accountexpires       : NEVER
admincount           : 1
userprincipalname    : mmorgan@inlanefreight.local
serviceprincipalname :
mail                 :
useraccountcontrol   : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, DONT_REQ_PREAUTH
```

Vimos información básica del usuario con PowerView. Ahora enumeremos cierta información del grupo de dominio. Podemos utilizar la función [Get-DomainGroupMember](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainGroupMember/) para recuperar información específica del grupo. Agregar la flag `-Recurse` le indica a PowerView que, si encuentra algún grupo que forme parte del grupo objetivo (pertenencia a grupos anidados), enumere los miembros de esos grupos. Por ejemplo, el resultado siguiente muestra que el grupo `Secadmins` es parte del grupo `Domain Admins` a través de la membresía de grupo anidado. En este caso, podremos ver todos los miembros de ese grupo que heredan derechos de administrador de dominio a través de su membresía en el grupo.

### **Membresía de grupo recursivo**

```powershell
PS C:\htb>  Get-DomainGroupMember -Identity "Domain Admins" -Recurse

GroupDomain             : INLANEFREIGHT.LOCAL
GroupName               : Domain Admins
GroupDistinguishedName  : CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
MemberDomain            : INLANEFREIGHT.LOCAL
MemberName              : svc_qualys
MemberDistinguishedName : CN=svc_qualys,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
MemberObjectClass       : user
MemberSID               : S-1-5-21-3842939050-3880317879-2865463114-5613

GroupDomain             : INLANEFREIGHT.LOCAL
GroupName               : Domain Admins
GroupDistinguishedName  : CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
MemberDomain            : INLANEFREIGHT.LOCAL
MemberName              : sp-admin
MemberDistinguishedName : CN=Sharepoint Admin,OU=Service Accounts,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
MemberObjectClass       : user
MemberSID               : S-1-5-21-3842939050-3880317879-2865463114-5228

GroupDomain             : INLANEFREIGHT.LOCAL
GroupName               : Secadmins
GroupDistinguishedName  : CN=Secadmins,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
MemberDomain            : INLANEFREIGHT.LOCAL
MemberName              : spong1990
MemberDistinguishedName : CN=Maggie
                          Jablonski,OU=Operations,OU=Logistics-HK,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
MemberObjectClass       : user
MemberSID               : S-1-5-21-3842939050-3880317879-2865463114-1965

<SNIP>  
```

Arriba, realizamos una búsqueda recursiva en el grupo `Domain Admins` para enumerar sus miembros. Ahora sabemos a quién dirigirnos para una posible elevación de privilegios. Al igual que con el módulo AD PowerShell, también podemos enumerar las asignaciones de confianza de dominio.

### **Enumeración de confianza**

```powershell
PS C:\htb> Get-DomainTrustMapping

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : LOGISTICS.INLANEFREIGHT.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : WITHIN_FOREST
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 6:20:22 PM
WhenChanged     : 2/26/2022 11:55:55 PM

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : FREIGHTLOGISTICS.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : FOREST_TRANSITIVE
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 8:07:09 PM
WhenChanged     : 2/27/2022 12:02:39 AM

SourceName      : LOGISTICS.INLANEFREIGHT.LOCAL
TargetName      : INLANEFREIGHT.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : WITHIN_FOREST
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 6:20:22 PM
WhenChanged     : 2/26/2022 11:55:55 PM 
```

Podemos usar la función [Test-AdminAccess](https://powersploit.readthedocs.io/en/latest/Recon/Test-AdminAccess/) para probar el acceso de administrador local en la máquina actual o en una remota.

### **Prueba de acceso de administrador local**

```powershell
PS C:\htb> Test-AdminAccess -ComputerName ACADEMY-EA-MS01

ComputerName    IsAdmin
------------    -------
ACADEMY-EA-MS01    True 
```

Arriba, determinamos que el usuario que estamos utilizando actualmente es un administrador en el host ACADEMY-EA-MS01. Podemos realizar la misma función para cada host para ver dónde tenemos acceso administrativo. Más adelante veremos qué tan bien realiza BloodHound este tipo de comprobaciones. Ahora podemos buscar usuarios con el atributo SPN configurado, lo que indica que la cuenta puede estar sujeta a un ataque Kerberoasting.

### **Cómo encontrar usuarios con SPN configurado**

```powershell
PS C:\htb> Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName

serviceprincipalname                          samaccountname
--------------------                          --------------
adfsconnect/azure01.inlanefreight.local       adfs
backupjob/veam001.inlanefreight.local         backupagent
d0wngrade/kerberoast.inlanefreight.local      d0wngrade
kadmin/changepw                               krbtgt
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433 sqldev
MSSQLSvc/SPSJDB.inlanefreight.local:1433      sqlprod
MSSQLSvc/SQL-CL01-01inlanefreight.local:49351 sqlqa
sts/inlanefreight.local                       solarwindsmonitor
testspn/kerberoast.inlanefreight.local        testspn
testspn2/kerberoast.inlanefreight.local       testspn2
```

Pruebe algunas funciones más de la herramienta hasta que se sienta cómodo usándola. Veremos PowerView varias veces más a medida que avancemos en este módulo.

***

## <mark style="color:purple;">SharpView</mark>

PowerView es parte del kit de herramientas ofensivo PowerShell de PowerSploit, ahora obsoleto. La herramienta ha estado recibiendo actualizaciones de BC-Security como parte de su marco [Empire 4](https://github.com/BC-SECURITY/Empire/blob/master/empire/server/data/module_source/situational_awareness/network/powerview.ps1) . Empire 4 es la bifurcación de BC-Security del proyecto Empire original y se mantiene activamente a partir de abril de 2022. A lo largo de este módulo mostramos ejemplos utilizando la versión de desarrollo de PowerView porque es una excelente herramienta de reconocimiento en un entorno de Active Directory y todavía es extremadamente potente y útil en redes AD modernas aunque no se mantenga la versión original. La versión BC-SECURITY de [PowerView](https://github.com/BC-SECURITY/Empire/blob/master/empire/server/data/module_source/situational_awareness/network/powerview.ps1) tiene algunas funciones nuevas, como la que se utiliza `Get-NetGmsa` para buscar [cuentas de servicio administradas por grupo](https://docs.microsoft.com/en-us/windows-server/security/group-managed-service-accounts/group-managed-service-accounts-overview) , que está fuera del alcance de este módulo. Vale la pena jugar con ambas versiones para ver las sutiles diferencias entre las versiones antiguas y las mantenidas actualmente.

Otra herramienta con la que vale la pena experimentar es `SharpView`, una versión .NET de PowerView. Muchas de las mismas funciones admitidas por PowerView se pueden utilizar con SharpView. Podemos escribir el nombre de un método con `-Help` para obtener una lista de argumentos.

```powershell
PS C:\htb> .\SharpView.exe Get-DomainUser -Help

Get_DomainUser -Identity <String[]> -DistinguishedName <String[]> -SamAccountName <String[]> -Name <String[]> -MemberDistinguishedName <String[]> -MemberName <String[]> -SPN <Boolean> -AdminCount <Boolean> -AllowDelegation <Boolean> -DisallowDelegation <Boolean> -TrustedToAuth <Boolean> -PreauthNotRequired <Boolean> -KerberosPreauthNotRequired <Boolean> -NoPreauth <Boolean> -Domain <String> -LDAPFilter <String> -Filter <String> -Properties <String[]> -SearchBase <String> -ADSPath <String> -Server <String> -DomainController <String> -SearchScope <SearchScope> -ResultPageSize <Int32> -ServerTimeLimit <Nullable`1> -SecurityMasks <Nullable`1> -Tombstone <Boolean> -FindOne <Boolean> -ReturnOne <Boolean> -Credential <NetworkCredential> -Raw <Boolean> -UACFilter <UACEnum> 
```

Aquí podemos usar SharpView para enumerar información sobre un usuario específico, como el usuario `forend` que controlamos.

```powershell
PS C:\htb> .\SharpView.exe Get-DomainUser -Identity forend

[Get-DomainSearcher] search base: LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
[Get-DomainUser] filter string: (&(samAccountType=805306368)(|(samAccountName=forend)))
objectsid                      : {S-1-5-21-3842939050-3880317879-2865463114-5614}
samaccounttype                 : USER_OBJECT
objectguid                     : 53264142-082a-4cb8-8714-8158b4974f3b
useraccountcontrol             : NORMAL_ACCOUNT
accountexpires                 : 12/31/1600 4:00:00 PM
lastlogon                      : 4/18/2022 1:01:21 PM
lastlogontimestamp             : 4/9/2022 1:33:21 PM
pwdlastset                     : 2/28/2022 12:03:45 PM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 4/5/2022 7:09:07 AM
name                           : forend
distinguishedname              : CN=forend,OU=IT Admins,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
whencreated                    : 2/28/2022 8:03:45 PM
whenchanged                    : 4/9/2022 8:33:21 PM
samaccountname                 : forend
memberof                       : {CN=VPN Users,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Shared Calendar Read,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=Printer Access,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=File Share H Drive,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL, CN=File Share G Drive,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL}
cn                             : {forend}
objectclass                    : {top, person, organizationalPerson, user}
badpwdcount                    : 0
countrycode                    : 0
usnchanged                     : 3259288
logoncount                     : 26618
primarygroupid                 : 513
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL
dscorepropagationdata          : {3/24/2022 3:58:07 PM, 3/24/2022 3:57:44 PM, 3/24/2022 3:52:58 PM, 3/24/2022 3:49:31 PM, 7/14/1601 10:36:49 PM}
usncreated                     : 3054181
instancetype                   : 4
codepage                       : 0
```

Experimente con SharpView en el host MS01 y vuelva a crear tantos ejemplos de PowerView como sea posible. Aunque la evasión no está dentro del alcance de este módulo, SharpView puede ser útil cuando un cliente se ha vuelto más resistente al uso de PowerShell o necesitamos evitar su uso.

***

## <mark style="color:purple;">Recursos compartidos</mark>

Los recursos compartidos permiten a los usuarios de un dominio acceder rápidamente a información relevante para sus funciones diarias y compartir contenido con su organización. Cuando se configuran correctamente, los recursos compartidos de dominio requerirán que el usuario esté unido al dominio y se le solicite que se autentique al acceder al sistema. También se establecerán permisos para garantizar que los usuarios solo puedan acceder y ver lo que sea necesario para su función diaria. Los recursos compartidos demasiado permisivos pueden provocar la divulgación accidental de información confidencial, especialmente aquella que contiene datos médicos, legales, de personal, de RR. HH., etc.&#x20;

En un ataque, obtener el control sobre un usuario de dominio estándar que puede acceder a recursos compartidos, como los recursos compartidos de TI/infraestructura, podría llevar a la divulgación de datos confidenciales, como archivos de configuración o archivos de autenticación, como claves SSH o contraseñas almacenadas de forma insegura. Queremos identificar cualquier problema como estos para asegurarnos de que el cliente no exponga ningún dato a usuarios que no necesitan acceder a él para sus trabajos diarios y que cumplan con los requisitos legales/regulatorios a los que están sujetos (HIPAA, PCI, etc.).&#x20;

Podemos usar PowerView para buscar recursos compartidos y luego ayudarnos a buscarlos o usar varios comandos manuales para buscar cadenas comunes, como archivos con el nombre `pass`. Este puede ser un proceso tedioso y podemos pasar por alto cosas, especialmente en entornos grandes. Ahora, tomémonos un tiempo para explorar la herramienta `Snaffler` y ver cómo puede ayudarnos a identificar estos problemas de manera más precisa y eficiente.

***

## <mark style="color:purple;">Snaffler</mark>

[Snaffler](https://github.com/SnaffCon/Snaffler) es una herramienta que nos puede ayudar a adquirir credenciales u otros datos confidenciales en un entorno de Active Directory. Snaffler funciona obteniendo una lista de hosts dentro del dominio y luego enumerando esos hosts para recursos compartidos y directorios legibles. Una vez hecho esto, itera a través de todos los directorios legibles por nuestro usuario y busca archivos que podrían servir para mejorar nuestra posición dentro de la evaluación. Snaffler requiere que se ejecute desde un host unido al dominio o en un contexto de usuario de dominio.

Para ejecutar Snaffler, podemos usar el siguiente comando:

```bash
Snaffler.exe -s -d inlanefreight.local -o snaffler.log -v data
```

El `-s` le indica que imprima los resultados en la consola, el `-d` especifica el dominio dentro del cual buscar y el `-o` le indica a Snaffler que escriba los resultados en un archivo de registro. La opción `-v` es el nivel de verbosidad. Normalmente `data` es mejor, ya que solo muestra los resultados en la pantalla, por lo que es más fácil comenzar a buscar en las ejecuciones de la herramienta. Snaffler puede producir una `cantidad considerable de datos`, por lo que normalmente deberíamos generar la salida en un archivo y dejar que se ejecute y luego volver a él más tarde. También puede ser útil proporcionar la salida sin procesar de Snaffler a los clientes como datos complementarios durante una prueba de penetración, ya que puede ayudarlos a concentrarse en los recursos compartidos de alto valor que deben bloquearse primero.

#### **Snaffler en acción**

```powershell
PS C:\htb> .\Snaffler.exe -d INLANEFREIGHT.LOCAL -s -v data

 .::::::.:::.    :::.  :::.    .-:::::'.-:::::':::    .,:::::: :::::::..
;;;`    ``;;;;,  `;;;  ;;`;;   ;;;'''' ;;;'''' ;;;    ;;;;'''' ;;;;``;;;;
'[==/[[[[, [[[[[. '[[ ,[[ '[[, [[[,,== [[[,,== [[[     [[cccc   [[[,/[[['
  '''    $ $$$ 'Y$c$$c$$$cc$$$c`$$$'`` `$$$'`` $$'     $$""   $$$$$$c
 88b    dP 888    Y88 888   888,888     888   o88oo,.__888oo,__ 888b '88bo,
  'YMmMY'  MMM     YM YMM   ''` 'MM,    'MM,  ''''YUMMM''''YUMMMMMMM   'W'
                         by l0ss and Sh3r4 - github.com/SnaffCon/Snaffler

2022-03-31 12:16:54 -07:00 [Share] {Black}(\\ACADEMY-EA-MS01.INLANEFREIGHT.LOCAL\ADMIN$)
2022-03-31 12:16:54 -07:00 [Share] {Black}(\\ACADEMY-EA-MS01.INLANEFREIGHT.LOCAL\C$)
2022-03-31 12:16:54 -07:00 [Share] {Green}(\\ACADEMY-EA-MX01.INLANEFREIGHT.LOCAL\address)
2022-03-31 12:16:54 -07:00 [Share] {Green}(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares)
2022-03-31 12:16:54 -07:00 [Share] {Green}(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\User Shares)
2022-03-31 12:16:54 -07:00 [Share] {Green}(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\ZZZ_archive)
2022-03-31 12:17:18 -07:00 [Share] {Green}(\\ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL\CertEnroll)
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.kdb$|289B|3/31/2022 12:09:22 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\GroupBackup.kdb) .kdb
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.key$|299B|3/31/2022 12:05:33 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\ShowReset.key) .key
2022-03-31 12:17:19 -07:00 [Share] {Green}(\\ACADEMY-EA-FILE.INLANEFREIGHT.LOCAL\UpdateServicesPackages)
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.kwallet$|302B|3/31/2022 12:04:45 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\WriteUse.kwallet) .kwallet
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.key$|298B|3/31/2022 12:05:10 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\ProtectStep.key) .key
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.ppk$|275B|3/31/2022 12:04:40 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\StopTrace.ppk) .ppk
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.key$|301B|3/31/2022 12:09:17 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\WaitClear.key) .key
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.sqldump$|312B|3/31/2022 12:05:30 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\DenyRedo.sqldump) .sqldump
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.sqldump$|310B|3/31/2022 12:05:02 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\AddPublish.sqldump) .sqldump
2022-03-31 12:17:19 -07:00 [Share] {Green}(\\ACADEMY-EA-FILE.INLANEFREIGHT.LOCAL\WsusContent)
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.keychain$|295B|3/31/2022 12:08:42 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\SetStep.keychain) .keychain
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.tblk$|279B|3/31/2022 12:05:25 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\FindConnect.tblk) .tblk
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.psafe3$|301B|3/31/2022 12:09:33 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\GetUpdate.psafe3) .psafe3
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.keypair$|278B|3/31/2022 12:09:09 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\UnprotectConvertTo.keypair) .keypair
2022-03-31 12:17:19 -07:00 [File] {Black}<KeepExtExactBlack|R|^\.tblk$|280B|3/31/2022 12:05:17 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\ExportJoin.tblk) .tblk
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.mdf$|305B|3/31/2022 12:09:27 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\FormatShow.mdf) .mdf
2022-03-31 12:17:19 -07:00 [File] {Red}<KeepExtExactRed|R|^\.mdf$|299B|3/31/2022 12:09:14 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\LockConfirm.mdf) .mdf

<SNIP>
```

Podemos encontrar contraseñas, claves SSH, archivos de configuración u otros datos que se pueden utilizar para facilitar nuestro acceso. Snaffler codifica por colores la salida y nos proporciona un resumen de los tipos de archivos que se encuentran en los recursos compartidos.

Ahora que tenemos una gran cantidad de datos sobre el dominio `INLANEFREIGHT.LOCAL` (y, con suerte, notas claras y resultados del archivo de registro), necesitamos una forma de correlacionarlos y visualizarlos. Profundicemos en `BloodHound` y veamos cuán poderosa puede ser esta herramienta durante cualquier evaluación de seguridad centrada en AD.

***

## <mark style="color:purple;">Bloodhound</mark>

Como se analizó en la sección anterior, `Bloodhound` es una herramienta excepcional de código abierto que puede identificar rutas de ataque dentro de un entorno AD mediante el análisis de las relaciones entre objetos. Tanto los evaluadores de penetración como los miembros del equipo azul pueden beneficiarse al aprender a utilizar BloodHound para visualizar las relaciones en el dominio. Cuando se usa correctamente y se combina con consultas de cifrado personalizadas, BloodHound puede encontrar fallas de alto impacto, pero difíciles de descubrir, que han estado presentes en el dominio durante años.

Primero, debemos autenticarnos como usuario de dominio desde un host de ataque de Windows ubicado dentro de la red (pero no unido al dominio) o transferir la herramienta a un host unido a un dominio. Hay muchas maneras de lograr esto cubiertas en el módulo [Transferencia de archivos](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md) . Para nuestros propósitos, trabajaremos con `SharpHound.exe` que ya está en el host de ataque, pero vale la pena experimentar transfiriendo la herramienta al host de ataque o nuestra propia VM usando métodos como un `servidor HTTP Python`, `smbserver.py` de Impacket, etc.

Si ejecutamos SharpHound con la opción `--help` , podremos ver las opciones que tenemos disponibles.

#### **SharpHound en acción**

```powershell
PS C:\htb>  .\SharpHound.exe --help

SharpHound 1.0.3
Copyright (C) 2022 SpecterOps

  -c, --collectionmethods    (Default: Default) Collection Methods: Container, Group, LocalGroup, GPOLocalGroup,
                             Session, LoggedOn, ObjectProps, ACL, ComputerOnly, Trusts, Default, RDP, DCOM, DCOnly

  -d, --domain               Specify domain to enumerate

  -s, --searchforest         (Default: false) Search all available domains in the forest

  --stealth                  Stealth Collection (Prefer DCOnly whenever possible!)

  -f                         Add an LDAP filter to the pregenerated filter.

  --distinguishedname        Base DistinguishedName to start the LDAP search at

  --computerfile             Path to file containing computer names to enumerate
  
  <SNIP>
```

Comenzaremos ejecutando el recopilador SharpHound.exe desde el host de ataque MS01.

```powershell
PS C:\htb> .\SharpHound.exe -c All --zipfilename ILFREIGHT

2022-04-18T13:58:22.1163680-07:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, GPOLocalGroup, Session, LoggedOn, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote
2022-04-18T13:58:22.1163680-07:00|INFORMATION|Initializing SharpHound at 1:58 PM on 4/18/2022
2022-04-18T13:58:22.6788709-07:00|INFORMATION|Flags: Group, LocalAdmin, GPOLocalGroup, Session, LoggedOn, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote
2022-04-18T13:58:23.0851206-07:00|INFORMATION|Beginning LDAP search for INLANEFREIGHT.LOCAL
2022-04-18T13:58:53.9132950-07:00|INFORMATION|Status: 0 objects finished (+0 0)/s -- Using 67 MB RAM
2022-04-18T13:59:15.7882419-07:00|INFORMATION|Producer has finished, closing LDAP channel
2022-04-18T13:59:16.1788930-07:00|INFORMATION|LDAP channel closed, waiting for consumers
2022-04-18T13:59:23.9288698-07:00|INFORMATION|Status: 3793 objects finished (+3793 63.21667)/s -- Using 112 MB RAM
2022-04-18T13:59:45.4132561-07:00|INFORMATION|Consumers finished, closing output channel
Closing writers
2022-04-18T13:59:45.4601086-07:00|INFORMATION|Output channel closed, waiting for output task to complete
2022-04-18T13:59:45.8663528-07:00|INFORMATION|Status: 3809 objects finished (+16 46.45122)/s -- Using 110 MB RAM
2022-04-18T13:59:45.8663528-07:00|INFORMATION|Enumeration finished in 00:01:22.7919186
2022-04-18T13:59:46.3663660-07:00|INFORMATION|SharpHound Enumeration Completed at 1:59 PM on 4/18/2022! Happy Graphing
```

A continuación, podemos extraer el conjunto de datos a nuestra propia máquina virtual o ingerirlo en la herramienta `GUI BloodHound` en MS01. Podemos hacer esto en MS01 escribiendo `bloodhound` en una consola CMD o PowerShell. Las credenciales deben guardarse, pero ingréselas `neo4j: HTB_@cademy_stdnt!` si aparece un mensaje. A continuación, haga clic en el botón  `Upload Data` del lado derecho, seleccione el archivo zip recién generado y haga clic en `Open`. Aparecerá una ventana `Upload Progress`. Una vez que todos los archivos .json estén 100% completos, haga clic en la X en la parte superior de esa ventana.

Podemos empezar escribiendo `domain:` en la barra de búsqueda de la parte superior izquierda y eligiendo `INLANEFREIGHT.LOCAL` entre los resultados. Tómate un momento para explorar la pestaña de información del nodo. Como podemos ver, esta sería una empresa bastante grande con más de 550 hosts a los que apuntar y fideicomisos con otros dos dominios.

Ahora, veamos algunas consultas predefinidas en la pestaña `Analysis`. La consulta `Find Computers with Unsupported Operating Systems` es excelente para encontrar sistemas operativos obsoletos y sin soporte que ejecutan software heredado. Estos sistemas son relativamente comunes de encontrar dentro de las redes empresariales (especialmente en entornos más antiguos), ya que a menudo ejecutan algún producto que aún no se puede actualizar o reemplazar. Mantener estos hosts puede ahorrar dinero, pero también pueden agregar vulnerabilidades innecesarias a la red. Los hosts más antiguos pueden ser susceptibles a vulnerabilidades de ejecución de código remoto más antiguas como [MS08-067](https://support.microsoft.com/en-us/topic/ms08-067-vulnerability-in-server-service-could-allow-remote-code-execution-ac7878fc-be69-7143-472d-2507a179cd15) . Si nos encontramos con estos hosts más antiguos durante una evaluación, debemos tener cuidado antes de atacarlos (o incluso consultar con nuestro cliente), ya que pueden ser frágiles y ejecutar una aplicación o servicio crítico. Podemos recomendar a nuestro cliente que segmente estos hosts del resto de la red tanto como sea posible si aún no pueden eliminarlos, pero también debemos recomendar que comiencen a elaborar un plan para desmantelarlos y reemplazarlos.

Esta consulta muestra dos hosts, uno que ejecuta Windows 7 y otro que ejecuta Windows Server 2008 (ninguno de ellos está "activo" en nuestro laboratorio). A veces, veremos hosts que ya no están encendidos, pero que aún aparecen como registros en AD. Siempre debemos validar si están "activos" o no antes de hacer recomendaciones en nuestros informes. Podemos escribir un hallazgo de alto riesgo para sistemas operativos heredados o una recomendación de mejores prácticas para limpiar registros antiguos en AD.

### **Sistemas operativos no compatibles**

![texto](https://academy.hackthebox.com/storage/modules/143/unsupported.png)

A menudo, veremos usuarios con derechos de administrador local en su host (quizás temporalmente para instalar un software, y los derechos nunca se eliminaron), o ocupan un rol lo suficientemente alto en la organización como para exigir estos derechos (ya sea que los requieran o no). Otras veces, veremos derechos de administrador local excesivos otorgados en toda la organización, como múltiples grupos en el departamento de TI con administrador local sobre grupos de servidores o incluso todo el grupo de usuarios del dominio con administrador local sobre uno o más hosts.&#x20;

Esto puede beneficiarnos si tomamos el control de una cuenta de usuario con estos derechos sobre una o más máquinas. Podemos ejecutar la consulta `Find Computers where Domain Users are Local Admin` para ver rápidamente si hay algún host donde todos los usuarios tengan derechos de administrador local. Si este es el caso, entonces cualquier cuenta que controlemos normalmente se puede usar para acceder al host o hosts en cuestión, y es posible que podamos recuperar credenciales de la memoria o encontrar otros datos confidenciales.

### **Administradores locales**

![texto](https://academy.hackthebox.com/storage/modules/143/local-admin.png)

Esta es solo una pequeña muestra de las consultas útiles que podemos ejecutar. A medida que avancemos en este módulo, verá varias más que pueden resultar útiles para encontrar otras debilidades en el dominio. Para un estudio más profundo de BloodHound, consulte el módulo [`Bloodhound`](#bloodhound) . Tómese un tiempo y pruebe cada una de las consultas de la pestaña `Analysis` para familiarizarse más con la herramienta. También vale la pena experimentar con [consultas Cypher personalizadas](https://hausec.com/2019/09/09/bloodhound-cypher-cheatsheet/) pegándolas en el cuadro `Raw Query` en la parte inferior de la pantalla.

Tenga en cuenta que a medida que avanzamos en la interacción, debemos documentar cada archivo que se transfiere hacia y desde los hosts del dominio y dónde se colocaron en el disco. Esta es una buena práctica si tenemos que desconflictar nuestras acciones con el cliente. Además, dependiendo del alcance del compromiso, debes asegurarte de cubrir tus huellas y limpiar todo lo que coloques en el medio ambiente al finalizar el compromiso.

***

## <mark style="color:purple;">Caso práctico</mark>

```
RDP a 10.129.81.106 (ACADEMY-EA-MS01)
Usuario " htb-student "
Contraseña " Academy_student_AD! "
```

### Pregunta 1

Con Bloodhound, determine cuántas cuentas Kerberoastable existen dentro del dominio INLANEFREIGHT.

```powershell
PS C:\htb> .\SharpHound.exe -c All --zipfilename ILFREIGHT

<-----SNIP----->
2024-07-01T10:36:14.0053266-07:00|INFORMATION|Consumers finished, closing output channel
2024-07-01T10:36:14.0521360-07:00|INFORMATION|Output channel closed, waiting for output task to complete
Closing writers
2024-07-01T10:36:14.1927443-07:00|INFORMATION|Status: 3809 objects finished (+16 58.6)/s -- Using 122 MB RAM
2024-07-01T10:36:14.1927443-07:00|INFORMATION|Enumeration finished in 00:01:05.2323651
2024-07-01T10:36:14.5521146-07:00|INFORMATION|SharpHound Enumeration Completed at 10:36 AM on 7/1/2024! Happy Graphing!
```

```powershell
PS C:\Tools> ls

    Directory: C:\Tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        4/18/2022  11:23 AM                BloodHound-GUI
-a----         3/8/2022   8:37 PM         906752 SharpHound.exe
-a----         7/1/2024  10:36 AM         261119 20240701103556_ILFREIGHT.zip
```

Una vez que tenemos el .zip vamos a importarlo en BloodHound:

<figure><img src="/files/glmhA9RYLg1KbD1HBsSb" alt=""><figcaption></figcaption></figure>

Con domain: encontramos 3 dominios dentro de esta red. En la parte de Analysis hay un apartado específico para encontrar usuarios Kerberoasteables:

<figure><img src="/files/Hf4wV9A45UD07Ad9sd04" alt=""><figcaption></figcaption></figure>

Encontramos `13 usuarios Kerberoasteables`, y `4` de ellos pertenecen a grupos privilegiados:

<figure><img src="/files/cRejLmTiMZp9LVjMGjlE" alt=""><figcaption></figcaption></figure>

`SQLDEV` puede ser un buen usuario para comprometer, ya que pertenece al grupo Domain Admins y puede tener las claves para acceder a la base de datos

También encontramos 2 máquinas con software obsoleto en ese sistema, lo cual las convierten en un objetivo vulnerable dentro de esta organización:

<figure><img src="/files/a0Gbbnj87IF3DxIG9vDf" alt=""><figcaption></figcaption></figure>

### Pregunta 2

Ejecute Snaffler y busque un archivo de configuración web legible. ¿Cuál es el nombre del usuario que aparece en la cadena de conexión dentro del archivo?

```powershell
PS C:\Tools> .\Snaffler.exe -s -d inlanefreight.local -o snaffler.log -v data
PS C:\Tools> Get-Content .\snaffler.log
2024-07-01 11:02:26 -07:00 [Share] {Black}(\\ACADEMY-EA-MS01.INLANEFREIGHT.LOCAL\ADMIN$)
2024-07-01 11:02:26 -07:00 [Share] {Black}(\\ACADEMY-EA-MS01.INLANEFREIGHT.LOCAL\C$)
2024-07-01 11:02:26 -07:00 [Share] {Green}(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares)
2024-07-01 11:02:26 -07:00 [Share] {Green}(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\User Shares)
2024-07-01 11:02:26 -07:00 [Share] {Green}(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\ZZZ_archive)
2024-07-01 11:02:52 -07:00 [File] {Red}<KeepExtExactRed|RW|^\.key$|299B|3/31/2022 12:05:33 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\ShowReset.key) .key
2024-07-01 11:02:52 -07:00 [File] {Red}<KeepExtExactRed|RW|^\.key$|298B|3/31/2022 12:05:10 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Infosec\ProtectStep.key) .key
```

Una vez que tenemos el archivo .log podemos buscar por archivos de configuración con estos comandos:

```powershell
# Lee el archivo de log y filtra líneas que mencionen archivos de configuración web
$logFile = "C:\Tools\snaffler.log"
$configFiles = Get-Content $logFile | Where-Object { $_ -match 'web.config|appsettings.json' }

# Muestra las rutas de los archivos de configuración encontrados
$configFiles

PS C:\Users\htb-student\Desktop> $configFiles
2024-07-01 11:02:52 -07:00 [File] {Red}<KeepConfigRegexRed|RW|connectionstring[[:space:]]*=[[:space:]]*[\'\"][^\'\"].....*|253B|3/31/2022 12:12:43 PM>(\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\web.config) <?xml version="1.0" encoding="utf-8"?>
```

Una vez que hemos encontrado el archivo de configuración podemos leerlo por Powershell con los siguiente comandos:

```powershell
# Ruta del archivo de configuración
$filePath = "\\ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Development\web.config"

# Leer el contenido del archivo de configuración
$configContent = Get-Content -LiteralPath $filePath

# Mostrar el contenido del archivo
$configContent

PS C:\Users> $configContent
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <connectionStrings>
    <add name="myConnectionString" connectionString="server=ACADEMY-EA-DB01;database=Employees;uid=sa;password=ILFREIGHTDB01!;" />
  </connectionStrings>
</configuration>
```

Buuum! Encontramos las credenciales para acceder a la base de datos de un usuario administrador `sa` (sysadmin):

```
server=ACADEMY-EA-DB01;
database=Employees;
uid=sa;
password=ILFREIGHTDB01!;
```

***

Tenemos una excelente imagen del diseño, las fortalezas y las debilidades del dominio. Tenemos credenciales para varios usuarios y hemos enumerado una gran cantidad de información, como usuarios, grupos, computadoras, GPO, ACL, derechos de administrador local, derechos de acceso (RDP, WinRM, etc.), cuentas configuradas con nombres principales de servicio (SPN). y más. Tenemos notas detalladas y una gran cantidad de resultados y experimentamos con muchas herramientas diferentes para practicar la enumeración de AD con y sin credenciales en hosts de ataque de Linux y Windows.&#x20;

¿Qué pasa si estamos restringidos con el shell que tenemos o no tenemos la capacidad de importar herramientas? Nuestro cliente puede pedirnos que realicemos todo el trabajo desde un host administrado dentro de su red sin acceso a Internet y sin forma de cargar nuestras herramientas. Podríamos aterrizar en un host como `SYSTEM` después de un ataque exitoso, pero estar en una posición en la que es muy difícil o no posible cargar herramientas. ¿Qué hacemos entonces? En la siguiente sección, veremos distintas acciones.
