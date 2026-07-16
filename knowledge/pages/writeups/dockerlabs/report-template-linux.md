
# Report Template - Linux

<figure><img src="/files/hZMiyVkDAuu0CnV3Yxuj" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Despliegue de la máquina</mark>

```bash
sudo bash auto_deploy.sh library.tar

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2
```

## <mark style="color:purple;">Información General</mark>

* **IP:** `172.17.0.2`
* **Sistema operativo:** Linux
* **Dificultad:** 🟢 Fácil | 🟡 Media | 🔴 Difícil (seleccionar)
* **Fecha:** DD-MM-AAAA

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "172.17.0.2" | sudo tee -a /etc/hosts
```

### Acceso Web

Accedemos a `http://planning.htb` y observamos que parece ser una plataforma de cursos en línea.

<figure><img src="/files/i7yQwHwiDrUCEZlLguIu" alt=""><figcaption></figcaption></figure>

Comandos adicionales útiles:

```bash
host 172.17.0.2
dig 172.17.0.2
curl -I 172.17.0.2
whatweb h172.17.0.2
netcat -vz 172.17.0.2 1-1000
```

***

## <mark style="color:purple;">Escaneo de Puertos</mark>

```bash
sudo nmap -v -sV -T5 172.17.0.2
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1
80/tcp open  http    nginx 1.24.0
```

Observaciones: Solo encontramos puertos comunes abiertos.

***

## <mark style="color:purple;">Enumeración Web</mark>

### Testing de Formularios

* Probar inyecciones SQL y XSS:
  * `' OR '1'='1`
  * `<script>alert(1)</script>`
* Observar mensajes, errores, cambios de comportamiento
* Herramientas: Burp Suite, sqlmap, wfuzz

Probamos distintas técnicas de inyección SQL/XSS sin éxito.

### Fuzzing de Directorios

```bash
dirsearch -u 172.17.0.2 -x 404
```

```bash
gobuster dir -u http://172.17.0.2 -w /usr/share/wordlists/dirb/common.txt
```

```bash
ffuf -u http://172.17.0.2/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

**Directorios encontrados:**

* `/about.php`
* `/contact.php`
* `/js/` (403)
* `/lib/` (403)

No se encuentran datos sensibles directamente accesibles.

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://172.17.0.2 -H "Host: defnotvalid.planning.htb" | grep "Content-Length:"

Content-Length: 178
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://172.17.0.2/ -H 'Host: FUZZ.planning.htb' -fs 178
```

**Encontramos el subdominio:** `grafana.planning.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de Grafana v11.0.0.

***

## <mark style="color:purple;">Explotación</mark>

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con Grafana 11.0.0 en fuentes como:

* <https://sploitus.com>
* <https://exploit-db.com>
* <https://github.com>

**Exploit seleccionado:** *(Describir qué exploit se usó y su URL de referencia)*

### Ejecución del Exploit

Describir paso a paso cómo se logró la ejecución remota o el primer acceso.

***

## <mark style="color:purple;">Acceso Inicial</mark>

Una vez obtenido acceso:

* Verificar usuario actual (`whoami`)
* Verificar entorno (`uname -a`, `id`, `sudo -l`)

***

## <mark style="color:purple;">User Flag</mark>

Ubicación y obtención de la flag del usuario:

```bash
cat /home/<usuario>/user.txt
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

Herramientas usadas:

* `linpeas.sh`
* `pspy`
* `sudo -l`
* `find / -perm -4000 2>/dev/null`

#### Técnica aplicada

Describir la técnica usada: binario con SUID, cronjob mal configurado, credenciales duras, etc.

***

### 👑 Root Flag

```bash
cat /root/root.txt
```
