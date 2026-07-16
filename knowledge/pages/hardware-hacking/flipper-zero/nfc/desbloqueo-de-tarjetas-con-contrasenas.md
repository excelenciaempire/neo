
# Desbloqueo de tarjetas con contraseñas

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-MFsPWijVuiBwTA2sNqlul-20241107-112823.png?format=webp" alt=""><figcaption></figcaption></figure>

Existen tarjetas NFC que tienen los datos organizados en páginas, como las tarjetas MIFARE Ultralight® y NTAG®. Si no puede leer todas las páginas de la tarjeta NFC con la función [Leer](https://docs.flipperzero.one/nfc/read) , es posible que la tarjeta esté protegida con una contraseña. Para desbloquear la tarjeta protegida, puede ingresar la contraseña manualmente, generar la contraseña para desbloquear las páginas o extraer la contraseña del lector.

El uso de estas funciones podría bloquear su tarjeta. Algunas tarjetas tienen una función de seguridad que bloquea la tarjeta después de varias autenticaciones con una contraseña incorrecta.﻿

## <mark style="color:orange;">Extraer la contraseña del lector</mark> <a href="#id-2chnn" id="id-2chnn"></a>

Si tiene acceso al lector y a la tarjeta, intente extraer la contraseña del lector emulando los datos de la tarjeta capturada . El lector puede autenticar la tarjeta con una contraseña, que puede ser capturada y guardada por su Flipper Zero. Después de eso, puede leer los datos en las páginas restantes de la tarjeta .

Para extraer la contraseña y desbloquear la tarjeta, haga lo siguiente:

1. ﻿[Lea y guarde](https://docs.flipperzero.one/nfc/read) la tarjeta
2. Vaya al **Menú principal -> NFC -> Guardados -> Nombre de la tarjeta -> Desbloquear**
3. Seleccione **Desbloquear con lector** y luego toque el lector con su Flipper Zero

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-nGTWC9NTOp_sNkrlmdgce-20241107-112752.png?format=webp" alt=""><figcaption><p>Para capturar la contraseña, toque el lector con su Flipper Zero﻿</p></figcaption></figure>

4. Cuando haya capturado la contraseña, presione **Continuar**

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/rWzAZTDZa-jy6y5TsRHl7_flipperzerounlocknfccardswithreader.png?format=webp" alt=""><figcaption><p>La contraseña capturada se muestra en la pantalla.</p></figcaption></figure>

5. Lee la tarjeta sosteniéndola cerca de la parte posterior de tu Flipper Zero

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-PYPg8lTp6xekgfufC9sKD-20241107-112912.png?format=webp" alt=""><figcaption><p>Sostén la tarjeta en el centro de la parte posterior de tu Flipper Zero.﻿</p></figcaption></figure>

6. Una vez desbloqueadas las páginas, presione **Guardar**

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/nnLEnF_-6NW9uYSM9n6uS_successfulunlockofallpagesofnfccard.png?format=webp" alt=""><figcaption><p>El número de páginas leídas se muestra en la pantalla.﻿</p></figcaption></figure>

7. Nombra la tarjeta y luego presiona **Guardar**

### Si el desbloqueo falló <a href="#dylqr" id="dylqr"></a>

* Es posible que la tarjeta esté conectada a otro lector.

## <mark style="color:orange;">Generando la contraseña</mark> <a href="#gh6u3" id="gh6u3"></a>

Con Flipper Zero, puedes generar una contraseña para la tecnología NFC de los amibos y el purificador de aire Xiaomi. Cuando la tarjeta está cerca, Flipper Zero genera la contraseña a partir del UID de la tarjeta.

Para generar la contraseña y desbloquear la tarjeta haga lo siguiente:

1. Vaya al **Menú principal -> NFC -> Acciones adicionales -> Desbloquear NTAG/Ultralight**
2. Selecciona el tipo de tarjeta y luego sostén la tarjeta cerca de la parte posterior de tu Flipper Zero
3. Una vez desbloqueadas las páginas, presione **Guardar**
4. Nombra la tarjeta y luego presiona **Guardar**

## <mark style="color:orange;">Introducir la contraseña manualmente</mark> <a href="#id-6i8bg" id="id-6i8bg"></a>

Si conoce la contraseña, puede ingresarla manualmente y desbloquear la tarjeta haciendo lo siguiente:

1. ﻿[Lea y guarde](https://docs.flipperzero.one/nfc/read) la tarjeta.
2. Vaya al **Menú principal -> NFC -> Guardado** .
3. Seleccione la tarjeta guardada.
4. Luego vaya a **Desbloquear con contraseña -> Ingresar contraseña manualmente** .
5. Ingrese la contraseña en hexadecimal y luego presione **Guardar** .
6. Para desbloquear la tarjeta con la contraseña ingresada, sostenga la tarjeta cerca de la parte posterior de su Flipper Zero&#x20;
7. Una vez desbloqueadas las páginas, presione **Guardar** .
8. Nombra la tarjeta y luego presiona **Guardar** .
