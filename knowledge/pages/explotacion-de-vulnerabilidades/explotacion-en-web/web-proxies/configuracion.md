
# Configuración

Tanto Burp como ZAP están disponibles para Windows, macOS y cualquier distribución de Linux.  Ambas herramientas están preinstaladas en distribuciones de Linux de pruebas de penetración como Parrot o Kali. Cubriremos el proceso de instalación y configuración de Burp y Zap en esta sección, lo que será útil si queremos instalar las herramientas en nuestra propia máquina virtual.

***

## <mark style="color:purple;">Burp Suite</mark>

Si Burp no está preinstalado en nuestra máquina virtual, podemos empezar descargándolo desde [la página de descargas de Burp](https://portswigger.net/burp/releases/) . Una vez descargado, podemos ejecutar el instalador y seguir las instrucciones, que varían de un sistema operativo a otro, pero deberían ser bastante sencillas. Hay instaladores para Windows, Linux y macOS.

También se puede instalar en Kali Linux con apt-get:

```shell-session
afsh4ck@kali$ sudo apt-get install burpsuite
```

Una vez instalado, Burp se puede ejecutar desde la terminal escribiendo `burpsuite`, o desde el menú de aplicaciones como se mencionó anteriormente. Otra opción es descargar el archivo `JAR` (que se puede usar en todos los sistemas operativos con un Java Runtime Environment (JRE) instalado) desde la página de descargas anterior. Podemos ejecutarlo con la siguiente línea de comandos o haciendo doble clic en él:

```shell-session
afsh4ck@kali$ java -jar </path/to/burpsuite.jar>
```

{% hint style="info" %}
**Nota**: Tanto Burp como ZAP dependen de Java Runtime Environment para ejecutarse, pero este paquete debería estar incluido en el instalador de forma predeterminada. En caso contrario, podemos seguir las instrucciones que se encuentran en esta [página](https://docs.oracle.com/goldengate/1212/gg-winux/GDRAD/java.htm) .
{% endhint %}

Una vez que iniciamos Burp, se nos solicita que creemos un nuevo proyecto. Si estamos ejecutando la versión comunitaria, solo podremos usar proyectos temporales sin la posibilidad de guardar nuestro progreso y continuar más tarde:

![Proyecto comunitario Burp](https://academy.hackthebox.com/storage/modules/110/burp_project_community.jpg)

Si utilizamos la versión pro/enterprise, tendremos la opción de iniciar un nuevo proyecto o abrir un proyecto existente.

![Proyecto Burp Pro](https://academy.hackthebox.com/storage/modules/110/burp_project_prof.jpg)

Es posible que necesitemos guardar nuestro progreso si estamos realizando pruebas de penetración en aplicaciones web enormes o ejecutando un `Active Web Scan`. Sin embargo, es posible que no necesitemos guardar nuestro progreso y, en muchos casos, podemos comenzar un proyecto `temporal` cada vez.

Entonces, seleccionemos `temporary project` y hagamos clic en continuar. Una vez que lo hagamos, se nos solicitará que usemos `Burp Default Configurations` o `Load a Configuration File` y elegiremos la primera opción:

![Configuración del proyecto Burp](https://academy.hackthebox.com/storage/modules/110/burp_project_config.jpg)

Una vez que comencemos a utilizar las funciones de Burp de forma intensiva, es posible que queramos personalizar nuestras configuraciones y cargarlas al iniciar Burp. Por ahora, podemos mantener `Use Burp Defaults`, y `Start Burp`. Una vez que hayamos hecho todo esto, deberíamos estar listos para comenzar a usar Burp.

***

## <mark style="color:purple;">ZAP</mark>

Podemos descargar ZAP desde su [página de descargas](https://www.zaproxy.org/download/) , elegir el instalador que se adapte a nuestro sistema operativo y seguir las instrucciones básicas de instalación para instalarlo. ZAP también se puede descargar como un archivo JAR multiplataforma y ejecutarlo con el comando `java -jar` o haciendo doble clic sobre él, de forma similar a Burp.

También se puede instalar en Kali Linux con apt-get:

```shell-session
afsh4ck@kali$ sudo apt-get install zaproxy
```

Para empezar a utilizar ZAP, podemos iniciarlo desde la terminal con el comando `zaproxy` o acceder a él desde el menú de aplicaciones como Burp. Una vez que se inicia ZAP, a diferencia de la versión gratuita de Burp, se nos solicitará que creemos un nuevo proyecto o un proyecto temporal. Usemos un proyecto temporal eligiendo `no`, ya que no trabajaremos en un gran proyecto que necesitaremos mantener durante varios días:

<figure><img src="/files/iMSABtTRdrl5jtVkdgbZ" alt=""><figcaption></figcaption></figure>

Después de eso, tendremos ZAP ejecutándose y podremos continuar con el proceso de configuración del proxy, como discutiremos en la siguiente sección.

{% hint style="info" %}
**Consejo**: Si prefieres usar un tema oscuro, puedes hacerlo en Burp yendo a ( `User Options > Display`) y seleccionando "Dark" debajo de (`theme`), y en ZAP yendo a ( `Herramientas > Opciones > Mostrar`) y seleccionando "Flat Dark" en ( `Apariencia`).
{% endhint %}

<figure><img src="/files/VGlcGoFdczQy61Z9Rofz" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Configurar Web Proxy</mark>

Ahora que hemos instalado e iniciado ambas herramientas, aprenderemos a utilizar la función más utilizada `Web Proxy`;

Podemos configurar estas herramientas como proxy para cualquier aplicación, de modo que todas las solicitudes web se enruten a través de ellas para que podamos examinar manualmente qué solicitudes web envía y recibe una aplicación. Esto nos permitirá comprender mejor lo que hace la aplicación en segundo plano y nos permitirá interceptar y cambiar estas solicitudes o reutilizarlas con varios cambios para ver cómo responde la aplicación.

***

### Navegador preconfigurado

Para utilizar las herramientas como servidores proxy web, debemos configurar los ajustes de proxy de nuestro navegador para utilizarlas como proxy o utilizar el navegador preconfigurado. Ambas herramientas cuentan con un navegador preconfigurado que viene con ajustes de proxy preconfigurados y los certificados CA preinstalados, lo que hace que iniciar una prueba de penetración web sea muy rápido y fácil.

En Burp Suite ( `Proxy > Intercept`), podemos hacer clic en `Open Browser`, lo que abrirá el navegador preconfigurado de Burp y enrutará automáticamente todo el tráfico web a través de Burp:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/110/burp_preconfigured_browser.jpg" alt=""><figcaption></figcaption></figure>

En ZAP, podemos hacer clic en el icono del navegador Firefox al final de la barra superior, y se abrirá el navegador preconfigurado:

![Navegador preconfigurado ZAP](https://academy.hackthebox.com/storage/modules/110/zap_preconfigured_browser.jpg)

Para nuestros usos en este módulo, utilizar el navegador preconfigurado debería ser suficiente.

***

### Configuración de Proxy

En muchos casos, es posible que queramos utilizar un navegador real para realizar pruebas de penetración, como Firefox. Para utilizar Firefox con nuestras herramientas de proxy web, primero debemos configurarlo para que las utilice como proxy. Podemos ir manualmente a las preferencias de Firefox y configurar el proxy para que utilice el puerto de escucha del proxy web. Tanto Burp como ZAP utilizan el puerto `8080`de forma predeterminada, pero podemos utilizar cualquier puerto disponible. Si elegimos un puerto que esté en uso, el proxy no se iniciará y recibiremos un mensaje de error.

{% hint style="info" %}
**Nota**: En caso de que quisiéramos servir el proxy web en un puerto diferente, podemos hacerlo en Burp en ( `Proxy>Options`), o en ZAP en ( `Tools>Options>Local Proxies`). En ambos casos, debemos asegurarnos de que el proxy configurado en Firefox utilice el mismo puerto.
{% endhint %}

En lugar de cambiar el proxy manualmente, podemos utilizar la extensión de Firefox [Foxy Proxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/) para cambiar el proxy de Firefox de forma fácil y rápida. Esta extensión se puede instalar en su propio navegador Firefox visitando la [página de extensiones de Firefox](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/) (también sirve para Chrome) y haciendo clic en `Add to Firefox` para instalarla.

Una vez que tengamos la extensión agregada, podemos configurar el proxy web en ella haciendo clic en su ícono en la barra superior de Firefox y luego eligiendo `options`:

![Opciones de Foxyproxy](https://academy.hackthebox.com/storage/modules/110/foxyproxy_options.jpg)

Una vez que estemos en `options`, podemos hacer clic en `add` en el panel izquierdo y luego usar `127.0.0.1` como IP y `8080` como puerto y nombrarlo `Burp` o `ZAP`:

![Foxyproxy Agregar](https://academy.hackthebox.com/storage/modules/110/foxyproxy_add.jpg)

Por último, podemos hacer clic en el icono de `Foxy Proxy` y seleccionar `Burp`/ `ZAP`.&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/110/foxyproxy_use.jpg" alt=""><figcaption></figcaption></figure>

***

### Instalación del certificado CA

Otro paso importante al utilizar Burp Proxy/ZAP con nuestro navegador es instalar los certificados CA del proxy web. Si no realizamos este paso, es posible que parte del tráfico HTTPS no se enrute correctamente o que tengamos que hacer clic en `aceptar` cada vez que Firefox necesite enviar una solicitud HTTPS.

Podemos instalar el certificado de Burp una vez que seleccionemos Burp como nuestro proxy en `Foxy Proxy`, navegando a `http://burp`, y descargando el certificado desde allí haciendo clic en `CA Certificate`:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/burp_cert.jpg" alt=""><figcaption></figcaption></figure>

Para obtener el certificado de ZAP, podemos ir a ( `Tools>Options>Dynamic SSL Certificate`), luego hacer clic en `Save`:

![Certificado ZAP](https://academy.hackthebox.com/storage/modules/110/zap_cert.jpg)

También podemos cambiar nuestro certificado generando uno nuevo con el botón `Generate`.

Una vez que tengamos nuestros certificados, podemos instalarlos dentro de Firefox navegando a <about:preferences#privacy> , desplazándonos hasta la parte inferior y haciendo clic en `View Certificates`:

![Certificado Firefox](https://academy.hackthebox.com/storage/modules/110/firefox_cert.jpg)

Después de eso, podemos seleccionar la pestaña `Authorities` y luego hacer clic en `import` y seleccionar el certificado CA descargado:

![Importar certificado de Firefox](https://academy.hackthebox.com/storage/modules/110/firefox_import_cert.jpg)

Por último debemos seleccionar `Trust this CA to identify websites` y `Trust this CA to identify email users` y luego hacer clic en Aceptar:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/firefox_trust_cert.jpg" alt=""><figcaption></figcaption></figure>

Una vez que instalamos el certificado y configuramos el proxy de Firefox, todo el tráfico web de Firefox comenzará a enrutarse a través de nuestro proxy web.
