
# GPIO y Módulos

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-fptSNCh8iwnphSh__G9QE-20241025-123350.png?format=webp" alt=""><figcaption></figcaption></figure>

Puede utilizar Flipper Zero para explorar hardware, actualizar firmware, depurar y realizar pruebas de fuzzing. Flipper Zero se puede conectar al hardware mediante sus pines GPIO integrados, controlar el hardware con botones, ejecutar su código y mostrar mensajes de depuración en la pantalla. Flipper Zero también se puede utilizar como un convertidor USB a UART/SPI/I2C.

Inserte una tarjeta microSD para usar la aplicación GPIOAntes de usar la aplicación GPIO, asegúrese de actualizar el firmware de Flipper Zero con una tarjeta microSD insertada, ya que Flipper Zero almacena bases de datos en una tarjeta microSD. Para obtener más información sobre el proceso de actualización, visite la página [de actualización de firmware .](https://docs.flipperzero.one/basics/firmware-update)﻿

## <mark style="color:orange;">Distribución de pines GPIO</mark> <a href="#mifss" id="mifss"></a>

Flipper Zero tiene 18 pines en la parte superior, que consisten en pines de fuente de alimentación y pines de E/S. **Los pines de fuente de alimentación** se pueden utilizar para alimentar los módulos externos. Los **pines de entrada/salida (E/S)** son tolerantes a +3,3 V para entrada y salida. Para obtener más información, consulte [Tolerancia a 3,3 V y 5 V.](https://docs.flipperzero.one/gpio-and-modules#svyi9)

Los pines de E/S conectan módulos externos a los pines de E/S del microcontrolador [STM32WB55](https://www.st.com/resource/en/datasheet/stm32wb55rg.pdf) a través de resistencias de 51 ohmios. Todos los pines están protegidos contra descargas electrostáticas (ESD). Para obtener información sobre la funcionalidad básica de los pines de Flipper Zero, consulte la siguiente imagen.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/rDj495vJHGg8Ae5H_4vdo_image.png?format=webp" alt=""><figcaption><p>Pines de Flipper Zero﻿</p></figcaption></figure>

En la siguiente imagen se puede encontrar información detallada sobre la distribución de pines y la funcionalidad de los pines.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/zRucuAM1fjos-_rn5VdBb_flipperzeropinout.jpg?format=webp" alt=""><figcaption><p>Distribución de pines GPIO de Flipper Zero</p></figcaption></figure>

### <mark style="color:orange;">Alimentación de +3,3 V (pin 9)</mark> <a href="#id-44hrq" id="id-44hrq"></a>

* La salida está habilitada de forma predeterminada.
* La carga máxima es 1,2 A.
* La tarjeta microSD de Flipper Zero se alimenta a +3,3 V. Durante las actualizaciones de firmware y el montaje de la tarjeta microSD, la fuente de alimentación al pin 9 se desactiva temporalmente.

{% hint style="danger" %}
Conecte módulos externos con una gran carga capacitiva solo cuando Flipper Zero esté **apagado**. De lo contrario, los datos de la tarjeta microSD pueden corromperse.﻿
{% endhint %}

### <mark style="color:orange;">Alimentación de +5 V (pin 1)</mark> <a href="#brgpy" id="brgpy"></a>

El pin 1 puede recibir alimentación mediante la batería incorporada o un cable USB.

Cuando Flipper Zero está conectado a un cable USB, la alimentación al pin 1 se suministra directamente desde el USB. Nunca exceda la corriente máxima de 1,2 A.﻿

Cuando Flipper Zero funciona con la batería incorporada:

* La salida no está habilitada de manera predeterminada. Para habilitar la alimentación al pin 1, haga lo siguiente: 1. En el **menú principal** , vaya a **GPIO** . 2. Seleccione **5 V en GPIO** y configúrelo en **ON** .
* La carga máxima es 1,2 A.

### <mark style="color:orange;">Pines de entrada/salida</mark> <a href="#a02ys" id="a02ys"></a>

El consumo total de energía de los pines de E/S no debe superar los 5 W. De lo contrario, la batería podría pasar al modo de protección y Flipper Zero podría apagarse. Cada pin puede suministrar hasta 20 mA.

### <mark style="color:orange;">Tolerancia de 3,3 V y 5 V</mark> <a href="#svyi9" id="svyi9"></a>

La interfaz de E/S de los chips CMOS modernos está diseñada para funcionar en un rango de voltaje específico. En el caso del microcontrolador STM32WB55 de Flipper Zero, la interfaz de E/S está diseñada para funcionar con un voltaje de 3,3 V.

Evita conectar 5 periféricos VI/O a su Flipper Zero para evitar posibles daños. La única excepción es cuando un pin GPIO específico está configurado para entrada, entonces se vuelve tolerante a 5 V. Cuando el pin GPIO está configurado para salida, ya no es tolerante a 5 V.﻿

Para obtener más información, consulte [la nota de aplicación AN4899](https://www.st.com/resource/en/application_note/dm00315319-stm32-gpio-configuration-for-hardware-settings-and-lowpower-consumption-stmicroelectronics.pdf) .

## <mark style="color:orange;">Menú GPIO</mark> <a href="#fodlk" id="fodlk"></a>

Puede acceder a la aplicación GPIO desde el menú principal. En la aplicación, puede configurar la funcionalidad USB-UART, probar pines por separado y habilitar o deshabilitar la fuente de alimentación de +5 V al pin 1.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/SnlXP2zIsJppwcA-JvIlx_monosnap-miro-2023-10-16-12-16-56.jpg?format=webp" alt=""><figcaption><p>Menú de la aplicación GPIO﻿</p></figcaption></figure>

* **USB-UART Bridge:** Flipper Zero actúa como un convertidor USB a UART serie.
* **Control manual de GPIO:** prueba la salida de pines GPIO individuales o de todos ellos presionando **OK** . Opciones de configuración disponibles: PA7 (pin 2), PA6 (pin 3), PA4 (pin 4), PB3 (pin 5), PB2 (pin 6), PC3 (pin 7), PC1 (pin 15), PC0 (pin 16) y ALL.
* **5V en GPIO:** habilita/deshabilita la fuente de alimentación de +5 V al pin 1. Consulte [esta sección](https://docs.flipperzero.one/gpio-and-modules#brgPY) para obtener más información.

## <mark style="color:orange;">Inserción de un módulo externo</mark> <a href="#xl_gx" id="xl_gx"></a>

Es importante insertar el módulo externo en los orificios de los pines GPIO de su Flipper Zero correctamente. Si su **Flipper Zero no está en una funda de silicona** , inserte el módulo hasta el fondo, de modo que no haya espacio entre su Flipper Zero y el módulo. Es posible que deba aplicar más fuerza para insertarlo por completo .

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-oXtUpGPwNmFQHfVSIlrFl-20241025-123418.png?format=webp" alt=""><figcaption><p>Asegúrese de que los pines GPIO del módulo no estén visibles﻿</p></figcaption></figure>

Si su **Flipper Zero está en una funda de silicona** , inserte el módulo completamente, de modo que no quede ningún espacio en el medio entre la funda de silicona y el módulo .

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-ZY7H2H4NQkCYRWeaoYVGE-20241025-123757.png?format=webp" alt=""><figcaption><p>Asegúrese de que no haya ningún espacio en el medio.</p></figcaption></figure>
