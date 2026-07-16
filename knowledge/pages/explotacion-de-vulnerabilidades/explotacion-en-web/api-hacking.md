
# API Hacking

## <mark style="color:purple;">Introducción a los ataques API</mark> <a href="#introduction-to-api-attacks" id="introduction-to-api-attacks"></a>

***

Las `Application Programming Interfaces (API)` son fundamentales para el desarrollo de software moderno, siendo las API web la forma más común. Permiten la comunicación fluida y el intercambio de datos entre diversos sistemas a través de internet, actuando como puentes cruciales que facilitan la integración y la colaboración entre diferentes aplicaciones de software.

En esencia, las API consisten en reglas y protocolos definidos que determinan cómo interactúan los distintos sistemas. Especifican los requisitos de formato de datos, definen los métodos de acceso a los recursos y definen las estructuras de respuesta esperadas. Las API se clasifican, en general, en públicas (accesibles a terceros) o privadas (restringidas a organizaciones o grupos de sistemas específicos).

### Estilos de construcción de API <a href="#api-building-styles" id="api-building-styles"></a>

Las API web se pueden crear utilizando varios estilos arquitectónicos, incluidos `REST`, `SOAP`, `GraphQL`, y `gRPC`, cada uno con sus propias fortalezas y casos de uso:

* [Representational State Transfer](https://ics.uci.edu/~fielding/pubs/dissertation/top.htm) ( `REST`) es el estilo de API más popular. Utiliza un modelo `client-server` en el que los clientes realizan solicitudes a recursos en un servidor mediante métodos HTTP estándar ( `GET`, `POST`, `PUT`, `DELETE`). Las API `RESTful` no tienen estado, lo que significa que cada solicitud contiene toda la información necesaria para que el servidor la procese, y las respuestas suelen serializarse como JSON o XML.
* [Simple Object Access Protocol](https://www.w3.org/TR/2000/NOTE-SOAP-20000508/) (`SOAP`) utiliza XML para el intercambio de mensajes entre sistemas. Las API `SOAP` están altamente estandarizadas y ofrecen funciones integrales de seguridad, transacciones y gestión de errores, pero generalmente son más complejas de implementar y usar que las API `REST`.
* [GraphQL](https://graphql.org/) es un estilo alternativo que ofrece una forma más flexible y eficiente de obtener y actualizar datos. En lugar de devolver un conjunto fijo de campos para cada recurso, `GraphQL` permite a los clientes especificar exactamente los datos que necesitan, lo que reduce la sobrecaptura y la subcaptura de datos. Las API `GraphQL` utilizan un único endpoint y un lenguaje de consulta fuertemente tipado para recuperar datos.
* [gRPC](https://grpc.io/) es un estilo más reciente que utiliza [Protocol Buffers](https://protobuf.dev/) para la serialización de mensajes, lo que proporciona una forma eficiente y de alto rendimiento de comunicarse entre sistemas. Las API `gRPC` se pueden desarrollar en diversos lenguajes de programación y son especialmente útiles para microservicios y sistemas distribuidos.

En este módulo, nos centraremos en los ataques contra una [API web RESTful](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html) . Sin embargo, las vulnerabilidades demostradas también podrían existir en API creadas con otros estilos arquitectónicos.

***

## <mark style="color:purple;">Ataques API</mark> <a href="#api-attacks" id="api-attacks"></a>

Debido a su versatilidad y ubicuidad, las API son un arma de doble filo. Si bien son un componente crítico de la arquitectura de software moderna, también presentan una amplia superficie de ataque. La naturaleza misma de las API, que facilitan el intercambio de datos y la comunicación entre diversos sistemas, introduce vulnerabilidades, como `Exposure of Sensitive Data`, `Authentication and Authorization Issues`, `Insufficient Rate Limiting`, `Improper Error Handling` y otras configuraciones de seguridad incorrectas.

### API OWASP Top 10 <a href="#owasp-top-10-api-security-risks" id="owasp-top-10-api-security-risks"></a>

Para categorizar y estandarizar las vulnerabilidades de seguridad y las configuraciones incorrectas que pueden enfrentar las API, [OWASP](https://owasp.org/) ha creado el [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) , una lista completa de los riesgos de seguridad más críticos relacionados específicamente con las API:

| **Riesgo**                                                                                                                                                           | **Descripción**                                                                                                                                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| [API1:2023 - Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)                             | La API permite a los usuarios autenticados acceder a datos que no están autorizados a ver.                                                        |
| [API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)                                                     | Los mecanismos de autenticación de la API se pueden eludir o eludir, permitiendo el acceso no autorizado.                                         |
| [API3:2023 - Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)           | La API revela datos confidenciales a usuarios autorizados a los que no deben acceder o les permite manipular propiedades confidenciales.          |
| [API4:2023 - Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)                             | La API no limita la cantidad de recursos que los usuarios pueden consumir.                                                                        |
| [API5:2023 - Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)                         | La API permite que usuarios no autorizados realicen operaciones autorizadas.                                                                      |
| [API6:2023 - Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/) | La API expone flujos comerciales sensibles, lo que puede generar posibles pérdidas financieras y otros daños.                                     |
| [API7:2023 - Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/)                                         | La API no valida adecuadamente las solicitudes, lo que permite a los atacantes enviar solicitudes maliciosas e interactuar con recursos internos. |
| [API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)                                             | La API sufre configuraciones de seguridad incorrectas, incluidas vulnerabilidades que conducen a ataques de inyección.                            |
| [API9:2023 - Improper Inventory Management](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/)                                     | La API no administra de forma adecuada y segura el inventario de versiones.                                                                       |
| [API10:2023 - Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)                                          | La API consume otra API de forma insegura, lo que genera posibles riesgos de seguridad.                                                           |

Este módulo se centrará en explotar todos estos riesgos de seguridad y comprender cómo prevenirlos.

***

## <mark style="color:purple;">Relacionado</mark>

{% content-ref url="/pages/4HL0qkVNDavWpFlAp9Gg" %}
[IDOR en APIs Inseguras](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-web-modernos/idor/idor-en-apis-inseguras.md)
{% endcontent-ref %}
