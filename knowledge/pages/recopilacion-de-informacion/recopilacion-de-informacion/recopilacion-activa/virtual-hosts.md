
# Virtual Hosts

Un host virtual ( `vHost`) es una característica que permite alojar varios sitios web en un solo servidor. Esta es una excelente solución si tenemos muchos sitios web y no queremos pasar por el proceso lento (y costoso) de configurar un nuevo servidor web para cada uno. Imaginaos tener que configurar un servidor web diferente para una versión móvil y de escritorio de la misma página. Hay dos formas de configurar hosts virtuales:

* Virtual host basado en `IP`
* Virtual host basado en `Nombre`

## <mark style="color:purple;">**Virtual host basado en IP**</mark>

Para este tipo, un host puede tener múltiples interfaces de red. Se pueden configurar varias direcciones IP o alias de interfaz en cada interfaz de red de un host. Los servidores o servidores virtuales que se ejecutan en el host pueden vincularse a una o más direcciones IP. Esto significa que se pueden direccionar diferentes servidores con diferentes direcciones IP en este host. Desde el punto de vista del cliente, los servidores son independientes entre sí.

## <mark style="color:purple;">**Virtual host basado en nombres**</mark>

La distinción para qué dominio se solicita el servicio se realiza a nivel de aplicación. Por ejemplo, varios nombres de dominio, como `admin.inlanefreight.htb` y `backup.inlanefreight.htb`, pueden hacer referencia a la misma IP. Internamente en el servidor, estos se separan y distinguen mediante diferentes carpetas. Usando este ejemplo, en un servidor Linux, el vHost  `admin.inlanefreight.htb` podría apuntar a la carpeta `/var/www/admin`. El nombre del directorio `backup.inlanefreight.htb` se adaptaría y podría verse así `/var/www/backup`.

Durante nuestras actividades de descubrimiento de subdominios, hemos visto algunos subdominios que tienen la misma dirección IP que pueden ser hosts virtuales o, en algunos casos, diferentes servidores detrás de un proxy.

Imaginemos que hemos identificado un servidor web `192.168.10.10` durante un pentest interno y muestra un sitio web predeterminado usando el siguiente comando. ¿Hay hosts virtuales presentes?

```shell-session
afsh4ck@kali$ curl -s http://192.168.10.10

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

Realizamos una solicitud `curl` enviando un dominio previamente identificado durante la recopilación de información en el encabezado `HOST`. Podemos hacerlo así:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ curl -s http://192.168.10.10 -H "Host: randomtarget.com"
</strong>
&#x3C;html>
    &#x3C;head>
        &#x3C;title>Welcome to randomtarget.com!&#x3C;/title>
    &#x3C;/head>
    &#x3C;body>
        &#x3C;h1>Success! The randomtarget.com server block is working!&#x3C;/h1>
    &#x3C;/body>
&#x3C;/html>
</code></pre>

Ahora podemos automatizar esto usando un archivo de diccionario de posibles nombres de vhost (como `/usr/share/seclists/Discovery/DNS/namelist.txt`) y examinando el encabezado Content-Length para buscar diferencias.

### **Lista de hosts virtuales**

Este es un ejemplo de lista de host virtuales `namelist.txt`:

```shell-session
app
blog
dev-admin
forum
help
m
my
shop
some
store
support
www
```

## <mark style="color:purple;">**Fuzzing de vHost con CURL**</mark>

{% code overflow="wrap" %}

```bash
cat namelist.txt | while read vhost;do echo "\n********\nFUZZING: ${vhost}\n********";curl -s -I http://192.168.10.10 -H "HOST: ${vhost}.randomtarget.com" | grep "Content-Length: ";done

********
FUZZING: app
********
Content-Length: 612

********
FUZZING: blog
********
Content-Length: 612

********
FUZZING: dev-admin
********
Content-Length: 120

....
```

{% endcode %}

También podríamos guardar los resultados añadiendo al final `> vhost` (o el nombre que le queramos dar al archivo):

{% code overflow="wrap" %}

```bash
cat /usr/share/seclists/Discovery/DNS/namelist.txt | while read vhost;do echo "\n********\nFUZZING: ${vhost}\n********";curl -s -I http://10.129.129.104 -H "HOST: ${vhost}.inlanefreight.htb" | grep "Content-Length: ";done > vhosts
```

{% endcode %}

Después podemos filtrar los resultados utilizando el comando grep nuevamente y filtramos las líneas que contienen el texto `“Content-Length:”`. Luego, usamos el comando `uniq` para eliminar cualquier línea duplicada en un archivo de texto y la flag `-c` para contar la cantidad de veces que aparece cada línea única.

```bash
cat vhosts | grep "Content-Length:" | uniq -c
```

```bash
cat vhosts | grep "Content-Length:" | uniq -c
   3133 Content-Length: 10918
      1 Content-Length: 102    # <--- Línea única
      1 Content-Length: 103    # <--- Línea única
      1 Content-Length: 100    # <--- Línea única
      1 Content-Length: 94     # <--- Línea única
      1 Content-Length: 95     # <--- Línea única
      1 Content-Length: 96     # <--- Línea única
