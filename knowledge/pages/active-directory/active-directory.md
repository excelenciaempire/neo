
# Active Directory

* Almacena información acerca de los recursos de una red: servidores, impresoras, cuentas de usuario, equipos…
* Utiliza un almacén de datos estructurados
* Active Directory Domain Services

***

## <mark style="color:purple;">Estructura Active Directory</mark>

&#x20;Bosques > Dominios > Unidades Organizativas

* Un bosque contiene dominios
* Los dominios pueden contener una o varios OUs
* La información de los Dominios y OUs se almacena en un <mark style="color:purple;">controlador de dominio o DC</mark>. Este almacén se denomina Data Store
* La información se almacena en forma de objeto, y todos los objetos están definidos por un esquema

### Bosques

* Los bosques son el nivel organizativo mas alto dentro de AD. Cada bosque comparte un único directorio
* Los bosques pueden contener uno o varios Dominios

### Dominios

Un Dominio es una partición lógica de objetos dentro de un Bosque que comparten configuraciones comunes de administración, seguridad y replicación.

* Garantiza la identidad de un usuario en toda la red
* Proporciona servicios de autenticación y autorización
* Permiten replicar la información entre diferentes Controladores de Dominio y gestionarlos como una única entidad
* Permite la creación de relaciones de confianza

### Unidad organizativa (OU)

Es un objeto contenedor que permite organizar objetos dentro de un dominio

* Visualización organizada de objetos (usuarios, equipos...)
* Agrupa objetos a los que aplicar Políticas de Grupo
* Agrupa objetos de manera que se puedan delegar permisos de gestión a otros usuarios y grupos dentro del dominio

### Domain Controller (DC)

Un Domain Controller (DC) es un servidor que ejecuta el servicio de directorio Active Directory de Microsoft Windows. El Domain Controller es el elemento central de la infraestructura de Active Directory y es responsable de autenticar y autorizar a los usuarios y equipos en la red, así como de proporcionar servicios de gestión de políticas de seguridad, permisos y recursos de la red.

Algunas de las funciones del Domain Controller incluyen:

* Autenticación y autorización de usuarios y equipos de la red.
* Administración centralizada de cuentas de usuario y equipos.
* Administración centralizada de políticas de seguridad y permisos.
* Replicación de datos de Active Directory a través de la red.
* Integración con otros servicios de Microsoft, como Exchange y SharePoint.

***

## <mark style="color:purple;">Conexiones en Active Directory</mark>

### **Conexión a través de xfreeRDP**

Podemos conectarnos a través de la línea de comando usando el comando:

```shell-session
afsh4ck@kali$ xfreerdp /v:<MS01 target IP> /u:htb-student /p:Academy_student_AD!
```

### **Conexión a través de SSH**

Podemos conectarnos al host usando el siguiente comando y luego ingresar la contraseña:

```shell-session
afsh4ck@kali$ ssh htb-student@<ATTACK01 target IP>
```

***

## <mark style="color:purple;">Herramientas útiles</mark>

Gran parte de estas herramientas las tengo recogidas en un único repositorio de GitHub, desde el que nos las podemos descargar directamente en un equipo dentro de una red Active Directory para empezar a hacer auditorías:

{% embed url="<https://github.com/afsh4ck/AD-Tools>" %}

