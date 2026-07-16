
# Cómo redactar un hallazgo

La sección `Findings o Hallazgos` de nuestro informe es la esencia. Aquí es donde mostramos lo que encontramos, cómo lo explotamos y ofrecemos al cliente orientación sobre cómo solucionar los problemas. Cuanto más detallado sea cada hallazgo, mejor. Esto ayudará a los equipos técnicos a reproducir el hallazgo por sí mismos y luego podrán comprobar que su solución funcionó. Ser detallado en esta sección también ayudará a quien esté a cargo de la evaluación posterior a la remediación si el cliente contrata a su empresa para realizarla. Si bien solemos tener hallazgos de inventario en algún tipo de base de datos, es esencial ajustarlos para que se ajusten al entorno de nuestro cliente y asegurarnos de que no estemos tergiversando nada.

***

## <mark style="color:purple;">Desglose de un hallazgo</mark>

Cada hallazgo debe incluir el mismo tipo de información general, que debe adaptarse a las circunstancias específicas de su cliente. Si un hallazgo se redacta para adaptarse a varios escenarios o protocolos diferentes, la versión final debe ajustarse para que solo haga referencia a las circunstancias particulares identificadas.  "`Credenciales predeterminadas`" podrían tener diferentes significados en cuanto al riesgo si afectan a una impresora DeskJet, al sistema de climatización del edificio o a otra aplicación web de alto impacto. Como mínimo, se debe incluir la siguiente información para cada hallazgo:

* Descripción del hallazgo y a qué plataforma(s) afecta la vulnerabilidad
* Impacto si el hallazgo queda sin resolver
* Sistemas, redes, entornos o aplicaciones afectados
* Recomendación sobre cómo abordar el problema
* Enlaces de referencia con información adicional sobre el hallazgo y su resolución.
* Pasos para reproducir el problema y la evidencia que recopiló

Algunos campos adicionales y opcionales incluyen:

```
- CVE
- IDs de OWASP y MITRE
- Puntuación CVSS o similar
- Facilidad de explotación y probabilidad de ataque
- Cualquier otra información que pueda ayudar a conocer y mitigar el ataque
```

***

## <mark style="color:purple;">Demostrando los pasos para reproducirlos adecuadamente</mark>

Como se mencionó en la sección anterior sobre el Resumen Ejecutivo, es importante recordar que, aunque su persona de contacto tenga conocimientos técnicos, si no tiene experiencia específica en pruebas de penetración, es muy probable que no tenga ni idea de lo que está viendo. Es posible que ni siquiera haya oído hablar de la herramienta que utilizó para explotar la vulnerabilidad, y mucho menos comprenda la importancia del texto que genera al ejecutar el comando. Por ello, es fundamental evitar dar por sentado que las personas saben cómo realizar un pentesting. Si no lo hace correctamente, la eficacia de su entrega se verá afectada, pero esta vez ante su público técnico. Algunos conceptos a considerar:

* Divide cada paso en su propia imagen o figura. Si realizas varios pasos en la misma imagen, un lector que no esté familiarizado con las herramientas utilizadas podría no comprender lo que está sucediendo, y mucho menos tener idea de cómo reproducirlo.
* Si se requiere configuración (p. ej., módulos de Metasploit), capture la configuración completa para que el lector pueda ver cómo debería verse la configuración del exploit antes de ejecutarlo. Cree una segunda figura que muestre lo que sucede al ejecutar el exploit.
* Escribe una narrativa entre las figuras que describa lo que sucede y lo que piensas en este momento de la evaluación. No intentes explicar lo que sucede en la figura con el pie de foto ni tener varias figuras consecutivas.
* Después de realizar su demostración usando su kit de herramientas preferido, ofrezca herramientas alternativas que puedan usarse para validar el hallazgo si existen (solo mencione la herramienta y proporcione un enlace de referencia, no realice la explotación dos veces con más de una herramienta).

Tu objetivo principal debe ser presentar la evidencia de forma comprensible y práctica para el cliente. Piensa en cómo usará la información que presentas. Si muestras una vulnerabilidad en una aplicación web, una captura de pantalla de Burp no es la mejor manera de presentarla si estás creando tus propias solicitudes web. El cliente probablemente querrá copiar y pegar la carga útil de tus pruebas para recrearla, y no podrá hacerlo si solo es una captura de pantalla.

Otro aspecto crucial a considerar es si sus pruebas son completamente defendibles. Por ejemplo, si intenta demostrar que la información se transmite en texto claro debido al uso de autenticación básica en una aplicación web, no basta con capturar la ventana emergente del mensaje de inicio de sesión. Esto demuestra que la autenticación básica está activa, pero no ofrece ninguna prueba de que la información se transmita sin cifrar. En este caso, mostrar el mensaje de inicio de sesión con credenciales falsas introducidas y las credenciales en texto claro en una captura de paquetes de Wireshark de la solicitud de autenticación legible por humanos no deja lugar a debate.&#x20;