```

Luego podríamos ver el vhost filtrado con el siguiente comando:

```bash
cat vhosts | grep -B 4 "Content-Length: 102"
```

```bash
cat vhosts | grep -B 4 "Content-Length: 102"
********
FUZZING: ap
********
Content-Length: 102

cat vhosts | grep -B 4 "Content-Length: 103"
********
FUZZING: app
********
Content-Length: 103

cat vhosts | grep -B 4 "Content-Length: 100"
********
FUZZING: citrix
********
Content-Length: 100

cat vhosts | grep -B 4 "Content-Length: 94" 
********
FUZZING: customers
********
Content-Length: 94

cat vhosts | grep -B 4 "Content-Length: 95" 
********
FUZZING: dmz
********
Content-Length: 94

cat vhosts | grep -B 4 "Content-Length: 96"              
********
FUZZING: www2
********
Content-Length: 96
```

Como vemos hay 6 vhost en esta máquina: `ap`, `app`, `citrix` , `customers` , `dmz` y `www2` . Podríamos acceder a cada una de ellas u obtener información a través de curl de la siguiente manera:

```bash
curl -s http://10.129.129.104 -H "Host: ap.inlanefreight.htb"
<!doctype html>
<head>FLAG No.1:</head>
<body>
	HTB{h8973hrpiusnzjoie7zrou23i4zhmsxi8732zjso}
</body>

curl -s http://10.129.129.104 -H "Host: app.inlanefreight.htb"
<!doctype html>
<head>FLAG No.2:</head>
<body>
	HTB{u23i4zhmsxi872z3rn98h7nh2sxnbgriusd32zjso}
</body>

curl -s http://10.129.129.104 -H "Host: citrix.inlanefreight.htb"
<!doctype html>
<head>FLAG No.3:</head>
<body>
	HTB{Fl4gF0uR_o8763tznb4xou7zhgsniud7gfi734}
</body>

curl -s http://10.129.129.104 -H "Host: customers.inlanefreight.htb"
<!doctype html>
<head>FLAG No.4:</head>
<body>
	HTB{bzghi7tghin2u76x3ghdni62higz7x3s}
</body>

curl -s http://10.129.129.104 -H "Host: dmz.inlanefreight.htb"
<!doctype html>
<head>FLAG</head>
<body>
	HTB{7zbnr4i3n7zhrxn347zhh3dnrz4dh7zdjfbgn6d}
</body>

curl -s http://10.129.129.104 -H "Host: www2.inlanefreight.htb"
<!doctype html>
<head>FLAG</head>
<body>
	HTB{h8973hrpiusnzjoie7zrou23i4zhmsxi8732zjso}
</body>
```

### Post enumeración

Después de identificar los hosts virtuales, agregamos HTTP o HTTPS para generar una lista de URL. Podemos usar un script bash de una sola línea para hacer eso.

```bash
for i in $(cat vhost2); do echo "https://"$i; done > vhosts3
```

***

## <mark style="color:purple;">Automatizar enumeración de vHosts</mark>

### Ffuf

Podemos utilizar este enfoque manual para una pequeña lista de hosts virtuales, pero no será factible si tenemos una lista extensa. Usando [ffuf](https://github.com/ffuf/ffuf) , podemos acelerar el proceso y filtrar según los parámetros presentes en la respuesta. Repitamos el mismo proceso que hicimos con ffuf, pero primero, veamos algunas de sus opciones.

```bash
MATCHER OPTIONS:
  -mc                 Match HTTP status codes, or "all" for everything. (default: 200,204,301,302,307,401,403,405)
  -ml                 Match amount of lines in response
  -mr                 Match regexp
  -ms                 Match HTTP response size
  -mw                 Match amount of words in response

