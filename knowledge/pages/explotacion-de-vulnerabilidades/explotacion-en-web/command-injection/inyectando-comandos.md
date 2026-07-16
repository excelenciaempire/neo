
# Inyectando comandos

## <mark style="color:purple;">Inyección de comandos</mark>

***

Hasta ahora, hemos descubierto que la aplicación web `Host Checker` es potencialmente vulnerable a las inyecciones de comandos y hemos analizado varios métodos de inyección que podemos utilizar para explotar la aplicación web. Por lo tanto, comencemos nuestros intentos de inyección de comandos con el operador de punto y coma ( `;`).

***

### Inyectando nuestro comando

Podemos agregar un punto y coma después de nuestra IP de entrada `127.0.0.1`y luego agregar nuestro comando (por ejemplo, `whoami`), de modo que la carga útil final que usaremos sea ( `127.0.0.1; whoami`), y el comando final a ejecutar sería:

```bash
ping -c 1 127.0.0.1; whoami
```

Primero, intentemos ejecutar el comando anterior en nuestra máquina virtual Linux para asegurarnos de que se ejecute:

```shell-session
afsh4ck@kali$ ping -c 1 127.0.0.1; whoami
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.055 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.055/0.055/0.055/0.000 ms
kali
```

Como podemos ver, el comando final se ejecuta correctamente y obtenemos el resultado de ambos comandos (como se mencionó en la tabla anterior para `;`). Ahora, podemos intentar usar nuestra carga útil anterior en la aplicación web `Host Checker`:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_basic_injection.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, la aplicación web rechazó nuestra entrada, ya que parece que solo acepta entradas en formato IP. Sin embargo, por el aspecto del mensaje de error, parece que se origina en el front-end en lugar del back-end. Podemos comprobarlo haciendo click en `Firefox Developer Tools` o `[CTRL + SHIFT + E]` para mostrar la pestaña Red y luego haciendo clic en el botón `Check` nuevamente:

![Inyección básica](https://academy.hackthebox.com/storage/modules/109/cmdinj_basic_injection_network.jpg)

Como podemos ver, no se realizaron nuevas solicitudes de red cuando hicimos clic en el botón Check, pero recibimos un mensaje de error. Esto indica que la validación de la entrada del usuario se está realizando en el `front-end`.

Esto parece ser un intento de evitar que enviemos cargas útiles maliciosas al permitir únicamente la entrada del usuario en formato IP. Sin embargo, es muy común que los desarrolladores solo realicen la validación de entradas en el front-end y no validen ni desinfecten las entradas en el back-end. Esto ocurre por varias razones, como tener dos equipos diferentes trabajando en el front-end/back-end o confiar en la validación del front-end para evitar cargas útiles maliciosas.

Sin embargo, como veremos, las validaciones del front-end generalmente no son suficientes para evitar las inyecciones, ya que se pueden eludir muy fácilmente enviando solicitudes HTTP personalizadas directamente al back-end.

***

### Cómo eludir la validación del front-end

El método más sencillo para personalizar las solicitudes HTTP que se envían al servidor back-end es utilizar un proxy web que pueda interceptar las solicitudes HTTP que envía la aplicación. Para ello, podemos iniciar `Burp Suite` o `ZAP` y configurar Firefox para que procese el tráfico a través de ellos. A continuación, podemos habilitar la función de intercepción de proxy, enviar una solicitud estándar desde la aplicación web con cualquier IP (por ejemplo `127.0.0.1`, ) y enviar la solicitud HTTP interceptada a `repeater` haciendo clic en `[CTRL + R]`, y deberíamos tener la solicitud HTTP para personalizar:

#### **Solicitud de POST de Burp**

![Inyección básica](https://academy.hackthebox.com/storage/modules/109/cmdinj_basic_repeater_1.jpg)

Ahora podemos personalizar nuestra solicitud HTTP y enviarla para ver cómo la maneja la aplicación web. Comenzaremos usando la misma carga útil anterior ( `127.0.0.1; whoami`). También deberíamos codificar la URL de nuestra carga útil para asegurarnos de que se envíe como queremos. Podemos hacerlo seleccionando la carga útil y luego haciendo clic en `[CTRL + U]`. Finalmente, podemos hacer clic en `Send` para enviar nuestra solicitud HTTP:

#### **Solicitud de POST de Burp**

![Inyección básica](https://academy.hackthebox.com/storage/modules/109/cmdinj_basic_repeater_2.jpg)

Como podemos ver, la respuesta que obtuvimos esta vez contiene el resultado del comando ping y el resultado del comando whoami, lo que significa que inyectamos con éxito nuestro nuevo comando.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 83.136.254.158:34041
```

Revise el código fuente HTML de la página para encontrar dónde se realiza la validación de entrada del frontend. ¿En qué número de línea se encuentra?

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>Host Checker</title>
  <link rel="stylesheet" href="./style.css">

</head>

<body>
  <div class="main">
    <h1>Host Checker</h1>

    <form method="post" action="">
      <label>Enter an IP Address</label>
      <input type="text" name="ip" placeholder="127.0.0.1" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$">
      <button type="submit">Check</button>
    </form>

    <p>
    <pre>
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.014 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.014/0.014/0.014/0.000 ms
</pre>
    </p>

  </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js'></script>
</body>

</html>
```

Concretamente en la línea 17 observamos el input que hace la validación:

```html
<input type="text" name="ip" placeholder="127.0.0.1" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$">
```

Como ya hemos visto podemos eludir esto con BurpSuite añadiendo el parámetro codificado y enviando la petición al Repeater:

<figure><img src="/files/dYQAMiGzK1BorrhUp4sp" alt=""><figcaption></figcaption></figure>
