
# NFC

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-ECak9q-WNAb6hlhRC7bCl-20241025-091909.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero es compatible con la tecnología NFC, que se implementa en tarjetas inteligentes de transporte público, tarjetas de acceso o etiquetas y tarjetas de presentación digitales. Estas tarjetas tienen protocolos complejos y admiten cifrado, autenticación y transferencia de datos bidireccional completa. Flipper Zero tiene un módulo NFC de 13,56 MHz integrado capaz de leer, guardar y emular tarjetas NFC.

Inserte una tarjeta microSD para usar la aplicación NFC. Antes de usar la aplicación NFC, asegúrese de actualizar el firmware de Flipper Zero con una tarjeta microSD insertada, ya que Flipper Zero almacena bases de datos en una tarjeta microSD. Para obtener más información sobre el proceso de actualización, visite la página [de actualización de firmware .](https://docs.flipperzero.one/basics/firmware-update)﻿﻿

## <mark style="color:orange;">Menú NFC</mark> <a href="#qrfq1" id="qrfq1"></a>

Puedes acceder a la aplicación NFC desde el Menú Principal. En la aplicación, puedes interactuar con tarjetas NFC, analizar lectores y generar tarjetas NFC.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/sxVJfLTi3S3vuUMROKnoA_image.png?format=webp" alt=""><figcaption><p>Menú de la aplicación NFC﻿</p></figcaption></figure>

* ﻿[Leer:](https://docs.flipperzero.one/nfc/read) lee y guardade, como UID, SAK, ATQA y datos almacenados.
* ﻿[Extraer claves MF:](https://docs.flipper.net/nfc/mfkey32#-DSjM)﻿ emula una tarjeta NFC para recopilar datos ( [nonces](https://en.wikipedia.org/wiki/Cryptographic_nonce) ) utilizados para calcular las claves intentadas por un lector.
* **Guardado:** enumera las tarjetas NFC guardadas, que se pueden emular y cambiar de nombre.
* **Acciones adicionales:** scripts de lectura adicionales, complementos, gestión de claves, etc.
* ﻿[Agregar manualmente:](https://docs.flipper.net/nfc/add-manually) genera nuevas tarjetas NFC virtuales ingresandolas manualmente.

## <mark style="color:purple;">Hardware NFC</mark> <a href="#aoyvj" id="aoyvj"></a>

Flipper Zero tiene un módulo NFC integrado basado en un [chip NFC ST25R3916](https://www.st.com/en/nfc/st25r3916.html#overview) y una antena de alta frecuencia de 13,56 MHz. El chip se utiliza para protocolos de alta frecuencia y es responsable de la lectura y emulación de tarjetas.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/9XmJfDiY5bfEwnuohxxsF_image.png?format=webp" alt=""><figcaption></figcaption></figure>

La antena de alta frecuencia de 13,56 MHz se coloca en la antena RFID de doble banda junto a la antena de baja frecuencia de 125 kHz.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/pnsmXFwTUPK1P4B0QVYuh_image.png?format=webp" alt=""><figcaption><p>Antena RFID de doble banda</p></figcaption></figure>
