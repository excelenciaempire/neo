
# Username Enumeration

## <mark style="color:$primary;">Introducción</mark>

La enumeración de usuarios es una de las vulnerabilidades más comunes y a menudo subestimadas en los mecanismos de autenticación. No permite acceder directamente a una cuenta, pero es el **primer paso crítico** para ataques posteriores como fuerza bruta, credential stuffing o ingeniería social. Un atacante que conoce la lista de usuarios válidos ya tiene la mitad del trabajo hecho.

***

#### ¿Qué es la enumeración de usuarios?

La enumeración de usuarios ocurre cuando un atacante puede **determinar si un nombre de usuario (o email) existe en el sistema** basándose en las respuestas del servidor. Esto suele ser posible porque la aplicación se comporta de manera diferente ante un usuario existente que ante uno inexistente.

No se trata de una vulnerabilidad que comprometa cuentas directamente, pero es un **enumerador de información** que facilita ataques posteriores. En el OWASP Top 10, se considera parte de **A01: Control de acceso roto** y **A07: Fallos de identificación y autenticación**.

***

#### ¿Por qué es peligrosa?

<table data-header-hidden><thead><tr><th width="217.4444580078125"></th><th></th></tr></thead><tbody><tr><td>Ataque posterior</td><td>Cómo ayuda la enumeración</td></tr><tr><td><strong>Fuerza bruta</strong></td><td>Reduce el espacio de búsqueda de millones de usuarios posibles a unos pocos cientos o miles.</td></tr><tr><td><strong>Credential stuffing</strong></td><td>Permite probar listas de credenciales filtradas solo contra usuarios existentes.</td></tr><tr><td><strong>Ingeniería social</strong></td><td>El atacante sabe a quién contactar o suplantar.</td></tr><tr><td><strong>Ataques de diccionario</strong></td><td>Optimiza el tiempo al no perder recursos con usuarios inexistentes.</td></tr><tr><td><strong>DoS por bloqueo de cuentas</strong></td><td>El atacante puede enumerar usuarios y luego provocar bloqueos intencionados.</td></tr></tbody></table>

***

## <mark style="color:$primary;">Vectores comunes de enumeración</mark>

Los vectores de enumeración se basan en **diferencias observables** en la respuesta del servidor cuando se introduce un usuario existente vs. inexistente.

### **1. Mensajes de error diferenciales**

El vector más común y fácil de explotar.

**Comportamiento vulnerable:**

* Usuario inexistente: *"`El usuario no existe`"*
* Usuario existente, contraseña incorrecta: *"`Contraseña incorrecta`"*

**Mensajes neutrales (buena práctica):**

* Usuario inexistente: *"`Credenciales inválidas`"*
* Usuario existente, contraseña incorrecta: *"`Credenciales inválidas`"*

**Cómo testearlo:**

```bash
POST /login HTTP/1.1
Host: ejemplo.com
Content-Type: application/x-www-form-urlencoded

username=usuario_inexistente&password=cualquiercosa
```

vs.

```bash
POST /login HTTP/1.1
Host: ejemplo.com
Content-Type: application/x-www-form-urlencoded

username=admin&password=cualquiercosa
```

Compara los mensajes de error.

### **2. Diferencias en tiempos de respuesta**

Incluso si los mensajes de error son idénticos, el **tiempo que tarda el servidor en responder** puede variar.

**Causas:**

* El servidor busca al usuario en la base de datos (existente) vs. respuesta inmediata (inexistente).
* El servidor aplica el hash de la contraseña (existente) vs. aborta temprano (inexistente).
* El servidor ejecuta lógica adicional (como registrar el intento fallido) solo para usuarios existentes.

**Cómo testearlo:**

```bash
# Usar time curl para medir
time curl -X POST https://ejemplo.com/login -d "username=admin&password=wrong"
time curl -X POST https://ejemplo.com/login -d "username=xyz123&password=wrong"

# O usar Burp Repeater con el medidor de tiempo
```

**Herramientas específicas:**