FILTER OPTIONS:
  -fc                 Filter HTTP status codes from response. Comma separated list of codes and ranges
  -fl                 Filter by amount of lines in response. Comma separated list of line counts and ranges
  -fr                 Filter regexp
  -fs                 Filter HTTP response size. Comma separated list of sizes and ranges
  -fw                 Filter by amount of words in response. Comma separated list of word counts and ranges
```

Podemos unir o filtrar respuestas según diferentes opciones. El servidor web responde con un sitio web estático y predeterminado cada vez que publicamos un host virtual no válido en el encabezado `HOST`. Podemos usar la opción `-fs` de filtrar por tamaño para descartar la respuesta predeterminada ya que siempre tendrá el mismo tamaño.

```bash
curl -s -I http://192.168.10.10 -H "HOST: defnotvalid.randomtarget.com" | grep "Content-Length:"

Content-Length: 612
```

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ ffuf -w /usr/share/dirb/wordlists/common.txt -t 50 -u http://192.168.10.10 -H "HOST: FUZZ.randomtarget.com" -fs 612

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.1.0-git
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.10.10
 :: Wordlist         : FUZZ: ./vhosts
 :: Header           : Host: FUZZ.randomtarget.com
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response size: 612
________________________________________________

dev-admin               [Status: 200, Size: 120, Words: 7, Lines: 12]
www                     [Status: 200, Size: 185, Words: 41, Lines: 9]
some                    [Status: 200, Size: 195, Words: 41, Lines: 9]
:: Progress: [12/12] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```

{% endcode %}

Dónde:

* `-w`: Ruta a nuestra lista de palabras
* `-u`: URL que queremos difuminar
* `-H "HOST: FUZZ.randomtarget.com"`: Este es el encabezado `HOST` y la palabra `FUZZ` se utilizará como punto de fuzzing.
* `-fs 612`: Filtra respuestas con un tamaño de 612, tamaño de respuesta predeterminado en este caso.

### Gobuster

Con Gobuster también podríamos encontrar vhost con el siguiente comando:

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ gobuster vhost -u http://10.129.118.153 -w /usr/share/dirb/wordlists/common.txt -t 50  -p pattern --exclude-length 301 -t 10
```

{% endcode %}

Antes debemos crear un archivo pattern que contenga el nombre del host para automatizar la búsqueda de subdominios:

```shell-session
afsh4ck@kali$ echo '{GOBUSTER}.inlanefreight.htb' > pattern             

afsh4ck@kali$ cat pattern                                  
{GOBUSTER}.inlanefreight.htb
```

```shell-session
afsh4ck@kali$ gobuster vhost -u http://10.129.178.242 -w /usr/share/dirb/wordlists/common.txt -t 50  -p pattern --exclude-length 301 -t 10

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:              http://10.129.178.242
[+] Method:           GET
[+] Threads:          10
[+] Wordlist:         /usr/share/dirb/wordlists/common.txt
[+] Patterns:         pattern (1 entries)
[+] User Agent:       gobuster/3.6
[+] Timeout:          10s
[+] Append Domain:    false
[+] Exclude Length:   301
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
Found: ap.inlanefreight.htb Status: 200 [Size: 102]
Found: app.inlanefreight.htb Status: 200 [Size: 103]
Found: citrix.inlanefreight.htb Status: 200 [Size: 100]
Found: customers.inlanefreight.htb Status: 200 [Size: 94]
Found: dmz.inlanefreight.htb Status: 200 [Size: 95]
Found: www2.inlanefreight.htb Status: 200 [Size: 96]
Progress: 9228 / 4615 (199.96%)
===============================================================
Finished
===============================================================
```

## <mark style="color:purple;">Cheatsheet</mark>

<table data-header-hidden><thead><tr><th width="492"></th><th></th></tr></thead><tbody><tr><td><strong>Recurso/Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>curl -s http://192.168.10.10 -H "Host: randomtarget.com"</code></td><td>Cambiar el encabezado HTTP HOST para solicitar un dominio específico.</td></tr><tr><td><code>cat ./vhosts.list | while read vhost;do echo "\n********\nFUZZING: ${vhost}\n********";curl -s -I http://&#x3C;IP address> -H "HOST: ${vhost}.target.domain" | grep "Content-Length: ";done</code></td><td>Fuerza bruta para posibles hosts virtuales en el dominio de destino.</td></tr><tr><td><code>ffuf -w ./vhosts -u http://&#x3C;IP address> -H "HOST: FUZZ.target.domain" -fs 612</code></td><td>Fuerza bruta para posibles hosts virtuales en el dominio de destino utilizando <code>ffuf</code>.</td></tr></tbody></table>
