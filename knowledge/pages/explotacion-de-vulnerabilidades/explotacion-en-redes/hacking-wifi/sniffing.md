
# Sniffing

{% hint style="danger" %}
**Disclaimer**: Este tipo de actividad debe realizarse únicamente en redes que te pertenezcan o donde tengas permiso para realizar pruebas de seguridad, ya que hacer sniffing sin autorización es ilegal y antiético.
{% endhint %}

{% hint style="warning" %}
**Nota:** Para este laboratorio la red debe estar configurada como WEP. Deshabilitar SKA (Shell Key Autentication). De lo contrario puede que no funcione como esperamos.
{% endhint %}

## <mark style="color:purple;">Bases del Sniffing</mark>

El sniffing es una técnica que se basa en capturar tramas de una red. Esto se suele hacer en redes internas aunque también se puede hacer en internet y en redes WiFi.

### Conceptos relevantes

<table><thead><tr><th width="125">Término</th><th>Descripción</th></tr></thead><tbody><tr><td>BSSID</td><td>Dirección MAC de la estación base (punto de acceso) que se está analizando</td></tr><tr><td>PWR</td><td>Potencia de la señal recibida, medida en dBm (decibelios milivatios)</td></tr><tr><td>Beacons</td><td>Número de paquetes de balizas (beacons) recibidos desde el BSSID</td></tr><tr><td>#Data</td><td>Número total de paquetes de datos recibidos desde el BSSID</td></tr><tr><td>#/s</td><td>Tasa de recepción de paquetes de datos por segundo desde el BSSID</td></tr><tr><td>CH</td><td>Canal en el que opera la estación base (punto de acceso)</td></tr><tr><td>MB</td><td>Velocidad máxima de transmisión admitida por la estación base</td></tr><tr><td>ENC</td><td>Método de cifrado utilizado por la red (WEP, WPA, WPA2, etc.)</td></tr><tr><td>CIPHER</td><td>Algoritmo de cifrado utilizado (CCMP, AES, TKIP, etc.)</td></tr><tr><td>AUTH</td><td>Método de autenticación utilizado por la red (Open, Shared, etc.)</td></tr><tr><td>ESSID</td><td>Nombre de la red inalámbrica (ESSID) transmitido por la estación base</td></tr></tbody></table>

```bash
sudo airodump-ng wlan0   

# Pulsando espacio lo podemos detener
 CH 11 ][ Elapsed: 24 s ][ 2023-10-31 17:15 ][ paused output

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
                                               
 B0:76:1B:91:21:1A  -82        1        0    0   4  400   WPA2 CCMP   PSK  DIGI-H36b                                                   
 D8:E8:44:B3:6B:F6  -77        4        0    0   2  324   WPA2 CCMP   PSK  DIGIFIBRA-yCtU                                              
 C6:8B:92:FA:80:37  -70        4        1    0  11  720   WPA2 CCMP   PSK  MIWIFI_hRNd                                                                                                 
 F8:AA:3F:61:EB:24  -78        8        0    0   8  130   WPA2 CCMP   PSK  Desproposito                                                      
 3C:A7:AE:92:29:F5  -74        3        0    0  10  360   WPA2 CCMP   PSK  DIGIFIBRA-PbYb                                              
 84:2A:FD:E8:1B:9F  -56       15        0    0   6   65   WPA2 CCMP   PSK  DIRECT-7B-HP DeskJet 2700 series                                                            
 EC:F4:51:A2:32:0C  -55       37        2    0  11  130   WPA2 CCMP   PSK  MiFibra-327A                                                
 18:69:D8:CA:AA:AB  -71       22        0    0   5   65   OPN              Conga-AAEB                                               
 58:76:AC:F2:04:6F  -80       25        7    2  12  130   WPA2 CCMP   PSK  vodafoneBA7211                                              
 E4:66:AB:4C:2F:18  -59       20        0    0   6  720   WPA2 CCMP   PSK  DIGIFIBRA-cQT5
```

## <mark style="color:purple;">Sniffing con Airodump y Wireshark</mark>

* Encontrar a la víctima
* Realizar sniffing con airodump
* Subir el archivo .CAP a wireshark

### 1. Iniciamos airmon-ng

```bash
# Apagamos el adaptador wlan0
sudo ifconfig wlan0 down

# Iniciamos el modo monitor con airmon-ng
sudo airmon-ng start wlan0
```

### 2. Encontrar a la víctima

```bash
sudo airodump-ng wlan0
 CH 13 ][ Elapsed: 4 mins ][ 2023-10-31 18:30 ][ paused output

  BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
                                                                            
 EA:66:AB:4C:31:EA  -45       21        0    0   9  720   WPA2 CCMP   PSK  INHACKEABLE 
```

