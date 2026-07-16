
# Hardening en Windows

Un reforzamiento adecuado puede eliminar la mayoría, si no todas, las oportunidades de escalada de privilegios locales. Se deben tomar, como mínimo, las siguientes medidas para reducir el riesgo de que un atacante obtenga acceso a nivel de sistema.

***

## <mark style="color:purple;">Instalación segura y limpia del sistema operativo</mark>

Dedicar tiempo a desarrollar una imagen personalizada para su entorno puede ahorrarle mucho tiempo en el futuro, ya que no tendrá que solucionar problemas con los hosts. Puede hacerlo utilizando una imagen ISO limpia de la versión del sistema operativo que necesita, un servidor de implementación de Windows o una aplicación equivalente para enviar imágenes mediante disco o medios de red, y System Center Configuration Manager (si corresponde en su entorno). SCCM y WDS son temas mucho más extensos de los que podemos abordar aquí, así que los dejaremos para otra ocasión. Puede encontrar copias de sistemas operativos Windows [aquí](https://www.microsoft.com/en-us/software-download/) o descargarlas con la Herramienta de creación de medios de Microsoft. Esta imagen debe incluir, como mínimo:

1. Cualquier aplicación necesaria para las tareas diarias de sus empleados.
2. Cambios de configuración necesarios para garantizar la funcionalidad y seguridad del host en su entorno.
3. Las actualizaciones principales y secundarias actuales ya se han probado para su entorno y se consideran seguras para la implementación del host.

Siguiendo este proceso, puede asegurarse de eliminar cualquier bloatware o software no deseado preinstalado en el host al momento de la compra. Esto también garantiza que todos los hosts de su empresa comiencen con la misma configuración base, lo que le permite solucionar problemas, realizar cambios y enviar actualizaciones con mayor facilidad.

***

## <mark style="color:purple;">Actualizaciones y parches</mark>

[El orquestador de actualizaciones de Microsoft](https://docs.microsoft.com/en-us/windows/deployment/update/how-windows-update-works) ejecutará las actualizaciones automáticamente en segundo plano según la configuración. En la mayoría de los casos, esto significa que descargará e instalará las actualizaciones más recientes automáticamente. Tenga en cuenta que algunas actualizaciones requieren reiniciar el sistema para que surtan efecto, por lo que es recomendable reiniciar los hosts periódicamente. Si trabaja en un entorno empresarial, puede configurar un servidor WSUS dentro de su entorno para que cada equipo no tenga que descargarlas individualmente. En su lugar, podrán acceder al servidor WSUS configurado para obtener las actualizaciones necesarias.

En pocas palabras, el proceso de actualización se parece a esto:

![imagen](https://academy.hackthebox.com/storage/modules/67/Windows-Update-Process.png)

1. Windows Update Orchestrator se comunicará con los servidores de Microsoft Update o con su propio servidor WSUS para encontrar nuevas actualizaciones necesarias.
   * Esto sucederá a intervalos aleatorios para que sus hosts no inunden el servidor de actualización con solicitudes todas a la vez.
   * Luego, el orquestador comparará esa lista con la configuración de su host para extraer las actualizaciones adecuadas.
2. Una vez que el Orchestrator decide qué actualizaciones son aplicables, iniciará las descargas en segundo plano.
   * Las actualizaciones se almacenan en la carpeta temporal para su acceso. Se revisan los manifiestos de cada descarga y solo se extraen los archivos necesarios para su aplicación.
3. Luego, Update Orchestrator llamará al agente de instalación y le pasará la lista de acciones necesarias.
4. Desde aquí, el agente de instalación aplica las actualizaciones.
   * Tenga en cuenta que las actualizaciones aún no están finalizadas.
5. Una vez realizadas las actualizaciones, Orchestrator las finalizará con un reinicio del host.
   * Esto garantiza que cualquier modificación a los servicios o configuraciones críticas surta efecto.

Estas acciones se pueden administrar mediante [Windows Server Update Services](https://docs.microsoft.com/en-us/windows-server/administration/windows-server-update-services/get-started/windows-server-update-services-wsus)  (`WSUS`) o mediante la directiva de grupo. Independientemente del método elegido para aplicar actualizaciones, asegúrese de tener un plan y de que las actualizaciones se apliquen con regularidad para evitar cualquier problema. Como en todo lo relacionado con las TI, pruebe primero la implementación de las actualizaciones en un entorno de desarrollo (en varios hosts) antes de implementar una actualización en toda la empresa. Esto le ayudará a evitar dañar accidentalmente alguna aplicación o función crítica con las actualizaciones.

***

## <mark style="color:purple;">Gestión de la configuración</mark>

En Windows, la gestión de la configuración se puede realizar fácilmente mediante la directiva de grupo. Esta directiva nos permite administrar de forma centralizada la configuración y las preferencias de usuarios y equipos en todo el entorno. Esto se puede lograr mediante la Consola de administración de directivas de grupo (GPMC) o mediante PowerShell.

![imagen](https://academy.hackthebox.com/storage/modules/67/gpmc.png)

La directiva de grupo funciona mejor en un entorno de Active Directory, pero también permite administrar la configuración local del equipo y del usuario mediante la directiva de grupo local. Desde aquí, puede administrar todo, desde los fondos de pantalla, los marcadores y otras configuraciones del navegador de cada usuario, hasta cómo y cuándo Windows Defender analiza el host y realiza actualizaciones. Este proceso puede ser muy granular, así que asegúrese de tener un plan para la implementación de cualquier nueva directiva de grupo creada o modificada.

***

## <mark style="color:purple;">Gestión de usuarios</mark>

Limitar el número de cuentas de usuario y administrador en cada sistema y garantizar que los intentos de inicio de sesión (válidos o no) se registren y supervisen puede contribuir significativamente a la protección del sistema y a la monitorización de posibles problemas. También es recomendable implementar una política de contraseñas robusta y la autenticación de dos factores, rotar las contraseñas periódicamente y restringir que los usuarios reutilicen contraseñas antiguas mediante la configuración `Password Policy` de la directiva de grupo. Esta configuración se puede encontrar en GPMC en la ruta `Computer Configuration\Windows Settings\Security Settings\Account Policies\Password Policy`. También debemos comprobar que los usuarios no estén asignados a grupos que les otorguen permisos excesivos innecesarios para sus tareas diarias (por ejemplo, un usuario normal con derechos de administrador de dominio) y aplicar restricciones de inicio de sesión para las cuentas de administrador.

![imagen](https://academy.hackthebox.com/storage/modules/67/password-policy.png)

Esta captura de pantalla muestra un ejemplo de cómo utilizar el editor de políticas de grupo para ver y modificar la política de contraseñas en la subárbol mencionada anteriormente.

La autenticación de dos factores también puede ayudar a prevenir inicios de sesión fraudulentos. En resumen, la 2FA requiere que sepas `password or pin`y tengas algo `a token, id card, or authenticator application key code`. Este paso reducirá significativamente la posibilidad de que las cuentas de usuario se usen con fines maliciosos.

***

## <mark style="color:purple;">Auditoría</mark>

Realice comprobaciones periódicas de seguridad y configuración de todos los sistemas. Existen varias líneas base de seguridad, como las [Guías de Implementación Técnica de Seguridad (STIG) de DISA o ](https://public.cyber.mil/stigs/)[el Kit de Herramientas de Cumplimiento de Seguridad](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-security-configuration-framework/security-compliance-toolkit-10) de Microsoft , que pueden seguirse para establecer un estándar de seguridad en su entorno. Existen muchos marcos de cumplimiento, como [ISO27001](https://www.iso.org/isoiec-27001-information-security.html) , [PCI-DSS](https://www.pcisecuritystandards.org/pci_security/) e [HIPAA,](https://www.hhs.gov/hipaa/for-professionals/security/index.html) que una organización puede utilizar para ayudar a establecer líneas base de seguridad. Todos estos deben usarse como guías de referencia y no como la base de un programa de seguridad. Un programa de seguridad sólido debe tener controles adaptados a las necesidades de la organización, el entorno operativo y los tipos de datos que almacenan y procesan (es decir, información personal de salud, datos financieros, secretos comerciales o información disponible públicamente).

![imagen](https://academy.hackthebox.com/storage/modules/67/stig-viewer.png)

La ventana del visor STIG que se ve arriba permite realizar una auditoría de la seguridad de un host. Importamos una lista de verificación disponible en el enlace STIG mencionado anteriormente y revisamos las reglas paso a paso. Cada ID de regla corresponde a una comprobación de seguridad o una tarea de refuerzo para mejorar la seguridad general del host. En el panel derecho, se pueden ver detalles sobre las acciones necesarias para completar la comprobación STIG.

Una auditoría y revisión de configuración no sustituyen una prueba de penetración ni otras evaluaciones técnicas y prácticas, y suelen considerarse un ejercicio de verificación de requisitos en el que una organización aprueba una auditoría de controles por realizar lo mínimo indispensable. Estas revisiones pueden complementar los análisis de vulnerabilidades regulares, las pruebas de penetración y los programas de gestión de parches, vulnerabilidades y configuración.

***

## <mark style="color:purple;">Logging</mark>

Un registro y una correlación de registros adecuados pueden marcar la diferencia al solucionar un problema o detectar una amenaza potencial en su red. A continuación, analizaremos algunas aplicaciones y registros que pueden ayudarle a mejorar su seguridad en un host Windows.

***

### Sysmon

Sysmon es una herramienta desarrollada por Microsoft e incluida en la suite Sysinternals que mejora la capacidad de registro y recopilación de eventos en Windows. Sysmon proporciona información detallada sobre procesos, conexiones de red, lecturas y escrituras de archivos, intentos y éxitos de inicio de sesión, y mucho más. Estos registros se pueden correlacionar y enviar a un SIEM para su análisis, lo que proporciona una mejor comprensión de lo que ocurre en nuestro entorno. Sysmon es persistente en el host y comienza a escribir registros al inicio. Es una herramienta extremadamente útil si se implementa correctamente. Para obtener más información sobre Sysmon, consulte [la información sobre Sysmon](https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon) .

Todos los registros que Sysmon escribe se almacenarán en la sección: `Applications and Service Logs\Microsoft\Windows\Sysmon\Operational`. Puede verlos utilizando el visor de eventos y explorando la sección.

***

### Registros de red y host

Herramientas como [PacketBeat](https://www.elastic.co/beats/packetbeat) , implementaciones de IDS/IPS como los sensores Security Onion y otras soluciones de monitoreo de red pueden ayudar a sus administradores a completar la información. Recopilan y envían registros de tráfico de red a sus soluciones de monitoreo y SIEMS.

***

### Medidas clave de Hardening

Esta no es de ninguna manera una lista exhaustiva, pero algunas medidas de endurecimiento simples son:

* El arranque seguro y el cifrado de disco con BitLocker deben estar habilitados y en uso.
* Auditar archivos y directorios grabables y cualquier binario con la capacidad de iniciar otras aplicaciones.
* Asegúrese de que todas las tareas programadas y los scripts que se ejecutan con privilegios elevados especifiquen todos los binarios o ejecutables utilizando la ruta absoluta.
* No almacene credenciales en texto sin formato en archivos legibles para todo el mundo en el host o en unidades compartidas.
* Limpia los directorios de inicio y el historial de PowerShell.
* Asegúrese de que los usuarios con bajos privilegios no puedan modificar ninguna biblioteca personalizada llamada por los programas.
* Elimine todos los paquetes y servicios innecesarios que potencialmente aumenten la superficie de ataque.
* Utilice las funciones Device Guard y Credential Guard integradas por Microsoft en Windows 10 y la mayoría de los nuevos sistemas operativos de servidor.
* Utilice la política de grupo para aplicar cualquier cambio de configuración necesario en los sistemas de la empresa.

Si se toma el tiempo de leer una lista de verificación de STIG, notará que muchas de estas medidas están incluidas en las comprobaciones. Tenga en cuenta lo que utilizan sus entornos y determine cómo estas medidas afectarán la capacidad para cumplir la misión. No implemente medidas de reforzamiento generalizadas en toda su red a ciegas, ya que lo que funciona para una organización puede no funcionar para otra. Es fundamental saber que está intentando proteger y aplicar las medidas adecuadas según los requisitos del negocio.

***

## <mark style="color:purple;">Conclusión</mark>

Como hemos visto, existen muchas maneras de escalar privilegios en sistemas Windows: desde simples configuraciones erróneas y exploits públicos para servicios vulnerables conocidos, hasta el desarrollo de exploits basado en bibliotecas y ejecutables personalizados. Una vez obtenido el acceso de administrador o de nivel SYSTEM, resulta más fácil usarlo como punto de apoyo para futuras explotaciones de la red. El fortalecimiento del sistema es igualmente crucial tanto para pequeñas como para grandes empresas.&#x20;

Al observar las tendencias de ataques actuales, podemos ver que a los atacantes ya no les importa quién es la víctima, siempre y cuando puedan obtener lo que desean del intercambio. Las directrices y controles de mejores prácticas existen en diversas formas. Las revisiones deben incluir una combinación de pruebas manuales prácticas y análisis automatizado de la configuración con herramientas como Nessus, seguido de la validación de los resultados. Al aplicar parches para los ataques más recientes e implementar sofisticadas capacidades de monitorización, no olvide los aspectos básicos y las opciones más fáciles de abordar que se tratan en este módulo.

Por último, asegúrese de que su personal reciba constantemente desafíos y capacitación y se mantenga a la vanguardia de las nuevas vulnerabilidades y PoC de explotación para que su organización pueda permanecer protegida a medida que los investigadores continúan descubriendo nuevas vías de ataque.
