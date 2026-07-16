
# Metasploit

{% embed url="<https://github.com/rapid7/metasploit-framework/tree/master>" %}

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Instalación</mark>

Metasploit tiene una amplia variedad de herramientas de prueba de penetración que pueden utilizarse para identificar vulnerabilidades, explotarlas y tomar el control de sistemas informáticos. Viene instalado por defecto en Kali Linux.

Para utilizar Metasploit en Kali Linux, sigue los siguientes pasos:

```bash
sudo apt update && sudo apt install metasploit-framework
sudo msfconsole
```

5. Utiliza el comando "`search`" para buscar exploits específicos o para buscar exploits relacionados con una vulnerabilidad específica.
6. Utiliza el comando "`use`" para seleccionar un exploit específico.
7. Utiliza el comando "`set`" para configurar las opciones necesarias para el exploit seleccionado.
8. Utiliza el comando "`exploit`" para ejecutar el exploit.

```bash
msfconsole 
search
search cve:2010-2075  # Buscar exploits de un CVE
use exploit/EXPLOIT
show options 
set rhost IP-TARGET
show payloads 
exploit
```

## <mark style="color:purple;">Módulos en Metasploit</mark>

Los módulos en Metasploit son componentes clave que permiten realizar diversas acciones relacionadas con pruebas de penetración y explotación de vulnerabilidades. Están categorizados en diferentes tipos, como exploits, payloads, auxiliares, encoders, nops y post, cada uno sirviendo un propósito específico.&#x20;

* Los exploits son scripts que aprovechan las vulnerabilidades de los sistemas.
* Los payloads son las cargas útiles ejecutadas después de que un exploit ha tenido éxito.
* Los módulos auxiliares pueden realizar tareas como escaneo o recopilación de información.
* Los encoders ayudan a evadir detección.

Podemos ver todos los módulos de Metasploit en la siguiente ruta:

```bash
cd /usr/share/metasploit-framework/modules

ls
auxiliary
encoders
evasion
exploits
nops
payloads
post
```

```bash
cd exploits

ls  
aix        bsdi        example_linux_priv_esc.rb  hpux       multi    qnx
android    dialup      example_webapp.rb          irix       netware  solaris
apple_ios  example.py  firefox                    linux      openbsd  unix
bsd        example.rb  freebsd                    mainframe  osx      windows
```

## <mark style="color:purple;">Ver si el host es vulnerable a un exploit</mark>

```shell-session
use exploit windows/smb/ms17_010_psexec
msf6 exploit(windows/smb/ms17_010_psexec) > check

[*] 10.10.10.40:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 10.10.10.40:445       - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
[*] 10.10.10.40:445       - Scanned 1 of 1 hosts (100% complete)
[+] 10.10.10.40:445 - The target is vulnerable.
```

## <mark style="color:purple;">Usando Nmap dentro de Msfconsole</mark>

Podemos usar Nmap directamente desde msfconsole. Para escanear directamente desde la consola sin tener que pasar a segundo plano o salir del proceso, use el comando `db_nmap`. Lo bueno de esta técnica es que nos guardará todos los resultados en la base de datos de Metasploit.

### **DB\_Nmap**

```bash
msf6 > db_nmap -sV -sS 10.10.10.8

[*] Nmap: Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-17 21:04 UTC
[*] Nmap: Nmap scan report for 10.10.10.8
[*] Nmap: Host is up (0.016s latency).
[*] Nmap: Not shown: 999 filtered ports
[*] Nmap: PORT   STATE SERVICE VERSION
[*] Nmap: 80/TCP open  http    HttpFileServer httpd 2.3
[*] Nmap: Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
[*] Nmap: Service detection performed. Please report any incorrect results at https://nmap.org/submit/ 
[*] Nmap: Nmap done: 1 IP address (1 host up) scanned in 11.12 seconds

msf6 > hosts     # Nos muestra los hosts
msf6 > services  # Nos muestra los servicios corriendo
msf6 > vulns     # Nos muestra las vulnerabilidades encontradas
```

## <mark style="color:purple;">Base de datos de Metasploit</mark>

La base de datos de Metasploit es una herramienta integral que almacena información relevante recolectada a lo largo de una prueba de penetración. Esta funcionalidad optimiza la gestión de datos al permitir registrar y consultar detalles sobre hosts, servicios, vulnerabilidades o credenciales capturadas, entre otros.

