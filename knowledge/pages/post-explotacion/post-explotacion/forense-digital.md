
# Forense Digital

## <mark style="color:purple;">¿Qué es el Análisis Forense Digital?</mark>

El **análisis forense digital** es una disciplina dentro de la ciberseguridad y la criminalística digital encargada de **identificar, preservar, analizar y presentar evidencia digital** de manera legalmente válida, generalmente con el fin de apoyar investigaciones internas, judiciales o incidentes de seguridad informática.

<figure><img src="/files/N5HQmqXVHXLUKd6Pklo4" alt=""><figcaption></figcaption></figure>

Se utiliza en casos de:&#x20;

* Acceso no autorizado
* Fraude electrónico
* Malware
* Abuso de sistemas
* Fuga de datos
* Espionaje corporativo
* Etc...

***

## <mark style="color:purple;">Objetivos del Análisis Forense Digital</mark>

#### **1. Preservar**

* Garantizar que los datos recolectados no sean alterados desde el momento de su adquisición.
* Usar imágenes forenses y calcular hashes (SHA256, MD5) para garantizar la autenticidad.

#### **2. Identificar**

* Localizar los dispositivos, archivos, registros o elementos que contienen evidencia relevante.
* Distinguir evidencia directa (p. ej. un archivo malicioso) de evidencia indirecta (p. ej. logs, metadatos).

#### **3. Extraer**

* Obtener la información de forma estructurada, usando técnicas no invasivas.
* Herramientas como `autopsy`, `volatility`, `sleuthkit` se usan para extraer información sin modificar el artefacto original.

#### **4. Analizar**

* Correlacionar fechas, archivos, procesos, comunicaciones o eventos sospechosos.
* Buscar patrones, indicadores de compromiso (IOCs), persistencia, rootkits, etc.

#### **5. Documentar**

* Generar informes claros, cronológicos y técnicamente detallados, que puedan sostenerse en entornos legales.
* Toda acción debe registrarse con hora, método y resultado.

***

## <mark style="color:purple;">Tipos de Análisis Forense Digita</mark>l

#### **Forense de Disco (Disk Forensics)**

* Análisis de particiones, archivos eliminados, sistemas de archivos (NTFS, ext4), metadatos, timestamps, artefactos.
* Herramientas: `Autopsy`, `FTK Imager`, `Sleuthkit`.

#### **Forense de Memoria (Memory Forensics)**

* Estudio de la RAM para detectar procesos en ejecución, conexiones, DLLs cargadas, malware en memoria.
* Herramientas: `Volatility`, `LiME`.

#### **Forense de Red (Network Forensics)**

* Análisis de tráfico de red (pcaps, logs) para detectar intrusiones, comunicaciones C2, movimientos laterales.
* Herramientas: `Wireshark`, `tcpdump`, `Zeek`.

#### **Forense Móvil (Mobile Forensics)**

* Extracción y análisis de datos en dispositivos móviles (iOS, Android): apps, mensajes, GPS, fotos.
* Herramientas: `Cellebrite`, `Magnet AXIOM`, `MobSF`.

#### **Forense de Malware (Malware Analysis)**

* Estudio de archivos maliciosos: comportamiento, persistencia, payloads, cifrado, comunicaciones.
* Herramientas: `Ghidra`, `Cuckoo Sandbox`, `REMnux`.

***

## <mark style="color:purple;">Principios Forenses Fundamentales</mark>

#### **Cadena de Custodia**

* Registro documentado de quién accedió a la evidencia, cuándo y cómo.
* Mantiene la validez legal de la prueba.
* Cada transferencia de archivos debe firmarse y validarse.

#### **Integridad**

* La evidencia debe mantenerse sin alteraciones desde su adquisición.
* Se usan hashes criptográficos (`md5sum`, `sha256sum`) para verificar.

#### **No Alteración (No Invasión)**

* El proceso de adquisición y análisis no debe modificar los datos originales.
* Se trabaja sobre copias forenses (imágenes de disco, capturas de RAM).
* Uso de sistemas de archivos de solo lectura (`mount -o ro`).

***

## <mark style="color:purple;">Ejemplos prácticos de forense digital</mark>

En las siguientes secciones veremos casos prácticos de Forense Digital aplicados a labs de la plataforma Ciberdefenders:

{% embed url="<https://cyberdefenders.org/tracks/>" %}

{% content-ref url="/pages/BGdA8PlDnChX8RkDmCpo" %}
[Análisis de Malware](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/forense-digital/analisis-de-malware.md)
{% endcontent-ref %}

{% content-ref url="/pages/AaMminD4hXXYLml03Di6" %}
[Análisis de Memoria](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/forense-digital/analisis-de-memoria.md)
{% endcontent-ref %}

{% content-ref url="/pages/gyPDd9nOCjDAKgFxiCPr" %}
[Análisis de Android](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/forense-digital/analisis-de-android.md)
{% endcontent-ref %}
