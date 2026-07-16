
# Active Directory Primer

Todo el contenido de esta sección se encuentra completo y mucho mejor explicado en la sección:

{% content-ref url="/pages/7fv7EEbu7KK1gMw2Jfhe" %}
[Active Directory](/ethical-hacking-cheatsheet/active-directory/active-directory.md)
{% endcontent-ref %}

## <mark style="color:purple;">1. Introducción a Active Directory</mark>

#### ¿Qué es Active Directory?

Active Directory (AD) es un servicio de directorio desarrollado por Microsoft para redes de dominio Windows. Funciona como una **base de datos centralizada** que almacena información sobre objetos de la red (usuarios, equipos, grupos, recursos) y proporciona servicios de autenticación y autorización.

#### **¿Por qué es importante?**

* Permite a los administradores gestionar toda la red desde un solo lugar
* Centraliza la autenticación (un solo usuario y contraseña para acceder a múltiples recursos)
* Facilita la aplicación de políticas de seguridad a nivel de toda la organización
* Escala desde pequeñas empresas hasta grandes corporaciones con miles de objetos

#### **Componentes principales**

* **Domain Controller (DC)**: Servidor que ejecuta Active Directory Domain Services (AD DS)
* **Base de datos NTDS.dit**: Archivo que almacena todos los objetos del directorio
* **Sysvol**: Carpeta compartida que contiene scripts, políticas de grupo (GPOs) y otros archivos necesarios para la replicación entre DCs
* **Global Catalog (GC)**: Índice parcial de todos los objetos del bosque, almacenado en servidores designados como Global Catalog Servers. Acelera las búsquedas entre dominios

### Cheatsheet

<table data-header-hidden><thead><tr><th width="201.5"></th><th></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando (PowerShell)</td><td>Comando (CMD)</td></tr><tr><td>Ver dominio actual</td><td><code>(Get-ADDomain).Name</code></td><td><code>echo %userdomain%</code></td></tr><tr><td>Ver DC actual</td><td><code>$env:LOGONSERVER</code></td><td><code>echo %logonserver%</code></td></tr><tr><td>Listar todos los DCs</td><td><code>Get-ADDomainController -Filter *</code></td><td><code>nltest /dclist:&#x3C;domain></code></td></tr><tr><td>Ver información del dominio</td><td><code>Get-ADDomain</code></td><td><code>nltest /domain_trusts</code></td></tr><tr><td>Ver forest</td><td><code>Get-ADForest</code></td><td><code>nltest /dsgetdc:&#x3C;domain></code></td></tr><tr><td>Ver versión de AD (nivel funcional)</td><td><code>(Get-ADDomain).DomainMode</code></td><td><code>netdom query fsmo</code></td></tr></tbody></table>

***

## <mark style="color:purple;">2. Usuarios</mark>

#### ¿Qué es un usuario en Active Directory?

Un usuario en AD representa una **identidad digital** que permite a una persona autenticarse en la red y acceder a recursos según sus permisos. Cada usuario tiene atributos como nombre, apellido, nombre de inicio de sesión, contraseña, grupos a los que pertenece, etc.

#### **Tipos de cuentas de usuario:**

<table data-header-hidden><thead><tr><th width="198.1666259765625"></th><th></th><th></th></tr></thead><tbody><tr><td>Tipo</td><td>Descripción</td><td>Ejemplo</td></tr><tr><td><strong>Usuario normal</strong></td><td>Cuentas para personas reales</td><td><code>jperez</code>, <code>mrodriguez</code></td></tr><tr><td><strong>Cuenta de servicio</strong></td><td>Para ejecutar aplicaciones o servicios</td><td><code>svc_sql</code>, <code>svc_backup</code></td></tr><tr><td><strong>Administrador</strong></td><td>Cuenta con privilegios elevados</td><td><code>Administrator</code> (built-in)</td></tr><tr><td><strong>Administrador de dominio</strong></td><td>Miembro del grupo "Domain Admins"</td><td>Puede administrar todo el dominio</td></tr><tr><td><strong>Usuario invitado</strong></td><td>Acceso limitado, deshabilitado por defecto</td><td><code>Guest</code></td></tr></tbody></table>

