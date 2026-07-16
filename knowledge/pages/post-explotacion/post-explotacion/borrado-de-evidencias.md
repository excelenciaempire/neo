
# Borrado de evidencias

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir acceso a un sistema y eliminar archivos que nos incriminen, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Objetivo</mark>

Una vez completadas las pruebas, debemos realizar cualquier limpieza necesaria, como eliminar herramientas/scripts cargados en los sistemas de destino, revertir cualquier cambio de configuración (menor) que hayamos realizado, etc.&#x20;

Deberíamos tener notas detalladas de todas nuestras actividades, haciendo cualquier actividad de limpieza fácil y eficiente. Si no podemos acceder a un sistema donde es necesario eliminar un artefacto o revertir otro cambio, debemos alertar al cliente y enumerar estos problemas en los apéndices del informe.&#x20;

Incluso si podemos eliminar cualquier archivo cargado y revertir los cambios (como agregar una cuenta de administrador local), debemos documentar estos cambios en los apéndices de nuestro informe en caso de que el cliente reciba alertas de que necesita realizar un seguimiento y confirmar que la actividad en cuestión fue parte de nuestras pruebas autorizadas.

A continuación se presentan algunos archivos relevantes que deben considerarse para eliminar después de la realización del ejercicio de Hacking Ético en Linux o Windows.

## <mark style="color:purple;">1. Borrado de Evidencias en Linux</mark>

Linux almacena un amplio registro de actividades de usuario, conexiones, historial de comandos y logs del sistema que pueden ser utilizados para identificar una intrusión o cambios en el sistema. Los principales archivos y directorios que contienen información relevante para un atacante incluyen los logs del sistema, el historial de comandos, las conexiones SSH, el historial de clientes FTP, y los logs de servidores de aplicaciones.

### **Principales Archivos de Log en Linux**

Los sistemas Linux almacenan eventos y errores en varios archivos de log en el sistema, mayormente en el directorio `/var/log`. Esos archivos pueden rastrear desde accesos y autenticaciones hasta mensajes del kernel. Algunos archivos de log críticos incluyen:

<table><thead><tr><th width="239">Archivo</th><th>Descripción</th></tr></thead><tbody><tr><td><code>/var/log/auth.log</code> (o <code>/var/log/secure</code>)</td><td>Registros de autenticación, que contienen intentos de login y de sudo.</td></tr><tr><td><code>/var/log/syslog</code></td><td>Log del sistema que almacena eventos generales de varias aplicaciones.</td></tr><tr><td><code>/var/log/messages</code></td><td>Contiene mensajes globales y eventos del sistema.</td></tr><tr><td><code>/var/log/lastlog</code></td><td>Registro del último login de cada usuario.</td></tr><tr><td><code>/var/log/btmp</code></td><td>Contiene intentos de login fallidos, utilizado con el comando <code>lastb</code>.</td></tr><tr><td><code>/var/log/wtmp</code></td><td>Registros de inicio y cierre de sesión de los usuarios, consultado con <code>last</code>.</td></tr><tr><td><code>/var/log/dmesg</code></td><td>Mensajes del kernel, registrados en el proceso de arranque y durante eventos de hardware.</td></tr></tbody></table>

### **Archivos de Historial de Comandos y Conexiones**

Los historiales de comandos y conexiones pueden ser clave para un atacante, ya que contienen detalles sobre actividades anteriores del usuario y accesos remotos.

<table><thead><tr><th width="242">Archivo</th><th>Descripción</th></tr></thead><tbody><tr><td><code>~/.bash_history</code></td><td>Contiene el historial de comandos ejecutados en Bash.</td></tr><tr><td><code>~/.sh_history</code></td><td>Historial de comandos en el shell Bourne (<code>sh</code>).</td></tr><tr><td><code>~/.history</code></td><td>Otro archivo de historial de comandos, a veces compartido entre distintos shells.</td></tr><tr><td><code>~/.lesshst</code></td><td>Historial de búsquedas y navegación en el comando <code>less</code>.</td></tr><tr><td><code>~/.lftp/rl_history</code></td><td>Historial de comandos utilizados en el cliente de FTP <code>lftp</code>.</td></tr><tr><td><code>~/.lftp/cwd_history</code></td><td>Historial de directorios visitados en <code>lftp</code>.</td></tr><tr><td><code>~/.ncftp/history</code></td><td>Historial de conexiones y comandos en el cliente FTP <code>ncftp</code>.</td></tr><tr><td><code>~/.ssh/known_hosts</code></td><td>Lista de equipos a los que el usuario se ha conectado vía SSH; útil para rastrear conexiones.</td></tr></tbody></table>

### **Logs del Servidor de Aplicación**

En sistemas Linux, los logs de servidores web como Apache se almacenan en diferentes ubicaciones, dependiendo de la configuración y de la distribución de Linux. Estos archivos contienen registros de accesos, errores y otros eventos importantes de aplicaciones web.

