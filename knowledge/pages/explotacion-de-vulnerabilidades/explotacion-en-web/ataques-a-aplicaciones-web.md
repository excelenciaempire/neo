
# Ataques a Aplicaciones Web

Las aplicaciones web son comunes en la mayoría de los entornos, si no en todos, en los que nos encontramos como pentesters. Durante nuestras evaluaciones, nos encontraremos con una amplia variedad de aplicaciones web, como sistemas de gestión de contenido (CMS), aplicaciones web personalizadas, portales de intranet utilizados por desarrolladores y administradores de sistemas, repositorios de código, herramientas de monitorización de red, sistemas de tickets, wikis, bases de conocimiento, rastreadores de problemas, aplicaciones de contenedores de servlets y más. Es habitual encontrar las mismas aplicaciones en muchos entornos diferentes. Si bien una aplicación puede no ser vulnerable en un entorno, puede estar mal configurada o sin parches en el siguiente. Un evaluador debe tener un conocimiento sólido de cómo enumerar y atacar las aplicaciones comunes que se tratan en este módulo.

Las aplicaciones web son aplicaciones interactivas a las que se puede acceder a través de navegadores web. Las aplicaciones web suelen adoptar una arquitectura cliente-servidor para ejecutarse y gestionar las interacciones. Suelen estar formadas por componentes front-end (la interfaz del sitio web o "lo que ve el usuario") que se ejecutan en el lado del cliente (navegador) y otros componentes back-end (código fuente de la aplicación web) que se ejecutan en el lado del servidor (servidor back-end/bases de datos).