* **Timing attack detector** (plugins Burp)
* **Scripts personalizados** con mediciones estadísticas (múltiples muestras para evitar ruido)

### **3. Códigos de estado HTTP**

El servidor puede devolver códigos diferentes según el resultado de la autenticación.

<table data-header-hidden><thead><tr><th width="171.22222900390625"></th><th></th><th></th></tr></thead><tbody><tr><td>Código</td><td>Significado</td><td>Uso común</td></tr><tr><td>200 OK</td><td>Página de error mostrada (usuario inexistente o contraseña incorrecta)</td><td>Poco informativo por sí solo</td></tr><tr><td>302 Found</td><td>Redirección a dashboard (login exitoso)</td><td>Útil para fuerza bruta</td></tr><tr><td>401 Unauthorized</td><td>Autenticación fallida (puede ser igual para ambos casos)</td><td>Neutral si es igual</td></tr><tr><td>403 Forbidden</td><td>Cuenta bloqueada o acceso denegado</td><td>Puede revelar existencia</td></tr></tbody></table>

**Cómo testearlo:**\
Observa la cabecera `Location` en respuestas 302. Si redirige a `/dashboard` solo cuando el usuario existe (incluso con contraseña incorrecta), es un fallo.

### **4. Diferencias en el cuerpo de la respuesta**

Incluso si el mensaje principal es idéntico, el HTML puede contener diferencias sutiles:

* Comentarios HTML (`<!-- usuario encontrado -->`)
* Campos ocultos distintos
* JavaScript adicional para usuarios existentes
* URLs de recursos diferentes (imágenes, CSS)
* Longitud de la respuesta (content-length)

**Cómo testearlo:**

```bash
# Comparar longitudes de respuesta
curl -s -X POST https://ejemplo.com/login -d "user=admin&pass=wrong" | wc -c
curl -s -X POST https://ejemplo.com/login -d "user=xyz&pass=wrong" | wc -c

# Usar diff para comparar respuestas completas
curl -s ... > response_admin.txt
curl -s ... > response_xyz.txt
diff response_admin.txt response_xyz.txt
```

### **5. Registro de recuperación de contraseña**

El flujo de "olvidé mi contraseña" es a menudo más revelador que el login.

**Comportamiento vulnerable:**

* Usuario existente: *"Te hemos enviado un enlace de restablecimiento"*
* Usuario inexistente: *"No encontramos una cuenta con ese email"*

**Comportamiento seguro:**

* Mensaje idéntico en ambos casos, pero internamente:
  * Si existe → envía correo
  * Si no existe → no hace nada (o envía correo genérico)

**Cómo testearlo:**\
Solicita restablecimiento para un email conocido y otro desconocido. Compara mensajes.

### **6. Registro de usuarios**

El formulario de registro puede revelar qué usuarios ya existen.

**Comportamiento vulnerable:**

* Email ya registrado: *"Este email ya está en uso"*
* Email disponible: *"Revisa tu correo para verificar tu cuenta"*

**Esto es normal** (es necesario informar que el email ya existe), pero puede ser un vector de enumeración. Para mitigarlo, algunos sistemas usan captcha o rate limiting en registro.

### **7. APIs y endpoints JSON**

Las APIs modernas (REST, GraphQL) a menudo devuelven estructuras JSON detalladas.

**Ejemplo vulnerable:**

```json
// Usuario inexistente
{
  "success": false,
  "error": "user_not_found"
}

// Usuario existente, contraseña incorrecta
{
  "success": false,
  "error": "invalid_password"
}
```

**Cómo testearlo:**\
Intercepta las peticiones de la API y observa las respuestas JSON. Busca campos `error`, `code`, `message` que varíen.

### **8. Diferencias en cabeceras HTTP**

La respuesta puede incluir cabeceras diferentes según el usuario.

* `X-RateLimit-Remaining` (puede decrementar solo para usuarios existentes)
* `X-Robots-Tag` (diferente para páginas autenticadas vs no autenticadas)
* `Set-Cookie` (puede asignar cookies diferentes)

