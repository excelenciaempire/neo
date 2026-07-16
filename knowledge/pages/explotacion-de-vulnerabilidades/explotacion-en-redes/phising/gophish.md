
# Gophish

**GoPhish** es una plataforma de código abierto diseñada para ejecutar campañas de phishing ético y entrenar a los usuarios contra ataques de ingeniería social. Es ampliamente utilizada en ciberseguridad para simular ataques reales y educar a los empleados o usuarios finales sobre cómo reconocer intentos de phishing.

### Repositorio de Github

{% embed url="<https://github.com/gophish/gophish.git>" %}

### Web oficial

{% embed url="<https://getgophish.com/>" %}

## <mark style="color:purple;">Instalación</mark>

```bash
git clone https://github.com/gophish/gophish.git
cd gophish
go build
```

## <mark style="color:purple;">Configuración</mark>

Debemos editar el archivo `config.json` en `phish_server` y poner nuestra url local 192.168.x.x:

```json
"phish_server": {
     "listen_url": "192.168.1.181:80",
     "use_tls": false,
     "cert_path": "example.crt",
     "key_path": "example.key"
},
```

Una vez configurado ejecutamos el binario con:

```
./gophish
```

Ahora abrimos en un navegador la URL que nos da al final:

```bash
time="2025-02-17T20:23:34Z" level=info msg="Starting IMAP monitor manager"
time="2025-02-17T20:23:34Z" level=info msg="Starting phishing server at http://192.168.1.181:80"
time="2025-02-17T20:23:34Z" level=info msg="Starting new IMAP monitor for user admin"
time="2025-02-17T20:23:34Z" level=info msg="TLS Certificate Generation complete"
time="2025-02-17T20:23:34Z" level=info msg="Starting admin server at https://127.0.0.1:3333"
```

```
https://127.0.0.1:3333
```

En la primera ejecución también nos muestra las credenciales por defecto para el usuario admin en la siguiente línea:

```bash
time="2025-02-17T20:23:34Z" level=info msg="Please login with the username admin and the password 51555af8a3484baa"
```

<figure><img src="/files/Wdb5hrG59LZoP7IauhfI" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">1. Crear cuenta de email SMTP</mark>

Vamos a crearnos una cuenta en TurboSMTP para hacer la campaña de prueba. También podríamos usar cualquier servidor de emails que admita SMTP, como Hostinguer por ejemplo.

{% hint style="success" %}
Tiene un **plan gratuito** de hasta 200 mails enviados al día, suficiente para nuestro test.
{% endhint %}

{% embed url="<https://serversmtp.com/es/>" %}

Podemos ver los datos de conexión en `Conectando vía SMTP`:

<figure><img src="/files/ehsYeIZF35qsYV2boDQG" alt=""><figcaption></figcaption></figure>

Esos datos los tendremos que vincular en Gophish. En `Sending Profiles > New Sending Profile`

<figure><img src="/files/OoI5gtQaKfyT32CtFurq" alt=""><figcaption></figcaption></figure>

Probamos a enviar un correo de prueba y vemos que se envía correctamente. Le damos a Save Profile

## <mark style="color:purple;">2. Crear Landing Page</mark>

Vamos a crear una landing page para capturar credenciales. En el contexto de phising en una organización podría ser una buena idea generar una landing de un panel de login de una aplicación que use la empresa (Microsoft, Oracle, Figma...)

1. Le damos a `import site` y escribimos la URL, en nuestro caso usaremos facebook.com
2. Activamos los checks de captura de credenciales
3. Añadimos la página a la que redirigirá al usuario una vez introduzca los datos

<figure><img src="/files/fcVcQJ6LFLmfd3s3WoyC" alt=""><figcaption></figcaption></figure>

4. Le damos a `Save Page` y se guarda correctamente

## <mark style="color:purple;">3. Crear plantilla de email</mark>

Ahora debemos crear una plantilla de email. Lo que mejor suele funcionar es un email de intento de login en una aplicación, que tenga un CTA de "`No he sido yo`" o cambiar contraseña, que nosotros como atacantes podemos modificar. Sería un mail parecido a este:

<figure><img src="/files/wRvjxBVwUzqYhKroYnn2" alt=""><figcaption></figcaption></figure>

Podríamos usar también herramientas cómo [Cyber Phish](https://github.com/Cyber-Dioxide/CyberPhish) que nos generan plantillas de email en html para phising. Para importarlo en Gophish necesitamos el html del email. En Gmail por ejemplo se puede conseguir haciendo clic en los `3 puntitos` del mail > `Mostrar original`

<figure><img src="/files/QQezVSK8r3nJxJzgCZBa" alt=""><figcaption></figcaption></figure>

Luego le damos a `Copiar en el portapapeles`:

<figure><img src="/files/ZKdBkKcq4EAf3SJM0lbS" alt=""><figcaption></figcaption></figure>

Ahora en Gophish vamos a `Email Templates > New Template > Import Email` y pegamos el código fuente del mail anterior. Debemos corregir cualquier error que pueda tener el email para dejarlo prácticamente igual al original.

<figure><img src="/files/VP9TudfsTYXtSTMw1MsK" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">4. Crear usuarios y grupos</mark>

Ahora vamos a añadir los usuarios que queramos que les lleguen los mails. Podemos añadirlos uno por uno manualmente o importar un CSV. Para recoger multitud de emails y nombres de empleados de una empresa podríamos usar técnicas de OSINT como [Crosslinked](https://github.com/m8sec/CrossLinked) por ejemplo.

```bash
python3 crosslinked.py -f '{first}.{last}@microsoft.com' microsoft
```

<figure><img src="https://afsh4ck.gitbook.io/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252F0j7U0grk7ISGC2nI10Fe%252Fimage.png%3Falt%3Dmedia%26token%3D7d98dd9e-a1c3-47aa-8974-4b1cfbeb4338&#x26;width=768&#x26;dpr=4&#x26;quality=100&#x26;sign=d5417d50&#x26;sv=2" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/hc0Txr1eo37bWKf9R2Z0" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">5. Crear campaña</mark>

Ahora vamos a juntar todos los datos que hemos creado para generar una campaña:

<figure><img src="/files/XLNVqkff3XZWVAASeFjH" alt=""><figcaption></figcaption></figure>

Le damos a `Launch Campaign` y ya solo nos quedaría esperar a que los usuarios caigan en el phising para recibir credenciales:

<figure><img src="/files/0tbmAtILuexCziyXkwoZ" alt=""><figcaption></figcaption></figure>
