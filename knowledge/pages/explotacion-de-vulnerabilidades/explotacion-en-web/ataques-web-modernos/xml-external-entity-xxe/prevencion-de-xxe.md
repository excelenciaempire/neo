
# Prevención de XXE

Hemos visto que las vulnerabilidades XXE ocurren principalmente cuando una entrada XML no segura hace referencia a una entidad externa, que eventualmente se explota para leer archivos confidenciales y realizar otras acciones. Prevenir las vulnerabilidades XXE es relativamente más fácil que prevenir otras vulnerabilidades web, ya que son causadas principalmente por bibliotecas XML obsoletas.

***

## <mark style="color:purple;">Evitar componentes obsoletos</mark>

Si bien otras vulnerabilidades de validación de entrada web suelen evitarse mediante prácticas de codificación seguras (por ejemplo, XSS, IDOR, SQLi, inyección de SO), esto no es del todo necesario para evitar vulnerabilidades XXE. Esto se debe a que la entrada XML no suele ser manejada manualmente por los desarrolladores web, sino por las bibliotecas XML integradas. Por lo tanto, si una aplicación web es vulnerable a XXE, es muy probable que se deba a una biblioteca XML obsoleta que analiza los datos XML.

Por ejemplo, la función [libxml\_disable\_entity\_loader](https://www.php.net/manual/en/function.libxml-disable-entity-loader.php) de PHP está obsoleta porque permite a un desarrollador habilitar entidades externas de manera insegura, lo que genera vulnerabilidades XXE. Si visitamos la documentación de PHP para esta función, vemos la siguiente advertencia:

{% hint style="danger" %}
**Warning:** This function has been *DEPRECATED* as of PHP 8.0.0. Relying on this function is highly discouraged.
{% endhint %}

Además, incluso los editores de código comunes (por ejemplo, VSCode) resaltarán que esta función específica está obsoleta y nos advertirán contra su uso:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_xxe_deprecated_warning.jpg" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Nota: Puede encontrar un informe detallado de todas las bibliotecas XML vulnerables, con recomendaciones sobre cómo actualizarlas y utilizar funciones seguras, en [la Hoja de referencia de prevención XXE de OWASP](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html#php) .
{% endhint %}

Además de actualizar las bibliotecas XML, también deberíamos actualizar todos los componentes que analizan la entrada XML, como las bibliotecas API como SOAP. Además, todos los procesadores de documentos o archivos que puedan realizar análisis XML, como los procesadores de imágenes SVG o los procesadores de documentos PDF, también pueden ser vulnerables a vulnerabilidades XXE, por lo que también deberíamos actualizarlos.

Estos problemas no son exclusivos de las bibliotecas XML, ya que lo mismo se aplica a todos los demás componentes web (por ejemplo, `Node Modules` obsoletos). Además de los administradores de paquetes comunes (por ejemplo `npm`), los editores de código comunes notificarán a los desarrolladores web sobre el uso de componentes obsoletos y sugerirán otras alternativas. Al final, el uso de las últimas bibliotecas XML y componentes de desarrollo web puede ayudar enormemente a reducir diversas vulnerabilidades web, incluido XXE.

***

## <mark style="color:purple;">Uso de configuraciones XML seguras</mark>

Además de utilizar las bibliotecas XML más recientes, ciertas configuraciones XML para aplicaciones web pueden ayudar a reducir la posibilidad de explotación de XXE. Entre ellas se incluyen:

* Deshabilitar referencia a `Document Type Definitions (DTDs)` personalizada.
* Deshabilitar referencia a `External XML Entities`
* Deshabilitar procesamiento `Parameter Entity`
* Deshabilitar el soporte para `XInclude`
* Prevenir `Entity Reference Loops`

Otra cosa que vimos fue la explotación de XXE basada en errores. Por lo tanto, siempre deberíamos tener un manejo de excepciones adecuado en nuestras aplicaciones web y siempre se debe desactivar la visualización de errores de tiempo de ejecución en los servidores web.

Estas configuraciones deberían ser otra capa de protección si no actualizamos algunas bibliotecas XML y también deberían evitar la explotación de XXE. Sin embargo, es posible que sigamos utilizando bibliotecas vulnerables en estos casos y que solo apliquemos soluciones alternativas contra la explotación, lo que no es ideal.

Debido a los diversos problemas y vulnerabilidades que presentan los datos XML, muchos también recomiendan usar otros formatos, como JSON o YAML. Esto también incluye evitar los estándares de API que se basan en XML (por ejemplo, SOAP) y usar API basadas en JSON en su lugar (por ejemplo, REST).

Por último, el uso de firewalls de aplicaciones web (WAF) es otra capa de protección contra la explotación de XXE. Sin embargo, nunca debemos confiar completamente en los WAF y dejar vulnerable el back-end, ya que siempre se pueden eludir.
