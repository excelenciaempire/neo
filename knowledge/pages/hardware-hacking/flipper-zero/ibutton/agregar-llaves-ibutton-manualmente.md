
# Agregar llaves iButton manualmente

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO---QqAHgHrB1u3mS1FJnem-20241025-124238.png?format=webp" alt=""><figcaption></figcaption></figure>

Además de leer y guardar llave físicas de iButton, puedes emularlas con Flipper Zero.&#x20;

## Creación de claves iButton virtuales <a href="#sxizq" id="sxizq"></a>

Para crear una llave iButton virtual, haga lo siguiente:

1. Vaya al **Menú principal -> iButton -> Agregar manualmente**
2. Seleccione el protocolo iButton de la lista:

* **Dallas DS1990**
* **Dallas DS1992**
* **Dallas DS1996**
* **Dallas DS1971**
* **Dallas (no específico)** : cualquier dispositivo iButton que utilice el protocolo Dallas
* **Cifral**
* **Metakom**

3. Introduzca el UID de la llave original en formato hexadecimal.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/Vx4FORBxdpDTjxuR_SH7z_flipper-zero-ibutton-dallas-non-specific.jpg?format=webp" alt=""><figcaption></figcaption></figure>

4. Presione **Guardar** , luego ingrese un nuevo nombre para la llave y presione **Guardar** nuevamente.

Después de agregar una nueva llave virtual iButton, puedes **emularla** . Las llaves Dallas agregadas manualmente se pueden [escribir en una clave en blanco o en una clave del mismo tipo](https://docs.flipper.net/ibutton/write) .

## <mark style="color:orange;">Edición de claves de iButton guardadas</mark> <a href="#hentc" id="hentc"></a>

Puede editar el UID de la llave guardada haciendo lo siguiente:

1. Vaya al **Menú principal -> iButton -> Guardado**
2. Seleccione la llave que desea editar y seleccione **Editar**
3. Introduzca el valor deseado en hexadecimal.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/sfGsfAUW-hdPi8qWYUr5__monosnap-miro-2023-08-11-19-36-54.jpg?format=webp" alt=""><figcaption></figcaption></figure>

4. Presione **Guardar** , luego ingrese un nuevo nombre para la llave y presione **Guardar** nuevamente.
