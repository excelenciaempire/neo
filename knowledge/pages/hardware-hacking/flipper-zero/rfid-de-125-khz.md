
# RFID de 125 kHz

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-NUgMYUy2yqX9dy6_MJfb7-20241024-180922.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero es compatible con la tecnología de identificación por radiofrecuencia (RFID) de baja frecuencia (LF) que se implementa en sistemas de control de acceso, chips para animales y sistemas de seguimiento de la cadena de suministro. A diferencia de las tarjetas NFC, las tarjetas RFID LF no suelen ofrecer altos niveles de seguridad. Esta tecnología se presenta en muchos formatos, como tarjetas de plástico, llaveros, etiquetas, pulseras y microchips para animales. Flipper Zero tiene un módulo RFID de baja frecuencia capaz de leer, guardar, emular y escribir tarjetas RFID LF.

Inserte una tarjeta microSD para utilizar la aplicación RFID de 125 kHzAntes de utilizar la aplicación RFID de 125 kHz, asegúrese de actualizar el firmware de Flipper Zero con una tarjeta microSD insertada, ya que Flipper Zero almacena bases de datos en una tarjeta microSD. Para obtener más información sobre el proceso de actualización, visite la página [de actualización de firmware .](https://docs.flipperzero.one/basics/firmware-update)﻿﻿

## <mark style="color:orange;">Menú RFID de 125 kHz</mark> <a href="#bv_w4" id="bv_w4"></a>

Puede acceder a la aplicación RFID de 125 kHz desde el Menú principal. En la aplicación, puede leer, guardar, emular, escribir y generar nuevas tarjetas RFID LF.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/srFuJIxYqC8TaGqECmY57_monosnap-miro-2023-09-12-15-01-29.jpg?format=webp" alt=""><figcaption><p>Menú de aplicaciones RFID de 125 kHz﻿</p></figcaption></figure>

* ﻿[Leer:](https://docs.flipperzero.one/rfid/read) lee y guarda tarjetas RFID LF.
* **Guardados:** enumera las tarjetas guardadas que se pueden [emular](https://docs.flipperzero.one/rfid/read#5MRwS) y [escribir](https://docs.flipper.net/rfid/write-data) en una tarjeta regrabable.
* ﻿[Agregar manualmente:](https://docs.flipperzero.one/rfid/add-manually) genera nuevas tarjetas RFID LF virtuales ingresando el ID de las tarjetas.
* **Acciones Extra:** permite leer tarjetas RFID LF con la codificación ASK o PSK preseleccionada.

## <mark style="color:orange;">Hardware RFID de 125 kHz</mark> <a href="#ctlru" id="ctlru"></a>

Flipper Zero tiene soporte RFID integrado con una antena de baja frecuencia ubicada en la parte posterior de Flipper Zero. La unidad de microcontrolador STM32WB55 se utiliza para la funcionalidad RFID de 125 kHz.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/5eSBYsSUbS2T87YGVZBjz_image.png?format=webp" alt=""><figcaption></figcaption></figure>

La antena de baja frecuencia de 125 kHz se coloca en la antena RFID de doble banda junto a la antena de alta frecuencia de 13,56 MHz.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/quAVWEi_M28-IALyI6BMO_image.png?format=webp" alt=""><figcaption><p>ntena RFID de doble banda</p></figcaption></figure>
