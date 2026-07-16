
# Análisis de Android

Tras entrevistar a testigos y al círculo íntimo de la víctima, tu objetivo es analizar minuciosamente la información recopilada y rastrear diligentemente las pruebas para reconstruir la secuencia de eventos que condujeron al incidente.

{% embed url="<https://cyberdefenders.org/blueteam-ctf-challenges/the-crime/>" %}

## <mark style="color:purple;">Descarga de la evidencia</mark>

Nos descargamos los archivos en Kali Linux y los extraemos. Tendremos un volcado completo del móvil Android del fallecido, con multitud de carpetas que contienen multitud de archivos:

```bash
cd data

ls

adb  app-asec       app-private  cache  local       mediadrm  misc_de     ota          resource-cache  system_ce   user     vendor_ce
anr  app-ephemeral  backup       data   lost+found  misc      nativetest  ota_package  ss              system_de   user_de  vendor_de
app  app-lib        bootchart    drm    media       misc_ce   nfc         property     system          tombstones  vendor   
```

***

## <mark style="color:purple;">Herramientas</mark>

Para este laboratorio usaremos ALEAPP (Android Logs Events And Protobuf Parser). Es una herramienta forense diseñada para analizar y extraer datos de dispositivos Android. Desarrollada por Alexis Brignoni, esta herramienta permite a los investigadores forenses obtener información clave de un dispositivo Android, procesando diversos tipos de archivos y generando informes comprehensivos sobre la actividad del dispositivo, las aplicaciones instaladas, y datos almacenados. Esta utilidad es particularmente valiosa para el análisis de dispositivos en investigaciones criminales y civiles, ya que facilita el acceso a evidencia digital que podría ser crucial para un caso.

{% embed url="<https://github.com/abrignoni/ALEAPP>" %}

#### Instalación

```bash
git clone https://github.com/abrignoni/ALEAPP.git
cd ALEAPP
pip3 install -r requirements.txt

python3 aleappGUI.py
```

***

## <mark style="color:purple;">Pregunta 1</mark>

> Según los testimonios de los testigos y personas cercanas a la víctima, se ha evidenciado que esta tenía interés en el trading. Esto lo llevó a invertir todo su dinero y a endeudarse. ¿Puede identificar el hash `SHA256` de la aplicación de trading que la víctima usaba principalmente en su teléfono?

Usaremos ALEAPP desde Kali Linux para analizar los datos del móvil Android de la víctima:

```bash
python3 aleappGUI.py
```

Se abre la GUI donde seleccionaremos la carpeta principal con los datos y la carpeta de Output:

<figure><img src="/files/pGuhXYCNjvnsT8MKAuOb" alt=""><figcaption></figcaption></figure>

Le damos a `Process` y empieza a analizar toda la información. Al terminar nos genera un informe HTML navegable

#### Informe HTML

<figure><img src="/files/ahqQDNfucJDFzErTVJFE" alt=""><figcaption></figcaption></figure>

En la pestaña Installed Apps encontramos la aplicación de trading que utilizaba y el sha256 asociado:

<figure><img src="/files/vEvWomjlAmgypvPgDhDR" alt=""><figcaption></figcaption></figure>

Al parecer utilizaba OlympTrade como plataforma principal de trading :

{% embed url="<https://olymptrade.com/>" %}

***

## <mark style="color:purple;">Pregunta 2</mark>

> Según el testimonio del mejor amigo de la víctima, dijo: " `Mientras estábamos juntos, mi amigo recibió varias llamadas que evitó. Dijo que le debía mucho dinero a quien lo llamó, pero que ya no podía pagar`". ¿Cuánto le debe la víctima a esta persona?

Si vamos a la pestaña Call logs encontramos multitud de llamadas del mismo número de teléfono:

<figure><img src="/files/gvqhDVOuAmExkCNDhTiT" alt=""><figcaption></figcaption></figure>

En la pestaña de SMS encontramos el mensaje con la suma de dinero que le debía:

<figure><img src="/files/obuavyVTevVCZEcGNmdn" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Pregunta 3</mark>

> ¿Cuál es el nombre de la persona a quien la víctima le debe dinero?

En la imagen anterior vemos el número de teléfono de la persona a la que debe dinero la víctima. Si nos vamos a la pestaña `Contacts`, vemos que ese número pertenece a un tal `Shady Wahab`:

<figure><img src="/files/nlqx9VhdEUIOJcoNNNWG" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Pregunta 4</mark>

> Según la declaración de la familia de la víctima, afirmaron que el `20 de Septiembre de 2023` salió de su domicilio sin informar a nadie de su destino. ¿Dónde se encontraba la víctima en ese momento?

En la pestaña Recent Activity encontramos una captura de pantalla de ese día en concreto, y vemos que se encontraba en `The Nile Ritz-Carlton` a las 23:50:

<figure><img src="/files/PjhvOQwIzWFZE9BpI38O" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/lUmMCvvSDBAEIRkmkjpM" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Pregunta 5</mark>

> El detective continuó su investigación interrogando a la recepción del hotel. Ella le informó que la víctima había reservado la habitación por 10 días y tenía programado un vuelo para después. El investigador cree que la víctima podría haber guardado la información de su boleto en su teléfono. Averigüe adónde pretendía viajar la víctima.

Si nos vamos a la pestaña `Discord Chats` encontramos una conversación de un usuario llamado `rob1ns0n` que le dice a la víctima que se encontrarán en "`The Mob Museum`"

<figure><img src="/files/aSGHG2T8IOon0egEy2VI" alt=""><figcaption></figcaption></figure>

Buscando `The Mob Museum` en Google descubrimos que se encuentra en Las Vegas:

<figure><img src="/files/BW1sST4KDgyTlKlGxvei" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Pregunta 6</mark>

> Tras examinar las conversaciones de Discord de la víctima, descubrimos que había quedado con un amigo en un lugar específico. ¿Puedes determinar dónde se suponía que se encontrarían?

Esta pregunta la respondimos en la anterior, quedarían en `The Mob Museum` en Las Vegas.
