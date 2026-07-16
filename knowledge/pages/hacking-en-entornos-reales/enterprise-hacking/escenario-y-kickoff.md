
# Escenario y KickOff

Nuestro cliente, Inlanefreight, ha contratado a nuestra empresa, Acme Security, Ltd., para realizar una prueba de penetración externa completa para evaluar la seguridad de su perímetro. El cliente nos ha solicitado que identifiquemos el mayor número posible de vulnerabilidades; por lo tanto, no se requieren pruebas evasivas. Quieren comprobar qué tipo de acceso puede lograr un usuario anónimo en Internet. Según las Reglas de Compromiso (RdC), si logramos vulnerar la DMZ y acceder a la red interna, nos piden que veamos hasta dónde podemos llegar con ese acceso, incluyendo la vulneración del dominio de Active Directory. El cliente no ha proporcionado credenciales de usuario de aplicaciones web, VPN ni Active Directory. Los siguientes rangos de dominios y redes están dentro del alcance de las pruebas:

| **Pruebas externas**                            | **Pruebas internas**                              |
| ----------------------------------------------- | ------------------------------------------------- |
| `10.129.xx.xx` (host de destino "externo")      | 172.16.8.0/23                                     |
| `*.inlanefreight.local` (todos los subdominios) | 172.16.9.0/23                                     |
|                                                 | INLANEFREIGHT.LOCAL (dominio de Active Directory) |

El cliente ha proporcionado el dominio principal y las redes internas, pero no ha especificado los subdominios exactos dentro de este ámbito ni los hosts activos que encontraremos en la red. Quieren que realicemos un descubrimiento para ver qué tipo de visibilidad puede obtener un atacante contra su red externa (y la interna, si logramos establecernos).

Se permiten técnicas de prueba automatizadas, como la enumeración y el análisis de vulnerabilidades, pero debemos actuar con cuidado para no causar interrupciones del servicio. Los siguientes aspectos quedan fuera del alcance de esta evaluación:

* Phishing/Ingeniería social contra cualquier empleado o cliente de Inlanefreight
* Ataques físicos contra las instalaciones de Inlanefreight
* Acciones destructivas o pruebas de denegación de servicio (DoS)
* Modificaciones al entorno sin el consentimiento por escrito del personal de TI autorizado de Inlanefreight

***

## <mark style="color:purple;">Inicio del proyecto</mark>

En este punto, contamos con un `Scope of Work (SoW)` firmado por la gerencia de nuestra empresa y un miembro autorizado del departamento de TI de Inlanefreight. Este documento detalla los detalles de las pruebas, nuestra metodología, el cronograma, las reuniones y los entregables acordados. El cliente también firmó un documento separado de `Rules of Engagement (RoE)`, comúnmente conocido como `Autorización para el Pentesting`.&#x20;

Es fundamental tener este documento a mano antes de comenzar las pruebas y detalla el alcance de todos los tipos de evaluación (URL, direcciones IP individuales, rangos de red CIDR y credenciales, si corresponde). Este documento también incluye al personal clave de la empresa de pentesting y de Inlanefreight (un mínimo de dos contactos de cada parte, incluyendo su número de teléfono y dirección de correo electrónico). El documento también detalla detalles como la fecha de inicio y finalización de las pruebas, y el período de prueba permitido.

Nos han dado una semana para realizar pruebas y dos días adicionales para redactar el borrador del informe (en el que trabajaremos sobre la marcha). El cliente nos ha autorizado a realizar pruebas 24/7, pero nos ha pedido que realicemos análisis de vulnerabilidades exhaustivos fuera del horario laboral habitual (después de las 18:00, hora de Londres). Hemos revisado todos los documentos necesarios y contamos con las firmas requeridas de ambas partes. El alcance está completo, por lo que estamos listos para empezar desde el punto de vista administrativo.

***

## <mark style="color:purple;">Inicio del pentesting</mark>

Es lunes a primera hora de la mañana y estamos listos para empezar las pruebas. Nuestra máquina virtual de pruebas está configurada y lista para funcionar, y hemos configurado una estructura básica de toma de notas y directorios para tomar notas con nuestra herramienta favorita. Mientras se ejecutan nuestros análisis de descubrimiento iniciales, como siempre, completaremos la plantilla de informe tanto como sea posible. Esto es un pequeño avance que podemos lograr mientras esperamos a que finalicen los análisis para optimizar el tiempo disponible para el pentesting. Hemos redactado el siguiente correo electrónico para anunciar el inicio de las pruebas y hemos enviado una copia a todo el personal necesario.

![texto](https://academy.hackthebox.com/storage/modules/163/start_testing.png)

Hacemos clic en enviar en el correo electrónico y damos inicio a nuestra recopilación de información externa.
