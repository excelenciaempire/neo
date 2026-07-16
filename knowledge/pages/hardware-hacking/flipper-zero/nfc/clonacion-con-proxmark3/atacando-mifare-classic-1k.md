
# Atacando MIFARE Classic 1K

<figure><img src="/files/vXNkjTyi8mGxO4Nfcz1s" alt=""><figcaption></figcaption></figure>

### La comunicación: ISO 14443 y cifrado CRYPTO1

Las MIFARE Classic siguen, en su mayor parte, el estándar **ISO 14443** para la comunicación entre el lector y la tarjeta. El flujo básico es:

1. El lector selecciona la tarjeta.
2. Se realiza un proceso de **autenticación**.
3. A partir de ahí, toda la comunicación va **cifrada**.

Ese cifrado se hace con el algoritmo propietario **CRYPTO1**, de **NXP Semiconductors**. El problema:

* Usa **claves de 48 bits**, lo que permite ataques de fuerza bruta razonables.
* El **generador de números pseudoaleatorios (PRNG)** es predecible.

Gracias a la ingeniería inversa de **Nohl y Plotz**, hoy conocemos el funcionamiento interno de CRYPTO1 y de su PRNG. Eso abrió la puerta a todo lo que viene ahora.

***

### El PRNG: cuando el “azar” ya no es tan azar

La tarjeta genera un número aleatorio (**nonce, Nt**) que se usa en la autenticación. Ese número se obtiene de un **LFSR (Linear Feedback Shift Register)** dentro del PRNG.

Problema:\
El resultado *no* es realmente aleatorio, sino que depende del número de ciclos de reloj desde que la tarjeta fue activada por el lector. Eso hace que el PRNG sea **predecible** y, por tanto, explotable.

***

## <mark style="color:orange;">Tipos de ataques a MIFARE Classic</mark>

A nivel práctico, podemos agrupar los ataques en dos grandes familias:

1. **Ataques con lector y tarjeta válidos (sniffing)**\
   Capturamos la comunicación entre un lector legítimo y una tarjeta real (o un emulador, por ejemplo con una **Proxmark3**).\
   Con esa conversación challenge–response podemos recuperar las **claves de los sectores implicados** (por ejemplo, del sector 9 si solo se usa ese).
2. **Ataques usando únicamente una tarjeta válida**\
   No tenemos acceso al lector, solo a una tarjeta que sabemos que funciona.\
   Aquí entran los ataques clásicos: **Nested, Hardnested, DarkSide y variantes para “fixed nonce”**.

Vamos a verlos uno a uno.

***

### 1️⃣ Nested Attack

Es el ataque típico de partida.

👉 **Requisito:** conocer al menos **una clave válida** de algún sector (porque es por defecto, porque la hemos sacado con diccionario, etc.).

#### Flujo del ataque

1. Nos autenticamos en un sector usando una clave que sí conocemos.
2. Durante la autenticación, la tarjeta nos envía un **nonce Nt**.
3. Cerramos el proceso correctamente (porque la clave es válida).
4. Volvemos a autenticarnos en el mismo sector y obtenemos **otro Nt**.
5. Comparando esos nonces y el estado del LFSR, podemos deducir el **keystream**.
6. A partir de ahí, es posible ir obteniendo las **claves de otros sectores**.

Este ataque explota lo predecible del PRNG y el hecho de que, una vez dentro, la lógica de cifrado es reutilizable.

***

### 2️⃣ Hardnested Attack

Es el “hermano mayor” del Nested, pensado para cuando el PRNG está **parcheado** y el ataque Nested ya no funciona tan fácil.

👉 **Idea básica:**\
En lugar de depender de dos nonces cercanos, recopilamos **miles de nonces** (del orden de 2.000–4.000) autenticándonos repetidamente en un sector cuya clave sí conocemos.

Con todos esos datos:

* Podemos hacer un **ataque de fuerza bruta offline** sobre la clave del sector.
* El tiempo de cómputo es mayor, pero sigue siendo viable.

Se llama “Hardnested” precisamente porque es una versión más dura, pero conceptualmente sigue aprovechando problemas del diseño del cifrado.

***

### 3️⃣ DarkSide Attack

Este ataque es más sutil. En lugar de explotar el PRNG, explota **cómo responde la tarjeta a errores durante la autenticación**.

Durante la autenticación, el lector envía dos valores importantes: **Nr** y **Ar**.\
La tarjeta:

