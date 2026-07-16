
# Proxy: Skills Assestment

Estamos realizando pruebas de penetración internas para una empresa local. A medida que se topa con sus aplicaciones web internas, se le presentan diferentes situaciones en las que Burp/ZAP puede resultar útil. Lea cada uno de los escenarios de las preguntas a continuación y determine las características que serían más útiles para cada caso. Luego, utilícelas para ayudarlo a alcanzar el objetivo especificado.

```
Objetivo: 83.136.253.61:53806
```

### Pregunta 1

La página /lucky.php tiene un botón que parece estar deshabilitado. Intente habilitar el botón y luego haga clic en él para obtener la bandera.

<figure><img src="/files/jRXa4R8HBqcm5xhNvZAc" alt=""><figcaption></figcaption></figure>

Le damos click derecho > Inspeccionar, cambiamos el disabled por enabled, y le damos al botón para capturar la petición. Aquí le tendremos click unas 10 veces y aparece la flag:

<figure><img src="/files/QbQpXsTNcemGkgVYXfjv" alt=""><figcaption></figcaption></figure>

### Pregunta 2

La página /admin.php utiliza una cookie que ha sido codificada varias veces. Intente decodificar la cookie hasta que obtenga un valor de 31 caracteres. Envíe el valor como respuesta.

<figure><img src="/files/q2Vmifr6Libsipkacdra" alt=""><figcaption></figcaption></figure>

```
cookie=4d325268597a6b7a596a686a5a4449314d4746684f474d7859544d325a6d5a6d597a63355954453359513d3d
```

Empezamos a decodificar, primero en ASCII:

<figure><img src="/files/JvXICKnDgQGxFOcjG1Tl" alt=""><figcaption></figcaption></figure>

Y después en base64, y obtenemos la cadena de 31 caracteres:

<figure><img src="/files/RSlEIQrpqpxAl495ZN4R" alt=""><figcaption></figcaption></figure>

```
3dac93b8cd250aa8c1a36fffc79a17a
```

### Pregunta 3

Una vez que decodifique la cookie, notará que solo tiene 31 caracteres, lo que parece ser un hash md5 al que le falta el último carácter. Por lo tanto, intente realizar un fuzzing del último carácter de la cookie md5 decodificada con todos los caracteres alfanuméricos, mientras codifica cada solicitud con los métodos de codificación que identificó anteriormente. (Puede utilizar la lista de palabras "alphanum-case.txt" de Seclist para el payload)

Vamos a enviar la petición a `Intruder`:

<figure><img src="/files/fewBii93GI3MwFb1s8rR" alt=""><figcaption></figcaption></figure>

En la parte de Payloads configuramos lo siguiente:

<figure><img src="/files/o25qw14lF7VMd9SDxG6m" alt=""><figcaption></figcaption></figure>

Una vez que termina el fuzzing, vemos que hay una cookie con un tamaño de respuesta superior al resto:

<figure><img src="/files/8aDAhVApjfqGPlOhsm6w" alt=""><figcaption></figcaption></figure>

Entonces la copiamos, la cambiamos en el navegador desde click derecho > Inspeccionar > Stogare > Cookie, recargamos la página y aparece la flag:

<figure><img src="/files/a4qLp4bU4mwkwoHNfibj" alt=""><figcaption></figcaption></figure>

### Pregunta 4

Estás usando la herramienta '`auxiliary/scanner/http/coldfusion_locale_traversal`' dentro de Metasploit, pero no te está funcionando correctamente. Decide capturar la solicitud enviada por Metasploit para poder verificarla manualmente y repetirla. Una vez que capturas la solicitud, ¿cuál es el directorio 'XXXXX' al que se llama en '/XXXXX/administrator/..'?

Para capturar la petición con Burpsuite vamos a utilizar la opción:

```
set PROXIES http://127.0.0.1:8080
```

<figure><img src="/files/afaLwDwbD0SHiiPJnKtQ" alt=""><figcaption></figcaption></figure>
