
# Escaneo de Redes Wifi

<figure><img src="/files/BLKnEiCX1Rn5VOuJyPT8" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Escaneo de AP (Access Points)</mark> <a href="#mifss" id="mifss"></a>

Un AP, o Punto de Acceso (Access Point), es un dispositivo de red que permite a los dispositivos inalámbricos conectarse a una red cableada. Funciona como un puente que amplía la cobertura de red, proporcionando acceso a Internet u otros recursos de red a los dispositivos que se encuentran en su rango de acción. Los AP son esenciales en ambientes donde se requiere movilidad y flexibilidad de acceso, comúnmente utilizados en oficinas, hogares, y espacios públicos para garantizar una conectividad robusta y estable.

### Escaneo con Marauder

Una vez que tenemos Marauder instalado podemos escanear redes de la siguiente manera:

1. Vamos a `GPIO > ESP > Wifi Marauder`

<figure><img src="/files/SzHpcqU50YheCvJdhQqa" alt=""><figcaption></figcaption></figure>

2. Seleccionamos `Scan ap`

{% hint style="info" %}
Podemos cambiar `ap` a `station` para escanear dispositivos conectados a las redes.
{% endhint %}

<figure><img src="/files/0Va79NHyva51xktWTqHq" alt=""><figcaption></figcaption></figure>

3. Le damos y empieza a escanear todas las redes Wifi cercanas con datos como el BSSID, ESSID, el Beacon... Esto nos servirá para identificar la red objetivo:

<figure><img src="/files/FTecKRDWgDyWjUr3TQDs" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Ver log del escaneo</mark>

Todos los escaneos que realizamos se guardan en logs para poder consultarlo posteriormente. Vamos a `View Log From start` y observamos los datos recopilados.

<div><figure><img src="/files/QRodtw7VIfa8aOTC2KZf" alt=""><figcaption></figcaption></figure> <figure><img src="/files/pPgN1oUwJP0AEVv2MUcW" alt=""><figcaption></figcaption></figure></div>

## <mark style="color:orange;">Ver listado de APs, SSIDs o Stations</mark>

Si vamos al apartado `List` y seleccionamos `ap, ssid, station o airtag` vemos un listado en detalle del nombre de los APs o dispositivos conectados, con un número asociado. Este número nos servirá para configurar ataques como el Deauth.

<div><figure><img src="/files/Cv8bKokggUFqBKx41qOY" alt=""><figcaption></figcaption></figure> <figure><img src="/files/MvqUULXYdODKzVA2bnJx" alt=""><figcaption></figcaption></figure></div>

En nuestro caso, el objetivo será la red `INHACKEABLE`  con el `ID 1`. Vosotros podéis configurar una red Wifi vulnerable para seguir estas secciones desde los ajustes de vuestro router.
