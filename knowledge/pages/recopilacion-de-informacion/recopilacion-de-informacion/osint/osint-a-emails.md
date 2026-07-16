
# OSINT a Emails

{% embed url="<https://youtu.be/eg6K7HRu4gU>" %}

## <mark style="color:purple;">Holehe</mark>

**Holehe** es una herramienta de **OSINT** que permite verificar si una dirección de correo electrónico está asociada con cuentas en múltiples plataformas web y servicios en línea. Es útil para investigaciones de ciberseguridad y reconocimiento de objetivos, ya que proporciona información sobre la exposición potencial de una dirección de correo electrónico.

{% embed url="<https://github.com/megadose/holehe.git>" %}

```bash
pip3 install holehe
holehe --no-password-recovery --only-used user@gmail.com
```

<figure><img src="/files/E9bLiXjQDvQtGHVDyEsM" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">IntelBase</mark>

IntelBase es una plataforma de OSINT orientada a investigar emails expuestos públicamente. Puede servir para relacionar una dirección de correo con registros indexados, dominios, servicios y posibles fuentes de exposición.

{% hint style="warning" %}
Consulta únicamente datos públicos y autorizados. Un resultado no confirma la identidad ni la titularidad de una cuenta.
{% endhint %}

{% embed url="<https://intelbase.is/>" %}

<figure><img src="/files/lW4gLnHZp3Q4GJCstGVF" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Epieos</mark>

Epieos es una plataforma online que nos permite buscar el propietario de un email o un teléfono de manera muy simple y extraer distinta información sobre el usuario. También nos da la posibilidad de exportarlo a un JSON para su procesamiento con otras herramientas.

{% embed url="<https://epieos.com/>" %}

<figure><img src="/files/1QaiaP3sQsYO1KY3pzO7" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Zehef</mark>

**Zehef** es una herramienta OSINT especializada en el análisis de correos electrónicos 🎯. Está pensada para **identificar filtraciones, combinaciones de correos y presencia en redes sociales y servicios online**, ideal para tareas de **reconocimiento pasivo** o investigaciones de ciberinteligencia.

Zehef recopila información pública relacionada con un **email objetivo**, y realiza tareas como:

* 🔎 Verifica si el correo aparece en bases de datos públicas como **Pastebin**.
* 🕵️‍♂️ Busca posibles **filtraciones y leaks** usando **HudsonRock API**.
* 📱 Revisa si el correo está asociado a redes como:
  * Instagram
  * Spotify
  * Deezer
  * Adobe
  * 𝕏 (Twitter)
  * y más...
* 🧮 Genera **variaciones y combinaciones** del email objetivo.

{% embed url="<https://github.com/N0rz3/Zehef>" %}

```bash
git clone https://github.com/N0rz3/Zehef.git
cd Zehef
pip3 install -r requirements.txt

python3 zehef.py <email>
```

***

## <mark style="color:purple;">MailFinder</mark>

MailFinder es una herramienta en python que sirve para generar un listado de emails válidos contra un objetivo, especificándole el nombre, apellidos, etc...

{% embed url="<https://github.com/mishakorzik/MailFinder>" %}

<figure><img src="/files/7dXvGjDQSmXutRWkbcfq" alt=""><figcaption></figcaption></figure>

#### Instalación

```bash
git clone https://github.com/mishakorzik/MailFinder
cd MailFinder
python MailFinder.py
```

***

## <mark style="color:purple;">Snov</mark>

Snov.io es una plataforma que proporciona herramientas para encontrar direcciones de correo electrónico y realizar actividades relacionadas con la búsqueda de prospectos y la generación de leads. La plataforma ofrece funciones como búsqueda de correos electrónicos, verificación de correos electrónicos, y envío de correos electrónicos en frío.

{% hint style="success" %}
Es gratuito y tiene una extensión de navegador muy útil para ir a una web y encontrar emails relacionados
{% endhint %}

{% embed url="<https://snov.io/es/>" %}

<figure><img src="/files/Rik3QqhxT0Zdpg6KdSN3" alt=""><figcaption></figcaption></figure>
