
# Añadir nuevas tarjetas NFC

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-D_amnmZ1ylbnryXnoir95-20241025-093010.png?format=webp" alt=""><figcaption></figcaption></figure>

﻿Con Flipper Zero, puede generar varias tarjetas NFC que se pueden programar como llaves en sistemas de control de acceso o escribir diversos datos en ellas usando su teléfono inteligente, como enlaces a su sitio web personal, currículum o tarjeta de presentación. Ya no necesita comprar nuevas tarjetas NFC físicas, ya que puede programar su Flipper Zero para que actúe como una llave.﻿

## ﻿<mark style="color:orange;">Creación de tarjetas NFC</mark> <a href="#ywzbl" id="ywzbl"></a>

Hay dos formas de crear tarjetas NFC, según tus necesidades:

* Generar una tarjeta NFC a partir de la lista de tipos de tarjetas estándar disponibles con un UID aleatorio.
* Cree manualmente una tarjeta NFC-A ingresando los valores UID, ATQA y SAK que podrían funcionar con sistemas de control de acceso simples que usan el UID de la tarjeta para autenticar a los usuarios.

Repasemos ambas opciones.

## <mark style="color:orange;">Generar un tipo específico de tarjeta NFC</mark> <a href="#id-9rsyl" id="id-9rsyl"></a>

Puede crear tarjetas NFC virtuales con la misma organización de datos que las siguientes tarjetas NFC:

* MIFARE Ultralight®
* MIFARE Ultralight® EV1 11
* MIFARE Ultralight® EV1 H11
* MIFARE Ultralight® EV1 21
* MIFARE Ultralight® EV1 H21
* NTAG® 203
* NTAG® 213
* NTAG® 215
* NTAG® 216
* NTAG® I2C 1K
* NTAG® I2C 2K
* NTAG® I2C más 1K
* NTAG® I2C más 2K
* MIFARE Mini®
* MIFARE Classic® 1K con un UID de 4 bytes
* MIFARE Classic® 1K con un UID de 7 bytes
* MIFARE Classic® 4K con un UID de 4 bytes
* MIFARE Classic® 4K con un UID de 7 bytes

Si desea utilizar la tarjeta NFC creada con su teléfono inteligente, NTAG 216 debería funcionar en la mayoría de los casos. Sin embargo, el tipo de tarjeta que debe utilizar varía según sus requisitos. Consulte la documentación de la aplicación o el dispositivo con el que planea utilizarla.﻿

La tarjeta NFC virtual tendrá un UID aleatorio y valores de datos predeterminados, similares a una nueva tarjeta NFC física vacía.

Para generar una tarjeta, haga lo siguiente:

1. Vaya al **Menú principal -> NFC -> Agregar manualmente**
2. Seleccione el tipo de tarjeta NFC que necesita
3. Revise los datos y luego seleccione **Más**
4. Ingrese el nombre de la tarjeta y luego seleccione **Guardar**

Una vez guardada la tarjeta, se puede programar para que funcione como tecla de acceso o para almacenar datos, como una URL que conduce a un sitio web.﻿

Los distintos sistemas de control de acceso y aplicaciones móviles tienen distintos procedimientos de programación. Consulte la documentación de su sistema o aplicación de control de acceso para obtener instrucciones y conocer los tipos de tarjetas compatibles.﻿

### <mark style="color:orange;">Emulación de la tarjeta</mark>

Antes de programar la tarjeta NFC virtual creada, es necesario emularla para que un lector la reconozca como una tarjeta NFC física.

Siga estos pasos:

1. Vaya al **Menú principal -> NFC -> Guardado** .
2. Seleccione la tarjeta agregada y presione **Emular** .
3. Mantenga su Flipper Zero cerca del lector o teléfono inteligente para programarlo.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-go9hvvkOvcRGrEcuJCR59-20241025-093158.png?format=webp" alt=""><figcaption><p>Debes emular la tarjeta guardada para que Flipper Zero actúe como una tarjeta física﻿</p></figcaption></figure>

## <mark style="color:orange;">Crear una tarjeta NFC manualmente</mark>﻿ <a href="#h2vtu" id="h2vtu"></a>

Algunos sistemas de control de acceso utilizan los datos UID, ATQA y SAK para otorgar acceso. Si conoce estos valores, puede ingresarlos manualmente para crear la tarjeta NFC necesaria:

1. Vaya al **Menú principal -> NFC -> Agregar manualmente** .
2. Seleccione el tipo de tarjeta NFC necesario según el tamaño del UID:

* NFC-Un UID de 7 bytes *o*
* NFC-A UID de 4 bytes

3. **Ingrese el valor SAK** conocido en hexadecimal, luego seleccione **Guardar** .
4. **Ingrese el valor ATQA** conocido en hexadecimal, luego seleccione **Guardar** .
5. Ingrese el valor **UID** conocido en hexadecimal, luego seleccione **Guardar** .
6. Ingrese el nombre de la tarjeta y luego seleccione **Guardar.**

Una vez que hayas guardado la tarjeta con los valores conocidos, podrás utilizarla como clave de acceso.
