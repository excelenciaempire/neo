
# Web Application Penetration Testing CTF 2

Este laboratorio se centra en la identificación y explotación de vulnerabilidades en aplicaciones web para descubrir flags ocultas. Utilizará diversas técnicas de pruebas de penetración para analizar la aplicación web objetivo. Su objetivo es investigar las debilidades en los diferentes componentes de la aplicación y detectar todos los indicadores ocultos. Mediante el reconocimiento, los ataques de inyección, la enumeración de usuarios y la explotación de errores de configuración, verificarás las vulnerabilidades de seguridad críticas que podrían explotarse en un ataque real.

### Task 1

> Identify a vulnerability in the 'About CTF' page.

Nuestro objetivo es `target.ine.local`:

```bash
┌──(root㉿INE)-[~]
└─# cat /etc/hosts
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.1.0.9        INE
127.0.0.1 AttackDefense-Kali
192.24.30.2     INE
192.24.30.2 INE
192.24.30.3 target.ine.local
```

Al acceder a About CTF vemos que se pasa un parámetro en la URL que pinta el número en el front de la web:

<figure><img src="/files/19ubssX4SFKYaMkhz4eh" alt=""><figcaption></figcaption></figure>

Y al modificar el número en la URL vemos que el número en el front cambia, por lo que podríamos explotarlo:

<figure><img src="/files/apHW0SIsCrp9yOhzoony" alt=""><figcaption></figcaption></figure>

Si vemos el código fuente de la página vemos la FLAG 1 en un comentario en un script:

<figure><img src="/files/7vESzQLwPLkhquVZwcmU" alt=""><figcaption></figcaption></figure>

### Task 2

> Exploit the login page vulnerability.

<figure><img src="/files/92wsyDTsfuG2fYERlkB7" alt=""><figcaption></figcaption></figure>

Si en el login introducimos la siguiente inyección conseguimos bypassearlo y acceder con cualquier contraseña:

```bash
admin' OR 1=1-- - 
# Cualquier contraseña
```

<figure><img src="/files/TZJOWchfsLPVsAquzJuV" alt=""><figcaption></figcaption></figure>

### Task 3

> Exploit the search functionality to discover hidden users.

Al usar el siguiente payload en el buscador nos devuelve todos los usuarios y la FLAG 3:

```
' or 1=1 -- - 
```

<figure><img src="/files/tb10X5JpUqaPB1piFanO" alt=""><figcaption></figcaption></figure>

### Task 4

> Leverage user profile enumeration to extract sensitive data.

Al loguearnos con la inyección de la task 2 vemos que en la url hay un ID de usuario:

<figure><img src="/files/A6HB4WAULeOdn3PzqnwA" alt=""><figcaption></figcaption></figure>

Cambiando el ID del usuario rooty (`576786`) nos devuelve la FLAG 4:

<figure><img src="/files/yVioWOdZiDCddAlZTOZp" alt=""><figcaption></figcaption></figure>