Al integrar esta base de datos, los usuarios pueden realizar un análisis más estructurado y eficiente de la información obtenida, facilitando la identificación de patrones y correlaciones dentro de sus investigaciones de seguridad. La capacidad de registrar y recuperar datos de forma sistemática simplifica la gestión de proyectos a mayor escala, asegurando así una estrategia organizada y detallada durante las pruebas de penetración.

### Cheatsheet

```bash
# Iniciar la base de datos
#---------------------------
sudo service postgresql status   # Status de postgresql
sudo systemctl start postgresql  # Iniciar la base de datos postgresql
sudo msfdb init                  # Iniciar la base de datos msfdb
sudo msfdb status                # Status de la base de datos msfdb
sudo msfdb run                   # Conectarse a la base de datos msfdb

# Reiniciar la base de datos
#---------------------------
msfdb reinit
cp /usr/share/metasploit-framework/config/database.yml ~/.msf4/
sudo service postgresql restart
msfconsole -q

# Opciones de la base de datos
#-----------------------------
msf6 > help database  # Opciones de la base de datos
msf6 > workspace -h   # Opciones de Espacio de trabajo
msf6 > hosts -h       # Opciones de hosts
msf6 > services -h    # Opciones de servicios
msf6 > creds -h       # Opciones de credenciales encontradas
msf6 > loot -h        # Opciones de loot
```

***

## <mark style="color:purple;">**Uso de la base de datos de Metasploit**</mark>

Utilizar la base de datos facilita el seguimiento de nuestras actividades y la correlación de datos en investigaciones complejas.

### **Paso 1: Preparar la base de datos**

#### **1. Instalar PostgreSQL**

Metasploit utiliza PostgreSQL como su sistema de gestión de bases de datos. En Kali Linux, PostgreSQL generalmente viene preinstalado. Si no está instalado:

```bash
sudo apt update
sudo apt install postgresql
```

#### **2. Iniciar el servicio PostgreSQL**

Asegúrate de que PostgreSQL esté activo:

```bash
sudo service postgresql start
```

#### **3. Configurar la base de datos con Metasploit**

Metasploit tiene una utilidad para inicializar y configurar la base de datos:

```bash
msfdb init
```

Este comando:

* Inicia PostgreSQL si no está en ejecución.
* Crea una base de datos llamada `msf`.
* Configura Metasploit para conectarse a esa base de datos.

Para verificar que la base de datos está conectada, inicia Metasploit y usa:

```bash
msfconsole
db_status
```

Deberías ver algo como: `PostgreSQL connected to msf`.

***

### **Paso 2: Almacenar información en la base de datos**

Metasploit permite guardar información de objetivos escaneados, servicios, credenciales, y más:

#### **1. Escaneo de red**

Puedes usar herramientas dentro de Metasploit, como `auxiliary/scanner`, o integrar **Nmap** para escanear redes y almacenar resultados en la base de datos.

* **Ejecutar un escaneo con Nmap e importar resultados:**

```bash
nmap -sS -p- -oX scan_results.xml 192.168.1.0/24
db_import scan_results.xml
```

* **Escaneo directamente desde Metasploit:**

```bash
use auxiliary/scanner/portscan/tcp
set RHOSTS 192.168.1.0/24
run
```

Los resultados del escaneo se guardarán automáticamente en la base de datos.

#### **2. Guardar hosts manualmente**

Puedes agregar información de hosts de manera manual:

```bash
hosts -a 192.168.1.10
```

***

### **Paso 3: Consultar datos en la base de datos**

#### **1. Ver hosts almacenados**

Muestra una lista de todas las máquinas descubiertas.

```bash
hosts
```

#### **2. Consultar servicios detectados**

Muestra los servicios descubiertos, como puertos abiertos y protocolos en uso.

```bash
services
```

#### **3. Ver vulnerabilidades asociadas**

Si has realizado un análisis de vulnerabilidades (e.g., con Nmap, Nessus o Nexpose) e importado resultados:

```bash
vulns
```

#### **4. Listar credenciales recolectadas**

Muestra las credenciales detectadas o crackeadas durante la sesión.

```bash
creds
```

***

### **Paso 4: Usar datos en ataques**

