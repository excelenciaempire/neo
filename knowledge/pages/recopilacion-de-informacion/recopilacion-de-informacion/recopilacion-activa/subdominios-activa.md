
# Subdominios - Activa

## <mark style="color:purple;">Enumeración activa de subdominios</mark>

Podemos realizar una enumeración activa de subdominios sondeando la infraestructura administrada por la organización de destino o los servidores DNS de terceros que hemos identificado previamente. En este caso, la cantidad de tráfico generado puede llevar a la detección de nuestras actividades de reconocimiento.

{% hint style="danger" %}
Reconocimiento activo, no usar estas técnicas sin autorización del objetivo.&#x20;
{% endhint %}

***

## <mark style="color:purple;">Transferencia de Zona</mark>

La transferencia de zona es la forma en que un servidor DNS secundario recibe información del servidor DNS primario y la actualiza. El enfoque maestro-esclavo se utiliza para organizar servidores DNS dentro de un dominio, y los esclavos reciben información DNS actualizada del DNS maestro. El servidor DNS maestro debe configurarse para permitir transferencias de zona desde servidores DNS secundarios (esclavos), aunque es posible que esté mal configurado.

Por ejemplo, utilizaremos el servicio <https://hackertarget.com/zone-transfer/> y el dominio `zonetransfer.me` para tener una idea de la información que se puede obtener mediante esta técnica.

