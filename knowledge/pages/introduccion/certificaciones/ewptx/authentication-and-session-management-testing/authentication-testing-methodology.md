
# Authentication Testing Methodology

## <mark style="color:$primary;">Metodología de Autenticación</mark>

Authentication testing es el proceso de **sondear y explotar debilidades** en los mecanismos de verificación de identidad de una aplicación web. No se trata solo de probar si el formulario de login funciona correctamente (eso ya lo hacen los tests funcionales), sino de encontrar la manera de **saltarlo, engañarlo o romperlo**.

En términos prácticos: el equipo de desarrollo construyó una puerta. Tu trabajo como tester es intentar abrirla sin la llave, forzarla o encontrar la ventana que dejaron abierta.

***

### ¿Qué se prueba exactamente?

El testing de autenticación abarca todos los componentes relacionados con la verificación de identidad:

<table data-header-hidden><thead><tr><th width="270.03704833984375"></th><th></th></tr></thead><tbody><tr><td>Componente</td><td>¿Qué se prueba?</td></tr><tr><td><strong>Login forms</strong></td><td>¿Se puede enumerar usuarios? ¿Es vulnerable a fuerza bruta? ¿Hay bypass mediante inyección?</td></tr><tr><td><strong>Password reset functionality</strong></td><td>¿El enlace de restablecimiento es predecible? ¿Se puede cambiar la contraseña de otro usuario?</td></tr><tr><td><strong>Multi-factor authentication (MFA/2FA)</strong></td><td>¿Es obligatorio? ¿Se puede omitir? ¿Los códigos son predecibles o reutilizables?</td></tr><tr><td><strong>Account lockouts</strong></td><td>¿Existe bloqueo tras múltiples fallos? ¿Se puede provocar un DoS bloqueando cuentas ajenas?</td></tr><tr><td><strong>Registration functionality</strong></td><td>¿Se pueden registrar cuentas con emails existentes (toma de cuenta)? ¿Se puede escalar privilegios en el registro?</td></tr><tr><td><strong>Change credentials</strong></td><td>¿Requiere la contraseña actual? ¿Se puede cambiar la contraseña de otro usuario?</td></tr><tr><td><strong>Logout functionality</strong></td><td>¿Realmente invalida la sesión en el servidor?</td></tr></tbody></table>

***

### ¿Qué vulnerabilidades busca?

El objetivo final es descubrir fallos que puedan permitir:

1. **Bypass de controles de login** – Entrar sin necesidad de credenciales (ej. mediante inyección SQL en el formulario de login).
2. **Weak password policies** – Contraseñas demasiado cortas, sin complejidad, o que permiten palabras comunes del diccionario.
3. **Brute force / Credential stuffing** – Ausencia de rate limiting o captcha, permitiendo probar miles de combinaciones.
4. **Session fixation** – Forzar a la víctima a usar un Session ID conocido.
5. **Inadequate token handling** – Tokens de recuperación de contraseña predecibles, JWT sin firma o con algoritmos débiles.
6. **Enumeración de usuarios** – Poder determinar qué usuarios existen en el sistema.
7. **Autenticación deficiente en APIs** – Endpoints de autenticación sin las mismas protecciones que la interfaz web.

***

## <mark style="color:$primary;">OWASP WSTG</mark>

{% embed url="<https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/README>" %}

El **OWASP Web Security Testing Guide (WSTG)** dedica una sección completa a las pruebas de autenticación. La metodología se organiza en las siguientes categorías (versión 4.2):

<table data-header-hidden><thead><tr><th width="171.962890625"></th><th width="250.96295166015625"></th><th></th></tr></thead><tbody><tr><td>ID</td><td>Prueba</td><td>Descripción breve</td></tr><tr><td><strong>WSTG-ATHN-01</strong></td><td>Testing for Credentials Transported over an Encrypted Channel</td><td>Verificar que las credenciales solo viajan por HTTPS (nunca HTTP plano).</td></tr><tr><td><strong>WSTG-ATHN-02</strong></td><td>Testing for Default Credentials</td><td>Buscar usuarios y contraseñas por defecto (admin/admin, root/root, etc.).</td></tr><tr><td><strong>WSTG-ATHN-03</strong></td><td>Testing for Weak Lock Out Mechanism</td><td>Probar el mecanismo de bloqueo por intentos fallidos (rate limiting, captcha, tiempo de espera).</td></tr><tr><td><strong>WSTG-ATHN-04</strong></td><td>Testing for Bypassing Authentication Schema</td><td>Intentar saltar el login mediante inyección, modificación de parámetros o manipulación de respuestas.</td></tr><tr><td><strong>WSTG-ATHN-05</strong></td><td>Testing for Vulnerable Remember Password</td><td>Probar la funcionalidad "recordarme" (cómo almacena la cookie, si es predecible).</td></tr><tr><td><strong>WSTG-ATHN-06</strong></td><td>Testing for Browser Cache Weaknesses</td><td>Verificar que las páginas sensibles no se almacenan en caché del navegador.</td></tr><tr><td><strong>WSTG-ATHN-07</strong></td><td>Testing for Weak Password Policy</td><td>Validar la política de contraseñas (longitud, complejidad, diccionario).</td></tr><tr><td><strong>WSTG-ATHN-08</strong></td><td>Testing for Weak Security Question/Answer</td><td>Probar preguntas de seguridad (¿son fáciles de adivinar o investigar?).</td></tr><tr><td><strong>WSTG-ATHN-09</strong></td><td>Testing for Weak Password Change or Reset Functionality</td><td>Verificar que cambiar/recuperar contraseña es seguro y no permite toma de cuentas.</td></tr><tr><td><strong>WSTG-ATHN-10</strong></td><td>Testing for Weaker Authentication in Alternative Channels</td><td>Probar autenticación en canales alternativos (APIs, webservices, versiones móviles).</td></tr></tbody></table>