#### **Atributos importantes de un usuario**

* **sAMAccountName**: Nombre de inicio de sesión (ej: `jperez`)
* **userPrincipalName (UPN)**: Formato de correo (ej: `jperez@contoso.com`)
* **objectSid**: Identificador único (SID) del objeto
* **userAccountControl**: Flags que definen el estado de la cuenta (habilitada, deshabilitada, requiere cambio de contraseña, etc.)

### Comandos para usuarios

<table data-header-hidden><thead><tr><th width="198.166748046875"></th><th></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando (PowerShell con RSAT)</td><td>Comando (CMD / nativo)</td></tr><tr><td>Listar usuarios del dominio</td><td><code>Get-ADUser -Filter *</code></td><td><code>net user /domain</code></td></tr><tr><td>Ver detalles de un usuario</td><td><code>Get-ADUser jperez -Properties *</code></td><td><code>net user jperez /domain</code></td></tr><tr><td>Crear un usuario</td><td><code>New-ADUser -Name "Juan Perez" -GivenName Juan -Surname Perez -SamAccountName jperez -UserPrincipalName jperez@contoso.com -AccountPassword (ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force) -Enabled $true</code></td><td><code>net user jperez P@ssw0rd /add /domain</code></td></tr><tr><td>Habilitar/Deshabilitar usuario</td><td><code>Enable-ADAccount -Identity jperez</code> / <code>Disable-ADAccount -Identity jperez</code></td><td><code>net user jperez /active:yes</code> / <code>net user jperez /active:no</code></td></tr><tr><td>Cambiar contraseña</td><td><code>Set-ADAccountPassword -Identity jperez -NewPassword (ConvertTo-SecureString "NuevaP@ss" -AsPlainText -Force) -Reset</code></td><td><code>net user jperez * /domain</code></td></tr><tr><td>Buscar usuarios por atributo</td><td><code>Get-ADUser -Filter "Name -like '*admin*'"</code></td><td><code>net user | findstr /i admin</code></td></tr><tr><td>Ver último logon</td><td><code>Get-ADUser jperez -Properties LastLogonDate</code></td><td>No directo</td></tr><tr><td>Desbloquear usuario</td><td><code>Unlock-ADAccount -Identity jperez</code></td><td><code>net user jperez /active:yes</code></td></tr><tr><td>Eliminar usuario</td><td><code>Remove-ADUser -Identity jperez</code></td><td><code>net user jperez /delete</code></td></tr></tbody></table>

***

## <mark style="color:purple;">3. Grupos</mark>

#### ¿Qué son los grupos en Active Directory?

Los grupos son contenedores lógicos que permiten **gestionar permisos de forma colectiva** en lugar de asignarlos usuario por usuario. Cuando asignas permisos a un grupo, todos sus miembros heredan esos permisos automáticamente.

#### **Tipos de grupos**

<table data-header-hidden><thead><tr><th width="158.1666259765625"></th><th></th><th></th></tr></thead><tbody><tr><td>Tipo</td><td>Alcance</td><td>Se puede usar para...</td></tr><tr><td><strong>Domain Local</strong></td><td>Asignar permisos sobre recursos dentro del mismo dominio</td><td>Permisos a carpetas compartidas, impresoras dentro del dominio</td></tr><tr><td><strong>Global</strong></td><td>Agrupar usuarios del mismo dominio; puede anidarse en otros grupos</td><td>Agrupar usuarios por departamento (ej: "Ventas Global")</td></tr><tr><td><strong>Universal</strong></td><td>Disponible en todo el bosque, útil para múltiples dominios</td><td>Proyectos que involucran varios dominios</td></tr></tbody></table>

#### **Grupos especiales y predeterminados**

