
# Ffuf

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que hacen muchas peticiones al servidor del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

<figure><img src="/files/fOFj56R0bUF1kT4oz05Y" alt=""><figcaption></figcaption></figure>

ffuf utiliza una lista de palabras clave o diccionario para generar solicitudes HTTP manipuladas y ver cómo responde la aplicación.

Donde indiquemos el parámetro `FUZZ` probará todas las palabras del diccionario

## <mark style="color:purple;">Fuzzing con ffuf</mark>

### Fuzzing de directorios

```bash
ffuf -w /usr/share/wordlists/rockyou.txt -u http://example.com/FUZZ
```

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ -u https://inlanefreight.com/FUZZ -mc 200,301,302

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://inlanefreight.com/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,301,302
________________________________________________

wp-content              [Status: 301, Size: 329, Words: 20, Lines: 10, Duration: 36ms]
wp-includes             [Status: 301, Size: 330, Words: 20, Lines: 10, Duration: 36ms]
wp-admin                [Status: 301, Size: 327, Words: 20, Lines: 10, Duration: 50ms]
```

### Fuzzing buscando archivos específicos

```bash
ffuf -w /usr/share/wordlists/rockyou.txt -u http://example.com/FUZZ -e .jpg,.pdf
```

{% hint style="info" %}
El parámetro `-e` sirve para filtrar por tipo de archivo
{% endhint %}

### Fuzzing de subdominios

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u https://FUZZ.kali.org/   

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://FUZZ.kali.org/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

old                     [Status: 200, Size: 2920, Words: 113, Lines: 18, Duration: 105ms]
www                     [Status: 200, Size: 45355, Words: 2637, Lines: 72, Duration: 511ms]
images                  [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 526ms]
download                [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 520ms]
forums                  [Status: 200, Size: 10277, Words: 1179, Lines: 170, Duration: 503ms]
docs                    [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 519ms]
image                   [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 508ms]
archive                 [Status: 200, Size: 2170, Words: 86, Lines: 13, Duration: 104ms]
tools                   [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 529ms]
git                     [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 496ms]
downloads               [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 503ms]
```

### Niveles de profundidad

```bash
ffuf -w rockyou.txt -u http://example.com/FUZZ -recursion -recursion-depth 2
```

{% hint style="info" %}
El parámetro `-recursion` sirve para hacer escaneo profundo dentro de cada directorio encontrado
{% endhint %}

### Respuestas con un código de estado HTTP 200

```bash
ffuf -w rockyou.txt -u http://example.com/FUZZ -mc 200
```

### Descubrir Vhosts

{% code overflow="wrap" %}

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://94.237.48.48:54645/ -H 'Host: FUZZ.example.com' -ms 0
```

{% endcode %}

```bash
ffuf -u http://example.com -H "Host:FUZZ.example.com" -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt:FUZZ -fs 612

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://example.com
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt
 :: Header           : Host: FUZZ.example.com
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 12
________________________________________________

web                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 64ms]
m                       [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 65ms]
mail1                   [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 65ms]
gw                      [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 66ms]
dev                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 87ms]
secure                  [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 86ms]
mail2                   [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
ww1                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
ww42                    [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 87ms]
owa                     [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
server                  [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
webmail                 [Status: 200, Size: 15949, Words: 6243, Lines: 518, Duration: 90ms]
crm                     [Status: 200, Size: 6360, Words: 397, Lines: 150, Duration: 98ms]
```

### Fuzzing de extensiones

{% code overflow="wrap" %}

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt -u http://faculty.academy.htb:40053/indexFUZZ  
```

{% endcode %}

### Fuzzing de parámetros de URL

Método GET

{% code overflow="wrap" %}

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php?FUZZ=key -fs 774
```

{% endcode %}

Método POST

{% code overflow="wrap" %}

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs 774
```

{% endcode %}

### Fuzzing con Cookie Session

```bash
ffuf -w rockyou.txt -u http://example.com/FUZZ -H "Cookie: sessionid=123456"
```

### Guardar resultados en HTML

```bash
ffuf -w rockyou.txt -u http://example.com/FUZZ -o output.txt -of html
```

## <mark style="color:purple;">Fuzzing avanzado con ffuf</mark>

### Utilizar varios diccionarios simultáneamente

{% code overflow="wrap" %}

```bash
ffuf -u http://IP_VICTIM/W1/W2 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:W1 -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:W2
```

{% endcode %}

{% hint style="info" %}
Utilizar :W1 y :W2  después de la ruta para establecer los diccionarios
{% endhint %}

### Fuzzing de USER o PASSWORD en Login

* Capturar request de login con burpsuite y guardar archivo request-burp
* Editar archivo con un editor de texto como (gedit o nano) cambiando los parámetros que queramos fuzzear por FUZZ o :W1 y :W2 si usamos varios diccionarios

{% code overflow="wrap" %}

```bash
ffuf -request request-burp -w /usr/share/seclists/Discovery/Web-Content/directory-list-lowercase-2.3-small.txt
```

{% endcode %}

## <mark style="color:purple;">Ffuf Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="387"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td> <code>ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?FUZZ=value' -fs 2287</code></td><td>Fuzzing de parámetros en una URL</td></tr><tr><td> <code>ffuf -w /opt/useful/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?language=FUZZ' -fs 2287</code></td><td>Fuzzing con LFI payloads</td></tr><tr><td> <code>ffuf -w /opt/useful/SecLists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ -u 'http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?language=../../../../FUZZ/index.php' -fs 2287</code></td><td>Fuzzing  de webroot path</td></tr><tr><td> <code>ffuf -w ./LFI-WordList-Linux:FUZZ -u 'http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?language=../../../../FUZZ' -fs 2287</code></td><td>Fuzzing de configuraciones de servidor</td></tr><tr><td> <a href="https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI">LFI Wordlists</a></td><td></td></tr><tr><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt">LFI-Jhaddix.txt</a></td><td></td></tr><tr><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-linux.txt">Webroot path wordlist for Linux</a></td><td></td></tr><tr><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-windows.txt">Webroot path wordlist for Windows</a></td><td></td></tr><tr><td><a href="https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Linux">Server configurations wordlist for Linux</a></td><td></td></tr><tr><td><a href="https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Windows">Server configurations wordlist for Windows</a></td><td></td></tr></tbody></table>
