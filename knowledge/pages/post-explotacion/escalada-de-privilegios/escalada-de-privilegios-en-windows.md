
# Escalada de privilegios en Windows

## <mark style="color:purple;">Introducción</mark>

Una vez que nos hemos afianzado, elevar nuestros privilegios nos proporcionará más opciones de persistencia y puede revelar información almacenada localmente que puede mejorar nuestro acceso dentro del entorno. El objetivo general de la escalada de privilegios de Windows es ampliar nuestro acceso a un sistema determinado a un miembro del grupo `Local Administrators` o la cuenta `NT AUTHORITY\SYSTEM`.&#x20;

Sin embargo, puede haber escenarios en los que la escalada a otro usuario del sistema sea suficiente para alcanzar nuestro objetivo. La escalada de privilegios suele ser un paso vital durante cualquier compromiso. Necesitamos utilizar el acceso obtenido o algunos datos (como las credenciales) encontrados solo una vez que tengamos una sesión en un contexto elevado. En algunos casos, la escalada de privilegios puede ser el objetivo final de la evaluación si nuestro cliente nos contrata para una evaluación de tipo "imagen dorada" o "ruptura de la estación de trabajo". La escalada de privilegios suele ser vital para continuar a través de una red hacia nuestro objetivo final, así como para el movimiento lateral.

Dicho esto, es posible que necesitemos aumentar los privilegios por una de las siguientes razones:

<table><thead><tr><th width="76"></th><th></th></tr></thead><tbody><tr><td>1.</td><td><a href="https://www.techopedia.com/definition/29456/golden-image">Al probar la imagen dorada</a> de una estación de trabajo y un servidor de Windows del cliente para detectar fallas</td></tr><tr><td>2.</td><td>Para escalar privilegios localmente para obtener acceso a algún recurso local como una base de datos</td></tr><tr><td>3.</td><td>Para obtener acceso a nivel de <a href="https://docs.microsoft.com/en-us/windows/win32/services/localsystem-account">NT AUTHORITY\System</a> en una máquina unida a un dominio para obtener un punto de apoyo en el entorno de Active Directory del cliente</td></tr><tr><td>4.</td><td>Para obtener credenciales para moverse lateralmente o escalar privilegios dentro de la red del cliente</td></tr></tbody></table>

Hay muchas herramientas disponibles para nosotros como pentesters que nos ayudan con la escalada de privilegios. Sin embargo, también es esencial entender cómo realizar comprobaciones de escalada de privilegios y aprovechar las fallas `manuaalmente` en la medida de lo posible en un escenario determinado. Podemos encontrarnos con situaciones en las que un cliente nos coloca en una estación de trabajo administrada sin acceso a Internet, con un firewall muy fuerte y los puertos USB deshabilitados, por lo que no podemos cargar ninguna herramienta o script de ayuda. En este caso, sería crucial tener un conocimiento sólido de las comprobaciones de escalada de privilegios de Windows utilizando tanto PowerShell como la línea de comandos de Windows.

Los sistemas Windows presentan una amplia superficie de ataque. Algunas de las formas en que podemos aumentar los privilegios son:

|                                                            |                                                   |
| ---------------------------------------------------------- | ------------------------------------------------- |
| Abuso de privilegios de grupo de Windows                   | Abuso de privilegios de usuario de Windows        |
| Cómo eludir el control de cuentas de usuario               | Abuso de permisos de archivos o servicios débiles |
| Aprovechamiento de vulnerabilidades del kernel sin parches | Robo de credenciales                              |
| Captura de tráfico                                         | y muchas más.                                     |

***

## <mark style="color:purple;">Escenario 1: Bypass de las restricciones de la red</mark>

Una vez me dieron la tarea de escalar privilegios en un sistema proporcionado por el cliente sin acceso a Internet y con puertos USB bloqueados. Debido al control de acceso a la red implementado, no pude conectar mi máquina de ataque directamente a la red del usuario para que me ayudara. Durante la evaluación, ya había encontrado una falla de red en la que la VLAN de la impresora estaba configurada para permitir la comunicación saliente a través de los puertos 80, 443 y 445. Utilicé métodos de enumeración manual para encontrar una falla relacionada con los permisos que me permitiera escalar privilegios y realizar un volcado de memoria manual del proceso `LSASS`. Desde aquí, pude montar un recurso compartido SMB alojado en mi máquina de ataque en la VLAN de la impresora y extraer el archivo DMP `LSASS`. Con este archivo en la mano, utilicé `Mimikatz` sin conexión para recuperar el hash de contraseña NTLM para un administrador de dominio, que pude descifrar sin conexión y usar para acceder a un controlador de dominio desde el sistema proporcionado por el cliente.

