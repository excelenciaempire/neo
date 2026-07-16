
# OSINT en Linkedin

## <mark style="color:purple;">Crosslinked</mark>

CrossLinked es una herramienta de enumeración de LinkedIn que utiliza su motor de búsqueda para recopilar nombres válidos de empleados de una organización. Esta herramienta proporciona resultados precisos sin el uso de claves API, credenciales o acceso directo a LinkedIn.

{% embed url="<https://github.com/m8sec/CrossLinked>" %}

```bash
git clone https://github.com/m8sec/crosslinked
cd crosslinked
pip3 install .

# Ejemplos de búsqueda
python3 crosslinked.py -f '{first}.{last}@domain.com' company_name
python3 crosslinked.py -f 'domain\{f}{last}' -t 15 -j 2 company_name
```

<figure><img src="/files/BO0DrqCEsppRKNWScqNO" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Linkedin2Username</mark>

Linkedin2Username es una herramienta que genera una lista de posibles nombres de usuario de empleados de una empresa utilizando LinkedIn. Esta herramienta aprovecha la búsqueda avanzada de LinkedIn para crear nombres de usuario basados en los nombres y apellidos de los empleados.

Es un web scraper puro, que no requiere clave API. Usa tu nombre de usuario y contraseña válidos de LinkedIn para iniciar sesión y creará varias listas con posibles formatos de nombres de usuarios para todos los empleados de la empresa a la que lo dirijas.

{% embed url="<https://github.com/initstring/linkedin2username>" %}

<figure><img src="/files/c6GZmWuLH4GdlJdiPRsL" alt=""><figcaption></figcaption></figure>

```bash
git clone https://github.com/initstring/linkedin2username.git
cd linkedin2username
pip3 install -r requirements.txt
```

Aquí un ejemplo para extraer todos los empleados de tesla:

```bash
python3 linkedin2username.py -c tesla
```

Ejemplo para extraer una lista más corta y agregarle el nombre de dominio `@tesla.com`:

```bash
python3 linkedin2username.py -c tesla -d 5 -n 'tesla.com'
```

***

## <mark style="color:purple;">Signal Hire</mark>

SignalHire es una herramienta que nos permite obtener el teléfono y el email de cualquier usuario de Linkedin. Tiene una extensión de navegador especialmente últil que se activa cada vez que entramos a un perfil.

{% hint style="success" %}
Esta extensión tiene **10 créditos gratuitos al mes** a fecha de redacción de este artículo (2025)
{% endhint %}

{% embed url="<https://chromewebstore.google.com/detail/signalhire-find-email-or/aeidadjdhppdffggfgjpanbafaedankd?hl=es&utm_source=ext_sidebar>" %}

<figure><img src="/files/ZNmaSzDG2MiNAJjtceHm" alt=""><figcaption></figcaption></figure>
