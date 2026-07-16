
# Cupp

{% embed url="<https://github.com/Mebus/cupp>" %}

## <mark style="color:purple;">**Instalación**</mark>

```shell-session
afsh4ck@kali$ sudo apt install cupp -y
```

## <mark style="color:purple;">**Ejecución básica**</mark>

Para ejecutar CUPP con la configuración predeterminada, simplemente puedes usar:

```bash
cupp -i
```

Este comando iniciará la interfaz interactiva de CUPP, donde te guiará para proporcionar información sobre el usuario.

```shell-session
afsh4ck@kali$ cupp -i

___________
   cupp.py!                 # Common
      \                     # User
       \   ,__,             # Passwords
        \  (oo)____         # Profiler
           (__)    )\
              ||--|| *      [ Muris Kurgas | j0rgan@remote-exploit.org ]
                            [ Mebus | https://github.com/Mebus/]


[+] Insert the information about the victim to make a dictionary
[+] If you don't know all the info, just hit enter when asked! ;)

> First Name: Jane
> Surname: Smith
> Nickname: Janey
> Birthdate (DDMMYYYY): 11121990

> Partners) name: Jim
> Partners) nickname: Jimbo
> Partners) birthdate (DDMMYYYY): 12121990

> Child's name:
> Child's nickname:
> Child's birthdate (DDMMYYYY):

> Pet's name: Spot
> Company name: AHI

> Do you want to add some key words about the victim? Y/[N]: y
> Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed: hacker,blue
> Do you want to add special chars at the end of words? Y/[N]: y
> Do you want to add some random numbers at the end of words? Y/[N]:y
> Leet mode? (i.e. leet = 1337) Y/[N]: y

[+] Now making a dictionary...
[+] Sorting list and removing duplicates...
[+] Saving dictionary to jane.txt, counting 46790 words.
[+] Now load your pistolero with jane.txt and shoot! Good luck!
```

## <mark style="color:purple;">Leet Mode</mark>

El modo leet cambia las letras por un número similar a la letra:

```
Leet mode? (i.e. leet = 1337) Y/[N]: y
```

## <mark style="color:purple;">Filtro de política de contraseñas</mark>

Ya tenemos una lista generada de nombre de user.txt y una lista de contraseñas de jane.txt, pero hay algo más que debemos resolver. CUPP nos ha generado muchas contraseñas posibles, pero la empresa de Jane, AHI, tiene una política de contraseñas bastante peculiar.

* Longitud mínima: 6 caracteres
* Debe incluir:
  * Al menos una letra mayúscula
  * Al menos una letra minúscula
  * Al menos un número
  * Al menos dos caracteres especiales (del conjunto `!@#$%^&*`)

Como hicimos anteriormente, podemos usar grep para filtrar esa lista de contraseñas para que coincida con esa política:

```shell-session
afsh4ck@kali$ grep -E '^.{6,}$' jane.txt | grep -E '[A-Z]' | grep -E '[a-z]' | grep -E '[0-9]' | grep -E '([!@#$%^&*].*){2,}' > jane-filtered.txt
```

Este comando filtra eficientemente `jane.txt` para que coincida con la política proporcionada, desde aproximadamente 46 000 contraseñas hasta aproximadamente 7900. Primero, garantiza una longitud mínima de 6 caracteres, luego busca al menos una letra mayúscula, una minúscula, un número y, finalmente, al menos dos caracteres especiales del conjunto especificado. Los resultados filtrados se almacenan en formato `jane-filtered.txt`.

## <mark style="color:purple;">**Archivo de configuración**</mark>

Puedes usar un archivo de configuración para proporcionar la información del usuario.

```bash
cupp -config config.txt
```

Donde `config.txt` es un archivo que contiene la información del usuario:

{% code title="config.txt" %}

```bash
# Información personal
name = Juan
surname = Perez
nickname = juanito88
birthdate = 1988
birthplace = Madrid
partner = Maria
partner_birthdate = 1990
child = Sofia
child_birthdate = 2015
pet = Rex
company = CyberTech

# Otros datos
words = hacking,football,linux

# Opciones adicionales
leet = y
complexity = y
```

{% endcode %}
