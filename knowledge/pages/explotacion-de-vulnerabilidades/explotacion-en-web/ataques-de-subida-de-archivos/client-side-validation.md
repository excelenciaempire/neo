
# Client-Side Validation

Muchas aplicaciones web solo dependen del código JavaScript del frontend para validar el formato de archivo seleccionado antes de cargarlo y no lo cargarían si el archivo no está en el formato requerido (por ejemplo, si no es una imagen).

Sin embargo, como la validación del formato de archivo se realiza en el lado del cliente, podemos evitarla fácilmente interactuando directamente con el servidor, lo que nos permite omitir por completo las validaciones del frontend. También podemos modificar el código del frontend a través de las herramientas de desarrollo de nuestro navegador para desactivar cualquier validación existente.

***

## <mark style="color:purple;">Validación del lado del cliente</mark>

El ejercicio al final de esta sección muestra una funcionalidad básica de subir una `Imagen de perfil`, que se ve frecuentemente en aplicaciones web que utilizan funciones de perfil de usuario, como las aplicaciones web de redes sociales:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_profile_image_upload.jpg" alt=""><figcaption></figcaption></figure>

Sin embargo, esta vez, cuando aparece el cuadro de selección de archivos, no podemos ver nuestros scripts `PHP` (o puede que estén en gris), ya que el cuadro de diálogo parece estar limitado únicamente a formatos de imagen:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_select_file_types.jpg" alt=""><figcaption></figcaption></figure>

De todas formas , aún podemos seleccionar la opción `All Files` para seleccionar nuestro script `PHP`, pero cuando lo hacemos, recibimos un mensaje de error que dice ( `Only images are allowed!`), y el botón `Upload` se deshabilita:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_select_denied.jpg" alt=""><figcaption></figcaption></figure>

Esto indica algún tipo de validación del tipo de archivo, por lo que no podemos simplemente cargar un webshell a través del formulario de carga como hicimos en la sección anterior. Afortunadamente, toda la validación parece estar sucediendo en el front-end, ya que la página nunca se actualiza ni envía ninguna solicitud HTTP después de seleccionar nuestro archivo. Por lo tanto, deberíamos poder tener un control total sobre estas validaciones del lado del cliente.

Todo código que se ejecuta en el lado del cliente está bajo nuestro control. Si bien el servidor web es responsable de enviar el código front-end, la representación y ejecución del código front-end se realizan dentro de nuestro navegador. Si la aplicación web no aplica ninguna de estas validaciones en el back-end, deberíamos poder cargar cualquier tipo de archivo.

Como se mencionó anteriormente, para evitar estas protecciones, podemos:

1. Modificar la solicitud de carga al servidor back-end
2. Manipular el código front-end para deshabilitar estas validaciones de tipo.

***

## <mark style="color:purple;">Solicitud de modificación del back-end</mark>

Comencemos examinando una solicitud normal a través de `Burp`. Cuando seleccionamos una imagen, vemos que se refleja como nuestra imagen de perfil y, cuando hacemos clic en `Upload`, nuestra imagen de perfil se actualiza y persiste a través de actualizaciones. Esto indica que nuestra imagen se cargó al servidor, que ahora nos la muestra:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_normal_request.jpg" alt=""><figcaption></figcaption></figure>

Si capturamos la solicitud de carga con `Burp`, vemos la siguiente solicitud enviada por la aplicación web:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_image_upload_request.jpg" alt=""><figcaption></figcaption></figure>

La aplicación web parece estar enviando una solicitud de carga HTTP estándar a `/upload.php`. De esta manera, ahora podemos modificar esta solicitud para satisfacer nuestras necesidades sin tener las restricciones de validación de tipo del front-end. Si el servidor back-end no valida el tipo de archivo cargado, entonces, en teoría, deberíamos poder enviar cualquier tipo de archivo/contenido, y este se cargaría al servidor.

Las dos partes importantes de la solicitud son `filename="HTB.png"` y el contenido del archivo al final de la solicitud. Si modificamos el `filename` a `shell.php` y modificamos el contenido de la webshell que usamos en la sección anterior, estaríamos cargando un webshell `PHP` en lugar de una imagen.

Entonces, capturemos otra solicitud de carga de imagen y luego modifiquémosla en consecuencia:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_modified_upload_request.jpg" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Nota**: También podemos modificar el `Content-Type` del archivo cargado, aunque esto no debería jugar un papel importante en esta etapa, por lo que lo mantendremos sin modificar.
{% endhint %}

Como podemos ver, nuestra solicitud de carga se realizó correctamente y obtuvimos la respuesta `File successfully uploaded`. Por lo tanto, ahora podemos visitar el archivo cargado e interactuar con él para obtener la ejecución remota del código.

***

## <mark style="color:purple;">Deshabilitar la validación del front-end</mark>

Otro método para evitar las validaciones del lado del cliente es manipular el código del front-end. Como estas funciones se procesan completamente dentro de nuestro navegador web, tenemos control total sobre ellas. Por lo tanto, podemos modificar estos scripts o deshabilitarlos por completo. Luego, podemos usar la función de carga para cargar cualquier tipo de archivo sin necesidad de utilizar la función de captura y modificación de nuestras solicitudes con `BurpSuite`.

Para comenzar, podemos hacer clic en \[ `CTRL+SHIFT+C`] para alternar el navegador `Page Inspector` y luego hacer clic en la imagen de perfil, que es donde activamos el selector de archivos para el formulario de carga:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_element_inspector.jpg" alt=""><figcaption></figcaption></figure>

