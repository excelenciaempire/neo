
# ACLs - Access Control Lists

Por razones de seguridad, no todos los usuarios y equipos de un entorno de AD pueden acceder a todos los objetos y archivos. Estos tipos de permisos se controlan mediante listas de control de acceso (ACL). Una pequeña configuración incorrecta de una ACL puede suponer una grave amenaza para la seguridad del dominio y filtrar permisos a otros objetos que no los necesitan.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

***

## <mark style="color:purple;">Descripción general de la lista de control de acceso (ACL)</mark>

En su forma más simple, las ACL son listas que definen:

1. Quién tiene acceso a qué activo o recurso
2. El nivel de acceso que se les otorga.&#x20;

Las configuraciones en una ACL se denominan `Access Control Entries`( `ACEs`). Cada ACE se asigna a un usuario, grupo o proceso (también conocido como entidad de seguridad) y define los derechos otorgados a esa entidad. Cada objeto tiene una ACL, pero puede tener varias ACE porque varias entidades de seguridad pueden acceder a los objetos en AD. Las ACL también se pueden usar para auditar el acceso dentro de AD.

Hay dos tipos de ACL:

1. `Discretionary Access Control List`( `DACL`) - Define a qué entidades de seguridad se les concede o se les niega el acceso a un objeto. Las DACL se componen de ACE que permiten o niegan el acceso. Cuando alguien intenta acceder a un objeto, el sistema comprobará la DACL para saber el nivel de acceso permitido. Si no existe una DACL para un objeto, todos los que intenten acceder al objeto tendrán todos los derechos. Si existe una DACL, pero no tiene ninguna entrada ACE que especifique configuraciones de seguridad específicas, el sistema negará el acceso a todos los usuarios, grupos o procesos que intenten acceder a ella.
2. `System Access Control Lists`( `SACL`) - Permite a los administradores registrar los intentos de acceso realizados a objetos protegidos.

En la imagen siguiente, vemos la ACL de la cuenta de usuario `forend`. Cada elemento que se muestra debajo de `Permission entries` constituye la `DACL` de la cuenta de usuario, mientras que las entradas individuales (como `Full Control` o `Change Password`) son entradas de ACE que muestran los derechos otorgados sobre este objeto de usuario a varios usuarios y grupos.

**Visualización de la ACL del usuario forend**

