
# OSINT a Teléfonos

## <mark style="color:purple;">Introducción</mark>

En el siguiente video analizo en detalle las 4 herramientas de esta sección utilizadas para investigar un número de teléfono, para obtener el nombre de la persona que nos ha llamado, redes sociales, ubicación aproximada y posibles filtraciones de datos:

{% embed url="<https://youtu.be/PV_6RoYqrF0?si=AC-oj0tjf91H8aoa>" %}

## <mark style="color:purple;">Truecaller Bot de Telegram</mark>

El Truecaller Bot de Telegram es una herramienta eficiente para obtener información detallada sobre números de teléfono. Utiliza una base de datos extensa para identificar nombres asociados a números de contacto, ayudando a descubrir la identidad de las personas que llaman. Además de la identificación de llamadas, el bot también puede proporcionar enlaces a perfiles en redes sociales vinculados al número investigado (Whatsapp y Telegram), ofreciendo una perspectiva más completa sobre la persona detrás de la llamada. Es especialmente útil para quienes necesitan confirmar la legitimidad de las llamadas entrantes o investigar contactos desconocidos.

{% embed url="<https://t.me/TrueCaller_Z_Bot>" %}

<figure><img src="/files/rrWb8vA98uwiiQi5tj1D" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Phoneinfoga</mark>

Phoneinfoga es una herramienta de código abierto ampliamente utilizada para la búsqueda de información relacionada con números de teléfono. Permite a los usuarios realizar un análisis exhaustivo para determinar la procedencia de un número, identificar la localización geográfica y extraer cualquier dato público asociado. Además nos da un montón de Google Dorks para realizar búsquedas en Google usando ese teléfono.

{% embed url="<https://github.com/sundowndev/phoneinfoga>" %}

```bash
phoneinfoga scan -n "34611237623"
Running scan for phone number 34611237623...

Results for googlesearch

Social media:
	URL: https://www.google.com/search?q=site%3Afacebook.com+intext%3A%2234611237623%22+%7C+intext%3A%22%2B34611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Atwitter.com+intext%3A%2234611237623%22+%7C+intext%3A%22%2B34611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Alinkedin.com+intext%3A%2234611237623%22+%7C+intext%3A%22%2B34611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Ainstagram.com+intext%3A%2234611237623%22+%7C+intext%3A%22%2B34611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Avk.com+intext%3A%2234611237623%22+%7C+intext%3A%22%2B34611237623%22+%7C+intext%3A%22611237623%22

Disposable providers:
	URL: https://www.google.com/search?q=site%3Ahs3x.com+intext%3A%2234611237623%22
	URL: https://www.google.com/search?q=site%3Areceive-sms-now.com+intext%3A%2234611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Asmslisten.com+intext%3A%2234611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Asmsnumbersonline.com+intext%3A%2234611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Afreesmscode.com+intext%3A%2234611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Acatchsms.com+intext%3A%2234611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Asmstibo.com+intext%3A%2234611237623%22+%7C+intext%3A%22611237623%22
	URL: https://www.google.com/search?q=site%3Asmsreceiving.com+intext%3A%2234611237623%22+%7C+intext%3A%22611237623%22
	<----SNIP---->
	
Results for local
Raw local: 611237623
Local: 611 23 76 23
E164: +34611237623
International: 34611237623
Country: ES
```

#### Instalación y uso

{% embed url="<https://sundowndev.github.io/phoneinfoga/getting-started/install/>" %}

```bash
bash <( curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/scripts/install )
sudo install ./phoneinfoga /usr/local/bin/phoneinfoga
phoneinfoga version
```

```bash
phoneinfoga scan -n "+1 (555) 444-1212"
phoneinfoga scan -n "+34 649667788"
phoneinfoga scan -n "34649667788"
```

Ten en cuenta que todos los escáneres utilizan variables de entorno para los valores de configuración. Puedes definir una variable de entorno en línea o colocarla en un archivo llamado `.env` en el directorio actual. La herramienta la analizará automáticamente. Para especificar otro nombre de archivo, utilza la flag `--env-file`.

```bash
# .env.local
NUMVERIFY_API_KEY="value"
GOOGLECSE_CX="value"
GOOGLE_API_KEY="value"
```

```bash
phoneinfoga scan -n "+34 649667788" --env-file=.env.local
```

## <mark style="color:purple;">Epieos</mark>

Epieos es una plataforma online que nos permite buscar el propietario de un email o un teléfono de manera muy simple y extraer distinta información sobre el usuario. También nos da la posibilidad de exportarlo a un JSON para su procesamiento con otras herramientas.

{% embed url="<https://epieos.com/>" %}

<figure><img src="/files/1QaiaP3sQsYO1KY3pzO7" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Mr.Holmes</mark>

Mr.Holmes es una herramienta de recopilación de información (OSINT). El objetivo principal es obtener información completa sobre dominios, nombres de usuario y números de teléfono con la ayuda de fuentes públicas disponibles en Internet y también utiliza Google Dorks para investigaciones específicas. También utiliza servidores proxy para que sus solicitudes sean completamente anónimas y una API WhoIS para obtener más información sobre un dominio.

{% embed url="<https://github.com/Lucksi/Mr.Holmes>" %}

<figure><img src="/files/r3z9HWnnduRl53cwZY21" alt=""><figcaption></figcaption></figure>
