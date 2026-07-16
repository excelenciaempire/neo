
# Extensiones

Tanto Burp como ZAP tienen capacidades de extensión, de modo que la comunidad de usuarios de Burp puede desarrollar extensiones para Burp para que todos las usen. Dichas extensiones pueden realizar acciones específicas en cualquier solicitud capturada, por ejemplo, o agregar nuevas funciones, como decodificar y embellecer el código. Burp permite la extensibilidad a través de su característica `Extender` y su [BApp Store](https://portswigger.net/bappstore) , mientras que ZAP tiene su [ZAP Marketplace](https://www.zaproxy.org/addons/) para instalar nuevos complementos.

***

## <mark style="color:purple;">BApp Store</mark>

Para encontrar todas las extensiones disponibles, podemos hacer clic en la pestaña `Extender` dentro de Burp y seleccionar la subpestaña `BApp Store`. Una vez que lo hagamos, veremos una gran cantidad de extensiones. Podemos ordenarlas por `Popularity` para saber cuáles son las que los usuarios encuentran más útiles:

![](https://academy.hackthebox.com/storage/modules/110/burp_bapp_store.jpg)

{% hint style="info" %}
**Nota**: Algunas extensiones son solo para usuarios Pro, mientras que la mayoría de las demás están disponibles para todos.
{% endhint %}

Vemos muchas extensiones útiles. Tómese un tiempo para revisarlas y ver cuáles son las más útiles para usted. Luego, intente instalarlas y probarlas. Probemos a instalar la extensión `Decoder Improved`:

![Extensión para eructar](https://academy.hackthebox.com/storage/modules/110/burp_extension.jpg)

{% hint style="info" %}
**Nota**: Algunas extensiones tienen requisitos que normalmente no se instalan en Linux/macOS/Windows de forma predeterminada, como \`Jython\`, por lo que debes instalarlos antes de poder instalar la extensión.
{% endhint %}

Una vez que instalamos `Decoder Improved`, veremos que su nueva pestaña se ha añadido a Burp. Cada extensión tiene un uso diferente, por lo que podemos hacer click en la documentación de cualquier extensión en `BApp Store` para leer más sobre ella o visitar su página de GitHub para obtener más información sobre su uso. Podemos utilizar esta extensión de la misma forma que utilizaríamos el Decodificador de Burp, con el beneficio de tener muchos codificadores adicionales incluidos. Por ejemplo, podemos introducir el texto con el que queremos codificar `MD5` y seleccionar `Hash With > MD5`:

![](https://academy.hackthebox.com/storage/modules/110/burp_extension_decoder_improved.jpg)

De manera similar, podemos realizar otros tipos de codificación y hash. Existen muchas otras extensiones de Burp que se pueden utilizar para ampliar aún más la funcionalidad de Burp.

Algunas extensiones que vale la pena revisar incluyen, entre otras:

|                              |                           |                                |
| ---------------------------- | ------------------------- | ------------------------------ |
| .NET beautifier              | J2EEScan                  | Software Vulnerability Scanner |
| Software Version Reporter    | Active Scan++             | Additional Scanner Checks      |
| AWS Security Checks          | Backslash Powered Scanner | Wsdler                         |
| Java Deserialization Scanner | C02                       | Cloud Storage Tester           |
| CMS Scanner                  | Error Message Checks      | Detect Dynamic JS              |
| Headers Analyzer             | HTML5 Auditor             | PHP Object Injection Check     |
| JavaScript Security          | Retire.JS                 | CSP Auditor                    |
| Random IP Address Header     | Autorize                  | CSRF Scanner                   |
| JS Link Finder               |                           |                                |

***

## <mark style="color:purple;">ZAP Marketplace</mark>

ZAP también tiene su propia función de extensibilidad con `Marketplace` con el que podemos instalar varios tipos de complementos desarrollados por la comunidad. Para acceder al marketplace de ZAP, podemos hacer click en el botón `Manage Add-ons` y luego seleccionar la pestaña `Marketplace`:

![](https://academy.hackthebox.com/storage/modules/110/zap_marketplace_button.jpg)

En esta pestaña, podemos ver los diferentes complementos disponibles para ZAP. Algunos complementos pueden estar en su compilación `Release`, lo que significa que deberían ser estables para su uso, mientras que otros están en su compilación `Beta/Alpha`, lo que significa que pueden experimentar algunos problemas en su uso. Probemos a instalar los complementos `FuzzDB Files` y `FuzzDB Offensive`, que agregan nuevas listas de palabras para usar en el fuzzer de ZAP:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzdb_install.jpg" alt=""><figcaption></figcaption></figure>

Ahora, tendremos la opción de elegir entre las distintas listas de palabras y payloads proporcionadas por FuzzDB al realizar un ataque. Por ejemplo, supongamos que tuviéramos que realizar un ataque de fuzzing de inyección de comandos en uno de los ejercicios que usamos anteriormente en este módulo. En ese caso, veremos que tenemos más opciones en las listas de palabras `File Fuzzers`, incluida una lista de palabras de inyección de comandos del sistema operativo bajo ( `fuzzdb > attack > os-cmd-execution`), que sería perfecta para este ataque:

![](https://academy.hackthebox.com/storage/modules/110/zap_fuzzdb_cmd_exec.jpg)

Ahora, si ejecutamos el fuzzer en nuestro ejercicio usando la lista de palabras anterior, veremos que fue capaz de explotarla de varias maneras, lo que sería muy útil si estuviéramos tratando con una aplicación web protegida por WAF:

![Ejecución de CMD de FuzzDB](https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_cmd_inj.jpg)

***

## <mark style="color:purple;">Reflexiones finales</mark>

A lo largo de este módulo, hemos demostrado el poder de Burp Suite y los proxies ZAP y hemos analizado las diferencias y similitudes entre las versiones gratuitas y profesionales de Burp y el proxy ZAP gratuito y de código abierto. Estas herramientas son esenciales para los pentesters centrados en las evaluaciones de seguridad de aplicaciones web, pero tienen muchas aplicaciones para todos los profesionales de la seguridad ofensiva, así como para los desarrolladores y los profesionales del Blue Team.&#x20;
