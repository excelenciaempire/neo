
# SAM

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Enumeración local de SAM</mark>&#x20;

Desde un equipo de empleado podríamos usar varias técnicas de enumeración local:

### Saber qué usuario somos

```
$env:UserDomain
```

```
whoami
```

### Dominio al que pertenece el usuario

```
$env:UserDomain
```

### Nombre del equipo

```
$env:ComputerName
```

### Grupos locales

Con PowerView:

```
. .\powerview.ps1
```

```
Get-NetLocalGroup
```

Sin PowerView:

```
Get-LocalGroup | Select Name, Objectclass, Principalsource, sid
```

### Ver que privilegios tenemos

```
Get-NetGroup -UserName “empleado1” | select name
```

### Ver miembros del grupo administradores

Con PowerView:

{% code overflow="wrap" %}

```
Get-NetLocalGroupMember -GroupName Administradores | Select-Object MemberName, IsGroup, IsDomain
```

{% endcode %}

Sin PowerView:

```
Get-LocalGroupMember -Group Administradores
```

### Ver usuarios logueados

```
Get-NetLoggedon
```

### Ver sesiones en mi máquina

```
Get-NetSession
```

## <mark style="color:purple;">Enumeración Remota de SAM</mark>

### Sacar los grupos de una máquina remota

Con PowerView

```powershell
Get-NetLocalGroup -ComputerName WS02
```

Sin PowerView

{% code overflow="wrap" %}

```powershell
Invoke-Command -ScriptBlock { Get-LocalGroupMember -Group Administradores } -ComputerName WS02
```

{% endcode %}

## <mark style="color:purple;">Enumeración de SAM con Kali Linux</mark>

* Configurar el DNS Server como el mismo que el DC
* Configuración de red > IPV4 > Dns manual (que coincida con el del DC)

### Como saber la IP del DC

```bash
sudo map -sS -n IP.0-7
```

* Suele estar en el puerto 5
* Tiene bastantes servicios corriendo

### RPC Client

{% code title="En Kali Linux" %}

```bash
rpcclient -U “corp/empleado%PassWord” WS01.corp.local
```

{% endcode %}

### Impacket

```bash
impacket-netview corp.local/empleado:’Passw0rd’ -target WS01.corp.local
```

{% hint style="warning" %}
Necesitamos permisos de admin para usar este técnica
{% endhint %}

## <mark style="color:purple;">Atacando a SAM</mark>

En la siguiente sección veremos ataques de contraseñas a la base da datos SAM:

{% content-ref url="/pages/R6QjgH0qNuwUQAgCOVnq" %}
[Atacando a SAM](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/atacando-a-sam.md)
{% endcontent-ref %}
