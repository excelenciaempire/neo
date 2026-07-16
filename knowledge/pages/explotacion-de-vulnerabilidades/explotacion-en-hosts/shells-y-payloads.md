
# Shells y Payloads

Como evaluadores de penetración y profesionales de la seguridad de la información, un shell suele ser el resultado de explotar una vulnerabilidad o eludir las medidas de seguridad para obtener acceso interactivo a un host. Notaremos que la mayor parte de este módulo se centrará en lo que viene después de la enumeración e identificación de exploits prometedores.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

***

## <mark style="color:purple;">Introducción</mark>

Recuerde que el shell nos da acceso directo al `sistema operativo`, a los `comandos del sistema` y al `sistema de archivos`. Entonces, si obtenemos acceso, podemos comenzar a enumerar el sistema en busca de vectores que puedan permitirnos escalar privilegios, pivotar, transferir archivos y más. Si no establecemos una sesión de shell, estamos bastante limitados en cuanto a hasta dónde podemos llegar en una máquina de destino.

Establecer un shell también nos permite mantener la persistencia en el sistema, dándonos más tiempo para trabajar. Puede facilitar el uso de nuestras herramientas de ataque, `extraer datos`, `recopilar`, `almacenar` y `documentar` todos los detalles de nuestro ataque, como pronto veremos en las demostraciones siguientes.&#x20;

Es importante tener en cuenta que establecer un shell casi siempre significa que estamos accediendo a la CLI del sistema operativo, y esto puede hacer que sea `más difícil notarlos` que si estuviéramos accediendo de forma remota a un shell gráfico a través de [VNC](https://en.wikipedia.org/wiki/Virtual_Network_Computing) o [RDP](https://www.cloudflare.com/learning/access-management/what-is-the-remote-desktop-protocol/) . Otro beneficio importante de adquirir habilidades con las interfaces de línea de comandos es que `pueden ser más difíciles de detectar que los shells gráficos`, más rápidos de navegar por el sistema operativo y más fáciles de automatizar nuestras acciones. A lo largo de este módulo, vemos los caparazones a través de la lente de las siguientes perspectivas:

<table data-header-hidden><thead><tr><th width="173"></th><th></th></tr></thead><tbody><tr><td><strong>Perspectiva</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>Ordenadores</code></td><td>El entorno de usuario basado en texto que se utiliza para administrar tareas y enviar instrucciones en una PC. Piense en Bash, Zsh, cmd y PowerShell.</td></tr><tr><td><code>Explotación y seguridad</code></td><td>Un shell suele ser el resultado de explotar una vulnerabilidad o eludir medidas de seguridad para obtener acceso interactivo a un host. Un ejemplo sería activar <a href="https://www.cisecurity.org/wp-content/uploads/2019/01/Security-Primer-EternalBlue.pdf">EternalBlue</a> en un host de Windows para obtener acceso al símbolo del cmd en un host de forma remota.</td></tr><tr><td><code>Web</code></td><td>Esto es un poco diferente. Un shell web es muy parecido a un shell estándar, excepto que explota una vulnerabilidad (a menudo la capacidad de cargar un archivo o script) que proporciona al atacante una manera de emitir instrucciones, leer y acceder a archivos, y potencialmente realizar acciones destructivas en el sistema subyacente. anfitrión. El control del shell web a menudo se realiza llamando al script dentro de una ventana del navegador.</td></tr></tbody></table>

***

## <mark style="color:purple;">Payloads</mark>

### Los Payloads nos dan Shells

Dentro de la industria de TI en su conjunto, un `Payload` o "`Carga Útil`" se puede definir de diferentes maneras:

* `Networking`: La porción de datos encapsulados de un paquete que atraviesa las redes informáticas modernas.
* `Computación Básica`: Una carga útil es la parte de un conjunto de instrucciones que define la acción a realizar. Se eliminaron los encabezados y la información del protocolo.
* `Programación`: La porción de datos a la que hace referencia o es transportada por la instrucción del lenguaje de programación.
* `Explotación y Seguridad`: Una carga útil es un código elaborado con la intención de explotar una vulnerabilidad en un sistema informático. El término carga útil puede describir varios tipos de malware, incluido, entre otros, el ransomware.

En este módulo, trabajaremos con muchos tipos diferentes de cargas útiles y métodos de entrega en el contexto de otorgarnos acceso a un host y establecer sesiones de shell remotas con sistemas vulnerables.

***

## <mark style="color:purple;">Anatomía de un Shell</mark>

Todo sistema operativo tiene un shell y para interactuar con él debemos utilizar una aplicación conocida como `Emulador de Terminal`. Estos son algunos de los emuladores de terminal más comunes:

<table data-header-hidden><thead><tr><th width="354"></th><th></th></tr></thead><tbody><tr><td><strong>Emulador de Terminal</strong></td><td><strong>Sistema Operativo</strong></td></tr><tr><td><a href="https://github.com/microsoft/terminal">Windows Terminal</a></td><td>Windows</td></tr><tr><td><a href="https://cmder.app/">cmder</a></td><td>Windows</td></tr><tr><td><a href="https://www.putty.org/">PuTTY</a></td><td>Windows</td></tr><tr><td><a href="https://sw.kovidgoyal.net/kitty/">kitty</a></td><td>Windows, Linux and MacOS</td></tr><tr><td><a href="https://github.com/alacritty/alacritty">Alacritty</a></td><td>Windows, Linux and MacOS</td></tr><tr><td><a href="https://invisible-island.net/xterm/">xterm</a></td><td>Linux</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/GNOME_Terminal">GNOME Terminal</a></td><td>Linux</td></tr><tr><td><a href="https://github.com/mate-desktop/mate-terminal">MATE Terminal</a></td><td>Linux</td></tr><tr><td><a href="https://konsole.kde.org/">Konsole</a></td><td>Linux</td></tr><tr><td><a href="https://en.wikipedia.org/wiki/Terminal_(macOS)">Terminal</a></td><td>MacOS</td></tr><tr><td><a href="https://iterm2.com/">iTerm2</a></td><td>MacOS</td></tr></tbody></table>

Esta lista no incluye todos los emuladores de terminal disponibles, pero incluye algunos dignos de mención. El emulador de terminal con el que interactuamos en los objetivos dependerá esencialmente de lo que exista en el sistema de forma nativa.

***

## <mark style="color:purple;">Hack Tools Plugin</mark>

<figure><img src="/files/zdEcbJZuAKpCSX2KAXvs" alt=""><figcaption><p>Hack Tools PLugin</p></figcaption></figure>

{% embed url="<https://chrome.google.com/webstore/detail/hack-tools/cmbndhnoonmghfofefkcccljbkdpamhi?hl=es-419>" %}

Este plugin disponible para todos los navegadores nos permite crear Shells a medida para una IP y un puerto que le establezcamos, y en varios lenguajes de programación.
