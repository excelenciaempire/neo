
# OSINT en Instagram

## <mark style="color:purple;">SilverInstaEye</mark>

**SilverInstaEye** es una herramienta de código abierto diseñada para la recopilación de información y análisis en Instagram. Facilita la captura de datos públicos disponibles en perfiles, publicaciones y comentarios o stories, almacenando todos los datos recopilados en archivos de texto.

{% embed url="<https://github.com/silverxpymaster/SilverInstaEye>" %}

<figure><img src="/files/CdHwkUqpoi2fPxaGiYYO" alt=""><figcaption></figcaption></figure>

#### Instalación

```bash
git clone https://github.com/silverxpymaster/SilverInstaEye.git
cd SilverInstaEye
pip install -r requirements.txt
python3 silverinstaeye.py
```

{% hint style="danger" %}
Se recomienda el uso de una `cuenta fake`, ya que al realizar muchas peticiones Instagram puede banear nuestra cuenta principal
{% endhint %}

***

## <mark style="color:purple;">Yes It´s Me</mark>

**yesitsme** es un script en Python que busca cuentas de Instagram asociadas a un nombre, correo electrónico y número de teléfono específicos. Aprovechando las capacidades de indexación de dumpor.com, recupera todos los nombres de usuario asociados a un nombre y compara automáticamente el correo electrónico/teléfono ofuscado de toutatis obtenido con el proporcionado, ahorrando tiempo y esfuerzo en las investigaciones en línea.

{% embed url="<https://github.com/0x0be/yesitsme>" %}

#### Instalación

```bash
git clone https://github.com/blackeko/yesitsme/
cd yesitsme
pip3 install -r requirements.txt
python3 yesitsme.py -s SESSION_ID -n NAME -e EMAIL -p PHONE -t TIMEOUT 
```

<table><thead><tr><th width="118.3046875">Argumento</th><th width="197.31640625">Ejemplo</th><th>Descripción</th></tr></thead><tbody><tr><td><code>-s</code></td><td><code>"SESSION_ID"</code></td><td>Cookie <code>sessionid</code> de tu cuenta de Instagram (por ejemplo, una cuenta falsa).</td></tr><tr><td><code>-n</code></td><td><code>"Nombre Apellido"</code></td><td>Nombre y apellido del objetivo (insensible a mayúsculas/minúsculas).</td></tr><tr><td><code>-e</code></td><td><code>"a****z@gmail.com"</code></td><td>Primera y última letra del correo electrónico del objetivo.</td></tr><tr><td><code>-p</code></td><td><code>"+34 ** 09"</code></td><td>Prefijo y dos últimos dígitos del número de teléfono del objetivo.</td></tr><tr><td><code>-t</code></td><td><code>"10"</code></td><td>Tiempo de espera entre cada solicitud (valor por defecto = 0).</td></tr></tbody></table>

```bash
python3 yesitsme.py -s 5t3El3650d4Z7A3jA2%Y1R70vnYn%36U3 -n "John Doe" -e "j*****e@gmail.com" -p "+34 *** *** *09" -t 10
```

<figure><img src="/files/08wNIPVFuuagtQVGewG2" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Osintgram</mark>

Osintgram es una herramienta de recolección de información que proporciona una shell interactiva para analizar cuentas de Instagram usando el nombre de usuario del objetivo. La shell interactiva permite ejecutar múltiples comandos para extraer datos útiles como seguidores, seguidos, fotos etiquetadas, comentarios y más, facilitando un análisis detallado de la actividad y relaciones del usuario en Instagram.

{% embed url="<https://github.com/Datalux/Osintgram>" %}

<figure><img src="/files/YxNL9EgXtJlB9KtgoS0X" alt=""><figcaption></figcaption></figure>

**Osintgram** ofrece una shell interactiva para realizar análisis en cuentas de Instagram de cualquier usuario a través de su nombre de usuario. Puedes obtener:

<table><thead><tr><th width="150.6171875">Comando</th><th>Descripción</th></tr></thead><tbody><tr><td><code>addrs</code></td><td>Obtener todas las direcciones registradas en las fotos del objetivo</td></tr><tr><td><code>captions</code></td><td>Obtener las descripciones de las fotos del usuario</td></tr><tr><td><code>comments</code></td><td>Obtener el total de comentarios en las publicaciones del objetivo</td></tr><tr><td><code>followers</code></td><td>Obtener los seguidores del objetivo</td></tr><tr><td><code>followings</code></td><td>Obtener los usuarios seguidos por el objetivo</td></tr><tr><td><code>fwersemail</code></td><td>Obtener los correos electrónicos de los seguidores del objetivo</td></tr><tr><td><code>fwingsemail</code></td><td>Obtener los correos electrónicos de los usuarios seguidos por el objetivo</td></tr><tr><td><code>fwersnumber</code></td><td>Obtener los números de teléfono de los seguidores del objetivo</td></tr><tr><td><code>fwingsnumber</code></td><td>Obtener los números de teléfono de los usuarios seguidos por el objetivo</td></tr><tr><td><code>hashtags</code></td><td>Obtener los hashtags utilizados por el objetivo</td></tr><tr><td><code>info</code></td><td>Obtener información del objetivo</td></tr><tr><td><code>likes</code></td><td>Obtener el total de “me gusta” en las publicaciones del objetivo</td></tr><tr><td><code>mediatype</code></td><td>Obtener el tipo de publicaciones del usuario (foto o video)</td></tr><tr><td><code>photodes</code></td><td>Obtener las descripciones de las fotos del objetivo</td></tr><tr><td><code>photos</code></td><td>Descargar las fotos del usuario en la carpeta de salida</td></tr><tr><td><code>propic</code></td><td>Descargar la foto de perfil del usuario</td></tr><tr><td><code>stories</code></td><td>Descargar las historias del usuario</td></tr><tr><td><code>tagged</code></td><td>Obtener la lista de usuarios etiquetados por el objetivo</td></tr><tr><td><code>wcommented</code></td><td>Obtener una lista de usuarios que comentaron las fotos del objetivo</td></tr><tr><td><code>wtagged</code></td><td>Obtener una lista de usuarios que etiquetaron al objetivo</td></tr></tbody></table>

#### Instalación

1. **Clona o descarga el repositorio:**

```bash
git clone https://github.com/Datalux/Osintgram.git
cd Osintgram
```

2. **Crea un entorno virtual para el proyecto:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

4. **Configura tus credenciales de Instagram:**

{% hint style="danger" %}
Se recomienda el uso de una `cuenta fake`, ya que al realizar muchas peticiones Instagram puede banear nuestra cuenta principal
{% endhint %}

* Abre el archivo `config/credentials.ini` y escribe tu nombre de usuario y contraseña.
* **Alternativa:** Ejecuta `make setup` para generar y completar automáticamente el archivo de configuración.

5. **Ejecuta el script principal:**

```bash
python3 main.py <nombre_de_usuario_objetivo>
```

* O ejecuta un comando directamente:

```bash
python3 main.py <nombre_de_usuario_objetivo> --command <comando>
```

***

### O**sintgram v2 (versión beta)**

La versión 2 es más rápida y tiene una nueva interfaz para la ejecución de comandos.

1. Cambia a la rama `v2`:

```bash
git checkout v2
```

2. Luego repite los pasos de instalación anteriores dentro de esa rama.
