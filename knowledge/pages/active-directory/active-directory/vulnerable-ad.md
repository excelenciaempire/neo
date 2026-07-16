
# Vulnerable AD

{% embed url="<https://github.com/WazeHell/vulnerable-AD>" %}

## Instalación

* Ejecutar el script vulnad.ps1 en nuestro DC

```
. .\vulnad.ps1
Invoke-VulnAD -UsersLimit 1000 -DomainName “corp.local”
```

* Esto nos va a crear una infraestructura de red de 1000 empleados, con distintas vulnerabilidades y fallos de configuración incorporados que podemos explotar.
