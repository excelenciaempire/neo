
# Tipos de informes

La estructura de nuestro informe variará ligeramente según la evaluación que se nos asigne. En este módulo, nos centraremos principalmente en un informe de prueba de penetración interna en el que el evaluador logró comprometer un dominio de Active Directory (AD) durante una prueba de penetración interna. El informe con el que trabajaremos mostrará los elementos típicos de un informe de prueba de penetración interna. Analizaremos aspectos de otros informes (como los apéndices adicionales que pueden incluirse en un informe de prueba de penetración externa).&#x20;

No es raro ver un informe de prueba de penetración externa que resultó en un compromiso interno con una cadena de ataque y otros elementos que abordaremos. La principal diferencia en nuestro laboratorio es que no incluiremos datos OSINT ni información pública disponible, como direcciones de correo electrónico, subdominios, credenciales en volcados de infracciones, datos de registro/propiedad de dominios, etc., porque no estamos probando con una empresa real con presencia en internet. Si bien existen algunos actores veteranos con gran trayectoria, como Have I Been Pwned, Shodan e Intelx, las herramientas OSINT suelen ser muy flexibles, por lo que, para cuando leas este artículo, es posible que la mejor herramienta o recurso para recopilar esa información haya cambiado. En su lugar, enumeramos algunos tipos de información comunes para facilitar una prueba de penetración y dejamos que el lector pruebe y descubra qué herramientas o API ofrecen los mejores resultados. Siempre es recomendable no depender de una sola herramienta; por lo tanto, ejecute varias y observe la diferencia en los datos.

* Registros públicos de propiedad de dominios y DNS
* Direcciones de correo electrónico
  * Luego, puede usarlos para verificar si alguno estuvo involucrado en una infracción o usar Google Dorks para buscarlos en sitios como Pastebin.
* Subdominios
* Proveedores externos
* Dominios similares
* Recursos de nube pública