### 3. Sniffing con Airodump-ng

```bash
sudo airodump-ng --bssid EA:66:AB:4C:31:EA --channel 9 wlan0 --write sniffing_test

CH 100 ][ Elapsed: 1 min ][ 2023-10-31 17:37 

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID
 EA:66:AB:4C:32:EA  -44       13        0    0   1  720   WPA3 CCMP   SAE  PRUEBAS                                    

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Probes
 EA:66:AB:4C:32:EA  8C:B0:E9:4B:1C:E9  -58    0 - 6      0        1                                                                     
 EA:66:AB:4C:32:EA  E6:A3:67:1A:B3:76  -69    0 -24      0        7                                                                     
 EA:66:AB:4C:32:EA  42:72:FA:7B:37:05  -37    6e-24      0        4                                                                     
 EA:66:AB:4C:32:EA  28:F0:76:4F:4E:3C  -45    6e-24e     0        2                                                                     
 EA:66:AB:4C:32:EA  F4:D4:88:85:E8:74  -39    0 -24      0       20 
```

### 4. Ver el archivo .cap

```bash
 # Tenemos el archivo .cap
 ls
 sniffing_test-01.cap
```

### 5. Abrir archivo .cap con wireshark

<figure><img src="/files/qb8lXQINUYRXFWmrlb8B" alt=""><figcaption></figcaption></figure>

Vemos correctamente el sniffing, aunque los datos están cifrados, ya que el tráfico es a través de HTTPS:

<figure><img src="/files/p9cZLQqF4ffMq7n2PfKj" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Sniffing con Bettercap</mark>

Bettercap es una herramienta poderosa para realizar ataques de red, monitoreo y pruebas de penetración en redes inalámbricas. Se utiliza frecuentemente para realizar tareas como el “sniffing” (escucha o interceptación de tráfico de red) en redes Wi-Fi.

### 1. Instalar Bettercap:&#x20;

Asegúrate de tener Bettercap instalado en tu máquina. Puedes instalarlo en Kali Linux usando:

```bash
sudo apt update && sudo apt install bettercap
```

### 2. Configurar el Modo Monitor

Antes de comenzar a usar Bettercap, debes asegurarte de que tu tarjeta de red Wi-Fi esté en modo monitor para poder escuchar el tráfico de red.

<pre class="language-bash"><code class="lang-bash"># Apagamos el adaptador wlan0
<strong>sudo ifconfig wlan0 down
</strong>
# Iniciamos el modo monitor con airmon-ng
sudo airmon-ng start wlan0
</code></pre>

### 3. Iniciar Bettercap

Una vez que tu tarjeta de red esté en modo monitor, inicia Bettercap con privilegios de superusuario:

```bash
sudo bettercap -iface wlan0
```

### 4. Escanear Redes Wi-Fi

Para encontrar las redes disponibles, utiliza el módulo de wifi de Bettercap. Este módulo te permitirá escanear todas las redes Wi-Fi cercanas.

```bash
wifi.recon on
wifi.show
```

<figure><img src="/files/efDnR50fqhb0w84YQsaU" alt=""><figcaption></figcaption></figure>

### 5. Seleccionar la Red Objetivo

Una vez que encuentres la red que deseas monitorear, selecciona la red objetivo. Esto se hace utilizando el BSSID:

```bash
set wifi.recon.bssid XX:XX:XX:XX:XX:XX
```

### 6. Mostrar dispositivos conectados

```bash
net.show
```

### 7. Habilitar el Sniffing

Para capturar los paquetes de red, debes habilitar el módulo de sniffing. El módulo de sniffer captura los paquetes de la red, incluidos los paquetes no cifrados.

```bash
set net.sniff.local true
net.sniff on
```

Esto capturará los paquetes locales en tu red y te permitirá ver el tráfico no cifrado (HTTP, por ejemplo) o información de red de dispositivos conectados.

También podríamos guardar el tráfico capturado en un archivo pcap para analizarlo más tarde con herramientas como Wireshark, como ya hemos visto en esta sección:

```bash
set net.sniff.output /home/kali/wifi_hacking/output.pcap
net.sniff on
```

### 8. Mejorando el Sniffing: Bypass de HTTPS (HSTS)

**Problema:** Hoy en día la mayoría de sitios usan HTTPS (cifrado). Si haces sniffing solo verás datos cifrados (basura).

**Solución:** Bettercap puede hacer **SSL Stripping** usando el caplet `hstshijack`.

```bash
sudo bettercap -eval "set arp.spoof.targets 192.168.1.10; arp.spoof on; hstshijack on"
```

*Esto engaña al navegador de la víctima para que use HTTP, permitiéndote ver el tráfico.*
