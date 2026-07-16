
# Cookie Tampering

## <mark style="color:$primary;">Lab -</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**Vulnerable Bank Portal: Improper Session Management**</mark>

En este ejercicio, nos centraremos en las vulnerabilidades [OWASP A2 Broken Authentication](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A2-Broken_Authentication) y veremos cómo aprovechar esta vulnerabilidad en una aplicación web.

**Objetivo**: Aprovechar la vulnerabilidad de Broken Authentication para acceder al portal administrativo.

Es posible que se requieran las siguientes credenciales:

```
james@secbank.com | password1
```

<figure><img src="/files/jON2tKWfkQGutFSw5cRN" alt=""><figcaption></figcaption></figure>

***

### Login

Al loguearnos observamos que tenemos un mensaje: `No Flag for you :(`

<figure><img src="/files/jimYYPBsE5CTlRQ03SHG" alt=""><figcaption></figcaption></figure>

### Broken Auth con Cookie Tampering

Intercentamos un login con BurpSuite y vemos que se envía al puerto 5000, lo cual ns indica una posible API de por medio:

<figure><img src="/files/kb4fov8t4pj04XmdghIe" alt=""><figcaption></figcaption></figure>

Hacemos forward, y una vez logueados observamos que se establece una `Cookie Set-Cookie` con un  Session ID y un `Path`:

<figure><img src="/files/wDy5an7xCWJKDscFJd8I" alt=""><figcaption></figcaption></figure>

```
sessid=bG9nZ2VkaW49VHJ1ZTthZG1pbj1GYWxzZQ==
```

Este Session ID está codificado en Base64 (lo sabemos por los dos signos de = al final).

#### Decodificar Session ID

Lo decodificamos con click derecho > Send to decoder

<figure><img src="/files/xRRAYTnoWDhbwHys8mpB" alt=""><figcaption></figcaption></figure>

Y observamos el texto en plano:

<figure><img src="/files/q1n8IJ6cxtDhu3s4HGxH" alt=""><figcaption></figcaption></figure>

```
±ë,id=loggedin=True;admin=False
```

Cambiamos el valor de admin de False a True y lo codificamos de nuevo en base64, también podemos hacerlo con el comando:

```bash
echo -n "loggedin=True;admin=True" | base64
bG9nZ2VkaW49VHJ1ZTthZG1pbj1UcnVl
```

#### Log out

Interceptamos un request de logout:

<figure><img src="/files/yNHRKHnwhEZVhC5nbOzD" alt=""><figcaption></figcaption></figure>

Y modificamos el valor de logout por `/` (que es la ruta del Path):

```
Path=/
```

Y la cookie por nuestra cookie modificada:

```
bG9nZ2VkaW49VHJ1ZTthZG1pbj1UcnVl
```

<figure><img src="/files/xYocxfYpHetMu4T3na5t" alt=""><figcaption></figcaption></figure>

#### Obtenemos la flag

En HTTP History del request de logout, observamos la flag en la respuesta:

<figure><img src="/files/czlTmc19u0R3kun6eJfl" alt=""><figcaption></figcaption></figure>
