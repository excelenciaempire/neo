
# PHP Webshell

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

***

## <mark style="color:purple;">Webshells en PHP</mark>

[PHP](https://www.php.net/) es un lenguaje de programación de código abierto y de propósito general que normalmente se utiliza como parte de un web stack que impulsa un sitio web. En el momento de escribir este artículo (octubre de 2021), PHP es el archivo `server-side programming language`. Según una [encuesta reciente](https://w3techs.com/technologies/details/pl-php) realizada por W3Techs, "PHP es utilizado por `78.6%`todos los sitios web cuyo lenguaje de programación del lado del servidor conocemos".

Consideremos un ejemplo práctico de cómo completar los campos de cuenta de usuario y contraseña en un formulario web de inicio de sesión.

### **Página de Login PHP**

![imagen](https://academy.hackthebox.com/storage/modules/115/rconfig.png)

¿Recuerda el servidor rConfig de antes en este módulo? Utiliza PHP. Podemos ver un archivo `login.php`. Entonces, cuando seleccionamos el botón de inicio de sesión después de completar el campo Nombre de usuario y Contraseña, esa información se procesa en el lado del servidor usando PHP. Saber que un servidor web utiliza PHP nos da a los pentesters una pista de que podemos obtener un shell web basado en PHP en este sistema. Analicemos este concepto de forma práctica.

***

## <mark style="color:purple;">Práctica con un webshell en PHP</mark>

Dado que PHP procesa código y comandos en el lado del servidor, podemos usar cargas útiles preescritas para obtener un shell a través del navegador o iniciar una sesión de shell inversa con nuestro cuadro de ataque. En este caso, aprovecharemos la vulnerabilidad en rConfig 3.9.6 para cargar manualmente un shell web PHP e interactuar con el host Linux subyacente. Además de todas las funciones mencionadas anteriormente, rConfig permite a los administradores agregar dispositivos de red y clasificarlos por proveedor. Continua e inicie sesión en rConfig con las credenciales predeterminadas (`admin:admin`), luego navegue hasta `Devices`> `Vendors`y haz clic en `Add Vendor`.

### **Pestaña Vendors**

![imagen](https://academy.hackthebox.com/storage/modules/115/vendors_tab.png)

### PHP Webshell

{% embed url="<https://github.com/WhiteWinterWolf/wwwolf-php-webshell>" %}

Podemos descargar esto o copiar y pegar el código fuente en un archivo `.php`. Tenga en cuenta que el tipo de archivo es importante, como pronto veremos. Nuestro objetivo es cargar el webshell en PHP a través del botón `browse`. Intentar hacer esto inicialmente fallará ya que rConfig está verificando el tipo de archivo. Sólo permitirá cargar tipos de archivos de imagen (.png,.jpg,.gif, etc.). Sin embargo, podemos evitar esto utilizando `Burp Suite`.

Inicie Burp Suite, navegue hasta el menú de configuración de red del navegador y complete la configuración del proxy. `127.0.0.1`irá al campo de dirección IP y `8080`al campo de puerto para garantizar que todas las solicitudes pasen a través de Burp (recuerde que Burp actúa como proxy web).

### **Configuración de proxy**

![imagen](https://academy.hackthebox.com/storage/modules/115/proxy_settings.png)

Nuestro objetivo es cambiar `content-type` para evitar la restricción del tipo de archivo al cargar archivos para que se "presenten" como el logotipo del proveedor para que podamos navegar hasta ese archivo y tener nuestro shell web.

***

## <mark style="color:purple;">Omitir la restricción del tipo de archivo</mark>

Con Burp abierto y la configuración del proxy de nuestro navegador web configurada correctamente, ahora podemos cargar el webshell PHP. Haga clic en el botón Examinar, navegue hasta donde esté almacenado nuestro archivo .php en nuestro equipo de atacante y seleccione abrir y `Save`(es posible que debamos aceptar el certificado PortSwigger). Parecerá que la página web está colgada, pero eso es sólo porque necesitamos decirle a Burp que reenvíe las solicitudes HTTP. Reenvíe las solicitudes hasta que vea la solicitud POST que contiene nuestra carga de archivos. Se verá así:

### **Solicitud POST**

![Eructar](https://academy.hackthebox.com/storage/modules/115/burp.png)

Como se mencionó en una sección anterior, notará que algunos payloads tienen comentarios del autor que explican su uso y enlaces a blogs personales. Esto puede delatarnos, por lo que no siempre es mejor dejar los comentarios en su lugar. Cambiaremos el tipo de contenido de `application/x-php`a `image/gif`. Básicamente, esto "engañará" al servidor y nos permitirá cargar el archivo .php, evitando la restricción del tipo de archivo. Una vez que hagamos esto, podemos seleccionar `Forward` dos veces y se enviará el archivo. Podemos apagar el interceptor Burp ahora y volver al navegador para ver los resultados.

### **Proveedor agregado**

![Eructar](https://academy.hackthebox.com/storage/modules/115/added_vendor.png)

El mensaje: "`Se agregó un nuevo proveedor NetVen a la base de datos`" nos informa que la carga de nuestro archivo se realizó correctamente. También podemos ver la entrada del proveedor de NetVen con el logotipo que muestra un trozo de papel rasgado. Esto significa que rConfig no reconoció el tipo de archivo como una imagen, por lo que utilizó esa imagen de forma predeterminada. Ahora podemos intentar utilizar nuestro shell web. Usando el navegador, navegue hasta este directorio en el servidor rConfig:

`/images/vendor/connect.php`

Esto ejecuta el payload y nos proporciona una sesión de shell no interactiva completamente en el navegador, lo que nos permite ejecutar comandos en el sistema operativo subyacente.

### **Éxito del webshell**

![imagen](https://academy.hackthebox.com/storage/modules/115/web_shell_now.png)

***

## <mark style="color:purple;">P0wny-Shell</mark>

{% embed url="<https://github.com/flozz/p0wny-shell>" %}

Es un shell PHP muy básico de un solo archivo. Se puede utilizar para ejecutar rápidamente comandos en un servidor al realizar pruebas de una aplicación PHP. Úsalo con precaución: este script representa un riesgo de seguridad para el servidor.

**Características:**

* Historial de comandos (usando las teclas de flecha `↑` `↓`)
* Autocompletar de comandos y nombres de archivos (usando `Tab`)
* Navegar en el sistema de archivos remoto (usando el comando `cd`)
* Cargar un archivo al servidor (usando el comando `upload <destination_file_name>`)
* Descargar un archivo del servidor (usando el comando `download <file_name>`)

<figure><img src="/files/PuWW2Bxvp1nfmEWYA710" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Consideraciones al trabajar con webshells</mark>

Al utilizar web shells, considere los siguientes problemas potenciales que pueden surgir durante su proceso de prueba de penetración:

* Las aplicaciones web a veces eliminan archivos automáticamente después de un período predefinido
* La interactividad limitada con el sistema operativo en términos de navegación por el sistema de archivos, descarga y carga de archivos, encadenamiento de comandos puede no funcionar (por ejemplo `whoami && hostname`), lo que ralentiza el progreso, especialmente al realizar la enumeración. -Posible inestabilidad a través de un shell web no interactivo.
* Mayores posibilidades de dejar pruebas de que tuvimos éxito en nuestro ataque.

Dependiendo del tipo de interacción (es decir, un pentesting de caja negra), es posible que debamos intentar pasar desapercibidos y `camuflar nuestros pasos`. A menudo ayudamos a nuestros clientes a probar sus capacidades para detectar una amenaza real, por lo que debemos emular en la medida de lo posible los métodos que un atacante malintencionado puede intentar, incluido el intento de operar de forma sigilosa.&#x20;

Esto ayudará a nuestro cliente y nos evitará, a largo plazo, que se descubran archivos una vez finalizado el período de participación. En la mayoría de los casos, al intentar obtener una sesión de shell con un objetivo, sería prudente establecer un shell inverso y luego eliminar el payload ejecutado. Además, debemos documentar cada método que intentamos, qué funcionó y qué no funcionó, e incluso los nombres de las cargas útiles y los archivos que intentamos utilizar. Podríamos incluir un hash sha1sum o MD5 del nombre del archivo, cargar ubicaciones en nuestros informes como prueba y proporcionar atribución.
