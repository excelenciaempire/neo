
# Recopilación Pasiva

{% hint style="success" %}
**Nota:** Este tipo de búsquedas no son invasivas, ya que no hacen peticiones al servidor del objetivo, por lo que podemos utilizar estas técnicas libremente.
{% endhint %}

## Herramientas útiles

### <mark style="color:purple;">Whois</mark>

Whois es un protocolo de red utilizado para buscar información sobre un dominio, una dirección IP o un bloque de direcciones IP en una base de datos pública. La información que se puede obtener a través de una consulta Whois incluye el nombre del propietario del dominio, la información de contacto, la fecha de registro, la fecha de vencimiento y los servidores de nombres de dominio asociados.

<pre class="language-shell-session"><code class="lang-shell-session"><strong>whois tesla.com
</strong><strong>   Domain Name: TESLA.COM
</strong>   Registry Domain ID: 187902_DOMAIN_COM-VRSN
   Registrar WHOIS Server: whois.markmonitor.com
   Registrar URL: http://www.markmonitor.com
   Updated Date: 2022-10-02T09:36:05Z
   Creation Date: 1992-11-04T05:00:00Z
   Registry Expiry Date: 2024-11-03T06:00:00Z
   Registrar: MarkMonitor Inc.
   Registrar IANA ID: 292
   Registrant Name: Domain Administrator
   Registrant Organization: DNStination Inc.
   Registrant Street: 3450 Sacramento Street, Suite 405
   Registrant City: San Francisco
   Registrant State/Province: CA
   Registrant Postal Code: 94118
   Registrant Country: US
   Registrant Phone: +1.4155319335
   Registrant Phone Ext: 
   Registrant Fax: +1.4155319336
   Registrant Fax Ext: 
   Registrant Email: admin@dnstinations.com
   Registry Admin ID: 
   Admin Name: Domain Administrator
   Admin Organization: DNStination Inc.
   Admin Street: 3450 Sacramento Street, Suite 405
   Admin City: San Francisco
   Admin State/Province: CA
   Admin Postal Code: 94118
   Admin Country: US
   Admin Phone: +1.4155319335
   Admin Phone Ext: 
   Admin Fax: +1.4155319336
   Admin Fax Ext: 
   Admin Email: admin@dnstinations.com
</code></pre>

### <mark style="color:purple;">Nslookup y Dig</mark>

Supongamos que un cliente nos solicitó realizar una prueba de penetración externa. Por lo tanto, primero debemos familiarizarnos con su infraestructura e identificar qué hosts son de acceso público. Esto lo podemos averiguar utilizando diferentes tipos de solicitudes DNS. Con `Nslookup`, podemos buscar servidores de nombres de dominio en Internet y pedirles información sobre hosts y dominios. Aunque la herramienta tiene dos modos, interactivo y no interactivo, nos centraremos principalmente en el módulo `no interactivo`.

Podemos consultar registros `A` simplemente enviando un nombre de dominio. Pero también podemos usar el parámetro `-query` para buscar registros de recursos específicos. Algunos ejemplos son:

**Consulta: CUALQUIER registro existente**

En este ejemplo, utilizamos Google como ejemplo en lugar de Facebook, ya que el último no respondió a nuestra consulta.

```bash
afsh4ck$ export TARGET="google.com"
afsh4ck$ nslookup -query=ANY $TARGET

Server:		10.100.0.1
Address:	10.100.0.1#53

Non-authoritative answer:
Name:	google.com
Address: 172.217.16.142
Name:	google.com
Address: 2a00:1450:4001:808::200e
google.com	text = "docusign=05958488-4752-4ef2-95eb-aa7ba8a3bd0e"
google.com	text = "docusign=1b0a6754-49b1-4db5-8540-d2c12664b289"
google.com	text = "v=spf1 include:_spf.google.com ~all"
google.com	text = "MS=E4A68B9AB2BB9670BCE15412F62916164C0B20BB"
google.com	text = "globalsign-smime-dv=CDYX+XFHUw2wml6/Gb8+59BsH31KzUr6c1l2BPvqKX8="
google.com	text = "apple-domain-verification=30afIBcvSuDV2PLX"
google.com	text = "google-site-verification=wD8N7i1JTNTkezJ49swvWW48f8_9xveREV4oB-0Hf5o"
google.com	text = "facebook-domain-verification=22rm551cu4k0ab0bxsw536tlds4h95"
google.com	text = "google-site-verification=TV9-DBe4R80X4v0M4U_bd_J9cpOJM0nikft0jAgjmsQ"
google.com	nameserver = ns3.google.com.
google.com	nameserver = ns2.google.com.
google.com	nameserver = ns1.google.com.
google.com	nameserver = ns4.google.com.
google.com	mail exchanger = 10 aspmx.l.google.com.
google.com	mail exchanger = 40 alt3.aspmx.l.google.com.
google.com	mail exchanger = 20 alt1.aspmx.l.google.com.
google.com	mail exchanger = 30 alt2.aspmx.l.google.com.
google.com	mail exchanger = 50 alt4.aspmx.l.google.com.
google.com
	origin = ns1.google.com
	mail addr = dns-admin.google.com
	serial = 398195569
	refresh = 900
	retry = 900
	expire = 1800
	minimum = 60
google.com	rdata_257 = 0 issue "pki.goog"

Authoritative answers can be found from:
```