<table data-header-hidden><thead><tr><th width="198.166748046875"></th><th></th><th></th></tr></thead><tbody><tr><td>Grupo</td><td>Descripción</td><td>Privilegios</td></tr><tr><td><strong>Domain Admins</strong></td><td>Administradores del dominio</td><td>Control total sobre el dominio</td></tr><tr><td><strong>Enterprise Admins</strong></td><td>Administradores del bosque</td><td>Control total sobre todos los dominios del bosque (solo existe en el dominio raíz)</td></tr><tr><td><strong>Administrators</strong></td><td>Administradores locales en todos los equipos del dominio</td><td>Control local en cada máquina</td></tr><tr><td><strong>Domain Controllers</strong></td><td>Controladores de dominio</td><td>Pueden replicar el directorio</td></tr><tr><td><strong>Schema Admins</strong></td><td>Pueden modificar el esquema de AD</td><td>Extremadamente poderoso, raramente usado</td></tr><tr><td><strong>Domain Users</strong></td><td>Todos los usuarios del dominio</td><td>Grupo por defecto</td></tr><tr><td><strong>Domain Computers</strong></td><td>Todos los equipos unidos al dominio</td><td></td></tr><tr><td><strong>Protected Users</strong></td><td>Protección adicional (no credenciales en caché, no delegación)</td><td>Grupo de seguridad desde Windows Server 2012 R2</td></tr></tbody></table>

**Anidamiento de grupos:** Los grupos pueden contener otros grupos. Por ejemplo, "Ventas Global" (grupo global) puede ser miembro de "Permisos Carpeta Ventas" (grupo domain local).

### Comandos para grupos

<table data-header-hidden><thead><tr><th width="194.833251953125"></th><th></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando (PowerShell)</td><td>Comando (CMD)</td></tr><tr><td>Listar grupos</td><td><code>Get-ADGroup -Filter *</code></td><td><code>net group /domain</code></td></tr><tr><td>Ver miembros de un grupo</td><td><code>Get-ADGroupMember -Identity "Domain Admins"</code></td><td><code>net group "Domain Admins" /domain</code></td></tr><tr><td>Crear grupo</td><td><code>New-ADGroup -Name "Ventas" -GroupScope Global -GroupCategory Security</code></td><td><code>net group Ventas /add /domain</code></td></tr><tr><td>Agregar usuario a grupo</td><td><code>Add-ADGroupMember -Identity Ventas -Members jperez</code></td><td><code>net group Ventas jperez /add /domain</code></td></tr><tr><td>Remover usuario de grupo</td><td><code>Remove-ADGroupMember -Identity Ventas -Members jperez</code></td><td><code>net group Ventas jperez /delete /domain</code></td></tr><tr><td>Ver grupos de un usuario</td><td><code>Get-ADUser jperez -Properties MemberOf | Select-Object -ExpandProperty MemberOf</code></td><td><code>net user jperez /domain</code></td></tr><tr><td>Ver grupos anidados</td><td><code>Get-ADGroup -Identity Ventas -Properties Members</code></td><td>No directo</td></tr><tr><td>Eliminar grupo</td><td><code>Remove-ADGroup -Identity Ventas</code></td><td><code>net group Ventas /delete /domain</code></td></tr></tbody></table>

***

## <mark style="color:purple;">4. Computers</mark>

#### ¿Qué son los equipos en Active Directory?

Los objetos **Computer** representan estaciones de trabajo, servidores y otros dispositivos que se han **unido al dominio**. Cuando un equipo se une al dominio, se crea una cuenta de equipo (con un sufijo `$` en su nombre, ej: `PC-JUAN$`). Estas cuentas también tienen una contraseña (cambiada automáticamente cada 30 días) que permite al equipo autenticarse en el dominio.

#### **¿Por qué son importantes?**

* Permiten aplicar políticas de grupo (GPO) a equipos específicos
* Controlan qué equipos pueden acceder a recursos de red
* Facilitan la administración remota y la implementación de software

#### **Atributos importantes**

* **OperatingSystem**: Versión de Windows
* **IPv4Address**: Dirección IP del equipo
* **LastLogonDate**: Cuándo se autenticó por última vez
* **Primary Group**: Generalmente "Domain Computers"

### Comandos para equipos