<table data-header-hidden><thead><tr><th width="174"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Descripción</td></tr><tr><td><a href="https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1">PowerView</a> / <a href="https://github.com/dmchell/SharpView">SharpView</a></td><td>Se utiliza una herramienta PowerShell y un puerto .NET de la misma para obtener conocimiento de la situación en AD. Estas herramientas se pueden utilizar como reemplazo de varios <code>net*</code>comandos de Windows y más. PowerView y SharpView pueden ayudarnos a recopilar gran parte de los datos que recopila BloodHound, pero requiere más trabajo para establecer relaciones significativas entre todos los puntos de datos. Estas herramientas son excelentes para verificar qué acceso adicional podemos tener con un nuevo conjunto de credenciales, apuntar a usuarios o computadoras específicas, o encontrar algunas "victorias rápidas", como usuarios que pueden ser atacados mediante Kerberoasting o ASREPRoasting.</td></tr><tr><td><a href="https://github.com/BloodHoundAD/BloodHound">BloodHound</a></td><td>Se utiliza para trazar visualmente las relaciones de AD y ayudar a planificar rutas de ataque que de otro modo pasarían desapercibidas. Utiliza el procesador <a href="https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors">SharpHound PowerShell o C# para recopilar datos que luego se importarán a la aplicación BloodHound JavaScript (Electron) con una base de datos </a><a href="https://neo4j.com/">Neo4j</a> para el análisis gráfico del entorno AD.</td></tr><tr><td><a href="https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors">SharpHound</a></td><td>El recopilador de datos de C# para recopilar información de Active Directory sobre diversos objetos de AD, como usuarios, grupos, computadoras, ACL, GPO, atributos de usuario y computadora, sesiones de usuario y más. La herramienta produce archivos JSON que luego pueden ingerirse en la herramienta GUI de BloodHound para su análisis.</td></tr><tr><td><a href="https://github.com/fox-it/BloodHound.py">BloodHound.py</a></td><td>Un ingeridor BloodHound basado en Python basado en el <a href="https://github.com/CoreSecurity/impacket/">kit de herramientas Impacket</a> . Es compatible con la mayoría de los métodos de recopilación de BloodHound y se puede ejecutar desde un host de ataque que no esté unido a un dominio. La salida se puede incorporar a la GUI de BloodHound para su análisis.</td></tr><tr><td><a href="https://github.com/ropnop/kerbrute">Kerbrute</a></td><td>Una herramienta escrita en Go que utiliza la autenticación previa de Kerberos para enumerar cuentas de Active Directory, realizar pulverización de contraseñas y fuerza bruta.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket">Impacket toolkit</a></td><td>Una colección de herramientas escritas en Python para interactuar con protocolos de red. El conjunto de herramientas contiene varios scripts para enumerar y atacar Active Directory.</td></tr><tr><td><a href="https://github.com/lgandx/Responder">Responder</a></td><td>Responder es una herramienta diseñada específicamente para envenenar LLMNR, NBT-NS y MDNS, con muchas funciones diferentes.</td></tr><tr><td><a href="https://github.com/Kevin-Robertson/Inveigh/blob/master/Inveigh.ps1">Inveigh.ps1</a></td><td>Similar a Responder, una herramienta de PowerShell para realizar diversos ataques de envenenamiento y suplantación de red.</td></tr><tr><td><a href="https://github.com/Kevin-Robertson/Inveigh/tree/master/Inveigh">C# Inveigh (InveighZero)</a></td><td>La versión C# de Inveigh con una consola semiinteractiva para interactuar con datos capturados, como hash de nombre de usuario y contraseña.</td></tr><tr><td><a href="https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/rpcinfo">rpcinfo</a></td><td>La utilidad rpcinfo se utiliza para consultar el estado de un programa RPC o enumerar la lista de servicios RPC disponibles en un host remoto. La opción "-p" se utiliza para especificar el host de destino. Por ejemplo, el comando "rpcinfo -p 10.0.0.1" devolverá una lista de todos los servicios RPC disponibles en el host remoto, junto con su número de programa, número de versión y protocolo. Tenga en cuenta que este comando debe ejecutarse con privilegios suficientes.</td></tr><tr><td><a href="https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html">rpcclient</a></td><td>Una parte de la suite Samba en distribuciones de Linux que se puede utilizar para realizar una variedad de tareas de enumeración de Active Directory a través del servicio RPC remoto.</td></tr><tr><td><a href="https://github.com/byt3bl33d3r/CrackMapExec">CrackMapExec (CME)</a></td><td>CME es un conjunto de herramientas de enumeración, ataque y post-explotación que puede ayudarnos enormemente en la enumeración y realización de ataques con los datos que recopilamos. CME intenta "vivir de la tierra" y abusar de las funciones y protocolos integrados de AD como SMB, WMI, WinRM y MSSQL.</td></tr><tr><td><a href="https://github.com/GhostPack/Rubeus">Rubeus</a></td><td>Rubeus es una herramienta C# creada para el abuso de Kerberos.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetUserSPNs.py">GetUserSPNs.py</a></td><td>Otro módulo de Impacket orientado a encontrar nombres de principales de servicio vinculados a usuarios normales.</td></tr><tr><td><a href="https://hashcat.net/hashcat/">Hashcat</a></td><td>Una excelente herramienta para descifrar hash y recuperar contraseñas.</td></tr><tr><td><a href="https://github.com/CiscoCXSecurity/enum4linux">enum4linux</a></td><td>Una herramienta para enumerar información de sistemas Windows y Samba.</td></tr><tr><td><a href="https://github.com/cddmp/enum4linux-ng">enum4linux-ng</a></td><td>Una reelaboración de la herramienta Enum4linux original que funciona un poco diferente.</td></tr><tr><td><a href="https://linux.die.net/man/1/ldapsearch">ldapsearch</a></td><td>Interfaz incorporada para interactuar con el protocolo LDAP.</td></tr><tr><td><a href="https://github.com/ropnop/windapsearch">windapsearch</a></td><td>Un script de Python utilizado para enumerar usuarios, grupos y computadoras de AD mediante consultas LDAP. Útil para automatizar consultas LDAP personalizadas.</td></tr><tr><td><a href="https://github.com/dafthack/DomainPasswordSpray">DomainPasswordSpray.ps1</a></td><td>DomainPasswordSpray es una herramienta escrita en PowerShell para realizar un ataque de pulverización de contraseñas contra los usuarios de un dominio.</td></tr><tr><td><a href="https://github.com/leoloobeek/LAPSToolkit">LAPSToolkit</a></td><td>El kit de herramientas incluye funciones escritas en PowerShell que aprovechan PowerView para auditar y atacar entornos de Active Directory que han implementado la solución de contraseña de administrador local (LAPS) de Microsoft.</td></tr><tr><td><a href="https://github.com/ShawnDEvans/smbmap">smbmap</a></td><td>Enumeración de recursos compartidos de SMB en un dominio.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/psexec.py">psexec.py</a></td><td>Como parte del conjunto de herramientas de Impacket, nos proporciona una funcionalidad similar a Psexec en forma de un shell semiinteractivo.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/wmiexec.py">wmiexec.py</a></td><td>Como parte del kit de herramientas Impacket, proporciona la capacidad de ejecución de comandos a través de WMI.</td></tr><tr><td><a href="https://github.com/SnaffCon/Snaffler">Snaffler</a></td><td>Útil para buscar información (como credenciales) en Active Directory en computadoras con archivos compartidos accesibles.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbserver.py">smbserver.py</a></td><td>Ejecución simple de servidor SMB para interacción con hosts de Windows. Manera sencilla de transferir archivos dentro de una red.</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc731241(v=ws.11)">setspn.exe</a></td><td>Agrega, lee, modifica y elimina la propiedad del directorio de nombres principales de servicio (SPN) para una cuenta de servicio de Active Directory.</td></tr><tr><td><a href="https://github.com/ParrotSec/mimikatz">Mimikatz</a></td><td>Realiza muchas funciones. En particular, los ataques pass-the-hash, la extracción de contraseñas en texto plano y la extracción de tickets Kerberos de la memoria de un host.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/secretsdump.py">secretsdump.py</a></td><td>Módulo de Impacket que vuelca de forma remota los secretos de SAM y LSA desde un host.</td></tr><tr><td><a href="https://github.com/Hackplayers/evil-winrm">evil-winrm</a></td><td>Nos proporciona un shell interactivo en un host a través del protocolo WinRM.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/mssqlclient.py">mssqlclient.py</a></td><td>Como parte del kit de herramientas Impacket, brinda la capacidad de interactuar con bases de datos MSSQL.</td></tr><tr><td><a href="https://github.com/Ridter/noPac">noPac.py</a></td><td>Aproveche el combo utilizando CVE-2021-42278 y CVE-2021-42287 para hacerse pasar por DA de un usuario de dominio estándar.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/rpcdump.py">rpcdump.py</a></td><td>Parte del conjunto de herramientas Impacket, asignador de puntos finales RPC.</td></tr><tr><td><a href="https://github.com/cube0x0/CVE-2021-1675/blob/main/CVE-2021-1675.py">CVE-2021-1675.py</a></td><td>Printnightmare PoC en Python.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/ntlmrelayx.py">ntlmrelayx.py</a></td><td>Como parte del conjunto de herramientas Impacket, realiza ataques de retransmisión SMB.</td></tr><tr><td><a href="https://github.com/topotam/PetitPotam">PetitPotam.py</a></td><td>Herramienta PoC para CVE-2021-36942 para obligar a los hosts de Windows a autenticarse en otras máquinas a través de MS-EFSRPC EfsRpcOpenFileRaw u otras funciones.</td></tr><tr><td><a href="https://github.com/dirkjanm/PKINITtools/blob/master/gettgtpkinit.py">gettgtpkinit.py</a></td><td>Herramienta de manipulación de certificados y TGT.</td></tr><tr><td><a href="https://github.com/dirkjanm/PKINITtools/blob/master/getnthash.py">getnthash.py</a></td><td>Esta herramienta utilizará un TGT existente para solicitar un PAC para el usuario actual que usa U2U.</td></tr><tr><td><a href="https://github.com/dirkjanm/adidnsdump">adidnsdump</a></td><td>Una herramienta para enumerar y volcar registros DNS de un dominio. Similar a realizar una transferencia de zona DNS.</td></tr><tr><td><a href="https://github.com/t0thkr1s/gpp-decrypt">gpp-descifrar</a></td><td>Extrae nombres de usuario y contraseñas de los archivos de preferencias de políticas de grupo.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetNPUsers.py">GetNPUsers.py</a></td><td>Parte del kit de herramientas Impacket. Se utiliza para realizar el ataque ASREPRoasting para enumerar y obtener hashes AS-REP para usuarios con la configuración "No requiere autenticación previa de Kerberos". Estos hashes luego se introducen en una herramienta como Hashcat para intentar descifrar contraseñas fuera de línea.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/lookupsid.py">lookupsid.py</a></td><td>Herramienta de fuerza bruta SID.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/ticketer.py">ticketer.py</a></td><td>Una herramienta para la creación y personalización de billetes TGT/TGS. Se puede utilizar para la creación de Golden Ticket, ataques de confianza de niño a padre, etc.</td></tr><tr><td><a href="https://github.com/SecureAuthCorp/impacket/blob/master/examples/raiseChild.py">raiseChild.py</a></td><td>Parte del kit de herramientas Impacket, es una herramienta para la escalada automatizada de privilegios de dominio infantil a principal.</td></tr><tr><td><a href="https://docs.microsoft.com/en-us/sysinternals/downloads/adexplorer">Active Directory Explorer</a></td><td>Active Directory Explorer (AD Explorer) es un visor y editor de AD. Se puede utilizar para navegar por una base de datos de AD y ver las propiedades y atributos de los objetos. También se puede utilizar para guardar una instantánea de una base de datos de AD para su análisis fuera de línea. Cuando se carga una instantánea de AD, se puede explorar como una versión en vivo de la base de datos. También se puede utilizar para comparar dos instantáneas de bases de datos de AD para ver cambios en objetos, atributos y permisos de seguridad.</td></tr><tr><td><a href="https://www.pingcastle.com/documentation/">PingCastle</a></td><td>Se utiliza para auditar el nivel de seguridad de un entorno de AD basándose en un marco de madurez y evaluación de riesgos (basado en <a href="https://en.wikipedia.org/wiki/Capability_Maturity_Model_Integration">CMMI</a> adaptado a la seguridad de AD).</td></tr><tr><td><a href="https://github.com/Group3r/Group3r">Group3r</a></td><td>Group3r es útil para auditar y encontrar configuraciones erróneas de seguridad en objetos de política de grupo (GPO) de AD.</td></tr><tr><td><a href="https://github.com/adrecon/ADRecon">ADRecon</a></td><td>Una herramienta utilizada para extraer diversos datos de un entorno AD de destino. Los datos se pueden generar en formato Microsoft Excel con vistas resumidas y análisis para ayudar con el análisis y ofrecer una imagen del estado general de seguridad del entorno.</td></tr></tbody></table>

