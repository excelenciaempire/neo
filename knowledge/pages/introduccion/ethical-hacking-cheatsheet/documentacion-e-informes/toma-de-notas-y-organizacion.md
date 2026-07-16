
# Toma de notas y organización

mar notas exhaustivamente es fundamental durante cualquier evaluación. Nuestras notas, junto con los resultados de las herramientas y los registros, constituyen la base de nuestro borrador del informe, que suele ser la única parte de la evaluación que nuestro cliente ve. Aunque normalmente guardamos nuestras notas, debemos mantener la organización y desarrollar un proceso repetible para ahorrar tiempo y facilitar el proceso de elaboración de informes. Las notas detalladas también son imprescindibles en caso de un problema de red o una pregunta del cliente (por ejemplo, ¿escaneó el host X el día Y?), por lo que ser demasiado detallado al tomar notas nunca está de más.&#x20;

Cada persona tendrá su propio estilo con el que se sienta cómoda y deberá trabajar con sus herramientas y estructura organizativa preferidas para garantizar los mejores resultados posibles. En este módulo, abordaremos los elementos mínimos que, según nuestra experiencia profesional, deben anotarse durante una evaluación (o incluso al trabajar en un módulo extenso, hackear una máquina vulnerable en HTB o realizar un examen) para ahorrar tiempo y energía a la hora de presentar informes o como guía de referencia más adelante. Si forma parte de un equipo más grande en el que alguien puede tener que cubrir una reunión con un cliente por usted, es fundamental tomar notas claras y coherentes para garantizar que su compañero de equipo pueda hablar con confianza y precisión sobre qué actividades se realizaron y qué no.

***

## <mark style="color:purple;">Estructura de muestra para tomar notas</mark>

No existe una solución ni una estructura universal para la toma de notas, ya que cada proyecto y pentester es diferente. La estructura que se presenta a continuación es la que consideramos útil, pero debe adaptarse a su flujo de trabajo, tipo de proyecto y circunstancias específicas que haya experimentado durante el mismo. Por ejemplo, algunas de estas categorías podrían no ser aplicables a una evaluación centrada en la aplicación e incluso podrían justificar categorías adicionales no incluidas aquí.

* <mark style="color:purple;">`Ruta de Ataque`</mark> -  Un esquema de la ruta completa si se establece una conexión durante una prueba de penetración externa o se compromete uno o más hosts (o el dominio de AD) durante una prueba de penetración interna. Delinear la ruta con la mayor precisión posible mediante capturas de pantalla y la salida del comando facilitará su posterior inserción en el informe y solo tendrá que preocuparse por el formato.
* <mark style="color:purple;">`Credenciales`</mark> - Un lugar centralizado para mantener sus credenciales y secretos comprometidos a medida que avanza.
* <mark style="color:purple;">`Hallazgos`</mark> - Recomendamos crear una subcarpeta para cada hallazgo y luego escribir nuestra narrativa y guardarla en ella junto con cualquier evidencia (capturas de pantalla, resultados de comandos). También conviene tener una sección en su herramienta de notas para registrar la información de los hallazgos y organizarla para el informe.
* <mark style="color:purple;">`Vulnerability Scan Research`</mark> - Una sección para tomar notas sobre las cosas que has investigado y probado con tus análisis de vulnerabilidad (para que no termines rehaciendo el trabajo que ya hiciste).
* <mark style="color:purple;">`Service Enumeration Research`</mark>- Una sección para tomar notas sobre qué servicios has investigado, intentos fallidos de explotación, vulnerabilidades/configuraciones incorrectas prometedoras, etc.
* <mark style="color:purple;">`Web Application Research`</mark> - Una sección para anotar las aplicaciones web interesantes encontradas mediante diversos métodos, como la fuerza bruta de subdominios. Siempre es recomendable realizar una enumeración exhaustiva de subdominios externamente, buscar puertos web comunes en evaluaciones internas y ejecutar una herramienta como Aquatone o EyeWitness para capturar todas las aplicaciones. Al revisar el informe de capturas de pantalla, anote las aplicaciones de interés, los pares de credenciales comunes/predeterminadas que probó, etc.
* <mark style="color:purple;">`AD Enumeration Research`</mark>- Una sección para mostrar, paso a paso, la enumeración de Active Directory que ya ha realizado. Anote cualquier área de interés que necesite revisar más adelante en la evaluación.
* <mark style="color:purple;">`OSINT`</mark>- Una sección para realizar un seguimiento de la información interesante que ha recopilado a través de OSINT, si corresponde al compromiso.
* <mark style="color:purple;">`Administrative Information`</mark> - A algunas personas les puede resultar útil tener una ubicación centralizada para almacenar la información de contacto de otras partes interesadas del proyecto, como los gerentes de proyecto (GP) o los puntos de contacto del cliente (POC), los objetivos/indicadores únicos definidos en las reglas de participación (RdP) y otros elementos que se consultan con frecuencia durante el proyecto. También puede usarse como una lista de tareas pendientes. A medida que surjan ideas para las pruebas que necesite realizar o que desee probar pero no tenga tiempo, anótelas aquí para poder retomarlas más adelante.
* <mark style="color:purple;">`Scoping Information`</mark> - Aquí podemos almacenar información sobre direcciones IP/rangos CIDR dentro del alcance, URL de aplicaciones web y cualquier credencial para aplicaciones web, VPN o AD proporcionada por el cliente. También podría incluir cualquier otra información relevante al alcance de la evaluación para evitar tener que reabrir constantemente la información y asegurarnos de no desviarnos del alcance de la evaluación.
* <mark style="color:purple;">`Activity Log`</mark> - Seguimiento de alto nivel de todo lo que hizo durante la evaluación para una posible correlación de eventos.
* <mark style="color:purple;">`Payload Log`</mark> - Al igual que con el registro de actividad, es fundamental rastrear las cargas útiles que se utilizan (y el hash de archivo de todo lo cargado y su ubicación) en un entorno de cliente. Más información al respecto más adelante.