```bash
afsh4ck$ dig any google.com @8.8.8.8

; <<>> DiG 9.16.1-Ubuntu <<>> any google.com @8.8.8.8
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 49154
;; flags: qr rd ra; QUERY: 1, ANSWER: 22, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;google.com.                    IN      ANY

;; ANSWER SECTION:
google.com.             249     IN      A       142.250.184.206
google.com.             249     IN      AAAA    2a00:1450:4001:830::200e
google.com.             549     IN      MX      10 aspmx.l.google.com.
google.com.             3549    IN      TXT     "apple-domain-verification=30afIBcvSuDV2PLX"
google.com.             3549    IN      TXT     "facebook-domain-verification=22rm551cu4k0ab0bxsw536tlds4h95"
google.com.             549     IN      MX      20 alt1.aspmx.l.google.com.
google.com.             3549    IN      TXT     "docusign=1b0a6754-49b1-4db5-8540-d2c12664b289"
google.com.             3549    IN      TXT     "v=spf1 include:_spf.google.com ~all"
google.com.             3549    IN      TXT     "globalsign-smime-dv=CDYX+XFHUw2wml6/Gb8+59BsH31KzUr6c1l2BPvqKX8="
google.com.             3549    IN      TXT     "google-site-verification=wD8N7i1JTNTkezJ49swvWW48f8_9xveREV4oB-0Hf5o"
google.com.             9       IN      SOA     ns1.google.com. dns-admin.google.com. 403730046 900 900 1800 60
google.com.             21549   IN      NS      ns1.google.com.
google.com.             21549   IN      NS      ns3.google.com.
google.com.             549     IN      MX      50 alt4.aspmx.l.google.com.
google.com.             3549    IN      TXT     "docusign=05958488-4752-4ef2-95eb-aa7ba8a3bd0e"
google.com.             549     IN      MX      30 alt2.aspmx.l.google.com.
google.com.             21549   IN      NS      ns2.google.com.
google.com.             21549   IN      NS      ns4.google.com.
google.com.             549     IN      MX      40 alt3.aspmx.l.google.com.
google.com.             3549    IN      TXT     "MS=E4A68B9AB2BB9670BCE15412F62916164C0B20BB"
google.com.             3549    IN      TXT     "google-site-verification=TV9-DBe4R80X4v0M4U_bd_J9cpOJM0nikft0jAgjmsQ"
google.com.             21549   IN      CAA     0 issue "pki.goog"

;; Query time: 16 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mo Okt 18 16:15:22 CEST 2021
;; MSG SIZE  rcvd: 922
```

### <mark style="color:purple;">The Harvester</mark>

The Harvester es una herramienta de búsqueda de información que se utiliza en pruebas de penetración y en hacking ético para recopilar información sobre un objetivo. The Harvester puede buscar información en una variedad de fuentes, incluyendo motores de búsqueda, redes sociales, sitios web públicos y más. Viene instalado por defecto en Kali Linux.

{% embed url="<https://github.com/laramies/theHarvester>" %}

```bash
theHarvester -h
```

```bash
theHarvester -d facebook.com -l 400 -b all
```

En la siguiente sección veremos esta herramienta en detalle:

{% content-ref url="/pages/7Bwxmq5INs5YpamqjP3t" %}
[Subdominios - Pasiva](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-pasiva/subdominios-pasiva.md)
{% endcontent-ref %}

### <mark style="color:purple;">Shodan</mark>

Shodan es un motor de búsqueda especializado en dispositivos conectados a Internet, como cámaras de seguridad, routers, servidores y otros dispositivos IoT (Internet de las cosas). A diferencia de los motores de búsqueda convencionales, Shodan no indexa sitios web, sino que escanea y recopila información sobre los dispositivos conectados a Internet.

