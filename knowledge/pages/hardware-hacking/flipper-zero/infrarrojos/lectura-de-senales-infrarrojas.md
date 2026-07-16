
# Lectura de señales infrarrojas

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-0TXdhNpDm1DVj5ynB9PXh-20241025-105459.png?format=webp" alt=""><figcaption></figcaption></figure>

Con Flipper Zero, puedes capturar y guardar señales [infrarrojas](https://en.wikipedia.org/wiki/Infrared) (IR) de controles remotos IR. Estos controles remotos se utilizan para controlar televisores, aires acondicionados, proyectores, sistemas de audio y más. Las señales guardadas se pueden reproducir para enviar comandos en lugar del control remoto original.﻿

## <mark style="color:orange;">Captura de señales infrarrojas</mark> <a href="#g3zt0" id="g3zt0"></a>

Flipper Zero captura y demodula señales IR con una frecuencia portadora de 38 kHz con su [receptor IR integrado](https://docs.flipperzero.one/infrared#FOaB8) . Para los controles remotos con protocolos conocidos, Flipper Zero decodifica automáticamente las señales IR. Si se desconoce el protocolo del control remoto, Flipper Zero grabará la señal en formato RAW. Para capturar y guardar una señal, haga lo siguiente:

1. Vaya al **Menú principal -> Infrarrojos -> Aprender nuevo control remoto** .
2. Coloque su control remoto IR en la línea de visión del receptor IR de su Flipper Zero.
3. En su control remoto IR, presione el botón que desea que su Flipper Zero grabe.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-LnLkB1XgiOWAampVLoqEE-20241025-105531.png?format=webp" alt=""><figcaption><p>Mantenga el control remoto en la línea de visión del receptor de infrarrojos.﻿</p></figcaption></figure>

4. Una vez capturada la señal, verás el nombre del protocolo remoto en la pantalla de tu Flipper Zero.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/P5i59VFhO3r7a5faLYyZS_image.png?format=webp" alt=""><figcaption><p>Los datos capturados se muestran en la pantalla.﻿</p></figcaption></figure>

5. Para guardar la señal capturada, presione **Guardar** , nombre el botón y presione **Guardar** nuevamente.
6. Después de guardar el primer botón, Flipper Zero crea un control remoto virtual con el nuevo botón. Puedes agregar un nuevo botón al control remoto seleccionando ➕.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/Z2gqQG_RkhpyfcvtNRXnh_image.png?format=webp" alt=""><figcaption><p>Añadir nuevas señales al control remoto virtual﻿</p></figcaption></figure>

7. Para personalizar o eliminar el control remoto virtual, seleccione **Editar** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/IpW7hzpRvknmD2ijvy0al_image.png?format=webp" alt=""><figcaption><p>Personaliza tus controles remotos virtuales﻿</p></figcaption></figure>

También puede personalizar los controles remotos guardados yendo a **Menú principal -> Infrarrojos -> Controles remotos guardados** .

Tenga en cuenta que Flipper Zero puede capturar la luz infrarroja del sol o de una bombilla doméstica mientras intenta capturar una señal de un control remoto.﻿﻿

## <mark style="color:orange;">Emulación de señales infrarrojas</mark> <a href="#b8ncd" id="b8ncd"></a>

[Con su transmisor de infrarrojos](https://docs.flipperzero.one/infrared#FOaB8) integrado, Flipper Zero puede enviar señales guardadas a televisores, aires acondicionados, proyectores, sistemas de sonido y más. Para enviar una señal, haga lo siguiente:

1. Vaya al **Menú principal -> Infrarrojos -> Controles remotos guardados** .
2. Seleccione el control remoto guardado de la lista de controles remotos.
3. Apunta el Flipper Zero hacia el dispositivo que quieres controlar. Asegúrate de que el transmisor de infrarrojos del Flipper Zero esté orientado hacia el dispositivo.
4. Para enviar el comando, seleccione el botón que desea emular y presione el botón **OK** .

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-aYbGhFk9yDTFsFuyRVB2A-20241025-105637.png?format=webp" alt=""><figcaption><p>Para enviar una señal, apunte su Flipper Zero al dispositivo y presione el botón OK</p></figcaption></figure>