Esto resaltará la siguiente entrada de archivo HTML:

```html
<input type="file" name="uploadFile" id="uploadFile" onchange="checkFile(this)" accept=".jpg,.jpeg,.png">
```

Aquí, vemos que la entrada de archivo especifica ( `.jpg,.jpeg,.png`) como los tipos de archivo permitidos dentro del cuadro de diálogo de selección de archivos. Sin embargo, podemos modificar esto fácilmente y seleccionar `All Files` como lo hicimos antes, por lo que no es necesario cambiar esta parte de la página.

La parte más interesante es `onchange="checkFile(this)"`, que parece ejecutar un código JavaScript cada vez que seleccionamos un archivo, lo que parece realizar la validación del tipo de archivo. Para obtener los detalles de esta función, podemos ir a  `Console` con \[ `CTRL+SHIFT+K`] y luego podemos escribir el nombre de la función ( `checkFile`) para obtener sus detalles:

```javascript
function checkFile(File) {
...SNIP...
    if (extension !== 'jpg' && extension !== 'jpeg' && extension !== 'png') {
        $('#error_message').text("Only images are allowed!");
        File.form.reset();
        $("#submit").attr("disabled", true);
    ...SNIP...
    }
}
```

Lo fundamental que nos llevamos de esta función es que comprueba si la extensión del archivo es una imagen, y si no lo es imprime el mensaje de error que vimos antes ( `Only images are allowed!`) y desactiva el botón `Upload`. Podemos añadir `PHP` como una de las extensiones permitidas o modificar la función para quitar la comprobación de la extensión.

Afortunadamente, no necesitamos escribir ni modificar código JavaScript. Podemos eliminar esta función del código HTML, ya que su uso principal parece ser la validación del tipo de archivo y eliminarla no debería afectar a nada.

Para ello, podemos volver a nuestro inspector, hacer clic nuevamente en la imagen de perfil, hacer doble click en el nombre de la función ( `checkFile`) en la línea `18`, y eliminarlo:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_removed_js_function.jpg" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
**Consejo**: También puedes hacer lo mismo para eliminar `accept=".jpg,.jpeg,.png"`, lo que debería facilitar la selección del shell `PHP` en el cuadro de diálogo de selección de archivos, aunque esto no es obligatorio, como se mencionó anteriormente.
{% endhint %}

Con la función `checkFile` eliminada de la entrada del archivo, deberíamos poder seleccionar nuestro webshell `PHP` a través del cuadro de diálogo de selección de archivo y cargarlo normalmente sin validaciones, similar a lo que hicimos en la sección anterior.

{% hint style="info" %}
**Nota**: La modificación que realizamos en el código fuente es temporal y no se mantendrá en las actualizaciones de la página, ya que solo la estamos modificando en el lado del cliente. Sin embargo, nuestra única necesidad es omitir la validación del lado del cliente, por lo que debería ser suficiente para este propósito.
{% endhint %}

Una vez que cargamos nuestro webshell usando cualquiera de los métodos anteriores y luego actualizamos la página, podemos usar el `Page Inspector` una vez más con \[ `CTRL+SHIFT+C`], hacer click en la imagen de perfil y deberíamos ver la URL de nuestro webshell cargado:

```html
<img src="/profile_images/shell.php" class="profile-image" id="profile-image">
```

Si podemos hacer clic en el enlace de arriba, llegaremos a nuestro shell web cargado, con el que podemos interactuar para ejecutar comandos en el servidor back-end:

<figure><img src="https://academy.hackthebox.com/storage/modules/136/file_uploads_php_manual_shell.jpg" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Nota**: Los pasos que se muestran se aplican a Firefox, ya que otros navegadores pueden tener métodos ligeramente diferentes para aplicar cambios locales a la fuente, como el uso `overrides` en Chrome.
{% endhint %}

***

## Caso práctico

Intente omitir las validaciones de tipo de archivo del lado del cliente en el ejercicio anterior, luego cargue un webshell para leer `/flag.txt`

```
Objetivo: 94.237.58.211:36276
```

Intentamos cargar una webshell PHP pero no nos deja, tiene una validación para solamente permitir imágenes:

<figure><img src="/files/js3zYO5DWwG0lhMHTRYZ" alt=""><figcaption></figcaption></figure>

Encontramos una función `validate()` interesante, que es la que hace la validación de las imágenes:

```javascript
function validate() {
  var file = $("#uploadFile")[0].files[0];
  var filename = file.name;
  var extension = filename.split('.').pop();

  if (extension !== 'jpg' && extension !== 'jpeg' && extension !== 'png') {
    $('#error_message').text("Only images are allowed!");
    File.form.reset();
    $("#submit").attr("disabled", true);
    return false;
  } else {
    return true;
  }
}
```

Vamos a eliminar esta función del HTML, dejando solo el `upload()`, ya que es una función posiblemente necesaria para subir este archivo:

<figure><img src="/files/9fS1apZVSxByCq8plrEi" alt=""><figcaption></figcaption></figure>

Le damos a upload para subir la webshell en PHP, y si miramos ahora el código fuente nos encontramos con la ruta de la imagen:

<figure><img src="/files/pqS3ZwZikf08mWPuFQ0J" alt=""><figcaption></figcaption></figure>

Si accedemos entramos directamente a la webshell:

<figure><img src="/files/EJdJBWnYfelvLx2xxBuG" alt=""><figcaption></figcaption></figure>

Bingo! Obtenemos la flag 🏆
