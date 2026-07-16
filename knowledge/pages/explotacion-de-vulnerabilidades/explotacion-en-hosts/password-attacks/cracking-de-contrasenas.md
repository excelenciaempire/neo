
# Cracking de Contraseñas

{% hint style="info" %}
Se utiliza para probar la seguridad de las contraseñas, aumentando la dificultad de su crackeo. Se suelen utilizar caracteres especiales y mezcla de números y letras mayúsculas y minúsculas para aumentar su seguridad.
{% endhint %}

## <mark style="color:purple;">John the Ripper</mark>

[John the Ripper](https://github.com/openwall/john) (`john`) es una herramienta de pentesting esencial que se utiliza para comprobar la seguridad de las contraseñas y descifrar contraseñas cifradas (o hash) mediante fuerza bruta o ataques de diccionario. Es un software de código abierto desarrollado inicialmente para sistemas basados ​​en UNIX y lanzado por primera vez en 1996. Se ha convertido en un elemento básico para los profesionales de la seguridad debido a sus diversas capacidades. La variante "Jumbo" se recomienda para quienes trabajan en el campo de la seguridad, ya que tiene optimizaciones de rendimiento y características adicionales como listas de palabras multilingües y soporte para arquitecturas de 64 bits. Esta versión es más efectiva para descifrar contraseñas con mayor precisión y velocidad.

Con esto, podemos usar varias herramientas para convertir diferentes tipos de archivos y hashes a un formato que John pueda utilizar. Además, el software se actualiza periódicamente para mantenerse al día con las tendencias y tecnologías de seguridad actuales, garantizando la seguridad del usuario.

***

### Tecnologías de cifrado

<table data-header-hidden><thead><tr><th width="298"></th><th></th></tr></thead><tbody><tr><td><strong>Tecnología de cifrado</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>UNIX crypt(3)</code></td><td>Crypt(3) es un sistema de cifrado UNIX tradicional con una clave de 56 bits.</td></tr><tr><td><code>Traditional DES-based</code></td><td>El cifrado basado en DES utiliza el algoritmo del estándar de cifrado de datos para cifrar los datos.</td></tr><tr><td><code>bigcrypt</code></td><td>Bigcrypt es una extensión del cifrado tradicional basado en DES. Utiliza una clave de 128 bits.</td></tr><tr><td><code>BSDI extended DES-based</code></td><td>El cifrado extendido basado en DES BSDI es una extensión del cifrado tradicional basado en DES y utiliza una clave de 168 bits.</td></tr><tr><td><code>FreeBSD MD5-based</code>(Linux y Cisco)</td><td>El cifrado basado en FreeBSD MD5 utiliza el algoritmo MD5 para cifrar datos con una clave de 128 bits.</td></tr><tr><td><code>OpenBSD Blowfish-based</code></td><td>El cifrado basado en OpenBSD Blowfish utiliza el algoritmo Blowfish para cifrar datos con una clave de 448 bits.</td></tr><tr><td><code>Kerberos/AFS</code></td><td>Kerberos y AFS son sistemas de autenticación que utilizan cifrado para garantizar una comunicación segura entre entidades.</td></tr><tr><td><code>Windows LM</code></td><td>El cifrado de Windows LM utiliza el algoritmo estándar de cifrado de datos para cifrar datos con una clave de 56 bits.</td></tr><tr><td><code>DES-based tripcodes</code></td><td>Los códigos de viaje basados ​​en DES se utilizan para autenticar a los usuarios según el algoritmo del estándar de cifrado de datos.</td></tr><tr><td><code>SHA-crypt hashes</code></td><td>Los hash SHA-crypt se utilizan para cifrar datos con una clave de 256 bits y están disponibles en versiones más recientes de Fedora y Ubuntu.</td></tr><tr><td><code>SHA-crypt</code>y <code>SUNMD5 hashes</code>(Solaris)</td><td>Los hashes SHA-crypt y SUNMD5 utilizan los algoritmos SHA-crypt y MD5 para cifrar datos con una clave de 256 bits y están disponibles en Solaris.</td></tr><tr><td><code>...</code></td><td>y muchos más.</td></tr></tbody></table>

***

## <mark style="color:purple;">John - Métodos de ataque</mark>

### **Ataques de diccionario**

Los ataques de diccionario implican el uso de una lista pregenerada de palabras y frases (conocida como diccionario) para intentar descifrar una contraseña. Esta lista de palabras y frases suele obtenerse de diversas fuentes, como diccionarios disponibles públicamente, contraseñas filtradas o incluso adquiridas en empresas especializadas. Luego, el diccionario se usa para generar una serie de cadenas que luego se usan para comparar con las contraseñas hash. Si se encuentra una coincidencia, la contraseña se descifra, proporcionando al atacante acceso al sistema y a los datos almacenados en él. Este tipo de ataque es muy eficaz. Por lo tanto, es esencial tomar las medidas necesarias para garantizar que las contraseñas se mantengan seguras, como usar contraseñas complejas y únicas, cambiarlas periódicamente y utilizar autenticación de dos factores.

### **Ataques de fuerza bruta**

Los ataques de fuerza bruta implican intentar todas las combinaciones imaginables de caracteres que podrían formar una contraseña. Este es un proceso extremadamente lento y, por lo general, solo se recomienda utilizar este método si no hay otras alternativas. También es importante tener en cuenta que cuanto más larga y compleja sea la contraseña, más difícil será descifrarla y más tiempo llevará agotar todas las combinaciones. Por este motivo, es muy recomendable que las contraseñas tengan al menos 8 caracteres de longitud, con una combinación de letras, números y símbolos.

### **Ataques de Rainbow Table**

Los ataques de Rainbow Table implican el uso de una tabla precalculada de hashes y sus correspondientes contraseñas de texto sin formato, que es un método mucho más rápido que un ataque de fuerza bruta. Sin embargo, este método está limitado por el tamaño de la rainbow table: cuanto más grande sea la tabla, más contraseñas y hashes podrá almacenar. Además, debido a la naturaleza del ataque, es imposible utilizar rainbow tables para determinar el texto sin formato de los hashes que aún no están incluidos en la tabla. Como resultado, los ataques a la rainbow table solo son efectivos contra los hashes que ya están presentes en la tabla, por lo que cuanto más grande sea la tabla, más exitoso será el ataque.

***

## <mark style="color:purple;">John - Modos de craqueo</mark>

`Single Crack Mode` es uno de los modos más comunes que se utilizan al intentar descifrar contraseñas utilizando una lista de contraseñas única. Es un ataque de fuerza bruta, lo que significa que se prueban todas las contraseñas de la lista, una por una, hasta encontrar la correcta. Este método es la forma más básica y sencilla de descifrar contraseñas y, por lo tanto, es una opción popular para quienes desean obtener acceso a un sistema seguro. Sin embargo, está lejos de ser el método más eficaz, ya que puede llevar un tiempo indefinido descifrar una contraseña, dependiendo de la longitud y complejidad de la contraseña en cuestión. La sintaxis básica del comando es:

### **Single Crack Mode**

```shell-session
afsh4ck@kali$ john --format=<hash_type> <hash or hash_file>
```

Por ejemplo, si tenemos un archivo `hashes_to_crack.txt`cuyo nombre contiene hashes `SHA-256`, el comando para descifrarlos sería:

```shell-session
afsh4ck@kali$ john --format=sha256 hashes_to_crack.txt
```

* `john`es el comando para ejecutar el programa John the Ripper
* `--format=sha256` especifica que el formato hash es SHA-256
* `hashes.txt` es el nombre del archivo que contiene los hashes que se van a descifrar

Cuando ejecutamos el comando, John leerá los hashes del archivo especificado y luego intentará descifrarlos comparándolos con las palabras en su lista de palabras incorporada y cualquier lista de palabras adicional especificada con la opción `--wordlist`. Además, utilizará cualquier regla establecida con la opción `--rules` (si se proporciona alguna regla) para generar más contraseñas candidatas.

El proceso de descifrar contraseñas puede ser complicado `very time-consuming`, ya que la cantidad de tiempo necesaria para descifrar una contraseña depende de múltiples factores, como la complejidad de la contraseña, la configuración de la máquina y el tamaño de la lista de palabras. Descifrar contraseñas es casi una cuestión de suerte. Porque la contraseña en sí puede ser elemental, pero si usamos una lista incorrecta donde la palabra no está presente o John no puede generarla, eventualmente no lograremos descifrar la contraseña.

John enviará las contraseñas descifradas a la consola y el archivo "john.pot" ( `~/.john/john.pot`) al directorio de inicio del usuario actual. Además, continuará descifrando los hashes restantes en segundo plano y podemos comprobar el progreso ejecutando el `john --show`comando. Para maximizar las posibilidades de éxito, es importante asegurarse de que las listas de palabras y las reglas utilizadas sean completas y estén actualizadas.

### **Cracking con John**

<table data-header-hidden><thead><tr><th width="146"></th><th width="235"></th><th></th></tr></thead><tbody><tr><td><strong>Hash Format</strong></td><td><strong>Example Command</strong></td><td><strong>Description</strong></td></tr><tr><td>afs</td><td><code>john --format=afs hashes_to_crack.txt</code></td><td>AFS (Andrew File System) password hashes</td></tr><tr><td>bfegg</td><td><code>john --format=bfegg hashes_to_crack.txt</code></td><td>bfegg hashes used in Eggdrop IRC bots</td></tr><tr><td>bf</td><td><code>john --format=bf hashes_to_crack.txt</code></td><td>Blowfish-based crypt(3) hashes</td></tr><tr><td>bsdi</td><td><code>john --format=bsdi hashes_to_crack.txt</code></td><td>BSDi crypt(3) hashes</td></tr><tr><td>crypt(3)</td><td><code>john --format=crypt hashes_to_crack.txt</code></td><td>Traditional Unix crypt(3) hashes</td></tr><tr><td>des</td><td><code>john --format=des hashes_to_crack.txt</code></td><td>Traditional DES-based crypt(3) hashes</td></tr><tr><td>dmd5</td><td><code>john --format=dmd5 hashes_to_crack.txt</code></td><td>DMD5 (Dragonfly BSD MD5) password hashes</td></tr><tr><td>dominosec</td><td><code>john --format=dominosec hashes_to_crack.txt</code></td><td>IBM Lotus Domino 6/7 password hashes</td></tr><tr><td>EPiServer SID hashes</td><td><code>john --format=episerver hashes_to_crack.txt</code></td><td>EPiServer SID (Security Identifier) password hashes</td></tr><tr><td>hdaa</td><td><code>john --format=hdaa hashes_to_crack.txt</code></td><td>hdaa password hashes used in Openwall GNU/Linux</td></tr><tr><td>hmac-md5</td><td><code>john --format=hmac-md5 hashes_to_crack.txt</code></td><td>hmac-md5 password hashes</td></tr><tr><td>hmailserver</td><td><code>john --format=hmailserver hashes_to_crack.txt</code></td><td>hmailserver password hashes</td></tr><tr><td>ipb2</td><td><code>john --format=ipb2 hashes_to_crack.txt</code></td><td>Invision Power Board 2 password hashes</td></tr><tr><td>krb4</td><td><code>john --format=krb4 hashes_to_crack.txt</code></td><td>Kerberos 4 password hashes</td></tr><tr><td>krb5</td><td><code>john --format=krb5 hashes_to_crack.txt</code></td><td>Kerberos 5 password hashes</td></tr><tr><td>LM</td><td><code>john --format=LM hashes_to_crack.txt</code></td><td>LM (Lan Manager) password hashes</td></tr><tr><td>lotus5</td><td><code>john --format=lotus5 hashes_to_crack.txt</code></td><td>Lotus Notes/Domino 5 password hashes</td></tr><tr><td>mscash</td><td><code>john --format=mscash hashes_to_crack.txt</code></td><td>MS Cache password hashes</td></tr><tr><td>mscash2</td><td><code>john --format=mscash2 hashes_to_crack.txt</code></td><td>MS Cache v2 password hashes</td></tr><tr><td>mschapv2</td><td><code>john --format=mschapv2 hashes_to_crack.txt</code></td><td>MS CHAP v2 password hashes</td></tr><tr><td>mskrb5</td><td><code>john --format=mskrb5 hashes_to_crack.txt</code></td><td>MS Kerberos 5 password hashes</td></tr><tr><td>mssql05</td><td><code>john --format=mssql05 hashes_to_crack.txt</code></td><td>MS SQL 2005 password hashes</td></tr><tr><td>mssql</td><td><code>john --format=mssql hashes_to_crack.txt</code></td><td>MS SQL password hashes</td></tr><tr><td>mysql-fast</td><td><code>john --format=mysql-fast hashes_to_crack.txt</code></td><td>MySQL fast password hashes</td></tr><tr><td>mysql</td><td><code>john --format=mysql hashes_to_crack.txt</code></td><td>MySQL password hashes</td></tr><tr><td>mysql-sha1</td><td><code>john --format=mysql-sha1 hashes_to_crack.txt</code></td><td>MySQL SHA1 password hashes</td></tr><tr><td>NETLM</td><td><code>john --format=netlm hashes_to_crack.txt</code></td><td>NETLM (NT LAN Manager) password hashes</td></tr><tr><td>NETLMv2</td><td><code>john --format=netlmv2 hashes_to_crack.txt</code></td><td>NETLMv2 (NT LAN Manager version 2) password hashes</td></tr><tr><td>NETNTLM</td><td><code>john --format=netntlm hashes_to_crack.txt</code></td><td>NETNTLM (NT LAN Manager) password hashes</td></tr><tr><td>NETNTLMv2</td><td><code>john --format=netntlmv2 hashes_to_crack.txt</code></td><td>NETNTLMv2 (NT LAN Manager version 2) password hashes</td></tr><tr><td>NEThalfLM</td><td><code>john --format=nethalflm hashes_to_crack.txt</code></td><td>NEThalfLM (NT LAN Manager) password hashes</td></tr><tr><td>md5ns</td><td><code>john --format=md5ns hashes_to_crack.txt</code></td><td>md5ns (MD5 namespace) password hashes</td></tr><tr><td>nsldap</td><td><code>john --format=nsldap hashes_to_crack.txt</code></td><td>nsldap (OpenLDAP SHA) password hashes</td></tr><tr><td>ssha</td><td><code>john --format=ssha hashes_to_crack.txt</code></td><td>ssha (Salted SHA) password hashes</td></tr><tr><td>NT</td><td><code>john --format=nt hashes_to_crack.txt</code></td><td>NT (Windows NT) password hashes</td></tr><tr><td>openssha</td><td><code>john --format=openssha hashes_to_crack.txt</code></td><td>OPENSSH private key password hashes</td></tr><tr><td>oracle11</td><td><code>john --format=oracle11 hashes_to_crack.txt</code></td><td>Oracle 11 password hashes</td></tr><tr><td>oracle</td><td><code>john --format=oracle hashes_to_crack.txt</code></td><td>Oracle password hashes</td></tr><tr><td>pdf</td><td><code>john --format=pdf hashes_to_crack.txt</code></td><td>PDF (Portable Document Format) password hashes</td></tr><tr><td>phpass-md5</td><td><code>john --format=phpass-md5 hashes_to_crack.txt</code></td><td>PHPass-MD5 (Portable PHP password hashing framework) password hashes</td></tr><tr><td>phps</td><td><code>john --format=phps hashes_to_crack.txt</code></td><td>PHPS password hashes</td></tr><tr><td>pix-md5</td><td><code>john --format=pix-md5 hashes_to_crack.txt</code></td><td>Cisco PIX MD5 password hashes</td></tr><tr><td>po</td><td><code>john --format=po hashes_to_crack.txt</code></td><td>Po (Sybase SQL Anywhere) password hashes</td></tr><tr><td>rar</td><td><code>john --format=rar hashes_to_crack.txt</code></td><td>RAR (WinRAR) password hashes</td></tr><tr><td>raw-md4</td><td><code>john --format=raw-md4 hashes_to_crack.txt</code></td><td>Raw MD4 password hashes</td></tr><tr><td>raw-md5</td><td><code>john --format=raw-md5 hashes_to_crack.txt</code></td><td>Raw MD5 password hashes</td></tr><tr><td>raw-md5-unicode</td><td><code>john --format=raw-md5-unicode hashes_to_crack.txt</code></td><td>Raw MD5 Unicode password hashes</td></tr><tr><td>raw-sha1</td><td><code>john --format=raw-sha1 hashes_to_crack.txt</code></td><td>Raw SHA1 password hashes</td></tr><tr><td>raw-sha224</td><td><code>john --format=raw-sha224 hashes_to_crack.txt</code></td><td>Raw SHA224 password hashes</td></tr><tr><td>raw-sha256</td><td><code>john --format=raw-sha256 hashes_to_crack.txt</code></td><td>Raw SHA256 password hashes</td></tr><tr><td>raw-sha384</td><td><code>john --format=raw-sha384 hashes_to_crack.txt</code></td><td>Raw SHA384 password hashes</td></tr><tr><td>raw-sha512</td><td><code>john --format=raw-sha512 hashes_to_crack.txt</code></td><td>Raw SHA512 password hashes</td></tr><tr><td>salted-sha</td><td><code>john --format=salted-sha hashes_to_crack.txt</code></td><td>Salted SHA password hashes</td></tr><tr><td>sapb</td><td><code>john --format=sapb hashes_to_crack.txt</code></td><td>SAP CODVN B (BCODE) password hashes</td></tr><tr><td>sapg</td><td><code>john --format=sapg hashes_to_crack.txt</code></td><td>SAP CODVN G (PASSCODE) password hashes</td></tr><tr><td>sha1-gen</td><td><code>john --format=sha1-gen hashes_to_crack.txt</code></td><td>Generic SHA1 password hashes</td></tr><tr><td>skey</td><td><code>john --format=skey hashes_to_crack.txt</code></td><td>S/Key (One-time password) hashes</td></tr><tr><td>ssh</td><td><code>john --format=ssh hashes_to_crack.txt</code></td><td>SSH (Secure Shell) password hashes</td></tr><tr><td>sybasease</td><td><code>john --format=sybasease hashes_to_crack.txt</code></td><td>Sybase ASE password hashes</td></tr><tr><td>xsha</td><td><code>john --format=xsha hashes_to_crack.txt</code></td><td>xsha (Extended SHA) password hashes</td></tr><tr><td>zip</td><td><code>john --format=zip hashes_to_crack.txt</code></td><td>ZIP (WinZip) password hashes</td></tr></tbody></table>

### **Modo de lista de palabras (wordlist)**

Se utiliza para descifrar contraseñas utilizando múltiples listas de palabras. Es un ataque de diccionario, lo que significa que probará todas las palabras de las listas una por una hasta encontrar la correcta. Generalmente se usa para descifrar múltiples hashes de contraseñas usando una lista de palabras o una combinación de listas de palabras. Es más efectivo que el modo Single Crack porque utiliza más palabras pero sigue siendo relativamente básico. La sintaxis básica del comando es:

```shell-session
afsh4ck@kali$ john --wordlist=<wordlist_file> --rules <hash_file>
```

Primero, especificamos el archivo o archivos de lista de palabras que se utilizarán para descifrar los hash de contraseña. La lista de palabras puede estar en formato de texto plano, con una palabra por línea. Se pueden especificar varias listas de palabras separándolas con una coma. Luego podemos especificar un conjunto de reglas o aplicar las reglas de manipulación integradas a las palabras de la lista de palabras. Estas reglas generan contraseñas candidatas mediante transformaciones como agregar números, poner letras en mayúscula y agregar caracteres especiales.

### **Modo incremental**

`Incremental Mode` es un modo avanzado que se utiliza para descifrar contraseñas utilizando un conjunto de caracteres. Es un ataque híbrido, lo que significa que intentará hacer coincidir la contraseña probando todas las combinaciones posibles de caracteres del conjunto de caracteres. Este modo es el más eficaz y, al mismo tiempo, el que consume más tiempo de todos los modos John. Este modo funciona mejor cuando sabemos cuál podría ser la contraseña, ya que probará todas las combinaciones posibles en secuencia, comenzando por la más corta.&#x20;

Esto lo hace mucho más rápido que el ataque de fuerza bruta, donde todas las combinaciones se prueban al azar. Además, el modo incremental también se puede utilizar para descifrar contraseñas débiles, que pueden resultar difíciles de descifrar con los modos estándar de John. La principal diferencia entre el modo incremental y el modo de lista de palabras es la fuente de las adivinanzas de contraseña. El modo incremental genera conjeturas sobre la marcha, mientras que el modo de lista de palabras utiliza una lista predefinida de palabras. Al mismo tiempo, el modo de descifrado único se utiliza para comparar una única contraseña con un hash.

La sintaxis para ejecutar John the Ripper en modo incremental es la siguiente:

### **Modo incremental en John**

```shell-session
afsh4ck@kali$ john --incremental <hash_file>
```

Usando este comando leeremos los hashes en el archivo hash especificado y luego generaremos todas las combinaciones posibles de caracteres, comenzando con un solo carácter e incrementando con cada iteración. Es importante tener en cuenta que este modo consume muchos recursos y puede tardar mucho en completarse, dependiendo de la complejidad de las contraseñas, la configuración de la máquina y la cantidad de caracteres establecidos. Además, es importante tener en cuenta que el juego de caracteres predeterminado está limitado a `a-zA-Z0-9`. Por lo tanto, si intentamos descifrar contraseñas complejas con caracteres especiales, necesitamos utilizar un juego de caracteres personalizado.

***

## <mark style="color:purple;">John - Descifrar archivos</mark>

También es posible descifrar incluso archivos cifrados o protegidos con contraseña con John. Usamos herramientas adicionales que procesan los archivos proporcionados y producen hashes con los que John puede trabajar. Detecta automáticamente los formatos e intenta descifrarlos. La sintaxis para esto puede verse así:

### **Descifrando archivos con John**

```shell-session
cry0l1t3@htb:~$ <tool> <file_to_crack> > file.hash
cry0l1t3@htb:~$ pdf2john server_doc.pdf > server_doc.hash
cry0l1t3@htb:~$ john server_doc.hash
                # o
cry0l1t3@htb:~$ john --wordlist=<wordlist.txt> server_doc.hash 
```

Además, podemos usar diferentes modos para esto con nuestras listas de palabras y reglas personales. Hemos creado una lista que incluye muchas, pero no todas, las herramientas que se pueden utilizar para John:

<table data-header-hidden><thead><tr><th width="261"></th><th></th></tr></thead><tbody><tr><td><strong>Herramienta</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>pdf2john</code></td><td>Convierte documentos PDF para John</td></tr><tr><td><code>ssh2john</code></td><td>Convierte claves privadas SSH para John</td></tr><tr><td><code>mscash2john</code></td><td>Convierte hashes de MS Cash para John</td></tr><tr><td><code>keychain2john</code></td><td>Convierte archivos de llavero de OS X para John</td></tr><tr><td><code>rar2john</code></td><td>Convierte archivos RAR para John</td></tr><tr><td><code>pfx2john</code></td><td>Convierte archivos PKCS#12 para John</td></tr><tr><td><code>truecrypt_volume2john</code></td><td>Convierte volúmenes TrueCrypt para John</td></tr><tr><td><code>keepass2john</code></td><td>Convierte bases de datos KeePass para John</td></tr><tr><td><code>vncpcap2john</code></td><td>Convierte archivos VNC PCAP para John</td></tr><tr><td><code>putty2john</code></td><td>Convierte claves privadas PuTTY para John</td></tr><tr><td><code>zip2john</code></td><td>Convierte archivos ZIP para John</td></tr><tr><td><code>hccap2john</code></td><td>Convierte capturas de protocolo de enlace WPA/WPA2 para John</td></tr><tr><td><code>office2john</code></td><td>Convierte documentos de MS Office para John</td></tr><tr><td><code>wpa2john</code></td><td>Convierte protocolos de enlace WPA/WPA2 para John</td></tr></tbody></table>

Se pueden encontrar más de estas herramientas de la siguiente manera:

```shell-session
afsh4ck@kali$ locate *2john*

/usr/bin/bitlocker2john
/usr/bin/dmg2john
/usr/bin/gpg2john
/usr/bin/hccap2john
/usr/bin/keepass2john
/usr/bin/putty2john
/usr/bin/racf2john
/usr/bin/rar2john
/usr/bin/uaf2john
/usr/bin/vncpcap2john
/usr/bin/wlanhcx2john
/usr/bin/wpapcap2john
/usr/bin/zip2john
/usr/share/john/1password2john.py
/usr/share/john/7z2john.pl
/usr/share/john/DPAPImk2john.py
/usr/share/john/adxcsouf2john.py
/usr/share/john/aem2john.py
/usr/share/john/aix2john.pl
/usr/share/john/aix2john.py
/usr/share/john/andotp2john.py
/usr/share/john/androidbackup2john.py
...SNIP...
```

En este módulo, trabajaremos mucho con John y, por lo tanto, deberíamos saber de qué es capaz esta herramienta.

## <mark style="color:purple;">Hashcat</mark>

Hashcat es una herramienta de cracking de contraseñas de código abierto que se utiliza para realizar ataques de fuerza bruta y diccionario contra hashes de contraseñas. Hashcat es capaz de utilizar la potencia de procesamiento de la CPU y la GPU para acelerar el proceso de cracking de contraseñas y puede descifrar hashes de contraseñas en muchos formatos diferentes.

Viene instalado por defecto en Kali Linux.

{% embed url="<https://github.com/hashcat/hashcat>" %}

### Instalación

```bash
git clone https://github.com/hashcat/hashcat.git
cd hashcat
make
```

### Uso

```bash
./hashcat -h
./hashcat -m <tipo_de_hash> <archivo_de_hash> <archivo_de_diccionario>
./hashcat -a 3 -m 1400 pass /usr/share/wordlists/rockyou.txt
```

`-a` Attack mode

`-m` Tipo de hash (en este caso 1400 se corresponde con SHA-256)

## <mark style="color:purple;">CrackStation</mark>

Es un servicio online que nos permite crackear hashes de contraseñas. Utiliza un diccionario con más de 190GB, y más de 1.5 billones de contraseñas.

{% embed url="<https://crackstation.net/>" %}

<figure><img src="/files/UfhR1DZlZHeZjQw9aCiB" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Changeme</mark>

Herramienta que busca contraseñas por defecto en una infraestructura de red. Changeme trabaja específicamente para detectar contraseñas débiles, comunes o predecibles en diferentes servicios, como LDAP, MySQL, PostgreSQL, FTP, SSH, SNMP y otros. La herramienta utiliza una base de datos de contraseñas comunes y diccionarios de fuerza bruta para verificar la fortaleza de las contraseñas.

{% embed url="<https://github.com/ztgrace/changeme>" %}

### Instalación y uso

```bash
git clone https://github.com/ztgrace/changeme.git
cd changeme
pip install -r requirements.txt
python3 changeme.py —dump # Nos vuelca todas las contraseñas por defecto
python3 changeme.py IP_RED_0/24
```

## <mark style="color:purple;">Generador de contraseñas seguras</mark>

<figure><img src="/files/tvAauOQiuLIbOeP3yh7o" alt=""><figcaption></figcaption></figure>

{% embed url="<https://www.avast.com/random-password-generator>" %}
Avast Random Password Generator
{% endembed %}

Este generador de contraseñas online de Avast nos permite crear contraseñas super seguras, mezclando mayúsculas, minúsculas, números y carácteres especiales, pudiendo controlar la longitud de la contraseña.

{% code title="E.j Contraseña segura" %}

```
2xVij;GY^Be@TI1;t82s^DE&2;1jZXFTT9aXC0a[QNo,Yv!NM,
```

{% endcode %}

{% hint style="info" %}
Si utilizamos un gestor de contraseñas como One Password o Bitwarden podemos elegir la contraseña más larga, ya que nos la almacenará y recordará automáticamente.
{% endhint %}