***

## <mark style="color:$primary;">Técnicas de explotación</mark>

#### **Enumeración manual con Burp Repeater**

1. Captura una petición de login con Burp Proxy.
2. Envía a **Repeater**.
3. Modifica el parámetro `username` con diferentes valores.
4. Observa diferencias en: mensajes de error, longitud de respuesta, códigos de estado, cabeceras.

#### **Enumeración automatizada con Burp Intruder**

**Configuración:**

1. Envía la petición a **Intruder**.
2. Posición de ataque: en el parámetro `username`.
3. Payload: lista de posibles usuarios (diccionario de nombres comunes, emails, etc.).
4. Añade **Grep - Match** para identificar patrones de usuarios existentes:
   * Frases como "contraseña incorrecta", "invalid password"
   * Longitud de respuesta específica
   * Códigos de estado concretos

#### **Extra: Ataque de "escalera" (pitchfork)**

Si tienes dos listas (usuarios y contraseñas), puedes hacer un ataque de tipo **Pitchfork** donde cada usuario se prueba con su contraseña correspondiente (útil para credential stuffing).

### **Herramientas especializadas**

<table data-header-hidden><thead><tr><th width="246.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Propósito</td></tr><tr><td><strong>Burp Suite Intruder</strong></td><td>Automatización de peticiones con detección de diferencias.</td></tr><tr><td><strong>wfuzz</strong></td><td>Fuzzing de parámetros con filtrado por palabras, líneas o tiempo.</td></tr><tr><td><strong>FFuf</strong></td><td>Similar a wfuzz, muy rápido.</td></tr><tr><td><strong>Hydra</strong> (modo enumeración)</td><td>Prueba usuarios uno a uno con una contraseña fija.</td></tr><tr><td><strong>Nmap (http-enum script)</strong></td><td>Enumeración básica de recursos y usuarios.</td></tr><tr><td><strong>Python + requests</strong></td><td>Scripts personalizados para timing attacks o lógica específica.</td></tr></tbody></table>

#### **Ejemplo con FFuf**

```bash
ffuf -w users.txt -X POST -d "username=FUZZ&password=test" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -u "https://ejemplo.com/login" \
  -mr "invalid password" \
  -ac
```

* `-mr`: filtro por expresión regular (muestra solo respuestas que contienen "invalid password")
* `-ac`: calibración automática del filtrado

***

## <mark style="color:$primary;">Estrategias de mitigación (para defensores)</mark>

Estas son las prácticas que las aplicaciones seguras implementan y que tú, como tester, debes verificar.

<table data-header-hidden><thead><tr><th width="226.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Estrategia</td><td>Implementación</td></tr><tr><td><strong>Mensajes de error genéricos</strong></td><td>Usar "Credenciales inválidas" tanto para usuario inexistente como para contraseña incorrecta.</td></tr><tr><td><strong>Tiempos de respuesta uniformes</strong></td><td>Añadir retrasos artificiales (dormir random o fijo) en respuestas de login fallido para igualar tiempos.</td></tr><tr><td><strong>Rate limiting global</strong></td><td>Limitar por IP, por usuario objetivo, o por combinación (ej. 5 intentos por minuto).</td></tr><tr><td><strong>Captcha después de intentos fallidos</strong></td><td>Obliga a resolver un captcha tras varios fallos.</td></tr><tr><td><strong>No registrar intentos de usuarios inexistentes</strong></td><td>O al menos no generar respuestas diferentes.</td></tr><tr><td><strong>Ocultar diferencia en APIs</strong></td><td>En JSON, usar siempre <code>{"success": false, "message": "Invalid credentials"}</code>.</td></tr><tr><td><strong>Proteger registro y recuperación</strong></td><td>Aplicar rate limiting también en estos endpoints.</td></tr><tr><td><strong>Usar identificadores opacos</strong></td><td>No usar emails como identificadores públicos; utilizar UUIDs o tokens.</td></tr></tbody></table>

