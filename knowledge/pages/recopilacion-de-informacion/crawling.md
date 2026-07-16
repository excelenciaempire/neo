
# Crawling

## <mark style="color:purple;">Introducción</mark>

El `crawling` (tambien llamado `spidering`) es el proceso sistemático o automático de explorar un sitio web para enumerar todos los recursos encontrados. Nos muestra la estructura del sitio web que estamos auditando y una descripción general de la superficie de ataque que probaremos en el futuro. Utilizamos el proceso de crawling para encontrar tantas páginas y subdirectorios pertenecientes a un sitio web como sea posible.

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que hacen muchas peticiones al servidor del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

De manera similar a cómo una araña navega por su red, un rastreador web sigue enlaces de una página a otra y recopila información. Estos rastreadores son esencialmente robots que utilizan algoritmos predefinidos para descubrir e indexar páginas web, haciéndolas accesibles a través de motores de búsqueda o para otros fines como análisis de datos y reconocimiento web.

### Cómo funcionan los rastreadores web

El funcionamiento básico de un rastreador web es sencillo pero potente. Comienza con una URL inicial, que es la página web inicial a rastrear. El rastreador busca esta página, analiza su contenido y extrae todos sus enlaces. Luego agrega estos enlaces a una cola y los rastrea, repitiendo el proceso de forma iterativa. Dependiendo de su alcance y configuración, el rastreador puede explorar un sitio web completo o incluso una gran parte de la web.

1. `Homepage`: comienza con la página de inicio que contiene `link1`, `link2` y `link3`

```txt
Homepage
├── link1
├── link2
└── link3
```

2. `Visitar link1`: Al visitar `link1` se muestra la página de inicio, `link2` y también `link4`y `link5`

```txt
link1
├── Homepage
├── link2
├── link4
└── link5
```

3. `Continua el Crawling`: El rastreador continúa siguiendo estos enlaces sistemáticamente, recopilando todas las páginas accesibles y sus enlaces.

Este ejemplo ilustra cómo un rastreador web descubre y recopila información siguiendo enlaces sistemáticamente, distinguiéndolo de la confusión, que implica adivinar enlaces potenciales.

Hay dos tipos principales de estrategias de crawling:

#### Breadth-First Crawling

<figure><img src="/files/NTdFV5wzkfwwCy8zlRUt" alt=""><figcaption></figcaption></figure>

`Breadth-first crawling` prioriza explorar el ancho de un sitio web antes de profundizar. Comienza rastreando todos los enlaces de la página inicial, luego pasa a los enlaces de esas páginas, y así sucesivamente. Esto es útil para obtener una visión general amplia de la estructura y el contenido de un sitio web.

#### Depth-First Crawling

<figure><img src="/files/kwVKhYXQIc6BChffUu3y" alt=""><figcaption></figcaption></figure>

Por el contrario, `depth-first crawling` prioriza la profundidad sobre la amplitud. Sigue un único camino de enlaces en la medida de lo posible antes de retroceder y explorar otros caminos. Esto puede resultar útil para encontrar contenido específico o profundizar en la estructura de un sitio web.

La elección de la estrategia depende de los objetivos específicos del proceso de rastreo.

### Extraer información valiosa

Los rastreadores pueden extraer una amplia gama de datos, cada uno de los cuales tiene un propósito específico en el proceso de reconocimiento:

* `Links (Internos y Externos)`: Estos son los componentes fundamentales de la web, conectando páginas dentro de un sitio web (`links internos`) y con otros sitios web (`links internos`). Los rastreadores recopilan meticulosamente estos enlaces, lo que le permite trazar la estructura de un sitio web, descubrir páginas ocultas e identificar relaciones con recursos externos.
* `Comentarios`: Las secciones de comentarios en blogs, foros u otras páginas interactivas pueden ser una mina de oro de información. Los usuarios a menudo revelan sin darse cuenta detalles confidenciales, procesos internos o indicios de vulnerabilidades en sus comentarios.
* `Metadatos`: Los metadatos se refieren a `datos sobre datos`. En el contexto de las páginas web, incluye información como títulos de páginas, descripciones, palabras clave, nombres de autores y fechas. Estos metadatos pueden proporcionar un contexto valioso sobre el contenido, el propósito y la relevancia de una página para sus objetivos de reconocimiento.
* `Archivos sensibles`: Los rastreadores web se pueden configurar para buscar activamente archivos confidenciales que podrían quedar expuestos inadvertidamente en un sitio web. Esto incluye `backups`(p. ej. `.bak`, , `.old`), `archivos de configuración`(p. ej. `web.config`, `settings.php`), `archivos de log` (p. ej. `error_log`, `access_log`) y otros archivos que contienen contraseñas `API keys` u otra información confidencial. Examinar detenidamente los archivos extraídos, especialmente los archivos de copia de seguridad y de configuración, puede revelar una gran cantidad de información confidencial, como `credenciales de una base de datos`, `claves de encriptación` o incluso fragmentos de código fuente.

