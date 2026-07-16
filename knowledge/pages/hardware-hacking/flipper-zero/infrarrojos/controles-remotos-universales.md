
# Controles remotos universales

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-7lRVz9RMrd7l0oVMsxuw3-20241025-105816.png?format=webp" alt=""><figcaption></figcaption></figure>

Flipper Zero te permite controlar varios dispositivos sin copiar sus controles remotos infrarrojos (IR) originales. Con la ayuda de la función de **controles remotos universales** , puedes usar tu Flipper Zero como un control remoto IR universal para enviar comandos a televisores, sistemas de sonido, proyectores y aires acondicionados. Esta función envía comandos desde el diccionario integrado de protocolos de control remoto IR. Las principales marcas de productos electrónicos utilizan esos protocolos para controlar sus dispositivos con controles remotos IR.

## <mark style="color:orange;">Controles remotos universales</mark> <a href="#udh5x" id="udh5x"></a>

Flipper Zero tiene controles remotos universales integrados, como un control remoto de TV, un control remoto de sistema de audio, un control remoto de proyector y un control remoto de aire acondicionado. Se puede acceder a los controles remotos universales yendo a **Menú principal -> Infrarrojos -> Controles remotos universales** .

### <mark style="color:orange;">Control remoto de TV</mark> <a href="#cjlzi" id="cjlzi"></a>

El control remoto universal del televisor le permite controlar la energía, configurar el volumen del sonido, cambiar canales y silenciar su televisor.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/TWhQbZ4YgMd1XE9JCrPhY_tvmonosnap-miro-2023-09-11-14-10-31.jpg?format=webp" alt=""><figcaption><p>Controla tu TV incluso sin el control remoto IR original﻿</p></figcaption></figure>

### <mark style="color:orange;">Control remoto del sistema de audio</mark> <a href="#yymbq" id="yymbq"></a>

El control remoto del sistema de audio le permite controlar la energía, reproducir y pausar canciones, cambiar canciones, configurar el volumen del sonido y silenciar su sistema de audio.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/X2a59PjsU8rvpuIL07C6O_audiomonosnap-miro-2023-09-11-14-11-16.jpg?format=webp" alt=""><figcaption><p>Utilice su Flipper Zero para controlar su sistema de audio﻿</p></figcaption></figure>

### <mark style="color:orange;">Control remoto del proyector</mark> <a href="#d2bso" id="d2bso"></a>

El control remoto universal del proyector le permite controlar la energía, configurar el volumen del sonido y silenciar el proyector.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/vqIz4OFvZ3YT9ybmOutXT_monosnap-miro-2023-09-15-17-08-14.jpg?format=webp" alt=""><figcaption><p>Envíe comandos a su proyector con el control remoto del proyector﻿</p></figcaption></figure>

### <mark style="color:orange;">Control remoto del aire acondicionado</mark> <a href="#uhfjd" id="uhfjd"></a>

El control remoto universal del aire acondicionado le permite controlar la potencia, activar un modo deshumidificador de aire y configurar la temperatura en los modos de enfriamiento o calefacción. Tenga en cuenta que el botón **OFF** solo apaga el aire acondicionado. Para encender el aire acondicionado, presione cualquier otro botón del control remoto universal del aire acondicionado.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/xg4P9s1Klin_5dj0nDzp0_airmonosnap-miro-2023-09-11-14-13-41.jpg?format=webp" alt=""><figcaption><p>Tome el control de su aire acondicionado sin el control remoto IR original﻿﻿</p></figcaption></figure>

## <mark style="color:orange;">Enviando comandos</mark> <a href="#sndh6" id="sndh6"></a>

Al enviar comandos, Flipper Zero emula un diccionario completo de protocolos utilizados por los controles remotos IR. Cuando el protocolo enviado por su Flipper Zero coincide con el protocolo utilizado por el dispositivo que desea controlar, el dispositivo ejecuta el comando.

Para enviar un comando, haga lo siguiente:

1. Vaya al **Menú principal -> Infrarrojos -> Controles remotos universales** .
2. Seleccione el control remoto universal según el dispositivo que desee controlar.
3. Seleccione el botón/comando que desea enviar.
4. Apunta tu Flipper Zero hacia el dispositivo y presiona el botón **OK** — tu Flipper Zero comienza a enviar el comando usando protocolos del diccionario.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-8B4S0ALKVJBUAqD5N-RQf-20241025-105844.png?format=webp" alt=""><figcaption><p>Apunta tu Flipper Zero hacia el televisor, envía el comando y espera hasta que el televisor ejecute el comando.</p></figcaption></figure>

Continúe apuntando su Flipper Zero hacia el dispositivo hasta que este ejecute el comando o hasta que se reproduzca todo el diccionario.

Tenga en cuenta que puede llevar hasta dos minutos emular el diccionario completo de controles remotos IR compatibles.﻿Envío del comando utilizando protocolos del diccionario﻿

#### Si la ejecución del comando falló <a href="#jlu-x" id="jlu-x"></a>

* El protocolo de su control remoto original no está en el diccionario Flipper Zero. -> Si tiene acceso al control remoto original, intente [leer](https://docs.flipperzero.one/infrared/read) comandos desde él o agregar comandos al diccionario de controles remotos universales.
