
# Footprinting Lab - Medium

## <mark style="color:purple;">Introducción</mark>

***

Este segundo servidor es un servidor al que tienen acceso todos los usuarios de la red interna. En nuestra conversación con nuestro cliente, señalamos que estos servidores son a menudo uno de los principales objetivos de los atacantes y que este servidor debería agregarse al alcance.

Nuestro cliente aceptó esto y agregó este servidor a nuestro alcance. También en este caso el objetivo sigue siendo el mismo. Necesitamos encontrar la mayor cantidad de información posible sobre este servidor y encontrar formas de usarla contra el mismo. Para la comprobación y protección de los datos del cliente se ha creado un usuario denominado `HTB` . En consecuencia, necesitamos obtener las credenciales de este usuario como prueba.

***

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV 10.129.193.210

PORT     STATE SERVICE       VERSION
111/tcp  open  rpcbind       2-4 (RPC #100000)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
2049/tcp open  mountd        1-3 (RPC #100005)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

```bash
sudo nmap -v -sCV -A -T5 10.129.193.210

PORT     STATE SERVICE       VERSION
111/tcp  open  rpcbind       2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/tcp6  rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  2,3,4        111/udp6  rpcbind
|   100003  2,3         2049/udp   nfs
|   100003  2,3         2049/udp6  nfs
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/tcp6  nfs
|   100005  1,2,3       2049/tcp   mountd
|   100005  1,2,3       2049/tcp6  mountd
|   100005  1,2,3       2049/udp   mountd
|   100005  1,2,3       2049/udp6  mountd
|   100021  1,2,3,4     2049/tcp   nlockmgr
|   100021  1,2,3,4     2049/tcp6  nlockmgr
|   100021  1,2,3,4     2049/udp   nlockmgr
|   100021  1,2,3,4     2049/udp6  nlockmgr
|   100024  1           2049/tcp   status
|   100024  1           2049/tcp6  status
|   100024  1           2049/udp   status
|_  100024  1           2049/udp6  status
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
2049/tcp open  nlockmgr      1-4 (RPC #100021)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: WINMEDIUM
|   NetBIOS_Domain_Name: WINMEDIUM
|   NetBIOS_Computer_Name: WINMEDIUM
|   DNS_Domain_Name: WINMEDIUM
|   DNS_Computer_Name: WINMEDIUM
|   Product_Version: 10.0.17763
|_  System_Time: 2024-02-09T13:57:24+00:00
|_ssl-date: 2024-02-09T13:57:35+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=WINMEDIUM
| Issuer: commonName=WINMEDIUM
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2024-02-08T13:54:38
| Not valid after:  2024-08-09T13:54:38
| MD5:   d35e:ad5c:ed34:6089:daeb:d38c:0709:8df2
|_SHA-1: 2071:d6a7:0897:89a4:5dce:b2e2:7801:a5ce:a8f6:1b12

Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-02-09T13:57:29
|_  start_date: N/A

TRACEROUTE (using port 443/tcp)
HOP RTT      ADDRESS
1   42.35 ms 10.10.14.1
2   42.57 ms 10.129.162.185
```

Empezemos por NFS. Puede ser trivial acceder a NFS si está mal configurado. Lo primero que hay que considerar son los puertos en los que opera NFS, `TCP/111` y `TCP/2049`. Usando Metasploit para escanear el servicio, encontramos un recurso compartido montable en el que podamos hurgar: `/TechSupport`

```
[msf](Jobs:0 Agents:0) auxiliary(scanner/nfs/nfsmount) >> run

[*] 10.129.193.210:111    - 10.129.193.210 NFS Export: /TechSupport []
[*] 10.129.193.210:111    - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

## <mark style="color:purple;">Montando NFS</mark>

Ahora vamos a montar este directorio en local con el siguiente comando:

```bash
mount -t nfs 10.129.193.210:/TechSupport /home/kali/Escritorio/machines/Footprint-Labs/medium
```

Al acceder nos encontramos con un montón de `ticket.txt`, la mayoría vacíos menos 1:

<figure><img src="/files/o9lDcCzh63i9NoaVpOiW" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/eJehS2KtWPosCwlGvQaA" alt=""><figcaption></figcaption></figure>

Al abrir este archivo nos encontramos una conversación con información relevante:

```bash
cat ticket4238791283782.txt

Conversation with InlaneFreight Ltd

Started on November 10, 2021 at 01:27 PM London time GMT (GMT+0200)
---
01:27 PM | Operator: Hello,. 
 
So what brings you here today?
01:27 PM | alex: hello
01:27 PM | Operator: Hey alex!
01:27 PM | Operator: What do you need help with?
01:36 PM | alex: I run into an issue with the web config file on the system for the smtp server. do you mind to take a look at the config?
01:38 PM | Operator: Of course
01:42 PM | alex: here it is:

 1smtp {
 2    host=smtp.web.dev.inlanefreight.htb
 3    #port=25
 4    ssl=true
 5    user="alex"
 6    password="lol123!mD"
 7    from="alex.g@web.dev.inlanefreight.htb"
 8}
 9
10securesocial {
11    
12    onLoginGoTo=/
13    onLogoutGoTo=/login
14    ssl=false
15    
16    userpass {      
17    	withUserNameSupport=false
18    	sendWelcomeEmail=true
19    	enableGravatarSupport=true
20    	signupSkipLogin=true
21    	tokenDuration=60
22    	tokenDeleteInterval=5
23    	minimumPasswordLength=8
24    	enableTokenJob=true
25    	hasher=bcrypt
26	}
27
28     cookie {
29     #       name=id
30     #       path=/login
31     #       domain="10.129.2.59:9500"
32            httpOnly=true
33            makeTransient=false
34            absoluteTimeoutInMinutes=1440
35            idleTimeoutInMinutes=1440
36    }   
```

```
User:  alex
Pass:  lol123!mD
Host:  smtp.web.dev.inlanefreight.htb
Email: alex.g@web.dev.inlanefreight.htb
```

Al intentar conectarnos por `xfreerdp` nos da un error, debido a la exclamación en la contraseña, por lo que vamos a utilizar otro gestor, como `Remmina`:

<figure><img src="/files/AIxGMyPx9nKkbiOyBpkg" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Configurando Remmina</mark>

```bash
sudo apt-get update
sudo apt-get -y install remmina
```

Iniciamos la GUI de Remmina y lo configuramos con las siguientes credenciales:

<figure><img src="/files/htVst5OF5scTNn29rmW2" alt=""><figcaption></figcaption></figure>

Accedemos correctamente al sistema y lo podemos controlar remotamente.

<figure><img src="/files/3Ortgw4xxG6a6gi9sxkR" alt=""><figcaption></figcaption></figure>

Una vez dentro, vamos a acceder a SQL Management Studio, desde el link del escritorio.

<figure><img src="/files/DuZBff6RrVUgYjgXFAUx" alt=""><figcaption></figcaption></figure>

Al intentar loguearnos y probar todos los métodos de autenticación, nos da el siguiente error, por lo que tendremos que explorar un poco el sistema de archivos:

<figure><img src="/files/MkBcbIiw1yYEDoU4v361" alt=""><figcaption></figcaption></figure>

Abrimos una powershell y vemos los archivos del sistema. Nos encontramos la carpeta que ya nos descargamos en local `TechSupport` y una carpeta `devshare`:

<figure><img src="/files/mNZ66MarwAYdmkOOoJ6e" alt=""><figcaption></figcaption></figure>

Accedemos a `devshare` y nos encontramos el archivo `important.txt`

<figure><img src="/files/NV2cWpYt8XKYL6UccA24" alt=""><figcaption></figcaption></figure>

Lo abrimos y encontramos las credenciales de acceso para el usuario `sa` o `System Admin`:

```
sa:87N1ns@slls83
```

En este punto vamos a iniciar el SQL Management Studio como administrador y vamos a probar con estas credenciales:

<figure><img src="/files/KWXpRHufzNIDAHztKzWE" alt=""><figcaption><p>Ejecutar SQL Server Management como Administrador</p></figcaption></figure>

Funciona y entramos correctamente como `Administrator`:

<figure><img src="/files/0JIrXn7jbzLm8FqFEhVr" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Enumeración de la base de datos</mark>

En este punto podemos empezar a utilizar distintas Queys para enumerar información sobre los usuarios del sistema:

<figure><img src="/files/LoCIN2KKMsj8HDmra9Q0" alt=""><figcaption></figcaption></figure>

También necesitamos saber las tablas que contiene en este caso la base de datos `accounts` con la siguiente Query:

<figure><img src="/files/uoVWj6skjPuQJf0rz16A" alt=""><figcaption></figcaption></figure>

Y bumm, accedemos a las credenciales de todos los usuarios:

<figure><img src="/files/0ni3UfQCQukedjdJAUmz" alt=""><figcaption></figcaption></figure>

Y conseguimos encontrar la contraseña del usuario HTB 🏆

<figure><img src="/files/oNOdZvnsRL6usXPIYejg" alt=""><figcaption></figcaption></figure>