Todos los tipos de aplicaciones web (comerciales, de código abierto y personalizadas) pueden sufrir los mismos tipos de vulnerabilidades y configuraciones incorrectas, a saber, los 10 principales riesgos de las aplicaciones web cubiertos en el [Top 10 de OWASP](https://owasp.org/www-project-top-ten/) . Si bien podemos encontrar versiones vulnerables de muchas aplicaciones comunes que sufren vulnerabilidades conocidas (públicas), como inyección SQL, XSS, errores de ejecución de código remoto, lectura de archivos locales y carga de archivos sin restricciones, es igualmente importante para nosotros comprender cómo podemos abusar de la funcionalidad incorporada de muchas de estas aplicaciones para lograr la ejecución remota de código.

***

## <mark style="color:purple;">Datos de la aplicación</mark>

En este módulo se estudiarán en profundidad varias aplicaciones comunes y se abordarán brevemente otras menos comunes (pero que se ven a menudo). Algunas de las categorías de aplicaciones que podemos encontrar durante una evaluación determinada y que podemos aprovechar para ganar terreno o acceder a datos confidenciales incluyen:

<table data-header-hidden><thead><tr><th width="340"></th><th></th></tr></thead><tbody><tr><td><strong>Categoria</strong></td><td><strong>Aplicación</strong></td></tr><tr><td><a href="https://enlyft.com/tech/web-content-management">Web Content Management</a></td><td>Joomla, Drupal, WordPress, DotNetNuke, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/application-servers">Application Servers</a></td><td>Apache Tomcat, Phusion Passenger, Oracle WebLogic, IBM WebSphere, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/security-information-and-event-management-siem">Security Information and Event Management (SIEM)</a></td><td>Splunk, Trustwave, LogRhythm, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/network-management">Network Management</a></td><td>PRTG Network Monitor, ManageEngine Opmanger, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/it-management-software">IT Management</a></td><td>Nagios, Puppet, Zabbix, ManageEngine ServiceDesk Plus, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/software-frameworks">Software Frameworks</a></td><td>JBoss, Axis2, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/customer-service-management">Customer Service Management</a></td><td>osTicket, Zendesk, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/search-engines">Search Engines</a></td><td>Elasticsearch, Apache Solr, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/software-configuration-management">Software Configuration Management</a></td><td>Atlassian JIRA, GitHub, GitLab, Bugzilla, Bugsnag, Bitbucket, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/software-development-tools">Software Development Tools</a></td><td>Jenkins, Atlassian Confluence, phpMyAdmin, etc.</td></tr><tr><td><a href="https://enlyft.com/tech/enterprise-application-integration">Enterprise Application Integration</a></td><td>Oracle Fusion Middleware, BizTalk Server, Apache ActiveMQ, etc.</td></tr></tbody></table>

Como puede ver al navegar por los enlaces de cada categoría anterior, existen [miles de aplicaciones](https://enlyft.com/tech/) que podemos encontrar durante una evaluación determinada. Muchas de ellas sufren vulnerabilidades conocidas públicamente o tienen funciones que se pueden aprovechar para obtener ejecución remota de código, robar credenciales o acceder a información confidencial con o sin credenciales válidas. Este módulo cubrirá las aplicaciones más frecuentes que vemos repetidamente durante las evaluaciones internas y externas.

Echemos un vistazo al sitio web de Enlyft. Podemos ver, por ejemplo, que pudieron recopilar datos sobre más de 3,7 millones de empresas que utilizan [WordPress](https://enlyft.com/tech/products/wordpress) , lo que representa casi el 70 % de la cuota de mercado mundial de aplicaciones de gestión de contenido web para todas las empresas encuestadas. En el caso de la herramienta SIEM, [Splunk](https://enlyft.com/tech/products/splunk) fue utilizada por 22 174 de las empresas encuestadas y representó casi el 30 % de la cuota de mercado de herramientas SIEM. Si bien las demás aplicaciones que cubriremos representan una cuota de mercado mucho menor para su respectiva categoría, aún las veo a menudo y las habilidades aprendidas aquí se pueden aplicar a muchas situaciones diferentes.

***

## <mark style="color:purple;">Aplicaciones comunes</mark>

Normalmente me encuentro con al menos una de las aplicaciones que se indican a continuación, que abordaremos en profundidad en las secciones del módulo. Si bien no podemos cubrir todas las posibles aplicaciones que podemos encontrar, las habilidades que se enseñan en este módulo nos prepararán para abordar todas las aplicaciones con un ojo crítico y evaluarlas en busca de vulnerabilidades públicas y configuraciones incorrectas.

<table data-header-hidden><thead><tr><th width="127"></th><th></th></tr></thead><tbody><tr><td>Aplicación</td><td>Descripción</td></tr><tr><td>WordPress</td><td><a href="https://wordpress.org/">WordPress</a> es un sistema de gestión de contenido (CMS) de código abierto que se puede utilizar para múltiples propósitos. A menudo se utiliza para alojar blogs y foros. WordPress es altamente personalizable y compatible con SEO, lo que lo hace popular entre las empresas. Sin embargo, su capacidad de personalización y naturaleza extensible lo hacen propenso a vulnerabilidades a través de temas y complementos de terceros. WordPress está escrito en PHP y generalmente se ejecuta en Apache con MySQL como backend.</td></tr><tr><td>Drupal</td><td><a href="https://www.drupal.org/">Drupal</a> es otro CMS de código abierto muy popular entre empresas y desarrolladores. Drupal está escrito en PHP y admite el uso de MySQL o PostgreSQL para el backend. Además, se puede utilizar SQLite si no hay un DBMS instalado. Al igual que WordPress, Drupal permite a los usuarios mejorar sus sitios web mediante el uso de temas y módulos.</td></tr><tr><td>Joomla</td><td><a href="https://www.joomla.org/">Joomla</a> es otro CMS de código abierto escrito en PHP que normalmente utiliza MySQL pero que puede ejecutarse con PostgreSQL o SQLite. Joomla se puede utilizar para blogs, foros de debate, comercio electrónico y más. Joomla se puede personalizar en gran medida con temas y extensiones y se estima que es el tercer CMS más utilizado en Internet después de WordPress y Shopify.</td></tr><tr><td>Apache Tomcat</td><td><a href="https://tomcat.apache.org/">Apache Tomcat</a> es un servidor web de código abierto que aloja aplicaciones escritas en Java. Tomcat fue diseñado inicialmente para ejecutar servlets de Java y scripts de Java Server Pages (JSP). Sin embargo, su popularidad aumentó con los frameworks basados ​​en Java y ahora es ampliamente utilizado por frameworks como Spring y herramientas como Gradle.</td></tr><tr><td>Jenkins</td><td><a href="https://jenkins.io/">Jenkins</a> es un servidor de automatización de código abierto escrito en Java que ayuda a los desarrolladores a crear y probar sus proyectos de software de forma continua. Es un sistema basado en servidor que se ejecuta en contenedores de servlets como Tomcat. A lo largo de los años, los investigadores han descubierto varias vulnerabilidades en Jenkins, incluidas algunas que permiten la ejecución remota de código sin necesidad de autenticación.</td></tr><tr><td>Splunk</td><td>Splunk es una herramienta de análisis de registros que se utiliza para recopilar, analizar y visualizar datos. Aunque originalmente no estaba pensada para ser una herramienta SIEM, Splunk se utiliza a menudo para la supervisión de la seguridad y el análisis empresarial. Las implementaciones de Splunk se utilizan a menudo para almacenar datos confidenciales y podrían proporcionar una gran cantidad de información a un atacante si se ven comprometidas. Históricamente, Splunk no ha sufrido una cantidad considerable de vulnerabilidades conocidas aparte de una vulnerabilidad de divulgación de información ( <a href="https://nvd.nist.gov/vuln/detail/CVE-2018-11409">CVE-2018-11409</a> ) y una vulnerabilidad de ejecución remota de código autenticado en versiones muy antiguas ( <a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-4642">CVE-2011-4642</a> ).</td></tr><tr><td>PRTG Network Monitor</td><td><a href="https://www.paessler.com/prtg">PRTG Network Monitor</a> es un sistema de monitoreo de red sin agente que se puede utilizar para monitorear métricas como el tiempo de actividad, el uso del ancho de banda y más desde una variedad de dispositivos como enrutadores, conmutadores, servidores, etc. Utiliza un modo de detección automática para escanear una red y luego aprovecha protocolos como ICMP, WMI, SNMP y NetFlow para comunicarse con los dispositivos detectados y recopilar datos de ellos. PRTG está escrito en <a href="https://en.wikipedia.org/wiki/Delphi_(software)">Delphi</a> .</td></tr><tr><td>osTicket</td><td><a href="https://osticket.com/">osTicket</a> es un sistema de tickets de soporte de código abierto ampliamente utilizado. Se puede utilizar para gestionar tickets de servicio al cliente recibidos por correo electrónico, teléfono y la interfaz web. osTicket está escrito en PHP y puede ejecutarse en Apache o IIS con MySQL como backend.</td></tr><tr><td>GitLab</td><td><a href="https://about.gitlab.com/">GitLab</a> es una plataforma de desarrollo de software de código abierto con un administrador de repositorios Git, control de versiones, seguimiento de problemas, revisión de código, integración y despliegue continuos, y más. Originalmente se escribió en Ruby, pero ahora utiliza Ruby on Rails, Go y Vue.js. GitLab ofrece versiones del software tanto para la comunidad (gratuitas) como para empresas.</td></tr></tbody></table>

***

## <mark style="color:purple;">Objetivos del módulo</mark>

A lo largo de las secciones del módulo, haremos referencia a direcciones URL como `http://app.inlanefreight.local`. Para simular un entorno grande y realista con varios servidores web, utilizamos Vhosts para alojar las aplicaciones web. Dado que todos estos Vhosts se asignan a un directorio diferente en el mismo host, tenemos que realizar entradas manuales en nuestro archivo `/etc/hosts` en la máquina virtual de ataque local para interactuar con el laboratorio. Esto debe hacerse para cualquier ejemplo que muestre escaneos o capturas de pantalla utilizando un FQDN. Las secciones como Splunk que solo utilizan la dirección IP del objetivo generado no requerirán una entrada en el archivo de hosts, y puede interactuar simplemente con la dirección IP generada y el puerto asociado.

Para hacer esto rápidamente, podríamos ejecutar lo siguiente:

```shell-session
afsh4ck@kali$ IP=10.129.42.195
afsh4ck@kali$ printf "%s\t%s\n\n" "$IP" "app.inlanefreight.local dev.inlanefreight.local blog.inlanefreight.local" | sudo tee -a /etc/hosts
```

Después de este comando, nuestro archivo `/etc/hosts` se vería así:

```bash
afsh4ck@kali$ cat /etc/hosts

# Your system has configured 'manage_etc_hosts' as True.
# As a result, if you wish for changes to this file to persist
# then you will need to either
# a.) make changes to the master file in /etc/cloud/templates/hosts.debian.tmpl
# b.) change or remove the value of 'manage_etc_hosts' in
#     /etc/cloud/cloud.cfg or cloud-config from user-data
#
127.0.1.1 htb-9zftpkslke.htb-cloud.com htb-9zftpkslke
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts

10.129.42.195	app.inlanefreight.local dev.inlanefreight.local blog.inlanefreight.local
```
