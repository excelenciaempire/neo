
# osTicket

[osTicket](https://osticket.com/) es un sistema de tickets de soporte de código abierto. Se puede comparar con sistemas como Jira, OTRS, Request Tracker y Spiceworks. osTicket puede integrar consultas de usuarios por correo electrónico, teléfono y formularios web en una interfaz web. osTicket está escrito en PHP y utiliza un backend MySQL. Se puede instalar en Windows o Linux. Aunque no hay una cantidad considerable de información de mercado disponible sobre osTicket, una rápida búsqueda en Google `Helpdesk software - powered by osTicket` arroja unos 44.000 resultados, muchos de los cuales parecen ser empresas, sistemas escolares, universidades, gobiernos locales, etc., que utilizan la aplicación. osTicket incluso se mostró brevemente en el programa [Mr. Robot](https://forum.osticket.com/d/86225-osticket-on-usas-mr-robot-s01e08) .

Además de aprender a enumerar y atacar osTicket, el propósito de esta sección también es presentarle el mundo de los sistemas de tickets de soporte y por qué no deben pasarse por alto durante nuestras evaluaciones.

***

## <mark style="color:purple;">Footprinting / Discovery /Enumeración</mark>

Al mirar nuevamente nuestro escaneo EyeWitness anterior, notamos una captura de pantalla de una instancia de osTicket que también muestra que se configuró una cookie llamada `OSTSESSID` al visitar la página.

![imagen](https://academy.hackthebox.com/storage/modules/113/osticket_eyewitness.png)

Además, la mayoría de las instalaciones de osTicket mostrarán el logotipo de osTicket con la frase `powered by` delante en el pie de página de la página. El pie de página también puede contener las palabras `Support Ticket System`.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/osticket_main.png" alt=""><figcaption></figcaption></figure>

Un escaneo de Nmap sólo mostrará información sobre el servidor web, como Apache o IIS, y no nos ayudará a rastrear la aplicación.

`osTicket` es una aplicación web que recibe un alto nivel de mantenimiento y servicio. Si analizamos los [CVE](https://www.cvedetails.com/vendor/2292/Osticket.html) encontrados a lo largo de las décadas, no encontraremos muchas vulnerabilidades y exploits que osTicket podría tener. Este es un excelente ejemplo para demostrar lo importante que es comprender cómo funciona una aplicación web. Incluso si la aplicación no es vulnerable, aún puede usarse para nuestros fines. Aquí podemos desglosar las funciones principales en las capas:

| `1. Entrada del usuario` | `2. Procesamiento` | `3. Solución` |
| ------------------------ | ------------------ | ------------- |

#### **Entrada del usuario**

La función principal de osTicket es informar a los empleados de la empresa sobre un problema para que se pueda resolver con el servicio u otros componentes. Una ventaja importante que tenemos aquí es que la aplicación es de código abierto. Por lo tanto, tenemos muchos tutoriales y ejemplos disponibles para examinar más de cerca la aplicación. Por ejemplo, en la [documentación](https://docs.osticket.com/en/latest/Getting%20Started/Post-Installation.html) de osTicket , podemos ver que solo el personal y los usuarios con privilegios de administrador pueden acceder al panel de administración. Por lo tanto, si nuestra empresa objetivo utiliza esta aplicación o una similar, podemos causar un problema y "hacernos los tontos" y contactar con el personal de la empresa. La "falta de" conocimiento simulada sobre los servicios ofrecidos por la empresa en combinación con un problema técnico es un enfoque de ingeniería social muy extendido para obtener más información de la empresa.

#### **Procesamiento**

Como personal o administradores, intentan reproducir errores significativos para encontrar el núcleo del problema. El procesamiento finalmente se realiza internamente en un entorno aislado que tendrá configuraciones muy similares a los sistemas en producción. Supongamos que el personal y los administradores sospechan que hay un error interno que puede estar afectando al negocio. En ese caso, analizarán más en detalle para descubrir posibles errores de código y abordar problemas más importantes.

#### **Solución**

Dependiendo de la profundidad del problema, es muy probable que otros miembros del personal de los departamentos técnicos estén involucrados en la correspondencia por correo electrónico. Esto nos proporcionará nuevas direcciones de correo electrónico para usar en el panel de administración de osTicket (en el peor de los casos) y posibles nombres de usuario con los que podemos realizar OSINT o intentar aplicar a otros servicios de la empresa.

***

## <mark style="color:purple;">Atacando a osTicket</mark>

Una búsqueda de osTicket en exploit-db muestra varios problemas, como inclusión remota de archivos, inyección SQL, carga arbitraria de archivos, XSS, etc. La versión 1.14.1 de osTicket presenta [CVE-2020-24881](https://nvd.nist.gov/vuln/detail/CVE-2020-24881) , que era una vulnerabilidad SSRF. Si se explota, este tipo de falla puede aprovecharse para obtener acceso a recursos internos o realizar escaneo de puertos internos.

Además de las vulnerabilidades relacionadas con las aplicaciones web, los portales de soporte a veces se pueden utilizar para obtener una dirección de correo electrónico para un dominio de la empresa, que se puede utilizar para registrarse en otras aplicaciones expuestas que requieren el envío de una verificación por correo electrónico. Como se mencionó anteriormente en el módulo, esto se ilustra en la caja de lanzamiento semanal de HTB [con](https://0xdf.gitlab.io/2021/05/22/htb-delivery.html) un tutorial en video [aquí](https://www.youtube.com/watch?v=gbs43E71mFM) .

Veamos un ejemplo rápido, que está relacionado con esta [excelente publicación de blog](https://medium.com/intigriti/how-i-hacked-hundreds-of-companies-through-their-helpdesk-b7680ddc2d4c) que [@ippsec](https://twitter.com/ippsec) también mencionó que fue una inspiración para su máquina Delivery, que recomiendo revisar después de leer esta sección.

Supongamos que encontramos un servicio expuesto, como el servidor Slack de una empresa o GitLab, que requiere una dirección de correo electrónico válida de la empresa para unirse. Muchas empresas tienen un correo electrónico de soporte como `support@inlanefreight.local`, y los correos electrónicos enviados a este están disponibles en portales de soporte en línea que pueden ir desde Zendesk hasta una herramienta personalizada interna. Además, un portal de soporte puede asignar una dirección de correo electrónico interna temporal a un nuevo ticket para que los usuarios puedan verificar rápidamente su estado.

Si encontramos un portal de atención al cliente durante nuestra evaluación y podemos enviar un nuevo ticket, es posible que podamos obtener una dirección de correo electrónico válida de la empresa.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/new_ticket.png" alt=""><figcaption></figcaption></figure>

Esta es una versión modificada de osTicket a modo de ejemplo, pero podemos ver que se proporcionó una dirección de correo electrónico.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/ticket_email.png" alt=""><figcaption></figcaption></figure>

Ahora, si iniciamos sesión, podemos ver información sobre el ticket y las formas de publicar una respuesta. Si la empresa configuró su software de soporte técnico para correlacionar los números de ticket con los correos electrónicos, entonces cualquier correo electrónico enviado al correo electrónico que recibimos al registrarnos, `940288@inlanefreight.local`, se mostraría aquí. Con esta configuración, si podemos encontrar un portal externo como una Wiki, un servicio de chat (Slack, Mattermost, Rocket.chat) o un repositorio Git como GitLab o Bitbucket, es posible que podamos usar este correo electrónico para registrar una cuenta y el portal de soporte técnico para recibir un correo electrónico de confirmación de registro.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/ost_tickets.png" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">osTicket - Exposición de datos sensibles</mark>

Supongamos que estamos realizando una prueba de penetración externa. Durante la fase de OSINT y recopilación de información, descubrimos varias credenciales de usuario utilizando la herramienta [Dehashed](http://dehashed.com/) (para nuestros fines, los datos de muestra que aparecen a continuación son ficticios).

```shell-session
afsh4ck@kali$ sudo python3 dehashed.py -q inlanefreight.local -p

id : 5996447501
email : julie.clayton@inlanefreight.local
username : jclayton
password : JulieC8765!
hashed_password : 
name : Julie Clayton
vin : 
address : 
phone : 
database_name : ModBSolutions


id : 7344467234
email : kevin@inlanefreight.local
username : kgrimes
password : Fish1ng_s3ason!
hashed_password : 
name : Kevin Grimes
vin : 
address : 
phone : 
database_name : MyFitnessPal

<SNIP>
```

Este volcado muestra contraseñas en texto simple para dos usuarios diferentes: `jclayton` y `kgrimes`. En este punto, también hemos realizado una enumeración de subdominios y encontramos varios interesantes.

```shell-session
afsh4ck@kali$ cat ilfreight_subdomains

vpn.inlanefreight.local
support.inlanefreight.local
ns1.inlanefreight.local
mail.inlanefreight.local
apps.inlanefreight.local
ftp.inlanefreight.local
dev.inlanefreight.local
ir.inlanefreight.local
auth.inlanefreight.local
careers.inlanefreight.local
portal-stage.inlanefreight.local
dns1.inlanefreight.local
dns2.inlanefreight.local
meet.inlanefreight.local
portal-test.inlanefreight.local
home.inlanefreight.local
legacy.inlanefreight.local
```

Exploramos cada subdominio y encontramos que muchos están inactivos, pero el `support.inlanefreight.local` y `vpn.inlanefreight.local` están activos y son muy prometedores. `Support.inlanefreight.local` está alojando una instancia de osTicket, y `vpn.inlanefreight.local` es un portal web Barracuda SSL VPN que no parece estar usando autenticación multifactor.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/osticket_admin.png" alt=""><figcaption></figcaption></figure>

Probamos las credenciales para `jclayton`. No hubo suerte. Luego probamos las credenciales para `kgrimes` y no tuvimos éxito, pero notamos que la página de inicio de sesión también acepta una dirección de correo electrónico. ¡Intentamos con `kevin@inlanefreight.local` y conseguimos iniciar sesión correctamente!

<figure><img src="https://academy.hackthebox.com/storage/modules/113/osticket_kevin.png" alt=""><figcaption></figcaption></figure>

El usuario `kevin` parece ser un agente de soporte, pero no tiene ningún ticket abierto. ¿Quizás ya no esté activo? En una empresa con mucho trabajo, esperaríamos ver algunos tickets abiertos. Investigando un poco, encontramos un ticket cerrado, una conversación entre un empleado remoto y el agente de soporte.

<figure><img src="https://academy.hackthebox.com/storage/modules/113/osticket_ticket.png" alt=""><figcaption></figcaption></figure>

El empleado afirma que se le bloqueó el acceso a su cuenta VPN y le pide al agente que la restablezca. Luego, el agente le dice al usuario que la contraseña se restableció a la contraseña estándar para nuevos miembros. El usuario no tiene esta contraseña y le pide al agente que lo llame para que se la proporcione (¡una sólida conciencia de seguridad!). Luego, el agente comete un error y envía la contraseña al usuario directamente a través del portal. Desde aquí, podríamos probar esta contraseña en el portal VPN expuesto, ya que es posible que el usuario no la haya cambiado.

Además, el agente de soporte indica que esta es la contraseña estándar que se les da a los nuevos usuarios y establece la contraseña del usuario con este valor. Hemos estado en muchas organizaciones donde el servicio de asistencia técnica utiliza una contraseña estándar para los nuevos usuarios y los restablecimientos de contraseñas. A menudo, la política de contraseñas del dominio es laxa y no obliga al usuario a cambiarla en el siguiente inicio de sesión. Si este es el caso, puede funcionar para otros usuarios. Aunque está fuera del alcance de este módulo, en este escenario, valdría la pena utilizar herramientas como [linkedin2username](https://github.com/initstring/linkedin2username) para crear una lista de usuarios de los empleados de la empresa e intentar un ataque de rociado de contraseñas contra el punto final de la VPN con esta contraseña estándar.

Muchas aplicaciones como osTicket también contienen una libreta de direcciones. También valdría la pena exportar todos los correos electrónicos y nombres de usuario de la libreta de direcciones como parte de nuestra enumeración, ya que también podrían resultar útiles en un ataque como el de robo de contraseñas.

***

## <mark style="color:purple;">Reflexiones finales</mark>

Aunque en esta sección se muestran algunos escenarios ficticios, se basan en situaciones que probablemente veremos en el mundo real. Cuando nos topamos con portales de soporte (especialmente externos), deberíamos probar la funcionalidad y ver si podemos hacer cosas como crear un ticket y que nos asignen una dirección de correo electrónico legítima de la empresa. Desde allí, es posible que podamos usar la dirección de correo electrónico para iniciar sesión en otros servicios de la empresa y obtener acceso a datos confidenciales.

En esta sección también se muestran los peligros de la reutilización de contraseñas y los tipos de datos que es muy probable que encontremos si logramos acceder a la cola de tickets de soporte de un agente de soporte técnico. Las organizaciones pueden evitar este tipo de fuga de información siguiendo unos pasos relativamente sencillos:

* Limitar qué aplicaciones están expuestas externamente
* Imponer la autenticación multifactor en todos los portales externos
* Proporcionar capacitación sobre concientización sobre seguridad a todos los empleados y recomendarles que no utilicen sus correos electrónicos corporativos para registrarse en servicios de terceros.
* Aplicar una política de contraseñas segura en Active Directory y en todas las aplicaciones, que no permita palabras comunes como variaciones de `welcome`, y `password`, el nombre de la empresa, y estaciones y meses.
* Requerir que un usuario cambie su contraseña después de su inicio de sesión inicial y hacer caducar periódicamente las contraseñas del usuario

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.23.62 (ACADEMY-ATCKAPPS-APP04) 

vHosts necesarios:
support.inlanefreight.local
```

> Encuentra el camino hacia la instancia de osTicket y envía la contraseña enviada desde el agente de atención al cliente Charles Smithson.

Añadimos la IP y el subdominio a /etc/hosts.

### Escaneo de puertos

```bash
sudo nmap -v -sV -T5 10.129.23.62

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
8081/tcp open  http    nginx
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Accedemos por el puerto 80 y nos encontramos la instancia de OS Ticket:

<figure><img src="/files/XjkaB85N3VstdD1EnmD9" alt=""><figcaption></figcaption></figure>

Recordamos que el objetivo es Charles Smithson, por lo que vamos a probar con su nombre y posible email, ya que es un agente de soporte:

<figure><img src="/files/9i4Ng7bEqG3fbqNnrFFt" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/l2W3fcyOclz2Q070VM4e" alt=""><figcaption></figcaption></figure>

Se crea el ticket y usamos los datos para ver el ticket que hemos creado:

<figure><img src="/files/Yn96vHIdUf4e5zTwSamJ" alt=""><figcaption></figcaption></figure>

### Explotación

También tenemos datos de credenciales del pentesting anterior a esta máquina que podríamos utilizar:

```shell-session
afsh4ck@kali$ sudo python3 dehashed.py -q inlanefreight.local -p

id : 5996447501
email : julie.clayton@inlanefreight.local
username : jclayton
password : JulieC8765!
hashed_password : 
name : Julie Clayton
vin : 
address : 
phone : 
database_name : ModBSolutions


id : 7344467234
email : kevin@inlanefreight.local
username : kgrimes
password : Fish1ng_s3ason!
hashed_password : 
name : Kevin Grimes
vin : 
address : 
phone : 
database_name : MyFitnessPal

<SNIP>
```

Para ello en la pantalla de login como agente probamos a entrar como el usuario kevin:

<figure><img src="/files/CzI8NSTOPiZ9sQNJp0rn" alt=""><figcaption></figcaption></figure>

En los tickets cerrados encontramos uno interesante:

<figure><img src="/files/jWKFkVYJ6kmbm1lbuArR" alt=""><figcaption></figcaption></figure>

Echándole un ojo al ticket encontramos las credenciales para el usuario Charles Smithson:

<figure><img src="/files/DGkgPR24bRVGWdEn5nNk" alt=""><figcaption></figcaption></figure>
