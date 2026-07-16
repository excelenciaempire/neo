
# OWASP Top 10

OWASP (Open Web Application Security Project) publica cada pocos años un ranking de los riesgos de seguridad más críticos para aplicaciones web. La última versión (2021) sigue siendo la referencia. Conocer esta lista no es optativo: es la base de cualquier estrategia de pruebas avanzada.

{% embed url="<https://owasp.org/www-project-top-ten/>" %}

A continuación, cada riesgo se explica con un ejemplo concreto y una técnica de testing asociada.

## A01:2021 – Control de acceso roto

Significa que un usuario puede hacer cosas que no debería: ver datos de otro, modificar su perfil o ejecutar acciones administrativas.

**Ejemplo:** Un endpoint `GET /api/orders/{id}` no verifica que el `id` pertenezca al usuario autenticado. Cualquier cliente puede cambiar el número y ver pedidos ajenos (IDOR).

**Técnica de testing:** Probar con identificadores secuenciales o UUIDs adivinables; modificar el método HTTP (cambiar GET por POST) para saltar reglas mal configuradas.

## A02:2021 – Fallos criptográficos

Datos sensibles en tránsito o en reposo sin cifrado adecuado, o cifrado débil (MD5, SHA1, algoritmos obsoletos).

**Ejemplo:** La aplicación envía la cookie de sesión por HTTP sin TLS. Un atacante en la misma red la roba mediante sniffing.

**Técnica de testing:** Inspeccionar cabeceras, buscar `http://` en lugar de `https://`, probar si se pueden forzar conexiones sin cifrar (downgrade attack).

## A03:2021 – Inyección

SQL, NoSQL, comandos del sistema, LDAP… El clásico que no muere. Ocurre cuando datos no confiables se concatenan en un intérprete.

**Ejemplo:** `consulta = "SELECT * FROM usuarios WHERE nombre = '" + nombre + "'";` con `nombre = "admin' --"`.

**Técnica de testing:** Fuzzing de parámetros con payloads específicos; uso de `sqlmap` en modo seguro.

## A04:2021 – Diseño inseguro

Fallo a nivel de arquitectura o flujo lógico, no de código. OWASP diferencia esto de los fallos de implementación.

**Ejemplo:** Una tienda aplica descuentos en el front-end y confía en el precio enviado desde el cliente. Un atacante modifica el valor con Burp y se lleva productos gratis.

**Técnica de testing:** Analizar diagramas de flujo, probar transacciones fuera de orden, manipular parámetros que deberían ser inmutables en cliente.

## A05:2021 – Configuración de seguridad incorrecta

Software desactualizado, puertos innecesarios abiertos, mensajes de error detallados, configuraciones por defecto (contraseñas `admin/admin`).

**Ejemplo:** El panel de administración de Tomcat expuesto en `/manager/html` con credenciales por defecto.

**Técnica de testing:** Escaneo de directorios comunes, revisión de cabeceras HTTP (missing security headers), versión del servidor en banners.

## A06:2021 – Componentes vulnerables y desactualizados

Librerías de terceros (npm, pip, Maven) con vulnerabilidades conocidas.

**Ejemplo:** La versión de Log4j anterior a 2.15.0, que permite ejecución remota de código (Log4Shell).

**Técnica de testing:** Análisis de dependencias con herramientas como OWASP Dependency-Check, Snyk, o `npm audit`.

## A07:2021 – Fallos de identificación y autenticación

Mecanismos de login débiles: permitir credenciales comunes, no limitar intentos, recuperación de contraseña insegura, tokens JWT con firma mal validada.

**Ejemplo:** El token JWT usa el algoritmo `none` si se modifica la cabecera; el servidor lo acepta.

**Técnica de testing:** Fuerza bruta controlada, pruebas de bypass de login con parámetros como `password=' OR 1=1 --`, manipulación de tokens.

## A08:2021 – Fallos de integridad de software y datos

Confiar en actualizaciones o datos sin verificar firma o integridad. Muy relevante en CI/CD y plugins.

**Ejemplo:** Una extensión de WordPress se descarga desde un canal no HTTPS y es manipulada en tránsito.

**Técnica de testing:** Verificar que las actualizaciones se sirven sobre TLS y que el código está firmado; probar si se puede sustituir un recurso por otro malicioso.

## A09:2021 – Fallos de monitoreo y registro

No hay logs, o están incompletos, o no se generan alertas ante intentos de ataque. Esto impide detectar una intrusión a tiempo.

**Ejemplo:** Un atacante prueba 500 contraseñas en un usuario y nunca se genera un evento de seguridad.

**Técnica de testing:** Intentar acciones sospechosas deliberadamente y verificar si aparecen en los registros a los que el equipo de seguridad tiene acceso.

## A10:2021 – Server-Side Request Forgery (SSRF)

El servidor realiza peticiones HTTP a URLs controladas por el atacante, lo que permite escanear redes internas o acceder a servicios no expuestos.

**Ejemplo:** Un endpoint `POST /proxy?url=https://api.example.com/data` puede cambiarse a `http://169.254.169.254/latest/meta-data/` para robar credenciales de la nube.

**Técnica de testing:** Fuzzing de parámetros de URL, probar protocolos `file://`, `gopher://`, puertos internos comunes.

***

#### ¡Ojo! No es una lista de vulnerabilidades

Muchos profesionales cometen el error de tratar OWASP Top 10 como un chequeo estático. En realidad es un **ranking de riesgos**, donde cada riesgo agrupa múltiples vulnerabilidades. Para hacer un testing avanzado, debes entender el riesgo y después buscar sus manifestaciones concretas.
