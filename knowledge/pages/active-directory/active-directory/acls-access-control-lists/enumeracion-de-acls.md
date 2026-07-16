
# Enumeración de ACLs

Vamos a empezar a enumerar las ACL con PowerView y a analizar algunas representaciones gráficas con BloodHound. Luego, abordaremos algunos escenarios y ataques en los que las ACL que enumeramos se pueden aprovechar para obtener más acceso en el entorno interno.

***

## <mark style="color:purple;">Enumeración de ACL con PowerView</mark>

Podemos usar PowerView para enumerar las ACL, pero la tarea de buscar entre *todos* los resultados demandará mucho tiempo y probablemente sea inexacta. Por ejemplo, si ejecutamos la función, `Find-InterestingDomainAcl` recibiremos una enorme cantidad de información que necesitaremos buscar para entender:

### **Powerview - Find-InterestingDomainAcl**

```powershell
PS C:\htb> Find-InterestingDomainAcl

ObjectDN                : DC=INLANEFREIGHT,DC=LOCAL
AceQualifier            : AccessAllowed
ActiveDirectoryRights   : ExtendedRight
ObjectAceType           : ab721a53-1e2f-11d0-9819-00aa0040529b
AceFlags                : ContainerInherit
AceType                 : AccessAllowedObject
InheritanceFlags        : ContainerInherit
SecurityIdentifier      : S-1-5-21-3842939050-3880317879-2865463114-5189
IdentityReferenceName   : Exchange Windows Permissions
IdentityReferenceDomain : INLANEFREIGHT.LOCAL
IdentityReferenceDN     : CN=Exchange Windows Permissions,OU=Microsoft Exchange Security 
                          Groups,DC=INLANEFREIGHT,DC=LOCAL
IdentityReferenceClass  : group

ObjectDN                : DC=INLANEFREIGHT,DC=LOCAL
AceQualifier            : AccessAllowed
ActiveDirectoryRights   : ExtendedRight
ObjectAceType           : 00299570-246d-11d0-a768-00aa006e0529
AceFlags                : ContainerInherit
AceType                 : AccessAllowedObject
InheritanceFlags        : ContainerInherit
SecurityIdentifier      : S-1-5-21-3842939050-3880317879-2865463114-5189
IdentityReferenceName   : Exchange Windows Permissions
IdentityReferenceDomain : INLANEFREIGHT.LOCAL
IdentityReferenceDN     : CN=Exchange Windows Permissions,OU=Microsoft Exchange Security 
                          Groups,DC=INLANEFREIGHT,DC=LOCAL
IdentityReferenceClass  : group

<SNIP>
```

Si intentamos analizar todos estos datos durante una evaluación con límite de tiempo, es probable que nunca los analicemos todos ni encontremos nada interesante antes de que finalice la evaluación. Ahora bien, existe una forma de utilizar una herramienta como PowerView de forma más eficaz: realizar una enumeración dirigida a partir de un usuario sobre el que tengamos control.&#x20;

Centrémonos en el usuario `wley`, que obtuvimos después de resolver la última pregunta de la sección [`LLMNR/NBT-NS Poisoning - Desde Linux`](/ethical-hacking-cheatsheet/active-directory/active-directory/sniffing-desde-el-foothold/llmnr-nbt-ns-poisoning-desde-linux.md). Profundicemos y veamos si este usuario tiene algún derecho de ACL interesante que podamos aprovechar. Primero, debemos obtener el SID de nuestro usuario objetivo para realizar una búsqueda eficaz.

```powershell
PS C:\htb> Import-Module .\PowerView.ps1
PS C:\htb> $sid = Convert-NameToSid wley
```

Luego podemos usar la función `Get-DomainObjectACL` para realizar nuestra búsqueda específica. En el siguiente ejemplo, usamos esta función para encontrar todos los objetos de dominio sobre los que nuestro usuario tiene derechos al asignar el SID del usuario usando la variable `$sid` a la propiedad `SecurityIdentifier`, que es lo que nos dice *quién* tiene el derecho otorgado sobre un objeto. Una cosa importante a tener en cuenta es que si buscamos sin la bandera `ResolveGUIDs`, veremos resultados como el siguiente, donde el derecho `ExtendedRight` no nos da una imagen clara de qué entrada ACE tiene el usuario `wley` sobre `damundsen`. Esto se debe a que la propiedad `ObjectAceType` está devolviendo un valor GUID que no es legible para humanos.

