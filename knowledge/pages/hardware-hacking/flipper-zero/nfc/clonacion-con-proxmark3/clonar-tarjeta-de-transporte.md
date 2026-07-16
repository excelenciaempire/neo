
# Clonar tarjeta de transporte

<figure><img src="/files/I800hrxOVotjwwAR1nov" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:orange;">Atacando tarjeta de transporte</mark>

### Comprobación inicial

```bash
hf search
```

<figure><img src="/files/nRJUjRNmieWEF4xcQbZj" alt=""><figcaption></figcaption></figure>

Vemos que esta tarjeta de transporte es una Es una **MIFARE Plus S 1K Generation 1, mucho más segura que las tradicionales MIFARE Classic 1K.**

**MIFARE Plus** tiene tres modos de seguridad:

* **Modo 1**: Compatibilidad con Classic (débil)
* **Modo 2**: Seguridad mejorada
* **Modo 3**: Seguridad avanzada (AES)&#x20;

### Obtener más info de la tarjeta

```bash
hf mfp info
```

<figure><img src="/files/C9J2uYqpMGKnUUrnsmJJ" alt=""><figcaption></figcaption></figure>

Tenemos información crucial: **MIFARE Plus en modo SL1** (Security Level 1). Esto significa:

**SL1 = Compatibilidad con MIFARE Classic** - pero con algunas protecciones adicionales.

#### Buenas Noticias:

* ✅ Debería ser compatible con ataques MIFARE Classic

#### Malas Noticias:

* ❌ El PRNG es más seguro (por eso nested/darkside no funcionan)
* ❌ Las claves pueden ser únicas

### Comprobar claves por defecto

```bash
hf mf chk
```

<figure><img src="/files/btpszfMmugrBaCNQFKAf" alt=""><figcaption></figcaption></figure>

Vemos que no hemos conseguido extraer ninguna clave, por lo que empezaremos a intentar extraerlas con distintos ataques.

### Ataque Autopwn con default keys

```bash
hf mf autopwn -f mfc_default_keys
```

<figure><img src="/files/J4fsYHi69kF8NSuW4oAL" alt=""><figcaption></figcaption></figure>

Solamente nos ha encontrado una clave válida, pero nos sirve para encadenarlo con otros ataques.

También podríamos probar con otros diccionarios que tenemos al instalar `pm3` en la siguiente ruta:

```bash
afsh4ck@kali$ ls -la /usr/local/share/proxmark3/dictionaries/

drwxrwxr-x kali kali  4.0 KB Tue Nov 25 21:38:10 2025  .
drwxr-xr-x root root  4.0 KB Tue Nov 25 21:46:20 2025  ..
drwxrwxr-x kali kali  4.0 KB Tue Nov 25 21:38:10 2025  extras
.rw-rw-r-- kali kali  384 B  Tue Nov 25 21:38:10 2025  ht2_default.dic
.rw-rw-r-- kali kali 1003 B  Tue Nov 25 21:38:10 2025  iclass_default_keys.dic
.rw-rw-r-- kali kali   12 KB Tue Nov 25 21:38:10 2025  iclass_elite_keys.dic
.rw-rw-r-- kali kali   44 KB Tue Nov 25 21:38:10 2025  mfc_default_keys.dic
.rw-rw-r-- kali kali   13 KB Tue Nov 25 21:38:10 2025  mfc_keys_bmp_sorted.dic
.rw-rw-r-- kali kali   13 KB Tue Nov 25 21:38:10 2025  mfc_keys_icbmp_sorted.dic
.rw-rw-r-- kali kali  741 B  Tue Nov 25 21:38:10 2025  mfc_keys_mrzd_sorted.dic
.rw-rw-r-- kali kali  2.3 KB Tue Nov 25 21:38:10 2025  mfdes_default_keys.dic
.rw-rw-r-- kali kali  1.1 KB Tue Nov 25 21:38:10 2025  mfp_default_keys.dic
.rw-rw-r-- kali kali  521 B  Tue Nov 25 21:38:10 2025  mfulc_default_keys.dic
.rw-rw-r-- kali kali  2.4 KB Tue Nov 25 21:38:10 2025  t55xx_default_pwds.dic
```

### Ataque Hardnested con una clave válida

Usaremos la clave A del bloque 11 que hemos descubierto:

