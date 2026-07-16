
# Lectura de tarjetas RFID

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-N5Zy447XyN9b94MuBkft2-20241024-181130.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero le permite leer, guardar y emular tarjetas RFID de 125 kHz. Una tarjeta RFID de 125 kHz es un [transpondedor](https://en.wikipedia.org/wiki/Transponder) que almacena un número de identificación único. Cuando se escanea con un lector, una tarjeta de 125 kHz transmite su número de identificación. Si la tarjeta tiene el protocolo compatible, Flipper Zero puede leer y guardar el número de identificación.﻿

{% hint style="info" %}
Un ejemplo de estas tarjetas sería la pulsera para acceder a un gimnasio, una tarjeta para abrir la habitación de un hotel, o un chip de un perro.
{% endhint %}

## <mark style="color:orange;">Protocolos soportados</mark> <a href="#vkado" id="vkado"></a>

Flipper Zero puede leer tarjetas RFID de 125 kHz con los siguientes protocolos:

<table data-header-hidden><thead><tr><th width="234"></th><th></th></tr></thead><tbody><tr><td><strong>Protocolo</strong></td><td><strong>Descripción</strong></td></tr><tr><td><strong>EM-Micro EM4100</strong></td><td>Protocolo de 125 kHz ampliamente utilizado en aplicaciones de control de acceso básicas.</td></tr><tr><td><strong>EM-Micro EM4100/32</strong></td><td>Variante del EM4100 con un formato de 32 bits, compatible con sistemas de baja frecuencia (125 kHz).</td></tr><tr><td><strong>EM-Micro EM4100/16</strong></td><td>Variante del EM4100 con un formato de 16 bits, usado en sistemas de control de acceso simples.</td></tr><tr><td><strong>HID H10301</strong></td><td>Estándar de 26 bits utilizado por HID Global para control de acceso en entornos comerciales.</td></tr><tr><td><strong>IDTECK Idteck</strong></td><td>Protocolo de 26 bits utilizado por sistemas IDTECK para control de acceso y autenticación.</td></tr><tr><td><strong>Motorola Indala 26</strong></td><td>Tecnología de 125 kHz que utiliza un formato de 26 bits para control de acceso corporativo.</td></tr><tr><td><strong>Kantech IoProx XSF</strong></td><td>Protocolo exclusivo de Kantech para sus sistemas de control de acceso con seguridad adicional.</td></tr><tr><td><strong>AWID</strong></td><td>Tecnología de 125 kHz empleada en control de acceso, sistemas de estacionamiento y aplicaciones empresariales.</td></tr><tr><td><strong>FECAVA FDX-A</strong></td><td>Protocolo de identificación de 134.2 kHz utilizado principalmente en sistemas de identificación animal.</td></tr><tr><td><strong>ISO FDX-B</strong></td><td>Estándar internacional de 134.2 kHz para identificación de animales, regulado por la norma ISO 11784/85.</td></tr><tr><td><strong>Generic HID Prox</strong></td><td>Tecnología de 125 kHz usada en múltiples sistemas de control de acceso genéricos.</td></tr><tr><td><strong>Generic HID Ext</strong></td><td>Variante extendida de HID Prox con mayor capacidad de datos y compatibilidad con sistemas avanzados.</td></tr><tr><td><strong>Farpointe Pyramid</strong></td><td>Tecnología RFID de baja frecuencia (125 kHz) utilizada en sistemas de control de acceso.</td></tr><tr><td><strong>Viking</strong></td><td>Protocolo RFID utilizado en sistemas de seguridad y control de acceso específicos de Viking.</td></tr><tr><td><strong>Jablotron</strong></td><td>Protocolo exclusivo utilizado en sistemas de seguridad y alarmas fabricados por Jablotron.</td></tr><tr><td><strong>Paradox</strong></td><td>Tecnología propia de Paradox para integración con sus sistemas de control de acceso y seguridad.</td></tr><tr><td><strong>PAC Stanley</strong></td><td>Protocolo RFID de 125 kHz desarrollado para sistemas de acceso de alta seguridad.</td></tr><tr><td><strong>Keri</strong></td><td>Protocolo RFID utilizado en sistemas de control de acceso de la marca Keri Systems.</td></tr><tr><td><strong>Gallagher</strong></td><td>Tecnología avanzada utilizada en soluciones de seguridad física y control de acceso.</td></tr><tr><td><strong>Honeywell Nexwatch</strong></td><td>Protocolo utilizado en sistemas de seguridad y control de acceso de Honeywell.</td></tr><tr><td><strong>Electra</strong></td><td>Protocolo utilizado en soluciones de acceso y control para aplicaciones residenciales y comerciales.</td></tr><tr><td><strong>Securakey</strong></td><td>Tecnología RFID usada en sistemas de control de acceso, con opciones de baja y alta frecuencia.</td></tr></tbody></table>

## Cómo leer tarjetas de 125 kHz <a href="#n6-dm" id="n6-dm"></a>

Para leer y guardar los datos de la tarjeta de 125 kHz , haga lo siguiente:

1. Vaya al **Menú principal -> RFID 125 kHz** .
2. Presiona **Leer** , luego sostén la tarjeta cerca de la parte posterior de tu Flipper Zero .

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-ZSvJK21YCuGtFAnFsyf5x-20241024-181249.png?format=webp" alt=""><figcaption></figcaption></figure>

No mueva la tarjeta mientras lee. El proceso de lectura puede tardar varios segundos porque Flipper Zero cambia las codificaciones cada 3 segundos e intenta hacer coincidir el protocolo de la tarjeta con la lista de protocolos compatibles.﻿

Durante la lectura, Flipper Zero cambia entre las codificaciones ASK y PSK cada tres segundos para leer datos de la tarjeta RFID de 125 kHz.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/vmurU-epvnvogwFJ7nv9u_monosnap-miro-2023-09-12-14-53-25.jpg?format=webp" alt=""><figcaption></figcaption></figure>

3. Una vez finalizada la lectura, revise los datos de la tarjeta que se muestran en la pantalla.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/1PesPJ3jO3z7DsVZS-Tyl_monosnap-miro-2023-09-12-14-54-23.jpg?format=webp" alt=""><figcaption></figcaption></figure>

4. Para guardar la tarjeta, vaya a **Más -> Guardar** .
5. Nombra la tarjeta y luego presiona **Guardar** .

### <mark style="color:orange;">Si la lectura falló</mark> <a href="#id-6iwpi" id="id-6iwpi"></a>

* Es posible que la tarjeta utilice tecnología NFC -> Lea la tarjeta con la [aplicación NFC](https://docs.flipperzero.one/nfc).
* Flipper Zero cambia de codificación cada tres segundos. Es posible que no se puedan leer algunas tarjetas porque puede llevar hasta 10 segundos leer los datos. -> [Lee la tarjeta con la codificación ASK o PSK preseleccionada](https://docs.flipperzero.one/rfid/read#A28I4).

### <mark style="color:orange;">Lectura con una codificación preseleccionada</mark> <a href="#a28i4" id="a28i4"></a>

Flipper Zero permite leer tarjetas RFID de 125 kHz con la codificación ASK o PSK preseleccionada.

Para leer y guardar los datos de la tarjeta de 125 kHz con una codificación preseleccionada, haga lo siguiente:

1. Vaya al **Menú principal -> RFID 125 kHz -> Acciones adicionales** .
2. Seleccione **Leer ASK** o **Leer PSK** .
3. Sostenga la tarjeta cerca de la parte posterior de su Flipper Zero .
4. Después de leer, vaya a **Más -> Guardar** .
5. Nombra la tarjeta y luego presiona **Guardar** .

## <mark style="color:orange;">Emulación de tarjetas RFID de 125 kHz</mark> <a href="#id-5mrws" id="id-5mrws"></a>

Flipper Zero puede emular tarjetas RFID de 125 kHz guardadas haciendo lo siguiente:

1. Vaya al **Menú principal -> RFID 125 kHz -> Guardado** .
2. Seleccione la tarjeta que desea emular y luego presione **Emular** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/rHlSYiV_1dnfnfuP1A-Tc_monosnap-miro-2023-09-12-14-49-16.jpg?format=webp" alt=""><figcaption></figcaption></figure>

Mantenga su Flipper Zero cerca del lector, con la parte posterior del dispositivo orientada hacia el lector.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-WifMsOzPepWbdVsq7O4u0-20241107-102717.png?format=webp" alt=""><figcaption></figcaption></figure>