La base de datos no solo almacena información, sino que también te permite usarla en tus ataques:

#### **1. Explorar un host desde la base de datos**

Selecciona un host específico para atacarlo, esto configura el objetivo de forma global para los módulos que ejecutes:

```bash
setg RHOST 192.168.1.10
```

#### **2. Explorar servicios almacenados**

Puedes atacar directamente los servicios detectados en un host:

```bash
use exploit/windows/smb/ms17_010_eternalblue
set RHOST 192.168.1.10
set RPORT 445
run
```

***

### **Paso 5: Exportar y analizar datos**

**Exportar información de la base de datos**

Puedes guardar los datos recopilados en formatos reutilizables:

```bash
msf6 > db_export -f xml -o machine-export.xml
[*] Starting export of workspace default to machine-export.xml [ xml ]...
[*] Finished export of workspace default to machine-export.xml [ xml ]...
```

#### **Limpiar la base de datos**

Si necesitas limpiar información para comenzar un nuevo análisis:

```bash
msf6 > hosts -d     # Elimina todos los host encontrados
msf6 > services -d  # Elimina todos los servicios corriendo
msf6 > vulns -d     # Elimina todas las vulnerabilidades encontradas
msf6 > creds -d     # Elimina todas las credenciales obtenidas
msf6 > loot -d      # Elimina todo el loot obtenido (archivos importantes)

# Reiniciar la base de datos
#---------------------------
msfdb reinit
cp /usr/share/metasploit-framework/config/database.yml ~/.msf4/
sudo service postgresql restart
msfconsole -q
```

***

## <mark style="color:purple;">Instalar nuevos plugins</mark>

```bash
cd /usr/share/metasploit-framework/plugins
git clone https://github.com/darkoperator/Metasploit-Plugins
ls Metasploit-Plugins

aggregator.rb      ips_filter.rb  pcap_log.rb          sqlmap.rb
alias.rb           komand.rb      pentest.rb           thread.rb
auto_add_route.rb  lab.rb         request.rb           token_adduser.rb
beholder.rb        libnotify.rb   rssfeed.rb           token_hunter.rb
db_credcollect.rb  msfd.rb        sample.rb            twitt.rb
db_tracker.rb      msgrpc.rb      session_notifier.rb  wiki.rb
event_tester.rb    nessus.rb      session_tagger.rb    wmap.rb
ffautoregen.rb     nexpose.rb     socket_logger.rb
growl.rb           openvas.rb     sounds.rb

# Copiar estos archivos a la carpeta /usr/share/metasploit-framework/plugins
sudo cp ./Metasploit-Plugins/* /usr/share/metasploit-framework/plugins/

# Comprobar que funcionan
msfconsole -q
msf6 > load pentest # Por ejemplo
help
```

## <mark style="color:purple;">Integrar Metasploit con Nessus</mark>

```
msfconsole
load nessus
nessus_help
```

## <mark style="color:purple;">Importación de escaneos</mark>

La importación de escaneos es un paso crucial al integrar herramientas de análisis de seguridad como Nessus y Nmap en Metasploit. Permite centralizar la información de hosts, servicios y vulnerabilidades detectadas, lo que facilita la planificación y ejecución de pruebas de penetración.&#x20;

### Importar escaneo de Nessus en Metasploit

Para importar un escaneo de Nessus, se exporta el archivo en formato .nessus y se utiliza el comando `db_import`, apuntando al archivo guardado.

```bash

# Importación de escaneo con Nessus
# ---------------------------------
msfconsole
db_import /home/kali/escaneo.nessus

hosts     # Ver todos los hosts
services  # Ver servicios identificados
vulns     # Ver vulnerabilidades encontradas

# Importación de escaneo con Nmap
# ---------------------------------
msfconsole
db_import target.xml

hosts     # Ver todos los hosts
services  # Ver servicios identificados
vulns     # Ver vulnerabilidades encontradas
```

### Importar escaneo de Nmap en Metasploit

Igualmente, los resultados de un escaneo de Nmap pueden importarse en Metasploit exportando el escaneo en formato XML.

```bash
nmap -v -sV --script vuln -oX target.xml 10.10.10.10
```

```bash
msfconsole
db_import target.xml

hosts     # Ver todos los hosts
services  # Ver servicios identificados
vulns     # Ver vulnerabilidades encontradas
```