***

## <mark style="color:purple;">Escenario 2: Saqueo de acciones abiertas</mark>

Durante otra evaluación, me encontré en un entorno bastante cerrado, bien monitoreado y sin fallas de configuración obvias ni servicios/aplicaciones vulnerables en uso. Encontré un recurso compartido de archivos completamente abierto, que permitía a todos los usuarios enumerar su contenido y descargar archivos almacenados en él. Este recurso compartido alojaba copias de seguridad de máquinas virtuales en el entorno. Estaba explícitamente interesado en los archivos del disco duro virtual ( `.VMDK` y archivos `.VHDX`). Podía acceder a este recurso compartido desde una máquina virtual de Windows, montar el disco duro virtual `.VHDX` como una unidad local y explorar el sistema de archivos. Desde aquí, recuperé los subárboles de registro `SYSTEM` , `SAM` y `SECURITY`, los moví a mi máquina de atacante Kali Linux y extraje el hash de la contraseña del administrador local utilizando la herramienta [secretsdump.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/secretsdump.py) . La organización estaba utilizando una imagen dorada, y el hash del administrador local se podía utilizar para obtener acceso de administrador a casi todos los sistemas Windows a través de un ataque de paso del hash.

***

## <mark style="color:purple;">Escenario 3: Credential Hunting y abuso de privilegios de cuenta</mark>