#### La importancia del contexto

Comprender el contexto que rodea los datos extraídos es primordial.

Un solo dato, como un comentario que mencione una versión de software específica, puede no parecer significativo por sí solo. Sin embargo, cuando se combina con otros hallazgos, como una versión desactualizada incluida en los metadatos o un archivo de configuración potencialmente vulnerable descubierto mediante el rastreo, puede transformarse en un indicador crítico de una vulnerabilidad potencial.

El verdadero valor de los datos extraídos radica en conectar los puntos y construir una imagen completa del panorama digital del objetivo.

Por ejemplo, una lista de enlaces extraídos puede parecer inicialmente mundana. Pero tras un examen más detenido, observa un patrón: varias URL apuntan a un directorio llamado `/files/`. Esto despierta su curiosidad y decide visitar manualmente el directorio. Para su sorpresa, descubre que la exploración de directorios está habilitada, lo que expone una gran cantidad de archivos, incluidos archivos de respaldo, documentos internos y datos potencialmente confidenciales. Este descubrimiento no habría sido posible simplemente observando enlaces individuales de forma aislada; El análisis contextual lo llevó a este hallazgo crítico.

De manera similar, comentarios aparentemente inofensivos pueden adquirir importancia cuando se correlacionan con otros descubrimientos. Es posible que un comentario que mencione un "servidor de archivos" no genere ninguna señal de alerta inicialmente. Sin embargo, cuando se combina con el descubrimiento del `/files/`directorio antes mencionado, refuerza la posibilidad de que el servidor de archivos sea de acceso público, lo que podría exponer información sensible o datos confidenciales.

Por lo tanto, es esencial abordar el análisis de datos de manera integral, considerando las relaciones entre los diferentes puntos de datos y sus posibles implicaciones para sus objetivos de reconocimiento.

***

## <mark style="color:purple;">Robots.txt</mark>

Imagina que eres un invitado a una gran fiesta en una casa. Si bien eres libre de socializar y explorar, es posible que haya ciertas salas marcadas como "Privadas" que se espera que evites. Esto es similar a cómo funciona `robots.txt` en el mundo del rastreo web. Actúa como una "`guía de etiquetado`" virtual para los bots, describiendo a qué áreas de un sitio web se les permite acceder y cuáles están prohibidas.

### ¿Qué es robots.txt?

Técnicamente, `robots.txt` es un archivo de texto simple ubicado en el directorio raíz de un sitio web (por ejemplo, `www.example.com/robots.txt`). Cumple con el Estándar de exclusión de robots, pautas sobre cómo deben comportarse los rastreadores web cuando visitan un sitio web. Este archivo contiene instrucciones en forma de "directivas" que indican a los robots qué partes del sitio web pueden y no pueden rastrear.

#### Cómo funciona el archivo robots.txt

Las directivas en robots.txt generalmente apuntan a `user-agents` específicos, que son identificadores para diferentes tipos de bots. Por ejemplo, una directiva podría verse así:

```txt
User-agent: *
Disallow: /private/
```

Esta directiva les dice a todos los User-agent ( `*`es un comodín) que no pueden acceder a ninguna URL que comience con `/private/`. Otras directivas pueden permitir el acceso a directorios o archivos específicos, establecer retrasos en el rastreo para evitar sobrecargar un servidor o proporcionar enlaces a sitemaps para un rastreo eficiente.

### Estructura de robots.txt

El archivo robots.txt es un documento de texto sin formato que se encuentra en el directorio raíz de un sitio web. Sigue una estructura sencilla, con cada conjunto de instrucciones, o "registro", separados por una línea en blanco. Cada registro consta de dos componentes principales:

1. `User-agent`: esta línea especifica a qué rastreador o bot se aplican las siguientes reglas. Un comodín ( `*`) indica que las reglas se aplican a todos los bots. También se pueden seleccionar agentes de usuario específicos, como "Googlebot" (el rastreador de Google) o "Bingbot" (el rastreador de Microsoft).
2. `Directivas`: Estas líneas proporcionan instrucciones específicas al usuario-agente identificado.

Las directivas comunes incluyen:

<table data-header-hidden><thead><tr><th width="167"></th><th width="321"></th><th></th></tr></thead><tbody><tr><td>Directiva</td><td>Descripción</td><td>Ejemplo</td></tr><tr><td><code>Disallow</code></td><td>Especifica rutas o patrones que el bot no debe rastrear.</td><td><code>Disallow: /admin/</code>(no permite el acceso al directorio de administración)</td></tr><tr><td><code>Allow</code></td><td>Permite explícitamente que el bot rastree rutas o patrones específicos, incluso si se encuentran bajo una regla <code>Disallow</code> más amplia.</td><td><code>Allow: /public/</code>(permite el acceso al directorio público)</td></tr><tr><td><code>Crawl-delay</code></td><td>Establece un retraso (en segundos) entre solicitudes sucesivas del bot para evitar sobrecargar el servidor.</td><td><code>Crawl-delay: 10</code>(Retraso de 10 segundos entre solicitudes)</td></tr><tr><td><code>Sitemap</code></td><td>Proporciona la URL de un mapa del sitio XML para un rastreo más eficiente.</td><td><code>Sitemap: https://www.example.com/sitemap.xml</code></td></tr></tbody></table>

#### ¿Por qué respetar el archivo robots.txt?

Si bien el archivo robots.txt no se puede aplicar estrictamente (un robot malicioso aún podría ignorarlo), la mayoría de los rastreadores web y robots de motores de búsqueda legítimos respetarán sus directivas. Esto es importante por varias razones:

* `Evitar sobrecargar los servidores`: Al limitar el acceso de los rastreadores a ciertas áreas, los propietarios de sitios web pueden evitar un tráfico excesivo que podría ralentizar o incluso bloquear sus servidores.
* `Proteger información sensible`: Robots.txt puede proteger la información privada o confidencial para que no sea indexada por los motores de búsqueda.
* `Cumplimiento Legal y Ético`: En algunos casos, ignorar las directivas de robots.txt podría considerarse una violación de los términos de servicio de un sitio web o incluso una cuestión legal, especialmente si implica acceder a datos privados o protegidos por derechos de autor.

### Robots.txt en Reconocimiento Web

Para el reconocimiento web, robots.txt constituye una valiosa fuente de inteligencia. Si bien respetan las directivas descritas en este archivo, los profesionales de la seguridad pueden obtener información crucial sobre la estructura y las posibles vulnerabilidades de un sitio web objetivo:

* `Descubrir directorios ocultos`: Las rutas no permitidas en robots.txt a menudo apuntan a directorios o archivos que el propietario del sitio web desea intencionalmente mantener fuera del alcance de los rastreadores de los motores de búsqueda. Estas áreas ocultas pueden albergar información confidencial, archivos de respaldo, paneles administrativos u otros recursos que podrían interesar a un atacante.
* `Mapeo de la estructura del sitio web`: Al analizar las rutas permitidas y no permitidas, los profesionales de seguridad pueden crear un mapa rudimentario de la estructura del sitio web. Esto puede revelar secciones que no están vinculadas desde la navegación principal, lo que podría conducir a páginas o funcionalidades no descubiertas.
* `Detectar Crawler Traps`: Algunos sitios web incluyen intencionalmente directorios "honeypot" en robots.txt para atraer robots maliciosos. La identificación de dichas trampas puede proporcionar información sobre la conciencia de seguridad y las medidas defensivas del objetivo.

#### Analizando robots.txt

A continuación se muestra un ejemplo de un archivo robots.txt:

```txt
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /public/

User-agent: Googlebot
Crawl-delay: 10

Sitemap: https://www.example.com/sitemap.xml
```

Este archivo contiene las siguientes directivas:

* Ningún user-agent puede acceder a los directorios `/admin/` y `/private/`
* Todos los user-agent pueden acceder al directorio `/public/`
* `Googlebot` (El rastreador web de Google) recibe instrucciones específicas de esperar 10 segundos entre solicitudes.
* El sitemap, ubicado en `https://www.example.com/sitemap.xml`, se proporciona para facilitar el rastreo y la indexación.

Al analizar este archivo robots.txt, podemos inferir que el sitio web probablemente tenga un panel de administración ubicado `/admin/` y algún contenido privado en el `/private/` directorio.

***

## <mark style="color:purple;">Well-Known URLs</mark>