![imagen](https://academy.hackthebox.com/storage/modules/143/DACL_example.png)

Los SACL se pueden ver dentro de la pestaña `Auditing`.

**Visualización de las SACL a través de la pestaña Auditoría**

![imagen](https://academy.hackthebox.com/storage/modules/143/SACL_example.png)

***

### Entradas de control de acceso (ACE)

Como se indicó anteriormente, las listas de control de acceso (ACL) contienen entradas ACE que nombran a un usuario o grupo y el nivel de acceso que tienen sobre un objeto protegible determinado. Existen `3 tipos` principales de ACE que se pueden aplicar a todos los objetos protegibles en AD:

<table data-header-hidden><thead><tr><th width="244"></th><th></th></tr></thead><tbody><tr><td><strong>AS</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>Access denied ACE</code></td><td>Se utiliza dentro de una DACL para mostrar que a un usuario o grupo se le niega explícitamente el acceso a un objeto.</td></tr><tr><td><code>Access allowed ACE</code></td><td>Se utiliza dentro de una DACL para mostrar que a un usuario o grupo se le concede explícitamente acceso a un objeto.</td></tr><tr><td><code>System audit ACE</code></td><td>Se utiliza dentro de una SACL para generar registros de auditoría cuando un usuario o grupo intenta acceder a un objeto. Registra si se concedió o no el acceso y qué tipo de acceso se produjo</td></tr></tbody></table>

Cada ACE está formado por los siguientes `4 componentes`:

1. El identificador de seguridad (SID) del usuario/grupo que tiene acceso al objeto (o nombre principal gráficamente)
2. Una flag que indica el tipo de ACE (acceso denegado, permitido o ACE de auditoría del sistema)
3. Un conjunto de indicadores que especifican si los contenedores/objetos secundarios pueden heredar o no la entrada ACE dada del objeto primario o padre.
4. Una [máscara de acceso](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-dtyp/7a53f60e-e730-4dfe-bbe9-b21b62eb790b?redirectedfrom=MSDN) que es un valor de 32 bits que define los derechos otorgados a un objeto

Podemos visualizar esto gráficamente en `Active Directory Users and Computers`( `ADUC`). En la imagen de ejemplo a continuación, podemos ver lo siguiente para la entrada ACE del usuario `forend`:

**Visualización de permisos a través de usuarios y equipos de Active Directory**

![imagen](https://academy.hackthebox.com/storage/modules/143/ACE_example.png)

1. La directora de seguridad es Angela Dunn ( <adunn@inlanefreight.local> )
2. El tipo ACE es`Allow`
3. La herencia se aplica a "Este objeto y todos los objetos descendientes", lo que significa que cualquier objeto secundario del objeto `forend` tendría los mismos permisos otorgados.
4. Los derechos otorgados al objeto, nuevamente mostrados gráficamente en este ejemplo

Cuando se verifican las listas de control de acceso para determinar permisos, se verifican de arriba a abajo hasta que se encuentra un acceso denegado en la lista.

***

## <mark style="color:purple;">¿Por qué son importantes las ACE?</mark>

Los atacantes utilizan las entradas ACE para obtener más acceso o establecer la persistencia. Estas pueden ser muy útiles para nosotros como evaluadores de penetración, ya que muchas organizaciones desconocen las ACE aplicadas a cada objeto o el impacto que pueden tener si se aplican de forma incorrecta. Las herramientas de análisis de vulnerabilidades no pueden detectarlas y, a menudo, pasan desapercibidas durante muchos años, especialmente en entornos grandes y complejos.&#x20;

Durante una evaluación en la que el cliente se ha ocupado de todos los errores o configuraciones incorrectas de AD que están al alcance de la mano, el abuso de ACL puede ser una excelente manera de movernos lateralmente o verticalmente e incluso lograr un compromiso total del dominio. Algunos ejemplos de permisos de seguridad de objetos de Active Directory son los siguientes. Se pueden enumerar (y visualizar) utilizando una herramienta como BloodHound y todos se pueden abusar con PowerView, entre otras herramientas:

* `ForceChangePassword`abusado con`Set-DomainUserPassword`
* `Add Members`abusado con`Add-DomainGroupMember`
* `GenericAll`abusado con `Set-DomainUserPassword`o`Add-DomainGroupMember`
* `GenericWrite`abusado con`Set-DomainObject`
* `WriteOwner`abusado con`Set-DomainObjectOwner`
* `WriteDACL`abusado con`Add-DomainObjectACL`
* `AllExtendedRights`abusado con `Set-DomainUserPassword`o`Add-DomainGroupMember`
* `Addself`abusado con`Add-DomainGroupMember`

En este módulo, cubriremos la enumeración y el aprovechamiento de cuatro ACE específicas para resaltar el poder de los ataques ACL:

* [`ForceChangePassword`](https://bloodhound.readthedocs.io/en/latest/data-analysis/edges.html#forcechangepassword) : nos da el derecho de restablecer la contraseña de un usuario sin conocer primero su contraseña (se debe usar con precaución y, por lo general, es mejor consultar a nuestro cliente antes de restablecer las contraseñas).
* [`GenericWrite`](https://bloodhound.readthedocs.io/en/latest/data-analysis/edges.html#genericwrite) : nos da el derecho de escribir en cualquier atributo no protegido de un objeto. Si tenemos este acceso sobre un usuario, podríamos asignarle un SPN y realizar un ataque Kerberoasting (que se basa en que la cuenta de destino tenga una contraseña débil). Sobre un grupo significa que podríamos agregarnos a nosotros mismos o a otro principal de seguridad a un grupo determinado. Por último, si tenemos este acceso sobre un objeto informático, podríamos realizar un ataque de delegación restringida basado en recursos que está fuera del alcance de este módulo.
* `AddSelf`- muestra los grupos de seguridad a los que un usuario puede agregarse.
* [`GenericAll`](https://bloodhound.readthedocs.io/en/latest/data-analysis/edges.html#genericall) : esto nos otorga control total sobre un objeto de destino. Nuevamente, dependiendo de si esto se otorga sobre un usuario o grupo, podríamos modificar la membresía del grupo, forzar el cambio de una contraseña o realizar un ataque Kerberoasting dirigido. Si tenemos este acceso sobre un objeto de computadora y la [Local Administrator Password Solution (LAPS)](https://www.microsoft.com/en-us/download/details.aspx?id=46899) está en uso en el entorno, podemos leer la contraseña de LAPS y obtener acceso de administrador local a la máquina, lo que puede ayudarnos en el movimiento lateral o la escalada de privilegios en el dominio si podemos obtener controles privilegiados o algún tipo de acceso privilegiado.

Este gráfico, adaptado de un gráfico creado por [Charlie Bromberg (Shutdown)](https://twitter.com/_nwodtuhs) , muestra un excelente desglose de los posibles ataques ACE y las herramientas para realizar estos ataques tanto desde Windows como desde Linux (si corresponde). En las siguientes secciones, cubriremos principalmente la enumeración y realización de estos ataques desde un host de ataque de Windows y mencionaremos cómo se podrían realizar estos ataques desde Linux. En un módulo posterior, específicamente sobre ataques ACL, se profundizará mucho más en cada uno de los ataques enumerados en este gráfico y en cómo realizarlos desde Windows y Linux.

![imagen](https://academy.hackthebox.com/storage/modules/143/ACL_attacks_graphic.png)

De vez en cuando nos encontraremos con muchos otros ACE (privilegios) interesantes en Active Directory. La metodología para enumerar posibles ataques de ACL utilizando herramientas como BloodHound y PowerView e incluso herramientas de administración de AD integradas debería ser lo suficientemente adaptable como para ayudarnos siempre que encontremos nuevos privilegios en la naturaleza con los que aún no estemos familiarizados. Por ejemplo, podemos importar datos a BloodHound y ver que un usuario sobre el que tenemos control (o que potencialmente podemos asumir) tiene los derechos para leer la contraseña de una cuenta de servicio administrada por grupo (gMSA) a través del borde [ReadGMSAPassword](https://bloodhound.readthedocs.io/en/latest/data-analysis/edges.html#readgmsapassword) .&#x20;

En este caso, existen herramientas como [GMSAPasswordReader](https://github.com/rvazarkar/GMSAPasswordReader) que podríamos usar, junto con otros métodos, para obtener la contraseña de la cuenta de servicio en cuestión. Otras veces podemos encontrarnos con derechos extendidos como [Unexpire-Password](https://learn.microsoft.com/en-us/windows/win32/adschema/r-unexpire-password) o [Reanimate-Tombstones](https://learn.microsoft.com/en-us/windows/win32/adschema/r-reanimate-tombstones) utilizando PowerView y tenemos que investigar un poco para descubrir cómo explotarlos para nuestro beneficio. Vale la pena familiarizarse con todas las [aristas de BloodHound](https://bloodhound.readthedocs.io/en/latest/data-analysis/edges.html) y tantos [derechos extendidos](https://learn.microsoft.com/en-us/windows/win32/adschema/extended-rights) de Active Directory como sea posible, ya que nunca se sabe cuándo puede encontrarse con uno menos común durante una evaluación.

***

## <mark style="color:purple;">Ataques de ACL</mark>

Podemos utilizar ataques ACL para:

* `Movimiento lateral`
* `Escalada de privilegios`
* `Persistencia`

Algunos escenarios de ataque comunes pueden incluir:

<table data-header-hidden><thead><tr><th width="234"></th><th></th></tr></thead><tbody><tr><td>Ataque</td><td>Descripción</td></tr><tr><td><code>Abusar de los permisos de contraseña olvidada</code></td><td>A menudo, a los usuarios de Help Desk y de otros departamentos de TI se les conceden permisos para restablecer contraseñas y realizar otras tareas privilegiadas. Si podemos tomar el control de una cuenta con estos privilegios (o una cuenta en un grupo que confiere estos privilegios a sus usuarios), es posible que podamos restablecer la contraseña de una cuenta con más privilegios en el dominio.</td></tr><tr><td><code>Abusar de la gestión de membresía de grupo</code></td><td>También es común ver a Help Desk y a otro personal que tienen el derecho de agregar o eliminar usuarios de un grupo determinado. Siempre vale la pena enumerar esto con más detalle, ya que a veces podemos agregar una cuenta que controlamos a un grupo AD integrado privilegiado o a un grupo que nos otorga algún tipo de privilegio interesante.</td></tr><tr><td><code>Derechos de usuario excesivos</code></td><td>También es habitual ver objetos de usuario, equipo y grupo con derechos excesivos que el cliente probablemente desconozca. Esto puede ocurrir después de algún tipo de instalación de software (Exchange, por ejemplo, agrega muchos cambios de ACL al entorno en el momento de la instalación) o algún tipo de configuración heredada o accidental que le otorga a un usuario derechos no deseados. A veces, podemos tomar el control de una cuenta a la que se le otorgaron ciertos derechos por conveniencia o para resolver un problema persistente más rápidamente.</td></tr></tbody></table>

Existen muchos otros escenarios de ataque posibles en el mundo de las ACL de Active Directory, pero estos tres son los más comunes. Abordaremos la enumeración de estos derechos de diversas maneras, la realización de los ataques y la limpieza de los mismos.

{% hint style="info" %}
**Nota:** Algunos ataques de ACL pueden considerarse "destructivos", como cambiar la contraseña de un usuario o realizar otras modificaciones dentro del dominio de AD de un cliente. En caso de duda, siempre es mejor ejecutar un ataque determinado por parte de nuestro cliente antes de realizarlo para tener documentación escrita de su aprobación en caso de que surja un problema. Siempre debemos documentar cuidadosamente nuestros ataques de principio a fin y revertir cualquier cambio. Estos datos deben incluirse en nuestro informe, pero también debemos resaltar claramente cualquier cambio que realicemos para que el cliente pueda volver atrás y verificar que nuestros cambios se revirtieron correctamente.
{% endhint %}