***

## <mark style="color:$primary;">Enfoque práctico: ¿por dónde empiezo?</mark>

Aquí hay una secuencia lógica para abordar el testing de autenticación en cualquier aplicación web:

1. **Reconocimiento inicial** (navegación manual)
   * Identifica todos los puntos de autenticación: login, registro, recuperación, cambio de contraseña, MFA, etc.
   * Anota si hay rate limiting aparente (¿mensajes de "demasiados intentos"?).
   * Observa si se usan captchas.
2. **Transporte de credenciales**
   * Verifica que todo formulario de login use HTTPS.
   * Comprueba que las credenciales no aparezcan en la URL (método GET en lugar de POST).
3. **Enumeración de usuarios**
   * Prueba mensajes de error diferenciales ("usuario no existe" vs. "contraseña incorrecta").
   * Observa tiempos de respuesta (pueden variar entre usuarios existentes e inexistentes).
4. **Política de contraseñas**
   * Intenta registrar cuentas con contraseñas débiles ("123456", "password", "admin", "qwerty").
   * Verifica longitud mínima y requisitos de complejidad.
5. **Fuerza bruta (con autorización)**
   * Prepara listas de usuarios (si los enumeraste) y contraseñas comunes (SecLists, rockyou.txt).
   * Usa Burp Intruder o Hydra con pausas para respetar límites.
   * **Nunca** en producción sin autorización explícita.
6. **Bypass de autenticación**
   * Prueba inyecciones en campos de usuario/contraseña (`' OR '1'='1`, `admin'--`).
   * Manipula parámetros de respuesta (si el login devuelve `success=false`).
   * Intenta acceder directamente a URLs autenticadas sin haber hecho login.
7. **Recuperación de contraseña**
   * Solicita un restablecimiento para tu cuenta y analiza el enlace: ¿es predecible (timestamp, hash corto)? ¿expira?
   * Intenta restablecer la contraseña de otro usuario (cambiando el email o ID en la petición).
   * Verifica que el token de recuperación no se pueda adivinar.
8. **MFA/2FA**
   * Si hay MFA, ¿se puede omitir modificando la respuesta?
   * ¿El código MFA es numérico de 6 dígitos? ¿Hay rate limiting? ¿Se puede forzar bruto?
   * ¿Se puede registrar sin configurar MFA aunque sea obligatorio?
9. **Cierre de sesión**
   * Inicia sesión, captura el Session ID, cierra sesión, reutiliza el ID. ¿Sigue funcionando?

***

## <mark style="color:$primary;">Herramientas específicas</mark>

<table data-header-hidden><thead><tr><th width="203.370361328125"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Uso principal</td></tr><tr><td><strong>Burp Suite (Intruder)</strong></td><td>Fuerza bruta, fuzzing de parámetros de autenticación.</td></tr><tr><td><strong>Burp Suite (Repeater)</strong></td><td>Manipulación manual de peticiones de login, recuperación, MFA.</td></tr><tr><td><strong>Hydra</strong></td><td>Fuerza bruta desde línea de comandos (útil para scripts).</td></tr><tr><td><strong>Medusa</strong></td><td>Alternativa a Hydra, más rápida en algunos escenarios.</td></tr><tr><td><strong>Patator</strong></td><td>Fuerza bruta modular (soporta diferentes protocolos).</td></tr><tr><td><strong>wfuzz</strong></td><td>Fuzzing de parámetros, incluyendo autenticación básica y formularios.</td></tr><tr><td><strong>CrackMapExec</strong></td><td>Para autenticación en entornos de dominio, útil en pruebas internas.</td></tr><tr><td><strong>EyeWitness</strong></td><td>Captura de pantallas de páginas de login para documentación.</td></tr><tr><td><strong>Nmap (http-form-brute script)</strong></td><td>Escaneo rápido de autenticación débil.</td></tr><tr><td><strong>Python (requests + multiprocessing)</strong></td><td>Scripts personalizados para pruebas específicas.</td></tr></tbody></table>

***

## <mark style="color:$primary;">Checklist - Authentication Testing</mark>

