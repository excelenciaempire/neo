
# Lectura de tarjetas NFC

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-u1LYs23GvHeBO8r7-18au-20241025-091938.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero permite leer, guardar y emular tarjetas NFC. Una tarjeta NFC es un transpondedor que funciona a 13,56 MHz y tiene un número único (UID), así como una parte de la memoria regrabable para almacenar datos. Según el tipo de tarjeta, la memoria se puede segmentar en sectores, páginas, aplicaciones y más. Cuando se acercan a un lector, las tarjetas NFC transmiten los datos solicitados.

## <mark style="color:orange;">Cómo leer tarjetas NFC</mark> <a href="#mfysg" id="mfysg"></a>

El proceso de lectura es automático y no requiere que el usuario lo configure manualmente.

Para leer y guardar los datos de la tarjeta NFC , haga lo siguiente:

1. Vaya al **Menú principal -> NFC**
2. Presiona **Leer** , luego sostén la tarjeta cerca de la parte posterior de tu Flipper Zero

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-gnszUyotO_ud3xoQys1F9-20241025-092103.png?format=webp" alt=""><figcaption></figcaption></figure>

3. No mueva la tarjeta mientras la lee. El proceso de lectura puede tardar varios minutos.﻿3
4. Cuando termine de leer, vaya a **Más -> Guardar** .
5. Nombra la tarjeta leída y luego presiona **Guardar** .

### <mark style="color:orange;">Leyendo lo que hay en la tarjeta</mark> <a href="#md7f" id="md7f"></a>

