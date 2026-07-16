
# Escritura de datos en Magic Cards

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-krTDtVEgklKVffjrKttyY-20241025-092905.png?format=webp" alt=""><figcaption></figcaption></figure>

Las tarjetas NFC estándar tienen números de identificación únicos (UID) asignados por el fabricante. Estos números no se pueden cambiar . Las tarjetas **NFC Magic** o **UID regrabables** son tarjetas especiales que pueden cambiar sus UID. Eso hace que las tarjetas Magic sean más poderosas: pueden copiar el UID y los datos de una tarjeta original. Existen [diferentes generaciones](https://lab401.com/blogs/academy/know-your-magic-cards) de tarjetas Magic.

Para utilizar esta función, debes descargar la aplicación [NFC Magic a tu Flipper Zero desde ](https://lab.flipper.net/apps/nfc_magic)[Aplicaciones .](https://docs.flipper.net/apps)﻿﻿

## <mark style="color:orange;">Escribir datos de la tarjeta</mark> <a href="#z3dni" id="z3dni"></a>

Flipper Zero puede escribir datos en tarjetas mágicas **Gen1** , **Gen2** y **Gen4** , así como en tarjetas **MIFARE Classic® normales** (sin reescribir el UID) .

**Las cartas mágicas Gen1** se pueden configurar como el siguiente tipo de carta:

* MIFARE Classic® 1K

**Las cartas mágicas Gen2** se pueden configurar como el siguiente tipo de carta:

* MIFARE Classic® 1K (se requiere una tarjeta Gen 2 compatible)
* MIFARE Classic® 4K (se requiere una tarjeta Gen 2 compatible)

**Las cartas mágicas Gen4 (Ultimate)** se pueden configurar como los siguientes tipos de cartas:

* Cualquier MIFARE Classic®
* MIFARE Ultralight® EV1
* MIFARE Ultralight® EV2
* NTAG® 203
* NTAG® 213
* NTAG® 215
* NTAG® 216

Para copiar la tarjeta NFC original, debes escribir el UID y los datos originales en la tarjeta mágica NFC haciendo lo siguiente:

1. ﻿[Lea y guarde la tarjeta original](https://docs.flipperzero.one/nfc/read) . Asegúrese de que su Flipper Zero lea todos los sectores o páginas de la tarjeta original
2. Vaya al **Menú principal -> Aplicaciones -> NFC -> NFC Magic**
3. Comprueba si tienes una magic card Gen1, Gen2 o Gen4 compatible usando la opción **Check Magic Tag** y sosteniendo la magic card cerca de la parte posterior de tu Flipper Zero . *O* si tienes una tarjeta Gen4 protegida con contraseña, ve a **Acciones Gen4 -> Autenticación con contraseña** para ingresar la contraseña manualmente. Luego, usa la opción **Check Magic Tag** .

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-PYPg8lTp6xekgfufC9sKD-20241107-112912.png?format=webp" alt=""><figcaption><p>Sostenga la tarjeta cerca de la parte posterior de su Flipper Zero﻿</p></figcaption></figure>

4. Si la tarjeta mágica es compatible, verás el mensaje a continuación; de lo contrario, tu Flipper Zero seguirá intentando determinar el tipo de tarjeta.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/Tui4uuc2lF8FYPA7hbP-X_image.png?format=webp" alt=""><figcaption><p>Tu Flipper Zero te avisará si tienes la magic card</p></figcaption></figure>

5. Vaya a **Más** para ver las opciones para este tipo de carta mágica.
6. Para escribir el UID y los datos de la tarjeta original, utilice la opción **Escribir**.
7. Selecciona la tarjeta original en el navegador y mantén la tarjeta mágica cerca de la parte posterior de tu Flipper Zero.
8. Una vez que tu Flipper Zero escriba datos en la tarjeta mágica, verás el mensaje a continuación.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/FqbYTQSK6M0vIbvjA7rWV_image.png?format=webp" alt=""><figcaption><p>Los datos de la tarjeta original se escriben en la magic card</p></figcaption></figure>

También puedes formatear la tarjeta mágica usando la opción  **Borrar** : el UID se restablecerá al valor predeterminado y se eliminarán los datos de los sectores o páginas.
