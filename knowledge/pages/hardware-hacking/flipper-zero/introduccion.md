
# Introducción

## <mark style="color:orange;">Documentación oficial</mark>

Flipper Zero siempre se está actualizando constantemente, por lo que se recomienda revisar la documentación oficial:

{% embed url="<https://docs.flipper.net/>" %}

## <mark style="color:orange;">Encendido</mark> <a href="#qaygi" id="qaygi"></a>

Enciende el Flipper Zero presionando y manteniendo presionado el botón **ATRÁS** durante 3 segundos.

<figure><img src="/files/stJu1FKDOCURScF3WcTY" alt=""><figcaption></figcaption></figure>

Si su Flipper Zero no se enciende es posible que la batería de su Flipper Zero esté completamente agotada. Para encenderlo, simplemente conecte el cable de carga USB y el dispositivo se encenderá automáticamente.\
\
En caso de que su Flipper Zero no se encienda incluso después de cargarlo, intente mantener presionados los botones IZQUIERDO y ATRÁS durante 5 segundos. Si su Flipper Zero sigue sin encenderse, siga los pasos que se describen en [Recuperación de firmware](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/introduccion/recuperacion-de-firmware.md).&#x20;

## <mark style="color:orange;">Reinicio</mark>​ <a href="#repos" id="repos"></a>

Si su Flipper Zero se congela mientras está en uso, mantenga presionados los botones **IZQUIERDO** y **ATRÁS** durante 5 segundos para reiniciar el dispositivo.

<figure><img src="/files/onHBLY4NIpZ5l3cDysFY" alt=""><figcaption></figcaption></figure>

