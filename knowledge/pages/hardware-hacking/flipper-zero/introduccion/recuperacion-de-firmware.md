
# Recuperación de Firmware

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-Or4KP_Q3-DmCqKbi91kad-20241024-174139.png?format=webp" alt=""><figcaption></figcaption></figure>

En ocasiones, es posible que el Flipper Zero no se actualice correctamente, no muestre imágenes o no responda a las pulsaciones de botones. Estos problemas pueden deberse a una corrupción en el firmware del dispositivo.

## <mark style="color:orange;">Cómo reparar el firmware</mark> <a href="#y_p7b" id="y_p7b"></a>

Puede reparar el firmware dañado con la ayuda de [qFlipper](https://docs.flipperzero.one/qflipper) y el cargador de arranque USB Device Firmware Update (DFU) integrado . El cargador de arranque USB DFU le permite actualizar su Flipper Zero sin pasar por el sistema operativo del dispositivo, lo que minimiza el riesgo de errores durante el proceso de actualización.

Pero primero, intenta hacer lo siguiente:

* Reinicie su Flipper Zero presionando y manteniendo presionados los botones **IZQUIERDO** y **ATRÁS** durante 5 segundos.
* Cargue su dispositivo con el cable USB Tipo-C provisto durante varios minutos porque su Flipper Zero podría tener la batería completamente agotada.

Si su Flipper Zero aún no se actualiza correctamente, no muestra imágenes o no responde a las pulsaciones de botones , siga los pasos a continuación.

La reparación del firmware borra todos los datos del almacenamiento internoSe borrarán el nivel, la configuración y la información sobre los dispositivos emparejados del delfín. Se guardarán los datos de la tarjeta microSD.﻿﻿

## <mark style="color:orange;">Paso 1. Cambiar al modo de recuperación</mark> <a href="#wldo5" id="wldo5"></a>

Antes de comenzar el proceso de reparación con qFlipper, cambia tu Flipper Zero al modo de recuperación. Esto activará el cargador de arranque USB DFU integrado. Los pasos para cambiar tu dispositivo al modo de recuperación pueden ser diferentes y dependen del estado del dispositivo.

### <mark style="color:orange;">Si su dispositivo está operativo pero no se actualiza correctamente</mark> <a href="#id-2vus0" id="id-2vus0"></a>

Cambie su Flipper Zero al modo de recuperación haciendo lo siguiente:

1. Vaya al **Menú principal -> Configuración -> Energía**
2. Luego vaya a **Reiniciar -> Actualización de firmware**
3. Presione **DERECHA** para reiniciar.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/hPV85zL3QzZ-mK9jEq55p_flipper-zero-dfu-mode-firmware-upgrade.jpg?format=webp" alt=""><figcaption></figcaption></figure>

4. Conecte el Flipper Zero a su computadora mediante un cable USB. La computadora debería detectar el Flipper Zero como un dispositivo DFU.
5. [Proceda a la reparación del firmware a través de qFlipper.](https://docs.flipper.net/basics/firmware-update/firmware-recovery#dYF_V)﻿

Alternativamente, puede cambiar el dispositivo al modo de recuperación haciendo lo siguiente:

1. Mantenga presionados los botones **IZQUIERDO** y **ATRÁS durante 5 segundos** .
2. Suelte el botón **ATRÁS** , pero siga presionando el botón **IZQUIERDO** hasta que se encienda el LED azul.
3. Conecte el Flipper Zero a su computadora mediante un cable USB. La computadora debería detectar el Flipper Zero como un dispositivo DFU.
4. ﻿[Proceda a la reparación del firmware a través de qFlipper.](https://docs.flipper.net/basics/firmware-update/firmware-recovery#dYF_V)﻿

Para salir del modo de recuperación, mantenga presionados los botones %left% LEFT y %back% BACK .﻿﻿

### <mark style="color:orange;">Si su dispositivo no muestra ninguna imagen o no responde al presionar los botones</mark> <a href="#tsogv" id="tsogv"></a>

Si su Flipper Zero está bloqueado, cambie el dispositivo al modo de recuperación mediante un reinicio completo:

1. **Desconecte el cable USB de su Flipper Zero** si está conectado.
2. Mantenga presionados los botones **OK** y **BACK** durante 30 segundos. Es normal que su Flipper Zero no presente indicaciones en la pantalla.
3. Conecte el Flipper Zero a su computadora mediante un cable USB. La computadora debería detectar el Flipper Zero como un dispositivo DFU.
4. ﻿[Proceda a la reparación del firmware a través de qFlipper.](https://docs.flipper.net/basics/firmware-update/firmware-recovery#dYF_V)﻿

## <mark style="color:orange;">Comprobando la conexión</mark> <a href="#kuqtq" id="kuqtq"></a>

Puede comprobar si el dispositivo está conectado a su computadora como un dispositivo DFU haciendo lo siguiente:

### <mark style="color:orange;">Windows</mark>

1. Vaya al **Administrador de dispositivos**
2. Busque el dispositivo **DFU en modo FS** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/TbGugqseaSUdpVpJWTI2y_monosnap-miro-2023-05-12-20-15-38.png?format=webp" alt=""><figcaption></figcaption></figure>

Su Flipper Zero se ha conectado correctamente como dispositivo DFU﻿. El dispositivo Flipper Zero DFU no incluye un controlador para Windows. El controlador se instala automáticamente durante el proceso de instalación de la aplicación qFlipper.﻿

#### Si su Flipper Zero no se detecta como un dispositivo DFU <a href="#s6lwj" id="s6lwj"></a>

* Utilice un cable USB diferente.
* Si es posible, conecta tu Flipper Zero directamente a un puerto USB de la placa base de tu ordenador, evitando el uso de un adaptador o concentrador.
* Primero, retire la tarjeta microSD de su Flipper Zero, cargue el dispositivo durante una hora y luego intente conectarlo **sin** la tarjeta microSD insertada.

## <mark style="color:orange;">Paso 2. Reparación del firmware mediante qFlipper</mark> <a href="#dyf_v" id="dyf_v"></a>

Una vez que su Flipper Zero esté conectado a su computadora como un dispositivo DFU, qFlipper detectará automáticamente el dispositivo.

Para reparar el firmware:

1. Ejecute **qFlipper** en su pc.
2. En su pc, haga clic en el botón **Reparar** . qFlipper realizará una instalación completa del firmware. qFlipper detecta automáticamente su Flipper Zero como un dispositivo DFU﻿

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/tCyKLvjzNphiI6ABaD6p9_monosnap-miro-2023-11-29-16-16-25.jpg?format=webp" alt=""><figcaption></figcaption></figure>

### <mark style="color:orange;">Si qFlipper no puede reparar el firmware</mark> <a href="#n0qce" id="n0qce"></a>

* Asegúrese de que la aplicación qFlipper esté instalada correctamente en su computadora. Para obtener más detalles, consulte [Instalación de qFlipper](https://docs.flipper.net/qflipper#Xf0g4) .
* Reinicie su dispositivo presionando y manteniendo presionados los botones **IZQUIERDO** y **ATRÁS** con un cable USB desconectado, luego repita el proceso de reparación.
* Si qFlipper aún no logra reparar el firmware, realice un reinicio completo presionando y manteniendo presionado el botón **ATRÁS** durante 30 segundos con un cable USB desconectado, luego repita el proceso de reparación.
* Ejecute qFlipper como administrador.
* Si es posible, conecta tu Flipper Zero directamente a un puerto USB de la placa base de tu ordenador, evitando el uso de un adaptador o concentrador.
* Si tiene problemas en su computadora con Windows, visite [Solucionar problemas de controladores en Windows](https://docs.flipper.net/qflipper/windows-debug) .
