
# Ataques de subida de archivos

## <mark style="color:purple;">Introducción</mark>

***

La carga de archivos se ha convertido en una característica clave para la mayoría de las aplicaciones web modernas, ya que permiten la extensibilidad de las aplicaciones web con información de los usuarios. Un sitio web de redes sociales permite cargar imágenes de perfil de usuario y otras redes sociales, mientras que un sitio web corporativo puede permitir a los usuarios cargar archivos PDF y otros documentos para uso corporativo.

Sin embargo, cuando los desarrolladores de aplicaciones web habilitan esta función, también corren el riesgo de permitir que los usuarios finales almacenen sus datos potencialmente maliciosos en el servidor back-end de la aplicación web. Si los datos ingresados ​​por el usuario y los archivos cargados no se filtran y validan correctamente, los atacantes pueden aprovechar la función de carga de archivos para realizar actividades maliciosas, como ejecutar comandos en el servidor back-end para tomar el control del mismo.

Las vulnerabilidades de carga de archivos se encuentran entre las vulnerabilidades más comunes que se encuentran en aplicaciones web y móviles, como podemos ver en los últimos [informes CVE](https://www.cvedetails.com/vulnerability-list/cweid-434/vulnerabilities.html) . También observaremos que la mayoría de estas vulnerabilidades se califican como `High`o `Critical`vulnerabilidades, lo que muestra el nivel de riesgo que causa la carga insegura de archivos.

***

## <mark style="color:purple;">Tipos de ataques de subida de archivos</mark>

La razón más común detrás de las vulnerabilidades de carga de archivos es una validación y verificación deficiente de archivos, que pueden no estar bien protegidas para evitar tipos de archivos no deseados o pueden no estar presentes en absoluto. El peor tipo posible de vulnerabilidad de carga de archivos es una vulnerabilidad `unauthenticated arbitrary file upload`. Con este tipo de vulnerabilidad, una aplicación web permite que cualquier usuario no autenticado cargue cualquier tipo de archivo, lo que la deja a un paso de permitir que cualquier usuario ejecute código en el servidor back-end.

Muchos desarrolladores web emplean distintos tipos de pruebas para validar la extensión o el contenido del archivo cargado. Sin embargo, como veremos en este módulo, si estos filtros no son seguros, es posible que podamos eludirlos y, aun así, acceder a archivos cargados de forma arbitraria para realizar nuestros ataques.

El ataque más común y crítico causado por la carga arbitraria de archivos se produce `ganando ejecución remota de comandos` a través del servidor back-end mediante la carga de un webshell o la carga de un script que envía un reverse shell. Un shell web, como veremos en la siguiente sección, nos permite ejecutar cualquier comando que especifiquemos y se puede convertir en un shell interactivo para enumerar el sistema fácilmente y explotar aún más la red. También es posible cargar un script que envíe un shell inverso a un receptor en nuestra máquina y luego interactuar con el servidor remoto de esa manera.

En algunos casos, es posible que no podamos cargar archivos arbitrarios y que solo podamos cargar un tipo de archivo específico. Incluso en estos casos, existen varios ataques que podemos realizar para explotar la funcionalidad de carga de archivos si faltan ciertas protecciones de seguridad en la aplicación web.

Algunos ejemplos de estos ataques incluyen:

* Introduciendo otras vulnerabilidades como `XSS` o `XXE`.
* Provocando un error `Denial of Service (DoS)` en el servidor back-end.
* Sobrescribir archivos y configuraciones críticos del sistema.
* Y muchos otros.

Por último, una vulnerabilidad de carga de archivos no solo se produce por escribir funciones inseguras, sino que también suele deberse al uso de bibliotecas obsoletas que pueden ser vulnerables a estos ataques. Al final del módulo, repasaremos varios consejos y prácticas para proteger nuestras aplicaciones web contra los tipos más comunes de ataques de carga de archivos, además de otras recomendaciones para evitar vulnerabilidades de carga de archivos que podamos pasar por alto.
