
# The Metasploit Framework - CTF 2

Los sistemas basados ​​en Linux son frecuentemente objetivo de pruebas de penetración debido a su prevalencia en entornos de servidores. Este laboratorio se centra en el uso de Metasploit Framework (MSF) para explotar servicios mal configurados y aplicaciones vulnerables en sistemas Linux. Los participantes utilizarán MSF para enumerar servicios, explorar sistemas de archivos y explotar aplicaciones web para obtener acceso a la línea de comandos.

***

## <mark style="color:$primary;">Tarea 1</mark>

> Enumera los puertos abiertos usando Metasploit e inspecciona detenidamente el banner RSYNC; podría revelar algo interesante.

### Target

Nuestro objetivo es `target.ine.local`:

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.5        INE
127.0.0.1 AttackDefense-Kali
10.10.49.2      INE
10.2.30.41    target.ine.local
```

### Escaneo de puertos

```bash
┌──(root㉿INE)-[~]
└─# nmap -v -sV target.ine.local

PORT      STATE SERVICE            VERSION
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
1433/tcp  open  ms-sql-s           Microsoft SQL Server 2012 11.00.6020; SP3
3389/tcp  open  ssl/ms-wbt-server?
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49154/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
```

Vemos que hay MSSQL por el puerto 1433.

***

## <mark style="color:$primary;">Tarea 2</mark>

> Los archivos del servidor RSYNC contienen información valiosa. Explora su contenido para encontrar la flag.

***

## <mark style="color:$primary;">Tarea 3</mark>

> Intenta explotar la aplicación web para obtener una shell usando Metasploit en target2.ine.local.

***

## <mark style="color:$primary;">Tarea 4</mark>

> Las tareas automatizadas a veces pueden dejar pistas. Investiga los trabajos programados o los procesos en ejecución para descubrir la flag oculta.
