
# Identificar Tecnologías

## <mark style="color:purple;">WhatWeb</mark>

WhatWeb es una herramienta de reconocimiento de aplicaciones web de código abierto utilizada para identificar tecnologías web y aplicaciones utilizadas en un sitio web. La herramienta utiliza técnicas de análisis de encabezados HTTP y otros datos públicos para identificar los componentes y tecnologías utilizados en un sitio web. Viene por defecto en Kali Linux.

[<mark style="color:purple;">https://github.com/urbanadventurer/WhatWeb</mark>](https://github.com/urbanadventurer/WhatWeb)

{% hint style="warning" %}
Es muy poco intrusivo, pero hace peticiones al servidor.
{% endhint %}

### Ver todos los plugins disponibles

```
whatweb -l
```

### Escaneo normal

```
whatweb -v IP-TARGET
```

{% hint style="info" %}
Quitar el flag -v para una versión reducida
{% endhint %}

### Escaneo agresivo

```
whatweb -a 4 http://IP-TARGET:8080
```

{% hint style="danger" %}
Esta técnica es intrusiva, ya que hace muchas más peticiones al servidor.
{% endhint %}

## <mark style="color:purple;">WebAnalyze</mark>

WebAnalyze es una herramienta de análisis de seguridad de código abierto utilizada para evaluar la seguridad de aplicaciones web y sitios web. Esta herramienta es muy útil para identificar vulnerabilidades en aplicaciones web y para evaluar la efectividad de las medidas de seguridad implementadas.

{% embed url="<https://github.com/rverton/webanalyze>" %}

```php
go install -v github.com/rverton/webanalyze/cmd/webanalyze@latest
webanalyze -update # loads new technologies.json file from wappalyzer project
webanalyze -h
```

```
webanalyze -host IP-TARGET
```
