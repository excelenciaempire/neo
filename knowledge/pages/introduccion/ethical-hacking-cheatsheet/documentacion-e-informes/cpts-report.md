
# CPTS Report

<figure><img src="/files/ijEfLwFFJHTorVMGR397" alt=""><figcaption></figcaption></figure>

El examen `Certified Penetration Testing Specialist - CPTS` de HTB tiene dos criterios principales que debes cumplir dentro del período de examen de `diez días`:

1. Captura al menos doce de las catorce flags disponibles.
2. Producir un informe de prueba de penetración de nivel comercial y alta calidad.

Si eres como yo antes del examen, probablemente tengas confianza en tus habilidades de hacking, pero quizás no tengas mucha experiencia en la redacción de informes de pruebas de penetración.

Una buena manera de prepararse, como se recomienda en el material del curso, es crear informes simulados. Esta práctica puede ayudarte a desarrollar las habilidades necesarias para redactar un informe sólido el día del examen.

Pero, sinceramente, no hice nada de eso (salvo algunos informes de CTF). El primer informe real de pruebas de penetración que escribí fue el que presenté para mi examen. Y, según los comentarios que recibí, creo que quedó bastante bien.

Lo logré desarrollando de antemano lo que llamo una **metodología de informes basada en activadores o "Triggers"**, que seguí durante el examen con gran éxito.

Esta metodología me permitió completar el informe a medida que avanzaba en el proyecto. Mantuvo el proceso fluido y equilibrado, de modo que la redacción del informe no interrumpió mi ritmo de trabajo y viceversa.

En esta publicación, compartiré las herramientas que utilicé para escribir mi informe y la metodología única que me ayudó a tener éxito.

{% hint style="warning" %}
**Nota:** No tomes esta publicación como una recomendación para omitir la práctica de reportar. Si sientes la necesidad de practicar, hazlo. Solo comparto lo que me funcionó.
{% endhint %}

## <mark style="color:purple;">Herramientas</mark> <a href="#tools" id="tools"></a>

Antes de profundizar en la metodología de informes, cubramos rápidamente las herramientas que utilicé para escribir mi informe. Si bien la metodología es el enfoque principal, estas herramientas fueron cruciales para mi éxito.

### SysReptor <a href="#sysreptor" id="sysreptor"></a>

Cuando empecé a revisar el material del curso, estaba seguro de que usaría un procesador de texto sencillo como LibreOffice Writer para escribir mi informe. No quería lidiar con la sobrecarga de un software especializado en informes de pruebas de penetración, así que decidí descargar una plantilla de internet y empezar a escribir.

Pero una vez que llegué al módulo de [Documentación e Informes](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/documentacion-e-informes.md), me di cuenta de que no era suficiente. Al ver la complejidad y el detalle que implica un informe profesional, me di cuenta de que necesitaba un software adecuado para redactar informes.

