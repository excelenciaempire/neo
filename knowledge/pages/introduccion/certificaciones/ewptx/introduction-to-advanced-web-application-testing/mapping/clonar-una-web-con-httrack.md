
# Clonar una web con HTTRack

## <mark style="color:$primary;">Clonación de sitios web</mark>

Cuando se audita una aplicación web, no siempre es posible o conveniente mantener una conexión activa con el servidor objetivo durante el análisis. La capacidad de trabajar **offline** es una herramienta fundamental para minimizar la exposición, reducir el ruido en los logs del servidor y permitir un análisis pausado del código fuente. HTTrack es la solución ideal para esta tarea.

***

### ¿Qué es HTTrack?

HTTrack es una utilidad de navegación offline que permite descargar un sitio web completo desde Internet a un directorio local. Construye recursivamente todas las estructuras de directorios, obteniendo HTML, imágenes y otros archivos del servidor, mientras reorganiza los enlaces para que funcionen localmente. Simplemente abre cualquier página del sitio "clonado" en tu navegador y podrás navegar como si estuvieras online.

{% embed url="<https://www.httrack.com/>" %}

#### **Características principales**

* **Actualizaciones inteligentes** – Puede actualizar un clon existente descargando solo los archivos modificados.
* **Reanudación de descargas** – Si la conexión falla, la descarga se puede reanudar desde donde se interrumpió.
* **Configuración total** – Control completo sobre qué descargar y qué ignorar mediante opciones y filtros.

***

## <mark style="color:$primary;">Instalación</mark>

**En distribuciones basadas en Debian/Ubuntu/Kali Linux:**

```bash
sudo apt install httrack
```

El tamaño de instalación es de aproximadamente 67 KB.

Puedes verificar que todo funciona correctamente con:

```bash
httrack -h
```

***

## <mark style="color:$primary;">Uso básico</mark>

La sintaxis fundamental de HTTrack es:

```bash
httrack [URLs] [-opciones] [+filtro_inclusión] [-filtro_exclusión] [+tipo_mime] [-tipo_mime]
```

El comando más simple para clonar un sitio web completo:

```bash
httrack http://ejemplo.com
```

Esto iniciará el asistente interactivo que te guiará a través de la configuración del proyecto, incluyendo:

* Nombre del proyecto
* Ruta donde guardar los archivos
* Acciones a realizar (mirror, get files, continue)
* Opciones de proxy (si es necesario)

***

## <mark style="color:$primary;">Opciones</mark>

**Nota:** Donde aparece `N` en las opciones, se debe reemplazar por un número.

#### **Acción**

<table data-header-hidden><thead><tr><th width="135.9630126953125"></th><th></th></tr></thead><tbody><tr><td>Opción</td><td>Descripción</td></tr><tr><td><code>w</code></td><td>Mirror de sitios web (comportamiento por defecto)</td></tr><tr><td><code>W</code></td><td>Mirror en modo semi-automático (hace preguntas)</td></tr><tr><td><code>g</code></td><td>Solo obtener archivos, guardar en directorio actual</td></tr><tr><td><code>i</code></td><td>Continuar un mirror interrumpido usando la caché</td></tr><tr><td><code>Y</code></td><td>Mirror de <strong>todos</strong> los enlaces ubicados en las páginas de primer nivel</td></tr></tbody></table>

#### **Límites y control**

<table data-header-hidden><thead><tr><th width="133.74072265625"></th><th></th></tr></thead><tbody><tr><td>Opción</td><td>Descripción</td></tr><tr><td><code>rN</code></td><td>Profundidad del mirror (<code>r9999</code> por defecto, equivalente a sin límite)</td></tr><tr><td><code>%eN</code></td><td>Profundidad de enlaces externos (<code>%e0</code> por defecto, no sigue enlaces externos)</td></tr><tr><td><code>mN</code></td><td>Longitud máxima de archivo para archivos no HTML</td></tr><tr><td><code>mN,N2</code></td><td>Longitud máxima para archivos no HTML (N) y HTML (N2)</td></tr><tr><td><code>MN</code></td><td>Tamaño total máximo que puede ser descargado/escaneado</td></tr><tr><td><code>EN</code></td><td>Tiempo máximo de mirror en segundos (ej: 3600 = 1 hora)</td></tr><tr><td><code>AN</code></td><td>Tasa de transferencia máxima en bytes/segundo (1000 = 1KB/s)</td></tr><tr><td><code>%cN</code></td><td>Número máximo de conexiones por segundo (<code>%c10</code> por defecto)</td></tr></tbody></table>

#### **Conexiones y rendimiento**

<table data-header-hidden><thead><tr><th width="130.7777099609375"></th><th></th></tr></thead><tbody><tr><td>Opción</td><td>Descripción</td></tr><tr><td><code>cN</code></td><td>Número de conexiones múltiples (<code>c8</code> por defecto)</td></tr><tr><td><code>TN</code></td><td>Timeout en segundos</td></tr><tr><td><code>RN</code></td><td>Número de reintentos (<code>R1</code> por defecto)</td></tr><tr><td><code>JN</code></td><td>Control de congestión: tasa mínima de transferencia tolerada por enlace</td></tr></tbody></table>

***

## <mark style="color:$primary;">Cheatsheet rápido</mark>

<table data-header-hidden><thead><tr><th width="188.25927734375"></th><th width="312.333251953125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando / Opción</td><td>Explicación</td></tr><tr><td>Mirror básico</td><td><code>httrack http://ejemplo.com</code></td><td>Asistente interactivo</td></tr><tr><td>Mirror rápido y agresivo</td><td><code>httrack --connection-per-second=50 --sockets=80 --keep-alive --display --verbose --advanced-progressinfo --disable-security-limits -n -i -s0 -m -F 'User-Agent' -A100000000 -#L500000000 'URL'</code></td><td>Alta velocidad, ignora cortesías</td></tr><tr><td>Ignorar <code>robots.txt</code></td><td><code>-s0</code></td><td>Muy útil cuando el sitio bloquea rastreadores</td></tr><tr><td>Saltear límites de seguridad</td><td><code>--disable-security-limits -A100000000</code></td><td>Elimina límites de velocidad</td></tr><tr><td>Obtener archivos "cercanos"</td><td><code>-n</code></td><td>Obtiene archivos como imágenes fuera del dominio</td></tr><tr><td>Conexiones rápidas</td><td><code>--connection-per-second=50 --sockets=80</code></td><td>Acelera la descarga</td></tr><tr><td>Personalizar agente de usuario</td><td><code>-F "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"</code></td><td>Evita bloqueos por user-agent</td></tr><tr><td>Profundidad de mirror</td><td><code>httrack -r2 http://ejemplo.com</code></td><td>Solo baja 2 niveles de profundidad</td></tr><tr><td>Seguir enlaces externos</td><td><code>httrack -%e2 http://ejemplo.com</code></td><td>Profundidad 2 en enlaces externos</td></tr><tr><td>Solo obtener archivos</td><td><code>httrack -g http://ejemplo.com/archivo.pdf</code></td><td>Descarga archivos individuales</td></tr><tr><td>Continuar mirror</td><td><code>httrack -i</code></td><td>Reanuda mirror interrumpido</td></tr><tr><td>Proxy básico</td><td><code>httrack -P proxy.ejemplo.com:8080 http://ejemplo.com</code></td><td>Usa proxy para la conexión</td></tr></tbody></table>
