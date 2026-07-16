
# Webshells

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

### ¿Qué es un shell web?

Una `web shell` es una sesión de shell basada en navegador que podemos usar para interactuar con el sistema operativo de un servidor web. Nuevamente, para obtener la ejecución remota de código a través del shell web, primero debemos encontrar una vulnerabilidad de un sitio web o una aplicación web que pueda brindarnos capacidades de carga de archivos. La mayoría de los shells web se obtienen cargando una carga útil escrita en un lenguaje web en el servidor de destino. Las cargas útiles que subimos deberían brindarnos la capacidad de ejecución remota de código dentro del navegador.&#x20;

Las secciones y desafíos siguientes se centrarán principalmente en la ejecución de comandos a través de nuestros shells web en el navegador. Aún así, es esencial saber que confiar únicamente en el shell web para interactuar con el sistema puede ser inestable y poco confiable porque algunas aplicaciones web están configuradas para eliminar la carga de archivos después de un cierto período de tiempo. Para lograr persistencia en un sistema, en muchos casos, esta es la forma inicial de obtener la ejecución remota de código a través de una aplicación web, que luego podemos usar para actualizar posteriormente a un shell inverso más interactivo.

En las siguientes secciones, aprenderemos y experimentaremos con varios shells web que nos permiten interactuar con el sistema operativo subyacente de un servidor web a través del navegador web.

{% code title="Simple webshell" %}

```bash
<?php echo passthru($_GET[‘cmd’]); ?>
```

{% endcode %}

## <mark style="color:purple;">Webshells</mark>

{% content-ref url="/pages/0PKmAK58pQVG5PDeSfyt" %}
[Laudanum](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/webshells/laudanum.md)
{% endcontent-ref %}

{% content-ref url="/pages/ASpSatdzYuxPQXXAbyhf" %}
[PHP Webshell](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/shells-y-payloads/webshells/php-webshell.md)
{% endcontent-ref %}
