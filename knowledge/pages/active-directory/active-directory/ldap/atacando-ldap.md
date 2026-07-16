
# Atacando LDAP

El Lightweight Directory Access Protocol **(LDAP)** se utiliza para acceder y administrar información de directorios. Un **directorio** es un almacén de datos jerárquico que contiene información sobre recursos de red como **usuarios, grupos, computadoras, impresoras y otros dispositivos**. LDAP proporciona algunas funciones excelentes:

* **`Autenticación centralizada`:** Permite a los usuarios autenticarse en múltiples sistemas utilizando un solo conjunto de credenciales.
* **`Gestión de usuarios y grupos`:** Facilita la administración de cuentas de usuario y permisos dentro de una organización.
* **`Acceso eficiente a la información`:** Permite la búsqueda rápida de datos en el directorio.
* **`Interoperabilidad`:** Compatible con diversas plataformas y servicios.

Sin embargo, también presenta algunos problemas importantes:

* **`Seguridad`:** Sin cifrado, LDAP puede ser vulnerable a ataques de interceptación de credenciales.
* **`Complejidad`:** Requiere configuración y mantenimiento adecuados para garantizar su eficacia.
* **`Rendimiento`:** Para grandes volúmenes de datos, pueden surgir problemas de latencia.

## <mark style="color:purple;">Uso de LDAP</mark>

LDAP se usa comúnmente para proporcionar **servicios de directorio** y una **ubicación central** para la administración de datos. Los **servicios de directorio** son colecciones de información sobre la organización, sus usuarios y activos, como nombres de usuario y contraseñas. LDAP permite a las organizaciones almacenar, administrar y proteger esta información de manera estandarizada.\
A continuación, se presentan algunos casos de uso comunes:

* **Autenticación de usuarios:** Integración con sistemas de inicio de sesión único (SSO).
* **Gestión de accesos:** Control sobre qué usuarios pueden acceder a qué recursos.
* **Búsqueda de información organizativa:** Recuperación de detalles de empleados o recursos de red.
* **Integración con otras aplicaciones:** Comunicación con sistemas como correo electrónico o bases de datos.

## <mark style="color:purple;">Implementaciones Populares de LDAP</mark>

Existen dos implementaciones populares de LDAP:

<table><thead><tr><th width="303">Implementación</th><th>Descripción</th></tr></thead><tbody><tr><td><strong>OpenLDAP</strong></td><td>Software de código abierto ampliamente utilizado y compatible con múltiples sistemas.</td></tr><tr><td><strong>Microsoft Active Directory (AD)</strong></td><td>Implementación basada en Windows que se integra perfectamente con otros productos y servicios de Microsoft.</td></tr></tbody></table>

Aunque **LDAP y AD están relacionados**, sirven para propósitos diferentes:

* **LDAP** es un **protocolo** que especifica el método de acceso y modificación de servicios de directorio.
* **AD** es un **servicio de directorio** que almacena y administra datos de usuarios y equipos.
* LDAP puede **comunicarse** con AD y otros servicios de directorio, pero no es un servicio de directorio en sí mismo.
* **Active Directory** ofrece funcionalidades adicionales, como **administración de políticas**, **inicio de sesión único (SSO)** e **integración con productos de Microsoft**.

## <mark style="color:purple;">¿Cómo funciona LDAP?</mark>

LDAP funciona mediante una arquitectura **cliente-servidor**.\
Un **cliente** envía una solicitud **LDAP** a un **servidor**, que busca en el servicio de directorio y devuelve una respuesta al cliente.

LDAP es más simple y eficiente que **X.500**, en el que se basa. Utiliza un modelo cliente-servidor donde:

1. Los **clientes** envían solicitudes a los servidores mediante mensajes LDAP codificados en **ASN.1** (Abstract Syntax Notation One).
2. Se transmiten a través de **TCP/IP** (Transmission Control Protocol/Internet Protocol).
3. Los **servidores** procesan las solicitudes y envían respuestas utilizando el mismo formato.

LDAP admite varias solicitudes, tales como:

* **bind** (autenticación)
* **unbind** (desconexión)
* **search** (búsqueda)
* **compare** (comparación de datos)
* **add** (agregar entrada)
* **delete** (eliminar entrada)
* **modify** (modificación de atributos)

### Solicitudes LDAP

Las solicitudes **LDAP** son los mensajes de datos que los **clientes** envían a los **servidores** para realizar operaciones en un servicio de directorio.

