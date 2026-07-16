
# Drupal - Enumeración

## <mark style="color:purple;">Introducción</mark>

[Drupal](https://www.drupal.org/) , lanzado en 2001, es el tercer y último CMS que cubriremos en nuestro recorrido por el mundo de las aplicaciones comunes. Drupal es otro CMS de código abierto que es popular entre empresas y desarrolladores. Drupal está escrito en PHP y admite el uso de MySQL o PostgreSQL para el backend. Además, se puede utilizar SQLite si no hay un DBMS instalado. Al igual que WordPress, Drupal permite a los usuarios mejorar sus sitios web mediante el uso de temas y módulos. En el momento de escribir este artículo, el proyecto Drupal tiene casi 43.000 módulos y 2.900 temas y es el tercer CMS más popular por participación de mercado. Aquí hay algunas [estadísticas](https://websitebuilder.org/blog/drupal-statistics/) interesantes sobre Drupal recopiladas de varias fuentes:

* Alrededor del 1,5% de los sitios en Internet utilizan Drupal (¡más de 1,1 millones de sitios!), el 5% del millón de sitios web más importantes de Internet y el 7% de los 10.000 sitios más importantes
* Drupal representa alrededor del 2,4% del mercado de CMS
* Está disponible en 100 idiomas.
* Drupal está orientado a la comunidad y tiene más de 1,3 millones de miembros.
* Drupal 8 fue creado por 3.290 colaboradores, 1.288 empresas y la ayuda de la comunidad.
* 33 de las empresas Fortune 500 utilizan Drupal de alguna manera
* El 56% de los sitios web gubernamentales en todo el mundo utilizan Drupal
* El 23,8% de las universidades, colegios y escuelas utilizan Drupal en todo el mundo
* Algunas de las principales marcas que utilizan Drupal incluyen: Tesla y Warner Bros Records

Según el [sitio web](https://www.drupal.org/project/usage/drupal) de Drupal , en el momento de redactar este artículo hay alrededor de 950 000 instancias de Drupal en uso (distribuidas desde la versión 5.x hasta la versión 9.3.x, al 5 de septiembre de 2021). Como podemos ver en estas estadísticas, el uso de Drupal se ha mantenido estable entre 900 000 y 1,1 millones de instancias entre junio de 2013 y septiembre de 2021. Estas estadísticas no tienen en cuenta `EVERY`las instancias de Drupal en uso en todo el mundo, sino las instancias que ejecutan el módulo [Update Status](https://www.drupal.org/project/update_status) , que se comunica con drupal.org a diario para buscar nuevas versiones de Drupal o actualizaciones de los módulos en uso.

***

## <mark style="color:purple;">Discovery / Footprinting</mark>

Durante una prueba de penetración externa, nos encontramos con lo que parece ser un CMS, pero sabemos por una enumeración superficial que el sitio no utiliza WordPress ni Joomla. Sabemos que los CMS suelen ser objetivos "atrayentes", así que analicemos este caso y veamos qué podemos descubrir.

Un sitio web Drupal se puede identificar de varias maneras, incluso por el mensaje de encabezado o pie de página `Powered by Drupal`, el logotipo estándar de Drupal, la presencia de un archivo `CHANGELOG.txt` o `README.txt file`, a través del código fuente de la página o pistas en el archivo robots.txt como referencias a `/node`.

```shell-session
afsh4ck@kali$ curl -s http://drupal.inlanefreight.local | grep Drupal

<meta name="Generator" content="Drupal 8 (https://www.drupal.org)" />
      <span>Powered by <a href="https://www.drupal.org">Drupal</a></span>
```

Otra forma de identificar Drupal CMS es a través de [los nodos](https://www.drupal.org/docs/8/core/modules/node/about-nodes) . Drupal indexa su contenido mediante nodos. Un nodo puede contener cualquier cosa, como una publicación de blog, una encuesta, un artículo, etc. Las URL de las páginas suelen tener el formato `/node/<nodeid>`.  &#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/113/drupal_node.png" alt=""><figcaption></figcaption></figure>

Por ejemplo, la entrada del blog anterior se encuentra en `/node/1`. Esta representación es útil para identificar un sitio web Drupal cuando se utiliza un tema personalizado.

Nota: No todas las instalaciones de Drupal tendrán el mismo aspecto ni mostrarán la página de inicio de sesión o incluso permitirán a los usuarios acceder a la página de inicio de sesión desde Internet.

Drupal admite tres tipos de usuarios de forma predeterminada:

1. `Administrator`: Este usuario tiene control completo sobre el sitio web de Drupal.
2. `Authenticated User`: Estos usuarios pueden iniciar sesión en el sitio web y realizar operaciones como agregar y editar artículos según sus permisos.
3. `Anonymous`: Todos los visitantes del sitio web se consideran anónimos. De manera predeterminada, estos usuarios solo pueden leer publicaciones.

***

## <mark style="color:purple;">Enumeración</mark>

Una vez que hemos descubierto una instancia de Drupal, podemos hacer una combinación de enumeración manual y basada en herramientas (automatizada) para descubrir la versión, los complementos instalados y más. Según la versión de Drupal y las medidas de refuerzo que se hayan implementado, es posible que debamos probar varias formas de identificar el número de versión. Las instalaciones más nuevas de Drupal bloquean de forma predeterminada el acceso a los archivos `CHANGELOG.txt` y `README.txt`, por lo que es posible que debamos realizar una enumeración adicional. Veamos un ejemplo de enumeración del número de versión utilizando el archivo `CHANGELOG.txt` . Para ello, podemos utilizar `cURL` junto con `grep`, `sed`, `head`, etc.

```shell-session
afsh4ck@kali]$ curl -s http://drupal-acc.inlanefreight.local/CHANGELOG.txt | grep -m2 ""

Drupal 7.57, 2018-02-21
```

Aquí hemos identificado una versión anterior de Drupal en uso. Al probar esto con la última versión de Drupal en el momento de escribir este artículo, obtenemos una respuesta 404.

```shell-session
afsh4ck@kali$ curl -s http://drupal.inlanefreight.local/CHANGELOG.txt

<!DOCTYPE html><html><head><title>404 Not Found</title></head><body><h1>Not Found</h1><p>The requested URL "http://drupal.inlanefreight.local/CHANGELOG.txt" was not found on this server.</p></body></html>
```

Hay otras cosas que podríamos comprobar en este caso para identificar la versión.&#x20;

### Droopscan

{% embed url="<https://github.com/SamJoan/droopescan>" %}

Probemos un escaneo con `droopescan`. Ejecutemos un escaneo contra el host `http://drupal.inlanefreight.local`.

```bash
pip install droopescan
```

```shell-session
afsh4ck@kali$ droopescan scan drupal -u http://drupal.inlanefreight.local

[+] Plugins found:                                                              
    php http://drupal.inlanefreight.local/modules/php/
        http://drupal.inlanefreight.local/modules/php/LICENSE.txt

[+] No themes found.

[+] Possible version(s):
    8.9.0
    8.9.1

[+] Possible interesting urls found:
    Default admin - http://drupal.inlanefreight.local/user/login

[+] Scan finished (0:03:19.199526 elapsed)
```

Esta instancia parece estar ejecutando una versión `8.9.1`de Drupal. Al momento de escribir este artículo, no era la más reciente, ya que se lanzó en junio de 2020. Una búsqueda rápida de [vulnerabilidades](https://www.cvedetails.com/vulnerability-list/vendor_id-1367/product_id-2387/Drupal-Drupal.html) relacionadas con Drupal no muestra nada evidente para esta versión principal de Drupal. En este caso, lo siguiente que queremos hacer es analizar los complementos instalados o el abuso de la funcionalidad integrada.

***

## <mark style="color:purple;">Caso práctico</mark>

Identifique el número de versión de Drupal en uso en `http://drupal-qa.inlanefreight.local`

```
Objetivo(s): 10.129.48.231 

drupal.inlanefreight.local
drupal-qa.inlanefreight.local
```

<figure><img src="/files/z7zFFuJBggZecn6BKI1O" alt=""><figcaption></figcaption></figure>

```bash
droopescan scan drupal -u http://drupal-qa.inlanefreight.local

[+] Plugins found:                                                              
    profile http://drupal-qa.inlanefreight.local/modules/profile/
    php http://drupal-qa.inlanefreight.local/modules/php/
    image http://drupal-qa.inlanefreight.local/modules/image/

[+] Themes found:
    seven http://drupal-qa.inlanefreight.local/themes/seven/
    garland http://drupal-qa.inlanefreight.local/themes/garland/

[+] Possible version(s):
    7.30

[+] Possible interesting urls found:
    Default changelog file - http://drupal-qa.inlanefreight.local/CHANGELOG.txt
    Default admin - http://drupal-qa.inlanefreight.local/user/login

[+] Scan finished (0:02:27.786997 elapsed)
```

Encontramos correctamente la versión de Drupal: `7.30`