<table data-header-hidden><thead><tr><th width="214.8333740234375"></th><th></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando (PowerShell)</td><td>Comando (CMD)</td></tr><tr><td>Listar equipos del dominio</td><td><code>Get-ADComputer -Filter *</code></td><td><code>net view</code> (limitado)</td></tr><tr><td>Ver detalles de un equipo</td><td><code>Get-ADComputer PC-JUAN -Properties *</code></td><td><code>nltest /server:PC-JUAN</code></td></tr><tr><td>Buscar equipos por SO</td><td><code>Get-ADComputer -Filter "OperatingSystem -like '*Server*'"</code></td><td>No directo</td></tr><tr><td>Ver equipos activos (último logon reciente)</td><td><code>Get-ADComputer -Filter * -Properties LastLogonDate | Where-Object { $_.LastLogonDate -gt (Get-Date).AddDays(-30) }</code></td><td>No directo</td></tr><tr><td>Deshabilitar cuenta de equipo</td><td><code>Disable-ADAccount -Identity PC-JUAN$</code></td><td><code>net user PC-JUAN$ /active:no</code></td></tr><tr><td>Unir equipo al dominio (local)</td><td><code>Add-Computer -DomainName contoso.com -Credential (Get-Credential)</code></td><td>No directo</td></tr><tr><td>Salir del dominio (local)</td><td><code>Remove-Computer -UnjoinDomaincredential (Get-Credential) -Restart</code></td><td>No directo</td></tr><tr><td>Ver DC autenticado por un equipo</td><td><code>nltest /dsgetdc:contoso.com</code></td><td><code>nltest /dsgetdc:contoso.com</code></td></tr></tbody></table>

***

## <mark style="color:purple;">5. Organizational Units (OUs)</mark>

#### ¿Qué son las Organizational Units?

Las **Unidades Organizativas (OUs)** son contenedores dentro de un dominio que permiten **estructurar y organizar objetos** (usuarios, grupos, equipos) de forma jerárquica. Son similares a las carpetas en un sistema de archivos. A diferencia de los grupos (que se usan para permisos), las OUs se usan principalmente para **delegar administración** y **aplicar políticas de grupo (GPOs)**.

#### **Estructura típica de OUs**

```
contoso.com (dominio)
├── Ventas
│   ├── Usuarios
│   ├── Equipos
│   └── Grupos
├── IT
│   ├── Usuarios
│   ├── Servidores
│   └── Estaciones
├── RRHH
└── Administracion
```

#### **¿Para qué sirven las OUs?**

* **Delegación administrativa**: Dar control limitado a un usuario sobre una OU específica (ej: que el administrador de ventas pueda resetear contraseñas solo de usuarios de Ventas)
* **Aplicación de GPOs**: Las políticas de grupo pueden aplicarse a nivel de OU, permitiendo configuraciones diferentes por departamento
* **Organización lógica**: Facilitar la administración y el descubrimiento de objetos

#### **Diferencia entre OUs y Grupos**

<table data-header-hidden><thead><tr><th width="161.5"></th><th></th><th></th></tr></thead><tbody><tr><td><strong>Característica</strong></td><td><strong>OUs</strong></td><td><strong>Grupos</strong></td></tr><tr><td>Propósito</td><td>Organización estructural</td><td>Asignación de permisos</td></tr><tr><td>Anidamiento</td><td>Sí (jerárquico)</td><td>Sí (pero con alcances)</td></tr><tr><td>GPOs</td><td>Se aplican a OUs</td><td>No se aplican directamente</td></tr><tr><td>Delegación</td><td>Sí</td><td>No</td></tr><tr><td>Contiene</td><td>Usuarios, equipos, otros OUs</td><td>Usuarios, equipos, otros grupos</td></tr></tbody></table>

### Comandos para OUs

