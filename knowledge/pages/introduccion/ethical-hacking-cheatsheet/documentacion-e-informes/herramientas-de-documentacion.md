
# Herramientas de documentación

## <mark style="color:purple;">Documentación</mark>

Cuando se trata de documentación, primero debemos determinar la *audiencia* del informe. Documentaremos nuestras actividades de forma diferente a cómo presentaríamos nuestros resultados a un cliente. La finalidad de la documentación es presentar la información que hemos obtenido de forma comprensible y sencilla para reproducir una actividad concreta.

Por tanto las características esenciales de la documentación son:

1. `Descripción general`
2. `Estructura`
3. `Claridad`

A medida que aprendemos y practicamos, nos encontraremos con muchas situaciones y recursos diferentes. Como comentamos antes, tendremos que procesar cantidades masivas de información.

## <mark style="color:purple;">Herramientas</mark>

Hay muchos recursos disponibles para la documentación, aquí dejo alguno de los mejores:

{% embed url="<https://www.notion.so/>" %}
Documentación online estilo Markdown
{% endembed %}

{% embed url="<https://xmind.app/>" %}
Mapas mentales y relación de ideas
{% endembed %}

{% embed url="<https://obsidian.md/>" %}
Documentación online estilo Markdown
{% endembed %}

{% embed url="<https://www.gitbook.com/>" %}
Documentación online estilo Markdown
{% endembed %}

{% embed url="<https://docs.sysreptor.com/>" %}

## <mark style="color:purple;">Instalar Obsidian en Kali Linux</mark>

Una de las ventajas de usar Obsidian en Kali  Linux es que los datos se almacenan de forma local en el sistema, lo que la convierte en una herramienta excelente para auditorías internas:

```bash
wget https://github.com/obsidianmd/obsidian-releases/releases/latest/download/Obsidian-1.8.9.AppImage -O obsidian.AppImage
chmod +x obsidian.AppImage
sudo mv obsidian.AppImage /usr/local/bin/obsidian
obsidian
```

<figure><img src="/files/yWThgB8yQN2CKCxqCL9q" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Pautas a seguir</mark>

No importa a quién esté destinada la documentación, aquí hay algunas pautas que podemos seguir:

1. Es beneficioso ponernos en el lugar de nuestros lectores. Esto nos facilitará mucho el diseño de la documentación.
2. Evita la repetición y la ambigüedad.
3. Haz que la documentación sea lo más fácil de leer posible. Nadie quiere leer documentación que sea difícil de entender o seguir.
4. Antes de crear documentación para nuestros clientes, podemos aclarar qué puntos son más importantes para ellos.

## <mark style="color:purple;">Plantilla de informe</mark>

Por aquí os dejo una serie de recursos para crear informes que podemos utilizar libremente:

{% embed url="<https://drive.proton.me/urls/P6P3MFRJC4#pychIelN2pF6>" %}

#### Plantilla de reporte del ECPPTv3 en Google Docs

<https://docs.google.com/document/d/1psAcc1I2cXMj6UHDas5qVnkVjMXgcuIH/edit?usp=sharing&ouid=109728548091185682065&rtpof=true&sd=true>

## <mark style="color:purple;">Informe final</mark>

Nuestro informe entregable debe consistir en lo siguiente:

* Una `cadena de ataque` (en caso de compromiso interno total o acceso externo a interno) que detalla los pasos tomados para lograr el compromiso.
* Un sólido `resumen ejecutivo` que una audiencia `no técnica` pueda entender.
* `Hallazgos detallados específicos` del entorno del cliente que incluyen una calificación de riesgo, hallazgo de impacto, recomendaciones de remediación y referencias externas de alta calidad relacionadas con el problema.
* Pasos adecuados para `reproducir cada hallazgo` para que el equipo responsable de la remediación pueda comprender y probar el problema mientras implementa las soluciones.
* `Recomendaciones` específicas para el medio ambiente a corto, mediano y largo plazo.
* `Apéndices` que incluyen información como el alcance objetivo, datos OSINT (si son relevantes para el compromiso), análisis de descifrado de contraseñas (si es relevante), puertos/servicios descubiertos, hosts comprometidos, cuentas comprometidas, archivos transferidos a sistemas propiedad del cliente, cualquier creación de cuenta. /modificaciones del sistema, un análisis de seguridad de Active Directory (si corresponde), datos de escaneo relevantes/documentación complementaria y cualquier otra información necesaria para explicar un hallazgo o recomendación específica con más detalle

{% content-ref url="/pages/FymiiJ2sEA90VD3GTVkT" %}
[CPTS Report](/ethical-hacking-cheatsheet/introduccion/ethical-hacking-cheatsheet/documentacion-e-informes/cpts-report.md)
{% endcontent-ref %}

### Blackstone

Como herramienta relevante para generar informes de hacking os dejo Blackstone, y un video del funcionamiento de la herramienta:

{% embed url="<https://github.com/micro-joan/BlackStone>" %}

{% embed url="<https://youtu.be/x9J0YlRtXu8>" %}