***

## <mark style="color:purple;">Herramientas para tomar notas</mark>

Hay muchas herramientas disponibles para tomar notas, y la elección es muy personal. Estas son algunas de las opciones disponibles:

|                                                       |                                                      |                                              |
| ----------------------------------------------------- | ---------------------------------------------------- | -------------------------------------------- |
| [CherryTree](https://www.giuspen.com/cherrytree/)     | [Visual Studio Code](https://code.visualstudio.com/) | [Evernote](https://evernote.com/)            |
| [Notion](https://www.notion.so/)                      | [GitBook](https://www.gitbook.com/)                  | [Sublime Text](https://www.sublimetext.com/) |
| [Notepad++](https://notepad-plus-plus.org/downloads/) | [OneNote](https://www.onenote.com/?public=1)         | [Outline](https://www.getoutline.com/)       |
| [Obsidian](https://obsidian.md/)                      | [Cryptpad](https://cryptpad.fr/)                     | [Standard Notes](https://standardnotes.com/) |

Como equipo, hemos debatido mucho sobre las ventajas y desventajas de las distintas herramientas para tomar notas. Un factor clave es distinguir entre soluciones locales y en la nube antes de elegir una. Una solución en la nube probablemente sea adecuada para cursos de formación, CTFs, laboratorios, etc., pero una vez que nos involucramos en los proyectos y en la gestión de datos de los clientes, debemos ser más cuidadosos con la solución que elegimos. Es probable que su empresa tenga algún tipo de política u obligaciones contractuales en torno al almacenamiento de datos, por lo que es recomendable consultar con su gerente o jefe de equipo si está permitido o no usar una herramienta específica para tomar notas. `Obsidian` es una excelente solución para el almacenamiento local y `Outline` es ideal para la nube, pero también cuenta con una [versión alojada en el propio equipo](https://github.com/outline/outline) . Ambas herramientas se pueden exportar a Markdown e importar a cualquier otra herramienta que acepte este práctico formato.

### **Obsidian**

<figure><img src="/files/erydo0qbgwdNqzjB7X7k" alt=""><figcaption></figcaption></figure>

Nuevamente, las herramientas dependen de las preferencias personales de cada persona. Los requisitos suelen variar según la empresa, así que experimente con diferentes opciones y encuentre una con la que se sienta cómodo. Practique con diferentes configuraciones y formatos mientras trabaja con los módulos de la Academia, las cajas HTB, los Laboratorios Pro y otras capacitaciones para familiarizarse con su estilo de toma de notas, siendo lo más exhaustivo posible.

***

## <mark style="color:purple;">Logging</mark>

Es fundamental registrar todos los intentos de escaneo y ataque, y conservar los resultados de la herramienta sin procesar siempre que sea posible. Esto nos será de gran ayuda a la hora de presentar informes. Si bien nuestras notas deben ser claras y completas, es posible que se nos escape algo, y tener nuestros registros como respaldo puede sernos útil al añadir más evidencia a un informe o responder a la pregunta de un cliente.

### **Intentos de explotación**

[Tmux logging](https://github.com/tmux-plugins/tmux-logging) es una excelente opción para el registro de terminales, y sin duda deberíamos usarlo en `Tmux` junto con el registro, ya que esto guardará todo lo que escribamos en un panel de Tmux en un archivo de registro. También es esencial registrar los intentos de explotación en caso de que el cliente necesite correlacionar eventos posteriormente (o en una situación donde haya muy pocos hallazgos y tenga dudas sobre el trabajo realizado). Es sumamente vergonzoso no poder proporcionar esta información, y puede dar la impresión de ser un pentester inexperto y poco profesional. También es recomendable registrar las pruebas que se probaron durante la evaluación y que no funcionaron. Esto es especialmente útil en aquellos casos en los que el informe contiene pocos o ningún hallazgo. En este caso, podemos redactar una descripción de los tipos de pruebas realizadas, para que el lector comprenda contra qué tipo de amenazas está adecuadamente protegido. Podemos configurar el registro de Tmux en nuestro sistema de la siguiente manera:

Primero, clone el repositorio [de Tmux Plugin Manager](https://github.com/tmux-plugins/tpm) en nuestro directorio de inicio (en nuestro caso `/home/htb-student`o simplemente `~`).

```shell-session
afsh4ck@kali$ git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

A continuación, cree un archivo `.tmux.conf` en el directorio de inicio.

```shell-session
afsh4ck@kali$ touch .tmux.conf
```

El archivo de configuración debe tener el siguiente contenido:

```bash
afsh4ck@kali$ cat .tmux.conf 

# List of plugins

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-logging'

# Initialize TMUX plugin manager (keep at bottom)
run '~/.tmux/plugins/tpm/tpm'
```

Tras crear este archivo de configuración, debemos ejecutarlo en nuestra sesión actual para que la configuración del archivo `.tmux.conf` surta efecto. Podemos hacerlo con el comando [source .](https://www.geeksforgeeks.org/source-command-in-linux-with-examples/)

```shell-session
afsh4ck@kali$ tmux source ~/.tmux.conf 
```

A continuación, podemos iniciar una nueva sesión de Tmux (es decir, `tmux new -s setup`).

Una vez en la sesión, escriba `[Ctrl] + [B]`y luego presione `[Shift] + [I]`(o `prefix`+ `[Shift] + [I]` si no está usando la tecla de prefijo predeterminada), y el complemento se instalará (esto podría demorar alrededor de 5 segundos en completarse).

Una vez instalado el complemento, inicie el registro de la sesión actual (o panel) escribiendo " + " `[Ctrl] + [B]` seguido de `[Shift] + [P]`" + ". Si todo ha ido según lo previsto, la parte inferior de la ventana mostrará que el registro está habilitado y el archivo de salida. Para detener el registro, repita la combinación de teclas "+ " o escriba "+" para cerrar la sesión. Tenga en cuenta que el archivo de registro solo se completará al detener el registro o al salir de la sesión de Tmux con `prefix[Shift] + [P]prefix[Shift] + [P]exit`

Una vez finalizado el registro, podrá encontrar todos los comandos y la salida en el archivo de registro asociado. Vea la demostración a continuación para obtener una breve visualización sobre cómo iniciar y detener el registro de Tmux y ver los resultados.

Si olvidamos habilitar el registro de Tmux y estamos inmersos en un proyecto, podemos realizar un registro retroactivo escribiendo `[Ctrl] + [B]`y pulsando `[Alt] + [Shift] + [P]`( `prefix`+ `[Alt] + [Shift] + [P]`), y se guardará todo el panel. La cantidad de datos guardados depende del Tmux `history-limit` o del número de líneas guardadas en el búfer de retroceso de Tmux. Si se deja con el valor predeterminado e intentamos realizar un registro retroactivo, es muy probable que perdamos datos de etapas anteriores de la evaluación. Para evitar esta situación, podemos añadir las siguientes líneas al archivo `.tmux.conf` (ajustando el número de líneas a nuestro gusto):

#### **Tmux.conf**

```shell-session
set -g history-limit 50000
```

Otro truco útil es la posibilidad de tomar una captura de pantalla de la ventana actual de Tmux o de un panel individual. Supongamos que trabajamos con una ventana dividida (dos paneles), uno con `Responder` y otro con `ntlmrelayx.py`. Si intentamos copiar y pegar la salida de un panel, obtendremos datos del otro panel, lo que se verá muy desordenado y requerirá limpieza. Podemos evitar esto tomando una captura de pantalla como sigue: `[Ctrl] + [B]` seguido de `[Alt] + [P]`( `prefix`+ `[Alt] + [P]`). Veamos una demostración rápida.

Aquí vemos que trabajamos con dos paneles. Si intentamos copiar texto de un panel, tomaremos el texto del otro, lo que generaría un error en la salida. Sin embargo, con el registro de Tmux habilitado, podemos tomar una captura del panel y exportarla correctamente a un archivo.

<figure><img src="/files/lhawWwaRoK5qdEJo9aWN" alt=""><figcaption></figcaption></figure>

Para recrear el ejemplo anterior, inicie una nueva sesión de tmux: `tmux new -s sessionname`. Una vez dentro de la sesión, escriba `[Ctrl] + [B]`+ `[Shift] + [%]`( `prefix`+ `[Shift] + [%]`) para dividir los paneles verticalmente (reemplace `[%]`con `["]`para dividirlos horizontalmente). A continuación, podemos desplazarnos entre paneles escribiendo `[Ctrl] + [B]`+ `[O]`( `prefix`+ `[O]`).

Por último, podemos borrar el historial del panel escribiendo `[Ctrl] + [B]`seguido de `[Alt] + [C]`( `prefix`+ `[Alt] + [C]`).

Hay muchas otras cosas que podemos hacer con Tmux, como personalizaciones que podemos realizar con el registro de Tmux (por ejemplo, [cambiar la ruta de registro predeterminada](https://github.com/tmux-plugins/tmux-logging/blob/master/docs/configuration.md) , cambiar las combinaciones de teclas, ejecutar múltiples ventanas dentro de las sesiones y paneles dentro de esas ventanas, etc.). Vale la pena informarse sobre todas las funciones que ofrece Tmux y descubrir cómo la herramienta se adapta mejor a su flujo de trabajo. Finalmente, aquí hay algunos plugins adicionales que nos gustan:

* [tmux-sessionist](https://github.com/tmux-plugins/tmux-sessionist) : nos brinda la capacidad de manipular sesiones de Tmux desde dentro de una sesión: cambiar a otra sesión, crear una nueva sesión con nombre, matar una sesión sin separar Tmux, promover el panel actual a una nueva sesión y más.
* [tmux-pain-control](https://github.com/tmux-plugins/tmux-pain-control) : un complemento para controlar paneles y proporcionar combinaciones de teclas más intuitivas para moverse, redimensionar y dividir paneles.
* [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect) : Este práctico plugin nos permite restaurar nuestro entorno Tmux tras reiniciar el host. Algunas funciones incluyen la restauración de todas las sesiones, ventanas, paneles y su orden, la restauración de programas en ejecución en un panel, la restauración de sesiones de Vim y mucho más.

Consulta la [lista completa de plugins de tmux](https://github.com/tmux-plugins/list) para ver si otros se adaptan a tu flujo de trabajo. Para más información sobre tmux, consulta este excelente [video](https://www.youtube.com/watch?v=Lqehvpe_djs) de Ippsec y esta [guía práctica](https://mavericknerd.github.io/knowledgebase/ippsec/tmux/) basada en él.

***

## <mark style="color:purple;">Artefactos abandonados</mark>

Como mínimo, deberíamos registrar cuándo se usó un payload, en qué host se usó, en qué ruta de archivos se colocó en el objetivo y si el cliente la limpió o necesita limpiarla. También se recomienda un hash de archivo para facilitar la búsqueda por parte del cliente. Es recomendable proporcionar esta información incluso si eliminamos web shells, payloads o herramientas.

### **Creación de cuenta/Modificaciones del sistema**

Si creamos cuentas o modificamos la configuración del sistema, es evidente que debemos realizar un seguimiento de estos cambios en caso de que no podamos revertirlos una vez finalizada la evaluación. Algunos ejemplos incluyen:

* Dirección IP del host(s)/nombre(s) de host donde se realizó el cambio
* Marca de tiempo del cambio
* Descripción del cambio
* Ubicación en el host(s) donde se realizó el cambio
* Nombre de la aplicación o servicio que fue manipulado
* Nombre de la cuenta (si creó una) y quizás la contraseña en caso de que se le solicite que la entregue

No hace falta decirlo, pero como profesional y para evitar crearse enemigos en el equipo de infraestructura, es recomendable obtener la aprobación por escrito del cliente antes de realizar este tipo de modificaciones del sistema o cualquier tipo de prueba que pueda causar problemas de estabilidad o disponibilidad. Esto normalmente se puede resolver durante la llamada de inicio del proyecto para determinar el límite que el cliente está dispuesto a tolerar sin ser notificado.

***

## <mark style="color:purple;">Evidencias</mark>

Independientemente del tipo de evaluación, a nuestro cliente (normalmente) no le importan las cadenas de exploits que implementamos ni la facilidad con la que "destruimos" su red. En definitiva, pagan por el informe, que debe comunicar claramente los problemas detectados y las pruebas que puedan utilizarse para la validación y la reproducción. Sin pruebas claras, puede resultar difícil para los equipos de seguridad interna, administradores de sistemas, desarrolladores, etc., reproducir nuestro trabajo mientras implementan una solución o incluso comprender la naturaleza del problema.

### **Qué capturar**

Como sabemos, cada hallazgo requiere evidencia. También puede ser prudente recopilar evidencia de las pruebas realizadas que no tuvieron éxito, por si el cliente cuestiona su minuciosidad. Si trabaja en la línea de comandos, los registros de Tmux pueden ser evidencia suficiente para pegarlos en el informe como salida literal de la terminal, pero pueden tener un formato pésimo. Por esta razón, es recomendable capturar la salida de la terminal para los pasos significativos a medida que avanza y hacer un seguimiento por separado junto con sus hallazgos. Para todo lo demás, se recomienda tomar capturas de pantalla.

### **Almacenamiento**

Al igual que con nuestra estructura de toma de notas, conviene crear un marco para organizar los datos recopilados durante una evaluación. Esto puede parecer excesivo en evaluaciones pequeñas, pero si realizamos pruebas en un entorno grande y no contamos con una forma estructurada de llevar un registro, terminaremos olvidando algo, infringiendo las reglas de participación y probablemente haciendo cosas más de una vez, lo que puede suponer una gran pérdida de tiempo, especialmente durante una evaluación con límite de tiempo. A continuación, se sugiere una estructura de carpetas básica, pero es posible que deba adaptarla según el tipo de evaluación que esté realizando o las circunstancias específicas.

* <mark style="color:purple;">`Admin`</mark>
  * Alcance del trabajo o Scope of Work (SoW) en el que está trabajando, sus notas de la reunión de inicio del proyecto, informes de estado, notificaciones de vulnerabilidad, etc.
* <mark style="color:purple;">`Entregables`</mark>
  * Carpeta para guardar los entregables a medida que los trabaja. Generalmente, esta carpeta será su informe, pero puede incluir otros elementos, como hojas de cálculo y presentaciones complementarias, según los requisitos específicos del cliente.
* <mark style="color:purple;">`Evidencias`</mark>
  * <mark style="color:orange;">`Recomendaciones`</mark>
    * Le sugerimos crear una carpeta para cada hallazgo que planee incluir en el informe para guardar la evidencia de cada hallazgo en un contenedor y hacer que sea más fácil armar el recorrido cuando escriba el informe.
  * <mark style="color:orange;">`Escaneos`</mark>
    * `Análisis de vulnerabilidades`
      * Exporte archivos desde su escáner de vulnerabilidad (si corresponde para el tipo de evaluación) para archivarlos.
    * `Enumeración de servicios`
      * Exporta archivos de las herramientas que utilizas para enumerar servicios en el entorno de destino, como Nmap, Masscan, Rumble, etc.
    * `Web`
      * Exportar archivos para herramientas como archivos de estado ZAP o Burp, EyeWitness, Aquatone, etc.
    * `Enumeración AD`
      * Archivos JSON de BloodHound, archivos CSV generados desde PowerView o ADRecon, datos de Ping Castle, archivos de registro de Snaffler, registros de CrackMapExec, datos de herramientas Impacket, etc.
  * <mark style="color:orange;">`Notas`</mark>
    * Una carpeta para guardar tus notas.
  * <mark style="color:orange;">`OSINT`</mark>
    * Cualquier salida OSINT de herramientas como Intelx y Maltego que no se ajuste bien a su documento de notas.
  * <mark style="color:orange;">`Wireless`</mark>
    * Opcional si las pruebas inalámbricas están dentro del alcance, puede usar esta carpeta para la salida de las herramientas de pruebas inalámbricas.
  * <mark style="color:orange;">`Logging Output`</mark>
    * Registra la salida de Tmux, Metasploit y cualquier otra salida de registro que no se ajuste a los subdirectorios `Scan` enumerados anteriormente.
  * <mark style="color:orange;">`Archivos varios`</mark>
    * Web shells, payloads, scripts personalizados y cualquier otro archivo generado durante la evaluación que sea relevante para el proyecto.
* <mark style="color:purple;">`Retest`</mark>
  * Esta carpeta es opcional si necesita regresar después de la evaluación original y volver a analizar los hallazgos previamente descubiertos. Puede replicar la estructura de carpetas que utilizó durante la evaluación inicial en este directorio para mantener la evidencia de la nueva prueba separada de la evidencia original.

### Script de configuración de directorios

Es recomendable tener scripts y trucos para la configuración al inicio de una evaluación. Podríamos usar el siguiente comando para crear nuestros directorios y subdirectorios y adaptarlos aún más.

#### En español

```shell-session
afsh4ck@kali$ mkdir -p ACME-IPT/{Admin,Entregables,Evidencias/{Hallazgos,Escaneos/{Vulnerabilidades,Servicios,Web,'Enumeración AD'},Notas,OSINT,Wireless,'Salida de terminal','Archivos varios'},Retest}
```

#### En inglés

```shell-session
afsh4ck@kali$ mkdir -p ACME-IPT/{Admin,Deliverables,Evidence/{Findings,Scans/{Vuln,Service,Web,'AD Enumeration'},Notes,OSINT,Wireless,'Logging output','Misc Files'},Retest}
```

```shell-session
afsh4ck@kali$ tree ACME-IPT/

ACME-IPT/
├── Admin
├── Deliverables
├── Evidence
│   ├── Findings
│   ├── Logging output
│   ├── Misc Files
│   ├── Notes
│   ├── OSINT
│   ├── Scans
│   │   ├── AD Enumeration
│   │   ├── Service
│   │   ├── Vuln
│   │   └── Web
│   └── Wireless
└── Retest
```

Una característica interesante de una herramienta como Obsidian es que podemos combinar la estructura de carpetas con la de notas. De esta forma, podemos interactuar con las notas/carpetas directamente desde la línea de comandos o dentro de Obsidian. Aquí podemos ver la estructura general de carpetas en funcionamiento con Obsidian.

<figure><img src="/files/AIniUttaipy0QtC97uTw" alt=""><figcaption></figcaption></figure>

Profundizando más, podemos ver los beneficios de combinar la toma de notas y la estructura de carpetas. Durante una evaluación real, podemos añadir páginas o carpetas adicionales o eliminar algunas, una página y una carpeta por cada hallazgo, etc.

<figure><img src="/files/NeRSMCtGXG7YalOckMAB" alt=""><figcaption></figcaption></figure>

Echando un vistazo rápido a la estructura del directorio, podemos ver cada carpeta que creamos anteriormente. También podríamos crear una estructura de directorios y archivos más compleja con el siguiente script:

{% code title="Obsidian-Pentest.sh" %}

```bash
#!/bin/bash

# Definir la estructura de directorios
mkdir -p "Penetration Testing Report/Admin"
mkdir -p "Penetration Testing Report/Deliverables/Reports"
mkdir -p "Penetration Testing Report/Deliverables/Presentations"
mkdir -p "Penetration Testing Report/Deliverables/Checklists"
mkdir -p "Penetration Testing Report/Evidence/Findings"
mkdir -p "Penetration Testing Report/Evidence/Logging output"
mkdir -p "Penetration Testing Report/Evidence/Misc files"
mkdir -p "Penetration Testing Report/Evidence/Notes"
mkdir -p "Penetration Testing Report/Evidence/OSINT"
mkdir -p "Penetration Testing Report/Evidence/Scans/AD Enumeration"
mkdir -p "Penetration Testing Report/Evidence/Scans/Service"
mkdir -p "Penetration Testing Report/Evidence/Scans/Vuln"
mkdir -p "Penetration Testing Report/Evidence/Scans/Web"
mkdir -p "Penetration Testing Report/Evidence/Wireless"
mkdir -p "Penetration Testing Report/Evidence/Screenshots"
mkdir -p "Penetration Testing Report/Evidence/Credentials"
mkdir -p "Penetration Testing Report/Evidence/Exploits"
mkdir -p "Penetration Testing Report/Retest"
mkdir -p "Penetration Testing Report/Documentation/Methodology"
mkdir -p "Penetration Testing Report/Documentation/Tools"
mkdir -p "Penetration Testing Report/Documentation/References"

# Crear archivos en Findings
declare -a findings=(
    "H1 - Kerberoasting",
    "H2 - ASREPRoasting",
    "H3 - LLMNR&NBT-NS Response Spoofing",
    "H4 - Tomcat Manager Weak Credentials",
    "H5 - SQL Injection",
    "H6 - XSS Vulnerabilities",
    "H7 - Privilege Escalation",
    "H8 - SMB Relay Attack",
    "H9 - NTLMv2 Hash Capture"
)

for finding in "${findings[@]}"; do
    touch "Penetration Testing Report/Evidence/Findings/$finding.md"
done

# Crear archivos en Notes
declare -a notes=(
    "1. Administrative Information",
    "2. Scoping Information",
    "3. Activity Log",
    "4. Payload Log",
    "5. OSINT Data",
    "6. Credentials",
    "7. Web Application Research",
    "8. Vulnerability Scan Research",
    "9. Service Enumeration Research",
    "10. AD Enumeration Research",
    "11. Attack Path",
    "12. Findings",
    "13. Exploits Used",
    "14. Post-Exploitation Findings"
)

for note in "${notes[@]}"; do
    touch "Penetration Testing Report/Evidence/Notes/$note.md"
done

# Crear archivos en Deliverables
touch "Penetration Testing Report/Deliverables/Reports/Final Report.docx"
touch "Penetration Testing Report/Deliverables/Reports/Executive Summary.docx"
touch "Penetration Testing Report/Deliverables/Reports/Technical Report.docx"
touch "Penetration Testing Report/Deliverables/Presentations/Presentation.pptx"
touch "Penetration Testing Report/Deliverables/Checklists/Pentest Checklist.md"

# Crear archivos en Documentation
touch "Penetration Testing Report/Documentation/Methodology/Testing Methodology.md"
touch "Penetration Testing Report/Documentation/Tools/Tools Used.md"
touch "Penetration Testing Report/Documentation/References/References.md"

echo "Estructura de pentesting completa creada correctamente."
```

{% endcode %}

```shell-session
afsh4ck@kali$ tree
.
└── Inlanefreight Penetration Test
    ├── Admin
    ├── Deliverables
    ├── Evidence
    │   ├── Findings
    │   │   ├── H1 - Kerberoasting.md
    │   │   ├── H2 - ASREPRoasting.md
    │   │   ├── H3 - LLMNR&NBT-NS Response Spoofing.md
    │   │   └── H4 - Tomcat Manager Weak Credentials.md
    │   ├── Logging output
    │   ├── Misc files
    │   ├── Notes
    │   │   ├── 10. AD Enumeration Research.md
    │   │   ├── 11. Attack Path.md
    │   │   ├── 12. Findings.md
    │   │   ├── 1. Administrative Information.md
    │   │   ├── 2. Scoping Information.md
    │   │   ├── 3. Activity Log.md
    │   │   ├── 4. Payload Log.md
    │   │   ├── 5. OSINT Data.md
    │   │   ├── 6. Credentials.md
    │   │   ├── 7. Web Application Research.md
    │   │   ├── 8. Vulnerability Scan Research.md
    │   │   └── 9. Service Enumeration Research.md
    │   ├── OSINT
    │   ├── Scans
    │   │   ├── AD Enumeration
    │   │   ├── Service
    │   │   ├── Vuln
    │   │   └── Web
    │   └── Wireless
    └── Retest

16 directories, 16 files
```

{% hint style="success" %}
**Recordatorio**: La estructura de carpetas y notas que se muestra arriba es la que nos ha funcionado en nuestras carreras, pero variará según la persona y la interacción. Te animamos a que la pruebes como base, veas cómo te funciona y la uses como base para crear un estilo que te funcione. Lo importante es que somos minuciosos y organizados, y no hay una única forma de abordarlo.&#x20;
{% endhint %}

Igualmente podemos usar este script en powershell en Windows:

{% code title="obsidian.ps1" %}

```powershell
# Base directory
$base = "Penetration Testing Report"

# Define directory structure
$folders = @(
    "$base/Admin",
    "$base/Deliverables/Reports",
    "$base/Deliverables/Presentations",
    "$base/Deliverables/Checklists",
    "$base/Evidence/Findings",
    "$base/Evidence/Logging output",
    "$base/Evidence/Misc files",
    "$base/Evidence/Notes",
    "$base/Evidence/OSINT",
    "$base/Evidence/Scans/AD Enumeration",
    "$base/Evidence/Scans/Service",
    "$base/Evidence/Scans/Vuln",
    "$base/Evidence/Scans/Web",
    "$base/Evidence/Wireless",
    "$base/Evidence/Screenshots",
    "$base/Evidence/Credentials",
    "$base/Evidence/Exploits",
    "$base/Retest",
    "$base/Documentation/Methodology",
    "$base/Documentation/Tools",
    "$base/Documentation/References"
)

# Create folders
foreach ($folder in $folders) {
    New-Item -Path $folder -ItemType Directory -Force | Out-Null
}

# Create findings files
$findings = @(
    "H1 - Kerberoasting",
    "H2 - ASREPRoasting",
    "H3 - LLMNR&NBT-NS Response Spoofing",
    "H4 - Tomcat Manager Weak Credentials",
    "H5 - SQL Injection",
    "H6 - XSS Vulnerabilities",
    "H7 - Privilege Escalation",
    "H8 - SMB Relay Attack",
    "H9 - NTLMv2 Hash Capture"
)

foreach ($f in $findings) {
    New-Item -Path "$base/Evidence/Findings/$f.md" -ItemType File -Force | Out-Null
}

# Create notes files
$notes = @(
    "1. Administrative Information",
    "2. Scoping Information",
    "3. Activity Log",
    "4. Payload Log",
    "5. OSINT Data",
    "6. Credentials",
    "7. Web Application Research",
    "8. Vulnerability Scan Research",
    "9. Service Enumeration Research",
    "10. AD Enumeration Research",
    "11. Attack Path",
    "12. Findings",
    "13. Exploits Used",
    "14. Post-Exploitation Findings"
)

foreach ($n in $notes) {
    New-Item -Path "$base/Evidence/Notes/$n.md" -ItemType File -Force | Out-Null
}

# Deliverables files
New-Item -Path "$base/Deliverables/Reports/Final Report.docx" -ItemType File -Force | Out-Null
New-Item -Path "$base/Deliverables/Reports/Executive Summary.docx" -ItemType File -Force | Out-Null
New-Item -Path "$base/Deliverables/Reports/Technical Report.docx" -ItemType File -Force | Out-Null
New-Item -Path "$base/Deliverables/Presentations/Presentation.pptx" -ItemType File -Force | Out-Null
New-Item -Path "$base/Deliverables/Checklists/Pentest Checklist.md" -ItemType File -Force | Out-Null

# Documentation files
New-Item -Path "$base/Documentation/Methodology/Testing Methodology.md" -ItemType File -Force | Out-Null
New-Item -Path "$base/Documentation/Tools/Tools Used.md" -ItemType File -Force | Out-Null
New-Item -Path "$base/Documentation/References/References.md" -ItemType File -Force | Out-Null

Write-Host "✅ Penetration testing report structure created successfully."

```

{% endcode %}

Obsidian es una herramienta excelente, y este formato es claro, fácil de seguir y fácilmente reproducible entre interacciones. Puedes crear un script para crear la estructura de directorios y los 10 archivos Markdown iniciales. Tendrás la oportunidad de experimentar con esta estructura de ejemplo mediante el acceso a la interfaz gráfica de usuario de una máquina virtual Parrot al final de esta sección.

***

## <mark style="color:purple;">Formato y redacción</mark>

Las credenciales y la información personal identificable ( `PII`) deben eliminarse en las capturas de pantalla y cualquier elemento que sea moralmente objetable, como material gráfico o comentarios y lenguaje obsceno. También puede considerar lo siguiente:

* Agregar anotaciones a la imagen, como flechas o cuadros, para llamar la atención sobre los elementos importantes en la captura de pantalla, en particular si suceden muchas cosas en la imagen (no haga esto en MS Word).
* Agregar un borde mínimo alrededor de la imagen para que se destaque sobre el fondo blanco del documento.
* Recortar la imagen para mostrar solo la información relevante (por ejemplo, en lugar de una captura de pantalla completa, solo para mostrar un formulario de inicio de sesión básico).
* Incluya la barra de direcciones del navegador o alguna otra información que indique a qué URL o host está conectado.

### **Capturas de pantalla**

**Una de las mejores herramientas para capturas de pantalla que podemos utilizar es Flameshot:**

{% embed url="<https://flameshot.org/>" %}

Siempre que sea posible, debemos intentar usar la salida de la terminal en lugar de capturas de pantalla. Es más fácil redactar, resaltar las partes importantes (es decir, el comando que ejecutamos en texto azul y la parte de la salida que queremos destacar en rojo), generalmente se ve más ordenado en el documento y puede evitar que el documento se convierta en un archivo enorme y difícil de manejar si tenemos muchos hallazgos.&#x20;

Debemos tener cuidado de no alterar la salida de la terminal, ya que queremos dar una representación exacta del comando que ejecutamos y el resultado. Está bien acortar o cortar la salida innecesaria y marcar la parte eliminada con, `<SNIP>` pero nunca alterar la salida ni agregar cosas que no estaban en el comando o la salida original. El uso de figuras basadas en texto también facilita que el cliente copie y pegue para reproducir los resultados. También es importante que el material de origen que está pegando *tenga* todo el formato eliminado antes de entrar en su documento de Word. Si está pegando texto que tiene formato incrustado, puede terminar pegando caracteres no codificados en UTF-8 en sus comandos (generalmente comillas alternativas o apóstrofes), lo que en realidad puede provocar que el comando no funcione correctamente cuando el cliente intente reproducirlo.

Una forma común de redactar capturas de pantalla es mediante la pixelación o el desenfoque con una herramienta como Greenshot. [Las investigaciones](https://www.bleepingcomputer.com/news/security/researcher-reverses-redaction-extracts-words-from-pixelated-image/) han demostrado que este método no es infalible y que existe una alta probabilidad de recuperar los datos originales revirtiendo la técnica de pixelación/desenfoque. Esto se puede hacer con una herramienta como [Unredacter](https://github.com/bishopfox/unredacter) . En su lugar, debemos evitar esta técnica y usar barras negras (u otra forma sólida) sobre el texto que queremos redactar. Debemos editar la imagen directamente y no simplemente aplicar una forma en MS Word, ya que alguien con acceso al documento podría eliminarla fácilmente. Por cierto, si escribe una entrada de blog o algo publicado en la web con datos confidenciales redactados, no confíe en el estilo HTML/CSS para intentar ocultar el texto (es decir, texto negro con fondo negro), ya que esto se puede ver fácilmente resaltando el texto o editando temporalmente el código fuente de la página. En caso de duda, use la salida de consola, pero si debe usar una captura de pantalla de terminal, asegúrese de redactar la información correctamente. A continuación, se muestran ejemplos de las dos técnicas:

#### **Pixelar datos de contraseñas**

<figure><img src="/files/ZxJYd47f4PKs0FRbVZjB" alt=""><figcaption></figcaption></figure>

#### **Borrar contraseña con forma sólida**

<figure><img src="/files/RgeubUYezbWVPUWDhBHv" alt=""><figcaption></figcaption></figure>

Finalmente, se sugiere presentar la evidencia terminal en un informe. Conservamos el comando y la salida originales, pero los mejoramos para resaltar tanto el comando como la salida de interés (autenticación correcta).

<figure><img src="/files/DawWSWxDg02v6R3LvdvD" alt=""><figcaption></figcaption></figure>

La forma de presentar la evidencia varía según el informe. Es posible que no podamos copiar y pegar la salida de la consola, por lo que tendremos que usar una captura de pantalla. Los consejos que se presentan aquí ofrecen opciones para crear un informe claro y preciso con toda la evidencia representada adecuadamente.

### **Terminal**

Normalmente, lo único que debe eliminarse de la salida de la terminal son las credenciales (ya sea en el propio comando o en su salida). Esto incluye los hashes de contraseñas. En el caso de los hashes de contraseñas, normalmente se puede eliminar la parte central y dejar los primeros 3 o 4 caracteres, así como los últimos, para indicar que efectivamente había un hash. Para credenciales en texto plano o cualquier otro contenido legible que deba ofuscarse, se puede reemplazar con un marcador de posición `<REDACTED>` o `<PASSWORD REDACTED>`, o algo similar.

También debería considerar el resaltado con código de colores en la salida de su terminal para destacar el comando ejecutado y el resultado interesante. Esto facilita que el lector identifique las partes esenciales de la evidencia y qué buscar si intenta reproducirla por su cuenta. Si trabaja con una carga útil web compleja, puede ser difícil identificarla en un enorme bloque de texto de solicitud con URL codificada si no se dedica a esto. Debemos aprovechar todas las oportunidades para que el informe sea más claro para nuestros lectores, quienes a menudo no tendrán un conocimiento tan profundo del entorno (especialmente desde la perspectiva de un pentester) como el nuestro al final de la evaluación.

***

## <mark style="color:purple;">Qué no archivar</mark>

Al iniciar una prueba de penetración, nuestros clientes confían en nosotros para acceder a su red y evitar causar daños siempre que sea posible. Esto significa no interrumpir ningún host ni afectar la disponibilidad de aplicaciones o recursos, no cambiar contraseñas (a menos que se permita explícitamente), no realizar cambios de configuración significativos o difíciles de revertir, ni ver o eliminar ciertos tipos de datos del entorno. Estos datos pueden incluir `información personal identificable (PII)` sin redactar, información potencialmente delictiva, cualquier elemento considerado legalmente "descubrible", etc.

Por ejemplo, si accede a un recurso compartido de red con datos confidenciales, probablemente sea mejor simplemente capturar la carpeta con los archivos en lugar de abrir archivos individuales y capturar su contenido. Si los archivos son tan confidenciales como cree, recibirán el mensaje y sabrán qué contienen según el nombre del archivo. Recopilar PII real y extraerla del entorno objetivo puede implicar importantes obligaciones de cumplimiento para el almacenamiento y procesamiento de dichos datos, como el RGPD y otras disposiciones similares, y podría generar numerosos problemas tanto para nuestra empresa como para nosotros.

***

## <mark style="color:purple;">Seguimos</mark>

Ahora que tenemos una buena idea de nuestra estructura de organización de carpetas y toma de notas y qué tipos de evidencia conservar y no conservar, y qué registrar para nuestros informes, hablemos de los distintos tipos de informes que nuestros clientes pueden solicitar según el tipo de compromiso.
