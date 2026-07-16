
# Weak Password Policy

## <mark style="color:$primary;">Lab -</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**Vulnerable Bank Portal: Dictionary Attack**</mark>

### WSTG-ATHN07

[OWASP Top 10](https://owasp.org/www-project-top-ten/) es un documento informativo que describe los riesgos de seguridad más críticos para las aplicaciones web. Las pruebas de penetración se realizan según el estándar OWASP Top 10 para reducir o mitigar dichos riesgos.

En este ejercicio, nos centraremos en las vulnerabilidades [de autenticación defectuosa de OWASP A2](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/Top_10-2017_A2-Broken_Authentication) y veremos cómo aprovechar esta vulnerabilidad en una aplicación web de una sola página.

**Objetivo**: Aprovechar la vulnerabilidad de autenticación defectuosa para acceder al portal administrativo.

Instrucciones:&#x20;

* Dirección de correo electrónico para realizar un ataque de diccionario:  **<admin@secbank.com>**
* No ataques la puerta de enlace ubicada en la dirección IP 192.XY1.

***

En este lab tenemos una instancia de Kali con una aplicación bancaria vulnerable:

<figure><img src="/files/jAv7FqDFt6ayVBI9DEhe" alt=""><figcaption></figcaption></figure>

### Hosts

Nuestro objetivo es `secure-bank.com`:

```bash
root@attackdefense:~# cat /etc/hosts

127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
ff00::0	ip6-mcastprefix
ff02::1	ip6-allnodes
ff02::2	ip6-allrouters
10.1.0.11	attackdefense.com attackdefense
127.0.0.1 AttackDefense-Kali
192.174.104.2	attackdefense.com attackdefense
192.174.104.3 secure-bank.com
192.174.104.3 www.secure-bank.com
```

### Prueba de login

Captutamos un login con BurpSuite y vemos que hace una petición con el método `OPTIONS` al endpoint `/login` hacia el puerto `8000`:

<figure><img src="/files/49y1lqcRTbxOXqObQPxX" alt=""><figcaption></figcaption></figure>

Y depués de hacer forward observamos que los datos se envían en formato JSON a través de la API:

<figure><img src="/files/EzIgrgkUFdZgyLv74YcN" alt=""><figcaption></figcaption></figure>

### Forgot password

Si pulsamos en `forgot password` observamos que debemos introducir un `Customer ID` que enviará por mail el enlace para restablecer la contraseña:

<figure><img src="/files/OloSdmZn3rkKx2eeDrWv" alt=""><figcaption></figcaption></figure>

Al capturar el request con BurpSuite vemos que envía los datos por GET al endpoint `/reset?custid=1`

<figure><img src="/files/ARGUg0G3LZyB1BIaRbDw" alt=""><figcaption></figcaption></figure>

### Dictionary Attack

Capturamos un request normal > click derecho > Send to Intruder

<figure><img src="/files/34TBXaVEHi3erXp14N1o" alt=""><figcaption></figcaption></figure>

Añadimos el parámetro password a payload positions:

<figure><img src="/files/6ZUC0iFNjGEKZRd11gls" alt=""><figcaption></figcaption></figure>

En payloads cargamos una wordlist:

<figure><img src="/files/G92E2uB0QK6VvM8wB0Nt" alt=""><figcaption></figcaption></figure>

Iniciamos el ataque y observamos que el Lenght del payload `christmas` es distinto al resto, y obtenemos un token y una flag en la respuesta:

<figure><img src="/files/XEVtBgEq0DT3qzOAejOa" alt=""><figcaption></figcaption></figure>

Nos logueamos con esas credenciales y funciona, obteniendo de igual manera la flag:

<figure><img src="/files/A0iCLzAwULV8paCEhmr2" alt=""><figcaption></figcaption></figure>
