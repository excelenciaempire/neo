
# Lab - Ataques a Aplicaciones III

## <mark style="color:purple;">**Skills Assestment III**</mark>

Durante nuestra prueba de penetración, nuestro equipo encontró un host Windows ejecutándose en la red y las credenciales correspondientes para el administrador. Es necesario que nos conectemos al host y busquemos las credenciales `hardcodeadas` para el servicio MSSQL.

```
Objetivo: 10.129.95.200

RDP con usuario “Administrator” y contraseña “xcyj8izxNVzhf4z”
```

***

## <mark style="color:purple;">Pregunta 1</mark>

> ¿Cuál es la contraseña codificada para la conexión a la base de datos en el archivo `MultimasterAPI.dll`?

### Acceso por RDP

Al acceder nos encontramos con un archivo root.txt en el escritorio:

<figure><img src="/files/nNoqEV5VGa4eDIM0IJHs" alt=""><figcaption></figcaption></figure>

```
89edf1a0bcdd83db7cc8d8a2f176a33e
```

Podría ser una contraseña o hash de un administrador. Como ya somos admin no nos interesa en principio.

### Búsqueda del binario

```powershell
PS C:\Users\Administrator> Get-ChildItem -Path C:\ -Recurse -Filter
>>

    Directory: C:\inetpub\wwwroot\bin

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         1/9/2020   4:13 AM          13824 MultimasterAPI.dll
```

### Análisis del archivo DLL

Abrimos **`MultimasterAPI.dll`** en `dnSpy`.

<figure><img src="/files/cnI9e44FSQ8nIWOLwd6e" alt=""><figcaption></figcaption></figure>

Si navegamos hasta `Colleague Controller` podemos ver las credenciales hardcodeadas en plano:

<figure><img src="/files/jESSfH7tILSweZTjKuw1" alt=""><figcaption></figcaption></figure>
