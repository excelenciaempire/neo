
# Ataques Web Modernos

## <mark style="color:purple;">Introducción a los ataques web</mark>

***

A medida que las aplicaciones web se vuelven cada vez más comunes y se utilizan en la mayoría de las empresas, la importancia de protegerlas contra ataques maliciosos también se vuelve más crítica. A medida que las aplicaciones web modernas se vuelven más complejas y avanzadas, también lo hacen los tipos de ataques utilizados contra ellas. Esto genera una amplia superficie de ataque para la mayoría de las empresas en la actualidad, por lo que los ataques web son los tipos de ataques más comunes contra las empresas. Proteger las aplicaciones web se está convirtiendo en una de las principales prioridades para cualquier departamento de TI.

Los ataques a aplicaciones web externas pueden poner en riesgo la red interna de la empresa, lo que puede derivar en el robo de activos o la interrupción de servicios. Esto puede provocar un desastre financiero para la empresa. Incluso si una empresa no tiene aplicaciones web externas, es probable que utilice aplicaciones web internas o puntos finales de API externos, ambos vulnerables a los mismos tipos de ataques y que pueden aprovecharse para lograr los mismos objetivos.

En este módulo, cubriremos tres ataques web que pueden encontrarse en cualquier aplicación web, que pueden llevar a una vulneración. Analizaremos cómo detectar, explotar y prevenir cada uno de estos tres ataques.

***

## <mark style="color:purple;">Ataques web</mark>

### **HTTP Verb Tampering**

El primer ataque web que se analiza en este módulo es [HTTP Verb Tampering](https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/03-Testing_for_HTTP_Verb_Tampering) . Este ataque explota servidores web que aceptan muchos verbos y métodos HTTP. Esto se puede explotar enviando solicitudes maliciosas mediante métodos inesperados, lo que puede llevar a eludir el mecanismo de autorización de la aplicación web o incluso a eludir sus controles de seguridad contra otros ataques web. Los ataques HTTP Ver Tampering son uno de los muchos otros ataques HTTP que se pueden utilizar para explotar las configuraciones de servidores web mediante el envío de solicitudes HTTP maliciosas.

### **Insecure Direct Object References (IDOR)**

El segundo ataque que se analiza en este módulo es el [Insecure Direct Object References (IDOR)](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References). IDOR es una de las vulnerabilidades web más comunes y puede llevar al acceso a datos a los que los atacantes no deberían tener acceso. Lo que hace que este ataque sea muy común es, esencialmente, la falta de un sistema de control de acceso sólido en el back-end. Como las aplicaciones web almacenan archivos e información de los usuarios, pueden usar números secuenciales o identificadores de usuario para identificar cada elemento. Supongamos que la aplicación web carece de un mecanismo de control de acceso sólido y expone referencias directas a archivos y recursos. En ese caso, podemos acceder a los archivos e información de otros usuarios simplemente adivinando o calculando sus identificadores de archivo.

### **XML External Entity (XXE) Injection**

El tercer y último ataque web que analizaremos es [XML External Entity (XXE) Injection](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_\(XXE\)_Processing). Muchas aplicaciones web procesan datos XML como parte de su funcionalidad. Supongamos que una aplicación web utiliza bibliotecas XML obsoletas para analizar y procesar datos de entrada XML del usuario front-end. En ese caso, es posible enviar datos XML maliciosos para revelar archivos locales almacenados en el servidor back-end. Estos archivos pueden ser archivos de configuración que pueden contener información confidencial, como contraseñas o incluso el código fuente de la aplicación web, lo que nos permitiría realizar una prueba de penetración de caja blanca en la aplicación web para identificar más vulnerabilidades. Los ataques XXE incluso se pueden aprovechar para robar las credenciales del servidor de alojamiento, lo que comprometería todo el servidor y permitiría la ejecución remota de código.

Comencemos analizando el primero de estos ataques en la siguiente sección.
