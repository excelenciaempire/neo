
# Herramientas de Ofuscación de comandos

Si estamos tratando con herramientas de seguridad avanzadas, es posible que no podamos utilizar técnicas básicas de ofuscación manual. En esos casos, puede ser mejor recurrir a herramientas de ofuscación automatizadas. En esta sección se comentarán un par de ejemplos de este tipo de herramientas, una para `Linux`y otra para`Windows.`

***

## <mark style="color:purple;">Linux (Bashfuscator)</mark>

{% embed url="<https://github.com/Bashfuscator/Bashfuscator>" %}

Una herramienta útil que podemos utilizar para ofuscar comandos bash es [Bashfuscator](https://github.com/Bashfuscator/Bashfuscator) . Podemos clonar el repositorio desde GitHub y luego instalar sus requisitos, de la siguiente manera:

```shell-session
afsh4ck@kali$ git clone https://github.com/Bashfuscator/Bashfuscator
afsh4ck@kali$ cd Bashfuscator
afsh4ck@kali$ pip3 install setuptools==65
afsh4ck@kali$ python3 setup.py install --user
```

Una vez que tenemos la herramienta configurada, podemos comenzar a usarla desde el directorio `./bashfuscator/bin/`. Hay muchas opciones que podemos usar con la herramienta para ajustar nuestro comando ofuscado final, como podemos ver en el menú de ayuda con `-h`:

```shell-session
afsh4ck@kali$ cd ./bashfuscator/bin/
afsh4ck@kali$ ./bashfuscator -h

usage: bashfuscator [-h] [-l] ...SNIP...

optional arguments:
  -h, --help            show this help message and exit

Program Options:
  -l, --list            List all the available obfuscators, compressors, and encoders
  -c COMMAND, --command COMMAND
                        Command to obfuscate
...SNIP...
```

Podemos comenzar simplemente proporcionando el comando que queremos ofuscar con `-c`:

```shell-session
afsh4ck@kali$ ./bashfuscator -c 'cat /etc/passwd'

[+] Mutators used: Token/ForCode -> Command/Reverse
[+] Payload:
 ${*/+27\[X\(} ...SNIP...  ${*~}   
[+] Payload size: 1664 characters
```

Sin embargo, al ejecutar la herramienta de esta manera, se seleccionará aleatoriamente una técnica de ofuscación, que puede generar una longitud de comando que va desde unos pocos cientos de caracteres hasta más de un millón de caracteres. Por lo tanto, podemos usar algunas de las banderas del menú de ayuda para producir un comando ofuscado más corto y simple, como se muestra a continuación:

```shell-session
afsh4ck@kali$ ./bashfuscator -c 'cat /etc/passwd' -s 1 -t 1 --no-mangling --layers 1

[+] Mutators used: Token/ForCode
[+] Payload:
eval "$(W0=(w \  t e c p s a \/ d);for Ll in 4 7 2 1 8 3 2 4 8 5 7 6 6 0 9;{ printf %s "${W0[$Ll]}";};)"
[+] Payload size: 104 characters
```

Ahora podemos probar el comando generado con `bash -c ''`, para ver si ejecuta el comando deseado:

```shell-session
afsh4ck@kali$ bash -c 'eval "$(W0=(w \  t e c p s a \/ d);for Ll in 4 7 2 1 8 3 2 4 8 5 7 6 6 0 9;{ printf %s "${W0[$Ll]}";};)"'

root:x:0:0:root:/root:/bin/bash
...SNIP...
```

Podemos ver que el comando ofuscado funciona, aunque parece completamente ofuscado y no se parece a nuestro comando original. También podemos notar que la herramienta utiliza muchas técnicas de ofuscación, incluidas las que analizamos anteriormente y muchas otras.

***

## Windows (DOSfuscation)

También existe una herramienta muy similar que podemos usar para Windows llamada [DOSfuscation](https://github.com/danielbohannon/Invoke-DOSfuscation) . A diferencia de `Bashfuscator`, esta es una herramienta interactiva, ya que la ejecutamos una vez e interactuamos con ella para obtener el comando ofuscado deseado. Podemos clonar nuevamente la herramienta desde GitHub y luego invocarla a través de PowerShell, de la siguiente manera:

```powershell
PS C:\afsh4ck> git clone https://github.com/danielbohannon/Invoke-DOSfuscation.git
PS C:\afsh4ck> cd Invoke-DOSfuscation
PS C:\afsh4ck> Import-Module .\Invoke-DOSfuscation.psd1
PS C:\afsh4ck> Invoke-DOSfuscation
Invoke-DOSfuscation> help

HELP MENU :: Available options shown below:
[*]  Tutorial of how to use this tool             TUTORIAL
...SNIP...

Choose one of the below options:
[*] BINARY      Obfuscated binary syntax for cmd.exe & powershell.exe
[*] ENCODING    Environment variable encoding
[*] PAYLOAD     Obfuscated payload via DOSfuscation
```

Incluso podemos aprovechar el `tutorial` para ver un ejemplo de cómo funciona la herramienta. Una vez que estemos preparados, podemos empezar a utilizar la herramienta, de la siguiente manera:

```powershell
Invoke-DOSfuscation> SET COMMAND type C:\Users\htb-student\Desktop\flag.txt
Invoke-DOSfuscation> encoding
Invoke-DOSfuscation\Encoding> 1

...SNIP...
Result:
typ%TEMP:~-3,-2% %CommonProgramFiles:~17,-11%:\Users\h%TMP:~-13,-12%b-stu%SystemRoot:~-4,-3%ent%TMP:~-19,-18%%ALLUSERSPROFILE:~-4,-3%esktop\flag.%TMP:~-13,-12%xt
```

Finalmente, podemos intentar ejecutar el comando ofuscado en `CMD`, y vemos que efectivamente funciona como se esperaba:

```powershell
C:\afsh4ck> typ%TEMP:~-3,-2% %CommonProgramFiles:~17,-11%:\Users\h%TMP:~-13,-12%b-stu%SystemRoot:~-4,-3%ent%TMP:~-19,-18%%ALLUSERSPROFILE:~-4,-3%esktop\flag.%TMP:~-13,-12%xt

test_flag
```

{% hint style="info" %}
Consejo: Si no tenemos acceso a una máquina virtual Windows, podemos ejecutar el código anterior en una máquina virtual Linux a través de `pwsh`. Ejecuta `pwsh`y luego sigue exactamente el mismo comando anterior.
{% endhint %}
