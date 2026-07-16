
# Introducción

La autenticación y la gestión de sesiones son las **puertas de entrada** a cualquier aplicación web. No importa cuán seguro sea el código interno, si un atacante puede suplantar a un usuario legítimo, toda la aplicación está comprometida. Por eso, esta área es casi siempre la primera en la lista de prioridades de cualquier prueba de penetración que se precie.

***

### ¿Por qué son tan críticas?

Imagina una fortaleza con muros de diez metros de altura, sistemas de vigilancia avanzados y guardias entrenados. Ahora imagina que la puerta principal tiene una cerradura de juguete. Todo el resto del esfuerzo es irrelevante.

La autenticación y la gestión de sesiones son esa **puerta principal**. Si fallan:

* Un atacante puede acceder a cuentas de administrador.
* Datos sensibles de usuarios pueden ser robados.
* Operaciones críticas (transferencias bancarias, cambios de contraseña, compras) pueden ser ejecutadas por quien no debe.
* La reputación de la empresa se desploma.
* En muchos sectores, hay consecuencias legales y regulatorias (GDPR, PCI-DSS, HIPAA, etc.).

Por eso, **el testing de autenticación y sesiones es obligatorio en cualquier auditoría de seguridad** y suele ser el punto de partida después del reconocimiento inicial.

***

### Autenticación vs. Autorización vs. Gestión de sesiones

Antes de profundizar, conviene distinguir tres conceptos que a menudo se confunden:

<table data-header-hidden><thead><tr><th width="151.96295166015625"></th><th width="369.111083984375"></th><th></th></tr></thead><tbody><tr><td>Concepto</td><td>Definición</td><td>Pregunta que responde</td></tr><tr><td><strong>Autenticación</strong></td><td>Verificar que el usuario es quien dice ser (mediante credenciales, biometría, MFA, etc.)</td><td><em>"¿Quién eres?"</em></td></tr><tr><td><strong>Autorización</strong></td><td>Determinar qué puede hacer un usuario autenticado (permisos, roles, políticas de acceso)</td><td><em>"¿Qué puedes hacer?"</em></td></tr><tr><td><strong>Gestión de sesiones</strong></td><td>Mantener el estado del usuario entre múltiples peticiones HTTP (stateless)</td><td><em>"¿Cómo te recordamos?"</em></td></tr></tbody></table>

Un fallo en autenticación permite a un atacante **entrar** sin ser quien dice ser. Un fallo en autorización permite a un usuario legítimo **hacer cosas que no debería**. Un fallo en gestión de sesiones permite **secuestrar la identidad** de otro usuario ya autenticado.

Esta sección cubre **autenticación y gestión de sesiones**.

***

### Objetivos del testing de autenticación y sesiones

Cuando pruebas los mecanismos de autenticación y gestión de sesiones de una aplicación web, buscas responder estas preguntas:

#### **Sobre autenticación**

* ¿Se puede enumerar usuarios válidos a través de mensajes de error diferenciales?
* ¿El sistema es vulnerable a fuerza bruta (ausencia de rate limiting o captcha)?
* ¿Las políticas de contraseña son suficientemente robustas?
* ¿El mecanismo de "olvidé mi contraseña" es seguro (o permite tomar el control de cuentas)?
* ¿Se puede registrar un usuario con un email existente (toma de cuenta)?
* ¿El MFA/2FA es obligatorio y se puede sortear?
* ¿Las credenciales se transmiten siempre cifradas (HTTPS)?

#### **Sobre gestión de sesiones**

* ¿Los Session IDs son criptográficamente aleatorios e impredecibles?
* ¿Las cookies tienen los flags de seguridad (`Secure`, `HttpOnly`, `SameSite`)?
* ¿El Session ID se regenera después del login exitoso (previene fijación)?
* ¿Las sesiones expiran por inactividad y tienen una expiración absoluta?
* ¿El logout invalida correctamente la sesión en el servidor?
* ¿Se puede secuestrar una sesión mediante XSS (falta `HttpOnly`), sniffing (falta `Secure`) o predicción?
* ¿El sistema es vulnerable a Session Fixation?

***

### Enfoque metodológico

Como ya vimos en la sección de **Metodología** (fases 6, 7 y 8), las pruebas de autenticación y sesiones se dividen en tres bloques distintos:

<table data-header-hidden><thead><tr><th width="83.81475830078125"></th><th width="258.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Fase</td><td>Nombre</td><td>Qué prueba</td></tr><tr><td><strong>6</strong></td><td>Authentication Testing</td><td>Login, registro, recuperación, MFA, credenciales</td></tr><tr><td><strong>7</strong></td><td>Authorization Testing</td><td>Permisos, roles, IDOR (se verá en detalle más adelante)</td></tr><tr><td><strong>8</strong></td><td>Session Management Testing</td><td>Cookies, tokens, expiración, hijacking, fixation</td></tr></tbody></table>

En esta sección nos centramos en **Authentication (6)** y **Session Management (8)**.

***

## <mark style="color:$primary;">Áreas de prueba específicas</mark>

A continuación, un mapa de las pruebas que desarrollaremos en los siguientes capítulos:

#### **Authentication Testing (Fase 6)**

<table data-header-hidden><thead><tr><th width="238.1851806640625"></th><th></th></tr></thead><tbody><tr><td>Prueba</td><td>Descripción breve</td></tr><tr><td><strong>Enumeración de usuarios</strong></td><td>Detectar si se puede saber qué usuarios existen mediante mensajes de error, tiempos de respuesta o endpoints diferenciales.</td></tr><tr><td><strong>Fuerza bruta (credential stuffing)</strong></td><td>Probar listas de contraseñas comunes, diccionarios o credenciales filtradas (con autorización y límites de tasa).</td></tr><tr><td><strong>Políticas de contraseña</strong></td><td>Validar longitud mínima, complejidad, uso de contraseñas comunes prohibidas, historial, etc.</td></tr><tr><td><strong>Recuperación de contraseña</strong></td><td>Verificar que el proceso no permita tomar el control de cuentas ajenas (enlaces predecibles, respuesta de seguridad débil, preguntas fáciles de adivinar).</td></tr><tr><td><strong>Registro de usuarios</strong></td><td>Probar si se puede registrar con emails existentes (toma de cuenta), si se puede crear un usuario con privilegios escalados, si la verificación de email es salteable.</td></tr><tr><td><strong>MFA/2FA</strong></td><td>Verificar si el segundo factor es obligatorio, si se puede omitir, si los códigos son predecibles o reutilizables, si hay rate limiting.</td></tr><tr><td><strong>Capacidad de cambio de credenciales</strong></td><td>Probar que cambiar contraseña requiere la contraseña actual (o confirmación por email/MFA) y que no se puede cambiar la de otro usuario.</td></tr><tr><td><strong>Credenciales por defecto</strong></td><td>Buscar usuarios conocidos (<code>admin</code>, <code>test</code>, <code>guest</code>) con contraseñas por defecto o débiles.</td></tr></tbody></table>

#### **Session Management Testing (Fase 8)**

<table data-header-hidden><thead><tr><th width="241.888916015625"></th><th></th></tr></thead><tbody><tr><td>Prueba</td><td>Descripción breve</td></tr><tr><td><strong>Análisis de cookies</strong></td><td>Verificar flags <code>Secure</code>, <code>HttpOnly</code>, <code>SameSite</code>, <code>Domain</code>, <code>Path</code>, expiración.</td></tr><tr><td><strong>Aleatoriedad de Session ID</strong></td><td>Usar Burp Sequencer o herramientas similares para medir entropía y detectar patrones predecibles.</td></tr><tr><td><strong>Regeneración post-login</strong></td><td>Confirmar que el Session ID cambia después de una autenticación exitosa (previene fijación).</td></tr><tr><td><strong>Regeneración en cambio de rol</strong></td><td>Verificar que el Session ID cambia cuando un usuario cambia su nivel de privilegios (ej. se convierte en admin).</td></tr><tr><td><strong>Expiración de sesión</strong></td><td>Probar que la sesión expira por inactividad (timeout) y por tiempo máximo absoluto.</td></tr><tr><td><strong>Invalidación en logout</strong></td><td>Confirmar que cerrar sesión invalida el Session ID en el servidor (no solo en el cliente).</td></tr><tr><td><strong>Session Fixation</strong></td><td>Intentar fijar un Session ID conocido antes de autenticación y verificar si se mantiene tras login.</td></tr><tr><td><strong>Session Hijacking</strong></td><td>Probar robo mediante XSS (si no hay <code>HttpOnly</code>), sniffing (si no hay <code>Secure</code> o HTTPS inconsistente), o predicción.</td></tr><tr><td><strong>Concurrencia de sesiones</strong></td><td>Determinar si se permiten múltiples sesiones por usuario y si hay notificaciones de nuevos inicios de sesión.</td></tr><tr><td><strong>Tokens en URL</strong></td><td>Verificar que los Session IDs nunca viajen en la URL (query string), solo en cookies o cabeceras seguras.</td></tr></tbody></table>

