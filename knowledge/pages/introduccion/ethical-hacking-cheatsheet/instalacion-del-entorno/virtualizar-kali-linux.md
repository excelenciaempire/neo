
# Virtualizar Kali Linux

## <mark style="color:purple;">**Video de instalación**</mark>

{% embed url="<https://youtu.be/xevyl1R2AYI>" %}

## <mark style="color:purple;">Requisitos previos</mark>

### VMware Workstation Pro o VMware Fusion (para MacOS)

Si no tienes VMware instalado, puedes descargarlo desde su sitio web oficial.

{% content-ref url="/pages/F2VJnrkdbHtu9h7MTLux" %}
[Instalación de VMWare](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/instalacion-del-entorno/instalacion-de-vmware.md)
{% endcontent-ref %}

### ISO de Kali Linux

Necesitarás el archivo de instalación de Kali Linux. Puedes descargarlo desde el sitio oficial:

{% embed url="<https://www.kali.org/>" %}

Asegúrate de descargar la versión de 64 bits o la que sea compatible con tu hardware.

## <mark style="color:purple;">Guía para virtualizar Kali Linux en VMware</mark>

### 1. Instalar VMware Workstation Player o Pro

Si no tienes VMware instalado, descárgalo e instálalo siguiendo los pasos estándar:

* Descarga el archivo de instalación desde el sitio de VMware.
* Ejecuta el archivo de instalación y sigue las instrucciones para completar la instalación.
* Una vez instalado, abre VMware Workstation Player o Pro.

### 2. Crear una nueva máquina virtual

1. &#x20;Abre VMware.
2. &#x20;En el menú principal, selecciona “Create a New Virtual Machine”.
3. &#x20;Aparecerá un asistente para configurar la nueva máquina virtual:

* Elige “Installer disc image file (iso)” y busca el archivo ISO de Kali Linux que descargaste.
* Haz clic en Next.

### 3. Seleccionar sistema operativo invitado

* En la siguiente pantalla, selecciona “`Linux`” como tipo de sistema operativo.
* En la lista de versiones, elige `Debian 10.x 64-bit` (Kali Linux está basado en Debian).
* Haz clic en Next.

### 4. Asignar un nombre a la máquina virtual

* Asigna un nombre para tu máquina virtual, como “Kali Linux”.
* Elige la ubicación donde se guardará la máquina virtual en tu disco.
* Haz clic en Next.

### 5. Asignar almacenamiento de disco

* Se te pedirá que asignes espacio en disco. Selecciona un tamaño adecuado para la instalación. 20 GB es recomendable para Kali Linux.
* Selecciona la opción “Store virtual disk as a single file” para mejor rendimiento.
* Haz clic en Next.

### 6. Configurar la memoria (RAM)

* Antes de finalizar, ajusta la memoria (RAM) asignada a la máquina virtual.  2 GB (2048 MB) es suficiente, pero si tienes más RAM en tu sistema, asignar 4 GB (4096 MB) mejorará el rendimiento.
* Haz clic en Next.

### 7. Configurar procesadores y otras opciones

* Para mejorar el rendimiento, puedes asignar 2 CPUs o más si tu sistema lo permite.
* Haz clic en Finish para completar la creación de la máquina virtual.

### 8. Ajustar la configuración de red (opcional)

* Antes de iniciar la máquina virtual, ve a “Edit Virtual Machine Settings”.
* En la sección Network Adapter, selecciona “`Bridged`” para que la máquina virtual tenga su propia dirección IP en la red, o deja “`NAT`” si quieres que comparta la conexión con el host.

### 9. Iniciar la máquina virtual e instalar Kali Linux

1. &#x20;Haz clic en Power on this virtual machine.
2. &#x20;La máquina virtual se iniciará desde el archivo ISO de Kali Linux.
3. &#x20;En el menú de arranque, selecciona “Graphical Install”.
4. &#x20;Sigue el asistente de instalación:

* Selecciona el idioma y la región.
* Configura el teclado.
* Elige un nombre de usuario y una contraseña (recuerda estos datos).
* En la sección de particionado de discos, selecciona “`Guided - Use entire disk`” para facilitar el proceso.

5\. Sigue las instrucciones para completar la instalación.

### 10. Configuración final

* Después de completar la instalación, reinicia la máquina virtual.
* Inicia sesión con el usuario y la contraseña que configuraste.
* Tu Kali Linux ya estará listo para usarse en VMware.

## <mark style="color:purple;">Optimización y herramientas adicionales</mark>

### <mark style="color:purple;">Instalar VMware Tools</mark>

VMware Tools permite una mejor integración con el sistema anfitrión, facilitando copiar/pegar entre el host y la máquina virtual, arrastrar y soltar archivos, y mejorar el rendimiento gráfico.

1\. Ve a Player en la barra de menús de VMware.

2\. Selecciona Manage -> Install VMware Tools.

3\. Monta el disco de VMware Tools y sigue las instrucciones para instalarlo en Kali.

### <mark style="color:purple;">Actualización y upgrade del sistema</mark>

Siempre es recomendable actualizar los paquetes de Kali Linux tras la instalación. Abre la terminal y ejecuta:

```bash
sudo apt update && sudo apt full-upgrade -y
```

En sistemas basados en Debian, como Kali Linux y Ubuntu, ambos comandos (`apt update` y `apt-get update`) sirven para actualizar la lista de paquetes y repositorios del sistema, pero existen algunas diferencias entre ellos:

#### Diferencias clave:

<table><thead><tr><th width="191">Comando</th><th>Descripción</th><th>Detalles</th></tr></thead><tbody><tr><td><code>apt update</code></td><td>Comando más moderno e interactivo, diseñado para usuarios finales</td><td><em>Combina</em> opciones comunes de <code>apt-get</code> y <code>apt-cache</code>, además de proporcionar salidas más legibles.</td></tr><tr><td><code>apt-get update</code></td><td>Comando más antiguo, orientado a scripts y automatización de tareas</td><td>Parte de la "vieja" herramienta <code>apt-get</code>, con opciones avanzadas pero sin mejoras de interacción</td></tr></tbody></table>

`apt upgrade` y `apt-get upgrade` también tienen diferencias sutiles, aunque su propósito es similar: **actualizar los paquetes instalados en el sistema**. Aquí te detallo sus características y diferencias:

#### Diferencias clave entre `apt upgrade` y `apt-get upgrade`

<table><thead><tr><th width="193">Comando</th><th>Descripción</th><th>Detalles</th></tr></thead><tbody><tr><td><code>apt upgrade</code></td><td>Herramienta moderna para actualizar paquetes. Ofrece una experiencia de usuario mejorada.</td><td>Más interactivo y orientado a usuario final, con salidas de terminal claras y coloridas.</td></tr><tr><td><code>apt-get upgrade</code></td><td>Herramienta antigua, más básica y detallada, sin optimización en la interacción.</td><td>Usado frecuentemente en scripts y automatizaciones; mantiene estabilidad en scripts antiguos.</td></tr></tbody></table>

## <mark style="color:purple;">Conclusión</mark>

Con esta guía, tendrás Kali Linux funcionando de manera eficiente en VMware. Esto te permitirá experimentar con herramientas de hacking ético y ciberseguridad en un entorno aislado, sin poner en riesgo tu sistema principal.

En la siguiente sección veremos cómo podemos personalizar nuestro sistema Kali Linux con un entorno custom.
