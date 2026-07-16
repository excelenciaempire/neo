
# Enumeración en AD

## <mark style="color:purple;">Principios de enumeración y reconocimiento externo</mark>

***

Antes de iniciar cualquier pentest, puede resultar beneficioso realizar un `reconocimiento externo` del objetivo. Esto puede cumplir muchas funciones diferentes, tales como:

* Validar la información que le proporcionó el cliente en el documento de alcance
* Asegurarse de que está tomando medidas en el ámbito adecuado cuando trabaja de forma remota
* Buscar cualquier información de acceso público que pueda afectar el resultado de su prueba, como credenciales filtradas.

Piensa en esto, de esta manera; Estamos tratando de `lay of the land`garantizar que proporcionamos la prueba más completa posible para nuestro cliente. Eso también significa identificar posibles fugas de información y datos de violación en el mundo. Esto puede ser tan simple como obtener un formato de nombre de usuario del sitio web principal o de las redes sociales del cliente.&#x20;

También podemos sumergirnos tan profundamente como escanear repositorios de GitHub en busca de credenciales dejadas en el código, buscar en documentos enlaces a una intranet o sitios accesibles remotamente, y simplemente buscar cualquier información que pueda indicarnos cómo está configurado el entorno empresarial.

***

## <mark style="color:purple;">¿Qué estamos buscando?</mark>

Al realizar nuestro reconocimiento externo, hay varios elementos clave que debemos buscar. Es posible que esta información no siempre sea de acceso público, pero sería prudente ver qué hay disponible. Si nos quedamos atascados durante una prueba de penetración, mirar hacia atrás y ver lo que se podría obtener a través del reconocimiento pasivo puede darnos el empujón necesario para seguir adelante, como datos de violación de contraseñas que podrían usarse para acceder a una VPN u otro servicio externo. La siguiente tabla destaca el " `Qué`" de lo que estaríamos buscando durante esta fase de nuestro compromiso.

<table data-header-hidden><thead><tr><th width="176"></th><th></th></tr></thead><tbody><tr><td><strong>Punto de datos</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>IP Space</code></td><td>ASN válido para nuestro objetivo, bloques de red en uso para la infraestructura pública de la organización, presencia en la nube y los proveedores de alojamiento, entradas de registros DNS, etc.</td></tr><tr><td><code>Información del dominio</code></td><td>Basado en datos de IP, DNS y registros de sitios. ¿Quién administra el dominio? ¿Hay subdominios vinculados a nuestro objetivo? ¿Hay algún servicio de dominio accesible públicamente? (Servidores de correo, DNS, sitios web, portales VPN, etc.) ¿Podemos determinar qué tipo de defensas existen? (SIEM, AV, IPS/IDS en uso, etc.)</td></tr><tr><td><code>Formato del Schema</code></td><td>¿Podemos descubrir las cuentas de correo electrónico de la organización, los nombres de usuario de AD e incluso las políticas de contraseñas? Cualquier cosa que nos brinde información que podamos usar para crear una lista de nombres de usuario válida para probar servicios externos para pulverización de contraseñas, relleno de credenciales, fuerza bruta, etc.</td></tr><tr><td><code>Data Disclosures</code></td><td>Para la divulgación de datos, buscaremos archivos de acceso público (.pdf, .ppt, .docx, .xlsx, etc.) para cualquier información que ayude a arrojar luz sobre el objetivo. Por ejemplo, cualquier archivo publicado que contenga <code>intranet</code> listados de sitios, metadatos de usuarios, recursos compartidos u otro software o hardware crítico en el entorno (credenciales enviadas a un repositorio público de GitHub, el formato de nombre de usuario interno de AD en los metadatos de un PDF, por ejemplo).</td></tr><tr><td><code>Breach Data</code></td><td>Cualquier nombre de usuario, contraseña u otra información crítica publicada públicamente que pueda ayudar a un atacante a establecerse.</td></tr></tbody></table>

## <mark style="color:purple;">¿Hacia dónde estamos mirando?</mark>

Nuestra lista de puntos de datos anterior se puede recopilar de muchas maneras diferentes. Existen muchos sitios web y herramientas diferentes que pueden proporcionarnos parte o toda la información anterior y que podríamos utilizar para obtener información vital para nuestra evaluación. La siguiente tabla enumera algunos recursos potenciales y ejemplos que se pueden utilizar.