Decidí probar [SysReptor](https://docs.sysreptor.com/) , una herramienta de generación de informes diseñada específicamente para pruebas de penetración. Es gratuita, de código abierto y alojada por el usuario.

{% embed url="<https://docs.sysreptor.com/>" %}

<figure><img src="/files/yI7HlLn6lmwPE4ok3DDX" alt=""><figcaption></figcaption></figure>

#### Instalación en Kali Linux

```bash
# Actualiza paquetes y dependencias
sudo apt update
sudo apt install -y sed curl openssl uuid-runtime coreutils
```

```bash
# Descarga y instala Docker
curl -fsSL https://get.docker.com | sudo bash

# Descarga e instala Docker Compose V.2 (necesario)
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
```

```bash
# Añade al usuario al grupo Docker
sudo usermod -aG docker $USER
newgrp docker
```

```bash
# Instala sysreptor
bash <(curl -s https://docs.sysreptor.com/install.sh)

Good to see you.
Get ready for the easiest pentest reporting tool.

Downloading Docker Compose files from https://github.com/syslifters/sysreptor/releases/latest/download/setup.tar.gz ...
Checking download...
Unpacking sysreptor.tar.gz...
License key (leave blank for Community Edition; you can upgrade anytime later): 
Encrypt files and database? [y/n]: n
Creating app.env...
Generating Django secret key...

<----SNIP---->

All imported.

Very nice.
You can now login at http://127.0.0.1:9999
Username: reptor
Password: uU+fSHd9mPPqlLCWf9Piroe8veI
```

{% hint style="warning" %}
**Nota**: En la instalación en Kali Linux se recomienda no usar un puerto común en actividades de hacking para el webser, como los puertos 80, 8080, 4444, 443, etc... usar un puerto como el `9999` por ejemplo.
{% endhint %}

Sysreptor resultó ser una excelente decisión, ya que facilitó considerablemente el proceso de generación de informes en comparación con escribirlo todo desde cero. SysReptor realmente cumple su promesa de simplificar la creación de informes.

En resumen, SysReptor funciona permitiéndole elegir una plantilla de informe que divide el documento en secciones, cada una con sus propios campos. Simplemente edite los campos y añada sus hallazgos para completar el informe. La estructuración y el estilo del informe ya están hechos.

Cuando hayas terminado, puedes exportar el informe como un documento PDF o una página HTML.

{% embed url="<https://www.brunorochamoura.com/posts/cpts-report/sysreptor-example.gif>" %}

Además existe una [plantilla CPTS oficial de HTB](https://docs.sysreptor.com/assets/reports/HTB-CPTS-Report.pdf) para SysReptor, ¡recomendada por Hack The Box! Consulta la demo para ver cómo quedaría un informe final.

Puedes consultar esta [publicación de blog de HTB](https://www.hackthebox.com/blog/certification-templates) sobre cómo instalar SysReptor y agregar la plantilla CPTS.

Puedes instalar la plantilla con el siguiente comando:

```bash
cd sysreptor/deploy
url="https://docs.sysreptor.com/assets/htb-designs.tar.gz"
curl -s "$url" | docker compose exec --no-TTY app python3 manage.py importdemodata --type=design
```

Después solo tenemos que recargar Sysreptor y nos aparecerán las plantillas en Designs:

<figure><img src="/files/SoWtNoogk5ZNscXr7I0H" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/byWixDzu0PudibWVwRtI" alt=""><figcaption></figcaption></figure>

La metodología que desarrollé se basa en completar la plantilla HTB CPTS de SysReptor, por lo que tenerla instalada es un requisito previo.

### ChatGPT <a href="#chatgpt" id="chatgpt"></a>

Otro recurso valioso para redactar informes es ChatGPT o cualquier otro chatbot LLM de su elección.

Puedes mejorar la calidad y la eficiencia de tu proceso de escritura redactando textos rápidamente sin preocuparte demasiado por la gramática ni la fluidez. La IA puede refinarlo corrigiendo errores y ajustando el tono a tus necesidades.

Simplemente pedirle al bot que “`reformule el texto de una manera clara y profesional`” puede transformar tu borrador en un informe pulido y profesional en poco tiempo, lo que te permitirá concentrarte en el pentesting.

Sin embargo, es importante revisar cuidadosamente lo que produce el bot para asegurarte de que se ajuste a tu visión. Además, limita su uso a reformular lo que escribes en lugar de generar contenido desde cero, ya que la IA a veces puede generar contenido sin sentido.

***

## <mark style="color:purple;">Metodología</mark> <a href="#methodology" id="methodology"></a>

Muy bien, profundicemos en la metodología real y cómo surgió.

Un consejo común para este (y otros) exámenes es no dejar la redacción de informes para el final. En su lugar, conviene trabajar en ella a medida que se avanza.

Este es un consejo sólido, pero no aborda realmente una pregunta crucial: ¿cuándo debería tomarse un descanso de piratear para actualizar su informe?

Si actualizas tu informe con demasiada frecuencia, interrumpes tu flujo de trabajo y ralentizas tu progreso. Pero si te tomas muy pocos descansos, tendrás demasiado que reportar a la vez, lo que puede perjudicar la calidad de tus informes. La clave está en encontrar un equilibrio predecible y manejable.

Aquí es donde entra en juego mi metodología. Como mencioné antes, usaremos la plantilla SysReptor HTB CPTS, que gestiona la estructura del informe. Ahora solo necesitamos una estrategia clara sobre cuándo y cómo completarlo.

Lo que desarrollé es un **enfoque basado en activadores** , donde asigno los diferentes campos del informe a hitos específicos durante el compromiso.

Cada vez que alcanzo un hito, me motiva a trabajar en ciertas partes del informe. Al establecer esto de antemano, siempre sé cuándo tomarme un descanso y exactamente en qué secciones del informe centrarme en ese momento.

Seguir esta metodología tiene varios beneficios:

* **Claro y fácil de seguir con un enfoque práctico.**
* **Elimina las conjeturas sobre cuándo pausar el pentesting para trabajar en los informes.**
* **Divide los informes en pequeñas sesiones relacionadas con lo que acabas de trabajar.**
* **Los informes son detallados porque escribes mientras las cosas están frescas en tu mente.**
* **Gracias a SysReptor no es necesario preocuparse por el estilo ni la estructura del informe.**
* **Tu informe estará completo en más del 90% cuando termines de capturar las flags.**

Vamos a entrar en materia.

### Estructura del informe <a href="#reporting-structure" id="reporting-structure"></a>

Antes de sumergirnos en los activadores que utilicé y recomiendo personalmente, veamos primero la estructura de la plantilla HTB CPTS SysReptor.

<figure><img src="/files/Qj5goU36cBh55OU2SezC" alt=""><figcaption></figcaption></figure>

A continuación se muestran las secciones y sus respectivos campos:

* `Meta`
  * Nombre, título y email
  * Engagement Information
* `Document Control`
  * Customer Contacts
* `Executive Summary`
  * Executive Summary
  * Approach
  * Scope
  * Assessment Overview and Recommendations
* `Network Penetration Testing Assessment Summary`
  * Network Summary
  * Summary of Findings
* `Internal Network Compromise Walkthrough`
  * Walkthrough Summary
  * Detailed Walkthrough
* `Remediation Summary`
  * Remediation Summary
  * Short Term
  * Medium Term
  * Long Term
* `Appendix`
  * Finding Severities
  * Host & Service Discovery
  * Subdomain Discovery
  * Exploited Hosts
  * Compromised Users
  * Changes/Host Cleanup
  * Flags Discovered
  * Domain Password Review
* `Findings`
  * Title
  * CWE
  * CVSS
  * Overview
  * Impact
  * Affected Components
  * Recommendations
  * References
  * Details

La mayoría de los campos ya tienen textos predeterminados. Estos pueden ser marcadores que deberá completar o texto estándar bastante aceptable.

No es necesario modificar drásticamente todos los campos, ya que algunos ya tienen texto que funciona bien en la mayoría de los informes. Estas son las viñetas que no están resaltadas en negrita. Puede dejarlas prácticamente como están (pero asegúrate de leerlas) o reformularlas con tus propias palabras.

{% hint style="danger" %}
Los campos <mark style="color:red;">**`TODO`**</mark> en rojo son aquellos en los que definitivamente necesitarás cambiar el texto predeterminado por el tuyo. Además podemos escribir nosotros <mark style="color:red;">**`TODO`**</mark> manualmente para crear nuestras propias plantillas y que si olvidamos completarlo que aparezca como error antes de exportar el reporte.
{% endhint %}

<figure><img src="/files/Mdjq7CZqlkOwpOYqOC57" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/zXQjOakDZwNJKN2c7klt" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Triggers</mark> <a href="#triggers" id="triggers"></a>

Por último, repasemos los factores desencadenantes que utilicé durante el examen.

Asociaremos los hitos que se produzcan naturalmente durante el pentesting con campos específicos del informe. **Cuando se active un evento, deténte y completa los campos correspondientes.**

La idea es que al completar el informe a medida que ocurren estos hitos, tendrás la mayor parte del informe listo cuando finalice el compromiso.

Estos son los triggers que utilicé, pero puedes crear los tuyos propios según lo que mejor te funcione. Asegúrate de anotarlos y consultarlos regularmente durante el examen. Si lo deseas, puedes consultar el índice de esta entrada del blog periódicamente.

### Cuando comienza el examen <a href="#when-the-exam-starts" id="when-the-exam-starts"></a>

Estos son los campos que deberás rellenar nada más iniciar el examen y recibir la información sobre el pentesting que realizarás:

* `Meta`
  * Nombre, título y email
  * Engagement Information
* `Document Control`
  * Customer Contacts
* `Network Penetration Testing Assessment Summary`
  * Network Summary
  * Summary of Findings
* `Executive Summary`
  * Executive Summary
  * Approach
  * Scope

Básicamente, complete completamente las secciones **Meta** , **Document control** y **Network Penetration Testing Assessment Summary** y la mayor parte del **Executive Summary** , dejando el campo **Descripción general de la evaluación y Recomendaciones** para más adelante.

La mayoría de estos campos son bastante estándar y requieren poca o ninguna modificación. Léalos detenidamente y decida usted mismo si necesita cambiar algo o dejarlos como están.

### Cuando descubres un host o servicio <a href="#when-a-host-or-service-is-discovered" id="when-a-host-or-service-is-discovered"></a>

Una vez que descubras un host activo y enumere los servicios disponibles (por ejemplo, a través de un escaneo de Nmap), debe completar el apéndice correspondiente:

* Appendix
  * **Host & Service Discovery**

En este campo, me desvié ligeramente del texto predeterminado proporcionado por la plantilla y creé una tabla para cada host descubierto con sus servicios disponibles.

Para cada host descubierto, crea una tabla con las siguientes columnas:

#### Host 01 - example.com

<table><thead><tr><th width="96.07421875">Port</th><th width="197.51953125">Service</th><th>Notes</th></tr></thead><tbody><tr><td><code>80</code></td><td><code>nginx 1.18.0</code></td><td>Hosts a custom support web application.</td></tr><tr><td><code>443</code></td><td><code>Apache 2.4.52</code></td><td>TLS enabled; uses self-signed certificate.</td></tr><tr><td><code>22</code></td><td><code>OpenSSH 8.2p1</code></td><td>Accessible with public key authentication.</td></tr></tbody></table>

Asegúrate de que cada tabla esté claramente etiquetada con un encabezado que identifique a qué host pertenece la información.

{% hint style="success" %}
Podemos crear esta tabla a partir de un escaneo de nmap con este prompt:&#x20;

Dame una tabla en formato markdown en inglés que tenga 3 columnas, puerto, servicio y notas, del siguiente escaneo de nmap: \<pegar escaneo de nmap>
{% endhint %}

### Cuando descubres un vhost o un subdominio <a href="#when-a-virtual-host-or-subdomain-is-discovered" id="when-a-virtual-host-or-subdomain-is-discovered"></a>

Debes completar el apéndice correspondiente con los dominios previstos en el alcance del compromiso (si los hay) y aquellos que descubras durante tu prueba de penetración:

* Appendix
  * **Subdomain Discovery**

Este campo consta de una única tabla con las siguientes columnas:

<table><thead><tr><th width="191.734375">URL</th><th width="305.59765625">Description</th><th>Discovery Method</th></tr></thead><tbody><tr><td><strong>URL</strong></td><td><strong>Description</strong></td><td><strong>Discovery Method</strong></td></tr><tr><td><code>admin.target.htb</code></td><td>Administrator dashboard for the web application.</td><td>Revealed in HTML comment.</td></tr><tr><td><code>api.target.htb</code></td><td>Backend API endpoint used by frontend SPA.</td><td>Discovered via JavaScript file.</td></tr><tr><td><code>dev.target.htb</code></td><td>Development version of the main site (staging env).</td><td>Enumerated via subdomain brute-force.</td></tr><tr><td><code>monitor.target.htb</code></td><td>Internal service monitoring panel.</td><td>Enumerated via zone transfer.</td></tr></tbody></table>

{% hint style="success" %}
Podemos crear esta tabla con el siguiente promt, por ejemplo de una transferencia de zona:

Dame una tabla con estos subdominios que he descubierto por transferencia de zona, necesito 3 columnas, URL, description y discovery method: \<pegar zone transfer>
{% endhint %}

### Cuando descubres un hallazgo o "FInding" <a href="#when-a-security-finding-is-discovered" id="when-a-security-finding-is-discovered"></a>

Este es uno de los triggers más importantes y que más tiempo consume, por lo que es fundamental manejarlo correctamente. Para cada hallazgo de seguridad, debe agregar un **hallazgo o Finding** al informe.

Rellena todos los campos:

* Findings
  * **Title**
  * **CWE**
  * **CVSS**
  * **Overview**
  * **Impact**
  * **Affected Components**
  * **Recommendations**
  * **Details**
* Remediation Summary
  * **Short Term**
  * **Medium Term**
  * **Long Term**

Recuerda que cada hallazgo de seguridad debe documentarse individualmente. No agrupes varias vulnerabilidades en un solo hallazgo.

Desglosemos los campos que deberá completar:

#### Title

Para el "**Title"** , si bien puede ser difícil de crear, no hay un estándar estricto que deba seguirse. Siempre que el título sea claro y coherente, puede nombrar los hallazgos como mejor le parezca.

A continuación se muestran algunos títulos de ejemplo basados ​​en los que recopilé de las fuentes de Hack The Box que podrían inspirarte:

```
Insecure File Shares
Sensitive Data on File Shares
Unnecessary Exposed Services
Insecure Direct Object Reference (IDOR)
HTTP Verb Tampering
Unrestricted File Upload
Local File Inclusion (LFI)
Weak <APPLICATION> Admin Credentials
SQL Injection
Cross-Site Scripting (XSS)
SSRF to Local File Read
XML External Entity (XXE) Injection
Command Injection
Excessive Active Directory Group Privileges
Passwords in AD User Description Field 
Misconfigured <APPLICATION> Instance
```

Mi recomendación es que guardes cada uno por separado en la pestaña `Templates` para utilizarlo durante el examen.&#x20;

<figure><img src="/files/J1ouGaMrYi57togo1ozO" alt=""><figcaption></figcaption></figure>

#### Prompt para generar el contenido de cada Finding

Puedes crear una descripción genérica con ChatGPT y el siguiente prompt, que puedes modificar una vez que encuentres la vulnerabilidad para hacerlo más completo:

{% code title="Prompt" overflow="wrap" %}

```
Generate a comprehensive markdown report template for a penetration testing finding. The template should be in English and reusable for other vulnerabilities. Use the following structure and include detailed, professional content under each section, tailored to the specific vulnerability I provide. Include all the content in markdown formatting.

Sections required:

- Overview (From an atacker point of view)
- CWE
- CVSS (Common Vulnerability Scoring System): Include the score, vector string, and detailed breakdown as follows:
    - Score (e.g., 7.4 High)
    - Vector string (e.g., CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N)
    - Attack Vector (AV):
    - Attack Complexity (AC):
    - Privileges Required (PR):
    - User Interaction (UI):
    - Scope (S):
    - Confidentiality (C):
    - Integrity (I):
    - Availability (A):
- Technical description
- Affected components (Vulnerable domain or URL)
- Impact
- Recommendations
- Details (include examples, technical explanation, and context)
- Remediation Summary
    - Short Term Mitigation
    - Medium Term Mitigation
    - Long Term Mitigation
- Severity/Criticality Rating
- References (NIST, MITRE, OWASP Prevention Cheatsheet (if exist), GitHub exploit or PoC (if exist)...)

The vulnerability is: Sensitive Data on File Shares
```

{% endcode %}

#### CWE

Para el **CWE** , si no está seguro, puedes preguntar a ChatGPT qué CWE se ajusta a la vulnerabilidad. Luego, valide la información buscando en Google `<CWE> MITRE` y revisando la descripción.

#### CVSS

Para **CVSS** , use la calculadora CVSS integrada en SysReptor o busca una en internet. Si necesitas ayuda, ChatGPT puede ayudarte, pero asegúrate de verificar el resultado tu mismo.

#### Overview

En el campo **"Overview"** , proporciona una explicación detallada de la vulnerabilidad, tanto en general como en el contexto de su hallazgo. Evite abordar aquí el impacto o la remediación, ya que estos se abordarán en campos posteriores.

#### Impact

En la sección "**Impact"** , describe las implicaciones de seguridad de la vulnerabilidad si persiste en el entorno del cliente. Proporcione ejemplos específicos relevantes para esta instancia de la vulnerabilidad. Puede presentar esta información como un párrafo o una lista con viñetas, pero mantenga el formato uniforme en todos los hallazgos.

En el campo "**Affected Components"**, proporciona la etiqueta más pequeña que abarque todos los componentes afectados por la vulnerabilidad.

Por ejemplo:

* Si una vulnerabilidad afecta a un solo host o servicio, utiliza una etiqueta que incluya tanto el host como el servicio, si corresponde, como " `HOST01`(SMB / 139,445 TCP)". (p. ej., EternalBlue)
* Si afecta a un subdominio específico, utiliza una etiqueta como `app.target.htb`. (por ejemplo, SQLi en una aplicación web)
* Para vulnerabilidades que afecten a una subred completa o a un entorno de Active Directory, no enumeres cada host individualmente. En su lugar, utiliza una etiqueta como “`target.htb Active Directory domain`” o un rango de IP, como `10.0.0.0/8`. (p. ej., Kerberoasting).

#### **Recommendations**

En el campo **"Recommendations"** , proporciona pasos prácticos para abordar la vulnerabilidad. Nunca intentes solucionar el problema por tí mismo, por ejemplo, proporcionando una versión corregida del código. En su lugar, guíe al cliente sobre cómo resolverlo. Cada vulnerabilidad tratada en el CPTS cuenta con una sección de la Academia con sugerencias de mitigación que puedes usar como referencia al redactar recomendaciones. Puedes presentar estas acciones como un listado con bullets.

#### References

En el campo **References** , incluye enlaces a recursos relacionados con el hallazgo de seguridad. Algunas referencias útiles podrían ser:

* La página del NIST para el CVE, si corresponde, y cualquier publicación de blog relevante.
* La página MITRE para CWE, si está disponible.
* Un OWASP Prevention Cheatsheet para la vulnerabilidad, si existe alguno.
* Si utilizaste un script de prueba de concepto (PoC) que no escribiste tu mismo, proporciona un enlace.

#### Details

Por último, en el campo **"Details"** , proporciona un procedimiento paso a paso para reproducir el descubrimiento y la explotación del hallazgo, incluyendo explicaciones para cada paso. Asegúrate de incluir:

* Muchas imágenes y bloques de código para ilustrar sus puntos.
* Etiqueta claramente todas las imágenes y bloques de código.
* Resalta líneas importantes en bloques de código.
* Recorta las imágenes para mostrar sólo las partes relevantes.
* Redacta cualquier información confidencial tanto de las imágenes como de los bloques de código.
* Menciona las herramientas y scripts utilizados.

#### **Remediation Summary**

Una vez completada la sección de hallazgos, tómate un momento para completar los campos relacionados con la sección **Remediation Summary** agregando recomendaciones para abordar este hallazgo específico.

En este paso, generalmente puede copiar y pegar las acciones de remediación que sugirió en el campo Recomendación del hallazgo y distribuirlas en los campos **Short Term** , **Medium Term** y **Long Term** según corresponda.

Al finalizar el compromiso, debe tener una lista con bullets de acciones de remediación a corto, mediano y largo plazo para todos los hallazgos de seguridad que descubrió.

### Cuando obtienes acceso a un host

Una vez que logras la ejecución de comandos en un host, es momento de agregarlo a "**Exploited Hosts**" al apéndice apropiado.

También documentarás los pasos para este compromiso inicial en el **Internal Network Compromise Walkthrough**.

* Internal Network Compromise Walkthrough
  * Walkthrough Summary
  * **Detailed Walkthrough**
* Appendix
  * **Exploited Hosts**

#### **Exploited Hosts**

Para el apéndice **Exploited Hosts** , completa una tabla con las siguientes columnas para cada host:

<table><thead><tr><th width="146.078125">Columna</th><th>Explicación</th></tr></thead><tbody><tr><td>Host</td><td>El nombre y la dirección IP del host. E.j., “<code>HOST01</code> (<code>192.158.1.38</code>)”</td></tr><tr><td>Scope</td><td>Indica “<code>External</code>” o “<code>Internal</code>”, dependiendo de si el host está expuesto al exterior o si es interno (por ejemplo, en una DMZ).</td></tr><tr><td>Method</td><td>Describe el método de explotación utilizado para comprometer el host. E.j., “<code>Command injection on web application</code>.”</td></tr><tr><td>Notes</td><td>Incluye cualquier nota adicional sobre el host. E.j., “<code>Domain Controller for target.htb</code>.”</td></tr></tbody></table>

Aquí un ejemplo:

<table><thead><tr><th width="237.25390625">Host</th><th width="102.24609375">Scope</th><th>Method</th><th>Notes</th></tr></thead><tbody><tr><td><code>DC01 (192.158.1.38)</code></td><td>External</td><td>Command injection on web application.</td><td>Domain Controller for target.htb.</td></tr><tr><td><code>DMZ01 (10.0.5.14)</code></td><td>Internal</td><td>LFI to RCE via vulnerable PHP endpoint.</td><td>Hosts intranet portal.</td></tr></tbody></table>

Para el **Internal Network Compromise Walkthrough**, comience revisando el campo **Walkthrough Summary**. Realiza los ajustes necesarios y comprueba si te parece correcto. Si lo necesitas, puedes reformularlo con tus propias palabras o dejarlo como está.

#### **Detailed Walkthrough**

Para el **Detailed Walkthrough** , documentarás los pasos relacionados con el host que acabas de explotar en formato Writeup, similar a los que encontramos en la sección de Writeups de HTB:

{% content-ref url="/pages/wXx3hF51p06FSIEM44Ri" %}
[Hack the Box](/ethical-hacking-cheatsheet/writeups/hack-the-box.md)
{% endcontent-ref %}

Utiliza la siguiente estructura, que se divide en dos partes:

{% code overflow="wrap" %}

```
{{ report.candidate.a_name }} ("the tester" herein) performed the following to fully compromise the <DOMAIN> domain.
<Aquí, incluye una lista numerada con bullets donde cada punto describe un paso en la cadena de ataque.>
**Detailed reproduction steps for this attack chain are as follows:**
<Aquí se proporcionan los pasos detallados en formato writeup.>
```

{% endcode %}

En ambas partes, excluya cualquier hallazgo no relacionado con la ruta de ataque más corta para comprometer el dominio. Escriba en tercera persona, refiriéndote a tí mismo como "el pentester".

* **Bullet Point List:** Manténgala concisa y enfocada. Está bien tener varios puntos para un mismo hallazgo, pero no exagere. No incluya imágenes, bloques de código ni detalles superfluos.
* **Detailed Walkthrough:** Describa los pasos detalladamente en un documento. Sea muy descriptivo y explique cada técnica o acción en detalle, al menos una vez. Incluya abundantes imágenes y bloques de código; en caso de duda, opte por incluir demasiados en lugar de demasiados. Agregue comentarios pertinentes cuando corresponda, como reconocer la eficacia de las medidas de seguridad.

A medida que se comprometen más hosts durante el pentesting, este campo se irá llenando gradualmente, lo que dará como resultado un recorrido completo de la cadena de ataque al final.

### Cuando conseguimos root en un host <a href="#when-you-root-a-host" id="when-you-root-a-host"></a>

Una vez que hayas obtenido el privilegio local más alto en un host (root o SYSTEM), completa los siguientes campos:

* Internal Network Compromise Walkthrough
  * **Detailed Walkthrough**
* Appendix
  * **Changes/Host Cleanup**

Primero, tómate un momento para recordar todos los cambios que realizaste en el host desde que te estableciste. Esto podría incluir acciones como agregar un shell web, transferir un ejecutable, crear un usuario local, etc.

Incluso si revirtiste un cambio, como eliminar un script de PoC después de usarlo, es importante documentarlo en el informe. La transferencia podría haber generado una alerta de EDR, y el cliente necesitará saber si formó parte de la prueba de penetración o de una posible brecha de seguridad.

Después de compilar tu lista, agrega una tabla al apéndice **Changes/Host Cleanup** con las siguientes columnas:

<table><thead><tr><th width="180.10546875">Columna</th><th>Explicación</th></tr></thead><tbody><tr><td>Host</td><td>El nombre y la dirección IP del host. E.j. “<code>HOST01</code> (<code>192.158.1.38</code>)</td></tr><tr><td>Scope</td><td>Indica “<code>External</code>” o “<code>Internal</code>”, dependiendo de si el host está expuesto al exterior o si es interno (por ejemplo, en una DMZ).</td></tr><tr><td>Change/Cleanup Needed</td><td>Una descripción del cambio realizado. Si implica la creación o transferencia de un archivo, incluya el MD5 Sum. E.j. “Uploaded a web shell to <code>/var/www/html/shell.php</code>. MD5: <code>6ea3393fd7a4544d2fda0e42d7634013</code>”</td></tr></tbody></table>

Aquí un ejemplo:

#### Host 01 - example.com

<table><thead><tr><th width="223.4296875">Host</th><th width="110.171875">Scope</th><th>Change/Cleanup Needed</th></tr></thead><tbody><tr><td><code>HOST01 (192.158.1.38)</code></td><td>Internal</td><td>Uploaded a web shell to <code>/var/www/html/shell.php</code>. MD5: <code>6ea3393fd7a4544d2fda0e42d7634013</code></td></tr><tr><td><code>VPN01 (203.0.113.25)</code></td><td>External</td><td>Deployed custom scanner binary for internal recon. Remove <code>/opt/scan/recon.bin</code> post-test. MD5: <code>91a3f45723df2ef1e3a1c913c96415b</code></td></tr></tbody></table>

{% hint style="success" %}
**Nota**: Se puede obtener el MD5 Sum con el comando `md5sum shell.php`
{% endhint %}

Asegúrate de agregar un encabezado antes de la tabla para identificar a qué host se refieren los cambios.

Después de documentar los cambios, incluye los pasos para este compromiso en el campo **Detailed Walkthrough**, tanto en la lista de bullets como en la descripción detallada.

Consulta el trigger “[Cuando obtienes acceso a un host](#cuando-obtienes-acceso-a-un-host)” para obtener orientación sobre cómo estructurar este campo.

### Cuando se compromete a un usuario <a href="#when-you-compromise-a-user" id="when-you-compromise-a-user"></a>

Si hacemos técnicas de enumeración de usuarios por fuerza bruta, debemos anotar un **Finding: User Enumeration (Medium)**

Una vez que obtienes el control de un usuario, ya sea obteniendo sus contraseñas, hash NTLM o cualquier otro medio, agrega esta información al apéndice correspondiente.

* Appendix
  * **Compromised Users**

Recomiendo crear una tabla para usuarios locales y otra para cada dominio de Active Directory donde se haya comprometido a un usuario. Como alternativa, puede crear una tabla independiente para usuarios locales en cada host si le resulta más conveniente.

Las tablas deben incluir las siguientes columnas:

<table><thead><tr><th width="186.05078125">Columna</th><th>Explicación</th></tr></thead><tbody><tr><td>Username</td><td>El nombre de usuario. E.g., “<code>www-data</code>”</td></tr><tr><td>Method</td><td>El método utilizado para comprometer al usuario. E.g., “<code>Kerberoasted</code>”</td></tr><tr><td>Notes</td><td>Notas sobre el usuario. Para usuarios locales, especifica el host al que pertenecen. Si el usuario tiene un propósito específico, indícalo también. E.g., “<code>HOST01</code>’s local user for Tomcat service.”</td></tr></tbody></table>

Aquí un ejemplo:

#### Host 01 - example.com

<table><thead><tr><th width="152.328125">Username</th><th width="180.59765625">Method</th><th>Notes</th></tr></thead><tbody><tr><td><code>www-data</code></td><td>Kerberoasted</td><td><code>HOST01</code>’s local user for Tomcat service.</td></tr><tr><td><code>svc-backup</code></td><td>Password Spraying</td><td><code>HOST02</code>’s service account used for scheduled backups.</td></tr><tr><td><code>administrator</code></td><td>DCSync</td><td>Domain admin account compromised via DCSync from internal host DC01.</td></tr></tbody></table>

Como siempre, asegúrate de que las tablas estén precedidas por un encabezado que identifique el host o dominio con el que están asociadas.

### Cuando capturamos una flag <a href="#when-you-capture-a-flag" id="when-you-capture-a-flag"></a>

¡Capturaste una flag! ¡Excelente trabajo! Ahora, agrégala al apéndice correspondiente:

* Appendix
  * **Flags Discovered**

Recomiendo utilizar una sola tabla con las siguientes columnas:

<table><thead><tr><th width="177.0703125">Columna</th><th>Explicación</th></tr></thead><tbody><tr><td>Flag #</td><td>El número de la flag. Ordena las filas en orden ascendente. E.j. “1.”</td></tr><tr><td>Host</td><td>El nombre del host donde has encontrado la flag. E.g., “<code>HOST01</code>”</td></tr><tr><td>Flag Value</td><td>El valor exacto de la flag que has encontrado</td></tr><tr><td>Flag Location</td><td>Dónde has encontrado la flag. Si está en un archivo introduce la ruta completa. E.j. “<code>/root/flag.txt</code>”</td></tr><tr><td>Method Used</td><td>El método usado para llegar a la flag. E.j. “Privilege escalation via sudo rights over the <code>wget</code> binary.”</td></tr></tbody></table>

{% hint style="success" %}
En la plantilla CPTS por defecto ya tendrás preconfiguradas todas estas tablas y solo tendrás que rellenar su contenido.
{% endhint %}

### Cuando el pentesting termina <a href="#when-the-engagement-is-done" id="when-the-engagement-is-done"></a>

Al finalizar tu pentesting, si seguiste la metodología de activadores, tu informe debería estar completo en más del 90 %. Solo falta completar los campos restantes y pulirlos.

Los campos que es necesario rellenar o revisar son:

* Executive Summary
  * **Assessment Overview and Recommendations**
* Remediation Summary
  * **Short Term**
  * **Medium Term**
  * **Long Term**
* Appendix
  * **Domain Password Review**

#### **Assessment Overview and Recommendations**

hora que tiene un recorrido completo de la ruta de ataque en el campo Recorrido detallado, es momento de completar la sección **Assessment Overview and Recommendations** del Executive Summary.

En esta sección, proporcionará un resumen claro de la estrategia de ataque y las conclusiones generales de la interacción. Evite el lenguaje técnico, las viñetas y los bloques de código, ya que esta parte está dirigida a un público sin conocimientos técnicos.

Comience con un párrafo sobre su evaluación general de su postura de seguridad. Reflexione sobre los hallazgos de seguridad y lo que revelan sobre las prácticas de seguridad del cliente. Por ejemplo, si ningún ataque de robo de contraseñas tuvo éxito, elogie su sólida política de contraseñas.

Luego, escribe un párrafo para cada hallazgo de seguridad en la cadena de ataque. Explica cada vulnerabilidad en términos sencillos que cualquiera pueda entender (sin parecer condescendiente) e incluye sugerencias directas para solucionarlo.

El texto predeterminado para este campo está bien escrito, así que consérvelo e inserte su propio texto donde se indica.

Después, revise los campos de remediación **a corto plazo** , **mediano plazo** y **largo plazo** . Para este momento, debería tener acciones de remediación relacionadas con los hallazgos de seguridad específicos enumerados. Sin embargo, también es importante agregar recomendaciones que aborden la postura de seguridad general de la organización.

Por ejemplo, si muchos hallazgos se relacionan con software obsoleto con CVE conocidos, debería recomendar la revisión y mejora de sus procedimientos de actualización de software. Además, ofrezca consejos generales, como realizar auditorías de seguridad periódicas y mantenerse al día con las mejores prácticas.

Un apéndice no incluido en la plantilla SysReptor pero recomendado por el material del curso es **Domain Password Review**.

En este apéndice, se proporcionarán estadísticas sobre las contraseñas de los usuarios del dominio de Active Directory tras la vulneración y el volcado del dominio `NTDS.dit`. Las estadísticas clave que se deben incluir son:

* Number of hashes obtained
* Number of unique hashes
* Percentage of hashes cracked
* Most commonly used passwords
* Password length breakdown

Para generar estas estadísticas, recomiendo usar el script [DPAT](https://github.com/clr2of8/DPAT) de Python. Utilice las estadísticas más detalladas que proporciona y cree tablas para ellas en el apéndice.

Por último, revise su informe completo a fondo y añada los últimos retoques necesarios. Revíselo varias veces. Si tiene tiempo, tómese un descanso cuando considere que el informe está listo, consúltelo con la almohada y léalo de nuevo a la mañana siguiente con una perspectiva fresca.

¡Y ahí lo tienes, un informe completo! Envíalo y listo.

***

## <mark style="color:purple;">Conclusión</mark> <a href="#conclusion" id="conclusion"></a>

A la mayoría de los pentesters les encanta profundizar en el aspecto técnico del hacking, pero les aterra redactar el informe después. Si te interesan los aspectos técnicos de las pruebas de penetración, redactar informes para altos ejecutivos y otros profesionales del sector probablemente no sea lo tuyo.

Pero recuerde, el informe final de un trabajo, junto con otros entregables, es lo que el cliente realmente nos paga. No es solo una formalidad molesta, es la razón principal por la que nuestro cliente nos contrató.

Espero que esta publicación te ayude a escribir un excelente informe para tu intento de examen HTB CPTS.
