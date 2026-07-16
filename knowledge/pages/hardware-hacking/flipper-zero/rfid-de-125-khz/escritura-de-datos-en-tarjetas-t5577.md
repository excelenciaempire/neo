
# Escritura de datos en tarjetas T5577

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-vaj3FU3Tik1TnrSpSj_CW-20241107-102744.png?format=webp" alt=""><figcaption></figcaption></figure>

En general, las tarjetas y llaveros RFID de 125 kHz son de solo lectura. Si se pueden escribir, normalmente tienen una contraseña y utilizan un chip incompatible con Flipper Zero para escribir. Sin embargo, existen tarjetas en blanco regrabables T5577, que se pueden programar para emular tarjetas con varios protocolos RFID de baja frecuencia.

Puede escribir tarjetas de 125 kHz guardadas y agregadas manualmente en tarjetas en blanco T5577. Estas tarjetas en blanco vienen en diferentes formas y tamaños, como tarjetas, llaveros, calcomanías y microchips para animales. Flipper Zero puede escribir datos con todos los protocolos RFID de baja frecuencia compatibles.

## <mark style="color:orange;">Escritura de datos</mark>

Para escribir datos en la tarjeta, haga lo siguiente:

1. Vaya al **Menú principal -> RFID 125 kHz -> Saved**
2. Seleccione la tarjeta que desea escribir y luego presione **Escribir**
3. Sostén el Flipper Zero cerca de la tarjeta en blanco T5577, con la parte posterior del dispositivo orientada hacia la tarjeta.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/4OLd8i7ScKnLYB400y-H6_image.png?format=webp" alt=""><figcaption></figcaption></figure>

Sostén la tarjeta en el centro de la parte posterior de tu Flipper Zero.﻿4

Después de escribir datos en la tarjeta en blanco, el dispositivo mostrará el mensaje **Escrito exitosamente** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/-ABqxxpZ1edTUlR99IkcE_monosnap-miro-2023-09-12-14-32-23.jpg?format=webp" alt=""><figcaption></figcaption></figure>

Tenga en cuenta que su Flipper Zero puede mostrar el  mensaje **"Escrito correctamente"**  al escribir en una tarjeta de solo lectura. Esto puede suceder si los mismos datos ya están presentes en la tarjeta de solo lectura.

## <mark style="color:orange;">Si la escritura falló</mark> <a href="#id-16d-t" id="id-16d-t"></a>

* La tarjeta en blanco T5577 puede estar protegida con una contraseña.
* Está intentando escribir en una tarjeta RFID de solo lectura, no en una tarjeta en blanco T5577.
* No todas las tarjetas son regrabables﻿

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/pxrZdGMjevNVBwStiQFLK_monosnap-miro-2023-09-12-11-34-39.jpg?format=webp" alt=""><figcaption></figcaption></figure>
