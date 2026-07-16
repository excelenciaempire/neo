
# Modos de Red

## <mark style="color:purple;">Modos de Red</mark>

<table><thead><tr><th width="142">Modo de red</th><th>Descripción</th><th>Conectividad</th><th>Ventajas</th><th>Limitaciones</th></tr></thead><tbody><tr><td><strong>NAT</strong></td><td>La máquina virtual usa la IP del host para acceder a Internet mediante traducción de direcciones (NAT)</td><td>Puede acceder a Internet a través del host, pero no es directamente accesible desde la red externa</td><td>Fácil de configurar y segura para conexiones salientes</td><td>No permite el acceso directo desde dispositivos externos</td></tr><tr><td><strong>Bridge</strong></td><td>La máquina virtual se conecta como si fuera otro dispositivo en la misma red que el host</td><td>Puede comunicarse con cualquier dispositivo en la misma red, incluida la red externa e Internet</td><td>Acceso completo a la red local y permite conexiones directas</td><td>Depende de la configuración de la red física</td></tr><tr><td><strong>Host-Only</strong></td><td>La máquina virtual solo se comunica con el host y otras VM configuradas en modo host-only</td><td>Solo permite comunicación entre el host y otras VM en la misma red virtual</td><td>Aislada de la red externa; útil para redes de prueba</td><td>No tiene acceso a Internet u otros dispositivos externos</td></tr></tbody></table>

## <mark style="color:purple;">¿Cuando usar cada modo de red?</mark>

En **ejercicios de hacking ético**, el uso de diferentes modos de red en máquinas virtuales (como Kali Linux) depende del tipo de pruebas que se estén realizando y el nivel de aislamiento y conectividad que se requiera. Aquí te doy un resumen de cuándo usar cada modo de red:

### 1. **Modo NAT** (Network Address Translation)

* **Cuándo usarlo:**
  * Cuando necesitas que la máquina virtual (VM) tenga acceso a **Internet** para realizar descargas de herramientas, actualizaciones, o acceder a servicios externos, pero **sin exponer** la VM directamente a la red local o a otras redes.
  * Ideal para **entornos de prueba** donde la VM necesita interactuar con el mundo exterior, pero no deseas que sea accesible desde otras máquinas o redes.
* **Ejemplo de uso:**
  * Si estás realizando un ejercicio de **reconocimiento** o **scanning** donde la máquina virtual necesita acceder a repositorios en línea (por ejemplo, para obtener herramientas o parches), pero no quieres que sea accesible desde fuera de la VM.

### 2. **Modo Bridge** (Puente)

* **Cuándo usarlo:**
  * Cuando necesitas que la VM esté en la **misma red que el host**, como si fuera una máquina física más, con su propia dirección IP.
  * Es útil cuando deseas que tu **VM sea accesible desde otras máquinas en la red** o cuando la VM necesita interactuar directamente con otros dispositivos en la red local o incluso **realizar pruebas de penetración** en dispositivos externos.
* **Ejemplo de uso:**
  * Durante un ejercicio de **penetración externa** o pruebas de **explotación de vulnerabilidades** en una red interna o red local, donde tu máquina virtual necesita comunicarse directamente con otros sistemas, como **escaneo de puertos** o ataques como **SQL Injection** a sistemas dentro de la misma red.

### 3. **Modo Host-Only**

* **Cuándo usarlo:**
  * Cuando deseas **aislar completamente la VM de la red externa** (sin acceso a Internet o a otras redes), pero permitir la **comunicación con el host y otras VMs** en el mismo entorno.
  * Ideal para **entornos controlados** donde se simulan ataques de **hacking interno** o **pruebas de seguridad** en un entorno aislado, como una **Red de Prueba** o un **entorno CTF (Capture the Flag)**.
* **Ejemplo de uso:**
  * Si estás realizando ejercicios de **explotación interna**, como **movimiento lateral** o pruebas de **Kerberoasting**, donde la VM necesita comunicarse solo con el host o con otras VMs, pero no debe tener acceso a redes externas por razones de seguridad o de control del entorno.