<table data-header-hidden><thead><tr><th width="159.8333740234375"></th><th></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando (PowerShell)</td><td>Comando (CMD/DSQuery)</td></tr><tr><td>Listar OUs</td><td><code>Get-ADOrganizationalUnit -Filter *</code></td><td><code>dsquery ou</code></td></tr><tr><td>Ver detalles de una OU</td><td><code>Get-ADOrganizationalUnit -Identity "OU=Ventas,DC=contoso,DC=com" -Properties *</code></td><td><code>dsquery ou -name Ventas</code></td></tr><tr><td>Crear OU</td><td><code>New-ADOrganizationalUnit -Name "Ventas" -Path "DC=contoso,DC=com"</code></td><td><code>dsadd ou "OU=Ventas,DC=contoso,DC=com"</code></td></tr><tr><td>Mover objeto a OU</td><td><code>Move-ADObject -Identity "CN=jperez,CN=Users,DC=contoso,DC=com" -TargetPath "OU=Ventas,DC=contoso,DC=com"</code></td><td><code>dsmove</code></td></tr><tr><td>Eliminar OU</td><td><code>Remove-ADOrganizationalUnit -Identity "OU=Ventas,DC=contoso,DC=com"</code></td><td><code>dsrm "OU=Ventas,DC=contoso,DC=com"</code></td></tr><tr><td>Ver objetos dentro de OU</td><td><code>Get-ADUser -Filter * -SearchBase "OU=Ventas,DC=contoso,DC=com"</code></td><td><code>dsquery user -name * -searchbase "OU=Ventas,DC=contoso,DC=com"</code></td></tr></tbody></table>

***

## <mark style="color:purple;">6. Active Directory Authentication</mark>

#### ¿Cómo funciona la autenticación en Active Directory?

Active Directory utiliza dos protocolos principales para autenticar usuarios y equipos: **Kerberos** (por defecto desde Windows 2000) y **NTLM** (legado, por compatibilidad).

#### Kerberos (Protocolo principal)

Kerberos es un protocolo de autenticación basado en **tickets** que permite la autenticación mutua entre el cliente y el servidor sin enviar contraseñas por la red.

#### **Flujo de autenticación Kerberos:**

```
1. Cliente → AS (Authentication Service): Solicita TGT (Ticket Granting Ticket)
2. AS → Cliente: TGT (cifrado con clave del KDC) + session key
3. Cliente → TGS (Ticket Granting Service): TGT + solicitud de ticket para servicio específico
4. TGS → Cliente: Service Ticket (cifrado con clave del servicio)
5. Cliente → Servicio: Service Ticket
6. Servicio → Cliente: Autenticación confirmada
```

#### **Componentes clave**

<table data-header-hidden><thead><tr><th width="280.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Componente</td><td>Descripción</td></tr><tr><td><strong>KDC (Key Distribution Center)</strong></td><td>Servicio que emite tickets, corre en el Domain Controller</td></tr><tr><td><strong>AS (Authentication Service)</strong></td><td>Valida credenciales y emite TGT</td></tr><tr><td><strong>TGS (Ticket Granting Service)</strong></td><td>Emite tickets para servicios específicos</td></tr><tr><td><strong>TGT (Ticket Granting Ticket)</strong></td><td>Ticket inicial, válido por 10 horas (por defecto)</td></tr><tr><td><strong>Service Ticket</strong></td><td>Ticket para acceder a un recurso específico (ej: SQL Server, archivo compartido)</td></tr><tr><td><strong>PAC (Privilege Attribute Certificate)</strong></td><td>Contiene los SIDs del usuario (miembroships de grupos)</td></tr></tbody></table>

#### NTLM (Legado)

NTLM es un protocolo de autenticación por **desafío-respuesta** (challenge-response). Se usa cuando Kerberos no está disponible (ej: servidores antiguos, aplicaciones no compatibles).

**Flujo NTLM:**

```
1. Cliente → Servidor: Solicita acceso
2. Servidor → Cliente: Challenge (número aleatorio)
3. Cliente → Servidor: Respuesta = Hash(NTLM) cifrado con el challenge
4. Servidor → DC: Reenvía credenciales al Domain Controller
5. DC → Servidor: Verificación (éxito/fracaso)
```

### Cheatsheet - Autenticación