En este último escenario, me colocaron en una red bastante bloqueada con el objetivo de acceder a servidores de bases de datos críticos. El cliente me proporcionó una computadora portátil con una cuenta de usuario de dominio estándar y pude cargar herramientas en ella. Finalmente, ejecuté la herramienta [Snaffler](https://github.com/SnaffCon/Snaffler) para buscar información confidencial en los recursos compartidos de archivos. Encontré algunos archivos `.sql` que contenían credenciales de base de datos con pocos privilegios para una base de datos en uno de sus servidores de bases de datos. Utilicé un cliente MSSQL localmente para conectarme a la base de datos utilizando las credenciales de la base de datos, habilitar el procedimiento almacenado [xp\_cmdshell](https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-ver15) y obtener la ejecución local del comando. Al usar este acceso como una cuenta de servicio, confirmé que tenía el [SeImpersonatePrivilege](https://docs.microsoft.com/en-us/troubleshoot/windows-server/windows-security/seimpersonateprivilege-secreateglobalprivilege) , que se puede aprovechar para la escalada de privilegios locales. Descargué una versión compilada personalizada de [Juicy Potato](https://github.com/ohpe/juicy-potato) al host para ayudar con la escalada de privilegios y pude agregar un usuario administrador local. Agregar un usuario no fue ideal, pero mis intentos de obtener una shell inversa no funcionaron. Con este acceso, pude ingresar de forma remota al host de la base de datos y obtener control total de las bases de datos de uno de los clientes de la empresa.

***

## <mark style="color:purple;">¿Por qué ocurre la escalada de privilegios?</mark>

No existe una única razón por la que los hosts de una empresa puedan ser víctimas de una escalada de privilegios, pero existen varias posibles causas subyacentes. Algunas de las razones típicas por las que se introducen fallas y pasan desapercibidas son el personal y el presupuesto. Muchas organizaciones simplemente no tienen el personal para mantenerse al día con la aplicación de parches, la gestión de vulnerabilidades, las evaluaciones internas periódicas (autoevaluaciones), la supervisión continua y las iniciativas más grandes que consumen más recursos. Estas iniciativas pueden incluir actualizaciones de estaciones de trabajo y servidores, así como auditorías de recursos compartidos de archivos (para bloquear directorios y proteger/eliminar archivos confidenciales, como scripts o archivos de configuración que contienen credenciales).

***

## <mark style="color:purple;">Hacia delante</mark>

Los escenarios anteriores muestran cómo la comprensión de la escalada de privilegios de Windows es crucial para un evaluador de penetración. En el mundo real, rara vez atacaremos un solo host y debemos ser capaces de pensar con rapidez. Deberíamos ser capaces de encontrar formas creativas de escalar privilegios y formas de usar este acceso para avanzar hacia el objetivo de la evaluación.

***

## <mark style="color:purple;">Ejemplos prácticos</mark>

A lo largo del módulo, cubriremos ejemplos con la salida de comandos correspondiente, la mayoría de los cuales se pueden reproducir en las máquinas virtuales de destino que se pueden generar dentro de las secciones relevantes. Se le proporcionarán credenciales RDP para interactuar con las máquinas virtuales de destino y completar los ejercicios y evaluaciones de habilidades de la sección. Puede conectarse desde Pwnbox o su propia máquina virtual (después de descargar una clave VPN una vez que se genera una máquina) a través de RDP usando [FreeRDP](https://github.com/FreeRDP/FreeRDP/wiki/CommandLineInterface) , [Remmina](https://remmina.org/) o el cliente RDP de su elección.

### **Conexión a través de FreeRDP**

Podemos conectarnos a través de la línea de comandos usando el comando `xfreerdp /v:<target ip> /u:htb-student` y escribiendo la contraseña proporcionada cuando se nos solicite. La mayoría de las secciones proporcionarán credenciales para el usuario `htb-student`, pero algunas, según el material, le pedirán que se conecte a RDP con un usuario diferente y se proporcionarán credenciales alternativas.

```shell-session
afsh4ck@hkali$  xfreerdp /v:10.129.43.36 /u:htb-student

[21:17:27:323] [28158:28159] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[21:17:27:323] [28158:28159] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
[21:17:27:324] [28158:28159] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd
[21:17:27:324] [28158:28159] [INFO][com.freerdp.client.common.cmdline] - loading channelEx cliprdr
[21:17:27:648] [28158:28159] [INFO][com.freerdp.primitives] - primitives autodetect, using optimized
[21:17:27:672] [28158:28159] [INFO][com.freerdp.core] - freerdp_tcp_is_hostname_resolvable:freerdp_set_last_error_ex resetting error state
[21:17:27:672] [28158:28159] [INFO][com.freerdp.core] - freerdp_tcp_connect:freerdp_set_last_error_ex resetting error state
[21:17:28:770] [28158:28159] [INFO][com.freerdp.crypto] - creating directory /home/user2/.config/freerdp
[21:17:28:770] [28158:28159] [INFO][com.freerdp.crypto] - creating directory [/home/user2/.config/freerdp/certs]
[21:17:28:771] [28158:28159] [INFO][com.freerdp.crypto] - created directory [/home/user2/.config/freerdp/server]
[21:17:28:794] [28158:28159] [WARN][com.freerdp.crypto] - Certificate verification failure 'self signed certificate (18)' at stack position 0
[21:17:28:794] [28158:28159] [WARN][com.freerdp.crypto] - CN = WINLPE-SKILLS1-SRV
[21:17:28:795] [28158:28159] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
[21:17:28:795] [28158:28159] [ERROR][com.freerdp.crypto] - @           WARNING: CERTIFICATE NAME MISMATCH!           @
[21:17:28:795] [28158:28159] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
[21:17:28:795] [28158:28159] [ERROR][com.freerdp.crypto] - The hostname used for this connection (10.129.43.36:3389) 
[21:17:28:795] [28158:28159] [ERROR][com.freerdp.crypto] - does not match the name given in the certificate:
[21:17:28:795] [28158:28159] [ERROR][com.freerdp.crypto] - Common Name (CN):
[21:17:28:795] [28158:28159] [ERROR][com.freerdp.crypto] - 	WINLPE-SKILLS1-SRV
[21:17:28:795] [28158:28159] [ERROR][com.freerdp.crypto] - A valid certificate for the wrong name should NOT be trusted!
Certificate details for 10.129.43.36:3389 (RDP-Server):
	Common Name: WINLPE-SKILLS1-SRV
	Subject:     CN = WINLPE-SKILLS1-SRV
	Issuer:      CN = WINLPE-SKILLS1-SRV
	Thumbprint:  9f:f0:dd:28:f5:6f:83:db:5e:8c:5a:e9:5f:50:a4:50:2d:b3:e7:a7:af:f4:4a:8a:1a:08:f3:cb:46:c3:c3:e8
The above X.509 certificate could not be verified, possibly because you do not have
the CA certificate in your certificate store, or the certificate has expired.
Please look at the OpenSSL documentation on how to add a private CA to the store.
Do you trust the above certificate? (Y/T/N) y
Password: 
```

Muchas de las secciones que veremos en este módulo requieren herramientas como scripts de código abierto, archivos binarios precompilados y PoC de explotación. En los ejemplos prácticos, estos se pueden encontrar en el directorio `C:\Tools` del host de destino. Aunque se proporcionan la mayoría de las herramientas, desafíese a cargar archivos en el destino (utilizando las técnicas que se muestran en el módulo [`Transferencias de archivos`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md)) e incluso puedes probar a compilar algunas de las herramientas por tu cuenta utilizando [Visual Studio](https://visualstudio.microsoft.com/downloads/) .

¡Diviértete y no olvides pensar fuera de la caja!<br>
