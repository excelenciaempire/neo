
# Evil Portal

<figure><img src="/files/xXilXdwvoEmhyShSH0Nc" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Evil Portal</mark> <a href="#mifss" id="mifss"></a>

Un `Evil Portal` es una técnica utilizada en hacking ético para interceptar y recopilar credenciales de usuarios conectados a redes WiFi. Funciona creando una página web maliciosa que imita el portal cautivo de una red pública o privada, engañando a los usuarios para que ingresen información sensible, como nombres de usuario y contraseñas. Los atacantes suelen implementar un evil portal junto con otras herramientas de ataque, como deauth, para forzar a los usuarios a reconectarse a través del portal falso, facilitando así la captura de datos confidenciales.

Para realizar esta técnica usaremos el siguiente repositorio, que contiene las plantillas necesarias para llevar a cabo el ataque dentro del directorio `/portals`:

{% embed url="<https://github.com/bigbrodude6119/flipper-zero-evil-portal>" %}

Necesitamos tener instalado el [Firmware de Momentum](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/custom-firmwares.md) para que funcione correctamente. Una vez instalado tendremos la opción de `Evil Portal` habilitada en:

```
Apps > GPIO > ESP > [ESP32] Evil Portal
```

<figure><img src="/files/ogyT7lJ976xvor827JdE" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Importar plantillas</mark>

Necesitamos descargarnos el repositorio en nuestro equipo, y importar las plantillas html del directorio `/portals` en la siguiente ruta:

```
SD Card > apps_data > evil_portal > html
```

## <mark style="color:orange;">Configurar nombre de AP</mark>

Podemos configurar el nombre del AP en la opción `Set AP name`:

{% hint style="success" %}
Para introducir espacios debemos mantener pulsado el botón central sobre la barra baja `_` y para escribir mayúsculas mantener el botón central sobre una letra.
{% endhint %}

<div><figure><img src="/files/f3kbtp4jpIIkL5CQpOpg" alt=""><figcaption></figcaption></figure> <figure><img src="/files/9rJ8bqmkt0PsqZlZzD8v" alt=""><figcaption></figcaption></figure></div>

También podemos descargarnos el archivo ap.config.txt y sustituir el index.html que viene por defecto para que se cargue automáticamente siempre que iniciemos el Evil Portal:

<figure><img src="/files/SEZFMTtKk8RksiB6ma8i" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Seleccionar plantilla</mark>

En la opción `Select HTML` aparecerán todas las plantillas HTML que hemos cargado. Solamente tendríamos que seleccionar la que nosotros queramos, por ejemplo la de Google:

## <mark style="color:orange;">Iniciar Evil Portal</mark>

Una vez configurado todo solamente seleccionamos la opción Start Portal y eso nos genera el AP malicioso. Cuando un usuario introduzca sus credenciales las recibiremos en el Flipper al instante. Además se guardará un archivo de log