<table data-header-hidden><thead><tr><th width="203"></th><th></th></tr></thead><tbody><tr><td><strong>Recurso</strong></td><td><strong>Ejemplos</strong></td></tr><tr><td><code>Registradores ASN/IP</code></td><td><a href="https://www.iana.org/">IANA</a> , <a href="https://www.arin.net/">arin</a> para realizar búsquedas en América, <a href="https://www.ripe.net/">RIPE</a> para realizar búsquedas en Europa, <a href="https://bgp.he.net/">BGP Toolkit</a></td></tr><tr><td><code>Registradores de Dominios y DNS</code></td><td><a href="https://www.domaintools.com/">Domaintools</a> , <a href="http://ptrarchive.com/">PTRArchive</a> , <a href="https://lookup.icann.org/lookup">ICANN</a> , solicitudes manuales de registros DNS contra el dominio en cuestión o contra servidores DNS conocidos, como <code>8.8.8.8</code>.</td></tr><tr><td><code>Redes Sociales</code></td><td>Buscar en Linkedin, Twitter, Facebook, los principales sitios de redes sociales de su región, artículos de noticias y cualquier información relevante que pueda encontrar sobre la organización.</td></tr><tr><td><code>Sitios web de empresas de cara al público</code></td><td>A menudo, el sitio web público de una corporación tendrá información relevante incorporada. Los artículos de noticias, los documentos incrustados y las páginas "Acerca de nosotros" y "Contáctenos" también pueden ser minas de oro.</td></tr><tr><td><code>Espacios de almacenamiento en la nube y desarrollo</code></td><td><a href="https://github.com/">GitHub</a> , <a href="https://grayhatwarfare.com/">depósitos de AWS S3 y contenedores de almacenamiento de Azure Blog</a> , <a href="https://www.exploit-db.com/google-hacking-database">búsquedas en Google utilizando "Dorks"</a></td></tr><tr><td><code>Fuentes de datos filtrados</code></td><td><a href="https://haveibeenpwned.com/">HaveIBeenPwned</a> para determinar si alguna cuenta de correo electrónico corporativa aparece en los datos públicos de violación, <a href="https://www.dehashed.com/">Dehashed</a> para buscar correos electrónicos corporativos con contraseñas de texto sin cifrar o hashes que podamos intentar descifrar sin conexión. Luego podemos probar estas contraseñas con cualquier portal de inicio de sesión expuesto (Citrix, RDS, OWA, 0365, VPN, VMware Horizon, aplicaciones personalizadas, etc.) que puedan usar autenticación AD.</td></tr></tbody></table>

#### Encontrar espacios de direcciones

