
# Web Application Security Testing

Las “pruebas de seguridad” a menudo se confunden con las pruebas de penetración, pero son un concepto más amplio. Incluye cualquier actividad que tenga como objetivo descubrir debilidades de seguridad en una aplicación web, sin importar el nivel de automatización o el momento del ciclo de vida.

## <mark style="color:$primary;">Tipos de pruebas de seguridad según el enfoque</mark>

### **SAST (Static Application Security Testing)**

* **Qué es:** Análisis del código fuente en busca de patrones inseguros.
* **Cuándo se hace:** Durante el desarrollo, integrado en el IDE o pipeline CI/CD.
* **Ventaja:** Encuentra problemas muy temprano.
* **Desventaja:** Falsos positivos, no detecta fallos de configuración del entorno.
* **Herramientas:** SonarQube, Checkmarx, Semgrep, CodeQL.

### **DAST (Dynamic Application Security Testing)**

* **Qué es:** Prueba la aplicación en ejecución, enviando peticiones maliciosas y analizando respuestas.
* **Cuándo se hace:** En entornos de staging o producción (con cuidado).
* **Ventaja:** No necesita acceso al código, simula un atacante externo.
* **Desventaja:** No cubre lógicas profundas ni rutas poco exploradas.
* **Herramientas:** OWASP ZAP, Burp Suite Professional, Nikto, w3af.

### **IAST (Interactive Application Security Testing)**

* **Qué es:** Híbrido: sensores dentro de la aplicación mientras se ejecutan pruebas funcionales o DAST.
* **Ventaja:** Muy alta precisión, bajo ruido.
* **Desventaja:** Requiere instrumentación del entorno (agentes Java/.NET).
* **Herramientas:** Contrast Security, Seeker.

### **RASP (Runtime Application Self-Protection)**

* **Qué es:** No es una prueba sino una defensa, pero se incluye en el ecosistema: protege la aplicación en tiempo real detectando y bloqueando ataques.
* **Ejemplo:** Un agente que detecta una inyección SQL y la rechaza antes de que llegue a la base de datos.

## Pruebas manuales vs automatizadas

<table data-header-hidden><thead><tr><th width="371.96295166015625"></th><th></th><th></th></tr></thead><tbody><tr><td>Característica</td><td>Automatizado</td><td>Manual</td></tr><tr><td>Rapidez en pruebas repetitivas</td><td>Excelente</td><td>Lento</td></tr><tr><td>Detección de fallos lógicos o de negocio</td><td>Muy malo</td><td>Excelente</td></tr><tr><td>Capacidad de encadenar vulnerabilidades</td><td>Limitada</td><td>Alta</td></tr><tr><td>Escalabilidad (miles de endpoints)</td><td>Alta</td><td>Baja</td></tr><tr><td>Falsos positivos</td><td>Altos</td><td>Casi nulos</td></tr></tbody></table>

**Conclusión práctica:** La mejor estrategia es usar automatización para cubrir el terreno (escaneo de directorios, parámetros, inyecciones básicas) y luego invertir tiempo en pruebas manuales dirigidas por el conocimiento de la aplicación.

## <mark style="color:$primary;">Flujo de pruebas de seguridad en el SDLC</mark>

1. **Requisitos:** Definir posturas de seguridad (por ejemplo, “todos los endpoints críticos deben tener logs”).
2. **Diseño:** Revisión de arquitectura (threat modeling).
3. **Desarrollo:** SAST en cada commit, análisis de dependencias.
4. **Pruebas:** DAST en entorno de integración; pruebas de penetración periódicas.
5. **Producción:** Monitoreo continuo, RASP, bug bounty opcional.

## <mark style="color:$primary;">Herramientas esenciales para pentesting web</mark>

No necesitas cien herramientas, sino dominar unas pocas:

* **Proxy interceptors:** Burp Suite Community o ZAP (para manipular peticiones).
* **Fuzzing:** ffuf, wfuzz, o el intruder de Burp (categorías).
* **Detección de vulnerabilidades:** nuclei (plantillas), nikto (rápido).
* **Inyección SQL:** sqlmap (con cuidado, sin modo automático agresivo).
* **Escaneo de dependencias:** OWASP Dependency-Check, Snyk.
* **Automatización de pruebas de seguridad API:** Postman + Newman con colecciones de seguridad, o ZAP en modo headless.

## <mark style="color:$primary;">Buenas prácticas profesionales</mark>

* **Documenta todo el alcance y las reglas de enfrentamiento (RoE):** qué IPs, qué métodos, horarios.
* **Usa entornos aislados siempre que sea posible.** Si pruebas en producción, coordina ventanas de bajo tráfico.
* **Mantén un registro de acciones (logbook):** cada petición inusual, cada payload. Puede servir como evidencia legal.
* **Nunca explotes una vulnerabilidad más allá de la prueba de concepto** sin autorización expresa.
* **Verifica dos veces antes de ejecutar comandos destructivos** (DROP TABLE, rm -rf, etc.).
