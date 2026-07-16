
# Bad USB

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-PUVMYpliqUJ_2-MPHnZtf-20241025-125639.png?format=webp" alt=""><figcaption></figcaption></figure>

{% hint style="danger" %}
Algunas de las técnicas recogidas en esta sección pueden ser **ilegales** si se realizan sin autorización. No me hago responsable del mal uso de las técnicas recogidas en este manual.
{% endhint %}

Flipper Zero puede actuar como un [dispositivo BadUSB](https://web.archive.org/web/20220816200129/https://github.com/hak5darren/USB-Rubber-Ducky/wiki/) , reconocido por las computadoras como un [dispositivo de interfaz humana](https://en.wikipedia.org/wiki/Human_interface_device) (HID), como un teclado. Un dispositivo BadUSB puede cambiar la configuración del sistema, abrir puertas traseras, recuperar datos, iniciar reverse shells o básicamente hacer cualquier cosa que se pueda lograr con acceso físico. Se hace ejecutando un conjunto de comandos escritos en el lenguaje de script Rubber Ducky, también conocido como DuckyScript. Este conjunto de comandos también se denomina payload.

{% content-ref url="/pages/UK53Zz6eExMme2kaODFh" %}
[Shells y Payloads](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads.md)
{% endcontent-ref %}

Inserte una tarjeta microSD para usar la aplicación Bad USB. Antes de usar la aplicación Bad USB, asegúrese de actualizar el firmware de Flipper Zero con una tarjeta microSD insertada, ya que Flipper Zero almacena bases de datos en una tarjeta microSD. Para obtener más información sobre el proceso de actualización, visite la página [de actualización de firmware .](https://docs.flipperzero.one/basics/firmware-update)﻿﻿

## <mark style="color:orange;">Lenguaje de programación Flipper Zero</mark> <a href="#x8ppp" id="x8ppp"></a>

Antes de utilizar Flipper Zero como dispositivo BadUSB, debe escribir un payload en formato .txt en cualquier editor de texto ASCII común que utilice el lenguaje de programación. Flipper Zero puede ejecutar la sintaxis de programación Rubber Ducky extendida. La sintaxis es compatible con el lenguaje [de programación Rubber Ducky 1.0](https://web.archive.org/web/20220816200129/http://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript) clásico , pero proporciona comandos y funciones adicionales, como el método de entrada ALT+Numpad, el comando SysRq y más.

Para obtener más información sobre el lenguaje de script Flipper Zero, consulte [esta página.](https://developer.flipper.net/flipperzero/doxygen/badusb_file_format.html)

Un recurso útil es la web de﻿﻿ Payload Studio de Hak5, donde podemos desarrollar nuestros scripts en formato Duckyscript y descargarlos en local:

{% embed url="<https://payloadstudio.hak5.org/community/>" %}

## <mark style="color:orange;">Cargando nuevos payloads a Flipper Zero</mark> <a href="#iomsq" id="iomsq"></a>

Una vez creado el payload, puedes cargarlo en tu Flipper Zero a través de [qFlipper](https://docs.flipperzero.one/qflipper) o [la aplicación Flipper Mobile](https://docs.flipperzero.one/mobile-app) en la carpeta `SD Card/badusb/` . Los nuevos payloads que añadas estarán disponibles en la aplicación Bad USB.

﻿Al cargar, los archivos con el mismo nombre se sobrescribirán sin previo aviso.﻿﻿

<figure><img src="/files/Ubl2Wkzvy2pQWPQMYBUI" alt=""><figcaption></figcaption></figure>

### Repositorios interesantes de scripts

{% embed url="<https://github.com/stars/afsh4ck/lists/flipper-zero>" %}

## <mark style="color:orange;">Cómo usar Flipper Zero como dispositivo BadUSB</mark> <a href="#uk2m2" id="uk2m2"></a>

### <mark style="color:orange;">Mediante conexión USB</mark> <a href="#oejsx" id="oejsx"></a>

Para convertir su Flipper Zero en un dispositivo BadUSB mediante USB, haga lo siguiente:

1. Si qFlipper se está ejecutando en su computadora, ciérrelo.﻿
2. En su Flipper Zero, vaya a **Menú principal -> Bad USB**
3. Seleccione el payload y presione el botón **OK**
4. Vaya a **Configuración**
5. *(Opcional* ) Si es necesario, puede modificar la distribución del teclado (el inglés de EE. UU. es el predeterminado).﻿
6. Seleccionar tipo de conexión: **USB**
7. Conecte su Flipper Zero a la computadora mediante un cable USB.
8. Presione **Ejecutar** para ejecutar la carga útil en la computadora.

<figure><img src="/files/5Gr8nJykFlFNWhLZfX8J" alt=""><figcaption></figcaption></figure>

### ﻿<mark style="color:orange;">A través de la conexión BLE</mark>﻿ <a href="#wcjxy" id="wcjxy"></a>

Para convertir su Flipper Zero en un dispositivo BadUSB usando BLE , haga lo siguiente:

1. Active Bluetooth en su Flipper Zero yendo a **Menú principal -> Configuración -> Bluetooth**
2. Si qFlipper se está ejecutando en su computadora, ciérrelo
3. En su Flipper Zero, vaya a **Menú principal -> Bad USB**
4. Seleccione el payload
5. Vaya a **Configuración**
6. *(Opcional)* Si es necesario, puede modificar la distribución del teclado (el inglés de EE. UU. es el predeterminado).
7. Seleccionar el tipo de conexión: **BLE**
8. Presiona **ATRÁS**
9. En su computadora, vaya a la configuración de Bluetooth y conéctese al dispositivo BadUSB inalámbrico detectado
10. Confirme la conexión tanto en su computadora como en Flipper Zero (seleccionando **Aceptar**)
11. En su Flipper Zero , presione Ejecutar **para** ejecutar el payload en la computadora.
