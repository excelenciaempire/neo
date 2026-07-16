
# Detección

## <mark style="color:purple;">Detección de Command Injection</mark>

***

El proceso de detección de vulnerabilidades básicas de inyección de comandos del sistema operativo es el mismo proceso para explotar dichas vulnerabilidades. Intentamos agregar nuestro comando a través de varios métodos de inyección. Si el resultado del comando cambia con respecto al resultado habitual previsto, hemos explotado la vulnerabilidad con éxito.&#x20;

Esto puede no ser cierto para vulnerabilidades de inyección de comandos más avanzadas porque podemos utilizar varios métodos de fuzzing o revisiones de código para identificar posibles vulnerabilidades de inyección de comandos. Luego, podemos construir gradualmente nuestra carga útil hasta lograr la inyección de comandos.

Este módulo se centrará en las inyecciones de comandos básicas, donde controlamos la entrada del usuario que se usa directamente en una función de ejecución de comando del sistema sin ningún tipo de desinfección.

Para demostrarlo, utilizaremos el ejercicio que se encuentra al final de esta sección.

***

### Detección de inyección de comandos

Cuando visitamos la aplicación web en el siguiente ejercicio, vemos una utilidad `Host Checker` que parece pedirnos una IP para comprobar si está viva o no:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_basic_exercise_1.jpg" alt=""><figcaption></figcaption></figure>

Podemos intentar ingresar la IP del host local `127.0.0.1` para verificar la funcionalidad y, como se esperaba, devuelve la salida del comando `ping` que nos dice que el host local está efectivamente activo:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_basic_exercise_2.jpg" alt=""><figcaption></figcaption></figure>

Aunque no tenemos acceso al código fuente de la aplicación web, podemos suponer con seguridad que la IP que ingresamos va a un comando `ping` ya que el resultado que recibimos así lo sugiere. Como el resultado muestra un solo paquete transmitido en el comando ping, el comando utilizado puede ser el siguiente:

```bash
ping -c 1 OUR_INPUT
```

Si no se desinfecta ni se escapa nuestra entrada antes de usarla con el comando `ping`, es posible que podamos inyectar otro comando arbitrario. Por lo tanto, intentemos ver si la aplicación web es vulnerable a la inyección de comandos del sistema operativo.

***

### Métodos de inyección de comandos

Para inyectar un comando adicional al deseado, podemos utilizar cualquiera de los siguientes operadores:

<table data-header-hidden><thead><tr><th width="157"></th><th width="130"></th><th width="172"></th><th></th></tr></thead><tbody><tr><td><strong>Operador de inyección</strong></td><td><strong>Carácter de inyección</strong></td><td><strong>Carácter codificado en URL</strong></td><td><strong>Comando ejecutado</strong></td></tr><tr><td>Punto y coma</td><td><code>;</code></td><td><code>%3b</code></td><td>Ambos</td></tr><tr><td>Nueva linea</td><td></td><td><code>%0a</code></td><td>Ambos</td></tr><tr><td>Background</td><td><code>&#x26;</code></td><td><code>%26</code></td><td>Ambos (la segunda salida generalmente se muestra primero)</td></tr><tr><td>Pipe</td><td><code>|</code></td><td><code>%7c</code></td><td>Ambos (solo se muestra la segunda salida)</td></tr><tr><td>AND</td><td><code>&#x26;&#x26;</code></td><td><code>%26%26</code></td><td>Ambos (solo si el primero tiene éxito)</td></tr><tr><td>OR</td><td><code>||</code></td><td><code>%7c%7c</code></td><td>Segundo (solo si falla el primero)</td></tr><tr><td>Sub-Shell</td><td><code>``</code></td><td><code>%60%60</code></td><td>Ambos (solo Linux)</td></tr><tr><td>Sub-Shell</td><td><code>$()</code></td><td><code>%24%28%29</code></td><td>Ambos (solo Linux)</td></tr></tbody></table>

Podemos usar cualquiera de estos operadores para inyectar otro comando para que se ejecuten ambos o cualquiera de los comandos. Escribiríamos nuestra entrada esperada (por ejemplo, una IP), luego usaríamos cualquiera de los operadores anteriores y luego escribiríamos nuestro nuevo comando.

{% hint style="success" %}
**Consejo**: Además de lo anterior, hay algunos operadores exclusivos de Unix que funcionarían en Linux y macOS, pero no en Windows, como envolver nuestro comando inyectado con comillas dobles invertidas ( ` `` `) o con un operador de sub-shell ( `$()`).
{% endhint %}

En general, para la inyección de comandos básicos, todos estos operadores se pueden utilizar para inyecciones de comandos independientemente del lenguaje de la aplicación web, el marco o el servidor back-end. Entonces, si estamos inyectando una aplicación web PHP que se ejecuta en un servidor Linux, o una aplicación web .Net que se ejecuta en un servidor back-end de Windows, o una aplicación web NodeJS que se ejecuta en un servidor back-end de macOS, nuestras inyecciones deberían funcionar. a pesar de todo.

{% hint style="info" %}
Nota: La única excepción puede ser el punto y coma `;`, que no funcionará si el comando se ejecuta con `Windows Command Line (CMD)`, pero sí funcionará si se ejecuta con `Windows PowerShell`.
{% endhint %}

En la siguiente sección, intentaremos utilizar uno de los operadores de inyección anteriores para explotar el ejercicio `Host Checker`.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 83.136.254.158:34041
```

Intente agregar cualquiera de los operadores de inyección después de la dirección IP en el campo IP. ¿Qué decía el mensaje de error (en inglés)?

<figure><img src="/files/4VFgPRxe6gFbwKEZg0N4" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/AUB9gEq8YLcj9Z5Zf205" alt=""><figcaption></figcaption></figure>