1. Comprueba primero los **bits de paridad**.
   * Si hay algún error → deja de responder.
2. Si las paridades son correctas, comprueba **Ar**.
   * Si Ar es incorrecto → responde con un **NACK cifrado** (`0x5` en 4 bits).

La clave está aquí:

Si el lector hace un **XOR** entre ese NACK en texto claro (`0x5`) y su versión cifrada, puede recuperar el **keystream**.\
Desde ese keystream se puede llegar a la **clave**, y con la clave → al sector.

DarkSide aprovecha, en esencia, que la tarjeta da *demasiada* información incluso cuando algo va mal.

***

### 4️⃣ Fixed Nonce (Static Nested)

Existe un tipo de tarjetas que, ante las vulnerabilidades anteriormente descritas, siempre envían el mismo nonce *Nt*, por lo que ya no es posible llevar a cabo estos ataques.&#x20;

Sin embargo, como veremos a continuación, en el [Github del RRG (Rfid Research Group)](https://github.com/RfidResearchGroup/proxmark3#proxmark3-rdv4) se hicieron eco de este tipo de tarjetas y buscaron una solución.&#x20;

***

## <mark style="color:orange;">Probando los ataques</mark>

Todo esto no se queda en teoría: Los ataques están implementados en herramientas reales que podemos usar, por ejemplo, desde **Kali Linux**.

#### 🧰 Con Proxmark3 (RRG firmware)

Con una **Proxmark3** y el firmware del **RRG** puedes:

* Sniffear comunicación entre tarjeta y lector.
* Lanzar ataques Nested, Hardnested y variantes para fixed nonce.
* Trabajar con tarjetas problemáticas o poco documentadas.

#### 🧰 Con herramientas en Kali Linux

Además, tenemos herramientas específicas:

* **MFOC** → Ataque Nested a MIFARE Classic
* **MFOC-Hardnested** → Variante Hardnested
* **MFCUK** → Implementa el ataque **DarkSide**

{% hint style="danger" %}
MFOC pertenece a las herramientas antiguas para MIFARE Classic, y requiere un lector como:

* ACR122U
* ACR1252
* ChameleonTiny cuando se usa como reader
* PN532
* Similar compatible con libnfc

Estos lectores usan el driver PC/SC o libnfc, **no funcionan con Proxmark**.
{% endhint %}

#### 🔁 Flujo típico de ataque

El flujo habitual sería:

1. **Probar MFOC (Nested)**

```bash
mfoc -O dump.dmp
```

<figure><img src="/files/GnMmKef7UhqXNTX5Got8" alt=""><figcaption></figcaption></figure>

* Intenta encontrar claves por defecto.
* Si encuentra una, lanza el ataque Nested y obtiene el resto.
* Al final, hace un **volcado completo** (`dump.dmp`) con todos los datos de la tarjeta.

<figure><img src="/files/62FhgrHTbouUdNy3h2is" alt=""><figcaption><p>Dumpeo completo de MIFARE Classic 1K</p></figcaption></figure>

2. **Si MFOC no encuentra nada**, probamos **DarkSide con MFCUK** contra un sector concreto.

* Si con DarkSide conseguimos una clave, la volvemos a usar con **MFOC** para recuperar el resto.

3. **Si el PRNG está parcheado y nada de eso funciona**, probamos **Hardnested con MFOC-Hardnested**, siempre que conozcamos **al menos una clave**.

* Si ninguna clave está por defecto, podemos generar diccionarios e ir probando.

4. **Si tampoco funciona porque el nonce es fijo**, usamos las herramientas específicas del **RRG para Proxmark** diseñadas para tarjetas con **“fixed nonce”**.

Al final del proceso ideal, obtenemos:

* **Todas las claves A y B de todos los sectores**
* Un **dump completo** de la tarjeta MIFARE Classic 1K, listo para analizar, clonar o emular.

***

### 🚀 ¿Y ahora qué?

En esta segunda parte hemos visto:

* Cómo se cifra la comunicación MIFARE (CRYPTO1 + PRNG débil).
* Qué tipos de ataques existen.
* Cómo se apoyan en vulnerabilidades concretas del diseño.
* Qué herramientas usar y en qué orden.

En la siguiente parte toca hacer algo todavía más jugoso: **jugar con esos dumps, clonar tarjetas, probar PoCs y ver por qué usar MIFARE Classic 1K para pagos o control de acceso serio es una muy, muy mala idea.**
