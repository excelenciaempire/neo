
# Evasión de WAFs

## <mark style="color:purple;">WAF Detector</mark>

Un detector de WAF (Web Application Firewall) es una herramienta de seguridad utilizada para identificar si un sitio web está protegido por un WAF y, en algunos casos, para identificar el tipo de WAF que se está utilizando. Estos detectores de WAF utilizan diferentes técnicas de análisis para determinar si un sitio web está siendo protegido por un WAF.

### wafw00f

WAFW00F (Web Application Firewall Fingerpriting Tool) es una herramienta de código abierto utilizada para identificar si un sitio web está protegido por un WAF y, en algunos casos, para identificar el tipo de WAF que se está utilizando. WAFW00F utiliza una variedad de técnicas de análisis para determinar si un sitio web está siendo protegido por un WAF.

{% embed url="<https://github.com/EnableSecurity/wafw00f>" %}

```
wafw00f TARGET
```

## <mark style="color:purple;">WAF Evasion</mark>

La evasión de WAF (Web Application Firewall) se refiere a técnicas utilizadas por los atacantes para superar o evitar las medidas de seguridad implementadas por un WAF y llevar a cabo ataques exitosos a una aplicación web protegida por un WAF.

* Buscar resto de subdominios que no esté protegido por un WAF
* Sino hay nada hay alternativas usando bypass

### BFD - Bypass Firewalls by DNS History

Bypass Firewalls by DNS History (BDF) es una técnica de evasión de firewall que aprovecha la información de los registros de historial de DNS de un sitio web para acceder a contenido bloqueado por un firewall. BDF se basa en la idea de que los firewalls a menudo bloquean el acceso a sitios web en función de su dirección IP o nombre de dominio, pero no tienen en cuenta la historia del DNS de los sitios web.

{% embed url="<https://github.com/vincentcox/bypass-firewalls-by-DNS-history>" %}

```
cd bypass
sudo apt install jq
bash bypass-firewalls-by-DNS-history.sh -d TARGET
```

### WAF Bypass

Esta página web recoge multitud de post sobre Bypass de WAFs

{% embed url="<https://waf-bypass.com/>" %}

{% hint style="danger" %}
Estas técnicas son muy intrusivas, no utilizar estas técnicas sin autorización del objetivo.
{% endhint %}

#### Herramientas de WAF Bypass

* WhatWaf: <https://github.com/Ekultek/WhatWaf>
* WafNinja: <https://github.com/khalilbijjou/wafninja>
* WafPass: <https://sectechno.com/wafpass-analyzing-waf-bypass-methods/>
