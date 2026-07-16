
# AD: Políticas de contraseñas

## <mark style="color:purple;">Enumeración de la política de contraseñas - Desde Linux - Con credenciales</mark>

Como se indicó en la sección anterior, podemos extraer la política de contraseñas del dominio de varias maneras, dependiendo de cómo esté configurado el dominio y de si tenemos o no credenciales de dominio válidas. Con credenciales de dominio válidas, la política de contraseñas también se puede obtener de forma remota utilizando herramientas como [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) o `rpcclient`.

```shell-session
afsh4ck@kali$ crackmapexec smb 172.16.5.5 -u avazquez -p Password123 --pass-pol

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\avazquez:Password123 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] Dumping password info for domain: INLANEFREIGHT
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Minimum password length: 8
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Password history length: 24
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Maximum password age: Not Set
SMB         172.16.5.5      445    ACADEMY-EA-DC01  
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Password Complexity Flags: 000001
SMB         172.16.5.5      445    ACADEMY-EA-DC01  	Domain Refuse Password Change: 0
SMB         172.16.5.5      445    ACADEMY-EA-DC01  	Domain Password Store Cleartext: 0
SMB         172.16.5.5      445    ACADEMY-EA-DC01  	Domain Password Lockout Admins: 0
SMB         172.16.5.5      445    ACADEMY-EA-DC01  	Domain Password No Clear Change: 0
SMB         172.16.5.5      445    ACADEMY-EA-DC01  	Domain Password No Anon Change: 0
SMB         172.16.5.5      445    ACADEMY-EA-DC01  	Domain Password Complex: 1
SMB         172.16.5.5      445    ACADEMY-EA-DC01  
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Minimum password age: 1 day 4 minutes 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Reset Account Lockout Counter: 30 minutes 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Locked Account Duration: 30 minutes 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Account Lockout Threshold: 5
SMB         172.16.5.5      445    ACADEMY-EA-DC01  Forced Log off Time: Not Set
```

***

## <mark style="color:purple;">Enumeración de la política de contraseñas - desde Linux - Sesiones SMB NULL</mark>

Sin credenciales, es posible que podamos obtener la política de contraseñas a través de una sesión SMB NULL o un enlace anónimo LDAP. La primera es a través de una sesión SMB NULL. Las sesiones SMB NULL permiten a un atacante no autenticado recuperar información del dominio, como una lista completa de usuarios, grupos, computadoras, atributos de cuentas de usuario y la política de contraseñas del dominio. Las configuraciones erróneas de la sesión SMB NULL a menudo son el resultado de la actualización de controladores de dominio heredados, lo que en última instancia trae consigo configuraciones inseguras, que existían de forma predeterminada en versiones anteriores de Windows Server.

Al crear un dominio en versiones anteriores de Windows Server, se concedía acceso anónimo a determinados recursos compartidos, lo que permitía la enumeración del dominio. Una sesión SMB NULL se puede enumerar fácilmente. Para la enumeración, podemos utilizar herramientas como `enum4linux`, `CrackMapExec`, `rpcclient`, etc.

Podemos usar [rpcclient](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html) para verificar un controlador de dominio para acceso a sesión SMB NULL.

Una vez conectados, podemos emitir un comando RPC cómo `querydominfo` para obtener información sobre el dominio y confirmar el acceso a la sesión NULL.

### **Usando rpcclient**

```shell-session
afsh4ck@kali$ rpcclient -U "" -N 172.16.5.5

rpcclient $> querydominfo
Domain:		INLANEFREIGHT
Server:		
Comment:	
Total Users:	3650
Total Groups:	0
Total Aliases:	37
Sequence No:	1
Force Logoff:	-1
Domain Server State:	0x1
Server Role:	ROLE_DOMAIN_PDC
Unknown 3:	0x1
```

También podemos obtener la política de contraseñas. Podemos ver que la política de contraseñas es relativamente débil, permitiendo una contraseña mínima de 8 caracteres.

