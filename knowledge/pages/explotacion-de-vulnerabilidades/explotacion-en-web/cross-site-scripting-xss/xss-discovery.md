
# XSS Discovery

A estas alturas, ya deberíamos tener una buena comprensión de lo que es una vulnerabilidad XSS, los tres tipos de XSS y en qué se diferencia cada uno de los demás. También deberíamos entender cómo funciona XSS al inyectar código JavaScript en la fuente de la página del lado del cliente, ejecutando así código adicional, que luego aprenderemos a utilizar en nuestro beneficio.

En esta sección, repasaremos varias formas de detectar vulnerabilidades XSS dentro de una aplicación web. En el caso de las vulnerabilidades de aplicaciones web (y de todas las vulnerabilidades en general), detectarlas puede resultar tan difícil como explotarlas. Sin embargo, como las vulnerabilidades XSS están muy extendidas, existen muchas herramientas que pueden ayudarnos a detectarlas e identificarlas.

***

## <mark style="color:purple;">Descubrimiento automatizado</mark>

Casi todos los escáneres de vulnerabilidades de aplicaciones web (como [Nessus](https://www.tenable.com/products/nessus) , [Burp Pro](https://portswigger.net/burp/pro) o [ZAP](https://www.zaproxy.org/) ) tienen varias capacidades para detectar los tres tipos de vulnerabilidades XSS. Estos escáneres suelen realizar dos tipos de escaneo: un escaneo pasivo, que revisa el código del lado del cliente en busca de posibles vulnerabilidades basadas en DOM, y un escaneo activo, que envía varios tipos de payloads para intentar activar un XSS mediante la inyección de payloads en el código fuente de la página.

Aunque las herramientas de pago suelen tener un mayor nivel de precisión a la hora de detectar vulnerabilidades XSS (especialmente cuando se requieren eludir las normas de seguridad), aún podemos encontrar herramientas de código abierto que pueden ayudarnos a identificar posibles vulnerabilidades XSS. Estas herramientas suelen funcionar identificando campos de entrada en páginas web, enviando varios tipos de payloads XSS y luego comparando el código fuente de la página renderizada para ver si se puede encontrar el mismo payload en ella, lo que puede indicar una inyección XSS exitosa. Aun así, esto no siempre será preciso, ya que a veces, incluso si se inyectó el mismo payload, es posible que no se ejecute correctamente debido a varias razones, por lo que siempre debemos verificar manualmente la inyección XSS.

Algunas de las herramientas de código abierto más comunes que pueden ayudarnos a descubrir XSS son [XSS Strike](https://github.com/s0md3v/XSStrike) , [Brute XSS](https://github.com/rajeshmajumdar/BruteXSS) y [XSSer](https://github.com/epsylon/xsser) .&#x20;

### XSS Strike

Podemos clonar `XSS Strike` en nuestra máquina virtual con `git clone`:

```shell-session
afsh4ck@kali$ git clone https://github.com/s0md3v/XSStrike.git
afsh4ck@kali$ cd XSStrike
afsh4ck@kali$ pip install -r requirements.txt
afsh4ck@kali$ python xsstrike.py
```

Luego podemos ejecutar el script y proporcionarle una URL con el parámetro `-u`. Intentemos usarlo con nuestro ejemplo `Reflected XSS` de la sección anterior:

```shell-session
afsh4ck@kali$ python xsstrike.py -u "http://SERVER_IP:PORT/index.php?task=test" 

        XSStrike v3.1.4

[~] Checking for DOM vulnerabilities 
[+] WAF Status: Offline 
[!] Testing parameter: task 
[!] Reflections found: 1 
[~] Analysing reflections 
[~] Generating payloads 
[!] Payloads generated: 3072 
------------------------------------------------------------
[+] Payload: <HtMl%09onPoIntERENTER+=+confirm()> 
[!] Efficiency: 100 
[!] Confidence: 10 
[?] Would you like to continue scanning? [y/N]
```

Como podemos ver, la herramienta identificó el parámetro como vulnerable a XSS desde el primer payload.

***

## <mark style="color:purple;">Descubrimiento manual</mark>

En lo que respecta al descubrimiento manual de XSS, la dificultad de encontrar la vulnerabilidad XSS depende del nivel de seguridad de la aplicación web. Las vulnerabilidades XSS básicas se pueden encontrar normalmente probando varias cargas útiles XSS, pero la identificación de vulnerabilidades XSS avanzadas requiere habilidades avanzadas de revisión de código.

***

### **Payloads XSS**

El método más básico para buscar vulnerabilidades XSS es probar manualmente varios payloads XSS en un campo de entrada de una página web determinada. Podemos encontrar enormes listas de cargas útiles XSS en línea, como la de [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md) o la de [PayloadBox](https://github.com/payloadbox/xss-payload-list) . Luego podemos comenzar a probar estas cargas útiles una por una copiando cada una y añadiéndolas a nuestro formulario, y viendo si aparece un cuadro de alerta.

{% hint style="info" %}
**Nota**: XSS se puede inyectar en cualquier entrada en la página HTML, lo que no es exclusivo de los campos de entrada HTML, sino que también puede estar en encabezados HTTP como Cookie o User-Agent (es decir, cuando sus valores se muestran en la página).
{% endhint %}

Notarás que la mayoría de los payloads mencionados anteriormente no funcionan con nuestras aplicaciones web de ejemplo, a pesar de que estamos tratando con el tipo más básico de vulnerabilidades XSS. Esto se debe a que estos payloads están escritos para una amplia variedad de puntos de inyección (como la inyección después de una comilla simple) o están diseñadas para evadir ciertas medidas de seguridad (como filtros de sanitización). Además, dichos payloads utilizan una variedad de vectores de inyección para ejecutar código JavaScript, como etiquetas `<script>` básicas, otros `HTML Attributes` como `<img>`, o incluso atributos `CSS Style`. Es por eso que podemos esperar que muchos de estos payloads no funcionen en todos los casos de prueba, ya que están diseñadas para funcionar con ciertos tipos de inyecciones.

Por eso no resulta muy eficiente recurrir a copiar y pegar manualmente los payloads XSS, ya que, incluso si una aplicación web es vulnerable, puede llevarnos un tiempo identificar la vulnerabilidad, especialmente si tenemos muchos campos de entrada para probar. Por eso puede resultar más eficiente escribir nuestro propio script de Python para automatizar el envío de estos payloads y luego comparar el código fuente de la página para ver cómo se renderizaron nuestros payloads. Esto puede ayudarnos en casos avanzados en los que las herramientas XSS no pueden enviar y comparar fácilmente los payloads. De esta manera, tendríamos la ventaja de personalizar nuestra herramienta para nuestra aplicación web de destino. Sin embargo, este es un enfoque avanzado para el descubrimiento de XSS y no forma parte del alcance de este módulo.

En la siguiente sección muestro una selección de Payloads XSS que nos pueden resultar útiles:

{% content-ref url="/pages/L0KjWOwTnEfFteinfjfK" %}
[XSS Payloads](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss/xss-payloads.md)
{% endcontent-ref %}

***

### Revisión de código

El método más fiable para detectar vulnerabilidades XSS es la revisión manual del código, que debería abarcar tanto el código de back-end como el de front-end. Si comprendemos con precisión cómo se gestiona nuestra entrada hasta que llega al navegador web, podemos escribir una carga útil personalizada que debería funcionar con gran fiabilidad.

En la sección anterior, analizamos un ejemplo básico de revisión de código HTML al analizar las vulnerabilidades XSS `Source` y `Sink` basadas en DOM. Esto nos permitió ver rápidamente cómo funciona la revisión de código de frontend para identificar vulnerabilidades XSS, aunque en un ejemplo de frontend muy básico.

Es poco probable que encontremos vulnerabilidades XSS a través de listas de payloads o herramientas XSS para las aplicaciones web más comunes. Esto se debe a que los desarrolladores de dichas aplicaciones web probablemente ejecuten sus aplicaciones a través de herramientas de evaluación de vulnerabilidades y luego parcheen las vulnerabilidades identificadas antes del lanzamiento. Para tales casos, la revisión manual del código puede revelar vulnerabilidades XSS no detectadas, que pueden sobrevivir a los lanzamientos públicos de aplicaciones web comunes. Estas también son técnicas avanzadas que están fuera del alcance de este módulo.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.49.212:42651
```

<figure><img src="/files/fckAmkcW1TYMBJSlW1Sd" alt=""><figcaption></figcaption></figure>

### Pregunta 1

Utilice algunas de las técnicas mencionadas en esta sección para identificar el parámetro de entrada vulnerable que se encuentra en el servidor mencionado anteriormente. ¿Cuál es el nombre del parámetro vulnerable?

Al introducir los datos de registro vemos que se almacenan como parámetros en la URL de esta manera:

```
http://94.237.49.212:42651/?fullname=test&username=test&password=test&email=test%40test.es
```

Vamos a usar XSS Strike para ver que detecta:

```
python3 xsstrike.py -u 'http://94.237.49.212:42651/?fullname=test&username=test&password=test&email=test%40test.es'

	XSStrike v3.1.5

[~] Checking for DOM vulnerabilities 
[+] WAF Status: Offline 
[!] Testing parameter: fullname 
[-] No reflection found 
[!] Testing parameter: username 
[-] No reflection found 
[!] Testing parameter: password 
[-] No reflection found 
[!] Testing parameter: email 
[!] Reflections found: 1 
[~] Analysing reflections 
[~] Generating payloads 
[!] Payloads generated: 3072 
------------------------------------------------------------
[+] Payload: <D3v%09ONPoINTereNteR%0a=%0aconfirm()%0dx>v3dm0s 
[!] Efficiency: 100 
[!] Confidence: 10 
[?] Would you like to continue scanning? [y/N] y
```

Vemos que XSS Strike nos detecta la vulnerabilidad desde el primer payload, concretamente en el parámetro `email`.

### Pregunta 2

¿Qué tipo de XSS se encontró en el servidor mencionado anteriormente? "solo nombre"

```
[!] Testing parameter: email 
[!] Reflections found: 1 
```

Concretamente es una vulnerabilidad XSS Reflected