<table><thead><tr><th width="254">Componente</th><th>Descripción</th></tr></thead><tbody><tr><td><strong>Conexión de sesión</strong></td><td>El cliente se conecta al servidor a través de un puerto LDAP (normalmente <strong>389</strong> para LDAP sin cifrar o <strong>636</strong> para LDAP con SSL/TLS).</td></tr><tr><td><strong>Tipo de solicitud</strong></td><td>El cliente especifica la operación que desea realizar, como <strong>bind, search, add, delete, modify</strong>.</td></tr><tr><td><strong>Parámetros de solicitud</strong></td><td>Incluyen el <strong>nombre distintivo (DN)</strong> de la entrada a la que se accederá o modificará, el <strong>alcance y filtro</strong> de la consulta de búsqueda, los <strong>atributos y valores</strong> a agregar o cambiar, etc.</td></tr><tr><td><strong>ID de solicitud</strong></td><td>El cliente asigna un <strong>identificador único</strong> para cada solicitud, lo que permite hacer coincidir la respuesta del servidor.</td></tr></tbody></table>

Una vez que el servidor recibe la solicitud, la procesa y envía un mensaje de **respuesta** que incluye:

<table><thead><tr><th width="257">Componente</th><th>Descripción</th></tr></thead><tbody><tr><td><strong>Tipo de respuesta</strong></td><td>Indica la operación que se realizó en respuesta a la solicitud del cliente.</td></tr><tr><td><strong>Código de resultado</strong></td><td>Indica si la operación fue exitosa o fallida y proporciona un motivo en caso de error.</td></tr><tr><td><strong>DN coincidente</strong></td><td>Si corresponde, devuelve el <strong>DN</strong> de la entrada existente más cercana que coincide con la solicitud.</td></tr><tr><td><strong>Referencia</strong></td><td>Si aplica, el servidor devuelve una URL de otro servidor que puede tener más información sobre la solicitud.</td></tr><tr><td><strong>Datos de respuesta</strong></td><td>Devuelve cualquier dato adicional relacionado con la respuesta, como los atributos y valores de una entrada que se buscó o modificó.</td></tr></tbody></table>

### Desconexión

Después de recibir y procesar la respuesta, el cliente **se desconecta** del puerto **LDAP**, finalizando la comunicación con el servidor.

## <mark style="color:purple;">**LdapSearch**</mark>

`ldapsearch` es una utilidad de línea de comandos que se utiliza para buscar información almacenada en un directorio mediante el protocolo LDAP. Se utiliza habitualmente para consultar y recuperar datos de un servicio de directorio LDAP.

```shell-session
afsh4ck@kali$ ldapsearch -H ldap://ldap.example.com:389 -D "cn=admin,dc=example,dc=com" -w secret123 -b "ou=people,dc=example,dc=com" "(mail=john.doe@example.com)"
```

Este comando se puede desglosar de la siguiente manera:

* Conectarse al servidor `ldap.example.com` en el puerto `389`.
* Vincular (autenticar) como `cn=admin,dc=example,dc=com` con contraseña `secret123`.
* Buscar bajo el DN base `ou=people,dc=example,dc=com`.
* Utilizar el filtro `(mail=john.doe@example.com)` para encontrar entradas que tengan esta dirección de correo electrónico.

El servidor procesaría la solicitud y enviaría una respuesta, que podría verse así:

```ldap
dn: uid=jdoe,ou=people,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: top
cn: John Doe
sn: Doe
uid: jdoe
mail: john.doe@example.com

result: 0 Success
```

Esta respuesta incluye las entradas `distinguished name (DN)`que coinciden con los criterios de búsqueda y sus atributos y valores.

***

## <mark style="color:purple;">Inyección LDAP</mark>

`LDAP injection` es un ataque que `explota aplicaciones web que usan LDAP` para la autenticación o el almacenamiento de información del usuario. El atacante puede `inyectar código malicioso` o `caractéres` en consultas LDAP para alterar el comportamiento de la aplicación, `evitar medidas de seguridad y acceder a datos confidenciales` que se almacena en el directorio LDAP.

Para probar la inyección LDAP, puede utilizar valores de entrada que contengan `caracteres especiales o operadores` lo que puede cambiar el significado de la consulta:

<table data-header-hidden><thead><tr><th width="130"></th><th></th></tr></thead><tbody><tr><td>Caracter</td><td>Descripción</td></tr><tr><td><code>*</code></td><td>Un asterisco <code>*</code> puede coincidir con cualquier número de caracteres.</td></tr><tr><td><code>( )</code></td><td>Los paréntesis <code>( )</code>pueden <code>agrupar expresiones</code>.</td></tr><tr><td><code>|</code></td><td>Una barra vertical <code>|</code> puede realizar <code>logical OR</code>.</td></tr><tr><td><code>&#x26;</code></td><td>Un ampersand <code>&#x26;</code> puede funcionar como <code>logical AND</code>.</td></tr><tr><td><code>(cn=*)</code></td><td>Valores de entrada que intentan eludir las comprobaciones de autenticación o autorización mediante la introducción de condiciones que siempre evalúan como verdaderas pueden utilizar. Por ejemplo, (<code>cn=)</code> <em>o (</em><code>objectClass=</code>) se pueden utilizar como valores de entrada para campos de nombre de usuario o contraseña.</td></tr></tbody></table>

Los ataques de inyección LDAP  son `similares a SQL injection` solo tienen como objetivo el servicio de directorio LDAP en lugar de una base de datos.