El estándar `.well-known`, definido en [RFC 8615](https://datatracker.ietf.org/doc/html/rfc8615) , sirve como un directorio estandarizado dentro del dominio raíz de un sitio web. Esta ubicación designada, generalmente accesible a través de la ruta `/.well-known/` de un servidor web, centraliza los metadatos críticos de un sitio web, incluidos archivos de configuración e información relacionada con sus servicios, protocolos y mecanismos de seguridad.

Al establecer una ubicación coherente para dichos datos, `.well-known` simplifica el proceso de descubrimiento y acceso para diversas partes interesadas, incluidos navegadores web, aplicaciones y herramientas de seguridad. Este enfoque simplificado permite a los clientes localizar y recuperar automáticamente archivos de configuración específicos mediante la construcción de la URL adecuada. Por ejemplo, para acceder a la política de seguridad de un sitio web, un cliente solicitaría `https://example.com/.well-known/security.txt`.

( IANA - `Internet Assigned Numbers Authority`) mantiene un [registro](https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml) de URI, cada uno de los cuales tiene un propósito específico definido por varias especificaciones y estándares. A continuación se muestra una tabla que destaca algunos ejemplos notables:`IANA.well-known`

<table data-header-hidden><thead><tr><th width="202"></th><th width="229"></th><th width="128"></th><th></th></tr></thead><tbody><tr><td>Sufijo URI</td><td>Descripción</td><td>Estado</td><td>Referencia</td></tr><tr><td><code>security.txt</code></td><td>Contiene información de contacto para que los investigadores de seguridad informen vulnerabilidades.</td><td>Permanente</td><td>RFC 9116</td></tr><tr><td><code>/.well-known/change-password</code></td><td>Proporciona una URL estándar para dirigir a los usuarios a una página de cambio de contraseña.</td><td>Provisional</td><td>https://w3c.github.io/webappsec-change-password-url/#the-change-password-well-known-uri</td></tr><tr><td><code>openid-configuration</code></td><td>Define los detalles de configuración para OpenID Connect, una capa de identidad además del protocolo OAuth 2.0.</td><td>Permanente</td><td>http://openid.net/specs/openid-connect-discovery-1_0.html</td></tr><tr><td><code>assetlinks.json</code></td><td>Se utiliza para verificar la propiedad de activos digitales (por ejemplo, aplicaciones) asociados con un dominio.</td><td>Permanente</td><td>https://github.com/google/digitalassetlinks/blob/master/well-known/specification.md</td></tr><tr><td><code>mta-sts.txt</code></td><td>Especifica la política de seguridad de transporte estricta SMTP MTA (MTA-STS) para mejorar la seguridad del correo electrónico.</td><td>Permanente</td><td>RFC 8461</td></tr></tbody></table>

Esta es sólo una pequeña muestra de los muchos `.well-known`URI registrados en la IANA. Cada entrada en el registro ofrece pautas y requisitos específicos para la implementación, lo que garantiza un enfoque estandarizado para aprovechar el mecanismo `.well-known` para diversas aplicaciones.

### .well-known en Reconocimiento Web

En el reconocimiento web, las URLs `.well-known` pueden ser invaluables para descubrir endpoints y detalles de configuración que se pueden probar más durante una prueba de penetración. Un URI particularmente útil es `openid-configuration`.

El `openid-configuration` es parte del protocolo OpenID Connect Discovery, una capa de identidad construida sobre el protocolo OAuth 2.0. Cuando una aplicación cliente desea utilizar OpenID Connect para la autenticación, puede recuperar la configuración del proveedor de OpenID Connect accediendo al endpoint `https://example.com/.well-known/openid-configuration`. Este endpoint devuelve un documento JSON que contiene metadatos sobre los endpoints del proveedor, métodos de autenticación admitidos, emisión de tokens y más:

```json
{
  "issuer": "https://example.com",
  "authorization_endpoint": "https://example.com/oauth2/authorize",
  "token_endpoint": "https://example.com/oauth2/token",
  "userinfo_endpoint": "https://example.com/oauth2/userinfo",
  "jwks_uri": "https://example.com/oauth2/jwks",
  "response_types_supported": ["code", "token", "id_token"],
  "subject_types_supported": ["public"],
  "id_token_signing_alg_values_supported": ["RS256"],
  "scopes_supported": ["openid", "profile", "email"]
}
```

La información obtenida del endpoint `openid-configuration` brinda múltiples oportunidades de exploración:

1. `Endpoint Discovery`:

* `Authorization Endpoint`: Identifica la URL para las solicitudes de autorización de usuarios.
* `Token Endpoint`: Encuentra la URL donde se emiten los tokens.
* `Userinfo Endpoint`: Localización del endpoint que proporciona información del usuario.

2. `JWKS URI`: `jwks_uri` revela el `JSON Web Key Set`( `JWKS`), detallando las claves criptográficas utilizadas por el servidor.
3. `Alcances admitidos y tipos de respuesta`: Comprender qué alcances y tipos de respuesta se admiten ayuda a mapear la funcionalidad y las limitaciones de la implementación de OpenID Connect.
4. `Detalles del algoritmo`: La información sobre los algoritmos de firma admitidos puede ser crucial para comprender las medidas de seguridad implementadas.

Explorar el [Registro de la IANA](https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml) y experimentar con los distintos `.well-known`URI es un enfoque invaluable para descubrir oportunidades adicionales de reconocimiento web. Como se demostró con el punto anterior `openid-configuration`, estos URI estandarizados brindan acceso estructurado a metadatos críticos y detalles de configuración, lo que permite a los profesionales de la seguridad trazar de manera integral el panorama de seguridad de un sitio web.
