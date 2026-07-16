
# Procdump y lsass.exe

{% embed url="<https://learn.microsoft.com/en-us/sysinternals/downloads/procdump>" %}

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir información sensible, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Volcado de memoria en Windows</mark>

En Windows con Procdump y lsass.exe

* Descargar procdump y descomprimir carpeta en el escritorio
* En una terminal ir a la ruta de la carpeta

```
cd Users/User/Desktop/Procdump
procdump64.exe -accepteula -ma lsass.exe lsass.dmp
```

## <mark style="color:purple;">Procdump para Linux</mark>

{% embed url="<https://github.com/Sysinternals/ProcDump-for-Linux>" %}

#### Instrucciones de instalación

{% embed url="<https://github.com/Sysinternals/ProcDump-for-Linux/blob/master/INSTALL.md>" %}
