
# Escritura de datos en llaves iButton

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-Rhtu2q0Qxu2DfKyFvDVkB-20241025-124310.png?format=webp" alt=""><figcaption></figcaption></figure>

Una vez que haya [leído y guardado](/ethical-hacking-cheatsheet/hardware-hacking/flipper-zero/ibutton/lectura-de-llaves-ibutton.md) las claves de Dallas iButton, puede escribir algunas de ellas en espacios físicos o en llaves iButton del mismo tipo.&#x20;

## <mark style="color:orange;">Llaves y blanks compatibles</mark> <a href="#bhmfr" id="bhmfr"></a>

Los blanks y las llaves iButton permiten escribir distintos datos. Las llaves iButton tienen un UID permanente que no se puede cambiar, pero aún así se puede reescribir su memoria. Por el contrario, en el caso de los blanks, tanto el UID como la memoria se pueden reescribir. Sin embargo, Flipper Zero aún no admite la reescritura de la memoria de un blank.

A continuación se muestran blanks compatibles en los que puede escribir:

| **Tipo de blank** | **Compatible con** | **Comentario**                                                |
| ----------------- | ------------------ | ------------------------------------------------------------- |
| RW1990            | DS1990             | Escribe solo el UID                                           |
| TM1990            | DS1990             | Escribe solo el UID                                           |
| TM08v2            | DS1990             | Escribe solo el UID                                           |
| RW2004            | DS1990, DS1992     | Escribe solo el UID aunque el espacio en blanco tenga memoria |

En cuanto a las llaves iButton, Flipper Zero ahora admite la escritura de datos de memoria de las llaves iButton **DS1992** , **DS1996** y **DS1971** en otra llave del mismo tipo (DS1992 -> DS1992).

## <mark style="color:orange;">Cómo escribir datos en blanks y llaves</mark> <a href="#zdvum" id="zdvum"></a>

Después de guardar o agregar una llave Dallas, puede escribirla en un blank o en una llave del mismo tipo haciendo lo siguiente:

1. Vaya al **Menú principal -> iButton -> Saved**
2. Seleccione la llave iButton de Dallas que desea escribir
3. Seleccionar:

* **Escriba ID** para escribir el UID en el blank. *o*
* **Escritura completa en el mismo tipo** para escribir solo datos de memoria en la llave.

4. Conecte los pines de su Flipper Zero al espacio en blanco o a la llave como se muestra a continuación.

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-I1z2ib-yILJh4tHHev-t0-20241025-124417.png?format=webp" alt=""><figcaption></figcaption></figure>

5. Si los datos se escriben correctamente, verás a tu delfín feliz mostrando el siguiente mensaje de confirmación.

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/eRIXUmuHY-bKLERGa1uyY_flipper-zero-ibutton-successful-writing.jpg?format=webp" alt=""><figcaption></figcaption></figure>

### Si la escritura falló <a href="#swxcn" id="swxcn"></a>

* Es posible que los pines no toquen correctamente la llave iButton. -> Asegúrese de conectar la llave como se muestra arriba.
* Es posible que el iButton en blanco no sea compatible con Flipper Zero.
* Es posible que la llave de memoria táctil o el blank estén dañados.