En el caso de algunas tarjetas, Flipper Zero puede leer y mostrar datos en un formato legible. Por ejemplo, puedes obtener información como la fecha de validez de la tarjeta, el saldo o los viajes restantes. Esta funcionalidad es posible gracias a los analizadores que aporta la comunidad. Puedes ver la lista completa de analizadores disponibles en el [repositorio de GitHub de Flipper Zero](https://github.com/flipperdevices/flipperzero-firmware/tree/dev/applications/main/nfc/plugins/supported_cards) .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/AQ3NAORc_8qJTRMf9PUWl_image.png?format=webp" alt=""><figcaption></figcaption></figure>

#### Si la lectura falló: <a href="#id-9rrh" id="id-9rrh"></a>

* Es posible que la tarjeta utilice tecnología RFID de 125 kHz. -> Lea la tarjeta con la [aplicación RFID de 125 kHz](https://docs.flipperzero.one/rfid) .
* La tarjeta puede combinar dos tipos diferentes de tarjetas NFC en una sola tarjeta. -> [Preseleccione el tipo de tarjeta que desea leer](https://docs.flipperzero.one/nfc/read#DcXWX) .

## <mark style="color:orange;">Tarjetas NFC tipo A</mark> <a href="#fgawl" id="fgawl"></a>

#### MIFARE Classic® <a href="#aqfwj" id="aqfwj"></a>

Flipper Zero puede leer tarjetas MIFARE Classic 1K, MIFARE Classic 4K y MIFARE Classic Mini y guardar datos. Para leer los datos almacenados en sectores, Flipper Zero tiene que encontrar las 32 claves para 16 sectores (MIFARE Classic 1K), las 80 claves para 40 sectores (MIFARE Classic 4K) y las 10 claves para 5 sectores (MIFARE Classic Mini). Para ello, Flipper Zero utiliza claves del **diccionario del sistema** .

Puede agregar sus claves al **diccionario de usuario** yendo a **Menú principal -> NFC -> Acciones adicionales -> Claves clásicas MIFARE** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/Ez8ZD9nkjXRr2uPsvsh94_image.png?format=webp" alt=""><figcaption><p>Datos capturados organizados en sectores﻿</p></figcaption></figure>

Para las tarjetas MIFARE Classic, Flipper Zero emula solo sectores desbloqueados.﻿

Después de que Flipper Zero lee una tarjeta MIFARE Classic, los datos originales se almacenan en la memoria. Cuando implementa cambios en los datos a través de [la aplicación Flipper Mobile](https://docs.flipperzero.one/mobile-app) o mediante [la emulación](https://docs.flipperzero.one/nfc/read#Cy_5M) a través de su Flipper Zero, el dispositivo genera un nuevo archivo shadow que representa el nuevo estado de los datos. Esto provoca la desincronización entre el estado real de su Flipper Zero y la tarjeta física. Para sincronizar la tarjeta física con el estado de los datos de su Flipper Zero, utilice la función **Escribir en la tarjeta inicial** .

De manera similar, los datos de la tarjeta física pueden modificarse después de la interacción con un lector, lo que provoca la desincronización de los estados de los datos. Para sincronizar los estados, utilice la función **Actualizar desde la tarjeta inicial .**

Puede descartar los cambios realizados en su Flipper Zero utilizando la función **Restaurar al original** . En este caso, Flipper Zero elimina el archivo shadow.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/TyieRKpgtiI06ZgdZ6044_image.png?format=webp" alt=""><figcaption><p>Puede sincronizar estados de datos entre Flipper Zero y la tarjeta física﻿﻿</p></figcaption></figure>

#### MIFARE Ultralight® y NTAG® <a href="#rhfhr" id="rhfhr"></a>

Para las tarjetas MIFARE Ultralight y NTAG, Flipper Zero puede leer y guardar datos en páginas abiertas.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/hQ7-uVjrLXHsaFUEY3-HU_image.png?format=webp" alt=""><figcaption><p>Datos capturados organizados en páginas﻿</p></figcaption></figure>

Para las tarjetas MIFARE Ultralight y NTAG, Flipper Zero emula únicamente las páginas que fueron leídas.﻿

Flipper Zero puede escribir datos NTAG guardados en otra tarjeta NTAG del mismo tipo (por ejemplo, NTAG 213 - NTAG 213). Esta función está disponible para las tarjetas NTAG 213, NTAG 215 y NTAG 216. Las tarjetas NTAG iniciales y de destino deben tener su PWD, PACK y AUTH0 deshabilitados por defecto. Además, los bits de bloqueo estático y dinámico deben ser 0 tanto para las tarjetas NTAG iniciales como para las de destino, lo que garantiza que toda la memoria del usuario esté desbloqueada.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/npJrVsYrMNXrM2dG5qAMP_monosnap-miro-2023-12-08-18-54-13.jpg?format=webp" alt=""><figcaption><p>Puede escribir datos NTAG en otras tarjetas NTAG﻿﻿</p></figcaption></figure>

#### MIFARE® DESFire® <a href="#icdui" id="icdui"></a>

Flipper Zero puede leer tarjetas MIFARE DESFire y guardar datos. En este tipo de tarjeta, la memoria se organiza en aplicaciones con múltiples archivos. Flipper Zero lee y guarda aplicaciones y archivos sin protección con datos.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/Q7vSvbPMantuBnvFnzKgg_image.png?format=webp" alt=""><figcaption><p>Datos capturados organizados en aplicaciones</p></figcaption></figure>

﻿Para las tarjetas MIFARE DESFire, Flipper Zero solo puede emular el UID.﻿﻿

#### Tarjetas desconocidas <a href="#id-37eo8" id="id-37eo8"></a>

Al leer una tarjeta NFC desconocida, Flipper Zero lee y guarda solo el UID, SAK y ATQA.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/3JC7vjwnJfkS_PXVFDZcE_image.png?format=webp" alt=""><figcaption><p>Datos capturados de una tarjeta ISO desconocida</p></figcaption></figure>

﻿Para tarjetas NFC desconocidas, Flipper Zero solo puede emular el UID.﻿﻿

## <mark style="color:orange;">Tarjetas NFC tipo V</mark> <a href="#o3fjc" id="o3fjc"></a>

#### ICODE® SLIX <a href="#fpu9d" id="fpu9d"></a>

Flipper Zero puede leer y guardar datos almacenados en etiquetas ICODE SLIX, SLIX-2, SLIX-L y SLIX-S. En estas etiquetas, la memoria está organizada en bloques.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/HXAfpPZxEb2rqVtyQtvpz_monosnap-miro-2023-06-20-14-03-50.jpg?format=webp" alt=""><figcaption><p>Datos capturados organizados en bloques</p></figcaption></figure>

﻿Para las tarjetas ICODE SLIX, Flipper Zero puede emular el UID y los datos en bloques.﻿

#### Tarjetas desconocidas <a href="#uw4u5" id="uw4u5"></a>

Al leer una tarjeta NFC-V desconocida, Flipper Zero lee y guarda el UID y los datos en bloques de lectura.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/b1X4elL7KQf8-HqE-Fl34_monosnap-miro-2023-06-22-14-02-38.jpg?format=webp" alt=""><figcaption><p>Datos capturados de una tarjeta NFC-V desconocida﻿</p></figcaption></figure>

Para tarjetas NFC-V desconocidas, Flipper Zero puede emular el UID y los datos en bloques de lectura.﻿﻿

## <mark style="color:orange;">Tarjetas NFC tipo F</mark> <a href="#vc-cr" id="vc-cr"></a>

#### FeliCa™ Lite-S <a href="#m1io4" id="m1io4"></a>

Flipper Zero puede leer, guardar y emular tarjetas FeliCa Lite-S. En particular, puede leer el ID de fabricación (IDm), el parámetro de fabricación (PMm) y los datos en bloques .

﻿

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/baMu164pe2roL4uVaA4hV_image.png?format=webp" alt=""><figcaption></figcaption></figure>

Si su Flipper Zero lee 26 de 28 bloques, significa que todos los datos se han leído correctamente. Esto sucede debido a la naturaleza de la lectura de las tarjetas FeliCa. Sin embargo, si tiene menos de 26 bloques leídos, significa que algunos bloques están bloqueados. Para acceder a estos bloques bloqueados, use la función Desbloquear e ingrese la clave de 16 bits del fabricante.﻿﻿

## <mark style="color:orange;">Tarjetas NFC tipo B</mark> <a href="#wyg51" id="wyg51"></a>

#### ST25TB <a href="#tfcbs" id="tfcbs"></a>

Flipper Zero puede leer y guardar tarjetas ST25TB . Se pueden capturar los datos de la tarjeta y el UID .﻿

Se admiten los siguientes tipos de tarjetas con diferente organización de memoria:

* ST25TB512
* ST25TB512-AC
* SRIX512
* ST25TB02K
* ST25TB04K
* SRIX4K

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/OL0izPoPPG3hErxPGvizT_image.png?format=webp" alt=""><figcaption></figcaption></figure>

#### Otras tarjetas NFC tipo B <a href="#id-97wv6" id="id-97wv6"></a>

Para otras tarjetas NFC tipo B, Flipper Zero solo puede leer y mostrar el UID sin guardarlo.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/pNqqhBDEjrOD8ej2z2wf5_monosnap-miro-2023-06-22-13-58-13.jpg?format=webp" alt=""><figcaption><p>Datos capturados de una tarjeta NFC tipo B﻿﻿</p></figcaption></figure>

### Lectura de un tipo de tarjeta específico <a href="#dcxwx" id="dcxwx"></a>

Las tarjetas híbridas combinan dos tipos de tarjetas NFC en una sola tarjeta. Por ejemplo, una tarjeta EMV se puede combinar con una tarjeta MIFARE Classic. En este caso, deberá especificar qué tipo de tarjeta desea leer haciendo lo siguiente:

1. Vaya al **Menú principal -> NFC -> Acciones adicionales -> Leer tipo de tarjeta específico** .
2. Seleccione el tipo de tarjeta que desea leer y luego presione **OK** .
3. Sostenga la tarjeta cerca de la parte posterior de su Flipper Zero para leer los datos de la tarjeta .

## <mark style="color:orange;">Emulación de tarjetas NFC</mark> <a href="#cy_5m" id="cy_5m"></a>

Flipper Zero puede emular una tarjeta NFC completa o solo el UID según el tipo de tarjeta NFC y los datos guardados.

Para emular la tarjeta NFC guardada, haga lo siguiente:

1. Vaya al **Menú principal -> NFC -> Saved**
2. Seleccione la tarjeta y luego presione **Emulate**

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/d5PaBknny0wsAWLNwJd4W_monosnap-miro-2023-06-22-14-20-08.jpg?format=webp" alt=""><figcaption></figcaption></figure>

Mantenga su Flipper Zero cerca del lector para transferir datos.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/YVyto0hMEn8sKwC78Kh4V_image.png?format=webp" alt=""><figcaption></figcaption></figure>

Mientras emula la tarjeta NFC, sostenga su Flipper Zero cerca del lector﻿Al emular tarjetas MIFARE Classic, Flipper Zero intenta adivinar la frecuencia del lector para modular correctamente la señal. Flipper Zero supone que la frecuencia de campo es exactamente 13,56 MHz. Si la frecuencia difiere significativamente, la señal no se modulará correctamente, lo que provocará errores de emulación.﻿﻿
