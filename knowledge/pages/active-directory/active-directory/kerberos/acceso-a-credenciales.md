
# Acceso a Credenciales

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Autenticación y autorización en Windows</mark>

### Logon Sessions

Descargar módulo logonsessions de sysinternals

[<mark style="color:purple;">https://learn.microsoft.com/en-us/sysinternals/downloads/logonsessions</mark>](https://learn.microsoft.com/en-us/sysinternals/downloads/logonsessions)

```
cd logonsessions
```

```
.\logonsessions.exe -p verbose
```

{% hint style="success" %}
Esto nos saca un listado de todas las sesiones en nuestro equipo de empleado, pudiendo haber alguna de algún usuario administrador junto con su hash NTLM
{% endhint %}

En los siguientes módulos veremos las técnicas mas usadas para acceder a credenciales y realizar movimientos laterales a otras máquinas de la infraestructura.