<table data-header-hidden><thead><tr><th width="78.592529296875"></th><th width="369.66668701171875"></th><th width="181.962890625"></th><th></th></tr></thead><tbody><tr><td>#</td><td>Prueba</td><td>Herramienta</td><td>Severidad</td></tr><tr><td>1</td><td>Las credenciales viajan solo por HTTPS</td><td>Burp, navegador</td><td>Crítica</td></tr><tr><td>2</td><td>No hay credenciales por defecto (admin/admin)</td><td>Manual, wordlists</td><td>Alta</td></tr><tr><td>3</td><td>Existe rate limiting o captcha tras N fallos</td><td>Burp Intruder</td><td>Alta</td></tr><tr><td>4</td><td>Mensajes de error no permiten enumerar usuarios</td><td>Manual</td><td>Media</td></tr><tr><td>5</td><td>Política de contraseñas robusta (min 8-12, complejidad)</td><td>Registro manual</td><td>Media</td></tr><tr><td>6</td><td>El sistema bloquea contraseñas comunes (rockyou)</td><td>Diccionario</td><td>Media</td></tr><tr><td>7</td><td>No se puede hacer bypass mediante inyección SQL</td><td>Payloads manuales</td><td>Crítica</td></tr><tr><td>8</td><td>El enlace de recuperación es impredecible y expira</td><td>Análisis manual</td><td>Alta</td></tr><tr><td>9</td><td>No se puede cambiar contraseña de otro usuario</td><td>Manipulación ID</td><td>Alta</td></tr><tr><td>10</td><td>MFA no es salteable (requerido, sin bypass)</td><td>Manipulación</td><td>Crítica</td></tr><tr><td>11</td><td>Logout invalida la sesión en servidor</td><td>Reutilizar cookie</td><td>Alta</td></tr><tr><td>12</td><td>La caché del navegador no guarda páginas sensibles</td><td>Verificar cabeceras</td><td>Media</td></tr></tbody></table>

***

## <mark style="color:$primary;">Ejemplo práctico: fuerza bruta controlada con Burp Intruder</mark>

**Escenario:** Formulario de login sin captcha ni rate limiting (en entorno autorizado).

**Paso 1 – Capturar la petición**\
Envía una petición de login con credenciales de prueba (ej. `usuario=test&pass=test`). Intercepta con Burp Proxy.

**Paso 2 – Enviar a Intruder**\
Haz clic derecho → `Send to Intruder`.

**Paso 3 – Configurar posiciones de ataque**

* Posición 1: usuario (marca `test`)
* Posición 2: contraseña (marca `test`)
* Tipo de ataque: `Cluster bomb` (prueba todas las combinaciones)

**Paso 4 – Cargar payloads**

* Payload 1 (usuarios): lista de usuarios encontrados (o diccionario común)
* Payload 2 (contraseñas): rockyou.txt o lista de contraseñas débiles

**Paso 5 – Configurar recurso de agrupamiento (Resource pool)**

* `Maximum concurrent requests`: 1 o 2 (evitar saturar)
* `Delay between requests`: 1000 ms (respetar límites)

**Paso 6 – Configurar detección de éxito**\
Ve a `Settings > Grep - Match` y añade una cadena que aparezca solo en login exitoso (ej. "Bienvenido" o la redirección a `/dashboard`).

**Paso 7 – Ejecutar**\
Lanza el ataque. Observa las peticiones que contienen la cadena de éxito.

**⚠️ Precaución:** Este procedimiento solo debe ejecutarse en entornos autorizados. Incluso así, avisa a los administradores del sistema para que monitoricen posibles bloqueos de cuenta.

***

## <mark style="color:$primary;">📚 Referencias OWASP WSTG</mark>

* [WSTG - Latest: Authentication Testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/README)
* [WSTG-ATHN-01: Testing for Credentials Transported over an Encrypted Channel](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/01-Testing_for_Credentials_Transported_over_an_Encrypted_Channel)
* [WSTG-ATHN-02: Testing for Default Credentials](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Default_Credentials)
* [WSTG-ATHN-03: Testing for Weak Lock Out Mechanism](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism)
* [WSTG-ATHN-04: Testing for Bypassing Authentication Schema](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/04-Testing_for_Bypassing_Authentication_Schema)
* [WSTG-ATHN-05: Testing for Vulnerable Remember Password](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/05-Testing_for_Vulnerable_Remember_Password)
* [WSTG-ATHN-06: Testing for Browser Cache Weaknesses](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/06-Testing_for_Browser_Cache_Weaknesses)
* [WSTG-ATHN-07: Testing for Weak Password Policy](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/07-Testing_for_Weak_Password_Policy)
* [WSTG-ATHN-08: Testing for Weak Security Question/Answer](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/08-Testing_for_Weak_Security_Question_Answer)
* [WSTG-ATHN-09: Testing for Weak Password Change or Reset Functionality](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/09-Testing_for_Weak_Password_Change_or_Reset_Functionality)
* [WSTG-ATHN-10: Testing for Weaker Authentication in Alternative Channels](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/10-Testing_for_Weaker_Authentication_in_Alternative_Channels)