<table data-header-hidden><thead><tr><th width="251.5"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando / Explicación</td></tr><tr><td>Ver ticket Kerberos actual</td><td><code>klist</code></td></tr><tr><td>Renovar tickets</td><td><code>klist purge</code> (borrar) / <code>klist get &#x3C;SPN></code> (obtener nuevo)</td></tr><tr><td>Ver información de dominio para Kerberos</td><td><code>nltest /dsgetdc:contoso.com /kdc</code></td></tr><tr><td>Forzar autenticación NTLM (net use)</td><td><code>net use \\server\share /user:contoso\jperez *</code></td></tr><tr><td>Ver sesiones NTLM activas</td><td><code>net session</code></td></tr><tr><td>Kerberos SPN (Service Principal Name)</td><td><code>setspn -L jperez</code> (ver SPNs asociados a un usuario)</td></tr><tr><td>Ticket Golden (ataque)</td><td>Creación de TGT falso con krbtgt hash</td></tr><tr><td>Ticket Silver (ataque)</td><td>Creación de Service Ticket falso para un servicio específico</td></tr></tbody></table>

***

## <mark style="color:purple;">7. Trees, Forests & Trusts</mark>

### Trees (Árboles)

Un **Tree** es una colección de uno o más **dominios** que comparten un **namespace contiguo** (espacio de nombres continuo) y una relación de confianza **automática bidireccional transitiva**.

#### **Ejemplo de Tree**

```
contoso.com (dominio raíz)
├── europe.contoso.com
├── asia.contoso.com
└── america.contoso.com
```

#### **Características:**

* Todos los dominios comparten el mismo esquema y configuración global
* Las relaciones de confianza son automáticas entre padres e hijos
* El dominio padre puede administrar políticas para los dominios hijos

### Forests (Bosques)

Un **Forest** es el contenedor de más alto nivel en Active Directory. Es una colección de uno o más **Trees** (árboles de dominios) que comparten un **esquema común**, una **configuración global** y **catálogos globales**. Los bosques proporcionan un límite de seguridad: lo que ocurre en un bosque no afecta a otro bosque a menos que se establezcan trusts explícitos.

#### **Ejemplo de Forest**

```
Forest: contoso.local
├── Tree 1: contoso.local
│   ├── europe.contoso.local
│   └── asia.contoso.local
└── Tree 2: fabrikam.local (namespace diferente)
    └── us.fabrikam.local
```

#### **Componentes únicos por Forest**

* **Schema**: Definición de todos los tipos de objetos y atributos
* **Configuration partition**: Configuración de la topología del forest
* **Enterprise Admins group**: Administradores de todo el forest
* **Schema Admins group**: Pueden modificar el esquema

### Trusts (Relaciones de confianza)

Las **Trusts** (relaciones de confianza) permiten que usuarios de un dominio accedan a recursos de otro dominio. Determinan cómo se extiende la autenticación entre dominios.

#### **Tipos de Trusts**

<table data-header-hidden><thead><tr><th width="135.33331298828125"></th><th width="170.8333740234375"></th><th width="154"></th><th></th></tr></thead><tbody><tr><td>Tipo</td><td>Dirección</td><td>Transitividad</td><td>Descripción</td></tr><tr><td><strong>Parent-Child</strong></td><td>Bidireccional</td><td>Transitiva</td><td>Automática entre dominio padre e hijo</td></tr><tr><td><strong>Tree-Root</strong></td><td>Bidireccional</td><td>Transitiva</td><td>Automática entre la raíz de un tree y otro tree en el mismo forest</td></tr><tr><td><strong>Shortcut</strong></td><td>Unidireccional o bidireccional</td><td>Transitiva</td><td>Manual, acelera autenticación entre dominios que no son padre-hijo</td></tr><tr><td><strong>Forest</strong></td><td>Unidireccional o bidireccional</td><td>Transitiva o no</td><td>Conexión entre dos bosques diferentes</td></tr><tr><td><strong>External</strong></td><td>Unidireccional</td><td>No transitiva</td><td>Conexión a un dominio fuera del forest (NT4, AD)</td></tr><tr><td><strong>Realm</strong></td><td>Unidireccional o bidireccional</td><td>Transitiva o no</td><td>Conexión con un Realm de Kerberos no Windows</td></tr></tbody></table>