<table><thead><tr><th width="281">Directorio</th><th>Descripción</th></tr></thead><tbody><tr><td><code>/apache/logs/</code></td><td>Carpeta de logs por defecto de Apache, común en instalaciones personalizadas.</td></tr><tr><td><code>/etc/httpd/logs/</code></td><td>Carpeta de logs de Apache en algunas distribuciones Linux, como CentOS.</td></tr><tr><td><code>/var/www/logs/</code></td><td>Logs de servidores web; en algunos sistemas se encuentran aquí los registros de acceso.</td></tr><tr><td><code>/var/log/</code></td><td>Carpeta principal de logs del sistema, contiene varios archivos de log incluyendo Apache.</td></tr><tr><td><code>/usr/local/apache/logs/</code></td><td>Carpeta de logs para instalaciones de Apache en <code>/usr/local</code>.</td></tr><tr><td><code>/var/log/apache/</code></td><td>Ubicación de logs de Apache, especialmente en configuraciones antiguas o personalizadas.</td></tr><tr><td><code>/var/log/apache2/</code></td><td>Ubicación de logs para Apache2, común en sistemas modernos como Ubuntu.</td></tr></tbody></table>

### **Comandos para Borrar Evidencias en Linux**

Para borrar o limpiar archivos que contienen rastros de actividades en Linux, los siguientes comandos pueden ser usados. Cada uno de ellos cumple una función específica y, en conjunto, pueden ayudar a borrar la mayoría de las trazas en un sistema Linux.

#### **Borrado de logs**:&#x20;

Para eliminar o vaciar archivos de log sin borrar el archivo en sí (lo cual podría levantar sospechas):

```bash
cat /dev/null > /var/log/auth.log  # Vacía el archivo auth.log
```

O, para borrar el archivo directamente:

```bash
rm /var/log/auth.log
```

#### **Historial de comandos**:&#x20;

Los historiales de comandos pueden limpiarse usando el siguiente comando en Bash, que borra tanto el historial en el archivo como en la sesión actual:

```bash
~/.bash_history && history -c
```

#### **Archivos temporales**:&#x20;

Los archivos en `/tmp` y `/var/tmp` pueden ser eliminados con `rm -rf` para limpiar archivos temporales del sistema:

```bash
rm -rf /tmp/* /var/tmp/*
```

#### **Borrado seguro de archivos**:&#x20;

Para eliminar archivos de manera que no puedan recuperarse, los comandos `shred` y `wipe` son útiles ya que sobrescriben el archivo varias veces antes de borrarlo:

```bash
shred -u /var/log/auth.log  # Sobrescribe y elimina auth.log de manera segura
```

### Herramientas para borrar evidencias en Linux

#### Shred&#x20;

Nos permite borrar contenido de archivos

```sh
shred -vfz test.txt
```

#### SRM

```sh
srm test.txt
```

***

## <mark style="color:purple;">2. Borrado de evidencias en Windows</mark>

Windows guarda un registro exhaustivo de actividades del sistema, eventos de usuario, logs de seguridad y temporales. Estas evidencias son útiles en la detección de incidentes y, por tanto, representan un objetivo para los atacantes que buscan ocultar sus rastros. A continuación, se detalla cómo identificar y manipular estos registros en el contexto de hacking ético.

A continuación encontrarás un poster de SANS DFIR con los principales archivos y directorios que deberíamos limpiar en sistemas Windows después de una auditoría:

{% embed url="<https://cyber-ssct.com/SANS%20Digital%20Forensic%20Poster.pdf>" %}
Poster Forensic SANS
{% endembed %}

<figure><img src="/files/BarnKm1rCZq4eT0BW9Cc" alt=""><figcaption><p>Poster Forensic SANS</p></figcaption></figure>

### **Principales Archivos de Log en Windows**

En Windows, la mayoría de los eventos del sistema se registran en el Visor de Eventos (Event Viewer), organizados en varias categorías de logs. A continuación, los más relevantes:

<table><thead><tr><th width="192">Log</th><th>Descripción</th></tr></thead><tbody><tr><td><strong>Security</strong></td><td>Registra eventos de seguridad como inicios de sesión, intentos de autenticación y auditorías.</td></tr><tr><td><strong>Application</strong></td><td>Almacena errores y eventos relacionados con aplicaciones del sistema y de terceros.</td></tr><tr><td><strong>System</strong></td><td>Contiene registros de eventos críticos del sistema, como arranques, errores y mensajes del kernel.</td></tr><tr><td><strong>Setup</strong></td><td>Incluye eventos relacionados con la configuración y cambios importantes en el sistema operativo.</td></tr><tr><td><strong>Forwarded Events</strong></td><td>Registra eventos enviados desde otros equipos para centralizar la auditoría de eventos.</td></tr></tbody></table>

