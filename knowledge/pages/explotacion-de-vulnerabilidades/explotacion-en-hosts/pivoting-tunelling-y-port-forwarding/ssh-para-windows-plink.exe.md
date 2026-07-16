
# SSH para Windows: plink.exe

## plink.exe

***

[Plink](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) , abreviatura de PuTTY Link, es una herramienta SSH de línea de comandos de Windows que viene como parte del paquete PuTTY cuando se instala. Al igual que SSH, Plink también se puede utilizar para crear reenvíos de puertos dinámicos y proxies SOCKS. Antes del otoño de [2018](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview) , Windows no incluía un cliente ssh nativo, por lo que los usuarios tenían que instalar el suyo propio. La herramienta elegida por muchos administradores de sistemas que necesitaban conectarse a otros hosts fue [PuTTY](https://www.putty.org/) .

Imaginemos que estamos en un pentest y accedemos a una máquina con Windows. Enumeramos rápidamente el host y su postura de seguridad y determinamos que está moderadamente bloqueado. Necesitamos utilizar este host como punto de pivote, pero es poco probable que podamos colocar nuestras propias herramientas en el host sin quedar expuestos. En cambio, podemos vivir de la tierra y utilizar lo que ya está allí. Si el host es más antiguo y PuTTY está presente (o podemos encontrar una copia en un archivo compartido), Plink puede ser nuestro camino hacia la victoria. Podemos usarlo para crear nuestro pivote y potencialmente evitar la detección por un poco más de tiempo.

Éste es sólo un escenario potencial en el que Plink podría resultar beneficioso. También podríamos usar Plink si usamos un sistema Windows como nuestro principal host de ataque en lugar de un sistema basado en Linux.

***

### Conociendo a Plink

En la imagen de abajo, tenemos un host de ataque basado en Windows.

![](https://academy.hackthebox.com/storage/modules/158/66.png)

El host de ataque de Windows inicia un proceso plink.exe con los siguientes argumentos de línea de comandos para iniciar un puerto dinámico hacia el servidor Ubuntu. Esto inicia una sesión SSH entre el host de ataque de Windows y el servidor Ubuntu, y luego plink comienza a escuchar en el puerto 9050.

### **Uso de Plink.exe**

```cmd-session
plink -ssh -D 9050 ubuntu@10.129.15.50
```

Se puede utilizar otra herramienta basada en Windows llamada [Proxifier](https://www.proxifier.com/) para iniciar un túnel SOCKS a través de la sesión SSH que creamos. Proxifier es una herramienta de Windows que crea una red en túnel para aplicaciones cliente de escritorio y le permite operar a través de un proxy SOCKS o HTTPS y permite el encadenamiento de proxy. Es posible crear un perfil donde podamos proporcionar la configuración de nuestro servidor SOCKS iniciado por Plink en el puerto 9050.

![](https://academy.hackthebox.com/storage/modules/158/reverse_shell_9.png)

Después de configurar el servidor SOCKS para `127.0.0.1`el puerto 9050, podemos comenzar directamente `mstsc.exe`a iniciar una sesión RDP con un destino de Windows que permita conexiones RDP.
