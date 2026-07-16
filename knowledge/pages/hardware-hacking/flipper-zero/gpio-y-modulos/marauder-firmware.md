
# Marauder Firmware

<figure><img src="/files/BLKnEiCX1Rn5VOuJyPT8" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Marauder</mark> <a href="#mifss" id="mifss"></a>

El firmware Marauder es un software personalizado diseñado para dispositivos de hardware especializados, como placas de desarrollo y microcontroladores, orientado a realizar pruebas de seguridad en redes inalámbricas. Este firmware permite a los usuarios explorar, analizar y, en algunos casos, explotar redes Wi-Fi y uso pruebas de penetración. Equipado con una interfaz fácil de usar, Marauder ofrece herramientas avanzadas para escanear redes, interceptar tráfico de datos y evaluar la seguridad de los puntos de acceso Wi-Fi.

### Flasheo de Wifi Dev Board

Una vez que tenemos [Momentum ](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/custom-firmwares.md)instalado, podemos flashear la Wifi Dev Board de manera super simple, evitando instalaciones más complejas como el Arduino IDE.

1. Vamos a `GPIO > ESP > ESP Flasher`

<figure><img src="/files/4yqKZiLwHY17nfyDrbuS" alt=""><figcaption></figcaption></figure>

2. Seleccionamos `Quick Flash > Flipper Wifi Devboard` (o la tarjeta wifi que estemos utilizando)

<figure><img src="/files/rXMxSTI0C23czKP1chdA" alt=""><figcaption></figcaption></figure>

3. Seleccionamos `Marauder` y empieza el proceso de flasheo.

<figure><img src="/files/mJOtlKfm8stA0uR4UZt7" alt=""><figcaption></figcaption></figure>

4. Esperamos a que termine y ya podemos usar todas las funcionalidades de Marauder con nuestro Flipper Zero.

En las próximas secciones profundizaremos en distintos ataques Wifi que podemos realizar con el Flipper Zero.