***

## <mark style="color:$primary;">Herramientas habituales</mark>

| Herramienta                                     | Uso en autenticación y sesiones                                      |
| ----------------------------------------------- | -------------------------------------------------------------------- |
| **Burp Suite (Repeater, Intruder, Sequencer)**  | Manipulación de peticiones, fuerza bruta, análisis de tokens.        |
| **ZAP (OWASP Zed Attack Proxy)**                | Alternativa gratuita similar a Burp.                                 |
| **Hydra / Medusa**                              | Fuerza bruta de formularios de login desde línea de comandos.        |
| **wfuzz**                                       | Fuzzing de parámetros de autenticación.                              |
| **EditThisCookie / Cookie-Editor**              | Manipulación rápida de cookies desde navegador.                      |
| **Browser DevTools (Consola, Application tab)** | Inspección de cookies, pruebas manuales de XSS para robo.            |
| **curl**                                        | Peticiones automatizadas para probar reutilización de sesiones.      |
| **Python (requests, selenium)**                 | Automatización de flujos de autenticación y pruebas de concurrencia. |

***

## <mark style="color:$primary;">⚠️ Consideraciones importantes antes de empezar</mark>

#### **Alcance y autorización (fase Pre-Engagement)**

Las pruebas de autenticación pueden ser especialmente **agresivas**:

* **Fuerza bruta** puede bloquear cuentas reales.
* **Recuperación de contraseña** puede enviar correos no deseados a usuarios reales.
* **Registro masivo** puede llenar la base de datos de cuentas basura.

#### **Antes de ejecutar cualquier prueba:**

1. Confirmar por escrito que **está permitido** bloquear cuentas (si no, usa listas de usuarios de prueba).
2. Definir ventanas de ejecución (evitar horas punta).
3. Tener una cuenta de contacto para desbloquear cuentas bloqueadas accidentalmente.
4. Usar entornos de **staging** o **sandbox** siempre que sea posible.

#### **Entorno de pruebas recomendado**

Siempre que puedas, trabaja sobre:

* Un entorno de desarrollo o staging idéntico a producción.
* Cuentas de prueba dedicadas (no las de usuarios reales).
* Una base de datos con datos sintéticos, no reales.

Si la única opción es producción (algunos pentests lo exigen), extremar las precauciones.

#### **Ética y legalidad**

* **Nunca** realices fuerza bruta contra sistemas que no son tuyos sin autorización.
* **Nunca** explotes un fallo de autenticación para acceder a cuentas reales (solo a las de prueba).
* **Nunca** reveles vulnerabilidades públicamente sin haber seguido un proceso de divulgación responsable.

***

#### 📚 Lo que verás en los siguientes capítulos

Con esta introducción como base, pasaremos a los detalles prácticos:

1. **Pruebas de autenticación** (fase 6)
   * Enumeración de usuarios
   * Fuerza bruta y credential stuffing
   * Pruebas de políticas de contraseña
   * Recuperación de contraseña insegura
   * MFA/2FA bypass
   * Registro de usuarios vulnerable
2. **Pruebas de gestión de sesiones** (fase 8)
   * Análisis de cookies y atributos
   * Análisis de entropía (Burp Sequencer)
   * Regeneración de Session IDs
   * Expiración y logout
   * Session Fixation (en profundidad)
   * Session Hijacking: predicción, sniffing, XSS (ya visto en detalle anteriormente)
3. **Casos prácticos y ejercicios** (aplicación vulnerable de laboratorio)

***

## <mark style="color:$primary;">Referencias oficiales</mark>

* [OWASP Testing Guide: Authentication Testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/README)
* [OWASP Testing Guide: Session Management Testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/README)
* [OWASP Cheat Sheet: Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
* [OWASP Cheat Sheet: Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
* [PortSwigger Web Security Academy: Authentication](https://portswigger.net/web-security/authentication)
