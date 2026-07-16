
# qFlipper

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-mU-xci-ZON3mhTIBwe9Ta-20241025-132049.png?format=webp" alt=""><figcaption></figcaption></figure>

**qFlipper** es una aplicación de escritorio para actualizar el firmware y las bases de datos de Flipper Zero, administrar archivos en la tarjeta microSD y reparar firmware dañado. qFlipper está disponible en Windows, macOS y Linux.﻿

## <mark style="color:orange;">Instalación de qFlipper</mark> <a href="#xf0g4" id="xf0g4"></a>

Para instalar la aplicación qFlipper en su computadora, haga lo siguiente:

1. Descargue el archivo de instalación de qFlipper para su sistema operativo.

{% embed url="<https://flipperzero.one/downloads>" %}

2. Ejecute el archivo descargado y siga las instrucciones para su sistema operativo.

<figure><img src="/files/NB5YMszl6yuXoeEcqCrV" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">qFlipper: descripción general</mark> <a href="#xinqx" id="xinqx"></a>

Después de haber instalado la aplicación qFlipper en su computadora, **conecte su Flipper Zero (con una tarjeta microSD insertada) a su computadora mediante un cable USB** .

En la pestaña **Información del dispositivo** , puede ver la información principal sobre el hardware de Flipper Zero y el firmware instalado, [actualizar el dispositivo](https://docs.flipper.net/qflipper#ORL5Q) y [controlarlo de forma remota](https://docs.flipper.net/qflipper#Yag86) .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/Tb0rOpzudusehbt6n32Wx_monosnap-miro-2023-11-29-16-25-49.jpg?format=webp" alt=""><figcaption></figcaption></figure>

La pestaña de información del dispositivo ofrece una descripción general de las características principales﻿

En la pestaña **Control avanzado** , puede realizar copias de seguridad, restaurar y restablecer su Flipper Zero, así como elegir el firmware que desea instalar en el dispositivo. De manera similar a la pestaña Información del dispositivo, puede controlar su Flipper Zero e iniciar el procedimiento de actualización. Consulte [Reparación de almacenamiento interno](https://docs.flipperzero.one/basics/firmware-update/storage-repair) para obtener más información sobre los procedimientos de copia de seguridad y restauración.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/-uBB7wv13CSyWOhX6_t-0_monosnap-miro-2023-11-29-16-26-48.jpg?format=webp" alt=""><figcaption></figcaption></figure>

La pestaña de controles avanzados le brinda acceso a funciones de actualización, borrado y restauración.﻿

En la pestaña **Administrador de archivos** , puedes eliminar, cambiar el nombre y cargar archivos en Flipper Zero. Puedes navegar fácilmente por los archivos con las teclas de flecha del teclado.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/bniUEuWxZLKXo_fTds6wQ_image.png?format=webp" alt=""><figcaption></figcaption></figure>

Puede administrar archivos de Flipper Zero en la aplicación qFlipper﻿

Para cargar archivos en la pestaña **Administrador de archivos** , arrastre y suelte los archivos en la carpeta deseada o haga clic derecho en la carpeta requerida y haga clic en **Cargar aquí** .

﻿Al cargar, los archivos con el mismo nombre se sobrescribirán sin previo aviso.﻿

Puede navegar fácilmente en la pestaña Administrador de archivos usando solo un teclado :

| **Comando**             | **Teclas en Windows y Linux** | **Teclas en macOS** |
| ----------------------- | ----------------------------- | ------------------- |
| Ingresar                | Enter                         | Enter               |
| Atrás                   | Retroceso                     | Retroceso           |
| Subir                   | Ctrl+L                        | Comando+L           |
| Descargar               | Ctrl+D                        | Comando+D           |
| Borrar                  | Borrar                        | Fn+Retroceso        |
| Eliminar inmediatamente | Mayús+Suprimir                | Mayús+Fn+Retroceso  |
| Nueva carpeta           | Ctrl+N                        | Comando+N           |
| Rebautizar              | Ctrl+E                        | Comando+E           |
| Actualizar vista        | Ctrl+G                        | Comando+G           |

## <mark style="color:orange;">Actualizar Flipper Zero a través de qFlipper</mark> <a href="#orl5q" id="orl5q"></a>

La aplicación qFlipper tiene tres canales de actualización de firmware:

* ﻿**DESARROLLO (Dev):** el desarrollo continuo consiste en crear constantemente una nueva versión del firmware con cada nueva confirmación, a menudo varias veces al día. Esta versión de desarrollo incluye todas las funciones más recientes, pero puede ser inestable, provocar el bloqueo o la corrupción de los datos o dejar de funcionar por completo.
* ﻿**RELEASE CANDIDATE (RC):** la versión enviada para pruebas de validación al departamento de control de calidad. Si se detectan errores durante la fase de prueba, se revisa la versión y se emite un nuevo candidato a la versión de lanzamiento. Una vez que el candidato a la versión de lanzamiento pasa todas las pruebas con éxito, se convierte en la versión de lanzamiento.
* ﻿**RESEALE:** la versión estable del firmware ha sido ampliamente probada para garantizar su confiabilidad y, por lo tanto, se recomienda para uso general.

Inserte una tarjeta microSD antes del procedimiento de actualizaciónPara actualizar el firmware correctamente, se debe insertar una tarjeta microSD en el Flipper Zero. Las bases de datos del Flipper Zero se almacenan en una tarjeta microSD. Para obtener más información, consulte [Configuración de la tarjeta microSD .](https://docs.flipperzero.one/basics/sd-card)﻿

Para actualizar su Flipper Zero a través de la aplicación qFlipper, haga lo siguiente:

1. Conecte su Flipper Zero a su computadora mediante un cable USB.
2. En su computadora, ejecute la aplicación **qFlipper** .
3. En la aplicación qFlipper, vaya a la pestaña **Controles avanzados .**
4. Haga clic en **Actualizar canal** y seleccione una versión de firmware de la lista desplegable ( **se recomienda Lanzamiento** ).
5. Haga clic en **Actualizar** para iniciar el proceso de actualización.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/tZ27yn5Kj3LI9fXR48O_F_monosnap-miro-2023-11-29-16-01-36.jpg?format=webp" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Controlar Flipper Zero a través de qFlipper</mark> <a href="#yag86" id="yag86"></a>

También puedes controlar tu Flipper Zero de forma remota a través de la aplicación qFlipper haciendo lo siguiente:

1. En la pestaña Información del dispositivo , haga clic en la imagen Flipper Zero.
2. Haga clic en los botones de la pantalla
3. Utilice el teclado para controlar su Flipper Zero de forma remota. Haga clic en ℹ️ para obtener más información sobre los controles del teclado.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/o-7OIQ_JDzXtTWS14--S8_monosnap-miro-2023-11-29-16-30-50.jpg?format=webp" alt=""><figcaption></figcaption></figure>

Además, puedes capturar capturas de pantalla desde tu dispositivo Flipper Zero y guardarlas directamente en tu computadora haciendo clic en el botón **SAVE SCREENSHOT**.
