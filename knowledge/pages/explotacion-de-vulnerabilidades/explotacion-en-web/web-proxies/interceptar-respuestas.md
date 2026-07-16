
# Interceptar respuestas

En algunos casos, es posible que necesitemos interceptar las respuestas HTTP del servidor antes de que lleguen al navegador. Esto puede resultar útil cuando queremos cambiar el aspecto de una página web específica, como habilitar determinados campos deshabilitados o mostrar determinados campos ocultos, lo que puede ayudarnos en nuestras actividades de pruebas de penetración.

Entonces, veamos cómo podemos lograr esto con el ejercicio que probamos en la sección anterior.

En nuestro ejercicio anterior, el campo `IP` solo nos permitía ingresar valores numéricos. Si interceptamos la respuesta antes de que llegue a nuestro navegador, podemos editarla para que acepte cualquier valor, lo que nos permitiría ingresar directamente el payload que usamos la última vez.

***

## <mark style="color:purple;">Interceptar respuestas</mark>

### Burp Suite

En Burp, podemos habilitar la interceptación de respuestas yendo a ( `Proxy>Options`) y habilitando `Intercept Response` en `Intercept Server Responses`:

![](https://academy.hackthebox.com/storage/modules/110/response_interception_enable.jpg)

Después de eso, podemos habilitar la interceptación de solicitudes una vez más y actualizar la página con \[ `CTRL+SHIFT+R`] en nuestro navegador (para forzar una actualización completa). Cuando volvamos a Burp, deberíamos ver la solicitud interceptada y podemos hacer clic en `forward`. Una vez que reenviemos la solicitud, veremos nuestra respuesta interceptada:

![Respuesta de interceptación de Burp](https://academy.hackthebox.com/storage/modules/110/response_intercept_response_1_1.jpg)

Intentemos cambiar la línea 27 `type="number"` a `type="text"`, lo que debería permitirnos escribir cualquier valor que queramos. También cambiaremos a `maxlength="3"` a `maxlength="100"` para poder ingresar datos más largos:

```html
<input type="text" id="ip" name="ip" min="1" max="255" maxlength="100"
    oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
    required>
```

Ahora, una vez que hagamos clic nuevamente en `forward`, podremos regresar a Firefox para examinar la respuesta editada:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/response_intercept_response_2.jpg" alt=""><figcaption></figcaption></figure>

Como podemos ver, podemos cambiar la forma en que el navegador muestra la página y ahora podemos ingresar cualquier valor que queramos. Podemos usar la misma técnica para habilitar de forma persistente cualquier botón HTML deshabilitado modificando su código HTML.

***

### ZAP

Vamos a intentar ver cómo podemos hacer lo mismo con ZAP. Como vimos en la sección anterior, cuando nuestras peticiones son interceptadas por ZAP, podemos hacer clic en `Step`, y enviará la petición e interceptará automáticamente la respuesta:

![Respuesta de intercepción ZAP](https://academy.hackthebox.com/storage/modules/110/zap_response_intercept_response.jpg)

Una vez que hagamos los mismos cambios que hicimos anteriormente y hagamos clic en `Continue`, veremos que también podemos usar cualquier valor de entrada:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/ZAP_edit_response.jpg" alt=""><figcaption></figcaption></figure>

Sin embargo, ZAP HUD también tiene otra característica poderosa que nos puede ayudar en casos como este. Si bien en muchas ocasiones podemos necesitar interceptar la respuesta para realizar cambios personalizados, si todo lo que queremos es habilitar los campos de entrada deshabilitados o mostrar los campos de entrada ocultos, entonces podemos hacer clic en el tercer botón de la izquierda (el ícono de la bombilla), y habilitará/mostrará estos campos sin que tengamos que interceptar la respuesta o actualizar la página.

Por ejemplo, la siguiente aplicación web tiene el campo de entrada `IP` deshabilitado:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/ZAP_disabled_field.jpg" alt=""><figcaption></figcaption></figure>

En estos casos, podemos hacer clic en el botón `Show/Enable` y se habilitará para nosotros y podremos interactuar con él para agregar nuestra entrada:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/ZAP_enable_field.jpg" alt=""><figcaption></figcaption></figure>

De manera similar, podemos usar esta función para mostrar todos los campos o botones ocultos. `Burp` también tiene una función similar, que podemos habilitar en `Proxy>Options>Response Modification` y luego seleccionar una de las opciones, como `Unhide hidden form fields`.

Otra característica similar es el botón `Comments`, que indicará las posiciones donde hay comentarios HTML que normalmente solo son visibles en el código fuente. Podemos hacer clic en el botón `+` en el panel izquierdo y seleccionar `Comments`, y una vez que hagamos clic en él se deberían mostrar los indicadores. Por ejemplo, la siguiente captura de pantalla muestra un indicador para una posición que tiene un comentario, y al pasar el cursor sobre él se muestra el contenido del comentario:

<figure><img src="https://academy.hackthebox.com/storage/modules/110/ZAP_show_comments.jpg" alt=""><figcaption></figcaption></figure>

Poder modificar el aspecto de la página web nos facilita mucho la realización de pruebas de penetración de aplicaciones web en determinados escenarios en lugar de tener que enviar nuestra entrada a través de una petición interceptada. A continuación, veremos cómo podemos automatizar este proceso para modificar nuestros cambios en la respuesta de forma automática y no tener que seguir interceptando y cambiando manualmente las respuestas.