Tenga en cuenta que este comando tardará un tiempo en ejecutarse, especialmente en un entorno de gran tamaño. Puede llevar entre 1 y 2 minutos obtener un resultado en nuestro laboratorio.

### **Powerview - Get-DomainObjectACL**

```powershell
PS C:\htb> Get-DomainObjectACL -Identity * | ? {$_.SecurityIdentifier -eq $sid}

ObjectDN               : CN=Dana Amundsen,OU=DevOps,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
ObjectSID              : S-1-5-21-3842939050-3880317879-2865463114-1176
ActiveDirectoryRights  : ExtendedRight
ObjectAceFlags         : ObjectAceTypePresent
ObjectAceType          : 00299570-246d-11d0-a768-00aa006e0529
InheritedObjectAceType : 00000000-0000-0000-0000-000000000000
BinaryLength           : 56
AceQualifier           : AccessAllowed
IsCallback             : False
OpaqueLength           : 0
AccessMask             : 256
SecurityIdentifier     : S-1-5-21-3842939050-3880317879-2865463114-1181
AceType                : AccessAllowedObject
AceFlags               : ContainerInherit
IsInherited            : False
InheritanceFlags       : ContainerInherit
PropagationFlags       : None
AuditFlags             : None
```

Podríamos buscar en Google el valor GUID `00299570-246d-11d0-a768-00aa006e0529`y descubrir [esta](https://docs.microsoft.com/en-us/windows/win32/adschema/r-user-force-change-password) página que muestra que el usuario tiene derecho a forzar el cambio de la contraseña del otro usuario. Como alternativa, podríamos hacer una búsqueda inversa con PowerShell para asignar el nombre correcto al valor GUID.

### **Realizar una búsqueda inversa y asignarlo a un valor GUID**

```powershell
PS C:\htb> $guid= "00299570-246d-11d0-a768-00aa006e0529"
PS C:\htb> Get-ADObject -SearchBase "CN=Extended-Rights,$((Get-ADRootDSE).ConfigurationNamingContext)" -Filter {ObjectClass -like 'ControlAccessRight'} -Properties * |Select Name,DisplayName,DistinguishedName,rightsGuid| ?{$_.rightsGuid -eq $guid} | fl

Name              : User-Force-Change-Password
DisplayName       : Reset Password
DistinguishedName : CN=User-Force-Change-Password,CN=Extended-Rights,CN=Configuration,DC=INLANEFREIGHT,DC=LOCAL
rightsGuid        : 00299570-246d-11d0-a768-00aa006e0529
```

Esto nos dio la respuesta, pero sería muy ineficiente durante una evaluación. PowerView tiene el indicador `ResolveGUIDs` que hace exactamente esto por nosotros. Observe cómo cambia el resultado cuando incluimos este indicador para mostrar el formato legible para humanos de la propiedad `ObjectAceType` como `User-Force-Change-Password`.

**Indicador -ResolveGUIDs**

```powershell
PS C:\htb> Get-DomainObjectACL -ResolveGUIDs -Identity * | ? {$_.SecurityIdentifier -eq $sid} 

AceQualifier           : AccessAllowed
ObjectDN               : CN=Dana Amundsen,OU=DevOps,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights  : ExtendedRight
ObjectAceType          : User-Force-Change-Password
ObjectSID              : S-1-5-21-3842939050-3880317879-2865463114-1176
InheritanceFlags       : ContainerInherit
BinaryLength           : 56
AceType                : AccessAllowedObject
ObjectAceFlags         : ObjectAceTypePresent
IsCallback             : False
PropagationFlags       : None
SecurityIdentifier     : S-1-5-21-3842939050-3880317879-2865463114-1181
AccessMask             : 256
AuditFlags             : None
IsInherited            : False
AceFlags               : ContainerInherit
InheritedObjectAceType : All
OpaqueLength           : 0
```

`¿Por qué analizamos este ejemplo cuando podríamos haber buscado usando ResolveGUID primero?`

Es fundamental que comprendamos lo que hacen nuestras herramientas y que tengamos métodos alternativos en nuestro conjunto de herramientas en caso de que una herramienta falle o se bloquee. Antes de continuar, echemos un vistazo rápido a cómo podríamos hacer esto utilizando los cmdlets [Get-Acl](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-acl?view=powershell-7.2) y [Get-ADUser](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-aduser?view=windowsserver2022-ps) que podemos encontrar disponibles en un sistema cliente. Saber cómo realizar este tipo de búsqueda sin utilizar una herramienta como PowerView es muy beneficioso y podría diferenciarnos de nuestros pares. Podemos utilizar este conocimiento para lograr resultados cuando un cliente nos pide que trabajemos desde uno de sus sistemas y estamos restringidos a las herramientas que están disponibles en el sistema sin la capacidad de incorporar ninguna de las nuestras.

Este ejemplo no es muy eficiente y el comando puede tardar mucho tiempo en ejecutarse, especialmente en un entorno grande. Tardará mucho más que el comando equivalente que utiliza PowerView. En este comando, primero hemos creado una lista de todos los usuarios del dominio con el siguiente comando:

### **Creación de una lista de usuarios del dominio**

```powershell
PS C:\htb> Get-ADUser -Filter * | Select-Object -ExpandProperty SamAccountName > ad_users.txt
```

Luego leemos cada línea del archivo mediante un bucle `foreach` y usamos el cmdlet `Get-Acl` para recuperar la información de ACL para cada usuario del dominio al pasar cada línea del archivo `ad_users.txt` al cmdlet `Get-ADUser`. Luego seleccionamos solo `Access property`, que nos dará información sobre los derechos de acceso. Finalmente, establecemos la propiedad `IdentityReference` para el usuario que controlamos (o que buscamos ver qué derechos tiene), en nuestro caso, `wley`.

### **Un bucle foreach útil**

```powershell
PS C:\htb> foreach($line in [System.IO.File]::ReadLines("C:\Users\htb-student\Desktop\ad_users.txt")) {get-acl  "AD:\$(Get-ADUser $line)" | Select-Object Path -ExpandProperty Access | Where-Object {$_.IdentityReference -match 'INLANEFREIGHT\\wley'}}

Path                  : Microsoft.ActiveDirectory.Management.dll\ActiveDirectory:://RootDSE/CN=Dana 
                        Amundsen,OU=DevOps,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
InheritanceType       : All
ObjectType            : 00299570-246d-11d0-a768-00aa006e0529
InheritedObjectType   : 00000000-0000-0000-0000-000000000000
ObjectFlags           : ObjectAceTypePresent
AccessControlType     : Allow
IdentityReference     : INLANEFREIGHT\wley
IsInherited           : False
InheritanceFlags      : ContainerInherit
PropagationFlags      : None
```

Una vez que tengamos estos datos, podríamos seguir los mismos métodos mostrados anteriormente para convertir el GUID a un formato legible por humanos para comprender qué derechos tenemos sobre el usuario objetivo.

Para resumir, comenzamos con el usuario `wley` y ahora tenemos control sobre `damundsen` a través del derecho extendido `User-Force-Change-Password`. Usemos Powerview para buscar a dónde nos podría llevar el control sobre la cuenta `damundsen`.

**Enumeración adicional de derechos del usuario damundsen**

```powershell
PS C:\htb> $sid2 = Convert-NameToSid damundsen
PS C:\htb> Get-DomainObjectACL -ResolveGUIDs -Identity * | ? {$_.SecurityIdentifier -eq $sid2} -Verbose

AceType               : AccessAllowed
ObjectDN              : CN=Help Desk Level 1,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ListChildren, ReadProperty, GenericWrite
OpaqueLength          : 0
ObjectSID             : S-1-5-21-3842939050-3880317879-2865463114-4022
InheritanceFlags      : ContainerInherit
BinaryLength          : 36
IsInherited           : False
IsCallback            : False
PropagationFlags      : None
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-1176
AccessMask            : 131132
AuditFlags            : None
AceFlags              : ContainerInherit
AceQualifier          : AccessAllowed
```

Ahora podemos ver que nuestro usuario `damundsen` tiene privilegios `GenericWrite` sobre el grupo `Help Desk Level 1`. Esto significa, entre otras cosas, que podemos agregar cualquier usuario (o nosotros mismos) a este grupo y heredar cualquier derecho que este grupo le haya aplicado. Una búsqueda de derechos conferidos a este grupo no arroja ningún resultado interesante.

Veamos si este grupo está anidado en otros grupos, recordando que la pertenencia a un grupo anidado significa que cualquier usuario del grupo A heredará todos los derechos de cualquier grupo en el que esté anidado el grupo A (del que sea miembro). Una búsqueda rápida nos muestra que el grupo `Help Desk Level 1` está anidado en el grupo `Information Technology`, lo que significa que podemos obtener cualquier derecho que el grupo `Information Technology` otorgue a sus miembros si simplemente nos agregamos al grupo `Help Desk Level 1` en el que nuestro usuario `damundsen` tiene privilegios `GenericWrite`.

### **Investigación de grupo con Get-DomainGroup**

```powershell
PS C:\htb> Get-DomainGroup -Identity "Help Desk Level 1" | select memberof

memberof                                                                      
--------                                                                      
CN=Information Technology,OU=Security Groups,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
```

¡Esto es mucho para digerir! Recapitulemos dónde estamos:

* Tenemos control sobre el usuario `wley` cuyo hash recuperamos anteriormente en el módulo (evaluación) usando Responder y desciframos sin conexión usando Hashcat para revelar el valor de la contraseña en texto sin formato.
* Enumeramos los objetos sobre los que el usuario `wley` tiene control y descubrimos que podíamos forzar el cambio de la contraseña del usuario `damundsen`
* Desde aquí, descubrimos que el usuario `damundsen` puede agregar un miembro al grupo `Help Desk Level 1` usando privilegios `GenericWrite`.
* El grupo `Help Desk Level 1` está anidado en el grupo `Information Technology`, lo que otorga a los miembros de ese grupo todos los derechos previstos para el grupo `Information Technology`.

Ahora, echemos un vistazo y veamos si los miembros de `Information Technology` pueden hacer algo interesante. Una vez más, al realizar nuestra búsqueda con `Get-DomainObjectACL` nos muestra que los miembros del grupo `Information Technology` tienen derechos `GenericAll` sobre el usuario `adunn`, lo que significa que podríamos:

* Modificar la membresía del grupo
* Forzar el cambio de contraseña
* Realizar un ataque Kerberoasting dirigido e intentar descifrar la contraseña del usuario si es débil

**Investigando el Grupo Information Technology**

```powershell
PS C:\htb> $itgroupsid = Convert-NameToSid "Information Technology"
PS C:\htb> Get-DomainObjectACL -ResolveGUIDs -Identity * | ? {$_.SecurityIdentifier -eq $itgroupsid} -Verbose

AceType               : AccessAllowed
ObjectDN              : CN=Angela Dunn,OU=Server Admin,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : GenericAll
OpaqueLength          : 0
ObjectSID             : S-1-5-21-3842939050-3880317879-2865463114-1164
InheritanceFlags      : ContainerInherit
BinaryLength          : 36
IsInherited           : False
IsCallback            : False
PropagationFlags      : None
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-4016
AccessMask            : 983551
AuditFlags            : None
AceFlags              : ContainerInherit
AceQualifier          : AccessAllowed

```

Por último, veamos si el usuario  `adunn` tiene algún tipo de acceso interesante que podamos aprovechar para acercarnos a nuestro objetivo.

### **Buscando acceso interesante**

```powershell
PS C:\htb> $adunnsid = Convert-NameToSid adunn 
PS C:\htb> Get-DomainObjectACL -ResolveGUIDs -Identity * | ? {$_.SecurityIdentifier -eq $adunnsid} -Verbose

AceQualifier           : AccessAllowed
ObjectDN               : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights  : ExtendedRight
ObjectAceType          : DS-Replication-Get-Changes-In-Filtered-Set
ObjectSID              : S-1-5-21-3842939050-3880317879-2865463114
InheritanceFlags       : ContainerInherit
BinaryLength           : 56
AceType                : AccessAllowedObject
ObjectAceFlags         : ObjectAceTypePresent
IsCallback             : False
PropagationFlags       : None
SecurityIdentifier     : S-1-5-21-3842939050-3880317879-2865463114-1164
AccessMask             : 256
AuditFlags             : None
IsInherited            : False
AceFlags               : ContainerInherit
InheritedObjectAceType : All
OpaqueLength           : 0

AceQualifier           : AccessAllowed
ObjectDN               : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights  : ExtendedRight
ObjectAceType          : DS-Replication-Get-Changes
ObjectSID              : S-1-5-21-3842939050-3880317879-2865463114
InheritanceFlags       : ContainerInherit
BinaryLength           : 56
AceType                : AccessAllowedObject
ObjectAceFlags         : ObjectAceTypePresent
IsCallback             : False
PropagationFlags       : None
SecurityIdentifier     : S-1-5-21-3842939050-3880317879-2865463114-1164
AccessMask             : 256
AuditFlags             : None
IsInherited            : False
AceFlags               : ContainerInherit
InheritedObjectAceType : All
OpaqueLength           : 0

<SNIP>
```

El resultado anterior muestra que nuestro usuario `adunn` tiene derechos `DS-Replication-Get-Changes` y `DS-Replication-Get-Changes-In-Filtered-Set` sobre el objeto de dominio. Esto significa que se puede aprovechar este usuario para realizar un ataque DCSync. Trataremos este ataque `DCSync` en profundidad en esta sección.

***

## <mark style="color:purple;">Enumeración de ACL con BloodHound</mark>

Ahora que hemos enumerado la ruta de ataque utilizando métodos más manuales como PowerView y cmdlets de PowerShell integrados, veamos cuánto más fácil hubiera sido identificar esto utilizando BloodHound. Tomemos los datos que recopilamos anteriormente con el ingestador SharpHound y carguemoslos en BloodHound.&#x20;

A continuación, podemos establecer el usuario `wley` como nuestro nodo de inicio, seleccionar la pestaña `Node Info` y desplazarnos hacia abajo hasta `Outbound Control Rights`. Esta opción nos mostrará los objetos sobre los que tenemos control directamente, a través de la membresía del grupo, y la cantidad de objetos que nuestro usuario podría hacer que controlemos a través de rutas de ataque de ACL bajo `Transitive Object Control`. Si hacemos clic en `1` junto a `First Degree Object Control`, vemos el primer conjunto de derechos que enumeramos, `ForceChangePassword` sobre el usuario `damundsen`.

**Visualización de información de nodos a través de BloodHound**

![imagen](https://academy.hackthebox.com/storage/modules/143/wley_damundsen.png)

Si hacemos clic derecho en la línea entre los dos objetos, aparecerá un menú. Si seleccionamos `Help`, se nos presentará ayuda sobre cómo abusar de este ACE, que incluye:

* `Más información sobre los derechos, herramientas y comandos específicos que se pueden utilizar para llevar a cabo este ataque.`
* `Consideraciones sobre seguridad operacional (Opsec)`
* `Referencias externas.`

Profundizaremos en este menú más adelante.

**Investigando más a fondo ForceChangePassword**

![imagen](https://academy.hackthebox.com/storage/modules/143/help_edge.png)

Si hacemos clic en el número `16` en `Transitive Object Control`, veremos el camino completo que hemos enumerado con tanto esmero anteriormente. Desde aquí, podemos aprovechar los menús de ayuda de cada borde para encontrar la mejor manera de ejecutar cada ataque.

**Visualización de posibles rutas de ataque a través de BloodHound**

![imagen](https://academy.hackthebox.com/storage/modules/143/wley_path.png)

Finalmente, podemos usar las consultas predefinidas en BloodHound para confirmar que el usuario `adunn` tiene derechos DCSync.

**Visualización de consultas previas a la compilación a través de BloodHound**

![imagen](https://academy.hackthebox.com/storage/modules/143/adunn_dcsync.png)

***

## <mark style="color:purple;">Caso práctico</mark>

### Pregunta 1

Utilizando las habilidades aprendidas en esta sección, enumere los `ActiveDirectoryRights` que el usuario `forend` tiene sobre el usuario `dpayne` (Dagmar Payne).

{% hint style="info" %}
No olvides obtener el SID del usuario principal antes de realizar tu búsqueda
{% endhint %}

Lo primero vamos a utilizar el módulo de PowerView `Find-InterestingDomainAcl` para encontrar ACLs interesantes en el sistema, y lo vamos a exportar a un archivo de texto para manejar mejor los datos:

```powershell
PS C:\Tools> Find-InterestingDomainAcl > acls.txt
```

Para obtener el SID del usuario `forend`:

```powershell
PS C:\Tools> Import-Module .\PowerView.ps1

PS C:\Tools> Convert-NameToSid forend
S-1-5-21-3842939050-3880317879-2865463114-5614

# O podemos exportarlo en una variable para usarlo con otras técnicas
PS C:\Tools> $sid = Convert-NameToSid forend
```

Ahora vamos a ejecutar el módulo `Get-DomainObjectACL` para obtener información completa sobre los permisos del usuario forend dentro del dominio:

```powershell
PS C:\Tools> Get-DomainObjectACL -Identity * | ? {$_.SecurityIdentifier -eq $sid}


ObjectDN              : CN=Dagmar Payne,OU=HelpDesk,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
ObjectSID             : S-1-5-21-3842939050-3880317879-2865463114-1152
ActiveDirectoryRights : GenericAll
BinaryLength          : 36
AceQualifier          : AccessAllowed
IsCallback            : False
OpaqueLength          : 0
AccessMask            : 983551
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-5614
AceType               : AccessAllowed
AceFlags              : ContainerInherit
IsInherited           : False
InheritanceFlags      : ContainerInherit
PropagationFlags      : None
AuditFlags            : None
```

Observamos que el usuario forend tiene permisos `GenericAll` sobre el usuario Dagmar Payne, lo que le permitiría en principio hacer cualquier tipo de acción contra este usuario.

### Pregunta 2

Lo primero, vamos a enumerar todos los grupos del dominio, para comprobar que existe:

```powershell
PS C:\Tools> Get-ADGroup -Filter * | Select-Object Name, Description, GroupScope, GroupCategory

Name                                    Description  GroupScope GroupCategory
----                                    -----------  ---------- -------------
Administrators                                      DomainLocal      Security
Users                                               DomainLocal      Security
Guests                                              DomainLocal      Security
Print Operators                                     DomainLocal      Security
Backup Operators                                    DomainLocal      Security
Domain Admins                                            Global      Security
Domain Users                                             Global      Security
Domain Guests                                            Global      Security
DnsAdmins                                           DomainLocal      Security
Accounting                                               Global      Security
Engineering                                              Global      Security
Executives                                               Global      Security
Human Resources                                          Global      Security
Marketing                                                Global      Security
Operations                                               Global      Security
GPO Management                                           Global      Security
<----------SNIP---------->
```

Ahora que hemos descubierto que el grupo existe, podríamos usar Bloodhound para ver los `Explicit Object Controllers`, filtrando por el grupo GPO Management y descubrimos que el usuario forend tiene permisos `AddSelf` y `GenericWrite` sobre este grupo, por lo que se podría añadir el mismo al grupo privilegiado o hacer cualquier tipo de acción.

<figure><img src="/files/mrpREMhBZWyOtuvBk2Fo" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/j1ObnIB0QnMt4HrIt7lz" alt=""><figcaption></figcaption></figure>

***

Ya hemos enumerado estas rutas de ataque de varias maneras. El siguiente paso será ejecutar esta cadena de ataque de principio a fin. ¡Vamos a profundizar en ello!