De igual manera, si intenta demostrar la presencia de una vulnerabilidad en una aplicación web específica o en algún otro elemento con una interfaz gráfica de usuario (como RDP), es importante capturar la URL en la barra de direcciones o la salida de un comando `ifconfig`\`o `ipconfig` para demostrar que está en el host del cliente y no en una imagen aleatoria descargada de Google. Además, si captura la pantalla de su navegador, desactive la barra de marcadores y desactive cualquier extensión de navegador no profesional o dedique un navegador web específico a sus pruebas.

### Ejemplo

A continuación, se muestra un ejemplo de cómo podríamos mostrar los pasos para capturar un hash con la herramienta Responder y descifrarlo sin conexión con Hashcat. Si bien no es absolutamente necesario, puede ser útil enumerar herramientas alternativas, como hicimos con este hallazgo. El cliente podría trabajar desde una máquina Windows y encontrar un script o ejecutable de PowerShell más intuitivo, o quizás esté más familiarizado con otro conjunto de herramientas. Tenga en cuenta que también ocultamos el hash y las contraseñas en texto plano, ya que este informe podría compartirse con diferentes usuarios, por lo que es recomendable ocultar las credenciales siempre que sea posible.

<figure><img src="/files/7yWHa9wHCwPvyn0ZqhIU" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Recomendaciones de remediación efectivas</mark>

#### **Ejemplo 1**

* `Malo` : Reconfigure los ajustes de registro para protegerse contra X.
* `Buena` : Para corregir completamente este hallazgo, se deben actualizar las siguientes secciones del registro con los valores especificados. Tenga en cuenta que los cambios en componentes críticos, como el registro, deben abordarse con precaución y probarse en un grupo pequeño antes de realizar cambios a gran escala.
  * `[enumere la ruta completa a las secciones del registro afectadas]`
    * Cambiar el valor X al valor Y

#### **Razón fundamental**

Aunque el ejemplo "malo" es al menos algo útil, es bastante perezoso y estás desperdiciando una oportunidad de aprendizaje. Una vez más, el lector de este informe podría no tener la misma experiencia en Windows que tú, y darle una recomendación que le requerirá horas de trabajo para que la descubra solo lo frustrará. Investiga y sé lo más específico posible. Hacerlo tiene las siguientes ventajas:

* De esta manera, aprenderás más y te sentirás mucho más cómodo respondiendo preguntas durante la revisión del informe. Esto reforzará la confianza del cliente en usted y será un conocimiento que podrá aprovechar en futuras evaluaciones y para ayudar a mejorar su equipo.
* El cliente agradecerá que investigues por él y le describas específicamente lo que debe hacerse para que sea lo más eficiente posible. Esto aumentará la probabilidad de que te solicite evaluaciones futuras y te recomiende a ti y a tu equipo a sus amigos.

También vale la pena destacar que el ejemplo "bueno" incluye una advertencia: cambiar algo tan importante como el registro conlleva sus propios riesgos y debe realizarse con precaución. Esto le indica al cliente que usted vela por sus intereses y que realmente desea que tenga éxito. Para bien o para mal, habrá clientes que harán lo que usted les diga sin pensarlo dos veces y no dudarán en exigirle responsabilidades si al hacerlo se rompe algo.

#### **Ejemplo 2**

* `Malo` : Implementar `[alguna herramienta comercial que cuesta una fortuna]` para abordar este hallazgo.
* `Bueno` : Existen diferentes enfoques para abordar este hallazgo. \[`Nombre del proveedor de software afectado]` ha publicado una solución provisional. Para mayor brevedad, se incluye un enlace a la guía en los enlaces de referencia a continuación. Como alternativa, existen herramientas comerciales que permiten desactivar por completo la funcionalidad vulnerable del software afectado, pero estas herramientas pueden resultar prohibitivas.

#### **Razón fundamental**

El ejemplo "malo" no le permite al cliente solucionar este problema sin gastar mucho dinero que quizás no tenga. Si bien la herramienta comercial puede ser la solución más sencilla, muchos clientes no tienen el presupuesto para hacerlo y necesitan una solución alternativa. Esta solución alternativa puede ser un parche o extremadamente engorrosa, o ambas cosas, pero al menos le dará al cliente algo de tiempo hasta que el proveedor publique una solución oficial.

***

## <mark style="color:purple;">Selección de referencias de calidad</mark>

Cada hallazgo debe incluir una o más referencias externas para obtener más información sobre una vulnerabilidad o configuración incorrecta en particular. Algunos criterios que aumentan la utilidad de una referencia son:

* Una fuente independiente del proveedor es útil. Obviamente, si encuentra una vulnerabilidad de ASA, un enlace de referencia de Cisco tiene sentido, pero no recurriría a ellos para que describan nada ajeno a las redes. Si cita un artículo escrito por un proveedor de productos, es probable que el artículo se centre en explicar al lector cómo su producto puede ayudar cuando lo único que el lector quiere es saber cómo solucionarlo por sí mismo.

Es preferible una explicación detallada del hallazgo y las soluciones alternativas o mitigaciones recomendadas. No elijas artículos de pago ni nada que te permita obtener solo una parte de lo que necesitas sin pagar.

* Usa artículos que vayan al grano. Este no es un sitio web de recetas, y a nadie le importa la frecuencia con la que tu abuela hacía esas galletas. Tenemos problemas que resolver, y obligar a alguien a revisar todo el documento NIST 800-53 o una RFC es más molesto que útil.
* Elija fuentes que tengan sitios web limpios y que no le hagan sentir como si un montón de mineros de criptomonedas estuvieran ejecutándose en segundo plano o que aparecieran anuncios en todas partes.
* Si es posible, escriba sobre su propia información y publique en su blog. La investigación le ayudará a explicar el impacto del hallazgo a sus clientes, y aunque la comunidad de seguridad informática es muy útil, es preferible no dirigir a sus clientes al sitio web de la competencia.

***

## <mark style="color:purple;">Ejemplos de hallazgos</mark>

A continuación, se presentan algunos ejemplos de hallazgos. Los dos primeros son ejemplos de problemas que pueden descubrirse durante una prueba de penetración interna. Como puede ver, cada hallazgo incluye todos los elementos clave: una descripción detallada de lo que sucede, el impacto en el entorno si no se corrige, los hosts afectados por el problema (o todo el dominio), consejos de remediación genéricos que no recomiendan herramientas de proveedores específicos y ofrecen varias opciones de remediación. Finalmente, los enlaces de referencia provienen de fuentes reconocidas y de buena reputación que probablemente no se eliminarán pronto, como podría ocurrir con un blog personal.

Una nota sobre el formato: Este podría ser un tema muy controvertido. Los hallazgos de ejemplo se presentan en formato de tabla, pero si alguna vez ha trabajado en Word o ha intentado automatizar la generación de informes, sabe que las tablas pueden ser un verdadero problema. Por esta razón, algunos optan por separar las secciones de sus hallazgos con diferentes niveles de encabezado. Cualquiera de estos enfoques es aceptable, ya que lo importante es que el mensaje llegue al lector y que sea fácil distinguir las señales visuales de cuándo termina un hallazgo y comienza otro; la legibilidad es fundamental. Si logra esto, podrá ajustar los colores, el diseño, el orden e incluso los nombres de las secciones.

#### **Autenticación Kerberos débil (“Kerberoasting”)**

<figure><img src="/files/Q28lXzr24WHTv6fgojha" alt=""><figcaption></figcaption></figure>

#### **Credenciales débiles/predeterminadas del administrador de Tomcat**

<figure><img src="/files/Lxy2zbcHHlh1FXYyaHE1" alt=""><figcaption></figcaption></figure>

#### **Hallazgo mal redactado**

A continuación se muestra un ejemplo de un hallazgo mal redactado que presenta varios problemas:

* El formato es descuidado con el enlace CWE
* No se completa ninguna puntuación CVSS (no es obligatorio, pero si su plantilla de informe la utiliza, debe completarla)
* La descripción no explica claramente el problema o la causa raíz
* El impacto en la seguridad es vago y genérico
* La sección de Remediation no es clara ni procesable

Si leo este informe, veo que este hallazgo es grave (porque está en rojo), pero ¿por qué me importa? ¿Qué puedo hacer al respecto? Cada hallazgo debe detallar el problema y educar al lector sobre él (es muy probable que nunca haya oído hablar de Kerberoasting ni de ningún otro ataque). Explique claramente el riesgo de seguridad y `porqué` debe remediarse, incluyendo recomendaciones prácticas.

<figure><img src="/files/7OCQN1gUZdzHRp5YWtsp" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Hacia delante</mark>

Ahora que hemos cubierto cómo mantenerse organizado durante una prueba de penetración, los tipos de informes, los componentes estándar de un informe y cómo redactar un hallazgo, tengo algunos consejos y trucos de informes para compartir contigo a partir de mi experiencia en el campo.
