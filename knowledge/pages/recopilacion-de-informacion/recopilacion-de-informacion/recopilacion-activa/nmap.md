
# Nmap

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que hacen muchas peticiones al servidor del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Nmap</mark>

{% embed url="<https://nmap.org/>" %}

Nmap es una de las herramientas de seguridad más populares y potentes de la actualidad, y se utiliza en pruebas de penetración, hacking ético, administración de redes y otros propósitos relacionados con la seguridad de la red. Viene instalado por defecto en Kali Linux.

## <mark style="color:purple;">Video completo de la herramienta</mark>

{% embed url="<https://youtu.be/bYMR3HHUtWQ>" %}

## <mark style="color:purple;">Cheatsheet</mark>

<table><thead><tr><th width="328">Comando</th><th>Descripción</th></tr></thead><tbody><tr><td><code>nmap &#x3C;host></code></td><td>Escaneo de host simple</td></tr><tr><td><code>nmap &#x3C;start_ip>-&#x3C;end_ip></code></td><td>Escaneo de rangos de direcciones IP</td></tr><tr><td><code>nmap -p &#x3C;port_range> &#x3C;host></code></td><td>Escaneo de un rango de puertos</td></tr><tr><td><code>nmap -p- &#x3C;host></code></td><td>Escaneo de todos los puertos</td></tr><tr><td><code>nmap -p 1-1000 &#x3C;host></code></td><td>Escaneo de los 1000 puertos más comunes</td></tr><tr><td><code>nmap -sS &#x3C;host></code></td><td>Escaneo sigiloso (no genera registros en destino)</td></tr><tr><td><code>nmap -sV &#x3C;host></code></td><td>Escaneo de servicios y versiones</td></tr><tr><td><code>nmap -T5 -F &#x3C;host></code></td><td>Escaneo rápido sin resolución de DNS</td></tr><tr><td><code>nmap -O &#x3C;host></code></td><td>Escaneo de sistemas operativos</td></tr><tr><td><code>nmap --script vuln &#x3C;host></code></td><td>Escaneo de scripts de vulnerabilidades</td></tr><tr><td><code>nmap --script &#x3C;script_name> &#x3C;host></code></td><td>Escaneo de scripts específicos</td></tr><tr><td><code>nmap -sU &#x3C;host></code></td><td>Escaneo UDP</td></tr><tr><td><code>nmap -sn &#x3C;network></code></td><td>Escaneo de hosts vivos en una red</td></tr><tr><td><code>nmap -oX output.xml &#x3C;host></code></td><td>Guardar resultados en formato XML</td></tr></tbody></table>

## <mark style="color:purple;">Estados de los puertos</mark>

Hay un total de 6 estados diferentes para un puerto escaneado que podemos obtener:

<table data-header-hidden><thead><tr><th width="200"></th><th></th></tr></thead><tbody><tr><td><strong>Estado</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>open</code></td><td>Esto indica que se ha establecido la conexión con el puerto escaneado. Estas conexiones pueden ser conexiones TCP, UDP o SCTP.</td></tr><tr><td><code>closed</code></td><td>Cuando el puerto se muestra como cerrado, el protocolo TCP indica que el paquete que recibimos contiene un indicador RST. Este método de escaneo también se puede utilizar para determinar si nuestro objetivo está vivo o no.</td></tr><tr><td><code>filtered</code></td><td>Nmap no puede identificar correctamente si el puerto escaneado está abierto o cerrado porque no se devuelve ninguna respuesta del destino para el puerto o recibimos un código de error del destino.</td></tr><tr><td><code>unfiltered</code></td><td>Este estado de un puerto solo ocurre durante el escaneo TCP-ACK y significa que el puerto es accesible, pero no se puede determinar si está abierto o cerrado.</td></tr><tr><td><code>open|filtered</code></td><td>Si no obtenemos respuesta para un puerto específico, Nmap lo establecerá en ese estado. Esto indica que un firewall o un filtro de paquetes pueden proteger el puerto.</td></tr><tr><td><code>closed|filtered</code></td><td>Este estado solo ocurre en los escaneos inactivos de ID de IP e indica que fue imposible determinar si el puerto escaneado está cerrado o filtrado por un firewall.</td></tr></tbody></table>