#### **Ejemplo de respuesta segura (buena práctica)**

**Login fallido (tanto usuario inexistente como contraseña incorrecta):**

```bash
HTTP/1.1 200 OK
Content-Type: text/html

<div class="error">Invalid username or password</div>
```

**Recuperación segura:**

```bash
HTTP/1.1 200 OK
Content-Type: text/html

<div class="message">If an account exists with that email, you will receive a password reset link.</div>
```

***

## <mark style="color:$primary;">Checklist - Enumeración de usuarios</mark>

<table data-header-hidden><thead><tr><th width="63.77777099609375"></th><th width="319.85186767578125"></th><th></th><th></th></tr></thead><tbody><tr><td>#</td><td>Vector de enumeración</td><td>Herramienta</td><td>Severidad</td></tr><tr><td>1</td><td>Mensajes de error diferenciales en login</td><td>Manual, Burp Repeater</td><td>Media</td></tr><tr><td>2</td><td>Diferencias en tiempos de respuesta</td><td>Script Python, Burp + plugin</td><td>Media</td></tr><tr><td>3</td><td>Códigos de estado HTTP diferentes</td><td>Burp Repeater</td><td>Media</td></tr><tr><td>4</td><td>Diferencias en longitud de respuesta (<code>Content-Length</code>)</td><td>Burp Intruder, wfuzz</td><td>Media</td></tr><tr><td>5</td><td>Mensajes de error en recuperación de contraseña</td><td>Manual</td><td>Alta (depende del contexto)</td></tr><tr><td>6</td><td>Mensajes de error en registro de usuarios</td><td>Manual</td><td>Baja (pero informativo)</td></tr><tr><td>7</td><td>APIs JSON con códigos de error diferenciales</td><td>Burp Repeater, navegación</td><td>Media</td></tr><tr><td>8</td><td>Cabeceras HTTP diferenciales</td><td>Burp Repeater</td><td>Baja</td></tr><tr><td>9</td><td>Endpoints de verificación de usuario (chequeo de disponibilidad)</td><td>Fuzzing</td><td>Alta</td></tr><tr><td>10</td><td>Gráficas de progreso (strong/weak password) al escribir email</td><td>Inspector de red</td><td>Baja</td></tr></tbody></table>

***

## <mark style="color:$primary;">Enumeración vs. otros conceptos relacionados</mark>

<table data-header-hidden><thead><tr><th width="235.96295166015625"></th><th></th></tr></thead><tbody><tr><td>Concepto</td><td>Diferencia</td></tr><tr><td><strong>Username Enumeration</strong></td><td>Determinar si un usuario existe.</td></tr><tr><td><strong>Credential Stuffing</strong></td><td>Probar pares (usuario, contraseña) de listas filtradas.</td></tr><tr><td><strong>Brute Force</strong></td><td>Probar todas las combinaciones posibles (o muchas) sobre uno o varios usuarios.</td></tr><tr><td><strong>Password Spraying</strong></td><td>Probar una contraseña común contra muchos usuarios (evita bloqueos).</td></tr><tr><td><strong>User IDOR</strong></td><td>Acceder a recursos de otros usuarios cambiando un ID numérico (es autorización, no autenticación).</td></tr></tbody></table>

***

## <mark style="color:$primary;">📊 Ejemplo práctico: Reporte de hallazgo</mark>

**Hallazgo:** Username Enumeration mediante mensajes de error diferenciales

**Severidad:** Media (CVSS 5.3)

**Descripción:** El endpoint `/login` devuelve mensajes diferentes cuando se introduce un usuario inexistente vs. una contraseña incorrecta, permitiendo enumerar usuarios válidos.

**Evidencia:**

| Petición                         | Respuesta                       |
| -------------------------------- | ------------------------------- |
| `username=admin&password=wrong`  | `{"error": "Invalid password"}` |
| `username=xyz123&password=wrong` | `{"error": "User not found"}`   |