Si su Flipper Zero se congela, reinícielo. ﻿Flipper Zero se puede reiniciar en distintos modos, incluido el modo de recuperación. Para obtener más información sobre los tipos de reinicio, visita [Reiniciar](https://docs.flipperzero.one/basics/reboot) .﻿﻿

## <mark style="color:orange;">Insertar una tarjeta microSD</mark> <a href="#mmmzv" id="mmmzv"></a>

{% hint style="warning" %}
Se necesita una tarjeta microSD para utilizar el dispositivo. Flipper Zero no viene con una tarjeta microSD, por lo que deberás comprar una por separado.﻿
{% endhint %}

{% embed url="<https://amzn.to/409Biml>" %}

La tarjeta microSD almacena varios tipos de datos, como llaves, tarjetas, mandos a distancia, bases de datos y mucho más. Flipper Zero admite tarjetas microSD de hasta 256 GB, pero una **tarjeta microSD de 4 GB es suficiente** para almacenar todos los datos necesarios. Ten en cuenta que Flipper Zero puede tardar más en reconocer una tarjeta microSD con mayor capacidad de almacenamiento.

Para obtener más información, visita la página [de configuración de la tarjeta MicroSD](https://docs.flipper.net/basics/sd-card) .

Inserte la tarjeta microSD con los pines hacia arriba﻿. Utilice una tarjeta microSD de alta calidad.&#x20;

<figure><img src="/files/JWtxV09ec3yqcziixWSL" alt=""><figcaption></figcaption></figure>

Es importante utilizar tarjetas microSD de marca y de alta calidad, como SanDisk , Kingston u otras, para garantizar el rendimiento adecuado de su Flipper Zero. El uso de tarjetas microSD de baja calidad no solo puede generar un rendimiento deficiente, sino que también puede bloquear o incluso dañar su dispositivo .﻿

Si su Flipper Zero no reconoce la tarjeta, visite [la sección correspondiente de la página de configuración de la tarjeta MicroSD](https://docs.flipper.net/basics/sd-card#rtpsy) .

## <mark style="color:orange;">Actualizar el firmware</mark> <a href="#id-1jgx9" id="id-1jgx9"></a>

{% hint style="info" %}
Inserte una tarjeta microSD antes de actualizar su Flipper Zero. Asegúrate de tener una tarjeta microSD en tu Flipper Zero antes de actualizar el firmware: el dispositivo la necesita para almacenar sus bases de datos. Para obtener más información, visita [Configuración de la tarjeta microSD .](https://docs.flipperzero.one/basics/sd-card)﻿
{% endhint %}

El firmware de Flipper Zero se encuentra en desarrollo activo y cambia con frecuencia. Recomendamos actualizar el firmware de su Flipper Zero a la última versión de inmediato.

Puede actualizar su Flipper Zero a través de [la aplicación móvil Flipper](https://docs.flipperzero.one/mobile-app) o [qFlipper](https://docs.flipperzero.one/qflipper) :

Con **la aplicación móvil Flipper** , puedes actualizar tu Flipper Zero directamente desde tu teléfono a través de Bluetooth. La aplicación móvil Flipper está disponible para iOS y Android.

### <mark style="color:orange;">Conectar el teléfono a Flipper Zero</mark> <a href="#sr5pc" id="sr5pc"></a>

Una vez que hayas descargado la aplicación móvil Flipper, puedes conectar tu teléfono a tu Flipper Zero:

1. Activa el Bluetooth en tu teléfono.
2. Activa el Bluetooth en tu Flipper Zero:

* Vaya al **Menú principal -> Configuración -> Bluetooth**&#x20;
* Configure **Bluetooth** en **ON**&#x20;

3. En la aplicación móvil Flipper, toque **Conectar** .
4. En la siguiente pantalla , junto al nombre del Flipper Zero detectado, toque **Conectar** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/0JzD-I8wdGDMPv8UR4LzO_flipper-mobile-app-bluetooth-connection.jpg?format=webp" alt=""><figcaption></figcaption></figure>

En la aplicación móvil Flipper, **ingrese el código de emparejamiento** que se muestra en la pantalla de Flipper Zero.

6. Toque **Emparejar** para finalizar el emparejamiento.

### <mark style="color:orange;">Actualizar Flipper Zero a través de la app Flipper</mark> <a href="#qqlck" id="qqlck"></a>

Para actualizar su Flipper Zero a través de la aplicación móvil Flipper, haga lo siguiente:

1. En la pestaña Menú principal, toque el botón **Actualizar .**
2. Toque el botón **Actualizar** para confirmar la acción.

La actualización a través de la aplicación móvil Flipper puede tardar **hasta aproximadamente 10 minutos** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/g_O9PZs8DWKlWccjC0RoT_flipper-zero-first-firmware-update-via-mobile-app.png?format=webp" alt=""><figcaption></figcaption></figure>

Para obtener información adicional sobre los pasos de actualización del firmware, visita [Actualización de firmware](https://docs.flipperzero.one/basics/firmware-update) .

## <mark style="color:orange;">Personalizar las preferencias del sistema</mark> <a href="#lfly" id="lfly"></a>

Una vez que haya actualizado su Flipper Zero, podrá modificar la configuración del sistema, como cambiar al modo para zurdos, configurar las unidades de medida que prefiera y seleccionar el formato de fecha y hora. Para acceder a la configuración del sistema, vaya a **Menú principal -> Configuración -> Sistema** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/c7zpK-xwB1YF47FA71-CN_image.png?format=webp" alt=""><figcaption></figcaption></figure>

Para obtener más información, visita la página de [Configuración](https://docs.flipper.net/basics/settings) .

## <mark style="color:orange;">Carga de la batería</mark> <a href="#su3-p" id="su3-p"></a>

Para cargar el Flipper Zero, conecta el cable USB tipo C incluido al puerto de carga y a una fuente de alimentación. La carga completa del dispositivo demora aproximadamente dos horas.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/bZR0CHKhuteGNld5FEfcU_image.png?format=webp" alt=""><figcaption></figcaption></figure>

Para ver información sobre la batería, vaya a **Menú principal -> Setting -> Power -> Battery Info**

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/1Z0RIs0FR_F2tXru2XCEW_image.png?format=webp" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Apagar el Flipper</mark> <a href="#d3znc" id="d3znc"></a>

Para apagar su Flipper Zero, vaya a **Menú principal -> Configuración -> Energía -> Apagar** y confirme la acción presionando el botón **DERECHO** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/N-fvG-3_usdCDeHvfI4pg_flipper-zero-power-off-screen.png?format=webp" alt=""><figcaption></figcaption></figure>

No deje el dispositivo descargado durante mucho tiempo﻿. Evite dejar su Flipper Zero descargado durante períodos prolongados. Si planeas dejar el Flipper Zero apagado durante un período prolongado, te recomendamos cargar el dispositivo hasta aproximadamente el 50 % antes de apagarlo.&#x20;

{% hint style="warning" %}
Dejar el dispositivo descargado durante un período prolongado puede degradar la salud de la batería.﻿﻿
{% endhint %}

## <mark style="color:orange;">Modos de potencia</mark> <a href="#xxkj" id="xxkj"></a>

Flipper Zero tiene dos modos de funcionamiento: **Activo** y **Suspendido** . Cada modo consume energía de forma diferente.

### <mark style="color:orange;">Modo activo</mark> <a href="#qsyhr" id="qsyhr"></a>

Cuando Flipper Zero ejecuta una aplicación o se establece una conexión, el dispositivo entra en modo Activo, que consume hasta 30 mA con luz de fondo. Con un transceptor activo, el consumo de energía puede alcanzar los 400 mA, e incluso 2 A con un transceptor activo y un módulo externo conectado.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/DV35vBLrP0dxmWYZIZTFi_image.png?format=webp" alt=""><figcaption></figcaption></figure>

Ver el consumo de energía en tiempo real﻿Utilice una tarjeta microSD de alta calidad para una mayor duración de la bateríaCuando la luz de fondo de la pantalla está encendida, el consumo de corriente de Flipper Zero con una tarjeta microSD de marca original es de hasta 30 mA. Con una tarjeta microSD que no sea original, el consumo de corriente total puede alcanzar hasta 50 mA, lo que reduce la duración de la batería de su dispositivo.\
\
Si la batería de tu Flipper Zero se agota rápidamente, verifica el consumo actual: Menú principal -> Configuración -> Energía -> Información de la batería .﻿

### <mark style="color:orange;">Modo de suspensión</mark> <a href="#mlrev" id="mlrev"></a>

Cuando no hay aplicaciones en ejecución ni conexiones establecidas en su Flipper Zero, el dispositivo entra en modo de suspensión, que tiene un consumo de energía de alrededor de 1,5 mA.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/FSL6fuRBN-RqQTL1zubEy_image.png?format=webp" alt=""><figcaption></figcaption></figure>

En modo de suspensión, el dispositivo consume alrededor de 1,5 mA.﻿Para que el modo de suspensión funcione correctamente, el modo de depuración debe estar deshabilitado.Puede desactivar el modo de depuración yendo a Menú principal -> Configuración -> Sistema , seleccionando Depuración y configurándolo en APAGADO .﻿

Hay dos modos de suspensión disponibles para el Flipper Zero: **predeterminado** y **heredado** . El modo de suspensión predeterminado tiene un consumo de energía de alrededor de 1,5 mA, lo que da como resultado una mayor duración de la batería. Sin embargo, es posible que experimente fallas del dispositivo mientras usa este modo. El modo de suspensión heredado tiene un consumo de energía de 9 mA, lo que da como resultado una menor duración de la batería, pero también proporciona más estabilidad a su dispositivo.

Puede cambiar al modo de suspensión heredado en **Menú principal -> Configuración -> Sistema** y configurando **Método de suspensión** en **Heredado** .﻿

## <mark style="color:orange;">Consejos para maximizar el rendimiento de la batería</mark> <a href="#ydqex" id="ydqex"></a>

**La vida útil de la batería** es el tiempo que funciona el Flipper Zero antes de que sea necesario recargarlo. **La vida útil de la batería** es el tiempo que dura la batería hasta que es necesario reemplazarla.

### <mark style="color:orange;">Batería de larga duración</mark> <a href="#gnr4j" id="gnr4j"></a>

* Actualice a la última versión de firmware. -> [Actualice su Flipper Zero](https://docs.flipperzero.one/basics/firmware-update) periódicamente ya que optimizamos constantemente el firmware y agregamos nuevas funciones de ahorro de energía.
* Optimice su configuración. -> Puede ajustar parámetros en la aplicación [Configuración](https://docs.flipperzero.one/basics/settings) , como Bluetooth, pantalla y configuraciones del sistema.

### <mark style="color:orange;">Larga duración de la batería</mark> <a href="#qbnwr" id="qbnwr"></a>

* Evite las temperaturas ambientales extremas. -> Flipper Zero está diseñado para funcionar en un rango de temperatura de 0° a 40° C (32° a 104° F). Evite exponer su dispositivo a temperaturas ambientales fuera de este rango especificado.
* Guarde el dispositivo medio cargado cuando esté apagado durante períodos prolongados. -> Cargue su Flipper Zero hasta aproximadamente el 50 % antes de apagarlo durante un período prolongado.

﻿

## Características del sistema eléctrico <a href="#dtq6a" id="dtq6a"></a>

| **Parámetro**                                                                         | **Valor**  |
| ------------------------------------------------------------------------------------- | ---------- |
| Capacidad de la batería                                                               | 2100 mAh   |
| Duración de la batería                                                                | 1 mes      |
| Tiempo de carga                                                                       | 2 horas    |
| Conector de alimentación                                                              | USB tipo C |
| Voltaje y corriente de carga                                                          | 5 V, 1 A   |
| Voltaje de funcionamiento de la batería                                               | 3,3-4,2 V  |
| Voltaje del pin 1 (la energía se suministra directamente desde USB)                   | 5 voltios  |
| Corriente máxima de alimentación del cable USB, incluidos los dispositivos conectados | 3 A        |

﻿
