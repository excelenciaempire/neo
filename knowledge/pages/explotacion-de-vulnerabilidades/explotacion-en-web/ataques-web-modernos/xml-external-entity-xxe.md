
# XML External Entity (XXE)

## <mark style="color:purple;">Introducción a XXE</mark>

Las vulnerabilidades `XML External Entity (XXE) Injection` ocurren cuando se toman datos XML de una entrada controlada por el usuario sin sanitizarlos o analizarlos de manera segura, lo que puede permitirnos usar funciones XML para realizar acciones maliciosas. Las vulnerabilidades XXE pueden causar daños considerables a una aplicación web y a su servidor back-end, desde la divulgación de archivos confidenciales hasta el apagado del servidor back-end, por lo que se considera uno de los [10 principales riesgos de seguridad web](https://owasp.org/www-project-top-ten/) según OWASP.

***

## <mark style="color:purple;">XML</mark>

`Extensible Markup Language (XML)` es un lenguaje de marcado común (similar a HTML y SGML) diseñado para la transferencia y el almacenamiento flexibles de datos y documentos en varios tipos de aplicaciones. XML no se centra en la visualización de datos, sino principalmente en el almacenamiento de datos de documentos y la representación de estructuras de datos. Los documentos XML están formados por árboles de elementos, donde cada elemento se denota esencialmente por un `tag`, y el primer elemento se llama `root element`, mientras que los demás elementos son `child elements`.

Aquí vemos un ejemplo básico de un documento XML que representa la estructura de un documento de correo electrónico:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<email>
  <date>01-01-2022</date>
  <time>10:00 am UTC</time>
  <sender>john@inlanefreight.com</sender>
  <recipients>
    <to>HR@inlanefreight.com</to>
    <cc>
        <to>billing@inlanefreight.com</to>
        <to>payslips@inlanefreight.com</to>
    </cc>
  </recipients>
  <body>
  Hello,
      Kindly share with me the invoice for the payment made on January 1, 2022.
  Regards,
  John
  </body> 
</email>
```

El ejemplo anterior muestra algunos de los elementos clave de un documento XML, como:

<table data-header-hidden><thead><tr><th width="171"></th><th width="321"></th><th></th></tr></thead><tbody><tr><td>Llave</td><td>Definición</td><td>Ejemplo</td></tr><tr><td><code>Etiqueta</code></td><td>Las claves de un documento XML, normalmente entre caracteres ( <code>&#x3C;</code>/ <code>></code>).</td><td><code>&#x3C;date></code></td></tr><tr><td><code>Entidad</code></td><td>Variables XML, normalmente entre caracteres ( <code>&#x26;</code>/ <code>;</code>).</td><td><code>&#x26;lt;</code></td></tr><tr><td><code>Elemento</code></td><td>El elemento raíz o cualquiera de sus elementos secundarios, y su valor se almacena entre una etiqueta de inicio y una etiqueta de fin.</td><td><code>&#x3C;date>01-01-2022&#x3C;/date></code></td></tr><tr><td><code>Atributo</code></td><td>Especificaciones opcionales para cualquier elemento almacenado en las etiquetas, que puede utilizar el analizador XML.</td><td><code>version="1.0"</code>/<code>encoding="UTF-8"</code></td></tr><tr><td><code>Declaración</code></td><td>Generalmente es la primera línea de un documento XML y define la versión XML y la codificación que se utilizará al analizarlo.</td><td><code>&#x3C;?xml version="1.0" encoding="UTF-8"?></code></td></tr></tbody></table>

Además, algunos caracteres se utilizan como parte de la estructura de un documento XML, como `<`, , o . Por lo tanto, si necesitamos usarlos en un documento XML, debemos reemplazarlos con sus referencias de entidad correspondientes (por ejemplo , `>`, , ). Finalmente, podemos escribir comentarios en documentos XML entre y , de manera similar a los documentos HTML.

```xml
&"&lt;&gt;&amp;&quot;<!-- Esto es un comentario en XML -->
```

***

## <mark style="color:purple;">DTD XML</mark>

`XML Document Type Definition (DTD)` permite la validación de un documento XML con respecto a una estructura de documento predefinida. La estructura de documento predefinida puede definirse en el propio documento o en un archivo externo. El siguiente es un ejemplo de DTD para el documento XML que vimos anteriormente:

```xml
<!DOCTYPE email [
  <!ELEMENT email (date, time, sender, recipients, body)>
  <!ELEMENT recipients (to, cc?)>
  <!ELEMENT cc (to*)>
  <!ELEMENT date (#PCDATA)>
  <!ELEMENT time (#PCDATA)>
  <!ELEMENT sender (#PCDATA)>
  <!ELEMENT to  (#PCDATA)>
  <!ELEMENT body (#PCDATA)>
]>
```

Como podemos ver, el DTD declara el elemento raíz `email` con la declaración de tipo `ELEMENT` y luego denota sus elementos secundarios. Después de eso, también se declara cada uno de los elementos secundarios, donde algunos de ellos también tienen elementos secundarios, mientras que otros pueden contener solo datos sin procesar (como se indica con `PCDATA`).

El DTD anterior se puede colocar dentro del documento XML, justo después de la `Declaración XML` de la primera línea. De lo contrario, se puede almacenar en un archivo externo (por ejemplo, `email.dtd`) y luego hacer referencia a él dentro del documento XML con la palabra clave `SYSTEM`, de la siguiente manera:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email SYSTEM "email.dtd">
```

También es posible referenciar una DTD a través de una URL, de la siguiente manera:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email SYSTEM "http://inlanefreight.com/email.dtd">
```

Esto es relativamente similar a cómo los documentos HTML definen y hacen referencia a los scripts JavaScript y CSS.

***

## <mark style="color:purple;">Entidades XML</mark>

También podemos definir entidades personalizadas (es decir, variables XML) en DTD XML, para permitir la refactorización de variables y reducir los datos repetitivos. Esto se puede hacer con el uso de la palabra clave `ENTITY`, seguida del nombre de la entidad y su valor, de la siguiente manera:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email [
  <!ENTITY company "Inlane Freight">
]>
```

Una vez que definimos una entidad, se puede hacer referencia a ella en un documento XML entre un ampersand `&` y un punto y coma `;`(por ejemplo, `&company;`). Siempre que se haga referencia a una entidad, el analizador XML la reemplazará con su valor. Sin embargo, lo más interesante es que podemos hacer `referencia a Entidades Externas XML` con la palabra clave `SYSTEM`, seguida de la ruta de la entidad externa, de la siguiente manera:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email [
  <!ENTITY company SYSTEM "http://localhost/company.txt">
  <!ENTITY signature SYSTEM "file:///var/www/html/signature.txt">
]>
```

{% hint style="info" %}
**Nota**: También podemos usar la palabra clave `PUBLIC` en lugar de `SYSTEM` para cargar recursos externos, lo que se usa con entidades y estándares declarados públicamente, como un código de idioma (`lang="en"`). En este módulo, usaremos `SYSTEM`, pero deberíamos poder usar cualquiera de los dos en la mayoría de los casos.
{% endhint %}

Esto funciona de manera similar a las entidades XML internas definidas dentro de los documentos. Cuando hacemos referencia a una entidad externa (por ejemplo, \&signature;), el analizador reemplazará la entidad con su valor almacenado en el archivo externo (por ejemplo, firma.txt). Cuando el archivo XML se analiza en el lado del servidor, en casos como API SOAP (XML) o formularios web, entonces una entidad puede hacer referencia a un archivo almacenado en el servidor back-end, que eventualmente puede ser revelado a nosotros cuando hagamos referencia al entidad.

En la siguiente sección, veremos cómo podemos utilizar entidades XML externas para leer archivos locales o incluso realizar acciones más maliciosas.
