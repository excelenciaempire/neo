
# Hashcat

[Hashcat](https://hashcat.net/) es una conocida herramienta de cracking de contraseñas para Linux, Windows y macOS. De 2009 a 2015 era software propietario, pero desde entonces se ha publicado como código abierto. Gracias a su excelente compatibilidad con GPU, permite descifrar una gran variedad de hashes. Al igual que John, Hashcat admite múltiples modos de ataque (cracking) que permiten atacar hashes de contraseñas de forma eficiente.

La sintaxis general utilizada para ejecutar hashcat es la siguiente:

```shell-session
afsh4ck@kali$ hashcat -a 0 -m 0 <hashes> [wordlist, rule, mask, ...]
```

En el comando anterior:

* `-a` se utiliza para especificar el `attack mode`
* `-m` se utiliza para especificar el `hash type`
* `<hashes>` es una cadena hash o un archivo que contiene uno o más hashes de contraseña del mismo tipo
* `[wordlist, rule, mask, ...]` es un marcador de posición para argumentos adicionales que dependen del modo de ataque

## <mark style="color:purple;">Tipos de hash</mark>

Hashcat admite cientos de tipos de hash diferentes, cada uno con un ID asignado. Se puede generar una lista de ID asociados ejecutando `hashcat --help`.

```shell-session
afsh4ck@kali$ hashcat --help

...SNIP...

- [ Hash modes ] -

      # | Name                                                       | Category
  ======+============================================================+======================================
    900 | MD4                                                        | Raw Hash
      0 | MD5                                                        | Raw Hash
    100 | SHA1                                                       | Raw Hash
   1300 | SHA2-224                                                   | Raw Hash
   1400 | SHA2-256                                                   | Raw Hash
  10800 | SHA2-384                                                   | Raw Hash
   1700 | SHA2-512                                                   | Raw Hash
  17300 | SHA3-224                                                   | Raw Hash
  17400 | SHA3-256                                                   | Raw Hash
  17500 | SHA3-384                                                   | Raw Hash
  17600 | SHA3-512                                                   | Raw Hash
   6000 | RIPEMD-160                                                 | Raw Hash
    600 | BLAKE2b-512                                                | Raw Hash
  11700 | GOST R 34.11-2012 (Streebog) 256-bit, big-endian           | Raw Hash
  11800 | GOST R 34.11-2012 (Streebog) 512-bit, big-endian           | Raw Hash
   6900 | GOST R 34.11-94                                            | Raw Hash
  17010 | GPG (AES-128/AES-256 (SHA-1($pass)))                       | Raw Hash
   5100 | Half MD5                                                   | Raw Hash
  17700 | Keccak-224                                                 | Raw Hash
  17800 | Keccak-256                                                 | Raw Hash
  17900 | Keccak-384                                                 | Raw Hash
  18000 | Keccak-512                                                 | Raw Hash
   6100 | Whirlpool                                                  | Raw Hash
  10100 | SipHash                                                    | Raw Hash
     70 | md5(utf16le($pass))                                        | Raw Hash
    170 | sha1(utf16le($pass))                                       | Raw Hash
   1470 | sha256(utf16le($pass))                                     | Raw Hash
...SNIP...
```

El sitio web hashcat alberga una lista completa de [hashes de ejemplo](https://hashcat.net/wiki/doku.php?id=example_hashes) que pueden ayudar a identificar manualmente un tipo de hash desconocido y determinar el identificador del modo hash Hashcat correspondiente.

Alternativamente, se puede utilizar [hashID](https://github.com/psypanda/hashID) para identificar rápidamente el tipo de hash hashcat especificando la flag `-m`

```shell-session
afsh4ck@htb[/htb]$ hashid -m '$1$FNr44XZC$wQxY6HHLrgrGX0e1195k.1'

Analyzing '$1$FNr44XZC$wQxY6HHLrgrGX0e1195k.1'
[+] MD5 Crypt [Hashcat Mode: 500]
[+] Cisco-IOS(MD5) [Hashcat Mode: 500]
[+] FreeBSD MD5 [Hashcat Mode: 500]
```

## <mark style="color:purple;">Modos de ataque</mark>

Hashcat tiene muchos modos de ataque diferentes, incluyendo `dictionary`, `mask`, `combinator` y `association`. En esta sección, repasaremos los dos primeros, ya que probablemente sean los más comunes que necesitarás usar.

### **Ataque de diccionario**

[El ataque de diccionario](https://hashcat.net/wiki/doku.php?id=dictionary_attack) (`-a 0`) es, como su nombre indica, un ataque de diccionario. El usuario proporciona hashes de contraseñas y una lista de palabras como entrada, y Hashcat prueba cada palabra de la lista como una posible contraseña hasta encontrar la correcta o hasta agotar la lista.

Por ejemplo, imaginemos que extrajimos el siguiente hash de contraseña de una base de datos SQL: `e3e3ec5831ad5e7288241960e5d4fdb8`. Primero, podríamos identificarlo como un hash MD5, cuyo ID de hash es `0`. Para intentar descifrar este hash usando la wordlist `rockyou.txt`, se usaría el siguiente comando:

```shell-session
afsh4ck@kali$ hashcat -a 0 -m 0 e3e3ec5831ad5e7288241960e5d4fdb8 /usr/share/wordlists/rockyou.txt

...SNIP...               

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 0 (MD5)
Hash.Target......: e3e3ec5831ad5e7288241960e5d4fdb8
Time.Started.....: Sat Apr 19 08:58:44 2025 (0 secs)
Time.Estimated...: Sat Apr 19 08:58:44 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1706.6 kH/s (0.14ms) @ Accel:512 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 28672/14344385 (0.20%)
Rejected.........: 0/28672 (0.00%)
Restore.Point....: 27648/14344385 (0.19%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: 010292 -> spongebob9
Hardware.Mon.#1..: Util: 40%

Started: Sat Apr 19 08:58:43 2025
Stopped: Sat Apr 19 08:58:46 2025
```

Una lista de palabras por sí sola no suele ser suficiente para descifrar el hash de una contraseña. Como en el caso de John, se puede usar `rules` para realizar modificaciones específicas en las contraseñas y generar aún más intentos. Los archivos de reglas que vienen con hashcat se encuentran generalmente en `/usr/share/hashcat/rules`:

```shell-session
afsh4ck@kali$ ls -l /usr/share/hashcat/rules

total 2852
-rw-r--r-- 1 root root 309439 Apr 24  2024 Incisive-leetspeak.rule
-rw-r--r-- 1 root root  35802 Apr 24  2024 InsidePro-HashManager.rule
-rw-r--r-- 1 root root  20580 Apr 24  2024 InsidePro-PasswordsPro.rule
-rw-r--r-- 1 root root  64068 Apr 24  2024 T0XlC-insert_00-99_1950-2050_toprules_0_F.rule
-rw-r--r-- 1 root root   2027 Apr 24  2024 T0XlC-insert_space_and_special_0_F.rule
-rw-r--r-- 1 root root  34437 Apr 24  2024 T0XlC-insert_top_100_passwords_1_G.rule
-rw-r--r-- 1 root root  34813 Apr 24  2024 T0XlC.rule
-rw-r--r-- 1 root root   1289 Apr 24  2024 T0XlC_3_rule.rule
-rw-r--r-- 1 root root 168700 Apr 24  2024 T0XlC_insert_HTML_entities_0_Z.rule
-rw-r--r-- 1 root root 197418 Apr 24  2024 T0XlCv2.rule
-rw-r--r-- 1 root root    933 Apr 24  2024 best64.rule
-rw-r--r-- 1 root root    754 Apr 24  2024 combinator.rule
-rw-r--r-- 1 root root 200739 Apr 24  2024 d3ad0ne.rule
-rw-r--r-- 1 root root 788063 Apr 24  2024 dive.rule
-rw-r--r-- 1 root root  78068 Apr 24  2024 generated.rule
-rw-r--r-- 1 root root 483425 Apr 24  2024 generated2.rule
drwxr-xr-x 2 root root   4096 Oct 19 15:30 hybrid
-rw-r--r-- 1 root root    298 Apr 24  2024 leetspeak.rule
-rw-r--r-- 1 root root   1280 Apr 24  2024 oscommerce.rule
-rw-r--r-- 1 root root 301161 Apr 24  2024 rockyou-30000.rule
-rw-r--r-- 1 root root   1563 Apr 24  2024 specific.rule
-rw-r--r-- 1 root root     45 Apr 24  2024 toggles1.rule
-rw-r--r-- 1 root root    570 Apr 24  2024 toggles2.rule
-rw-r--r-- 1 root root   3755 Apr 24  2024 toggles3.rule
-rw-r--r-- 1 root root  16040 Apr 24  2024 toggles4.rule
-rw-r--r-- 1 root root  49073 Apr 24  2024 toggles5.rule
-rw-r--r-- 1 root root  55346 Apr 24  2024 unix-ninja-leetspeak.rule
```

Como otro ejemplo, imaginemos que se filtró un hash MD5 adicional de la base de datos SQL: `1b0556a75770563578569ae21392630c`. No pudimos descifrarlo usando `rockyou.txt` , así que, en un intento posterior, podríamos aplicar algunas transformaciones comunes basadas en reglas. Un conjunto de reglas que podríamos probar es `best64.rule`, que contiene 64 modificaciones estándar de contraseñas, como añadir números o sustituir caracteres por sus equivalentes "leet". Para realizar este tipo de ataque, añadiríamos la opción `-r <ruleset>` al comando, como se muestra a continuación:

```shell-session
afsh4ck@kali$ hashcat -a 0 -m 0 1b0556a75770563578569ae21392630c /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

...SNIP...

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 0 (MD5)
Hash.Target......: 1b0556a75770563578569ae21392630c
Time.Started.....: Sat Apr 19 09:16:35 2025 (0 secs)
Time.Estimated...: Sat Apr 19 09:16:35 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Mod........: Rules (/usr/share/hashcat/rules/best64.rule)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........: 13624.4 kH/s (5.40ms) @ Accel:512 Loops:77 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 236544/1104517645 (0.02%)
Rejected.........: 0/236544 (0.00%)
Restore.Point....: 2048/14344385 (0.01%)
Restore.Sub.#1...: Salt:0 Amplifier:0-77 Iteration:0-77
Candidate.Engine.: Device Generator
Candidates.#1....: slimshady -> drousd
Hardware.Mon.#1..: Util: 47%

Started: Sat Apr 19 09:16:35 2025
Stopped: Sat Apr 19 09:16:37 2025
```

### **Ataque con máscara**

[El ataque de máscara](https://hashcat.net/wiki/doku.php?id=mask_attack) (`-a 3`) es un tipo de ataque de fuerza bruta en el que el espacio de claves lo define explícitamente el usuario. Por ejemplo, si sabemos que una contraseña tiene ocho caracteres, en lugar de probar todas las combinaciones posibles, podríamos definir una máscara que pruebe combinaciones de seis letras seguidas de dos números.

Una máscara se define combinando una secuencia de símbolos, cada uno de los cuales representa un conjunto de caracteres integrado o personalizado. Hashcat incluye varios conjuntos de caracteres integrados:

<table><thead><tr><th width="115.828125">Símbolo</th><th>Charset</th></tr></thead><tbody><tr><td>?l</td><td>abcdefghijklmnopqrstuvwxyz</td></tr><tr><td>?u</td><td>ABCDEFGHIJKLMNOPQRSTUVWXYZ</td></tr><tr><td>?d</td><td>0123456789</td></tr><tr><td>?h</td><td>0123456789abcdef</td></tr><tr><td>?H</td><td>0123456789ABCDEF</td></tr><tr><td>?s</td><td>«space»!"#$%&#x26;'()*+,-./:;&#x3C;=>?@[]^_`{</td></tr><tr><td>?a</td><td>?l?u?d?s</td></tr><tr><td>?b</td><td>0x00 - 0xff</td></tr></tbody></table>

Los conjuntos de caracteres personalizados se pueden definir con los argumentos `-1`, `-2`, `-3`, y `-4`, y luego hacer referencia a ellos con `?1`, `?2`, `?3`, y `?4`.

Supongamos que queremos probar contraseñas que empiezan con una letra mayúscula, continúan con cuatro letras minúsculas, un dígito y finalmente un símbolo. La máscara hashcat resultante sería `?u?l?l?l?l?d?s`.

```shell-session
afsh4ck@kali$ hashcat -a 3 -m 0 1e293d6912d074c0fd15844d803400dd '?u?l?l?l?l?d?s'

...SNIP...

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 0 (MD5)
Hash.Target......: 1e293d6912d074c0fd15844d803400dd
Time.Started.....: Sat Apr 19 09:43:02 2025 (4 secs)
Time.Estimated...: Sat Apr 19 09:43:06 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Mask.......: ?u?l?l?l?l?d?s [7]
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   101.6 MH/s (9.29ms) @ Accel:512 Loops:1024 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 456237056/3920854080 (11.64%)
Rejected.........: 0/456237056 (0.00%)
Restore.Point....: 25600/223080 (11.48%)
Restore.Sub.#1...: Salt:0 Amplifier:5120-6144 Iteration:0-1024
Candidate.Engine.: Device Generator
Candidates.#1....: Uayvf7- -> Dikqn5!
Hardware.Mon.#1..: Util: 98%

Started: Sat Apr 19 09:42:46 2025
Stopped: Sat Apr 19 09:43:08 2025
```

***

## <mark style="color:purple;">Caso práctico</mark>

### Pregunta 1

> Utiliza un ataque de diccionario para descifrar el hash de la contraseña.&#x20;
>
> (Hash: e3e3ec5831ad5e7288241960e5d4fdb8)

```bash
hashcat -a 0 -m 0 e3e3ec5831ad5e7288241960e5d4fdb8 /usr/share/wordlists/rockyou.txt

hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 6.0+debian  Linux, None+Asserts, RELOC, LLVM 18.1.8, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
============================================================================================================================================
* Device #1: cpu-skylake-avx512-AMD Ryzen 7 8845HS w/ Radeon 780M Graphics, 2124/4313 MB (1024 MB allocatable), 16MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Raw-Hash

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 4 MB

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 14344385

e3e3ec5831ad5e7288241960e5d4fdb8:crazy!                   
                                                          
Session..........: hashcat
Status...........: Cracked
```

### Pregunta 2

> Utiliza un ataque de diccionario con reglas para descifrar el hash de la segunda contraseña.&#x20;
>
> (Hash: 1b0556a75770563578569ae21392630c)

```bash
hashcat -a 0 -m 0 1b0556a75770563578569ae21392630c /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule 

hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 6.0+debian  Linux, None+Asserts, RELOC, LLVM 18.1.8, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
============================================================================================================================================
* Device #1: cpu-skylake-avx512-AMD Ryzen 7 8845HS w/ Radeon 780M Graphics, 2124/4313 MB (1024 MB allocatable), 16MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 77

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Raw-Hash

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 4 MB

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 1104517645

1b0556a75770563578569ae21392630c:c0wb0ys1                 
                                                          
Session..........: hashcat
Status...........: Cracked
```

### Pregunta 3

> Utiliza un ataque de máscara para descifrar el tercer hash de la contraseña.&#x20;
>
> (Hash: 1e293d6912d074c0fd15844d803400dd)

```bash
hashcat -a 3 -m 0 1e293d6912d074c0fd15844d803400dd '?u?l?l?l?l?d?s'

hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 6.0+debian  Linux, None+Asserts, RELOC, LLVM 18.1.8, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
============================================================================================================================================
* Device #1: cpu-skylake-avx512-AMD Ryzen 7 8845HS w/ Radeon 780M Graphics, 2124/4313 MB (1024 MB allocatable), 16MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Brute-Force
* Raw-Hash

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 4 MB

1e293d6912d074c0fd15844d803400dd:Mouse5!                  
                                                          
Session..........: hashcat
Status...........: Cracked
```
