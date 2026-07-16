
# Port Forwarding con Windows Netsh

[Netsh](https://docs.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-contexts) es una herramienta de línea de comandos de Windows que puede ayudar con la configuración de red de un sistema Windows en particular. Estas son solo algunas de las tareas relacionadas con las redes que podemos utilizar `Netsh` para:

* `Encontrar rutas`&#x20;
* `Ver la configuración del firewall`&#x20;
* `Agregar servidores proxy`&#x20;
* `Crear reglas de Port Forwarding`

Tomemos un ejemplo del siguiente escenario en el que nuestro host comprometido es la estación de trabajo de un administrador de TI basada en Windows 10 ( `10.129.15.150`, `172.16.5.25`). Tenga en cuenta que es posible que en un contrato podamos obtener acceso a la estación de trabajo de un empleado a través de métodos como la ingeniería social y el phishing. Esto nos permitiría girar más lejos de la red en la que se encuentra la estación de trabajo.

![](https://academy.hackthebox.com/storage/modules/158/88.png)

Podemos usarlo `netsh.exe` para reenviar todos los datos recibidos en un puerto específico (digamos 8080) a un host remoto en un puerto remoto. Esto se puede realizar usando el siguiente comando.

### **Usando Netsh.exe para Port Forwarding**

```cmd-session
C:\Windows\system32> netsh.exe interface portproxy add v4tov4 listenport=8080 listenaddress=10.129.15.150 connectport=3389 connectaddress=172.16.5.25
```

### **Verificación de Port Forwarding**

```powershell
C:\Windows\system32> netsh.exe interface portproxy show v4tov4

Listen on ipv4:             Connect to ipv4:

Address         Port        Address         Port
--------------- ----------  --------------- ----------
10.129.42.198   8080        172.16.5.25     3389
```

Después de configurar `portproxy` nuestro host pivote basado en Windows, intentaremos conectarnos al puerto 8080 de este host desde nuestro host de ataque usando xfreerdp. Una vez que se envía una solicitud desde nuestro host de ataque, el host de Windows enrutará nuestro tráfico de acuerdo con la configuración del proxy configurada por netsh.exe.

### **Conexión al host interno a través de Port Forwarding**

![](https://academy.hackthebox.com/storage/modules/158/netsh_pivot.png)

## <mark style="color:purple;">Caso práctico</mark>

Utilizando los conceptos cubiertos en esta sección, tome el control del DC (`172.16.5.19`) usando xfreerdp pivotando a través del host de destino de Windows 10. Envíe el nombre del contacto que se encuentra dentro del archivo "`VendorContacts.txt`" ubicado en la carpeta "Approved Vendors" en el escritorio de Victor&#x20;

### Datos de acceso

```
RDP a 10.129.42.198 con usuario "htb-student" y contraseña "HTB_@cademy_stdnt!"
```

```
Credenciales de Victor: victor:pass@123
```

### Conexión por RDP

```
xfreerdp /v:10.129.42.198 /u:htb-student /p:'HTB_@cademy_stdnt!'
```

<figure><img src="/files/p1QjLyvH7wBSvAgcrN4u" alt=""><figcaption></figcaption></figure>

La IP de la máquina es `10.129.42.198` y la de la red interna `172.16.5.150`

### Ejecutar Netsh

```
netsh.exe interface portproxy add v4tov4 listenport=8080 listenaddress=10.129.42.198 connectport=3389 connectaddress=172.16.5.19 
```

### Comprobación de Port Forwarding

```powershell
PS C:\Windows\system32> netsh.exe interface portproxy show v4tov4                                      
Listen on ipv4:             Connect to ipv4:

Address         Port        Address         Port
--------------- ----------  --------------- ----------
10.129.42.198   8080        172.16.5.19     3389
```

<figure><img src="/files/OgHGY0tSBPAVS5IV7slo" alt=""><figcaption></figcaption></figure>

### Conexión al DC con Port Forwarding

```
xfreerdp /v:10.129.42.198:8080 /u:victor /p:'pass@123'
```

<figure><img src="/files/VyO46GR5B3wMIE0xpoio" alt=""><figcaption></figcaption></figure>
