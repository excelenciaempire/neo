
# Lectura de señales

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-c0M5DM4ySGJfJGLDo4yLo-20241024-180047.png?format=webp" alt=""><figcaption></figcaption></figure>

Con el Flipper Zero, podrás leer, guardar y emular diferentes tipos de controles remotos con protocolos conocidos.

Existen controles remotos que funcionan con protocolos que Flipper Zero aún no conoce. Las señales de estos controles remotos se pueden grabar en formato RAW, guardar y reproducir con la función [Read RAW](https://docs.flipperzero.one/sub-ghz/read-raw) .[﻿](https://forum.flipperzero.one/t/my-remote-isnt-supported-how-to-add-new-sub-ghz-protocol-in-flipper-zero/2033)

## <mark style="color:orange;">Procedimiento de lectura</mark> <a href="#pl8-x" id="pl8-x"></a>

En el modo de lectura, Flipper Zero lee y decodifica señales demoduladas de controles remotos según protocolos conocidos. Si el protocolo del control remoto es estático, Flipper Zero puede guardar y enviar la señal.

{% hint style="danger" %}
**¡No utilices la función Read con las llaves de tu coche!**

Los sistemas de cierre centralizado de los coches modernos utilizan códigos rotativos, lo que significa que cada vez que utilizas el llavero, este genera un código único. Este código se basa en una secuencia conocida por el sistema de cierre centralizado y se utiliza para desbloquear el coche. Si capturas la señal del llavero y la reproduces en el coche, corres el riesgo de desincronizar la llave original, lo que la dejaría inutilizable .﻿
{% endhint %}

Para leer y guardar la señal de su control remoto, haga lo siguiente:

1. Vaya al **Menú principal -> Sub-GHz** .
2. Presione **Leer** y luego presione el botón del control remoto que desea leer.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/3LARdEupzZR64-chUzbPH_monosnap-miro-2023-07-14-12-19-41.jpg?format=webp" alt=""><figcaption></figcaption></figure>

3. Cuando se capture la señal, presione **OK** y luego presione **Guardar** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/oSgQs07b-5ukhIV49qyaX_monosnap-miro-2023-07-12-19-43-57.jpg?format=webp" alt=""><figcaption></figcaption></figure>

4. Nombra la señal capturada y luego presiona **Guardar** .

﻿Los controles remotos tienen diferentes frecuencias y modulaciones.Para leer las señales correctamente, es necesario conocer los parámetros del control remoto y configurar el Flipper Zero en consecuencia. Si el Flipper Zero no puede leer la señal con la configuración predeterminada, deberá interactuar con los parámetros de frecuencia y modulación en el menú de configuración.﻿﻿

## <mark style="color:orange;">Menú de configuración</mark> <a href="#yjx97" id="yjx97"></a>

En este menú, puede cambiar frecuencias manualmente y en modo de salto, cambiar modulaciones manualmente y bloquear el teclado mientras busca señales. Para abrir el menú de configuración, en la pantalla de escaneo, presione **Config** . Verá lo siguiente:

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/ayaJKt_oZ7ZE8eP619laK_monosnap-miro-2023-07-14-16-27-45.jpg?format=webp" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Configuración de frecuencia</mark> <a href="#id-1zaxs" id="id-1zaxs"></a>

Puede cambiar las frecuencias en las que Flipper Zero recibe señales. En el **menú de configuración** , al presionar **IZQUIERDA** o **DERECHA,** puede configurar manualmente las frecuencias de la lista:

<figure><img src="https://cdn.flipperzero.one/Monosnap_Miro_2022-08-23_14-24-29.png" alt=""><figcaption></figcaption></figure>

Para leer la señal correctamente, es necesario determinar la frecuencia del mando a distancia. Para ello, puede utilizar la función Analizador de frecuencia.

## <mark style="color:orange;">Analizador de frecuencia</mark> <a href="#bwvdc" id="bwvdc"></a>

Durante el análisis, Flipper Zero escanea la intensidad de la señal en todas las frecuencias disponibles en el menú de configuración. Flipper Zero muestra la frecuencia con el valor más alto del indicador de intensidad de la señal recibida (RSSI), con una intensidad de señal superior a -90 [dBm](https://en.wikipedia.org/wiki/DBm) .

Para determinar la frecuencia del control remoto , haga lo siguiente:

1. Coloca el control remoto muy cerca del lado izquierdo de su Flipper Zero.

{% hint style="info" %}
﻿Es importante colocar el control remoto muy cerca de su Flipper Zero para evitar analizar señales de otros dispositivos.﻿
{% endhint %}

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/nR_6aWyXoMwgfH-_fo2Ff_image.png?format=webp" alt=""><figcaption></figcaption></figure>

2. Vaya al **Menú principal -> Sub-GHz -> Analizador de frecuencia**
3. En su control remoto, presione y mantenga presionado el botón que desea analizar.
4. Revise el valor de frecuencia medido en la pantalla.

Al presionar el botón **IZQUIERDO** o **DERECHO** , puede pasar a la segunda pantalla que muestra hasta 15 frecuencias medidas. En la segunda pantalla, puede ordenar las frecuencias medidas presionando el botón **OK** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/Gmsu49H4Ga7x6aWwbLWBO_image.png?format=webp" alt=""><figcaption></figcaption></figure>

Los resultados del análisis pueden ser aproximados. Flipper Zero muestra valores que pueden ayudarle a determinar la banda de frecuencia en la que se envía la señal. En la mayoría de los casos, las señales se envían en frecuencias de las bandas de 315, 433 y 868 MHz.﻿﻿

## <mark style="color:orange;">Saltando entre frecuencias (Hop)</mark> <a href="#otoen" id="otoen"></a>

Para recibir una señal en una frecuencia desconocida, utilice el modo de salto. En este modo, Flipper Zero cambia rápidamente entre las frecuencias disponibles y mide la intensidad de la señal. Una vez que la intensidad de la señal supera los -90 dBm, el cambio se detiene y Flipper Zero recibe la señal en esa frecuencia durante un segundo; luego, se reanuda el cambio entre frecuencias.

Para buscar señales en modo Salto, en el **Menú de configuración** , configura **Hop** en **ON** .

<figure><img src="/files/nujynwXuzju2oDjvf3vd" alt=""><figcaption></figcaption></figure>

﻿El cambio entre frecuencias lleva algún tiempo, por lo que las señales transmitidas en el momento del cambio pueden perderse. Para una mejor recepción de la señal, configure una frecuencia fija determinada por el analizador de frecuencia.﻿

En el modo de salto, también puedes cambiar las modulaciones manualmente.

## <mark style="color:orange;">Configuración de modulación</mark> <a href="#znwgy" id="znwgy"></a>

Para capturar la señal del control remoto, debe configurar los ajustes de modulación correctos en su Flipper Zero. Debido a que Flipper Zero no es una radio definida por software, debe configurar la modulación correcta antes de escanear la señal; de lo contrario, no recibirá los datos correctos.

Flipper Zero admite modulaciones de señal [de amplitud (AM)](https://en.wikipedia.org/wiki/Amplitude_modulation) y [frecuencia (FM)](https://en.wikipedia.org/wiki/Frequency_modulation) . En el **menú de configuración** , al presionar **IZQUIERDA** o **DERECHA** , puede configurar manualmente las modulaciones de señal de la lista:

* **AM270:** modulación de amplitud con un ancho de banda de 270 kHz.
* **AM650:** modulación de amplitud con un ancho de banda de 650 kHz (establecido como predeterminado).
* **FM238:** modulación de frecuencia con un ancho de banda de 270 kHz y una [desviación](https://www.youtube.com/watch?v=gFu7-7lUGDg\&t=142s) de 2,380371 kHz.
* **FM476:** modulación de frecuencia con un ancho de banda de 270 kHz y una desviación de 47,60742 kHz.

## <mark style="color:orange;">Bin\_RAW</mark> <a href="#xedsv" id="xedsv"></a>

Esta opción permite procesar señales RAW que no fueron decodificadas durante el proceso de lectura. El procesamiento implica eliminar el ruido de fondo, eliminar los segmentos de señal repetidos y corregir los errores de sincronización.

Para utilizar esta función, debe habilitar la opción Bin\_RAW manualmente. Además, es importante verificar que los parámetros de frecuencia y modulación coincidan con los de su control remoto para lograr una funcionalidad óptima.

## <mark style="color:orange;">Bloquear teclado</mark> <a href="#vycdi" id="vycdi"></a>

Esta función le permite bloquear el teclado mientras su Flipper Zero está escaneando en busca de señales. Para bloquear el teclado, en el **Menú de configuración** , seleccione **Bloquear teclado** y presione **OK** .

## <mark style="color:orange;">Envío de señales (Emulación)</mark> <a href="#y7ifn" id="y7ifn"></a>

Flipper Zero puede enviar señales guardadas que se graban en frecuencias permitidas para la transmisión en su región.

Para enviar una señal guardada con Flipper Zero, haga lo siguiente:

1. Vaya al **Menú principal -> Sub-GHz -> Saved**
2. Seleccione la señal y luego presione **Emulate**
3. Presione **Enviar** para enviar la señal guardada

Algunas frecuencias pueden estar bloqueadas para transmisión en su región. Flipper Zero puede recibir señales en todas las frecuencias de las bandas operativas. Sin embargo, Flipper Zero puede transmitir señales solo en las frecuencias permitidas para la transmisión en su región.﻿

Para obtener más información sobre las regiones y las frecuencias de transmisión permitidas, visita la página [Frecuencias](https://docs.flipperzero.one/sub-ghz/frequencies) .

## <mark style="color:orange;">Escuchando walkie-talkies</mark> <a href="#id-9w8q" id="id-9w8q"></a>

Es posible escuchar walkie-talkies analógicos con el altavoz del Flipper Zero. Aunque no estaba previsto originalmente, las funciones de lectura de sub-GHz y lectura de datos RAW permiten esta funcionalidad.

{% hint style="info" %}
Es posible que esta función no funcione bien
{% endhint %}

Flipper Zero está diseñado para recibir señales digitales. Cuando recibe una señal de radio analógica modulada en FM, el dispositivo la procesa como datos digitales e interpreta las frecuencias superiores a un determinado umbral como 1 y las inferiores como 0. Además, el altavoz de Flipper Zero no está diseñado para la reproducción de voz humana. Para utilizar esta función de forma eficaz, hable lo suficientemente alto en el walkie-talkie.﻿

Para empezar a escuchar un walkie-talkie:

1. Vaya al **Menú principal -> Sub-GHz**&#x20;
2. Selecciona:

* **Read** : sólo para escuchar.
* **Read RAW** : para escuchar y grabar.

3. Vaya a **Configuración**&#x20;
4. Establezca **la frecuencia** en la frecuencia del walkie-talkie que desea escuchar.
5. Establezca **la modulación** en **FM238**
6. Establezca **el sonido** en **ON**
7. (Opcional) Si ha seleccionado **Read RAW** , también puede configurar **el Umbral RSSI** para registrar únicamente las señales que superen el nivel de intensidad de señal establecido. [Obtenga más información sobre la configuración del Umbral RSSI.](https://docs.flipper.net/sub-ghz/read-raw#yDGEq)﻿
8. Presione **ATRÁS**&#x20;
9. Si ha seleccionado **Read RAW** , presione **OK** para comenzar a escuchar.

Todo listo. Ahora, si la persona del otro lado habla lo suficientemente alto, podrás escuchar su voz a través del timbre de tu Flipper Zero.