### <mark style="color:purple;">**Obtención de la Política de Contraseñas usando rpcclient**</mark>

```shell-session
rpcclient $> querydominfo

Domain:		INLANEFREIGHT
Server:		
Comment:	
Total Users:	3650
Total Groups:	0
Total Aliases:	37
Sequence No:	1
Force Logoff:	-1
Domain Server State:	0x1
Server Role:	ROLE_DOMAIN_PDC
Unknown 3:	0x1
rpcclient $> getdompwinfo
min_password_length: 8
password_properties: 0x00000001
	DOMAIN_PASSWORD_COMPLEX
```

***

### **enum4linux**

Probemos esto usando [enum4linux](https://labs.portcullis.co.uk/tools/enum4linux) . `enum4linux` es una herramienta construida alrededor del [conjunto de herramientas Samba](https://www.samba.org/samba/docs/current/man-html/samba.7.html) `nmblookup` , `net` , `rpcclient` y `smbclient`para enumerar  hosts y dominios de Windows. Se puede encontrar preinstalado en muchas distribuciones de pruebas de penetración diferentes, incluido Parrot Security Linux. A continuación tenemos un resultado de ejemplo que muestra información que puede ser proporcionada por `enum4linux`. A continuación se muestran algunas herramientas de enumeración comunes y los puertos que utilizan:

<table data-header-hidden><thead><tr><th width="242"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Puertos</td></tr><tr><td><code>nmblookup</code></td><td>137/UDP</td></tr><tr><td><code>nbtstat</code></td><td>137/UDP</td></tr><tr><td><code>net</code></td><td>139/TCP, 135/TCP, TCP y UDP 135 y 49152-65535</td></tr><tr><td><code>rpcclient</code></td><td>135/TCP</td></tr><tr><td><code>smbclient</code></td><td>445/TCP</td></tr></tbody></table>

#### **Ejecutando enum4linux**

```shell-session
afsh4ck@kali$ enum4linux -P 172.16.5.5

<SNIP>

 ================================================== 
|    Password Policy Information for 172.16.5.5    |
 ================================================== 

[+] Attaching to 172.16.5.5 using a NULL share
[+] Trying protocol 139/SMB...

	[!] Protocol failed: Cannot request session (Called Name:172.16.5.5)

[+] Trying protocol 445/SMB...
[+] Found domain(s):

	[+] INLANEFREIGHT
	[+] Builtin

[+] Password Info for Domain: INLANEFREIGHT

	[+] Minimum password length: 8
	[+] Password history length: 24
	[+] Maximum password age: Not Set
	[+] Password Complexity Flags: 000001

		[+] Domain Refuse Password Change: 0
		[+] Domain Password Store Cleartext: 0
		[+] Domain Password Lockout Admins: 0
		[+] Domain Password No Clear Change: 0
		[+] Domain Password No Anon Change: 0
		[+] Domain Password Complex: 1

	[+] Minimum password age: 1 day 4 minutes 
	[+] Reset Account Lockout Counter: 30 minutes 
	[+] Locked Account Duration: 30 minutes 
	[+] Account Lockout Threshold: 5
	[+] Forced Log off Time: Not Set

[+] Retieved partial password policy with rpcclient:

Password Complexity: Enabled
Minimum Password Length: 8

enum4linux complete on Tue Feb 22 17:39:29 2022
```

La herramienta [enum4linux-ng](https://github.com/cddmp/enum4linux-ng) es una evolución de `enum4linux` en Python y tiene características adicionales como la capacidad de exportar datos como archivos YAML o JSON que luego pueden usarse para procesar más los datos o alimentarlos a otras herramientas. También admite salida en color, entre otras características.

### **enum4linux-ng**

```shell-session
afsh4ck@kali]$ enum4linux-ng -P 172.16.5.5 -oA ilfreight

ENUM4LINUX - next generation

<SNIP>

 =======================================
|    RPC Session Check on 172.16.5.5    |
 =======================================
[*] Check for null session
[+] Server allows session using username '', password ''
[*] Check for random user session
[-] Could not establish random user session: STATUS_LOGON_FAILURE

 =================================================
|    Domain Information via RPC for 172.16.5.5    |
 =================================================
[+] Domain: INLANEFREIGHT
[+] SID: S-1-5-21-3842939050-3880317879-2865463114
[+] Host is part of a domain (not a workgroup)

 =========================================================
|    Domain Information via SMB session for 172.16.5.5    |
========================================================
[*] Enumerating via unauthenticated SMB session on 445/tcp
[+] Found domain information via SMB
NetBIOS computer name: ACADEMY-EA-DC01
NetBIOS domain name: INLANEFREIGHT
DNS domain: INLANEFREIGHT.LOCAL
FQDN: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL

 =======================================
|    Policies via RPC for 172.16.5.5    |
 =======================================
[*] Trying port 445/tcp
[+] Found policy:
domain_password_information:
  pw_history_length: 24
  min_pw_length: 8
  min_pw_age: 1 day 4 minutes
  max_pw_age: not set
  pw_properties:
  - DOMAIN_PASSWORD_COMPLEX: true
  - DOMAIN_PASSWORD_NO_ANON_CHANGE: false
  - DOMAIN_PASSWORD_NO_CLEAR_CHANGE: false
  - DOMAIN_PASSWORD_LOCKOUT_ADMINS: false
  - DOMAIN_PASSWORD_PASSWORD_STORE_CLEARTEXT: false
  - DOMAIN_PASSWORD_REFUSE_PASSWORD_CHANGE: false
domain_lockout_information:
  lockout_observation_window: 30 minutes
  lockout_duration: 30 minutes
  lockout_threshold: 5
domain_logoff_information:
  force_logoff_time: not set

Completed after 5.41 seconds
```

Enum4linux-ng nos proporcionó una salida un poco más clara y una salida JSON y YAML útil usando la opción `-oA`.

**Mostrando el contenido de ilfreight.json**

```shell-session
afsh4ck@kali$ cat ilfreight.json 

{
    "target": {
        "host": "172.16.5.5",
        "workgroup": ""
    },
    "credentials": {
        "user": "",
        "password": "",
        "random_user": "yxditqpc"
    },
    "services": {
        "SMB": {
            "port": 445,
            "accessible": true
        },
        "SMB over NetBIOS": {
            "port": 139,
            "accessible": true
        }
    },
    "smb_dialects": {
        "SMB 1.0": false,
        "SMB 2.02": true,
        "SMB 2.1": true,
        "SMB 3.0": true,
        "SMB1 only": false,
        "Preferred dialect": "SMB 3.0",
        "SMB signing required": true
    },
    "sessions_possible": true,
    "null_session_possible": true,

<SNIP>
```

***

## <mark style="color:purple;">Enumeración de Null Sessions - Desde Windows</mark>

Es menos común realizar este tipo de ataque de sesión nula desde Windows, pero podríamos usar el comando `net use \\host\ipc$ "" /u:""` para establecer una sesión nula desde una máquina con Windows y confirmar si podemos realizar más ataques de este tipo.

**Establecer una sesión nula desde Windows**

```powershell
C:\htb> net use \\DC01\ipc$ "" /u:""
The command completed successfully.
```

También podemos usar una combinación de nombre de usuario y contraseña para intentar conectarnos. Veamos algunos errores comunes al intentar autenticarse:

<mark style="color:red;">**Error: la cuenta está deshabilitada**</mark>

```powershell
C:\htb> net use \\DC01\ipc$ "" /u:guest
System error 1331 has occurred.

This user can't sign in because this account is currently disabled.
```

<mark style="color:red;">**Error: la contraseña es incorrecta**</mark>

```cmd-session
C:\htb> net use \\DC01\ipc$ "password" /u:guest
System error 1326 has occurred.

The user name or password is incorrect.
```

<mark style="color:red;">**Error: La cuenta está bloqueada (Política de contraseñas)**</mark>

```cmd-session
C:\htb> net use \\DC01\ipc$ "password" /u:guest
System error 1909 has occurred.

The referenced account is currently locked out and may not be logged on to.
```

***

## <mark style="color:purple;">Enumeración de la política de contraseñas - Desde Linux - LDAP Anonymous Bind</mark>

[LDAP anonymous binds](https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/anonymous-ldap-operations-active-directory-disabled) permite a atacantes no autenticados recuperar información del dominio, como una lista completa de usuarios, grupos, computadoras, atributos de cuentas de usuario y la política de contraseñas del dominio. Esta es una configuración heredada y, a partir de Windows Server 2003, sólo los usuarios autenticados pueden iniciar solicitudes LDAP. Todavía vemos esta configuración de vez en cuando, ya que es posible que un administrador haya necesitado configurar una aplicación en particular para permitir enlaces anónimos y haber otorgado más acceso del previsto, dando así a los usuarios no autenticados acceso a todos los objetos en AD.

Con un enlace anónimo de LDAP, podemos utilizar herramientas de enumeración específicas de LDAP, como `windapsearch.py`, `ldapsearch`, `ad-ldapdomaindump.py` etc., para extraer la política de contraseñas. Con [ldapsearch](https://linux.die.net/man/1/ldapsearch) , puede resultar un poco engorroso pero factible. Un comando de ejemplo para obtener la política de contraseñas es el siguiente:

**Usando ldapsearch**

```shell-session
afsh4ck@kali$ ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "*" | grep -m 1 -B 10 pwdHistoryLength

forceLogoff: -9223372036854775808
lockoutDuration: -18000000000
lockOutObservationWindow: -18000000000
lockoutThreshold: 5
maxPwdAge: -9223372036854775808
minPwdAge: -864000000000
minPwdLength: 8
modifiedCountAtLastProm: 0
nextRid: 1002
pwdProperties: 1
pwdHistoryLength: 24
```

Aquí podemos ver la longitud mínima de la contraseña de 8, el umbral de bloqueo de 5 y la complejidad de la contraseña establecida ( `pwdProperties` establecida en `1`).

***

## <mark style="color:purple;">Enumeración de la política de contraseñas - Desde Windows</mark>

Si podemos autenticarnos en el dominio desde un host de Windows, podemos usar archivos binarios integrados de Windows, como `net.exe` para recuperar la política de contraseñas. También podemos utilizar diversas herramientas como `PowerView`, `CrackMapExec` portado a Windows, `SharpMapExec`, `SharpView`, etc.

El uso de comandos integrados es útil si llegamos a un sistema Windows y no podemos transferirle herramientas, o si el cliente nos coloca en un sistema Windows, pero no tenemos forma de instalar herramientas en él. Un ejemplo que utiliza el binario `net.exe` integrado es:

### **Usando net.exe**

```powershell
C:\htb> net accounts

Force user logoff how long after time expires?:       Never
Minimum password age (days):                          1
Maximum password age (days):                          Unlimited
Minimum password length:                              8
Length of password history maintained:                24
Lockout threshold:                                    5
Lockout duration (minutes):                           30
Lockout observation window (minutes):                 30
Computer role:                                        SERVER
The command completed successfully.
```

Aquí podemos recoger la siguiente información:

* `Las contraseñas nunca caducan` (la antigüedad máxima de la contraseña se establece en `Unlimited`)
* `La longitud mínima de la contraseña es 8`, por lo que es probable que se utilicen contraseñas débiles.
* `El umbral de bloqueo es 5` contraseñas incorrectas
* `Las cuentas permanecen bloqueadas durante 30 minutos`

Esta política de contraseñas es excelente para la pulverización de contraseñas. El mínimo de ocho caracteres significa que podemos probar contraseñas débiles comunes como `Welcome1`. El umbral de bloqueo de 5 significa que podemos intentar 2-3 (para estar seguros) pulverizaciones cada 31 minutos sin el riesgo de bloquear ninguna cuenta. Si una cuenta ha sido bloqueada, se desbloqueará automáticamente (sin intervención manual de un administrador) después de 30 minutos, pero debemos evitar bloquear cuentas a toda costa.

PowerView también es bastante útil para esto:

### **Usando PowerView**

```powershell
PS C:\htb> import-module .\PowerView.ps1
PS C:\htb> Get-DomainPolicy

Unicode        : @{Unicode=yes}
SystemAccess   : @{MinimumPasswordAge=1; MaximumPasswordAge=-1; MinimumPasswordLength=8; PasswordComplexity=1;
                 PasswordHistorySize=24; LockoutBadCount=5; ResetLockoutCount=30; LockoutDuration=30;
                 RequireLogonToChangePassword=0; ForceLogoffWhenHourExpire=0; ClearTextPassword=0;
                 LSAAnonymousNameLookup=0}
KerberosPolicy : @{MaxTicketAge=10; MaxRenewAge=7; MaxServiceAge=600; MaxClockSkew=5; TicketValidateClient=1}
Version        : @{signature="$CHICAGO$"; Revision=1}
RegistryValues : @{MACHINE\System\CurrentControlSet\Control\Lsa\NoLMHash=System.Object[]}
Path           : \\INLANEFREIGHT.LOCAL\sysvol\INLANEFREIGHT.LOCAL\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHI
                 NE\Microsoft\Windows NT\SecEdit\GptTmpl.inf
GPOName        : {31B2F340-016D-11D2-945F-00C04FB984F9}
GPODisplayName : Default Domain Policy
```

PowerView nos dio el mismo resultado que nuestro comando `net accounts`, solo que en un formato diferente, pero también reveló que la complejidad de la contraseña está habilitada ( `PasswordComplexity=1`).

Al igual que con Linux, tenemos muchas herramientas a nuestra disposición para recuperar la política de contraseñas mientras estamos en un sistema Windows, ya sea nuestro sistema de ataque o un sistema proporcionado por el cliente. PowerView/SharpView siempre son buenas apuestas, al igual que CrackMapExec, SharpMapExec y otros. La elección de las herramientas depende del objetivo de la evaluación, las consideraciones de sigilo, cualquier antivirus o EDR implementado y otras posibles restricciones en el host de destino. Cubramos algunos ejemplos.

***

## <mark style="color:purple;">Análisis de la política de contraseñas</mark>

Ahora hemos eliminado la política de contraseñas de numerosas maneras. Repasemos la política para el dominio `INLANEFREIGHT.LOCAL` pieza por pieza.

* `La longitud mínima de la contraseña es 8` (8 es muy común, pero hoy en día, vemos que cada vez más organizaciones imponen una contraseña de 10 a 14 caracteres, lo que puede eliminar algunas opciones de contraseña para nosotros, pero no mitiga por completo el vector de dispersión de contraseñas).
* `El umbral de bloqueo de la cuenta es 5` (no es raro ver un umbral más bajo, como 3, o incluso ningún umbral de bloqueo establecido)
* `La duración del bloqueo es de 30 minutos` (puede ser mayor o menor dependiendo de la organización), por lo que si accidentalmente bloqueamos (¡evitamos!) una cuenta, se desbloqueará después de que pase el período de 30 minutos.
* `Las cuentas se desbloquean automáticamente` (en algunas organizaciones, un administrador debe desbloquear la cuenta manualmente). Nunca queremos bloquear cuentas mientras realizamos la pulverización de contraseñas, pero queremos especialmente evitar bloquear cuentas en una organización donde un administrador tendría que intervenir y desbloquear cientos (o miles) de cuentas manualmente o mediante script.
* `La complejidad de la contraseña está habilitada`, lo que significa que un usuario debe elegir una contraseña con 3/4 de los siguientes: una letra mayúscula, una letra minúscula, un número, un carácter especial ( `Password1`o `Welcome1` satisfaría el requisito de "complejidad" aquí, pero siguen siendo contraseñas claramente débiles). .

La política de contraseña predeterminada cuando se crea un nuevo dominio es la siguiente, y ha habido muchas organizaciones que nunca cambiaron esta política:

<table data-header-hidden><thead><tr><th width="491"></th><th></th></tr></thead><tbody><tr><td><strong>Política</strong></td><td><strong>Valor por defecto</strong></td></tr><tr><td>Hacer cumplir el historial de contraseñas</td><td>24 dias</td></tr><tr><td>Edad máxima de la contraseña</td><td>42 dias</td></tr><tr><td>Edad mínima de la contraseña</td><td>1 día</td></tr><tr><td>Longitud mínima de la contraseña</td><td>7</td></tr><tr><td>La clave debe cumplir los requerimientos de complejidad</td><td>Activado</td></tr><tr><td>Almacene contraseñas mediante cifrado reversible</td><td>Desactivado</td></tr><tr><td>Duración del bloqueo de cuenta</td><td>No establecido</td></tr><tr><td>Umbral de bloqueo de cuenta</td><td>0</td></tr><tr><td>Restablecer el contador de bloqueo de cuenta después</td><td>No establecido</td></tr></tbody></table>

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.42.75 (ACADEMY-EA-ATTACK01)
Usuario " htb-student " 
Contraseña " HTB_@cademy_stdnt! "
```

### Pregunta 1

¿Cuál es el valor `minPwdLength` establecido en el dominio INLANEFREIGHT.LOCAL?

```
┌─[htb-student@ea-attack01]─[~]
└──╼ $enum4linux-ng -P 172.16.5.5 -oA ilfreight
ENUM4LINUX - next generation

<----SNIP---->

 =======================================
|    Policies via RPC for 172.16.5.5    |
 =======================================
[*] Trying port 445/tcp
[+] Found policy:
domain_password_information:
  pw_history_length: 24
  min_pw_length: 8
  min_pw_age: 1 day 4 minutes
  max_pw_age: not set
  pw_properties:
  - DOMAIN_PASSWORD_COMPLEX: true
  - DOMAIN_PASSWORD_NO_ANON_CHANGE: false
  - DOMAIN_PASSWORD_NO_CLEAR_CHANGE: false
  - DOMAIN_PASSWORD_LOCKOUT_ADMINS: false
  - DOMAIN_PASSWORD_PASSWORD_STORE_CLEARTEXT: false
  - DOMAIN_PASSWORD_REFUSE_PASSWORD_CHANGE: false
domain_lockout_information:
  lockout_observation_window: 30 minutes
  lockout_duration: 30 minutes
  lockout_threshold: 5
domain_logoff_information:
  force_logoff_time: not set
```

La longitud mínima de contraseña es: `8 caracteres`

***

## <mark style="color:purple;">Próximos pasos</mark>

Ahora que tenemos la política de contraseñas a mano, necesitamos crear una lista de usuarios objetivo para realizar nuestro ataque de pulverización de contraseñas. Recuerde que a veces no podremos obtener la política de contraseñas si estamos realizando una pulverización externa de contraseñas (o si estamos en una evaluación interna y no podemos recuperar la política utilizando ninguno de los métodos que se muestran aquí).&#x20;

En estos casos, `DEBEMOS` extremar las precauciones para no bloquear cuentas. Siempre podemos preguntar a nuestro cliente su política de contraseñas si el objetivo es una evaluación lo más completa posible. Si solicitar la política no se ajusta a las expectativas de la evaluación o el cliente no quiere proporcionarla, debemos ejecutar uno, máximo dos, intentos de pulverización de contraseña (independientemente de si somos internos o externos) y esperar más de una hora entre intentos si realmente decidimos intentar dos.&#x20;

Si bien la mayoría de las organizaciones tendrán un umbral de bloqueo de 5 intentos de contraseña incorrectos, una duración de bloqueo de 30 minutos y las cuentas se desbloquearán automáticamente, no siempre podemos contar con que esto sea normal. He visto muchas organizaciones con un umbral de bloqueo de 3, lo que requiere que un administrador intervenga y desbloquee las cuentas manualmente.
