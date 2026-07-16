
# Extracción de claves con MFKey32

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-LcbRRk6BTxstYEl2WJYmP-20241025-092032.png?format=webp" alt=""><figcaption></figcaption></figure>

Si no pudo leer todos los sectores de la tarjeta MIFARE Classic® con la función [Leer](https://docs.flipperzero.one/nfc/read) o los sectores que leyó no son suficientes para obtener acceso, intente usar la función **Extract MF Keys** . Esta función realiza el ataque MFKey32, que [explota las debilidades](https://www.cs.bham.ac.uk/~garciaf/publications/Dismantling.Mifare.pdf) en el algoritmo de cifrado [Crypto-1](https://en.wikipedia.org/wiki/Crypto-1) . MFKey32 es el nombre de una herramienta/algoritmo utilizado para recuperar las claves MIFARE Classic de los pares [de nonce](https://en.wikipedia.org/wiki/Cryptographic_nonce) Crypto-1 del lector . Funciona recuperando el estado inicial del [Registro de desplazamiento de retroalimentación lineal](https://en.wikipedia.org/wiki/Linear-feedback_shift_register) Crypto-1 , que contiene la clave.

## <mark style="color:orange;">Sectores en las tarjetas NFC</mark>

Lo primero vamos a entender cómo funcionan los bloques en las tarjetas NFC:

<table><thead><tr><th width="144">Sector</th><th width="267">Descripción</th><th width="193">Clave A</th><th>Clave B</th></tr></thead><tbody><tr><td><strong>Sector 0</strong></td><td>Contiene el <strong>Bloque de Fabricación</strong> y el <strong>UID</strong> (Identificador Único). No se puede modificar en la mayoría de las tarjetas.</td><td>Generalmente <code>FFFFFFFFFFFF</code> o <code>A0A1A2A3A4A5</code></td><td>No siempre accesible</td></tr><tr><td><strong>Sector 1-N</strong></td><td>Espacio de almacenamiento de datos, dividido en <strong>bloques de 16 bytes</strong> cada uno. Se utiliza para guardar información personalizada, como identificadores, saldos o datos cifrados.</td><td>Puede ser personalizada según el sistema</td><td>Puede ser personalizada según el sistema</td></tr><tr><td><strong>Último sector</strong></td><td>Contiene el <strong>trailer block</strong>, donde se almacenan las claves <strong>A</strong> y <strong>B</strong>, además de los bits de control de acceso. Se usa para definir permisos sobre los datos del sector.</td><td>Clave para leer y verificar datos</td><td>Clave para escribir y modificar permisos</td></tr></tbody></table>

* Cada **sector** de una tarjeta NFC MIFARE Classic generalmente tiene **4 bloques**.
* **Clave A** se usa para autenticación y lectura en algunos casos.
* **Clave B** puede permitir escritura o configuración de accesos.
* Para leer y escribir en sectores protegidos, se necesita conocer las **claves correctas**.
* Las herramientas como **mfoc** o **mfcuk** pueden usarse para recuperar claves en algunas tarjetas.

## <mark style="color:orange;">Si tenemos acceso a la tarjeta</mark> <a href="#lsm_n" id="lsm_n"></a>

La mejor forma de llevar a cabo el ataque MFKey32 es tener acceso a la tarjeta, incluso si no se han leído todos los sectores. Al obtener la clave del lector , se pueden leer más sectores de la tarjeta, lo que podría ser suficiente para abrir la puerta.

Para obtener las claves del lector y leer la tarjeta MIFARE Classic, haga lo siguiente:

1. ﻿[Lee y guarda la tarjeta](https://docs.flipperzero.one/nfc/read) con tu Flipper Zero.
2. Vaya a **Menú principal -> NFC -> Saved -> Nombre de la tarjeta guardada -> Extract MF KEys.** Flipper Zero emulará esta tarjeta para el ataque MFKey32.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/aRTJ3BCig7LCW4CH1YDNL_monosnap-miro-2023-08-03-19-50-38.jpg?format=webp" alt=""><figcaption><p>Tu Flipper Zero está listo para recolectar los nonces del lector﻿</p></figcaption></figure>

**Toque el lector** con su Flipper Zero, como se muestra a continuación. Cuando esté cerca del lector, su Flipper Zero recopilará los nonces del lector . Según el lector, es posible que deba tocar el lector con su Flipper Zero hasta 10 veces para simular varias autenticaciones de tarjetas. En la pantalla de Flipper Zero , la cantidad de pares de nonce recopilados debería aumentar con cada nuevo toque del lector. Si la cantidad de pares de nonce no aumenta , el lector no está intentando autenticar la tarjeta emulada por Flipper Zero.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-nh8jrj31z6hOnHThNEcw7-20241107-112652.png?format=webp" alt=""><figcaption><p>Para recolectar nonces, toque el lector con su Flipper Zero﻿</p></figcaption></figure>

Pulse **OK** para guardar los pares nonce recopilados en la tarjeta microSD. Una vez que se haya recopilado la cantidad necesaria de pares nonce, la pantalla mostrará un mensaje **de Finalizado** . Después de eso, puede pulsar el botón **OK** para ver los datos capturados, incluido el sector y la clave de donde se obtuvieron.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/sR4_86WJB_5haA4HoEwHc_mfkey32noncepairscollected.jpg?format=webp" alt=""><figcaption><p>Una vez que se hayan recolectado los nonces, puedes guardarlos en la tarjeta microSD﻿</p></figcaption></figure>

**Recuperar claves** de los nonces recopilados. Puedes hacerlo mediante: **Aplicación móvil Flipper**

1. En su teléfono, ejecute [la aplicación móvil Flipper](https://docs.flipperzero.one/mobile-app) y sincronícela con su Flipper Zero
2. Vaya a **Herramientas -> Mfkey32 (Detectar lector)**

### <mark style="color:orange;">**Flipper Lab**</mark>

1. Conecte su Flipper Zero a su computadora mediante un cable USB-C.
2. En su computadora, vaya a [lab.flipper.net](https://lab.flipper.net/)
3. Vaya a **herramientas NFC** y luego haga clic en el botón **GIVE ME THE KEYS**

{% embed url="<https://lab.flipper.net>" %}

<figure><img src="/files/I1w1au3bgK6S5t4v5GPq" alt=""><figcaption></figcaption></figure>

### <mark style="color:orange;">**Aplicación MFKey**</mark>

Para utilizar esta función, debe descargar la aplicación [MFKey a su Flipper Zero desde ](https://lab.flipper.net/apps/mfkey)[Aplicaciones .](https://docs.flipper.net/apps)﻿

Si no tienes acceso a un teléfono inteligente o una computadora, puedes recuperar las claves de los nonces recolectados usando únicamente tu Flipper Zero. Ten en cuenta que la recuperación de las claves demora varios minutos debido a la capacidad de procesamiento limitada del dispositivo.

1. En su Flipper Zero, vaya a **Menú principal -> Aplicaciones -> NFC**
2. Ejecute la aplicación **MFKey** y presione el botón **OK** .

Las claves recuperadas se mostrarán en la pantalla. Luego, se pueden agregar al **diccionario de usuario** . En algunos casos, las claves no se pueden recuperar de los nonces debido a que el lector no reconoce correctamente la emulación de Flipper Zero.

Una vez que se agregan nuevas claves al diccionario de usuario, **vuelva a leer la tarjeta** . La cantidad de claves encontradas y sectores leídos puede aumentar, lo que indica que se recopilaron los datos necesarios.

3. **Emule la tarjeta** y mantenga su Flipper Zero cerca del lector para obtener acceso.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-r7Ac9hzhZeg8dR59XFOv--20241107-112730.png?format=webp" alt=""><figcaption></figcaption></figure>

Mientras emula la tarjeta NFC, sostenga su Flipper Zero cerca del lector﻿Si la tarjeta emulada no abre la puerta, intente realizar los pasos 1 a 6 nuevamente en caso de que su lector lea varios sectores secuencialmente.\
\
Si, después de repetir los pasos 1 a 6, el número de claves y sectores de la tarjeta leídos por su Flipper Zero no aumenta, entonces el lector y la tarjeta no están en el mismo sistema o el lector no es vulnerable al ataque MFKey32.﻿﻿

## <mark style="color:orange;">Si no tenemos acceso a la tarjeta</mark> <a href="#dsjm" id="dsjm"></a>

Incluso si no tienes acceso a la tarjeta, puedes intentar obtener las claves del lector y luego agregarlas al **diccionario de usuario** para ampliarlo.

Para obtener y guardar las claves del lector , haga lo siguiente:

1. Vaya al **Menú principal -> NFC -> Extraer claves MF** . Flipper Zero emulará una tarjeta NFC para el ataque MFKey32.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/daUwKKVW4HBirdmwgk7tQ_monosnap-miro-2023-08-03-19-51-29.jpg?format=webp" alt=""><figcaption><p>Tu Flipper Zero está listo para recolectar los nonces del lector</p></figcaption></figure>

2. **Toque el lector** con su Flipper Zero como se muestra a continuación.&#x20;

Cuando esté cerca del lector, su Flipper Zero recopilará los nonces del lector . Según el lector, es posible que deba tocar el lector con su Flipper Zero hasta 10 veces para simular varias autenticaciones de tarjetas. En la pantalla de Flipper Zero , la cantidad de pares de nonce recopilados debería aumentar con cada nuevo toque del lector. Si la cantidad de pares de nonce no aumenta , el lector no está intentando autenticar la tarjeta emulada por Flipper Zero.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-nGTWC9NTOp_sNkrlmdgce-20241107-112752.png?format=webp" alt=""><figcaption><p>Para recolectar nonces, toque el lector con su Flipper Zero</p></figcaption></figure>

Pulse **OK** para guardar los pares nonce recopilados en la tarjeta microSD. Una vez que se haya recopilado la cantidad necesaria de pares nonce, la pantalla mostrará un mensaje **de Finalizado** . Después de eso, puede pulsar el botón **OK** para ver los datos capturados, incluido el sector y la clave de donde se obtuvieron.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/EE9Cqc28ze8WOSjyqvNkK_mfkey32noncepairscollected.jpg?format=webp" alt=""><figcaption><p>Una vez que se hayan recolectado los nonces, puedes guardarlos en la tarjeta microSD﻿</p></figcaption></figure>

### <mark style="color:orange;">**Recuperar claves**</mark> <mark style="color:orange;"></mark><mark style="color:orange;">de los nonces recopilados</mark>&#x20;

Puedes hacerlo mediante:&#x20;

#### **Aplicación móvil Flipper**

1. En su teléfono, ejecute [la aplicación móvil Flipper](https://docs.flipperzero.one/mobile-app) y sincronícela con su Flipper Zero
2. Vaya a **Herramientas -> Mfkey32 (Detectar lector)**

#### **Flipper Lab**

1. Conecte su Flipper Zero a su computadora mediante un cable USB-C
2. En su computadora, vaya a [lab.flipper.net](https://lab.flipper.net/)
3. Vaya a **herramientas NFC** y luego haga clic en el botón **GIVE ME THE KEYS**

#### **Aplicación MFKey**

Para utilizar esta función, debe descargar la aplicación [MFKey a su Flipper Zero desde ](https://lab.flipper.net/apps/mfkey)[Aplicaciones .](https://docs.flipper.net/apps)﻿

Si no tienes acceso a un teléfono inteligente o una computadora, puedes recuperar las claves de los nonces recolectados usando únicamente tu Flipper Zero. Ten en cuenta que la recuperación de las claves demora varios minutos debido a la capacidad de procesamiento limitada del dispositivo.

1. En su Flipper Zero, vaya a **Menú principal -> Aplicaciones -> NFC**
2. Ejecute la aplicación **MFKey** y presione el botón **OK** .

Las claves recuperadas y los números de sector se mostrarán en la pantalla. Luego, se pueden agregar al **diccionario de usuario** . En algunos casos, las claves no se pueden recuperar de los nonces porque el lector no reconoce correctamente la emulación Flipper Zero.