```bash
[usb] pm3 --> hf mf hardnested --blk 11 -a -k 749934CC8ED3
```

<figure><img src="/files/gloGjttT5IGhmixVFJWH" alt=""><figcaption></figcaption></figure>

Si el ataque Nested falla, pasamos al Hardnested

### Ataque Autopwn con dos claves válidas

```bash
hf mf autopwn -k F6E89721B60B -k 749934CC8ED3
```

<figure><img src="/files/6YXaCXeV8mIwVUf99BXh" alt=""><figcaption></figcaption></figure>

Vemos que el autopwn solo confirmó las claves que ya tenía pero no encontró nuevas. Dado que tenemos una **MIFARE Plus** (más segura), necesitamos estrategias diferentes.

### Analizar los sectores completos descubiertos

```bash
# Leer sector 0 con key A
hf mf rdsc -s 0 -k F6E89721B60B -a -v

# Leer sector 2 con key A  
hf mf rdsc -s 2 -k 749934CC8ED3 -a -v
```

<figure><img src="/files/Lkn5yi3saV9R4XVCUPye" alt=""><figcaption><p>Sector 0</p></figcaption></figure>

<figure><img src="/files/fxGeIDQda2XPbC8btt9f" alt=""><figcaption><p>Sector 2</p></figcaption></figure>

Aquí observamos lo siguiente:

#### **Sector 0**

* **Bloque 0**: Contiene UID `54 21 88 B0` + datos "AP" (posiblemente identificación de aplicación)
* **Bloque 1**: Datos con timestamp `F0 92 54 A6` + referencia "O"
* **Bloque 2**: Datos que parecen contadores o valores (`63 00 70 33`)
* **Configuración**: Key B deshabilitada, acceso de solo lectura para datos

#### **Sector 2**

* **Bloque 8**: Datos de configuración con referencia `E4 4F 03 0A`
* **Bloque 9**: Vacío (posiblemente espacio no usado)
* **Bloque 10**: Contiene valor `01 00 80 2E` (posible saldo o contador)
* **Configuración**: Idéntica al sector 0

#### **Patrones Detectados**

1. **Misma configuración de seguridad** en ambos sectores
2. **Key B deshabilitada** en ambos (patrón de seguridad débil)
3. **Bytes de acceso idénticos** (`78 77 88 69`)
4. **Estructura similar**: 3 bloques de datos + 1 bloque de control

#### **Posible Uso**

* **Sector 0**: Datos maestros/identificación
* **Sector 2**: Datos transaccionales o de aplicación específica
* Podría ser un sistema de control de acceso o pago

Los datos recuperados son limitados pero muestran una estructura consistente, aunque la mayoría de la tarjeta permanece segura.

***

## <mark style="color:orange;">Resumen Final de la Auditoría</mark>

### **Resultados Obtenidos**

#### **✅ Sectores Recuperados:**

* **Sector 0**: Clave A = `F6E89721B60B`
* **Sector 2**: Clave A = `749934CC8ED3`

#### **🔍 Análisis de Seguridad:**

* **MIFARE Plus S 1K** en modo SL1 (compatibilidad Classic)
* **Mismo patrón de acceso** en ambos sectores: `78 77 88 69`
* **Key B deshabilitada** en ambos sectores (`000000000000`)
* **Configuración de acceso consistente** pero segura

#### **📈 Efectividad del Ataque:**

* **12.5% de la tarjeta** comprometida (2 de 16 sectores)
* **87.5% permanece seguro** (14 sectores no recuperables)

### **Evaluación de Seguridad**

#### **Puntos Fuertes de la Tarjeta**

* MIFARE Plus con PRNG mejorado
* Claves únicas no en diccionarios
* Prevención de ataques nested/darkside

#### **Puntos Débiles Identificados**

* 2 sectores con claves recuperables
* Key B deshabilitada (configuración común pero riesgosa)
* Mismo patrón de bytes de acceso

### **Recomendaciones**

#### **Para el propietario de la tarjeta**

* Considerar reemplazar por MIFARE Plus en modo SL3 (AES)
* Rotar claves periódicamente
* Usar Key B con claves fuertes

#### **Para el auditor**

* La tarjeta tiene buena resistencia contra ataques estándar
* Los sectores recuperados podrían contener información útil
* Considerar ataques side-channel para sectores restantes

***
