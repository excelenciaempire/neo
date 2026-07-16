
# Bypass de filtros de espacios

Existen numerosas formas de detectar intentos de inyección y existen múltiples métodos para evitar estas detecciones. Demostraremos el concepto de detección y cómo funciona la omisión utilizando Linux como ejemplo. Aprenderemos cómo utilizar estas omisiones y, eventualmente, podremos prevenirlas. Una vez que comprendamos bien cómo funcionan, podemos consultar varias fuentes en Internet para descubrir otros tipos de omisiones y aprender cómo mitigarlas.

***

## <mark style="color:purple;">Evitar operadores incluidos en la lista negra</mark>

Veremos que la mayoría de los operadores de inyección están en la lista negra. Sin embargo, el carácter de nueva línea no suele estarlo, ya que puede ser necesario en la carga útil en sí. Sabemos que el carácter de nueva línea funciona para agregar nuestros comandos tanto en Linux como en Windows, así que intentemos usarlo como nuestro operador de inyección:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_operator.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, aunque nuestra carga útil incluía un carácter de nueva línea, nuestra solicitud no fue denegada y obtuvimos el resultado del comando ping, lo que significa que este carácter no está en la lista negra y podemos usarlo como nuestro operador de inyección. Comencemos discutiendo cómo omitir un carácter comúnmente incluido en la lista negra: un carácter de espacio.

***

## <mark style="color:purple;">Evitar espacios en la lista negra</mark>

Ahora que tenemos un operador de inyección que funciona, modifiquemos nuestra carga útil original y enviémosla nuevamente como (`127.0.0.1%0a whoami`):&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_spaces_1.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, aún recibimos un mensaje de error `invalid input`, lo que significa que aún tenemos otros filtros que omitir. Por lo tanto, como hicimos antes, agreguemos solo el siguiente carácter (que es un espacio) y veamos si causó la solicitud rechazada:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_spaces_2.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, el carácter de espacio también está incluido en la lista negra. Un espacio es un carácter que se incluye comúnmente en la lista negra, especialmente si la entrada no debe contener ningún espacio, como una dirección IP, por ejemplo. Aun así, ¡existen muchas formas de agregar un carácter de espacio sin tener que usarlo!

### **Uso de tabulaciones**

El uso de tabulaciones (`%09`) en lugar de espacios es una técnica que puede funcionar, ya que tanto Linux como Windows aceptan comandos con tabulaciones entre argumentos y se ejecutan de la misma manera. Por lo tanto, intentemos usar una tabulación en lugar del carácter de espacio ( `127.0.0.1%0a%09`) y veamos si se acepta nuestra solicitud:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_spaces_3.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, hemos evitado con éxito el filtro de espacios en blanco utilizando una tabulación. Veamos otro método para reemplazar espacios en blanco.

### **Usando $IFS**

El uso de la variable de entorno Linux ($IFS) también puede funcionar, ya que su valor predeterminado es un espacio y una tabulación, lo que funcionaría entre los argumentos del comando. Por lo tanto, si usamos `${IFS}` donde deberían estar los espacios, la variable debería reemplazarse automáticamente con un espacio y nuestro comando debería funcionar.

Vamos a usar `${IFS}` y ver si funciona ( `127.0.0.1%0a${IFS}`):&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/109/cmdinj_filters_spaces_4.jpg" alt=""><figcaption></figcaption></figure>

Vemos que nuestra solicitud no fue denegada esta vez y volvimos a pasar por alto el filtro de espacio.

### **Uso de la expansión de llaves**

Existen muchos otros métodos que podemos utilizar para evitar los filtros de espacio. Por ejemplo, podemos utilizar la función `Bash Brace Expansion` que agrega automáticamente espacios entre los argumentos encerrados entre llaves, de la siguiente manera:

```shell-session
afsh4ck@kali$ {ls,-la}

total 0
drwxr-xr-x 1 21y4d 21y4d   0 Jul 13 07:37 .
drwxr-xr-x 1 21y4d 21y4d   0 Jul 13 13:01 ..
```

Como podemos ver, el comando se ejecutó correctamente sin tener espacios. Podemos utilizar el mismo método para omitir el filtro de inyección de comandos, utilizando la expansión de llaves en nuestros argumentos de comando, como ( `127.0.0.1%0a{ls,-la}`). Para descubrir más omisiones de filtros de espacio, consulte la página [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#bypass-without-space) sobre cómo escribir comandos sin espacios.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 83.136.250.196:33250
```

Utilice lo aprendido en esta sección para ejecutar el comando '`ls -la`'. ¿Cuál es el tamaño del archivo '`index.php`'?

Vamos a utilizar el siguiente payload:

```url
127.0.0.1%0a{ls,-la}
```

<figure><img src="/files/BkZtsp4gIviPFaHcMX4X" alt=""><figcaption></figcaption></figure>

Funciona y podemos ver el tamaño de `index.php`, que concretamente es de `1613kb`