***

## <mark style="color:purple;">Escenario</mark>

Pongamos que somos Pentesters trabajando para `CAT-5 Security`. Después de algunos compromisos exitosos siguiendo al equipo, los miembros más senior quieren ver qué tan bien podemos hacerlo al iniciar una evaluación por nuestra cuenta. El Red Team Leader nos envió el siguiente correo electrónico detallando lo que debemos lograr.

**Correo electrónico de tareas**

![imagen](https://academy.hackthebox.com/storage/modules/143/scenario-email.png)

Este módulo nos permitirá practicar nuestras habilidades (tanto anteriores como nuevas) con estas tareas. La evaluación final de este módulo es la ejecución de `dos` pruebas de penetración internas contra la empresa `Inlanefreight`. Durante estas evaluaciones, trabajaremos a través de una prueba de penetración interna que simulará comenzar desde una posición de infracción externa y una segunda que comenzará con una caja de ataque dentro de la red interna, como los clientes suelen solicitar.&#x20;

Completar las evaluaciones de habilidades significa completar con éxito las tareas mencionadas en el documento de alcance y el correo electrónico de tareas anteriores. Al hacerlo, demostraremos una comprensión firme de muchos conceptos de enumeración y ataques de AD automatizados y manuales, conocimiento y experiencia con una amplia gama de herramientas y la capacidad de interpretar los datos recopilados de un entorno de AD para tomar decisiones críticas para avanzar en la evaluación.&#x20;

El contenido de este módulo está destinado a cubrir los conceptos básicos de enumeración necesarios para que cualquiera pueda realizar con éxito pruebas de penetración internas en entornos de Active Directory. También cubriremos muchas de las técnicas de ataque más comunes con gran profundidad mientras trabajamos en algunos conceptos más avanzados como introducción al material centrado en AD que se cubrirá en módulos más avanzados.

A continuación encontrará un documento de alcance completo para el compromiso que contiene toda la información pertinente proporcionada por el cliente.

***

### <mark style="color:purple;">Alcance de la evaluación</mark>

Las siguientes `IPs`, `hosts` y `dominios` que se definen a continuación conforman el alcance de la evaluación.

**Dentro del alcance de la evaluación**

<table data-header-hidden><thead><tr><th width="346"></th><th></th></tr></thead><tbody><tr><td><strong>Rango/Dominio</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>INLANEFREIGHT.LOCAL</code></td><td>Dominio del cliente para incluir AD y servicios web.</td></tr><tr><td><code>LOGISTICS.INLANEFREIGHT.LOCAL</code></td><td>Subdominio del cliente</td></tr><tr><td><code>FREIGHTLOGISTICS.LOCAL</code></td><td>Empresa filial propiedad de Inlanefreight. Confianza forestal externa con INLANEFREIGHT.LOCAL</td></tr><tr><td><code>172.16.5.0/23</code></td><td>Subred interna dentro del alcance.</td></tr></tbody></table>

**Fuera del alcance**

* `Cualquier otro subdominio de INLANEFREIGHT.LOCAL`&#x20;
* `Cualquier subdominio de FREIGHTLOGISTICS.LOCAL`&#x20;
* `Cualquier ataque de phishing o ingeniería social`&#x20;
* `Cualquier otra IPS/dominios/subdominios no mencionados explícitamente`&#x20;
* `Cualquier tipo de ataque contra el sitio web inlanefreight.com del mundo real fuera de la enumeración pasiva que se muestra en este módulo`

***

### <mark style="color:purple;">Métodos utilizados</mark>

Están autorizados los siguientes métodos para evaluar Inlanefreight y sus sistemas:

#### Recopilación de información externa (verificaciones pasivas)

Se autoriza la recopilación de información externa para demostrar los riesgos asociados a la información que se puede recopilar sobre la empresa a través de Internet. Para simular un ataque del mundo real, CAT-5 y sus asesores recopilarán información externa desde una perspectiva anónima en Internet sin proporcionar información por adelantado sobre Inlanefreight fuera de lo que se proporciona en este documento.

Cat-5 realizará una enumeración pasiva para descubrir información que pueda ayudar con las pruebas internas. Las pruebas emplearán varios grados de recopilación de información de recursos de código abierto para identificar datos de acceso público que puedan representar un riesgo para Inlanefreight y ayudar con la prueba de penetración interna. No se realizarán enumeraciones activas, escaneos de puertos ni ataques contra direcciones IP del "mundo real" conectadas a Internet ni contra el sitio web ubicado en `https://www.inlanefreight.com`.

#### Pruebas internas

La parte de evaluación interna está diseñada para demostrar los riesgos asociados con las vulnerabilidades en hosts y servicios internos ( `Active Directory specifically`) al intentar emular vectores de ataque desde dentro del área de operaciones de Inlanefreight. El resultado permitirá a Inlanefreight evaluar los riesgos de las vulnerabilidades internas y el impacto potencial de una vulnerabilidad explotada con éxito.

Para simular un ataque del mundo real, Cat-5 llevará a cabo la evaluación desde una perspectiva interna no confiable sin información previa más allá de la proporcionada en esta documentación y descubierta a partir de pruebas externas. Las pruebas comenzarán desde una posición anónima en la red interna con el objetivo de obtener credenciales de usuario del dominio, enumerar el dominio interno, ganar terreno y moverse lateral y verticalmente para lograr el compromiso de todos los dominios internos dentro del alcance. Los sistemas informáticos y las operaciones de red no se interrumpirán intencionalmente durante la prueba.

#### Pruebas de contraseñas

Los archivos de contraseñas capturados desde los dispositivos de Inlanefreight, o proporcionados por la organización, se pueden cargar en estaciones de trabajo fuera de línea para descifrarlos y utilizarlos para obtener mayor acceso y lograr los objetivos de la evaluación. En ningún momento se revelará un archivo de contraseña capturado o las contraseñas descifradas a personas que no participen oficialmente en la evaluación. Todos los datos se almacenarán de forma segura en sistemas aprobados y de propiedad de Cat-5 y se conservarán durante un período de tiempo definido en el contrato oficial entre Cat-5 e Inlanefreight.
