
# Lectura de llaves iButton

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-bLQmvodKHC_977LM0Riu--20241025-124101.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero le permite leer, guardar y emular cómodamente las llaves de control de acceso iButton con protocolos Dallas, Cyfral y Metakom. Además, puede modificar los identificadores únicos (UID) de las llaves guardadas.

Para obtener más información sobre las llaves iButton y la implementación de hardware de Flipper Zero, consulte [iButton](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/ibutton.md) .﻿﻿

## <mark style="color:orange;">Cómo leer llaves de iButton</mark> <a href="#y8m2c" id="y8m2c"></a>

Flipper Zero puede leer los siguientes tipos de llaves iButton y sus respectivos datos:

* **Dallas DS1990:** solo el UID (la clave no tiene memoria)
* **Dallas DS1992:** el UID y los datos en la memoria
* **Dallas DS1996:** el UID y los datos en memoria
* **Dallas DS1971:** el UID y los datos en la memoria
* **Dallas, claves no compatibles:** solo el UID
* **Metakom:** solo el UID (la clave no tiene memoria)
* **Cyfral:** solo el UID (la clave no tiene memoria)

Para leer y guardar los datos de una llave iButton con su Flipper Zero, haga lo siguiente:

1. Vaya al **Menú principal -> iButton -> Leer**
2. Conecte la llave a los pines **de datos** y **tierra** , como se muestra a continuación

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-fG-F2Y09x4EHsOjGTylOW-20241025-124131.png?format=webp" alt=""><figcaption></figcaption></figure>

3. Una vez finalizada la lectura, visualice los datos de la llave

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/czEIeCtoj7MCK43HYg5OT_flipper-zero-ibutton-key-read-screen.jpg?format=webp" alt=""><figcaption></figcaption></figure>

4. Para guardar la llave, vaya a **Más -> Guardar**
5. Nombra la llave y luego presiona **Guardar**

Ahora que ha guardado la llave, puede emularla, renombrarla, eliminarla, editarla y escribirla en un espacio en blanco o en una clave del mismo tipo.

### Si la lectura falló <a href="#lfy40" id="lfy40"></a>

* Es posible que la llave iButton no toque los pines correctamente. -> Asegúrese de conectar la llave como se muestra arriba.
* Es posible que la llave iButton utilice un protocolo no compatible.
* La llave iButton podría estar dañada.
* Si recibió un **error de CRC** al leer una llave Dallas. -> Lea la llave nuevamente e intente emularla. Si la emulación no es exitosa , el error no se puede solucionar . Para obtener más información, consulte la sección [Error de lectura de CRC](https://docs.flipper.net/ibutton/read#r-y31) a continuación.

## <mark style="color:orange;">Edición de llaves de iButton guardadas</mark> <a href="#xwybx" id="xwybx"></a>

Puede editar el UID de la llave guardada haciendo lo siguiente:

1. Vaya al **Menú principal -> iButton -> Guardado**
2. Seleccione la llave que desea editar y seleccione **Editar**
3. Introduzca el valor requerido en hexadecimal.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/sfGsfAUW-hdPi8qWYUr5__monosnap-miro-2023-08-11-19-36-54.jpg?format=webp" alt=""><figcaption></figcaption></figure>

4. Presione **Guardar** , luego ingrese un nuevo nombre para la llave y presione **Guardar** nuevamente.

También puedes crear una llave iButton virtual utilizando la función [Agregar manualmente](https://docs.flipper.net/ibutton/add-manually) .

## <mark style="color:orange;">Emulación de llaves iButton guardadas</mark> <a href="#elm2r" id="elm2r"></a>

Cuando tengas una llave guardada en tu Flipper Zero, podrás emularla siguiendo estos pasos:

1. Vaya al **Menú principal -> iButton -> Saved**
2. Seleccione la llave que desea emular.
3. Coloque su Flipper Zero contra el lector iButton, asegurándose de que los pines **de datos** y **de tierra** lo toquen como se muestra a continuación.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-flzTb0FY1WPy607o24jMF-20241025-124211.png?format=webp" alt=""><figcaption></figcaption></figure>

En ocasiones, el diseño del lector iButton puede afectar la conexión con los pines de Flipper Zero, lo que hace que no se lea la llave. En este caso, alinee el pin del borde (datos) con el centro del lector y el pin del medio (tierra) con el borde del lector, exactamente como se muestra arriba.﻿

### Si la emulación falló <a href="#mxvw6" id="mxvw6"></a>

* Es posible que los pines del Flipper Zero no toquen correctamente el lector. -> Asegúrese de conectar los pines del Flipper Zero al lector como se muestra arriba.
* El pin del medio (tierra) no puede alcanzar el borde del lector. -> Puedes usar cables para emular la llave iButton. Transfiere datos al lector con dos cables insertados en los pines GPIO de Flipper Zero:
  * Pin 17 del GPIO (datos)
  * Pin GPIO 8, 11 o 18 (tierra)

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/gSNsZ-ycXN-P84DlS0F-W_flipper-zero-gpio-pins-ibutton-key-emulation.jpg?format=webp" alt=""><figcaption></figcaption></figure>

También se pueden emular llaves iButton con ayuda de cables.﻿

* El lector está protegido contra la emulación. -> Flipper Zero no puede evitarlo.
* Si agregó la llave manualmente o la editó, es posible que haya ingresado un UID de llave incorrecto.

## <mark style="color:orange;">Error de lectura de CRC</mark> <a href="#r-y31" id="r-y31"></a>

Las claves Dallas tienen una estructura de llave UID que contiene 8 bytes, incluido el byte de código de familia y el byte de verificación de redundancia cíclica (CRC). El byte CRC ayuda a garantizar la integridad de los datos al detectar errores que pueden haberse producido durante la transferencia o el almacenamiento de datos.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/G_lXv4f7aNZgNF0acTzVP_dallas-ibutton-key-uid-structure-flipper-zero.jpg?format=webp" alt=""><figcaption><p>El UID de la llave de Dallas incluye código de familia, CRC y número de serie﻿</p></figcaption></figure>

Cada vez que se lee una llave iButton, Flipper Zero comprueba si el byte CRC es correcto calculándolo nuevamente. Si el byte CRC capturado no coincide con el calculado, se produce un error CRC, lo que indica que el UID está dañado.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/bh66EAhwqiVyJ8Q2Y_mD0_flipper-zero-ibutton-crc-error.jpg?format=webp" alt=""><figcaption><p>Flipper Zero mostrará el byte CRC correcto esperado﻿</p></figcaption></figure>
