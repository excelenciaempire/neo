
# MIFARE Classic 1K

<figure><img src="/files/vXNkjTyi8mGxO4Nfcz1s" alt=""><figcaption></figcaption></figure>

#### Blog interesante: Hacking tarjetas NFC MiFare Classic

{% embed url="<https://www.elladodelmal.com/2023/01/hacking-de-tarjetas-nfc-mifare-classic.html>" %}

## <mark style="color:orange;">Hacking NFC: Introducción a las MIFARE Classic 1K</mark>&#x20;

Las tarjetas **NFC** están por todas partes: acceso a edificios, transporte, máquinas de vending o pagos móviles. Entre ellas, una de las más comunes —y más vulnerables— es la **MIFARE Classic 1K**, protagonista de sección.

Antes de entrar en materia, recuerda que el NFC opera en **13.56 MHz**, una frecuencia libre que no necesita licencia. No destaca por mover grandes cantidades de datos, sino por su **velocidad**, **simplicidad** y **comodidad**.

***

### ¿Cómo funciona NFC?

Existen dos modos:

* **Activo**: un dispositivo genera el campo electromagnético.
* **Pasivo**: el otro aprovecha ese campo para encenderse y responder.

Esto permite que una simple tarjeta opere sin batería.

***

### ¿Qué es exactamente una MIFARE Classic 1K?

Es una tarjeta con **1 KB de memoria EEPROM**, de los cuales **768 bytes** están disponibles para datos. Su estructura se divide en:

* **16 sectores**
* Cada uno con **4 bloques** de **16 bytes**

<figure><img src="/files/L0oNP0sZJF3Abi76wJ3Y" alt=""><figcaption></figcaption></figure>

El **primer bloque del sector 0** contiene el ID del fabricante, teóricamente de solo lectura (aunque algunas tarjetas chinas permiten escribirlo una vez → útil para clonar totalmente una tarjeta).

Los otros 3 bloques por sector contienen:

* **Datos**
* **Un bloque especial llamado “trailer”**, donde se almacenan:
  * **Clave A**
  * **Clave B**
  * **Bytes de acceso**

Estas claves determinan qué puede hacerse en ese sector: leer, escribir, incrementar, etc.

***

### Las claves: la primera barrera (que suele ser débil)

En muchos lugares de Internet explican cómo “hackear” estas tarjetas mostrando comandos y nada más. Pero lo cierto es que la clave está en **entender cómo funcionan**.

Lo primero: muchas tarjetas siguen usando claves **por defecto**:\
`FFFFFFFFFFFF`, `000000000000`, etc.

Por eso un simple ataque de diccionario suele funcionar rápido.

¿Pero qué ocurre si las claves han sido cambiadas? Aquí entra en juego el verdadero hacking: analizar cómo se generan, cómo se almacenan y qué debilidades tiene el sistema.

De hecho, existe un paper extraordinario donde se desmonta físicamente la tarjeta, capa por capa, hasta entender su lógica interna. Ingeniería inversa a nivel de micras.

***

### Los bytes de acceso: la lógica que controla cada bloque

Los **bytes de acceso** definen qué se puede hacer en cada bloque: leer, escribir, modificar valores…

Estos permisos se codifican mediante **tres bits: C1, C2 y C3**, almacenados tanto en forma normal como invertida dentro del trailer. Aunque parece complejo, solo importan los bytes 6, 7 y 8 del trailer.

<figure><img src="/files/8WIBkeoIjhcrMH7HCFPh" alt=""><figcaption></figcaption></figure>

Cada conjunto de bits determina los permisos en:

* **Bloques de datos (0, 1 y 2)**
* **El trailer (bloque 3)**

Con estos bits podemos saber:

* Con qué clave se puede leer
* Con qué clave se puede escribir
* Si se permite incrementar/decrementar valores
* Si el bloque es totalmente restrictivo

Aquí tenéis un recurso *online* que os ayudará a calcular los *bytes* de acceso para unos permisos concretos.&#x20;

{% embed url="<http://calc.gmss.ru/Mifare1k/>" %}
