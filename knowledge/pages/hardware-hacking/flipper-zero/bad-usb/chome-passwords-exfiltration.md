
# Chome Passwords Exfiltration

{% hint style="danger" %}
Este script y sus instrucciones están diseñados para fines educativos y para realizar pruebas en entornos con permiso explícito. El uso no autorizado de estos scripts es ilegal y puede tener consecuencias graves.
{% endhint %}

## <mark style="color:orange;">Repositorio</mark>

Vamos a utilizar el siguiente repositorio:

{% embed url="<https://github.com/FalsePhilosopher/badusb/tree/main/exfiltration/Win/chrome-exfil>" %}

Es un script para extraer credenciales del navegador Chrome de un objetivo. Se ingresa de forma interactiva para evitar muchos activadores de antivirus relacionados con PowerShell.

La solicitud GET de Chrome requiere un ancho de banda bajo, pero no debería generar el mismo nivel de alarma de detección de AV que Invoke-WebRequest.

### Dependencias

* Windows 10
* PowerShell 5.1 (o PowerShell 7.x si desea capturar contraseñas posteriores a Chrome v80)
* Chrome

### Configuración

Cambie en el script la URL `http://localhost:8000/`para que coincida con un servidor accesible al destino que haya configurado. Para ello en Kali Linux vamos a abrir un servidor local con python:

```shell-session
afsh4ck@kali$ python3 -m http.server 8000
```

Una vez configurado podemos ejecutar el script con el Flipper y recibir las contraseñas decodificadas.
