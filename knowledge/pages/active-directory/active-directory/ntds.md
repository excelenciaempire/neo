
# NTDS

La base de datos NTDS.dit almacena información sobre los objetos de Active Directory, incluyendo nombres de usuario y contraseñas, ACLs recursos compartidos y documentos sensibles en sistemas de Windows.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Enumeración de NTDS</mark>

{% code title="Modulo AD" %}

```
Get-ADDomain
(Get-DomainPolicy).”SystemAccess”
```

{% endcode %}

### Saber la IP del DC

{% code title="Modulo AD" %}

```
Get-ADDomainController
```

{% endcode %}

{% code title="PowerView" %}

```
Get-NetDomainController
```

{% endcode %}

### Saber todos los usuarios de mi dominio

{% code title="Modulo AD" %}

```
Get-ADUsers
Get-ADUsers -Filter * | select Name, ObjectClass,ObjectGuid
```

{% endcode %}

{% code title="PowerView" %}

```
Get-NetUser
```

{% endcode %}

### Información sobre los equipos de mi dominio

{% code title="Modulo AD" %}

```
Get-ADComputer
```

{% endcode %}

{% code title="PowerView" %}

```
Get-NetComputer
Get-NetComputer | select name, operatingsystem
Get-NetComputer -Ping | select name, operatingsystem
```

{% endcode %}

### Información sobre los grupos de mi dominio

{% code title="PowerView" %}

```
Get-DomainGroup
```

{% endcode %}

### Recursos compartidos

{% code title="PowerView" %}

```
Find-DomainShare
```

{% endcode %}

### Ver unidades organizativas

{% code title="PowerView" %}

```
Get-NetOU
```

{% endcode %}

### Enumerar GPOs

{% code title="" %}

```
Get-NetGPO
Get-NetGPO -ComputerIdentity WS02 | select displayname
```

{% endcode %}

### Enumerar ACLs (Access control list)

{% code title="PowerView" %}

```
Get-ObjectAcl -SamAccountName empleado1
```

{% endcode %}

### Ver máquinas con administrador local

{% code title="" %}

```
Find-LocalAdminAccess -Verbose
Invoke-EnumerateLocalAdmin -Verbose
```

{% endcode %}
