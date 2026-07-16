
# LDAP

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Recopilación de objetos en un Dominio con LDAP</mark>

### En el Domain Controller (DC):&#x20;

```
Get-ADDomain
```

### En máquina empleado:&#x20;

Necesitamos la DLL del DC que está en:&#x20;

```
C > Windows > Microsoft.NET > assembly > GAC_64 > Microsoft.Active.Directory.Management
```

Nos enviamos el .dll a nuestra máquina host y la pasamos a una máquina de empleado

```bash
cd Desktop
Import-Module .\Microsoft.ActiveDirectory.Management.dll
Get-ADDomain
```

## <mark style="color:purple;">Enumeración con Kali Linux</mark>

### LdapSearch

#### Enumerar todos los objetos

Con login anonimo

```bash
ldapsearch -x -h {IP_DC} -D ‘’ -w ‘’ -b “DC=corp,DC=local”
```

Con acceso a credenciales de un usuario

```bash
ldapsearch -x -h {IP_DC} -D ‘CORP/empleado1’ -w ‘Passw0rd2’ -b “DC=corp,DC=local”
```

#### Enumerar todos los usuarios

```bash
ldapsearch -x -h {IP_DC} -D ‘CORP/empleado1’ -w ‘Passw0rd2’ -b “CN=Users,DC=corp,DC=local”
```

#### Filtrar por usuario

```bash
ldapsearch -x -h {IP_DC} -D ‘CORP/empleado1’ -w ‘Passw0rd2’ -b “CN=empleado1,CN=Users,DC=corp,DC=local”
```

#### Enumerar todos los equipos

```bash
ldapsearch -x -h {IP_DC} -D ‘CORP/empleado1’ -w ‘Passw0rd2’ -b “CN=Computers,DC=corp,DC=local”
```

#### Enumerar los administradores

```
-x -h {IP_DC} -D ‘CORP/empleado1’ -w ‘Passw0rd2’ -b “CN=Administradores,CN=Builtin,DC=corp,DC=local”
```

## <mark style="color:purple;">Pywerview</mark>&#x20;

Muestra la información de una forma más simple.

```bash
pywerview -h
```

### Enumerar todos los usuarios

```bash
pywerview get-netuser -u empleado1 —dc-ip {IP_DC} -p Passw0rd2
```

### Enumerar todos los grupos

```bash
pywerview get-netgroup -u empleado1 —dc-ip {IP_DC} -p Passw0rd2
```

### Enumerar todas las GPOs

```bash
pywerview get-netgpo -u empleado1 —dc-ip {IP_DC} -p Passw0rd2
```

## <mark style="color:purple;">JXplorer</mark>

Con interfaz gráfica

```
sudo apt update
```

```
sudo apt install jxplorer
```

```
jxplorer
```
