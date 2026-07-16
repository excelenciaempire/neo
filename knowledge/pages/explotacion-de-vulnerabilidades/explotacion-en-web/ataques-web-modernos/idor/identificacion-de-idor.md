
# Identificación de IDOR

## <mark style="color:purple;">Parámetros de URL y API</mark>

El primer paso para explotar las vulnerabilidades de IDOR es identificar referencias directas a objetos. Siempre que recibamos un archivo o recurso específico, debemos estudiar las solicitudes HTTP para buscar parámetros de URL o API con una referencia a un objeto (por ejemplo, `?uid=1`o `?filename=file_1.pdf`). Estos se encuentran principalmente en parámetros de URL o API, pero también pueden encontrarse en otros encabezados HTTP, como las cookies.

En los casos más básicos, podemos intentar incrementar los valores de las referencias de objetos para recuperar otros datos, como ( `?uid=2`) o ( `?filename=file_2.pdf`). También podemos usar una aplicación de fuzzing para probar miles de variaciones y ver si devuelven algún dato. Cualquier acceso exitoso a archivos que no sean nuestros indicaría una vulnerabilidad de IDOR.

***

## <mark style="color:purple;">Llamadas AJAX</mark>

También podemos identificar parámetros o API no utilizados en el código del front-end en forma de llamadas AJAX de JavaScript. Algunas aplicaciones web desarrolladas en marcos de JavaScript pueden colocar de manera insegura todas las llamadas de función en el front-end y usar las adecuadas según el rol del usuario.

Por ejemplo, si no tuviéramos una cuenta de administrador, solo se utilizarían las funciones de nivel de usuario, mientras que las funciones de administrador estarían deshabilitadas. Sin embargo, aún podríamos encontrar las funciones de administrador si analizamos el código JavaScript del frontend y podríamos identificar llamadas AJAX a puntos finales o API específicos que contengan referencias directas a objetos. Si identificamos referencias directas a objetos en el código JavaScript, podemos probarlas para detectar vulnerabilidades de IDOR.

Por supuesto, esto no es exclusivo de las funciones de administración, sino que también puede ser cualquier función o llamada que no se pueda encontrar mediante el monitoreo de solicitudes HTTP. El siguiente ejemplo muestra un ejemplo básico de una llamada AJAX:

```javascript
function changeUserPassword() {
    $.ajax({
        url:"change_password.php",
        type: "post",
        dataType: "json",
        data: {uid: user.uid, password: user.password, is_admin: is_admin},
        success:function(result){
            //
        }
    });
}
```

Es posible que la función anterior nunca se invoque cuando usemos la aplicación web como un usuario que no sea administrador. Sin embargo, si la ubicamos en el código del front-end, podemos probarla de diferentes maneras para ver si podemos invocarla para realizar cambios, lo que indicaría que es vulnerable a IDOR. Podemos hacer lo mismo con el código del back-end si tenemos acceso a él (por ejemplo, aplicaciones web de código abierto).

***

## <mark style="color:purple;">Comprender el hash/codificación</mark>

Es posible que algunas aplicaciones web no utilicen números secuenciales simples como referencias de objetos, sino que codifiquen la referencia o la conviertan en hash. Si encontramos que dichos parámetros utilizan valores codificados o en hash, es posible que aún podamos aprovecharlos si no hay un sistema de control de acceso en el back-end.

Supongamos que la referencia se codificó con un codificador común (por ejemplo, `base64`). En ese caso, podríamos decodificarla y ver el texto sin formato de la referencia del objeto, cambiar su valor y luego codificarlo nuevamente para acceder a otros datos. Por ejemplo, si vemos una referencia como ( `?filename=ZmlsZV8xMjMucGRm`), podemos adivinar inmediatamente que el nombre del archivo está `base64`codificado (a partir de su conjunto de caracteres), que podemos decodificar para obtener la referencia del objeto original de ( `file_123.pdf`). Luego, podemos intentar codificar una referencia de objeto diferente (por ejemplo, `file_124.pdf`) e intentar acceder a ella con la referencia de objeto codificada ( `?filename=ZmlsZV8xMjQucGRm`), lo que puede revelar una vulnerabilidad de IDOR si pudiéramos recuperar algún dato.

Por otro lado, la referencia del objeto puede estar codificada en hash, como ( `download.php?filename=c81e728d9d4c2f636f067f89cc14862c`). A primera vista, podemos pensar que se trata de una referencia de objeto segura, ya que no utiliza texto claro ni codificación sencilla. Sin embargo, si observamos el código fuente, podemos ver qué se codifica en hash antes de que se realice la llamada a la API:

```javascript
$.ajax({
    url:"download.php",
    type: "post",
    dataType: "json",
    data: {filename: CryptoJS.MD5('file_1.pdf').toString()},
    success:function(result){
        //
    }
});
```

En este caso, podemos ver que el código utiliza el `filename` y lo codifica con `CryptoJS.MD5`, lo que nos facilita el cálculo de `filename` para otros archivos potenciales. De lo contrario, podemos intentar identificar manualmente el algoritmo de codificación que se está utilizando (por ejemplo, con herramientas de identificación de codificación) y luego codificar el nombre del archivo para ver si coincide con el hash utilizado. Una vez que podamos calcular los hashes para otros archivos, podemos intentar descargarlos, lo que puede revelar una vulnerabilidad de IDOR si podemos descargar cualquier archivo que no nos pertenezca.

***

## <mark style="color:purple;">Comparar roles de usuario</mark>

Si queremos realizar ataques IDOR más avanzados, es posible que necesitemos registrar varios usuarios y comparar sus solicitudes HTTP y referencias de objetos. Esto puede permitirnos comprender cómo se calculan los parámetros de URL y los identificadores únicos y luego calcularlos para que otros usuarios recopilen sus datos.

Por ejemplo, si tuviéramos acceso a dos usuarios diferentes, uno de los cuales puede ver su salario después de realizar la siguiente llamada API:

```json
{
  "attributes" : 
    {
      "type" : "salary",
      "url" : "/services/data/salaries/users/1"
    },
  "Id" : "1",
  "Name" : "User1"
}
```

Es posible que el segundo usuario no tenga todos estos parámetros de API para replicar la llamada y no debería poder realizar la misma llamada que `User1`. Sin embargo, con estos detalles a mano, podemos intentar repetir la misma llamada de API mientras estamos conectados para `User2`ver si la aplicación web devuelve algo. Estos casos pueden funcionar si la aplicación web solo requiere una sesión iniciada con sesión válida para realizar la llamada de API, pero no tiene control de acceso en el back-end para comparar la sesión del llamador con los datos que se están llamando.

Si este es el caso y podemos calcular los parámetros de la API para otros usuarios, se trataría de una vulnerabilidad de IDOR. Incluso si no pudiéramos calcular los parámetros de la API para otros usuarios, igualmente habríamos identificado una vulnerabilidad en el sistema de control de acceso de back-end y podríamos comenzar a buscar otras referencias de objetos para explotar.
