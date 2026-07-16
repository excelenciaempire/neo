
# Metasploitable 3

{% embed url="<https://github.com/rapid7/metasploitable3?tab=readme-ov-file>" %}

## <mark style="color:purple;">Instalación en VMWare</mark>

Para instalarlo de forma gratuíta en VMWare no podemos hacerlo a través de vagrant como indica en las instrucciones del repositorio, ya que esto utiliza un plugin de pago. Para ello vamos a instalarlo de la siguiente manera:

{% embed url="<https://youtu.be/hi0-2Hn2QUk?si=QaW0-VPpYKUEudoV>" %}

### <mark style="color:purple;">1. Descargar los archivos oficiales</mark>

{% embed url="<https://portal.cloud.hashicorp.com/vagrant/discover/rapid7>" %}

<figure><img src="/files/6TNUhYFNbG4e3nJ4GtvT" alt=""><figcaption></figcaption></figure>

Vamos a descargar los ejecutables de ambas máquinas, concretamente la que pone `vmware_desktop`:

<figure><img src="/files/R8QVqr1b6iglO2xafjM4" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;">2. Manipulación de archivos</mark>

Una vez descargados tendremos 2 archivos con un nombre random que no podemos virtualizar directamente en vmware, por lo que tendremos que cambiar su nombre y añadirle `.zip` al final:

<figure><img src="/files/Kj9k8wSjdFFVSbFu5Fsh" alt=""><figcaption></figcaption></figure>

1. Archivo sin modificar de la máquina Linux
2. Archivo con el nombre modificado de la máquina Windows

Ahora que tenemos los archivos con la extensión `.zip` vamos a descomprimirlos (recomiendo Winrar) y lo extraemos en la carpeta:

<figure><img src="/files/O4qoRsgwwyC1xF4ZtYqQ" alt=""><figcaption></figcaption></figure>

Esto nos va a generar una carpeta y dentro otro archivo que debemos cambiarle la extensión a `.zip` y que ya nos va a extraer los archivos necesarios para virtualizarlo:

{% hint style="info" %}
Fijaros que nos genera un archivo que ocupa 14gb para la máquina virtual Windows
{% endhint %}

<figure><img src="/files/ntrSpaz8DODXYYDoZjOL" alt=""><figcaption></figcaption></figure>

Una vez renombrado lo extraemos en la misma carpeta:

<figure><img src="/files/nUr6gGGJSNtM4AGENZ48" alt=""><figcaption></figcaption></figure>

Una vez extraídos los archivos podemos eliminar el zip original para que no ocupe espacio en disco y importamos el archivo de configuración en VMWare:

<figure><img src="/files/JH0DM4F7uEOnkz6oimLe" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;">3. Virtualizar máquinas</mark>

Ahora tendríamos 2 carpetas con los archivos necesarios:

* Una carpeta con todos los archivos de la máquina Windows Server 2008 R2
* Una carpeta con todos los archivos de la máquina Linux Ubuntu

Para instalar estas máquinas en VMWare es tan sencillo como arrastrar a la ventana de VMWare los archivos de configuración de cada máquina.

### <mark style="color:purple;">4. Activar Metasploitable</mark>

Esta máquina Metasploitable 3 utiliza una versión de Windows de desarrollo sin una licencia, por lo que cada ciertos minutos se reinicia y es incómodo.

Podemos activar la licencia de la máquina Windows de forma permanente escribiendo el siguiente comando en la powershell:

```bash
irm https://get.activated.win | iex
```

En el menú que nos aparece se nos marcará en verde las opciones compatibles, en nuestro caso seleccionaremos TSforge:

<figure><img src="/files/Cd29K6odTHkguwJvMWCy" alt=""><figcaption></figcaption></figure>

Y aquí seleccionamos la opción 5: `Activate - All`

<figure><img src="/files/f4SymaLGaJM6gKQ0F0f4" alt=""><figcaption></figcaption></figure>

Eso activará la licencia de forma permanente en el equipo:

<figure><img src="/files/ysP5uCX3YtIiYKXmvCXS" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Guías de explotación</mark>

### Máquina Windows

{% embed url="<https://github.com/rapid7/metasploitable3/wiki/Vulnerabilities>" %}

Al acceder a la máquina Windows podemos acceder como:

* `Administrator:vagrant`
* `vagrant:vagrant`

<figure><img src="/files/2FXo08BVUeHf16cnLuOv" alt=""><figcaption></figcaption></figure>

Con `ipconfig` vemos la IP de la máquina, la cual usaremos para atacar a esta máquina en nuestro entorno local:

<figure><img src="/files/kdZw9PYuEATIzSMGlBve" alt=""><figcaption></figcaption></figure>

#### Configurar el teclado en español (Windows)

Es necesario cambiar el idioma del teclado ya que por defecto viene en inglés. Para ello vamos a hacer lo siguiente:

<figure><img src="/files/nhyPn2C1sgOCzUtc7DII" alt=""><figcaption></figcaption></figure>

1. Abrimos el panel de control
2. Keyboard
3. Region & Language > Change keyboards
4. Add
5. Seleccionamos el idioma español
6. Apply > OK

Con eso ya tendremos el teclado bien configurado en español.

<figure><img src="/files/LWTyTcrMeKODUGTcasrS" alt=""><figcaption></figcaption></figure>

### Máquina Linux Ubuntu

{% embed url="<https://stuffwithaurum.com/2020/04/17/metasploitable-3-linux-an-exploitation-guide/>" %}

#### Configurar el teclado en español (Linux)

Por defecto Metasploitable usa un teclado en inglés, que no coincide con el layout de otros idiomas, lo que dificulta bastante la escritura en la terminal o en el sistema.

Para cambiar el idioma del teclado solo tenemos que ejecutar:

```bash
apt update && apt install -y console-data console-setup keyboard-configuration
dpkg-reconfigure keyboard-configuration
setupcon
```

Deberemos seleccionar nuestro idioma y se ajustará automáticamente. Si cambia la fuente de la terminal, podemos restaurarlo a la configuración original con:

```bash
nano /etc/default/console-setup
```

```bash
FONTFACE="VGA"
FONTSIZE="16"
```

```bash
setupcon
# o
systemctl restart console-setup
```
