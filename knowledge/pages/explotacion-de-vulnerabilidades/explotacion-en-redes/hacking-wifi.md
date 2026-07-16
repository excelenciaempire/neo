
# Hacking WiFi

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

{% hint style="warning" %}
**Aviso:** Para realizar estas técnicas necesitarás una antena o tarjeta de red que permita el modo monitor
{% endhint %}

## <mark style="color:purple;">Laboratorio</mark>

Para realizar estas técnicas necesitaremos:

1. Máquina virtual Kali Linux
2. Router que permita WEP/WPA/WPA2
3. Adaptador de red

### Adaptador de red

El adaptador de red debe tener estas características:

```
- Chipset: RealTek RTL8812UA / Atheros AR9271 o similar
- Debe permitir Modo monitor
- Debe permitir Modo AP
- Packet injection
```

#### Recomendado

{% embed url="<https://amzn.to/4cRKgHK>" %}

### Drivers para el adaptador BrosTrend

Para instalar los drivers en Kali Linux conectar el adaptador y ejecutar:

```bash
sh -c 'wget linux.brostrend.com/install -O /tmp/install && sh /tmp/install'
```

***

### WiFi Challenge Lab

Es muy recomendable utilizar la VM de WiFi Challenge Lab, ya que nos permite practicar todo tipo de técnicas de Hacking WiFi en un entorno controlado y seguro:

{% embed url="<https://lab.wifichallenge.com/>" %}

#### Instalación

{% embed url="<https://lab.wifichallenge.com/README>" %}

1. Descargar la VM (enlace en el README)
2. Importar en VMWare o Virtualbox el archivo Open Virtualization Format Package
3. Arrancar e iniciar la máquina
4. Acceder con el usuario y contraseña: `user:user`

<figure><img src="/files/zSrI6uhSfxaDvFkicW9h" alt=""><figcaption></figcaption></figure>

#### Resolver los Challenges

El objetivo de Wifi Challenge es ir consiguiendo las flags de cada uno de los Challenges, que deberemos introducir en su página web:

{% embed url="<https://lab.wifichallenge.com/challenges>" %}

***

## <mark style="color:purple;">Links a las secciones</mark>

{% content-ref url="/pages/NK4Dtivn5kO3xj5WIHlQ" %}
[Conceptos básicos](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/conceptos-basicos.md)
{% endcontent-ref %}

{% content-ref url="/pages/6Wj8yEzrGo8GS2036ti7" %}
[Redes Básicas](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/redes-basicas.md)
{% endcontent-ref %}

{% content-ref url="/pages/zObK3pmL22ftryMxem3O" %}
[Sniffing](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/sniffing.md)
{% endcontent-ref %}

{% content-ref url="/pages/qeg4sP7H8SEkxd0kUXjq" %}
[Deauth](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/deauth.md)
{% endcontent-ref %}

{% content-ref url="/pages/JZOg8myOswgIyLEhIuwg" %}
[Redes ocultas (Hidden AP)](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/redes-ocultas-hidden-ap.md)
{% endcontent-ref %}

{% content-ref url="/pages/hCKEYOUFHTCrxOAkPOUd" %}
[WEP Cracking](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wep-cracking.md)
{% endcontent-ref %}

{% content-ref url="/pages/R0TU8XV7BiWATJAoN4eY" %}
[WPS Cracking](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wps-cracking.md)
{% endcontent-ref %}

{% content-ref url="/pages/7Wgx95Ej3jXnmYp8Sloz" %}
[WPA/WPA2 Cracking](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wpa-wpa2-cracking.md)
{% endcontent-ref %}

{% content-ref url="/pages/IbOtaOqFpR4rrmtWetea" %}
[Rainbow Table](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/rainbow-table.md)
{% endcontent-ref %}

{% content-ref url="/pages/DBqEmD6gIgFR8iFHqfgU" %}
[WPA/WPA2 Enterprise](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wpa-wpa2-enterprise.md)
{% endcontent-ref %}