**Impacto:** Un atacante puede enumerar todos los usuarios válidos del sistema, facilitando ataques posteriores de fuerza bruta o credential stuffing.

**Recomendación:** Modificar los mensajes de error para que sean idénticos en ambos casos, por ejemplo: `{"error": "Invalid username or password"}`. Además, implementar rate limiting en el endpoint de login.

**Referencia OWASP:** [WSTG-ATHN-02 - Testing for Default Credentials / Enumeration](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Default_Credentials)

***

## <mark style="color:$primary;">📚 Referencias OWASP WSTG</mark>

**Sección principal:** [WSTG-ATHN-02 - Testing for Default Credentials](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Default_Credentials) (La enumeración se cubre dentro de esta sección, aunque el nombre sea "default credentials". El testing guide recomienda probar enumeración antes de fuerza bruta.)

**Relacionadas:**

* [WSTG-ATHN-03 - Testing for Weak Lock Out Mechanism](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism)
* [WSTG-ATHN-04 - Testing for Bypassing Authentication Schema](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/04-Testing_for_Bypassing_Authentication_Schema)
* [OWASP Cheat Sheet: Username Enumeration](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#username-enumeration)

***

## <mark style="color:$primary;">Lab:</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**WebGoat**</mark>

{% embed url="<https://owasp.org/www-project-webgoat/>" %}

[Webgoat](https://www.owasp.org/index.php/Category:OWASP_WebGoat_Project) es una aplicación web deliberadamente vulnerable mantenida por [OWASP](https://www.owasp.org/). Está licenciada bajo [la GPLv2](https://www.gnu.org/licenses/gpl-2.0.html) .

Puedes descargar Webgoat localmente e instalarlo en una máquina virtual.

Algunos ejemplos de vulnerabilidades que incluye:

* Cross Site Scripting
* Access Control Flaw
* Buffer Overflow
* Injection Flaw
* Malicious Execution...

### User Enumeration

Lo primero nos logueamos en la aplicación con la cuenta de Admin:

<figure><img src="/files/3wPVV8gI1D15dRoUOKhS" alt=""><figcaption></figcaption></figure>

Una vez dentro tenemos todas las secciones disponibles:

<figure><img src="/files/zhcKKrEgc0nMqWeFF1Sa" alt=""><figcaption></figcaption></figure>

#### Forgot Password

<figure><img src="/files/i8ePL3WbR7OJM0D0dJHN" alt=""><figcaption></figcaption></figure>

Introducimos un usuario que no existe y vemos que da el error:

{% code overflow="wrap" %}

```
* Not a valid username. Please try again.
```

{% endcode %}

<figure><img src="/files/1PHDnFUrgQAq1QtP7zZ8" alt=""><figcaption></figcaption></figure>

Y si ponemos el usuario admin vemos que pasa a la siguiente fase:

<figure><img src="/files/DM3Tr4Hxb6MKOEIxkUzV" alt=""><figcaption></figcaption></figure>

#### Captura de request con BurpSuite

<figure><img src="/files/xcaCVdV6Hbq1Up1lPq5t" alt=""><figcaption></figcaption></figure>

Hacemos click derecho en el request > Send to Intruder

Marcamos el username como position para el ataque:

<figure><img src="/files/YC6bqYNn79qfwpZcnTYD" alt=""><figcaption></figcaption></figure>

En Payloads cargamos una lista de usuarios, por ejemplo de las Seclists

<figure><img src="/files/nRwnbm2yWGJil5FGziJK" alt=""><figcaption></figcaption></figure>

En Payload processing seleccionamos Match/replace y en el regex le ponemos el error cuando falla el usuario:

<figure><img src="/files/V0QbtR9IIN4CvQfiACp6" alt=""><figcaption></figcaption></figure>

Observamos en `Length` que el usuario admin tiene un valor distinto al resto, y es Response confirmamos que efectivamente pasa de fase, lo que indica que es un usuario válido:

<figure><img src="/files/4qj6cTQnNpPAp17k5wfo" alt=""><figcaption></figcaption></figure>