## <mark style="color:purple;">Definir el target en una variable</mark>

```bash
export TARGET="githubapp.com"
```

## <mark style="color:purple;">Reconocimiento de Hosts</mark>

```bash
sudo nmap -sn $TARGET
```

```bash
sudo nmap 10.129.2.0/24 -sn -oA tnet | grep for | cut -d " " -f5

10.129.2.4
10.129.2.10
10.129.2.11
10.129.2.18
10.129.2.19
10.129.2.20
10.129.2.28
```

<table data-header-hidden><thead><tr><th width="255">Opciones</th><th>Descripción</th></tr></thead><tbody><tr><td><code>10.129.2.0/24</code></td><td>Rango de red objetivo.</td></tr><tr><td><code>-sn</code></td><td>Desactiva el escaneo de puertos.</td></tr><tr><td><code>-oA tnet</code></td><td>Almacena los resultados en todos los formatos comenzando con el nombre 'tnet'.</td></tr></tbody></table>

## <mark style="color:purple;">Escanear lista de IP</mark>&#x20;

Durante una prueba de penetración interna, no es raro que se nos proporcione una lista de IP con los hosts que necesitamos probar. Nmap también nos da la opción de trabajar con listas y leer los hosts de esta lista en lugar de definirlos o escribirlos manualmente.

Una lista de este tipo podría verse así:

```bash
cat hosts.lst

10.129.2.4
10.129.2.10
10.129.2.11
10.129.2.18
10.129.2.19
10.129.2.20
10.129.2.28
```

```bash
sudo nmap -sn -oA tnet -iL hosts.lst | grep for | cut -d " " -f5

10.129.2.18
10.129.2.19
10.129.2.20
```

<table data-header-hidden><thead><tr><th width="255">Opciones</th><th>Descripción</th></tr></thead><tbody><tr><td><code>-iL hosts.lst</code></td><td>Realiza análisis definidos contra objetivos en la lista <code>hosts.lst</code></td></tr></tbody></table>

## <mark style="color:purple;">Descubrir todos los nodos de la red</mark>

```bash
sudo nmap IP-TARGET # el último valor cambiar por 0/24
sudo nmap 198.164.1.0/24
```

## <mark style="color:purple;">Descubrir puertos abiertos</mark>

```bash
sudo nmap -p- --open -sS --min-rate 5000 -v -n $TARGET
```

## <mark style="color:purple;">Identificación del sistema operativo</mark>

```bash
sudo nmap -A -V $TARGET
sudo nmap -v -O $TARGET
```

## <mark style="color:purple;">Escaneo de puertos TCP</mark>

```bash
sudo nmap -sS $TARGET
sudo nmap -sS IP(terminado en .0/24)
```

## <mark style="color:purple;">Escaneo de puertos UDP</mark>

```bash
sudo nmap -sU $TARGET
sudo nmap -sU IP(terminado en .0/24)
```

## <mark style="color:purple;">Escaneo de los puertos Top 10</mark>

```bash
sudo nmap $TARGET --top-ports=10 

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 15:36 CEST
Nmap scan report for 10.129.2.28
Host is up (0.021s latency).

PORT     STATE    SERVICE
21/tcp   closed   ftp
22/tcp   open     ssh
23/tcp   closed   telnet
25/tcp   open     smtp
80/tcp   open     http
110/tcp  open     pop3
139/tcp  filtered netbios-ssn
443/tcp  closed   https
445/tcp  filtered microsoft-ds
3389/tcp closed   ms-wbt-server
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 1.44 seconds
```

Para los Top 100 es igual pero con el parámetro -F

```bash
sudo nmap $TARGET -F
```

## <mark style="color:purple;">Escaneo de servicios</mark>

{% hint style="danger" %}
Es la técnica de escaneo más intrusiva
{% endhint %}

{% code overflow="wrap" %}

```bash
sudo nmap -p- -sV $TARGET
sudo nmap -sV $TARGET -p 80
```

{% endcode %}

## <mark style="color:purple;">Enumeración básica de servicios</mark>

