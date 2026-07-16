
# Metodología OSSTMM

## <mark style="color:purple;">Manual</mark>

{% embed url="<https://www.isecom.org/OSSTMM.3.pdf>" %}

## <mark style="color:purple;">Fases</mark>

La metodología OSSTMM se basa en principios y técnicas de prueba de seguridad comprobados y ofrece una guía sistemática para llevar a cabo pruebas de seguridad efectivas. A continuación, se describen los pasos de la metodología OSSTMM:

### 1 - Recopilación de información

En esta fase, se recopila información sobre el sistema de información o red que se va a evaluar. Se pueden utilizar técnicas como el escaneo de puertos, la enumeración de servicios y la obtención de información a través de motores de búsqueda y fuentes de información públicas (OSINT).

{% content-ref url="/pages/ALDUNSDEyY0bVOdNQRV7" %}
[Recopilación de información](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion.md)
{% endcontent-ref %}

### 2 - Análisis de la información

En esta fase, se analiza la información recopilada para identificar posibles vulnerabilidades y debilidades en la seguridad del sistema. También se incluiría la enumeración de servicios.

{% content-ref url="/pages/Ag9r8hEh8uYEXCNRBKfS" %}
[Enumeración](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion.md)
{% endcontent-ref %}

### 3 - Análisis de vulnerabilidades

En esta fase, se llevan a cabo análisis de vulnerabilidad para identificar las debilidades en la seguridad del sistema. Esto puede incluir análisis de vulnerabilidades con Nmap, Nikto, Nessus o otras herramientas, y búsqueda de CVEs asociados a una vulnerabilidad.

{% content-ref url="/pages/xG7UjcFyqbAyLYb0q8N3" %}
[Análisis de vulnerabilidades](/ethical-hacking-cheatsheet/analisis-de-vulnerabilidades/analisis-de-vulnerabilidades.md)
{% endcontent-ref %}

### 4 - Explotación de vulnerabilidades

En esta fase, se explotan las vulnerabilidades identificadas para demostrar los riesgos de seguridad y evaluar la capacidad del sistema para resistir ataques.

{% content-ref url="/pages/32EWeHCoJpgJQKiFEWPu" %}
[Explotación en Hosts](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts.md)
{% endcontent-ref %}

{% content-ref url="/pages/lR7kEr6Z3xg5x5zFtu6n" %}
[Explotación en Web](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web.md)
{% endcontent-ref %}

{% content-ref url="/pages/IF7ffHyuTVXjujBFqecP" %}
[Explotación en Redes](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes.md)
{% endcontent-ref %}

### 5 - Post explotación

En esta fase usamos técnicas específicas de post explotación para comprometer aún más a un objetivo ya comprometido y elevar nuestros permisos en el sistema, movernos lateralmente por una red empresarial, obtener credenciales, etc...

{% content-ref url="/pages/LoHk1ifaBkOE3jxQoCTD" %}
[Post Explotación](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion.md)
{% endcontent-ref %}

{% content-ref url="/pages/5KGjWN4U83ofo1wtIfWj" %}
[Escalada de Privilegios](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios.md)
{% endcontent-ref %}

### 6 - Documentación

En esta fase, se documentan los hallazgos, las debilidades y las recomendaciones de seguridad para el sistema evaluado. La documentación puede incluir informes de pruebas, recomendaciones de seguridad y planes de acción.

{% content-ref url="/pages/nZTjWz0qMz3buqRw7tth" %}
[Documentos iniciales](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/documentacion-e-informes/documentos-iniciales.md)
{% endcontent-ref %}
