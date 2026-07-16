
# Relaciones de confianza

Muchas organizaciones grandes adquieren nuevas empresas con el tiempo y las incorporan a su red. Una forma de hacerlo para facilitar su uso es establecer una relación de confianza con el nuevo dominio. De esta manera, puede evitar migrar todos los objetos establecidos, lo que hace que la integración sea mucho más rápida. Esta confianza también puede introducir debilidades en el entorno del cliente si no tiene cuidado. Un subdominio con una falla o vulnerabilidad explotable puede proporcionarnos una ruta rápida hacia el dominio de destino.&#x20;

Las empresas también pueden establecer confianzas con otras empresas (como un MSP), un cliente u otras unidades comerciales de la misma empresa (como una división de la empresa en otra región geográfica). Exploremos más las confianzas de dominio y cómo podemos abusar de la funcionalidad incorporada durante nuestras evaluaciones.

***

## La confianza de dominio

Una [confianza](https://social.technet.microsoft.com/wiki/contents/articles/50969.active-directory-forest-trust-attention-points.aspx) se utiliza para establecer una autenticación de bosque a bosque o de dominio a dominio (dentro de un dominio), que permite a los usuarios acceder a recursos de otro dominio (o realizar tareas administrativas) fuera del dominio principal donde reside su cuenta. Una confianza crea un vínculo entre los sistemas de autenticación de dos dominios y puede permitir una comunicación unidireccional o bidireccional.&#x20;

Una organización puede crear varios tipos de confianzas:

* `Parent-child`: Dos o más dominios dentro del mismo bosque. El dominio secundario tiene una confianza transitiva bidireccional con el dominio principal, lo que significa que los usuarios del dominio secundario `corp.inlanefreight.local` pueden autenticarse en el dominio principal `inlanefreight.local` y viceversa.
* `Cross-link`: Una confianza entre dominios secundarios para acelerar la autenticación.
* `External`: Una confianza no transitiva entre dos dominios separados en bosques separados que no están unidos por una confianza de bosque. Este tipo de confianza utiliza [el filtrado de SID](https://www.serverbrain.org/active-directory-2008/sid-history-and-sid-filtering.html) o filtra las solicitudes de autenticación (por SID) que no provienen del dominio de confianza.
* `Tree-root`: Una confianza transitiva bidireccional entre un dominio raíz de bosque y un nuevo dominio raíz de árbol. Se crean por diseño cuando se configura un nuevo dominio raíz de árbol dentro de un bosque.
* `Forest`: Una confianza transitiva entre dos dominios raíz del bosque.
* [ESAE](https://docs.microsoft.com/en-us/security/compass/esae-retirement) : Un bosque bastión utilizado para administrar Active Directory.

Al establecer una confianza, ciertos elementos pueden modificarse dependiendo del caso de negocio.

La confianza puede ser transitiva o no transitiva.

* Una confianza `transitiva` significa que la confianza se extiende a los objetos en los que confía el dominio secundario. Por ejemplo, supongamos que tenemos tres dominios. En una relación transitiva, si el `Dominio A` tiene una confianza con el `Dominio B`, y `Dominio B` tiene una confianza `transitiva` con `Dominio C`, entonces el `Dominio A` confiará automáticamente en `Domain C`.
* En una confianza `no transitiva`, el dominio secundario es el único en el que se confía.

![imagen](https://academy.hackthebox.com/storage/modules/143/transitive-trusts.png)

**Tabla de confianza**

| `Transitivo`                                                                        | `No transitivo`                                                    |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Compartido, 1 a muchos                                                              | Confianza directa                                                  |
| La confianza se comparte con cualquier persona en el bosque                         | No se extiende a los dominios secundarios del siguiente nivel      |
| La confianza de bosque, árbol-raíz, padre-hijo y de vínculo cruzado son transitivos | Típico para configuraciones de confianza externas o personalizadas |

Una comparación fácil de hacer es la entrega de un paquete a su domicilio. En el caso de una confianza `transitiva`, tu has otorgado permiso a cualquier persona de tu hogar (bosque) para que acepte un paquete en su nombre. En el caso de una confianza `no transitiva`, tu has dado órdenes estrictas con el paquete de que nadie más que el servicio de entrega y usted puede manipularlo, y solo usted puede firmar por él.

Las relaciones de confianza se pueden establecer en dos direcciones:

* `Unidireccionales`: Los usuarios de un dominio pueden acceder a los recursos de un dominio de confianza, no al revés.
* `Bidireccionales`: Los usuarios de ambos dominios de confianza pueden acceder a los recursos del otro dominio. Por ejemplo, en una confianza bidireccional entre `INLANEFREIGHT.LOCAL` y `FREIGHTLOGISTICS.LOCAL`, los usuarios de `INLANEFREIGHT.LOCAL` podrían acceder a los recursos de `FREIGHTLOGISTICS.LOCAL` y viceversa.

Las relaciones de confianza de dominio suelen configurarse de forma incorrecta y pueden proporcionarnos rutas de ataque críticas no deseadas. Además, las confianzas configurados para facilitar su uso pueden no revisarse más adelante para detectar posibles implicaciones de seguridad si no se tiene en cuenta la seguridad antes de establecer la relación de confianza. Una fusión y adquisición (M\&A) entre dos empresas puede dar lugar a confianzas bidireccionales con las empresas adquiridas, lo que puede introducir sin saberlo un riesgo en el entorno de la empresa adquirente si la postura de seguridad de la empresa adquirida es desconocida y no se ha probado.&#x20;

Si alguien quisiera atacar a su organización, también podría buscar en la otra empresa que adquirió un objetivo potencialmente más fácil de atacar, lo que le permitiría entrar en su organización de forma indirecta. No es raro poder realizar un ataque como Kerberoasting contra un dominio fuera del dominio principal y obtener un usuario que tenga acceso administrativo dentro del dominio principal. He realizado muchas pruebas de penetración en las que este era el caso: no pude encontrar un punto de apoyo en el dominio principal, pero pude encontrar una falla en un dominio de confianza que, a su vez, me dio un punto de apoyo, o incluso derechos de administrador completos en el dominio principal. Este tipo de ataque "end-around" se podría prevenir si se considera la seguridad como una cuestión primordial antes de establecer cualquier tipo de confianza en el dominio.&#x20;

A medida que examinamos las relaciones de confianza, ten en cuenta estas ideas para los informes. A menudo, descubriremos que la organización más grande no sabe que existe una relación de confianza con uno o más dominios.

## <mark style="color:purple;">Tipos de confianza</mark>

A continuación se muestra una representación gráfica de los distintos tipos de confianza.

![imagen](https://academy.hackthebox.com/storage/modules/143/trusts-diagram.png)

***

## <mark style="color:purple;">Enumeración de relaciones de confianza</mark>

Podemos utilizar el cmdlet [Get-ADTrust](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-adtrust?view=windowsserver2022-ps) para enumerar las relaciones de confianza de dominio. Esto resulta especialmente útil si estamos limitados a utilizar únicamente herramientas integradas.

### **Uso de Get-ADTrust**

```powershell
PS C:\htb> Import-Module activedirectory
PS C:\htb> Get-ADTrust -Filter *

Direction               : BiDirectional
DisallowTransivity      : False
DistinguishedName       : CN=LOGISTICS.INLANEFREIGHT.LOCAL,CN=System,DC=INLANEFREIGHT,DC=LOCAL
ForestTransitive        : False
IntraForest             : True
IsTreeParent            : False
IsTreeRoot              : False
Name                    : LOGISTICS.INLANEFREIGHT.LOCAL
ObjectClass             : trustedDomain
ObjectGUID              : f48a1169-2e58-42c1-ba32-a6ccb10057ec
SelectiveAuthentication : False
SIDFilteringForestAware : False
SIDFilteringQuarantined : False
Source                  : DC=INLANEFREIGHT,DC=LOCAL
Target                  : LOGISTICS.INLANEFREIGHT.LOCAL
TGTDelegation           : False
TrustAttributes         : 32
TrustedPolicy           :
TrustingPolicy          :
TrustType               : Uplevel
UplevelOnly             : False
UsesAESKeys             : False
UsesRC4Encryption       : False

Direction               : BiDirectional
DisallowTransivity      : False
DistinguishedName       : CN=FREIGHTLOGISTICS.LOCAL,CN=System,DC=INLANEFREIGHT,DC=LOCAL
ForestTransitive        : True
IntraForest             : False
IsTreeParent            : False
IsTreeRoot              : False
Name                    : FREIGHTLOGISTICS.LOCAL
ObjectClass             : trustedDomain
ObjectGUID              : 1597717f-89b7-49b8-9cd9-0801d52475ca
SelectiveAuthentication : False
SIDFilteringForestAware : False
SIDFilteringQuarantined : False
Source                  : DC=INLANEFREIGHT,DC=LOCAL
Target                  : FREIGHTLOGISTICS.LOCAL
TGTDelegation           : False
TrustAttributes         : 8
TrustedPolicy           :
TrustingPolicy          :
TrustType               : Uplevel
UplevelOnly             : False
UsesAESKeys             : False
UsesRC4Encryption       : False
```

El resultado anterior muestra que nuestro dominio actual `INLANEFREIGHT.LOCAL` tiene dos confianzas de dominio. La primera es con `LOGISTICS.INLANEFREIGHT.LOCAL`, y la propiedad `IntraForest` muestra que se trata de un dominio secundario, y actualmente estamos ubicados en el dominio raíz del bosque. La segunda confianza es con el dominio `FREIGHTLOGISTICS.LOCAL,`y la propiedad `ForestTransitive` está establecida en `True`, lo que significa que se trata de una confianza de bosque o una confianza externa.&#x20;

Podemos ver que ambas confianzas están configuradas para ser `bidireccionales`, lo que significa que los usuarios pueden autenticarse en ambas confianzas. Es importante tener esto en cuenta durante una evaluación. Si no podemos autenticarnos en una confianza, no podemos realizar ninguna enumeración ni ataques en la confianza.

Además de utilizar herramientas de AD integradas, como el módulo PowerShell de Active Directory, tanto PowerView como BloodHound se pueden utilizar para enumerar relaciones de confianza, el tipo de confianzas establecidas y el flujo de autenticación. Después de importar PowerView, podemos utilizar la función [Get-DomainTrust](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainTrust/) para enumerar qué confianzas existen, si las hay.

### **PowerView - Get-DomainTrust**

```powershell
PS C:\htb> Get-DomainTrust 

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : LOGISTICS.INLANEFREIGHT.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : WITHIN_FOREST
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 6:20:22 PM
WhenChanged     : 2/26/2022 11:55:55 PM

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : FREIGHTLOGISTICS.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : FOREST_TRANSITIVE
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 8:07:09 PM
WhenChanged     : 2/27/2022 12:02:39 AM
```

PowerView se puede utilizar para realizar un mapeo de confianza de dominio y brindar información como el tipo de confianza (principal/secundaria, externa, de bosque) y la dirección de la confianza (unidireccional o bidireccional). Esta información es útil una vez que se obtiene un punto de apoyo y planeamos comprometer aún más el entorno.

### **PowerView - Get-DomainTrustMapping**

```powershell
PS C:\htb> Get-DomainTrustMapping

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : LOGISTICS.INLANEFREIGHT.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : WITHIN_FOREST
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 6:20:22 PM
WhenChanged     : 2/26/2022 11:55:55 PM

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : FREIGHTLOGISTICS.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : FOREST_TRANSITIVE
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 8:07:09 PM
WhenChanged     : 2/27/2022 12:02:39 AM

SourceName      : FREIGHTLOGISTICS.LOCAL
TargetName      : INLANEFREIGHT.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : FOREST_TRANSITIVE
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 8:07:08 PM
WhenChanged     : 2/27/2022 12:02:41 AM

SourceName      : LOGISTICS.INLANEFREIGHT.LOCAL
TargetName      : INLANEFREIGHT.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : WITHIN_FOREST
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 6:20:22 PM
WhenChanged     : 2/26/2022 11:55:55 PM
```

Desde aquí, podríamos comenzar a realizar la enumeración en todas las confianzas. Por ejemplo, podríamos observar todos los usuarios del dominio secundario:

### **Enumerar usuarios en el dominio secundario con Get-DomainUser**

```powershell
PS C:\htb> Get-DomainUser -Domain LOGISTICS.INLANEFREIGHT.LOCAL | select SamAccountName

samaccountname
--------------
htb-student_adm
Administrator
Guest
lab_adm
krbtgt
```

Otra herramienta que podemos utilizar para obtener la confianza del dominio es `netdom`. El subcomando `netdom query` de la herramienta de línea de comandos `netdom` de Windows puede recuperar información sobre el dominio, incluida una lista de estaciones de trabajo, servidores y confianzas de dominio.

### **netdom - Consultar la confianza del dominio**

```powershell
C:\htb> netdom query /domain:inlanefreight.local trust
Direction Trusted\Trusting domain                         Trust type
========= =======================                         ==========

<->       LOGISTICS.INLANEFREIGHT.LOCAL
Direct
 Not found

<->       FREIGHTLOGISTICS.LOCAL
Direct
 Not found

The command completed successfully.
```

### **netdom - Consultar controladores de dominio**

```powershell
C:\htb> netdom query /domain:inlanefreight.local dc
List of domain controllers with accounts in the domain:

ACADEMY-EA-DC01
The command completed successfully.
```

### **netdom - Consultar estaciones de trabajo y servidores**

```shell-session
C:\htb> netdom query /domain:inlanefreight.local workstation
List of workstations with accounts in the domain:

ACADEMY-EA-MS01
ACADEMY-EA-MX01      ( Workstation or Server )

SQL01      ( Workstation or Server )
ILF-XRG      ( Workstation or Server )
MAINLON      ( Workstation or Server )
CISERVER      ( Workstation or Server )
INDEX-DEV-LON      ( Workstation or Server )
...SNIP...
```

También podemos utilizar BloodHound para visualizar estas relaciones de confianza mediante la consulta predefinida `Map Domain Trusts`. Aquí podemos ver fácilmente que existen dos relaciones de confianza bidireccionales.

### **BloodHound - Relaciones de confianza**

![imagen](https://academy.hackthebox.com/storage/modules/143/BH_trusts.png)

***

## <mark style="color:purple;">Caso práctico</mark>

### Pregunta 1

¿Cuál es el dominio secundario de `INLANEFREIGHT.LOCAL`? (formato: FQDN, es decir, DEV.ACME.LOCAL)

```powershell
PS C:\Tools> Import-Module .\PowerView.ps1
PS C:\Tools> Get-DomainTrust

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : LOGISTICS.INLANEFREIGHT.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : WITHIN_FOREST
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 6:20:22 PM
WhenChanged     : 3/29/2022 5:14:31 PM

SourceName      : INLANEFREIGHT.LOCAL
TargetName      : FREIGHTLOGISTICS.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : FOREST_TRANSITIVE
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 8:07:09 PM
WhenChanged     : 3/29/2022 4:48:04 PM
```

El dominio secundario es `LOGISTICS.INLANEFREIGHT.LOCAL`

### Pregunta 2

¿Con qué dominio tiene el dominio INLANEFREIGHT.LOCAL una confianza transitiva de bosque? ¿Hacia dónde va esta confianza?

```
SourceName      : INLANEFREIGHT.LOCAL
TargetName      : FREIGHTLOGISTICS.LOCAL
TrustType       : WINDOWS_ACTIVE_DIRECTORY
TrustAttributes : FOREST_TRANSITIVE
TrustDirection  : Bidirectional
WhenCreated     : 11/1/2021 8:07:09 PM
WhenChanged     : 3/29/2022 4:48:04 PM
```

Aquí observamos que tiene una confianza transitiva con FREIGHTLOGISTICS.LOCAL, que a su vez es bidireccional.

***

## <mark style="color:purple;">Hacia delante</mark>

En las siguientes secciones, abordaremos los ataques comunes que podemos realizar contra confianzas de dominios secundarios --> principales y entre confianzas de bosques bidireccionales. Estos tipos de ataques no deben pasarse por alto, pero siempre debemos consultar con nuestro cliente para asegurarnos de que cualquier confianza que descubramos durante nuestra enumeración esté dentro del alcance de la evaluación y no estemos fuera de las Reglas de interacción.