```bash
sudo nmap -sCV -p 22,80 $TARGET -oN targeted 
```

## <mark style="color:purple;">Escaneo completo con identificación de servicios</mark>

```bash
sudo nmap -sV -sC -p- $TARGET
sudo nmap -sC -sS -sV -T5 $TARGET # El -T5 aumenta la velocidad de escaneo
```

## <mark style="color:purple;">Generación de informe</mark>

```bash
sudo nmap -v --reason -sV -oX servicios.xml --webxml $TARGET
```

A partir de un xml podríamos usar la herramienta `xsltproc` para generar un html visual, para abrirlo desde un navegador:

```bash
xsltproc target.xml -o target.html
```

## <mark style="color:purple;">SMB Enumeration</mark>

Sirve para encontrar carpetas y archivos compartidos. Trabaja en los puertos 139 y 445

```bash
sudo nmap -v -sS -p 139,445 $TARGET
```

* Ver scripts de tareas automatizadas:

```bash
cd /usr/share/nmap/scripts -> ls
```

* Añadir filtro dentro de la carpeta:

```bash
ls smb*
```

* Ejecutar un script en concreto:

```bash
sudo nmap -v -sS -p 139,445 --script=SCRIPT $TARGET
```

## <mark style="color:purple;">SNMP Enumeration</mark>&#x20;

{% hint style="info" %}
Suele ser vulnerable
{% endhint %}

* Sirve para ganar datos de acceso a la configuración de un sistema
* Trabaja en el puerto 161

{% code overflow="wrap" %}

```bash
sudo nmap -v -sS -p 161 $TARGET

# Ver los scripts para snmp: 
cd /usr/share/nmap/scripts -> ls snmp*
```

{% endcode %}

## <mark style="color:purple;">Listado SMB</mark>

```python
smbclient -N -L \\\\10.129.42.253         # Listado SMB
smbclient \\\\10.129.42.253\\users        # Acceso por SMB
smbclient -U bob \\\\10.129.42.253\\users # Acceso con usuario
```

## <mark style="color:purple;">Identificar bases de datos MySQL</mark>

<pre class="language-bash"><code class="lang-bash"><strong>sudo nmap -sS -p 3306 IP-TARGET.0/24
</strong># El puerto 3306 es el de la base de datos MySQL
</code></pre>

<figure><img src="/files/4NQFNLHxSEGNmqSs0ewz" alt=""><figcaption><p>Identificación de bases de datos en un red</p></figcaption></figure>

## <mark style="color:purple;">Nmap Automator</mark>

{% embed url="<https://github.com/21y4d/nmapAutomator>" %}

Script automático de escaneo con nmap. Es muy útil y ampliamente utilizado en pentesting, ya que podemos configurar distintas opciones y nos devuelve un resultado muy visual.

```bash
git clone https://github.com/21y4d/nmapAutomator.git
cd nmapAutomator
./nmapAutomator.sh -H $TARGET -t <TYPE>
```

```shell-session
./nmapAutomator.sh -h

Usage: nmapAutomator.sh -H/--host <TARGET-IP> -t/--type <TYPE>
Optional: [-r/--remote <REMOTE MODE>] [-d/--dns <DNS SERVER>] [-o/--output <OUTPUT DIRECTORY>] [-s/--static-nmap <STATIC NMAP PATH>]

Scan Types:
	Network : Shows all live hosts in the host's network (~15 seconds)
	Port    : Shows all open ports (~15 seconds)
	Script  : Runs a script scan on found ports (~5 minutes)
	Full    : Runs a full range port scan, then runs a script scan on new ports (~5-10 minutes)
	UDP     : Runs a UDP scan "requires sudo" (~5 minutes)
	Vulns   : Runs CVE scan and nmap Vulns scan on all found ports (~5-15 minutes)
	Recon   : Suggests recon commands, then prompts to automatically run them
	All     : Runs all the scans (~20-30 minutes)
```

```bash
./nmapAutomator.sh -H $TARGET -t Vulns

Running a Vulns scan on 10.129.183.35
Host is likely running Windows

---------------------Starting Port Scan-----------------------

PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
5000/tcp open  upnp

<----- SNIP ----->
```
