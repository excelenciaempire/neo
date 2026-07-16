
# Sub-GHz

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-h6KaDMvzQwWL27ZZH84ZR-20241024-175959.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero puede recibir y transmitir frecuencias de radio en el rango de 300 a 928 MHz con su módulo integrado, que puede leer, guardar y emular controles remotos. Estos controles se utilizan para interactuar con puertas, barreras, cerraduras por radio, interruptores de control remoto, timbres inalámbricos, luces inteligentes y más.

Inserte una tarjeta microSD para usar la aplicación Sub-GHzAntes de usar la aplicación Sub-GHz, asegúrese de actualizar el firmware de su Flipper Zero con una tarjeta microSD insertada, ya que Flipper Zero almacena bases de datos en una tarjeta microSD. Para obtener más información sobre el proceso de actualización, visite la página [de actualización de firmware .](https://docs.flipperzero.one/basics/firmware-update)﻿

## <mark style="color:orange;">Menú Sub-GHz</mark> <a href="#og_4x" id="og_4x"></a>

Puede acceder a la aplicación Sub-GHz desde el menú principal. En la aplicación, puede leer y emular controles remotos, agregar controles manualmente y determinar la frecuencia del control remoto.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/_yl6oxmqzaB7G7BFLSkgu_monosnap-miro-2023-07-14-13-17-38.jpg?format=webp" alt=""><figcaption></figcaption></figure>

* ﻿[Lectura:](https://docs.flipperzero.one/sub-ghz/read) lee y decodifica señales según protocolos conocidos. Si el protocolo es estático, Flipper Zero guarda la señal.
* ﻿[Leer RAW:](https://docs.flipperzero.one/sub-ghz/read-raw) lee y guarda señales en formato RAW, incluidas señales de controles remotos con protocolos desconocidos.
* **Guardado:** enumera las señales guardadas, que se pueden emular y renombrar.
* ﻿[Agregar manualmente:](https://docs.flipperzero.one/sub-ghz/add-new-remote) crea un control remoto virtual que se puede emparejar con un lector.
* ﻿[Analizador de frecuencia:](https://docs.flipperzero.one/sub-ghz/read#bwvDc) determina las frecuencias en las que se envía la señal desde el control remoto.
* **Información de la región:** proporciona información sobre su región y enumera las frecuencias permitidas para la transmisión. Para obtener más información sobre las regiones, visite [Frecuencias](https://docs.flipperzero.one/sub-ghz/frequencies) .
* **Configuración de radio:** permite cambiar entre la antena interna y la antena externa si está conectada.

## <mark style="color:orange;">Hardware de sub-GHz</mark> <a href="#kfpn7" id="kfpn7"></a>

Flipper Zero tiene un módulo integrado de frecuencias inferiores a 1 GHz basado en un [transceptor CC1101](https://www.ti.com/lit/ds/symlink/cc1101.pdf) y una antena de radio (el alcance máximo es de 50 metros). Tanto el chip CC1101 como la antena están diseñados para funcionar en las bandas de frecuencias de 300-348 MHz, 387-464 MHz y 779-928 MHz.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/iWJNVsM0quT9-4IdFRVEq_monosnap-miro-2023-07-14-13-19-38.jpg?format=webp" alt=""><figcaption></figcaption></figure>

La aplicación Sub-GHz admite módulos de radio externos basados ​​en el transceptor CC1101. Para obtener más información, visite [esta página](https://github.com/flipperdevices/flipperzero-firmware/pull/2747) .

## <mark style="color:orange;">Link útiles</mark>

{% content-ref url="/pages/tnosRDzXuKsvNSSLuIft" %}
[Lectura de señales](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/sub-ghz/lectura-de-senales.md)
{% endcontent-ref %}

{% content-ref url="/pages/pSNRdvh6v6sUyZJ8RtJg" %}
[Lectura de señales RAW](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/sub-ghz/lectura-de-senales-raw.md)
{% endcontent-ref %}

{% content-ref url="/pages/P5QXg6usm1zr4GslOAKS" %}
[Añadir nuevos controles remotos](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/sub-ghz/anadir-nuevos-controles-remotos.md)
{% endcontent-ref %}

{% content-ref url="/pages/rWoPUxmSSOoqsZULRVf0" %}
[Frecuencias](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/sub-ghz/frecuencias.md)
{% endcontent-ref %}