Estos tipos de recopilación de información se tratan en otros módulos, como [Recopilación de información - Edición web](https://academy.hackthebox.com/course/preview/information-gathering---web-edition) , [OSINT: Reconocimiento corporativo](https://academy.hackthebox.com/course/preview/osint-corporate-recon) y [Huellas](https://academy.hackthebox.com/course/preview/footprinting) , y están fuera del alcance de este módulo.

***

## <mark style="color:purple;">Diferencias entre los tipos de evaluación</mark>

Antes de repasar los distintos tipos de informes disponibles y luego profundizar en los componentes de un informe de prueba de penetración, definamos algunos tipos de evaluación clave.

#### **Evaluación de vulnerabilidad**

Las evaluaciones de vulnerabilidades implican la ejecución de un análisis automatizado de un entorno para enumerar las vulnerabilidades. Estas pueden estar autenticadas o no. No se intenta explotarlas, pero a menudo validamos los resultados del análisis para que nuestro informe pueda mostrar al cliente qué resultados representan problemas reales y cuáles son falsos positivos. La validación puede consistir en realizar una comprobación adicional para confirmar que se utiliza una versión vulnerable o que existe una configuración incorrecta, pero el objetivo no es consolidarse ni moverse lateral o verticalmente. Algunos clientes incluso solicitan los resultados del análisis sin validación.

#### **Interno vs. Externo**

Un análisis externo se realiza desde la perspectiva de un usuario anónimo en internet, dirigido a los sistemas públicos de la organización. Un análisis interno se realiza desde la perspectiva de un escáner en la red interna e investiga los hosts tras el firewall. Esto puede realizarse desde la perspectiva de un usuario anónimo en la red corporativa, emulando un servidor comprometido o en cualquier otro escenario. Un cliente puede incluso solicitar un análisis interno con credenciales, lo que puede generar muchos más hallazgos del escáner, pero también resultados más precisos y menos genéricos.

#### **Contenido del informe**

Estos informes suelen centrarse en temas observables en los resultados del análisis y destacan la cantidad de vulnerabilidades y su gravedad. Estos análisis pueden generar una gran cantidad de datos, por lo que identificar patrones y relacionarlos con deficiencias de procedimiento es fundamental para evitar una sobrecarga de información.

***

## <mark style="color:purple;">Pruebas de penetración</mark>

Las pruebas de penetración van más allá de los análisis automatizados y pueden aprovechar los datos de los análisis de vulnerabilidades para guiar la explotación. Al igual que los análisis de vulnerabilidades, pueden realizarse desde una perspectiva interna o externa. Dependiendo del tipo de prueba de penetración (es decir, una prueba evasiva), es posible que no realicemos ningún tipo de análisis de vulnerabilidades.

Una prueba de penetración puede realizarse desde varias perspectivas, como "`black box`" donde solo disponemos del nombre de la empresa durante una conexión externa o de red para una interna; "`grey box`" donde solo se nos proporcionan direcciones IP/rangos de red CIDR dentro del alcance; o "`white box`" donde se nos proporcionan credenciales, código fuente, configuraciones y más. Las pruebas se pueden realizar con `zero evasion` para intentar descubrir el mayor número posible de vulnerabilidades. Desde una perspectiva `evasiva híbrida`, se prueban las defensas del cliente, comenzando con evasión y aumentando gradualmente el nivel de ruido para ver hasta qué punto los equipos de seguridad internos o las herramientas de monitorización nos detectan y bloquean.&#x20;

Normalmente, una vez detectados en este tipo de evaluación, el cliente nos solicitará que pasemos a pruebas no evasivas durante el resto de la evaluación. Este tipo de evaluación es excelente para clientes con algunas defensas implementadas, pero con una estrategia de seguridad defensiva aún no muy consolidada. Puede ayudar a identificar las deficiencias en sus defensas y determinar dónde deben concentrar sus esfuerzos para mejorar sus reglas de detección y prevención. Para clientes con mayor experiencia, este tipo de evaluación puede ser una excelente prueba de sus defensas y procedimientos internos para garantizar que todas las partes desempeñen sus funciones correctamente en caso de un ataque real.

Finalmente, es posible que se nos pida que realicemos el pentesting en modalidad `evasive testing` durante todo el proceso. En este tipo de evaluación, intentaremos pasar desapercibidos el mayor tiempo posible y analizaremos qué tipo de acceso, si lo hay, podemos obtener trabajando de forma sigilosa. Esto puede ayudar a simular un atacante más avanzado. Sin embargo, este tipo de evaluación suele estar limitado por limitaciones de tiempo que no existen para un atacante real. Un cliente también puede optar por una simulación de adversario a largo plazo, que puede durar varios meses, con poco personal de la empresa al tanto de la evaluación y poco o ningún miembro del personal del cliente conociendo el día y la hora exactos de inicio. Este tipo de evaluación es ideal para organizaciones con mayor madurez en seguridad y requiere un conjunto de habilidades ligeramente diferente al de un evaluador de penetración de redes/aplicaciones tradicional.

#### **Interno vs. Externo**

Al igual que las perspectivas de escaneo de vulnerabilidades, las pruebas de penetración externas suelen realizarse desde la perspectiva de un atacante anónimo en internet. Pueden aprovechar datos OSINT o información pública para intentar acceder a datos confidenciales a través de aplicaciones o la red interna, atacando hosts conectados a internet. Las pruebas de penetración internas pueden realizarse como un usuario anónimo en la red interna o como un usuario autenticado. Su objetivo habitual es encontrar el mayor número posible de vulnerabilidades para establecerse, realizar escaladas de privilegios horizontales y verticales, actuar lateralmente y comprometer la red interna (normalmente el entorno de Active Directory del cliente).

***

## <mark style="color:purple;">Evaluaciones interdisciplinarias</mark>

Algunas evaluaciones pueden requerir la participación de personas con habilidades diversas y complementarias. Si bien son logísticamente más complejas, tienden a ser más colaborativas entre el equipo consultor y el cliente, lo que aporta un gran valor a la evaluación y a la confianza en la relación. Algunos ejemplos de este tipo de evaluaciones incluyen:

#### **Evaluaciones de estilo Purple Team**

Como su nombre indica, se trata de un esfuerzo conjunto entre el `red team` y el `blue team`, generalmente un experto en pruebas de penetración y un responsable de respuesta a incidentes. El concepto general es que el experto en pruebas de penetración simula una amenaza determinada, y el responsable de respuesta a incidentes trabaja con el equipo azul interno para revisar sus herramientas y determinar si las alertas están configuradas correctamente o si se requieren ajustes para permitir una identificación correcta.

#### **Pruebas de penetración centradas en la nube**

Si bien se solapa considerablemente con una prueba de penetración convencional, una evaluación centrada en la nube se beneficiará del conocimiento de alguien con experiencia en arquitectura y administración de la nube. A menudo, puede ser tan simple como explicar al pentester qué se puede abusar de la información descubierta (como secretos o claves). Obviamente, al introducir infraestructuras menos convencionales, como contenedores y aplicaciones sin servidor, el enfoque para probar esos recursos requiere conocimientos muy específicos, probablemente una metodología y un conjunto de herramientas completamente diferentes. Dado que los informes de este tipo de evaluaciones son relativamente similares a los de las pruebas de penetración convencionales, se mencionan en este contexto para su conocimiento, pero los detalles técnicos sobre las pruebas de estos recursos únicos quedan fuera del alcance de este curso.

#### **Pruebas integrales de IoT**

Las plataformas IoT suelen tener tres componentes principales: red, nube y aplicación. Hay profesionales altamente especializados en cada uno de ellos que podrán proporcionar una evaluación mucho más exhaustiva en conjunto, en lugar de depender de una sola persona con conocimientos básicos en cada área. Otro componente que podría requerir pruebas es la capa de hardware, que se describe a continuación. Al igual que las pruebas en la nube, existen aspectos de estas pruebas que probablemente requieran habilidades especializadas fuera del alcance de este curso; sin embargo, el formato estándar de los informes de pruebas de penetración es adecuado para presentar este tipo de datos.

***

## <mark style="color:purple;">Pruebas de penetración de aplicaciones web</mark>

Dependiendo del alcance, este tipo de evaluación también puede considerarse interdisciplinaria. Algunas evaluaciones de aplicaciones pueden centrarse únicamente en identificar y validar las vulnerabilidades de una aplicación mediante pruebas autenticadas basadas en roles, sin interés en evaluar el servidor subyacente. Otras podrían querer probar tanto la aplicación como la infraestructura, con la intención de que el ataque inicial se produzca a través de la propia aplicación web (de nuevo, quizás desde una perspectiva autenticada o basada en roles) y luego intentar ir más allá de la aplicación para ver qué otros hosts y sistemas subyacentes pueden verse comprometidos. Este último tipo de evaluación se beneficiaría de la experiencia de alguien con desarrollo y pruebas de aplicaciones para el ataque inicial, y luego, quizás, de un pentester especializado en redes para que se mantenga al día y distribuya o escale privilegios a través de Active Directory o algún otro medio más allá de las propias aplicaciones.

***

## <mark style="color:purple;">Pruebas de penetración de hardware</mark>

Este tipo de prueba se suele realizar en dispositivos IoT, pero puede extenderse a la prueba de seguridad física de una computadora portátil enviada por el cliente, un quiosco o cajero automático in situ. Cada cliente tendrá un nivel de comodidad diferente con la profundidad de las pruebas, por lo que es fundamental establecer las reglas de actuación antes de comenzar la evaluación, especialmente cuando se trata de pruebas destructivas. Si el cliente espera que su dispositivo vuelva intacto y funcionando, probablemente no sea recomendable intentar desoldar los chips de la placa base ni realizar ataques similares.

***

## <mark style="color:purple;">Borrador del informe</mark>

Cada vez es más común que los clientes esperen dialogar e incorporar sus comentarios en un informe. Esto puede presentarse de diversas formas, ya sea para añadir comentarios sobre cómo planean abordar cada hallazgo (respuesta de la gerencia), ajustar el lenguaje potencialmente polémico o adaptar las cosas para que se ajusten mejor a sus necesidades.&#x20;

Por estas razones, es mejor planificar la entrega de un borrador del informe primero, dar tiempo al cliente para revisarlo por su cuenta y luego ofrecerle un espacio de tiempo para que pueda revisarlo con usted para hacer preguntas, obtener aclaraciones o explicar lo que desea ver. Al final, el cliente paga por el informe, y debemos asegurarnos de que sea lo más completo y valioso posible para él. Algunos no harán ningún comentario sobre el informe, mientras que otros solicitarán cambios o adiciones significativas para que se ajuste a sus necesidades, ya sea para presentarlo ante su junta directiva para obtener financiación adicional o para utilizar el informe como base para su plan de seguridad para implementar medidas de remediación y fortalecer su estrategia de seguridad.

***

## <mark style="color:purple;">Informe final</mark>

Normalmente, tras revisar el informe con el cliente y confirmar su satisfacción, se puede emitir el informe final con las modificaciones necesarias. Esto puede parecer un proceso superficial, pero varias firmas de auditoría no aceptan un borrador del informe para cumplir con sus obligaciones de cumplimiento, por lo que es importante desde la perspectiva del cliente.

#### **Informe posterior a la remediación**

También es común que un cliente solicite que se vuelvan a analizar los hallazgos detectados durante la evaluación original después de haber tenido la oportunidad de corregirlos. Esto es prácticamente obligatorio para las organizaciones sujetas a un estándar de cumplimiento como PCI. **No debería** rehacer toda la evaluación para esta fase. En su lugar, debería centrarse en volver a analizar únicamente los hallazgos y los hosts afectados por ellos en la evaluación original. También debe asegurarse de que exista un límite de tiempo después de la evaluación inicial para realizar las pruebas de remediación. A continuación, se detallan algunos de los posibles problemas si no lo hace.

* El cliente le pide que pruebe su remediación varios meses o incluso un año o más después, y el entorno ha cambiado tanto que es imposible obtener una comparación "de igual a igual".
* Si verifica todo el entorno en busca de nuevos hosts afectados por un hallazgo determinado, puede descubrir nuevos hosts afectados y caer en un ciclo interminable de pruebas de remediación de los nuevos hosts que descubrió la última vez.
* Si ejecuta nuevos análisis a gran escala, como análisis de vulnerabilidades, probablemente encontrará cosas que no estaban allí antes y su alcance se saldrá de control rápidamente.
* Si un cliente tiene un problema con la naturaleza de "instantánea" de este tipo de prueba, podría recomendar una herramienta de tipo Simulación de ataques y violaciones (BAS) para ejecutar periódicamente esos escenarios y asegurarse de que no sigan apareciendo.

Si se presenta alguna de estas situaciones, debe esperar un mayor escrutinio sobre los niveles de gravedad y quizás presión para modificar aspectos que no deben modificarse para ayudarlos. En estas situaciones, su respuesta debe ser cuidadosamente elaborada para dejar claro que no va a cruzar los límites éticos (pero tenga cuidado de no insinuar que le están pidiendo que haga algo intencionalmente deshonesto, lo que indica que son deshonestos), pero también para comprender su situación y ofrecerles algunas soluciones. Por ejemplo, si su preocupación es estar en apuros con un auditor para corregir algo en un plazo del que no disponen, puede que no sepan que muchos auditores aceptarán un plan de remediación minuciosamente documentado con un plazo razonable (y una justificación de por qué no se puede completar más rápidamente) en lugar de remediar y cerrar el hallazgo dentro del período de examen. Esto le permite mantener su integridad intacta, fomenta en el cliente la sensación de que le importa sinceramente su situación y le ofrece una vía de salida sin tener que esforzarse demasiado para lograrlo.

Un enfoque podría ser considerar esto como una nueva evaluación en estas situaciones. Si el cliente no está dispuesto, probablemente querríamos volver a analizar únicamente los hallazgos del informe original y anotar cuidadosamente en el informe el tiempo transcurrido desde la evaluación original, que se trata de una comprobación puntual para evaluar si SOLO las vulnerabilidades previamente reportadas afectan al host o hosts reportados originalmente y que es probable que el entorno del cliente haya cambiado significativamente, por lo que no se realizó una nueva evaluación.

En términos del diseño del informe, algunas personas pueden preferir actualizar la evaluación original etiquetando los hosts afectados en cada hallazgo con un estado (por ejemplo, resuelto, no resuelto, parcial, etc.), mientras que otras pueden preferir emitir un informe completamente nuevo que tenga algún contenido de comparación adicional y un resumen ejecutivo actualizado.

***

## <mark style="color:purple;">Informe de certificación</mark>

Algunos clientes solicitarán un documento `Attestation Letter` o `Attestation Report` que sea adecuado para sus proveedores o clientes que requieran evidencia de haber realizado una prueba de penetración. La diferencia más significativa es que su cliente no querrá compartir con terceros los detalles técnicos específicos de todos los hallazgos, credenciales u otra información confidencial que pueda estar incluida. Este documento puede derivarse del informe. Debe centrarse únicamente en el número de hallazgos detectados, el enfoque adoptado y comentarios generales sobre el entorno. Probablemente, este documento solo tenga una o dos páginas.

***

## <mark style="color:purple;">Otros entregables</mark>

#### **Presentación de diapositivas**

También se le podría solicitar que prepare una presentación que pueda presentarse en varios niveles. Su audiencia puede ser técnica o más ejecutiva. El lenguaje y el enfoque de su presentación ejecutiva deben ser tan diferentes como el resumen ejecutivo y los detalles técnicos de los hallazgos en su informe. Incluir solo gráficos y cifras aburrirá a su audiencia, así que es mejor estar preparado con algunas anécdotas de su propia experiencia o quizás algunos eventos recientes que se correlacionen con un vector de ataque o una vulneración específica. Puntos extra si dicha historia se relaciona con el mismo sector que su cliente. El objetivo no es alarmista, y debe tener cuidado de no presentarlo de esa manera, pero ayudará a mantener la atención de su audiencia. Hará que el riesgo sea lo suficientemente comprensible como para maximizar sus posibilidades de actuar al respecto.

#### **Hoja de cálculo de hallazgos**

La hoja de cálculo de hallazgos debe ser bastante intuitiva. Contiene todos los campos de los hallazgos de su informe, en un formato tabular que el cliente puede usar para facilitar la clasificación y la manipulación de datos. Esto también puede ayudarle a importar dichos hallazgos a un sistema de tickets para fines de seguimiento interno. Este documento *no* debe incluir su resumen ejecutivo ni narrativas. Idealmente, aprenda a usar tablas dinámicas y utilícelas para crear análisis interesantes que el cliente pueda encontrar interesantes. El objetivo más útil de esto es ordenar los hallazgos por gravedad o categoría para ayudar a priorizar la remediación.

***

## <mark style="color:purple;">Notificaciones de vulnerabilidad</mark>

A veces, durante una evaluación, descubriremos una falla crítica que requiere que detengamos el trabajo e informemos a nuestros clientes sobre un problema para que puedan decidir si desean emitir una solución de emergencia o esperar hasta que finalice la evaluación.

#### **Cuándo redactar uno**

Como mínimo, esto debería hacerse para cualquier hallazgo directamente explotable que se exponga a internet y que provoque la ejecución remota de código no autenticado o la exposición de datos confidenciales, o que utilice credenciales débiles o predeterminadas para ello. Además, las expectativas deben establecerse durante el inicio del proyecto. Algunos clientes podrían querer que todos los hallazgos importantes y críticos se reporten fuera de banda, independientemente de si son internos o externos. Algunos también podrían necesitar medios. Por lo general, es mejor establecer una línea base, explicarle al cliente qué esperar y permitirle solicitar modificaciones al proceso si las necesita.

#### **Contenido**

Debido a la naturaleza de estas notificaciones, es importante limitar la información superflua en estos documentos para que el personal técnico pueda ir directamente a los detalles y comenzar a solucionar el problema. Por esta razón, probablemente sea mejor limitarse al contenido típico de los detalles técnicos de los hallazgos y proporcionar evidencia basada en herramientas que respalde el hallazgo, de modo que el cliente pueda reproducirlo rápidamente si es necesario.
