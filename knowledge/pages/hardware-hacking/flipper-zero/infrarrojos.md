
# Infrarrojos

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-AWL5WHe8vxeeHCE7HnCzc-20241025-105353.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero puede interactuar con dispositivos que utilizan luz infrarroja (IR) para enviar comandos, como televisores, aires acondicionados, sistemas multimedia, etc. Con su módulo infrarrojo incorporado, Flipper Zero puede aprender y guardar controles remotos infrarrojos y usar sus propios controles remotos universales para controlar otros dispositivos.

Inserte una tarjeta microSD para usar la aplicación InfrarrojosAntes de usar la aplicación Infrared, asegúrese de actualizar el firmware de su Flipper Zero con una tarjeta microSD insertada, ya que Flipper Zero almacena bases de datos en una tarjeta microSD. Para obtener más información sobre el proceso de actualización, visite la página [de actualización de firmware .](https://docs.flipperzero.one/basics/firmware-update)﻿

## <mark style="color:orange;">Menú infrarrojos</mark> <a href="#ldjwg" id="ldjwg"></a>

Puede acceder a la aplicación Infrarrojos desde el Menú principal. En la aplicación, puede utilizar controles remotos universales para controlar otros dispositivos, aprender nuevos controles remotos y administrar controles remotos guardados.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/RZ8AsqCjrx2rPP_hNSbE2_flipper-zero-infrared-menu.jpg?format=webp" alt=""><figcaption><p>Menú de la aplicación de infrarrojos﻿</p></figcaption></figure>

* ﻿[Controles remotos universales:](https://docs.flipper.net/infrared/universal-remotes) itera sobre un diccionario de protocolos conocidos y envía el mismo comando para todos los modelos compatibles. El diccionario se almacena en la tarjeta microSD. Esto también se conoce como ataque de fuerza bruta. Debido a que Flipper Zero itera sobre un diccionario completo, el proceso de envío de señales demora unos segundos.
* ﻿[Aprender un nuevo control remoto:](https://docs.flipperzero.one/infrared/read) lee y guarda las señales de los controles remotos infrarrojos. Cada botón de un control remoto se guarda por separado.
* **Controles remotos guardados:** enumera los controles remotos guardados, que se pueden editar y reproducir.
* **Configuración GPIO:** establece la salida de señal y el suministro de energía a un transmisor IR externo.

## <mark style="color:orange;">Hardware infrarrojos</mark> <a href="#foab8" id="foab8"></a>

Flipper Zero tiene un módulo de infrarrojos incorporado que consta de una ventana de plástico transparente con luz infrarroja, tres LED de transmisión de infrarrojos y un receptor de infrarrojos.

<figure><img src="/files/SYyZRb7OVmH9Po770kiQ" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/1fCgiOMCB2Z3N6vRWwkI" alt=""><figcaption></figcaption></figure>