#### **Dirección de la confianza**

* **Bidireccional**: Usuarios de Domain A acceden a recursos de Domain B y viceversa
* **Unidireccional**: Solo usuarios de Domain A pueden acceder a recursos de Domain B (no al revés)

#### **Transitividad**

* **Transitiva**: Si A confía en B y B confía en C, entonces A confía en C automáticamente
* **No transitiva**: La confianza termina en el dominio especificado

### Cheatsheet - Trees, Forests & Trusts

<table data-header-hidden><thead><tr><th width="185.66668701171875"></th><th></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando (PowerShell)</td><td>Comando (CMD)</td></tr><tr><td>Ver forest actual</td><td><code>Get-ADForest</code></td><td><code>nltest /dsgetdc:&#x3C;domain> /forest</code></td></tr><tr><td>Ver dominios en el forest</td><td><code>(Get-ADForest).Domains</code></td><td><code>nltest /domain_trusts /forest</code></td></tr><tr><td>Ver trusts del dominio</td><td><code>Get-ADTrust -Filter *</code></td><td><code>nltest /domain_trusts /all_trusts</code></td></tr><tr><td>Ver detalles de un trust</td><td><code>Get-ADTrust -Identity "contoso.local"</code></td><td><code>nltest /server:&#x3C;dc> /trusted_domains</code></td></tr><tr><td>Ver esquema del forest</td><td><code>Get-ADObject -SearchBase (Get-ADForest).SchemaNamingContext</code></td><td>No directo</td></tr><tr><td>Ver nivel funcional del forest</td><td><code>(Get-ADForest).ForestMode</code></td><td><code>nltest /dsgetdc:&#x3C;domain> /forest</code></td></tr><tr><td>Ver raíz del forest</td><td><code>(Get-ADForest).RootDomain</code></td><td><code>nltest /dsgetdc:&#x3C;domain> /forest</code></td></tr><tr><td>Listar DCs Global Catalog</td><td><code>Get-ADDomainController -Filter {IsGlobalCatalog -eq $true}</code></td><td><code>nslookup -type=SRV _gc._tcp.&#x3C;domain></code></td></tr></tbody></table>

***

## Resumen Rápido - Cheatsheet General de AD

{% hint style="info" %}
**Nota**: Los comandos de PowerShell requieren el módulo `ActiveDirectory` (RSAT). Si no está disponible, usar alternativas con `net`, `nltest`, `dsquery` o herramientas de terceros como `PowerView` (parte de PowerSploit).
{% endhint %}

<table data-header-hidden><thead><tr><th width="155.666748046875"></th><th></th></tr></thead><tbody><tr><td>Categoría</td><td>Comandos útiles (PowerShell con RSAT)</td></tr><tr><td><strong>Dominio</strong></td><td><code>Get-ADDomain</code>, <code>Get-ADDomainController</code>, <code>nltest /dclist</code></td></tr><tr><td><strong>Usuarios</strong></td><td><code>Get-ADUser -Filter * -Properties *</code>, <code>net user /domain</code></td></tr><tr><td><strong>Grupos</strong></td><td><code>Get-ADGroup -Filter *</code>, <code>Get-ADGroupMember -Identity "GroupName"</code></td></tr><tr><td><strong>Equipos</strong></td><td><code>Get-ADComputer -Filter * -Properties OperatingSystem,IPv4Address</code></td></tr><tr><td><strong>OUs</strong></td><td><code>Get-ADOrganizationalUnit -Filter * -Properties *</code></td></tr><tr><td><strong>Kerberos</strong></td><td><code>klist</code> (ver tickets), <code>klist purge</code> (limpiar)</td></tr><tr><td><strong>Trusts</strong></td><td><code>Get-ADTrust -Filter *</code>, <code>nltest /domain_trusts</code></td></tr><tr><td><strong>Forest</strong></td><td><code>Get-ADForest</code>, <code>(Get-ADForest).Domains</code></td></tr></tbody></table>
