
# Infraestructura - Pasiva

## <mark style="color:purple;">Netcraft</mark>

[Netcraft](https://www.netcraft.com/) puede ofrecernos información sobre los servidores sin siquiera interactuar con ellos, y esto es algo valioso desde el punto de vista de la recopilación pasiva de información. Podemos utilizar el servicio visitando [`https://sitereport.netcraft.com`](https://sitereport.netcraft.com)e ingresando el dominio objetivo.

<figure><img src="/files/hZcimjqzwyGbKIbUJSkx" alt=""><figcaption></figcaption></figure>

Algunos detalles interesantes que podemos observar en el informe son:

<table><thead><tr><th width="208"></th><th></th></tr></thead><tbody><tr><td><code>Background</code></td><td>Información general sobre el dominio, incluida la fecha en que los rastreadores de Netcraft lo vieron por primera vez.</td></tr><tr><td><code>Network</code></td><td>Información sobre el propietario del netblock, la empresa de alojamiento, los servidores de nombres, etc.</td></tr><tr><td><code>Hosting history</code></td><td>Últimas IP utilizadas, servidor web y sistema operativo de destino.</td></tr></tbody></table>

Debemos prestar especial atención a las últimas IP utilizadas. A veces podemos detectar la dirección IP real del servidor web antes de que se colocara detrás de un balanceador de carga, un firewall de aplicaciones web o un IDS, lo que nos permite conectarnos directamente a él si la configuración lo permite. Este tipo de tecnología podría interferir o alterar nuestras futuras actividades de prueba.

***

## <mark style="color:purple;">Wayback Machine</mark>

Internet [Archive](https://en.wikipedia.org/wiki/Internet_Archive) es una biblioteca digital estadounidense que brinda acceso público gratuito a materiales digitalizados, incluidos sitios web, recopilados automáticamente a través de sus rastreadores web.

Podemos acceder a varias versiones de estos sitios web utilizando [Wayback Machine](http://web.archive.org/) para encontrar versiones antiguas que puedan tener comentarios interesantes en el código fuente o archivos que no deberían estar allí. Esta herramienta se puede utilizar para encontrar versiones anteriores de un sitio web en un momento dado. Tomemos como ejemplo un sitio web que ejecuta WordPress. Es posible que no encontremos nada interesante al evaluarlo utilizando métodos manuales y herramientas automatizadas, por lo que lo buscamos usando Wayback Machine y encontramos una versión que utiliza un complemento específico (ahora vulnerable). Volviendo a la versión actual del sitio, encontramos que el complemento no se eliminó correctamente y aún se puede acceder a él a través del directorio `wp-content`. Luego podemos utilizarlo para obtener la ejecución remota de código en el host.

![imagen](https://academy.hackthebox.com/storage/modules/144/wayback1.png)

Podemos consultar una de las primeras versiones capturadas de `facebook.com` el 1 de diciembre de 2005, lo cual es interesante, quizás nos da una sensación de nostalgia pero también es sumamente útil para nosotros como investigadores de seguridad.

<figure><img src="/files/U6ynmJApig7MK4hmbRhr" alt=""><figcaption></figcaption></figure>

También podemos utilizar la herramienta [waybackurls](https://github.com/tomnomnom/waybackurls) para inspeccionar las URL guardadas por Wayback Machine y buscar palabras clave específicas. Siempre que hayamos `Go`configurado correctamente en nuestro host, podemos instalar la herramienta de la siguiente manera:

```bash
go install github.com/tomnomnom/waybackurls@latest
```

Para obtener una lista de URL rastreadas de un dominio con la fecha en que se obtuvo, podemos agregar el modificador `-dates` a nuestro comando de la siguiente manera:

```bash
afsh4ck$ waybackurls -dates https://facebook.com > waybackurls.txt
afsh4ck$ cat waybackurls.txt

2018-05-20T09:46:07Z http://www.facebook.com./
2018-05-20T10:07:12Z https://www.facebook.com/
2018-05-20T10:18:51Z http://www.facebook.com/#!/pages/Welcome-Baby/143392015698061?ref=tsrobots.txt
2018-05-20T10:19:19Z http://www.facebook.com/
2018-05-20T16:00:13Z http://facebook.com
2018-05-21T22:12:55Z https://www.facebook.com
2018-05-22T15:14:09Z http://www.facebook.com
2018-05-22T17:34:48Z http://www.facebook.com/#!/Syerah?v=info&ref=profile/robots.txt
2018-05-23T11:03:47Z http://www.facebook.com/#!/Bin595

<SNIP>
```

Si queremos acceder a un recurso específico, debemos colocar la URL en el menú de búsqueda y navegar hasta la fecha en que se creó la instantánea. Como se indicó anteriormente, Wayback Machine puede ser una herramienta útil y no debe pasarse por alto. Es muy probable que nos lleve a descubrir activos, páginas, etc. olvidados, lo que puede llevarnos a descubrir una falla.

***

## <mark style="color:purple;">Reconocimiento Activo de Infraestructura</mark>

En la siguiente sección veremos otras técnicas de reconocimiento, en este caso activas de una infraestructura:

{% content-ref url="/pages/tJy7DwMM7xKe9I9jPo3d" %}
[Infraestructura - Activa](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-activa/infraestructura-activa.md)
{% endcontent-ref %}
