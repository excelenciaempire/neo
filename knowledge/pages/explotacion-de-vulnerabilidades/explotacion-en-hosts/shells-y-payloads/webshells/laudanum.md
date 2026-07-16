
# Laudanum

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

***

## <mark style="color:purple;">Laudanum, una webshell para gobernarlos a todos</mark>

Laudanum es un repositorio de archivos listos para usar que se pueden usar para inyectar en una víctima y recibir acceso posterior a través de un shell inverso, ejecutar comandos en el host de la víctima directamente desde el navegador y más. El repositorio incluye archivos inyectables para incluir muchos lenguajes de aplicaciones web diferentes `asp, aspx, jsp, php,`y más. Este es un elemento básico que debe tener en cualquier pentester. Si está utilizando su propia máquina virtual, Laudanum está integrado en Parrot OS y Kali de forma predeterminada. Para cualquier otra distribución, probablemente necesitarás descargar una copia para usarla. Puedes obtenerlo [aqui](https://github.com/jbarcia/Web-Shells/tree/master/laudanum) . Examinemos Laudanum y veamos cómo funciona.

***

### Trabajando con Laudanum

Los archivos de Laudanum se pueden encontrar en el directorio:

```
/usr/share/webshells/laudanum
```

Para la mayoría de los archivos dentro de Laudanum, puede copiarlos tal cual y colocarlos donde necesite que la víctima los ejecute. Para archivos específicos, como los shells, primero debe `editar` el archivo para insertar la `dirección IP atacante` de su host y asegurarse de poder acceder al shell web o recibir una devolución de llamada en el caso de que utilice un shell inverso. Antes de utilizar los diferentes archivos, asegúrese de leer el contenido y los comentarios para asegurarse de tomar las acciones adecuadas.

***

## <mark style="color:purple;">Demostración</mark>

Ahora que entendemos qué es Laudanum y cómo funciona, veamos una aplicación web que encontramos en nuestro entorno de laboratorio y veamos si podemos ejecutar un shell web. Si desea seguir esta demostración, deberá agregar una entrada en su archivo `/etc/hosts` en su VM de ataque para el host que estamos atacando. Esa entrada debería decir:&#x20;

`<target ip> status.inlanefreight.local`.&#x20;

### **Mover una copia para modificarla**

```bash
cp /usr/share/webshells/laudanum/aspx/shell.aspx /home/kali/Escritorio/demo.aspx
```

Añade tu dirección IP a la variable `allowedIps` en línea `59`. Realice cualquier otro cambio que desee. Puede ser prudente eliminar el arte ASCII y los comentarios del archivo. Estos elementos en una carga útil a menudo están firmados y pueden alertar a los defensores/AV sobre lo que estás haciendo.

### **Modificar el Shell para su uso**

<figure><img src="/files/HEKwicZHyz4RIJT8pJR4" alt=""><figcaption></figcaption></figure>

Estamos aprovechando la función de carga en la parte inferior de la página para subir nuestro webshell al servidor. Si tiene éxito, debería imprimir la ruta donde se guardó el archivo. Utiliza la función de carga. El mensaje de éxito imprime dónde se almacena el archivo, navegue hasta él.

### **Aprovechando la función de carga del servidor**

![imagen](https://academy.hackthebox.com/storage/modules/115/laud-upload.png)

Una vez que la carga se haya realizado correctamente, deberá navegar hasta su shell web para utilizar sus funciones. La siguiente imagen nos muestra cómo hacerlo. Como se ve en la última imagen, nuestro shell se cargó en el directorio `\\files\` y el nombre se mantuvo igual. Este no será siempre el caso. Es posible que se encuentre con algunas implementaciones que aleatorizan los nombres de los archivos al cargarlos y que no tienen un directorio de archivos públicos ni ninguna otra posible protección. Por ahora, tenemos suerte de que ese no sea el caso.&#x20;

Con esta aplicación web en particular, nuestro archivo fue `status.inlanefreight.local\\files\demo.aspx` y requerirá que busquemos el payload usando ese \ en la ruta en lugar de / como lo normal. Una vez que haga esto, su navegador lo limpiará en su ventana de URL para que aparezca como : `status.inlanefreight.local//files/demo.aspx`.

### **Navegando a nuestro Shell**

![imagen](https://academy.hackthebox.com/storage/modules/115/laud-nav.png)

Ahora podemos utilizar el shell Laudanum que subimos para enviar comandos al host. Podemos ver en el ejemplo que se ejecutó el comando `systeminfo` correctamente.

### **Éxito!**

![imagen](https://academy.hackthebox.com/storage/modules/115/laud-success.png)
