
# Introducción

Las pruebas de aplicaciones web han dejado de ser una tarea secundaria. En un panorama donde los ataques evolucionan más rápido que las defensas, validar funcionalidades ya no es suficiente. El testing avanzado no busca confirmar que “funciona”, sino asegurar que **no se pueda romper** de formas predecibles… ni de las impredecibles.

Esta sección no es una lista de herramientas ni un manual de uso de escáneres. Es una hoja de ruta práctica para pensar como un atacante, anticipar fallos de diseño y poner a prueba los puntos ciegos que los tests tradicionales dejan sin cubrir.

***

## <mark style="color:$primary;">Qué vas a encontrar aquí</mark>

Hemos organizado el contenido en seis áreas que cubren el espectro completo del testing ofensivo aplicado a aplicaciones web modernas.

#### 0. Introducción

Un punto de partida para entender la mentalidad del testing avanzado, preparar tu entorno de laboratorio y conocer las metodologías que usaremos en el resto de capítulos.

#### 1. Authentication & Session Management Testing

La puerta de entrada a cualquier aplicación. Veremos cómo romper mecanismos de login, secuestrar sesiones, explotar tokens mal generados y probar políticas de recuperación de contraseña. No basta con que la autenticación *exista*; tiene que ser infranqueable.

#### 2. Advanced Injection Attacks

Inyección SQL, NoSQL, comandos del sistema operativo, LDAP, XPath… pero nada de ejemplos de manual. Aquí profundizamos en técnicas para sortear validaciones, explotar contextos ciegos (blind injection) y construir payloads que realmente ejecuten código o extraigan datos sin alertar a los sistemas de defensa.

#### 3. API Penetration Testing

Las APIs dirigen el tráfico de casi todas las aplicaciones modernas, y suelen estar peor protegidas que las interfaces web tradicionales. Abordaremos desde autenticación rota en REST y GraphQL hasta abusos de rate limiting, IDOR (Insecure Direct Object References) y problemas específicos de webhooks.

#### 4. Filter Evasion & WAF Bypass Techniques

Los cortafuegos de aplicación (WAF) y los filtros de entrada ayudan… hasta que alguien descubre cómo rodearlos. Esta sección enseña técnicas reales de ofuscación, fragmentación de payloads, aprovechamiento de codificaciones ambiguas y errores de parsing para que una inyección llegue intacta al backend.

#### 5. Server Side Attacks

SSRF (Server-Side Request Forgery), SSTI (Server-Side Template Injection), deserialización insegura y ataques a procesos internos. Aquí pasamos del cliente al servidor: atacamos lo que ocurre *detrás* del firewall, donde muchas veces la seguridad es más laxa.

### Cómo sacarle el máximo partido

* **No leas de forma lineal si no es necesario**: cada sección es autocontenida, aunque recomendamos empezar por Autenticación si eres nuevo en el testing avanzado.
* **Prueba mientras aprendes**: configura un laboratorio local (OWASP WebGoat, Juice Shop o tus propios contenedores) y replica los ejemplos.
* **Piensa como atacante, actúa como ingeniero**: documenta cada fallo que encuentres, entiende su causa raíz y aprende a proponer correcciones, no solo a explotar.