Por ejemplo, supongamos que una aplicación utiliza la siguiente consulta LDAP para autenticar usuarios:

```php
(&(objectClass=user)(sAMAccountName=$username)(userPassword=$password))
```

En esta consulta, `$username` y `$password` contiene las credenciales de inicio de sesión del usuario. Un atacante podría introducir el carácter `*` en el campo `$username` o `$password` para modificar la consulta LDAP y omitir la autenticación.

Si un atacante introduce el carácter `*` en el campo `$username`, la consulta LDAP buscará cualquier cuenta de usuario con cualquier contraseña. Esto permitiría al atacante acceder a la aplicación con cualquier contraseña, como se muestra a continuación:

```php
$username = "*";
$password = "dummy";
(&(objectClass=user)(sAMAccountName=$username)(userPassword=$password))
```

De manera alternativa, si un atacante inyecta el carácter `*` en el campo `$password`, la consulta LDAP buscaría coincidencias entre cualquier cuenta de usuario y cualquier contraseña que contenga la cadena inyectada. Esto permitiría al atacante obtener acceso a la aplicación con cualquier nombre de usuario, como se muestra a continuación:

```php
$username = "dummy";
$password = "*";
(&(objectClass=user)(sAMAccountName=$username)(userPassword=$password))
```

Los ataques de inyección LDAP pueden provocar consecuencias severas, como por ejemplo `acceso no autorizado a información confidencial con privilegios elevados`, e incluso ataques de `control total` sobre la aplicación o servidor afectado de malware. Estos ataques también pueden afectar considerablemente la integridad y la disponibilidad de los datos, ya que los atacantes pueden hacerlo alterar o eliminar datos dentro del servicio de directorio, lo que provoca interrupciones en las aplicaciones y los servicios que dependen de esos datos.&#x20;

Para mitigar los riesgos asociados con los ataques de inyección LDAP, es fundamental validar exhaustivamente y desinfectar los inputs de usuario de incorporarlo a las consultas LDAP. Este proceso debe implicar eliminar caracteres especiales específicos de LDAP y \*para emplear consultas parametrizadas, garantizar que la entrada del usuario sea tratada únicamente como código de datos ejecutable y sin código de sesión.

***

## <mark style="color:purple;">Enumeración</mark>

Enumerar el objetivo nos ayuda a comprender los servicios y los puertos expuestos. Un escaneo de servicios con `nmap` es un tipo de técnica de análisis de red que se utiliza para identificar y analizar los servicios que se ejecutan en un sistema o red de destino. Al sondear los puertos abiertos y evaluar las respuestas, nmap puede deducir qué servicios están activos y sus respectivas versiones. El análisis proporciona información valiosa sobre la infraestructura de red del objetivo y las posibles vulnerabilidades y superficies de ataque.

```shell-session
afsh4ck@kali$ nmap -p- -sC -sV --open --min-rate=1000 10.129.204.229

Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-23 14:43 SAST
Nmap scan report for 10.129.204.229
Host is up (0.18s latency).
Not shown: 65533 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT    STATE SERVICE VERSION
80/tcp  open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: Login
389/tcp open  ldap    OpenLDAP 2.2.X - 2.3.X

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 149.73 seconds

```

Nmap detecta un servidor `http` que se ejecuta en el puerto `80`y un servidor  `ldap`que se ejecuta en el puerto`389`

### **Inyección**

Como `OpenLDAP` se ejecuta en el servidor, es seguro asumir que la aplicación web que se ejecuta en el puerto `80`utiliza LDAP para la autenticación.

Intentar iniciar sesión con un carácter comodín (`*`) en los campos de nombre de usuario y contraseña otorga acceso al sistema, de manera efectiva eludiendo cualquier medida de autenticación que se haya implementado. Esto es un importante problema de seguridad, ya que permite que cualquier persona con conocimiento de la vulnerabilidad acceda a un sistema de acceso no autorizado y a datos potencialmente confidenciales.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.205.18
```

> Después de bypassear el login, ¿qué es el sitio web "Powered by"?

### Escaneo de puertos

```bash
sudo nmap -v -sV -T5 10.129.205.18     

PORT    STATE SERVICE VERSION
80/tcp  open  http    Apache httpd 2.4.41 ((Ubuntu))
389/tcp open  ldap    OpenLDAP 2.2.X - 2.3.X
```

Encontramos abierto el puerto 389 LDAP.

### Acceso web

Al acceder nos encontramos un panel de login:

<figure><img src="/files/nmN1dgfnTjZJBZoHuMQz" alt=""><figcaption></figcaption></figure>

### Bypass de login

Vamos a poner `*` en el campo de usuario y contraseña y consegui9mos acceder evadiendo la autenticación:

<figure><img src="/files/IMhTcyTicsw89kOISv2W" alt=""><figcaption></figcaption></figure>

Observamos que tenemos el tipo de librería que usa:: `Powered by w3.css`