![imagen](https://academy.hackthebox.com/storage/modules/144/zonetransfer.png)

Un enfoque manual será el siguiente conjunto de comandos:

### **1. Identificación de NameServers**

```shell-session
afsh4ck@kali$ nslookup -type=NS zonetransfer.me

Server:		10.100.0.1
Address:	10.100.0.1#53

Non-authoritative answer:
zonetransfer.me	nameserver = nsztm2.digi.ninja.
zonetransfer.me	nameserver = nsztm1.digi.ninja.
```

Realiza la transferencia de zona utilizando los parámetros `-type=any` y `-query=AXFR`

### **2. Prueba de transferencia de zona ANY y AXFR**

```shell-session
afsh4ck@kali$ nslookup -type=any -query=AXFR zonetransfer.me nsztm1.digi.ninja

Server:		nsztm1.digi.ninja
Address:	81.4.108.41#53

zonetransfer.me
	origin = nsztm1.digi.ninja
	mail addr = robin.digi.ninja
	serial = 2019100801
	refresh = 172800
	retry = 900
	expire = 1209600
	minimum = 3600
zonetransfer.me	hinfo = "Casio fx-700G" "Windows XP"
zonetransfer.me	text = "google-site-verification=tyP28J7JAUHA9fw2sHXMgcCC0I6XBmmoVi04VlMewxA"
zonetransfer.me	mail exchanger = 0 ASPMX.L.GOOGLE.COM.
zonetransfer.me	mail exchanger = 10 ALT1.ASPMX.L.GOOGLE.COM.
zonetransfer.me	mail exchanger = 10 ALT2.ASPMX.L.GOOGLE.COM.
zonetransfer.me	mail exchanger = 20 ASPMX2.GOOGLEMAIL.COM.
zonetransfer.me	mail exchanger = 20 ASPMX3.GOOGLEMAIL.COM.
zonetransfer.me	mail exchanger = 20 ASPMX4.GOOGLEMAIL.COM.
zonetransfer.me	mail exchanger = 20 ASPMX5.GOOGLEMAIL.COM.
Name:	zonetransfer.me
Address: 5.196.105.14
zonetransfer.me	nameserver = nsztm1.digi.ninja.
zonetransfer.me	nameserver = nsztm2.digi.ninja.
_acme-challenge.zonetransfer.me	text = "6Oa05hbUJ9xSsvYy7pApQvwCUSSGgxvrbdizjePEsZI"
_sip._tcp.zonetransfer.me	service = 0 0 5060 www.zonetransfer.me.
14.105.196.5.IN-ADDR.ARPA.zonetransfer.me	name = www.zonetransfer.me.
asfdbauthdns.zonetransfer.me	afsdb = 1 asfdbbox.zonetransfer.me.
Name:	asfdbbox.zonetransfer.me
Address: 127.0.0.1
asfdbvolume.zonetransfer.me	afsdb = 1 asfdbbox.zonetransfer.me.
Name:	canberra-office.zonetransfer.me
Address: 202.14.81.230
cmdexec.zonetransfer.me	text = "; ls"
contact.zonetransfer.me	text = "Remember to call or email Pippa on +44 123 4567890 or pippa@zonetransfer.me when making DNS changes"
Name:	dc-office.zonetransfer.me
Address: 143.228.181.132
Name:	deadbeef.zonetransfer.me
Address: dead:beaf::
dr.zonetransfer.me	loc = 53 20 56.558 N 1 38 33.526 W 0.00m 1m 10000m 10m
DZC.zonetransfer.me	text = "AbCdEfG"
email.zonetransfer.me	naptr = 1 1 "P" "E2U+email" "" email.zonetransfer.me.zonetransfer.me.
Name:	email.zonetransfer.me
Address: 74.125.206.26
Hello.zonetransfer.me	text = "Hi to Josh and all his class"
Name:	home.zonetransfer.me
Address: 127.0.0.1
Info.zonetransfer.me	text = "ZoneTransfer.me service provided by Robin Wood - robin@digi.ninja. See http://digi.ninja/projects/zonetransferme.php for more information."
internal.zonetransfer.me	nameserver = intns1.zonetransfer.me.
internal.zonetransfer.me	nameserver = intns2.zonetransfer.me.
Name:	intns1.zonetransfer.me
Address: 81.4.108.41
Name:	intns2.zonetransfer.me
Address: 167.88.42.94
Name:	office.zonetransfer.me
Address: 4.23.39.254
Name:	ipv6actnow.org.zonetransfer.me
Address: 2001:67c:2e8:11::c100:1332
Name:	owa.zonetransfer.me
Address: 207.46.197.32
robinwood.zonetransfer.me	text = "Robin Wood"
rp.zonetransfer.me	rp = robin.zonetransfer.me. robinwood.zonetransfer.me.
sip.zonetransfer.me	naptr = 2 3 "P" "E2U+sip" "!^.*$!sip:customer-service@zonetransfer.me!" .
sqli.zonetransfer.me	text = "' or 1=1 --"
sshock.zonetransfer.me	text = "() { :]}; echo ShellShocked"
staging.zonetransfer.me	canonical name = www.sydneyoperahouse.com.
Name:	alltcpportsopen.firewall.test.zonetransfer.me
Address: 127.0.0.1
testing.zonetransfer.me	canonical name = www.zonetransfer.me.
Name:	vpn.zonetransfer.me
Address: 174.36.59.154
Name:	www.zonetransfer.me
Address: 5.196.105.14
xss.zonetransfer.me	text = "'><script>alert('Boo')</script>"
zonetransfer.me
	origin = nsztm1.digi.ninja
	mail addr = robin.digi.ninja
	serial = 2019100801
	refresh = 172800
	retry = 900
	expire = 1209600
	minimum = 3600
```

Si logramos realizar una transferencia de zona exitosa para un dominio, no es necesario continuar enumerando este dominio en particular ya que esto extraerá toda la información disponible.

### 3. Dig

```shell-session
afsh4ck@kali$ dig axfr inlanefreight.htb @10.129.42.195

; <<>> DiG 9.19.17-2~kali1-Kali <<>> axfr inlanefreight.htb @10.129.42.195
;; global options: +cmd
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.	604800	IN	NS	ns.inlanefreight.htb.
admin.inlanefreight.htb. 604800	IN	A	10.10.34.2
ftp.admin.inlanefreight.htb. 604800 IN	A	10.10.34.2
careers.inlanefreight.htb. 604800 IN	A	10.10.34.50
dc1.inlanefreight.htb.	604800	IN	A	10.10.34.16
dc2.inlanefreight.htb.	604800	IN	A	10.10.34.11
internal.inlanefreight.htb. 604800 IN	A	127.0.0.1
admin.internal.inlanefreight.htb. 604800 IN A	10.10.1.11
wsus.internal.inlanefreight.htb. 604800	IN A	10.10.1.240
ir.inlanefreight.htb.	604800	IN	A	10.10.45.5
dev.ir.inlanefreight.htb. 604800 IN	A	10.10.45.6
ns.inlanefreight.htb.	604800	IN	A	127.0.0.1
resources.inlanefreight.htb. 604800 IN	A	10.10.34.100
securemessaging.inlanefreight.htb. 604800 IN A	10.10.34.52
test1.inlanefreight.htb. 604800	IN	A	10.10.34.101
us.inlanefreight.htb.	604800	IN	A	10.10.200.5
cluster14.us.inlanefreight.htb.	604800 IN A	10.10.200.14
messagecenter.us.inlanefreight.htb. 604800 IN A	10.10.200.10
ww02.inlanefreight.htb.	604800	IN	A	10.10.34.112
www1.inlanefreight.htb.	604800	IN	A	10.10.34.111
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
;; Query time: 31 msec
;; SERVER: 10.129.42.195#53(10.129.42.195) (TCP)
;; WHEN: Wed Feb 21 08:50:14 CET 2024
;; XFR size: 22 records (messages 1, bytes 594)
```

***

## <mark style="color:purple;">Bruteforce de subdominios</mark>

`Subdomain Brute-Force Enumeration` es una técnica de descubrimiento de subdominios activa y eficaz que aprovecha listas predefinidas de posibles nombres de subdominios. Este enfoque prueba sistemáticamente estos nombres en relación con el dominio de destino para identificar subdominios válidos. Al utilizar listas de palabras cuidadosamente elaboradas, puede aumentar significativamente la eficiencia y la eficacia de sus esfuerzos de descubrimiento de subdominios.

Hay varias herramientas disponibles que se destacan en la enumeración de fuerza bruta:

<table><thead><tr><th width="139">Tool</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://github.com/blacklanternsecurity/bbot">bbot</a></td><td>Herramienta de código abierto con múltiples opciones, entre ellas la búsqueda activa y pasiva de subdominios</td></tr><tr><td><a href="https://github.com/fwaeytens/dnsenum">dnsenum</a></td><td>Completa herramienta de enumeración de DNS que admite ataques de diccionario y de fuerza bruta para descubrir subdominios.</td></tr><tr><td><a href="https://github.com/mschwager/fierce">fierce</a></td><td>Herramienta fácil de usar para el descubrimiento recursivo de subdominios, que incluye detección de comodines y una interfaz fácil de usar.</td></tr><tr><td><a href="https://github.com/darkoperator/dnsrecon">dnsrecon</a></td><td>Herramienta versátil que combina múltiples técnicas de reconocimiento de DNS y ofrece formatos de salida personalizables.</td></tr><tr><td><a href="https://github.com/owasp-amass/amass">amass</a></td><td>Herramienta mantenida activamente centrada en el descubrimiento de subdominios, conocida por su integración con otras herramientas y amplias fuentes de datos.</td></tr><tr><td><a href="https://github.com/tomnomnom/assetfinder">assetfinder</a></td><td>Herramienta sencilla pero eficaz para encontrar subdominios utilizando diversas técnicas, ideal para escaneos rápidos y ligeros.</td></tr><tr><td><a href="https://github.com/d3mondev/puredns">puredns</a></td><td>Potente y flexible herramienta de fuerza bruta DNS, capaz de resolver y filtrar resultados de forma eficaz.</td></tr></tbody></table>

### Bbot

**Bbot** es una herramienta de código abierto diseñada para la recolección de información y pruebas de seguridad. Su objetivo principal es facilitar el reconocimiento de infraestructuras de red al permitir la enumeración de subdominios, recopilación de puertos abiertos, servicios y otros detalles críticos.

{% embed url="<https://github.com/blacklanternsecurity/bbot>" %}

```bash
# Subdominios - Activa
bbot -t inlanefreight.com -p subdomain-enum

# Subdominios - Pasiva
bbot -t inlanefreight.com -p subdomain-enum -rf passive
```

BBOT encuentra entre un 20 % y un 50 % más de subdominios que otras herramientas. Cuanto mayor sea el dominio, mayor será la diferencia.

<figure><img src="/files/ETBPxQoWKmvlv1Pn842p" alt=""><figcaption></figcaption></figure>

### dnsnum

Herramienta de línea de comandos versátil y ampliamente utilizada escrita en Perl. Es un conjunto de herramientas integral para el reconocimiento de DNS, que proporciona varias funcionalidades para recopilar información sobre la infraestructura de DNS de un dominio de destino y los posibles subdominios. La herramienta ofrece varias funciones clave:

Veamos `dnsenum` en acción enumerando subdominios en nuestro objetivo `inlanefreight.com`. En esta demostración, utilizaremos la wordlist `subdomains-top1million-5000.txt` de [SecLists](https://github.com/danielmiessler/SecLists) , que contiene los 5000 subdominios más comunes.

```bash
dnsenum --enum inlanefreight.com -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -r
```

```shell-session
afsh4ck@kali$ dnsenum --enum inlanefreight.com -f  /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt 

dnsenum VERSION:1.2.6

-----   inlanefreight.com   -----


Host's addresses:
__________________

inlanefreight.com.                       300      IN    A        134.209.24.248

[...]

Brute forcing with /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt:
_______________________________________________________________________________________

www.inlanefreight.com.                   300      IN    A        134.209.24.248
support.inlanefreight.com.               300      IN    A        134.209.24.248
[...]


done.
```

***

## <mark style="color:purple;">Gobuster</mark>

Gobuster es una herramienta que podemos utilizar para realizar la enumeración de subdominios. Para nosotros son especialmente interesantes las opciones de patrones, ya que hemos aprendido algunas convenciones de nomenclatura a partir de la recopilación pasiva de información que podemos utilizar para descubrir nuevos subdominios que siguen el mismo patrón.

Podemos usar una lista de palabras del repositorio [Seclists](https://github.com/danielmiessler/SecLists) si buscamos palabras en patrones en lugar de números. Recuerde que durante nuestras actividades de enumeración pasiva de subdominios, encontramos un patrón `lert-api-shv-{NUMBER}-sin6.facebook.com`. Podemos usar este patrón para descubrir subdominios adicionales. El primer paso será crear un archivo `patterns.txt` con los patrones descubiertos anteriormente, por ejemplo:

### **GoBuster - patterns.txt**

```bash
lert-api-shv-{GOBUSTER}-sin6
atlas-pp-shv-{GOBUSTER}-sin6
```

El siguiente paso será iniciar `gobuster` usando el módulo `dns`, especificando las siguientes opciones:

* `dns`: Inicia el módulo DNS
* `-q`: No imprime el banner ni otros ruidos.
* `-r`: Utiliza un servidor DNS personalizado
* `-d`: Nombre de dominio de destino
* `-p`: Ruta al archivo de patrones
* `-w`: Ruta a la lista de palabras
* `-o`: Archivo de salida

En nuestro caso, este será el comando.

### **Gobuster-DNS**

```shell-session
afsh4ck@kali$ export TARGET="facebook.com"
afsh4ck@kali$ export NS="d.ns.facebook.com"
afsh4ck@kali$ export WORDLIST="numbers.txt"
afsh4ck@kali$ gobuster dns -q -r "${NS}" -d "${TARGET}" -w "${WORDLIST}" -p ./patterns.txt -o "gobuster_${TARGET}.txt"

Found: lert-api-shv-01-sin6.facebook.com
Found: atlas-pp-shv-01-sin6.facebook.com
Found: atlas-pp-shv-02-sin6.facebook.com
Found: atlas-pp-shv-03-sin6.facebook.com
Found: lert-api-shv-03-sin6.facebook.com
Found: lert-api-shv-02-sin6.facebook.com
Found: lert-api-shv-04-sin6.facebook.com
Found: atlas-pp-shv-04-sin6.facebook.com
```

### Gobuster - Subdominios

También podemos usar gobuster para enumerar subdominios de forma genérica con el siguiente comando:

```shell-session
afsh4ck@kali$ export TARGET="githubapp.com"
afsh4ck@kali$ export WORDLIST="/usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt"
afsh4ck@kali$ gobuster dns -q -d "${TARGET}" -w "${WORDLIST}" -o "gobuster_${TARGET}.txt"

Found: office.githubapp.com
Found: data.githubapp.com
Found: gateway.githubapp.com
Found: stream.githubapp.com
Found: music.githubapp.com
Found: catalog.githubapp.com
Found: status.githubapp.com
Found: site.githubapp.com
Found: team.githubapp.com
Found: play.githubapp.com
Found: podcast.githubapp.com
Found: central.githubapp.com
Found: io.githubapp.com
```

También le puedes echar un ojo a la sección dedicada a esta herramienta:

{% content-ref url="/pages/BCt1x9j4Sf2NG3MCMhZJ" %}
[Gobuster](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing/gobuster.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">Subfinder</mark>

Subfinder es una herramienta de código abierto diseñada para realizar búsquedas de subdominios de manera eficiente. Fue desarrollada originalmente por James Cook y ahora es mantenida por el equipo de Project Discovery. La herramienta está escrita en el lenguaje de programación Go.

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ subfinder -d githubapp.com                     
</strong>
               __    _____           __         
   _______  __/ /_  / __(_)___  ____/ /__  _____
  / ___/ / / / __ \/ /_/ / __ \/ __  / _ \/ ___/
 (__  ) /_/ / /_/ / __/ / / / / /_/ /  __/ /    
/____/\__,_/_.___/_/ /_/_/ /_/\__,_/\___/_/

		projectdiscovery.io

[INF] Current subfinder version v2.6.0 (outdated)
[INF] Loading provider config from /home/kali/.config/subfinder/provider-config.yaml
[INF] Enumerating subdomains for githubapp.com
scim-bridge.githubapp.com
catalog.githubapp.com
hq.githubapp.com
io.githubapp.com
compute-products-fundamentals.githubapp.com
manual-of-style.githubapp.com
npm-reports.githubapp.com
gloss.githubapp.com
podcast.githubapp.com
team.githubapp.com
mlops.githubapp.com
....
</code></pre>

### Instalación de Subfinder

#### Paso 1: Instalar Go

Subfinder está escrito en Go, por lo que necesitas tener instalado Go en tu sistema. Si aún no lo tienes instalado, puedes instalarlo siguiendo estos pasos:

1. Abre una terminal.
2. Ejecuta el siguiente comando para instalar Go desde los repositorios de Kali Linux:

```bash
sudo apt install golang-go
```

#### Paso 2: Configurar las variables de entorno de Go

Después de instalar Go, necesitas configurar las variables de entorno. Abre tu archivo de perfil (`~/.bashrc`, `~/.bash_profile` o `~/.profile`) y agrega las siguientes líneas al final del archivo:

```bash
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```

Guarda el archivo y cierra la terminal actual o ejecuta `source` en el archivo para actualizar las variables de entorno:

```bash
source ~/.bashrc
```

#### Paso 3: Instalar Subfinder

Una vez configuradas las variables de entorno, puedes instalar Subfinder utilizando el siguiente comando:

```bash
GO111MODULE=on go get -u -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder
```

Esto descargará y compilará Subfinder y lo instalará en tu sistema.

#### Paso 4: Uso de Subfinder

Después de instalar Subfinder, puedes usarlo para buscar subdominios de un dominio específico. Por ejemplo, para buscar subdominios de `example.com`, puedes ejecutar el siguiente comando:

```bash
subfinder -d example.com
```

***

## <mark style="color:purple;">Reconocimiento Pasivo de Subdominios</mark>

En la siguiente sección veremos otras técnicas de reconocimiento pasivo de subdominios:

{% content-ref url="/pages/7Bwxmq5INs5YpamqjP3t" %}
[Subdominios - Pasiva](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-pasiva/subdominios-pasiva.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">Ataques específicos del protocolo</mark>

{% content-ref url="/pages/P96Vd5rlfE3eGxvLHTzL" %}
[Ataques a DNS](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/atacando-servicios-comunes/ataques-a-dns.md)
{% endcontent-ref %}
