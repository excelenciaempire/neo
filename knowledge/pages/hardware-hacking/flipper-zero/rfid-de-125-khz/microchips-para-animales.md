
# Microchips para animales

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-cNuTTC7kZqBSygHBzPVHa-20241024-181739.png?format=webp" alt=""><figcaption></figcaption></figure>

Un [microchip es un ](https://en.wikipedia.org/wiki/Microchip_implant_\(animal\))[transpondedor de](https://en.wikipedia.org/wiki/Transponder) identificación por radiofrecuencia (RFID) que almacena un número de identificación único y tiene aproximadamente el tamaño de un grano de arroz. El microchip se implanta debajo de la piel del animal . Cuando se escanea con un lector, el microchip transmite su número de identificación. Este número de identificación puede ayudarle a encontrar información sobre el animal y su dueño si se agrega a una base de datos.

Flipper Zero permite leer microchips de animales gracias a su antena RFID de baja frecuencia. La antena de Flipper Zero fue diseñada para funcionar a 125 kHz, mientras que la mayoría de microchips para animales funcionan a 134,2 kHz. La compatibilidad con la lectura de microchips de 134,2 kHz se implementó como una característica adicional. Para leer los datos del microchip, sostenga su Flipper Zero durante tres segundos sobre el microchip del animal que desea identificar. De lo contrario, Flipper Zero no detectará el microchip.

## <mark style="color:orange;">Microchips RFID para animales compatibles con Flipper Zero</mark> <a href="#id-2tz-v" id="id-2tz-v"></a>

* **Microchips compatibles** : [FDX-B](https://www.priority1design.com.au/fdx-b_animal_identification_protocol.html) (15 dígitos, compatible con ISO, incluidos microchips térmicos), FDX-A (10 dígitos, no compatible con ISO) y otros chips compatibles con Flipper Zero en el formato de un microchip animal.
* **Frecuencia de lectura:** 125 kHz. Flipper Zero también puede leer microchips en el rango de 110-140 kHz, pero con una distancia de lectura más corta.
* **Distancia de lectura:** 10 mm (0,39 pulgadas).

## <mark style="color:orange;">Lectura de microchips de animales</mark> <a href="#di0dg" id="di0dg"></a>

Los microchips para animales se pueden colocar en [diferentes lugares](https://wsava.org/wp-content/uploads/2020/01/Veterinary-List-of-Recommended-Microchip-Implantation-Sites.pdf) . En los perros y los gatos, el microchip se coloca debajo de la piel, en la parte posterior del cuello, **entre los omoplatos,** en la línea media dorsal. Las mascotas de Europa continental reciben un microchip **en la región media del cuello izquierdo**.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-yWQb-M5UMODNBjGPfDOJd-20241024-181823.png?format=webp" alt=""><figcaption></figcaption></figure>

### <mark style="color:orange;">Método 1. Localizar el microchip con los dedos</mark> <a href="#zblq9" id="zblq9"></a>

Recomendamos localizar primero el microchip del animal con los dedos y luego leerlo con el Flipper Zero. Mueva las yemas de los dedos sobre la piel de la mascota entre los omoplatos y la región media del cuello izquierdo. Aplique una presión suave para ver si puede detectar un objeto sólido del tamaño de un grano de arroz justo debajo de la piel. Tenga en cuenta que los microchips de los animales pueden migrar ligeramente de la ubicación original.

Una vez que hayas localizado el microchip, escanéalo con tu Flipper Zero usando la codificación ASK:

1. Vaya al **Menú principal -> RFID 125 kHz -> Acciones adicionales** .
2. Seleccione **Leer ASK** y presione **OK** .
3. Mantenga su Flipper Zero lo más cerca posible del microchip y no mueva el dispositivo durante tres segundos.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-BTwhIvFlP8EllkhJGx7ZW-20241107-102807.png?format=webp" alt=""><figcaption></figcaption></figure>

Sostén el Flipper Zero de manera que el microchip esté en el centro de la parte posterior del dispositivo.﻿

### <mark style="color:orange;">Método 2. Localización del microchip con el Flipper Zero</mark> <a href="#wvb0g" id="wvb0g"></a>

Para localizar y leer el microchip del animal, debe colocar su Flipper Zero con precisión sobre el microchip lo más cerca posible y esperar tres segundos. Para aumentar la probabilidad de detectar el microchip del animal, le recomendamos leer en el modo de `codificación ASK`:

1. Vaya al **Menú principal -> RFID 125 kHz -> Acción adicional** .
2. Seleccione **Leer ASK** y presione **OK** .
3. Mueva su Flipper Zero lo más cerca posible de la piel de la mascota ( la parte posterior del dispositivo orientada hacia la piel del animal ) y mueva el dispositivo paso a paso, sosteniéndolo durante tres segundos en cada ubicación.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-uDjsDej3RICnWIbDj9_0h-20241107-102819.png?format=webp" alt=""><figcaption></figcaption></figure>

Es importante mantener su Flipper Zero quieto durante tres segundos en cada parada.﻿

Mueva su Flipper Zero siguiendo el patrón que se muestra a continuación hasta que se detecte el microchip.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-iIjHejI9KHa_nUcudwSbP-20241024-182334.png?format=webp" alt=""><figcaption></figcaption></figure>

Preste atención a la indicación LED en su Flipper Zero. La indicación LED le ayudará a localizar el microchip.﻿:

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/n2vGgEFstHBS0K4TuI6Qt_monosnap-miro-2023-08-04-13-44-38.jpg?format=webp" alt=""><figcaption></figcaption></figure>

Si no se detecta el microchip , gire su Flipper Zero 90° y repita el procedimiento de escaneo como se muestra a continuación.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-HLzzshH8LDvCtSShpqVMg-20241024-182359.png?format=webp" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">**Si su Flipper Zero no**</mark> <mark style="color:orange;"></mark><mark style="color:orange;">detecta</mark> <mark style="color:orange;"></mark><mark style="color:orange;">**el microchip**</mark> <a href="#n20-y" id="n20-y"></a>

* Es posible que el microchip esté fuera de rango. -> Intenta mover tu Flipper Zero siguiendo los patrones que se muestran arriba, con pasos más pequeños y mantén el dispositivo en cada parada un poco más.
* El microchip podría migrar de la ubicación original. -> Intenta cubrir un área más grande con tu Flipper Zero.
* Los objetos metálicos y equipos electrónicos pueden afectar la detección del microchip. -> Intente escanear al animal lejos de estos objetos.
* El animal podría tener un microchip RFID de alta frecuencia. -> Intenta escanearlo [usando la aplicación NFC](https://docs.flipperzero.one/nfc/read) .
* Es posible que el animal tenga un tipo de microchip no compatible. -> Comuníquese con su clínica veterinaria local para escanear al animal con su equipo.

## <mark style="color:orange;">Estructura de datos del microchip RFID para animales</mark> <a href="#wtjoc" id="wtjoc"></a>

Después de capturar los datos del microchip, Flipper Zero mostrará la información sobre el animal: tipo de microchip, número de identificación, datos del microchip y temperatura del animal (si el microchip puede medirla).

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/meOm-VShGcnWAUDS4sepx_monosnap-miro-2023-08-04-13-44-59.jpg?format=webp" alt=""><figcaption><p>Estructura de datos de un microchip FDX-B compatible con ISO﻿</p></figcaption></figure>

Los microchips para animales que cumplen con la norma ISO tienen números de identificación de 15 dígitos. Los primeros tres dígitos representan un código [numérico](https://en.wikipedia.org/wiki/ISO_3166-1_numeric) de país ISO 3166-1 o un [código de fabricante](https://cdn.flipperzero.one/manufacturersisosandcountrycodes.pdf) . Los 12 dígitos restantes representan el número único del microchip.