![imagen](https://academy.hackthebox.com/storage/modules/143/bgp-toolkit.png)

El `BGP-Toolkit` alojado por [Hurricane Electric](http://he.net/) es un recurso fantástico para investigar qué bloques de direcciones se asignan a una organización y en qué ASN residen. Simplemente ingrese un dominio o dirección IP y el kit de herramientas buscará todos los resultados que pueda. Podemos aprender mucho de esta información. Muchas grandes corporaciones suelen alojar su propia infraestructura y, dado que tienen una huella tan grande, tendrán su propio ASN. Por lo general, este no será el caso de las organizaciones más pequeñas o las empresas incipientes. Mientras investiga, tenga esto en cuenta, ya que las organizaciones más pequeñas a menudo alojarán sus sitios web y otra infraestructura en el espacio de otra persona (Cloudflare, Google Cloud, AWS o Azure, por ejemplo). Comprender dónde reside esa infraestructura es extremadamente importante para nuestras pruebas. Tenemos que asegurarnos de no interactuar con infraestructura fuera de nuestro alcance. Si no tenemos cuidado al realizar un pentesting contra una organización más pequeña, podríamos terminar causando daño sin darnos cuenta a otra organización que comparte esa infraestructura. Tienes un acuerdo para realizar pruebas con el cliente, no con otros en el mismo servidor o con el proveedor. Las preguntas sobre la infraestructura autohospedada o administrada por terceros deben abordarse durante el proceso de determinación del alcance y enumerarse claramente en cualquier documento de alcance que reciba.

En algunos casos, es posible que su cliente necesite obtener la aprobación por escrito de un proveedor de alojamiento externo antes de poder realizar la prueba. Otros, como AWS, tienen [pautas](https://aws.amazon.com/security/penetration-testing/) específicas para realizar pruebas de penetración y no requieren aprobación previa para probar algunos de sus servicios. Otros, como Oracle, le solicitan que envíe una [Notificación de prueba de seguridad en la nube](https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_testing-policy_notification.htm) . Este tipo de pasos deben ser manejados por la gerencia de su empresa, el equipo legal, el equipo de contratos, etc. Si tiene dudas, intensifique la situación antes de atacar cualquier servicio externo del que no esté seguro durante una evaluación. Es nuestra responsabilidad asegurarnos de tener permiso explícito para atacar cualquier host (tanto interno como externo), y detener y aclarar el alcance por escrito nunca está de más.

#### DNS

DNS es una excelente manera de validar nuestro alcance y conocer los hosts accesibles que el cliente no reveló en su documento de alcance. Sitios como [domaintools](https://whois.domaintools.com/) y [viewdns.info](https://viewdns.info/) son excelentes lugares para comenzar. Podemos recuperar muchos registros y otros datos que van desde la resolución de DNS hasta pruebas de DNSSEC y si el sitio es accesible en países más restringidos. A veces podemos encontrar hosts adicionales fuera de alcance, pero parecen interesantes. En ese caso, podríamos llevar esta lista a nuestro cliente para ver si alguno de ellos debería incluirse en el alcance. También podemos encontrar subdominios interesantes que no figuran en los documentos de alcance, pero que residen en direcciones IP dentro del alcance y, por lo tanto, son un juego limpio.

**Viewdns.info**

![imagen](https://academy.hackthebox.com/storage/modules/143/viewdnsinfo.png)

Esta también es una excelente manera de validar algunos de los datos encontrados en nuestras búsquedas de IP/ASN. No toda la información sobre el dominio encontrado estará actualizada y realizar comprobaciones que puedan validar lo que vemos siempre es una buena práctica.

#### Datos públicos

Las redes sociales pueden ser un tesoro de datos interesantes que pueden darnos pistas sobre cómo está estructurada la organización, qué tipo de equipo opera, posibles implementaciones de software y seguridad, su esquema y más. En la parte superior de esa lista se encuentran sitios relacionados con el empleo como LinkedIn, Indeed.com y Glassdoor. Las ofertas de trabajo sencillas suelen revelar mucho sobre una empresa. Por ejemplo, eche un vistazo a la lista de trabajos a continuación. Es para un `SharePoint Administrator` y puede ayudarnos a entender muchas cosas. Podemos ver en la lista que la empresa ha estado usando SharePoint por un tiempo y tiene un programa maduro, ya que hablan de programas de seguridad, respaldo y recuperación ante desastres, y más. Lo que es interesante para nosotros en esta publicación es que podemos ver que la compañía probablemente usa SharePoint 2013 y SharePoint 2016. Eso significa que es posible que se hayan actualizado, dejando potencialmente vulnerabilidades en juego que pueden no existir en versiones más nuevas. Esto también significa que podemos encontrarnos con diferentes versiones de SharePoint durante nuestras interacciones.

#### Oferta de trabajo de administrador de Sharepoint

![imagen](https://academy.hackthebox.com/storage/modules/143/spjob2.png)

No descarte la información pública, como ofertas de trabajo o redes sociales. Se puede aprender mucho sobre una organización simplemente a partir de lo que publica, y una publicación bien intencionada podría revelar datos relevantes para nosotros como evaluadores de penetración.

Los sitios web alojados por la organización también son excelentes lugares para buscar información. Podemos recopilar correos electrónicos de contacto, números de teléfono, organigramas, documentos publicados, etc. Estos sitios, específicamente los documentos integrados, a menudo pueden tener enlaces a infraestructura interna o sitios de intranet que de otro modo no conocería. Verificar cualquier información de acceso público para ese tipo de detalles puede ser una ganancia rápida al intentar formular una imagen de la estructura del dominio.&#x20;

Con el uso cada vez mayor de sitios como GitHub, el almacenamiento en la nube de AWS y otras plataformas alojadas en la web, los datos también pueden filtrarse sin querer. Por ejemplo, un desarrollador que trabaja en un proyecto puede dejar accidentalmente algunas credenciales o notas codificadas en una versión de código. Si sabe dónde buscar esos datos, podrá obtener una ganancia fácil. Podría significar la diferencia entre tener que rociar contraseñas y credenciales de fuerza bruta durante horas o días o afianzarse rápidamente con las credenciales de desarrollador, que también pueden tener permisos elevados. Herramientas como [Trufflehog](https://github.com/trufflesecurity/truffleHog) y sitios como [Greyhat Warfare](https://buckets.grayhatwarfare.com/) son recursos fantásticos para encontrar estas rutas de navegación.

Hemos dedicado algún tiempo a discutir la enumeración externa y el reconocimiento de una organización, pero esto es sólo una pieza del rompecabezas. Para obtener una introducción más detallada a OSINT y la enumeración externa, consulte los módulos [Footprinting](https://academy.hackthebox.com/course/preview/footprinting) y [OSINT:Corporate Recon](https://academy.hackthebox.com/course/preview/osint-corporate-recon) .

Hasta este punto, hemos sido mayormente pasivos en nuestras discusiones. A medida que avance en el pentest, será más práctico, validará la información que ha encontrado y explorará el dominio para obtener más información. Dediquemos un minuto a analizar los principios de enumeración y cómo podemos implementar un proceso para realizar estas acciones.

***

## <mark style="color:purple;">Principios generales de enumeración</mark>

Teniendo en cuenta que nuestro objetivo es comprender mejor a nuestro objetivo, buscamos todas las vías posibles que podamos encontrar que nos proporcionen una ruta potencial hacia el interior. La enumeración en sí es un proceso iterativo que repetiremos varias veces durante una prueba de penetración.&#x20;

Además del documento de alcance del cliente, esta es nuestra principal fuente de información, por lo que queremos asegurarnos de no dejar ningún cabo sin remover. Al comenzar nuestra enumeración, primero usaremos recursos `pasivos`, comenzando con un alcance amplio y reduciéndolos. Una vez que agotemos nuestra ejecución inicial de enumeración pasiva, necesitaremos examinar los resultados y luego pasar a nuestra fase de enumeración activa.

***

### Ejemplo de proceso de enumeración

Ya hemos cubierto bastantes conceptos relacionados con la enumeración. Empecemos a juntarlo todo. Practicaremos nuestras tácticas de enumeración en el dominio `inlanefreight.com` sin realizar análisis intensivos (como Nmap o análisis de vulnerabilidades que están fuera de alcance). Primero comenzaremos verificando nuestros datos de Netblocks y viendo qué podemos encontrar.

**VerificarASN/IP y datos de dominio**

![imagen](https://academy.hackthebox.com/storage/modules/143/BGPhe-inlane.png)

De este primer vistazo, ya hemos obtenido información interesante. BGP.he está informando:

* Dirección IP: `134.209.24.248`
* Servidor de correo: `mail1.inlanefreight.com`
* Servidores de nombres: `NS1.inlanefreight.com` y `NS2.inlanefreight.com`

Por ahora, esto es lo que nos importa de su producción. Inlanefreight no es una gran corporación, por lo que no esperábamos encontrar que tuviera su propio ASN. Ahora validemos parte de esta información.

#### **Resultados de Viewdns**

![imagen](https://academy.hackthebox.com/storage/modules/143/viewdns-results.png)

En la solicitud anterior, utilizamos `viewdns.info` para validar la dirección IP de nuestro objetivo. Ambos resultados coinciden, lo cual es una buena señal. Ahora intentemos otra ruta para validar los dos servidores de nombres en nuestros resultados.

```shell-session
afsh4ck@kali$ nslookup ns1.inlanefreight.com

Server:		192.168.186.1
Address:	192.168.186.1#53

Non-authoritative answer:
Name:	ns1.inlanefreight.com
Address: 178.128.39.165

nslookup ns2.inlanefreight.com
Server:		192.168.86.1
Address:	192.168.86.1#53

Non-authoritative answer:
Name:	ns2.inlanefreight.com
Address: 206.189.119.186 
```

Ahora tenemos `dos` nuevas direcciones IP para agregar a nuestra lista para validación y prueba. Antes de tomar cualquier otra medida con ellos, asegúrese de que estén dentro del alcance de su prueba. Para nuestros propósitos, las direcciones IP reales no estarían dentro del alcance del escaneo, pero podríamos navegar pasivamente por cualquier sitio web para buscar datos interesantes. Por ahora, eso es todo con la enumeración de información de dominio de DNS. Echemos un vistazo a la información disponible públicamente.

Inlanefreight es una empresa ficticia que utilizamos para este módulo, por lo que no hay presencia real en las redes sociales. Sin embargo, buscaríamos información útil en sitios como LinkedIn, Twitter, Instagram y Facebook si fuera real. En su lugar, pasaremos a examinar el sitio web `inlanefreight.com`.

La primera comprobación que hicimos fue buscar documentos. Usando `filetype:pdf inurl:inlanefreight.com`como búsqueda, buscamos archivos PDF.

#### **Buscando archivos con Google Dorks**

![imagen](https://academy.hackthebox.com/storage/modules/143/google-dorks.png)

Apareció un documento, por lo que debemos asegurarnos de anotar el documento y su ubicación y descargar una copia localmente para explorar. Siempre es mejor guardar archivos, capturas de pantalla, resultados de escaneo, resultados de herramientas, etc., tan pronto como los encontremos o los generemos. Esto nos ayuda a mantener un registro lo más completo posible y no correr el riesgo de olvidar dónde vimos algo o perder datos críticos. A continuación, busquemos las direcciones de correo electrónico que podamos encontrar.

**Buscando direcciones de correo electrónico**

![imagen](https://academy.hackthebox.com/storage/modules/143/intext-dork.png)

Usando dork `intext:"@inlanefreight.com" inurl:inlanefreight.com`, buscamos cualquier instancia que parezca similar al final de una dirección de correo electrónico en el sitio web. Un resultado prometedor fue la creación de una página de contacto. Cuando miramos la página (que se muestra a continuación), podemos ver una lista grande de empleados e información de contacto de ellos. Esta información puede ser útil ya que podemos determinar que al menos estas personas probablemente estén activas y sigan trabajando con la empresa.

#### **Enviar resultados por correo electrónico**

Navegando por la [página de contacto](https://www.inlanefreight.com/index.php/contact/) , podemos ver varios correos electrónicos del personal de diferentes oficinas alrededor del mundo. Ahora tenemos una idea de su convención de nomenclatura de correo electrónico (primero.último) y dónde trabajan algunas personas en la organización. Esto podría ser útil en ataques posteriores de pulverización de contraseñas o si la ingeniería social/phishing fuera parte de nuestro alcance.

![imagen](https://academy.hackthebox.com/storage/modules/143/ilfreightemails.png)

#### **Recopilación de nombres de usuario**

Podemos utilizar una herramienta como [linkedin2username](https://github.com/initstring/linkedin2username) para extraer datos de la página de LinkedIn de una empresa y crear varias combinaciones de nombres de usuario (`flast`, `first.last`, `f.last`, etc.) que se pueden agregar a nuestra lista de posibles objetivos de pulverización de contraseñas.

**Búsqueda de credenciales**

[Dehashed](http://dehashed.com/) es una excelente herramienta para buscar credenciales de texto sin cifrar y hashes de contraseñas en datos violados. Podemos buscar en el sitio o usando un script que realiza consultas a través de la API. Normalmente encontraremos muchas contraseñas antiguas para usuarios que no funcionan en portales externos que usan autenticación AD (o interna), ¡pero podemos tener suerte! Esta es otra herramienta que puede resultar útil para crear una lista de usuarios para la pulverización de contraseñas internas o externas.

{% hint style="info" %}
**Nota**: Para nuestros propósitos, los datos de muestra a continuación son ficticios.
{% endhint %}

```shell-session
afsh4ck@kali$ sudo python3 dehashed.py -q inlanefreight.local -p

id : 5996447501
email : roger.grimes@inlanefreight.local
username : rgrimes
password : Ilovefishing!
hashed_password : 
name : Roger Grimes
vin : 
address : 
phone : 
database_name : ModBSolutions

id : 7344467234
email : jane.yu@inlanefreight.local
username : jyu
password : Starlight1982_!
hashed_password : 
name : Jane Yu
vin : 
address : 
phone : 
database_name : MyFitnessPal

<SNIP>
```

Ahora que ya dominamos esto, intente buscar otros resultados relacionados con el dominio inlanefreight.com. ¿Qué puedes encontrar? ¿Hay otros archivos, páginas o información útiles integrados en el sitio? Esta sección demostró la importancia de analizar exhaustivamente nuestro objetivo, siempre que nos mantengamos dentro del alcance y no probemos nada a lo que no estemos autorizados y nos mantengamos dentro de las limitaciones de tiempo del compromiso.&#x20;

He tenido bastantes evaluaciones en las que estaba teniendo problemas para afianzarme desde un punto de vista anónimo en la red interna y recurrí a la creación de una lista de palabras utilizando diversas fuentes externas (Google, LinkedIn scraping, Dehashed, etc.) y luego realicé una contraseña interna específica. rociar para obtener credenciales válidas para una cuenta de usuario de dominio estándar. Como veremos en las siguientes secciones, podemos realizar la gran mayoría de nuestra enumeración interna de AD con solo un conjunto de credenciales de usuario de dominio con bajos privilegios e incluso muchos ataques. La diversión comienza una vez que tenemos un conjunto de credenciales. Pasemos a la enumeración interna y comencemos a analizar el `INLANEFREIGHT.LOCAL`dominio interno de forma pasiva y activa según el alcance y las reglas de participación de nuestra evaluación.
