
# Técnicas adicionales de auditoría en AD

Además de analizar el fortalecimiento de un dominio de AD, quería analizar la `Auditoría en AD`. Queremos proporcionar a nuestros clientes la mayor cantidad de información posible para ayudarlos a resolver los posibles problemas que encontremos. Al hacerlo, les brindaremos más datos para demostrar que tienen un problema y los ayudaremos a obtener respaldo y financiación para abordar esas soluciones. Las herramientas de esta sección se pueden utilizar para proporcionar diferentes visualizaciones y resultados de datos para este propósito.

***

## <mark style="color:purple;">Active Directory Explorer</mark>

[AD Explorer](https://docs.microsoft.com/en-us/sysinternals/downloads/adexplorer) es parte de Sysinternal Suite y se describe como:

"Un visor y editor avanzado de Active Directory (AD). Puede utilizar AD Explorer para navegar fácilmente por una base de datos de AD, definir ubicaciones favoritas, ver propiedades y atributos de objetos sin abrir cuadros de diálogo, editar permisos, ver el esquema de un objeto y ejecutar búsquedas sofisticadas que puede guardar y volver a ejecutar".

AD Explorer también se puede utilizar para guardar instantáneas de una base de datos de AD para verlas y compararlas sin conexión. Podemos tomar una instantánea de AD en un momento determinado y explorarla más tarde, durante la fase de generación de informes, como lo haríamos con cualquier otra base de datos. También se puede utilizar para realizar una comparación de AD antes y después para descubrir cambios en objetos, atributos y permisos de seguridad.

Cuando cargamos la herramienta por primera vez, se nos solicitan las credenciales de inicio de sesión o cargar una instantánea anterior. Podemos iniciar sesión con cualquier usuario de dominio válido.

#### **Iniciar sesión con AD Explorer**

![imagen](https://academy.hackthebox.com/storage/modules/47/AD_explorer1.png)

Una vez iniciada la sesión, podremos navegar libremente por AD y ver información sobre todos los objetos.

#### **Navegación por AD con AD Explorer**

![imagen](https://academy.hackthebox.com/storage/modules/47/AD_explorer_logged_in.png)

Para tomar una instantánea de AD, vaya a Archivo --> `Create Snapshot` e ingrese un nombre para la instantánea. Una vez que esté completa, podemos moverla fuera de línea para realizar un análisis más detallado.

#### **Creación de un Snapshot de AD con AD Explorer**

![imagen](https://academy.hackthebox.com/storage/modules/47/AD_explorer_snapshot.png)

***

## <mark style="color:purple;">Ping Castle</mark>

[PingCastle](https://www.pingcastle.com/documentation/) es una herramienta poderosa que evalúa la postura de seguridad de un entorno de AD y nos proporciona los resultados en varios mapas y gráficos diferentes. Pensando en la seguridad por un segundo, si no tiene un inventario activo de los hosts en su empresa, PingCastle puede ser un gran recurso para ayudarlo a recopilar uno en un mapa agradable y legible para el usuario del dominio.&#x20;

PingCastle es diferente de herramientas como PowerView y BloodHound porque, además de proporcionarnos datos de enumeración que pueden informar nuestros ataques, también proporciona un informe detallado del nivel de seguridad del dominio de destino utilizando una metodología basada en un marco de madurez/evaluación de riesgos. La puntuación que se muestra en el informe se basa en la [Integración del modelo de madurez de capacidad](https://en.wikipedia.org/wiki/Capability_Maturity_Model_Integration) (CMMI). Para ver rápidamente el contexto de ayuda proporcionado, puedes emitir el modificador `--help` en cmd.

{% hint style="info" %}
**Nota**: Si tienes problemas al iniciar la herramienta, cambia la fecha del sistema a una fecha anterior al 31 de julio de 2023 mediante el Panel de control (Configure la hora y la fecha).
{% endhint %}

#### **Menú de ayuda de PingCastle**

```cmd-session
C:\htb> PingCastle.exe --help

switch:
  --help              : display this message
  --interactive       : force the interactive mode
  --log               : generate a log file
  --log-console       : add log to the console
  --log-samba <option>: enable samba login (example: 10)

Common options when connecting to the AD
  --server <server>   : use this server (default: current domain controller)
                        the special value * or *.forest do the healthcheck for all domains
  --port <port>       : the port to use for ADWS or LDAP (default: 9389 or 389)
  --user <user>       : use this user (default: integrated authentication)
  --password <pass>   : use this password (default: asked on a secure prompt)
  --protocol <proto>  : selection the protocol to use among LDAP or ADWS (fastest)
                      : ADWSThenLDAP (default), ADWSOnly, LDAPOnly, LDAPThenADWS

<SNIP>  
```

#### **Ejecución de PingCastle**

Para ejecutar PingCastle, podemos llamar al ejecutable escribiendo `PingCastle.exe` en nuestra ventana de CMD o PowerShell o haciendo clic en el ejecutable, y nos llevará al modo interactivo, presentándonos un menú de opciones dentro de `Terminal User Interface`( `TUI`).

#### **Interfaz de usuario interactiva PingCastle**

```cmd-session
|:.      PingCastle (Version 2.10.1.0     1/19/2022 8:12:02 AM)
|  #:.   Get Active Directory Security at 80% in 20% of the time
# @@  >  End of support: 7/31/2023
| @@@:
: .#                                 Vincent LE TOUX (contact@pingcastle.com)
  .:       twitter: @mysmartlogon                    https://www.pingcastle.com
What do you want to do?
=======================
Using interactive mode.
Do not forget that there are other command line switches like --help that you can use
  1-healthcheck-Score the risk of a domain
  2-conso      -Aggregate multiple reports into a single one
  3-carto      -Build a map of all interconnected domains
  4-scanner    -Perform specific security checks on workstations
  5-export     -Export users or computers
  6-advanced   -Open the advanced menu
  0-Exit
==============================
This is the main functionnality of PingCastle. In a matter of minutes, it produces a report which will give you an overview of your Active Directory security. This report can be generated on other domains by using the existing trust links.
```

La opción predeterminada es la de ejecución `healthcheck`, que establecerá una visión general de referencia del dominio y nos proporcionará información pertinente sobre configuraciones erróneas y vulnerabilidades. Mejor aún, PingCastle puede informar sobre la susceptibilidad reciente a vulnerabilidades, nuestros recursos compartidos, confianzas, la delegación de permisos y mucho más sobre nuestros usuarios y estados de la computadora. En la opción Scanner, podemos encontrar la mayoría de estas comprobaciones.

#### **Opciones del escáner**

```cmd-session
|:.      PingCastle (Version 2.10.1.0     1/19/2022 8:12:02 AM)
|  #:.   Get Active Directory Security at 80% in 20% of the time
# @@  >  End of support: 7/31/2023
| @@@:
: .#                                 Vincent LE TOUX (contact@pingcastle.com)
  .:       twitter: @mysmartlogon                    https://www.pingcastle.com
Select a scanner
================
What scanner whould you like to run ?
WARNING: Checking a lot of workstations may raise security alerts.
  1-aclcheck                                                  9-oxidbindings
  2-antivirus                                                 a-remote
  3-computerversion                                           b-share
  4-foreignusers                                              c-smb
  5-laps_bitlocker                                            d-smb3querynetwork
  6-localadmin                                                e-spooler
  7-nullsession                                               f-startup
  8-nullsession-trust                                         g-zerologon
  0-Exit
==============================
Check authorization related to users or groups. Default to everyone, authenticated users and domain users
```

Ahora que entendemos cómo funciona y cómo iniciar los escaneos, veamos el informe.

#### **Visualización del informe**

A lo largo del informe, hay secciones como información sobre dominio, usuario, grupo y confianza, y una tabla específica que señala "anomalías" o problemas que pueden requerir atención inmediata. También se nos presentará la puntuación de riesgo general del dominio.

![texto](https://academy.hackthebox.com/storage/modules/143/report-example.png)

Además de ser útil para realizar una enumeración de dominios muy exhaustiva cuando se combina con otras herramientas, PingCastle puede ser útil para brindarles a los clientes un análisis rápido de la situación de seguridad de su dominio, o puede ser utilizado por equipos internos para autoevaluarse y encontrar áreas de preocupación u oportunidades para un mayor fortalecimiento. Tómese un tiempo para explorar los informes y mapas que PingCastle puede generar en el dominio de Inlanefreight.

#### **Política de grupo**

Dado que la política de grupo es una parte importante de cómo se administran los usuarios y las computadoras de AD, es lógico que queramos auditar sus configuraciones y resaltar cualquier agujero potencial. `Group3r`es una herramienta excelente para esto.

***

## <mark style="color:purple;">Group3r</mark>

[Group3r](https://github.com/Group3r/Group3r) es una herramienta diseñada específicamente para encontrar vulnerabilidades en la directiva de grupo asociada a Active Directory. Group3r debe ejecutarse desde un host unido a un dominio con un usuario de dominio (no es necesario que sea un administrador) o en el contexto de un usuario de dominio (es decir, utilizando `runas /netonly`).

#### **Uso básico de Group3r**

```bash
C:\htb> group3r.exe -f <filepath-name.log> 
```

Al ejecutar Group3r, debemos especificar el indicador indicador `-s` o `-f`. Estos indicadores especificarán si se deben enviar los resultados a la salida estándar (`-s`) o al archivo al que queremos enviar los resultados (`-f`). Para obtener más opciones e información de uso, utilice el indicador `-h` o consulte la información de uso en el enlace anterior.

#### **Salida de lectura**

![texto](https://academy.hackthebox.com/storage/modules/143/grouper-output.png)

Al leer la salida de Group3r, cada sangría es un nivel diferente, por lo que ninguna sangría será la GPO, una sangría será la configuración de la política y otra serán los hallazgos en esas configuraciones. A continuación, veremos la salida que se muestra a partir de un hallazgo.

#### **Hallazgo de group3r**

![texto](https://academy.hackthebox.com/storage/modules/143/grouper-finding.png)

En la imagen de arriba, verá un ejemplo de un hallazgo de Group3r. Lo presentará como un cuadro vinculado a la configuración de la política, definirá la parte interesante y nos dará una razón para el hallazgo. Vale la pena el esfuerzo de ejecutar Group3r si tiene la oportunidad. A menudo encontrará rutas u objetos interesantes que otras herramientas pasarían por alto.

***

## <mark style="color:purple;">AD Recon</mark>

Por último, existen otras herramientas que resultan útiles para recopilar una gran cantidad de datos de AD a la vez. En una evaluación en la que no se requiere sigilo, también vale la pena ejecutar una herramienta como [ADRecon](https://github.com/adrecon/ADRecon) y analizar los resultados, por si acaso nuestra enumeración no nos ha permitido ver algo menor que pueda resultarnos útil o que valga la pena señalarle a nuestro cliente.

#### **Ejecutando ADRecon**

```powershell
PS C:\htb> .\ADRecon.ps1

[*] ADRecon v1.1 by Prashant Mahajan (@prashant3535)
[*] Running on INLANEFREIGHT.LOCAL\MS01 - Member Server
[*] Commencing - 03/28/2022 09:24:58
[-] Domain
[-] Forest
[-] Trusts
[-] Sites
[-] Subnets
[-] SchemaHistory - May take some time
[-] Default Password Policy
[-] Fine Grained Password Policy - May need a Privileged Account
[-] Domain Controllers
[-] Users and SPNs - May take some time
[-] PasswordAttributes - Experimental
[-] Groups and Membership Changes - May take some time
[-] Group Memberships - May take some time
[-] OrganizationalUnits (OUs)
[-] GPOs
[-] gPLinks - Scope of Management (SOM)
[-] DNS Zones and Records
[-] Printers
[-] Computers and SPNs - May take some time
[-] LAPS - Needs Privileged Account
[-] BitLocker Recovery Keys - Needs Privileged Account
[-] GPOReport - May take some time
[*] Total Execution Time (mins): 11.05
[*] Output Directory: C:\Tools\ADRecon-Report-20220328092458
```

Una vez hecho esto, ADRecon nos dejará un informe en una nueva carpeta dentro del directorio desde el que ejecutamos el programa. Podemos ver un ejemplo de los resultados en la terminal a continuación. Obtendrá un informe en formato HTML y una carpeta con resultados CSV. Al generar el informe, debe tenerse en cuenta que el programa Excel debe estar instalado, o el script no generará automáticamente el informe de esa manera; solo lo dejará con los archivos .csv. Si desea obtener un resultado para la Política de grupo, debe asegurarse de que el host desde el que ejecuta tenga instalado el módulo PowerShell `GroupPolicy`. Podemos volver más tarde y generar el informe de Excel desde otro host utilizando la flag `-GenExcel` y alimentando la carpeta de informes.

#### **Informes**

```powershell
PS C:\htb> ls

    Directory: C:\Tools\ADRecon-Report-20220328092458

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         3/28/2022  12:42 PM                CSV-Files
-a----         3/28/2022  12:42 PM        2758736 GPO-Report.html
-a----         3/28/2022  12:42 PM         392780 GPO-Report.xml
```

***

Hemos cubierto muchas herramientas y tácticas en este módulo, pero consideramos que sería prudente mostrar y explicar algunas otras formas de auditar un dominio de destino. Tenga en cuenta que sus acciones deben tener un propósito y nuestro objetivo final es mejorar la postura de seguridad del cliente. Por lo tanto, con eso en mente, obtener más evidencia de los problemas solo servirá para:

`Hacer que nuestros informes sean más convincentes y brindar al cliente las herramientas que necesita para arreglar y proteger activamente su dominio.`
