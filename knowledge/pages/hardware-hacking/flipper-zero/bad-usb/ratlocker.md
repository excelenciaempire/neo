
# RatLocker

{% hint style="warning" %}
Aunque Ratlocker es una broma diseñada para educar o entretener, es importante usarlo de manera ética y responsable. No lo emplees sin el consentimiento explícito del usuario, ya que podría interpretarse como un comportamiento malicioso.
{% endhint %}

## <mark style="color:orange;">Ratlocker: Simulador de "Malware" (.ratl0ck3r)</mark>

El **Ratlocker** es un payload de broma creado por **ratcode404** (disponible en ratcode404.github.io). Este script genera un falso "malware" que simula bloquear archivos y establecer un fondo de pantalla, pero permite una fácil recuperación sin pérdida de datos ni configuraciones importantes.

Esta herramienta se encuentra en este repositorio en /`prank/win/RatLocker`:

{% embed url="<https://github.com/FalsePhilosopher/badusb/tree/main>" %}

<figure><img src="/files/VYxlbb7m91xIJPAB5fvr" alt=""><figcaption><p>Fondo de escritorio de la víctima</p></figcaption></figure>

<figure><img src="/files/g5gujELUDg8wQ0r8Xtuc" alt=""><figcaption><p>Archivos "cifrados" con RatLocker</p></figcaption></figure>

***

## <mark style="color:orange;">**Características del Ratlocker**</mark>

#### **1. Simulación de Cifrado de Archivos**:

* Agrega la extensión `.ratl0ck3r` a los archivos ubicados en `$HOME/Desktop` para simular un cifrado.
* Los archivos no se dañan ni pierden contenido; la recuperación es instantánea al eliminar la extensión.

#### **2. Fondo de Pantalla Personalizado**:

* Cambia el fondo de pantalla del usuario sin descargar imágenes ni utilizar URLs.
* La imagen original se guarda como respaldo en la ruta:

```bash
$HOME/Pictures/wallpaper.ratl0ck3r
```

* Esto asegura que no se pierdan fondos importantes, como fotos familiares.

#### **3. Rápido y "eficiente"**:

* Todo el proceso se ejecuta en menos de **7.5 segundos**.
* Puede usarse para educar o molestar a personas que dejan dispositivos sin bloquear.

***

## <mark style="color:orange;">**Requisitos**</mark>

* Sistema operativo: Windows (7/8/8.1/10)
* Dispositivo desbloqueado
* Sin necesidad de conexión a internet

***

## <mark style="color:orange;">**Proceso de Recuperación**</mark>

La recuperación de archivos afectados por **Ratlocker** es sencilla y no requiere claves ni herramientas adicionales.

#### **1. Eliminar la Extensión `.ratl0ck3r`**:

Cada archivo tiene la extensión `.ratl0ck3r` agregada. Simplemente quita esta extensión para restaurar el archivo al estado original.

Ejemplo de recuperación manual:

* Archivo afectado: `documento.pdf.ratl0ck3r`.
* Renómbralo a: `documento.pdf`.

#### **2. Restaurar el Fondo de Pantalla**:

El fondo original se encuentra en:

```bash
$HOME/Pictures/wallpaper.ratl0ck3r
```

Cambia la extensión del archivo guardado (por ejemplo, `.ratl0ck3r` a `.jpg`) y configúralo nuevamente como fondo de pantalla.

#### **3. Automatización de la Recuperación**:

Usa el siguiente comando de PowerShell para restaurar rápidamente todos los archivos:

```powershell
dir $HOME\Desktop\* | Rename-Item -NewName { $_.name.substring(0,$_.name.length-10) }Este comando elimina la extensión .ratl0ck3r de todos los archivos afectados en el escritorio.
```

#### **4. Script de Recuperación Rápida**:

El archivo `rat3ncrypt3er.bat` ejecuta automáticamente el comando de recuperación y restaura el fondo de pantalla guardado en `$HOME/Pictures/` a su estado original.

***

## <mark style="color:orange;">**Por qué usar Ratlocker**</mark>

#### **1. Autonomía Total**:

No necesita conexión a internet ni depender de imágenes externas. Todo el contenido se genera directamente con herramientas de línea de comandos de Windows.

#### **2. Fácil Recuperación**:

Garantiza que todos los archivos y configuraciones sean restaurables en cuestión de segundos.

#### **3. Robustez**:

Ha sido probado repetidamente sin causar errores ni pérdidas accidentales.

#### **4. Simplicidad y Rapidez**:

La ejecución completa del script toma menos de 7.5 segundos.
