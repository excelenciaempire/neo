
# Herramientas de Crawling

## <mark style="color:purple;">OWASP ZAP</mark>

[Zed Attack Proxy](https://www.zaproxy.org/) (`ZAP`) es un proxy web de código abierto que pertenece al [Open Web Application Security Project](https://owasp.org/) (`OWASP`). Nos permite realizar pruebas de seguridad manuales y automatizadas en aplicaciones web. Una de sus mejores funcionalidades es la de spider y fuzzer, y podemos utilizarlo también como un proxy para interceptar y manipular todo el tráfico que pasa por él.&#x20;

### Instalación

```bash
sudo apt install -y zaproxy
```

### Ejecución

Una vez que ZAP esté instalado, puedes iniciarlo desde la terminal utilizando el comando `zaproxy`. Hay dos formas comunes de ejecutar ZAP: interfaz gráfica y línea de comandos.

**Interfaz Gráfica:**

Para abrir la interfaz gráfica de ZAP, simplemente escribe `zaproxy` en la terminal y presiona Enter:

```bash
zaproxy
```

Esto iniciará la interfaz gráfica de usuario de ZAP, donde podrás interactuar con todas las características y herramientas que ofrece.

**Línea de Comandos:**

Si prefieres utilizar ZAP desde la línea de comandos, puedes ejecutarlo en modo demonio utilizando el siguiente comando:

```bash
zaproxy -daemon
```

Podemos utilizar la funcionalidad de `spidering` siguiendo los siguientes pasos. Abra ZAP y, en la esquina superior derecha, abra el navegador.

![imagen](https://academy.hackthebox.com/storage/modules/144/zap1.png)

Escriba el sitio web en la barra de direcciones y agréguelo al alcance usando la primera entrada en el menú de la izquierda.

![imagen](https://academy.hackthebox.com/storage/modules/144/zap2.png)

Regrese a la ventana ZAP, haga clic derecho en el sitio web de destino, haga clic en el menú Ataque y luego en el submenú Spider.

<figure><img src="/files/WE06i7MIdXHktAluqbRB" alt=""><figcaption></figcaption></figure>

Una vez finalizado el proceso podremos ver los recursos descubiertos por el proceso de spidering.

<figure><img src="/files/NZxGuiq2wdGrUNoK68OR" alt=""><figcaption></figcaption></figure>

Una característica útil de ZAP es el `Fuzzer integrado` y el `Editor de solicitudes` manuales. Podemos enviarles cualquier solicitud para modificarla manualmente o mezclarla con una lista de payloads haciendo clic derecho en la solicitud y usando el menú "Abrir/Reenviar con el editor de solicitudes..." o el submenú "Fuzz..." en el menú Ataque.

<figure><img src="/files/aeUbhWxo3MEXdsguzsUn" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/MOrlj40PvVcW3J57WOKB" alt=""><figcaption></figcaption></figure>

ZAP tiene [una documentación](https://www.zaproxy.org/docs/desktop/start/) excelente que puede ayudarte a entender mejor este programa y sus funciones.

***

## <mark style="color:purple;">Ffuf</mark>

El módulo Spider de ZAP solo enumera los recursos que encuentra en enlaces y formularios, pero puede omitir información importante como carpetas ocultas o archivos de backup.

Podemos usar [ffuf](https://github.com/ffuf/ffuf) para descubrir archivos y carpetas que no podemos detectar simplemente navegando por el sitio web. Todo lo que tenemos que hacer es iniciar `ffuf` con una lista de nombres de carpetas e indicarle que las busque de forma recursiva.

```bash
ffuf -recursion -recursion-depth 1 -u http://192.168.10.10/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-small-directories-lowercase.txt
```

```shell-session
afsh4ck@kali$ ffuf -recursion -recursion-depth 1 -u http://192.168.10.10/FUZZ -w /opt/useful/SecLists/Discovery/Web-Content/raft-small-directories-lowercase.txt

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.1.0-git
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.10.10/FUZZ
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/raft-small-directories-lowercase.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

wp-admin                [Status: 301, Size: 317, Words: 20, Lines: 10]
[INFO] Adding a new job to the queue: http://192.168.10.10/wp-admin/FUZZ

wp-includes             [Status: 301, Size: 320, Words: 20, Lines: 10]
[INFO] Adding a new job to the queue: http://192.168.10.10/wp-includes/FUZZ

wp-content              [Status: 301, Size: 319, Words: 20, Lines: 10]
[INFO] Adding a new job to the queue: http://192.168.10.10/wp-content/FUZZ

admin                   [Status: 302, Size: 0, Words: 1, Lines: 1]
login                   [Status: 302, Size: 0, Words: 1, Lines: 1]
feed                    [Status: 301, Size: 0, Words: 1, Lines: 1]
[INFO] Adding a new job to the queue: http://192.168.10.10/feed/FUZZ
...
```

* `-recursion`: Activa el escaneo recursivo.
* `-recursion-depth`: Especifica la profundidad máxima para escanear.
* `-u`: Nuestra URL de destino y `FUZZ` será el punto de inyección.
* `-w`: Ruta a nuestra lista de palabras.

Podemos ver en la imagen cómo `ffuf` crea nuevos trabajos para cada carpeta detectada. Esta tarea puede consumir muchos recursos para el servidor de destino. Si el sitio web responde más lento de lo habitual, podemos reducir la tasa de solicitudes utilizando el `-rate`parámetro.

El módulo [Atacar aplicaciones web con Ffuf](https://academy.hackthebox.com/course/preview/attacking-web-applications-with-ffuf) profundiza mucho más en `ffuf`el uso y muestra muchas de las técnicas que se enseñan en este módulo.

***

## <mark style="color:purple;">Katana</mark>

Katana es una herramienta de crawling por CLI que en vez de usar un diccionario para probar distintas rutas (cómo ffuf), navega directamente por el site devolviéndonos todas las rutas visibles y ocultas, mapeando por completo el sitio web.

{% embed url="<https://github.com/projectdiscovery/katana>" %}

<figure><img src="/files/3aLX9Iu9OWowMiS9TAIc" alt=""><figcaption></figcaption></figure>

#### Instalación

Necesitamos tener instalado go en Kali para la instalación:

```bash
CGO_ENABLED=1 go install github.com/projectdiscovery/katana/cmd/katana@latest

katana -h
```

#### Crawling básico

```bash
katana -u https://tesla.com
katana -u https://tesla.com -d 5  # Control de profundidad de Crawling
katana -u https://tesla.com -aff  # Autorelleno de formularios
```

#### Crawling desde archivo con URLs

```bash
cat url_list.txt

https://tesla.com
https://google.com
```

```bash
katana -list url_list.txt
```

#### Crawling autenticado

A continuación se muestra un ejemplo de cómo agregar una cookie a la solicitud:

```bash
katana -u https://tesla.com -H 'Cookie: usrsess=AmljNrESo'
```

También es posible proporcionar encabezados o cookies como archivo. Por ejemplo:

```bash
cat cookie.txt

Cookie: PHPSESSIONID=XXXXXXXXX
X-API-KEY: XXXXX
TOKEN=XX
```

```bash
katana -u https://tesla.com -H cookie.txt
```

***

## <mark style="color:purple;">Divulgación de información confidencial</mark>

Es típico que el servidor web y la aplicación web manejen los archivos que necesita para funcionar. Sin embargo, es común encontrar copias de seguridad o archivos sin referencia que pueden tener información o credenciales importantes. Se pueden generar archivos de respaldo o sin referencia mediante la creación de instantáneas, diferentes versiones de un archivo o desde un editor de texto sin el conocimiento del desarrollador web. Hay algunas listas de extensiones comunes que podemos encontrar en los `raft-[ small | medium | large ]-extensions.txt`archivos de [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content) .

Combinaremos algunas de las carpetas que hemos encontrado antes, una lista de extensiones comunes y algunas palabras extraídas del sitio web para ver si podemos encontrar algo que no debería estar allí. El primer paso será crear un archivo con los siguientes nombres de carpeta y guardarlo como `folders.txt`.

```shell-session
wp-admin
wp-content
wp-includes
```

A continuación, extraeremos algunas palabras clave del sitio web utilizando [CeWL](https://github.com/digininja/CeWL) . Le indicaremos a la herramienta que extraiga palabras con una longitud mínima de 5 caracteres `-m5`, las convierta a minúsculas `--lowercase`y las guarde en un archivo llamado wordlist.txt `-w <FILE>`:

```bash
cewl -m5 --lowercase -w wordlist.txt http://192.168.10.10
```

El siguiente paso será combinar todo en ffuf a ver si encontramos alguna información jugosa. Para ello utilizaremos los siguientes parámetros en `ffuf`:

* `-w`: Separamos las listas de palabras por coma y les agregamos un alias para inyectarlas como puntos de fusión más adelante
* `-u`: Nuestra URL de destino con los puntos borrosos.

```bash
ffuf -w ./folders.txt:FOLDERS,./wordlist.txt:WORDLIST,./extensions.txt:EXTENSIONS -u http://192.168.10.10/FOLDERS/WORDLISTEXTENSIONS
```

```shell-session
afsh4ck$ ffuf -w ./folders.txt:FOLDERS,./wordlist.txt:WORDLIST,./extensions.txt:EXTENSIONS -u http://192.168.10.10/FOLDERS/WORDLISTEXTENSIONS

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.1.0-git
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.10.10/FOLDERS/WORDLISTEXTENSIONS
 :: Wordlist         : FOLDERS: ./folders.txt
 :: Wordlist         : WORDLIST: ./wordlist.txt
 :: Wordlist         : EXTENSIONS: ./extensions.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

[Status: 200, Size: 8, Words: 1, Lines: 2]
    * EXTENSIONS: ~
    * FOLDERS: wp-content
    * WORDLIST: secret

[Status: 200, Size: 0, Words: 1, Lines: 1]
    * FOLDERS: wp-includes
    * WORDLIST: comment
    * EXTENSIONS: .php

[Status: 302, Size: 0, Words: 1, Lines: 1]
    * FOLDERS: wp-admin
    * WORDLIST: comment
    * EXTENSIONS: .php

...
```

```bash
afsh4ck$ curl http://192.168.10.10/wp-content/secret~

Oooops!
```

Siguiendo este enfoque, hemos encontrado con éxito un archivo secreto. 🏆

En el siguiente enlace podrás ir a la página de Ffuf, donde tratamos más en detalle esta herramienta:

{% content-ref url="/pages/27SGdsmGYGBRQvxKhO4z" %}
[Ffuf](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing/ffuf.md)
{% endcontent-ref %}
