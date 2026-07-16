
# Lectura de señales RAW

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-hAyBw0Rs8k34MVbpBtayE-20241024-180137.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero puede grabar señales de controles remotos de radio en formato RAW sin decodificar, de manera similar a cómo graba sonido un dictáfono. Las señales se demodulan de acuerdo con los ajustes de modulación. Puede utilizar la función **Read RAW** para grabar señales con protocolos conocidos y desconocidos para su posterior reproducción y análisis.[﻿](https://forum.flipperzero.one/t/my-remote-isnt-supported-how-to-add-new-sub-ghz-protocol-in-flipper-zero/2033)

{% hint style="danger" %}
**¡No utilices la función Read RAW con las llaves de tu coche!**

Los sistemas de cierre centralizado de los coches modernos utilizan códigos rotativos, lo que significa que cada vez que utilizas el llavero, este genera un código único. Este código se basa en una secuencia conocida por el sistema de cierre centralizado y se utiliza para desbloquear el coche. Si capturas la señal del llavero y la reproduces en el coche, corres el riesgo de desincronizar la llave original, lo que la dejaría inutilizable .﻿
{% endhint %}

#### **Si desactivó su llave después de usar la función Leer RAW**

* En el llavero original, intente presionar el mismo botón “Desbloquear” varias veces.
* Consulta los manuales del concesionario de tu vehículo para saber cómo añadir o quitar llaves nuevas. Puedes seguir estos procedimientos para añadir llaves nuevas sin ponerte en contacto con el concesionario.
* Comuníquese con el concesionario e infórmele que su llavero dejó de funcionar. Deberían poder ayudarlo a reparar el llavero del automóvil.

## <mark style="color:orange;">Procedimiento de lectura de señales RAW</mark> <a href="#vwun8" id="vwun8"></a>

En el modo de lectura RAW, Flipper Zero graba señales demoduladas de controles remotos en formato RAW.

Para leer y guardar la señal del control remoto en formato RAW, haga lo siguiente:

1. Vaya al **Menú principal -> Sub-GHz** .
2. Seleccione **Read RAW** y luego presione **REC** para iniciar el proceso de grabación.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/adErxek6n5j0LD6verni4_monosnap-miro-2023-07-14-13-33-11.jpg?format=webp" alt=""><figcaption></figcaption></figure>

3. Presione el botón del control remoto que desea grabar en formato RAW.
4. Después de grabar una muestra RAW, presione **Detener** y luego presione **Guardar**.
5. Nombra la señal grabada y luego presiona **Guardar**.

﻿Los controles remotos tienen diferentes frecuencias y modulaciones. En el rango de frecuencias inferiores a 1 GHz, los datos se transmiten a distintas frecuencias y modulaciones. Para demodular una señal correctamente, es necesario configurar los parámetros de frecuencia y modulación en el menú de configuración. Por lo general, estos parámetros se muestran en los controles remotos o en la documentación.﻿﻿

## <mark style="color:orange;">Menú de configuración RAW</mark> <a href="#id-0k9i1" id="id-0k9i1"></a>

En este menú puede cambiar manualmente las frecuencias y modulaciones y establecer la intensidad mínima de la señal registrada. Para abrir el menú de configuración, en la pantalla de escaneo, presione **Config** . Verá lo siguiente:

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/Q2ZbCdl3NUdpA5MdsjanN_monosnap-miro-2023-07-12-19-44-55.jpg?format=webp" alt=""><figcaption></figcaption></figure>

### <mark style="color:orange;">Configuración de frecuencia</mark> <a href="#uvuju" id="uvuju"></a>

Puedes cambiar las frecuencias en las que Flipper Zero recibe señales. En el menú de configuración, pulsando **IZQUIERDA** o **DERECHA** puedes configurar manualmente las frecuencias de la lista:

<figure><img src="https://cdn.flipperzero.one/Monosnap_Miro_2022-08-23_14-24-29.png" alt=""><figcaption></figcaption></figure>

Para leer la señal correctamente, es necesario determinar la frecuencia del mando a distancia. Para ello, puede utilizar la función [Analizador de frecuencia .](https://docs.flipperzero.one/sub-ghz/read#bwvDc)

### <mark style="color:orange;">Configuración de modulación</mark> <a href="#hue8f" id="hue8f"></a>

Para capturar la señal del control remoto, debe configurar los ajustes de modulación correctos en Flipper Zero. Debido a que Flipper Zero no es una radio definida por software, debe configurar la modulación correcta antes de escanear la señal. De lo contrario, Flipper Zero no demodulará ni registrará los datos correctamente.

Flipper Zero admite modulaciones de señal [de amplitud (AM)](https://en.wikipedia.org/wiki/Amplitude_modulation) y [frecuencia (FM)](https://en.wikipedia.org/wiki/Frequency_modulation) . En el **menú de configuración** , al presionar **IZQUIERDA** o **DERECHA,** puede configurar manualmente las modulaciones de señal de la lista:

* **AM270:** modulación de amplitud con un ancho de banda de 270 kHz.
* **AM650:** modulación de amplitud con un ancho de banda de 650 kHz (establecido como predeterminado).
* **FM238:** modulación de frecuencia con un ancho de banda de 270 kHz y una [desviación](https://www.youtube.com/watch?v=gFu7-7lUGDg\&t=142s) de 2,380371 kHz.
* **FM476:** modulación de frecuencia con un ancho de banda de 270 kHz y una desviación de 47,60742 kHz.

### <mark style="color:orange;">Configuración del umbral RSSI</mark> <a href="#ydgeq" id="ydgeq"></a>

Puede grabar señales de alta intensidad en formato RAW y evitar grabar señales de baja intensidad configurando la sensibilidad de la intensidad de la señal en unidades de [dBm](https://en.wikipedia.org/wiki/DBm) . Una vez que la intensidad de la señal caiga por debajo del valor RSSI mínimo seleccionado, Flipper Zero continuará grabando durante un segundo más y luego pausará la grabación. El proceso de grabación se reanudará una vez que la intensidad de la señal supere el valor RSSI mínimo seleccionado.﻿

## <mark style="color:orange;">Envío de señales RAW (Emulación)</mark> <a href="#o27we" id="o27we"></a>

Flipper Zero puede enviar señales RAW a frecuencias permitidas para la transmisión en su región. Para enviar una señal RAW guardada con su Flipper Zero, haga lo siguiente:

1. Vaya al **Menú principal -> Sub-GHz -> Saved**.
2. Seleccione la señal.
3. Presione **Enviar** para enviar la señal RAW guardada una vez.

Algunas frecuencias pueden estar bloqueadas para transmisión en su regiónFlipper Zero puede recibir señales en todas las frecuencias de las bandas operativas. Sin embargo, Flipper Zero puede transmitir señales solo en las frecuencias permitidas para la transmisión en su región.﻿

Para obtener más información sobre las regiones y las frecuencias de transmisión permitidas, visita la página [Frecuencias](https://docs.flipperzero.one/sub-ghz/frequencies) .
