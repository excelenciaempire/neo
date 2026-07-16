
# iButton

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-p0FVsy724Lu_Y_rim48S7-20241025-124007.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero es compatible con el protocolo de comunicación de dispositivos 1-Wire, que se implementa en pequeñas llaves electrónicas conocidas como llaves iButton. Estas llaves se utilizan para control de acceso, medición de temperatura, medición de humedad, almacenamiento de claves criptográficas, etc.

Flipper Zero puede leer, escribir y emular claves de control de acceso iButton con su módulo iButton integrado, que admite los protocolos de claves Dallas, Cyfral y Metakom.

Inserte una tarjeta microSD para usar la aplicación iButtonAntes de usar la aplicación iButton, asegúrese de actualizar el firmware de Flipper Zero con una tarjeta microSD insertada, ya que Flipper Zero almacena bases de datos en una tarjeta microSD. Para obtener más información sobre el proceso de actualización, visite la página [de actualización de firmware .](https://docs.flipperzero.one/basics/firmware-update)﻿

## <mark style="color:orange;">Menú iButton</mark> <a href="#kthdg" id="kthdg"></a>

Puede acceder a la aplicación iButton desde el menú principal. En la aplicación, puede leer, guardar, editar, escribir y emular teclas iButton.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/mcomeNOquOxGPZ1b68p0k_monosnap-miro-2023-10-16-12-20-54.jpg?format=webp" alt=""><figcaption><p>Menú de la aplicación iButton﻿</p></figcaption></figure>

* ﻿[Leer](https://docs.flipper.net/ibutton/read) **:** detecta, lee y guarda claves iButton.
* **Guardados :** emula, edita y escribe claves guardadas.
* ﻿[Agregar manualmente](https://docs.flipper.net/ibutton/add-manually) **:** genera claves con números únicos que se pueden emular.

## <mark style="color:orange;">Hardware del iButton</mark> <a href="#id-6zjo" id="id-6zjo"></a>

No todos los dispositivos iButton pueden ser detectados por Flipper ZeroVarios dispositivos iButton pueden tener el mismo factor de forma, sin embargo, Flipper Zero solo puede detectar las claves de control de acceso.﻿

Flipper Zero tiene un módulo iButton incorporado que consta de un pad iButton y tres [pines pogo con resorte](https://en.wikipedia.org/wiki/Pogo_pin) que se encuentran en la PCB iButton.

<figure><img src="https://cdn.flipperzero.one/Monosnap_Miro_2022-09-28_19-27-31.png" alt=""><figcaption><p>Pines del módulo iButton﻿</p></figcaption></figure>

Dos pines están asignados a la transferencia de datos y tienen salida al pin GPIO 17. El pin central restante es tierra.

<figure><img src="https://cdn.flipperzero.one/Monosnap_Miro_2022-09-28_19-29-05.png" alt=""><figcaption><p>Los pines de datos del iButton tienen salida al pin GPIO 17﻿</p></figcaption></figure>

La parte plana del pad permite conectar una llave iButton (esclava) con Flipper Zero (maestra). El pin de datos izquierdo y el pin de tierra del medio se utilizan para leer y escribir llaves iButton.

<figure><img src="https://cdn.flipperzero.one/Monosnap_Miro_2022-09-29_18-31-34.png" alt=""><figcaption><p>Pines utilizados para leer y escribir﻿</p></figcaption></figure>

La parte saliente del pad permite conectar Flipper Zero (esclavo) con un lector iButton (maestro). El pin de datos derecho y el pin de tierra intermedio se utilizan para emular las teclas iButton.

<figure><img src="https://cdn.flipperzero.one/Monosnap_Miro_2022-09-29_18-27-39.png" alt=""><figcaption><p>Pines utilizados para emulación</p></figcaption></figure>