Estos logs son accesibles y editables mediante el Visor de Eventos, que permite borrar manualmente entradas específicas de cada log. No obstante, es importante realizar estos cambios con comandos que dejen menos trazas evidentes.

### **Archivos de Historial de Comandos y Conexiones**

Windows también guarda un registro de comandos y conexiones en varios archivos y ubicaciones. En entornos de hacking ético, comprender estos registros ayuda a mejorar la detección y respuesta a incidentes.

<table><thead><tr><th width="282">Archivo</th><th>Descripción</th></tr></thead><tbody><tr><td><strong>PowerShell History</strong></td><td>Los comandos ejecutados en PowerShell se guardan en <code>$env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt</code>.</td></tr><tr><td><strong>Comandos ejecutados en CMD</strong></td><td>Aunque no tiene un archivo de historial por defecto, el historial de CMD en sesión se ve con <code>doskey /history</code>.</td></tr><tr><td><strong>Archivos de conexión RDP</strong></td><td>Windows guarda información de conexiones RDP en <code>C:\Users\[Usuario]\Documents</code> y en claves de registro de conexión.</td></tr></tbody></table>

### **Temporales y Prefetch en Windows**

Los archivos temporales y el prefetch también pueden contener rastros que identifican actividades recientes en el sistema.

<table><thead><tr><th width="322">Directorio</th><th>Descripción</th></tr></thead><tbody><tr><td><code>C:\Windows\Temp</code></td><td>Archivos temporales del sistema, a menudo usados por programas durante la ejecución.</td></tr><tr><td><code>C:\Users\[Usuario]\AppData\Local\Temp</code></td><td>Archivos temporales específicos del usuario, frecuentemente contienen rastros de programas ejecutados.</td></tr><tr><td><code>C:\Windows\Prefetch</code></td><td>Archivos Prefetch que contienen datos sobre la ejecución de programas, usados para optimizar el arranque.</td></tr></tbody></table>

### **Comandos para Borrar Evidencias en Windows**

Existen múltiples métodos y herramientas para limpiar logs y evidencias en Windows. A continuación, algunos de los comandos y utilidades más efectivos:

#### **Borrar Logs del Visor de Eventos**:&#x20;

El siguiente comando en PowerShell borra todos los eventos de una categoría específica (por ejemplo, “Security” o “Application”):

```powershell
wevtutil cl Security       # Borra el log de Seguridad
wevtutil cl Application    # Borra el log de Aplicación
wevtutil cl System         # Borra el log de Sistema
```

#### **Eliminar Historial de PowerShell**:&#x20;

PowerShell guarda el historial de comandos en un archivo de texto plano, que puede eliminarse de la siguiente manera:

```powershell
Remove-Item $env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

#### **Archivos Temporales**:&#x20;

Los archivos temporales pueden eliminarse con los siguientes comandos en CMD:

```sh
del /q /f %temp%\*       # Borra archivos temporales del usuario actual
del /q /f C:\Windows\Temp\*    # Borra archivos temporales globales
```

#### **Prefetch**:&#x20;

Para eliminar los archivos de Prefetch que contienen información sobre programas ejecutados:

```powershell
del C:\Windows\Prefetch\* /q
```

#### **Claves de Registro para Conexiones Remotas**:&#x20;

Las conexiones remotas RDP pueden rastrearse a través de varias claves en el registro. La limpieza de claves de RDP puede realizarse con el siguiente comando en PowerShell:

```powershell
Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Terminal Server Client\Default' -Name MRU* -Force
```

### **Herramientas Avanzadas para Borrado de Evidencias**

Algunas herramientas avanzadas pueden emplearse para borrar rastros y eliminar archivos de forma segura:

#### **Sysinternals SDelete**:&#x20;

Permite eliminar archivos y liberar espacio no usado sobrescribiéndolos para evitar su recuperación:

```powershell
sdelete -p 2 -s C:\Windows\Temp      # Sobrescribe dos veces los archivos en la carpeta Temp
```

#### **Auditpol**:&#x20;

Puede usarse para deshabilitar temporalmente las auditorías de seguridad en el sistema, lo que reduce la cantidad de eventos registrados. Esto es útil en entornos de prueba para observar la respuesta a la manipulación de auditorías:

```powershell
auditpol /clear   # Limpia las políticas de auditoría
```

#### Meterpreter (Windows):

```
run post/windows/manage/sdel FILE=C:\\Users\\vagrant\\desktop\\evidencias.txt
```

***

## <mark style="color:purple;">**Consideraciones Éticas**</mark>

Como en Linux, la eliminación de evidencias en Windows debe realizarse únicamente en entornos controlados y con autorización. La manipulación de logs y archivos en sistemas de producción es ilegal sin permiso explícito y puede interpretarse como encubrimiento de actividad maliciosa. En el contexto de hacking ético, la práctica debe estar documentada y limitada a entornos de laboratorio.
