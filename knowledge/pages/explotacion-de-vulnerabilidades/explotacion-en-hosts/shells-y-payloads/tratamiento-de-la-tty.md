
# Tratamiento de la TTY

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Generación de Shells interactivas</mark>

***

Al final de la última sección, establecimos una sesión de shell con el objetivo. Inicialmente, nuestro shell era limitado (también denominado `jail shell`), por lo que usamos python para generar un shell TTY bourne que nos diera acceso a más comandos y un mensaje desde el que trabajar. Esta será probablemente una situación en la que nos encontraremos cada vez más a medida que practicamos en labs virtuales y en el mundo real.

Puede haber ocasiones en las que aterricemos en un sistema con un shell limitado y Python no esté instalado. En estos casos, es bueno saber que podríamos usar varios métodos diferentes para generar un shell interactivo. Examinemos algunos de ellos.

Sepa que cada vez que veamos `/bin/sh` o `/bin/bash`, esto también podría reemplazarse con el binario asociado con el lenguaje del intérprete de shell presente en ese sistema. Con la mayoría de los sistemas Linux, es probable que encontremos `bourne shell`( `/bin/sh`) y `bourne again shell`( `/bin/bash`) presentes en el sistema de forma nativa.

***

### Python

Si tenemos python instalado en nuestro sistema podemos ejecutar el siguiente comando para tener una shell interactiva:

```python
python -c 'import pty; pty.spawn("/bin/bash")'
```

***

### /bin/sh -i

Este comando ejecutará el intérprete de shell especificado en la ruta en modo interactivo ( `-i`).

```bash
/bin/sh -i
sh: no job control in this shell
sh-4.2$
```

***

### Bash

```bash
script /dev/null -c bash
ctrl+Z
stty raw -echo; fg
reset xterm
stty rows 38 columns 168
export TERM=xterm
export SHELL=bash
```

***

### Perl

Si el lenguaje de programación [Perl](https://www.perl.org/) está presente en el sistema, estos comandos ejecutarán el intérprete de shell especificado.

```bash
perl —e 'exec "/bin/sh";
```

```bash
perl: exec "/bin/sh";
```

El comando de arriba debe ejecutarse desde un script.

***

### Ruby

Si el lenguaje de programación [Ruby](https://www.ruby-lang.org/en/) está presente en el sistema, este comando ejecutará el intérprete de shell especificado:

```bash
ruby: exec "/bin/sh"
```

El comando de arriba debe ejecutarse desde un script.

***

### Lua

Si el lenguaje de programación [Lua](https://www.lua.org/) está presente en el sistema, podemos usar el método `os.execute` para ejecutar el intérprete de shell especificado usando el comando completo a continuación:

```bash
lua: os.execute('/bin/sh')
```

El comando de arriba debe ejecutarse desde un script.

***

### AWK

[AWK](https://man7.org/linux/man-pages/man1/awk.1p.html) es un lenguaje de procesamiento y escaneo de patrones similar a C presente en la mayoría de los sistemas basados ​​en UNIX/Linux, ampliamente utilizado por desarrolladores y administradores de sistemas para generar informes. También se puede utilizar para generar un caparazón interactivo. Esto se muestra en el breve script awk a continuación:

```bash
awk 'BEGIN {system("/bin/sh")}'
```

***

### Find

[Find](https://man7.org/linux/man-pages/man1/find.1.html) es un comando presente en la mayoría de los sistemas Unix/Linux y se utiliza ampliamente para buscar y revisar archivos y directorios utilizando varios criterios. También se puede utilizar para ejecutar aplicaciones e invocar un intérprete de shell.

```bash
find / -name nameoffile -exec /bin/awk 'BEGIN {system("/bin/sh")}' \;
```

Este uso del comando buscar busca cualquier archivo enumerado después de la opción `-name`, luego ejecuta `awk`( `/bin/awk`) y ejecuta el mismo script que analizamos en la sección awk para ejecutar un intérprete de shell.

***

### Usando Exec para iniciar un Shell

```bash
find . -exec /bin/sh \; -quit
```

Este uso del comando de búsqueda utiliza la opción de ejecución ( `-exec`) para iniciar el intérprete de shell directamente. Si `find` no puede encontrar el archivo especificado, no se obtendrá ningún shell.

***

### VIM

Sí, podemos configurar el idioma del intérprete de shell desde el popular editor de texto basado en línea de comandos `VIM`. Esta es una situación muy específica en la que nos encontraríamos si tuviéramos que utilizar este método, pero es bueno saberlo por si acaso.

```bash
vim -c ':!/bin/sh'
```

**Vim Escape**

```bash
vim
:set shell=/bin/sh
:shell
```

***

## <mark style="color:purple;">Consideraciones sobre permisos de ejecución</mark>

Además de conocer todas las opciones enumeradas anteriormente, debemos tener en cuenta los permisos que tenemos con la cuenta de sesión de shell. Siempre podemos intentar ejecutar este comando para enumerar las propiedades del archivo y los permisos que tiene nuestra cuenta sobre cualquier archivo o binario determinado:

### **Permisos**

```bash
ls -la <path/to/fileorbinary>
```

También podemos intentar ejecutar este comando para verificar qué permisos `sudo` tiene la cuenta a la que llegamos:

### **sudo-l**

```bash
sudo -l

Matching Defaults entries for apache on ILF-WebSrv:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User apache may run the following commands on ILF-WebSrv:
    (ALL : ALL) NOPASSWD: ALL
```

El comando `sudo -l` anterior necesitará un shell interactivo estable para ejecutarse. Considerar los permisos no solo nos permitirá ver qué comandos podemos ejecutar, sino que también puede comenzar a darnos una idea de los vectores potenciales que nos permitirán escalar privilegios.