En Kali Linux, se puede utilizar Shodan para buscar dispositivos conectados a Internet y obtener información sobre ellos. Para utilizar Shodan en Kali Linux, se deben seguir los siguientes pasos:

1. Crear una cuenta en Shodan. Se puede hacer en su sitio web oficial: <https://www.shodan.io/>.
2. Obtener la API key de Shodan. Para ello, se debe ingresar a la cuenta de Shodan y navegar a la sección "API Access".
3. Instalar la herramienta de línea de comandos "shodan" en Kali Linux. Para ello, se puede utilizar el siguiente comando: sudo apt-get install shodan.
4. Configurar la API key de Shodan en la herramienta "shodan" utilizando el siguiente comando: shodan init \[API key de Shodan].

Algunos ejemplos de cómo usar Shodan:

{% code overflow="wrap" %}

```markup
shodan search [término de búsqueda]: busca dispositivos conectados a Internet que coinciden con el término de búsqueda especificado.

shodan host [dirección IP]: muestra información detallada sobre un dispositivo conectado a Internet específico.

shodan stats [término de búsqueda]: muestra estadísticas sobre los resultados de búsqueda para el término de búsqueda especificado.
```

{% endcode %}

### <mark style="color:purple;">Maltego</mark>

Maltego es una herramienta de inteligencia de código abierto que se utiliza en pruebas de penetración y en hacking ético para recopilar y analizar información sobre un objetivo. Maltego utiliza una interfaz gráfica de usuario intuitiva para visualizar y analizar la información recopilada, lo que lo hace especialmente útil para analizar grandes cantidades de datos y descubrir relaciones entre ellos. Viene instalado por defecto en Kali Linux.

Una vez que se ha instalado Maltego, se puede utilizar para recopilar y analizar información sobre un objetivo. Para utilizar Maltego, se deben seguir los siguientes pasos:

1. Abrir Maltego desde el menú de aplicaciones de Kali Linux.
2. Seleccionar el tipo de entidad que se desea buscar, como un nombre de dominio, una dirección IP o una dirección de correo electrónico.
3. Ingresar el valor de la entidad y hacer clic en "Siguiente".
4. Seleccionar las transformaciones que se desean aplicar a la entidad y hacer clic en "Ejecutar".
5. Analizar los resultados de las transformaciones y buscar relaciones entre las entidades.

Maltego también permite integrar diferentes fuentes de información, como Shodan, Facebook, Twitter, LinkedIn y más, lo que lo hace especialmente útil para descubrir relaciones entre diferentes entidades.

### <mark style="color:purple;">ReconNG</mark>

Recon-ng es una herramienta de reconocimiento de código abierto diseñada para automatizar la recopilación de información en pruebas de penetración y en hacking ético. Recon-ng utiliza una interfaz de línea de comandos y una arquitectura modular que permite a los usuarios personalizar y extender fácilmente la funcionalidad de la herramienta. Viene instalado por defecto en Kali Linux.

* `recon-ng`: Inicia la herramienta Recon-ng.
* `help`: Muestra una lista de comandos y opciones disponibles.
* `show modules`: Muestra una lista de módulos disponibles.
* `use [nombre del módulo]`: Selecciona un módulo específico.
* `show info`: Muestra información sobre el módulo seleccionado.
* `show options`: Muestra las opciones disponibles para el módulo seleccionado.
* `set [opción][valor]`: Configura las opciones del módulo.
* `run`: Ejecuta el módulo con las opciones configuradas.
* `back`: Vuelve al menú principal.
* `exit`: Sale de Recon-ng.

Algunos ejemplos de módulos que se pueden utilizar en Recon-ng son:

* `recon/domains-hosts/bing_domain_web`: Busca nombres de host y direcciones IP relacionadas con un dominio utilizando Bing.
* `recon/domains-hosts/google_site_web`: Busca nombres de host y direcciones IP relacionadas con un dominio utilizando Google.
* `recon/profiles-hosts/shodan_api`: Busca dispositivos conectados a Internet utilizando la API de Shodan.
* `recon/hosts-hosts/ipinfodb`: Busca información de geolocalización de direcciones IP utilizando la API de IPInfoDB.

### <mark style="color:purple;">GitLeaks</mark>

Sirve para identificar filtraciones en un repositorio publico, por ejemplo de alguna organización que estemos auditando

{% embed url="<https://github.com/gitleaks/gitleaks>" %}

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ git clone https://github.com/gitleaks/gitleaks.git
</strong>afsh4ck@kali$ cd gitleaks
afsh4ck@kali$ gitleaks detect -v
</code></pre>
